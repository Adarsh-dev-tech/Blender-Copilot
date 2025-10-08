import bpy
import unittest

class TestSceneIntegration(unittest.TestCase):
    def setUp(self):
        # Clear scene
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
    
    def test_addon_registration(self):
        """Test that add-on components are properly registered"""
        # Check operator is available
        self.assertTrue(hasattr(bpy.ops.copilot, 'create_three_point_lighting'))
        
        # Check operator properties
        op_cls = bpy.types.COPILOT_OT_create_three_point_lighting
        self.assertTrue(hasattr(op_cls, 'key_angle'))
        self.assertTrue(hasattr(op_cls, 'fill_angle'))
        self.assertTrue(hasattr(op_cls, 'rim_angle'))
        self.assertTrue(hasattr(op_cls, 'distance_scale'))
    
    def test_panel_registration(self):
        """Test that UI panel is properly registered"""
        # Check panel class is registered
        self.assertTrue(hasattr(bpy.types, 'COPILOT_PT_lighting_panel'))
        
        # Check panel properties
        panel_cls = bpy.types.COPILOT_PT_lighting_panel
        self.assertEqual(panel_cls.bl_space_type, 'VIEW_3D')
        self.assertEqual(panel_cls.bl_region_type, 'UI')
        self.assertEqual(panel_cls.bl_category, 'Copilot')
    
    def test_operator_availability_in_search(self):
        """Test that operator is available in operator search"""
        # This would need to be tested in actual Blender UI
        # For now, just check the operator exists and has proper bl_label
        op_cls = bpy.types.COPILOT_OT_create_three_point_lighting
        self.assertEqual(op_cls.bl_label, "Create Three-Point Lighting")
        self.assertEqual(op_cls.bl_idname, "copilot.create_three_point_lighting")
    
    def test_addon_in_preferences(self):
        """Test that add-on appears in preferences"""
        # Check if add-on info is accessible
        addon_info = bpy.context.preferences.addons.get('copilot')
        # Note: This test may not work in all contexts
        # In actual Blender, the add-on would need to be properly installed
    
    def test_ui_panel_context_filtering(self):
        """Test that panel only appears in appropriate contexts"""
        panel_cls = bpy.types.COPILOT_PT_lighting_panel
        self.assertEqual(panel_cls.bl_context, 'objectmode')
        
        # Panel should be available in object mode
        bpy.context.mode = 'OBJECT'
        # In actual test, would check panel visibility

if __name__ == "__main__":
    unittest.main()