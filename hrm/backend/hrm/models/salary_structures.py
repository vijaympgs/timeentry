"""
Salary Structures Models for HRM
Following BBP 04.1 Salary Structures specifications
Aligned with enterprise governance and Olivine UI canon
"""
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()

class SalaryStructure(models.Model):
    """
    Main salary structure model for compensation management
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    grade_level = models.CharField(max_length=50, blank=True)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='salarystructure_company')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='salarystructure_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='salarystructure_updated_by')
    structure_name = models.CharField(max_length=200)
    structure_code = models.CharField(max_length=50)
    structure_type = models.CharField(max_length=50, choices=[('corporate', 'Corporate'), ('executive', 'Executive'), ('sales', 'Sales'), ('technical', 'Technical'), ('hourly', 'Hourly'), ('contract', 'Contract'), ('intern', 'Intern'), ('regional', 'Regional')], default='corporate')
    status = models.CharField(max_length=20, choices=[('draft', 'Draft'), ('active', 'Active'), ('pending_approval', 'Pending Approval'), ('approved', 'Approved'), ('deprecated', 'Deprecated')], default='draft')
    effective_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    currency = models.CharField(max_length=10, default='USD')
    pay_frequency = models.CharField(max_length=20, choices=[('hourly', 'Hourly'), ('weekly', 'Weekly'), ('bi_weekly', 'Bi-Weekly'), ('semi_monthly', 'Semi-Monthly'), ('monthly', 'Monthly'), ('annual', 'Annual')], default='annual')
    description = models.TextField(blank=True)
    guidelines = models.TextField(blank=True)
    approval_required = models.BooleanField(default=True)
    approval_workflow = models.JSONField(default=dict, blank=True)
    market_data_source = models.CharField(max_length=200, blank=True)
    market_positioning = models.CharField(max_length=50, choices=[('lag', 'Lag'), ('match', 'Match'), ('lead', 'Lead')], default='match')
    market_position_percentage = models.IntegerField(default=50)
    geographic_differentials_enabled = models.BooleanField(default=False)
    default_geographic_differential = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_salary_structures'
        verbose_name = 'Salary Structure'
        verbose_name_plural = 'Salary Structures'
        indexes = [models.Index(fields=['company', 'status'], name='idx_structure_status'), models.Index(fields=['company', 'structure_type'], name='idx_structure_type'), models.Index(fields=['company', 'effective_date'], name='idx_structure_effective')]
        constraints = [models.UniqueConstraint(fields=['company', 'structure_code'], name='uk_structure_code')]
        ordering = ['structure_type', 'grade_level']

    def __str__(self):
        return f'{self.structure_name} ({self.structure_code})'

    def clean(self):
        """Validate salary structure data"""
        if self.effective_date and self.effective_date < timezone.now().date():
            if not self.pk:
                raise ValidationError('Effective date cannot be in the past')
        if self.expiry_date and self.effective_date and (self.expiry_date <= self.effective_date):
            raise ValidationError('Expiry date must be after effective date')
        if not 0 <= self.market_position_percentage <= 100:
            raise ValidationError('Market position percentage must be between 0 and 100')
        if self.default_geographic_differential and self.default_geographic_differential <= 0:
            raise ValidationError('Geographic differential must be positive')

class PayGrade(models.Model):
    """
    Pay grades within salary structures
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='paygrade_company')
    salary_structure = models.ForeignKey(SalaryStructure, on_delete=models.CASCADE, related_name='paygrade_salary_structure')
    grade_code = models.CharField(max_length=50)
    grade_name = models.CharField(max_length=200)
    grade_level = models.IntegerField()
    job_family = models.CharField(max_length=100, blank=True)
    job_category = models.CharField(max_length=100, blank=True)
    minimum_salary = models.DecimalField(max_digits=12, decimal_places=2)
    midpoint_salary = models.DecimalField(max_digits=12, decimal_places=2)
    maximum_salary = models.DecimalField(max_digits=12, decimal_places=2)
    range_spread_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    midpoint_to_min_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    max_to_midpoint_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    target_positioning = models.CharField(max_length=50, choices=[('minimum', 'Minimum'), ('quartile_1', '1st Quartile'), ('midpoint', 'Midpoint'), ('quartile_3', '3rd Quartile'), ('maximum', 'Maximum')], default='midpoint')
    target_positioning_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=50.0)
    promotion_eligible = models.BooleanField(default=True)
    promotion_to_grade = models.CharField(max_length=50, blank=True)
    merit_increase_range_min = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    merit_increase_range_max = models.DecimalField(max_digits=5, decimal_places=2, default=5.0)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive'), ('phased_out', 'Phased Out')], default='active')
    effective_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    special_requirements = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_pay_grades'
        verbose_name = 'Pay Grade'
        verbose_name_plural = 'Pay Grades'
        indexes = [models.Index(fields=['company', 'salary_structure'], name='idx_grade_structure'), models.Index(fields=['company', 'grade_level'], name='idx_grade_level'), models.Index(fields=['company', 'status'], name='idx_grade_status')]
        constraints = [models.UniqueConstraint(fields=['company', 'salary_structure', 'grade_code'], name='uk_grade_code')]
        ordering = ['grade_level']

    def __str__(self):
        return f'{self.grade_name} ({self.grade_code})'

    def clean(self):
        """Validate pay grade data"""
        if self.minimum_salary >= self.midpoint_salary:
            raise ValidationError('Minimum salary must be less than midpoint salary')
        if self.midpoint_salary >= self.maximum_salary:
            raise ValidationError('Midpoint salary must be less than maximum salary')
        if self.range_spread_percentage and (not 20 <= self.range_spread_percentage <= 200):
            raise ValidationError('Range spread percentage must be between 20 and 200')
        if self.merit_increase_range_min < 0 or self.merit_increase_range_max < 0:
            raise ValidationError('Merit increase ranges cannot be negative')
        if self.merit_increase_range_min > self.merit_increase_range_max:
            raise ValidationError('Minimum merit increase cannot exceed maximum merit increase')
        if not 0 <= self.target_positioning_percentage <= 100:
            raise ValidationError('Target positioning percentage must be between 0 and 100')

    def save(self, *args, **kwargs):
        """Calculate range percentages before saving"""
        if self.minimum_salary and self.midpoint_salary and self.maximum_salary:
            range_width = self.maximum_salary - self.minimum_salary
            if self.midpoint_salary > 0:
                self.range_spread_percentage = range_width / self.midpoint_salary * 100
            midpoint_to_min = self.midpoint_salary - self.minimum_salary
            if self.midpoint_salary > 0:
                self.midpoint_to_min_percentage = midpoint_to_min / self.midpoint_salary * 100
            max_to_midpoint = self.maximum_salary - self.midpoint_salary
            if self.midpoint_salary > 0:
                self.max_to_midpoint_percentage = max_to_midpoint / self.midpoint_salary * 100
        super().save(*args, **kwargs)

class CompensationRange(models.Model):
    """
    Detailed compensation ranges with geographic and other differentials
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='compensationrange_company')
    pay_grade = models.ForeignKey(PayGrade, on_delete=models.CASCADE, related_name='compensationrange_pay_grade')
    range_name = models.CharField(max_length=200)
    range_type = models.CharField(max_length=50, choices=[('base', 'Base Salary'), ('total_cash', 'Total Cash'), ('total_compensation', 'Total Compensation'), ('bonus_target', 'Bonus Target'), ('equity_value', 'Equity Value')], default='base')
    geographic_area = models.CharField(max_length=200)
    geographic_differential = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    adjusted_minimum = models.DecimalField(max_digits=12, decimal_places=2)
    adjusted_midpoint = models.DecimalField(max_digits=12, decimal_places=2)
    adjusted_maximum = models.DecimalField(max_digits=12, decimal_places=2)
    market_minimum = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    market_midpoint = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    market_maximum = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    market_data_source = models.CharField(max_length=200, blank=True)
    market_data_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive'), ('pending_review', 'Pending Review')], default='active')
    effective_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_compensation_ranges'
        verbose_name = 'Compensation Range'
        verbose_name_plural = 'Compensation Ranges'
        indexes = [models.Index(fields=['company', 'pay_grade'], name='idx_range_grade'), models.Index(fields=['company', 'geographic_area'], name='idx_range_geo'), models.Index(fields=['company', 'range_type'], name='idx_range_type')]
        ordering = ['geographic_area', 'range_type']

    def __str__(self):
        return f'{self.range_name} - {self.geographic_area}'

    def clean(self):
        """Validate compensation range data"""
        if self.geographic_differential and (not 0.5 <= self.geographic_differential <= 2.0):
            raise ValidationError('Geographic differential must be between 0.5 and 2.0')
        if self.adjusted_minimum >= self.adjusted_midpoint:
            raise ValidationError('Adjusted minimum salary must be less than adjusted midpoint salary')
        if self.adjusted_midpoint >= self.adjusted_maximum:
            raise ValidationError('Adjusted midpoint salary must be less than adjusted maximum salary')
        if self.market_minimum and self.market_midpoint and (self.market_minimum >= self.market_midpoint):
            raise ValidationError('Market minimum must be less than market midpoint')
        if self.market_midpoint and self.market_maximum and (self.market_midpoint >= self.market_maximum):
            raise ValidationError('Market midpoint must be less than market maximum')

    def save(self, *args, **kwargs):
        """Calculate adjusted salaries based on geographic differential"""
        if self.pay_grade and self.geographic_differential:
            base_minimum = self.pay_grade.minimum_salary
            base_midpoint = self.pay_grade.midpoint_salary
            base_maximum = self.pay_grade.maximum_salary
            self.adjusted_minimum = base_minimum * self.geographic_differential
            self.adjusted_midpoint = base_midpoint * self.geographic_differential
            self.adjusted_maximum = base_maximum * self.geographic_differential
        super().save(*args, **kwargs)

class JobLevel(models.Model):
    """
    Job levels for compensation mapping
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='joblevel_company')
    level_code = models.CharField(max_length=50)
    level_name = models.CharField(max_length=200)
    level_number = models.IntegerField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'hr_job_levels'
        verbose_name = 'Job Level'
        verbose_name_plural = 'Job Levels'
        indexes = [models.Index(fields=['company', 'level_number'], name='idx_job_level_number')]
        constraints = [models.UniqueConstraint(fields=['company', 'level_code'], name='uk_job_level_code')]

class MarketData(models.Model):
    """
    Market benchmarking data
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='marketdata_company')
    survey_name = models.CharField(max_length=200)
    survey_provider = models.CharField(max_length=200)
    job_family = models.CharField(max_length=100)
    job_level = models.CharField(max_length=100)
    geographic_area = models.CharField(max_length=200)
    percentile_25 = models.DecimalField(max_digits=12, decimal_places=2)
    percentile_50 = models.DecimalField(max_digits=12, decimal_places=2)
    percentile_75 = models.DecimalField(max_digits=12, decimal_places=2)
    effective_date = models.DateField()

    class Meta:
        db_table = 'hr_market_data'
        verbose_name = 'Market Data'
        verbose_name_plural = 'Market Data'
        indexes = [models.Index(fields=['company', 'job_family', 'job_level'], name='idx_market_job'), models.Index(fields=['company', 'geographic_area'], name='idx_market_geo')]