"""
Import Organization Chart from JSON - HRM Domain
Imports employee hierarchy from employee_data_273.json with proper L1-L5 levels
"""

import json
import uuid
from datetime import date
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.models import User
from hrm.models.employee import EmployeeRecord


class Command(BaseCommand):
    help = 'Import organization chart from employee_data_273.json with hierarchy levels'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='employee_data_273.json',
            help='Path to JSON file with employee data'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing employee records before importing'
        )

    def handle(self, *args, **options):
        json_file = options['file']
        clear_existing = options['clear']
        
        # Clear existing data if requested
        if clear_existing:
            EmployeeRecord.objects.all().delete()
            self.stdout.write(self.style.WARNING('Cleared existing employee records'))
        
        # Load JSON data
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {json_file}'))
            return
        
        nodes = data.get('nodeDataArray', [])
        self.stdout.write(f'Found {len(nodes)} employees in JSON file')
        
        # Get or create admin user
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={'is_staff': True, 'is_superuser': True}
        )
        
        # Import employees with hierarchy
        with transaction.atomic():
            employee_map = {}  # Map key to EmployeeRecord
            hierarchy_levels = {}  # Map key to hierarchy level
            
            # First pass: Calculate hierarchy levels
            self.calculate_hierarchy_levels(nodes, hierarchy_levels)
            
            # Second pass: Create all employees
            for node in nodes:
                employee = self.create_employee(node, hierarchy_levels, admin_user)
                employee_map[node['key']] = employee
            
            # Third pass: Set manager relationships
            for node in nodes:
                if 'parent' in node:
                    employee = employee_map[node['key']]
                    manager = employee_map.get(node['parent'])
                    if manager:
                        employee.manager = manager
                        employee.save(update_fields=['manager'])
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully imported {len(employee_map)} employees')
            )
            
            # Print hierarchy statistics
            level_counts = {}
            for level in hierarchy_levels.values():
                level_counts[level] = level_counts.get(level, 0) + 1
            
            self.stdout.write('\nHierarchy Level Distribution:')
            for level in sorted(level_counts.keys()):
                self.stdout.write(f'  L{level}: {level_counts[level]} employees')

    def calculate_hierarchy_levels(self, nodes, hierarchy_levels):
        """Calculate hierarchy level for each employee (L1-L5)"""
        # Build parent map
        parent_map = {}
        for node in nodes:
            if 'parent' in node:
                parent_map[node['key']] = node['parent']
        
        # Calculate levels recursively
        def get_level(key, visited=None):
            if visited is None:
                visited = set()
            
            if key in hierarchy_levels:
                return hierarchy_levels[key]
            
            if key in visited:
                return 1  # Circular reference, treat as L1
            
            visited.add(key)
            
            if key not in parent_map:
                # No parent = CEO = L1
                hierarchy_levels[key] = 1
                return 1
            
            parent_key = parent_map[key]
            parent_level = get_level(parent_key, visited)
            level = parent_level + 1
            hierarchy_levels[key] = level
            return level
        
        # Calculate level for all nodes
        for node in nodes:
            get_level(node['key'])

    def create_employee(self, node, hierarchy_levels, admin_user):
        """Create an EmployeeRecord from JSON node"""
        key = node['key']
        level = hierarchy_levels.get(key, 1)
        
        # Parse name
        name_parts = node['name'].split()
        first_name = name_parts[0] if len(name_parts) > 0 else 'Unknown'
        last_name = name_parts[-1] if len(name_parts) > 1 else 'Employee'
        middle_name = ' '.join(name_parts[1:-1]) if len(name_parts) > 2 else None
        
        # Generate employee number
        emp_number = f'EMP{key:04d}'
        
        # Determine salary based on level and title
        salary = self.calculate_salary(level, node.get('title', ''))
        
        # Create employee record
        employee = EmployeeRecord.objects.create(
            id=uuid.uuid4(),
            company_code='DEFAULT',
            employee_number=emp_number,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            date_of_birth=date(1980, 1, 1),  # Default DOB
            work_email=node.get('email', f'{emp_number.lower()}@company.com'),
            work_phone=node.get('phone', '(234) 555-0000'),
            hire_date=date(2020, 1, 1),
            original_hire_date=date(2020, 1, 1),
            employment_status='ACTIVE',
            employment_type='FULL_TIME',
            position_title=node.get('title', 'Employee'),
            department_name=node.get('dept', 'General'),
            job_level=f'L{level}',
            hierarchy_level=level,
            work_location_name='Headquarters',
            remote_work_eligible=True,
            remote_work_percentage=50 if level <= 2 else 20,
            manager=None,  # Will be set in third pass
            salary_grade=f'G{level}',
            salary_step='1',
            annual_salary=Decimal(str(salary)),
            currency='USD',
            pay_frequency='ANNUAL',
            is_active=True,
            is_key_employee=(level <= 2),
            username=f'user{key}',
            role=self.get_role_by_level(level),
            created_by_user=admin_user
        )
        
        return employee

    def calculate_salary(self, level, title):
        """Calculate salary based on hierarchy level and title"""
        base_salaries = {
            1: 250000,  # L1 - CEO
            2: 180000,  # L2 - VPs
            3: 120000,  # L3 - Directors/Managers
            4: 85000,   # L4 - Team Leads/Senior
            5: 65000,   # L5 - Individual Contributors
        }
        
        base = base_salaries.get(level, 60000)
        
        # Adjust for specific titles
        title_lower = title.lower()
        if 'ceo' in title_lower or 'chief' in title_lower:
            return base * 1.2
        elif 'vp' in title_lower or 'vice president' in title_lower:
            return base * 1.1
        elif 'director' in title_lower:
            return base * 1.05
        elif 'senior' in title_lower:
            return base * 1.1
        elif 'junior' in title_lower:
            return base * 0.9
        
        return base

    def get_role_by_level(self, level):
        """Get role name based on hierarchy level"""
        roles = {
            1: 'Executive',
            2: 'VP',
            3: 'Manager',
            4: 'Lead',
            5: 'Employee'
        }
        return roles.get(level, 'Employee')
