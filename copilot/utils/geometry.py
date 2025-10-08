import math
import mathutils

def spherical_to_cartesian(radius, horizontal_angle_deg, vertical_angle_deg):
    """
    Convert spherical coordinates to cartesian coordinates.
    
    Args:
        radius: Distance from origin
        horizontal_angle_deg: Horizontal angle in degrees (0 = +Y axis)
        vertical_angle_deg: Vertical angle in degrees (0 = XY plane, 90 = +Z axis)
    
    Returns:
        tuple: (x, y, z) cartesian coordinates
    """
    # Convert degrees to radians
    h_rad = math.radians(horizontal_angle_deg)
    v_rad = math.radians(vertical_angle_deg)
    
    # Spherical to cartesian conversion
    x = radius * math.cos(v_rad) * math.sin(h_rad)
    y = radius * math.cos(v_rad) * math.cos(h_rad)
    z = radius * math.sin(v_rad)
    
    return (x, y, z)

def analyze_bounding_box(obj):
    """
    Analyze object's bounding box and calculate useful properties.
    
    Args:
        obj: Blender object
    
    Returns:
        dict: Contains center, dimensions, radius, and corners
    """
    if not obj or not hasattr(obj, 'bound_box'):
        return None
    
    # Get bounding box corners in local space
    bbox_corners = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
    
    # Calculate center point
    center = mathutils.Vector((0, 0, 0))
    for corner in bbox_corners:
        center += corner
    center /= len(bbox_corners)
    
    # Calculate dimensions
    min_coords = mathutils.Vector((
        min(corner.x for corner in bbox_corners),
        min(corner.y for corner in bbox_corners),
        min(corner.z for corner in bbox_corners)
    ))
    max_coords = mathutils.Vector((
        max(corner.x for corner in bbox_corners),
        max(corner.y for corner in bbox_corners),
        max(corner.z for corner in bbox_corners)
    ))
    
    dimensions = max_coords - min_coords
    
    # Calculate bounding sphere radius (maximum distance from center to any corner)
    radius = max((corner - center).length for corner in bbox_corners)
    
    return {
        'center': center,
        'dimensions': dimensions,
        'radius': radius,
        'min_coords': min_coords,
        'max_coords': max_coords,
        'corners': bbox_corners
    }

def calculate_distance(point1, point2):
    """
    Calculate Euclidean distance between two 3D points.
    
    Args:
        point1: tuple or Vector (x, y, z)
        point2: tuple or Vector (x, y, z)
    
    Returns:
        float: Distance between points
    """
    if isinstance(point1, (tuple, list)):
        point1 = mathutils.Vector(point1)
    if isinstance(point2, (tuple, list)):
        point2 = mathutils.Vector(point2)
    
    return (point1 - point2).length

def calculate_light_position(target_center, horizontal_angle, vertical_angle, distance):
    """
    Calculate world position for a light based on target and angles.
    
    Args:
        target_center: Vector or tuple representing target object center
        horizontal_angle: Horizontal angle in degrees
        vertical_angle: Vertical angle in degrees  
        distance: Distance from target
    
    Returns:
        Vector: World position for the light
    """
    if isinstance(target_center, (tuple, list)):
        target_center = mathutils.Vector(target_center)
    
    # Get relative position using spherical coordinates
    rel_pos = spherical_to_cartesian(distance, horizontal_angle, vertical_angle)
    
    # Add to target center to get world position
    world_pos = target_center + mathutils.Vector(rel_pos)
    
    return world_pos