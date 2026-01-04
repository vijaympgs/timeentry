"""
Django admin configuration for HRM models
"""
from django.contrib import admin
from .models import EmployeeRecord, EmployeeAddress, Department


@admin.register(EmployeeRecord)
class EmployeeRecordAdmin(admin.ModelAdmin):
    """
    Admin configuration for EmployeeRecord model
    """
    list_display = [
        'employee_number',
        'first_name',
        'last_name',
        'email',
        'department_name',
        'position_title',
        'employment_status',
        'hire_date',
        'is_active'
    ]
    
    list_filter = [
        'employment_status',
        'employment_type',
        'gender',
        'marital_status',
        'is_active',
        'company_code',
        'hire_date'
    ]
    
    search_fields = [
        'employee_number',
        'first_name',
        'last_name',
        'work_email',
        'personal_email',
        'position_title',
        'department_name'
    ]
    
    ordering = ['-hire_date', 'last_name', 'first_name']
    
    fieldsets = (
        ('Employee Information', {
            'fields': ('employee_number', 'national_id', 'social_security_number', 'passport_number')
        }),
        ('Personal Details', {
            'fields': ('first_name', 'last_name', 'middle_name', 'preferred_name', 'name_prefix', 'name_suffix', 'gender', 'date_of_birth', 'marital_status')
        }),
        ('Contact Information', {
            'fields': ('work_email', 'personal_email', 'work_phone', 'mobile_phone', 'home_phone')
        }),
        ('Employment Details', {
            'fields': ('hire_date', 'original_hire_date', 'employment_status', 'employment_type', 'termination_date', 'termination_reason', 'rehire_eligible')
        }),
        ('Position Information', {
            'fields': ('position_title', 'department_name', 'job_category', 'job_level', 'job_family', 'work_location_name', 'remote_work_eligible', 'remote_work_percentage')
        }),
        ('Manager Information', {
            'fields': ('manager_name', 'hr_business_partner_name')
        }),
        ('Compensation', {
            'fields': ('salary_grade', 'salary_step', 'annual_salary', 'hourly_rate', 'currency', 'pay_frequency')
        }),
        ('Benefits', {
            'fields': ('benefits_eligibility_date', 'benefits_package_name', 'health_insurance_eligible', 'dental_insurance_eligible', 'vision_insurance_eligible', 'retirement_plan_eligible', 'life_insurance_eligible')
        }),
        ('Emergency Contacts', {
            'fields': ('primary_emergency_contact_name', 'primary_emergency_contact_relationship', 'primary_emergency_contact_phone', 'secondary_emergency_contact_name', 'secondary_emergency_contact_relationship', 'secondary_emergency_contact_phone')
        }),
        ('Status & System', {
            'fields': ('is_active', 'is_confidential', 'is_key_employee', 'is_high_potential', 'username', 'role', 'company_code')
        }),
        ('Audit', {
            'fields': ('created_by_user', 'updated_by_user', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def email(self, obj):
        return obj.work_email
    email.short_description = 'Email'


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """
    Admin configuration for Department model
    """
    list_display = [
        'name',
        'department_code',
        'parent_department',
        'manager',
        'is_active',
        'created_at'
    ]
    
    list_filter = [
        'is_active',
        'company_code',
        'created_at'
    ]
    
    search_fields = [
        'name',
        'department_code',
        'description'
    ]
    
    ordering = ['name']
    
    fieldsets = (
        ('Department Information', {
            'fields': ('name', 'department_code', 'description')
        }),
        ('Organization', {
            'fields': ('parent_department', 'manager')
        }),
        ('Status & System', {
            'fields': ('is_active', 'company_code')
        }),
        ('Audit', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(EmployeeAddress)
class EmployeeAddressAdmin(admin.ModelAdmin):
    """
    Admin configuration for EmployeeAddress model
    """
    list_display = [
        'employee',
        'address_type',
        'address_line_1',
        'city',
        'state',
        'country',
        'is_primary',
        'is_active'
    ]
    
    list_filter = [
        'address_type',
        'is_primary',
        'is_active',
        'company_code',
        'country'
    ]
    
    search_fields = [
        'employee__first_name',
        'employee__last_name',
        'employee__employee_number',
        'address_line_1',
        'city',
        'state',
        'postal_code'
    ]
    
    ordering = ['employee__last_name', 'employee__first_name', 'address_type']
    
    fieldsets = (
        ('Address Information', {
            'fields': ('employee', 'address_type', 'is_primary', 'is_active')
        }),
        ('Address Details', {
            'fields': ('address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country')
        }),
        ('System', {
            'fields': ('company_code',)
        }),
        ('Audit', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['created_at', 'updated_at']
