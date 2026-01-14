#!/usr/bin/env python3
"""
Simple runner script for the comprehensive related_name fix tool.
This provides an easy interface to run the fix with proper setup.
"""

import os
import sys
from pathlib import Path

def main():
    """Run the comprehensive related_name fix tool."""
    print("🚀 HRM Related Name Conflict Fix Tool")
    print("=" * 50)
    
    # Get the script directory
    script_dir = Path(__file__).parent
    backend_dir = script_dir.parent
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    # Import and run the fix tool
    try:
        from comprehensive_related_name_fix import RelatedNameFixer
        
        # Create fixer instance
        fixer = RelatedNameFixer()
        
        # First, analyze without applying changes
        print("📊 Step 1: Analyzing conflicts (dry run)...")
        result = fixer.fix_all_conflicts(apply_changes=False)
        
        if result['fixes_generated'] > 0:
            print(f"\n📋 Analysis Complete:")
            print(f"   - Conflicts found: {result['conflicts_found']}")
            print(f"   - Fixes needed: {result['fixes_generated']}")
            
            # Ask user if they want to apply fixes
            response = input("\n❓ Do you want to apply these fixes? (y/N): ").strip().lower()
            
            if response in ['y', 'yes']:
                print("\n🔧 Step 2: Applying fixes...")
                result = fixer.fix_all_conflicts(apply_changes=True)
                
                print("\n✅ Fix process completed!")
                print("\n🎯 Next steps:")
                print("   1. Run: python manage.py check")
                print("   2. If no errors: python manage.py makemigrations")
                print("   3. Test the application")
            else:
                print("\n💡 Fixes not applied. You can run this script again with 'y' to apply.")
        else:
            print("\n🎉 No conflicts found! All models are properly configured.")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running this from the backend directory.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
