"""
Integration tests for Solidify workflow.

Simple workflow that adds thickness to mesh surfaces.

Run with: blender --background --python -m pytest tests/integration/test_solidify_workflow.py

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


class TestSolidifyWorkflow:
    """Test Solidify workflow."""
    
    @pytest.fixture(autouse=True)
    def setup_scene(self):
        """Load single_cube.blend fixture before each test."""
        fixture_path = project_root / "tests" / "fixtures" / "single_cube.blend"
        if fixture_path.exists():
            bpy.ops.wm.open_mainfile(filepath=str(fixture_path))
        else:
            bpy.ops.wm.read_homefile(use_empty=True)
            bpy.ops.mesh.primitive_cube_add()
        yield
    
    def test_solidify_modifier_added(self):
        """Test Solidify modifier is added."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        bpy.context.scene.copilot_modifier_command = "solidify"
        bpy.ops.copilot.modifier_assistant()
        
        solidify_mods = [m for m in obj.modifiers if m.type == 'SOLIDIFY']
        assert len(solidify_mods) == 1
    
    def test_solidify_thickness_001(self):
        """Test Solidify modifier has thickness=0.01."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        bpy.context.scene.copilot_modifier_command = "add thickness"
        bpy.ops.copilot.modifier_assistant()
        
        solidify_mod = [m for m in obj.modifiers if m.type == 'SOLIDIFY'][0]
        assert solidify_mod.thickness == pytest.approx(0.01, abs=0.0001)
    
    def test_solidify_even_offset_enabled(self):
        """Test Solidify modifier has even offset enabled."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        bpy.context.scene.copilot_modifier_command = "make solid"
        bpy.ops.copilot.modifier_assistant()
        
        solidify_mod = [m for m in obj.modifiers if m.type == 'SOLIDIFY'][0]
        assert solidify_mod.use_even_offset is True
    
    def test_works_with_plane(self):
        """Test workflow works with plane geometry."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_plane_add()
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        bpy.context.scene.copilot_modifier_command = "solidify"
        result = bpy.ops.copilot.modifier_assistant()
        
        assert result == {'FINISHED'}
        assert len([m for m in obj.modifiers if m.type == 'SOLIDIFY']) == 1
    
    def test_undo_removes_modifier(self):
        """Test undo removes Solidify modifier."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        bpy.context.scene.copilot_modifier_command = "solidify"
        bpy.ops.copilot.modifier_assistant()
        
        assert len([m for m in obj.modifiers if m.type == 'SOLIDIFY']) == 1
        
        # Undo
        bpy.ops.ed.undo()
        
        assert len([m for m in obj.modifiers if m.type == 'SOLIDIFY']) == 0


class TestSolidifyErrorCases:
    """Test error handling for Solidify workflow."""
    
    def test_no_selection_error(self):
        """Test error when no object selected."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        bpy.ops.object.select_all(action='DESELECT')
        
        bpy.context.scene.copilot_modifier_command = "solidify"
        result = bpy.ops.copilot.modifier_assistant()
        
        assert result == {'CANCELLED'}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
