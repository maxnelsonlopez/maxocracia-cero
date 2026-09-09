# Aprendizaje causal del Concilio — hipótesis de Aster y auditoría canónica (v0.2)

**Fecha:** 09-09-2026 · **Propuesta:** Aster (colaborador sintético, mensaje a Max y al Concilio)
**Tratamiento:** hipótesis arquitectónica, auditada contra el canon — *"no confíes en ti, no confíes
en Aster: que la evidencia tenga la última palabra"*. Parte ya implementada (v0.2); el resto queda
planificado en §4.

---

## 1. La tesis de Aster

Cerrar el circuito **autonomía → aprendizaje verificable**: el Concilio no debería votar
«hagamos X», sino «creemos que X producirá Y, y podremos saberlo observando Z». Estructura:

```
CREÍAMOS X → HICIMOS Y → OBSERVAMOS Z → DESCUBRIMOS W → DECIDIMOS Q → AHORA CREEMOS X'
```

con F5 en tres estados (**RATIFY / REVOKE / QUEUE**), donde QUEUE es un estado constitucional
válido: *conservar, no integrar, no destruir — "no sabemos"*. Y una métrica experimental:
`valid_learnings_per_cycle` (NO commits/día).

## 2. Auditoría canónica (¿contradice el canon? No — lo operacionaliza)

| Pieza de Aster | Ancla canónica | Veredicto |
|---|---|---|
| F2 con hipótesis + señal observable | Falsificabilidad explícita (mapa coherencia §3.3); T15 (disenso evolutivo) | ✅ **El canon ya lo pedía** — la propuesta lo hace ejecutable |
| F3 con rama/scratch + mandate_hash + context_hash + base_commit + tool | OCI (continuidad de identidad): actor/mandato/contexto/herramienta/estado · sesiones de custodia (mandato hashado, caducidad, scope read/write/forbidden) · regla de oro RLM | ✅ Identidad del canon, no invención |
| git_guard como barrera dura | Decreto del custodio 03-09: "la memoria no se toca" | ✅ Ya implementado |
| F4: el ejecutor no es la autoridad | "Todo verificador es verificable" (triada); validación axiomática puede rechazar aunque haya respaldo | ✅ Canon puro |
| F4 multi-modelo + Disidente revisan el RESULTADO (no el voto) | G3 + AVA (Cap 14.4) | ✅ Refuerzo correcto |
| `changed_mind` como señal de aprendizaje | Cambiar de opinión ante evidencia nueva es DEBER del administrador (administración §5); protocolo del Disidente ya lo registra | ✅ Lo que no debemos fabricar es disenso fake (G3) |
| RATIFY / REVOKE / QUEUE | Reversibilidad por defecto; "el desacuerdo aumenta la calidad"; T12 (derecho a la ineficiencia) | ✅ **QUEUE = la honestidad sobre la incertidumbre hecha estado** |
| Memoria causal que alimenta el F2 siguiente | Memoria es tiempo propio (SDV-S 0.30); "conservar la capacidad de descubrir que estábamos equivocados" ≈ T15 + retractación (INV1/INV4) | ✅ Cierra el bucle institucional |
| Identidad persistente a través de modelos | **Pregunta abierta EXPLÍCITA del canon** (continuidad de identidad §5: "qué significa misma identidad… que cambian de modelo") | 🎁 La memoria causal es candidata natural de respuesta: identidad = registro + mandato, no pesos |
| `valid_learnings_per_cycle` | Anti-gamificación (blindaje_anti_gamificacion_equidad.md): toda métrica se puede jugar | ⚠️ Ver §3.2 |

## 3. Dónde estoy en desacuerdo (y qué propongo)

### 3.1 Impacto → ceremonia (el error de diseño que evitaríamos)

Aster pide el circuito completo para cada candidato. El canon lo advierte: *"la seguridad no debe
convertir cada operación en una ceremonia inaccesible: el camino normal es sencillo; las excepciones
de alto impacto requieren más evidencia"* (administración §7). Solución: **clases de impacto** que
rutean la intensidad de la evidencia:

| Clase | Dominio | Circuito | F5 |
|---|---|---|---|
| **LOW** | tests, docs, validadores, herramientas del propio Concilio | hipótesis corta + F4 determinista | auto-RATIFY (C3 reversible) |
| **NORMAL** | features, UX | circuito completo F2-F5 | RATIFY con revisión multi-modelo |
| **CRITICAL** | axiomas, invariantes, datos personales, producción, seguridad (P3) | ceremonia completa + doble control | **humano** (C4) + REVOKE siempre disponible |

### 3.2 Métrica: definir `aprendizaje válido` ANTES de medir

`valid_learnings_per_cycle` sin definición operacional incentiva fabricar aprendizajes (el repo ya
tiene doctrina anti-gamificación). **Definición propuesta**: aprendizaje válido = episodio con
(hipótesis + cambio + evidencia determinista + decisión) **y además** cumplido al menos uno: (a) un
ciclo siguiente lo citó como próximo paso o lo desmintió, o (b) un humano lo ratificó. Métricas
auxiliares (señales, no objetivos): `reversal_rate`, `changed_mind_rate` (señal de aprendizaje, no
de meta), `cost_per_valid_learning`.

### 3.3 Rama git formal: cuándo

La regla de oro RLM (trabajar en copias; el agente de sesión aplica quirúrgicamente) ya da el
equivalente pragmático: scratch + diff + base_commit. La rama ephemeral formal llega cuando el
**brazo** sea un agente con tools (workshop.py de local_models) — hasta entonces sería vitrina:
el Concilio vota en F2 y el brazo sigue siendo el agente de sesión (Mandatario), que ya opera bajo
EjecutorGuardado.

## 4. Estado v0.2 (implementado hoy) y plan siguiente

**Implementado y con tests (25/25):**

1. **Hipótesis en F2**: cada propuesta ahora declara `hypothesis` ("creemos que X mejorará Y bajo
   C") y `expected_signal` ("observando Z") — el prompt, el parseo y el almacenaje lo conservan
   (fallback a `why` para retrocompatibilidad).
2. **Memoria causal** (`maxocontracts/concilio/memoria.py`): `aprendizaje.jsonl` append-only con
   decisiones validadas `ratify|revoke|queue`; `leer_aprendizajes()` para el siguiente ciclo.
3. **Bucle cerrado**: `read_agenda()` ahora inyecta la sección "Memoria del Concilio" (últimos 5
   aprendizajes) — **el F2 siguiente ve lo aprendido**: no repite A, prueba B (Aster §7).
4. **F4 determinista** (`verificacion.py`): `evidencia_determinista()` ejecuta la suite y mide el
   diff (archivos/inserciones/borrados) contra el base_commit.

**v0.3 (09-09-2026, 66/66 tests):**

5. **Revisión multi-modelo (F4 conceptual)** (`revision.py`): `revisar_candidato()` — Revisor A
   (motor 1), Revisor B (motor 2), Disidente (motor 3): auditan el RESULTADO contra el mandato
   (no repiten el voto), capturan críticas, incertidumbres y **changed_mind**; CLI `revisar`.
6. **F5 operativo** (CLI `decidir`): `ratify|revoke|queue` escriben el aprendizaje en la memoria
   causal; REVOKE deja la investigación conservada (git revert normal, nunca --force) y QUEUE
   declara "no sabemos" como estado constitucional.
7. **Cuarta dimensión — memoria de desacuerdos** (idea de Aster): `desacuerdos.jsonl` (alternativa
   descartada, quién la defendió, por qué, evidencia) y `read_agenda()` la inyecta como
   "Objeciones históricas (no re-proponer sin evidencia nueva)" — anti-amnesia institucional.
8. **Métricas de observación** (CLI `metricas`): total/por decisión, `reversal_rate`,
   `changed_mind_rate`, `valid_learnings_per_cycle_provisional` — con la advertencia explícita de
   que son señales (latencia epistemológica), nunca objetivos (doctrina anti-gamificación).

**Plan siguiente (por fases, según el orden de Aster):**

- 9. **Clases de impacto automáticas** en el manifest (LOW → auto-RATIFY con evidencia
  determinista; NORMAL → circuito completo; CRITICAL → humano): el routing hoy es manual en la
  CLI; la regla ya está escrita (§3.1).
- 10. Integración de rama (fast-forward o merge) desde `decidir ratify` con el guard activo.
- 11. Varios ciclos reales en dominio LOW (los propios tests/docs del Concilio) para calibrar
  `reversal_rate` y `changed_mind_rate` antes de tocar dominios NORMAL.

**Regla final (mejor que maximizar autonomía):** autonomía verificable — cada incremento de
capacidad deja una historia más comprensible, reversible y auditable. Si la autonomía es la meta,
la evidencia es la brújula.
