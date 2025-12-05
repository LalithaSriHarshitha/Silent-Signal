@echo off
echo Starting Silent Signal AI Server...
cd /d C:\Users\HELLO\Silent-Signal-

echo.
echo Server will start at: http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

.venv\Scripts\uvicorn.exe backend.main:app --reload --host 0.0.0.0 --port 8000
