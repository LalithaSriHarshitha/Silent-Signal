# Integration Guide - Sponsor Tools

## 1. WorkOS (Authentication)

### Setup
1. Create account at https://workos.com
2. Create new project
3. Configure AuthKit
4. Get API key and Client ID

### Configuration
```env
WORKOS_API_KEY=sk_test_...
WORKOS_CLIENT_ID=client_...
WORKOS_REDIRECT_URI=http://localhost:8000/auth/callback
```

### Usage
- Login flow: `/auth/login`
- Callback: `/auth/callback`
- Session management via cookies

---

## 2. Cerebras (AI Inference)

### Setup
1. Sign up at https://cerebras.ai
2. Get API key
3. Choose model (llama3.1-8b recommended)

### Configuration
```env
CEREBRAS_API_KEY=your_key
CEREBRAS_MODEL=llama3.1-8b
```

### Usage
- Gesture classification
- Intention detection
- Embedding generation

---

## 3. ElevenLabs (Text-to-Speech)

### Setup
1. Create account at https://elevenlabs.io
2. Get API key
3. Choose voice ID

### Configuration
```env
ELEVENLABS_API_KEY=your_key
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM
```

### Usage
- Convert text to speech
- Audio caching in Redis
- Multiple voice support

---

## 4. Raindrop (LiquidMetal AI)

### Setup
1. Sign up at https://raindrop.ai
2. Create SmartFlow
3. Get API key and Flow ID

### Configuration
```env
RAINDROP_API_KEY=your_key
RAINDROP_SMARTFLOW_ID=your_flow_id
```

### Usage
- ML pipeline orchestration
- Secret management
- Smart action routing

---

## 5. Stripe (Payments)

### Setup
1. Create account at https://stripe.com
2. Get test API keys
3. Create products and prices
4. Configure webhook endpoint

### Configuration
```env
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PRICE_ID_PREMIUM=price_...
```

### Webhook Setup
- URL: `https://your-domain.com/api/payments/webhook`
- Events: `checkout.session.completed`, `customer.subscription.*`

---

## 6. Searchable (Search & Analytics)

### Setup
1. Sign up at https://searchable.ai
2. Create index
3. Get API key

### Configuration
```env
SEARCHABLE_API_KEY=your_key
SEARCHABLE_INDEX_NAME=silentsignal_gestures
```

### Usage
- Index gestures automatically
- Search user history
- Analytics dashboard

---

## 7. Vultr (Hosting)

### Setup
1. Create account at https://vultr.com
2. Deploy instance
3. Get API key

### Configuration
```env
VULTR_API_KEY=your_key
VULTR_INSTANCE_ID=your_instance
```

### Deployment
```bash
cd deploy
./vultr_deploy.sh
```

---

## 8. Cloudflare (CDN & Security)

### Setup
1. Create account at https://cloudflare.com
2. Add domain
3. Get API token

### Configuration
```env
CLOUDFLARE_API_TOKEN=your_token
CLOUDFLARE_ZONE_ID=your_zone
```

### Features
- DNS management
- CDN caching
- Rate limiting
- DDoS protection

---

## Testing Integrations

### WorkOS
```bash
curl http://localhost:8000/auth/login
```

### Cerebras
```python
from backend.integrations.cerebras_client import cerebras_client
result = await cerebras_client.classify_intention("blink", [0.2, 0.8, 1.0])
```

### ElevenLabs
```python
from backend.integrations.elevenlabs_client import elevenlabs_client
audio_url = await elevenlabs_client.text_to_speech("Hello", user_id=1)
```

### Stripe
```bash
curl -X POST http://localhost:8000/api/payments/create-checkout-session \
  -H "Content-Type: application/json" \
  -d '{"tier": "premium"}'
```

---

## Troubleshooting

### API Key Issues
- Verify keys are correct in .env
- Check key permissions
- Ensure keys are not expired

### Rate Limiting
- Implement exponential backoff
- Cache responses when possible
- Use batch operations

### Webhook Issues
- Verify webhook URL is accessible
- Check webhook secret
- Test with Stripe CLI: `stripe listen --forward-to localhost:8000/api/payments/webhook`
