#!/usr/bin/env python3
"""
Phase-3 Domain Reference Fix Script
Updates all 'domain.Company' references to 'hrm.Company' in model files
"""

import os
import re
from pathlib import Path

def fix_domain_references():
    """Fix all domain.Company references to hrm.Company"""
    
    # Get all Python files in models directory
    models_dir = Path(__file__).parent / 'hrm' / 'models'
    
    if not models_dir.exists():
        print(f"Models directory not found: {models_dir}")
        return
    
    # Pattern to find domain.Company references
    domain_pattern = re.compile(r"'domain\.Company'")
    
    # Files to process
    python_files = list(models_dir.glob('**/*.py'))
    
    print(f"Found {len(python_files)} Python files to process")
    
    files_updated = 0
    total_replacements = 0
    
    for file_path in python_files:
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if file contains domain.Company references
            if domain_pattern.search(content):
                # Replace domain.Company with hrm.Company
                updated_content = domain_pattern.sub("'hrm.Company'", content)
                
                # Count replacements
                replacements = len(domain_pattern.findall(content))
                
                # Write back to file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                print(f"Updated {file_path.name}: {replacements} replacements")
                files_updated += 1
                total_replacements += replacements
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    print(f"\nSummary:")
    print(f"Files updated: {files_updated}")
    print(f"Total replacements: {total_replacements}")

if __name__ == "__main__":
    fix_domain_references()
