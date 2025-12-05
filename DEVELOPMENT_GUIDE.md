# Silent Signal AI - Development Guide

## 🎯 Project Overview

Silent Signal AI is an offline + online multi-agent communication assistant for speech & hearing impaired people using:
- Hand gesture recognition
- Text-to-speech conversion
- Multi-agent AI system
- Real-time WebSocket communication

## 📋 Current Features

### ✅ Implemented
- FastAPI backend with async support
- SQLite database with 4 tables (users, gestures, sessions, subscriptions)
- WebSocket support for real-time gesture streaming
- Multi-agent gesture processing pipeline
- Authentication system (WorkOS integration)
- Payment processing (Stripe integration)
- Search functionality (Searchable.ai)
- Health monitoring endpoints
- Rate limiting and logging middleware

### 🔧 API Integrations
- **Cerebras AI** - Gesture intention classification
- **ElevenLabs** - Text-to-speech conversion
- **WorkOS** - User authentication
- **Stripe** - Payment processing
- **Raindrop/LiquidMetal** - AI workflow orchestration
- **Searchable** - Gesture search and analytics

## 🚀 Quick Start Testing

### 1. Test Health Endpoint
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "app": "Silent Signal",
  "environment": "development",
  "timestamp": "2025-12-02T..."
}
```

### 2. Access API Documentation
Open in browser:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

### 3. Test WebSocket Connection (JavaScript)
```javascript
const ws = new WebSocket('ws://localhost:8000/api/gestures/ws');

ws.onopen = () => {
    console.log('Connected to gesture stream');
    
    // Send gesture data
    ws.send(JSON.stringify({
        user_id: 1,
        gesture_type: "tap",
        data: {
            x: 100,
            y: 200,
            pressure: 0.8
        }
    }));
};

ws.onmessage = (event) => {
    const result = JSON.parse(event.data);
    console.log('Gesture processed:', result);
};
```

## 📁 Project Structure

```
Silent-Signal-/
├── backend/
│   ├── api/              # API utilities
│   ├── integrations/     # External service clients
│   │   ├── cerebras_client.py
│   │   ├── elevenlabs_client.py
│   │   ├── workos_client.py
│   │   ├── raindrop_client.py
│   │   └── searchable_client.py
│   ├── middleware/       # Custom middleware
│   ├── models/          # Database models
│   │   ├── user.py
│   │   ├── gesture.py
│   │   ├── session.py
│   │   └── subscription.py
│   ├── routes/          # API endpoints
│   │   ├── gestures.py  # Gesture processing
│   │   ├── users.py     # User management
│   │   ├── auth.py      # Authentication
│   │   ├── payments.py  # Stripe payments
│   │   └── health.py    # Health checks
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic
│   │   ├── gesture_service.py
│   │   └── user_service.py
│   ├── utils/           # Helper functions
│   ├── config.py        # Configuration
│   ├── database.py      # Database setup
│   └── main.py          # FastAPI app
├── frontend/
│   ├── static/          # CSS, JS, images
│   └── templates/       # HTML templates
├── .env                 # Environment variables
├── silentsignal.db     # SQLite database
└── requirements.txt     # Python dependencies
```

## 🔑 API Endpoints

### Health & Status
- `GET /api/health` - Basic health check
- `GET /api/status` - Detailed system status

### Gestures
- `WS /api/gestures/ws` - WebSocket for real-time gesture streaming
- `POST /api/gestures/` - Submit gesture (HTTP fallback)
- `GET /api/gestures/` - Get user's gesture history
- `GET /api/gestures/{id}` - Get specific gesture
- `DELETE /api/gestures/{id}` - Delete gesture

### Users
- `GET /api/users/me` - Get current user profile
- `PUT /api/users/me` - Update user profile
- `GET /api/users/{id}` - Get user by ID (admin)

### Authentication
- `GET /auth/login` - Initiate OAuth login
- `GET /auth/callback` - OAuth callback
- `POST /auth/logout` - Logout user

### Payments
- `POST /api/payments/create-checkout` - Create Stripe checkout
- `POST /api/payments/webhook` - Stripe webhook handler
- `GET /api/payments/subscription` - Get user subscription

## 🧪 Testing Workflow

### Step 1: Test Without Authentication
```bash
# Health check
curl http://localhost:8000/api/health

# System status
curl http://localhost:8000/api/status
```

### Step 2: Add API Keys (Optional)
Edit `.env` file:
```env
CEREBRAS_API_KEY=your_key
ELEVENLABS_API_KEY=your_key
WORKOS_API_KEY=your_key
WORKOS_CLIENT_ID=your_client_id
```

### Step 3: Test Gesture Processing
Use the Swagger UI at http://localhost:8000/api/docs

## 🛠️ Development Tasks

### Immediate Next Steps
1. ✅ Server running
2. ⏳ Test health endpoints
3. ⏳ Add gesture recognition model
4. ⏳ Create frontend UI
5. ⏳ Add API keys for integrations
6. ⏳ Test WebSocket connection
7. ⏳ Deploy to production

### Feature Enhancements
- [ ] Add camera/webcam gesture capture
- [ ] Implement offline mode with local models
- [ ] Add gesture training interface
- [ ] Create mobile-responsive UI
- [ ] Add voice feedback controls
- [ ] Implement gesture history analytics
- [ ] Add multi-language support

## 📝 Common Commands

### Start Server
```cmd
cd C:\Users\HELLO\Silent-Signal-
.venv\Scripts\uvicorn.exe backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Database Operations
```cmd
# Initialize database
.venv\Scripts\python.exe init_db.py

# Create migration
.venv\Scripts\alembic.exe revision --autogenerate -m "description"

# Run migrations
.venv\Scripts\alembic.exe upgrade head
```

### Install New Package
```cmd
.venv\Scripts\pip.exe install package-name
```

### Frontend Development
```cmd
cd frontend
npm run watch:css  # Watch Tailwind CSS changes
```

## 🐛 Troubleshooting

### Server won't start
- Check if port 8000 is already in use
- Verify `.env` file exists and has DATABASE_URL
- Check logs for missing dependencies

### Database errors
- Run `python init_db.py` to recreate tables
- Check DATABASE_URL in `.env`

### API integration errors
- Verify API keys in `.env`
- Check service status endpoints
- Review logs for specific error messages

## 📚 Resources

- FastAPI Docs: https://fastapi.tiangolo.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Pydantic: https://docs.pydantic.dev/
- WebSockets: https://websockets.readthedocs.io/

## 🎓 Learning Path

1. **Week 1**: Understand the codebase structure
2. **Week 2**: Add gesture recognition models
3. **Week 3**: Build frontend interface
4. **Week 4**: Integrate external APIs
5. **Week 5**: Testing and optimization
6. **Week 6**: Deployment and monitoring
