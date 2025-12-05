# 🔑 API Keys Setup Guide

## Current Status

Your Silent Signal AI works in **DEMO MODE** without API keys! However, to enable full functionality, you'll need to add API keys for external services.

## ✅ What Works Without API Keys

- ✅ Server running
- ✅ Health checks
- ✅ Database operations
- ✅ Frontend pages
- ✅ API testing interface
- ✅ Demo mode
- ✅ Pricing page

## ⚠️ What Needs API Keys

- ❌ User authentication (WorkOS)
- ❌ AI gesture classification (Cerebras)
- ❌ Text-to-speech (ElevenLabs)
- ❌ Payment processing (Stripe)
- ❌ Advanced AI workflows (Raindrop/LiquidMetal)
- ❌ Search & analytics (Searchable)

## 🚀 How to Add API Keys

### Step 1: Get Your API Keys

#### 1. **WorkOS** (Authentication) - RECOMMENDED FIRST
- Website: https://workos.com/
- Sign up for free account
- Create a new organization
- Get your API key and Client ID
- **Cost**: Free tier available

#### 2. **Cerebras** (AI Inference)
- Website: https://cerebras.ai/
- Sign up for developer account
- Get API key from dashboard
- **Cost**: Pay per use

#### 3. **ElevenLabs** (Text-to-Speech)
- Website: https://elevenlabs.io/
- Create account
- Get API key from settings
- **Cost**: Free tier: 10,000 characters/month

#### 4. **Stripe** (Payments) - Optional
- Website: https://stripe.com/
- Create account
- Get test API keys
- **Cost**: Transaction fees only

#### 5. **Raindrop AI** (LiquidMetal) - Optional
- Website: https://liquidmetal.ai/
- Contact for API access
- **Cost**: Contact for pricing

#### 6. **Searchable** (Search & Analytics) - Optional
- Website: https://searchable.ai/
- Sign up for account
- Get API key
- **Cost**: Free tier available

### Step 2: Add Keys to .env File

Open your `.env` file and add the keys:

```env
# ===== WORKOS (Authentication) =====
WORKOS_API_KEY=sk_live_your_actual_key_here
WORKOS_CLIENT_ID=client_your_actual_id_here
WORKOS_REDIRECT_URI=http://localhost:8000/auth/callback

# ===== CEREBRAS (AI Inference) =====
CEREBRAS_API_KEY=your_cerebras_key_here

# ===== ELEVENLABS (Text-to-Speech) =====
ELEVENLABS_API_KEY=your_elevenlabs_key_here
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM

# ===== STRIPE (Payments) - Optional =====
STRIPE_SECRET_KEY=sk_test_your_stripe_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_key_here

# ===== RAINDROP (AI Workflows) - Optional =====
RAINDROP_API_KEY=your_raindrop_key_here

# ===== SEARCHABLE (Search) - Optional =====
SEARCHABLE_API_KEY=your_searchable_key_here
```

### Step 3: Restart Your Server

After adding keys:
```cmd
# Stop the server (Ctrl+C in the terminal)
# Start it again
START_SERVER_HERE.bat
```

## 📋 Priority Order

### For Basic Testing (No API Keys Needed)
1. ✅ Use demo mode: http://localhost:8000/demo
2. ✅ Test API: http://localhost:8000/test
3. ✅ View docs: http://localhost:8000/api/docs

### For Authentication (Add First)
1. Get **WorkOS** API key
2. Add to `.env`
3. Restart server
4. Try "Get Started" button

### For Full Functionality
1. WorkOS (authentication)
2. Cerebras (AI classification)
3. ElevenLabs (text-to-speech)
4. Stripe (payments) - optional
5. Others - optional

## 🧪 Testing After Adding Keys

### Test WorkOS Authentication
```cmd
# Visit in browser
http://localhost:8000/auth/login
```

### Test Cerebras AI
```python
# Run test script
.venv\Scripts\python.exe -c "
from backend.integrations.cerebras_client import cerebras_client
import asyncio

async def test():
    result = await cerebras_client.classify_intention('tap', {}, '')
    print(result)

asyncio.run(test())
"
```

### Test ElevenLabs TTS
```python
# Run test script
.venv\Scripts\python.exe -c "
from backend.integrations.elevenlabs_client import elevenlabs_client
import asyncio

async def test():
    url = await elevenlabs_client.text_to_speech('Hello world', 1)
    print(f'Audio URL: {url}')

asyncio.run(test())
"
```

## 💡 Development Tips

### Start Without API Keys
- Use demo mode for development
- Build and test core features
- Add API keys when ready for integration testing

### Use Test/Development Keys
- Most services offer test keys
- Don't use production keys in development
- Keep keys in `.env`, never commit them

### Cost Management
- Start with free tiers
- Monitor usage in service dashboards
- Upgrade only when needed

## 🔒 Security Best Practices

1. **Never commit `.env` file** - It's in `.gitignore`
2. **Use test keys** in development
3. **Rotate keys** regularly
4. **Monitor usage** to detect issues
5. **Use environment variables** in production

## 🆘 Troubleshooting

### "Authentication service not configured"
- Add WorkOS API keys to `.env`
- Restart server
- Check keys are correct

### "API key invalid"
- Verify key is copied correctly
- Check for extra spaces
- Ensure key is active in service dashboard

### "Service unavailable"
- Check internet connection
- Verify service is not down
- Check API key has correct permissions

## 📚 Alternative: Build Without External APIs

You can build a fully functional app without external APIs by:

1. **Mock Authentication** - Create demo users in database
2. **Local AI Models** - Use lightweight models for gesture recognition
3. **Browser TTS** - Use Web Speech API for text-to-speech
4. **Skip Payments** - Focus on core features first

This approach lets you develop and test everything locally!

## 🎯 Recommended Approach

### Phase 1: Development (No API Keys)
- Build core features
- Test with demo mode
- Use mock data
- Focus on UI/UX

### Phase 2: Integration (Add Keys)
- Add WorkOS for auth
- Add Cerebras for AI
- Add ElevenLabs for TTS
- Test end-to-end

### Phase 3: Production (Production Keys)
- Get production API keys
- Set up monitoring
- Configure rate limits
- Deploy to cloud

## ✅ Current Recommendation

**For now, continue using demo mode!** You can:
- Visit http://localhost:8000/demo
- Test all features
- Build your gesture recognition
- Add API keys later when ready

Your app is fully functional in demo mode! 🎉
