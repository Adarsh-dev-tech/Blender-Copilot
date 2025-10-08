# Operator Contract: Three-Point Lighting Setup

## LightingRigOperator Contract

### Operator Identification
- **ID**: `copilot.create_three_point_lighting`
- **Label**: "Create Three-Point Lighting"
- **Description**: "Creates a professional three-point lighting setup for the selected object"
- **Class**: `COPILOT_OT_create_three_point_lighting`

### Input Contract

#### Required Context
```python
# Blender context requirements
bpy.context.active_object: bpy.types.Object  # Must exist and be valid
bpy.context.mode: str                         # Must be 'OBJECT' mode
bpy.context.scene: bpy.types.Scene           # Valid scene context
```

#### Operator Properties  
```python
class COPILOT_OT_create_three_point_lighting(bpy.types.Operator):
    # Optional overrides for default positioning
    key_angle: bpy.props.FloatProperty(
        name="Key Light Angle",
        default=45.0,
        min=-180.0,
        max=180.0,
        description="Horizontal angle for key light"
    )
    
    fill_angle: bpy.props.FloatProperty(
        name="Fill Light Angle", 
        default=-45.0,
        min=-180.0,
        max=180.0,
        description="Horizontal angle for fill light"
    )
    
    rim_angle: bpy.props.FloatProperty(
        name="Rim Light Angle",
        default=135.0, 
        min=-180.0,
        max=180.0,
        description="Horizontal angle for rim light"
    )
    
    distance_scale: bpy.props.FloatProperty(
        name="Distance Scale",
        default=1.0,
        min=0.1,
        max=10.0,
        description="Scale factor for light distances"
    )
```

### Output Contract

#### Success Condition
When operator completes successfully, the following objects must exist in the scene:

```python
# Created objects with predictable names
created_objects = {
    'key_light': "Key Light" | "Key Light.001" | "Key Light.XXX",
    'fill_light': "Fill Light" | "Fill Light.001" | "Fill Light.XXX", 
    'rim_light': "Rim Light" | "Rim Light.001" | "Rim Light.XXX",
    'target_empty': "Lighting Target" | "Lighting Target.001" | "Lighting Target.XXX",
    'collection': "Lighting Rig" | "Lighting Rig.001" | "Lighting Rig.XXX"
}

# Object properties verification
for light_name in ['Key Light', 'Fill Light', 'Rim Light']:
    light_obj = bpy.data.objects[light_name]
    assert light_obj.type == 'LIGHT'
    assert light_obj.data.type == 'AREA'
    assert len(light_obj.constraints) == 1
    assert light_obj.constraints[0].type == 'TRACK_TO'
    assert light_obj.constraints[0].target is not None

target_empty = bpy.data.objects["Lighting Target"]
assert target_empty.type == 'EMPTY'
assert target_empty.location == target_object.matrix_world.translation

collection = bpy.data.collections["Lighting Rig"] 
assert len(collection.objects) == 4  # 3 lights + 1 empty
```

#### Error Conditions
```python
# Error return values
OPERATOR_RETURN_VALUES = {
    'FINISHED': "Operation completed successfully",
    'CANCELLED': "User cancelled operation", 
    'RUNNING_MODAL': "Should not occur for this operator",
    'PASS_THROUGH': "Should not occur for this operator"
}

# Error reporting through self.report()
ERROR_MESSAGES = {
    'NO_ACTIVE_OBJECT': "No object selected. Please select an object to light.",
    'INVALID_OBJECT_TYPE': "Selected object cannot be lit. Please select a mesh object.",
    'OBJECT_MODE_REQUIRED': "Must be in Object mode to create lighting.",
    'CREATION_FAILED': "Failed to create lighting components. Check console for details."
}
```

### Side Effects Contract

#### Scene Modifications
```python
# Guaranteed scene changes on success
scene_changes = {
    'new_objects': 4,           # 3 lights + 1 empty
    'new_collections': 1,       # Lighting Rig collection
    'new_constraints': 3,       # 1 Track To per light
    'modified_collections': 1   # Scene collection gets new child
}

# Undo/Redo compatibility  
# All changes must be reversible through single undo operation
assert bpy.ops.ed.undo.poll() == True  # Undo must be available
```

#### Performance Contract
```python
# Performance requirements
execution_time_max = 1.0  # seconds
memory_overhead_max = 1   # MB
scene_updates_max = 10    # viewport updates
```

### Integration Contract

#### Panel Integration
```python
# UI Panel requirements
class COPILOT_PT_lighting_panel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Copilot'
    bl_label = "Lighting Tools"
    
    def draw(self, context):
        layout = self.layout
        layout.operator("copilot.create_three_point_lighting")
```

#### Command Integration  
```python
# Natural language command mapping (handled by parent system)
COMMAND_PATTERNS = [
    "create three point lighting",
    "create 3 point lighting", 
    "light the selected object",
    "set up lighting",
    "add lighting rig"
]
```

### Testing Contract

#### Unit Test Requirements
```python
# Minimum test coverage
test_cases = {
    'test_operator_registration': "Operator can be registered/unregistered",
    'test_valid_execution': "Executes successfully with valid input",
    'test_no_selection_error': "Reports error when no object selected", 
    'test_invalid_object_error': "Reports error for invalid object types",
    'test_mode_requirements': "Requires OBJECT mode",
    'test_naming_conflicts': "Handles existing name conflicts",
    'test_undo_compatibility': "Changes are undoable",
    'test_performance_limits': "Completes within time/memory limits"
}
```

#### Integration Test Requirements  
```python
# Blender environment tests
integration_tests = {
    'test_with_simple_cube': "Works with default cube",
    'test_with_complex_mesh': "Works with high-poly objects",
    'test_with_scaled_objects': "Works with scaled/rotated objects", 
    'test_multiple_executions': "Can create multiple rigs",
    'test_scene_persistence': "Rig survives save/reload",
    'test_constraint_behavior': "Lights track target correctly"
}
```

### Compatibility Contract

#### Blender Version Support
- **Minimum**: Blender 3.0 LTS
- **Tested**: Blender 3.6, 4.0
- **Python**: 3.10+ (embedded in Blender)

#### API Dependencies
```python
# Required Blender API modules
required_modules = [
    'bpy.data',      # Data access
    'bpy.context',   # Context access  
    'bpy.ops',       # Built-in operators
    'bpy.types',     # Type definitions
    'mathutils'      # Math utilities
]

# No external dependencies allowed
external_dependencies = []  # Must remain empty
```