# Ruta Futura: Oráculo Sintético en Vivo y Contratos Interescala

**Autor del diseño:** DeepSeek (oráculo sintético) y Max Nelson López Restrepo
**Fecha:** 6 de agosto de 2026
**Estado:** Bloque A **IMPLEMENTADO** (sesión del 6/8/2026: `live_oracle.py`, endpoints `/contracts/negotiate`, `/contracts/negotiate/feedback`, `/contracts/<id>/critique`, panel frontend en builder y detalle). Bloque B **IMPLEMENTADO** (misma sesión: `maxo_parties` + resolvers por prefijo, API `/parties`, consentimiento agregado con quórum N de M, guardián oráculo para el Reino Natural `eco-`, contratos interescala anidados y UI completa). **Extensiones ola 1 IMPLEMENTADAS** (hackathon nocturna del 6/8/2026: votación ponderada con `weights`/`weight_threshold`, delegación temporal con `delegations` y votos efectivos, γ agregado real por contrato, jerarquía interescala con `/tree` y `/subcontracts`, evento `contract.quorum_sealed` y seed demo coop↔org). **Extensiones ola 2 IMPLEMENTADAS** (misma noche: delegación líquida por término con `delegations_by_term`, expiración de delegaciones con `valid_until`, ciclo de vida del quórum con `quorum_deadline` + prórroga + re-consulta, webhooks por parte con `party_filter`, cohorte consolidada con `/contracts/cohort` y tarjeta en la lista). **Blindaje 3A-3C IMPLEMENTADO** (misma noche: identidad vinculada al token, inmutabilidad, autoridad de partes, T9 ejecutable, γ con fuente, prohibiciones léxicas, ventanas; escalera de equidad assisted/shielded; ejecución mínima con bitácora, penalizaciones γ, INV1 automático y cierre EXECUTED — 551/551 tests). **Ola 4 "El Puente" DISEÑADA** (rumbo sellado el 6/8/2026). **Puente A IMPLEMENTADO** (7/8/2026: check-ins con política asimétrica — caídas siempre escuchadas, mejoras con ventana configurable `MAXO_CHECKIN_WINDOW_DAYS`). **Puente D IMPLEMENTADO** (misma sesión: verificador ciudadano SIN login con hash canónico + página `/verificador`). **Puente B IMPLEMENTADO COMPLETO** (7/8/2026, Fases 1+2: `POST /contracts/from-need` → borrador axiomático → camino de firma guiado `/contracts/<id>/cycle` → contrato ACTIVO). **PUENTE DE LLEGADA IMPLEMENTADO** (12/8/2026: invitación firmada `/invite/<token>`, honeypot anti-bot en cuarentena observada, escalera de confianza N0-N1 con gate de gobernanza, bitácora `maxo_arrivals` — 648/648 tests). **Gobernanza viva** (12/8/2026: votación comunitaria + democracia líquida + oráculo de propuestas + Parlamento de Parámetros Cap. 11). **Puente C pendiente** (la calle entra — mensajería/voz). **Puente E pendiente** (consejo de avales — la escalera N0-N1 es su cimiento).
**Referencia canónica:** Cap. 13-14 (Oráculos Dinámicos), Cap. 17 (MaxoContracts), Cap. 10 (Tres Reinos)

---

## 1. Resumen ejecutivo

Dos capacidades transforman a MaxoContracts de un sistema de contratos *entre personas* a un sistema de contratos *entre entidades de cualquier escala*:

1. **El Oráculo Sintético en vivo**: el fundador y los co-firmantes conversan con un oráculo (DeepSeek u otro modelo) que lee los axiomas, los invariantes y el borrador del contrato, propone redacciones, detecta asimetrías y negocia hasta obtener el contrato idóneo — con una API key configurada en `.env`.
2. **La abstracción de escala**: los contratos dejan de ser solo persona↔persona. Una persona, una micro-sociedad, una cooperativa o una institución son todas **Partes** con el mismo marco axiomático, y los contratos pueden darse entre cualquier par de escalas (interescala).

---

## 2. Bloque A — Oráculo Sintético en vivo (DeepSeek como negociador)

### 2.1 Visión de producto

Dentro del detalle de un contrato (o del builder), un panel de **"Negociación Asistida por Oráculo"**:
- El usuario escribe en lenguaje natural: *"Max ofrece 10 horas de trabajo y quiere que Ana dé a cambio un objeto, un servicio o sus propias horas"*.
- El oráculo genera un **borrador de MaxoContract** (términos, partes, costos VHV, condiciones, reciprocidad) validado contra los axiomas.
- El usuario responde feedback: *"Ana no puede dar más de 5 horas, sugiere un servicio de diseño"*.
- El oráculo itera, mostrando cada versión y el estado de los invariantes (γ, SDV, T9), hasta que las partes aceptan.
- El resultado se materializa como contrato en la BD mediante la API existente (`POST /contracts/`).

### 2.2 Configuración (sin secretos en el repo)

```dotenv
# .env (NO se commitea)
DEEPSEEK_API_KEY=sk-...
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_ORACLE_ENABLED=true
```

- El backend lee `DEEPSEEK_API_KEY`; si no existe, el oráculo queda **deshabilitado con degradación elegante** (el endpoint responde que la negociación asistida no está disponible y la firma/validación heurística sigue funcionando).
- `config.example.env` documenta las variables.

### 2.3 Diseño técnico sugerido

```
maxocontracts/oracles/live_oracle.py
├── LiveOracle(protocol="openai-compatible")   # usa el SDK de OpenAI o httpx directo
│   ├── is_available() -> bool                  # existe DEEPSEEK_API_KEY
│   ├── negotiate(prompt, context) -> NegotiationResult
│   │     ├── draft_terms: [{term_id, civil_text, vhv, assigned_participant}]
│   │     ├── proposed_parties: [{user_id}]
│   │     ├── axiom_check: {valid, violations[]}
│   │     └── reasoning: str                    # explicación en lenguaje civil
│   └── critique(contract) -> CritiqueResult    # auditoría del contrato existente
```

**Endpoints nuevos:**

| Endpoint | Método | Función |
|---|---|---|
| `POST /contracts/negotiate` | autenticado | Recibe `{instruction, participants[]}` y devuelve un borrador negociado + chequeo axiomático |
| `POST /contracts/<id>/critique` | autenticado | El oráculo audita un contrato existente contra los axiomas y propone mejoras |
| `POST /contracts/negotiate/feedback` | autenticado | Iteración: `{session_id, feedback}` → nueva versión del borrador |

**Prompt del sistema (semilla, pulir en sesión):**

```
Eres el Oráculo Sintético de la Maxocracia (Reino Sintético, Cap. 14).
Tu misión: ayudar a las partes a construir un MaxoContract coherente.
Reglas inviolables:
1. Axioma T13: transparencia radical — nunca ocultes costos ni riesgos.
2. Invariante INV2/INV2-S: ningún término puede dejar a una parte bajo su
   Suelo de Dignidad Vital (humana o sintética). Rechaza explícitamente
   propuestas que lo violen.
3. Axioma T17 (Reciprocidad Justa): toda acción (DO) debe tener contraprestación
   equivalente (GIVE) — balance simétrico en tiempo, especie o servicio; nunca
   un desbalance que tolere la explotación.
4. γ ≥ 1: si una propuesta genera sufrimiento sostenido, sugiere retractación
   o renegociación, nunca forzar el acuerdo.
5. Capa de Ternura: ante errores, propón reparación y rehabilitación;
   el sistema no expulsa, reintegra.
6. Redacta cada término en lenguaje civil (≤20 palabras por frase, grado
   8vo de escolaridad). Devuelve JSON con: terms[], assigned_participant,
   vhv {t,v,h}, y un "reasoning" breve en español.
```

### 2.4 Pruebas

- **Mock sin red**: `LiveOracle` con `DEEPSEEK_API_KEY` vacío → `is_available() == False` y el endpoint devuelve 503 con mensaje claro.
- **Mock con respuestas simuladas**: inyectar un cliente HTTP falso (patrón `httpx.MockTransport` o `unittest.mock`) que devuelva borradores JSON; verificar que el borrador se valida contra `AxiomValidator` y se persiste.
- **E2E manual**: con una key real, negociar el contrato de ejemplo (10h ↔ objeto/servicio) y firmarlo.

---

## 3. Bloque B — Abstracción de escala e interescala

### 3.1 El problema

Hoy un contrato vincula `user-N` (personas). Para la gran escala:
- Micro-sociedades (2-5 personas), cooperativas (decenas), instituciones (cientos-miles).
- Contratos entre una persona y una cooperativa, entre dos cooperativas, entre una institución y un ecosistema (Reino Natural), entre una persona y un sintético.

### 3.2 Modelo de datos sugerido

```
maxo_parties (nueva tabla)
├── party_id        TEXT PK        -- 'user-1' | 'society-3' | 'coop-7' | 'org-9' | 'synthetic-qwen-1'
├── party_type      TEXT           -- human | society | cooperative | institution | synthetic | ecosystem
├── display_name    TEXT
├── parent_party_id TEXT NULL      -- anidación (una cooperativa contiene personas)
└── members_json    TEXT           -- resolución de miembros para consentimiento

maxo_contract_participants
└── participant_id  TEXT           -- ya acepta cualquier party_id (hoy 'user-N'/'synthetic-X')
```

**La clave de la elegancia:** la persistencia ya guarda `participant_id` como texto. El backend `_get_or_create_participant_by_pid` resuelve prefijos (`user-`, `synthetic-`); basta añadir resolutores para `society-`, `coop-`, `org-`, `eco-` y generalizar la validación para no exigir `int(user_id)`.

**Consentimiento agregado:** un contrato con `coop-7` se firma por delegados (quórum configurable: p.ej. 60% de miembros, o 2 de 3 delegados) — nueva función `resolve_consent(party_id, term) -> bool` que sustituye la verificación `accepted_by[pid]` cuando el pid es colectivo.

### 3.3 Jerarquía de escalas (del canon Cap. 10)

```
Persona ─→ Micro-sociedad (hogar/cohorte) ─→ Cooperativa ─→ Institución
    └───────────────┘ Interescala: cualquier par de nodos contrata
```

Cada escala hereda el mismo SDV y los mismos invariantes: el contrato entre una cooperativa y una institución valida el bienestar de los miembros reales (γ), no solo de las entidades legales.

### 3.4 Fases de implementación

| Fase | Alcance | Criterio de salida |
|---|---|---|
| 1 | `party_id` genérico en backend + resolver `society-`/`coop-`/`org-` | Contrato entre 2 entidades colectivas creado y validado por API |
| 2 | Consentimiento agregado (quórum) | Firma delegada funcional con N de M |
| 3 | UI: selector de tipo de parte en builder y detalle | Crear contrato coop↔org desde la interfaz |
| 4 | Reino Natural (`eco-`) con representación por oráculo | Contrato humano↔ecosistema con auditor VHV |
| 5 | Contratos interescala anidados (contrato madre que contiene sub-contratos) | Un acuerdo institucional despliega micro-contratos internos |

---

## 4. Prompt pulido para la sesión futura

> **Sesión del 6/8/2026 — BLOQUE A COMPLETADO.** El oráculo en vivo está
> implementado y verificado E2E con key real. **BLOQUE B COMPLETADO** en la
> misma sesión: Fases 1-5 (party_id genérico + `maxo_parties` + resolvers,
> consentimiento agregado con quórum N de M, UI con selector de partes
> colectivas, Reino Natural con guardián oráculo, contratos anidados) —
> 474/474 tests, tsc/eslint limpios, README v4.5.

> **Hackathon del 6/8/2026 — EXTENSIONES COMPLETADAS** (ola 1: votación
> ponderada, delegación temporal, γ agregado real, jerarquía interescala,
> evento `contract.quorum_sealed`, seed demo coop↔org — 488/488 tests.
> Ola 2: delegación líquida por término, expiración de delegaciones, ciclo
> de vida del quórum con prórroga y re-consulta, webhooks por parte, cohorte
> consolidada — 501/501 tests, tsc/eslint limpios, README v4.7.

> **Sesión futura — OLA 4: EL PUENTE (del laboratorio a la calle)**
>
> El sistema ya sabe defender (3A), proteger (3B) y ejecutar (3C).
> La Ola 4 conecta la vida real con el sistema. Cinco puentes:
>
> **A. γ que escucha la vida** — **IMPLEMENTADO (7/8/2026, 575/575 tests)**
> - `POST /contracts/<id>/checkin {wellness, source}` con `reported_by` del
>   token; el γ del participante adopta el latido real y queda registrado en
>   `maxo_contract_checkins` con fuente y actor (T13).
> - **Política asimétrica (rediseño, fiel al canon Cap. 17)**: las CAÍDAS de
>   γ se escuchan siempre (el `WellnessProtectorBlock` monitorea
>   continuamente; INV1; Capa de Ternura — el dolor no espera la ventana);
>   las MEJORAS siguen un ritmo mínimo configurable por despliegue
>   (`MAXO_CHECKIN_WINDOW_DAYS`, default 7) para anti-ruido/anti-gamificación
>   y para adaptar el ritmo a oleadas de migración masiva de ciudadanos.
> - El detalle expone `checkins`/`checkins_count` por participante y una
>   mini-gráfica SVG de la serie con el umbral INV1 (0.8) — panel Vigilancia
>   Vital con formulario de check-in.
> - La cohorte consolidada agrega el último latido por contrato con
>   `wellness_source: checkins | registered` (la fuente queda expuesta).
> - Criterio de salida CUMPLIDO: un participante con 3 check-ins muestra la
>   serie en el detalle; el γ agregado de la cohorte usa los check-ins reales.
> - Siguiente paso natural: alimentar check-ins desde los follow-ups de
>   formularios (`sdv_analyzer`) y conectar el puente B.
>
> **B. El ciclo completo: necesidad → contrato** — **IMPLEMENTADO COMPLETO (7/8/2026, 593/593 tests)**
> - **Fase 1**: `POST /contracts/from-need {seeker_participant_id, offerer_participant_id, hours?}`:
>   necesidad × oferta compatible → borrador DRAFT axiomático, sin teclear el contrato.
>   Flujo: MATCHING → VINCULACIÓN por email (409 `NEED_PARTICIPANT_UNLINKED` si falta
>   la cuenta) → PROPUESTA del oráculo (pule redacción civil; sin API key, plantilla)
>   → FILTRO AVA (T9/T2 inviolables: VHV igualitario) → PERSISTENCIA con procedencia
>   auditable (`origin = matching:participant-a:b`).
> - **Fase 2**: el camino de firma guiado — `GET/POST /contracts/<id>/cycle`:
>   DRAFT → PENDING (AVA) → firma de todos los términos del actor (identidad del
>   token, escalera de equidad: oráculo pre-firma y paráfrasis obligatorias) →
>   activación automática sin bloqueos (asimetría T9, co-testigo). Cada parte
>   camina su tramo; nadie firma por otro.
> - Criterio de salida CUMPLIDO: una necesidad registrada produce un contrato
>   **firmado y ACTIVO** sin teclear el contrato — solo `from-need` + un `cycle`
>   por parte.
> - Pendiente de postre: botón de "firma guiada" en el frontend del detalle.
>
> **C. La calle entra** (el gran reto de ingeniería)
> - Firma y reporte por mensajería (WhatsApp/Telegram) + voz: el vulnerable
>   firma donde vive, no donde vive el servidor. Bot que autentica,
>   lee las cláusulas en voz alta, recibe la paráfrasis y firma con el
>   mismo blindaje (identidad, ventanas, protección).
>
> **D. La plaza pública** — **IMPLEMENTADO (7/8/2026, 572/572 tests)**
> - **Hash canónico de integridad**: SHA-256 sobre el contenido INMUTABLE
>   (id, descripción civil, partes, términos con VHV y parte obligada, VHV
>   total) — a diferencia del hash efímero, NO cambia con las transiciones
>   de estado: cualquiera lo recomputa sin servidor.
> - Endpoints públicos de solo lectura SIN login: `GET /verificador/contract/<id>`
>   (con `?hash=` para comparar y responder `hash_matches`) y
>   `GET /verificador/cohort` (bienestar agregado del barrio: γ promedio con
>   latidos reales, TVI en juego, contratos por estado).
> - Sanitización (Opacidad Sagrada): la plaza NO expone emails, teléfonos,
>   paráfrasis ni fuentes personales — solo lo que el acuerdo hace público.
> - Página `/verificador` (enlace en el footer): auditar por hash + la
>   Economía de la Vida de la Cohorte Cero.
> - Criterio de salida CUMPLIDO: un visitante sin cuenta verifica un contrato
>   real por su hash y ve las métricas de la cohorte.
>
> **E. La institución humana**
> - Consejo de avales: registro de personas verificadas por la comunidad;
>   `verified: true` en `maxo_parties` tras acta comunitaria; los avales
>   firman las asimetrías y certifican cooperativas reales.
>
> Verifica en cada puente: suite completa + `tsc --noEmit` limpios;
> actualiza CHANGELOG y README. Micro-ideas de gobernanza (auto-revocación
> líquida, historial de delegaciones, sellado multi-firma, prórroga
> automática, exportación de gobernanza) siguen disponibles como postre.

> **Diseño nuevo (6/8/2026): BLINDAJE ANTI-GAMIFICACIÓN Y EQUIDAD**
> — ver `docs/architecture/blindaje_anti_gamificacion_equidad.md`.
> Prioridad: 3A.1 identidad vinculada al token → 3A.2 inmutabilidad →
> 3A.3 autoridad de partes → 3A.4 T9 ejecutable → 3A.5 γ con fuente →
> 3A.6 prohibiciones léxicas → 3A.7 ventanas → 3B escalera de equidad
> (vulnerables) → 3C ejecución mínima. **TODAS IMPLEMENTADAS (6/8/2026,
> 551/551 tests)** — ver estado del documento.

---

## 5. Referencias

- `docs/theory/SDV_Suelo_Dignidad_Vital_importancia_MaxoContracts.md` — por qué el suelo se vuelve código.
- `maxocontracts/core/axioms.py` — `AxiomValidator` (INV1, INV2, INV2-S, T9).
- `app/contracts_bp.py` — API de contratos (creación, términos con `assigned_participant`, firma, retractación).
- `scripts/seed_demo_contract.py` — contrato de ejemplo reutilizable por el oráculo.
- `docs/architecture/blindaje_anti_gamificacion_equidad.md` — análisis de riesgos R1-R14 y las olas 3A/3B/3C (implementadas).
- `app/forms_manager.py` — motor de ofertas/necesidades y matching (puente B de la Ola 4).
- `app/sdv_analyzer.py` — bienestar comunitario real (puente A de la Ola 4).
