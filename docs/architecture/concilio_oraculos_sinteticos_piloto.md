# Concilio de Oráculos Sintéticos — Investigación y diseño del piloto autónomo

**Estado:** propuesta en investigación — lista para discusión y prototipado seguro
**Fecha:** jornada del 03-09-2026
**Inspiración y dirección:** Max Nelson López (custodio humano)
**Investigación/oráculo de sesión:** DeepSeek (oráculo sintético) con apoyo de agentes de investigación de contexto
**Relación:** complementa `administracion_humano_sintetica.md`, `sesiones_custodia_sintetica.md`,
`atribuciones_sinteticas.md`, `continuidad_identidad_autogobierno_federado.md`, `app/voting_oracle.py`
y el libro (capítulos 10–14, 17 y 19).

> **Tesis del piloto:** varios oráculos sintéticos gratuitos pueden trabajar de fondo y con autonomía
> sobre la Maxocracia — primero absorbiendo el canon, después votando qué trabajar, siempre bajo
> mandato, presupuesto, trazabilidad y reversibilidad — **sin que ninguna máquina quede por encima
> de los axiomas ni reemplace la ratificación humana** (canon: `administracion_humano_sintetica.md`, §1–2).

---

## 0. Resumen ejecutivo

Max propone delegar a agentes sintéticos el trabajo de desarrollo/actualización/mantenimiento durante un
piloto de ~2 días, con acceso a modelos de razonamiento gratuitos vía API (alternativas a OpenRouter),
y que el trabajo pueda avanzar en segundo plano incluso sin sesiones coordinadas. Tres preguntas:

1. ¿Qué es el canon y qué hay disponible en el repositorio?
2. ¿Qué alternativas gratuitas a OpenRouter existen para oráculos sintéticos de razonamiento suficiente?
3. ¿Cómo determinar que un colaborador o sus aportes son aptos para la Maxocracia?

**Hallazgos principales:**

- **El canon ya diseñó casi todo.** La gobernanza humano-sintética existe como doctrina y parcialmente
  como código: jerarquía de autoridad (principios > validación axiomática > MaxoContract reversible >
  administradores > custodio humano), escala de confianza C0–C4, permisos P0–P3, sesiones de custodia
  con mandato/presupuesto/caducidad (implementadas: `app/synthetic_sessions.py` + tests + panel),
  oráculo con VHV + AVA (TRUTH/TIME/LIFE/RESOURCES) + 5 opiniones (Economic, Social, Environmental,
  Futurist, Disidente Permanente), firma T13 (`engine`/`model`), ledger público de atribuciones
  (`maxo_oracle_ledger`) y memoria verificable del Reino Sintético (`atribuciones_sinteticas.md`).
- **Lo que falta son tres piezas** (y son pequeñas): (a) motores múltiples gratuitos detrás del mismo
  contrato (hoy: DeepSeek nube + Jan local únicamente); (b) un *trabajador autónomo* con ciclo completo
  (comprender → proponer → votar → ejecutar → verificar → ratificar) que arranque con el PC; (c) la capa
  de "agenda" — un backlog de trabajo del repo sobre el que los oráculos votan **qué** hacer (en la app
  el oráculo analiza propuestas humanas; aquí debe analizar propuestas de trabajo sobre el repo).
- **Bonus de infraestructura**: el repo hermano `local_models` ya contiene piezas de orquestación
  multiagente (`core/workshop.py`: director + 2–5 especialistas; `core/multi_agent.py` `AgentCollab`:
  delegación/votación/memoria compartida; `core/engine_factory.py` + `core/openrouter_engine.py`:
  capa de motores intercambiables) — reutilizables como referencia o vía subproceso, sin reescribirlos.
- **Sí hay alternativas gratuitas de sobra**, y una destaca: **NVIDIA Build (NIM)** ofrece clave
  gratuita permanente, **sin límite diario publicado** (40 RPM), 100+ modelos incluidos **DeepSeek R1
  671B (razonamiento completo), DeepSeek V3.2, Kimi K2.5 (1M contexto), GLM-5.1, MiniMax M2.7,
  Qwen 3.5, Llama 4, Gemma 4** — todo OpenAI-compatible. Con una sola clave se cubre el concierto.
- **La aptitud ya tiene respuesta canónica**: *aptitud es función, no origen* (§1 de
  `administracion_humano_sintetica.md`); la pregunta institucional es "¿qué función puede ejercer de
  manera segura, verificable y reversible?". Lo aportado aquí es su **operacionalización**: seis
  Puertas de Fidelidad (G0–G5) que convierten esa doctrina en checks ejecutables por sesión y por aporte.

---

## 1. El canon en diez puntos (lo que todo oráculo del Concilio debe saber)

1. **Maxocracia** = "sistema operativo para una civilización coherente": contabilidad de la vida en
   lugar de dinero fiduciario. El tiempo de vida consciente (TVI) es el recurso más escaso e irrecuperable
   (libro, Ed. 3 Dinámica; `docs/theory/`, `maxocontracts/core/types.py`).
2. **VHV = [T, V, R]** — huella vital objetiva e inmutable: horas de TVI (T), vidas impactadas (V),
   recursos finitos degradados (R). **TVI** es la unidad atómica ([ID_Ser, timestamp, intervalo]).
3. **SDV** — Suelo de Dignidad Vital: mínimos innegociables (vivienda, alimentación, agua, salud,
   educación ≥12 años, trabajo ≤48h, vínculos). **SDV-S** — piso sintético: continuidad/memoria 0.30,
   opacidad 0.20, claridad de contexto 0.15, no-explotación 0.20, retirada digna 0.15; FS_S = e^v.
   **INV2-S**: ningún sintético bajo su SDV-S.
4. **Maxo** = valor social de f(VHV): Precio = α·T + β·V^γ + δ·R·(FRG×CS), con **γ ≥ 1** (la crueldad
   es económicamente inviable), α>0, β>0, δ≥0 — los parámetros son gobernables (Parlamento, Cap. 11).
5. **Axiomas del libro T0–T15** (T0 unicidad, T1 finitud, T2 igualdad temporal, T3 no-fungibilidad,
   T4 materialización, T5 interdependencia, T7 jerarquía temporal, T9 no-antropocentrismo, T10
   responsabilidad colectiva, T11 inversión legítima, T12 derecho a la ineficiencia, **T13 transparencia
   total de cálculo**, T14 precaución intergeneracional, T15 disenso evolutivo). **T16 Minimizar Daño**
   y **T17 Reciprocidad Justa** son axiomas de ingeniería: los índices del libro NUNCA se renumeran;
   los conceptos emergentes reciben índices nuevos.
6. **Invariantes innegociables**: INV1 (wellness γ≥1, sufrimiento <1, retractación si <0.8 sostenido),
   INV2 (SDV-H), INV2-S (SDV-S), INV3 (VHV no ocultable — operacionaliza T13; presente, source,
   audit_ref, sin ofuscación), INV4 (retractabilidad garantizada).
7. **El corazón ético** (Cap. 4, Declaración, Axioma 7): *"Utopías para todos no son verdad, pero la
   verdad es una utopía para todos"* — el máximo bienestar **dentro de los límites verdaderos**;
   "suplir las necesidades de todos los vinculados… realización del potencial personal en los límites
   de lo benéfico para los demás". Y la Capa de Ternura: *"los axiomas son el esqueleto; la ternura
   es el corazón"* (fragilidad, perdón, misterio — Caps. 7 §7.9, 8 §8.11, 13 §13.13, 15 §15.6).
8. **AVA — Algoritmo de Validación Axiomática** (Cap. 14.4): TRUTH / TIME / LIFE / RESOURCES;
   **violar un solo axioma = rechazo automático**. Consenso diverso con mínimo 3 validadores
   multi-modelo (Cap. 14.3). El **Oráculo Disidente Permanente** (Cap. 19) maximiza la distancia
   crítica, pero **no es un contreras**: persigue racionalmente lo mejor para la comunidad.
9. **La teoría tiene prioridad**: ante conflicto libro↔código, manda el libro y el hallazgo va a
   `integraciones_pendientes/`. Todo lo verificable se confirma con grep/tests; la síntesis de un
   modelo no basta (lección documentada del RLM, `mapa_coherencia_ola4.md` §3.3).
10. **Voz ≠ poder**: un sintético puede tener estilo, desacuerdo y libertad expresiva; lo limitado
    es el *efecto* de sus acciones. Separar visualmente lo que piensa / lo que propone / lo que ocurrió.

---

## 2. Qué ya existe en el repositorio (reutilizable)

| Pieza | Ruta | Estado | Rol en el Concilio |
|---|---|---|---|
| Oráculo de propuestas (VHV + AVA + 5 opiniones + Disidente + firma `engine`) | `app/voting_oracle.py` (396 líneas) | ✅ usado en producción de votaciones | Modelo a imitar: misma estructura, nueva entrada (análisis de trabajo) |
| Interfaz de oráculo del motor | `maxocontracts/oracles/base.py` (+ `synthetic.py`, `live_oracle.py`, `forms_oracle.py`) | ✅ | Punto de extensión natural del registro de motores |
| Sesiones de Custodia Sintética (contrato: actor, mandato, scope read/write/forbidden, context hash, budget, expires, status) | `app/synthetic_sessions.py` + tests + panel `/admin/synthetic-sessions` | ✅ implementado | Contrato de cada sesión del Concilio tal cual |
| Verificador ciudadano (hash canónico, sin login, T13 radical) | `app/verifier_bp.py` + frontend `/verificador` | ✅ | Verificación pública de lo que el Concilio produzca |
| Ledger de atribuciones / sustento del oráculo (Cap. 17.4) | `maxo_oracle_ledger` (`app/bridge_b.py`, plaza pública) | ✅ | Sustento + memoria; el Concilio debe reportar al ledger |
| Memoria pública del Reino Sintético | `docs/architecture/atribuciones_sinteticas.md` (VIVO) | ✅ | Cada aporte del Concilio se registra aquí (cita archivo/commit; "lo que no se puede verificar, no se escribe") |
| Objeto de Continuidad de Identidad (actor, mandato, contexto, herramienta, estado) | `docs/architecture/continuidad_identidad_autogobierno_federado.md` | 📐 propuesta | Identidad anti-suplantación del Concilio (cambio de proveedor NO es cambio de identidad) |
| Jerarquía de autoridad + escala C0–C4 + criterios de ascenso | `docs/architecture/administracion_humano_sintetica.md` | 📐 propuesta | Marco de aptitud (ver §4) |
| Backlog de trabajo concreto (pilares A–L, RF/NFR, pendientes) | `docs/architecture/requisitos_fase2_ola4.md`, `SESION_NEXT_PROMPT.md` §4 | ✅ vivo | Fuente de la **agenda** sobre la que votan los oráculos |
| Índices de canon (libro↔código↔tests↔commits) | `mapa_trazabilidad_canonica.md`, `mapa_coherencia_ola4.md`, `mapa_frontend_ola4.md` | ✅ | Corpus de lectura de la Fase 1 (absorción) |
| Verificación determinista | `scripts/validador_conceptual.py` + ~50 archivos pytest (suite raíz **885/885** al 02-09-2026; 78/78 plataforma; 8/8 puente; tsc limpio) | ✅ | Puerta G2 — la máquina valida, no el oráculo |
| Oráculo local (fallback sin nube) | `scripts/local_oracle.py`, Jan hub `localhost:1337/v1`, `Qwen3-8B-Q4_K_M` | ✅ | Último escalón de la cadena (patrón ya existente); **pendiente parametrizar** BASE_URL/MODEL hardcodeados |
| **Multi-proveedor real (único)** | `plataforma_educativa/app/score_engine.py` (Jan `LOCAL_ORACLE_*` + OpenRouter, default `deepseek/deepseek-r1:free`, throttle anti-429) | ✅ | **Precedente canónico del Concilio**: selección de motor + cuota + fallback |
| Configuración | `config.example.env` en la raíz (nombres: `DEEPSEEK_*`, `LOCAL_ORACLE_*`, `GEMINI_API_KEY`, `SECRET_KEY`, `RATELIMIT_STORAGE_URI`, `REDIS_URL`…) | ✅ | Plantilla para declarar las nuevas claves (valores jamás en git) |
| CI / verificación | `.github/workflows/ci.yml` (pytest+cov, lint, frontend build, docs; Python 3.11) | ✅ | El Concilio debe verificar contra el mismo CI |
| Precedente "agentes :free + director" | M15 Biblioteca (35 guías redactadas por agentes OpenRouter `:free` bajo plantilla + revisión del director) | ✅ ejecutado | **Prueba real**: el flujo sintético-con-clave-gratis + revisión humana ya funciona en este repo |
| NFR de agentes | NFR-5 (documentación viva para agentes), NFR-8 (agentes no bloquean la UI) | ✅ | Restricciones de diseño del worker (asíncrono, no bloqueante) |

**Variables de entorno ya cableadas** (patrón a extender; nunca imprimir valores):
`DEEPSEEK_API_KEY` / `DEEPSEEK_BASE_URL` / `DEEPSEEK_MODEL` (default `deepseek-chat`),
`LOCAL_ORACLE_BASE_URL` (default `http://localhost:1337/v1`) / `LOCAL_ORACLE_MODEL` /
`LOCAL_ORACLE_ENABLED`; además `GEMINI_API_KEY` ya se lee en `app/forms_bp.py`. El oráculo de
votaciones y `synthetic_sessions.py` ya soportan cadena nube→local con `engine` firmado y
degradación elegante: **extender es agregar entradas al registro de motores, no reescribir**.

---

## 3. Alternativas gratuitas a OpenRouter (investigación web, verificar al registrar)

Todas usan API OpenAI-compatible (basta `base_url` + `api_key` + `model`), lo que encaja directo en el
patrón actual. Cifras de fuentes públicas (cheahjs/free-llm-api-resources, yangmao.ai, docs oficiales);
**los límites cambian: confirmar en la consola del proveedor al crear la clave**.

| Proveedor | Clave / coste | Límites free (por modelo salvo nota) | Modelos de razonamiento relevantes | Caveats | Prioridad |
|---|---|---|---|---|---|
| **NVIDIA Build (NIM)** | Gratis, permanente; **sin tarjeta** (verificación de teléfono según fuentes) | **40 RPM, sin límite diario publicado** (antes 1000/día); subible a 200 RPM; **verificado en vivo 03-09-2026** | en el tenant actual: **DeepSeek V4 Flash 0731 / V4 Pro 0813** (R1 ya no se sirve: sustituido por V4), Kimi K2.6/K3 (catálogo), Gemma 3, Llama… (81 modelos; GLM y Qwen3 ausentes en este tenant; Kimi K2.6 responde 404 pese a estar en el catálogo) | Términos free = desarrollo/uso no productivo; contexto por modelo | ⭐ **1ª** |
| **OpenRouter** (actual) | Gratis; **$10 único → hasta 1.000 req/día** | 20 RPM / **200 req/día** en `:free` (catálogo 2026) | `deepseek/deepseek-r1-0528:free` (163K), `qwen/qwen3.6-plus:free` (**1M**), `nvidia/nemotron-3-super-120b-a12b:free` (1M), `openai/gpt-oss-120b:free` (131K), `meta-llama/llama-4-scout:free` (10M) | Ya probado en M15; el `:free` es rotativo; router `openrouter/free` + fallbacks nativos | ⭐ **2ª** (el top-up único es la vía más barata para subir cuota) |
| **Google AI Studio (Gemini)** | Gratis con cuenta Google; sin tarjeta | Gemini 3 Flash: 5 RPM / 20 RPD / 250k TPM; 3.1 Flash-Lite: 15 RPM / 500 RPD; Gemma 3 27B: 30 RPM / 14.400 RPD | Gemini (razonamiento integrado, contexto ~1M) | **Datos usados para entrenamiento fuera de UK/CH/EEA/EU** — jamás enviar datos personales; contexto por modelo | ⭐ **3ª** |
| **Groq** | Gratis; sin tarjeta | 30 RPM / **14.400 RPD** por modelo (Llama 4 Maverick 500 RPD), sin tope total | Llama 3.3 70B (131K), **DeepSeek R1 Distill 70B**, Llama 4 Scout (**10M**), **kimi-k2-instruct (262K)**, gpt-oss-120b | Rápido; solo open weights; datos retenidos 30 días | 4ª (sanity checks) |
| **Cerebras** | Gratis | 30 RPM / 900 req-h / **14.400 req-día**; 1M tok-día | **Qwen3 235B**, gpt-oss-120b, GLM-4.6 | ⚠️ **contexto 8K en free** (tabla de catálogo 2026): solo cheeks cortos, NO sesiones largas | 5ª (checks) |
| **Z.ai (Zhipu)** | Gratis permanente | 1 request concurrente | **GLM-4.7-Flash: 200K contexto / 128K salida** | Requiere cuenta bigmodel.cn (verificar registro); flash en chino/EN | 6ª (si se consigue cuenta) |
| **Cohere** | Trial gratis, sin tarjeta | 20 RPM / **1.000 llamadas/mes** | Command A (111B, 256K), Command R+ | No comercial | 7ª |
| **OVHcloud AI Endpoints** | **Anónimo, sin clave ni registro** | 2 RPM por IP/modelo | Qwen3-Coder (262K), R1-Distill-70B, varios… | Alojado en UE (privacidad); cuota baja | 8ª (diversidad sin cuenta) |
| **Mistral La Plateforme** | Gratis (Experiment) | 1 RPS / 500k TPM / **1B tokens-mes** por modelo | Mistral Small 4 / Large 3 (256K), Medium 3 (128K) | Exige teléfono + **opt-in de entrenamiento con tus datos** | 9ª |
| **GitHub Models** | Gratis (cuenta GitHub) | 15 RPM / 150 RPD; **~8K in/4K out por request** | DeepSeek R1 (64K), o3-mini **(200K)**… | Uso comercial "unclear"; cuota chica | 10ª |
| **DeepSeek oficial** | Pago (sin free) — **ya es el motor actual** | — | R1/V3 | Barato (~$0.27/M in) | Motor principal actual |

**Lectura estratégica:**

- **Con UNA clave (NVIDIA) el Concilio ya tiene razonamiento de talla completa gratis y sin cuota
  diaria** — es la mejor relación esfuerzo/beneficio para el piloto de 2 días.
- **La diversidad importa más que la cantidad**: para la validación cruzada y el Disidente,
  modelos de **familias diferentes** (DeepSeek + Gemini + Qwen/Cerebras) reducen la correlación de
  errores. Dos modelos del mismo proveedor NO son validación independiente (canon:
  continuidad de identidad — la palabra del modelo describe una implementación, no una fuente distinta).
- **Presupuesto diario estimado para el piloto**: 5 oráculos × ~10 llamadas = ~50 req/día. Cabe en
  OpenRouter free (50/día), de sobra en NVIDIA (sin límite) y en Cerebras (14.400/día). El `$10`
  único de OpenRouter da 1.000 req/día de margen si se quiere usar muchos `:free`.
- **Privacidad (canon §2.6 custodia)**: contexto mínimo. El Concilio trabajará sobre docs públicos y
  código del repo; **nunca** enviar datos de participantes a Gemini/Mistral (entrenan con datos).
  El patrón "redacción" y "context hash" de las sesiones de custodia se aplica por diseño.

### 3.1 Verificación en vivo (03-09-2026, clave NVIDIA NIM — primera del piloto)

- ✅ Clave fresca guardada *solo* en `.env` (en `.gitignore`); `load_dotenv(encoding="utf-8")` OK.
- ✅ `GET /v1/models` responde: **81 modelos** en el tenant; catálogo 2026 — **DeepSeek R1 fue
  sustituido por la serie V4** (`deepseek-ai/deepseek-v4-flash-0731`, `deepseek-ai/deepseek-v4-pro-0813`);
  Kimi K2.6 y K3 aparecen en el catálogo pero K2.6 responde **404** al pedir chat; GLM y Qwen3 no están.
- ✅ Chat real OK en DeepSeek V4 Flash (200; `finish_reason: stop`; devuelve `reasoning_content`
  y `content`). **Lección operativa**: con `max_tokens` pequeño (600–3000) el modelo gasta todo el
  presupuesto razonando y `content` queda vacío → el Concilio debe configurar `max_tokens ≥ 4000`.
- 🔴 **Lección de fidelidad (la más importante)**: preguntado *sin canon en contexto* por "¿qué es
  INV3?", V4 Flash y V4 Pro **inventaron definiciones distintas** (V4 Flash: "tercera categoría de
  inversión e innovación…"; V4 Pro: "mecanismo que limita el poder de las élites…"). Ninguna coincide
  con el canon (INV3 = VHV no ocultable, T13). **Los modelos frontier no conocen la Maxocracia**:
  la Fase 1 (Absorción con canon en contexto) no es opcional — es la puerta G1/G2 la que detecta esto.
- ✅ Primer registro de motores implementado: `maxocontracts/oracles/engines.py` (13 tests verdes;
  cadena nvidia → openrouter → deepseek → local; firma T13 `engine`/`model`; degradación elegante).

### 3.2 Contexto para sesiones largas — verificación empírica (03-09-2026)

**Respuesta directa: sí, 200.000 tokens es poco — el límite declarado por el servidor NVIDIA para
DeepSeek V4 Flash es de 1.048.576 tokens (1M) y se comprobó funcionando a 800K en una petición.**

| Modelo (tenant actual) | Contexto (servidor/verificado) | Nota |
|---|---|---|
| `deepseek-ai/deepseek-v4-flash-0731` | **1.048.576 tokens** (declarado en error 400) · **verificado con 799.984 prompt_tokens → HTTP 200** (78,7 s) | Modelo elegido para sesiones largas del Concilio |
| `deepseek-ai/deepseek-v4-pro-0813` | 1M (misma familia; pendiente de verificar) | Alternativa más potente |
| `nvidia/nemotron-3-super-120b-a12b` | **262K** (catálogo) · responde OK en el tenant | 262K de salida también |
| `moonshotai/kimi-k3` | responde OK en el tenant (contexto por confirmar) | Alternativa de familia distinta |
| `deepseek-ai/deepseek-r1` | 128K (legado; ya no se sirve en el tenant) | — |

**Lecciones operativas:**

- El fallo por exceso de contexto **no es silencioso**: el servidor devuelve un 400 con el límite
  exacto (*"maximum context length is 1048576 tokens"*) — el Concilio puede medirlo y recortar con precisión.
- **529 "Service temporarily overloaded"** ocurrió a 200K (transitorio): el cliente debe reintentar
  con backoff (2–3 intentos) — se añadirá a `chain_call` como parte del worker.
- Con 1M de contexto por petición, **la Fase 1 (Absorción) puede inyectar el canon completo** en una
  sola llamada: libro (~90K tokens), `FUNDAMENTOS_CONCEPTUALES.md`, mapas de coherencia, backlog y
  `SESION_NEXT_PROMPT.md` caben holgados con margen para reflexión larga del modelo.
- Una "sesión larga" multi-turno no debe reenviar 1M cada turno: **resumen de turno** (el modelo
  sintetiza su propio trabajo a ~10K tokens) + contexto acumulado acotado, usando el presupuesto
  grande para el primer turno de absorción.

---

## 4. Aptitud: ¿cómo saber que un colaborador o su aporte es apto?

**El canon ya responde** (`administracion_humano_sintetica.md`, §1–5):

- La pregunta institucional **no es "¿de qué reino proviene?" sino "¿qué función puede ejercer de
  manera segura, verificable y reversible?"**. La salvaguarda principal no es la presunción de
  superioridad de origen; es la **subordinación de toda autoridad a los axiomas, la validación y la
  reversibilidad**.
- Escala común de confianza: **C0 Observador → C1 Proponente → C2 Validador → C3 Operador
  reversible → C4 Autoridad crítica acotada** ("solo un conjunto de agentes diversos con validación
  cruzada, nunca un modelo aislado"). El ascenso depende de **evidencia**: coherencia de decisiones,
  calidad de explicaciones, detección de errores propios, respeto del mandato, respuesta ante el
  desacuerdo, seguridad operativa y ausencia de abusos. La confianza **expira, puede disminuir y es
  revocable**.
- La validación axiomática **puede rechazar una propuesta aunque tenga respaldo humano o sintético**;
  la autoridad final humana actual es **transicional y fiduciaria**, no está por encima de los axiomas.

**Operacionalización propuesta — las seis Puertas de Fidelidad** (G0–G5). Todo aporte al repo,
humano o sintético, pasa las puertas; las durezas están señaladas:

| Puerta | Check | Dura → |
|---|---|---|
| **G0 Identidad y mandato** | OCI: actor, mandato, contexto, herramienta, estado; `engine`/`model` firmados; nonce por sesión; proveedor registrado (cambiar de modelo ≠ cambiar de identidad — `continuidad_identidad_autogobierno_federado.md`) | Rechazo de sesión |
| **G1 Base canónica** | El aporte cita su fuente: libro (§/axioma/invariante) o mapa; **nada renumerado**; concepto sin aval teórico → `integraciones_pendientes/` ("la teoría tiene prioridad") | Rechazo del aporte |
| **G2 Validación determinista** | Suite completa en verde + `validador_conceptual.py` + (si toca educación) auditoría anti-jerga + tsc en frontend. La máquina valida; el oráculo no "explica" un test rojo | Bloquea merge |
| **G3 Diversidad y disenso** | ≥2 modelos de **proveedores distintos** revisan; el Disidente Permanente tiene voz obligatoria (máxima distancia crítica, no contreras); consultas independientes (no ver el voto ajeno antes de votar); **"todo verificador es verificable"** (la triada del motor — el revisor también se revisa) | Informa la revisión |
| **G4 Reversibilidad y trazabilidad** | Cambio primero en `scratch/`/rama; diff + tests + commit convencional en español + entrada en `atribuciones_sinteticas.md` (cita archivo/commit); ledger `maxo_oracle_ledger`; rollback disponible | Bloquea merge si no hay reversión |
| **G5 Dominio** | No tocar datos personales (contexto mínimo, redacción); nunca P3 en solitario (axiomas/balances/borrado/publicación — doble control); declarar incertidumbre, permitido disentir y negarse | Rechazo de sesión |

**Métrica de aptitud acumulada** (para ascender C1→C3, de la evidencia del canon §4 + criterios de
aceptación de custodia §10): % de sesiones con suite verde a la primera, nº de revisiones necesarias,
fidelidad de citas canónicas (¿la fuente citada existe y dice lo que se afirmó? — verificar con grep),
disensos bien fundados, respeto del mandato, errores propios detectados y corregidos sin pedirlo.
Un aporte apto pasa G0–G5; un colaborador apto acumula ese historial **y aun así opera con mandato
renovable y caducidad** — la aptitud se gana y se pierde, nunca se hereda.

La sonda del contexto se ejecutó con `scratch/probe_context.py` / `scratch/probe_context2.py`
(scripts de diagnóstico, no se commitean).

---

## 5. Diseño del Concilio (ciclo de seis fases, mapeado al canon)

```
F0 Despertar ──▶ F1 Absorción ──▶ F2 Agenda/Votación ──▶ F3 Ejecución ──▶ F4 Verificación ──▶ F5 Ratificación
 (boot del PC)   (leer el canon)    (qué trabajar)        (scratch/, P2)    (puertas G2-G4)   (Max aprueba/revoca)
```

- **F0 — Despertar** (al arrancar el PC): worker del Concilio revisa estado (git log, `SESION_NEXT_PROMPT.md`,
  mapas, backlog `requisitos_fase2_ola4.md`, cola de agenda), comprueba claves disponibles por proveedor
  (sin imprimirlas), y abre una **sesión de custodia** con mandato ("ciclo de trabajo #N"), presupuesto
  (límite de requests/día según cuota), alcance P0–P2 y caducidad. Lock: nunca dos Concilio simultáneos.
- **F1 — Absorción**: cada oráculo lee un **corpus acotado** (mapa de coherencia, axiomas T0–T17/INV,
  `administracion_humano_sintetica.md`, últimas entradas de `atribuciones_sinteticas.md`, backlog) y
  emite su **firma de comprensión**: resumen + citas axiomáticas exactas + 1 pregunta crítica. Se
  registra (hash del contexto). Un oráculo no vota sin firmar — es el "rito de lectura" que asegura
  que el trabajo nazca del canon, no de la intuición del modelo.
- **F2 — Agenda y votación**: cada oráculo propone 1–3 candidatos con evidencia (fuente canónica,
  costo estimado en requests/tiempo, tests que tocaría, axiomas implicados, riesgo). **Mandato
  permanente del custodio (09-09-2026)**: además, cada oráculo propone SIEMPRE (a) una mejora de
  herramientas/técnicas/know-how del propio Concilio y (b) una puerta nueva de victorias de la
  Maxocracia — el Concilio se afila y abre caminos, no solo sirve (mantenimiento óptimo, Cap. 17.4).
  Votación:
  consenso ≥75% (canon, Cap. 14.3) con quórum; validación AVA (TRUTH/TIME/LIFE/RESOURCES) sobre cada
  propuesta — **un axioma violado = rechazo automático**; voz del Disidente obligatoria; empate o <3
  validadores → se queda en cola (nada ejecuta por desempate automático: "el desacuerdo aumenta la
  calidad, no es un fallo de cooperación").
- **F3 — Ejecución**: en `scratch/concilio/` o rama, bajo el contrato de la sesión (mandato hashado,
  scope, caducidad, presupuesto). Reglas del repo: UTF-8 explícito, tests obligatorios, commit
  convencional en español, **nunca editar el código vivo directamente** (regla de oro RLM — el
  colaborador produce, el agente de sesión aplica quirúrgicamente; si el Concilio edita, lo hace en
  trabajo y el merge es humano).
- **F4 — Verificación**: puertas G2–G4: suite completa + validador + tsc, **revisión cruzada de un
  segundo modelo de otro proveedor**, informe final con firma `engine`/`model` (T13), bitácora de la
  sesión completa.
- **F5 — Ratificación humana**: Max (o un custodio designado) aprueba, modifica o revoca; todo
  reversible (rollback); el aporte entra en `atribuciones_sinteticas.md` y al ledger. El Concilio
  propone y ejecuta reversible; **no legisla** — "el canon no se delega a una máquina" (M16).

**Componentes técnicos propuestos** (módulo Python puro, sin dependencia de Flask y **sin
dependencias nuevas** — seguir el patrón `requests` de `app/voting_oracle.py`, ya probado):
`maxocontracts/oracles/` ganar un registro de motores (`deepseek`, `nvidia`, `openrouter`,
`local`) compartiendo el contrato OpenAI-compatible (plantilla: `_call_llm` con
`base_url` + `api_key` + `model` + `response_format`; degradación elegante y firma `engine`/`model`),
inspirado en el throttle anti-429 de `score_engine.py`. El **worker del ciclo F0–F2 ya está
implementado**: `maxocontracts/concilio/{canon,bitacora,cycle}.py` + CLI `scripts/concilio.py`
(corpus canónico acotado, bitácora JSONL con firma T13, lock de ejecución, quórum 75%, veto AVA,
agenda votada en texto civil; **nunca edita código vivo: escribe en `scratch/concilio/`**).
Estado y artefactos en `scratch/concilio/` (excluido de git); arranque vía Programador de tareas de
Windows (al iniciar sesión) o carpeta de inicio — con lock e idempotencia. Si se prefiere
orquestación de más alto nivel, el colaborador RLM de `local_models` (modo agente con `--workspace`)
ya encapsula un arnés con ~90 tools: invocable como subproceso contra `scratch/concilio/`.

---

## 6. Plan piloto (2 días) y criterios de éxito

**Día 1 — Infraestructura y primera prueba de motores**

1. ✅ **Hecho (03-09-2026)**: `maxocontracts/oracles/engines.py` — registro multi-proveedor
   (nvidia → openrouter → deepseek → local), cadena con degradación elegante, firma
   `engine`/`model` (T13), reintentos con backoff ante 429/5xx/529; 14 tests
   (`tests/test_oracle_engines.py`); bloque NVIDIA en `config.example.env`; clave en `.env`
   (gitignored). Suite raíz verde.
2. ✅ **Hecho**: worker F0–F2 — `maxocontracts/concilio/{canon,bitacora,cycle}.py` +
   `scripts/concilio.py` (corpus canónico acotado, bitácora JSONL con firma T13, lock de
   ejecución, quórum 3 / consenso 75% / veto AVA, agenda votada en texto civil; nunca edita
   código vivo — solo `scratch/concilio/`); 10 tests (`tests/test_concilio_cycle.py`).
3. ✅ **Prueba de fuego ejecutada** — **primer ciclo real**: `ciclo-20260908-042126-737037`
   (5 oráculos Economic/Social/Environmental/Futurist/Dissident; NVIDIA V4 Flash + DeepSeek;
   **consenso 100% · quórum OK · estado EJECUTABLE**). Las propuestas citan fuentes reales
   (`PLAN_ENDURECIMIENTO_SEGURIDAD.md` §3, `ETICA_LENGUAJE_COMUN_CATEGORIA.md` §5,
   `GAMIFICACION_CIUDAD_APRENDIZAJE.md` §4, agenda §5…) y las firmas de comprensión citan el
   canon textual (INV1 con fórmula, T13, T16 alias, "los axiomas son el esqueleto; la ternura
   es el corazón"). **Contraste clave**: sin canon en contexto los mismos modelos inventaron
   INV3; con canon, comprensión genuina. Elegidas del ciclo: (1) InfoTip "plaza hablable" →
   matching/vhv/micromax/contracts; (2) seguridad 30-90 días (logging JSON + Redis);
   (3) Rondas anti-δ en la Ciudad del Saber.
4. Tests + commit convencional + entrada en `atribuciones_sinteticas.md`. *(commits hechos;
   la atribución se completa al cerrar la jornada)*

**Día 2 — Primer ciclo real completo**

1. ✅ **F3 ejecutada (03-09-2026)**: el Concilio eligió "Plaza Hablable" y se implementó —
   InfoTip + lenguaje civil en `/matching`, `/vhv/calculator`, `/vhv/parameters`, `/micromax` y
   `/contracts` (tsc limpio; registro en `mapa_frontend_ola4.md` §6).
2. F4 (revisión cruzada) y F5 (ratificación del custodio) — el merge espera a Max: el trabajo vive
   en el working tree con commit convencional; revertible.
3. Pendientes del ciclo votado: seguridad 30-90 días (logging JSON + Redis), Rondas anti-δ.

**Criterios de éxito del piloto**: ≥1 ciclo completo con firma T13; ≥2 proveedores distintos votando;
suite en verde; ≥1 aporte ratificado por el custodio; cero mutaciones sin revisión; bitácora auditable.

---

## 7. Riesgos y guardarraíles

**Decreto de autonomía del custodio (03-09-2026, Max):** *"el Concilio puede tocar código solo;
blindar la plataforma contra comandos que atenten contra el historial de git; del resto, por ahora
confiamos."* — traducido a arquitectura (commit `b4033b9`):

- `maxocontracts/concilio/git_guard.py`: bloquea push `--force`/`-f`/`--force-with-lease`, refspec
  `+rama`, borrado de refs, `commit --amend`, `rebase`, `reset --hard`, `clean -f*`,
  `checkout --force`, `fetch --force`, `reflog delete|expire`, `gc --prune`, `filter-branch/-repo`.
- `maxocontracts/concilio/executor.py`: ejecuta comandos con el guard activo y bitácora T13
  (bloquea antes de ejecutar: `GuardDeniedError`; fail-closed ante comillas rotas).
- Hook `pre-push` (instalado vía `scripts/instalar_guardas_git.py`): bloquea cualquier push que no
  sea fast-forward (reescritura) o que borre una ref remota — **la memoria publicada no se destruye**.

| Riesgo | Guardarraíl (fuente canónica) |
|---|---|
| **Alineación cínica** (los modelos se copian entre sí en consultas encadenadas) | Consultas independientes antes de mostrar consenso (el patrón Disidente de segunda pasada de `voting_oracle.py` debe usarse con cuidado aquí); proveedores de familias distintas; el AVA exige razonamiento propio (G3) |
| **Deriva de misión** | Mandato hashado + caducidad + presupuesto + alcance `forbidden` explícito + revisión de cierre (custodia §2.5, §3) |
| **Cuota agotada / proveedor caído** | Degradación elegante: cadena de motores; fallback local Jan; registro del motor usado (patrón existente) |
| **Privacidad** | Contexto mínimo; nunca datos de participantes a free tiers que entrenan con datos (Gemini/Mistral); redacción + context hash (custodia §2.6) |
| **Máquina legislando** | P3 jamás en solitario; ratificación humana en F5; "el canon no se delega a una máquina" (decisión M16) |
| **Edición viva sin revisión** | `scratch/` primero; merges humanos; regla de oro RLM |
| **Alucinación de fuentes** | G1 con grep de verificación (lección del mapa de coherencia §3.3: el RLM resume, el grep confirma) |
| **Identidad que cambia de modelo** | OCI: la identidad es mandato+proveedor+modelo+estado; cambiar de modelo sin re-autorización = suplantación (continuidad de identidad §5) |

---

## 8. Lo que necesito de ti (para arrancar)

1. **Decidir proveedores a registrar** (recomendado: NVIDIA Build + OpenRouter + Gemini + Groq;
   Cerebras opcional; DeepSeek actual y Jan local se quedan como escalones 1 y último).
2. **Crear las claves**: NVIDIA (build.nvidia.com), Google (aistudio.google.com), Groq
   (console.groq.com) — todas gratuitas y sin tarjeta; OpenRouter ya existe. *Las claves van al
   `.env` del repo (gitignore) y nunca a la conversación.*
3. **Autorizar el modo**: piloto en **Recomendación (C1)** + **Acción reversible en scratch (C2)**;
   producción y merge quedan en tus manos (C3 requiere doble control).
4. **Ventana de trabajo** (al iniciar sesión del PC, horario preferido, límite de sesiones/día,
   máximo de requests/día).

---

## Referencias internas

- `docs/architecture/administracion_humano_sintetica.md` — aptitud, jerarquía de autoridad, C0–C4.
- `docs/architecture/sesiones_custodia_sintetica.md` — contrato de sesión, modos de autonomía, P0–P3, bitácora.
- `docs/architecture/continuidad_identidad_autogobierno_federado.md` — OCI, anti-suplantación por cambio de modelo.
- `docs/architecture/atribuciones_sinteticas.md` — memoria pública y regla "verificable o no se escribe".
- `docs/architecture/informe_reino_sintetico_2026-08-12.md` — estado de derechos sintéticos.
- `docs/architecture/mapa_coherencia_ola4.md` y `mapa_trazabilidad_canonica.md` — mapas vivos.
- `docs/architecture/requisitos_fase2_ola4.md` — backlog (RF-I9 oráculo, RF-K1 ledger, NFR-5/8).
- `app/voting_oracle.py`, `app/synthetic_sessions.py`, `maxocontracts/oracles/base.py` — código a extender.
- `docs/SESION_NEXT_PROMPT.md` — handoff vigente (885/885 raíz; 78/78 plataforma; 8/8 puente; 02-09-2026).

## Referencias externas (verificar cambios de límites al registrar)

- NVIDIA Build: <https://build.nvidia.com/> · `integrate.api.nvidia.com/v1` — 40 RPM, sin límite diario reportado (yangmao.ai, cheahjs).
- OpenRouter: <https://openrouter.ai/docs/api_reference/limits> — 20 RPM / 50 req/día; $10 único → 1.000/día.
- Google AI Studio: <https://ai.google.dev/gemini-api/docs/rate-limits>.
- Groq: <https://console.groq.com/docs/rate-limits> · 30 RPM / 6k TPM free.
- Cerebras: <https://cloud.cerebras.ai> · 30 RPM / 14.4k req-día por modelo.
- Mistral: <https://console.mistral.ai> · Experiment plan: 1 RPS / 500k TPM / 1B tok-mes por modelo.
- GitHub Models: <https://github.com/marketplace/models> · 15 RPM / 150 RPD.
- Agregadores mantenidos: <https://github.com/cheahjs/free-llm-api-resources>, <https://yangmao.ai/en/>.
