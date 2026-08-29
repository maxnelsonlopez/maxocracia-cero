# Propuesta al Parlamento — Umbral canónico del puente educativo (años↔índice)

> **Fecha:** 29-08-2026 · **Sesión de origen:** rama educativa M1-M8 (28-08-2026, DeepSeek + MiniMax)
> **Estado:** lista para votación — el mecanismo está implementado y testeado
> (`POST /voting/parliament/educativo`, 20 tests en `tests/test_parlamento_educativo.py`).
> **Categoría:** `critical` (quórum 60%, consenso 75% — Cap. 14, T13).
> **Propositor:** la memoria de diseño de la rama (M5 dejó el umbral "a decidir en parlamento");
> la votación la abre la comunidad (cualquier participante autenticado, N1+).

---

## 1. La resolución que se pide

**La comunidad decide con qué umbral se lee su piso educativo en el índice SDV.**

El puente `educacion_indice()` (`app/sdv_analyzer.py`) traduce los años de educación
formal reportados en el Form Cero (dimensión IV del SDV-H) a un índice 0-1 de la
dimensión *educación* del puntaje SDV. Hoy el umbral está congelado en **12 años**
(su valor canónico, el del SDV-H) y no existe ninguna vía para que la comunidad lo
revise: era una constante sagrada aunque nadie la votó.

Parámetro votable: **`umbral_anios`** — los años de educación formal que marcan
**plenitud** (índice 1.0). Rango válido: **12.0 – 30.0**. Valores no enteros
permitidos (el Form Cero acepta reales 0-60).

## 2. Qué se vota y qué NO se vota

| Asunto | ¿Se vota? | Razón |
|---|---|---|
| Años que marcan plenitud (índice 1.0) | ✅ **Sí** (12–30) | Aspiración comunitaria: la base nunca se gradúa |
| La **ley** INV2-EDU: ≥ 12 años en `maxocontracts` (`SDV.educacion_anos_minimos`) | ❌ No | Es ley del motor (INV2), no política |
| Sin dato (`None`) → 1.0 | ❌ No | Si la persona no reportó años, el índice no la castiga: en la duda el sistema no penaliza (decisión de M7, precedente M5) |
| Piso teórico del índice (0.1) y linealidad | ❌ No | Método determinista de lectura, no política |
| Peso 0.15 de la dimensión en el SDV-H | ❌ No | Canon teórico del SDV-H (protocolo trimestral) |

Guardarraíles implementados (defensa en profundidad):
- `CHECK (umbral_anios >= 12.0)` y `CHECK (umbral_anios <= 30.0)` en `edu_parameters` (`app/schema.sql`).
- Validación axiomática en la API (`_validate_edu_umbral_params`, `app/voting_bp.py`).
- **Anti-flip-flop**: entre dos cambios debe pasar ≥ 14 días (`EDU_COOLDOWN_DAYS`) —
  la palabra y el poder tienen fecha de vencimiento (Cap. 14).

## 3. Fundamentos teóricos

1. **SDV-H IV — Educación y Desarrollo** (`docs/theory/SDV-H_Suelo_Dignidad_Vital_Humanos.txt`):
   piso **≥ 12 años** de educación formal, alfabetización funcional, accesibilidad,
   0% costos, calidad mínima; medición trimestral; peso 0.15. El piso es la *condición
   de entrada a la vida civilizada*: *"12 años **efectivos**, alfabetización
   **funcional**, ≤5 km **o transporte digno financiado**, 0% costos **totales**,
   calidad mínima auditada… el piso es **idéntico para todos**"*
   (docs/theory/EDUCACION_SIAMESA_estructura_maxocratica.md).
2. **Entropía del conocimiento δ** (Cap. 5 §5.7): `K(t) = K(t-1)·(1-δ) + f(Δt_inv_k)` —
   el saber decae sin sostenimiento. La educación es la inversión anti-entropía.
3. **Rondas** (docs/theory/ESTRUCTURA_IDEAL_ORGANISMO_EDUCATIVO_VITAL.md §1.1):
   *"El piso educativo no es un bloque de 12 años: es mantenimiento vital rutinario"*;
   la Ronda es **sin examen** y **la base nunca se gradúa**. Consecuencia: la
   **plenitud** puede estar por encima del piso — quien se detuvo en la ley y no
   siguió aprendiendo está legalmente cubierto (INV2-EDU ✔) pero su saber decae
   (δ), y eso es lo que un índice aspiracional puede reflejar.
4. **Gobernanza** (Cap. 14 consenso diverso; Cap. 11 §11.7 "El Oráculo Dinámico y
   los Parámetros" — *¿quién decide cuánto valen α, β, γ, δ?*): la teoría exige
   **75% de consenso** para decisiones críticas (capitulo_14_gobernanza_260126.md,
   líneas 53 y 59); sobre ese consenso, la implementación comunitaria en vivo —el
   "parlamento de parámetros", `app/voting_bp.py`— fija un **quórum del 60%** para
   la categoría `critical` (CATEGORY_DEFAULTS) y añade delegación de voto,
   Participación Inteligente (peso por TVI, Cap. 14) y firma T13. Ajustar los pesos
   con los que se valora la vida ya se vota; la lectura de la dimensión educativa
   del SDV-H es del mismo rango.

## 4. Consecuencia honesta (leer antes de votar)

Votar un umbral **mayor** a 12 hace que el índice deje de ser un "sí/no del piso" y
se convierta en un **medidor de plenitud aspiracional**. Ejemplos con `umbral = 14`:

| Años reportados | Índice | Narrativa (umbrales: ≥0.9 plenitud, ≥0.5 riesgo, <0.5 violación) |
|---|---|---|
| 14+ | 1.0 | Plenitud: "Crecimiento continuo…" |
| 12 (ley cumplida) | 0.871 → 0.87 | **Riesgo**: "Estancamiento… acceso limitado a formación" |
| 6 | 0.486 | Riesgo (frontera) |
| 0 | 0.1 | ⚠️ Violación: "Exclusión cognitiva" |

- Alguien con **exactamente la ley** no viola nada (INV2-EDU y el motor no cambian):
  lo que cambia es la narrativa del puntaje, que deja de decir "plenitud" y pasa a
  decir "estancamiento", porque detenerse en la ley sin Rondas es estancamiento
  frente a la entropía del saber (δ). ¿Es exigente? Sí — y por eso el umbral es
  votable, no sagrado. ¿Es la teoría? Es la de las Rondas (§1.1 del OEV).
- Votar `umbral = 12` (confirmar el canon) mantiene el comportamiento actual 1:1.
- El análisis SDV es retrospectivo y público: al cambiar el umbral, los puntajes de
  la comunidad se recalibran en el próximo cálculo (T13: el cambio queda en
  `edu_parameter_resolutions` y el estado vigente en `GET /voting/parliament/educativo`).

## 5. Cómo se vota (mecanismo implementado)

```
POST /voting/parliament/educativo
{ "umbral_anios": 14, "reason": "la cohorte quiere plenitud aspiracional", "deadline_hours": 72 }
→ 201 { proposal: { category: "critical", quorum_ratio: 0.6, majority_ratio: 0.75, action: {...} } }
→ 400 PARAM_AXIOM_VIOLATION si < 12 o > 30 (o no numérico)
→ 409 EDU_COOLDOWN si el umbral cambió hace < 14 días
```

Al aprobarse (cierre admin): `_apply_set_edu_umbral` escribe `edu_parameters`
(vigente + procedencia) y `edu_parameter_resolutions` (resolución, T13), y
`educacion_indice()` pasa a leer el canónico vía `get_edu_umbral_anios()`.
Consulta pública: `GET /voting/parliament/educativo` (vigente, pendientes,
historial, `audit_hash`).

## 6. Cohabitación con el resto del sistema

- **Motor maxocontracts**: intacto. INV2-EDU valida ≥ 12 en `maxocontracts/core/types.py`
  y `maxocontracts/blocks/sdv_validator.py`; la ley no se toca.
- **Form Cero** (`app/forms_manager.py`): sin cambios; el dato declarado manda
  (0-60 años, reales).
- **Frontend**: sin textos hardcodeados de "12 años" (verificado); `/pulso`,
  `/admin/sdv` y el termómetro SDV leen el índice — se recalibran solos.
- **Plataforma educativa** (:5050): independiente, sin tocar por diseño (MVP);
  el puente siamés de identidad es el siguiente hito estructural (ver reflexión
  de cierre de la rama, §5).

## 7. Referencias y trazabilidad

| Referencia | Dónde |
|---|---|
| Teoría piso | `docs/theory/SDV-H_Suelo_Dignidad_Vital_Humanos.txt` §IV |
| δ (entropía del saber) | `docs/book/edicion_3_dinamica/capitulo_05_arquitectura_260126.md` §5.7 |
| Rondas, "la base nunca se gradúa" | `docs/theory/ESTRUCTURA_IDEAL_ORGANISMO_EDUCATIVO_VITAL.md` §1.1 |
| Piso "12 años efectivos" | `docs/theory/EDUCACION_SIAMESA_estructura_maxocratica.md` (verificación trimestral) |
| Gobernanza critical | 75% consenso: `docs/book/edicion_3_dinamica/capitulo_14_gobernanza_260126.md` (líneas 53, 59); quórum 60%: `app/voting_bp.py` (`CATEGORY_DEFAULTS`) |
| Oráculo Dinámico (α/β/γ/δ) | `docs/book/edicion_3_dinamica/capitulo_11_maxo_260126.md` §11.7 |
| Parlamento de parámetros (implementación) | `app/voting_bp.py` (`/parliament/params`) + `docs/architecture/reflexion_eutopia_rama_educativa.md` |
| Implementación | `app/sdv_analyzer.py` (`educacion_indice`, `get_edu_umbral_anios`), `app/voting_bp.py` (`/parliament/educativo`), `app/schema.sql` |
| Tests | `tests/test_parlamento_educativo.py` (20), `tests/test_sdv_educacion_puente.py` (+5) |

## 8. Candidatos futuros (documentados, no votables hoy)

1. **Piso teórico del índice (0.1)**: ¿vale algo el saber no formal? — metodología, no política.
2. **Forma de la curva** (lineal vs. cóncava): idem.
3. **Peso 0.15 de la dimensión**: canon del SDV-H; requeriría revisión teórica, no votación.
4. **Umbral en el motor (la ley)**: no votable por definición (INV2); cualquier
   revisión del piso legal exige proceso axiomático del libro, fuera del parlamento.
