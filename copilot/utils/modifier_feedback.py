"""User Feedback Utilities for Modifier Assistant.

This module provides centralized error messages and feedback functions
to ensure consistent user communication across the modifier assistant feature.
"""

# Error message constants matching operator contract specifications

# Command recognition errors
ERROR_COMMAND_NOT_UNDERSTOOD = (
    "Command not understood. Try: 'make array', 'hard-surface', 'mirror', "
    "'solidify', 'curve deform', or 'shrinkwrap'"
)

ERROR_COMMAND_EMPTY = "Please enter a command"

# Selection validation errors
ERROR_NO_SELECTION = "Please select an object first"

ERROR_WRONG_OBJECT_COUNT = "This command requires {expected} selected object(s), but {actual} are selected"

ERROR_WRONG_OBJECT_TYPES_MESH = "This command requires a mesh object to be selected"

ERROR_WRONG_OBJECT_TYPES_TWO_MESHES = "This command requires two mesh objects to be selected"

ERROR_WRONG_OBJECT_TYPES_MESH_EMPTY = "This command requires two selected objects: a mesh and an empty"

ERROR_WRONG_OBJECT_TYPES_MESH_CURVE = "This command requires two selected objects: a mesh and a curve"

ERROR_WRONG_MODE = "This command must be run in Object Mode (currently in {current_mode})"

ERROR_NO_ACTIVE_OBJECT = "Please ensure one of the selected objects is active"

# Execution errors
ERROR_SCALE_APPLICATION_FAILED = "Failed to apply scale to {object_name}"

ERROR_WORKFLOW_NOT_IMPLEMENTED = "Workflow not implemented: {workflow_type}"

ERROR_OBJECT_IDENTIFICATION_FAILED = "Could not identify {expected_types} objects"

# Success messages
SUCCESS_ARRAY_SINGLE = "Array modifier added with 5 copies on X-axis"

SUCCESS_ARRAY_CONTROLLED = "Array modifier added with empty object control"

SUCCESS_HARD_SURFACE = "Hard-surface setup applied (Bevel + Subdivision + Smooth)"

SUCCESS_SYMMETRIZE = "Symmetrize applied on X-axis (scale applied, positive X deleted)"

SUCCESS_CURVE_DEFORM = "Curve deform applied (scales applied, origins aligned)"

SUCCESS_SOLIDIFY = "Solidify modifier added (thickness: 0.01m, even offset enabled)"

SUCCESS_SHRINKWRAP = "Shrinkwrap modifier added (target: {target_name})"


def format_message(template: str, **kwargs) -> str:
    """Format a message template with provided values.

    Args:
        template: Message template with {placeholder} markers
        **kwargs: Values to substitute into placeholders

    Returns:
        Formatted message string

    Example:
        >>> format_message(ERROR_WRONG_OBJECT_COUNT, expected=2, actual=1)
        'This command requires 2 selected object(s), but 1 are selected'
    """
    return template.format(**kwargs)


def report_to_user(operator, level: str, message: str):
    """Report feedback to user through operator's report system.

    This is a thin wrapper around operator.report() for consistency
    and potential future enhancements (logging, analytics, etc.).

    Args:
        operator: Blender operator instance (must have report() method)
        level: Message level - 'INFO', 'WARNING', 'ERROR', 'DEBUG'
        message: Message text to display

    Example:
        >>> report_to_user(self, 'ERROR', ERROR_NO_SELECTION)
        >>> report_to_user(self, 'INFO', SUCCESS_ARRAY_SINGLE)
    """
    operator.report({level}, message)
