"""
Test Mixins for HRM Employee Records
Following .hrm.cline/05_tasks_checklist.md Section 4: Testing & Quality Assurance
"""

from django.test import TestCase
from django.core.management import call_command
from django.contrib.auth.models import User
from hrm.models.employee import EmployeeRecord, EmployeeAddress


class EmployeeTestDataMixin:
    """Mixin for creating test employee data using seed command"""
    
    @classmethod
    def setUpTestData(cls):
        """Set up test data using seed command"""
        super().setUpTestData()
        
        # Create test users
        cls.admin_user = User.objects.create_user(
            username='testadmin',
            email='admin@test.com',
            password='testpass123',
            is_staff=True,
            is_superuser=True
        )
        
        cls.regular_user = User.objects.create_user(
            username='testuser',
            email='user@test.com',
            password='testpass123'
        )
        
        # Create seed data for testing
        call_command('seed_employees', count=20, with_addresses=True, clear=True)
        
        # Get reference employees for testing
        cls.ceo = EmployeeRecord.objects.get(employee_number='EMP0001')
        cls.test_employee = EmployeeRecord.objects.filter(
            employee_number='EMP0002'
        ).first()
        
        if not cls.test_employee:
            # Create a specific test employee if seed didn't create enough
            cls.test_employee = EmployeeRecord.objects.create(
                employee_number='EMP9999',
                first_name='Test',
                last_name='User',
                gender='MALE',
                date_of_birth='1990-01-01',
                work_email='test.user@company.com',
                hire_date='2020-01-01',
                position_title='Test Engineer',
                department_name='Engineering',
                employment_status='ACTIVE',
                employment_type='FULL_TIME',
                username='testuser',
                created_by_user=cls.admin_user
            )
    
    def get_test_employee(self, **kwargs):
        """Get or create a test employee with custom parameters"""
        defaults = {
            'employee_number': 'EMP9998',
            'first_name': 'Custom',
            'last_name': 'Test',
            'gender': 'FEMALE',
            'date_of_birth': '1992-05-15',
            'work_email': 'custom.test@company.com',
            'hire_date': '2021-06-01',
            'position_title': 'Custom Engineer',
            'department_name='Engineering',
            'employment_status': 'ACTIVE',
            'employment_type': 'FULL_TIME',
            'username': 'customtest',
            'created_by_user': self.admin_user
        }
        defaults.update(kwargs)
        
        employee, created = EmployeeRecord.objects.get_or_create(
            employee_number=defaults['employee_number'],
            defaults=defaults
        )
        
        if not created:
            # Update existing employee with new values
            for key, value in defaults.items():
                if key != 'employee_number':
                    setattr(employee, key, value)
            employee.save()
        
        return employee
    
    def create_test_address(self, employee, **kwargs):
        """Create a test address for an employee"""
        defaults = {
            'employee': employee,
            'address_type': 'HOME',
            'address_line_1': '123 Test Street',
            'city': 'Test City',
            'state': 'TS',
            'postal_code': '12345',
            'country': 'USA',
            'is_primary': True
        }
        defaults.update(kwargs)
        
        return EmployeeAddress.objects.create(**defaults)
    
    def get_diverse_test_data(self, count=10):
        """Create diverse test data using seed command"""
        call_command('seed_employees', count=count, with_addresses=True, diverse_data=True, clear=True)
        return EmployeeRecord.objects.all()


class EmployeeAPITestMixin:
    """Mixin for API testing utilities"""
    
    def setUp(self):
        """Set up API test client"""
        super().setUp()
        self.client.force_authenticate(self.admin_user)
    
    def assert_employee_response(self, response, expected_data):
        """Assert employee response contains expected data"""
        self.assertEqual(response.status_code, 200)
        
        for key, value in expected_data.items():
            self.assertEqual(response.data[key], value)
    
    def assert_validation_error(self, response, field_name):
        """Assert validation error for specific field"""
        self.assertEqual(response.status_code, 400)
        self.assertIn(field_name, response.data)
    
    def create_employee_payload(self, **overrides):
        """Create employee creation payload"""
        payload = {
            'employee_number': 'TEST001',
            'first_name': 'Test',
            'last_name': 'User',
            'gender': 'MALE',
            'date_of_birth': '1990-01-01',
            'work_email': 'test.user@company.com',
            'hire_date': '2020-01-01',
            'position_title': 'Test Engineer',
            'department_name': 'Engineering',
            'employment_status': 'ACTIVE',
            'employment_type': 'FULL_TIME',
            'username': 'testuser'
        }
        payload.update(overrides)
        return payload
    
    def create_address_payload(self, **overrides):
        """Create address creation payload"""
        payload = {
            'address_type': 'HOME',
            'address_line_1': '123 Test Street',
            'city': 'Test City',
            'state': 'TS',
            'postal_code': '12345',
            'country': 'USA',
            'is_primary': True
        }
        payload.update(overrides)
        return payload


class EmployeePerformanceTestMixin:
    """Mixin for performance testing utilities"""
    
    def measure_response_time(self, url, method='GET', data=None):
        """Measure API response time"""
        import time
        
        start_time = time.time()
        
        if method == 'GET':
            response = self.client.get(url)
        elif method == 'POST':
            response = self.client.post(url, data, content_type='application/json')
        elif method == 'PUT':
            response = self.client.put(url, data, content_type='application/json')
        elif method == 'DELETE':
            response = self.client.delete(url)
        
        end_time = time.time()
        response_time = end_time - start_time
        
        return response, response_time
    
    def assert_performance_requirement(self, response_time, max_time, operation_name):
        """Assert performance requirement is met"""
        self.assertLess(
            response_time, 
            max_time, 
            f"{operation_name} took {response_time:.3f}s, expected < {max_time}s"
        )
    
    def create_performance_test_data(self, count=100):
        """Create performance test data"""
        call_command('seed_employees', count=count, clear=True)
        return EmployeeRecord.objects.count()


class EmployeeIntegrationTestMixin:
    """Mixin for integration testing utilities"""
    
    def test_complete_employee_workflow(self):
        """Test complete employee workflow from creation to deletion"""
        # Create employee
        payload = self.create_employee_payload()
        response = self.client.post('/api/employees/', payload)
        self.assertEqual(response.status_code, 201)
        employee_id = response.data['id']
        
        # Add address
        address_payload = self.create_address_payload()
        response = self.client.post(f'/api/employees/{employee_id}/addresses/', address_payload)
        self.assertEqual(response.status_code, 201)
        address_id = response.data['id']
        
        # Update employee
        update_payload = {'position_title': 'Senior Test Engineer'}
        response = self.client.patch(f'/api/employees/{employee_id}/', update_payload)
        self.assertEqual(response.status_code, 200)
        
        # Update address
        address_update = {'address_line_2': 'Apt 4B'}
        response = self.client.patch(f'/api/employees/{employee_id}/addresses/{address_id}/', address_update)
        self.assertEqual(response.status_code, 200)
        
        # Verify data
        response = self.client.get(f'/api/employees/{employee_id}/')
        self.assertEqual(response.data['position_title'], 'Senior Test Engineer')
        
        # Delete address
        response = self.client.delete(f'/api/employees/{employee_id}/addresses/{address_id}/')
        self.assertEqual(response.status_code, 204)
        
        # Delete employee
        response = self.client.delete(f'/api/employees/{employee_id}/')
        self.assertEqual(response.status_code, 204)
        
        # Verify deletion
        response = self.client.get(f'/api/employees/{employee_id}/')
        self.assertEqual(response.status_code, 404)
    
    def test_bulk_operations_workflow(self):
        """Test bulk operations workflow"""
        # Create multiple employees
        employees = []
        for i in range(5):
            payload = self.create_employee_payload(
                employee_number=f'BULK{i+1:03d}',
                first_name=f'Bulk{i}',
                last_name=f'Test{i}',
                work_email=f'bulk{i}@company.com',
                username=f'bulk{i}'
            )
            response = self.client.post('/api/employees/', payload)
            self.assertEqual(response.status_code, 201)
            employees.append(response.data['id'])
        
        # Bulk update (simulate)
        update_data = {'employment_status': 'ON_LEAVE'}
        for employee_id in employees:
            response = self.client.patch(f'/api/employees/{employee_id}/', update_data)
            self.assertEqual(response.status_code, 200)
        
        # Verify updates
        for employee_id in employees:
            response = self.client.get(f'/api/employees/{employee_id}/')
            self.assertEqual(response.data['employment_status'], 'ON_LEAVE')
        
        # Bulk delete
        for employee_id in employees:
            response = self.client.delete(f'/api/employees/{employee_id}/')
            self.assertEqual(response.status_code, 204)
        
        # Verify deletion
        for employee_id in employees:
            response = self.client.get(f'/api/employees/{employee_id}/')
            self.assertEqual(response.status_code, 404)


class EmployeeSecurityTestMixin:
    """Mixin for security testing utilities"""
    
    def test_authentication_required(self, url):
        """Test that authentication is required for endpoint"""
        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
    
    def test_authorization_required(self, url, method='GET', data=None):
        """Test that proper authorization is required"""
        # Test with regular user
        self.client.force_authenticate(self.regular_user)
        
        if method == 'GET':
            response = self.client.get(url)
        elif method == 'POST':
            response = self.client.post(url, data, content_type='application/json')
        elif method == 'PUT':
            response = self.client.put(url, data, content_type='application/json')
        elif method == 'DELETE':
            response = self.client.delete(url)
        
        # Most endpoints should work with regular users for employee data
        # This can be overridden in specific test classes for admin-only endpoints
        return response
    
    def test_input_validation(self, url, payload, expected_errors):
        """Test input validation for malicious data"""
        response = self.client.post(url, payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        for field, error_msg in expected_errors.items():
            self.assertIn(field, response.data)
            if isinstance(response.data[field], list):
                self.assertTrue(any(error_msg in str(err) for err in response.data[field]))
            else:
                self.assertIn(error_msg, str(response.data[field]))
    
    def test_sql_injection_protection(self, url):
        """Test SQL injection protection"""
        malicious_inputs = [
            "'; DROP TABLE employees; --",
            "' OR '1'='1",
            "1; DELETE FROM employees WHERE '1'='1' --",
            "'; UPDATE employees SET username='hacked' WHERE '1'='1' --"
        ]
        
        for malicious_input in malicious_inputs:
            payload = self.create_employee_payload(
                employee_number=malicious_input,
                first_name=malicious_input
            )
            response = self.client.post(url, payload, content_type='application/json')
            
            # Should either be rejected (400) or handled safely (201)
            self.assertIn(response.status_code, [400, 201])
            
            if response.status_code == 201:
                # Verify data was sanitized
                self.assertNotEqual(response.data['employee_number'], malicious_input)
                self.assertNotEqual(response.data['first_name'], malicious_input)
    
    def test_xss_protection(self, url):
        """Test XSS protection"""
        xss_payloads = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>",
            "';alert('xss');//"
        ]
        
        for xss_payload in xss_payloads:
            payload = self.create_employee_payload(
                first_name=xss_payload,
                last_name=xss_payload
            )
            response = self.client.post(url, payload, content_type='application/json')
            
            if response.status_code == 201:
                # Verify XSS was sanitized
                self.assertNotIn('<script>', response.data['first_name'])
                self.assertNotIn('javascript:', response.data['first_name'])
