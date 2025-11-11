"""Pytest configuration for integration tests.

This module handles Blender add-on registration for tests that need it.
"""

import sys
from pathlib import Path

# Import Blender
import bpy  # noqa: F401

# Add project root to path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


def pytest_sessionstart(session):
    """Called before test session starts - register scene property."""
    # Register the copilot_modifier_command property directly
    bpy.types.Scene.copilot_modifier_command = bpy.props.StringProperty(
        name="Copilot Modifier Command",
        description="Natural language command for modifier assistant",
        default="",
        maxlen=256
    )
    print("✓ Registered copilot_modifier_command scene property for test session")


def pytest_sessionfinish(session, exitstatus):
    """Called after test session finishes - clean up."""
    # Remove the property
    try:
        if hasattr(bpy.types.Scene, 'copilot_modifier_command'):
            del bpy.types.Scene.copilot_modifier_command
        print("✓ Unregistered copilot_modifier_command scene property")
    except Exception as e:
        print(f"Note: Could not unregister property: {e}")
