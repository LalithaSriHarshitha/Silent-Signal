# Silent Signal - API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication

All authenticated endpoints require a session cookie obtained through WorkOS login.

### Login Flow

**GET** `/auth/login`
- Returns authorization URL for WorkOS

**GET** `/auth/callback?code=...&state=...`
- Handles OAuth callback
- Sets session cookie
- Returns user token

**POST** `/auth/logout`
- Invalidates session
- Clears session cookie

**GET** `/auth/me`
- Returns current user profile

## Gestures

### WebSocket Endpoint

**WS** `/api/gestures/ws`

Send gesture data:
```json
{
  "user_id": 1,
  "gesture_type": "blink",
  "data": {
    "duration": 200,
    "intensity": 0.8,
    "eye": "both",
    "timestamp": 1234567890
  }
}
```

Receive response:
```json
{
  "gesture_id": 123,
  "intention": "yes",
  "confidence": 0.95,
  "text": "Yes",
  "audio_url": "/static/audio_cache/abc123.mp3",
  "processing_time_ms": 245
}
```

### HTTP Endpoints

**POST** `/api/gestures/`
- Create gesture (HTTP fallback)
- Body: `GestureCreate` schema

**GET** `/api/gestures/`
- Get user's gesture history
- Query params: `skip`, `limit`

**GET** `/api/gestures/{gesture_id}`
- Get specific gesture

**DELETE** `/api/gestures/{gesture_id}`
- Delete gesture

## Users

**GET** `/api/users/me`
- Get current user profile

**PUT** `/api/users/me`
- Update user profile
- Body: `UserUpdate` schema

**GET** `/api/users/preferences`
- Get user preferences

**PUT** `/api/users/preferences`
- Update preferences
- Body: `{ "gesture_sensitivity": "medium", "preferred_voice_id": "..." }`

## Payments

**POST** `/api/payments/create-checkout-session`
- Create Stripe checkout session
- Body: `{ "tier": "premium" }`

**POST** `/api/payments/cancel-subscription`
- Cancel user subscription

**POST** `/api/payments/webhook`
- Stripe webhook handler (internal)

## Search

**GET** `/api/search/gestures?q=...&limit=20`
- Search user's gestures

**GET** `/api/search/analytics`
- Get user analytics

## Health

**GET** `/api/health`
- System health check

**GET** `/api/status`
- Detailed system status

## Admin

**GET** `/api/admin/stats`
- System statistics (admin only)

## Schemas

### GestureCreate
```json
{
  "gesture_type": "blink|tap|micro_gesture",
  "raw_data": {
    // Type-specific data
  }
}
```

### UserUpdate
```json
{
  "full_name": "John Doe",
  "preferred_voice_id": "voice_id",
  "gesture_sensitivity": "low|medium|high"
}
```

## Error Responses

```json
{
  "detail": "Error message"
}
```

Status codes:
- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 429: Rate Limit Exceeded
- 500: Internal Server Error
