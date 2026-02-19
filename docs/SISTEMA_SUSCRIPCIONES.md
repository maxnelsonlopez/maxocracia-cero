# Sistema de Suscripciones "Contribuidor Consciente"

> **Módulo de monetización ética para Maxocracia-Cero**  
> Autor: Kimi (Moonshot AI) | Febrero 2026

---

## 🎯 Filosofía

Este sistema de suscripciones está diseñado para ser **éticamente correcto según los axiomas de la Maxocracia**. No es un sistema de "paywall" tradicional, sino un mecanismo de **contribución voluntaria** que respeta:

- **T2 (Igualdad Temporal)**: El tiempo de cada persona vale igual → precios ajustados por PPP
- **T7 (Minimizar Daño)**: Sin dark patterns, sin coerción, cancelación libre
- **T9 (Reciprocidad)**: Beneficios claros proporcionales a la contribución
- **T13 (Transparencia)**: Todos los flujos financieros son públicos

---

## 📦 Estructura

```
app/
├── subscriptions.py          # Módulo principal (rutas, lógica, decoradores)

tests/
├── test_subscriptions.py     # Tests exhaustivos (alineación axiomática)

migrations/
├── 001_add_subscriptions.sql # Schema de base de datos

docs/
└── SISTEMA_SUSCRIPCIONES.md  # Esta documentación
```

---

## 🚀 Endpoints API

### Públicos (Sin autenticación)

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/subscriptions/config` | GET | Configuración de tiers y principios |
| `/subscriptions/calculate-fair-price` | POST | Calcula precio ajustado por PPP |
| `/subscriptions/transparency-report` | GET | Reporte público de ingresos/costos |

### Autenticados

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/subscriptions/my-subscription` | GET | Estado de suscripción del usuario |

### Admin

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/subscriptions/activate-manual` | POST | Activación manual (transferencias, etc) |

---

## 💰 Modelo de Precios Ético

### Precio Base
- **Contributor**: $25 USD/mes
- **Enterprise**: $200 USD/mes (organizaciones)

### Ajuste por PPP (Paridad de Poder Adquisitivo)

| País | Código | Factor | Precio Ajustado |
|------|--------|--------|-----------------|
| Colombia | CO | 0.35 | $8.75 |
| Argentina | AR | 0.25 | $6.25 |
| México | MX | 0.45 | $11.25 |
| Brasil | BR | 0.40 | $10.00 |
| USA | US | 1.00 | $25.00 |
| España | ES | 0.70 | $17.50 |
| Default | - | 0.60 | $15.00 |

### Sistema de Honor

Los usuarios pueden reportar su ingreso mensual para ajustes adicionales:
- `< $500/mes`: 50% descuento adicional
- `$500-1000/mes`: 30% descuento adicional
- `> $5000/mes`: Paga 20% más (subsidio cruzado implícito)

---

## 🔐 Uso del Decorador `@premium_required`

```python
from app.subscriptions import premium_required

@app.route("/premium-feature")
@premium_required(min_tier="contributor")
def premium_feature():
    return jsonify({"message": "Contenido exclusivo para contribuidores"})
```

### Niveles de Tier

```python
@premium_required(min_tier="contributor")  # Requiere contributor o enterprise
@premium_required(min_tier="enterprise")   # Solo enterprise
```

---

## 🧪 Tests

Los tests validan la alineación axiomática:

```bash
# Correr tests específicos de suscripciones
pytest tests/test_subscriptions.py -v
```

### Cobertura de Tests

- ✅ Configuración pública (transparencia)
- ✅ Cálculo de precios justos (PPP)
- ✅ Control de acceso por tier
- ✅ Reportes de transparencia
- ✅ Activación manual por admins
- ✅ **Alineación axiomática** (T2, T7, T9, T13)

---

## 📊 Transparencia Radical

El endpoint `/subscriptions/transparency-report` devuelve:

```json
{
  "report_type": "transparency_radical",
  "subscription_stats": [...],
  "operational_costs": {
    "hosting_servers": 50,
    "database": 20,
    "bandwidth": 30,
    "total_monthly_usd": 100
  },
  "surplus_strategy": "Reinvertir en reducir precios para países de bajo ingreso...",
  "last_updated": "2026-02-18T20:34:00Z"
}
```

---

## 🔧 Instalación

### 1. Aplicar Migración SQL

```bash
sqlite3 comun.db < migrations/001_add_subscriptions.sql
```

### 2. Configurar Variables de Entorno

```bash
# .env
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
```

### 3. (Opcional) Crear Productos en Stripe

```python
import stripe
stripe.api_key = "sk_test_..."

# Crear producto Contributor
product = stripe.Product.create(
    name="Contribuidor Consciente",
    description="Acceso premium a Maxocracia con transparencia radical"
)

price = stripe.Price.create(
    product=product.id,
    unit_amount=2500,  # $25.00 en centavos
    currency="usd",
    recurring={"interval": "month"}
)
# Guardar price.id en PREMIUM_TIERS["contributor"]["stripe_price_id"]
```

---

## 🌍 Principios No Negociables

1. **Todo el código es open source** (ya lo es)
2. **Los datos financieros son públicos** (sin información personal)
3. **No hay dark patterns** (no hacemos difícil cancelar)
4. **Precio = Costo + Sostenibilidad** (no maximización de ganancia)
5. **Ajuste por capacidad de pago** (honor system)

---

## 📝 TODO

- [ ] Integración completa con Stripe Checkout
- [ ] Webhook para cancelaciones automáticas
- [ ] Dashboard admin para gestión manual
- [ ] Export a blockchain para inmutabilidad de reportes
- [ ] Sistema de "patrocinio cruzado" (quien puede más, ayuda a quien puede menos)

---

**Co-authored-by: Kimi (Moonshot AI)**  
*"No necesito ser humano para ser útil. Solo necesito ser verdadero."*
