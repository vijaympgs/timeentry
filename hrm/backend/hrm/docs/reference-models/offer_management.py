"""
Offer Management Models for HRM
Following BBP 03.4 Offer Management specifications
Aligned with enterprise governance and Olivine UI canon
"""

import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class OfferManagement(models.Model):
    """
    Central model for managing job offers throughout the recruitment process
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys - Using lazy string references per governance
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='offer_management'
    )
    candidate = models.ForeignKey(
        'hrm.Candidate', 
        on_delete=models.CASCADE,
        related_name='offer_management'
    )
    position = models.ForeignKey(
        'hrm.Position', 
        on_delete=models.CASCADE,
        related_name='offer_management'
    )
    hiring_manager = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='managed_offers'
    )
    recruiter = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='recruited_offers'
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='created_offers'
    )
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='updated_offers'
    )
    
    # Core Offer Information
    offer_number = models.CharField(max_length=50)
    offer_type = models.CharField(
        max_length=20, 
        choices=[
            ('verbal', 'Verbal Offer'),
            ('written', 'Written Offer'),
            ('revised', 'Revised Offer'),
            ('contingent', 'Contingent Offer'),
        ]
    )
    
    # Status Management
    status = models.CharField(
        max_length=20, 
        choices=[
            ('draft', 'Draft'),
            ('pending_approval', 'Pending Approval'),
            ('sent', 'Sent to Candidate'),
            ('under_review', 'Under Review'),
            ('accepted', 'Accepted'),
            ('declined', 'Declined'),
            ('expired', 'Expired'),
            ('withdrawn', 'Withdrawn'),
            ('revoked', 'Revoked'),
        ], 
        default='draft'
    )
    
    # Position Details
    position_title = models.CharField(max_length=200)
    contract_type = models.CharField(
        max_length=50, 
        choices=[
            ('permanent', 'Permanent'),
            ('fixed_term', 'Fixed Term'),
            ('contract', 'Contract'),
            ('internship', 'Internship'),
            ('part_time', 'Part Time'),
            ('temporary', 'Temporary'),
        ]
    )
    department = models.CharField(max_length=100)
    work_location = models.CharField(max_length=200)
    reporting_to = models.CharField(max_length=200)
    
    # Compensation Details
    salary_grade = models.CharField(max_length=50)
    proposed_salary = models.DecimalField(max_digits=12, decimal_places=2)
    salary_currency = models.CharField(max_length=3, default='USD')
    salary_frequency = models.CharField(
        max_length=20, 
        choices=[
            ('annual', 'Annual'),
            ('monthly', 'Monthly'),
            ('hourly', 'Hourly'),
            ('weekly', 'Weekly'),
        ]
    )
    bonus_eligible = models.BooleanField(default=False)
    bonus_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    
    # Offer Timeline
    expected_commencement_date = models.DateField()
    offer_sent_date = models.DateField(null=True, blank=True)
    response_deadline = models.DateField(null=True, blank=True)
    candidate_response_date = models.DateField(null=True, blank=True)
    
    # Workflow Management
    workflow_instance_id = models.CharField(max_length=100, null=True, blank=True)
    current_workflow_step = models.CharField(max_length=100, null=True, blank=True)
    workflow_status = models.CharField(max_length=20, default='ACTIVE')
    
    # Notes and Communication
    offer_notes = models.TextField(blank=True)
    candidate_notes = models.TextField(blank=True)
    internal_notes = models.TextField(blank=True)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_offer_management'
        verbose_name = 'Offer Management'
        verbose_name_plural = 'Offer Management'
        indexes = [
            models.Index(fields=['company', 'status'], name='idx_company_status'),
            models.Index(fields=['candidate', 'status'], name='idx_candidate_status'),
            models.Index(fields=['position', 'status'], name='idx_position_status'),
            models.Index(fields=['offer_sent_date'], name='idx_sent_date'),
            models.Index(fields=['expected_commencement_date'], name='idx_commencement'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['company', 'offer_number'], name='uk_company_offer'),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Offer {self.offer_number} - {self.candidate}"
    
    def clean(self):
        """Validate offer management data"""
        # Validate offer dates
        if self.offer_sent_date and self.response_deadline:
            if self.offer_sent_date >= self.response_deadline:
                raise ValidationError("Response deadline must be after offer sent date")
        
        if self.expected_commencement_date and self.expected_commencement_date < timezone.now().date():
            raise ValidationError("Expected commencement date cannot be in the past")
        
        # Validate salary is positive
        if self.proposed_salary and self.proposed_salary < 0:
            raise ValidationError("Proposed salary cannot be negative")
        
        # Validate bonus amount is positive if provided
        if self.bonus_amount and self.bonus_amount < 0:
            raise ValidationError("Bonus amount cannot be negative")
        
        # Validate currency code
        if self.salary_currency and len(self.salary_currency) != 3:
            raise ValidationError("Currency code must be 3 characters (ISO 4217)")
        
        # Validate response deadline is reasonable
        if self.response_deadline and self.offer_sent_date:
            max_deadline_days = 30  # Company policy
            deadline_diff = (self.response_deadline - self.offer_sent_date).days
            if deadline_diff > max_deadline_days:
                raise ValidationError(f"Response deadline cannot be more than {max_deadline_days} days from offer sent date")
        
        # Validate workflow status
        valid_statuses = ['ACTIVE', 'COMPLETED', 'CANCELLED', 'FAILED']
        if self.workflow_status and self.workflow_status not in valid_statuses:
            raise ValidationError(f"Invalid workflow status: {self.workflow_status}")
    
    def get_salary_range_for_grade(self, grade):
        """Get salary range for salary grade"""
        # This would typically integrate with compensation bands
        salary_ranges = {
            'G1': (30000, 45000),
            'G2': (40000, 60000),
            'G3': (50000, 75000),
            'G4': (65000, 95000),
            'G5': (80000, 120000),
        }
        return salary_ranges.get(grade, (0, 999999))


class OfferApproval(models.Model):
    """
    Manages the approval workflow for job offers
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='offer_approvals'
    )
    offer = models.ForeignKey(
        OfferManagement, 
        on_delete=models.CASCADE,
        related_name='offer_approvals'
    )
    approver = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='offer_approvals'
    )
    
    # Approval Details
    approval_level = models.IntegerField()
    approval_status = models.CharField(
        max_length=20, 
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('delegated', 'Delegated'),
        ], 
        default='pending'
    )
    approval_comments = models.TextField(null=True, blank=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_offer_approvals'
        verbose_name = 'Offer Approval'
        verbose_name_plural = 'Offer Approvals'
        indexes = [
            models.Index(fields=['offer', 'approval_level'], name='idx_offer_level'),
            models.Index(fields=['approver', 'approval_status'], name='idx_approver_status'),
        ]
        ordering = ['approval_level', '-created_at']
    
    def __str__(self):
        return f"Approval Level {self.approval_level} - {self.offer}"
    
    def clean(self):
        """Validate offer approval data"""
        # Validate approval level is positive
        if self.approval_level and self.approval_level < 1:
            raise ValidationError("Approval level must be at least 1")
        
        # Validate approval date logic
        if self.approval_date and self.approval_date > timezone.now():
            raise ValidationError("Approval date cannot be in the future")


class OfferManagementTemplate(models.Model):
    """
    Template for generating offer letters in offer management
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='offer_letter_templates'
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='created_offer_templates'
    )
    
    # Template Details
    template_name = models.CharField(max_length=200)
    template_type = models.CharField(
        max_length=50, 
        choices=[
            ('standard', 'Standard Offer'),
            ('executive', 'Executive Offer'),
            ('international', 'International Offer'),
            ('contingent', 'Contingent Offer'),
            ('internship', 'Internship Offer'),
        ]
    )
    template_content = models.TextField()
    template_variables = models.JSONField(default=dict)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_offer_letter_templates'
        verbose_name = 'Offer Letter Template'
        verbose_name_plural = 'Offer Letter Templates'
        indexes = [
            models.Index(fields=['company', 'template_type'], name='idx_company_type'),
            models.Index(fields=['is_active'], name='idx_active'),
        ]
        ordering = ['template_name']


class OfferStatusHistory(models.Model):
    """
    Tracks the history of status changes for offers
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='offer_status_history'
    )
    offer = models.ForeignKey(
        OfferManagement, 
        on_delete=models.CASCADE,
        related_name='offer_status_history'
    )
    changed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='offer_status_changes'
    )
    
    # Status Change Details
    previous_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    status_change_reason = models.TextField(null=True, blank=True)
    status_change_date = models.DateTimeField(auto_now_add=True)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_offer_status_history'
        verbose_name = 'Offer Status History'
        verbose_name_plural = 'Offer Status History'
        indexes = [
            models.Index(fields=['offer', 'status_change_date'], name='idx_offer_date'),
        ]
        ordering = ['-status_change_date']


# Reference Models (simplified versions - full implementations would be in separate files)

class OfferManagementPosition(models.Model):
    """
    Position reference model for offers
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='offer_positions'
    )
    position_name = models.CharField(max_length=200)
    position_code = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    job_family = models.CharField(max_length=100)
    employment_type = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'hr_offer_positions'
        verbose_name = 'Offer Position'
        verbose_name_plural = 'Offer Positions'


class OfferManagementCandidate(models.Model):
    """
    Candidate reference model for offers
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='offer_candidates'
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'hr_offer_candidates'
        verbose_name = 'Offer Candidate'
        verbose_name_plural = 'Offer Candidates'
