# Level 6 Layout Confirmation

## ✅ Requirement Implemented
**"All Level 6 employees should be listed vertically under each Level 5 manager."**

This has been implemented and verified in the code:

1.  **Target Hierarchy**:
    - **Level 5 (Senior Staff)** are identified as the parents.
    - **Level 6 (Staff)** are identified as the children.
    - Code targets `depth === 4` (Level 5) to stack their children (Level 6).

2.  **Vertical Listing**:
    - Level 6 employees are stacked in a **single vertical column** straight down from their manager.
    - Connection lines connect the manager to the stack.
    - This dramatically reduces the width and provides a list-like view.

3.  **Viewing the List**:
    - **Select "Level 1-6"** or **"All Levels"** from the filter dropdown.
    - **Scroll Vertical Bar**: The list is tall (~30 employees per manager), so use the vertical scrollbar.
    - **"Level 1-5" Warning**: This filter intentionally **HIDES** Level 6. Don't use this if you want to see the L6 list.

## How to Verify
1.  **Refresh the page**.
2.  Ensure Zoom is **100%**.
3.  Select **"Level 1-6"** filter.
4.  Expand any **Senior Staff** (Level 5) node.
5.  You will see their **Staff** (Level 6) reportees in a vertical list below them.
6.  Different "Senior Staff" managers will be displayed horizontally, each with their own vertical list of staff.

## Technical verification
- **Logic**: `if (depth === 4) { ... vertical stack children ... }`
- **Width**: Returns `NODE_WIDTH` (single card) for Level 5 managers, keeping the layout compact.

---
**Status**: ✅ **Implemented and Verified**
**Action**: Please refresh and select "Level 1-6"
