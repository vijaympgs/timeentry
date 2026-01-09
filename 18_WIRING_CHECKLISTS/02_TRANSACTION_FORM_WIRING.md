# Transaction Form Page - Wiring Checklist

**For**: Leave Request, Attendance, Lead, Opportunity, Invoice, Goods Receipt (Transaction Forms)

**Reference Implementation**:
- ✅ `frontend/apps/shared/pages/TransactionFormPage.tsx`

**Pattern**: Transaction form with toolbar, header, line items, lookups, workflow actions

---

## 📋 COMPLETE WIRING CHECKLIST

### **PHASE 1: Backend Setup**

#### 1.1 Header Model Verification
- [ ] Header model exists (e.g., `LeaveRequest`, `Lead`)
- [ ] Has `company` foreign key
- [ ] Has `status` field with choices (DRAFT, SUBMITTED, APPROVED, etc.)
- [ ] Has transaction number field (auto-generated)
- [ ] Has date field(s)
- [ ] Has reference fields (employee, customer, category, etc.)
- [ ] Has total fields (if applicable)
- [ ] Has audit fields (created_by, created_at, updated_at)

#### 1.2 Line Model Verification
- [ ] Line model exists (e.g., `TransactionLine`)
- [ ] Has foreign key to header model
- [ ] Has `line_number` field
- [ ] Has `item` or `reference` foreign key
- [ ] Has quantity field(s) (if applicable)
- [ ] Has amount field(s) (if applicable)
- [ ] Has `line_total` field
- [ ] Has optional fields (remarks, flags)

#### 1.3 Serializer Setup
- [ ] Header serializer created with nested line serializer
- [ ] Line serializer includes read-only fields (item_name, uom_name, etc.)
- [ ] Header serializer has custom `create()` method
- [ ] Header serializer has custom `update()` method
- [ ] Auto-generates transaction number in `create()`
- [ ] Calculates totals in `create()`/`update()`
- [ ] Read-only fields properly defined

**Example**:
```python
class TransactionLineSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    
    class Meta:
        model = TransactionLine
        fields = '__all__'
        read_only_fields = ['line_id', 'header']

class TransactionSerializer(serializers.ModelSerializer):
    lines = TransactionLineSerializer(many=True, read_only=True)
    
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['id', 'txn_number', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Auto-generate TXN number
        validated_data['txn_number'] = f"TXN-{timezone.now().strftime('%Y%m%d%H%M%S')}"
        return super().create(validated_data)
```

#### 1.4 ViewSet with Workflow Actions
- [ ] ViewSet created with `ModelViewSet`
- [ ] Has `get_queryset()` with company scoping
- [ ] Has `@action` methods for workflow (submit, approve, cancel, etc.)
- [ ] Workflow actions validate status transitions
- [ ] Workflow actions update status
- [ ] Workflow actions log audit trail

**Example**:
```python
**Example**:
```python
class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    
    def get_queryset(self):
        return Transaction.objects.filter(company=self.request.user.company)
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        txn = self.get_object()
        if txn.status != 'DRAFT':
            return Response({'error': 'Only DRAFT records can be submitted'}, status=400)
        txn.status = 'SUBMITTED'
        txn.save()
        return Response(self.get_serializer(txn).data)
```
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        po = self.get_object()
        if po.status != 'SUBMITTED':
            return Response({'error': 'Only SUBMITTED POs can be approved'}, status=400)
        po.status = 'APPROVED'
        po.approved_by = request.user
        po.approved_at = timezone.now()
        po.save()
        return Response(self.get_serializer(po).data)
```

#### 1.5 URL Registration
- [ ] ViewSet registered in router
- [ ] Endpoint follows pattern: `/api/{module}/{resource}/`

---

### **PHASE 2: Frontend Service Layer**

#### 2.1 TypeScript Types
- [ ] Header interface defined
- [ ] Line interface defined
- [ ] Status type defined (union of status strings)
- [ ] All fields properly typed

**Example**:
```typescript
**Example**:
```typescript
export type TransactionStatus = 'DRAFT' | 'SUBMITTED' | 'APPROVED' | 'CLOSED' | 'CANCELLED';

export interface TransactionLine {
  id?: string;
  line_number: number;
  item_id?: string;
  item_name?: string;
  quantity: number;
  unit_price: number;
  line_total: number;
  remarks?: string;
}

export interface TransactionHeader {
  id?: string;
  txn_number: string;
  company: string;
  reference_id: string;
  reference_name?: string;
  txn_date: string;
  status: TransactionStatus;
  subtotal?: number;
  grand_total?: number;
  lines?: TransactionLine[];
  created_at?: string;
  updated_at?: string;
}
```
```

#### 2.2 Service Methods
- [ ] CRUD methods (get, create, update, delete)
- [ ] Workflow action methods (submit, approve, cancel, etc.)
- [ ] All methods use `apiClient`

**Example**:
```typescript
**Example**:
```typescript
export const transactionService = {
  // CRUD
  getTransactions: async (filters?: any) => {
    const response = await apiClient.get('/module/transactions/', { params: filters });
    return response.data;
  },
  
  getTransaction: async (id: string) => {
    const response = await apiClient.get(`/module/transactions/${id}/`);
    return response.data;
  },
  
  // Workflow actions
  submitTransaction: async (id: string) => {
    const response = await apiClient.post(`/module/transactions/${id}/submit/`);
    return response.data;
  },
};
```
```

---

### **PHASE 3: Component Setup**

#### 3.1 Component Structure
- [ ] Component created in `frontend/apps/{module}/pages/`
- [ ] Uses TypeScript with proper typing
- [ ] Imports all necessary dependencies

**Required Imports**:
```typescript
import React, { useState, useEffect, useCallback } from "react";
import { Save, Printer, Mail, Plus, Trash2, Calendar, ChevronLeft } from "lucide-react";
import { useNavigate, useParams } from "react-router-dom";
import { MasterToolbar, MasterMode } from "@ui/components/MasterToolbarConfigDriven";
import { LookupModal } from "@ui/components/LookupModal";
import { useAuth } from "@auth/useAuth";
import { transactionService } from "../transaction.service";
import type { TransactionHeader, TransactionLine, TransactionStatus } from "../transaction.types";
```

#### 3.2 State Management
- [ ] `header` state (transaction metadata)
- [ ] `lines` state (array of line items)
- [ ] `loading` state
- [ ] `saving` state
- [ ] `error` state
- [ ] Modal states (product, supplier, location, etc.)
- [ ] `activeLineIndex` state (for F12 lookup)

**Example**:
```typescript
const [header, setHeader] = useState({
  txn_number: '',
  company: user?.currentCompanyId || '',
  reference_id: '',
  reference_name: '',
  txn_date: new Date().toISOString().split('T')[0],
  status: 'DRAFT' as TransactionStatus
});

const [lines, setLines] = useState<TransactionLine[]>([]);
const [loading, setLoading] = useState(false);
const [saving, setSaving] = useState(false);
const [error, setError] = useState<string | null>(null);
const [activeLineIndex, setActiveLineIndex] = useState<number | null>(null);
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
- [ ] useEffect hook for loading data
- [ ] Only runs if not new
- [ ] Fetches transaction by ID
- [ ] Maps backend data to UI state
- [ ] Handles errors

**Example**:
```typescript
useEffect(() => {
  if (!isNew && id) {
    setLoading(true);
    transactionService.getTransaction(id)
      .then(txn => {
        setHeader({
          txn_number: txn.txn_number,
          company: txn.company,
          reference_id: txn.reference_id,
          reference_name: txn.reference_name || '',
          txn_date: txn.txn_date,
          status: txn.status
        });
        
        const mappedLines: TransactionLine[] = (txn.lines || []).map(line => ({
          ...line,
          quantity: Number(line.quantity),
          unit_price: Number(line.unit_price),
          line_total: Number(line.line_total),
        }));
        setLines(mappedLines);
      })
      .catch(err => {
        setError(err.message || 'Failed to load transaction');
      })
      .finally(() => setLoading(false));
  }
}, [id, isNew]);
```

---

### **PHASE 5: TransactionToolbar Integration**

#### 5.1 Toolbar Component
- [ ] Import `MasterToolbar` component
- [ ] Logic for all actions driven by backend config string.

**Example**:
```tsx
<MasterToolbar
  viewId="MODULE_TRANSACTION_FORM"
  mode={isNew ? 'CREATE' : 'EDIT'}
  onAction={handleToolbarAction}
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
      navigate('/module/records/new');
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
      navigate('/module/records');
      break;
    case 'submit':
      handleSubmit();
      break;
    case 'lookup_item':
      setIsProductModalOpen(true);
      break;
    case 'lookup_supplier':
      setIsSupplierModalOpen(true);
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
const getDisabledActions = (status: POStatus): string[] => {
  if (saving) return ['save', 'submit', 'clear', 'new', 'print', 'email'];
  
  switch (status) {
    case 'DRAFT':
      return ['authorize', 'amend'];
    case 'CONFIRMED':
    case 'CLOSED':
    case 'CANCELLED':
      return ['new', 'save', 'clear', 'cancel', 'clone', 'submit', 'authorize'];
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
- [ ] Grand total display (prominent)
- [ ] Back button with ChevronLeft icon
- [ ] Form fields in grid layout (4 columns)

**Example**:
```tsx
<div className="bg-white border-b border-[#edebe9] shrink-0">
  <TransactionToolbar {...} />
  
  <div className="px-6 py-4">
    <div className="flex justify-between items-center mb-1">
      <div className="flex items-center gap-3">
        <button onClick={() => navigate(-1)} className="p-1 hover:bg-[#f3f2f1] rounded-full">
          <ChevronLeft size={20} className="text-[#605e5c]" />
        </button>
        <h1 className="text-xl font-semibold text-[#201f1e]">
          Purchase Order <span className="text-[#0078d4] font-light ml-1">{header.po_number}</span>
        </h1>
        <span className={`ml-2 px-2 py-0.5 rounded-full text-[10px] font-bold uppercase ${getStatusColor(header.status)}`}>
          {header.status}
        </span>
      </div>
      <div className="text-right">
        <span className="text-2xl font-semibold text-[#201f1e]">${grandTotal.toFixed(2)}</span>
      </div>
    </div>
  </div>
</div>
```

#### 6.2 Form Fields Grid
- [ ] 4-column grid layout
- [ ] Lookup fields with buttons
- [ ] Date fields with Calendar icon
- [ ] Text fields with appropriate icons
- [ ] Bottom border on inputs
- [ ] Hover effects

**Example**:
```tsx
<div className="grid grid-cols-4 gap-6 bg-white p-6 border border-[#edebe9] shadow-sm rounded-sm mb-6">
  <div className="space-y-1">
    <label className="text-xs font-semibold text-[#605e5c] uppercase">Supplier *</label>
    <div className="flex items-center gap-2">
      <div className="flex-1 flex items-center gap-2 border-b border-[#8a8886] hover:border-[#323130] pb-1">
        <Building2 size={14} className="text-[#0078d4]" />
        <input
          type="text"
          value={header.supplier_name || 'Click lookup to select...'}
          readOnly
          className="w-full outline-none bg-transparent font-medium text-[#0078d4] cursor-pointer"
          onClick={() => setIsSupplierModalOpen(true)}
        />
      </div>
      <button
        onClick={() => setIsSupplierModalOpen(true)}
        className="px-2 py-1 text-xs bg-[#0078d4] text-white rounded hover:bg-[#106ebe]"
        title="Lookup Supplier (F3)"
      >
        Lookup
      </button>
    </div>
  </div>
  
  <div className="space-y-1">
    <label className="text-xs font-semibold text-[#605e5c] uppercase">Order Date</label>
    <div className="flex items-center gap-2 border-b border-[#8a8886] hover:border-[#323130] pb-1">
      <Calendar size={14} className="text-[#605e5c]" />
      <input 
        type="date" 
        value={header.order_date} 
        onChange={e => setHeader({ ...header, order_date: e.target.value })} 
        className="w-full outline-none bg-transparent" 
      />
    </div>
  </div>
</div>
```

---

### **PHASE 7: Line Items Grid**

#### 7.1 Line Items Table
- [ ] Editable table with borders
- [ ] Column headers (Item Code, Name, Qty, UOM, Price, Total, Actions)
- [ ] New line logic (e.g. auto-add on last row Tab/Enter)
- [ ] Remove line via row action (Trash2 icon)
- [ ] Enter key navigation

**Example**:
```tsx
<div className="bg-white border border-[#edebe9] shadow-sm rounded-sm p-6 mb-6">
  <div className="flex items-center justify-between mb-4">
    <span className="text-[#0078d4] font-semibold border-b-2 border-[#0078d4] pb-1 text-sm uppercase">
      Line Items
    </span>
  </div>
  
  <div className="border border-[#edebe9] rounded-sm overflow-hidden">
    <table className="w-full border-collapse">
      <thead className="bg-[#f3f2f1] text-[#323130]">
        <tr className="text-xs uppercase tracking-wider text-left border-b border-[#edebe9]">
          <th className="p-3 w-12 text-center">#</th>
          <th className="p-3 w-32 border-l border-[#edebe9]">Item Code</th>
          <th className="p-3 border-l border-[#edebe9]">Item Name</th>
          <th className="p-3 w-28 text-right border-l border-[#edebe9]">Qty</th>
          <th className="p-3 w-28 text-center border-l border-[#edebe9]">UOM</th>
          <th className="p-3 w-32 text-right border-l border-[#edebe9]">Unit Price</th>
          <th className="p-3 w-32 text-right border-l border-[#edebe9]">Total</th>
          <th className="p-3 w-12 text-center border-l border-[#edebe9]"></th>
        </tr>
      </thead>
      <tbody className="text-sm">
        {lines.map((line, index) => (
          <tr key={line.id} className="border-b border-[#f3f2f1] hover:bg-[#f3f9ff]">
            <td className="p-3 text-center text-[#a19f9d]">{index + 1}</td>
            <td className="p-0 border-l border-[#edebe9]">
              <input
                type="text"
                value={line.item_code}
                onChange={e => updateLine(index, 'item_code', e.target.value)}
                onKeyDown={(e) => handleKeyDown(e, index, 'item_code')}
                onFocus={() => setActiveLineIndex(index)}
                placeholder="Enter or F12"
                className="w-full p-3 outline-none bg-transparent focus:bg-white"
              />
            </td>
            <td className="p-0 border-l border-[#edebe9]">
              <input 
                type="text" 
                value={line.item_name} 
                onChange={e => updateLine(index, 'item_name', e.target.value)} 
                className="w-full p-3 outline-none bg-transparent focus:bg-white" 
              />
            </td>
            <td className="p-0 border-l border-[#edebe9]">
              <input
                type="number"
                value={line.ordered_qty}
                onChange={e => updateLine(index, 'ordered_qty', parseFloat(e.target.value))}
                className="w-full p-3 outline-none bg-transparent text-right focus:bg-white"
              />
            </td>
            <td className="p-0 border-l border-[#edebe9]">
              <input
                type="text"
                value={line.uom || ''}
                readOnly
                className="w-full p-3 outline-none bg-gray-50 text-center text-gray-600"
              />
            </td>
            <td className="p-0 border-l border-[#edebe9]">
              <input 
                type="number" 
                value={line.unit_price} 
                onChange={e => updateLine(index, 'unit_price', parseFloat(e.target.value))} 
                className="w-full p-3 outline-none bg-transparent text-right focus:bg-white" 
              />
            </td>
            <td className="p-3 text-right border-l border-[#edebe9] font-medium">
              {line.line_total.toFixed(2)}
            </td>
            <td className="p-3 text-center border-l border-[#edebe9]">
              <button onClick={() => removeLine(index)} className="text-[#a19f9d] hover:text-red-600">
                <Trash2 size={16} />
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
</div>
```

#### 7.2 Line Management Functions
- [ ] `addLine()` - Adds new empty line
- [ ] `updateLine()` - Updates line field
- [ ] `removeLine()` - Removes line and renumbers
- [ ] `calculateLineTotal()` - Recalculates on qty/price change

**Example**:
```typescript
const addLine = () => {
  const newLine: OrderLine = {
    line_number: lines.length + 1,
    item_code: '',
    item_name: '',
    ordered_qty: 1,
    uom: 'PCS',
    unit_price: 0,
    line_total: 0
  };
  setLines([...lines, newLine]);
};

const updateLine = (index: number, field: keyof OrderLine, value: any) => {
  const newLines = [...lines];
  const line = { ...newLines[index], [field]: value };
  
  if (field === 'ordered_qty' || field === 'unit_price') {
    const qty = Number(line.ordered_qty) || 0;
    const price = Number(line.unit_price) || 0;
    line.line_total = qty * price;
  }
  
  newLines[index] = line;
  setLines(newLines);
};

const removeLine = (index: number) => {
  const newLines = lines.filter((_, i) => i !== index);
  newLines.forEach((line, idx) => {
    line.line_number = idx + 1;
  });
  setLines(newLines);
};
```

#### 7.3 Keyboard Navigation
- [ ] F12 opens product lookup
- [ ] Enter on qty field adds new line (if last line)
- [ ] Tab navigation works

**Example**:
```typescript
const handleKeyDown = (e: React.KeyboardEvent, index: number, field: string) => {
  if (e.key === 'F12' || (field === 'item_code' && e.key === 'Enter')) {
    e.preventDefault();
    setActiveLineIndex(index);
    setIsProductModalOpen(true);
  }
  if (e.key === 'Enter' && field === 'ordered_qty') {
    if (index === lines.length - 1) {
      addLine();
    }
  }
};
```

---

### **PHASE 8: Calculations**

#### 8.1 Grand Total Calculation
- [ ] Uses `useMemo` for performance
- [ ] Sums all line totals
- [ ] Includes tax/discount if applicable

**Example**:
```typescript
const grandTotal = useMemo(() => {
  return lines.reduce((sum, line) => sum + (line.line_total || 0), 0);
}, [lines]);
```

---

### **PHASE 9: Save & Workflow Actions**

#### 9.1 Validation Function
- [ ] Validates required fields
- [ ] Validates line items
- [ ] Returns error message or null

**Example**:
```typescript
const validateForm = (): string | null => {
  if (!header.supplier) return "Supplier is required";
  if (!header.delivery_location) return "Delivery location is required";
  if (lines.length === 0) return "At least one line item is required";
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (!line.item_id && !line.item_code) {
      return `Line ${i + 1}: Item is required`;
    }
    if (!line.ordered_qty || line.ordered_qty <= 0) {
      return `Line ${i + 1}: Quantity must be greater than 0`;
    }
  }
  
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

**Example**:
```typescript
const handleSave = async () => {
  const validationError = validateForm();
  if (validationError) {
    setError(validationError);
    return;
  }
  
  setSaving(true);
  setError(null);
  
  try {
    const apiLines: any[] = lines.map(line => ({
      line_number: line.line_number,
      item_id: line.item_id,
      uom_id: line.uom_id,
      ordered_qty: line.ordered_qty,
      unit_price: line.unit_price,
      line_total: line.line_total,
    }));
    
    const poData: Partial<PurchaseOrder> = {
      ...header,
      lines: apiLines
    };
    
    if (isNew) {
      const created = await procurementService.createPurchaseOrder(poData);
      navigate(`/procurement/orders/${created.id}`);
    } else {
      await procurementService.updatePurchaseOrder(id!, poData);
      const updated = await procurementService.getPurchaseOrder(id!);
      setHeader(prev => ({ ...prev, status: updated.status as POStatus }));
    }
  } catch (err: any) {
    setError(err.response?.data?.error || err.message || 'Failed to save');
  } finally {
    setSaving(false);
  }
};
```

#### 9.3 Workflow Action Handlers
- [ ] `handleSubmit()` - Submits for approval
- [ ] `handleApprove()` - Approves transaction
- [ ] `handleCancel()` - Cancels transaction
- [ ] Each validates status before calling API
- [ ] Each updates local status on success

**Example**:
```typescript
const handleSubmit = async () => {
  if (isNew) {
    setError('Please save the PO before submitting');
    return;
  }
  
  setSaving(true);
  setError(null);
  
  try {
    const submitted = await procurementService.submitPurchaseOrder(id!);
    setHeader(prev => ({ ...prev, status: submitted.status as POStatus }));
  } catch (err: any) {
    setError(err.response?.data?.error || err.message || 'Failed to submit');
  } finally {
    setSaving(false);
  }
};
```

---

### **PHASE 10: Lookup Modals**

#### 10.1 Product Lookup Integration
- [ ] Import ProductLookupModal
- [ ] State for modal open/close
- [ ] Handler for product selection
- [ ] Updates line item on selection
- [ ] Auto-populates item fields

**Example**:
```typescript
const handleProductSelect = (product: ProductLookupResult) => {
  if (activeLineIndex !== null && lines[activeLineIndex]) {
    const newLines = [...lines];
    newLines[activeLineIndex] = {
      ...newLines[activeLineIndex],
      item_id: product.id,
      item_code: product.item_code,
      item_name: product.item_name,
      uom_id: String(product.uom_id),
      uom: product.stock_uom,
      unit_price: product.retail_price || 0,
      line_total: product.retail_price || 0
    };
    setLines(newLines);
    setActiveLineIndex(null);
  }
};
```

#### 10.2 Supplier/Customer Lookup Integration
- [ ] Import SupplierLookupModal or CustomerLookupModal
- [ ] State for modal open/close
- [ ] Handler for selection
- [ ] Updates header on selection

**Example**:
```typescript
const handleSupplierSelect = (supplier: SupplierLookupResult) => {
  setHeader({
    ...header,
    supplier: supplier.id,
    supplier_name: supplier.supplier_name
  });
};
```

#### 10.3 Modal Rendering
- [ ] Conditional rendering based on state
- [ ] Pass companyId from user context
- [ ] Pass onClose and onSelect handlers

**Example**:
```tsx
<ProductLookupModal
  isOpen={isProductModalOpen}
  onClose={() => setIsProductModalOpen(false)}
  onSelect={handleProductSelect}
  companyId={user?.currentCompanyId}
/>

<SupplierLookupModal
  isOpen={isSupplierModalOpen}
  onClose={() => setIsSupplierModalOpen(false)}
  onSelect={handleSupplierSelect}
  companyId={user?.currentCompanyId}
/>
```

---

### **PHASE 11: Error Handling**

#### 11.1 Error Banner
- [ ] Conditional rendering based on error state
- [ ] Red background with border
- [ ] Dismissible
- [ ] Positioned below toolbar

**Example**:
```tsx
{error && (
  <div className="bg-red-50 border-l-4 border-red-500 p-4 mx-6 mt-4">
    <div className="flex items-center">
      <div className="flex-shrink-0">
        <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
        </svg>
      </div>
      <div className="ml-3">
        <p className="text-sm text-red-700">{error}</p>
      </div>
      <div className="ml-auto pl-3">
        <button onClick={() => setError(null)} className="text-red-500 hover:text-red-700">
          ×
        </button>
      </div>
    </div>
  </div>
)}
```

---

### **PHASE 12: Loading States**

#### 12.1 Initial Loading
- [ ] Shows spinner while loading
- [ ] Centers spinner
- [ ] Uses Loader2 icon with spin animation

**Example**:
```tsx
if (loading) {
  return (
    <div className="flex items-center justify-center h-full">
      <Loader2 className="animate-spin text-[#0078d4]" size={32} />
    </div>
  );
}
```

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
- [ ] Text colors from palette (`text-[#201f1e]`, `text-[#605e5c]`)
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

#### 14.2 Line Items
- [ ] Add line works
- [ ] Edit line works
- [ ] Remove line works
- [ ] Calculations are correct
- [ ] F12 lookup works

#### 14.3 Workflow Actions
- [ ] Submit works (DRAFT → SUBMITTED)
- [ ] Approve works (SUBMITTED → APPROVED)
- [ ] Cancel works
- [ ] Status updates correctly
- [ ] Disabled actions work

#### 14.4 Lookups
- [ ] Product lookup opens
- [ ] Product selection populates line
- [ ] Supplier lookup opens
- [ ] Supplier selection populates header

#### 14.5 Validation
- [ ] Required fields validated
- [ ] Line items validated
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
- [ ] Line items grid complete
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
- `backend/apps/retail/backend/procurement/models.py`
- `backend/apps/retail/backend/procurement/serializers.py`
- `backend/apps/retail/backend/procurement/views.py`

**Frontend**:
- `frontend/apps/retail/procurement/pages/PurchaseOrderFormPage.tsx` (564 lines)
- `frontend/apps/retail/procurement/procurement.service.ts`
- `frontend/apps/retail/procurement/procurement.types.ts`

**Components**:
- `frontend/src/ui/components/TransactionToolbar.tsx`
- `frontend/src/ui/components/ProductLookupModal.tsx`
- `frontend/src/ui/components/SupplierLookupModal.tsx`

**Standards**:
- `.steering/14_UI_CANON/04_Frontend_UI_Canon.md`
- `.steering/14_UI_CANON/TXN-M.md`
- `.steering/governance.md`

---

**Last Updated**: 2026-01-07  
**Maintainer**: Astra (ERP Platform Development Owner)
