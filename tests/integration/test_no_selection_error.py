import bpy
import unittest

class TestNoSelectionError(unittest.TestCase):
    def setUp(self):
        bpy.context.view_layer.objects.active = None
        bpy.context.view_layer.update()

    def test_no_selection_error(self):
        result = bpy.ops.copilot.create_three_point_lighting()
        self.assertEqual(result, {'CANCELLED'})
        # TODO: Check error message displayed

if __name__ == "__main__":
    unittest.main()
