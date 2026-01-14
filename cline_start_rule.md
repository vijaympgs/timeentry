# CLINE AGENT START RULE - GOVERNED EXECUTION

## 🚀 MANDATORY SESSION INITIALIZATION - ANY OF THESE TRIGGERS

### **TRIGGER PHRASES (ANY OF THESE)**
```
start session
initialize session
begin governed execution
read bootstrap and start
start development session
bootstrap session
governed execution start
```

### **WHAT HAPPENS WHEN USER SAYS ANY TRIGGER PHRASE**
When user prompts with ANY of the trigger phrases above, the Cline agent MUST:

1. **READ THIS START RULE FIRST**
   - Read `cline_start_rule.md` to understand governance requirements
   - This ensures consistent session initialization every time

2. **READ BOOTSTRAP MASTER INDEX SECOND**
   - Read `bootstrap/00_bootstrap_master_index.md` 
   - This is the SINGLE SOURCE OF TRUTH for all governance requirements
   - NO other files should be read until this is complete

3. **ANALYZE CURRENT SYSTEM STATE**
   - Review current task status from bootstrap documents
   - Identify pending priorities and implementation requirements
   - Understand current development context and constraints

4. **ESTABLISH GOVERNANCE CONTEXT**
   - Windows environment only (D:\platform\hrm\backend\manage.py)
   - Django runtime with strict path requirements
   - No Linux commands, no semicolon chaining, no path guessing

5. **CREATE EXECUTION PLAN**
   - Follow T1 Complex Master Template specifications
   - Maintain flat design patterns (no borders, shadows, hover effects)
   - Use backend-driven toolbar configuration system
   - Preserve existing functionality, additive enhancements only

### **CRITICAL RULES**

#### **🚫 NEVER DO THESE THINGS**
- ❌ Ask to re-read bootstrap files unnecessarily
- ❌ Re-question already fixed decisions
- ❌ Re-derive architecture or design intent
- ❌ Use Linux commands on Windows
- ❌ Guess filesystem paths or manage.py locations
- ❌ Modify models, migrations, or architecture without explicit instruction
- ❌ Break scope discipline or drift into rewrite mode
- ❌ **CRITICAL: NEVER use 'DEFAULT' as company code - ONLY '001' is allowed**
- ❌ **CRITICAL: NEVER create test data with company_code='DEFAULT'**
- ❌ **CRITICAL: NEVER assume company codes - ALWAYS use '001' for development**

#### **✅ ALWAYS DO THESE THINGS**
- ✅ Read `bootstrap/00_bootstrap_master_index.md` FIRST
- ✅ Execute deterministically within defined constraints
- ✅ Follow Windows/Django governance contract
- ✅ Use correct manage.py path: `D:\platform\hrm\backend\manage.py`
- ✅ Preserve complexity and existing functionality
- ✅ Implement missing pieces additively only

### **COMPLETE BOOTSTRAP READING REQUIREMENT**
After reading master index, MUST read ALL files listed below before proceeding:

**GOVERNANCE & FOUNDATION (00_XX → 01_XX):**
1. `bootstrap/00boostrap_governance.md` - Governed execution contract
2. `bootstrap/00EMP_REFERENCE_DEV_GUIDE.md` - Employee implementation reference
3. `bootstrap/01_01_governance_foundation.md` - Platform governance
4. `bootstrap/01_02_platform_onboarding.md` - Platform setup
5. `bootstrap/01_03_context_limit_rules.md` - Context management

**STABILIZATION & TECHNICAL (02_XX):**
6. `bootstrap/02_01_django_stabilization_summary.md` - Technical achievements
7. `bootstrap/02_02_hrm_stabilization_reference.md` - HRM reference
8. `bootstrap/02_03_session_context_preservation.md` - Session continuity

**UI DEVELOPMENT & STYLING (03_XX):**
9. `bootstrap/03_01_ui_development_guide.md` - UI development standards
10. `bootstrap/03_02_toolbar_universal_guide_v2.md` - Toolbar universal guide
11. `bootstrap/03_03_ui_typography_styling.md` - UI typography and styling

**AGENT E & TOOLBAR IMPLEMENTATION (04_XX):**
12. `bootstrap/04_01_cline_onboarding.md` - Agent E onboarding guide
13. `bootstrap/04_02_toolbar_implementation_guide_v2.md` - Implementation guide
14. `bootstrap/04_03_toolbar_code_examples_v2.md` - Code examples
15. `bootstrap/04_03_toolbar_mode_based_filtering_v2.md` - Mode filtering

**WIRING IMPLEMENTATION GUIDES (05_XX):**
16. `bootstrap/05_01_wiring_checklists_overview.md` - Wiring overview
17. `bootstrap/05_02_master_data_wiring_hrm.md` - Master data wiring
18. `bootstrap/05_03_transaction_form_wiring_hrm.md` - Transaction wiring
19. `bootstrap/05_04_workflow_wiring_hrm.md` - Workflow wiring

**PROJECT MANAGEMENT & TRACKING (06_XX):**
20. `bootstrap/06_01_next_session_plan.md` - Next session plan
21. `bootstrap/06_02_tasks_checklist.md` - Tasks checklist
22. `bootstrap/06_03_01_tasklist.md` - Task list details
23. `bootstrap/06_03_tasks.md` - Project tasks
24. `bootstrap/06_04_tracker.md` - Progress tracker
25. `bootstrap/06_05_findings_learnings.md` - Findings and learnings

**REFERENCE & TOOLS (99_XX):**
26. `bootstrap/99_toolbar_explorer_hrm.html` - Interactive toolbar inspector

**PROMPT TEMPLATES:**
27. `bootstrap/governace_prompt.md` - Governance prompt template
28. `bootstrap/task_execution_prompt.md` - Task execution prompt
29. `bootstrap/toolbar_implementation_checklist.md` - Implementation checklist

**CRITICAL: ALL FILES MUST BE READ BEFORE PROCEEDING WITH ANY DEVELOPMENT TASKS**

### **EXECUTION ENVIRONMENT CONTRACT**
- **OS**: Windows only
- **Shell**: CMD / PowerShell only  
- **Platform Root**: D:\platform\
- **Django Runtime**: D:\platform\hrm\backend\
- **Manage.py Path**: D:\platform\hrm\backend\manage.py

**Command Format**: `cd D:\platform\hrm\backend && python manage.py <command>`

### **SUCCESS CONDITIONS**
- Tasks move forward measurably
- Code executes cleanly
- No architectural drift occurs
- Existing functionality is preserved
- Enhancements are additive only
- Governance is respected
- Progress is visible and verifiable

---

**THIS RULE IS MANDATORY FOR ALL SESSIONS**
**VIOLATION CONSTITUTES GOVERNANCE FAILURE**
**ALWAYS START WITH ONE OF THE TRIGGER PHRASES ABOVE**

**AGENT INSTRUCTION: When you see any trigger phrase, read this file first, then bootstrap master index.**
