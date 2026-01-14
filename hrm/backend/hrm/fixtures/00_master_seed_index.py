"""
HRM Master Seed Data Index
Following BBP specifications with proper execution order
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# ROOT CAUSE ANALYSIS:
# Django is looking for 'hrm' module but the settings.py is in hrm.backend
# The INSTALLED_APPS includes 'hrm' which refers to the hrm package
# We need to ensure the hrm package (containing models) is in Python path

# Get current directory (should be D:\platform\hrm\backend\hrm\fixtures)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up 3 levels to reach hrm directory: fixtures -> hrm -> backend -> hrm
hrm_path = os.path.dirname(os.path.dirname(current_dir))

# Add hrm directory to Python path (contains models package)
if hrm_path not in sys.path:
    sys.path.insert(0, hrm_path)

# Add hrm.backend to Python path (contains settings.py)
hrm_backend_path = os.path.dirname(hrm_path)
if hrm_backend_path not in sys.path:
    sys.path.insert(0, hrm_backend_path)

# Set up Django - use correct project settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

def load_seed_data():
    """
    Load seed data in proper dependency order
    Masters (01-10) → Transactions (11-20) → Workflows (21-30)
    """
    
    print("Starting HRM Seed Data Loading...")
    
    # Master Data (01-10) - No dependencies - Phase 1 Only
    master_files = [
        '00_master_companies.json',
        '01_master_organizational_units.json',
        '02_master_positions.json', 
        '03_master_salary_structures.json',
        '04_master_ratings.json',
        '05_master_courses.json',
        '06_master_recognition_badges.json',
        '07_master_offer_templates.json',
        '08_master_contract_templates.json',
        '11_transaction_applications.json',
    ]
    
    # Load data in order - Phase 1 only
    all_files = master_files
    
    for fixture_file in all_files:
        try:
            print(f"Loading {fixture_file}...")
            execute_from_command_line(['manage.py', 'loaddata', '--traceback', '--app', 'hrm', fixture_file.replace('.json', '')])
            print(f"Successfully loaded {fixture_file}")
        except Exception as e:
            print(f"Error loading {fixture_file}: {str(e)}")
            continue
    
    print("HRM Seed Data Loading Complete!")

if __name__ == '__main__':
    load_seed_data()
