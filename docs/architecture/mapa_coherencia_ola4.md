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

## 3. Notas de verificación (lecciones del flujo RLM)

El análisis RLM del motor acertó en clases, oráculos y composición, pero produjo **3 errores que la
verificación determinista corrigió**:

1. Afirmó que los invariantes viven en `blocks/gamma_protector.py` → **falso**: se definen en
   `core/axioms.py` (`AxiomValidator`) y `gamma_protector` solo los usa.
2. Mencionó un "`core/validator.py` (implícito)" → **no existe**; el archivo real es `core/axioms.py`.
3. Omitió `blocks/sdv_validator.py` y `blocks/sdv_s_validator.py` del mapa de bloques → añadidos arriba.

**Conclusión operativa**: el RLM es excelente para *resumir y navegar* contextos gigantes, pero toda
afirmación sobre ubicaciones/nombres debe confirmarse con grep antes de documentarse.

## 4. Cómo regenerar / actualizar este mapa

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

## 5. Próximos hitos del Puente de Coherencia

- [ ] **M2 — Teoría ↔ código**: extraer del libro (`docs/book/libro_completo_310126.md`, 300 KB) los
      axiomas/reglas y contrastarlos con este mapa (RLM sobre el libro + verificación).
- [ ] **M3 — Tests**: inventario de qué invariante cubre cada test (`tests/`, ~40 archivos).
- [ ] **M4 — Frontend**: mapear páginas Next.js → blueprints consumidos.
- [ ] Mantener este documento actualizado en cada Ola.
