"""
Unit tests for context validator module.

These tests verify that selection context validation works correctly
using mocked Blender context (no actual Blender instance required).

NOTE: These tests will FAIL until copilot/utils/context_validator.py is implemented.
"""

import pytest
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import mock helpers
from tests.helpers.blender_mocks import MockBlenderContext, create_mock_scene, MockObject

# This import will fail until implementation exists - that's expected for TDD!
try:
    from copilot.utils.context_validator import (
        validate_object_selected,
        validate_object_count,
        validate_object_types,
        validate_active_object,
        validate_object_mode,
        validate_for_workflow
    )
except ImportError:
    # Create placeholders that will make all tests fail
    def validate_object_selected(context):
        raise NotImplementedError("context_validator module not yet implemented")
    
    def validate_object_count(context, expected):
        raise NotImplementedError("context_validator module not yet implemented")
    
    def validate_object_types(context, required_types):
        raise NotImplementedError("context_validator module not yet implemented")
    
    def validate_active_object(context):
        raise NotImplementedError("context_validator module not yet implemented")
    
    def validate_object_mode(context, required_mode):
        raise NotImplementedError("context_validator module not yet implemented")
    
    def validate_for_workflow(context, workflow_type):
        raise NotImplementedError("context_validator module not yet implemented")


class TestBasicValidation:
    """Test basic validation helper functions."""
    
    def test_validate_object_selected_with_selection(self):
        """Test validation passes when objects are selected."""
        ctx = create_mock_scene(num_meshes=1)
        is_valid, error_msg = validate_object_selected(ctx)
        assert is_valid is True
        assert error_msg == ""
    
    def test_validate_object_selected_without_selection(self):
        """Test validation fails when no objects selected."""
        ctx = create_mock_scene(num_meshes=0)
        is_valid, error_msg = validate_object_selected(ctx)
        assert is_valid is False
        assert error_msg == "Please select an object first"
    
    def test_validate_object_count_correct(self):
        """Test validation passes with correct object count."""
        ctx = create_mock_scene(num_meshes=2)
        is_valid, error_msg = validate_object_count(ctx, 2)
        assert is_valid is True
        assert error_msg == ""
    
    def test_validate_object_count_too_few(self):
        """Test validation fails with too few objects."""
        ctx = create_mock_scene(num_meshes=1)
        is_valid, error_msg = validate_object_count(ctx, 2)
        assert is_valid is False
        assert "requires 2 selected object(s), but 1 are selected" in error_msg
    
    def test_validate_object_count_too_many(self):
        """Test validation fails with too many objects."""
        ctx = create_mock_scene(num_meshes=3)
        is_valid, error_msg = validate_object_count(ctx, 2)
        assert is_valid is False
        assert "requires 2 selected object(s), but 3 are selected" in error_msg


class TestObjectTypeValidation:
    """Test validation of object types in selection."""
    
    def test_validate_single_mesh(self):
        """Test validation for single mesh requirement."""
        ctx = create_mock_scene(num_meshes=1)
        is_valid, error_msg = validate_object_types(ctx, {'MESH': 1})
        assert is_valid is True
        assert error_msg == ""
    
    def test_validate_mesh_and_empty(self):
        """Test validation for mesh + empty requirement."""
        ctx = create_mock_scene(num_meshes=1, num_empties=1)
        is_valid, error_msg = validate_object_types(ctx, {'MESH': 1, 'EMPTY': 1})
        assert is_valid is True
        assert error_msg == ""
    
    def test_validate_mesh_and_curve(self):
        """Test validation for mesh + curve requirement."""
        ctx = create_mock_scene(num_meshes=1, num_curves=1)
        is_valid, error_msg = validate_object_types(ctx, {'MESH': 1, 'CURVE': 1})
        assert is_valid is True
        assert error_msg == ""
    
    def test_validate_two_meshes(self):
        """Test validation for two mesh requirement."""
        ctx = create_mock_scene(num_meshes=2)
        is_valid, error_msg = validate_object_types(ctx, {'MESH': 2})
        assert is_valid is True
        assert error_msg == ""
    
    def test_validate_wrong_type_single(self):
        """Test validation fails with wrong object type."""
        ctx = create_mock_scene(num_empties=1)  # Empty instead of mesh
        is_valid, error_msg = validate_object_types(ctx, {'MESH': 1})
        assert is_valid is False
        assert "mesh" in error_msg.lower()
    
    def test_validate_wrong_type_combination(self):
        """Test validation fails with wrong type combination."""
        ctx = create_mock_scene(num_meshes=2)  # Two meshes instead of mesh + empty
        is_valid, error_msg = validate_object_types(ctx, {'MESH': 1, 'EMPTY': 1})
        assert is_valid is False
        assert error_msg != ""


class TestActiveObjectValidation:
    """Test validation of active object."""
    
    def test_validate_active_object_exists(self):
        """Test validation passes when active object exists."""
        ctx = create_mock_scene(num_meshes=1, with_active=True)
        is_valid, error_msg = validate_active_object(ctx)
        assert is_valid is True
        assert error_msg == ""
    
    def test_validate_active_object_missing(self):
        """Test validation fails when no active object."""
        ctx = create_mock_scene(num_meshes=1, with_active=False)
        is_valid, error_msg = validate_active_object(ctx)
        assert is_valid is False
        assert error_msg != ""


class TestModeValidation:
    """Test validation of Blender mode."""
    
    def test_validate_object_mode_correct(self):
        """Test validation passes in correct mode."""
        ctx = create_mock_scene(num_meshes=1)
        ctx.mode = 'OBJECT'
        is_valid, error_msg = validate_object_mode(ctx, 'OBJECT')
        assert is_valid is True
        assert error_msg == ""
    
    def test_validate_object_mode_wrong(self):
        """Test validation fails in wrong mode."""
        ctx = create_mock_scene(num_meshes=1)
        ctx.mode = 'EDIT'
        is_valid, error_msg = validate_object_mode(ctx, 'OBJECT')
        assert is_valid is False
        assert "Object Mode" in error_msg
        assert "EDIT" in error_msg


class TestWorkflowSpecificValidation:
    """Test validation for each specific workflow type."""
    
    def test_validate_smart_array_single(self):
        """Test validation for Smart Array single object variant."""
        ctx = create_mock_scene(num_meshes=1)
        is_valid, error_msg = validate_for_workflow(ctx, 'SMART_ARRAY')
        assert is_valid is True
        assert error_msg == ""
    
    def test_validate_smart_array_controlled(self):
        """Test validation for Smart Array controlled variant."""
        ctx = create_mock_scene(num_meshes=1, num_empties=1)
        is_valid, error_msg = validate_for_workflow(ctx, 'SMART_ARRAY')
        assert is_valid is True
        assert error_msg == ""
    
    def test_validate_hard_surface(self):
        """Test validation for Hard-Surface workflow."""
        ctx = create_mock_scene(num_meshes=1)
        is_valid, error_msg = validate_for_workflow(ctx, 'HARD_SURFACE')
        assert is_valid is True
        assert error_msg == ""
    
    def test_validate_symmetrize(self):
        """Test validation for Symmetrize workflow."""
        ctx = create_mock_scene(num_meshes=1)
        is_valid, error_msg = validate_for_workflow(ctx, 'SYMMETRIZE')
        assert is_valid is True
        assert error_msg == ""
    
    def test_validate_curve_deform(self):
        """Test validation for Curve Deform workflow."""
        ctx = create_mock_scene(num_meshes=1, num_curves=1)
        is_valid, error_msg = validate_for_workflow(ctx, 'CURVE_DEFORM')
        assert is_valid is True
        assert error_msg == ""
    
    def test_validate_solidify(self):
        """Test validation for Solidify workflow."""
        ctx = create_mock_scene(num_meshes=1)
        is_valid, error_msg = validate_for_workflow(ctx, 'SOLIDIFY')
        assert is_valid is True
        assert error_msg == ""
    
    def test_validate_shrinkwrap(self):
        """Test validation for Shrinkwrap workflow."""
        ctx = create_mock_scene(num_meshes=2)
        is_valid, error_msg = validate_for_workflow(ctx, 'SHRINKWRAP')
        assert is_valid is True
        assert error_msg == ""


class TestWorkflowValidationFailures:
    """Test validation failures for each workflow."""
    
    def test_smart_array_no_selection(self):
        """Test Smart Array fails with no selection."""
        ctx = create_mock_scene(num_meshes=0)
        is_valid, error_msg = validate_for_workflow(ctx, 'SMART_ARRAY')
        assert is_valid is False
        assert "select an object" in error_msg.lower()
    
    def test_hard_surface_wrong_count(self):
        """Test Hard-Surface fails with wrong object count."""
        ctx = create_mock_scene(num_meshes=2)
        is_valid, error_msg = validate_for_workflow(ctx, 'HARD_SURFACE')
        assert is_valid is False
        assert error_msg != ""
    
    def test_curve_deform_missing_curve(self):
        """Test Curve Deform fails without curve object."""
        ctx = create_mock_scene(num_meshes=2)  # Two meshes, no curve
        is_valid, error_msg = validate_for_workflow(ctx, 'CURVE_DEFORM')
        assert is_valid is False
        assert "curve" in error_msg.lower()
    
    def test_shrinkwrap_only_one_object(self):
        """Test Shrinkwrap fails with only one object."""
        ctx = create_mock_scene(num_meshes=1)
        is_valid, error_msg = validate_for_workflow(ctx, 'SHRINKWRAP')
        assert is_valid is False
        assert error_msg != ""
    
    def test_wrong_mode_fails(self):
        """Test workflows fail in wrong mode."""
        ctx = create_mock_scene(num_meshes=1)
        ctx.mode = 'EDIT'
        is_valid, error_msg = validate_for_workflow(ctx, 'SOLIDIFY')
        assert is_valid is False
        assert "Object Mode" in error_msg


class TestErrorMessageFormat:
    """Test that error messages match contract specifications exactly."""
    
    def test_no_selection_message(self):
        """Test no selection error message format."""
        ctx = create_mock_scene(num_meshes=0)
        is_valid, error_msg = validate_object_selected(ctx)
        assert error_msg == "Please select an object first"
    
    def test_wrong_count_message_format(self):
        """Test wrong count error message includes numbers."""
        ctx = create_mock_scene(num_meshes=1)
        is_valid, error_msg = validate_object_count(ctx, 2)
        assert "requires 2" in error_msg
        assert "but 1 are selected" in error_msg
    
    def test_wrong_mode_message_format(self):
        """Test wrong mode error message includes current mode."""
        ctx = create_mock_scene(num_meshes=1)
        ctx.mode = 'EDIT'
        is_valid, error_msg = validate_object_mode(ctx, 'OBJECT')
        assert "Object Mode" in error_msg
        assert "(currently in EDIT)" in error_msg or "EDIT" in error_msg


class TestValidationPerformance:
    """Test that validation is fast enough (<20ms per contract)."""
    
    def test_validation_performance(self):
        """Test that 1000 validation operations complete quickly."""
        import time
        
        ctx = create_mock_scene(num_meshes=1)
        
        start_time = time.time()
        for _ in range(1000):
            validate_object_selected(ctx)
            validate_object_count(ctx, 1)
            validate_object_mode(ctx, 'OBJECT')
        elapsed = time.time() - start_time
        
        # 1000 iterations × 3 checks = 3000 validation calls
        # Should complete in well under 1 second (target: <20ms each)
        assert elapsed < 0.5, f"Validation too slow: {elapsed:.3f}s for 3000 calls"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
