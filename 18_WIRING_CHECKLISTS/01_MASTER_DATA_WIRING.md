# Master Data List Page - Wiring Checklist

**For**: Employee, Department, Account, Contact, Category, Brand (Master Data)

**Reference Implementations**:
- ✅ `frontend/src/pages/SetupPage.tsx` (Standard Pattern)
- ✅ `frontend/apps/shared/pages/MasterDataLanding.tsx`

**Pattern**: List page with search/filter, MasterToolbar, modal for create/edit

---

## 📋 COMPLETE WIRING CHECKLIST

### **PHASE 1: Backend Setup**

#### 1.1 Model Verification
- [ ] Model exists in `backend/domain/company/models.py`
- [ ] Model has `company` foreign key field
- [ ] Model has `is_active` or `status` field
- [ ] Model has proper `__str__` method
- [ ] Model has `Meta` class with `ordering`

#### 1.2 Serializer Creation
- [ ] Serializer created in `backend/domain/company/serializers.py`
- [ ] Includes `company_name` read-only field (from `company.name`)
- [ ] Includes all necessary fields
- [ ] Has proper `Meta.fields` definition
- [ ] Has `read_only_fields` for auto-generated fields

**Example**:
```python
class EntitySerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    
    class Meta:
        model = Entity
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
```

#### 1.3 ViewSet Creation
- [ ] ViewSet created in `backend/domain/company/views.py`
- [ ] Inherits from `viewsets.ModelViewSet`
- [ ] Has `serializer_class` defined
- [ ] Has `filter_backends` (DjangoFilterBackend, SearchFilter, OrderingFilter)
- [ ] Has `filterset_fields` defined
- [ ] Has `search_fields` defined
- [ ] Has `ordering_fields` defined
- [ ] Has `ordering` default defined

**Example**:
```python
class EntityViewSet(viewsets.ModelViewSet):
    serializer_class = EntitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['company', 'entity_type', 'status']
    search_fields = ['entity_code', 'entity_name', 'phone', 'email']
    ordering_fields = ['entity_code', 'entity_name', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Entity.objects.filter(company=self.request.user.company)
```

#### 1.4 Company Scoping
- [ ] `get_queryset()` filters by `company`
- [ ] Uses `self.request.user.company` for filtering
- [ ] Includes `.select_related('company')` for performance

#### 1.5 URL Registration
- [ ] ViewSet registered in `backend/domain/company/urls.py`
- [ ] Uses `DefaultRouter`
- [ ] Endpoint follows pattern: `/api/company/{resource}/`

**Example**:
```python
router.register(r'entities', EntityViewSet, basename='entity')
```

---

### **PHASE 2: Frontend Service Layer**

#### 2.1 TypeScript Types
- [ ] Interface created in `frontend/src/services/{module}Service.ts`
- [ ] Includes all backend fields
- [ ] Uses proper TypeScript types (string, number, boolean, Date)
- [ ] Includes `company_name?: string` for display

**Example**:
```typescript
export interface EntityListItem {
  id: string;
  company: string;
  company_name?: string;
  entity_code: string;
  entity_name: string;
  entity_type: 'TYPE_A' | 'TYPE_B';
  phone?: string;
  email?: string;
  status: 'ACTIVE' | 'INACTIVE' | 'ARCHIVED';
  created_at: string;
  updated_at: string;
}

export interface EntityFilters {
  company_id?: string;
  entity_type?: string;
  status?: string;
  search?: string;
}
```

#### 2.2 Service Methods
- [ ] Service object created (e.g., `customerService`)
- [ ] `getAll()` method with filters parameter
- [ ] `getById(id)` method
- [ ] `create(data)` method
- [ ] `update(id, data)` method
- [ ] `delete(id)` method
- [ ] All methods use `apiClient` from `@services/apiClient`

**Example**:
```typescript
export const entityService = {
  getEntities: async (filters?: EntityFilters) => {
    const params = new URLSearchParams();
    if (filters?.company_id) params.append('company', filters.company_id);
    if (filters?.entity_type) params.append('entity_type', filters.entity_type);
    if (filters?.status) params.append('status', filters.status);
    if (filters?.search) params.append('search', filters.search);
    
    const response = await apiClient.get(`/company/entities/?${params}`);
    return response.data;
  },
  
  getEntity: async (id: string) => {
    const response = await apiClient.get(`/company/entities/${id}/`);
    return response.data;
  },
  
  createEntity: async (data: Partial<EntityListItem>) => {
    const response = await apiClient.post('/company/entities/', data);
    return response.data;
  },
  
  updateEntity: async (id: string, data: Partial<EntityListItem>) => {
    const response = await apiClient.put(`/company/entities/${id}/`, data);
    return response.data;
  },
  
  deleteEntity: async (id: string) => {
    await apiClient.delete(`/company/entities/${id}/`);
  },
};
```

---

### **PHASE 3: UI Component Structure**

#### 3.1 Page Component Setup
- [ ] Component created in `frontend/src/pages/{EntityName}Setup.tsx` or `frontend/apps/{module}/pages/`
- [ ] Imports all necessary dependencies
- [ ] Uses TypeScript with proper typing

**Required Imports**:
```typescript
import React, { useEffect, useState } from "react";
import { Plus, Search, Edit3, Trash2, {Icon} } from "lucide-react";
import { companyService, CompanyListItem } from "@services/companyService";
import { {entity}Service, {Entity}Filters, {Entity}ListItem } from "@services/{entity}Service";
import { {Entity}Modal } from "@core/ui-canon/frontend/components/{Entity}Modal";
```

#### 3.2 State Management
- [ ] `companies` state (CompanyListItem[])
- [ ] `data` state (EntityListItem[])
- [ ] `loading` state (boolean)
- [ ] `error` state (string | null)
- [ ] `filters` state (EntityFilters)
- [ ] `searchTerm` state (string)
- [ ] `showModal` state (boolean)
- [ ] `editingId` state (string | null)

**Example**:
```typescript
const [companies, setCompanies] = useState<CompanyListItem[]>([]);
const [entities, setEntities] = useState<EntityListItem[]>([]);
const [loading, setLoading] = useState(true);
const [error, setError] = useState<string | null>(null);
const [filters, setFilters] = useState<EntityFilters>({});
const [searchTerm, setSearchTerm] = useState('');
const [showModal, setShowModal] = useState(false);
const [editingId, setEditingId] = useState<string | null>(null);
```

#### 3.3 Lifecycle Hooks
- [ ] Load companies on mount
- [ ] Set default company filter
- [ ] Load data when filters change
- [ ] Handle search on Enter key

**Example**:
```typescript
useEffect(() => {
  (async () => {
    try {
      const activeCompanies = await companyService.getActiveCompanies();
      setCompanies(activeCompanies);
      if (activeCompanies.length > 0) {
        setFilters(prev => ({ ...prev, company_id: prev.company_id || activeCompanies[0].id }));
      }
    } catch {
      setError('Failed to load companies');
    }
  })();
}, []);

useEffect(() => {
  loadData();
}, [filters]);
```

#### 3.4 Data Loading Function
- [ ] `loadData()` function created
- [ ] Sets loading state
- [ ] Calls service method with filters
- [ ] Handles errors gracefully
- [ ] Clears error on success

**Example**:
```typescript
const loadData = async () => {
  try {
    setLoading(true);
    const resp = await entityService.getEntities({
      ...filters,
      search: searchTerm || undefined,
    });
    setEntities(resp?.results || []);
    setError(null);
  } catch (err) {
    setError('Failed to load records');
    console.error(err);
  } finally {
    setLoading(false);
  }
};
```
```

---

### **PHASE 4: UI Layout**

#### 4.1 Page Header
- [ ] Uses `page-container` class with `space-y-6`
- [ ] Icon from lucide-react (appropriate for entity)
- [ ] Title uses L1 typography (`erp-page-title` class)
- [ ] Subtitle uses L4 typography (`erp-page-subtitle` class)
- [ ] MasterToolbar integration (handles "New" and other actions)
**Example**:
```tsx
<div className="page-container space-y-6">
  <MasterToolbar 
    viewId="ENTITY_SETUP" 
    mode={getToolbarMode()} 
    onAction={handleToolbarAction} 
  />
  <div className="flex items-center justify-between">
    <div className="flex items-center space-x-3">
      <Users className="w-8 h-8 text-blue-600" />
      <div>
        <h1 className="erp-page-title">Employees</h1>
        <p className="erp-page-subtitle">Manage employee master data</p>
      </div>
    </div>
  </div>
</div>
```
#### 4.2 Filter Bar
- [ ] White background with shadow
- [ ] Grid layout (responsive)
- [ ] Search input with icon
- [ ] Company dropdown
- [ ] Type/category dropdown (if applicable)
- [ ] Status dropdown
- [ ] Enter key triggers search

**Example**:
```tsx
<div className="bg-white p-4 shadow-sm border border-gray-200">
  <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
    {/* Search */}
    <div className="md:col-span-2">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
        <input
          type="text"
          placeholder="Search items..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
          className="pl-10 pr-4 py-2 w-full border border-gray-300 focus:ring-blue-500 focus:border-blue-500"
        />
      </div>
    </div>

    {/* Company Filter */}
    <div>
      <select
        value={filters.company_id || ''}
        onChange={(e) => handleFilterChange('company_id', e.target.value)}
        className="w-full px-3 py-2 border border-gray-300 focus:ring-blue-500 focus:border-blue-500"
      >
        {companies.map(c => (
          <option key={c.id} value={c.id}>{c.company_name}</option>
        ))}
      </select>
    </div>

    {/* Type Filter */}
    <div>
      <select
        value={filters.entity_type || ''}
        onChange={(e) => handleFilterChange('entity_type', e.target.value)}
        className="w-full px-3 py-2 border border-gray-300 focus:ring-blue-500 focus:border-blue-500"
      >
        <option value="">All Types</option>
        <option value="TYPE_A">Type A</option>
        <option value="TYPE_B">Type B</option>
      </select>
    </div>

    {/* Status Filter */}
    <div>
      <select
        value={filters.status || ''}
        onChange={(e) => handleFilterChange('status', e.target.value)}
        className="w-full px-3 py-2 border border-gray-300 focus:ring-blue-500 focus:border-blue-500"
      >
        <option value="">Active Only</option>
        <option value="ACTIVE">Active</option>
        <option value="INACTIVE">Inactive</option>
      </select>
    </div>
  </div>
</div>
```

#### 4.3 Error Banner
- [ ] Conditional rendering based on error state
- [ ] Red background with border
- [ ] Dismissible (optional)

**Example**:
```tsx
{error && (
  <div className="bg-red-50 border border-red-200 rounded-md p-4">
    <div className="text-sm text-red-600">{error}</div>
  </div>
)}
```

#### 4.4 Data Table
- [ ] White background with shadow
- [ ] Gradient header (`bg-gradient-to-r from-gray-50 to-gray-100`)
- [ ] Table headers use `erp-table-header` class
- [ ] Hover effect on rows (`hover:bg-{color}-50`)
- [ ] Proper column widths
- [ ] Empty state message

**Example**:
```tsx
<div className="bg-white shadow-lg border border-gray-200 overflow-hidden">
  <div className="overflow-x-auto">
    <table className="min-w-full divide-y divide-gray-200">
      <thead className="bg-gradient-to-r from-gray-50 to-gray-100">
        <tr>
          <th className="px-6 py-4 text-left erp-table-header text-gray-600">Company</th>
          <th className="px-6 py-4 text-left erp-table-header text-gray-600">Code</th>
          <th className="px-6 py-4 text-left erp-table-header text-gray-600">Name</th>
          <th className="px-6 py-4 text-left erp-table-header text-gray-600">Type</th>
          <th className="px-6 py-4 text-left erp-table-header text-gray-600">Status</th>
          <th className="px-6 py-4 text-right erp-table-header text-gray-600">Actions</th>
        </tr>
      </thead>
      <tbody className="bg-white divide-y divide-gray-200">
        {entities.map(item => (
          <tr key={item.id} className="hover:bg-blue-50 transition-colors duration-200">
            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {item.company_name || item.company}
            </td>
            <td className="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-900">
              {item.entity_code}
            </td>
            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {item.entity_name}
            </td>
            <td className="px-6 py-4 whitespace-nowrap">
              {getTypeBadge(item.entity_type)}
            </td>
            <td className="px-6 py-4 whitespace-nowrap">
              {getStatusBadge(item.status)}
            </td>
            <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              {/* Actions handled via MasterToolbar + Row Selection */}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
</div>
```

---

### **PHASE 5: Action Handlers**

#### 5.1 Create Handler
- [ ] Sets `editingId` to null
- [ ] Opens modal

**Example**:
```typescript
const handleCreate = () => {
  setEditingId(null);
  setShowModal(true);
};
```

#### 5.2 Edit Handler
- [ ] Sets `editingId` to selected item ID
- [ ] Opens modal

**Example**:
```typescript
const handleEdit = (id: string) => {
  setEditingId(id);
  setShowModal(true);
};
```

#### 5.3 Delete Handler (Optional)
- [ ] Confirms deletion
- [ ] Calls service delete method
- [ ] Refreshes data on success
- [ ] Handles errors

**Example**:
```typescript
const handleDelete = async (item: EntityListItem) => {
  if (!confirm(`Delete ${item.entity_name}?`)) return;
  
  try {
    await entityService.deleteEntity(item.id);
    loadData();
  } catch (err: any) {
    setError(err?.response?.data?.error || 'Failed to delete');
  }
};
```

#### 5.4 Modal Close Handler
- [ ] Closes modal
- [ ] Clears `editingId`
- [ ] Refreshes data if `shouldRefresh` is true

**Example**:
```typescript
const handleModalClose = (shouldRefresh?: boolean) => {
  setShowModal(false);
  setEditingId(null);
  if (shouldRefresh) loadData();
};
```

#### 5.5 Filter Change Handler
- [ ] Updates filters object
- [ ] Clears value if empty

**Example**:
```typescript
const handleFilterChange = (key: keyof EntityFilters, value: any) => {
  setFilters({ ...filters, [key]: value || undefined });
};
```

#### 5.6 Search Handler
- [ ] Updates filters with search term
- [ ] Triggered on Enter key

**Example**:
```typescript
const handleSearch = () => {
  setFilters({ ...filters, search: searchTerm || undefined });
};
```

---

### **PHASE 6: Helper Functions**

#### 6.1 Status Badge Function
- [ ] Returns colored badge based on status
- [ ] Uses Tailwind classes
- [ ] Consistent color scheme

**Example**:
```typescript
const getStatusBadge = (status: string) => {
  const colors: Record<string, string> = {
    ACTIVE: 'bg-green-100 text-green-800',
    INACTIVE: 'bg-gray-100 text-gray-800',
    ARCHIVED: 'bg-red-100 text-red-800',
  };
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${colors[status] || 'bg-gray-100 text-gray-800'}`}>
      {status}
    </span>
  );
};
```

#### 6.2 Type Badge Function (If Applicable)
- [ ] Returns colored badge based on type
- [ ] Uses Tailwind classes

**Example**:
```typescript
const getTypeBadge = (type: string) => {
  const colors: Record<string, string> = {
    TYPE_A: 'bg-blue-100 text-blue-800',
    TYPE_B: 'bg-purple-100 text-purple-800',
  };
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${colors[type] || 'bg-gray-100 text-gray-800'}`}>
      {type}
    </span>
  );
};
```

---

### **PHASE 7: Modal Integration**

#### 7.1 Modal Component
- [ ] Modal component exists in `@core/ui-canon/frontend/components/`
- [ ] Uses BaseModal pattern
- [ ] Accepts `{entity}Id` and `onClose` props
- [ ] Handles create and edit modes
- [ ] Calls `onClose(true)` on successful save

#### 7.2 Modal Rendering
- [ ] Conditional rendering based on `showModal`
- [ ] Passes `editingId` as prop
- [ ] Passes `handleModalClose` as `onClose`

**Example**:
```tsx
{showModal && (
  <EntityModal entityId={editingId} onClose={handleModalClose} />
)}
```

---

### **PHASE 8: Loading States**

#### 8.1 Initial Loading
- [ ] Shows spinner while loading
- [ ] Centers spinner
- [ ] Only shows if data is empty

**Example**:
```tsx
if (loading && entities.length === 0) {
  return (
    <div className="flex items-center justify-center h-64">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>
  );
}
```
```

---

### **PHASE 9: UI Standards Compliance**

#### 9.1 Typography
- [ ] Page title uses L1 typography (or `erp-page-title`)
- [ ] Subtitle uses L4 typography (or `erp-page-subtitle`)
- [ ] Table headers use `erp-table-header` class
- [ ] No hardcoded font sizes

#### 9.2 Colors
- [ ] No hardcoded colors (use Tailwind classes or CSS variables)
- [ ] Primary button uses appropriate color (purple, blue, etc.)
- [ ] Hover states use lighter shades
- [ ] Status badges use semantic colors

#### 9.3 Spacing
- [ ] Page container uses `space-y-6`
- [ ] Consistent padding (px-4, py-2, etc.)
- [ ] Proper gap in grids (gap-4)

#### 9.4 Responsiveness
- [ ] Filter grid is responsive (`grid-cols-1 md:grid-cols-5`)
- [ ] Table has horizontal scroll on small screens
- [ ] Mobile-friendly spacing

---

### **PHASE 10: Company Scoping**

#### 10.1 Backend Scoping
- [ ] ViewSet `get_queryset()` filters by company
- [ ] Uses `self.request.user.company`
- [ ] No cross-company data leakage

#### 10.2 Frontend Scoping
- [ ] Company filter defaults to user's company
- [ ] Service calls include company_id
- [ ] No hardcoded company IDs

---

### **PHASE 11: Testing**

#### 11.1 CRUD Operations
- [ ] Create new record via modal
- [ ] Edit existing record via modal
- [ ] Delete record (if applicable)
- [ ] All operations persist to database

#### 11.2 Search & Filter
- [ ] Search works correctly
- [ ] Company filter works
- [ ] Type filter works (if applicable)
- [ ] Status filter works
- [ ] Filters can be combined

#### 11.3 Company Scoping
- [ ] Only see data for selected company
- [ ] Cannot access other company's data
- [ ] Company filter defaults correctly

#### 11.4 Error Handling
- [ ] Network errors display error banner
- [ ] Validation errors display correctly
- [ ] Error messages are user-friendly

#### 11.5 Loading States
- [ ] Initial load shows spinner
- [ ] Refresh shows spinner
- [ ] No flickering

#### 11.6 UI Standards
- [ ] Typography matches standards
- [ ] Colors match standards
- [ ] Spacing is consistent
- [ ] Responsive on mobile

---

## ✅ COMPLETION CHECKLIST

- [ ] All backend items checked
- [ ] All frontend service items checked
- [ ] All UI component items checked
- [ ] All action handlers implemented
- [ ] All helper functions created
- [ ] Modal integration complete
- [ ] Loading states implemented
- [ ] UI standards compliance verified
- [ ] Company scoping verified
- [ ] All tests passed

---

## 📚 Reference Files

**Backend**:
- `backend/domain/company/models.py`
- `backend/domain/company/serializers.py`
- `backend/domain/company/views.py`
- `backend/domain/company/urls.py`

**Frontend**:
- `frontend/src/pages/SetupPage.tsx`
- `frontend/apps/shared/pages/MasterDataLanding.tsx`
- `frontend/src/services/entityService.ts`

**Standards**:
- `.steering/14_UI_CANON/04_Frontend_UI_Canon.md`
- `.steering/14_UI_CANON/MST-M.md`
- `.steering/governance.md`

---

**Last Updated**: 2026-01-07  
**Maintainer**: Astra (ERP Platform Development Owner)
