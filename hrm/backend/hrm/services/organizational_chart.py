p"""Organizational Chart Service - HRM DomainFollowing platform.cline governance - Generate org chart from Employee Records"""
from typing import Dict, List, Any
from ..models.employee import EmployeeRecord


class OrganizationalChartService:
    """Service to generate organizational chart from existing Employee Records"""
    
    @staticmethod
    def build_org_chart_from_employees(company_id: str) -> Dict[str, Any]:
        """
        Build organizational chart hierarchy from Employee Records
        
        Args:
            company_id: Company UUID for filtering
            
        Returns:
            Dict containing organizational hierarchy
        """
        # Get all active employees for the company
        employees = EmployeeRecord.objects.filter(
            company_id=company_id,
            is_active=True
        ).select_related('reports_to').order_by('department', 'job_title', 'first_name')
        
        # Build hierarchy from reporting relationships
        org_chart = OrganizationalChartService._build_hierarchy(employees)
        
        # Generate department structure
        departments = OrganizationalChartService._build_departments(employees)
        
        return {
            'hierarchy': org_chart,
            'departments': departments,
            'total_employees': employees.count(),
            'stats': OrganizationalChartService._calculate_stats(employees)
        }
    
    @staticmethod
    def _build_hierarchy(employees) -> List[Dict[str, Any]]:
        """Build reporting hierarchy from employee relationships"""
        # Create employee lookup dict
        employee_dict = {}
        root_employees = []
        
        for emp in employees:
            employee_data = {
                'id': str(emp.id),
                'name': f"{emp.first_name} {emp.last_name}",
                'employee_id': emp.employee_id,
                'job_title': emp.job_title,
                'department': emp.department,
                'email': emp.email,
                'is_manager': False,
                'direct_reports': [],
                'level': 0
            }
            employee_dict[str(emp.id)] = employee_data
        
        # Build reporting relationships
        for emp in employees:
            emp_id = str(emp.id)
            if emp.reports_to:
                manager_id = str(emp.reports_to.id)
                if manager_id in employee_dict:
                    employee_dict[manager_id]['direct_reports'].append(employee_dict[emp_id])
                    employee_dict[manager_id]['is_manager'] = True
            else:
                root_employees.append(employee_dict[emp_id])
        
        # Calculate hierarchy levels
        def calculate_levels(employees, level=0):
            for emp in employees:
                emp['level'] = level
                calculate_levels(emp['direct_reports'], level + 1)
        
        calculate_levels(root_employees)
        
        return root_employees
    
    @staticmethod
    def _build_departments(employees) -> List[Dict[str, Any]]:
        """Build department structure from employee data"""
        dept_dict = {}
        
        for emp in employees:
            dept_name = emp.department or 'Unassigned'
            if dept_name not in dept_dict:
                dept_dict[dept_name] = {
                    'name': dept_name,
                    'employee_count': 0,
                    'managers': [],
                    'employees': []
                }
            
            dept_dict[dept_name]['employee_count'] += 1
            dept_dict[dept_name]['employees'].append({
                'id': str(emp.id),
                'name': f"{emp.first_name} {emp.last_name}",
                'job_title': emp.job_title,
                'email': emp.email,
                'is_manager': emp.reports_to is None  # Simplified - check if anyone reports to them
            })
        
        # Identify managers in each department
        for emp in employees:
            if emp.reports_to is None:  # Top level employees
                dept_name = emp.department or 'Unassigned'
                if dept_name in dept_dict:
                    dept_dict[dept_name]['managers'].append({
                        'id': str(emp.id),
                        'name': f"{emp.first_name} {emp.last_name}",
                        'job_title': emp.job_title
                    })
        
        return list(dept_dict.values())
    
    @staticmethod
    def _calculate_stats(employees) -> Dict[str, Any]:
        """Calculate organizational statistics"""
        total_employees = employees.count()
        managers = employees.filter(reports_to__isnull=True).count()
        individual_contributors = total_employees - managers
        
        # Department distribution
        dept_counts = {}
        for emp in employees:
            dept = emp.department or 'Unassigned'
            dept_counts[dept] = dept_counts.get(dept, 0) + 1
        
        # Job level distribution
        job_levels = {}
        for emp in employees:
            level = emp.job_level or 'Unspecified'
            job_levels[level] = job_levels.get(level, 0) + 1
        
        return {
            'total_employees': total_employees,
            'managers': managers,
            'individual_contributors': individual_contributors,
            'manager_to_ic_ratio': round(managers / individual_contributors, 2) if individual_contributors > 0 else 0,
            'departments': len(dept_counts),
            'department_distribution': dept_counts,
            'job_level_distribution': job_levels
        }
    
    @staticmethod
    def get_employee_reporting_structure(employee_id: str) -> Dict[str, Any]:
        """Get complete reporting structure for a specific employee"""
        try:
            employee = EmployeeRecord.objects.get(id=employee_id)
            
            # Get manager chain (upward)
            manager_chain = []
            current_manager = employee.reports_to
            level = 1
            while current_manager:
                manager_chain.append({
                    'id': str(current_manager.id),
                    'name': f"{current_manager.first_name} {current_manager.last_name}",
                    'job_title': current_manager.job_title,
                    'level': level
                })
                current_manager = current_manager.reports_to
                level += 1
            
            # Get direct reports (downward)
            direct_reports = EmployeeRecord.objects.filter(
                reports_to=employee,
                is_active=True
            ).order_by('job_title', 'first_name')
            
            reports_data = []
            for report in direct_reports:
                reports_data.append({
                    'id': str(report.id),
                    'name': f"{report.first_name} {report.last_name}",
                    'job_title': report.job_title,
                    'department': report.department,
                    'email': report.email
                })
            
            return {
                'employee': {
                    'id': str(employee.id),
                    'name': f"{employee.first_name} {employee.last_name}",
                    'job_title': employee.job_title,
                    'department': employee.department,
                    'email': employee.email
                },
                'manager_chain': manager_chain,
                'direct_reports': reports_data,
                'direct_reports_count': len(reports_data)
            }
            
        except EmployeeRecord.DoesNotExist:
            return {'error': 'Employee not found'}
