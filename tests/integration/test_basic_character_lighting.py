import bpy
import unittest

class TestBasicCharacterLighting(unittest.TestCase):
    def setUp(self):
        # Setup: create a mesh object and set as active
        mesh = bpy.data.meshes.new('TestMesh')
        obj = bpy.data.objects.new('TestCharacter', mesh)
        bpy.context.collection.objects.link(obj)
        bpy.context.view_layer.objects.active = obj
        bpy.context.view_layer.update()

    def test_lighting_rig_creation(self):
        # Execute operator
        result = bpy.ops.copilot.create_three_point_lighting()
        self.assertIn(result, [{'FINISHED'}, {'CANCELLED'}])
        # Validate rig: 3 lights, 1 empty, 1 collection
        lights = [obj for obj in bpy.context.collection.objects if obj.type == 'LIGHT']
        empties = [obj for obj in bpy.context.collection.objects if obj.type == 'EMPTY']
        self.assertEqual(len(lights), 3)
        self.assertEqual(len(empties), 1)
        # Check collection
        self.assertTrue(any(coll.name.startswith('ThreePointRig') for coll in bpy.data.collections))
        # Check Track To constraints
        for light in lights:
            constraints = [c for c in light.constraints if c.type == 'TRACK_TO']
            self.assertTrue(len(constraints) > 0)

if __name__ == "__main__":
    unittest.main()
