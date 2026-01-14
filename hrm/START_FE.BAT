@echo off
echo ..............................
echo    Starting Frontend Server
echo ..............................
echo.

cd C:\platform\hrm\frontend

echo Starting frontend server on port 3001..
echo.
echo ...................................................
echo   Frontend running at: http://localhost:3001
echo   Backend at: http://localhost:8000
echo ...................................................
echo.
echo Press Ctrl+C to stop the server
echo.

npm run dev