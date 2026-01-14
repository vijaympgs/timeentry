"""
Review Cycle Models for HRM
Following BBP 06.2 Review Cycle specifications
Aligned with enterprise governance and Olivine UI canon
"""

import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class PerformanceReviewCycle(models.Model):
    """
    Performance review cycle management
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys - Using lazy string references per governance
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='review_cycles'
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='created_review_cycles'
    )
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='updated_review_cycles'
    )
    
    # Cycle Details
    cycle_name = models.CharField(max_length=200)
    cycle_code = models.CharField(max_length=50)
    cycle_type = models.CharField(
        max_length=50, 
        choices=[
            ('annual', 'Annual Review'),
            ('semi_annual', 'Semi-Annual Review'),
            ('quarterly', 'Quarterly Review'),
            ('monthly', 'Monthly Review'),
            ('project', 'Project-Based Review'),
            ('probation', 'Probation Review'),
            ('promotion', 'Promotion Review'),
            ('custom', 'Custom Review'),
        ]
    )
    
    # Timeline Management
    start_date = models.DateField()
    end_date = models.DateField()
    self_assessment_start = models.DateField()
    self_assessment_end = models.DateField()
    manager_review_start = models.DateField()
    manager_review_end = models.DateField()
    
    # Status Management
    status = models.CharField(
        max_length=20, 
        choices=[
            ('draft', 'Draft'),
            ('planned', 'Planned'),
            ('active', 'Active'),
            ('self_assessment', 'Self Assessment'),
            ('manager_review', 'Manager Review'),
            ('calibration', 'Calibration'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ], 
        default='draft'
    )
    
    # Configuration
    include_self_assessment = models.BooleanField(default=True)
    include_manager_review = models.BooleanField(default=True)
    include_peer_review = models.BooleanField(default=False)
    include_360_feedback = models.BooleanField(default=False)
    include_goal_evaluation = models.BooleanField(default=True)
    include_competency_assessment = models.BooleanField(default=True)
    
    # Review Settings
    require_goal_completion = models.BooleanField(default=True)
    require_manager_approval = models.BooleanField(default=True)
    allow_employee_comments = models.BooleanField(default=True)
    allow_manager_editing = models.BooleanField(default=True)
    
    # Scope and Applicability
    applies_to_all = models.BooleanField(default=True)
    applies_to_departments = models.JSONField(default=list, blank=True)
    applies_to_employees = models.JSONField(default=list, blank=True)
    applies_to_employee_types = models.JSONField(default=list, blank=True)
    excludes_employees = models.JSONField(default=list, blank=True)
    
    # Notifications
    enable_notifications = models.BooleanField(default=True)
    notification_schedule = models.JSONField(default=dict, blank=True)
    reminder_enabled = models.BooleanField(default=True)
    reminder_frequency_days = models.IntegerField(default=7)
    
    # Description and Guidelines
    description = models.TextField(blank=True)
    employee_instructions = models.TextField(blank=True)
    manager_instructions = models.TextField(blank=True)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_review_cycles'
        verbose_name = 'Review Cycle'
        verbose_name_plural = 'Review Cycles'
        indexes = [
            models.Index(fields=['company', 'status'], name='idx_cycle_status'),
            models.Index(fields=['company', 'cycle_type'], name='idx_cycle_type'),
            models.Index(fields=['company', 'start_date'], name='idx_cycle_start_date'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['company', 'cycle_code'], name='uk_cycle_code'),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review Cycle {self.cycle_name} - {self.company}"
    
    def clean(self):
        """Validate review cycle data"""
        # Validate cycle dates
        if self.start_date >= self.end_date:
            raise ValidationError("End date must be after start date")
        
        # Validate assessment dates within cycle
        if self.self_assessment_start < self.start_date:
            raise ValidationError("Self assessment start must be after cycle start")
        
        if self.self_assessment_end < self.self_assessment_start:
            raise ValidationError("Self assessment end must be after start")
        
        if self.manager_review_start < self.start_date:
            raise ValidationError("Manager review start must be after cycle start")
        
        if self.manager_review_end < self.manager_review_start:
            raise ValidationError("Manager review end must be after start")
        
        # Validate dates are within cycle period
        if self.self_assessment_end > self.end_date:
            raise ValidationError("Self assessment end must be before cycle end")
        
        if self.manager_review_end > self.end_date:
            raise ValidationError("Manager review end must be before cycle end")
        
        # Validate reminder frequency
        if self.reminder_frequency_days and self.reminder_frequency_days < 1:
            raise ValidationError("Reminder frequency must be at least 1 day")


class PerformanceReview(models.Model):
    """
    Individual performance review records
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='performance_reviews'
    )
    review_cycle = models.ForeignKey(
        PerformanceReviewCycle, 
        on_delete=models.CASCADE,
        related_name='performance_reviews'
    )
    employee = models.ForeignKey(
        'hrm.Employee', 
        on_delete=models.CASCADE,
        related_name='performance_reviews'
    )
    manager = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='conducted_reviews'
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='created_performance_reviews'
    )
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='updated_performance_reviews'
    )
    
    # Review Details
    review_number = models.CharField(max_length=50)
    review_period_start = models.DateField()
    review_period_end = models.DateField()
    
    # Status Management
    status = models.CharField(
        max_length=20, 
        choices=[
            ('not_started', 'Not Started'),
            ('self_assessment', 'Self Assessment'),
            ('manager_review', 'Manager Review'),
            ('peer_review', 'Peer Review'),
            ('calibration', 'Calibration'),
            ('completed', 'Completed'),
            ('on_hold', 'On Hold'),
            ('cancelled', 'Cancelled'),
        ], 
        default='not_started'
    )
    
    # Progress Tracking
    self_assessment_completed = models.BooleanField(default=False)
    self_assessment_date = models.DateTimeField(null=True, blank=True)
    manager_review_completed = models.BooleanField(default=False)
    manager_review_date = models.DateTimeField(null=True, blank=True)
    peer_reviews_completed = models.IntegerField(default=0)
    total_peer_reviews = models.IntegerField(default=0)
    
    # Overall Rating
    overall_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    performance_level = models.CharField(max_length=50, blank=True)
    
    # Goal Evaluation Summary
    goals_count = models.IntegerField(default=0)
    goals_achieved = models.IntegerField(default=0)
    goals_partially_achieved = models.IntegerField(default=0)
    goals_not_achieved = models.IntegerField(default=0)
    goal_achievement_percentage = models.IntegerField(default=0)
    
    # Competency Summary
    competencies_count = models.IntegerField(default=0)
    competencies_above_expectations = models.IntegerField(default=0)
    competencies_meets_expectations = models.IntegerField(default=0)
    competencies_below_expectations = models.IntegerField(default=0)
    
    # Development and Feedback
    development_needs = models.JSONField(default=list, blank=True)
    strengths = models.JSONField(default=list, blank=True)
    areas_for_improvement = models.JSONField(default=list, blank=True)
    career_aspirations = models.TextField(blank=True)
    
    # Manager Comments
    manager_summary = models.TextField(blank=True)
    manager_feedback = models.TextField(blank=True)
    manager_recommendations = models.TextField(blank=True)
    
    # Employee Comments
    employee_comments = models.TextField(blank=True)
    employee_feedback = models.TextField(blank=True)
    employee_response = models.TextField(blank=True)
    
    # Sign-off Information
    employee_signoff = models.BooleanField(default=False)
    employee_signoff_date = models.DateTimeField(null=True, blank=True)
    manager_signoff = models.BooleanField(default=False)
    manager_signoff_date = models.DateTimeField(null=True, blank=True)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_performance_reviews'
        verbose_name = 'Performance Review'
        verbose_name_plural = 'Performance Reviews'
        indexes = [
            models.Index(fields=['company', 'review_cycle'], name='idx_review_cycle'),
            models.Index(fields=['company', 'employee'], name='idx_review_employee'),
            models.Index(fields=['company', 'manager'], name='idx_review_manager'),
            models.Index(fields=['company', 'status'], name='idx_review_status'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['company', 'review_number'], name='uk_review_number'),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review {self.review_number} - {self.employee}"
    
    def clean(self):
        """Validate performance review data"""
        # Validate review period dates
        if self.review_period_start >= self.review_period_end:
            raise ValidationError("Review period end must be after start")
        
        # Validate overall rating
        if self.overall_rating and (self.overall_rating < 1 or self.overall_rating > 5):
            raise ValidationError("Overall rating must be between 1 and 5")
        
        # Validate goal achievement percentage
        if self.goal_achievement_percentage and (self.goal_achievement_percentage < 0 or self.goal_achievement_percentage > 100):
            raise ValidationError("Goal achievement percentage must be between 0 and 100")
        
        # Validate peer review counts
        if self.peer_reviews_completed and self.total_peer_reviews:
            if self.peer_reviews_completed > self.total_peer_reviews:
                raise ValidationError("Completed peer reviews cannot exceed total peer reviews")
        
        if self.total_peer_reviews and self.total_peer_reviews < 0:
            raise ValidationError("Total peer reviews cannot be negative")
        
        # Validate competency counts are non-negative
        competency_fields = [
            'competencies_count', 'competencies_above_expectations',
            'competencies_meets_expectations', 'competencies_below_expectations'
        ]
        
        for field in competency_fields:
            value = getattr(self, field)
            if value and value < 0:
                raise ValidationError(f"{field.replace('_', ' ').title()} cannot be negative")
        
        # Validate sign-off dates logic
        if self.employee_signoff_date and self.employee_signoff_date > timezone.now():
            raise ValidationError("Employee signoff date cannot be in the future")
        
        if self.manager_signoff_date and self.manager_signoff_date > timezone.now():
            raise ValidationError("Manager signoff date cannot be in the future")
    
    def save(self, *args, **kwargs):
        """Auto-calculate goal achievement percentage"""
        if self.goals_count > 0:
            achieved_weight = self.goals_achieved * 100
            partial_weight = self.goals_partially_achieved * 50
            self.goal_achievement_percentage = int((achieved_weight + partial_weight) / self.goals_count)
        
        super().save(*args, **kwargs)


class ReviewForm(models.Model):
    """
    Review form templates and configurations
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='review_forms'
    )
    review_cycle = models.ForeignKey(
        PerformanceReviewCycle, 
        on_delete=models.CASCADE,
        null=True, 
        blank=True,
        related_name='review_forms'
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='created_review_forms'
    )
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='updated_review_forms'
    )
    
    # Form Details
    form_name = models.CharField(max_length=200)
    form_code = models.CharField(max_length=50)
    form_type = models.CharField(
        max_length=50, 
        choices=[
            ('self_assessment', 'Self Assessment'),
            ('manager_review', 'Manager Review'),
            ('peer_review', 'Peer Review'),
            ('360_feedback', '360 Degree Feedback'),
            ('calibration', 'Calibration Form'),
        ]
    )
    
    # Form Configuration
    description = models.TextField(blank=True)
    instructions = models.TextField(blank=True)
    
    # Form Structure
    sections = models.JSONField(default=list, blank=True)
    questions = models.JSONField(default=list, blank=True)
    rating_scales = models.JSONField(default=dict, blank=True)
    
    # Form Settings
    is_required = models.BooleanField(default=True)
    allow_partial_save = models.BooleanField(default=True)
    require_comments = models.BooleanField(default=False)
    show_progress = models.BooleanField(default=True)
    
    # Applicability
    applies_to_departments = models.JSONField(default=list, blank=True)
    applies_to_roles = models.JSONField(default=list, blank=True)
    applies_to_levels = models.JSONField(default=list, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_template = models.BooleanField(default=False)
    version = models.IntegerField(default=1)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_review_forms'
        verbose_name = 'Review Form'
        verbose_name_plural = 'Review Forms'
        constraints = [
            models.UniqueConstraint(fields=['company', 'form_code'], name='uk_form_code'),
        ]
        ordering = ['form_name']


# Reference Models (simplified versions - full implementations would be in separate files)

class ReviewResponse(models.Model):
    """
    Individual review responses and answers
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='review_responses'
    )
    performance_review = models.ForeignKey(
        PerformanceReview, 
        on_delete=models.CASCADE,
        related_name='review_responses'
    )
    review_form = models.ForeignKey(
        ReviewForm, 
        on_delete=models.CASCADE,
        related_name='review_responses'
    )
    reviewer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='review_responses'
    )
    question_id = models.CharField(max_length=100)
    response_data = models.JSONField(default=dict)
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    comments = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_review_responses'
        verbose_name = 'Review Response'
        verbose_name_plural = 'Review Responses'


class ReviewCalibrationSession(models.Model):
    """
    Calibration session for rating moderation
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='review_calibration_sessions'
    )
    review_cycle = models.ForeignKey(
        PerformanceReviewCycle, 
        on_delete=models.CASCADE,
        related_name='calibration_sessions'
    )
    session_name = models.CharField(max_length=200)
    session_date = models.DateTimeField()
    
    class Meta:
        db_table = 'hr_review_calibration_sessions'
        verbose_name = 'Review Calibration Session'
        verbose_name_plural = 'Review Calibration Sessions'
