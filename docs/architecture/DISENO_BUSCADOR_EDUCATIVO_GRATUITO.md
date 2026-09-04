# Diseño — Buscador educativo gratuito ($0 para el proyecto, $0 para la persona)

> **Sesión**: 03-09-2026 (continuación del estado del arte,
> `ESTADO_DEL_ARTE_BUSCADOR_EDUCATIVO.md`). **Petición de Max**: priorizar
> Internet Archive / Wayback Machine; incorporar blogspots y fuentes
> independientes; honestidad sobre la infraestructura de distorsión; y un
> **diseño con presupuesto cero** — con un pequeño uso de API de DeepSeek u
> OpenRouter (el agente `core/openrouter_engine.py` del proyecto hermano
> `local_models`) para dar un *score de confiabilidad* a los resultados.
> **Regla dura de este diseño**: ninguna pieza depende de dinero recurrente,
> ninguna pieza cobra al usuario, y ninguna pieza deja de funcionar si una API
> de pago desaparece (fail-open).

---

## 1. Principios constitucionales del buscador

| # | Principio | Qué implica |
|---|---|---|
| P1 | **$0 proyecto, $0 persona** | Sin APIs de pago obligatorias, sin hosting de pago obligatorio, sin cuentas ni cobros para buscar. |
| P2 | **Local primero** | Reranking y scoring corren en el hub local (Jan `localhost:1337`); la nube es respaldo opcional, nunca requisito. Ni la query ni el click salen de la máquina si no hace falta. |
| P3 | **Etiqueta, no censura** | El buscador nunca oculta resultados: ordena, etiqueta y explica. Toda ocultación silenciosa está prohibida (es exactamente lo que criticamos). |
| P4 | **Transparencia del ranking** | Cada resultado puede mostrar *por qué* está donde está (fuente, señales, pesos vigentes y su votación). |
| P5 | **Gobernanza** | Los pesos del ranking y los umbrales del score son parámetros votables en el Parlamento Educativo (patrón M9: historial vinculante T13, cooldown 14 días). |
| P6 | **Verificación antes de sembrar** | Herencia M15: ningún enlace entra al corpus sin verificación HTTP y ojos humanos. La cola de verificación es parte del pipeline, no un extra. |
| P7 | **Cero rankings de personas** | Se ordena material, nunca estudiantes (guardarraíl M14/M15 intacto). |
| P8 | **El archivo es memoria** | Internet Archive como capa prioritaria: longevidad como señal, rescate de enlaces muertos, y preservación propia deliberada. |

---

## 2. Presupuesto real

| Concepto | Coste | Nota |
|---|---|---|
| Desarrollo | $0 | Máquina local de Max (igual que toda la plataforma educativa). |
| APIs de fuentes | $0 | Zenodo, OpenAlex, ERIC, Wayback/IA, RSS de canales y blogs, Common Crawl: todas gratuitas (ver estado del arte, tabla de fuentes). |
| Hosting producción | $0–15/mes | Opción A ($0): mismo servidor/máquina que ya corre la plataforma educativa. Opción B ($0): free tier tipo Oracle Cloud Always Free (ARM, 4 OCPU/24 GB — verificar disponibilidad regional). Opción C: VPS pequeño si algún día hay presupuesto. |
| Modelos de scoring | $0 | Preferente: local vía Jan `localhost:1337` (ya existe para el oráculo). Respaldo: OpenRouter modelos `:free` — verificado: **20 req/min, 50 req/día** gratis; con **$10 comprados una sola vez (no recurrente)** el límite sube a **1,000 req/día** de por vida de la cuenta. |
| Brave Search API (respaldo opcional) | $0–5/mes | Solo si algún día se quiere respaldo SERP; no es requisito. |
| **Total obligatorio** | **$0** | — |

Con el cache de scores (§5.4), incluso el tier gratis de 50 req/día basta: es
una cola nocturna que puntúa solo URLs nuevas.

---

## 3. Fuentes por capas (con Internet Archive priorizada)

### 3A — Capa archivo: Internet Archive / Wayback Machine (prioritaria)

Cuatro roles concretos, todos vía APIs gratuitas:

| Rol | API | Uso en el buscador |
|---|---|---|
| **Longevidad como señal** | CDX: `https://web.archive.org/cdx/search/cdx?url=dominio&limit=1` | La primera captura de un dominio es una señal anti-spam barata y honesta: un blog vivo desde 2012 vale más que uno creado el mes pasado (el spam educativo de IA rara vez tiene historia). |
| **Rescate de enlaces muertos** | Availability: `https://archive.org/wayback/available?url=` | Un 404 no es fin: se ofrece el snapshot más cercano ("lo que decía"). Regla de la biblioteca: el enlace muerto se conserva *con fecha*, nunca se sustituye en silencio. |
| **Preservación propia deliberada** | Save Page Now: `https://web.archive.org/save/` (con cuenta, rate-limited) | Los papers de Zenodo, hilos de X, videos y materiales del corpus sembrado se archivan bajo demanda. La maxocracia no deja su memoria en manos de terceros. |
| **Colecciones abiertas** | Advancedsearch: `https://archive.org/advancedsearch.php` · Metadata: `https://archive.org/metadata/<id>` | Textos, audio y video educativos de dominio público (incl. Open Library) como resultados de primera clase. |

**Riesgo documentado y su mitigación**: Internet Archive perdió *Hachette v.
Internet Archive* (2ª Circuito 2024; fin del caso dic-2024) y resolvió el
pleito de las discográficas (Great 78) con acuerdo confidencial (sep-2025);
hacia nov-2025 la propia IA declara no tener litigios mayores activos — y en
todos los casos el **Wayback Machine no fue parte**. Aun así, en oct-2024
sufrió un gran DDoS con exposición de registros de cuentas (ampliamente
reportado). **Mitigación**: la IA es *complemento de memoria, no único punto
de fallo* — toda semilla tiene copia local del registro (metadatos) y la
preservación propia no depende solo de la IA.

### 3B — Capa blogs independientes (blogspot y amigos)

La clave: **los blogs ya son máquinas de indexación gratuitas**.

- **Feeds automáticos sin API ni clave**: Blogger/blogspot expone
  `/feeds/posts/default` (Atom) o `?alt=rss` en cada blog; WordPress
  `/feed`, Substack `/feed`, Ghost `/rss/`. Indexar 1 blog = 1 URL.
- **Descubrimiento en cascada (el rastreador de confianza)**: cada blog
  sembrado aporta sus *blogrolls* y enlaces de lectura; los webrings y
  directorios humanos (Curlie, heredero de DMOZ) y las recomendaciones
  cruzadas del Fediverso expanden la red. El crawler solo sigue **enlaces
  hechos por humanos** (blogrolls, páginas "sobre mí", webrings), nunca
  SERPs comerciales → la red de confianza crece sola sin diluirse.
- **Reglas heredadas de la M15**: todo candidato entra a la cola de
  verificación (HTTP real + revisión humana); sin verificación, no se siembra.
  El material educativo blogspot de calidad existe — solo está fuera de las
  métricas comerciales — y un feed de 2011 con veinte lectores puede valer
  más que un portal con ads.

### 3C — Capa académica abierta

Zenodo (API pública, papers de maxocracia incluidos), OpenAlex, ERIC, OER
Commons/MERLOT, DOAJ/arXiv/BASE — detalle completo y endpoints en el estado
del arte (§4). Sin cambios de diseño: es la capa con mejor relación
calidad/coste ($0) de todo el sistema.

### 3D — Capa video y federada

YouTube vía RSS de canal + `yt-dlp --flat-playlist` (metadatos del canal
propio y de canales educativos sembrados; sin tocar la cuota de la Data
API), PeerTube/SepiaSearch, Fediverso (APIs abiertas por instancia).

### 3E — Capa respaldo web general

SearXNG auto-hospedado como lente educativa (motores independientes dentro:
Marginalia, Mojeek, wiby; motores de ads fuera). Es la capa "el resto de la
web" — útil, pero **no es la identidad del buscador**: la identidad es el
corpus sembrado y verificado (A–D).

---

## 4. Sinceridad: ¿existe una infraestructura que limita, enfoca, censura y distorsiona?

Respuesta honesta y con evidencia: **sí, con matices importantes**. No hace
falta ninguna teoría de un comité central; lo documentado es peor y más
interesarante: son **mecanismos estructurales** — económicos, legales,
técnicos y editoriales — que producen sistemáticamente el efecto que Max
intuye, sin que nadie tenga que conspirar.

| Mecanismo | Evidencia documentada | Qué produce |
|---|---|---|
| **Incentivo comercial del ranking** | Estudio longitudinal Leipzig/Weimar (ACM EC 2024): el spam de afiliados domina los resultados de todos los buscadores examinados, en un juego del gato y el ratón sin fin. | Lo optimizado para dinero desplaza a lo verdadero. |
| **El orden es poder** | SEME — "Search Engine Manipulation Effect" (Epstein & Robertson, PNAS 2015): solo reordenar resultados desplaza las preferencias de votantes indecisos en más de 20 puntos sin que nadie lo note. | Cualquier ranking (también el nuestro) es una palanca editorial de primer orden. |
| **Downranking editorial declarado** | YouTube (ene-2019): "reducir recomendaciones de borderline content" aunque no viole reglas; dic-2019: 30+ cambios, −70% de watch time en ese contenido ([blog oficial](https://blog.youtube/news-and-events/continuing-our-work-to-improve/), [The Verge](https://www.theverge.com/2019/12/3/20992018/youtube-borderline-content-recommendation-algorithm-news-authoritative-sources)). Google: whitepaper *How Google Fights Disinformation* (Múnich, 2019) + directrices de calidad (YMYL/E-A-T, democión "Upsetting-Offensive"). | Una categoría indefinida ("borderline") baja de visibilidad por decisión interna, sin apelación ni transparencia. Puede usarse bien o mal — el problema es que es **opaca y sin derecho de réplica**. |
| **Remociones legales a escala** | Google Transparency Report: millones de URLs retiradas por año (DMCA, órdenes de gobiernos); DSA europea con obligaciones de filtrado. | La presión legal filtra el corpus antes de que el usuario elija. |
| **Jawboning gubernamental** | Twitter Files (2022-2023, documentación interna de coordinación Estado-plataforma); litigado en EE. UU. (*Murthy v. Missouri*, 2024). | La moderación puede ser impuesta desde fuera sin proceso público. |
| **Puntos de estrangulamiento físico** | Cierre de Bing Search APIs (11-08-2025); X API a pay-per-use; [Cloudflare bloquea AI crawlers por defecto desde jul-2025](https://blog.cloudflare.com/content-independence-day-no-ai-crawl-without-compensation/) (416 mil millones de peticiones bloqueadas a fin de 2025, CEO en WIRED). | Quien controla APIs, CDN y Payment Rails decide *quién puede existir* como buscador o fuente. |
| **Colapso del tráfico editorial** | Pew (jul-2025): con resumen de IA, los usuarios hacen clic menos; DCN/Digiday: −10% de referidos de Google en editoriales; Seer Interactive: −61% de CTR orgánico con AI Overviews; Press Gazette/Chartbeat: tráfico desde Google **−un tercio** en un año (hasta nov-2025). | El modelo "la web se financia con visitas de buscador" está muerto; lo que queda se concentra aún más arriba. |
| **Ataques a la memoria** | *Hachette v. IA* (perdida 2024), pleito discográficas (acuerdo sep-2025), DDoS/exposición de cuentas (oct-2024). | El archivo del mundo es un blanco; la preservación no puede delegarse por completo. |

**Lo que NO está documentado** (y por honestidad se declara): un único
organismo que orqueste todo. El fenómeno es **emergente**: gradientes de
incentivo + palancas legales + puntos de control técnico bastan para
producir limitación, enfoque, censura y distorsión a escala civilizatoria. De
hecho eso lo hace más grave: no hay quien llamar a la puerta.

**La autocrítica obligatoria**: si el ranking es poder (SEME), nuestro
buscador también es poder. El antídoto no es "ser buenos" sino diseño: P3
(etiqueta, nunca ocultar), P4 (explicar), P5 (los pesos los vota el
parlamento con historial público T13), y rúbrica de score centrada en
**procedencia verificable, no en conformidad de opinión**. Un buscador
alternativo sin estos guardarraíles sería solo otro pastor con otro rebaño.

---

## 5. El score de confiabilidad (diseño $0)

### 5.1 Filosofía

- Es una **etiqueta explicable**, no un número mágico ni un veredicto de
  verdad. Mide *procedencia y transparencia de la fuente*, nunca su alineación
  ideológica.
- Se muestra en bandas con razones: p. ej. **"Verificada"** (semilla con
  revisión humana), **"Rastreable"** (autor identificable, cita fuentes, sin
  ads), **"Desconocida"** (sin señales — que es información útil, no castigo).
- **Nunca elimina ni oculta** resultados (P3). Lo que hace el score es
  reordenar dentro de cada capa y acompañar al lector con razones visibles.

### 5.2 Nivel 1 — Heurístico (corre en TODO resultado, $0, sin LLM)

Señales calculables sin red extra (los pesos iniciales son parámetro votable):

| Señal | Fuente del dato | Dirección |
|---|---|---|
| Semilla verificada (M15) | tabla `buscador_seeds` | ↑↑ |
| DOI/ORCID/ISBN identificables | patrón regex + OpenAlex | ↑ |
| Autor persona identificable | metadatos (byline, `author`, JSON-LD) | ↑ |
| Cita fuentes externas | extracción de enlaces salientes (trafilatura) | ↑ |
| Antigüedad del dominio | primera captura en Wayback CDX | ↑ |
| Sin trackers de ads (heurística) | hosts conocidos de ad-tech en el HTML | ↑ |
| Feed/RSS presente | descubrimiento de `/feed`, `/feeds/...` | ↑ |
| Enlace muerto pero archivado | Wayback availability | → (se marca "histórico") |
| Dominio joven + optimización SEO agresiva | Wayback + densidad de keywords/afiliados | ↓ |

### 5.3 Nivel 2 — LLM juez (opcional, por lotes, fail-open)

- **Preferente: local** vía el hub Jan `localhost:1337` (el mismo que sirve el
  oráculo de votación; DeepSeek local). $0, sin cuota, offline. El proyecto
  hermano ya tiene el patrón exacto en
  `local_models/core/openrouter_engine.py` (interfaz `chat()`, throttle de
  1.8 s contra 429, `OPENROUTER_API_KEY` por env) — el buscador replica ese
  patrón con un `ScoreEngine` que elige motor: `JanLocalEngine` →
  `OpenRouterFreeEngine` → nada (solo Nivel 1).
- **Respaldo: OpenRouter `:free`** (misma API OpenAI-compatible). Límites
  verificados: 20 req/min; **50 req/día** gratis, o **1,000 req/día** si se
  compraron $10 de crédito una única vez. Rúbrica fija por prompt
  (procedencia, citas, densidad comercial, tono, autoría) sobre **lotes de
  ~10 URLs por llamada** → 50/día = 500 URLs/día; 1,000/día = 10,000.
- **Cola + cache**: solo se puntúan URLs nuevas (cache SQLite con TTL de 90
  días); el scoring nocturno no interfiere con la búsqueda.
- **Fail-open total**: sin key, sin cuota (429) o sin hub local → el buscador
  funciona igual con Nivel 1. El LLM **jamás bloquea** una búsqueda.
- **Procedencia del score**: cada score registra qué motor lo produjo
  (`jan:deepseek-local` / `openrouter:deepseek-r1:free` / `heuristico:v1`) y
  se muestra en la UI — el score también tiene trazabilidad T13.

### 5.4 Modelo de datos (SQLite, estilo `plataforma_educativa`)

```sql
buscador_seeds      (id, url, tipo[paper|video|hilo|blog|oer], fuente,
                     identidad_id, verificada, idioma, created_at)
buscador_docs       (id, url, titulo, resumen, texto_limpio, idioma,
                     capa[archivo|blogs|academico|video|web], seed_id,
                     wayback_ts, wayback_url, indexed_at)
buscador_scores     (url, nivel[1|2], banda[verificada|rastreable|desconocida],
                     razones_json, motor, scored_at, ttl_dias DEFAULT 90)
buscador_parameters (parametro, valor, procedencia)   -- patrón M9: votable,
                                                      -- historial en resolutions, T13
```

### 5.5 Endpoints (en `plataforma_educativa/`)

| Método | Ruta | Qué hace |
|---|---|---|
| GET | `/api/buscador?q=&capa=&idioma=` | Búsqueda unificada (corpus propio primero, respaldo SearXNG después); resultados con banda + razones |
| GET | `/api/buscador/score?url=` | Score actual y sus razones (explicabilidad P4) |
| POST | `/api/buscador/seeds` | Alta de semilla (coordinador; entra a verificación) |
| POST | `/api/buscador/archivar` | Envía una semilla/doc a Save Page Now (preservación propia) |
| GET | `/api/buscador/parametros` | Pesos vigentes + su resolución de parlamento |

---

## 6. Hitos (estilo del roadmap de la rama educativa)

Regla de coherencia heredada: cada hito = commit conventional en español +
tests + entrada en `atribuciones_sinteticas.md`.

| Hito | Qué entrega | Tests |
|---|---|---|
| **B1 — Lente + semillas** ✅ (03-09-2026) | SearXNG configurado (lente educativa), tabla `buscador_seeds` con las identidades maxocracia (Zenodo DOIs, canal, hilos, libro), motor de semillas como engine custom de SearXNG, endpoint proxy `/api/buscador` | proxy, fail-open sin SearXNG, semillas — **implementado: `app/buscador.py` + `app/buscador_routes.py` + `seeds/maxocracia.json` (5 DOI reales de Zenodo) + `searxng/`; 18 tests, plataforma 99/99** |
| **B2 — Corpus verificado** | Ingestores: Zenodo API, RSS/yt-dlp, blogs por feed, Wayback (CDX/availability/SPN); verificación HTTP previa (regla M15); índice SQLite FTS5 (o Meilisearch si hay 1 GB RAM de sobra) | idempotencia de ingestores, verificación obligatoria, wayback rescue de 404 |
| **B3 — Score Nivel 1 + UI** ✅ (04-09-2026) | Heurísticas de confiabilidad, bandas + razones en la UI de resultados, "por qué veo esto" | señales, TTL de cache, cero ocultación de resultados — **implementado: `buscador_scores` con TTL gobernable + `enriquecer_corpus` (procedencia/longevidad local) + UI 🔍 con bandas y por-qué-veo-esto; 7 tests, plataforma 119/119** |
| **B4 — LLM juez + parlamento** | `ScoreEngine` local→OpenRouter free→nada; cola nocturna; `buscador_parameters` votable en el Parlamento Educativo (cooldown 14 días) | fail-open en 429/timeout, rúbrica JSON estricta, votación de pesos |
| **B5 — Capas abiertas directas** ✅ (04-09-2026, adelantada a petición de Max: búsqueda general sin docker) | Wikipedia en español (referencia) + OpenAlex (academia con DOI/citas), APIs públicas sin clave, fail-open | parseo, fail-open, capas en la unificada — **implementado: `engine_wikipedia` + `engine_openalex` en `app/buscador.py`; 5 tests, verificado en vivo ("fotosintesis" → 10 académica + 5 referencia)** |

---

## 7. Riesgos del diseño

1. **Dependencia de aguas arriba (SearXNG)**: los motores que agrega pueden
   bloquear instancias → el corpus propio (capas A–D) es la capa primaria; el
   web general es extra.
2. **ToS**: usar siempre API oficial o RSS; `yt-dlp` solo para metadatos
   públicos de canales sembrados, y revisado antes de exponerlo públicamente.
   X: semilla manual (coste cero) antes que API de pago.
3. **Internet Archive como blanco**: mitigado en §3A — copia local de
   registros + preservación propia; la IA nunca es el único punto de fallo.
4. **El LLM juez puede equivocarse**: por eso su salida es una banda con
   razones revisables, nunca un veto; el parlamento puede cambiar la rúbrica;
   y el motor heurístico siempre existe como suelo.
5. **Free tier de OpenRouter puede cambiar**: verificado a hoy (50/1,000
   req/día); el diseño lo tolera porque el motor preferente es local.
6. **Crecimiento del corpus**: el costo de la verdad es la curaduría; la cola
   de verificación humana es la parte irreductible del sistema (y su valor
   diferencial: es lo que Google no puede comprar).

---

## 8. Fuentes nuevas de este documento (consultadas 03-09-2026)

- OpenRouter límites del tier gratuito — <https://openrouter.ai/docs/api_reference/limits> ·
  <https://openrouter.ai/pricing>
- Litigios de Internet Archive — <https://www.eff.org/cases/hachette-v-internet-archive> ·
  <https://blog.archive.org/2024/12/04/end-of-hachette-v-internet-archive/> ·
  <https://www.rollingstone.com/music/music-news/internet-archive-labels-settle-great-78-copyright-lawsuit-1235427887/> ·
  <https://arstechnica.com/tech-policy/2025/11/the-internet-archive-survived-major-copyright-losses-whats-next/>
- Downranking de "borderline content" — <https://blog.youtube/news-and-events/continuing-our-work-to-improve/> ·
  <https://www.theverge.com/2019/12/3/20992018/youtube-borderline-content-recommendation-algorithm-news-authoritative-sources> ·
  <https://www.kopp-online-marketing.com/how-google-fights-misinformation>
- SEME (PNAS 2015) — <https://www.pnas.org/doi/10.1073/pnas.1415257115>
- Cloudflare "Content Independence Day" — <https://blog.cloudflare.com/content-independence-day-no-ai-crawl-without-compensation/> ·
  <https://www.wired.com/story/big-interview-event-matthew-prince-cloudflare/>
- Colapso de tráfico editorial — <https://www.pewresearch.org/short-reads/2025/07/22/google-users-are-less-likely-to-click-on-links-when-an-ai-summary-appears-in-the-results/> ·
  <https://digiday.com/media/google-ai-overviews-linked-to-25-drop-in-publisher-referral-traffic-new-data-shows/> ·
  <https://pressgazette.co.uk/media-audience-and-business-data/google-traffic-down-2025-trends-report-2026/>
- Proyecto hermano — `C:\Users\DARKM\Documents\local_models\local_models\core\openrouter_engine.py`
  (patrón de motor OpenRouter con throttle anti-429; API key por `OPENROUTER_API_KEY`).
