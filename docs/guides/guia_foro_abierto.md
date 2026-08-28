# Foro Abierto — la plaza del conocimiento

> Documento de la rama educativa (OEV §1.7-1.8). Fuente única de verdad sobre el foro de la plataforma.

## 1. Qué es

El Foro Abierto es la **plaza pública del conocimiento** de la Maxocracia: el primer
espacio al que llega una persona cuando quiere aprender, enseñar o resolver algo junto
a otras. Es la puerta de entrada a la estructura triádica del aprendizaje (Foro →
Talleres → Grupos de Solución → Células Madre).

Su regla de oro es la **ignorancia bienvenida**: quien llega sin saber pregunta, y
quien sabe ofrece. No hay examen de entrada, no hay credencial previa, no hay juez
que decida quién merece hablar. Toda voz con silla: la disidencia no se borra, se
atiende (T12). Todo lo que se publica queda registrado con autor, fecha y estado
(T13) — la plaza expone **estado**, no jerarquía.

## 2. Qué se publica (los cuatro tipos)

En la plaza se publican cuatro tipos de contenido, todos con el mismo trato
(ignorancia bienvenida, voz con silla, registro auditable). Cada tipo tiene un
destino natural en la estructura triádica:

| Tipo | Símbolo canónico | Ejemplo de uso | Destino en la estructura triádica |
|---|---|---|---|
| **Tema** | `topic` | "Qué es la entropía del conocimiento (δ) y por qué importa" | Conversación abierta: la plaza como ágora. |
| **Pregunta** | `question` | "¿Cómo cierro un post con resolución auditable?" | Si la pregunta florece, convoca a un **Taller de Aprendizaje**. |
| **Oferta de taller** | `workshop_offer` | "Ofrezco taller de cocina fractal: sobras → fermentos → proteína" | Nace un **Taller de Aprendizaje** (5-12, facilitador, obra de salida). |
| **Necesidad** | `need` | "Necesito apoyo para reparar el techo de la célula del barrio" | Aparece en la puerta hacia **matching** y los **Grupos de Solución (ECEs)**. |

Los cuatro tipos viajan juntos: un tema se vuelve pregunta, una pregunta convoca
un taller, una necesidad suma manos, y las personas que se encuentran terminan
formando una célula.

## 3. Reglas de la plaza (los guardarraíles)

- **Sin matrícula ni credencial** — la ignorancia bienvenida (A2: el deber de
  buscar). El primer mensaje no exige currículum.
- **El disidente tiene silla** (T12) — la plaza no borra contenidos ajenos. Un
  post se cierra, no se silencia. Quien discrepa responde; quien modera cierra;
  nadie elimina por opinión.
- **La conversación se cierra con resolución auditable** (T13) — un post
  cerrado o resuelto **no recibe respuestas nuevas**: el cierre es el fin
  declarado de la conversación. El registro queda (autor, fechas, estado,
  resolución).
- **Sin rankings ni puntajes por persona** — anti-gamificación. La plaza
  expone estado (`open` / `closed` / `resolved`), no jerarquía. No hay karma,
  no hay tabla de "top contribuidores".
- **Cero juicio de entrada** — el moderador cierra por spam o cumplimiento
  legal; nunca por opinión. La voz molesta también tiene silla.

## 4. Cómo usarla (paso a paso para un miembro)

1. **Entrar a `/foro`** — la plaza en el navegador (también accesible vía la API
   que listamos abajo).
2. **Elegir el tipo** — tema, pregunta, oferta de taller o necesidad. No hay
   jerarquía entre los cuatro; el tipo es solo la forma que toma la intención.
3. **Publicar** — título (hasta 200 caracteres), cuerpo (hasta 5 000) y, si
   quieres, hasta 10 *tags* (palabras clave que ayudan a encontrar el post).
4. **Responder a un hilo** — al abrir un post aparece "Respuestas (N)"; quien
   quiera aportar envía su respuesta. El hilo crece en orden cronológico.
5. **Cerrar con resolución** — cuando la conversación terminó, el autor (o un
   admin) cierra el post. Si se incluye una `resolution`, el estado pasa a
   `resolved`; si no, a `closed`. A partir de ahí, el post no acepta respuestas
   nuevas.
6. **Para una necesidad** — publicar con tipo `need` (opcionalmente vinculando
   un `need_id` de `forms_bp`); la publicación aparece también en
   `GET /forum/needs`, la puerta hacia el *matching* y los Grupos de Solución.

## 5. Endpoints (referencia)

Los nombres y parámetros están verificados contra `app/forum_bp.py` (blueprint
`forum`, prefijo `/forum`). Todos requieren autenticación (`token_required`).

| Método | Ruta | Propósito |
|---|---|---|
| `POST` | `/forum/posts` | Publicar en la plaza. Body: `kind` ∈ {`topic`, `question`, `workshop_offer`, `need`}, `title`, `body`, `tags` (lista, opcional), `need_id` (opcional, solo si `kind=need`). |
| `GET` | `/forum/posts` | Listar la plaza. Filtros por query string: `type=` (canónico del *kind*), `tag=`, `status=` (`open` \| `closed` \| `resolved`), `limit=` (1-100, por defecto 50). Orden: más reciente primero. |
| `GET` | `/forum/posts/<id>` | Detalle de un post (T13: autor, fechas, estado, etiquetas). |
| `POST` | `/forum/posts/<id>/replies` | Responder en el hilo. Body: `body` (texto, requerido). Falla con 400 si el post está cerrado o resuelto. |
| `GET` | `/forum/posts/<id>/replies` | Listar las respuestas de un post en orden cronológico ascendente. |
| `POST` | `/forum/posts/<id>/close` | Cerrar el post. Solo el autor o un admin. Body: `resolution` (opcional, hasta 1 000 caracteres). Si hay resolución → estado `resolved`; si no, `closed`. |
| `GET` | `/forum/needs` | Listar las necesidades **abiertas** del foro (posts de tipo `need` con estado `open`). Es la puerta hacia el *matching* y los Grupos de Solución (ECEs). |

Notas operativas:

- El parámetro de filtro de tipo en el listado se llama **`type`** (en el
  payload de creación se llama `kind`); ambos aceptan los mismos valores
  canónicos.
- El blueprint **no duplica** las necesidades de `forms_bp` (`participant_needs`):
  el post de tipo `need` puede *referenciar* una necesidad existente vía
  `need_id`; `/forum/needs` es el índice, no la fuente de verdad.
- `init_forum_tables()` crea las tablas `forum_posts` y `forum_replies` (esquema
  idempotente, con `CHECK(kind IN (...))` y `CHECK(status IN (...))` para que la
  base de datos también defienda los guardarraíles).

## 6. De la plaza al conocimiento (el puente)

Del Foro Abierto nacen **tres caminos**, que son los otros tres cuerpos de la
estructura triádica del aprendizaje:

- **Preguntas y ofertas → Talleres de Aprendizaje** — el hilo donde la pregunta
  se respondió convoca a quien sabe, y de ahí nace un taller pequeño (5-12
  personas), con facilitador, obra de salida y materiales abiertos. El taller
  no necesita permiso: se auto-organiza desde la plaza.
- **Necesidades → Grupos de Solución (ECEs)** — la necesidad entra de la
  comunidad, la solución vuelve a ella. Cada grupo documenta y forma: siembra
  aprendizaje al resolver.
- **Personas que se encuentran → Células Madre** — el meta-grupo cuyo oficio
  es formar otros grupos (el fractal en su tercer nivel): la célula produce
  grupos; cada grupo produce más grupos.

Los tres enlaces viven ya en la plataforma: `/talleres` para los talleres,
`/grupos` para los grupos de solución, y el panel de Células para las células
madre. El foro es la **puerta**; el resto del organismo se llena desde ahí.

> *"La pregunta sin examen de entrada es el acceso a la verdad."*
> — Axioma 5 de la Maxocracia (Educación Integral: democratizar el acceso a la
> verdad, reducir asimetrías de información).
