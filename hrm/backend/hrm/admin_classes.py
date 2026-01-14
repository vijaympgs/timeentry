from django.contrib import admin
from .models import (
    # Toolbar Configuration Models
    ERPToolbarControl, ERPMenuItem, Role, RolePermission, UserRole,
    
    # Employee Management Models
    EmployeeRecord, EmployeeAddress, EmployeeProfile, EmployeeSkill, EmployeeDocument, SkillCategory,
)

# ============================================================================
# TOOLBAR CONFIGURATION ADMIN CLASSES
# ============================================================================

class ERPToolbarControlAdmin(admin.ModelAdmin):
    list_display = ['module_name', 'master_toolbar_string']
    list_filter = ['module_name']
    search_fields = ['module_name']
    fieldsets = (
        ('Toolbar Control', {
            'fields': ('module_name', 'master_toolbar_string')
        }),
    )

class ERPMenuItemAdmin(admin.ModelAdmin):
    list_display = ['menu_id', 'menu_name', 'app', 'submodule', 'module', 'menu_type', 'toolbar_config', 'display_toolbar_config', 'is_active']
    list_filter = ['app', 'module', 'menu_type', 'is_active', 'submodule']
    search_fields = ['menu_id', 'menu_name', 'app', 'submodule']
    list_editable = ['is_active', 'menu_type', 'toolbar_config']
    ordering = ['app', 'module', 'menu_name']
    
    def display_toolbar_config(self, obj):
        """Display the toolbar configuration in a more readable format."""
        if not obj.toolbar_config:
            return "-"
            
        # Map of action codes to their descriptions
        action_map = {
            'N': 'New', 'E': 'Edit', 'S': 'Save', 'C': 'Cancel', 'K': 'Clear',
            'V': 'View', 'P': 'Print', 'M': 'Email', 'R': 'Refresh', 'D': 'Delete',
            'X': 'Exit', 'Q': 'Search', 'F': 'Filter', 'I': 'Import', 'O': 'Export',
            'L': 'Clone', 'B': 'Notes', 'U': 'Attach', 'G': 'Settings', '?': 'Help',
            'T': 'Submit', 'J': 'Reject', 'H': 'Hold', 'Z': 'Void', 'A': 'Authorize',
            'W': 'Amend'
        }
        
        # Convert each code to its description
        actions = [action_map.get(code, code) for code in obj.toolbar_config if code.strip()]
        return ", ".join(actions) if actions else "-"
        
    display_toolbar_config.short_description = 'Toolbar Config'
        
    fieldsets = (
        ('Menu Information', {
            'fields': ('menu_id', 'menu_name', 'is_active')
        }),
        ('Application Structure', {
            'fields': ('app', 'submodule', 'module', 'menu_type')
        }),
        ('Toolbar Configuration', {
            'fields': ('toolbar_config', 'applicable_toolbar_config')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()

class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    fieldsets = (
        ('Role Information', {
            'fields': ('name', 'description', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )

class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ['role', 'menu_item', 'override_enabled', 'created_at']
    list_filter = ['override_enabled', 'role']
    search_fields = ['role__name', 'menu_item__menu_name']
    fieldsets = (
        ('Permission Configuration', {
            'fields': ('role', 'menu_item', 'toolbar_override', 'override_enabled')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'assigned_at', 'assigned_by']
    list_filter = ['role']
    search_fields = ['user__username', 'user__email', 'role__name']
    fieldsets = (
        ('User Role Assignment', {
            'fields': ('user', 'role', 'assigned_by')
        }),
        ('Assignment Details', {
            'fields': ('assigned_at',)
        }),
    )

# ============================================================================
# EMPLOYEE MANAGEMENT ADMIN CLASSES
# ============================================================================

class EmployeeRecordAdmin(admin.ModelAdmin):
    list_display = ['employee_number', 'first_name', 'last_name', 'work_email', 'department_name', 'employment_status', 'is_active']
    list_filter = ['employment_status', 'employment_type', 'is_active', 'department_name']
    search_fields = ['employee_number', 'first_name', 'last_name', 'work_email']
    list_editable = ['is_active', 'employment_status']
    ordering = ['employee_number']
    
    fieldsets = (
        ('Employee Information', {
            'fields': ('employee_number', 'first_name', 'last_name', 'middle_name', 'preferred_name')
        }),
        ('Contact Information', {
            'fields': ('work_email', 'personal_email', 'work_phone', 'mobile_phone', 'home_phone')
        }),
        ('Employment Details', {
            'fields': ('employment_status', 'employment_type', 'hire_date', 'termination_date', 'termination_reason')
        }),
        ('Job Information', {
            'fields': ('department_name', 'position_title', 'job_category', 'job_level', 'manager_name')
        }),
        ('Personal Information', {
            'fields': ('date_of_birth', 'gender', 'marital_status', 'national_id', 'social_security_number')
        }),
        ('System Information', {
            'fields': ('is_active', 'is_confidential', 'is_key_employee', 'username', 'role')
        }),
    )

class EmployeeAddressAdmin(admin.ModelAdmin):
    list_display = ['employee', 'address_type', 'city', 'state', 'country', 'is_primary', 'is_active']
    list_filter = ['address_type', 'is_primary', 'is_active', 'country']
    search_fields = ['employee__first_name', 'employee__last_name', 'city', 'state']
    ordering = ['employee', '-is_primary', 'address_type']
    
    fieldsets = (
        ('Address Information', {
            'fields': ('employee', 'address_type', 'is_primary', 'is_active')
        }),
        ('Address Details', {
            'fields': ('address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country')
        }),
    )

class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ['employee', 'preferred_name', 'gender', 'marital_status', 'profile_visibility', 'is_active']
    list_filter = ['gender', 'marital_status', 'profile_visibility', 'is_active']
    search_fields = ['employee__first_name', 'employee__last_name', 'preferred_name']
    ordering = ['employee']
    
    fieldsets = (
        ('Profile Information', {
            'fields': ('employee', 'preferred_name', 'middle_name', 'nickname', 'gender', 'date_of_birth')
        }),
        ('Contact Information', {
            'fields': ('personal_email', 'personal_phone', 'work_phone_extension')
        }),
        ('Address Information', {
            'fields': ('home_address_line_1', 'home_address_line_2', 'home_city', 'home_state', 'home_postal_code', 'home_country')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_relationship', 'emergency_contact_phone', 'emergency_contact_email')
        }),
        ('Profile Settings', {
            'fields': ('profile_visibility', 'profile_photo_url', 'bio', 'linkedin_url', 'twitter_url')
        }),
        ('Preferences', {
            'fields': ('preferred_language', 'timezone', 'email_notifications', 'sms_notifications')
        }),
        ('Status', {
            'fields': ('is_active', 'is_verified', 'verification_date')
        }),
    )

class EmployeeSkillAdmin(admin.ModelAdmin):
    list_display = ['employee', 'skill_name', 'skill_category', 'proficiency_level', 'years_experience', 'is_verified']
    list_filter = ['skill_category', 'proficiency_level', 'is_verified']
    search_fields = ['employee__employee__first_name', 'employee__employee_number', 'skill_name', 'skill_category']
    ordering = ['employee', 'skill_category', 'skill_name']
    
    fieldsets = (
        ('Skill Information', {
            'fields': ('employee', 'skill_name', 'skill_category', 'proficiency_level', 'years_experience', 'last_used', 'is_verified')
        }),
        ('Skill Details', {
            'fields': ('description', 'verified_by', 'verified_date')
        }),
    )

class EmployeeDocumentAdmin(admin.ModelAdmin):
    list_display = ['employee', 'document_name', 'document_type', 'upload_date', 'expiry_date', 'is_active']
    list_filter = ['document_type', 'is_active']
    search_fields = ['employee__employee__first_name', 'employee__employee_number', 'document_name', 'document_type']
    ordering = ['employee', 'document_type']
    
    fieldsets = (
        ('Document Information', {
            'fields': ('employee', 'document_name', 'document_type', 'is_active')
        }),
        ('Document Details', {
            'fields': ('description', 'file_url', 'file_size', 'file_type', 'upload_date', 'expiry_date', 'is_confidential')
        }),
    )
