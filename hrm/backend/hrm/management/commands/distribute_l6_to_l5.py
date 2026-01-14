from django.core.management.base import BaseCommand
from hrm.models.employee import EmployeeRecord

class Command(BaseCommand):
    help = 'Distribute Level 6 employees equally among all Level 5 managers'

    def handle(self, *args, **options):
        self.stdout.write('Fetching employees...')
        
        # Get Level 5 managers (Senior Staff)
        # hierarchy_level is 0-indexed: L5 is index 4
        l5_managers = list(EmployeeRecord.objects.filter(hierarchy_level=4))
        
        if not l5_managers:
            self.stdout.write(self.style.ERROR('No Level 5 managers found!'))
            return

        self.stdout.write(f'Found {len(l5_managers)} Level 5 managers.')

        # Get Level 6 employees (Staff)
        # hierarchy_level is 0-indexed: L6 is index 5
        l6_employees = list(EmployeeRecord.objects.filter(hierarchy_level=5))
        
        if not l6_employees:
            self.stdout.write(self.style.ERROR('No Level 6 employees found!'))
            return

        self.stdout.write(f'Found {len(l6_employees)} Level 6 employees.')
        self.stdout.write('Distributing L6 employees equally among L5 managers...')

        # Distribute equally
        updates = []
        for i, emp in enumerate(l6_employees):
            manager = l5_managers[i % len(l5_managers)]
            emp.manager = manager
            # Use specific position title to match manager's department if needed
            # But keeping current role/title is safer, or update dept?
            # User request only mentioned "Distribute L6 records equally"
            # We should probably update the department to match the new manager's department
            emp.department_name = manager.department_name
            emp.position_title = f'{manager.department_name} Specialist' # Standardize title
            updates.append(emp)

        # Batch update
        EmployeeRecord.objects.bulk_update(updates, ['manager', 'department_name', 'position_title'])

        self.stdout.write(self.style.SUCCESS(f'Successfully updated {len(updates)} Level 6 employees.'))
        self.stdout.write(self.style.SUCCESS(f'Each Level 5 manager now has ~{len(l6_employees) // len(l5_managers)} reports.'))
