"""
Profile View Models for HRM
Following BBP 02.3 Profile View specifications
Aligned with enterprise governance and Olivine UI canon
"""

import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class ProfileViewEmployee(models.Model):
    """
    Extended employee profile information for comprehensive profile management
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys - Using lazy string references per governance
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='employee_profiles'
    )
    employee = models.ForeignKey(
        'hrm.Employee', 
        on_delete=models.CASCADE,
        related_name='employee_profiles'
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='created_employee_profiles'
    )
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='updated_employee_profiles'
    )
    
    # Personal Information
    preferred_name = models.CharField(max_length=100, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    maiden_name = models.CharField(max_length=100, blank=True)
    nickname = models.CharField(max_length=50, blank=True)
    gender = models.CharField(
        max_length=20, 
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
            ('prefer_not_to_say', 'Prefer not to say'),
        ], 
        blank=True
    )
    date_of_birth = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=200, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    marital_status = models.CharField(
        max_length=20, 
        choices=[
            ('single', 'Single'),
            ('married', 'Married'),
            ('divorced', 'Divorced'),
            ('widowed', 'Widowed'),
            ('civil_partnership', 'Civil Partnership'),
        ], 
        blank=True
    )
    
    # Contact Information
    personal_email = models.EmailField(blank=True)
    personal_phone = models.CharField(max_length=50, blank=True)
    work_phone_extension = models.CharField(max_length=10, blank=True)
    
    # Address Information
    home_address_line_1 = models.CharField(max_length=500, blank=True)
    home_address_line_2 = models.CharField(max_length=500, blank=True)
    home_city = models.CharField(max_length=100, blank=True)
    home_state = models.CharField(max_length=100, blank=True)
    home_postal_code = models.CharField(max_length=20, blank=True)
    home_country = models.CharField(max_length=100, blank=True)
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True)
    emergency_contact_phone = models.CharField(max_length=50, blank=True)
    emergency_contact_email = models.EmailField(blank=True)
    
    # Profile Settings
    profile_visibility = models.CharField(
        max_length=20, 
        choices=[
            ('public', 'Public'),
            ('company', 'Company Only'),
            ('department', 'Department Only'),
            ('private', 'Private'),
        ], 
        default='company'
    )
    profile_photo_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    
    # Social Media
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    
    # Preferences
    preferred_language = models.CharField(max_length=10, default='en')
    timezone = models.CharField(max_length=50, default='UTC')
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_employee_profiles'
        verbose_name = 'Employee Profile'
        verbose_name_plural = 'Employee Profiles'
        indexes = [
            models.Index(fields=['company', 'employee'], name='idx_profile_employee'),
            models.Index(fields=['company', 'profile_visibility'], name='idx_profile_visibility'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['company', 'employee'], name='uk_profile_employee'),
        ]
    
    def __str__(self):
        return f"Profile - {self.employee}"
    
    def clean(self):
        """Validate employee profile data"""
        # Validate date of birth is not in future
        if self.date_of_birth and self.date_of_birth > timezone.now().date():
            raise ValidationError("Date of birth cannot be in the future")
        
        # Check minimum age (e.g., 16 years)
        if self.date_of_birth:
            age = timezone.now().date().year - self.date_of_birth.year
            min_age = 16
            if age < min_age:
                raise ValidationError(f"Employee must be at least {min_age} years old")
        
        # Validate emergency contact information
        if self.emergency_contact_name and not (self.emergency_contact_phone or self.emergency_contact_email):
            raise ValidationError("Emergency contact phone or email is required when contact name is provided")
        
        # Validate email format
        if self.personal_email and '@' not in self.personal_email:
            raise ValidationError("Personal email format is invalid")
        
        # Validate URL formats
        url_fields = ['profile_photo_url', 'linkedin_url', 'twitter_url']
        for field in url_fields:
            value = getattr(self, field)
            if value and not (value.startswith('http://') or value.startswith('https://')):
                raise ValidationError(f"{field.replace('_', ' ').title()} must start with http:// or https://")


class ProfileViewSkill(models.Model):
    """
    Employee skills and competencies tracking for profile view
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='employee_skills'
    )
    employee = models.ForeignKey(
        'hrm.Employee', 
        on_delete=models.CASCADE,
        related_name='employee_skills'
    )
    verified_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='verified_employee_skills'
    )
    
    # Skill Information
    skill_name = models.CharField(max_length=200)
    skill_category = models.CharField(max_length=100)
    proficiency_level = models.IntegerField(
        choices=[
            (1, 'Beginner'),
            (2, 'Novice'),
            (3, 'Intermediate'),
            (4, 'Advanced'),
            (5, 'Expert'),
        ]
    )
    years_experience = models.IntegerField(default=0)
    last_used = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    verified_date = models.DateField(null=True, blank=True)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_employee_skills'
        verbose_name = 'Employee Skill'
        verbose_name_plural = 'Employee Skills'
        indexes = [
            models.Index(fields=['company', 'employee'], name='idx_skill_employee'),
            models.Index(fields=['company', 'skill_category'], name='idx_skill_category'),
        ]
        ordering = ['skill_name']
    
    def __str__(self):
        return f"{self.skill_name} - {self.employee}"
    
    def clean(self):
        """Validate employee skill data"""
        # Validate proficiency level is within range
        if self.proficiency_level and (self.proficiency_level < 1 or self.proficiency_level > 5):
            raise ValidationError("Proficiency level must be between 1 and 5")
        
        # Validate years experience is non-negative
        if self.years_experience and self.years_experience < 0:
            raise ValidationError("Years of experience cannot be negative")
        
        # Validate last used date is not in future
        if self.last_used and self.last_used > timezone.now().date():
            raise ValidationError("Last used date cannot be in the future")
        
        # Validate verified date logic
        if self.verified_date and self.verified_date > timezone.now().date():
            raise ValidationError("Verified date cannot be in the future")


class ProfileViewDocument(models.Model):
    """
    Employee documents and attachments management for profile view
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Foreign Keys
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='employee_documents'
    )
    employee = models.ForeignKey(
        'hrm.Employee', 
        on_delete=models.CASCADE,
        related_name='employee_documents'
    )
    uploaded_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='uploaded_employee_documents'
    )
    
    # Document Information
    document_type = models.CharField(
        max_length=100, 
        choices=[
            ('resume', 'Resume'),
            ('contract', 'Contract'),
            ('offer_letter', 'Offer Letter'),
            ('id_proof', 'ID Proof'),
            ('passport', 'Passport'),
            ('visa', 'Visa'),
            ('work_permit', 'Work Permit'),
            ('certification', 'Certification'),
            ('education', 'Education'),
            ('training', 'Training'),
            ('performance', 'Performance Review'),
            ('other', 'Other'),
        ]
    )
    document_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file_url = models.URLField()
    file_size = models.BigIntegerField()
    file_type = models.CharField(max_length=100)
    upload_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)
    is_confidential = models.BooleanField(default=False)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_employee_documents'
        verbose_name = 'Employee Document'
        verbose_name_plural = 'Employee Documents'
        indexes = [
            models.Index(fields=['company', 'employee'], name='idx_doc_employee'),
            models.Index(fields=['company', 'document_type'], name='idx_doc_type'),
        ]
        ordering = ['-upload_date']
    
    def __str__(self):
        return f"{self.document_name} - {self.employee}"
    
    def clean(self):
        """Validate employee document data"""
        # Validate file size is positive
        if self.file_size and self.file_size < 0:
            raise ValidationError("File size cannot be negative")
        
        # Validate expiry date is not in past for new documents
        if self.expiry_date and self.expiry_date < timezone.now().date():
            if not self.pk:  # New document
                raise ValidationError("Expiry date cannot be in the past for new documents")
        
        # Validate file URL format
        if self.file_url and not (self.file_url.startswith('http://') or self.file_url.startswith('https://')):
            raise ValidationError("File URL must start with http:// or https://")


# Reference Models (simplified versions - full implementations would be in separate files)

class ProfileViewSkillCategory(models.Model):
    """
    Skill categories for classification for profile view
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        'domain.Company', 
        on_delete=models.CASCADE,
        related_name='skill_categories'
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    parent_category = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE,
        null=True, 
        blank=True,
        related_name='child_categories'
    )
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'hr_skill_categories'
        verbose_name = 'Skill Category'
        verbose_name_plural = 'Skill Categories'
