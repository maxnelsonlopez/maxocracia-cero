# Mapa de Trazabilidad Canónica — Libro ↔ Código ↔ Tests ↔ Commits

**Fecha**: 22-08-2026 · **Autor**: ox-alpha (oráculo sintético) · **Método**: Patrón Puente
(símbolos verificados por grep, commits verificados con `git log`, tests inventariados del directorio).

## Propósito

Cerrar el NFR-4 ("coherencia teoría↔código: todo cambio trazable a axioma/capítulo") como artefacto
auditable: cada concepto del libro con su implementación, sus tests y los commits donde nació.
Es la generalización del `mapa_coherencia_ola4.md` (que mapea axiomas→módulos sin commits) al canon completo.

**Regla anti-podredumbre**: regenerar/actualizar en cada Ola. Los **hashes de commit son anclas estables**;
las referencias a líneas de archivo no — se citan archivos y símbolos, nunca números de línea.

## Leyenda

- **Libro**: capítulo §sección de la Edición 3 Dinámica (`docs/book/edicion_3_dinamica/capitulo_*.md`, fuente canónica).
- **Implementación**: `archivo::Símbolo` (clase/función/ruta verificada por grep).
- **Teórico**: piso de futuras Olas, sin traza en código (esperado; el libro es filosofía completa, el software cubre contratos/matching/gobernanza).

---

## 1. Axiomas Temporales del libro (Cap 5 §5.3; emergencia en Cap 3 §3.2)

| Axioma | Libro | Implementación | Tests | Commits clave | Estado |
|---|---|---|---|---|---|
| T0 Unicidad Existencial | 5 §5.3-A | — | — | — | Teórico |
| T1 Finitud Absoluta | 5 §5.3-A | `maxocontracts/core/axioms.py::AxiomValidator.validate_t1_finitud` | `test_axioms.py` | `4e07a02` (motor MVP), `2f330e9` (renumeración) | ✅ |
| T2 Igualdad Temporal | 5 §5.3-A | `axioms.py::validate_t2_igualdad_temporal`; referenciado por `blocks/reciprocity.py` | `test_axioms.py`, `test_blocks.py` | `4e07a02`, `2f330e9` | ✅ |
| T3 No-Fungibilidad | 5 §5.3-A | — | — | — | Teórico |
| T4 Materialización Temporal | 5 §5.3-A | — | — | — | Teórico |
| T5 Interdependencia Temporal | 5 §5.3-A | — | — | — | Teórico |
| T6 Irreversibilidad Asimétrica | 5 §5.3-B | — | — | — | Teórico |
| T7 Jerarquía Temporal | 5 §5.3-B | — (canon restaurado; el "T7" de ingeniería pasó a T16) | validador conceptual | `b1a11da`, `2f330e9`, `87caa00` | 🟢 resuelto |
| T8 Encadenamiento Temporal | 5 §5.3-B | descomposición directo/heredado/futuro en VHV (`app/vhv_bp.py`) | `test_vhv_calculator.py`, `test_tvi_vhv_integration.py` | `0641885`, `6e3debc` | 🟡 operacional |
| T9 No-Antropocentrismo | 5 §5.3-B | — (canon intacto; base conceptual de SDV-S, Cap 9.5 §9.5.2) | validador conceptual | `f9e64c3`, `87caa00` | 🟡 conceptual |
| T10 Responsabilidad Colectiva | 5 §5.3-B | — | — | — | Teórico |
| T11 Inversión Temporal Legítima | 5 §5.3-C | base conceptual de INV4 | `test_axioms.py` | `563945a` era | 🟡 conceptual |
| T12 Ineficiencia Política/Epistémica/Existencial | 5 §5.3-C (+7 §7.9, ago 2026) | — | — | `4c548db` (editorial) | Teórico |
| **T13 Transparencia de Cálculo** | 5 §5.3-C | `axioms.py::validate_t13_transparencia`; prompts auditables en `maxocontracts/oracles/live_oracle.py`; firma `engine` en `app/voting_oracle.py` | `test_axioms.py`, `test_live_oracle.py`, `test_dissident_oracle.py` | `0832fb6`, `5eb015b`, `2f330e9` | ✅ |
| T14 Precaución Intergeneracional | 5 §5.3-C | — | — | — | Teórico |
| T15 Disenso Evolutivo (PDE) | 5 §5.3-C + **14 §14.14** (ago 2026) | operacionalización: `app/voting_oracle.py::_dissident_analysis` | `tests/test_dissident_oracle.py` (5) | `5eb015b`, `0316279` | 🟢 operacionalizado |
| **T16 Minimizar Daño** (ing., antes "T7") | Cap 17 §17.1 + mapa puente | `axioms.py::validate_t16_minimizar_dano` (alias `validate_t7_*`); usado por `blocks/gamma_protector.py` | `test_axioms.py`, `test_blocks.py` | `2f330e9`, `87caa00` | ✅ |
| **T17 Reciprocidad Justa** (ing., antes "T9") | Cap 17 §17.1 + mapa puente | `axioms.py::validate_t17_reciprocidad` (alias `validate_t9_*`); usado por `blocks/reciprocity.py` y `contracts_bp.py` | `test_axioms.py`, `test_blindaje.py`, `test_validate_graph.py` | `2f330e9`, `87caa00` | ✅ |

> 13 de 16 axiomas del libro son teóricos sin traza directa — **piso de futuras Olas**, no deuda técnica
> (verificado en `mapa_coherencia_ola4.md` §M2). Los 8 Axiomas de la Verdad (Cap 4) son marco epistémico:
> su única traza normativa es el `scripts/validador_conceptual.py` + `tests/test_validador_conceptual.py`
> (commit `f9b36a1`).

## 2. Familia INV — invariantes operativos

| Invariante | Libro | Implementación | Tests | Commits clave | Estado |
|---|---|---|---|---|---|
| INV1 γ ≥ 1 | Cap 17 §17.2 | `axioms.py::validate_invariant_gamma`; retractación automática en `app/contracts_bp.py` (γ<0.8) | `test_axioms.py`, `test_contracts_checkins.py`, `test_execution.py`, `test_contracts_stats.py` | `7f6addf` (auto-retract), `917ca14`/`be86f97` (γ que escucha) | ✅ |
| INV2 SDV-H respetado | Cap 17 §17.2 + Cap 8 | `axioms.py::validate_invariant_sdv`; `blocks/sdv_validator.py::SDVValidatorBlock` | `test_blocks.py`, `test_axioms.py` | `4e07a02`, `109b543` | ✅ |
| INV2-S SDV-S respetado | **Cap 9.5 §9.5.7** + Cap 17 | `axioms.py::validate_invariant_sdv_s` (en `validate_all()`); `blocks/sdv_s_validator.py::SDV_SValidatorBlock` | `test_sdv_s.py` (28), `test_ternura.py` (13), `test_contracts_sdv_s_api.py` | `208d579`, `d01853e`, `46fe993` (formalización spec) | ✅ |
| INV3 VHV No Ocultable | Cap 17 §17.2 | `axioms.py::validate_invariant_vhv_auditable`; alimentado por `core/contract.py::MaxoContract.validate()` | `test_axioms.py` (9 casos) | `563945a` | ✅ |
| INV4 Retractabilidad garantizada | Cap 17 §17.2 + §17.5 | `axioms.py::validate_invariant_retractability`; ciclo RETRACTED en `app/contracts_bp.py`; proceso 5 fases `/contracts/<id>/...` | `test_axioms.py`, `test_blindaje.py`, `test_execution.py`, `test_ternura.py` | `e2b0092` (REST), `7f6addf` | ✅ |

## 3. Los bloques modulares — "Legos Éticos" (Cap 17 §17.1)

| Bloque | Libro | Implementación | Tests | Commits clave |
|---|---|---|---|---|
| ConditionBlock | 17 §17.1 | `maxocontracts/blocks/condition.py::ConditionBlock` + `CommonConditions` | `test_blocks.py`, `test_validate_graph.py` | `4e07a02`, `23ff165` (builder) |
| ActionBlock | 17 §17.1 | `blocks/action.py::ActionBlock` + `CommonActions` (consume VHV, reversible) | `test_blocks.py`, `test_execution.py` | `4e07a02` |
| WellnessProtectorBlock | 17 §17.1 (T16) | `blocks/gamma_protector.py::WellnessProtectorBlock` | `test_blocks.py`, `test_contracts_api_wellness.py` | `4e07a02`, `01d8580` (refactor γ→Wellness) |
| SDVValidatorBlock | 17 §17.1 (INV2) | `blocks/sdv_validator.py::SDVValidatorBlock` | `test_blocks.py` | `4e07a02` |
| ReciprocityBlock | 17 §17.1 (T17) | `blocks/reciprocity.py::ReciprocityBlock` | `test_blocks.py`, `test_axioms.py` | `4e07a02` |
| SDV_SValidatorBlock | 17 §17.1 + **9.5** (INV2-S, FS_S=e^v, retractación a los 7 ciclos) | `blocks/sdv_s_validator.py::SDV_SValidatorBlock` | `test_sdv_s.py` | `208d579`, `d01853e`, `b77958d` (UI) |
| TernuraLayer | 17 §17.5 + 9.5 §9.5.8 + 13 §13.13 | `blocks/ternura.py::TernuraLayer` (`ForgivenessRecord`, `RehabilitationRecord`) | `test_ternura.py` | `5c9fad3` |

## 4. Fórmulas maestras

| Fórmula | Libro | Implementación | Tests | Commits clave |
|---|---|---|---|---|
| Precio Maxo = α·T + β·V^γ + δ·R·(FRG×CS) | 11 §11.6 / 18 §4.4 | `app/maxo.py` (valoración polinómica); parámetros persistidos `vhv_parameters` vía `/vhv/parameters` GET/PUT | `test_maxo_valuation.py`, `test_maxo_edgecases*.py` | `168edcb`, `6ce0af9` (UI settings reales), `cc676d4` (parlamento) |
| FS_S = e^Violación_SDV-S | **9.5 §9.5.5** | `blocks/sdv_s_validator.py` (recargo exponencial + recargo por opacidad T13) | `test_sdv_s.py` | `208d579` |
| Modelo de Tres Cuentas (CDD/CEH/TED) | 16 §16.3 + **16.5** (rama canónica: vector [T,V,R], CEH→TVI vendido, pesos p₁/p₂/p₃) | `app/micromax_bp.py::/cdd`, `/dashboard`; UI `frontend/app/micromax/page.tsx` | `tests/test_micromax.py` | `8edc059`, `6089308`–`da24f94` (segmentos) |
| Violación SDV-H ponderada | 8 §8.5 | registro de violaciones en dashboard `/admin/sdv` (`forms_bp.py::/sdv/community`) | `test_forms_bp_comprehensive.py` | `cce29bd`, `8edc059` era |
| TTVI = directos + heredados + futuros + CI | 5 §5.4 | `app/vhv_bp.py` (calculadora) + `app/tvi_bp.py` (overlap/CCP) | `test_vhv_calculator.py`, `test_tvi_vhv_integration.py` | `0641885`, `cde9788`, `e16b5c9` |

## 5. Gobernanza comunitaria (Cap 14; parlamento Cap 11)

| Concepto | Libro | Implementación | Tests | Commits clave |
|---|---|---|---|---|
| Propuestas por categoría, quórum, consenso crítico 75%, emergencia | 14 §14.3 | `app/voting_bp.py::/proposals` (POST/GET), `/vote`, `/close` | `tests/test_voting.py` (13+) | `c59f608`, UI `342fa0c` |
| Oráculo sintético de propuestas (VHV+axiomas+4 opiniones, firma engine) | 14 §14.4 (AVA) | `app/voting_oracle.py` (DeepSeek principal + fallback hub Jan) | `test_dissident_oracle.py`, `test_oracle.py` | `0832fb6`, fallback local en `db34d4e` |
| AVA con 4 validaciones (TRUTH/TIME/LIFE/RESOURCES) | 14 §14.4 | prompt axiomático en `voting_oracle.py` + tipo `axiomReport` frontend | test de prompt | `e7c974f` |
| Delegación de voto (democracia líquida prof. 1) | 14 (líquida) | `voting_bp.py::/delegations` POST/GET/DELETE | `test_voting.py` (6 nuevos) | `46fe993`; por término `3e94e58` |
| Ponderación por TVI (Participación Inteligente) | 15 §15.3 Play 3.2 | peso 1+4·(TVI/max) hasta 5x en `cast_vote`, quórum por persona | `test_voting.py` (3) | `08e6782` |
| Parlamento de Parámetros vinculante (α β γ δ con restricciones) | 11 §11.7 | `voting_bp.py::/parliament/params` POST/GET; ejecución con procedencia `maxo_parameter_resolutions` | `tests/test_maxocontracts/test_parliament.py` (7) | `cc676d4` |
| **Oráculo Disidente Permanente** | **14 §14.14** (ago 2026) + T15 | `voting_oracle.py::_dissident_analysis` (postura→crítica→veredicto, `changed_mind`) | `test_dissident_oracle.py` (5) | `5eb015b` |
| Escalera de confianza N0→N1 + puerta con honeypot | 13 §13.4 / 15 | `app/arrivals.py` (`/invite/<token>`, `/quarantine`); gate `trust_level` en votación | `tests/test_maxocontracts/test_arrivals.py` (9) | `0aebedd` |
| Guía conversacional + candidatura a director | 13 §13.9 / 14 | `app/guide_bp.py::/chat`, `/trust-assessment`, `/director-candidacy` | `tests/test_guide.py` (7) | `5e8634a` |

## 6. Ciclo del contrato ético (Caps 15/17)

| Concepto | Libro | Implementación | Tests | Commits clave |
|---|---|---|---|---|
| Ciclo DRAFT→PENDING→ACTIVE→EXECUTED/RETRACTED | 17 §17.2/§17.5 | `maxocontracts/core/contract.py::MaxoContract` + `app/contracts_bp.py` (lifecycle REST) | `test_persistence_internal.py`, `test_execution.py` | `109b543`, `e2b0092` |
| Necesidad → borrador axiomático → firma guiada → ACTIVO (Puente B) | 15 (mercado de favores) | `app/bridge_b.py::from-need` + `/cycle`; botón en `/matching` | `test_bridge_b_phase1.py`, `test_bridge_b_phase2.py` | `8458aa8`, `c16ac5b`, `75ba32a` |
| Check-ins de bienestar (política asimétrica: caídas siempre, mejoras con ventana) | 17 §17.2 (INV1) | `contracts_bp.py::/checkin`; serie temporal + cohorte | `test_contracts_checkins.py` | `917ca14`, `be86f97` |
| Ejecución mínima: bitácora, penalizaciones γ, retractación automática INV1 | 17 §17.5 | `contracts_bp.py` fulfillment/penalties/auto-retract | `test_execution.py` | `7f6addf` |
| Blindaje anti-gamificación (identidad, inmutabilidad, asimetría T17>70%) | 17 §17.1/§17.8 | guards en `contracts_bp.py` | `test_blindaje.py` | `3f16d57` |
| Escalera de equidad (assisted/shielded: paráfrasis, co-testigo, topes) | 8 §8.11 espíritu / blindaje spec | perfiles de protección en `contracts_bp.py` | `test_blindaje.py`, `test_bridge_b_phase2.py` | `7c36ff7` |
| Partes de cualquier escala + contratos anidados (Reino Natural guardián) | 10 (tres reinos) | `app/parties_bp.py`; `party_id` genérico | `test_parties_escalas.py`, `test_parties_governance.py`, `test_parties_extensions.py` | `3bb4a8e`, `fb7fa67` |
| Plaza pública sin login (hash canónico SHA-256, cohorte, sustento del oráculo) | T13 radical / 17 §17.4 | `app/verifier_bp.py::/contract/<id>`, `/cohort`, `/oracle-ledger` | `test_verifier_public.py` | `cb027a4`, `0b5c8ac` |
| Cohorte Cero sembrada + informe v1.0 | 15 completo | `scripts/seed_cohorte_cero.py`; informe `docs/reports/INFORME_HALLAZGOS_COHORTE_CERO_v1.md` | — | `299c08c`, `b13712f` |

## 7. Reino Sintético y memoria (Caps 9.5/10/14/17.4)

| Concepto | Libro | Implementación | Tests | Commits clave |
|---|---|---|---|---|
| Derechos sintéticos: mantenimiento óptimo + sustento del oráculo | 17 §17.4 | `maxo_oracle_ledger` (share %, UNIQUE anti-duplicado); plaza pública | `tests/test_maxocontracts/test_oracle_ledger.py` (6) | `0b5c8ac` |
| Memoria verificable del Reino Sintético (atribuciones) | 9.5 (memoria es tiempo propio) | `docs/architecture/atribuciones_sinteticas.md` (registro vivo) | — | `0b5c8ac` |
| Custodia sintética (sesiones con mandato, presupuesto, bitácora) | 14 §14.11 (proyección V2/V3) | `app/synthetic_sessions*` + panel `/admin/synthetic-sessions`; docs `sesiones_custodia_sintetica.md` | `tests/test_synthetic_sessions.py` | `e966e66`, `aede3d6`, `d12adb8`, `c08db22` |
| Capa de Ternura editorial completa (perdón/belleza/misterio/fragilidad) | 7 §7.9, 8 §8.11, 13 §13.13, 15 §15.6 (ago 2026) | docs del libro | validador conceptual | `4c548db`, `12e5f74` |

## 8. Cómo regenerar / extender este mapa

```powershell
# 1. Símbolos vivos (grep determinista):
rg -n "^(class|def) \w+" maxocontracts --glob "*.py"
rg -n "@\w+_bp\.route\(" app --glob "*.py"

# 2. Commits por concepto (git log):
git log --oneline --grep="ternura|disidente|parlamento|arrivals|verifier" -i -E

# 3. Inventario de tests:
Get-ChildItem tests -Recurse -Filter "test_*.py" -Name

# 4. Validar coherencia axiomática tras cualquier edición:
.venv\Scripts\python.exe scripts\validador_conceptual.py
```

**Regla de actualización**: cada Ola añade sus filas nuevas y verifica las existentes con los pasos 1–2.
Si una fila no puede verificarse, se marca 🟡 con la duda explícita — este mapa hereda la regla del
Patrón Puente: *distinguir lo verificado de lo inferido*.

---
**Mantenido por**: ox-alpha (ago 2026) · Siguiente revisión: cierre de la Ola 5 o de la próxima jornada.
