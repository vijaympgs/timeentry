#!/usr/bin/env python3
"""
Phase-4 Migration Defaults Fix Script
Fixes company field default values for migrations
"""

import os
import re
from pathlib import Path

def fix_migration_defaults():
    """Fix company field defaults in models for migrations"""
    
    # Get all Python files in models directory
    models_dir = Path(__file__).parent / 'hrm' / 'models'
    
    if not models_dir.exists():
        print(f"Models directory not found: {models_dir}")
        return
    
    # Files to process
    python_files = list(models_dir.glob('*.py'))
    
    print(f"Found {len(python_files)} Python files to process")
    
    files_updated = 0
    
    for file_path in python_files:
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            updated = False
            
            # Fix company field to be nullable or have default for existing tables
            # This is needed for migrations to work with existing data
            
            # Pattern to find company fields that need fixing
            company_field_pattern = re.compile(
                r'company = models\.ForeignKey\(\s*[\'"]hrm\.Company[\'"],\s*on_delete=models\.CASCADE,\s*related_name=[\'"][^\'\"]*[\'"],?\s*\)',
                re.MULTILINE | re.DOTALL
            )
            
            if company_field_pattern.search(content):
                # Replace with nullable version for migration compatibility
                content = company_field_pattern.sub(
                    "company = models.ForeignKey(\n        'hrm.Company', \n        on_delete=models.CASCADE,\n        related_name='{}',\n        null=True,\n        blank=True".format(
                        # Extract related_name from original match
                        re.search(r'related_name=[\'"]([^\'\"]*)[\'"]', content).group(1) if re.search(r'related_name=[\'"]([^\'\"]*)[\'"]', content) else 'related_name'
                    ),
                    content
                )
                updated = True
            
            # Write back if updated
            if updated:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"Updated {file_path.name}")
                files_updated += 1
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    print(f"\nSummary:")
    print(f"Files updated: {files_updated}")
    print("Migration defaults fixed!")

if __name__ == "__main__":
    fix_migration_defaults()
