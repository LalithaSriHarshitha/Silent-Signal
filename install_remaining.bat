@echo off
echo Installing remaining dependencies...
cd /d C:\Users\HELLO\Silent-Signal-

echo.
echo Installing numpy...
.venv\Scripts\python.exe -m pip install numpy

echo.
echo Installing email-validator...
.venv\Scripts\python.exe -m pip install email-validator

echo.
echo Checking installed packages...
.venv\Scripts\pip.exe list

echo.
echo Installation complete!
echo.
echo To start the server, run:
echo .venv\Scripts\uvicorn.exe backend.main:app --reload --host 0.0.0.0 --port 8000
pause
