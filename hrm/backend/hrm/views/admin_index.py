"""
Admin Index View for HRM Business Domain Navigation
Provides a landing page with links to all business domain admin sites
"""

from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def admin_index_view(request):
    """
    Admin index view that provides navigation to all business domain admin sites
    """
    admin_sites = [
        {
            'name': 'Employee Management',
            'url': '/admin/employee-management/',
            'description': 'Manage employee records, profiles, skills, and documents',
            'icon': 'users'
        },
        {
            'name': 'Organization Management',
            'url': '/admin/organization-management/',
            'description': 'Manage departments, organizational units, positions, and company structure',
            'icon': 'building'
        },
        {
            'name': 'Performance Management',
            'url': '/admin/performance-management/',
            'description': 'Manage performance reviews, ratings, and calibration sessions',
            'icon': 'chart-line'
        },
        {
            'name': 'Learning & Development',
            'url': '/admin/learning-development/',
            'description': 'Manage courses, training sessions, and learning paths',
            'icon': 'graduation-cap'
        },
        {
            'name': 'Compensation & Payroll',
            'url': '/admin/compensation-payroll/',
            'description': 'Manage salary structures, pay grades, and payroll processing',
            'icon': 'dollar-sign'
        },
        {
            'name': 'Recruitment & Screening',
            'url': '/admin/recruitment-screening/',
            'description': 'Manage job postings, applications, and screening processes',
            'icon': 'user-plus'
        },
        {
            'name': 'Time & Attendance',
            'url': '/admin/time-attendance/',
            'description': 'Manage time entries, shifts, and attendance policies',
            'icon': 'clock'
        },
        {
            'name': 'Badges & Recognition',
            'url': '/admin/badges-recognition/',
            'description': 'Manage badges, awards, and employee recognition programs',
            'icon': 'award'
        },
        {
            'name': 'Tax & Compliance',
            'url': '/admin/tax-compliance/',
            'description': 'Manage tax calculations, jurisdictions, and compliance',
            'icon': 'balance-scale'
        },
        {
            'name': 'Toolbar Configuration',
            'url': '/admin/toolbar-configuration/',
            'description': 'Manage toolbar configurations, roles, and permissions',
            'icon': 'tools'
        }
    ]
    
    context = {
        'admin_sites': admin_sites,
        'title': '',
        'user': request.user,
        'site_template': 'admin/base_site.html'  # Force default template for main admin page
    }
    
    return render(request, 'admin/admin_index.html', context)
