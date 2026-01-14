from django.core.management.base import BaseCommand
from hrm.models.toolbar_config import ERPMenuItem
from hrm.views.toolbar_permissions import parse_config_string

class Command(BaseCommand):
    help = 'Add toolbar configuration for HRM_ORG_CHART'

    def add_arguments(self, parser):
        parser.add_argument(
            '--actions',
            type=str,
            default='VEX',
            help='Toolbar actions string (default: VEX for View, Exit, Print, Export)'
        )
    
    def handle(self, *args, **options):
        try:
            # Get or create the menu item
            menu_item, created = ERPMenuItem.objects.get_or_create(
                menu_id='HRM_ORG_CHART',
                defaults={
                    'menu_name': 'Organizational Chart',
                    'toolbar_config': options.get('actions', 'VEX'),
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created new menu item: {menu_item.menu_id}'))
            else:
                menu_item.toolbar_config = options.get('actions', 'VEX')
                menu_item.save()
                self.stdout.write(self.style.SUCCESS(f'Updated existing menu item: {menu_item.menu_id}'))
            
            self.stdout.write(f'Toolbar config: {menu_item.toolbar_config}')
            
            # Test the parsing
            actions = parse_config_string(menu_item.toolbar_config)
            self.stdout.write(f'Actions in config: {actions}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
