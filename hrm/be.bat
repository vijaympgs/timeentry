@echo off
echo .....................................................
echo.

echo [CLEANUP] Killing existing processes...
taskkill /f /im python.exe 2>nul
taskkill /f /im node.exe 2>nul
taskkill /f /im vite.exe 2>nul
echo Cleanup completed.
echo ..............................
echo    Starting Backend Server
echo ..............................
echo.

cd D:\platform\hrm\Backend
python manage.py makemigrations
python manage.py migrate

echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver  