"""
Integration tests for Smart Array workflow.

These tests require an actual Blender instance and test the complete
workflow from command to modifier application.

Run with: blender --background --python -m pytest tests/integration/test_smart_array_workflow.py

NOTE: These tests will FAIL until the workflow is fully implemented.
"""

import sys
from pathlib import Path

# This file requires Blender to be running
try:
    import bpy
    import bmesh
except ImportError:
    print("ERROR: This test requires Blender. Run with: blender --background --python -m pytest")
    sys.exit(1)

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class TestSmartArraySingleObject:
    """Test Smart Array workflow with single mesh object."""
    
    @pytest.fixture(autouse=True)
    def setup_scene(self):
        """Load single_cube.blend fixture before each test."""
        fixture_path = project_root / "tests" / "fixtures" / "single_cube.blend"
        if fixture_path.exists():
            bpy.ops.wm.open_mainfile(filepath=str(fixture_path))
        else:
            # Fallback: create simple scene
            bpy.ops.wm.read_homefile(use_empty=True)
            bpy.ops.mesh.primitive_cube_add()
        yield
        # Cleanup handled by next fixture load
    
    def test_array_modifier_added(self):
        """Test Array modifier is added to selected object."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        # Select the cube
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        # Set command
        bpy.context.scene.copilot_modifier_command = "create an array"
        
        # Execute operator
        bpy.ops.copilot.modifier_assistant()
        
        # Verify modifier exists
        assert len(obj.modifiers) == 1
        assert obj.modifiers[0].type == 'ARRAY'
    
    def test_array_count_is_five(self):
        """Test Array modifier has count=5."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        bpy.context.scene.copilot_modifier_command = "make array"
        bpy.ops.copilot.modifier_assistant()
        
        array_mod = obj.modifiers[0]
        assert array_mod.count == 5
    
    def test_array_offset_x_axis(self):
        """Test Array modifier uses X-axis relative offset."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        bpy.context.scene.copilot_modifier_command = "array"
        bpy.ops.copilot.modifier_assistant()
        
        array_mod = obj.modifiers[0]
        assert array_mod.use_relative_offset is True
        assert array_mod.relative_offset_displace[0] == 1.0
        assert array_mod.relative_offset_displace[1] == 0.0
        assert array_mod.relative_offset_displace[2] == 0.0
    
    def test_no_selection_error(self):
        """Test error when no object selected."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        # Deselect all
        bpy.ops.object.select_all(action='DESELECT')
        
        bpy.context.scene.copilot_modifier_command = "create array"
        result = bpy.ops.copilot.modifier_assistant()
        
        assert result == {'CANCELLED'}
    
    def test_undo_removes_modifier(self):
        """Test undo removes the Array modifier."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        initial_mod_count = len(obj.modifiers)
        
        bpy.context.scene.copilot_modifier_command = "array"
        bpy.ops.copilot.modifier_assistant()
        
        assert len(obj.modifiers) == initial_mod_count + 1
        
        # Undo
        bpy.ops.ed.undo()
        
        assert len(obj.modifiers) == initial_mod_count


class TestSmartArrayObjectOffset:
    """Test Smart Array workflow with mesh + empty (object offset variant)."""
    
    @pytest.fixture(autouse=True)
    def setup_scene(self):
        """Load cube_and_empty.blend fixture before each test."""
        fixture_path = project_root / "tests" / "fixtures" / "cube_and_empty.blend"
        if fixture_path.exists():
            bpy.ops.wm.open_mainfile(filepath=str(fixture_path))
        else:
            # Fallback: create scene manually
            bpy.ops.wm.read_homefile(use_empty=True)
            bpy.ops.mesh.primitive_cube_add()
            bpy.ops.object.empty_add(type='PLAIN_AXES')
        yield
    
    def test_identifies_mesh_and_empty(self):
        """Test workflow correctly identifies mesh vs empty."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        # Select both objects
        bpy.ops.object.select_all(action='SELECT')
        
        # Find mesh object
        mesh_obj = [o for o in bpy.context.selected_objects if o.type == 'MESH'][0]
        
        bpy.context.scene.copilot_modifier_command = "array with offset"
        bpy.ops.copilot.modifier_assistant()
        
        # Modifier should be on mesh, not empty
        assert len(mesh_obj.modifiers) == 1
    
    def test_array_uses_empty_as_offset(self):
        """Test Array modifier references empty object."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        bpy.ops.object.select_all(action='SELECT')
        
        mesh_obj = [o for o in bpy.context.selected_objects if o.type == 'MESH'][0]
        empty_obj = [o for o in bpy.context.selected_objects if o.type == 'EMPTY'][0]
        
        bpy.context.scene.copilot_modifier_command = "create array"
        bpy.ops.copilot.modifier_assistant()
        
        array_mod = mesh_obj.modifiers[0]
        assert array_mod.use_object_offset is True
        assert array_mod.offset_object == empty_obj
    
    def test_relative_offset_disabled(self):
        """Test relative offset is disabled when using object offset."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        bpy.ops.object.select_all(action='SELECT')
        
        mesh_obj = [o for o in bpy.context.selected_objects if o.type == 'MESH'][0]
        
        bpy.context.scene.copilot_modifier_command = "array"
        bpy.ops.copilot.modifier_assistant()
        
        array_mod = mesh_obj.modifiers[0]
        assert array_mod.use_relative_offset is False


class TestSmartArrayErrorCases:
    """Test error handling for Smart Array workflow."""
    
    def test_wrong_object_type_error(self):
        """Test error with non-mesh object types."""
        # Create camera instead of mesh
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.object.camera_add()
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        bpy.context.scene.copilot_modifier_command = "create array"
        result = bpy.ops.copilot.modifier_assistant()
        
        # Should fail validation (camera not supported)
        assert result == {'CANCELLED'}
    
    def test_wrong_mode_error(self):
        """Test error when not in Object Mode."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        
        # Enter Edit Mode
        bpy.ops.object.mode_set(mode='EDIT')
        
        bpy.context.scene.copilot_modifier_command = "array"
        result = bpy.ops.copilot.modifier_assistant()
        
        assert result == {'CANCELLED'}
        
        # Return to object mode for cleanup
        bpy.ops.object.mode_set(mode='OBJECT')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
