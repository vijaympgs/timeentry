"""
Management command to populate organizational hierarchy
Creates a realistic org chart with:
- 1 CEO (Level 1)
- 2 VPs (Level 2)
- 5 Directors (Level 3)
- 8 Managers (Level 4)
- 8 Senior Staff (Level 5)
- 251 Full Staff (Level 6)
Total: 275 employees
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from hrm.models.employee import EmployeeRecord
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Populate organizational hierarchy with realistic data'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing employees...')
        EmployeeRecord.objects.all().delete()
        
        self.stdout.write('Creating organizational hierarchy...')
        
        # Departments and positions
        departments = {
            'Executive': ['Chief Executive Officer', 'Chief Operating Officer'],
            'Engineering': ['VP Engineering', 'Director of Engineering', 'Engineering Manager', 'Senior Engineer', 'Software Engineer'],
            'Sales': ['VP Sales', 'Director of Sales', 'Sales Manager', 'Senior Sales Rep', 'Sales Representative'],
            'Marketing': ['Director of Marketing', 'Marketing Manager', 'Senior Marketing Specialist', 'Marketing Specialist'],
            'Operations': ['Director of Operations', 'Operations Manager', 'Senior Operations Analyst', 'Operations Analyst'],
            'Finance': ['Director of Finance', 'Finance Manager', 'Senior Accountant', 'Accountant'],
            'HR': ['Director of HR', 'HR Manager', 'Senior HR Specialist', 'HR Specialist'],
            'IT': ['Director of IT', 'IT Manager', 'Senior IT Specialist', 'IT Support'],
            'Customer Success': ['Director of Customer Success', 'CS Manager', 'Senior CS Rep', 'CS Representative'],
            'Product': ['Director of Product', 'Product Manager', 'Senior Product Analyst', 'Product Analyst'],
        }
        
        first_names = [
            'James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda',
            'William', 'Barbara', 'David', 'Elizabeth', 'Richard', 'Susan', 'Joseph', 'Jessica',
            'Thomas', 'Sarah', 'Charles', 'Karen', 'Christopher', 'Nancy', 'Daniel', 'Lisa',
            'Matthew', 'Betty', 'Anthony', 'Margaret', 'Mark', 'Sandra', 'Donald', 'Ashley',
            'Steven', 'Kimberly', 'Paul', 'Emily', 'Andrew', 'Donna', 'Joshua', 'Michelle',
            'Kenneth', 'Carol', 'Kevin', 'Amanda', 'Brian', 'Dorothy', 'George', 'Melissa',
            'Edward', 'Deborah', 'Ronald', 'Stephanie', 'Timothy', 'Rebecca', 'Jason', 'Sharon',
            'Jeffrey', 'Laura', 'Ryan', 'Cynthia', 'Jacob', 'Kathleen', 'Gary', 'Amy',
            'Nicholas', 'Shirley', 'Eric', 'Angela', 'Jonathan', 'Helen', 'Stephen', 'Anna',
            'Larry', 'Brenda', 'Justin', 'Pamela', 'Scott', 'Nicole', 'Brandon', 'Emma',
            'Benjamin', 'Samantha', 'Samuel', 'Katherine', 'Raymond', 'Christine', 'Gregory', 'Debra',
            'Frank', 'Rachel', 'Alexander', 'Catherine', 'Patrick', 'Carolyn', 'Raymond', 'Janet',
            'Jack', 'Ruth', 'Dennis', 'Maria', 'Jerry', 'Heather', 'Tyler', 'Diane',
            'Aaron', 'Virginia', 'Jose', 'Julie', 'Adam', 'Joyce', 'Henry', 'Victoria',
            'Nathan', 'Olivia', 'Douglas', 'Kelly', 'Zachary', 'Christina', 'Peter', 'Lauren',
            'Kyle', 'Joan', 'Walter', 'Evelyn', 'Ethan', 'Judith', 'Jeremy', 'Megan',
            'Harold', 'Cheryl', 'Keith', 'Andrea', 'Christian', 'Hannah', 'Roger', 'Jacqueline',
            'Noah', 'Martha', 'Gerald', 'Gloria', 'Carl', 'Teresa', 'Terry', 'Ann',
            'Sean', 'Sara', 'Austin', 'Madison', 'Arthur', 'Frances', 'Lawrence', 'Kathryn',
            'Jesse', 'Janice', 'Dylan', 'Jean', 'Bryan', 'Abigail', 'Joe', 'Sophia',
        ]
        
        last_names = [
            'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
            'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas',
            'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson', 'White',
            'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker', 'Young',
            'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores',
            'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell',
            'Carter', 'Roberts', 'Gomez', 'Phillips', 'Evans', 'Turner', 'Diaz', 'Parker',
            'Cruz', 'Edwards', 'Collins', 'Reyes', 'Stewart', 'Morris', 'Morales', 'Murphy',
            'Cook', 'Rogers', 'Gutierrez', 'Ortiz', 'Morgan', 'Cooper', 'Peterson', 'Bailey',
            'Reed', 'Kelly', 'Howard', 'Ramos', 'Kim', 'Cox', 'Ward', 'Richardson',
            'Watson', 'Brooks', 'Chavez', 'Wood', 'James', 'Bennett', 'Gray', 'Mendoza',
            'Ruiz', 'Hughes', 'Price', 'Alvarez', 'Castillo', 'Sanders', 'Patel', 'Myers',
            'Long', 'Ross', 'Foster', 'Jimenez', 'Powell', 'Jenkins', 'Perry', 'Russell',
            'Sullivan', 'Bell', 'Coleman', 'Butler', 'Henderson', 'Barnes', 'Gonzales', 'Fisher',
            'Vasquez', 'Simmons', 'Romero', 'Jordan', 'Patterson', 'Alexander', 'Hamilton', 'Graham',
            'Reynolds', 'Griffin', 'Wallace', 'Moreno', 'West', 'Cole', 'Hayes', 'Bryant',
            'Herrera', 'Gibson', 'Ellis', 'Tran', 'Medina', 'Aguilar', 'Stevens', 'Murray',
            'Ford', 'Castro', 'Marshall', 'Owens', 'Harrison', 'Fernandez', 'McDonald', 'Woods',
            'Washington', 'Kennedy', 'Wells', 'Vargas', 'Henry', 'Chen', 'Freeman', 'Webb',
            'Tucker', 'Guzman', 'Burns', 'Crawford', 'Olson', 'Simpson', 'Porter', 'Hunter',
        ]
        
        def generate_employee(emp_num, first, last, position, dept, manager=None, level=1):
            """Helper to create employee"""
            hire_date = datetime.now().date() - timedelta(days=random.randint(30, 3650))
            
            return EmployeeRecord.objects.create(
                employee_number=f'EMP{emp_num:05d}',
                first_name=first,
                last_name=last,
                middle_name='',
                gender=random.choice(['MALE', 'FEMALE']),
                date_of_birth=datetime.now().date() - timedelta(days=random.randint(8000, 20000)),
                marital_status=random.choice(['SINGLE', 'MARRIED', 'DIVORCED']),
                work_email=f'{first.lower()}.{last.lower()}@company.com',
                work_phone=f'+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}',
                hire_date=hire_date,
                employment_status='ACTIVE',
                employment_type='FULL_TIME',
                position_title=position,
                department_name=dept,
                job_level=f'L{level}',
                manager=manager,
                hierarchy_level=level - 1,  # 0-indexed
                annual_salary=random.randint(50000, 250000),
                currency='USD',
                pay_frequency='MONTHLY',
                is_active=True,
                username=f'{first.lower()}.{last.lower()}',
                role='Employee' if level > 1 else 'Executive'
            )
        
        emp_counter = 1
        used_names = set()
        
        def get_unique_name():
            """Get unique first/last name combination"""
            while True:
                first = random.choice(first_names)
                last = random.choice(last_names)
                name = f'{first}_{last}'
                if name not in used_names:
                    used_names.add(name)
                    return first, last
        
        # Level 1: CEO (1 employee)
        self.stdout.write('Creating Level 1: CEO...')
        first, last = get_unique_name()
        ceo = generate_employee(emp_counter, first, last, 'Chief Executive Officer', 'Executive', None, 1)
        emp_counter += 1
        self.stdout.write(self.style.SUCCESS(f'  Created: {ceo.full_name} - CEO'))
        
        # Level 2: VPs (2 employees)
        self.stdout.write('Creating Level 2: VPs...')
        vps = []
        vp_titles = ['VP Engineering', 'VP Sales']
        vp_depts = ['Engineering', 'Sales']
        for i in range(2):
            first, last = get_unique_name()
            vp = generate_employee(emp_counter, first, last, vp_titles[i], vp_depts[i], ceo, 2)
            vps.append(vp)
            emp_counter += 1
            self.stdout.write(self.style.SUCCESS(f'  Created: {vp.full_name} - {vp.position_title}'))
        
        # Level 3: Directors (5 employees)
        self.stdout.write('Creating Level 3: Directors...')
        directors = []
        director_depts = ['Engineering', 'Engineering', 'Sales', 'Marketing', 'Operations']
        for i in range(5):
            first, last = get_unique_name()
            # Assign to VPs: Engineering directors to VP Eng, Sales to VP Sales, others to CEO
            if director_depts[i] == 'Engineering':
                manager = vps[0]
            elif director_depts[i] == 'Sales':
                manager = vps[1]
            else:
                manager = ceo
            
            director = generate_employee(
                emp_counter, first, last, 
                f'Director of {director_depts[i]}', 
                director_depts[i], 
                manager, 3
            )
            directors.append(director)
            emp_counter += 1
            self.stdout.write(self.style.SUCCESS(f'  Created: {director.full_name} - {director.position_title}'))
        
        # Level 4: Managers (8 employees)
        self.stdout.write('Creating Level 4: Managers...')
        managers = []
        manager_depts = ['Engineering', 'Engineering', 'Sales', 'Sales', 'Marketing', 'Operations', 'Finance', 'HR']
        for i in range(8):
            first, last = get_unique_name()
            # Assign to appropriate director
            dept = manager_depts[i]
            director = next((d for d in directors if d.department_name == dept), directors[0])
            
            manager = generate_employee(
                emp_counter, first, last,
                f'{dept} Manager',
                dept,
                director, 4
            )
            managers.append(manager)
            emp_counter += 1
            self.stdout.write(self.style.SUCCESS(f'  Created: {manager.full_name} - {manager.position_title}'))
        
        # Level 5: Senior Staff (8 employees)
        self.stdout.write('Creating Level 5: Senior Staff...')
        senior_staff = []
        for i in range(8):
            first, last = get_unique_name()
            # Distribute across managers
            manager = managers[i % len(managers)]
            
            senior = generate_employee(
                emp_counter, first, last,
                f'Senior {manager.department_name} Specialist',
                manager.department_name,
                manager, 5
            )
            senior_staff.append(senior)
            emp_counter += 1
            if i < 3:  # Show first few
                self.stdout.write(self.style.SUCCESS(f'  Created: {senior.full_name} - {senior.position_title}'))
        
        self.stdout.write(f'  ... and {len(senior_staff) - 3} more senior staff')
        
        # Level 6: Full Staff (251 employees)
        self.stdout.write('Creating Level 6: Full Staff (251 employees)...')
        staff_count = 0
        all_supervisors = managers + senior_staff  # Can report to managers or senior staff
        
        for i in range(251):
            first, last = get_unique_name()
            # Distribute across managers and senior staff
            supervisor = all_supervisors[i % len(all_supervisors)]
            
            staff = generate_employee(
                emp_counter, first, last,
                f'{supervisor.department_name} Specialist',
                supervisor.department_name,
                supervisor, 6
            )
            emp_counter += 1
            staff_count += 1
            
            if staff_count % 50 == 0:
                self.stdout.write(f'  Created {staff_count} staff members...')
        
        self.stdout.write(self.style.SUCCESS(f'  Created all {staff_count} staff members'))
        
        # Summary
        total = EmployeeRecord.objects.count()
        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully created {total} employees:'))
        self.stdout.write(f'  Level 1 (CEO): {EmployeeRecord.objects.filter(hierarchy_level=0).count()}')
        self.stdout.write(f'  Level 2 (VPs): {EmployeeRecord.objects.filter(hierarchy_level=1).count()}')
        self.stdout.write(f'  Level 3 (Directors): {EmployeeRecord.objects.filter(hierarchy_level=2).count()}')
        self.stdout.write(f'  Level 4 (Managers): {EmployeeRecord.objects.filter(hierarchy_level=3).count()}')
        self.stdout.write(f'  Level 5 (Senior Staff): {EmployeeRecord.objects.filter(hierarchy_level=4).count()}')
        self.stdout.write(f'  Level 6 (Staff): {EmployeeRecord.objects.filter(hierarchy_level=5).count()}')
        self.stdout.write(self.style.SUCCESS('\n🎉 Organizational hierarchy created successfully!'))
