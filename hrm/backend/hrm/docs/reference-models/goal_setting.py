"""
Goal Setting Models for HRM
Following BBP 06.1 Goal Setting specifications
Aligned with enterprise governance and Olivine UI canon
"""

import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class Goal(models.Model):
    """
    Main goal model for performance management
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys - Using lazy string references per governance
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='goals'
    )
    employee = models.ForeignKey(
        'hrm.Employee', 
        on_delete=models.CASCADE,
        related_name='goals'
    )
    manager = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='managed_goals'
    )
    parent_goal = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE,
        null=True, 
        blank=True,
        related_name='child_goals'
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='created_goals'
    )
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='updated_goals'
    )
    approved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='approved_goals'
    )
    
    # Goal Details
    goal_number = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Goal Classification
    goal_type = models.CharField(
        max_length=50, 
        choices=[
            ('performance', 'Performance Goal'),
            ('development', 'Development Goal'),
            ('behavioral', 'Behavioral Goal'),
            ('project', 'Project Goal'),
            ('team', 'Team Goal'),
            ('organizational', 'Organizational Goal'),
        ], 
        default='performance'
    )
    goal_category = models.CharField(
        max_length=100, 
        choices=[
            ('productivity', 'Productivity'),
            ('quality', 'Quality'),
            ('customer_service', 'Customer Service'),
            ('innovation', 'Innovation'),
            ('collaboration', 'Collaboration'),
            ('leadership', 'Leadership'),
            ('communication', 'Communication'),
            ('technical_skills', 'Technical Skills'),
            ('business_acumen', 'Business Acumen'),
            ('other', 'Other'),
        ]
    )
    
    # SMART Framework
    is_smart = models.BooleanField(default=False)
    specific_description = models.TextField(blank=True)
    measurable_metrics = models.JSONField(default=list, blank=True)
    achievable_assessment = models.TextField(blank=True)
    relevance_explanation = models.TextField(blank=True)
    time_bound_date = models.DateField(null=True, blank=True)
    
    # Goal Configuration
    priority = models.CharField(
        max_length=20, 
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('critical', 'Critical'),
        ], 
        default='medium'
    )
    weight_percentage = models.IntegerField(default=0)
    difficulty_level = models.CharField(
        max_length=20, 
        choices=[
            ('easy', 'Easy'),
            ('moderate', 'Moderate'),
            ('challenging', 'Challenging'),
            ('stretch', 'Stretch'),
        ], 
        default='moderate'
    )
    
    # Status Management
    status = models.CharField(
        max_length=20, 
        choices=[
            ('draft', 'Draft'),
            ('proposed', 'Proposed'),
            ('approved', 'Approved'),
            ('active', 'Active'),
            ('on_track', 'On Track'),
            ('at_risk', 'At Risk'),
            ('behind', 'Behind'),
            ('achieved', 'Achieved'),
            ('partially_achieved', 'Partially Achieved'),
            ('not_achieved', 'Not Achieved'),
            ('cancelled', 'Cancelled'),
        ], 
        default='draft'
    )
    
    # Timeline
    created_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    target_date = models.DateField()
    completion_date = models.DateField(null=True, blank=True)
    
    # Progress Tracking
    progress_percentage = models.IntegerField(default=0)
    current_status = models.TextField(blank=True)
    achievements = models.JSONField(default=list, blank=True)
    challenges = models.JSONField(default=list, blank=True)
    
    # Success Metrics
    success_criteria = models.JSONField(default=list, blank=True)
    measurement_method = models.CharField(max_length=100, blank=True)
    target_value = models.CharField(max_length=200, blank=True)
    current_value = models.CharField(max_length=200, blank=True)
    
    # Alignment
    strategic_objective = models.ForeignKey(
        'hrm.StrategicObjective', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='aligned_goals'
    )
    department_goal = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='department_aligned_goals'
    )
    company_goal = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='company_aligned_goals'
    )
    
    # Approval Information
    approved_date = models.DateTimeField(null=True, blank=True)
    approval_comments = models.TextField(blank=True)
    
    # Notes and Attachments
    employee_notes = models.TextField(blank=True)
    manager_notes = models.TextField(blank=True)
    attachment_urls = models.JSONField(default=list, blank=True)
    
    # Audit Fields
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_goals'
        verbose_name = 'Goal'
        verbose_name_plural = 'Goals'
        indexes = [
            models.Index(fields=['company', 'employee'], name='idx_goal_employee'),
            models.Index(fields=['company', 'status'], name='idx_goal_status'),
            models.Index(fields=['company', 'goal_type'], name='idx_goal_type'),
            models.Index(fields=['company', 'target_date'], name='idx_goal_target_date'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['company', 'goal_number'], name='uk_goal_number'),
        ]
        ordering = ['-created_date']
    
    def __str__(self):
        return f"Goal {self.goal_number} - {self.employee}"
    
    def clean(self):
        """Validate goal data"""
        # Validate progress percentage
        if self.progress_percentage and (self.progress_percentage < 0 or self.progress_percentage > 100):
            raise ValidationError("Progress percentage must be between 0 and 100")
        
        # Validate weight percentage
        if self.weight_percentage and (self.weight_percentage < 0 or self.weight_percentage > 100):
            raise ValidationError("Weight percentage must be between 0 and 100")
        
        # Validate goal dates
        if self.target_date and self.start_date:
            if self.target_date <= self.start_date:
                raise ValidationError("Target date must be after start date")
        
        # Validate completion date logic
        if self.completion_date and self.start_date:
            if self.completion_date < self.start_date:
                raise ValidationError("Completion date cannot be before start date")
        
        # Validate time bound date for SMART goals
        if self.is_smart and not self.time_bound_date:
            raise ValidationError("Time-bound date is required for SMART goals")
        
        # Validate completion date is not in future
        if self.completion_date and self.completion_date > timezone.now().date():
            raise ValidationError("Completion date cannot be in the future")
    
    def save(self, *args, **kwargs):
        """Auto-update status based on progress"""
        if self.status == 'achieved' and not self.completion_date:
            self.completion_date = timezone.now().date()
            self.progress_percentage = 100
        
        super().save(*args, **kwargs)


class GoalProgress(models.Model):
    """
    Goal progress updates and check-ins
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='goal_progress'
    )
    goal = models.ForeignKey(
        Goal, 
        on_delete=models.CASCADE,
        related_name='goal_progress'
    )
    employee = models.ForeignKey(
        'hrm.Employee', 
        on_delete=models.CASCADE,
        related_name='goal_progress'
    )
    
    # Progress Details
    progress_date = models.DateTimeField(auto_now_add=True)
    progress_percentage = models.IntegerField()
    status_update = models.CharField(
        max_length=20, 
        choices=[
            ('on_track', 'On Track'),
            ('ahead', 'Ahead of Schedule'),
            ('behind', 'Behind Schedule'),
            ('blocked', 'Blocked'),
            ('completed', 'Completed'),
        ]
    )
    
    # Progress Description
    achievements = models.TextField(blank=True)
    challenges = models.TextField(blank=True)
    next_steps = models.TextField(blank=True)
    support_needed = models.TextField(blank=True)
    
    # Metrics and Evidence
    metrics_data = models.JSONField(default=dict, blank=True)
    evidence_urls = models.JSONField(default=list, blank=True)
    milestone_achieved = models.BooleanField(default=False)
    
    # Manager Feedback
    manager_feedback = models.TextField(blank=True)
    manager_rating = models.IntegerField(null=True, blank=True)
    coaching_notes = models.TextField(blank=True)
    
    # Recognition
    recognition_given = models.BooleanField(default=False)
    recognition_details = models.TextField(blank=True)
    
    class Meta:
        db_table = 'hr_goal_progress'
        verbose_name = 'Goal Progress'
        verbose_name_plural = 'Goal Progress'
        indexes = [
            models.Index(fields=['company', 'goal'], name='idx_progress_goal'),
            models.Index(fields=['company', 'employee'], name='idx_progress_employee'),
            models.Index(fields=['company', 'progress_date'], name='idx_progress_date'),
        ]
        ordering = ['-progress_date']
    
    def __str__(self):
        return f"Progress for {self.goal} - {self.progress_date}"
    
    def clean(self):
        """Validate goal progress data"""
        # Validate progress percentage
        if self.progress_percentage and (self.progress_percentage < 0 or self.progress_percentage > 100):
            raise ValidationError("Progress percentage must be between 0 and 100")
        
        # Validate manager rating
        if self.manager_rating and (self.manager_rating < 1 or self.manager_rating > 5):
            raise ValidationError("Manager rating must be between 1 and 5")


class GoalTemplate(models.Model):
    """
    Goal templates for standardized goal creation
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='goal_templates'
    )
    
    # Template Details
    template_name = models.CharField(max_length=200)
    template_code = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    
    # Template Configuration
    goal_type = models.CharField(max_length=50)
    goal_category = models.CharField(max_length=100)
    suggested_weight = models.IntegerField(default=0)
    suggested_difficulty = models.CharField(max_length=20)
    
    # Template Content
    title_template = models.CharField(max_length=200)
    description_template = models.TextField(blank=True)
    success_criteria_template = models.JSONField(default=list, blank=True)
    measurement_method_template = models.CharField(max_length=100, blank=True)
    
    # Applicability
    applies_to_departments = models.JSONField(default=list, blank=True)
    applies_to_roles = models.JSONField(default=list, blank=True)
    applies_to_levels = models.JSONField(default=list, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_goal_templates'
        verbose_name = 'Goal Template'
        verbose_name_plural = 'Goal Templates'
        constraints = [
            models.UniqueConstraint(fields=['company', 'template_code'], name='uk_template_code'),
        ]
        ordering = ['template_name']


# Reference Models (simplified versions - full implementations would be in separate files)

class StrategicObjective(models.Model):
    """
    Strategic objectives for goal alignment
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='strategic_objectives'
    )
    objective_name = models.CharField(max_length=200)
    objective_code = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'hr_strategic_objectives'
        verbose_name = 'Strategic Objective'
        verbose_name_plural = 'Strategic Objectives'


class GoalCategory(models.Model):
    """
    Goal categories for classification
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='goal_categories'
    )
    category_name = models.CharField(max_length=100)
    category_code = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'hr_goal_categories'
        verbose_name = 'Goal Category'
        verbose_name_plural = 'Goal Categories'
