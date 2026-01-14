# Transaction Form Page - Wiring Checklist (HRM Focus)

**For**: Leave Request, Attendance Adjustment, Expense Claim, Performance Review (HRM Transaction Forms)  
**Pattern**: Transaction form with toolbar, header, line items, lookups, workflow actions

---

## 📋 COMPLETE WIRING CHECKLIST

### **PHASE 1: Backend Setup**

#### 1.1 Header Model Verification
- [ ] Header model exists (e.g., `LeaveRequest`, `ExpenseClaim`)
- [ ] Has `company` foreign key
- [ ] Has `status` field with choices (DRAFT, SUBMITTED, APPROVED, REJECTED, CANCELLED)
- [ ] Has transaction number field (auto-generated)
- [ ] Has date field(s) (start_date, end_date, request_date)
- [ ] Has reference fields (employee, department, position, etc.)
- [ ] Has total fields (amount, approved_amount, etc.)
- [ ] Has audit fields (created_by, created_at, updated_at)

#### 1.2 Line Model Verification (if applicable)
- [ ] Line model exists (e.g., `ExpenseClaimLine`)
- [ ] Has foreign key to header model
- [ ] Has `line_number` field
- [ ] Has `expense_type` or `item` foreign key
- [ ] Has `amount` field(s)
- [ ] Has `line_total` field
- [ ] Has optional fields (description, receipt_date, etc.)

#### 1.3 Serializer Setup
- [ ] Header serializer created with nested line serializer (if applicable)
- [ ] Line serializer includes read-only fields (employee_name, department_name, etc.)
- [ ] Header serializer has custom `create()` method
- [ ] Header serializer has custom `update()` method
- [ ] Auto-generates transaction number in `create()`
- [ ] Calculates totals in `create()/update()`
- [ ] Read-only fields properly defined

**Example**:
```python
class ExpenseClaimLineSerializer(serializers.ModelSerializer):
    expense_type_name = serializers.CharField(source='expense_type.name', read_only=True)
    employee_name = serializers.CharField(source='employee.employee_name', read_only=True)
    
    class Meta:
        model = ExpenseClaimLine
        fields = '__all__'
        read_only_fields = ['line_id', 'expense_claim']

class LeaveRequestSerializer(serializers.ModelSerializer):
    lines = ExpenseClaimLineSerializer(many=True, read_only=True)
    employee_name = serializers.CharField(source='employee.employee_name', read_only=True)
    
    class Meta:
        model = LeaveRequest
        fields = '__all__'
        read_only_fields = ['request_id', 'request_number', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Auto-generate request number
        validated_data['request_number'] = f"LR-{timezone.now().strftime('%Y%m%d%H%M%S')}"
        return super().create(validated_data)
```

#### 1.4 ViewSet with Workflow Actions
- [ ] ViewSet created with `ModelViewSet`
- [ ] Has `get_queryset()` with company scoping
- [ ] Has `@action` methods for workflow (submit, approve, reject, cancel, etc.)
- [ ] Workflow actions validate status transitions
- [ ] Workflow actions update status
- [ ] Workflow actions log audit trail

**Example**:
```python
class LeaveRequestViewSet(viewsets.ModelViewSet):
    serializer_class = LeaveRequestSerializer
    
    def get_queryset(self):
        return LeaveRequest.objects.filter(company=self.request.user.company)
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        leave_request = self.get_object()
        if leave_request.status != 'DRAFT':
            return Response({'error': 'Only DRAFT leave requests can be submitted'}, status=400)
        
        leave_request.status = 'SUBMITTED'
        leave_request.submitted_at = timezone.now()
        leave_request.save()
        
        return Response(self.get_serializer(leave_request).data)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        leave_request = self.get_object()
        if leave_request.status != 'SUBMITTED':
            return Response({'error': 'Only SUBMITTED leave requests can be approved'}, status=400)
        
        leave_request.status = 'APPROVED'
        leave_request.approved_by = request.user
        leave_request.approved_at = timezone.now()
        leave_request.save()
        
        return Response(self.get_serializer(leave_request).data)
```

#### 1.5 URL Registration
- [ ] ViewSet registered in router
- [ ] Endpoint follows pattern: `/api/hrm/{resource}/`

---

### **PHASE 2: Frontend Service Layer**

#### 2.1 TypeScript Types
- [ ] Header interface defined
- [ ] Line interface defined (if applicable)
- [ ] Status type defined (union of status strings)
- [ ] All fields properly typed

**Example**:
```typescript
export type LeaveRequestStatus = 'DRAFT' | 'SUBMITTED' | 'APPROVED' | 'REJECTED' | 'CANCELLED';

export interface ExpenseClaimLine {
    id?: string;
    line_number: number;
    expense_type_id?: string;
    expense_type_name?: string;
    description?: string;
    amount: number;
    receipt_date?: string;
    line_total: number;
}

export interface LeaveRequest {
    id?: string;
    request_number: string;
    company: string;
    employee: string;
    employee_name?: string;
    leave_type: string;
    leave_type_name?: string;
    start_date: string;
    end_date: string;
    reason: string;
    status: LeaveRequestStatus;
    total_days?: number;
    approved_days?: number;
    created_at?: string;
    updated_at?: string;
}
```

#### 2.2 Service Methods
- [ ] CRUD methods (get, create, update, delete)
- [ ] Workflow action methods (submit, approve, reject, cancel, etc.)
- [ ] All methods use `apiClient`

**Example**:
```typescript
export const hrmService = {
    // CRUD
    getLeaveRequests: async (filters?: any) => {
        const response = await apiClient.get('/hrm/leave-requests/', { params: filters });
        return response.data;
    },
    
    getLeaveRequest: async (id: string) => {
        const response = await apiClient.get(`/hrm/leave-requests/${id}/`);
        return response.data;
    },
    
    createLeaveRequest: async (data: Partial<LeaveRequest>) => {
        const response = await apiClient.post('/hrm/leave-requests/', data);
        return response.data;
    },
    
    updateLeaveRequest: async (id: string, data: Partial<LeaveRequest>) => {
        const response = await apiClient.put(`/hrm/leave-requests/${id}/`, data);
        return response.data;
    },
    
    // Workflow actions
    submitLeaveRequest: async (id: string) => {
        const response = await apiClient.post(`/hrm/leave-requests/${id}/submit/`);
        return response.data;
    },
    
    approveLeaveRequest: async (id: string) => {
        const response = await apiClient.post(`/hrm/leave-requests/${id}/approve/`);
        return response.data;
    },
    
    rejectLeaveRequest: async (id: string, reason?: string) => {
        const response = await apiClient.post(`/hrm/leave-requests/${id}/reject/`, { reason });
        return response.data;
    },
};
```

---

### **PHASE 3: Component Setup**

#### 3.1 Component Structure
- [ ] Component created in `frontend/apps/hrm/{module}/pages/`
- [ ] Uses TypeScript with proper typing
- [ ] Imports all necessary dependencies

**Required Imports**:
```typescript
import React, { useState, useEffect, useCallback } from "react";
import { Save, Printer, Mail, MoreHorizontal, Plus, Trash2, Calendar, ChevronLeft } from "lucide-react";
import { useNavigate, useParams } from "react-router-dom";
import { TransactionToolbar, TransactionStatus } from "@ui/components/TransactionToolbar";
import { EmployeeLookupModal, EmployeeLookupResult } from "@ui/components/EmployeeLookupModal";
import { useAuth } from "@auth/useAuth";
import hrmService from "../hrm.service";
import type { LeaveRequest, LeaveRequestLine, LeaveRequestStatus } from "../hrm.types";
```

#### 3.2 State Management
- [ ] `header` state (transaction metadata)
- [ ] `lines` state (array of line items, if applicable)
- [ ] `loading` state
- [ ] `saving` state
- [ ] `error` state
- [ ] Modal states (employee, department, position, etc.)
- [ ] `activeLineIndex` state (for F12 lookup, if applicable)

**Example**:
```typescript
const [header, setHeader] = useState({
    request_number: '',
    company: user?.currentCompanyId || '',
    employee: '',
    employee_name: '',
    leave_type: '',
    leave_type_name: '',
    start_date: new Date().toISOString().split('T')[0],
    end_date: '',
    reason: '',
    status: 'DRAFT' as LeaveRequestStatus
});

const [loading, setLoading] = useState(false);
const [saving, setSaving] = useState(false);
const [error, setError] = useState<string | null>(null);
const [isEmployeeModalOpen, setIsEmployeeModalOpen] = useState(false);
```

#### 3.3 URL Parameters
- [ ] Extract `id` from URL params
- [ ] Determine if new or edit mode

**Example**:
```typescript
const { id } = useParams();
const isNew = !id || id === "new";
```

---

### **PHASE 4: Data Loading**

#### 4.1 Load Existing Data (Edit Mode)
- [ ] `useEffect` hook for loading data
- [ ] Only runs if not new
- [ ] Fetches transaction by ID
- [ ] Maps backend data to UI state
- [ ] Handles errors

**Example**:
```typescript
useEffect(() => {
    if (!isNew && id) {
        setLoading(true);
        hrmService.getLeaveRequest(id)
            .then(leaveRequest => {
                setHeader({
                    request_number: leaveRequest.request_number,
                    company: leaveRequest.company,
                    employee: leaveRequest.employee,
                    employee_name: leaveRequest.employee_name || '',
                    leave_type: leaveRequest.leave_type,
                    leave_type_name: leaveRequest.leave_type_name || '',
                    start_date: leaveRequest.start_date,
                    end_date: leaveRequest.end_date || '',
                    reason: leaveRequest.reason || '',
                    status: leaveRequest.status
                });
            })
            .catch(err => {
                setError(err.message || 'Failed to load leave request');
            })
            .finally(() => setLoading(false));
    }
}, [id, isNew]);
```

---

### **PHASE 5: TransactionToolbar Integration**

#### 5.1 Toolbar Component
- [ ] Import `TransactionToolbar` component
- [ ] Pass `status` prop (uppercase)
- [ ] Implement `onAction` handler
- [ ] Define `disabledActions` based on status

**Example**:
```typescript
<TransactionToolbar 
    status={header.status.toUpperCase() as TransactionStatus} 
    onAction={handleToolbarAction} 
    disabledActions={getDisabledActions(header.status)} 
/>
```

#### 5.2 Toolbar Action Handler
- [ ] Switch statement for all actions
- [ ] Maps actions to handler functions
- [ ] Handles save, submit, approve, cancel, etc.
- [ ] Handles lookup actions

**Example**:
```typescript
const handleToolbarAction = (action: string) => {
    switch (action) {
        case 'new':
            navigate('/hrm/leave-requests/new');
            break;
        case 'save':
            handleSave();
            break;
        case 'clear':
            if (confirm('Clear all changes?')) {
                window.location.reload();
            }
            break;
        case 'cancel':
            navigate('/hrm/leave-requests');
            break;
        case 'submit':
            handleSubmit();
            break;
        case 'lookup_employee':
            setIsEmployeeModalOpen(true);
            break;
        default:
            console.log("Action:", action);
    }
};
```

#### 5.3 Disabled Actions Logic
- [ ] Function returns array of disabled actions
- [ ] Based on current status
- [ ] Disables all actions while saving

**Example**:
```typescript
const getDisabledActions = (status: LeaveRequestStatus): string[] => {
    if (saving) return ['save', 'submit', 'clear', 'new', 'print', 'email'];
    
    switch (status) {
        case 'DRAFT':
            return ['approve', 'reject'];
        case 'APPROVED':
        case 'REJECTED':
        case 'CANCELLED':
            return ['new', 'save', 'clear', 'cancel', 'submit', 'approve', 'reject'];
        default:
            return [];
    }
};
```

---

### **PHASE 6: Header Section**

#### 6.1 Header Layout
- [ ] White background with border
- [ ] Transaction number display (read-only)
- [ ] Status badge (color-coded)
- [ ] Total display (prominent, if applicable)
- [ ] Back button with ChevronLeft icon
- [ ] Form fields in grid layout (4 columns)

#### 6.2 Form Fields Grid
- [ ] 4-column grid layout
- [ ] Lookup fields with buttons
- [ ] Date fields with Calendar icon
- [ ] Text fields with appropriate icons
- [ ] Bottom border on inputs
- [ ] Hover effects

---

### **PHASE 7: Line Items Grid** (if applicable)

#### 7.1 Line Items Table
- [ ] Editable table with borders
- [ ] Column headers (Description, Amount, Date, Actions)
- [ ] Add line button
- [ ] Remove line button (Trash2 icon)
- [ ] F12 for lookup (if applicable)
- [ ] Enter key navigation

#### 7.2 Line Management Functions
- [ ] `addLine()` - Adds new empty line
- [ ] `updateLine()` - Updates line field
- [ ] `removeLine()` - Removes line and renumbers
- [ ] `calculateLineTotal()` - Recalculates on amount change

#### 7.3 Keyboard Navigation
- [ ] F12 opens lookup (if applicable)
- [ ] Enter on amount field adds new line (if last line)
- [ ] Tab navigation works

---

### **PHASE 8: Calculations**

#### 8.1 Total Calculation
- [ ] Uses `useMemo` for performance
- [ ] Sums all line totals (if applicable)
- [ ] Includes tax/discount if applicable

**Example**:
```typescript
const totalDays = useMemo(() => {
    if (header.start_date && header.end_date) {
        const start = new Date(header.start_date);
        const end = new Date(header.end_date);
        const diffTime = end.getTime() - start.getTime();
        return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    }
    return 0;
}, [header.start_date, header.end_date]);
```

---

### **PHASE 9: Save & Workflow Actions**

#### 9.1 Validation Function
- [ ] Validates required fields
- [ ] Validates line items (if applicable)
- [ ] Returns error message or null

**Example**:
```typescript
const validateForm = (): string | null => {
    if (!header.employee) return "Employee is required";
    if (!header.leave_type) return "Leave type is required";
    if (!header.start_date) return "Start date is required";
    if (!header.end_date) return "End date is required";
    if (new Date(header.start_date) >= new Date(header.end_date)) {
        return "End date must be after start date";
    }
    if (!header.reason) return "Reason is required";
    return null;
};
```

#### 9.2 Save Handler
- [ ] Validates form
- [ ] Maps UI data to API format
- [ ] Calls create or update service method
- [ ] Navigates on success (if new)
- [ ] Refreshes data (if edit)
- [ ] Handles errors

#### 9.3 Workflow Action Handlers
- [ ] `handleSubmit()` - Submits for approval
- [ ] `handleApprove()` - Approves transaction
- [ ] `handleReject()` - Rejects transaction with reason
- [ ] `handleCancel()` - Cancels transaction
- [ ] Each validates status before calling API
- [ ] Each updates local status on success

**Example**:
```typescript
const handleSubmit = async () => {
    if (isNew) {
        setError('Please save the leave request before submitting');
        return;
    }
    
    setSaving(true);
    setError(null);
    
    try {
        const submitted = await hrmService.submitLeaveRequest(id!);
        setHeader(prev => ({ ...prev, status: submitted.status as LeaveRequestStatus }));
    } catch (err: any) {
        setError(err.response?.data?.error || err.message || 'Failed to submit');
    } finally {
        setSaving(false);
    }
};
```

---

### **PHASE 10: Lookup Modals**

#### 10.1 Employee Lookup Integration
- [ ] Import EmployeeLookupModal
- [ ] State for modal open/close
- [ ] Handler for employee selection
- [ ] Updates header on selection
- [ ] Auto-populates employee fields

**Example**:
```typescript
const handleEmployeeSelect = (employee: EmployeeLookupResult) => {
    setHeader({
        ...header,
        employee: employee.id,
        employee_name: employee.employee_name,
        department: employee.department,
        position: employee.position
    });
};
```

#### 10.2 Department/Position Lookup Integration
- [ ] Import DepartmentLookupModal or PositionLookupModal
- [ ] State for modal open/close
- [ ] Handler for selection
- [ ] Updates header on selection

#### 10.3 Modal Rendering
- [ ] Conditional rendering based on state
- [ ] Pass companyId from user context
- [ ] Pass onClose and onSelect handlers

---

### **PHASE 11: Error Handling**

#### 11.1 Error Banner
- [ ] Conditional rendering based on error state
- [ ] Red background with border
- [ ] Dismissible
- [ ] Positioned below toolbar

---

### **PHASE 12: Loading States**

#### 12.1 Initial Loading
- [ ] Shows spinner while loading
- [ ] Centers spinner
- [ ] Uses Loader2 icon with spin animation

---

### **PHASE 13: UI Standards Compliance**

#### 13.1 Layout
- [ ] Uses flex column layout with `h-full`
- [ ] Background color `bg-[#faf9f8]`
- [ ] Toolbar at top (sticky)
- [ ] Scrollable content area

#### 13.2 Colors
- [ ] No hardcoded colors (use CSS variables or Tailwind)
- [ ] Border color `border-[#edebe9]`
- [ ] Text colors from palette (text-[#201f1e], text-[#605e5c])
- [ ] Primary color `text-[#0078d4]`

#### 13.3 Typography
- [ ] Consistent font sizes
- [ ] Proper font weights
- [ ] Uppercase labels for form fields

---

### **PHASE 14: Testing**

#### 14.1 CRUD Operations
- [ ] Create new transaction
- [ ] Edit existing transaction
- [ ] Save works correctly
- [ ] Data persists to database

#### 14.2 Line Items (if applicable)
- [ ] Add line works
- [ ] Edit line works
- [ ] Remove line works
- [ ] Calculations are correct
- [ ] F12 lookup works

#### 14.3 Workflow Actions
- [ ] Submit works (DRAFT → SUBMITTED)
- [ ] Approve works (SUBMITTED → APPROVED)
- [ ] Reject works (with reason)
- [ ] Cancel works
- [ ] Status updates correctly
- [ ] Disabled actions work

#### 14.4 Lookups
- [ ] Employee lookup opens
- [ ] Employee selection populates header
- [ ] Department/Position lookup opens
- [ ] Selection populates header

#### 14.5 Validation
- [ ] Required fields validated
- [ ] Line items validated (if applicable)
- [ ] Error messages display
- [ ] Cannot save invalid data

#### 14.6 Error Handling
- [ ] Network errors display
- [ ] Validation errors display
- [ ] Error banner dismissible

---

## ✅ COMPLETION CHECKLIST

- [ ] All backend items checked
- [ ] All frontend service items checked
- [ ] Component structure complete
- [ ] Data loading implemented
- [ ] TransactionToolbar integrated
- [ ] Header section complete
- [ ] Line items grid complete (if applicable)
- [ ] Calculations working
- [ ] Save & workflow actions implemented
- [ ] Lookup modals integrated
- [ ] Error handling implemented
- [ ] Loading states implemented
- [ ] UI standards compliance verified
- [ ] All tests passed

---

## 📚 Reference Files

**Backend**:
- `backend/apps/hrm/backend/leave/models.py`
- `backend/apps/hrm/backend/leave/serializers.py`
- `backend/apps/hrm/backend/leave/views.py`

**Frontend**:
- `frontend/apps/hrm/leave/pages/LeaveRequestFormPage.tsx`
- `frontend/apps/hrm/leave/hrm.service.ts`
- `frontend/apps/hrm/leave/hrm.types.ts`

**Components**:
- `frontend/src/ui/components/TransactionToolbar.tsx`
- `frontend/src/ui/components/EmployeeLookupModal.tsx`

**Standards**:
- `.steering/14_UI_CANON/04_Frontend_UI_Canon.md`
- `.steering/14_UI_CANON/TXN-M.md`
- `.steering/governance.md`

---

**Last Updated**: 2026-01-11  
**Maintainer**: Astra (ERP Platform Development Owner)
