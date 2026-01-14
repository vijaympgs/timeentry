#!/usr/bin/env python3
"""
Script to analyze Django system check errors and extract conflict information.
This script parses the Django check output to identify the specific conflicts that need fixing.
"""

import os
import re
import subprocess
from django.conf import settings
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

def run_django_check():
    """Run Django check and capture output."""
    try:
        # Get the correct path to manage.py (it's in the parent directory)
        manage_py_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'manage.py')
        
        result = subprocess.run(
            ['python', manage_py_path, 'check'],
            capture_output=True,
            text=True
        )
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        print(f"Error running Django check: {e}")
        return "", str(e), 1

def parse_django_errors(stdout, stderr):
    """Parse Django check output to extract conflict information."""
    
    # Combine stdout and stderr
    all_output = stdout + stderr
    
    # Pattern to match Django field errors
    error_pattern = r'(\w+\.\w+\.\w+):\s*\((fields\.[EWE]\d+)\)\s*(.+?)\n\s*HINT:\s*(.+?)'
    
    errors = re.findall(error_pattern, all_output, re.MULTILINE | re.DOTALL)
    
    conflicts = {}
    
    for error in errors:
        field_path, error_code, description, hint = error
        
        # Extract related_name conflicts
        if 'related_name' in description.lower() or 'related_name' in hint.lower():
            # Parse the conflict details
            if 'clashes with reverse accessor' in description:
                # Extract the related_name that's causing the conflict
                match = re.search(r"'(\w+)'", description)
                if match:
                    related_name = match.group(1)
                    
                    if related_name not in conflicts:
                        conflicts[related_name] = []
                    
                    conflicts[related_name].append({
                        'field': field_path,
                        'error_code': error_code,
                        'description': description.strip(),
                        'hint': hint.strip()
                    })
    
    return conflicts

def analyze_conflicts(conflicts):
    """Analyze the conflicts and suggest fixes."""
    
    print(f"Found {len(conflicts)} related_name conflicts:")
    print("=" * 60)
    
    for related_name, error_list in conflicts.items():
        print(f"\n🔴 CONFLICT: related_name = '{related_name}'")
        print(f"   Affects {len(error_list)} fields:")
        
        for error in error_list:
            field_parts = error['field'].split('.')
            model_name = field_parts[0]
            field_name = field_parts[2]
            
            print(f"   - {model_name}.{field_name}")
            print(f"     Error: {error['error_code']}")
            print(f"     Hint: {error['hint']}")
        
        # Suggest fixes
        print(f"\n   💡 SUGGESTED FIXES:")
        for i, error in enumerate(error_list):
            field_parts = error['field'].split('.')
            model_name = field_parts[0]
            field_name = field_parts[2]
            
            # Generate unique related_name
            if i == 0:
                print(f"   - Keep original: {model_name}.{field_name} (related_name='{related_name}')")
            else:
                new_related_name = f"{model_name.lower()}_{field_name.lower()}"
                print(f"   - Change to: {model_name}.{field_name} (related_name='{new_related_name}')")

def generate_fix_script(conflicts):
    """Generate a script to apply the fixes."""
    
    fix_commands = []
    
    for related_name, error_list in conflicts.items():
        for i, error in enumerate(error_list[1:], 1):  # Skip first one
            field_parts = error['field'].split('.')
            model_name = field_parts[0]
            field_name = field_parts[2]
            
            new_related_name = f"{model_name.lower()}_{field_name.lower()}"
            
            # This would need to be implemented to actually modify the model files
            fix_commands.append(f"# Fix {model_name}.{field_name}")
            fix_commands.append(f"# Change related_name from '{related_name}' to '{new_related_name}'")
    
    return fix_commands

def main():
    """Main function to analyze Django errors."""
    print("Analyzing Django system check errors for HRM-P4-MODEL-STABILIZATION...")
    
    # Run Django check
    stdout, stderr, returncode = run_django_check()
    
    if returncode == 0:
        print("✅ No Django system check errors found!")
        return
    
    print(f"Django check returned {returncode} errors")
    
    # Parse the errors
    conflicts = parse_django_errors(stdout, stderr)
    
    if not conflicts:
        print("No related_name conflicts found in the error output.")
        print("Raw error output:")
        print("=" * 60)
        print(stdout)
        if stderr:
            print("STDERR:")
            print("=" * 60)
            print(stderr)
        return
    
    # Analyze the conflicts
    analyze_conflicts(conflicts)
    
    # Generate fix suggestions
    print(f"\n📝 SUMMARY:")
    print(f"Total conflicts: {len(conflicts)}")
    total_fields = sum(len(error_list) for error_list in conflicts.values())
    print(f"Total fields affected: {total_fields}")
    
    print(f"\n🔧 NEXT STEPS:")
    print("1. Review the suggested fixes above")
    print("2. Manually edit the model files to add unique related_name arguments")
    print("3. Run 'python manage.py check' again to verify fixes")
    print("4. Repeat until all conflicts are resolved")

if __name__ == "__main__":
    main()
