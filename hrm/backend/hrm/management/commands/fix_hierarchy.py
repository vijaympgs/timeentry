from django.core.management.base import BaseCommand
from hrm.models.employee import EmployeeRecord


class Command(BaseCommand):
    help = 'Fix organizational hierarchy relationships'

    def handle(self, *args, **options):
        self.stdout.write("=== FIXING ORGANIZATIONAL HIERARCHY ===\n")
        
        # Get CEO
        ceo = EmployeeRecord.objects.filter(
            position_title__icontains='Chief Executive Officer'
        ).first()
        
        if not ceo:
            self.stdout.write("ERROR: CEO not found!")
            return
            
        self.stdout.write(f"CEO: {ceo.first_name} {ceo.last_name}")
        
        # Fix VP relationships - VPs report to CEO
        vps = EmployeeRecord.objects.filter(position_title__icontains='VP of')
        self.stdout.write(f"\nFound {vps.count()} VPs to update:")
        
        for vp in vps:
            vp.manager = ceo
            vp.save()
            self.stdout.write(f"  Updated VP {vp.first_name} {vp.last_name} -> CEO")
        
        # Fix Senior Manager relationships
        managers = EmployeeRecord.objects.filter(position_title__icontains='Senior Manager')
        self.stdout.write(f"\nFound {managers.count()} Senior Managers to update:")
        
        for mgr in managers:
            vp = None
            if 'Engineering' in mgr.position_title:
                vp = EmployeeRecord.objects.filter(
                    position_title__icontains='VP of Engineering'
                ).first()
            elif 'HR' in mgr.position_title:
                vp = EmployeeRecord.objects.filter(
                    position_title__icontains='VP of Human Resources'
                ).first()
            elif 'Finance' in mgr.position_title:
                vp = EmployeeRecord.objects.filter(
                    position_title__icontains='VP of Finance'
                ).first()
            elif 'Marketing' in mgr.position_title:
                vp = EmployeeRecord.objects.filter(
                    position_title__icontains='VP of Marketing'
                ).first()
            elif 'Sales' in mgr.position_title:
                vp = EmployeeRecord.objects.filter(
                    position_title__icontains='VP of Sales'
                ).first()
            elif 'Operations' in mgr.position_title:
                vp = EmployeeRecord.objects.filter(
                    position_title__icontains='VP of Operations'
                ).first()
            elif 'Customer Support' in mgr.position_title:
                vp = EmployeeRecord.objects.filter(
                    position_title__icontains='VP of Customer Support'
                ).first()
            elif 'IT' in mgr.position_title:
                vp = EmployeeRecord.objects.filter(
                    position_title__icontains='VP of Information Technology'
                ).first()
            
            if vp:
                mgr.manager = vp
                mgr.save()
                self.stdout.write(f"  Updated Manager {mgr.first_name} {mgr.last_name} -> {vp.first_name} {vp.last_name}")
        
        # Fix Specialist relationships - Specialists report to Senior Managers
        specialists = EmployeeRecord.objects.filter(
            position_title__icontains='Specialist'
        )
        self.stdout.write(f"\nFound {specialists.count()} Specialists to update:")
        
        for spec in specialists:
            manager = None
            if 'Engineering' in spec.department_name:
                manager = EmployeeRecord.objects.filter(
                    position_title__icontains='Senior Engineering Manager'
                ).first()
            elif 'HR' in spec.department_name:
                manager = EmployeeRecord.objects.filter(
                    position_title__icontains='Senior HR Manager'
                ).first()
            elif 'Finance' in spec.department_name:
                manager = EmployeeRecord.objects.filter(
                    position_title__icontains='Senior Finance Manager'
                ).first()
            elif 'Marketing' in spec.department_name:
                manager = EmployeeRecord.objects.filter(
                    position_title__icontains='Senior Marketing Manager'
                ).first()
            elif 'Sales' in spec.department_name:
                manager = EmployeeRecord.objects.filter(
                    position_title__icontains='Senior Sales Manager'
                ).first()
            elif 'Operations' in spec.department_name:
                manager = EmployeeRecord.objects.filter(
                    position_title__icontains='Senior Operations Manager'
                ).first()
            elif 'Customer Support' in spec.department_name:
                manager = EmployeeRecord.objects.filter(
                    position_title__icontains='Senior Customer Support Manager'
                ).first()
            elif 'IT' in spec.department_name:
                manager = EmployeeRecord.objects.filter(
                    position_title__icontains='Senior IT Manager'
                ).first()
            
            if manager:
                spec.manager = manager
                spec.save()
                self.stdout.write(f"  Updated Specialist {spec.first_name} {spec.last_name} -> {manager.first_name} {manager.last_name}")
        
        self.stdout.write("\n=== HIERARCHY RELATIONSHIPS UPDATED ===")
