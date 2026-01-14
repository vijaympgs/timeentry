#!/usr/bin/env python3
"""
Hard validation gate - Bootstrap Django and run system checks.
FAILS HARD on ANY error. No soft failures, no warnings.
"""

import os
import sys
from pathlib import Path

def validate_models():
    """Run Django system checks using manage.py."""
    print("Starting Django model validation...")
    print("=" * 50)
    
    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    try:
        print("Running Django system checks...")
        
        # Run manage.py check and capture output
        import subprocess
        
        result = subprocess.run(
            ['python', 'd:\\platform\\hrm\\backend\\manage.py', 'check'],
            capture_output=True,
            text=True
        )
        
        # Get output
        stdout_output = result.stdout
        stderr_output = result.stderr
        
        # Combine output
        full_output = stdout_output + stderr_output
        
        # Check for actual errors (return code != 0 OR error messages in output)
        has_errors = result.returncode != 0 or "ERROR:" in full_output or "SystemCheckError" in full_output
        
        if has_errors:
            print("VALIDATION FAILED:")
            print("=" * 50)
            print(full_output)
            print("=" * 50)
            print("[X] BLOCKING ERRORS FOUND")
            print("Fix the above errors and re-run validation.")
            return False
        else:
            print("[+] VALIDATION PASSED")
            print("[+] Zero Django system check errors")
            print("[+] Models are ready for migrations")
            if full_output.strip():
                print(f"Output: {full_output.strip()}")
            return True
            
    except Exception as e:
        print(f"[X] VALIDATION ERROR: {e}")
        print("=" * 50)
        import traceback
        traceback.print_exc()
        print("=" * 50)
        print("CRITICAL: Cannot validate models")
        return False

def main():
    """Main function."""
    success = validate_models()
    
    if success:
        print("\n[+] SUCCESS: All models validated!")
        print("Ready for next phase: migrations and seed data")
        sys.exit(0)
    else:
        print("\n[X] FAILURE: Validation blocked")
        print("DO NOT proceed to migrations")
        sys.exit(1)

if __name__ == "__main__":
    main()
