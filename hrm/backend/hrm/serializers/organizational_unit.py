"""Organizational Unit Serializers - HRM DomainFollowing platform.cline governance - API-first design"""
from rest_framework import serializers
from ..models.organizational_unit import OrganizationalUnit, Position, EmployeePosition


class OrganizationalUnitSerializer(serializers.ModelSerializer):
    """Serializer for Organizational Unit model"""
    
    parent_unit_name = serializers.CharField(source='parent_unit.name', read_only=True)
    manager_name = serializers.CharField(source='manager.name', read_only=True)
    children_count = serializers.SerializerMethodField()
    
    class Meta:
        model = OrganizationalUnit
        fields = [
            'id', 'company_id', 'parent_unit_id', 'parent_unit_name', 'manager_id', 'manager_name',
            'name', 'code', 'unit_type', 'description', 'level', 'sort_order', 'is_active',
            'effective_date', 'phone', 'email', 'cost_center_code', 'budget_owner_id',
            'created_at', 'updated_at', 'children_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'children_count']
    
    def get_children_count(self, obj):
        """Get count of direct child units"""
        return obj.get_children().count()
    
    def validate(self, data):
        """Validate organizational unit data"""
        # Validate parent unit is not self
        if 'parent_unit_id' in data and data.get('parent_unit_id') == str(self.instance.id if self.instance else None):
            raise serializers.ValidationError("An organizational unit cannot be its own parent")
        
        # Validate level constraints
        if 'level' in data and data['level'] > 10:
            raise serializers.ValidationError("Maximum organizational depth is 10 levels")
        
        return data


class PositionSerializer(serializers.ModelSerializer):
    """Serializer for Position model"""
    
    organizational_unit_name = serializers.CharField(source='organizational_unit.name', read_only=True)
    reports_to_position_title = serializers.CharField(source='reports_to_position.title', read_only=True)
    
    class Meta:
        model = Position
        fields = [
            'id', 'company_id', 'organizational_unit_id', 'organizational_unit_name',
            'title', 'position_code', 'job_grade', 'job_family', 'employment_type',
            'is_active', 'is_manager_position', 'headcount', 'filled_count', 'vacancy_count',
            'reports_to_position_id', 'reports_to_position_title', 'dotted_line_reports_to',
            'description', 'requirements', 'responsibilities', 'min_salary', 'max_salary',
            'currency', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'vacancy_count']
    
    def validate(self, data):
        """Validate position data"""
        # Validate headcount consistency
        if 'filled_count' in data and 'headcount' in data:
            if data['filled_count'] > data['headcount']:
                raise serializers.ValidationError("Filled count cannot exceed total headcount")
        
        # Validate salary range
        min_salary = data.get('min_salary', getattr(self.instance, 'min_salary', None))
        max_salary = data.get('max_salary', getattr(self.instance, 'max_salary', None))
        if min_salary and max_salary and min_salary > max_salary:
            raise serializers.ValidationError("Minimum salary cannot exceed maximum salary")
        
        return data


class EmployeePositionSerializer(serializers.ModelSerializer):
    """Serializer for Employee Position model"""
    
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    position_title = serializers.CharField(source='position.title', read_only=True)
    organizational_unit_name = serializers.CharField(source='organizational_unit.name', read_only=True)
    reports_to_employee_name = serializers.CharField(source='reports_to_employee.name', read_only=True)
    
    class Meta:
        model = EmployeePosition
        fields = [
            'id', 'company_id', 'employee_id', 'employee_name', 'position_id', 'position_title',
            'organizational_unit_id', 'organizational_unit_name', 'assignment_type', 'is_primary',
            'is_manager', 'effective_date', 'end_date', 'reports_to_employee_id',
            'reports_to_employee_name', 'dotted_line_reports_to', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validate employee position data"""
        # Validate effective date logic
        effective_date = data.get('effective_date', getattr(self.instance, 'effective_date', None))
        end_date = data.get('end_date', getattr(self.instance, 'end_date', None))
        if effective_date and end_date and effective_date > end_date:
            raise serializers.ValidationError("End date must be after effective date")
        
        return data


class OrganizationalChartSerializer(serializers.Serializer):
    """Serializer for organizational chart tree structure"""
    
    id = serializers.UUIDField()
    name = serializers.CharField()
    code = serializers.CharField()
    unit_type = serializers.CharField()
    level = serializers.IntegerField()
    is_active = serializers.BooleanField()
    parent_unit_id = serializers.UUIDField(allow_null=True)
    manager_id = serializers.UUIDField(allow_null=True)
    children = serializers.ListField(child=serializers.DictField(), required=False)
    positions = serializers.ListField(child=serializers.DictField(), required=False)
    employee_count = serializers.IntegerField(required=False)


class PositionHierarchySerializer(serializers.Serializer):
    """Serializer for position hierarchy within organizational units"""
    
    id = serializers.UUIDField()
    title = serializers.CharField()
    position_code = serializers.CharField()
    job_grade = serializers.CharField()
    is_active = serializers.BooleanField()
    is_manager_position = serializers.BooleanField()
    headcount = serializers.IntegerField()
    filled_count = serializers.IntegerField()
    vacancy_count = serializers.IntegerField()
    reports_to_position_id = serializers.UUIDField(allow_null=True)
    organizational_unit_id = serializers.UUIDField()
    organizational_unit_name = serializers.CharField()
    employees = serializers.ListField(child=serializers.DictField(), required=False)
