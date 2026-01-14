"""
Placeholder Company Model for Phase-3 Stabilization
Temporary replacement for domain.Company references
"""
import uuid
from django.db import models

class Company(models.Model):
    """
    Placeholder Company model to resolve domain.Company references
    Temporary solution for Phase-3 stabilization
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_companies'
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        ordering = ['name']

    def __str__(self):
        return self.name