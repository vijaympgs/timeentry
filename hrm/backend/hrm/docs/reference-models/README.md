# HRM Reference Models - Phase-2 Deferred

## Overview
These models have been moved from runtime to reference documentation as part of Phase-2 stabilization.

## Non-Runtime Models (Reference/BBP Only)

### Profile Management
- `profile_view.py` - ProfileViewEmployee, ProfileViewSkill, ProfileViewDocument, ProfileViewSkillCategory

### Survey & Feedback
- `pulse_surveys.py` - PulseSurvey and related models

### Recruitment & Interviewing
- `interview_scheduling.py` - InterviewScheduling and related models
- `offer_management.py` - OfferManagement and related models

### Onboarding & Offboarding
- `new_hire_setup.py` - OnboardingProcess, OnboardingTask, OnboardingDocument
- `exit_checklist.py` - ExitChecklist, ExitChecklistTask, ExitChecklistTemplate

### Performance & Goals
- `review_cycle.py` - PerformanceReviewCycle, PerformanceReview, ReviewForm
- `goal_setting.py` - Goal, GoalProgress, GoalTemplate

### Learning & Development
- `completion_tracking.py` - LearningProgress, ModuleProgress, Certificate

### Workflow Management
- `approval_workflow.py` - ApprovalRequest, ApprovalStep, ApprovalWorkflow
- `termination_workflow.py` - Termination, TerminationStep, TerminationTemplate

## Status
- **Phase**: 2 Deferred
- **Runtime**: No (moved to docs/)
- **Purpose**: Reference/BBP documentation only
- **Integration**: Can be reactivated in Phase-3 if needed

## Notes
- Models preserved for future reference
- No runtime dependencies
- Available for documentation and BBP specifications
