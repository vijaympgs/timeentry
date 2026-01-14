from django.contrib import admin
from .admin_sites import (
    employee_management_site, organization_management_site, performance_management_site,
    learning_development_site, compensation_payroll_site, recruitment_screening_site,
    time_attendance_site, badges_recognition_site, tax_compliance_site
)
from .models import (
    # Core Models
    Company,
    
    # Toolbar Configuration Models
    ERPToolbarControl, ERPMenuItem, Role, RolePermission, UserRole,
    
    # Employee Management Models
    EmployeeRecord, EmployeeAddress, EmployeeProfile, EmployeeSkill, EmployeeDocument, SkillCategory,
    
    # Organizational Models
    Department, OrganizationalUnit, Position, EmployeePosition,
    
    # Salary & Compensation Models
    SalaryStructure, PayGrade, CompensationRange, JobLevel, MarketData,
    
    # Rating & Performance Models
    RatingScale, RatingLevel, RatingDistribution, RatingGuideline, ReviewCycle, CalibrationSession,
    
    # Course & Learning Models
    Course, CourseContent, CourseSession, Instructor, CourseLearningPath,
    
    # Badge & Recognition Models
    Badge, BadgeAward, BadgeNomination, BadgeCategory, RecognitionFeed,
    
    # Offer & Contract Models
    OfferLetterTemplate, OfferLetter, OfferPosition, ContractTemplate, ContractPosition, ContractOrganizationalUnit,
    
    # Application & Screening Models
    JobApplication, ApplicationAnswer, ApplicationDocument, JobPosting, ApplicationCandidate, ApplicationQuestion,
    ScreeningProcess, ScreeningCriteria, BackgroundCheck, ScreeningTemplate, BackgroundCheckProvider,
    
    # Tax Models
    TaxCalculation, TaxWithholding, TaxJurisdiction, TaxRate, TaxExemption, TaxPayrollRun,
    
    # Payroll Models
    PayrollRun, PayrollCalculation, PayrollDisbursement, PayrollSchedule, EarningCode,
    
    # Time & Attendance Models
    TimeEntry, AttendanceException, AttendancePolicy, Shift, AttendanceDevice,
    
    # Timesheet Models
    Timesheet, TimesheetEntry, TimesheetApproval
)

# ============================================================================
# TOOLBAR CONFIGURATION ADMIN CLASSES
# ============================================================================
# Note: Toolbar admin classes have been moved to admin_classes.py
# to avoid circular import issues with admin_sites.py

# ============================================================================
# EMPLOYEE MANAGEMENT ADMIN SITE
# ============================================================================
# Note: Employee management models are now registered in admin_sites.py
# to avoid duplicate registration conflicts

# ============================================================================
# ORGANIZATION MANAGEMENT ADMIN SITE
# ============================================================================
@admin.register(Department, site=organization_management_site)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    fieldsets = (
        ('Department Information', {
            'fields': ('name', 'description')
        }),
    )

@admin.register(OrganizationalUnit, site=organization_management_site)
class OrganizationalUnitAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code', 'unit_type', 'level', 'is_active']
    search_fields = ['name', 'code']
    fieldsets = (
        ('Unit Information', {
            'fields': ('name', 'code', 'unit_type', 'level', 'parent_unit', 'manager')
        }),
        ('Unit Details', {
            'fields': ('description', 'phone', 'email', 'cost_center_code', 'budget_owner')
        }),
        ('Status', {
            'fields': ('is_active', 'effective_date')
        }),
    )

@admin.register(Position, site=organization_management_site)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'position_code', 'job_grade', 'employment_type', 'is_active']
    search_fields = ['title', 'position_code']
    fieldsets = (
        ('Position Information', {
            'fields': ('title', 'position_code', 'job_grade', 'job_family', 'employment_type')
        }),
        ('Position Details', {
            'fields': ('description', 'requirements', 'responsibilities')
        }),
        ('Compensation', {
            'fields': ('min_salary', 'max_salary', 'currency')
        }),
        ('Headcount', {
            'fields': ('headcount', 'filled_count')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

@admin.register(EmployeePosition, site=organization_management_site)
class EmployeePositionAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee', 'position', 'assignment_type', 'is_primary', 'status']
    search_fields = ['employee__first_name', 'employee__last_name', 'position__title']
    fieldsets = (
        ('Position Assignment', {
            'fields': ('employee', 'position', 'organizational_unit', 'assignment_type', 'is_primary')
        }),
        ('Assignment Details', {
            'fields': ('effective_date', 'end_date', 'status')
        }),
    )

@admin.register(Company, site=organization_management_site)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code', 'is_active']
    search_fields = ['name', 'code']
    fieldsets = (
        ('Company Information', {
            'fields': ('name', 'code', 'is_active')
        }),
    )

@admin.register(ContractTemplate, site=organization_management_site)
class ContractTemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'template_name', 'template_code', 'contract_type', 'status']
    search_fields = ['template_name', 'template_code']
    fieldsets = (
        ('Template Information', {
            'fields': ('template_name', 'template_code', 'contract_type')
        }),
        ('Template Content', {
            'fields': ('template_content',)
        }),
        ('Status', {
            'fields': ('status', 'template_type')
        }),
    )

@admin.register(ContractPosition, site=organization_management_site)
class ContractPositionAdmin(admin.ModelAdmin):
    list_display = ['id', 'position_code']
    search_fields = ['position_code']
    fieldsets = (
        ('Contract Position', {
            'fields': ('position_code',)
        }),
    )

@admin.register(ContractOrganizationalUnit, site=organization_management_site)
class ContractOrganizationalUnitAdmin(admin.ModelAdmin):
    list_display = ['id', 'unit_code', 'unit_name', 'unit_type']
    search_fields = ['unit_name', 'unit_code']
    fieldsets = (
        ('Contract Unit Information', {
            'fields': ('unit_code', 'unit_name', 'unit_type')
        }),
    )

# ============================================================================
# PERFORMANCE MANAGEMENT ADMIN SITE
# ============================================================================
@admin.register(RatingScale, site=performance_management_site)
class RatingScaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'scale_name', 'scale_code', 'scale_type', 'status']
    search_fields = ['scale_name', 'scale_code']
    fieldsets = (
        ('Rating Scale', {
            'fields': ('scale_name', 'scale_code', 'scale_type', 'description', 'min_value', 'max_value')
        }),
        ('Status', {
            'fields': ('status', 'template_type')
        }),
    )

@admin.register(RatingLevel, site=performance_management_site)
class RatingLevelAdmin(admin.ModelAdmin):
    list_display = ['id', 'level_name', 'level_code', 'rating_scale', 'numeric_value']
    search_fields = ['level_name', 'level_code']
    fieldsets = (
        ('Rating Level', {
            'fields': ('level_name', 'level_code', 'rating_scale', 'numeric_value')
        }),
    )

@admin.register(ReviewCycle, site=performance_management_site)
class ReviewCycleAdmin(admin.ModelAdmin):
    list_display = ['id', 'cycle_name', 'cycle_code', 'start_date', 'end_date']
    search_fields = ['cycle_name', 'cycle_code']
    fieldsets = (
        ('Review Cycle', {
            'fields': ('cycle_name', 'cycle_code', 'start_date', 'end_date', 'description')
        }),
    )

@admin.register(CalibrationSession, site=performance_management_site)
class CalibrationSessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'session_name', 'session_code', 'scheduled_date', 'status']
    search_fields = ['session_name', 'session_code']
    fieldsets = (
        ('Session Information', {
            'fields': ('session_name', 'session_code', 'scheduled_date', 'status')
        }),
    )

@admin.register(RatingGuideline, site=performance_management_site)
class RatingGuidelineAdmin(admin.ModelAdmin):
    list_display = ['id', 'rating_scale', 'guideline_title', 'guideline_type']
    search_fields = ['guideline_title']

@admin.register(RatingDistribution, site=performance_management_site)
class RatingDistributionAdmin(admin.ModelAdmin):
    list_display = ['id', 'rating_scale', 'rating_level', 'actual_count']
    search_fields = ['rating_scale__scale_name', 'rating_level__level_name']
    fieldsets = (
        ('Rating Distribution', {
            'fields': ('rating_scale', 'rating_level', 'actual_count')
        }),
    )

# ============================================================================
# LEARNING & DEVELOPMENT ADMIN SITE
# ============================================================================
@admin.register(Course, site=learning_development_site)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'course_name', 'course_code', 'course_type', 'course_category', 'status']
    search_fields = ['course_name', 'course_code']
    fieldsets = (
        ('Course Information', {
            'fields': ('course_name', 'course_code', 'course_type', 'course_category', 'description')
        }),
        ('Course Details', {
            'fields': ('duration', 'max_capacity', 'prerequisites')
        }),
        ('Status', {
            'fields': ('status',)
        }),
    )

@admin.register(CourseContent, site=learning_development_site)
class CourseContentAdmin(admin.ModelAdmin):
    list_display = ['id', 'content_title', 'course', 'content_type', 'sort_order']
    search_fields = ['content_title', 'course__course_name']
    fieldsets = (
        ('Content Information', {
            'fields': ('course', 'content_title', 'content_type', 'sort_order')
        }),
    )

@admin.register(CourseSession, site=learning_development_site)
class CourseSessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'session_name', 'course', 'start_date', 'status']
    search_fields = ['session_name', 'course__course_name']
    fieldsets = (
        ('Session Information', {
            'fields': ('course', 'session_name', 'start_date', 'end_date', 'status')
        }),
    )

@admin.register(Instructor, site=learning_development_site)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['id', 'instructor_name', 'instructor_code', 'is_active']
    search_fields = ['instructor_name', 'instructor_code']
    fieldsets = (
        ('Instructor Information', {
            'fields': ('instructor_name', 'instructor_code', 'bio', 'expertise_areas')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

@admin.register(CourseLearningPath, site=learning_development_site)
class LearningPathAdmin(admin.ModelAdmin):
    list_display = ['id', 'path_name', 'path_code', 'is_active']
    search_fields = ['path_name', 'path_code']
    fieldsets = (
        ('Learning Path', {
            'fields': ('path_name', 'path_code', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

# ============================================================================
# COMPENSATION & PAYROLL ADMIN SITE
# ============================================================================
@admin.register(SalaryStructure, site=compensation_payroll_site)
class SalaryStructureAdmin(admin.ModelAdmin):
    list_display = ['id', 'structure_type', 'status']
    search_fields = ['structure_type']
    fieldsets = (
        ('Salary Structure', {
            'fields': ('structure_type', 'description')
        }),
        ('Status', {
            'fields': ('status', 'template_type')
        }),
    )

@admin.register(PayGrade, site=compensation_payroll_site)
class PayGradeAdmin(admin.ModelAdmin):
    list_display = ['id', 'grade_code', 'grade_level']
    search_fields = ['grade_code', 'grade_level']
    fieldsets = (
        ('Pay Grade', {
            'fields': ('grade_code', 'grade_level')
        }),
    )

@admin.register(CompensationRange, site=compensation_payroll_site)
class CompensationRangeAdmin(admin.ModelAdmin):
    list_display = ['id', 'pay_grade', 'range_name', 'geographic_area', 'adjusted_minimum', 'adjusted_maximum']
    search_fields = ['pay_grade__grade_code', 'range_name', 'geographic_area']
    fieldsets = (
        ('Range Information', {
            'fields': ('pay_grade', 'range_name', 'range_type', 'geographic_area')
        }),
        ('Salary Range', {
            'fields': ('adjusted_minimum', 'adjusted_midpoint', 'adjusted_maximum')
        }),
    )

@admin.register(PayrollRun, site=compensation_payroll_site)
class PayrollRunAdmin(admin.ModelAdmin):
    list_display = ['id', 'run_number', 'status']
    search_fields = ['run_number']
    fieldsets = (
        ('Payroll Run', {
            'fields': ('run_number', 'status')
        }),
    )

@admin.register(PayrollCalculation, site=compensation_payroll_site)
class PayrollCalculationAdmin(admin.ModelAdmin):
    list_display = ['id', 'payroll_run', 'employee']
    search_fields = ['payroll_run__run_number', 'employee__first_name']
    fieldsets = (
        ('Payroll Calculation', {
            'fields': ('payroll_run', 'employee')
        }),
    )

@admin.register(PayrollDisbursement, site=compensation_payroll_site)
class PayrollDisbursementAdmin(admin.ModelAdmin):
    list_display = ['id', 'payroll_run', 'employee']
    search_fields = ['payroll_run__run_number', 'employee__first_name']
    fieldsets = (
        ('Payroll Disbursement', {
            'fields': ('payroll_run', 'employee')
        }),
    )

@admin.register(PayrollSchedule, site=compensation_payroll_site)
class PayrollScheduleAdmin(admin.ModelAdmin):
    list_display = ['id', 'schedule_name']
    search_fields = ['schedule_name']
    fieldsets = (
        ('Payroll Schedule', {
            'fields': ('schedule_name',)
        }),
    )

@admin.register(EarningCode, site=compensation_payroll_site)
class EarningCodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'description', 'earning_type', 'is_taxable']
    search_fields = ['code', 'description']
    fieldsets = (
        ('Earning Code', {
            'fields': ('code', 'description', 'earning_type', 'is_taxable')
        }),
    )

@admin.register(JobLevel, site=compensation_payroll_site)
class JobLevelAdmin(admin.ModelAdmin):
    list_display = ['id', 'level_number', 'level_name']
    search_fields = ['level_name']
    fieldsets = (
        ('Job Level', {
            'fields': ('level_number', 'level_name')
        }),
    )

@admin.register(MarketData, site=compensation_payroll_site)
class MarketDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'job_family', 'job_level', 'geographic_area']
    search_fields = ['job_family', 'job_level']
    fieldsets = (
        ('Market Data', {
            'fields': ('job_family', 'job_level', 'geographic_area')
        }),
    )

# ============================================================================
# RECRUITMENT & SCREENING ADMIN SITE
# ============================================================================
@admin.register(JobPosting, site=recruitment_screening_site)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    search_fields = ['title']
    fieldsets = (
        ('Job Posting', {
            'fields': ('title', 'description')
        }),
    )

@admin.register(JobApplication, site=recruitment_screening_site)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'application_number', 'candidate', 'job_posting', 'status', 'application_date']
    search_fields = ['application_number', 'candidate__first_name']
    fieldsets = (
        ('Application Information', {
            'fields': ('application_number', 'candidate', 'job_posting', 'status', 'application_date')
        }),
        ('Application Details', {
            'fields': ('cover_letter', 'resume', 'expected_salary')
        }),
    )

@admin.register(ApplicationQuestion, site=recruitment_screening_site)
class ApplicationQuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'question_text', 'question_type', 'is_required']
    search_fields = ['question_text']
    fieldsets = (
        ('Question Information', {
            'fields': ('question_text', 'question_type', 'is_required', 'options')
        }),
    )

@admin.register(ScreeningProcess, site=recruitment_screening_site)
class ScreeningProcessAdmin(admin.ModelAdmin):
    list_display = ['id', 'screening_number', 'candidate', 'job_posting', 'status', 'screening_date']
    search_fields = ['screening_number', 'candidate__first_name']
    fieldsets = (
        ('Screening Process', {
            'fields': ('screening_number', 'candidate', 'job_posting', 'status', 'screening_date')
        }),
        ('Screening Details', {
            'fields': ('screening_score', 'screening_notes')
        }),
    )

@admin.register(BackgroundCheck, site=recruitment_screening_site)
class BackgroundCheckAdmin(admin.ModelAdmin):
    list_display = ['id', 'candidate', 'check_type', 'status']
    search_fields = ['candidate__first_name']
    fieldsets = (
        ('Background Check', {
            'fields': ('candidate', 'check_type', 'status', 'check_date', 'results')
        }),
    )

@admin.register(ApplicationAnswer, site=recruitment_screening_site)
class ApplicationAnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'application', 'question']
    search_fields = ['application__application_number']
    fieldsets = (
        ('Answer Information', {
            'fields': ('application', 'question', 'answer_text')
        }),
    )

@admin.register(ApplicationDocument, site=recruitment_screening_site)
class ApplicationDocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'application', 'document_type', 'document_name']
    search_fields = ['application__application_number', 'document_name']
    fieldsets = (
        ('Document Information', {
            'fields': ('application', 'document_type', 'document_name', 'file')
        }),
    )

@admin.register(ApplicationCandidate, site=recruitment_screening_site)
class ApplicationCandidateAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'first_name', 'last_name']
    search_fields = ['first_name', 'last_name', 'email']
    fieldsets = (
        ('Candidate Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
    )

@admin.register(ScreeningCriteria, site=recruitment_screening_site)
class ScreeningCriteriaAdmin(admin.ModelAdmin):
    list_display = ['id', 'screening_process', 'criteria_type', 'weight']
    search_fields = ['screening_process__screening_number']
    fieldsets = (
        ('Screening Criteria', {
            'fields': ('screening_process', 'criteria_type', 'weight', 'description')
        }),
    )

@admin.register(ScreeningTemplate, site=recruitment_screening_site)
class ScreeningTemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'template_name']
    search_fields = ['template_name']
    fieldsets = (
        ('Screening Template', {
            'fields': ('template_name', 'description')
        }),
    )

@admin.register(BackgroundCheckProvider, site=recruitment_screening_site)
class BackgroundCheckProviderAdmin(admin.ModelAdmin):
    list_display = ['id', 'provider_name', 'is_active']
    search_fields = ['provider_name']
    fieldsets = (
        ('Provider Information', {
            'fields': ('provider_name', 'contact_info', 'services_offered')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

@admin.register(OfferLetter, site=recruitment_screening_site)
class OfferLetterAdmin(admin.ModelAdmin):
    list_display = ['id', 'candidate', 'job_position', 'offer_status', 'offer_date']
    search_fields = ['candidate__first_name', 'job_position__title']
    fieldsets = (
        ('Offer Information', {
            'fields': ('candidate', 'job_position', 'offer_status', 'offer_date', 'expiry_date')
        }),
        ('Offer Details', {
            'fields': ('salary_offered', 'start_date', 'benefits_package')
        }),
    )

@admin.register(OfferLetterTemplate, site=recruitment_screening_site)
class OfferLetterTemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'template_name', 'template_code', 'template_type', 'status']
    search_fields = ['template_name', 'template_code']
    fieldsets = (
        ('Template Information', {
            'fields': ('template_name', 'template_code', 'template_type')
        }),
        ('Template Content', {
            'fields': ('template_content',)
        }),
        ('Status', {
            'fields': ('status',)
        }),
    )

@admin.register(OfferPosition, site=recruitment_screening_site)
class OfferPositionAdmin(admin.ModelAdmin):
    list_display = ['id', 'position_code']
    search_fields = ['position_code']
    fieldsets = (
        ('Offer Position', {
            'fields': ('position_code',)
        }),
    )

# ============================================================================
# TIME & ATTENDANCE ADMIN SITE
# ============================================================================
@admin.register(TimeEntry, site=time_attendance_site)
class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee', 'entry_date', 'clock_in_time', 'clock_out_time', 'status']
    search_fields = ['employee__first_name']
    fieldsets = (
        ('Time Entry', {
            'fields': ('employee', 'entry_date', 'clock_in_time', 'clock_out_time', 'status')
        }),
    )

@admin.register(Shift, site=time_attendance_site)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ['id', 'shift_name', 'shift_code', 'start_time', 'end_time', 'is_active']
    search_fields = ['shift_name', 'shift_code']
    fieldsets = (
        ('Shift Information', {
            'fields': ('shift_name', 'shift_code', 'start_time', 'end_time', 'break_duration')
        }),
        ('Shift Details', {
            'fields': ('description', 'is_active')
        }),
    )

@admin.register(AttendancePolicy, site=time_attendance_site)
class AttendancePolicyAdmin(admin.ModelAdmin):
    list_display = ['id', 'policy_name', 'policy_code', 'policy_type']
    search_fields = ['policy_name', 'policy_code']
    fieldsets = (
        ('Policy Information', {
            'fields': ('policy_name', 'policy_code', 'policy_type', 'description')
        }),
    )

@admin.register(AttendanceDevice, site=time_attendance_site)
class AttendanceDeviceAdmin(admin.ModelAdmin):
    list_display = ['id', 'device_name', 'device_type', 'is_active']
    search_fields = ['device_name']
    fieldsets = (
        ('Device Information', {
            'fields': ('device_name', 'device_type', 'location', 'is_active')
        }),
    )

@admin.register(Timesheet, site=time_attendance_site)
class TimesheetAdmin(admin.ModelAdmin):
    list_display = ['id', 'timesheet_number', 'employee', 'timesheet_period_start', 'status']
    search_fields = ['timesheet_number', 'employee__first_name']
    fieldsets = (
        ('Timesheet', {
            'fields': ('timesheet_number', 'employee', 'timesheet_period_start', 'status')
        }),
    )

@admin.register(AttendanceException, site=time_attendance_site)
class AttendanceExceptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee', 'exception_type', 'status']
    search_fields = ['employee__first_name']
    fieldsets = (
        ('Exception Information', {
            'fields': ('employee', 'exception_type', 'exception_date', 'status')
        }),
    )

@admin.register(TimesheetEntry, site=time_attendance_site)
class TimesheetEntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'timesheet', 'entry_date', 'status']
    search_fields = ['timesheet__timesheet_number']

@admin.register(TimesheetApproval, site=time_attendance_site)
class TimesheetApprovalAdmin(admin.ModelAdmin):
    list_display = ['id', 'timesheet', 'approver', 'approval_date']
    search_fields = ['timesheet__timesheet_number']
    fieldsets = (
        ('Timesheet Approval', {
            'fields': ('timesheet', 'approver', 'approval_date')
        }),
    )

# ============================================================================
# BADGES & RECOGNITION ADMIN SITE
# ============================================================================
@admin.register(Badge, site=badges_recognition_site)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['id', 'badge_code', 'badge_category', 'status']
    search_fields = ['badge_code']
    fieldsets = (
        ('Badge Information', {
            'fields': ('badge_code', 'badge_category', 'badge_name', 'description')
        }),
        ('Badge Details', {
            'fields': ('points_required', 'badge_level', 'validity_period')
        }),
        ('Status', {
            'fields': ('status',)
        }),
    )

@admin.register(BadgeAward, site=badges_recognition_site)
class BadgeAwardAdmin(admin.ModelAdmin):
    list_display = ['id', 'badge', 'recipient_employee', 'awarded_by', 'status']
    search_fields = ['badge__badge_code', 'recipient_employee__first_name']
    fieldsets = (
        ('Badge Award', {
            'fields': ('badge', 'recipient_employee', 'awarded_by', 'award_date', 'status')
        }),
    )

@admin.register(BadgeNomination, site=badges_recognition_site)
class BadgeNominationAdmin(admin.ModelAdmin):
    list_display = ['id', 'badge', 'nominated_employee', 'nominated_by', 'status']
    search_fields = ['badge__badge_code', 'nominated_employee__first_name']
    fieldsets = (
        ('Badge Nomination', {
            'fields': ('badge', 'nominated_employee', 'nominated_by', 'nomination_date', 'status')
        }),
    )

@admin.register(RecognitionFeed, site=badges_recognition_site)
class RecognitionFeedAdmin(admin.ModelAdmin):
    list_display = ['id', 'badge_award']
    search_fields = ['badge_award__badge__badge_code']
    fieldsets = (
        ('Recognition Feed', {
            'fields': ('badge_award', 'feed_text', 'posted_date')
        }),
    )

@admin.register(BadgeCategory, site=badges_recognition_site)
class BadgeCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_code']
    search_fields = ['category_code']
    fieldsets = (
        ('Badge Category', {
            'fields': ('category_code', 'category_name', 'description')
        }),
    )

# ============================================================================
# TAX & COMPLIANCE ADMIN SITE
# ============================================================================
@admin.register(TaxCalculation, site=tax_compliance_site)
class TaxCalculationAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee', 'tax_year', 'calculation_status']
    search_fields = ['employee__first_name']
    fieldsets = (
        ('Tax Calculation', {
            'fields': ('employee', 'tax_year', 'calculation_status')
        }),
    )

@admin.register(TaxRate, site=tax_compliance_site)
class TaxRateAdmin(admin.ModelAdmin):
    list_display = ['id', 'tax_jurisdiction', 'effective_date']
    search_fields = ['tax_jurisdiction__jurisdiction_name']
    fieldsets = (
        ('Tax Rate', {
            'fields': ('tax_jurisdiction', 'effective_date')
        }),
    )

@admin.register(TaxJurisdiction, site=tax_compliance_site)
class TaxJurisdictionAdmin(admin.ModelAdmin):
    list_display = ['id', 'jurisdiction_name', 'state_code', 'jurisdiction_type', 'status']
    search_fields = ['jurisdiction_name', 'state_code']
    fieldsets = (
        ('Tax Jurisdiction', {
            'fields': ('jurisdiction_name', 'state_code', 'jurisdiction_type', 'status')
        }),
    )

@admin.register(TaxPayrollRun, site=tax_compliance_site)
class TaxPayrollRunAdmin(admin.ModelAdmin):
    list_display = ['id']
    search_fields = []

@admin.register(TaxWithholding, site=tax_compliance_site)
class TaxWithholdingAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee']
    search_fields = ['employee__first_name']
    fieldsets = (
        ('Tax Withholding', {
            'fields': ('employee',)
        }),
    )

@admin.register(TaxExemption, site=tax_compliance_site)
class TaxExemptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee']
    search_fields = ['employee__first_name']
    fieldsets = (
        ('Tax Exemption', {
            'fields': ('employee',)
        }),
    )
