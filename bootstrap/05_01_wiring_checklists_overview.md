# 🔧 WIRING CHECKLISTS - UI Implementation Guides

⚠️ **IMPORTANT: READ THIS FIRST**

## What is This Folder?

**Step-by-step implementation checklists** for wiring UI components to backend APIs.

These are **practical, hands-on guides** - not functional templates or governance rules.

---

## 🎯 NOT the Same as 14_UI_CANON

| **Aspect** | **14_UI_CANON** | **18_WIRING_CHECKLISTS** |
|------------|-----------------|--------------------------|
| **Purpose** | Standards, rules, templates | Implementation steps |
| **Content** | WHAT to build, WHY it works | HOW to wire it up |
| **Focus** | Business logic, patterns | API integration, UI setup |
| **Example** | "Calculate line totals" | "Connect service.getAll() to table" |
| **When to Use** | Understanding requirements | Implementing features |

---

## 📚 Quick Decision Tree

```
Need to understand UI standards?  → Go to: 14_UI_CANON/04_Frontend_UI_Canon.md
Need to understand transaction patterns?  → Go to: 14_UI_CANON/TXN-M.md
Need to implement a master data list page?  → You're in the right place! Use: MASTER_DATA_WIRING.md
Need to implement a transaction form?  → You're in the right place! Use: TRANSACTION_FORM_WIRING.md
Need to add workflow actions?  → You're in the right place! Use: WORKFLOW_WIRING.md
```

---

## 📁 Files in This Folder

### `MASTER_DATA_WIRING.md`

**For**: Employee, Department, Account, Contact, Category (Master Data)

**Reference Implementations**:
- `frontend/src/pages/SetupPage.tsx` (Generic Pattern)
- `frontend/apps/shared/pages/MasterDataLanding.tsx`

**Covers**:
- ✅ List page setup
- ✅ MasterToolbar integration (Add/New/Edit)
- ✅ Search bar + filters
- ✅ Data table with gradient headers
- ✅ Edit/delete actions
- ✅ Company scoping

---

### `TRANSACTION_FORM_WIRING.md`

**For**: Leave Request, Attendance, Lead, Opportunity, Invoice (Transaction Forms)

**Reference Implementation**:
- `frontend/apps/shared/pages/TransactionFormPage.tsx`

**Covers**:
- ✅ TransactionToolbar integration
- ✅ Header section with status badge
- ✅ Line items grid (editable)
- ✅ Lookup modals (F12 integration)
- ✅ Workflow actions (save, submit, approve)
- ✅ Real-time calculations

---

### `WORKFLOW_WIRING.md`

**For**: Status machines, Workflow actions, Business rules, Validation

**Reference Implementations**:
- `backend/domain/shared/views.py` (BaseWorkflowViewSet)
- `frontend/src/services/workflowService.ts`

**Covers**:
- ✅ Status state machine definition
- ✅ Workflow action handlers (backend)
- ✅ Workflow action methods (frontend)
- ✅ Validation rules
- ✅ Authorization & scoping
- ✅ Error handling

---

## 🔗 Must Read First (From 14_UI_CANON)

Before using these checklists, familiarize yourself with:

1. **Onboarding**: `.steering/14_UI_CANON/01_Onboarding_Context.md`
2. **UI Standards**: `.steering/14_UI_CANON/04_Frontend_UI_Canon.md`
3. **Governance**: `.steering/governance.md`
4. **Functional Templates**: `.steering/14_UI_CANON/TXN-M.md`, `MST-M.md`

---

## 🎯 How to Use These Checklists

1. **Choose the right checklist** based on what you're building
2. **Read the reference implementation** mentioned in the checklist
3. **Follow the steps sequentially** - they're ordered for a reason
4. **Check off each item** as you complete it
5. **Test thoroughly** using the testing section

---

## ✅ Success Criteria

Your implementation is complete when:
- ✅ All checklist items are checked
- ✅ UI adheres to standards in 14_UI_CANON
- ✅ Company scoping works correctly
- ✅ Error handling is robust
- ✅ Loading states are implemented
- ✅ All tests pass

---

## 📞 Need Help?

- **UI Standards Questions**: Check `14_UI_CANON/`
- **Business Logic Questions**: Check functional templates (`TXN-M.md`, `MST-M.md`)
- **Architecture Questions**: Check `governance.md`
- **Implementation Questions**: You're in the right place!

---

**Last Updated**: 2026-01-07  
**Maintainer**: Astra (ERP Platform Development Owner)
