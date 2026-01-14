# Organizational Hierarchy - Database Population

## ✅ Successfully Created 275 Employees!

### Hierarchy Structure

```
Level 1 (CEO):           1 employee
Level 2 (VPs):           2 employees
Level 3 (Directors):     5 employees
Level 4 (Managers):      8 employees
Level 5 (Senior Staff):  8 employees
Level 6 (Staff):       251 employees
─────────────────────────────────────
TOTAL:                 275 employees
```

### Organizational Chart

```
                    William Simmons
                         CEO
                          │
        ┌─────────────────┴─────────────────┐
        │                                   │
  Cynthia Griffin                      Joe Diaz
   VP Engineering                      VP Sales
        │                                   │
    ┌───┴───┐                          ┌────┴────┐
    │       │                          │         │
Frank    Ronald                    Deborah    + Others
Butler   Evans                     Porter
Director Director                  Director
    │       │                          │
    └───┬───┘                          │
        │                              │
    [8 Managers]                   [Managers]
        │                              │
    [8 Senior Staff]              [Senior Staff]
        │                              │
    [251 Full Staff distributed across all managers]
```

### Department Distribution

**Engineering** (Largest department)
- VP Engineering: Cynthia Griffin
- Directors: Frank Butler, Ronald Evans
- Managers: Christopher Long, Roger Guzman
- Senior Staff: Ronald Kim, Sarah Ramos
- Staff: ~80 employees

**Sales**
- VP Sales: Joe Diaz
- Director: Deborah Porter
- Managers: Michelle Brooks, Sarah Gonzalez
- Senior Staff: Ronald Aguilar
- Staff: ~60 employees

**Marketing**
- Director: Gary Medina (reports to CEO)
- Manager: Dennis Nelson
- Staff: ~30 employees

**Operations**
- Director: Jennifer Sanchez (reports to CEO)
- Manager: Lisa Porter
- Staff: ~30 employees

**Finance**
- Manager: Ruth Hill (reports to CEO)
- Staff: ~20 employees

**HR**
- Manager: Ethan Turner (reports to CEO)
- Staff: ~20 employees

**Other Departments**
- Distributed across remaining staff: ~35 employees

## Database Details

### Employee Fields Populated

Each employee has:
- ✅ **Unique employee number**: EMP00001 - EMP00275
- ✅ **Full name**: First + Last name (unique combinations)
- ✅ **Email**: firstname.lastname@company.com
- ✅ **Phone**: Random US phone number
- ✅ **Position title**: Based on level and department
- ✅ **Department**: Engineering, Sales, Marketing, etc.
- ✅ **Manager**: Proper reporting relationship
- ✅ **Hierarchy level**: 0 (CEO) to 5 (Staff)
- ✅ **Hire date**: Random date within last 10 years
- ✅ **Salary**: $50,000 - $250,000 based on level
- ✅ **Employment status**: All ACTIVE
- ✅ **Employment type**: All FULL_TIME

### Hierarchy Levels (0-indexed in DB)

```
hierarchy_level = 0  →  Level 1 (CEO)
hierarchy_level = 1  →  Level 2 (VPs)
hierarchy_level = 2  →  Level 3 (Directors)
hierarchy_level = 3  →  Level 4 (Managers)
hierarchy_level = 4  →  Level 5 (Senior Staff)
hierarchy_level = 5  →  Level 6 (Staff)
```

## How to Use

### View in Org Chart
1. Navigate to: http://localhost:3002/employees/org-chart
2. You'll see the full 275-employee hierarchy
3. Use filters:
   - **Level 1**: See just CEO
   - **Level 1-2**: See CEO + VPs
   - **Level 1-3**: See CEO + VPs + Directors
   - **Level 1-6**: See entire organization

### Test Filters
- **Department Filter**: Select "Engineering" to see ~80 employees
- **Level Filter**: Select "Level 1-3" to see top 8 employees
- **Search**: Type any name to find specific employees
- **Zoom**: Use zoom controls to navigate large hierarchy

### Re-run Command
To regenerate with different data:
```bash
cd hrm/backend
python manage.py populate_org_hierarchy
```

**Note**: This will DELETE all existing employees and create new ones!

## Management Command

**Location**: `hrm/backend/hrm/management/commands/populate_org_hierarchy.py`

**Usage**:
```bash
python manage.py populate_org_hierarchy
```

**What it does**:
1. Clears all existing employees
2. Creates CEO (Level 1)
3. Creates 2 VPs reporting to CEO (Level 2)
4. Creates 5 Directors reporting to VPs/CEO (Level 3)
5. Creates 8 Managers reporting to Directors (Level 4)
6. Creates 8 Senior Staff reporting to Managers (Level 5)
7. Creates 251 Staff reporting to Managers/Senior Staff (Level 6)

## Verification

### Check in Django Admin
```python
from hrm.models.employee import EmployeeRecord

# Count by level
for level in range(6):
    count = EmployeeRecord.objects.filter(hierarchy_level=level).count()
    print(f"Level {level+1}: {count} employees")

# View CEO
ceo = EmployeeRecord.objects.get(hierarchy_level=0)
print(f"CEO: {ceo.full_name}")

# View CEO's direct reports
vps = EmployeeRecord.objects.filter(manager=ceo)
print(f"VPs: {[vp.full_name for vp in vps]}")
```

### Check Reporting Relationships
```python
# Get all employees with no manager (should be 1 - CEO)
no_manager = EmployeeRecord.objects.filter(manager__isnull=True)
print(f"Employees with no manager: {no_manager.count()}")  # Should be 1

# Get all employees with managers (should be 274)
with_manager = EmployeeRecord.objects.filter(manager__isnull=False)
print(f"Employees with managers: {with_manager.count()}")  # Should be 274
```

## Sample Data

### Level 1 (CEO)
- William Simmons - Chief Executive Officer

### Level 2 (VPs)
- Cynthia Griffin - VP Engineering
- Joe Diaz - VP Sales

### Level 3 (Directors)
- Frank Butler - Director of Engineering
- Ronald Evans - Director of Engineering
- Deborah Porter - Director of Sales
- Gary Medina - Director of Marketing
- Jennifer Sanchez - Director of Operations

### Level 4 (Managers)
- Christopher Long - Engineering Manager
- Roger Guzman - Engineering Manager
- Michelle Brooks - Sales Manager
- Sarah Gonzalez - Sales Manager
- Dennis Nelson - Marketing Manager
- Lisa Porter - Operations Manager
- Ruth Hill - Finance Manager
- Ethan Turner - HR Manager

---

**Status**: ✅ Complete
**Total Employees**: 275
**Hierarchy Levels**: 6
**Ready for**: Org Chart visualization
