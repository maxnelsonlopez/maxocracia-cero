# Síntesis de Identidad del Organismo Educativo Vital (OEV)

> **Documento de Arquitectura y Memoria de Diseño**  
> **Fase:** 2 — Ola 4 "El Puente" (versión 5.6+)  
> **Área:** Rama Educativa / Identidad y Gobernanza Siamés  
> **Teoría canónica:** OEV §1.7-1.8 (`docs/theory/ESTRUCTURA_IDEAL_ORGANISMO_EDUCATIVO_VITAL.md`), Opacidad Vital (T0, T2, T13), y Reflexión Eutópica (§5.1).

---

## 1. Contexto y Problema Estructural

Hasta la culminación de los hitos educativos M1-M11, existían dos entornos aislados:
1. **Maxocracia-Cero Principal (`:5001` / Next.js)**: Base de datos central con SQLAlchemy (`users`, `participants`), autenticación por JWT (`HS256`), balances Maxo, contratos, gobernanza (`voting_bp`), matching y foros.
2. **Prototipo OEV (`plataforma_educativa/` en `:5050`)**: Servidor Flask y SQLite independiente (`plataforma_educativa.db`), Árbol de Habilidades de 8 ramas y 35 temas, tests de capacidad y planificador de reuniones semanales y mentorías.

El problema radicaba en que el participante debía mantener **dos identidades separadas** con credenciales distintas, lo que fracturaba la continuidad vital y aislaba el progreso educativo del Perfil Vital y la Escalera de Confianza (N0→N1).

---

## 2. Principios Invariantes Respetados

* **Autonomía Fractal (Invariante OEV)**: La `plataforma_educativa/` puede seguir siendo desplegada por cualquier comunidad, cooperativa o club barrial de forma aislada sin requerir la infraestructura central de Maxocracia.
* **UNA Sola Puerta (Single Door)**: Los usuarios autenticados en Maxocracia pueden interactuar con los servicios del OEV portando su JWT estándar sin necesidad de un segundo registro.
* **Opacidad Vital (T0, T2)**: El registro no impone correos obligatorios; el historial de ensayos y errores en tests educativos es privado. Solo se publican los hitos validados por triada.
* **Trazabilidad T13**: Todo evento de sincronización de maestría y mentoría genera un hash auditable en el ledger educativo (`edu_mastery_events`).

---

## 3. Arquitectura Técnica de la Síntesis

```
                     ┌──────────────────────────────────────────────┐
                     │              Frontend (Next.js)              │
                     │          (UNA sola puerta / Sesión)          │
                     └───────────────┬──────────────┬───────────────┘
                                     │              │
                       (JWT Bearer)  │              │ (JWT Bearer)
                                     ▼              ▼
     ┌───────────────────────────────────┐    ┌───────────────────────────────────┐
     │        Maxocracia (:5001)         │    │       OEV Educativo (:5050)       │
     ├───────────────────────────────────┤    ├───────────────────────────────────┤
     │ - Auth Central (JWT HS256)        │    │ - Autenticación Híbrida           │
     │ - Perfil Vital (/perfil)          │    │   * Token local en memoria        │
     │ - edu_bridge_bp.py                │    │   * JWT Maxocracia con JIT        │
     │ - Escalera N0 -> N1 por mentoría  │    │ - Tabla users (maxo_user_id)      │
     │ - edu_mastery_events (T13)        │    │ - Árbol, Tests y Células          │
     └───────────────────────────────────┘    └───────────────────────────────────┘
```

### 3.1 Flujo de Autenticación Híbrida en el OEV (`auth.py`)

Cuando el OEV recibe una petición protegida con `@login_required`:
1. **Extracción de Credenciales**: Inspecciona cabeceras `Authorization: Bearer <token>` o `X-Auth-Token`.
2. **Vía Local (Memoria)**: Si el token existe en `app.extensions["auth_tokens"]`, autentica como usuario local (`is_federated: False`).
3. **Vía Federada (JWT de Maxocracia)**:
   - Verifica la firma con la clave compartida (`SECRET_KEY`).
   - Decodifica claims: `user_id`, `email`, `is_admin`, `alias`, `name`.
   - **Aprovisionamiento JIT (Just-In-Time)**:
     - Si ya existe un usuario local con `maxo_user_id = jwt.user_id`, lo asocia de inmediato.
     - Si existe un usuario con el mismo `email`, vincula el `maxo_user_id`.
     - Si no existe, crea automáticamente el registro en la tabla `users` local, asignando rol de coordinador si `is_admin: 1`.
   - Establece `g.user_id` (ID local), `g.maxo_user_id` (ID central) y `g.is_federated: True`.

### 3.2 Puente Bidireccional (`app/edu_bridge_bp.py`)

En el sistema central (`:5001`):
* `GET /edu-bridge/status`: Reporta conectividad y estado de identidad unificada.
* `POST /edu-bridge/sync-mastery`: Recibe la culminación de un tema o ronda de mentoría aprobada por triada **reportada por el nodo OEV con su token de servicio** (`X-Edu-Bridge-Token`, env `EDU_BRIDGE_SERVICE_TOKEN`; sin él, fail-closed 403). El evento queda como **evidencia** T13 (SHA-256) del Perfil Vital.
* `GET /edu-bridge/events`: Expone el historial T13 de logros educativos.

> **Corrección de gobernanza (29-08-2026, revisión del orquestador):** la v1 de este
> endpoint permitía que CUALQUIER usuario autenticado declarara su propia maestría
> (`triada_approved=true`) y se promoviera N0→N1 con un único POST — la escalera de
> confianza se compraba con un request. Corregido: (1) procedencia exigida (token de
> servicio del nodo, comparación en tiempo constante); (2) **sin auto-promoción**:
> la escalera N0→N1 sigue siendo asunto del primer acuerdo (Cap. 13); el evento
> educativo es evidencia y el peso de la formación en la voz queda como candidato a
> decisión de parlamento (RF-EDU-16 candidato); (3) `t13_hash` real (SHA-256 del
> evento, antes una cadena predecible); (4) `SECRET_KEY` de la plataforma sin
> constante pública por defecto (fail-closed 503 si no está configurada).

---

## 4. Pruebas y Validación

La implementación cuenta con validación completa:
1. **Plataforma Educativa (`plataforma_educativa/tests/`)**:
   - `test_jwt_auth.py`: Pruebas de token Bearer, X-Auth-Token, aprovisionamiento JIT, enlace por email, tokens expirados/corruptos y convivencia con tokens locales (39/39 tests en verde).
2. **Backend Principal (`tests/`)**:
   - `test_edu_bridge.py`: Pruebas de estado, sincronización de maestría, promoción de confianza N0→N1 y registro de eventos T13.
3. **Frontend**:
   - Compilación limpia con `tsc --noEmit`.
