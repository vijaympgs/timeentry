"""
Completion Tracking Models for HRM
Following BBP 07.3 Completion Tracking specifications
Aligned with enterprise governance and Olivine UI canon
"""

import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class LearningProgress(models.Model):
    """
    Main learning progress tracking model
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys - Using lazy string references per governance
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='learning_progress'
    )
    employee = models.ForeignKey(
        'hrm.Employee', 
        on_delete=models.CASCADE,
        related_name='learning_progress'
    )
    enrollment = models.ForeignKey(
        'hrm.Enrollment', 
        on_delete=models.CASCADE,
        related_name='learning_progress'
    )
    course = models.ForeignKey(
        'hrm.Course', 
        on_delete=models.CASCADE,
        related_name='learning_progress'
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='created_learning_progress'
    )
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='updated_learning_progress'
    )
    
    # Progress Details
    progress_number = models.CharField(max_length=50)
    
    # Status Management
    status = models.CharField(
        max_length=20, 
        choices=[
            ('not_started', 'Not Started'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
            ('expired', 'Expired'),
            ('suspended', 'Suspended'),
            ('withdrawn', 'Withdrawn'),
        ], 
        default='not_started'
    )
    
    # Progress Metrics
    overall_progress_percentage = models.IntegerField(default=0)
    completed_modules = models.IntegerField(default=0)
    total_modules = models.IntegerField(default=0)
    completed_lessons = models.IntegerField(default=0)
    total_lessons = models.IntegerField(default=0)
    
    # Time Tracking
    total_time_spent_minutes = models.IntegerField(default=0)
    current_session_time = models.IntegerField(default=0)
    average_session_time = models.IntegerField(default=0)
    last_access_date = models.DateTimeField(null=True, blank=True)
    
    # Completion Information
    start_date = models.DateTimeField(null=True, blank=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    estimated_completion_date = models.DateTimeField(null=True, blank=True)
    
    # Assessment Results
    assessment_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    assessment_status = models.CharField(
        max_length=20, 
        choices=[
            ('not_attempted', 'Not Attempted'),
            ('in_progress', 'In Progress'),
            ('passed', 'Passed'),
            ('failed', 'Failed'),
            ('exempted', 'Exempted'),
        ], 
        default='not_attempted'
    )
    attempts_count = models.IntegerField(default=0)
    max_attempts_allowed = models.IntegerField(default=3)
    
    # Performance Metrics
    engagement_score = models.IntegerField(default=0)
    participation_score = models.IntegerField(default=0)
    knowledge_gain_score = models.IntegerField(default=0)
    
    # Certification Information
    certificate_issued = models.BooleanField(default=False)
    certificate_number = models.CharField(max_length=100, blank=True)
    certificate_issue_date = models.DateTimeField(null=True, blank=True)
    certificate_expiry_date = models.DateTimeField(null=True, blank=True)
    
    # Compliance Information
    compliance_required = models.BooleanField(default=False)
    compliance_met = models.BooleanField(default=False)
    compliance_due_date = models.DateField(null=True, blank=True)
    
    # Notes and Feedback
    learner_notes = models.TextField(blank=True)
    instructor_feedback = models.TextField(blank=True)
    system_notes = models.TextField(blank=True)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_learning_progress'
        verbose_name = 'Learning Progress'
        verbose_name_plural = 'Learning Progress'
        indexes = [
            models.Index(fields=['company', 'employee'], name='idx_progress_employee'),
            models.Index(fields=['company', 'enrollment'], name='idx_progress_enrollment'),
            models.Index(fields=['company', 'course'], name='idx_progress_course'),
            models.Index(fields=['company', 'status'], name='idx_progress_status'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['company', 'progress_number'], name='uk_progress_number'),
        ]
        ordering = ['-last_access_date']
    
    def __str__(self):
        return f"Progress {self.progress_number} - {self.employee}"
    
    def clean(self):
        """Validate learning progress data"""
        # Validate progress percentage
        if self.overall_progress_percentage and (self.overall_progress_percentage < 0 or self.overall_progress_percentage > 100):
            raise ValidationError("Progress percentage must be between 0 and 100")
        
        # Validate completed modules
        if self.completed_modules and self.completed_modules < 0:
            raise ValidationError("Completed modules cannot be negative")
        
        # Validate total modules
        if self.total_modules and self.total_modules < 0:
            raise ValidationError("Total modules cannot be negative")
        
        # Validate completed lessons
        if self.completed_lessons and self.completed_lessons < 0:
            raise ValidationError("Completed lessons cannot be negative")
        
        # Validate total lessons
        if self.total_lessons and self.total_lessons < 0:
            raise ValidationError("Total lessons cannot be negative")
        
        # Validate time tracking
        time_fields = [
            'total_time_spent_minutes', 'current_session_time', 'average_session_time'
        ]
        
        for field in time_fields:
            value = getattr(self, field)
            if value is not None and value < 0:
                raise ValidationError(f"{field.replace('_', ' ').title()} cannot be negative")
        
        # Validate assessment score
        if self.assessment_score and (self.assessment_score < 0 or self.assessment_score > 100):
            raise ValidationError("Assessment score must be between 0 and 100")
        
        # Validate attempts count
        if self.attempts_count and self.attempts_count < 0:
            raise ValidationError("Attempts count cannot be negative")
        
        # Validate max attempts allowed
        if self.max_attempts_allowed and self.max_attempts_allowed < 1:
            raise ValidationError("Max attempts allowed must be at least 1")
        
        # Validate performance scores
        score_fields = ['engagement_score', 'participation_score', 'knowledge_gain_score']
        
        for field in score_fields:
            value = getattr(self, field)
            if value is not None and (value < 0 or value > 100):
                raise ValidationError(f"{field.replace('_', ' ').title()} must be between 0 and 100")
        
        # Validate completion date logic
        if self.start_date and self.completion_date:
            if self.start_date >= self.completion_date:
                raise ValidationError("Completion date must be after start date")
        
        # Validate last access date is not in future
        if self.last_access_date and self.last_access_date > timezone.now():
            raise ValidationError("Last access date cannot be in the future")
        
        # Validate certificate expiry date logic
        if self.certificate_issue_date and self.certificate_expiry_date:
            if self.certificate_issue_date >= self.certificate_expiry_date:
                raise ValidationError("Certificate expiry date must be after issue date")
        
        # Validate compliance due date logic
        if self.compliance_due_date and self.compliance_due_date < timezone.now().date():
            if not self.pk:  # New progress
                raise ValidationError("Compliance due date cannot be in the past for new progress")
    
    def save(self, *args, **kwargs):
        """Auto-calculate progress based on modules and lessons"""
        # Calculate overall progress based on modules if available
        if self.total_modules > 0:
            module_progress = (self.completed_modules / self.total_modules) * 100
            self.overall_progress_percentage = int(module_progress)
        elif self.total_lessons > 0:
            lesson_progress = (self.completed_lessons / self.total_lessons) * 100
            self.overall_progress_percentage = int(lesson_progress)
        
        # Auto-set completion date when status is completed
        if self.status == 'completed' and not self.completion_date:
            self.completion_date = timezone.now()
            self.overall_progress_percentage = 100
            self.compliance_met = True
        
        super().save(*args, **kwargs)


class ModuleProgress(models.Model):
    """
    Individual module progress tracking
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='module_progress'
    )
    learning_progress = models.ForeignKey(
        LearningProgress, 
        on_delete=models.CASCADE,
        related_name='module_progress'
    )
    employee = models.ForeignKey(
        'hrm.Employee', 
        on_delete=models.CASCADE,
        related_name='module_progress'
    )
    course = models.ForeignKey(
        'hrm.Course', 
        on_delete=models.CASCADE,
        related_name='module_progress'
    )
    
    # Module Details
    module_name = models.CharField(max_length=200)
    module_number = models.IntegerField()
    
    # Status Management
    status = models.CharField(
        max_length=20, 
        choices=[
            ('not_started', 'Not Started'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('skipped', 'Skipped'),
        ], 
        default='not_started'
    )
    
    # Progress Metrics
    progress_percentage = models.IntegerField(default=0)
    completed_lessons = models.IntegerField(default=0)
    total_lessons = models.IntegerField(default=0)
    
    # Time Tracking
    time_spent_minutes = models.IntegerField(default=0)
    start_date = models.DateTimeField(null=True, blank=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    
    # Assessment Results
    assessment_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    assessment_passed = models.BooleanField(default=False)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_module_progress'
        verbose_name = 'Module Progress'
        verbose_name_plural = 'Module Progress'
        indexes = [
            models.Index(fields=['company', 'learning_progress'], name='idx_module_progress'),
            models.Index(fields=['company', 'employee'], name='idx_module_employee'),
        ]
        ordering = ['module_number']
    
    def __str__(self):
        return f"Module {self.module_number} - {self.employee}"
    
    def clean(self):
        """Validate module progress data"""
        # Validate progress percentage
        if self.progress_percentage and (self.progress_percentage < 0 or self.progress_percentage > 100):
            raise ValidationError("Progress percentage must be between 0 and 100")
        
        # Validate completed lessons
        if self.completed_lessons and self.completed_lessons < 0:
            raise ValidationError("Completed lessons cannot be negative")
        
        # Validate total lessons
        if self.total_lessons and self.total_lessons < 0:
            raise ValidationError("Total lessons cannot be negative")
        
        # Validate time spent
        if self.time_spent_minutes and self.time_spent_minutes < 0:
            raise ValidationError("Time spent cannot be negative")
        
        # Validate assessment score
        if self.assessment_score and (self.assessment_score < 0 or self.assessment_score > 100):
            raise ValidationError("Assessment score must be between 0 and 100")
        
        # Validate module number is positive
        if self.module_number and self.module_number < 1:
            raise ValidationError("Module number must be positive")
        
        # Validate completion date logic
        if self.start_date and self.completion_date:
            if self.start_date >= self.completion_date:
                raise ValidationError("Completion date must be after start date")
    
    def save(self, *args, **kwargs):
        """Auto-calculate progress based on lessons"""
        if self.total_lessons > 0:
            self.progress_percentage = int((self.completed_lessons / self.total_lessons) * 100)
        
        # Auto-set completion date when status is completed
        if self.status == 'completed' and not self.completion_date:
            self.completion_date = timezone.now()
            self.progress_percentage = 100
        
        super().save(*args, **kwargs)


class Certificate(models.Model):
    """
    Certificate generation and management
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='certificates'
    )
    employee = models.ForeignKey(
        'hrm.Employee', 
        on_delete=models.CASCADE,
        related_name='certificates'
    )
    course = models.ForeignKey(
        'hrm.Course', 
        on_delete=models.CASCADE,
        related_name='certificates'
    )
    learning_progress = models.ForeignKey(
        LearningProgress, 
        on_delete=models.CASCADE,
        related_name='certificates'
    )
    issued_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='issued_certificates'
    )
    
    # Certificate Details
    certificate_number = models.CharField(max_length=100)
    certificate_title = models.CharField(max_length=200)
    certificate_description = models.TextField(blank=True)
    
    # Issuance Information
    issue_date = models.DateTimeField(auto_now_add=True)
    
    # Validity Information
    expiry_date = models.DateTimeField(null=True, blank=True)
    is_valid = models.BooleanField(default=True)
    is_revoked = models.BooleanField(default=False)
    revocation_date = models.DateTimeField(null=True, blank=True)
    revocation_reason = models.TextField(blank=True)
    
    # Certificate Content
    certificate_template_id = models.UUIDField(null=True, blank=True)
    certificate_content = models.JSONField(default=dict, blank=True)
    
    # Verification Information
    verification_code = models.CharField(max_length=100, unique=True)
    verification_url = models.URLField(blank=True)
    
    # Digital Signature
    digital_signature = models.TextField(blank=True)
    signature_date = models.DateTimeField(null=True, blank=True)
    
    # File Information
    certificate_file_url = models.URLField(blank=True)
    certificate_file_type = models.CharField(max_length=50, blank=True)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_certificates'
        verbose_name = 'Certificate'
        verbose_name_plural = 'Certificates'
        indexes = [
            models.Index(fields=['company', 'employee'], name='idx_certificate_employee'),
            models.Index(fields=['company', 'course'], name='idx_certificate_course'),
            models.Index(fields=['company', 'verification_code'], name='idx_certificate_verification'),
        ]
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"Certificate {self.certificate_number} - {self.employee}"
    
    def clean(self):
        """Validate certificate data"""
        # Validate expiry date logic
        if self.expiry_date and self.expiry_date <= timezone.now():
            raise ValidationError("Expiry date must be in the future")
        
        # Validate revocation date logic
        if self.revocation_date and self.revocation_date > timezone.now():
            raise ValidationError("Revocation date cannot be in the future")
        
        # Validate signature date logic
        if self.signature_date and self.signature_date > timezone.now():
            raise ValidationError("Signature date cannot be in the future")


# Reference Models (simplified versions - full implementations would be in separate files)

class AssessmentResult(models.Model):
    """
    Assessment and quiz results tracking
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='assessment_results'
    )
    learning_progress = models.ForeignKey(
        LearningProgress, 
        on_delete=models.CASCADE,
        related_name='assessment_results'
    )
    employee = models.ForeignKey(
        'hrm.Employee', 
        on_delete=models.CASCADE,
        related_name='assessment_results'
    )
    assessment_type = models.CharField(max_length=50)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2)
    passed = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'hr_assessment_results'
        verbose_name = 'Assessment Result'
        verbose_name_plural = 'Assessment Results'


class LearningActivity(models.Model):
    """
    Learning activity and engagement tracking
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='learning_activities'
    )
    learning_progress = models.ForeignKey(
        LearningProgress, 
        on_delete=models.CASCADE,
        related_name='learning_activities'
    )
    employee = models.ForeignKey(
        'hrm.Employee', 
        on_delete=models.CASCADE,
        related_name='learning_activities'
    )
    activity_type = models.CharField(max_length=50)
    activity_data = models.JSONField(default=dict)
    activity_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'hr_learning_activities'
        verbose_name = 'Learning Activity'
        verbose_name_plural = 'Learning Activities'
