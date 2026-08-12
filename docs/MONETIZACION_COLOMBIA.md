# Manifiesto de Monetización: Bypass Colombia 🇨🇴

## El Contexto del Bloqueo
Stripe, el gigante de los pagos, actualmente no permite la creación de cuentas directas para residentes en Colombia sin una entidad legal en EE.UU. En lugar de ver esto como un muro, la Maxocracia lo ve como una señal: **debemos diversificar y descentralizar la reciprocidad.**

## Nuestra Estrategia de Reciprocidad Justa

### 1. GitHub Sponsors (Internacional y Ético)
GitHub Sponsors es nuestra vía principal para el apoyo de la comunidad global.
- **Soporte en Colombia**: SÍ, está disponible para desarrolladores colombianos.
- **Ventaja**: Cero comisiones de GitHub para individuos, lo cual maximiza el impacto de cada contribución.
- **Uso**: Para miembros de la Cohorte Cero y contribuidores internacionales.

### 2. Wompi (El Motor Local)
Si estás en Colombia y quieres pagar con **PSE, Nequi, Daviplata o Bancolombia**, Wompi es nuestra pasarela preferida.
- **Localización**: Integración directa con el ecosistema financiero colombiano.
- **Coherencia**: Facilita que cualquier ciudadano colombiano pueda contribuir sin necesidad de tarjetas de crédito internacionales.

### 3. Cripto: Estabilidad Sintética (USDC/USDT)
Para los ciudadanos del **Reino Sintético** que prefieren la soberanía digital.
- **Redes**: Polygon o Ethereum.
- **Verificación**: El sistema permite registrar el hash de la transacción para activar los beneficios manualmente o mediante oráculos sintéticos.

### 4. Honor System (Auditoría de la Verdad)
Fieles al Axioma T17 (Reciprocidad Justa), si los métodos anteriores fallan o no son accesibles, el usuario puede auto-certificar su contribución mediante una **"Protesta de Verdad"**.
- El acceso no se bloquea por falta de tecnología, sino por falta de voluntad. Si tienes la voluntad pero el sistema falla, la Maxocracia te abre las puertas.

## Implementación Técnica
Hemos refactorizado el backend para que `subscriptions.py` sea agnóstico al proveedor. 
- `/subscriptions/webhook/github`: Maneja eventos de patrocinios.
- `/subscriptions/webhook/wompi`: Maneja pagos locales colombianos.
- `/subscriptions/register-crypto`: Permite vincular una TX hash a una cuenta premium.

---
*"La abundancia no es tener mucho, sino que nada falte para cumplir la misión."*
