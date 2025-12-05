# Silent Signal - Setup Guide

## Environment Variables

Copy `.env.example` to `.env` and configure the following:

### Required API Keys

#### 1. WorkOS (Authentication)
```
WORKOS_API_KEY=sk_test_...
WORKOS_CLIENT_ID=client_...
WORKOS_REDIRECT_URI=http://localhost:8000/auth/callback
```
Get keys from: https://workos.com

#### 2. Cerebras (AI Inference)
```
CEREBRAS_API_KEY=your_key
CEREBRAS_MODEL=llama3.1-8b
```
Get keys from: https://cerebras.ai

#### 3. ElevenLabs (Text-to-Speech)
```
ELEVENLABS_API_KEY=your_key
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM
```
Get keys from: https://elevenlabs.io

#### 4. Raindrop (LiquidMetal AI)
```
RAINDROP_API_KEY=your_key
RAINDROP_SMARTFLOW_ID=your_flow_id
```
Get keys from: https://raindrop.ai

#### 5. Stripe (Payments)
```
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```
Get keys from: https://stripe.com

#### 6. Searchable (Search & Analytics)
```
SEARCHABLE_API_KEY=your_key
SEARCHABLE_INDEX_NAME=silentsignal_gestures
```
Get keys from: https://searchable.ai

#### 7. Vultr (Hosting)
```
VULTR_API_KEY=your_key
```
Get keys from: https://vultr.com

#### 8. Cloudflare (CDN)
```
CLOUDFLARE_API_TOKEN=your_token
CLOUDFLARE_ZONE_ID=your_zone
```
Get keys from: https://cloudflare.com

## Database Setup

1. Start PostgreSQL and Redis:
```bash
docker-compose up -d
```

2. Initialize database:
```bash
python -c "from backend.database import init_db; init_db()"
```

## Frontend Setup

```bash
cd frontend
npm install
npm run build:css
```

## Running the Application

### Development
```bash
uvicorn backend.main:app --reload --port 8000
```

### Production
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=backend
```

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running: `docker ps`
- Check DATABASE_URL in .env

### Redis Connection Issues
- Ensure Redis is running: `docker ps`
- Check REDIS_URL in .env

### Camera Access Issues
- Use HTTPS or localhost
- Grant camera permissions in browser

### WebSocket Connection Issues
- Check firewall settings
- Ensure correct WebSocket URL protocol (ws:// or wss://)

## Next Steps

1. Configure all API keys
2. Test authentication flow
3. Test gesture capture
4. Deploy to Vultr
5. Configure Cloudflare DNS
