"""
Shared domain models for the enterprise platform
Following governance: Shared models for cross-module use
"""
import uuid
from django.db import models


class Company(models.Model):
    """
    Company model - shared across all modules
    Canonical source for company information
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Company Information
    name = models.CharField(max_length=200, unique=True)
    legal_name = models.CharField(max_length=200, null=True, blank=True)
    registration_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    tax_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    
    # Contact Information
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'company'
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        indexes = [
            models.Index(fields=['is_active'], name='idx_company_active'),
            models.Index(fields=['registration_number'], name='idx_company_reg'),
        ]
    
    def __str__(self):
        return self.name
