#!/usr/bin/env python3
"""
Pure AST scanner to identify ALL relationship fields in HRM models.
No modifications, no regex, no heuristics - just pure AST parsing.
"""

import os
import ast
from pathlib import Path

class RelationshipFieldScanner:
    def __init__(self, models_dir="hrm/backend/hrm/models"):
        self.models_dir = Path(models_dir)
        
    def get_model_files(self):
        """Get all Python model files."""
        model_files = []
        for file_path in self.models_dir.glob("*.py"):
            if file_path.name != "__init__.py":
                model_files.append(file_path)
        return model_files
    
    def is_django_model(self, class_node):
        """Check if a class is a Django model."""
        for base in class_node.bases:
            if isinstance(base, ast.Attribute):
                if (isinstance(base.value, ast.Name) and 
                    base.value.id == 'models' and 
                    base.attr == 'Model'):
                    return True
        return False
    
    def extract_field_info(self, field_name, field_value):
        """Extract information about a Django relationship field."""
        if isinstance(field_value, ast.Call):
            if isinstance(field_value.func, ast.Attribute):
                if isinstance(field_value.func.value, ast.Name) and field_value.func.value.id == 'models':
                    field_type = field_value.func.attr
                    
                    # Check if it's a relationship field
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
    
    def scan_file(self, file_path):
        """Scan a single file for relationship fields."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            results = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    if self.is_django_model(node):
                        model_name = node.name
                        
                        for item in node.body:
                            if isinstance(item, ast.Assign):
                                for target in item.targets:
                                    if isinstance(target, ast.Name):
                                        field_info = self.extract_field_info(target.id, item.value)
                                        if field_info:
                                            results.append({
                                                'file': file_path.name,
                                                'model': model_name,
                                                'field': field_info['name'],
                                                'type': field_info['type'],
                                                'target': field_info['target_model'],
                                                'has_related_name': field_info['has_related_name'],
                                                'current_related_name': field_info['related_name'],
                                                'line': field_info['line_number']
                                            })
            
            return results
            
        except Exception as e:
            print(f"Error scanning {file_path}: {e}")
            return []
    
    def scan_all_files(self):
        """Scan all model files and return results."""
        all_results = []
        model_files = self.get_model_files()
        
        print(f"Scanning {len(model_files)} model files...")
        
        for file_path in model_files:
            print(f"  Scanning {file_path.name}...")
            results = self.scan_file(file_path)
            all_results.extend(results)
        
        return all_results
    
    def print_results(self, results):
        """Print results in a formatted table."""
        if not results:
            print("No relationship fields found.")
            return
        
        print(f"\nFound {len(results)} relationship fields:")
        print("=" * 120)
        print(f"{'File':<25} {'Model':<20} {'Field':<20} {'Type':<15} {'Target':<20} {'Has related_name':<15} {'Current related_name':<20}")
        print("=" * 120)
        
        for result in results:
            has_related = "Yes" if result['has_related_name'] else "No"
            current_name = result['current_related_name'] or "None"
            
            print(f"{result['file']:<25} {result['model']:<20} {result['field']:<20} {result['type']:<15} "
                  f"{result['target'] or 'Unknown':<20} {has_related:<15} {current_name:<20}")
        
        print("=" * 120)
        
        # Summary statistics
        total_fields = len(results)
        with_related_name = sum(1 for r in results if r['has_related_name'])
        without_related_name = total_fields - with_related_name
        
        print(f"\nSummary:")
        print(f"  Total relationship fields: {total_fields}")
        print(f"  With related_name: {with_related_name}")
        print(f"  Without related_name: {without_related_name}")
        print(f"  Fields needing related_name: {without_related_name}")

def main():
    """Main function."""
    scanner = RelationshipFieldScanner()
    results = scanner.scan_all_files()
    scanner.print_results(results)

if __name__ == "__main__":
    main()
