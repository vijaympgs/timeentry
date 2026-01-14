#!/usr/bin/env python3
"""
SCRIPT 1 — MODEL SCANNER & CONFLICT DETECTOR
Walk ALL files under hrm/models/ and detect ALL ForeignKey/OneToOne/ManyToMany related_name conflicts
"""

import os
import ast
import sys
from pathlib import Path
from collections import defaultdict

class ModelFieldScanner(ast.NodeVisitor):
    def __init__(self, file_path):
        self.file_path = file_path
        self.current_class = None
        self.fields = []
        
    def visit_ClassDef(self, node):
        # Only process Django model classes
        if any(base.id == 'Model' for base in node.bases if isinstance(base, ast.Name)):
            self.current_class = node.name
            self.generic_visit(node)
        self.current_class = None
        
    def visit_Call(self, node):
        if self.current_class:
            # Check for ForeignKey, OneToOneField, ManyToManyField calls
            if isinstance(node.func, ast.Attribute):
                field_type = node.func.attr
                if field_type in ['ForeignKey', 'OneToOneField', 'ManyToManyField']:
                    field_info = self.extract_field_info(node, field_type)
                    if field_info:
                        self.fields.append(field_info)
        self.generic_visit(node)
        
    def extract_field_info(self, node, field_type):
        field_name = None
        related_name = None
        target_model = None
        
        for keyword in node.keywords:
            if keyword.arg == 'related_name':
                if isinstance(keyword.value, ast.Constant):
                    related_name = keyword.value.value
                elif isinstance(keyword.value, ast.Str):  # Python < 3.8 compatibility
                    related_name = keyword.value.s
            elif keyword.arg == 'to':
                if isinstance(keyword.value, ast.Constant):
                    target_model = keyword.value.value
                elif isinstance(keyword.value, ast.Str):  # Python < 3.8 compatibility
                    target_model = keyword.value.s
                
        # Try to get field name from assignment - look for parent Assign nodes
        current = node
        while hasattr(current, 'parent'):
            current = current.parent
            if isinstance(current, ast.Assign):
                for target in current.targets:
                    if isinstance(target, ast.Name):
                        field_name = target.id
                        break
                break
        
        return {
            'file': str(self.file_path),
            'model': self.current_class,
            'field': field_name,
            'type': field_type,
            'target_model': target_model,
            'related_name': related_name
        }

def scan_model_files(models_dir):
    """Scan all Python files in models directory"""
    all_fields = []
    
    for py_file in models_dir.glob('*.py'):
        if py_file.name == '__init__.py':
            continue
            
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST
            tree = ast.parse(content)
            
            # Set parent references for field name detection
            for node in ast.walk(tree):
                for child in ast.iter_child_nodes(node):
                    child.parent = node
            
            scanner = ModelFieldScanner(py_file)
            scanner.visit(tree)
            all_fields.extend(scanner.fields)
            
        except Exception as e:
            print(f"ERROR scanning {py_file}: {e}")
            
    return all_fields

def detect_conflicts(fields):
    """Detect related_name conflicts per target model"""
    conflicts = defaultdict(list)
    
    # Group by target model and related_name
    target_groups = defaultdict(lambda: defaultdict(list))
    
    for field in fields:
        if field['related_name'] and field['target_model']:
            target_groups[field['target_model']][field['related_name']].append(field)
    
    # Find conflicts (same related_name for same target model)
    for target_model, related_groups in target_groups.items():
        for related_name, field_list in related_groups.items():
            if len(field_list) > 1:
                conflicts[target_model].extend(field_list)
    
    return conflicts

def generate_report(conflicts):
    """Generate conflict report"""
    print("=" * 80)
    print("RELATED NAME CONFLICTS REPORT")
    print("=" * 80)
    
    if not conflicts:
        print("NO CONFLICTS FOUND")
        return
        
    total_conflicts = sum(len(fields) for fields in conflicts.values())
    print(f"FOUND {total_conflicts} CONFLICTS ACROSS {len(conflicts)} TARGET MODELS")
    print()
    
    for target_model, field_list in conflicts.items():
        print(f"TARGET MODEL: {target_model}")
        print("-" * 60)
        
        # Group by related_name
        related_groups = defaultdict(list)
        for field in field_list:
            related_groups[field['related_name']].append(field)
        
        for related_name, fields in related_groups.items():
            print(f"  CONFLICT: related_name='{related_name}'")
            for field in fields:
                print(f"    File: {field['file']}")
                print(f"    Model: {field['model']}")
                print(f"    Field: {field['field']}")
                print(f"    Type: {field['type']}")
                print()
        print()

def main():
    """Main execution"""
    models_dir = Path(__file__).parent.parent / 'hrm' / 'models'
    
    if not models_dir.exists():
        print(f"ERROR: Models directory not found: {models_dir}")
        sys.exit(1)
    
    print("Scanning model files...")
    fields = scan_model_files(models_dir)
    
    print(f"Found {len(fields)} relationship fields")
    
    print("Detecting conflicts...")
    conflicts = detect_conflicts(fields)
    
    generate_report(conflicts)
    
    # Save detailed report to file
    report_file = Path(__file__).parent / 'conflicts_report.md'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# Related Name Conflicts Report\n\n")
        
        if not conflicts:
            f.write("✅ NO CONFLICTS FOUND\n")
        else:
            total_conflicts = sum(len(fields) for fields in conflicts.values())
            f.write(f"🚨 FOUND {total_conflicts} CONFLICTS\n\n")
            
            for target_model, field_list in conflicts.items():
                f.write(f"## Target Model: {target_model}\n\n")
                
                related_groups = defaultdict(list)
                for field in field_list:
                    related_groups[field['related_name']].append(field)
                
                for related_name, fields in related_groups.items():
                    f.write(f"### Conflict: `{related_name}`\n\n")
                    for field in fields:
                        f.write(f"- **File**: `{field['file']}`\n")
                        f.write(f"- **Model**: `{field['model']}`\n")
                        f.write(f"- **Field**: `{field['field']}`\n")
                        f.write(f"- **Type**: `{field['type']}`\n\n")
                    f.write("---\n\n")
    
    print(f"Detailed report saved to: {report_file}")
    
    # Exit with error code if conflicts found
    if conflicts:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
