"""Payment and subscription routes"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import structlog

from backend.database import get_db
from backend.middleware.auth import get_current_user
from backend.models.user import User
from backend.models.subscription import Subscription
from backend.integrations.stripe_client import stripe_client
from backend.config import settings

logger = structlog.get_logger()
router = APIRouter()


@router.post("/create-checkout-session")
async def create_checkout_session(
    request: Request,
    db: Session = Depends(get_db)
):
    """Create Stripe checkout session"""
    try:
        # Parse request body
        body = await request.json()
        tier = body.get("tier", "premium")
        
        if tier not in ["free", "premium"]:
            raise HTTPException(status_code=400, detail="Invalid tier")
        
        # Check if Stripe is configured
        if not settings.STRIPE_SECRET_KEY or not settings.STRIPE_PRICE_ID_PREMIUM:
            logger.warning("Stripe not fully configured, returning demo response")
            return {
                "success": False,
                "error": "Payment system not configured yet. Stripe Price IDs are missing. Please contact support.",
                "demo_mode": True
            }
        
        # Try to get current user (optional for demo)
        current_user = request.session.get("user")
        if not current_user:
            # For demo purposes, allow without authentication
            return {
                "success": False,
                "error": "Please log in to upgrade your account",
                "redirect": "/auth/login"
            }
        
        # Get or create subscription record
        subscription = db.query(Subscription).filter(
            Subscription.user_id == current_user.get("id")
        ).first()
        
        if not subscription:
            subscription = Subscription(user_id=current_user.get("id"))
            db.add(subscription)
            db.commit()
            db.refresh(subscription)
        
        # Create Stripe customer if needed
        if not subscription.stripe_customer_id:
            customer_id = await stripe_client.create_customer(
                current_user.get("email"),
                current_user.get("id")
            )
            subscription.stripe_customer_id = customer_id
            db.commit()
        
        # Create checkout session
        price_id = settings.STRIPE_PRICE_ID_PREMIUM if tier == "premium" else settings.STRIPE_PRICE_ID_FREE
        
        session = await stripe_client.create_checkout_session(
            customer_id=subscription.stripe_customer_id,
            price_id=price_id,
            success_url=f"{settings.CORS_ORIGINS[0]}/dashboard?payment=success",
            cancel_url=f"{settings.CORS_ORIGINS[0]}/pricing?payment=canceled"
        )
        
        return {"success": True, "url": session.get("url")}
        
    except Exception as e:
        logger.error("Failed to create checkout session", error=str(e))
        return {
            "success": False,
            "error": "Payment system is currently unavailable. Please try again later."
        }



@router.post("/cancel-subscription")
async def cancel_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel user subscription"""
    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id
    ).first()
    
    if not subscription or not subscription.stripe_subscription_id:
        raise HTTPException(status_code=404, detail="No active subscription")
    
    success = await stripe_client.cancel_subscription(subscription.stripe_subscription_id)
    
    if success:
        subscription.cancel_at_period_end = True
        db.commit()
        return {"message": "Subscription will be canceled at period end"}
    
    raise HTTPException(status_code=500, detail="Failed to cancel subscription")


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle Stripe webhooks"""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    try:
        event = stripe_client.construct_webhook_event(payload, sig_header)
    except Exception as e:
        logger.error("Webhook verification failed", error=str(e))
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Handle events
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        await handle_checkout_completed(session, db)
    elif event["type"] == "customer.subscription.updated":
        subscription = event["data"]["object"]
        await handle_subscription_updated(subscription, db)
    elif event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        await handle_subscription_deleted(subscription, db)
    
    return {"status": "success"}


async def handle_checkout_completed(session, db: Session):
    """Handle successful checkout"""
    customer_id = session.get("customer")
    subscription_id = session.get("subscription")
    
    subscription = db.query(Subscription).filter(
        Subscription.stripe_customer_id == customer_id
    ).first()
    
    if subscription:
        subscription.stripe_subscription_id = subscription_id
        subscription.tier = "premium"
        subscription.status = "active"
        
        user = db.query(User).filter(User.id == subscription.user_id).first()
        if user:
            user.is_premium = True
        
        db.commit()
        logger.info("Checkout completed", subscription_id=subscription_id)


async def handle_subscription_updated(stripe_subscription, db: Session):
    """Handle subscription update"""
    subscription = db.query(Subscription).filter(
        Subscription.stripe_subscription_id == stripe_subscription["id"]
    ).first()
    
    if subscription:
        subscription.status = stripe_subscription["status"]
        db.commit()


async def handle_subscription_deleted(stripe_subscription, db: Session):
    """Handle subscription deletion"""
    subscription = db.query(Subscription).filter(
        Subscription.stripe_subscription_id == stripe_subscription["id"]
    ).first()
    
    if subscription:
        subscription.status = "canceled"
        subscription.tier = "free"
        
        user = db.query(User).filter(User.id == subscription.user_id).first()
        if user:
            user.is_premium = False
        
        db.commit()
        logger.info("Subscription deleted", subscription_id=stripe_subscription["id"])
