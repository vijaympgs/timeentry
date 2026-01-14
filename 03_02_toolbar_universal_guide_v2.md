# 🎨 UNIVERSAL TOOLBAR IMPLEMENTATION GUIDE (v2.0 - API-Driven)

**Purpose**: Comprehensive guide for implementing API-driven toolbar permissions across HRM/CRM modules  
**Status**: ✅ PRODUCTION READY  
**Version**: 2.0 (API-Driven Permission System)  
**Scope**: HRM, CRM  
**Last Updated**: 2026-01-11 20:17 IST  

---

## 📜 VERSION HISTORY

| Version | Date | System | Description |
|---------|------|--------|-------------|
| **1.0** | 2026-01-11 10:57 IST | Character-Based | Frontend filtered character strings from backend |
| **2.0** | 2026-01-11 20:17 IST | API-Driven | Backend API returns filtered action IDs based on mode |

**Current System**: ✅ **API-Driven Permission System** (v2.0)

---

## 📋 EXECUTIVE SUMMARY

This document describes the **current production implementation** of mode-based toolbar filtering using the **API-driven permission system**. 

**Key Change from v1.0**: Backend API now returns filtered action IDs directly. Frontend no longer performs character-based filtering.

---

## 🎯 CORE ARCHITECTURE

### **API-Driven, Mode-Aware Toolbar Permissions**

```
Frontend Component → API Request → Backend Logic → Filtered Actions → Rendered Buttons
```

**Key Components:**
- **Backend API**: `/api/toolbar-permissions/` endpoint
- **Frontend Hook**: `useToolbarPermissions` for data fetching
- **Frontend Component**: `MasterToolbarConfigDriven.tsx` with mode prop
- **Feature Flag**: `USE_NEW_PERMISSION_SYSTEM` for graceful degradation

---

## 🔧 MODE-BASED PERMISSION SYSTEM

### **The Four Modes**

| Mode | Description | Use Case |
|------|-------------|----------|
| **VIEW** | Viewing list or browsing records | Master list, Transaction list |
| **VIEW_FORM** | Viewing single record (read-only) | Approved transactions, Read-only master view |
| **CREATE** | Creating new record | New master entry, New transaction |
| **EDIT** | Editing existing record | Modify draft master, Edit draft transaction |

---

### **VIEW Mode** - Browsing Lists or Records

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

---

### **VIEW_FORM Mode** - Read-Only Form View

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

---

### **CREATE Mode** - Creating New Record

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

---

### **EDIT Mode** - Editing Existing Record

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

---

## 🏗️ IMPLEMENTATION PATTERNS

### **Pattern 1: Master Data Setup (Employee, Department, etc.)**

#### **Backend Configuration**
```python
# Django Admin
ERPMenuItem.objects.create(
    menu_id="EMPLOYEE_MASTER",
    menu_name="Employee Master",
    module="HRM",
    submodule="Employee Management",
    menu_type="M",
    toolbar_config="NESCKVDXRQFIO",  # Config string for backend storage
    is_active=True
)
```

**Note**: The `toolbar_config` string is used by backend to determine base permissions. The API endpoint filters this based on mode and user permissions.

---

#### **Frontend Implementation**

```typescript
import React, { useState } from 'react';
import { MasterToolbar, MasterMode } from '@core/ui-canon/frontend/ui/components/MasterToolbarConfigDriven';

export const EmployeeSetup: React.FC = () => {
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState(false); // Read-only view
  const [selectedId, setSelectedId] = useState<string | null>(null);
  
  // Determine toolbar mode
  const getToolbarMode = (): MasterMode => {
    if (!showForm) return 'VIEW';        // Viewing list
    if (viewMode) return 'VIEW_FORM';    // Viewing record (read-only)
    return editingId ? 'EDIT' : 'CREATE'; // Editing or creating
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
          // Call your save logic here
          console.log('Saving employee...');
          setShowForm(false);
          setEditingId(null);
          setViewMode(false);
        }
        break;
      
      case 'cancel':
        setShowForm(false);
        setEditingId(null);
        setViewMode(false);
        break;
      
      case 'clear':
        if (showForm) {
          // Clear form fields
          console.log('Clearing form...');
        }
        break;
      
      case 'delete':
        if (selectedId && !showForm) {
          // Call delete logic
          console.log('Deleting employee:', selectedId);
        }
        break;
      
      case 'refresh':
        // Reload data
        console.log('Refreshing data...');
        break;
      
      case 'search':
        // Focus search input
        document.querySelector<HTMLInputElement>('input[type="text"]')?.focus();
        break;
      
      case 'filter':
        // Toggle filter panel
        setShowFilterPanel(!showFilterPanel);
        break;
      
      case 'exit':
        if (showForm) {
          // From form, return to list
          setShowForm(false);
          setEditingId(null);
          setViewMode(false);
        } else {
          // From list, navigate to dashboard
          navigate('/dashboard');
        }
        break;
    }
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
      
      {/* Page content with list/form switching logic */}
      {showForm ? (
        <EmployeeForm 
          id={editingId}
          readOnly={viewMode}
          onSave={handleSave}
          onCancel={() => setShowForm(false)}
        />
      ) : (
        <EmployeeList 
          onSelect={setSelectedId}
          selectedId={selectedId}
        />
      )}
    </>
  );
};
```

---

### **Pattern 2: Transaction Setup (Leave Request, Lead, etc.)**

#### **Backend Configuration**
```python
# Django Admin
ERPMenuItem.objects.create(
    menu_id="LEAVE_REQUEST",
    menu_name="Leave Request",
    module="HRM",
    submodule="Time & Attendance",
    menu_type="T",
    toolbar_config="NESCKZTJAVPMRDX1234QF",  // Full workflow
    is_active=True
)
```

---

#### **Frontend Implementation**

```typescript
import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { MasterToolbar, MasterMode } from '@core/ui-canon/frontend/ui/components/MasterToolbarConfigDriven';

export const LeaveRequestFormPage: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [leaveRequest, setLeaveRequest] = useState<any>(null);
  const [isEditing, setIsEditing] = useState(false);
  
  // Mode determination for transactions
  const getMode = (): MasterMode => {
    if (!id) return 'CREATE';                          // New transaction
    if (leaveRequest?.status === 'DRAFT') return 'EDIT'; // Draft - can edit
    return 'VIEW_FORM';                                 // Submitted/Approved - read-only
  };
  
  const handleToolbarAction = (action: string) => {
    switch (action) {
      case 'save':
        // Save logic
        console.log('Saving leave request...');
        break;
      
      case 'cancel':
        if (!id) {
          // Navigate back to list
          navigate('/hrm/leave-requests');
        } else {
          setIsEditing(false);
        }
        break;
      
      case 'submit':
        // Submit for approval
        console.log('Submitting for approval...');
        break;
      
      case 'authorize':
        // Approve request
        console.log('Approving leave request...');
        break;
      
      case 'reject':
        // Reject request
        console.log('Rejecting leave request...');
        break;
      
      case 'print':
        window.print();
        break;
      
      case 'exit':
        navigate('/hrm/leave-requests');
        break;
    }
  };
  
  return (
    <>
      <MasterToolbar
        viewId="LEAVE_REQUEST"  // Must match backend menu_id exactly
        mode={getMode()}
        onAction={handleToolbarAction}
        hasSelection={!!id}
        showLabels={false}
      />
      
      {/* Transaction form content */}
      <LeaveRequestForm 
        id={id}
        readOnly={getMode() === 'VIEW_FORM'}
        onSave={handleSave}
      />
    </>
  );
};
```

---

## 🔍 HOW THE API WORKS

### **Step 1: Frontend Calls Hook**

```typescript
// Inside MasterToolbar component
const { allowedActions, loading, error } = useToolbarPermissions(
  viewId,    // e.g., "EMPLOYEE_MASTER"
  mode,      // e.g., "VIEW"
  skip       // false to enable API call
);
```

---

### **Step 2: Hook Makes API Request**

```http
GET /api/toolbar-permissions/?view_id=EMPLOYEE_MASTER&mode=VIEW
Authorization: Bearer <token>
```

---

### **Step 3: Backend Returns Filtered Actions**

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

---

### **Step 4: Component Renders Only Allowed Buttons**

```typescript
const isActionVisible = (action: ActionButton): boolean => {
  return allowedActions.includes(action.id);
};

// Render only visible buttons
{ACTIONS
  .filter(a => isActionVisible(a))
  .map(action => <Button ... />)
}
```

---

## 📊 ACTION VISIBILITY MATRIX

**Note**: This shows typical backend behavior. Actual actions vary based on user permissions and screen configuration.

| Action ID | Description | VIEW | VIEW_FORM | CREATE | EDIT |
|-----------|-------------|------|-----------|--------|------|
| **new** | Create new record | ✅ | ❌ | ❌ | ❌ |
| **edit** | Edit selected record | ✅ | ✅ | ❌ | ❌ |
| **view** | View selected record | ✅ | ❌ | ❌ | ❌ |
| **save** | Save changes | ❌ | ❌ | ✅ | ✅ |
| **cancel** | Cancel operation | ❌ | ❌ | ✅ | ✅ |
| **clear** | Clear/Reset form | ❌ | ❌ | ✅ | ✅ |
| **delete** | Delete record | ✅ | ✅ | ❌ | ❌ |
| **refresh** | Reload list | ✅ | ❌ | ❌ | ❌ |
| **search** | Focus search box | ✅ | ❌ | ❌ | ❌ |
| **filter** | Toggle filters | ✅ | ❌ | ❌ | ❌ |
| **exit** | Navigate away | ✅ | ✅ | ✅ | ✅ |

### **Transaction-Specific Actions**

| Action ID | Description | VIEW | VIEW_FORM | CREATE | EDIT |
|-----------|-------------|------|-----------|--------|------|
| **submit** | Submit for approval | ❌ | ❌ | ❌ | ✅* |
| **authorize** | Approve transaction | ✅* | ✅* | ❌ | ❌ |
| **reject** | Reject transaction | ✅* | ✅* | ❌ | ❌ |
| **amend** | Amend approved | ✅* | ✅* | ❌ | ❌ |
| **print** | Print document | ✅* | ✅ | ❌ | ❌ |
| **email** | Email document | ✅* | ✅ | ❌ | ❌ |

**\* Conditional**: Shown based on transaction status and user role

---

## 📋 VALIDATION CHECKLIST

### **Backend Validation**
- [ ] One ERPMenuItem entry per screen (no separate list/form entries)
- [ ] menu_id in UPPERCASE_SNAKE_CASE
- [ ] toolbar_config string uses standard characters
- [ ] API endpoint `/api/toolbar-permissions/` exists and works

### **Frontend Validation**
- [ ] MasterToolbar imported from correct path
- [ ] viewId matches backend menu_id EXACTLY
- [ ] getMode() function returns VIEW, VIEW_FORM, CREATE, or EDIT
- [ ] handleToolbarAction handles all possible actions
- [ ] **DO NOT** use allowedActions prop (backend API controls this)
- [ ] State management for showForm, editingId, viewMode, selectedId

### **Mode Testing**
- [ ] VIEW mode shows: new, edit, view, delete, refresh, search, filter, exit
- [ ] VIEW_FORM mode shows: edit, delete, exit (and print/email for transactions)
- [ ] CREATE mode shows: save, cancel, clear, exit
- [ ] EDIT mode shows: save, cancel, clear, exit
- [ ] Mode switching works correctly on state changes

### **Integration Testing**
- [ ] Keyboard shortcuts work (F2, F3, F8, etc.)
- [ ] Exit navigation returns to correct mode
- [ ] Cancel behavior preserves data integrity
- [ ] Filter toggle works in VIEW mode
- [ ] Import/Export buttons appear where configured

---

## 🚨 COMMON IMPLEMENTATION MISTAKES TO AVOID

### **❌ CRITICAL MISTAKE #1: Multiple Database Entries**

```python
❌ WRONG:
ERPMenuItem(menu_id="employee-list", view_type="LIST_VIEW")
ERPMenuItem(menu_id="EMPLOYEE_MASTER", view_type="MASTER")

✅ CORRECT:
ERPMenuItem(menu_id="EMPLOYEE_MASTER", view_type="MASTER")
# Frontend handles both list and form with mode switching
```

---

### **❌ CRITICAL MISTAKE #2: Hardcoded Actions**

```typescript
❌ WRONG:
<MasterToolbar 
  viewId="EMPLOYEE_MASTER" 
  allowedActions={['new', 'edit', 'save']}  // ❌ Backend API controls this!
/>

✅ CORRECT:
<MasterToolbar 
  viewId="EMPLOYEE_MASTER" 
  mode={getMode()}  // Backend API + mode filtering
  onAction={handleToolbarAction}
/>
```

---

### **❌ CRITICAL MISTAKE #3: Wrong Hook Name**

```typescript
❌ WRONG:
import { useToolbarConfig } from '...';  // ❌ Old hook!
const { config } = useToolbarConfig(viewId);

✅ CORRECT:
// Hook is used internally by MasterToolbar component
// You don't need to call it directly
```

---

### **❌ CRITICAL MISTAKE #4: Case Mismatch**

```python
❌ WRONG:
Backend: menu_id="EMPLOYEE_MASTER"
Frontend: viewId="employee_master"  // ❌ Case mismatch!

✅ CORRECT:
Backend: menu_id="EMPLOYEE_MASTER"
Frontend: viewId="EMPLOYEE_MASTER"  // ✅ Exact match required
```

---

### **❌ CRITICAL MISTAKE #5: Missing VIEW_FORM Mode**

```typescript
❌ WRONG:
// Only 3 modes
const getMode = (): MasterMode => {
  if (!showForm) return 'VIEW';
  return editingId ? 'EDIT' : 'CREATE';
};

✅ CORRECT:
// All 4 modes
const getMode = (): MasterMode => {
  if (!showForm) return 'VIEW';
  if (viewMode) return 'VIEW_FORM';  // ← Read-only form view
  return editingId ? 'EDIT' : 'CREATE';
};
```

---

## 📊 PERFORMANCE CONSIDERATIONS

### **Efficient API Calls**
- Single API call per mode change
- Toolbar permissions cached appropriately
- Loading states handled gracefully

### **Memory Management**
- Single config string per screen in backend
- No duplicate action definitions
- Minimal re-renders on mode changes

### **Network Optimization**
- Permission filtering handled server-side
- Frontend only receives what it needs
- Graceful degradation if API fails

---

## 🎯 SUCCESS METRICS

### **Implementation Completeness**
- [ ] All screens follow API-driven pattern
- [ ] Zero hardcoded toolbar actions
- [ ] Consistent behavior across modules
- [ ] Permission enforcement working

### **User Experience**
- [ ] Context-aware button visibility
- [ ] Intuitive mode transitions
- [ ] Smart Exit (form → list, not form → dashboard)
- [ ] Keyboard shortcuts working consistently

### **Maintainability**
- [ ] Single source of truth (backend API)
- [ ] Zero frontend maintenance for button changes
- [ ] Centralized permission logic
- [ ] Consistent shortcuts across all screens

---

## 🚀 NEXT STEPS

1. **Verify Backend API** exists at `/api/toolbar-permissions/`
2. **Test with real data** to ensure API returns correct actions
3. **Implement VIEW_FORM mode** for approved transactions
4. **Add permission integration** for role-based filtering
5. **Test mode switching** across all implemented screens

---

## 🔗 RELATED DOCUMENTATION

- **Component Source**: `frontend/core/ui-canon/frontend/ui/components/MasterToolbarConfigDriven.tsx`
- **Hook Source**: `frontend/src/hooks/useToolbarPermissions.ts`
- **Backend API**: `/api/toolbar-permissions/` (Django REST Framework endpoint)
- **Retail Reference**: `.steering/20TOOLBAR_ROLLOUT/02_REFERENCE/MODE_BASED_FILTERING_TECHNICAL_REFERENCE.md`

---

**Status**: ✅ **PRODUCTION READY**  
**Version**: 2.0 (API-Driven Permission System)  
**Authority**: Platform Governance Canon  
**Last Updated**: 2026-01-11 20:17 IST  
**For**: Agent E (HRM/CRM Development)
