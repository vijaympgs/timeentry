"""
Pulse Surveys Models for HRM
Following BBP 08.1 Pulse Surveys specifications
Aligned with enterprise governance and Olivine UI canon
"""

import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class PulseSurvey(models.Model):
    """
    Main pulse survey model for employee feedback collection
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys - Using lazy string references per governance
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='pulse_surveys'
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='created_pulse_surveys'
    )
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='updated_pulse_surveys'
    )
    
    # Survey Details
    survey_name = models.CharField(max_length=200)
    survey_code = models.CharField(max_length=50)
    survey_description = models.TextField(blank=True)
    
    # Survey Configuration
    survey_type = models.CharField(
        max_length=50, 
        choices=[
            ('engagement', 'Engagement Survey'),
            ('satisfaction', 'Satisfaction Survey'),
            ('wellness', 'Wellness Check'),
            ('feedback', 'Feedback Survey'),
            ('recognition', 'Recognition Survey'),
            ('onboarding', 'Onboarding Survey'),
            ('exit_intent', 'Exit Intent Survey'),
            ('custom', 'Custom Survey'),
        ]
    )
    
    # Anonymity Settings
    is_anonymous = models.BooleanField(default=True)
    allow_identified_responses = models.BooleanField(default=False)
    anonymity_level = models.CharField(
        max_length=20, 
        choices=[
            ('fully_anonymous', 'Fully Anonymous'),
            ('hr_visible', 'HR Only'),
            ('manager_visible', 'Manager Visible'),
            ('identified', 'Identified'),
        ], 
        default='fully_anonymous'
    )
    
    # Status Management
    status = models.CharField(
        max_length=20, 
        choices=[
            ('draft', 'Draft'),
            ('scheduled', 'Scheduled'),
            ('active', 'Active'),
            ('paused', 'Paused'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ], 
        default='draft'
    )
    
    # Scheduling
    launch_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_recurring = models.BooleanField(default=False)
    recurring_frequency = models.CharField(
        max_length=50, 
        choices=[
            ('weekly', 'Weekly'),
            ('bi_weekly', 'Bi-Weekly'),
            ('monthly', 'Monthly'),
            ('quarterly', 'Quarterly'),
            ('custom', 'Custom'),
        ], 
        blank=True
    )
    
    # Target Audience
    target_all_employees = models.BooleanField(default=True)
    target_departments = models.JSONField(default=list, blank=True)
    target_teams = models.JSONField(default=list, blank=True)
    target_employees = models.JSONField(default=list, blank=True)
    exclude_employees = models.JSONField(default=list, blank=True)
    
    # Survey Settings
    estimated_completion_time = models.IntegerField(default=5)  # in minutes
    allow_partial_save = models.BooleanField(default=True)
    require_all_questions = models.BooleanField(default=False)
    show_progress_bar = models.BooleanField(default=True)
    
    # Response Management
    max_responses_per_employee = models.IntegerField(default=1)
    allow_edit_after_submit = models.BooleanField(default=False)
    
    # Notifications
    send_launch_notification = models.BooleanField(default=True)
    send_reminder_notifications = models.BooleanField(default=True)
    reminder_frequency_days = models.IntegerField(default=3)
    max_reminders = models.IntegerField(default=3)
    
    # Results and Analytics
    publish_results_to_employees = models.BooleanField(default=False)
    publish_results_to_managers = models.BooleanField(default=True)
    auto_generate_report = models.BooleanField(default=True)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_pulse_surveys'
        verbose_name = 'Pulse Survey'
        verbose_name_plural = 'Pulse Surveys'
        indexes = [
            models.Index(fields=['company', 'status'], name='idx_survey_status'),
            models.Index(fields=['company', 'survey_type'], name='idx_survey_type'),
            models.Index(fields=['company', 'launch_date'], name='idx_survey_launch_date'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['company', 'survey_code'], name='uk_survey_code'),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Survey {self.survey_name} - {self.company}"
    
    def clean(self):
        """Validate pulse survey data"""
        # Validate survey dates
        if self.launch_date and self.end_date:
            if self.launch_date >= self.end_date:
                raise ValidationError("End date must be after launch date")
        
        # Validate anonymity settings
        if self.is_anonymous and self.publish_results_to_employees:
            if self.anonymity_level == 'fully_anonymous':
                raise ValidationError("Cannot publish results for fully anonymous surveys")
        
        # Validate response limits
        if self.max_responses_per_employee and self.max_responses_per_employee < 1:
            raise ValidationError("Maximum responses per employee must be at least 1")
        
        # Validate completion time
        if self.estimated_completion_time and (self.estimated_completion_time < 1 or self.estimated_completion_time > 120):
            raise ValidationError("Estimated completion time must be between 1 and 120 minutes")
        
        # Validate reminder settings
        if self.reminder_frequency_days and self.reminder_frequency_days < 1:
            raise ValidationError("Reminder frequency must be at least 1 day")
        
        if self.max_reminders and self.max_reminders < 0:
            raise ValidationError("Maximum reminders cannot be negative")


class SurveyQuestion(models.Model):
    """
    Individual survey questions and response options
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='survey_questions'
    )
    survey = models.ForeignKey(
        PulseSurvey, 
        on_delete=models.CASCADE,
        related_name='survey_questions'
    )
    depends_on_question = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='dependent_questions'
    )
    
    # Question Details
    question_text = models.TextField()
    question_code = models.CharField(max_length=100, blank=True)
    question_type = models.CharField(
        max_length=50, 
        choices=[
            ('likert', 'Likert Scale'),
            ('multiple_choice', 'Multiple Choice'),
            ('single_choice', 'Single Choice'),
            ('open_text', 'Open Text'),
            ('rating', 'Rating Scale'),
            ('yes_no', 'Yes/No'),
            ('nps', 'Net Promoter Score'),
            ('csat', 'Customer Satisfaction'),
            ('emoji', 'Emoji Rating'),
            ('matrix', 'Matrix Grid'),
        ]
    )
    
    # Question Configuration
    is_required = models.BooleanField(default=True)
    is_randomizable = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    
    # Response Options
    response_options = models.JSONField(default=list, blank=True)
    scale_min = models.IntegerField(null=True, blank=True)
    scale_max = models.IntegerField(null=True, blank=True)
    scale_labels = models.JSONField(default=dict, blank=True)
    
    # Question Categories
    category = models.CharField(
        max_length=100, 
        choices=[
            ('engagement', 'Engagement'),
            ('satisfaction', 'Satisfaction'),
            ('wellness', 'Wellness'),
            ('leadership', 'Leadership'),
            ('communication', 'Communication'),
            ('recognition', 'Recognition'),
            ('development', 'Development'),
            ('work_life_balance', 'Work-Life Balance'),
            ('compensation', 'Compensation'),
            ('culture', 'Culture'),
            ('other', 'Other'),
        ]
    )
    
    # Analytics Configuration
    include_in_engagement_score = models.BooleanField(default=True)
    weight_in_score = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    
    # Conditional Logic
    conditional_logic = models.JSONField(default=dict, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_survey_questions'
        verbose_name = 'Survey Question'
        verbose_name_plural = 'Survey Questions'
        indexes = [
            models.Index(fields=['company', 'survey'], name='idx_question_survey'),
            models.Index(fields=['company', 'question_type'], name='idx_question_type'),
        ]
        ordering = ['display_order']
    
    def __str__(self):
        return f"Question: {self.question_text[:50]}..."
    
    def clean(self):
        """Validate survey question data"""
        # Validate display order is non-negative
        if self.display_order and self.display_order < 0:
            raise ValidationError("Display order cannot be negative")
        
        # Validate scale configuration
        if self.scale_min and self.scale_max:
            if self.scale_min >= self.scale_max:
                raise ValidationError("Scale minimum must be less than maximum")
        
        # Validate weight is positive
        if self.weight_in_score and self.weight_in_score <= 0:
            raise ValidationError("Weight in score must be positive")
        
        # Validate question text is not empty
        if not self.question_text or not self.question_text.strip():
            raise ValidationError("Question text cannot be empty")


class SurveyResponse(models.Model):
    """
    Individual survey responses and answers
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='survey_responses'
    )
    survey = models.ForeignKey(
        PulseSurvey, 
        on_delete=models.CASCADE,
        related_name='survey_responses'
    )
    employee = models.ForeignKey(
        'hrm.Employee', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='survey_responses'
    )
    
    # Response Details
    response_number = models.CharField(max_length=50)
    
    # Response Information
    start_date = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    completion_percentage = models.IntegerField(default=0)
    
    # Device and Location
    device_type = models.CharField(max_length=50, blank=True)
    browser_info = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    # Answers
    answers = models.JSONField(default=dict, blank=True)
    
    # Engagement Metrics
    time_spent_seconds = models.IntegerField(default=0)
    page_views = models.IntegerField(default=0)
    
    # Sentiment Analysis
    sentiment_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    sentiment_label = models.CharField(max_length=20, blank=True)
    
    # Status
    status = models.CharField(
        max_length=20, 
        choices=[
            ('started', 'Started'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('abandoned', 'Abandoned'),
            ('expired', 'Expired'),
        ], 
        default='started'
    )
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_survey_responses'
        verbose_name = 'Survey Response'
        verbose_name_plural = 'Survey Responses'
        indexes = [
            models.Index(fields=['company', 'survey'], name='idx_response_survey'),
            models.Index(fields=['company', 'employee'], name='idx_response_employee'),
            models.Index(fields=['company', 'status'], name='idx_response_status'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['company', 'response_number'], name='uk_response_number'),
        ]
        ordering = ['-start_date']
    
    def __str__(self):
        return f"Response {self.response_number} - {self.survey}"
    
    def clean(self):
        """Validate survey response data"""
        # Validate completion percentage
        if self.completion_percentage and (self.completion_percentage < 0 or self.completion_percentage > 100):
            raise ValidationError("Completion percentage must be between 0 and 100")
        
        # Validate time spent is non-negative
        if self.time_spent_seconds and self.time_spent_seconds < 0:
            raise ValidationError("Time spent cannot be negative")
        
        # Validate page views is non-negative
        if self.page_views and self.page_views < 0:
            raise ValidationError("Page views cannot be negative")
        
        # Validate sentiment score
        if self.sentiment_score and (self.sentiment_score < -1 or self.sentiment_score > 1):
            raise ValidationError("Sentiment score must be between -1 and 1")
        
        # Validate completion date logic
        if self.completion_date and self.start_date:
            if self.completion_date < self.start_date:
                raise ValidationError("Completion date cannot be before start date")
    
    def save(self, *args, **kwargs):
        """Auto-calculate completion percentage based on status"""
        if self.status == 'completed' and not self.completion_date:
            self.completion_date = timezone.now()
            self.completion_percentage = 100
        
        super().save(*args, **kwargs)


# Reference Models (simplified versions - full implementations would be in separate files)

class SurveyTemplate(models.Model):
    """
    Survey templates for quick survey creation
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='survey_templates'
    )
    template_name = models.CharField(max_length=200)
    template_code = models.CharField(max_length=50)
    template_description = models.TextField(blank=True)
    template_category = models.CharField(max_length=100)
    template_data = models.JSONField(default=dict)
    is_public = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'hr_survey_templates'
        verbose_name = 'Survey Template'
        verbose_name_plural = 'Survey Templates'


class SurveyAnalytics(models.Model):
    """
    Survey analytics and aggregated results
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='survey_analytics'
    )
    survey = models.ForeignKey(
        PulseSurvey, 
        on_delete=models.CASCADE,
        related_name='survey_analytics'
    )
    analytics_data = models.JSONField(default=dict)
    engagement_score = models.DecimalField(max_digits=5, decimal_places=2)
    response_rate = models.DecimalField(max_digits=5, decimal_places=2)
    
    class Meta:
        db_table = 'hr_survey_analytics'
        verbose_name = 'Survey Analytics'
        verbose_name_plural = 'Survey Analytics'
