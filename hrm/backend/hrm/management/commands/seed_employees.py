"""
Enhanced Seed Employees Command - HRM Domain
Following platform.cline governance - Create comprehensive seed data for testing and development
"""

import uuid
import random
from datetime import date, timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.models import User
from hrm.models.employee import EmployeeRecord, EmployeeAddress


class Command(BaseCommand):
    help = 'Create comprehensive seed employee data for testing and development'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=100,
            help='Number of employees to create'
        )
        parser.add_argument(
            '--with-addresses',
            action='store_true',
            help='Create addresses for employees'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing employee records before creating new ones'
        )
        parser.add_argument(
            '--diverse-data',
            action='store_true',
            help='Create diverse employee data with various statuses and types'
        )

    def handle(self, *args, **options):
        count = options['count']
        with_addresses = options['with_addresses']
        clear_existing = options['clear']
        diverse_data = options['diverse_data']
        
        # Clear existing data if requested
        if clear_existing:
            self.clear_existing_data()
        
        # Create seed data
        with transaction.atomic():
            employees = self.create_employees(count, diverse_data)
            
            if with_addresses:
                self.create_addresses(employees)
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created {len(employees)} employees')
            )
            if with_addresses:
                self.stdout.write(
                    self.style.SUCCESS(f'Created addresses for {len(employees)} employees')
                )

    def clear_existing_data(self):
        """Clear existing employee and address records"""
        EmployeeAddress.objects.all().delete()
        EmployeeRecord.objects.all().delete()
        self.stdout.write(self.style.WARNING('Cleared existing employee and address records'))

    def create_employees(self, count, diverse_data=False):
        """Create hierarchical employee structure with comprehensive data"""
        
        # Define departments and job titles
        departments = [
            'Engineering', 'Human Resources', 'Finance', 'Marketing', 'Sales',
            'Operations', 'Customer Support', 'Product', 'Design', 'Legal'
        ]
        
        job_titles = {
            'Engineering': [
                'CTO', 'VP of Engineering', 'Engineering Manager', 'Senior Software Engineer',
                'Software Engineer', 'Junior Software Engineer', 'DevOps Engineer', 'QA Engineer',
                'Technical Lead', 'Principal Engineer', 'Staff Engineer', 'Frontend Developer',
                'Backend Developer', 'Full Stack Developer', 'Mobile Developer'
            ],
            'Human Resources': [
                'CHRO', 'HR Director', 'HR Manager', 'HR Business Partner', 'Recruiter',
                'HR Coordinator', 'Training Specialist', 'Compensation Analyst', 'HR Generalist',
                'Talent Acquisition Specialist', 'Learning & Development Manager', 'HRIS Specialist'
            ],
            'Finance': [
                'CFO', 'Finance Director', 'Finance Manager', 'Senior Accountant', 'Accountant',
                'Financial Analyst', 'Payroll Specialist', 'Billing Specialist', 'Controller',
                'Tax Manager', 'Treasury Analyst', 'Cost Accountant', 'Financial Planner'
            ],
            'Marketing': [
                'CMO', 'Marketing Director', 'Marketing Manager', 'Product Marketing Manager',
                'Content Manager', 'Social Media Specialist', 'SEO Specialist', 'Graphic Designer',
                'Brand Manager', 'Digital Marketing Manager', 'Marketing Analyst', 'PR Specialist'
            ],
            'Sales': [
                'VP of Sales', 'Sales Director', 'Regional Sales Manager', 'Sales Manager',
                'Account Executive', 'Sales Development Rep', 'Customer Success Manager',
                'Sales Engineer', 'Business Development Manager', 'Key Account Manager'
            ],
            'Operations': [
                'COO', 'Operations Director', 'Operations Manager', 'Process Improvement Manager',
                'Supply Chain Manager', 'Logistics Coordinator', 'Quality Assurance Manager',
                'Facilities Manager', 'Inventory Manager', 'Procurement Manager'
            ],
            'Customer Support': [
                'Support Director', 'Support Manager', 'Team Lead', 'Senior Support Specialist',
                'Support Specialist', 'Technical Support Engineer', 'Customer Success Rep',
                'Support Analyst', 'Knowledge Base Manager'
            ],
            'Product': [
                'CPO', 'Product Director', 'Senior Product Manager', 'Product Manager',
                'Associate Product Manager', 'Product Analyst', 'Product Owner', 'Growth Product Manager'
            ],
            'Design': [
                'Design Director', 'Design Manager', 'Senior UX Designer', 'UX Designer',
                'UI Designer', 'Visual Designer', 'Researcher', 'Design System Lead',
                'Product Designer', 'Interaction Designer'
            ],
            'Legal': [
                'General Counsel', 'Legal Director', 'Senior Counsel', 'Corporate Counsel',
                'Paralegal', 'Contract Specialist', 'Compliance Officer', 'IP Counsel'
            ]
        }
        
        # Comprehensive name lists
        first_names = [
            'James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda',
            'William', 'Elizabeth', 'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica',
            'Thomas', 'Sarah', 'Charles', 'Karen', 'Christopher', 'Nancy', 'Daniel', 'Lisa',
            'Matthew', 'Betty', 'Anthony', 'Helen', 'Mark', 'Sandra', 'Donald', 'Donna',
            'Steven', 'Carol', 'Paul', 'Ruth', 'Andrew', 'Sharon', 'Joshua', 'Michelle',
            'Kevin', 'Laura', 'Brian', 'Ashley', 'George', 'Kimberly', 'Edward', 'Dorothy',
            'Ronald', 'Lisa', 'Timothy', 'Nancy', 'Jason', 'Betty', 'Jeffrey', 'Helen',
            'Ryan', 'Emily', 'Jacob', 'Stephanie', 'Gary', 'Maria', 'Nicholas', 'Heather',
            'Eric', 'Shannon', 'Jonathan', 'Amy', 'Stephen', 'Angela', 'Larry', 'Anna',
            'Justin', 'Brenda', 'Scott', 'Pamela', 'Brandon', 'Katherine', 'Benjamin', 'Nicole',
            'Samuel', 'Kathryn', 'Gregory', 'Victoria', 'Frank', 'Rachel', 'Alexander', 'Megan'
        ]
        
        last_names = [
            'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
            'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
            'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson',
            'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker',
            'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores',
            'Green', 'Adams', 'Baker', 'Gonzalez', 'Nelson', 'Carter', 'Mitchell', 'Roberts',
            'Turner', 'Phillips', 'Campbell', 'Parker', 'Evans', 'Edwards', 'Collins', 'Stewart',
            'Sanchez', 'Morris', 'Rogers', 'Reed', 'Cook', 'Morgan', 'Bell', 'Murphy', 'Bailey',
            'Rivera', 'Cooper', 'Richardson', 'Cox', 'Howard', 'Ward', 'Torres', 'Peterson',
            'Gray', 'Ramirez', 'James', 'Watson', 'Brooks', 'Kelly', 'Sanders', 'Price',
            'Bennett', 'Wood', 'Barnes', 'Ross', 'Henderson', 'Coleman', 'Jenkins', 'Perry'
        ]
        
        # Employment types and statuses for diverse data
        employment_types = ['FULL_TIME', 'PART_TIME', 'CONTRACT', 'INTERN', 'TEMPORARY', 'CONSULTANT']
        employment_statuses = ['ACTIVE', 'ON_LEAVE', 'TERMINATED', 'RETIREMENT', 'CONTRACT_END']
        genders = ['MALE', 'FEMALE', 'NON_BINARY', 'PREFER_NOT_TO_SAY']
        marital_statuses = ['SINGLE', 'MARRIED', 'DIVORCED', 'SEPARATED', 'WIDOWED', 'DOMESTIC_PARTNERSHIP']
        
        employees = []
        
        # Create or get admin user for created_by_user field
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@company.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        # Create CEO (top level)
        ceo = EmployeeRecord.objects.create(
            id=uuid.uuid4(),
            company_code='DEFAULT',
            employee_number='EMP0001',
            first_name='Robert',
            last_name='Johnson',
            middle_name='William',
            preferred_name='Bob',
            name_prefix='Mr.',
            name_suffix='Jr.',
            gender='MALE',
            date_of_birth=date(1980, 1, 15),
            marital_status='MARRIED',
            work_email='robert.johnson@company.com',
            personal_email='bob.johnson.personal@gmail.com',
            work_phone='555-0101',
            mobile_phone='555-0102',
            home_phone='555-0103',
            hire_date=date(2020, 1, 15),
            original_hire_date=date(2020, 1, 15),
            employment_status='ACTIVE',
            employment_type='FULL_TIME',
            position_title='CEO',
            department_name='Executive',
            job_category='Executive',
            job_level='L1',
            job_family='Leadership',
            work_location_name='Headquarters',
            remote_work_eligible=True,
            remote_work_percentage=50,
            manager=None,  # CEO has no manager
            hr_business_partner_name='Sarah Williams',
            salary_grade='EXEC',
            salary_step='1',
            annual_salary=Decimal('250000.00'),
            currency='USD',
            pay_frequency='ANNUAL',
            benefits_eligibility_date=date(2020, 1, 15),
            benefits_package_name='Executive Package',
            health_insurance_eligible=True,
            dental_insurance_eligible=True,
            vision_insurance_eligible=True,
            retirement_plan_eligible=True,
            life_insurance_eligible=True,
            primary_emergency_contact_name='Mary Johnson',
            primary_emergency_contact_relationship='Spouse',
            primary_emergency_contact_phone='555-0104',
            secondary_emergency_contact_name='William Johnson',
            secondary_emergency_contact_relationship='Father',
            secondary_emergency_contact_phone='555-0105',
            is_active=True,
            is_confidential=False,
            is_key_employee=True,
            is_high_potential=False,
            username='rjohnson',
            role='CEO',
            created_by_user=admin_user
        )
        employees.append(ceo)
        
        # Create remaining employees
        for i in range(1, min(count, len(first_names) * len(last_names))):
            dept = self.get_random_name(departments)
            titles = job_titles.get(dept, ['Software Engineer'])
            title = self.get_random_name(titles)
            
            # Generate diverse data if requested
            if diverse_data:
                emp_type = self.get_weighted_random(employment_types, [0.7, 0.15, 0.08, 0.04, 0.02, 0.01])
                emp_status = self.get_weighted_random(employment_statuses, [0.85, 0.08, 0.05, 0.01, 0.01])
                gender = self.get_random_name(genders)
                marital_status = self.get_random_name(marital_statuses)
                
                # Set termination date if terminated
                termination_date = None
                termination_reason = None
                if emp_status == 'TERMINATED':
                    termination_date = date(2023, random.randint(1, 12), random.randint(1, 28))
                    termination_reason = self.get_random_name([
                        'Resignation', 'Termination', 'Retirement', 'Contract End', 'Layoff'
                    ])
            else:
                emp_type = 'FULL_TIME'
                emp_status = 'ACTIVE'
                gender = 'MALE' if i % 2 == 0 else 'FEMALE'
                marital_status = 'SINGLE'
                termination_date = None
                termination_reason = None
            
            # Calculate salary based on job level and type
            base_salary = 60000 + (i % 10) * 10000
            if emp_type == 'PART_TIME':
                base_salary *= 0.6
            elif emp_type == 'CONTRACT':
                base_salary *= 1.2
            elif emp_type == 'INTERN':
                base_salary *= 0.4
            
            # Generate hire date
            hire_date = date(2020, 1, 1) + timedelta(days=random.randint(0, 1460))  # Last 4 years
            
            employee = EmployeeRecord.objects.create(
                id=uuid.uuid4(),
                company_code='DEFAULT',
                employee_number=f'EMP{i + 1:04d}',
                first_name=self.get_random_name(first_names),
                last_name=self.get_random_name(last_names),
                middle_name=self.get_random_name(['A', 'B', 'C', 'D', 'E']) if random.random() > 0.7 else None,
                preferred_name=self.get_random_name(first_names) if random.random() > 0.8 else None,
                name_prefix=random.choice(['Mr.', 'Ms.', 'Mrs.', 'Dr.']) if random.random() > 0.6 else None,
                gender=gender,
                date_of_birth=date(1980 + random.randint(22, 45), random.randint(1, 12), random.randint(1, 28)),
                marital_status=marital_status,
                work_email=f'employee{i + 1}@company.com',
                personal_email=f'personal{i + 1}@gmail.com' if random.random() > 0.3 else None,
                work_phone=f'555-{i + 1:04d}',
                mobile_phone=f'555-{i + 1000:04d}' if random.random() > 0.2 else None,
                home_phone=f'555-{i + 2000:04d}' if random.random() > 0.5 else None,
                hire_date=hire_date,
                original_hire_date=hire_date if random.random() > 0.1 else None,
                employment_status=emp_status,
                employment_type=emp_type,
                position_title=title,
                department_name=dept,
                job_category=self.get_random_name(['Technical', 'Professional', 'Managerial', 'Executive']),
                job_level=f'L{((i % 8) + 2)}',
                job_family=self.get_random_name(['Engineering', 'Business', 'Support', 'Leadership']),
                work_location_name=self.get_random_name(['Headquarters', 'Remote', 'Office A', 'Office B']),
                remote_work_eligible=random.choice([True, False]),
                remote_work_percentage=random.randint(0, 100) if random.random() > 0.5 else 0,
                manager=ceo if i < 10 else None,  # First 10 report to CEO, others will be assigned later
                hr_business_partner_name='Sarah Williams',
                salary_grade=f'G{((i % 5) + 1)}',
                salary_step=f'S{((i % 3) + 1)}',
                annual_salary=Decimal(str(base_salary)),
                hourly_rate=Decimal(str(base_salary / 2080)) if emp_type in ['PART_TIME', 'CONTRACT'] else None,
                currency='USD',
                pay_frequency=self.get_random_name(['HOURLY', 'WEEKLY', 'BI_WEEKLY', 'SEMI_MONTHLY', 'MONTHLY']),
                benefits_eligibility_date=hire_date + timedelta(days=90) if emp_type == 'FULL_TIME' else None,
                benefits_package_name=self.get_random_name(['Standard', 'Premium', 'Basic']) if emp_type == 'FULL_TIME' else None,
                health_insurance_eligible=emp_type == 'FULL_TIME',
                dental_insurance_eligible=emp_type == 'FULL_TIME' and random.random() > 0.2,
                vision_insurance_eligible=emp_type == 'FULL_TIME' and random.random() > 0.3,
                retirement_plan_eligible=emp_type == 'FULL_TIME' and random.random() > 0.1,
                life_insurance_eligible=emp_type == 'FULL_TIME' and random.random() > 0.4,
                primary_emergency_contact_name=f'Contact {i + 1}',
                primary_emergency_contact_relationship=self.get_random_name(['Spouse', 'Parent', 'Sibling', 'Friend']),
                primary_emergency_contact_phone=f'555-{i + 3000:04d}',
                secondary_emergency_contact_name=f'Emergency {i + 1}' if random.random() > 0.5 else None,
                secondary_emergency_contact_relationship=self.get_random_name(['Parent', 'Sibling', 'Friend']) if random.random() > 0.5 else None,
                secondary_emergency_contact_phone=f'555-{i + 4000:04d}' if random.random() > 0.5 else None,
                is_active=emp_status == 'ACTIVE',
                is_confidential=random.choice([True, False]) if random.random() > 0.95 else False,
                is_key_employee=random.choice([True, False]) if random.random() > 0.9 else False,
                is_high_potential=random.choice([True, False]) if random.random() > 0.85 else False,
                termination_date=termination_date,
                termination_reason=termination_reason,
                rehire_eligible=random.choice([True, False]) if termination_date else True,
                username=f'employee{i + 1}',
                role=self.get_random_name(['Employee', 'Manager', 'Lead', 'Specialist']),
                created_by_user=admin_user
            )
            employees.append(employee)
        
        return employees

    def create_addresses(self, employees):
        """Create addresses for employees"""
        address_types = ['HOME', 'WORK', 'MAILING', 'TEMPORARY']
        cities = [
            'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia',
            'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville',
            'Fort Worth', 'Columbus', 'Charlotte', 'San Francisco', 'Indianapolis',
            'Seattle', 'Denver', 'Washington'
        ]
        states = [
            'NY', 'CA', 'IL', 'TX', 'AZ', 'PA', 'FL', 'OH', 'NC', 'WA', 'CO', 'DC'
        ]
        
        for employee in employees:
            # Create 1-3 addresses per employee
            num_addresses = random.randint(1, 3)
            
            for i in range(num_addresses):
                address_type = address_types[i] if i < len(address_types) else 'HOME'
                is_primary = (i == 0)  # First address is primary
                
                EmployeeAddress.objects.create(
                    id=uuid.uuid4(),
                    company_code=employee.company_code,
                    employee=employee,
                    address_type=address_type,
                    address_line_1=f'{random.randint(100, 9999)} {self.get_random_name(["Main", "Oak", "Pine", "Maple", "Cedar", "Elm"])} {self.get_random_name(["St", "Ave", "Dr", "Ln", "Blvd", "Rd"])}',
                    address_line_2=f'Apt {random.randint(1, 999)}' if random.random() > 0.6 else None,
                    city=self.get_random_name(cities),
                    state=self.get_random_name(states),
                    postal_code=f'{random.randint(10000, 99999)}',
                    country='USA',
                    is_primary=is_primary,
                    is_active=True
                )

    def get_random_name(self, names):
        """Get a random name from the list"""
        return random.choice(names)

    def get_weighted_random(self, choices, weights):
        """Get a random choice with weighted probabilities"""
        return random.choices(choices, weights=weights)[0]
