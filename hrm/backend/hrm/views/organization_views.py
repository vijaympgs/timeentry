"""
Organization Chart and Employee Directory API Views
Display-only views using existing EmployeeRecord, EmployeePosition, and OrganizationalUnit models
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import models
from django.db.models import Q, Count, Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from ..models import (
    OrganizationalUnit, 
    Position, 
    EmployeePosition,
    EmployeeRecord,
    EmployeeProfile,
    EmployeeSkill
)
from ..serializers import (
    OrganizationalUnitSerializer,
    PositionSerializer,
    EmployeePositionSerializer,
    EmployeeRecordSerializer,
    EmployeeProfileSerializer
)


class OrganizationChartViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Display-only organization chart view using existing models
    Data Source: EmployeeRecord → EmployeePosition → OrganizationalUnit
    """
    permission_classes = [IsAuthenticated]
    serializer_class = OrganizationalUnitSerializer
    
    def get_queryset(self):
        """Get organizational units with employee counts and managers"""
        return OrganizationalUnit.objects.filter(
            is_active=True
        ).select_related(
            'parent_unit',
            'manager',
            'company'
        ).prefetch_related(
            'child_units'
        ).annotate(
            employee_count=Count(
                'employeeposition_organizational_unit',
                filter=Q(employeeposition_organizational_unit__status='active')
            )
        ).order_by('level', 'sort_order', 'name')
    
    @action(detail=False, methods=['get'])
    @method_decorator(cache_page(300))  # Cache for 5 minutes
    def hierarchy(self, request):
        """
        Get complete organizational hierarchy as tree structure
        Used for organization chart visualization
        """
        try:
            # Get CEO (employees with no manager and hierarchy_level = 0)
            ceo_employees = EmployeeRecord.objects.filter(
                manager__isnull=True,
                hierarchy_level=0,
                is_active=True
            ).order_by('hire_date')
            
            def build_employee_hierarchy(employee):
                """Recursively build employee hierarchy tree"""
                employee_data = {
                    'id': str(employee.id),
                    'employee_number': employee.employee_number,
                    'full_name': employee.full_name,
                    'first_name': employee.first_name,
                    'last_name': employee.last_name,
                    'position_title': employee.position_title,
                    'department_name': employee.department_name,
                    'work_email': employee.work_email,
                    'is_active': employee.is_active,
                    'hierarchy_level': employee.hierarchy_level,
                    'manager_name': employee.manager_name,
                    'children': []
                }
                
                # Get direct reports (employees who report to this employee)
                direct_reports = EmployeeRecord.objects.filter(
                    manager=employee,
                    is_active=True
                ).order_by('hierarchy_level', 'last_name', 'first_name')
                
                # Recursively add direct reports
                for report in direct_reports:
                    employee_data['children'].append(build_employee_hierarchy(report))
                
                return employee_data
            
            # Build complete hierarchy starting from CEO(s)
            hierarchy_data = []
            for ceo in ceo_employees:
                hierarchy_data.append(build_employee_hierarchy(ceo))
            
            # Calculate total levels and employees
            max_level = EmployeeRecord.objects.filter(is_active=True).aggregate(
                models.Max('hierarchy_level')
            )['hierarchy_level__max'] or 0
            
            total_employees = EmployeeRecord.objects.filter(is_active=True).count()
            
            return Response({
                'hierarchy': hierarchy_data,
                'total_employees': total_employees,
                'levels': max_level + 1  # +1 because levels start at 0
            })
            
        except Exception as e:
            return Response(
                {'error': f'Failed to build organization hierarchy: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Search organizational units by name, code, or manager
        """
        query = request.query_params.get('q', '').strip()
        unit_type = request.query_params.get('type', 'all')
        
        if not query:
            return Response(
                {'error': 'Search query is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            queryset = self.get_queryset()
            
            # Apply unit type filter
            if unit_type != 'all':
                queryset = queryset.filter(unit_type=unit_type)
            
            # Apply search filter
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(code__icontains=query) |
                Q(manager__first_name__icontains=query) |
                Q(manager__last_name__icontains=query)
            )
            
            # Serialize results
            serializer = self.get_serializer(queryset, many=True)
            
            return Response({
                'results': serializer.data,
                'count': queryset.count(),
                'query': query,
                'unit_type': unit_type
            })
            
        except Exception as e:
            return Response(
                {'error': f'Search failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class EmployeeDirectoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Display-only employee directory view using existing models
    Data Source: EmployeeRecord, EmployeeProfile, EmployeeSkill, EmployeePosition
    """
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeRecordSerializer
    
    def get_queryset(self):
        """Get employees with their positions and profiles"""
        return EmployeeRecord.objects.filter(
            is_active=True
        ).select_related(
            'company'
        ).prefetch_related(
            'employeeposition_employee_set__position',
            'employeeposition_employee_set__organizational_unit',
            'employee_profile',
            'employee_skill_set'
        ).order_by('last_name', 'first_name')
    
    @action(detail=False, methods=['get'])
    @method_decorator(cache_page(600))  # Cache for 10 minutes
    def directory(self, request):
        """
        Get complete employee directory with filtering and pagination
        """
        try:
            # Get query parameters
            search = request.query_params.get('search', '').strip()
            department = request.query_params.get('department', 'all')
            position = request.query_params.get('position', 'all')
            status_filter = request.query_params.get('status', 'all')
            page = int(request.query_params.get('page', 1))
            per_page = int(request.query_params.get('per_page', 20))
            
            # Start with base queryset
            queryset = EmployeeRecord.objects.all().select_related(
                'company'
            ).prefetch_related(
                'employeeposition_employee_set__position',
                'employeeposition_employee_set__organizational_unit',
                'employee_profile',
                'employee_skill_set'
            )
            
            # Apply filters
            if search:
                queryset = queryset.filter(
                    Q(first_name__icontains=search) |
                    Q(last_name__icontains=search) |
                    Q(employee_number__icontains=search) |
                    Q(email__icontains=search)
                )
            
            if department != 'all':
                queryset = queryset.filter(
                    employeeposition_employee__organizational_unit__name=department
                )
            
            if position != 'all':
                queryset = queryset.filter(
                    employeeposition_employee__position__title=position
                )
            
            if status_filter == 'active':
                queryset = queryset.filter(is_active=True)
            elif status_filter == 'inactive':
                queryset = queryset.filter(is_active=False)
            
            # Get total count
            total_count = queryset.count()
            
            # Apply pagination
            start = (page - 1) * per_page
            end = start + per_page
            employees = queryset[start:end]
            
            # Build employee data
            employee_data = []
            for employee in employees:
                # Get primary position
                primary_position = employee.employeeposition_employee_set.filter(
                    is_primary=True,
                    status='active'
                ).first()
                
                # Get skills
                skills = list(employee.employee_skill_set.values_list('skill_name', flat=True))
                
                # Get profile
                profile = getattr(employee, 'employee_profile', None)
                
                employee_info = {
                    'id': str(employee.id),
                    'employee_number': employee.employee_number,
                    'first_name': employee.first_name,
                    'last_name': employee.last_name,
                    'email': employee.email,
                    'work_phone': employee.work_phone,
                    'mobile_phone': employee.mobile_phone,
                    'position': primary_position.position.title if primary_position and primary_position.position else 'N/A',
                    'department': primary_position.organizational_unit.name if primary_position and primary_position.organizational_unit else 'N/A',
                    'organizational_unit': primary_position.organizational_unit.name if primary_position and primary_position.organizational_unit else 'N/A',
                    'is_active': employee.is_active,
                    'hire_date': employee.hire_date.strftime('%Y-%m-%d') if employee.hire_date else None,
                    'skills': skills,
                    'location': profile.location if profile else None,
                    'avatar': None  # TODO: Add avatar field if needed
                }
                
                employee_data.append(employee_info)
            
            # Get filter options
            departments = list(OrganizationalUnit.objects.filter(
                is_active=True
            ).values_list('name', flat=True).distinct())
            
            positions = list(Position.objects.filter(
                is_active=True
            ).values_list('title', flat=True).distinct())
            
            return Response({
                'employees': employee_data,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total_count,
                    'pages': (total_count + per_page - 1) // per_page
                },
                'filters': {
                    'departments': departments,
                    'positions': positions
                }
            })
            
        except Exception as e:
            return Response(
                {'error': f'Failed to load employee directory: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        """
        Get detailed employee profile
        """
        try:
            employee = self.get_object()
            
            # Get primary position
            primary_position = employee.employeeposition_employee_set.filter(
                is_primary=True,
                status='active'
            ).select_related('position', 'organizational_unit').first()
            
            # Get all positions
            all_positions = employee.employeeposition_employee_set.select_related(
                'position', 'organizational_unit'
            ).order_by('-effective_date')
            
            # Get skills
            skills = list(employee.employee_skill_set.values_list('skill_name', flat=True))
            
            # Get profile
            profile = getattr(employee, 'employee_profile', None)
            
            # Get documents
            documents = list(employee.employeedocument_employee_set.values(
                'document_type', 'title', 'description', 'upload_date'
            ).order_by('-upload_date'))
            
            profile_data = {
                'id': str(employee.id),
                'employee_number': employee.employee_number,
                'first_name': employee.first_name,
                'last_name': employee.last_name,
                'email': employee.email,
                'work_phone': employee.work_phone,
                'mobile_phone': employee.mobile_phone,
                'home_phone': employee.home_phone,
                'address': employee.address,
                'city': employee.city,
                'state': employee.state,
                'postal_code': employee.postal_code,
                'country': employee.country,
                'is_active': employee.is_active,
                'hire_date': employee.hire_date.strftime('%Y-%m-%d') if employee.hire_date else None,
                'birth_date': employee.birth_date.strftime('%Y-%m-%d') if employee.birth_date else None,
                'gender': employee.gender,
                'skills': skills,
                'location': profile.location if profile else None,
                'bio': profile.bio if profile else None,
                'emergency_contact': profile.emergency_contact if profile else None,
                'emergency_phone': profile.emergency_phone if profile else None,
                'primary_position': {
                    'title': primary_position.position.title if primary_position and primary_position.position else 'N/A',
                    'department': primary_position.organizational_unit.name if primary_position and primary_position.organizational_unit else 'N/A',
                    'unit_type': primary_position.organizational_unit.unit_type if primary_position and primary_position.organizational_unit else 'N/A',
                    'employment_type': primary_position.employment_type if primary_position else 'N/A',
                    'start_date': primary_position.effective_date.strftime('%Y-%m-%d') if primary_position and primary_position.effective_date else None
                },
                'all_positions': [
                    {
                        'title': pos.position.title if pos.position else 'N/A',
                        'department': pos.organizational_unit.name if pos.organizational_unit else 'N/A',
                        'employment_type': pos.employment_type,
                        'is_primary': pos.is_primary,
                        'status': pos.status,
                        'effective_date': pos.effective_date.strftime('%Y-%m-%d') if pos.effective_date else None,
                        'end_date': pos.end_date.strftime('%Y-%m-%d') if pos.end_date else None
                    }
                    for pos in all_positions
                ],
                'documents': documents
            }
            
            return Response(profile_data)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to load employee profile: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Get employee directory statistics
        """
        try:
            cache_key = 'employee_directory_stats'
            stats = cache.get(cache_key)
            
            if not stats:
                total_employees = EmployeeRecord.objects.count()
                active_employees = EmployeeRecord.objects.filter(is_active=True).count()
                
                # Department breakdown
                dept_stats = EmployeeRecord.objects.filter(
                    is_active=True
                ).values(
                    'employeeposition_employee__organizational_unit__name'
                ).annotate(
                    count=Count('id')
                ).order_by('-count')
                
                # Position breakdown
                position_stats = EmployeeRecord.objects.filter(
                    is_active=True
                ).values(
                    'employeeposition_employee__position__title'
                ).annotate(
                    count=Count('id')
                ).order_by('-count')
                
                stats = {
                    'total_employees': total_employees,
                    'active_employees': active_employees,
                    'inactive_employees': total_employees - active_employees,
                    'department_breakdown': list(dept_stats),
                    'position_breakdown': list(position_stats)
                }
                
                # Cache for 1 hour
                cache.set(cache_key, stats, 3600)
            
            return Response(stats)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to load statistics: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
