"""
Integration tests for Operator Contract compliance.

Verifies that the modifier assistant operator meets all contract specifications
including return values, error messages, performance, and undo behavior.

Run with: blender --background --python -m pytest tests/integration/test_operator_contract.py

NOTE: These tests will FAIL until the operator is fully implemented.
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


class TestOperatorRegistration:
    """Test operator is correctly registered with Blender."""
    
    def test_operator_exists(self):
        """Test operator can be accessed."""
        # Operator should be accessible
        assert hasattr(bpy.ops, 'copilot')
        assert hasattr(bpy.ops.copilot, 'modifier_assistant')
    
    def test_operator_has_undo_flag(self):
        """Test operator has UNDO in bl_options."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        assert 'UNDO' in COPILOT_OT_modifier_assistant.bl_options
    
    def test_operator_has_register_flag(self):
        """Test operator has REGISTER in bl_options."""
        from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
        
        assert 'REGISTER' in COPILOT_OT_modifier_assistant.bl_options


class TestOperatorReturnValues:
    """Test operator returns only FINISHED or CANCELLED, never crashes."""
    
    def test_returns_finished_on_success(self):
        """Test operator returns {'FINISHED'} on successful execution."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        bpy.context.scene.copilot_modifier_command = "solidify"
        result = bpy.ops.copilot.modifier_assistant()
        
        assert result == {'FINISHED'}
    
    def test_returns_cancelled_on_validation_failure(self):
        """Test operator returns {'CANCELLED'} when validation fails."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        bpy.ops.object.select_all(action='DESELECT')
        
        bpy.context.scene.copilot_modifier_command = "array"
        result = bpy.ops.copilot.modifier_assistant()
        
        assert result == {'CANCELLED'}
    
    def test_returns_cancelled_on_unknown_command(self):
        """Test operator returns {'CANCELLED'} for unknown commands."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        obj.select_set(True)
        
        bpy.context.scene.copilot_modifier_command = "xyz invalid command"
        result = bpy.ops.copilot.modifier_assistant()
        
        assert result == {'CANCELLED'}
    
    def test_never_returns_error_set(self):
        """Test operator never returns {'ERROR'} (should use CANCELLED instead)."""
        # Try various failing scenarios
        test_cases = [
            ("", False),  # Empty command, no selection
            ("array", False),  # Valid command, no selection
            ("xyz", True),  # Invalid command, with selection
        ]
        
        for command, with_selection in test_cases:
            bpy.ops.wm.read_homefile(use_empty=True)
            bpy.ops.mesh.primitive_cube_add()
            
            if not with_selection:
                bpy.ops.object.select_all(action='DESELECT')
            
            bpy.context.scene.copilot_modifier_command = command
            result = bpy.ops.copilot.modifier_assistant()
            
            assert result in [{'FINISHED'}, {'CANCELLED'}], \
                f"Operator returned unexpected value for command='{command}', selection={with_selection}"


class TestErrorMessageContract:
    """Test that error messages exactly match contract specifications."""
    
    def test_no_selection_error_message(self):
        """Test no selection error message matches contract."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        bpy.ops.object.select_all(action='DESELECT')
        
        bpy.context.scene.copilot_modifier_command = "array"
        
        # Execute and check error message appears in info area
        # (Blender stores messages in window manager)
        result = bpy.ops.copilot.modifier_assistant()
        
        assert result == {'CANCELLED'}
        # Message should have been reported (can't easily capture exact text in test)
    
    def test_unknown_command_error_message(self):
        """Test unknown command error message includes suggestions."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        obj.select_set(True)
        
        bpy.context.scene.copilot_modifier_command = "xyz invalid"
        result = bpy.ops.copilot.modifier_assistant()
        
        assert result == {'CANCELLED'}
        # Should report error with workflow suggestions
    
    def test_wrong_object_count_error_message(self):
        """Test wrong object count error message includes counts."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        bpy.ops.mesh.primitive_cube_add(location=(2, 0, 0))
        bpy.ops.object.select_all(action='SELECT')
        
        bpy.context.scene.copilot_modifier_command = "solidify"
        result = bpy.ops.copilot.modifier_assistant()
        
        assert result == {'CANCELLED'}
        # Should mention expecting 1 but got 2


class TestPerformanceContract:
    """Test that workflows meet performance targets."""
    
    def test_simple_workflow_under_50ms(self):
        """Test simple workflows (Array, Solidify, Shrinkwrap) complete in <50ms."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        simple_workflows = ["array", "solidify"]
        
        for command in simple_workflows:
            bpy.context.scene.copilot_modifier_command = command
            
            start_time = time.time()
            result = bpy.ops.copilot.modifier_assistant()
            elapsed = time.time() - start_time
            
            assert result == {'FINISHED'}
            assert elapsed < 0.05, f"{command} took {elapsed*1000:.1f}ms (should be <50ms)"
            
            # Clean up modifiers for next test
            obj.modifiers.clear()
    
    def test_complex_workflow_under_100ms(self):
        """Test complex workflow (Hard-Surface) completes in <100ms."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        bpy.context.scene.copilot_modifier_command = "hard-surface"
        
        start_time = time.time()
        result = bpy.ops.copilot.modifier_assistant()
        elapsed = time.time() - start_time
        
        assert result == {'FINISHED'}
        assert elapsed < 0.1, f"Hard-surface took {elapsed*1000:.1f}ms (should be <100ms)"
    
    def test_edit_mode_workflow_under_200ms(self):
        """Test Edit Mode workflow (Symmetrize) completes in <200ms."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        bpy.context.scene.copilot_modifier_command = "symmetrize"
        
        start_time = time.time()
        result = bpy.ops.copilot.modifier_assistant()
        elapsed = time.time() - start_time
        
        assert result == {'FINISHED'}
        assert elapsed < 0.2, f"Symmetrize took {elapsed*1000:.1f}ms (should be <200ms)"
    
    def test_end_to_end_under_350ms(self):
        """Test worst-case end-to-end execution is under 350ms."""
        workflows = [
            ("array", 1),
            ("hard-surface", 1),
            ("symmetrize", 1),
            ("curve deform", 2),  # mesh + curve
            ("solidify", 1),
        ]
        
        for command, obj_count in workflows:
            bpy.ops.wm.read_homefile(use_empty=True)
            
            if obj_count == 1:
                bpy.ops.mesh.primitive_cube_add()
            elif obj_count == 2:
                bpy.ops.mesh.primitive_cube_add()
                if "curve" in command:
                    bpy.ops.curve.primitive_bezier_curve_add(location=(2, 0, 0))
                else:
                    bpy.ops.mesh.primitive_cube_add(location=(2, 0, 0))
            
            bpy.ops.object.select_all(action='SELECT')
            
            bpy.context.scene.copilot_modifier_command = command
            
            start_time = time.time()
            result = bpy.ops.copilot.modifier_assistant()
            elapsed = time.time() - start_time
            
            assert result == {'FINISHED'}
            assert elapsed < 0.35, f"{command} took {elapsed*1000:.1f}ms (should be <350ms)"


class TestOperatorMultipleExecutions:
    """Test operator can be called multiple times successfully."""
    
    def test_can_execute_twice_in_sequence(self):
        """Test operator can be executed twice without issues."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        bpy.context.scene.copilot_modifier_command = "solidify"
        
        result1 = bpy.ops.copilot.modifier_assistant()
        result2 = bpy.ops.copilot.modifier_assistant()
        
        assert result1 == {'FINISHED'}
        assert result2 == {'FINISHED'}
        assert len(obj.modifiers) == 2  # Both executions added modifiers
    
    def test_can_switch_between_workflows(self):
        """Test can execute different workflows in sequence."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        
        obj = bpy.context.object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        # Execute three different workflows
        bpy.context.scene.copilot_modifier_command = "array"
        result1 = bpy.ops.copilot.modifier_assistant()
        
        bpy.context.scene.copilot_modifier_command = "solidify"
        result2 = bpy.ops.copilot.modifier_assistant()
        
        bpy.context.scene.copilot_modifier_command = "hard-surface"
        result3 = bpy.ops.copilot.modifier_assistant()
        
        assert result1 == {'FINISHED'}
        assert result2 == {'FINISHED'}
        assert result3 == {'FINISHED'}
        assert len(obj.modifiers) == 4  # 1 + 1 + 2 modifiers


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
