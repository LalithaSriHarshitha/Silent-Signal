"""Stripe payment client"""
import stripe
from typing import Dict, Any
import structlog

from backend.config import settings

logger = structlog.get_logger()

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeClient:
    """Stripe payment processing client"""
    
    @staticmethod
    async def create_customer(email: str, user_id: int) -> str:
        """Create Stripe customer"""
        try:
            customer = stripe.Customer.create(
                email=email,
                metadata={"user_id": user_id}
            )
            logger.info("Stripe customer created", customer_id=customer.id)
            return customer.id
        except Exception as e:
            logger.error("Customer creation failed", error=str(e))
            raise
    
    @staticmethod
    async def create_checkout_session(
        customer_id: str,
        price_id: str,
        success_url: str,
        cancel_url: str
    ) -> Dict[str, Any]:
        """Create Stripe checkout session"""
        try:
            session = stripe.checkout.Session.create(
                customer=customer_id,
                payment_method_types=["card"],
                line_items=[{"price": price_id, "quantity": 1}],
                mode="subscription",
                success_url=success_url,
                cancel_url=cancel_url,
            )
            logger.info("Checkout session created", session_id=session.id)
            return {"session_id": session.id, "url": session.url}
        except Exception as e:
            logger.error("Checkout session creation failed", error=str(e))
            raise

    
    @staticmethod
    async def cancel_subscription(subscription_id: str) -> bool:
        """Cancel Stripe subscription"""
        try:
            stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=True
            )
            logger.info("Subscription canceled", subscription_id=subscription_id)
            return True
        except Exception as e:
            logger.error("Subscription cancellation failed", error=str(e))
            return False
    
    @staticmethod
    def construct_webhook_event(payload: bytes, sig_header: str):
        """Construct and verify webhook event"""
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
            return event
        except Exception as e:
            logger.error("Webhook verification failed", error=str(e))
            raise


stripe_client = StripeClient()
