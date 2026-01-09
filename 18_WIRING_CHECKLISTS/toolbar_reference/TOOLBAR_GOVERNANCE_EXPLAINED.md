# 🎓 ERP Toolbar Governance & Behavior

This document records the core architectural understanding of the Olivine ERP Toolbar system, as established during the generalization of steering documentation.

---

## 🚀 CORE PRINCIPLES

### 1. Implementation of Toolbar Control (Django Models)
The system is anchored in a **Character-Based Registry** within the backend (`user_management` models):
*   **`ERPToolbarControl`**: Defines the "Super Strings" at the module level (e.g., RETAIL, HRM).
*   **`ERPMenuItem`**: The granular control point. Each screen uses an `applicable_toolbar_config` string (e.g., `NESCKVRT`).
*   **Registry Rule**: If a character (action) is not in this string, it cannot exist on that page, regardless of developer intent or user permission.
*   **Governance**: Admin Proxies in Django provide a "No-Code" way to toggle UI capabilities across the entire platform.

### 2. User & Permissions Integration
Permissions in Olivine follow a **Subtractive Intersection** logic:
*   **Intersecting Rights**: A button is visible ONLY if it exists in BOTH the Page's `applicable_toolbar_config` AND the User's `toolbar_override`.
*   **Centralized Control**: This allows administrators to strip "Delete" or "Authorize" capabilities from specific users or roles globally, without ever touching the React frontend code.

### 3. Display & Control in List Pages (VIEW Mode)
In list views, the toolbar acts as the **Primary Command Center**:
*   **Mode Visibility**: The UI initializes in `VIEW` mode.
*   **Filtering**: The toolbar applies a visibility filter that hides "Save" and "Cancel" (contextually irrelevant) and focuses on "New", "Search", "Refresh", and "Filter".
*   **Unified Actions**: It eliminates the need for "Add New" or "Export" buttons inside the page content, keeping the whitespace clean and the interaction standardized.

### 4. The "+" Flow (Switching to NEW Mode)
Clicking the **"+" (New)** icon (or pressing `F2`) triggers a profound UI transformation:
*   **State Shift**: The page state switches to `mode="NEW"`.
*   **Toolbar Swap**: The `MasterToolbar` detects this and immediately re-routes. It hides navigation/list tools and reveals **"Save (S)"** and **"Cancel (C)"**.
*   **Workflow Enforcement**: This prevents "UI Limbo." The user is forced to either commit the transaction or explicitly cancel it to return to the list.

### 5. The Role of `viewId`
The `viewId` is the **Handshake Key** between the SPA and the Database:
*   **Dynamic Mapping**: It allows the frontend to be generic. Every page uses the same React component; they only differ by the `viewId` sent to the backend.
*   **Maintenance**: If a business rule changes (e.g., "We now need to allow Exporting on the Employee List"), an admin simply adds `Y` to the `applicable_toolbar_config` for that `viewId` in the database.

### 6. Advanced Actions: Auth, Amend, & Clone
These characters handle complex transaction lifecycles:
*   **`Authorize (Z/A)`**: Point of no return. Finalizes a record, usually making it read-only and triggering accounting entries.
*   **`Amend (W)`**: Purposefully breaks the "Read-Only" state of an authorized document, creating an audit trail of the correction.
*   **`Clone (L)`**: A productivity booster. It triggers the **"+" Flow** but prepopulates data from the currently viewed record, perfect for recurring tasks.

### 7. Lookup Enablement Policy
Lookups (`!`, `@`, `#` for Customer, Supplier, Item) are **Context-Aware**:
*   **Strategic Hiding**: These are hidden in `VIEW` mode to reduce visual clutter.
*   **Strategic Revealing**: They automatically appear in **`NEW` and `EDIT` modes**.
*   **Standardized Shortcuts**: Using `F11`/`F12` across every form in the ERP provides a rhythmic, high-speed data entry experience for power users.

---

## ❓ DETAILED QA (Questions for the User)

**Astra's Questions for USER Verification:**

1.  **Business Logic vs. Permission**: If a user has "Delete" permission (`D`), but a record is in `STATUS = 'APPROVED'` (which should protect it from deletion), should the `isActionDisabled` logic be handled entirely in the `MasterToolbar` config fetch, or should the individual page pass a "soft-disable" prop based on local record status?
A : Based on the record status, if permission exists it can be transition to open/reopen..

2.  **Amendment Workflow**: When an "Amend" (`W`) action is triggered, should it simply flip the UI to `EDIT` mode, or do we need a specific `AMEND` mode to handle specialized validation or versioning logic?
A : Amend should be applicable for Qty changes, that too for Purchase order and Sales Order qty only , not for inventory , POS billing.
We can have a later a business rules page, which will define all this
like..
PO Amendment allowed [] if yes then what is allowed Qty[], Supplier[] ... like, the amendment would be applicable for authorized documents only.

3.  **Clone Data Integrity**: Should the "Clone" action automatically strip out unique identifiers (like `ID`, `TransactionNumber`) and dates, or should we rely on the backend serializer's `create` method to handle the "rebirth" of the record?
A: Clone is the to copy as new, appliacable only for Sales and Purchase Orders only.

4.  **Multi-Select Behavior**: In "List View", if a user checks multiple rows, many toolbar actions (Edit, Clone, Amend) become ambiguous. Should the toolbar automatically disable single-row actions when `selection.length > 1`?
A: Multi select can be applicable for Auth, Delete only, if multiple rows are selected then if view, or , new , edit pressed, "This is not allowed.." like that message should be shown.

5.  **Shortcut Conflicts**: Are there any specific OS-level or browser-level shortcuts we should avoid? (e.g., `F1` is often Help, `F5` is Refresh). Should the toolbar's `K` (Clear) always map to `F5`, or should we use something less likely to trigger a page browser reload?
A: within the application we can use F2 to F12, outside the application we can use F1 to F12.
---
**Maintained By**: Astra (ERP Platform Development Owner)  
**Last Updated**: 2026-01-09 13:40 IST
