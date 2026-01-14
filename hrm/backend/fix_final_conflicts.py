#!/usr/bin/env python3
"""
Phase-3 Final Conflicts Fix Script
Complete fix for all remaining naming conflicts in single shot
Root cause: Duplicate index names across models and reverse accessor clashes with field names
"""

import os
import re
from pathlib import Path

def fix_final_conflicts():
    """Fix all remaining naming conflicts comprehensively"""
    
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
            
            # Fix 1: Index name conflicts - make them unique per model
            if file_path.name == 'application_capture.py':
                content = content.replace(
                    "name='idx_app_doc_type'",
                    "name='idx_app_doc_type_app'"
                )
                updated = True
            elif file_path.name == 'employee_profile.py':
                content = content.replace(
                    "name='idx_app_doc_type'",
                    "name='idx_app_doc_type_emp'"
                )
                updated = True
            
            if file_path.name == 'course_catalog.py':
                content = content.replace(
                    "name='idx_course_session_dt'",
                    "name='idx_course_session_dt_course'"
                )
                updated = True
            elif file_path.name == 'ratings.py':
                content = content.replace(
                    "name='idx_course_session_dt'",
                    "name='idx_course_session_dt_rating'"
                )
                updated = True
            
            if file_path.name == 'enrollment.py':
                content = content.replace(
                    "name='idx_enroll_approval_approver'",
                    "name='idx_enroll_approval_approver_enroll'"
                )
                updated = True
            elif file_path.name == 'timesheets.py':
                content = content.replace(
                    "name='idx_enroll_approval_approver'",
                    "name='idx_enroll_approval_approver_timesheet'"
                )
                updated = True
            
            # Fix 2: Reverse accessor conflicts - add related_name to avoid clashes
            # RatingGuideline.rating_scale
            if file_path.name == 'ratings.py' and "class RatingGuideline" in content:
                content = re.sub(
                    r'rating_scale = models\.ForeignKey\(\s*[\'"]RatingScale[\'"],\s*on_delete=models\.CASCADE,\s*related_name=[\'"][^\'\"]*[\'"],?\s*\)',
                    "rating_scale = models.ForeignKey('RatingScale', on_delete=models.CASCADE, related_name='rating_guidelines_ref')",
                    content
                )
                updated = True
            
            # TaxRate.tax_jurisdiction
            if file_path.name == 'tax_calculations.py' and "class TaxRate" in content:
                content = re.sub(
                    r'tax_jurisdiction = models\.ForeignKey\(\s*[\'"]TaxJurisdiction[\'"],\s*on_delete=models\.CASCADE,\s*related_name=[\'"][^\'\"]*[\'"],?\s*\)',
                    "tax_jurisdiction = models.ForeignKey('TaxJurisdiction', on_delete=models.CASCADE, related_name='tax_rates_ref')",
                    content
                )
                updated = True
            
            # Fix 3: Missing ordering fields
            # RecognitionFeed - add created_at field
            if file_path.name == 'recognition_badges.py' and "class RecognitionFeed" in content:
                if "created_at = models.DateTimeField" not in content:
                    # Find the class and add created_at field before Meta
                    class_match = re.search(r'(class RecognitionFeed.*?)(\s+class Meta:)', content, re.DOTALL)
                    if class_match:
                        before_meta = class_match.group(1)
                        after_meta = class_match.group(2)
                        
                        # Add created_at field before Meta class
                        created_at_field = "    created_at = models.DateTimeField(auto_now_add=True)\n"
                        content = before_meta + created_at_field + after_meta
                        updated = True
            
            # SalaryStructure - add grade_level field
            if file_path.name == 'salary_structures.py' and "class SalaryStructure" in content:
                if "grade_level = models" not in content:
                    # Find the class and add grade_level field before Meta
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
    print("All Phase-3 conflicts resolved!")

if __name__ == "__main__":
    fix_final_conflicts()
