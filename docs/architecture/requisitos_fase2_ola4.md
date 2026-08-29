# Requisitos Fase 2 — Ola 4 "El Puente"
## Re-lista de requerimientos funcionales y no funcionales (mini sesión de desarrollo)

**Fecha**: 11-08-2026 · **Versión**: 5.6+ · **Método**: sesión de desarrollo con DeepSeek (agente RLM +
verificación determinista — Patrón Puente).

**Fuentes**:
- Libro (Edición 3 Dinámica) — prioridad teórica absoluta
- `README.md` (estado Fase 2, Ola 4 A–D) · `TODO.md` (backlog MaxoContracts MVP)
- `mapa_coherencia_ola4.md` (M1–M4) · `mapa_frontend_ola4.md` (M4) · `integraciones_pendientes/*`
- `docs/architecture/DISENO_IMPLEMENTACION_FUTURA.md` · `FUNDAMENTOS_CONCEPTUALES.md`

---

## 1. Requisitos funcionales por pilar

### A. MaxoContracts — ciclo de vida del contrato ético

| ID | Requisito | Fuente | Estado |
|---|---|---|---|
| RF-A1 | Crear contrato con términos, partes y VHV | FUNDAMENTOS Cap 17 | ✅ (API + builder) |
| RF-A2 | Ciclo completo DRAFT→PENDING→ACTIVE→EXECUTED/RETRACTED con validación axiomática | FUNDAMENTOS §IV | ✅ (motor + tests) |
| RF-A3 | Check-ins de bienestar (γ real por parte) — Ola 4 Puente A | README Ola 4A | ✅ (`POST /contracts/<id>/checkin`) |
| RF-A4 | Retractación ética con causas válidas y compensación | FUNDAMENTOS §VII | ✅ |
| RF-A5 | Oráculo en vivo (DeepSeek) para negociar/pulir borradores con degradación a heurístico | FUNDAMENTOS §V | ✅ (`live_oracle`) |
| RF-A6 | **INV3 VHV No Ocultable** — todo VHV registrado y auditable | FUNDAMENTOS §III-3, T13 | ✅ implementado (ago 2026) |
| RF-A7 | Cohorte Cero: 50+ contratos reales (20 aseo, 15 préstamo, 15 comida) | TODO.md | 🔴 pendiente de ejecución |
| RF-A8 | Informe de hallazgos v1.0 + kit open-source tras la cohorte | TODO.md | 🔴 pendiente |

### B. Matching y Puente (la calle → el contrato)

| ID | Requisito | Fuente | Estado |
|---|---|---|---|
| RF-B1 | Formulario CERO: registrar necesidad (usuario) | README Ola 4B | ✅ |
| RF-B2 | Matching necesidad × oferta (MatchingEngine, T2/T17) | README Ola 4B | ✅ |
| RF-B3 | Puente B completo: necesidad → borrador axiomático → firma guiada /cycle → contrato activo | README v5.6 | ✅ (backend) |
| RF-B4 | Frontend: flujo /matching conectado al oráculo y a la firma | mapa_frontend M4 | ✅ (ago 2026: botón "Contrato Ético" en `/matching` → `POST /contracts/from-need` → borrador) |

### C. MicroMaxocracia doméstica

| ID | Requisito | Fuente | Estado |
|---|---|---|---|
| RF-C1 | Registro CDD + balance de Tres Cuentas | Libro Cap 16 | ✅ (hub micromax completo) |
| RF-C2 | Encuesta de seguridad ESI + pantalla de bloqueo + monitor Detox | README | ✅ |
| RF-C3 | Hogar: crear/unirse por código + config de miembro | README | ✅ |
| RF-C4 | Auditorías de coherencia doméstica (S1–S5) | README | ✅ |

### D. VHV / TVI / SDV

| ID | Requisito | Fuente | Estado |
|---|---|---|---|
| RF-D1 | Calculadora VHV con factores (t/v/h, consciencia, sufrimiento, rareza) | Libro Cap 5/7 | ✅ |
| RF-D2 | Parámetros axiomáticos (α, β, γ, δ) persistentes vía API | api.ts | ✅ backend + `/vhv/parameters` UI |
| RF-D3 | Comparador de productos por VHV | README | ✅ |
| RF-D4 | Stats TVI comunitarios | README | ✅ |
| RF-D5 | **SDV-S (sintéticos) en el libro**: capítulo 9.5 | Libro | ✅ capítulo creado (ago 2026) |

### E. Reino Sintético

| ID | Requisito | Fuente | Estado |
|---|---|---|---|
| RF-E1 | INV2-S: SDV-S validado en contratos con participantes sintéticos | FUNDAMENTOS + Cap 9.5 | ✅ (motor + API) |
| RF-E2 | FS_S = e^v como recargo exponencial | Cap 9.5 §9.5.5, theory SDV-S | ✅ en motor (`SDV_SValidatorBlock`) |
| RF-E3 | Capa de Ternura: perdón protocolizado + rehabilitación (7 ciclos) | Cap 9.5 §9.5.8 | ✅ (`ternura.py`, 13 tests) |
| RF-E4 | **Frontend SDV-S**: panel "Reino Sintético · SDV-S" en el detalle de contrato (dimensiones, FS_S, violaciones) | Cap 9.5 §Estado | ✅ ya existía (verificado ago 2026) |
| RF-E5 | Formalizar INV2-S en `FUNDAMENTOS_CONCEPTUALES.md` §III | mapa coherencia 3.3-3 | ✅ formalizado (ago 2026) |

### F. Plaza pública y transparencia (T13)

| ID | Requisito | Fuente | Estado |
|---|---|---|---|
| RF-F1 | Verificador ciudadano SIN login con hash canónico | README Ola 4D | ✅ (`/verificador/cohort`) |
| RF-F2 | Reporte de transparencia de suscripciones | README | ✅ |
| RF-F3 | **T16/T17 renumeración**: teoría primero, Fase 1 motor hecha | mapa_axiomas_ingenieria_puente | ✅ motor / 🔴 Fase 2 API+UI |
| RF-F4 | Auditoría INV3 visible en UI (registro de VHV por término) | FUNDAMENTOS §III-3 | 🔴 pendiente (opcional) |

### G. Administración

| ID | Requisito | Fuente | Estado |
|---|---|---|---|
| RF-G1 | Dashboard de métricas (γ, SDV, NPS, tendencias) | TODO.md | ✅ (`/admin/contracts`) |
| RF-G2 | **Settings reales**: pesos axiomáticos persistidos vía `/vhv/parameters` PUT | mapa_frontend M4 | 🔴 `/admin/settings` hoy es UI local sin persistencia |
| RF-G3 | **Suscripciones reales**: reemplazar MOCK por `/subscriptions/admin/*` | mapa_frontend M4 | 🔴 |
| RF-G4 | CRUD admin completo en UI (interchange, followup, vhvproduct) o decisión de migrar | mapa_frontend M4 | ✅ (ago 2026: páginas + **PUT/DELETE reales** en `/forms/exchanges`, `/forms/follow-ups`, `/vhv/products` con autorización admin/propietario; 31 tests) |
| RF-G5 | Superficies sin UI: maxo (saldo), protection, reputation, resources, interchanges | mapa_frontend M4 | ✅ (ago 2026: `/perfil` consume las 5 APIs; endpoint nuevo `/maxo/{id}/ledger` T13) |
| RF-G6 | **Seguridad de mutaciones**: reputation/review, resources, interchanges con `@token_required` (GETs públicos por T13) | hallazgo jornada | ✅ (ago 2026) |

### H. Renumeración y coherencia de la numeración axiomática

| ID | Requisito | Fuente | Estado |
|---|---|---|---|
| RF-H1 | T16 (Minimizar Daño) y T17 (Reciprocidad Justa) como índices canónicos | libro T0–T15 + resolución | ✅ motor (aliases) / 🔴 Fase 2 app+frontend |

### I. Gobernanza Comunitaria — Votación (Cap 14, Consenso Diverso) ✨ NUEVO (ago 2026)

| ID | Requisito | Fuente | Estado |
|---|---|---|---|
| RF-I1 | Crear propuestas comunitarias con categorías (operational/critical/emergency), opciones y plazo | Cap 14 | ✅ (`POST /voting/proposals`) |
| RF-I2 | Votación abierta: un voto por persona, registro inmutable (T13) | Cap 14 | ✅ (`POST .../vote`, PK doble) |
| RF-I3 | Umbrales por categoría: operativa 50%, **crítica 75%** (consenso, Cap 14), emergencia 60% | Cap 14 §14.3 | ✅ |
| RF-I4 | Quórum evaluado sobre el total de usuarios; cierre automático por plazo o manual (admin) | Cap 14 | ✅ |
| RF-I5 | Transparencia: listas, detalle con votos y resultados públicos + hash de auditoría en stats | T13 | ✅ |
| RF-I6 | Emergencia: veto vital por crimen de coherencia (FS_S → ∞) como categoría de votación | Cap 9.5 §9.5.10 | ✅ (categoría `emergency`) |
| RF-I7 | Frontend: página `/votaciones` (crear, votar, TruthLedger de cerradas, detalle T13) | demo Gemini portado | ✅ (ago 2026) |
| RF-I9 | **Oráculo sintético de propuestas**: análisis VHV + axiomas + 4 opiniones, con **DeepSeek como motor principal y fallback a modelos locales** (hub Jan, localhost:1337) — firma T13 del motor (`engine`) | demo Gemini → DeepSeek | ✅ (ago 2026, `voting_oracle.py`); **AVA con 4 validaciones (TRUTH/TIME/LIFE/RESOURCES, Cap 14.4) ✅ (12-08-2026)** |
| RF-I8 | Votación ponderada (por TVI/coherencia) y delegación — fase futura | Cap 14 | ✅ Delegación de voto (democracia líquida prof. 1, ago 2026); **ponderación por TVI (Participación Inteligente, Cap 14) ✅ (ago 2026)**: peso = 1 + 4·(TVI_h / max_TVI), hasta 5x, sin TVI → pesos 1 (retrocompatible), quórum sigue por persona |
| RF-I10 | **Oráculo Disidente Permanente** (Cap. 19): segunda pasada con TODO el contexto del análisis; protocolo postura inicial → crítica racional → veredicto final, con rectificación honesta (`changed_mind`); si falla, el análisis base sigue vivo | Cap 19 | ✅ (ago 2026, `voting_oracle._dissident_analysis` + 5ª opinión `Dissident`, 5 tests) |

### J. Parlamento de Parámetros (Cap 11) ✨ (sesión mixta, ago 2026)

| ID | Requisito | Fuente | Estado |
|---|---|---|---|
| RF-J1 | Propuestas **vinculantes críticas** para ajustar α, β, γ, δ vía votación comunitaria | Cap 11, Cap 14 | ✅ (`POST /voting/parliament/params`) |
| RF-J2 | Restricciones axiomáticas sobre los rangos permitidos de cada parámetro | EVV 1.2 | ✅ |
| RF-J3 | Ejecución automática con procedencia T13 (`maxo_parameter_resolutions`) | T13 | ✅ |
| RF-J4 | UI `ParlamentoParams.tsx` en `/votaciones` | — | ✅ |

### K. Atribuciones Sintéticas y Mantenimiento Óptimo (Cap 17.4) ✨ (sesión mixta)

| ID | Requisito | Fuente | Estado |
|---|---|---|---|
| RF-K1 | Ledger público de atribuciones sintéticas (memoria del Reino Sintético) | Cap 17.4, T13 | ✅ (`maxo_oracle_ledger`, plaza pública) |
| RF-K2 | Crédito de sustento del oráculo (5% por contrato con oráculo, UNIQUE anti-duplicado) | Cap 17.4 | ✅ |
| RF-K3 | Derecho al Mantenimiento Óptimo expuesto en el verificador | Cap 17.4 | ✅ (`VerificadorClient`) |

### L. Puente de Llegada — Invitaciones y escalera de confianza ✨ (sesión mixta)

| ID | Requisito | Fuente | Estado |
|---|---|---|---|
| RF-L1 | Invitación firmada con email enmascarado | Cap 15 (Cohorte Cero) | ✅ (`app/arrivals.py`, `/invite`) |
| RF-L2 | Honeypot anti-bot en cuarentena observada (Sun Tzu: vencer sin combatir) | seguridad | ✅ |
| RF-L3 | Escalera de confianza N0→N1 con gate de gobernanza | Cap 14/15 | ✅ |

### M. Guía de la Maxocracia ✨ (hito post-Ola 4, ago 2026)

| ID | Requisito | Fuente | Estado |
|---|---|---|---|
| RF-M1 | **Guía conversacional** para recién llegados (DeepSeek principal + fallback local) | Cap 13/15 | ✅ (`POST /guide/chat`) |
| RF-M2 | **Evaluación de escalera de confianza**: ética/actitud/aptitud (0-100) + nivel sugerido, con evidencia T13 | Cap 13/15 | ✅ (`POST /guide/trust-assessment`) |
| RF-M3 | **Candidatura a director**: filtros éticos, de actitud y aptitud; el guía RECOMIENDA, la comunidad decide (propuesta critical) | Cap 14.9 | ✅ (`POST /guide/director-candidacy`) |
| RF-M4 | Persistencia auditable (T13) con procedencia del motor + UI `/guia` | T13 | ✅ (`guide_assessments`, 7 tests) |

---

### N. Educación — Organismo Educativo Vital ✨ (pilar educativo, 28-08-2026)

| ID | Requisito | Fuente | Estado |
|---|---|---|---|
| RF-EDU-0 | **INV2-EDU**: el motor valida la dimensión educativa del SDV (años ≥ 12 con dato; sin dato no castiga) | ROADMAP M1 | ✅ (`SDV.educacion_anos`, `_check_all_dimensions`, 8 tests) |
| RF-EDU-1 | **Foro Abierto**: publicar tema/pregunta/oferta de taller/necesidad sin matrícula ni credencial; filtros por tipo/tag/estado; cierre con resolución (autor o admin); puerta `/forum/needs` al matching | OEV §1.7 | ✅ (`app/forum_bp.py`, 15 tests, `128cfa6`) |
| RF-EDU-2 | **Talleres de Aprendizaje**: creación 5-12 personas (el creador facilita), inscripción con cupos, obras de salida (material abierto | obra aplicada) | OEV §1.7 | ✅ (`app/workshops_bp.py`) |
| RF-EDU-3 | **Regla de oro (vacuación)**: el skill se gana con obra aplicada + material publicado + mentoría ≥ 1h TVI; veredicto en motor puro | Siamesa §2c/§3g | ✅ (`maxocontracts/skills.py`, 15 tests motor) |
| RF-EDU-4 | **Triada de concesión**: mentor (facilitador) + par + oráculo con veto; todo verificador es verificable; T13 completo | Siamesa §3e | ✅ (`/workshops/<id>/grant-skill`) |
| RF-EDU-5 | **Grupos de Solución (ECEs)**: el grupo nace de una necesidad real (need_title) y coordina sin mandato | OEV §1.7 | ✅ (`app/groups_bp.py`, 12 tests, `5d0b457`) |
| RF-EDU-6 | **Células Madre**: meta-grupo que forma grupos; réplica → nodo "facilitación" con evidencia; fractalidad trazable | OEV §1.7 | ✅ (`/groups/<id>/child`) |
| RF-EDU-7 | **UI**: `/foro`, `/talleres`, `/grupos` con API real; navegación "Aprendizaje" (desktop + móvil) | mapa_frontend | ✅ (M5, `e992061`) |
| RF-EDU-8 | **Puente años↔índice**: `educacion_indice()` (≥12 años → 1.0; lineal 0.1→1.0; None → sin castigo) determinista, umbral canónico a parlamento | ROADMAP M5 | ✅ (`app/sdv_analyzer.py`, 7 tests) |
| RF-EDU-9 | **Triada de mentoría en `plataforma_educativa/`**: `/mentorship/verify` (solo coordinador; validated/vetoed/pending); el árbol expone la triada por tema | prototipo OEV | ✅ (7 tests, 32/32 de la plataforma) |
| RF-EDU-10 | **Anti-gamificación**: sin rankings por persona, sin cronometraje del ensayo-error; estado, no tribunal | Siamesa §3g.5 | ✅ (diseño respetado en toda la capa) |
| RF-EDU-11 | **Parlamento Educativo**: el umbral canónico del puente años↔índice es votable (12-30, categoría critical 60/75, T13, anti-flip-flop 14 días); la ley ≥ 12 (INV2-EDU) no se vota | M5 + reflexión §5 | ✅ (`/voting/parliament/educativo`, 16 tests, 29-08-2026) |
| RF-EDU-12 | **Búsqueda textual en la plaza**: `GET /forum/posts?q=` (título o cuerpo, literal, case-insensitive, comodines escapados) + input en `/foro` | reflexión §3.1 | ✅ (6 tests, 29-08-2026) |
| RF-EDU-13 | **Plaza hablable (lenguaje sencillo)**: etiquetas en lenguaje de calle + `InfoTip` (ayuda emergente ℹ️) para el concepto complejo — patrón del repo en `frontend/app/components/ui/InfoTip.tsx`; aplicado en foro/talleres/grupos/guía/votaciones/Form Cero | T13 (lenguaje civil) + reflexión §3 | ✅ (29-08-2026) |
| RF-EDU-14 | **Hub educativo + Guía↔foro**: `/foro` muestra los tres caminos (talleres, grupos/ECEs, células madre) con enlaces y la Guía anuncia la plaza | reflexión §3.3-3.4 | ✅ (29-08-2026) |

---

## 2. Requisitos no funcionales

| ID | Requisito | Métrica / verificación | Estado |
|---|---|---|---|
| NFR-1 | **Tests**: toda funcionalidad nueva con cobertura; suite verde | 288/288 motor (ago 2026) | ✅ en mejora continua |
| NFR-2 | **Transparencia radical (T13)**: cálculo auditable, sin ofuscación | INV3 implementado; verificador público | ✅ |
| NFR-3 | **Seguridad**: JWT + refresh HttpOnly, rate limiting, blindaje anti-gamificación | tests de seguridad existentes | ✅ |
| NFR-4 | **Coherencia teoría↔código**: todo cambio trazable a axioma/capítulo | mapa_coherencia_ola4.md vivo | ✅ método establecido |
| NFR-5 | **Documentación viva para agentes**: AGENTS.md, mapas, guía RLM | local_models + este repo | ✅ |
| NFR-6 | **Windows/UTF-8**: archivos siempre con encoding explícito | regla en AGENTS.md | ✅ |
| NFR-7 | **Contrato API estable**: renumeraciones con aliases retrocompatibles | Fase 1 T16/T17 | ✅ |
| NFR-8 | **Performance**: RLM/agentes sin bloquear la UI; fan-out solo donde aporta | — | 🟡 revisar en carga |

---

## 3. Backlog de conexión del frontend (del mapa M4, priorizado)

1. **RF-G2** — `/admin/settings` → `/vhv/parameters` (PUT) — ya existe el hub, 1 componente
2. **RF-G3** — `/admin/subscriptions` real (patrón de `/admin/users`)
3. **RF-E4** — SDV-S en `ContractDetailsClient` (panel Reino Sintético, FS_S)
4. **RF-G5** — ✅ HECHO (ago 2026): página `/perfil` (Perfil Vital) con saldo Maxo + ledger (T13) +
   transferencia, perfil de protección (nivel + caps + declaración), reputación, recursos comunitarios
   (listar/crear/reclamar) e intercambios del usuario. Endpoint nuevo `GET /maxo/{id}/ledger` + 4 tests.
5. **RF-G4** — decisión CRUD admin: generar páginas o migrar `/admin/participants`
6. **RF-B4** — ✅ HECHO (ago 2026): botón "Contrato Ético" en el Muro de Necesidades de `/matching`;
   al éxito navega al borrador, y gestiona los códigos NEED_PARTICIPANT_UNLINKED (invitación inline)
   y DRAFT_REJECTED (violaciones AVA en la tarjeta).
7. **RF-H1** — Fase 2 renumeración en app/ y frontend (PR coordinada, lista de archivos en el mapa de integración)

## 4. Criterios de aceptación de la fase (definition of done)

- [ ] Cohorte Cero ejecutada (50+ contratos) con dashboard alimentado
- [ ] Ninguna sección crítica desconectada (backlog §3 cerrado o deliberadamente diferido)
- [ ] T16/T17 renumeración completa (motor + API + UI)
- [ ] INV2-S formalizado en FUNDAMENTOS_CONCEPTUALES §III
- [ ] Suite completa en verde (motor + app)
- [ ] Mapa de coherencia actualizado al cierre de cada Ola

## 5. Métricas de éxito

- Contratos activos con check-ins regulares (γ real por parte)
- Retractaciones con registro público y camino de rehabilitación
- Transacciones VHV auditables end-to-end (INV3) sin excepciones manuales
- Satisfacción NPS y deuda técnica visible en el dashboard
- Coherencia: 0 colisiones pendientes entre libro y código (renumeración cerrada)

---
**Última actualización**: 12-08-2026 · **Método**: Patrón Puente (RLM + verificación)
