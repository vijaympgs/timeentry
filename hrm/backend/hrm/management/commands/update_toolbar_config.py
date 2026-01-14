from django.core.management.base import BaseCommand
from hrm.models.toolbar_config import ERPMenuItem
from hrm.views.toolbar_permissions import parse_config_string

class Command(BaseCommand):
    help = 'Update toolbar configuration for HRM_EMPLOYEE_MASTER'

    def handle(self, *args, **options):
        try:
            # Get the menu item
            hrm_menu = ERPMenuItem.objects.get(menu_id='HRM_EMPLOYEE_MASTER')
            self.stdout.write(f'Current config: {hrm_menu.toolbar_config}')

            # Update to include B (notes), U (attach), G (help)
            hrm_menu.toolbar_config = 'NESCKVDXRQFIOBUG'
            hrm_menu.save()
            self.stdout.write(self.style.SUCCESS(f'Updated config to: {hrm_menu.toolbar_config}'))

            # Test the parsing
            actions = parse_config_string(hrm_menu.toolbar_config)
            self.stdout.write(f'Actions in config: {actions}')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
