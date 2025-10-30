# Data Model: Intelligent Modifier Assistant

**Feature**: Intelligent Modifier Assistant  
**Date**: 2025-10-30  
**Status**: Phase 1 Design

## Overview
This document defines the key entities, their properties, relationships, and validation rules for the Intelligent Modifier Assistant feature. These entities represent the conceptual model, not implementation details.

---

## Core Entities

### 1. Command
**Description**: A natural language user request that maps to a specific modifier workflow.

**Properties**:
- **raw_text** (string): The original text entered by user (e.g., "create an array of 5 copies")
- **parsed_type** (enum): The identified workflow type
  - Values: `SMART_ARRAY`, `HARD_SURFACE`, `SYMMETRIZE`, `CURVE_DEFORM`, `SOLIDIFY`, `SHRINKWRAP`, `UNKNOWN`
- **confidence** (float): How well the command matched a pattern (0.0-1.0)
- **matched_keywords** (list[string]): Which keywords triggered the match

**Validation Rules**:
- `raw_text` must not be empty
- `raw_text` length must be >= 3 characters
- `parsed_type` must be one of the defined enum values
- If `parsed_type` is `UNKNOWN`, error message must be generated

**State Transitions**:
```
USER_INPUT → PARSED → VALIDATED → EXECUTED
           ↓         ↓
         UNKNOWN   VALIDATION_FAILED
```

---

### 2. SelectionContext
**Description**: The current state of selected objects in the Blender scene, used for validation.

**Properties**:
- **selected_objects** (list[Object]): All currently selected objects
- **active_object** (Object | null): The active object (can be null)
- **object_count** (int): Number of selected objects
- **current_mode** (enum): Current object mode
  - Values: `OBJECT`, `EDIT`, `SCULPT`, `VERTEX_PAINT`, etc.
- **object_types** (dict): Count of each object type
  - Example: `{'MESH': 2, 'EMPTY': 1}` or `{'MESH': 1, 'CURVE': 1}`

**Validation Rules**:
- `object_count` must equal `len(selected_objects)`
- `active_object` should be in `selected_objects` (if not null)
- `object_types` must accurately reflect types of `selected_objects`
- Most workflows require `current_mode == 'OBJECT'`

**Derived Properties**:
- `has_selection`: `object_count > 0`
- `has_active`: `active_object is not null`
- `is_single_mesh`: `object_count == 1 and object_types.get('MESH') == 1`
- `is_mesh_and_empty`: `object_count == 2 and object_types == {'MESH': 1, 'EMPTY': 1}`
- `is_mesh_and_curve`: `object_count == 2 and object_types == {'MESH': 1, 'CURVE': 1}`
- `is_two_meshes`: `object_count == 2 and object_types.get('MESH') == 2`

---

### 3. WorkflowRequirements
**Description**: The prerequisites that must be met for a specific workflow to execute.

**Properties**:
- **workflow_type** (enum): Which workflow these requirements apply to
- **required_object_count** (int | range): Expected number of selected objects
  - Example: `1` for Solidify, `2` for Curve Deform, `1-2` for Smart Array
- **required_object_types** (dict): Expected object type configuration
  - Example: `{'MESH': 1}` for Solidify, `{'MESH': 1, 'CURVE': 1}` for Curve Deform
- **required_mode** (enum): Expected Blender mode (usually `OBJECT`)
- **allows_multiple_configurations** (bool): Whether workflow has variants
  - Example: `True` for Smart Array (single object vs object offset)

**Validation Rules**:
- `required_object_count` must be > 0
- `required_object_types` must not be empty
- Total count in `required_object_types` should match `required_object_count`

**Relationships**:
- One `WorkflowRequirements` per workflow type
- Used to validate `SelectionContext` before execution

---

### 4. ModifierConfiguration
**Description**: The specific settings to apply for a modifier in a workflow.

**Properties**:
- **modifier_type** (enum): The Blender modifier type
  - Values: `ARRAY`, `BEVEL`, `SUBSURF`, `MIRROR`, `CURVE`, `SOLIDIFY`, `SHRINKWRAP`
- **modifier_name** (string): Display name for the modifier
- **parameter_settings** (dict): Key-value pairs of modifier properties
  - Example (Array): `{'count': 5, 'use_relative_offset': True, 'relative_offset_displace': (1.0, 0.0, 0.0)}`
  - Example (Bevel): `{'limit_method': 'ANGLE', 'segments': 3}`
- **execution_order** (int): Position in modifier stack (lower = earlier)
- **target_object** (Object | null): Object to apply modifier to (usually active object)

**Validation Rules**:
- `modifier_type` must be one of supported types
- `modifier_name` must be non-empty, max 64 characters
- `parameter_settings` keys must be valid for the `modifier_type`
- `execution_order` must be >= 0
- `target_object` must be a valid object reference

**Relationships**:
- One or more `ModifierConfiguration` per `Workflow`
- Bel belongs to a specific `Workflow`

---

### 5. Workflow
**Description**: A complete automated procedure that applies one or more modifiers with prerequisites.

**Properties**:
- **workflow_id** (enum): Unique identifier
  - Values: `SMART_ARRAY_SINGLE`, `SMART_ARRAY_CONTROLLED`, `HARD_SURFACE`, `SYMMETRIZE`, `CURVE_DEFORM`, `SOLIDIFY`, `SHRINKWRAP`
- **display_name** (string): User-friendly name (e.g., "Hard-Surface SubD Setup")
- **description** (string): What the workflow does
- **prerequisites** (list[string]): Required actions before modifier application
  - Example (Symmetrize): `['apply_scale', 'enter_edit_mode', 'delete_positive_x_vertices']`
  - Example (Curve Deform): `['apply_scale_mesh', 'apply_scale_curve', 'align_origins']`
- **modifiers** (list[ModifierConfiguration]): Modifiers to apply in order
- **post_actions** (list[string]): Actions after modifiers applied
  - Example (Hard-Surface): `['set_smooth_shading']`
  - Example (Symmetrize): `['exit_edit_mode']`
- **estimated_duration_ms** (int): Expected execution time in milliseconds

**Validation Rules**:
- `workflow_id` must be unique across all workflows
- `display_name` must be non-empty
- If `prerequisites` includes mode changes, `post_actions` should restore mode
- `modifiers` list must not be empty (except for workflows with only mesh operations)
- `estimated_duration_ms` should be > 0 and < 5000 (5 second max)

**Relationships**:
- Has one `WorkflowRequirements` (validation criteria)
- Contains one or more `ModifierConfiguration` (what to apply)
- Triggered by one `Command` (user intent)

---

### 6. ValidationResult
**Description**: The outcome of validating a selection context against workflow requirements.

**Properties**:
- **is_valid** (bool): Whether validation passed
- **error_message** (string | null): Human-readable error if validation failed
- **error_code** (enum | null): Machine-readable error type
  - Values: `NO_SELECTION`, `WRONG_OBJECT_COUNT`, `WRONG_OBJECT_TYPES`, `WRONG_MODE`, `NO_ACTIVE_OBJECT`
- **validated_at** (timestamp): When validation occurred
- **context_snapshot** (SelectionContext): Copy of context at validation time

**Validation Rules**:
- If `is_valid == True`, then `error_message` and `error_code` must be null
- If `is_valid == False`, then `error_message` and `error_code` must not be null
- `error_message` must be actionable and specific (e.g., "This command requires two selected objects: a mesh and a curve")

**Relationships**:
- Produced by validating `SelectionContext` against `WorkflowRequirements`
- Determines whether `Workflow` can proceed

---

### 7. ExecutionResult
**Description**: The outcome of executing a workflow.

**Properties**:
- **status** (enum): Execution outcome
  - Values: `SUCCESS`, `CANCELLED`, `ERROR`
- **message** (string): User-facing feedback message
- **workflow_executed** (Workflow): Which workflow was attempted
- **modifiers_added** (list[string]): Names of modifiers successfully added
- **objects_modified** (list[Object]): Objects that were changed
- **execution_time_ms** (int): Actual time taken
- **undo_available** (bool): Whether operation can be undone

**Validation Rules**:
- If `status == SUCCESS`, `modifiers_added` should not be empty (unless pure mesh operation)
- If `status == ERROR`, `message` must explain what went wrong
- `execution_time_ms` must be >= 0
- `undo_available` should be `True` for all successful operations

**Relationships**:
- Result of executing a `Workflow`
- Reported to user via UI feedback system

---

## Entity Relationships Diagram

```
Command
  ↓ (identifies)
Workflow
  ↓ (has requirements)
WorkflowRequirements
  ↓ (validates against)
SelectionContext → ValidationResult
  ↓ (if valid, execute)
Workflow
  ↓ (applies)
ModifierConfiguration × N
  ↓ (produces)
ExecutionResult
```

---

## Workflow-Specific Configurations

### Smart Array (Single Object)
**Requirements**:
- Objects: 1 mesh
- Mode: Object

**Modifiers**:
1. Array (count=5, relative X-offset=1.0)

**Prerequisites**: None  
**Post-Actions**: None

---

### Smart Array (Object Offset)
**Requirements**:
- Objects: 1 mesh + 1 empty
- Mode: Object

**Modifiers**:
1. Array (use_object_offset=True, offset_object=empty, use_relative_offset=False)

**Prerequisites**: Identify which object is mesh vs empty  
**Post-Actions**: None

---

### Hard-Surface SubD
**Requirements**:
- Objects: 1 mesh
- Mode: Object

**Modifiers**:
1. Bevel (limit_method='ANGLE', segments=3) [order=1]
2. Subdivision Surface (levels=2) [order=2]

**Prerequisites**: None  
**Post-Actions**: Set smooth shading

---

### Symmetrize
**Requirements**:
- Objects: 1 mesh
- Mode: Object

**Modifiers**:
1. Mirror (axis='X', use_bisect=True, use_clip=True)

**Prerequisites**:
1. Apply scale transformation
2. Enter Edit Mode
3. Select vertices where x > 0
4. Delete selected vertices

**Post-Actions**: Exit Edit Mode, return to Object Mode

---

### Curve Deform
**Requirements**:
- Objects: 1 mesh + 1 curve
- Mode: Object

**Modifiers**:
1. Curve (object=curve_object)

**Prerequisites**:
1. Apply scale to mesh
2. Apply scale to curve
3. Align mesh origin to curve origin

**Post-Actions**: None

---

### Solidify
**Requirements**:
- Objects: 1 mesh
- Mode: Object

**Modifiers**:
1. Solidify (thickness=0.01, use_even_offset=True)

**Prerequisites**: None  
**Post-Actions**: None

---

### Shrinkwrap
**Requirements**:
- Objects: 2 meshes (source and target)
- Mode: Object

**Modifiers**:
1. Shrinkwrap (target=non_active_mesh, wrap_method='NEAREST_SURFACEPOINT')

**Prerequisites**: Identify active (source) vs non-active (target)  
**Post-Actions**: None

---

## Validation Rule Summary

| Workflow | Object Count | Object Types | Mode | Special Validations |
|----------|--------------|--------------|------|---------------------|
| Smart Array (Single) | 1 | 1 MESH | OBJECT | - |
| Smart Array (Controlled) | 2 | 1 MESH + 1 EMPTY | OBJECT | Must identify which is mesh |
| Hard-Surface SubD | 1 | 1 MESH | OBJECT | - |
| Symmetrize | 1 | 1 MESH | OBJECT | Must have editable geometry |
| Curve Deform | 2 | 1 MESH + 1 CURVE | OBJECT | Must identify mesh vs curve |
| Solidify | 1 | 1 MESH | OBJECT | - |
| Shrinkwrap | 2 | 2 MESH | OBJECT | Must have active object |

---

## Error Message Standards

All error messages must follow these patterns:

**No Selection**:
- Message: "Please select an object first"
- Code: `NO_SELECTION`

**Wrong Object Count**:
- Message: "This command requires [N] selected object(s), but [M] are selected"
- Code: `WRONG_OBJECT_COUNT`

**Wrong Object Types** (specific variants):
- Message: "This command requires two selected objects: a mesh and a curve"
- Message: "This command requires a mesh object to be selected"
- Code: `WRONG_OBJECT_TYPES`

**Wrong Mode**:
- Message: "This command must be run in Object Mode (currently in [MODE])"
- Code: `WRONG_MODE`

**Command Not Understood**:
- Message: "Command not understood. Try: 'make array', 'hard-surface', 'mirror', 'solidify', 'curve deform', or 'shrinkwrap'"
- Code: `COMMAND_NOT_RECOGNIZED`

---

## Performance Targets

| Operation | Target Duration | Notes |
|-----------|----------------|-------|
| Command parsing | < 10ms | Pattern matching should be instant |
| Context validation | < 20ms | Simple object count/type checks |
| Simple modifier (Array, Solidify, Shrinkwrap) | < 50ms | Direct modifier addition |
| Complex modifier (Hard-Surface) | < 100ms | Multiple modifiers + shading |
| Edit mode workflow (Symmetrize) | < 200ms | Includes mode switch + bmesh ops |
| Multi-prerequisite (Curve Deform) | < 150ms | Scale application + origin alignment |

**Total End-to-End Target**: < 300ms from command submission to feedback

---

**Data Model Complete**: All entities, relationships, and validation rules defined. Ready for contract generation.
