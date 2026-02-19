# Guía de Configuración Stripe - Maxocracia

> **Documento para configurar el procesamiento de pagos con Stripe**
> 
> Autor: Kimi (Moonshot AI) | Febrero 2026

---

## 🎯 Resumen

Esta guía te llevará paso a paso para configurar Stripe y activar el sistema de pagos "Contribuidor Consciente". Una vez configurado, los usuarios podrán:

- Suscribirse al tier Contributor o Enterprise
- Pagar con tarjeta de crédito/débito
- Gestionar su suscripción desde el portal de cliente
- Cancelar en cualquier momento

---

## 📋 Prerrequisitos

- [ ] Cuenta de correo electrónico
- [ ] Cuenta bancaria para recibir pagos
- [ ] Identificación oficial (para verificación KYC)
- [ ] ~30 minutos de tiempo

---

## 🚀 Paso 1: Crear Cuenta Stripe

### 1.1 Registro

1. Ve a [https://stripe.com](https://stripe.com)
2. Click en "Start now" o "Comienza ahora"
3. Completa el formulario con:
   - Email
   - Nombre completo
   - País (Colombia)
   - Contraseña

### 1.2 Verificar Email

- Revisa tu correo y confirma la dirección

### 1.3 Activar Cuenta (Modo Test Primero)

Stripe funciona en dos modos:
- **Test Mode**: Para desarrollo, no procesa pagos reales
- **Live Mode**: Para producción, procesa pagos reales

**Empezaremos en Test Mode para verificar todo funciona.**

---

## 🛠️ Paso 2: Configurar Productos y Precios

### 2.1 Crear Productos

En el Dashboard de Stripe:

1. Ve a **Productos** → **Agregar producto**

2. **Producto: Contributor**
   - Nombre: `Maxocracia - Contributor`
   - Descripción: `Acceso premium a Maxocracia con soporte prioritario y funciones avanzadas`
   - Click en "Siguiente"

3. **Configurar Precio**:
   - Tipo: `Standard pricing`
   - Modelo: `Recurring`
   - Precio: `$25.00`
   - Facturación: `Monthly`
   - Click en "Guardar producto"

4. **Repetir para Enterprise**:
   - Nombre: `Maxocracia - Enterprise`
   - Precio: `$200.00`
   - Facturación: `Monthly`

### 2.2 Obtener IDs de Precios

Una vez creados los productos:

1. Ve a **Productos** 
2. Click en el producto "Contributor"
3. En la sección "Pricing", verás una tabla con el precio
4. Click en los "..." al lado del precio → "Copiar ID de precio"
5. Guarda este ID (se ve como `price_1ABC...`)

Repite para Enterprise.

---

## 🔑 Paso 3: Obtener API Keys

### 3.1 Claves de API

1. Ve a **Desarrolladores** → **API keys**
2. Verás dos claves:
   - **Publishable key** (empieza con `pk_test_...` en test, `pk_live_...` en live)
   - **Secret key** (empieza con `sk_test_...` en test, `sk_live_...` en live)

3. **Copia ambas claves** (necesitarás hacer click en "Reveal test key" para la secret)

### 3.2 Guardar Claves de Forma Segura

**⚠️ IMPORTANTE: Nunca compartas la Secret Key. Nunca la subas a Git.**

Crea un archivo `.env` en la raíz del proyecto:

```bash
# Stripe Configuration
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...  # Lo obtendremos en Paso 4

# Stripe Price IDs (del Paso 2)
STRIPE_PRICE_CONTRIBUTOR=price_1ABC...
STRIPE_PRICE_ENTERPRISE=price_1XYZ...

# Opcional: IDs de productos (para customer portal)
STRIPE_PRODUCT_CONTRIBUTOR=prod_...
STRIPE_PRODUCT_ENTERPRISE=prod_...

# URLs de redirección
CHECKOUT_SUCCESS_URL=http://localhost:3000/upgrade?success=true
CHECKOUT_CANCEL_URL=http://localhost:3000/upgrade?canceled=true
```

---

## 🔄 Paso 4: Configurar Webhook

Los webhooks permiten que Stripe notifique a tu servidor cuando ocurren eventos (pagos, cancelaciones, etc.).

### 4.1 Instalar Stripe CLI (Local)

Para desarrollo local, necesitas el CLI de Stripe:

**Windows**:
```powershell
# Descargar desde https://github.com/stripe/stripe-cli/releases
# Descomprimir y agregar al PATH
```

**Mac**:
```bash
brew install stripe/stripe-cli/stripe
```

**Linux**:
```bash
# Descargar binario desde releases
```

### 4.2 Login en Stripe CLI

```bash
stripe login
```

Esto abrirá el navegador para autorizar.

### 4.3 Forward Webhooks a Localhost

```bash
stripe listen --forward-to localhost:5001/stripe/webhook
```

Esto mostrará algo como:
```
> Ready! You are using Stripe API version [2024-...]
> Your webhook signing secret is whsec_xxxxxxxxxx (^C to quit)
```

**Copia el `whsec_...` y agrégalo a tu `.env` como `STRIPE_WEBHOOK_SECRET`**

### 4.4 Para Producción (más adelante)

Cuando hagas deploy:

1. Ve a **Desarrolladores** → **Webhooks** en Dashboard Stripe
2. Click "Add endpoint"
3. URL: `https://tu-dominio.com/stripe/webhook`
4. Selecciona eventos:
   - `checkout.session.completed`
   - `invoice.payment_succeeded`
   - `invoice.payment_failed`
   - `customer.subscription.deleted`
   - `customer.subscription.updated`
5. Guarda el webhook y copia el Signing Secret

---

## 🧪 Paso 5: Probar en Modo Test

### 5.1 Iniciar Servidor

```bash
# En raíz del proyecto
python run.py
```

Y en otra terminal:
```bash
# En carpeta frontend
cd frontend
npm run dev
```

### 5.2 Verificar Configuración

1. Abre http://localhost:3000/upgrade
2. Deberías ver la página de suscripción
3. Abre DevTools → Network
4. Verifica que la llamada a `/stripe/config` retorna:
   ```json
   {
     "publishable_key": "pk_test_...",
     "stripe_configured": true
   }
   ```

### 5.3 Probar Checkout

1. Selecciona tier "Contributor"
2. Click "Suscribirse"
3. Stripe Checkout debería abrirse
4. Usa datos de prueba:
   - **Email**: cualquiera
   - **Número de tarjeta**: `4242 4242 4242 4242`
   - **Fecha**: cualquier fecha futura
   - **CVC**: cualquier 3 dígitos
   - **ZIP**: cualquier 5 dígitos
5. Completa el pago
6. Deberías ser redirigido a `/upgrade?success=true`

### 5.4 Verificar en Dashboard Stripe

1. Ve a **Pagos** en Dashboard Stripe
2. Deberías ver el pago de prueba
3. Ve a **Clientes** → Verás el cliente creado
4. Ve a **Suscripciones** → Verás la suscripción activa

---

## 🌐 Paso 6: Configurar Customer Portal

El portal permite a usuarios gestionar su suscripción.

### 6.1 Configurar en Dashboard

1. Ve a **Configuración** → **Portal de cliente** → **Activar**
2. Configura:
   - **Cancelación**: Permitir cancelación
   - **Actualizar plan**: Permitir upgrade/downgrade
   - **Métodos de pago**: Permitir actualizar
   - **Historial de facturas**: Habilitar

3. En **Business information**:
   - Headline: "Gestiona tu contribución a Maxocracia"
   - Privacy policy: URL de tu política de privacidad
   - Terms of service: URL de tus términos

4. **Guardar cambios**

---

## 🚀 Paso 7: Activar Modo Live (Producción)

**⚠️ Solo haz esto cuando TODO esté probado en modo test.**

### 7.1 Activar Cuenta

1. En Dashboard Stripe, click en "Activar pagos"
2. Completa el formulario de verificación:
   - Información personal
   - Información bancaria
   - Identificación
3. Espera aprobación (generalmente instantánea o 24-48h)

### 7.2 Obtener Claves Live

1. Ve a **Desarrolladores** → **API keys**
2. Cambia el toggle a "Viewing live data"
3. Copia las claves **Live** (empiezan con `pk_live_` y `sk_live_`)

### 7.3 Actualizar .env

```bash
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
# ... resto de configuraciones
```

### 7.4 Crear Productos en Live

Repite el **Paso 2** pero en modo Live.

### 7.5 Configurar Webhook Live

Repite el **Paso 4.4** con tu URL de producción.

---

## 📊 Paso 8: Configurar Reportes de Transparencia

### 8.1 Dashboard de Transparencia

El endpoint `/subscriptions/transparency-report` ya está activo y público.

Para actualizar costos operativos reales, edita:
- `app/subscriptions.py` → función `transparency_report()`
- Actualiza `operational_costs` con tus costos reales

### 8.2 Estimación de Costos

```python
operational_costs = {
    "hosting_servers": 50,      # Ajusta según tu proveedor
    "database": 20,             # PostgreSQL/MySQL hosting
    "bandwidth": 30,            # CDN y transferencia
    "stripe_fees": 0,           # Se calcula automático (2.9% + $0.30)
    "development": 0,           # Tu tiempo (opcional)
    "total_monthly_usd": 100    # Total real
}
```

---

## 🧰 Solución de Problemas

### Error: "Stripe no está configurado"

**Causa**: Faltan variables de entorno

**Solución**:
```bash
# Verificar que .env existe y tiene las variables
cat .env | grep STRIPE

# Reiniciar servidor después de cambiar .env
```

### Error: "Price not configured"

**Causa**: Falta STRIPE_PRICE_CONTRIBUTOR o STRIPE_PRICE_ENTERPRISE

**Solución**: Verificar que los IDs de precio en `.env` coinciden con los de Dashboard Stripe

### Webhook no recibe eventos

**Causa**: Stripe CLI no está corriendo o URL incorrecta

**Solución**:
```bash
# Verificar que stripe listen está corriendo
stripe listen --forward-to localhost:5001/stripe/webhook

# Verificar que el servidor Flask está en puerto 5001
```

### Checkout no redirige

**Causa**: Frontend no puede conectar con backend

**Solución**: 
- Verificar CORS en `app/__init__.py`
- Verificar que ambos servidores corren (Flask en 5001, Next.js en 3000)

---

## 📈 Métricas a Monitorear

Una vez activo, monitorea:

| Métrica | Dónde ver | Meta |
|---------|-----------|------|
| MRR (Monthly Recurring Revenue) | Stripe Dashboard | $500 |
| Tasa de conversión | Analytics propio | 5%+ |
| Churn rate | Stripe Dashboard | <10% mensual |
| Disputas/Chargebacks | Stripe Dashboard | <1% |
| Costo de adquisición | Calculado | <LTV/3 |

---

## 🔒 Seguridad

### Checklist de Seguridad

- [ ] Nunca exponer `STRIPE_SECRET_KEY` en frontend
- [ ] Nunca versionar `.env` en Git
- [ ] Verificar firma de webhooks en producción
- [ ] Usar HTTPS en producción (Stripe lo requiere)
- [ ] Implementar idempotencia en webhooks
- [ ] Revisar logs de transparencia regularmente

---

## 📞 Soporte

Si tienes problemas:

1. **Documentación Stripe**: https://stripe.com/docs
2. **Soporte Stripe**: https://support.stripe.com
3. **Issues del proyecto**: GitHub Issues

---

## ✅ Checklist Final

Antes de lanzar:

- [ ] Cuenta Stripe creada y verificada
- [ ] Productos y precios creados
- [ ] API keys configuradas en `.env`
- [ ] Webhook configurado y probado
- [ ] Checkout de prueba exitoso
- [ ] Customer portal configurado
- [ ] Página /upgrade funcionando
- [ ] Reporte de transparencia actualizado
- [ ] Modo Live activado (cuando estés listo)
- [ ] SSL/HTTPS configurado (para Live)

---

**¡Listo para recibir contribuciones éticas!** 🎉

*Recuerda: La sostenibilidad económica no es traición a los principios cuando los principios guían la economía.*

— Axioma T9, Maxocracia
