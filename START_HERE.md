# 🎯 START HERE - Your First 5 Minutes

## ⚡ FASTEST WAY TO GET RUNNING

### 1️⃣ Install These 3 Things (One Time Only)

**Python** → https://www.python.org/downloads/ (Get 3.11+)
- ✅ Check "Add Python to PATH" when installing

**Node.js** → https://nodejs.org/ (Get LTS version)
- ✅ Just click Next, Next, Install

**Docker Desktop** → https://www.docker.com/products/docker-desktop/
- ✅ Install and restart your computer

---

### 2️⃣ Open Command Prompt Here

1. Press `Windows Key + R`
2. Type `cmd` and press Enter
3. Type this (replace with your actual path):
   ```cmd
   cd C:\path\to\silent-signal
   ```

---

### 3️⃣ Copy & Paste These Commands (One by One)

```cmd
copy .env.example .env
```
*(Creates your config file)*

```cmd
pip install -r requirements.txt
```
*(Installs Python stuff - takes 2-3 minutes)*

```cmd
cd frontend
npm install
cd ..
```
*(Installs frontend stuff - takes 1-2 minutes)*

```cmd
docker-compose up -d
```
*(Starts database - make sure Docker Desktop is open first!)*

```cmd
python scripts\init_db.py
```
*(Sets up database tables)*

---

### 4️⃣ Start the App

**Windows Users:**
```cmd
start.bat
```

**That's it!** Your browser should open automatically to http://localhost:8000

---

## 🔴 IF SOMETHING BREAKS

### "Python is not recognized"
→ You forgot to check "Add to PATH" when installing Python
→ Reinstall Python and check that box

### "Docker daemon is not running"
→ Open Docker Desktop app and wait for it to start
→ Look for whale icon in system tray

### "Port 8000 is already in use"
→ Something else is using that port
→ Close other apps or change port in `.env` file

### "pip is not recognized"
→ Try: `python -m pip install -r requirements.txt`

---

## 📋 WHAT YOU'LL SEE

When you visit http://localhost:8000:

1. **Landing Page** - Marketing page with features
2. **Login Button** - WorkOS authentication (needs API key)
3. **Dashboard** - Main app with gesture detection
4. **Settings** - Configure your preferences
5. **History** - See past gestures
6. **Pricing** - Stripe payment demo

---

## 🔑 GETTING API KEYS (For Full Functionality)

You need to sign up for these services (all have free tiers):

1. **WorkOS** → https://workos.com/ (Authentication)
2. **Cerebras** → https://cerebras.ai/ (AI Inference)
3. **ElevenLabs** → https://elevenlabs.io/ (Text-to-Speech)
4. **Raindrop/LiquidMetal** → Contact hackathon organizers
5. **Stripe** → https://stripe.com/ (Payments)
6. **Searchable** → https://searchable.ai/ (Search)

After signing up, copy your API keys into the `.env` file.

---

## 🎬 DEMO MODE (Without API Keys)

The app will run in **demo mode** without real API keys:
- ✅ You can see the UI
- ✅ You can test the frontend
- ❌ Authentication won't work
- ❌ Gesture detection won't process
- ❌ Speech generation won't work

To test everything, you need real API keys.

---

## 📚 MORE HELP

- **QUICKSTART.md** - Detailed beginner guide
- **docs/SETUP.md** - Complete setup instructions
- **docs/INTEGRATION_GUIDE.md** - How to configure each API
- **README.md** - Project overview

---

## ✅ CHECKLIST

- [ ] Installed Python 3.11+
- [ ] Installed Node.js
- [ ] Installed Docker Desktop
- [ ] Ran `copy .env.example .env`
- [ ] Ran `pip install -r requirements.txt`
- [ ] Ran `cd frontend && npm install && cd ..`
- [ ] Started Docker Desktop
- [ ] Ran `docker-compose up -d`
- [ ] Ran `python scripts\init_db.py`
- [ ] Ran `start.bat`
- [ ] Opened http://localhost:8000 in browser

---

## 🎉 YOU'RE DONE!

If you see the Silent Signal landing page, **you did it!**

Now explore the app and start adding your API keys to `.env` for full functionality.
