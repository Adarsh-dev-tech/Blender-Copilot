"""Command Parser for Intelligent Modifier Assistant.

This module parses natural language commands and maps them to specific modifier workflows.
Uses simple pattern matching for <10ms performance.
"""

from typing import Literal

# Type alias for workflow identifiers
WorkflowType = Literal[
    'SMART_ARRAY',
    'HARD_SURFACE',
    'SYMMETRIZE',
    'CURVE_DEFORM',
    'SOLIDIFY',
    'SHRINKWRAP',
    'UNKNOWN'
]

# Command pattern dictionary - order matters for priority
COMMAND_PATTERNS = {
    'SMART_ARRAY': [
        'array',
        'duplicate',
        'copies',
        'make 5',
        'create array',
    ],
    'HARD_SURFACE': [
        'hard-surface',
        'hard surface',
        'subdivision',
        'subd',
        'bevel',
    ],
    'SYMMETRIZE': [
        'mirror',
        'symmetrize',
        'symmetric',
        'sym',
    ],
    'CURVE_DEFORM': [
        'curve deform',
        'deform',
        'follow',
        'path',
        'bend',
    ],
    'SOLIDIFY': [
        'solidify',
        'thickness',
        'thicken',
        'solid',
    ],
    'SHRINKWRAP': [
        'shrinkwrap',
        'wrap',
        'conform',
    ],
}


def parse_command(command_text: str) -> WorkflowType:
    """Parse natural language command to workflow type.

    Uses case-insensitive pattern matching against COMMAND_PATTERNS dictionary.
    Returns first matching workflow or 'UNKNOWN' if no patterns match.

    Performance target: < 10ms

    Args:
        command_text: User's natural language command (e.g., "make array")

    Returns:
        Workflow type identifier: 'SMART_ARRAY', 'HARD_SURFACE', 'SYMMETRIZE',
        'CURVE_DEFORM', 'SOLIDIFY', 'SHRINKWRAP', or 'UNKNOWN'

    Examples:
        >>> parse_command("create an array")
        'SMART_ARRAY'
        >>> parse_command("Make this hard-surface")
        'HARD_SURFACE'
        >>> parse_command("xyz random text")
        'UNKNOWN'
    """
    # Normalize command: lowercase and strip whitespace
    normalized = command_text.lower().strip()

    # Early return for empty/too short commands
    if len(normalized) < 3:
        return 'UNKNOWN'

    # Check each workflow pattern in priority order
    for workflow_type, patterns in COMMAND_PATTERNS.items():
        for pattern in patterns:
            if pattern.lower() in normalized:
                return workflow_type  # type: ignore

    return 'UNKNOWN'
