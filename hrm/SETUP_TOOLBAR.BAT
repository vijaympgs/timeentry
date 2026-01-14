@echo off
echo ============================================
echo   HRM Toolbar Registry Setup
echo ============================================
echo.

cd C:\platform\hrm\backend

echo [1/3] Seeding essential menu items...
python manage.py seed_menu_items

echo.
echo [2/3] Verifying menu items...
python manage.py shell -c "from hrm.models.toolbar_config import ERPMenuItem; print(f'\nTotal Menu Items: {ERPMenuItem.objects.count()}\n'); print('Menu Items:'); print('=' * 80); [print(f'{item.menu_id:30} | {item.menu_name:30} | {item.toolbar_config}') for item in ERPMenuItem.objects.all().order_by('menu_id')]"

echo.
echo [3/3] Setup complete!
echo.
echo ============================================
echo   Access Admin Panel:
echo   http://localhost:8000/admin/hrm/erpmenuitem/
echo ============================================
echo.

pause
