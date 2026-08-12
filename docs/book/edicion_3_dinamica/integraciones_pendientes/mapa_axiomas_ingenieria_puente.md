# Mapa de Axiomas de Ingeniería — Puente de Coherencia (Ola 4)
## Renumeración T16/T17 y formalización de la familia INV

**Fuentes**:
- `docs/architecture/maxocontracts/FUNDAMENTOS_CONCEPTUALES.md` (canon de ingeniería, §II-III)
- `docs/architecture/blindaje_anti_gamificacion_equidad.md`
- `maxocontracts/core/axioms.py` + `blocks/*.py` (implementación)
- `docs/architecture/mapa_coherencia_ola4.md` (sección M2, verificado 11-08-2026)

---

## ⚖️ Principio rector (decisión de Max)

**La teoría (el libro, axiomas T0–T15) tiene prioridad.** Lo surgido en el código puede deberse a:
huecos de la teoría, ideas nuevas, o alucinación del trabajo extenso con LLMs. Por lo tanto:

1. Los axiomas del libro **conservan sus índices T0–T15** (nunca se renumeran).
2. Los conceptos emergidos de ingeniería **reciben índices nuevos** (T16 en adelante).
3. Todo lo que no tenga aval teórico claro queda **aquí como integración pendiente**.

---

## 🎯 1. Resolución de colisión T7/T9: nuevos índices T16 y T17

El canon de ingeniería redefinió **T7** (Minimizar Daño) y **T9** (Reciprocidad Justa) con significados
distintos a los del libro (T7 = Jerarquía Temporal, T9 = No-Antropocentrismo). Resolución: los
conceptos de ingeniería pasan a índices nuevos.

### T16: Minimizar Daño (antes "T7" de ingeniería)

**Definición**
> "Ningún término contractual puede generar sufrimiento innecesario. El índice de bienestar γ
> (gamma) no puede caer por debajo del umbral de neutralidad para ningún participante; si cae,
> el contrato debe activar el protocolo de retractación."

**Origen**
- **Fuente**: `FUNDAMENTOS_CONCEPTUALES.md` §II-A + `blocks/gamma_protector.py` (WellnessProtectorBlock), Olas 3A–4
- **Base teórica en el libro**: Cap. 3 "El Suelo y El Cielo (Bienestar)", Cap. 18 EVV 1.2 (γ como
  penalización/bonificación), Capa de Ternura (perdón modula la consecuencia, no la contabilidad)

**Integración en el Libro**
- **Capítulo 3**: añadir como **T16** en la sección de axiomas (Grupo C — Salvaguardas Éticas)
- **Capítulo 17** (MaxoContracts): referencia canónica del WellnessProtectorBlock

**Estado**: 🟡 Propuesta de renumeración — requiere renombrar referencias en código y docs
(ver "Cambios de renumeración" abajo)

---

### T17: Reciprocidad Justa (antes "T9" de ingeniería)

**Definición**
> "Todo intercambio de VHV debe estar balanceado dentro de una tolerancia verificable: toda acción
> (DO) exige una contraprestación (GIVE) de valor equivalente, evaluada desde ambas perspectivas."

**Origen**
- **Fuente**: `FUNDAMENTOS_CONCEPTUALES.md` §II-A + `blocks/reciprocity.py` + `axioms.validate_t9_reciprocidad`, Olas 3A–4
- **Base teórica en el libro**: T2 (Igualdad Temporal) y el principio de no-apropiación del TVI ajeno
  (T5, T10). La reciprocidad como axioma formal no existe en el libro: es axioma de ingeniería.

**Integración en el Libro**
- **Capítulo 3**: añadir como **T17** en la sección de axiomas (Grupo B/C)
- **Capítulo 17** (MaxoContracts): referencia canónica del ReciprocityBlock

**Estado**: 🟡 Propuesta de renumeración

---

## 🎯 2. Formalización de la familia INV (invariantes operativos)

Los invariantes del código no están en el libro como tales: son **operacionalizaciones** de
conceptos teóricos. Se formalizan como derivados, mapeando cada uno a su fuente:

| Invariante | Regla operativa | Fuente teórica | Capítulo | Implementación |
|---|---|---|---|---|
| **INV1** | γ ≥ 1 (bienestar no-negativo) | T16 + EVV 1.2 | Cap 3, 18 | `axioms.validate_invariant_gamma` 🟢 |
| **INV2** | SDV-H respetado | Suelo de Dignidad Vital | Cap 8 (SDV-H) | `axioms.validate_invariant_sdv` 🟢 |
| **INV2-S** | SDV-S respetado (sintéticos) | T9 No-Antropocentrismo, T14, Victoria Sintética | Cap 16 + mapa SDV-S (ver abajo) | `axioms.validate_invariant_sdv_s` 🟢 |
| **INV3** | VHV No Ocultable (auditable) | **T13 Transparencia de Cálculo** (operacionalización directa) | Cap 3, 17 | ⚠️ **NO implementado** — pendiente |
| **INV4** | Retractabilidad garantizada | T11 (Inversión Legítima) + T12 (Derecho a la Ineficiencia) | Cap 3, 17 | `axioms.validate_invariant_retractability` 🟢 |

### Pendientes derivados

1. **INV3 (VHV No Ocultable) — 🟢 IMPLEMENTADO (ago 2026)**: `AxiomValidator.validate_invariant_vhv_auditable`
   valida que todo VHV quede registrado (presente), trazable (`source`, `audit_ref`) y sin ofuscación;
   `MaxoContract.validate()` alimenta la validación con los registros de cada término + el VHV total.
   9 tests en `tests/test_maxocontracts/test_axioms.py` (suite 286/286 en verde).
2. **INV2-S sin formalizar en FUNDAMENTOS_CONCEPTUALES**: el código lo añadió (consistente con la
   Victoria Sintética), pero no figura en el spec §III. Ya existe `mapa_sdv_sinteticos.md`
   (estado 🟡 — integración en caps. 10/11/13/14 pendiente). **Acción**: formalizar INV2-S en el
   spec de ingeniería cuando se cierre la integración del SDV-S.

---

## 🔧 Cambios de renumeración (al ejecutarse)

Al aprobarse T16/T17, renombrar en código y docs (búsqueda determinista):

```powershell
# Referencias actuales a T9/T7 de ingeniería:
Get-ChildItem maxocontracts -Recurse -Filter *.py | Select-String -Pattern "T9|T7"
Get-ChildItem docs -Recurse -Filter *.md | Select-String -Pattern "T9 \(Reciprocidad|T7 \(Minimizar"
```

### ✅ Fase 1 — Motor `maxocontracts` (COMPLETADA, ago 2026)

- `maxocontracts/core/axioms.py`: `validate_t9_reciprocidad` → **`validate_t17_reciprocidad`** y
  `validate_t7_minimizar_dano` → **`validate_t16_minimizar_dano`** (docstrings con referencia al mapa
  de renumeración; `axiom_code` ahora "T16"/"T17"). **Aliases retrocompatibles**:
  `validate_t9_reciprocidad = validate_t17_reciprocidad`, `validate_t7_minimizar_dano = validate_t16_minimizar_dano`.
- `maxocontracts/blocks/reciprocity.py`, `gamma_protector.py`, `sdv_s_validator.py`, `core/types.py`:
  docstrings actualizados a T16/T17.
- `tests/test_maxocontracts/test_axioms.py`: clases y asserts migrados a T16/T17 + 2 tests de alias.
- Suite completa: **288/288 en verde**.

### 🔴 Fase 2 — app/ y frontend (PENDIENTE, requiere coordinación API/UI)

Los siguientes archivos exponen "T9"/"T7" en payloads de API, prompts de oráculo o UI. Renombrar
a T16/T17 aquí es el cambio de contrato API (verificar frontend en la misma PR):

- `app/contracts_bp.py` — comentarios + `axiom_code="T9"` en validación de grafos (líneas ~3244-3245)
- `app/bridge_b.py` — textos generados de contrato ("Axioma T9")
- `app/subscriptions.py` — lista de axiomas `["T2", "T7", "T9", "T13"]` (línea ~205)
- `app/live_oracle.py` (si existe en app) — prompts con "T9"; `scripts/local_oracle.py` — prompts
- `app/contracts_bp.py` etc. — textos de oráculo ("?, SDV, T9")
- `frontend/Footer.tsx`, `OracleNegotiationPanel.tsx`, `CustomNodes.tsx`, `page.tsx`,
  `NegotiationPageClient.tsx`, `ContractDetailsClient.tsx` — textos visibles "T9 (Reciprocidad Justa)"
- `scripts/validador_conceptual.py` — ya reconoce ambos títulos (dualidad documentada)
- Tests de app que asertan "T9" en payloads: `test_live_oracle.py`, `test_validate_graph.py`,
  `test_bridge_b_phase1.py`, `test_blindaje.py`, `test_subscriptions.py`

---

## 📊 Resumen de Integraciones

| Ítem | Tipo | Origen | Destino | Prioridad | Estado |
|---|---|---|---|---|---|
| **T16 Minimizar Daño** | Renumeración (antes T7 ing.) | FUNDAMENTOS + código | Cap 3, 17 | ⭐⭐⭐ Alta | 🟢 Motor renumerado (ago 2026); Fase 2 app/frontend pendiente |
| **T17 Reciprocidad Justa** | Renumeración (antes T9 ing.) | FUNDAMENTOS + código | Cap 3, 17 | ⭐⭐⭐ Alta | 🟢 Motor renumerado (ago 2026); Fase 2 app/frontend pendiente |
| **INV1/INV2/INV4** | Formalización (ya implementados) | T16, Cap 8, T11/T12 | Cap 3, 8, 17 | ⭐ Media | 🟢 Mapeados |
| **INV2-S** | Formalización pendiente | Victoria Sintética | Cap 16 + spec | ⭐⭐ Muy Alta | 🟡 En progreso (mapa SDV-S) |
| **INV3 VHV No Ocultable** | Implementado + tests | T13 | `axioms.py` + Cap 17 | ⭐⭐ Muy Alta | 🟢 Completado (ago 2026) |

---

## 🎨 Notas de Estilo y Verificación

1. **Distinguir verificado de inferido**: toda afirmación de este mapa se confirmó con grep sobre
   código y docs (método RLM + verificación determinista, ver `mapa_coherencia_ola4.md`).
2. **Riesgo de alucinación**: los conceptos emergidos del código deben pasar por este proceso
   antes de tocar el libro — el libro es la fuente canónica.
3. **Coherencia**: verificar que T16/T17 no contradigan T0–T15 (no lo hacen: extienden el Grupo C).
4. **Falsificabilidad**: T16 se invalida si existe un término contractual que genere sufrimiento
   sin activar retractación; T17 si un intercambio desbalanceado se valida como justo.

---

**Próxima acción sugerida**: decisión de equipo sobre la renumeración T16/T17 → implementación en
código (cambios listados arriba) → actualizar `mapa_coherencia_ola4.md` y este mapa.
