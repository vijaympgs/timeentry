# 📋 UNIVERSAL IMPLEMENTATION CHECKLIST (GOVERNANCE CANON)

**Status**: ✅ ACTIVE AUTHORITY  
**Scope**: All Modules (Retail, FMS, HRM, CRM)  
**Applies To**: Masters, Transactions, Reports, Dashboards  

> **PROTOCOL (NON-NEGOTIABLE)**  
> This checklist must be executed **BEFORE**, **DURING**, and **AFTER** every screen implementation.  
> Failure to follow this checklist constitutes an **incomplete and invalid delivery**.

---

## 1. 🛑 PRE-FLIGHT VALIDATION (MANDATORY BEFORE CODING)

> You are **not permitted to write or refactor code** until this section is completed.

- [ ] **Legacy Functionality Audit**
  - [ ] Enumerate every visible element: buttons, fields, tabs, grids, badges.
  - [ ] Identify hidden logic flows (auto-calculation, conditional behavior, disabled states).
  - [ ] Capture screenshots OR produce a precise mental model of existing behavior.
  - [ ] Confirm: _“I fully understand the current screen before touching it.”_

- [ ] **Service Layer Verification**
  - [ ] Open the corresponding `*Service.ts` file.
  - [ ] **CRITICAL RULE**: Identify **all fields** defined in service contracts (even if not shown in UI today).
  - [ ] Confirm that the new UI will include:
    - Old UI fields  
    - + Service contract fields  
    - − **No silent drops allowed**

- [ ] **Routing Awareness**
  - [ ] Locate existing route in `router.tsx`.
  - [ ] Identify whether implementation is:
    - In-place upgrade, OR  
    - Path migration  
  - [ ] Explicitly plan transition:  
    - `Existing Route` → `New Route`  
    - With no broken navigation.

---

## 2. 🏗️ ARCHITECTURE & CONFIG DISCIPLINE

> If this layer is wrong, everything above it becomes fragile.

- [ ] **Toolbar Configuration Integrity**
  - [ ] Define toolbar config string (e.g., `NESCKVDXRQF`).
  - [ ] Confirm corresponding entry exists in backend:
    - `ERPMenuItem`
    - `seed_toolbar_controls.py` or CSV seed
  - [ ] Explicitly validate mode behavior:
    - VIEW  
    - EDIT  
    - CREATE  
    are all correctly respected.

- [ ] **Container Pattern Compliance**
  - [ ] **Masters** must use:
    - `MasterToolbar`
    - Setup layout (Tabbed / Dense Form)
  - [ ] **Transactions** must use:
    - Toolbar + Workflow layout
    - List ↔ Detail behavior correctly wired

- [ ] **Permission Enforcement**
  - [ ] **Admin Law**: Built-in admin must always resolve to full permission mask (`111111...`).
  - [ ] Toolbar must receive resolved permissions dynamically.

- [ ] **Navigation Logic**
  - [ ] **Smart Exit**: 'Exit' action from Form mode must return to List mode (not Dashboard).
  - [ ] **Cancel**: 'Cancel' in Form mode returns to List mode.

---

## 3. 🧩 MASTERS (Item, Customer, Supplier, etc.)

> These are not CRUD demos. These are enterprise data control panels.

- [ ] **Screen Structure (STRICT)**
  - [ ] **Unified Container Only**:
    - List and Form Logic MUST be in the same component (State-based swap).
    - Router points to ONE file (the Setup component).
    - NO separate `ListPage.tsx`.
  - [ ] **Persistent Context**:
    - Master Title/Header must remain visible in both List and Form views.

- [ ] **Data Density Discipline**
  - [ ] Tabs present where required:
    - General  
    - Details  
    - Domain-specific (UOM, Addresses, Variants, etc.)
  - [ ] **No Skeleton Rule**:
    - Do NOT ship “basic now, we’ll add later”
    - Full richness first, refinement later.

- [ ] **Parity Guarantee**
  - [ ] Does the new UI support every capability the old UI supported?
  - [ ] Are metadata fields respected (Created By, Updated By, timestamps)?
  - [ ] Nothing removed silently.

---

## 4. 📝 TRANSACTIONS (PO, SO, Invoice, etc.)

> Transaction screens are governed by workflow correctness, not visual completion.

- [ ] **Navigation Controls**
  - [ ] First  
  - [ ] Previous  
  - [ ] Next  
  - [ ] Last  
  must be wired and functional.

- [ ] **Workflow Correctness**
  - [ ] Buttons (`Submit`, `Authorize`, `Reject`, etc.) appear **only** when allowed.
  - [ ] Status badge clearly visible and accurate (DRAFT, POSTED, etc.).

- [ ] **Operational Inputs**
  - [ ] Date range filters where applicable.
  - [ ] Line entry grids functional (not placeholders).
  - [ ] No broken add/remove/edit row flows.

---

## 5. 📊 REPORTS & DASHBOARDS

> Visual correctness is meaningless without data correctness.

- [ ] **Filter Panel**
  - [ ] F4 (or equivalent) filter panel present.
  - [ ] Supports core filters:
    - Date range  
    - Company  
    - Location  

- [ ] **Export Integrity**
  - [ ] Export works (CSV / PDF where applicable).
  - [ ] Exported data matches UI data.

- [ ] **Performance Discipline**
  - [ ] Server-side pagination enforced.
  - [ ] No full dataset loading for large reports.

---

## 6. ✅ FINAL VERIFICATION GATE (MERGE BLOCKER)

> You are **not allowed to declare completion** unless every item below passes.

- [ ] **Zero Regression Test**
  - [ ] Can I do everything the previous screen allowed?
  - [ ] No capability lost.

- [ ] **Build Integrity**
  - [ ] Vite build passes.
  - [ ] No unresolved imports.
  - [ ] No runtime crashes.

- [ ] **Console Hygiene**
  - [ ] No React warnings (keys, effects, hooks).
  - [ ] No red errors in console during normal flow.

- [ ] **Structural Discipline**
  - [ ] Folder boundaries respected (`apps/`, `core/`, `common`).
  - [ ] No cross-module leakage.
  - [ ] No architectural drift.

---

## 7. 🧨 ABSOLUTE FAILURE CONDITIONS

Any of the following immediately invalidates the delivery:

- Skeleton UI shipped for a complex master  
- Data exists in backend but list shows “No records”  
- Create form does not open or does not save  
- Fields removed without approval  
- Refactor treated as rewrite  
- Toolbar correct but screen functionally broken  

> Toolbar correctness **without functional correctness = FAILED DELIVERY**

---

**Last Updated**: 2026-01-10  
**Authority**: Viji (Final)  
**Classification**: Platform Governance Canon  


# 🎨 MODE-BASED TOOLBAR FILTERING - TECHNICAL REFERENCE

**Purpose**: Explains how `MasterToolbar` filters buttons based on `mode` prop  
**Date**: 2026-01-09 19:56 IST  
**Component**: `MasterToolbarConfigDriven.tsx`  
**Status**: ✅ PRODUCTION READY

---

## 🎯 THE CORE CONCEPT

### **Single Config String, Multiple Views**

The `MasterToolbar` component takes a **FULL configuration string** from the backend and **dynamically filters** which buttons to show based on the current **UI mode**.

**Example**:
```
Backend Config: NESCKZTJAVPMRDX1234QF (21 characters)

Frontend Usage:
  mode="VIEW"   → Shows 18 buttons (hides S, C, K)
  mode="CREATE" → Shows 4 buttons (S, C, K, X)
  mode="EDIT"   → Shows 4 buttons (S, C, K, X)
```

---

## 📊 HOW IT WORKS

### **Step 1: Backend Provides Full Config**

**ERPMenuItem Entry**:
```json
{
  "menu_id": "PURCHASE_ORDERS",
  "applicable_toolbar_config": "NESCKZTJAVPMRDX1234QF"
}
```

This string contains **ALL possible actions** for this screen.

---

### **Step 2: Frontend Passes Mode**

**List Page** (`PurchaseOrderListPage.tsx`):
```typescript
<MasterToolbar 
  viewId="PURCHASE_ORDERS" 
  mode="VIEW"  // ← Mode determines filtering
  onAction={handleAction}
/>
```

**Form Page - Viewing**:
```typescript
<MasterToolbar 
  viewId="PURCHASE_ORDERS" 
  mode="VIEW"  // ← Same mode, different context
  onAction={handleAction}
/>
```

**Form Page - Creating**:
```typescript
<MasterToolbar 
  viewId="PURCHASE_ORDERS" 
  mode="CREATE"  // ← Different mode
  onAction={handleAction}
/>
```

---

### **Step 3: Component Filters Buttons**

The `MasterToolbar` component internally:

1. **Fetches config** from backend using `viewId`
2. **Gets full string**: `NESCKZTJAVPMRDX1234QF`
3. **Applies mode filter** based on `mode` prop
4. **Renders only relevant buttons**

---

## 🔤 MODE-BASED FILTERING RULES

### **VIEW Mode** (Reading/Browsing)

**Purpose**: User is viewing data (list or single record), not editing

**Shows**:
```
N - New (F2)
E - Edit (F3)
V - View (F7)
D - Delete (F4)
X - Exit (Esc)
R - Refresh (F9)
Q - Search (Ctrl+F)
F - Filter (Alt+F)
Z - Authorize (F10)
T - Submit (Alt+S)
J - Reject (Alt+R)
A - Amend (Alt+A)
P - Print (Ctrl+P)
M - Email (Ctrl+M)
1234 - Navigation (Home/PgUp/PgDn/End)
I - Import (Ctrl+I)
O - Export (Ctrl+E)
```

**Hides**:
```
S - Save (F8)        ← Not relevant when viewing
C - Cancel (Esc)     ← Not relevant when viewing
K - Clear (F5)       ← Not relevant when viewing
```

**Logic**: "User is viewing, so show navigation and actions, hide form controls"

---

### **CREATE Mode** (Creating New Record)

**Purpose**: User is filling out a form to create new record

**Shows**:
```
S - Save (F8)
C - Cancel (Esc)
K - Clear (F5)
X - Exit (Esc)
? - Help (F1)
B - Notes (Alt+N)
G - Attachments (Alt+U)
```

**Hides**:
```
N - New              ← Already creating
E - Edit             ← Can't edit what doesn't exist yet
V - View             ← Can't view what doesn't exist yet
D - Delete           ← Can't delete what doesn't exist yet
R - Refresh          ← No data to refresh
Q - Search           ← Not relevant in form
F - Filter           ← Not relevant in form
Z,T,J,A - Workflow   ← Can't workflow unsaved record
P,M - Document       ← Can't print/email unsaved record
1234 - Navigation    ← No records to navigate
I,O - Import/Export  ← Not relevant in form
```

**Logic**: "User is creating, so show only form controls and cancel option"

---

### **EDIT Mode** (Editing Existing Record)

**Purpose**: User is modifying an existing record

**Shows**:
```
S - Save (F8)
C - Cancel (Esc)
K - Clear (F5)
X - Exit (Esc)
? - Help (F1)
B - Notes (Alt+N)
G - Attachments (Alt+U)
```

**Hides**:
```
N - New              ← Already editing
E - Edit             ← Already in edit mode
V - View             ← Already viewing (in edit mode)
D - Delete           ← Can't delete while editing
R - Refresh          ← Would lose changes
Q - Search           ← Not relevant in form
F - Filter           ← Not relevant in form
Z,T,J,A - Workflow   ← Can't workflow while editing
P,M - Document       ← Can't print/email while editing
1234 - Navigation    ← Would lose changes
I,O - Import/Export  ← Not relevant in form
```

**Logic**: "User is editing, so show only form controls and cancel option"

---

## 🎯 PRACTICAL EXAMPLES

### **Example 1: Purchase Orders**

**Backend Config**: `NESCKZTJAVPMRDX1234QF` (21 characters)

#### **List Page** (`/procurement/purchase-orders`):
```typescript
<MasterToolbar viewId="PURCHASE_ORDERS" mode="VIEW" />
```

**Buttons Shown** (subset for list context):
- New (F2) - Create new PO
- Edit (F3) - Edit selected PO
- Refresh (F9) - Reload list
- Search (Ctrl+F) - Search POs
- Filter (Alt+F) - Toggle filters
- Exit (Esc) - Leave page

**Buttons Hidden**: Save, Cancel, Clear, Print, Email, Authorize, etc.

---

#### **Form Page - Viewing** (`/procurement/orders/123`):
```typescript
<MasterToolbar viewId="PURCHASE_ORDERS" mode="VIEW" />
```

**Buttons Shown** (subset for form viewing):
- Edit (F3) - Switch to edit mode
- Delete (F4) - Delete this PO
- Print (Ctrl+P) - Print PO
- Email (Ctrl+M) - Email PO
- Authorize (F10) - Approve PO
- Submit (Alt+S) - Submit for approval
- Reject (Alt+R) - Reject PO
- Amend (Alt+A) - Amend approved PO
- Exit (Esc) - Leave page

**Buttons Hidden**: Save, Cancel, Clear, New

---

#### **Form Page - Creating** (`/procurement/orders/new`):
```typescript
<MasterToolbar viewId="PURCHASE_ORDERS" mode="CREATE" />
```

**Buttons Shown** (minimal for form creation):
- Save (F8) - Save new PO
- Cancel (Esc) - Cancel creation
- Clear (F5) - Clear form
- Exit (Esc) - Leave page

**Buttons Hidden**: All others (New, Edit, Delete, Print, Authorize, etc.)

---

### **Example 2: UOM Setup**

**Backend Config**: `NESCKVDXRQF` (11 characters)

#### **List Page** (`/inventory/uoms`):
```typescript
<MasterToolbar viewId="INVENTORY_UOM_SETUP" mode="VIEW" />
```

**Buttons Shown**:
- New (F2)
- Edit (F3)
- View (F7)
- Delete (F4)
- Exit (Esc)
- Refresh (F9)
- Search (Ctrl+F)
- Filter (Alt+F)

**Buttons Hidden**: Save, Cancel, Clear

---

#### **In-Place Form - Creating**:
```typescript
<MasterToolbar viewId="INVENTORY_UOM_SETUP" mode="CREATE" />
```

**Buttons Shown**:
- Save (F8)
- Cancel (Esc)
- Clear (F5)
- Exit (Esc)

**Buttons Hidden**: New, Edit, View, Delete, Refresh, Search, Filter

---

## 🔧 IMPLEMENTATION DETAILS

### **Component Logic** (`MasterToolbarConfigDriven.tsx`):

```typescript
// Pseudo-code for understanding

function MasterToolbar({ viewId, mode, onAction }) {
  // 1. Fetch full config from backend
  const fullConfig = fetchConfigFromBackend(viewId);
  // Returns: "NESCKZTJAVPMRDX1234QF"
  
  // 2. Define mode filters
  const VIEW_MODE_CHARS = 'NEVDXRQFZTJAPMI1234O';
  const CREATE_EDIT_MODE_CHARS = 'SCKX?BG';
  
  // 3. Filter based on mode
  let visibleChars;
  if (mode === 'VIEW') {
    visibleChars = fullConfig.split('').filter(char => 
      VIEW_MODE_CHARS.includes(char)
    );
  } else if (mode === 'CREATE' || mode === 'EDIT') {
    visibleChars = fullConfig.split('').filter(char => 
      CREATE_EDIT_MODE_CHARS.includes(char)
    );
  }
  
  // 4. Render only visible buttons
  return visibleChars.map(char => 
    <Button action={charToAction(char)} onClick={onAction} />
  );
}
```

---

## 📋 FILTERING MATRIX

| Character | Action | VIEW Mode | CREATE Mode | EDIT Mode |
|-----------|--------|-----------|-------------|-----------|
| **N** | New | ✅ Show | ❌ Hide | ❌ Hide |
| **E** | Edit | ✅ Show | ❌ Hide | ❌ Hide |
| **S** | Save | ❌ Hide | ✅ Show | ✅ Show |
| **C** | Cancel | ❌ Hide | ✅ Show | ✅ Show |
| **K** | Clear | ❌ Hide | ✅ Show | ✅ Show |
| **V** | View | ✅ Show | ❌ Hide | ❌ Hide |
| **D** | Delete | ✅ Show | ❌ Hide | ❌ Hide |
| **X** | Exit | ✅ Show | ✅ Show | ✅ Show |
| **R** | Refresh | ✅ Show | ❌ Hide | ❌ Hide |
| **Q** | Search | ✅ Show | ❌ Hide | ❌ Hide |
| **F** | Filter | ✅ Show | ❌ Hide | ❌ Hide |
| **Z** | Authorize | ✅ Show | ❌ Hide | ❌ Hide |
| **T** | Submit | ✅ Show | ❌ Hide | ❌ Hide |
| **J** | Reject | ✅ Show | ❌ Hide | ❌ Hide |
| **A** | Amend | ✅ Show | ❌ Hide | ❌ Hide |
| **P** | Print | ✅ Show | ❌ Hide | ❌ Hide |
| **M** | Email | ✅ Show | ❌ Hide | ❌ Hide |
| **I** | Import | ✅ Show | ❌ Hide | ❌ Hide |
| **O** | Export | ✅ Show | ❌ Hide | ❌ Hide |
| **1234** | Navigation | ✅ Show | ❌ Hide | ❌ Hide |
| **?** | Help | ✅ Show | ✅ Show | ✅ Show |
| **B** | Notes | ✅ Show | ✅ Show | ✅ Show |
| **G** | Attachments | ✅ Show | ✅ Show | ✅ Show |

---

## ✅ BENEFITS OF THIS APPROACH

### **1. Single Source of Truth**
- Backend defines FULL capability
- No duplication of config
- One place to update permissions

### **2. Context-Aware UI**
- List pages show navigation actions
- Form pages show form controls
- Automatic adaptation based on mode

### **3. No Hardcoding**
- Frontend doesn't hardcode which buttons to show
- All driven by backend config + mode
- Easy to add new actions

### **4. Consistent Behavior**
- Same filtering logic across all screens
- Predictable user experience
- Easy to maintain

---

## 🚀 USAGE PATTERN

### **For Every Screen**:

1. **Backend**: Create ONE `ERPMenuItem` entry with FULL config
2. **Frontend List Page**: Use `mode="VIEW"`
3. **Frontend Form Page**: Use `mode` based on state
4. **Component**: Automatically filters buttons

### **Example Template**:

```typescript
// List page
const ListPage = () => {
  return (
    <>
      <MasterToolbar 
        viewId="SCREEN_NAME" 
        mode="VIEW" 
        onAction={handleAction}
      />
      {/* List content */}
    </>
  );
};

// Form page
const FormPage = () => {
  const [isEditing, setIsEditing] = useState(false);
  const [isNew, setIsNew] = useState(false);
  
  const mode = isNew ? 'CREATE' : isEditing ? 'EDIT' : 'VIEW';
  
  return (
    <>
      <MasterToolbar 
        viewId="SCREEN_NAME" 
        mode={mode} 
        onAction={handleAction}
      />
      {/* Form content */}
    </>
  );
};
```

---

## 📊 REAL-WORLD SCENARIOS

### **Scenario 1: User Browsing List**
```
User Action: Opens /procurement/purchase-orders
Mode: VIEW
Buttons: New, Edit, Refresh, Search, Filter, Exit
User Can: Create new, edit selected, search, filter
User Cannot: Save, Cancel (no form active)
```

### **Scenario 2: User Viewing Single Record**
```
User Action: Clicks on PO #123
Mode: VIEW
Buttons: Edit, Delete, Print, Email, Authorize, Exit
User Can: Edit, delete, print, approve
User Cannot: Save, Cancel (not editing)
```

### **Scenario 3: User Creating New Record**
```
User Action: Clicks "New" button
Mode: CREATE
Buttons: Save, Cancel, Clear, Exit
User Can: Save new record, cancel, clear form
User Cannot: Edit, Delete, Print (record doesn't exist yet)
```

### **Scenario 4: User Editing Existing Record**
```
User Action: Clicks "Edit" button
Mode: EDIT
Buttons: Save, Cancel, Clear, Exit
User Can: Save changes, cancel, clear form
User Cannot: Delete, Print, Authorize (would lose changes)
```

---

## 🎯 KEY TAKEAWAYS

1. **One Config, Multiple Views**: Single backend string serves all contexts
2. **Mode Determines Visibility**: `mode` prop controls which buttons show
3. **Context-Aware**: Same screen, different buttons based on what user is doing
4. **No Hardcoding**: All driven by backend config + frontend mode
5. **Consistent Pattern**: Same logic across all screens

---

**Status**: ✅ PRODUCTION READY  
**Component**: `MasterToolbarConfigDriven.tsx`  
**Pattern**: Single-entry-per-screen with mode-based filtering