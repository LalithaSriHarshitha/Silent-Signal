# Silent Signal 🤫

**Gesture-based communication platform powered by AI**

Silent Signal enables communication through subtle physical cues like blinks, micro-gestures, and taps. Using advanced AI models, gestures are classified into intentions and converted to natural speech output.

---

## 🎯 NEW TO THIS PROJECT? START HERE!

### 📚 Complete Beginner Guides

**Never coded before? No problem!**

1. **[START_HERE.md](START_HERE.md)** ⭐ - Your first 5 minutes (READ THIS FIRST!)
2. **[QUICKSTART.md](QUICKSTART.md)** - Detailed step-by-step guide
3. **[COMMANDS_CHEATSHEET.md](COMMANDS_CHEATSHEET.md)** - All commands in one place
4. **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - When things go wrong
5. **[HOW_IT_WORKS.md](HOW_IT_WORKS.md)** - Understanding the system
6. **[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)** - Navigate all docs

**These guides assume ZERO prior knowledge and walk you through everything!**

---

## 🏆 Hackathon Sponsor Integrations

This MVP integrates **ALL 8 mandatory sponsor tools**:

1. **LiquidMetal AI (Raindrop)** - SmartFlow orchestration & secret management
2. **Vultr** - Backend hosting & object storage
3. **Cerebras** - AI inference for gesture classification
4. **ElevenLabs** - Text-to-speech generation
5. **Netlify** - Static frontend hosting (optional)
6. **WorkOS** - Authentication & user management
7. **Stripe** - Payment processing & subscriptions
8. **Searchable** - Gesture indexing & analytics

---

## 🚀 Quick Start (For Experienced Developers)

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL
- Redis

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd silent-signal
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. **Start database services**
```bash
docker-compose up -d
```

4. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

5. **Install frontend dependencies**
```bash
cd frontend
npm install
npm run build:css
cd ..
```

6. **Initialize database**
```bash
python -c "from backend.database import init_db; init_db()"
```

7. **Run the application**
```bash
uvicorn backend.main:app --reload
```

8. **Access the application**
```
http://localhost:8000
```

## 📁 Project Structure

```
silent-signal/
├── backend/
│   ├── api/              # API layer
│   ├── routes/           # API routes
│   ├── services/         # Business logic
│   ├── integrations/     # External service clients
│   ├── models/           # Database models
│   ├── schemas/          # Pydantic schemas
│   ├── middleware/       # Custom middleware
│   └── utils/            # Utilities
├── frontend/
│   ├── static/           # CSS, JS, images
│   └── templates/        # Jinja2 templates
├── docs/                 # Documentation
├── deploy/               # Deployment scripts
└── docker-compose.yml    # Local development
```

## 🔧 Configuration

See [SETUP.md](docs/SETUP.md) for detailed configuration instructions.

## 📚 Documentation

- [Setup Guide](docs/SETUP.md)
- [API Documentation](docs/API_DOCS.md)
- [Integration Guide](docs/INTEGRATION_GUIDE.md)
- [Deployment Guide](docs/DEPLOYMENT.md)

## 🎯 Features

- **Real-time Gesture Detection** - WebSocket-based streaming
- **AI-Powered Classification** - Cerebras inference
- **Natural Speech Output** - ElevenLabs TTS
- **User Authentication** - WorkOS integration
- **Premium Subscriptions** - Stripe payments
- **Search & Analytics** - Searchable indexing
- **Gesture History** - Full audit trail

## 🛠 Tech Stack

**Backend:**
- FastAPI
- SQLAlchemy + PostgreSQL
- Redis
- WebSockets

**Frontend:**
- Jinja2 Templates
- TailwindCSS
- Vanilla JavaScript
- WebRTC

**AI/ML:**
- Cerebras AI
- ElevenLabs

**Infrastructure:**
- Vultr (hosting)
- Cloudflare (CDN)
- Docker

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please read CONTRIBUTING.md first.

## 📧 Support

For issues and questions, please open a GitHub issue.

---

Built with ❤️ for the hackathon
