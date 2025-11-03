#!/usr/bin/env python3
"""Quick test to verify operator registration in Blender."""

import bpy

# Check if operator is registered
if hasattr(bpy.ops.copilot, 'modifier_assistant'):
    print("✓ Operator bpy.ops.copilot.modifier_assistant is registered")
else:
    print("✗ Operator bpy.ops.copilot.modifier_assistant NOT found")
    print("Available copilot operators:")
    print(dir(bpy.ops.copilot))

# Check if scene property exists
if hasattr(bpy.types.Scene, 'copilot_modifier_command'):
    print("✓ Scene property copilot_modifier_command exists")
else:
    print("✗ Scene property copilot_modifier_command NOT found")

# Try to import the operator class
try:
    from copilot.operators.modifier_assistant import COPILOT_OT_modifier_assistant
    print(f"✓ Successfully imported COPILOT_OT_modifier_assistant: {COPILOT_OT_modifier_assistant}")
except Exception as e:
    print(f"✗ Failed to import operator: {e}")
