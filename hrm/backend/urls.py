"""
HRM Backend Project URLs

Root URL configuration for HRM backend project.
This is the main URL entry point for the Django project.
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from hrm.admin_sites import (
    employee_management_site, organization_management_site, performance_management_site,
    learning_development_site, compensation_payroll_site, recruitment_screening_site,
    time_attendance_site, badges_recognition_site, tax_compliance_site, toolbar_configuration_site
)
from hrm.views.admin_index import admin_index_view
from hrm.views.toolbar_config import get_toolbar_config

urlpatterns = [
    # Root path - redirect to admin index landing page
    path('', lambda request: redirect('admin_index'), name='root'),
    
    # Business Domain-Specific Admin Sites FIRST
    # This enforces logical grouping and eliminates flat structure
    path('admin/employee-management/', employee_management_site.urls),
    path('admin/organization-management/', organization_management_site.urls),
    path('admin/performance-management/', performance_management_site.urls),
    path('admin/learning-development/', learning_development_site.urls),
    path('admin/compensation-payroll/', compensation_payroll_site.urls),
    path('admin/recruitment-screening/', recruitment_screening_site.urls),
    path('admin/time-attendance/', time_attendance_site.urls),
    path('admin/badges-recognition/', badges_recognition_site.urls),
    path('admin/tax-compliance/', tax_compliance_site.urls),
    path('admin/toolbar-configuration/', toolbar_configuration_site.urls),
    
    # Admin Index Landing Page (must come BEFORE admin.site.urls to avoid conflicts)
    path('admin/', admin_index_view, name='admin_index'),
    
    # Default admin site for authentication (login/logout) LAST
    # This provides login/logout functionality without exposing flat model structure
    # Since no models are registered to admin.site, it won't show flat structure
    path('admin/', admin.site.urls),
    
    # HRM Organization Chart and Employee Directory APIs
    path('api/hrm/', include('hrm.urls.organization_urls')),
    
    # Toolbar Configuration API (Learning/Dev Mode)
    path('api/toolbar-config/<str:menu_id>/', get_toolbar_config, name='toolbar-config'),
    
    # Toolbar Permissions API (v2.0 API-Driven)
    path('api/toolbar-permissions/', include('hrm.urls.toolbar_permissions')),
]
