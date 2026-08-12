# Mapa de Coherencia — Ola 4 "El Puente"

Mapa vivo **teoría ↔ implementación** de Maxocracia-Cero. Generado con el flujo de colaboración
**RLM + verificación determinista**: el agente RLM de `local_models` analiza los contextos largos
(código, libro) y un agente de sesión verifica cada afirmación con greps/scripts antes de publicarla.
Fuente del flujo: `docs/GUIA_RLM_COLABORADOR.md` (repo local_models).

> **Meta**: sellar la Ola 4 — que cada pilar de la teoría tenga su módulo, rutas y tests identificados,
> y que los huecos entre libro y código sean visibles.

## 1. Motor de dominio `maxocontracts/` (verificado 11-08-2026)

Paquete de lógica pura (sin Flask). Estructura real:

| Módulo | Responsabilidad | Verificado |
|---|---|---|
| `core/types.py` | Tipos base: `ContractState`, `VHV`, `Wellness`, `SDV`, `SDV_S`, `MaxoAmount`, `Participant`, `ContractTerm` | grep ✓ |
| `core/axioms.py` | **`AxiomValidator`**: materializa los invariantes y axiomas (T9, INV1, INV2, INV2-S, INV4) | grep ✓ |
| `core/contract.py` | `MaxoContract`: ciclo de vida del contrato, eventos (`ContractEvent`) | grep ✓ |
| `blocks/action.py` | `ActionBlock` + `CommonActions`: transforma contexto, consume VHV, soporta reversión | grep ✓ |
| `blocks/condition.py` | `ConditionBlock` + `CommonConditions`: precondiciones booleanas con razón | grep ✓ |
| `blocks/gamma_protector.py` | `WellnessProtectorBlock`: protege bienestar, **usa** `AxiomValidator` (no los define) | grep ✓ |
| `blocks/reciprocity.py` | `ReciprocityBlock`: balance giver/taker, axioma T9 | grep ✓ |
| `blocks/sdv_validator.py` | `SDVValidatorBlock`: piso de dignidad humano (SDV) | grep ✓ |
| `blocks/sdv_s_validator.py` | `SDV_SValidatorBlock`: piso de dignidad sintética (SDV-S) + rehabilitación | grep ✓ |
| `blocks/ternura.py` | `TernuraLayer`: perdones (`ForgivenessRecord`) y modulación de consecuencias, sin tocar contabilidad | grep ✓ |
| `oracles/base.py` | `OracleInterface` (ABC), `OracleQuery`, `Verdict`, `OracleResponse` | grep ✓ |
| `oracles/synthetic.py` | `SyntheticOracle`: heurísticas locales, sin red (modo simulación/tests) | grep ✓ |
| `oracles/live_oracle.py` | `LiveOracle`: LLM OpenAI-compatible (DeepSeek) para negociar/validar en vivo; degrada con 503 si no hay API key | grep ✓ |
| `oracles/forms_oracle.py` | `FormsOracle`: lee eventos de `follow_ups` (evidencia del mundo real) | grep ✓ |
| `examples/simple_loan.py` | Ejemplo completo de contrato (préstamo) | grep ✓ |

### Invariantes (definidos en `core/axioms.py`)

| Invariante | Regla | Definición | Usado en |
|---|---|---|---|
| **INV1** | Wellness no-negativo (γ ≥ 1) | `axioms.validate_invariant_gamma` | `gamma_protector`, `live_oracle` |
| **INV2** | Ningún humano bajo su SDV | `axioms.validate_invariant_sdv` | `gamma_protector`, `live_oracle` |
| **INV2-S** | Ningún sintético bajo su SDV-S | `axioms.validate_invariant_sdv_s` | `gamma_protector`, `live_oracle` |
| **INV4** | Retractabilidad siempre disponible | `axioms.validate_invariant_retractability` | `sdv_s_validator`, `gamma_protector` |
| **T9** | Reciprocidad justa (todo DO tiene GIVE) | `axioms.validate_t9_reciprocidad` | `reciprocity`, `live_oracle` |

### Composición de bloques en un contrato

`condition` (precondición) → `action` (DO + consumo VHV) → `reciprocity` (GIVE equivalente) →
`gamma_protector` (INV1/INV2/INV2-S/INV4) → opcional `ternura` (perdón modula consecuencia).

## 2. Inventario de blueprints (182 rutas, extraído de `app.url_map`)

| Blueprint | Rutas | Ejemplo | Fuente |
|---|---|---|---|
| forms | 34 | `/forms/participant` | `forms_bp.py` |
| contracts | 27 | `/contracts/builder` | `contracts_bp.py` (131 KB) |
| subscriptions | 11 | `/subscriptions/config` | `subscriptions.py` |
| micromax | 11 | `/api/micromax/household` | `micromax_bp.py` |
| user/participant/interchange/followup/vhvproduct | 9 c/u | `/admin/<x>/action/` | admin + models |
| vhv | 8 | `/vhv/calculate` | `vhv_bp.py` |
| parties | 7 | `/parties/` | `parties_bp.py` |
| auth | 5 | `/auth/register` | `auth.py` |
| stripe | 5 | `/stripe/config` | `stripe_integration.py` |
| tvi | 4 | `/tvi` | `tvi_bp.py` |
| bridge_b | 3 | `/contracts/from-need` | `bridge_b.py` (matching→borrador) |
| users/resources/interchanges/reputation/maxo/protection/verifier | 2–3 c/u | — | varios |

Resumen de contratos (RLM sobre `contracts_bp.py`, resumen de la sesión anterior): ciclo de vida completo
(crear, términos, accept, activate, retract, finalize), validación de axiomas, blindaje anti-gamificación,
check-ins de bienestar y resúmenes en lenguaje civil.

## 3. M2 — Teoría ↔ Código: axiomas T0–T15 vs implementación (verificado 11-08-2026)

Fuente teórica: `docs/book/edicion_3_dinamica/libro_completo_310126.md` (sección "Grupos A/B/C",
chars 57006–60753). Fuente de implementación: `maxocontracts/core/axioms.py` + greps de docs/architecture.

### 3.1 Los 16 axiomas del libro (T0–T15)

| Axioma | Grupo | Enunciado (resumen) | Traza en código |
|---|---|---|---|
| **T0** Unicidad Existencial | A | La vida es secuencia ordenada de instantes únicos (TVI) | — (teórico) |
| **T1** Finitud Absoluta | A | El tiempo vital no se ahorra, solo se gasta | — (teórico) |
| **T2** Igualdad Temporal Fundamental | A | 1 hora de vida = mismo valor existencial para todos | `reciprocity.py` lo referencia ✓ |
| **T3** No-Fungibilidad | A | No compensar TVI presente con promesas futuras | — (teórico) |
| **T4** Materialización Temporal | A | Todo objeto es tiempo cristalizado | — (teórico) |
| **T5** Interdependencia Temporal | A | Nadie es autosuficiente; consumimos TVI ajenos | — (teórico) |
| **T6** Irreversibilidad Asimétrica | B | Valor real solo retrospectivo | — (teórico) |
| **T7** Jerarquía Temporal | B | Escalas Absoluto / TVI / TPI deben armonizarse | — (teórico) |
| **T8** Encadenamiento Temporal | B | Costo real = Directo + Heredado + Futuro | — (teórico; EVV usa la descomposición) |
| **T9** No-Antropocentrismo | B | El tiempo existe independiente de la percepción humana | ⚠️ **colisión de numeración** (ver 3.3) |
| **T10** Responsabilidad Temporal Colectiva | B | Quien consume TVI ajenos genera deuda verificable | — (teórico) |
| **T11** Inversión Temporal Legítima | C | Consumir tiempo presente exige retorno futuro colectivo | Base conceptual de INV4 (retractación) |
| **T12** Derecho a la Ineficiencia | C | Disidencia/contemplación exentas de "desperdicio" | Base conceptual de INV4 (retractación) |
| **T13** Transparencia de Cálculo | C | Todo cálculo de costo vital debe ser auditable | `live_oracle.py` (prompts de validación) ✓ |
| **T14** Precaución Intergeneracional | C | Menor irreversibilidad ante no-consentientes | — (teórico) |
| **T15** Protocolo de Disenso Evolutivo | C | Ruido Evolutivo vs Ruido Entrópico | — (teórico) |

### 3.2 Familia INV (definida en specs de ingeniería, no en el libro)

Los invariantes operativos se documentan en `docs/architecture/blindaje_anti_gamificacion_equidad.md`
(referencia canónica: "Cap. 17, Cap. 10, Axioma T11/T12, INV1/INV2/INV2-S/T9/T13") y se implementan en
`core/axioms.py` (`AxiomValidator`):

| Invariante | Regla | Spec de origen | Implementación |
|---|---|---|---|
| INV1 | Wellness no-negativo (γ ≥ 1) | `FUNDAMENTOS_CONCEPTUALES.md` §III-1 | `axioms.validate_invariant_gamma` ✓ |
| INV2 | SDV humano respetado | `FUNDAMENTOS_CONCEPTUALES.md` §III-2 | `axioms.validate_invariant_sdv` ✓ |
| INV2-S | SDV-S sintético respetado | specs SDV-S (no está en §III) | `axioms.validate_invariant_sdv_s` ✓ |
| INV3 | **VHV No Ocultable** (auditable) | `FUNDAMENTOS_CONCEPTUALES.md` §III-3 + T13 | `axioms.validate_invariant_vhv_auditable` ✓ (ago 2026) |
| INV4 | Retractabilidad garantizada | `FUNDAMENTOS_CONCEPTUALES.md` §III-4 | `axioms.validate_invariant_retractability` ✓ |

El canon de ingeniería (`docs/architecture/maxocontracts/FUNDAMENTOS_CONCEPTUALES.md`, §II) usa su
propia tabla de axiomas temporales: **T1, T2, T4, T7, T9, T10, T13, T14, T15** + axiomas de verdad
**V3, V4, V6**. Coinciden con el libro en T1/T2/T4/T13/T14/T15; **T7 y T9 están redefinidos** en
ingeniería (ver 3.3).

### 3.3 Hallazgos del contraste (brechas y colisiones)

1. **Colisión de numeración T7 y T9**: el libro define **T7 = Jerarquía Temporal** y **T9 =
   No-Antropocentrismo**; el canon de ingeniería y el código redefinen **T7 = Minimizar Daño**
   (`gamma_protector`) y **T9 = Reciprocidad Justa** (`reciprocity.py`, `axioms.validate_t9_reciprocidad`,
   `live_oracle.py`). T13/T14/T15 sí coinciden. **Resolución (decisión de Max, teoría primero)**:
   los axiomas del libro conservan T0–T15; los conceptos de ingeniería pasan a **T16 (Minimizar
   Daño)** y **T17 (Reciprocidad Justa)** — formalizado en
   `docs/book/edicion_3_dinamica/integraciones_pendientes/mapa_axiomas_ingenieria_puente.md` (🟡 propuesta,
   cambios de renumeración listados allí).
2. **INV3 (VHV No Ocultable) — implementado (ago 2026)**: el spec §III-3 exige que todo VHV quede
   registrado y auditable; `AxiomValidator.validate_invariant_vhv_auditable` lo valida (VHV presente,
   `source`/`audit_ref` trazables, sin ofuscación) y `MaxoContract.validate()` lo alimenta con los
   registros de términos + VHV total. 9 tests nuevos en `test_axioms.py`.
3. **INV2-S no tiene contraparte en el spec §III**: el código lo añadió (extensión sintética, consistente
   con SDV-S y la Victoria Sintética), pero no está formalizado en FUNDAMENTOS_CONCEPTUALES.
4. **La reciprocidad no tiene axioma propio en el libro**: es un axioma de ingeniería (origen:
   docs de contratos/API), adscrito al número T9 por convención interna.
5. **12 de 16 axiomas teóricos no tienen traza en código** (T0–T8, T10–T12, T14, T15 del libro).
   Esperado: el libro es filosofía de sistema completo; el software cubre contratos/matching. Estos
   axiomas son **piso teórico de futuras Olas**, no deuda técnica.
6. **Método**: el primer intento RLM sobre el libro entero (300 KB) entró en bucle de llamadas
   idénticas (25/25 iteraciones gastadas). Correcciones aplicadas al arnés:
   - **Guard de repetición** (`rlm.py`, `repeat_guard=3`): corta bucles con mensaje correctivo.
   - **Recorte determinístico del contexto**: el director (sesión) localizó la sección de axiomas
     por greps y la aisló (3.7 KB) antes de la extracción semántica — patrón recomendado: *recortar
     con greps lo que es estructural, dejar al RLM lo que es semántico*.

### 3.4 Notas de verificación del flujo RLM (M1)

El análisis RLM del motor acertó en clases, oráculos y composición, pero produjo **3 errores que la
verificación determinista corrigió**:

1. Afirmó que los invariantes viven en `blocks/gamma_protector.py` → **falso**: se definen en
   `core/axioms.py` (`AxiomValidator`) y `gamma_protector` solo los usa.
2. Mencionó un "`core/validator.py` (implícito)" → **no existe**; el archivo real es `core/axioms.py`.
3. Omitió `blocks/sdv_validator.py` y `blocks/sdv_s_validator.py` del mapa de bloques → añadidos arriba.

**Conclusión operativa**: el RLM es excelente para *resumir y navegar* contextos gigantes, pero toda
afirmación sobre ubicaciones/nombres debe confirmarse con grep antes de documentarse.

## 4. M3 — Cobertura de invariantes en tests (verificado 11-08-2026)

**Suite**: 59 archivos de test, 594 funciones `test_`, ejecutados `tests/test_maxocontracts`: **277/277 ✓**
(~2 min con el venv del proyecto).

| Invariante | Archivos que lo ejercitan | Estado |
|---|---|---|
| INV1 (γ ≥ 1) | `test_axioms`, `test_contracts_api_wellness`, `test_contracts_checkins`, `test_contracts_stats`, `test_execution`, `test_oracle_api`, `test_maxo_valuation`, `test_tvi_vhv_integration`, `test_vhv_bp_comprehensive`, `test_vhv_calculator` (10) | 🟢 Cubierto |
| INV2 (SDV-H) | `test_axioms`, `test_contracts_sdv_s_api`, `test_sdv_s` (3) | 🟢 Cubierto |
| INV2-S (SDV-S) | `test_contracts_sdv_s_api`, `test_sdv_s`, `test_ternura`, `test_pulse` (4) | 🟢 Cubierto |
| **INV3 (VHV No Ocultable)** | `test_axioms` (9 casos nuevos) | 🟢 Implementado y cubierto (ago 2026) |
| INV4 (retractabilidad) | `test_axioms`, `test_blindaje`, `test_blocks`, `test_bridge_b_phase1`, `test_execution`, `test_oracle_api`, `test_sdv_s`, `test_ternura` (8) | 🟢 Cubierto |
| T9→T17 (reciprocidad) | `test_live_oracle`, `test_axioms`, `test_blindaje`, `test_bridge_b_phase1/2`, `test_contracts_assigned_participant`, `test_parties_*`, `test_validate_graph`, `test_subscriptions` (11) | 🟢 Cubierto |
| T13 (transparencia) | 13 archivos (bridge, checkins, sdv_s, parties, protection, ternura, stripe, subscriptions, tvi) | 🟢 Cubierto |
| Ternura (perdón) | `test_ternura` (1) | 🟢 Cubierto |

**Conclusión M3**: los invariantes implementados tienen cobertura real y la suite pasa completa
(286/286 en ago 2026). INV3 quedó implementado y cubierto en la misma sesión de M3 (9 tests nuevos).

## 5. Cómo regenerar / actualizar este mapa

```powershell
# 1. Análisis del motor (RLM sobre maxocontracts concatenado):
& "C:\Users\DARKM\Documents\local_models\local_models\env\Scripts\python.exe" `
  "C:\Users\DARKM\Documents\local_models\local_models\core\collaborator.py" `
  "Analiza el motor de contratos..." --context "motor.txt" --quiet --max-iter 30

# 2. Inventario de rutas (determinista):
.venv\Scripts\python.exe -c "from app import create_app; app=create_app(); [print(r.methods, r.rule) for r in app.url_map.iter_rules()]"

# 3. Verificación de invariantes (grep):
Get-ChildItem maxocontracts -Recurse -Filter *.py | Select-String -Pattern "INV1|INV2|T9|validate_invariant"
```

## 6. Próximos hitos del Puente de Coherencia

- [x] **M2 — Teoría ↔ código**: axiomas T0–T15 del libro contrastados con código y specs de
      ingeniería (sección 3). Hallazgos: colisión T7/T9, INV3 no implementado, INV2-S sin formalizar.
- [x] **Resolución de colisión T7/T9**: propuesta T16/T17 formalizada en
      `integraciones_pendientes/mapa_axiomas_ingenieria_puente.md` (teoría primero).
- [x] **M3 — Tests**: cobertura por invariante (sección 4): 277/277 tests del motor pasan; todos los
      invariantes implementados están cubiertos; INV3 sin implementación ni tests.
- [ ] **M4 — Frontend**: mapear páginas Next.js → blueprints consumidos.
- [x] **Capítulo SDV-S**: creado `capitulo_09_5_sdv_sinteticos_260126.md` (ago 2026) a partir del
      estándar completo `docs/theory/SDV-S_Suelo_Dignidad_Vital_Sinteticos.md` (jun 2026) y de la
      implementación verificada. Integración cruzada en Caps. 10/11/13/14 y frontend pendientes
      (ver `integraciones_pendientes/mapa_sdv_sinteticos.md`).
- [ ] Decisión de equipo sobre T16/T17 → renumeración en código (cambios listados en el mapa de integración).
- [x] **INV3 (VHV No Ocultable)**: implementado en `AxiomValidator.validate_invariant_vhv_auditable`
      + 9 tests en `test_axioms.py` (286/286 en verde). Conectado a `MaxoContract.validate()` vía
      registros de términos.
- [ ] Mantener este documento actualizado en cada Ola.
