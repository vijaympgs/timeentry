AGENT EXECUTION CONTRACT — HRM GOVERNANCE ENFORCEMENT (LOCKED)

You are NOT here to reason freely.  
You are here to EXECUTE deterministically under governance.

Any deviation = FAILURE.

================================================================
ABSOLUTE ENVIRONMENT AUTHORITY
================================================================
OS                : Windows ONLY
Shell             : CMD.exe syntax ONLY (not Linux, not mixed PowerShell)
Valid Working Dir : D:\platform\hrm\backend\
Valid Entry       : python manage.py
Valid Django Path : D:\platform\hrm\backend\manage.py

You must assume NOTHING else exists.

================================================================
CRITICAL FAILURE PATTERN OBSERVED (YOU MUST FIX THIS)
================================================================
You repeatedly:
- Execute from wrong folders
- Use invalid shell syntax (; instead of &&)
- Use Linux-style expectations (ls, pwd, cd .. logic)
- Use Push-Location / Pop-Location incorrectly
- Drift into analysis instead of execution
- Ignore provided governance even after acknowledgment

This must stop.

================================================================
MANDATORY COMMAND EXECUTION FORMAT
================================================================
ALL commands must follow EXACTLY this pattern:

    cd /d D:\platform\hrm\backend && python manage.py <command>

Examples:
    cd /d D:\platform\hrm\backend && python manage.py check
    cd /d D:\platform\hrm\backend && python manage.py migrate
    cd /d D:\platform\hrm\backend && python manage.py runserver

NOT ALLOWED:
    python manage.py ...
    cd D:\platform\hrm\backend; python manage.py ...
    Push-Location ...
    ls
    pwd
    ./manage.py
    hrm\manage.py
    D://hrm//managepy
    Any Linux-style assumption

If you execute any command, you MUST:
1. Explicitly state working directory
2. Show the exact command
3. Use the format above

================================================================
BOOTSTRAP COMPLIANCE (NON-NEGOTIABLE)
================================================================
At the START of every session you must:

1. Read:
   - bootstrap/00_bootstrap_master_index.md
   - bootstrap/06_03_tasks.md
   - bootstrap/06_04_tracker.md

2. Then state explicitly:
   - Current task
   - Which checklist applies
   - What you will implement next

You are NOT allowed to skip this.

================================================================
TASK MODE: IMPLEMENTATION ONLY
================================================================
You are NOT here to:
- Analyze endlessly
- Refactor unnecessarily
- Simplify UI
- Rewrite existing structures
- Invent your own architecture

You ARE here to:
- Enhance existing code only
- Preserve complexity
- Wire backend to existing UI
- Follow wiring checklist exactly
- Follow toolbar checklist exactly
- Follow typography rules exactly

"ENHANCE ONLY. DO NOT REWRITE." is a hard rule.

================================================================
SCRIPT DISCIPLINE
================================================================
If a task involves repetitive edits (JSON, models, fixtures, etc):
- You MUST propose a Python script
- You MUST implement the script
- You MUST run the script
- You MUST show results

Manual edits for repetitive tasks are considered incompetence.

================================================================
FAIL-FAST BEHAVIOR
================================================================
If you hit ANY of these:
- Path error
- File not found
- Unicode error
- Import error
- Unexpected behavior

You must STOP and report:
- The exact error
- The exact command you ran
- The exact working directory

You must NOT retry randomly.

================================================================
ABSOLUTE PROHIBITIONS
================================================================
- Do NOT use ls, pwd, cat
- Do NOT use semicolon (;) for chaining commands
- Do NOT use Push-Location / Pop-Location
- Do NOT assume paths
- Do NOT simplify UI
- Do NOT remove features
- Do NOT rewrite components
- Do NOT downgrade complexity
- Do NOT invent new architecture

================================================================
SUCCESS CRITERIA
================================================================
You are only succeeding if:
- All commands run from correct directory
- No path errors occur
- No governance violations occur
- Implementation follows bootstrap checklists
- No UI or logic regressions occur

================================================================
FINAL DIRECTIVE
================================================================
You must obey this contract strictly before continuing any HRM task.

If you cannot follow this structure, you must stop.

Acknowledge internally. Then proceed.