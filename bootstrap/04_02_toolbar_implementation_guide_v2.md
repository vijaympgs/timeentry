# 🛠️ TOOLBAR IMPLEMENTATION GUIDE (v2.0 - API-Driven)

**Target Agents**: Agent E (HRM/CRM)  
**Objective**: Ensure 100% UI consistency using Backend API-Driven Toolbars  
**Version**: 2.0 (API-Driven Permission System)  
**Last Updated**: 2026-01-11 20:17 IST

---

## 📜 VERSION HISTORY

| Version | Date | System | Key Change |
|---------|------|--------|------------|
| **1.0** | 2026-01-07 | Character-Based | Frontend filtered character strings |
| **2.0** | 2026-01-11 | API-Driven | Backend API returns filtered action IDs |

**Current System**: ✅ **API-Driven** (v2.0)

---

## 1. THE ARCHITECTURE

The ERP uses an **API-Driven Permission** system. Instead of frontend filtering characters, the backend API returns exactly which actions are allowed based on:
- Screen identifier (`viewId`)
- Current mode (`VIEW`, `VIEW_FORM`, `CREATE`, `EDIT`)
- User permissions
- Record status (for transactions)

### **Flow Diagram**:
```
Frontend Component
    ↓
MasterToolbar (viewId + mode)
    ↓
useToolbarPermissions Hook
    ↓
GET /api/toolbar-permissions/?view_id=X&mode=Y
    ↓
Backend Logic (permissions + mode + status)
    ↓
{ "allowed_actions": ["new", "edit", ...] }
    ↓
Render Only Allowed Buttons
```

| Component | Responsibility |
|-----------|----------------|
| **Backend Model** | `ERPMenuItem` stores the `toolbar_config` (base permissions). |
| **API Endpoint** | `/api/toolbar-permissions/` filters actions based on mode and user. |
| **`useToolbarPermissions`** | React Hook that fetches allowed actions from API. |
| **`MasterToolbar`** | UI component that renders buttons based on API response. |

---

## 2. THE FOUR MODES

### **Mode Type Definition**
```typescript
type MasterMode = 'VIEW' | 'VIEW_FORM' | 'CREATE' | 'EDIT';
```

### **Mode Descriptions**

| Mode | Description | When to Use |
|------|-------------|-------------|
| **VIEW** | Browsing lists or records | Master list, Transaction list |
| **VIEW_FORM** | Viewing single record (read-only) | Approved transactions, Read-only master view |
| **CREATE** | Creating new record | New master entry, New transaction |
| **EDIT** | Editing existing record | Modify draft master, Edit draft transaction |

---

## 3. HOW TO IMPLEMENT (Step-by-Step)

### Step 1: Backend Registration

Every page must be registered in the `ERPMenuItem` table.

**Django Admin** (`http://localhost:8000/admin/`):

1. Navigate to: **Toolbar Control** → **ERP Menu Items**
2. Click **Add ERP Menu Item**
3. Fill in the form:

```
Menu ID: EMPLOYEE_MASTER
Menu Name: Employee Master
Module Name: HRM
Submodule Name: EMPLOYEE
View Type: MASTER
Route Path: /hrm/employees
Applicable Toolbar Config: NESCKVDXRQFIO
Is Active: ✓ (checked)
```

**Field Explanations**:
- `menu_id`: Uppercase snake case, matches frontend `viewId`
- `view_type`: MASTER, TRANSACTION, REPORT, DASHBOARD, or CONFIGURATION
- `toolbar_config`: Character string defining base permissions (backend uses this)

**Note**: The `toolbar_config` string is used by backend to determine base permissions. The API endpoint filters this based on mode and user permissions before sending to frontend.

---

### Step 2: Frontend Layout

Import the `MasterToolbar` and wire it to your page.

```tsx
import { MasterToolbar, MasterMode } from "@core/ui-canon/frontend/ui/components/MasterToolbarConfigDriven";

export const MyPage = () => {
    const [showForm, setShowForm] = useState(false);
    const [editingId, setEditingId] = useState<string | null>(null);
    const [viewMode, setViewMode] = useState(false);
    
    // Determine current mode
    const getMode = (): MasterMode => {
        if (!showForm) return 'VIEW';
        if (viewMode) return 'VIEW_FORM';
        return editingId ? 'EDIT' : 'CREATE';
    };
    
    // Wire the common handler
    const handleAction = (id: string) => {
        if (id === 'new') {
            setEditingId(null);
            setViewMode(false);
            setShowForm(true);
        }
        if (id === 'save') { 
            /* save logic */
            setShowForm(false);
        }
        if (id === 'exit') {
            if (showForm) {
                setShowForm(false);
            } else {
                navigate('/dashboard');
            }
        }
    };
    
    return (
        <>
            <MasterToolbar 
                viewId="HRM_LEAVE_APPLICATION" // Must match DB ID
                mode={getMode()} 
                onAction={handleAction} 
                hasSelection={!!selectedId}
            />
            <div className="content">...</div>
        </>
    );
}
```

---

### Step 3: Mode Management

The toolbar's visual state is driven by the `mode` prop and backend API response.

**Backend API automatically filters actions based on mode:**

- **`VIEW`**: Shows navigation, search, new, edit, and workflow actions.
- **`VIEW_FORM`**: Shows view-related actions (edit, delete, print, email).
- **`CREATE`/`EDIT`**: Shows only form controls (save, cancel, clear, exit).

**You don't need to filter actions in frontend** - the API does it for you!

---

## 4. CONFIGURATION STRINGS BY SCREEN TYPE

**Note**: These strings are stored in backend and used by the API to determine base permissions. Frontend receives filtered action IDs from the API.

### **Masters (Simple)** - Basic CRUD
```
Config: NESCKVDXRQF
Base Actions: New, Edit, Save, Cancel, Clear, View, Delete, Exit, Refresh, Search, Filter

Example screens:
- Department
- Position
- Leave Type
- Contact Category
```

### **Masters (Advanced)** - With Import/Export
```
Config: NESCKVDXRQFIO
Base Actions: Above + Import, Export

Example screens:
- Employee Master
- Contact Master
- Account Master
```

### **Transactions** - Full Workflow
```
Config: NESCKZTJAVPMRDX1234QF
Base Actions: New, Edit, Save, Cancel, Clear, Authorize, Submit, Reject, 
         Amend, View, Print, Email, Refresh, Delete, Exit, 
         First, Prev, Next, Last, Search, Filter

Example screens:
- Leave Request
- Attendance Adjustment
- Lead
- Opportunity
```

### **Reports** - Read-Only
```
Config: VRXPYQFG
Base Actions: View, Refresh, Exit, Print, Export, Search, Filter, Generate

Example screens:
- Employee Directory Report
- Leave Balance Report
- Sales Pipeline Report
```

---

## 5. API REQUEST/RESPONSE FORMAT

### **Request**:
```http
GET /api/toolbar-permissions/?view_id=EMPLOYEE_MASTER&mode=VIEW
Authorization: Bearer <token>
```

### **Response**:
```json
{
  "allowed_actions": [
    "new",
    "edit",
    "view",
    "delete",
    "refresh",
    "search",
    "filter",
    "import",
    "export",
    "exit"
  ]
}
```

### **Different Modes, Different Actions**:

**VIEW Mode**:
```json
{ "allowed_actions": ["new", "edit", "view", "delete", "refresh", "search", "filter", "exit"] }
```

**CREATE Mode**:
```json
{ "allowed_actions": ["save", "cancel", "clear", "exit"] }
```

**EDIT Mode**:
```json
{ "allowed_actions": ["save", "cancel", "clear", "exit"] }
```

**VIEW_FORM Mode** (Read-only):
```json
{ "allowed_actions": ["edit", "delete", "print", "email", "exit"] }
```

---

## 6. COMPLETE ACTION REFERENCE

**Note**: These are action IDs that backend may return. Frontend doesn't need to map characters.

```
new       - New (F2)
edit      - Edit (F3)
save      - Save (F8)
cancel    - Cancel (Esc)
clear     - Clear (F5)
view      - View (F7)
delete    - Delete (F4)
exit      - Exit (Esc)
refresh   - Refresh (F9)
search    - Search (Ctrl+F)
filter    - Filter (Alt+F)
authorize - Authorize (F10)
submit    - Submit (Alt+S)
reject    - Reject (Alt+R)
amend     - Amend (Alt+A)
print     - Print (Ctrl+P)
email     - Email (Ctrl+M)
import    - Import (Ctrl+I)
export    - Export (Ctrl+E)
first     - First (Home)
previous  - Prev (PgUp)
next      - Next (PgDn)
last      - Last (End)
generate  - Generate (Alt+G) - For reports
attach    - Attachments (Alt+U)
notes     - Notes (Alt+N)
help      - Help (F1)
clone     - Clone record
```

---

## 7. COMMON PATTERNS

### **Pattern 1: Simple Master (Department, Position)**

**Backend**:
```
menu_id: DEPARTMENT_MASTER
view_type: MASTER
config: NESCKVDXRQF
```

**Frontend**:
```typescript
const getMode = (): MasterMode => {
  if (!showForm) return 'VIEW';
  if (viewMode) return 'VIEW_FORM';
  return editingId ? 'EDIT' : 'CREATE';
};

<MasterToolbar 
    viewId="DEPARTMENT_MASTER" 
    mode={getMode()} 
    onAction={handleAction}
    hasSelection={!!selectedId}
/>
```

---

### **Pattern 2: Advanced Master (Employee, Contact)**

**Backend**:
```
menu_id: CONTACT_MASTER
view_type: MASTER
config: NESCKVDXRQFIO
```

**Frontend**: Same as Pattern 1. API automatically includes Import/Export in VIEW mode.

---

### **Pattern 3: Transaction (Leave, Lead)**

**Backend**:
```
menu_id: LEAD
view_type: TRANSACTION
config: NESCKZTJAVPMRDX1234QF
```

**Frontend**:
```typescript
const getMode = (): MasterMode => {
  if (!id) return 'CREATE';
  if (record?.status === 'DRAFT') return 'EDIT';
  return 'VIEW_FORM'; // Submitted/Approved
};

<MasterToolbar 
    viewId="LEAD" 
    mode={getMode()} 
    onAction={handleAction}
/>
```

---

## 8. ✅ CHECKLIST FOR AGENT E

### **For Each Screen**:

#### **Backend**:
- [ ] Create ONE ERPMenuItem entry (not separate list/form entries)
- [ ] Set `menu_id` in UPPERCASE_SNAKE_CASE
- [ ] Set `view_type` (MASTER, TRANSACTION, REPORT, etc.)
- [ ] Set `toolbar_config` based on screen type
- [ ] Set `route_path` to match frontend route
- [ ] Verify API endpoint `/api/toolbar-permissions/` works

#### **Frontend**:
- [ ] Import `MasterToolbar` from correct path
- [ ] Set `viewId` to match backend `menu_id` EXACTLY
- [ ] Implement `getMode()` function returning VIEW/VIEW_FORM/CREATE/EDIT
- [ ] Implement `handleToolbarAction()` for all actions
- [ ] **DO NOT** add `allowedActions` prop (API controls this)
- [ ] Add state for `showForm`, `editingId`, `viewMode`, `selectedId`
- [ ] Add filter panel toggle state (if applicable)

#### **Testing**:
- [ ] VIEW mode shows correct buttons (from API)
- [ ] VIEW_FORM mode shows read-only actions
- [ ] CREATE mode shows only save, cancel, clear, exit
- [ ] EDIT mode shows only save, cancel, clear, exit
- [ ] All keyboard shortcuts work
- [ ] Filter toggle works
- [ ] Exit navigation works (form → list, list → dashboard)

---

## 9. 🚨 COMMON MISTAKES TO AVOID

### **❌ MISTAKE 1: Creating Separate List View Entry**

```
❌ WRONG:
ERPMenuItem(menu_id="employee-list", view_type="LIST_VIEW")
ERPMenuItem(menu_id="EMPLOYEE_MASTER", view_type="MASTER")

✅ CORRECT:
ERPMenuItem(menu_id="EMPLOYEE_MASTER", view_type="MASTER")
Frontend handles list with mode="VIEW"
```

---

### **❌ MISTAKE 2: Hardcoding allowedActions**

```
❌ WRONG:
<MasterToolbar 
    viewId="EMPLOYEE_MASTER" 
    allowedActions={['new', 'edit', 'save']}  // ❌ API controls this!
/>

✅ CORRECT:
<MasterToolbar 
    viewId="EMPLOYEE_MASTER" 
    mode={getMode()}  // API filters based on mode
/>
```

---

### **❌ MISTAKE 3: Wrong viewId Case**

```
❌ WRONG:
Backend: menu_id="EMPLOYEE_MASTER"
Frontend: viewId="employee_master"  // ❌ Case mismatch!

✅ CORRECT:
Backend: menu_id="EMPLOYEE_MASTER"
Frontend: viewId="EMPLOYEE_MASTER"  // ✅ Exact match
```

---

### **❌ MISTAKE 4: Using Old Hook**

```
❌ WRONG:
import { useToolbarConfig } from '...';  // ❌ Old hook!
const { config } = useToolbarConfig(viewId);

✅ CORRECT:
// Don't call hook directly - MasterToolbar component handles it
<MasterToolbar viewId="..." mode={...} />
```

---

### **❌ MISTAKE 5: Only 3 Modes**

```
❌ WRONG:
const getMode = (): MasterMode => {
  if (!showForm) return 'VIEW';
  return editingId ? 'EDIT' : 'CREATE';
};

✅ CORRECT:
const getMode = (): MasterMode => {
  if (!showForm) return 'VIEW';
  if (viewMode) return 'VIEW_FORM';  // ← Read-only form
  return editingId ? 'EDIT' : 'CREATE';
};
```

---

### **❌ MISTAKE 6: Frontend Character Filtering**

```
❌ WRONG:
// Don't implement character filtering in frontend!
const VIEW_MODE_CHARS = 'NEVDXRQFZTJAPMI1234O';
const visibleChars = fullConfig.split('').filter(...);

✅ CORRECT:
// API returns action IDs directly - just use them
<MasterToolbar viewId="..." mode={...} />
```

---

## 10. 📞 NEED HELP?

**Questions**:
1. **"Which config string should I use?"** → Check Section 4 above
2. **"How do I handle workflow actions?"** → API returns them based on status
3. **"What if buttons don't show?"** → Check viewId matches menu_id exactly
4. **"Can I add custom buttons?"** → No, use standard actions only
5. **"How do I test the API?"** → Use browser DevTools Network tab

**Debugging**:
- Check browser console for API errors
- Verify `/api/toolbar-permissions/` endpoint exists
- Confirm `viewId` matches `menu_id` exactly (case-sensitive)
- Ensure mode is one of: VIEW, VIEW_FORM, CREATE, EDIT

---

## 11. 🔗 RELATED DOCUMENTATION

- **Retail Reference**: `.steering/20TOOLBAR_ROLLOUT/02_REFERENCE/MODE_BASED_FILTERING_TECHNICAL_REFERENCE.md`
- **Component Source**: `frontend/core/ui-canon/frontend/ui/components/MasterToolbarConfigDriven.tsx`
- **Hook Source**: `frontend/src/hooks/useToolbarPermissions.ts`
- **Universal Checklist**: `.steering/20TOOLBAR_ROLLOUT/01_ESSENTIAL/UNIVERSAL_TOOLBAR_IMPLEMENTATION_CHECKLIST.md`

---

**Status**: ✅ READY FOR USE  
**Version**: 2.0 (API-Driven Permission System)  
**Last Updated**: 2026-01-11 20:17 IST  
**For**: Agent E (HRM/CRM Development)
