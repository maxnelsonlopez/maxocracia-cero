"""
Módulo de Suscripciones Premium - Maxocracia
=============================================

Sistema de membresías "Contribuidor Consciente" que respeta:
- Transparencia radical (todos los flujos son públicos)
- Igualdad del tiempo (precios ajustables por contexto)
- No-explotación (honor system, sin coerción)

Autor: Kimi (Moonshot AI)
Fecha: Febrero 2026
"""

from datetime import datetime, timedelta, timezone
from functools import wraps
from typing import Dict, List, Optional

from flask import Blueprint, jsonify, request, current_app

from .jwt_utils import token_required, verify_token
from .utils import get_db

# Blueprint de suscripciones
subscriptions_bp = Blueprint("subscriptions", __name__, url_prefix="/subscriptions")


# ============================================================================
# CONFIGURACIÓN DE TIER PREMIUM
# ============================================================================

PREMIUM_TIERS = {
    "free": {
        "price_usd": 0,
        "benefits": [
            "acceso_libro_completo",
            "calculadora_vhv_basica",
            "nexus_simulator_limitado",
            "github_discussions"
        ],
        "limits": {
            "vhv_calculations_per_day": 10,
            "support_response_hours": None,  # Sin soporte
        }
    },
    "contributor": {
        "price_usd": 25,  # Precio base
        "benefits": [
            "dashboard_avanzado",
            "soporte_prioritario",
            "acceso_anticipado",
            "badge_contribuidor",
            "sesiones_grupales_mensuales",
            "api_rate_limit_aumentado"
        ],
        "limits": {
            "vhv_calculations_per_day": 1000,
            "support_response_hours": 24,
        },
        "principles": {
            "price_transparent": True,
            "cost_based": True,
            "sliding_scale": True,
        }
    },
    "enterprise": {
        "price_usd": 200,  # Para organizaciones
        "benefits": [
            "todas_las_benefits_contributor",
            "consultoria_implementacion",
            "auditoria_vhv_personalizada",
            "white_label_maxocontracts",
            "soporte_dedicado"
        ],
        "limits": {
            "vhv_calculations_per_day": -1,  # Ilimitado
            "support_response_hours": 4,
        }
    }
}

# Ajustes por paridad de poder adquisitivo (PPP)
# Basado en principio T2: Igualdad Temporal Fundamental
# El tiempo de cada persona vale igual, por tanto el precio debe ajustarse
# al poder adquisitivo local.
PPP_ADJUSTMENTS = {
    "CO": 0.35,   # Colombia - 35% del costo US
    "AR": 0.25,   # Argentina
    "VE": 0.15,   # Venezuela
    "MX": 0.45,   # México
    "BR": 0.40,   # Brasil
    "PE": 0.35,   # Perú
    "CL": 0.50,   # Chile
    "US": 1.00,   # Estados Unidos
    "CA": 1.00,   # Canadá
    "GB": 0.95,   # Reino Unido
    "DE": 0.90,   # Alemania
    "ES": 0.70,   # España
    "FR": 0.90,   # Francia
    "DEFAULT": 0.60  # Resto del mundo
}

# Métodos de Pago Soportados
PAYMENT_METHODS = {
    "github_sponsors": "GitHub Sponsors (Recomendado Internacional)",
    "wompi": "Wompi (PSE/Nequi/Bancolombia - Colombia)",
    "crypto_usdc": "USDC (Polygon/Ethereum)",
    "crypto_usdt": "USDT (Polygon/Ethereum)",
    "manual_transfer": "Transferencia Manual / Honor System",
    "stripe": "Stripe (Solo internacional)"
}


# ============================================================================
# DECORADORES DE AUTORIZACIÓN
# ============================================================================

def premium_required(min_tier: str = "contributor"):
    """
    Decorador que requiere suscripción premium activa.
    
    Args:
        min_tier: Tier mínimo requerido ('contributor' o 'enterprise')
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth = request.headers.get("Authorization", "")
            if not auth.startswith("Bearer "):
                return jsonify({
                    "error": "authorization_required",
                    "message": "Se requiere autenticación"
                }), 401
            
            token = auth.split(" ", 1)[1]
            data = verify_token(token)
            
            if data is None:
                return jsonify({
                    "error": "invalid_token",
                    "message": "Token inválido o expirado"
                }), 401
            
            # Verificar suscripción activa
            db = get_db()
            sub = db.execute(
                """
                SELECT tier, status, expires_at 
                FROM subscriptions 
                WHERE user_id = ? 
                AND status = 'active' 
                AND (expires_at IS NULL OR expires_at > datetime('now'))
                """,
                (data.get("user_id"),)
            ).fetchone()
            
            tier_order = {"free": 0, "contributor": 1, "enterprise": 2}
            required_level = tier_order.get(min_tier, 1)
            
            if not sub or tier_order.get(sub["tier"], 0) < required_level:
                return jsonify({
                    "error": "premium_required",
                    "message": f"Esta función requiere ser '{min_tier}' o superior",
                    "current_tier": sub["tier"] if sub else "free",
                    "upgrade_url": "/subscriptions/upgrade",
                    "principles": {
                        "transparency": "Los precios reflejan costo real",
                        "equity": "Ajustamos por poder adquisitivo local",
                        "no_exploitation": "Sin dark patterns ni coerción"
                    }
                }), 403
            
            # Adjuntar info de suscripción al request
            request.user = data
            request.user_tier = sub["tier"]
            request.subscription = dict(sub)
            
            return f(*args, **kwargs)
        return decorated
    return decorator


# ============================================================================
# ENDPOINTS API
# ============================================================================

@subscriptions_bp.route("/config", methods=["GET"])
def get_config():
    """
    Configuración pública de tiers y precios.
    
    Principio: Transparencia Radical
    Todos los precios y beneficios son públicos.
    """
    return jsonify({
        "tiers": PREMIUM_TIERS,
        "principles": {
            "price_based_on_cost": True,
            "sliding_scale_available": True,
            "all_transactions_public": True,
            "no_data_selling": True,
            "honor_system": True,
            "cancel_anytime": True
        },
        "currency": "USD",
        "axioms": ["T2", "T7", "T9", "T13"],
        "last_updated": datetime.now(timezone.utc).isoformat()
    })


@subscriptions_bp.route("/calculate-fair-price", methods=["POST"])
def calculate_fair_price():
    """
    Calcula precio justo basado en contexto económico.
    
    Basado en Axioma T2: Igualdad Temporal Fundamental.
    El tiempo de cada persona vale igual, por tanto el precio
    debe ajustarse al poder adquisitivo local.
    
    Request JSON:
        {
            "country_code": "CO",  # ISO 3166-1 alpha-2
            "hourly_rate_usd": 5.5,  # Opcional, honor system
            "reported_monthly_income_usd": 800  # Opcional
        }
    
    Response:
        {
            "base_price": 25.0,
            "adjusted_price": 8.75,
            "adjustment_factor": 0.35,
            "country": "CO",
            "justification": "Ajustado por PPP (Paridad de Poder Adquisitivo)",
            "honor_system": true,
            "manual_override_allowed": true
        }
    """
    data = request.get_json() or {}
    country = data.get("country_code", "DEFAULT").upper()
    hourly_rate = data.get("hourly_rate_usd")
    monthly_income = data.get("reported_monthly_income_usd")
    
    base_price = PREMIUM_TIERS["contributor"]["price_usd"]
    
    # Ajuste por PPP
    adjustment = PPP_ADJUSTMENTS.get(country, PPP_ADJUSTMENTS["DEFAULT"])
    adjusted_price = base_price * adjustment
    
    # Ajuste adicional por ingreso reportado (honor system)
    income_adjustment = 1.0
    if monthly_income:
        if monthly_income < 500:
            income_adjustment = 0.5  # 50% descuento adicional
        elif monthly_income < 1000:
            income_adjustment = 0.7
        elif monthly_income > 5000:
            income_adjustment = 1.2  # Puede pagar más
    
    final_price = adjusted_price * income_adjustment
    
    return jsonify({
        "base_price": base_price,
        "adjusted_price": round(final_price, 2),
        "adjustment_factor": adjustment,
        "income_adjustment": income_adjustment,
        "country": country,
        "justification": (
            "Precio ajustado por Paridad de Poder Adquisitivo (PPP). "
            "Respetamos el principio de que el tiempo de cada persona vale igual, "
            "por tanto el costo debe representar la misma proporción del tiempo "
            "vital independientemente de la ubicación geográfica."
        ),
        "honor_system": True,
        "manual_override_allowed": True,
        "suggested_message": (
            "Paga lo que puedas justificar éticamente. "
            "Si el precio ajustado representa una carga excesiva, "
            "contactanos y encontraremos una solución."
        )
    })


@subscriptions_bp.route("/my-subscription", methods=["GET"])
@token_required
def get_my_subscription(current_user):
    """
    Obtiene el estado de suscripción del usuario autenticado.
    """
    db = get_db()
    
    # Buscar suscripción activa
    sub = db.execute(
        """
        SELECT 
            s.id, s.tier, s.status, s.started_at, s.expires_at,
            s.payment_method, s.external_customer_id
        FROM subscriptions s
        WHERE s.user_id = ?
        ORDER BY s.started_at DESC
        LIMIT 1
        """,
        (current_user["user_id"],)
    ).fetchone()
    
    if not sub:
        return jsonify({
            "tier": "free",
            "status": "active",
            "benefits": PREMIUM_TIERS["free"]["benefits"],
            "limits": PREMIUM_TIERS["free"]["limits"],
            "upgrade_available": True
        })
    
    sub_dict = dict(sub)
    tier = sub_dict.get("tier", "free")
    
    return jsonify({
        **sub_dict,
        "benefits": PREMIUM_TIERS.get(tier, {}).get("benefits", []),
        "limits": PREMIUM_TIERS.get(tier, {}).get("limits", {}),
        "days_until_expiry": (
            (datetime.fromisoformat(sub_dict["expires_at"].replace("Z", "+00:00")) - 
             datetime.now(timezone.utc)).days
            if sub_dict.get("expires_at") else None
        )
    })


@subscriptions_bp.route("/transparency-report", methods=["GET"])
def transparency_report():
    """
    Reporte público de todos los ingresos.
    
    Principio: Transparencia Radical (Axioma T13)
    Todos los flujos financieros son públicos y auditables.
    """
    db = get_db()
    
    # Estadísticas de suscripciones (anónimas)
    stats = db.execute(
        """
        SELECT 
            tier,
            COUNT(*) as count,
            strftime('%Y-%m', started_at) as month
        FROM subscriptions
        WHERE status = 'active'
        GROUP BY tier, month
        ORDER BY month DESC
        """
    ).fetchall()
    
    # Calcular ingresos estimados
    revenue_by_month = {}
    for row in stats:
        month = row["month"]
        tier = row["tier"]
        count = row["count"]
        price = PREMIUM_TIERS.get(tier, {}).get("price_usd", 0)
        
        if month not in revenue_by_month:
            revenue_by_month[month] = 0
        revenue_by_month[month] += count * price
    
    # Costos operativos (estimados, deberían ser actualizados mensualmente)
    operational_costs = {
        "hosting_servers": 50,
        "database": 20,
        "bandwidth": 30,
        "development_volunteer": 0,  # Voluntario por ahora
        "legal_accounting": 0,
        "total_monthly_usd": 100
    }
    
    return jsonify({
        "report_type": "transparency_radical",
        "principles": [
            "All financial flows are public",
            "No hidden costs",
            "No profit maximization",
            "Surplus reinvested in open source"
        ],
        "subscription_stats": [dict(row) for row in stats],
        "estimated_revenue_by_month": revenue_by_month,
        "operational_costs": operational_costs,
        "surplus_strategy": (
            "Excedentes reinvertidos en: (1) Reducir precios para países "
            "de bajo ingreso, (2) Desarrollar funcionalidades open source, "
            "(3) Financiar Cohortes Cero en nuevas regiones."
        ),
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "auditable": True,
        "blockchain_anchor": None  # TODO: Integrar con blockchain para inmutabilidad
    })


@subscriptions_bp.route("/webhook/github", methods=["POST"])
def github_webhook():
    """
    Webhook para GitHub Sponsors.
    Activa suscripciones basadas en el evento de 'sponsorship'.
    """
    # TODO: Validar firma de GitHub (X-Hub-Signature-256)
    data = request.get_json() or {}
    action = data.get("action")
    
    if action in ["created", "tier_changed"]:
        # Lógica de activación basada en el email o username de GitHub
        pass
        
    return jsonify({"status": "received", "source": "github"}), 200

@subscriptions_bp.route("/webhook/wompi", methods=["POST"])
def wompi_webhook():
    """
    Webhook para Wompi (Colombia).
    Maneja pagos locales por PSE, Nequi, etc.
    """
    # TODO: Validar firma de Wompi
    data = request.get_json() or {}
    # Wompi envía evento en data.event
    event_type = data.get("event")
    
    if event_type == "transaction.updated":
        transaction = data.get("data", {}).get("transaction", {})
        if transaction.get("status") == "APPROVED":
            # Activar suscripción
            pass
            
    return jsonify({"status": "received", "source": "wompi"}), 200

@subscriptions_bp.route("/register-crypto", methods=["POST"])
@token_required
def register_crypto(current_user):
    """
    Registra una transacción cripto para validación posterior.
    Fomenta la soberanía digital del Reino Sintético.
    """
    data = request.get_json() or {}
    tx_hash = data.get("tx_hash")
    network = data.get("network", "polygon")
    
    if not tx_hash:
        return jsonify({"error": "tx_hash_required"}), 400
        
    db = get_db()
    # Guardamos la intención de pago para validación manual/automática
    db.execute(
        "UPDATE subscriptions SET notes = ?, payment_method = 'crypto' WHERE user_id = ?",
        (f"TX: {tx_hash} ({network})", current_user["user_id"])
    )
    db.commit()
    
    return jsonify({
        "status": "pending_verification",
        "message": "Transacción registrada. Un oráculo validará el hash pronto.",
        "tx_hash": tx_hash
    })


@subscriptions_bp.route("/activate-manual", methods=["POST"])
@token_required
def activate_manual(current_user):
    """
    Activación manual de suscripción (para pagos fuera de plataforma).
    
    Casos de uso:
    - Transferencias bancarias directas
    - Pagos en efectivo (registrados por administrador)
    - Criptomonedas
    - Trueque documentado
    
    Solo administradores pueden activar manualmente.
    """
    # Verificar que sea admin
    if not current_user.get("is_admin"):
        return jsonify({
            "error": "admin_required",
            "message": "Solo administradores pueden activar suscripciones manualmente"
        }), 403
    
    data = request.get_json() or {}
    user_id = data.get("user_id")
    tier = data.get("tier", "contributor")
    months = data.get("months", 1)
    payment_method = data.get("payment_method", "manual_transfer")
    notes = data.get("notes", "")
    
    if not user_id:
        return jsonify({"error": "user_id_required"}), 400
    
    db = get_db()
    
    # Calcular fecha de expiración
    expires_at = (datetime.now(timezone.utc) + timedelta(days=30*months)).isoformat()
    
    # Insertar o actualizar suscripción
    db.execute(
        """
        INSERT INTO subscriptions 
        (user_id, tier, status, started_at, expires_at, payment_method, notes)
        VALUES (?, ?, 'active', datetime('now'), ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            tier = excluded.tier,
            status = 'active',
            expires_at = excluded.expires_at,
            payment_method = excluded.payment_method,
            notes = excluded.notes
        """,
        (user_id, tier, expires_at, payment_method, notes)
    )
    db.commit()
    
    # Log de transparencia (sin datos personales)
    current_app.logger.info(
        f"[TRANSPARENCIA] Suscripción manual activada: tier={tier}, "
        f"months={months}, method={payment_method}"
    )
    
    return jsonify({
        "status": "success",
        "message": f"Suscripción {tier} activada por {months} mes(es)",
        "expires_at": expires_at,
        "principle": "Transparencia Radical - Esta acción es visible en el reporte público"
    })


# ============================================================================
# ENDPOINTS DE ADMINISTRACIÓN (Next.js Dashboard support)
# ============================================================================

@subscriptions_bp.route("/admin/users", methods=["GET"])
@token_required
def admin_list_users(current_user):
    """
    Lista todos los usuarios con su estado de suscripción actual.
    Solo para administradores.
    """
    if not current_user.get("is_admin"):
        return jsonify({"error": "admin_required"}), 403
        
    db = get_db()
    users = db.execute(
        """
        SELECT 
            u.id, u.email, u.name, u.alias,
            s.tier, s.status as sub_status, s.expires_at, s.payment_method
        FROM users u
        LEFT JOIN subscriptions s ON u.id = s.user_id
        ORDER BY u.created_at DESC
        """
    ).fetchall()
    
    return jsonify([dict(u) for u in users])


@subscriptions_bp.route("/admin/stats", methods=["GET"])
@token_required
def admin_stats(current_user):
    """
    Estadísticas globales de suscripciones para el Dashboard.
    """
    if not current_user.get("is_admin"):
        return jsonify({"error": "admin_required"}), 403
        
    db = get_db()
    
    # Total de usuarios
    total_users = db.execute("SELECT COUNT(*) as count FROM users").fetchone()["count"]
    
    # Contribuidores activos por tier
    tiers_count = db.execute(
        """
        SELECT tier, COUNT(*) as count 
        FROM subscriptions 
        WHERE status = 'active' 
        AND (expires_at IS NULL OR expires_at > datetime('now'))
        GROUP BY tier
        """
    ).fetchall()
    
    # Ingresos mensuales base (estimados por tier)
    mrr = 0
    for row in tiers_count:
        price = PREMIUM_TIERS.get(row["tier"], {}).get("price_usd", 0)
        mrr += row["count"] * price
        
    return jsonify({
        "total_users": total_users,
        "active_contributors": sum(row["count"] for row in tiers_count),
        "mrr_usd_estimated": mrr,
        "tiers_breakdown": [dict(row) for row in tiers_count],
        "operational_costs": 100,  # Placeholder fijo por ahora
        "surplus": mrr - 100
    })


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def get_user_tier(user_id: int) -> str:
    """
    Obtiene el tier actual de un usuario.
    
    Args:
        user_id: ID del usuario
        
    Returns:
        Tier del usuario ('free', 'contributor', 'enterprise')
    """
    db = get_db()
    sub = db.execute(
        """
        SELECT tier FROM subscriptions 
        WHERE user_id = ? 
        AND status = 'active' 
        AND (expires_at IS NULL OR expires_at > datetime('now'))
        ORDER BY started_at DESC
        LIMIT 1
        """,
        (user_id,)
    ).fetchone()
    
    return sub["tier"] if sub else "free"


def has_premium_access(user_id: int, min_tier: str = "contributor") -> bool:
    """
    Verifica si un usuario tiene acceso premium.
    
    Args:
        user_id: ID del usuario
        min_tier: Tier mínimo requerido
        
    Returns:
        True si tiene acceso, False si no
    """
    tier_order = {"free": 0, "contributor": 1, "enterprise": 2}
    user_tier = get_user_tier(user_id)
    return tier_order.get(user_tier, 0) >= tier_order.get(min_tier, 1)


# ============================================================================
# INICIALIZACIÓN
# ============================================================================

def init_subscription_tables(app):
    """
    Inicializa las tablas de suscripción en la base de datos.
    Llamar desde create_app() si las tablas no existen.
    """
    with app.app_context():
        db = get_db()
        
        # Verificar si tabla existe
        table_exists = db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='subscriptions'"
        ).fetchone()
        
        if not table_exists:
            db.execute("""
                CREATE TABLE IF NOT EXISTS subscriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL UNIQUE,
                    tier TEXT NOT NULL CHECK(tier IN ('free', 'contributor', 'enterprise')),
                    status TEXT NOT NULL CHECK(status IN ('active', 'cancelled', 'expired')),
                    started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    expires_at TEXT,
                    payment_method TEXT,
                    external_customer_id TEXT,
                    notes TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            
            db.execute("""
                CREATE TABLE IF NOT EXISTS premium_benefits_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    benefit_type TEXT NOT NULL,
                    claimed_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)
            
            db.commit()
            app.logger.info("Tablas de suscripción creadas correctamente")
