# 🚀 QUICK START GUIDE - Silent Signal

## For Complete Beginners - Step by Step

### What You Need to Install First

#### 1. Install Python (3.11 or higher)
- Go to https://www.python.org/downloads/
- Download Python 3.11+ for Windows
- **IMPORTANT**: Check "Add Python to PATH" during installation
- Verify: Open Command Prompt and type: `python --version`

#### 2. Install Node.js (for frontend CSS building)
- Go to https://nodejs.org/
- Download LTS version for Windows
- Install with default settings
- Verify: Open Command Prompt and type: `node --version`

#### 3. Install Docker Desktop (for database)
- Go to https://www.docker.com/products/docker-desktop/
- Download for Windows
- Install and restart your computer
- Open Docker Desktop and let it start

---

## 🎯 STEP-BY-STEP: Getting Started

### Step 1: Open This Project in Your Terminal

1. Open Command Prompt (search "cmd" in Windows)
2. Navigate to this project folder:
   ```cmd
   cd path\to\silent-signal
   ```

### Step 2: Set Up Environment Variables

1. Copy the example environment file:
   ```cmd
   copy .env.example .env
   ```

2. Open `.env` file in a text editor (Notepad works)

3. Fill in these **REQUIRED** values (get from hackathon sponsors):

```env
# WorkOS (Authentication)
WORKOS_API_KEY=your_workos_api_key_here
WORKOS_CLIENT_ID=your_workos_client_id_here

# Cerebras (AI Inference)
CEREBRAS_API_KEY=your_cerebras_api_key_here

# ElevenLabs (Text-to-Speech)
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# LiquidMetal/Raindrop (Orchestration)
RAINDROP_API_KEY=your_raindrop_api_key_here
RAINDROP_API_URL=https://api.raindrop.ai

# Stripe (Payments)
STRIPE_SECRET_KEY=your_stripe_secret_key_here
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key_here

# Searchable (Search/Analytics)
SEARCHABLE_API_KEY=your_searchable_api_key_here

# Database (leave as-is for local development)
DATABASE_URL=postgresql://silentsignal:password@localhost:5432/silentsignal
REDIS_URL=redis://localhost:6379/0
```

4. Save the `.env` file

### Step 3: Install Python Dependencies

```cmd
pip install -r requirements.txt
```

This will take 2-3 minutes. Wait for it to complete.

### Step 4: Install Frontend Dependencies

```cmd
cd frontend
npm install
cd ..
```

### Step 5: Start Database Services

Make sure Docker Desktop is running, then:

```cmd
docker-compose up -d
```

This starts PostgreSQL and Redis in the background.

### Step 6: Initialize the Database

```cmd
python scripts/init_db.py
```

This creates all necessary database tables.

### Step 7: (Optional) Add Demo Data

```cmd
python scripts/seed_demo_data.py
```

This adds sample users and gestures for testing.

---

## ▶️ RUNNING THE APPLICATION

### Option A: Use the Start Script (Easiest)

**Windows:**
```cmd
start.bat
```

This will:
- Build the frontend CSS
- Start the FastAPI backend server
- Open your browser automatically

### Option B: Manual Start

**Terminal 1 - Build Frontend CSS:**
```cmd
cd frontend
npm run build:css
```

**Terminal 2 - Start Backend:**
```cmd
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Open Browser:**
Go to: http://localhost:8000

---

## 🧪 TESTING THE APP

### 1. Check if Backend is Running
Open browser: http://localhost:8000/health

You should see:
```json
{
  "status": "healthy",
  "services": {...}
}
```

### 2. Visit the Landing Page
Go to: http://localhost:8000

### 3. Try Login (if WorkOS is configured)
Click "Login" button

### 4. Test Gesture Detection
- Go to Dashboard
- Allow camera access
- Blink or make gestures
- See real-time detection

---

## 🔧 TROUBLESHOOTING

### "Python is not recognized"
- Reinstall Python and check "Add to PATH"
- Restart Command Prompt

### "Docker is not running"
- Open Docker Desktop application
- Wait for it to fully start (whale icon in system tray)

### "Port 8000 already in use"
- Stop other applications using port 8000
- Or change port: `uvicorn backend.main:app --port 8001`

### "Module not found" errors
- Make sure you ran: `pip install -r requirements.txt`
- Try: `pip install --upgrade pip` then reinstall

### Database connection errors
- Check Docker is running: `docker ps`
- Restart containers: `docker-compose restart`

### Frontend looks broken (no styling)
- Build CSS: `cd frontend && npm run build:css`
- Check `frontend/static/css/output.css` exists

---

## 📝 WHAT EACH FILE DOES

- **backend/main.py** - Main FastAPI application entry point
- **backend/routes/** - API endpoints (auth, gestures, payments, etc.)
- **backend/services/** - Business logic
- **backend/integrations/** - External API clients (Cerebras, ElevenLabs, etc.)
- **frontend/templates/** - HTML pages
- **frontend/static/** - CSS, JavaScript, images
- **.env** - Your secret configuration (NEVER commit this!)
- **docker-compose.yml** - Database setup
- **requirements.txt** - Python packages needed

---

## 🎓 LEARNING RESOURCES

### FastAPI (Backend Framework)
- Official Tutorial: https://fastapi.tiangolo.com/tutorial/

### Jinja2 (HTML Templates)
- Documentation: https://jinja.palletsprojects.com/

### TailwindCSS (Styling)
- Documentation: https://tailwindcss.com/docs

### WebSockets (Real-time Communication)
- MDN Guide: https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API

---

## 🆘 GETTING HELP

1. Check `docs/SETUP.md` for detailed setup instructions
2. Check `docs/API_DOCS.md` for API endpoint documentation
3. Check `docs/INTEGRATION_GUIDE.md` for sponsor tool setup
4. Read error messages carefully - they usually tell you what's wrong
5. Check the logs in your terminal for detailed error information

---

## ✅ NEXT STEPS

Once everything is running:

1. **Configure Sponsor APIs** - Add real API keys to `.env`
2. **Test Each Integration** - Follow `docs/INTEGRATION_GUIDE.md`
3. **Customize the UI** - Edit files in `frontend/templates/`
4. **Add Features** - Modify `backend/routes/` and `backend/services/`
5. **Deploy** - Follow `docs/DEPLOYMENT.md` when ready

---

## 🎉 YOU'RE READY!

The app should now be running at: **http://localhost:8000**

Start by exploring the landing page, then try the dashboard with gesture detection!
