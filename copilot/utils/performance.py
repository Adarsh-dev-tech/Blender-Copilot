import time
import bpy
import mathutils

def optimize_bounding_box_calculation(obj):
    """
    Optimized bounding box calculation for better performance.
    
    Args:
        obj: Blender object
        
    Returns:
        dict: Optimized bounding box information
    """
    if not obj or not hasattr(obj, 'bound_box'):
        return None
    
    # Use matrix multiplication for faster coordinate transformation
    matrix = obj.matrix_world
    
    # Pre-calculate bound box corners in world space
    local_corners = obj.bound_box
    world_corners = [matrix @ mathutils.Vector(corner) for corner in local_corners]
    
    # Use numpy-style vectorized operations where possible
    xs = [corner.x for corner in world_corners]
    ys = [corner.y for corner in world_corners]
    zs = [corner.z for corner in world_corners]
    
    min_coords = mathutils.Vector((min(xs), min(ys), min(zs)))
    max_coords = mathutils.Vector((max(xs), max(ys), max(zs)))
    
    # Calculate center more efficiently
    center = (min_coords + max_coords) * 0.5
    
    # Calculate radius using the maximum extent
    dimensions = max_coords - min_coords
    radius = max(dimensions) * 0.5
    
    return {
        'center': center,
        'dimensions': dimensions,
        'radius': radius,
        'min_coords': min_coords,
        'max_coords': max_coords
    }

def batch_object_creation(object_specs):
    """
    Create multiple objects in a batch for better performance.
    
    Args:
        object_specs: List of object specification dictionaries
        
    Returns:
        list: Created objects
    """
    created_objects = []
    
    # Disable viewport updates during batch creation
    original_update = bpy.context.scene.frame_set
    
    try:
        # Batch create objects
        for spec in object_specs:
            if spec['type'] == 'LIGHT':
                obj = _create_light_optimized(spec)
            elif spec['type'] == 'EMPTY':
                obj = _create_empty_optimized(spec)
            else:
                continue
            
            created_objects.append(obj)
        
        # Update scene once after all objects are created
        bpy.context.view_layer.update()
        
    except Exception as e:
        print(f"Error in batch object creation: {e}")
    
    return created_objects

def _create_light_optimized(spec):
    """Optimized light creation"""
    light_data = bpy.data.lights.new(name=spec['name'], type='AREA')
    light_data.energy = spec.get('power', 100)
    light_data.size = spec.get('size', 1.0)
    
    light_object = bpy.data.objects.new(spec['name'], light_data)
    light_object.location = spec.get('location', (0, 0, 0))
    
    return light_object

def _create_empty_optimized(spec):
    """Optimized empty creation"""
    empty = bpy.data.objects.new(spec['name'], None)
    empty.location = spec.get('location', (0, 0, 0))
    empty.empty_display_type = 'SPHERE'
    empty.empty_display_size = 0.5
    
    return empty

def measure_execution_time(func):
    """
    Decorator to measure execution time of functions.
    
    Args:
        func: Function to measure
        
    Returns:
        Decorated function
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        print(f"{func.__name__} executed in {execution_time:.4f} seconds")
        
        # Warn if execution is too slow
        if execution_time > 1.0:
            print(f"WARNING: {func.__name__} exceeded 1 second execution time")
        
        return result
    
    return wrapper

def optimize_constraint_application(lights, target):
    """
    Apply constraints to multiple lights efficiently.
    
    Args:
        lights: List of light objects
        target: Target object for constraints
    """
    # Batch constraint creation
    for light in lights:
        constraint = light.constraints.new(type='TRACK_TO')
        constraint.target = target
        constraint.track_axis = 'TRACK_NEGATIVE_Z'
        constraint.up_axis = 'UP_Y'
    
    # Update constraints in batch
    bpy.context.view_layer.update()

class PerformanceMonitor:
    """Monitor performance metrics during lighting operations"""
    
    def __init__(self):
        self.start_time = None
        self.checkpoints = []
    
    def start(self):
        """Start performance monitoring"""
        self.start_time = time.time()
        self.checkpoints = []
    
    def checkpoint(self, name):
        """Add a performance checkpoint"""
        if self.start_time is None:
            return
        
        current_time = time.time()
        elapsed = current_time - self.start_time
        self.checkpoints.append((name, elapsed))
    
    def report(self):
        """Report performance metrics"""
        if not self.checkpoints:
            return
        
        print("Performance Report:")
        for name, elapsed in self.checkpoints:
            print(f"  {name}: {elapsed:.4f}s")
        
        total_time = self.checkpoints[-1][1]
        if total_time > 1.0:
            print(f"WARNING: Total execution time {total_time:.4f}s exceeds target")
    
    def meets_performance_target(self, target_seconds=1.0):
        """Check if performance meets target"""
        if not self.checkpoints:
            return True
        
        total_time = self.checkpoints[-1][1]
        return total_time <= target_seconds

# Memory optimization utilities
def clear_unused_data():
    """Clear unused data blocks to free memory"""
    # Clear unused meshes
    for mesh in bpy.data.meshes:
        if mesh.users == 0:
            bpy.data.meshes.remove(mesh)
    
    # Clear unused materials  
    for material in bpy.data.materials:
        if material.users == 0:
            bpy.data.materials.remove(material)
    
    # Clear unused lights
    for light in bpy.data.lights:
        if light.users == 0:
            bpy.data.lights.remove(light)