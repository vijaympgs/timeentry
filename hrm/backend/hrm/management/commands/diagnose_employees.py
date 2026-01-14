"""
Management command to diagnose existing employee data
"""

from django.core.management.base import BaseCommand
from hrm.models.employee import EmployeeRecord


class Command(BaseCommand):
    help = 'Diagnose existing employee data structure'

    def add_arguments(self, parser):
        parser.add_argument(
            '--company-code',
            type=str,
            help='Filter by specific company code'
        )

    def handle(self, *args, **options):
        company_code = options.get('company_code')
        
        self.stdout.write("=== EMPLOYEE DATA DIAGNOSIS ===\n")
        
        # Check all employees
        all_employees = EmployeeRecord.objects.all()
        self.stdout.write(f"Total employees in database: {all_employees.count()}")
        
        if all_employees.exists():
            # Check company codes
            company_codes = all_employees.values_list('company_code', flat=True).distinct()
            self.stdout.write(f"\nCompany codes found: {list(company_codes)}")
            
            for code in company_codes:
                count = all_employees.filter(company_code=code).count()
                self.stdout.write(f"  {code}: {count} employees")
            
            # Show sample employees
            self.stdout.write(f"\nSample employees:")
            for i, emp in enumerate(all_employees[:10]):
                self.stdout.write(f"  {i+1}. {emp.company_code} - {emp.employee_number} - {emp.first_name} {emp.last_name} - {emp.department_name}")
        else:
            self.stdout.write("No employees found in database!")
            return
        
        # If specific company code requested, show details
        if company_code:
            employees = all_employees.filter(company_code=company_code)
            self.stdout.write(f"\n=== DETAILS FOR COMPANY {company_code} ===\n")
            
            if employees.exists():
                self.stdout.write(f"Employees: {employees.count()}")
                
                # Departments
                departments = employees.values_list('department_name', flat=True).distinct()
                self.stdout.write(f"\nDepartments ({len(departments)}):")
                for dept in sorted(departments):
                    count = employees.filter(department_name=dept).count()
                    self.stdout.write(f"  {dept}: {count} employees")
                
                # Position titles
                positions = employees.values_list('position_title', flat=True).distinct()
                self.stdout.write(f"\nPosition titles ({len(positions)}):")
                for pos in sorted(positions)[:20]:  # Show first 20
                    self.stdout.write(f"  {pos}")
                if len(positions) > 20:
                    self.stdout.write(f"  ... and {len(positions) - 20} more")
                
                # Manager relationships
                with_manager = employees.filter(manager__isnull=False).count()
                without_manager = employees.filter(manager__isnull=True).count()
                self.stdout.write(f"\nManager relationships:")
                self.stdout.write(f"  With manager: {with_manager}")
                self.stdout.write(f"  Without manager: {without_manager}")
                
                # Hierarchy levels
                hierarchy_levels = employees.values_list('hierarchy_level', flat=True).distinct()
                null_levels = employees.filter(hierarchy_level__isnull=True).count()
                self.stdout.write(f"\nHierarchy levels:")
                for level in sorted([h for h in hierarchy_levels if h is not None]):
                    count = employees.filter(hierarchy_level=level).count()
                    self.stdout.write(f"  Level {level}: {count} employees")
                if null_levels > 0:
                    self.stdout.write(f"  NULL level: {null_levels} employees")
            else:
                self.stdout.write(f"No employees found for company code: {company_code}")
