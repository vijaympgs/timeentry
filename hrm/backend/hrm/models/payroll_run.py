"""
Payroll Run Models for HRM
Following BBP 04.3 Payroll Run specifications
Aligned with enterprise governance and Olivine UI canon
"""
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()

class PayrollRun(models.Model):
    """
    Main payroll run model for payroll processing
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='payrollrun_company')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='payrollrun_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='payrollrun_updated_by')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='payrollrun_approved_by')
    run_number = models.CharField(max_length=50)
    run_type = models.CharField(max_length=20, choices=[('regular', 'Regular Payroll'), ('off_cycle', 'Off-Cycle Payroll'), ('bonus', 'Bonus Run'), ('termination', 'Termination Payroll'), ('adjustment', 'Adjustment Payroll'), ('year_end', 'Year-End Payroll')], default='regular')
    pay_period_start = models.DateField()
    pay_period_end = models.DateField()
    pay_date = models.DateField()
    pay_frequency = models.CharField(max_length=20, choices=[('weekly', 'Weekly'), ('bi_weekly', 'Bi-Weekly'), ('semi_monthly', 'Semi-Monthly'), ('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('annual', 'Annual')])
    status = models.CharField(max_length=20, choices=[('draft', 'Draft'), ('calculating', 'Calculating'), ('calculated', 'Calculated'), ('validating', 'Validating'), ('validated', 'Validated'), ('pending_approval', 'Pending Approval'), ('approved', 'Approved'), ('processing', 'Processing'), ('processed', 'Processed'), ('paid', 'Paid'), ('cancelled', 'Cancelled'), ('error', 'Error')], default='draft')
    total_employees = models.IntegerField(default=0)
    total_gross_pay = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_net_pay = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_taxes = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_deductions = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_employer_taxes = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    calculation_start_time = models.DateTimeField(null=True, blank=True)
    calculation_end_time = models.DateTimeField(null=True, blank=True)
    processing_duration = models.DurationField(null=True, blank=True)
    approval_required = models.BooleanField(default=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    approved_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    disbursement_method = models.CharField(max_length=20, choices=[('direct_deposit', 'Direct Deposit'), ('check', 'Check'), ('cash', 'Cash'), ('mixed', 'Mixed')], default='direct_deposit')
    disbursement_date = models.DateField(null=True, blank=True)
    bank_batch_id = models.CharField(max_length=100, blank=True)
    include_terminated = models.BooleanField(default=False)
    include_contractors = models.BooleanField(default=False)
    calculate_overtime = models.BooleanField(default=True)
    calculate_bonuses = models.BooleanField(default=True)
    run_notes = models.TextField(blank=True)
    error_messages = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_payroll_runs'
        verbose_name = 'Payroll Run'
        verbose_name_plural = 'Payroll Runs'
        indexes = [models.Index(fields=['company', 'status'], name='idx_payroll_status'), models.Index(fields=['company', 'pay_period_start'], name='idx_payroll_period'), models.Index(fields=['company', 'pay_date'], name='idx_payroll_date')]
        constraints = [models.UniqueConstraint(fields=['company', 'run_number'], name='uk_payroll_run_number')]
        ordering = ['-pay_date']

    def __str__(self):
        return f'Payroll Run {self.run_number} - {self.pay_date}'

    def clean(self):
        """Validate payroll run data"""
        if self.pay_period_start and self.pay_period_end:
            if self.pay_period_start >= self.pay_period_end:
                raise ValidationError('Pay period start must be before end date')
        if self.pay_date and self.pay_period_end and (self.pay_date <= self.pay_period_end):
            raise ValidationError('Pay date must be after pay period end')
        financial_fields = ['total_gross_pay', 'total_net_pay', 'total_taxes', 'total_deductions', 'total_employer_taxes']
        for field in financial_fields:
            value = getattr(self, field)
            if value is not None and value < 0:
                raise ValidationError(f"{field.replace('_', ' ').title()} cannot be negative")
        if self.total_employees and self.total_employees < 0:
            raise ValidationError('Total employees cannot be negative')
        if self.approved_amount and self.approved_amount < 0:
            raise ValidationError('Approved amount cannot be negative')

class PayrollCalculation(models.Model):
    """
    Individual employee payroll calculation details
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='payrollcalculation_company')
    payroll_run = models.ForeignKey(PayrollRun, on_delete=models.CASCADE, related_name='payrollcalculation_payroll_run')
    employee = models.ForeignKey('hrm.Employee', on_delete=models.CASCADE, related_name='payrollcalculation_employee')
    employee_number = models.CharField(max_length=50)
    employee_name = models.CharField(max_length=200)
    department = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    base_salary = models.DecimalField(max_digits=12, decimal_places=2)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    regular_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    overtime_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    double_time_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    holiday_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    vacation_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    sick_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    regular_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    overtime_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    holiday_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bonus_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    commission_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    gross_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    federal_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    state_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    local_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    social_security_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    medicare_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other_taxes = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_taxes = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    health_insurance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    dental_insurance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vision_insurance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    retirement_401k = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    retirement_403b = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fsa_medical = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fsa_dependent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    hsa = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other_pretax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_pretax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    garnishment = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    child_support = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_levy = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    loan_repayment = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    union_dues = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other_posttax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_posttax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    employer_health = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    employer_retirement = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    employer_futa = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    employer_suta = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    employer_other = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_employer_contributions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ytd_gross_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ytd_net_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ytd_taxes = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ytd_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    calculation_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('calculated', 'Calculated'), ('error', 'Error'), ('adjusted', 'Adjusted')], default='pending')
    payment_method = models.CharField(max_length=20, choices=[('direct_deposit', 'Direct Deposit'), ('check', 'Check'), ('cash', 'Cash')])
    bank_account_type = models.CharField(max_length=20, choices=[('checking', 'Checking'), ('savings', 'Savings')], blank=True)
    bank_routing_number = models.CharField(max_length=20, blank=True)
    bank_account_number = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_payroll_calculations'
        verbose_name = 'Payroll Calculation'
        verbose_name_plural = 'Payroll Calculations'
        indexes = [models.Index(fields=['company', 'payroll_run'], name='idx_calculation_run'), models.Index(fields=['company', 'employee'], name='idx_calculation_employee'), models.Index(fields=['company', 'calculation_status'], name='idx_calculation_status')]
        ordering = ['employee_name']

    def __str__(self):
        return f'Payroll Calculation - {self.employee_name}'

    def clean(self):
        """Validate payroll calculation data"""
        hour_fields = ['regular_hours', 'overtime_hours', 'double_time_hours', 'holiday_hours', 'vacation_hours', 'sick_hours']
        for field in hour_fields:
            value = getattr(self, field)
            if value is not None and value < 0:
                raise ValidationError(f"{field.replace('_', ' ').title()} cannot be negative")
        pay_fields = ['base_salary', 'hourly_rate', 'regular_pay', 'overtime_pay', 'holiday_pay', 'bonus_pay', 'commission_pay', 'other_earnings', 'gross_pay', 'federal_tax', 'state_tax', 'local_tax', 'social_security_tax', 'medicare_tax', 'other_taxes', 'total_taxes']
        for field in pay_fields:
            value = getattr(self, field)
            if value is not None and value < 0:
                raise ValidationError(f"{field.replace('_', ' ').title()} cannot be negative")
        deduction_fields = ['health_insurance', 'dental_insurance', 'vision_insurance', 'retirement_401k', 'retirement_403b', 'fsa_medical', 'fsa_dependent', 'hsa', 'other_pretax', 'total_pretax', 'garnishment', 'child_support', 'tax_levy', 'loan_repayment', 'union_dues', 'other_posttax', 'total_posttax']
        for field in deduction_fields:
            value = getattr(self, field)
            if value is not None and value < 0:
                raise ValidationError(f"{field.replace('_', ' ').title()} cannot be negative")
        calculated_net = self.gross_pay - self.total_taxes - self.total_pretax - self.total_posttax
        if abs(calculated_net - self.net_pay) > 0.01:
            raise ValidationError('Net pay calculation is incorrect')

    def save(self, *args, **kwargs):
        """Calculate totals before saving"""
        self.total_taxes = self.federal_tax + self.state_tax + self.local_tax + self.social_security_tax + self.medicare_tax + self.other_taxes
        self.total_pretax = self.health_insurance + self.dental_insurance + self.vision_insurance + self.retirement_401k + self.retirement_403b + self.fsa_medical + self.fsa_dependent + self.hsa + self.other_pretax
        self.total_posttax = self.garnishment + self.child_support + self.tax_levy + self.loan_repayment + self.union_dues + self.other_posttax
        self.total_employer_contributions = self.employer_health + self.employer_retirement + self.employer_futa + self.employer_suta + self.employer_other
        super().save(*args, **kwargs)

class PayrollDisbursement(models.Model):
    """
    Payroll disbursement and payment tracking
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='payrolldisbursement_company')
    payroll_run = models.ForeignKey(PayrollRun, on_delete=models.CASCADE, related_name='payrolldisbursement_payroll_run')
    employee = models.ForeignKey('hrm.Employee', on_delete=models.CASCADE, related_name='payrolldisbursement_employee')
    disbursement_number = models.CharField(max_length=50)
    disbursement_method = models.CharField(max_length=20, choices=[('direct_deposit', 'Direct Deposit'), ('check', 'Check'), ('cash', 'Cash'), ('wire', 'Wire Transfer')])
    gross_amount = models.DecimalField(max_digits=12, decimal_places=2)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    bank_name = models.CharField(max_length=200, blank=True)
    bank_routing_number = models.CharField(max_length=20, blank=True)
    bank_account_number = models.CharField(max_length=50, blank=True)
    bank_account_type = models.CharField(max_length=20, blank=True)
    check_number = models.CharField(max_length=20, blank=True)
    check_date = models.DateField(null=True, blank=True)
    check_status = models.CharField(max_length=20, choices=[('printed', 'Printed'), ('signed', 'Signed'), ('mailed', 'Mailed'), ('distributed', 'Distributed'), ('cashed', 'Cashed'), ('voided', 'Voided')], blank=True)
    disbursement_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('processed', 'Processed'), ('sent', 'Sent'), ('completed', 'Completed'), ('failed', 'Failed'), ('returned', 'Returned'), ('voided', 'Voided')], default='pending')
    processing_date = models.DateTimeField(null=True, blank=True)
    settlement_date = models.DateField(null=True, blank=True)
    confirmation_number = models.CharField(max_length=100, blank=True)
    tracking_number = models.CharField(max_length=100, blank=True)
    error_code = models.CharField(max_length=50, blank=True)
    error_message = models.TextField(blank=True)
    retry_count = models.IntegerField(default=0)
    retry_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_payroll_disbursements'
        verbose_name = 'Payroll Disbursement'
        verbose_name_plural = 'Payroll Disbursements'
        indexes = [models.Index(fields=['company', 'payroll_run'], name='idx_disbursement_run'), models.Index(fields=['company', 'employee'], name='idx_disbursement_employee'), models.Index(fields=['company', 'disbursement_status'], name='idx_disbursement_status')]
        constraints = [models.UniqueConstraint(fields=['company', 'disbursement_number'], name='uk_disbursement_number')]
        ordering = ['-processing_date']

    def __str__(self):
        return f'Disbursement {self.disbursement_number} - {self.employee}'

    def clean(self):
        """Validate payroll disbursement data"""
        if self.gross_amount and self.gross_amount < 0:
            raise ValidationError('Gross amount cannot be negative')
        if self.net_amount and self.net_amount < 0:
            raise ValidationError('Net amount cannot be negative')
        if self.net_amount and hasattr(self, 'payroll_run'):
            pass
        if self.retry_count and self.retry_count < 0:
            raise ValidationError('Retry count cannot be negative')
        if self.check_date and self.check_date:
            if self.check_date < timezone.now().date():
                raise ValidationError('Check date cannot be in the past for new disbursements')

class PayrollSchedule(models.Model):
    """
    Payroll schedule configuration
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='payrollschedule_company')
    schedule_name = models.CharField(max_length=200)
    pay_frequency = models.CharField(max_length=20)
    next_pay_date = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'hr_payroll_schedules'
        verbose_name = 'Payroll Schedule'
        verbose_name_plural = 'Payroll Schedules'

class EarningCode(models.Model):
    """
    Earning codes for different types of pay
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='earningcode_company')
    code = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    earning_type = models.CharField(max_length=50)
    is_taxable = models.BooleanField(default=True)

    class Meta:
        db_table = 'hr_earning_codes'
        verbose_name = 'Earning Code'
        verbose_name_plural = 'Earning Codes'