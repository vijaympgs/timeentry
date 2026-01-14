"""
Application Capture Models for HRM
Following BBP 03.1 Application Capture specifications
Aligned with enterprise governance and Olivine UI canon
"""
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()

class JobApplication(models.Model):
    """
    Core job application model for capturing candidate information
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='jobapplication_company')
    job_posting = models.ForeignKey('hrm.JobPosting', on_delete=models.CASCADE, related_name='jobapplication_job_posting')
    candidate = models.ForeignKey('hrm.Candidate', on_delete=models.CASCADE, related_name='jobapplication_candidate')
    referral_employee = models.ForeignKey('hrm.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='jobapplication_referral_employee')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='jobapplication_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='jobapplication_updated_by')
    application_number = models.CharField(max_length=50)
    application_date = models.DateTimeField(auto_now_add=True)
    application_source = models.CharField(max_length=100, choices=[('career_site', 'Career Site'), ('job_board', 'Job Board'), ('social_media', 'Social Media'), ('referral', 'Employee Referral'), ('agency', 'Recruitment Agency'), ('campus', 'Campus Recruitment'), ('walk_in', 'Walk In'), ('internal', 'Internal Transfer'), ('other', 'Other')])
    source_details = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=50, choices=[('received', 'Received'), ('under_review', 'Under Review'), ('screening', 'Screening'), ('interview', 'Interview'), ('assessment', 'Assessment'), ('offer_extended', 'Offer Extended'), ('offer_accepted', 'Offer Accepted'), ('offer_declined', 'Offer Declined'), ('hired', 'Hired'), ('rejected', 'Rejected'), ('withdrawn', 'Withdrawn'), ('on_hold', 'On Hold')], default='received')
    priority = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('urgent', 'Urgent')], default='medium')
    screening_score = models.IntegerField(null=True, blank=True)
    screening_notes = models.TextField(blank=True)
    auto_screened = models.BooleanField(default=False)
    preferred_contact_method = models.CharField(max_length=50, choices=[('email', 'Email'), ('phone', 'Phone'), ('sms', 'SMS'), ('portal', 'Candidate Portal')], default='email')
    gender = models.CharField(max_length=20, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other'), ('prefer_not_to_say', 'Prefer not to say')], blank=True)
    ethnicity = models.CharField(max_length=100, blank=True)
    veteran_status = models.CharField(max_length=50, choices=[('no', 'No'), ('yes', 'Yes'), ('prefer_not_to_say', 'Prefer not to say')], blank=True)
    disability = models.CharField(max_length=50, choices=[('no', 'No'), ('yes', 'Yes'), ('prefer_not_to_say', 'Prefer not to say')], blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_job_applications'
        verbose_name = 'Job Application'
        verbose_name_plural = 'Job Applications'
        indexes = [models.Index(fields=['company', 'job_posting'], name='idx_app_job'), models.Index(fields=['company', 'candidate'], name='idx_app_candidate'), models.Index(fields=['company', 'status'], name='idx_app_status'), models.Index(fields=['company', 'application_date'], name='idx_app_date')]
        constraints = [models.UniqueConstraint(fields=['company', 'application_number'], name='uk_app_number')]
        ordering = ['-application_date']

    def __str__(self):
        return f'{self.application_number} - {self.candidate}'

    def clean(self):
        """Validate application data"""
        if self.application_date and self.application_date > timezone.now():
            raise ValidationError('Application date cannot be in the future')
        if self.screening_score is not None and (self.screening_score < 0 or self.screening_score > 100):
            raise ValidationError('Screening score must be between 0 and 100')

class ApplicationAnswer(models.Model):
    """
    Answers to application form questions
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='applicationanswer_company')
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='applicationanswer_application')
    question = models.ForeignKey('hrm.ApplicationQuestion', on_delete=models.CASCADE, related_name='applicationanswer_question')
    question_text = models.TextField()
    answer_text = models.TextField(blank=True)
    answer_type = models.CharField(max_length=50, choices=[('text', 'Text'), ('textarea', 'Textarea'), ('select', 'Select'), ('multiselect', 'Multi Select'), ('radio', 'Radio'), ('checkbox', 'Checkbox'), ('date', 'Date'), ('number', 'Number'), ('email', 'Email'), ('phone', 'Phone'), ('url', 'URL'), ('file', 'File')])
    answer_options = models.JSONField(default=dict, blank=True)
    is_required = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=True)
    validation_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_application_answers'
        verbose_name = 'Application Answer'
        verbose_name_plural = 'Application Answers'
        indexes = [models.Index(fields=['company', 'application'], name='idx_answer_app'), models.Index(fields=['company', 'question'], name='idx_answer_question')]
        unique_together = [['application', 'question']]

    def __str__(self):
        return f'Answer for {self.question.question_text[:50]}...'

    def clean(self):
        """Validate answer data"""
        if self.is_required and (not self.answer_text.strip()):
            raise ValidationError('This question is required and must be answered')

class ApplicationDocument(models.Model):
    """
    Documents attached to job applications
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='applicationdocument_company')
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='applicationdocument_application')
    document_type = models.CharField(max_length=100, choices=[('resume', 'Resume/CV'), ('cover_letter', 'Cover Letter'), ('transcript', 'Academic Transcript'), ('certificate', 'Certificate'), ('portfolio', 'Portfolio'), ('id_proof', 'ID Proof'), ('work_samples', 'Work Samples'), ('reference', 'Reference Letter'), ('other', 'Other')])
    document_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file_url = models.URLField()
    file_size = models.BigIntegerField()
    file_type = models.CharField(max_length=100)
    processing_status = models.CharField(max_length=50, choices=[('uploaded', 'Uploaded'), ('processing', 'Processing'), ('processed', 'Processed'), ('error', 'Error'), ('virus_scan', 'Virus Scan')], default='uploaded')
    upload_date = models.DateTimeField(auto_now_add=True)
    processed_date = models.DateTimeField(null=True, blank=True)
    virus_scan_result = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_application_documents'
        verbose_name = 'Application Document'
        verbose_name_plural = 'Application Documents'
        indexes = [models.Index(fields=['company', 'application'], name='idx_doc_app'), models.Index(fields=['company', 'document_type'], name='idx_app_doc_type_app')]
        ordering = ['-upload_date']

    def __str__(self):
        return f'{self.document_name} ({self.document_type})'

    def clean(self):
        """Validate document data"""
        max_size = 10 * 1024 * 1024
        if self.file_size > max_size:
            raise ValidationError('File size cannot exceed 10MB')
        allowed_types = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'image/jpeg', 'image/png', 'text/plain']
        if self.file_type not in allowed_types:
            raise ValidationError('File type not allowed')

class JobPosting(models.Model):
    """
    Job posting that applications are submitted for
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='jobposting_company')
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'hr_job_postings'
        verbose_name = 'Job Posting'
        verbose_name_plural = 'Job Postings'

class ApplicationCandidate(models.Model):
    """
    Candidate information for applications (avoiding conflict with main Candidate model)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='applicationcandidate_company')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'hr_application_candidates'
        verbose_name = 'Application Candidate'
        verbose_name_plural = 'Application Candidates'
        indexes = [models.Index(fields=['company', 'email'], name='idx_app_candidate_email')]
        constraints = [models.UniqueConstraint(fields=['company', 'email'], name='uk_app_candidate_email')]

    def clean(self):
        """Validate candidate data"""
        if self.email:
            try:
                validate_email(self.email)
            except ValidationError:
                raise ValidationError('Please enter a valid email address')

class ApplicationQuestion(models.Model):
    """
    Dynamic questions for application forms
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='applicationquestion_company')
    question_text = models.TextField()
    question_type = models.CharField(max_length=50, choices=[('text', 'Text'), ('textarea', 'Textarea'), ('select', 'Select'), ('multiselect', 'Multi Select'), ('radio', 'Radio'), ('checkbox', 'Checkbox'), ('date', 'Date'), ('number', 'Number'), ('email', 'Email'), ('phone', 'Phone'), ('url', 'URL'), ('file', 'File')])
    is_required = models.BooleanField(default=False)
    options = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'hr_application_questions'
        verbose_name = 'Application Question'
        verbose_name_plural = 'Application Questions'