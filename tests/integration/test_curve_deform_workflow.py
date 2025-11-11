"""
Integration tests for Curve Deform workflow.

Tests workflow with mesh + curve selection, scale application,
and origin alignment.

Run with: blender --background --python -m pytest tests/integration/test_curve_deform_workflow.py

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


class TestCurveDeformWorkflow:
    """Test Curve Deform workflow."""
    
    @pytest.fixture(autouse=True)
    def setup_scene(self):
        """Load cube_and_curve.blend fixture before each test."""
        fixture_path = project_root / "tests" / "fixtures" / "cube_and_curve.blend"
        if fixture_path.exists():
            bpy.ops.wm.open_mainfile(filepath=str(fixture_path))
        else:
            bpy.ops.wm.read_homefile(use_empty=True)
            bpy.ops.mesh.primitive_cube_add()
            bpy.ops.curve.primitive_bezier_curve_add(location=(2, 0, 0))
        yield
    
    def test_curve_modifier_added_to_mesh(self):
        """Test Curve modifier is added to mesh object."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        bpy.ops.object.select_all(action='SELECT')
        
        # Find mesh object
        mesh_obj = [o for o in bpy.context.selected_objects if o.type == 'MESH'][0]
        
        bpy.context.scene.copilot_modifier_command = "curve deform"
        bpy.ops.copilot.modifier_assistant()
        
        curve_mods = [m for m in mesh_obj.modifiers if m.type == 'CURVE']
        assert len(curve_mods) == 1
    
    def test_curve_object_is_target(self):
        """Test curve object is set as modifier target."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        bpy.ops.object.select_all(action='SELECT')
        
        mesh_obj = [o for o in bpy.context.selected_objects if o.type == 'MESH'][0]
        curve_obj = [o for o in bpy.context.selected_objects if o.type == 'CURVE'][0]
        
        bpy.context.scene.copilot_modifier_command = "bend along curve"
        bpy.ops.copilot.modifier_assistant()
        
        curve_mod = [m for m in mesh_obj.modifiers if m.type == 'CURVE'][0]
        assert curve_mod.object == curve_obj
    
    def test_scale_applied_to_mesh(self):
        """Test scale is applied to mesh object."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        bpy.ops.object.select_all(action='SELECT')
        
        mesh_obj = [o for o in bpy.context.selected_objects if o.type == 'MESH'][0]
        mesh_obj.scale = (2.0, 1.5, 1.0)
        
        bpy.context.scene.copilot_modifier_command = "curve deform"
        bpy.ops.copilot.modifier_assistant()
        
        assert mesh_obj.scale[0] == pytest.approx(1.0, abs=0.001)
        assert mesh_obj.scale[1] == pytest.approx(1.0, abs=0.001)
        assert mesh_obj.scale[2] == pytest.approx(1.0, abs=0.001)
    
    def test_scale_applied_to_curve(self):
        """Test scale is applied to curve object."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        bpy.ops.object.select_all(action='SELECT')
        
        curve_obj = [o for o in bpy.context.selected_objects if o.type == 'CURVE'][0]
        curve_obj.scale = (1.5, 2.0, 1.0)
        
        bpy.context.scene.copilot_modifier_command = "deform to curve"
        bpy.ops.copilot.modifier_assistant()
        
        assert curve_obj.scale[0] == pytest.approx(1.0, abs=0.001)
        assert curve_obj.scale[1] == pytest.approx(1.0, abs=0.001)
        assert curve_obj.scale[2] == pytest.approx(1.0, abs=0.001)
    
    def test_mesh_origin_aligned_to_curve(self):
        """Test mesh origin is moved to curve origin."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        bpy.ops.object.select_all(action='SELECT')
        
        mesh_obj = [o for o in bpy.context.selected_objects if o.type == 'MESH'][0]
        curve_obj = [o for o in bpy.context.selected_objects if o.type == 'CURVE'][0]
        
        # Set different locations
        curve_obj.location = (3.0, 2.0, 1.0)
        
        bpy.context.scene.copilot_modifier_command = "curve deform"
        bpy.ops.copilot.modifier_assistant()
        
        # Mesh should be at curve's location
        assert mesh_obj.location.x == pytest.approx(curve_obj.location.x, abs=0.001)
        assert mesh_obj.location.y == pytest.approx(curve_obj.location.y, abs=0.001)
        assert mesh_obj.location.z == pytest.approx(curve_obj.location.z, abs=0.001)
    
    def test_curve_object_unchanged(self):
        """Test curve object has no modifiers added."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        bpy.ops.object.select_all(action='SELECT')
        
        curve_obj = [o for o in bpy.context.selected_objects if o.type == 'CURVE'][0]
        
        bpy.context.scene.copilot_modifier_command = "curve deform"
        bpy.ops.copilot.modifier_assistant()
        
        assert len(curve_obj.modifiers) == 0
    
    def test_undo_restores_origins_and_scales(self):
        """Test undo restores original origins, scales, and removes modifier."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        bpy.ops.object.select_all(action='SELECT')
        
        mesh_obj = [o for o in bpy.context.selected_objects if o.type == 'MESH'][0]
        curve_obj = [o for o in bpy.context.selected_objects if o.type == 'CURVE'][0]
        
        initial_mesh_scale = tuple(mesh_obj.scale)
        initial_mesh_loc = tuple(mesh_obj.location)
        
        bpy.context.scene.copilot_modifier_command = "curve deform"
        bpy.ops.copilot.modifier_assistant()
        
        # Undo
        bpy.ops.ed.undo()
        
        # Check restoration
        assert mesh_obj.scale[0] == pytest.approx(initial_mesh_scale[0], abs=0.001)
        assert mesh_obj.location.x == pytest.approx(initial_mesh_loc[0], abs=0.001)
        assert len([m for m in mesh_obj.modifiers if m.type == 'CURVE']) == 0


class TestCurveDeformErrorCases:
    """Test error handling for Curve Deform workflow."""
    
    def test_wrong_object_types_error(self):
        """Test error when selected objects aren't mesh + curve."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        bpy.ops.mesh.primitive_cube_add(location=(2, 0, 0))
        bpy.ops.object.select_all(action='SELECT')
        
        bpy.context.scene.copilot_modifier_command = "curve deform"
        result = bpy.ops.copilot.modifier_assistant()
        
        assert result == {'CANCELLED'}
    
    def test_only_one_object_error(self):
        """Test error when only one object selected."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        obj.select_set(True)
        
        bpy.context.scene.copilot_modifier_command = "curve deform"
        result = bpy.ops.copilot.modifier_assistant()
        
        assert result == {'CANCELLED'}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
