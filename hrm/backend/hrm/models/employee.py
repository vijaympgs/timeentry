"""
Employee aggregate root - Canonical HRM model
Following governance: One file = One aggregate root
"""
import uuid
from django.db import models
from django.contrib.auth.models import User
from ..tenancy import DEFAULT_COMPANY_CODE

class EmployeeRecord(models.Model):
    """
    Central model for managing comprehensive employee information
    Canonical Employee aggregate - all employee-related data centers here
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_code = models.CharField(max_length=10, db_index=True, default=DEFAULT_COMPANY_CODE)
    created_by_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='employeerecord_created_by_user')
    updated_by_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='employeerecord_updated_by_user')
    employee_number = models.CharField(max_length=50, unique=True)
    national_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    social_security_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    passport_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    preferred_name = models.CharField(max_length=100, null=True, blank=True)
    name_prefix = models.CharField(max_length=20, null=True, blank=True)
    name_suffix = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('NON_BINARY', 'Non-Binary'), ('PREFER_NOT_TO_SAY', 'Prefer not to say')])
    date_of_birth = models.DateField()
    marital_status = models.CharField(max_length=20, choices=[('SINGLE', 'Single'), ('MARRIED', 'Married'), ('DIVORCED', 'Divorced'), ('SEPARATED', 'Separated'), ('WIDOWED', 'Widowed'), ('DOMESTIC_PARTNERSHIP', 'Domestic Partnership')])
    work_email = models.EmailField(max_length=254)
    personal_email = models.EmailField(max_length=254, null=True, blank=True)
    work_phone = models.CharField(max_length=20, null=True, blank=True)
    mobile_phone = models.CharField(max_length=20, null=True, blank=True)
    home_phone = models.CharField(max_length=20, null=True, blank=True)
    hire_date = models.DateField()
    original_hire_date = models.DateField(null=True, blank=True)
    employment_status = models.CharField(max_length=20, choices=[('ACTIVE', 'Active'), ('ON_LEAVE', 'On Leave'), ('TERMINATED', 'Terminated'), ('RETIREMENT', 'Retirement'), ('CONTRACT_END', 'Contract End'), ('SUSPENDED', 'Suspended')])
    employment_type = models.CharField(max_length=50, choices=[('FULL_TIME', 'Full Time'), ('PART_TIME', 'Part Time'), ('CONTRACT', 'Contract'), ('INTERN', 'Intern'), ('TEMPORARY', 'Temporary'), ('SEASONAL', 'Seasonal'), ('CONSULTANT', 'Consultant'), ('FREELANCER', 'Freelancer')])
    position_title = models.CharField(max_length=200)
    department_name = models.CharField(max_length=100)
    job_category = models.CharField(max_length=100, null=True, blank=True)
    job_level = models.CharField(max_length=50, null=True, blank=True)
    job_family = models.CharField(max_length=100, null=True, blank=True)
    work_location_name = models.CharField(max_length=200, null=True, blank=True)
    remote_work_eligible = models.BooleanField(default=False)
    remote_work_percentage = models.IntegerField(default=0)
    manager_name = models.CharField(max_length=200, null=True, blank=True)
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='direct_reports')
    hierarchy_level = models.IntegerField(default=0, help_text="Organization hierarchy level (0=CEO, 1=Direct reports, etc.)")
    hr_business_partner_name = models.CharField(max_length=200, null=True, blank=True)
    salary_grade = models.CharField(max_length=50, null=True, blank=True)
    salary_step = models.CharField(max_length=50, null=True, blank=True)
    annual_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default='USD')
    pay_frequency = models.CharField(max_length=20, choices=[('HOURLY', 'Hourly'), ('WEEKLY', 'Weekly'), ('BI_WEEKLY', 'Bi-weekly'), ('SEMI_MONTHLY', 'Semi-monthly'), ('MONTHLY', 'Monthly'), ('ANNUAL', 'Annual')])
    benefits_eligibility_date = models.DateField(null=True, blank=True)
    benefits_package_name = models.CharField(max_length=100, null=True, blank=True)
    health_insurance_eligible = models.BooleanField(default=False)
    dental_insurance_eligible = models.BooleanField(default=False)
    vision_insurance_eligible = models.BooleanField(default=False)
    retirement_plan_eligible = models.BooleanField(default=False)
    life_insurance_eligible = models.BooleanField(default=False)
    primary_emergency_contact_name = models.CharField(max_length=200, null=True, blank=True)
    primary_emergency_contact_relationship = models.CharField(max_length=100, null=True, blank=True)
    primary_emergency_contact_phone = models.CharField(max_length=20, null=True, blank=True)
    secondary_emergency_contact_name = models.CharField(max_length=200, null=True, blank=True)
    secondary_emergency_contact_relationship = models.CharField(max_length=100, null=True, blank=True)
    secondary_emergency_contact_phone = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_confidential = models.BooleanField(default=False)
    is_key_employee = models.BooleanField(default=False)
    is_high_potential = models.BooleanField(default=False)
    termination_date = models.DateField(null=True, blank=True)
    termination_reason = models.CharField(max_length=200, null=True, blank=True)
    rehire_eligible = models.BooleanField(default=True)
    username = models.CharField(max_length=150, unique=True)
    role = models.CharField(max_length=50, default='Employee')
    @property
    def full_name(self):
        """Return the employee's full name."""
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def manager_name(self):
        """Return the manager's full name, or empty string if no manager."""
        return self.manager.full_name if self.manager else ''
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'employee_record'
        verbose_name = 'Employee Record'
        verbose_name_plural = 'Employee Records'
        indexes = [models.Index(fields=['company_code', 'employee_number'], name='idx_company_employee'), models.Index(fields=['company_code', 'is_active'], name='idx_employee_company_active'), models.Index(fields=['department_name', 'is_active'], name='idx_dept_active'), models.Index(fields=['position_title', 'is_active'], name='idx_position_active'), models.Index(fields=['hire_date'], name='idx_hire_date'), models.Index(fields=['last_name', 'first_name'], name='idx_name'), models.Index(fields=['work_email'], name='idx_work_email')]

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.employee_number})'

class EmployeeAddress(models.Model):
    """
    Supporting model for Employee aggregate
    Manages multiple addresses for employees - references Employee aggregate root
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_code = models.CharField(max_length=10, db_index=True, default=DEFAULT_COMPANY_CODE)
    employee = models.ForeignKey(EmployeeRecord, on_delete=models.CASCADE, related_name='employeeaddress_employee')
    address_type = models.CharField(max_length=50, choices=[('HOME', 'Home'), ('WORK', 'Work'), ('MAILING', 'Mailing'), ('TEMPORARY', 'Temporary')])
    address_line_1 = models.CharField(max_length=200)
    address_line_2 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'employee_address'
        verbose_name = 'Employee Address'
        verbose_name_plural = 'Employee Addresses'
        indexes = [models.Index(fields=['employee', 'address_type'], name='idx_employee_type'), models.Index(fields=['is_primary'], name='idx_primary')]

    def __str__(self):
        return f'{self.employee.first_name} {self.employee.last_name} - {self.address_type}'
