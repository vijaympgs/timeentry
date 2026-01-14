"""
HRM Models Package - Phase-3 Stabilization
Following governance: One file = One aggregate root
Phase-3: Fix domain.Company references with placeholder models
"""

# Import placeholder models for Phase-3 stabilization
from .company import Company

# Import toolbar configuration models
from .toolbar_config import ERPToolbarControl, ERPMenuItem, Role, RolePermission, UserRole
# Import audit trail models
from .audit_trail import AuditTrail, AuditTrailConfiguration

# Import canonical aggregate roots (Phase-1 Executable)
from .employee import EmployeeRecord, EmployeeAddress
from .department import Department
from .organizational_unit import OrganizationalUnit, Position, EmployeePosition
from .employee_profile import EmployeeProfile, EmployeeSkill, EmployeeDocument, SkillCategory
from .profile_view import ProfileViewAccess, ProfileEndorsement, ProfileViewSettings

# Import essential BBP models (Phase-1 Executable)
from .salary_structures import SalaryStructure, PayGrade, CompensationRange, JobLevel, MarketData
from .ratings import RatingScale, RatingLevel, RatingDistribution, RatingGuideline, ReviewCycle, CalibrationSession
from .course_catalog import Course, CourseContent, CourseSession, Instructor, CourseLearningPath
from .recognition_badges import Badge, BadgeAward, BadgeNomination, BadgeCategory, RecognitionFeed
from .offer_letter import OfferLetterTemplate, OfferLetter, OfferPosition
from .contract_template import ContractTemplate, ContractPosition, ContractOrganizationalUnit
from .application_capture import JobApplication, ApplicationAnswer, ApplicationDocument, JobPosting, ApplicationCandidate, ApplicationQuestion
from .screening import ScreeningProcess, ScreeningCriteria, BackgroundCheck, ScreeningTemplate, BackgroundCheckProvider
from .tax_calculations import TaxCalculation, TaxWithholding, TaxJurisdiction, TaxRate, TaxExemption, TaxPayrollRun
from .payroll_run import PayrollRun, PayrollCalculation, PayrollDisbursement, PayrollSchedule, EarningCode
from .clock_in_out import TimeEntry, AttendanceException, AttendancePolicy, Shift, AttendanceDevice
from .timesheets import Timesheet, TimesheetEntry, TimesheetApproval
from .enrollment import Enrollment, EnrollmentWaitlist, EnrollmentApproval, EnrollmentRule, EnrollmentTemplate, EnrollmentCourse, EnrollmentCourseSession
# from .project_management import Project, Task  # Module doesn't exist yet
# from .employee import Employee  # Employee model doesn't exist yet, only EmployeeRecord

# Phase-2 Deferred: Remove from imports (keep files, mark as non-runtime)
# from .profile_view import ProfileViewEmployee, ProfileViewSkill, ProfileViewDocument, ProfileViewSkillCategory
# from .pulse_surveys import PulseSurvey
# from .interview_scheduling import InterviewScheduling
# from .offer_management import OfferManagement
# from .new_hire_setup import OnboardingProcess, OnboardingTask, OnboardingDocument
# from .approval_workflow import ApprovalRequest, ApprovalStep, ApprovalWorkflow
# from .goal_setting import Goal, GoalProgress, GoalTemplate
# from .review_cycle import PerformanceReviewCycle, PerformanceReview, ReviewForm
# from .completion_tracking import LearningProgress, ModuleProgress, Certificate
# from .exit_checklist import ExitChecklist, ExitChecklistTask, ExitChecklistTemplate
# from .termination_workflow import Termination, TerminationStep, TerminationTemplate

__all__ = [
    # Core Models
    'Company',  # 'Employee',  # Employee model doesn't exist yet, only EmployeeRecord
    
    # Toolbar Configuration Models
    'ERPToolbarControl', 'ERPMenuItem', 'Role', 'RolePermission', 'UserRole',
    
    # Audit Trail Models
    'AuditTrail', 'AuditTrailConfiguration',
    
    # Masters (Phase-1 Executable)
    'EmployeeRecord', 'EmployeeAddress', 'Department', 'OrganizationalUnit', 'Position', 'EmployeePosition',
    'EmployeeProfile', 'EmployeeSkill', 'EmployeeDocument', 'SkillCategory',
    'SalaryStructure', 'PayGrade', 'CompensationRange', 'JobLevel', 'MarketData',
    'RatingScale', 'RatingLevel', 'RatingDistribution', 'RatingGuideline', 'ReviewCycle', 'CalibrationSession',
    'Course', 'CourseContent', 'CourseSession', 'Instructor', 'CourseLearningPath',
    'Badge', 'BadgeAward', 'BadgeNomination', 'BadgeCategory', 'RecognitionFeed',
    'OfferLetterTemplate', 'OfferLetter', 'OfferPosition',
    'ContractTemplate', 'ContractPosition', 'ContractOrganizationalUnit',
    
    # Transactions (Phase-1 Executable)
    'JobApplication', 'ApplicationAnswer', 'ApplicationDocument', 'JobPosting', 'ApplicationCandidate', 'ApplicationQuestion',
    'ScreeningProcess', 'ScreeningCriteria', 'BackgroundCheck', 'ScreeningTemplate', 'BackgroundCheckProvider',
    'TaxCalculation', 'TaxWithholding', 'TaxJurisdiction', 'TaxRate', 'TaxExemption', 'TaxPayrollRun',
    'PayrollRun', 'PayrollCalculation', 'PayrollDisbursement', 'PayrollSchedule', 'EarningCode',
    'TimeEntry', 'AttendanceException', 'AttendancePolicy', 'Shift', 'AttendanceDevice',
    'Timesheet', 'TimesheetEntry', 'TimesheetApproval',
    'Enrollment', 'EnrollmentWaitlist', 'EnrollmentApproval', 'EnrollmentRule', 'EnrollmentTemplate', 'EnrollmentCourse', 'EnrollmentCourseSession',
    # 'Project', 'Task',  # Module doesn't exist yet
    
    # Phase-2 Deferred (moved to docs/, non-runtime)
    # 'ProfileViewEmployee', 'ProfileViewSkill', 'ProfileViewDocument', 'ProfileViewSkillCategory',
    # 'PulseSurvey', 'InterviewScheduling', 'OfferManagement', 
    # 'OnboardingProcess', 'OnboardingTask', 'OnboardingDocument',
    # 'ApprovalRequest', 'ApprovalStep', 'ApprovalWorkflow',
    # 'Goal', 'GoalProgress', 'GoalTemplate',
    # 'PerformanceReviewCycle', 'PerformanceReview', 'ReviewForm',
    # 'LearningProgress', 'ModuleProgress', 'Certificate',
    # 'ExitChecklist', 'ExitChecklistTask', 'ExitChecklistTemplate',
    # 'Termination', 'TerminationStep', 'TerminationTemplate',
]
