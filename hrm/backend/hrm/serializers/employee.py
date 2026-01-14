"""Employee SerializersFollowing T1 Complex Master Template specifications with company scoping"""

from rest_framework import serializers
from ..models.employee import EmployeeRecord, EmployeeAddress


class EmployeeAddressSerializer(serializers.ModelSerializer):
    """Serializer for EmployeeAddress model"""
    class Meta:
        model = EmployeeAddress
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class EmployeeRecordSerializer(serializers.ModelSerializer):
    """Serializer for EmployeeRecord model following T1 Complex Master Template"""
    # Read-only fields for display
    full_name = serializers.ReadOnlyField()
    company_name = serializers.CharField(source='get_company_name', read_only=True)
    
    # Nested serializer for addresses
    addresses = EmployeeAddressSerializer(many=True, read_only=True)
    
    # Hierarchy fields
    manager_name = serializers.CharField(source='manager.full_name', read_only=True)
    manager_employee_number = serializers.CharField(source='manager.employee_number', read_only=True)
    direct_reports_count = serializers.SerializerMethodField()
    
    # Computed fields
    age = serializers.SerializerMethodField()
    years_of_service = serializers.SerializerMethodField()
    
    class Meta:
        model = EmployeeRecord
        fields = '__all__'
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'created_by_user', 'updated_by_user',
            'full_name', 'company_name', 'addresses', 'age', 'years_of_service',
            'manager_name', 'manager_employee_number', 'direct_reports_count'
        ]
    
    def get_direct_reports_count(self, obj):
        """Get count of direct reports"""
        return obj.direct_reports.count()
    
    def get_age(self, obj):
        """Calculate age from date of birth"""
        from datetime import date
        if obj.date_of_birth:
            today = date.today()
            return today.year - obj.date_of_birth.year - (
                (today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day)
            )
        return None
    
    def get_years_of_service(self, obj):
        """Calculate years of service from hire date"""
        from datetime import date
        if obj.hire_date:
            today = date.today()
            return today.year - obj.hire_date.year - (
                (today.month, today.day) < (obj.hire_date.month, obj.hire_date.day)
            )
        return None
    
    def get_company_name(self, obj):
        """Get company name - placeholder for now"""
        # In a real implementation, this would fetch from Company model
        return f"Company-{obj.company_code}"


class EmployeeRecordListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views following T1 specifications"""
    full_name = serializers.ReadOnlyField()
    first_name = serializers.ReadOnlyField()
    last_name = serializers.ReadOnlyField()
    company_name = serializers.CharField(source='get_company_name', read_only=True)
    age = serializers.SerializerMethodField()
    years_of_service = serializers.SerializerMethodField()
    
    class Meta:
        model = EmployeeRecord
        fields = [
            'id', 'employee_number', 'first_name', 'last_name', 'full_name', 'company_name', 'work_email',
            'department_name', 'position_title', 'employment_status', 'is_active',
            'hire_date', 'age', 'years_of_service'
        ]
    
    def get_age(self, obj):
        """Calculate age from date of birth"""
        from datetime import date
        if obj.date_of_birth:
            today = date.today()
            return today.year - obj.date_of_birth.year - (
                (today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day)
            )
        return None
    
    def get_years_of_service(self, obj):
        """Calculate years of service from hire date"""
        from datetime import date
        if obj.hire_date:
            today = date.today()
            return today.year - obj.hire_date.year - (
                (today.month, today.day) < (obj.hire_date.month, obj.hire_date.day)
            )
        return None
    
    def get_company_name(self, obj):
        """Get company name - placeholder for now"""
        return f"Company-{obj.company_code}"


class EmployeeRecordCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating EmployeeRecord following T1 specifications"""
    manager = serializers.PrimaryKeyRelatedField(queryset=EmployeeRecord.objects.all(), required=False, allow_null=True)
    
    class Meta:
        model = EmployeeRecord
        fields = [
            'employee_number', 'national_id', 'social_security_number', 'passport_number',
            'first_name', 'last_name', 'middle_name', 'preferred_name', 'name_prefix',
            'name_suffix', 'gender', 'date_of_birth', 'marital_status',
            'work_email', 'personal_email', 'work_phone', 'mobile_phone', 'home_phone',
            'hire_date', 'original_hire_date', 'employment_status', 'employment_type',
            'position_title', 'department_name', 'job_category', 'job_level', 'job_family',
            'work_location_name', 'remote_work_eligible', 'remote_work_percentage',
            'manager_name', 'manager', 'hierarchy_level', 'hr_business_partner_name', 
            'salary_grade', 'salary_step', 'annual_salary', 'hourly_rate', 'currency', 'pay_frequency',
            'benefits_eligibility_date', 'benefits_package_name',
            'health_insurance_eligible', 'dental_insurance_eligible',
            'vision_insurance_eligible', 'retirement_plan_eligible',
            'life_insurance_eligible', 'primary_emergency_contact_name',
            'primary_emergency_contact_relationship', 'primary_emergency_contact_phone',
            'secondary_emergency_contact_name', 'secondary_emergency_contact_relationship',
            'secondary_emergency_contact_phone', 'is_active', 'is_confidential',
            'is_key_employee', 'is_high_potential', 'username', 'role'
        ]
    
    def validate(self, data):
        """Validate hierarchy level based on manager"""
        manager = data.get('manager')
        hierarchy_level = data.get('hierarchy_level', 0)
        
        if manager:
            if hierarchy_level <= manager.hierarchy_level:
                raise serializers.ValidationError(
                    f"Hierarchy level must be greater than manager's level ({manager.hierarchy_level})"
                )
        else:
            # If no manager, should be CEO (level 0)
            if hierarchy_level != 0:
                raise serializers.ValidationError("CEO must have hierarchy level 0")
        
        return data
    
    def validate_employee_number(self, value):
        """Validate employee number uniqueness within company"""
        company_code = self.initial_data.get('company_code', 'DEFAULT')
        if EmployeeRecord.objects.filter(
            company_code=company_code, 
            employee_number=value
        ).exists():
            raise serializers.ValidationError(
                f"Employee number {value} already exists in this company."
            )
        return value
    
    def validate_work_email(self, value):
        """Validate work email uniqueness"""
        company_code = self.initial_data.get('company_code', 'DEFAULT')
        if EmployeeRecord.objects.filter(
            company_code=company_code, 
            work_email=value
        ).exists():
            raise serializers.ValidationError(
                f"Work email {value} already exists in this company."
            )
        return value


class EmployeeRecordUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating EmployeeRecord following T1 specifications"""
    manager = serializers.PrimaryKeyRelatedField(queryset=EmployeeRecord.objects.all(), required=False, allow_null=True)
    
    class Meta:
        model = EmployeeRecord
        fields = [
            'national_id', 'social_security_number', 'passport_number',
            'first_name', 'last_name', 'middle_name', 'preferred_name', 'name_prefix',
            'name_suffix', 'gender', 'date_of_birth', 'marital_status',
            'personal_email', 'work_phone', 'mobile_phone', 'home_phone',
            'original_hire_date', 'employment_status', 'employment_type',
            'position_title', 'department_name', 'job_category', 'job_level', 'job_family',
            'work_location_name', 'remote_work_eligible', 'remote_work_percentage',
            'manager_name', 'manager', 'hierarchy_level', 'hr_business_partner_name', 
            'salary_grade', 'salary_step', 'annual_salary', 'hourly_rate', 'currency', 'pay_frequency',
            'benefits_eligibility_date', 'benefits_package_name',
            'health_insurance_eligible', 'dental_insurance_eligible',
            'vision_insurance_eligible', 'retirement_plan_eligible',
            'life_insurance_eligible', 'primary_emergency_contact_name',
            'primary_emergency_contact_relationship', 'primary_emergency_contact_phone',
            'secondary_emergency_contact_name', 'secondary_emergency_contact_relationship',
            'secondary_emergency_contact_phone', 'is_active', 'is_confidential',
            'is_key_employee', 'is_high_potential', 'termination_date', 'termination_reason',
            'rehire_eligible', 'username', 'role'
        ]
    
    def validate(self, data):
        """Validate hierarchy level based on manager"""
        manager = data.get('manager')
        hierarchy_level = data.get('hierarchy_level')
        
        # Get current instance for validation
        instance = self.instance
        
        if manager:
            # Prevent circular references
            if manager == instance:
                raise serializers.ValidationError("Employee cannot be their own manager")
            
            # Check for circular reference in hierarchy
            current = manager
            while current:
                if current == instance:
                    raise serializers.ValidationError("This would create a circular reference in the hierarchy")
                current = current.manager
        
        if hierarchy_level is not None and manager:
            if hierarchy_level <= manager.hierarchy_level:
                raise serializers.ValidationError(
                    f"Hierarchy level must be greater than manager's level ({manager.hierarchy_level})"
                )
        
        return data
