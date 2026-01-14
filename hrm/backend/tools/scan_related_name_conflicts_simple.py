#!/usr/bin/env python3
"""
Simple script to scan for related_name conflicts in HRM models.
Focuses on the most critical conflicts that need immediate resolution.
"""

import os
import re
from django.conf import settings
import django
from django.apps import apps

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

def scan_conflicts():
    """Scan for related_name conflicts and return critical ones."""
    
    conflicts = []
    
    # Get all HRM models
    hrm_config = apps.get_app_config('hrm')
    models = hrm_config.get_models()
    
    # Track field relationships
    field_map = {}
    
    for model_class in models:
        model_name = model_class.__name__
        for field in model_class._meta.get_fields():
            if field.many_to_one or field.one_to_many or field.many_to_many:
                # Get the related name
                related_name = getattr(field, 'related_name', None)
                if related_name is None:
                    related_name = f"{model_name.lower()}_set"
                
                # Track this relationship
                key = f"{model_name}.{field.name}"
                if key not in field_map:
                    field_map[key] = []
                field_map[key].append({
                    'model': model_name,
                    'field': field.name,
                    'related_name': related_name,
                    'target_model': field.related_model.__name__ if field.related_model else None
                })
    
    # Find conflicts
    for field_key, relationships in field_map.items():
        if len(relationships) > 1:
            # Check for same related_name
            related_names = {}
            for rel in relationships:
                rn = rel['related_name']
                if rn not in related_names:
                    related_names[rn] = []
                related_names[rn].append(rel)
            
            for rn, rels in related_names.items():
                if len(rels) > 1:
                    conflicts.append({
                        'related_name': rn,
                        'models': rels,
                        'severity': 'HIGH' if 'company' in rn.lower() else 'MEDIUM'
                    })
    
    return conflicts

def main():
    """Main function to scan and report conflicts."""
    print("Scanning for related_name conflicts in HRM models...")
    
    try:
        conflicts = scan_conflicts()
        
        if not conflicts:
            print("No related_name conflicts found!")
            return
        
        print(f"\nFound {len(conflicts)} related_name conflicts:")
        print("=" * 60)
        
        # Sort by severity
        conflicts.sort(key=lambda x: x['severity'], reverse=True)
        
        for conflict in conflicts:
            print(f"\n{conflict['severity']} SEVERITY: {conflict['related_name']}")
            for rel in conflict['models']:
                print(f"   - {rel['model']}.{rel['field']} -> {rel['target_model']}")
        
        # Generate fix suggestions
        print(f"\nSUGGESTED FIXES:")
        print("=" * 60)
        
        for conflict in conflicts[:5]:  # Show first 5 most critical
            related_name = conflict['related_name']
            models = conflict['models']
            
            print(f"\nFor related_name '{related_name}':")
            for i, rel in enumerate(models):
                new_name = f"{rel['model'].lower()}_{rel['field'].lower()}"
                print(f"  {rel['model']}.{rel['field']}: related_name='{new_name}'")
        
    except Exception as e:
        print(f"Error scanning conflicts: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
