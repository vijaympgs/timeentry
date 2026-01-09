# 🛠️ TOOLBAR IMPLEMENTATION GUIDE (Standardized)
**Target Agents**: Astra (Retail/FMS), Agent E (HRM/CRM)  
**Objective**: Ensure 100% UI consistency across all ERP modules using Backend-Driven Toolbars.

---

## 1. THE ARCHITECTURE
The ERP uses a **Character-Based Configuration** system. Instead of hardcoding which buttons appear on which page, the backend provides a string of codes. 

**Example**: `NRQFX` 
- `N`: New
- `R`: Refresh
- `Q`: Search
- `F`: Filter
- `X`: Exit

| Component | Responsibility |
|-----------|----------------|
| **Backend Model** | `ERPMenuItem` stores the `applicable_toolbar_config` (the string). |
| **API Endpoint** | Delivering the config along with user permissions. |
| **`useToolbarConfig`** | React Hook that parses the string into a boolean object. |
| **`MasterToolbar`** | The UI component that renders buttons based on the parsed object. |

---

## 2. THE CHARACTER MAP (Master Registry)
Reference this table when configuring the `applicable_toolbar_config` in Django Admin.

### CRUD & Navigation (Standard)
| Code | Action | Shortcut | Mode Behavior |
|------|--------|----------|---------------|
| **N** | New | F2 | Visible in VIEW |
| **E** | Edit | F3 | Visible in VIEW |
| **S** | **SAVE** | F8 | Visible in CREATE/EDIT |
| **C** | **CANCEL** | ESC | Visible in CREATE/EDIT |
| **K** | **CLEAR** | F5 | Visible in CREATE/EDIT |
| **D** | Delete | F4 | Visible in VIEW |
| **X** | **EXIT** | ESC | Always visible |

### Workflow & Transactions
| Code | Action | Shortcut | Description |
|------|--------|----------|-------------|
| **T** | Submit | Alt+S | Transition to next status |
| **J** | Reject | Alt+R | Decline document |
| **A** | Authorize| F10 | Manager approval |
| **H** | Hold | Alt+H | Suspend transaction |
| **Z** | Void | Alt+V | Annul/Reverse entry |
| **W** | Amend | Alt+A | Modify authorized doc |

### Data & Tools
| Code | Action | Description |
|------|--------|-------------|
| **V** | View | Detail view/drill down |
| **R** | Refresh | Reload grid data |
| **Q** | Search | Primary search focus |
| **F** | Filter | Advanced filter toggle |
| **B** | Notes | Internal remarks/comments |
| **U** | Attach | File uploads |

---

## 3. HOW TO IMPLEMENT (Step-by-Step)

### Step 1: Backend Registration
Every page must be registered in the `ERPMenuItem` table.
- **`menu_id`**: Assign a unique name (e.g., `HRM_LEAVE_APPLICATION`).
- **`applicable_toolbar_config`**: Assign the standard string (e.g., `NESCKPVDXRTJZ` for transactions).

### Step 2: Frontend Layout
Import the `MasterToolbar` and wire it to your page.

```tsx
import { MasterToolbar, MasterMode } from "../core/ui-canon/frontend/ui/components/MasterToolbarConfigDriven";

export const MyPage = () => {
    const [mode, setMode] = useState<MasterMode>('VIEW');
    
    // Wire the common handler
    const handleAction = (id: string) => {
        if (id === 'new') setMode('CREATE');
        if (id === 'save') { /* logic */; setMode('VIEW'); }
        if (id === 'exit') navigate('/dashboard');
    };

    return (
        <>
            <MasterToolbar 
                viewId="HRM_LEAVE_APPLICATION" // Must match DB ID
                mode={mode} 
                onAction={handleAction} 
            />
            <div className="content">...</div>
        </>
    );
}
```

### Step 3: Mode Management
The toolbar's visual state is driven by the `mode` prop.
- **`VIEW`**: Shows navigation, search, new, edit, and workflow.
- **`EDIT`/`CREATE`**: Swaps the toolbar to show only **Save, Cancel, Clear, and Help**.

---

## 4. REFERENCE ASSETS
The following files are source-of-truth copies for replication:
1. `toolbar_reference/MasterToolbarConfigDriven.tsx` (Frontend Core)
2. `toolbar_reference/models_reference.py` (Backend Logic)
3. `toolbar_reference/WiringSample.tsx` (Implementation Example)
4. `toolbar_reference/toolbar_config.json` (Mapping Reference)
5. `toolbar_reference/toolbar-demo.html` (Interactive Behavior Inspector)

**Location**: `.steering/18_WIRING_CHECKLISTS/toolbar_reference/`

---

## 5. INTERACTIVE BEHAVIOR GUIDE
For a live understanding of how the toolbar shifts between modes and pages, refer to:
👉 `toolbar_reference/toolbar-demo.html`

### **Key Behavioral Transitions**:
1. **From List to Form (The "+" Flow)**:
   - When in a List View (Mode: `VIEW`), clicking **New (+)** should NOT just open a modal if it's a complex record.
   - It should transition the UI to `NEW` mode.
   - The Toolbar will automatically swap from "List Actions" (Search, Filter, Export) to "Form Actions" (Save, Cancel, Clear).

2. **From View to Edit (The "Edit" Flow)**:
   - Selecting a record and clicking **Edit (F3)** transitions the mode to `EDIT`.
   - The toolbar hides "Delete" and "New" and shows "Save" and "Cancel".

3. **Escaping/Cancelling**:
   - The `Cancel` action (Esc) in `EDIT/NEW` mode must always return the user to `VIEW` mode, discarding unsaved changes.

4. **Multi-Select Behavior (List Views)**:
   - **Allowed Actions**: Bulk actions like **Authorize (A)** and **Delete (D)** are permitted when multiple rows are selected.
   - **Blocked Actions**: Single-record actions like **View (V)**, **Edit (E)**, or **Clone (L)** should remain disabled or trigger a "This action is not allowed for multiple records" notification if selection length > 1.

### **Specialized Action Guidance**:
- **Amend (W)**: Applicable only for authorized documents (e.g., PO/SO). Primary use is for Quantity changes. Controlled by future Business Rules pages.
- **Clone (L)**: Purpose is to duplicate an existing Order (PO/SO) into a new record. Switches UI to `NEW` mode with prepopulated data.
