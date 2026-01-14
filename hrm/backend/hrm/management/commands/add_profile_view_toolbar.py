from django.core.management.base import BaseCommand
from hrm.models import ERPMenuItem


class Command(BaseCommand):
    help = 'Add Profile View toolbar configuration'

    def handle(self, *args, **options):
        # Create or update Profile View toolbar configuration
        menu_item, created = ERPMenuItem.objects.update_or_create(
            menu_id='HRM_PROFILE_VIEW',
            defaults={
                'menu_name': 'Profile View',
                'app': 'HRM',
                'submodule': 'Employee Management',
                'module': 'HRM',
                'menu_type': 'MST-M',  # Medium Master
                'toolbar_config': 'NRQFXVDIOLBUG',  # Standard master config
                'is_active': True
            }
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created Profile View toolbar configuration')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('Successfully updated Profile View toolbar configuration')
            )

        # Display the configuration
        self.stdout.write(f'\nConfiguration Details:')
        self.stdout.write(f'   Menu ID: {menu_item.menu_id}')
        self.stdout.write(f'   Menu Name: {menu_item.menu_name}')
        self.stdout.write(f'   App: {menu_item.app}')
        self.stdout.write(f'   Module: {menu_item.module}')
        self.stdout.write(f'   Submodule: {menu_item.submodule}')
        self.stdout.write(f'   Menu Type: {menu_item.menu_type}')
        self.stdout.write(f'   Toolbar Config: {menu_item.toolbar_config}')
        self.stdout.write(f'   Is Active: {menu_item.is_active}')
