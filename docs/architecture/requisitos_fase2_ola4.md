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
| RF-B4 | Frontend: flujo /matching conectado al oráculo y a la firma | mapa_frontend M4 | ✅ parcial — verificar /contracts/from-need en UI (RF-F5) |

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
| RF-E4 | **Frontend SDV-S**: exponer `sdv_s_actual` en detalle de contrato y builder | Cap 9.5 §Estado | 🔴 pendiente |
| RF-E5 | Formalizar INV2-S en `FUNDAMENTOS_CONCEPTUALES.md` §III | mapa coherencia 3.3-3 | 🔴 pendiente |

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
| RF-G4 | CRUD admin completo en UI (interchange, followup, vhvproduct) o decisión de migrar | mapa_frontend M4 | 🔴 |
| RF-G5 | Superficies sin UI: maxo (saldo), protection, reputation, resources, interchanges | mapa_frontend M4 | 🔴 |

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
| RF-I8 | Votación ponderada (por TVI/coherencia) y delegación — fase futura | Cap 14 | 🔴 pendiente (extensión) |

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
4. **RF-G5** — maxo (saldo) en detalle de contrato o perfil; luego protection/reputation/resources
5. **RF-G4** — decisión CRUD admin: generar páginas o migrar `/admin/participants`
6. **RF-B4** — confirmar/conectar `/contracts/from-need` desde `/matching`
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
**Última actualización**: 11-08-2026 · **Método**: Patrón Puente (RLM + verificación)
