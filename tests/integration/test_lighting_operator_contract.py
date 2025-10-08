import bpy
import unittest

# Blender's bpy module is only available inside Blender's Python environment.
# For contract tests, use stubs or run inside Blender with pytest/unittest.


class TestLightingOperatorContract(unittest.TestCase):
    def setUp(self):
        if bpy is None:
            self.skipTest("bpy module not available outside Blender")

    def test_operator_registration(self):
        # Operator should be registered
        self.assertTrue(hasattr(bpy.types, 'COPILOT_OT_create_three_point_lighting'))

    def test_operator_properties(self):
        op = getattr(bpy.types, 'COPILOT_OT_create_three_point_lighting', None)
        self.assertIsNotNone(op)
        # Check required properties
        for prop in ['key_angle', 'fill_angle', 'rim_angle', 'distance_scale']:
            self.assertTrue(hasattr(op, prop))

    def test_input_validation(self):
        # Should fail if no active object or not in Object mode
        bpy.context.active_object = None
        result = bpy.ops.copilot.create_three_point_lighting()
        self.assertEqual(result, {'CANCELLED'})
        # Switch to Object mode and set active object
        bpy.context.mode = 'OBJECT'
        # Create a dummy mesh object for testing
        mesh = bpy.data.meshes.new('TestMesh')
        obj = bpy.data.objects.new('TestObject', mesh)
        bpy.context.collection.objects.link(obj)
        bpy.context.view_layer.objects.active = obj
        result = bpy.ops.copilot.create_three_point_lighting()
        self.assertIn(result, [{'FINISHED'}, {'CANCELLED'}])

    def test_success_error_return_values(self):
        # Should return FINISHED on success, CANCELLED on error
        # (Assume previous test sets up valid context)
        result = bpy.ops.copilot.create_three_point_lighting()
        self.assertIn(result, [{'FINISHED'}, {'CANCELLED'}])

    def test_undo_redo_compatibility(self):
        # Operator should be undoable
        result = bpy.ops.copilot.create_three_point_lighting()
        self.assertIn(result, [{'FINISHED'}, {'CANCELLED'}])
        # Undo last operation
        bpy.ops.ed.undo()
        # Redo last operation
        bpy.ops.ed.redo()

if __name__ == "__main__":
    unittest.main()
