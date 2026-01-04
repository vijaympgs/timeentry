# 🚀 HRM Development Guide

## 📋 Overview

This comprehensive development guide provides complete guidance for HRM module development, integrating stability practices, implementation processes, quality assurance, and UI component standards.

---

## 🎯 **Table of Contents**

1. [Development Stability & Emergency Recovery](#development-stability--emergency-recovery)
2. [Implementation Process](#implementation-process)
3. [Comprehensive Development Checklist](#comprehensive-development-checklist)
4. [UI Component Library](#ui-component-library)
5. [Workflow Integration](#workflow-integration)

---

## 🚨 Development Stability & Emergency Recovery

### **Emergency Recovery Instructions**

If context is lost, auto-retry occurs, or content gets cut off during development:

1. **STOP IMMEDIATELY** - Do not continue or regenerate from beginning
2. **USE THIS RECOVERY PROMPT:**
```
EMERGENCY: Context lost during [TASK_DESCRIPTION]
Current status: Working on [MODULE_NAME] ([COMPONENT])
Last completed section: [LAST_COMPLETED_SECTION]
Next section to implement: [NEXT_SECTION]

RECOVERY ACTIONS:
1. Read existing files for current context
2. Review .hrm.cline/01_governance.md
3. Continue from exact stopping point
4. Implement ONLY the next component/section
5. Test before proceeding further
6. WAIT for confirmation before continuing
```

### **Content Length Management**
- **Maximum 120 lines per response** to prevent cutoffs
- **Implement one component at a time** - never multiple components
- **Use clear section markers** after each major component
- **If component exceeds 120 lines**, split into logical sub-components
- **Focus on single responsibility principle** per response

### **Context Preservation Rules**
- **NEVER auto-retry** or restart from beginning
- **NEVER regenerate completed components**
- **ALWAYS continue from exact stopping point**
- **MAINTAIN state** across multiple responses
- **VERIFY existing code** before adding new content
- **TEST incrementally** after each major change

### **Development Completion Checklist**
Before implementing each component, verify:
- [ ] Existing code has been reviewed and understood
- [ ] Current file state is analyzed
- [ ] Component follows .hrm.cline/01_governance.md rules
- [ ] Implementation sequence is logical
- [ ] 120-line limit will be respected
- [ ] Testing will be performed after implementation
- [ ] No auto-retry will occur

### **Error Recovery Protocol**
If you detect context loss or interruption:
1. **STOP coding immediately**
2. **Announce the issue**: "Context lost - using recovery protocol"
3. **Use the emergency recovery prompt**
4. **Wait for confirmation** before continuing

---

## 🏗️ Implementation Process

### **Single Line Prompt for HRM Development:**
```
Refer .hrm.cline/01_governance.md and implement [BBP_FILE_PATH] with UI following Olivine UI canon, ensure CRUD operations work correctly, and verify Django persistence
```

**Example:**
```
Refer .hrm.cline/01_governance.md and implement D:\platform\hrm\bbp\02.Employee Management\02.1 Employee Records.md with UI following Olivine UI canon, ensure CRUD operations work correctly, and verify Django persistence
```

### **Mandatory Pre-Development Checklist**

#### **Step 1: Governance Compliance (REQUIRED)**
Before any development, you MUST read and reference:
- **`.hrm.cline/01_governance.md`** - Core governance contract & domain ownership rules

#### **Step 2: BBP Analysis (For Existing BBP Modules)**
If implementing from existing BBP file:
- ✅ Read the BBP file completely to understand requirements
- ✅ Extract Django models from BBP specifications
- ✅ Note UI/UX requirements from BBP
- ✅ Review business rules and validation requirements
- ✅ Check API specifications and integration points

#### **Step 3: Domain Ownership Verification**
- ✅ Verify module belongs to correct domain (HRM/CRM/FMS)
- ✅ Check no cross-domain model references
- ✅ Ensure Company model uses lazy string reference: `'domain.Company'`
- ✅ Confirm NO Location references in HRM/CRM modules

#### **Step 4: Architecture Compliance**
- ✅ Follow folder structure per governance
- ✅ Ensure mergeability contract compliance
- ✅ Use shared components via `common/` only
- ✅ Maintain module isolation

---

## 🏗️ Step-by-Step Implementation

### **Step 5: Django Models & Persistence**

#### **Model Implementation Standards:**
```python
# Primary Model Structure
class [ModelName](models.Model):
    """Model description following domain ownership"""
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys (MANDATORY)
    company_id = models.UUIDField()  # Always include for multi-tenant
    created_by_user_id = models.UUIDField()
    
    # Core Fields (per requirements)
    [field_name] = models.[FieldType](max_length=[length], [options])
    
    # Audit Fields (MANDATORY)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = '[table_name]'
        verbose_name = '[Verbose Name]'
        verbose_name_plural = '[Verbose Name Plural]'
        indexes = [
            models.Index(fields=['field1', 'field2'], name='idx_[name]'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['field1', 'field2'], name='uk_[name]'),
        ]
```

#### **CRUD Operations Implementation:**
```python
# Views (per development stability guidelines)
class [ModelName]ViewSet(viewsets.ModelViewSet):
    """CRUD operations following governance standards"""
    
    queryset = [ModelName].objects.all()
    serializer_class = [ModelName]Serializer
    permission_classes = [IsAuthenticated]
    
    # Custom actions as needed
    @action(detail=False, methods=['get'])
    def custom_action(self, request):
        pass
```

#### **Database Migration:**
```bash
# Create and apply migrations (Windows environment)
# Navigate to hrm/backend/ directory where manage.py exists
cd hrm/backend
python manage.py makemigrations hrm
python manage.py migrate
```

### **Step 6: UI Construction & Olivine UI Canon**

#### **UI Framework Choice (per governance):**
**Option A: Olivine UI Canon (RECOMMENDED)**
- Follow `.hrm.cline/01_governance.md` UI Canon section
- Use nexus color tokens and typography
- Implement enterprise-first dense functional UI
- Apply Material Design 3.0 principles

#### **Olivine UI Canon Implementation:**
```tsx
// Component Structure Example
import React from 'react';
import { Button } from '@/components/ui/Button';
import { DataTable } from '@/components/ui/DataTable';

const [ComponentName] = () => {
  return (
    <div className="min-h-screen bg-nexus-gray-50">
      {/* Fixed Header */}
      <header className="fixed top-0 h-16 bg-white border-b border-nexus-gray-200">
        {/* Header content */}
      </header>
      
      {/* Sidebar Navigation */}
      <aside className="fixed left-0 top-16 w-64 bg-nexus-gray-100">
        {/* Navigation content */}
      </aside>
      
      {/* Main Content */}
      <main className="ml-64 mt-16 p-6">
        {/* Transaction Toolbar */}
        <div className="mb-6 flex justify-between items-center">
          <Button variant="primary">+ New</Button>
          <Button variant="secondary">Edit</Button>
          <Button variant="secondary">Delete</Button>
        </div>
        
        {/* Data Grid */}
        <DataTable 
          data={data}
          columns={columns}
          className="bg-white rounded-sm shadow-nexus-sm"
        />
      </main>
    </div>
  );
};
```

### **Step 7: CRUD Operations Implementation**

#### **Frontend CRUD Pattern:**
```tsx
// CRUD Operations Example
const [ComponentName] = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // CREATE
  const handleCreate = async (formData) => {
    try {
      setLoading(true);
      const response = await api.post('/api/[endpoint]/', formData);
      setData([...data, response.data]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // READ
  const fetchData = async () => {
    try {
      setLoading(true);
      const response = await api.get('/api/[endpoint]/');
      setData(response.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // UPDATE
  const handleUpdate = async (id, formData) => {
    try {
      setLoading(true);
      const response = await api.put(`/api/[endpoint}/${id}/`, formData);
      setData(data.map(item => item.id === id ? response.data : item));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // DELETE
  const handleDelete = async (id) => {
    try {
      setLoading(true);
      await api.delete(`/api/[endpoint}/${id}/`);
      setData(data.filter(item => item.id !== id));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    // Component JSX with CRUD operations
  );
};
```

### **Step 8: Testing & Quality Assurance**

#### **Unit Testing:**
```python
# Model Tests
class ModelNameTestCase(TestCase):
    def setUp(self):
        self.model = [ModelName].objects.create(
            field1='test_value',
            field2='test_value'
        )

    def test_model_creation(self):
        self.assertEqual(self.model.field1, 'test_value')

    def test_model_string_representation(self):
        self.assertEqual(str(self.model), '[ModelName] object (1)')

# View Tests
class [ModelName]ViewSetTestCase(APITestCase):
    def setUp(self):
        self.factory = [ModelName]Factory()
        self.client = APIClient()

    def test_list_endpoint(self):
        response = self.client.get('/api/[endpoint]/')
        self.assertEqual(response.status_code, 200)

    def test_create_endpoint(self):
        data = {'field1': 'test_value', 'field2': 'test_value'}
        response = self.client.post('/api/[endpoint]/', data)
        self.assertEqual(response.status_code, 201)
```

### **Step 9: Deployment Configuration**

#### **Production Settings:**
```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Security Settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

### **Step 10: Monitoring & Logging**

#### **Logging Configuration:**
```python
# logging.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process} {message}',
            'style': '{',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/django.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        '[app_name]': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

---

## 📋 Comprehensive Development Checklist

### **Section 1: UI Foundation & Olivine UI Canon Compliance**

#### **Typography & Visual Identity**
- [ ] **Font Implementation**: Use Inter font for UI/body text, JetBrains Mono for IDs/data
- [ ] **Font Sizes**: Apply text-sm for fields, text-xs for labels per governance
- [ ] **Color Tokens**: Implement nexus color palette consistently
  - [ ] nexus-primary-600 (#6d4de6) for primary actions/links
  - [ ] nexus-primary-700 (#5d3dcb) for hover states
  - [ ] nexus-gray-50 (#fafafa) for page backgrounds
  - [ ] nexus-gray-100 (#f5f5f5) for panel backgrounds
  - [ ] nexus-gray-900 (#212121) for heavy text
  - [ ] nexus-error-600 (#db2777) for validation errors
  - [ ] nexus-success-600 (#059669) for success states

#### **Layout Structure & Components**
- [ ] **App Header (A):** Implement top-fixed header (h-16) with branding and user info
- [ ] **Sidebar Navigation (B):** Create fixed left sidebar (w-64) with module menu
- [ ] **Primary Workspace (C):** Configure main content with proper margins (ml-64 mt-16)
- [ ] **Status Bar (D):** Add fixed status bar at bottom with system information
- [ ] **Transaction Toolbar:** Add fixed toolbar with Save/Cancel/Reset/Workflow actions
- [ ] **Shape System**: Apply rounded-none for inputs, rounded-sm for cards/buttons
- [ ] **Shadow System**: Use shadow-nexus-sm for cards, shadow-2xl for modals

#### **Responsive Design & Accessibility**
- [ ] **Mobile Compatibility:** Ensure responsive design for mobile/tablet
- [ ] **Accessibility Compliance**: Achieve WCAG 2.1 AA standards
- [ ] **Keyboard Navigation:** Implement proper tab order and keyboard shortcuts
- [ ] **Screen Reader Support:** Add ARIA labels and semantic HTML
- [ ] **Color Contrast:** Verify sufficient contrast ratios per guidelines

### **Section 2: CRUD Operations Functionality**

#### **Create Operations**
- [ ] **Form Implementation:** Build forms based on Django model fields
- [ ] **Client-Side Validation:** Add real-time form validation
- [ ] **Server-Side Validation:** Implement backend validation rules
- [ ] **Error Handling:** Display validation errors clearly
- [ ] **Success Feedback:** Show success messages/tokens after creation
- [ ] **Loading States:** Implement loading indicators during submission

#### **Read Operations**
- [ ] **Data Grid Implementation:** Create responsive data tables with sorting/filtering
- [ ] **Search Functionality:** Add search bars with real-time filtering
- [ ] **Pagination:** Implement pagination for large datasets
- [ ] **Data Display:** Format data appropriately (dates, numbers, etc.)
- [ ] **Empty States:** Design empty state screens with helpful messages
- [ ] **Loading Skeletons:** Add skeleton screens during data loading

#### **Update Operations**
- [ ] **Edit Forms:** Implement edit functionality with pre-populated data
- [ ] **Inline Editing:** Add inline editing capabilities where appropriate
- [ ] **Batch Updates:** Support bulk update operations
- [ ] **Change Tracking:** Track and display field changes
- [ ] **Conflict Resolution:** Handle concurrent edit conflicts
- [ ] **Audit Trail:** Log all update operations

#### **Delete Operations**
- [ ] **Delete Confirmation:** Implement confirmation dialogs with impact details
- [ ] **Soft Delete:** Use soft delete with audit trail where required
- [ ] **Batch Delete:** Support bulk deletion with proper warnings
- [ ] **Cascade Handling:** Handle related record dependencies
- [ ] **Recovery Options:** Provide undo/recovery mechanisms
- [ ] **Cleanup Processes**: Implement proper data cleanup

### **Section 3: Django Persistence Verification**

#### **Model Compliance**
- [ ] **Domain Ownership:** Verify models belong to correct HRM domain per .hrm.cline/01_governance.md
- [ ] **Company References**: Use lazy string reference: `'domain.Company'` for multi-tenant
- [ ] **Audit Fields**: Ensure created_at, updated_at, created_by_user_id present
- [ ] **Indexes & Constraints**: Verify proper database indexes and constraints
- [ ] **Relationships**: Check foreign key relationships are properly defined
- [ ] **Validation Rules**: Implement model-level validation per BBP specifications

#### **Database Operations**
- [ ] **Migration Testing:** Verify migrations create and apply correctly
- [ ] **CRUD Endpoints:** Test all create, read, update, delete endpoints
- [ ] **Data Integrity**: Ensure no data loss during CRUD operations
- [ ] **Performance:** Verify query performance with proper indexes
- [ ] **Transaction Safety**: Ensure atomic transactions for complex operations
- [ ] **Backup Safety**: Verify data backup and recovery procedures

#### **API Integration**
- [ ] **Serializer Validation:** Test serializer validation rules
- [ ] **Permission Checks:** Verify proper authentication and authorization
- [ ] **Error Responses**: Test proper error handling and status codes
- [ ] **Data Formatting**: Ensure consistent API response formats
- [ ] **Rate Limiting**: Implement appropriate rate limiting
- [ ] **API Documentation**: Maintain accurate API documentation

### **Section 4: Testing & Quality Assurance**

#### **Unit Testing**
- [ ] **Model Tests**: Test all model methods and validations
- [ ] **View Tests**: Test all CRUD endpoints with various scenarios
- [ ] **Serializer Tests**: Test serializer validation and data transformation
- [ ] **Utility Tests**: Test helper functions and utilities
- [ ] **Form Tests**: Test form validation and processing
- [ ] **Service Tests**: Test business logic in service layers

#### **Integration Testing**
- [ ] **End-to-End Workflows:** Test complete user journeys
- [ ] **API Integration:** Test frontend-backend integration
- [ ] **Database Integration:** Test data persistence and retrieval
- [ ] **Cross-Module Testing:** Verify no cross-app imports or dependencies
- [ ] **Permission Testing**: Test role-based access control
- [ ] **Performance Testing**: Test under load conditions

#### **User Acceptance Testing**
- [ ] **Usability Testing:** Verify intuitive user interface
- [ ] **Workflow Testing:** Test real-world usage scenarios
- [ ] **Browser Compatibility:** Test across supported browsers
- [ ] **Device Testing:** Test on various screen sizes
- [ ] **Accessibility Testing:** Verify screen reader compatibility
- [ ] **Error Scenario Testing**: Test error handling and recovery

### **Section 5: Deployment & Monitoring**

#### **Production Readiness**
- [ ] **Environment Configuration:** Set up production settings
- [ ] **Database Configuration:** Configure production database connections
- [ ] **Static Files:** Configure static file serving and CDN
- [ ] **Security Headers**: Implement security headers and HTTPS
- [ ] **Performance Optimization**: Enable caching and compression
- [ ] **Backup Procedures**: Implement automated backup systems

#### **Monitoring & Logging**
- [ ] **Error Logging:** Configure comprehensive error logging
- [ ] **Performance Monitoring**: Set up application performance monitoring
- [ ] **User Analytics:** Implement user behavior tracking
- [ ] **Health Checks:** Configure application health endpoints
- [ ] **Alert Systems:** Set up alerting for critical issues
- [ ] **Audit Logging**: Maintain comprehensive audit trails

### **Section 6: Governance Compliance**

#### **Platform.cline Compliance**
- [ ] **Governance Rules**: Follow .hrm.cline/01_governance.md rules strictly
- [ ] **Development Stability**: Follow development stability best practices
- [ ] **Domain Ownership**: Maintain proper HRM domain boundaries
- [ ] **Mergeability Contract**: Ensure COPY→PASTE→RUN works
- [ ] **No Cross-App Imports**: Verify complete module isolation
- [ ] **UI Canon Compliance**: Follow Olivine UI canon exactly

#### **Quality Gates**
- [ ] **Code Review**: Complete peer review process
- [ ] **Security Review**: Pass security vulnerability assessment
- [ ] **Performance Review**: Meet performance benchmarks
- [ ] **Documentation Review**: Ensure complete documentation
- [ ] **Testing Coverage**: Achieve >80% test coverage
- [ ] **Deployment Approval**: Get deployment approval from stakeholders

---

## 🎨 UI Component Library

### **Overview**

This section defines the canonical UI components and design system for the platform. All new UI development should follow these standards to ensure consistency and reusability.

### **Component Categories**

#### **1. Form Components**

##### Input Fields**
```tsx
// Standard Input
<input className="form-input" type="text" placeholder="Enter text..." />

// Email Input
<input className="form-input" type="email" placeholder="email@example.com" />

// Number Input
<input className="form-input" type="number" placeholder="0" />

// Date Input
<input className="form-input" type="date" />
```

##### Buttons
```tsx
// Primary Button
<button className="btn btn-primary">Save</button>

// Secondary Button
<button className="btn btn-secondary">Cancel</button>

// Outline Button
<button className="btn btn-outline">Edit</button>

// Danger Button
<button className="btn btn-danger">Delete</button>

// Icon Button
<button className="btn btn-icon">
  <Icon className="w-4 h-4" />
</button>
```

##### Select Dropdowns
```tsx
<select className="form-select">
  <option value="">Select option</option>
  <option value="option1">Option 1</option>
  <option value="option2">Option 2</option>
</select>
```

#### **2. Layout Components**

##### Cards
```tsx
<div className="card">
  <div className="card-header">
    <h3 className="card-title">Card Title</h3>
  </div>
  <div className="card-body">
    Card content goes here
  </div>
  <div className="card-footer">
    <button className="btn btn-primary">Action</button>
  </div>
</div>
```

##### Modals
```tsx
<div className="modal-overlay">
  <div className="modal">
    <div className="modal-header">
      <h2 className="modal-title">Modal Title</h2>
      <button className="modal-close">&times;</button>
    </div>
    <div className="modal-body">
      Modal content
    </div>
    <div className="modal-footer">
      <button className="btn btn-secondary">Cancel</button>
      <button className="btn btn-primary">Confirm</button>
    </div>
  </div>
</div>
```

#### **3. Navigation Components**

##### Breadcrumbs
```tsx
<nav className="breadcrumb">
  <a href="#" className="breadcrumb-item">Home</a>
  <a href="#" className="breadcrumb-item">Products</a>
  <span className="breadcrumb-item active">Current Page</span>
</nav>
```

##### Tabs
```tsx
<div className="tabs">
  <div className="tab-list">
    <button className="tab-item active">Tab 1</button>
    <button className="tab-item">Tab 2</button>
    <button className="tab-item">Tab 3</button>
  </div>
  <div className="tab-content">
    <div className="tab-pane active">Tab 1 content</div>
    <div className="tab-pane">Tab 2 content</div>
    <div className="tab-pane">Tab 3 content</div>
  </div>
</div>
```

#### **4. Data Display Components**

##### Tables
```tsx
<table className="table">
  <thead>
    <tr>
      <th>Name</th>
      <th>Email</th>
      <th>Status</th>
      <th>Actions</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>John Doe</td>
      <td>john@example.com</td>
      <td><span className="badge badge-success">Active</span></td>
      <td>
        <button className="btn btn-sm btn-outline">Edit</button>
      </td>
    </tr>
  </tbody>
</table>
```

##### Badges
```tsx
<span className="badge">Default</span>
<span className="badge badge-primary">Primary</span>
<span className="badge badge-success">Success</span>
<span className="badge badge-warning">Warning</span>
<span className="badge badge-danger">Danger</span>
```

#### **5. Feedback Components**

##### Alerts
```tsx
<div className="alert alert-info">
  <strong>Info:</strong> This is an info alert.
</div>

<div className="alert alert-success">
  <strong>Success:</strong> Operation completed successfully.
</div>

<div className="alert alert-warning">
  <strong>Warning:</strong> Please review your input.
</div>

<div className="alert alert-danger">
  <strong>Error:</strong> Something went wrong.
</div>
```

### **Design System**

#### **Colors**
```css
:root {
  /* Primary Colors */
  --color-primary: #3b82f6;
  --color-primary-hover: #2563eb;
  --color-primary-light: #dbeafe;
  --color-primary-dark: #1d4ed8;
  
  /* Secondary Colors */
  --color-secondary: #6b7280;
  --color-secondary-hover: #4b5563;
  --color-secondary-light: #f3f4f6;
  --color-secondary-dark: #374151;
  
  /* Success Colors */
  --color-success: #10b981;
  --color-success-hover: #059669;
  --color-success-light: #d1fae5;
  --color-success-dark: #047857;
  
  /* Warning Colors */
  --color-warning: #f59e0b;
  --color-warning-hover: #d97706;
  --color-warning-light: #fef3c7;
  --color-warning-dark: #b45309;
  
  /* Error Colors */
  --color-error: #ef4444;
  --color-error-hover: #dc2626;
  --color-error-light: #fef2f2;
  --color-error-dark: #b91c1c;
  
  /* Neutral Colors */
  --color-gray-50: #f9fafb;
  --color-gray-100: #f3f4f6;
  --color-gray-200: #e5e7eb;
  --color-gray-300: #d1d5db;
  --color-gray-400: #9ca3af;
  --color-gray-500: #6b7280;
  --color-gray-600: #4b5563;
  --color-gray-700: #374151;
  --color-gray-800: #1f2937;
  --color-gray-900: #111827;
}
```

#### **Typography**
```css
:root {
  /* Font Families */
  --font-sans: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  --font-mono: 'SF Mono', Monaco, 'Inconsolata', 'Roboto Mono', monospace;
  
  /* Font Sizes */
  --text-xs: 0.75rem;    /* 12px */
  --text-sm: 0.875rem;   /* 14px */
  --text-base: 1rem;      /* 16px */
  --text-lg: 1.125rem;    /* 18px */
  --text-xl: 1.25rem;     /* 20px */
  --text-2xl: 1.5rem;     /* 24px */
  --text-3xl: 1.875rem;   /* 30px */
  --text-4xl: 2.25rem;    /* 36px */
  --text-5xl: 3rem;       /* 48px */
  --text-6xl: 3.75rem;     /* 60px */
  
  /* Font Weights */
  --font-light: 300;
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
  --font-extrabold: 800;
  
  /* Line Heights */
  --leading-tight: 1.25;
  --leading-snug: 1.375;
  --leading-normal: 1.5;
  --leading-relaxed: 1.625;
  --leading-loose: 1.75;
  
  /* Spacing */
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.25rem;    /* 20px */
  --space-6: 1.5rem;     /* 24px */
  --space-8: 2rem;       /* 32px */
  --space-10: 2.5rem;    /* 40px */
  --space-12: 3rem;       /* 48px */
  --space-16: 4rem;       /* 64px */
  --space-20: 5rem;       /* 80px */
  --space-24: 6rem;       /* 96px */
  --space-32: 8rem;       /* 128px */
}
```

#### **Border Radius**
```css
:root {
  --radius-none: 0;
  --radius-sm: 0.125rem;   /* 2px */
  --radius: 0.25rem;      /* 4px */
  --radius-md: 0.375rem;    /* 6px */
  --radius-lg: 0.5rem;      /* 8px */
  --radius-xl: 0.75rem;     /* 12px */
  --radius-2xl: 1rem;       /* 16px */
  --radius-3xl: 1.5rem;     /* 24px */
  --radius-full: 9999px;
}
```

#### **Shadows**
```css
:root {
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.07), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}
```

### **Component Classes**

#### **Base Classes**
```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  font-weight: var(--font-medium);
  transition: all 0.2s ease;
  cursor: pointer;
  border: 1px solid transparent;
  text-decoration: none;
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  line-height: var(--leading-tight);
  padding: var(--space-2) var(--space-3);
  white-space: nowrap;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn:focus {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.form-input {
  display: block;
  width: 100%;
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--color-gray-300);
  border-radius: var(--radius-md);
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  line-height: var(--leading-tight);
  background-color: white;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.form-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.card {
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
  border: 1px solid var(--color-gray-200);
  overflow: hidden;
}

.badge {
  display: inline-flex;
  align-items: center;
  padding: var(--space-1) var(--space-2);
  font-size: var(--text-xs);
  font-weight: var(--font-medium);
  border-radius: var(--radius-full);
  white-space: nowrap;
}

.alert {
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
  margin-bottom: var(--space-4);
  border: 1px solid transparent;
}

.table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow);
  border: 1px solid var(--color-gray-200);
}

.table th,
.table td {
  padding: var(--space-3) var(--space-4);
  text-align: left;
  border-bottom: 1px solid var(--color-gray-200);
}

.table th {
  font-weight: var(--font-semibold);
  background-color: var(--color-gray-50);
  color: var(--color-gray-900);
}
```

---

## 🔄 Workflow Integration

### **Development Integration**
- **Implementation Steps**: Follow detailed implementation guidance in this development guide
- **Governance Compliance**: Adhere to all governance rules in `.hrm.cline/01_governance.md`
- **Task Execution**: Use enhanced task checklists in `.hrm.cline/tasks.md` for complete development guidance

### **Implementation Workflow**
When using these components in HRM module development:

#### **1. Planning Phase**
- Reference this development guide for step-by-step implementation
- Review `.hrm.cline/01_governance.md` for governance requirements

#### **2. Development Phase**
- Follow development stability guidelines in this guide
- Use Olivine UI canon components from the UI Component Library section

#### **3. Verification Phase**
- Complete comprehensive checklist in the Development Checklist section
- Track progress using detailed task lists in `.hrm.cline/tasks.md`

### **Quality Standards**
- **UI Compliance**: All components must follow Olivine UI canon specifications
- **Development Standards**: Follow platform.cline development stability guidelines
- **Testing Requirements**: Verify all components pass comprehensive quality checks
- **Documentation**: Maintain proper documentation for component usage and implementation

### **Cross-Reference Network**
```
.hrm.cline/01_governance.md (Foundation)
    ↓
.hrm.cline/dev_guide.md (This consolidated guide)
    ↓
.hrm.cline/tasks.md (Task execution)
.hrm.cline/tracker.md (Progress tracking)
```

---

## 📊 **Success Criteria**

### **Must-Have Requirements:**
- ✅ UI follows Olivine UI canon exactly
- ✅ All CRUD operations work correctly
- ✅ Data persists in Django without loss
- ✅ No governance breaches detected
- ✅ All tests passing with >80% coverage

### **Should-Have Requirements:**
- ✅ Responsive design works on all devices
- ✅ Accessibility compliance achieved
- ✅ Performance benchmarks met
- ✅ User acceptance testing passed

### **Could-Have Requirements:**
- ✅ Advanced features implemented
- ✅ Enhanced user experience
- ✅ Additional optimizations
- ✅ Extended documentation

---

## 📋 **Usage Instructions**

### **For Each HRM Module Development:**
1. **Read BBP Specification**: Review the HRM2 BBP file for requirements
2. **Follow Implementation Process**: Use the 10-step implementation process
3. **Complete Development Checklist**: Verify all checklist items are completed
4. **Use UI Components**: Apply Olivine UI canon components from the library
5. **Ensure Governance Compliance**: Follow all governance rules

### **Quality Gate Process:**
- **Pre-Development**: Review checklist and understand requirements
- **During Development**: Track progress through each section
- **Pre-Deployment**: Verify all checklist items completed
- **Post-Deployment**: Monitor and maintain compliance

---

**VERSION:** 3.0 (Consolidated)  
**LAST UPDATED**: January 4, 2026  
**COMPATIBLE**: All .hrm.cline governance documents  
**SCOPE**: Complete HRM module development guidance

This consolidated development guide ensures consistent, high-quality HRM module development while maintaining strict adherence to platform standards and governance requirements.
