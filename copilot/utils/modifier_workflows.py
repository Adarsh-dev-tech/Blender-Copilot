"""Modifier Workflows for Intelligent Modifier Assistant.

This module implements the six automated modifier workflows.
Each workflow applies modifiers with optimized settings and handles prerequisites.
"""

from typing import Optional
import bpy  # noqa: F401
import bmesh  # noqa: F401


def _get_preferences():
    """Get add-on preferences with defaults fallback."""
    try:
        from copilot.preferences import get_addon_preferences
        return get_addon_preferences()
    except (ImportError, KeyError):
        # Fallback to None if preferences not available
        return None


def apply_smart_array_single(obj: 'bpy.types.Object') -> tuple[set, str]:
    """Apply Smart Array workflow to a single mesh object.

    Adds Array modifier with count and offset from preferences (default: 5 copies, X=1.0).

    Args:
        obj: Target mesh object

    Returns:
        Tuple of (status, message)
        - status: {'FINISHED'} or {'CANCELLED'}
        - message: User feedback string

    Performance target: < 50ms
    """
    try:
        # Get preferences or use hardcoded defaults
        prefs = _get_preferences()
        count = prefs.default_array_count if prefs else 5
        offset_x = prefs.default_array_offset_x if prefs else 1.0
        
        # Add Array modifier
        modifier = obj.modifiers.new(name="Array", type='ARRAY')

        # Configure for X-axis duplication
        modifier.count = count
        modifier.use_relative_offset = True
        modifier.relative_offset_displace = (offset_x, 0.0, 0.0)

        return {'FINISHED'}, f"Array modifier added with {count} copies on X-axis (offset {offset_x})"

    except Exception as e:
        return {'CANCELLED'}, f"Failed to add Array modifier: {str(e)}"


def apply_smart_array_controlled(
    mesh_obj: 'bpy.types.Object',
    empty_obj: 'bpy.types.Object'
) -> tuple[set, str]:
    """Apply Smart Array workflow with empty object control.

    Adds Array modifier to mesh using empty object as offset controller.

    Args:
        mesh_obj: Target mesh object
        empty_obj: Empty object for offset control

    Returns:
        Tuple of (status, message)

    Performance target: < 50ms
    """
    try:
        # Add Array modifier to mesh
        modifier = mesh_obj.modifiers.new(name="Array", type='ARRAY')

        # Configure for object offset
        modifier.use_relative_offset = False
        modifier.use_object_offset = True
        modifier.offset_object = empty_obj

        return {'FINISHED'}, "Array modifier added with empty object control"

    except Exception as e:
        return {'CANCELLED'}, f"Failed to add Array modifier: {str(e)}"


def apply_hard_surface_setup(obj: 'bpy.types.Object') -> tuple[set, str]:
    """Apply Hard-Surface SubD workflow.

    Adds Bevel modifier followed by Subdivision Surface, then sets smooth shading.
    Modifier order is critical for correct hard-surface appearance.
    Uses preferences for bevel segments and subdivision levels.

    Args:
        obj: Target mesh object

    Returns:
        Tuple of (status, message)

    Performance target: < 100ms
    """
    try:
        # Get preferences or use hardcoded defaults
        prefs = _get_preferences()
        bevel_segments = prefs.default_bevel_segments if prefs else 3
        subsurf_levels = prefs.default_subdivision_levels if prefs else 2
        
        # Add Bevel modifier first
        bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
        bevel.limit_method = 'ANGLE'
        bevel.segments = bevel_segments

        # Add Subdivision Surface modifier after Bevel
        subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
        subsurf.levels = subsurf_levels

        # Set smooth shading
        # Need to use mesh data for shading (deprecated ops method)
        mesh = obj.data
        for poly in mesh.polygons:
            poly.use_smooth = True

        return {'FINISHED'}, "Hard-surface setup applied (Bevel + Subdivision + Smooth)"

    except Exception as e:
        return {'CANCELLED'}, f"Failed to apply hard-surface setup: {str(e)}"


def apply_symmetrize(obj: 'bpy.types.Object') -> tuple[set, str]:
    """Apply Symmetrize workflow (Mirror with geometry cleanup).

    Multi-step workflow:
    1. Apply scale transformation
    2. Add Mirror modifier on X-axis
    3. Delete vertices on positive X side

    Args:
        obj: Target mesh object

    Returns:
        Tuple of (status, message)

    Performance target: < 200ms
    """
    try:
        # Step 1: Apply scale
        # Store current mode to restore later
        original_mode = bpy.context.mode

        # Ensure we're in object mode
        if bpy.context.active_object != obj:
            bpy.context.view_layer.objects.active = obj

        if original_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        # Apply scale transformation
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        # Step 2: Add Mirror modifier
        mirror = obj.modifiers.new(name="Mirror", type='MIRROR')
        mirror.use_axis = (True, False, False)  # X-axis
        mirror.use_bisect_axis = (True, False, False)
        mirror.use_clip = True

        # Step 3: Delete positive X vertices
        # Enter Edit Mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Use bmesh for vertex operations
        mesh = obj.data
        bm = bmesh.from_edit_mesh(mesh)

        # Deselect all
        for vert in bm.verts:
            vert.select = False

        # Select vertices where x > 0
        verts_to_delete = [v for v in bm.verts if v.co.x > 0.0]
        for vert in verts_to_delete:
            vert.select = True

        # Delete selected vertices
        bmesh.ops.delete(bm, geom=verts_to_delete, context='VERTS')

        # Update mesh
        bmesh.update_edit_mesh(mesh)

        # Return to Object Mode
        bpy.ops.object.mode_set(mode='OBJECT')

        return {'FINISHED'}, "Symmetrize applied on X-axis (scale applied, positive X deleted)"

    except Exception as e:
        # Ensure we return to object mode on error
        try:
            if bpy.context.mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')
        except:  # noqa: E722
            pass
        return {'CANCELLED'}, f"Failed to apply symmetrize: {str(e)}"


def apply_curve_deform(
    mesh_obj: 'bpy.types.Object',
    curve_obj: 'bpy.types.Object'
) -> tuple[set, str]:
    """Apply Curve Deform workflow.

    Multi-step workflow:
    1. Apply scale to both objects
    2. Align mesh origin to curve origin
    3. Add Curve modifier to mesh

    Args:
        mesh_obj: Target mesh object to deform
        curve_obj: Curve object to deform along

    Returns:
        Tuple of (status, message)

    Performance target: < 150ms
    """
    try:
        # Store original active object
        original_active = bpy.context.active_object

        # Step 1: Apply scale to mesh
        bpy.context.view_layer.objects.active = mesh_obj
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        # Step 2: Apply scale to curve
        bpy.context.view_layer.objects.active = curve_obj
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        # Step 3: Align mesh origin to curve origin
        mesh_obj.location = curve_obj.location.copy()

        # Step 4: Add Curve modifier to mesh
        bpy.context.view_layer.objects.active = mesh_obj
        modifier = mesh_obj.modifiers.new(name="Curve", type='CURVE')
        modifier.object = curve_obj

        # Restore original active object
        bpy.context.view_layer.objects.active = original_active

        return {'FINISHED'}, "Curve deform applied (scales applied, origins aligned)"

    except Exception as e:
        return {'CANCELLED'}, f"Failed to apply curve deform: {str(e)}"


def apply_solidify(obj: 'bpy.types.Object') -> tuple[set, str]:
    """Apply Solidify workflow.

    Adds Solidify modifier with thickness from preferences (default: 0.01m).

    Args:
        obj: Target mesh object

    Returns:
        Tuple of (status, message)

    Performance target: < 50ms
    """
    try:
        # Get preferences or use hardcoded defaults
        prefs = _get_preferences()
        thickness = prefs.default_solidify_thickness if prefs else 0.01
        
        # Add Solidify modifier
        modifier = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
        modifier.thickness = thickness
        modifier.use_even_offset = True

        return {'FINISHED'}, f"Solidify modifier added (thickness: {thickness:.4f}m, even offset enabled)"

    except Exception as e:
        return {'CANCELLED'}, f"Failed to add Solidify modifier: {str(e)}"


def apply_shrinkwrap(
    source_obj: 'bpy.types.Object',
    target_obj: 'bpy.types.Object'
) -> tuple[set, str]:
    """Apply Shrinkwrap workflow.

    Adds Shrinkwrap modifier to source object targeting another mesh.

    Args:
        source_obj: Object to wrap (active object)
        target_obj: Object to wrap to (non-active selected object)

    Returns:
        Tuple of (status, message)

    Performance target: < 50ms
    """
    try:
        # Add Shrinkwrap modifier to source
        modifier = source_obj.modifiers.new(name="Shrinkwrap", type='SHRINKWRAP')
        modifier.target = target_obj
        modifier.wrap_method = 'NEAREST_SURFACEPOINT'

        return {'FINISHED'}, f"Shrinkwrap modifier added (target: {target_obj.name})"

    except Exception as e:
        return {'CANCELLED'}, f"Failed to add Shrinkwrap modifier: {str(e)}"


def identify_mesh_and_empty(
    obj1: 'bpy.types.Object',
    obj2: 'bpy.types.Object'
) -> tuple[Optional['bpy.types.Object'], Optional['bpy.types.Object']]:
    """Identify which object is mesh and which is empty.

    Args:
        obj1: First object
        obj2: Second object

    Returns:
        Tuple of (mesh_obj, empty_obj) or (None, None) if types don't match
    """
    if obj1.type == 'MESH' and obj2.type == 'EMPTY':
        return obj1, obj2
    elif obj1.type == 'EMPTY' and obj2.type == 'MESH':
        return obj2, obj1
    else:
        return None, None


def identify_mesh_and_curve(
    obj1: 'bpy.types.Object',
    obj2: 'bpy.types.Object'
) -> tuple[Optional['bpy.types.Object'], Optional['bpy.types.Object']]:
    """Identify which object is mesh and which is curve.

    Args:
        obj1: First object
        obj2: Second object

    Returns:
        Tuple of (mesh_obj, curve_obj) or (None, None) if types don't match
    """
    if obj1.type == 'MESH' and obj2.type == 'CURVE':
        return obj1, obj2
    elif obj1.type == 'CURVE' and obj2.type == 'MESH':
        return obj2, obj1
    else:
        return None, None
