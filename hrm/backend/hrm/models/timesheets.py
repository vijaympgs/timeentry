"""
Timesheets Models for HRM
Following BBP 05.2 Timesheets specifications
Aligned with enterprise governance and Olivine UI canon
"""
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()

class Timesheet(models.Model):
    """
    Main timesheet model for time tracking and approval
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='timesheet_company')
    employee = models.ForeignKey('hrm.Employee', on_delete=models.CASCADE, related_name='timesheet_employee')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='timesheet_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='timesheet_updated_by')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='timesheet_approved_by')
    timesheet_number = models.CharField(max_length=50)
    timesheet_period_start = models.DateField()
    timesheet_period_end = models.DateField()
    timesheet_type = models.CharField(max_length=20, choices=[('weekly', 'Weekly'), ('bi_weekly', 'Bi-Weekly'), ('semi_monthly', 'Semi-Monthly'), ('monthly', 'Monthly'), ('custom', 'Custom')], default='weekly')
    status = models.CharField(max_length=20, choices=[('draft', 'Draft'), ('submitted', 'Submitted'), ('under_review', 'Under Review'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('paid', 'Paid'), ('voided', 'Voided')], default='draft')
    total_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    regular_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    overtime_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    double_time_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    billable_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    non_billable_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    billable_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default='USD')
    submitted_date = models.DateTimeField(null=True, blank=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    employee_notes = models.TextField(blank=True)
    approver_notes = models.TextField(blank=True)
    auto_submit = models.BooleanField(default=False)
    requires_approval = models.BooleanField(default=True)
    allow_edit_after_approval = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_timesheets'
        verbose_name = 'Timesheet'
        verbose_name_plural = 'Timesheets'
        indexes = [models.Index(fields=['company', 'employee'], name='idx_timesheet_employee'), models.Index(fields=['company', 'status'], name='idx_timesheet_status'), models.Index(fields=['company', 'timesheet_period_start'], name='idx_timesheet_period')]
        constraints = [models.UniqueConstraint(fields=['company', 'timesheet_number'], name='uk_timesheet_number')]
        ordering = ['-timesheet_period_start']

    def __str__(self):
        return f'Timesheet {self.timesheet_number} - {self.employee}'

    def clean(self):
        """Validate timesheet data"""
        if self.timesheet_period_start >= self.timesheet_period_end:
            raise ValidationError('Period start must be before end date')
        if self.total_hours and self.total_hours < 0:
            raise ValidationError('Total hours cannot be negative')
        if self.regular_hours and self.regular_hours < 0:
            raise ValidationError('Regular hours cannot be negative')
        if self.overtime_hours and self.overtime_hours < 0:
            raise ValidationError('Overtime hours cannot be negative')
        if self.double_time_hours and self.double_time_hours < 0:
            raise ValidationError('Double time hours cannot be negative')
        if self.billable_hours and self.billable_hours < 0:
            raise ValidationError('Billable hours cannot be negative')
        if self.non_billable_hours and self.non_billable_hours < 0:
            raise ValidationError('Non-billable hours cannot be negative')
        if self.total_amount and self.total_amount < 0:
            raise ValidationError('Total amount cannot be negative')
        if self.billable_amount and self.billable_amount < 0:
            raise ValidationError('Billable amount cannot be negative')
        if self.timesheet_period_end > timezone.now().date():
            if not self.pk:
                raise ValidationError('Timesheet period cannot be in the future')

    def save(self, *args, **kwargs):
        """Calculate totals before saving"""
        self.total_hours = self.regular_hours + self.overtime_hours + self.double_time_hours
        if self.total_hours > 0:
            if self.billable_hours + self.non_billable_hours != self.total_hours:
                if self.billable_hours == 0 and self.non_billable_hours == 0:
                    self.billable_hours = self.total_hours
                else:
                    self.non_billable_hours = self.total_hours - self.billable_hours
        super().save(*args, **kwargs)

class TimesheetEntry(models.Model):
    """
    Individual time entries within a timesheet
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='timesheetentry_company')
    timesheet = models.ForeignKey(Timesheet, on_delete=models.CASCADE, related_name='timesheetentry_timesheet')
    employee = models.ForeignKey('hrm.Employee', on_delete=models.CASCADE, related_name='timesheetentry_employee')
    project = models.ForeignKey('hrm.Project', on_delete=models.SET_NULL, null=True, blank=True, related_name='timesheetentry_project')
    task = models.ForeignKey('hrm.Task', on_delete=models.SET_NULL, null=True, blank=True, related_name='timesheetentry_task')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='timesheetentry_approved_by')
    entry_date = models.DateField()
    activity_type = models.CharField(max_length=100, choices=[('regular', 'Regular Work'), ('meeting', 'Meeting'), ('training', 'Training'), ('travel', 'Travel'), ('break', 'Break'), ('overtime', 'Overtime'), ('double_time', 'Double Time'), ('holiday', 'Holiday Work'), ('on_call', 'On Call'), ('standby', 'Standby'), ('administrative', 'Administrative'), ('research', 'Research'), ('development', 'Development'), ('testing', 'Testing'), ('documentation', 'Documentation'), ('other', 'Other')], default='regular')
    hours = models.DecimalField(max_digits=8, decimal_places=2)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    rate_type = models.CharField(max_length=20, choices=[('standard', 'Standard'), ('overtime', 'Overtime'), ('double_time', 'Double Time'), ('custom', 'Custom')], default='standard')
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bill_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_billable = models.BooleanField(default=True)
    billable_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    work_location = models.CharField(max_length=200, blank=True)
    remote_work = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[('draft', 'Draft'), ('submitted', 'Submitted'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('adjusted', 'Adjusted')], default='draft')
    approved_date = models.DateTimeField(null=True, blank=True)
    approval_comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_timesheet_entries'
        verbose_name = 'Timesheet Entry'
        verbose_name_plural = 'Timesheet Entries'
        indexes = [models.Index(fields=['company', 'timesheet'], name='idx_entry_timesheet'), models.Index(fields=['company', 'employee'], name='idx_entry_employee'), models.Index(fields=['company', 'entry_date'], name='idx_entry_date'), models.Index(fields=['company', 'project'], name='idx_entry_project')]
        ordering = ['entry_date']

    def __str__(self):
        return f'Entry {self.entry_date} - {self.hours}h - {self.employee}'

    def clean(self):
        """Validate timesheet entry data"""
        if self.hours and self.hours < 0:
            raise ValidationError('Entry hours cannot be negative')
        if self.hours and self.hours > 24:
            raise ValidationError('Entry hours cannot exceed 24')
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError('Start time must be before end time')
        if self.hourly_rate and self.hourly_rate < 0:
            raise ValidationError('Hourly rate cannot be negative')
        if self.bill_rate and self.bill_rate < 0:
            raise ValidationError('Bill rate cannot be negative')
        if self.billable_amount and self.billable_amount < 0:
            raise ValidationError('Billable amount cannot be negative')
        if self.timesheet and self.entry_date:
            if self.entry_date < self.timesheet.timesheet_period_start or self.entry_date > self.timesheet.timesheet_period_end:
                raise ValidationError('Entry date must be within timesheet period')
        if self.entry_date and self.entry_date > timezone.now().date():
            if not self.pk:
                raise ValidationError('Entry date cannot be in the future')

    def save(self, *args, **kwargs):
        """Calculate billable amount before saving"""
        if self.is_billable and self.bill_rate:
            self.billable_amount = self.hours * self.bill_rate
        elif not self.is_billable:
            self.billable_amount = 0
        super().save(*args, **kwargs)

class TimesheetApproval(models.Model):
    """
    Timesheet approval workflow tracking
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='timesheetapproval_company')
    timesheet = models.ForeignKey(Timesheet, on_delete=models.CASCADE, related_name='timesheetapproval_timesheet')
    approver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='timesheetapproval_approver')
    delegated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='timesheetapproval_delegated_by')
    approval_level = models.IntegerField(default=1)
    approval_action = models.CharField(max_length=20, choices=[('submitted', 'Submitted'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('returned', 'Returned'), ('escalated', 'Escalated')])
    approval_date = models.DateTimeField(auto_now_add=True)
    approver_comments = models.TextField(blank=True)
    system_notes = models.TextField(blank=True)
    is_current = models.BooleanField(default=True)
    is_final = models.BooleanField(default=False)
    delegation_reason = models.TextField(blank=True)

    class Meta:
        db_table = 'hr_timesheet_approvals'
        verbose_name = 'Timesheet Approval'
        verbose_name_plural = 'Timesheet Approvals'
        indexes = [models.Index(fields=['company', 'timesheet'], name='idx_approval_timesheet'), models.Index(fields=['company', 'approver'], name='idx_enroll_appr_approver_ts'), models.Index(fields=['company', 'approval_date'], name='idx_approval_date')]
        ordering = ['-approval_date']

    def __str__(self):
        return f'Approval {self.approval_action} - {self.timesheet}'

    def clean(self):
        """Validate timesheet approval data"""
        if self.approval_level and self.approval_level < 1:
            raise ValidationError('Approval level must be at least 1')
        if self.approval_date and self.approval_date > timezone.now():
            raise ValidationError('Approval date cannot be in the future')

class Project(models.Model):
    """
    Project information for time tracking
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='project_company')
    project_name = models.CharField(max_length=200)
    project_code = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'hr_projects'
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

class Task(models.Model):
    """
    Task information for time tracking
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='task_company')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='task_project')
    task_name = models.CharField(max_length=200)
    task_code = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'hr_tasks'
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'