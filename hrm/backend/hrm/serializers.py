from rest_framework import serializers
from hrm.models.employee import EmployeeRecord
from hrm.models.department import Department


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for Employee model"""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = EmployeeRecord
        fields = ['id', 'employee_number', 'first_name', 'last_name', 
                  'full_name', 'work_email', 'mobile_phone', 'department_name', 'position_title',
                  'hire_date', 'annual_salary', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department model"""
    employee_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'employee_count', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_employee_count(self, obj):
        return EmployeeRecord.objects.filter(department_name=obj.name).count()
