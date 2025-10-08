"""
Blender Copilot - Automated Three-Point Lighting Setup

A professional Blender add-on that automates the creation of cinematic three-point
lighting rigs for selected objects. The add-on analyzes object geometry and creates
appropriately positioned key, fill, and rim lights with proper constraints and
organization.

Features:
- One-click three-point lighting setup
- Automatic object analysis and light positioning  
- Professional lighting ratios and color temperatures
- Organized collection hierarchy
- Full undo/redo support
- Customizable light angles and distances

Author: Adarsh Hinsodiya
License: MIT
Version: 1.0.0
"""

bl_info = {
    "name": "Blender Copilot - Automated Three-Point Lighting",
    "author": "Adarsh Hinsodiya", 
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Copilot Tab",
    "description": "Automated three-point lighting setup with professional positioning and ratios",
    "warning": "",
    "doc_url": "https://github.com/Adarsh-dev-tech/Blender-Copilot",
    "tracker_url": "https://github.com/Adarsh-dev-tech/Blender-Copilot/issues",
    "support": "COMMUNITY",
    "category": "Lighting",
}

import bpy

# Import add-on modules
from .operators import lighting
from .panels import lighting_panel

# Classes to register
classes = [
    lighting.COPILOT_OT_create_three_point_lighting,
    lighting_panel.COPILOT_PT_lighting_panel,
]

def register():
    """Register all add-on classes and components"""
    for cls in classes:
        bpy.utils.register_class(cls)
    
    print("Blender Copilot: Three-Point Lighting add-on registered")

def unregister():
    """Unregister all add-on classes and components"""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    print("Blender Copilot: Three-Point Lighting add-on unregistered")

if __name__ == "__main__":
    register()
