"""
Profile View serializers for employee self-service profile viewing and management
"""

from rest_framework import serializers
from ..models.profile_view import ProfileViewAccess, ProfileEndorsement, ProfileViewSettings
from ..models.employee_profile import EmployeeProfile, EmployeeSkill, EmployeeDocument
from ..models.employee import EmployeeRecord


class ProfileViewAccessSerializer(serializers.ModelSerializer):
    """Serializer for profile view access tracking"""
    viewer_name = serializers.CharField(source='viewer.username', read_only=True)
    viewer_email = serializers.CharField(source='viewer.email', read_only=True)
    profile_name = serializers.CharField(source='profile.employee.first_name', read_only=True)
    profile_employee_number = serializers.CharField(source='profile.employee.employee_number', read_only=True)
    
    class Meta:
        model = ProfileViewAccess
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProfileEndorsementSerializer(serializers.ModelSerializer):
    """Serializer for profile skill endorsements"""
    endorser_name = serializers.CharField(source='endorser.username', read_only=True)
    endorser_email = serializers.CharField(source='endorser.email', read_only=True)
    profile_name = serializers.CharField(source='profile.employee.first_name', read_only=True)
    profile_employee_number = serializers.CharField(source='profile.employee.employee_number', read_only=True)
    skill_name = serializers.CharField(source='skill.name', read_only=True)
    skill_category = serializers.CharField(source='skill.skill_category', read_only=True)
    verified_by_name = serializers.CharField(source='verified_by.username', read_only=True)
    
    class Meta:
        model = ProfileEndorsement
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProfileViewSettingsSerializer(serializers.ModelSerializer):
    """Serializer for profile view settings"""
    company_name = serializers.CharField(source='company.name', read_only=True)
    
    class Meta:
        model = ProfileViewSettings
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class EmployeeProfileSerializer(serializers.ModelSerializer):
    """Serializer for employee profiles"""
    employee_name = serializers.CharField(source='employee.first_name', read_only=True)
    employee_number = serializers.CharField(source='employee.employee_number', read_only=True)
    employee_email = serializers.CharField(source='employee.work_email', read_only=True)
    department_name = serializers.CharField(source='employee.department_name', read_only=True)
    position_title = serializers.CharField(source='employee.position_title', read_only=True)
    
    # Skills and certifications
    skills_data = serializers.SerializerMethodField()
    certifications_data = serializers.SerializerMethodField()
    
    # Profile statistics
    skills_count = serializers.SerializerMethodField()
    certifications_count = serializers.SerializerMethodField()
    endorsements_count = serializers.SerializerMethodField()
    
    class Meta:
        model = EmployeeProfile
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_skills_data(self, obj):
        """Get skills data for the profile"""
        skills = obj.skills.all()
        return [
            {
                'id': str(skill.id),
                'name': skill.skill_name,
                'category': skill.skill_category,
                'proficiency_level': skill.proficiency_level,
                'years_experience': skill.years_experience,
                'is_verified': skill.is_verified
            }
            for skill in skills
        ]
    
    def get_certifications_data(self, obj):
        """Get certifications data for the profile"""
        # Note: This would need to be implemented based on the actual certification model structure
        return []
    
    def get_skills_count(self, obj):
        """Get total skills count"""
        return obj.skills.count()
    
    def get_certifications_count(self, obj):
        """Get total certifications count"""
        # Note: This would need to be implemented based on the actual certification model structure
        return 0
    
    def get_endorsements_count(self, obj):
        """Get total endorsements count"""
        return ProfileEndorsement.objects.filter(profile=obj).count()


class ProfileViewListSerializer(serializers.ModelSerializer):
    """Serializer for profile list view"""
    employee_name = serializers.CharField(source='employee.first_name', read_only=True)
    employee_number = serializers.CharField(source='employee.employee_number', read_only=True)
    employee_email = serializers.CharField(source='employee.work_email', read_only=True)
    department_name = serializers.CharField(source='employee.department_name', read_only=True)
    position_title = serializers.CharField(source='employee.position_title', read_only=True)
    profile_visibility = serializers.CharField(read_only=True)
    is_profile_public = serializers.BooleanField(read_only=True)
    skills_count = serializers.SerializerMethodField()
    endorsements_count = serializers.SerializerMethodField()
    
    class Meta:
        model = EmployeeProfile
        fields = [
            'id', 'employee', 'employee_name', 'employee_number', 'employee_email',
            'department_name', 'position_title', 'profile_visibility', 'is_profile_public',
            'skills_count', 'endorsements_count', 'created_at', 'updated_at'
        ]
    
    def get_skills_count(self, obj):
        """Get total skills count"""
        return obj.skills.count()
    
    def get_endorsements_count(self, obj):
        """Get total endorsements count"""
        return ProfileEndorsement.objects.filter(profile=obj).count()


class ProfileViewDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for profile view with all related data"""
    employee_name = serializers.CharField(source='employee.first_name', read_only=True)
    employee_number = serializers.CharField(source='employee.employee_number', read_only=True)
    employee_email = serializers.CharField(source='employee.work_email', read_only=True)
    department_name = serializers.CharField(source='employee.department_name', read_only=True)
    position_title = serializers.CharField(source='employee.position_title', read_only=True)
    
    # Extended profile data
    skills = EmployeeSkillSerializer(source='employeeskill_employee', many=True, read_only=True)
    documents = EmployeeDocumentSerializer(source='employeedocument_employee', many=True, read_only=True)
    
    # Profile enrichment data
    endorsements = ProfileEndorsementSerializer(source='profile_endorsement_profile', many=True, read_only=True)
    access_log = ProfileViewAccessSerializer(source='profile_view_access_profile', many=True, read_only=True)
    
    # Profile statistics
    skills_count = serializers.SerializerMethodField()
    certifications_count = serializers.SerializerMethodField()
    endorsements_count = serializers.SerializerMethodField()
    profile_views = serializers.SerializerMethodField()
    
    class Meta:
        model = EmployeeProfile
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_skills_count(self, obj):
        """Get total skills count"""
        return obj.skills.count()
    
    def get_certifications_count(self, obj):
        """Get total certifications count"""
        return obj.employeedocument_employee.count()
    
    def get_endorsements_count(self, obj):
        """Get total endorsements count"""
        return obj.profile_endorsement_profile.count()
    
    def get_profile_views(self, obj):
        """Get total profile views"""
        return obj.profile_view_access_profile.count()


class ProfileEndorsementCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating profile endorsements"""
    
    class Meta:
        model = ProfileEndorsement
        fields = ['skill', 'endorsement_level', 'endorsement_text']
    
    def validate(self, attrs):
        """Validate endorsement data"""
        # Add any custom validation logic here
        return attrs


class ProfileViewAccessCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating profile view access records"""
    
    class Meta:
        model = ProfileViewAccess
        fields = ['profile', 'access_level']
    
    def validate(self, attrs):
        """Validate access data"""
        # Add any custom validation logic here
        return attrs
