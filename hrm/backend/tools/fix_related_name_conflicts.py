#!/usr/bin/env python3
"""
Script to fix related_name conflicts in HRM models.
This script will systematically add unique related_name arguments to resolve Django system check errors.
"""

import os
import re
from django.conf import settings
import django
from django.apps import apps

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

def generate_unique_related_name(model_name, field_name, target_model_name):
    """Generate a unique related_name based on model and field names."""
    return f"{model_name.lower()}_{field_name.lower()}"

def fix_model_conflicts():
    """Fix related_name conflicts by adding unique related_name arguments."""
    
    # Get all HRM models
    hrm_config = apps.get_app_config('hrm')
    models = hrm_config.get_models()
    
    # Track conflicts and fixes
    conflicts_found = []
    fixes_applied = []
    
    # First pass: identify all relationships and their related_names
    for model_class in models:
        model_name = model_class.__name__
        for field in model_class._meta.get_fields():
            if field.many_to_one or field.one_to_many or field.many_to_many:
                # Get the actual related_name from the field
                related_name = getattr(field, 'related_name', None)
                
                conflicts_found.append({
                    'model': model_name,
                    'field_name': field.name,
                    'field': field,
                    'related_name': related_name,
                    'target_model': field.related_model.__name__ if field.related_model else None
                })
    
    # Group by related_name to find conflicts
    related_name_groups = {}
    for conflict in conflicts_found:
        rn = conflict['related_name']
        if rn is not None:  # Only consider explicit related_names
            if rn not in related_name_groups:
                related_name_groups[rn] = []
            related_name_groups[rn].append(conflict)
    
    # Find actual conflicts (multiple fields with same related_name)
    actual_conflicts = {rn: group for rn, group in related_name_groups.items() if len(group) > 1}
    
    print(f"Found {len(actual_conflicts)} related_name conflicts to fix:")
    
    # Generate fixes for conflicts
    for related_name, conflicts in actual_conflicts.items():
        print(f"\nFixing conflicts for related_name: '{related_name}'")
        
        for i, conflict in enumerate(conflicts):
            model_name = conflict['model']
            field_name = conflict['field_name']
            target_model = conflict['target_model']
            
            # Generate unique related_name (skip first one to keep original)
            if i == 0:
                print(f"  Keeping original: {model_name}.{field_name} -> {related_name}")
                continue
            
            # Generate unique related_name for subsequent conflicts
            unique_name = generate_unique_related_name(model_name, field_name, target_model)
            
            fix = {
                'model_file': f"hrm/backend/hrm/models/{model_name.lower()}.py",
                'model_name': model_name,
                'field_name': field_name,
                'old_related_name': related_name,
                'new_related_name': unique_name,
                'target_model': target_model
            }
            fixes_applied.append(fix)
            
            print(f"  {model_name}.{field_name}: {related_name} -> {unique_name}")
    
    return fixes_applied

def apply_fixes_to_files(fixes):
    """Apply the fixes to the actual model files."""
    
    print(f"\nApplying {len(fixes)} fixes to model files...")
    
    for fix in fixes:
        file_path = fix['model_file']
        model_name = fix['model_name']
        field_name = fix['field_name']
        old_related_name = fix['old_related_name']
        new_related_name = fix['new_related_name']
        
        if not os.path.exists(file_path):
            print(f"Warning: File {file_path} not found, skipping fix for {model_name}.{field_name}")
            continue
        
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the field definition and add/modify related_name
        # This is a simplified approach - in practice, you might need more sophisticated parsing
        field_pattern = rf'(\s+{field_name}\s*=\s*models\.\w+.*?)(\s*$)'
        
        # Try to find existing related_name
        related_name_pattern = rf'(\s+{field_name}\s*=\s*models\.\w+.*?related_name\s*=\s*["\']{re.escape(old_related_name)}["\'].*?)(\s*$)'
        
        if re.search(related_name_pattern, content, re.MULTILINE | re.DOTALL):
            # Replace existing related_name
            new_content = re.sub(
                related_name_pattern,
                f'\\1related_name=\'{new_related_name}\'\\2',
                content,
                flags=re.MULTILINE | re.DOTALL
            )
            print(f"  Updated existing related_name in {file_path}")
        else:
            # Add related_name to the field
            field_pattern = rf'(\s+{field_name}\s*=\s*models\.\w+[^,\n]*?)(\s*$)'
            if re.search(field_pattern, content, re.MULTILINE):
                new_content = re.sub(
                    field_pattern,
                    f'\\1, related_name=\'{new_related_name}\'\\2',
                    content,
                    flags=re.MULTILINE
                )
                print(f"  Added new related_name to {file_path}")
            else:
                print(f"  Warning: Could not find field {field_name} in {file_path}")
                continue
        
        # Write the updated content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  Fixed: {model_name}.{field_name} -> {new_related_name}")

def main():
    """Main function to fix related_name conflicts."""
    print("Starting HRM-P4-MODEL-STABILIZATION: Fixing related_name conflicts...")
    
    try:
        # Identify conflicts and generate fixes
        fixes = fix_model_conflicts()
        
        if not fixes:
            print("No related_name conflicts found!")
            return
        
        print(f"\nGenerated {len(fixes)} fixes to apply.")
        
        # Ask for confirmation before applying fixes
        response = input("\nDo you want to apply these fixes? (y/N): ").strip().lower()
        
        if response == 'y':
            apply_fixes_to_files(fixes)
            print(f"\nApplied {len(fixes)} fixes successfully!")
            print("Run 'python manage.py check' again to verify the fixes.")
        else:
            print("Fixes not applied. Run the script again with 'y' to apply fixes.")
        
    except Exception as e:
        print(f"Error fixing conflicts: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
