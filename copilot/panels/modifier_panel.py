"""Modifier Assistant Panel for Blender 3D View sidebar.

This panel provides the UI for the Intelligent Modifier Assistant feature.
"""

import bpy


class COPILOT_PT_modifier_assistant(bpy.types.Panel):
    """Panel for Modifier Assistant in 3D View sidebar."""

    bl_label = "Modifier Assistant"
    bl_idname = "COPILOT_PT_modifier_assistant"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Copilot'

    def draw(self, context):
        """Draw the panel UI."""
        layout = self.layout
        scene = context.scene
        
        # Get preferences for UI visibility options
        try:
            from copilot.preferences import get_addon_preferences
            prefs = get_addon_preferences(context)
        except (ImportError, KeyError):
            prefs = None

        # Command input section
        box = layout.box()
        box.label(text="Natural Language Command:", icon='CONSOLE')
        box.prop(scene, "copilot_modifier_command", text="")

        # Execute button
        row = box.row()
        row.scale_y = 1.5
        row.operator("copilot.modifier_assistant", text="Execute", icon='PLAY')

        # Selection info section (controlled by preferences)
        if prefs is None or prefs.show_selection_info:
            layout.separator()
            info_box = layout.box()
            info_box.label(text="Selection Info:", icon='INFO')

            # Show current selection count and types
            selected = context.selected_objects
            active = context.active_object

            if not selected:
                info_box.label(text="No objects selected", icon='ERROR')
            else:
                info_box.label(text=f"Selected: {len(selected)} object(s)")

                # Show object types
                if len(selected) <= 3:
                    for obj in selected:
                        icon = 'MESH_DATA' if obj.type == 'MESH' else 'OUTLINER_OB_' + obj.type
                        active_marker = " (active)" if obj == active else ""
                        info_box.label(text=f"  • {obj.name} ({obj.type}){active_marker}")
                else:
                    # Count by type
                    type_counts = {}
                    for obj in selected:
                        type_counts[obj.type] = type_counts.get(obj.type, 0) + 1
                    for obj_type, count in type_counts.items():
                        info_box.label(text=f"  • {obj_type}: {count}")

                # Show current mode
                info_box.label(text=f"Mode: {context.mode}")

        # Help section (controlled by preferences)
        if prefs is None or prefs.show_command_help:
            layout.separator()
            help_box = layout.box()
            help_box.label(text="Recognized Commands:", icon='QUESTION')

            col = help_box.column(align=True)
            col.scale_y = 0.8
            col.label(text='• "array" / "make 5 copies" → Smart Array')
            col.label(text='• "hard-surface" / "subd" → Hard-Surface')
            col.label(text='• "mirror" / "symmetrize" → Symmetrize')
            col.label(text='• "curve deform" / "bend" → Curve Deform')
            col.label(text='• "solidify" / "add thickness" → Solidify')
            col.label(text='• "shrinkwrap" / "wrap" → Shrinkwrap')


# Registration
def register():
    """Register panel."""
    bpy.utils.register_class(COPILOT_PT_modifier_assistant)


def unregister():
    """Unregister panel."""
    bpy.utils.unregister_class(COPILOT_PT_modifier_assistant)


if __name__ == "__main__":
    register()
