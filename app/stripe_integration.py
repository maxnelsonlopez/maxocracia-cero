"""
Módulo de Integración Stripe - Maxocracia
=========================================

Procesamiento de pagos ético para el sistema "Contribuidor Consciente".
Respeta los principios de transparencia radical, igualdad temporal y no-explotación.

Autor: Kimi (Moonshot AI)
Fecha: Febrero 2026
"""

import os
from datetime import datetime, timedelta, timezone
from functools import wraps
from typing import Dict, Optional

try:
    import stripe
except ImportError:
    stripe = None  # Opcional para testing
from flask import Blueprint, jsonify, request, current_app

from .jwt_utils import token_required
from .subscriptions import PREMIUM_TIERS, PPP_ADJUSTMENTS, get_db

# ============================================================================
# CONFIGURACIÓN STRIPE
# ============================================================================

# Inicializar Stripe con API key desde variables de entorno
if stripe:
    stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY", "")

# IDs de productos/precios de Stripe (configurar en dashboard de Stripe)
STRIPE_PRICE_IDS = {
    "contributor": os.environ.get("STRIPE_PRICE_CONTRIBUTOR", ""),
    "enterprise": os.environ.get("STRIPE_PRICE_ENTERPRISE", ""),
}

# Configuración de checkout
CHECKOUT_SUCCESS_URL = os.environ.get(
    "CHECKOUT_SUCCESS_URL", 
    "http://localhost:3000/upgrade?success=true"
)
CHECKOUT_CANCEL_URL = os.environ.get(
    "CHECKOUT_CANCEL_URL",
    "http://localhost:3000/upgrade?canceled=true"
)


stripe_bp = Blueprint("stripe", __name__, url_prefix="/stripe")


# ============================================================================
# DECORADORES Y UTILIDADES
# ============================================================================

def stripe_configured(f):
    """
    Decorador que verifica si Stripe está configurado.
    
    Autor: Kimi
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if not stripe or not stripe.api_key:
            return jsonify({
                "error": "stripe_not_configured",
                "message": "Integración con Stripe no configurada",
                "setup_required": [
                    "Crear cuenta en https://stripe.com",
                    "Obtener STRIPE_SECRET_KEY de dashboard",
                    "Configurar STRIPE_PUBLISHABLE_KEY",
                    "Agregar variables al archivo .env"
                ]
            }), 503
        return f(*args, **kwargs)
    return decorated


def get_or_create_stripe_customer(user_id: int, email: str, name: str) -> str:
    """
    Obtiene o crea un cliente de Stripe para el usuario.
    
    Args:
        user_id: ID del usuario local
        email: Email del usuario
        name: Nombre del usuario
        
    Returns:
        ID del cliente de Stripe
        
    Autor: Kimi
    """
    db = get_db()
    
    # Buscar si ya tiene customer_id
    result = db.execute(
        "SELECT external_customer_id FROM subscriptions WHERE user_id = ?",
        (user_id,)
    ).fetchone()
    
    if result and result["external_customer_id"]:
        # Verificar que el cliente exista en Stripe
        try:
            customer = stripe.Customer.retrieve(result["external_customer_id"])
            if customer and not customer.get("deleted", False):
                return result["external_customer_id"]
        except stripe.error.InvalidRequestError:
            # Cliente no existe, crear nuevo
            pass
    
    # Crear nuevo cliente en Stripe
    customer = stripe.Customer.create(
        email=email,
        name=name,
        metadata={
            "user_id": str(user_id),
            "platform": "maxocracia"
        }
    )
    
    return customer.id


def calculate_ppp_adjustment(country_code: str) -> float:
    """
    Calcula el factor de ajuste por PPP.
    
    Principio T2: Igualdad Temporal Fundamental
    El tiempo de cada persona vale igual.
    
    Autor: Kimi
    """
    return PPP_ADJUSTMENTS.get(country_code.upper(), PPP_ADJUSTMENTS["DEFAULT"])


# ============================================================================
# ENDPOINTS API
# ============================================================================

@stripe_bp.route("/config", methods=["GET"])
def get_stripe_config():
    """
    Configuración pública de Stripe para el frontend.
    
    Retorna la publishable key (safe para frontend) y estado de configuración.
    
    Autor: Kimi
    """
    return jsonify({
        "publishable_key": STRIPE_PUBLISHABLE_KEY,
        "stripe_configured": bool(stripe.api_key and STRIPE_PUBLISHABLE_KEY),
        "prices_configured": {
            tier: bool(price_id)
            for tier, price_id in STRIPE_PRICE_IDS.items()
        },
        "principles": {
            "transparency": "Los precios reflejan costo real + PPP",
            "privacy": "Stripe procesa pagos, nosotros no guardamos tarjetas",
            "control": "Cancelación libre en cualquier momento"
        }
    })


@stripe_bp.route("/create-checkout-session", methods=["POST"])
@token_required
@stripe_configured
def create_checkout_session(current_user):
    """
    Crea una sesión de checkout de Stripe.
    
    Request JSON:
        {
            "tier": "contributor" | "enterprise",
            "country_code": "CO",  # Para ajuste PPP
            "success_url": "...",  # Opcional, override
            "cancel_url": "..."    # Opcional, override
        }
    
    Response:
        {
            "session_id": "cs_...",
            "url": "https://checkout.stripe.com/..."
        }
    
    Autor: Kimi
    """
    data = request.get_json() or {}
    tier = data.get("tier", "contributor")
    country_code = data.get("country_code", "DEFAULT")
    
    # Validar tier
    if tier not in ["contributor", "enterprise"]:
        return jsonify({
            "error": "invalid_tier",
            "message": "Tier debe ser 'contributor' o 'enterprise'"
        }), 400
    
    # Verificar que tenemos price_id configurado
    price_id = STRIPE_PRICE_IDS.get(tier)
    if not price_id:
        return jsonify({
            "error": "price_not_configured",
            "message": f"Precio de Stripe no configurado para tier '{tier}'",
            "setup_instruction": f"Crear precio en dashboard de Stripe y configurar STRIPE_PRICE_{tier.upper()}"
        }), 503
    
    try:
        # Obtener o crear cliente de Stripe
        customer_id = get_or_create_stripe_customer(
            current_user["user_id"],
            current_user.get("email", ""),
            current_user.get("name", "")
        )
        
        # Calcular ajuste PPP para metadata
        ppp_factor = calculate_ppp_adjustment(country_code)
        base_price = PREMIUM_TIERS[tier]["price_usd"]
        adjusted_price = round(base_price * ppp_factor, 2)
        
        # Crear sesión de checkout
        checkout_session = stripe.checkout.Session.create(
            customer=customer_id,
            payment_method_types=["card"],
            line_items=[{
                "price": price_id,
                "quantity": 1,
            }],
            mode="subscription",
            success_url=data.get("success_url", CHECKOUT_SUCCESS_URL),
            cancel_url=data.get("cancel_url", CHECKOUT_CANCEL_URL),
            metadata={
                "user_id": str(current_user["user_id"]),
                "tier": tier,
                "country_code": country_code,
                "ppp_factor": str(ppp_factor),
                "adjusted_price_usd": str(adjusted_price),
                "platform": "maxocracia"
            },
            subscription_data={
                "metadata": {
                    "user_id": str(current_user["user_id"]),
                    "tier": tier,
                }
            },
            # Permitir código de descuento (honor system)
            allow_promotion_codes=True,
            # Información de impuestos automática
            automatic_tax={"enabled": True},
            # Mensaje de confirmación ético
            custom_text={
                "submit": {
                    "message": "Gracias por contribuir a la sostenibilidad de Maxocracia. Tu apoyo respeta el principio de Igualdad Temporal."
                }
            }
        )
        
        # Log de transparencia
        current_app.logger.info(
            f"[STRIPE] Checkout creado: user_id={current_user['user_id']}, "
            f"tier={tier}, ppp_factor={ppp_factor}, session={checkout_session.id}"
        )
        
        return jsonify({
            "session_id": checkout_session.id,
            "url": checkout_session.url,
            "tier": tier,
            "ppp_adjustment": {
                "factor": ppp_factor,
                "base_price": base_price,
                "adjusted_price": adjusted_price,
                "country": country_code
            }
        })
        
    except stripe.error.StripeError as e:
        current_app.logger.error(f"[STRIPE ERROR] {str(e)}")
        return jsonify({
            "error": "stripe_error",
            "message": str(e)
        }), 400


@stripe_bp.route("/customer-portal", methods=["POST"])
@token_required
@stripe_configured
def create_customer_portal(current_user):
    """
    Crea una sesión del portal de cliente de Stripe.
    
    Permite al usuario gestionar su suscripción:
    - Actualizar método de pago
    - Cancelar suscripción
    - Ver historial de facturas
    
    Autor: Kimi
    """
    db = get_db()
    
    # Buscar customer_id del usuario
    result = db.execute(
        "SELECT external_customer_id FROM subscriptions WHERE user_id = ?",
        (current_user["user_id"],)
    ).fetchone()
    
    if not result or not result["external_customer_id"]:
        return jsonify({
            "error": "no_subscription",
            "message": "No tienes una suscripción activa para gestionar"
        }), 404
    
    try:
        session = stripe.billing_portal.Session.create(
            customer=result["external_customer_id"],
            return_url=data.get("return_url", "http://localhost:3000/account"),
            # Configuración del portal
            configuration={
                "features": {
                    "payment_method_update": {"enabled": True},
                    "subscription_cancel": {
                        "enabled": True,
                        "mode": "at_period_end",  # Cancelar al final del período
                        "cancellation_reason": {
                            "enabled": True,
                            "options": [
                                "too_expensive",
                                "missing_features",
                                "switched_service",
                                "unused",
                                "other"
                            ]
                        }
                    },
                    "subscription_update": {
                        "enabled": True,
                        "default_allowed_updates": ["price"],
                        "products": [
                            {
                                "product": os.environ.get("STRIPE_PRODUCT_CONTRIBUTOR", ""),
                                "prices": [os.environ.get("STRIPE_PRICE_CONTRIBUTOR", "")]
                            },
                            {
                                "product": os.environ.get("STRIPE_PRODUCT_ENTERPRISE", ""),
                                "prices": [os.environ.get("STRIPE_PRICE_ENTERPRISE", "")]
                            }
                        ]
                    },
                    "invoice_history": {"enabled": True}
                },
                "business_profile": {
                    "headline": "Gestiona tu contribución a Maxocracia",
                    "privacy_policy_url": "http://localhost:3000/privacy",
                    "terms_of_service_url": "http://localhost:3000/terms"
                }
            }
        )
        
        return jsonify({
            "url": session.url,
            "message": "Redirigiendo al portal de gestión de suscripción"
        })
        
    except stripe.error.StripeError as e:
        current_app.logger.error(f"[STRIPE ERROR] {str(e)}")
        return jsonify({
            "error": "stripe_error",
            "message": str(e)
        }), 400


@stripe_bp.route("/webhook", methods=["POST"])
def stripe_webhook():
    """
    Webhook para procesar eventos de Stripe.
    
    Eventos manejados:
    - checkout.session.completed: Suscripción nueva
    - invoice.payment_succeeded: Pago recurrente exitoso
    - invoice.payment_failed: Pago fallido
    - customer.subscription.deleted: Suscripción cancelada
    
    Autor: Kimi
    """
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature", "")
    
    # Verificar firma del webhook
    if STRIPE_WEBHOOK_SECRET:
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            # Payload inválido
            return jsonify({"error": "invalid_payload"}), 400
        except stripe.error.SignatureVerificationError:
            # Firma inválida
            return jsonify({"error": "invalid_signature"}), 400
    else:
        # Sin webhook secret, parsear manualmente (solo desarrollo)
        try:
            event = stripe.Event.construct_from(
                request.get_json(), stripe.api_key
            )
        except ValueError:
            return jsonify({"error": "invalid_payload"}), 400
    
    # Procesar evento
    event_type = event["type"]
    data_object = event["data"]["object"]
    
    current_app.logger.info(f"[STRIPE WEBHOOK] Evento recibido: {event_type}")
    
    try:
        if event_type == "checkout.session.completed":
            _handle_checkout_completed(data_object)
        elif event_type == "invoice.payment_succeeded":
            _handle_payment_succeeded(data_object)
        elif event_type == "invoice.payment_failed":
            _handle_payment_failed(data_object)
        elif event_type == "customer.subscription.deleted":
            _handle_subscription_deleted(data_object)
        elif event_type == "customer.subscription.updated":
            _handle_subscription_updated(data_object)
        else:
            current_app.logger.info(f"[STRIPE WEBHOOK] Evento no manejado: {event_type}")
            
    except Exception as e:
        current_app.logger.error(f"[STRIPE WEBHOOK ERROR] {str(e)}")
        # Retornar 200 para que Stripe no reintente
        # pero loggear el error para revisión manual
    
    return jsonify({"status": "success"}), 200


def _handle_checkout_completed(session: Dict):
    """
    Maneja el evento checkout.session.completed.
    
    Crea/actualiza la suscripción en nuestra base de datos.
    
    Autor: Kimi
    """
    metadata = session.get("metadata", {})
    user_id = int(metadata.get("user_id", 0))
    tier = metadata.get("tier", "contributor")
    customer_id = session.get("customer")
    subscription_id = session.get("subscription")
    
    if not user_id:
        current_app.logger.error("[STRIPE WEBHOOK] checkout.session sin user_id")
        return
    
    # Obtener detalles de la suscripción de Stripe
    stripe_sub = stripe.Subscription.retrieve(subscription_id)
    
    # Calcular fecha de expiración (current_period_end)
    expires_at = datetime.fromtimestamp(
        stripe_sub.current_period_end, tz=timezone.utc
    ).isoformat()
    
    db = get_db()
    
    # Insertar o actualizar suscripción
    db.execute(
        """
        INSERT INTO subscriptions 
        (user_id, tier, status, started_at, expires_at, payment_method, 
         external_customer_id, external_subscription_id, notes)
        VALUES (?, ?, 'active', datetime('now'), ?, 'stripe', ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            tier = excluded.tier,
            status = 'active',
            expires_at = excluded.expires_at,
            payment_method = 'stripe',
            external_customer_id = excluded.external_customer_id,
            external_subscription_id = excluded.external_subscription_id,
            notes = excluded.notes
        """,
        (
            user_id, tier, expires_at, customer_id, subscription_id,
            f"Created via Stripe checkout. PPP factor: {metadata.get('ppp_factor', 'N/A')}"
        )
    )
    db.commit()
    
    # Log de transparencia
    current_app.logger.info(
        f"[TRANSPARENCIA] Nueva suscripción Stripe: user_id={user_id}, "
        f"tier={tier}, customer={customer_id}"
    )


def _handle_payment_succeeded(invoice: Dict):
    """
    Maneja pagos recurrentes exitosos.
    
    Autor: Kimi
    """
    subscription_id = invoice.get("subscription")
    
    if not subscription_id:
        return
    
    # Buscar suscripción en nuestra BD
    db = get_db()
    sub = db.execute(
        "SELECT user_id, tier FROM subscriptions WHERE external_subscription_id = ?",
        (subscription_id,)
    ).fetchone()
    
    if not sub:
        return
    
    # Actualizar fecha de expiración
    stripe_sub = stripe.Subscription.retrieve(subscription_id)
    expires_at = datetime.fromtimestamp(
        stripe_sub.current_period_end, tz=timezone.utc
    ).isoformat()
    
    db.execute(
        "UPDATE subscriptions SET expires_at = ?, status = 'active' WHERE external_subscription_id = ?",
        (expires_at, subscription_id)
    )
    db.commit()
    
    current_app.logger.info(
        f"[TRANSPARENCIA] Pago recurrente exitoso: user_id={sub['user_id']}, "
        f"amount={invoice.get('amount_paid')}"
    )


def _handle_payment_failed(invoice: Dict):
    """
    Maneja pagos fallidos.
    
    Autor: Kimi
    """
    subscription_id = invoice.get("subscription")
    
    if not subscription_id:
        return
    
    current_app.logger.warning(
        f"[STRIPE WEBHOOK] Pago fallido: subscription={subscription_id}, "
        f"attempt_count={invoice.get('attempt_count')}"
    )
    
    # No cancelamos inmediatamente, Stripe reintentará automáticamente
    # Podríamos notificar al usuario aquí


def _handle_subscription_deleted(subscription: Dict):
    """
    Maneja cancelaciones de suscripción.
    
    Autor: Kimi
    """
    subscription_id = subscription.get("id")
    
    db = get_db()
    sub = db.execute(
        "SELECT user_id, tier FROM subscriptions WHERE external_subscription_id = ?",
        (subscription_id,)
    ).fetchone()
    
    if not sub:
        return
    
    # Marcar como cancelada
    db.execute(
        "UPDATE subscriptions SET status = 'cancelled' WHERE external_subscription_id = ?",
        (subscription_id,)
    )
    db.commit()
    
    current_app.logger.info(
        f"[TRANSPARENCIA] Suscripción cancelada: user_id={sub['user_id']}, "
        f"tier={sub['tier']}"
    )


def _handle_subscription_updated(subscription: Dict):
    """
    Maneja actualizaciones de suscripción (upgrade/downgrade).
    
    Autor: Kimi
    """
    subscription_id = subscription.get("id")
    status = subscription.get("status")
    
    db = get_db()
    
    # Mapear estado de Stripe a nuestros estados
    status_map = {
        "active": "active",
        "canceled": "cancelled",
        "incomplete": "expired",
        "incomplete_expired": "expired",
        "past_due": "active",  # Aún activa, intentando cobrar
        "trialing": "active",
        "unpaid": "expired"
    }
    
    our_status = status_map.get(status, "expired")
    
    # Actualizar fecha de expiración
    expires_at = datetime.fromtimestamp(
        subscription.get("current_period_end", 0), tz=timezone.utc
    ).isoformat()
    
    db.execute(
        """
        UPDATE subscriptions 
        SET status = ?, expires_at = ?
        WHERE external_subscription_id = ?
        """,
        (our_status, expires_at, subscription_id)
    )
    db.commit()


# ============================================================================
# ENDPOINTS AUXILIARES
# ============================================================================

@stripe_bp.route("/subscription-status", methods=["GET"])
@token_required
@stripe_configured
def get_stripe_subscription_status(current_user):
    """
    Obtiene el estado actual de la suscripción desde Stripe.
    
    Útil para sincronización manual o debugging.
    
    Autor: Kimi
    """
    db = get_db()
    
    result = db.execute(
        """
        SELECT external_subscription_id, external_customer_id 
        FROM subscriptions 
        WHERE user_id = ?
        """,
        (current_user["user_id"],)
    ).fetchone()
    
    if not result or not result["external_subscription_id"]:
        return jsonify({
            "has_stripe_subscription": False,
            "message": "No hay suscripción de Stripe asociada"
        })
    
    try:
        stripe_sub = stripe.Subscription.retrieve(
            result["external_subscription_id"],
            expand=["latest_invoice.payment_intent"]
        )
        
        return jsonify({
            "has_stripe_subscription": True,
            "stripe_status": stripe_sub.status,
            "current_period_start": datetime.fromtimestamp(
                stripe_sub.current_period_start, tz=timezone.utc
            ).isoformat(),
            "current_period_end": datetime.fromtimestamp(
                stripe_sub.current_period_end, tz=timezone.utc
            ).isoformat(),
            "cancel_at_period_end": stripe_sub.cancel_at_period_end,
            "plan": {
                "id": stripe_sub.plan.id if hasattr(stripe_sub, 'plan') else None,
                "amount": stripe_sub.plan.amount if hasattr(stripe_sub, 'plan') else None,
                "currency": stripe_sub.plan.currency if hasattr(stripe_sub, 'plan') else None,
            }
        })
        
    except stripe.error.StripeError as e:
        return jsonify({
            "error": "stripe_error",
            "message": str(e)
        }), 400
