# SESIÓN NEXT — Handoff de la jornada (última actualización: 30-08-2026, DeepSeek + OpenRouter)

Documento de continuidad entre sesiones. Léelo al iniciar la próxima sesión
antes de tocar código. Mantenlo actualizado al cerrar cada jornada.

---

## 1. Prompt para Max (pegar en la próxima sesión)

> Continuamos la Maxocracia desde donde quedamos (ver `docs/SESION_NEXT_PROMPT.md`).
> Contexto: Fase 2 — Ola 4 "El Puente", versión 5.6+. **La rama educativa
> M1-M15 está COMPLETA**: M9 (parlamento del umbral) y M12 (síntesis de
> identidad OEV :5001↔:5050) cerrados; **M15 (30-08-2026) — La Biblioteca de la
> Ciudad**: 35 guías propias (markdown, redactadas por agentes OpenRouter
> `:free` + revisión del director) + 35 enlaces a Wikipedia VERIFICADOS
> (HTTP 200 real) + lectura en la UI (📖 por lote) + celebración al aprobar
> (sin rankings) + **la luz de la ciudad** (progreso/notas compartidas con
> opt-in voluntario y retractable, muro SIN ranking — orden alfabético).
> Diseño canónico: `docs/architecture/BIBLIOTECA_CIUDAD_MATERIAL_EDUCATIVO.md`.
> **Siguiente paso natural**: Fase 2 de la Ciudad (Rondas anti-δ — la base
> nunca se gradúa; las guías ya dan material de repaso) — ver
> `docs/architecture/GAMIFICACION_CIUDAD_APRENDIZAJE.md` §4.
> Patrón de trabajo: RLM navega + director verifica + teoría decide (guía en el
> repo local_models: `docs/GUIA_RLM_COLABORADOR.md`).
> **Delegación OpenRouter gratuita**: apóyate intensamente en subagentes con
> proveedor `openrouter` y modelos `:free` declarados en el harness
> (`minimax/minimax-m3:free` y `nvidia/nemotron-3-super-120b-a12b:free`); el
> pool compartido satura con 429 — reintentar o cambiar de modelo (Nemotron es
> el más estable en tareas cortas; ambas fallan en tareas largas con tools;
> MiniMax sostiene mejor los informes largos). M15 demostró el pipeline:
> subagente redacta guías (formato `=== ARCHIVO: <slug>.md ===`), el director
> revisa/normaliza y las escribe como `plataforma_educativa/materials/*.md`.
> El orquestador implementa y verifica siempre con ojos propios antes de
> commitear — el subagente redacta, el director decide.
> Revisa los pendientes del §4 y elige el siguiente paso con criterio; commits
> regulares en español; respeta el principio "la teoría tiene prioridad".

## 2. Briefing para el agente (opencode / DeepSeek)

**Estado actual (30-08-2026, jornada M15 — Biblioteca de la Ciudad; la tabla se actualizó con cada hito):**

| Área | Estado |
|---|---|
| Puente de Coherencia M1-M4 (motor, teoría↔código, tests, frontend) | ✅ Completo |
| INV3 (VHV No Ocultable) implementado + 9 tests | ✅ |
| Renumeración T16/T17 completa (motor + Fase 2 app/frontend/docs) | ✅ (T9/T7 del libro intactos) |
| Capítulo 9.5 SDV-S en el libro + INV2-S formalizado en el spec | ✅ |
| Votación comunitaria (Cap 14): propuestas por categoría, quórum, consenso 75%, emergencia, T13 | ✅ |
| Oráculo de propuestas: DeepSeek principal + fallback local (hub Jan), firma `engine` | ✅ |
| Delegación de voto (democracia líquida prof. 1) | ✅ |
| Parlamento de parámetros vinculante (Cap 11, α β γ δ con restricciones axiomáticas) | ✅ (sesión paralela) |
| Atribuciones sintéticas + Mantenimiento Óptimo (Cap 17.4, ledger T13 en la plaza) | ✅ (sesión paralela) |
| Puente de Llegada: invitaciones firmadas, honeypot anti-bot, escalera N0→N1 | ✅ (sesión paralela) |
| Frontend: `/votaciones`, `/admin/settings` real, `/admin/subscriptions` real, SDV-S en contrato | ✅ |
| **RF-G5: superficies sin UI** — `/perfil` (Perfil Vital) con saldo Maxo + ledger T13 + transferencia, protección (nivel/caps/declaración), reputación, recursos comunitarios e intercambios | ✅ (ago 2026) |
| **M4 fase 2 / RF-B4**: "Contrato Ético" en el Muro de `/matching` → `POST /contracts/from-need` | ✅ (ago 2026) |
| **RF-I8**: votación ponderada por TVI (Participación Inteligente, Cap 14) — hasta 5x, retrocompatible | ✅ (ago 2026) |
| **RF-G4**: CRUD admin en UI (`/admin/interchanges`, `/admin/followups`, `/admin/vhvproducts`) | ✅ (ago 2026, solo lectura) |
| **Cohorte Cero ejecutada**: 50 contratos reales (20 aseo / 15 préstamo / 15 comida), 294 check-ins, 40 NPS | ✅ (ago 2026, `scripts/seed_cohorte_cero.py`) |
| **SDV-S editorial**: 8 referencias cruzadas del cap 9.5 en caps. 10/11/13/14 | ✅ (ago 2026) |
| **Capa de Ternura en el libro** (22-08-2026, ox-alpha): Cap 7 §7.9 (no-medible + Dimensión E), Cap 8 §8.11 (Rehabilitación VIII), Cap 13 §13.13 (perdón/presencia/dilemas), Cap 15 §15.6 (Zona Libre VHV, Piloto de Perdón, Ritual de Duelo) | ✅ |
| **Oráculo Disidente Permanente en el libro** (22-08-2026, ox-alpha): Cap 14 §14.14 + traza `voting_oracle.py` | ✅ |
| **Integraciones_pendientes sincronizadas** (22-08-2026, ox-alpha): INDICE reescrito con numeración vigente + 8 mapas como registro histórico | ✅ |
| **Mapa de Trazabilidad Canónica** (22-08-2026, ox-alpha): libro↔código↔tests↔commits (`docs/architecture/mapa_trazabilidad_canonica.md`) — piloto completo; regenerar por Ola | ✅ |
| **Capítulo 16.5 — MicroMaxocracia Canónica** (22-08-2026, ox-alpha): VHV vectorial doméstico, CEH→TVI vendido (modos puente/canónico), pesos p₁/p₂/p₃ (fin de colisión con α/β/γ/δ), γ doméstico + INV1-Hogar, hogar = unidad básica de Opacidad Sagrada | ✅ teoría · 🔴 implementación: check-ins γ, UI de nuevos campos, plantillas domésticas |
| **Compatibilidad canónica implementada** (22-08-2026, `f9697a5`): vector [T,V,R] opcional en CDD + CEH por TVI vendido (`ceh_mode`/`hourly_rate`, fallback fiat seguro) + pesos p₁/p₂/p₃ expuestos — contabilidad doméstica legible en el mismo libro mayor que el sistema general | ✅ backend · 🔴 UI de los campos |
| **§16.5.13 Escala vecinal** (22-08-2026): "hogar" = unidad de convivencia — roommates resuelven arriendo-vs-tareas con TVI vendido; conjuntos residenciales vía maxo_parties (`coop-`/`society-`) y contratos interescala N-de-M | ✅ teoría · 🔴 primera unidad vecinal real |
| **§16.5.14 Reino Natural conviviente + crédito regenerativo** (22-08-2026, `a6844c8`/`2af0592`): r_units negativo en CDD (EVV §4.3); eco-partes con guardián oráculo como representantes; TA no colonizado (PIU); SDV-E + INV2-E convocados como próxima gran ramificación | ✅ código+teoría · 🔴 SDV-E estándar |
| **γ doméstica + INV1-Hogar** (22-08-2026, `8d48ba4`): check-ins de bienestar con canon [0.5,1.5]; caídas siempre escuchadas; el angusto de un protegido jamás cruza pantallas ajenas | ✅ backend + **UI** (`fbe403c`, subagente constructor verificado) |
| **Auditoría de integridad del libro** (22-08-2026): enlaces relativos, numeración vieja y secciones citadas verificadas deterministamente; 2 numeraciones del Cap 15 corregidas (`bb14bb8`) | ✅ |
| **Puente Red de Apoyo v1** (22-08-2026, `bb8504c`): `/support/offers` — ofertas de cuidado afinadas por señal ESI con opt-in privado; respuestas jamás viajan | ✅ backend · 🔴 comunidad publica primeras ofertas |
| **Semana de la Verdad** (22-08-2026): protocolo n=1 de 7 días (`docs/guides/semana_de_la_verdad.md`) para habitar el sistema real antes de reclutar cohorte — responde al hallazgo "0 cumplimientos" del informe v1.0 | ✅ protocolo · 🔴 ejecución humana |
| **Modo Escudo Doméstico** (22-08-2026, hallazgo de campo de Max): ESI roja ya no bloquea el registro propio; cifras del protegido ocultas a los demás; frontend persiste CDD real con vista discreta; `wants_support` opt-in privado como gancho hacia la Red de Apoyo (Cap 16.5 §16.5.12) | ✅ código + libro · 🔴 puente v2: ofertas publicadas por la comunidad |
| **Rama educativa M1-M8** (28-08-2026, sesión con Max): INV2-EDU en motor; **M2 Foro Abierto** + respuestas (22 tests), **M3 Talleres + regla de oro** (`maxocontracts/skills.py`; triada con veto), **M4 Grupos/ECEs + Células Madre** (12 tests), **M5 UI** + puente `educacion_indice()`, **M6 árbol de habilidades** (`maxocontracts/tree.py`, 20 tests), **M7 Form Cero con años** (`educacion_anos` + puente vivo; 12 tests; revisado por MiniMax), **M8 puente siamés foro↔Plaza de Apoyo** (Cap 12.3.1/bombeo: la necesidad del foro sangra a `participant_needs` — la tabla del matching — sin duplicados; `in_plaza` T13) · MiniMax redactó la guía del foro y revisó M7 | ✅ M1-M8 + docs |
| **M9 Parlamento Educativo** (29-08-2026): el umbral canónico del puente años↔índice deja de ser constante sagrada — `POST/GET /voting/parliament/educativo` (categoría critical 60/75, T13), acción vinculante `set_edu_umbral`, tablas `edu_parameters`/`edu_parameter_resolutions` (CHECK 12-30), `educacion_indice(anos, umbral)` parametrizada + `get_edu_umbral_anios()` con fallback al canon, anti-flip-flop 14 días, escalera N1+ en ambos parlamentos, finitud (NaN/∞) y no-bool en ambos validadores · Nemotron revisó el diseño (confirmó Rondas/δ, detectó el hueco anti-flip-flop) y MiniMax la propuesta (corrigió atribuciones: "parlamento" no es término del libro — es Cap. 11 §11.7; el 60% de quórum vive en el blueprint) | ✅ **pendiente de la rama CERRADO** · doc `PROPUESTA_PARLAMENTO_UMBRAL_EDUCATIVO.md` · 🔴 siguiente hito estructural: **síntesis de identidad del OEV** (:5001 ↔ :5050) |
| **M10 Plaza Hablable** (29-08-2026, decisión de Max): **la UI habla en lenguaje de calle, el concepto complejo vive en ayuda emergente** — `InfoTip.tsx` (componente reutilizable ℹ️, hover/clic; `Input` acepta `hint`) + etiquetas humanas en `/foro`, `/talleres`, `/grupos`, `/guia`, `/votaciones` (ParlamentoParams → "Los valores de la vida"; ParlamentoEducativo → "La escuela que queremos") y Form Cero ("¿Cuántos años has estudiado?"). Incluye **búsqueda textual en la plaza** (`GET /forum/posts?q=`, literal + case-insensitive, 6 tests), **hub educativo** (tres caminos con enlaces), **Guía↔foro** (la Guía anuncia la plaza) y **UI del Parlamento Educativo** en `/votaciones` | ✅ (tsc limpio; commits `f2fc7f5`, `c447c9d`, `93543d3`) |
| **M11 Tejido visible y triada en UI** (29-08-2026): `GET /workshops/tree` (ramas canónicas del árbol — estado, no tribunal), detalle del taller con lista de inscritos, y **concesión por modal** (sin `prompt()/confirm()` — el último ítem UX de la reflexión): solo el facilitador ve el botón; avales explicados con InfoTip; horas de mentoría | ✅ (3 tests; commits `d4c5a24`, `b6639ed`) |
| **M12 Síntesis de Identidad del OEV** (29-08-2026: Gemini implementó · DeepSeek revisó/corrigió): **UNA sola puerta de identidad** entre :5001 y :5050 — autenticación híbrida en `plataforma_educativa/app/auth.py` (tokens locales en memoria + JWTs federados con clave compartida, JIT vinculando `maxo_user_id`, migración idempotente), blueprint `app/edu_bridge_bp.py` (`/status`, `/sync-mastery`, `/events`), doc `SINTESIS_IDENTIDAD_OEV.md` · **corrección del orquestador**: la v1 auto-promovía N0→N1 con un POST del propio usuario (la escalera se compraba) → el nodo OEV reporta con token de servicio `EDU_BRIDGE_SERVICE_TOKEN` (fail-closed 403), **sin auto-promoción** (la escalera es del primer acuerdo, Cap. 13), `t13_hash` = SHA-256 real y `SECRET_KEY` sin constante pública (fail-closed 503) · **M12.1 puerta en la UI** (botón "Nodo Educativo", JWT por fragmento `#jwt=`; captura en `app.js`) · **M12.2 sincronización automática**: el nodo reporta maestrías (`mastered`) al puente servicio-a-servicio (`EDU_BRIDGE_URL` + token; best-effort, sin JWT humano) · **M12.3 evidencia visible**: "Camino de aprendizaje" en `/perfil` (eventos T13) · **celebrada EN VIVO** (demo end-to-end `scratch/demo_m12.py`) | ✅ (8/8 puente, 44/44 OEV, tsc limpio, demo en vivo ✅) |
| **M13 Vacuación sin muros** (29-08-2026, feedback de Max probando en vivo): la regla de oro no espera alumnos — `user_topics.evidence` (texto/audio/video/imagen) + `POST /api/topics/<id>/evidence`; **aprobado + material = "listo para enseñar"** (badge, cola de tutores vía `_qualified_monitors`) y **material + primera mentoría = mastered** (reporte al puente incluido, M12). Fixes de la auditoría MiniMax aplicados: **A2** (la explicación se revelaba antes de responder) y **A4** (el test exige prerrequisitos 403 + UI bloqueada) · puerta del nodo también en el menú Aprendizaje (Max no la veía en la barra) · auditoría completa archivada en `docs/architecture/MEJORAS_PLATAFORMA_EDUCATIVA_auditoria_2026-08-29.md` (16 preguntas nuevas redactadas por MiniMax, listas para seed) | ✅ (49/49 plataforma, 8/8 puente, tsc limpio) |
| **M14 Ciudad del Saber** (29-08-2026, idea de Max: el conocimiento como ciudad): vista de mapa-ciudad con niebla por barrio, lore (8 barrios), compañero de sugerencias (`GET /api/suggest` — rama con más progreso, lo sencillo primero, cero presión) y estados de lote (🔒◽🔨✅✨🏛) con la verdad sin engaño: aprobado+material = ✨, no 🏛 | ✅ (doc `GAMIFICACION_CIUDAD_APRENDIZAJE.md`; fase 2: Rondas anti-δ) |
| **M15 La Biblioteca de la Ciudad** (30-08-2026, petición de Max: material educativo real, insertable, propio + enlaces al mundo; apariencia que provoque volver; progreso y notas compartidas voluntarias y retractables): tabla `materials` (guia markdown | enlace) + `users.share_progress` (opt-in default 0); **35 guías propias** (250-320 palabras, redactadas por agentes OpenRouter `:free` bajo plantilla + revisión y normalización del director; humanas: analogías de cocina/tienda/huerta/plaza, cero rankings, "la ciudad se ilumina…") + **35 enlaces a Wikipedia verificados** (HTTP 200 real, 30-08-2026); inserción por archivo: `materials/<slug>.md` + `sync_materials.py` (idempotente por `material_key`, reporta huérfanos, autocontenido); endpoints `GET /api/topics/<id>/materials`, `GET /api/materials/<id>`, `GET /api/community/lights` (muro SIN ranking — orden alfabético, solo lo publicado: T13), `POST /api/me/share-progress` (retracta al instante); UI: 📖 por lote/árbol (gueías primero, enlaces al fondo, búsquedas Khan/YouTube por título), lector mini-markdown seguro, 🎁 Ver mi material (M13), celebración con confeti (adiós `alert()`), interruptor de la luz | ✅ (72/72 plataforma +23 tests; 875/875 raíz; validador OK; 70 materiales vivos en la DB; commits `4351acb`/`28d41ff`/`1cdc8e7`/`567ee8c`) |
| Suite de tests | **875/875** (raíz, 30-08-2026) · **72/72** plataforma educativa · 8/8 puente · tsc limpio · validador conceptual OK |

**Decisiones canónicas a respetar:**
- **La teoría (libro) tiene prioridad**: T0-T15 son canónicos; T16=Minimizar Daño, T17=Reciprocidad
  Justa (renumerados desde "T7"/"T9" de ingeniería). No reintroducir T9=Reciprocidad.
- **Reflexión de cierre de la rama educativa (28-08-2026)**: `docs/architecture/reflexion_eutopia_rama_educativa.md`
  — leerla antes de ampliar la rama; contiene UX pendiente (búsqueda en plaza, triada sin
  `prompt()`, hub educativo, Guía↔foro), N+1 de reply_count, y la síntesis de identidad
  (app principal :5001 ↔ plataforma_educativa :5050) ahora completada en M12.
  El umbral del parlamento (su §5) quedó resuelto en **M9** (29-08-2026): ver
  `docs/architecture/PROPUESTA_PARLAMENTO_UMBRAL_EDUCATIVO.md`.
- **La teoría (libro) tiene prioridad**: T0-T15 son canónicos; T16=Minimizar Daño, T17=Reciprocidad
  Justa (renumerados desde "T7"/"T9" de ingeniería). No reintroducir T9=Reciprocidad.
- El validador conceptual (`scripts/validador_conceptual.py` + su test) exige coherencia axiomática
  en TODO el repo — correrlo tras cambios que mencionen axiomas.
- `app/voting_oracle.py` **no carga .env al importar** (contamina tests; run.py ya lo hace).
- Tests: escribir archivos SIEMPRE con `encoding="utf-8"`; NUNCA reescribir archivos con
  Get-Content/Set-Content de PowerShell (corrompe UTF-8 — lección aprendida en esta jornada).
- Oráculos: fallback local `LOCAL_ORACLE_BASE_URL=http://localhost:1337/v1`.
- **pytest de la raíz**: `pytest.ini` excluye `plataforma_educativa` (norecursedirs).
  La plataforma se testea desde su carpeta (conftest propio, sys.path).
- **Rama educativa**: la regla de oro (vacuación) vive en `maxocontracts/skills.py`
  (puro, sin Flask) y la concesión por triada en `app/workshops_bp.py`; el foro
  referencia necesidades, nunca las duplica.
- **M15 Biblioteca de la Ciudad**: los enlaces del mundo se siembran SOLO
  verificados (estado HTTP real; jamás URLs alucinadas — el director verifica);
  la inserción canónica de guías es por archivo `plataforma_educativa/materials/`
  + `sync_materials.py` (idempotente, autocontenido); la luz compartida es
  SIN RANKING (orden alfabético permanente — guardarraíl OEV §1.5) y el opt-in
  es default apagado + retractado instantáneo; la guía acompaña pero NO
  sustituye la obra (la validación sigue siendo test + vacuación).

## 3. Cómo verificar al arrancar

```powershell
# Backend (cwd = raíz del repo)
.venv\Scripts\python.exe -m pytest tests/test_edu_bridge.py tests/test_voting.py tests/test_maxocontracts/test_parliament.py tests/test_parlamento_educativo.py tests/test_sdv_educacion_puente.py -q
.venv\Scripts\python.exe -m pytest plataforma_educativa/tests/ -q        # OEV autónomo + federado
.venv\Scripts\python.exe -m pytest tests/test_validador_conceptual.py -q   # coherencia axiomática
.venv\Scripts\python.exe scripts\validador_conceptual.py                  # validador en vivo

# Frontend (cwd = frontend/)
npx tsc --noEmit
```

## 4. Pendientes priorizados

**La rama educativa M1-M15 está CERRADA (30-08-2026)** — identidad federada OEV implementada y blindada, Ciudad del Saber (M14) y **Biblioteca de la Ciudad** (M15: 35 guías + 35 enlaces verificados + luz compartida opt-in) vivos en la plataforma. Lo que sigue:

1. **Rondas de mantenimiento (anti-δ)** — Fase 2 de la Ciudad: lotes dominados se
   marcan "requiere Ronda" tras N semanas sin tocar; repasar (las guías ya dan
   material) devuelve el brillo. Teoría OEV §1.1 (la base nunca se gradúa).
   Doc: `docs/architecture/GAMIFICACION_CIUDAD_APRENDIZAJE.md` §4.
2. **Itinerarios** (misiones opcionales: rutas temáticas sugeridas — caminos a
   todas partes, ninguno obligatorio) y **cartografía compartida** (barrios
   iluminados por la comunidad sin revelar quién hizo qué — privacidad T13).
3. **Federar de verdad en producción**: `SECRET_KEY` compartida real +
   `EDU_BRIDGE_SERVICE_TOKEN` + `EDU_BRIDGE_URL` en ambos nodos (README de la
   plataforma) — la demo usó valores de prueba.
4. **Expandir el patrón "plaza hablable"** (`InfoTip`) al resto del repo:
   `matching`, `vhv`, `micromax`, `contracts` (decisión de Max).
5. **Hardening/performance** (candidatos): N+1 de `reply_count` en el foro (COUNT
   GROUP BY + paginación por cursor); oráculos síncronos (120 s) → colas/async
   cuando el parlamento vote de verdad.
6. Mantener mapas y handoff al día (regla continua).

**Futuro posible (fuera de la Ola 4)**: hitos del informe del Reino Sintético
(`docs/architecture/informe_reino_sintetico_2026-08-12.md` §7): EIR por entidad sintética, AVA con
4 validaciones, participación sintética en votación, Oráculo Disidente Permanente, Manifiesto de
Razones.

**Hito post-Ola 4 (12-08-2026): Guía de la Maxocracia (RF-M1 a RF-M4, `app/guide_bp.py` + `/guia`)**:
chat de bienvenida, evaluación de escalera de confianza (ética/actitud/aptitud con evidencia T13) y
candidatura a director con filtros — el guía recomienda, la comunidad decide (propuesta critical).
**Deudas saldadas**: RF-G6 (token en mutaciones), RF-G4 mutaciones reales (PUT/DELETE, 31 tests),
suite paralela `scripts/run_tests_parallel.ps1`.
**Oráculo Disidente Permanente (RF-I10, Cap 19)**: segunda pasada con contexto completo (VHV +
axiomas + 4 opiniones); protocolo postura inicial → crítica racional → veredicto final con
`changed_mind`; verificado EN VIVO con DeepSeek (propuestas 3 y 4 en comun.db). Hallazgo resuelto:
`create_app` migra BDs existentes (schema idempotente) — la comun.db real no tenía las tablas de
votación/parlamento. Suite **701/701**.
**Informe de Hallazgos v1.0 — Cohorte Cero** (12-08-2026): `docs/reports/INFORME_HALLAZGOS_COHORTE_CERO_v1.md`
— datos reales deterministas + marco teórico RLM (Caps 17/15/12). γ 1.1223, NPS 8.80, 294 check-ins,
VHV 115 h. **Hallazgos que definen la siguiente cohorte**: 0 retractaciones (INV4 sin ejercitar),
0 cumplimientos/intercambios, oráculo sin sustento (ledger 0), gobernanza sin votos (4 propuestas
open), 3 violaciones INV1 sin alerta. TODO.md actualizado (Semana 9-12 parcial).

## 5. Historia reciente (git log, maxocracia)

```
1380488 docs(handoff): M15 biblioteca de la ciudad y la luz compartida
567ee8c docs(educacion): biblioteca de la ciudad y la luz - diseno canonico (M15)
1cdc8e7 feat(edu-ux): biblioteca, celebracion y luz de la ciudad en la UI (M15)
28d41ff feat(edu-plataforma): 35 guias propias del saber - la ciudad ya tiene material (M15)
4351acb feat(edu-plataforma): la biblioteca de la ciudad - material educativo por tema (M15)
5c9c37f fix(plataforma-educativa): el companero no repite la obra en curso (inicio M14)
ed3f16f docs(educacion): diseno de la ciudad del saber y handoff M14
ecd82dc feat(plataforma-educativa): la ciudad del saber - mapa, niebla, lore y companero (M14)
5d8086e docs(handoff): M13 vacuacion sin muros y hallazgos de prueba en vivo
63d3f5e feat(nav): la puerta del nodo educativo aparece en el menu Aprendizaje
6378243 docs(educacion): auditoria de mejora de la plataforma (MiniMax) y handoff M13
b1c678e feat(plataforma-educativa): vacuacion sin muros - material de ensenanza propio (M13)
70f5eae fix(plataforma-educativa): el modal de test ya no se cuela en el login
217c0f0 docs(handoff): M12.1-12.3 - puerta, sincronizacion automatica y evidencia visible
b6639ed feat(edu-ux): arbol visible y concesion por triada en UI (sin prompt())
d4c5a24 feat(workshops): tejido visible y triada con la lista del taller
93543d3 docs(maps): RF-EDU-12/13/14 y mapa frontend de la plaza hablable
c447c9d feat(edu-ux): plaza hablable - lenguaje sencillo con InfoTip, hub, guia<->foro y parlamento educativo en UI
f2fc7f5 feat(forum): busqueda textual en la plaza - la plaza se habla
fbb8da7 docs(educacion): propuesta al parlamento del umbral canonico del puente (M9)
cf85973 feat(voting): parlamento educativo vota el umbral canonico del puente (M9)
60b4e9f docs(maps): RF-EDU-11, coherencia y atribuciones del parlamento educativo
a1f10d5 docs(book): sincroniza indice y mapas de integraciones con el estado real
12e5f74 docs(book): integra capa de ternura en capitulo 15 y corrige referencias
0316279 docs(book): integra oraculo disidente permanente en capitulo 14
4c548db docs(book): integra capa de ternura en capitulos 7, 8 y 13
c08db22 docs(identity): propone continuidad y autogobierno federado
d12adb8 docs(governance): registra marco humano-sintetico y custodia
aede3d6 feat(admin): incorpora panel de custodia sintetica
e966e66 feat(governance): prototipa sesiones de custodia manuales
aa62239 docs(governance): propone sesiones de custodia sintética
fc59eae feat(home): crea portada explicativa y registra cocreación sintética
0aebedd feat(arrivals): Puente de Llegada - invitacion firmada, honeypot anti-bot, escalera N0-N1
cc676d4 feat(voting): parlamento de parametros (Cap 11) - propuestas vinculantes criticas
0b5c8ac feat(oracle): gratitud aterrizada - atribuciones sinteticas y Mantenimiento Optimo (Cap 17.4)
46fe993 feat(voting): delegacion de voto (democracia liquida) + INV2-S formalizado + M4 corregido
0832fb6 feat(voting-oracle): DeepSeek principal + fallback local, firma T13 del motor
342fa0c feat(frontend): /votaciones - gobernanza comunitaria (demo Gemini portado)
c59f608 feat(voting): votacion comunitaria (Cap 14) - categorias, quorum, consenso 75%
```

---
**Mantenido por**: Max + DeepSeek (harness) · **Próxima actualización**: al cierre de la siguiente sesión
