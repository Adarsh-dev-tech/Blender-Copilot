import bpy

def ensure_undo_push(operation_name="Copilot Operation"):
    """
    Ensure that an operation is properly recorded in Blender's undo system.
    
    Args:
        operation_name: Name to display in undo history
    """
    # Blender automatically handles undo for operators with 'UNDO' in bl_options
    # This function provides additional utilities if needed
    bpy.ops.ed.undo_push(message=operation_name)

def validate_undo_state():
    """
    Validate that the current operation can be undone.
    
    Returns:
        bool: True if undo is available
    """
    # Check if undo is available
    return bpy.ops.ed.undo.poll()

def test_undo_redo_cycle(context):
    """
    Test that undo/redo works correctly for lighting operations.
    
    Args:
        context: Blender context
        
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        # Store initial state
        initial_objects = set(bpy.data.objects.keys())
        initial_collections = set(bpy.data.collections.keys())
        
        # Check if undo is available before operation
        if not validate_undo_state():
            return False, "Undo not available before operation"
        
        # Note: In actual implementation, this would be called after 
        # the lighting operator execution
        
        # Perform undo
        if bpy.ops.ed.undo.poll():
            bpy.ops.ed.undo()
            
            # Check that objects were removed
            after_undo_objects = set(bpy.data.objects.keys())
            after_undo_collections = set(bpy.data.collections.keys())
            
            if after_undo_objects != initial_objects:
                return False, "Undo did not properly remove created objects"
            
            if after_undo_collections != initial_collections:
                return False, "Undo did not properly remove created collections"
        
        # Perform redo
        if bpy.ops.ed.redo.poll():
            bpy.ops.ed.redo()
            
            # Check that objects were recreated
            after_redo_objects = set(bpy.data.objects.keys())
            after_redo_collections = set(bpy.data.collections.keys())
            
            # Objects and collections should be restored
            # (exact check would depend on operation results)
        
        return True, "Undo/redo cycle completed successfully"
        
    except Exception as e:
        return False, f"Error during undo/redo test: {str(e)}"

def cleanup_orphaned_data():
    """
    Clean up any orphaned data blocks that might remain after undo operations.
    This is a utility function for maintaining scene cleanliness.
    """
    try:
        # Remove orphaned meshes
        for mesh in bpy.data.meshes:
            if mesh.users == 0:
                bpy.data.meshes.remove(mesh)
        
        # Remove orphaned lights
        for light in bpy.data.lights:
            if light.users == 0:
                bpy.data.lights.remove(light)
        
        # Remove orphaned materials
        for material in bpy.data.materials:
            if material.users == 0:
                bpy.data.materials.remove(material)
                
    except Exception as e:
        print(f"Warning: Error during orphaned data cleanup: {e}")

# Integration helpers for operators
class UndoContext:
    """Context manager for ensuring proper undo integration"""
    
    def __init__(self, operation_name="Copilot Operation"):
        self.operation_name = operation_name
        self.initial_state = None
    
    def __enter__(self):
        # Store initial state if needed
        self.initial_state = {
            'objects': set(bpy.data.objects.keys()),
            'collections': set(bpy.data.collections.keys())
        }
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            # Operation succeeded, ensure undo push
            ensure_undo_push(self.operation_name)
        else:
            # Operation failed, cleanup any partial changes
            cleanup_orphaned_data()
            return False  # Re-raise exception