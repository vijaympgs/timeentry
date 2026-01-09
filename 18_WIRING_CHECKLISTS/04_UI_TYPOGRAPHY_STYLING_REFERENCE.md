# UI TYPOGRAPHY & STYLING REFERENCE

**Purpose**: Comprehensive font, size, and color specifications for all UI elements  
**Audience**: Agent E (HRM, FMS, CRM module development)  
**Date**: 2026-01-07 20:47 IST  
**Source**: Extracted from Retail module implementations

---

## 📋 **TABLE OF CONTENTS**

1. [Typography Levels (L1-L4)](#typography-levels)
2. [List Pages](#list-pages)
3. [Form Pages / Modals](#form-pages--modals)
4. [Buttons](#buttons)
5. [Form Elements](#form-elements)
6. [Tables & Grids](#tables--grids)
7. [Status Badges](#status-badges)
8. [Colors Palette](#colors-palette)
9. [Quick Reference](#quick-reference)

---

## 🎨 **TYPOGRAPHY LEVELS**

### **L1 - Page Titles**
```css
font-size: var(--typography-l1-size)      /* 20px / 1.25rem */
font-weight: var(--typography-l1-weight)  /* 600 (semibold) */
color: var(--typography-l1-color)         /* #201f1e (dark gray) */
```

**Usage**: Main page headings
```tsx
<h1 style={{
    fontSize: 'var(--typography-l1-size)',
    fontWeight: 'var(--typography-l1-weight)',
    color: 'var(--typography-l1-color)'
}}>
    Page Title
</h1>
```

**Alternative (Tailwind)**:
```tsx
<h1 className="text-xl font-semibold text-[#201f1e]">
    Page Title
</h1>
```

---

### **L2 - Section Headers**
```css
font-size: 16px / 1rem
font-weight: 600 (semibold)
color: #323130 (medium gray)
```

**Usage**: Section titles, card headers
```tsx
<h2 className="text-base font-semibold text-[#323130]">
    Section Header
</h2>
```

---

### **L3 - Subsection Headers**
```css
font-size: 14px / 0.875rem
font-weight: 600 (semibold)
color: #605e5c (gray)
text-transform: uppercase
letter-spacing: 0.05em
```

**Usage**: Form labels, table headers
```tsx
<label className="text-sm font-semibold text-[#605e5c] uppercase">
    Field Label
</label>
```

---

### **L4 - Body Text**
```css
font-size: 14px / 0.875rem
font-weight: 400 (normal)
color: #323130 (medium gray)
```

**Usage**: Regular text, table cells
```tsx
<p className="text-sm text-[#323130]">
    Body text content
</p>
```

---

## 📄 **LIST PAGES**

### **Page Title**
```tsx
<h1 className="text-xl font-semibold text-[#201f1e]">
    Records Directory
</h1>
```
- **Font Size**: `20px` / `text-xl`
- **Font Weight**: `600` / `font-semibold`
- **Color**: `#201f1e` (dark gray)

---

### **Page Subtitle**
```tsx
<p className="text-sm text-[#605e5c]">
    Manage master data records
</p>
```
- **Font Size**: `14px` / `text-sm`
- **Font Weight**: `400` / `font-normal`
- **Color**: `#605e5c` (gray)

---

### **MasterToolbar (Primary Actions)**
> ⚠️ **Note**: No more "Add New" buttons in page headers. All primary actions (New, Edit, Save, Cancel) are handled through the `MasterToolbar` component.

```tsx
<MasterToolbar 
    viewId="PAGE_ID" 
    mode={mode} 
    onAction={handleAction} 
/>
```
- **Action Pattern**: Add through "+" button in the toolbar ONLY.
- **Shortcut**: `F2` for New.

### **Search Input**
```tsx
<input
    type="text"
    placeholder="Search records..."
    className="px-3 py-1.5 border border-gray-300 rounded-sm text-sm w-64"
/>
```
- **Font Size**: `14px` / `text-sm`
- **Padding**: `px-3 py-1.5`
- **Border**: `1px solid #d1d1d1` / `border-gray-300`
- **Border Radius**: `2px` / `rounded-sm`

---

### **Filter Dropdown**
```tsx
<select className="px-3 py-1.5 border border-gray-300 rounded-sm text-sm">
    <option>All Status</option>
</select>
```
- **Font Size**: `14px` / `text-sm`
- **Padding**: `px-3 py-1.5`
- **Border**: `1px solid #d1d1d1` / `border-gray-300`

---

### **Table Headers**
```tsx
<th className="p-3 text-xs uppercase tracking-wider text-left bg-[#f3f2f1] text-[#323130]">
    Customer Name
</th>
```
- **Font Size**: `12px` / `text-xs`
- **Font Weight**: `600` / `font-semibold`
- **Text Transform**: `uppercase`
- **Letter Spacing**: `0.05em` / `tracking-wider`
- **Background**: `#f3f2f1` (light gray)
- **Color**: `#323130` (medium gray)
- **Padding**: `12px` / `p-3`

---

### **Table Cells**
```tsx
<td className="p-3 text-sm text-[#323130]">
    John Doe
</td>
```
- **Font Size**: `14px` / `text-sm`
- **Color**: `#323130` (medium gray)
- **Padding**: `12px` / `p-3`

---

### **Row Hover State**
```tsx
<tr className="border-b border-[#f3f2f1] hover:bg-[#f3f9ff]">
```
- **Border**: `1px solid #f3f2f1` (light gray)
- **Hover Background**: `#f3f9ff` (light blue)

---

## 📝 **FORM PAGES / MODALS**

### **Modal Title**
```tsx
<h2 className="text-xl font-semibold text-[#201f1e]">
    Add New Record
</h2>
```
- **Font Size**: `20px` / `text-xl`
- **Font Weight**: `600` / `font-semibold`
- **Color**: `#201f1e` (dark gray)

---

### **Form Section Header**
```tsx
<h3 className="text-base font-semibold text-[#323130] mb-4">
    Contact Information
</h3>
```
- **Font Size**: `16px` / `text-base`
- **Font Weight**: `600` / `font-semibold`
- **Color**: `#323130` (medium gray)
- **Margin Bottom**: `16px` / `mb-4`

---

### **Field Labels (Standard)**
```tsx
<label className="text-xs font-semibold text-[#605e5c] uppercase">
    Entity Name *
</label>
```
- **Font Size**: `12px` / `text-xs`
- **Font Weight**: `600` / `font-semibold`
- **Color**: `#605e5c` (gray)
- **Text Transform**: `uppercase`
- **Required Indicator**: `*` (asterisk)

---

### **Field Labels (Inline)**
```tsx
<label className="text-sm font-medium text-[#323130]">
    Email Address
</label>
```
- **Font Size**: `14px` / `text-sm`
- **Font Weight**: `500` / `font-medium`
- **Color**: `#323130` (medium gray)

---

### **Text Input (Standard)**
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

---

### **Text Input (Underline Style)**
```tsx
<div className="flex items-center gap-2 border-b border-[#8a8886] hover:border-[#323130] pb-1">
    <Building2 size={14} className="text-[#0078d4]" />
    <input
        type="text"
        className="w-full outline-none bg-transparent font-medium text-[#0078d4]"
    />
</div>
```
- **Font Size**: `14px` / `text-sm`
- **Font Weight**: `500` / `font-medium`
- **Color**: `#0078d4` (blue) - for lookup fields
- **Border**: Bottom only, `1px solid #8a8886`
- **Hover Border**: `#323130` (dark gray)
- **Icon Size**: `14px`

---

### **Text Input (Read-Only)**
```tsx
<input
    type="text"
    readOnly
    className="w-full p-3 outline-none bg-gray-50 text-center text-gray-600"
/>
```
- **Font Size**: `14px` / `text-sm`
- **Color**: `#6b7280` / `text-gray-600`
- **Background**: `#f9fafb` / `bg-gray-50`
- **Padding**: `12px` / `p-3`

---

### **Textarea**
```tsx
<textarea
    rows={4}
    className="w-full px-3 py-2 border border-gray-300 rounded-sm text-sm focus:border-[#0078d4] focus:ring-1 focus:ring-[#0078d4] outline-none"
/>
```
- **Font Size**: `14px` / `text-sm`
- **Padding**: `px-3 py-2`
- **Border**: `1px solid #d1d1d1` / `border-gray-300`
- **Focus Border**: `#0078d4` (blue)

---

### **Select Dropdown (LOV)**
```tsx
<select className="w-full px-3 py-2 border border-gray-300 rounded-sm text-sm focus:border-[#0078d4] focus:ring-1 focus:ring-[#0078d4] outline-none">
    <option>Select...</option>
</select>
```
- **Font Size**: `14px` / `text-sm`
- **Padding**: `px-3 py-2`
- **Border**: `1px solid #d1d1d1` / `border-gray-300`
- **Focus Border**: `#0078d4` (blue)

---

### **Checkbox**
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

---

### **Radio Button**
```tsx
<label className="flex items-center gap-2">
    <input
        type="radio"
        className="w-4 h-4 text-[#0078d4] border-gray-300 focus:ring-[#0078d4]"
    />
    <span className="text-sm text-[#323130]">Individual</span>
</label>
```
- **Radio Size**: `16px` / `w-4 h-4`
- **Checked Color**: `#0078d4` (blue)
- **Border**: `1px solid #d1d1d1` / `border-gray-300`
- **Label Font Size**: `14px` / `text-sm`
- **Label Color**: `#323130` (medium gray)

---

### **Date Input**
```tsx
<input
    type="date"
    className="w-full px-3 py-2 border border-gray-300 rounded-sm text-sm focus:border-[#0078d4] outline-none"
/>
```
- **Font Size**: `14px` / `text-sm`
- **Padding**: `px-3 py-2`
- **Border**: `1px solid #d1d1d1` / `border-gray-300`

---

### **Number Input**
```tsx
<input
    type="number"
    className="w-full p-3 outline-none bg-transparent text-right focus:bg-white"
/>
```
- **Font Size**: `14px` / `text-sm`
- **Text Align**: `right` / `text-right`
- **Padding**: `12px` / `p-3`
- **Focus Background**: `white` / `bg-white`

---

## 🔘 **BUTTONS**

### **Primary Button**
```tsx
<button
    style={{
        backgroundColor: 'var(--button-primary-bg)',      /* #ff6600 (orange) */
        color: 'var(--button-primary-text)'               /* #ffffff (white) */
    }}
    className="px-3 py-1.5 font-medium rounded-sm"
    onMouseEnter={(e) => {
        e.currentTarget.style.backgroundColor = 'var(--button-primary-hover-bg)';  /* #e65c00 */
    }}
    onMouseLeave={(e) => {
        e.currentTarget.style.backgroundColor = 'var(--button-primary-bg)';
    }}
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

---

### **Secondary Button**
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

### **Link Button**
```tsx
<button className="text-[#0078d4] hover:underline font-medium text-sm">
    View Details
</button>
```
- **Text Color**: `#0078d4` (blue)
- **Hover**: `underline`
- **Font Size**: `14px` / `text-sm`
- **Font Weight**: `500` / `font-medium`

---

### **Icon Button**
```tsx
<button className="p-2 hover:bg-[#f3f2f1] rounded-full">
    <Edit3 size={16} className="text-[#605e5c]" />
</button>
```
- **Padding**: `8px` / `p-2`
- **Icon Size**: `16px`
- **Icon Color**: `#605e5c` (gray)
- **Hover Background**: `#f3f2f1` (light gray)
- **Border Radius**: `50%` / `rounded-full`

---

## 📊 **TABLES & GRIDS**

### **Table Container**
```tsx
<div className="border border-[#edebe9] rounded-sm overflow-hidden">
    <table className="w-full border-collapse">
```
- **Border**: `1px solid #edebe9` (light gray)
- **Border Radius**: `2px` / `rounded-sm`
- **Border Collapse**: `collapse`

---

### **Table Header Row**
```tsx
<thead className="bg-[#f3f2f1] text-[#323130]">
    <tr className="text-xs uppercase tracking-wider text-left border-b border-[#edebe9]">
```
- **Background**: `#f3f2f1` (light gray)
- **Text Color**: `#323130` (medium gray)
- **Font Size**: `12px` / `text-xs`
- **Text Transform**: `uppercase`
- **Letter Spacing**: `0.05em` / `tracking-wider`
- **Border Bottom**: `1px solid #edebe9`

---

### **Table Header Cell**
```tsx
<th className="p-3 border-l border-[#edebe9]">
    Customer Name
</th>
```
- **Padding**: `12px` / `p-3`
- **Border Left**: `1px solid #edebe9` (for cell separation)

---

### **Table Body Row**
```tsx
<tr className="border-b border-[#f3f2f1] hover:bg-[#f3f9ff]">
```
- **Border Bottom**: `1px solid #f3f2f1` (light gray)
- **Hover Background**: `#f3f9ff` (light blue)

---

### **Table Data Cell**
```tsx
<td className="p-3 text-sm text-[#323130]">
    John Doe
</td>
```
- **Padding**: `12px` / `p-3`
- **Font Size**: `14px` / `text-sm`
- **Color**: `#323130` (medium gray)

---

### **Table Cell (Numeric)**
```tsx
<td className="p-3 text-sm text-right font-medium">
    $1,234.56
</td>
```
- **Text Align**: `right` / `text-right`
- **Font Weight**: `500` / `font-medium`

---

### **Table Cell (Muted)**
```tsx
<td className="p-3 text-sm text-[#a19f9d]">
    N/A
</td>
```
- **Color**: `#a19f9d` (light gray) - for empty/placeholder values

---

## 🏷️ **STATUS BADGES**

### **Status Badge (Generic)**
```tsx
<span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-{color}-100 text-{color}-800">
    ACTIVE
</span>
```
- **Padding**: `px-2.5 py-0.5` (10px horizontal, 2px vertical)
- **Border Radius**: `9999px` / `rounded-full`
- **Font Size**: `12px` / `text-xs`
- **Font Weight**: `500` / `font-medium`

---

### **Status Badge (Uppercase)**
```tsx
<span className="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase bg-green-100 text-green-800">
    COMPLETED
</span>
```
- **Padding**: `px-2 py-0.5` (8px horizontal, 2px vertical)
- **Font Size**: `10px` / `text-[10px]`
- **Font Weight**: `700` / `font-bold`
- **Text Transform**: `uppercase`

---

### **Status Colors**

| Status | Background | Text |
|--------|------------|------|
| **DRAFT** | `bg-gray-100` | `text-gray-700` |
| **ACTIVE** | `bg-green-100` | `text-green-800` |
| **SUBMITTED** | `bg-yellow-100` | `text-yellow-700` |
| **APPROVED** | `bg-blue-100` | `text-blue-700` |
| **IN_TRANSIT** | `bg-purple-100` | `text-purple-700` |
| **RECEIVED** | `bg-teal-100` | `text-teal-700` |
| **COMPLETED** | `bg-green-100` | `text-green-700` |
| **CANCELLED** | `bg-red-100` | `text-red-700` |
| **INACTIVE** | `bg-gray-100` | `text-gray-800` |
| **BLACKLISTED** | `bg-red-100` | `text-red-800` |

---

## 🎨 **COLORS PALETTE**

### **Primary Colors**
```css
--primary-blue: #0078d4      /* Links, focus states, icons */
--primary-orange: #ff6600    /* Primary buttons */
--primary-orange-hover: #e65c00  /* Primary button hover */
```

### **Text Colors**
```css
--text-dark: #201f1e         /* Page titles, headings */
--text-medium: #323130       /* Body text, labels */
--text-gray: #605e5c         /* Secondary text, field labels */
--text-light: #a19f9d        /* Placeholder, disabled text */
```

### **Background Colors**
```css
--bg-white: #ffffff          /* Cards, modals, tables */
--bg-light: #faf9f8          /* Page background */
--bg-gray: #f3f2f1           /* Table headers, hover states */
--bg-blue-light: #f3f9ff     /* Row hover (blue tint) */
```

### **Border Colors**
```css
--border-light: #edebe9      /* Card borders, dividers */
--border-medium: #d1d1d1     /* Input borders */
--border-dark: #8a8886       /* Underline inputs */
--border-focus: #0078d4      /* Focus state */
```

### **Status Colors**
```css
/* Green (Success/Active/Completed) */
--green-100: #d1fae5
--green-700: #047857
--green-800: #065f46

/* Yellow (Warning/Submitted) */
--yellow-100: #fef3c7
--yellow-700: #b45309

/* Blue (Info/Approved) */
--blue-100: #dbeafe
--blue-700: #1d4ed8

/* Red (Error/Cancelled/Blacklisted) */
--red-100: #fee2e2
--red-700: #b91c1c
--red-800: #991b1b

/* Purple (In Transit) */
--purple-100: #e9d5ff
--purple-700: #7e22ce

/* Teal (Received) */
--teal-100: #ccfbf1
--teal-700: #0f766e

/* Gray (Draft/Inactive) */
--gray-100: #f3f4f6
--gray-700: #374151
--gray-800: #1f2937
```

---

## ⚡ **QUICK REFERENCE**

### **Common Patterns**

#### **Page Header**
```tsx
<div className="px-6 py-3 border-b border-[#edebe9] bg-white">
    <h1 className="text-xl font-semibold text-[#201f1e]">
        Page Title
    </h1>
</div>
```

#### **Form Field**
```tsx
<div className="space-y-1">
    <label className="text-xs font-semibold text-[#605e5c] uppercase">
        Field Label *
    </label>
    <input
        type="text"
        className="w-full px-3 py-2 border border-gray-300 rounded-sm text-sm focus:border-[#0078d4] outline-none"
    />
</div>
```

#### **Action Button Group (Modals Only)**
> ⚠️ **Note**: Page-level Save/Cancel actions must use the `MasterToolbar`. Physical buttons are reserved for Modal footers.

```tsx
<div className="flex items-center gap-2">
    <button className="px-3 py-1.5 bg-[#ff6600] text-white font-medium rounded-sm">
        Save
    </button>
    <button className="px-3 py-1.5 hover:bg-[#edebe9] rounded-sm text-[#323130] font-medium">
        Cancel
    </button>
</div>
```

#### **Status Badge**
```tsx
<span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
    ACTIVE
</span>
```

---

## 📝 **NOTES FOR AGENT E**

1.  **Always use CSS variables** for primary button colors (`var(--button-primary-bg)`)
2.  **Typography levels** are defined in `layoutConfig.ts` - use them for consistency
3.  **Border radius** is always `2px` (`rounded-sm`) except for badges (`rounded-full`)
4.  **Focus states** always use `#0078d4` (blue) with `outline-none`
5.  **Hover states** for secondary elements use `#edebe9` (light gray)
6.  **Icon sizes** are typically `14px` or `16px`
7.  **Padding** for buttons is `px-3 py-1.5` (12px x 6px)
8.  **Table padding** is `p-3` (12px all sides)
9.  **Status badges** use `100` background and `700/800` text colors
10. **Uppercase labels** use `text-xs font-semibold text-[#605e5c] uppercase`

---

**Last Updated**: 2026-01-07 20:47 IST  
**Reference**: Generic ERP UI Patterns (Master Setup, Transaction Forms)  
**Maintained By**: Astra (AI Coding Assistant)
