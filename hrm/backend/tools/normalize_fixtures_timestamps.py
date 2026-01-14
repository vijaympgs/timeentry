#!/usr/bin/env python3
"""
Normalize fixtures by adding missing created_at and updated_at timestamps.
Script-first approach - no manual JSON edits required.
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime

class FixtureNormalizer:
    def __init__(self, fixtures_dir="D:\\platform\\hrm\\backend\\hrm\\fixtures"):
        self.fixtures_dir = Path(fixtures_dir)
        
    def normalize_fixture_file(self, fixture_file):
        """Normalize a single fixture file by adding missing timestamps."""
        try:
            with open(fixture_file, 'r', encoding='utf-8') as f:
                fixture_data = json.load(f)
            
            modified = False
            
            # Process each fixture entry
            for entry in fixture_data:
                if 'fields' in entry:
                    fields = entry['fields']
                    
                    # Add created_at if missing
                    if 'created_at' not in fields:
                        fields['created_at'] = "2024-01-01T00:00:00Z"
                        modified = True
                    
                    # Add updated_at if missing
                    if 'updated_at' not in fields:
                        fields['updated_at'] = "2024-01-01T00:00:00Z"
                        modified = True
            
            # Write back if modified
            if modified:
                with open(fixture_file, 'w', encoding='utf-8') as f:
                    json.dump(fixture_data, f, indent=2)
                print(f"Normalized: {fixture_file.name}")
                return True
            else:
                print(f"No changes needed: {fixture_file.name}")
                return False
                
        except Exception as e:
            print(f"Error processing {fixture_file.name}: {e}")
            return False
    
    def normalize_all_fixtures(self):
        """Normalize all JSON fixture files."""
        print("Normalizing fixtures for missing timestamps...")
        
        fixture_files = list(self.fixtures_dir.glob("*.json"))
        
        if not fixture_files:
            print("No JSON fixture files found.")
            return False
        
        modified_count = 0
        for fixture_file in fixture_files:
            if self.normalize_fixture_file(fixture_file):
                modified_count += 1
        
        print(f"\nSummary:")
        print(f"  Total fixture files: {len(fixture_files)}")
        print(f"  Files modified: {modified_count}")
        print(f"  Files unchanged: {len(fixture_files) - modified_count}")
        
        return modified_count > 0

def main():
    """Main function."""
    normalizer = FixtureNormalizer()
    
    # Change to correct directory
    script_dir = Path(__file__).parent
    backend_dir = script_dir.parent
    os.chdir(backend_dir)
    
    try:
        success = normalizer.normalize_all_fixtures()
        
        if success:
            print("\nFixture normalization complete!")
            print("Next step: Test loading one fixture")
        else:
            print("\nNo fixtures needed normalization.")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
