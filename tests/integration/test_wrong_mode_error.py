import bpy
import unittest

class TestWrongModeError(unittest.TestCase):
    def setUp(self):
        mesh = bpy.data.meshes.new('TestMesh')
        obj = bpy.data.objects.new('TestObject', mesh)
        bpy.context.collection.objects.link(obj)
        bpy.context.view_layer.objects.active = obj
        bpy.context.view_layer.update()
        bpy.ops.object.mode_set(mode='EDIT')

    def test_wrong_mode_error(self):
        result = bpy.ops.copilot.create_three_point_lighting()
        self.assertEqual(result, {'CANCELLED'})
        # TODO: Check error message for wrong mode

if __name__ == "__main__":
    unittest.main()
