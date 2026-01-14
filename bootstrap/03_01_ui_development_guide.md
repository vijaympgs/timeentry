# 🚀 NEW UI DEVELOPMENT GUIDE - COMPREHENSIVE REFERENCE

**Purpose**: Complete UI development guidelines for HRM, CRM, and FMS modules  
**Target Audience**: Agent E and development team building enterprise modules  
**Date**: 2026-01-08  
**Context**: Consolidated reference from all wiring specifications for seamless integration

---

## 📋 TABLE OF CONTENTS

1. [Quick Decision Tree](#quick-decision-tree)
2. [Mandatory Reading Order](#mandatory-reading-order)
3. [Typography & Styling Standards](#typography--styling-standards)
4. [Master Data Implementation](#master-data-implementation)
5. [Transaction Form Implementation](#transaction-form-implementation)
6. [Workflow & Business Rules](#workflow--business-rules)
7. [UI Standards Compliance](#ui-standards-compliance)
8. [Quick Reference Patterns](#quick-reference-patterns)
9. [Integration Checklist](#integration-checklist)
10. [Common Pitfalls to Avoid](#common-pitfalls-to-avoid)

---

## 🎯 QUICK DECISION TREE

```
Need to understand UI standards? → Go to: Typography & Styling Standards
Need to implement master data list? → Go to: Master Data Implementation
Need to implement transaction form? → Go to: Transaction Form Implementation
Need workflow actions? → Go to: Workflow & Business Rules
Need copy-paste patterns? → Go to: Quick Reference Patterns
```

---

## 📚 MANDATORY READING ORDER

### **Step 1: Foundation Standards**
1. **Typography & Styling Standards** (this document) - UI bible with exact specs
2. **UI Canon Templates** - Functional patterns and governance rules

### **Step 2: Implementation Guides**
3. **Master Data Implementation** - For Employee, Department, Position, Contact, Account
4. **Transaction Form Implementation** - For Leave Request, Lead, Opportunity, Invoice
5. **Workflow & Business Rules** - For status machines and approval flows

---

## 🎨 TYPOGRAPHY & STYLING STANDARDS

### **Typography Levels (Non-Negotiable)**

#### **L1 - Page Titles**
```html
<h1 className="text-xl font-semibold text-[#201f1e]">Page Title</h1>
```
- Font Size: 20px / text-xl
- Font Weight: 600 / font-semibold
- Color: #201f1e (dark gray)

#### **L2 - Section Headers**
```html
<h2 className="text-base font-semibold text-[#323130]">Section Header</h2>
```
- Font Size: 16px / text-base
- Font Weight: 600 / font-semibold
- Color: #323130 (medium gray)

#### **L3 - Field Labels**
```html
<label className="text-xs font-semibold text-[#605e5c] uppercase">Field Label *</label>
```
- Font Size: 12px / text-xs
- Font Weight: 600 / font-semibold
- Color: #605e5c (gray)
- Text Transform: uppercase

#### **L4 - Body Text**
```html
<p className="text-sm text-[#323130]">Body text content</p>
```
- Font Size: 14px / text-sm
- Font Weight: 400 / font-normal
- Color: #323130 (medium gray)

### **Form Elements (Exact Specifications)**

#### **Text Input (Standard)**
```html
<input type="text" 
       className="w-full px-3 py-2 border border-gray-300 rounded-sm text-sm 
              focus:border-[#0078d4] focus:ring-1 focus:ring-[#0078d4] outline-none" />
```

#### **Text Input (Underline Style for Lookups)**
```html
<div className="flex items-center gap-2 border-b border-[#8a8886] hover:border-[#323130] pb-1">
  <Building2 size={14} className="text-[#0078d4]" />
  <input type="text" 
         className="w-full outline-none bg-transparent font-medium text-[#0078d4] cursor-pointer" />
</div>
```

#### **Select Dropdown (LOV)**
```html
<select className="w-full px-3 py-2 border border-gray-300 rounded-sm text-sm 
                focus:border-[#0078d4] outline-none">
  <option>Select...</option>
</select>
```

#### **Checkbox**
```html
<label className="flex items-center gap-2">
  <input type="checkbox" 
         className="w-4 h-4 text-[#0078d4] border-gray-300 rounded focus:ring-[#0078d4]" />
  <span className="text-sm text-[#323130]">Active</span>
</label>
```

#### **Radio Button**
```html
<label className="flex items-center gap-2">
  <input type="radio" 
         className="w-4 h-4 text-[#0078d4] border-gray-300 focus:ring-[#0078d4]" />
  <span className="text-sm text-[#323130]">Option</span>
</label>
```

### **Buttons (Standard Styles)**

#### **Primary Button**
```html
<button style={{ backgroundColor: 'var(--button-primary-bg)', color: 'var(--button-primary-text)' }} 
        className="px-3 py-1.5 font-medium rounded-sm">
  Save
</button>
```
- Background: #ff6600 (orange) via CSS variable
- Text Color: #ffffff (white)
- Font Size: 14px / text-sm
- Font Weight: 500 / font-medium
- Padding: px-3 py-1.5 (12px x 6px)
- Border Radius: 2px / rounded-sm

#### **Secondary Button**
```html
<button className="px-3 py-1.5 hover:bg-[#edebe9] rounded-sm text-[#323130] font-medium">
  Cancel
</button>
```

#### **Icon Button**
```html
<button className="p-2 hover:bg-[#f3f2f1] rounded-full">
  <Edit3 size={16} className="text-[#605e5c]" />
</button>
```

### **Status Badges**

#### **Standard Badge**
```html
<span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
  ACTIVE
</span>
```

#### **Status Color Mapping**
| Status | Background | Text |
|--------|------------|------|
| ACTIVE | bg-green-100 | text-green-800 |
| DRAFT | bg-gray-100 | text-gray-700 |
| SUBMITTED | bg-yellow-100 | text-yellow-700 |
| APPROVED | bg-blue-100 | text-blue-700 |
| COMPLETED | bg-green-100 | text-green-800 |
| CANCELLED | bg-red-100 | text-red-800 |
| INACTIVE | bg-gray-100 | text-gray-800 |

### **Color Palette (Exact Hex Codes)**

```css
/* Primary Colors */
--primary-blue: #0078d4;    /* Links, focus states, icons */
--primary-orange: #ff6600;  /* Primary buttons */

/* Text Colors */
--text-dark: #201f1e;      /* Page titles, headings */
--text-medium: #323130;    /* Body text, labels */
--text-gray: #605e5c;      /* Secondary text, field labels */
--text-light: #a19f9d;     /* Placeholder, disabled text */

/* Background Colors */
--bg-white: #ffffff;       /* Cards, modals, tables */
--bg-light: #faf9f8;       /* Page background */
--bg-gray: #f3f2f1;        /* Table headers, hover states */
--bg-blue-light: #f3f9ff;   /* Row hover (blue tint) */

/* Border Colors */
--border-light: #edebe9;    /* Card borders, dividers */
--border-medium: #d1d1d1;   /* Input borders */
--border-dark: #8a8886;     /* Underline inputs */
--border-focus: #0078d4;     /* Focus state */
```

---

## 📋 MASTER DATA IMPLEMENTATION

### **When to Use**
- Employee Master, Department, Position, Contact, Account
- Product Catalog, Service Catalog
- Any list-based CRUD operations

### **Reference Implementations**
- `frontend/src/pages/CustomerSetup.tsx` (243 lines)
- `frontend/apps/retail/inventory/pages/UOMSetup.tsx` (251 lines)

### **Complete Implementation Phases**

#### **Phase 1: Backend Setup**
1. **Model Verification**
   - Model exists with `company` foreign key
   - Has `is_active` or `status` field
   - Proper `__str__` method
   - Meta class with `ordering`

2. **Serializer Creation**
   ```python
   class CustomerSerializer(serializers.ModelSerializer):
       company_name = serializers.CharField(source='company.name', read_only=True)
       
       class Meta:
           model = Customer
           fields = '__all__'
           read_only_fields = ['id', 'created_at', 'updated_at']
   ```

3. **ViewSet Creation**
   ```python
   class CustomerViewSet(viewsets.ModelViewSet):
       serializer_class = CustomerSerializer
       filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
       filterset_fields = ['company', 'customer_type', 'status']
       search_fields = ['customer_code', 'customer_name', 'phone', 'email']
       ordering_fields = ['customer_code', 'customer_name', 'created_at']
       ordering = ['-created_at']
       
       def get_queryset(self):
           return Customer.objects.filter(company=self.request.user.company)
   ```

4. **URL Registration**
   ```python
   router.register(r'customers', CustomerViewSet, basename='customer')
   ```

#### **Phase 2: Frontend Service Layer**
1. **TypeScript Types**
   ```typescript
   export interface CustomerListItem {
     id: string;
     company: string;
     company_name?: string;
     customer_code: string;
     customer_name: string;
     customer_type: 'INDIVIDUAL' | 'BUSINESS';
     status: 'ACTIVE' | 'INACTIVE' | 'BLACKLISTED';
     created_at: string;
   }
   
   export interface CustomerFilters {
     company_id?: string;
     customer_type?: string;
     status?: string;
     search?: string;
   }
   ```

2. **Service Methods**
   ```typescript
   export const customerService = {
     getCustomers: async (filters?: CustomerFilters) => {
       const params = new URLSearchParams();
       if (filters?.company_id) params.append('company', filters.company_id);
       if (filters?.search) params.append('search', filters.search);
       const response = await apiClient.get(`/company/customers/?${params}`);
       return response.data;
     },
     createCustomer: async (data: Partial<CustomerListItem>) => {
       const response = await apiClient.post('/company/customers/', data);
       return response.data;
     },
     // ... other CRUD methods
   };
   ```

#### **Phase 3: UI Component Structure**
1. **Page Header**
   ```html
   <div className="page-container space-y-6">
     <div className="flex items-center justify-between">
       <div className="flex items-center space-x-3">
         <Users className="w-8 h-8 text-purple-600" />
         <div>
           <h1 className="erp-page-title">Customers</h1>
           <p className="erp-page-subtitle">Manage customer master data</p>
         </div>
       </div>
       <button onClick={handleCreate} className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700">
         <Plus className="w-4 h-4 mr-2" />
         Add Customer
       </button>
     </div>
   </div>
   ```

2. **Filter Bar**
   ```html
   <div className="bg-white p-4 shadow-sm border border-gray-200">
     <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
       <div className="md:col-span-2">
         <div className="relative">
           <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
           <input type="text" placeholder="Search by code, name, phone, email..."
                  className="pl-10 pr-4 py-2 w-full border border-gray-300 focus:ring-purple-500 focus:border-purple-500" />
         </div>
       </div>
       <!-- Company, Type, Status filters -->
     </div>
   </div>
   ```

3. **Data Table**
   ```html
   <div className="bg-white shadow-lg border border-gray-200 overflow-hidden">
     <table className="min-w-full divide-y divide-gray-200">
       <thead className="bg-gradient-to-r from-gray-50 to-gray-100">
         <tr>
           <th className="px-6 py-4 text-left erp-table-header text-gray-600">Company</th>
           <th className="px-6 py-4 text-left erp-table-header text-gray-600">Code</th>
           <th className="px-6 py-4 text-left erp-table-header text-gray-600">Name</th>
           <th className="px-6 py-4 text-right erp-table-header text-gray-600">Actions</th>
         </tr>
       </thead>
       <tbody className="bg-white divide-y divide-gray-200">
         {customers.map(customer => (
           <tr key={customer.id} className="hover:bg-purple-50 transition-colors duration-200">
             <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
               {customer.company_name || customer.company}
             </td>
             <td className="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-900">
               {customer.customer_code}
             </td>
             <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
               {customer.customer_name}
             </td>
             <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
               <div className="flex items-center justify-end space-x-2">
                 <button onClick={() => handleEdit(customer.id)} 
                         className="text-purple-600 hover:text-purple-900 p-1 rounded">
                   <Edit3 className="w-4 h-4" />
                 </button>
               </div>
             </td>
           </tr>
         ))}
       </tbody>
     </table>
   </div>
   ```

---

## 📝 TRANSACTION FORM IMPLEMENTATION

### **When to Use**
- Leave Request, Attendance Adjustment, Expense Claim
- Lead, Opportunity, Quote, Invoice
- Purchase Order, Sales Order, Goods Receipt

### **Reference Implementation**
- `frontend/apps/retail/procurement/pages/PurchaseOrderFormPage.tsx` (564 lines)

### **Complete Implementation Phases**

#### **Phase 1: Backend Setup**
1. **Header Model with Status Choices**
   ```python
   class PurchaseOrder(models.Model):
       STATUS_CHOICES = [
           ('DRAFT', 'Draft'),
           ('SUBMITTED', 'Submitted'),
           ('APPROVED', 'Approved'),
           ('CONFIRMED', 'Confirmed'),
           ('CLOSED', 'Closed'),
           ('CANCELLED', 'Cancelled'),
       ]
       status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
   ```

2. **Nested Serializer with Lines**
   ```python
   class PurchaseOrderLineSerializer(serializers.ModelSerializer):
       item_name = serializers.CharField(source='item.item_name', read_only=True)
       uom_name = serializers.CharField(source='uom.uom_code', read_only=True)
       
       class Meta:
           model = PurchaseOrderLine
           fields = '__all__'
           read_only_fields = ['line_id', 'purchase_order']
   
   class PurchaseOrderSerializer(serializers.ModelSerializer):
       lines = PurchaseOrderLineSerializer(many=True, read_only=True)
       supplier_name = serializers.CharField(source='supplier.supplier_name', read_only=True)
       
       def create(self, validated_data):
           validated_data['po_number'] = f"PO-{timezone.now().strftime('%Y%m%d%H%M%S')}"
           return super().create(validated_data)
   ```

3. **ViewSet with Workflow Actions**
   ```python
   class PurchaseOrderViewSet(viewsets.ModelViewSet):
       @action(detail=True, methods=['post'])
       def submit(self, request, pk=None):
           po = self.get_object()
           if po.status != 'DRAFT':
               return Response({'error': 'Only DRAFT POs can be submitted'}, status=400)
           po.status = 'SUBMITTED'
           po.submitted_by = request.user
           po.submitted_at = timezone.now()
           po.save()
           return Response(self.get_serializer(po).data)
   ```

#### **Phase 2: Frontend Service Layer**
1. **TypeScript Types with Status Union**
   ```typescript
   export type POStatus = 'DRAFT' | 'SUBMITTED' | 'APPROVED' | 'CONFIRMED' | 'CLOSED' | 'CANCELLED';
   
   export interface PurchaseOrderLine {
     id?: string;
     line_number: number;
     item_id?: string;
     item_code?: string;
     item_name?: string;
     ordered_qty: number;
     unit_price: number;
     line_total: number;
   }
   
   export interface PurchaseOrder {
     id?: string;
     po_number: string;
     status: POStatus;
     lines?: PurchaseOrderLine[];
     subtotal?: number;
     grand_total?: number;
   }
   ```

2. **Service with Workflow Methods**
   ```typescript
   export const procurementService = {
     submitPurchaseOrder: async (id: string) => {
       const response = await apiClient.post(`/procurement/purchase-orders/${id}/submit/`);
       return response.data;
     },
     approvePurchaseOrder: async (id: string) => {
       const response = await apiClient.post(`/procurement/purchase-orders/${id}/approve/`);
       return response.data;
     },
     // ... other CRUD and workflow methods
   };
   ```

#### **Phase 3: Component Structure**
1. **TransactionToolbar Integration**
   ```html
   <TransactionToolbar 
     status={header.status.toUpperCase() as TransactionStatus}
     onAction={handleToolbarAction}
     disabledActions={getDisabledActions(header.status)} />
   ```

2. **Header Section**
   ```html
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

3. **Line Items Grid**
   ```html
   <div className="bg-white border border-[#edebe9] shadow-sm rounded-sm p-6 mb-6">
     <div className="flex items-center justify-between mb-4">
       <button className="text-[#0078d4] font-semibold border-b-2 border-[#0078d4] pb-1 text-sm uppercase">
         Line Items
       </button>
       <button onClick={addLine} className="flex items-center gap-1 text-xs font-bold uppercase text-[#0078d4] hover:underline">
         <Plus size={14} />
         Add Line
       </button>
     </div>
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
               <input type="text" value={line.item_code} 
                      onChange={e => updateLine(index, 'item_code', e.target.value)}
                      onKeyDown={(e) => handleKeyDown(e, index, 'item_code')}
                      className="w-full p-3 outline-none bg-transparent focus:bg-white" />
             </td>
             <td className="p-0 border-l border-[#edebe9]">
               <input type="text" value={line.item_name} 
                      onChange={e => updateLine(index, 'item_name', e.target.value)}
                      className="w-full p-3 outline-none bg-transparent focus:bg-white" />
             </td>
             <td className="p-0 border-l border-[#edebe9]">
               <input type="number" value={line.ordered_qty} 
                      onChange={e => updateLine(index, 'ordered_qty', parseFloat(e.target.value))}
                      className="w-full p-3 outline-none bg-transparent text-right focus:bg-white" />
             </td>
             <td className="p-0 border-l border-[#edebe9]">
               <input type="text" value={line.uom || ''} readOnly 
                      className="w-full p-3 outline-none bg-gray-50 text-center text-gray-600" />
             </td>
             <td className="p-0 border-l border-[#edebe9]">
               <input type="number" value={line.unit_price} 
                      onChange={e => updateLine(index, 'unit_price', parseFloat(e.target.value))}
                      className="w-full p-3 outline-none bg-transparent text-right focus:bg-white" />
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
   ```

---

## ⚙️ WORKFLOW & BUSINESS RULES

### **Status State Machine Definition**
```typescript
export type POStatus = 'DRAFT' | 'SUBMITTED' | 'APPROVED' | 'CONFIRMED' | 'CLOSED' | 'CANCELLED';

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
    next: 'CONFIRMED',
    label: 'Approved',
    color: 'text-blue-600',
    bgColor: 'bg-blue-100',
    description: 'Approved by manager'
  },
  // ... other statuses
};
```

### **Backend Workflow Actions**
```python
@action(detail=True, methods=['post'])
def submit(self, request, pk=None):
    """Submit PO for approval"""
    po = self.get_object()
    if po.status != 'DRAFT':
        return Response({'error': 'Only DRAFT POs can be submitted'}, status=400)
    
    po.status = 'SUBMITTED'
    po.submitted_by = request.user
    po.submitted_at = timezone.now()
    po.save()
    
    serializer = self.get_serializer(po)
    return Response(serializer.data)

@action(detail=True, methods=['post'])
def approve(self, request, pk=None):
    """Approve PO"""
    po = self.get_object()
    if po.status != 'SUBMITTED':
        return Response({'error': 'Only SUBMITTED POs can be approved'}, status=400)
    
    # Business logic (e.g., reserve inventory)
    # ...
    
    po.status = 'APPROVED'
    po.approved_by = request.user
    po.approved_at = timezone.now()
    po.save()
    
    serializer = self.get_serializer(po)
    return Response(serializer.data)
```

### **Frontend Workflow Handlers**
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

const getDisabledActions = (status: POStatus): string[] => {
  if (saving) return ['save', 'submit', 'approve', 'cancel'];
  
  switch (status) {
    case 'DRAFT': return ['approve'];
    case 'SUBMITTED': return ['save', 'submit'];
    case 'APPROVED':
    case 'CONFIRMED':
    case 'CLOSED': return ['save', 'submit', 'approve', 'cancel'];
    default: return [];
  }
};
```

---

## ✅ UI STANDARDS COMPLIANCE

### **Layout Standards**
- Use flex column layout with `h-full`
- Background color `bg-[#faf9f8]`
- Toolbar at top (sticky)
- Scrollable content area

### **Spacing Standards**
- Page container uses `space-y-6`
- Consistent padding: `px-3 py-1.5` for buttons, `px-3 py-2` for inputs
- Proper gap in grids: `gap-4`
- Table padding: `p-3` (12px all sides)

### **Border Standards**
- Border radius always `rounded-sm` (2px) except badges (`rounded-full`)
- Focus states always use `#0078d4` (blue)
- Hover states for secondary elements use `#edebe9` (light gray)

### **Icon Standards**
- Icon sizes typically 14px or 16px
- Use Lucide React icons consistently
- Color coding: `#0078d4` for primary, `#605e5c` for secondary

---

## 🚀 QUICK REFERENCE PATTERNS

### **Common Page Header**
```html
<div className="px-6 py-3 border-b border-[#edebe9] bg-white">
  <h1 className="text-xl font-semibold text-[#201f1e]">Page Title</h1>
</div>
```

### **Form Field Group**
```html
<div className="space-y-1">
  <label className="text-xs font-semibold text-[#605e5c] uppercase">Field Label *</label>
  <input type="text" 
         className="w-full px-3 py-2 border border-gray-300 rounded-sm text-sm 
                focus:border-[#0078d4] focus:ring-1 focus:ring-[#0078d4] outline-none" />
</div>
```

### **Action Button Group**
```html
<div className="flex items-center gap-2">
  <button className="px-3 py-1.5 bg-[#ff6600] text-white font-medium rounded-sm">Save</button>
  <button className="px-3 py-1.5 hover:bg-[#edebe9] rounded-sm text-[#323130] font-medium">Cancel</button>
</div>
```

### **Status Badge**
```html
<span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">ACTIVE</span>
```

---

## 📋 INTEGRATION CHECKLIST

### **Before You Start Coding**
- [ ] Read Typography & Styling Standards (this document)
- [ ] Read the appropriate wiring checklist (master/transaction)
- [ ] Identify the template type (MST-S/M/C or TXN-S/M/C)
- [ ] Find the reference implementation in Retail module
- [ ] Copy the reference file to your HRM/CRM folder
- [ ] Rename and adapt for your feature

### **While Coding**
- [ ] Use exact font sizes from typography reference
- [ ] Use exact colors from color palette
- [ ] Use `var(--button-primary-bg)` for primary buttons
- [ ] Use `rounded-sm` (2px) for all borders except badges
- [ ] Use `focus:border-[#0078d4]` for all inputs
- [ ] Use `hover:bg-[#edebe9]` for secondary buttons
- [ ] Follow the wiring checklist phase by phase

### **Before Committing**
- [ ] All font sizes match typography reference
- [ ] All colors match color palette
- [ ] All buttons use standard styling
- [ ] All form elements use standard styling
- [ ] All tables use standard styling
- [ ] All status badges use standard colors
- [ ] Code follows wiring checklist
- [ ] Tested in browser

---

## 🚫 COMMON PITFALLS TO AVOID

### **❌ DO NOT Create Custom Toolbars**
- Don't create your own toolbar component
- Don't use different button styles in toolbars
- Don't change keyboard shortcuts (F1-F12)
- ✅ **INSTEAD**: Use `TransactionToolbar` component for transaction forms

### **❌ DO NOT Use Different Colors**
- Don't use purple, indigo, pink for primary actions
- Don't use different shades of blue
- Don't create custom color schemes
- ✅ **INSTEAD**: Primary buttons: #ff6600 (orange), Links/Focus: #0078d4 (blue)

### **❌ DO NOT Use Different Font Sizes**
- Don't use text-lg, text-2xl, text-3xl for page titles
- Don't use text-base for labels
- Don't use custom font weights
- ✅ **INSTEAD**: Page titles: text-xl (20px), Labels: text-xs (12px), Body: text-sm (14px)

### **❌ DO NOT Skip Wiring Checklists**
- Don't jump straight to UI without backend setup
- Don't skip service layer
- Don't skip validation
- Don't skip testing
- ✅ **INSTEAD**: Follow all phases for master data (11 phases) and transactions (14 phases)

---

## 🎯 MODULE-SPECIFIC GUIDANCE

### **HRM Features**
| Feature | Template | Reference |
|---------|----------|----------|
| Employee Master | MST-M (Medium) | CustomerSetup.tsx |
| Department | MST-S (Simple) | UOMSetup.tsx |
| Position | MST-S (Simple) | UOMSetup.tsx |
| Leave Request | TXN-M (Medium) | PurchaseOrderFormPage.tsx |
| Attendance Adjustment | TXN-S (Simple) | Custom implementation |
| Expense Claim | TXN-M (Medium) | PurchaseOrderFormPage.tsx |
| Performance Review | TXN-C (Complex) | Custom implementation |

### **CRM Features**
| Feature | Template | Reference |
|---------|----------|----------|
| Contact | MST-M (Medium) | CustomerSetup.tsx |
| Account | MST-C (Complex) | Custom implementation |
| Product Catalog | MST-M (Medium) | CustomerSetup.tsx |
| Lead | TXN-M (Medium) | PurchaseOrderFormPage.tsx |
| Opportunity | TXN-C (Complex) | Custom implementation |
| Campaign | TXN-M (Medium) | PurchaseOrderFormPage.tsx |
| Quote | TXN-M (Medium) | PurchaseOrderFormPage.tsx |

---

## 📞 WHEN YOU NEED HELP

### **Questions to Ask**
- "Which template should I use for [feature]?" → Check template mapping
- "What color should I use for [element]?" → Check color palette
- "How do I implement [workflow]?" → Check workflow section
- "What's the reference for [feature type]?" → Check implementation guides

### **Red Flags (Ask Before Proceeding)**
- ⚠️ "I'm creating a custom toolbar" → STOP, ask first
- ⚠️ "I'm using a different color scheme" → STOP, ask first
- ⚠️ "I'm skipping the service layer" → STOP, ask first
- ⚠️ "I'm not following the wiring checklist" → STOP, ask first

---

## ✅ SUCCESS CRITERIA

Your HRM/CRM modules are ready for integration when:

### **Visual Consistency**
- ✅ All UIs look identical to Retail module (same fonts, colors, spacing)
- ✅ All typography levels match standards exactly
- ✅ All color codes match palette exactly
- ✅ All button styles follow standards

### **Functional Completeness**
- ✅ All wiring checklists followed completely
- ✅ All reference implementations adapted correctly
- ✅ All code follows enterprise shell patterns
- ✅ All features tested and working

### **Integration Readiness**
- ✅ No custom toolbars, colors, or fonts
- ✅ Ready to copy into olivine-erp-platform/
- ✅ All imports use path aliases (@services, @ui, @auth)
- ✅ All routes registered in router.tsx

---

## 📚 FINAL REMINDERS

1. **Read Typography & Styling Standards FIRST** - This is your bible
2. **Follow wiring checklists EXACTLY** - Don't skip phases
3. **Copy reference implementations** - Don't reinvent the wheel
4. **Use exact colors and fonts** - No variations allowed
5. **No custom toolbars** - Use standard components
6. **Test before copying** - Ensure everything works
7. **Ask when unsure** - Better to ask than to redo

---

**Welcome to the team! 🚀**

Your mission: Build HRM and CRM modules that seamlessly integrate into the Olivine ERP Platform with zero visual or functional inconsistencies.

---

**Last Updated**: 2026-01-08  
**Maintained By**: Development Team  
**For**: Agent E and UI Development Team
