"""
Department aggregate root - Canonical HRM model
Following governance: One file = One aggregate root
"""
import uuid
from django.db import models
from ..tenancy import DEFAULT_COMPANY_CODE

class Department(models.Model):
    """
    Department aggregate root - canonical department model
    All department-related data centers here
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_code = models.CharField(max_length=10, db_index=True, default=DEFAULT_COMPANY_CODE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    department_code = models.CharField(max_length=20, unique=True)
    parent_department = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='department_parent_department')
    manager = models.ForeignKey('hrm.EmployeeRecord', on_delete=models.SET_NULL, null=True, blank=True, related_name='department_manager')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'department'
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        unique_together = ['company_code', 'name']
        indexes = [models.Index(fields=['company_code', 'is_active'], name='idx_dept_company_active'), models.Index(fields=['department_code'], name='idx_dept_code'), models.Index(fields=['parent_department'], name='idx_parent_dept')]

    def __str__(self):
        return f'{self.name} ({self.department_code})'