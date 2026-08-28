# Mapa del Frontend — Ola 4 (M4)

Mapa completo del frontend Next.js: páginas → endpoints consumidos → blueprints del backend, **incluyendo
las secciones desconectadas**. Generado el 11-08-2026 con verificación determinista (grep de `apiFetch`/
`fetch`/`api.*` sobre `frontend/app`, cruzado con el inventario de 182 rutas de `mapa_coherencia_ola4.md` §2).

**Stack**: Next.js App Router, `frontend/app/lib/api.ts` como hub (`apiFetch` con Bearer token;
`API_URL` → localhost:5001 en dev). 34 páginas, ~15k líneas de UI.

## 1. Páginas conectadas (página → API consumida)

| Ruta | Líneas | Endpoints consumidos | Blueprint |
|---|---|---|---|
| `/` (landing) | 32 | `/contracts/`, `/contracts/stats`, `/contracts/negotiate`, `/contracts/negotiate/feedback`, `/forms/exchange`, `/forms/follow-up`, `/forms/matching/me`, `/forms/matching/gaps`, `/forms/dashboard/*`, `/forms/pulse`, `/subscriptions/my-subscription`, `/users`, `/parties`, `/auth/*` | contracts, forms, subscriptions, users, parties, auth |
| `/contracts` | 428 | `/contracts/`, `/contracts/cohort` | contracts |
| `/contracts/builder` | 1270 | `/contracts/`, `/contracts/validate_graph`, `/parties`, `/parties/`, `/users` | contracts, parties, users |
| `/contracts/negotiate` | 5+client | `/contracts/negotiate`, `/contracts/negotiate/feedback`, `/contracts/` | contracts |
| `/contracts/:id` | 12+client | `/contracts/{id}`, `/checkin`, `/witness`, `/terms/{id}/fulfillment`, `/finalize`, `/civil`, `/tree`, `/accept`, `/activate`, `/participants`, `/retract` | contracts (ciclo de vida completo) |
| `/forms/cero` | 304 | `/forms/participant` | forms |
| `/forms/exchange` | 413 | `/forms/exchange` | forms |
| `/forms/follow-up` | 406 | `/forms/follow-up` | forms |
| `/matching` | 2118 | `/forms/exchange`, `/forms/matching/me`, `/forms/matching/gaps`, `/forms/matching/urgent`, `/forms/oracle/chat`, `/contracts/from-need` | forms + oráculo + bridge_b |
| `/micromax` | 1553 | `/api/micromax/*` (household, join, config, cdd, safety-survey, audit, audits, dashboard) | micromax (hub completo) |
| `/pulso` | 1036 | `/forms/pulse` | forms |
| `/vhv/calculator` | 210 | `/vhv/calculate`, `/vhv/case-studies` | vhv |
| `/vhv/comparison` | 157 | `/vhv/products` | vhv |
| `/vhv/parameters` | 209 | `/vhv/parameters` (GET/PUT) | vhv |
| `/tvi/stats` | 204 | `/tvi/stats`, `/tvi/community-stats` | tvi |
| `/login` · `/register` | 127/158 | `/auth/login`, `/auth/register` (+`/auth/me`, `/auth/logout` vía AuthContext) | auth |
| `/perfil` | 660 | `/maxo/{id}/balance`, `/maxo/{id}/ledger`, `/maxo/transfer`, `/protection/profile`, `/reputation/{id}`, `/resources`, `/resources/{id}/claim`, `/interchanges` | maxo, protection, reputation, resources, interchanges |
| `/upgrade` | 24+client | `/stripe/config`, `/stripe/create-checkout-session` | stripe |
| `/transparency` | 12+client | `/subscriptions/transparency-report` | subscriptions |
| `/verificador` | 12+client | `/verificador/cohort` | verifier |
| `/guia` | 552 | `/guide/chat`, `/guide/trust-assessment`, `/guide/director-candidacy` | guide |
| `/foro` | ~340 | `/forum/posts` (GET/POST), `/forum/posts/{id}`, `/forum/posts/{id}/close`, `/forum/needs` | forum (rama educativa M2) |
| `/talleres` | ~400 | `/workshops` (GET/POST), `/workshops/{id}`, `/enroll`, `/outputs`, `/grant-skill`, `/close` | workshops + motor de vacuación (M3) |
| `/grupos` | ~330 | `/groups` (GET/POST), `/groups/{id}`, `/join`, `/child`, `/close` | groups — ECEs + Células Madre (M4) |
| `/admin/contracts` | 620 | `/contracts/`, `/contracts/stats` | contracts |
| `/admin/dashboard` | 276 | `/forms/dashboard/alerts|stats|trends`, `/subscriptions/admin/stats` | forms, subscriptions |
| `/admin/matching` | 529 | `/forms/matching/gaps`, `/forms/matching/urgent` | forms |
| `/admin/network` | 225 | `/forms/dashboard/network` | forms |
| `/admin/reports` | 250 | `/forms/dashboard/categories`, `/forms/dashboard/resolution` | forms |
| `/admin/sdv` | 276 | `/forms/participants?limit=50`, `/forms/sdv/community` | forms |
| `/admin/users` | 279 | `/subscriptions/admin/users`, `/subscriptions/activate-manual` | subscriptions |
| `/admin/participants` | 849 | `/forms/participants`, `/forms/participants/{id}` (GET/POST/DELETE) | forms |
| `/admin/synthetic-sessions` | panel nuevo | `/api/synthetic-sessions`, `/<session_id>`, `/<session_id>/run`, `/review`, `/revoke`, `/audit` | synthetic_sessions |

## 2. Páginas sin conexión a API (contenido / estáticas)

| Ruta | Tipo | Nota |
|---|---|---|
| `/participar` | Informativa | Escalera de participación (lectura en voz alta), sin API — intencional |
| `/privacy` · `/terms` | Informativas | Textos legales estáticos |
| `/admin/settings` | ⚠️ UI local | Pesos axiomáticos en `useState`; **no persisten** — `api.ts` ya expone `/vhv/parameters` PUT |
| `/admin/subscriptions` | ⚠️ MOCK | Transacciones simuladas hardcodeadas; backend `/subscriptions/admin/*` real sin usar |

## 3. Backend sin consumidor en el frontend (secciones desconectadas)

| Endpoints backend | Blueprint | Estado |
|---|---|---|
| `/maxo/{id}/balance`, `/maxo/{id}/ledger`, `/maxo/transfer` | maxo | ✅ Conectado (`/perfil` — RF-G5, ago 2026) |
| `/protection/profile` | protection | ✅ Conectado (`/perfil` — RF-G5, ago 2026) |
| `/reputation/{id}` | reputation | ✅ Conectado (`/perfil` — RF-G5, ago 2026) |
| `/resources` (GET/POST) y `/resources/{id}/claim` | resources | ✅ Conectado (`/perfil` — RF-G5, ago 2026) |
| `/interchanges` (GET) | interchanges | ✅ Conectado (`/perfil` — RF-G5, ago 2026; `POST` y `create_interchange` siguen sin UI, se usa el blueprint forms) |
| `/contracts/from-need`, `/contracts/from-need/...` (3) | bridge_b | ✅ Conectado (ago 2026): botón "Contrato Ético" en cada necesidad del Muro de `/matching` → borrador DRAFT → `/contracts/{id}`; maneja NEED_PARTICIPANT_UNLINKED (invitación) y DRAFT_REJECTED (AVA) |
| `/tvi` (raíz), `/vhv` (raíz) | tvi, vhv | 🟡 Solo existen páginas hijas (`/tvi/stats`, `/vhv/calculator`) |
| `/admin/user`, `/admin/interchange`, `/admin/followup`, `/admin/vhvproduct` (CRUD 9 c/u) | Flask-Admin | 🔴 CRUD solo parcialmente expuesto: `/admin/participants` usa `/forms/participants` (no `/admin/participant`); el resto sin página |

## 4. Hallazgos y recomendaciones (por prioridad)

1. **Conectar `/admin/settings`** a `/vhv/parameters` (PUT) — ✅ HECHO (ago 2026): pesos persistidos con nota auditable T13.
2. **Reemplazar el MOCK de `/admin/subscriptions`** — ✅ HECHO (ago 2026): KPIs y tabla reales vía `/subscriptions/admin/*`.
3. **SDV-S en UI** — ✅ **ya existía**: el panel "Reino Sintético · SDV-S" está en `ContractDetailsClient.tsx`
   (dimensiones, FS_S = e^v, violaciones, badge de dignidad). *Corrección M4: la primera versión de este
   mapa lo marcó pendiente porque el script de rastreo solo detectaba llamadas API directas, no datos
   renderizados desde `participants_details` del contrato.*
4. **Exponer el CRUD real** (Flask-Admin): decidir entre generar páginas para interchange/followup/vhvproduct
   o migrar `/admin/participants` al CRUD `/admin/participant` (hoy usa `/forms/participants`).
5. **Superficies sin UI**: ✅ **CERRADO (ago 2026, RF-G5)**: página `/perfil` (Perfil Vital) consume
   `/maxo/{id}/balance` + `/maxo/{id}/ledger` (endpoint nuevo, T13) + transferencia, `/protection/profile`
   (nivel efectivo + caps + declaración), `/reputation/{id}`, `/resources` (listar/crear/reclamar) e
   `/interchanges` filtrado por usuario. Enlace en Navigation (desktop + móvil).
6. **`/contracts/from-need`**: ✅ CERRADO (ago 2026, M4 fase 2): el Muro de Necesidades de `/matching`
   tiene ahora el botón "Contrato Ético" que llama al bridge (`POST /contracts/from-need`), navega al
   borrador al éxito y muestra la invitación (NEED_PARTICIPANT_UNLINKED) o las violaciones AVA
   (DRAFT_REJECTED) en la propia tarjeta.

## 5. Verificación (cómo se regeneró este mapa)

```powershell
# 1. Páginas:
Get-ChildItem frontend\app -Recurse -Filter "page.tsx"
# 2. Endpoints consumidos (página + client components colindantes):
Get-ChildItem frontend\app -Recurse -Include "*.tsx","*.ts" | Select-String -Pattern "apiFetch\(|fetch\(|api\."
# 3. Hub de API:
Get-Content frontend\app\lib\api.ts
# 4. Cruzar con el inventario de 182 rutas del backend (mapa_coherencia_ola4.md §2)
```

---
**Última actualización**: 19-08-2026 · **Método**: RLM + verificación determinista (Patrón Puente)
