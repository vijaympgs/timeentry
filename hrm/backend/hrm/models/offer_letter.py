"""
Offer Letter Template Models for HRM
Following BBP 15.1 Offer Letter specifications
Aligned with enterprise governance and Olivine UI canon
"""
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()

class OfferLetterTemplate(models.Model):
    """
    Main offer letter template model for recruitment
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='offerlettertemplate_company')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='offerlettertemplate_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='offerlettertemplate_updated_by')
    template_name = models.CharField(max_length=200)
    template_code = models.CharField(max_length=50)
    template_description = models.TextField(blank=True)
    template_type = models.CharField(max_length=50, choices=[('standard', 'Standard Offer'), ('executive', 'Executive Offer'), ('internship', 'Internship Offer'), ('contract', 'Contract Offer'), ('temporary', 'Temporary Offer'), ('part_time', 'Part-time Offer'), ('remote', 'Remote Work Offer'), ('international', 'International Offer'), ('internal', 'Internal Transfer'), ('promotion', 'Promotion Offer'), ('custom', 'Custom Template')])
    template_category = models.CharField(max_length=100, choices=[('technology', 'Technology'), ('sales', 'Sales'), ('marketing', 'Marketing'), ('finance', 'Finance'), ('hr', 'Human Resources'), ('operations', 'Operations'), ('customer_service', 'Customer Service'), ('engineering', 'Engineering'), ('management', 'Management'), ('administrative', 'Administrative'), ('custom', 'Custom')])
    template_content = models.TextField()
    template_variables = models.JSONField(default=dict, blank=True)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    version = models.CharField(max_length=20, default='1.0')
    legal_disclaimer = models.TextField(blank=True)
    compliance_notes = models.TextField(blank=True)
    required_signatures = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=20, choices=[('draft', 'Draft'), ('active', 'Active'), ('inactive', 'Inactive'), ('archived', 'Archived'), ('deprecated', 'Deprecated')], default='draft')
    effective_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    usage_count = models.IntegerField(default=0)
    last_used_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_offer_letter_templates'
        verbose_name = 'Offer Letter Template'
        verbose_name_plural = 'Offer Letter Templates'
        indexes = [models.Index(fields=['company', 'status'], name='idx_template_status'), models.Index(fields=['company', 'template_type'], name='idx_template_type'), models.Index(fields=['company', 'template_category'], name='idx_template_category')]
        constraints = [models.UniqueConstraint(fields=['company', 'template_code'], name='uk_template_code')]
        ordering = ['template_name']

    def __str__(self):
        return f'{self.template_name} ({self.template_code})'

    def clean(self):
        """Validate offer letter template data"""
        if self.effective_date and self.expiry_date:
            if self.effective_date >= self.expiry_date:
                raise ValidationError('Expiry date must be after effective date')
        if self.version and (not self.version.replace('.', '').isdigit()):
            raise ValidationError('Version must be in format X.Y')
        if self.usage_count and self.usage_count < 0:
            raise ValidationError('Usage count cannot be negative')

class OfferLetter(models.Model):
    """
    Individual offer letter records
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='offerletter_company')
    template = models.ForeignKey(OfferLetterTemplate, on_delete=models.PROTECT, related_name='offerletter_template')
    candidate = models.ForeignKey('hrm.Candidate', on_delete=models.CASCADE, related_name='offerletter_candidate')
    job_position = models.ForeignKey('hrm.Position', on_delete=models.CASCADE, related_name='offerletter_job_position')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='offerletter_created_by')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='offerletter_approved_by')
    offer_number = models.CharField(max_length=50)
    offer_date = models.DateTimeField(auto_now_add=True)
    offer_status = models.CharField(max_length=20, choices=[('draft', 'Draft'), ('pending_approval', 'Pending Approval'), ('approved', 'Approved'), ('sent', 'Sent'), ('accepted', 'Accepted'), ('declined', 'Declined'), ('withdrawn', 'Withdrawn'), ('expired', 'Expired'), ('revoked', 'Revoked')], default='draft')
    start_date = models.DateField()
    employment_type = models.CharField(max_length=50, choices=[('full_time', 'Full Time'), ('part_time', 'Part Time'), ('contract', 'Contract'), ('internship', 'Internship'), ('temporary', 'Temporary'), ('remote', 'Remote Work')])
    work_schedule = models.CharField(max_length=50, choices=[('standard', 'Standard'), ('flexible', 'Flexible'), ('compressed', 'Compressed'), ('shift_based', 'Shift Based')])
    salary_amount = models.DecimalField(max_digits=12, decimal_places=2)
    salary_currency = models.CharField(max_length=10, default='USD')
    salary_frequency = models.CharField(max_length=20, choices=[('annual', 'Annual'), ('monthly', 'Monthly'), ('hourly', 'Hourly'), ('bi_weekly', 'Bi-Weekly'), ('semi_monthly', 'Semi-Monthly')])
    bonus_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    bonus_currency = models.CharField(max_length=10, blank=True)
    benefits_package = models.JSONField(default=dict, blank=True)
    benefits_description = models.TextField(blank=True)
    reports_to_employee = models.ForeignKey('hrm.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='offerletter_reports_to_employee')
    department = models.ForeignKey('hrm.OrganizationalUnit', on_delete=models.SET_NULL, null=True, blank=True, related_name='offerletter_department')
    probation_period_months = models.IntegerField(null=True, blank=True)
    notice_period_days = models.IntegerField(null=True, blank=True)
    confidentiality_required = models.BooleanField(default=True)
    non_compete_clause = models.BooleanField(default=False)
    offer_letter_content = models.TextField()
    email_content = models.TextField(blank=True)
    sent_date = models.DateTimeField(null=True, blank=True)
    response_deadline = models.DateTimeField(null=True, blank=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    acceptance_date = models.DateTimeField(null=True, blank=True)
    decline_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_offer_letters'
        verbose_name = 'Offer Letter'
        verbose_name_plural = 'Offer Letters'
        indexes = [models.Index(fields=['company', 'offer_status'], name='idx_offer_status'), models.Index(fields=['company', 'candidate'], name='idx_offer_candidate'), models.Index(fields=['company', 'job_position'], name='idx_offer_position'), models.Index(fields=['company', 'offer_date'], name='idx_offer_date')]
        constraints = [models.UniqueConstraint(fields=['company', 'offer_number'], name='uk_offer_number')]
        ordering = ['-offer_date']

    def __str__(self):
        return f'Offer: {self.candidate} - {self.job_position}'

    def clean(self):
        """Validate offer letter data"""
        if self.offer_date and self.offer_date > timezone.now():
            if not self.pk:
                raise ValidationError('Offer date cannot be in the future')
        if self.start_date and self.start_date < timezone.now().date():
            raise ValidationError('Start date cannot be in the past')
        if self.salary_amount and self.salary_amount < 0:
            raise ValidationError('Salary amount cannot be negative')
        if self.bonus_amount and self.bonus_amount < 0:
            raise ValidationError('Bonus amount cannot be negative')
        if self.probation_period_months and self.probation_months < 0:
            raise ValidationError('Probation period cannot be negative')
        if self.notice_period_days and self.notice_period_days < 0:
            raise ValidationError('Notice period cannot be negative')
        if self.approval_date and self.offer_date and (self.approval_date < self.offer_date):
            raise ValidationError('Approval date cannot be before offer date')
        if self.response_deadline and self.offer_date and (self.response_deadline <= self.offer_date):
            raise ValidationError('Response deadline must be after offer date')
        if self.acceptance_date and self.offer_date and (self.acceptance_date < self.offer_date):
            raise ValidationError('Acceptance date cannot be before offer date')

class Candidate(models.Model):
    """
    Candidate information for offer letters
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='candidate_company')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'hr_candidates'
        verbose_name = 'Candidate'
        verbose_name_plural = 'Candidates'
        constraints = [models.UniqueConstraint(fields=['company', 'email'], name='uk_candidate_email')]

class OfferPosition(models.Model):
    """
    Position information for offer letters (avoiding conflict with main Position model)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='offerposition_company')
    title = models.CharField(max_length=200)
    position_code = models.CharField(max_length=50)
    job_grade = models.CharField(max_length=50)
    job_family = models.CharField(max_length=100)

    class Meta:
        db_table = 'hr_offer_positions'
        verbose_name = 'Offer Position'
        verbose_name_plural = 'Offer Positions'
        constraints = [models.UniqueConstraint(fields=['company', 'position_code'], name='uk_offer_position_code')]