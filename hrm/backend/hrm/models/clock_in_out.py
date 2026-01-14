"""
Clock-In-Out Models for HRM
Following BBP 05.1 Clock-In-Out specifications
Aligned with enterprise governance and Olivine UI canon
"""
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()

class TimeEntry(models.Model):
    """
    Main time entry model for clock-in/out tracking
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='timeentry_company')
    employee = models.ForeignKey('hrm.Employee', on_delete=models.CASCADE, related_name='timeentry_employee')
    shift = models.ForeignKey('hrm.Shift', on_delete=models.SET_NULL, null=True, blank=True, related_name='timeentry_shift')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='timeentry_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='timeentry_updated_by')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='timeentry_approved_by')
    entry_number = models.CharField(max_length=50)
    entry_date = models.DateField()
    clock_in_time = models.DateTimeField()
    clock_in_method = models.CharField(max_length=20, choices=[('web', 'Web'), ('mobile', 'Mobile'), ('kiosk', 'Kiosk'), ('biometric', 'Biometric'), ('rfid', 'RFID Card'), ('facial_recognition', 'Facial Recognition'), ('manual', 'Manual')])
    clock_in_location = models.CharField(max_length=200, blank=True)
    clock_in_ip_address = models.GenericIPAddressField(null=True, blank=True)
    clock_in_device_id = models.CharField(max_length=100, blank=True)
    clock_in_coordinates = models.JSONField(default=dict, blank=True)
    clock_out_time = models.DateTimeField(null=True, blank=True)
    clock_out_method = models.CharField(max_length=20, choices=[('web', 'Web'), ('mobile', 'Mobile'), ('kiosk', 'Kiosk'), ('biometric', 'Biometric'), ('rfid', 'RFID Card'), ('facial_recognition', 'Facial Recognition'), ('manual', 'Manual'), ('auto', 'Auto')], blank=True)
    clock_out_location = models.CharField(max_length=200, blank=True)
    clock_out_ip_address = models.GenericIPAddressField(null=True, blank=True)
    clock_out_device_id = models.CharField(max_length=100, blank=True)
    clock_out_coordinates = models.JSONField(default=dict, blank=True)
    total_hours = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    regular_hours = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    overtime_hours = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    double_time_hours = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    break_start_time = models.DateTimeField(null=True, blank=True)
    break_end_time = models.DateTimeField(null=True, blank=True)
    break_duration = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    unpaid_break = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('completed', 'Completed'), ('missed_clock_out', 'Missed Clock Out'), ('pending_approval', 'Pending Approval'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('adjusted', 'Adjusted'), ('voided', 'Voided')], default='active')
    validation_status = models.CharField(max_length=20, choices=[('not_validated', 'Not Validated'), ('valid', 'Valid'), ('invalid', 'Invalid'), ('warning', 'Warning')], default='not_validated')
    is_late = models.BooleanField(default=False)
    is_early_departure = models.BooleanField(default=False)
    is_overtime = models.BooleanField(default=False)
    is_weekend = models.BooleanField(default=False)
    is_holiday = models.BooleanField(default=False)
    employee_notes = models.TextField(blank=True)
    manager_notes = models.TextField(blank=True)
    system_notes = models.TextField(blank=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    approval_comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_time_entries'
        verbose_name = 'Time Entry'
        verbose_name_plural = 'Time Entries'
        indexes = [models.Index(fields=['company', 'employee'], name='idx_time_employee'), models.Index(fields=['company', 'entry_date'], name='idx_time_date'), models.Index(fields=['company', 'status'], name='idx_time_status'), models.Index(fields=['company', 'clock_in_time'], name='idx_time_clock_in')]
        constraints = [models.UniqueConstraint(fields=['company', 'entry_number'], name='uk_time_entry_number')]
        ordering = ['-clock_in_time']

    def __str__(self):
        return f'Time Entry {self.entry_number} - {self.employee}'

    def clean(self):
        """Validate time entry data"""
        if self.clock_out_time and self.clock_out_time <= self.clock_in_time:
            raise ValidationError('Clock out time must be after clock in time')
        if self.break_start_time and self.break_end_time:
            if self.break_start_time <= self.clock_in_time:
                raise ValidationError('Break start must be after clock in')
            if self.clock_out_time and self.break_end_time >= self.clock_out_time:
                raise ValidationError('Break end must be before clock out')
        if self.total_hours and self.total_hours < 0:
            raise ValidationError('Total hours cannot be negative')
        if self.regular_hours and self.regular_hours < 0:
            raise ValidationError('Regular hours cannot be negative')
        if self.overtime_hours and self.overtime_hours < 0:
            raise ValidationError('Overtime hours cannot be negative')
        if self.double_time_hours and self.double_time_hours < 0:
            raise ValidationError('Double time hours cannot be negative')
        if self.break_duration and self.break_duration < 0:
            raise ValidationError('Break duration cannot be negative')
        if self.entry_date and self.entry_date > timezone.now().date():
            if not self.pk:
                raise ValidationError('Entry date cannot be in the future')

    def save(self, *args, **kwargs):
        """Calculate time fields before saving"""
        if self.clock_out_time:
            time_diff = self.clock_out_time - self.clock_in_time
            total_hours = time_diff.total_seconds() / 3600
            if self.break_duration:
                total_hours -= float(self.break_duration)
            self.total_hours = round(total_hours, 2)
            if self.total_hours:
                if self.total_hours <= 8:
                    self.regular_hours = self.total_hours
                    self.overtime_hours = 0
                elif self.total_hours <= 12:
                    self.regular_hours = 8
                    self.overtime_hours = self.total_hours - 8
                else:
                    self.regular_hours = 8
                    self.overtime_hours = 4
                    self.double_time_hours = self.total_hours - 12
        super().save(*args, **kwargs)

class AttendanceException(models.Model):
    """
    Attendance exceptions and policy violations
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='attendanceexception_company')
    time_entry = models.ForeignKey(TimeEntry, on_delete=models.CASCADE, related_name='attendanceexception_time_entry')
    employee = models.ForeignKey('hrm.Employee', on_delete=models.CASCADE, related_name='attendanceexception_employee')
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='attendanceexception_resolved_by')
    exception_type = models.CharField(max_length=50, choices=[('late_arrival', 'Late Arrival'), ('early_departure', 'Early Departure'), ('missed_clock_in', 'Missed Clock In'), ('missed_clock_out', 'Missed Clock Out'), ('unauthorized_break', 'Unauthorized Break'), ('excessive_break', 'Excessive Break'), ('overtime_violation', 'Overtime Violation'), ('shift_violation', 'Shift Violation'), ('location_violation', 'Location Violation'), ('device_violation', 'Device Violation')])
    exception_severity = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')], default='medium')
    exception_description = models.TextField()
    expected_time = models.DateTimeField(null=True, blank=True)
    actual_time = models.DateTimeField(null=True, blank=True)
    variance_minutes = models.IntegerField(null=True, blank=True)
    policy_name = models.CharField(max_length=200, blank=True)
    policy_rule = models.CharField(max_length=500, blank=True)
    policy_threshold = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('open', 'Open'), ('under_review', 'Under Review'), ('resolved', 'Resolved'), ('escalated', 'Escalated'), ('dismissed', 'Dismissed')], default='open')
    resolution = models.CharField(max_length=50, choices=[('employee_corrected', 'Employee Corrected'), ('manager_approved', 'Manager Approved'), ('hr_approved', 'HR Approved'), ('auto_corrected', 'Auto Corrected'), ('dismissed', 'Dismissed')], blank=True)
    resolution_notes = models.TextField(blank=True)
    resolved_date = models.DateTimeField(null=True, blank=True)
    employee_notified = models.BooleanField(default=False)
    manager_notified = models.BooleanField(default=False)
    hr_notified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_attendance_exceptions'
        verbose_name = 'Attendance Exception'
        verbose_name_plural = 'Attendance Exceptions'
        indexes = [models.Index(fields=['company', 'time_entry'], name='idx_exception_time_entry'), models.Index(fields=['company', 'employee'], name='idx_exception_employee'), models.Index(fields=['company', 'status'], name='idx_exception_status')]
        ordering = ['-created_at']

    def __str__(self):
        return f'Exception: {self.exception_type} - {self.employee}'

    def clean(self):
        """Validate attendance exception data"""
        if self.variance_minutes and self.variance_minutes < 0:
            raise ValidationError('Variance minutes cannot be negative')
        if self.policy_threshold and self.policy_threshold < 0:
            raise ValidationError('Policy threshold cannot be negative')
        if self.expected_time and self.actual_time:
            if self.expected_time >= self.actual_time:
                raise ValidationError('Expected time must be before actual time')

class AttendancePolicy(models.Model):
    """
    Attendance policies and rules configuration
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='attendancepolicy_company')
    policy_name = models.CharField(max_length=200)
    policy_code = models.CharField(max_length=50)
    policy_type = models.CharField(max_length=50, choices=[('general', 'General Attendance'), ('late_arrival', 'Late Arrival'), ('early_departure', 'Early Departure'), ('break_policy', 'Break Policy'), ('overtime', 'Overtime'), ('weekend', 'Weekend'), ('holiday', 'Holiday'), ('remote_work', 'Remote Work')])
    applies_to_all = models.BooleanField(default=True)
    applies_to_departments = models.JSONField(default=list, blank=True)
    applies_to_employees = models.JSONField(default=list, blank=True)
    applies_to_shifts = models.JSONField(default=list, blank=True)
    grace_period_minutes = models.IntegerField(default=0)
    late_threshold_minutes = models.IntegerField(default=5)
    early_departure_threshold_minutes = models.IntegerField(default=5)
    break_required = models.BooleanField(default=True)
    break_duration_minutes = models.IntegerField(default=30)
    break_after_hours = models.DecimalField(max_digits=4, decimal_places=2, default=4.0)
    max_break_duration_minutes = models.IntegerField(default=60)
    overtime_after_hours = models.DecimalField(max_digits=4, decimal_places=2, default=8.0)
    overtime_rate_multiplier = models.DecimalField(max_digits=4, decimal_places=2, default=1.5)
    double_time_after_hours = models.DecimalField(max_digits=4, decimal_places=2, default=12.0)
    location_required = models.BooleanField(default=False)
    allowed_locations = models.JSONField(default=list, blank=True)
    geofence_enabled = models.BooleanField(default=False)
    geofence_radius_meters = models.IntegerField(null=True, blank=True)
    allowed_devices = models.JSONField(default=list, blank=True)
    device_verification_required = models.BooleanField(default=False)
    biometric_required = models.BooleanField(default=False)
    auto_approve_exceptions = models.BooleanField(default=False)
    exception_approval_workflow = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, choices=[('draft', 'Draft'), ('active', 'Active'), ('inactive', 'Inactive'), ('archived', 'Archived')], default='draft')
    effective_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    policy_document_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_attendance_policies'
        verbose_name = 'Attendance Policy'
        verbose_name_plural = 'Attendance Policies'
        indexes = [models.Index(fields=['company', 'policy_type'], name='idx_policy_type'), models.Index(fields=['company', 'status'], name='idx_policy_status')]
        constraints = [models.UniqueConstraint(fields=['company', 'policy_code'], name='uk_policy_code')]
        ordering = ['policy_name']

    def __str__(self):
        return f'{self.policy_name} ({self.policy_code})'

    def clean(self):
        """Validate attendance policy data"""
        threshold_fields = ['grace_period_minutes', 'late_threshold_minutes', 'early_departure_threshold_minutes']
        for field in threshold_fields:
            value = getattr(self, field)
            if value is not None and value < 0:
                raise ValidationError(f"{field.replace('_', ' ').title()} cannot be negative")
        if self.break_duration_minutes and self.break_duration_minutes < 0:
            raise ValidationError('Break duration minutes cannot be negative')
        if self.max_break_duration_minutes and self.max_break_duration_minutes < 0:
            raise ValidationError('Maximum break duration minutes cannot be negative')
        if self.break_after_hours and self.break_after_hours < 0:
            raise ValidationError('Break after hours cannot be negative')
        if self.overtime_after_hours and self.overtime_after_hours < 0:
            raise ValidationError('Overtime after hours cannot be negative')
        if self.overtime_rate_multiplier and self.overtime_rate_multiplier < 1:
            raise ValidationError('Overtime rate multiplier must be at least 1.0')
        if self.double_time_after_hours and self.double_time_after_hours < 0:
            raise ValidationError('Double time after hours cannot be negative')
        if self.geofence_radius_meters and self.geofence_radius_meters < 0:
            raise ValidationError('Geofence radius meters cannot be negative')
        if self.effective_date and self.expiry_date:
            if self.effective_date >= self.expiry_date:
                raise ValidationError('Expiry date must be after effective date')

class Shift(models.Model):
    """
    Shift configuration for attendance
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='shift_company')
    shift_name = models.CharField(max_length=200)
    shift_code = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    days_of_week = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'hr_shifts'
        verbose_name = 'Shift'
        verbose_name_plural = 'Shifts'

class AttendanceDevice(models.Model):
    """
    Attendance devices for clock-in/out
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='attendancedevice_company')
    device_name = models.CharField(max_length=200)
    device_type = models.CharField(max_length=50)
    device_id = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'hr_attendance_devices'
        verbose_name = 'Attendance Device'
        verbose_name_plural = 'Attendance Devices'