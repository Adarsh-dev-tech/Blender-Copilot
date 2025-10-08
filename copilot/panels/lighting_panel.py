import bpy
from bpy.types import Panel


class COPILOT_PT_lighting_panel(Panel):
    """Panel for Copilot lighting tools in 3D Viewport"""
    
    bl_label = "Copilot Lighting"
    bl_idname = "COPILOT_PT_lighting_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Copilot"
    bl_context = "objectmode"
    
    def draw(self, context):
        """Draw the panel UI"""
        layout = self.layout
        
        # Main operator button
        col = layout.column(align=True)
        col.scale_y = 1.5
        
        # Check if we can execute the operator
        active_obj = context.active_object
        can_execute = (active_obj is not None and 
                      context.mode == 'OBJECT' and
                      active_obj.type in {'MESH', 'CURVE', 'SURFACE', 'META', 'FONT'})
        
        if can_execute:
            op = col.operator("copilot.create_three_point_lighting", 
                            text="Create Three-Point Lighting", 
                            icon='LIGHT')
        else:
            col.enabled = False
            col.operator("copilot.create_three_point_lighting", 
                        text="Create Three-Point Lighting", 
                        icon='LIGHT')
        
        # Status information
        layout.separator()
        
        if not active_obj:
            layout.label(text="No object selected", icon='INFO')
        elif context.mode != 'OBJECT':
            layout.label(text="Must be in Object Mode", icon='INFO')
        elif active_obj.type not in {'MESH', 'CURVE', 'SURFACE', 'META', 'FONT'}:
            layout.label(text=f"Object type '{active_obj.type}' not supported", icon='INFO')
        else:
            layout.label(text=f"Ready for: {active_obj.name}", icon='CHECKMARK')
        
        # Advanced options (collapsible)
        if can_execute:
            layout.separator()
            
            box = layout.box()
            col = box.column()
            col.label(text="Advanced Options:", icon='SETTINGS')
            
            # Get the operator for property access
            # Note: This is a simplified approach for the UI
            col.label(text="Key Light Angle: 45°")
            col.label(text="Fill Light Angle: -45°") 
            col.label(text="Rim Light Angle: 135°")
            col.label(text="Distance Scale: 1.0")
            
            # Info about customization
            col.separator()
            col.label(text="Use F9 after operation to adjust", icon='INFO')


def register():
    bpy.utils.register_class(COPILOT_PT_lighting_panel)


def unregister():
    bpy.utils.unregister_class(COPILOT_PT_lighting_panel)


if __name__ == "__main__":
    register()