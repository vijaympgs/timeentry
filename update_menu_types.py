#!/usr/bin/env python3
"""
Script to update ERPMenuItem menu_type values based on bootstrap/06_03_tasks.md template classifications
Usage: python update_menu_types.py
"""
import sys
import os

# Add the backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'hrm', 'backend')
sys.path.insert(0, backend_path)

# Change to backend directory
os.chdir(backend_path)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

import django
django.setup()

from hrm.models.toolbar_config import ERPMenuItem

def update_menu_types():
    """Update ERPMenuItem menu_type values based on template classifications"""
    
    # Template classifications from bootstrap/06_03_tasks.md
    TEMPLATE_CLASSIFICATIONS = {
        # HRM Master Data
        'HRM_EMPLOYEE_MASTER': 'MST-C',      # Employee Master → T1 Complex Master Template
        'HRM_DEPARTMENT_MASTER': 'MST-S',    # Department → MST-S Simple Master Template
        'HRM_POSITION_MASTER': 'MST-S',      # Position → MST-S Simple Master Template
        'ORG_ORGANIZATIONAL_UNITS': 'MST-M', # Organizational Unit → MST-M Medium Master Template
        'ORG_COMPANIES': 'MST-M',            # Companies → MST-M Medium Master Template
        'ORG_DEPARTMENTS': 'MST-S',          # Departments → MST-S Simple Master Template
        'ORG_POSITIONS': 'MST-S',            # Positions → MST-S Simple Master Template
        
        # HRM Transactions
        'TIME_TIME_ENTRIES': 'TXN-S',        # Time Entries → TXN-S Simple Transaction Template
        'TIME_TIMESHEETS': 'TXN-S',          # Timesheets → TXN-S Simple Transaction Template
        'TIME_SHIFTS': 'MST-S',              # Shifts → MST-S Simple Master Template
        'TIME_ATTENDANCE_POLICIES': 'MST-S',  # Attendance Policies → MST-S Simple Master Template
        
        # HRM Performance
        'PERF_RATING_SCALES': 'MST-M',       # Rating Scales → MST-M Medium Master Template
        'PERF_REVIEW_CYCLES': 'MST-M',       # Review Cycles → MST-M Medium Master Template
        'PERF_CALIBRATION_SESSIONS': 'MST-M', # Calibration Sessions → MST-M Medium Master Template
        
        # HRM Learning
        'LEARN_COURSES': 'MST-M',            # Courses → MST-M Medium Master Template
        'LEARN_INSTRUCTORS': 'MST-M',        # Instructors → MST-M Medium Master Template
        'LEARN_LEARNING_PATHS': 'MST-M',     # Learning Paths → MST-M Medium Master Template
        'LEARN_TRAINING_SESSIONS': 'TXN-M',  # Training Sessions → TXN-M Medium Transaction Template
        'HRM_COURSE_CATALOG': 'MST-M',        # Course Catalog → MST-M Medium Master Template
        
        # HRM Compensation
        'COMP_SALARY_STRUCTURES': 'MST-M',    # Salary Structures → MST-M Medium Master Template
        'HRM_SALARY_STRUCTURES': 'MST-M',    # Salary Structures → MST-M Medium Master Template
        'COMP_PAY_GRADES': 'MST-M',          # Pay Grades → MST-M Medium Master Template
        'COMP_PAYROLL_RUNS': 'TXN-M',        # Payroll Runs → TXN-M Medium Transaction Template
        
        # HRM Recruitment
        'RECR_JOB_APPLICATIONS': 'TXN-M',     # Job Applications → TXN-M Medium Transaction Template
        'RECR_JOB_POSTINGS': 'MST-M',        # Job Postings → MST-M Medium Master Template
        'RECR_SCREENING_PROCESSES': 'TXN-M', # Screening Processes → TXN-M Medium Transaction Template
        'HRM_OFFER_LETTER': 'MST-M',         # Offer Letter Templates → MST-M Medium Master Template
        'HRM_CONTRACT_TEMPLATE': 'MST-M',     # Contract Templates → MST-M Medium Master Template
        
        # HRM Employee Data
        'HRM_EMPLOYEE_ADDRESSES': 'MST-M',   # Employee Addresses → MST-M Medium Master Template
        'HRM_EMPLOYEE_PROFILES': 'MST-M',    # Employee Profiles → MST-M Medium Master Template
        'HRM_EMPLOYEE_DOCUMENTS': 'MST-M',   # Employee Documents → MST-M Medium Master Template
        'HRM_EMPLOYEE_SKILLS': 'MST-M',      # Employee Skills → MST-M Medium Master Template
        'HRM_EMPLOYEE_DIRECTORY': 'MST-M',    # Employee Directory → MST-M Medium Master Template
        'HRM_SKILL_CATEGORIES': 'MST-S',      # Skill Categories → MST-S Simple Master Template
        'HRM_ORGANIZATIONAL_CHART': 'MST-C', # Organizational Chart → T1 Complex Master Template
        'HRM_RECOGNITION_BADGES': 'MST-M',    # Recognition Badges → MST-M Medium Master Template
        'BADGE_BADGES': 'MST-M',              # Badges → MST-M Medium Master Template
        'BADGE_AWARDS': 'TXN-M',              # Badge Awards → TXN-M Medium Transaction Template
        'BADGE_NOMINATIONS': 'TXN-M',         # Badge Nominations → TXN-M Medium Transaction Template
        
        # CRM Master Data
        'CRM_CUSTOMERS': 'MST-C',             # Account → MST-C Complex Master Template - has hierarchy
        'CRM_CONTACTS': 'MST-M',              # Contact → MST-M Medium Master Template
        'CRM_LEADS': 'TXN-M',                 # Lead → TXN-M Medium Transaction Template
        'CRM_OPPORTUNITIES': 'TXN-C',         # Opportunity → TXN-C Complex Transaction Template - has stages
        'CRM_CAMPAIGNS': 'TXN-M',             # Campaign → TXN-M Medium Transaction Template
        
        # FMS Master Data
        'FMS_INVOICES': 'TXN-M',              # Invoices → TXN-M Medium Transaction Template
        'FMS_PAYMENTS': 'TXN-M',              # Payments → TXN-M Medium Transaction Template
        'FMS_EXPENSE_REPORTS': 'TXN-M',       # Expense Reports → TXN-M Medium Transaction Template
        'FMS_FINANCIAL_STATEMENTS': 'R',      # Financial Statements → R Report
        'FMS_BUDGETS': 'MST-M',               # Budgets → MST-M Medium Master Template
        'FMS_ACCOUNT_CHARTS': 'MST-M',        # Account Charts → MST-M Medium Master Template
        
        # Tax & Compliance
        'TAX_CALCULATIONS': 'TXN-M',          # Tax Calculations → TXN-M Medium Transaction Template
        'TAX_WITHHOLDINGS': 'TXN-M',          # Tax Withholdings → TXN-M Medium Transaction Template
        'TAX_JURISDICTIONS': 'MST-M',         # Tax Jurisdictions → MST-M Medium Master Template
    }
    
    # Define toolbar configurations by template type
    TOOLBAR_CONFIGS = {
        'MST-S': 'NESCKVDXRQF',              # Simple Master - Basic operations
        'MST-M': 'NESCKVDXRQFIO',             # Medium Master - Advanced operations
        'MST-C': 'NESCKVDXRQFIO',             # Complex Master - Full operations
        'TXN-S': 'NESCKZTJAVPMRDX1234QF',    # Simple Transaction
        'TXN-M': 'NESCKZTJAVPMRDX1234QF',    # Medium Transaction
        'TXN-C': 'NESCKZTJAVPMRDX1234QF',    # Complex Transaction
        'D': 'VRXPYQFG',                      # Dashboard
        'R': 'VRXPYQFG',                      # Report
        'C': 'NRQFX',                         # Configuration
        'S': 'NRQFX',                         # Setup
        'U': 'NRQFX',                         # Utility
        'Q': 'NRQFX',                         # Query
        'W': 'NESCKZTJAVPMRDX1234QF',        # Workflow
        'A': 'VRXPYQFG',                      # Analytics
    }
    
    print("🔧 Updating ERPMenuItem menu_type and toolbar_config values...")
    print("=" * 80)
    
    updated_count = 0
    total_count = ERPMenuItem.objects.count()
    
    for item in ERPMenuItem.objects.all():
        old_menu_type = item.menu_type
        old_toolbar_config = item.toolbar_config
        
        # Get new menu type from template classifications
        new_menu_type = TEMPLATE_CLASSIFICATIONS.get(item.menu_id, old_menu_type)
        
        # Get new toolbar config based on new menu type
        new_toolbar_config = TOOLBAR_CONFIGS.get(new_menu_type, old_toolbar_config)
        
        # Update if anything changed
        if old_menu_type != new_menu_type or old_toolbar_config != new_toolbar_config:
            item.menu_type = new_menu_type
            item.toolbar_config = new_toolbar_config
            item.save()
            
            print(f"✅ Updated: {item.menu_id} ({item.menu_name})")
            if old_menu_type != new_menu_type:
                print(f"   Menu Type: {old_menu_type} → {new_menu_type}")
            if old_toolbar_config != new_toolbar_config:
                print(f"   Toolbar Config: {old_toolbar_config} → {new_toolbar_config}")
            print()
            updated_count += 1
        else:
            print(f"⏭️  Skipped: {item.menu_id} ({item.menu_name}) - Already correct")
    
    print("=" * 80)
    print(f"📊 Summary:")
    print(f"   Total items: {total_count}")
    print(f"   Updated: {updated_count}")
    print(f"   Skipped: {total_count - updated_count}")
    print()
    print("🎉 Menu type and toolbar configuration update completed!")

def list_current_classifications():
    """List current ERPMenuItem classifications"""
    print("📋 Current ERPMenuItem classifications:")
    print("=" * 90)
    
    for item in ERPMenuItem.objects.all().order_by('module', 'menu_name'):
        print(f"{item.menu_id:25} | {item.menu_name:30} | {item.menu_type:6} | {item.toolbar_config}")
    
    print("=" * 90)
    print(f"Total: {ERPMenuItem.objects.count()} items")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--list':
        list_current_classifications()
    else:
        update_menu_types()
