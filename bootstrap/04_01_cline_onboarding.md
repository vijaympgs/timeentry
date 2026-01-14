# AGENT E ONBOARDING: HRM & CRM UI DEVELOPMENT GUIDE

**Purpose**: Complete UI development guidelines for Agent E building HRM and CRM modules  
**Target**: HRM and CRM modules to be integrated into Olivine ERP Platform  
**Date**: 2026-01-07 20:51 IST  
**Context**: Agent E is building forms and UIs that will be copied into the enterprise shell

---

## 🎯 **CRITICAL UNDERSTANDING**

### **Project Structure**
```
olivine-erp-platform/
├── Retail (WIP - Astra)
├── FMS (Planned)
└── [Agent E builds separately, then copies here]
    ├── CRM/
    └── HRM/
```

**Your Mission**: Build HRM and CRM modules following **exact same standards** as Retail. Use **identical UI patterns, typography, colors, and styling**. Ensure **seamless integration** when copied into enterprise shell.

---

## 📚 **MANDATORY READING (IN ORDER)**

### **1. UI Typography & Styling Reference** ⭐ **MOST IMPORTANT**
**File**: `.steering/18_WIRING_CHECKLISTS/UI_TYPOGRAPHY_STYLING_REFERENCE.md`

**What it contains**:
- ✅ Exact font sizes for every element (L1-L4 typography)
- ✅ Exact colors (hex codes) for text, backgrounds, borders
- ✅ Form elements: labels, textboxes, LOV, checkbox, radio button
- ✅ Button styles: primary, secondary, link, icon
- ✅ Table styles: headers, cells, hover states
- ✅ Status badge colors and styles
- ✅ Copy-paste code snippets for common patterns

**READ THIS FIRST** - This is your UI bible!

---

### **2. Wiring Checklists** ⭐ **IMPLEMENTATION GUIDES**
**Location**: `.steering/18_WIRING_CHECKLISTS/`

#### **Master Data Wiring**
**File**: `MASTER_DATA_WIRING.md`

**Use for**: Employee Master, Department, Position, Contact, Account, etc.

**11 Phases**:
- Backend Model & Serializer
- Backend ViewSet & URLs
- Frontend Types
- Frontend Service Layer
- Main Component Structure
- State Management
- Data Fetching
- UI Layout (List Page)
- Action Handlers (Add, Edit, Delete)
- Modal Integration
- Testing & Validation

#### **Transaction Form Wiring**
**File**: `TRANSACTION_FORM_WIRING.md`

**Use for**: Leave Request, Attendance Adjustment, Lead, Opportunity, Campaign, etc.

**14 Phases**:
- Backend Model & Serializer
- Backend ViewSet with Workflow
- Frontend Types
- Frontend Service Layer
- Form Page Component Structure
- **TransactionToolbar Integration** ⚠️ **IMPORTANT**
- Header Section
- Line Items Grid (if applicable)
- Lookup Modals
- Workflow Actions
- Status State Machine
- Real-time Calculations
- Validation & Error Handling
- Testing

#### **Workflow Wiring**
**File**: `WORKFLOW_WIRING.md`

**Use for**: Leave approval, Attendance workflow, Lead qualification, Opportunity stages, etc.

**10 Phases**:
- Status State Machine Definition
- Backend Workflow Actions
- Frontend Workflow Service
- Status-based UI States
- Action Buttons & Toolbar
- Validation Rules
- Authorization & Permissions
- Audit Trail
- Notifications
- Testing

---

### **3. UI Canon Templates** ⭐ **FUNCTIONAL PATTERNS**
**Location**: `.steering/14UI_CANON/`

#### **Governance & Standards (01-09)**:
- `01_Onboarding_Context.md` - Project context
- `02_Architecture_Rules.md` - Architecture rules
- `03_Development_Standards.md` - Development standards
- `04_Frontend_UI_Canon.md` - Frontend structure
- `05_UI_Menu_Template_Mapping.md` - Menu to template mapping
- `06_Layout_Terminology.md` - Layout & design system
- `07_Governance_Market_References.md` - Governance rules
- `08_Sidebar_Implementation.md` - Sidebar specs
- `09_Lookup_Canon.md` - Lookup modal patterns

#### **Functional Templates (10-15)**:
- `10_Master_Simple_Template.md` - Simple master pattern (e.g., Department, Position)
- `11_Master_Medium_Template.md` - Medium master pattern (e.g., Employee, Contact)
- `12_Master_Complex_Template.md` - Complex master pattern (e.g., Account with hierarchy)
- `13_Transaction_Simple_Template.md` - Simple transaction (e.g., Attendance Adjustment)
- `14_Transaction_Medium_Template.md` - Medium transaction (e.g., Leave Request, Lead)
- `15_Transaction_Complex_Template.md` - Complex transaction (e.g., Opportunity with stages)

---

## 🎨 **UI STANDARDS (NON-NEGOTIABLE)**

### **Typography Levels**

#### **L1 - Page Titles**
```tsx
<h1 className="text-xl font-semibold text-[#201f1e]">
    Employee Directory
</h1>
```

- **Font Size**: `20px` / `text-xl`
- **Font Weight**: `600` / `font-semibold`
- **Color**: `#201f1e` (dark gray)

#### **L2 - Section Headers**
```tsx
<h2 className="text-base font-semibold text-[#323130]">
    Personal Information
</h2>
```

- **Font Size**: `16px` / `text-base`
- **Font Weight**: `600` / `font-semibold`
- **Color**: `#323130` (medium gray)

#### **L3 - Field Labels**
```tsx
<label className="text-xs font-semibold text-[#605e5c] uppercase">
    Employee Name *
</label>
```

- **Font Size**: `12px` / `text-xs`
- **Font Weight**: `600` / `font-semibold`
- **Color**: `#605e5c` (gray)
- **Text Transform**: `uppercase`

#### **L4 - Body Text**
```tsx
<p className="text-sm text-[#323130]">
    Regular content text
</p>
```

- **Font Size**: `14px` / `text-sm`
- **Color**: `#323130` (medium gray)

---

### **Form Elements**

#### **Text Input (Standard)**
```tsx
<input 
    type="text" 
    className="w-full px-3 py-2 border border-gray-300 rounded-sm text-sm focus:border-[#0078d4] focus:ring-1 focus:ring-[#0078d4] outline-none" 
/>
```

- **Font Size**: `14px` / `text-sm`
- **Padding**: `px-3 py-2` (12px horizontal, 8px vertical)
- **Border**: `1px solid #d1d1d1` / `border-gray-300`
- **Border Radius**: `2px` / `rounded-sm`
- **Focus Border**: `#0078d4` (blue)
- **Focus Ring**: `1px solid #0078d4`

#### **Select Dropdown (LOV)**
```tsx
<select className="w-full px-3 py-2 border border-gray-300 rounded-sm text-sm focus:border-[#0078d4] outline-none">
    <option>Select Department...</option>
</select>
```

- **Font Size**: `14px` / `text-sm`
- **Padding**: `px-3 py-2`
- **Border**: `1px solid #d1d1d1` / `border-gray-300`
- **Focus Border**: `#0078d4` (blue)

#### **Checkbox**
```tsx
<label className="flex items-center gap-2">
    <input 
        type="checkbox" 
        className="w-4 h-4 text-[#0078d4] border-gray-300 rounded focus:ring-[#0078d4]" 
    />
    <span className="text-sm text-[#323130]">Active</span>
</label>
```

- **Checkbox Size**: `16px` / `w-4 h-4`
- **Checked Color**: `#0078d4` (blue)
- **Border**: `1px solid #d1d1d1` / `border-gray-300`
- **Label Font Size**: `14px` / `text-sm`
- **Label Color**: `#323130` (medium gray)

#### **Radio Button**
```tsx
<label className="flex items-center gap-2">
    <input 
        type="radio" 
        className="w-4 h-4 text-[#0078d4] border-gray-300 focus:ring-[#0078d4]" 
    />
    <span className="text-sm text-[#323130]">Full-time</span>
</label>
```

- **Radio Size**: `16px` / `w-4 h-4`
- **Checked Color**: `#0078d4` (blue)
- **Border**: `1px solid #d1d1d1` / `border-gray-300`
- **Label Font Size**: `14px` / `text-sm`
- **Label Color**: `#323130` (medium gray)

---

### **Buttons**

#### **Primary Button**
```tsx
<button 
    style={{ 
        backgroundColor: 'var(--button-primary-bg)', /* #ff6600 */ 
        color: 'var(--button-primary-text)' /* #ffffff */ 
    }} 
    className="px-3 py-1.5 font-medium rounded-sm" 
>
    Save
</button>
```

- **Background**: `#ff6600` (orange) / `var(--button-primary-bg)`
- **Text Color**: `#ffffff` (white) / `var(--button-primary-text)`
- **Hover Background**: `#e65c00` (darker orange) / `var(--button-primary-hover-bg)`
- **Font Size**: `14px` / `text-sm`
- **Font Weight**: `500` / `font-medium`
- **Padding**: `px-3 py-1.5` (12px horizontal, 6px vertical)
- **Border Radius**: `2px` / `rounded-sm`

#### **Secondary Button**
```tsx
<button className="px-3 py-1.5 hover:bg-[#edebe9] rounded-sm text-[#323130] font-medium">
    Cancel
</button>
```

- **Background**: `transparent`
- **Text Color**: `#323130` (medium gray)
- **Hover Background**: `#edebe9` (light gray)
- **Font Size**: `14px` / `text-sm`
- **Font Weight**: `500` / `font-medium`
- **Padding**: `px-3 py-1.5`
- **Border Radius**: `2px` / `rounded-sm`

---

### **Status Badges**
```tsx
<span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
    ACTIVE
</span>
```

**Status Colors**:
- **ACTIVE**: `bg-green-100 text-green-800`
- **PENDING**: `bg-yellow-100 text-yellow-700`
- **APPROVED**: `bg-blue-100 text-blue-700`
- **REJECTED**: `bg-red-100 text-red-700`
- **DRAFT**: `bg-gray-100 text-gray-700`

---

## 🚫 **WHAT NOT TO DO (CRITICAL)**

### ❌ **DO NOT Create Custom Toolbars**
- Don't create your own toolbar component
- Don't use different button styles in toolbars
- Don't change keyboard shortcuts (F1-F12)
- Don't hardcode `allowedActions` prop - API controls this
- Don't create separate list/form database entries

**✅ INSTEAD**: 
- Use `MasterToolbar` from `@core/ui-canon/frontend/ui/components/MasterToolbarConfigDriven`
- Implement API-driven permission system (v2.0)
- Use `getMode()` function for VIEW/VIEW_FORM/CREATE/EDIT modes
- Match frontend `viewId` to backend `menu_id` exactly
- Follow toolbar_implementation_checklist.md completely

---

### ❌ **DO NOT Use Different Colors**
- Don't use `purple`, `indigo`, `pink` for primary actions
- Don't use different shades of blue
- Don't create custom color schemes

**✅ INSTEAD**:
- Primary buttons: `#ff6600` (orange) via `var(--button-primary-bg)`
- Links/Focus: `#0078d4` (blue)
- Text: `#201f1e`, `#323130`, `#605e5c` (grays)

---

### ❌ **DO NOT Use Different Font Sizes**
- Don't use `text-lg`, `text-2xl`, `text-3xl` for page titles
- Don't use `text-base` for labels
- Don't use custom font weights

**✅ INSTEAD**:
- Page titles: `text-xl` (20px)
- Section headers: `text-base` (16px)
- Labels: `text-xs` (12px) uppercase
- Body text: `text-sm` (14px)

---

### ❌ **DO NOT Skip Wiring Checklists**
- Don't jump straight to UI without backend setup
- Don't skip service layer
- Don't skip validation
- Don't skip testing

**✅ INSTEAD**:
- Follow all 11 phases for master data
- Follow all 14 phases for transactions
- Check off each step as you complete it

---

## ✅ **WHAT TO DO (BEST PRACTICES)**

### ✅ **Follow the Pattern**
1. **Read the wiring checklist** for your feature type (master/transaction)
2. **Copy the reference implementation** (e.g., `CustomerSetup.tsx`, `PurchaseOrderFormPage.tsx`)
3. **Adapt it for your feature** (e.g., `EmployeeSetup.tsx`, `LeaveRequestFormPage.tsx`)
4. **Use exact same styling** from `UI_TYPOGRAPHY_STYLING_REFERENCE.md`
5. **Test thoroughly**

---

### ✅ **Use Reference Implementations**

#### **For Master Data Pages**:
**Reference**: `frontend/src/pages/CustomerSetup.tsx`

**Copy for**: Employee, Department, Position, Contact, Account, etc.

**Pattern**:
- List view with search and filters
- "Add New" button (primary orange)
- Table with hover states
- Edit/Delete actions
- Modal for add/edit

#### **For Transaction Forms**:
**Reference**: `frontend/apps/retail/procurement/pages/PurchaseOrderFormPage.tsx`

**Copy for**: Leave Request, Attendance Adjustment, Lead, Opportunity, etc.

**Pattern**:
- TransactionToolbar at top
- Header section with fields
- Line items grid (if applicable)
- Workflow actions (Save, Submit, Approve, etc.)
- Status state machine

---

### ✅ **Use Exact Color Codes**
```css
/* Primary Colors */
--primary-blue: #0078d4      /* Links, focus states */
--primary-orange: #ff6600    /* Primary buttons */

/* Text Colors */
--text-dark: #201f1e         /* Page titles */
--text-medium: #323130       /* Body text */
--text-gray: #605e5c         /* Labels */
--text-light: #a19f9d        /* Placeholder */

/* Background Colors */
--bg-white: #ffffff          /* Cards, modals */
--bg-light: #faf9f8          /* Page background */
--bg-gray: #f3f2f1           /* Table headers */
--bg-blue-light: #f3f9ff     /* Row hover */

/* Border Colors */
--border-light: #edebe9      /* Card borders */
--border-medium: #d1d1d1     /* Input borders */
--border-focus: #0078d4      /* Focus state */
```

---

## 📋 **QUICK START CHECKLIST**

### **Before You Start Coding**:
- [ ] Read `UI_TYPOGRAPHY_STYLING_REFERENCE.md` (entire file)
- [ ] Read the appropriate wiring checklist (master/transaction)
- [ ] Identify the template type (MST-S/M/C or TXN-S/M/C)
- [ ] Find the reference implementation in Retail module
- [ ] Copy the reference file to your HRM/CRM folder
- [ ] Rename and adapt for your feature

### **While Coding**:
- [ ] Use exact font sizes from typography reference
- [ ] Use exact colors from color palette
- [ ] Use `var(--button-primary-bg)` for primary buttons
- [ ] Use `rounded-sm` (2px) for all borders except badges
- [ ] Use `focus:border-[#0078d4]` for all inputs
- [ ] Use `hover:bg-[#edebe9]` for secondary buttons
- [ ] Follow the wiring checklist phase by phase

### **Before Committing**:
- [ ] All font sizes match typography reference
- [ ] All colors match color palette
- [ ] All buttons use standard styling
- [ ] All form elements use standard styling
- [ ] All tables use standard styling
- [ ] All status badges use standard colors
- [ ] Code follows wiring checklist
- [ ] Tested in browser

---

## 🎯 **HRM SPECIFIC GUIDANCE**

### **Common HRM Features**:

#### **Master Data**:
- **Employee Master** → Use `MST-M` (Medium Master Template)
- **Department** → Use `MST-S` (Simple Master Template)
- **Position** → Use `MST-S` (Simple Master Template)
- **Organizational Unit** → Use `MST-M` (Medium Master Template)

#### **Transactions**:
- **Leave Request** → Use `TXN-M` (Medium Transaction Template)
- **Attendance Adjustment** → Use `TXN-S` (Simple Transaction Template)
- **Expense Claim** → Use `TXN-M` (Medium Transaction Template)
- **Performance Review** → Use `TXN-C` (Complex Transaction Template)

---

## 🎯 **CRM SPECIFIC GUIDANCE**

### **Common CRM Features**:

#### **Master Data**:
- **Contact** → Use `MST-M` (Medium Master Template)
- **Account** → Use `MST-C` (Complex Master Template) - has hierarchy
- **Product Catalog** → Use `MST-M` (Medium Master Template)

#### **Transactions**:
- **Lead** → Use `TXN-M` (Medium Transaction Template)
- **Opportunity** → Use `TXN-C` (Complex Transaction Template) - has stages
- **Campaign** → Use `TXN-M` (Medium Transaction Template)
- **Quote** → Use `TXN-M` (Medium Transaction Template)

---

## 📁 **FILE STRUCTURE (WHEN COPYING TO ENTERPRISE SHELL)**

### **Expected Structure**:
```
olivine-erp-platform/
├── frontend/
│   ├── apps/
│   │   ├── retail/ (Astra's work)
│   │   ├── hrm/ (Your work - copy here)
│   │   │   ├── employee/
│   │   │   ├── leave/
│   │   │   ├── attendance/
│   │   │   └── ...
│   │   └── crm/ (Your work - copy here)
│   │       ├── leads/
│   │       ├── opportunities/
│   │       ├── contacts/
│   │       └── ...
│   └── src/
│       ├── services/ (Add hrmService.ts, crmService.ts)
│       └── ui/
│           └── components/ (Shared components)
└── backend/
    └── domain/
        ├── hrm/ (Your work - copy here)
        └── crm/ (Your work - copy here)
```

---

## 🚀 **INTEGRATION CHECKLIST (BEFORE COPYING)**

### **Frontend**:
- [ ] All imports use path aliases (`@services`, `@ui`, `@auth`)
- [ ] All components follow Retail naming conventions
- [ ] All routes registered in `router.tsx`
- [ ] All services created in `src/services/`
- [ ] All types defined in service files
- [ ] No hardcoded URLs (use `apiClient`)

### **Backend**:
- [ ] All models in `domain/hrm/` or `domain/crm/`
- [ ] All serializers follow DRF patterns
- [ ] All ViewSets use company scoping
- [ ] All URLs registered in `urls.py`
- [ ] All migrations applied
- [ ] Admin registered for all models

---

## 📞 **WHEN YOU NEED HELP**

### **Questions to Ask**:
- "Which template should I use for [feature]?" → Check `05_UI_Menu_Template_Mapping.md`
- "What color should I use for [element]?" → Check `UI_TYPOGRAPHY_STYLING_REFERENCE.md`
- "How do I implement [workflow]?" → Check `WORKFLOW_WIRING.md`
- "What's the reference for [feature type]?" → Check wiring checklists

### **Red Flags** (Ask before proceeding):
- ⚠️ "I'm creating a custom toolbar" → **STOP, ask first**
- ⚠️ "I'm using a different color scheme" → **STOP, ask first**
- ⚠️ "I'm skipping the service layer" → **STOP, ask first**
- ⚠️ "I'm not following the wiring checklist" → **STOP, ask first**

---

## ✅ **SUCCESS CRITERIA**

Your HRM/CRM modules are ready for integration when:
- ✅ All UIs look identical to Retail module (same fonts, colors, spacing)
- ✅ All wiring checklists followed completely
- ✅ All reference implementations adapted correctly
- ✅ All code follows enterprise shell patterns
- ✅ All features tested and working
- ✅ No custom toolbars, colors, or fonts
- ✅ Ready to copy into `olivine-erp-platform/`

---

## 📚 **FINAL REMINDERS**

1. **Read `UI_TYPOGRAPHY_STYLING_REFERENCE.md` FIRST** - This is your bible
2. **Follow wiring checklists EXACTLY** - Don't skip phases
3. **Copy reference implementations** - Don't reinvent the wheel
4. **Use exact colors and fonts** - No variations
5. **No custom toolbars** - Use standard components
6. **Test before copying** - Ensure everything works
7. **Ask when unsure** - Better to ask than to redo

---

**Welcome to the team, Agent E!** 🚀

Your mission: Build HRM and CRM modules that seamlessly integrate into the Olivine ERP Platform with zero visual or functional inconsistencies.

---

**Last Updated**: 2026-01-07 20:51 IST  
**Maintained By**: Astra (AI Coding Assistant)  
**For**: Agent E (HRM & CRM Development)
