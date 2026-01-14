"""
Profile View Models - Layer 3: Experience/Enrichment Layer
Human-centered employee profile with enrichment data
Aggregates data from Employee Records and Organizational Chart
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid

from .employee import EmployeeRecord
from .organizational_unit import OrganizationalUnit, Position

User = get_user_model()


class ProfileViewAccess(models.Model):
    """
    Track profile view access and permissions
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, related_name='profile_view_access_company')
    profile = models.ForeignKey('hrm.EmployeeProfile', on_delete=models.CASCADE, related_name='profile_view_access_profile')
    viewer = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='profile_view_access_viewer')
    access_level = models.CharField(
        max_length=20,
        choices=[
            ('SELF', 'Self'),
            ('MANAGER', 'Manager'),
            ('HR', 'HR'),
            ('ADMIN', 'Admin')
        ],
        default='SELF'
    )
    last_viewed = models.DateTimeField(null=True, blank=True)
    view_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_profile_view_access'
        verbose_name = 'Profile View Access'
        verbose_name_plural = 'Profile View Access'
        indexes = [
            models.Index(fields=['company', 'profile'], name='idx_profile_view_profile'),
            models.Index(fields=['company', 'viewer'], name='idx_profile_view_viewer'),
        ]
        unique_together = ['company', 'profile', 'viewer']
    
    def __str__(self):
        return f'{self.viewer.username} -> {self.profile.employee.first_name} {self.profile.employee.last_name}'


class ProfileEndorsement(models.Model):
    """
    Employee skill endorsements from colleagues
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, related_name='profile_endorsement_company')
    profile = models.ForeignKey('hrm.EmployeeProfile', on_delete=models.CASCADE, related_name='profile_endorsement_profile')
    skill = models.ForeignKey('hrm.EmployeeSkill', on_delete=models.CASCADE, related_name='profile_endorsement_skill')
    endorser = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='profile_endorsement_endorser')
    endorsement_level = models.IntegerField(choices=[
        (1, 'Basic'),
        (2, 'Intermediate'),
        (3, 'Advanced'),
        (4, 'Expert'),
        (5, 'Master'),
    ], default=1)
    endorsement_text = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='profile_endorsement_verified_by')
    verified_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_profile_endorsements'
        verbose_name = 'Profile Endorsement'
        verbose_name_plural = 'Profile Endorsements'
        indexes = [
            models.Index(fields=['company', 'profile', 'skill'], name='idx_endorsement_profile_skill'),
            models.Index(fields=['company', 'endorser'], name='idx_endorsement_endorser'),
            models.Index(fields=['company', 'is_verified'], name='idx_endorsement_verified'),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.endorser.username} endorses {self.profile.employee.first_name} for {self.skill.name}'


class ProfileViewSettings(models.Model):
    """
    Global profile view settings and configurations
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.OneToOneField('hrm.Company', on_delete=models.CASCADE, related_name='profile_view_settings_company')
    
    # Visibility Settings
    allow_public_profiles = models.BooleanField(default=False)
    allow_skill_endorsements = models.BooleanField(default=True)
    allow_profile_sharing = models.BooleanField(default=True)
    
    # Default Visibility Levels
    default_profile_visibility = models.CharField(
        max_length=20,
        choices=[
            ('private', 'Private - HR and managers only'),
            ('team', 'Team - Direct team members'),
            ('department', 'Department level'),
            ('company', 'Company level'),
            ('public', 'Public to all employees')
        ],
        default='private'
    )
    
    # Feature Flags
    enable_profile_analytics = models.BooleanField(default=True)
    enable_skill_gap_analysis = models.BooleanField(default=True)
    enable_career_pathing = models.BooleanField(default=True)
    
    # Notification Settings
    notify_profile_updates = models.BooleanField(default=True)
    notify_endorsements = models.BooleanField(default=True)
    notify_profile_views = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_profile_view_settings'
        verbose_name = 'Profile View Settings'
        verbose_name_plural = 'Profile View Settings'
    
    def __str__(self):
        return f'Profile View Settings for {self.company.name}'


# Validation methods
def clean_endorsement_level(self):
    """Validate endorsement level"""
    if self.endorsement_level < 1 or self.endorsement_level > 5:
        raise ValidationError("Endorsement level must be between 1 and 5")

def clean_profile_visibility(self):
    """Validate profile visibility settings"""
    valid_visibilities = ['private', 'team', 'department', 'company', 'public']
    if self.default_profile_visibility not in valid_visibilities:
        raise ValidationError("Profile visibility must be one of the predefined options")
