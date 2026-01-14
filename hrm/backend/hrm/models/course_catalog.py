"""
Course Catalog Models for HRM
Following BBP 07.1 Course Catalog specifications
Aligned with enterprise governance and Olivine UI canon
"""
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()

class Course(models.Model):
    """
    Main course model for learning management
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='course_company')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='course_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='course_updated_by')
    course_code = models.CharField(max_length=50)
    course_name = models.CharField(max_length=200)
    course_description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True)
    course_type = models.CharField(max_length=50, choices=[('instructor_led', 'Instructor-Led'), ('self_paced', 'Self-Paced'), ('blended', 'Blended'), ('virtual', 'Virtual'), ('online', 'Online'), ('classroom', 'Classroom'), ('elearning', 'E-Learning'), ('webinar', 'Webinar'), ('workshop', 'Workshop'), ('seminar', 'Seminar')])
    course_category = models.CharField(max_length=100, choices=[('leadership', 'Leadership'), ('management', 'Management'), ('technical', 'Technical Skills'), ('soft_skills', 'Soft Skills'), ('compliance', 'Compliance'), ('safety', 'Safety'), ('onboarding', 'Onboarding'), ('product', 'Product Training'), ('sales', 'Sales Training'), ('customer_service', 'Customer Service'), ('communication', 'Communication'), ('diversity', 'Diversity & Inclusion'), ('wellness', 'Wellness'), ('other', 'Other')])
    duration_hours = models.DecimalField(max_digits=6, decimal_places=2)
    difficulty_level = models.CharField(max_length=20, choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced'), ('expert', 'Expert')])
    language = models.CharField(max_length=10, default='en')
    status = models.CharField(max_length=20, choices=[('draft', 'Draft'), ('active', 'Active'), ('inactive', 'Inactive'), ('archived', 'Archived'), ('under_review', 'Under Review')], default='draft')
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_mandatory = models.BooleanField(default=False)
    cost_per_employee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default='USD')
    budget_code = models.CharField(max_length=50, blank=True)
    max_capacity = models.IntegerField(null=True, blank=True)
    min_enrollment = models.IntegerField(default=1)
    current_enrollment = models.IntegerField(default=0)
    waitlist_enabled = models.BooleanField(default=False)
    prerequisites = models.JSONField(default=list, blank=True)
    target_audience = models.JSONField(default=list, blank=True)
    required_materials = models.JSONField(default=list, blank=True)
    learning_objectives = models.JSONField(default=list, blank=True)
    key_takeaways = models.JSONField(default=list, blank=True)
    competencies = models.JSONField(default=list, blank=True)
    skills = models.JSONField(default=list, blank=True)
    job_roles = models.JSONField(default=list, blank=True)
    delivery_method = models.JSONField(default=list, blank=True)
    schedule_type = models.CharField(max_length=50, choices=[('fixed', 'Fixed Schedule'), ('flexible', 'Flexible Schedule'), ('on_demand', 'On Demand'), ('recurring', 'Recurring')])
    offers_certification = models.BooleanField(default=False)
    certification_details = models.TextField(blank=True)
    ceu_credits = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    requires_evaluation = models.BooleanField(default=False)
    evaluation_method = models.CharField(max_length=100, blank=True)
    feedback_enabled = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    effective_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    tags = models.JSONField(default=list, blank=True)
    keywords = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = 'hr_courses'
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        indexes = [models.Index(fields=['company', 'status'], name='idx_course_status'), models.Index(fields=['company', 'course_category'], name='idx_course_category'), models.Index(fields=['company', 'course_type'], name='idx_course_type')]
        constraints = [models.UniqueConstraint(fields=['company', 'course_code'], name='uk_course_code')]
        ordering = ['course_name']

    def __str__(self):
        return f'{self.course_name} ({self.course_code})'

    def clean(self):
        """Validate course data"""
        if self.duration_hours and self.duration_hours < 0:
            raise ValidationError('Duration hours must be positive')
        if self.duration_hours and self.duration_hours > 1000:
            raise ValidationError('Duration hours cannot exceed 1000')
        if self.max_capacity and self.max_capacity < 1:
            raise ValidationError('Maximum capacity must be at least 1')
        if self.min_enrollment and self.min_enrollment < 1:
            raise ValidationError('Minimum enrollment must be at least 1')
        if self.max_capacity and self.min_enrollment and (self.min_enrollment > self.max_capacity):
            raise ValidationError('Minimum enrollment cannot exceed maximum capacity')
        if self.current_enrollment < 0:
            raise ValidationError('Current enrollment cannot be negative')
        if self.max_capacity and self.current_enrollment > self.max_capacity:
            raise ValidationError('Current enrollment cannot exceed maximum capacity')
        if self.effective_date and self.expiry_date:
            if self.effective_date >= self.expiry_date:
                raise ValidationError('Expiry date must be after effective date')
        if self.ceu_credits and self.ceu_credits < 0:
            raise ValidationError('CEU credits cannot be negative')
        if self.cost_per_employee and self.cost_per_employee < 0:
            raise ValidationError('Cost per employee cannot be negative')

class CourseContent(models.Model):
    """
    Course content and materials
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='coursecontent_company')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='coursecontent_course')
    content_title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=50, choices=[('video', 'Video'), ('document', 'Document'), ('presentation', 'Presentation'), ('scorm', 'SCORM Package'), ('xapi', 'xAPI Content'), ('audio', 'Audio'), ('image', 'Image'), ('quiz', 'Quiz'), ('assignment', 'Assignment'), ('resource', 'Resource'), ('link', 'External Link')])
    description = models.TextField(blank=True)
    file_url = models.URLField(blank=True)
    file_size = models.BigIntegerField(null=True, blank=True)
    file_type = models.CharField(max_length=100, blank=True)
    module_number = models.IntegerField(null=True, blank=True)
    lesson_number = models.IntegerField(null=True, blank=True)
    sort_order = models.IntegerField(default=0)
    duration_minutes = models.IntegerField(null=True, blank=True)
    is_required = models.BooleanField(default=True)
    is_downloadable = models.BooleanField(default=False)
    access_level = models.CharField(max_length=50, choices=[('public', 'Public'), ('enrolled', 'Enrolled Only'), ('prerequisite', 'After Prerequisite'), ('completion', 'After Completion')], default='enrolled')
    status = models.CharField(max_length=20, choices=[('draft', 'Draft'), ('active', 'Active'), ('inactive', 'Inactive'), ('archived', 'Archived')], default='draft')
    tags = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_course_contents'
        verbose_name = 'Course Content'
        verbose_name_plural = 'Course Contents'
        indexes = [models.Index(fields=['company', 'course'], name='idx_content_course'), models.Index(fields=['company', 'content_type'], name='idx_content_type')]
        ordering = ['module_number', 'lesson_number', 'sort_order']

    def __str__(self):
        return f'{self.content_title} - {self.course.course_name}'

    def clean(self):
        """Validate course content data"""
        if self.duration_minutes and self.duration_minutes < 0:
            raise ValidationError('Duration minutes cannot be negative')
        if self.file_size and self.file_size < 0:
            raise ValidationError('File size cannot be negative')
        if self.module_number and self.module_number < 1:
            raise ValidationError('Module number must be positive')
        if self.lesson_number and self.lesson_number < 1:
            raise ValidationError('Lesson number must be positive')
        if self.sort_order < 0:
            raise ValidationError('Sort order cannot be negative')

class CourseSession(models.Model):
    """
    Scheduled course sessions and classes
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='coursesession_company')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='coursesession_course')
    instructor = models.ForeignKey('hrm.Instructor', on_delete=models.SET_NULL, null=True, blank=True, related_name='coursesession_instructor')
    session_name = models.CharField(max_length=200)
    session_number = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    timezone = models.CharField(max_length=50, default='UTC')
    location_type = models.CharField(max_length=50, choices=[('classroom', 'Classroom'), ('virtual', 'Virtual'), ('online', 'Online'), ('onsite', 'On-site'), ('hybrid', 'Hybrid')])
    location_name = models.CharField(max_length=200, blank=True)
    location_address = models.TextField(blank=True)
    virtual_meeting_url = models.URLField(blank=True)
    meeting_id = models.CharField(max_length=100, blank=True)
    meeting_password = models.CharField(max_length=100, blank=True)
    max_participants = models.IntegerField()
    current_participants = models.IntegerField(default=0)
    waitlist_count = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=[('scheduled', 'Scheduled'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled'), ('postponed', 'Postponed')], default='scheduled')
    session_notes = models.TextField(blank=True)
    instructor_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_course_sessions'
        verbose_name = 'Course Session'
        verbose_name_plural = 'Course Sessions'
        indexes = [models.Index(fields=['company', 'course'], name='idx_session_course'), models.Index(fields=['company', 'instructor'], name='idx_session_instructor'), models.Index(fields=['company', 'start_date'], name='idx_course_session_dt_course')]
        ordering = ['start_date']

    def __str__(self):
        return f'{self.session_name} - {self.course.course_name}'

    def clean(self):
        """Validate course session data"""
        if self.start_date and self.end_date:
            if self.start_date >= self.end_date:
                raise ValidationError('End date must be after start date')
        if self.start_date and self.end_date:
            duration = self.end_date - self.start_date
            duration_hours = duration.total_seconds() / 3600
            if duration_hours > 8:
                raise ValidationError('Session duration cannot exceed 8 hours')
        if self.session_number and self.session_number < 1:
            raise ValidationError('Session number must be positive')
        if self.max_participants and self.max_participants < 1:
            raise ValidationError('Maximum participants must be at least 1')
        if self.current_participants < 0:
            raise ValidationError('Current participants cannot be negative')
        if self.max_participants and self.current_participants > self.max_participants:
            raise ValidationError('Current participants cannot exceed maximum participants')
        if self.waitlist_count < 0:
            raise ValidationError('Waitlist count cannot be negative')
        if self.location_type == 'virtual' and (not self.virtual_meeting_url):
            raise ValidationError('Virtual sessions must have a meeting URL')
        if self.start_date and self.start_date < timezone.now():
            if not self.pk:
                raise ValidationError('Session start date cannot be in the past')

class Instructor(models.Model):
    """
    Course instructor and facilitator information
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='instructor_company')
    instructor_name = models.CharField(max_length=200)
    instructor_code = models.CharField(max_length=50)
    bio = models.TextField(blank=True)
    expertise_areas = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'hr_instructors'
        verbose_name = 'Instructor'
        verbose_name_plural = 'Instructors'
        constraints = [models.UniqueConstraint(fields=['company', 'instructor_code'], name='uk_instructor_code')]

class CourseLearningPath(models.Model):
    """
    Learning paths and curriculum
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, related_name='courselearningpath_company')
    path_name = models.CharField(max_length=200)
    path_code = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    duration_weeks = models.IntegerField(default=4)  # 4 weeks default
    difficulty_level = models.IntegerField(choices=[
        (1, 'Beginner'),
        (2, 'Intermediate'),
        (3, 'Advanced'),
        (4, 'Expert'),
        (5, 'Master'),
    ], default=1)
    prerequisites = models.TextField(blank=True)
    learning_objectives = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_learning_paths'
        verbose_name = 'Learning Path'
        verbose_name_plural = 'Learning Paths'
        indexes = [
            models.Index(fields=['company', 'is_active'], name='idx_lp_active'),
        ]
        ordering = ['difficulty_level', 'path_name']
    
    def __str__(self):
        return f"{self.path_name} ({self.get_difficulty_level_display()})"
