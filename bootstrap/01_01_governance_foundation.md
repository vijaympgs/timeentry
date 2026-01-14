# ENTERPRISE ERP PLATFORM — MASTER GOVERNANCE

> **Status:** FINAL / AUTHORITATIVE / ENFORCEABLE  
> **Audience:** HRM & CRM Engineers, UI Agents, Backend Agents  
> **Rule:** This document is the SINGLE source of truth. Any deviation is a governance violation.

---

## 🎯 PURPOSE & GOVERNANCE

### Purpose
Consolidates **ALL architectural, governance, UI, and execution rules** for HRM and CRM development in the Olivine Enterprise ERP Platform.

Goals:
- Zero ambiguity for new agents
- Copy–paste mergeability
- UI and UX consistency
- Long-term architectural integrity

This is **not guidance**. This is a **contract**.

---

## 🏗️ ENTERPRISE SHELL & APP ISOLATION

### Enterprise Shell
```
erp-platform/
├── retail/
├── hrm/
├── crm/
├── fms/
└── common/
```

Rules:
- Each app is independently developable
- Apps may live on different machines
- Final integration is folder-level copy–paste
> COPY → PASTE → RUN is mandatory. If this fails, the architecture is INVALID.

---

## 💻 TECHNOLOGY STACK

### Backend
- Python 3.x
- Django (modular apps)
- Django REST Framework
- PostgreSQL

### Frontend
- Vite
- React (SPA)
- TypeScript (strict)
- Tailwind CSS (Olivine UI canon)

---

## 📁 EXECUTION FOLDER STRUCTURE

```
retail-erp-platform/
├── hrm/
│   ├── backend/
│   │   ├── models/
│   │   ├── serializers/
│   │   ├── views/
│   │   ├── urls.py
│   │   └── migrations/
│   └── frontend/
│       ├── pages/
│       ├── modules/
│       ├── services/
│       ├── routes/
│       └── templates/
├── crm/
│   ├── backend/
│   └── frontend/
├── common/
│   ├── domain/
│   ├── auth/
│   ├── permissions/
│   ├── ui-canon/
│   └── shared-services/
```

Rules:
- No cross-app imports
- Shared logic ONLY via common/
- Folder structure is NON-NEGOTIABLE

---

## 🔒 DOMAIN OWNERSHIP (LOCKED)

### Platform / common (READ-ONLY CONTRACTS)
- Company → `common/domain/models.py`
- User → `common/auth/`
- Permission → `common/permissions/`
- Role → `common/permissions/`
- AuthPolicy → `common/auth/`
- ItemMaster (base) → `common/domain/`
- Supplier (base) → `common/domain/`
- UnitOfMeasure → `common/domain/`

### HRM Domain
- Employee → `hrm/backend/models/`
- Department → `hrm/backend/models/`
- Position → `hrm/backend/models/`
- Operates strictly at Company level

### CRM Domain
- Lead → `crm/backend/models/`
- Opportunity → `crm/backend/models/`
- Account → `crm/backend/models/`
- Operates strictly at Company level

### FMS Domain
- Finance → `fms/backend/models/`
- Location → `fms/backend/models/` (RETAIL ONLY)

❌ NO Location references allowed in HRM/CRM.

---

## 🤝 MERGEABILITY CONTRACT

Rules:
- HRM / CRM must run without Retail present
- Copy–paste of hrm/ or crm/ must work
- No refactor after merge

Violation = architecture failure.

---

## 🎨 UI CANON (OLIVINE RULE SET)

### Core Principles
- Enterprise-first
- Dense, functional UI
- No decorative design
- Predictability over creativity

### Layout Rules
- Fixed left sidebar
- Header for global actions only
- Content scrolls

### Transaction Toolbar (MANDATORY)
- Fixed position
- Save / Cancel / Reset
- Workflow actions
- Keyboard shortcuts

### Lookup Rules
- ALWAYS right-side panel
- NEVER inline in form
- Reusable lookup components only

### Visual Identity Tokens

**Typography:**
- Primary Font: `Inter` (UI, Body)
- Secondary Font: `JetBrains Mono` (Code, IDs, Data)
- Sizes: `text-sm` for fields, `text-xs` for labels

**Color Palette:**
| Token | Hex | Usage |
|-------|-----|-------|
| `nexus-primary-600` | `#6d4de6` | Primary Actions / Links |
| `nexus-primary-700` | `#5d3dcb` | Hover States |
| `nexus-gray-50` | `#fafafa` | Page Backgrounds |
| `nexus-gray-100` | `#f5f5f5` | Panel Backgrounds |
| `nexus-gray-900` | `#212121` | Heavy Text / Dark Mode |
| `nexus-error-600` | `#db2777` | Validation Errors |
| `nexus-success-600` | `#059669` | Success States |

**Shape:**
- Inputs: `rounded-none` (Legacy/Enterprise feel)
- Cards: `rounded-sm` or `rounded-md` (Subtle)
- Buttons: `rounded-none` (Action Bars) or `rounded-sm` (Modals)
- Shadows: `shadow-nexus-sm` (Cards), `shadow-2xl` (Modals/Popovers)

**Animation:**
- Speed: `duration-180` (Normal) or `duration-120` (Fast)
- Easing: `ease-out`
- Transitions: Use `transition-all` on interactive elements

---

## 📱 SCREEN TYPES

### Master Screens
- Form-first
- Toolbar-driven CRUD
- No inline tables

### Transaction Screens
- Header context
- Line grid
- Summary section
- Workflow toolbar

### Configuration Screens
- Grouped sections
- Explicit save/reset
- No auto-save

---

## ✅ FORM & VALIDATION RULES

- Explicit required fields
- Blur-level soft validation
- Save-level hard validation
- Read-only clearly indicated
- No hidden mandatory fields

---

## 📋 SIDEBAR & MENU GROUPING

Rules:
- Sidebar reflects domain ownership
- HRM & CRM menus operate at Company level
- NO Retail menus duplicated
- ONE UI per master (no duplicates)

---

## ⚠️ DO / DO NOT (ENFORCEMENT)

### DO
- Follow canon strictly
- Reuse templates
- Ask before deviating

### DO NOT
- Rebrand UI
- Create alternate layouts
- Duplicate masters
- Ignore rules for speed

---

## 🔍 QUALITY & AUDIT GATES

Before approval:
- Canon compliance
- No Location leakage
- No Licensing masters
- Copy–paste merge test passes

---

## 📞 COMMUNICATION PROTOCOL (MANDATORY)

### Response Format Rules
- **Standard Tasks**: Keep responses to 1-2 simple lines maximum
- **Onboarding/Overview**: Detailed responses allowed for initial platform understanding
- **Development Tasks**: Concise, action-oriented responses only
- **Error Reporting**: Brief description + immediate next step

**Violation**: Excessive verbosity = **Governance Breach**

## 🏁 FINAL LOCK

> Licensing controls access.  
> Company anchors all domains.  
> Retail owns Location.  
> HRM and CRM remain clean, isolated, and mergeable.
> Communication follows concise protocol.

Any violation is a **governance breach**.

---

## 🏢 CRITICAL MODEL REFERENCES

### Company Model (MANDATORY SHARED)

> Since all apps operate at the Legal Entity level, you MUST link your models to the Company.

- **Canonical Source:** `common/domain/models.py`
- **Reference Strategy:** Use Lazy String Reference to avoid circular imports.
  - ✅ `company = models.ForeignKey('domain.Company', ...)`
  - ❌ `from common.domain.models import Company` (Avoid)
- **Constraint:** **READ-ONLY**. You must not modify the Company model.

### Location Model (STRICTLY FORBIDDEN)

> Location is a Retail Operations concept.

- **Rule:** HRM and CRM must **NEVER** import or reference `Location`.
- **Violation:** Any Reference to `Location` = **Immediate Audit Failure**.

---

**END OF MASTER GOVERNANCE**
