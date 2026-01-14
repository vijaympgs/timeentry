#!/usr/bin/env python3
"""
Phase-3 Remaining Conflicts Fix Script
Fixes remaining index name length and reverse accessor issues
"""

import os
import re
from pathlib import Path

def fix_remaining_conflicts():
    """Fix remaining naming conflicts in model files"""
    
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
            
            # Fix 1: Index name length issues (max 30 chars)
            index_length_fixes = {
                "idx_enrollment_approval_approver": "idx_enroll_approval_approver",
                "idx_application_document_type": "idx_app_doc_type",
                "idx_course_session_date": "idx_course_session_dt"
            }
            
            for old_name, new_name in index_length_fixes.items():
                if f"name='{old_name}'" in content:
                    content = content.replace(f"name='{old_name}'", f"name='{new_name}'")
                    updated = True
            
            # Fix 2: Reverse accessor conflicts with field names
            # RatingGuideline.rating_scale - change field name instead of related_name
            if "rating_guidelines = models.JSONField(default=list" in content and "RatingGuideline" in content:
                content = content.replace(
                    "rating_guidelines = models.JSONField(default=list",
                    "rating_guidelines_data = models.JSONField(default=list"
                )
                updated = True
            
            # TaxJurisdiction.tax_rates - change field name instead of related_name
            if "tax_rates = models.JSONField(default=dict" in content and "TaxJurisdiction" in content:
                content = content.replace(
                    "tax_rates = models.JSONField(default=dict",
                    "tax_rates_data = models.JSONField(default=dict"
                )
                updated = True
            
            # Fix 3: Missing ordering fields
            # RecognitionFeed - add created_at field if missing
            if "class RecognitionFeed" in content and "created_at = models.DateTimeField" not in content:
                # Find the class and add created_at field
                class_match = re.search(r'(class RecognitionFeed.*?)(\s+class Meta:)', content, re.DOTALL)
                if class_match:
                    before_meta = class_match.group(1)
                    after_meta = class_match.group(2)
                    
                    # Add created_at field before Meta class
                    created_at_field = "    created_at = models.DateTimeField(auto_now_add=True)\n"
                    content = before_meta + created_at_field + after_meta
                    updated = True
            
            # SalaryStructure - add grade_level field if missing
            if "class SalaryStructure" in content and "grade_level = models" not in content:
                # Find the class and add grade_level field
                class_match = re.search(r'(class SalaryStructure.*?)(\s+class Meta:)', content, re.DOTALL)
                if class_match:
                    before_meta = class_match.group(1)
                    after_meta = class_match.group(2)
                    
                    # Add grade_level field before Meta class
                    grade_level_field = "    grade_level = models.CharField(max_length=50, blank=True)\n"
                    content = before_meta + grade_level_field + after_meta
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

if __name__ == "__main__":
    fix_remaining_conflicts()
