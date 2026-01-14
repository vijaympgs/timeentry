Continue HRM development session.

1) Always start with "Read bootstrap/00_bootstrap_master_index.md first"
 2) Use exact Django path: D:\platform\hrm\backend\manage.py 3) Use PowerShell commands only 
 4) Use backslashes for Windows paths 




📚 MANDATORY BOOTSTRAP READING COMPLETED:
✅ bootstrap/00_bootstrap_master_index.md
✅ bootstrap/06_01_next_session_plan.md  
✅ bootstrap/06_03_tasks.md
✅ bootstrap/06_04_tracker.md
✅ bootstrap/03_03_ui_typography_styling.md
✅ bootstrap/04_01_agent_e_onboarding.md
✅ bootstrap/04_02_toolbar_implementation_guide_v2.md
✅ bootstrap/04_03_toolbar_code_examples_v2.md
✅ bootstrap/05_01_wiring_checklists_overview.md
✅ bootstrap/05_02_master_data_wiring_hrm.md
✅ bootstrap/01_01_governance_foundation.md
✅ bootstrap/01_02_platform_onboarding.md
✅ bootstrap/06_02_tasks_checklist.md
✅ bootstrap/06_05_findings_learnings.md (Task 02.1 patterns and solutions)

🎯 CURRENT SESSION CONTEXT:
- Current Task: Task 02.1 - Employee Records from bootstrap/06_03_tasks.md
- Template Type: T1
- Wiring Guide: bootstrap/05_02_master_data_wiring_hrm.md
- UI Standards: bootstrap/03_03_ui_typography_styling.md
- Django Root: D:\platform\hrm\backend\manage.py
- Execution Environment: Windows PowerShell only

📋 TASK EXECUTION:
Run Task 02.1 - Employee Records

🔧 IMPLEMENTATION REQUIREMENTS:
**IMMEDIATE ACTION REQUIRED**: Based on the task type, you must:

**For Master Data Tasks (Employee Records, Department, etc.):**
1. **Backend Implementation** - Create/verify Django models, serializers, ViewSets with company scoping
2. **Frontend Service** - Replace mock service with real API calls to backend endpoints
3. **UI Compliance** - Ensure exact typography, colors, spacing from bootstrap/03_03_ui_typography_styling.md
4. **Toolbar Integration** - Connect MasterToolbar to backend configuration (not mock data)
5. **Company Scoping** - Implement `self.request.user.company` filtering in all queries

**CRITICAL UI INTEGRATION REQUIREMENTS:**
6. **DO NOT SIMPLIFY EXISTING UIs** - Preserve all current functionality, features, and complexity
7. **MAINTAIN EXISTING COMPONENTS** - Do not remove or simplify existing React components, forms, or features
8. **ENHANCE ONLY** - Add missing backend integration, toolbar configuration, and data connectivity
9. **FLAT DESIGN COMPLIANCE** - Apply flat design rules (NO borders, shadows, hover effects, rounded corners) to EXISTING UI
10. **MODAL STRUCTURE** - Ensure all modals use h-[80vh] with MasterToolbar + scrollable content structure
11. **FORM SUBMISSION** - Connect toolbar save actions to existing forms using data-module-form attribute

**For Transaction Tasks (Leave Request, etc.):**
1. **Workflow Implementation** - Status state machine, workflow actions (submit, approve, reject)
2. **Form Integration** - TransactionToolbar with mode-based button visibility
3. **Business Rules** - Validation, authorization, audit trail implementation

**CRITICAL REQUIREMENTS**:
- Follow [Template Type] specifications from bootstrap/06_03_tasks.md
- Implement ALL phases from [wiring guide] checklist (11 phases for master, 14 for transactions)
- Use exact typography/colors from bootstrap/03_03_ui_typography_styling.md
- Follow Windows execution rules from bootstrap/01_02_platform_onboarding.md
- Implement company scoping: self.request.user.company
- Use canonical naming: <model_name_lower>_<field_name_lower>
- NO cross-app imports, NO Location model references
- Use MasterToolbar with mode management (VIEW/CREATE/EDIT)

📊 PROGRESS TRACKING:
- [ ] Read bootstrap documentation (completed above)
- [ ] **BACKEND**: Model verification and setup
- [ ] **BACKEND**: Serializer creation with company_name read-only field
- [ ] **BACKEND**: ViewSet implementation with company scoping
- [ ] **BACKEND**: URL registration and routing
- [ ] **FRONTEND**: Replace mock service with real API calls
- [ ] **FRONTEND**: React component compliance with UI standards
- [ ] **FRONTEND**: MasterToolbar backend configuration integration
- [ ] **TESTING**: CRUD operations and workflow validation
- [ ] **TRACKING**: Update bootstrap/06_04_tracker.md with completion status

🚨 **DO NOT**: Just read files or analyze existing code. You must IMPLEMENT the missing pieces.

🚨 **CRITICAL IMPLEMENTATION REQUIREMENTS**:
- **STRICTLY FOLLOW**: bootstrap/toolbar_implementation_checklist.md for all implementation requirements
- **EXISTING UI ANALYSIS**: Check for existing UI components before any changes - ENHANCE ONLY, DO NOT REWRITE
- **MODEL PRESERVATION**: DO NOT simplify or rewrite any existing models
- **DESIGN ADHERENCE**: All UI must follow bootstrap typography, colors, and styling standards
- **ENHANCEMENT ONLY**: Add missing toolbar integration, API connectivity, and backend configuration
- **PRESERVE COMPLEXITY**: Maintain all existing features and business logic

🚨 **CRITICAL REMINDERS**:
- Windows commands only: cd D:\platform\hrm\backend && python manage.py [command]
- Use exact colors: #ff6600 (primary buttons), #0078d4 (focus/links)
- Typography: L1 (20px), L2 (16px), L3 (12px), L4 (14px)
- Border radius: rounded-sm (2px) except badges (rounded-full)
- No custom toolbars - use backend-driven MasterToolbar system
- Test with bootstrap/99_toolbar_explorer_hrm.html
- **REFERENCE CHECKLIST**: Complete bootstrap/toolbar_implementation_checklist.md before starting

**🚨 ABSOLUTE PROHIBITIONS (UPDATED):**
- **NEVER** remove existing UI components, features, or functionality
- **NEVER** simplify existing forms, modals, or complex interactions
- **NEVER** replace advanced features with basic versions
- **NEVER** remove data tables, filters, search functionality, or bulk operations
- **NEVER** downgrade component complexity or remove business logic
- **ALWAYS** preserve current state management and data flow
- **ALWAYS** maintain existing event handlers and user interactions
- **ALWAYS** keep current validation rules and error handling

**🔧 MASTERTOOLBAR INTEGRATION (MANDATORY):**
- **viewId**: MUST match exact `menu_id` from `hrm/models/toolbar_config.py` erpMenu records
- **mode management**: Implement VIEW/CREATE/EDIT mode switching based on component state
- **form submission**: Connect save action to existing forms using `data-module-form` attribute
- **backend configuration**: Load toolbar actions from Django backend, not mock data
- **action handling**: Implement toolbar action handlers that work with existing component logic

**📋 EXACT IMPLEMENTATION SEQUENCE:**
1. **DO NOT MODIFY existing React components structure**
2. **DO NOT REMOVE existing features, forms, or UI elements**
3. **APPLY flat design rules** (rounded-none, no shadows, no hover effects) to EXISTING elements
4. **CONNECT MasterToolbar** to existing forms and data flow
5. **INTEGRATE backend API calls** with existing service layer
6. **MAINTAIN all current functionality** while adding missing backend integration
```

---

## 📝 Usage Instructions

**For User Reference Only:**

1. **Copy the prompt above** - This is a reusable template for any HRM task
2. **Fill in the bracketed values**:
   - `{{TASK_NUMBER}}` - Task number from bootstrap/06_03_tasks.md (e.g., 02.1, 03.1, etc.)
   - `{{TASK_NAME}}` - Task name from bootstrap/06_03_tasks.md (e.g., Employee Records, Application Capture)
   - `[Template Type]` - Use template classifications from bootstrap/context_preservation_prompt_template.md
   - `[Specific wiring document path]` - Choose based on task type:
     - Master Data: `bootstrap/05_02_master_data_wiring_hrm.md`
     - Transaction: `bootstrap/05_03_transaction_form_wiring_hrm.md`
     - Workflow: `bootstrap/05_04_workflow_wiring_hrm.md`
3. **Paste and execute** - This ensures all bootstrap standards are followed

**Note**: The system will dynamically resolve both task number and task name from bootstrap/06_03_tasks.md.

## 🔧 Quick Reference for Task Information

- **Task List**: `bootstrap/06_03_tasks.md`
- **Progress Tracker**: `bootstrap/06_04_tracker.md`
- **Next Session Plan**: `bootstrap/06_01_next_session_plan.md`
- **Template Classifications**: See mapping in `bootstrap/context_preservation_prompt_template.md`
- **Wiring Guide Selection**: Based on task type (Master/Transaction/Workflow)

## 🎯 Template Type Mapping (from bootstrap/context_preservation_prompt_template.md)

### HRM Master Data:
- Employee Master → **T1** (Complex Master Template)
- Department → **MST-S** (Simple Master Template)
- Position → **MST-S** (Simple Master Template)
- Organizational Unit → **MST-M** (Medium Master Template)

### HRM Transactions:
- Leave Request → **TXN-M** (Medium Transaction Template)
- Attendance Adjustment → **TXN-S** (Simple Transaction Template)
- Expense Claim → **TXN-M** (Medium Transaction Template)
- Performance Review → **TXN-C** (Complex Transaction Template)
