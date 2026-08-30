# La Biblioteca de la Ciudad — material educativo abierto (M15)

> **Sesión**: 30-08-2026 (petición de Max: material educativo real, insertado
> fácilmente, con contenido propio de carga rápida y enlaces al mundo;
> apariencia que provoque volver; progreso y notas compartidos de forma
> voluntaria, opcional y retractable). **Estado**: diseño canónico (M15),
> ampliado por la **categoría Ética (M16)** — los fundamentos en lenguaje común
> con estructura para traducciones (idioma en materiales y personas):
> `docs/architecture/ETICA_LENGUAJE_COMUN_CATEGORIA.md`.
> Recordar: OEV §1.7-1.8 (el tejido es el conocimiento total, forkable, con
> materiales abiertos en los talleres) y §1.5 (chequeos con guardarraíles).

## 1. Qué es

La **Biblioteca de la Ciudad** es el material educativo que acompaña cada lote
(tema) de la ciudad del saber. Tres capas, cada una con su lugar:

| Capa | Qué es | Fuente | Carga |
|---|---|---|---|
| **Guías de la Ciudad** | Texto breve (250-320 palabras) por tema: qué es, lo esencial, prueba en la vida, ir más lejos | Propias (OEV, redacción por agentes + verificación humana) + aprendices que obran | Instantánea (local, sin red) |
| **Enlaces al mundo** | Un artículo de Wikipedia curado y verificado + búsquedas directas de Khan Academy / YouTube | el mundo compartido (no monopolio estatal) | Red (el mundo es el mundo) |
| **Obra de los aprendices** | El material de enseñanza que cada quien aporta al vacuar (M13: evidence) | La vacuación — la validación es la transferencia | Local |

La guía de la ciudad **nunca sustituye la obra**: el test sigue siendo el hecho
verificable, y la maestría sigue siendo la transferencia (regla de oro). El
material acompaña; la validación es de la persona.

## 2. Por qué es así (teoría)

- **El tejido, no la trama** (OEV §1.8): el contenido es conocimiento compartido
  e infinito; cada rama puede mutar (fork). Las guías nacen pequeñas y se
  enriquecen con la comunidad — se escriben en `.md` para que cualquiera pueda
  forkearlas sin máquinas.
- **Verificable, no opinión de autoridad** (Educación Siamesa §3): los enlaces
  al mundo se verifican (estado HTTP real) y se citan; la guía propia se somete
  a revisión humana antes de la siembra — todo verificador es verificable.
- **Anti-entropía δ** (cap. 5 §5.7): las guías son también material de Ronda
  (Fase 2 del mapa de gamificación) — repasar no se castiga; el que más
  necesita Ronda, más acompañado va.
- **Piso común, cielo personal**: las guías son las mismas para todos (piso);
  el ritmo lo pone la persona (cielo). Cero ranking, cero puntos comparativos
  (guardarraíl M14): **la biblioteca nunca se ordena por quién leyó más**.

## 3. Pipeline de generación e inserción (fácil de verdad)

1. **Redacción**: agentes OpenRouter `:free` redactan guías contra una plantilla
   estricta (formato de salida `=== ARCHIVO: <slug>.md ===`). Son borradores.
2. **Revisión del director**: el agente de sesión muestrea/verifica; lo que
   compromete al sistema se corrige o descarta. Nunca se siembra sin ojos
   humanos (la regla de oro del patrón de trabajo: *el subagente redacta, el
   director decide*).
3. **Inserción**: cada guía es un archivo `plataforma_educativa/materials/<slug>.md`
   con un mini front-matter de 4 líneas (`titulo`, `tema`, `orden`, otros).
4. **Sincronización**: `scripts/sync_materials.py` (con su test) los carga en
   la tabla `materials` — idempotente por `material_key`, repite sin duplicar.
5. **Cola de mejora**: cualquier persona (o agente) puede proponer una nueva
   guía o un fork simplemente dejando otro `.md` — el más reciente con el mismo
   `material_key` gana (el tejido muta, la genealogía queda en git).

## 4. Compartir la luz (espacio compartido, voluntario y retractable)

Petición de Max: *"pueden mostrarse los progresos del estudiante y sus notas en
espacio compartido, de manera voluntaria y opcional, también retractable"*.

Reglas canónicas:

- **Opt-in explícito**: la persona activa "mostrar mi luz" desde su perfil
  (un interruptor, lenguaje de calle: *"que la ciudad vea cuánto construyo"*).
  Retirable en cualquier momento: al apagarlo, la luz desaparece de inmediato
  (sin demora, sin preguntas).
- **Qué se comparte**: nombre/apodo, progreso por barrio (%), temas dominados,
  mejor nota por tema (etiqueta de nivel, no ranking) y materiales aportados.
  **Nunca**: contraseñas, emails, datos de contacto, respuestas de tests, ni
  evidencia íntima sin permiso (T13: lo que la persona no publica, no viaja).
- **Estado, no tribunal** (OEV §1.5): la vista comunitaria es un **muro de
  luces** (fichas en cuadrícula, orden alfabético — nunca por puntaje) y un
  **conteo por barrio** ("12 luces en el barrio verde") — motivación colectiva
  sin comparación de personas. Está prohibido ordenar por progreso.
- **El que no comparte, no pierde nada**: la luz de la ciudad muestra solo
  agregados, y ningún privilegio depende del opt-in.

## 5. Datos

```sql
CREATE TABLE IF NOT EXISTS materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id INTEGER NOT NULL REFERENCES topics(id),
    material_key TEXT NOT NULL UNIQUE,     -- "<topic_slug>#g<orden>"
    titulo TEXT NOT NULL,
    tipo TEXT NOT NULL DEFAULT 'guia' CHECK(tipo IN ('guia', 'enlace')),
    fuente TEXT NOT NULL DEFAULT 'oev',    -- oev | wikipedia | khan | youtube | <aprendiz>
    url TEXT,                              -- para tipo 'enlace'
    contenido TEXT,                        -- markdown, para tipo 'guia'
    autor TEXT NOT NULL DEFAULT 'siembra',
    orden INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);
```

`users.share_progress INTEGER NOT NULL DEFAULT 0` (migración idempotente).

## 6. Endpoints (nuevos, blueprint `api`)

| Método | Ruta | Qué hace |
|---|---|---|
| GET | `/api/topics/<id>/materials` | Guías + enlaces del tema (metadata; el contenido de guía se pide aparte) |
| GET | `/api/materials/<id>` | Contenido completo (markdown) de una guía |
| GET | `/api/community/lights` | Muro de luces: usuarios con opt-in (sin ranking) + conteos por barrio |
| POST | `/api/me/share-progress` | Interruptor del opt-in (body: `on` bool) |

El `POST /api/topics/<id>/materials` (coordinador) queda como API para la siembra
manual desde la UI en fases posteriores; el canal canónico de inserción es el
sincronizador de archivos (más forkable).

## 7. Tests

- `tests/test_materials.py` — CRUD de lecturas, 404s, idempotencia del sync,
  markdown servido sin revelar nada más, enlaces verificados en el seed.
- `tests/test_community.py` — opt-in/retract, luz apagada = invisible de
  inmediato, cero ranking (orden alfabético), agregados por barrio sin datos
  privados.
- Suite completa de la plataforma en verde (49 → 60+).

## 8. Referencias

- OEV §1.1 (Rondas), §1.5 (chequeos con guardarraíles), §1.7-1.8 (triada +
  tejido). `docs/theory/ESTRUCTURA_IDEAL_ORGANISMO_EDUCATIVO_VITAL.md`.
- Educación Siamesa §3 (validación por hecho), §5 (piso común).
- M14 Ciudad del Saber: `docs/architecture/GAMIFICACION_CIUDAD_APRENDIZAJE.md`.
- T13 (registro público / privacidad): libro cap. 19 y motor `maxocontracts`.
