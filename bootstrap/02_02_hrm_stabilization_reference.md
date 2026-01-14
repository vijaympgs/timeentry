# HRM Django Stabilization Reference

## Models
**Location:** `D:\platform\hrm\backend\hrm\models\`
- 80 models across 18 files with canonical related_name pattern applied
- Key models: Company, OrganizationalUnit, Position, Employee, RatingScale, Course
- All relationship fields follow: `<model_name_lower>_<field_name_lower>`

## Fixtures
**Location:** `D:\platform\hrm\backend\hrm\fixtures\`
- **00_master_companies.json** - Company master data (1 record)
- **01_master_organizational_units.json** - Organizational hierarchy (5 records)
- **02_master_positions.json** - Job positions (5 records)
- **03_master_salary_structures.json** - Compensation structures (1 record)
- **04_master_ratings.json** - Performance rating scales and levels (6 records)
- **05_master_courses.json** - Training courses (2 records)
- **00_master_seed_index.py** - Seed data loading script

## Tools
**Location:** `D:\platform\hrm\backend\tools\`
- **scan_relationship_fields.py** - AST scanner for relationship field detection
- **apply_canonical_related_names.py** - Automated canonical naming rewriter
- **validate_models_only.py** - Django system check validation
- **normalize_fixtures_timestamps.py** - Fixture timestamp normalization script

## Validate Fixtures
**Command:** `python D:\platform\hrm\backend\manage.py loaddata --app hrm <fixture_name>`
**Individual Loading:** Test each fixture separately before batch loading
**Validation:** `python D:\platform\hrm\backend\manage.py shell` - Check object counts

## Fixes Applied
1. **Model Conflicts:** Resolved 1,234 Django system check errors (fields.E304/E305)
2. **Migration Issues:** Fixed non-nullable field conflicts with null=True, blank=True
3. **Fixture Timestamps:** Added missing created_at/updated_at fields via automation
4. **JSON Format:** Fixed malformed JSON structure in ratings fixture
5. **Field Mismatches:** Aligned fixture fields with actual model definitions
6. **Foreign Keys:** Created missing Company fixture for dependency resolution

## Current Status
- Django System Checks: 0 errors
- Database: 20 master records loaded across 7 model types
- Platform: Ready for BBP task development
- Tools: Automated and reusable for future model changes
