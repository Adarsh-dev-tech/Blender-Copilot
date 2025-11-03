"""
Integration tests for Symmetrize workflow.

This is the most complex workflow involving scale application, Edit Mode,
BMesh operations, and vertex deletion.

Run with: blender --background --python -m pytest tests/integration/test_symmetrize_workflow.py

NOTE: These tests will FAIL until the workflow is fully implemented.
"""

import sys
from pathlib import Path

try:
    import bpy
    import bmesh
except ImportError:
    print("ERROR: This test requires Blender. Run with: blender --background --python -m pytest")
    sys.exit(1)

import pytest

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class TestSymmetrizeWorkflow:
    """Test Symmetrize (Mirror) workflow."""
    
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
    
    def test_mirror_modifier_added(self):
        """Test Mirror modifier is added."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        bpy.context.scene.copilot_modifier_command = "mirror on X"
        bpy.ops.copilot.modifier_assistant()
        
        mirror_mods = [m for m in obj.modifiers if m.type == 'MIRROR']
        assert len(mirror_mods) == 1
    
    def test_mirror_axis_x(self):
        """Test Mirror modifier is set to X-axis."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        bpy.context.scene.copilot_modifier_command = "symmetrize"
        bpy.ops.copilot.modifier_assistant()
        
        mirror_mod = [m for m in obj.modifiers if m.type == 'MIRROR'][0]
        assert mirror_mod.use_axis[0] is True  # X-axis
        assert mirror_mod.use_axis[1] is False  # Not Y
        assert mirror_mod.use_axis[2] is False  # Not Z
    
    def test_mirror_bisect_enabled(self):
        """Test Mirror modifier has bisect enabled."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        bpy.context.scene.copilot_modifier_command = "make symmetric"
        bpy.ops.copilot.modifier_assistant()
        
        mirror_mod = [m for m in obj.modifiers if m.type == 'MIRROR'][0]
        assert mirror_mod.use_bisect_axis[0] is True
    
    def test_mirror_clipping_enabled(self):
        """Test Mirror modifier has clipping enabled."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        bpy.context.scene.copilot_modifier_command = "symmetrize"
        bpy.ops.copilot.modifier_assistant()
        
        mirror_mod = [m for m in obj.modifiers if m.type == 'MIRROR'][0]
        assert mirror_mod.use_clip is True
    
    def test_scale_applied(self):
        """Test scale transformation is applied."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        # Set non-uniform scale
        obj.scale = (2.0, 1.5, 1.0)
        
        bpy.context.scene.copilot_modifier_command = "mirror"
        bpy.ops.copilot.modifier_assistant()
        
        # Scale should be applied (reset to 1,1,1)
        assert obj.scale[0] == pytest.approx(1.0, abs=0.001)
        assert obj.scale[1] == pytest.approx(1.0, abs=0.001)
        assert obj.scale[2] == pytest.approx(1.0, abs=0.001)
    
    def test_positive_x_vertices_deleted(self):
        """Test vertices on positive X side are deleted."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        # Count vertices before
        initial_vert_count = len(obj.data.vertices)
        
        bpy.context.scene.copilot_modifier_command = "symmetrize"
        bpy.ops.copilot.modifier_assistant()
        
        # Should have fewer vertices (half deleted)
        final_vert_count = len(obj.data.vertices)
        assert final_vert_count < initial_vert_count
    
    def test_only_negative_x_vertices_remain(self):
        """Test only vertices with x <= 0 remain after workflow."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        bpy.context.scene.copilot_modifier_command = "mirror on X"
        bpy.ops.copilot.modifier_assistant()
        
        # Check all remaining vertices
        for vert in obj.data.vertices:
            # Account for floating point precision
            assert vert.co.x <= 0.0001, f"Vertex at x={vert.co.x} should have been deleted"
    
    def test_returns_to_object_mode(self):
        """Test workflow returns to Object Mode after Edit Mode operations."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        # Start in Object Mode
        bpy.ops.object.mode_set(mode='OBJECT')
        
        bpy.context.scene.copilot_modifier_command = "symmetrize"
        bpy.ops.copilot.modifier_assistant()
        
        # Should still be in Object Mode
        assert bpy.context.mode == 'OBJECT'
    
    def test_undo_restores_vertices_and_modifier(self):
        """Test undo restores deleted vertices and removes modifier in one step."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        initial_vert_count = len(obj.data.vertices)
        initial_scale = tuple(obj.scale)
        
        bpy.context.scene.copilot_modifier_command = "mirror"
        bpy.ops.copilot.modifier_assistant()
        
        # Undo
        bpy.ops.ed.undo()
        
        # Vertices should be restored
        assert len(obj.data.vertices) == initial_vert_count
        # Modifier should be removed
        assert len([m for m in obj.modifiers if m.type == 'MIRROR']) == 0
        # Scale should be restored
        assert obj.scale[0] == pytest.approx(initial_scale[0], abs=0.001)
    
    def test_performance_under_200ms(self):
        """Test workflow completes in under 200ms (contract requirement)."""
        import time
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        bpy.context.scene.copilot_modifier_command = "symmetrize"
        
        start_time = time.time()
        bpy.ops.copilot.modifier_assistant()
        elapsed = time.time() - start_time
        
        assert elapsed < 0.2, f"Symmetrize workflow took {elapsed*1000:.1f}ms (should be <200ms)"


class TestSymmetrizeComplexGeometry:
    """Test Symmetrize with more complex geometry."""
    
    def test_works_with_subdivided_cube(self):
        """Test workflow handles subdivided geometry correctly."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        obj = bpy.context.object
        
        # Add subdivision modifier and apply it
        bpy.ops.object.modifier_add(type='SUBSURF')
        bpy.ops.object.modifier_apply(modifier="Subdivision")
        
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        initial_vert_count = len(obj.data.vertices)
        
        bpy.context.scene.copilot_modifier_command = "symmetrize"
        bpy.ops.copilot.modifier_assistant()
        
        # Should still delete approximately half the vertices
        final_vert_count = len(obj.data.vertices)
        assert final_vert_count < initial_vert_count * 0.6  # Roughly half


class TestSymmetrizeErrorCases:
    """Test error handling for Symmetrize workflow."""
    
    def test_no_selection_error(self):
        """Test error when no object selected."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        bpy.ops.object.select_all(action='DESELECT')
        
        bpy.context.scene.copilot_modifier_command = "symmetrize"
        result = bpy.ops.copilot.modifier_assistant()
        
        assert result == {'CANCELLED'}
    
    def test_multiple_objects_error(self):
        """Test error when multiple objects selected."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        bpy.ops.mesh.primitive_cube_add(location=(2, 0, 0))
        bpy.ops.object.select_all(action='SELECT')
        
        bpy.context.scene.copilot_modifier_command = "mirror"
        result = bpy.ops.copilot.modifier_assistant()
        
        assert result == {'CANCELLED'}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
