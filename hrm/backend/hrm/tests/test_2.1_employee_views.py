"""
View tests for Employee Records API endpoints
Following .hrm.cline/05_tasks_checklist.md Section 4: Testing & Quality Assurance
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date, datetime
from decimal import Decimal
from hrm.models.employee import EmployeeRecord, EmployeeAddress
from .test_mixins import EmployeeTestDataMixin, EmployeeAPITestMixin, EmployeePerformanceTestMixin, EmployeeSecurityTestMixin


class EmployeeRecordAPITestCase(APITestCase):
    """Test Employee Record API endpoints"""
    
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
            'date_of_birth': '1990-01-01',
            'work_email': 'john.doe@company.com',
            'hire_date': '2020-01-01',
            'position_title': 'Software Engineer',
            'department_name': 'Engineering',
            'employment_status': 'ACTIVE',
            'employment_type': 'FULL_TIME',
            'annual_salary': '75000.00',
            'username': 'johndoe'
        }
        
        self.employee = EmployeeRecord.objects.create(
            created_by_user=self.user,
            **self.employee_data
        )
    
    def test_get_employee_list(self):
        """Test GET /api/employees/ endpoint"""
        url = reverse('employee-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['employee_number'], 'EMP001')
    
    def test_get_employee_detail(self):
        """Test GET /api/employees/{id}/ endpoint"""
        url = reverse('employee-detail', kwargs={'pk': self.employee.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['employee_number'], 'EMP001')
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['last_name'], 'Doe')
    
    def test_create_employee(self):
        """Test POST /api/employees/ endpoint"""
        url = reverse('employee-list')
        new_employee_data = {
            'employee_number': 'EMP002',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'gender': 'FEMALE',
            'date_of_birth': '1992-05-15',
            'work_email': 'jane.smith@company.com',
            'hire_date': '2021-06-01',
            'position_title': 'Designer',
            'department_name': 'Design',
            'employment_status': 'ACTIVE',
            'employment_type': 'FULL_TIME',
            'username': 'janesmith'
        }
        
        response = self.client.post(url, new_employee_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EmployeeRecord.objects.count(), 2)
        self.assertEqual(response.data['employee_number'], 'EMP002')
        self.assertEqual(response.data['first_name'], 'Jane')
        self.assertEqual(response.data['last_name'], 'Smith')
    
    def test_update_employee(self):
        """Test PUT /api/employees/{id}/ endpoint"""
        url = reverse('employee-detail', kwargs={'pk': self.employee.id})
        updated_data = self.employee_data.copy()
        updated_data['position_title'] = 'Senior Software Engineer'
        updated_data['annual_salary'] = '85000.00'
        
        response = self.client.put(url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.position_title, 'Senior Software Engineer')
        self.assertEqual(str(self.employee.annual_salary), '85000.00')
    
    def test_delete_employee(self):
        """Test DELETE /api/employees/{id}/ endpoint"""
        url = reverse('employee-detail', kwargs={'pk': self.employee.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(EmployeeRecord.objects.count(), 0)
    
    def test_employee_validation_errors(self):
        """Test validation error handling"""
        url = reverse('employee-list')
        
        # Test missing required fields
        invalid_data = {
            'first_name': 'Test',
            # Missing required fields
        }
        
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_unique_constraint_validation(self):
        """Test unique constraint validation"""
        url = reverse('employee-list')
        
        # Duplicate employee number
        duplicate_data = self.employee_data.copy()
        
        response = self.client.post(url, duplicate_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('employee_number', response.data)
    
    def test_authentication_required(self):
        """Test that authentication is required"""
        url = reverse('employee-list')
        
        # Clear authentication
        self.client.force_authenticate(user=None)
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_permission_checks(self):
        """Test permission checks"""
        url = reverse('employee-detail', kwargs={'pk': self.employee.id})
        
        # Test with unauthenticated user
        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Test with authenticated user
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_pagination(self):
        """Test pagination functionality"""
        # Create multiple employees for pagination testing
        for i in range(10, 15):
            EmployeeRecord.objects.create(
                created_by_user=self.user,
                employee_number=f'EMP{i:03d}',
                first_name=f'Test{i}',
                last_name=f'User{i}',
                gender='MALE',
                date_of_birth=date(1990, 1, 1),
                work_email=f'test{i}@company.com',
                hire_date=date(2020, 1, 1),
                position_title='Test Position',
                department_name='Test Department',
                employment_status='ACTIVE',
                employment_type='FULL_TIME',
                username=f'test{i}'
            )
        
        url = reverse('employee-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 11)  # 1 original + 10 new
    
    def test_filtering_by_department(self):
        """Test filtering by department"""
        # Create employees in different departments
        EmployeeRecord.objects.create(
            created_by_user=self.user,
            employee_number='EMP009',
            first_name='Marketing',
            last_name='User',
            gender='FEMALE',
            date_of_birth=date(1991, 3, 15),
            work_email='marketing@company.com',
            hire_date=date(2021, 3, 1),
            position_title='Marketing Manager',
            department_name='Marketing',
            employment_status='ACTIVE',
            employment_type='FULL_TIME',
            username='marketinguser'
        )
        
        url = reverse('employee-list')
        response = self.client.get(url, {'department': 'Engineering'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['department_name'], 'Engineering')
    
    def test_filtering_by_status(self):
        """Test filtering by employment status"""
        # Create terminated employee
        EmployeeRecord.objects.create(
            created_by_user=self.user,
            employee_number='EMP010',
            first_name='Terminated',
            last_name='User',
            gender='MALE',
            date_of_birth=date(1985, 5, 20),
            work_email='terminated@company.com',
            hire_date=date(2018, 1, 1),
            termination_date=date(2023, 12, 31),
            termination_reason='Resignation',
            position_title='Former Employee',
            department_name='Operations',
            employment_status='TERMINATED',
            employment_type='FULL_TIME',
            username='terminateduser'
        )
        
        url = reverse('employee-list')
        response = self.client.get(url, {'employment_status': 'ACTIVE'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['employment_status'], 'ACTIVE')
    
    def test_search_functionality(self):
        """Test search functionality"""
        url = reverse('employee-list')
        response = self.client.get(url, {'search': 'John'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn('John', response.data[0]['first_name'])
    
    def test_date_range_filtering(self):
        """Test date range filtering"""
        url = reverse('employee-list')
        
        # Test hire date range
        start_date = '2020-01-01'
        end_date = '2020-12-31'
        response = self.client.get(url, {
            'hire_date_after': start_date,
            'hire_date_before': end_date
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
        # Verify date filtering works
        for employee in response.data:
            hire_date = datetime.strptime(employee['hire_date'], '%Y-%m-%d').date()
            self.assertGreaterEqual(hire_date, date(2020, 1, 1))
            self.assertLessEqual(hire_date, date(2020, 12, 31))


class EmployeeAddressAPITestCase(APITestCase):
    """Test Employee Address API endpoints"""
    
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
            date_of_birth='1990-01-01',
            work_email='john.doe@company.com',
            hire_date='2020-01-01',
            position_title='Software Engineer',
            department_name='Engineering',
            employment_status='ACTIVE',
            employment_type='FULL_TIME',
            username='johndoe'
        )
        
        self.address_data = {
            'employee': self.employee.id,
            'address_type': 'HOME',
            'address_line_1': '123 Main St',
            'city': 'Anytown',
            'state': 'CA',
            'postal_code': '12345',
            'country': 'USA',
            'is_primary': True
        }
        
        self.address = EmployeeAddress.objects.create(**self.address_data)
    
    def test_get_employee_addresses(self):
        """Test GET /api/employees/{id}/addresses/ endpoint"""
        url = reverse('employee-address-list', kwargs={'employee_id': self.employee.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['address_type'], 'HOME')
    
    def test_create_employee_address(self):
        """Test POST /api/employees/{id}/addresses/ endpoint"""
        url = reverse('employee-address-list', kwargs={'employee_id': self.employee.id})
        new_address_data = {
            'address_type': 'WORK',
            'address_line_1': '456 Work St',
            'city': 'Worktown',
            'state': 'NY',
            'postal_code': '67890',
            'country': 'USA',
            'is_primary': False
        }
        
        response = self.client.post(url, new_address_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.employee.addresses.count(), 2)
        self.assertEqual(response.data['address_type'], 'WORK')
    
    def test_update_employee_address(self):
        """Test PUT /api/employees/{id}/addresses/{id}/ endpoint"""
        url = reverse('employee-address-detail', kwargs={
            'employee_id': self.employee.id,
            'pk': self.address.id
        })
        
        updated_data = self.address_data.copy()
        updated_data['address_line_2'] = 'Apt 4B'
        
        response = self.client.put(url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.address.refresh_from_db()
        self.assertEqual(self.address.address_line_2, 'Apt 4B')
    
    def test_delete_employee_address(self):
        """Test DELETE /api/employees/{id}/addresses/{id}/ endpoint"""
        url = reverse('employee-address-detail', kwargs={
            'employee_id': self.employee.id,
            'pk': self.address.id
        })
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.employee.addresses.count(), 0)
    
    def test_primary_address_constraint(self):
        """Test that only one address can be primary per employee"""
        url = reverse('employee-address-list', kwargs={'employee_id': self.employee.id})
        
        # Attempt to create second primary address
        second_primary_data = {
            'employee': self.employee.id,
            'address_type': 'WORK',
            'address_line_1': '789 Work St',
            'city': 'Worktown',
            'state': 'NY',
            'postal_code': '67890',
            'country': 'USA',
            'is_primary': True
        }
        
        response = self.client.post(url, second_primary_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('is_primary', response.data)
    
    def test_address_validation_errors(self):
        """Test address validation errors"""
        url = reverse('employee-address-list', kwargs={'employee_id': self.employee.id})
        
        # Test missing required fields
        invalid_data = {
            'address_type': 'HOME',
            # Missing required fields
        }
        
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_address_type_choices(self):
        """Test valid address type choices"""
        url = reverse('employee-address-list', kwargs={'employee_id': self.employee.id})
        
        valid_types = ['HOME', 'WORK', 'MAILING', 'TEMPORARY']
        
        for addr_type in valid_types:
            address_data = {
                'employee': self.employee.id,
                'address_type': addr_type,
                'address_line_1': f'{addr_type} St',
                'city': 'Test City',
                'state': 'TS',
                'postal_code': '12345',
                'country': 'USA'
            }
            
            response = self.client.post(url, address_data, format='json')
            
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data['address_type'], addr_type)
    
    def test_cascade_delete_protection(self):
        """Test that addresses are deleted when employee is deleted"""
        # Delete employee
        employee_url = reverse('employee-detail', kwargs={'pk': self.employee.id})
        self.client.delete(employee_url)
        
        # Verify addresses are also deleted
        address_url = reverse('employee-address-list', kwargs={'employee_id': self.employee.id})
        response = self.client.get(address_url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class EmployeeWorkflowIntegrationTestCase(APITestCase):
    """Integration tests for complete employee workflows"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_complete_employee_lifecycle(self):
        """Test complete employee lifecycle from creation to termination"""
        # Create employee
        employee_data = {
            'employee_number': 'EMP011',
            'first_name': 'Lifecycle',
            'last_name': 'Test',
            'gender': 'MALE',
            'date_of_birth': '1990-01-01',
            'work_email': 'lifecycle@test.com',
            'hire_date': '2020-01-01',
            'position_title': 'Test Position',
            'department_name': 'Test Department',
            'employment_status': 'ACTIVE',
            'employment_type': 'FULL_TIME',
            'username': 'lifecycle'
        }
        
        create_url = reverse('employee-list')
        create_response = self.client.post(create_url, employee_data, format='json')
        
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        employee_id = create_response.data['id']
        
        # Add address
        address_data = {
            'employee': employee_id,
            'address_type': 'HOME',
            'address_line_1': '123 Lifecycle St',
            'city': 'Test City',
            'state': 'TS',
            'postal_code': '12345',
            'country': 'USA',
            'is_primary': True
        }
        
        address_url = reverse('employee-address-list', kwargs={'employee_id': employee_id})
        address_response = self.client.post(address_url, address_data, format='json')
        
        self.assertEqual(address_response.status_code, status.HTTP_201_CREATED)
        
        # Update employee (promotion)
        update_url = reverse('employee-detail', kwargs={'pk': employee_id})
        update_data = employee_data.copy()
        update_data['position_title'] = 'Senior Test Position'
        update_data['annual_salary'] = '85000.00'
        
        update_response = self.client.put(update_url, update_data, format='json')
        
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        
        # Terminate employee
        termination_url = reverse('employee-detail', kwargs={'pk': employee_id})
        termination_data = {
            'employment_status': 'TERMINATED',
            'termination_date': '2023-12-31',
            'termination_reason': 'End of contract',
            'is_active': False
        }
        
        termination_response = self.client.patch(termination_url, termination_data, format='json')
        
        self.assertEqual(termination_response.status_code, status.HTTP_200_OK)
        
        # Verify final state
        employee_url = reverse('employee-detail', kwargs={'pk': employee_id})
        final_response = self.client.get(employee_url)
        
        self.assertEqual(final_response.status_code, status.HTTP_200_OK)
        self.assertEqual(final_response.data['employment_status'], 'TERMINATED')
        self.assertFalse(final_response.data['is_active')
    
    def test_bulk_employee_operations(self):
        """Test bulk employee operations"""
        # Create multiple employees
        employees_data = []
        for i in range(5):
            employees_data.append({
                'employee_number': f'EMP{i+12:03d}',
                'first_name': f'Bulk{i}',
                'last_name=f'Employee{i}',
                'gender': 'MALE',
                'date_of_birth': f'199{i}-01-01',
                'work_email': f'bulk{i}@company.com',
                'hire_date': f'202{i}-01-01',
                'position_title': f'Bulk Position {i}',
                'department_name': 'Bulk Department',
                'employment_status': 'ACTIVE',
                'employment_type': 'FULL_TIME',
                'username': f'bulk{i}'
            })
        
        create_url = reverse('employee-list')
        create_responses = []
        
        for emp_data in employees_data:
            response = self.client.post(create_url, emp_data, format='json')
            create_responses.append(response)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertEqual(EmployeeRecord.objects.count(), 6)  # 1 original + 5 bulk
        
        # Test bulk update
        update_url = reverse('employee-list')
        bulk_update_data = {
            'employment_status': 'ON_LEAVE',
            'is_active': False
        }
        
        bulk_response = self.client.patch(update_url, bulk_update_data, format='json')
        
        self.assertEqual(bulk_response.status_code, status.HTTP_200_OK)
        
        # Verify updates
        updated_employees = EmployeeRecord.objects.filter(employment_status='ON_LEAVE')
        self.assertEqual(updated_employees.count(), 5)
    
    def test_employee_search_and_filter_integration(self):
        """Test search and filtering integration"""
        # Create diverse employee dataset
        employees_data = [
            {
                'employee_number': 'EMP013',
                'first_name': 'Search',
                'last_name': 'Test',
                'gender': 'MALE',
                'date_of_birth': '1990-01-01',
                'work_email': 'search@test.com',
                'hire_date': '2020-01-01',
                'position_title': 'Search Specialist',
                'department_name': 'Search',
                'employment_status': 'ACTIVE',
                'employment_type': 'FULL_TIME',
                'username': 'searchuser'
            },
            {
                'employee_number': 'EMP014',
                'first_name': 'Filter',
                'last_name': 'Test',
                'gender': 'FEMALE',
                'date_of_birth': '1992-01-01',
                'work_email': 'filter@test.com',
                'hire_date': '2021-01-01',
                'position_title': 'Filter Specialist',
                'department_name': 'Filter',
                'employment_status': 'ACTIVE',
                'employment_type': 'PART_TIME',
                'username': 'filteruser'
            },
            {
                'employee_number': 'EMP015',
                'first_name': 'Integration',
                'last_name': 'Test',
                'gender': 'MALE',
                'date_of_birth': '1988-01-01',
                'work_email': 'integration@test.com',
                'hire_date': '2019-01-01',
                'position_title': 'Integration Specialist',
                'department_name': 'Integration',
                'employment_status': 'TERMINATED',
                'employment_type': 'CONTRACT',
                'username': 'integrationuser'
            }
        ]
        
        for emp_data in employees_data:
            EmployeeRecord.objects.create(
                created_by_user=self.user,
                **emp_data
            )
        
        # Test search functionality
        search_url = reverse('employee-list')
        search_response = self.client.get(search_url, {'search': 'Search'})
        
        self.assertEqual(search_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(search_response.data), 1)
        
        # Test filtering by employment type
        part_time_url = reverse('employee-list')
        part_time_response = self.client.get(part_time_url, {'employment_type': 'PART_TIME'})
        
        self.assertEqual(part_time_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(part_time_response.data), 1)
        
        # Test filtering by status
        terminated_url = reverse('employee-list')
        terminated_response = self.client.get(terminated_url, {'employment_status': 'TERMINATED'})
        
        self.assertEqual(terminated_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(terminated_response.data), 1)
        
        # Test combined filters
        combined_url = reverse('employee-list')
        combined_response = self.client.get(combined_url, {
            'search': 'Integration',
            'employment_status': 'TERMINATED'
        })
        
        self.assertEqual(combined_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(combined_response.data), 1)
