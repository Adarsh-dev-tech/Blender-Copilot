# Quickstart: Automated Three-Point Lighting Setup

## Overview
This guide demonstrates how to use the automated three-point lighting feature to quickly set up professional lighting for any object in Blender.

## Prerequisites
- Blender 3.0+ with Blender Copilot add-on installed
- Basic familiarity with Blender's object selection

## Quick Start Steps

### 1. Select Your Object
1. Open Blender with your 3D model/scene
2. Click on the object you want to light (e.g., character, product, sculpture)
3. Ensure the object is highlighted (active) in the 3D viewport

### 2. Access the Feature
**Option A: Natural Language Command**
1. Open the Copilot command interface
2. Type: `"create three-point lighting"` or `"light the selected object"`
3. Press Enter

**Option B: UI Panel**
1. In the 3D viewport, open the Properties panel (N key)
2. Find the "Copilot" tab
3. Locate the "Lighting Tools" section
4. Click "Create Three-Point Lighting" button

### 3. Verify Results
After execution, you should see:
- Three new area lights in your scene: "Key Light", "Fill Light", "Rim Light"
- One "Lighting Target" empty object at your object's center
- A new "Lighting Rig" collection in the Outliner containing all components
- Your object is now properly lit with professional three-point lighting

## Expected Results

### Light Positioning
- **Key Light**: Positioned 45° to the left, slightly above your object (primary illumination)
- **Fill Light**: Positioned 45° to the right, lower than key light (fills shadows)
- **Rim Light**: Positioned 135° behind object, elevated (creates edge definition)

### Light Properties
- **Key Light**: 100W power, daylight color temperature (5600K)
- **Fill Light**: 40W power, daylight color temperature (5600K), larger size
- **Rim Light**: 80W power, cooler color temperature (7000K), smaller size

### Automatic Behaviors
- All lights automatically point at your object (Track To constraints)
- Lights maintain focus even if you move the original object
- Professional intensity ratios create natural-looking illumination

## Testing Scenarios

### Scenario 1: Basic Character Lighting
1. **Setup**: Import or create a character model (e.g., Suzanne the monkey)
2. **Action**: Select the character, run `"create three-point lighting"`
3. **Expected**: Character is well-lit with clear key light, soft fill, and rim definition
4. **Validation**: Switch to rendered view mode - character should look professionally lit

### Scenario 2: Product Visualization
1. **Setup**: Create or import a product model (cube, bottle, etc.)
2. **Action**: Select the product, run `"light the selected object"`
3. **Expected**: Product has dramatic lighting suitable for marketing/presentation
4. **Validation**: Rotate the viewport - rim light should create nice edge highlights

### Scenario 3: Large Scene Object
1. **Setup**: Create a large object (scale default cube to 10x size)
2. **Action**: Select the large object, create lighting rig
3. **Expected**: Lights are positioned at appropriate distances from the large object
4. **Validation**: Lights should not be too close or too far from the object

### Scenario 4: Multiple Objects
1. **Setup**: Scene with multiple objects, select one as active
2. **Action**: Create three-point lighting
3. **Expected**: Lighting rig targets only the active object
4. **Validation**: Other objects may be lit incidentally but focus is on active object

## Error Handling Validation

### No Selection Error
1. **Setup**: Deselect all objects in the scene
2. **Action**: Attempt to create three-point lighting
3. **Expected**: Error message "No object selected. Please select an object to light."

### Invalid Object Error  
1. **Setup**: Select a camera or light object
2. **Action**: Attempt to create lighting rig
3. **Expected**: Error message about invalid object type

### Wrong Mode Error
1. **Setup**: Select a mesh, enter Edit mode
2. **Action**: Attempt to create lighting
3. **Expected**: Error message about requiring Object mode

## Success Criteria

### Visual Quality
- [ ] Object is clearly visible and well-lit
- [ ] Shadows are present but not too harsh (fill light working)
- [ ] Object edges are defined by rim light
- [ ] Overall lighting looks professional and balanced

### Technical Verification
- [ ] Exactly 3 lights created with correct names
- [ ] 1 empty object created at object center
- [ ] 1 collection created containing all components
- [ ] All lights have Track To constraints pointing at empty
- [ ] Lights are positioned according to three-point lighting principles

### Integration Verification
- [ ] Operation completes in under 1 second
- [ ] No error messages appear
- [ ] Undo operation reverses all changes
- [ ] Objects appear correctly in Outliner hierarchy

## Troubleshooting

### "Nothing happened"
- Verify object is selected (highlighted in viewport)
- Check you're in Object mode, not Edit mode
- Ensure Copilot add-on is enabled

### "Lights are too close/far"
- Feature automatically scales based on object size
- For very small/large objects, you may need to manually adjust distances
- This is expected behavior, not a bug

### "Lights not pointing at object"
- Verify the "Lighting Target" empty is at object center
- Check Track To constraints are properly applied
- Try moving the original object - lights should follow

### "Name conflicts"
- Feature automatically handles name conflicts by appending numbers
- Look for "Key Light.001", "Fill Light.001", etc.
- This is normal behavior when multiple rigs exist

## Advanced Usage

### Customizing the Rig
After creation, you can:
- Adjust individual light power/color in Properties panel
- Move lights to different positions (constraints will maintain pointing)
- Add additional lights to the rig collection
- Modify the target empty position to change focus point

### Working with Animation
- The lighting rig follows the target object automatically
- You can animate the target empty for dynamic lighting effects
- Individual lights can be animated independently

### Multiple Lighting Rigs
- Create separate rigs for different objects in the same scene
- Each rig is independent and self-contained
- Collections keep everything organized