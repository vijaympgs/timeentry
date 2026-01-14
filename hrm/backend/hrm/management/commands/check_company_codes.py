"""
Management command to check company codes and employee data
"""

from django.core.management.base import BaseCommand
from hrm.models.employee import EmployeeRecord


class Command(BaseCommand):
    help = 'Check company codes and employee data in the database'

    def handle(self, *args, **options):
        self.stdout.write("Checking company codes and employee data...\n")
        
        # Check all company codes
        company_codes = EmployeeRecord.objects.values_list('company_code', flat=True).distinct()
        self.stdout.write(f"Company codes found: {list(company_codes)}\n")
        
        # Check employees by company code
        for company_code in company_codes:
            count = EmployeeRecord.objects.filter(company_code=company_code).count()
            self.stdout.write(f"Company '{company_code}': {count} employees")
            
            # Check for CEO (no manager, hierarchy_level=0)
            ceos = EmployeeRecord.objects.filter(
                company_code=company_code,
                manager__isnull=True,
                hierarchy_level=0
            )
            self.stdout.write(f"  CEOs (no manager, level 0): {ceos.count()}")
            for ceo in ceos:
                self.stdout.write(f"    - {ceo.first_name} {ceo.last_name} ({ceo.employee_number})")
            
            # Check manager relationships
            with_manager = EmployeeRecord.objects.filter(
                company_code=company_code,
                manager__isnull=False
            ).count()
            without_manager = EmployeeRecord.objects.filter(
                company_code=company_code,
                manager__isnull=True
            ).count()
            self.stdout.write(f"  With manager: {with_manager}")
            self.stdout.write(f"  Without manager: {without_manager}")
            
            # Check hierarchy levels
            levels = EmployeeRecord.objects.filter(
                company_code=company_code
            ).values_list('hierarchy_level', flat=True).distinct()
            self.stdout.write(f"  Hierarchy levels: {sorted(list(levels))}")
            self.stdout.write("")
        
        # Show some sample employees
        self.stdout.write("Sample employees:")
        employees = EmployeeRecord.objects.all()[:10]
        for emp in employees:
            manager_name = f"{emp.manager.first_name} {emp.manager.last_name}" if emp.manager else "None"
            self.stdout.write(f"  {emp.employee_number} - {emp.first_name} {emp.last_name} - Company: {emp.company_code} - Manager: {manager_name} - Level: {emp.hierarchy_level}")
