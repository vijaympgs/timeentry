# Phase-4 HRM Migration Detailed Report

## Current Status: 620 Reverse Accessor Conflicts

## Migration Issues Identified

### 1. Application Models (5 models)
**Problem**: All using `app_questions` related_name
**Models Affected**:
- ApplicationAnswer → `app_answers` ✅ FIXED
- ApplicationCandidate → `app_candidates` ✅ FIXED  
- ApplicationDocument → `app_documents` ✅ FIXED
- ApplicationQuestion → `app_questions` ❌ STILL BROKEN
- JobApplication → `job_applications` ✅ FIXED
- JobPosting → `job_postings` ✅ FIXED

**Remaining Issue**: ApplicationQuestion still uses `app_questions` instead of `app_questions`

### 2. Badge Models (5 models)
**Problem**: All using `recognition_feeds` related_name
**Models Affected**:
- Badge → `badges` ✅ FIXED
- BadgeAward → `badge_awards` ✅ FIXED
- BadgeCategory → `badge_categories` ✅ FIXED
- BadgeNomination → `badge_nominations` ✅ FIXED
- RecognitionFeed → `recognition_feeds` ❌ STILL BROKEN

**Remaining Issue**: RecognitionFeed still uses `recognition_feeds` instead of `recognition_feeds`

### 3. Course Models (5 models)
**Problem**: All using `learning_paths` related_name
**Models Affected**:
- Course → `courses` ✅ FIXED
- CourseContent → `course_contents` ✅ FIXED
- CourseSession → `course_sessions` ✅ FIXED
- Instructor → `instructors` ✅ FIXED
- LearningPath → `learning_paths` ❌ STILL BROKEN

**Remaining Issue**: LearningPath still uses `learning_paths` instead of `learning_paths`

### 4. Salary Models (5 models)
**Problem**: All using `market_data` related_name
**Models Affected**:
- SalaryStructure → `salary_structures` ✅ FIXED
- JobLevel → `job_levels` ✅ FIXED
- MarketData → `market_data` ❌ STILL BROKEN
- PayGrade → `pay_grades` ✅ FIXED
- CompensationRange → `compensation_ranges` ✅ FIXED

**Remaining Issue**: MarketData still uses `market_data` instead of `market_data`

### 5. Contract Models (5 models)
**Problem**: All using `contract_org_units` related_name
**Models Affected**:
- ContractTemplate → `contract_templates` ✅ FIXED
- ContractPosition → `contract_positions` ✅ FIXED
- ContractOrganizationalUnit → `contract_org_units` ✅ FIXED
- Employee → `employees` ✅ FIXED
- EmploymentContract → `employment_contracts` ✅ FIXED

**Status**: All Contract models FIXED ✅

### 6. Enrollment Models (7 models)
**Problem**: All using `enrollment_course_sessions` related_name
**Models Affected**:
- Enrollment → `enrollments` ✅ FIXED
- EnrollmentApproval → `enrollment_approvals` ✅ FIXED
- EnrollmentCourse → `enrollment_courses` ✅ FIXED
- EnrollmentCourseSession → `enrollment_course_sessions` ✅ FIXED
- EnrollmentRule → `enrollment_rules` ✅ FIXED
- EnrollmentTemplate → `enrollment_templates` ✅ FIXED
- EnrollmentWaitlist → `enrollment_waitlists` ✅ FIXED

**Status**: All Enrollment models FIXED ✅

### 7. Rating Models (6 models)
**Problem**: All using `review_cycles` related_name
**Models Affected**:
- RatingScale → `rating_scales` ✅ FIXED
- RatingLevel → `rating_levels` ✅ FIXED
- RatingDistribution → `rating_distributions` ✅ FIXED
- RatingGuideline → `rating_guidelines` ✅ FIXED
- CalibrationSession → `calibration_sessions` ✅ FIXED
- ReviewCycle → `review_cycles` ❌ STILL BROKEN

**Remaining Issue**: ReviewCycle still uses `review_cycles` instead of `review_cycles`

### 8. Screening Models (5 models)
**Problem**: All using `background_check_providers` related_name
**Models Affected**:
- BackgroundCheck → `background_checks` ✅ FIXED
- BackgroundCheckProvider → `background_check_providers` ❌ STILL BROKEN
- ScreeningCriteria → `screening_criteria` ✅ FIXED
- ScreeningProcess → `screening_processes` ✅ FIXED
- ScreeningTemplate → `screening_templates` ✅ FIXED

**Remaining Issue**: BackgroundCheckProvider still uses `background_check_providers` instead of `background_check_providers`

### 9. Timesheet Models (5 models)
**Problem**: All using `tasks` related_name
**Models Affected**:
- Timesheet → `timesheets` ✅ FIXED
- TimesheetApproval → `timesheet_approvals` ✅ FIXED
- TimesheetEntry → `timesheet_entries` ✅ FIXED
- Project → `projects` ✅ FIXED
- Task → `tasks` ❌ STILL BROKEN

**Remaining Issue**: Task still uses `tasks` instead of `tasks`

### 10. Attendance Models (5 models)
**Problem**: All using `attendance_devices` related_name
**Models Affected**:
- AttendanceDevice → `attendance_devices` ✅ FIXED
- AttendanceException → `attendance_exceptions` ✅ FIXED
- AttendancePolicy → `attendance_policies` ✅ FIXED
- Shift → `shifts` ✅ FIXED
- TimeEntry → `time_entries` ✅ FIXED

**Status**: All Attendance models FIXED ✅

### 11. Tax Models (7 models)
**Problem**: All using `tax_payroll_runs` related_name
**Models Affected**:
- TaxCalculation → `tax_calculations` ✅ FIXED
- TaxWithholding → `tax_withholdings` ✅ FIXED
- TaxJurisdiction → `tax_jurisdictions` ✅ FIXED
- TaxRate → `tax_rates` ✅ FIXED
- TaxExemption → `tax_exemptions` ✅ FIXED
- TaxPayrollRun → `tax_payroll_runs` ❌ STILL BROKEN

**Remaining Issue**: TaxPayrollRun still uses `tax_payroll_runs` instead of `tax_payroll_runs`

### 12. Offer Models (4 models)
**Problem**: All using `offer_positions` related_name
**Models Affected**:
- OfferLetter → `offer_letters` ✅ FIXED
- OfferLetterTemplate → `offer_letter_templates` ✅ FIXED
- OfferPosition → `offer_positions` ❌ STILL BROKEN
- Candidate → `candidates` ✅ FIXED

**Remaining Issue**: OfferPosition still uses `offer_positions` instead of `offer_positions`

### 13. Organizational Models (3 models)
**Problem**: All using `employee_positions` related_name
**Models Affected**:
- OrganizationalUnit → `org_units` ✅ FIXED
- Position → `positions` ✅ FIXED
- EmployeePosition → `employee_positions` ❌ STILL BROKEN

**Remaining Issue**: EmployeePosition still uses `employee_positions` instead of `employee_positions`

## Root Cause Analysis

### Regex Pattern Limitations
The current fix script uses basic regex patterns that may not catch:
1. Multi-line ForeignKey definitions
2. ForeignKey fields with different formatting
3. Models with multiple company ForeignKey fields
4. Inherited or abstract base class patterns

### Migration Script Issues
Previous scripts may have:
1. Applied incorrect related_name mappings
2. Left some models untouched
3. Created inconsistent naming patterns
4. Failed to handle edge cases

## Seed Data Status

### Available Fixtures
- ✅ 01_master_organizational_units.json
- ✅ 02_master_positions.json  
- ✅ 03_master_salary_structures.json
- ✅ 04_master_ratings.json
- ✅ 05_master_courses.json
- ✅ 06_master_recognition_badges.json
- ✅ 07_master_offer_templates.json
- ✅ 08_master_contract_templates.json
- ✅ 11_transaction_applications.json
- ✅ 00_master_seed_index.py

### Migration Dependencies
- **Prerequisite**: Django check must pass (0 issues)
- **Required**: Database migrations created and run
- **Next**: Seed data loading and validation

## Immediate Action Required

### Manual Fix Options
1. **Individual Model Review**: Manually edit each remaining broken model
2. **Enhanced Regex Script**: Create more comprehensive fix patterns
3. **Database Migration**: Proceed with migrations after Django check passes

### Recommended Approach
1. **Manual Intervention**: Fix the 12 remaining model groups
2. **Validation**: Run Django check after each fix
3. **Incremental Migration**: Create migrations progressively
4. **Seed Data Loading**: Load and validate fixtures

## Next Steps After Fix

1. **Database Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Seed Data Loading**:
   ```bash
   python manage.py loaddata fixtures/00_master_seed_index.py
   python manage.py loaddata fixtures/01_master_organizational_units.json
   # ... continue with all fixtures
   ```

3. **Validation**:
   ```bash
   python manage.py check
   python manage.py validate
   ```

## Critical Path Forward

The 620 conflicts represent the final barrier to Phase-4 completion. Each model group requires individual attention to resolve the remaining related_name conflicts before database migrations can proceed successfully.
