# Virtualization Fix for Zoomed View

## 🐛 The Issue
When zoomed out (e.g., to 10%), scrolling to the bottom of the chart caused nodes to disappear (white space).
- **Cause**: The "Virtualization" engine (which only draws what is visible to save memory) was getting confused by the zoom scale. It thought you were looking at the top of the chart (small scroll number) while you were actually at the bottom (scaled down).

## ✅ The Fix
Updated the layout engine to calculate visible area using **"Unscaled Coordinates"**.
- Now, if you are at 10% zoom and scroll to pixel 300, the system correctly understands this maps to pixel 3000 in the chart logic.
- **Result**: ALL 251 Level 6 employees will properly render, even at minimum zoom.

## How to Verify
1.  **Refresh** the page.
2.  Switch to **"All Levels"**.
3.  **Zoom Out** to the minimum (10%).
4.  **Scroll** all the way to the bottom.
5.  Confirm that all lists are fully populated and visible.

---
**Status**: ✅ **Fixed Rendering Issue**
