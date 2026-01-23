# Documentación de la API de Maxocracia

Bienvenido a la documentación de la API de Maxocracia. Este documento proporciona una guía completa para interactuar con los servicios de Maxocracia, incluyendo autenticación, gestión de intercambios, reputación y más.

## Tabla de Contenidos

- [Introducción](#introducción)
- [Autenticación](#autenticación)
- [Endpoints](#endpoints)
  - [Autenticación](#autenticación-1)
  - [Intercambios](#intercambios)
  - [Reputación](#reputación)
  - [Recursos](#recursos)
  - [Maxo (Moneda)](#maxo-moneda)
- [Rate Limiting](#rate-limiting)
- [Calculadora VHV](#calculadora-vhv)
- [TVI (Tiempo Vital Indexado)](#tvi-tiempo-vital-indexado)
- [Seguridad](#seguridad)
- [Ejecución Local](#ejecución-local)
- [Pruebas](#pruebas)
- [Notas de Seguridad](#notas-de-seguridad)

## Introducción

La API de Maxocracia está construida con Flask y utiliza SQLite como base de datos. Sigue los principios RESTful y utiliza JSON para el intercambio de datos.

### Convenciones

- **URL Base**: `http://localhost:5001` (para desarrollo)
- **Formato de Fechas**: ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`)
- **Autenticación**: JWT (JSON Web Tokens)
- **Tasa de Límite**: Aplicada según el endpoint
- **Formato de Respuesta**: JSON
- **Interfaz Administrativa**: `/admin` (HTML)

### Códigos de Estado HTTP

| Código | Descripción |
|--------|-------------|
| 200 | OK - La solicitud fue exitosa |
| 201 | Creado - Recurso creado exitosamente |
| 400 | Solicitud incorrecta - Verifica los parámetros |
| 401 | No autorizado - Se requiere autenticación |
| 403 | Prohibido - No tienes permiso |
| 404 | No encontrado - El recurso no existe |
| 429 | Demasiadas solicitudes - Límite de tasa excedido |
| 500 | Error del servidor - Algo salió mal |

## Autenticación

La autenticación se realiza mediante JWT (JSON Web Tokens). Debes incluir el token en el encabezado `Authorization: Bearer <token>` para acceder a los endpoints protegidos.

### Flujo de Autenticación

1. **Registro**: Crea una nueva cuenta de usuario
2. **Inicio de Sesión**: Obtén un token de acceso y un token de actualización
3. **Uso**: Incluye el token de acceso en las solicitudes
4. **Renovación**: Usa el token de actualización para obtener un nuevo token de acceso

### Tokens

- **Token de Acceso**: Válido por 15 minutos
- **Token de Actualización**: Válido por 7 días, se usa para obtener nuevos tokens de acceso

## Ejecución Local

### Requisitos

- Python 3.8+
- pip
- SQLite3

### Configuración Inicial

1. Clona el repositorio
2. Crea un entorno virtual:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```
4. Inicializa la base de datos:
   ```bash
   python3 seeds/seed_demo.py
   ```
5. Inicia el servidor:
   ```bash
   PORT=5001 python3 run.py
   ```

## Endpoints

### Autenticación

#### Registrar Usuario

```http
POST /auth/register
```

**Cuerpo de la Solicitud:**
```json
{
  "email": "usuario@ejemplo.com",
  "password": "contraseñaSegura123",
  "name": "Nombre del Usuario",
  "alias": "alias_usuario"
}
```

**Parámetros:**
- `email` (string, requerido): Correo electrónico del usuario
- `password` (string, requerido): Contraseña (mínimo 8 caracteres)
- `name` (string, requerido): Nombre completo del usuario
- `alias` (string, opcional): Alias del usuario

**Respuesta Exitosa (201):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "jti.raw_refresh_token",
  "expires_in": 3600
}
```

**Errores:**
- 400: Datos inválidos o faltantes
- 409: El correo electrónico ya está registrado
- 429: Demasiadas solicitudes

#### Iniciar Sesión

```http
POST /auth/login
```

**Cuerpo de la Solicitud:**
```json
{
  "email": "usuario@ejemplo.com",
  "password": "contraseñaSegura123"
}
```

**Respuesta Exitosa (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "jti.raw_refresh_token",
  "expires_in": 3600
}
```

**Errores:**
- 400: Credenciales faltantes
- 401: Credenciales inválidas
- 429: Demasiados intentos de inicio de sesión

#### Cerrar Sesión

```http
POST /auth/logout
```

**Encabezados:**
```
Authorization: Bearer <token>
```

**Respuesta Exitosa (200):**
```json
{
  "message": "Sesión cerrada exitosamente"
}
```

**Errores:**
- 401: No autorizado

#### Obtener Perfil de Usuario

```http
GET /auth/me
```

**Encabezados:**
```
Authorization: Bearer <token>
```

**Respuesta Exitosa (200):**
```json
{
  "user_id": 1,
  "email": "usuario@ejemplo.com",
  "name": "Nombre del Usuario",
  "alias": "alias_usuario",
  "created_at": "2025-11-13T18:00:00Z"
}
```

**Errores:**
- 401: No autorizado

#### Renovar Token de Acceso

```http
POST /auth/refresh
```

**Encabezados:**
```
Authorization: Bearer <refresh_token>
```

**Respuesta Exitosa (200):**
```json
{
  "token": "nuevo_token_de_acceso",
  "refresh_token": "nuevo_refresh_token"
}
```

**Errores:**
- 400: Token de actualización inválido o faltante
- 401: Token de actualización inválido o expirado

### Intercambios

#### Listar Intercambios

```http
GET /interchanges
```

**Parámetros de Consulta:**
- `limit` (opcional, default=200): Número máximo de intercambios a devolver
- `offset` (opcional, default=0): Número de intercambios a omitir

**Respuesta Exitosa (200):**
```json
[
  {
    "interchange_id": "550e8400-e29b-41d4-a716-446655440000",
    "giver_id": 1,
    "receiver_id": 2,
    "description": "Intercambio de servicios",
    "uth_hours": 2.5,
    "uvc_score": 0.5,
    "urf_units": 1.2,
    "vhv_time_seconds": 9000,
    "vhv_lives": 0.5,
    "vhv_resources_json": "{\"agua\": 10, \"energia\": 5}",
    "impact_resolution_score": 8,
    "created_at": "2025-11-13T18:00:00Z"
  }
]
```

#### Crear Intercambio

```http
POST /interchanges
```

**Encabezados:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Cuerpo de la Solicitud:**
```json
{
  "interchange_id": "550e8400-e29b-41d4-a716-446655440000",
  "giver_id": 1,
  "receiver_id": 2,
  "description": "Intercambio de servicios",
  "uth_hours": 2.5,
  "impact_resolution_score": 8,
  "uvc_score": 0.5,
  "urf_units": 1.2,
  "vhv_time_seconds": 9000,
  "vhv_lives": 0.5,
  "vhv_resources": {
    "agua": 10,
    "energia": 5
  }
}
```

**Respuesta Exitosa (201):**
```json
{
  "message": "Intercambio creado exitosamente",
  "credit": 3.1,
  "interchange_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Fórmula de Valoración Maxo (Polinómica):**
```
Precio = α·T + β·V^γ + δ·R·(FRG × CS)
```

Donde:
- `T` (Tiempo): Horas de Tiempo Vital indexado.
- `V` (Vida): Unidades de Vida Consumidas (UVC).
- `R` (Recursos): Unidades de recursos finitos.
- `α` (Alpha): Peso del tiempo (Default: 100.0).
- `β` (Beta): Peso de la vida (Default: 2000.0).
- `γ` (Gamma): Exponente de aversión al sufrimiento (Default: 1.0, debe ser ≥ 1).
- `δ` (Delta): Peso de recursos (Default: 100.0).
- `FRG`: Factor de Rareza Geológica.
- `CS`: Criticidad Sistémica.

**Nota:** Los parámetros se obtienen dinámicamente de la base de datos (Tabla `vhv_parameters`).

**Errores:**
- 400: Datos inválidos o faltantes
- 401: No autorizado
- 500: Error al crear el intercambio

### Reputación

#### Crear o Actualizar Revisión

```http
POST /reputation/review
```

**Encabezados:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Cuerpo de la Solicitud:**
```json
{
  "user_id": 2,
  "score": 5
}
```

**Respuesta Exitosa (201):**
```json
{
  "message": "Revisión guardada exitosamente",
  "review_id": 1,
  "average_score": 4.8,
  "total_reviews": 1
}
```

**Errores:**
- 400: Puntuación inválida (debe estar entre 1 y 5)
- 401: No autorizado
- 404: Usuario no encontrado

#### Obtener Reputación de Usuario

```http
GET /reputation/<int:user_id>
```

**Respuesta Exitosa (200):**
```json
{
  "user_id": 2,
  "score": 4.8,
  "reviews_count": 15
}
```

**Errores:**
- 404: Usuario no encontrado

### Recursos

#### Listar Recursos Disponibles

```http
GET /resources
```

**Respuesta Exitosa (200):**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "title": "Herramientas de jardinería",
    "description": "Juego completo de herramientas para jardinería",
    "category": "herramientas",
    "status": "available",
    "created_at": "2025-11-10T10:00:00Z"
  }
]
```

#### Crear Recurso

```http
POST /resources
```

**Encabezados:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Cuerpo de la Solicitud:**
```json
{
  "user_id": 1,
  "title": "Bicicleta de montaña",
  "description": "Bicicleta en buen estado para uso urbano",
  "category": "transporte"
}
```

**Respuesta Exitosa (201):**
```json
{
  "id": 2,
  "user_id": 1,
  "title": "Bicicleta de montaña",
  "description": "Bicicleta en buen estado para uso urbano",
  "category": "transporte",
  "status": "available",
  "created_at": "2025-11-13T18:00:00Z"
}
```

**Errores:**
- 400: Datos inválidos o faltantes
- 401: No autorizado

#### Reclamar Recurso

```http
POST /resources/<int:resource_id>/claim
```

**Encabezados:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Cuerpo de la Solicitud:**
```json
{
  "user_id": 2
}
```

**Respuesta Exitosa (200):**
```json
{
  "message": "Recurso reclamado exitosamente",
  "resource_id": 2,
  "status": "claimed"
}
```

**Errores:**
- 400: El recurso no está disponible
- 401: No autorizado
- 404: Recurso no encontrado

### Maxo (Moneda)

#### Obtener Saldo

```http
GET /maxo/<int:user_id>/balance
```

**Encabezados:**
```
Authorization: Bearer <token>
```

**Respuesta Exitosa (200):**
```json
{
  "user_id": 1,
  "balance": 150.75,
  "updated_at": "2025-11-13T18:00:00Z"
}
```

**Errores:**
- 401: No autorizado
- 403: No tienes permiso para ver este saldo
- 404: Usuario no encontrado

#### Transferir Maxo

```http
POST /maxo/transfer
```

**Encabezados:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Cuerpo de la Solicitud:**
```json
{
  "from_user_id": 1,
  "to_user_id": 2,
  "amount": 50.25,
  "reason": "Pago por servicios"
}
```

**Respuesta Exitosa (200):**
```json
{
  "message": "Transferencia exitosa",
  "transaction_id": "tx_1234567890",
  "from_balance": 100.50,
  "to_balance": 75.25
}
```

**Errores:**
- 400: Fondos insuficientes o monto inválido
- 401: No autorizado
- 403: No tienes permiso para realizar esta transferencia
- 404: Usuario no encontrado

### Calculadora VHV

#### Calcular VHV y Precio

```http
POST /vhv/calculate
```

Calcula el Vector de Huella Vital y el precio en Maxos para un producto dado.

**Cuerpo de la Solicitud:**
```json
{
  "name": "Producto Ejemplo",
  "t_direct_hours": 1.5,
  "t_inherited_hours": 0.5,
  "t_future_hours": 0.1,
  "v_organisms_affected": 0.001,
  "v_consciousness_factor": 0.9,
  "v_suffering_factor": 1.1,
  "v_abundance_factor": 0.0006,
  "v_rarity_factor": 1.0,
  "r_minerals_kg": 0.1,
  "r_water_m3": 0.05,
  "r_petroleum_l": 0.0,
  "r_land_hectares": 0.0,
  "r_frg_factor": 1.0,
  "r_cs_factor": 1.0,
  "save": true
}
```

**Respuesta Exitosa (200):**
```json
{
  "vhv": {
    "T": 2.1,
    "V": 0.000594,
    "R": 0.105
  },
  "maxo_price": 220.55,
  "breakdown": {
    "time_contribution": 210.0,
    "life_contribution": 0.05,
    "resource_contribution": 10.5
  },
  "product_id": 1
}
```

#### Listar Productos

```http
GET /vhv/products
```

**Parámetros:**
- `category`: Filtrar por categoría
- `limit`: Límite de resultados (default 50)
- `offset`: Paginación

#### Comparar Productos

```http
GET /vhv/compare?ids=1,2
```

Compara dos o más productos y determina cuál es el más económico en términos de Maxos (costo vital).

**Respuesta Exitosa (200):**
```json
{
  "products": [...],
  "comparison": {
    "cheapest": {...},
    "most_expensive": {...}
  }
}
```

#### Obtener Parámetros de Valoración

```http
GET /vhv/parameters
```

Devuelve los valores actuales de α, β, γ, δ utilizados en la fórmula de precio.

#### Actualizar Parámetros (Requiere Auth)

```http
PUT /vhv/parameters
```

**Cuerpo:**
```json
{
  "alpha": 100.0,
  "notes": "Ajuste trimestral"
}
```

### TVI (Tiempo Vital Indexado)

#### Registrar Bloque de Tiempo

```http
POST /tvi
```

**Requiere Autenticación:** Sí

Registra un bloque de tiempo vital único para el usuario autenticado. Implementa el Axioma T0 (Unicidad Existencial) rechazando bloques que se superpongan.

**Cuerpo de la Solicitud:**
```json
{
  "start_time": "2025-01-01T10:00:00",
  "end_time": "2025-01-01T11:30:00",
  "category": "INVESTMENT",
  "description": "Estudio de arquitectura temporal"
}
```

**Categorías Válidas:**
- `MAINTENANCE`: Tiempo de mantenimiento vital (sueño, alimentación, higiene)
- `INVESTMENT`: Inversión en capitales vitales (aprendizaje, desarrollo)
- `LEISURE`: Tiempo de disfrute consciente
- `WORK`: Trabajo remunerado o productivo
- `WASTE`: Tiempo desperdiciado o no intencional

**Respuesta Exitosa (201):**
```json
{
  "id": 1,
  "user_id": 1,
  "start_time": "2025-01-01T10:00:00",
  "end_time": "2025-01-01T11:30:00",
  "duration_seconds": 5400,
  "category": "INVESTMENT",
  "description": "Estudio de arquitectura temporal"
}
```

**Errores:**
- 400: Datos inválidos, categoría incorrecta, o violación del Axioma T0 (superposición detectada)
- 401: No autorizado

#### Listar Bloques de Tiempo

```http
GET /tvi
```

**Requiere Autenticación:** Sí

**Parámetros:**
- `limit`: Límite de resultados (default 50)
- `offset`: Paginación

**Respuesta Exitosa (200):**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "start_time": "2025-01-01T10:00:00",
    "end_time": "2025-01-01T11:30:00",
    "duration_seconds": 5400,
    "category": "INVESTMENT",
    "description": "Estudio de arquitectura temporal",
    "created_at": "2025-01-01T10:00:00"
  }
]
```

#### Obtener Estadísticas y CCP

```http
GET /tvi/stats
```

**Requiere Autenticación:** Sí

Calcula el **Coeficiente de Coherencia Personal (CCP)**, una métrica que mide la soberanía del usuario sobre su tiempo vital.

**Parámetros Opcionales:**
- `start_date`: Fecha de inicio (ISO8601)
- `end_date`: Fecha de fin (ISO8601)

**Respuesta Exitosa (200):**
```json
{
  "ccp": 0.8571,
  "stats": {
    "MAINTENANCE": 28800,
    "INVESTMENT": 28800,
    "LEISURE": 14400,
    "WASTE": 7200,
    "WORK": 0
  },
  "total_seconds": 79200,
  "discretionary_seconds": 50400
}
```

**Fórmula CCP:**
```
CCP = (Investment + Leisure) / (Total Time - Maintenance)
```

Un CCP cercano a 1.0 indica alta intencionalidad y soberanía temporal.

#### Obtener Estadísticas Comunitarias

```http
GET /tvi/community-stats
```

**Requiere Autenticación:** No (Público para transparencia)

Devuelve estadísticas agregadas de toda la comunidad (CCP promedio y distribución total de tiempo).

**Respuesta Exitosa (200):**
```json
{
  "active_users_count": 15,
  "average_ccp": 0.725,
  "distribution": {
    "INVESTMENT": 45000,
    "LEISURE": 20000,
    "MAINTENANCE": 50000,
    "WASTE": 5000,
    "WORK": 40000
  },
  "total_hours_logged": 44.4
}
```

#### Calcular VHV desde TVIs Registrados

```http
POST /vhv/calculate-from-tvi
```

**Requiere Autenticación:** Sí

Calcula el VHV usando entradas TVI registradas del usuario para el componente T (Tiempo). Esta integración permite usar el tiempo vital real registrado en lugar de valores manuales.

**Cuerpo de la Solicitud:**
```json
{
  "start_date": "2025-01-01T00:00:00",
  "end_date": "2025-01-31T23:59:59",
  "category_filter": "WORK",
  "v_organisms_affected": 0.001,
  "v_consciousness_factor": 0.9,
  "v_suffering_factor": 1.1,
  "v_abundance_factor": 0.0006,
  "v_rarity_factor": 1.0,
  "r_minerals_kg": 0.1,
  "r_water_m3": 0.05,
  "r_petroleum_l": 0.0,
  "r_land_hectares": 0.0,
  "r_frg_factor": 1.0,
  "r_cs_factor": 1.0,
  "inherited_hours_override": 0.5,
  "future_hours_override": 0.2,
  "save": false
}
```

**Parámetros Opcionales:**
- `start_date`: Filtrar TVIs desde esta fecha (ISO8601)
- `end_date`: Filtrar TVIs hasta esta fecha (ISO8601)
- `category_filter`: Filtrar por categoría (MAINTENANCE, INVESTMENT, WASTE, WORK, LEISURE)
- `inherited_hours_override`: Sobrescribir horas heredadas calculadas (default: 0)
- `future_hours_override`: Sobrescribir horas futuras calculadas (default: 0)
- `save`: Guardar producto en base de datos (default: false)

**Respuesta Exitosa (200):**
```json
{
  "vhv": {
    "T": 2.1,
    "V": 0.000594,
    "R": 0.105
  },
  "maxo_price": 220.55,
  "breakdown": {
    "time_contribution": 210.0,
    "life_contribution": 0.05,
    "resource_contribution": 10.5
  },
  "parameters_used": {
    "alpha": 100.0,
    "beta": 2000.0,
    "gamma": 1.0,
    "delta": 100.0
  },
  "ttvi_breakdown": {
    "direct_hours": 1.5,
    "inherited_hours": 0.0,
    "future_hours": 0.0,
    "total_hours": 1.5,
    "breakdown_by_category": {
      "WORK": 1.5
    }
  },
  "product_id": 1
}
```

**Notas:**
- El componente T se calcula automáticamente desde las entradas TVI del usuario autenticado
- Las categorías WORK e INVESTMENT se consideran "direct_hours" (tiempo directamente invertido)
- Las horas heredadas y futuras pueden sobrescribirse si se conocen valores más precisos
- Este endpoint implementa el Axioma T8 (Encadenamiento Temporal) integrando TVI con VHV

## Rate Limiting

La API implementa límites de tasa para prevenir abusos. Los límites varían según el endpoint:

- `POST /auth/login`: 5 solicitudes por minuto
- `POST /auth/register`: 10 solicitudes por hora
- `POST /auth/refresh`: 20 solicitudes por hora
- Resto de la API: 200 solicitudes por día, 50 por hora

### Respuesta de Error (429):
```json
{
  "error": "Demasiadas peticiones",
  "message": "5 per 1 minute",
  "retry_after": 60
}
```

## Seguridad

### Configuración Recomendada para Producción

Copia el archivo `config.example.env` a `.env` y configura los siguientes valores:

```env
SECRET_KEY=tu_clave_secreta_muy_larga_y_segura
FLASK_ENV=production
PORT=5001
REDIS_URL=redis://localhost:6379/0
RATELIMIT_LOGIN_LIMIT="5 per minute"
RATELIMIT_REGISTER_LIMIT="10 per hour"
RATELIMIT_REFRESH_LIMIT="20 per hour"
RATELIMIT_API_LIMIT="50 per hour"
```

### Mejores Prácticas

1. **Tokens JWT**:
   - Nunca compartas tus tokens
   - Almacénalos de forma segura
   - Usa HTTPS para todas las comunicaciones

2. **Contraseñas**:
   - Usa contraseñas fuertes y únicas
   - No las reutilices en otros servicios

3. **Rate Limiting**:
   - Implementa retroalimentación al usuario cuando se acerque al límite
   - Considera implementar un sistema de cola para solicitudes frecuentes

## Pruebas

Ejecuta las pruebas con:

```bash
python3 -m pytest -v
```

## Notas de Seguridad

1. **Contraseñas**:
   - Las contraseñas se almacenan con hash seguro (Werkzeug)
   - Las contraseñas de demostración están en texto plano solo para pruebas locales

2. **Tokens JWT**:
   - La clave secreta se configura mediante la variable de entorno `SECRET_KEY`
   - Los tokens tienen una vida útil limitada
   - Los tokens de actualización se rotan automáticamente

3. **Base de Datos**:
   - SQLite se usa para desarrollo
   - Considera usar PostgreSQL para producción

4. **Monitoreo**:
   - Implementa monitoreo de seguridad
   - Revisa regularmente los logs de acceso

## Soporte

Para problemas o preguntas, por favor abre un issue en el repositorio del proyecto.

## Getting started (local)

- Create virtualenv and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

- Initialize DB and seed (optional):

```bash
python3 seeds/seed_demo.py
```

- Run server (choose a free port):

```bash
PORT=5001 python3 run.py
```

## Authentication (JWT)

Register a user:

```bash
curl -X POST http://127.0.0.1:5001/auth/register -H 'Content-Type: application/json' -d '{"email":"alice@example.com","password":"password1","name":"Alice"}'
```

Login and obtain token:

```bash
curl -s -X POST http://127.0.0.1:5001/auth/login -H 'Content-Type: application/json' -d '{"email":"alice@example.com","password":"password1"}' | jq -r '.token'
```

Use token in Authorization header:

```bash
curl -H "Authorization: Bearer <TOKEN>" http://127.0.0.1:5001/maxo/1/balance
```

## Endpoints (summary)

- POST /auth/register

  - body: { email, password, name, alias }
  - returns 201 on success

- POST /auth/login

  - body: { email, password }
  - returns { token, user_id }

- GET /interchanges

  - returns list of interchanges

- POST /interchanges

  - body: { interchange_id, giver_id, receiver_id, uth_hours, impact_resolution_score, description }
  - on success returns { message, credit }

  - optional fields:
    - `uvc_score` (number): componente de Unidades de Vida Consumidas
    - `urf_units` (number): componente de Unidades de Recursos Finitos
  - credit formula (configurable):
    - `credit = uth_hours*MAXO_WEIGHT_UTH + impact_resolution_score*MAXO_WEIGHT_IMPACT + uvc_score*MAXO_WEIGHT_UVC + urf_units*MAXO_WEIGHT_URF`
    - defaults: `MAXO_WEIGHT_UTH=1.0`, `MAXO_WEIGHT_IMPACT=0.5`, `MAXO_WEIGHT_UVC=0.0`, `MAXO_WEIGHT_URF=0.0`
  - implementation: `app/maxo.py:12–26` y uso en `app/interchanges.py:35–44,27–33`

### VHV (Vector de Huella Vital)

- Definición: `VHV = (tiempo_total_consumido, seres_vivos_consumidos, recursos_consumidos)`.
- En `interchange` se almacena como:
  - `vhv_time_seconds` (número): segundos totales consumidos (por defecto `uth_hours*3600`).
  - `vhv_lives` (número): fracciones o enteros de vidas consumidas (por defecto `uvc_score` si se provee, o `0`).
  - `vhv_resources_json` (JSON texto): desglose de recursos (energía, agua, CO2, etc.).
- Body opcional en `POST /interchanges`:
  - `vhv_time_seconds`: número.
  - `vhv_lives`: número.
  - `vhv_resources`: objeto JSON.
- Notas:
  - VHV registra datos objetivos; la conversión a crédito usa pesos separados (ver fórmula de crédito).
  - Los campos VHV son opcionales; si no se envían, se derivan valores básicos para mantener compatibilidad.

- POST /reputation/review

  - body: { user_id, score }
  - adds/updates reputation average for the user

- GET /reputation/<user_id>

  - returns { user_id, score, reviews_count }

- POST /resources

  - body: { user_id, title, description, category }
  - creates a resource and returns 201

- GET /resources

  - returns list of available resources

- POST /resources/<id>/claim

  - body: { user_id }
  - claims a resource (marks unavailable)

- GET /maxo/<user_id>/balance

  - returns { user_id, balance }

- POST /maxo/transfer
  - protected (Authorization: Bearer <token>)
  - body: { from_user_id, to_user_id, amount, reason }
  - requires token user_id == from_user_id
 - enforces sufficient balance (no overdraft)

## Rate limiting

The API enforces per-endpoint rate limits using Flask-Limiter.

- Defaults (production):
  - `POST /auth/login`: `5 per minute`
  - `POST /auth/register`: `10 per hour`
  - `POST /auth/refresh`: `20 per hour`
  - General API: `200 per day`, `50 per hour`

- Testing behavior:
  - In testing (`app.config['TESTING']=True`) the defaults are permissive to avoid interfering with the suite.
  - Individual tests can override limits via `app.config`.

- Configuration keys (can be provided via app config or environment variables loaded at startup):
  - `RATELIMIT_LOGIN_LIMIT`: overrides login limit (e.g. `"5 per minute"`).
  - `RATELIMIT_REGISTER_LIMIT`: overrides register limit.
  - `RATELIMIT_REFRESH_LIMIT`: overrides refresh limit.
  - `RATELIMIT_AUTH_LIMIT`: legacy/fallback override used when endpoint-specific keys are not set.
  - `RATELIMIT_API_LIMIT`: override for general API limits.
  - `REDIS_URL`: storage backend for limiter (default `memory://` for local/testing). Example: `redis://localhost:6379/0`.

- Implementation details:
  - Limiter setup: `app/limiter.py:7–12`.
  - Dynamic endpoint limits: `app/limiter.py:33–72` (`LOGIN_LIMITS`, `REGISTER_LIMITS`, `REFRESH_LIMITS`).
  - Decorators applied in auth routes: `app/auth.py:24–26`, `app/auth.py:71–73`, `app/auth.py:200–202`.

- Error response example (HTTP 429):

```json
{
  "error": "Demasiadas peticiones",
  "message": "5 per 1 minute",
  "retry_after": 60
}
```

- Example: quickly hitting login limit

```bash
for i in $(seq 1 10); do
  curl -s -X POST http://127.0.0.1:5001/auth/login \
    -H 'Content-Type: application/json' \
    -d '{"email":"alice@example.com","password":"password1"}' | jq -r '.error';
done
```

Notes:
- For production, prefer Redis storage (`REDIS_URL`) for accurate distributed rate limiting.
- The limiter key function is the remote address (client IP).

### Recommended production configuration

- Copy `config.example.env` to `.env` and set values:

```
SECRET_KEY=change_me_in_production
FLASK_ENV=production
PORT=5001
REDIS_URL=redis://localhost:6379/0
RATELIMIT_LOGIN_LIMIT="5 per minute"
RATELIMIT_REGISTER_LIMIT="10 per hour"
RATELIMIT_REFRESH_LIMIT="20 per hour"
RATELIMIT_API_LIMIT="50 per hour"
```

- Load the `.env` before running locally:

```bash
set -a
source .env
set +a
PORT=${PORT:-5001} python3 run.py
```

## Tests

Run the test suite locally:

```bash
python3 -m pytest -q
```

CI uses GitHub Actions (see `.github/workflows/ci.yml`) to run the same tests.

## I accidentally merged/closed the PR — what to do?

If you merged and closed the PR by mistake, you have options:

- Revert the merge commit on `main` and open a fresh PR from `feature/core-api`:

```bash
# on main
git checkout main
git pull
# find the merge commit SHA then
git revert <merge-sha>
# push the revert and open a new PR if needed
```

- Or open a new PR from `feature/core-api` (already pushed). The repo shows an active PR URL if one exists. If you want me to open a new PR or prepare a revert commit, I can do that — tell me which you'd prefer.

## Notes & Security

- Seeds now store password hashes (werkzeug). Demo passwords are still plain text in the seeds file and should only be used locally.
- JWT secret is `SECRET_KEY` env var; change it in production.
- The current Maxo crediting logic is simple and should be replaced with a formal spec before public deployment.

## Demo script

There's a small demo script at `scripts/demo.sh` that walks through register/login, creating an interchange, checking balances, transferring Maxo, creating and claiming a resource, and posting a reputation review. Run the server and then:

```bash
./scripts/demo.sh
```

---

Document created by the development session on 2025-10-19.
