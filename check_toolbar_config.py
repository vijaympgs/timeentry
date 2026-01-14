#!/usr/bin/env python3
"""
Script to check ERPMenuItem configuration for a specific menu_id
Usage: python check_toolbar_config.py HRM_EMPLOYEE_MASTER
"""
import sys
import os

# Add the backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'hrm', 'backend')
sys.path.insert(0, backend_path)

# Change to backend directory
os.chdir(backend_path)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

import django
django.setup()

from hrm.models.toolbar_config import ERPMenuItem

def check_menu_config(menu_id):
    """Check and print ERPMenuItem configuration for given menu_id"""
    try:
        item = ERPMenuItem.objects.get(menu_id=menu_id)
        print(f"✅ Found: {item.menu_name} ({item.menu_id})")
        print(f"🔧 Toolbar Config: {item.toolbar_config}")
        print(f"📋 Menu Type: {item.menu_type}")
        print(f"🟢 Is Active: {item.is_active}")
        print(f"📱 App: {item.app}")
        print(f"📂 Module: {item.module}")
        print(f"📁 Submodule: {item.submodule}")
        return item
    except ERPMenuItem.DoesNotExist:
        print(f"❌ {menu_id} not found in ERPMenuItem table")
        print("\n📋 Available items:")
        for item in ERPMenuItem.objects.all():
            print(f"  - {item.menu_id}: {item.menu_name}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_toolbar_config.py <MENU_ID>")
        print("Example: python check_toolbar_config.py HRM_EMPLOYEE_MASTER")
        sys.exit(1)
    
    menu_id = sys.argv[1]
    check_menu_config(menu_id)
