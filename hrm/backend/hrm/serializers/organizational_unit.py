"""
Organizational Unit Serializers for HRM
"""

from rest_framework import serializers
from ..models.organizational_unit import OrganizationalUnit, Position, EmployeePosition
from ..models.department import Department


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department model"""
    
    class Meta:
        model = Department
        fields = [
            'id', 'name', 'description', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class OrganizationalUnitSerializer(serializers.ModelSerializer):
    """Serializer for Organizational Unit model"""
    
    parent_unit_name = serializers.CharField(source='parent_unit.name', read_only=True)
    manager_name = serializers.CharField(source='manager.get_full_name', read_only=True)
    budget_owner_name = serializers.CharField(source='budget_owner.get_full_name', read_only=True)
    children_count = serializers.SerializerMethodField()
    
    class Meta:
        model = OrganizationalUnit
        fields = [
            'id', 'company', 'parent_unit', 'parent_unit_name', 'manager', 'manager_name',
            'budget_owner', 'budget_owner_name', 'name', 'code', 'unit_type', 'description',
            'level', 'sort_order', 'is_active', 'effective_date', 'phone', 'email',
            'cost_center_code', 'children_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_children_count(self, obj):
        return obj.get_children().count()


class PositionSerializer(serializers.ModelSerializer):
    """Serializer for Position model"""
    
    organizational_unit_name = serializers.CharField(source='organizational_unit.name', read_only=True)
    reports_to_position_title = serializers.CharField(source='reports_to_position.title', read_only=True)
    vacancy_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Position
        fields = [
            'id', 'company', 'organizational_unit', 'organizational_unit_name',
            'reports_to_position', 'reports_to_position_title', 'title', 'position_code',
            'job_grade', 'job_family', 'employment_type', 'is_active', 'is_manager_position',
            'headcount', 'filled_count', 'vacancy_count', 'description', 'requirements',
            'responsibilities', 'min_salary', 'max_salary', 'currency', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class EmployeePositionSerializer(serializers.ModelSerializer):
    """Serializer for Employee Position model"""
    
    employee_name = serializers.CharField(source='employee.get_full_name', read_only=True)
    position_title = serializers.CharField(source='position.title', read_only=True)
    organizational_unit_name = serializers.CharField(source='organizational_unit.name', read_only=True)
    reports_to_employee_name = serializers.CharField(source='reports_to_employee.get_full_name', read_only=True)
    
    class Meta:
        model = EmployeePosition
        fields = [
            'id', 'company', 'employee', 'employee_name', 'position', 'position_title',
            'organizational_unit', 'organizational_unit_name', 'reports_to_employee',
            'reports_to_employee_name', 'assignment_type', 'is_primary', 'is_manager',
            'effective_date', 'end_date', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class OrganizationalUnitTreeSerializer(serializers.ModelSerializer):
    """Serializer for hierarchical org unit tree structure"""
    
    children = serializers.SerializerMethodField()
    positions = PositionSerializer(many=True, read_only=True)
    
    class Meta:
        model = OrganizationalUnit
        fields = [
            'id', 'name', 'code', 'unit_type', 'level', 'is_active', 'children', 'positions'
        ]
    
    def get_children(self, obj):
        children = obj.get_children()
        return OrganizationalUnitTreeSerializer(children, many=True).data
