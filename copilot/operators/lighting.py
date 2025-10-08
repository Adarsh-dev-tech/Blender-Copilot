"""
Three-Point Lighting Operator for Blender Copilot

This module implements the main operator for creating automated three-point lighting setups.
The operator analyzes the selected object and creates a professional lighting rig with
key, fill, and rim lights positioned using cinematic lighting principles.

Classes:
    COPILOT_OT_create_three_point_lighting: Main operator for lighting creation

Usage:
    bpy.ops.copilot.create_three_point_lighting()
    
    # With custom angles
    bpy.ops.copilot.create_three_point_lighting(
        key_angle=30.0,
        fill_angle=-60.0,
        rim_angle=120.0,
        distance_scale=1.5
    )

Requirements:
    - Active object must be selected
    - Must be in Object Mode
    - Object type must be MESH, CURVE, SURFACE, META, or FONT
"""

import bpy
import mathutils
from typing import Set, Tuple, Dict, Any, Optional
from bpy.types import Operator
from bpy.props import FloatProperty

from ..utils.validation import validate_target_object
from ..utils.geometry import analyze_bounding_box, calculate_light_position
from ..utils.blender_helpers import (
    create_area_light, create_target_empty, add_track_to_constraint,
    create_lighting_collection, move_object_to_collection,
    generate_unique_name
)
from ..utils.light_defaults import (
    LIGHT_DEFAULTS, LIGHT_NAMES, TARGET_EMPTY_NAME, COLLECTION_NAME_PREFIX
)


class COPILOT_OT_create_three_point_lighting(Operator):
    """Create a professional three-point lighting setup for the selected object"""
    
    bl_idname = "copilot.create_three_point_lighting"
    bl_label = "Create Three-Point Lighting"
    bl_description = "Creates a professional three-point lighting setup for the selected object"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Operator properties for customization
    key_angle: FloatProperty(
        name="Key Light Angle",
        default=45.0,
        min=-180.0,
        max=180.0,
        description="Horizontal angle for key light"
    )
    
    fill_angle: FloatProperty(
        name="Fill Light Angle",
        default=-45.0,
        min=-180.0,
        max=180.0,
        description="Horizontal angle for fill light"
    )
    
    rim_angle: FloatProperty(
        name="Rim Light Angle",
        default=135.0,
        min=-180.0,
        max=180.0,
        description="Horizontal angle for rim light"
    )
    
    distance_scale: FloatProperty(
        name="Distance Scale",
        default=1.0,
        min=0.1,
        max=10.0,
        description="Scale factor for light distances"
    )

    def execute(self, context):
        """Main execution method for the lighting operator"""
        try:
            # Validate target object
            target_obj = context.active_object
            is_valid, error_msg = validate_target_object(target_obj)
            
            if not is_valid:
                self.report({'ERROR'}, error_msg)
                return {'CANCELLED'}
            
            # Analyze target object geometry
            bbox_info = analyze_bounding_box(target_obj)
            if not bbox_info:
                self.report({'ERROR'}, "Could not analyze object geometry")
                return {'CANCELLED'}
            
            target_center = bbox_info['center']
            object_radius = bbox_info['radius']
            
            # Create lighting collection
            collection_name = generate_unique_name(
                f"{COLLECTION_NAME_PREFIX}_{target_obj.name}"
            )
            lighting_collection = create_lighting_collection(collection_name)
            
            # Create target empty for constraints
            target_empty_name = generate_unique_name(
                f"{TARGET_EMPTY_NAME}_{target_obj.name}"
            )
            target_empty = create_target_empty(target_empty_name, target_center)
            move_object_to_collection(target_empty, lighting_collection)
            
            # Store created objects for potential cleanup on error
            created_objects = [target_empty]
            
            try:
                # Create lights based on configuration
                lights_created = self._create_lighting_rig(
                    target_center, object_radius, target_empty, 
                    lighting_collection, created_objects
                )
                
                if not lights_created:
                    self._cleanup_on_error(created_objects, lighting_collection)
                    self.report({'ERROR'}, "Failed to create lighting rig")
                    return {'CANCELLED'}
                
                # Report success
                self.report({'INFO'}, f"Created three-point lighting rig for '{target_obj.name}'")
                return {'FINISHED'}
                
            except Exception as e:
                # Cleanup on error
                self._cleanup_on_error(created_objects, lighting_collection)
                self.report({'ERROR'}, f"Error creating lighting rig: {str(e)}")
                return {'CANCELLED'}
                
        except Exception as e:
            self.report({'ERROR'}, f"Unexpected error: {str(e)}")
            return {'CANCELLED'}
    
    def _create_lighting_rig(self, target_center, object_radius, target_empty, 
                            lighting_collection, created_objects):
        """Create the three lights with proper positioning and constraints"""
        
        # Light configurations with custom angles
        light_configs = {
            'KEY': {
                **LIGHT_DEFAULTS['KEY'],
                'horizontal_angle': self.key_angle
            },
            'FILL': {
                **LIGHT_DEFAULTS['FILL'], 
                'horizontal_angle': self.fill_angle
            },
            'RIM': {
                **LIGHT_DEFAULTS['RIM'],
                'horizontal_angle': self.rim_angle
            }
        }
        
        lights_created = 0
        
        for light_type, config in light_configs.items():
            try:
                # Calculate light position
                distance = object_radius * config['distance_multiplier'] * self.distance_scale
                light_pos = calculate_light_position(
                    target_center,
                    config['horizontal_angle'],
                    config['vertical_angle'],
                    distance
                )
                
                # Create light
                light_name = generate_unique_name(LIGHT_NAMES[light_type])
                light_obj = create_area_light(
                    light_name,
                    light_pos,
                    config['power_watts'],
                    config['color_temperature'],
                    config['size']
                )
                
                # Add track-to constraint
                add_track_to_constraint(light_obj, target_empty)
                
                # Move to collection
                move_object_to_collection(light_obj, lighting_collection)
                created_objects.append(light_obj)
                
                lights_created += 1
                
            except Exception as e:
                print(f"Error creating {light_type} light: {e}")
                continue
        
        return lights_created == 3
    
    def _cleanup_on_error(self, created_objects, collection):
        """Clean up created objects if operation fails"""
        try:
            # Remove created objects
            for obj in created_objects:
                if obj and obj.name in bpy.data.objects:
                    bpy.data.objects.remove(obj, do_unlink=True)
            
            # Remove collection if it exists and is empty
            if collection and collection.name in bpy.data.collections:
                if len(collection.objects) == 0:
                    bpy.data.collections.remove(collection)
                    
        except Exception as e:
            print(f"Error during cleanup: {e}")

    @classmethod
    def poll(cls, context):
        """Check if operator can be executed in current context"""
        return (context.active_object is not None and 
                context.mode == 'OBJECT')


def register():
    bpy.utils.register_class(COPILOT_OT_create_three_point_lighting)


def unregister():
    bpy.utils.unregister_class(COPILOT_OT_create_three_point_lighting)


if __name__ == "__main__":
    register()