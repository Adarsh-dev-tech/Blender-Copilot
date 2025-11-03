"""
Integration tests for Hard-Surface SubD workflow.

These tests require an actual Blender instance and test the complete
workflow including modifier ordering and shading.

Run with: blender --background --python -m pytest tests/integration/test_hard_surface_workflow.py

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


class TestHardSurfaceWorkflow:
    """Test Hard-Surface SubD setup workflow."""
    
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
    
    def test_bevel_modifier_added(self):
        """Test Bevel modifier is added."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        bpy.context.scene.copilot_modifier_command = "make hard-surface"
        bpy.ops.copilot.modifier_assistant()
        
        # Find bevel modifier
        bevel_mods = [m for m in obj.modifiers if m.type == 'BEVEL']
        assert len(bevel_mods) == 1
    
    def test_subdivision_modifier_added(self):
        """Test Subdivision Surface modifier is added."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        bpy.context.scene.copilot_modifier_command = "hard-surface setup"
        bpy.ops.copilot.modifier_assistant()
        
        # Find subdivision modifier
        subsurf_mods = [m for m in obj.modifiers if m.type == 'SUBSURF']
        assert len(subsurf_mods) == 1
    
    def test_modifier_order_bevel_then_subsurf(self):
        """Test Bevel modifier comes before Subdivision (critical for hard-surface look)."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        bpy.context.scene.copilot_modifier_command = "apply hard-surface"
        bpy.ops.copilot.modifier_assistant()
        
        modifier_types = [m.type for m in obj.modifiers]
        assert len(modifier_types) == 2
        assert modifier_types[0] == 'BEVEL'
        assert modifier_types[1] == 'SUBSURF'
    
    def test_bevel_settings_angle_limit(self):
        """Test Bevel modifier uses angle limit method."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        bpy.context.scene.copilot_modifier_command = "hard-surface"
        bpy.ops.copilot.modifier_assistant()
        
        bevel_mod = [m for m in obj.modifiers if m.type == 'BEVEL'][0]
        assert bevel_mod.limit_method == 'ANGLE'
    
    def test_bevel_settings_segments(self):
        """Test Bevel modifier has 3 segments."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        bpy.context.scene.copilot_modifier_command = "hard surface"
        bpy.ops.copilot.modifier_assistant()
        
        bevel_mod = [m for m in obj.modifiers if m.type == 'BEVEL'][0]
        assert bevel_mod.segments == 3
    
    def test_subdivision_settings_levels(self):
        """Test Subdivision modifier has levels=2."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        bpy.context.scene.copilot_modifier_command = "hard-surface"
        bpy.ops.copilot.modifier_assistant()
        
        subsurf_mod = [m for m in obj.modifiers if m.type == 'SUBSURF'][0]
        assert subsurf_mod.levels == 2
    
    def test_smooth_shading_applied(self):
        """Test object shading is set to smooth."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        # Start with flat shading
        bpy.ops.object.shade_flat()
        
        bpy.context.scene.copilot_modifier_command = "hard-surface"
        bpy.ops.copilot.modifier_assistant()
        
        # Check if smooth shading is applied
        # Note: In Blender, shading is per-polygon, not per-object
        # Check first face smooth attribute
        mesh = obj.data
        if len(mesh.polygons) > 0:
            assert mesh.polygons[0].use_smooth is True
    
    def test_undo_removes_both_modifiers_and_shading(self):
        """Test undo removes both modifiers and restores flat shading in one step."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        bpy.ops.object.shade_flat()
        initial_smooth = obj.data.polygons[0].use_smooth if len(obj.data.polygons) > 0 else False
        
        bpy.context.scene.copilot_modifier_command = "hard-surface"
        bpy.ops.copilot.modifier_assistant()
        
        assert len(obj.modifiers) == 2
        
        # Undo
        bpy.ops.ed.undo()
        
        # Both modifiers should be removed
        assert len(obj.modifiers) == 0
        # Shading should be restored
        if len(obj.data.polygons) > 0:
            assert obj.data.polygons[0].use_smooth == initial_smooth
    
    def test_multiple_executions_dont_stack(self):
        """Test running workflow multiple times doesn't keep adding modifiers."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        bpy.context.scene.copilot_modifier_command = "hard-surface"
        
        # Execute twice
        bpy.ops.copilot.modifier_assistant()
        bpy.ops.copilot.modifier_assistant()
        
        # Should have 4 modifiers total (2 per execution)
        # This tests that workflow doesn't check for existing modifiers
        assert len(obj.modifiers) == 4


class TestHardSurfaceErrorCases:
    """Test error handling for Hard-Surface workflow."""
    
    def test_no_selection_error(self):
        """Test error when no object selected."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        bpy.ops.object.select_all(action='DESELECT')
        
        bpy.context.scene.copilot_modifier_command = "hard-surface"
        result = bpy.ops.copilot.modifier_assistant()
        
        assert result == {'CANCELLED'}
    
    def test_multiple_objects_error(self):
        """Test error when multiple objects selected."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        bpy.ops.mesh.primitive_cube_add(location=(2, 0, 0))
        bpy.ops.object.select_all(action='SELECT')
        
        bpy.context.scene.copilot_modifier_command = "hard-surface"
        result = bpy.ops.copilot.modifier_assistant()
        
        assert result == {'CANCELLED'}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
