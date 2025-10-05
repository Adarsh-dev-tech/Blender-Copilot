# Tasks: Automated Three-Point Lighting Setup

**Input**: Design documents from `/home/adarsh-hinsodiya/Projects/Blender-Copilot/specs/001-automated-three-point/`
**Prerequisites**: plan.md (✓), research.md (✓), data-model.md (✓), contracts/lighting_operator.md (✓), quickstart.md (✓)

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Blender Add-on**: `copilot/`, `tests/` at repository root
- Paths follow single add-on structure as defined in plan.md

## Phase 3.1: Setup
- [X] T001 Create Blender add-on directory structure at copilot/ with operators/, panels/, utils/, props/ subdirectories
- [X] T002 Initialize copilot/__init__.py with add-on metadata and registration framework
- [X] T003 [P] Configure development tools: create .flake8, pyproject.toml for Black formatting

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**

### Contract Tests
- [ ] T004 [P] Lighting operator contract test in tests/integration/test_lighting_operator_contract.py
  - Test operator registration and properties
  - Test input validation (active object, object mode)
  - Test success/error return values
  - Test undo/redo compatibility
  
### Integration Tests Based on Quickstart Scenarios
- [ ] T005 [P] Basic character lighting test in tests/integration/test_basic_character_lighting.py
  - Test scenario: Select mesh object, execute operator, verify lighting rig creation
  - Validate 3 lights + 1 empty + 1 collection created
  - Check Track To constraints properly applied
  
- [ ] T006 [P] Product visualization test in tests/integration/test_product_lighting.py
  - Test lighting for product-style objects
  - Verify professional lighting ratios and positioning
  - Check rim light edge highlight functionality
  
- [ ] T007 [P] Large scene object test in tests/integration/test_large_object_lighting.py
  - Test with objects of various scales
  - Verify distance calculations based on bounding box
  - Ensure lights positioned at appropriate distances
  
- [ ] T008 [P] Multiple objects test in tests/integration/test_multiple_objects.py
  - Test active object selection with multiple objects selected
  - Verify lighting rig targets only the active object
  
### Error Handling Tests
- [ ] T009 [P] No selection error test in tests/integration/test_no_selection_error.py
  - Test error handling when no object is selected
  - Verify appropriate error message displayed
  
- [ ] T010 [P] Invalid object error test in tests/integration/test_invalid_object_error.py
  - Test with camera, light, and other non-mesh objects
  - Verify error messages for invalid object types
  
- [ ] T011 [P] Wrong mode error test in tests/integration/test_wrong_mode_error.py
  - Test error handling in Edit mode and other non-Object modes
  - Verify mode requirement enforcement

### Unit Tests for Utilities
- [ ] T012 [P] Geometry utility tests in tests/unit/test_geometry_utils.py
  - Test spherical coordinate calculations
  - Test bounding box analysis functions
  - Test distance calculation algorithms
  
- [ ] T013 [P] Validation utility tests in tests/unit/test_validation_utils.py
  - Test object selection validation
  - Test object type validation
  - Test mode validation functions

## Phase 3.3: Core Implementation (ONLY after tests are failing)

### Data Model Implementation
- [ ] T014 [P] Light configuration defaults in copilot/utils/light_defaults.py
  - Implement LIGHT_DEFAULTS dictionary from data model
  - Include power, color temperature, size, angle configurations
  
### Utility Functions
- [ ] T015 [P] Geometry calculations in copilot/utils/geometry.py
  - Implement spherical to cartesian coordinate conversion
  - Implement bounding box analysis functions
  - Implement distance calculation based on object radius
  
- [ ] T016 [P] Object validation utilities in copilot/utils/validation.py
  - Implement active object validation
  - Implement object type checking
  - Implement mode validation functions
  
- [ ] T017 [P] Blender API helpers in copilot/utils/blender_helpers.py
  - Implement light creation functions
  - Implement constraint application helpers
  - Implement collection management functions

### Core Operator Implementation
- [ ] T018 Main lighting operator in copilot/operators/lighting.py
  - Implement COPILOT_OT_create_three_point_lighting class
  - Integrate validation, geometry, and Blender helper utilities
  - Implement complete lighting rig creation workflow
  - Handle error reporting and undo integration

### UI Implementation  
- [ ] T019 Lighting panel in copilot/panels/lighting_panel.py
  - Implement COPILOT_PT_lighting_panel class
  - Add operator button with proper layout
  - Include panel in VIEW_3D space under Copilot category

## Phase 3.4: Integration
- [ ] T020 Complete add-on registration in copilot/__init__.py
  - Register lighting operator class
  - Register lighting panel class
  - Implement proper registration/unregistration functions
  - Add add-on preferences if needed

- [ ] T021 Blender scene integration testing in tests/integration/test_scene_integration.py
  - Test add-on installation and enabling
  - Test UI panel appearance and functionality
  - Test operator availability in search

- [ ] T022 Undo/redo system integration in copilot/utils/undo_integration.py
  - Ensure all operations are properly recorded for undo
  - Test undo behavior reverts all lighting rig components
  - Verify redo functionality works correctly

## Phase 3.5: Polish
- [ ] T023 [P] Performance optimization in copilot/utils/performance.py
  - Optimize bounding box calculations
  - Batch object creation for better scene updates
  - Ensure sub-second execution time requirement

- [ ] T024 [P] Enhanced error messages in copilot/utils/user_feedback.py
  - Implement detailed, helpful error messages
  - Add success feedback for completed operations
  - Ensure messages follow Blender UI conventions

- [ ] T025 [P] Code documentation in all Python files
  - Add comprehensive docstrings to all functions
  - Include usage examples in docstrings
  - Add type hints throughout codebase

- [ ] T026 [P] Add-on metadata completion in copilot/__init__.py
  - Complete bl_info dictionary with proper version, author, etc.
  - Add description and Blender version requirements
  - Include proper category and location information

- [ ] T027 Manual testing procedures in tests/manual/test_procedures.md
  - Document step-by-step manual testing procedures
  - Include visual verification checklist
  - Add troubleshooting guide for common issues

- [ ] T028 Performance benchmarking in tests/performance/test_benchmarks.py
  - Test execution time with objects of various complexities
  - Verify memory usage stays within acceptable limits
  - Test UI responsiveness during operation

## Dependencies
- Setup (T001-T003) before all other phases
- Tests (T004-T013) before implementation (T014-T019)
- Utilities (T014-T017) before operator implementation (T018)
- Core implementation (T014-T018) before UI (T019)
- Core components (T014-T019) before integration (T020-T022)
- Integration (T020-T022) before polish (T023-T028)

## Parallel Example
```bash
# Phase 3.2: Launch all test tasks together
Task: "Lighting operator contract test in tests/integration/test_lighting_operator_contract.py"
Task: "Basic character lighting test in tests/integration/test_basic_character_lighting.py" 
Task: "Product visualization test in tests/integration/test_product_lighting.py"
Task: "Large scene object test in tests/integration/test_large_object_lighting.py"
Task: "Multiple objects test in tests/integration/test_multiple_objects.py"
Task: "No selection error test in tests/integration/test_no_selection_error.py"
Task: "Invalid object error test in tests/integration/test_invalid_object_error.py"
Task: "Wrong mode error test in tests/integration/test_wrong_mode_error.py"
Task: "Geometry utility tests in tests/unit/test_geometry_utils.py"
Task: "Validation utility tests in tests/unit/test_validation_utils.py"

# Phase 3.3: Launch utility implementations in parallel
Task: "Light configuration defaults in copilot/utils/light_defaults.py"
Task: "Geometry calculations in copilot/utils/geometry.py"
Task: "Object validation utilities in copilot/utils/validation.py"
Task: "Blender API helpers in copilot/utils/blender_helpers.py"
```

## Notes
- All tests MUST fail initially (TDD approach)
- Commit after each completed task
- Use exact file paths shown in task descriptions
- Follow constitutional principles: seamless integration, empowerment, action-oriented, Python-first, transparent
- Ensure all operations are undoable through Blender's standard undo system

## Validation Checklist
*GATE: Checked before marking tasks complete*

- [ ] All contract tests implemented and initially failing
- [ ] All entities from data model have corresponding utilities
- [ ] All quickstart scenarios have integration tests
- [ ] Operator follows exact contract specifications
- [ ] UI panel integrates with Blender's standard patterns
- [ ] Performance requirements met (sub-second execution)
- [ ] Constitutional compliance verified throughout
- [ ] No external dependencies introduced for core functionality