import bpy
import mathutils
from .light_defaults import LIGHT_DEFAULTS, LIGHT_NAMES, TARGET_EMPTY_NAME, COLLECTION_NAME_PREFIX

def create_area_light(name, location=(0, 0, 0), power=100, color_temp=5600, size=1.0):
    """
    Create an area light with specified properties.
    
    Args:
        name: Name for the light object
        location: World location tuple (x, y, z)
        power: Light power in watts
        color_temp: Color temperature in Kelvin
        size: Light size
    
    Returns:
        bpy.types.Object: Created light object
    """
    # Create light data
    light_data = bpy.data.lights.new(name=name, type='AREA')
    light_data.energy = power
    light_data.color = color_temperature_to_rgb(color_temp)
    light_data.size = size
    
    # Create light object
    light_object = bpy.data.objects.new(name, light_data)
    light_object.location = location
    
    # Link to scene
    bpy.context.collection.objects.link(light_object)
    
    return light_object

def create_target_empty(name, location=(0, 0, 0)):
    """
    Create an empty object to serve as track-to target.
    
    Args:
        name: Name for the empty object
        location: World location tuple (x, y, z)
    
    Returns:
        bpy.types.Object: Created empty object
    """
    empty = bpy.data.objects.new(name, None)
    empty.location = location
    empty.empty_display_type = 'SPHERE'
    empty.empty_display_size = 0.5
    
    # Link to scene
    bpy.context.collection.objects.link(empty)
    
    return empty

def add_track_to_constraint(light_obj, target_obj):
    """
    Add a Track To constraint to make light point at target.
    
    Args:
        light_obj: Light object that will track
        target_obj: Target object to track to
    
    Returns:
        bpy.types.Constraint: Created constraint
    """
    constraint = light_obj.constraints.new(type='TRACK_TO')
    constraint.target = target_obj
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'
    
    return constraint

def create_lighting_collection(name):
    """
    Create a new collection for organizing lighting rig components.
    
    Args:
        name: Name for the collection
    
    Returns:
        bpy.types.Collection: Created collection
    """
    # Create collection
    collection = bpy.data.collections.new(name)
    
    # Link to scene
    bpy.context.scene.collection.children.link(collection)
    
    return collection

def move_object_to_collection(obj, collection):
    """
    Move an object to a specific collection.
    
    Args:
        obj: Object to move
        collection: Target collection
    """
    # Remove from all current collections
    for coll in obj.users_collection:
        coll.objects.unlink(obj)
    
    # Add to target collection
    collection.objects.link(obj)

def color_temperature_to_rgb(temp_k):
    """
    Convert color temperature in Kelvin to RGB values.
    Simplified approximation for common lighting temperatures.
    
    Args:
        temp_k: Temperature in Kelvin
    
    Returns:
        tuple: (r, g, b) values from 0.0 to 1.0
    """
    # Simplified conversion for common lighting temperatures
    if temp_k <= 3000:
        return (1.0, 0.6, 0.3)  # Warm/tungsten
    elif temp_k <= 4000:
        return (1.0, 0.8, 0.6)  # Warm white
    elif temp_k <= 5000:
        return (1.0, 0.9, 0.8)  # Neutral
    elif temp_k <= 6000:
        return (1.0, 1.0, 0.95) # Cool white
    else:
        return (0.8, 0.9, 1.0)  # Daylight/cool

def generate_unique_name(base_name, existing_names=None):
    """
    Generate a unique name by appending numbers if needed.
    
    Args:
        base_name: Base name to start with
        existing_names: Optional set of existing names to avoid
    
    Returns:
        str: Unique name
    """
    if existing_names is None:
        existing_names = {obj.name for obj in bpy.data.objects}
    
    if base_name not in existing_names:
        return base_name
    
    counter = 1
    while f"{base_name}.{counter:03d}" in existing_names:
        counter += 1
    
    return f"{base_name}.{counter:03d}"

def cleanup_lighting_rig(collection_name):
    """
    Remove a lighting rig collection and all its contents.
    
    Args:
        collection_name: Name of collection to remove
    
    Returns:
        bool: True if cleanup was successful
    """
    collection = bpy.data.collections.get(collection_name)
    if not collection:
        return False
    
    # Remove all objects in collection
    for obj in collection.objects:
        bpy.data.objects.remove(obj, do_unlink=True)
    
    # Remove collection
    bpy.data.collections.remove(collection)
    
    return True