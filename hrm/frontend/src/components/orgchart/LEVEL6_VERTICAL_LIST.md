# Feature Request: Vertical List Layout for Level 6

## Requirement
Display Level 6 employees (251 staff members) as a **vertical flat list** instead of spreading them horizontally across the tree.

## Current Behavior
- All levels use horizontal tree layout
- Children are positioned side-by-side under their parent
- Level 6 has 251 employees spread across the tree width
- This creates a very wide org chart

## Desired Behavior
- Levels 1-5: Keep horizontal tree layout
- Level 6: Display as vertical list under each manager
- More compact and space-efficient
- Easier to scroll through Level 6 employees

## Implementation Approach

### Option 1: Vertical List Layout (Recommended)
**Changes Required:**
1. **Detect Level 6 in layout algorithm**
   - Track current level during tree traversal
   - When level === 6, switch to vertical layout

2. **Modify `computeSubtreeWidth`**
   ```typescript
   const computeSubtreeWidth = (node: OrgChartNode, level: number): number => {
     if (level === 6) {
       // Level 6: width is just one card
       return NODE_WIDTH;
     }
     // Levels 1-5: sum of children widths
     // ... existing logic
   }
   ```

3. **Modify `placeNode` function**
   ```typescript
   const placeNode = (node: OrgChartNode, x: number, y: number, level: number) => {
     if (level === 6) {
       // Vertical layout: stack children vertically
       let currentY = y + NODE_HEIGHT + VERTICAL_GAP;
       children.forEach(child => {
         placeNode(child, x, currentY, level + 1);
         currentY += NODE_HEIGHT + VERTICAL_GAP;
       });
     } else {
       // Horizontal layout: spread children horizontally
       // ... existing logic
     }
   }
   ```

4. **Update height calculation**
   - Level 6 vertical list increases total height
   - Need to calculate max height for each Level 5 manager's list

### Option 2: Compact Grid Layout
**Alternative:**
- Display Level 6 in a compact grid (2-3 columns)
- Still under their manager
- More compact than horizontal spread
- Less dramatic change than full vertical list

### Option 3: Collapsible List View
**Alternative:**
- Keep tree layout for Levels 1-5
- Add a "View Team" button on Level 5 managers
- Opens a modal/panel with vertical list of their Level 6 reports
- Keeps main org chart compact

## Visual Mockup

### Current Layout (Horizontal):
```
        [Manager L5]
           |
    ┌──────┼──────┬──────┬──────┬──────┐
    │      │      │      │      │      │
  [L6]   [L6]   [L6]   [L6]   [L6]  ...
  
  (251 employees spread horizontally = VERY WIDE)
```

### Proposed Layout (Vertical List):
```
        [Manager L5]
           |
        [L6 Employee 1]
        [L6 Employee 2]
        [L6 Employee 3]
        [L6 Employee 4]
        ...
        [L6 Employee 30]
        
  (Vertical list = COMPACT)
```

## Estimated Effort

### Option 1 (Vertical List):
- **Complexity**: High
- **Time**: 30-45 minutes
- **Files to modify**:
  - `useVirtualTree.ts`: Layout algorithm
  - `VirtualOrgChart.tsx`: Rendering logic
  - `orgChart.virtual.css`: Styling for vertical list

### Option 2 (Compact Grid):
- **Complexity**: Medium
- **Time**: 20-30 minutes
- **Files to modify**:
  - `useVirtualTree.ts`: Layout algorithm
  - `orgChart.virtual.css`: Grid styling

### Option 3 (Collapsible List):
- **Complexity**: Medium
- **Time**: 15-25 minutes
- **Files to modify**:
  - `VirtualOrgChart.tsx`: Add modal/panel component
  - `orgChart.virtual.css`: Modal styling

## Benefits

### Vertical List:
✅ Much more compact org chart
✅ Easier to see all Level 6 employees
✅ Less horizontal scrolling
✅ Better for printing
✅ More professional appearance

### Challenges:
⚠️ Different layout paradigm for one level
⚠️ Need to handle varying list lengths
⚠️ May create very tall charts
⚠️ Requires significant refactoring

## Recommendation

**Implement Option 1 (Vertical List)** for the best user experience, but this requires:
1. Refactoring the layout algorithm
2. Adding level tracking
3. Conditional layout logic
4. Testing with real data

**Quick Alternative**: Option 3 (Collapsible List) is faster to implement and provides similar benefits without major refactoring.

## Next Steps

Please confirm which approach you prefer:
1. **Full vertical list** (30-45 min, best UX)
2. **Compact grid** (20-30 min, middle ground)
3. **Collapsible modal** (15-25 min, quickest)

---

**Status**: 📋 Feature Request
**Priority**: High (251 employees at Level 6)
**Impact**: Significant UX improvement
**Decision Needed**: Which implementation approach?
