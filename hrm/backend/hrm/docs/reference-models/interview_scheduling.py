"""
Interview Scheduling Models for HRM
Following BBP 03.3 Interview Scheduling specifications
Aligned with enterprise governance and Olivine UI canon
"""

import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class InterviewSchedule(models.Model):
    """
    Main interview scheduling model for managing interview appointments
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys - Using lazy string references per governance
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='interview_schedules'
    )
    application = models.ForeignKey(
        'hrm.JobApplication', 
        on_delete=models.CASCADE,
        related_name='interview_schedules'
    )
    job_posting = models.ForeignKey(
        'hrm.JobPosting', 
        on_delete=models.CASCADE,
        related_name='interview_schedules'
    )
    candidate = models.ForeignKey(
        'hrm.Candidate', 
        on_delete=models.CASCADE,
        related_name='interview_schedules'
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='created_interview_schedules'
    )
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='updated_interview_schedules'
    )
    
    # Interview Details
    interview_number = models.CharField(max_length=50)
    interview_title = models.CharField(max_length=200)
    interview_type = models.CharField(
        max_length=50, 
        choices=[
            ('phone_screen', 'Phone Screen'),
            ('video_interview', 'Video Interview'),
            ('technical', 'Technical Interview'),
            ('behavioral', 'Behavioral Interview'),
            ('panel', 'Panel Interview'),
            ('final', 'Final Interview'),
            ('cultural_fit', 'Cultural Fit Interview'),
            ('case_study', 'Case Study Interview'),
            ('presentation', 'Presentation Interview'),
            ('onsite', 'On-site Interview'),
        ]
    )
    
    # Scheduling Information
    scheduled_date = models.DateTimeField()
    duration_minutes = models.IntegerField(default=60)
    timezone = models.CharField(max_length=50, default='UTC')
    
    # Location and Virtual Meeting
    interview_location = models.CharField(max_length=200, blank=True)
    meeting_room = models.CharField(max_length=100, blank=True)
    meeting_url = models.URLField(blank=True)
    meeting_id = models.CharField(max_length=100, blank=True)
    meeting_password = models.CharField(max_length=100, blank=True)
    conference_type = models.CharField(
        max_length=50, 
        choices=[
            ('in_person', 'In Person'),
            ('video', 'Video Conference'),
            ('phone', 'Phone Call'),
            ('hybrid', 'Hybrid'),
        ], 
        default='in_person'
    )
    
    # Status Management
    status = models.CharField(
        max_length=50, 
        choices=[
            ('scheduled', 'Scheduled'),
            ('confirmed', 'Confirmed'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
            ('rescheduled', 'Rescheduled'),
            ('no_show', 'No Show'),
            ('postponed', 'Postponed'),
        ], 
        default='scheduled'
    )
    
    # Priority and Urgency
    priority = models.CharField(
        max_length=20, 
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('urgent', 'Urgent'),
        ], 
        default='medium'
    )
    
    # Communication Settings
    send_invitation = models.BooleanField(default=True)
    send_reminders = models.BooleanField(default=True)
    reminder_timing = models.IntegerField(default=24)  # hours before
    invitation_sent = models.BooleanField(default=False)
    invitation_sent_date = models.DateTimeField(null=True, blank=True)
    
    # Rescheduling Information
    reschedule_count = models.IntegerField(default=0)
    reschedule_reason = models.TextField(blank=True)
    original_scheduled_date = models.DateTimeField(null=True, blank=True)
    
    # Interview Details
    interview_description = models.TextField(blank=True)
    interview_format = models.CharField(max_length=200, blank=True)
    special_instructions = models.TextField(blank=True)
    required_materials = models.TextField(blank=True)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_interview_schedules'
        verbose_name = 'Interview Schedule'
        verbose_name_plural = 'Interview Schedules'
        indexes = [
            models.Index(fields=['company', 'application'], name='idx_interview_app'),
            models.Index(fields=['company', 'candidate'], name='idx_interview_candidate'),
            models.Index(fields=['company', 'status'], name='idx_interview_status'),
            models.Index(fields=['company', 'scheduled_date'], name='idx_interview_date'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['company', 'interview_number'], name='uk_interview_number'),
        ]
        ordering = ['-scheduled_date']
    
    def __str__(self):
        return f"Interview {self.interview_number} - {self.candidate}"
    
    def clean(self):
        """Validate interview schedule data"""
        # Validate interview date is not in past for new interviews
        if self.scheduled_date and self.scheduled_date < timezone.now():
            if not self.pk:  # New interview
                raise ValidationError("Interview date cannot be in the past")
        
        # Validate duration is reasonable
        if self.duration_minutes and (self.duration_minutes < 15 or self.duration_minutes > 480):
            raise ValidationError("Interview duration must be between 15 minutes and 8 hours")
        
        # Validate reminder timing
        if self.reminder_timing and self.reminder_timing < 1:
            raise ValidationError("Reminder timing must be at least 1 hour before interview")
        
        # Validate reschedule count
        if self.reschedule_count and self.reschedule_count < 0:
            raise ValidationError("Reschedule count cannot be negative")
        
        # Validate meeting URL format
        if self.meeting_url and not (self.meeting_url.startswith('http://') or self.meeting_url.startswith('https://')):
            raise ValidationError("Meeting URL must start with http:// or https://")


class InterviewPanel(models.Model):
    """
    Interview panel members and their roles
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='interview_panels'
    )
    interview_schedule = models.ForeignKey(
        InterviewSchedule, 
        on_delete=models.CASCADE,
        related_name='interview_panels'
    )
    panel_member = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='interview_panel_assignments'
    )
    
    # Panel Member Information
    panel_member_name = models.CharField(max_length=200)
    panel_member_email = models.EmailField()
    panel_member_role = models.CharField(
        max_length=100, 
        choices=[
            ('lead_interviewer', 'Lead Interviewer'),
            ('technical_interviewer', 'Technical Interviewer'),
            ('hr_interviewer', 'HR Interviewer'),
            ('hiring_manager', 'Hiring Manager'),
            ('panel_member', 'Panel Member'),
            ('observer', 'Observer'),
            ('subject_matter_expert', 'Subject Matter Expert'),
        ]
    )
    
    # Participation Details
    is_required = models.BooleanField(default=True)
    is_external = models.BooleanField(default=False)
    organization = models.CharField(max_length=200, blank=True)
    
    # Availability and Confirmation
    availability_confirmed = models.BooleanField(default=False)
    confirmation_date = models.DateTimeField(null=True, blank=True)
    declined_reason = models.TextField(blank=True)
    
    # Feedback Responsibility
    required_feedback = models.BooleanField(default=True)
    feedback_submitted = models.BooleanField(default=False)
    feedback_due_date = models.DateTimeField(null=True, blank=True)
    
    # Scoring Authority
    can_score = models.BooleanField(default=True)
    scoring_weight = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_interview_panels'
        verbose_name = 'Interview Panel'
        verbose_name_plural = 'Interview Panels'
        indexes = [
            models.Index(fields=['company', 'interview_schedule'], name='idx_panel_interview'),
            models.Index(fields=['company', 'panel_member'], name='idx_panel_member'),
        ]
        ordering = ['panel_member_role']
    
    def __str__(self):
        return f"Panel: {self.panel_member_name} - {self.interview_schedule}"
    
    def clean(self):
        """Validate interview panel data"""
        # Validate scoring weight is positive
        if self.scoring_weight and self.scoring_weight <= 0:
            raise ValidationError("Scoring weight must be positive")
        
        # Validate confirmation date logic
        if self.confirmation_date and self.confirmation_date > timezone.now():
            raise ValidationError("Confirmation date cannot be in the future")
        
        # Validate feedback due date logic
        if self.feedback_due_date and self.feedback_due_date < timezone.now():
            raise ValidationError("Feedback due date cannot be in the past")
        
        # Validate email format
        if self.panel_member_email and '@' not in self.panel_member_email:
            raise ValidationError("Panel member email format is invalid")


class InterviewFeedback(models.Model):
    """
    Interview feedback and evaluation data
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='interview_feedback'
    )
    interview_schedule = models.ForeignKey(
        InterviewSchedule, 
        on_delete=models.CASCADE,
        related_name='interview_feedback'
    )
    panel_member = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='interview_feedback_submissions'
    )
    
    # Overall Assessment
    overall_rating = models.IntegerField(
        choices=[
            (1, 'Strongly Not Recommended'),
            (2, 'Not Recommended'),
            (3, 'Neutral'),
            (4, 'Recommended'),
            (5, 'Strongly Recommended'),
        ], 
        null=True, 
        blank=True
    )
    recommendation = models.CharField(
        max_length=50, 
        choices=[
            ('reject', 'Reject'),
            ('hold', 'Hold'),
            ('next_round', 'Next Round'),
            ('hire', 'Hire'),
            ('strong_hire', 'Strong Hire'),
        ], 
        blank=True
    )
    
    # Skills Assessment
    technical_skills = models.IntegerField(null=True, blank=True)
    communication_skills = models.IntegerField(null=True, blank=True)
    problem_solving = models.IntegerField(null=True, blank=True)
    cultural_fit = models.IntegerField(null=True, blank=True)
    leadership_potential = models.IntegerField(null=True, blank=True)
    
    # Detailed Feedback
    strengths = models.TextField(blank=True)
    weaknesses = models.TextField(blank=True)
    additional_notes = models.TextField(blank=True)
    key_observations = models.TextField(blank=True)
    
    # Question Responses
    question_responses = models.JSONField(default=list, blank=True)
    
    # Submission Details
    feedback_date = models.DateTimeField(auto_now_add=True)
    is_draft = models.BooleanField(default=True)
    submitted_date = models.DateTimeField(null=True, blank=True)
    
    # Follow-up Actions
    follow_up_required = models.BooleanField(default=False)
    follow_up_notes = models.TextField(blank=True)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_interview_feedback'
        verbose_name = 'Interview Feedback'
        verbose_name_plural = 'Interview Feedback'
        indexes = [
            models.Index(fields=['company', 'interview_schedule'], name='idx_feedback_interview'),
            models.Index(fields=['company', 'panel_member'], name='idx_feedback_panelist'),
        ]
        ordering = ['-feedback_date']
    
    def __str__(self):
        return f"Feedback - {self.panel_member} - {self.interview_schedule}"
    
    def clean(self):
        """Validate interview feedback data"""
        # Validate rating is within range
        if self.overall_rating and (self.overall_rating < 1 or self.overall_rating > 5):
            raise ValidationError("Overall rating must be between 1 and 5")
        
        # Validate skill ratings are within range
        skill_fields = [
            'technical_skills', 'communication_skills', 'problem_solving',
            'cultural_fit', 'leadership_potential'
        ]
        
        for field in skill_fields:
            value = getattr(self, field)
            if value is not None and (value < 1 or value > 5):
                raise ValidationError(f"{field.replace('_', ' ').title()} must be between 1 and 5")
        
        # Validate submission date logic
        if self.submitted_date and self.submitted_date < timezone.now():
            raise ValidationError("Submitted date cannot be in the past")
        
        # Validate question responses format
        if self.question_responses and not isinstance(self.question_responses, list):
            raise ValidationError("Question responses must be a list")


# Reference Models (simplified versions - full implementations would be in separate files)

class InterviewTemplate(models.Model):
    """
    Reusable interview templates for different job types
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='interview_templates'
    )
    template_name = models.CharField(max_length=200)
    job_category = models.CharField(max_length=100)
    interview_type = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    duration_minutes = models.IntegerField(default=60)
    questions = models.JSONField(default=list)
    evaluation_criteria = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'hr_interview_templates'
        verbose_name = 'Interview Template'
        verbose_name_plural = 'Interview Templates'


class InterviewRoom(models.Model):
    """
    Interview rooms and resources management
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='interview_rooms'
    )
    room_name = models.CharField(max_length=200)
    room_location = models.CharField(max_length=200)
    capacity = models.IntegerField(default=1)
    equipment = models.JSONField(default=list)
    is_available = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'hr_interview_rooms'
        verbose_name = 'Interview Room'
        verbose_name_plural = 'Interview Rooms'

# Alias for backward compatibility with import expectations
InterviewScheduling = InterviewSchedule
