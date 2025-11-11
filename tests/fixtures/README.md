# Test Fixtures for Modifier Assistant

This directory contains Blender scene files (.blend) used for integration testing.

## Generating Fixtures

The fixtures need to be generated using Blender's Python API. To create them:

### Method 1: Run in Blender UI
1. Open Blender 3.0 or newer
2. Switch to the "Scripting" workspace
3. Open `generate_fixtures.py` in the text editor
4. Click "Run Script" button
5. Check the console output - 4 .blend files will be created in this directory

### Method 2: Run from Command Line
```bash
# From repository root
blender --background --python tests/fixtures/generate_fixtures.py
```

## Fixture Files

After generation, you should have these files:

### single_cube.blend
- **Contents**: One cube object at origin
- **Used for**: Smart Array (single object), Hard-Surface SubD, Symmetrize, Solidify workflows
- **Objects**: "TestCube" (MESH)

### cube_and_empty.blend
- **Contents**: One cube + one empty object
- **Used for**: Smart Array with object offset control
- **Objects**: 
  - "TestCube" (MESH) at (0, 0, 0)
  - "ArrayController" (EMPTY) at (2, 0, 0)

### cube_and_curve.blend
- **Contents**: One cube + one bezier curve
- **Used for**: Curve Deform workflow
- **Objects**:
  - "TestCube" (MESH) at (0, 0, 0)
  - "DeformPath" (CURVE) - curved path for deformation testing

### two_cubes.blend
- **Contents**: Two cubes side by side
- **Used for**: Shrinkwrap workflow
- **Objects**:
  - "SourceCube" (MESH) at (-1.5, 0, 0)
  - "TargetCube" (MESH) at (1.5, 0, 0) - scaled 1.5x

## Testing Without Generated Fixtures

If you cannot generate fixtures, integration tests should handle missing files gracefully by:
1. Creating objects programmatically in the test
2. Skipping tests that require specific .blend files
3. Providing clear error messages about missing fixtures

## Regenerating Fixtures

If test requirements change, update `generate_fixtures.py` and regenerate:
```bash
cd /path/to/Blender-Copilot
blender --background --python tests/fixtures/generate_fixtures.py
```

## File Sizes

Each .blend file should be < 1MB (they contain minimal geometry).
All fixtures together should be < 5MB total.
