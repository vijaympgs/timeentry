#!/usr/bin/env python3
"""
Script to update toolbar configurations for all ERPMenuItems
Usage: python update_toolbar_configs.py
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

def update_all_toolbar_configs():
    """Update toolbar configurations for all ERPMenuItems based on menu type"""
    
    # Define toolbar configurations by template type based on bootstrap/06_03_tasks.md
    TOOLBAR_CONFIGS = {
        # Master Data Templates
        'MST-S': 'NESCKVDXRQF',  # Simple Master - Basic operations
        'MST-M': 'NESCKVDXRQFIO',  # Medium Master - Advanced operations
        'MST-C': 'NESCKVDXRQFIO',  # Complex Master - Full operations
        
        # Transaction Templates
        'TXN-S': 'NESCKZTJAVPMRDX1234QF',  # Simple Transaction
        'TXN-M': 'NESCKZTJAVPMRDX1234QF',  # Medium Transaction
        'TXN-C': 'NESCKZTJAVPMRDX1234QF',  # Complex Transaction
        
        # Other Types
        'D': 'VRXPYQFG',  # Dashboard
        'R': 'VRXPYQFG',  # Report
        'C': 'NRQFX',  # Configuration
        'S': 'NRQFX',  # Setup
        'U': 'NRQFX',  # Utility
        'Q': 'NRQFX',  # Query
        'W': 'NESCKZTJAVPMRDX1234QF',  # Workflow
        'A': 'VRXPYQFG',  # Analytics
        
        # Default for legacy 'M' type - use Medium Master
        'M': 'NESCKVDXRQFIO',  # Default Master - Medium Master Template
    }
    
    print("🔧 Updating toolbar configurations for all ERPMenuItems...")
    print("=" * 60)
    
    updated_count = 0
    total_count = ERPMenuItem.objects.count()
    
    for item in ERPMenuItem.objects.all():
        old_config = item.toolbar_config
        new_config = TOOLBAR_CONFIGS.get(item.menu_type, 'NRQFX')
        
        if old_config != new_config:
            item.toolbar_config = new_config
            item.save()
            print(f"✅ Updated: {item.menu_id} ({item.menu_name})")
            print(f"   Type: {item.menu_type}")
            print(f"   Old: {old_config} → New: {new_config}")
            print()
            updated_count += 1
        else:
            print(f"⏭️  Skipped: {item.menu_id} ({item.menu_name}) - Already correct")
    
    print("=" * 60)
    print(f"📊 Summary:")
    print(f"   Total items: {total_count}")
    print(f"   Updated: {updated_count}")
    print(f"   Skipped: {total_count - updated_count}")
    print()
    print("🎉 Toolbar configuration update completed!")

def list_current_configs():
    """List current toolbar configurations for all ERPMenuItems"""
    print("📋 Current ERPMenuItem toolbar configurations:")
    print("=" * 80)
    
    for item in ERPMenuItem.objects.all().order_by('module', 'menu_name'):
        print(f"{item.menu_id:25} | {item.menu_name:30} | {item.menu_type:2} | {item.toolbar_config}")
    
    print("=" * 80)
    print(f"Total: {ERPMenuItem.objects.count()} items")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--list':
        list_current_configs()
    else:
        update_all_toolbar_configs()
