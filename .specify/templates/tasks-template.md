# Tasks: [FEATURE NAME]

**Input**: Design documents from `/specs/[###-feature-name]/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → If not found: ERROR "No implementation plan found"
   → Extract: tech stack, libraries, structure
2. Load optional design documents:
   → data-model.md: Extract entities → model tasks
   → contracts/: Each file → contract test task
   → research.md: Extract decisions → setup tasks
3. Generate tasks by category:
   → Setup: project init, dependencies, linting
   → Tests: contract tests, integration tests
   → Core: models, services, CLI commands
   → Integration: DB, middleware, logging
   → Polish: unit tests, performance, docs
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate task completeness:
   → All contracts have tests?
   → All entities have models?
   → All endpoints implemented?
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Blender Add-on**: `copilot/`, `tests/` at repository root
- **Multi-module Add-on**: `copilot/core/`, `copilot/ui/`, `copilot/operators/`
- **External Services**: `copilot/client/`, `external_service/src/`
- Paths shown below assume single add-on - adjust based on plan.md structure

## Phase 3.1: Setup
- [ ] T001 Create Blender add-on structure per implementation plan
- [ ] T002 Initialize add-on __init__.py with registration/unregistration
- [ ] T003 [P] Configure linting and formatting tools (Black, flake8)

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [ ] T004 [P] Operator contract test in tests/integration/test_operator_contracts.py
- [ ] T005 [P] Panel integration test in tests/integration/test_panel_integration.py
- [ ] T006 [P] Python script generation test in tests/integration/test_script_generation.py
- [ ] T007 [P] Context awareness test in tests/integration/test_context_awareness.py

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [ ] T008 [P] Base operator class in copilot/operators/base.py
- [ ] T009 [P] Property groups in copilot/props/copilot_props.py
- [ ] T010 [P] UI panels in copilot/panels/main_panel.py
- [ ] T011 Context detection utility in copilot/utils/context.py
- [ ] T012 Script generation engine in copilot/utils/script_generator.py
- [ ] T013 Blender API wrapper utilities in copilot/utils/bpy_utils.py
- [ ] T014 Error handling and undo integration

## Phase 3.4: Integration
- [ ] T015 Register all operators and panels in __init__.py
- [ ] T016 Add-on preferences integration
- [ ] T017 Script execution with undo support
- [ ] T018 Context-aware operation triggering

## Phase 3.5: Polish
- [ ] T019 [P] Unit tests for utilities in tests/unit/test_utils.py
- [ ] T020 Performance tests (UI responsiveness, large scenes)
- [ ] T021 [P] Update add-on documentation
- [ ] T022 Code cleanup and optimization
- [ ] T023 Manual testing with real Blender workflows

## Dependencies
- Tests (T004-T007) before implementation (T008-T014)
- T008 blocks T009, T015
- T016 blocks T018
- Implementation before polish (T019-T023)

## Parallel Example
```
# Launch T004-T007 together:
Task: "Operator contract test in tests/integration/test_operator_contracts.py"
Task: "Panel integration test in tests/integration/test_panel_integration.py"
Task: "Python script generation test in tests/integration/test_script_generation.py"
Task: "Context awareness test in tests/integration/test_context_awareness.py"
```

## Notes
- [P] tasks = different files, no dependencies
- Verify tests fail before implementing
- Commit after each task
- Avoid: vague tasks, same file conflicts

## Task Generation Rules
*Applied during main() execution*

1. **From Contracts**:
   - Each contract file → contract test task [P]
   - Each endpoint → implementation task
   
2. **From Data Model**:
   - Each property group → model creation task [P]
   - Blender data relationships → utility function tasks
   
3. **From User Stories**:
   - Each workflow → integration test [P]
   - UI interaction scenarios → panel/operator tests

4. **Ordering**:
   - Setup → Tests → Properties → Operators → Panels → Utils → Polish
   - Dependencies block parallel execution

## Validation Checklist
*GATE: Checked by main() before returning*

- [ ] All operators have corresponding tests
- [ ] All panels have integration tests
- [ ] All tests come before implementation
- [ ] Parallel tasks truly independent
- [ ] Each task specifies exact file path
- [ ] No task modifies same file as another [P] task
- [ ] Add-on registration/unregistration handled
- [ ] Blender API compatibility verified