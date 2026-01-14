# Toolbar Registry Setup Instructions

## Overview
The HRM platform uses a backend-driven toolbar system where each page/view has a registry entry in the `ERPMenuItem` model. This controls what toolbar actions are available on each page.

## Current Status
- ✅ Migrations are applied (0006, 0007, 0008)
- ✅ Models are ready: `ERPMenuItem`, `ERPToolbarControl`, `Role`, `RolePermission`, `UserRole`
- ❌ Menu items need to be seeded
- ❌ Toolbar configurations need to be set

## Step-by-Step Setup

### Step 1: Seed Essential Menu Items
Run the seed command to create the basic menu items:

```bash
cd C:\platform\hrm\backend
python manage.py seed_menu_items
```

This will create 10 essential menu items including:
- HRM_EMPLOYEE_MASTER (Employee Records)
- HRM_ORG_CHART (Organization Chart)
- HRM_PROFILE_VIEW (Employee Profile)
- HRM_DASHBOARD (HR Dashboard)
- And more...

### Step 2: Verify Menu Items
Check that menu items were created:

```bash
python manage.py shell -c "from hrm.models.toolbar_config import ERPMenuItem; print(f'Total Menu Items: {ERPMenuItem.objects.count()}'); [print(f'{item.menu_id}: {item.toolbar_config}') for item in ERPMenuItem.objects.all()]"
```

### Step 3: (Optional) Update Menu Types
If you need to update menu types for existing items:

```bash
cd C:\platform
python update_menu_types.py
```

### Step 4: (Optional) Update Toolbar Configs
If you need to update toolbar configurations:

```bash
cd C:\platform
python update_toolbar_configs.py
```

## Toolbar Action Codes Reference

### Standard Actions
- **N**: New (Plus) - Create new record
- **E**: Edit (Edit) - Edit existing record
- **S**: Save (Save) - Save changes
- **C**: Cancel (X) - Cancel operation
- **K**: Clear (Rotate) - Clear form
- **V**: View (Eye) - View mode
- **D**: Delete (Trash) - Delete record
- **X**: Exit (LogOut) - Exit/Close
- **R**: Refresh (Refresh) - Reload data
- **Q**: Search (Search) - Search functionality
- **F**: Filter (Filter) - Filter data

### Import/Export
- **I**: Import (Upload) - Import data
- **O**: Export (Download) - Export data

### Utilities
- **L**: Clone (Copy) - Duplicate record
- **B**: Notes (Note) - Add notes
- **U**: Attach (Paperclip) - Attachments
- **G**: Settings (Gear) - Settings
- **P**: Print (Printer) - Print
- **M**: Email (Mail) - Email

### Workflow Actions
- **T**: Submit (Send) - Submit for approval
- **J**: Reject (Ban) - Reject
- **H**: Hold (Pause) - Put on hold
- **Z**: Void (Octagon) - Void transaction
- **A**: Authorize (Check) - Approve
- **W**: Amend (FileEdit) - Amend

## Template-Based Toolbar Configs

### Master Data Templates
- **MST-S** (Simple Master): `NESCKVDXRQF`
- **MST-M** (Medium Master): `NESCKVDXRQF`
- **MST-C** (Complex Master): `NESCKVDXRQFIOBUG`

### Transaction Templates
- **TXN-S** (Simple Transaction): `NESCKVDXRQF`
- **TXN-M** (Medium Transaction): `NESCKVDXRQFTJHZA`
- **TXN-C** (Complex Transaction): `NESCKVDXRQFTJHZA`

### Other Types
- **Dashboard**: `VRQFX` (View, Refresh, Search, Filter, Exit)
- **Report**: `VRQFXPO` (+ Print, Export)

## Current Menu Items Configuration

After running `seed_menu_items`, you'll have:

| Menu ID | Menu Name | Type | Toolbar Config |
|---------|-----------|------|----------------|
| HRM_EMPLOYEE_MASTER | Employee Records | MST-C | NESCKVDXRQFIOBUG |
| HRM_ORG_CHART | Organization Chart | D | VRQFX |
| HRM_PROFILE_VIEW | Employee Profile | D | VEXR |
| HRM_DASHBOARD | HR Dashboard | D | VRQ |
| HRM_DEPARTMENT_MASTER | Department Master | MST-S | NESCKVDXRQF |
| HRM_POSITION_MASTER | Position Master | MST-M | NESCKVDXRQF |
| HRM_LEAVE_APPLICATION | Leave Application | TXN-M | NESCKVDXRQFTJHZA |
| HRM_ATTENDANCE | Attendance | TXN-S | NESCKVDXRQF |
| HRM_PAYROLL | Payroll Processing | TXN-C | NESCKVDXRQFTJHZA |
| HRM_RECRUITMENT | Recruitment | TXN-C | NESCKVDXRQFTJHZA |

## Admin Interface

Access the toolbar configuration admin at:
```
http://localhost:8000/admin/hrm/erpmenuitem/
```

Login with:
- Username: `admin`
- Password: `admin`

## Frontend Integration

The frontend fetches toolbar configuration from:
```
GET /api/hrm/api/toolbar-config/{view_id}/
GET /api/hrm/api/toolbar-permissions/?view_id={view_id}&mode={mode}
```

Example for Employee Records page:
```javascript
// Frontend uses viewId: 'HRM_EMPLOYEE_MASTER'
const config = await fetch('/api/hrm/api/toolbar-config/HRM_EMPLOYEE_MASTER/');
```

## Troubleshooting

### No menu items showing
Run: `python manage.py seed_menu_items`

### Toolbar not showing correct actions
1. Check menu item exists: `python manage.py shell -c "from hrm.models.toolbar_config import ERPMenuItem; print(ERPMenuItem.objects.filter(menu_id='HRM_EMPLOYEE_MASTER').first())"`
2. Verify toolbar_config field has correct value
3. Check frontend is using correct viewId

### Need to add new menu item
Either:
1. Add to `seed_menu_items.py` and re-run
2. Add via Django admin at `/admin/hrm/erpmenuitem/`
3. Create via Django shell

## References

- Bootstrap Guide: `bootstrap/04_02_toolbar_implementation_guide_v2.md`
- Code Examples: `bootstrap/04_03_toolbar_code_examples_v2.md`
- Mode-Based Filtering: `bootstrap/04_03_toolbar_mode_based_filtering_v2.md`
