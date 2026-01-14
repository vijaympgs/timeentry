#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from hrm.models.toolbar_config import ERPMenuItem

print(f'Total ERP Menu Items: {ERPMenuItem.objects.count()}')
print('Menu Items by Module:')
for module in ERPMenuItem.objects.values_list('module', flat=True).distinct():
    count = ERPMenuItem.objects.filter(module=module).count()
    print(f'  {module}: {count}')

print('\nAll Menu Items:')
for item in ERPMenuItem.objects.all().order_by('module', 'menu_name'):
    print(f'  {item.module} - {item.menu_name} ({item.menu_id})')
