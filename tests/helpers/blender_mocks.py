"""
Test helpers for mocking Blender context in unit tests.

This module provides mock classes and utilities for testing Blender add-on code
without requiring a full Blender instance.
"""

from typing import List, Optional, Dict, Any
from unittest.mock import MagicMock


class MockModifier:
    """Mock Blender modifier object."""
    
    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type
        # Common modifier properties
        self.show_viewport = True
        self.show_render = True
        
    def __repr__(self):
        return f"MockModifier(name='{self.name}', type='{self.type}')"


class MockModifierList:
    """Mock collection of modifiers (mimics bpy.types.ObjectModifiers)."""
    
    def __init__(self):
        self._modifiers: List[MockModifier] = []
    
    def new(self, name: str, type: str) -> MockModifier:
        """Add a new modifier to the object."""
        modifier = MockModifier(name, type)
        self._modifiers.append(modifier)
        return modifier
    
    def remove(self, modifier: MockModifier):
        """Remove a modifier from the object."""
        self._modifiers.remove(modifier)
    
    def clear(self):
        """Remove all modifiers."""
        self._modifiers.clear()
    
    def __getitem__(self, key):
        """Get modifier by name or index."""
        if isinstance(key, int):
            return self._modifiers[key]
        # Find by name
        for mod in self._modifiers:
            if mod.name == key:
                return mod
        raise KeyError(f"Modifier '{key}' not found")
    
    def __len__(self):
        return len(self._modifiers)
    
    def __iter__(self):
        return iter(self._modifiers)


class MockObject:
    """Mock Blender object."""
    
    def __init__(self, name: str, obj_type: str = 'MESH'):
        self.name = name
        self.type = obj_type
        self.modifiers = MockModifierList()
        self.location = (0.0, 0.0, 0.0)
        self.rotation_euler = (0.0, 0.0, 0.0)
        self.scale = (1.0, 1.0, 1.0)
        self.data = MagicMock()  # Mock mesh/curve data
        self.select_set = MagicMock()
        
    def __repr__(self):
        return f"MockObject(name='{self.name}', type='{self.type}')"


class MockBlenderContext:
    """Mock Blender context (mimics bpy.context)."""
    
    def __init__(self):
        self.selected_objects: List[MockObject] = []
        self.active_object: Optional[MockObject] = None
        self.mode = 'OBJECT'
        self.scene = MagicMock()
        self.view_layer = MagicMock()
        
    def __repr__(self):
        return (f"MockBlenderContext(selected={len(self.selected_objects)}, "
                f"active={self.active_object.name if self.active_object else None}, "
                f"mode='{self.mode}')")


def create_mock_scene(
    num_meshes: int = 0,
    num_empties: int = 0,
    num_curves: int = 0,
    with_active: bool = True
) -> MockBlenderContext:
    """
    Create a mock Blender scene with specified objects.
    
    Args:
        num_meshes: Number of mesh objects to create
        num_empties: Number of empty objects to create
        num_curves: Number of curve objects to create
        with_active: If True, set first object as active
        
    Returns:
        MockBlenderContext with specified objects selected
    """
    context = MockBlenderContext()
    
    # Create mesh objects
    for i in range(num_meshes):
        obj = MockObject(f"Mesh{i+1}", 'MESH')
        context.selected_objects.append(obj)
    
    # Create empty objects
    for i in range(num_empties):
        obj = MockObject(f"Empty{i+1}", 'EMPTY')
        context.selected_objects.append(obj)
    
    # Create curve objects
    for i in range(num_curves):
        obj = MockObject(f"Curve{i+1}", 'CURVE')
        context.selected_objects.append(obj)
    
    # Set active object
    if with_active and context.selected_objects:
        context.active_object = context.selected_objects[0]
    
    return context


def assert_modifier_exists(obj: MockObject, modifier_name: str) -> bool:
    """
    Assert that a modifier with the given name exists on the object.
    
    Args:
        obj: Mock object to check
        modifier_name: Name of modifier to find
        
    Returns:
        True if modifier exists
        
    Raises:
        AssertionError: If modifier not found
    """
    modifier_names = [mod.name for mod in obj.modifiers]
    assert modifier_name in modifier_names, \
        f"Modifier '{modifier_name}' not found. Available: {modifier_names}"
    return True


def assert_modifier_type(obj: MockObject, modifier_name: str, expected_type: str) -> bool:
    """
    Assert that a modifier has the expected type.
    
    Args:
        obj: Mock object to check
        modifier_name: Name of modifier to check
        expected_type: Expected modifier type (e.g., 'ARRAY', 'BEVEL')
        
    Returns:
        True if type matches
        
    Raises:
        AssertionError: If type doesn't match
    """
    assert_modifier_exists(obj, modifier_name)
    modifier = obj.modifiers[modifier_name]
    assert modifier.type == expected_type, \
        f"Modifier '{modifier_name}' type is '{modifier.type}', expected '{expected_type}'"
    return True


def assert_modifier_order(obj: MockObject, expected_order: List[str]) -> bool:
    """
    Assert that modifiers are in the expected order.
    
    Args:
        obj: Mock object to check
        expected_order: List of modifier names in expected order
        
    Returns:
        True if order matches
        
    Raises:
        AssertionError: If order doesn't match
    """
    actual_order = [mod.name for mod in obj.modifiers]
    assert actual_order == expected_order, \
        f"Modifier order mismatch. Expected: {expected_order}, Got: {actual_order}"
    return True


def get_object_type_counts(context: MockBlenderContext) -> Dict[str, int]:
    """
    Get count of each object type in selection.
    
    Args:
        context: Mock Blender context
        
    Returns:
        Dictionary mapping object type to count (e.g., {'MESH': 2, 'EMPTY': 1})
    """
    type_counts: Dict[str, int] = {}
    for obj in context.selected_objects:
        type_counts[obj.type] = type_counts.get(obj.type, 0) + 1
    return type_counts


# Example usage for testing
if __name__ == "__main__":
    # Create a scene with 1 mesh and 1 empty
    ctx = create_mock_scene(num_meshes=1, num_empties=1)
    print(ctx)
    print(f"Selected objects: {ctx.selected_objects}")
    print(f"Active object: {ctx.active_object}")
    
    # Add a modifier to the mesh
    mesh = ctx.selected_objects[0]
    array_mod = mesh.modifiers.new("Array", "ARRAY")
    print(f"Added modifier: {array_mod}")
    
    # Test assertions
    assert_modifier_exists(mesh, "Array")
    assert_modifier_type(mesh, "Array", "ARRAY")
    print("✓ All assertions passed")
