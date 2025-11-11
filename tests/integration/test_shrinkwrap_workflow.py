"""
Integration tests for Shrinkwrap workflow.

Tests workflow with two mesh objects where one wraps to the other.

Run with: blender --background --python -m pytest tests/integration/test_shrinkwrap_workflow.py

NOTE: These tests will FAIL until the workflow is fully implemented.
"""

import sys
from pathlib import Path

try:
    import bpy
except ImportError:
    print("ERROR: This test requires Blender. Run with: blender --background --python -m pytest")
    sys.exit(1)

import pytest

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class TestShrinkwrapWorkflow:
    """Test Shrinkwrap workflow."""
    
    @pytest.fixture(autouse=True)
    def setup_scene(self):
        """Load two_cubes.blend fixture before each test."""
        fixture_path = project_root / "tests" / "fixtures" / "two_cubes.blend"
        if fixture_path.exists():
            bpy.ops.wm.open_mainfile(filepath=str(fixture_path))
        else:
            bpy.ops.wm.read_homefile(use_empty=True)
            bpy.ops.mesh.primitive_cube_add()
            bpy.ops.mesh.primitive_cube_add(location=(3, 0, 0))
        yield
    
    def test_shrinkwrap_modifier_added_to_active(self):
        """Test Shrinkwrap modifier is added to active object."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        bpy.ops.object.select_all(action='SELECT')
        
        active_obj = bpy.context.view_layer.objects.active
        
        bpy.context.scene.copilot_modifier_command = "shrinkwrap"
        bpy.ops.copilot.modifier_assistant()
        
        shrinkwrap_mods = [m for m in active_obj.modifiers if m.type == 'SHRINKWRAP']
        assert len(shrinkwrap_mods) == 1
    
    def test_target_is_non_active_object(self):
        """Test non-active object is set as shrinkwrap target."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        bpy.ops.object.select_all(action='SELECT')
        
        active_obj = bpy.context.view_layer.objects.active
        non_active_objs = [o for o in bpy.context.selected_objects if o != active_obj]
        
        bpy.context.scene.copilot_modifier_command = "wrap to surface"
        bpy.ops.copilot.modifier_assistant()
        
        shrinkwrap_mod = [m for m in active_obj.modifiers if m.type == 'SHRINKWRAP'][0]
        assert shrinkwrap_mod.target in non_active_objs
    
    def test_wrap_method_nearest_surface(self):
        """Test shrinkwrap uses NEAREST_SURFACEPOINT method."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        bpy.ops.object.select_all(action='SELECT')
        
        active_obj = bpy.context.view_layer.objects.active
        
        bpy.context.scene.copilot_modifier_command = "conform to mesh"
        bpy.ops.copilot.modifier_assistant()
        
        shrinkwrap_mod = [m for m in active_obj.modifiers if m.type == 'SHRINKWRAP'][0]
        assert shrinkwrap_mod.wrap_method == 'NEAREST_SURFACEPOINT'
    
    def test_target_object_has_no_modifier(self):
        """Test target object doesn't get a modifier."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        bpy.ops.object.select_all(action='SELECT')
        
        active_obj = bpy.context.view_layer.objects.active
        non_active_objs = [o for o in bpy.context.selected_objects if o != active_obj]
        
        bpy.context.scene.copilot_modifier_command = "shrinkwrap"
        bpy.ops.copilot.modifier_assistant()
        
        # Target should have no modifiers
        for obj in non_active_objs:
            assert len([m for m in obj.modifiers if m.type == 'SHRINKWRAP']) == 0
    
    def test_works_with_different_mesh_types(self):
        """Test workflow works with different mesh geometries."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_uv_sphere_add()
        sphere = bpy.context.object
        
        bpy.ops.mesh.primitive_plane_add(location=(0, 0, -2))
        plane = bpy.context.object
        
        bpy.ops.object.select_all(action='SELECT')
        bpy.context.view_layer.objects.active = plane
        
        bpy.context.scene.copilot_modifier_command = "shrinkwrap"
        result = bpy.ops.copilot.modifier_assistant()
        
        assert result == {'FINISHED'}
        assert len([m for m in plane.modifiers if m.type == 'SHRINKWRAP']) == 1
    
    def test_undo_removes_modifier(self):
        """Test undo removes Shrinkwrap modifier."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        bpy.ops.object.select_all(action='SELECT')
        
        active_obj = bpy.context.view_layer.objects.active
        
        bpy.context.scene.copilot_modifier_command = "shrinkwrap"
        bpy.ops.copilot.modifier_assistant()
        
        assert len([m for m in active_obj.modifiers if m.type == 'SHRINKWRAP']) == 1
        
        # Undo
        bpy.ops.ed.undo()
        
        assert len([m for m in active_obj.modifiers if m.type == 'SHRINKWRAP']) == 0


class TestShrinkwrapErrorCases:
    """Test error handling for Shrinkwrap workflow."""
    
    def test_only_one_object_error(self):
        """Test error when only one object selected."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        obj.select_set(True)
        
        bpy.context.scene.copilot_modifier_command = "shrinkwrap"
        result = bpy.ops.copilot.modifier_assistant()
        
        assert result == {'CANCELLED'}
    
    def test_no_active_object_error(self):
        """Test error when no active object but objects selected."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        bpy.ops.mesh.primitive_cube_add(location=(2, 0, 0))
        bpy.ops.object.select_all(action='SELECT')
        
        # Clear active object
        bpy.context.view_layer.objects.active = None
        
        bpy.context.scene.copilot_modifier_command = "shrinkwrap"
        result = bpy.ops.copilot.modifier_assistant()
        
        # Should handle gracefully (either succeed by picking one or fail with clear error)
        assert result in [{'FINISHED'}, {'CANCELLED'}]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
