"""
Integration tests for workflow chaining.

Tests running multiple workflows on the same object in sequence.

Run with: blender --background --python -m pytest tests/integration/test_workflow_chaining.py

NOTE: These tests will FAIL until all workflows are fully implemented.
"""

import sys
from pathlib import Path
import time

try:
    import bpy
except ImportError:
    print("ERROR: This test requires Blender. Run with: blender --background --python -m pytest")
    sys.exit(1)

import pytest

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class TestSimpleChaining:
    """Test chaining two workflows."""
    
    def test_array_then_solidify(self):
        """Test Array workflow followed by Solidify."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        obj.select_set(True)
        
        # First workflow
        bpy.context.scene.copilot_modifier_command = "array"
        result1 = bpy.ops.copilot.modifier_assistant()
        
        # Second workflow
        bpy.context.scene.copilot_modifier_command = "solidify"
        result2 = bpy.ops.copilot.modifier_assistant()
        
        assert result1 == {'FINISHED'}
        assert result2 == {'FINISHED'}
        assert len(obj.modifiers) == 2
        assert obj.modifiers[0].type == 'ARRAY'
        assert obj.modifiers[1].type == 'SOLIDIFY'
    
    def test_mirror_then_array(self):
        """Test Symmetrize workflow followed by Array."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        obj.select_set(True)
        
        # First workflow (modifies geometry)
        bpy.context.scene.copilot_modifier_command = "mirror"
        result1 = bpy.ops.copilot.modifier_assistant()
        
        # Second workflow
        bpy.context.scene.copilot_modifier_command = "array"
        result2 = bpy.ops.copilot.modifier_assistant()
        
        assert result1 == {'FINISHED'}
        assert result2 == {'FINISHED'}
        assert len(obj.modifiers) == 2


class TestThreeWorkflowChain:
    """Test chaining three workflows."""
    
    def test_array_solidify_hard_surface(self):
        """Test Array → Solidify → Hard-Surface chain."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        obj.select_set(True)
        
        # Workflow 1
        bpy.context.scene.copilot_modifier_command = "array"
        bpy.ops.copilot.modifier_assistant()
        
        # Workflow 2
        bpy.context.scene.copilot_modifier_command = "solidify"
        bpy.ops.copilot.modifier_assistant()
        
        # Workflow 3
        bpy.context.scene.copilot_modifier_command = "hard-surface"
        bpy.ops.copilot.modifier_assistant()
        
        # Should have 4 modifiers total (1 + 1 + 2)
        assert len(obj.modifiers) == 4
        assert obj.modifiers[0].type == 'ARRAY'
        assert obj.modifiers[1].type == 'SOLIDIFY'
        assert obj.modifiers[2].type == 'BEVEL'
        assert obj.modifiers[3].type == 'SUBSURF'


class TestModifierStackOrdering:
    """Test that modifier stack order is preserved when chaining."""
    
    def test_modifier_order_preserved(self):
        """Test modifiers stay in execution order."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        obj.select_set(True)
        
        # Execute workflows in specific order
        workflows = ["array", "solidify", "hard-surface"]
        
        for workflow in workflows:
            bpy.context.scene.copilot_modifier_command = workflow
            bpy.ops.copilot.modifier_assistant()
        
        # Check order
        modifier_types = [m.type for m in obj.modifiers]
        expected = ['ARRAY', 'SOLIDIFY', 'BEVEL', 'SUBSURF']
        assert modifier_types == expected


class TestUndoWithChaining:
    """Test undo behavior with chained workflows."""
    
    def test_undo_removes_most_recent_workflow(self):
        """Test undo removes only the most recent workflow."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        obj.select_set(True)
        
        # Chain two workflows
        bpy.context.scene.copilot_modifier_command = "array"
        bpy.ops.copilot.modifier_assistant()
        
        bpy.context.scene.copilot_modifier_command = "solidify"
        bpy.ops.copilot.modifier_assistant()
        
        assert len(obj.modifiers) == 2
        
        # Undo should remove only Solidify
        bpy.ops.ed.undo()
        
        assert len(obj.modifiers) == 1
        assert obj.modifiers[0].type == 'ARRAY'
    
    def test_undo_all_chained_workflows(self):
        """Test undoing entire chain step by step."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        obj.select_set(True)
        
        # Chain three workflows
        workflows = ["array", "solidify", "hard-surface"]
        for workflow in workflows:
            bpy.context.scene.copilot_modifier_command = workflow
            bpy.ops.copilot.modifier_assistant()
        
        # Undo all three
        bpy.ops.ed.undo()  # Remove hard-surface
        assert len(obj.modifiers) == 2
        
        bpy.ops.ed.undo()  # Remove solidify
        assert len(obj.modifiers) == 1
        
        bpy.ops.ed.undo()  # Remove array
        assert len(obj.modifiers) == 0


class TestComplexChaining:
    """Test complex workflow combinations."""
    
    def test_curve_deform_then_solidify(self):
        """Test Curve Deform followed by Solidify."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        bpy.ops.curve.primitive_bezier_curve_add(location=(2, 0, 0))
        
        bpy.ops.object.select_all(action='SELECT')
        
        mesh_obj = [o for o in bpy.context.selected_objects if o.type == 'MESH'][0]
        
        # Workflow 1: Curve Deform
        bpy.context.scene.copilot_modifier_command = "curve deform"
        result1 = bpy.ops.copilot.modifier_assistant()
        
        # Workflow 2: Solidify (only mesh selected now)
        bpy.ops.object.select_all(action='DESELECT')
        mesh_obj.select_set(True)
        bpy.context.view_layer.objects.active = mesh_obj
        
        bpy.context.scene.copilot_modifier_command = "solidify"
        result2 = bpy.ops.copilot.modifier_assistant()
        
        assert result1 == {'FINISHED'}
        assert result2 == {'FINISHED'}
        assert len(mesh_obj.modifiers) == 2


class TestPerformanceWithChaining:
    """Test performance with multiple workflows chained."""
    
    def test_five_workflows_chained(self):
        """Test chaining 5 workflows completes reasonably fast."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        obj.select_set(True)
        
        workflows = ["array", "solidify", "hard-surface"]
        
        start_time = time.time()
        
        for workflow in workflows:
            bpy.context.scene.copilot_modifier_command = workflow
            bpy.ops.copilot.modifier_assistant()
        
        elapsed = time.time() - start_time
        
        # Should complete in reasonable time
        assert elapsed < 1.0, f"Chaining 3 workflows took {elapsed:.2f}s"
        assert len(obj.modifiers) == 4


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
