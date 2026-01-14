"""
Exit Checklist Models for HRM
Following BBP 11.1 Exit Checklist specifications
Aligned with enterprise governance and Olivine UI canon
"""

import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class ExitChecklist(models.Model):
    """
    Main exit checklist model for employee offboarding
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys - Using lazy string references per governance
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='exit_checklists'
    )
    employee = models.ForeignKey(
        'hrm.Employee', 
        on_delete=models.CASCADE,
        related_name='exit_checklists'
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='created_exit_checklists'
    )
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='updated_exit_checklists'
    )
    manager = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='managed_exit_checklists'
    )
    hr_assignee = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='hr_assigned_exit_checklists'
    )
    it_assignee = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='it_assigned_exit_checklists'
    )
    finance_assignee = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='finance_assigned_exit_checklists'
    )
    security_assignee = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='security_assigned_exit_checklists'
    )
    
    # Checklist Details
    checklist_number = models.CharField(max_length=50)
    checklist_name = models.CharField(max_length=200)
    checklist_description = models.TextField(blank=True)
    
    # Employee Information
    employee_name = models.CharField(max_length=255)
    employee_email = models.EmailField()
    employee_department = models.CharField(max_length=100)
    employee_position = models.CharField(max_length=200)
    
    # Separation Details
    separation_type = models.CharField(
        max_length=50, 
        choices=[
            ('resignation', 'Resignation'),
            ('termination', 'Termination'),
            ('retirement', 'Retirement'),
            ('contract_end', 'Contract End'),
            ('layoff', 'Layoff'),
            ('mutual_agreement', 'Mutual Agreement'),
            ('death', 'Death'),
            ('other', 'Other'),
        ]
    )
    separation_reason = models.CharField(max_length=200, blank=True)
    last_working_day = models.DateField()
    actual_separation_date = models.DateField(null=True, blank=True)
    
    # Status Management
    status = models.CharField(
        max_length=20, 
        choices=[
            ('initiated', 'Initiated'),
            ('in_progress', 'In Progress'),
            ('pending_review', 'Pending Review'),
            ('completed', 'Completed'),
            ('on_hold', 'On Hold'),
            ('cancelled', 'Cancelled'),
        ], 
        default='initiated'
    )
    
    # Progress Tracking
    total_tasks = models.IntegerField(default=0)
    completed_tasks = models.IntegerField(default=0)
    pending_tasks = models.IntegerField(default=0)
    overdue_tasks = models.IntegerField(default=0)
    completion_percentage = models.IntegerField(default=0)
    
    # Timeline Information
    initiated_date = models.DateTimeField(auto_now_add=True)
    target_completion_date = models.DateField()
    actual_completion_date = models.DateTimeField(null=True, blank=True)
    
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
    
    # Checklist Template
    checklist_template = models.ForeignKey(
        'hrm.ExitChecklistTemplate', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='template_checklists'
    )
    template_name = models.CharField(max_length=200, blank=True)
    
    # Additional Information
    special_instructions = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_exit_checklists'
        verbose_name = 'Exit Checklist'
        verbose_name_plural = 'Exit Checklists'
        indexes = [
            models.Index(fields=['company', 'employee'], name='idx_checklist_employee'),
            models.Index(fields=['company', 'status'], name='idx_checklist_status'),
            models.Index(fields=['company', 'last_working_day'], name='idx_checklist_lwd'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['company', 'checklist_number'], name='uk_checklist_number'),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Exit Checklist {self.checklist_number} - {self.employee_name}"
    
    def clean(self):
        """Validate exit checklist data"""
        # Validate last working day is not in past for new checklists
        if self.last_working_day and self.last_working_day < timezone.now().date():
            if not self.pk:  # New checklist
                raise ValidationError("Last working day cannot be in the past")
        
        # Validate target completion date logic
        if self.target_completion_date and self.last_working_day:
            if self.target_completion_date < self.last_working_day:
                raise ValidationError("Target completion date should be after last working day")
        
        # Validate actual separation date logic
        if self.actual_separation_date and self.last_working_day:
            if self.actual_separation_date < self.last_working_day:
                raise ValidationError("Actual separation date cannot be before last working day")
        
        # Validate completion percentage
        if self.total_tasks > 0:
            calculated_percentage = int((self.completed_tasks / self.total_tasks) * 100)
            if abs(calculated_percentage - self.completion_percentage) > 1:
                raise ValidationError("Completion percentage does not match task completion")
        
        # Validate task counts are non-negative
        task_fields = [
            'total_tasks', 'completed_tasks', 'pending_tasks', 'overdue_tasks'
        ]
        
        for field in task_fields:
            value = getattr(self, field)
            if value is not None and value < 0:
                raise ValidationError(f"{field.replace('_', ' ').title()} cannot be negative")
    
    def save(self, *args, **kwargs):
        """Auto-calculate progress percentage"""
        if self.total_tasks > 0:
            self.completion_percentage = int((self.completed_tasks / self.total_tasks) * 100)
        
        # Auto-set completion date when status is completed
        if self.status == 'completed' and not self.actual_completion_date:
            self.actual_completion_date = timezone.now()
            self.completion_percentage = 100
        
        super().save(*args, **kwargs)


class ExitChecklistTask(models.Model):
    """
    Individual tasks within exit checklists
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='exit_checklist_tasks'
    )
    exit_checklist = models.ForeignKey(
        ExitChecklist, 
        on_delete=models.CASCADE,
        related_name='exit_checklist_tasks'
    )
    assigned_to = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_exit_tasks'
    )
    approved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='approved_exit_tasks'
    )
    
    # Task Details
    task_name = models.CharField(max_length=200)
    task_description = models.TextField()
    task_instructions = models.TextField(blank=True)
    
    # Task Classification
    task_category = models.CharField(
        max_length=50, 
        choices=[
            ('hr_tasks', 'HR Tasks'),
            ('it_tasks', 'IT Tasks'),
            ('finance_tasks', 'Finance Tasks'),
            ('security_tasks', 'Security Tasks'),
            ('manager_tasks', 'Manager Tasks'),
            ('admin_tasks', 'Admin Tasks'),
            ('legal_tasks', 'Legal Tasks'),
            ('compliance_tasks', 'Compliance Tasks'),
            ('asset_tasks', 'Asset Tasks'),
            ('knowledge_transfer', 'Knowledge Transfer'),
        ]
    )
    task_type = models.CharField(
        max_length=50, 
        choices=[
            ('document_collection', 'Document Collection'),
            ('asset_return', 'Asset Return'),
            ('access_revocation', 'Access Revocation'),
            ('handover', 'Handover'),
            ('verification', 'Verification'),
            ('approval', 'Approval'),
            ('notification', 'Notification'),
            ('interview', 'Interview'),
            ('calculation', 'Calculation'),
            ('review', 'Review'),
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
            ('overdue', 'Overdue'),
            ('skipped', 'Skipped'),
            ('cancelled', 'Cancelled'),
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
    depends_on_tasks = models.JSONField(default=list, blank=True)
    
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
        db_table = 'hr_exit_checklist_tasks'
        verbose_name = 'Exit Checklist Task'
        verbose_name_plural = 'Exit Checklist Tasks'
        indexes = [
            models.Index(fields=['company', 'exit_checklist'], name='idx_task_checklist'),
            models.Index(fields=['company', 'assigned_to'], name='idx_task_assignee'),
            models.Index(fields=['company', 'status'], name='idx_task_status'),
        ]
        ordering = ['due_date', 'priority']
    
    def __str__(self):
        return f"Task: {self.task_name} - {self.exit_checklist}"
    
    def clean(self):
        """Validate exit checklist task data"""
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


class ExitChecklistTemplate(models.Model):
    """
    Templates for standardized exit checklists
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='exit_checklist_templates'
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
            ('role_specific', 'Role Specific'),
            ('department_specific', 'Department Specific'),
            ('separation_type', 'Separation Type'),
            ('urgency_based', 'Urgency Based'),
            ('custom', 'Custom'),
        ]
    )
    applicable_roles = models.JSONField(default=list, blank=True)
    applicable_departments = models.JSONField(default=list, blank=True)
    applicable_separation_types = models.JSONField(default=list, blank=True)
    
    # Template Content
    task_templates = models.JSONField(default=list, blank=True)
    default_assignments = models.JSONField(default=dict, blank=True)
    default_timelines = models.JSONField(default=dict, blank=True)
    
    # Status and Usage
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    usage_count = models.IntegerField(default=0)
    
    # Version Control
    version_number = models.CharField(max_length=20, default='1.0')
    is_latest_version = models.BooleanField(default=True)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_exit_checklist_templates'
        verbose_name = 'Exit Checklist Template'
        verbose_name_plural = 'Exit Checklist Templates'
        indexes = [
            models.Index(fields=['company', 'template_type'], name='idx_template_type'),
            models.Index(fields=['company', 'is_active'], name='idx_template_active'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['company', 'template_code'], name='uk_template_code'),
        ]
        ordering = ['template_name']


# Reference Models (simplified versions - full implementations would be in separate files)

class ExitDocument(models.Model):
    """
    Documents collected during exit process
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='exit_documents'
    )
    exit_checklist = models.ForeignKey(
        ExitChecklist, 
        on_delete=models.CASCADE,
        related_name='exit_documents'
    )
    document_name = models.CharField(max_length=255)
    document_type = models.CharField(max_length=100)
    document_url = models.URLField()
    
    class Meta:
        db_table = 'hr_exit_documents'
        verbose_name = 'Exit Document'
        verbose_name_plural = 'Exit Documents'


class ExitHandover(models.Model):
    """
    Knowledge and responsibility handover tracking
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='exit_handovers'
    )
    exit_checklist = models.ForeignKey(
        ExitChecklist, 
        on_delete=models.CASCADE,
        related_name='exit_handovers'
    )
    handover_type = models.CharField(max_length=100)
    handover_to = models.ForeignKey(
        'hrm.Employee', 
        on_delete=models.CASCADE,
        related_name='received_handovers'
    )
    handover_status = models.CharField(
        max_length=20, 
        choices=[
            ('pending', 'Pending'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ]
    )
    
    class Meta:
        db_table = 'hr_exit_handovers'
        verbose_name = 'Exit Handover'
        verbose_name_plural = 'Exit Handovers'
