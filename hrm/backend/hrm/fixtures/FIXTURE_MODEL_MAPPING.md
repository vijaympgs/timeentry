# HRM Fixture → Model Mapping Table

## Complete Fixture Analysis

| Fixture File | Current "model" value(s) | Actual Django Model Class | Correct Canonical "model" value | Source File | Status |
|-------------|------------------------|--------------------------|--------------------------------|-------------|---------|
| 01_master_organizational_units.json | hrm.organizationalunit | OrganizationalUnit | hrm.organizationalunit | hrm/models/organizational_unit.py | VALID |
| 02_master_positions.json | hrm.position | Position | hrm.position | hrm/models/organizational_unit.py | VALID |
| 03_master_salary_structures.json | hrm.salarystructure, hrm.paygrade, hrm.compensationrange | SalaryStructure, PayGrade, CompensationRange | hrm.salarystructure, hrm.paygrade, hrm.compensationrange | hrm/models/salary_structures.py | VALID |
| 04_master_ratings.json | hrm.ratingscale | RatingScale | hrm.ratingscale | hrm/models/ratings.py | VALID |
| 05_master_courses.json | hrm.course | Course | hrm.course | hrm/models/course_catalog.py | VALID |
| 06_master_recognition_badges.json | hrm.badge | Badge | hrm.badge | hrm/models/recognition_badges.py | VALID |
| 07_master_offer_templates.json | hrm.offerlettertemplate | OfferLetterTemplate | hrm.offerlettertemplate | hrm/models/offer_letter.py | VALID |
| 08_master_contract_templates.json | hrm.contracttemplate | ContractTemplate | hrm.contracttemplate | hrm/models/contract_template.py | VALID |
| 11_transaction_applications.json | hrm.jobapplication | ApplicationCapture | hrm.applicationcapture | hrm/models/application_capture.py | **FIXED** |

## Model Verification

All models are verified to exist in `hrm/models/__init__.py`:

- ✅ OrganizationalUnit
- ✅ Position  
- ✅ SalaryStructure, PayGrade, CompensationRange
- ✅ RatingScale
- ✅ Course
- ✅ Badge
- ✅ OfferLetterTemplate
- ✅ ContractTemplate
- ✅ ApplicationCapture

## Canonical HRM Naming Standard

All fixtures follow the canonical format: `hrm.<ExactModelClassLowercase>`

## Required Fixes

### 11_transaction_applications.json
- **Current**: `hrm.jobapplication`
- **Correct**: `hrm.applicationcapture`
- **Reason**: Model class is `ApplicationCapture`, not `JobApplication`

## Validation Status

- **Total Fixtures**: 9
- **Valid**: 8
- **Need Fix**: 1
- **Overall Status**: ⚠️ REQUIRES NORMALIZATION
