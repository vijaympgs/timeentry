"""
Audit Trail Models for HRM Module
Following T1 Complex Master Template specifications for complete change tracking
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json


class AuditTrail(models.Model):
    """
    Comprehensive audit trail for all HRM data changes
    Tracks create, update, delete operations with full change details
    """
    
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('VIEW', 'View'),  # For sensitive data access
    ]
    
    # Core tracking fields
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)  # e.g., 'EmployeeRecord'
    model_id = models.CharField(max_length=50)     # Primary key of the record
    company_code = models.CharField(max_length=50, db_index=True)
    
    # User and session tracking
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    user_email = models.EmailField(max_length=254)  # Redundant for when user is deleted
    session_key = models.CharField(max_length=40, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    
    # Change tracking
    old_values = models.JSONField(null=True, blank=True)  # Before state
    new_values = models.JSONField(null=True, blank=True)  # After state
    changed_fields = models.JSONField(default=list)        # List of field names
    
    # Metadata
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    reason = models.TextField(null=True, blank=True)      # Optional reason for change
    batch_id = models.CharField(max_length=50, null=True, blank=True)  # For bulk operations
    
    class Meta:
        db_table = 'hrm_audit_trail'
        verbose_name = 'Audit Trail'
        verbose_name_plural = 'Audit Trails'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['model_name', 'model_id']),
            models.Index(fields=['company_code', 'timestamp']),
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['action', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.action} {self.model_name} {self.model_id} by {self.user_email} at {self.timestamp}"
    
    @classmethod
    def log_create(cls, model_instance, user, company_code, **kwargs):
        """Log a create operation"""
        return cls.objects.create(
            action='CREATE',
            model_name=model_instance.__class__.__name__,
            model_id=str(model_instance.pk),
            company_code=company_code,
            user=user,
            user_email=user.email if user else 'system',
            new_values=model_to_dict(model_instance),
            changed_fields=list(model_instance.__dict__.keys()),
            **kwargs
        )
    
    @classmethod
    def log_update(cls, model_instance, old_values, user, company_code, changed_fields=None, **kwargs):
        """Log an update operation"""
        new_values = model_to_dict(model_instance)
        if changed_fields is None:
            # Auto-detect changed fields
            changed_fields = []
            for field in old_values:
                if old_values[field] != new_values.get(field):
                    changed_fields.append(field)
        
        return cls.objects.create(
            action='UPDATE',
            model_name=model_instance.__class__.__name__,
            model_id=str(model_instance.pk),
            company_code=company_code,
            user=user,
            user_email=user.email if user else 'system',
            old_values=old_values,
            new_values=new_values,
            changed_fields=changed_fields,
            **kwargs
        )
    
    @classmethod
    def log_delete(cls, model_instance, user, company_code, **kwargs):
        """Log a delete operation"""
        return cls.objects.create(
            action='DELETE',
            model_name=model_instance.__class__.__name__,
            model_id=str(model_instance.pk),
            company_code=company_code,
            user=user,
            user_email=user.email if user else 'system',
            old_values=model_to_dict(model_instance),
            changed_fields=list(model_instance.__dict__.keys()),
            **kwargs
        )
    
    @classmethod
    def log_view(cls, model_instance, user, company_code, **kwargs):
        """Log a view operation for sensitive data"""
        return cls.objects.create(
            action='VIEW',
            model_name=model_instance.__class__.__name__,
            model_id=str(model_instance.pk),
            company_code=company_code,
            user=user,
            user_email=user.email if user else 'system',
            new_values={'viewed': True},
            changed_fields=['view_access'],
            **kwargs
        )


class AuditTrailConfiguration(models.Model):
    """
    Configuration for audit trail settings per model
    Allows fine-tuning what gets audited
    """
    
    model_name = models.CharField(max_length=100, unique=True)
    is_enabled = models.BooleanField(default=True)
    
    # What to track
    track_creates = models.BooleanField(default=True)
    track_updates = models.BooleanField(default=True)
    track_deletes = models.BooleanField(default=True)
    track_views = models.BooleanField(default=False)  # For sensitive models only
    
    # Field-level tracking
    tracked_fields = models.JSONField(default=list)  # Empty list = track all fields
    excluded_fields = models.JSONField(default=list)  # Fields to exclude from tracking
    
    # Retention policy
    retention_days = models.IntegerField(default=365)  # Keep for 1 year by default
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hrm_audit_config'
        verbose_name = 'Audit Configuration'
        verbose_name_plural = 'Audit Configurations'
    
    def __str__(self):
        return f"{self.model_name} - {'Enabled' if self.is_enabled else 'Disabled'}"


def model_to_dict(model_instance):
    """Convert model instance to dictionary, handling various field types"""
    result = {}
    for field in model_instance._meta.fields:
        field_name = field.name
        field_value = getattr(model_instance, field_name)
        
        # Handle different field types
        if field_value is None:
            result[field_name] = None
        elif isinstance(field_value, (models.Model, User)):
            # Foreign key - store the ID and string representation
            result[field_name] = {
                'id': field_value.pk,
                'str': str(field_value)
            }
        elif hasattr(field_value, 'isoformat'):  # DateTime, Date, Time
            result[field_name] = field_value.isoformat()
        elif isinstance(field_value, (list, dict)):  # JSONField
            result[field_name] = field_value
        else:
            result[field_name] = str(field_value)
    
    return result


# Audit trail middleware for automatic logging
class AuditTrailMiddleware:
    """Middleware to capture request context for audit trails"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Store request context for audit logging
        request.audit_context = {
            'ip_address': self.get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'session_key': request.session.session_key if hasattr(request, 'session') else None,
        }
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """Get client IP address considering proxies"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
