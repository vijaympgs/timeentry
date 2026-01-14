# Company Code Fix - '001' vs 'DEFAULT'

## Issue
- **Problem**: Blank org chart page, "no employees found"
- **Root Cause**: Company code mismatch
  - Employees in database: `company_code = '001'`
  - API filtering for: `company_code = 'DEFAULT'`

## Solution

### Files Fixed:
**`hrm/backend/hrm/views/employee.py`**

#### Change 1: get_queryset() method (Line 84)
```python
# Before:
company_code = getattr(user, 'company_code', 'DEFAULT')

# After:
company_code = getattr(user, 'company_code', '001')
```

#### Change 2: perform_create() method (Line 119)
```python
# Before:
company_code = getattr(user, 'company_code', 'DEFAULT')

# After:
company_code = getattr(user, 'company_code', '001')
```

## Verification

### Database Check:
```bash
cd hrm/backend
python manage.py shell -c "from hrm.models.employee import EmployeeRecord; total = EmployeeRecord.objects.count(); company_001 = EmployeeRecord.objects.filter(company_code='001').count(); print('Total employees:', total); print('Company 001:', company_001)"
```

**Result:**
- Total employees: 275
- Company 001: 275 ✅

### API Test:
```bash
curl http://localhost:8000/api/hrm/api/v1/employees/hierarchy/
```

**Expected Response:**
```json
{
  "hierarchy": [
    {
      "id": "...",
      "full_name": "William Simmons",
      "position_title": "Chief Executive Officer",
      "children": [...]
    }
  ],
  "total_employees": 275,
  "levels": 6
}
```

## Company Code Standard

### Current Setup:
- **Default Company Code**: `'001'` (defined in `hrm/backend/hrm/tenancy.py`)
- **All employees**: Created with `company_code = '001'`
- **API filtering**: Now uses `'001'` as default

### Why '001'?
- Standard enterprise company code format
- Matches tenancy configuration
- Allows for multi-company expansion (002, 003, etc.)

## Testing

### 1. Refresh Frontend
Navigate to: http://localhost:3002/employees/org-chart

**Expected Result:**
- ✅ Org chart loads with 275 employees
- ✅ Shows 6-level hierarchy
- ✅ CEO at top (William Simmons)
- ✅ 2 VPs below CEO
- ✅ 5 Directors below VPs
- ✅ Full pyramid structure visible

### 2. Test Filters
- **Level 1**: Shows 1 employee (CEO)
- **Level 1-2**: Shows 3 employees (CEO + 2 VPs)
- **Level 1-3**: Shows 8 employees (CEO + VPs + 5 Directors)
- **All Levels**: Shows all 275 employees

### 3. Test Search
- Search for "William" → Finds CEO
- Search for "Engineering" → Finds all Engineering employees
- Search for "Manager" → Finds all managers

## Related Files

### Tenancy Configuration:
**`hrm/backend/hrm/tenancy.py`**
```python
DEFAULT_COMPANY_CODE = "001"
```

### Employee Model:
**`hrm/backend/hrm/models/employee.py`** (Line 16)
```python
company_code = models.CharField(
    max_length=10, 
    db_index=True, 
    default=DEFAULT_COMPANY_CODE  # Uses '001'
)
```

### Management Command:
**`hrm/backend/hrm/management/commands/populate_org_hierarchy.py`**
- Creates all employees with `company_code='001'` (inherited from model default)

## Summary

✅ **Fixed**: Changed API default company code from 'DEFAULT' to '001'
✅ **Verified**: 275 employees exist with company_code='001'
✅ **Ready**: Org chart should now load all employees

**Action Required**: Refresh the frontend page to see the org chart!

---

**Status**: ✅ Complete
**Issue**: Resolved
**Next**: Test org chart in browser
