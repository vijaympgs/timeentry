"""
Contract Template Models for HRM
Following BBP 15.2 Contract Template specifications
Aligned with enterprise governance and Olivine UI canon
"""
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()

class ContractTemplate(models.Model):
    """
    Main contract template model for employment agreements
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='contracttemplate_company')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='contracttemplate_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='contracttemplate_updated_by')
    template_name = models.CharField(max_length=200)
    template_code = models.CharField(max_length=50)
    template_description = models.TextField(blank=True)
    contract_type = models.CharField(max_length=50, choices=[('permanent', 'Permanent Employment'), ('fixed_term', 'Fixed Term Contract'), ('probation', 'Probation Contract'), ('internship', 'Internship Agreement'), ('consultant', 'Consultant Agreement'), ('contractor', 'Independent Contractor'), ('temporary', 'Temporary Employment'), ('part_time', 'Part Time Agreement'), ('remote_work', 'Remote Work Agreement'), ('non_compete', 'Non-Compete Agreement'), ('nda', 'Non-Disclosure Agreement'), ('custom', 'Custom Template')])
    template_category = models.CharField(max_length=100, choices=[('employment', 'Employment'), ('consulting', 'Consulting'), ('freelance', 'Freelance'), ('internship', 'Internship'), ('volunteer', 'Volunteer'), ('apprenticeship', 'Apprenticeship'), ('commission_only', 'Commission Only'), ('custom', 'Custom')])
    template_content = models.TextField()
    template_variables = models.JSONField(default=dict, blank=True)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    version = models.CharField(max_length=20, default='1.0')
    legal_disclaimer = models.TextField(blank=True)
    compliance_notes = models.TextField(blank=True)
    required_signatures = models.JSONField(default=list, blank=True)
    legal_jurisdiction = models.CharField(max_length=200, blank=True)
    governing_law = models.CharField(max_length=200, blank=True)
    default_duration_months = models.IntegerField(null=True, blank=True)
    auto_renewal_enabled = models.BooleanField(default=False)
    renewal_notice_days = models.IntegerField(null=True, blank=True)
    termination_notice_days = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('draft', 'Draft'), ('active', 'Active'), ('inactive', 'Inactive'), ('archived', 'Archived'), ('deprecated', 'Deprecated')], default='draft')
    effective_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    usage_count = models.IntegerField(default=0)
    last_used_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_contract_templates'
        verbose_name = 'Contract Template'
        verbose_name_plural = 'Contract Templates'
        indexes = [models.Index(fields=['company', 'status'], name='idx_contract_template_status'), models.Index(fields=['company', 'contract_type'], name='idx_contract_template_type'), models.Index(fields=['company', 'template_category'], name='idx_contract_template_category')]
        constraints = [models.UniqueConstraint(fields=['company', 'template_code'], name='uk_contract_template_code')]
        ordering = ['template_name']

    def __str__(self):
        return f'{self.template_name} ({self.template_code})'

    def clean(self):
        """Validate contract template data"""
        if self.effective_date and self.expiry_date:
            if self.effective_date >= self.expiry_date:
                raise ValidationError('Expiry date must be after effective date')
        if self.version and (not self.version.replace('.', '').isdigit()):
            raise ValidationError('Version must be in format X.Y')
        if self.usage_count and self.usage_count < 0:
            raise ValidationError('Usage count cannot be negative')
        if self.default_duration_months and self.default_duration_months < 1:
            raise ValidationError('Default duration must be at least 1 month')
        if self.renewal_notice_days and self.renewal_notice_days < 1:
            raise ValidationError('Renewal notice days must be at least 1')
        if self.termination_notice_days and self.termination_notice_days < 1:
            raise ValidationError('Termination notice days must be at least 1')

class EmploymentContract(models.Model):
    """
    Individual employment contract records
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='employmentcontract_company')
    template = models.ForeignKey(ContractTemplate, on_delete=models.PROTECT, related_name='employmentcontract_template')
    employee = models.ForeignKey('hrm.Employee', on_delete=models.CASCADE, related_name='employmentcontract_employee')
    job_position = models.ForeignKey('hrm.Position', on_delete=models.CASCADE, related_name='employmentcontract_job_position')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='employmentcontract_created_by')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='employmentcontract_approved_by')
    contract_number = models.CharField(max_length=50)
    contract_title = models.CharField(max_length=200)
    contract_date = models.DateTimeField(auto_now_add=True)
    contract_status = models.CharField(max_length=20, choices=[('draft', 'Draft'), ('pending_approval', 'Pending Approval'), ('approved', 'Approved'), ('signed', 'Signed'), ('active', 'Active'), ('expired', 'Expired'), ('terminated', 'Terminated'), ('suspended', 'Suspended'), ('renewed', 'Renewed')], default='draft')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_fixed_term = models.BooleanField(default=False)
    contract_duration_months = models.IntegerField(null=True, blank=True)
    employment_type = models.CharField(max_length=50, choices=[('permanent', 'Permanent'), ('fixed_term', 'Fixed Term'), ('probation', 'Probation'), ('internship', 'Internship'), ('consultant', 'Consultant'), ('contractor', 'Independent Contractor'), ('temporary', 'Temporary'), ('part_time', 'Part Time')])
    work_schedule = models.CharField(max_length=50, choices=[('standard', 'Standard'), ('flexible', 'Flexible'), ('compressed', 'Compressed'), ('shift_based', 'Shift Based'), ('remote', 'Remote'), ('hybrid', 'Hybrid')])
    salary_amount = models.DecimalField(max_digits=12, decimal_places=2)
    salary_currency = models.CharField(max_length=10, default='USD')
    salary_frequency = models.CharField(max_length=20, choices=[('annual', 'Annual'), ('monthly', 'Monthly'), ('hourly', 'Hourly'), ('bi_weekly', 'Bi-Weekly'), ('semi_monthly', 'Semi-Monthly'), ('weekly', 'Weekly')])
    weekly_hours = models.DecimalField(max_digits=5, decimal_places=2, default=40.0)
    overtime_eligible = models.BooleanField(default=True)
    overtime_rate = models.DecimalField(max_digits=5, decimal_places=2, default=1.5)
    benefits_package = models.JSONField(default=dict, blank=True)
    allowances = models.JSONField(default=dict, blank=True)
    benefits_description = models.TextField(blank=True)
    annual_leave_days = models.IntegerField(default=20)
    sick_leave_days = models.IntegerField(default=10)
    personal_leave_days = models.IntegerField(default=5)
    maternity_leave_weeks = models.IntegerField(null=True, blank=True)
    paternity_leave_weeks = models.IntegerField(null=True, blank=True)
    reports_to_employee = models.ForeignKey('hrm.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='employmentcontract_reports_to_employee')
    department = models.ForeignKey('hrm.OrganizationalUnit', on_delete=models.SET_NULL, null=True, blank=True, related_name='employmentcontract_department')
    work_location = models.CharField(max_length=200, blank=True)
    probation_period_months = models.IntegerField(null=True, blank=True)
    notice_period_days = models.IntegerField(null=True, blank=True)
    confidentiality_required = models.BooleanField(default=True)
    non_compete_clause = models.BooleanField(default=False)
    non_solicitation_clause = models.BooleanField(default=False)
    auto_renewal_enabled = models.BooleanField(default=False)
    renewal_terms = models.JSONField(default=dict, blank=True)
    renewal_notice_days = models.IntegerField(null=True, blank=True)
    contract_content = models.TextField()
    special_terms = models.TextField(blank=True)
    amendments = models.JSONField(default=list, blank=True)
    employee_signature_date = models.DateTimeField(null=True, blank=True)
    company_signature_date = models.DateTimeField(null=True, blank=True)
    witness_signature_date = models.DateTimeField(null=True, blank=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    activation_date = models.DateTimeField(null=True, blank=True)
    termination_date = models.DateTimeField(null=True, blank=True)
    termination_reason = models.TextField(blank=True)
    renewal_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_employment_contracts'
        verbose_name = 'Employment Contract'
        verbose_name_plural = 'Employment Contracts'
        indexes = [models.Index(fields=['company', 'contract_status'], name='idx_contract_status'), models.Index(fields=['company', 'employee'], name='idx_contract_employee'), models.Index(fields=['company', 'job_position'], name='idx_contract_position'), models.Index(fields=['company', 'start_date'], name='idx_contract_start_date')]
        constraints = [models.UniqueConstraint(fields=['company', 'contract_number'], name='uk_contract_number')]
        ordering = ['-contract_date']

    def __str__(self):
        return f'Contract: {self.employee} - {self.job_position}'

    def clean(self):
        """Validate employment contract data"""
        if self.contract_date and self.contract_date > timezone.now():
            if not self.pk:
                raise ValidationError('Contract date cannot be in the future')
        if self.start_date and self.start_date < timezone.now().date():
            if not self.pk:
                raise ValidationError('Start date cannot be in the past for new contracts')
        if self.is_fixed_term and (not self.end_date):
            raise ValidationError('Fixed term contracts must have an end date')
        if self.end_date and self.start_date and (self.end_date <= self.start_date):
            raise ValidationError('End date must be after start date')
        if self.contract_duration_months and self.contract_duration_months < 1:
            raise ValidationError('Contract duration must be at least 1 month')
        if self.salary_amount and self.salary_amount < 0:
            raise ValidationError('Salary amount cannot be negative')
        if self.weekly_hours and (self.weekly_hours < 1 or self.weekly_hours > 80):
            raise ValidationError('Weekly hours must be between 1 and 80')
        if self.overtime_rate and self.overtime_rate < 1:
            raise ValidationError('Overtime rate must be at least 1.0')
        if self.annual_leave_days and self.annual_leave_days < 0:
            raise ValidationError('Annual leave days cannot be negative')
        if self.sick_leave_days and self.sick_leave_days < 0:
            raise ValidationError('Sick leave days cannot be negative')
        if self.personal_leave_days and self.personal_leave_days < 0:
            raise ValidationError('Personal leave days cannot be negative')
        if self.probation_period_months and self.probation_period_months < 0:
            raise ValidationError('Probation period cannot be negative')
        if self.notice_period_days and self.notice_period_days < 1:
            raise ValidationError('Notice period must be at least 1 day')
        if self.approval_date and self.contract_date and (self.approval_date < self.contract_date):
            raise ValidationError('Approval date cannot be before contract date')
        if self.activation_date and self.start_date and (self.activation_date < self.start_date):
            raise ValidationError('Activation date cannot be before start date')
        if self.termination_date and self.start_date and (self.termination_date < self.start_date):
            raise ValidationError('Termination date cannot be before start date')

class Employee(models.Model):
    """
    Employee information for contracts
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='employee_company')
    employee_number = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    class Meta:
        db_table = 'hr_employees'
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        constraints = [models.UniqueConstraint(fields=['company', 'employee_number'], name='uk_employee_number')]

class ContractPosition(models.Model):
    """
    Position information for contracts (avoiding conflict with main Position model)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='contractposition_company')
    title = models.CharField(max_length=200)
    position_code = models.CharField(max_length=50)
    job_grade = models.CharField(max_length=50)
    job_family = models.CharField(max_length=100)

    class Meta:
        db_table = 'hr_contract_positions'
        verbose_name = 'Contract Position'
        verbose_name_plural = 'Contract Positions'
        constraints = [models.UniqueConstraint(fields=['company', 'position_code'], name='uk_contract_position_code')]

class ContractOrganizationalUnit(models.Model):
    """
    Organizational unit information for contracts (avoiding conflict with main OrganizationalUnit model)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='contractorganizationalunit_company')
    unit_name = models.CharField(max_length=200)
    unit_code = models.CharField(max_length=50)
    unit_type = models.CharField(max_length=50)

    class Meta:
        db_table = 'hr_contract_org_units'
        verbose_name = 'Contract Organizational Unit'
        verbose_name_plural = 'Contract Organizational Units'
        constraints = [models.UniqueConstraint(fields=['company', 'unit_code'], name='uk_contract_org_unit_code')]