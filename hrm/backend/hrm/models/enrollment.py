"""
Enrollment Models for HRM
Following BBP 07.2 Enrollment specifications
Aligned with enterprise governance and Olivine UI canon
"""
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()

class Enrollment(models.Model):
    """
    Main enrollment model for course registration
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='enrollment_company')
    employee = models.ForeignKey('hrm.Employee', on_delete=models.CASCADE, related_name='enrollment_employee')
    course = models.ForeignKey('hrm.Course', on_delete=models.CASCADE, related_name='enrollment_course')
    course_session = models.ForeignKey('hrm.CourseSession', on_delete=models.SET_NULL, null=True, blank=True, related_name='enrollment_course_session')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='enrollment_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='enrollment_updated_by')
    manager_approval = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='enrollment_manager_approval')
    enrollment_number = models.CharField(max_length=50)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('waitlisted', 'Waitlisted'), ('active', 'Active'), ('completed', 'Completed'), ('cancelled', 'Cancelled'), ('dropped', 'Dropped'), ('expired', 'Expired'), ('suspended', 'Suspended')], default='pending')
    enrollment_type = models.CharField(max_length=50, choices=[('self_enrollment', 'Self Enrollment'), ('manager_assigned', 'Manager Assigned'), ('hr_assigned', 'HR Assigned'), ('bulk_enrollment', 'Bulk Enrollment'), ('mandatory', 'Mandatory Training'), ('compliance', 'Compliance Required'), ('learning_path', 'Learning Path')])
    priority = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('urgent', 'Urgent')], default='medium')
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default='USD')
    budget_code = models.CharField(max_length=50, blank=True)
    cost_center = models.CharField(max_length=100, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    estimated_hours = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    progress_percentage = models.IntegerField(default=0)
    completion_date = models.DateTimeField(null=True, blank=True)
    last_access_date = models.DateTimeField(null=True, blank=True)
    manager_approval_required = models.BooleanField(default=False)
    manager_approval_date = models.DateTimeField(null=True, blank=True)
    waitlist_position = models.IntegerField(null=True, blank=True)
    waitlist_date = models.DateTimeField(null=True, blank=True)
    waitlist_notification_sent = models.BooleanField(default=False)
    cancellation_date = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)
    refund_eligible = models.BooleanField(default=False)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    employee_notes = models.TextField(blank=True)
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_enrollments'
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollments'
        indexes = [models.Index(fields=['company', 'employee'], name='idx_enrollment_employee'), models.Index(fields=['company', 'course'], name='idx_enrollment_course'), models.Index(fields=['company', 'status'], name='idx_enrollment_status'), models.Index(fields=['company', 'enrollment_date'], name='idx_enrollment_date')]
        constraints = [models.UniqueConstraint(fields=['company', 'enrollment_number'], name='uk_enrollment_number')]
        ordering = ['-enrollment_date']

    def __str__(self):
        return f'Enrollment {self.enrollment_number} - {self.employee}'

    def clean(self):
        """Validate enrollment data"""
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError('Start date must be before end date')
        if self.progress_percentage and (self.progress_percentage < 0 or self.progress_percentage > 100):
            raise ValidationError('Progress percentage must be between 0 and 100')
        if self.estimated_hours and self.estimated_hours < 0:
            raise ValidationError('Estimated hours cannot be negative')
        if self.cost and self.cost < 0:
            raise ValidationError('Cost cannot be negative')
        if self.refund_amount and self.refund_amount < 0:
            raise ValidationError('Refund amount cannot be negative')
        if self.waitlist_position and self.waitlist_position < 1:
            raise ValidationError('Waitlist position must be positive')
        if self.completion_date and self.start_date:
            if self.completion_date.date() < self.start_date:
                raise ValidationError('Completion date cannot be before start date')
        if self.last_access_date and self.last_access_date > timezone.now():
            raise ValidationError('Last access date cannot be in the future')

    def save(self, *args, **kwargs):
        """Auto-calculate progress based on status"""
        if self.status == 'completed':
            self.progress_percentage = 100
            if not self.completion_date:
                self.completion_date = timezone.now()
        elif self.status == 'cancelled' or self.status == 'dropped':
            pass
        super().save(*args, **kwargs)

class EnrollmentWaitlist(models.Model):
    """
    Waitlist management for course enrollments
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='enrollmentwaitlist_company')
    course = models.ForeignKey('hrm.Course', on_delete=models.CASCADE, related_name='enrollmentwaitlist_course')
    employee = models.ForeignKey('hrm.Employee', on_delete=models.CASCADE, related_name='enrollmentwaitlist_employee')
    waitlist_position = models.IntegerField()
    waitlist_date = models.DateTimeField(auto_now_add=True)
    notification_sent = models.BooleanField(default=False)
    notification_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('expired', 'Expired'), ('enrolled', 'Enrolled'), ('cancelled', 'Cancelled')], default='active')
    notification_email = models.EmailField(blank=True)
    notification_phone = models.CharField(max_length=50, blank=True)
    preferred_session_times = models.JSONField(default=list, blank=True)
    preferred_location = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_enrollment_waitlists'
        verbose_name = 'Enrollment Waitlist'
        verbose_name_plural = 'Enrollment Waitlists'
        indexes = [models.Index(fields=['company', 'course'], name='idx_waitlist_course'), models.Index(fields=['company', 'employee'], name='idx_waitlist_employee'), models.Index(fields=['company', 'status'], name='idx_waitlist_status')]
        ordering = ['waitlist_position']

    def __str__(self):
        return f'Waitlist #{self.waitlist_position} - {self.employee}'

    def clean(self):
        """Validate waitlist data"""
        if self.waitlist_position and self.waitlist_position < 1:
            raise ValidationError('Waitlist position must be positive')
        if self.notification_date and self.notification_date > timezone.now():
            raise ValidationError('Notification date cannot be in the future')

class EnrollmentApproval(models.Model):
    """
    Enrollment approval workflow tracking
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='enrollmentapproval_company')
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='enrollmentapproval_enrollment')
    approver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollmentapproval_approver')
    approval_type = models.CharField(max_length=50, choices=[('manager', 'Manager Approval'), ('hr', 'HR Approval'), ('budget', 'Budget Approval'), ('capacity', 'Capacity Approval'), ('compliance', 'Compliance Approval')])
    decision = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('returned', 'Returned'), ('escalated', 'Escalated')], default='pending')
    decision_date = models.DateTimeField(null=True, blank=True)
    approver_comments = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_enrollment_approvals'
        verbose_name = 'Enrollment Approval'
        verbose_name_plural = 'Enrollment Approvals'
        indexes = [models.Index(fields=['company', 'enrollment'], name='idx_approval_enrollment'), models.Index(fields=['company', 'approver'], name='idx_enroll_appr_approver_en')]
        ordering = ['-created_at']

    def __str__(self):
        return f'Approval {self.approval_type} - {self.enrollment}'

    def clean(self):
        """Validate enrollment approval data"""
        if self.decision_date and self.decision_date > timezone.now():
            raise ValidationError('Decision date cannot be in the future')

class EnrollmentRule(models.Model):
    """
    Enrollment rules and business logic
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='enrollmentrule_company')
    rule_name = models.CharField(max_length=200)
    rule_type = models.CharField(max_length=50)
    rule_conditions = models.JSONField(default=dict)
    rule_actions = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'hr_enrollment_rules'
        verbose_name = 'Enrollment Rule'
        verbose_name_plural = 'Enrollment Rules'

class EnrollmentTemplate(models.Model):
    """
    Enrollment templates for bulk operations
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='enrollmenttemplate_company')
    template_name = models.CharField(max_length=200)
    template_type = models.CharField(max_length=50)
    template_criteria = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'hr_enrollment_templates'
        verbose_name = 'Enrollment Template'
        verbose_name_plural = 'Enrollment Templates'

class EnrollmentCourse(models.Model):
    """
    Course reference model for enrollments (avoiding conflict with main Course model)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='enrollmentcourse_company')
    course_name = models.CharField(max_length=200)
    course_code = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'hr_enrollment_courses'
        verbose_name = 'Enrollment Course'
        verbose_name_plural = 'Enrollment Courses'

class EnrollmentCourseSession(models.Model):
    """
    Course session reference model for enrollments (avoiding conflict with main CourseSession model)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='enrollmentcoursesession_company')
    course = models.ForeignKey(EnrollmentCourse, on_delete=models.CASCADE, related_name='enrollmentcoursesession_course')
    session_name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'hr_enrollment_sessions'
        verbose_name = 'Enrollment Course Session'
        verbose_name_plural = 'Enrollment Course Sessions'