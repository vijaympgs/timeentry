#!/usr/bin/env python3
"""
Complete script to fix ALL related_name conflicts in HRM models.
Based on the analysis of 1,234 Django system check errors.

This script will:
1. Parse all model files in hrm/backend/hrm/models/
2. Identify ALL ForeignKey fields without unique related_name arguments
3. Generate appropriate related_name arguments based on conflict patterns
4. Apply fixes systematically to resolve ALL conflicts
5. Handle both fields.E304 and fields.E305 errors
"""

import os
import re
import ast
import sys
from pathlib import Path

class CompleteRelatedNameFixer:
    def __init__(self, models_dir="hrm/backend/hrm/models"):
        self.models_dir = Path(models_dir)
        self.fixes_applied = []
        self.conflicts_found = []
        
        # Comprehensive conflict patterns for ALL models identified in analysis
        self.conflict_patterns = {
            'company': {
                'models': ['ApplicationAnswer', 'ApplicationCandidate', 'ApplicationDocument', 'ApplicationQuestion', 
                          'JobApplication', 'JobPosting', 'AttendanceDevice', 'AttendanceException', 'AttendancePolicy', 
                          'Shift', 'TimeEntry', 'Badge', 'BadgeAward', 'BadgeCategory', 'BadgeNomination', 'RecognitionFeed',
                          'CalibrationSession', 'RatingDistribution', 'RatingGuideline', 'RatingLevel', 'RatingScale', 
                          'ReviewCycle', 'EmployeePosition', 'OrganizationalUnit', 'Position', 'Employee', 'ContractOrganizationalUnit',
                          'ContractPosition', 'ContractTemplate', 'EmploymentContract', 'Course', 'CourseContent', 'CourseSession',
                          'Instructor', 'LearningPath', 'Enrollment', 'EnrollmentApproval', 'EnrollmentCourse', 'EnrollmentCourseSession',
                          'EnrollmentRule', 'EnrollmentTemplate', 'EnrollmentWaitlist', 'PayrollCalculation', 'PayrollDisbursement',
                          'PayrollRun', 'PayrollSchedule', 'EarningCode', 'SalaryStructure', 'CompensationRange', 'JobLevel',
                          'MarketData', 'PayGrade', 'BackgroundCheck', 'BackgroundCheckProvider', 'ScreeningCriteria',
                          'ScreeningProcess', 'ScreeningTemplate', 'TaxCalculation', 'TaxExemption', 'TaxJurisdiction',
                          'TaxPayrollRun', 'TaxRate', 'TaxWithholding', 'Project', 'Task', 'Timesheet', 'TimesheetApproval',
                          'TimesheetEntry'],
                'naming_pattern': '{model_name_lower}_set'
            },
            'user': {
                'models': ['Badge', 'BadgeAward', 'BadgeCategory', 'BadgeNomination', 'CalibrationSession', 'RatingScale',
                          'EmployeePosition', 'OrganizationalUnit', 'Position', 'ContractTemplate', 'EmploymentContract',
                          'Course', 'Enrollment', 'EnrollmentApproval', 'PayrollRun', 'SalaryStructure', 'ScreeningCriteria',
                          'ScreeningProcess', 'Timesheet', 'TimesheetApproval', 'TimesheetEntry', 'TimeEntry', 'AttendanceException'],
                'naming_pattern': '{model_name_lower}_{field_name}'
            },
            'employee': {
                'models': ['EmployeePosition', 'EmployeeDocument', 'EmployeeProfile', 'EmployeeSkill', 'EmployeeRecord',
                          'AttendanceException', 'TimeEntry', 'EmploymentContract', 'Enrollment', 'EnrollmentWaitlist',
                          'PayrollCalculation', 'PayrollDisbursement', 'TaxCalculation', 'TaxExemption', 'TaxWithholding',
                          'Timesheet', 'TimesheetEntry', 'BadgeAward', 'BadgeNomination'],
                'naming_pattern': '{model_name_lower}_{field_name}'
            },
            'jobapplication': {
                'models': ['ApplicationAnswer', 'ApplicationDocument'],
                'naming_pattern': '{model_name_lower}_{field_name}_set'
            },
            'candidate': {
                'models': ['BackgroundCheck', 'ScreeningProcess'],
                'naming_pattern': '{model_name_lower}_{field_name}'
            },
            'course': {
                'models': ['CourseContent', 'CourseSession'],
                'naming_pattern': '{model_name_lower}_{field_name}_set'
            },
            'employee': {
                'models': ['EmployeeDocument', 'EmployeeSkill'],
                'naming_pattern': '{model_name_lower}_{field_name}'
            },
            'employeeprofiles': {
                'models': ['EmployeeDocument', 'EmployeeProfile', 'EmployeeSkill'],
                'naming_pattern': '{model_name_lower}_{field_name}'
            },
            'organizationalunits': {
                'models': ['EmployeePosition', 'OrganizationalUnit', 'Position'],
                'naming_pattern': '{model_name_lower}_{field_name}'
            },
            'organizationalunit': {
                'models': ['EmployeePosition', 'Position'],
                'naming_pattern': '{model_name_lower}_{field_name}_set'
            },
            'ratingscales': {
                'models': ['CalibrationSession', 'RatingDistribution', 'RatingGuideline', 'RatingLevel', 'RatingScale', 'ReviewCycle'],
                'naming_pattern': '{model_name_lower}_set'
            },
            'salarystructures': {
                'models': ['CompensationRange', 'JobLevel', 'MarketData', 'PayGrade', 'SalaryStructure'],
                'naming_pattern': '{model_name_lower}_set'
            },
            'contracttemplates': {
                'models': ['ContractOrganizationalUnit', 'ContractPosition', 'ContractTemplate', 'Employee', 'EmploymentContract'],
                'naming_pattern': '{model_name_lower}_set'
            },
            'courses': {
                'models': ['CourseContent', 'CourseSession', 'Instructor', 'LearningPath'],
                'naming_pattern': '{model_name_lower}_set'
            },
            'enrollments': {
                'models': ['Enrollment', 'EnrollmentApproval', 'EnrollmentCourse', 'EnrollmentCourseSession',
                          'EnrollmentRule', 'EnrollmentTemplate', 'EnrollmentWaitlist'],
                'naming_pattern': '{model_name_lower}_set'
            },
            'offerlettertemplates': {
                'models': ['Candidate', 'OfferLetter', 'OfferLetterTemplate', 'OfferPosition'],
                'naming_pattern': '{model_name_lower}_set'
            },
            'timesheets': {
                'models': ['Project', 'Task', 'Timesheet', 'TimesheetApproval', 'TimesheetEntry'],
                'naming_pattern': '{model_name_lower}_set'
            },
            'screeningprocesses': {
                'models': ['BackgroundCheck', 'BackgroundCheckProvider', 'ScreeningCriteria', 'ScreeningProcess', 'ScreeningTemplate'],
                'naming_pattern': '{model_name_lower}_set'
            },
            'taxcalculations': {
                'models': ['TaxCalculation', 'TaxExemption', 'TaxJurisdiction', 'TaxPayrollRun', 'TaxRate', 'TaxWithholding'],
                'naming_pattern': '{model_name_lower}_set'
            },
            'badges': {
                'models': ['Badge', 'BadgeAward', 'BadgeCategory', 'BadgeNomination', 'RecognitionFeed'],
                'naming_pattern': '{model_name_lower}_set'
            },
            'timesheets': {
                'models': ['Timesheet', 'TimesheetApproval', 'TimesheetEntry'],
                'naming_pattern': '{model_name_lower}_{field_name}'
            },
            'payrollruns': {
                'models': ['PayrollCalculation', 'PayrollDisbursement', 'PayrollRun', 'PayrollSchedule'],
                'naming_pattern': '{model_name_lower}_set'
            },
            'timeentries': {
                'models': ['TimeEntry'],
                'naming_pattern': '{model_name_lower}_{field_name}'
            }
        }

    def get_model_files(self):
        """Get all Python model files."""
        model_files = []
        for file_path in self.models_dir.glob("*.py"):
            if file_path.name != "__init__.py":
                model_files.append(file_path)
        return model_files

    def extract_model_info(self, file_path):
        """Extract model class and field information from a Python file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse the AST
            tree = ast.parse(content)
            
            models_info = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Check if it's a Django model
                    if self.is_django_model(node, content):
                        model_info = {
                            'name': node.name,
                            'file_path': file_path,
                            'fields': []
                        }
                        
                        # Extract field information
                        for item in node.body:
                            if isinstance(item, ast.Assign):
                                for target in item.targets:
                                    if isinstance(target, ast.Name):
                                        field_info = self.extract_field_info(target.id, item.value, content)
                                        if field_info:
                                            model_info['fields'].append(field_info)
                        
                        models_info.append(model_info)
            
            return models_info
            
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return []

    def is_django_model(self, class_node, content):
        """Check if a class is a Django model."""
        # Simple heuristic: check if it has models.Model as a base class
        for base in class_node.bases:
            if isinstance(base, ast.Attribute):
                if (isinstance(base.value, ast.Name) and 
                    base.value.id == 'models' and 
                    base.attr == 'Model'):
                    return True
        return False

    def extract_field_info(self, field_name, field_value, content):
        """Extract information about a Django model field."""
        if isinstance(field_value, ast.Call):
            if isinstance(field_value.func, ast.Attribute):
                if isinstance(field_value.func.value, ast.Name) and field_value.func.value.id == 'models':
                    field_type = field_value.func.attr
                    
                    # Check if it's a ForeignKey or similar relationship field
                    if field_type in ['ForeignKey', 'OneToOneField', 'ManyToManyField']:
                        field_info = {
                            'name': field_name,
                            'type': field_type,
                            'has_related_name': False,
                            'related_name': None,
                            'target_model': None,
                            'line_number': field_value.lineno
                        }
                        
                        # Extract target model
                        if field_value.args:
                            target_arg = field_value.args[0]
                            if isinstance(target_arg, ast.Name):
                                field_info['target_model'] = target_arg.id
                            elif isinstance(target_arg, ast.Attribute):
                                field_info['target_model'] = target_arg.attr
                        
                        # Check for existing related_name
                        for keyword in field_value.keywords:
                            if keyword.arg == 'related_name':
                                field_info['has_related_name'] = True
                                if isinstance(keyword.value, ast.Constant):
                                    field_info['related_name'] = keyword.value.value
                                elif isinstance(keyword.value, ast.Str):
                                    field_info['related_name'] = keyword.value.s
                        
                        return field_info
        
        return None

    def generate_related_name(self, model_name, field_name, target_model):
        """Generate an appropriate related_name based on conflict patterns."""
        model_lower = model_name.lower()
        field_lower = field_name.lower()
        
        # Check if this matches a known conflict pattern
        if target_model and target_model.lower() in self.conflict_patterns:
            pattern = self.conflict_patterns[target_model.lower()]
            if model_name in pattern['models']:
                return pattern['naming_pattern'].format(
                    model_name_lower=model_lower,
                    field_name=field_lower
                )
        
        # Default naming convention
        if field_lower in ['company', 'created_by', 'updated_by', 'employee']:
            return f"{model_lower}_{field_lower}"
        else:
            return f"{model_lower}_{field_lower}_set"

    def identify_conflicts(self, all_models_info):
        """Identify all related_name conflicts."""
        # Group relationships by target model and related_name
        relationships = {}
        
        for model_info in all_models_info:
            for field in model_info['fields']:
                if field['target_model']:
                    key = (field['target_model'], field['related_name'])
                    if key not in relationships:
                        relationships[key] = []
                    relationships[key].append({
                        'model': model_info['name'],
                        'field': field['name'],
                        'file_path': model_info['file_path'],
                        'has_related_name': field['has_related_name'],
                        'line_number': field['line_number']
                    })
        
        # Find conflicts (multiple relationships with same target and related_name)
        conflicts = []
        for (target_model, related_name), rels in relationships.items():
            if len(rels) > 1:
                conflicts.append({
                    'target_model': target_model,
                    'related_name': related_name,
                    'relationships': rels
                })
        
        return conflicts

    def generate_fixes(self, conflicts):
        """Generate fixes for all conflicts."""
        fixes = []
        
        for conflict in conflicts:
            target_model = conflict['target_model']
            related_name = conflict['related_name']
            relationships = conflict['relationships']
            
            # Sort by model name for consistent ordering
            relationships.sort(key=lambda x: x['model'])
            
            # Keep the first one as-is, fix the rest
            for i, rel in enumerate(relationships):
                if i == 0 and rel['has_related_name']:
                    # Keep the original related_name for the first one
                    continue
                
                # Generate a new related_name
                new_related_name = self.generate_related_name(
                    rel['model'], rel['field'], target_model
                )
                
                fix = {
                    'file_path': rel['file_path'],
                    'model_name': rel['model'],
                    'field_name': rel['field'],
                    'line_number': rel['line_number'],
                    'target_model': target_model,
                    'old_related_name': related_name,
                    'new_related_name': new_related_name,
                    'has_existing_related_name': rel['has_related_name']
                }
                
                fixes.append(fix)
        
        return fixes

    def apply_fix_to_file(self, fix):
        """Apply a single fix to a model file."""
        file_path = fix['file_path']
        field_name = fix['field_name']
        new_related_name = fix['new_related_name']
        line_number = fix['line_number']
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Find the field definition (around the line number)
            field_start = None
            field_end = None
            
            for i in range(max(0, line_number - 2), min(len(lines), line_number + 3)):
                if field_name in lines[i]:
                    field_start = i
                    # Find the end of the field definition
                    for j in range(i, len(lines)):
                        if lines[j].strip().endswith(')') and 'models.' in lines[j]:
                            field_end = j + 1
                            break
                    break
            
            if field_start is not None and field_end is not None:
                # Extract the field definition
                field_lines = lines[field_start:field_end]
                field_def = ''.join(field_lines)
                
                # Check if related_name already exists
                if 'related_name=' in field_def:
                    # Replace existing related_name
                    new_field_def = re.sub(
                        r'related_name\s*=\s*["\'][^"\']*["\']',
                        f'related_name="{new_related_name}"',
                        field_def
                    )
                else:
                    # Add related_name before the closing parenthesis
                    new_field_def = re.sub(
                        r'(\s+)(\))',
                        f'\\1, related_name="{new_related_name}"\\2',
                        field_def
                    )
                
                # Replace the field definition
                lines[field_start:field_end] = [new_field_def]
                
                # Write back to file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                
                return True
            else:
                print(f"  Warning: Could not locate field {field_name} in {file_path}")
                return False
                
        except Exception as e:
            print(f"  Error applying fix to {file_path}: {e}")
            return False

    def fix_all_conflicts(self, apply_changes=False):
        """Main method to identify and fix all conflicts."""
        print("Starting COMPLETE related_name conflict fix...")
        print(f"Scanning models directory: {self.models_dir}")
        
        # Get all model files
        model_files = self.get_model_files()
        print(f"Found {len(model_files)} model files")
        
        # Extract model information
        all_models_info = []
        for file_path in model_files:
            print(f"Analyzing {file_path.name}...")
            models_info = self.extract_model_info(file_path)
            all_models_info.extend(models_info)
        
        print(f"Found {len(all_models_info)} models with {sum(len(m['fields']) for m in all_models_info)} fields")
        
        # Identify conflicts
        conflicts = self.identify_conflicts(all_models_info)
        print(f"Identified {len(conflicts)} related_name conflicts")
        
        # Generate fixes
        fixes = self.generate_fixes(conflicts)
        print(f"Generated {len(fixes)} fixes to apply")
        
        # Display conflicts and fixes
        if conflicts:
            print("\nConflict Summary:")
            for i, conflict in enumerate(conflicts[:20], 1):  # Show first 20
                target_model = conflict['target_model']
                related_name = conflict['related_name']
                relationships = conflict['relationships']
                print(f"  {i}. {target_model}.'{related_name}' used by:")
                for rel in relationships:
                    print(f"     - {rel['model']}.{rel['field']}")
            
            if len(conflicts) > 20:
                print(f"  ... and {len(conflicts) - 20} more conflicts")
        
        if fixes:
            print(f"\nFixes to apply:")
            for i, fix in enumerate(fixes[:20], 1):  # Show first 20
                print(f"  {i}. {fix['model_name']}.{fix['field_name']}: {fix['old_related_name']} -> {fix['new_related_name']}")
            
            if len(fixes) > 20:
                print(f"  ... and {len(fixes) - 20} more fixes")
        
        # Apply fixes if requested
        if apply_changes and fixes:
            print(f"\nApplying {len(fixes)} fixes...")
            success_count = 0
            
            for fix in fixes:
                print(f"  Fixing {fix['model_name']}.{fix['field_name']}...")
                if self.apply_fix_to_file(fix):
                    success_count += 1
                    print(f"    Fixed: {fix['old_related_name']} -> {fix['new_related_name']}")
                else:
                    print(f"    Failed to fix")
            
            print(f"\nSuccessfully applied {success_count}/{len(fixes)} fixes")
            
            if success_count > 0:
                print("\nNext steps:")
                print("   1. Run 'python manage.py check' to verify fixes")
                print("   2. Run 'python manage.py makemigrations' if needed")
                print("   3. Test the application")
        
        return {
            'conflicts_found': len(conflicts),
            'fixes_generated': len(fixes),
            'fixes': fixes
        }

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Fix ALL related_name conflicts in HRM models')
    parser.add_argument('--apply', action='store_true', help='Apply fixes to files')
    parser.add_argument('--models-dir', default='hrm/backend/hrm/models', help='Models directory path')
    
    args = parser.parse_args()
    
    # Change to the correct directory
    script_dir = Path(__file__).parent
    backend_dir = script_dir.parent
    os.chdir(backend_dir)
    
    fixer = CompleteRelatedNameFixer(args.models_dir)
    
    try:
        result = fixer.fix_all_conflicts(apply_changes=args.apply)
        
        if not args.apply and result['fixes_generated'] > 0:
            print(f"\nTo apply these fixes, run:")
            print(f"   python {Path(__file__).name} --apply")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
