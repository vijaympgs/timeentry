"""Employee Profile aggregate root - Canonical HRM modelFollowing governance: One file = One aggregate root"""
import uuid
from django.db import models
from ..tenancy import DEFAULT_COMPANY_CODE

class EmployeeProfile(models.Model):
    """
    Extended employee profile information for comprehensive profile management
    Canonical Employee Profile aggregate - all profile-related data centers here
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_code = models.CharField(max_length=10, db_index=True, default=DEFAULT_COMPANY_CODE)
    employee = models.OneToOneField('hrm.EmployeeRecord', on_delete=models.CASCADE, related_name='employeeprofile_employee')
    created_by_user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='employeeprofile_created_by_user')
    updated_by_user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='employeeprofile_updated_by_user')
    preferred_name = models.CharField(max_length=100, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    maiden_name = models.CharField(max_length=100, blank=True)
    nickname = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=20, choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('NON_BINARY', 'Non-Binary'), ('PREFER_NOT_TO_SAY', 'Prefer not to say')], blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=200, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    marital_status = models.CharField(max_length=20, choices=[('SINGLE', 'Single'), ('MARRIED', 'Married'), ('DIVORCED', 'Divorced'), ('WIDOWED', 'Widowed'), ('CIVIL_PARTNERSHIP', 'Civil Partnership')], blank=True)
    personal_email = models.EmailField(blank=True)
    personal_phone = models.CharField(max_length=50, blank=True)
    work_phone_extension = models.CharField(max_length=10, blank=True)
    home_address_line_1 = models.CharField(max_length=500, blank=True)
    home_address_line_2 = models.CharField(max_length=500, blank=True)
    home_city = models.CharField(max_length=100, blank=True)
    home_state = models.CharField(max_length=100, blank=True)
    home_postal_code = models.CharField(max_length=20, blank=True)
    home_country = models.CharField(max_length=100, blank=True)
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True)
    emergency_contact_phone = models.CharField(max_length=50, blank=True)
    emergency_contact_email = models.EmailField(blank=True)
    profile_visibility = models.CharField(max_length=20, choices=[('PUBLIC', 'Public'), ('COMPANY', 'Company Only'), ('DEPARTMENT', 'Department Only'), ('PRIVATE', 'Private')], default='COMPANY')
    profile_photo_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    preferred_language = models.CharField(max_length=10, default='en')
    timezone = models.CharField(max_length=50, default='UTC')
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'employee_profile'
        verbose_name = 'Employee Profile'
        verbose_name_plural = 'Employee Profiles'
        indexes = [models.Index(fields=['company_code', 'employee'], name='idx_profile_employee'), models.Index(fields=['company_code', 'profile_visibility'], name='idx_profile_visibility'), models.Index(fields=['employee', 'is_active'], name='idx_employee_active')]
        constraints = [models.UniqueConstraint(fields=['company_code', 'employee'], name='uk_profile_employee')]

    def __str__(self):
        return f'Profile: {self.employee.first_name} {self.employee.last_name}'

class EmployeeSkill(models.Model):
    """
    Employee skills and competencies tracking
    Supporting model for Employee Profile aggregate
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_code = models.CharField(max_length=10, db_index=True, default=DEFAULT_COMPANY_CODE)
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name='employeeskill_employee')
    verified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='employeeskill_verified_by')
    skill_name = models.CharField(max_length=200)
    skill_category = models.CharField(max_length=100)
    proficiency_level = models.IntegerField(choices=[(1, 'Beginner'), (2, 'Novice'), (3, 'Intermediate'), (4, 'Advanced'), (5, 'Expert')])
    years_experience = models.IntegerField(default=0)
    last_used = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    verified_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'employee_skill'
        verbose_name = 'Employee Skill'
        verbose_name_plural = 'Employee Skills'
        indexes = [models.Index(fields=['company_code', 'employee'], name='idx_skill_employee'), models.Index(fields=['company_code', 'skill_category'], name='idx_skill_category'), models.Index(fields=['employee', 'is_active'], name='idx_skill_active')]

    def __str__(self):
        return f'{self.employee.employee.first_name} - {self.skill_name}'

class EmployeeDocument(models.Model):
    """
    Employee documents and attachments management
    Supporting model for Employee Profile aggregate
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_code = models.CharField(max_length=10, db_index=True, default=DEFAULT_COMPANY_CODE)
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name='employeedocument_employee')
    uploaded_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='employeedocument_uploaded_by')
    document_type = models.CharField(max_length=100, choices=[('RESUME', 'Resume'), ('CONTRACT', 'Contract'), ('OFFER_LETTER', 'Offer Letter'), ('ID_PROOF', 'ID Proof'), ('PASSPORT', 'Passport'), ('VISA', 'Visa'), ('WORK_PERMIT', 'Work Permit'), ('CERTIFICATION', 'Certification'), ('EDUCATION', 'Education'), ('TRAINING', 'Training'), ('PERFORMANCE', 'Performance Review'), ('OTHER', 'Other')])
    document_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file_url = models.URLField()
    file_size = models.BigIntegerField()
    file_type = models.CharField(max_length=100)
    upload_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)
    is_confidential = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'employee_document'
        verbose_name = 'Employee Document'
        verbose_name_plural = 'Employee Documents'
        indexes = [models.Index(fields=['company_code', 'employee'], name='idx_doc_employee'), models.Index(fields=['company_code', 'document_type'], name='idx_app_doc_type_emp'), models.Index(fields=['employee', 'is_active'], name='idx_doc_active')]

    def __str__(self):
        return f'{self.employee.employee.first_name} - {self.document_name}'

class SkillCategory(models.Model):
    """
    Skill categories for classification
    Reference model for Employee Skills
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_code = models.CharField(max_length=10, db_index=True, default=DEFAULT_COMPANY_CODE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='skillcategory_parent_category')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'skill_category'
        verbose_name = 'Skill Category'
        verbose_name_plural = 'Skill Categories'
        indexes = [models.Index(fields=['company_code', 'is_active'], name='idx_skill_cat_active'), models.Index(fields=['parent_category'], name='idx_parent_category')]
        unique_together = ['company_code', 'name']

    def __str__(self):
        return self.name