"""
Screening Models for HRM
Following BBP 03.2 Screening specifications
Aligned with enterprise governance and Olivine UI canon
"""
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()

class ScreeningProcess(models.Model):
    """
    Main screening process model for tracking application screening
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='screeningprocess_company')
    application = models.ForeignKey('hrm.JobApplication', on_delete=models.CASCADE, related_name='screeningprocess_application')
    job_posting = models.ForeignKey('hrm.JobPosting', on_delete=models.CASCADE, related_name='screeningprocess_job_posting')
    candidate = models.ForeignKey('hrm.Candidate', on_delete=models.CASCADE, related_name='screeningprocess_candidate')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='screeningprocess_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='screeningprocess_updated_by')
    primary_screener = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='screeningprocess_primary_screener')
    secondary_screener = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='screeningprocess_secondary_screener')
    final_approver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='screeningprocess_final_approver')
    screening_number = models.CharField(max_length=50)
    screening_date = models.DateTimeField(auto_now_add=True)
    screening_type = models.CharField(max_length=50, choices=[('initial', 'Initial Screening'), ('technical', 'Technical Screening'), ('background', 'Background Check'), ('reference', 'Reference Check'), ('comprehensive', 'Comprehensive Screening')], default='initial')
    status = models.CharField(max_length=50, choices=[('initiated', 'Initiated'), ('in_progress', 'In Progress'), ('pending_verification', 'Pending Verification'), ('completed', 'Completed'), ('on_hold', 'On Hold'), ('failed', 'Failed'), ('passed', 'Passed'), ('rejected', 'Rejected')], default='initiated')
    overall_score = models.IntegerField(null=True, blank=True)
    max_score = models.IntegerField(default=100)
    screening_decision = models.CharField(max_length=50, choices=[('pass', 'Pass'), ('fail', 'Fail'), ('conditional', 'Conditional Pass'), ('pending', 'Pending Review')], blank=True)
    priority = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('urgent', 'Urgent')], default='medium')
    target_completion_date = models.DateField(null=True, blank=True)
    actual_completion_date = models.DateField(null=True, blank=True)
    compliance_notes = models.TextField(blank=True)
    audit_required = models.BooleanField(default=False)
    audit_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_screening_processes'
        verbose_name = 'Screening Process'
        verbose_name_plural = 'Screening Processes'
        indexes = [models.Index(fields=['company', 'application'], name='idx_screening_app'), models.Index(fields=['company', 'status'], name='idx_screening_status'), models.Index(fields=['company', 'screening_date'], name='idx_screening_date')]
        constraints = [models.UniqueConstraint(fields=['company', 'screening_number'], name='uk_screening_number')]
        ordering = ['-screening_date']

    def __str__(self):
        return f'Screening {self.screening_number} - {self.candidate}'

    def clean(self):
        """Validate screening process data"""
        if self.overall_score is not None and self.overall_score > self.max_score:
            raise ValidationError('Overall score cannot exceed maximum score')
        if self.status == 'completed' and (not self.screening_decision):
            raise ValidationError('Screening decision is required when status is completed')
        if self.target_completion_date and self.target_completion_date < timezone.now().date():
            raise ValidationError('Target completion date cannot be in the past')

class ScreeningCriteria(models.Model):
    """
    Screening criteria and evaluation parameters
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='screeningcriteria_company')
    screening_process = models.ForeignKey(ScreeningProcess, on_delete=models.CASCADE, related_name='screeningcriteria_screening_process')
    evaluator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='screeningcriteria_evaluator')
    criteria_name = models.CharField(max_length=200)
    criteria_type = models.CharField(max_length=50, choices=[('skill', 'Skill Assessment'), ('experience', 'Experience Validation'), ('education', 'Education Verification'), ('certification', 'Certification Check'), ('background', 'Background Check'), ('reference', 'Reference Check'), ('legal', 'Legal Compliance'), ('custom', 'Custom Criteria')])
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    max_points = models.IntegerField(default=10)
    awarded_points = models.IntegerField(null=True, blank=True)
    score_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    evaluation_method = models.CharField(max_length=50, choices=[('automated', 'Automated'), ('manual', 'Manual'), ('hybrid', 'Hybrid')], default='manual')
    result = models.CharField(max_length=50, choices=[('pass', 'Pass'), ('fail', 'Fail'), ('partial', 'Partial'), ('pending', 'Pending'), ('not_applicable', 'Not Applicable')], blank=True)
    notes = models.TextField(blank=True)
    evaluation_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_screening_criteria'
        verbose_name = 'Screening Criteria'
        verbose_name_plural = 'Screening Criteria'
        indexes = [models.Index(fields=['company', 'screening_process'], name='idx_criteria_process'), models.Index(fields=['company', 'criteria_type'], name='idx_criteria_type')]
        ordering = ['criteria_name']

    def __str__(self):
        return f'{self.criteria_name} - {self.screening_process}'

    def clean(self):
        """Validate screening criteria data"""
        if self.awarded_points is not None and self.awarded_points > self.max_points:
            raise ValidationError('Awarded points cannot exceed maximum points')
        if self.weight and self.weight <= 0:
            raise ValidationError('Weight must be positive')
        if self.max_points and self.max_points <= 0:
            raise ValidationError('Maximum points must be positive')

    def save(self, *args, **kwargs):
        """Calculate score percentage before saving"""
        if self.awarded_points is not None and self.max_points > 0:
            self.score_percentage = self.awarded_points / self.max_points * 100
        super().save(*args, **kwargs)

class BackgroundCheck(models.Model):
    """
    Background check details and results
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='backgroundcheck_company')
    screening_process = models.ForeignKey(ScreeningProcess, on_delete=models.CASCADE, related_name='backgroundcheck_screening_process')
    candidate = models.ForeignKey('hrm.Candidate', on_delete=models.CASCADE, related_name='backgroundcheck_candidate')
    check_type = models.CharField(max_length=50, choices=[('criminal', 'Criminal Record'), ('credit', 'Credit History'), ('employment', 'Employment Verification'), ('education', 'Education Verification'), ('reference', 'Reference Check'), ('drug_test', 'Drug Test'), ('motor_vehicle', 'Motor Vehicle Record'), ('professional_license', 'Professional License'), ('social_media', 'Social Media Screening')])
    provider_name = models.CharField(max_length=200)
    provider_reference = models.CharField(max_length=100, blank=True)
    provider_contact = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=50, choices=[('requested', 'Requested'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('failed', 'Failed'), ('cancelled', 'Cancelled'), ('expedited', 'Expedited')], default='requested')
    request_date = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    expected_completion_date = models.DateTimeField(null=True, blank=True)
    check_result = models.CharField(max_length=50, choices=[('clear', 'Clear'), ('caution', 'Caution'), ('adverse', 'Adverse'), ('pending', 'Pending'), ('unable_to_complete', 'Unable to Complete')], blank=True)
    result_details = models.TextField(blank=True)
    adverse_action_required = models.BooleanField(default=False)
    adverse_action_reason = models.TextField(blank=True)
    consent_form_url = models.URLField(blank=True)
    report_url = models.URLField(blank=True)
    supporting_documents = models.JSONField(default=list, blank=True)
    check_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost_center = models.CharField(max_length=100, blank=True)
    billed_to_company = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_background_checks'
        verbose_name = 'Background Check'
        verbose_name_plural = 'Background Checks'
        indexes = [models.Index(fields=['company', 'screening_process'], name='idx_bg_process'), models.Index(fields=['company', 'status'], name='idx_bg_status'), models.Index(fields=['company', 'check_type'], name='idx_bg_type')]
        ordering = ['-request_date']

    def __str__(self):
        return f'{self.check_type} - {self.candidate}'

    def clean(self):
        """Validate background check data"""
        if self.check_cost and self.check_cost < 0:
            raise ValidationError('Check cost cannot be negative')
        if self.expected_completion_date and self.expected_completion_date < timezone.now():
            raise ValidationError('Expected completion date cannot be in the past')
        if self.completion_date and self.request_date and (self.completion_date < self.request_date):
            raise ValidationError('Completion date cannot be before request date')

class ScreeningTemplate(models.Model):
    """
    Reusable screening templates for different job types
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='screeningtemplate_company')
    template_name = models.CharField(max_length=200)
    job_category = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    criteria_config = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'hr_screening_templates'
        verbose_name = 'Screening Template'
        verbose_name_plural = 'Screening Templates'

class BackgroundCheckProvider(models.Model):
    """
    Background check service providers
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='backgroundcheckprovider_company')
    provider_name = models.CharField(max_length=200)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=50)
    api_endpoint = models.URLField(blank=True)
    api_key = models.CharField(max_length=200, blank=True)
    supported_checks = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'hr_bg_check_providers'
        verbose_name = 'Background Check Provider'
        verbose_name_plural = 'Background Check Providers'