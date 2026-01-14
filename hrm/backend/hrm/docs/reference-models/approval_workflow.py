"""
Approval Workflow Models for HRM
Following BBP 05.3 Approval Workflow specifications
Aligned with enterprise governance and Olivine UI canon
"""

import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class ApprovalRequest(models.Model):
    """
    Main approval request model for workflow management
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys - Using lazy string references per governance
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='approval_requests'
    )
    employee = models.ForeignKey(
        'hrm.Employee', 
        on_delete=models.CASCADE,
        related_name='approval_requests'
    )
    workflow = models.ForeignKey(
        'hrm.ApprovalWorkflow', 
        on_delete=models.CASCADE,
        related_name='approval_requests'
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='created_approval_requests'
    )
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='updated_approval_requests'
    )
    
    # Request Details
    request_number = models.CharField(max_length=50)
    request_type = models.CharField(
        max_length=50, 
        choices=[
            ('timesheet', 'Timesheet'),
            ('time_off', 'Time Off'),
            ('attendance_exception', 'Attendance Exception'),
            ('overtime', 'Overtime'),
            ('schedule_change', 'Schedule Change'),
            ('leave_adjustment', 'Leave Adjustment'),
            ('timesheet_correction', 'Timesheet Correction'),
        ]
    )
    request_title = models.CharField(max_length=200)
    request_description = models.TextField(blank=True)
    
    # Status Management
    status = models.CharField(
        max_length=20, 
        choices=[
            ('draft', 'Draft'),
            ('submitted', 'Submitted'),
            ('in_review', 'In Review'),
            ('pending_approval', 'Pending Approval'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('returned', 'Returned'),
            ('escalated', 'Escalated'),
            ('withdrawn', 'Withdrawn'),
            ('expired', 'Expired'),
        ], 
        default='draft'
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
    
    # Request Data
    request_data = models.JSONField(default=dict)  # Flexible storage for request-specific data
    attachment_urls = models.JSONField(default=list, blank=True)
    
    # Timeline Information
    submitted_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    
    # Current Approval Information
    current_approval_level = models.IntegerField(default=1)
    current_approver = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='current_approvals'
    )
    next_approval_level = models.IntegerField(null=True, blank=True)
    
    # Final Decision
    final_approver = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='final_approvals'
    )
    final_approval_date = models.DateTimeField(null=True, blank=True)
    final_comments = models.TextField(blank=True)
    
    # Delegation Information
    delegated_approver = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='delegated_approvals'
    )
    delegation_reason = models.TextField(blank=True)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_approval_requests'
        verbose_name = 'Approval Request'
        verbose_name_plural = 'Approval Requests'
        indexes = [
            models.Index(fields=['company', 'employee'], name='idx_request_employee'),
            models.Index(fields=['company', 'status'], name='idx_request_status'),
            models.Index(fields=['company', 'request_type'], name='idx_request_type'),
            models.Index(fields=['company', 'current_approver'], name='idx_request_approver'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['company', 'request_number'], name='uk_request_number'),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Request {self.request_number} - {self.employee}"
    
    def clean(self):
        """Validate approval request data"""
        # Validate approval dates
        if self.due_date and self.submitted_date:
            if self.due_date <= self.submitted_date:
                raise ValidationError("Due date must be after submitted date")
        
        # Validate approval levels are positive
        if self.current_approval_level and self.current_approval_level < 1:
            raise ValidationError("Current approval level must be positive")
        
        if self.next_approval_level and self.next_approval_level < 1:
            raise ValidationError("Next approval level must be positive")
        
        # Validate final approval date logic
        if self.final_approval_date and self.submitted_date:
            if self.final_approval_date < self.submitted_date:
                raise ValidationError("Final approval date cannot be before submitted date")
        
        # Validate final approval date is not in future
        if self.final_approval_date and self.final_approval_date > timezone.now():
            raise ValidationError("Final approval date cannot be in the future")
        
        # Validate completed date logic
        if self.completed_date and self.submitted_date:
            if self.completed_date < self.submitted_date:
                raise ValidationError("Completed date cannot be before submitted date")


class ApprovalStep(models.Model):
    """
    Individual approval steps within a workflow
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='approval_steps'
    )
    approval_request = models.ForeignKey(
        ApprovalRequest, 
        on_delete=models.CASCADE,
        related_name='approval_steps'
    )
    approver = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='approval_step_assignments'
    )
    delegated_to = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='delegated_approval_steps'
    )
    
    # Step Details
    step_number = models.IntegerField()
    step_name = models.CharField(max_length=200)
    step_type = models.CharField(
        max_length=50, 
        choices=[
            ('individual', 'Individual Approver'),
            ('group', 'Group Approval'),
            ('parallel', 'Parallel Approval'),
            ('sequential', 'Sequential Approval'),
            ('conditional', 'Conditional Approval'),
            ('auto', 'Automatic Approval'),
        ]
    )
    
    # Approver Information
    approver_role = models.CharField(max_length=100, blank=True)
    approver_group = models.CharField(max_length=100, blank=True)
    
    # Step Configuration
    is_required = models.BooleanField(default=True)
    is_final_step = models.BooleanField(default=False)
    approval_required = models.BooleanField(default=True)
    
    # Conditional Rules
    condition_rules = models.JSONField(default=dict, blank=True)
    approval_criteria = models.JSONField(default=dict, blank=True)
    
    # Status and Timing
    status = models.CharField(
        max_length=20, 
        choices=[
            ('pending', 'Pending'),
            ('in_progress', 'In Progress'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('skipped', 'Skipped'),
            ('escalated', 'Escalated'),
        ], 
        default='pending'
    )
    assigned_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    
    # Decision Information
    decision = models.CharField(
        max_length=20, 
        choices=[
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('returned', 'Returned'),
            ('escalated', 'Escalated'),
        ], 
        blank=True
    )
    approver_comments = models.TextField(blank=True)
    system_notes = models.TextField(blank=True)
    
    # Delegation
    delegation_reason = models.TextField(blank=True)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_approval_steps'
        verbose_name = 'Approval Step'
        verbose_name_plural = 'Approval Steps'
        indexes = [
            models.Index(fields=['company', 'approval_request'], name='idx_step_request'),
            models.Index(fields=['company', 'approver'], name='idx_step_approver'),
            models.Index(fields=['company', 'status'], name='idx_step_status'),
        ]
        ordering = ['step_number']
    
    def __str__(self):
        return f"Step {self.step_number}: {self.step_name} - {self.approval_request}"
    
    def clean(self):
        """Validate approval step data"""
        # Validate step number is positive
        if self.step_number and self.step_number < 1:
            raise ValidationError("Step number must be positive")
        
        # Validate due date logic
        if self.due_date and self.assigned_date:
            if self.due_date <= self.assigned_date:
                raise ValidationError("Due date must be after assigned date")
        
        # Validate completed date logic
        if self.completed_date and self.assigned_date:
            if self.completed_date < self.assigned_date:
                raise ValidationError("Completed date cannot be before assigned date")
        
        # Validate completed date is not in future
        if self.completed_date and self.completed_date > timezone.now():
            raise ValidationError("Completed date cannot be in the future")
    
    def save(self, *args, **kwargs):
        """Auto-set completed date when status is completed"""
        if self.status in ['approved', 'rejected'] and not self.completed_date:
            self.completed_date = timezone.now()
            self.decision = self.status
        
        super().save(*args, **kwargs)


class ApprovalWorkflow(models.Model):
    """
    Approval workflow configuration and rules
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='approval_workflows'
    )
    
    # Workflow Details
    workflow_name = models.CharField(max_length=200)
    workflow_code = models.CharField(max_length=50)
    workflow_type = models.CharField(
        max_length=50, 
        choices=[
            ('timesheet', 'Timesheet Approval'),
            ('time_off', 'Time Off Approval'),
            ('attendance_exception', 'Attendance Exception Approval'),
            ('overtime', 'Overtime Approval'),
            ('schedule_change', 'Schedule Change Approval'),
            ('leave_adjustment', 'Leave Adjustment Approval'),
            ('timesheet_correction', 'Timesheet Correction Approval'),
        ]
    )
    
    # Workflow Configuration
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    
    # Scope and Applicability
    applies_to_all = models.BooleanField(default=True)
    applies_to_departments = models.JSONField(default=list, blank=True)
    applies_to_employees = models.JSONField(default=list, blank=True)
    applies_to_employee_types = models.JSONField(default=list, blank=True)
    
    # Workflow Rules
    max_approval_levels = models.IntegerField(default=5)
    allow_parallel_approval = models.BooleanField(default=False)
    require_all_approvers = models.BooleanField(default=True)
    allow_delegation = models.BooleanField(default=True)
    
    # Timing Rules
    approval_timeout_hours = models.IntegerField(default=72)
    escalation_enabled = models.BooleanField(default=True)
    escalation_after_hours = models.IntegerField(default=48)
    auto_approve_conditions = models.JSONField(default=dict, blank=True)
    
    # Notification Rules
    notify_submitter = models.BooleanField(default=True)
    notify_approvers = models.BooleanField(default=True)
    notify_on_completion = models.BooleanField(default=True)
    reminder_enabled = models.BooleanField(default=True)
    reminder_interval_hours = models.IntegerField(default=24)
    
    # Status and Dates
    status = models.CharField(
        max_length=20, 
        choices=[
            ('draft', 'Draft'),
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ('archived', 'Archived'),
        ], 
        default='draft'
    )
    effective_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_approval_workflows'
        verbose_name = 'Approval Workflow'
        verbose_name_plural = 'Approval Workflows'
        indexes = [
            models.Index(fields=['company', 'workflow_type'], name='idx_workflow_type'),
            models.Index(fields=['company', 'status'], name='idx_workflow_status'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['company', 'workflow_code'], name='uk_workflow_code'),
        ]
        ordering = ['workflow_name']
    
    def __str__(self):
        return f"Workflow {self.workflow_name} - {self.company}"
    
    def clean(self):
        """Validate approval workflow data"""
        # Validate max approval levels is positive
        if self.max_approval_levels and self.max_approval_levels < 1:
            raise ValidationError("Maximum approval levels must be at least 1")
        
        # Validate timeout hours is positive
        if self.approval_timeout_hours and self.approval_timeout_hours < 1:
            raise ValidationError("Approval timeout hours must be at least 1")
        
        # Validate escalation hours is positive
        if self.escalation_after_hours and self.escalation_after_hours < 1:
            raise ValidationError("Escalation after hours must be at least 1")
        
        # Validate reminder interval hours is positive
        if self.reminder_interval_hours and self.reminder_interval_hours < 1:
            raise ValidationError("Reminder interval hours must be at least 1")
        
        # Validate escalation timing
        if self.escalation_enabled and self.escalation_after_hours >= self.approval_timeout_hours:
            raise ValidationError("Escalation time must be less than approval timeout")
        
        # Validate effective date logic
        if self.effective_date and self.effective_date > timezone.now().date():
            if self.status == 'active':
                raise ValidationError("Effective date cannot be in the future for active workflows")
        
        # Validate expiry date logic
        if self.expiry_date and self.effective_date:
            if self.expiry_date <= self.effective_date:
                raise ValidationError("Expiry date must be after effective date")


# Reference Models (simplified versions - full implementations would be in separate files)

class ApprovalRule(models.Model):
    """
    Approval rules and conditions
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='approval_rules'
    )
    workflow = models.ForeignKey(
        ApprovalWorkflow, 
        on_delete=models.CASCADE,
        related_name='approval_rules'
    )
    rule_name = models.CharField(max_length=200)
    rule_condition = models.JSONField(default=dict)
    rule_action = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'hr_approval_rules'
        verbose_name = 'Approval Rule'
        verbose_name_plural = 'Approval Rules'


class Delegation(models.Model):
    """
    Approval delegation configuration
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='delegations'
    )
    delegator = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='delegated_approvals'
    )
    delegate = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='received_delegations'
    )
    delegation_type = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'hr_delegations'
        verbose_name = 'Delegation'
        verbose_name_plural = 'Delegations'
