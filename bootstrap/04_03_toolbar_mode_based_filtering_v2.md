# 🎨 MODE-BASED TOOLBAR FILTERING - TECHNICAL REFERENCE

**Purpose**: Explains how `MasterToolbar` filters buttons based on `mode` prop using API-driven permissions  
**Last Updated**: 2026-01-11 19:47 IST  
**Component**: `MasterToolbarConfigDriven.tsx`  
**Status**: ✅ PRODUCTION READY  
**Version**: 2.0 (API-Driven Permission System)

---

## 📜 VERSION HISTORY

| Version | Date | System | Description |
|---------|------|--------|-------------|
| **1.0** | 2026-01-09 | Character-Based | Frontend filtered character strings from backend |
| **2.0** | 2026-01-11 | API-Driven | Backend API returns filtered action IDs based on mode |

**Current System**: ✅ **API-Driven Permission System** (v2.0)

---

## 🎯 THE CORE CONCEPT

### **API-Driven, Mode-Aware Toolbar Permissions**

The `MasterToolbar` component uses a **backend API** to determine which toolbar buttons to display based on:
1. **Screen Identity** (`viewId`) - Which screen is being viewed
2. **UI Mode** (`mode`) - What the user is currently doing (viewing, creating, editing)
3. **User Permissions** - What the user is allowed to do (handled by backend)

**Flow**:
```
Frontend Component → API Request → Backend Logic → Filtered Actions → Rendered Buttons
```

**Example**:
```
Request:  GET /api/toolbar-permissions/?view_id=ITEM_MASTER&mode=VIEW
Response: { "allowed_actions": ["new", "edit", "view", "delete", "refresh", "search", "filter", "exit"] }
Result:   Only these 8 buttons are rendered in the toolbar
```

---

## 📊 HOW IT WORKS

### **Step 1: Frontend Determines Current Mode**

**Master Screen Example** (List + In-Place Form):
```typescript
const getToolbarMode = (): MasterMode => {
  if (!showForm) return 'VIEW';        // Viewing list
  if (viewMode) return 'VIEW_FORM';    // Viewing record (read-only)
  return editingId ? 'EDIT' : 'CREATE'; // Editing or creating
};
```

**Transaction Screen Example** (Separate Form Page):
```typescript
const getToolbarMode = (): MasterMode => {
  if (isReadOnly) return 'VIEW_FORM';   // Viewing submitted/approved record
  if (isNewRecord) return 'CREATE';     // Creating new transaction
  return 'EDIT';                        // Editing draft transaction
};
```

---

### **Step 2: Component Calls Backend API**

**Component Usage**:
```typescript
<MasterToolbar 
  viewId="ITEM_MASTER"           // ← Screen identifier
  mode={getToolbarMode()}        // ← Current UI mode
  onAction={handleToolbarAction} // ← Action handler
  hasSelection={!!selectedId}    // ← State for enabling/disabling buttons
/>
```

**API Request** (automatically made by `useToolbarPermissions` hook):
```http
GET /api/toolbar-permissions/?view_id=ITEM_MASTER&mode=VIEW
Authorization: Bearer <token>
```

**API Response**:
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
    "exit"
  ]
}
```

---

### **Step 3: Component Renders Filtered Buttons**

**Internal Logic** (`MasterToolbarConfigDriven.tsx`):
```typescript
const { allowedActions, loading, error } = useToolbarPermissions(viewId, mode);

const isActionVisible = (action: ActionButton): boolean => {
  return allowedActions.includes(action.id);
};

// Render only visible buttons
{ACTIONS
  .filter(a => isActionVisible(a))
  .map(action => <Button ... />)
}
```

**Result**: Only buttons in `allowedActions` array are rendered.

## 🔄 FEATURE FLAG SYSTEM

The component supports **both old and new permission systems** via a feature flag:

```typescript
// In MasterToolbarConfigDriven.tsx
const USE_NEW_PERMISSION_SYSTEM = true; // ✅ Currently ENABLED

const isActionVisible = (action: ActionButton): boolean => {
  if (USE_NEW_PERMISSION_SYSTEM) {
    // NEW: API-driven (current system)
    return allowedActions.includes(action.id);
  } else {
    // OLD: Hardcoded mode logic (fallback only)
    switch (mode) {
      case 'VIEW':
        return ['new', 'edit', 'view', 'delete', 'refresh', ...].includes(action.id);
      case 'CREATE':
      case 'EDIT':
        return ['save', 'cancel', 'clear', 'exit'].includes(action.id);
    }
  }
};
```

**Current Status**: ✅ API-driven system is **ACTIVE**  
**Fallback**: If API fails, component gracefully falls back to hardcoded logic

---

## 🔤 MODE-BASED FILTERING RULES

### **Supported Modes**

| Mode | Description | Use Case |
|------|-------------|----------|
| **VIEW** | Viewing list or browsing records | Master list, Transaction list |
| **VIEW_FORM** | Viewing single record (read-only) | Approved transactions, Read-only master view |
| **CREATE** | Creating new record | New master entry, New transaction |
| **EDIT** | Editing existing record | Modify draft master, Edit draft transaction |

---

### **VIEW Mode** (Browsing Lists or Records)

**Purpose**: User is viewing data (list or single record), not editing

**Typical Actions Returned by Backend**:
```json
{
  "allowed_actions": [
    "new",      // Create new record
    "edit",     // Edit selected record
    "view",     // View selected record (read-only)
    "delete",   // Delete/deactivate record
    "refresh",  // Reload list
    "search",   // Focus search box
    "filter",   // Toggle filter panel
    "import",   // Import data (optional)
    "export",   // Export data (optional)
    "exit"      // Navigate away
  ]
}
```

**Additional Actions for Transactions**:
```json
{
  "allowed_actions": [
    // ... all VIEW actions above, plus:
    "authorize", // Approve transaction
    "submit",    // Submit for approval
    "reject",    // Reject transaction
    "amend",     // Amend approved transaction
    "print",     // Print document
    "email",     // Email document
    "first",     // Navigate to first record
    "previous",  // Navigate to previous record
    "next",      // Navigate to next record
    "last"       // Navigate to last record
  ]
}
```

**Logic**: "User is viewing, so show navigation and actions, hide form controls"

---

### **VIEW_FORM Mode** (Read-Only Form View)

**Purpose**: User is viewing a single record in form layout, but cannot edit

**Typical Actions Returned by Backend**:
```json
{
  "allowed_actions": [
    "edit",      // Switch to edit mode
    "delete",    // Delete this record
    "print",     // Print document (transactions)
    "email",     // Email document (transactions)
    "clone",     // Clone this record (optional)
    "exit"       // Navigate away
  ]
}
```

**Logic**: "User is viewing form, so show view-related actions, hide save/cancel"

---

### **CREATE Mode** (Creating New Record)

**Purpose**: User is filling out a form to create new record

**Typical Actions Returned by Backend**:
```json
{
  "allowed_actions": [
    "save",      // Save new record
    "cancel",    // Cancel creation
    "clear",     // Clear form fields
    "exit",      // Navigate away
    "help",      // Show help (optional)
    "notes",     // Add notes (optional)
    "attach"     // Add attachments (optional)
  ]
}
```

**Logic**: "User is creating, so show only form controls and cancel option"

---

### **EDIT Mode** (Editing Existing Record)

**Purpose**: User is modifying an existing record

**Typical Actions Returned by Backend**:
```json
{
  "allowed_actions": [
    "save",      // Save changes
    "cancel",    // Cancel editing
    "clear",     // Reset form to original values
    "exit",      // Navigate away
    "help",      // Show help (optional)
    "notes",     // Add notes (optional)
    "attach"     // Add attachments (optional)
  ]
}
```

**Logic**: "User is editing, so show only form controls and cancel option"

---

## 🎯 PRACTICAL EXAMPLES

### **Example 1: Master Data Screen** (e.g., Item Master, Customer Master, Supplier Master)

**Pattern**: List + In-Place Form Swap

---

#### **Scenario A: Viewing List** (`/masters/items`)

```typescript
<MasterToolbar 
  viewId="ITEM_MASTER" 
  mode="VIEW"
  onAction={handleToolbarAction}
  hasSelection={!!selectedItemId}
/>
```

**API Response**:
```json
{
  "allowed_actions": ["new", "edit", "view", "delete", "refresh", "search", "filter", "import", "export", "exit"]
}
```

**Rendered Buttons**:
- ✅ New (F2) - Create new master record
- ✅ Edit (F3) - Edit selected record (disabled if no selection)
- ✅ View (F7) - View selected record (disabled if no selection)
- ✅ Delete (F4) - Delete selected record (disabled if no selection)
- ✅ Refresh (F9) - Reload list
- ✅ Search (Ctrl+F) - Focus search box
- ✅ Filter (Alt+F) - Toggle filters
- ✅ Import (Ctrl+I) - Import records
- ✅ Export (Ctrl+E) - Export records
- ✅ Exit (Esc) - Leave page

**Hidden**: Save, Cancel, Clear

---

#### **Scenario B: Creating New Record** (In-Place Form)

```typescript
<MasterToolbar 
  viewId="ITEM_MASTER" 
  mode="CREATE"
  onAction={handleToolbarAction}
/>
```

**API Response**:
```json
{
  "allowed_actions": ["save", "cancel", "clear", "exit"]
}
```

**Rendered Buttons**:
- ✅ Save (F8) - Save new record
- ✅ Cancel (Esc) - Cancel and return to list
- ✅ Clear (F5) - Clear form fields
- ✅ Exit (Esc) - Leave page

**Hidden**: New, Edit, View, Delete, Refresh, Search, Filter, Import, Export

---

#### **Scenario C: Editing Existing Record** (In-Place Form)

```typescript
<MasterToolbar 
  viewId="ITEM_MASTER" 
  mode="EDIT"
  onAction={handleToolbarAction}
/>
```

**API Response**:
```json
{
  "allowed_actions": ["save", "cancel", "clear", "exit"]
}
```

**Rendered Buttons**:
- ✅ Save (F8) - Save changes
- ✅ Cancel (Esc) - Cancel and return to list
- ✅ Clear (F5) - Reset form to original values
- ✅ Exit (Esc) - Leave page

**Hidden**: New, Edit, View, Delete, Refresh, Search, Filter, Import, Export

---

#### **Scenario D: Viewing Record (Read-Only)** (In-Place Form)

```typescript
<MasterToolbar 
  viewId="ITEM_MASTER" 
  mode="VIEW_FORM"
  onAction={handleToolbarAction}
/>
```

**API Response**:
```json
{
  "allowed_actions": ["edit", "delete", "clone", "exit"]
}
```

**Rendered Buttons**:
- ✅ Edit (F3) - Switch to edit mode
- ✅ Delete (F4) - Delete this record
- ✅ Clone (Ctrl+Shift+C) - Clone this record
- ✅ Exit (Esc) - Return to list

**Hidden**: Save, Cancel, Clear, New, Refresh, Search, Filter

---

### **Example 2: Transaction Screen** (e.g., Purchase Order, Sales Order, Transfer)

**Pattern**: Separate Form Page with Workflow

---

#### **Scenario A: Viewing Transaction List** (`/transactions/purchase-orders`)

```typescript
<MasterToolbar 
  viewId="PURCHASE_ORDERS" 
  mode="VIEW"
  onAction={handleToolbarAction}
  hasSelection={!!selectedOrderId}
/>
```

**API Response**:
```json
{
  "allowed_actions": ["new", "edit", "view", "delete", "refresh", "search", "filter", "export", "exit"]
}
```

**Rendered Buttons**:
- ✅ New (F2) - Create new transaction
- ✅ Edit (F3) - Edit selected transaction (disabled if no selection)
- ✅ View (F7) - View selected transaction (disabled if no selection)
- ✅ Delete (F4) - Delete selected transaction (disabled if no selection)
- ✅ Refresh (F9) - Reload list
- ✅ Search (Ctrl+F) - Focus search box
- ✅ Filter (Alt+F) - Toggle filters
- ✅ Export (Ctrl+E) - Export transactions
- ✅ Exit (Esc) - Leave page

**Hidden**: Save, Cancel, Clear, Authorize, Submit, Reject, Print, Email, Navigation

---

#### **Scenario B: Creating New Transaction** (`/transactions/purchase-orders/new`)

```typescript
<MasterToolbar 
  viewId="PURCHASE_ORDERS" 
  mode="CREATE"
  onAction={handleToolbarAction}
/>
```

**API Response**:
```json
{
  "allowed_actions": ["save", "cancel", "clear", "exit"]
}
```

**Rendered Buttons**:
- ✅ Save (F8) - Save new transaction (as DRAFT)
- ✅ Cancel (Esc) - Cancel and return to list
- ✅ Clear (F5) - Clear form fields
- ✅ Exit (Esc) - Leave page

**Hidden**: New, Edit, View, Delete, Refresh, Search, Filter, Authorize, Submit, Print, Email

---

#### **Scenario C: Editing Draft Transaction** (`/transactions/purchase-orders/123`)

```typescript
<MasterToolbar 
  viewId="PURCHASE_ORDERS" 
  mode="EDIT"
  onAction={handleToolbarAction}
/>
```

**API Response**:
```json
{
  "allowed_actions": ["save", "cancel", "clear", "submit", "exit"]
}
```

**Rendered Buttons**:
- ✅ Save (F8) - Save changes
- ✅ Submit (Alt+S) - Submit for approval
- ✅ Cancel (Esc) - Cancel and return to list
- ✅ Clear (F5) - Reset form to saved values
- ✅ Exit (Esc) - Leave page

**Hidden**: New, Edit, View, Delete, Refresh, Search, Filter, Authorize, Reject, Print, Email

---

#### **Scenario D: Viewing Submitted Transaction** (`/transactions/purchase-orders/123`)

```typescript
<MasterToolbar 
  viewId="PURCHASE_ORDERS" 
  mode="VIEW_FORM"
  onAction={handleToolbarAction}
/>
```

**API Response** (for approver):
```json
{
  "allowed_actions": ["authorize", "reject", "print", "email", "first", "previous", "next", "last", "exit"]
}
```

**Rendered Buttons**:
- ✅ Authorize (F10) - Approve transaction
- ✅ Reject (Alt+R) - Reject transaction
- ✅ Print (Ctrl+P) - Print document
- ✅ Email (Ctrl+M) - Email document
- ✅ First (Home) - Navigate to first transaction
- ✅ Previous (PgUp) - Navigate to previous transaction
- ✅ Next (PgDn) - Navigate to next transaction
- ✅ Last (End) - Navigate to last transaction
- ✅ Exit (Esc) - Leave page

**Hidden**: Save, Cancel, Clear, New, Edit, Delete, Refresh, Search, Filter

---

#### **Scenario E: Viewing Approved Transaction** (`/transactions/purchase-orders/123`)

```typescript
<MasterToolbar 
  viewId="PURCHASE_ORDERS" 
  mode="VIEW_FORM"
  onAction={handleToolbarAction}
/>
```

**API Response**:
```json
{
  "allowed_actions": ["amend", "print", "email", "clone", "first", "previous", "next", "last", "exit"]
}
```

**Rendered Buttons**:
- ✅ Amend (Alt+A) - Amend approved transaction
- ✅ Print (Ctrl+P) - Print document
- ✅ Email (Ctrl+M) - Email document
- ✅ Clone (Ctrl+Shift+C) - Clone this transaction
- ✅ First (Home) - Navigate to first transaction
- ✅ Previous (PgUp) - Navigate to previous transaction
- ✅ Next (PgDn) - Navigate to next transaction
- ✅ Last (End) - Navigate to last transaction
- ✅ Exit (Esc) - Leave page

**Hidden**: Save, Cancel, Clear, New, Edit, Delete, Refresh, Search, Filter, Authorize, Submit, Reject

---
## 🔧 IMPLEMENTATION DETAILS

### **Component Architecture** (`MasterToolbarConfigDriven.tsx`)

```typescript
// Actual implementation (simplified for clarity)

export const MasterToolbar: React.FC<MasterToolbarProps> = ({
  viewId,
  mode,
  onAction,
  hasSelection = false
}) => {
  // 1. Fetch allowed actions from backend API
  const { allowedActions, loading, error } = useToolbarPermissions(
    viewId,
    mode,
    !USE_NEW_PERMISSION_SYSTEM // skip if using fallback
  );

  // 2. Determine if action should be visible
  const isActionVisible = (action: ActionButton): boolean => {
    if (USE_NEW_PERMISSION_SYSTEM) {
      // API-driven: Check if action is in allowed list
      return allowedActions.includes(action.id);
    } else {
      // Fallback: Hardcoded mode logic
      switch (mode) {
        case 'VIEW':
          return ['new', 'edit', 'view', 'delete', 'refresh', ...].includes(action.id);
        case 'CREATE':
        case 'EDIT':
          return ['save', 'cancel', 'clear', 'exit'].includes(action.id);
      }
    }
  };

  // 3. Determine if action should be enabled (state-based)
  const isActionEnabled = (action: ActionButton): boolean => {
    // Edit/Delete/View require selection
    if (['edit', 'delete', 'view'].includes(action.id) && !hasSelection) {
      return false;
    }
    return true;
  };

  // 4. Render filtered and enabled buttons
  return (
    <div className="toolbar">
      {ACTIONS
        .filter(a => isActionVisible(a))
        .map(action => (
          <button
            onClick={() => onAction(action.id)}
            disabled={!isActionEnabled(action)}
          >
            <action.icon />
            {action.label}
          </button>
        ))
      }
    </div>
  );
};
```

---

### **useToolbarPermissions Hook**

```typescript
export const useToolbarPermissions = (
  viewId: string,
  mode: MasterMode,
  skip: boolean = false
) => {
  const [allowedActions, setAllowedActions] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (skip) {
      setLoading(false);
      return;
    }

    const fetchPermissions = async () => {
      try {
        // Call backend API
        const response = await fetch(
          `/api/toolbar-permissions/?view_id=${viewId}&mode=${mode}`,
          {
            headers: {
              'Authorization': `Bearer ${getAuthToken()}`
            }
          }
        );

        const data = await response.json();
        setAllowedActions(data.allowed_actions);
        setLoading(false);
      } catch (err) {
        setError('Failed to load toolbar permissions');
        setLoading(false);
      }
    };

    fetchPermissions();
  }, [viewId, mode, skip]);

  return { allowedActions, loading, error };
};
```

---

## 📋 ACTION VISIBILITY MATRIX

**Note**: This matrix shows typical backend API behavior for each mode. Actual actions may vary based on user permissions and screen configuration.

| Action ID | Description | VIEW Mode | VIEW_FORM Mode | CREATE Mode | EDIT Mode |
|-----------|-------------|-----------|----------------|-------------|-----------|
| **new** | Create new record | ✅ Show | ❌ Hide | ❌ Hide | ❌ Hide |
| **edit** | Edit selected record | ✅ Show | ✅ Show | ❌ Hide | ❌ Hide |
| **view** | View selected record | ✅ Show | ❌ Hide | ❌ Hide | ❌ Hide |
| **save** | Save changes | ❌ Hide | ❌ Hide | ✅ Show | ✅ Show |
| **cancel** | Cancel operation | ❌ Hide | ❌ Hide | ✅ Show | ✅ Show |
| **clear** | Clear/Reset form | ❌ Hide | ❌ Hide | ✅ Show | ✅ Show |
| **delete** | Delete record | ✅ Show | ✅ Show | ❌ Hide | ❌ Hide |
| **refresh** | Reload list | ✅ Show | ❌ Hide | ❌ Hide | ❌ Hide |
| **search** | Focus search box | ✅ Show | ❌ Hide | ❌ Hide | ❌ Hide |
| **filter** | Toggle filters | ✅ Show | ❌ Hide | ❌ Hide | ❌ Hide |
| **exit** | Navigate away | ✅ Show | ✅ Show | ✅ Show | ✅ Show |
| **import** | Import data | ✅ Show | ❌ Hide | ❌ Hide | ❌ Hide |
| **export** | Export data | ✅ Show | ❌ Hide | ❌ Hide | ❌ Hide |
| **clone** | Clone record | ❌ Hide | ✅ Show | ❌ Hide | ❌ Hide |

### **Transaction-Specific Actions**

| Action ID | Description | VIEW Mode | VIEW_FORM Mode | CREATE Mode | EDIT Mode |
|-----------|-------------|-----------|----------------|-------------|-----------|
| **submit** | Submit for approval | ❌ Hide | ❌ Hide | ❌ Hide | ✅ Show* |
| **authorize** | Approve transaction | ✅ Show* | ✅ Show* | ❌ Hide | ❌ Hide |
| **reject** | Reject transaction | ✅ Show* | ✅ Show* | ❌ Hide | ❌ Hide |
| **amend** | Amend approved | ✅ Show* | ✅ Show* | ❌ Hide | ❌ Hide |
| **print** | Print document | ✅ Show* | ✅ Show | ❌ Hide | ❌ Hide |
| **email** | Email document | ✅ Show* | ✅ Show | ❌ Hide | ❌ Hide |
| **first** | First record | ✅ Show* | ✅ Show | ❌ Hide | ❌ Hide |
| **previous** | Previous record | ✅ Show* | ✅ Show | ❌ Hide | ❌ Hide |
| **next** | Next record | ✅ Show* | ✅ Show | ❌ Hide | ❌ Hide |
| **last** | Last record | ✅ Show* | ✅ Show | ❌ Hide | ❌ Hide |

**\* Conditional**: Shown based on transaction status and user role

---

## ✅ BENEFITS OF API-DRIVEN APPROACH

### **1. Backend Controls Everything**
- **Single Source of Truth**: Backend API determines all permissions
- **Dynamic Permissions**: Can change based on user role, record status, business rules
- **Security**: Frontend cannot bypass permission checks
- **Auditability**: All permission decisions logged on backend

### **2. Context-Aware UI**
- **Mode-Based**: Different buttons for viewing vs editing
- **Status-Based**: Different buttons for draft vs approved transactions
- **Role-Based**: Different buttons for creator vs approver
- **Automatic Adaptation**: UI updates based on backend response

### **3. No Frontend Hardcoding**
- **API-Driven**: Frontend doesn't decide which buttons to show
- **Flexible**: Easy to add new actions without frontend changes
- **Consistent**: Same logic across all screens
- **Maintainable**: Permission logic centralized in backend

### **4. Graceful Degradation**
- **Feature Flag**: Can toggle between API-driven and fallback mode
- **Error Handling**: Falls back to hardcoded logic if API fails
- **Loading States**: Shows loading indicator while fetching permissions
- **Resilient**: System works even if backend is slow

---

## 🚀 USAGE PATTERN

### **For Master Data Screens** (List + In-Place Form):

```typescript
import { MasterToolbar, MasterMode } from '@core/ui-canon/frontend/ui/components/MasterToolbarConfigDriven';

const MasterDataScreen = () => {
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState(false);
  const [selectedId, setSelectedId] = useState<string | null>(null);

  // Determine current mode
  const getToolbarMode = (): MasterMode => {
    if (!showForm) return 'VIEW';        // Viewing list
    if (viewMode) return 'VIEW_FORM';    // Viewing record (read-only)
    return editingId ? 'EDIT' : 'CREATE'; // Editing or creating
  };

  const handleToolbarAction = (action: string) => {
    switch (action) {
      case 'new':
        setEditingId(null);
        setViewMode(false);
        setShowForm(true);
        break;
      case 'edit':
        if (selectedId) {
          setEditingId(selectedId);
          setViewMode(false);
          setShowForm(true);
        }
        break;
      case 'view':
        if (selectedId) {
          setEditingId(selectedId);
          setViewMode(true);
          setShowForm(true);
        }
        break;
      case 'save':
        // Save logic
        break;
      case 'cancel':
        setShowForm(false);
        setEditingId(null);
        setViewMode(false);
        break;
      // ... other actions
    }
  };

  return (
    <div>
      <MasterToolbar 
        viewId="ITEM_MASTER"
        mode={getToolbarMode()}
        onAction={handleToolbarAction}
        hasSelection={!!selectedId}
      />
      
      {showForm ? (
        <FormComponent 
          id={editingId}
          readOnly={viewMode}
        />
      ) : (
        <ListComponent 
          onSelect={setSelectedId}
        />
      )}
    </div>
  );
};
```

---

### **For Transaction Screens** (Separate Form Page):

```typescript
import { MasterToolbar, MasterMode } from '@core/ui-canon/frontend/ui/components/MasterToolbarConfigDriven';

const TransactionFormPage = () => {
  const { id } = useParams();
  const [transaction, setTransaction] = useState<Transaction | null>(null);
  const isNew = !id;

  // Determine current mode based on transaction status
  const getToolbarMode = (): MasterMode => {
    if (isNew) return 'CREATE';
    if (transaction?.status === 'DRAFT') return 'EDIT';
    return 'VIEW_FORM'; // Submitted/Approved transactions are read-only
  };

  const handleToolbarAction = (action: string) => {
    switch (action) {
      case 'save':
        // Save transaction
        break;
      case 'submit':
        // Submit for approval
        break;
      case 'authorize':
        // Approve transaction
        break;
      case 'reject':
        // Reject transaction
        break;
      case 'print':
        // Print document
        break;
      // ... other actions
    }
  };

  return (
    <div>
      <MasterToolbar 
        viewId="PURCHASE_ORDERS"
        mode={getToolbarMode()}
        onAction={handleToolbarAction}
      />
      
      <TransactionForm 
        transaction={transaction}
        readOnly={getToolbarMode() === 'VIEW_FORM'}
      />
    </div>
  );
};
```

---

## 📊 REAL-WORLD SCENARIOS

### **Scenario 1: User Browsing Master Data List**
```
User Action: Opens /masters/items
Frontend Mode: VIEW
API Request: GET /api/toolbar-permissions/?view_id=ITEM_MASTER&mode=VIEW
API Response: ["new", "edit", "view", "delete", "refresh", "search", "filter", "import", "export", "exit"]
Rendered Buttons: New, Edit, View, Delete, Refresh, Search, Filter, Import, Export, Exit
User Can: Create new, edit selected, view selected, search, filter
User Cannot: Save, Cancel, Clear (no form active)
```

### **Scenario 2: User Creating New Master Record**
```
User Action: Clicks "New" button
Frontend Mode: CREATE
API Request: GET /api/toolbar-permissions/?view_id=ITEM_MASTER&mode=CREATE
API Response: ["save", "cancel", "clear", "exit"]
Rendered Buttons: Save, Cancel, Clear, Exit
User Can: Save new record, cancel creation, clear form
User Cannot: Edit, Delete, Refresh, Search (form is active)
```

### **Scenario 3: User Viewing Transaction (Read-Only)**
```
User Action: Opens approved transaction
Frontend Mode: VIEW_FORM
API Request: GET /api/toolbar-permissions/?view_id=PURCHASE_ORDERS&mode=VIEW_FORM
API Response: ["print", "email", "clone", "first", "previous", "next", "last", "exit"]
Rendered Buttons: Print, Email, Clone, Navigation buttons, Exit
User Can: Print, email, clone, navigate between records
User Cannot: Edit, Save, Delete (transaction is approved)
```

### **Scenario 4: User Editing Draft Transaction**
```
User Action: Opens draft transaction
Frontend Mode: EDIT
API Request: GET /api/toolbar-permissions/?view_id=PURCHASE_ORDERS&mode=EDIT
API Response: ["save", "cancel", "clear", "submit", "exit"]
Rendered Buttons: Save, Submit, Cancel, Clear, Exit
User Can: Save changes, submit for approval, cancel editing
User Cannot: Authorize, Print, Email (transaction not submitted yet)
```

### **Scenario 5: Approver Reviewing Submitted Transaction**
```
User Action: Opens submitted transaction (as approver)
Frontend Mode: VIEW_FORM
API Request: GET /api/toolbar-permissions/?view_id=PURCHASE_ORDERS&mode=VIEW_FORM&user_role=APPROVER
API Response: ["authorize", "reject", "print", "email", "first", "previous", "next", "last", "exit"]
Rendered Buttons: Authorize, Reject, Print, Email, Navigation, Exit
User Can: Approve, reject, print, email, navigate
User Cannot: Edit, Save, Delete (transaction is locked for approval)
```

---

## 🎯 KEY TAKEAWAYS

1. **API-Driven Permissions**: Backend API determines which buttons to show based on `viewId`, `mode`, user role, and record status

2. **Four Modes Supported**: 
   - `VIEW` - Browsing lists or records
   - `VIEW_FORM` - Viewing single record (read-only)
   - `CREATE` - Creating new record
   - `EDIT` - Editing existing record

3. **Context-Aware UI**: Same screen shows different buttons based on what user is doing and what they're allowed to do

4. **Security First**: Frontend cannot bypass permission checks - all decisions made by backend

5. **Graceful Degradation**: System falls back to hardcoded logic if API fails, ensuring resilience

6. **Generic Patterns**: Same implementation works for both Master Data and Transaction screens

7. **State-Based Enabling**: Some buttons (Edit, Delete, View) are disabled based on selection state

8. **Consistent Experience**: Same toolbar behavior across all screens in the application

---

## 🔗 RELATED DOCUMENTATION

- **Component Source**: `frontend/core/ui-canon/frontend/ui/components/MasterToolbarConfigDriven.tsx`
- **Hook Source**: `frontend/src/hooks/useToolbarPermissions.ts`
- **Backend API**: `/api/toolbar-permissions/` (Django REST Framework endpoint)
- **Example Implementation**: `frontend/apps/retail/inventory/pages/ItemMasterSetup.tsx`
- **UI Gold Standard**: `.steering/20TOOLBAR_ROLLOUT/04_ARCHIVE/UOM/UOM_TOOLBAR_ACTION_AND_CHECKLIST_MANUAL.md`

---

**Status**: ✅ PRODUCTION READY  
**Version**: 2.0 (API-Driven Permission System)  
**Last Updated**: 2026-01-11 19:47 IST  
**Component**: `MasterToolbarConfigDriven.tsx`  
**Pattern**: API-driven, mode-based toolbar filtering with graceful fallback

