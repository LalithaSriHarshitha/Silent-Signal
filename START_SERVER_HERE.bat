@echo off
cls
echo.
echo ========================================
echo   SILENT SIGNAL AI - SERVER STARTUP
echo ========================================
echo.
cd /d C:\Users\HELLO\Silent-Signal-
echo Starting server...
echo.
echo Server will be available at:
echo   - http://localhost:8000
echo   - http://localhost:8000/test (Test Dashboard)
echo   - http://localhost:8000/api/docs (API Docs)
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

.venv\Scripts\uvicorn.exe backend.main:app --reload --host 0.0.0.0 --port 8000

pause
