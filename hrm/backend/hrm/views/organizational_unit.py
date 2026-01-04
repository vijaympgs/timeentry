"""Organizational Chart Views - HRM DomainFollowing platform.cline governance - Generate org chart from Employee Records"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models.employee import EmployeeRecord


class OrganizationalChartViewSet(viewsets.ViewSet):
    """Organizational Chart ViewSet - Generated from Employee Records"""
    
    permission_classes = []  # Allow unauthenticated access for development
    
    @action(detail=False, methods=['get'])
    def chart(self, request):
        """Get organizational chart generated from Employee Records"""
        try:
            # Get all employees and build hierarchy
            employees = EmployeeRecord.objects.filter(is_active=True).order_by('position_title', 'last_name', 'first_name')
            
            # Build department structure
            departments = {}
            for emp in employees:
                dept_name = emp.department_name or 'Unassigned'
                if dept_name not in departments:
                    departments[dept_name] = {
                        'name': dept_name,
                        'employees': [],
                        'manager': None
                    }
                
                employee_data = {
                    'id': str(emp.id),
                    'name': f"{emp.first_name} {emp.last_name}",
                    'employee_id': emp.employee_number,
                    'position': emp.position_title,
                    'department': emp.department_name,
                    'email': emp.work_email,
                    'is_manager': self.is_manager_position(emp.position_title)
                }
                
                departments[dept_name]['employees'].append(employee_data)
                
                # Identify managers (simplified logic)
                if emp.position_title and ('Manager' in emp.position_title or 'Director' in emp.position_title or 'VP' in emp.position_title or 'CEO' in emp.position_title):
                    if not departments[dept_name]['manager']:
                        departments[dept_name]['manager'] = employee_data
            
            # Build hierarchy structure
            hierarchy = []
            for dept_name, dept_data in departments.items():
                dept_unit = {
                    'id': dept_name.replace(' ', '_').lower(),
                    'name': dept_name,
                    'code': dept_name[:3].upper(),
                    'unit_type': 'department',
                    'level': 1,
                    'is_active': True,
                    'parent_unit_id': None,
                    'manager_id': dept_data['manager']['id'] if dept_data['manager'] else None,
                    'employee_count': len(dept_data['employees']),
                    'children': []
                }
                
                # Add manager as first child
                if dept_data['manager']:
                    dept_unit['children'].append({
                        'id': dept_data['manager']['id'],
                        'name': dept_data['manager']['name'],
                        'code': dept_data['manager']['employee_id'],
                        'unit_type': 'manager',
                        'level': 2,
                        'is_active': True,
                        'parent_unit_id': dept_unit['id'],
                        'manager_id': None,
                        'employee_count': 1,
                        'children': []
                    })
                
                # Add other employees
                for emp in dept_data['employees']:
                    if emp != dept_data['manager']:
                        dept_unit['children'].append({
                            'id': emp['id'],
                            'name': emp['name'],
                            'code': emp['employee_id'],
                            'unit_type': 'employee',
                            'level': 3,
                            'is_active': True,
                            'parent_unit_id': dept_unit['id'],
                            'manager_id': dept_data['manager']['id'] if dept_data['manager'] else None,
                            'employee_count': 1,
                            'children': []
                        })
                
                hierarchy.append(dept_unit)
            
            return Response({
                'hierarchy': hierarchy,
                'departments': list(departments.keys()),
                'total_employees': employees.count(),
                'total_departments': len(departments)
            })
            
        except Exception as e:
            return Response(
                {'error': f'Failed to generate organizational chart: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def is_manager_position(self, position_title):
        """Simple heuristic to determine if a position is a manager role"""
        if not position_title:
            return False
        
        manager_keywords = ['manager', 'director', 'vp', 'vice president', 'ceo', 'chief', 'head', 'lead', 'supervisor']
        position_lower = position_title.lower()
        
        return any(keyword in position_lower for keyword in manager_keywords)
