"""
Ratings Models for HRM
Following BBP 06.3 Ratings specifications
Aligned with enterprise governance and Olivine UI canon
"""
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()

class RatingScale(models.Model):
    """
    Main rating scale model for performance management
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='ratingscale_company')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='ratingscale_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='ratingscale_updated_by')
    scale_name = models.CharField(max_length=200)
    scale_code = models.CharField(max_length=50)
    scale_type = models.CharField(max_length=50, choices=[('numeric', 'Numeric Scale'), ('descriptive', 'Descriptive Scale'), ('behavioral', 'Behavioral Scale'), ('competency', 'Competency Scale'), ('hybrid', 'Hybrid Scale'), ('custom', 'Custom Scale')])
    description = models.TextField(blank=True)
    min_rating = models.DecimalField(max_digits=5, decimal_places=2)
    max_rating = models.DecimalField(max_digits=5, decimal_places=2)
    rating_increment = models.DecimalField(max_digits=5, decimal_places=2)
    allow_decimal_ratings = models.BooleanField(default=False)
    decimal_places = models.IntegerField(default=0)
    reverse_rating_order = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=[('draft', 'Draft'), ('active', 'Active'), ('inactive', 'Inactive'), ('deprecated', 'Deprecated')], default='draft')
    is_default = models.BooleanField(default=False)
    applies_to_departments = models.JSONField(default=list, blank=True)
    applies_to_roles = models.JSONField(default=list, blank=True)
    applies_to_levels = models.JSONField(default=list, blank=True)
    effective_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    rating_guidelines_text = models.TextField(blank=True)
    calibration_guidelines = models.TextField(blank=True)
    documentation_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_rating_scales'
        verbose_name = 'Rating Scale'
        verbose_name_plural = 'Rating Scales'
        indexes = [models.Index(fields=['company', 'status'], name='idx_scale_status'), models.Index(fields=['company', 'scale_type'], name='idx_scale_type')]
        constraints = [models.UniqueConstraint(fields=['company', 'scale_code'], name='uk_scale_code')]
        ordering = ['scale_name']

    def __str__(self):
        return f'{self.scale_name} ({self.scale_code})'

    def clean(self):
        """Validate rating scale data"""
        if self.min_rating >= self.max_rating:
            raise ValidationError('Maximum rating must be greater than minimum rating')
        if self.rating_increment <= 0:
            raise ValidationError('Rating increment must be positive')
        if self.decimal_places < 0 or self.decimal_places > 5:
            raise ValidationError('Decimal places must be between 0 and 5')
        if self.effective_date and self.effective_date < timezone.now().date():
            if not self.pk:
                raise ValidationError('Effective date cannot be in the past')
        if self.expiry_date and self.effective_date and (self.expiry_date <= self.effective_date):
            raise ValidationError('Expiry date must be after effective date')
        range_width = self.max_rating - self.min_rating
        if self.rating_increment > range_width:
            raise ValidationError('Rating increment cannot be larger than the rating range')

class RatingLevel(models.Model):
    """
    Individual rating levels within a rating scale
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='ratinglevel_company')
    rating_scale = models.ForeignKey(RatingScale, on_delete=models.CASCADE, related_name='ratinglevel_rating_scale')
    level_number = models.IntegerField()
    level_name = models.CharField(max_length=200)
    level_code = models.CharField(max_length=50)
    level_description = models.TextField(blank=True)
    numeric_value = models.DecimalField(max_digits=5, decimal_places=2)
    numeric_range_min = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    numeric_range_max = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    performance_level = models.CharField(max_length=50, choices=[('outstanding', 'Outstanding'), ('exceeds_expectations', 'Exceeds Expectations'), ('meets_expectations', 'Meets Expectations'), ('needs_improvement', 'Needs Improvement'), ('unsatisfactory', 'Unsatisfactory'), ('custom', 'Custom')])
    color_code = models.CharField(max_length=20, blank=True)
    icon_name = models.CharField(max_length=100, blank=True)
    behavioral_indicators = models.JSONField(default=list, blank=True)
    key_behaviors = models.JSONField(default=list, blank=True)
    development_suggestions = models.JSONField(default=list, blank=True)
    calibration_notes = models.TextField(blank=True)
    target_distribution = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_rating_levels'
        verbose_name = 'Rating Level'
        verbose_name_plural = 'Rating Levels'
        indexes = [models.Index(fields=['company', 'rating_scale'], name='idx_level_scale'), models.Index(fields=['company', 'level_number'], name='idx_level_number')]
        constraints = [models.UniqueConstraint(fields=['company', 'rating_scale', 'level_code'], name='uk_level_code')]
        ordering = ['level_number']

    def __str__(self):
        return f'{self.level_name} ({self.level_code})'

    def clean(self):
        """Validate rating level data"""
        if self.level_number and self.level_number < 1:
            raise ValidationError('Level number must be positive')
        if self.rating_scale:
            if self.numeric_value < self.rating_scale.min_rating or self.numeric_value > self.rating_scale.max_rating:
                raise ValidationError(f'Numeric value must be between {self.rating_scale.min_rating} and {self.rating_scale.max_rating}')
        if self.numeric_range_min and self.numeric_range_max and (self.numeric_range_min >= self.numeric_range_max):
            raise ValidationError('Range minimum must be less than range maximum')
        if self.target_distribution and (not 0 <= self.target_distribution <= 100):
            raise ValidationError('Target distribution must be between 0 and 100')
        if self.color_code and (not self.color_code.startswith('#')):
            raise ValidationError('Color code must start with #')

class CalibrationSession(models.Model):
    """
    Calibration session for rating moderation and standardization
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='calibrationsession_company')
    review_cycle = models.ForeignKey('hrm.ReviewCycle', on_delete=models.CASCADE, related_name='calibrationsession_review_cycle')
    rating_scale = models.ForeignKey(RatingScale, on_delete=models.CASCADE, related_name='calibrationsession_rating_scale')
    facilitator = models.ForeignKey('hrm.Employee', on_delete=models.SET_NULL, null=True, related_name='calibrationsession_facilitator')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='calibrationsession_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='calibrationsession_updated_by')
    session_name = models.CharField(max_length=200)
    session_code = models.CharField(max_length=50)
    session_type = models.CharField(max_length=50, choices=[('department', 'Department Calibration'), ('division', 'Division Calibration'), ('organization', 'Organization Calibration'), ('level', 'Level Calibration'), ('custom', 'Custom Calibration')])
    description = models.TextField(blank=True)
    objectives = models.TextField(blank=True)
    scheduled_date = models.DateTimeField()
    duration_hours = models.IntegerField(default=2)
    location = models.CharField(max_length=200, blank=True)
    is_virtual = models.BooleanField(default=False)
    meeting_url = models.URLField(blank=True)
    participants = models.JSONField(default=list, blank=True)
    required_attendees = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=20, choices=[('planned', 'Planned'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled'), ('postponed', 'Postponed')], default='planned')
    target_distribution = models.JSONField(default=dict, blank=True)
    tolerance_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=5.0)
    require_justification = models.BooleanField(default=True)
    total_reviews_calibrated = models.IntegerField(default=0)
    ratings_adjusted = models.IntegerField(default=0)
    average_rating_change = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    session_notes = models.TextField(blank=True)
    action_items = models.JSONField(default=list, blank=True)
    follow_up_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_calibration_sessions'
        verbose_name = 'Calibration Session'
        verbose_name_plural = 'Calibration Sessions'
        indexes = [models.Index(fields=['company', 'review_cycle'], name='idx_session_cycle'), models.Index(fields=['company', 'status'], name='idx_session_status'), models.Index(fields=['company', 'scheduled_date'], name='idx_course_session_dt_rating')]
        constraints = [models.UniqueConstraint(fields=['company', 'session_code'], name='uk_session_code')]
        ordering = ['-scheduled_date']

    def __str__(self):
        return f'{self.session_name} ({self.session_code})'

    def clean(self):
        """Validate calibration session data"""
        if self.duration_hours and (self.duration_hours < 1 or self.duration_hours > 8):
            raise ValidationError('Duration must be between 1 and 8 hours')
        if self.scheduled_date and self.scheduled_date < timezone.now():
            if not self.pk:
                raise ValidationError('Scheduled date cannot be in the past')
        if self.tolerance_percentage and (not 0 <= self.tolerance_percentage <= 50):
            raise ValidationError('Tolerance percentage must be between 0 and 50')
        if self.participants and len(self.participants) < 3:
            raise ValidationError('Calibration sessions require at least 3 participants')
        if self.is_virtual and (not self.meeting_url):
            raise ValidationError('Virtual sessions must have a meeting URL')
        if self.average_rating_change and abs(self.average_rating_change) > 10:
            raise ValidationError('Average rating change seems unrealistic')

class RatingDistribution(models.Model):
    """
    Rating distribution analysis and monitoring
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='ratingdistribution_company')
    review_cycle = models.ForeignKey('hrm.ReviewCycle', on_delete=models.CASCADE, related_name='ratingdistribution_review_cycle')
    rating_scale = models.ForeignKey(RatingScale, on_delete=models.CASCADE, related_name='ratingdistribution_rating_scale')
    rating_level = models.ForeignKey(RatingLevel, on_delete=models.CASCADE, related_name='ratingdistribution_rating_level')
    actual_count = models.IntegerField(default=0)
    expected_count = models.IntegerField(default=0)
    actual_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    expected_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hr_rating_distributions'
        verbose_name = 'Rating Distribution'
        verbose_name_plural = 'Rating Distributions'
        indexes = [models.Index(fields=['company', 'review_cycle'], name='idx_dist_cycle'), models.Index(fields=['company', 'rating_scale'], name='idx_dist_scale')]

class RatingGuideline(models.Model):
    """
    Rating guidelines and documentation
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='ratingguideline_company')
    rating_scale = models.ForeignKey(RatingScale, on_delete=models.CASCADE, related_name='ratingguideline_rating_scale')
    guideline_title = models.CharField(max_length=200)
    guideline_content = models.TextField()
    guideline_type = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'hr_rating_guidelines'
        verbose_name = 'Rating Guideline'
        verbose_name_plural = 'Rating Guidelines'
        indexes = [models.Index(fields=['company', 'rating_scale'], name='idx_guideline_scale')]

class ReviewCycle(models.Model):
    """
    Review cycle for calibration sessions
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='reviewcycle_company')
    cycle_name = models.CharField(max_length=200)
    cycle_code = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('planned', 'Planned'), ('active', 'Active'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='planned')

    class Meta:
        db_table = 'hr_review_cycles'
        verbose_name = 'Review Cycle'
        verbose_name_plural = 'Review Cycles'
        constraints = [models.UniqueConstraint(fields=['company', 'cycle_code'], name='uk_cycle_code')]