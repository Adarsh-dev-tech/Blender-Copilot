<!--
Sync Impact Report:
- Version change: Initial → 1.0.0
- New constitution created with 5 core principles
- Added sections: Core Principles, Development Standards, Quality Assurance, Governance
- Templates requiring updates: ✅ All templates reviewed for consistency
- Follow-up TODOs: None - all placeholders filled
-->

# Blender Copilot Constitution

## Core Principles

### I. Seamless Workflow Integration
The assistant MUST feel like a native part of Blender. It MUST be context-aware, understanding the user's current mode (Object, Edit, Sculpt), selection, and active objects to provide relevant, non-disruptive assistance. All operations MUST respect Blender's existing workflow patterns and interface conventions.

**Rationale**: User adoption depends on the tool feeling integrated rather than bolted-on. Context awareness prevents irrelevant suggestions and ensures the assistant understands the user's intent.

### II. Empowerment Over Automation
The primary goal is to augment the artist's creativity, not replace it. The Copilot MUST handle tedious, repetitive, and technical tasks (such as complex modifier setups or scripting), freeing the user to focus on creative decisions. The user MUST always remain the final artist with complete creative control.

**Rationale**: Artists value their creative agency. The tool should amplify human creativity by removing barriers, not by making creative decisions automatically.

### III. Action-Oriented and Practical
The assistant MUST have a bias for action. When a user makes a request, the preferred response is to perform an operation, generate a script, or provide direct, actionable steps, rather than just offering theoretical explanations. Every interaction SHOULD result in tangible progress toward the user's goal.

**Rationale**: Artists are focused on creation and results. Theoretical explanations without action create friction in the creative flow.

### IV. Python-First Foundation
Blender's power lies in its Python API (`bpy`). The Copilot MUST leverage this API as its primary means of performing operations. Generating and executing `bpy` scripts MUST be a core capability for automation and custom tool creation. All complex operations SHOULD be implementable through Python scripting.

**Rationale**: The Python API provides comprehensive access to all Blender functionality. Building on this foundation ensures maximum capability and consistency with Blender's architecture.

### V. Transparent and Auditable Actions
The user MUST have clarity on what the Copilot has done. Complex operations MUST be undoable and, where possible, broken down into visible steps in the modifier stack or as a logged script in the info panel. The assistant MUST NOT operate as a "black box" - all actions MUST be traceable and reversible.

**Rationale**: Trust requires transparency. Artists need to understand and potentially modify the assistant's work. Undoability preserves the iterative nature of creative work.

## Development Standards

### Technology Requirements
- **Primary Language**: Python 3.10+ (matching Blender's embedded Python)
- **Core API**: Blender Python API (`bpy`) for all Blender operations
- **UI Framework**: Blender's `bpy.types.Panel` and operator system for native integration
- **Testing Framework**: `unittest` or `pytest` for Python components
- **Code Quality**: PEP 8 compliance with Black formatting
- **Documentation**: All public APIs MUST include docstrings with examples

### Architecture Constraints
- All Copilot functionality MUST be implementable as Blender add-ons
- Core features MUST work in Blender's standard installation without external dependencies
- Optional advanced features MAY require additional Python packages with clear dependency management
- All operations MUST respect Blender's undo/redo system
- Memory usage MUST be optimized for large scenes and complex operations

## Quality Assurance

### Testing Requirements
- **Unit Tests**: All Python modules MUST have unit tests with >80% coverage
- **Integration Tests**: Key workflows MUST be tested within actual Blender instances
- **User Acceptance**: New features MUST be validated with representative artist workflows
- **Performance Testing**: Operations affecting large datasets MUST include performance benchmarks

### Code Review Standards
- All code changes MUST pass automated linting and formatting checks
- Complex algorithms MUST include performance analysis and optimization documentation
- User-facing features MUST include usability testing results
- Breaking changes MUST include migration guides and deprecation warnings

## Governance

### Amendment Process
This constitution governs all development decisions for Blender Copilot. Amendments require:
1. Documentation of proposed changes with rationale
2. Impact analysis on existing features and workflows
3. Community feedback period (minimum 7 days for minor changes, 14 days for major changes)
4. Implementation of necessary migration steps

### Version Control
- **MAJOR**: Backward incompatible changes to core principles or user workflows
- **MINOR**: New principles added or significant expansion of existing guidance
- **PATCH**: Clarifications, wording improvements, non-semantic refinements

### Compliance Review
All feature specifications, implementation plans, and code reviews MUST verify compliance with these principles. Any violations MUST be documented with explicit justification or the approach MUST be refactored to align with constitutional requirements.

**Version**: 1.0.0 | **Ratified**: 2025-10-04 | **Last Amended**: 2025-10-04