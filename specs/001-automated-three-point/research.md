# Research: Automated Three-Point Lighting Setup

## Research Tasks

### 1. Blender Python API for Light Creation and Manipulation

**Decision**: Use `bpy.data.lights.new()` and `bpy.data.objects.new()` for light creation
**Rationale**: This is the standard Blender API pattern for creating new data blocks and linking them to the scene
**Alternatives considered**: 
- `bpy.ops.mesh.primitive_*_add()` - Rejected as it's for mesh primitives, not lights
- Direct manipulation of `bpy.context.scene.objects` - Rejected as it doesn't properly create data blocks

**Key API Methods**:
- `bpy.data.lights.new(name, type='AREA')` - Create light data block
- `bpy.data.objects.new(name, object_data)` - Create object wrapper
- `bpy.context.collection.objects.link(obj)` - Add to scene
- `obj.location = (x, y, z)` - Position lights
- `obj.rotation_euler = (x, y, z)` - Orient lights

### 2. Object Selection and Context Awareness

**Decision**: Use `bpy.context.active_object` for target object identification
**Rationale**: Follows Blender's standard pattern where the active object is the primary focus for operations
**Alternatives considered**:
- `bpy.context.selected_objects[0]` - Rejected as it doesn't guarantee consistent behavior with multiple selections
- User input for object selection - Rejected as it breaks the seamless workflow principle

**Key API Methods**:
- `bpy.context.active_object` - Get the current active object
- `obj.bound_box` - Get object bounding box for size calculations
- `obj.matrix_world` - Get object world transformation matrix

### 3. Track To Constraints Implementation

**Decision**: Use `obj.constraints.new(type='TRACK_TO')` for automatic light aiming
**Rationale**: Track To constraints are the standard Blender mechanism for making objects point at targets
**Alternatives considered**:
- Manual rotation calculations - Rejected as it's more complex and less maintainable
- Look At constraints - Rejected as Track To is more appropriate for lights

**Key API Methods**:
- `constraint = obj.constraints.new(type='TRACK_TO')`
- `constraint.target = target_object`
- `constraint.track_axis = 'TRACK_NEGATIVE_Z'` - Standard for lights
- `constraint.up_axis = 'UP_Y'` - Standard up direction

### 4. Three-Point Lighting Mathematical Positioning

**Decision**: Use spherical coordinates with standard cinema lighting angles
**Rationale**: Professional three-point lighting follows established conventions that translate well to 3D space
**Alternatives considered**:
- Random positioning - Rejected as it wouldn't produce professional results
- User-defined positions - Rejected as it defeats the automation purpose

**Standard Positions** (relative to object center):
- **Key Light**: 45° horizontal, 30° vertical, distance = 2 * object_radius
- **Fill Light**: -45° horizontal, 15° vertical, distance = 1.8 * object_radius  
- **Rim Light**: 135° horizontal, 45° vertical, distance = 2.2 * object_radius

**Calculation Method**:
```python
import math
# Convert spherical to cartesian coordinates
x = distance * math.cos(vertical_angle) * math.cos(horizontal_angle)
y = distance * math.cos(vertical_angle) * math.sin(horizontal_angle)
z = distance * math.sin(vertical_angle)
```

### 5. Collection Organization and Scene Management

**Decision**: Create a new collection named "Lighting Rig" for organization
**Rationale**: Collections are Blender's standard way to organize related objects
**Alternatives considered**:
- No organization - Rejected as it clutters the outliner
- Parenting to the target object - Rejected as it complicates the relationship

**Key API Methods**:
- `bpy.data.collections.new(name)` - Create new collection
- `bpy.context.scene.collection.children.link(collection)` - Add to scene
- `collection.objects.link(obj)` - Add objects to collection

### 6. Error Handling and User Feedback

**Decision**: Use `self.report()` method in operators for user feedback
**Rationale**: This is Blender's standard way to provide user feedback in operators
**Alternatives considered**:
- Print statements - Rejected as they don't reach the user
- Popup dialogs - Rejected as they're too intrusive

**Key Patterns**:
- `self.report({'ERROR'}, "No object selected")` - Error messages
- `self.report({'INFO'}, "Lighting rig created")` - Success messages

### 7. Default Light Properties

**Decision**: Use cinema-standard power and color values
**Rationale**: Professional lighting follows established conventions for color temperature and intensity
**Alternatives considered**:
- Blender default values - Rejected as they're not optimized for three-point lighting
- User-configurable defaults - Deferred to future enhancement

**Default Values**:
- **Key Light**: Power=100W, Color=5600K (daylight), Size=1.0
- **Fill Light**: Power=40W, Color=5600K (daylight), Size=1.5  
- **Rim Light**: Power=80W, Color=7000K (cooler), Size=0.8

## Technology Stack Validation

**Confirmed Technologies**:
- Python 3.10+ (Blender embedded)
- Blender Python API (`bpy`) 
- `mathutils` for 3D calculations
- `unittest` for testing framework
- Blender add-on architecture

**Performance Considerations**:
- All operations are O(1) complexity
- No dependency on external libraries
- Scene modification through standard Blender undo system
- Memory usage minimal (3 lights + 1 empty + 1 collection)

## Integration Points

**Natural Language Processing**: Deferred to parent Copilot system - this operator will be triggered by the command parser
**UI Integration**: Standard Blender panel with operator buttons
**Script Generation**: Operations will be logged to Blender's info panel automatically
**Undo/Redo**: Automatic through Blender's standard operator system