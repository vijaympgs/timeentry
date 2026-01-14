#!/usr/bin/env python3
"""
SCRIPT 2 — CANONICAL RELATED_NAME FIXER
Use AST to safely modify Python files and apply canonical naming rules
"""

import os
import ast
import sys
import re
from pathlib import Path
from copy import deepcopy

class RelatedNameFixer(ast.NodeTransformer):
    def __init__(self, model_name):
        self.model_name = model_name
        self.canonical_name = self.get_canonical_name(model_name)
        self.modified = False
        
    def get_canonical_name(self, model_name):
        """Convert model name to canonical plural lowercase related_name"""
        # Handle common pluralization rules
        if model_name.endswith('y'):
            # City -> cities, Company -> companies
            return model_name[:-1] + 'ies'
        elif model_name.endswith(('s', 'ss', 'sh', 'ch', 'x', 'z')):
            # Class -> classes, Box -> boxes
            return model_name + 'es'
        elif model_name.endswith('f'):
            # Wolf -> wolves
            return model_name[:-1] + 'ves'
        elif model_name.endswith('fe'):
            # Life -> lives
            return model_name[:-2] + 'ves'
        else:
            # Default: just add 's'
            return model_name.lower() + 's'
    
    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            field_type = node.func.attr
            if field_type in ['ForeignKey', 'OneToOneField', 'ManyToManyField']:
                # Check if this has a related_name argument
                for i, keyword in enumerate(node.keywords):
                    if keyword.arg == 'related_name':
                        # Replace the related_name value
                        if isinstance(keyword.value, ast.Constant):
                            old_value = keyword.value.value
                            if old_value != self.canonical_name:
                                # Create new Constant node with canonical name
                                new_keyword = ast.keyword(
                                    arg='related_name',
                                    value=ast.Constant(value=self.canonical_name)
                                )
                                node.keywords[i] = new_keyword
                                self.modified = True
                                print(f"  Fixed: {old_value} -> {self.canonical_name}")
                        break
        
        return self.generic_visit(node)

def fix_model_file(file_path, model_name):
    """Fix related_name in a single model file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse AST
        tree = ast.parse(content)
        
        # Apply fixes
        fixer = RelatedNameFixer(model_name)
        fixed_tree = fixer.visit(tree)
        
        if fixer.modified:
            # Convert back to source code
            fixed_content = ast.unparse(fixed_tree)
            
            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            return True
        else:
            return False
            
    except Exception as e:
        print(f"ERROR fixing {file_path}: {e}")
        return False

def get_model_name_from_file(file_path):
    """Extract model class name from file using regex for better compatibility"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Use regex to find Django model classes
        import re
        class_pattern = re.compile(r'class\s+(\w+)\s*\(models\.Model\):')
        match = class_pattern.search(content)
        
        if match:
            return match.group(1)
        
        return None
        
    except Exception as e:
        print(f"ERROR extracting model name from {file_path}: {e}")
        return None

def main():
    """Main execution"""
    models_dir = Path(__file__).parent.parent / 'hrm' / 'models'
    
    if not models_dir.exists():
        print(f"ERROR: Models directory not found: {models_dir}")
        sys.exit(1)
    
    print("=" * 80)
    print("CANONICAL RELATED_NAME FIXER")
    print("=" * 80)
    
    files_fixed = 0
    
    for py_file in models_dir.glob('*.py'):
        if py_file.name == '__init__.py':
            continue
        
        print(f"\nProcessing: {py_file.name}")
        
        model_name = get_model_name_from_file(py_file)
        if not model_name:
            print("  No Django model found")
            continue
        
        print(f"  Model: {model_name}")
        
        if fix_model_file(py_file, model_name):
            files_fixed += 1
            print("  FIXED")
        else:
            print("  No changes needed")
    
    print("\n" + "=" * 80)
    print(f"SUMMARY: Fixed {files_fixed} files")
    print("=" * 80)
    
    if files_fixed > 0:
        print("\nRELATED NAMES CANONICALIZED")
        print("Run validate_models.py to verify all conflicts are resolved")
    else:
        print("\nALL RELATED NAMES ALREADY CANONICAL")

if __name__ == "__main__":
    main()
