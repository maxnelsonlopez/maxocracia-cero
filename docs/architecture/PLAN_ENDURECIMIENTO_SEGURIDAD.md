# Plan de Endurecimiento de Seguridad — Maxocracia-Cero

**Fecha:** 02 de septiembre de 2026
**Estado:** VIVO — ejecutada la fase inmediata (0-30 días); el mediano plazo (30-90 días) queda como roadmap con notas concretas para este repo.
**Origen:** metas de seguridad dictadas por GLM (interfaz web, sep 2026), ejecutadas y verificadas contra el código real en sesión con Max.
**Principio:** la seguridad sirve a la coherencia — la Opacidad Sagrada (T13) y la escalera de confianza (Cap. 13) solo valen si los datos que protegen no se pueden forjar ni filtrar.

---

## 1. Qué ya existía (verificado en código, sep 2026)

El plan genérico asumía gaps que el repo ya tenía cubiertos. Se verificó línea por línea:

| Control | Estado | Dónde |
|---|---|---|
| Rate limiting | ✅ Flask-Limiter con límites por endpoint (login 3/min, registro 10/h, refresh 20/h, API 60/min) + handler 429 + overrides por env | `app/limiter.py` |
| Cabeceras de seguridad | ✅ CSP, HSTS (solo sobre HTTPS), X-Content-Type-Options, X-Frame-Options DENY, Referrer-Policy, no-cache | `app/__init__.py::add_security_headers` |
| CORS restringido | ✅ Solo localhost:3000 + `FRONTEND_URL` | `app/__init__.py` |
| Secretos fuera de git | ✅ `.env` en `.gitignore` (línea 131) y sin trackear; `config.example.env` solo placeholders | raíz del repo |
| JWT con firma gestionada | ✅ `jwt_utils.get_secure_key()`: fail-closed en producción, clave aleatoria en desarrollo | `app/jwt_utils.py` |
| Plataforma educativa fail-closed | ✅ `SECRET_KEY` sin constante pública (503 si falta), token de servicio del puente fail-closed 403 | M12, `plataforma_educativa/app/` |

## 2. Ejecutado en esta jornada (0-30 días)

### 2.1 Auditoría de dependencias

- **npm audit (frontend)**: 4 vulnerabilidades **high** en `next@16.1.6` (SSRF en Server Actions, DoS, cache confusion, disclosure de endpoints internos) + `postcss` y `sharp` heredados. **Fix aplicado: `next@16.3.4`** (fuera del rango declarado — verificado con `tsc --noEmit` y build).
- **pip-audit (backend)**: PYSECs en PyJWT (múltiples, incluyendo claves HMAC cortas), Werkzeug, Flask-CORS, idna, requests, urllib3, python-dotenv. **Pins actualizados** en `requirements.txt`:
  - PyJWT 2.10.1 → **2.13.0** (crítico: firma de todos los JWT)
  - Werkzeug 3.1.3 → **3.1.6** · Flask-CORS 5.0.0 → **6.0.0**
  - idna 3.11 → 3.15 · requests 2.32.5 → 2.33.0 · urllib3 2.5.0 → 2.6.3 · python-dotenv 1.2.1 → 1.2.2
- **PyJWT 2.13 ahora advierte claves HMAC < 32 bytes** (RFC 7518 §3.2): las claves de test y el fallback de desarrollo se alargaron a 32+ bytes y la suite quedó sin warnings.
- **Snyk**: no ejecutado (requiere cuenta/token); `npm audit` + `pip-audit` cubren el mismo terreno. Queda como opción si Max crea cuenta.
- Script de auditoría recurrente: `scripts/security_audit.ps1` (npm audit + pip-audit en un comando).

### 2.2 Cadena de secretos fail-closed

Hallazgo real (la vulnerabilidad más seria de la jornada): si se desplegaba con `FLASK_ENV=production` sin `SECRET_KEY`, `run.py` forzaba una clave **conocida y hardcodeada** y el servidor arrancaba así — con ella se firman JWTs (`jwt_utils`) e invitaciones (`arrivals._secret`), o sea: **escalera de confianza comprable**.

- `run.py`: en producción sin `SECRET_KEY` → **aborta con error claro** (fail-closed). El fallback de desarrollo se conserva (es deliberado, documentado) pero con clave de 32+ bytes.
- `app/create_app()`: mismo guard en la factory — protege despliegues WSGI que no pasan por `run.py` (waitress directo, gunicorn, etc.).
- `config.example.env`: documentado el requisito de 32+ bytes (`openssl rand -hex 32`) y la variable nueva `FORCE_HTTPS`.

### 2.3 HTTPS y CSP de producción

- **`FORCE_HTTPS=1`** (opt-in): toda petición que llega con `X-Forwarded-Proto: http` se redirige **308** a https. El TLS real lo termina el proxy inverso (waitress no habla TLS) — documentado en §4.
- **CSP sin WebSocket de localhost en producción**: `ws://localhost:*` solo se anuncia fuera de producción (HMR de Next en dev); en producción la exportación estática no lo necesita.

### 2.4 Tests y verificación

- **`tests/test_security_hardening.py`** — 9 tests: fail-closed en producción (factory), fallback de dev intacto, longitud del fallback, redirección 308 (on/off/https-entrante), CSP prod vs dev, HSTS.
- Suite raíz completa en verde tras los cambios (ver handoff para el número exacto de la jornada).
- Auth smoke test primero (14/14), suite completa después.

## 3. Roadmap mediano plazo (30-90 días) — notas para este repo

Cada ítem merece su propia sesión con la cultura del repo (teoría primero, tests, commits en español).

1. **SQLite → PostgreSQL con cifrado**: `config.example.env` ya contempla `DATABASE_URL=postgresql://...`; SQLAlchemy lo hace directo. Lo no trivial: migrar `comun.db` (datos de la Cohorte Cero), los `init_*_tables` con SQL idempotente dialecto-SQLite (CHECK, INSERT OR IGNORE → ON CONFLICT), y la plataforma educativa (su propio schema). Decisión canónica pendiente: ¿la vida contable cifrada en reposo con cifrado a nivel de disco (BitLocker) o a nivel de campo? T13 sugiere campo a campo para lo sensible.
2. **Cache Redis con TTL**: Flask-Limiter ya soporta `storage_uri=redis://` (hoy `memory://` — los límites se reinician por proceso; en multi-worker real se necesitan Redis). Redis ya está en `requirements.txt`. TTL según dominio: sesiones cortas, ledger largo.
3. **API Gateway con autenticación centralizada**: hoy cada blueprint usa `token_required`/`admin_required` de `jwt_utils` — la autenticación YA es central; el gateway añadiría TLS, WAF y rate limiting perimetral. Recomendación: Caddy/nginx + `FORCE_HTTPS=1` antes de un gateway pesado.
4. **Logging estructurado JSON sin información sensible**: los logs actuales son prints de desarrollo. Nunca loguear: tokens, γ verdadero de protegidos (Modo Escudo, §16.5.12), contenido de ESI, hashes T13 con datos personales. El T13 ya es la evidencia — loguear su hash, no su contenido.
5. **SAST**: integrar `bandit` (Python) y `npm audit --audit-level=high` en CI. El validador conceptual (`scripts/validador_conceptual.py`) ya es una forma de SAST axiomático — mantenerlo en verde.
6. **Pentesting anual y bug bounty**: para la fase de comunidad real. El bug bounty puede pagarse en Maxo (coherente con el Mantenimiento Óptimo, Cap. 17.4) — decisión del parlamento, no de un agente.
7. **Gestor de secretos (Vault/AWS SM)**: cuando haya despliegue real multi-nodo (:5001 + :5050 federados). Hoy: `.env` fuera de git + rotación manual documentada (§5) es suficiente y verificable.
8. **Rotación pendiente menor**: pytest 8.4.2 → 9.x (PYSEC-2026-1845, solo dev; el salto mayor puede romper plugins pytest-env/pytest-cov — probar en sesión aparte).

## 4. Configuración de producción recomendada (receta)

```env
FLASK_ENV=production
SECRET_KEY=<openssl rand -hex 32>        # obligatoria: fail-closed si falta
JWT_SECRET_KEY=<openssl rand -hex 32>    # distinta de SECRET_KEY
FORCE_HTTPS=1                            # detrás de proxy TLS (Caddy/nginx)
FRONTEND_URL=https://tu-dominio.org
RATELIMIT_STORAGE_URI=redis://localhost:6379/0   # cuando haya multi-worker
```

El proxy inverso termina TLS y pasa `X-Forwarded-Proto: https`; Flask redirige y emite HSTS.

## 5. Procedimiento de rotación de claves

1. Generar clave nueva (`openssl rand -hex 32`), 32+ bytes.
2. Actualizar `SECRET_KEY` en el entorno del nodo y reiniciar. Efecto: los JWT existentes dejan de validar (los usuarios vuelven a hacer login) y las invitaciones firmadas con la clave vieja se invalidan — reemitir con `POST /invite`.
3. Los refresh tokens viven en `refresh_tokens` (BD) con jti propio — sobreviven si su verificación no depende de la SECRET_KEY; verificar en el momento de rotar.
4. Rotar cuando: se sospeche filtración, cada 90 días en producción, o al rotar personal con acceso al servidor.
5. La rotación se registra como evidencia T13 en la bitácora del nodo (hash de la decisión, nunca la clave).

---

*Verificado con la suite completa y el validador conceptual antes de commitear. Atribuciones de la jornada en `docs/architecture/atribuciones_sinteticas.md`.*
