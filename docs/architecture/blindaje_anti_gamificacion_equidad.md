# Blindaje Anti-Gamificación y Equidad Vital

**Autor del diseño:** DeepSeek (oráculo sintético) y Max Nelson López Restrepo
**Fecha:** 6 de agosto de 2026
**Estado:** Ola 3A **IMPLEMENTADA** (identidad vinculada al token, inmutabilidad, autoridad de partes, T9 ejecutable, γ con fuente, prohibiciones léxicas, ventanas temporales). Ola 3B **IMPLEMENTADA** (escalera de equidad: perfiles standard/assisted/shielded, paráfrasis obligatoria, revisión oracular sin degradación, co-testigo, topes de exposición, piso de reflexión, lectura en voz alta — 538/538 tests). Pendiente: Ola 3C (ejecución mínima con dientes).
**Referencia canónica:** Cap. 17 (MaxoContracts), Cap. 10 (Tres Reinos), Axioma T11/T12 (retractación coherente), INV1/INV2/INV2-S/T9/T13

---

## 1. Advertencia preliminar

Este documento responde a dos preguntas del fundador:

1. **¿Qué pasaría si los mejores abogados del mundo quisieran sacar provecho inadecuado de los límites o restricciones de los MaxoContracts actuales?**
2. **¿Qué nos faltaría implementar para que las personas más vulnerables (y quizás ignorantes) también tengan contratos dignos?**

Cada riesgo fue **verificado contra el código actual** (referencias `archivo:línea`). No son hipótesis teóricas: son vectores reproducibles hoy.

---

## 2. Mapa de riesgo actual (cómo se explota HOY)

### 2.1 Riesgos de identidad e integridad (los más graves)

| ID | Riesgo | Vector de explotación | Severidad |
|---|---|---|---|
| **R1** | **Firma por suplantación** | `POST /contracts/<id>/accept` toma `user_id`/`delegate_id` del **cuerpo de la petición**, no del token JWT (`app/contracts_bp.py:1435-1450`). Cualquier usuario autenticado puede firmar **como cualquier participante** (humano, sintético o delegado de una cooperativa). Un abogado podría fabricar el consentimiento completo de un contrato. | 🔴 CRÍTICA |
| **R2** | **Reescritura de contratos existentes** | `_save_contract` es un **upsert** (`ON CONFLICT(contract_id) DO UPDATE SET civil_description, state, ...` en `app/contracts_bp.py:265-280`). `POST /contracts/` con un `contract_id` ya existente **reinicia el estado a DRAFT y sobreescribe la descripción y los términos**. Un contrato ACTIVO puede ser "borrado" por cualquiera re-creándolo. No existe `creator_user_id`. | 🔴 CRÍTICA |
| **R3** | **Secuestro de gobernanza colectiva** | `PUT /parties/<id>` (`app/parties_bp.py:update_party`) no verifica **autoridad**: cualquier usuario autenticado puede reemplazar los delegados/pesos/quórum de una cooperativa ajena y luego firmar contratos en su nombre. | 🔴 CRÍTICA |
| **R4** | **Partes fantasma** | `POST /parties/` crea cualquier parte (`coop-*`, `org-*`, `eco-*`) sin verificar que el creador tenga autoridad sobre esa entidad. Un abogado crea "Cooperativa X" consigo mismo como único delegado (quórum 1.0) y contrata "en nombre de" una entidad que no existe o no le pertenece. | 🟠 ALTA |
| **R5** | **γ auto-reportado sin fuente** | `wellness`/`gamma` viajan en el cuerpo de la petición (`_apply_wellness`, `add_participant`). Cualquiera puede declarar γ=1.5 (verse sano) o γ=0.4 (activar alertas de otro). No hay serie temporal, ni actor, ni vínculo con los datos reales (follow-ups del dominio de formularios). INV1/INV2 se calculan sobre datos falsificables. | 🟠 ALTA |

### 2.2 Riesgos de contenido y axiomas

| ID | Riesgo | Vector | Severidad |
|---|---|---|---|
| **R6** | **T9 (Reciprocidad Justa) NO se valida en el backend de creación** | `AxiomValidator.validate_all` (`maxocontracts/core/axioms.py:254-289`) solo valida T1, T13, INV1, INV2, INV2-S e INV4. **No llama a `validate_exchange`/T9**. Un contrato 100% unilateral (solo "A debe 1000 horas a B", sin contraprestación) **pasa la validación y se activa**. El oráculo en vivo sí computa `reciprocity_balance` con tolerancia, pero la API REST no bloquea. El propio demo `demo-intercambio-10h` es asimétrico (10h vs 3h) — la asimetría necesita **tolerancia explícita y declarada**, no ausencia de chequeo. | 🟠 ALTA |
| **R7** | **Cláusulas punitivas no prohibidas** | El UI ya modela "Penalización γ (-0.2)" en los nodos. Nada impide una cláusula "si te retractas, debes 1000 horas" — **penalizar la retractación viola T11/T12** (retractación coherente y sin jaulas). INV4 está **hardcodeado a True** (`axioms.py:286`): el sistema asume retractabilidad, pero no impide que un término la anule de facto. | 🟠 ALTA |
| **R8** | **Lenguaje civil no enforceable** | El prompt del oráculo pide ≤20 palabras/frase en grado 8º, pero la API **no valida** `civil_text` (ni longitud, ni complejidad, ni léxico). Un abogado puede enterrar trampas en legalese; la "traducción civil" es convención, no garantía. | 🟡 MEDIA |
| **R9** | **Términos sin parte obligada** | `assigned_participant` es opcional (columna nullable). Obligaciones "fantasma" sin responsable pasan validación. | 🟡 MEDIA |

### 2.3 Riesgos de proceso y ejecución

| ID | Riesgo | Vector | Severidad |
|---|---|---|---|
| **R10** | **Sin ventana de firma por contrato** | El deadline de quórum existe solo para partes colectivas. Un contrato puede crearse, firmarse y activarse en segundos, sin periodo de reflexión ni caducidad de la oferta. | 🟡 MEDIA |
| **R11** | **Enfriamiento solo client-side** | El temporizador de la firma rigurosa (10s) vive en el navegador (`ContractDetailsClient.tsx`); no hay mínimos server-side. | 🟡 MEDIA |
| **R12** | **Sin dientes: la autoejecución es declarativa** | El estado `executed` existe en el esquema y el UI promete "penalizaciones automáticas", pero **no hay código que ejecute consecuencias**: el incumplimiento solo alimenta métricas. Un abogado explota la brecha entre el reclamo ("vigilancia axiomática en tiempo real") y la realidad (monitoreo pasivo + retractación mediada por humanos). | 🟠 ALTA |
| **R13** | **Guardián eco con heurística laxa** | Sin `DEEPSEEK_API_KEY`, el guardián del Reino Natural aprueba si los invariantes pasan — y con R6, eso incluye contratos unilaterales. | 🟡 MEDIA |
| **R14** | **Spam de métricas** | NPS y eventos aceptan identidad arbitraria (R1 aplica); las métricas del dashboard pueden contaminarse. | 🟢 BAJA |

### 2.4 Resumen ejecutivo del riesgo

> **Hoy, el "mejor abogado del mundo" no necesita trucos sofisticados:**
> 1. Se autentica con su cuenta (R1) y firma él mismo **todos** los términos de un contrato que solo lo obliga a él… o que obliga a otros sin su consentimiento.
> 2. Crea una parte fantasma (R4) o secuestra una real (R3) y contrata "en nombre de" una cooperativa.
> 3. Redacta cláusulas unilaterales (R6), punitivas (R7) y en legalese (R8) que **pasan validación**.
> 4. Si el contrato no le conviene, lo re-crea para resetearlo a borrador (R2).
>
> **La defensa del sistema no es el código, es la buena fe de los participantes.** Eso hay que cambiarlo.

---

## 3. Ola 3A — Blindaje mínimo (rápido, alta prioridad)

Fixes que cierran los agujeros críticos sin rediseñar el core. Cada uno con criterio de salida verificable.

### 3A.1 Identidad vinculada al token (R1, R4, R14)
- `accept`/`delegate`/`retract`/`nps`: el actor **siempre** deriva del token (`current_user.user_id`).
  - Firma humana: solo `user-{token_uid}` puede firmar por sí mismo.
  - Firma delegada: `delegate_id` explícito SOLO si es `user-{token_uid}` (los delegados siempre son humanos reales).
  - Sintéticos: requieren el flujo oracular (ver 3A.6) o un `actor_id` registrado.
- **Compatibilidad**: los tests existentes que firman "por" varios usuarios deberán crear tokens por usuario (patrón ya usado en `test_parties_escalas`).
- **Criterio de salida**: test de regresión — firmar como `user-2` con token de `user-1` → 403.

### 3A.2 Inmutabilidad de contratos (R2)
- Columna `creator_user_id` en `maxo_contracts` (migración automática) + `created_by` en el evento.
- `POST /contracts/` con `contract_id` existente:
  - Si el contrato es DRAFT del mismo creador → actualización legítima (upsert actual).
  - Cualquier otro caso → **409 CONFLICT**.
- Auditoría: cada mutación API registra `actor_id` en `maxo_contract_events`.
- **Criterio de salida**: re-crear un contrato ACTIVO ajeno → 409; re-crear el propio DRAFT → 200.

### 3A.3 Autoridad sobre las partes (R3, R4)
- `maxo_parties.owner_user_id` (migración automática; `user-*` del creador).
- `PUT /parties/<id>` y cambios de `members_json`:
  - Requieren token del owner, **o** aprobación por quórum de los delegados actuales (endpoint `POST /parties/<id>/governance-change` que registra votos en `maxo_contract_delegate_approvals`-style).
- Todo cambio de gobernanza se registra con actor y razón (T13).
- `POST /parties/` para colectivas: requiere `display_name` + declaración de autoridad (campo `authority_declared_by`); la verificación real (registro mercantil, acta) queda marcada `verified: false` hasta proceso humano.
- **Criterio de salida**: modificar delegados ajenos → 403; quórum de delegados puede aprobar el cambio.

### 3A.4 T9 ejecutable con tolerancia declarada (R6)
- Añadir al core `T9ValidatorBlock`-style: balance entre el VHV total asignado a cada parte (DO vs GIVE).
- Modo estricto (por defecto en creación API): asimetría total del contrato > umbral (p. ej. ratio 3:1 o delta > 5h) → **rechazo**, salvo:
  - `asymmetry_acknowledged: true` firmado por **ambas** partes + aval de un tercero (humano u oráculo en vivo).
- El demo `10h vs 3h` se ajusta al umbral o se migra al flujo de asimetría declarada (el oráculo ya la declara en `reasoning`).
- **Compatibilidad**: `validate_graph` y el oráculo siguen funcionando; el chequeo vive en `_load_contract`/`submit_for_acceptance` (core puro) o en la capa API.
- **Criterio de salida**: contrato unilateral rechazado; asimétrico con declaración aceptado y registrado.

### 3A.5 γ con fuente (R5)
- `maxo_contract_participants` + columnas `reported_by` (actor) y `reported_at` (serie en `maxo_contract_events`).
- Topes defensivos: γ ∈ [0.5, 1.5] (fuera → 400).
- Integración opcional con `follow_ups` del dominio de formularios (bienestar real reportado) — primera versión: solo registrar actor/timestamp.
- **Criterio de salida**: γ=2.0 → 400; cambio de γ registrado con actor.

### 3A.6 Prohibiciones léxicas y estructurales (R7, R8, R9)
- Servidor: bloqueo léxico de patrones explotativos: renuncia a retractación, renovación automática, exclusividad forzosa, penalización por retractarse, cesión no consentida de SDV.
- Lenguaje civil enforceable: `civil_text` ≤ 40 palabras y ≤ 2 oraciones; detector de "frases trampa" (jerga jurídica, porcentajes complejos, anidamiento) → bandera `needs_oracle_review`.
- `assigned_participant` **obligatorio** para contratos con peso ≥ medio (y siempre recomendado).
- **Criterio de salida**: cláusula "sin derecho a retractación" → 400; texto de 200 palabras → 400.

### 3A.7 Ventanas temporales (R10, R11)
- `signature_deadline` por contrato (ISO, configurable) y **enfriamiento server-side**: `min_reflection_hours` entre creación y primera firma (por defecto 0 para contratos simples; ≥ 24h si hay perfil vulnerable o asimetría declarada).
- **Criterio de salida**: firma antes del enfriamiento → 423 LOCKED.

---

## 4. Ola 3B — Equidad: la escalera de salvaguardas

Objetivo: **la dignidad no puede depender de la astucia ni de la escolaridad.** Las personas vulnerables reciben protección creciente y verificable.

### 4.1 Perfil de vulnerabilidad
Fuentes (integración con el dominio existente de formularios):
- Edad (menores protegidos: no contratan sin tutor-aval; mayores con cuidados).
- Escolaridad declarada baja.
- Necesidades activas registradas (`participant_needs`).
- Primera vez en la plataforma (sin historial de contratos).
- Bandera manual de acompañante (trabajador social, cuidador).

El perfil se computa server-side (`vulnerability_score(uid) -> 0..1`) y se expone como `protection_level: standard | assisted | shielded`.

### 4.2 La escalera (protección progresiva)

| Protección | standard | assisted | shielded |
|---|---|---|---|
| Paráfrasis oracular obligatoria por término | ✗ | ✓ | ✓ |
| Firma asistida (cada término leído en voz civil antes de aceptar) | ✗ | ✓ | ✓ |
| Co-testigo humano obligatorio (aval `user-*` ajeno a las partes) | ✗ | ✗ | ✓ |
| Enfriamiento server-side | 0h | 24h | 72h |
| Tope de exposición VHV (T total por contrato) | — | 20h | 8h |
| Tope semanal de TVI contratado | — | 40h | 15h |
| Revisión oracular pre-firma obligatoria | ✗ | ✓ | ✓ |
| **Si el oráculo no está disponible** | degradación normal | bloqueo de firma | bloqueo de creación |
| Aviso de asimetría (T9) con lectura forzada | ✓ | ✓ | ✓ |
| Registro de decisiones (qué se entendió, qué se aceptó) | ✓ | ✓ | ✓ |

> **Principio clave**: la degradación elegante (sin API key → oráculo heurístico) es aceptable para perfiles standard, pero **prohibida para assisted/shielded**: un vulnerable no firma sin paráfrasis oracular real. La equidad no se negocia con el presupuesto.

### 4.3 Derecho a la comprensión (R8 profundizado)
- Todo término tiene su **traducción civil** verificable en la respuesta del detalle (ya existe `civil`): se vuelve **contrato** (campo `civil_text` YA es civil; el problema es que no se verifica).
- Para assisted/shielded: la aceptación registra el hash de la paráfrasis oracular que leyó (`paraphrase_hash` en `maxo_contract_term_approvals`).
- Si el peso del contrato es "riguroso", la firma exige la pregunta de comprensión por término (hoy existe solo client-side; se server-side).

### 4.4 Contratos para analfabetas funcionales
- Audio: endpoint `GET /contracts/<id>/audio` (TTS server-side o client-side con `speechSynthesis`) que lee cada término en civil.
- "Firma" con confirmación oral registrada como evento con actor y timestamp.
- El co-testigo del perfil shielded **valida la lectura** (`witness_reads_aloud: true`).

---

## 5. Ola 3C — Dientes: ejecución mínima (diseño)

Cierra la brecha del reclamo vs la realidad (R12), respetando la filosofía no-coercitiva:

1. **Penalizaciones γ ejecutables**: cuando un término con `penalty` vence sin cumplirse → el sistema actualiza γ del incumplidor (actor: oráculo, `reported_by=oracle`), dispara evento `contract.violation`, y si γ < 0.8 habilita retractación automática (INV1).
2. **Estado executed**: al vencerse todos los términos → `executed` con balance VHV final.
3. **Bitácora de cumplimiento** por término (`maxo_contract_term_fulfillments`): cumplido/incumplido/parcial con actor.
4. La retractación sigue siendo mediada por el oráculo (nada de jaulas); la penalización de retractación está **prohibida** (3A.6).
5. La ejecución es **transparente y apelable**: todo evento tiene actor; el oráculo en vivo audita disputas.

---

## 6. Plan de verificación (cada ola)

- **Tests de seguridad** (`tests/test_maxocontracts/test_blindaje.py`): suplantación → 403; re-escritura ajena → 409; takeover de parte → 403; unilateral → rechazo; cláusula prohibida → 400; enfriamiento → 423; γ fuera de rango → 400; perfil shielded sin oráculo → bloqueo.
- **Regresión**: suite completa + `tsc --noEmit` + build exportado; el seed demo (10h vs 3h) se ajusta al umbral T9 o al flujo de asimetría declarada.
- **Hackathon interno de ataque**: intentar cada vector del §2 contra la build post-blindaje.

## 7. Prioridad sugerida

| Orden | Ola | Impacto | Esfuerzo |
|---|---|---|---|
| 1 | 3A.1 Identidad vinculada | 🔴 Cierra R1/R14 | Bajo (endpoints + tests) |
| 2 | 3A.2 Inmutabilidad | 🔴 Cierra R2 | Bajo |
| 3 | 3A.3 Autoridad de partes | 🔴 Cierra R3/R4 | Medio |
| 4 | 3A.4 T9 ejecutable | 🟠 Cierra R6 | Medio (tolerancia + demo) |
| 5 | 3A.5 γ con fuente | 🟠 Cierra R5 | Bajo |
| 6 | 3A.6 Prohibiciones + civil | 🟠 Cierra R7/R8/R9 | Medio |
| 7 | 3A.7 Ventanas | 🟡 Cierra R10/R11 | Bajo |
| 8 | 3B Escalera de equidad | 🟠 Vulnerables | Medio-Alto |
| 9 | 3C Dientes | 🟠 Cierra R12 | Alto (diseño + ejecución) |

---

## 8. Referencias de código verificadas

- `app/contracts_bp.py:1435-1450` — accept con identidad del body (R1).
- `app/contracts_bp.py:265-280` — upsert de contratos (R2).
- `app/parties_bp.py:update_party` — sin autorización (R3).
- `app/parties_bp.py:create_party` — partes fantasma (R4).
- `app/contracts_bp.py:_apply_wellness` — γ del body (R5).
- `maxocontracts/core/axioms.py:254-289` — validate_all sin T9 (R6); `:286` INV4 hardcodeado (R7).
- `app/schema.sql:394` — assigned_participant nullable (R9).
- `frontend/app/contracts/[id]/ContractDetailsClient.tsx` — timer client-side (R11).
- Dominios de integración: `app/forms_manager.py` (necesidades/follow-ups), `app/sdv_analyzer.py` (bienestar real).
