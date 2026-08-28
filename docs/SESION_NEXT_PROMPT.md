# SESIÓN NEXT — Handoff de la jornada (última actualización: 22-08-2026, ox-alpha)

Documento de continuidad entre sesiones. Léelo al iniciar la próxima sesión
antes de tocar código. Mantenlo actualizado al cerrar cada jornada.

---

## 1. Prompt para Max (pegar en la próxima sesión)

> Continuamos la Maxocracia desde donde quedamos (ver `docs/SESION_NEXT_PROMPT.md`).
> Contexto: Fase 2 — Ola 4 "El Puente", versión 5.6+. El sistema de gobernanza comunitaria
> está completo (propuestas por categoría con quórum y consenso 75%, oráculo DeepSeek con
> fallback local, delegación de voto, parlamento de parámetros vinculante). El Puente de
> Coherencia (mapa teoría↔código) está en `docs/architecture/mapa_coherencia_ola4.md` y los
> requisitos en `docs/architecture/requisitos_fase2_ola4.md`.
> Patrón de trabajo: RLM navega + director verifica + teoría decide (guía en el repo
> local_models: `docs/GUIA_RLM_COLABORADOR.md`).
> Revisa los pendientes del §4 y elige el siguiente paso con criterio; commits regulares
> en español; respeta el principio "la teoría tiene prioridad".

## 2. Briefing para el agente (opencode / DeepSeek)

**Estado actual (12-08-2026, jornada mixta de dos sesiones):**

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
| **Rama educativa M1-M7** (28-08-2026, sesión con Max): INV2-EDU ya en motor; **M2 Foro Abierto** (`app/forum_bp.py` + **respuestas** `forum_replies`, 22 tests), **M3 Talleres + regla de oro** (`maxocontracts/skills.py` — vacuación: obra + material + mentoría ≥1h TVI, triada mentor+par+oráculo con veto; `app/workshops_bp.py`), **M4 Grupos/ECEs + Células Madre** (`app/groups_bp.py`, fractalidad → nodo "facilitación", 12 tests), **M5 UI** `/foro` `/talleres` `/grupos` + nav "Aprendizaje" + puente `educacion_indice()` (años↔índice, 7 tests), **M6 árbol de habilidades** (`maxocontracts/tree.py` — SkillTree con caminos de maestría y forks, 20 tests), **M7 Form Cero con años** (`educacion_anos` 0-60 en participants + migración idempotente + puente vivo en `estimate_participant_sdv`; 12 tests; revisado por MiniMax) · miniMax redactó la guía del foro (`docs/guides/guia_foro_abierto.md`) | ✅ M1-M7 + docs · 🔴 pendientes: matching↔foro, umbral del puente al parlamento |
| Suite de tests | **818/818** (verificado 28-08-2026 tras M6 árbol de habilidades; plataforma educativa 32/32 en su propio venv/contexto — excluida de la recolección raíz vía `pytest.ini` `norecursedirs`) |

**Decisiones canónicas a respetar:**
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

## 3. Cómo verificar al arrancar

```powershell
# Backend (cwd = raíz del repo)
.venv\Scripts\python.exe -m pytest tests/test_voting.py tests/test_maxocontracts/test_parliament.py -q
.venv\Scripts\python.exe -m pytest tests/test_validador_conceptual.py -q   # coherencia axiomática

# Frontend (cwd = frontend/)
npx tsc --noEmit
```

## 4. Pendientes priorizados

**El backlog de la Ola 4 está CERRADO (12-08-2026, sesión continua).** Estado final:

1. ~~Cohorte Cero real~~ ✅ **EJECUTADA**: 50 contratos en `comun.db` via `scripts/seed_cohorte_cero.py`
   (20 aseo, 15 préstamo, 15 comida; 294 check-ins, 40 NPS; γ 1.099, NPS 57.5 en `/admin/contracts`)
2. ~~RF-G4~~ ✅ páginas `/admin/interchanges`, `/admin/followups`, `/admin/vhvproducts` (solo lectura
   + detalle; faltan PUT/DELETE backend para mutación — candidato a futura ola)
3. ~~RF-I8~~ ✅ votación ponderada por TVI (Participación Inteligente, Cap 14): peso 1+4·(TVI/max) hasta
   5x, retrocompatible, quórum por persona; badge en `/votaciones`
4. ~~M4 fase 2 / RF-B4~~ ✅ botón "Contrato Ético" en `/matching` → `POST /contracts/from-need`
5. ~~SDV-S editorial~~ ✅ 8 referencias cruzadas del cap. 9.5 en caps. 10/11/13/14
6. Mantener mapas y handoff al día (regla continua)

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
**Mantenido por**: Max + DeepSeek (opencode) · **Próxima actualización**: al cierre de la siguiente sesión
