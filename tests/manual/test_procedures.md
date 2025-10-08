# Manual Testing Procedures - Blender Copilot Three-Point Lighting

## Prerequisites
- Blender 3.0 or higher installed
- Blender Copilot add-on installed and enabled
- Basic knowledge of Blender interface

## Test Environment Setup

### 1. Fresh Blender Session
1. Start Blender with factory settings (File > Defaults > Load Factory Settings)
2. Confirm add-on is enabled (Edit > Preferences > Add-ons > Search "Copilot")
3. Verify "Copilot" tab appears in 3D Viewport sidebar (N key)

### 2. Test Scene Preparation
1. Delete default cube (X key > Delete)
2. Create test objects for various scenarios

## Core Functionality Tests

### Test 1: Basic Mesh Object Lighting
**Objective**: Verify basic functionality with a simple mesh

**Setup**:
1. Add mesh object (Shift+A > Mesh > Monkey/Suzanne)
2. Keep object selected and in Object Mode

**Procedure**:
1. Open 3D Viewport sidebar (N key)
2. Navigate to "Copilot" tab
3. Verify panel shows "Ready for: Suzanne" status
4. Click "Create Three-Point Lighting" button

**Expected Results**:
- ✅ Three area lights created (Key_Light, Fill_Light, Rim_Light)
- ✅ One empty object created (LightTarget_Suzanne)
- ✅ Collection created (ThreePointRig_Suzanne)
- ✅ All objects organized in collection
- ✅ Lights properly aimed at target object
- ✅ Success message displayed
- ✅ Operation completes in under 1 second

**Visual Verification**:
- Key light positioned at 45° from front-right
- Fill light positioned at -45° from front-left
- Rim light positioned at 135° from back-right
- All lights have Track To constraints pointing at empty
- Lighting appears professional and balanced

### Test 2: Multiple Object Types
**Objective**: Test with different supported object types

**Test Cases**:
1. **Curve Object**: Add Bezier curve, test lighting creation
2. **Text Object**: Add text object, test lighting creation  
3. **Surface Object**: Add NURBS surface, test lighting creation
4. **Metaball**: Add metaball, test lighting creation

**Procedure** (for each type):
1. Add object type
2. Select object, ensure Object Mode
3. Execute lighting operator
4. Verify successful creation

### Test 3: Error Handling
**Objective**: Verify proper error messages and prevention

**Test 3.1: No Selection**
1. Deselect all objects (Alt+A)
2. Attempt to create lighting
3. **Expected**: "No object selected" error message

**Test 3.2: Wrong Mode**
1. Select mesh object
2. Enter Edit Mode (Tab)
3. Attempt to create lighting
4. **Expected**: "Must be in Object Mode" error message

**Test 3.3: Invalid Object Type**
1. Add camera (Shift+A > Camera)
2. Select camera
3. Attempt to create lighting
4. **Expected**: "Object type 'CAMERA' not supported" error

**Test 3.4: Multiple Objects Selected**
1. Add two mesh objects
2. Select both (Shift+click)
3. Set one as active
4. Create lighting
5. **Expected**: Lighting created for active object only

### Test 4: Customization Options
**Objective**: Test operator property customization

**Procedure**:
1. Select mesh object
2. Execute operator: `bpy.ops.copilot.create_three_point_lighting()`
3. Press F9 to open operator properties
4. Adjust angles: Key=30°, Fill=-60°, Rim=120°
5. Adjust distance scale to 1.5
6. Confirm changes

**Expected Results**:
- Lights reposition according to new angles
- Distance from object increases with scale factor
- Changes apply immediately

## Advanced Testing

### Test 5: Complex Geometry
**Objective**: Test with complex objects

**Test Objects**:
1. High-poly mesh (subdivided monkey)
2. Very large object (scaled up 10x)
3. Very small object (scaled down 0.1x)
4. Non-uniform scaled object

**Verification**:
- Lighting scales appropriately to object size
- Performance remains acceptable
- Bounding box calculation accurate

### Test 6: Scene Integration
**Objective**: Test in complex scenes

**Setup**:
1. Create scene with multiple objects
2. Existing lighting and collections
3. Custom materials and textures

**Procedure**:
1. Add lighting to object in complex scene
2. Verify no interference with existing elements
3. Check collection organization

### Test 7: Undo/Redo System
**Objective**: Verify undo system integration

**Procedure**:
1. Create lighting rig
2. Perform undo (Ctrl+Z)
3. Verify all components removed
4. Perform redo (Ctrl+Shift+Z)
5. Verify all components restored

**Expected Results**:
- Undo removes all: lights, empty, collection
- Redo restores complete rig
- No orphaned data blocks remain

## Performance Testing

### Test 8: Execution Time
**Objective**: Verify sub-second execution requirement

**Procedure**:
1. Create objects of varying complexity
2. Measure execution time for each
3. Test with 10k+ vertex objects

**Requirements**:
- Simple objects: < 0.5 seconds
- Complex objects: < 1.0 second
- No noticeable UI freeze

### Test 9: Memory Usage
**Objective**: Verify reasonable memory consumption

**Procedure**:
1. Monitor Blender memory usage
2. Create multiple lighting rigs
3. Check for memory leaks

## UI/UX Testing

### Test 10: Panel Behavior
**Objective**: Test UI panel functionality

**Test Cases**:
1. Panel appears only in Object Mode
2. Button enables/disables based on selection
3. Status messages update correctly
4. Advanced options display properly

### Test 11: User Feedback
**Objective**: Verify clear user communication

**Check Points**:
- Success messages are informative
- Error messages provide actionable guidance
- Progress indication during operation
- Help text accessibility

## Edge Cases

### Test 12: Name Conflicts
**Objective**: Handle naming conflicts gracefully

**Setup**:
1. Create objects named "Key_Light", "Fill_Light", etc.
2. Create collection named "ThreePointRig_Object"

**Procedure**:
1. Create lighting for object
2. Verify unique names generated

### Test 13: Locked/Protected Objects
**Objective**: Handle protected scene elements

**Test with**:
- Locked collections
- Protected objects
- Read-only blend files

## Troubleshooting Guide

### Common Issues

**Issue**: Panel not visible
**Solution**: 
1. Check add-on is enabled
2. Press N to show sidebar
3. Verify in Object Mode

**Issue**: "Permission error" message
**Solution**:
1. Ensure blend file is not read-only
2. Check collection permissions
3. Restart Blender if needed

**Issue**: Lights positioned incorrectly
**Solution**:
1. Check object has valid geometry
2. Try applying transforms (Ctrl+A)
3. Verify object scale is reasonable

**Issue**: Poor performance
**Solution**:
1. Reduce object complexity if possible
2. Close unnecessary Blender features
3. Check system resources

## Test Report Template

```
Test Date: ___________
Blender Version: ___________
Add-on Version: ___________
Operating System: ___________

Test Results:
□ Basic Functionality (Test 1)
□ Multiple Object Types (Test 2)  
□ Error Handling (Test 3)
□ Customization (Test 4)
□ Complex Geometry (Test 5)
□ Scene Integration (Test 6)
□ Undo/Redo (Test 7)
□ Performance (Test 8-9)
□ UI/UX (Test 10-11)
□ Edge Cases (Test 12-13)

Issues Found:
_________________________
_________________________
_________________________

Overall Assessment:
□ Pass - Ready for release
□ Pass with minor issues
□ Fail - Major issues found

Tester Signature: ___________
```

## Automation Hints

For automated testing of these procedures:
1. Use Blender's Python scripting for repetitive tasks
2. Screenshot comparison for visual verification
3. Performance timing with Python's `time` module
4. Memory profiling with appropriate tools