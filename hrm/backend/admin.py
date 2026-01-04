from django.contrib import admin
from .models import Company, Department, EmployeeRecord

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'created_at']
    search_fields = ['name', 'email']
    ordering = ['name']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'created_at']
    search_fields = ['name', 'company__name']
    list_filter = ['company']
    ordering = ['name']

@admin.register(EmployeeRecord)
class EmployeeRecordAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'employee_id', 'email', 'department', 'position', 'employment_status', 'is_active']
    search_fields = ['first_name', 'last_name', 'email', 'employee_id']
    list_filter = ['department', 'employment_status', 'gender', 'company']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'gender', 'address')
        }),
        ('Employment Information', {
            'fields': ('employee_id', 'company', 'department', 'position', 'employment_status', 'hire_date', 'salary', 'is_active')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
