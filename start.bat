@echo off
REM Silent Signal - Windows Startup Script

echo Starting Silent Signal...

REM Check if .env exists
if not exist .env (
    echo .env file not found. Copying from .env.example...
    copy .env.example .env
    echo Please edit .env with your API keys before continuing.
    pause
    exit /b 1
)

REM Start Docker services
echo Starting Docker services (PostgreSQL, Redis)...
docker-compose up -d

REM Wait for services
echo Waiting for services to be ready...
timeout /t 5 /nobreak

REM Initialize database
echo Checking database...
python scripts\init_db.py

REM Install frontend dependencies if needed
if not exist "frontend\node_modules" (
    echo Installing frontend dependencies...
    cd frontend
    call npm install
    call npm run build:css
    cd ..
)

REM Start the application
echo Starting Silent Signal API...
echo Application will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/api/docs
echo.
echo Press Ctrl+C to stop
echo.

uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
