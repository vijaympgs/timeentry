import os
import django
import sys

# Setup Django environment
sys.path.append('c:/platform/hrm/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrm_backend.settings')
django.setup()

from hrm.models.employee import EmployeeRecord
from django.db.models import Count

def generate_report():
    print("\nORGANIZATIONAL HIERARCHY SUMMARY")
    print("================================")

    # Level 1: CEO
    l1 = EmployeeRecord.objects.filter(hierarchy_level=0)
    print(f"\nLevel 1 (CEO): {l1.count()} Employee(s)")
    for emp in l1:
        count = EmployeeRecord.objects.filter(manager=emp).count()
        print(f"  - {emp.full_name} ({emp.position_title}): {count} Direct Reports (Level 2 VPs)")

    # Level 2: VPs
    l2 = EmployeeRecord.objects.filter(hierarchy_level=1)
    print(f"\nLevel 2 (VPs): {l2.count()} Employee(s)")
    for emp in l2:
        count = EmployeeRecord.objects.filter(manager=emp).count()
        print(f"  - {emp.full_name} ({emp.position_title}): {count} Direct Reports (Level 3 Directors)")

    # Level 3: Directors
    l3 = EmployeeRecord.objects.filter(hierarchy_level=2)
    print(f"\nLevel 3 (Directors): {l3.count()} Employee(s)")
    # Group by manager to see distribution
    # Just listing total reports per director
    for emp in l3:
        count = EmployeeRecord.objects.filter(manager=emp).count()
        print(f"  - {emp.full_name} ({emp.position_title}): {count} Direct Reports (Level 4 Managers)")

    # Level 4: Managers
    l4 = EmployeeRecord.objects.filter(hierarchy_level=3)
    print(f"\nLevel 4 (Managers): {l4.count()} Employee(s)")
    for emp in l4:
        count = EmployeeRecord.objects.filter(manager=emp).count()
        print(f"  - {emp.full_name} ({emp.position_title}): {count} Direct Reports (Level 5 Senior Staff)")

    # Level 5: Senior Staff
    l5 = EmployeeRecord.objects.filter(hierarchy_level=4)
    print(f"\nLevel 5 (Senior Staff): {l5.count()} Employee(s)")
    print("  (These are the managers of the vertical lists)")
    for emp in l5:
        count = EmployeeRecord.objects.filter(manager=emp).count()
        print(f"  - {emp.full_name} ({emp.position_title}): {count} Direct Reports (Level 6 Staff)")

    # Level 6: Staff
    l6 = EmployeeRecord.objects.filter(hierarchy_level=5)
    print(f"\nLevel 6 (Staff): {l6.count()} Employee(s)")
    print("  - Individual Contributors (No Reports)")

    print("\n================================")
    print(f"TOTAL EMPLOYEES: {EmployeeRecord.objects.count()}")

generate_report()
