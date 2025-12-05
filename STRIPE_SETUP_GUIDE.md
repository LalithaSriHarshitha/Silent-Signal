# Stripe Payment Setup Guide

## Current Status
✅ Stripe API keys are configured  
❌ Stripe Price IDs are missing

## What You Need to Do

### 1. Create Products in Stripe Dashboard

1. Go to https://dashboard.stripe.com/test/products
2. Click "Add product"

#### Free Tier Product
- **Name**: Silent Signal Free
- **Description**: 100 gestures per day, basic features
- **Pricing**: $0.00 / month (recurring)
- Click "Save product"
- Copy the **Price ID** (starts with `price_`)

#### Premium Tier Product
- **Name**: Silent Signal Premium
- **Description**: Unlimited gestures, all features
- **Pricing**: $9.00 / month (recurring)
- Click "Save product"
- Copy the **Price ID** (starts with `price_`)

### 2. Update Your .env File

Add the Price IDs you copied:

```env
STRIPE_PRICE_ID_FREE=price_xxxxxxxxxxxxx
STRIPE_PRICE_ID_PREMIUM=price_xxxxxxxxxxxxx
```

### 3. Set Up Webhook (Optional but Recommended)

1. Go to https://dashboard.stripe.com/test/webhooks
2. Click "Add endpoint"
3. Enter your endpoint URL: `http://localhost:8000/api/payments/webhook`
4. Select events to listen to:
   - `checkout.session.completed`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
5. Copy the **Webhook Secret** (starts with `whsec_`)
6. Add to .env:
   ```env
   STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxx
   ```

### 4. Restart Your Server

```bash
START_SERVER_HERE.bat
```

## Testing Payments

Use Stripe test cards:
- **Success**: 4242 4242 4242 4242
- **Decline**: 4000 0000 0000 0002
- Any future expiry date (e.g., 12/34)
- Any 3-digit CVC

## Current Behavior

Without Price IDs configured, clicking "Upgrade to Premium" will show:
> "Payment system not configured yet. Stripe Price IDs are missing. Please contact support."

This is expected and prevents errors. Once you add the Price IDs, the checkout will work properly.
