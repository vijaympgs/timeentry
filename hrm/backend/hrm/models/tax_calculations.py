"""
Tax Calculations Models for HRM
Following BBP 04.2 Tax Calculations specifications
Aligned with enterprise governance and Olivine UI canon
"""
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()

class TaxCalculation(models.Model):
    """
    Main tax calculation model for payroll tax processing
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='taxcalculation_company')
    employee = models.ForeignKey('hrm.Employee', on_delete=models.CASCADE, related_name='taxcalculation_employee')
    payroll_run = models.ForeignKey('hrm.PayrollRun', on_delete=models.CASCADE, related_name='taxcalculation_payroll_run')
    calculated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='taxcalculation_calculated_by')
    calculation_date = models.DateTimeField(auto_now_add=True)
    pay_period_start = models.DateField()
    pay_period_end = models.DateField()
    pay_frequency = models.CharField(max_length=20, choices=[('weekly', 'Weekly'), ('bi_weekly', 'Bi-Weekly'), ('semi_monthly', 'Semi-Monthly'), ('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('annual', 'Annual')])
    tax_year = models.IntegerField()
    gross_wages = models.DecimalField(max_digits=12, decimal_places=2)
    supplemental_wages = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    taxable_wages = models.DecimalField(max_digits=12, decimal_places=2)
    year_to_date_gross = models.DecimalField(max_digits=12, decimal_places=2)
    federal_income_tax = models.DecimalField(max_digits=12, decimal_places=2)
    social_security_tax = models.DecimalField(max_digits=12, decimal_places=2)
    medicare_tax = models.DecimalField(max_digits=12, decimal_places=2)
    additional_medicare_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    futa_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    state_income_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    state_disability_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    state_unemployment_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other_state_taxes = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    local_income_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    local_school_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    local_city_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other_local_taxes = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_tax_withholding = models.DecimalField(max_digits=12, decimal_places=2)
    total_employer_tax = models.DecimalField(max_digits=12, decimal_places=2)
    calculation_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('calculated', 'Calculated'), ('verified', 'Verified'), ('error', 'Error'), ('adjusted', 'Adjusted')], default='pending')
    validation_status = models.CharField(max_length=20, choices=[('not_validated', 'Not Validated'), ('validated', 'Validated'), ('validation_failed', 'Validation Failed')], default='not_validated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_tax_calculations'
        verbose_name = 'Tax Calculation'
        verbose_name_plural = 'Tax Calculations'
        indexes = [models.Index(fields=['company', 'employee'], name='idx_tax_employee'), models.Index(fields=['company', 'payroll_run'], name='idx_tax_payroll'), models.Index(fields=['company', 'tax_year'], name='idx_tax_year'), models.Index(fields=['company', 'calculation_status'], name='idx_tax_status')]
        ordering = ['-calculation_date']

    def __str__(self):
        return f'Tax Calculation {self.employee} - {self.pay_period_end}'

    def clean(self):
        """Validate tax calculation data"""
        if self.tax_year and (self.tax_year < 2000 or self.tax_year > 2100):
            raise ValidationError('Tax year must be between 2000 and 2100')
        if self.pay_period_start and self.pay_period_end:
            if self.pay_period_start >= self.pay_period_end:
                raise ValidationError('Pay period start must be before end date')
        if self.gross_wages and self.gross_wages < 0:
            raise ValidationError('Gross wages cannot be negative')
        tax_fields = ['federal_income_tax', 'social_security_tax', 'medicare_tax', 'additional_medicare_tax', 'futa_tax', 'state_income_tax', 'state_disability_tax', 'state_unemployment_tax', 'other_state_taxes', 'local_income_tax', 'local_school_tax', 'local_city_tax', 'other_local_taxes']
        for field in tax_fields:
            value = getattr(self, field)
            if value is not None and value < 0:
                raise ValidationError(f"{field.replace('_', ' ').title()} cannot be negative")

    def save(self, *args, **kwargs):
        """Calculate total taxes before saving"""
        self.total_tax_withholding = self.federal_income_tax + self.social_security_tax + self.medicare_tax + self.additional_medicare_tax + self.state_income_tax + self.state_disability_tax + self.local_income_tax + self.local_school_tax + self.local_city_tax + self.other_state_taxes + self.other_local_taxes
        self.total_employer_tax = self.social_security_tax + self.medicare_tax + self.futa_tax + self.state_unemployment_tax + self.state_disability_tax
        super().save(*args, **kwargs)

class TaxWithholding(models.Model):
    """
    Employee tax withholding preferences and allowances
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='taxwithholding_company')
    employee = models.ForeignKey('hrm.Employee', on_delete=models.CASCADE, related_name='taxwithholding_employee')
    federal_filing_status = models.CharField(max_length=50, choices=[('single', 'Single'), ('married_filing_jointly', 'Married Filing Jointly'), ('married_filing_separately', 'Married Filing Separately'), ('head_of_household', 'Head of Household'), ('qualifying_widow', 'Qualifying Widow(er)')])
    federal_allowances = models.IntegerField(default=0)
    additional_federal_withholding = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    federal_exempt = models.BooleanField(default=False)
    state_filing_status = models.CharField(max_length=50, blank=True)
    state_allowances = models.IntegerField(default=0)
    additional_state_withholding = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    state_exempt = models.BooleanField(default=False)
    local_filing_status = models.CharField(max_length=50, blank=True)
    local_allowances = models.IntegerField(default=0)
    additional_local_withholding = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    local_exempt = models.BooleanField(default=False)
    nonresident_alien = models.BooleanField(default=False)
    dual_status_alien = models.BooleanField(default=False)
    exemption_from_withholding = models.BooleanField(default=False)
    tax_treaty_country = models.CharField(max_length=100, blank=True)
    tax_treaty_article = models.CharField(max_length=100, blank=True)
    tax_treaty_exemption_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    additional_withholding_401k = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    additional_withholding_health = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    additional_withholding_other = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    effective_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive'), ('pending', 'Pending')], default='active')
    w4_form_date = models.DateField(null=True, blank=True)
    w4_form_url = models.URLField(blank=True)
    state_w4_form_date = models.DateField(null=True, blank=True)
    state_w4_form_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_tax_withholding'
        verbose_name = 'Tax Withholding'
        verbose_name_plural = 'Tax Withholding'
        indexes = [models.Index(fields=['company', 'employee'], name='idx_withholding_employee'), models.Index(fields=['company', 'status'], name='idx_withholding_status')]
        ordering = ['-effective_date']

    def __str__(self):
        return f'Tax Withholding - {self.employee}'

    def clean(self):
        """Validate tax withholding data"""
        if self.federal_allowances and self.federal_allowances < 0:
            raise ValidationError('Federal allowances cannot be negative')
        if self.state_allowances and self.state_allowances < 0:
            raise ValidationError('State allowances cannot be negative')
        if self.local_allowances and self.local_allowances < 0:
            raise ValidationError('Local allowances cannot be negative')
        withholding_fields = ['additional_federal_withholding', 'additional_state_withholding', 'additional_local_withholding', 'additional_withholding_401k', 'additional_withholding_health', 'additional_withholding_other']
        for field in withholding_fields:
            value = getattr(self, field)
            if value is not None and value < 0:
                raise ValidationError(f"{field.replace('_', ' ').title()} cannot be negative")
        if self.effective_date and self.expiry_date:
            if self.effective_date >= self.expiry_date:
                raise ValidationError('Expiry date must be after effective date')
        if self.federal_allowances and self.federal_allowances > 10:
            raise ValidationError('Federal allowances cannot exceed 10 without special circumstances')

class TaxJurisdiction(models.Model):
    """
    Tax jurisdictions and their configuration
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='taxjurisdiction_company')
    jurisdiction_type = models.CharField(max_length=20, choices=[('federal', 'Federal'), ('state', 'State'), ('local', 'Local'), ('school_district', 'School District'), ('city', 'City'), ('county', 'County')])
    jurisdiction_name = models.CharField(max_length=200)
    jurisdiction_code = models.CharField(max_length=50)
    state_code = models.CharField(max_length=10, blank=True)
    country_code = models.CharField(max_length=10, default='US')
    tax_type = models.CharField(max_length=50, choices=[('income_tax', 'Income Tax'), ('unemployment_tax', 'Unemployment Tax'), ('disability_tax', 'Disability Tax'), ('transit_tax', 'Transit Tax'), ('school_tax', 'School Tax'), ('other', 'Other')])
    tax_rate_type = models.CharField(max_length=20, choices=[('flat', 'Flat Rate'), ('progressive', 'Progressive'), ('tiered', 'Tiered')])
    tax_rates_data = models.JSONField(default=list)
    wage_base_limit = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    minimum_wage_threshold = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    employee_responsible = models.BooleanField(default=True)
    employer_responsible = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive'), ('pending', 'Pending'), ('deprecated', 'Deprecated')], default='active')
    effective_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    filing_frequency = models.CharField(max_length=20, choices=[('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('annual', 'Annual'), ('semi_annual', 'Semi-Annual')])
    filing_agency = models.CharField(max_length=200, blank=True)
    filing_form = models.CharField(max_length=100, blank=True)
    special_rules = models.JSONField(default=dict, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_tax_jurisdictions'
        verbose_name = 'Tax Jurisdiction'
        verbose_name_plural = 'Tax Jurisdictions'
        indexes = [models.Index(fields=['company', 'jurisdiction_type'], name='idx_jurisdiction_type'), models.Index(fields=['company', 'state_code'], name='idx_jurisdiction_state'), models.Index(fields=['company', 'status'], name='idx_jurisdiction_status')]
        constraints = [models.UniqueConstraint(fields=['company', 'jurisdiction_code'], name='uk_jurisdiction_code')]
        ordering = ['jurisdiction_type', 'jurisdiction_name']

    def __str__(self):
        return f'{self.jurisdiction_name} ({self.jurisdiction_code})'

    def clean(self):
        """Validate tax jurisdiction data"""
        if self.wage_base_limit and self.wage_base_limit < 0:
            raise ValidationError('Wage base limit cannot be negative')
        if self.minimum_wage_threshold and self.minimum_wage_threshold < 0:
            raise ValidationError('Minimum wage threshold cannot be negative')
        if not self.tax_rates or len(self.tax_rates) == 0:
            raise ValidationError('Tax rates must be configured')
        if self.effective_date and self.expiry_date:
            if self.effective_date >= self.expiry_date:
                raise ValidationError('Expiry date must be after effective date')

class TaxRate(models.Model):
    """
    Tax rate brackets and configurations
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='taxrate_company')
    tax_jurisdiction = models.ForeignKey(TaxJurisdiction, on_delete=models.CASCADE, related_name='taxrate_tax_jurisdiction')
    bracket_number = models.IntegerField()
    minimum_wage = models.DecimalField(max_digits=12, decimal_places=2)
    maximum_wage = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    tax_rate = models.DecimalField(max_digits=8, decimal_places=6)
    base_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    effective_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'hr_tax_rates'
        verbose_name = 'Tax Rate'
        verbose_name_plural = 'Tax Rates'

class TaxExemption(models.Model):
    """
    Tax exemptions and deductions
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='taxexemption_company')
    employee = models.ForeignKey('hrm.Employee', on_delete=models.CASCADE, related_name='taxexemption_employee')
    exemption_type = models.CharField(max_length=50)
    exemption_amount = models.DecimalField(max_digits=12, decimal_places=2)
    tax_jurisdiction = models.ForeignKey(TaxJurisdiction, on_delete=models.CASCADE, related_name='taxexemption_tax_jurisdiction')
    effective_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'hr_tax_exemptions'
        verbose_name = 'Tax Exemption'
        verbose_name_plural = 'Tax Exemptions'

class TaxPayrollRun(models.Model):
    """
    Payroll run reference model for tax calculations (avoiding conflict with main PayrollRun model)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='taxpayrollrun_company')
    run_number = models.CharField(max_length=50)
    run_date = models.DateTimeField()
    status = models.CharField(max_length=20)

    class Meta:
        db_table = 'hr_tax_payroll_runs'
        verbose_name = 'Tax Payroll Run'
        verbose_name_plural = 'Tax Payroll Runs'