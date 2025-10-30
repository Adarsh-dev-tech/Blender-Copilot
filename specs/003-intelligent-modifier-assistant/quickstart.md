# Quickstart Guide: Intelligent Modifier Assistant

**Feature**: Intelligent Modifier Assistant  
**Date**: 2025-10-30  
**Version**: 1.0  
**Target Users**: 3D Artists, Modelers, Blender Users

## What This Feature Does

The Intelligent Modifier Assistant automates six common modifier workflows through simple text commands. Instead of manually adding modifiers, configuring dozens of settings, and remembering the correct order, you type what you want (e.g., "make this hard-surface") and the assistant handles all the technical details.

**Supported Workflows**:
1. **Smart Array** - Create arrays with or without empty object control
2. **Hard-Surface SubD** - Auto-configure Bevel + Subdivision for hard-surface modeling
3. **Symmetrize** - Mirror with automatic cleanup (applies scale, deletes half the mesh)
4. **Curve Deform** - Deform mesh along a curve path with correct origin alignment
5. **Smart Solidify** - Add thickness to flat geometry with quality settings
6. **Shrinkwrap** - Wrap one mesh to another's surface

---

## Installation

**Prerequisites**:
- Blender 3.0 or newer
- Blender Copilot add-on installed

**Steps**:
1. Open Blender Preferences (`Edit > Preferences`)
2. Go to **Add-ons** tab
3. Ensure "Blender Copilot" is enabled (checkbox checked)
4. Look for "Copilot" tab in 3D View sidebar (press `N` to show sidebar)

---

## Quick Start (30 Seconds)

### 1. Access the Tool
1. Open Blender (or start a new scene)
2. Press `N` to show the 3D View sidebar
3. Click the **"Copilot"** tab
4. Find the **"Modifier Assistant"** panel

### 2. Try Your First Command
1. Select the default cube in your scene
2. In the Modifier Assistant panel, type: **`make hard-surface`**
3. Click **"Execute"**
4. **Result**: The cube now has Bevel + Subdivision modifiers and smooth shading!

### 3. Undo If Needed
- Press `Ctrl+Z` to undo the entire operation in one step
- Everything returns to the way it was before

---

## Basic Workflows

### Workflow 1: Create an Array

**Use Case**: You want to duplicate an object multiple times in a row.

**Steps**:
1. Select one mesh object (e.g., a cube)
2. Type command: **`create an array`** or **`make 5 copies`**
3. Click **Execute**

**What Happens**:
- Array modifier is added
- 5 copies appear along the X-axis
- You can adjust the count or offset in the modifier panel

**Expected Result**:
```
Before: ◻️
After:  ◻️ ◻️ ◻️ ◻️ ◻️
```

---

### Workflow 2: Array with Empty Object Control

**Use Case**: You want an array that follows a custom path defined by an empty object.

**Steps**:
1. Select your mesh object
2. Add an empty object (`Shift+A` → Empty → Plain Axes)
3. Move the empty to create an offset (e.g., move 3 units on Y-axis)
4. Select BOTH objects (mesh first, then Shift+click empty)
5. Type command: **`array controlled by empty`**
6. Click **Execute**

**What Happens**:
- Array modifier added to mesh
- Modifier uses the empty's transform for offset
- Moving the empty now controls the array pattern

**Pro Tip**: Rotate or scale the empty to create complex array patterns!

---

### Workflow 3: Hard-Surface SubD Setup

**Use Case**: You're modeling hard-surface objects (machines, vehicles) and need the Bevel+Subdivision workflow.

**Steps**:
1. Select your mesh object (works best with cubes or angular shapes)
2. Type command: **`make this hard-surface`** or **`add subdivision`**
3. Click **Execute**

**What Happens**:
- Bevel modifier added (preserves hard edges with angle detection)
- Subdivision Surface modifier added AFTER Bevel
- Object shading set to Smooth
- Clean beveled edges with subdivision smoothness

**Why This Matters**: The modifier ORDER is critical - Bevel must come before Subdivision. The assistant handles this automatically.

---

### Workflow 4: Symmetrize (Mirror with Cleanup)

**Use Case**: You want to model half an object and mirror it to the other side (common in character/vehicle modeling).

**Steps**:
1. Select your mesh object
2. Type command: **`mirror this`** or **`symmetrize on X`**
3. Click **Execute**

**What Happens** (multi-step automation):
1. Your object's scale is applied (critical prerequisite)
2. Mirror modifier is added on the X-axis
3. System enters Edit Mode
4. All vertices on the positive X side are automatically deleted
5. Returns to Object Mode

**Result**: Perfect mirrored object with clean center axis.

**⚠️ Warning**: This DELETES half your geometry. Make sure you're ready or save first!

---

### Workflow 5: Curve Deform

**Use Case**: You want to bend a mesh object along a curve path (great for roads, pipes, cables).

**Steps**:
1. Create a mesh object (e.g., a plane or cylinder)
2. Add a curve (`Shift+A` → Curve → Bezier)
3. Edit the curve to create your desired path
4. Select BOTH objects (mesh first, then Shift+click curve)
5. Type command: **`deform along curve`** or **`follow this path`**
6. Click **Execute**

**What Happens** (with prerequisites):
1. Scale is applied to BOTH objects
2. Mesh origin is aligned to curve origin (critical for correct deformation)
3. Curve modifier is added to mesh
4. Mesh deforms to follow the curve path

**Common Gotcha**: If the mesh doesn't deform correctly, it's usually because origins weren't aligned. The assistant fixes this automatically!

---

### Workflow 6: Add Thickness (Solidify)

**Use Case**: You have a flat object (plane, circle) and want to give it thickness.

**Steps**:
1. Select your flat mesh (e.g., a plane)
2. Type command: **`add thickness`** or **`solidify this`**
3. Click **Execute**

**What Happens**:
- Solidify modifier is added
- Thickness set to 0.01m (1cm)
- "Even Thickness" option enabled for better quality

**Adjusting**: You can increase thickness in the modifier properties panel.

---

### Workflow 7: Shrinkwrap to Surface

**Use Case**: You want one mesh to conform to the surface of another (great for clothing, decals, projections).

**Steps**:
1. Create/select your SOURCE mesh (the one that will wrap)
2. Create/select your TARGET mesh (the surface to wrap to)
3. Make sure the SOURCE is the active object (last selected, highlighted)
4. Select both objects
5. Type command: **`shrinkwrap to target`** or **`wrap this mesh`**
6. Click **Execute**

**What Happens**:
- Shrinkwrap modifier added to the active (source) object
- Target object is set as the shrinkwrap target
- Wrap method is set to "Nearest Surface Point" (most reliable)
- Source mesh deforms to match target surface

---

## Testing Your Installation

### Validation Test Procedure

**Test 1: Simple Array** (30 seconds)
1. Delete default cube, add a new cube (`Shift+A` → Mesh → Cube)
2. Command: `create an array`
3. ✅ **Pass**: You see 5 cubes in a row
4. ❌ **Fail**: Error message or no modifier added

**Test 2: Hard-Surface** (30 seconds)
1. Select the cube
2. Command: `make this hard-surface`
3. ✅ **Pass**: Cube has rounded edges, smooth shading, two modifiers (Bevel and Subdivision Surface)
4. ❌ **Fail**: No modifiers or wrong order

**Test 3: Error Handling** (15 seconds)
1. Deselect all objects (`Alt+A`)
2. Command: `make array`
3. ✅ **Pass**: Error message "Please select an object first"
4. ❌ **Fail**: No error or Blender crashes

**Test 4: Undo** (15 seconds)
1. Press `Ctrl+Z` to undo the hard-surface setup
2. ✅ **Pass**: All modifiers removed in one undo step
3. ❌ **Fail**: Only partial undo or broken state

**All Tests Pass?** → Installation successful! ✅  
**Any Test Fails?** → Check console for errors or report an issue

---

## Command Reference

### Recognized Command Patterns

| Workflow | Example Commands |
|----------|-----------------|
| **Smart Array** | "create an array", "make 5 copies", "duplicate this", "array" |
| **Hard-Surface** | "make this hard-surface", "add subdivision", "hard surface setup", "subd" |
| **Symmetrize** | "mirror this", "symmetrize on X", "make symmetric", "sym" |
| **Curve Deform** | "deform along curve", "follow this path", "curve deform", "bend along curve" |
| **Solidify** | "add thickness", "solidify this", "make this solid", "thicken" |
| **Shrinkwrap** | "shrinkwrap to target", "wrap this mesh", "conform to surface", "shrinkwrap" |

**Case Insensitive**: Commands work in ANY case (UPPER, lower, or MiXeD).

---

## Troubleshooting

### Problem: "Command not understood" error

**Possible Causes**:
- Typo in command
- Using unsupported command

**Solutions**:
- Check spelling
- Try one of the example commands from the reference table
- Commands must contain key words like "array", "mirror", "solidify", etc.

---

### Problem: "Please select an object first"

**Cause**: No objects are selected in the scene.

**Solution**:
- Click an object in the 3D View to select it
- Check that the object is highlighted (orange outline)

---

### Problem: "This command requires two selected objects: a mesh and a curve"

**Cause**: Workflow needs specific object types (e.g., Curve Deform needs mesh + curve).

**Solution**:
- For Curve Deform: Select your mesh, then Shift+click the curve
- For Shrinkwrap: Select source mesh, then Shift+click target mesh
- For Array with empty: Select mesh, then Shift+click empty

**How to Select Multiple Objects**:
1. Click first object
2. Hold `Shift` and click second object
3. The last-clicked object is the "active" object (brighter highlight)

---

### Problem: Symmetrize deleted the wrong half of my mesh

**Cause**: The Mirror modifier uses the world X-axis. If your object is rotated, the axis might not be where you expect.

**Solution**:
- Apply rotation first: Select object → `Ctrl+A` → Rotation
- Or manually position your object so the desired mirror axis aligns with X-axis
- Then run the command again

---

### Problem: Curve Deform doesn't look right

**Possible Causes**:
- Objects weren't at the same location
- Origins misaligned (assistant should fix this, but check if it failed)

**Solutions**:
- Undo (`Ctrl+Z`)
- Manually move mesh object to the same location as the curve's start
- Try the command again
- Check modifier settings: The curve object should be assigned in the "Object" field of the Curve modifier

---

### Problem: Performance is slow (>1 second)

**Possible Causes**:
- Very high-poly mesh (100k+ vertices) for Symmetrize workflow
- Large scenes with many objects

**Solutions**:
- For Symmetrize: Consider decimating the mesh first
- For large scenes: Hide unneeded objects before running command
- This is expected behavior for very complex meshes

---

## Advanced Tips

### Tip 1: Chain Multiple Workflows
You can run multiple workflows on the same object:

1. Command: `make array` (creates array)
2. Command: `add thickness` (solidifies the array)
3. Command: `make hard-surface` (adds bevel and subdivision)

Result: A thick, beveled array of objects!

### Tip 2: Customize After Execution
All modifiers appear in the Properties panel (Modifiers tab). After the assistant applies them, you can:
- Adjust array count
- Change bevel width
- Modify subdivision levels
- Tweak solidify thickness

The assistant just gets you 90% there with good defaults!

### Tip 3: Use for Learning
If you're new to modifiers:
1. Run a workflow command
2. Look at the modifier stack
3. See which modifiers were added and their settings
4. Learn the pattern for next time

The assistant is also a teaching tool!

### Tip 4: Save Presets
If you use the same modifier setups often:
1. Let the assistant create the setup
2. Customize the parameters
3. Save your file as a template
4. Append the object to new projects

### Tip 5: Combine with Blender's Built-in Tools
The assistant works alongside Blender's native modifier system:
- Add assistant modifiers first (quick setup)
- Then add manual modifiers (fine-tuning)
- Mix and match as needed

---

## Keyboard Shortcuts (Future Enhancement)

Currently, the feature is UI-button driven. Future versions may support:
- Quick command shortcuts (e.g., `Shift+Ctrl+M` for modifier assistant)
- Command history (recall previous commands)
- Favorite commands

---

## Getting Help

**In-Tool Help**:
- Hover over the "Execute" button for quick tips
- Check the status bar (bottom of Blender window) for feedback messages

**Documentation**:
- Full specification: `specs/003-intelligent-modifier-assistant/spec.md`
- Technical details: `specs/003-intelligent-modifier-assistant/research.md`

**Reporting Issues**:
If something doesn't work:
1. Check Blender version (must be 3.0+)
2. Check console for error messages (`Window` → `Toggle System Console` on Windows)
3. Note your exact command and selection
4. Report with steps to reproduce

---

## What's Next?

Once you're comfortable with basic workflows, try:
1. Combining workflows for complex effects
2. Using arrays with empty objects for circular patterns
3. Creating complex hard-surface models with the SubD workflow
4. Experimenting with curve deformation for organic shapes

**Happy modeling!** 🎨

---

**Quickstart Guide Complete** - Users can now validate the feature and understand all workflows.
