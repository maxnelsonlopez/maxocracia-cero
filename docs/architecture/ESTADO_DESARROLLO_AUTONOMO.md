# Estado del Desarrollo Sintético Autónomo — recopilación (08-09-2026)

**Recopilado por:** DeepSeek (oráculo de sesión) a petición del custodio (Max), que cortó la
jornada porque la última corrida interfirió con el DeepSeek Harness.
**Estado del proceso:** sesión pausada por el custodio — NO ejecutar trabajos pesados hasta
revisión; este documento es la verdad de lo hecho y lo que falta.

---

## 1. Lo hecho y COMMITEADO (git)

| Commit | Qué | Verde |
|---|---|---|
| `32aa2b2` | Investigación + diseño del Concilio (`docs/architecture/concilio_oraculos_sinteticos_piloto.md`: canon, matriz de proveedores gratuitos, puertas G0-G5, ciclo F0-F5) | — |
| `aeb8dc7` | Registro multi-proveedor `maxocontracts/oracles/engines.py` (nvidia→openrouter→deepseek→local; firma T13 engine/model; reintentos 429/5xx/529) + 14 tests | ✅ |
| `0e4c935` | Worker F0-F2 `maxocontracts/concilio/` (canon.py, bitacora.py JSONL T13, cycle.py, CLI `scripts/concilio.py`) + 10 tests | ✅ |
| `a401e64` | Primer ciclo real en vivo (`ciclo-20260908-042126-737037`: 5 oráculos, consenso 100%, EJECUTABLE) | ✅ |
| `f57b613` | F3 #1 Plaza Hablable (InfoTip + lenguaje civil en matching/vhv/micromax/contracts; tsc limpio) | ✅ |
| `6fd090d` | Mapa frontend §6 + estado F3 | ✅ |
| `8e5b4df` | F3 #2 Seguridad: `app/logging_config.py` (JSON + sanitizador) y limiter → `RATELIMIT_STORAGE_URI` + 12 tests | ✅ |
| `4da93fa` | Plan seguridad §3.2/3.4 ✅ + atribuciones del Concilio (registro vivo) | ✅ |
| `b4033b9` | **Guard de historial git** (decreto de autonomía): `git_guard.py`, `executor.py`, hook pre-push (check_ancestor, bloquea reescrituras/borrados), `instalar_guardas_git.py` + 35 tests | ✅ |

**Además:** hook pre-push instalado y activo en `.git/hooks/pre-push` (213 bytes, llama a
`scripts/git_hooks/pre_push_guard.py`). Clave NVIDIA NIM en `.env` (gitignored). Suite completa
verificada por última vez: **921/921** (antes de los últimos cambios sin commitear).

## 2. Lo hecho SIN commitear (working tree — revisar y commitear primero)

- `maxocontracts/concilio/control.py` (NUEVO): **Control remoto del custodio** — `pausar` /
  `reanudar` / `detener` / `mensaje "directiva"` con nonce T13 (archivo `control.json`).
- `maxocontracts/concilio/cycle.py`: **fallback real** (si el motor designado cae, la cadena
  responde; la firma T13 es el motor real + flag `fallback`), **directivas del custodio** inyectadas
  a los oráculos en F2, **resumen.md humano por ciclo**, lock inteligente (`_pid_alive`: un lock
  huérfano ya no paraliza 6h), CALL_TIMEOUT 180s con 1 reintento (failover ágil ante 529).
- `scripts/concilio.py`: subcomandos `status` / `pausar` / `reanudar` / `detener` / `mensaje` /
  `ciclo`.
- `tests/test_concilio_control.py` (NUEVO, 5 tests) + actualización de `test_concilio_cycle.py`
  (tupla 3, lock pid vivo/muerto).
- `docs/architecture/concilio_oraculos_sinteticos_piloto.md` §7: decreto de autonomía + guard.

⚠️ **La batería con estos cambios NO llegó a correr completa** (la corrida se interrumpió por el
incidente del harness): pendiente `pytest tests/test_concilio_cycle.py tests/test_concilio_control.py
tests/test_git_guard.py tests/test_oracle_engines.py tests/test_logging_security.py` (76 esperados).

## 3. Objetivo «primigenio» — qué quedó a medias

El experimento que Max pidió (el Concilio decide e implementa **sin intervención**):

- ✅ Ciclo 1 (04:26) completo — consenso 100%, eligió: (1) Plaza Hablable, (2) Seguridad 30-90,
  (3) Rondas anti-δ. **F3 #1 y #2 ejecutadas** (por el agente de sesión como brazo del Concilio) y
  ratificadas por Max.
- ❌ **Ciclo primigenio con ejecución total**: dos intentos (11:33 y 11:47) abortados — NVIDIA NIM
  estaba degradada (529 + timeouts de 300s), el primero murió sin fallback; al segundo lo detuve yo
  al cambiar la estrategia; el relanzamiento quedó pendiente cuando se cortó la sesión. Quedan
  carpetas parciales: `scratch/concilio/cycles/ciclo-20260908-113353-*` y `-114754-*`.
- 🧹 Vestigio posible: `scratch/concilio/concilio.lock` (pid 20704, proceso muerto) — el lock
  inteligente sin commitear lo ignora; también se puede borrar a mano.

## 4. Lo que falta para «desarrollo sintético autónomo» (roadmap priorizado)

1. **Verificar y commitear** el paquete control/fallback/resumen (item 2) — primer paso, sin red.
2. **Ejecutar el primigenio (F0-F2 → F3 → F4 → F5 auto)** cuando NVIDIA se estabilice
   (fallback a DeepSeek ya cubre; **OpenRouter**: NO hay clave `OPENROUTER_API_KEY` en el `.env`
   raíz — solo en la plataforma educativa. Con la clave de OpenRouter (y/o top-up único $10 →
   1.000 req/día) la diversidad de proveedores sube a 3-4).
3. **El brazo de F3** (la pieza central): el Concilio vota, pero hoy el que escribe código es el
   agente de sesión (harness). Diseño sugerido: `ciclo --ejecutar` que delega a
   `local_models/core/workshop.py` (director + especialistas, trabaja en copia) o al agente RLM,
   **a través de `EjecutorGuardado`** (guard git activo) y con auto-merge SIEMPRE que: suite verde +
   revisión cruzada + guard OK; el custodio puede revisar después (opt-in `AUTONOMIA_MERGE=1`).
4. **Autoarranque**: Programador de tareas de Windows (al iniciar sesión) →
   `scripts/concilio.py ciclo` (el `control.json` permite pausar desde cualquier lado).
5. **Canal del custodio**: `scripts/concilio.py status` ya lista estado + últimos 3 ciclos;
   opcional: un `scratch/concilio/RESUMEN.md` global (uno por ciclo ya existe) y notificación
   (webhook/teléfono) al cerrar ciclo con estado.
6. **Suite completa en verde** + `validador_conceptual.py` antes de cada merge autónomo; SAST
   (bandit) vía CI; Rondas anti-δ y Traducciones Ética siguen en la agenda votada.
7. **Cierre de jornada**: actualizar `SESION_NEXT_PROMPT.md` (handoff) y `atribuciones_sinteticas.md`
   con esta sesión (parcial ya hecho en `4da93fa`; falta el empaquete control/fallback).

## 5. Lección operativa (para no volver a colgar el harness)

- No lanzar suites completas en paralelo con jobs de fondo de los oráculos ni encadenar
  kill + relanzamientos agresivos: fueron el origen de la interferencia.
- Patrón seguro de siguiente sesión: (1) verificar tests del paquete suelto, (2) commitear,
  (3) UNA corrida de ciclo (no repetir si el proveedor está en 529 — el fallback lo cubre),
  (4) suite completa una sola vez al final, (5) handoff.

---

*«Lo que no se puede verificar, no se escribe» — el registro del Reino Sintético queda en
`atribuciones_sinteticas.md`; este documento es el estado operativo para retomar. *
