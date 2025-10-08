# Data Model: Automated Three-Point Lighting Setup

## Core Entities

### LightingRig
**Purpose**: Represents a complete three-point lighting setup as a cohesive unit
**Attributes**:
- `target_object`: Reference to the Blender object being lit
- `key_light`: Reference to the key light object
- `fill_light`: Reference to the fill light object  
- `rim_light`: Reference to the rim light object
- `target_empty`: Reference to the empty object used as constraint target
- `collection`: Reference to the Blender collection containing all components
- `created_timestamp`: When the rig was created

**Relationships**:
- Contains exactly three LightConfiguration entities
- Associated with one TargetObject
- Owns one BlenderCollection

### LightConfiguration
**Purpose**: Defines the properties and positioning for each light in the rig
**Attributes**:
- `light_type`: Enum ('KEY', 'FILL', 'RIM')
- `blender_object`: Reference to the actual Blender light object
- `power_watts`: Light intensity in watts
- `color_temperature`: Color temperature in Kelvin  
- `size`: Light source size (for area lights)
- `horizontal_angle`: Position angle around target (degrees)
- `vertical_angle`: Elevation angle above target (degrees)
- `distance_multiplier`: Distance as multiple of object radius

**Relationships**:
- Belongs to one LightingRig
- References one Blender Light data block
- Has one TrackToConstraint

### TargetObject  
**Purpose**: Represents the Blender object that the lighting rig focuses on
**Attributes**:
- `blender_object`: Reference to the selected Blender object
- `center_location`: World space center coordinates (x, y, z)
- `bounding_radius`: Radius of bounding sphere for distance calculations
- `object_type`: Type of Blender object (MESH, CURVE, etc.)

**Relationships**:
- Target of one LightingRig
- Referenced by multiple TrackToConstraint entities

### TrackToConstraint
**Purpose**: Represents the Blender constraint that makes lights point at the target
**Attributes**:
- `blender_constraint`: Reference to Blender constraint object
- `track_axis`: Which axis points toward target (default: TRACK_NEGATIVE_Z)
- `up_axis`: Which axis points up (default: UP_Y)
- `target_object`: Reference to the empty object being tracked

**Relationships**:
- Applied to one LightConfiguration
- Points to one TargetObject (via empty)

### BlenderCollection
**Purpose**: Organizational container for all lighting rig components  
**Attributes**:
- `blender_collection`: Reference to Blender collection object
- `name`: Collection name (e.g., "Lighting Rig", "Lighting Rig.001")
- `is_visible`: Collection visibility state
- `is_selectable`: Collection selectability state

**Relationships**:
- Contains multiple Blender objects (lights + empty)
- Belongs to one LightingRig

## Default Value Configurations

### Standard Light Configurations
```python
LIGHT_DEFAULTS = {
    'KEY': {
        'power_watts': 100,
        'color_temperature': 5600,  # Daylight
        'size': 1.0,
        'horizontal_angle': 45,     # degrees
        'vertical_angle': 30,       # degrees  
        'distance_multiplier': 2.0
    },
    'FILL': {
        'power_watts': 40,
        'color_temperature': 5600,  # Daylight
        'size': 1.5,
        'horizontal_angle': -45,    # degrees
        'vertical_angle': 15,       # degrees
        'distance_multiplier': 1.8
    },
    'RIM': {
        'power_watts': 80,
        'color_temperature': 7000,  # Cooler
        'size': 0.8,
        'horizontal_angle': 135,    # degrees
        'vertical_angle': 45,       # degrees
        'distance_multiplier': 2.2
    }
}
```

## State Transitions

### Lighting Rig Creation Flow
1. **Validation State**: Check for valid target object selection
2. **Preparation State**: Calculate target object properties (center, radius)
3. **Creation State**: Create lights, empty, and collection
4. **Positioning State**: Position lights according to configuration
5. **Constraint State**: Apply Track To constraints
6. **Organization State**: Add all objects to collection
7. **Completion State**: Report success to user

### Error States
- **No Selection Error**: No active object in Blender context
- **Invalid Object Error**: Active object is not suitable for lighting (e.g., light, camera)
- **Name Collision Error**: Required names already exist in scene
- **Creation Failure Error**: Blender API calls fail during creation

## Data Validation Rules

### Target Object Validation
- Must be a valid Blender object
- Must have a bounding box (eliminates some object types)
- Must be visible and selectable
- Must not be a light or camera object

### Collection Name Validation  
- Must be unique in scene
- Follow Blender naming conventions
- Automatically append .001, .002 etc. for conflicts

### Light Property Validation
- Power values must be > 0
- Color temperature must be in range 1000-12000K
- Size values must be > 0
- Angles must be in valid degree ranges (-180 to 180)

## Memory and Performance Considerations

### Object References
- Store weak references to Blender objects to avoid circular dependencies
- Validate object existence before access (objects can be deleted)
- Use Blender's built-in object ID system for persistence

### Calculation Optimization
- Cache bounding radius calculation (expensive operation)
- Pre-calculate trigonometric values for positioning
- Batch object creation to minimize scene updates

### Cleanup Procedures
- Automatic cleanup on operator failure
- Proper constraint removal if lighting rig is deleted
- Collection cleanup when all contained objects are removed