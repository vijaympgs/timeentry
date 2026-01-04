from rest_framework import serializers
from models.employee import EmployeeRecord, Department

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
    manager_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'manager', 'manager_name', 
                 'employee_count', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_employee_count(self, obj):
        return EmployeeRecord.objects.filter(department_name=obj.name).count()

    def get_manager_name(self, obj):
        if obj.manager:
            return f"{obj.manager.first_name} {obj.manager.last_name}"
        return None
