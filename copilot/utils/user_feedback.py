import bpy

# Error message templates following Blender UI conventions
ERROR_MESSAGES = {
    'NO_SELECTION': {
        'message': "No object selected",
        'details': "Select a mesh, curve, surface, metaball, or text object to create lighting for",
        'icon': 'ERROR'
    },
    'INVALID_MODE': {
        'message': "Must be in Object Mode",
        'details': "Switch to Object Mode (Tab key) before creating lighting",
        'icon': 'ERROR'
    },
    'INVALID_OBJECT_TYPE': {
        'message': "Object type not supported", 
        'details': "Select a mesh, curve, surface, metaball, or text object. Cameras, lights, and empties are not supported",
        'icon': 'ERROR'
    },
    'GEOMETRY_ANALYSIS_FAILED': {
        'message': "Could not analyze object geometry",
        'details': "The selected object may be corrupted or have invalid geometry. Try selecting a different object",
        'icon': 'ERROR'
    },
    'CREATION_FAILED': {
        'message': "Failed to create lighting rig",
        'details': "An error occurred while creating the lights. Check the console for details",
        'icon': 'ERROR'
    },
    'PERMISSION_ERROR': {
        'message': "Cannot modify scene",
        'details': "The scene may be locked or you may not have permission to add objects",
        'icon': 'ERROR'
    }
}

SUCCESS_MESSAGES = {
    'LIGHTING_CREATED': {
        'message': "Three-point lighting rig created successfully",
        'details': "Use F9 to adjust light angles and distances",
        'icon': 'CHECKMARK'
    },
    'LIGHTING_UPDATED': {
        'message': "Lighting rig updated",
        'details': "Changes applied to existing lighting setup",
        'icon': 'CHECKMARK'
    }
}

INFO_MESSAGES = {
    'READY_FOR_OBJECT': {
        'message': "Ready to create lighting",
        'details': "Selected object: {object_name}",
        'icon': 'INFO'
    },
    'MULTIPLE_OBJECTS': {
        'message': "Multiple objects selected",
        'details': "Lighting will be created for the active object: {object_name}",
        'icon': 'INFO'
    }
}

def report_error(operator, error_type, context_info=None):
    """
    Report an error with consistent formatting and helpful details.
    
    Args:
        operator: Blender operator instance (has .report method)
        error_type: Key from ERROR_MESSAGES
        context_info: Optional dict with additional context
    """
    if error_type not in ERROR_MESSAGES:
        operator.report({'ERROR'}, f"Unknown error: {error_type}")
        return
    
    error_info = ERROR_MESSAGES[error_type]
    message = error_info['message']
    details = error_info['details']
    
    # Add context-specific information
    if context_info:
        if 'object_type' in context_info:
            details = details.format(object_type=context_info['object_type'])
        elif 'object_name' in context_info:
            details = details.format(object_name=context_info['object_name'])
    
    # Report to user
    operator.report({'ERROR'}, f"{message}: {details}")
    
    # Also print to console for debugging
    print(f"COPILOT ERROR: {message}")
    print(f"DETAILS: {details}")
    if context_info:
        print(f"CONTEXT: {context_info}")

def report_success(operator, success_type, context_info=None):
    """
    Report a successful operation with helpful follow-up information.
    
    Args:
        operator: Blender operator instance
        success_type: Key from SUCCESS_MESSAGES  
        context_info: Optional dict with additional context
    """
    if success_type not in SUCCESS_MESSAGES:
        operator.report({'INFO'}, "Operation completed")
        return
    
    success_info = SUCCESS_MESSAGES[success_type]
    message = success_info['message']
    details = success_info['details']
    
    # Add context-specific information
    if context_info:
        if 'object_name' in context_info:
            message = f"{message} for '{context_info['object_name']}'"
    
    # Report to user
    operator.report({'INFO'}, f"{message}. {details}")
    
    # Print to console
    print(f"COPILOT SUCCESS: {message}")

def report_info(operator, info_type, context_info=None):
    """
    Report informational message to user.
    
    Args:
        operator: Blender operator instance
        info_type: Key from INFO_MESSAGES
        context_info: Optional dict with additional context
    """
    if info_type not in INFO_MESSAGES:
        return
    
    info = INFO_MESSAGES[info_type]
    message = info['message']
    details = info['details']
    
    if context_info and 'object_name' in context_info:
        details = details.format(object_name=context_info['object_name'])
    
    operator.report({'INFO'}, f"{message}: {details}")

def get_context_error_message(context):
    """
    Analyze context and return appropriate error message.
    
    Args:
        context: Blender context
        
    Returns:
        tuple: (error_type, context_info) or (None, None) if valid
    """
    active_obj = context.active_object
    
    # Check for object selection
    if not active_obj:
        return 'NO_SELECTION', None
    
    # Check mode
    if context.mode != 'OBJECT':
        return 'INVALID_MODE', {'current_mode': context.mode}
    
    # Check object type
    valid_types = {'MESH', 'CURVE', 'SURFACE', 'META', 'FONT'}
    if active_obj.type not in valid_types:
        return 'INVALID_OBJECT_TYPE', {'object_type': active_obj.type}
    
    return None, None

def format_object_info(obj):
    """
    Format object information for user messages.
    
    Args:
        obj: Blender object
        
    Returns:
        str: Formatted object description
    """
    if not obj:
        return "No object"
    
    return f"{obj.name} ({obj.type.lower()})"

def create_help_text():
    """
    Create help text for the operator.
    
    Returns:
        str: Multi-line help text
    """
    help_lines = [
        "Three-Point Lighting Setup Help:",
        "",
        "Requirements:",
        "• Select a mesh, curve, surface, metaball, or text object",
        "• Be in Object Mode (Tab key)",
        "",
        "The operator will create:",
        "• Key light (main illumination)",
        "• Fill light (shadow softening)", 
        "• Rim light (edge definition)",
        "• Target empty (for light aiming)",
        "• Collection (for organization)",
        "",
        "Tips:",
        "• Use F9 after execution to adjust settings",
        "• All components can be edited manually after creation",
        "• Use Ctrl+Z to undo if needed"
    ]
    
    return "\n".join(help_lines)

class UserFeedbackManager:
    """Centralized manager for user feedback and messages"""
    
    def __init__(self, operator):
        self.operator = operator
        self.messages = []
    
    def add_error(self, error_type, context_info=None):
        """Add an error message"""
        report_error(self.operator, error_type, context_info)
        self.messages.append(('ERROR', error_type, context_info))
    
    def add_success(self, success_type, context_info=None):
        """Add a success message"""
        report_success(self.operator, success_type, context_info)
        self.messages.append(('SUCCESS', success_type, context_info))
    
    def add_info(self, info_type, context_info=None):
        """Add an info message"""
        report_info(self.operator, info_type, context_info)
        self.messages.append(('INFO', info_type, context_info))
    
    def has_errors(self):
        """Check if any errors were reported"""
        return any(msg[0] == 'ERROR' for msg in self.messages)
    
    def get_summary(self):
        """Get a summary of all messages"""
        return self.messages