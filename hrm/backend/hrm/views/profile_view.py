"""
Profile View API Endpoints - Layer 3: Experience/Enrichment Layer
API endpoints for employee profile, skills, certifications, and career development
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Q, Count, Avg
from django.utils import timezone

from ..models.profile_view import (
    EmployeeProfile, Skill, Certification, Language, 
    LearningPath, Aspiration
)
from ..serializers.profile_view import (
    EmployeeProfileSerializer, EmployeeProfileListSerializer, 
    EmployeeProfileDetailSerializer, ProfileUpdateSerializer,
    SkillSerializer, CertificationSerializer, LanguageSerializer,
    LearningPathSerializer, AspirationSerializer,
    SkillEndorsementSerializer, ProfileSearchSerializer,
    ProfileAnalyticsSerializer
)

User = get_user_model()


class EmployeeProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for EmployeeProfile management
    Layer 3: Experience/Enrichment Layer
    """
    serializer_class = EmployeeProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['company', 'profile_visibility', 'is_profile_public']
    search_fields = [
        'employee__first_name', 'employee__last_name', 'employee__employee_number',
        'bio', 'summary', 'interests', 'skills__name', 'certifications__name'
    ]
    ordering_fields = ['created_at', 'updated_at', 'employee__first_name', 'employee__last_name']
    ordering = ['-updated_at']
    
    def get_queryset(self):
        """
        Filter profiles based on user permissions and visibility settings
        """
        user = self.request.user
        queryset = EmployeeProfile.objects.select_related(
            'employee', 'employee__department', 'employee__position', 
            'employee__manager', 'created_by_user', 'updated_by_user'
        ).prefetch_related('skills', 'certifications', 'languages', 'learning_paths')
        
        # Company scoping
        queryset = queryset.filter(company=user.company)
        
        # Visibility filtering based on user role
        if not user.is_staff:  # Non-HR users
            # Employees can see their own profile and public/team profiles
            queryset = queryset.filter(
                Q(employee=user.employee_record) |  # Own profile
                Q(profile_visibility__in=['public', 'company']) |  # Public profiles
                Q(profile_visibility='department', employee__department=user.employee_record.department) |  # Same department
                Q(profile_visibility='team', employee__manager=user.employee_record.manager)  # Same team
            )
        
        return queryset
    
    def get_serializer_class(self):
        """
        Return appropriate serializer based on action
        """
        if self.action == 'list':
            return EmployeeProfileListSerializer
        elif self.action == 'retrieve':
            return EmployeeProfileDetailSerializer
        elif self.action in ['update', 'partial_update']:
            return ProfileUpdateSerializer
        return EmployeeProfileSerializer
    
    @action(detail=False, methods=['post'])
    def search(self, request):
        """
        Advanced profile search with multiple filters
        """
        serializer = ProfileSearchSerializer(data=request.data)
        if serializer.is_valid():
            query = serializer.validated_data['query']
            
            # Build search query
            search_filters = Q()
            
            # Basic text search
            if query:
                search_filters |= Q(employee__first_name__icontains=query)
                search_filters |= Q(employee__last_name__icontains=query)
                search_filters |= Q(employee__employee_number__icontains=query)
                search_filters |= Q(bio__icontains=query)
                search_filters |= Q(summary__icontains=query)
                search_filters |= Q(skills__name__icontains=query)
                search_filters |= Q(certifications__name__icontains=query)
            
            # Skill category filter
            if serializer.validated_data.get('skill_category'):
                search_filters &= Q(skills__skill_category=serializer.validated_data['skill_category'])
            
            # Proficiency level filter
            if serializer.validated_data.get('proficiency_level'):
                search_filters &= Q(skills__proficiency_level=serializer.validated_data['proficiency_level'])
            
            # Department filter
            if serializer.validated_data.get('department'):
                search_filters &= Q(employee__department__name__icontains=serializer.validated_data['department'])
            
            # Position level filter
            if serializer.validated_data.get('position_level'):
                search_filters &= Q(employee__position__level=serializer.validated_data['position_level'])
            
            # Profile visibility filter
            if serializer.validated_data.get('profile_visibility'):
                search_filters &= Q(profile_visibility=serializer.validated_data['profile_visibility'])
            
            # Apply search
            profiles = self.get_queryset().filter(search_filters).distinct()
            
            # Serialize results
            page = self.paginate_queryset(profiles)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(profiles, many=True)
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """
        Get profile analytics and insights
        """
        queryset = self.get_queryset()
        
        # Basic counts
        total_profiles = queryset.count()
        public_profiles = queryset.filter(is_profile_public=True).count()
        
        # Profiles by department
        profiles_by_department = {}
        dept_data = queryset.values('employee__department__name').annotate(count=Count('id'))
        for item in dept_data:
            if item['employee__department__name']:
                profiles_by_department[item['employee__department__name']] = item['count']
        
        # Profiles by position level
        profiles_by_position_level = {}
        level_data = queryset.values('employee__position__level').annotate(count=Count('id'))
        for item in level_data:
            if item['employee__position__level']:
                profiles_by_position_level[f"Level {item['employee__position__level']}"] = item['count']
        
        # Top skills
        top_skills = []
        skill_data = queryset.values('skills__name').annotate(count=Count('skills')).order_by('-count')[:10]
        for item in skill_data:
            if item['skills__name']:
                top_skills.append({'name': item['skills__name'], 'count': item['count']})
        
        # Skill distribution
        skill_distribution = {}
        skill_cat_data = queryset.values('skills__skill_category').annotate(count=Count('skills'))
        for item in skill_cat_data:
            if item['skills__skill_category']:
                skill_distribution[item['skills__skill_category']] = item['count']
        
        # Certification trends (active certifications)
        certification_trends = []
        cert_data = queryset.filter(
            certifications__is_active=True,
            certifications__expiry_date__gte=timezone.now().date()
        ).values('certifications__name').annotate(count=Count('certifications')).order_by('-count')[:10]
        for item in cert_data:
            if item['certifications__name']:
                certification_trends.append({'name': item['certifications__name'], 'count': item['count']})
        
        # Learning path completion (placeholder)
        learning_path_completion = {
            'total_enrolled': queryset.values('learning_paths').count(),
            'completed': 0,  # Would need progress tracking
            'in_progress': 0,  # Would need progress tracking
        }
        
        analytics_data = {
            'total_profiles': total_profiles,
            'public_profiles': public_profiles,
            'profiles_by_department': profiles_by_department,
            'profiles_by_position_level': profiles_by_position_level,
            'top_skills': top_skills,
            'skill_distribution': skill_distribution,
            'certification_trends': certification_trends,
            'learning_path_completion': learning_path_completion
        }
        
        serializer = ProfileAnalyticsSerializer(analytics_data)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def endorse_skill(self, request, pk=None):
        """
        Endorse a skill for an employee profile
        """
        profile = self.get_object()
        serializer = SkillEndorsementSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            skill_id = serializer.validated_data['skill_id']
            endorsement_level = serializer.validated_data['endorsement_level']
            comment = serializer.validated_data.get('comment', '')
            
            try:
                skill = Skill.objects.get(id=skill_id, company=request.user.company)
                
                # Check if skill belongs to the profile
                if not profile.skills.filter(id=skill_id).exists():
                    return Response(
                        {'error': 'Skill not found in this profile'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Create endorsement (you might want to create a separate model for this)
                # For now, just return success
                return Response({
                    'message': 'Skill endorsed successfully',
                    'skill': skill.name,
                    'endorsement_level': endorsement_level,
                    'comment': comment
                })
                
            except Skill.DoesNotExist:
                return Response(
                    {'error': 'Skill not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def my_profile(self, request):
        """
        Get current user's profile
        """
        try:
            profile = EmployeeProfile.objects.get(
                employee=request.user.employee_record,
                company=request.user.company
            )
            serializer = EmployeeProfileDetailSerializer(profile)
            return Response(serializer.data)
        except EmployeeProfile.DoesNotExist:
            return Response(
                {'error': 'Profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def directory(self, request):
        """
        Get employee directory with basic profile information
        """
        queryset = self.get_queryset().filter(
            profile_visibility__in=['public', 'company']
        )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = EmployeeProfileListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = EmployeeProfileListSerializer(queryset, many=True)
        return Response(serializer.data)


class SkillViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Skill management
    """
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['company', 'skill_category', 'proficiency_level', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'skill_category', 'proficiency_level', 'created_at']
    ordering = ['skill_category', 'proficiency_level', 'name']
    
    def get_queryset(self):
        return Skill.objects.filter(company=self.request.user.company)
    
    def perform_create(self, serializer):
        serializer.save(
            company=self.request.user.company,
            created_by_user=self.request.user,
            updated_by_user=self.request.user
        )
    
    def perform_update(self, serializer):
        serializer.save(
            updated_by_user=self.request.user
        )


class CertificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Certification management
    """
    serializer_class = CertificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['company', 'employee', 'skill_category', 'is_active']
    search_fields = ['name', 'issuing_organization', 'credential_id', 'certification_number']
    ordering_fields = ['name', 'issue_date', 'expiry_date', 'created_at']
    ordering = ['-issue_date', 'name']
    
    def get_queryset(self):
        queryset = Certification.objects.filter(company=self.request.user.company)
        
        # Non-HR users can only see their own certifications
        if not self.request.user.is_staff:
            queryset = queryset.filter(employee=self.request.user.employee_record)
        
        return queryset.select_related('employee')
    
    def perform_create(self, serializer):
        serializer.save(
            company=self.request.user.company,
            created_by_user=self.request.user,
            updated_by_user=self.request.user
        )
    
    def perform_update(self, serializer):
        serializer.save(
            updated_by_user=self.request.user
        )
    
    @action(detail=False, methods=['get'])
    def expiring_soon(self, request):
        """
        Get certifications expiring in the next 30 days
        """
        from datetime import timedelta
        
        thirty_days_from_now = timezone.now().date() + timedelta(days=30)
        
        queryset = self.get_queryset().filter(
            expiry_date__lte=thirty_days_from_now,
            expiry_date__gte=timezone.now().date(),
            is_active=True
        )
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class LanguageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Language management
    """
    serializer_class = LanguageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['company', 'proficiency_level', 'is_active']
    search_fields = ['name', 'iso_code']
    ordering_fields = ['name', 'proficiency_level', 'created_at']
    ordering = ['proficiency_level', 'name']
    
    def get_queryset(self):
        return Language.objects.filter(company=self.request.user.company)
    
    def perform_create(self, serializer):
        serializer.save(
            company=self.request.user.company,
            created_by_user=self.request.user,
            updated_by_user=self.request.user
        )
    
    def perform_update(self, serializer):
        serializer.save(
            updated_by_user=self.request.user
        )


class LearningPathViewSet(viewsets.ModelViewSet):
    """
    ViewSet for LearningPath management
    """
    serializer_class = LearningPathSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['company', 'category', 'difficulty_level', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'category', 'difficulty_level', 'created_at']
    ordering = ['difficulty_level', 'name']
    
    def get_queryset(self):
        return LearningPath.objects.filter(company=self.request.user.company)
    
    def perform_create(self, serializer):
        serializer.save(
            company=self.request.user.company,
            created_by_user=self.request.user,
            updated_by_user=self.request.user
        )
    
    def perform_update(self, serializer):
        serializer.save(
            updated_by_user=self.request.user
        )


class AspirationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Aspiration management
    """
    serializer_class = AspirationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['company', 'employee', 'target_role', 'target_role_level', 'time_horizon']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'target_role', 'success_probability', 'created_at']
    ordering = ['success_probability', 'time_horizon']
    
    def get_queryset(self):
        queryset = Aspiration.objects.filter(company=self.request.user.company)
        
        # Non-HR users can only see their own aspirations
        if not self.request.user.is_staff:
            queryset = queryset.filter(employee=self.request.user.employee_record)
        
        return queryset.select_related('employee')
    
    def perform_create(self, serializer):
        serializer.save(
            company=self.request.user.company,
            created_by_user=self.request.user,
            updated_by_user=self.request.user
        )
    
    def perform_update(self, serializer):
        serializer.save(
            updated_by_user=self.request.user
        )
