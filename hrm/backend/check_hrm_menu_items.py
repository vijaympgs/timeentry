#!/usr/bin/env python
import os
import sys
import django

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from hrm.models.toolbar_config import ERPMenuItem

def check_hrm_menu_items():
    """Check all HRM menu items and their toolbar configurations"""
    print("=== HRM Menu Items Investigation ===")
    
    try:
        items = ERPMenuItem.objects.filter(module='HRM').order_by('menu_id')
        
        if not items.exists():
            print("No HRM menu items found in database")
            return
        
        print(f"\nFound {items.count()} HRM menu items:")
        print("-" * 60)
        
        for item in items:
            print(f"Menu ID: {item.menu_id}")
            print(f"Name: {item.menu_name}")
            print(f"Submodule: {item.submodule}")
            print(f"View Type: {item.view_type}")
            print(f"Toolbar Config: {item.applicable_toolbar_config}")
            print(f"Route: {item.route_path}")
            print(f"Active: {item.is_active}")
            print("-" * 60)
            
    except Exception as e:
        print(f"Error checking HRM menu items: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_hrm_menu_items()
