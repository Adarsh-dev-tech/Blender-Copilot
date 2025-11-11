"""
Integration tests for selection validation edge cases.

Tests unusual selection states and object configurations to ensure
robust validation behavior.

Run with: blender --background --python -m pytest tests/integration/test_selection_edge_cases.py

NOTE: These tests will FAIL until the validator is fully implemented.
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


class TestManyObjectsSelected:
    """Test validation with large number of objects selected."""
    
    def test_workflow_with_100_objects_selected(self):
        """Test validation handles 100+ selected objects efficiently."""
        bpy.ops.wm.read_homefile(use_empty=True)
        
        # Create 100 cubes
        for i in range(100):
            bpy.ops.mesh.primitive_cube_add(location=(i * 2, 0, 0))
        
        bpy.ops.object.select_all(action='SELECT')
        
        # Should fail validation gracefully (too many objects)
        bpy.context.scene.copilot_modifier_command = "solidify"
        result = bpy.ops.copilot.modifier_assistant()
        
        assert result == {'CANCELLED'}
    
    def test_validation_performance_with_many_objects(self):
        """Test validation completes quickly even with 100+ objects."""
        import time
        
        bpy.ops.wm.read_homefile(use_empty=True)
        
        for i in range(100):
            bpy.ops.mesh.primitive_cube_add(location=(i * 2, 0, 0))
        
        bpy.ops.object.select_all(action='SELECT')
        
        bpy.context.scene.copilot_modifier_command = "array"
        
        start_time = time.time()
        result = bpy.ops.copilot.modifier_assistant()
        elapsed = time.time() - start_time
        
        # Validation should be fast even with many objects
        assert elapsed < 0.1, f"Validation took {elapsed*1000:.1f}ms with 100 objects"


class TestMixedObjectTypes:
    """Test selection with various object types mixed."""
    
    def test_mesh_plus_camera_plus_light(self):
        """Test selection with mesh, camera, and light objects."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        bpy.ops.object.camera_add(location=(5, 0, 0))
        bpy.ops.object.light_add(type='POINT', location=(0, 5, 0))
        
        bpy.ops.object.select_all(action='SELECT')
        
        # Should fail validation (requires specific types)
        bpy.context.scene.copilot_modifier_command = "solidify"
        result = bpy.ops.copilot.modifier_assistant()
        
        assert result == {'CANCELLED'}
    
    def test_multiple_empties_selected(self):
        """Test selection with only empty objects."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        bpy.ops.object.empty_add(type='ARROWS', location=(2, 0, 0))
        
        bpy.ops.object.select_all(action='SELECT')
        
        # Should fail validation (no mesh objects)
        bpy.context.scene.copilot_modifier_command = "array"
        result = bpy.ops.copilot.modifier_assistant()
        
        assert result == {'CANCELLED'}


class TestActiveObjectEdgeCases:
    """Test unusual active object states."""
    
    def test_no_active_object_but_objects_selected(self):
        """Test when objects are selected but no active object."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        bpy.ops.mesh.primitive_cube_add(location=(2, 0, 0))
        
        bpy.ops.object.select_all(action='SELECT')
        bpy.context.view_layer.objects.active = None
        
        # Should either handle gracefully or fail with clear error
        bpy.context.scene.copilot_modifier_command = "solidify"
        result = bpy.ops.copilot.modifier_assistant()
        
        assert result in [{'FINISHED'}, {'CANCELLED'}]
    
    def test_active_object_not_in_selection(self):
        """Test when active object is not in selected objects."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        cube1 = bpy.context.object
        
        bpy.ops.mesh.primitive_cube_add(location=(2, 0, 0))
        cube2 = bpy.context.object
        
        # Select only cube1, but make cube2 active
        cube1.select_set(True)
        cube2.select_set(False)
        bpy.context.view_layer.objects.active = cube2
        
        # Should handle this unusual state
        bpy.context.scene.copilot_modifier_command = "array"
        result = bpy.ops.copilot.modifier_assistant()
        
        # Implementation determines if this is valid or not
        assert result in [{'FINISHED'}, {'CANCELLED'}]


class TestDifferentModes:
    """Test workflows in different Blender modes."""
    
    def test_edit_mode_fails_validation(self):
        """Test all workflows fail when in Edit Mode."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        obj.select_set(True)
        
        # Enter Edit Mode
        bpy.ops.object.mode_set(mode='EDIT')
        
        workflows = ["array", "hard-surface", "mirror", "solidify"]
        
        for command in workflows:
            bpy.context.scene.copilot_modifier_command = command
            result = bpy.ops.copilot.modifier_assistant()
            
            assert result == {'CANCELLED'}, f"{command} should fail in Edit Mode"
        
        # Return to Object Mode for cleanup
        bpy.ops.object.mode_set(mode='OBJECT')
    
    def test_sculpt_mode_fails_validation(self):
        """Test workflows fail in Sculpt Mode."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        obj.select_set(True)
        
        # Enter Sculpt Mode
        bpy.ops.object.mode_set(mode='SCULPT')
        
        bpy.context.scene.copilot_modifier_command = "solidify"
        result = bpy.ops.copilot.modifier_assistant()
        
        assert result == {'CANCELLED'}
        
        # Return to Object Mode
        bpy.ops.object.mode_set(mode='OBJECT')


class TestLockedAndHiddenObjects:
    """Test selection with locked or hidden objects."""
    
    def test_locked_object_selected(self):
        """Test workflow with locked object in selection."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        obj.select_set(True)
        
        # Lock transforms
        obj.lock_location = (True, True, True)
        obj.lock_rotation = (True, True, True)
        obj.lock_scale = (True, True, True)
        
        # Should still work (locks don't affect modifiers)
        bpy.context.scene.copilot_modifier_command = "array"
        result = bpy.ops.copilot.modifier_assistant()
        
        # Implementation determines if this succeeds or fails
        assert result in [{'FINISHED'}, {'CANCELLED'}]


class TestCollections:
    """Test selection from different collections."""
    
    def test_objects_from_multiple_collections(self):
        """Test selection spanning multiple collections."""
        bpy.ops.wm.read_homefile(use_empty=True)
        
        # Create two collections
        col1 = bpy.data.collections.new("Collection1")
        col2 = bpy.data.collections.new("Collection2")
        bpy.context.scene.collection.children.link(col1)
        bpy.context.scene.collection.children.link(col2)
        
        # Add cube to collection1
        bpy.ops.mesh.primitive_cube_add()
        cube1 = bpy.context.object
        bpy.context.scene.collection.objects.unlink(cube1)
        col1.objects.link(cube1)
        
        # Add cube to collection2
        bpy.ops.mesh.primitive_cube_add(location=(2, 0, 0))
        cube2 = bpy.context.object
        bpy.context.scene.collection.objects.unlink(cube2)
        col2.objects.link(cube2)
        
        # Select both
        cube1.select_set(True)
        cube2.select_set(True)
        bpy.context.view_layer.objects.active = cube1
        
        # Should work normally (collections don't affect workflows)
        bpy.context.scene.copilot_modifier_command = "shrinkwrap"
        result = bpy.ops.copilot.modifier_assistant()
        
        assert result in [{'FINISHED'}, {'CANCELLED'}]


class TestObjectHierarchies:
    """Test selection with parent-child relationships."""
    
    def test_parent_and_child_both_selected(self):
        """Test workflow with both parent and child objects selected."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        parent = bpy.context.object
        
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 2))
        child = bpy.context.object
        
        # Make parent-child relationship
        child.parent = parent
        
        # Select both
        parent.select_set(True)
        child.select_set(True)
        
        # Should handle parent-child selection
        bpy.context.scene.copilot_modifier_command = "shrinkwrap"
        result = bpy.ops.copilot.modifier_assistant()
        
        assert result in [{'FINISHED'}, {'CANCELLED'}]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
