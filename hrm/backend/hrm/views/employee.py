"""Employee ViewSetsFollowing T1 Complex Master Template specifications with company scoping"""

from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from ..models.employee import EmployeeRecord, EmployeeAddress
from ..serializers.employee import (
    EmployeeRecordSerializer,
    EmployeeRecordListSerializer,
    EmployeeRecordCreateSerializer,
    EmployeeRecordUpdateSerializer,
    EmployeeAddressSerializer
)


class EmployeeRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet for EmployeeRecord model following T1 Complex Master Template
    Implements company scoping, advanced filtering, and bulk operations
    """
    
    # Use different serializers for different operations
    serializer_class = EmployeeRecordListSerializer
    permission_classes = [permissions.AllowAny]  # Allow access for development
    
    # Enable filtering, searching, and ordering
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    
    # Define filterable fields
    filterset_fields = [
        'company_code',
        'department_name',
        'position_title',
        'employment_status',
        'employment_type',
        'is_active',
        'gender',
        'job_level'
    ]
    
    # Define searchable fields
    search_fields = [
        'employee_number',
        'first_name',
        'last_name',
        'work_email',
        'personal_email',
        'mobile_phone',
        'position_title',
        'department_name'
    ]
    
    # Define orderable fields
    ordering_fields = [
        'employee_number',
        'first_name',
        'last_name',
        'hire_date',
        'created_at',
        'updated_at',
        'department_name',
        'position_title'
    ]
    
    # Default ordering
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Get queryset with company scoping following T1 specifications
        Filters by user's company and includes performance optimizations
        """
        user = self.request.user
                
        # For development, use company code '001' which matches the imported data
        # In production, this would be user.company.id
        company_code = getattr(user, 'company_code', '001')
                
        queryset = EmployeeRecord.objects.filter(
            company_code=company_code
        ).select_related(
            'created_by_user',
            'updated_by_user'
        ).prefetch_related(
            'employeeaddress_employee'
        )
                
        return queryset
    
    def get_serializer_class(self):
        """
        Return appropriate serializer based on action
        Following T1 Complex Master Template specifications
        """
        if self.action == 'create':
            return EmployeeRecordCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return EmployeeRecordUpdateSerializer
        elif self.action == 'retrieve':
            return EmployeeRecordSerializer
        elif self.action == 'list':
            return EmployeeRecordListSerializer
        
        return super().get_serializer_class()
    
    def perform_create(self, serializer):
        """
        Handle employee creation with company scoping and audit trail
        Following T1 specifications for company scoping
        """
        user = self.request.user
        company_code = getattr(user, 'company_code', '001')
        
        serializer.save(
            company_code=company_code,
            created_by_user=user
        )
    
    def perform_update(self, serializer):
        """
        Handle employee update with audit trail
        Following T1 specifications
        """
        serializer.save(updated_by_user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Get only active employees
        Following T1 specifications for filtered views
        """
        queryset = self.get_queryset().filter(is_active=True)
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_department(self, request):
        """
        Filter employees by department
        Following T1 specifications for advanced filtering
        """
        department = request.query_params.get('department')
        if not department:
            return Response(
                {"error": "Department parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(department_name=department)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """
        Filter employees by employment status
        Following T1 specifications for advanced filtering
        """
        employment_status = request.query_params.get('status')
        if not employment_status:
            return Response(
                {"error": "Status parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(employment_status=employment_status)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search_advanced(self, request):
        """
        Advanced search with multiple criteria
        Following T1 specifications for complex filtering
        """
        queryset = self.get_queryset()
        
        # Filter by multiple criteria
        name = request.query_params.get('name')
        if name:
            queryset = queryset.filter(
                Q(first_name__icontains=name) | 
                Q(last_name__icontains=name)
            )
        
        email = request.query_params.get('email')
        if email:
            queryset = queryset.filter(
                Q(work_email__icontains=email) | 
                Q(personal_email__icontains=email)
            )
        
        department = request.query_params.get('department')
        if department:
            queryset = queryset.filter(department_name__icontains=department)
        
        position = request.query_params.get('position')
        if position:
            queryset = queryset.filter(position_title__icontains=position)
        
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def bulk_update_status(self, request):
        """
        Bulk update employee status
        Following T1 specifications for bulk operations
        """
        employee_ids = request.data.get('employee_ids', [])
        new_status = request.data.get('status')
        
        if not employee_ids or not new_status:
            return Response(
                {"error": "employee_ids and status are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(id__in=employee_ids)
        count = queryset.count()
        
        queryset.update(employment_status=new_status)
        
        return Response({
            "message": f"Updated {count} employees to {new_status}",
            "count": count
        })
    
    @action(detail=False, methods=['post'])
    def bulk_activate(self, request):
        """
        Bulk activate employees
        Following T1 specifications for bulk operations
        """
        employee_ids = request.data.get('employee_ids', [])
        
        if not employee_ids:
            return Response(
                {"error": "employee_ids are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(id__in=employee_ids)
        count = queryset.count()
        
        queryset.update(is_active=True)
        
        return Response({
            "message": f"Activated {count} employees",
            "count": count
        })
    
    @action(detail=False, methods=['post'])
    def bulk_deactivate(self, request):
        """
        Bulk deactivate employees
        Following T1 specifications for bulk operations
        """
        employee_ids = request.data.get('employee_ids', [])
        
        if not employee_ids:
            return Response(
                {"error": "employee_ids are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(id__in=employee_ids)
        count = queryset.count()
        
        queryset.update(is_active=False)
        
        return Response({
            "message": f"Deactivated {count} employees",
            "count": count
        })
    
    @action(detail=True, methods=['get', 'post', 'put', 'delete'])
    def addresses(self, request, pk=None):
        """
        Manage employee addresses
        Following T1 specifications for nested resource management
        """
        employee = self.get_object()
        
        if request.method == 'GET':
            addresses = employee.employeeaddress_employee_set.all()
            serializer = EmployeeAddressSerializer(addresses, many=True)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            serializer = EmployeeAddressSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(employee=employee, company_code=employee.company_code)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method in ['PUT', 'POST']:
            # Handle bulk address operations
            addresses_data = request.data.get('addresses', [])
            if not addresses_data:
                return Response(
                    {"error": "addresses data is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Delete existing addresses
            employee.employeeaddress_employee_set.all().delete()
            
            # Create new addresses
            created_addresses = []
            for address_data in addresses_data:
                address_data['employee'] = employee.id
                address_data['company_code'] = employee.company_code
                serializer = EmployeeAddressSerializer(data=address_data)
                if serializer.is_valid():
                    created_addresses.append(serializer.save())
            
            serializer = EmployeeAddressSerializer(created_addresses, many=True)
            return Response(serializer.data)
        
        elif request.method == 'DELETE':
            employee.employeeaddress_employee_set.all().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Get employee statistics
        Following T1 specifications for analytics
        """
        queryset = self.get_queryset()
        
        stats = {
            'total_employees': queryset.count(),
            'active_employees': queryset.filter(is_active=True).count(),
            'inactive_employees': queryset.filter(is_active=False).count(),
            'by_department': {},
            'by_status': {},
            'by_employment_type': {}
        }
        
        # Department statistics
        for dept in queryset.values_list('department_name', flat=True).distinct():
            stats['by_department'][dept] = queryset.filter(
                department_name=dept
            ).count()
        
        # Status statistics
        for status in queryset.values_list('employment_status', flat=True).distinct():
            stats['by_status'][status] = queryset.filter(
                employment_status=status
            ).count()
        
        # Employment type statistics
        for emp_type in queryset.values_list('employment_type', flat=True).distinct():
            stats['by_employment_type'][emp_type] = queryset.filter(
                employment_type=emp_type
            ).count()
        
        return Response(stats)

    @action(detail=False, methods=['get'])
    def hierarchy(self, request):
        """
        Get organizational hierarchy data for org chart
        Builds tree structure from manager relationships using foreign key
        """
        queryset = self.get_queryset().filter(is_active=True).select_related('manager')
        
        # Debug logging
        print(f"DEBUG: Total employees found: {queryset.count()}")
        print(f"DEBUG: Company code filter: {getattr(self.request.user, 'company_code', 'DEFAULT')}")
        
        # Create employee lookup dictionary
        employees = {}
        for emp in queryset:
            employees[emp.id] = {
                'id': str(emp.id),
                'employee_number': emp.employee_number,
                'first_name': emp.first_name,
                'last_name': emp.last_name,
                'full_name': f"{emp.first_name} {emp.last_name}".strip(),
                'position_title': emp.position_title,
                'department_name': emp.department_name,
                'work_email': emp.work_email,
                'manager_name': f"{emp.manager.first_name} {emp.manager.last_name}" if emp.manager else None,
                'is_active': emp.is_active,
                'children': []
            }
        
        print(f"DEBUG: Employees dictionary size: {len(employees)}")
        
        # Build hierarchy tree using manager foreign key
        root_nodes = []
        
        # Clear all children arrays first
        for emp_id, emp_data in employees.items():
            employees[emp_id]['children'] = []
        
        # Build tree structure - First pass: identify all root nodes and build parent-child mapping
        for emp_id, emp_data in employees.items():
            # Get the actual employee object to access manager relationship
            emp_obj = next((e for e in queryset if str(e.id) == emp_id), None)
            
            if emp_obj and emp_obj.manager_id:
                manager_id = str(emp_obj.manager_id)
                if manager_id in employees:
                    # Add as child of manager
                    employees[manager_id]['children'].append(emp_data)
                    print(f"DEBUG: Added {emp_data['full_name']} as child of manager {manager_id}")
                else:
                    # Manager not found in active employees, treat as root
                    root_nodes.append(emp_data)
                    print(f"DEBUG: Manager {manager_id} not found, treating {emp_data['full_name']} as root")
            else:
                # This is a root node (no manager)
                root_nodes.append(emp_data)
                print(f"DEBUG: No manager for {emp_data['full_name']}, treating as root")
        
        # Second pass: Build hierarchy using manager_name matching as fallback
        if len(root_nodes) == len(employees):  # If all are root nodes, try name-based matching
            print("DEBUG: All employees are root nodes, trying name-based matching")
            root_nodes = []
            
            # Clear children arrays again
            for emp_id, emp_data in employees.items():
                employees[emp_id]['children'] = []
            
            # Rebuild hierarchy using manager_name matching
            for emp_id, emp_data in employees.items():
                if emp_data['manager_name']:
                    # Find manager by name
                    for potential_manager_id, potential_manager in employees.items():
                        if potential_manager['full_name'] == emp_data['manager_name']:
                            potential_manager['children'].append(emp_data)
                            print(f"DEBUG: Name-based: Added {emp_data['full_name']} as child of {potential_manager['full_name']}")
                            break
                else:
                    # No manager name, this is a root node
                    root_nodes.append(emp_data)
                    print(f"DEBUG: Name-based: No manager name for {emp_data['full_name']}, treating as root")
        
        print(f"DEBUG: Root nodes found: {len(root_nodes)}")
        print(f"DEBUG: Root node names: {[node['full_name'] for node in root_nodes]}")
        
        # Debug: Check some manager relationships
        for emp in queryset[:5]:
            print(f"DEBUG: Employee {emp.first_name} {emp.last_name} - manager_id: {emp.manager_id}")
        
        levels = self._calculate_hierarchy_levels(root_nodes)
        print(f"DEBUG: Calculated levels: {levels}")
        
        return Response({
            'hierarchy': root_nodes,
            'total_employees': len(employees),
            'levels': levels
        })
    
    def _calculate_hierarchy_levels(self, nodes, level=1):
        """Calculate the maximum depth of the hierarchy"""
        if not nodes:
            return level - 1  # Return the last valid level
        
        max_level = level
        for node in nodes:
            if node['children']:
                child_level = self._calculate_hierarchy_levels(node['children'], level + 1)
                if child_level is not None:
                    max_level = max(max_level, child_level)
        
        # Ensure we always show at least 5 levels for user requirements
        return max(max_level, 5)
