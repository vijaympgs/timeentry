"""
Seed Comprehensive Menu Items for HRM/CRM/FMS Modules
Creates toolbar registry entries based on update_menu_types.py classifications
"""

from django.core.management.base import BaseCommand
from hrm.models.toolbar_config import ERPMenuItem


class Command(BaseCommand):
    help = 'Seed comprehensive menu items for all modules'

    def handle(self, *args, **options):
        # Comprehensive menu items based on update_menu_types.py
        menu_items = [
            # HRM Master Data
            # HRM Master Data
            {'menu_id': 'HRM_EMPLOYEE_MASTER', 'menu_name': 'Employee Master', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Employee Management', 'menu_type': 'MST-C', 'toolbar_config': 'NESCKVDXRQFIO', 'is_active': True},
            {'menu_id': 'HRM_DEPARTMENT_MASTER', 'menu_name': 'Department Master', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Organization', 'menu_type': 'MST-S', 'toolbar_config': 'NESCKVDXRQF', 'description': 'Department Master Data', 'is_active': True},
            {'menu_id': 'HRM_POSITION_MASTER', 'menu_name': 'Position Master', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Organization', 'menu_type': 'MST-S', 'toolbar_config': 'NESCKVDXRQF', 'description': 'Position Master Data', 'is_active': True},
            {'menu_id': 'ORG_ORGANIZATIONAL_UNITS', 'menu_name': 'Organizational Units', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Organization', 'menu_type': 'MST-M', 'toolbar_config': 'NESCKVDXRQFIO', 'description': 'Organizational Unit Master', 'is_active': True},
            {'menu_id': 'ORG_COMPANIES', 'menu_name': 'Companies', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Organization', 'menu_type': 'MST-M', 'toolbar_config': 'NESCKVDXRQFIO', 'description': 'Company Master', 'is_active': True},
            {'menu_id': 'ORG_DEPARTMENTS', 'menu_name': 'Departments', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Organization', 'menu_type': 'MST-S', 'toolbar_config': 'NESCKVDXRQF', 'description': 'Department Master', 'is_active': True},
            {'menu_id': 'ORG_POSITIONS', 'menu_name': 'Positions', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Organization', 'menu_type': 'MST-S', 'toolbar_config': 'NESCKVDXRQF', 'description': 'Position Master', 'is_active': True},
            
            # HRM Time & Attendance
            {'menu_id': 'TIME_TIME_ENTRIES', 'menu_name': 'Time Entries', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Time Management', 'menu_type': 'TXN-S', 'toolbar_config': 'NESCKZTJAVPMRDX1234QF', 'description': 'Time Entry Transactions', 'is_active': True},
            {'menu_id': 'TIME_TIMESHEETS', 'menu_name': 'Timesheets', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Time Management', 'menu_type': 'TXN-S', 'toolbar_config': 'NESCKZTJAVPMRDX1234QF', 'description': 'Timesheet Management', 'is_active': True},
            {'menu_id': 'TIME_SHIFTS', 'menu_name': 'Shifts', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Time Management', 'menu_type': 'MST-S', 'toolbar_config': 'NESCKVDXRQF', 'description': 'Shift Master', 'is_active': True},
            {'menu_id': 'TIME_ATTENDANCE_POLICIES', 'menu_name': 'Attendance Policies', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Time Management', 'menu_type': 'MST-S', 'toolbar_config': 'NESCKVDXRQF', 'description': 'Attendance Policy Master', 'is_active': True},
            
            # HRM Performance
            {'menu_id': 'PERF_RATING_SCALES', 'menu_name': 'Rating Scales', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Performance', 'menu_type': 'MST-M', 'toolbar_config': 'NESCKVDXRQFIO', 'description': 'Rating Scale Master', 'is_active': True},
            {'menu_id': 'PERF_REVIEW_CYCLES', 'menu_name': 'Review Cycles', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Performance', 'menu_type': 'MST-M', 'toolbar_config': 'NESCKVDXRQFIO', 'description': 'Review Cycle Master', 'is_active': True},
            {'menu_id': 'PERF_CALIBRATION_SESSIONS', 'menu_name': 'Calibration Sessions', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Performance', 'menu_type': 'MST-M', 'toolbar_config': 'NESCKVDXRQFIO', 'description': 'Calibration Session Master', 'is_active': True},
            
            # HRM Learning
            {'menu_id': 'LEARN_COURSES', 'menu_name': 'Courses', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Learning', 'menu_type': 'MST-M', 'toolbar_config': 'NESCKVDXRQFIO', 'description': 'Course Master', 'is_active': True},
            {'menu_id': 'LEARN_INSTRUCTORS', 'menu_name': 'Instructors', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Learning', 'menu_type': 'MST-M', 'toolbar_config': 'NESCKVDXRQFIO', 'description': 'Instructor Master', 'is_active': True},
            {'menu_id': 'LEARN_LEARNING_PATHS', 'menu_name': 'Learning Paths', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Learning', 'menu_type': 'MST-M', 'toolbar_config': 'NESCKVDXRQFIO', 'description': 'Learning Path Master', 'is_active': True},
            {'menu_id': 'LEARN_TRAINING_SESSIONS', 'menu_name': 'Training Sessions', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Learning', 'menu_type': 'TXN-M', 'toolbar_config': 'NESCKZTJAVPMRDX1234QF', 'description': 'Training Session Transactions', 'is_active': True},
            {'menu_id': 'HRM_COURSE_CATALOG', 'menu_name': 'Course Catalog', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Learning', 'menu_type': 'MST-M', 'toolbar_config': 'NESCKVDXRQFIO', 'description': 'Course Catalog', 'is_active': True},
            
            # HRM Compensation
            {'menu_id': 'COMP_SALARY_STRUCTURES', 'menu_name': 'Salary Structures', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Compensation', 'menu_type': 'MST-M', 'toolbar_config': 'NESCKVDXRQFIO', 'description': 'Salary Structure Master', 'is_active': True},
            {'menu_id': 'HRM_SALARY_STRUCTURES', 'menu_name': 'Salary Structures', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Compensation', 'menu_type': 'MST-M', 'toolbar_config': 'NESCKVDXRQFIO', 'description': 'Salary Structure Master', 'is_active': True},
            {'menu_id': 'COMP_PAY_GRADES', 'menu_name': 'Pay Grades', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Compensation', 'menu_type': 'MST-M', 'toolbar_config': 'NESCKVDXRQFIO', 'description': 'Pay Grade Master', 'is_active': True},
            {'menu_id': 'COMP_PAYROLL_RUNS', 'menu_name': 'Payroll Runs', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Payroll', 'menu_type': 'TXN-M', 'toolbar_config': 'NESCKZTJAVPMRDX1234QF', 'description': 'Payroll Processing', 'is_active': True},
            
            # HRM Recruitment
            {'menu_id': 'RECR_JOB_APPLICATIONS', 'menu_name': 'Job Applications', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Recruitment', 'menu_type': 'TXN-M', 'toolbar_config': 'NESCKZTJAVPMRDX1234QF', 'description': 'Job Application Transactions', 'is_active': True},
            {'menu_id': 'RECR_JOB_POSTINGS', 'menu_name': 'Job Postings', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Recruitment', 'menu_type': 'MST-M', 'toolbar_config': 'NESCKVDXRQFIO', 'description': 'Job Posting Master', 'is_active': True},
            {'menu_id': 'RECR_SCREENING_PROCESSES', 'menu_name': 'Screening Processes', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Recruitment', 'menu_type': 'TXN-M', 'toolbar_config': 'NESCKZTJAVPMRDX1234QF', 'description': 'Screening Process Transactions', 'is_active': True},
            {'menu_id': 'HRM_OFFER_LETTER', 'menu_name': 'Offer Letter Templates', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Recruitment', 'menu_type': 'MST-M', 'toolbar_config': 'NESCKVDXRQFIO', 'description': 'Offer Letter Template Master', 'is_active': True},
            {'menu_id': 'HRM_CONTRACT_TEMPLATE', 'menu_name': 'Contract Templates', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Recruitment', 'menu_type': 'MST-M', 'toolbar_config': 'NESCKVDXRQFIO', 'description': 'Contract Template Master', 'is_active': True},
            
            # HRM Employee Data
            {'menu_id': 'HRM_EMPLOYEE_ADDRESSES', 'menu_name': 'Employee Addresses', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Employee Management', 'menu_type': 'MST-M', 'toolbar_config': 'NESCKVDXRQFIO', 'description': 'Employee Address Management', 'is_active': True},
            {'menu_id': 'HRM_EMPLOYEE_PROFILES', 'menu_name': 'Employee Profiles', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Employee Management', 'menu_type': 'MST-M', 'toolbar_config': 'NESCKVDXRQFIO', 'description': 'Employee Profile Management', 'is_active': True},
            {'menu_id': 'HRM_EMPLOYEE_DOCUMENTS', 'menu_name': 'Employee Documents', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Employee Management', 'menu_type': 'MST-M', 'toolbar_config': 'NESCKVDXRQFIO', 'description': 'Employee Document Management', 'is_active': True},
            {'menu_id': 'HRM_EMPLOYEE_SKILLS', 'menu_name': 'Employee Skills', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Employee Management', 'menu_type': 'MST-M', 'toolbar_config': 'NESCKVDXRQFIO', 'description': 'Employee Skill Management', 'is_active': True},
            {'menu_id': 'HRM_EMPLOYEE_DIRECTORY', 'menu_name': 'Employee Directory', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Employee Management', 'menu_type': 'MST-M', 'toolbar_config': 'NESCKVDXRQFIO', 'description': 'Employee Directory', 'is_active': True},
            {'menu_id': 'HRM_SKILL_CATEGORIES', 'menu_name': 'Skill Categories', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Employee Management', 'menu_type': 'MST-S', 'toolbar_config': 'NESCKVDXRQF', 'description': 'Skill Category Master', 'is_active': True},
            {'menu_id': 'HRM_ORGANIZATIONAL_CHART', 'menu_name': 'Organizational Chart', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Organization', 'menu_type': 'MST-C', 'toolbar_config': 'NESCKVDXRQFIO', 'description': 'Organizational Hierarchy', 'is_active': True},
            {'menu_id': 'HRM_ORG_CHART', 'menu_name': 'Organization Chart', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Organization', 'menu_type': 'D', 'toolbar_config': 'VRXPYQFG', 'description': 'Organizational Hierarchy Visualization', 'is_active': True},
            {'menu_id': 'HRM_RECOGNITION_BADGES', 'menu_name': 'Recognition Badges', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Recognition', 'menu_type': 'MST-M', 'toolbar_config': 'NESCKVDXRQFIO', 'description': 'Recognition Badge Master', 'is_active': True},
            {'menu_id': 'BADGE_BADGES', 'menu_name': 'Badges', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Recognition', 'menu_type': 'MST-M', 'toolbar_config': 'NESCKVDXRQFIO', 'description': 'Badge Master', 'is_active': True},
            {'menu_id': 'BADGE_AWARDS', 'menu_name': 'Badge Awards', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Recognition', 'menu_type': 'TXN-M', 'toolbar_config': 'NESCKZTJAVPMRDX1234QF', 'description': 'Badge Award Transactions', 'is_active': True},
            {'menu_id': 'BADGE_NOMINATIONS', 'menu_name': 'Badge Nominations', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Recognition', 'menu_type': 'TXN-M', 'toolbar_config': 'NESCKZTJAVPMRDX1234QF', 'description': 'Badge Nomination Transactions', 'is_active': True},
            
            # Dashboards & Views
            {'menu_id': 'HRM_PROFILE_VIEW', 'menu_name': 'Employee Profile', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Employee Management', 'menu_type': 'D', 'toolbar_config': 'VRXPYQFG', 'description': 'Employee Profile View', 'is_active': True},
            {'menu_id': 'HRM_DASHBOARD', 'menu_name': 'HR Dashboard', 'app': 'HRM', 'module': 'HRM', 'submodule': 'Dashboard', 'menu_type': 'D', 'toolbar_config': 'VRXPYQFG', 'description': 'HR Analytics Dashboard', 'is_active': True},
            
            # CRM Master Data
            {'menu_id': 'CRM_CUSTOMERS', 'menu_name': 'Customers', 'app': 'CRM', 'module': 'CRM', 'submodule': 'Customer Management', 'menu_type': 'MST-C', 'toolbar_config': 'NESCKVDXRQFIO', 'description': 'Customer Account Master', 'is_active': True},
            {'menu_id': 'CRM_CONTACTS', 'menu_name': 'Contacts', 'app': 'CRM', 'module': 'CRM', 'submodule': 'Customer Management', 'menu_type': 'MST-M', 'toolbar_config': 'NESCKVDXRQFIO', 'description': 'Contact Master', 'is_active': True},
            {'menu_id': 'CRM_LEADS', 'menu_name': 'Leads', 'app': 'CRM', 'module': 'CRM', 'submodule': 'Sales', 'menu_type': 'TXN-M', 'toolbar_config': 'NESCKZTJAVPMRDX1234QF', 'description': 'Lead Management', 'is_active': True},
            {'menu_id': 'CRM_OPPORTUNITIES', 'menu_name': 'Opportunities', 'app': 'CRM', 'module': 'CRM', 'submodule': 'Sales', 'menu_type': 'TXN-C', 'toolbar_config': 'NESCKZTJAVPMRDX1234QF', 'description': 'Opportunity Management', 'is_active': True},
            {'menu_id': 'CRM_CAMPAIGNS', 'menu_name': 'Campaigns', 'app': 'CRM', 'module': 'CRM', 'submodule': 'Marketing', 'menu_type': 'TXN-M', 'toolbar_config': 'NESCKZTJAVPMRDX1234QF', 'description': 'Campaign Management', 'is_active': True},
            
            # FMS Master Data
            {'menu_id': 'FMS_INVOICES', 'menu_name': 'Invoices', 'app': 'FMS', 'module': 'FMS', 'submodule': 'Accounts Receivable', 'menu_type': 'TXN-M', 'toolbar_config': 'NESCKZTJAVPMRDX1234QF', 'description': 'Invoice Management', 'is_active': True},
            {'menu_id': 'FMS_PAYMENTS', 'menu_name': 'Payments', 'app': 'FMS', 'module': 'FMS', 'submodule': 'Accounts Payable', 'menu_type': 'TXN-M', 'toolbar_config': 'NESCKZTJAVPMRDX1234QF', 'description': 'Payment Management', 'is_active': True},
            {'menu_id': 'FMS_EXPENSE_REPORTS', 'menu_name': 'Expense Reports', 'app': 'FMS', 'module': 'FMS', 'submodule': 'Expense Management', 'menu_type': 'TXN-M', 'toolbar_config': 'NESCKZTJAVPMRDX1234QF', 'description': 'Expense Report Management', 'is_active': True},
            {'menu_id': 'FMS_FINANCIAL_STATEMENTS', 'menu_name': 'Financial Statements', 'app': 'FMS', 'module': 'FMS', 'submodule': 'Reporting', 'menu_type': 'R', 'toolbar_config': 'VRXPYQFG', 'description': 'Financial Statement Reports', 'is_active': True},
            {'menu_id': 'FMS_BUDGETS', 'menu_name': 'Budgets', 'app': 'FMS', 'module': 'FMS', 'submodule': 'Budgeting', 'menu_type': 'MST-M', 'toolbar_config': 'NESCKVDXRQFIO', 'description': 'Budget Master', 'is_active': True},
            {'menu_id': 'FMS_ACCOUNT_CHARTS', 'menu_name': 'Account Charts', 'app': 'FMS', 'module': 'FMS', 'submodule': 'General Ledger', 'menu_type': 'MST-M', 'toolbar_config': 'NESCKVDXRQFIO', 'description': 'Chart of Accounts', 'is_active': True},
            
            # Tax & Compliance
            {'menu_id': 'TAX_CALCULATIONS', 'menu_name': 'Tax Calculations', 'app': 'FMS', 'module': 'FMS', 'submodule': 'Tax', 'menu_type': 'TXN-M', 'toolbar_config': 'NESCKZTJAVPMRDX1234QF', 'is_active': True},
            {'menu_id': 'TAX_WITHHOLDINGS', 'menu_name': 'Tax Withholdings', 'app': 'FMS', 'module': 'FMS', 'submodule': 'Tax', 'menu_type': 'TXN-M', 'toolbar_config': 'NESCKZTJAVPMRDX1234QF', 'is_active': True},
            {'menu_id': 'TAX_JURISDICTIONS', 'menu_name': 'Tax Jurisdictions', 'app': 'FMS', 'module': 'FMS', 'submodule': 'Tax', 'menu_type': 'MST-M', 'toolbar_config': 'NESCKVDXRQFIO', 'is_active': True},
        ]

        created_count = 0
        updated_count = 0

        for item_data in menu_items:
            # Remove description field if it exists
            item_data = {k: v for k, v in item_data.items() if k != 'description'}
            menu_item, created = ERPMenuItem.objects.update_or_create(
                menu_id=item_data['menu_id'],
                defaults=item_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Created: {menu_item.menu_id} - {menu_item.menu_name}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'🔄 Updated: {menu_item.menu_id} - {menu_item.menu_name}')
                )

        self.stdout.write('\n' + '=' * 80)
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Seeding complete!\n'
                f'   Created: {created_count} items\n'
                f'   Updated: {updated_count} items\n'
                f'   Total: {ERPMenuItem.objects.count()} menu items in database\n'
                f'\n📊 By Module:'
            )
        )
        
        # Show counts by module
        for module in ['HRM', 'CRM', 'FMS']:
            count = ERPMenuItem.objects.filter(module=module).count()
            self.stdout.write(f'   {module}: {count} items')
        
        self.stdout.write('\n' + '=' * 80)
