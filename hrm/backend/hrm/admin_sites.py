from django.contrib.admin import AdminSite
from .models import (
    # Employee Management Models
    EmployeeRecord, EmployeeAddress, EmployeeProfile, EmployeeSkill, EmployeeDocument, SkillCategory,
    
    # Organizational Models
    Department, OrganizationalUnit, Position, EmployeePosition, Company, ContractTemplate, ContractPosition, ContractOrganizationalUnit,
    
    # Performance Management Models
    RatingScale, RatingLevel, RatingDistribution, RatingGuideline, ReviewCycle, CalibrationSession,
    
    # Learning & Development Models
    Course, CourseContent, CourseSession, Instructor, CourseLearningPath,
    
    # Compensation & Payroll Models
    SalaryStructure, PayGrade, CompensationRange, JobLevel, MarketData, PayrollRun, PayrollCalculation, PayrollDisbursement, PayrollSchedule, EarningCode,
    
    # Recruitment & Screening Models
    JobPosting, JobApplication, ApplicationQuestion, ScreeningProcess, ScreeningCriteria, BackgroundCheck, BackgroundCheckProvider, ApplicationAnswer, ApplicationDocument, ApplicationCandidate, ScreeningTemplate, OfferLetter, OfferLetterTemplate, OfferPosition,
    
    # Time & Attendance Models
    TimeEntry, Shift, AttendancePolicy, AttendanceDevice, Timesheet, TimesheetEntry, TimesheetApproval, AttendanceException,
    
    # Badge & Recognition Models
    Badge, BadgeAward, BadgeNomination, BadgeCategory, RecognitionFeed,
    
    # Tax & Compliance Models
    TaxCalculation, TaxRate, TaxJurisdiction, TaxWithholding, TaxExemption, TaxPayrollRun,
    
    # Toolbar Configuration Models
    ERPToolbarControl, ERPMenuItem, Role, RolePermission, UserRole
)

# ============================================================================
# SPECIALIZED ADMIN SITES
# ============================================================================

employee_management_site = AdminSite(name='employee_management')
employee_management_site.site_header = 'Employee Management Administration'
employee_management_site.site_title = 'Employee Management Admin'
employee_management_site.index_title = 'Welcome to Employee Management Administration'

organization_management_site = AdminSite(name='organization_management')
organization_management_site.site_header = 'Organization Management Administration'
organization_management_site.site_title = 'Organization Management Admin'
organization_management_site.index_title = 'Welcome to Organization Management Administration'

performance_management_site = AdminSite(name='performance_management')
performance_management_site.site_header = 'Performance Management Administration'
performance_management_site.site_title = 'Performance Management Admin'
performance_management_site.index_title = 'Welcome to Performance Management Administration'

learning_development_site = AdminSite(name='learning_development')
learning_development_site.site_header = 'Learning & Development Administration'
learning_development_site.site_title = 'Learning & Development Admin'
learning_development_site.index_title = 'Welcome to Learning & Development Administration'

compensation_payroll_site = AdminSite(name='compensation_payroll')
compensation_payroll_site.site_header = 'Compensation & Payroll Administration'
compensation_payroll_site.site_title = 'Compensation & Payroll Admin'
compensation_payroll_site.index_title = 'Welcome to Compensation & Payroll Administration'

recruitment_screening_site = AdminSite(name='recruitment_screening')
recruitment_screening_site.site_header = 'Recruitment & Screening Administration'
recruitment_screening_site.site_title = 'Recruitment & Screening Admin'
recruitment_screening_site.index_title = 'Welcome to Recruitment & Screening Administration'

time_attendance_site = AdminSite(name='time_attendance')
time_attendance_site.site_header = 'Time & Attendance Administration'
time_attendance_site.site_title = 'Time & Attendance Admin'
time_attendance_site.index_title = 'Welcome to Time & Attendance Administration'

badges_recognition_site = AdminSite(name='badges_recognition')
badges_recognition_site.site_header = 'Badges & Recognition Administration'
badges_recognition_site.site_title = 'Badges & Recognition Admin'
badges_recognition_site.index_title = 'Welcome to Badges & Recognition Administration'

tax_compliance_site = AdminSite(name='tax_compliance')
tax_compliance_site.site_header = 'Tax & Compliance Administration'
tax_compliance_site.site_title = 'Tax & Compliance Admin'
tax_compliance_site.index_title = 'Welcome to Tax & Compliance Administration'

# ============================================================================
# NEW: TOOLBAR CONFIGURATION ADMIN SITE
# ============================================================================

toolbar_configuration_site = AdminSite(name='toolbar_configuration')
toolbar_configuration_site.site_header = 'Toolbar Configuration Administration'
toolbar_configuration_site.site_title = 'Toolbar Configuration Admin'
toolbar_configuration_site.index_title = 'Welcome to Toolbar Configuration Administration'

# Import the enhanced admin classes
from .admin_classes import (
    ERPToolbarControlAdmin, ERPMenuItemAdmin, RoleAdmin, 
    RolePermissionAdmin, UserRoleAdmin
)

# Register toolbar models to the dedicated toolbar admin site with enhanced admin classes
toolbar_configuration_site.register(ERPToolbarControl, ERPToolbarControlAdmin)
toolbar_configuration_site.register(ERPMenuItem, ERPMenuItemAdmin)
toolbar_configuration_site.register(Role, RoleAdmin)
toolbar_configuration_site.register(RolePermission, RolePermissionAdmin)
toolbar_configuration_site.register(UserRole, UserRoleAdmin)

# ============================================================================
# REGISTER MODELS TO SPECIALIZED SITES
# ============================================================================
# Register Employee Management models to employee_management_site
from .admin_classes import (
    EmployeeRecordAdmin, EmployeeAddressAdmin, EmployeeProfileAdmin, 
    EmployeeSkillAdmin, EmployeeDocumentAdmin
)

employee_management_site.register(EmployeeRecord, EmployeeRecordAdmin)
employee_management_site.register(EmployeeAddress, EmployeeAddressAdmin)
employee_management_site.register(EmployeeProfile, EmployeeProfileAdmin)
employee_management_site.register(EmployeeSkill, EmployeeSkillAdmin)
employee_management_site.register(EmployeeDocument, EmployeeDocumentAdmin)

# Note: Other model registrations are handled in admin.py
# to avoid duplicate registration conflicts
