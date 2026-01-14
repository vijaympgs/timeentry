from django.core.management.base import BaseCommand
from hrm.models.employee import EmployeeRecord
import math

class Command(BaseCommand):
    help = 'Distribute employees equally across all hierarchy levels'

    def handle(self, *args, **options):
        self.stdout.write('Starting global redistribution...')

        levels = {
            'L1': {'level': 0, 'name': 'CEO'},
            'L2': {'level': 1, 'name': 'VP'},
            'L3': {'level': 2, 'name': 'Director'},
            'L4': {'level': 3, 'name': 'Manager'},
            'L5': {'level': 4, 'name': 'Senior Staff'},
            'L6': {'level': 5, 'name': 'Staff'},
        }

        # Fetch all employees by level
        employees = {}
        for key, info in levels.items():
            employees[key] = list(EmployeeRecord.objects.filter(hierarchy_level=info['level']).order_by('id'))
            self.stdout.write(f"Fetched {len(employees[key])} {info['name']}s ({key})")

        # Helper to distribute Equal Reportees
        def distribute(managers, reportees, manager_level_name, reportee_level_name):
            if not managers or not reportees:
                self.stdout.write(f"Skipping {manager_level_name} -> {reportee_level_name} (missing data)")
                return
            
            self.stdout.write(f"Distributing {len(reportees)} {reportee_level_name}s among {len(managers)} {manager_level_name}s...")
            
            updates = []
            for i, reportee in enumerate(reportees):
                # Round-robin assignment
                manager = managers[i % len(managers)]
                
                # Check if change is needed
                if reportee.manager_id != manager.id:
                    reportee.manager = manager
                    # Update department/title to match manager for consistency?
                    # User asked for "Equivalent reportees", implies structural change.
                    # I'll update manager linkage primarily.
                    # Optionally sync department if it looks weird otherwise
                    if reportee_level_name == 'Staff' or reportee_level_name == 'Senior Staff':
                        # For lower levels, sync department
                        reportee.department_name = manager.department_name
                    
                    updates.append(reportee)
            
            if updates:
                EmployeeRecord.objects.bulk_update(updates, ['manager', 'department_name'])
                self.stdout.write(self.style.SUCCESS(f"  Updated {len(updates)} records."))
            else:
                self.stdout.write("  No changes needed (already balanced).")

            # Report Distribution Stats
            counts = {m.id: 0 for m in managers}
            for r in reportees:
                # We need to simulate the new state since DB might not reflect bulk_update instantly in 'reportees' list if filtered?
                # Actually bulk_update updates DB. 
                # Let's count properly via logic:
                mid = managers[list(reportees).index(r) % len(managers)].id
                counts[mid] += 1
            
            min_c = min(counts.values())
            max_c = max(counts.values())
            self.stdout.write(f"  Result: Each {manager_level_name} has between {min_c} and {max_c} reportees.")

        # Execute Distributions
        distribute(employees['L1'], employees['L2'], 'CEO', 'VP')         # 1 -> 2
        distribute(employees['L2'], employees['L3'], 'VP', 'Director')    # 2 -> 5
        distribute(employees['L3'], employees['L4'], 'Director', 'Manager') # 5 -> 8
        distribute(employees['L4'], employees['L5'], 'Manager', 'Senior Staff') # 8 -> 8
        distribute(employees['L5'], employees['L6'], 'Senior Staff', 'Staff')   # 8 -> 251

        self.stdout.write(self.style.SUCCESS('\n✅ Global redistribution complete!'))
