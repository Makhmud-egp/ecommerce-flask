import stripe
from flask import current_app


class PaymentService:

    @staticmethod
    def create_payment_intent(amount, currency='usd'):
        """Create Stripe payment intent"""
        stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

        if not stripe.api_key:
            raise RuntimeError("Stripe secret key is missing")

        try:
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Convert to cents
                currency=currency,
                automatic_payment_methods={'enabled': True}
            )
            return intent

        except Exception as e:
            current_app.logger.error(f"Stripe error: {e}")
            return None

    @staticmethod
    def get_payment_intent(payment_intent_id):
        """Get payment intent details"""
        stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

        try:
            return stripe.PaymentIntent.retrieve(payment_intent_id)
        except Exception as e:
            return None