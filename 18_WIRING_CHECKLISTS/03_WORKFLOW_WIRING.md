# Workflow & Business Rules - Wiring Checklist

**For**: Status machines, Workflow actions, Validation rules, Configuration pages

**Reference Implementations**:
- ✅ `backend/domain/shared/views.py` (BaseWorkflowViewSet)
- ✅ `frontend/src/services/workflowService.ts`
- ✅ `frontend/apps/shared/pages/TransactionFormPage.tsx`

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
class Transaction(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted'),
        ('APPROVED', 'Approved'),
        ('CLOSED', 'Closed'),
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
export type TransactionStatus = 'DRAFT' | 'SUBMITTED' | 'APPROVED' | 'CLOSED' | 'CANCELLED';

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
    next: 'CLOSED', 
    label: 'Approved', 
    color: 'text-blue-600',
    bgColor: 'bg-blue-100',
    description: 'Approved by manager'
  },
  CLOSED: { 
    next: null, 
    label: 'Closed', 
    color: 'text-gray-900',
    bgColor: 'bg-gray-200',
    description: 'Order completed and closed'
  },
  CANCELLED: { 
    next: null, 
    label: 'Cancelled', 
    color: 'text-red-600',
    bgColor: 'bg-red-100',
    description: 'Order cancelled'
  }
};
```

#### 1.3 Document Workflow Diagram
- [ ] Create visual workflow diagram (optional)
- [ ] Document in BBP or README
- [ ] Show all transitions

**Example**:
```
DRAFT → SUBMITTED → APPROVED → CLOSED
                         ↓
                    CANCELLED
```

---

### **PHASE 2: Backend Workflow Actions**

#### 2.1 Submit Action
- [ ] `@action` decorator with `detail=True, methods=['post']`
- [ ] Validates current status (must be DRAFT)
- [ ] Updates status to SUBMITTED
- [ ] Logs audit trail
- [ ] Returns updated serializer data

**Example**:
```python
@action(detail=True, methods=['post'])
def submit(self, request, pk=None):
    """Submit record for approval"""
    txn = self.get_object()
    
    # Validate status
    if txn.status != 'DRAFT':
        return Response(
            {'error': 'Only DRAFT records can be submitted'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Update status
    txn.status = 'SUBMITTED'
    txn.submitted_by = request.user
    txn.submitted_at = timezone.now()
    txn.save()
    
    # Return updated data
    serializer = self.get_serializer(txn)
    return Response(serializer.data)
```

#### 2.2 Approve Action
- [ ] Validates current status (must be SUBMITTED)
- [ ] Updates status to APPROVED
- [ ] Records approver and timestamp
- [ ] Performs any business logic (e.g., reserve inventory)
- [ ] Returns updated data

**Example**:
```python
@action(detail=True, methods=['post'])
def approve(self, request, pk=None):
    """Approve record"""
    txn = self.get_object()
    
    if txn.status != 'SUBMITTED':
        return Response(
            {'error': 'Only SUBMITTED records can be approved'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    txn.status = 'APPROVED'
    txn.approved_by = request.user
    txn.approved_at = timezone.now()
    txn.save()
    
    # Business logic (e.g., reserve inventory)
    # ...
    
    serializer = self.get_serializer(txn)
    return Response(serializer.data)
```

#### 2.3 Cancel Action
- [ ] Validates current status (usually DRAFT or SUBMITTED)
- [ ] Updates status to CANCELLED
- [ ] Records cancellation reason (optional)
- [ ] Reverses any side effects (e.g., unreserve inventory)
- [ ] Returns updated data

**Example**:
```python
@action(detail=True, methods=['post'])
def cancel(self, request, pk=None):
    """Cancel record"""
    txn = self.get_object()
    
    if txn.status not in ['DRAFT', 'SUBMITTED']:
        return Response(
            {'error': 'Only DRAFT or SUBMITTED records can be cancelled'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    txn.status = 'CANCELLED'
    txn.cancelled_by = request.user
    txn.cancelled_at = timezone.now()
    txn.cancellation_reason = request.data.get('reason', '')
    txn.save()
    
    # Reverse side effects
    # ...
    
    serializer = self.get_serializer(txn)
    return Response(serializer.data)
```

#### 2.4 Additional Workflow Actions
- [ ] Implement all necessary workflow actions
- [ ] Each action validates status
- [ ] Each action updates status
- [ ] Each action logs audit trail
- [ ] Each action handles business logic

---

### **PHASE 3: Frontend Workflow Methods**

#### 3.1 Service Methods for Workflow Actions
- [ ] Method for each workflow action
- [ ] Uses POST to custom action endpoint
- [ ] Returns updated transaction data

**Example**:
```typescript
export const workflowService = {
  submitRecord: async (id: string) => {
    const response = await apiClient.post(`/module/records/${id}/submit/`);
    return response.data;
  },
  
  approveRecord: async (id: string) => {
    const response = await apiClient.post(`/module/records/${id}/approve/`);
    return response.data;
  },
  
  cancelRecord: async (id: string, reason?: string) => {
    const response = await apiClient.post(`/module/records/${id}/cancel/`, { reason });
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
    setError('Please save the record before submitting');
    return;
  }
  
  setSaving(true);
  setError(null);
  
  try {
    const submitted = await workflowService.submitRecord(id!);
    setHeader(prev => ({ ...prev, status: submitted.status as TransactionStatus }));
  } catch (err: any) {
    setError(err.response?.data?.error || err.message || 'Failed to submit');
  } finally {
    setSaving(false);
  }
};

const handleApprove = async () => {
  if (!confirm('Approve this record?')) return;
  
  setSaving(true);
  setError(null);
  
  try {
    const approved = await workflowService.approveRecord(id!);
    setHeader(prev => ({ ...prev, status: approved.status as TransactionStatus }));
  } catch (err: any) {
    setError(err.response?.data?.error || err.message || 'Failed to approve');
  } finally {
    setSaving(false);
  }
};

const handleCancel = async () => {
  const reason = prompt('Cancellation reason (optional):');
  if (reason === null) return; // User clicked cancel
  
  setSaving(true);
  setError(null);
  
  try {
    const cancelled = await procurementService.cancelPurchaseOrder(id!, reason);
    setHeader(prev => ({ ...prev, status: cancelled.status as POStatus }));
  } catch (err: any) {
    setError(err.response?.data?.error || err.message || 'Failed to cancel');
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
const getDisabledActions = (status: POStatus): string[] => {
  // Disable all actions while saving
  if (saving) {
    return ['save', 'submit', 'approve', 'cancel', 'clear', 'new', 'print', 'email'];
  }
  
  switch (status) {
    case 'DRAFT':
      return ['approve']; // Can't approve DRAFT
    
    case 'SUBMITTED':
      return ['save', 'submit']; // Can't edit or re-submit
    
    case 'APPROVED':
    case 'CONFIRMED':
    case 'CLOSED':
      return ['save', 'submit', 'approve', 'cancel']; // Read-only
    
    case 'CANCELLED':
      return ['save', 'submit', 'approve', 'cancel']; // Read-only
    
    default:
      return [];
  }
};
```

#### 4.2 Pass to TransactionToolbar
- [ ] Pass disabled actions to toolbar
- [ ] Toolbar grays out disabled buttons
- [ ] Tooltip shows why disabled (optional)

**Example**:
```tsx
<TransactionToolbar
  status={header.status.toUpperCase() as TransactionStatus}
  onAction={handleToolbarAction}
  disabledActions={getDisabledActions(header.status)}
/>
```

---

### **PHASE 5: Validation Rules**

#### 5.1 Backend Validation
- [ ] Model-level validation (clean method)
- [ ] Serializer-level validation (validate method)
- [ ] ViewSet-level validation (perform_create, perform_update)
- [ ] Custom validators for complex rules

**Example**:
```python
class PurchaseOrderSerializer(serializers.ModelSerializer):
    def validate(self, data):
        # Validate delivery date is after order date
        if data.get('expected_delivery_date') and data.get('order_date'):
            if data['expected_delivery_date'] < data['order_date']:
                raise serializers.ValidationError(
                    "Delivery date cannot be before order date"
                )
        
        # Validate supplier is active
        if data.get('supplier') and not data['supplier'].is_active:
            raise serializers.ValidationError(
                "Cannot create PO for inactive supplier"
            )
        
        return data
    
    def validate_lines(self, value):
        if not value or len(value) == 0:
            raise serializers.ValidationError("At least one line item is required")
        
        for line in value:
            if line['ordered_qty'] <= 0:
                raise serializers.ValidationError("Quantity must be greater than 0")
        
        return value
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
  if (!header.supplier) return "Supplier is required";
  if (!header.delivery_location) return "Delivery location is required";
  if (!header.order_date) return "Order date is required";
  
  // Date validation
  if (header.expected_delivery_date && header.expected_delivery_date < header.order_date) {
    return "Delivery date cannot be before order date";
  }
  
  // Line items validation
  if (lines.length === 0) return "At least one line item is required";
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    
    if (!line.item_id && !line.item_code) {
      return `Line ${i + 1}: Item is required`;
    }
    
    if (!line.ordered_qty || line.ordered_qty <= 0) {
      return `Line ${i + 1}: Quantity must be greater than 0`;
    }
    
    if (!line.unit_price || line.unit_price < 0) {
      return `Line ${i + 1}: Unit price must be 0 or greater`;
    }
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
    return PurchaseOrder.objects.filter(
        company=self.request.user.company
    ).select_related('supplier', 'delivery_location')
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
    if not request.user.has_perm('procurement.approve_purchaseorder'):
        return Response(
            {'error': 'You do not have permission to approve POs'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # ... rest of approval logic
```

#### 6.3 Company Scoping (Frontend)
- [ ] Service calls include company_id filter
- [ ] Uses `user.currentCompanyId` from auth context
- [ ] No hardcoded company IDs

**Example**:
```typescript
const { user } = useAuth();

const [header, setHeader] = useState({
  company: user?.currentCompanyId || '',
  // ... other fields
});
```

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
class PurchaseOrder(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='pos_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    submitted_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='pos_submitted')
    submitted_at = models.DateTimeField(null=True, blank=True)
    
    approved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='pos_approved')
    approved_at = models.DateTimeField(null=True, blank=True)
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
    po = self.get_object()
    
    # ... status validation ...
    
    # Update status
    po.status = 'APPROVED'
    po.approved_by = request.user
    po.approved_at = timezone.now()
    po.save()
    
    # Side effect: Reserve inventory
    for line in po.lines.all():
        try:
            reserve_inventory(
                item=line.item,
                quantity=line.ordered_qty,
                location=po.delivery_location,
                reference=f"PO-{po.po_number}"
            )
        except InsufficientStockError as e:
            # Rollback status change
            po.status = 'SUBMITTED'
            po.approved_by = None
            po.approved_at = None
            po.save()
            
            return Response(
                {'error': f'Insufficient stock for {line.item.item_name}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    serializer = self.get_serializer(po)
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
class ProcurementConfig(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    auto_approve_threshold = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    require_approval = models.BooleanField(default=True)
    default_payment_terms = models.CharField(max_length=50, default='NET 30')
    po_number_prefix = models.CharField(max_length=10, default='PO')
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
- `backend/apps/retail/backend/procurement/models.py`
- `backend/apps/retail/backend/procurement/serializers.py`
- `backend/apps/retail/backend/procurement/views.py` (PurchaseOrderViewSet)

**Frontend**:
- `frontend/src/services/workflowService.ts`
- `frontend/apps/shared/pages/TransactionFormPage.tsx`

**Standards**:
- `.steering/14_UI_CANON/TXN-M.md`
- `.steering/governance.md`

---

**Last Updated**: 2026-01-07  
**Maintainer**: Astra (ERP Platform Development Owner)
