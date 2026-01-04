"""
HRM Models Package - Canonical aggregate structure
Following governance: One file = One aggregate root
"""

# Import canonical aggregate roots
from .employee import EmployeeRecord, EmployeeAddress
from .department import Department
from .organizational_unit import OrganizationalUnit, Position, EmployeePosition
from .employee_profile import EmployeeProfile, EmployeeSkill, EmployeeDocument, SkillCategory

__all__ = [
    'EmployeeRecord',
    'EmployeeAddress', 
    'Department',
    'OrganizationalUnit',
    'Position',
    'EmployeePosition',
    'EmployeeProfile',
    'EmployeeSkill',
    'EmployeeDocument',
    'SkillCategory',
]
