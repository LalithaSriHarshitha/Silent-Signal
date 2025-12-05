# 📝 COMMAND CHEAT SHEET

## Quick Reference for All Commands

---

## 🚀 FIRST TIME SETUP

```cmd
REM 1. Create environment file
copy .env.example .env

REM 2. Install Python dependencies
pip install -r requirements.txt

REM 3. Install frontend dependencies
cd frontend
npm install
cd ..

REM 4. Start database services
docker-compose up -d

REM 5. Initialize database
python scripts\init_db.py

REM 6. (Optional) Add demo data
python scripts\seed_demo_data.py
```

---

## ▶️ STARTING THE APP

### Quick Start (Recommended)
```cmd
start.bat
```

### Manual Start
```cmd
REM Terminal 1 - Build CSS
cd frontend
npm run build:css

REM Terminal 2 - Start server
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Start with Custom Port
```cmd
uvicorn backend.main:app --port 8001
```

---

## 🛑 STOPPING THE APP

### Stop Backend
```
Press Ctrl+C in the terminal
```

### Stop Docker Services
```cmd
docker-compose stop
```

### Stop Everything
```cmd
docker-compose down
```

---

## 🐳 DOCKER COMMANDS

### Start Services
```cmd
docker-compose up -d
```

### Stop Services
```cmd
docker-compose stop
```

### Restart Services
```cmd
docker-compose restart
```

### View Running Containers
```cmd
docker ps
```

### View All Containers (including stopped)
```cmd
docker ps -a
```

### View Logs
```cmd
REM All services
docker-compose logs

REM Specific service
docker-compose logs postgres
docker-compose logs redis

REM Follow logs (real-time)
docker-compose logs -f
```

### Remove Everything (Clean Slate)
```cmd
docker-compose down -v
```

### Access PostgreSQL
```cmd
docker exec -it silentsignal-postgres psql -U silentsignal -d silentsignal_db
```

### Access Redis CLI
```cmd
docker exec -it silentsignal-redis redis-cli
```

---

## 🗄️ DATABASE COMMANDS

### Initialize Database
```cmd
python scripts\init_db.py
```

### Seed Demo Data
```cmd
python scripts\seed_demo_data.py
```

### Reset Database
```cmd
docker-compose down -v
docker-compose up -d
timeout /t 5
python scripts\init_db.py
```

### Backup Database
```cmd
docker exec silentsignal-postgres pg_dump -U silentsignal silentsignal_db > backup.sql
```

### Restore Database
```cmd
docker exec -i silentsignal-postgres psql -U silentsignal -d silentsignal_db < backup.sql
```

---

## 📦 PYTHON COMMANDS

### Install Dependencies
```cmd
pip install -r requirements.txt
```

### Install Single Package
```cmd
pip install package-name
```

### Update All Packages
```cmd
pip install --upgrade -r requirements.txt
```

### List Installed Packages
```cmd
pip list
```

### Check for Outdated Packages
```cmd
pip list --outdated
```

### Create Virtual Environment (Optional)
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🎨 FRONTEND COMMANDS

### Install Dependencies
```cmd
cd frontend
npm install
cd ..
```

### Build CSS (One Time)
```cmd
cd frontend
npm run build:css
cd ..
```

### Watch CSS (Auto-rebuild on changes)
```cmd
cd frontend
npm run watch:css
```

### Update Dependencies
```cmd
cd frontend
npm update
cd ..
```

---

## 🧪 TESTING COMMANDS

### Test Backend Health
```cmd
curl http://localhost:8000/health
```
Or visit in browser: http://localhost:8000/health

### Test Database Connection
```cmd
python -c "from backend.database import engine; print('Database OK')"
```

### Test Redis Connection
```cmd
docker exec -it silentsignal-redis redis-cli ping
```
Should return: `PONG`

### Test API Endpoint
```cmd
curl http://localhost:8000/api/docs
```
Or visit in browser: http://localhost:8000/api/docs

---

## 🔍 DEBUGGING COMMANDS

### Check Python Version
```cmd
python --version
```

### Check pip Version
```cmd
pip --version
```

### Check Node Version
```cmd
node --version
```

### Check npm Version
```cmd
npm --version
```

### Check Docker Version
```cmd
docker --version
```

### Check Docker Compose Version
```cmd
docker-compose --version
```

### Find Process Using Port
```cmd
netstat -ano | findstr :8000
```

### Kill Process by PID
```cmd
taskkill /PID <number> /F
```

### View Environment Variables
```cmd
type .env
```

### Check if File Exists
```cmd
dir .env
dir frontend\node_modules
dir frontend\static\css\output.css
```

---

## 🧹 CLEANUP COMMANDS

### Remove Python Cache
```cmd
rmdir /s /q __pycache__
rmdir /s /q backend\__pycache__
```

### Remove Node Modules
```cmd
rmdir /s /q frontend\node_modules
```

### Remove Docker Volumes
```cmd
docker-compose down -v
```

### Clean Everything
```cmd
docker-compose down -v
rmdir /s /q __pycache__
rmdir /s /q backend\__pycache__
rmdir /s /q frontend\node_modules
```

---

## 📊 MONITORING COMMANDS

### Watch Backend Logs
```cmd
REM Just run the server and watch terminal output
uvicorn backend.main:app --reload
```

### Watch Docker Logs
```cmd
docker-compose logs -f
```

### Check Disk Space
```cmd
docker system df
```

### Check Container Resource Usage
```cmd
docker stats
```

---

## 🔐 SECURITY COMMANDS

### Generate Secret Key
```cmd
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Check for Security Issues
```cmd
pip install safety
safety check
```

---

## 📝 GIT COMMANDS (If using version control)

### Initialize Git
```cmd
git init
```

### Add All Files
```cmd
git add .
```

### Commit Changes
```cmd
git commit -m "Initial commit"
```

### Check Status
```cmd
git status
```

### View Changes
```cmd
git diff
```

---

## 🚀 DEPLOYMENT COMMANDS

### Build Docker Image
```cmd
docker build -t silentsignal:latest .
```

### Run Production Server
```cmd
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Deploy to Vultr (if configured)
```cmd
bash deploy\vultr_deploy.sh
```

---

## 🆘 EMERGENCY COMMANDS

### Nuclear Reset (Start Fresh)
```cmd
REM Stop everything
docker-compose down -v
taskkill /F /IM python.exe

REM Clean cache
rmdir /s /q __pycache__
rmdir /s /q backend\__pycache__

REM Reinstall
pip install --force-reinstall -r requirements.txt
cd frontend
npm install
npm run build:css
cd ..

REM Restart
docker-compose up -d
timeout /t 5
python scripts\init_db.py
start.bat
```

---

## 📚 USEFUL URLS

```
Landing Page:       http://localhost:8000
Dashboard:          http://localhost:8000/dashboard
API Docs:           http://localhost:8000/api/docs
Health Check:       http://localhost:8000/health
Admin Panel:        http://localhost:8000/admin
```

---

## 💡 PRO TIPS

### Run Multiple Commands at Once
```cmd
command1 & command2 & command3
```

### Run Command in Background
```cmd
start /B command
```

### Create Alias (Shortcut)
Create a `.bat` file:
```cmd
@echo off
docker-compose up -d
timeout /t 5
python scripts\init_db.py
uvicorn backend.main:app --reload
```

### Check All Services Status
```cmd
docker ps & python --version & node --version
```

---

## 🎯 COMMON WORKFLOWS

### Daily Development Start
```cmd
docker-compose up -d
start.bat
```

### Daily Development End
```cmd
REM Press Ctrl+C to stop server
docker-compose stop
```

### After Changing .env
```cmd
REM Restart server (Ctrl+C then)
start.bat
```

### After Changing Frontend CSS
```cmd
cd frontend
npm run build:css
cd ..
REM Refresh browser
```

### After Changing Backend Code
```cmd
REM Server auto-reloads if using --reload flag
REM Just refresh browser
```

### After Pulling New Code
```cmd
pip install -r requirements.txt
cd frontend
npm install
npm run build:css
cd ..
docker-compose restart
python scripts\init_db.py
```

---

## 📋 CHECKLIST COMMANDS

Run these to verify setup:

```cmd
python --version
pip --version
node --version
npm --version
docker --version
docker-compose --version
docker ps
dir .env
pip list | findstr fastapi
dir frontend\node_modules
dir frontend\static\css\output.css
curl http://localhost:8000/health
```

All should complete successfully!

---

## 🔖 BOOKMARK THIS FILE

Keep this file open for quick reference while developing!
