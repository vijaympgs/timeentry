#!/usr/bin/env python3
"""
HRM Fixture Validation Script

Validates all HRM fixtures against Django model registry.
Windows-safe, bootstraps Django correctly.

Usage:
    cd D:\platform\hrm\backend
    python hrm\fixtures\validate_fixtures.py
"""

import os
import sys
import json
from pathlib import Path

# Add Django project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Bootstrap Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

import django
django.setup()

from django.apps import apps


def load_fixture_data(fixture_path):
    """Load and parse JSON fixture data."""
    try:
        with open(fixture_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"X Error loading {fixture_path}: {e}")
        return None


def validate_fixture_model(model_identifier):
    """Validate that a model identifier exists in Django registry."""
    try:
        app_label, model_name = model_identifier.split('.')
        model_class = apps.get_model(app_label, model_name)
        return model_class is not None
    except Exception:
        return False


def main():
    """Main validation function."""
    print("HRM Fixture Validation")
    print("=" * 50)
    
    fixtures_dir = Path(__file__).parent
    fixture_files = [
        "01_master_organizational_units.json",
        "02_master_positions.json", 
        "03_master_salary_structures.json",
        "04_master_ratings.json",
        "05_master_courses.json",
        "06_master_recognition_badges.json",
        "07_master_offer_templates.json",
        "08_master_contract_templates.json",
        "11_transaction_applications.json"
    ]
    
    all_valid = True
    invalid_models = set()
    
    for fixture_file in fixture_files:
        fixture_path = fixtures_dir / fixture_file
        
        if not fixture_path.exists():
            print(f"WARNING {fixture_file}: FILE NOT FOUND")
            all_valid = False
            continue
            
        print(f"\nValidating {fixture_file}...")
        
        data = load_fixture_data(fixture_path)
        if data is None:
            all_valid = False
            continue
            
        # Handle both single object and array formats
        if isinstance(data, dict):
            data = [data]
        elif not isinstance(data, list):
            print(f"X {fixture_file}: Invalid JSON structure")
            all_valid = False
            continue
            
        fixture_models = set()
        for item in data:
            if 'model' not in item:
                print(f"X {fixture_file}: Missing 'model' field")
                all_valid = False
                break
                
            fixture_models.add(item['model'])
        
        # Validate each model identifier
        file_valid = True
        for model_id in fixture_models:
            if not validate_fixture_model(model_id):
                print(f"  X Invalid model: {model_id}")
                invalid_models.add(model_id)
                file_valid = False
                all_valid = False
            else:
                print(f"  + Valid model: {model_id}")
        
        if file_valid:
            print(f"+ {fixture_file}: VALID")
        else:
            print(f"X {fixture_file}: INVALID")
    
    print("\n" + "=" * 50)
    print("VALIDATION SUMMARY")
    print("=" * 50)
    
    if all_valid:
        print("+ ALL FIXTURES VALID")
        return 0
    else:
        print("X FIXTURES INVALID")
        if invalid_models:
            print("\nInvalid Model Identifiers:")
            for model_id in sorted(invalid_models):
                print(f"  - {model_id}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
