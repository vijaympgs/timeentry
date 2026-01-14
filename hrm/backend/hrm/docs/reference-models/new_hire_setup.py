"""
New Hire Setup Models for HRM
Following BBP 03.5 New Hire Setup specifications
Aligned with enterprise governance and Olivine UI canon
"""

import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class OnboardingProcess(models.Model):
    """
    Main onboarding process model for managing new hire setup
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys - Using lazy string references per governance
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='onboarding_processes'
    )
    employee = models.ForeignKey(
        'hrm.Employee', 
        on_delete=models.CASCADE,
        related_name='onboarding_processes'
    )
    job_posting = models.ForeignKey(
        'hrm.JobPosting', 
        on_delete=models.CASCADE,
        related_name='onboarding_processes'
    )
    offer = models.ForeignKey(
        'hrm.OfferManagement', 
        on_delete=models.CASCADE,
        related_name='onboarding_processes'
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='created_onboarding_processes'
    )
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='updated_onboarding_processes'
    )
    
    # Process Details
    onboarding_number = models.CharField(max_length=50)
    start_date = models.DateField()
    onboarding_type = models.CharField(
        max_length=50, 
        choices=[
            ('standard', 'Standard Onboarding'),
            ('expedited', 'Expedited Onboarding'),
            ('remote', 'Remote Onboarding'),
            ('international', 'International Onboarding'),
            ('executive', 'Executive Onboarding'),
            ('intern', 'Intern Onboarding'),
            ('contractor', 'Contractor Onboarding'),
        ], 
        default='standard'
    )
    
    # Status Management
    status = models.CharField(
        max_length=50, 
        choices=[
            ('initiated', 'Initiated'),
            ('in_progress', 'In Progress'),
            ('pending_documents', 'Pending Documents'),
            ('pending_setup', 'Pending Setup'),
            ('ready', 'Ready for Start'),
            ('active', 'Active'),
            ('completed', 'Completed'),
            ('on_hold', 'On Hold'),
            ('cancelled', 'Cancelled'),
        ], 
        default='initiated'
    )
    
    # Timeline Management
    process_start_date = models.DateTimeField(auto_now_add=True)
    target_completion_date = models.DateField()
    actual_completion_date = models.DateField(null=True, blank=True)
    
    # Progress Tracking
    total_tasks = models.IntegerField(default=0)
    completed_tasks = models.IntegerField(default=0)
    progress_percentage = models.IntegerField(default=0)
    
    # Team Assignment
    hr_coordinator = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='coordinated_onboarding'
    )
    hiring_manager = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='managed_onboarding'
    )
    it_coordinator = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='it_onboarding'
    )
    buddy = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='buddy_onboarding'
    )
    
    # Onboarding Settings
    send_welcome_email = models.BooleanField(default=True)
    enable_self_service = models.BooleanField(default=True)
    require_document_upload = models.BooleanField(default=True)
    
    # Special Requirements
    special_requirements = models.TextField(blank=True)
    accessibility_needs = models.TextField(blank=True)
    equipment_requests = models.JSONField(default=list, blank=True)
    
    # Compliance and Audit
    compliance_checklist_completed = models.BooleanField(default=False)
    background_check_completed = models.BooleanField(default=False)
    drug_test_completed = models.BooleanField(default=False)
    
    # Notes
    onboarding_notes = models.TextField(blank=True)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_onboarding_processes'
        verbose_name = 'Onboarding Process'
        verbose_name_plural = 'Onboarding Processes'
        indexes = [
            models.Index(fields=['company', 'employee'], name='idx_onboarding_employee'),
            models.Index(fields=['company', 'status'], name='idx_onboarding_status'),
            models.Index(fields=['company', 'start_date'], name='idx_onboarding_start_date'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['company', 'onboarding_number'], name='uk_onboarding_number'),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Onboarding {self.onboarding_number} - {self.employee}"
    
    def clean(self):
        """Validate onboarding process data"""
        # Validate start date is not in past for new processes
        if self.start_date and self.start_date < timezone.now().date():
            if not self.pk:  # New onboarding process
                raise ValidationError("Start date cannot be in the past")
        
        # Validate progress percentage is within valid range
        if self.progress_percentage is not None and (self.progress_percentage < 0 or self.progress_percentage > 100):
            raise ValidationError("Progress percentage must be between 0 and 100")
        
        # Validate task counts are non-negative
        if self.total_tasks and self.total_tasks < 0:
            raise ValidationError("Total tasks cannot be negative")
        
        if self.completed_tasks and self.completed_tasks < 0:
            raise ValidationError("Completed tasks cannot be negative")
        
        # Validate target completion date logic
        if self.target_completion_date and self.start_date:
            if self.target_completion_date < self.start_date:
                raise ValidationError("Target completion date must be after start date")
        
        # Validate actual completion date logic
        if self.actual_completion_date and self.start_date:
            if self.actual_completion_date < self.start_date:
                raise ValidationError("Actual completion date cannot be before start date")
    
    def save(self, *args, **kwargs):
        """Auto-calculate progress percentage"""
        if self.total_tasks > 0:
            self.progress_percentage = int((self.completed_tasks / self.total_tasks) * 100)
        
        # Auto-set completion date when status is completed
        if self.status == 'completed' and not self.actual_completion_date:
            self.actual_completion_date = timezone.now().date()
            self.progress_percentage = 100
        
        super().save(*args, **kwargs)


class OnboardingTask(models.Model):
    """
    Individual tasks within the onboarding process
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='onboarding_tasks'
    )
    onboarding_process = models.ForeignKey(
        OnboardingProcess, 
        on_delete=models.CASCADE,
        related_name='onboarding_tasks'
    )
    assigned_to = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_onboarding_tasks'
    )
    completed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='completed_onboarding_tasks'
    )
    
    # Task Details
    task_name = models.CharField(max_length=200)
    task_description = models.TextField(blank=True)
    task_category = models.CharField(
        max_length=50, 
        choices=[
            ('hr', 'HR Tasks'),
            ('it', 'IT Tasks'),
            ('facilities', 'Facilities Tasks'),
            ('finance', 'Finance Tasks'),
            ('compliance', 'Compliance Tasks'),
            ('training', 'Training Tasks'),
            ('documentation', 'Documentation Tasks'),
            ('equipment', 'Equipment Tasks'),
            ('orientation', 'Orientation Tasks'),
        ]
    )
    
    # Assignment and Responsibility
    assigned_to_role = models.CharField(
        max_length=100, 
        choices=[
            ('hr_coordinator', 'HR Coordinator'),
            ('hiring_manager', 'Hiring Manager'),
            ('it_coordinator', 'IT Coordinator'),
            ('facilities_coordinator', 'Facilities Coordinator'),
            ('payroll_coordinator', 'Payroll Coordinator'),
            ('new_hire', 'New Hire'),
            ('buddy', 'Buddy/Mentor'),
        ]
    )
    
    # Status and Timing
    status = models.CharField(
        max_length=50, 
        choices=[
            ('pending', 'Pending'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('overdue', 'Overdue'),
            ('cancelled', 'Cancelled'),
        ], 
        default='pending'
    )
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
    due_date = models.DateTimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    
    # Task Configuration
    is_required = models.BooleanField(default=True)
    is_prerequisite = models.BooleanField(default=False)
    auto_assign = models.BooleanField(default=True)
    
    # Dependencies
    depends_on_tasks = models.JSONField(default=list, blank=True)
    blocks_tasks = models.JSONField(default=list, blank=True)
    
    # Completion Details
    completion_notes = models.TextField(blank=True)
    
    # Attachments and Links
    required_documents = models.JSONField(default=list, blank=True)
    task_instructions = models.TextField(blank=True)
    external_links = models.JSONField(default=list, blank=True)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_onboarding_tasks'
        verbose_name = 'Onboarding Task'
        verbose_name_plural = 'Onboarding Tasks'
        indexes = [
            models.Index(fields=['company', 'onboarding_process'], name='idx_task_process'),
            models.Index(fields=['company', 'assigned_to'], name='idx_task_assignee'),
            models.Index(fields=['company', 'status'], name='idx_task_status'),
        ]
        ordering = ['due_date', 'priority']
    
    def __str__(self):
        return f"Task: {self.task_name} - {self.onboarding_process}"
    
    def clean(self):
        """Validate onboarding task data"""
        # Validate due date logic
        if self.due_date and self.due_date < timezone.now():
            if self.status == 'pending':
                raise ValidationError("Due date cannot be in the past for pending tasks")
        
        # Validate completion date logic
        if self.completed_date and self.due_date:
            if self.completed_date < self.due_date:
                # This is allowed but might indicate overdue completion
                pass
        
        # Validate completion date is not in future
        if self.completed_date and self.completed_date > timezone.now():
            raise ValidationError("Completion date cannot be in the future")
    
    def save(self, *args, **kwargs):
        """Auto-set completion date when status is completed"""
        if self.status == 'completed' and not self.completed_date:
            self.completed_date = timezone.now()
        
        super().save(*args, **kwargs)


class OnboardingDocument(models.Model):
    """
    Documents collected during onboarding process
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='onboarding_documents'
    )
    onboarding_process = models.ForeignKey(
        OnboardingProcess, 
        on_delete=models.CASCADE,
        related_name='onboarding_documents'
    )
    employee = models.ForeignKey(
        'hrm.Employee', 
        on_delete=models.CASCADE,
        related_name='onboarding_documents'
    )
    uploaded_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='uploaded_onboarding_documents'
    )
    verified_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='verified_onboarding_documents'
    )
    
    # Document Details
    document_type = models.CharField(
        max_length=100, 
        choices=[
            ('id_proof', 'ID Proof'),
            ('passport', 'Passport'),
            ('visa', 'Visa'),
            ('work_permit', 'Work Permit'),
            ('tax_form', 'Tax Form'),
            ('bank_details', 'Bank Details'),
            ('emergency_contact', 'Emergency Contact'),
            ('medical_form', 'Medical Form'),
            ('nda', 'Non-Disclosure Agreement'),
            ('employment_contract', 'Employment Contract'),
            ('policy_acknowledgment', 'Policy Acknowledgment'),
            ('beneficiary_form', 'Beneficiary Form'),
            ('direct_deposit', 'Direct Deposit Form'),
            ('i9', 'I-9 Form'),
            ('w4', 'W-4 Form'),
            ('other', 'Other'),
        ]
    )
    document_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # File Information
    file_url = models.URLField()
    file_size = models.BigIntegerField()
    file_type = models.CharField(max_length=100)
    file_hash = models.CharField(max_length=256, blank=True)
    
    # Status and Verification
    status = models.CharField(
        max_length=50, 
        choices=[
            ('uploaded', 'Uploaded'),
            ('pending_review', 'Pending Review'),
            ('verified', 'Verified'),
            ('rejected', 'Rejected'),
            ('expired', 'Expired'),
        ], 
        default='uploaded'
    )
    verification_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    # Expiry and Renewal
    expiry_date = models.DateField(null=True, blank=True)
    reminder_sent = models.BooleanField(default=False)
    
    # Compliance and Security
    is_confidential = models.BooleanField(default=False)
    access_level = models.CharField(
        max_length=50, 
        choices=[
            ('public', 'Public'),
            ('hr_only', 'HR Only'),
            ('manager', 'Manager'),
            ('restricted', 'Restricted'),
        ], 
        default='hr_only'
    )
    
    # Upload Details
    upload_source = models.CharField(
        max_length=50, 
        choices=[
            ('employee_portal', 'Employee Portal'),
            ('hr_upload', 'HR Upload'),
            ('email_attachment', 'Email Attachment'),
            ('scan', 'Scan'),
        ], 
        default='employee_portal'
    )
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_onboarding_documents'
        verbose_name = 'Onboarding Document'
        verbose_name_plural = 'Onboarding Documents'
        indexes = [
            models.Index(fields=['company', 'onboarding_process'], name='idx_doc_process'),
            models.Index(fields=['company', 'document_type'], name='idx_doc_type'),
            models.Index(fields=['company', 'status'], name='idx_doc_status'),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Document: {self.document_name} - {self.employee}"
    
    def clean(self):
        """Validate onboarding document data"""
        # Validate file size is positive
        if self.file_size and self.file_size < 0:
            raise ValidationError("File size cannot be negative")
        
        # Validate expiry date logic
        if self.expiry_date and self.expiry_date < timezone.now().date():
            if self.status != 'expired':
                raise ValidationError("Expiry date cannot be in the past for non-expired documents")
        
        # Validate verification date logic
        if self.verification_date and self.verification_date > timezone.now():
            raise ValidationError("Verification date cannot be in the future")
        
        # Validate file URL format
        if self.file_url and not (self.file_url.startswith('http://') or self.file_url.startswith('https://')):
            raise ValidationError("File URL must start with http:// or https://")


# Reference Models (simplified versions - full implementations would be in separate files)

class OnboardingTemplate(models.Model):
    """
    Reusable onboarding templates for different employee types
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='onboarding_templates'
    )
    template_name = models.CharField(max_length=200)
    employee_category = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    task_config = models.JSONField(default=dict)
    document_requirements = models.JSONField(default=list)
    timeline_config = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'hr_onboarding_templates'
        verbose_name = 'Onboarding Template'
        verbose_name_plural = 'Onboarding Templates'


class OnboardingChecklist(models.Model):
    """
    Standard onboarding checklists
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='onboarding_checklists'
    )
    checklist_name = models.CharField(max_length=200)
    checklist_category = models.CharField(max_length=100)
    items = models.JSONField(default=list)
    is_mandatory = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'hr_onboarding_checklists'
        verbose_name = 'Onboarding Checklist'
        verbose_name_plural = 'Onboarding Checklists'
