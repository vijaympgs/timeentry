#!/usr/bin/env python3
"""
Phase-4 Related Names Fix Script
Fixes 608 reverse accessor conflicts by assigning unique related_name to each model
"""

import os
import re
from pathlib import Path

def fix_related_names():
    """Fix related_name conflicts in all model files"""
    
    # Get all Python files in models directory
    models_dir = Path(__file__).parent / 'hrm' / 'models'
    
    if not models_dir.exists():
        print(f"Models directory not found: {models_dir}")
        return
    
    # Files to process
    python_files = list(models_dir.glob('*.py'))
    
    print(f"Found {len(python_files)} Python files to process")
    
    files_updated = 0
    
    # Define unique related_name mappings for each model
    related_name_mappings = {
        # Application models
        'ApplicationAnswer': 'app_answers',
        'ApplicationCandidate': 'app_candidates', 
        'ApplicationDocument': 'app_documents',
        'ApplicationQuestion': 'app_questions',
        'JobApplication': 'job_applications',
        'JobPosting': 'job_postings',
        
        # Badge models
        'Badge': 'badges',
        'BadgeAward': 'badge_awards',
        'BadgeCategory': 'badge_categories',
        'BadgeNomination': 'badge_nominations',
        'RecognitionFeed': 'recognition_feeds',
        
        # Course models
        'Course': 'courses',
        'CourseContent': 'course_contents',
        'CourseSession': 'course_sessions',
        'Instructor': 'instructors',
        'LearningPath': 'learning_paths',
        
        # Salary models
        'SalaryStructure': 'salary_structures',
        'PayGrade': 'pay_grades',
        'CompensationRange': 'compensation_ranges',
        'JobLevel': 'job_levels',
        'MarketData': 'market_data',
        
        # Contract models
        'ContractTemplate': 'contract_templates',
        'ContractOrganizationalUnit': 'contract_org_units',
        'ContractPosition': 'contract_positions',
        'EmploymentContract': 'employment_contracts',
        'Employee': 'employees',
        
        # Enrollment models
        'Enrollment': 'enrollments',
        'EnrollmentApproval': 'enrollment_approvals',
        'EnrollmentCourse': 'enrollment_courses',
        'EnrollmentCourseSession': 'enrollment_course_sessions',
        'EnrollmentRule': 'enrollment_rules',
        'EnrollmentTemplate': 'enrollment_templates',
        'EnrollmentWaitlist': 'enrollment_waitlists',
        
        # Rating models
        'RatingScale': 'rating_scales',
        'RatingLevel': 'rating_levels',
        'RatingDistribution': 'rating_distributions',
        'RatingGuideline': 'rating_guidelines',
        'CalibrationSession': 'calibration_sessions',
        'ReviewCycle': 'review_cycles',
        
        # Screening models
        'BackgroundCheck': 'background_checks',
        'BackgroundCheckProvider': 'background_check_providers',
        'ScreeningCriteria': 'screening_criteria',
        'ScreeningProcess': 'screening_processes',
        'ScreeningTemplate': 'screening_templates',
        
        # Timesheet models
        'Timesheet': 'timesheets',
        'TimesheetApproval': 'timesheet_approvals',
        'TimesheetEntry': 'timesheet_entries',
        'Project': 'projects',
        'Task': 'tasks',
        
        # Attendance models
        'TimeEntry': 'time_entries',
        'AttendanceDevice': 'attendance_devices',
        'AttendanceException': 'attendance_exceptions',
        'AttendancePolicy': 'attendance_policies',
        'Shift': 'shifts',
        
        # Payroll models
        'PayrollRun': 'payroll_runs',
        'PayrollCalculation': 'payroll_calculations',
        'PayrollDisbursement': 'payroll_disbursements',
        'PayrollSchedule': 'payroll_schedules',
        'EarningCode': 'earning_codes',
        
        # Tax models
        'TaxCalculation': 'tax_calculations',
        'TaxWithholding': 'tax_withholdings',
        'TaxJurisdiction': 'tax_jurisdictions',
        'TaxRate': 'tax_rates',
        'TaxExemption': 'tax_exemptions',
        'TaxPayrollRun': 'tax_payroll_runs',
        
        # Offer models
        'OfferLetter': 'offer_letters',
        'OfferLetterTemplate': 'offer_letter_templates',
        'OfferPosition': 'offer_positions',
        'Candidate': 'candidates',
        
        # Organizational models
        'OrganizationalUnit': 'org_units',
        'Position': 'positions',
        'EmployeePosition': 'employee_positions',
    }
    
    for file_path in python_files:
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            updated = False
            
            # Find all class definitions in this file
            class_pattern = re.compile(r'class\s+(\w+)\s*\(models\.Model\):')
            
            for match in class_pattern.finditer(content):
                class_name = match.group(1)
                
                if class_name in related_name_mappings:
                    # Find company ForeignKey for this class
                    fk_pattern = re.compile(
                        rf'company = models\.ForeignKey\(\s*[\'"]hrm\.Company[\'"],\s*on_delete=models\.CASCADE,\s*related_name=[\'"][^\'\"]*[\'"],?\s*null=True,\s*blank=True\s*\)',
                        re.MULTILINE | re.DOTALL
                    )
                    
                    if fk_pattern.search(content):
                        # Replace with unique related_name
                        new_related_name = related_name_mappings[class_name]
                        content = fk_pattern.sub(
                            f"company = models.ForeignKey(\n        'hrm.Company', \n        on_delete=models.CASCADE,\n        related_name='{new_related_name}',\n        null=True,\n        blank=True\n    )",
                            content
                        )
                        updated = True
                        print(f"Fixed {class_name} -> {new_related_name}")
            
            # Write back if updated
            if updated:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                files_updated += 1
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    print(f"\nSummary:")
    print(f"Files updated: {files_updated}")
    print("Related name conflicts fixed!")

if __name__ == "__main__":
    fix_related_names()
