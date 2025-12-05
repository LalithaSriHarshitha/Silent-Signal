@echo off
echo ========================================
echo Silent Signal AI - Quick Start
echo ========================================
echo.
cd /d C:\Users\HELLO\Silent-Signal-

echo [1/2] Checking dependencies...
.venv\Scripts\python.exe -c "import fastapi, uvicorn, sqlalchemy, numpy; print('✓ All dependencies installed')"

echo.
echo [2/2] Starting server...
echo Server URL: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

.venv\Scripts\uvicorn.exe backend.main:app --reload --host 0.0.0.0 --port 8000
