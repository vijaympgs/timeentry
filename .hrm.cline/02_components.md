# UI Canon - Reusable Component Library

## Overview

This document defines the canonical UI components and design system for the platform. All new UI development should follow these standards to ensure consistency and reusability.

## Component Categories

### 1. Form Components

#### Input Fields
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

#### Buttons
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

#### Select Dropdowns
```tsx
<select className="form-select">
  <option value="">Select option</option>
  <option value="option1">Option 1</option>
  <option value="option2">Option 2</option>
</select>
```

### 2. Layout Components

#### Cards
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

#### Modals
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

### 3. Navigation Components

#### Breadcrumbs
```tsx
<nav className="breadcrumb">
  <a href="#" className="breadcrumb-item">Home</a>
  <a href="#" className="breadcrumb-item">Products</a>
  <span className="breadcrumb-item active">Current Page</span>
</nav>
```

#### Tabs
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

### 4. Data Display Components

#### Tables
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

#### Badges
```tsx
<span className="badge">Default</span>
<span className="badge badge-primary">Primary</span>
<span className="badge badge-success">Success</span>
<span className="badge badge-warning">Warning</span>
<span className="badge badge-danger">Danger</span>
```

### 5. Feedback Components

#### Alerts
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

#### Tooltips
```tsx
<div className="tooltip">
  <div className="tooltip-content">
    Hover me for more information
  </div>
</div>
```

## Design System

### Colors
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

### Typography
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

### Border Radius
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

### Shadows
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

## Component Classes

### Base Classes
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

### Modifier Classes

#### Button Variants
```css
.btn-primary {
  background-color: var(--color-primary);
  color: white;
  border-color: var(--color-primary);
}

.btn-primary:hover {
  background-color: var(--color-primary-hover);
  border-color: var(--color-primary-dark);
}

.btn-secondary {
  background-color: var(--color-gray-100);
  color: var(--color-gray-900);
  border-color: var(--color-gray-300);
}

.btn-secondary:hover {
  background-color: var(--color-gray-200);
  border-color: var(--color-gray-400);
}

.btn-outline {
  background-color: transparent;
  color: var(--color-gray-700);
  border-color: var(--color-gray-300);
}

.btn-outline:hover {
  background-color: var(--color-gray-50);
  color: var(--color-gray-900);
}

.btn-sm {
  padding: var(--space-1) var(--space-2);
  font-size: var(--text-xs);
}

.btn-lg {
  padding: var(--space-3) var(--space-4);
  font-size: var(--text-base);
}
```

#### Status Variants
```css
.badge-primary {
  background-color: var(--color-primary);
  color: white;
}

.badge-success {
  background-color: var(--color-success);
  color: white;
}

.badge-warning {
  background-color: var(--color-warning);
  color: white;
}

.badge-danger {
  background-color: var(--color-error);
  color: white;
}
```

#### Alert Variants
```css
.alert-info {
  background-color: #eff6ff;
  border-color: #bfdbfe;
  color: #1e40af;
}

.alert-success {
  background-color: #d1fae5;
  border-color: #a7f3d0;
  color: #065f46;
}

.alert-warning {
  background-color: #fffbeb;
  border-color: #fde68a;
  color: #92400e;
}

.alert-danger {
  background-color: #fef2f2;
  border-color: #fecaca;
  color: #991b1b;
}
```

## Usage Guidelines

### 1. Component Reusability
- Always use the predefined component classes
- Create wrapper components for complex UI patterns
- Maintain consistency across all modules

### 2. Customization
- Use CSS variables for theming
- Extend base classes with modifiers
- Follow the naming convention

### 3. Accessibility
- Include proper ARIA attributes
- Ensure keyboard navigation support
- Maintain color contrast ratios

### 4. Responsive Design
- Use relative units for scalability
- Implement mobile-first approach
- Test across different screen sizes

### 5. Development Integration
- **Implementation Steps**: Follow detailed implementation guidance in `.hrm.cline/03_dev_guide.md`
- **Development Stability**: Ensure development stability and best practices per `.hrm.cline/03_dev_guide.md`
- **Quality Assurance**: Verify implementation completeness with comprehensive checklist in `.hrm.cline/03_dev_guide.md`
- **Governance Compliance**: Adhere to all governance rules in `.hrm.cline/01_governance.md`
- **Task Execution**: Use enhanced task checklists in `.hrm.cline/04_tasks.md` for complete development guidance

### 6. Implementation Workflow
When using these components in HRM module development:

1. **Planning Phase**: 
   - Reference `.hrm.cline/03_dev_guide.md` for step-by-step implementation
   - Review `.hrm.cline/01_governance.md` for governance requirements

2. **Development Phase**:
   - Follow development stability guidelines in `.hrm.cline/03_dev_guide.md`
   - Use Olivine UI canon components from this document (`.hrm.cline/02_components.md`)

3. **Verification Phase**:
   - Complete comprehensive checklist in `.hrm.cline/03_dev_guide.md`
   - Track progress using detailed task lists in `.hrm.cline/04_tasks.md`

### 7. Quality Standards
- **UI Compliance**: All components must follow Olivine UI canon specifications
- **Development Standards**: Follow platform.cline development stability guidelines
- **Testing Requirements**: Verify all components pass comprehensive quality checks
- **Documentation**: Maintain proper documentation for component usage and implementation

## Implementation Examples

### Reusable Button Component
```tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick,
  children
}) => {
  const variantClasses = {
    primary: 'btn btn-primary',
    secondary: 'btn btn-secondary',
    outline: 'btn btn-outline',
    danger: 'btn btn-danger'
  };

  const sizeClasses = {
    sm: 'btn-sm',
    md: '',
    lg: 'btn-lg'
  };

  return (
    <button
      className={`${variantClasses[variant]} ${sizeClasses[size]} ${disabled ? 'disabled' : ''}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
};
```

### Reusable Card Component
```tsx
interface CardProps {
  title?: string;
  footer?: React.ReactNode;
  children: React.ReactNode;
  className?: string;
}

export const Card: React.FC<CardProps> = ({
  title,
  footer,
  children,
  className = ''
}) => {
  return (
    <div className={`card ${className}`}>
      {title && (
        <div className="card-header">
          <h3 className="card-title">{title}</h3>
        </div>
      )}
      <div className="card-body">
        {children}
      </div>
      {footer && (
        <div className="card-footer">
          {footer}
        </div>
      )}
    </div>
  );
};
```

This UI canon ensures consistent, reusable, and maintainable UI components across the entire platform.
