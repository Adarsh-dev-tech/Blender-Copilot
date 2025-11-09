"""Context Validator for Intelligent Modifier Assistant.

This module validates Blender selection context against workflow requirements.
Provides specific error messages matching the operator contract.
"""

from typing import Optional
import bpy  # noqa: F401


def _get_performance_mode() -> bool:
    """Check if performance mode is enabled in preferences."""
    try:
        from copilot.preferences import get_addon_preferences
        prefs = get_addon_preferences()
        return prefs.performance_mode if prefs else False
    except (ImportError, KeyError):
        return False


def validate_context(workflow_type: str) -> tuple[bool, str]:
    """Validate current Blender context against workflow requirements.

    Performance target: < 20ms

    Args:
        workflow_type: The workflow identifier (e.g., 'SMART_ARRAY')

    Returns:
        Tuple of (is_valid, error_message)
        - If valid: (True, "")
        - If invalid: (False, "Specific error message")

    Examples:
        >>> # With no selection
        >>> validate_context('SMART_ARRAY')
        (False, "Please select an object first")
    
    Note:
        If performance mode is enabled in preferences, some validations may be skipped.
    """
    # Validation routing by workflow type
    validators = {
        'SMART_ARRAY': _validate_smart_array,
        'HARD_SURFACE': _validate_single_mesh,
        'SYMMETRIZE': _validate_single_mesh,
        'CURVE_DEFORM': _validate_mesh_and_curve,
        'SOLIDIFY': _validate_single_mesh,
        'SHRINKWRAP': _validate_two_meshes,
    }

    validator = validators.get(workflow_type)
    if validator is None:
        return False, f"Unknown workflow type: {workflow_type}"

    return validator()


def _validate_smart_array() -> tuple[bool, str]:
    """Validate for Smart Array workflow (1 mesh OR 1 mesh + 1 empty)."""
    context = bpy.context
    selected = context.selected_objects

    # Check for selection
    if not selected:
        return False, "Please select an object first"

    # Check mode
    if context.mode != 'OBJECT':
        return False, f"This command must be run in Object Mode (currently in {context.mode})"

    # Count object types
    type_counts = _count_object_types(selected)
    num_objects = len(selected)

    # Variant 1: Single mesh
    if num_objects == 1 and type_counts.get('MESH') == 1:
        return True, ""

    # Variant 2: Mesh + Empty
    if num_objects == 2 and type_counts.get('MESH') == 1 and type_counts.get('EMPTY') == 1:
        return True, ""

    # Invalid configuration
    if num_objects == 1:
        return False, "This command requires a mesh object to be selected"
    elif num_objects == 2:
        return False, "This command requires two selected objects: a mesh and an empty"
    else:
        return False, f"This command requires 1 or 2 selected object(s), but {num_objects} are selected"


def _validate_single_mesh() -> tuple[bool, str]:
    """Validate for workflows requiring exactly 1 mesh object."""
    context = bpy.context
    selected = context.selected_objects

    # Check for selection
    if not selected:
        return False, "Please select an object first"

    # Check mode
    if context.mode != 'OBJECT':
        return False, f"This command must be run in Object Mode (currently in {context.mode})"

    # Check count
    if len(selected) != 1:
        return False, f"This command requires 1 selected object(s), but {len(selected)} are selected"

    # Check type
    if selected[0].type != 'MESH':
        return False, "This command requires a mesh object to be selected"

    return True, ""


def _validate_mesh_and_curve() -> tuple[bool, str]:
    """Validate for Curve Deform workflow (1 mesh + 1 curve)."""
    context = bpy.context
    selected = context.selected_objects

    # Check for selection
    if not selected:
        return False, "Please select an object first"

    # Check mode
    if context.mode != 'OBJECT':
        return False, f"This command must be run in Object Mode (currently in {context.mode})"

    # Check count
    if len(selected) != 2:
        return False, f"This command requires 2 selected object(s), but {len(selected)} are selected"

    # Check types
    type_counts = _count_object_types(selected)
    if type_counts.get('MESH') == 1 and type_counts.get('CURVE') == 1:
        return True, ""

    return False, "This command requires two selected objects: a mesh and a curve"


def _validate_two_meshes() -> tuple[bool, str]:
    """Validate for Shrinkwrap workflow (2 meshes with active object)."""
    context = bpy.context
    selected = context.selected_objects
    active = context.active_object

    # Check for selection
    if not selected:
        return False, "Please select an object first"

    # Check mode
    if context.mode != 'OBJECT':
        return False, f"This command must be run in Object Mode (currently in {context.mode})"

    # Check count
    if len(selected) != 2:
        return False, f"This command requires 2 selected object(s), but {len(selected)} are selected"

    # Check types
    type_counts = _count_object_types(selected)
    if type_counts.get('MESH') != 2:
        return False, "This command requires two mesh objects to be selected"

    # Check active object
    if active is None or active not in selected:
        return False, "Please ensure one of the selected objects is active"

    return True, ""


def _count_object_types(objects: list) -> dict[str, int]:
    """Count objects by type.

    Args:
        objects: List of Blender objects

    Returns:
        Dictionary mapping object types to counts
        Example: {'MESH': 2, 'EMPTY': 1}
    """
    type_counts: dict[str, int] = {}
    for obj in objects:
        obj_type = obj.type
        type_counts[obj_type] = type_counts.get(obj_type, 0) + 1
    return type_counts
