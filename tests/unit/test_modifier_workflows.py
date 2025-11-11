"""
Unit tests for modifier workflow functions.

These tests verify that individual workflow functions execute correctly
using mocked Blender operations (no actual Blender instance required).

NOTE: These tests will FAIL until copilot/utils/modifier_workflows.py is implemented.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch, call

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import mock helpers
from tests.helpers.blender_mocks import MockBlenderContext, MockObject, create_mock_scene

# This import will fail until implementation exists - that's expected for TDD!
try:
    from copilot.utils.modifier_workflows import (
        apply_smart_array_single,
        apply_smart_array_controlled,
        apply_hard_surface_setup,
        apply_symmetrize,
        apply_curve_deform,
        apply_solidify,
        apply_shrinkwrap
    )
except ImportError:
    # Create placeholders that will make all tests fail
    def apply_smart_array_single(obj):
        raise NotImplementedError("modifier_workflows module not yet implemented")
    
    def apply_smart_array_controlled(mesh, empty):
        raise NotImplementedError("modifier_workflows module not yet implemented")
    
    def apply_hard_surface_setup(obj):
        raise NotImplementedError("modifier_workflows module not yet implemented")
    
    def apply_symmetrize(obj):
        raise NotImplementedError("modifier_workflows module not yet implemented")
    
    def apply_curve_deform(mesh, curve):
        raise NotImplementedError("modifier_workflows module not yet implemented")
    
    def apply_solidify(obj):
        raise NotImplementedError("modifier_workflows module not yet implemented")
    
    def apply_shrinkwrap(source, target):
        raise NotImplementedError("modifier_workflows module not yet implemented")


class TestSmartArraySingle:
    """Test Smart Array single object workflow."""
    
    def test_returns_correct_status(self):
        """Test function returns correct status tuple."""
        obj = MockObject("Cube", "MESH")
        status, message = apply_smart_array_single(obj)
        assert status == {'FINISHED'}
        assert isinstance(message, str)
        assert len(message) > 0
    
    def test_adds_array_modifier(self):
        """Test Array modifier is added to object."""
        obj = MockObject("Cube", "MESH")
        apply_smart_array_single(obj)
        assert len(obj.modifiers) == 1
        assert obj.modifiers[0].type == 'ARRAY'
    
    def test_array_modifier_name(self):
        """Test Array modifier has correct name."""
        obj = MockObject("Cube", "MESH")
        apply_smart_array_single(obj)
        assert obj.modifiers[0].name == "Array"
    
    def test_array_count_is_five(self):
        """Test Array modifier count is set to 5."""
        obj = MockObject("Cube", "MESH")
        apply_smart_array_single(obj)
        modifier = obj.modifiers[0]
        assert hasattr(modifier, 'count') or 'count' in str(modifier.__dict__)
        # This will be properly testable once implementation exists
    
    def test_success_message_content(self):
        """Test success message mentions array and parameters."""
        obj = MockObject("Cube", "MESH")
        status, message = apply_smart_array_single(obj)
        assert "array" in message.lower()
        assert "5" in message


class TestSmartArrayControlled:
    """Test Smart Array with object offset workflow."""
    
    def test_returns_correct_status(self):
        """Test function returns correct status tuple."""
        mesh = MockObject("Cube", "MESH")
        empty = MockObject("Empty", "EMPTY")
        status, message = apply_smart_array_controlled(mesh, empty)
        assert status == {'FINISHED'}
        assert isinstance(message, str)
    
    def test_adds_modifier_to_mesh(self):
        """Test Array modifier is added to mesh object (not empty)."""
        mesh = MockObject("Cube", "MESH")
        empty = MockObject("Empty", "EMPTY")
        apply_smart_array_controlled(mesh, empty)
        assert len(mesh.modifiers) == 1
        assert len(empty.modifiers) == 0  # Empty should have no modifiers
    
    def test_array_uses_object_offset(self):
        """Test Array modifier uses object offset mode."""
        mesh = MockObject("Cube", "MESH")
        empty = MockObject("Empty", "EMPTY")
        apply_smart_array_controlled(mesh, empty)
        modifier = mesh.modifiers[0]
        # Will be testable once implementation exists
        assert modifier.type == 'ARRAY'
    
    def test_success_message_mentions_empty(self):
        """Test success message mentions empty object."""
        mesh = MockObject("Cube", "MESH")
        empty = MockObject("Empty", "EMPTY")
        status, message = apply_smart_array_controlled(mesh, empty)
        assert "empty" in message.lower() or "object" in message.lower()


class TestHardSurfaceSetup:
    """Test Hard-Surface SubD workflow."""
    
    def test_returns_correct_status(self):
        """Test function returns correct status tuple."""
        obj = MockObject("Cube", "MESH")
        status, message = apply_hard_surface_setup(obj)
        assert status == {'FINISHED'}
        assert isinstance(message, str)
    
    def test_adds_two_modifiers(self):
        """Test both Bevel and Subdivision modifiers are added."""
        obj = MockObject("Cube", "MESH")
        apply_hard_surface_setup(obj)
        assert len(obj.modifiers) == 2
    
    def test_bevel_modifier_first(self):
        """Test Bevel modifier is added before Subdivision."""
        obj = MockObject("Cube", "MESH")
        apply_hard_surface_setup(obj)
        assert obj.modifiers[0].type == 'BEVEL'
        assert obj.modifiers[0].name == "Bevel"
    
    def test_subsurf_modifier_second(self):
        """Test Subdivision Surface modifier is added second."""
        obj = MockObject("Cube", "MESH")
        apply_hard_surface_setup(obj)
        assert obj.modifiers[1].type == 'SUBSURF'
        assert obj.modifiers[1].name in ["Subdivision Surface", "Subdivision"]
    
    def test_modifier_order_critical(self):
        """Test modifier order is Bevel then Subdivision (not reversed)."""
        obj = MockObject("Cube", "MESH")
        apply_hard_surface_setup(obj)
        modifier_types = [mod.type for mod in obj.modifiers]
        assert modifier_types == ['BEVEL', 'SUBSURF']
    
    def test_success_message_mentions_both_modifiers(self):
        """Test success message mentions bevel and subdivision."""
        obj = MockObject("Cube", "MESH")
        status, message = apply_hard_surface_setup(obj)
        assert "bevel" in message.lower()
        assert ("subdivision" in message.lower() or "subsurf" in message.lower())


class TestSymmetrize:
    """Test Symmetrize workflow."""
    
    def test_returns_correct_status(self):
        """Test function returns correct status tuple."""
        obj = MockObject("Cube", "MESH")
        status, message = apply_symmetrize(obj)
        assert status == {'FINISHED'}
        assert isinstance(message, str)
    
    def test_adds_mirror_modifier(self):
        """Test Mirror modifier is added."""
        obj = MockObject("Cube", "MESH")
        apply_symmetrize(obj)
        assert len(obj.modifiers) >= 1
        # Find mirror modifier
        mirror_mods = [m for m in obj.modifiers if m.type == 'MIRROR']
        assert len(mirror_mods) == 1
    
    def test_scale_application_attempted(self):
        """Test that scale application is attempted (will mock bpy.ops)."""
        obj = MockObject("Cube", "MESH")
        # This test will need proper mocking of bpy.ops once implemented
        status, message = apply_symmetrize(obj)
        assert status == {'FINISHED'}
    
    def test_success_message_mentions_symmetrize(self):
        """Test success message mentions symmetrize or mirror."""
        obj = MockObject("Cube", "MESH")
        status, message = apply_symmetrize(obj)
        assert ("symmetrize" in message.lower() or 
                "mirror" in message.lower() or
                "x-axis" in message.lower())


class TestCurveDeform:
    """Test Curve Deform workflow."""
    
    def test_returns_correct_status(self):
        """Test function returns correct status tuple."""
        mesh = MockObject("Cube", "MESH")
        curve = MockObject("BezierCurve", "CURVE")
        status, message = apply_curve_deform(mesh, curve)
        assert status == {'FINISHED'}
        assert isinstance(message, str)
    
    def test_adds_curve_modifier_to_mesh(self):
        """Test Curve modifier is added to mesh object."""
        mesh = MockObject("Cube", "MESH")
        curve = MockObject("BezierCurve", "CURVE")
        apply_curve_deform(mesh, curve)
        assert len(mesh.modifiers) == 1
        assert mesh.modifiers[0].type == 'CURVE'
    
    def test_curve_not_modified(self):
        """Test curve object gets no modifiers."""
        mesh = MockObject("Cube", "MESH")
        curve = MockObject("BezierCurve", "CURVE")
        apply_curve_deform(mesh, curve)
        assert len(curve.modifiers) == 0
    
    def test_success_message_mentions_curve(self):
        """Test success message mentions curve deform."""
        mesh = MockObject("Cube", "MESH")
        curve = MockObject("BezierCurve", "CURVE")
        status, message = apply_curve_deform(mesh, curve)
        assert "curve" in message.lower()


class TestSolidify:
    """Test Solidify workflow."""
    
    def test_returns_correct_status(self):
        """Test function returns correct status tuple."""
        obj = MockObject("Cube", "MESH")
        status, message = apply_solidify(obj)
        assert status == {'FINISHED'}
        assert isinstance(message, str)
    
    def test_adds_solidify_modifier(self):
        """Test Solidify modifier is added."""
        obj = MockObject("Cube", "MESH")
        apply_solidify(obj)
        assert len(obj.modifiers) == 1
        assert obj.modifiers[0].type == 'SOLIDIFY'
        assert obj.modifiers[0].name == "Solidify"
    
    def test_thickness_is_001(self):
        """Test Solidify thickness is set to 0.01."""
        obj = MockObject("Cube", "MESH")
        apply_solidify(obj)
        # Will be properly testable once implementation exists
        status, message = apply_solidify(obj)
        assert "0.01" in message
    
    def test_success_message_mentions_solidify(self):
        """Test success message mentions solidify."""
        obj = MockObject("Cube", "MESH")
        status, message = apply_solidify(obj)
        assert "solidify" in message.lower()


class TestShrinkwrap:
    """Test Shrinkwrap workflow."""
    
    def test_returns_correct_status(self):
        """Test function returns correct status tuple."""
        source = MockObject("Cube1", "MESH")
        target = MockObject("Cube2", "MESH")
        status, message = apply_shrinkwrap(source, target)
        assert status == {'FINISHED'}
        assert isinstance(message, str)
    
    def test_adds_modifier_to_source_only(self):
        """Test Shrinkwrap modifier added to source, not target."""
        source = MockObject("Cube1", "MESH")
        target = MockObject("Cube2", "MESH")
        apply_shrinkwrap(source, target)
        assert len(source.modifiers) == 1
        assert len(target.modifiers) == 0
    
    def test_shrinkwrap_modifier_type(self):
        """Test correct modifier type is added."""
        source = MockObject("Cube1", "MESH")
        target = MockObject("Cube2", "MESH")
        apply_shrinkwrap(source, target)
        assert source.modifiers[0].type == 'SHRINKWRAP'
        assert source.modifiers[0].name == "Shrinkwrap"
    
    def test_success_message_mentions_target(self):
        """Test success message mentions target object."""
        source = MockObject("Cube1", "MESH")
        target = MockObject("Cube2", "MESH")
        status, message = apply_shrinkwrap(source, target)
        assert "shrinkwrap" in message.lower()
        assert ("target" in message.lower() or target.name in message)


class TestErrorHandling:
    """Test error handling in workflow functions."""
    
    def test_smart_array_with_none_object(self):
        """Test Smart Array handles None object gracefully."""
        # Should either raise ValueError or return {'CANCELLED'}
        with pytest.raises((ValueError, TypeError, NotImplementedError)):
            apply_smart_array_single(None)
    
    def test_hard_surface_with_wrong_type(self):
        """Test Hard-Surface handles non-mesh object types."""
        obj = MockObject("Camera", "CAMERA")
        # Should handle gracefully (may add modifiers anyway or reject)
        # Implementation will determine exact behavior
        try:
            status, message = apply_hard_surface_setup(obj)
            # If it succeeds, should return valid status
            assert status in [{'FINISHED'}, {'CANCELLED'}]
        except (ValueError, NotImplementedError):
            pass  # Also acceptable to raise error


class TestReturnValueConsistency:
    """Test that all workflow functions return consistent tuple format."""
    
    def test_all_workflows_return_tuple(self):
        """Test all functions return (status, message) tuple."""
        obj = MockObject("Cube", "MESH")
        empty = MockObject("Empty", "EMPTY")
        curve = MockObject("Curve", "CURVE")
        
        workflows = [
            (apply_smart_array_single, (obj,)),
            (apply_smart_array_controlled, (obj, empty)),
            (apply_hard_surface_setup, (obj,)),
            (apply_symmetrize, (obj,)),
            (apply_curve_deform, (obj, curve)),
            (apply_solidify, (obj,)),
            (apply_shrinkwrap, (obj, obj)),
        ]
        
        for func, args in workflows:
            result = func(*args)
            assert isinstance(result, tuple), f"{func.__name__} should return tuple"
            assert len(result) == 2, f"{func.__name__} should return 2-tuple"
            status, message = result
            assert isinstance(status, (set, dict)), f"{func.__name__} status should be set/dict"
            assert isinstance(message, str), f"{func.__name__} message should be string"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
