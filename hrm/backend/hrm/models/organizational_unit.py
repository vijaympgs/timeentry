"""
Organizational Unit and Position Models for HRM
Following BBP 02.2 Organizational Chart specifications
Aligned with enterprise governance and Olivine UI canon
"""
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
User = get_user_model()

class OrganizationalUnit(models.Model):
    """
    Represents an organizational unit (department, division, team, etc.)
    in the company structure with hierarchical relationships
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='organizationalunit_company')
    parent_unit = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='organizationalunit_parent_unit')
    manager = models.ForeignKey('hrm.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='organizationalunit_manager')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='organizationalunit_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='organizationalunit_updated_by')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)
    unit_type = models.CharField(max_length=50, choices=[('company', 'Company'), ('division', 'Division'), ('department', 'Department'), ('team', 'Team'), ('section', 'Section'), ('cost_center', 'Cost Center'), ('business_unit', 'Business Unit')])
    description = models.TextField(blank=True)
    level = models.IntegerField(default=0)
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    effective_date = models.DateField()
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    cost_center_code = models.CharField(max_length=50, blank=True)
    budget_owner = models.ForeignKey('hrm.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='organizationalunit_budget_owner')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_organizational_units'
        verbose_name = 'Organizational Unit'
        verbose_name_plural = 'Organizational Units'
        indexes = [models.Index(fields=['company', 'parent_unit'], name='idx_org_hierarchy'), models.Index(fields=['company', 'unit_type'], name='idx_org_type'), models.Index(fields=['company', 'is_active'], name='idx_org_active'), models.Index(fields=['company', 'level'], name='idx_org_level')]
        constraints = [models.UniqueConstraint(fields=['company', 'code'], name='uk_org_unit_code')]
        ordering = ['level', 'sort_order', 'name']

    def __str__(self):
        return f'{self.name} ({self.code})'

    def clean(self):
        """Validate organizational unit data"""
        if self.parent_unit and self.parent_unit_id == self.id:
            raise ValidationError('An organizational unit cannot be its own parent')
        if self.parent_unit:
            if self.is_ancestor_of(self.parent_unit):
                raise ValidationError('Circular reference detected in organizational hierarchy')

    def is_ancestor_of(self, unit):
        """Check if this unit is an ancestor of the given unit"""
        if not unit.parent_unit:
            return False
        if unit.parent_unit_id == self.id:
            return True
        return self.is_ancestor_of(unit.parent_unit)

    def get_children(self):
        """Get all direct child units"""
        return self.child_units.filter(is_active=True)

    def get_descendants(self):
        """Get all descendant units recursively"""
        descendants = []
        for child in self.get_children():
            descendants.append(child)
            descendants.extend(child.get_descendants())
        return descendants

    def get_ancestors(self):
        """Get all ancestor units"""
        ancestors = []
        current = self.parent_unit
        while current:
            ancestors.append(current)
            current = current.parent_unit
        return ancestors

    def get_full_path(self):
        """Get the full path of this unit in the hierarchy"""
        ancestors = self.get_ancestors()
        path = ' > '.join([unit.name for unit in reversed(ancestors)] + [self.name])
        return path

class Position(models.Model):
    """
    Represents a specific position within an organizational unit
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='position_company')
    organizational_unit = models.ForeignKey(OrganizationalUnit, on_delete=models.CASCADE, null=True, blank=True, related_name='position_organizational_unit')
    reports_to_position = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='position_reports_to_position')
    dotted_line_reports_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='position_dotted_line_reports_to')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='position_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='position_updated_by')
    title = models.CharField(max_length=200)
    position_code = models.CharField(max_length=50)
    job_grade = models.CharField(max_length=50)
    job_family = models.CharField(max_length=100)
    employment_type = models.CharField(max_length=50, choices=[('full_time', 'Full Time'), ('part_time', 'Part Time'), ('contract', 'Contract'), ('intern', 'Intern'), ('temporary', 'Temporary')])
    is_active = models.BooleanField(default=True)
    is_manager_position = models.BooleanField(default=False)
    headcount = models.IntegerField(default=1)
    filled_count = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    responsibilities = models.TextField(blank=True)
    min_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default='USD')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_positions'
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'
        indexes = [models.Index(fields=['company', 'organizational_unit'], name='idx_pos_org'), models.Index(fields=['company', 'is_active'], name='idx_pos_active'), models.Index(fields=['company', 'job_grade'], name='idx_pos_grade')]
        constraints = [models.UniqueConstraint(fields=['company', 'position_code'], name='uk_position_code')]
        ordering = ['job_grade', 'title']

    def __str__(self):
        return f'{self.title} ({self.position_code})'

    @property
    def vacancy_count(self):
        """Calculate vacancy count"""
        return max(0, self.headcount - self.filled_count)

    def clean(self):
        """Validate position data"""
        if self.filled_count > self.headcount:
            raise ValidationError('Filled count cannot exceed total headcount')
        if self.min_salary and self.max_salary and (self.min_salary > self.max_salary):
            raise ValidationError('Minimum salary cannot exceed maximum salary')

class EmployeePosition(models.Model):
    """
    Links employees to their positions in the organizational structure
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='employeeposition_company')
    employee = models.ForeignKey('hrm.Employee', on_delete=models.CASCADE, null=True, blank=True, related_name='employeeposition_employee')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True, related_name='employeeposition_position')
    organizational_unit = models.ForeignKey(OrganizationalUnit, on_delete=models.CASCADE, null=True, blank=True, related_name='employeeposition_organizational_unit')
    reports_to_employee = models.ForeignKey('hrm.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='employeeposition_reports_to_employee')
    dotted_line_reports_to = models.ForeignKey('hrm.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='employeeposition_dotted_line_reports_to')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='employeeposition_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='employeeposition_updated_by')
    assignment_type = models.CharField(max_length=50, choices=[('primary', 'Primary'), ('secondary', 'Secondary'), ('acting', 'Acting'), ('interim', 'Interim')])
    is_primary = models.BooleanField(default=True)
    is_manager = models.BooleanField(default=False)
    effective_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('active', 'Active'), ('on_leave', 'On Leave'), ('terminated', 'Terminated'), ('transferred', 'Transferred')], default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_employee_positions'
        verbose_name = 'Employee Position'
        verbose_name_plural = 'Employee Positions'
        indexes = [models.Index(fields=['company', 'employee'], name='idx_emp_pos_employee'), models.Index(fields=['company', 'position'], name='idx_emp_pos_position'), models.Index(fields=['company', 'organizational_unit'], name='idx_emp_pos_org'), models.Index(fields=['company', 'is_primary'], name='idx_emp_pos_primary')]
        ordering = ['-effective_date']

    def __str__(self):
        return f'{self.employee} - {self.position} ({self.assignment_type})'

    def clean(self):
        """Validate employee position assignment"""
        if self.end_date and self.effective_date > self.end_date:
            raise ValidationError('End date must be after effective date')
        if self.is_primary:
            existing_primary = EmployeePosition.objects.filter(employee=self.employee, is_primary=True, status='active').exclude(id=self.id)
            if existing_primary.exists():
                raise ValidationError('Employee can only have one primary position assignment')
