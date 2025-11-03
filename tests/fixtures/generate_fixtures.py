"""
Generate test fixture .blend files for Modifier Assistant integration tests.

Run this script in Blender's scripting workspace to create the test fixtures.

Usage:
    1. Open Blender
    2. Switch to Scripting workspace
    3. Open this file
    4. Click "Run Script"
    
This will create 4 .blend files in the tests/fixtures/ directory.
"""

import bpy
import os
from pathlib import Path


def get_fixtures_dir():
    """Get the absolute path to tests/fixtures/ directory."""
    
    script_filepath_str = ""
    try:
        # Get path from the currently active text editor
        script_filepath_str = bpy.context.space_data.text.filepath
    except AttributeError:
        print("Could not find script path from 'bpy.context.space_data.text.filepath'.")
        print("Please make sure you are running this from the 'Scripting' workspace text editor.")
        raise

    if not script_filepath_str:
        print("ERROR: This script file is not saved to disk.")
        print("Please save this .py file (e.g., generate_fixtures.py) in your project's root directory and run it again.")
        raise ValueError("Script file must be saved to disk before running.")

    # Get the directory containing this script (e.g., the repo root)
    # bpy.path.abspath() makes sure we have a full, clean path
    script_dir = Path(bpy.path.abspath(script_filepath_str)).parent
    
    # The fixtures directory should be 'tests/fixtures' inside the script's dir
    fixtures_dir = script_dir / "tests" / "fixtures"
    
    # Ensure the directory exists BEFORE trying to save to it
    print(f"Fixtures will be saved to: {fixtures_dir}")
    fixtures_dir.mkdir(parents=True, exist_ok=True)
    
    return fixtures_dir


def clear_scene():
    """Delete all objects, meshes, materials, etc. from the current scene."""
    # Delete all objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Delete all mesh data
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)
    
    # Delete all materials
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)
        
    # Delete all curves
    for curve in bpy.data.curves:
        bpy.data.curves.remove(curve)


def create_single_cube():
    """Create fixture with one cube at origin."""
    clear_scene()
    
    # Add cube at origin
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
    cube = bpy.context.active_object
    cube.name = "TestCube"
    
    return "single_cube.blend"


def create_cube_and_empty():
    """Create fixture with one cube and one empty object."""
    clear_scene()
    
    # Add cube
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
    cube = bpy.context.active_object
    cube.name = "TestCube"
    
    # Deselect cube
    cube.select_set(False)
    
    # Add empty
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(2, 0, 0))
    empty = bpy.context.active_object
    empty.name = "ArrayController"
    
    return "cube_and_empty.blend"


def create_cube_and_curve():
    """Create fixture with one cube and one bezier curve."""
    clear_scene()
    
    # Add cube
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
    cube = bpy.context.active_object
    cube.name = "TestCube"
    
    # Deselect cube
    cube.select_set(False)
    
    # Add bezier curve
    bpy.ops.curve.primitive_bezier_curve_add(location=(0, 0, 0))
    curve = bpy.context.active_object
    curve.name = "DeformPath"
    
    # Modify curve to create a simple path
    # Curve should have some curvature for testing deformation
    curve_data = curve.data
    if len(curve_data.splines) > 0:
        spline = curve_data.splines[0]
        if len(spline.bezier_points) >= 2:
            # Move second point to create a curve
            spline.bezier_points[1].co = (3, 2, 0)
            spline.bezier_points[1].handle_left = (2, 1, 0)
            spline.bezier_points[1].handle_right = (4, 3, 0)
    
    return "cube_and_curve.blend"


def create_two_cubes():
    """Create fixture with two cubes side by side."""
    clear_scene()
    
    # Add first cube (will be source for shrinkwrap)
    bpy.ops.mesh.primitive_cube_add(location=(-1.5, 0, 0))
    cube1 = bpy.context.active_object
    cube1.name = "SourceCube"
    
    # Deselect first cube
    cube1.select_set(False)
    
    # Add second cube (will be target for shrinkwrap)
    bpy.ops.mesh.primitive_cube_add(location=(1.5, 0, 0))
    cube2 = bpy.context.active_object
    cube2.name = "TargetCube"
    
    # Scale second cube to make it bigger (better for shrinkwrap testing)
    cube2.scale = (1.5, 1.5, 1.5)
    
    return "two_cubes.blend"


def main():
    """Generate all test fixture files."""
    fixtures_dir = get_fixtures_dir()
    
    print("=" * 60)
    print("Generating Modifier Assistant Test Fixtures")
    print("=" * 60)
    
    fixtures = [
        ("single_cube.blend", create_single_cube),
        ("cube_and_empty.blend", create_cube_and_empty),
        ("cube_and_curve.blend", create_cube_and_curve),
        ("two_cubes.blend", create_two_cubes),
    ]
    
    created_files = []
    
    for filename, create_func in fixtures:
        print(f"\nCreating {filename}...")
        
        # Create the scene
        actual_filename = create_func()
        
        # Save the file
        filepath = fixtures_dir / actual_filename
        bpy.ops.wm.save_as_mainfile(filepath=str(filepath))
        
        print(f"  ✓ Saved to: {filepath}")
        created_files.append(filepath)
    
    print("\n" + "=" * 60)
    print("Fixture Generation Complete!")
    print("=" * 60)
    print(f"\nCreated {len(created_files)} fixture files:")
    for filepath in created_files:
        print(f"  - {filepath}")
    print("\nThese fixtures are ready for integration testing.")


if __name__ == "__main__":
    main()
