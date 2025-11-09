"""
Add-on preferences for Blender Copilot.

This module defines the add-on preferences UI that appears in Blender's
Edit > Preferences > Add-ons panel when the user expands the Blender Copilot add-on.
"""

import bpy
from bpy.types import AddonPreferences
from bpy.props import IntProperty, FloatProperty, BoolProperty


class CopilotAddonPreferences(AddonPreferences):
    """Preferences for Blender Copilot add-on."""
    
    # This must match the add-on name (the package name)
    bl_idname = __package__
    
    # Modifier Assistant Defaults
    default_array_count: IntProperty(
        name="Default Array Count",
        description="Default number of copies for Smart Array workflow",
        default=5,
        min=1,
        max=1000
    )
    
    default_array_offset_x: FloatProperty(
        name="Default Array Offset X",
        description="Default X-axis offset for Smart Array workflow",
        default=1.0,
        min=-100.0,
        max=100.0
    )
    
    default_bevel_segments: IntProperty(
        name="Default Bevel Segments",
        description="Default number of segments for Hard Surface bevel modifier",
        default=3,
        min=1,
        max=100
    )
    
    default_subdivision_levels: IntProperty(
        name="Default Subdivision Levels",
        description="Default viewport subdivision levels for Hard Surface workflow",
        default=2,
        min=0,
        max=6
    )
    
    default_solidify_thickness: FloatProperty(
        name="Default Solidify Thickness",
        description="Default thickness for Solidify modifier (in meters)",
        default=0.01,
        min=0.0001,
        max=10.0,
        unit='LENGTH'
    )
    
    # UI Preferences
    show_command_help: BoolProperty(
        name="Show Command Help",
        description="Display recognized commands in the Modifier Assistant panel as help text",
        default=True
    )
    
    show_selection_info: BoolProperty(
        name="Show Selection Info",
        description="Display current selection count and types in Modifier Assistant panel",
        default=True
    )
    
    # Performance Preferences
    performance_mode: BoolProperty(
        name="Performance Mode",
        description="Skip some validation checks for faster execution (use with caution)",
        default=False
    )
    
    show_performance_metrics: BoolProperty(
        name="Show Performance Metrics",
        description="Log execution time metrics to console (for debugging)",
        default=False
    )
    
    def draw(self, context):
        """Draw the preferences UI."""
        layout = self.layout
        
        # Modifier Assistant section
        box = layout.box()
        box.label(text="Modifier Assistant Defaults", icon='MODIFIER')
        
        col = box.column(align=True)
        col.prop(self, "default_array_count")
        col.prop(self, "default_array_offset_x")
        
        col = box.column(align=True)
        col.prop(self, "default_bevel_segments")
        col.prop(self, "default_subdivision_levels")
        
        col = box.column(align=True)
        col.prop(self, "default_solidify_thickness")
        
        # UI Preferences section
        box = layout.box()
        box.label(text="UI Preferences", icon='PREFERENCES')
        
        col = box.column(align=True)
        col.prop(self, "show_command_help")
        col.prop(self, "show_selection_info")
        
        # Performance section
        box = layout.box()
        box.label(text="Performance", icon='TIME')
        
        col = box.column(align=True)
        col.prop(self, "performance_mode")
        col.prop(self, "show_performance_metrics")
        
        if self.performance_mode:
            col.label(text="Warning: Performance mode may skip important validations", icon='ERROR')


def get_addon_preferences(context=None):
    """
    Convenience function to get add-on preferences.
    
    Args:
        context: Blender context (optional, uses bpy.context if not provided)
    
    Returns:
        CopilotAddonPreferences: The add-on preferences instance
    """
    if context is None:
        context = bpy.context
    
    preferences = context.preferences.addons[__package__].preferences
    return preferences


# Registration
classes = (
    CopilotAddonPreferences,
)


def register():
    """Register preferences classes."""
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    """Unregister preferences classes."""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
