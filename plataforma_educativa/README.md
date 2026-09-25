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
- `pyjwt >= 2.8` (autenticación federada).

## Federación con Maxocracia (Una sola puerta)

La plataforma acepta dos credenciales: tokens locales (modo autónomo) y **JWTs
de Maxocracia** (modo federado, aprovisionamiento Just-In-Time). Para federar:

```powershell
# En el nodo OEV y en :5001, LA MISMA clave (la de la app principal):
$env:SECRET_KEY = "<la misma SECRET_KEY de Maxocracia>"

# Token de servicio con el que el nodo reporta maestrías al puente (:5001)
# (en :5001 y en el nodo OEV, el mismo valor):
$env:EDU_BRIDGE_SERVICE_TOKEN = "<secreto compartido del puente>"
```

Sin `SECRET_KEY` la federación queda **cerrada por diseño** (503 explícito; el modo
autónomo local sigue funcionando). Sin `EDU_BRIDGE_SERVICE_TOKEN` el puente
`/edu-bridge/sync-mastery` rechaza con 403 (fail-closed): la escalera de confianza
no se compra con una declaración.

**Sincronización automática de maestrías**: cuando el nodo verifica una maestría
(`mastered` = test aprobado + mentoría a otros), la reporta al puente de :5001 con
su token de servicio (la persona no necesita estar conectada ni tener su JWT). Es
best-effort: si el puente está caído, el nodo sigue vivo:

```powershell
$env:EDU_BRIDGE_URL = "http://127.0.0.1:5001"   # el :5001 de Maxocracia
```

## La Biblioteca de la Ciudad (M15): material educativo

Cada lote (tema) tiene material junto al test: **guías propias** en markdown
(carga instantánea, sin red) y **enlaces al mundo** (Wikipedia verificado +
búsquedas Kahn/YouTube). La inserción es por archivo — el tejido se fork, no se
rasca:

```powershell
# 1. Escribir el .md con mini front-matter:
#    titulo: Conteo, la llave
#    tema: conteo
#    orden: 1
#    <contenido markdown>
#    ...en plataforma_educativa/materials/conteo.md

# 2. Sincronizar (idempotente: repite sin duplicar; el tejido muta en git):
python sync_materials.py
```

Reglas de la biblioteca (ver
`docs/architecture/BIBLIOTECA_CIUDAD_MATERIAL_EDUCATIVO.md`): el material acompaña
pero **no sustituye la obra** (la validez sigue siendo el test + la vacuación);
cero rankings; los enlaces se verifican antes de sembrar; "compartir la luz" es
opt-in voluntario y retractable (nada se publica sin permiso).

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
| GET | `/api/topics/<id>/materials` | La biblioteca del lote (guías + enlaces; en la lengua de la persona, `?lang=` sobreescribe) |
| GET | `/api/materials/<id>` | Guía completa en markdown (para leerla) |
| GET | `/api/community/lights` | El muro de luces (opt-in, sin ranking) |
| POST | `/api/me/share-progress` | Interruptor de la luz (`{on: bool}`) |
| POST | `/api/me/idioma` | Preferencia de idioma para la biblioteca (`{idioma: "es"}`) |
| GET | `/api/buscador?q=` | **B1+B2+B3+B5**: búsqueda unificada (semillas + corpus + Zenodo + OpenAlex + Wikipedia + SearXNG opcional); `&format=searx` para federar desde una lente SearXNG |
| GET | `/api/buscador/score?url=` | Score de confiabilidad Nivel 1 (banda + razones + motor) |
| GET | `/api/buscador/archivo?url=` | Rescate Wayback Machine (snapshot más cercano) |
| GET | `/api/buscador/seeds` | Semillas del buscador (verificadas primero) |
| POST | `/api/buscador/seeds` | Siembra una semilla candidata (solo coordinador; regla M15) |
| POST | `/api/buscador/seeds/<id>/verificar` | Verificación humana de una semilla (solo coordinador) |
| GET | `/api/buscador/parametros` | Parámetros vigentes (gobernable; votación en B4) |
| GET | `/api/buscador/corpus?q=` | **B2**: solo el corpus propio (memoria local, sin red) |
| GET | `/api/buscador/feeds` | **B2**: feeds registrados (candidatos + verificados) |
| POST | `/api/buscador/feeds` | **B2**: registra un feed candidato (solo coordinador; M15) |
| POST | `/api/buscador/feeds/<id>/verificar` | **B2**: verificación HTTP+parse real (solo coordinador) |
| POST | `/api/buscador/feeds/<id>/ingerir` | **B2**: ingiere feed verificado al corpus (solo coordinador) |
| POST | `/api/buscador/seeds/<id>/materializar` | **B2**: materializa semilla verificada al corpus (solo coordinador) |
| GET | `/api/buscador/scoring/estado` | **B4**: foto pública de la cola nocturna y veredictos Nivel 2 |
| POST | `/api/buscador/scoring/encolar` | **B4**: encola el tejido sin Nivel 2 (solo coordinador) |
| POST | `/api/buscador/scoring/ejecutar` | **B4**: procesa un lote con el juez; 502 fail-open sin juez |
| GET | `/api/buscador/resoluciones` | **B4**: historial vinculante del parlamento |
| POST | `/api/buscador/parametros/<nombre>/resolver` | **B4**: registra lo resuelto (valor + procedencia, cooldown 14 días; 409 si hay prisa) |
| GET | `/api/buscador/lupa?titulo=` | **B6**: meta-panorama del artículo (reversiones, anonimato, guerra, top editores) |
| GET | `/api/buscador/lupa/diff?de=&a=` | **B6**: diff palabra por palabra entre revisiones (Verbo Justo) |

## El Buscador educativo (B1–B7)

Buscador independiente sin ads ni tracking: **semillas verificadas primero**
(bloque garantizado), capa académica abierta (Zenodo, API pública sin token)
y capa web opcional vía SearXNG auto-hospedado. Principios (diseño canónico en
`docs/architecture/DISENO_BUSCADOR_EDUCATIVO_GRATUITO.md`): $0 para el
proyecto y la persona, fail-open (un motor caído se reporta, no rompe),
**etiqueta-no-censura** (bandas con razones, nunca oculta resultados), y
regla M15 (las semillas nacen candidatas; solo la verificación humana las
siembra). Todo con la librería estándar — cero dependencias nuevas.

**B2 — Corpus verificado**: los feeds (blogs, YouTube, web) nacen candidatos
y solo la verificación HTTP + parse real los habilita para ingesta (regla
M15); los documentos viven en `buscador_docs` con índice FTS5 (degrada a LIKE
si el SQLite no lo trae compilado) y la búsqueda unificada los pone segundos,
tras las semillas y antes de Zenodo/SearXNG. Longevidad Wayback (CDX) como
señal guardada en `wayback_ts`; rescate de 404 en `/archivo`.

**B3 — Score con memoria + UI**: el score Nivel 1 vive en `buscador_scores`
con TTL gobernable (`buscador_score_ttl_dias`, 90 días; `GET /score` dice
`cache: hit|miss`); el corpus suma razones propias (semilla materializada →
banda verificada, feed verificado, longevidad Wayback). La UI (🔍 El buscador
de la ciudad) muestra cada resultado con su banda de color + razones y un
"¿Por qué veo esto?" con capas, motores caídos y principios — cero censura.

**B5 — Búsqueda general sin docker**: Wikipedia + Wikibooks + Wikiversidad
(referencia, mismo motor) y OpenAlex (academia con DOI/citas), APIs públicas
sin clave. **Orden canónico**: semillas → corpus → referencia → académica →
web — la memoria propia manda (§5.3) y la respuesta trae `orden_capas` para
que el orden sea auditable (P4).

**B4 — El juez trabaja de noche + parlamento**: el Nivel 1 responde al
instante; el juez LLM (Jan local → OpenRouter `:free` → nada, rúbrica fija de
procedencia, ~10 urls por llamada) puntúa la cola nocturna y sus veredictos
Nivel 2 refinan al heurístico con motor trazable (🤖 en la UI). Sin juez, todo
sigue (fail-open total, verificado en vivo: 502 honesto). Los parámetros los
gobierna la asamblea: valor + procedencia obligatoria + cooldown de 14 días
(409 si hay prisa).

**B6 — La Lupa (Ojo Claro + Disenso, caps. 1-4 del canon)**: cada resultado de
referencia trae su 🔍 lupa — historial del artículo (protección, reversiones,
anonimato, indicios de guerra, top editores, saltos de tamaño) y diff palabra
por palabra entre revisiones. Hechos contados, lectura humana: la máquina
muestra, tú juzgas.

**B7 — Biblioteca privada**: tus archivos propios (PDF Springer y demás +
texto plano `.txt`/`.md`, recursivo) se ingieren en casa con
`ingest_biblioteca.py` (`$env:BIBLIOTECA_PDF_DIR` al disco; `pypdf` solo para
PDF, única dependencia nueva) a `buscador_docs` capa `biblioteca`,
idempotente por hash de contenido. Reglas duras: cifrado se omite (jamás se
fuerza), lo no indexable se reporta (nada en silencio), y la API solo sirve
FRAGMENTOS (snippet FTS5 o recorte) — el libro nunca sale de tu disco, ni
siquiera vía federación searx (Opacidad Sagrada). Solo archivos propios sin
DRM; la base no se commitea.

**B8 — Biblioteca curada en 3 niveles**: `catalogo_biblioteca.py` inventaría
la fuente real (`catalogo.json`: ruta, hash, categoría, licencia, curaduría —
nada inventado); el ingestor lo lee (sin catálogo, todo nace `closed` +
privada: fail-closed). El curador publica con `POST /corpus/<id>/publicar`
(licencia explícita no-closed + nota de procedencia, M15): lo publicado cruza
al nivel 1 y a la federación; lo demás jamás sale de casa.

```powershell
# Opcional: capa web general con lente educativa (ver searxng/README.md)
$env:BUSCADOR_SEARXNG_URL = "http://127.0.0.1:8888"   # sin esto, no hay capa web
$env:BUSCADOR_UPSTREAM_TIMEOUT = "6"                   # timeout de motores (seg.)
$env:BUSCADOR_ZENODO_SIZE = "5"                        # resultados por consulta
$env:BUSCADOR_OPENALEX_SIZE = "5"                      # papers de OpenAlex (B5, sin clave)
$env:BUSCADOR_WIKIPEDIA_SIZE = "5"                     # artículos de referencia (B5, sin clave)
$env:BUSCADOR_WIKIMEDIA_SIZE = "3"                      # Wikibooks + Wikiversidad (mismo motor)
$env:BUSCADOR_JUEZ_LOTE = "10"                          # urls por llamada al juez (B4)
$env:BUSCADOR_JUEZ_TIMEOUT = "60"                       # el juez piensa despacio (seg.)
$env:BUSCADOR_OPENROUTER_MODEL = "deepseek/deepseek-r1:free"  # respaldo :free (B4)
# El juez preferente es local y reuse las variables del oráculo: LOCAL_ORACLE_BASE_URL,
# LOCAL_ORACLE_MODEL, LOCAL_ORACLE_ENABLED. Respaldo: OPENROUTER_API_KEY. Sin ambos,
# el buscador sigue con Nivel 1 (fail-open total).
```

Las semillas canónicas viven en `seeds/maxocracia.json` (5 DOI reales de
Zenodo descubiertos por API + GitHub). Para sembrar más (canal de YouTube con
su `channel_id`, hilos de X, blogs independientes): añade entradas al JSON, o
usa `POST /api/buscador/seeds` + `POST /api/buscador/seeds/<id>/verificar`
como coordinador.


## Modelo de datos (SQLite)

`users`, `branches` (9 ramas: **Ética** — orden 0, los valores primero — + 8 del saber),
`topics` (47 temas, con `prereq_ids` JSON y `dificultad` 1-5), `questions` (≥3 por tema),
`user_topics` (progreso con `estado` y `mentor_rounds`), `meetings`,
`meeting_participants`, `availability`, `materials` (la Biblioteca: guías y enlaces,
con `idioma` para convivencia de lenguas; llave única `material_key`),
`users.share_progress` (opt-in de la luz) y `users.idioma` (lengua de la persona).

La **categoría Ética** (M16) enseña los fundamentos del sistema en lenguaje común:
12 temas en el orden de los capítulos del libro, con la jerga propia (VHV, TVI, SDV,
Maxo, MaxoContract, EIR, OEV) reservada al puente final *El idioma de la ciudad*.
Diseño: `docs/architecture/ETICA_LENGUAJE_COMUN_CATEGORIA.md`.

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
