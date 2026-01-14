"""
Termination Workflow Models for HRM
Following BBP 11.3 Termination Workflow specifications
Aligned with enterprise governance and Olivine UI canon
"""

import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class Termination(models.Model):
    """
    Main termination workflow model for employee separation
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys - Using lazy string references per governance
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='terminations'
    )
    employee = models.ForeignKey(
        'hrm.Employee', 
        on_delete=models.CASCADE,
        related_name='terminations'
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='created_terminations'
    )
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='updated_terminations'
    )
    manager = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='managed_terminations'
    )
    hr_coordinator = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='hr_coordinated_terminations'
    )
    legal_reviewer = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='legal_reviewed_terminations'
    )
    management_approver = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='management_approved_terminations'
    )
    it_coordinator = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='it_coordinated_terminations'
    )
    finance_coordinator = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='finance_coordinated_terminations'
    )
    initiated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='initiated_terminations'
    )
    approved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='approved_terminations'
    )
    
    # Workflow Details
    workflow_number = models.CharField(max_length=50)
    workflow_name = models.CharField(max_length=200)
    workflow_description = models.TextField(blank=True)
    
    # Employee Information
    employee_name = models.CharField(max_length=255)
    employee_email = models.EmailField()
    employee_department = models.CharField(max_length=100)
    employee_position = models.CharField(max_length=200)
    
    # Termination Details
    termination_type = models.CharField(
        max_length=50, 
        choices=[
            ('voluntary_resignation', 'Voluntary Resignation'),
            ('involuntary_termination', 'Involuntary Termination'),
            ('mutual_agreement', 'Mutual Agreement'),
            ('retirement', 'Retirement'),
            ('contract_end', 'Contract End'),
            ('layoff', 'Layoff'),
            ('redundancy', 'Redundancy'),
            ('misconduct', 'Misconduct'),
            ('performance', 'Performance Issues'),
            ('long_term_disability', 'Long-term Disability'),
            ('death', 'Death'),
            ('other', 'Other'),
        ]
    )
    termination_reason = models.CharField(max_length=200, blank=True)
    termination_reason_category = models.CharField(
        max_length=100, 
        choices=[
            ('performance', 'Performance'),
            ('misconduct', 'Misconduct'),
            ('restructuring', 'Restructuring'),
            ('financial', 'Financial'),
            ('personal', 'Personal'),
            ('legal', 'Legal'),
            ('business', 'Business'),
            ('other', 'Other'),
        ]
    )
    
    # Status Management
    status = models.CharField(
        max_length=20, 
        choices=[
            ('initiated', 'Initiated'),
            ('under_review', 'Under Review'),
            ('approved', 'Approved'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
            ('on_hold', 'On Hold'),
            ('error', 'Error'),
        ], 
        default='initiated'
    )
    
    # Timeline Information
    notification_date = models.DateField()
    effective_date = models.DateField()
    last_working_day = models.DateField()
    actual_separation_date = models.DateField(null=True, blank=True)
    
    # Priority and Urgency
    priority = models.CharField(
        max_length=20, 
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('urgent', 'Urgent'),
            ('critical', 'Critical'),
        ], 
        default='medium'
    )
    
    # Workflow Template
    workflow_template = models.ForeignKey(
        'hrm.TerminationTemplate', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='template_terminations'
    )
    template_name = models.CharField(max_length=200, blank=True)
    
    # Approval Information
    initiated_date = models.DateTimeField(auto_now_add=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    legal_approval_date = models.DateTimeField(null=True, blank=True)
    
    # Progress Tracking
    total_steps = models.IntegerField(default=0)
    completed_steps = models.IntegerField(default=0)
    pending_steps = models.IntegerField(default=0)
    overdue_steps = models.IntegerField(default=0)
    completion_percentage = models.IntegerField(default=0)
    
    # Cost Information
    estimated_cost = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    actual_cost = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    currency = models.CharField(max_length=10, default='USD')
    
    # Legal and Compliance
    legal_review_required = models.BooleanField(default=True)
    legal_review_completed = models.BooleanField(default=False)
    legal_review_date = models.DateTimeField(null=True, blank=True)
    legal_review_notes = models.TextField(blank=True)
    
    # Communication Information
    employee_notified = models.BooleanField(default=False)
    manager_notified = models.BooleanField(default=False)
    hr_notified = models.BooleanField(default=False)
    it_notified = models.BooleanField(default=False)
    
    # Additional Information
    special_instructions = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    confidential_notes = models.TextField(blank=True)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_terminations'
        verbose_name = 'Termination'
        verbose_name_plural = 'Terminations'
        indexes = [
            models.Index(fields=['company', 'employee'], name='idx_termination_employee'),
            models.Index(fields=['company', 'status'], name='idx_termination_status'),
            models.Index(fields=['company', 'effective_date'], name='idx_termination_effective_date'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['company', 'workflow_number'], name='uk_workflow_number'),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Termination {self.workflow_number} - {self.employee_name}"
    
    def clean(self):
        """Validate termination data"""
        # Validate effective date is not in past for new terminations
        if self.effective_date and self.effective_date < timezone.now().date():
            if not self.pk:  # New termination
                raise ValidationError("Effective date cannot be in the past")
        
        # Validate last working day logic
        if self.last_working_day and self.effective_date:
            if self.last_working_day < self.effective_date:
                raise ValidationError("Last working day must be on or after effective date")
        
        # Validate actual separation date logic
        if self.actual_separation_date and self.last_working_day:
            if self.actual_separation_date < self.last_working_day:
                raise ValidationError("Actual separation date cannot be before last working day")
        
        # Validate completion percentage
        if self.total_steps > 0:
            calculated_percentage = int((self.completed_steps / self.total_steps) * 100)
            if abs(calculated_percentage - self.completion_percentage) > 1:
                raise ValidationError("Completion percentage does not match step completion")
        
        # Validate step counts are non-negative
        step_fields = [
            'total_steps', 'completed_steps', 'pending_steps', 'overdue_steps'
        ]
        
        for field in step_fields:
            value = getattr(self, field)
            if value is not None and value < 0:
                raise ValidationError(f"{field.replace('_', ' ').title()} cannot be negative")
        
        # Validate costs are non-negative
        cost_fields = ['estimated_cost', 'actual_cost']
        
        for field in cost_fields:
            value = getattr(self, field)
            if value is not None and value < 0:
                raise ValidationError(f"{field.replace('_', ' ').title()} cannot be negative")
        
        # Validate currency code
        if self.currency and len(self.currency) != 3:
            raise ValidationError("Currency code must be 3 characters (ISO 4217)")
    
    def save(self, *args, **kwargs):
        """Auto-calculate progress percentage"""
        if self.total_steps > 0:
            self.completion_percentage = int((self.completed_steps / self.total_steps) * 100)
        
        # Auto-set completion date when status is completed
        if self.status == 'completed' and not self.actual_separation_date:
            self.actual_separation_date = timezone.now().date()
            self.completion_percentage = 100
        
        super().save(*args, **kwargs)


class TerminationStep(models.Model):
    """
    Individual steps within termination workflows
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='termination_steps'
    )
    termination = models.ForeignKey(
        Termination, 
        on_delete=models.CASCADE,
        related_name='termination_steps'
    )
    assigned_to = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_termination_steps'
    )
    approved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='approved_termination_steps'
    )
    
    # Step Details
    step_name = models.CharField(max_length=200)
    step_description = models.TextField()
    step_instructions = models.TextField(blank=True)
    
    # Step Classification
    step_category = models.CharField(
        max_length=50, 
        choices=[
            ('notification', 'Notification'),
            ('documentation', 'Documentation'),
            ('approval', 'Approval'),
            ('coordination', 'Coordination'),
            ('technical', 'Technical'),
            ('financial', 'Financial'),
            ('legal', 'Legal'),
            ('communication', 'Communication'),
            ('handover', 'Handover'),
            ('verification', 'Verification'),
            ('final_settlement', 'Final Settlement'),
        ]
    )
    step_type = models.CharField(
        max_length=50, 
        choices=[
            ('employee_notification', 'Employee Notification'),
            ('manager_notification', 'Manager Notification'),
            ('hr_notification', 'HR Notification'),
            ('it_notification', 'IT Notification'),
            ('finance_notification', 'Finance Notification'),
            ('legal_review', 'Legal Review'),
            ('management_approval', 'Management Approval'),
            ('document_collection', 'Document Collection'),
            ('access_revocation', 'Access Revocation'),
            ('asset_recovery', 'Asset Recovery'),
            ('final_payroll', 'Final Payroll'),
            ('benefits_cancellation', 'Benefits Cancellation'),
            ('exit_interview', 'Exit Interview'),
            ('reference_check', 'Reference Check'),
            ('system_deprovisioning', 'System Deprovisioning'),
            ('final_communication', 'Final Communication'),
        ]
    )
    
    # Assignment Information
    assigned_to_name = models.CharField(max_length=255, blank=True)
    assigned_to_role = models.CharField(max_length=100, blank=True)
    assigned_to_department = models.CharField(max_length=100, blank=True)
    
    # Status Management
    status = models.CharField(
        max_length=20, 
        choices=[
            ('pending', 'Pending'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('skipped', 'Skipped'),
            ('failed', 'Failed'),
            ('cancelled', 'Cancelled'),
            ('overdue', 'Overdue'),
        ], 
        default='pending'
    )
    
    # Priority and Dependencies
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
    depends_on_steps = models.JSONField(default=list, blank=True)
    
    # Timing Information
    due_date = models.DateField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    
    # Duration and Effort
    estimated_duration_hours = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    actual_duration_hours = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    
    # Requirements and Conditions
    is_mandatory = models.BooleanField(default=True)
    requires_approval = models.BooleanField(default=False)
    requires_documentation = models.BooleanField(default=False)
    requires_verification = models.BooleanField(default=False)
    
    # Completion Information
    completion_notes = models.TextField(blank=True)
    completion_method = models.CharField(
        max_length=50, 
        choices=[
            ('manual', 'Manual'),
            ('automated', 'Automated'),
            ('system_verified', 'System Verified'),
            ('self_service', 'Self Service'),
        ], 
        blank=True
    )
    
    # Attachments and Evidence
    required_documents = models.JSONField(default=list, blank=True)
    uploaded_documents = models.JSONField(default=list, blank=True)
    evidence_required = models.BooleanField(default=False)
    
    # Approval Information
    approval_comments = models.TextField(blank=True)
    
    # Notifications
    notification_sent = models.BooleanField(default=False)
    reminder_sent_count = models.IntegerField(default=0)
    last_reminder_date = models.DateTimeField(null=True, blank=True)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_termination_steps'
        verbose_name = 'Termination Step'
        verbose_name_plural = 'Termination Steps'
        indexes = [
            models.Index(fields=['company', 'termination'], name='idx_step_termination'),
            models.Index(fields=['company', 'assigned_to'], name='idx_step_assignee'),
            models.Index(fields=['company', 'status'], name='idx_step_status'),
        ]
        ordering = ['due_date', 'priority']
    
    def __str__(self):
        return f"Step: {self.step_name} - {self.termination}"
    
    def clean(self):
        """Validate termination step data"""
        # Validate due date logic
        if self.due_date and self.start_date:
            if self.due_date < self.start_date:
                raise ValidationError("Due date must be on or after start date")
        
        # Validate completion date logic
        if self.completed_date and self.start_date:
            if self.completed_date.date() < self.start_date:
                raise ValidationError("Completion date cannot be before start date")
        
        # Validate duration hours are positive
        duration_fields = ['estimated_duration_hours', 'actual_duration_hours']
        
        for field in duration_fields:
            value = getattr(self, field)
            if value is not None and value < 0:
                raise ValidationError(f"{field.replace('_', ' ').title()} cannot be negative")
        
        # Validate reminder count is non-negative
        if self.reminder_sent_count and self.reminder_sent_count < 0:
            raise ValidationError("Reminder sent count cannot be negative")
        
        # Validate last reminder date logic
        if self.last_reminder_date and self.last_reminder_date > timezone.now():
            raise ValidationError("Last reminder date cannot be in the future")
    
    def save(self, *args, **kwargs):
        """Auto-set completion date when status is completed"""
        if self.status == 'completed' and not self.completed_date:
            self.completed_date = timezone.now()
        
        super().save(*args, **kwargs)


class TerminationTemplate(models.Model):
    """
    Templates for standardized termination workflows
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='termination_templates'
    )
    approved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='approved_termination_templates'
    )
    
    # Template Details
    template_name = models.CharField(max_length=200)
    template_code = models.CharField(max_length=50)
    template_description = models.TextField(blank=True)
    
    # Template Classification
    template_type = models.CharField(
        max_length=50, 
        choices=[
            ('standard', 'Standard'),
            ('voluntary', 'Voluntary'),
            ('involuntary', 'Involuntary'),
            ('performance', 'Performance'),
            ('misconduct', 'Misconduct'),
            ('layoff', 'Layoff'),
            ('retirement', 'Retirement'),
            ('custom', 'Custom'),
        ]
    )
    applicable_termination_types = models.JSONField(default=list, blank=True)
    applicable_departments = models.JSONField(default=list, blank=True)
    applicable_positions = models.JSONField(default=list, blank=True)
    
    # Template Content
    step_templates = models.JSONField(default=list, blank=True)
    default_assignments = models.JSONField(default=dict, blank=True)
    default_timelines = models.JSONField(default=dict, blank=True)
    
    # Status and Usage
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    usage_count = models.IntegerField(default=0)
    
    # Version Control
    version_number = models.CharField(max_length=20, default='1.0')
    is_latest_version = models.BooleanField(default=True)
    
    # Approval Information
    approval_date = models.DateTimeField(null=True, blank=True)
    legal_review_date = models.DateTimeField(null=True, blank=True)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_termination_templates'
        verbose_name = 'Termination Template'
        verbose_name_plural = 'Termination Templates'
        indexes = [
            models.Index(fields=['company', 'template_type'], name='idx_template_type'),
            models.Index(fields=['company', 'is_active'], name='idx_template_active'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['company', 'template_code'], name='uk_template_code'),
        ]
        ordering = ['template_name']


# Reference Models (simplified versions - full implementations would be in separate files)

class TerminationDocument(models.Model):
    """
    Documents collected during termination process
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='termination_documents'
    )
    termination = models.ForeignKey(
        Termination, 
        on_delete=models.CASCADE,
        related_name='termination_documents'
    )
    document_name = models.CharField(max_length=255)
    document_type = models.CharField(max_length=100)
    document_url = models.URLField()
    
    class Meta:
        db_table = 'hr_termination_documents'
        verbose_name = 'Termination Document'
        verbose_name_plural = 'Termination Documents'


class TerminationCommunication(models.Model):
    """
    Communication records during termination process
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='termination_communications'
    )
    termination = models.ForeignKey(
        Termination, 
        on_delete=models.CASCADE,
        related_name='termination_communications'
    )
    communication_type = models.CharField(max_length=100)
    communication_date = models.DateTimeField(auto_now_add=True)
    recipient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='received_termination_communications'
    )
    subject = models.CharField(max_length=200)
    message_content = models.TextField()
    
    class Meta:
        db_table = 'hr_termination_communications'
        verbose_name = 'Termination Communication'
        verbose_name_plural = 'Termination Communications'
