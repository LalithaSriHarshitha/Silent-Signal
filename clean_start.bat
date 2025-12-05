@echo off
echo ========================================
echo   CLEAN START - Silent Signal AI
echo ========================================
echo.

cd /d C:\Users\HELLO\Silent-Signal-

echo [1/4] Killing any running servers...
taskkill /F /IM uvicorn.exe 2>nul
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

echo [2/4] Cleaning Python cache...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul

echo [3/4] Waiting for cleanup...
timeout /t 2 /nobreak >nul

echo [4/4] Starting fresh server...
echo.
echo Server will be available at:
echo   - http://localhost:8000
echo   - http://localhost:8000/demo
echo   - http://localhost:8000/test
echo.
echo Press Ctrl+C to stop
echo ========================================
echo.

.venv\Scripts\uvicorn.exe backend.main:app --reload --host 0.0.0.0 --port 8000

pause
