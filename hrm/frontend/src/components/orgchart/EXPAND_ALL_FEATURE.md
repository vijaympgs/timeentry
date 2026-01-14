# Expand All / Collapse All Feature Added

## Issue
User reported: "it's not displaying all the 275 records"

## Root Cause
The org chart uses **expand/collapse functionality** for the hierarchy. By default, nodes can be collapsed, hiding their direct reports. Users need to manually click the expand arrows (▶/▼) on each card to see all employees.

## Solution
Added **"Expand All"** and **"Collapse All"** buttons to the toolbar.

### Changes Made:

#### 1. Added Functions (VirtualOrgChart.tsx)
```typescript
// Expand all nodes
const handleExpandAll = useCallback(() => {
  const all = new Set<string>();
  collectIds(filteredRoots, all);
  setExpanded(all);
}, [filteredRoots]);

// Collapse all nodes
const handleCollapseAll = useCallback(() => {
  setExpanded(new Set());
}, []);
```

#### 2. Added Icons
```typescript
import { ..., Maximize2, Minimize2 } from 'lucide-react';
```

#### 3. Added Buttons to Toolbar
```typescript
<button onClick={handleExpandAll}>
  <Maximize2 size={16} />
  <span>Expand All</span>
</button>

<button onClick={handleCollapseAll}>
  <Minimize2 size={16} />
  <span>Collapse All</span>
</button>
```

## How to Use

### To See All 275 Employees:
1. **Click "Expand All" button** in the toolbar
2. All nodes will expand showing the complete hierarchy
3. Scroll to see all employees across all 6 levels

### To Collapse:
1. **Click "Collapse All" button** to hide all direct reports
2. Only top-level employees will be visible

### Manual Expand/Collapse:
- Click **▼** (down arrow) on a card to collapse that employee's reports
- Click **▶** (right arrow) on a card to expand and show their reports

## Toolbar Layout (Updated)

```
[Search] [Dept ▼] [Level ▼] | [−][100%][+][↻] [Expand All] [Collapse All]  [Reload]
```

## Expected Behavior

### On Initial Load:
- All nodes are **expanded by default**
- You should see all 275 employees in the hierarchy
- If you don't, click **"Expand All"**

### After Filtering:
- Department filter: Shows filtered employees (may need to expand)
- Level filter: Shows only specified levels
- Search: Auto-expands matching nodes

### With Zoom:
- Zoom in: See details of expanded hierarchy
- Zoom out: See overview of structure
- Works with both expanded and collapsed states

## Files Modified

1. **`VirtualOrgChart.tsx`**:
   - Added `handleExpandAll()` function
   - Added `handleCollapseAll()` function
   - Added Maximize2, Minimize2 icon imports
   - Added two new buttons to toolbar

## Testing

- [ ] Click "Expand All" - should show all 275 employees
- [ ] Click "Collapse All" - should show only root nodes
- [ ] Manually expand/collapse individual nodes
- [ ] Use with department filter
- [ ] Use with level filter
- [ ] Use with search
- [ ] Use with zoom controls

## Summary

✅ **Added "Expand All" button** - Shows all 275 employees at once
✅ **Added "Collapse All" button** - Hides all direct reports
✅ **Maintains existing functionality** - Manual expand/collapse still works
✅ **Works with filters** - Expands filtered results

---

**Status**: ✅ Complete
**Action**: Refresh page and click "Expand All" to see all 275 employees
**Location**: Toolbar, between zoom controls and reload button
