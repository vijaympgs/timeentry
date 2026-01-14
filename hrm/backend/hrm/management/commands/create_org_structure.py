"""
Management command to create organizational structure using existing employees only
Idempotent implementation that works with authoritative employee data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from hrm.models.employee import EmployeeRecord
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Create organizational structure using existing employees only (no new inserts)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--company-code',
            type=str,
            default='DEFAULT',
            help='Company code for the employees'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force recreation of organizational structure (clears hierarchy only)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without making changes'
        )

    def handle(self, *args, **options):
        company_code = options['company_code']
        force = options['force']
        dry_run = options['dry_run']
        
        self.stdout.write(f"Creating organizational structure for company: {company_code}\n")
        
        if dry_run:
            self.stdout.write("DRY RUN MODE - No changes will be made\n")
        
        with transaction.atomic():
            # Get all existing employees for this company
            employees = EmployeeRecord.objects.filter(company_code=company_code)
            
            if not employees.exists():
                self.stdout.write(
                    self.style.ERROR(f"No employees found for company {company_code}. Cannot create org structure.\n")
                )
                return
            
            self.stdout.write(f"Found {employees.count()} existing employees\n")
            
            if force:
                self.stdout.write("Force flag detected - clearing existing hierarchy structure...\n")
                if not dry_run:
                    # Clear only hierarchy-related fields, not employee records
                    updated_count = employees.update(
                        manager=None,
                        hierarchy_level=None
                    )
                    self.stdout.write(f"Cleared hierarchy for {updated_count} employees.\n")
            
            # Analyze existing data structure
            self.analyze_existing_data(employees)
            
            # Build organizational structure using existing employees
            org_structure = self.build_org_structure(employees)
            
            if dry_run:
                self.stdout.write("\nDRY RUN SUMMARY:")
                self.stdout.write(f"CEO: {org_structure['ceo'].first_name} {org_structure['ceo'].last_name}")
                self.stdout.write(f"Department Heads: {len(org_structure['department_heads'])}")
                self.stdout.write(f"Managers: {len(org_structure['managers'])}")
                self.stdout.write(f"Reportees: {len(org_structure['reportees'])}")
                return
            
            # Apply the organizational structure
            self.apply_org_structure(org_structure, company_code)
            
            # Show final statistics
            self.show_final_statistics(company_code)

    def analyze_existing_data(self, employees):
        """Analyze existing employee data structure"""
        self.stdout.write("\nANALYZING EXISTING DATA:\n")
        
        # Department analysis
        departments = employees.values_list('department_name', flat=True).distinct()
        self.stdout.write(f"Departments found: {len(departments)}")
        for dept in sorted(departments):
            count = employees.filter(department_name=dept).count()
            self.stdout.write(f"  {dept}: {count} employees")
        
        # Position title analysis
        positions = employees.values_list('position_title', flat=True).distinct()
        self.stdout.write(f"\nUnique position titles: {len(positions)}")
        
        # Manager relationship analysis
        with_manager = employees.filter(manager__isnull=False).count()
        without_manager = employees.filter(manager__isnull=True).count()
        self.stdout.write(f"\nManager relationships:")
        self.stdout.write(f"  With manager: {with_manager}")
        self.stdout.write(f"  Without manager: {without_manager}")
        
        # Hierarchy level analysis
        hierarchy_levels = employees.values_list('hierarchy_level', flat=True).distinct()
        null_levels = employees.filter(hierarchy_level__isnull=True).count()
        self.stdout.write(f"\nHierarchy levels:")
        for level in sorted([h for h in hierarchy_levels if h is not None]):
            count = employees.filter(hierarchy_level=level).count()
            self.stdout.write(f"  Level {level}: {count} employees")
        if null_levels > 0:
            self.stdout.write(f"  NULL level: {null_levels} employees")

    def build_org_structure(self, employees):
        """Build organizational structure using existing employees"""
        self.stdout.write("\nBUILDING ORGANIZATIONAL STRUCTURE:\n")
        
        org_structure = {
            'ceo': None,
            'department_heads': {},
            'managers': {},
            'reportees': []
        }
        
        # Step 1: Identify CEO (most senior employee)
        # Strategy: Look for CEO/Chief/Executive titles, fallback to earliest hire date
        senior_keywords = ['CEO', 'Chief', 'President', 'Executive', 'Director']
        ceo_candidates = employees.none()
        
        for keyword in senior_keywords:
            candidates = employees.filter(position_title__icontains=keyword)
            ceo_candidates = ceo_candidates | candidates
        
        if ceo_candidates.exists():
            # Choose the most senior by hire date
            org_structure['ceo'] = ceo_candidates.order_by('hire_date').first()
            self.stdout.write(f"+ CEO identified: {org_structure['ceo'].position_title} - {org_structure['ceo'].first_name} {org_structure['ceo'].last_name}")
        else:
            # Fallback: Employee with earliest hire date
            org_structure['ceo'] = employees.order_by('hire_date').first()
            self.stdout.write(f"+ CEO (fallback): {org_structure['ceo'].position_title} - {org_structure['ceo'].first_name} {org_structure['ceo'].last_name}")
        
        # Step 2: Identify department heads
        departments = employees.values_list('department_name', flat=True).distinct()
        
        for dept in departments:
            dept_employees = employees.filter(department_name=dept)
            
            # Strategy: Look for Manager/Lead/Head in position title
            manager_keywords = ['Manager', 'Lead', 'Head', 'Supervisor', 'Director']
            dept_head_candidates = dept_employees.none()
            
            for keyword in manager_keywords:
                candidates = dept_employees.filter(position_title__icontains=keyword)
                dept_head_candidates = dept_head_candidates | candidates
            
            if dept_head_candidates.exists():
                # Choose most senior by hire date
                dept_head = dept_head_candidates.order_by('hire_date').first()
                org_structure['department_heads'][dept] = dept_head
                self.stdout.write(f"+ Department Head ({dept}): {dept_head.position_title} - {dept_head.first_name} {dept_head.last_name}")
            else:
                # Fallback: Most senior employee in department
                dept_head = dept_employees.order_by('hire_date').first()
                org_structure['department_heads'][dept] = dept_head
                self.stdout.write(f"✓ Department Head ({dept}, fallback): {dept_head.position_title} - {dept_head.first_name} {dept_head.last_name}")
        
        # Step 3: Identify managers (employees who can be managers)
        # Strategy: Employees with Manager/Lead/Supervisor in title, excluding department heads
        manager_keywords = ['Manager', 'Lead', 'Supervisor']
        potential_managers = employees.none()
        
        for keyword in manager_keywords:
            candidates = employees.filter(position_title__icontains=keyword)
            potential_managers = potential_managers | candidates
        
        # Exclude department heads
        dept_head_ids = [emp.id for emp in org_structure['department_heads'].values()]
        potential_managers = potential_managers.exclude(id__in=dept_head_ids)
        
        # Assign managers to departments (up to 3 per department)
        for dept in departments:
            dept_employees = potential_managers.filter(department_name=dept)
            dept_managers = dept_employees[:3]  # Limit to 3 managers per department
            
            for i, manager in enumerate(dept_managers):
                manager_key = f"{dept}_manager_{i+1}"
                org_structure['managers'][manager_key] = manager
                self.stdout.write(f"✓ Manager ({dept} #{i+1}): {manager.position_title} - {manager.first_name} {manager.last_name}")
        
        # Step 4: All other employees are reportees
        managed_ids = [org_structure['ceo'].id] + [emp.id for emp in org_structure['department_heads'].values()] + [emp.id for emp in org_structure['managers'].values()]
        org_structure['reportees'] = employees.exclude(id__in=managed_ids)
        
        self.stdout.write(f"✓ Reportees: {len(org_structure['reportees'])}")
        
        return org_structure

    def apply_org_structure(self, org_structure, company_code):
        """Apply the organizational structure using bulk updates"""
        self.stdout.write(f"\nAPPLYING ORGANIZATIONAL STRUCTURE:\n")
        
        updates = []
        
        # Update CEO
        ceo = org_structure['ceo']
        updates.append(ceo)
        ceo.hierarchy_level = 0
        ceo.manager = None
        self.stdout.write(f"✓ Updated CEO: {ceo.first_name} {ceo.last_name} (Level 0)")
        
        # Update department heads
        for dept, dept_head in org_structure['department_heads'].items():
            updates.append(dept_head)
            dept_head.hierarchy_level = 1
            dept_head.manager = org_structure['ceo']
            self.stdout.write(f"✓ Updated Department Head ({dept}): {dept_head.first_name} {dept_head.last_name} (Level 1)")
        
        # Update managers
        for manager_key, manager in org_structure['managers'].items():
            dept_name = manager_key.split('_manager_')[0]
            dept_head = org_structure['department_heads'].get(dept_name)
            
            updates.append(manager)
            manager.hierarchy_level = 2
            manager.manager = dept_head
            self.stdout.write(f"✓ Updated Manager ({manager_key}): {manager.first_name} {manager.last_name} (Level 2)")
        
        # Update reportees
        for reportee in org_structure['reportees']:
            # Assign to appropriate manager based on department
            dept_name = reportee.department_name
            dept_head = org_structure['department_heads'].get(dept_name)
            
            if dept_head:
                # Find first available manager in the department
                dept_managers = [emp for emp in org_structure['managers'].values() 
                                if emp.department_name == dept_name]
                
                if dept_managers:
                    # Assign to first available manager (round-robin)
                    manager_index = hash(reportee.employee_number) % len(dept_managers)
                    assigned_manager = dept_managers[manager_index]
                    
                    updates.append(reportee)
                    reportee.hierarchy_level = 3
                    reportee.manager = assigned_manager
                    self.stdout.write(f"✓ Updated Reportee: {reportee.first_name} {reportee.last_name} -> {assigned_manager.first_name} {assigned_manager.last_name} (Level 3)")
                else:
                    # Report directly to department head
                    updates.append(reportee)
                    reportee.hierarchy_level = 3
                    reportee.manager = dept_head
                    self.stdout.write(f"✓ Updated Reportee: {reportee.first_name} {reportee.last_name} -> {dept_head.first_name} {dept_head.last_name} (Level 3)")
            else:
                # No department head found, assign to CEO
                updates.append(reportee)
                reportee.hierarchy_level = 3
                reportee.manager = org_structure['ceo']
                self.stdout.write(f"✓ Updated Reportee: {reportee.first_name} {reportee.last_name} -> CEO (Level 3)")
        
        # Bulk update all employees
        if updates:
            EmployeeRecord.objects.bulk_update(
                updates,
                ['hierarchy_level', 'manager']
            )
            self.stdout.write(f"\n✅ Bulk updated {len(updates)} employees successfully")

    def show_final_statistics(self, company_code):
        """Show final organizational structure statistics"""
        self.stdout.write(f"\nFINAL ORGANIZATIONAL STRUCTURE:\n")
        
        employees = EmployeeRecord.objects.filter(company_code=company_code)
        
        # Count by hierarchy level
        level_counts = {}
        for level in range(5):  # 0-4 levels
            count = employees.filter(hierarchy_level=level).count()
            if count > 0:
                level_counts[f'Level {level}'] = count
        
        for level, count in level_counts.items():
            self.stdout.write(f"  {level}: {count} employees")
        
        # Manager relationship summary
        with_manager = employees.filter(manager__isnull=False).count()
        without_manager = employees.filter(manager__isnull=True).count()
        
        self.stdout.write(f"\nManager Relationships:")
        self.stdout.write(f"  With manager: {with_manager}")
        self.stdout.write(f"  Without manager: {without_manager}")
        
        # Department summary
        departments = employees.values_list('department_name', flat=True).distinct()
        self.stdout.write(f"\nDepartments: {len(departments)}")
        
        total_employees = employees.count()
        self.stdout.write(f"\nTotal employees in organizational structure: {total_employees}")
