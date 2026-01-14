# Workflow & Business Rules - Wiring Checklist (HRM Focus)

**For**: Status machines, Workflow actions, Validation rules, Configuration pages (HRM)  
**Pattern**: Workflow state machine with backend actions and frontend integration

---

## 📋 COMPLETE WIRING CHECKLIST

### **PHASE 1: Status State Machine Definition**

#### 1.1 Define Status Choices (Backend)
- [ ] Status field in model with choices
- [ ] All possible statuses defined
- [ ] Default status set to initial state (usually DRAFT)

**Example**:
```python
class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled'),
    ]
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='DRAFT'
    )
```

#### 1.2 Define Status Machine (Frontend)
- [ ] Status type defined (TypeScript union)
- [ ] Status machine object created
- [ ] Each status has: next, label, color, description
- [ ] Transitions clearly defined

**Example**:
```typescript
export type LeaveRequestStatus = 'DRAFT' | 'SUBMITTED' | 'APPROVED' | 'REJECTED' | 'CANCELLED';

const statusMachine = {
    DRAFT: {
        next: 'SUBMITTED',
        label: 'Draft',
        color: 'text-gray-600',
        bgColor: 'bg-gray-100',
        description: 'Initial draft state'
    },
    SUBMITTED: {
        next: 'APPROVED',
        label: 'Submitted',
        color: 'text-yellow-600',
        bgColor: 'bg-yellow-100',
        description: 'Submitted for approval'
    },
    APPROVED: {
        next: null,
        label: 'Approved',
        color: 'text-green-600',
        bgColor: 'bg-green-100',
        description: 'Approved by manager'
    },
    REJECTED: {
        next: null,
        label: 'Rejected',
        color: 'text-red-600',
        bgColor: 'bg-red-100',
        description: 'Rejected by manager'
    },
    CANCELLED: {
        next: null,
        label: 'Cancelled',
        color: 'text-gray-600',
        bgColor: 'bg-gray-100',
        description: 'Request cancelled'
    }
};
```

#### 1.3 Document Workflow Diagram
- [ ] Create visual workflow diagram (optional)
- [ ] Document in BBP or README
- [ ] Show all transitions

**Example**:
```
DRAFT → SUBMITTED → APPROVED
                ↓
             REJECTED
                ↓
             CANCELLED
```

---

### **PHASE 2: Backend Workflow Actions**

#### 2.1 Submit Action
- [ ] `@action` decorator with `detail=True`, methods=['post']
- [ ] Validates current status (must be DRAFT)
- [ ] Updates status to SUBMITTED
- [ ] Logs audit trail
- [ ] Returns updated serializer data

**Example**:
```python
@action(detail=True, methods=['post'])
def submit(self, request, pk=None):
    """Submit leave request for approval"""
    leave_request = self.get_object()
    
    # Validate status
    if leave_request.status != 'DRAFT':
        return Response(
            {'error': 'Only DRAFT leave requests can be submitted'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Update status
    leave_request.status = 'SUBMITTED'
    leave_request.submitted_by = request.user
    leave_request.submitted_at = timezone.now()
    leave_request.save()
    
    # Return updated data
    serializer = self.get_serializer(leave_request)
    return Response(serializer.data)
```

#### 2.2 Approve Action
- [ ] Validates current status (must be SUBMITTED)
- [ ] Updates status to APPROVED
- [ ] Records approver and timestamp
- [ ] Performs any business logic (e.g., update leave balance)
- [ ] Returns updated data

**Example**:
```python
@action(detail=True, methods=['post'])
def approve(self, request, pk=None):
    """Approve leave request"""
    leave_request = self.get_object()
    
    if leave_request.status != 'SUBMITTED':
        return Response(
            {'error': 'Only SUBMITTED leave requests can be approved'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    leave_request.status = 'APPROVED'
    leave_request.approved_by = request.user
    leave_request.approved_at = timezone.now()
    leave_request.save()
    
    # Business logic (e.g., update leave balance)
    update_leave_balance(
        employee=leave_request.employee,
        leave_type=leave_request.leave_type,
        days=leave_request.total_days,
        operation='deduct'
    )
    
    serializer = self.get_serializer(leave_request)
    return Response(serializer.data)
```

#### 2.3 Reject Action
- [ ] Validates current status (must be SUBMITTED)
- [ ] Updates status to REJECTED
- [ ] Records rejection reason
- [ ] Returns updated data

**Example**:
```python
@action(detail=True, methods=['post'])
def reject(self, request, pk=None):
    """Reject leave request"""
    leave_request = self.get_object()
    
    if leave_request.status != 'SUBMITTED':
        return Response(
            {'error': 'Only SUBMITTED leave requests can be rejected'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    leave_request.status = 'REJECTED'
    leave_request.rejected_by = request.user
    leave_request.rejected_at = timezone.now()
    leave_request.rejection_reason = request.data.get('reason', '')
    leave_request.save()
    
    serializer = self.get_serializer(leave_request)
    return Response(serializer.data)
```

#### 2.4 Cancel Action
- [ ] Validates current status (usually DRAFT or SUBMITTED)
- [ ] Updates status to CANCELLED
- [ ] Records cancellation reason (optional)
- [ ] Reverses any side effects (e.g., restore leave balance)
- [ ] Returns updated data

---

### **PHASE 3: Frontend Workflow Methods**

#### 3.1 Service Methods for Workflow Actions
- [ ] Method for each workflow action
- [ ] Uses POST to custom action endpoint
- [ ] Returns updated transaction data

**Example**:
```typescript
export const hrmService = {
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
    
    cancelLeaveRequest: async (id: string, reason?: string) => {
        const response = await apiClient.post(`/hrm/leave-requests/${id}/cancel/`, { reason });
        return response.data;
    },
};
```

#### 3.2 Workflow Action Handlers (Component)
- [ ] Handler for each workflow action
- [ ] Validates prerequisites (e.g., must save first)
- [ ] Shows confirmation dialog (if needed)
- [ ] Calls service method
- [ ] Updates local state on success
- [ ] Handles errors

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

const handleApprove = async () => {
    if (!confirm('Approve this leave request?')) return;
    
    setSaving(true);
    setError(null);
    
    try {
        const approved = await hrmService.approveLeaveRequest(id!);
        setHeader(prev => ({ ...prev, status: approved.status as LeaveRequestStatus }));
    } catch (err: any) {
        setError(err.response?.data?.error || err.message || 'Failed to approve');
    } finally {
        setSaving(false);
    }
};

const handleReject = async () => {
    const reason = prompt('Rejection reason:');
    if (reason === null) return; // User clicked cancel
    
    setSaving(true);
    setError(null);
    
    try {
        const rejected = await hrmService.rejectLeaveRequest(id!, reason);
        setHeader(prev => ({ ...prev, status: rejected.status as LeaveRequestStatus }));
    } catch (err: any) {
        setError(err.response?.data?.error || err.message || 'Failed to reject');
    } finally {
        setSaving(false);
    }
};
```

---

### **PHASE 4: Disabled Actions Logic**

#### 4.1 Define Disabled Actions Function
- [ ] Function returns array of disabled action names
- [ ] Based on current status
- [ ] Disables all actions while saving
- [ ] Follows business rules

**Example**:
```typescript
const getDisabledActions = (status: LeaveRequestStatus): string[] => {
    // Disable all actions while saving
    if (saving) {
        return ['save', 'submit', 'approve', 'reject', 'cancel', 'clear', 'new', 'print', 'email'];
    }
    
    switch (status) {
        case 'DRAFT':
            return ['approve', 'reject']; // Can't approve/reject DRAFT
        case 'SUBMITTED':
            return ['save', 'submit']; // Can't edit or re-submit
        case 'APPROVED':
        case 'REJECTED':
        case 'CANCELLED':
            return ['save', 'submit', 'approve', 'reject', 'cancel']; // Read-only
        default:
            return [];
    }
};
```

#### 4.2 Pass to TransactionToolbar
- [ ] Pass disabled actions to toolbar
- [ ] Toolbar grays out disabled buttons
- [ ] Tooltip shows why disabled (optional)

---

### **PHASE 5: Validation Rules**

#### 5.1 Backend Validation
- [ ] Model-level validation (clean method)
- [ ] Serializer-level validation (validate method)
- [ ] ViewSet-level validation (perform_create, perform_update)
- [ ] Custom validators for complex rules

**Example**:
```python
class LeaveRequestSerializer(serializers.ModelSerializer):
    def validate(self, data):
        # Validate end date is after start date
        if data.get('end_date') and data.get('start_date'):
            if data['end_date'] < data['start_date']:
                raise serializers.ValidationError(
                    "End date cannot be before start date"
                )
        
        # Validate employee is active
        if data.get('employee') and not data['employee'].is_active:
            raise serializers.ValidationError(
                "Cannot create leave request for inactive employee"
            )
        
        # Validate leave balance
        if data.get('start_date') and data.get('end_date') and data.get('leave_type'):
            days = (data['end_date'] - data['start_date']).days + 1
            balance = get_leave_balance(data['employee'], data['leave_type'])
            if balance < days:
                raise serializers.ValidationError(
                    f"Insufficient leave balance. Available: {balance} days"
                )
        
        return data
```

#### 5.2 Frontend Validation
- [ ] Client-side validation before save
- [ ] Required field validation
- [ ] Format validation (dates, numbers, etc.)
- [ ] Business rule validation
- [ ] Returns error message or null

**Example**:
```typescript
const validateForm = (): string | null => {
    // Required fields
    if (!header.employee) return "Employee is required";
    if (!header.leave_type) return "Leave type is required";
    if (!header.start_date) return "Start date is required";
    if (!header.end_date) return "End date is required";
    if (!header.reason) return "Reason is required";
    
    // Date validation
    if (new Date(header.start_date) >= new Date(header.end_date)) {
        return "End date must be after start date";
    }
    
    // Business rule validation
    const totalDays = calculateTotalDays(header.start_date, header.end_date);
    if (totalDays <= 0) {
        return "Total days must be greater than 0";
    }
    
    if (totalDays > 30) {
        return "Leave request cannot exceed 30 days";
    }
    
    return null;
};
```

---

### **PHASE 6: Authorization & Scoping**

#### 6.1 Company Scoping (Backend)
- [ ] ViewSet `get_queryset()` filters by company
- [ ] Uses `self.request.user.company`
- [ ] Prevents cross-company access
- [ ] Applies to all CRUD operations

**Example**:
```python
def get_queryset(self):
    return LeaveRequest.objects.filter(
        company=self.request.user.company
    ).select_related('employee', 'leave_type')
```

#### 6.2 Role-Based Permissions (Backend)
- [ ] Define permission classes
- [ ] Check user role for workflow actions
- [ ] Return 403 if unauthorized

**Example**:
```python
@action(detail=True, methods=['post'])
def approve(self, request, pk=None):
    # Check if user has approval permission
    if not request.user.has_perm('hrm.approve_leaverequest'):
        return Response(
            {'error': 'You do not have permission to approve leave requests'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # ... rest of approval logic
```

#### 6.3 Company Scoping (Frontend)
- [ ] Service calls include company_id filter
- [ ] Uses `user.currentCompanyId` from auth context
- [ ] No hardcoded company IDs

---

### **PHASE 7: Audit Trail**

#### 7.1 Audit Fields (Backend)
- [ ] `created_by` foreign key to User
- [ ] `created_at` datetime field
- [ ] `updated_at` datetime field
- [ ] Workflow-specific fields (submitted_by, approved_by, etc.)
- [ ] Auto-populated in save/create

**Example**:
```python
class LeaveRequest(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='leaves_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    submitted_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='leaves_submitted')
    submitted_at = models.DateTimeField(null=True, blank=True)
    
    approved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='leaves_approved')
    approved_at = models.DateTimeField(null=True, blank=True)
    
    rejected_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='leaves_rejected')
    rejected_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
```

#### 7.2 Audit Trail Logging
- [ ] Log all status changes
- [ ] Log all workflow actions
- [ ] Include user, timestamp, old/new values
- [ ] Store in audit table or use django-auditlog

---

### **PHASE 8: Business Logic Integration**

#### 8.1 Side Effects on Workflow Actions
- [ ] Identify side effects for each action
- [ ] Implement in workflow action methods
- [ ] Handle rollback on error

**Example**:
```python
@action(detail=True, methods=['post'])
def approve(self, request, pk=None):
    leave_request = self.get_object()
    
    # ... status validation ...
    
    # Update status
    leave_request.status = 'APPROVED'
    leave_request.approved_by = request.user
    leave_request.approved_at = timezone.now()
    leave_request.save()
    
    # Side effect: Update leave balance
    try:
        update_leave_balance(
            employee=leave_request.employee,
            leave_type=leave_request.leave_type,
            days=leave_request.total_days,
            operation='deduct'
        )
    except InsufficientLeaveBalanceError as e:
        # Rollback status change
        leave_request.status = 'SUBMITTED'
        leave_request.approved_by = None
        leave_request.approved_at = None
        leave_request.save()
        
        return Response(
            {'error': f'Insufficient leave balance: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    serializer = self.get_serializer(leave_request)
    return Response(serializer.data)
```

---

### **PHASE 9: Configuration Pages (Optional)**

#### 9.1 Module Configuration Model
- [ ] Model for module-level settings
- [ ] Company-specific configuration
- [ ] Default values

**Example**:
```python
class HRMConfig(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    
    # Leave configuration
    max_leave_days_per_request = models.IntegerField(default=30)
    require_leave_balance_check = models.BooleanField(default=True)
    auto_approve_manager_leave = models.BooleanField(default=False)
    
    # Approval configuration
    require_manager_approval = models.BooleanField(default=True)
    require_hr_approval = models.BooleanField(default=False)
    
    # Notification configuration
    send_approval_notifications = models.BooleanField(default=True)
    send_rejection_notifications = models.BooleanField(default=True)
```

#### 9.2 Configuration UI Page
- [ ] Page to view/edit configuration
- [ ] Form with all config fields
- [ ] Save button
- [ ] Company scoping

---

### **PHASE 10: Testing**

#### 10.1 Workflow Transition Tests
- [ ] Test all valid transitions
- [ ] Test invalid transitions (should fail)
- [ ] Test status updates correctly
- [ ] Test audit fields populated

#### 10.2 Validation Tests
- [ ] Test required field validation
- [ ] Test business rule validation
- [ ] Test error messages display
- [ ] Test cannot save invalid data

#### 10.3 Authorization Tests
- [ ] Test company scoping works
- [ ] Test cannot access other company's data
- [ ] Test role-based permissions
- [ ] Test unauthorized actions fail

#### 10.4 Business Logic Tests
- [ ] Test side effects execute
- [ ] Test rollback on error
- [ ] Test integration with other modules

---

## ✅ COMPLETION CHECKLIST

- [ ] Status state machine defined (backend & frontend)
- [ ] All workflow actions implemented (backend)
- [ ] All workflow service methods created (frontend)
- [ ] All workflow action handlers implemented (frontend)
- [ ] Disabled actions logic implemented
- [ ] Validation rules implemented (backend & frontend)
- [ ] Authorization & scoping implemented
- [ ] Audit trail implemented
- [ ] Business logic integration complete
- [ ] Configuration page created (if needed)
- [ ] All tests passed

---

## 📚 Reference Files

**Backend**:
- `backend/apps/hrm/backend/leave/models.py`
- `backend/apps/hrm/backend/leave/serializers.py`
- `backend/apps/hrm/backend/leave/views.py` (LeaveRequestViewSet)

**Frontend**:
- `frontend/apps/hrm/leave/hrm.service.ts`
- `frontend/apps/hrm/leave/pages/LeaveRequestFormPage.tsx`

**Standards**:
- `.steering/14_UI_CANON/TXN-M.md`
- `.steering/governance.md`

---

**Last Updated**: 2026-01-11  
**Maintainer**: Astra (ERP Platform Development Owner)
