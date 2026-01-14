#!/usr/bin/env python
"""
Python script to analyze existing employee data structure
Run with: python analyze_employees.py
"""

import os
import sys
import django

# Add the backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'hrm', 'backend')
sys.path.insert(0, backend_path)

# Change to backend directory
os.chdir(backend_path)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from hrm.models.employee import EmployeeRecord

def analyze_employee_data():
    """Analyze existing employee data structure"""
    print("=== EMPLOYEE DATA ANALYSIS ===\n")
    
    # Get all employees for company '001'
    employees = EmployeeRecord.objects.filter(company_code='001').order_by('employee_number')
    
    print(f"Total employees: {employees.count()}")
    print()
    
    # Sample employees
    print("Sample employees:")
    for i, emp in enumerate(employees[:10]):
        print(f"{i+1}. {emp.employee_number} - {emp.first_name} {emp.last_name} - {emp.position_title} - {emp.department_name}")
    print()
    
    # Departments
    print("Departments:")
    depts = employees.values_list('department_name', flat=True).distinct()
    for dept in depts:
        count = employees.filter(department_name=dept).count()
        print(f"  {dept}: {count} employees")
    print()
    
    # Position titles
    print("Position titles (first 20):")
    positions = employees.values_list('position_title', flat=True).distinct()[:20]
    for pos in positions:
        print(f"  {pos}")
    print()
    
    # Manager relationships
    print("Manager relationships:")
    with_manager = employees.filter(manager__isnull=False).count()
    without_manager = employees.filter(manager__isnull=True).count()
    print(f"  With manager: {with_manager}")
    print(f"  Without manager: {without_manager}")
    print()
    
    # Hierarchy levels
    print("Hierarchy levels:")
    hierarchy_levels = employees.values_list('hierarchy_level', flat=True).distinct()
    for level in sorted(hierarchy_levels):
        if level is not None:
            count = employees.filter(hierarchy_level=level).count()
            print(f"  Level {level}: {count} employees")
    null_levels = employees.filter(hierarchy_level__isnull=True).count()
    if null_levels > 0:
        print(f"  NULL level: {null_levels} employees")
    print()
    
    # Hire dates for seniority analysis
    print("Hire date range:")
    oldest = employees.order_by('hire_date').first()
    newest = employees.order_by('-hire_date').first()
    if oldest and newest:
        print(f"  Oldest hire: {oldest.hire_date} ({oldest.first_name} {oldest.last_name})")
        print(f"  Newest hire: {newest.hire_date} ({newest.first_name} {newest.last_name})")
    print()
    
    # Potential CEO candidates (senior positions)
    senior_keywords = ['CEO', 'Chief', 'Director', 'President', 'VP', 'Vice President', 'Executive']
    print("Potential senior employees:")
    senior_employees = employees.filter(
        position_title__icontains=senior_keywords[0]
    )
    for keyword in senior_keywords[1:]:
        senior_employees = senior_employees | employees.filter(position_title__icontains=keyword)
    
    for emp in senior_employees.order_by('hire_date')[:10]:
        print(f"  {emp.position_title} - {emp.first_name} {emp.last_name} - {emp.hire_date}")
    
    print(f"\nTotal senior candidates found: {senior_employees.count()}")

if __name__ == '__main__':
    analyze_employee_data()
