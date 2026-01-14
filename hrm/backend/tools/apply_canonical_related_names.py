#!/usr/bin/env python3
"""
Deterministic AST rewriter to apply canonical related_name to ALL relationship fields.
Canonical rule: <model_name_lower>_<field_name_lower>
AST only, no regex, idempotent, safe to re-run.
"""

import os
import ast
from pathlib import Path
import copy

class CanonicalRelatedNameApplier:
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
    
    def generate_canonical_related_name(self, model_name, field_name):
        """Generate canonical related_name: <model_name_lower>_<field_name_lower>"""
        return f"{model_name.lower()}_{field_name.lower()}"
    
    def process_field_call(self, call_node, model_name, field_name):
        """Process a field call node and ensure canonical related_name."""
        if not isinstance(call_node.func, ast.Attribute):
            return call_node
        
        if not isinstance(call_node.func.value, ast.Name) or call_node.func.value.id != 'models':
            return call_node
        
        field_type = call_node.func.attr
        if field_type not in ['ForeignKey', 'OneToOneField', 'ManyToManyField']:
            return call_node
        
        # Create a new call node with canonical related_name
        new_call = copy.deepcopy(call_node)
        
        # Remove existing related_name if present
        new_keywords = []
        has_related_name = False
        
        for keyword in new_call.keywords:
            if keyword.arg != 'related_name':
                new_keywords.append(keyword)
            else:
                has_related_name = True
        
        # Add canonical related_name
        canonical_name = self.generate_canonical_related_name(model_name, field_name)
        related_name_keyword = ast.keyword(
            arg='related_name',
            value=ast.Constant(value=canonical_name)
        )
        new_keywords.append(related_name_keyword)
        new_call.keywords = new_keywords
        
        return new_call
    
    def process_assign_node(self, assign_node, model_name):
        """Process an assign node to fix relationship fields."""
        if not isinstance(assign_node.value, ast.Call):
            return assign_node
        
        # Check if this is a relationship field assignment
        if isinstance(assign_node.value.func, ast.Attribute):
            if (isinstance(assign_node.value.func.value, ast.Name) and 
                assign_node.value.func.value.id == 'models'):
                
                field_type = assign_node.value.func.attr
                if field_type in ['ForeignKey', 'OneToOneField', 'ManyToManyField']:
                    # Get field name from target
                    field_name = None
                    for target in assign_node.targets:
                        if isinstance(target, ast.Name):
                            field_name = target.id
                            break
                    
                    if field_name:
                        new_call = self.process_field_call(assign_node.value, model_name, field_name)
                        if new_call != assign_node.value:
                            new_assign = copy.deepcopy(assign_node)
                            new_assign.value = new_call
                            return new_assign
        
        return assign_node
    
    def process_class_node(self, class_node):
        """Process a class node to fix all relationship fields."""
        if not self.is_django_model(class_node):
            return class_node
        
        model_name = class_node.name
        new_body = []
        
        for item in class_node.body:
            if isinstance(item, ast.Assign):
                new_item = self.process_assign_node(item, model_name)
                new_body.append(new_item)
            else:
                new_body.append(item)
        
        new_class = copy.deepcopy(class_node)
        new_class.body = new_body
        return new_class
    
    def process_file(self, file_path):
        """Process a single file and apply canonical related names."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            new_body = []
            changes_made = False
            
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    new_class = self.process_class_node(node)
                    new_body.append(new_class)
                    if new_class != node:
                        changes_made = True
                else:
                    new_body.append(node)
            
            if changes_made:
                new_tree = ast.Module(body=new_body, type_ignores=tree.type_ignores)
                
                # Write back to file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(ast.unparse(new_tree))
                
                return True
            else:
                return False
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return False
    
    def apply_to_all_files(self):
        """Apply canonical related names to all model files."""
        model_files = self.get_model_files()
        
        print(f"Processing {len(model_files)} model files...")
        
        files_changed = 0
        for file_path in model_files:
            print(f"  Processing {file_path.name}...")
            if self.process_file(file_path):
                files_changed += 1
                print(f"    [+] Modified")
            else:
                print(f"    [-] No changes needed")
        
        print(f"\nSummary:")
        print(f"  Files processed: {len(model_files)}")
        print(f"  Files modified: {files_changed}")
        
        return files_changed > 0

def main():
    """Main function."""
    applier = CanonicalRelatedNameApplier()
    
    print("Applying canonical related_name to all relationship fields...")
    print("Canonical rule: <model_name_lower>_<field_name_lower>")
    print()
    
    changes_made = applier.apply_to_all_files()
    
    if changes_made:
        print("\n[+] Canonical related names applied successfully!")
        print("Next step: Run python tools\\validate_models_only.py")
    else:
        print("\n[-] All relationship fields already have canonical related names")

if __name__ == "__main__":
    main()
