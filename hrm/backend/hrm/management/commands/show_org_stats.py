from django.core.management.base import BaseCommand
from hrm.models.employee import EmployeeRecord

class Command(BaseCommand):
    help = 'Show distinct summary of org hierarchy'

    def handle(self, *args, **options):
        self.stdout.write("\nORGANIZATIONAL HIERARCHY SUMMARY")
        self.stdout.write("================================")

        # Level 1: CEO
        l1 = EmployeeRecord.objects.filter(hierarchy_level=0)
        self.stdout.write(f"\nLevel 1 (CEO): {l1.count()} Employee(s)")
        for emp in l1:
            count = EmployeeRecord.objects.filter(manager=emp).count()
            self.stdout.write(f"  - {emp.full_name}: {count} Reports (VPs)")

        # Level 2: VPs
        l2 = EmployeeRecord.objects.filter(hierarchy_level=1)
        self.stdout.write(f"\nLevel 2 (VPs): {l2.count()} Employee(s)")
        for emp in l2:
            count = EmployeeRecord.objects.filter(manager=emp).count()
            self.stdout.write(f"  - {emp.full_name}: {count} Reports (Directors)")

        # Level 3: Directors
        l3 = EmployeeRecord.objects.filter(hierarchy_level=2)
        self.stdout.write(f"\nLevel 3 (Directors): {l3.count()} Employee(s)")
        for emp in l3:
            count = EmployeeRecord.objects.filter(manager=emp).count()
            self.stdout.write(f"  - {emp.full_name}: {count} Reports (Managers)")

        # Level 4: Managers
        l4 = EmployeeRecord.objects.filter(hierarchy_level=3)
        self.stdout.write(f"\nLevel 4 (Managers): {l4.count()} Employee(s)")
        for emp in l4:
            count = EmployeeRecord.objects.filter(manager=emp).count()
            self.stdout.write(f"  - {emp.full_name}: {count} Reports (Senior Staff)")

        # Level 5: Senior Staff
        l5 = EmployeeRecord.objects.filter(hierarchy_level=4)
        self.stdout.write(f"\nLevel 5 (Senior Staff): {l5.count()} Employee(s)")
        for emp in l5:
            count = EmployeeRecord.objects.filter(manager=emp).count()
            self.stdout.write(f"  - {emp.full_name}: {count} Reports (Level 6 Staff)")

        # Level 6: Staff
        l6 = EmployeeRecord.objects.filter(hierarchy_level=5)
        self.stdout.write(f"\nLevel 6 (Staff): {l6.count()} Employee(s)")

        self.stdout.write("\n================================")
        self.stdout.write(f"TOTAL: {EmployeeRecord.objects.count()}")
