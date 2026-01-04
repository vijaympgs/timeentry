"""Organizational Unit Model - HRM DomainFollowing platform.cline governance - Domain Ownership: HRM → OrganizationalUnit/Position/EmployeePosition"""
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from ..tenancy import DEFAULT_COMPANY_CODE


class OrganizationalUnit(models.Model):
    """
    Represents an organizational unit (department, division, team, etc.)
    in the company structure with hierarchical relationships
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Canonical Tenancy Field
    company_code = models.CharField(
        max_length=10,
        db_index=True,
        default=DEFAULT_COMPANY_CODE
    )
    created_by_user_id = models.UUIDField()
    updated_by_user_id = models.UUIDField(null=True, blank=True)
    parent_unit_id = models.UUIDField(null=True, blank=True)
    manager_id = models.UUIDField(null=True, blank=True)
    
    # Core Fields
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)
    unit_type = models.CharField(max_length=50, choices=[
        ('company', 'Company'),
        ('division', 'Division'),
        ('department', 'Department'),
        ('team', 'Team'),
        ('section', 'Section'),
        ('cost_center', 'Cost Center'),
        ('business_unit', 'Business Unit'),
    ])
    description = models.TextField(blank=True)
    level = models.IntegerField(default=0)
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    effective_date = models.DateField()
    
    # Contact Information
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    
    # Budget and Cost Information
    cost_center_code = models.CharField(max_length=50, blank=True)
    budget_owner_id = models.UUIDField(null=True, blank=True)
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_organizational_units'
        verbose_name = 'Organizational Unit'
        verbose_name_plural = 'Organizational Units'
        indexes = [
            models.Index(fields=['company_code', 'parent_unit_id'], name='idx_org_hierarchy'),
            models.Index(fields=['company_code', 'unit_type'], name='idx_org_type'),
            models.Index(fields=['company_code', 'is_active'], name='idx_org_active'),
            models.Index(fields=['company_code', 'level'], name='idx_org_level'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['company_code', 'code'], name='uk_org_unit_code'),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def clean(self):
        """Validate organizational unit data"""
        self.clean_parent_unit()
        self.clean_level()
    
    def clean_parent_unit(self):
        """Validate parent unit to prevent circular references"""
        if self.parent_unit_id and self.parent_unit_id == str(self.id):
            raise ValidationError("An organizational unit cannot be its own parent")
        
        # Check for circular references
        if self.parent_unit_id:
            try:
                parent = OrganizationalUnit.objects.get(id=self.parent_unit_id)
                if self.is_ancestor_of(parent):
                    raise ValidationError("Circular reference detected in organizational hierarchy")
            except OrganizationalUnit.DoesNotExist:
                raise ValidationError("Parent unit does not exist")
    
    def clean_level(self):
        """Validate organizational level"""
        if self.level < 0:
            raise ValidationError("Level cannot be negative")
        if self.level > 10:
            raise ValidationError("Maximum organizational depth is 10 levels")
    
    def is_ancestor_of(self, unit):
        """Check if this unit is an ancestor of the given unit"""
        if not unit.parent_unit_id:
            return False
        try:
            parent = OrganizationalUnit.objects.get(id=unit.parent_unit_id)
            if parent.id == self.id:
                return True
            return self.is_ancestor_of(parent)
        except OrganizationalUnit.DoesNotExist:
            return False
    
    def get_children(self):
        """Get direct child units"""
        return OrganizationalUnit.objects.filter(parent_unit_id=self.id, is_active=True)
    
    def get_all_descendants(self):
        """Get all descendant units recursively"""
        descendants = []
        children = self.get_children()
        for child in children:
            descendants.append(child)
            descendants.extend(child.get_all_descendants())
        return descendants
    
    def get_ancestors(self):
        """Get all ancestor units"""
        ancestors = []
        if self.parent_unit_id:
            try:
                parent = OrganizationalUnit.objects.get(id=self.parent_unit_id)
                ancestors.append(parent)
                ancestors.extend(parent.get_ancestors())
            except OrganizationalUnit.DoesNotExist:
                pass
        return ancestors


class Position(models.Model):
    """
    Represents a specific position within an organizational unit
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Canonical Tenancy Field
    company_code = models.CharField(
        max_length=10,
        db_index=True,
        default=DEFAULT_COMPANY_CODE
    )
    organizational_unit_id = models.UUIDField()
    created_by_user_id = models.UUIDField()
    updated_by_user_id = models.UUIDField(null=True, blank=True)
    
    # Core Fields
    title = models.CharField(max_length=200)
    position_code = models.CharField(max_length=50)
    job_grade = models.CharField(max_length=50)
    job_family = models.CharField(max_length=100)
    employment_type = models.CharField(max_length=50, choices=[
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('intern', 'Intern'),
        ('temporary', 'Temporary'),
    ])
    is_active = models.BooleanField(default=True)
    is_manager_position = models.BooleanField(default=False)
    headcount = models.IntegerField(default=1)
    filled_count = models.IntegerField(default=0)
    vacancy_count = models.IntegerField(default=0)
    
    # Reporting Structure
    reports_to_position_id = models.UUIDField(null=True, blank=True)
    dotted_line_reports_to = models.UUIDField(null=True, blank=True)
    
    # Position Details
    description = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    responsibilities = models.TextField(blank=True)
    
    # Compensation Range
    min_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default='USD')
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_positions'
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'
        indexes = [
            models.Index(fields=['company_code', 'organizational_unit_id'], name='idx_pos_org'),
            models.Index(fields=['company_code', 'is_active'], name='idx_pos_active'),
            models.Index(fields=['company_code', 'job_grade'], name='idx_pos_grade'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['company_code', 'position_code'], name='uk_position_code'),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.position_code})"
    
    def clean(self):
        """Validate position data"""
        self.clean_headcount()
        self.clean_salary_range()
    
    def clean_headcount(self):
        """Validate headcount consistency"""
        if self.filled_count > self.headcount:
            raise ValidationError("Filled count cannot exceed total headcount")
        self.vacancy_count = self.headcount - self.filled_count
    
    def clean_salary_range(self):
        """Validate salary range"""
        if self.min_salary and self.max_salary and self.min_salary > self.max_salary:
            raise ValidationError("Minimum salary cannot exceed maximum salary")


class EmployeePosition(models.Model):
    """
    Links employees to their positions in the organizational structure
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Canonical Tenancy Field
    company_code = models.CharField(
        max_length=10,
        db_index=True,
        default=DEFAULT_COMPANY_CODE
    )
    employee_id = models.UUIDField()
    position_id = models.UUIDField()
    organizational_unit_id = models.UUIDField()
    created_by_user_id = models.UUIDField()
    updated_by_user_id = models.UUIDField(null=True, blank=True)
    
    # Assignment Details
    assignment_type = models.CharField(max_length=50, choices=[
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('acting', 'Acting'),
        ('interim', 'Interim'),
    ])
    is_primary = models.BooleanField(default=True)
    is_manager = models.BooleanField(default=False)
    
    # Assignment Period
    effective_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    
    # Reporting Structure
    reports_to_employee_id = models.UUIDField(null=True, blank=True)
    dotted_line_reports_to = models.UUIDField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=50, choices=[
        ('active', 'Active'),
        ('on_leave', 'On Leave'),
        ('terminated', 'Terminated'),
        ('transferred', 'Transferred'),
    ], default='active')
    
    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hr_employee_positions'
        verbose_name = 'Employee Position'
        verbose_name_plural = 'Employee Positions'
        indexes = [
            models.Index(fields=['company_code', 'employee_id'], name='idx_emp_pos_employee'),
            models.Index(fields=['company_code', 'position_id'], name='idx_emp_pos_position'),
            models.Index(fields=['company_code', 'organizational_unit_id'], name='idx_emp_pos_org'),
            models.Index(fields=['company_code', 'is_primary'], name='idx_emp_pos_primary'),
        ]
    
    def __str__(self):
        return f"Employee {self.employee_id} - {self.position_id}"
    
    def clean(self):
        """Validate employee position data"""
        self.clean_effective_dates()
    
    def clean_effective_dates(self):
        """Validate effective date logic"""
        if self.end_date and self.effective_date > self.end_date:
            raise ValidationError("End date must be after effective date")
