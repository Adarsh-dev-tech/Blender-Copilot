import bpy

def is_valid_selection(obj=None):
    """
    Check if there is a valid object selection.
    
    Args:
        obj: Optional object to check, defaults to active object
    
    Returns:
        bool: True if selection is valid
    """
    if obj is None:
        obj = bpy.context.active_object
    
    return obj is not None

def is_valid_object_type(obj_type):
    """
    Check if object type is valid for lighting setup.
    
    Args:
        obj_type: String representing object type
    
    Returns:
        bool: True if object type is supported
    """
    valid_types = {'MESH', 'CURVE', 'SURFACE', 'META', 'FONT'}
    return obj_type in valid_types

def is_valid_mode(mode=None):
    """
    Check if current mode is valid for operator execution.
    
    Args:
        mode: Optional mode string, defaults to current mode
    
    Returns:
        bool: True if mode is valid
    """
    if mode is None:
        mode = bpy.context.mode
    
    return mode == 'OBJECT'

def validate_target_object(obj=None):
    """
    Comprehensive validation of target object for lighting setup.
    
    Args:
        obj: Object to validate, defaults to active object
    
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    if obj is None:
        obj = bpy.context.active_object
    
    # Check if object exists
    if not is_valid_selection(obj):
        return False, "No object selected"
    
    # Check object type
    if not is_valid_object_type(obj.type):
        return False, f"Object type '{obj.type}' is not supported. Use MESH, CURVE, SURFACE, META, or FONT objects."
    
    # Check mode
    if not is_valid_mode():
        return False, f"Must be in Object mode. Current mode: {bpy.context.mode}"
    
    return True, ""

def get_scene_context_info():
    """
    Get information about current scene context for validation.
    
    Returns:
        dict: Context information including mode, active object, etc.
    """
    return {
        'mode': bpy.context.mode,
        'active_object': bpy.context.active_object,
        'selected_objects': bpy.context.selected_objects,
        'scene': bpy.context.scene,
        'view_layer': bpy.context.view_layer
    }