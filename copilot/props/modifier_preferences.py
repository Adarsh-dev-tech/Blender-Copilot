"""
Property groups for Modifier Assistant.

This module defines Blender property groups for storing modifier assistant
settings and user command text.
"""

import bpy
from bpy.props import StringProperty, IntProperty, FloatProperty, BoolProperty
from bpy.types import PropertyGroup


class ModifierAssistantProperties(PropertyGroup):
    """Properties for the Modifier Assistant feature."""
    
    # Command text input
    command_text: StringProperty(
        name="Command",
        description="Natural language command for modifier workflow (e.g., 'make hard-surface')",
        default="",
        maxlen=256
    )
    
    # Workflow default values
    array_count: IntProperty(
        name="Array Count",
        description="Default number of copies for array modifier",
        default=5,
        min=1,
        max=1000
    )
    
    array_offset_x: FloatProperty(
        name="Array Offset X",
        description="Default X-axis offset for array modifier",
        default=1.0,
        min=-100.0,
        max=100.0
    )
    
    bevel_segments: IntProperty(
        name="Bevel Segments",
        description="Default number of segments for bevel modifier",
        default=3,
        min=1,
        max=100
    )
    
    subdivision_levels: IntProperty(
        name="Subdivision Levels",
        description="Default viewport subdivision levels",
        default=2,
        min=0,
        max=6
    )
    
    solidify_thickness: FloatProperty(
        name="Solidify Thickness",
        description="Default thickness for solidify modifier (in meters)",
        default=0.01,
        min=0.0001,
        max=10.0,
        unit='LENGTH'
    )
    
    # UI preferences
    show_command_help: BoolProperty(
        name="Show Command Help",
        description="Display recognized commands in the panel as help text",
        default=True
    )
    
    show_selection_info: BoolProperty(
        name="Show Selection Info",
        description="Display current selection count and types in panel",
        default=True
    )


# Registration functions
classes = (
    ModifierAssistantProperties,
)


def register():
    """Register property groups."""
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Add properties to Scene
    bpy.types.Scene.modifier_assistant = bpy.props.PointerProperty(
        type=ModifierAssistantProperties
    )
    
    # Add command text property directly to Scene for operator access
    bpy.types.Scene.copilot_modifier_command = bpy.props.StringProperty(
        name="Copilot Modifier Command",
        description="Natural language command for modifier assistant",
        default="",
        maxlen=256
    )


def unregister():
    """Unregister property groups."""
    # Remove command property from Scene
    if hasattr(bpy.types.Scene, 'copilot_modifier_command'):
        del bpy.types.Scene.copilot_modifier_command
    
    # Remove from Scene
    if hasattr(bpy.types.Scene, 'modifier_assistant'):
        del bpy.types.Scene.modifier_assistant
    
    # Unregister classes
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
