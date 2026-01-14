"""Employee Profile Serializers - HRM Domain
Following platform.cline governance - API serialization for profile management
"""

from rest_framework import serializers
from ..models.employee_profile import EmployeeProfile, EmployeeSkill, EmployeeDocument, SkillCategory
from ..models.employee import EmployeeRecord


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for Employee Record model"""
    
    class Meta:
        model = EmployeeRecord
        fields = [
            'id', 'first_name', 'last_name', 'employee_number', 'work_email', 'personal_email',
            'date_of_birth', 'gender', 'work_phone', 'mobile_phone', 'home_phone',
            'address', 'city', 'state', 'postal_code', 'country',
            'hire_date', 'employment_status', 'termination_date', 'termination_reason',
            'is_active'
        ]


class EmployeeRecordSerializer(serializers.ModelSerializer):
    """Serializer for Employee Record model (alias for EmployeeSerializer)"""
    
    class Meta:
        model = EmployeeRecord
        fields = [
            'id', 'first_name', 'last_name', 'employee_number', 'work_email', 'personal_email',
            'date_of_birth', 'gender', 'work_phone', 'mobile_phone', 'home_phone',
            'address', 'city', 'state', 'postal_code', 'country',
            'hire_date', 'employment_status', 'termination_date', 'termination_reason',
            'is_active'
        ]


class EmployeeProfileSerializer(serializers.ModelSerializer):
    """Serializer for Employee Profile model"""
    
    # Read-only fields from related employee
    employee_name = serializers.CharField(source='employee.first_name', read_only=True)
    employee_last_name = serializers.CharField(source='employee.last_name', read_only=True)
    employee_number = serializers.CharField(source='employee.employee_number', read_only=True)
    employee_email = serializers.CharField(source='employee.work_email', read_only=True)
    employee_department = serializers.CharField(source='employee.department_name', read_only=True)
    employee_position = serializers.CharField(source='employee.position_title', read_only=True)
    
    # Computed fields
    full_name = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    complete_address = serializers.SerializerMethodField()
    
    class Meta:
        model = EmployeeProfile
        fields = [
            'id', 'employee', 'employee_name', 'employee_last_name', 'employee_number',
            'employee_email', 'employee_department', 'employee_position', 'full_name', 'age',
            'preferred_name', 'middle_name', 'maiden_name', 'nickname', 'gender',
            'date_of_birth', 'place_of_birth', 'nationality', 'marital_status',
            'personal_email', 'personal_phone', 'work_phone_extension',
            'home_address_line_1', 'home_address_line_2', 'home_city', 'home_state',
            'home_postal_code', 'home_country', 'complete_address',
            'emergency_contact_name', 'emergency_contact_relationship', 'emergency_contact_phone',
            'emergency_contact_email', 'profile_visibility', 'profile_photo_url', 'bio',
            'linkedin_url', 'twitter_url', 'preferred_language', 'timezone',
            'email_notifications', 'sms_notifications', 'is_active', 'is_verified',
            'verification_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'verification_date']
    
    def get_full_name(self, obj):
        """Get full name with preferred name consideration"""
        first_name = obj.preferred_name or obj.employee.first_name
        return f"{first_name} {obj.employee.last_name}"
    
    def get_age(self, obj):
        """Calculate age from date of birth"""
        if obj.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - obj.date_of_birth.year - (
                (today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day)
            )
        return None
    
    def get_complete_address(self, obj):
        """Get formatted complete address"""
        address_parts = []
        if obj.home_address_line_1:
            address_parts.append(obj.home_address_line_1)
        if obj.home_address_line_2:
            address_parts.append(obj.home_address_line_2)
        if obj.home_city or obj.home_state or obj.home_postal_code:
            city_state_zip = []
            if obj.home_city:
                city_state_zip.append(obj.home_city)
            if obj.home_state:
                city_state_zip.append(obj.home_state)
            if obj.home_postal_code:
                city_state_zip.append(obj.home_postal_code)
            address_parts.append(', '.join(city_state_zip))
        if obj.home_country:
            address_parts.append(obj.home_country)
        return ', '.join(address_parts)


class EmployeeSkillSerializer(serializers.ModelSerializer):
    """Serializer for Employee Skill model"""
    
    # Read-only fields
    employee_name = serializers.CharField(source='employee.employee.first_name', read_only=True)
    verified_by_name = serializers.CharField(source='verified_by.username', read_only=True)
    proficiency_level_display = serializers.CharField(source='get_proficiency_level_display', read_only=True)
    
    class Meta:
        model = EmployeeSkill
        fields = [
            'id', 'employee', 'employee_name', 'skill_name', 'skill_category',
            'proficiency_level', 'proficiency_level_display', 'years_experience',
            'last_used', 'is_verified', 'verified_by', 'verified_by_name',
            'verified_date', 'description', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'verified_date']


class EmployeeDocumentSerializer(serializers.ModelSerializer):
    """Serializer for Employee Document model"""
    
    # Read-only fields
    employee_name = serializers.CharField(source='employee.employee.first_name', read_only=True)
    uploaded_by_name = serializers.CharField(source='uploaded_by.username', read_only=True)
    document_type_display = serializers.CharField(source='get_document_type_display', read_only=True)
    file_size_display = serializers.SerializerMethodField()
    
    class Meta:
        model = EmployeeDocument
        fields = [
            'id', 'employee', 'employee_name', 'document_type', 'document_type_display',
            'document_name', 'description', 'file_url', 'file_size', 'file_size_display',
            'file_type', 'upload_date', 'expiry_date', 'is_confidential',
            'uploaded_by', 'uploaded_by_name', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'upload_date']
    
    def get_file_size_display(self, obj):
        """Get human-readable file size"""
        if obj.file_size:
            for unit in ['B', 'KB', 'MB', 'GB']:
                if obj.file_size < 1024.0:
                    return f"{obj.file_size:.1f} {unit}"
                obj.file_size /= 1024.0
            return f"{obj.file_size:.1f} TB"
        return "0 B"


class SkillCategorySerializer(serializers.ModelSerializer):
    """Serializer for Skill Category model"""
    
    # Read-only fields
    parent_category_name = serializers.CharField(source='parent_category.name', read_only=True)
    children_count = serializers.SerializerMethodField()
    
    class Meta:
        model = SkillCategory
        fields = [
            'id', 'name', 'description', 'parent_category', 'parent_category_name',
            'is_active', 'children_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_children_count(self, obj):
        """Get count of active child categories"""
        return obj.child_categories.filter(is_active=True).count()


class EmployeeProfileDetailSerializer(EmployeeProfileSerializer):
    """Detailed serializer for Employee Profile with related data"""
    
    skills = EmployeeSkillSerializer(many=True, read_only=True)
    documents = EmployeeDocumentSerializer(many=True, read_only=True)
    
    class Meta(EmployeeProfileSerializer.Meta):
        fields = EmployeeProfileSerializer.Meta.fields + ['skills', 'documents']


class SkillCategoryWithSkillsSerializer(SkillCategorySerializer):
    """Serializer for Skill Category with associated skills"""
    
    skills = serializers.SerializerMethodField()
    
    class Meta(SkillCategorySerializer.Meta):
        fields = SkillCategorySerializer.Meta.fields + ['skills']
    
    def get_skills(self, obj):
        """Get skills in this category for a specific employee"""
        employee_id = self.context.get('employee_id')
        if employee_id:
            skills = EmployeeSkill.objects.filter(
                employee__employee_id=employee_id,
                skill_category=obj.name,
                is_active=True
            )
            return EmployeeSkillSerializer(skills, many=True).data
        return []


class EmployeeProfileSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for profile summaries in lists"""
    
    employee_name = serializers.CharField(source='employee.first_name', read_only=True)
    employee_last_name = serializers.CharField(source='employee.last_name', read_only=True)
    employee_number = serializers.CharField(source='employee.employee_number', read_only=True)
    employee_department = serializers.CharField(source='employee.department_name', read_only=True)
    employee_position = serializers.CharField(source='employee.position_title', read_only=True)
    skills_count = serializers.SerializerMethodField()
    documents_count = serializers.SerializerMethodField()
    
    class Meta:
        model = EmployeeProfile
        fields = [
            'id', 'employee', 'employee_name', 'employee_last_name', 'employee_number',
            'employee_department', 'employee_position', 'profile_photo_url', 'bio',
            'skills_count', 'documents_count', 'is_active', 'is_verified', 'updated_at'
        ]
    
    def get_skills_count(self, obj):
        """Get count of active skills"""
        return obj.skills.filter(is_active=True).count()
    
    def get_documents_count(self, obj):
        """Get count of active documents"""
        return obj.documents.filter(is_active=True).count()
