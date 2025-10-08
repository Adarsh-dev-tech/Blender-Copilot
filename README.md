# Blender Copilot: Automated Three-Point Lighting Add-on

## Overview
Blender Copilot is a professional Blender add-on that automates the creation of cinematic three-point lighting rigs for any selected object. Designed for artists, product visualizers, and animators, it eliminates the manual process of positioning and configuring lights, ensuring fast, consistent, and professional results with a single click.

## Features
- **One-Click Lighting:** Instantly create a three-point lighting setup for any supported object.
- **Professional Positioning:** Key, fill, and rim lights are placed using industry-standard angles and ratios.
- **Automatic Object Analysis:** Lights are positioned and scaled based on object geometry and size.
- **Customizable:** Adjust light angles and distances via operator properties (F9 menu).
- **Organized Collections:** All rig components are grouped in a dedicated collection for easy management.
- **Undo/Redo Support:** All operations are fully undoable using Blender's standard system.
- **Error Handling:** Clear, actionable error messages for unsupported scenarios.
- **Performance Optimized:** Sub-second execution, even for complex scenes.
- **Comprehensive Testing:** Includes unit, integration, and performance tests.

## Installation
### 1. Install from Source (Development)
1. Open Blender and go to `Edit > Preferences > Add-ons`.
2. Click `Install...` and select the `copilot` folder from your project directory.
3. Enable "Blender Copilot - Automated Three-Point Lighting" in the add-ons list.
4. Save preferences if desired.

### 2. Install from ZIP (Distribution)
1. Zip the `copilot` folder (must contain `__init__.py`).
2. In Blender, go to `Edit > Preferences > Add-ons > Install...` and select the ZIP file.
3. Enable the add-on as above.

## Usage
1. Select a supported object (Mesh, Curve, Surface, Meta, or Font) in Object Mode.
2. Open the 3D Viewport sidebar (`N` key) and go to the `Copilot` tab.
3. Click "Create Three-Point Lighting".
4. Optionally, press `F9` to adjust angles and distance scale.
5. Lights, empty target, and collection are created and organized automatically.

## Supported Object Types
- Mesh
- Curve
- Surface
- Meta
- Font

## Advanced Options
- **Key Light Angle:** Horizontal angle for key light (default: 45°)
- **Fill Light Angle:** Horizontal angle for fill light (default: -45°)
- **Rim Light Angle:** Horizontal angle for rim light (default: 135°)
- **Distance Scale:** Multiplier for light distances (default: 1.0)

## Error Handling
- No object selected: "No object selected" error
- Wrong mode: "Must be in Object Mode" error
- Invalid object type: "Object type not supported" error
- Permission errors and geometry analysis failures are reported with details

## Manual Testing Procedures
See [`tests/manual/test_procedures.md`](tests/manual/test_procedures.md) for a full checklist covering:
- Basic functionality
- Multiple object types
- Error handling
- Customization
- Complex geometry
- Scene integration
- Undo/redo
- Performance
- UI/UX
- Edge cases

## Performance Benchmarks
See [`tests/performance/test_benchmarks.py`](tests/performance/test_benchmarks.py) for automated performance and memory usage tests.

## Development
- Code is organized by feature: `copilot/operators/`, `copilot/panels/`, `copilot/utils/`
- Utilities for geometry, validation, Blender API, performance, and user feedback
- All functions and classes are documented with docstrings and usage examples
- TDD workflow: All tests written before implementation

## Contributing
Pull requests and issues are welcome! Please follow the project constitution and coding standards. See [`specs/001-automated-three-point/constitution.md`](specs/001-automated-three-point/constitution.md) for governance principles.

## License
MIT License. See [`LICENSE`](LICENSE) for details.

## Author
Adarsh Hinsodiya

## Links
- [GitHub Repository](https://github.com/Adarsh-dev-tech/Blender-Copilot)
- [Issue Tracker](https://github.com/Adarsh-dev-tech/Blender-Copilot/issues)

## Acknowledgements
- Blender Foundation
- Community contributors

---
For questions, feedback, or support, open an issue on GitHub or contact the author via the repository.
