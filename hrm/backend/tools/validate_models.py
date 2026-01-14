#!/usr/bin/env python3
"""SCRIPT 3 — POST-FIX VALIDATION GATE
Run Django setup and execute comprehensive model validation"""

import os
import sys
import django
from pathlib import Path
from django.conf import settings
from django.core.management import execute_from_command_line
from django.core.checks import run_checks
from django.apps import apps


def setup_django():
    """Setup Django environment"""
    # Add the backend directory to Python path
    backend_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(backend_dir))
    
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    
    # Configure Django
    django.setup()
    
    # Populate apps registry
    apps.populate(installed_apps=getattr(settings, 'INSTALLED_APPS', []))


def run_model_validation():
    """Run comprehensive Django model validation"""
    print("=" * 80)
    print("DJANGO MODEL VALIDATION")
    print("=" * 80)
    
    try:
        # Run Django system checks
        print("Running Django system checks...")
        errors = run_checks(include_deployment_checks=False)
        
        if errors:
            print("VALIDATION FAILED - ERRORS FOUND:")
            print()
            
            for error in errors:
                print(f"[ERROR] {error.id}: {error.msg}")
                if error.hint:
                    print(f"   [HINT] {error.hint}")
                if error.obj:
                    print(f"   [OBJECT] {error.obj}")
                print()
            
            return False
        else:
            print("[OK] SYSTEM CHECKS PASSED")
        
        # Try to import all models to catch import errors
        print("\nValidating model imports...")
        
        from django.apps import apps
        app_config = apps.get_app_config('hrm')
        
        model_count = 0
        for model in app_config.get_models():
            try:
                # Try to access the model class
                model_class = model.get_model_class()
                model_count += 1
                print(f"  [OK] {model_class.__name__}")
            except Exception as e:
                print(f"  [FAIL] {model.name}: {e}")
                return False
        
        print(f"\n[OK] ALL {model_count} MODELS IMPORTED SUCCESSFULLY")
        
        # Run makemigrations in dry-run mode to check for migration issues
        print("\nChecking migration status...")
        
        try:
            from django.core.management import call_command
            call_command('makemigrations', '--dry-run', '--check', verbosity=0)
            print("[OK] MIGRATIONS UP TO DATE")
        except SystemExit as e:
            if e.code != 0:
                print("[FAIL] MIGRATION ISSUES DETECTED")
                print("   Run 'python manage.py makemigrations' to create missing migrations")
                return False
        except Exception as e:
            print(f"[ERROR] VALIDATION ERROR: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        return True
    
    except Exception as e:
        print(f"[ERROR] VALIDATION ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main execution"""
    print("Setting up Django environment...")
    
    try:
        setup_django()
        print("Django environment configured")
    except Exception as e:
        print(f"DJANGO SETUP FAILED: {e}")
        sys.exit(1)
    
    print("\nStarting model validation...")
    
    if run_model_validation():
        print("\n" + "=" * 80)
        print("[SUCCESS] VALIDATION SUCCESSFUL")
        print("[OK] All Django models are stable and ready for migrations")
        print("=" * 80)
        sys.exit(0)
    else:
        print("\n" + "=" * 80)
        print("[FAIL] VALIDATION FAILED")
        print("[ACTION] Fix the reported errors before proceeding")
        print("=" * 80)
        sys.exit(1)


if __name__ == "__main__":
    main()
