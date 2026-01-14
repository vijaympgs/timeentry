# TOOLBAR IMPLEMENTATION - COMPLETE CODE EXAMPLES (v2.0)

**Purpose**: Complete, copy-paste code examples for implementing API-driven toolbars  
**For**: Agent E (HRM/CRM Development)  
**Version**: 2.0 (API-Driven Permission System)  
**Last Updated**: 2026-01-11 20:17 IST  
**Status**: ✅ PRODUCTION READY

---

## 📜 VERSION HISTORY

| Version | Date | System | Key Change |
|---------|------|--------|------------|
| **1.0** | 2026-01-09 | Character-Based | Frontend filtered character strings |
| **2.0** | 2026-01-11 | API-Driven | Backend API returns filtered action IDs |

**Current System**: ✅ **API-Driven** (v2.0)

---

## 🎯 CRITICAL ARCHITECTURE RULE

### **ONE SCREEN = ONE DATABASE ENTRY**

```
❌ WRONG: 
ERPMenuItem #1: menu_id="employee-list", view_type="LIST_VIEW"  
ERPMenuItem #2: menu_id="EMPLOYEE_MASTER", view_type="MASTER"

✅ CORRECT: 
ERPMenuItem: menu_id="EMPLOYEE_MASTER", view_type="MASTER"
    Frontend handles BOTH:
    - List page: mode="VIEW"
    - Form page: mode="VIEW_FORM|CREATE|EDIT"
```

---

## 📋 PART 1: BACKEND SETUP

### **Step 1: Create ERPMenuItem Entry**

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

**Note**: The `toolbar_config` is used by backend API to determine base permissions. The API endpoint filters this based on mode and user permissions.

---

### **Step 2: Toolbar Configuration Strings**

**Choose based on screen type**:

#### **Masters (Simple)** - Basic CRUD

```
Config: NESCKVDXRQF
Base Actions: New, Edit, Save, Cancel, Clear, View, Delete, Exit, Refresh, Search, Filter

Example screens:
- Department
- Position  
- Leave Type
- Contact Category
```

#### **Masters (Advanced)** - With Import/Export

```
Config: NESCKVDXRQFIO
Base Actions: Above + Import, Export

Example screens:
- Employee Master
- Contact Master
- Account Master
```

#### **Transactions** - Full Workflow

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

#### **Reports** - Read-Only

```
Config: VRXPYQFG
Base Actions: View, Refresh, Exit, Print, Export, Search, Filter, Generate

Example screens:
- Employee Directory Report
- Leave Balance Report
- Sales Pipeline Report
```

---

## 📋 PART 2: FRONTEND IMPLEMENTATION

### **Example 1: Employee Master (HRM) - Master Data Pattern**

#### **File**: `frontend/apps/hrm/employee/pages/EmployeeSetup.tsx`

```typescript
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { MasterToolbar, MasterMode } from '@core/ui-canon/frontend/ui/components/MasterToolbarConfigDriven';
import { ConfirmationDialog } from '@core/ui-canon/frontend/ui/components/ConfirmationDialog';
import { EmployeeForm } from './EmployeeForm';
import { EmployeeList } from './EmployeeList';

export const EmployeeSetup: React.FC = () => {
  const navigate = useNavigate();
  
  // State management
  const [employees, setEmployees] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState(false); // Read-only view
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [showFilterPanel, setShowFilterPanel] = useState(true);
  
  // Dialog states
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [isCancelDialogOpen, setIsCancelDialogOpen] = useState(false);
  const [isExitDialogOpen, setIsExitDialogOpen] = useState(false);
  
  // Determine toolbar mode (4 modes supported)
  const getToolbarMode = (): MasterMode => {
    if (!showForm) return 'VIEW';        // Viewing list
    if (viewMode) return 'VIEW_FORM';    // Viewing record (read-only)
    return editingId ? 'EDIT' : 'CREATE'; // Editing or creating
  };
  
  // Load employees
  useEffect(() => {
    loadEmployees();
  }, []);
  
  const loadEmployees = async () => {
    try {
      // Call your API
      const data = await employeeService.getAll();
      setEmployees(data);
    } catch (error) {
      console.error('Failed to load employees:', error);
    }
  };
  
  // Handle toolbar actions
  const handleToolbarAction = (action: string) => {
    switch (action) {
      case 'new':
        setEditingId(null);
        setViewMode(false);
        setShowForm(true);
        break;
      
      case 'edit':
        if (selectedId && !showForm) {
          setEditingId(selectedId);
          setViewMode(false);
          setShowForm(true);
        }
        break;
      
      case 'view':
        if (selectedId && !showForm) {
          setEditingId(selectedId);
          setViewMode(true);
          setShowForm(true);
        }
        break;
      
      case 'save':
        if (showForm) {
          // Form component will handle save
          // This is triggered by form's save button
          console.log('Save triggered from toolbar');
        }
        break;
      
      case 'cancel':
        if (showForm) {
          // Show confirmation if form has changes
          setIsCancelDialogOpen(true);
        }
        break;
      
      case 'clear':
        if (showForm) {
          // Clear form fields (form component handles this)
          console.log('Clear form fields');
        }
        break;
      
      case 'delete':
        if (selectedId && !showForm) {
          setIsDeleteDialogOpen(true);
        }
        break;
      
      case 'refresh':
        loadEmployees();
        break;
      
      case 'search':
        // Focus search input
        document.querySelector<HTMLInputElement>('input[type="text"]')?.focus();
        break;
      
      case 'filter':
        setShowFilterPanel(!showFilterPanel);
        break;
      
      case 'import':
        alert('Import functionality coming soon');
        break;
      
      case 'export':
        alert('Export functionality coming soon');
        break;
      
      case 'exit':
        if (showForm) {
          // From form, check for unsaved changes
          setIsExitDialogOpen(true);
        } else {
          // From list, navigate to dashboard
          navigate('/dashboard');
        }
        break;
    }
  };
  
  // Confirmation handlers
  const handleConfirmDelete = async () => {
    if (selectedId) {
      try {
        await employeeService.delete(selectedId);
        setIsDeleteDialogOpen(false);
        setSelectedId(null);
        loadEmployees();
      } catch (error) {
        console.error('Failed to delete employee:', error);
      }
    }
  };
  
  const handleConfirmCancel = () => {
    setShowForm(false);
    setEditingId(null);
    setViewMode(false);
    setIsCancelDialogOpen(false);
  };
  
  const handleConfirmExit = () => {
    setShowForm(false);
    setEditingId(null);
    setViewMode(false);
    setIsExitDialogOpen(false);
  };
  
  const handleSaveSuccess = () => {
    setShowForm(false);
    setEditingId(null);
    setViewMode(false);
    loadEmployees();
  };
  
  return (
    <>
      {/* Toolbar - Backend API determines which buttons show */}
      <MasterToolbar
        viewId="EMPLOYEE_MASTER"  // Must match backend menu_id exactly
        mode={getToolbarMode()}    // VIEW, VIEW_FORM, CREATE, or EDIT
        onAction={handleToolbarAction}
        hasSelection={!!selectedId}
        showLabels={false}
        // ❌ DO NOT ADD: allowedActions={[...]} - Backend API controls this!
      />
      
      <div className="page-container space-y-6">
        {/* Page header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl font-semibold text-[#201f1e]">
              Employee Directory
            </h1>
            <p className="text-sm text-[#605e5c]">
              Manage employee information
            </p>
          </div>
        </div>
        
        {/* Show form or list based on state */}
        {showForm ? (
          <EmployeeForm
            id={editingId}
            readOnly={viewMode}
            onSave={handleSaveSuccess}
            onCancel={() => setIsCancelDialogOpen(true)}
          />
        ) : (
          <>
            {/* Filter panel */}
            {showFilterPanel && (
              <div className="bg-white p-4 shadow-sm border border-gray-200">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                  <input
                    type="text"
                    placeholder="Search employees..."
                    className="px-3 py-2 border border-gray-300 rounded-sm text-sm focus:border-[#0078d4] outline-none"
                  />
                  {/* More filters */}
                </div>
              </div>
            )}
            
            {/* Employee list */}
            <EmployeeList
              employees={employees}
              selectedId={selectedId}
              onSelect={setSelectedId}
            />
          </>
        )}
      </div>
      
      {/* Confirmation Dialogs */}
      <ConfirmationDialog
        isOpen={isDeleteDialogOpen}
        onClose={() => setIsDeleteDialogOpen(false)}
        onConfirm={handleConfirmDelete}
        title="Delete Employee"
        message="Are you sure you want to delete this employee? This action cannot be undone."
        confirmText="Delete"
        cancelText="Cancel"
        variant="danger"
      />
      
      <ConfirmationDialog
        isOpen={isCancelDialogOpen}
        onClose={() => setIsCancelDialogOpen(false)}
        onConfirm={handleConfirmCancel}
        title="Cancel Changes"
        message="You have unsaved changes. Are you sure you want to cancel?"
        confirmText="Yes, Cancel"
        cancelText="No, Keep Editing"
        variant="warning"
      />
      
      <ConfirmationDialog
        isOpen={isExitDialogOpen}
        onClose={() => setIsExitDialogOpen(false)}
        onConfirm={handleConfirmExit}
        title="Exit Without Saving"
        message="You have unsaved changes. Are you sure you want to exit?"
        confirmText="Yes, Exit"
        cancelText="No, Stay Here"
        variant="warning"
      />
    </>
  );
};
```

---

### **Example 2: Leave Request (HRM Transaction) - Transaction Pattern**

#### **File**: `frontend/apps/hrm/leave/pages/LeaveRequestFormPage.tsx`

```typescript
import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { MasterToolbar, MasterMode } from '@core/ui-canon/frontend/ui/components/MasterToolbarConfigDriven';
import { ConfirmationDialog } from '@core/ui-canon/frontend/ui/components/ConfirmationDialog';

export const LeaveRequestFormPage: React.FC = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  
  // State
  const [leaveRequest, setLeaveRequest] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  
  // Dialog states
  const [isCancelDialogOpen, setIsCancelDialogOpen] = useState(false);
  const [isSubmitDialogOpen, setIsSubmitDialogOpen] = useState(false);
  const [isAuthorizeDialogOpen, setIsAuthorizeDialogOpen] = useState(false);
  const [isRejectDialogOpen, setIsRejectDialogOpen] = useState(false);
  
  // Determine mode based on transaction status
  const getMode = (): MasterMode => {
    if (!id) return 'CREATE';                          // New transaction
    if (!leaveRequest) return 'VIEW_FORM';             // Loading
    if (leaveRequest.status === 'DRAFT') return 'EDIT'; // Draft - can edit
    return 'VIEW_FORM';                                 // Submitted/Approved - read-only
  };
  
  // Load leave request
  useEffect(() => {
    if (id) {
      loadLeaveRequest();
    } else {
      setIsLoading(false);
    }
  }, [id]);
  
  const loadLeaveRequest = async () => {
    try {
      const data = await leaveRequestService.getById(id);
      setLeaveRequest(data);
      setIsLoading(false);
    } catch (error) {
      console.error('Failed to load leave request:', error);
      setIsLoading(false);
    }
  };
  
  // Handle toolbar actions
  const handleToolbarAction = (action: string) => {
    switch (action) {
      case 'new':
        navigate('/hrm/leave-requests/new');
        break;
      
      case 'edit':
        // Switch to edit mode (if allowed)
        console.log('Edit mode activated');
        break;
      
      case 'save':
        // Save logic
        handleSave();
        break;
      
      case 'cancel':
        if (!id) {
          // New record - navigate back to list
          setIsCancelDialogOpen(true);
        } else {
          // Editing - reload original data
          loadLeaveRequest();
        }
        break;
      
      case 'clear':
        // Clear form fields
        console.log('Clear form');
        break;
      
      case 'submit':
        // Submit for approval
        setIsSubmitDialogOpen(true);
        break;
      
      case 'authorize':
        // Approve request
        setIsAuthorizeDialogOpen(true);
        break;
      
      case 'reject':
        // Reject request
        setIsRejectDialogOpen(true);
        break;
      
      case 'print':
        window.print();
        break;
      
      case 'email':
        alert('Email functionality coming soon');
        break;
      
      case 'first':
        // Navigate to first record
        console.log('Navigate to first');
        break;
      
      case 'previous':
        // Navigate to previous record
        console.log('Navigate to previous');
        break;
      
      case 'next':
        // Navigate to next record
        console.log('Navigate to next');
        break;
      
      case 'last':
        // Navigate to last record
        console.log('Navigate to last');
        break;
      
      case 'exit':
        navigate('/hrm/leave-requests');
        break;
    }
  };
  
  const handleSave = async () => {
    try {
      if (id) {
        await leaveRequestService.update(id, leaveRequest);
      } else {
        await leaveRequestService.create(leaveRequest);
      }
      navigate('/hrm/leave-requests');
    } catch (error) {
      console.error('Failed to save leave request:', error);
    }
  };
  
  const handleSubmit = async () => {
    try {
      await leaveRequestService.submit(id);
      setIsSubmitDialogOpen(false);
      loadLeaveRequest();
    } catch (error) {
      console.error('Failed to submit leave request:', error);
    }
  };
  
  const handleAuthorize = async () => {
    try {
      await leaveRequestService.authorize(id);
      setIsAuthorizeDialogOpen(false);
      loadLeaveRequest();
    } catch (error) {
      console.error('Failed to authorize leave request:', error);
    }
  };
  
  const handleReject = async () => {
    try {
      await leaveRequestService.reject(id);
      setIsRejectDialogOpen(false);
      loadLeaveRequest();
    } catch (error) {
      console.error('Failed to reject leave request:', error);
    }
  };
  
  if (isLoading) {
    return <div>Loading...</div>;
  }
  
  return (
    <>
      {/* Toolbar - API determines buttons based on mode and status */}
      <MasterToolbar
        viewId="LEAVE_REQUEST"  // Must match backend menu_id exactly
        mode={getMode()}
        onAction={handleToolbarAction}
        hasSelection={!!id}
        showLabels={false}
      />
      
      <div className="page-container space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl font-semibold text-[#201f1e]">
              {!id ? 'New Leave Request' : `Leave Request #${id}`}
            </h1>
            <p className="text-sm text-[#605e5c]">
              {!id ? 'Create a new leave request' : 'View or edit leave request'}
            </p>
          </div>
          
          {id && leaveRequest && (
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${
              leaveRequest.status === 'APPROVED' ? 'bg-green-100 text-green-700' :
              leaveRequest.status === 'REJECTED' ? 'bg-red-100 text-red-700' :
              leaveRequest.status === 'SUBMITTED' ? 'bg-yellow-100 text-yellow-700' :
              'bg-gray-100 text-gray-700'
            }`}>
              {leaveRequest.status}
            </span>
          )}
        </div>
        
        {/* Form */}
        <div className="bg-white p-6 shadow-sm border border-gray-200">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Employee */}
            <div>
              <label className="block text-xs font-semibold text-[#605e5c] uppercase mb-2">
                Employee *
              </label>
              <input
                type="text"
                disabled={getMode() === 'VIEW_FORM'}
                className="w-full px-3 py-2 border border-gray-300 rounded-sm text-sm focus:border-[#0078d4] outline-none disabled:bg-gray-50"
              />
            </div>
            
            {/* Leave Type */}
            <div>
              <label className="block text-xs font-semibold text-[#605e5c] uppercase mb-2">
                Leave Type *
              </label>
              <select
                disabled={getMode() === 'VIEW_FORM'}
                className="w-full px-3 py-2 border border-gray-300 rounded-sm text-sm focus:border-[#0078d4] outline-none disabled:bg-gray-50"
              >
                <option>Select leave type...</option>
                <option>Annual Leave</option>
                <option>Sick Leave</option>
                <option>Casual Leave</option>
              </select>
            </div>
            
            {/* From Date */}
            <div>
              <label className="block text-xs font-semibold text-[#605e5c] uppercase mb-2">
                From Date *
              </label>
              <input
                type="date"
                disabled={getMode() === 'VIEW_FORM'}
                className="w-full px-3 py-2 border border-gray-300 rounded-sm text-sm focus:border-[#0078d4] outline-none disabled:bg-gray-50"
              />
            </div>
            
            {/* To Date */}
            <div>
              <label className="block text-xs font-semibold text-[#605e5c] uppercase mb-2">
                To Date *
              </label>
              <input
                type="date"
                disabled={getMode() === 'VIEW_FORM'}
                className="w-full px-3 py-2 border border-gray-300 rounded-sm text-sm focus:border-[#0078d4] outline-none disabled:bg-gray-50"
              />
            </div>
            
            {/* Reason */}
            <div className="md:col-span-2">
              <label className="block text-xs font-semibold text-[#605e5c] uppercase mb-2">
                Reason *
              </label>
              <textarea
                rows={3}
                disabled={getMode() === 'VIEW_FORM'}
                className="w-full px-3 py-2 border border-gray-300 rounded-sm text-sm focus:border-[#0078d4] outline-none disabled:bg-gray-50"
              />
            </div>
          </div>
        </div>
      </div>
      
      {/* Confirmation Dialogs */}
      <ConfirmationDialog
        isOpen={isCancelDialogOpen}
        onClose={() => setIsCancelDialogOpen(false)}
        onConfirm={() => navigate('/hrm/leave-requests')}
        title="Cancel Leave Request"
        message="Are you sure you want to cancel? All unsaved changes will be lost."
        confirmText="Yes, Cancel"
        cancelText="No, Keep Editing"
        variant="warning"
      />
      
      <ConfirmationDialog
        isOpen={isSubmitDialogOpen}
        onClose={() => setIsSubmitDialogOpen(false)}
        onConfirm={handleSubmit}
        title="Submit Leave Request"
        message="Are you sure you want to submit this leave request for approval?"
        confirmText="Submit"
        cancelText="Cancel"
        variant="primary"
      />
      
      <ConfirmationDialog
        isOpen={isAuthorizeDialogOpen}
        onClose={() => setIsAuthorizeDialogOpen(false)}
        onConfirm={handleAuthorize}
        title="Authorize Leave Request"
        message="Are you sure you want to approve this leave request?"
        confirmText="Approve"
        cancelText="Cancel"
        variant="success"
      />
      
      <ConfirmationDialog
        isOpen={isRejectDialogOpen}
        onClose={() => setIsRejectDialogOpen(false)}
        onConfirm={handleReject}
        title="Reject Leave Request"
        message="Are you sure you want to reject this leave request?"
        confirmText="Reject"
        cancelText="Cancel"
        variant="danger"
      />
    </>
  );
};
```

---

## 📋 PART 3: API BEHAVIOR BY MODE

### **How Backend API Filters Actions**

The backend API automatically filters actions based on mode. Frontend receives only allowed actions.

#### **VIEW Mode** (List or viewing records)

**API Request**:
```http
GET /api/toolbar-permissions/?view_id=EMPLOYEE_MASTER&mode=VIEW
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
    "import",
    "export",
    "exit"
  ]
}
```

**Logic**: User is viewing, so show navigation and actions, hide form controls

---

#### **VIEW_FORM Mode** (Read-only form view)

**API Request**:
```http
GET /api/toolbar-permissions/?view_id=LEAVE_REQUEST&mode=VIEW_FORM
```

**API Response** (for approver):
```json
{
  "allowed_actions": [
    "authorize",
    "reject",
    "print",
    "email",
    "first",
    "previous",
    "next",
    "last",
    "exit"
  ]
}
```

**Logic**: User is viewing approved/submitted record, show workflow and navigation actions

---

#### **CREATE Mode** (Creating new record)

**API Request**:
```http
GET /api/toolbar-permissions/?view_id=EMPLOYEE_MASTER&mode=CREATE
```

**API Response**:
```json
{
  "allowed_actions": [
    "save",
    "cancel",
    "clear",
    "exit"
  ]
}
```

**Logic**: User is creating, show only form controls

---

#### **EDIT Mode** (Editing existing record)

**API Request**:
```http
GET /api/toolbar-permissions/?view_id=LEAVE_REQUEST&mode=EDIT
```

**API Response**:
```json
{
  "allowed_actions": [
    "save",
    "cancel",
    "clear",
    "submit",
    "exit"
  ]
}
```

**Logic**: User is editing draft, show form controls and submit option

---

## 📋 PART 4: COMPLETE ACTION REFERENCE

**Note**: These are action IDs that backend may return. Frontend receives them directly from API.

```
new       - New (F2)          - Create new record
edit      - Edit (F3)         - Edit selected record
view      - View (F7)         - View selected record (read-only)
save      - Save (F8)         - Save changes
cancel    - Cancel (Esc)      - Cancel operation
clear     - Clear (F5)        - Clear/Reset form
delete    - Delete (F4)       - Delete record
exit      - Exit (Esc)        - Navigate away
refresh   - Refresh (F9)      - Reload list
search    - Search (Ctrl+F)   - Focus search box
filter    - Filter (Alt+F)    - Toggle filter panel
authorize - Authorize (F10)   - Approve transaction
submit    - Submit (Alt+S)    - Submit for approval
reject    - Reject (Alt+R)    - Reject transaction
amend     - Amend (Alt+A)     - Amend approved transaction
print     - Print (Ctrl+P)    - Print document
email     - Email (Ctrl+M)    - Email document
import    - Import (Ctrl+I)   - Import data
export    - Export (Ctrl+E)   - Export data
first     - First (Home)      - Navigate to first record
previous  - Prev (PgUp)       - Navigate to previous record
next      - Next (PgDn)       - Navigate to next record
last      - Last (End)        - Navigate to last record
generate  - Generate (Alt+G)  - Generate report
attach    - Attachments (Alt+U) - Manage attachments
notes     - Notes (Alt+N)     - Add notes
help      - Help (F1)         - Show help
clone     - Clone             - Clone record
```

---

## ✅ CHECKLIST FOR AGENT E

### **For Each Screen**:

#### **Backend**:
- [ ] Create ONE ERPMenuItem entry (not separate list/form entries)
- [ ] Set `menu_id` in UPPERCASE_SNAKE_CASE
- [ ] Set `view_type` (MASTER, TRANSACTION, REPORT, etc.)
- [ ] Set `toolbar_config` based on screen type
- [ ] Set `route_path` to match frontend route

#### **Frontend**:
- [ ] Import `MasterToolbar` from correct path
- [ ] Set `viewId` to match backend `menu_id` EXACTLY
- [ ] Implement `getMode()` function returning VIEW/VIEW_FORM/CREATE/EDIT
- [ ] Implement `handleToolbarAction()` for all actions
- [ ] **DO NOT** add `allowedActions` prop (API controls this)
- [ ] Add state for `showForm`, `editingId`, `viewMode`, `selectedId`
- [ ] Add confirmation dialogs for destructive actions
- [ ] Add filter panel toggle state (if applicable)

#### **Testing**:
- [ ] VIEW mode shows correct buttons (from API)
- [ ] VIEW_FORM mode shows read-only actions
- [ ] CREATE mode shows only save, cancel, clear, exit
- [ ] EDIT mode shows only save, cancel, clear, exit (+ submit for transactions)
- [ ] All keyboard shortcuts work
- [ ] Filter toggle works
- [ ] Exit navigation works (form → list, list → dashboard)
- [ ] Confirmation dialogs appear for destructive actions

---

## 🚨 COMMON MISTAKES TO AVOID

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

### **❌ MISTAKE 4: Only 3 Modes**

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

## 📞 NEED HELP?

**Questions**:
1. **"Which config string should I use?"** → Check Part 1, Step 2 above
2. **"How do I handle workflow actions?"** → See Leave Request example
3. **"What if buttons don't show?"** → Check viewId matches menu_id exactly
4. **"Can I add custom buttons?"** → No, use standard actions only
5. **"How do I test the API?"** → Use browser DevTools Network tab

**Debugging**:
- Check browser console for API errors
- Verify `/api/toolbar-permissions/` endpoint exists
- Confirm `viewId` matches `menu_id` exactly (case-sensitive)
- Ensure mode is one of: VIEW, VIEW_FORM, CREATE, EDIT
- Check Network tab to see actual API response

---

## 🔗 RELATED DOCUMENTATION

- **Retail Reference**: `.steering/20TOOLBAR_ROLLOUT/02_REFERENCE/MODE_BASED_FILTERING_TECHNICAL_REFERENCE.md`
- **Component Source**: `frontend/core/ui-canon/frontend/ui/components/MasterToolbarConfigDriven.tsx`
- **Hook Source**: `frontend/src/hooks/useToolbarPermissions.ts`
- **Universal Checklist**: `.steering/20TOOLBAR_ROLLOUT/01_ESSENTIAL/UNIVERSAL_TOOLBAR_IMPLEMENTATION_CHECKLIST.md`

---

**Status**: ✅ READY FOR USE  
**Version**: 2.0 (API-Driven Permission System)  
**Last Updated**: 2026-01-11 20:17 IST  
**For**: Agent E (HRM/CRM Development)
