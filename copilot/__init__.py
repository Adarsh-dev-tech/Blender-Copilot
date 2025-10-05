bl_info = {
    "name": "Blender Copilot - Three-Point Lighting",
    "author": "Adarsh Hinsodiya",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Copilot Tab",
    "description": "Automated three-point lighting setup for selected objects.",
    "category": "Lighting",
}

import bpy

# Registration framework for operators and panels
classes = []

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
