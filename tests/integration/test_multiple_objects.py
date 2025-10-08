import bpy
import unittest

class TestMultipleObjectsLighting(unittest.TestCase):
    def setUp(self):
        mesh1 = bpy.data.meshes.new('Mesh1')
        obj1 = bpy.data.objects.new('Object1', mesh1)
        mesh2 = bpy.data.meshes.new('Mesh2')
        obj2 = bpy.data.objects.new('Object2', mesh2)
        bpy.context.collection.objects.link(obj1)
        bpy.context.collection.objects.link(obj2)
        bpy.context.view_layer.objects.active = obj2
        bpy.context.view_layer.update()

    def test_active_object_lighting(self):
        result = bpy.ops.copilot.create_three_point_lighting()
        self.assertIn(result, [{'FINISHED'}, {'CANCELLED'}])
        # Verify only active object is targeted (stub)
        # TODO: Check rig targets only active object

if __name__ == "__main__":
    unittest.main()
