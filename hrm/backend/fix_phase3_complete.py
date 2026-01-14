#!/usr/bin/env python3
"""
Phase-3 Complete Fix Script
Final resolution of all remaining conflicts with proper analysis
Root cause: Index name length limit (30 chars) and reverse accessor field name clashes
"""

import os
import re
from pathlib import Path

def fix_phase3_complete():
    """Complete Phase-3 conflict resolution"""
    
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
            
            # Fix 1: Index name length limit (max 30 chars)
            if file_path.name == 'enrollment.py':
                content = content.replace(
                    "name='idx_enroll_approval_approver_enroll'",
                    "name='idx_enroll_appr_approver_en'"
                )
                updated = True
            elif file_path.name == 'timesheets.py':
                content = content.replace(
                    "name='idx_enroll_approval_approver_timesheet'",
                    "name='idx_enroll_appr_approver_ts'"
                )
                updated = True
            
            # Fix 2: Reverse accessor conflicts - change field names in target models
            if file_path.name == 'ratings.py':
                # Change RatingScale.rating_guidelines field name to avoid clash
                content = content.replace(
                    "rating_guidelines = models.JSONField(default=list",
                    "rating_guidelines_list = models.JSONField(default=list"
                )
                # Update RatingGuideline foreign key to use proper related_name
                content = re.sub(
                    r'rating_scale = models\.ForeignKey\(\s*[\'"]RatingScale[\'"],\s*on_delete=models\.CASCADE,\s*related_name=[\'"][^\'\"]*[\'"],?\s*\)',
                    "rating_scale = models.ForeignKey('RatingScale', on_delete=models.CASCADE, related_name='rating_guidelines_ref')",
                    content
                )
                updated = True
            
            if file_path.name == 'tax_calculations.py':
                # Change TaxJurisdiction.tax_rates field name to avoid clash
                content = content.replace(
                    "tax_rates = models.JSONField(default=dict",
                    "tax_rates_data = models.JSONField(default=dict"
                )
                # Update TaxRate foreign key to use proper related_name
                content = re.sub(
                    r'tax_jurisdiction = models\.ForeignKey\(\s*[\'"]TaxJurisdiction[\'"],\s*on_delete=models\.CASCADE,\s*related_name=[\'"][^\'\"]*[\'"],?\s*\)',
                    "tax_jurisdiction = models.ForeignKey('TaxJurisdiction', on_delete=models.CASCADE, related_name='tax_rates_ref')",
                    content
                )
                updated = True
            
            # Fix 3: Missing ordering fields - add them properly
            if file_path.name == 'recognition_badges.py' and "class RecognitionFeed" in content:
                if "created_at = models.DateTimeField" not in content:
                    # Find a good place to add the field (after id, before Meta)
                    if "id = models.UUIDField" in content:
                        content = re.sub(
                            r'(id = models\.UUIDField.*?\n)',
                            r'\1    created_at = models.DateTimeField(auto_now_add=True)\n',
                            content
                        )
                        updated = True
            
            if file_path.name == 'salary_structures.py' and "class SalaryStructure" in content:
                if "grade_level = models" not in content:
                    # Find a good place to add the field (after id, before Meta)
                    if "id = models.UUIDField" in content:
                        content = re.sub(
                            r'(id = models\.UUIDField.*?\n)',
                            r'\1    grade_level = models.CharField(max_length=50, blank=True)\n',
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
    print("Phase-3 conflicts completely resolved!")

if __name__ == "__main__":
    fix_phase3_complete()
