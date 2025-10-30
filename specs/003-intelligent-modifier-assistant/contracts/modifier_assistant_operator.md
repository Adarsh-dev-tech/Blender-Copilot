# Operator Contract: Modifier Assistant

**Operator ID**: `copilot.modifier_assistant`  
**Feature**: Intelligent Modifier Assistant  
**Date**: 2025-10-30  
**Status**: Contract Definition (Phase 1)

## Overview
This contract defines the interface, behavior, and guarantees for the Modifier Assistant operator. This is the main orchestration operator that coordinates command parsing, context validation, and workflow execution.

---

## Operator Interface

### Blender Registration
```python
bl_idname = "copilot.modifier_assistant"
bl_label = "Execute Modifier Command"
bl_description = "Parse and execute intelligent modifier workflow"
bl_options = {'REGISTER', 'UNDO'}
```

### Properties
```python
command_text: StringProperty(
    name="Command",
    description="Natural language command (e.g., 'make hard-surface')",
    default=""
)
```

---

## Input Contract

### Preconditions
1. **Blender Context Available**:
   - `bpy.context` must be accessible
   - `bpy.context.scene` must exist
   - `bpy.context.view_layer` must exist

2. **Command Text**:
   - `command_text` property must be set (via scene property or operator property)
   - Length must be >= 3 characters
   - Cannot be empty or whitespace-only

3. **Scene State**:
   - Scene must not be in restricted context (e.g., during render)
   - Objects must be accessible for modification

### Input Validation
| Check | Validation | Error If Failed |
|-------|------------|-----------------|
| Command exists | `len(command_text.strip()) >= 3` | "Please enter a command" |
| Context valid | `bpy.context is not None` | "Invalid Blender context" |
| Scene accessible | `bpy.context.scene is not None` | "No active scene" |

---

## Processing Contract

### Execution Flow
```
1. PARSE COMMAND
   Input: command_text
   Output: workflow_type (enum) or UNKNOWN
   Duration: < 10ms

2. VALIDATE CONTEXT
   Input: bpy.context, workflow_type
   Output: ValidationResult (is_valid, error_message)
   Duration: < 20ms

3. IF VALIDATION FAILS
   → Report error to user (ERROR level)
   → Return {'CANCELLED'}
   → STOP

4. EXECUTE WORKFLOW
   Input: workflow_type, selected_objects, active_object
   Output: ExecutionResult (status, message, modifiers_added)
   Duration: < 300ms (varies by workflow)

5. REPORT RESULT
   → If SUCCESS: Report with INFO level
   → If ERROR: Report with ERROR level
   → Return operator status

Total Duration: < 350ms for all workflows
```

### Parsing Phase Contract

**Function**: `parse_command(command_text: str) -> str`

**Input**:
- `command_text`: User's natural language command

**Output**:
- Workflow type enum value: `'SMART_ARRAY'`, `'HARD_SURFACE'`, `'SYMMETRIZE'`, `'CURVE_DEFORM'`, `'SOLIDIFY'`, `'SHRINKWRAP'`, or `'UNKNOWN'`

**Behavior**:
- Must check command against pattern dictionary
- Case-insensitive matching
- Returns first matching workflow (priority order matters)
- Returns `'UNKNOWN'` if no patterns match

**Performance**: < 10ms

**Examples**:
```python
parse_command("create an array") → 'SMART_ARRAY'
parse_command("Make this hard-surface") → 'HARD_SURFACE'
parse_command("mirror on X") → 'SYMMETRIZE'
parse_command("xyz random text") → 'UNKNOWN'
```

---

### Validation Phase Contract

**Function**: `validate_context(workflow_type: str) -> tuple[bool, str]`

**Input**:
- `workflow_type`: The parsed workflow identifier
- Implicit: `bpy.context` (current selection state)

**Output**:
- Tuple of `(is_valid: bool, error_message: str)`
- If valid: `(True, "")`
- If invalid: `(False, "Specific error message")`

**Validation Rules by Workflow**:

| Workflow | Selection Check | Type Check | Mode Check |
|----------|----------------|------------|------------|
| SMART_ARRAY | 1 or 2 objects | 1 MESH or 1 MESH + 1 EMPTY | OBJECT |
| HARD_SURFACE | 1 object | 1 MESH | OBJECT |
| SYMMETRIZE | 1 object | 1 MESH | OBJECT |
| CURVE_DEFORM | 2 objects | 1 MESH + 1 CURVE | OBJECT |
| SOLIDIFY | 1 object | 1 MESH | OBJECT |
| SHRINKWRAP | 2 objects | 2 MESH | OBJECT |

**Error Messages** (must match exactly):
- No selection: `"Please select an object first"`
- Wrong count: `"This command requires {N} selected object(s), but {M} are selected"`
- Wrong types: `"This command requires {specific type description}"`
  - Example: `"This command requires two selected objects: a mesh and a curve"`
- Wrong mode: `"This command must be run in Object Mode (currently in {current_mode})"`

**Performance**: < 20ms

---

### Execution Phase Contract

**Function**: `execute_workflow(workflow_type: str) -> tuple[set, str]`

**Input**:
- `workflow_type`: Validated workflow identifier
- Implicit: `bpy.context.selected_objects`, `bpy.context.active_object`

**Output**:
- Tuple of `(status: set, message: str)`
- Status: `{'FINISHED'}` or `{'CANCELLED'}`
- Message: User-facing feedback string

**Workflow Execution Contracts**:

#### 1. Smart Array (Single Object)
**Input Requirements**:
- 1 mesh object selected

**Actions**:
1. Get active object
2. Add Array modifier
3. Set count = 5
4. Set use_relative_offset = True
5. Set relative_offset_displace = (1.0, 0.0, 0.0)

**Output**:
- Status: `{'FINISHED'}`
- Message: `"Array modifier added with 5 copies on X-axis"`
- Modifiers added: `["Array"]`

**Side Effects**:
- One new modifier in active object's modifier stack
- Modifier stack order preserved

**Performance**: < 50ms

---

#### 2. Smart Array (Object Offset)
**Input Requirements**:
- 1 mesh object + 1 empty object selected

**Actions**:
1. Identify which object is mesh, which is empty
2. Add Array modifier to mesh object
3. Set use_relative_offset = False
4. Set use_object_offset = True
5. Set offset_object = empty object

**Output**:
- Status: `{'FINISHED'}`
- Message: `"Array modifier added with empty object control"`
- Modifiers added: `["Array"]`

**Side Effects**:
- One new modifier on mesh object
- Modifier references empty object (dependency created)

**Performance**: < 50ms

---

#### 3. Hard-Surface SubD
**Input Requirements**:
- 1 mesh object selected

**Actions**:
1. Get active object
2. Add Bevel modifier:
   - limit_method = 'ANGLE'
   - segments = 3
3. Add Subdivision Surface modifier AFTER Bevel:
   - levels = 2 (viewport)
4. Set object shading to Smooth

**Output**:
- Status: `{'FINISHED'}`
- Message: `"Hard-surface setup applied (Bevel + Subdivision + Smooth)"`
- Modifiers added: `["Bevel", "Subdivision Surface"]`

**Side Effects**:
- Two new modifiers in specific order
- Object shading mode changed to Smooth
- Viewport appearance immediately updated

**Performance**: < 100ms

---

#### 4. Symmetrize (Mirror)
**Input Requirements**:
- 1 mesh object selected
- Object must have editable mesh data

**Actions**:
1. Get active object
2. Apply scale transformation (`bpy.ops.object.transform_apply(scale=True)`)
3. Add Mirror modifier:
   - use_axis = (True, False, False) # X-axis
   - use_bisect_axis = (True, False, False)
   - use_clip = True
4. Enter Edit Mode (`bpy.ops.object.mode_set(mode='EDIT')`)
5. Deselect all vertices
6. Select vertices where x > 0.0 (using bmesh)
7. Delete selected vertices
8. Return to Object Mode

**Output**:
- Status: `{'FINISHED'}`
- Message: `"Symmetrize applied on X-axis (scale applied, positive X deleted)"`
- Modifiers added: `["Mirror"]`

**Side Effects**:
- Scale transformation applied (cannot be undone separately)
- Geometry modified (vertices deleted)
- One new modifier added
- Mode changes (Edit → Object)
- Entire operation is ONE undo step

**Performance**: < 200ms

**Error Conditions**:
- If scale application fails: Return `{'CANCELLED'}`, `"Failed to apply scale"`
- If no vertices to delete: Proceed anyway (valid state)

---

#### 5. Curve Deform
**Input Requirements**:
- 1 mesh object + 1 curve object selected
- Active object should be the mesh

**Actions**:
1. Identify which object is mesh, which is curve
2. Apply scale to mesh object
3. Apply scale to curve object
4. Align mesh object origin to curve object origin (set mesh.location = curve.location)
5. Add Curve modifier to mesh:
   - object = curve object

**Output**:
- Status: `{'FINISHED'}`
- Message: `"Curve deform applied (scales applied, origins aligned)"`
- Modifiers added: `["Curve"]`

**Side Effects**:
- Scale applied to both objects (cannot be undone separately)
- Mesh object origin/location changed
- One new modifier added
- Dependency created (mesh modifier references curve)

**Performance**: < 150ms

**Error Conditions**:
- If scale application fails on either object: Return `{'CANCELLED'}`, `"Failed to apply scale to {object_name}"`

---

#### 6. Solidify
**Input Requirements**:
- 1 mesh object selected

**Actions**:
1. Get active object
2. Add Solidify modifier:
   - thickness = 0.01 (meters)
   - use_even_offset = True

**Output**:
- Status: `{'FINISHED'}`
- Message: `"Solidify modifier added (thickness: 0.01m, even offset enabled)"`
- Modifiers added: `["Solidify"]`

**Side Effects**:
- One new modifier added
- Immediate viewport update (thickness visible)

**Performance**: < 50ms

---

#### 7. Shrinkwrap
**Input Requirements**:
- 2 mesh objects selected
- Must have an active object

**Actions**:
1. Get active object (source)
2. Get non-active selected object (target)
3. Add Shrinkwrap modifier to source:
   - target = target object
   - wrap_method = 'NEAREST_SURFACEPOINT'

**Output**:
- Status: `{'FINISHED'}`
- Message: `"Shrinkwrap modifier added (target: {target_name})"`
- Modifiers added: `["Shrinkwrap"]`

**Side Effects**:
- One new modifier on active object
- Modifier references target object (dependency created)
- Source geometry deforms to target surface

**Performance**: < 50ms

---

## Error Handling Contract

### Error Categories

**Category 1: Command Recognition Errors**
- **Trigger**: Parsed workflow type is `'UNKNOWN'`
- **Action**: Report error with ERROR level
- **Message**: `"Command not understood. Try: 'make array', 'hard-surface', 'mirror', 'solidify', 'curve deform', or 'shrinkwrap'"`
- **Return**: `{'CANCELLED'}`

**Category 2: Selection Validation Errors**
- **Trigger**: Selection doesn't match workflow requirements
- **Action**: Report error with ERROR level
- **Message**: Specific error from validation function
- **Return**: `{'CANCELLED'}`

**Category 3: Execution Errors**
- **Trigger**: Workflow execution fails (e.g., scale application fails)
- **Action**: Report error with ERROR level
- **Message**: Specific error describing what failed
- **Return**: `{'CANCELLED'}`
- **Side Effects**: Partial state changes MAY have occurred (user can undo)

### Error Recovery
- All errors must be non-fatal to Blender
- Operator must always return a valid status (`{'FINISHED'}` or `{'CANCELLED'}`)
- User must always see a clear error message
- Scene state must remain valid (no corrupted data)

---

## Undo/Redo Contract

### Undo Behavior
- **Operator Flag**: `bl_options = {'REGISTER', 'UNDO'}`
- **Single Undo Step**: Entire workflow (all modifiers + prerequisites) is one undo operation
- **Undo Scope**: Includes:
  - All modifier additions
  - Scale applications
  - Geometry changes (Symmetrize vertex deletion)
  - Shading changes (Hard-Surface smooth shading)
  - Mode changes are NOT undone separately (already in Object Mode after undo)

### Redo Behavior
- Redo re-executes the entire workflow
- Command text is preserved in undo history
- Selection context at redo time may differ (validation runs again)

---

## UI Integration Contract

### Operator Invocation
```python
# From Panel Button
bpy.ops.copilot.modifier_assistant()

# Command text is read from scene property:
bpy.context.scene.copilot_modifier_command
```

### User Feedback
All feedback uses Blender's `self.report()` system:

**Success Messages** (`{'INFO'}` level):
- Appear in status bar
- Auto-dismiss after 3 seconds
- Include what was done

**Error Messages** (`{'ERROR'}` level):
- Appear in status bar
- Persist until user clicks away
- Include actionable guidance

### Panel Requirements
- Panel must provide text input field bound to `bpy.context.scene.copilot_modifier_command`
- Panel must provide "Execute" button that calls `bpy.ops.copilot.modifier_assistant()`
- Panel should show current selection count for user awareness
- Panel location: 3D View sidebar, "Copilot" tab

---

## Performance Contract

### Guaranteed Maximums
| Operation | Maximum Duration |
|-----------|-----------------|
| Command parsing | 10ms |
| Context validation | 20ms |
| Simple workflows (Array, Solidify, Shrinkwrap) | 50ms |
| Complex workflows (Hard-Surface) | 100ms |
| Edit mode workflows (Symmetrize) | 200ms |
| Multi-prerequisite workflows (Curve Deform) | 150ms |
| **Total end-to-end (worst case)** | **350ms** |

### Performance Testing
- Must be tested on scenes with 100k+ vertices
- Must be tested with 10+ objects selected (for validation performance)
- Must profile BMesh operations in Symmetrize workflow
- Must measure mode switch overhead

---

## Testing Contract

### Unit Test Requirements
1. **Command Parsing Tests** (`test_command_parser.py`):
   - Test all six workflow patterns match correctly
   - Test case insensitivity
   - Test unknown commands return 'UNKNOWN'
   - Test empty/whitespace commands

2. **Context Validation Tests** (`test_context_validator.py`):
   - Test each workflow's validation rules
   - Test all error conditions
   - Test error message formatting
   - Mock `bpy.context` for testing

### Integration Test Requirements
1. **Per-Workflow Tests** (one file per workflow):
   - Test happy path (correct selection → modifiers applied)
   - Test all error conditions
   - Test undo/redo behavior
   - Verify modifier stack order (for multi-modifier workflows)
   - Verify all parameter values are correct

2. **End-to-End Tests**:
   - Test complete flow: command entry → parsing → validation → execution → feedback
   - Test workflow switching (execute different workflows in sequence)
   - Test operator called multiple times

### Test Fixtures Required
- `single_cube.blend`: One mesh object
- `cube_and_empty.blend`: One mesh + one empty
- `cube_and_curve.blend`: One mesh + one bezier curve
- `two_cubes.blend`: Two mesh objects
- `complex_selection.blend`: Multiple object types selected

---

## Compatibility Contract

### Blender Version Support
- **Minimum**: Blender 3.0
- **Tested**: Blender 3.6, 4.0, 4.2
- **Python**: 3.10+

### Platform Support
- Windows 10/11
- macOS 11+ (Intel and Apple Silicon)
- Linux (Ubuntu 20.04+, Fedora 35+)

### Breaking Changes
- No breaking changes to operator ID (`copilot.modifier_assistant`)
- Property names may evolve (but will maintain backward compatibility)
- New workflows may be added without breaking existing commands

---

## Dependencies

### Required Blender Modules
- `bpy.types.Operator`
- `bpy.props.StringProperty`
- `bpy.ops` (for transform_apply, mode_set, shade_smooth)
- `bmesh` (for Symmetrize vertex operations)

### Internal Module Dependencies
- `copilot.utils.command_parser`
- `copilot.utils.context_validator`
- `copilot.utils.modifier_workflows`
- `copilot.utils.user_feedback`

### No External Dependencies
- No third-party Python packages required
- Pure Blender Python API implementation

---

## Contract Compliance

### Validation Checklist
- [ ] All input preconditions documented
- [ ] All output guarantees documented
- [ ] All error conditions listed with messages
- [ ] Performance targets specified
- [ ] Undo behavior defined
- [ ] Test requirements enumerated
- [ ] Dependencies listed
- [ ] Compatibility requirements stated

### Contract Tests
Contract tests will verify:
1. Operator returns only `{'FINISHED'}` or `{'CANCELLED'}`
2. All error messages match documented formats
3. Undo flag is set correctly
4. Performance targets are met
5. All workflows execute without Blender crashes

---

**Contract Status**: ✅ Complete and ready for test generation
**Next Step**: Generate contract tests that verify these specifications
