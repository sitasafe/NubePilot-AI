import os

import stripe

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def crear_suscripcion(customer_email, plan_id):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": plan_id, "quantity": 1}],
        mode="subscription",
        success_url="https://flowmerce.com/success",
        cancel_url="https://flowmerce.com/cancel",
        customer_email=customer_email,
    )
    return session.url
