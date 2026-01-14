"""
Comprehensive test suite for Employee models
Following .hrm.cline/05_tasks_checklist.md Section 4: Testing & Quality Assurance
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from datetime import date, datetime
from decimal import Decimal
from hrm.models.employee import EmployeeRecord, EmployeeAddress
from .test_mixins import EmployeeTestDataMixin


class EmployeeRecordTestCase(TestCase):
    """Test EmployeeRecord model methods and validations"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.employee_data = {
            'employee_number': 'EMP001',
            'first_name': 'John',
            'last_name': 'Doe',
            'gender': 'MALE',
            'date_of_birth': date(1990, 1, 1),
            'work_email': 'john.doe@company.com',
            'hire_date': date(2020, 1, 1),
            'position_title': 'Software Engineer',
            'department_name': 'Engineering',
            'employment_status': 'ACTIVE',
            'employment_type': 'FULL_TIME',
            'annual_salary': Decimal('75000.00'),
            'username': 'johndoe'
        }
    
    def test_employee_creation(self):
        """Test employee record creation"""
        employee = EmployeeRecord.objects.create(created_by_user=self.user, **self.employee_data)
        
        self.assertEqual(employee.first_name, 'John')
        self.assertEqual(employee.last_name, 'Doe')
        self.assertEqual(employee.employee_number, 'EMP001')
        self.assertEqual(employee.gender, 'MALE')
        self.assertTrue(employee.is_active)
        self.assertIsNotNone(employee.created_at)
        self.assertIsNotNone(employee.updated_at)
    
    def test_employee_string_representation(self):
        """Test employee string representation"""
        employee = EmployeeRecord.objects.create(created_by_user=self.user, **self.employee_data)
        expected_str = "John Doe (EMP001)"
        self.assertEqual(str(employee), expected_str)
    
    def test_unique_employee_number(self):
        """Test employee number uniqueness constraint"""
        EmployeeRecord.objects.create(created_by_user=self.user, **self.employee_data)
        
        # Attempt to create another employee with same number
        with self.assertRaises(IntegrityError):
            EmployeeRecord.objects.create(
                created_by_user=self.user,
                employee_number='EMP001',
                first_name='Jane',
                last_name='Smith',
                gender='FEMALE',
                date_of_birth=date(1992, 5, 15),
                work_email='jane.smith@company.com',
                hire_date=date(2021, 6, 1),
                position_title='Designer',
                department_name='Design',
                employment_status='ACTIVE',
                employment_type='FULL_TIME',
                username='janesmith'
            )
    
    def test_unique_work_email(self):
        """Test work email uniqueness constraint"""
        EmployeeRecord.objects.create(created_by_user=self.user, **self.employee_data)
        
        # Attempt to create another employee with same work email
        with self.assertRaises(IntegrityError):
            EmployeeRecord.objects.create(
                created_by_user=self.user,
                employee_number='EMP002',
                first_name='Jane',
                last_name='Smith',
                gender='FEMALE',
                date_of_birth=date(1992, 5, 15),
                work_email='john.doe@company.com',  # Same email
                hire_date=date(2021, 6, 1),
                position_title='Designer',
                department_name='Design',
                employment_status='ACTIVE',
                employment_type='FULL_TIME',
                username='janesmith'
            )
    
    def test_unique_username(self):
        """Test username uniqueness constraint"""
        EmployeeRecord.objects.create(created_by_user=self.user, **self.employee_data)
        
        # Attempt to create another employee with same username
        with self.assertRaises(IntegrityError):
            EmployeeRecord.objects.create(
                created_by_user=self.user,
                employee_number='EMP002',
                first_name='Jane',
                last_name='Smith',
                gender='FEMALE',
                date_of_birth=date(1992, 5, 15),
                work_email='jane.smith@company.com',
                hire_date=date(2021, 6, 1),
                position_title='Designer',
                department_name='Design',
                employment_status='ACTIVE',
                employment_type='FULL_TIME',
                username='johndoe'  # Same username
            )
    
    def test_employment_status_choices(self):
        """Test valid employment status choices"""
        valid_statuses = ['ACTIVE', 'ON_LEAVE', 'TERMINATED', 'RETIREMENT', 'CONTRACT_END', 'SUSPENDED']
        
        for status in valid_statuses:
            employee = EmployeeRecord.objects.create(
                created_by_user=self.user,
                employee_number=f'EMP{status}',
                first_name='Test',
                last_name='User',
                gender='MALE',
                date_of_birth=date(1990, 1, 1),
                work_email=f'test{status}@company.com',
                hire_date=date(2020, 1, 1),
                position_title='Test Position',
                department_name='Test Department',
                employment_status=status,
                employment_type='FULL_TIME',
                username=f'test{status}'
            )
            self.assertEqual(employee.employment_status, status)
    
    def test_employment_type_choices(self):
        """Test valid employment type choices"""
        valid_types = ['FULL_TIME', 'PART_TIME', 'CONTRACT', 'INTERN', 'TEMPORARY', 'SEASONAL', 'CONSULTANT', 'FREELANCER']
        
        for emp_type in valid_types:
            employee = EmployeeRecord.objects.create(
                created_by_user=self.user,
                employee_number=f'EMP{emp_type}',
                first_name='Test',
                last_name='User',
                gender='MALE',
                date_of_birth=date(1990, 1, 1),
                work_email=f'test{emp_type}@company.com',
                hire_date=date(2020, 1, 1),
                position_title='Test Position',
                department_name='Test Department',
                employment_status='ACTIVE',
                employment_type=emp_type,
                username=f'test{emp_type}'
            )
            self.assertEqual(employee.employment_type, emp_type)
    
    def test_gender_choices(self):
        """Test valid gender choices"""
        valid_genders = ['MALE', 'FEMALE', 'NON_BINARY', 'PREFER_NOT_TO_SAY']
        
        for gender in valid_genders:
            employee = EmployeeRecord.objects.create(
                created_by_user=self.user,
                employee_number=f'EMP{gender}',
                first_name='Test',
                last_name='User',
                gender=gender,
                date_of_birth=date(1990, 1, 1),
                work_email=f'test{gender}@company.com',
                hire_date=date(2020, 1, 1),
                position_title='Test Position',
                department_name='Test Department',
                employment_status='ACTIVE',
                employment_type='FULL_TIME',
                username=f'test{gender}'
            )
            self.assertEqual(employee.gender, gender)
    
    def test_marital_status_choices(self):
        """Test valid marital status choices"""
        valid_statuses = ['SINGLE', 'MARRIED', 'DIVORCED', 'SEPARATED', 'WIDOWED', 'DOMESTIC_PARTNERSHIP']
        
        for status in valid_statuses:
            employee = EmployeeRecord.objects.create(
                created_by_user=self.user,
                employee_number=f'EMP{status}',
                first_name='Test',
                last_name='User',
                gender='MALE',
                date_of_birth=date(1990, 1, 1),
                marital_status=status,
                work_email=f'test{status}@company.com',
                hire_date=date(2020, 1, 1),
                position_title='Test Position',
                department_name='Test Department',
                employment_status='ACTIVE',
                employment_type='FULL_TIME',
                username=f'test{status}'
            )
            self.assertEqual(employee.marital_status, status)
    
    def test_pay_frequency_choices(self):
        """Test valid pay frequency choices"""
        valid_frequencies = ['HOURLY', 'WEEKLY', 'BI_WEEKLY', 'SEMI_MONTHLY', 'MONTHLY', 'ANNUAL']
        
        for frequency in valid_frequencies:
            employee = EmployeeRecord.objects.create(
                created_by_user=self.user,
                employee_number=f'EMP{frequency}',
                first_name='Test',
                last_name='User',
                gender='MALE',
                date_of_birth=date(1990, 1, 1),
                work_email=f'test{frequency}@company.com',
                hire_date=date(2020, 1, 1),
                position_title='Test Position',
                department_name='Test Department',
                employment_status='ACTIVE',
                employment_type='FULL_TIME',
                pay_frequency=frequency,
                username=f'test{frequency}'
            )
            self.assertEqual(employee.pay_frequency, frequency)
    
    def test_default_values(self):
        """Test default field values"""
        employee = EmployeeRecord.objects.create(
            created_by_user=self.user,
            employee_number='EMP003',
            first_name='Test',
            last_name='User',
            gender='MALE',
            date_of_birth=date(1990, 1, 1),
            work_email='test3@company.com',
            hire_date=date(2020, 1, 1),
            position_title='Test Position',
            department_name='Test Department',
            employment_status='ACTIVE',
            employment_type='FULL_TIME',
            username='testuser3'
        )
        
        self.assertTrue(employee.is_active)
        self.assertFalse(employee.is_confidential)
        self.assertFalse(employee.is_key_employee)
        self.assertFalse(employee.is_high_potential)
        self.assertTrue(employee.rehire_eligible)
        self.assertFalse(employee.remote_work_eligible)
        self.assertEqual(employee.remote_work_percentage, 0)
        self.assertEqual(employee.currency, 'USD')
        self.assertEqual(employee.role, 'Employee')
    
    def test_optional_fields_null(self):
        """Test that optional fields can be null"""
        employee = EmployeeRecord.objects.create(
            created_by_user=self.user,
            employee_number='EMP004',
            first_name='Test',
            last_name='User',
            gender='MALE',
            date_of_birth=date(1990, 1, 1),
            work_email='test4@company.com',
            hire_date=date(2020, 1, 1),
            position_title='Test Position',
            department_name='Test Department',
            employment_status='ACTIVE',
            employment_type='FULL_TIME',
            username='testuser4'
        )
        
        # These fields should be None/null
        self.assertIsNone(employee.middle_name)
        self.assertIsNone(employee.preferred_name)
        self.assertIsNone(employee.national_id)
        self.assertIsNone(employee.social_security_number)
        self.assertIsNone(employee.passport_number)
        self.assertIsNone(employee.annual_salary)
        self.assertIsNone(employee.hourly_rate)
        self.assertIsNone(employee.termination_date)
        self.assertIsNone(employee.termination_reason)
    
    def test_audit_fields_auto_population(self):
        """Test that audit fields are automatically populated"""
        before_creation = datetime.now()
        
        employee = EmployeeRecord.objects.create(
            created_by_user=self.user,
            **self.employee_data
        )
        
        after_creation = datetime.now()
        
        self.assertIsNotNone(employee.created_at)
        self.assertIsNotNone(employee.updated_at)
        self.assertGreaterEqual(employee.created_at, before_creation)
        self.assertLessEqual(employee.created_at, after_creation)
        self.assertGreaterEqual(employee.updated_at, before_creation)
        self.assertLessEqual(employee.updated_at, after_creation)
    
    def test_company_code_default(self):
        """Test that company_code gets default value"""
        employee = EmployeeRecord.objects.create(
            created_by_user=self.user,
            **self.employee_data
        )
        
        self.assertIsNotNone(employee.company_code)
        self.assertEqual(employee.company_code, 'DEFAULT')  # Based on DEFAULT_COMPANY_CODE


class EmployeeAddressTestCase(TestCase):
    """Test EmployeeAddress model methods and validations"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.employee = EmployeeRecord.objects.create(
            created_by_user=self.user,
            employee_number='EMP001',
            first_name='John',
            last_name='Doe',
            gender='MALE',
            date_of_birth=date(1990, 1, 1),
            work_email='john.doe@company.com',
            hire_date=date(2020, 1, 1),
            position_title='Software Engineer',
            department_name='Engineering',
            employment_status='ACTIVE',
            employment_type='FULL_TIME',
            username='johndoe'
        )
        
        self.address_data = {
            'employee': self.employee,
            'address_type': 'HOME',
            'address_line_1': '123 Main St',
            'city': 'Anytown',
            'state': 'CA',
            'postal_code': '12345',
            'country': 'USA'
        }
    
    def test_address_creation(self):
        """Test address creation"""
        address = EmployeeAddress.objects.create(**self.address_data)
        
        self.assertEqual(address.employee, self.employee)
        self.assertEqual(address.address_type, 'HOME')
        self.assertEqual(address.address_line_1, '123 Main St')
        self.assertEqual(address.city, 'Anytown')
        self.assertEqual(address.state, 'CA')
        self.assertEqual(address.postal_code, '12345')
        self.assertEqual(address.country, 'USA')
        self.assertTrue(address.is_active)
        self.assertFalse(address.is_primary)
        self.assertIsNotNone(address.created_at)
        self.assertIsNotNone(address.updated_at)
    
    def test_address_string_representation(self):
        """Test address string representation"""
        address = EmployeeAddress.objects.create(**self.address_data)
        expected_str = "John Doe - HOME"
        self.assertEqual(str(address), expected_str)
    
    def test_address_type_choices(self):
        """Test valid address type choices"""
        valid_types = ['HOME', 'WORK', 'MAILING', 'TEMPORARY']
        
        for addr_type in valid_types:
            address = EmployeeAddress.objects.create(
                employee=self.employee,
                address_type=addr_type,
                address_line_1=f'{addr_type} St',
                city='Test City',
                state='TS',
                postal_code='12345',
                country='USA'
            )
            self.assertEqual(address.address_type, addr_type)
    
    def test_primary_address_constraint(self):
        """Test that only one address can be primary per employee"""
        # Create first primary address
        EmployeeAddress.objects.create(
            employee=self.employee,
            address_type='HOME',
            address_line_1='123 Main St',
            city='Anytown',
            state='CA',
            postal_code='12345',
            country='USA',
            is_primary=True
        )
        
        # Attempt to create second primary address for same employee
        with self.assertRaises(IntegrityError):
            EmployeeAddress.objects.create(
                employee=self.employee,
                address_type='WORK',
                address_line_1='456 Work St',
                city='Worktown',
                state='NY',
                postal_code='67890',
                country='USA',
                is_primary=True
            )
    
    def test_multiple_addresses_per_employee(self):
        """Test that employee can have multiple addresses"""
        home_address = EmployeeAddress.objects.create(
            employee=self.employee,
            address_type='HOME',
            address_line_1='123 Main St',
            city='Anytown',
            state='CA',
            postal_code='12345',
            country='USA',
            is_primary=True
        )
        
        work_address = EmployeeAddress.objects.create(
            employee=self.employee,
            address_type='WORK',
            address_line_1='456 Work St',
            city='Worktown',
            state='NY',
            postal_code='67890',
            country='USA',
            is_primary=False
        )
        
        self.assertEqual(self.employee.addresses.count(), 2)
        self.assertTrue(home_address.is_primary)
        self.assertFalse(work_address.is_primary)
    
    def test_address_cascade_delete(self):
        """Test that addresses are deleted when employee is deleted"""
        address = EmployeeAddress.objects.create(**self.address_data)
        self.assertEqual(EmployeeAddress.objects.count(), 1)
        
        # Delete employee
        self.employee.delete()
        
        # Address should also be deleted
        self.assertEqual(EmployeeAddress.objects.count(), 0)
    
    def test_company_code_inheritance(self):
        """Test that address inherits company_code from employee"""
        address = EmployeeAddress.objects.create(**self.address_data)
        self.assertEqual(address.company_code, self.employee.company_code)
    
    def test_optional_address_fields(self):
        """Test that optional address fields can be null"""
        address = EmployeeAddress.objects.create(
            employee=self.employee,
            address_type='HOME',
            address_line_1='123 Main St',
            city='Anytown',
            state='CA',
            postal_code='12345',
            country='USA',
            address_line_2='Apt 4B'  # Optional field
        )
        
        self.assertEqual(address.address_line_2, 'Apt 4B')
        
        # Test with null optional field
        address2 = EmployeeAddress.objects.create(
            employee=self.employee,
            address_type='WORK',
            address_line_1='456 Work St',
            city='Worktown',
            state='NY',
            postal_code='67890',
            country='USA'
        )
        
        self.assertIsNone(address2.address_line_2)


class EmployeeModelIntegrationTestCase(TestCase):
    """Integration tests for Employee models"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_employee_with_multiple_addresses_workflow(self):
        """Test complete workflow of employee with multiple addresses"""
        # Create employee
        employee = EmployeeRecord.objects.create(
            created_by_user=self.user,
            employee_number='EMP001',
            first_name='John',
            last_name='Doe',
            gender='MALE',
            date_of_birth=date(1990, 1, 1),
            work_email='john.doe@company.com',
            hire_date=date(2020, 1, 1),
            position_title='Software Engineer',
            department_name='Engineering',
            employment_status='ACTIVE',
            employment_type='FULL_TIME',
            username='johndoe'
        )
        
        # Add home address (primary)
        home_address = EmployeeAddress.objects.create(
            employee=employee,
            address_type='HOME',
            address_line_1='123 Main St',
            city='Anytown',
            state='CA',
            postal_code='12345',
            country='USA',
            is_primary=True
        )
        
        # Add work address
        work_address = EmployeeAddress.objects.create(
            employee=employee,
            address_type='WORK',
            address_line_1='456 Work St',
            city='Worktown',
            state='NY',
            postal_code='67890',
            country='USA',
            is_primary=False
        )
        
        # Verify relationships
        self.assertEqual(employee.addresses.count(), 2)
        self.assertIn(home_address, employee.addresses.all())
        self.assertIn(work_address, employee.addresses.all())
        
        # Verify primary address
        primary_address = employee.addresses.get(is_primary=True)
        self.assertEqual(primary_address, home_address)
        
        # Test cascade delete
        employee.delete()
        self.assertEqual(EmployeeAddress.objects.count(), 0)
    
    def test_employee_termination_workflow(self):
        """Test employee termination workflow"""
        # Create active employee
        employee = EmployeeRecord.objects.create(
            created_by_user=self.user,
            employee_number='EMP002',
            first_name='Jane',
            last_name='Smith',
            gender='FEMALE',
            date_of_birth=date(1992, 5, 15),
            work_email='jane.smith@company.com',
            hire_date=date(2018, 3, 1),
            position_title='Manager',
            department_name='Sales',
            employment_status='ACTIVE',
            employment_type='FULL_TIME',
            username='janesmith'
        )
        
        # Verify initial state
        self.assertTrue(employee.is_active)
        self.assertIsNone(employee.termination_date)
        self.assertIsNone(employee.termination_reason)
        
        # Terminate employee
        termination_date = date(2023, 12, 31)
        termination_reason = 'Resignation'
        
        employee.employment_status = 'TERMINATED'
        employee.termination_date = termination_date
        employee.termination_reason = termination_reason
        employee.is_active = False
        employee.save()
        
        # Verify termination
        employee.refresh_from_db()
        self.assertEqual(employee.employment_status, 'TERMINATED')
        self.assertEqual(employee.termination_date, termination_date)
        self.assertEqual(employee.termination_reason, termination_reason)
        self.assertFalse(employee.is_active)
    
    def test_compensation_update_workflow(self):
        """Test compensation update workflow"""
        # Create employee with initial salary
        employee = EmployeeRecord.objects.create(
            created_by_user=self.user,
            employee_number='EMP003',
            first_name='Bob',
            last_name='Johnson',
            gender='MALE',
            date_of_birth=date(1985, 8, 15),
            work_email='bob.johnson@company.com',
            hire_date=date(2019, 6, 1),
            position_title='Developer',
            department_name='Engineering',
            employment_status='ACTIVE',
            employment_type='FULL_TIME',
            annual_salary=Decimal('65000.00'),
            username='bobjohnson'
        )
        
        # Verify initial compensation
        self.assertEqual(employee.annual_salary, Decimal('65000.00'))
        self.assertIsNone(employee.hourly_rate)
        
        # Update compensation (promotion)
        employee.annual_salary = Decimal('75000.00')
        employee.position_title = 'Senior Developer'
        employee.salary_grade = 'L3'
        employee.save()
        
        # Verify update
        employee.refresh_from_db()
        self.assertEqual(employee.annual_salary, Decimal('75000.00'))
        self.assertEqual(employee.position_title, 'Senior Developer')
        self.assertEqual(employee.salary_grade, 'L3')
    
    def test_remote_work_eligibility_workflow(self):
        """Test remote work eligibility workflow"""
        # Create employee
        employee = EmployeeRecord.objects.create(
            created_by_user=self.user,
            employee_number='EMP004',
            first_name='Alice',
            last_name='Wilson',
            gender='FEMALE',
            date_of_birth=date(1991, 3, 20),
            work_email='alice.wilson@company.com',
            hire_date=date(2021, 1, 1),
            position_title='Designer',
            department_name='Design',
            employment_status='ACTIVE',
            employment_type='FULL_TIME',
            username='alicewilson'
        )
        
        # Initially not remote work eligible
        self.assertFalse(employee.remote_work_eligible)
        self.assertEqual(employee.remote_work_percentage, 0)
        
        # Update to remote work eligible
        employee.remote_work_eligible = True
        employee.remote_work_percentage = 100
        employee.save()
        
        # Verify update
        employee.refresh_from_db()
        self.assertTrue(employee.remote_work_eligible)
        self.assertEqual(employee.remote_work_percentage, 100)
    
    def test_benefits_eligibility_workflow(self):
        """Test benefits eligibility workflow"""
        # Create employee
        employee = EmployeeRecord.objects.create(
            created_by_user=self.user,
            employee_number='EMP005',
            first_name='Charlie',
            last_name='Brown',
            gender='MALE',
            date_of_birth=date(1988, 11, 10),
            work_email='charlie.brown@company.com',
            hire_date=date(2022, 2, 1),
            position_title='Analyst',
            department_name='Finance',
            employment_status='ACTIVE',
            employment_type='FULL_TIME',
            username='charliebrown'
        )
        
        # Initially not benefits eligible
        self.assertFalse(employee.health_insurance_eligible)
        self.assertFalse(employee.dental_insurance_eligible)
        self.assertFalse(employee.vision_insurance_eligible)
        self.assertFalse(employee.retirement_plan_eligible)
        self.assertFalse(employee.life_insurance_eligible)
        
        # Update benefits eligibility after probation period
        benefits_date = date(2022, 8, 1)
        employee.benefits_eligibility_date = benefits_date
        employee.health_insurance_eligible = True
        employee.dental_insurance_eligible = True
        employee.vision_insurance_eligible = True
        employee.retirement_plan_eligible = True
        employee.life_insurance_eligible = True
        employee.benefits_package_name = 'Standard Package'
        employee.save()
        
        # Verify update
        employee.refresh_from_db()
        self.assertEqual(employee.benefits_eligibility_date, benefits_date)
        self.assertTrue(employee.health_insurance_eligible)
        self.assertTrue(employee.dental_insurance_eligible)
        self.assertTrue(employee.vision_insurance_eligible)
        self.assertTrue(employee.retirement_plan_eligible)
        self.assertTrue(employee.life_insurance_eligible)
        self.assertEqual(employee.benefits_package_name, 'Standard Package')
    
    def test_employee_search_functionality(self):
        """Test employee search and filtering functionality"""
        # Create multiple employees
        employees_data = [
            {
                'employee_number': 'EMP006',
                'first_name': 'David',
                'last_name': 'Miller',
                'gender': 'MALE',
                'date_of_birth': date(1987, 6, 25),
                'work_email': 'david.miller@company.com',
                'hire_date': date(2019, 9, 1),
                'position_title': 'Project Manager',
                'department_name': 'Project Management',
                'employment_status': 'ACTIVE',
                'employment_type': 'FULL_TIME',
                'username': 'davidmiller'
            },
            {
                'employee_number': 'EMP007',
                'first_name': 'Emma',
                'last_name': 'Davis',
                'gender': 'FEMALE',
                'date_of_birth': date(1993, 2, 14),
                'work_email': 'emma.davis@company.com',
                'hire_date': date(2020, 5, 15),
                'position_title': 'HR Specialist',
                'department_name': 'Human Resources',
                'employment_status': 'ACTIVE',
                'employment_type': 'FULL_TIME',
                'username': 'emmadavis'
            },
            {
                'employee_number': 'EMP008',
                'first_name': 'Frank',
                'last_name': 'Garcia',
                'gender': 'MALE',
                'date_of_birth': date(1989, 9, 30),
                'work_email': 'frank.garcia@company.com',
                'hire_date': date(2021, 11, 20),
                'position_title': 'Data Analyst',
                'department_name': 'Analytics',
                'employment_status': 'ON_LEAVE',
                'employment_type': 'FULL_TIME',
                'username': 'frankgarcia'
            }
        ]
        
        for emp_data in employees_data:
            EmployeeRecord.objects.create(created_by_user=self.user, **emp_data)
        
        # Test search by name
        search_results = EmployeeRecord.objects.filter(
            first_name__icontains='david'
        )
        self.assertEqual(search_results.count(), 1)
        self.assertEqual(search_results.first().last_name, 'Miller')
        
        # Test search by department
        dept_results = EmployeeRecord.objects.filter(
            department_name='Engineering'
        )
        self.assertEqual(dept_results.count(), 1)
        
        # Test filter by employment status
        active_employees = EmployeeRecord.objects.filter(
            employment_status='ACTIVE'
        )
        self.assertEqual(active_employees.count(), 2)
        
        # Test filter by employment type
        full_time_employees = EmployeeRecord.objects.filter(
            employment_type='FULL_TIME'
        )
        self.assertEqual(full_time_employees.count(), 3)
