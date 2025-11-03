# Tasks: Intelligent Modifier Assistant

**Input**: Design documents from `/home/adarsh-hinsodiya/Projects/Blender-Copilot/specs/003-intelligent-modifier-assistant/`
**Prerequisites**: plan.md, data-model.md, contracts/modifier_assistant_operator.md, quickstart.md

## Execution Flow (main)
```
1. Load plan.md from feature directory ✅
   → Tech stack: Python 3.10+, Blender Python API (bpy), bmesh
   → Structure: Single Blender add-on extending existing Copilot
2. Load design documents: ✅
   → data-model.md: 7 entities (Command, SelectionContext, WorkflowRequirements, etc.)
   → contracts/: modifier_assistant_operator.md (main operator contract)
   → quickstart.md: 6 workflows, test procedures
3. Generate tasks by category: ✅
   → Setup: 4 tasks (fixtures, structure, dependencies)
   → Tests: 14 tasks (unit + integration, all TDD)
   → Core: 12 tasks (parser, validator, workflows, operator, panel)
   → Integration: 4 tasks (registration, preferences, undo)
   → Polish: 6 tasks (optimization, docs, manual tests)
4. Apply task rules: ✅
   → Different files = [P] marked
   → Same file = sequential
   → Tests before implementation
5. Number tasks sequentially (T001-T040) ✅
6. Generate dependency graph ✅
7. Create parallel execution examples ✅
8. Validate task completeness: ✅
   → All workflows have integration tests ✅
   → All utilities have unit tests ✅
   → Operator has contract tests ✅
9. Return: SUCCESS (40 tasks ready for execution) ✅
```

---

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- All paths relative to repository root: `/home/adarsh-hinsodiya/Projects/Blender-Copilot/`

---

## Phase 3.1: Setup & Test Fixtures (4 tasks)

### T001: Create Blender test scene fixtures
**File**: `tests/fixtures/single_cube.blend`, `tests/fixtures/cube_and_empty.blend`, `tests/fixtures/cube_and_curve.blend`, `tests/fixtures/two_cubes.blend`

**Description**: Create four .blend test fixture files for integration testing:
1. `single_cube.blend` - One default cube at origin
2. `cube_and_empty.blend` - One cube + one empty object (for array workflow)
3. `cube_and_curve.blend` - One cube + one bezier curve (for curve deform workflow)
4. `two_cubes.blend` - Two cubes side by side (for shrinkwrap workflow)

Save all files in `tests/fixtures/` directory.

**Acceptance**: All four .blend files load successfully in Blender 3.0+

---

### T002: Initialize add-on properties for modifier assistant
**File**: `copilot/props/modifier_preferences.py`

**Description**: Create property group file to store modifier assistant preferences and command text:
- Create `ModifierAssistantProperties` class inheriting from `bpy.types.PropertyGroup`
- Add `copilot_modifier_command` StringProperty (stores user's command text)
- Add default values for each workflow (e.g., array_count, solidify_thickness)
- Include registration/unregistration functions

**Acceptance**: File exists, compiles without errors, follows Blender property group patterns

---

### T003 [P]: Configure Python linting for new files
**File**: `.flake8`, `pyproject.toml` (if using Black)

**Description**: Ensure linting configuration covers new modifier assistant files:
- Add `copilot/operators/modifier_assistant.py` to linting scope
- Add `copilot/utils/command_parser.py`, `context_validator.py`, `modifier_workflows.py`
- Add all test files to scope
- Verify max line length = 100 (Blender convention)

**Acceptance**: Running `flake8 copilot/ tests/` reports no configuration errors

---

### T004 [P]: Create test helpers for Blender context mocking
**File**: `tests/helpers/blender_mocks.py`

**Description**: Create helper utilities for unit tests that need to mock Blender context:
- `MockBlenderContext` class with `selected_objects`, `active_object`, `mode` properties
- `MockObject` class with `type`, `name`, `modifiers` properties
- `create_mock_scene()` function for common test scenarios
- Helper functions to assert modifier stack contents

**Acceptance**: File compiles, can be imported by unit tests, provides clean mock API

---

## Phase 3.2: Tests First (TDD) ✅ COMPLETE (14 tasks)

**STATUS: All 14 test files created. Tests will FAIL until Phase 3.3 implementation is complete.**

### T005 [P]: ✅ Command parser unit tests
**File**: `tests/unit/test_command_parser.py`

**Description**: Write unit tests for command parsing logic (using mocks, no Blender required):
- Test parsing "create an array" → `'SMART_ARRAY'`
- Test parsing "make hard-surface" → `'HARD_SURFACE'`
- Test parsing all six workflow patterns
- Test case insensitivity (e.g., "MAKE ARRAY" works)
- Test unknown commands → `'UNKNOWN'`
- Test empty/whitespace commands → `'UNKNOWN'`
- Test partial matches prioritize longer patterns

**Acceptance**: 15+ test cases, all currently FAILING (parser not implemented yet) ✅ DONE

---

### T006 [P]: ✅ Context validator unit tests
**File**: `tests/unit/test_context_validator.py`

**Description**: Write unit tests for context validation using mocked Blender context:
- Test `validate_object_selected()` with empty selection → (False, error)
- Test `validate_object_count(1)` with 2 objects → (False, error)
- Test `validate_object_types({'MESH': 1})` with correct/incorrect types
- Test `validate_object_mode('OBJECT')` in different modes
- Test all error messages match contract specifications exactly
- Test each workflow's specific validation requirements

**Acceptance**: 20+ test cases covering all validation functions, all currently FAILING ✅ DONE

---

### T007 [P]: ✅ Modifier workflows unit tests
**File**: `tests/unit/test_modifier_workflows.py`

**Description**: Write unit tests for individual workflow functions (mocked bpy operations):
- Test each workflow function signature (input/output types)
- Test modifier parameter values are correct (e.g., array count=5)
- Test return values match contract (status set, message string)
- Test error conditions (e.g., scale application failure)
- Mock `bpy.ops`, `bpy.data.modifiers.new()` calls
- Verify correct sequence of operations

**Acceptance**: 25+ test cases (4-5 per workflow), all currently FAILING ✅ DONE

---

### T008 [P]: ✅ Smart Array workflow integration test
**File**: `tests/integration/test_smart_array_workflow.py`

**Description**: Write integration test for Smart Array workflow (requires Blender instance):
- Test single object variant: Load `single_cube.blend`, execute, verify Array modifier exists
- Test object offset variant: Load `cube_and_empty.blend`, execute, verify empty is offset object
- Test modifier parameters: count=5, relative_offset_displace=(1,0,0)
- Test error: No selection → "Please select an object first"
- Test error: Wrong object types → specific error message
- Test undo: Execute → Undo → modifier removed

**Acceptance**: 8+ test cases, requires Blender, all currently FAILING ✅ DONE

---

### T009 [P]: ✅ Hard-Surface SubD workflow integration test
**File**: `tests/integration/test_hard_surface_workflow.py`

**Description**: Write integration test for Hard-Surface SubD workflow:
- Load `single_cube.blend`
- Execute workflow, verify Bevel modifier added first
- Verify Subdivision Surface modifier added second (correct order!)
- Verify Bevel settings: limit_method='ANGLE', segments=3
- Verify Subdivision settings: levels=2
- Verify object shading mode is SMOOTH
- Test undo: All modifiers + shading removed in one step
- Test error conditions

**Acceptance**: 10+ test cases, all currently FAILING ✅ DONE

---

### T010 [P]: ✅ Symmetrize workflow integration test
**File**: `tests/integration/test_symmetrize_workflow.py`

**Description**: Write integration test for Symmetrize (most complex workflow):
- Load `single_cube.blend`
- Execute workflow
- Verify scale was applied (check object.scale == (1,1,1))
- Verify Mirror modifier added with correct settings
- Verify positive X vertices were deleted (count vertices, check coordinates)
- Verify returned to Object Mode
- Test undo: Restores deleted vertices + removes modifier
- Test BMesh operations performance (<200ms)

**Acceptance**: 12+ test cases including performance test, all FAILING ✅ DONE

---

### T011 [P]: ✅ Curve Deform workflow integration test
**File**: `tests/integration/test_curve_deform_workflow.py`

**Description**: Write integration test for Curve Deform workflow:
- Load `cube_and_curve.blend`
- Execute workflow
- Verify scale applied to both mesh and curve
- Verify mesh origin moved to curve origin (location check)
- Verify Curve modifier added to mesh
- Verify curve object assigned as modifier target
- Test error: Wrong object types (e.g., two meshes)
- Test undo: Restores origins and removes modifier

**Acceptance**: 10+ test cases, all currently FAILING ✅ DONE

---

### T012 [P]: ✅ Solidify workflow integration test
**File**: `tests/integration/test_solidify_workflow.py`

**Description**: Write integration test for Solidify workflow:
- Load `single_cube.blend`
- Execute workflow
- Verify Solidify modifier added
- Verify thickness = 0.01
- Verify use_even_offset = True
- Test with different object types (plane, circle)
- Test undo behavior

**Acceptance**: 6+ test cases, all currently FAILING ✅ DONE

---

### T013 [P]: ✅ Shrinkwrap workflow integration test
**File**: `tests/integration/test_shrinkwrap_workflow.py`

**Description**: Write integration test for Shrinkwrap workflow:
- Load `two_cubes.blend`
- Select both cubes (one active, one not)
- Execute workflow
- Verify Shrinkwrap modifier added to active object
- Verify non-active object is the target
- Verify wrap_method = 'NEAREST_SURFACEPOINT'
- Test error: Only one object selected
- Test undo

**Acceptance**: 8+ test cases, all currently FAILING ✅ DONE

---

### T014 [P]: ✅ Operator contract compliance test
**File**: `tests/integration/test_operator_contract.py`

**Description**: Write test to verify operator meets contract specifications:
- Test operator returns only {'FINISHED'} or {'CANCELLED'}, never crashes
- Test all error messages exactly match contract specifications
- Test `bl_options` includes 'UNDO' flag
- Test performance: measure end-to-end execution time for each workflow
- Verify all performance targets met (<350ms total)
- Test operator called multiple times in sequence works correctly

**Acceptance**: 15+ contract verification tests, all currently FAILING ✅ DONE

---

### T015 [P]: ✅ Command parsing edge cases test
**File**: `tests/integration/test_command_edge_cases.py`

**Description**: Write integration tests for command parsing edge cases:
- Test very long commands (1000+ characters)
- Test commands with special characters (@#$%^&*)
- Test commands with only keywords (e.g., just "array")
- Test commands with multiple workflow keywords (e.g., "array and mirror")
- Test multi-language characters (Unicode)
- Test command history/recall (if implemented)

**Acceptance**: 10+ edge case tests, all currently FAILING ✅ DONE

---

### T016 [P]: ✅ Selection validation edge cases test
**File**: `tests/integration/test_selection_edge_cases.py`

**Description**: Write integration tests for selection validation edge cases:
- Test with 100+ objects selected
- Test with different object types mixed (MESH + LIGHT + CAMERA)
- Test with no active object but objects selected
- Test with active object not in selection
- Test in wrong modes (Edit Mode, Sculpt Mode, etc.)
- Test with locked/hidden objects

**Acceptance**: 12+ edge case tests, all currently FAILING ✅ DONE

---

### T017 [P]: ✅ Undo/Redo comprehensive test
**File**: `tests/integration/test_undo_redo.py`

**Description**: Write comprehensive undo/redo integration tests:
- Test undo after each workflow type
- Test redo re-executes correctly
- Test undo/redo multiple times in sequence
- Test undo after partial failure (e.g., Symmetrize with scale failure)
- Test undo stack depth (ensure only one undo step per workflow)
- Test undo with selection changed

**Acceptance**: 15+ undo/redo tests, all currently FAILING ✅ DONE

---

### T018 [P]: ✅ Multi-workflow chaining test
**File**: `tests/integration/test_workflow_chaining.py`

**Description**: Write integration tests for running multiple workflows on same object:
- Test: Array → Solidify → Hard-Surface (three workflows stacked)
- Test: Mirror → Array (symmetry then duplicate)
- Test: Curve Deform → Solidify (bend then thicken)
- Verify modifiers stack correctly
- Verify undo removes most recent workflow only
- Test performance with 5+ workflows chained

**Acceptance**: 8+ chaining tests, all currently FAILING ✅ DONE

---

## Phase 3.3: Core Implementation (ONLY after Phase 3.2 tests are failing) (12 tasks)

**✅ READY TO START - All Phase 3.2 tests are written and will fail until implementation**

### T019 [P]: Implement command parser module
**File**: `copilot/utils/command_parser.py`

**Description**: Implement the natural language command parser:
- Create `COMMAND_PATTERNS` dictionary mapping workflow types to keyword lists
- Implement `parse_command(command_text: str) -> str` function
- Use case-insensitive matching
- Return first matching workflow or 'UNKNOWN'
- Optimize for <10ms execution (use simple string matching, not regex)

**Success Criteria**: T005 tests now PASS

---

### T020 [P]: Implement context validator module
**File**: `copilot/utils/context_validator.py`

**Description**: Implement context validation service:
- Implement `validate_object_selected() -> tuple[bool, str]`
- Implement `validate_object_count(expected: int) -> tuple[bool, str]`
- Implement `validate_object_types(required_types: dict) -> tuple[bool, str]`
- Implement `validate_active_object() -> tuple[bool, str]`
- Implement `validate_object_mode(required_mode: str) -> tuple[bool, str]`
- All error messages must match contract exactly

**Success Criteria**: T006 tests now PASS

---

### T021: Implement Smart Array workflow function
**File**: `copilot/utils/modifier_workflows.py`

**Description**: Implement `apply_smart_array_single()` and `apply_smart_array_controlled()` functions:
- Single variant: Add Array modifier with count=5, relative X-offset=1.0
- Controlled variant: Identify mesh vs empty, add Array with object offset
- Return (status_set, message) tuple
- Handle errors gracefully

**Dependencies**: Requires T019 (parser) and T020 (validator) for context

**Success Criteria**: T007 array tests + T008 integration tests PASS

---

### T022: Implement Hard-Surface SubD workflow function
**File**: `copilot/utils/modifier_workflows.py` (append to same file)

**Description**: Implement `apply_hard_surface_setup(obj)` function:
- Add Bevel modifier first (limit_method='ANGLE', segments=3)
- Add Subdivision Surface modifier second (levels=2)
- Call `bpy.ops.object.shade_smooth()` to set smooth shading
- Ensure correct modifier order in stack

**Dependencies**: Requires T021 complete (same file)

**Success Criteria**: T007 hard-surface tests + T009 integration tests PASS

---

### T023: Implement Symmetrize workflow function
**File**: `copilot/utils/modifier_workflows.py` (append to same file)

**Description**: Implement `apply_symmetrize(obj)` function:
- Apply scale: `bpy.ops.object.transform_apply(scale=True)`
- Add Mirror modifier (X-axis, bisect=True, clip=True)
- Enter Edit Mode
- Use bmesh to select vertices where x > 0.0
- Delete selected vertices with `bmesh.ops.delete()`
- Return to Object Mode
- Optimize for <200ms performance

**Dependencies**: Requires T022 complete (same file)

**Success Criteria**: T007 symmetrize tests + T010 integration tests PASS

---

### T024: Implement Curve Deform workflow function
**File**: `copilot/utils/modifier_workflows.py` (append to same file)

**Description**: Implement `apply_curve_deform(mesh, curve)` function:
- Identify which object is mesh vs curve
- Apply scale to both objects
- Align mesh origin to curve origin (set mesh.location = curve.location)
- Add Curve modifier to mesh with curve as target
- Handle scale application failures gracefully

**Dependencies**: Requires T023 complete (same file)

**Success Criteria**: T007 curve deform tests + T011 integration tests PASS

---

### T025: Implement Solidify and Shrinkwrap workflow functions
**File**: `copilot/utils/modifier_workflows.py` (append to same file)

**Description**: Implement final two workflows:
- `apply_solidify(obj)`: Add Solidify modifier (thickness=0.01, use_even_offset=True)
- `apply_shrinkwrap(source, target)`: Add Shrinkwrap modifier (wrap_method='NEAREST_SURFACEPOINT')
- Both are simple single-modifier workflows

**Dependencies**: Requires T024 complete (same file)

**Success Criteria**: T007 solidify/shrinkwrap tests + T012/T013 integration tests PASS

---

### T026: Implement modifier assistant operator (parsing & validation only)
**File**: `copilot/operators/modifier_assistant.py`

**Description**: Create the main operator class with parsing and validation only:
- Create `COPILOT_OT_modifier_assistant` class inheriting from `bpy.types.Operator`
- Set `bl_idname`, `bl_label`, `bl_options = {'REGISTER', 'UNDO'}`
- Implement `execute(self, context)` method:
  - Get command text from `context.scene.copilot_modifier_command`
  - Call `parse_command()` to get workflow type
  - If UNKNOWN, report error and return {'CANCELLED'}
  - Call appropriate validation function for workflow type
  - If validation fails, report error and return {'CANCELLED'}
  - Return {'FINISHED'} (workflow execution added in T027)

**Dependencies**: Requires T019 (parser) and T020 (validator) complete

**Success Criteria**: Operator loads, validates correctly, T014 partial tests pass

---

### T027: Implement operator workflow execution routing
**File**: `copilot/operators/modifier_assistant.py` (modify existing)

**Description**: Add workflow execution logic to operator's `execute()` method:
- Add conditional routing based on workflow type
- Call appropriate workflow function from `modifier_workflows.py`
- Handle different selection patterns (1 object vs 2 objects)
- Report success/error message from workflow function
- Return workflow status

**Dependencies**: Requires T026 (operator skeleton) and T021-T025 (all workflows) complete

**Success Criteria**: All T008-T013 integration tests PASS, T014 contract tests PASS

---

### T028 [P]: Implement modifier assistant UI panel
**File**: `copilot/panels/modifier_panel.py`

**Description**: Create the UI panel for modifier assistant:
- Create `COPILOT_PT_modifier_assistant` class inheriting from `bpy.types.Panel`
- Set `bl_space_type = 'VIEW_3D'`, `bl_region_type = 'UI'`, `bl_category = 'Copilot'`
- Implement `draw(self, context)` method:
  - Add text input field for command (bound to scene property)
  - Add "Execute" button calling `bpy.ops.copilot.modifier_assistant()`
  - Show current selection count
  - Optionally show list of recognized commands as help text

**Dependencies**: Can run in parallel with operator implementation

**Success Criteria**: Panel appears in 3D View sidebar, UI is functional

---

### T029 [P]: Create error message constants and user feedback utility
**File**: `copilot/utils/user_feedback.py`

**Description**: Create centralized error messages and feedback utilities:
- Define all error message constants matching contract
- Create helper function `format_error_message()` for consistent formatting
- Create helper function `report_to_user(operator, level, message)` wrapping `self.report()`
- Ensure all messages are user-friendly and actionable

**Dependencies**: Can run in parallel

**Success Criteria**: All error messages consistent across codebase

---

### T030: Update operator to use user feedback utility
**File**: `copilot/operators/modifier_assistant.py` (modify existing)

**Description**: Refactor operator to use centralized user feedback:
- Import `user_feedback` utility
- Replace direct `self.report()` calls with `report_to_user()`
- Use error message constants instead of hardcoded strings
- Ensure all feedback matches contract specifications exactly

**Dependencies**: Requires T029 (user feedback utility) and T027 (operator execution) complete

**Success Criteria**: T014 contract tests PASS with exact message matching

---

## Phase 3.4: Integration (4 tasks)

### T031: Register modifier assistant in add-on __init__.py
**File**: `copilot/__init__.py` (modify existing)

**Description**: Add modifier assistant components to add-on registration:
- Import `modifier_assistant.py` operator
- Import `modifier_panel.py` panel
- Import `modifier_preferences.py` properties
- Add classes to `classes` list for registration
- Register scene property for command text
- Add to `register()` and `unregister()` functions

**Dependencies**: Requires T027 (operator), T028 (panel), T002 (properties) complete

**Success Criteria**: Add-on loads without errors, all components registered

---

### T032: Implement add-on preferences for modifier defaults
**File**: `copilot/preferences.py` (create or modify)

**Description**: Add preference options for modifier assistant:
- Add preferences for default values (array count, solidify thickness, etc.)
- Add toggle for showing command help in panel
- Add preference for performance mode (skip some validations for speed)
- Create preferences UI panel

**Dependencies**: Requires T031 (registration) complete

**Success Criteria**: Preferences appear in add-on settings, defaults work

---

### T033: Integrate undo system verification
**File**: `copilot/operators/modifier_assistant.py` (modify existing)

**Description**: Verify and optimize undo system integration:
- Ensure `bl_options = {'REGISTER', 'UNDO'}` is set
- Test that all workflows create single undo step
- Verify complex workflows (Symmetrize) undo completely
- Verify prerequisites (scale application) are included in undo
- Add undo testing to operator docstring

**Dependencies**: Requires T027 (operator execution) complete

**Success Criteria**: T017 undo/redo tests PASS

---

### T034: Performance profiling and optimization
**File**: `copilot/utils/performance.py` (create)

**Description**: Add performance monitoring and optimization:
- Create performance profiler decorator
- Profile each workflow function
- Identify bottlenecks (especially Symmetrize BMesh operations)
- Optimize slow operations to meet contract targets (<350ms total)
- Add performance metrics logging (optional debug mode)

**Dependencies**: Requires all workflows implemented (T021-T025)

**Success Criteria**: All performance targets in contract met, T014 performance tests PASS

---

## Phase 3.5: Polish (6 tasks)

### T035 [P]: Add comprehensive docstrings and type hints
**File**: All `.py` files in `copilot/operators/`, `copilot/utils/`, `copilot/panels/`

**Description**: Add documentation to all modules:
- Add module-level docstrings explaining purpose
- Add function docstrings with Args, Returns, Raises sections
- Add type hints to all function signatures
- Add inline comments for complex logic (especially Symmetrize BMesh code)
- Follow Google Python Style Guide

**Dependencies**: Can run in parallel after implementation complete

**Success Criteria**: All functions have docstrings, type checker (mypy) passes

---

### T036 [P]: Code cleanup and style consistency
**File**: All `.py` files in `copilot/` and `tests/`

**Description**: Clean up code for production:
- Run Black formatter on all files
- Run flake8 and fix all linting errors
- Remove debug print statements
- Remove commented-out code
- Ensure consistent naming conventions
- Verify all imports are used and sorted

**Dependencies**: Can run in parallel with T035

**Success Criteria**: `flake8 copilot/ tests/` passes with zero errors

---

### T037: Update quickstart.md with final commands
**File**: `specs/003-intelligent-modifier-assistant/quickstart.md` (modify)

**Description**: Update quickstart guide to match implementation:
- Verify all command examples work exactly as documented
- Update any changed error messages
- Add screenshots of UI panel (if available)
- Add troubleshooting section for common issues
- Verify test procedures in quickstart still work

**Dependencies**: Requires all implementation complete

**Success Criteria**: Following quickstart guide works for new users

---

### T038: Create developer documentation
**File**: `specs/003-intelligent-modifier-assistant/DEVELOPMENT.md` (create)

**Description**: Write developer documentation for future maintainers:
- Explain architecture (parser → validator → workflows → operator)
- Document how to add new workflows (extension strategy from research)
- Explain command pattern priority system
- Document testing strategy and how to run tests
- Add troubleshooting guide for common development issues

**Dependencies**: Requires all implementation complete

**Success Criteria**: New developer can add a workflow following the doc

---

### T039 [P]: Manual testing with real workflows
**File**: `specs/003-intelligent-modifier-assistant/MANUAL_TESTS.md` (create)

**Description**: Perform comprehensive manual testing in Blender:
- Test each workflow with real 3D models (not just test cubes)
- Test with high-poly meshes (100k+ vertices)
- Test with complex multi-object selections
- Test in different Blender versions (3.0, 3.6, 4.0)
- Test on different platforms (Windows, macOS, Linux if available)
- Document any issues found
- Create manual test checklist document

**Dependencies**: Can run after implementation complete

**Success Criteria**: All workflows work in real-world scenarios, issues documented

---

### T040: Final integration test run and validation
**File**: N/A (run all tests)

**Description**: Final validation before completion:
- Run entire test suite: `python -m pytest tests/`
- Verify all unit tests pass
- Verify all integration tests pass
- Verify performance tests meet targets
- Run manual test checklist from T039
- Verify quickstart guide from T037
- Check code coverage (aim for >80%)
- Verify no regressions in existing lighting feature

**Dependencies**: Requires ALL previous tasks complete

**Success Criteria**: 100% test pass rate, >80% code coverage, no regressions

---

## Dependencies Graph

```
Setup Phase:
T001, T002, T003, T004 [all parallel] → [blocks Phase 3.2]

Test Phase (TDD - MUST complete before implementation):
T005, T006, T007 [parallel unit tests]
T008, T009, T010, T011, T012, T013 [parallel integration tests per workflow]
T014, T015, T016 [parallel operator/edge case tests]
T017, T018 [parallel undo/chaining tests]

Core Implementation:
T019 [parser] ─┐
T020 [validator] ─┼─→ T026 [operator skeleton] → T027 [operator execution] → T030 [feedback integration]
                  │
T021 [array] → T022 [hard-surface] → T023 [symmetrize] → T024 [curve] → T025 [solidify/shrinkwrap]
                                                                          │
T028 [panel, parallel]                                                   │
T029 [feedback utility, parallel] → T030                                 │
                                                                          ↓
Integration:
T031 [registration] → T032 [preferences] → T033 [undo verification]
                                              │
                                              ↓
T034 [performance optimization]

Polish:
T035, T036 [parallel cleanup]
T037 [quickstart update] → T038 [dev docs]
T039 [manual testing, parallel]
All → T040 [final validation]
```

---

## Parallel Execution Examples

### Example 1: All Test Fixtures (Setup)
```bash
# Can run these 4 tasks simultaneously
Task 1: Create tests/fixtures/single_cube.blend
Task 2: Create tests/fixtures/cube_and_empty.blend
Task 3: Create tests/fixtures/cube_and_curve.blend
Task 4: Create tests/fixtures/two_cubes.blend
```

### Example 2: Unit Tests (TDD Phase)
```bash
# Can run these 3 unit test tasks simultaneously
Task 5: tests/unit/test_command_parser.py
Task 6: tests/unit/test_context_validator.py
Task 7: tests/unit/test_modifier_workflows.py
```

### Example 3: Workflow Integration Tests
```bash
# Can run all 6 workflow integration tests simultaneously
Task 8: tests/integration/test_smart_array_workflow.py
Task 9: tests/integration/test_hard_surface_workflow.py
Task 10: tests/integration/test_symmetrize_workflow.py
Task 11: tests/integration/test_curve_deform_workflow.py
Task 12: tests/integration/test_solidify_workflow.py
Task 13: tests/integration/test_shrinkwrap_workflow.py
```

### Example 4: Core Utilities
```bash
# Can run parser and validator in parallel (different files)
Task 19: copilot/utils/command_parser.py
Task 20: copilot/utils/context_validator.py

# But T021-T025 must be sequential (same file modifier_workflows.py)
```

### Example 5: Final Polish
```bash
# Can run these 3 polish tasks simultaneously
Task 35: Add docstrings and type hints
Task 36: Code cleanup and linting
Task 39: Manual testing
```

---

## Validation Checklist
*GATE: Verify before considering tasks complete*

- [x] All 6 workflows have integration tests (T008-T013)
- [x] All 3 core utilities have unit tests (T005-T007)
- [x] Operator has contract test (T014)
- [x] All tests written BEFORE implementation (Phase 3.2 before 3.3)
- [x] Parallel tasks use different files (verified with [P] markers)
- [x] Each task specifies exact file path
- [x] No task modifies same file as another [P] task
- [x] Add-on registration handled (T031)
- [x] Undo system verified (T033)
- [x] Performance optimization included (T034)
- [x] Documentation complete (T035, T037, T038)
- [x] Manual testing procedure defined (T039)
- [x] Final validation step included (T040)

---

## Execution Notes

1. **TDD Enforcement**: Do NOT implement any code in Phase 3.3 until ALL tests in Phase 3.2 are written and failing.

2. **Sequential Files**: Tasks T021-T025 modify the same file (`modifier_workflows.py`) so they MUST run sequentially in that order.

3. **Test-First Mindset**: Each implementation task (T019-T030) should make specific tests pass. Reference the test task ID in commit messages.

4. **Performance Targets**: Task T034 is critical - all workflows must meet contract performance targets (<350ms total).

5. **Undo Testing**: Task T033 verifies the most complex requirement - ensure Symmetrize undo works perfectly.

6. **Manual Validation**: Task T039 is essential - automated tests can't catch all UX issues.

7. **Commit Strategy**: Commit after each task completes and its tests pass. Use task ID in commit message (e.g., "T019: Implement command parser").

---

**Tasks Complete**: 40 tasks ready for execution
**Estimated Total Time**: 25-35 hours
**Recommended Execution**: 3-5 days with 2-3 developers working in parallel

**Next Step**: Begin with Phase 3.1 (Setup), then strictly follow TDD in Phase 3.2 before any implementation.
