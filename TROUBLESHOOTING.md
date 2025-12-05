# 🔧 TROUBLESHOOTING GUIDE

## Common Issues & Solutions

### ❌ "python is not recognized as an internal or external command"

**Problem:** Python is not installed or not in PATH

**Solution:**
1. Download Python from https://www.python.org/downloads/
2. Run installer
3. **IMPORTANT:** Check the box "Add Python to PATH"
4. Click "Install Now"
5. Restart Command Prompt
6. Test: `python --version`

---

### ❌ "pip is not recognized"

**Problem:** pip is not in PATH

**Solution:**
Try using Python module syntax:
```cmd
python -m pip install -r requirements.txt
```

---

### ❌ "docker-compose is not recognized" or "Cannot connect to Docker daemon"

**Problem:** Docker Desktop is not installed or not running

**Solution:**
1. Install Docker Desktop from https://www.docker.com/products/docker-desktop/
2. Open Docker Desktop application
3. Wait for it to fully start (whale icon in system tray should be steady, not animated)
4. Try again: `docker-compose up -d`

**Check if Docker is running:**
```cmd
docker ps
```
You should see a list of containers (might be empty, that's OK)

---

### ❌ "Port 8000 is already in use"

**Problem:** Another application is using port 8000

**Solution 1 - Find and stop the other app:**
```cmd
netstat -ano | findstr :8000
```
This shows the Process ID (PID). Then:
```cmd
taskkill /PID <number> /F
```

**Solution 2 - Use a different port:**
Edit `.env` file and change:
```env
API_PORT=8001
```
Then start with:
```cmd
uvicorn backend.main:app --port 8001
```

---

### ❌ "ModuleNotFoundError: No module named 'fastapi'"

**Problem:** Python packages not installed

**Solution:**
```cmd
pip install -r requirements.txt
```

If that fails, try:
```cmd
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

### ❌ "Could not connect to database"

**Problem:** PostgreSQL is not running or wrong credentials

**Solution:**

**Check if Docker containers are running:**
```cmd
docker ps
```
You should see `silentsignal-postgres` and `silentsignal-redis`

**If not running, start them:**
```cmd
docker-compose up -d
```

**Check logs:**
```cmd
docker-compose logs postgres
```

**Reset database:**
```cmd
docker-compose down -v
docker-compose up -d
python scripts\init_db.py
```

---

### ❌ "Redis connection failed"

**Problem:** Redis is not running

**Solution:**
```cmd
docker-compose restart redis
```

**Check Redis is working:**
```cmd
docker exec -it silentsignal-redis redis-cli ping
```
Should respond with: `PONG`

---

### ❌ Frontend has no styling (looks broken)

**Problem:** TailwindCSS not built

**Solution:**
```cmd
cd frontend
npm install
npm run build:css
cd ..
```

**Check if output.css exists:**
```cmd
dir frontend\static\css\output.css
```

---

### ❌ "npm is not recognized"

**Problem:** Node.js not installed

**Solution:**
1. Download from https://nodejs.org/
2. Install LTS version
3. Restart Command Prompt
4. Test: `node --version` and `npm --version`

---

### ❌ "Cannot find module 'uvicorn'"

**Problem:** uvicorn not installed

**Solution:**
```cmd
pip install uvicorn[standard]
```

---

### ❌ "WorkOS authentication not working"

**Problem:** Missing or invalid API keys

**Solution:**
1. Sign up at https://workos.com/
2. Get your API key and Client ID
3. Edit `.env` file:
```env
WORKOS_API_KEY=sk_test_your_actual_key
WORKOS_CLIENT_ID=client_your_actual_id
```
4. Restart the server

---

### ❌ "Gesture detection not working"

**Problem:** Camera permissions or missing API keys

**Solution:**

**Check browser permissions:**
- Click the lock icon in address bar
- Allow camera access
- Refresh page

**Check Cerebras API key:**
- Edit `.env` file
- Add valid `CEREBRAS_API_KEY`
- Restart server

**Check browser console:**
- Press F12 in browser
- Look for errors in Console tab

---

### ❌ "Speech not playing"

**Problem:** ElevenLabs API key missing or invalid

**Solution:**
1. Sign up at https://elevenlabs.io/
2. Get API key
3. Edit `.env`:
```env
ELEVENLABS_API_KEY=your_actual_key
```
4. Restart server

---

### ❌ "Internal Server Error 500"

**Problem:** Backend error

**Solution:**

**Check backend logs:**
Look at the terminal where you ran `start.bat` or `uvicorn`

**Common causes:**
- Missing environment variables
- Database connection failed
- Invalid API keys
- Missing dependencies

**Debug mode:**
Edit `.env`:
```env
DEBUG=True
LOG_LEVEL=DEBUG
```
Restart and check detailed error messages

---

### ❌ "CORS error in browser"

**Problem:** Frontend and backend on different domains

**Solution:**
Edit `.env`:
```env
CORS_ORIGINS=http://localhost:8000,http://localhost:3000,http://127.0.0.1:8000
```
Restart server

---

### ❌ "Database tables don't exist"

**Problem:** Database not initialized

**Solution:**
```cmd
python scripts\init_db.py
```

**If that fails:**
```cmd
docker-compose down -v
docker-compose up -d
timeout /t 5
python scripts\init_db.py
```

---

### ❌ "Permission denied" errors

**Problem:** File permissions or admin rights needed

**Solution:**
Run Command Prompt as Administrator:
1. Search "cmd" in Windows
2. Right-click "Command Prompt"
3. Select "Run as administrator"
4. Navigate to project and try again

---

## 🔍 DEBUGGING CHECKLIST

When something doesn't work, check these in order:

1. **Is Docker running?**
   ```cmd
   docker ps
   ```

2. **Are dependencies installed?**
   ```cmd
   pip list | findstr fastapi
   ```

3. **Is .env file configured?**
   ```cmd
   type .env
   ```

4. **Are database tables created?**
   ```cmd
   python scripts\init_db.py
   ```

5. **Is the server running?**
   - Check terminal for errors
   - Visit http://localhost:8000/health

6. **Are API keys valid?**
   - Check each service dashboard
   - Verify keys in `.env`

---

## 📞 STILL STUCK?

### Check Logs

**Backend logs:**
Look at terminal where `uvicorn` is running

**Docker logs:**
```cmd
docker-compose logs
```

**Specific service:**
```cmd
docker-compose logs postgres
docker-compose logs redis
```

### Test Individual Components

**Test database connection:**
```cmd
python -c "from backend.database import engine; print('DB OK')"
```

**Test Redis connection:**
```cmd
docker exec -it silentsignal-redis redis-cli ping
```

**Test API health:**
```cmd
curl http://localhost:8000/health
```
Or visit in browser

### Clean Slate (Nuclear Option)

If nothing works, start fresh:

```cmd
REM Stop everything
docker-compose down -v
taskkill /F /IM python.exe

REM Clean Python cache
rmdir /s /q __pycache__
rmdir /s /q backend\__pycache__

REM Reinstall
pip install --force-reinstall -r requirements.txt

REM Restart
docker-compose up -d
timeout /t 5
python scripts\init_db.py
start.bat
```

---

## 💡 TIPS

- Always check the terminal for error messages
- Read error messages carefully - they usually tell you what's wrong
- Make sure Docker Desktop is running before starting the app
- Restart the server after changing `.env` file
- Use `Ctrl+C` to stop the server gracefully
- Check browser console (F12) for frontend errors

---

## ✅ VERIFICATION COMMANDS

Run these to verify everything is set up correctly:

```cmd
REM Check Python
python --version

REM Check pip
pip --version

REM Check Node.js
node --version

REM Check npm
npm --version

REM Check Docker
docker --version

REM Check Docker Compose
docker-compose --version

REM Check if containers are running
docker ps

REM Check if dependencies are installed
pip list

REM Check if .env exists
dir .env

REM Test database
python -c "from backend.database import engine; print('Database OK')"
```

All should complete without errors!
