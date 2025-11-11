"""
Integration tests for Undo/Redo comprehensive coverage.

Tests that undo/redo works correctly for all workflows and edge cases.

Run with: blender --background --python -m pytest tests/integration/test_undo_redo.py

NOTE: These tests will FAIL until undo integration is fully implemented.
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


class TestBasicUndo:
    """Test basic undo functionality for each workflow."""
    
    def test_undo_array_workflow(self):
        """Test undo removes Array modifier."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        obj.select_set(True)
        
        bpy.context.scene.copilot_modifier_command = "array"
        bpy.ops.copilot.modifier_assistant()
        
        assert len(obj.modifiers) == 1
        
        bpy.ops.ed.undo()
        
        assert len(obj.modifiers) == 0
    
    def test_undo_hard_surface_workflow(self):
        """Test undo removes both modifiers and shading."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        obj.select_set(True)
        
        bpy.ops.object.shade_flat()
        
        bpy.context.scene.copilot_modifier_command = "hard-surface"
        bpy.ops.copilot.modifier_assistant()
        
        assert len(obj.modifiers) == 2
        
        bpy.ops.ed.undo()
        
        # Both modifiers should be gone
        assert len(obj.modifiers) == 0
    
    def test_undo_symmetrize_workflow(self):
        """Test undo restores deleted vertices."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        obj.select_set(True)
        
        initial_vert_count = len(obj.data.vertices)
        
        bpy.context.scene.copilot_modifier_command = "symmetrize"
        bpy.ops.copilot.modifier_assistant()
        
        # Vertices should be deleted
        assert len(obj.data.vertices) < initial_vert_count
        
        bpy.ops.ed.undo()
        
        # Vertices should be restored
        assert len(obj.data.vertices) == initial_vert_count


class TestRedoFunctionality:
    """Test redo re-executes workflows correctly."""
    
    def test_redo_array_workflow(self):
        """Test redo re-applies Array modifier."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        obj.select_set(True)
        
        bpy.context.scene.copilot_modifier_command = "array"
        bpy.ops.copilot.modifier_assistant()
        
        assert len(obj.modifiers) == 1
        
        bpy.ops.ed.undo()
        assert len(obj.modifiers) == 0
        
        bpy.ops.ed.redo()
        assert len(obj.modifiers) == 1
        assert obj.modifiers[0].type == 'ARRAY'
    
    def test_redo_after_scene_change(self):
        """Test redo works even after selection changes."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        cube1 = bpy.context.object
        
        cube1.select_set(True)
        
        bpy.context.scene.copilot_modifier_command = "solidify"
        bpy.ops.copilot.modifier_assistant()
        
        bpy.ops.ed.undo()
        
        # Change selection
        bpy.ops.mesh.primitive_cube_add(location=(5, 0, 0))
        cube2 = bpy.context.object
        cube1.select_set(False)
        cube2.select_set(True)
        
        # Redo should still work on original object
        bpy.ops.ed.redo()
        
        # Check if redo worked (behavior may vary)
        assert len(cube1.modifiers) == 1 or len(cube2.modifiers) == 1


class TestMultipleUndoRedo:
    """Test undo/redo multiple times in sequence."""
    
    def test_undo_redo_cycle_three_times(self):
        """Test undo-redo-undo-redo cycle."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        obj.select_set(True)
        
        bpy.context.scene.copilot_modifier_command = "solidify"
        bpy.ops.copilot.modifier_assistant()
        
        # Cycle 3 times
        for _ in range(3):
            assert len(obj.modifiers) == 1
            bpy.ops.ed.undo()
            assert len(obj.modifiers) == 0
            bpy.ops.ed.redo()
            assert len(obj.modifiers) == 1
    
    def test_multiple_workflows_undo_sequence(self):
        """Test undoing multiple different workflows."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        obj.select_set(True)
        
        # Execute three workflows
        bpy.context.scene.copilot_modifier_command = "array"
        bpy.ops.copilot.modifier_assistant()
        
        bpy.context.scene.copilot_modifier_command = "solidify"
        bpy.ops.copilot.modifier_assistant()
        
        bpy.context.scene.copilot_modifier_command = "hard-surface"
        bpy.ops.copilot.modifier_assistant()
        
        assert len(obj.modifiers) == 4  # 1 + 1 + 2
        
        # Undo in reverse order
        bpy.ops.ed.undo()
        assert len(obj.modifiers) == 2  # Hard-surface removed
        
        bpy.ops.ed.undo()
        assert len(obj.modifiers) == 1  # Solidify removed
        
        bpy.ops.ed.undo()
        assert len(obj.modifiers) == 0  # Array removed


class TestUndoStackDepth:
    """Test undo stack behavior."""
    
    def test_single_undo_step_per_workflow(self):
        """Test each workflow execution is one undo step."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        obj.select_set(True)
        
        # Hard-surface adds 2 modifiers + shading
        bpy.context.scene.copilot_modifier_command = "hard-surface"
        bpy.ops.copilot.modifier_assistant()
        
        assert len(obj.modifiers) == 2
        
        # Should require only ONE undo
        bpy.ops.ed.undo()
        
        assert len(obj.modifiers) == 0


class TestUndoWithPartialFailure:
    """Test undo behavior when workflow partially fails."""
    
    def test_undo_after_symmetrize_scale_failure(self):
        """Test undo works even if scale application failed."""
        # This test simulates a potential failure scenario
        # Implementation will determine exact behavior
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        obj.select_set(True)
        
        # Try symmetrize (might fail at scale step)
        bpy.context.scene.copilot_modifier_command = "symmetrize"
        result = bpy.ops.copilot.modifier_assistant()
        
        if result == {'FINISHED'}:
            # If it succeeded, undo should work
            bpy.ops.ed.undo()
            # Should restore state
        elif result == {'CANCELLED'}:
            # If it failed, undo should still be safe to call
            bpy.ops.ed.undo()


class TestUndoAfterSelectionChange:
    """Test undo after changing selection."""
    
    def test_undo_with_different_object_selected(self):
        """Test undo works after selecting different object."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        cube1 = bpy.context.object
        
        cube1.select_set(True)
        
        bpy.context.scene.copilot_modifier_command = "array"
        bpy.ops.copilot.modifier_assistant()
        
        assert len(cube1.modifiers) == 1
        
        # Select different object
        bpy.ops.mesh.primitive_cube_add(location=(5, 0, 0))
        cube2 = bpy.context.object
        cube1.select_set(False)
        cube2.select_set(True)
        
        # Undo should still affect cube1
        bpy.ops.ed.undo()
        
        assert len(cube1.modifiers) == 0
    
    def test_undo_with_no_selection(self):
        """Test undo works with no objects selected."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        obj.select_set(True)
        
        bpy.context.scene.copilot_modifier_command = "solidify"
        bpy.ops.copilot.modifier_assistant()
        
        # Deselect all
        bpy.ops.object.select_all(action='DESELECT')
        
        # Undo should still work
        bpy.ops.ed.undo()
        
        assert len(obj.modifiers) == 0


class TestUndoPreservesContext:
    """Test that undo preserves object state correctly."""
    
    def test_undo_preserves_object_location(self):
        """Test undo doesn't affect object location."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        obj.location = (5, 3, 2)
        obj.select_set(True)
        
        bpy.context.scene.copilot_modifier_command = "array"
        bpy.ops.copilot.modifier_assistant()
        
        bpy.ops.ed.undo()
        
        # Location should be unchanged
        assert obj.location.x == pytest.approx(5.0, abs=0.001)
        assert obj.location.y == pytest.approx(3.0, abs=0.001)
        assert obj.location.z == pytest.approx(2.0, abs=0.001)
    
    def test_undo_preserves_object_name(self):
        """Test undo doesn't affect object properties."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        obj.name = "MySpecialCube"
        obj.select_set(True)
        
        bpy.context.scene.copilot_modifier_command = "solidify"
        bpy.ops.copilot.modifier_assistant()
        
        bpy.ops.ed.undo()
        
        assert obj.name == "MySpecialCube"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
