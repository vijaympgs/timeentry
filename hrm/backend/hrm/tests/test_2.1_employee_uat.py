"""
User Acceptance Tests for Employee Records
Following .hrm.cline/05_tasks_checklist.md Section 4: Testing & Quality Assurance
"""

from django.test import TestCase, LiveServerTestCase
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import date, datetime
from decimal import Decimal
from hrm.models.employee import EmployeeRecord, EmployeeAddress
from .test_mixins import EmployeeTestDataMixin
import time


class EmployeeRecordsUATTestCase(LiveServerTestCase):
    """User Acceptance Tests for Employee Records"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test browser"""
        super().setUpClass()
        
        # Configure Chrome options for headless testing
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        
        try:
            cls.driver = webdriver.Chrome(options=chrome_options)
            cls.driver.implicitly_wait(10)
        except Exception:
            # Skip Selenium tests if Chrome driver not available
            cls.driver = None
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test browser"""
        if cls.driver:
            cls.driver.quit()
        super().tearDownClass()
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='uatuser',
            email='uat@example.com',
            password='uatpass123'
        )
        
        self.employee_data = {
            'employee_number': 'UAT001',
            'first_name': 'UAT',
            'last_name': 'Test',
            'gender': 'MALE',
            'date_of_birth': '1990-01-01',
            'work_email': 'uat.test@company.com',
            'hire_date': '2020-01-01',
            'position_title': 'UAT Specialist',
            'department_name': 'Quality Assurance',
            'employment_status': 'ACTIVE',
            'employment_type': 'FULL_TIME',
            'username': 'uattest'
        }
    
    def test_employee_creation_workflow(self):
        """Test complete employee creation workflow from user perspective"""
        if not self.driver:
            self.skipTest("Chrome driver not available")
        
        # Navigate to employee creation page
        self.driver.get(f'{self.live_server_url}/employees/create/')
        
        # Wait for page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'employee-form'))
        )
        
        # Fill in employee information
        self.driver.find_element(By.ID, 'id_employee_number').send_keys('UAT002')
        self.driver.find_element(By.ID, 'id_first_name').send_keys('Workflow')
        self.driver.find_element(By.ID, 'id_last_name').send_keys('Test')
        self.driver.find_element(By.ID, 'id_gender').send_keys('MALE')
        self.driver.find_element(By.ID, 'id_date_of_birth').send_keys('1992-05-15')
        self.driver.find_element(By.ID, 'id_work_email').send_keys('workflow.test@company.com')
        self.driver.find_element(By.ID, 'id_hire_date').send_keys('2021-06-01')
        self.driver.find_element(By.ID, 'id_position_title').send_keys('Workflow Specialist')
        self.driver.find_element(By.ID, 'id_department_name').send_keys('Testing')
        self.driver.find_element(By.ID, 'id_username').send_keys('workflowtest')
        
        # Submit form
        self.driver.find_element(By.ID, 'submit-btn').click()
        
        # Wait for success message
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'alert-success'))
        )
        
        # Verify employee was created
        success_message = self.driver.find_element(By.CLASS_NAME, 'alert-success').text
        self.assertIn('successfully created', success_message.lower())
        
        # Verify employee appears in list
        self.driver.get(f'{self.live_server_url}/employees/')
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'employee-table'))
        )
        
        # Search for created employee
        search_box = self.driver.find_element(By.ID, 'search-input')
        search_box.send_keys('Workflow')
        search_box.send_keys(Keys.RETURN)
        
        # Verify employee appears in results
        employee_rows = self.driver.find_elements(By.CLASS_NAME, 'employee-row')
        self.assertGreater(len(employee_rows), 0)
        
        # Verify employee data
        found_employee = False
        for row in employee_rows:
            if 'Workflow' in row.text and 'Test' in row.text:
                found_employee = True
                break
        
        self.assertTrue(found_employee, "Created employee not found in search results")
    
    def test_employee_edit_workflow(self):
        """Test employee editing workflow"""
        if not self.driver:
            self.skipTest("Chrome driver not available")
        
        # Create test employee
        employee = EmployeeRecord.objects.create(
            created_by_user=self.user,
            **self.employee_data
        )
        
        # Navigate to employee edit page
        self.driver.get(f'{self.live_server_url}/employees/{employee.id}/edit/')
        
        # Wait for page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'employee-form'))
        )
        
        # Verify existing data is loaded
        employee_number_field = self.driver.find_element(By.ID, 'id_employee_number')
        self.assertEqual(employee_number_field.get_attribute('value'), 'UAT001')
        
        first_name_field = self.driver.find_element(By.ID, 'id_first_name')
        self.assertEqual(first_name_field.get_attribute('value'), 'UAT')
        
        # Update employee information
        position_field = self.driver.find_element(By.ID, 'id_position_title')
        position_field.clear()
        position_field.send_keys('Senior UAT Specialist')
        
        salary_field = self.driver.find_element(By.ID, 'id_annual_salary')
        salary_field.send_keys('85000.00')
        
        # Submit form
        self.driver.find_element(By.ID, 'submit-btn').click()
        
        # Wait for success message
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'alert-success'))
        )
        
        # Verify update was successful
        success_message = self.driver.find_element(By.CLASS_NAME, 'alert-success').text
        self.assertIn('successfully updated', success_message.lower())
        
        # Verify updated data
        employee.refresh_from_db()
        self.assertEqual(employee.position_title, 'Senior UAT Specialist')
        self.assertEqual(str(employee.annual_salary), '85000.00')
    
    def test_employee_search_and_filter_workflow(self):
        """Test employee search and filtering functionality"""
        if not self.driver:
            self.skipTest("Chrome driver not available")
        
        # Create test employees
        employees_data = [
            {
                'employee_number': 'UAT003',
                'first_name': 'Search',
                'last_name': 'Test',
                'gender': 'MALE',
                'date_of_birth': '1990-01-01',
                'work_email': 'search.test@company.com',
                'hire_date': '2020-01-01',
                'position_title': 'Search Specialist',
                'department_name': 'Search',
                'employment_status': 'ACTIVE',
                'employment_type': 'FULL_TIME',
                'username': 'searchtest'
            },
            {
                'employee_number': 'UAT004',
                'first_name': 'Filter',
                'last_name': 'Test',
                'gender': 'FEMALE',
                'date_of_birth': '1992-01-01',
                'work_email': 'filter.test@company.com',
                'hire_date': '2021-01-01',
                'position_title': 'Filter Specialist',
                'department_name': 'Filter',
                'employment_status': 'ACTIVE',
                'employment_type': 'PART_TIME',
                'username': 'filtertest'
            },
            {
                'employee_number': 'UAT005',
                'first_name': 'Terminated',
                'last_name': 'Test',
                'gender': 'MALE',
                'date_of_birth': '1988-01-01',
                'work_email': 'terminated.test@company.com',
                'hire_date': '2019-01-01',
                'termination_date': '2023-12-31',
                'termination_reason': 'Resignation',
                'position_title': 'Former Employee',
                'department_name': 'Operations',
                'employment_status': 'TERMINATED',
                'employment_type': 'CONTRACT',
                'username': 'terminatedtest'
            }
        ]
        
        for emp_data in employees_data:
            EmployeeRecord.objects.create(
                created_by_user=self.user,
                **emp_data
            )
        
        # Navigate to employee list
        self.driver.get(f'{self.live_server_url}/employees/')
        
        # Wait for page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'employee-table'))
        )
        
        # Test search functionality
        search_box = self.driver.find_element(By.ID, 'search-input')
        search_box.send_keys('Search')
        search_box.send_keys(Keys.RETURN)
        
        # Wait for search results
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'employee-row'))
        )
        
        # Verify search results
        employee_rows = self.driver.find_elements(By.CLASS_NAME, 'employee-row')
        self.assertEqual(len(employee_rows), 1)
        self.assertIn('Search', employee_rows[0].text)
        
        # Clear search
        search_box = self.driver.find_element(By.ID, 'search-input')
        search_box.clear()
        search_box.send_keys(Keys.RETURN)
        
        # Test department filter
        department_filter = self.driver.find_element(By.ID, 'department-filter')
        department_filter.send_keys('Search')
        department_filter.send_keys(Keys.RETURN)
        
        # Wait for filter results
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'employee-row'))
        )
        
        # Verify filter results
        employee_rows = self.driver.find_elements(By.CLASS_NAME, 'employee-row')
        self.assertEqual(len(employee_rows), 1)
        
        # Test employment status filter
        status_filter = self.driver.find_element(By.ID, 'status-filter')
        status_filter.send_keys('TERMINATED')
        status_filter.send_keys(Keys.RETURN)
        
        # Wait for filter results
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'employee-row'))
        )
        
        # Verify filter results
        employee_rows = self.driver.find_elements(By.CLASS_NAME, 'employee-row')
        self.assertEqual(len(employee_rows), 1)
        self.assertIn('Terminated', employee_rows[0].text)
    
    def test_employee_address_management_workflow(self):
        """Test employee address management workflow"""
        if not self.driver:
            self.skipTest("Chrome driver not available")
        
        # Create test employee
        employee = EmployeeRecord.objects.create(
            created_by_user=self.user,
            **self.employee_data
        )
        
        # Navigate to employee detail page
        self.driver.get(f'{self.live_server_url}/employees/{employee.id}/')
        
        # Wait for page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'employee-detail'))
        )
        
        # Click on addresses tab
        addresses_tab = self.driver.find_element(By.ID, 'addresses-tab')
        addresses_tab.click()
        
        # Wait for addresses section to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'addresses-section'))
        )
        
        # Click add address button
        add_address_btn = self.driver.find_element(By.ID, 'add-address-btn')
        add_address_btn.click()
        
        # Wait for address form to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'address-form'))
        )
        
        # Fill in address information
        self.driver.find_element(By.ID, 'id_address_type').send_keys('HOME')
        self.driver.find_element(By.ID, 'id_address_line_1').send_keys('123 UAT Street')
        self.driver.find_element(By.ID, 'id_city').send_keys('Test City')
        self.driver.find_element(By.ID, 'id_state').send_keys('TS')
        self.driver.find_element(By.ID, 'id_postal_code').send_keys('12345')
        self.driver.find_element(By.ID, 'id_country').send_keys('USA')
        
        # Set as primary address
        primary_checkbox = self.driver.find_element(By.ID, 'id_is_primary')
        primary_checkbox.click()
        
        # Submit form
        self.driver.find_element(By.ID, 'submit-address-btn').click()
        
        # Wait for success message
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'alert-success'))
        )
        
        # Verify address was created
        success_message = self.driver.find_element(By.CLASS_NAME, 'alert-success').text
        self.assertIn('successfully created', success_message.lower())
        
        # Verify address appears in list
        addresses_list = self.driver.find_element(By.ID, 'addresses-list')
        self.assertIn('123 UAT Street', addresses_list.text)
        self.assertIn('Primary', addresses_list.text)
    
    def test_employee_validation_error_handling(self):
        """Test validation error handling from user perspective"""
        if not self.driver:
            self.skipTest("Chrome driver not available")
        
        # Navigate to employee creation page
        self.driver.get(f'{self.live_server_url}/employees/create/')
        
        # Wait for page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'employee-form'))
        )
        
        # Submit form without required fields
        self.driver.find_element(By.ID, 'submit-btn').click()
        
        # Wait for error messages
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'alert-danger'))
        )
        
        # Verify error messages are displayed
        error_alert = self.driver.find_element(By.CLASS_NAME, 'alert-danger')
        self.assertIn('required', error_alert.text.lower())
        
        # Verify field-level errors
        required_fields = ['employee_number', 'first_name', 'last_name', 'work_email']
        for field in required_fields:
            try:
                field_element = self.driver.find_element(By.ID, f'id_{field}')
                field_error = field_element.find_element(By.CLASS_NAME, 'field-error')
                self.assertTrue(field_error.is_displayed())
            except NoSuchElementException:
                self.fail(f"Expected error message for field: {field}")
    
    def test_employee_bulk_operations_workflow(self):
        """Test bulk employee operations workflow"""
        if not self.driver:
            self.skipTest("Chrome driver not available")
        
        # Create test employees
        for i in range(3):
            EmployeeRecord.objects.create(
                created_by_user=self.user,
                employee_number=f'UAT{i+6:03d}',
                first_name=f'Bulk{i}',
                last_name='Test',
                gender='MALE',
                date_of_birth=date(1990, 1, 1),
                work_email=f'bulk{i}@company.com',
                hire_date=date(2020, 1, 1),
                position_title=f'Bulk Position {i}',
                department_name='Bulk Department',
                employment_status='ACTIVE',
                employment_type='FULL_TIME',
                username=f'bulk{i}'
            )
        
        # Navigate to employee list
        self.driver.get(f'{self.live_server_url}/employees/')
        
        # Wait for page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'employee-table'))
        )
        
        # Select all employees
        select_all_checkbox = self.driver.find_element(By.ID, 'select-all-employees')
        select_all_checkbox.click()
        
        # Verify all checkboxes are selected
        employee_checkboxes = self.driver.find_elements(By.CLASS_NAME, 'employee-checkbox')
        for checkbox in employee_checkboxes:
            self.assertTrue(checkbox.is_selected())
        
        # Perform bulk update
        bulk_actions_dropdown = self.driver.find_element(By.ID, 'bulk-actions-dropdown')
        bulk_actions_dropdown.click()
        
        bulk_update_option = self.driver.find_element(By.ID, 'bulk-update-option')
        bulk_update_option.click()
        
        # Wait for bulk update modal
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'bulk-update-modal'))
        )
        
        # Select field to update
        field_to_update = self.driver.find_element(By.ID, 'field-to-update')
        field_to_update.send_keys('employment_status')
        
        # Select new value
        new_value = self.driver.find_element(By.ID, 'new-value')
        new_value.send_keys('ON_LEAVE')
        
        # Confirm bulk update
        confirm_btn = self.driver.find_element(By.ID, 'confirm-bulk-update')
        confirm_btn.click()
        
        # Wait for success message
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'alert-success'))
        )
        
        # Verify bulk update was successful
        success_message = self.driver.find_element(By.CLASS_NAME, 'alert-success').text
        self.assertIn('successfully updated', success_message.lower())
        
        # Verify employees were updated
        updated_employees = EmployeeRecord.objects.filter(employment_status='ON_LEAVE')
        self.assertEqual(updated_employees.count(), 3)
    
    def test_responsive_design_mobile_view(self):
        """Test responsive design on mobile view"""
        if not self.driver:
            self.skipTest("Chrome driver not available")
        
        # Set mobile viewport
        self.driver.set_window_size(375, 667)  # iPhone 6/7/8 size
        
        # Navigate to employee list
        self.driver.get(f'{self.live_server_url}/employees/')
        
        # Wait for page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'employee-table'))
        )
        
        # Verify mobile-specific elements
        try:
            mobile_menu = self.driver.find_element(By.CLASS_NAME, 'mobile-menu')
            self.assertTrue(mobile_menu.is_displayed())
        except NoSuchElementException:
            self.fail("Mobile menu not found")
        
        # Test mobile navigation
        mobile_menu.click()
        
        # Wait for mobile navigation to appear
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'mobile-nav'))
        )
        
        # Verify navigation items are visible
        nav_items = self.driver.find_elements(By.CLASS_NAME, 'nav-item')
        self.assertGreater(len(nav_items), 0)
        
        # Test mobile table view
        employee_cards = self.driver.find_elements(By.CLASS_NAME, 'employee-card')
        self.assertGreater(len(employee_cards), 0)
        
        # Verify card layout is mobile-friendly
        for card in employee_cards:
            self.assertTrue(card.is_displayed())
            # Check if card has mobile-specific styling
            card_classes = card.get_attribute('class')
            self.assertIn('mobile', card_classes.lower())
    
    def test_accessibility_compliance(self):
        """Test accessibility compliance"""
        if not self.driver:
            self.skipTest("Chrome driver not available")
        
        # Navigate to employee creation page
        self.driver.get(f'{self.live_server_url}/employees/create/')
        
        # Wait for page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'employee-form'))
        )
        
        # Test keyboard navigation
        form_fields = [
            'id_employee_number',
            'id_first_name',
            'id_last_name',
            'id_gender',
            'id_date_of_birth',
            'id_work_email'
        ]
        
        for field_id in form_fields:
            field = self.driver.find_element(By.ID, field_id)
            field.send_keys(Keys.TAB)  # Tab to next field
            
            # Verify focus moves to next field
            active_element = self.driver.switch_to.active_element
            self.assertTrue(active_element.is_displayed())
        
        # Test ARIA labels
        required_fields = ['employee_number', 'first_name', 'last_name', 'work_email']
        for field in required_fields:
            field_element = self.driver.find_element(By.ID, f'id_{field}')
            aria_required = field_element.get_attribute('aria-required')
            self.assertEqual(aria_required, 'true')
        
        # Test form labels
        for field in required_fields:
            try:
                label = self.driver.find_element(By.CSS_SELECTOR, f'label[for="id_{field}"]')
                self.assertTrue(label.is_displayed())
                self.assertNotEqual(label.text.strip(), '')
            except NoSuchElementException:
                self.fail(f"Label not found for field: {field}")
        
        # Test error announcements
        # Submit form without required fields to trigger errors
        self.driver.find_element(By.ID, 'submit-btn').click()
        
        # Wait for error messages
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'alert-danger'))
        )
        
        # Verify error messages are accessible
        error_alert = self.driver.find_element(By.CLASS_NAME, 'alert-danger')
        aria_live = error_alert.get_attribute('aria-live')
        self.assertEqual(aria_live, 'polite')
        
        # Test form validation messages
        for field in required_fields:
            try:
                field_element = self.driver.find_element(By.ID, f'id_{field}')
                aria_invalid = field_element.get_attribute('aria-invalid')
                self.assertEqual(aria_invalid, 'true')
                
                aria_describedby = field_element.get_attribute('aria-describedby')
                self.assertIsNotNone(aria_describedby)
                
                error_message = self.driver.find_element(By.ID, aria_describedby)
                self.assertTrue(error_message.is_displayed())
            except NoSuchElementException:
                self.fail(f"Accessibility error message not found for field: {field}")


class EmployeeRecordsPerformanceTestCase(TestCase):
    """Performance tests for Employee Records"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='perfuser',
            email='perf@example.com',
            password='perfpass123'
        )
        
        # Create test employees for performance testing
        self.employees = []
        for i in range(100):
            employee = EmployeeRecord.objects.create(
                created_by_user=self.user,
                employee_number=f'PERF{i:03d}',
                first_name=f'Perf{i}',
                last_name='Test',
                gender='MALE',
                date_of_birth=date(1990, 1, 1),
                work_email=f'perf{i}@company.com',
                hire_date=date(2020, 1, 1),
                position_title=f'Performance Test {i}',
                department_name='Performance Testing',
                employment_status='ACTIVE',
                employment_type='FULL_TIME',
                username=f'perf{i}'
            )
            self.employees.append(employee)
    
    def test_employee_list_performance(self):
        """Test employee list loading performance"""
        from django.test import Client
        import time
        
        client = Client()
        client.force_login(self.user)
        
        # Measure response time
        start_time = time.time()
        response = client.get('/api/employees/')
        end_time = time.time()
        
        response_time = end_time - start_time
        
        # Verify response is successful
        self.assertEqual(response.status_code, 200)
        
        # Verify performance meets requirements (should load in under 2 seconds)
        self.assertLess(response_time, 2.0, f"Employee list took {response_time:.2f} seconds to load")
        
        # Verify all employees are returned
        self.assertEqual(len(response.data), 100)
    
    def test_employee_search_performance(self):
        """Test employee search performance"""
        from django.test import Client
        import time
        
        client = Client()
        client.force_login(self.user)
        
        # Measure search response time
        start_time = time.time()
        response = client.get('/api/employees/?search=Perf50')
        end_time = time.time()
        
        response_time = end_time - start_time
        
        # Verify response is successful
        self.assertEqual(response.status_code, 200)
        
        # Verify performance meets requirements (should search in under 1 second)
        self.assertLess(response_time, 1.0, f"Employee search took {response_time:.2f} seconds")
        
        # Verify search results are correct
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['employee_number'], 'PERF050')
    
    def test_employee_filter_performance(self):
        """Test employee filter performance"""
        from django.test import Client
        import time
        
        client = Client()
        client.force_login(self.user)
        
        # Measure filter response time
        start_time = time.time()
        response = client.get('/api/employees/?department=Performance Testing')
        end_time = time.time()
        
        response_time = end_time - start_time
        
        # Verify response is successful
        self.assertEqual(response.status_code, 200)
        
        # Verify performance meets requirements (should filter in under 1 second)
        self.assertLess(response_time, 1.0, f"Employee filter took {response_time:.2f} seconds")
        
        # Verify filter results are correct
        self.assertEqual(len(response.data), 100)
    
    def test_employee_creation_performance(self):
        """Test employee creation performance"""
        from django.test import Client
        import time
        
        client = Client()
        client.force_login(self.user)
        
        employee_data = {
            'employee_number': 'PERF101',
            'first_name': 'Performance',
            'last_name': 'Test',
            'gender': 'MALE',
            'date_of_birth': '1990-01-01',
            'work_email': 'performance.test@company.com',
            'hire_date': '2020-01-01',
            'position_title': 'Performance Test',
            'department_name': 'Performance Testing',
            'employment_status': 'ACTIVE',
            'employment_type': 'FULL_TIME',
            'username': 'perftest'
        }
        
        # Measure creation response time
        start_time = time.time()
        response = client.post('/api/employees/', employee_data, content_type='application/json')
        end_time = time.time()
        
        response_time = end_time - start_time
        
        # Verify response is successful
        self.assertEqual(response.status_code, 201)
        
        # Verify performance meets requirements (should create in under 1 second)
        self.assertLess(response_time, 1.0, f"Employee creation took {response_time:.2f} seconds")
        
        # Verify employee was created
        self.assertEqual(EmployeeRecord.objects.count(), 101)
