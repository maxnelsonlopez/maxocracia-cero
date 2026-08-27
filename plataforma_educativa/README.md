# Plataforma Educativa (Maxocracia-compatible)

Plataforma educativa **independiente pero compatible** con la Maxocracia. Vive
por completo dentro de `plataforma_educativa/` y no toca el resto del repositorio
(`app/`, `frontend/`, etc.). Es un MVP funcional: backend Flask mínimo + SQLite +
frontend estático sin build + tests pytest en verde.

El propósito es hacer tangible, con código simple y testeable, la rama educativa:
un **Árbol de Habilidades** con prerrequisitos y pruebas por tema, y la planificación
de **reuniones semanales** que funcionan como **células de aprendizaje**, donde un
**monitor** que ya domina un tema lo enseña (la idea de la *vacuación*). Es una
implementación de demostración; no reemplaza la plataforma Maxocracia.

---

## Requisitos

- Python 3.13 (probado) — se usan `Flask` y el `sqlite3` de la librería estándar.
- No hace falta SQLAlchemy ni ORM: se usa `sqlite3`.

## Cómo correr (Windows)

Desde la carpeta `plataforma_educativa/`:

```powershell
# 1. Crear el entorno virtual (una sola vez)
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Arrancar la plataforma (puerto 5050, distinto del 5001 de Maxocracia)
python run.py
# → abre http://localhost:5050
```

Comando equivalente con el CLI de Flask (debe **ejecutarse dentro de
`plataforma_educativa/`**, porque el paquete `app` de esta plataforma convive
con el `app/` de Maxocracia a nivel de raíz del repo):

```powershell
$env:FLASK_APP = "app"
python -m flask --app app run --port 5050
```

El primer usuario registrado es **coordinador** (puede "Generar semana").
El email es **opcional** en el registro.

> La base de datos se crea como `plataforma_educativa.db` en esta carpeta y está
> en `.gitignore` (no se commitea). Para usar otra ruta, fija la variable de
> entorno `PLATAFORMA_EDUCATIVA_DB`.

## Cómo pasar los tests

Desde la raíz del repositorio (o desde `plataforma_educativa/`):

```powershell
python -m pytest plataforma_educativa/tests/ -q
# → 25 passed
```

Los tests usan `tmp_path`, así que **no dejan bases de datos ni artefactos**.

---

## API REST

Autenticación por token simple: al `login` se devuelve un token aleatorio (en
memoria) que se envía en la cabecera `X-Auth-Token`.

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/auth/register` | Crea usuario `{username, password, email?}` (email opcional) |
| POST | `/api/auth/login` | `{username, password}` → `{token, user}` |
| GET | `/api/me` | Perfil + progreso por rama |
| GET | `/api/tree` | Árbol completo con el estado del usuario |
| GET | `/api/topics/<id>` | Detalle del tema + preguntas (sin revelar la correcta) |
| POST | `/api/topics/<id>/start` | Marca `learning` (valida prerrequisitos, 403 si no aprobados) |
| POST | `/api/topics/<id>/test` | `{answers:[indices]}` → califica (≥70% → `test_passed`) |
| POST | `/api/topics/<id>/request-mentorship` | Marca `mentorship_approved` (pendiente; la valida la triada) |
| GET/POST | `/api/availability` | Disponibilidad semanal (`{week, slots}`) |
| POST | `/api/meetings/generate?week=` | Genera las reuniones de la semana (solo coordinador) |
| GET | `/api/meetings?week=` | Lista reuniones de la semana |
| POST | `/api/meetings/<id>/join` | Inscribe al usuario (409 si está llena) |
| POST | `/api/meetings/<id>/attend` | El monitor/coordinador marca asistencias |
| GET | `/api/meetings/monitor-queue` | Temas que necesitan monitor |
| GET | `/api/monitors?branch=` | Usuarios calificados para enseñar por rama |

## Modelo de datos (SQLite)

`users`, `branches` (8 ramas), `topics` (35 temas, con `prereq_ids` JSON y
`dificultad` 1-5), `questions` (≥3 por tema), `user_topics` (progreso con
`estado` y `mentor_rounds`), `meetings`, `meeting_participants`, `availability`.

Estados de progreso: `not_seen` → `learning` → `test_passed` → `mastered`.
`mastered` exige aprobar el test **y** haber participado como monitor de ≥1
reunión (`mentor_rounds >= 1`).

## Decisiones de implementación clave

- **`sqlite3` en vez de SQLAlchemy**: menos dependencias, todo con la librería
  estándar; `requirements.txt` solo pide `flask`.
- **Token en memoria** (`app.extensions["auth_tokens"]`): simple para el MVP; en
  producción se pasaría a un token persistente/JWT.
- **Algoritmo de agrupación** (el corazón, en `app/planner.py`, función pura
  `plan_meetings`): agrupa por el **tema más débil** de cada persona; cuando hay
  muchos usuarios con el mismo tema débil, **se reparte por similitud de
  perfiles** (se juntan los que comparten *el resto* de sus debilidades) mediante
  una expansión voraz determinista, y luego un **rebalanceo** garantiza que ninguna
  célula quede con menos de 3 sin superar los 8. `assign_monitors` asigna monitor
  **solo si** hay alguien calificado (tema `mastered` + `mentor_rounds >= 1` +
  disponibilidad).
- **`is_coordinator` = primer usuario registrado**: el que puede "Generar semana".
- **Detalle de tema expone las preguntas pero no la respuesta correcta**: el
  servidor califica; el cliente solo necesita las opciones.
- **Todos los archivos en UTF-8** (`# -*- coding: utf-8 -*-` y escritura UTF-8).

## Mapeo conceptual a la Maxocracia

Esta plataforma implementa, en miniatura y de forma independiente, conceptos de la
rama de educación definidos en
`docs/theory/ESTRUCTURA_IDEAL_ORGANISMO_EDUCATIVO_VITAL.md`:

| Concepto Maxocracia | Implementación en esta plataforma |
|---|---|
| **Árbol de Tecnologías y Habilidades** (§1.2) | Las 8 **ramas** (`branches`) y 35 **temas** (`topics`) con prerrequisitos (`prereq_ids`) y dificultad. |
| Células = grupos pequeños **coordinados** (§1.3) | Las **reuniones semanales** (`meetings`) de a lo sumo 8 participantes. La teoría habla de células de 5-12; el MVP acota a 8 (máx) y 3 (mín) para las pruebas. |
| **La vacuación**: *el skill se gana enseñándolo* (§1.4) | El estado **`mastered`** solo se alcanza aprobando el test **y** participando como **monitor** de ≥1 reunión (`mentor_rounds >= 1`). El "monitor calificado" es quien domina el tema. |
| Prerrequisitos del Árbol (nodos padres) | `prereq_ids`: no se puede *empezar* un tema sin aprobar los anteriores (403). |
| La triada de validación (mentor + par + oráculo) (§1.2) | `request-mentorship` deja la solicitud **pendiente**; en producción la valida la triada (aquí se documenta, no se ejecuta). |
| La EIR y el flujo de necesidades (complementario a `matching.py`) | La agrupación de reuniones aproxima la lógica de *necesidad × oferta*: empareja a quienes necesitan reforzar un tema con quien puede enseñarlo (monitor). |

La plataforma es **autónoma**: no importa el código de Maxocracia ni comparte su
base de datos. Correrá en el puerto **5050** junto al Flask de Maxocracia (5001).

## Límites y plan futuro

- **Email opcional**: no se exige ni se valida; queda soportado en el modelo para
  un futuro envío de recordatorios.
- **Triada de mentoría**: la `request-mentorship` solo marca "pendiente"; la
  validación real (mentor + par + oráculo con veto) queda como flujo futuro.
- **Bootstrapping del monitor**: para ser monitor hay que tener `mastered`, que
  exige `mentor_rounds >= 1`; en el MVP los primeros monitores se siembran/validan
  externamente (en pruebas se setea directo). Documentado como límite de arranque.
- **Integración con Maxocracia**: conectar el "matching" de necesidades
  (`app/matching.py`) para que las reuniones/necesidades educativas se capitalicen
  en intercambios reales, y la contabilidad vital (TVI/VHV) como métrica de la
  mentoría.
- **Estado real de las reuniones**: asistencia, ausencias y Tiempo Opaco (teoría,
  cap. 18) no se miden todavía.
- El mismo `app/` de esta plataforma puede chocar con el `app/` de Maxocracia si se
  importa desde la raíz del repo: por eso los tests insertan la raíz de la
  plataforma al inicio del `sys.path` y los comandos se ejecutan desde
  `plataforma_educativa/`.
