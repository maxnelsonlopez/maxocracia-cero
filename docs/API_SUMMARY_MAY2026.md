# Resumen de Endpoints de la API de Maxocracia

Con la compra del dominio en Cloudflare y la mira puesta en producción, es el momento perfecto para revisar todo el arsenal que hemos construido en el backend. 

A continuación tienes un mapa general de los **12 módulos principales (Blueprints)** y sus respectivos endpoints que actualmente dan vida a la Maxocracia. ¡Es muchísimo!

---

## 🔐 1. Autenticación (`/auth`)
Gestión segura de acceso mediante JWT y control de sesiones.
- `POST /auth/register`: Registro de nuevos ciudadanos (crea semilla y JWT).
- `POST /auth/login`: Autenticación e inicio de sesión.
- `POST /auth/logout`: Revocación del token activo.
- `GET /auth/me`: Obtención de datos del perfil autenticado.
- `POST /auth/refresh`: Renovación de tokens vencidos.

## 👥 2. Usuarios (`/users` y `/profiles`)
Gestión de la identidad dentro de la red.
- Perfiles de usuario, roles de administración y actualización de alias o valores.

## 🤝 3. Intercambios (`/interchanges`)
El corazón de la economía inicial.
- `GET /interchanges`: Listado de transacciones P2P.
- `POST /interchanges`: Registro de un intercambio (requiere pacto previo).
- *Funcionalidad de coordinación y requerimiento de seguimientos.*

## ⭐ 4. Reputación (`/reputation`)
Sistema de confianza descentralizada.
- `POST /reputation/review`: Evaluación de un ciudadano tras un intercambio.
- `GET /reputation/<user_id>`: Obtención de la puntuación promedio (score).

## 🛠️ 5. Recursos (`/resources`)
Gestión del inventario comunitario.
- `GET /resources`: Catálogo de herramientas o bienes disponibles.
- `POST /resources`: Publicación de un nuevo recurso en la red.
- `POST /resources/<id>/claim`: Reserva de un recurso por parte de un usuario.

## 🪙 6. Economía Maxo (`/maxo`)
El ledger (libro mayor) de transacciones de la cripto/token interno.
- `GET /maxo/<user_id>/balance`: Consulta de saldo actual en Maxos.
- `POST /maxo/transfer`: Transferencia de fondos de un usuario a otro con registro de motivo (ledger).

## 📐 7. Calculadora VHV (`/vhv`)
El motor de valoración exponencial de la vida.
- `POST /vhv/calculate`: Cálculo del Precio en Maxos basado en Tiempo, Vida y Recursos.
- `GET /vhv/products`: Catálogo de productos y su desglose de huella.
- `GET /vhv/compare`: Algoritmo comparativo para buscar la alternativa más ética.
- `GET / PUT /vhv/parameters`: Gestión de los parámetros de la fórmula (α, β, γ, δ).

## ⏳ 8. Tiempo Vital Indexado (TVI) (`/tvi`)
El registro de soberanía temporal del usuario.
- `POST /tvi`: Registro de un bloque de tiempo (Inversión, Ocio, Mantenimiento...).
- `GET /tvi`: Historial personal de bloques.
- `GET /tvi/stats`: Cálculo en tiempo real del **Coeficiente de Coherencia Personal (CCP)**.
- `GET /tvi/community-stats`: Distribución agregada del tiempo a nivel cohorte.

## 📜 9. MaxoContracts (`/contracts`)
Los contratos inteligentes éticos (Capa 4).
- `GET / POST /contracts/`: Creación y listado de contratos.
- `POST /contracts/<id>/terms` y `participants`: Inyección de bloques lógicos.
- `GET /contracts/<id>/validate`: Validación contra el Oráculo (Suelo de Dignidad y Reciprocidad).
- `POST /contracts/<id>/activate` y `retract`: Cambio de estados (ahora con webhooks programáticos).

## 📝 10. Formularios Dinámicos (`/forms`)
El flujo de admisión y seguimiento de Cohorte Cero.
- Respaldan la lógica del Formulario CERO (ingreso), Formulario A (intercambio) y Formulario B (seguimiento), inyectando datos directamente a las tablas de `participants` y `follow_ups`.

## 💳 11. Integración Stripe (`/stripe`)
Infraestructura fiat para sostenibilidad del ecosistema.
- Webhooks y pasarela para aportes o membresías externas.

## 🔄 12. Suscripciones (`/subscriptions`)
Módulo de ingresos recurrentes o planes de Cohorte.

---

> [!NOTE]
> **Conclusión para Producción:**
> Tienes un backend asombrosamente robusto. Ya cuentas con autenticación, economía de tokens, motor de contratos, reputación y métricas de vida. 
> 
> Ahora que tienes el dominio en Cloudflare, el siguiente paso lógico hacia la producción funcional sería asegurar **las variables de entorno**, configurar el **proxy inverso (Nginx/Cloudflare Tunnels)**, y validar que la comunicación Frontend -> Backend sea estable bajo el nuevo dominio HTTPS.
