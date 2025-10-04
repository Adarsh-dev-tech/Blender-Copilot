# Blender Copilot Development Guidelines

Auto-generated from all feature plans. Last updated: [DATE]

## Active Technologies
- **Primary Language**: Python 3.10+ (Blender embedded Python)
- **Core API**: Blender Python API (`bpy`)
- **UI Framework**: `bpy.types.Panel`, `bpy.types.Operator`
- **Testing**: `unittest`/`pytest` with Blender test environment
- **Add-on Architecture**: Standard Blender add-on structure

## Project Structure
```
copilot/
├── __init__.py          # Add-on registration
├── operators/           # Blender operators (actions)
├── panels/             # UI panels
├── props/              # Property groups
├── utils/              # Utility functions
└── bpy_scripts/        # Generated/template scripts

tests/
├── integration/        # Tests requiring Blender instance
├── unit/              # Pure Python unit tests
└── fixtures/          # Test scene files
```

## Constitutional Requirements
- **Seamless Integration**: All UI must use Blender's native panel/operator system
- **Context Awareness**: Always check `bpy.context` for current mode, selection, objects
- **Python-First**: Core functionality through `bpy` API, generate scripts for complex operations
- **Transparency**: Log actions in info panel, ensure operations are undoable
- **Empowerment**: Handle technical tasks, preserve user creative control

## Development Commands
- **Add-on Installation**: Copy to Blender's add-ons directory, enable in preferences
- **Testing**: Run tests with Blender's background mode: `blender --background --python-expr "import pytest; pytest.main()"`
- **Debugging**: Use Blender's Console and Info panels for debugging
- **Script Testing**: Test generated scripts in Blender's Text Editor

## Code Style
- **Python Style**: PEP 8 compliance, Black formatting
- **Blender Conventions**: Follow Blender's operator/panel naming conventions
- **Documentation**: Docstrings for all operators, panels, and utilities
- **Error Handling**: Graceful degradation, user-friendly error messages

## Recent Changes
[LAST 3 FEATURES AND WHAT THEY ADDED]

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->