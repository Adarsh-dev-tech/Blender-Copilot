
# Implementation Plan: Automated Three-Point Lighting Setup

**Branch**: `001-automated-three-point` | **Date**: 2025-10-04 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/home/adarsh-hinsodiya/Projects/Blender-Copilot/specs/001-automated-three-point/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from file system structure or context (web=frontend+backend, mobile=app+api)
   → Set Structure Decision based on project type
3. Fill the Constitution Check section based on the content of the constitution document.
4. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
5. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
6. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file (e.g., `CLAUDE.md` for Claude Code, `.github/copilot-instructions.md` for GitHub Copilot, `GEMINI.md` for Gemini CLI, `QWEN.md` for Qwen Code, or `AGENTS.md` for all other agents).
7. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
8. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
9. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
**Primary Requirement**: Create a fast, one-command way to set up a standard three-point lighting rig that automatically aims at a selected object, eliminating the manual process of creating, positioning, and configuring three individual lights.

**Technical Approach**: Develop a Blender operator that processes natural language commands, validates object selection, creates three Area Lights with appropriate positioning and Track To constraints, organizes components in a collection, and provides user feedback through Blender's native interface systems.

## Technical Context
**Language/Version**: Python 3.10+ (Blender embedded Python)  
**Primary Dependencies**: Blender Python API (`bpy`), Blender UI framework (`bpy.types.Panel`, `bpy.types.Operator`), `mathutils` for spatial calculations  
**Storage**: Blender scene data (objects, constraints, collections), no external storage required  
**Testing**: `unittest` with Blender test environment, integration tests requiring Blender instance  
**Target Platform**: Blender 3.0+ cross-platform (Windows, macOS, Linux)  
**Project Type**: Blender add-on (determines addon structure)  
**Performance Goals**: Sub-second lighting rig creation, real-time UI responsiveness, handle objects up to 10k vertices efficiently  
**Constraints**: Blender Python API limitations, undo/redo system compatibility, collection naming conflicts  
**Scale/Scope**: Single-user tool, supports complex scenes with multiple objects, 3-light configuration only

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**I. Seamless Workflow Integration**: Does the feature respect Blender's workflow patterns and maintain context awareness?
- [x] Feature integrates with Blender's existing UI/UX patterns
- [x] Operations are context-aware (current mode, selection, active objects)
- [x] No disruption to standard Blender workflows

**II. Empowerment Over Automation**: Does the feature augment rather than replace artistic decision-making?
- [x] User maintains creative control at all times
- [x] Focus on handling technical/repetitive tasks
- [x] No automatic creative decisions without user approval

**III. Action-Oriented and Practical**: Does the feature prioritize actionable results over theoretical explanations?
- [x] Every user interaction results in tangible progress
- [x] Bias toward performing operations rather than describing them
- [x] Direct, actionable responses provided

**IV. Python-First Foundation**: Does the feature leverage Blender's Python API as the primary mechanism?
- [x] Core functionality implemented through `bpy` API
- [x] Script generation capability for complex operations
- [x] Python scripting as foundation for automation

**V. Transparent and Auditable Actions**: Are all operations visible, traceable, and reversible?
- [x] Operations are undoable through Blender's undo system
- [x] Complex operations broken into visible steps
- [x] Scripts logged in info panel for transparency
- [x] No "black box" behavior

**Development Standards Check**:
- [x] Python 3.10+ compatibility maintained
- [x] Blender add-on architecture followed
- [x] No external dependencies for core features
- [x] Performance optimized for large scenes

## Project Structure

### Documentation (this feature)
```
specs/[###-feature]/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
copilot/
├── __init__.py          # Add-on registration
├── operators/           # Blender operators (actions)
│   └── lighting.py      # Three-point lighting operator
├── panels/             # UI panels  
│   └── lighting_panel.py # UI panel for lighting commands
├── utils/              # Utility functions
│   ├── geometry.py      # Spatial calculations and positioning
│   └── validation.py    # Object selection validation
└── bpy_scripts/        # Generated/template scripts
    └── lighting_templates/ # Pre-built lighting scripts

tests/
├── integration/        # Tests requiring Blender instance
│   ├── test_lighting_operator.py
│   └── test_lighting_panel.py
├── unit/              # Pure Python unit tests
│   ├── test_geometry_utils.py
│   └── test_validation_utils.py
└── fixtures/          # Test scene files
    ├── simple_object.blend
    ├── complex_scene.blend
    └── no_selection.blend
```

**Structure Decision**: Single Blender Add-on structure chosen as this is a focused feature within the larger Blender Copilot system. The feature requires operator logic, UI panels, utility functions for calculations, and comprehensive testing with actual Blender scenes.

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Phase 0: Outline & Research ✅ COMPLETED
**Output**: research.md with all technical decisions resolved

**Research Topics Completed**:
1. **Blender Python API**: Confirmed `bpy.data.lights.new()` and object creation patterns
2. **Object Selection**: Validated `bpy.context.active_object` approach for target identification  
3. **Track To Constraints**: Established `obj.constraints.new(type='TRACK_TO')` implementation
4. **Three-Point Positioning**: Defined spherical coordinate system with cinema-standard angles
5. **Collection Organization**: Confirmed `bpy.data.collections.new()` for scene organization
6. **Error Handling**: Validated `self.report()` pattern for user feedback
7. **Light Properties**: Established professional default values for power and color temperature

**Key Decisions Made**:
- Use Blender's native area lights with Track To constraints
- Position lights using spherical coordinates relative to object bounding box
- Organize components in collections for clean scene management
- Follow Blender operator patterns for UI integration and error handling

## Phase 1: Design & Contracts ✅ COMPLETED
**Output**: data-model.md, contracts/lighting_operator.md, quickstart.md

**Design Artifacts Created**:

1. **Data Model** (`data-model.md`):
   - LightingRig entity (complete lighting setup)
   - LightConfiguration entity (individual light properties)
   - TargetObject entity (selected object wrapper)
   - TrackToConstraint entity (automatic aiming)
   - BlenderCollection entity (scene organization)
   - Default value configurations and validation rules

2. **Operator Contract** (`contracts/lighting_operator.md`):
   - Complete operator interface definition
   - Input/output contracts with validation
   - Error handling specifications
   - Performance and compatibility requirements
   - Integration contracts for UI and command systems

3. **User Guide** (`quickstart.md`):
   - Step-by-step usage instructions
   - Expected results and validation criteria
   - Testing scenarios and error handling examples
   - Troubleshooting guide and advanced usage tips

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `.specify/templates/tasks-template.md` as base
- Generate tasks from Phase 1 design docs (contracts, data model, quickstart)
- Each contract → contract test task [P]
- Each entity → model creation task [P] 
- Each user story → integration test task
- Implementation tasks to make tests pass

**Ordering Strategy**:
- TDD order: Tests before implementation 
- Dependency order: Models before services before UI
- Mark [P] for parallel execution (independent files)

**Estimated Output**: 25-30 numbered, ordered tasks in tasks.md

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `lighting_operator.md` contract → Generate operator implementation task [P]
- Load `data-model.md` entities → Generate utility function tasks [P]
- Load `quickstart.md` scenarios → Generate integration test tasks [P]
- Generate UI panel task for command interface
- Generate comprehensive test suite covering all error conditions

**Ordering Strategy**:
- TDD order: Contract tests before operator implementation
- Dependency order: Utilities before operator before panel before integration
- Mark [P] for parallel execution where files are independent

**Estimated Task Breakdown**:
1. **Setup Tasks** (3-4 tasks): Project structure, dependencies, linting
2. **Test-First Tasks** (6-8 tasks): Contract tests, utility tests, integration tests  
3. **Core Implementation** (5-7 tasks): Geometry utils, validation utils, operator class, panel class
4. **Integration Tasks** (3-4 tasks): Add-on registration, command mapping, error handling
5. **Polish Tasks** (4-5 tasks): Performance optimization, documentation, manual testing

**Estimated Output**: 21-28 numbered, ordered tasks in tasks.md

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)  
**Phase 4**: Implementation (execute tasks.md following constitutional principles)  
**Phase 5**: Validation (run tests, execute quickstart.md, performance validation)

## Complexity Tracking
*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |


## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command)
- [x] Phase 1: Design complete (/plan command)
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS
- [x] Post-Design Constitution Check: PASS
- [x] All NEEDS CLARIFICATION resolved
- [x] Complexity deviations documented (none required)

---
*Based on Constitution v1.0.0 - See `/memory/constitution.md`*
