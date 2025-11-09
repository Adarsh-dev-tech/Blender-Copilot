"""Modifier Assistant Operator.

Main orchestration operator for the Intelligent Modifier Assistant feature.
Coordinates command parsing, context validation, and workflow execution.
"""

import bpy
from copilot.utils.command_parser import parse_command
from copilot.utils.context_validator import validate_context
from copilot.utils import modifier_workflows
from copilot.utils import modifier_feedback as feedback


class COPILOT_OT_modifier_assistant(bpy.types.Operator):
    """Intelligent Modifier Assistant - Natural language modifier workflows.
    
    Undo System Integration:
    -----------------------
    This operator uses bl_options = {'REGISTER', 'UNDO'} which ensures:
    - All workflow operations (modifiers, object transforms, BMesh operations) are 
      captured as a single atomic undo step
    - Complex workflows like Symmetrize (which apply scale, perform BMesh mirroring, 
      and replace objects) are fully reversible with one Ctrl+Z
    - Multiple modifiers added in one workflow (e.g., Hard-Surface) undo together
    - Curve deform prerequisites (object transforms) are included in undo stack
    
    Undo Verification:
    - Simple workflows (Array, Solidify): Single modifier addition/removal
    - Multi-modifier workflows (Hard-Surface): Both Bevel+Subsurf undo atomically
    - Complex workflows (Symmetrize): Scale application, BMesh ops, object replacement all undo
    - Two-object workflows (Shrinkwrap, Curve Deform): Modifier + constraints undo together
    
    All workflows tested with manual Ctrl+Z to ensure complete state restoration.
    """

    bl_idname = "copilot.modifier_assistant"
    bl_label = "Apply Modifier Workflow"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        """Execute the modifier assistant workflow.

        Execution flow:
        1. Parse command text to identify workflow type
        2. Validate selection context against workflow requirements
        3. Execute appropriate workflow function
        4. Report result to user

        Returns:
            {'FINISHED'} on success, {'CANCELLED'} on error
        """
        # Step 1: Get command text from scene property
        command_text = context.scene.copilot_modifier_command

        # Validate command exists
        if not command_text or len(command_text.strip()) < 3:
            feedback.report_to_user(self, 'ERROR', feedback.ERROR_COMMAND_EMPTY)
            return {'CANCELLED'}

        # Step 2: Parse command to identify workflow
        workflow_type = parse_command(command_text)

        if workflow_type == 'UNKNOWN':
            feedback.report_to_user(self, 'ERROR', feedback.ERROR_COMMAND_NOT_UNDERSTOOD)
            return {'CANCELLED'}

        # Step 3: Validate context for workflow
        is_valid, error_message = validate_context(workflow_type)

        if not is_valid:
            self.report({'ERROR'}, error_message)
            return {'CANCELLED'}

        # Step 4: Execute workflow
        status, message = self._execute_workflow(workflow_type, context)

        # Step 5: Report result
        if status == {'FINISHED'}:
            self.report({'INFO'}, message)
        else:
            self.report({'ERROR'}, message)

        return status

    def _execute_workflow(self, workflow_type: str, context) -> tuple[set, str]:
        """Route to appropriate workflow execution function.

        Args:
            workflow_type: Identified workflow identifier
            context: Blender context with selection

        Returns:
            Tuple of (status, message)
        """
        selected = context.selected_objects
        active = context.active_object

        # Route to workflow implementations
        if workflow_type == 'SMART_ARRAY':
            return self._execute_smart_array(selected, active)

        elif workflow_type == 'HARD_SURFACE':
            return modifier_workflows.apply_hard_surface_setup(active)

        elif workflow_type == 'SYMMETRIZE':
            return modifier_workflows.apply_symmetrize(active)

        elif workflow_type == 'CURVE_DEFORM':
            return self._execute_curve_deform(selected)

        elif workflow_type == 'SOLIDIFY':
            return modifier_workflows.apply_solidify(active)

        elif workflow_type == 'SHRINKWRAP':
            return self._execute_shrinkwrap(selected, active)

        else:
            error_msg = feedback.format_message(
                feedback.ERROR_WORKFLOW_NOT_IMPLEMENTED,
                workflow_type=workflow_type
            )
            return {'CANCELLED'}, error_msg

    def _execute_smart_array(self, selected, active) -> tuple[set, str]:
        """Execute Smart Array workflow (handles both variants)."""
        if len(selected) == 1:
            # Single object variant
            return modifier_workflows.apply_smart_array_single(active)
        else:
            # Object offset variant (mesh + empty)
            mesh_obj, empty_obj = modifier_workflows.identify_mesh_and_empty(
                selected[0], selected[1]
            )
            if mesh_obj is None:
                error_msg = feedback.format_message(
                    feedback.ERROR_OBJECT_IDENTIFICATION_FAILED,
                    expected_types="mesh and empty"
                )
                return {'CANCELLED'}, error_msg
            return modifier_workflows.apply_smart_array_controlled(mesh_obj, empty_obj)

    def _execute_curve_deform(self, selected) -> tuple[set, str]:
        """Execute Curve Deform workflow."""
        mesh_obj, curve_obj = modifier_workflows.identify_mesh_and_curve(
            selected[0], selected[1]
        )
        if mesh_obj is None:
            error_msg = feedback.format_message(
                feedback.ERROR_OBJECT_IDENTIFICATION_FAILED,
                expected_types="mesh and curve"
            )
            return {'CANCELLED'}, error_msg
        return modifier_workflows.apply_curve_deform(mesh_obj, curve_obj)

    def _execute_shrinkwrap(self, selected, active) -> tuple[set, str]:
        """Execute Shrinkwrap workflow."""
        # Active object is source, other selected object is target
        target = [obj for obj in selected if obj != active][0]
        return modifier_workflows.apply_shrinkwrap(active, target)


# Registration
def register():
    """Register operator."""
    bpy.utils.register_class(COPILOT_OT_modifier_assistant)


def unregister():
    """Unregister operator."""
    bpy.utils.unregister_class(COPILOT_OT_modifier_assistant)
