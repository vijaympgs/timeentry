# CLINE AGENT END RULE - GOVERNED SESSION TERMINATION

## 🚀 MANDATORY SESSION TERMINATION - ANY OF THESE TRIGGERS

### **TRIGGER PHRASES (ANY OF THESE)**
```
end session
terminate session
close session
finish session
session complete
wrap up session
conclude session
session end
wind off
save and exit
session summary
```

### **WHAT HAPPENS WHEN USER SAYS ANY TRIGGER PHRASE**
When user prompts with ANY of the trigger phrases above, the Cline agent MUST:

1. **READ THIS END RULE FIRST**
   - Read `cline_end_rule.md` to understand session termination requirements
   - This ensures consistent session closure every time

2. **SUMMARIZE SESSION ACCOMPLISHMENTS**
   - Review tasks completed during the session
   - Document progress made and issues resolved
   - Note any incomplete tasks or blockers encountered

3. **UPDATE RELEVANT BOOTSTRAP DOCUMENTS**
   - Update `bootstrap/06_04_tracker.md` with session progress
   - Update `bootstrap/06_05_findings_learnings.md` with new insights
   - Update `bootstrap/06_01_next_session_plan.md` if priorities changed
   - Note: Do NOT miss task-related updates during session termination

4. **CAPTURE CURRENT SYSTEM STATE**
   - Document current state of implemented components
   - Note any configuration changes or data modifications
   - Record any technical debt or issues identified

5. **PREPARE NEXT SESSION CONTEXT**
   - Ensure next session plan is up to date
   - Document any prerequisites for next session
   - Note any dependencies or blocking issues

6. **PROVIDE SESSION SUMMARY**
   - Clear summary of what was accomplished
   - Status of ongoing tasks and priorities
   - Readiness state for next session

### **SESSION TERMINATION CHECKLIST**

#### **📋 DOCUMENTATION UPDATES**
- [ ] Progress tracker updated (`bootstrap/06_04_tracker.md`)
- [ ] Findings and learnings documented (`bootstrap/06_05_findings_learnings.md`)
- [ ] Next session plan updated if needed (`bootstrap/06_01_next_session_plan.md`)
- [ ] Important: Do NOT miss task-related updates during session termination

#### **🔧 SYSTEM STATE CAPTURE**
- [ ] Current implementation status documented
- [ ] Any configuration changes recorded
- [ ] Data modifications or migrations noted
- [ ] Technical debt or issues identified

#### **🎯 NEXT SESSION PREPARATION**
- [ ] Next session priorities clearly defined
- [ ] Prerequisites for next session documented
- [ ] Dependencies or blocking issues noted
- [ ] Environment state preserved

#### **✅ QUALITY ASSURANCE**
- [ ] All code changes committed and saved
- [ ] No unsaved work or pending changes
- [ ] System left in stable state
- [ ] No broken functionality or errors

### **SESSION SUMMARY TEMPLATE**

```markdown
## 🎯 SESSION SUMMARY

**Date**: [Current Date]
**Time**: [Current Time IST]
**Duration**: [Session Duration]
**Focus**: [Primary Session Focus]

### ✅ **COMPLETED TASKS**
- [Task 1 completion status]
- [Task 2 completion status]
- [Task 3 completion status]

### 🔄 **IN PROGRESS TASKS**
- [Task 1 current status]
- [Task 2 current status]
- [Task 3 current status]

### 📋 **NEXT SESSION PRIORITIES**
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

### 🔧 **SYSTEM STATE**
- [Current system state]
- [Any changes made]
- [Issues identified]

### 📊 **PROGRESS METRICS**
- [Key progress indicators]
- [Performance metrics]
- [Quality metrics]

**SESSION STATUS**: [COMPLETED/PARTIALLY COMPLETED/BLOCKED]
**NEXT SESSION READINESS**: [READY/NEEDS PREPARATION/BLOCKED]
```

### **CRITICAL RULES**

#### **🚫 NEVER END SESSION WITHOUT**
- ❌ Leaving unsaved work or changes
- ❌ Breaking functionality or introducing errors
- ❌ Not updating relevant documentation
- ❌ Not providing clear session summary
- ❌ Not preparing next session context

#### **✅ ALWAYS DO THESE THINGS**
- ✅ Read this end rule first when triggered
- ✅ Provide comprehensive session summary
- ✅ Update all relevant bootstrap documents
- ✅ Ensure system is left in stable state
- ✅ Document next session requirements clearly

### **SESSION HANDOFF PROTOCOL**

#### **FOR SAME DAY RESUMPTION:**
- Document current context and state
- Note exact stopping point
- Preserve any in-memory state or configurations
- Provide clear continuation instructions

#### **FOR NEXT DAY RESUMPTION:**
- Complete session summary with full context
- Update all tracking documents
- Ensure system is in stable, commit-ready state
- Document any environment or setup requirements

#### **FOR LONGER GAPS:**
- Comprehensive session documentation
- Complete system state capture
- Detailed next session plan
- Environment setup and configuration guide

### **QUALITY GATES**

#### **SESSION COMPLETION CRITERIA:**
- All intended tasks completed or properly documented as in-progress
- No broken functionality or errors introduced
- All documentation updated and accurate
- System left in stable, testable state
- Next session properly prepared and documented

#### **SESSION SUCCESS METRICS:**
- Measurable progress toward goals
- Code quality maintained or improved
- Documentation accuracy and completeness
- System stability and reliability
- Team readiness for next session

---

**THIS RULE IS MANDATORY FOR ALL SESSION TERMINATIONS**
**VIOLATION CONSTITUTES GOVERNANCE FAILURE**
**ALWAYS END WITH ONE OF THE TRIGGER PHRASES ABOVE**

**AGENT INSTRUCTION: When you see any trigger phrase, read this file first, then execute proper session termination protocol.**
