# Estado del arte — Buscador educativo independiente

> **Sesión**: 03-09-2026. **Petición de Max**: un buscador de internet para la
> sección de educación que sea *mejor que Google* — sin anuncios ni intereses
> corporativos — y que sí reconozca el contenido independiente: los papers de
> maxocracia en Zenodo, el canal de YouTube, los hilos de X.com, y toda la
> buena información que los buscadores comerciales entierran.
> **Estado**: investigación (fase 0). Este documento no implementa nada;
> delimita qué existe, qué murió, qué se puede reutilizar, y deja la base para
> el diseño de la siguiente Ola.
> **Conexión con el repo**: Biblioteca de la Ciudad (M15,
> `BIBLIOTECA_CIUDAD_MATERIAL_EDUCATIVO.md`), Parlamento Educativo (M9,
> `PROPUESTA_PARLAMENTO_UMBRAL_EDUCATIVO.md`), roadmap de la rama educativa
> (`ROADMAP_RAMA_EDUCATIVA.md`), `plataforma_educativa/`.
> **Continuación (diseño con presupuesto $0, Internet Archive priorizada,
> score de confiabilidad e hitos B1-B4)**:
> `DISENO_BUSCADOR_EDUCATIVO_GRATUITO.md`.

---

## 1. TL;DR — lo que dice el estado del arte

1. **No construir un índice web general.** Es el cementerio más poblado de la
   web independiente: Gigablast (2022), Neeva (2023), Stract (archivado
   2026). Un índice completo cuesta millones al año; incluso Marginalia, el
   mejor índice nicho del mundo, vive con ~$200/mes de infraestructura porque
   **delimitó su corpus** a lo no comercial.
2. **La base práctica existe y es madura**: SearXNG (metabuscador libre en
   Python — el mismo lenguaje del backend del proyecto) agrega 271 motores
   sin rastrear usuarios, se auto-hospeda, expone API JSON y permite definir
   motores propios. Sobre él se monta un "lente educativo" en días, no meses.
3. **Lo viejo funciona mejor que lo nuevo para encontrar lo escondido**:
   RSS/Atom, directorios humanos, feeds del Fediverso, los índices académicos
   abiertos (Zenodo, OpenAlex, ERIC) y Common Crawl permiten construir un
   corpus educativo real **sin rastrear la web entera ni pagar APIs caras**.
4. **La métrica que pide Max (reconocer lo propio y lo independiente) es
   tractable**: no es un problema de ranking global sino de **curaduría
   verificada + grafo de coherencia propia** (DOI ↔ video ↔ hilo ↔ libro) +
   heurísticas anti-comerciales ya inventadas (Marginalia, Kagi Small Web).
5. **El reranking semántico ya corre local y gratis**: Qwen3-Embedding /
   Qwen3-Reranker (Apache 2.0, 0.6B–8B, 100+ idiomas, líderes del MTEB
   multilingüe) reordenan resultados en la máquina local — y el repo ya tiene
   el hub local (Jan `localhost:1337`, oráculo DeepSeek con fallback) para
   servirlos.
6. **La diferencia no técnica es la gobernanza**: nadie en el estado del arte
   deja que la comunidad vote los pesos del ranking con parlamento, historial
   vinculante y trazabilidad T13. Eso ya existe en este repo (M9). Un
   buscador *gobernable* es la contribución original posible aquí.

---

## 2. Diagnóstico: por qué la búsqueda comercial está rota (evidencia 2024-2026)

### 2.1 Evidencia académica

El estudio **"Is Google Getting Worse? A Longitudinal Investigation of SEO
Spam in Search Engines"** (Universidad de Leipzig + Bauhaus-Universität
Weimar + ScaDS.AI, ACM EC 2024, estudio longitudinal de un año) encontró que
**todos** los buscadores examinados (Google, Bing, DuckDuckGo) tienen
problemas serios con contenido afiliado altamente optimizado: una fracción
pequeña de la web (reseñas de producto con marketing de afiliados) domina los
resultados, y cuando un patrón de spam se filtra, reaparece en forma nueva —
un juego del gato y el ratón estructural, no accidental.

A esto se suma la "enshittification" (Doctorow) como modelo de negocio
documentado: anuncios cada vez más indistinguibles del contenido orgánico,
personalización que encierra al usuario en su burbuja, y ahora resúmenes de
IA que responden con el contenido rascado de terceros sin enviarles tráfico.

### 2.2 La infraestructura de búsqueda se está cerrando

| Cierre | Fecha | Consecuencia |
|---|---|---|
| **Bing Search APIs** (Microsoft) | retirada **11-08-2025** | Los metabuscadores y apps que dependían de Bing tuvieron que migrar a alternativas 40-483% más caras (PPC Land). DuckDuckGo, Startpage, Ecosia y Qwant dependen (o dependían) de Bing/Google — la independencia real es rara. |
| **X/Twitter API** | modelo pay-per-use (por defecto para nuevos devs desde feb-2026) | Lecturas ~$0.005, escritos $0.015 ($0.20 con media/links); los planes antiguos Basic ($200/mes, búsqueda de 7 días) y Pro ($5,000/mes, archivo completo) **cerrados a altas nuevas**. Verificado: `docs.x.com/x-api/getting-started/pricing`. |
| **YouTube Data API** | vigente pero acotada | Cuota por defecto 10,000 unidades/día; `search.list` cuesta 100 unidades → **~100 búsquedas/día**. Alternativas gratuitas: feed RSS por canal (últimos ~15 videos) y `yt-dlp --flat-playlist` para metadatos de canal. |
| Reddit API | 2023 | La lección clásica: la "API gratuita" puede dejar de serlo sin apelación. |

**Lectura para el proyecto**: construir sobre APIs de terceros comerciales es
construir sobre arena. La arquitectura debe priorizar **fuentes abiertas con
contrato estable** (Zenodo, OpenAlex, ERIC, Common Crawl, RSS) y usar las
comerciales solo como semilla curada.

### 2.3 Los índices independientes: quién vive, quién murió, y por qué

| Motor | Estado a 2026-09 | Modelo | Lección |
|---|---|---|---|
| **Mojeek** (UK, desde 2004) | Vivo | Rastreador propio, sin ads, API de pago | Un índice propio es sostenible a escala modesta si el alcance es honesto. |
| **Brave Search** | Vivo | Índice propio + datos del Web Discovery Project; API $5/1k peticiones (los $5 de crédito mensual sustituyeron al free tier en 2026) | La independencia a escala se paga; para nosotros es *fuente*, no base. |
| **Marginalia** (Viktor Löfgren, Suecia) | Vivo — 4 años, 2 grants NLnet + FUTO ($15k), costos ~$200/mes | Índice propio **sesgado a lo no comercial**: penaliza SEO/ads/afiliados, prioriza blogs y páginas personales | **La prueba de que un buscador nicho cabe en un presupuesto de persona.** Comparte resultados con Kagi Teclis. |
| **Kagi** (Teclis + Small Web) | Vivo, por suscripción (~US$5-25/mes) | Sin ads, sin tracking; Teclis = rastreo propio de small web + resultados de Marginalia; Small Web = feed open source (`kagisearch/smallweb`) de blogs/feeds | El modelo de negocio sin ads funciona si el usuario paga; su índice de small web es arte del estado del arte. |
| **SearXNG** | Vivo (versiones 2026.9.x), 271 motores | Metabuscador AGPL auto-hospedado; sin tracking; API JSON activable; motores custom por configuración | **La base práctica recomendada** (Python, como el backend del proyecto). |
| **Mwmbl** | Servicio vivo, desarrollo frenado (~dic-2024); índice comunitario ~1.5B páginas | Buscador sin fines de lucro, curaduría por la comunidad | La curaduría comunitaria pura no se sostiene sola sin motor dedicado. |
| **Alexandria** (Suecia) | Durmiente (sin actividad visible 2025) | Índice construido sobre Common Crawl, sin ads | Construir sobre Common Crawl es viable pero exige mantenimiento continuo. |
| **YaCy** | Vivo (desde 2003) | P2P: cada nodo rastrea y comparte su índice descentralizado | La federación de índices es posible con tecnología vieja y probada. |
| Gigablast | Muerto (2022) | Índice propio solo | — |
| Neeva | Muerto (2023) | Sin ads, por suscripción, índice propio | Ni pagando usuarios se sostiene un índice general si se juega a ser Google. |
| **Stract** | Archivado (abr-2026); el dominio lo absorbió otra empresa | Open source, sin lucro, NLnet | Murió el *servicio*, el código sigue siendo reutilizable. |
| **EUSP / Staan** (JV Ecosia+Qwant) | Lanzado; metas ~50% de queries FR y ~33% DE a fines 2025 | Índice europeo con respaldo institucional | Hasta los "grandes independientes" europeos se aliaron para poder construir un índice: confirmación de la escala del problema. |

---

## 3. Las tecnologías antiguas que resuelven lo nuevo

La intuición de Max ("quizá con tecnologías antiguas") es correcta. Todo el
estado del arte del "small web" descansa en estándares de los 90-2000:

- **RSS/Atom/OPML** — suscribirse en vez de rastrear. El Small Web de Kagi se
  alimenta de feeds; un canal de YouTube es un RSS gratuito
  (`youtube.com/feeds/videos.xml?channel_id=...`); los blogs independientes
  casi todos publican feed. Indexar 1,000 blogs educativos = 1,000 peticiones
  HTTP al día, sin API, sin crawler distribuido.
- **Directorios humanos** — Curlie (sucesor de DMOZ), webrings, blogrolls:
  curaduría previa al SEO. Es exactamente la regla de la Biblioteca de la
  Ciudad ("los enlaces se verifican antes de sembrar") aplicada a escala.
- **Metadatos declarativos** — `sitemap.xml`, `schema.org`/JSON-LD,
  Microformats (`h-entry`)/IndieWeb: el sitio *declara* qué es; no hay que
  adivinar con un parser.
- **Índices académicos abiertos** — Zenodo, arXiv, OpenAlex, DOAJ, ERIC,
  BASE: la academia ya resolvió la discoverability sin anuncios con
  identificadores persistentes (DOI/ORCID) y OAI-PMH. Los papers de
  maxocracia en Zenodo llevan DOI del prefijo `10.5281` (DataCite) y son
  consultables por API gratuita.
- **Common Crawl** — 300,000M+ páginas acumuladas, ~2-3 mil millones de
  páginas nuevas al mes (~400 TiB/crawl, p. ej. `CC-MAIN-2026-34`), con índice
  CDXJ consultable por API: se puede "mirar el índice primero" y descargar
  solo las páginas de los dominios curados — **rastreo selectivo sin rastrear**.
- **P2P federado** — YaCy (índice compartido entre nodos), PeerTube +
  SepiaSearch (video federado), el Fediverso (Mastodon: APIs abiertas por
  instancia). La escalera N0→N1 del proyecto ya piensa en federación; el
  índice educativo puede federarse igual.

---

## 4. Fuentes y APIs verificadas para el corpus educativo

Tabla operativa (todo consultado el 03-09-2026). Las tres primeras filas son
el caso concreto de maxocracia.

| Fuente | Qué da | Acceso y límites | Coste |
|---|---|---|---|
| **Zenodo** (papers de maxocracia) | Registros con DOI, abstract, archivos | `GET https://zenodo.org/api/records?q=...` — búsqueda pública **sin token**; sintaxis de query igual a la UI; prefijo DOI `10.5281`; concept-DOI resuelve a la última versión | $0 |
| **YouTube** (canal de maxocracia + educadores) | Videos, títulos, descripciones, capítulos | (a) Feed RSS por canal (gratis, sin clave, últimos ~15 videos); (b) `yt-dlp --flat-playlist` para metadatos de todo el canal; (c) Data API: 10,000 u/día, búsqueda = 100 u | $0 en (a)/(b) |
| **X.com** (hilos de maxocracia) | Hilos, enlaces, fechas | Pay-per-use (~$0.005/lectura; "owned reads" $0.001 desde 20-04-2026); **o lista de semillas manual** (los hilos propios son finitos y se conocen) | Cientos o $0 según estrategia |
| **OpenAlex** | Grafo académico abierto (autores, obras, citas; heredero de Microsoft Academic) | API REST gratuita y generosa, sin clave; indexa DOI de Zenodo vía DataCite; autores resolvibles por ORCID | $0 |
| **ERIC** | Investigación educativa (IES, Dept. de Educación de EE. UU.) | API REST pública (`eric.ed.gov/?api`); ojo: por defecto usa OR entre términos | $0 |
| **OER Commons** | ~50k+ recursos educativos abiertos, con licencias y niveles | API de metadatos **con token** (solicitar acceso) | $0 |
| **MERLOT** | Colección curada ~85k+ materiales revisados por pares + Smart Search federada | Web service para integrar búsqueda | $0 |
| **OER Metafinder** (George Mason) | Búsqueda federada en tiempo real sobre 17 fuentes OER | Web scraping/agregación de referencia (no API formal) | $0 |
| **Wikipedia/Wikidata/Wikiversidad** | Artículos verificados, datos estructurados | REST API + SPARQL, sin clave (la Biblioteca M15 ya usa Wikipedia) | $0 |
| **PeerTube / SepiaSearch** | Video federado no-corporativo | `sepiasearch.org` + APIs de instancias | $0 |
| **Fediverso (Mastodon etc.)** | Conversación educativa independiente | API abierta por instancia (sin puerta central) | $0 |
| **Common Crawl** | Texto completo de la web para el corpus curado | Índice CDXJ por API; descarga selectiva por dominio | $0 (ancho de banda aparte) |
| **Khan Academy / MIT OCW / OpenStax** | Contenido educativo canónico | Sitemaps + deep-links directos (la M15 ya enlaza Khan) | $0 |
| **SearXNG** | Agregación web general (Google/Bing/DDG/Mojeek/Marginalia/wiby…) | Auto-hospedado; API JSON (`format=json`) | $0 + hosting |
| **Brave Search API** | SERP independiente de respaldo | $5/1,000 peticiones; $5 de crédito gratis/mes (~1,000 búsquedas) | ~$0-5/mes |

**Conclusión de la tabla**: un corpus educativo es/EN con papers, video,
OER, blogs y el contenido propio completo se construye **con $0 de APIs**
(solo hosting), porque casi todo lo valioso tiene acceso abierto. Las APIs
caras (X histórica, Brave a volumen) son opcionales y de respaldo.

---

## 5. Métricas de ranking: del PageRank a la coherencia

### 5.1 Clásicas y sus sesgos

- **BM25/TF-IDF** (relevancia léxica): base honesta, sin sesgo comercial
  inherente; no resuelve autoridad.
- **PageRank/backlinks**: mide popularidad de enlaces → hereda los sesgos del
  web comercial (quien más se promociona, más aparece) y es atacable con
  granjas de enlaces. Es la métrica que **no** ve los links de maxocracia en
  Zenodo/YouTube/X: un DOI y un hilo de X no aportan "link equity" al sitio.

### 5.2 Heurísticas anti-comerciales (ya inventadas, reutilizables)

- **Marginalia**: penaliza dominios con trackers/anuncios/afiliados y páginas
  de optimización SEO; favorece páginas personales, texto denso, sitios
  antiguos y no comerciales. El engine de SearXNG ya expone estos resultados.
- **Kagi**: lentes (filtros por dominio/bajar peso), downrank de SEO spam,
  Small Web como canal separado. Los *lenses* son exactamente el mecanismo
  del "lente educativo" propuesto aquí.
- **Million Short / wiby**: excluir los N dominios más populares o buscar solo
  la web "clásica" — trivial de implementar como filtro de corpus.

### 5.3 La métrica de identidad y coherencia (lo que pide Max)

El problema real de Max no es "rankear mejor la web": es que **lo propio y lo
independiente es invisible** para métricas de popularidad. La solución del
estado del arte es tratarlo como **corpus sembrado con identidad verificada**:

1. **Registro de identidad maxocracia**: una tabla de semillas con las
   identidades propias — DOI/concept-DOI de Zenodo, `channel_id` de YouTube,
   handles de X, ORCID, y las URLs del libro. Esto NO es SEO: es curaduría
   declarativa (la misma regla M15: se verifica antes de sembrar).
2. **Grafo de coherencia propia**: aristas cruzadas entre objetos propios
   (el paper X cita el libro Y; el video Z presenta el paper X; el hilo de X
   enlaza el video Z). Un resultado con aristas propias sube: es "el mismo
   pensamiento en otra superficie". Esto es un mini-PageRank **del corpus
   propio**, donde sí importa.
3. **Resolución de identidad externa**: ORCID → OpenAlex; DOI → Zenodo; así
   los papers aparecen con metadatos limpios sin scraping.
4. **Garantía editorial**: los resultados con identidad verificada no
   compiten por posición con el resto — entran en su propio bloque (como
   hace Kagi con Small Web). Eso elimina el incentivo a "ganar" el ranking.

### 5.4 Reranking semántico local (2025-2026)

- **Qwen3-Embedding + Qwen3-Reranker** (jun-2025, Apache 2.0; tamaños 0.6B /
  4B / 8B; 100+ idiomas): estado del arte abierto del MTEB multilingüe; el
  0.6B corre rápido en local (contexto 32k) y según la comunidad supera a los
  embeddings de OpenAI. Perfecto para es/EN sin mandar datos a la nube.
- Alternativa probada: BGE-M3 + `bge-reranker-v2-m3` (multilingüe).
- **Infraestructura ya existente en el repo**: el oráculo ya corre DeepSeek
  local vía hub Jan (`localhost:1337`, `LOCAL_ORACLE_*` en
  `app/voting_oracle.py`) y el colaborador RLM hermano. El mismo hub puede
  servir embeddings/rerank → el buscador es *soberano por diseño*: ni la
  query ni el click salen de la máquina.
- LLM como juez/sintetizador (opcional, después): resumen con citas sobre los
  resultados rerankeados (patrón RAG), con el riesgo conocido de alucinación
  mitigado por cita obligatoria a fuente.

### 5.5 Gobernanza del ranking (lo que nadie más tiene)

Coherencia directa con el repo:

- El **Parlamento Educativo (M9)** ya vota parámetros con historial
  vinculante, cooldown anti-flip-flop de 14 días y escalera de confianza
  N1+. Los pesos del buscador (cuánto pesa identidad propia vs. frescura vs.
  no-comercial vs. idioma) encajan en el mismo patrón (`edu_parameters` →
  `buscador_parameters`).
- **Regla M15 "cero rankings"** intacta: se rankea *material*, nunca
  *personas*. El muro de luces sigue en orden alfabético; el buscador ordena
  recursos, no estudiantes.
- **Transparencia**: cada resultado muestra por qué aparece ("semilla
  verificada", "fuente no comercial", "voto de parlamento vigente"). Ningún
  buscador comercial explica su ranking; es la ventaja ética y práctica.

### 5.6 Evaluación

- Métricas estándar IR: nDCG@10, MRR sobre un **set de oro propio** (50-100
  queries educativas es/EN con relevancia juzgada a mano) — barato de
  construir y suficiente para un buscador vertical.
- Benchmarks de modelos de recuperación: BEIR/MTEB multilingüe para elegir
  embeddings (Qwen3 ya es líder — ver fuentes).

---

## 6. Arquitectura candidata para maxocracia-cero (propuesta, no implementada)

```
                    ┌────────────────────────────────────────┐
   query ──►  SearXNG (lente educativa, JSON API)            │  capa web
                    │  + motores custom:                     │
                    │    Zenodo · OpenAlex · ERIC ·          │
                    │    semillas maxocracia (YAML)          │
                    └───────┬────────────────────────────────┘
                            ▼
                    fusión + heurísticas anti-comerciales
                    (boost semillas verificadas, grafo de
                     coherencia, penalización afiliados)
                            ▼
                    reranking Qwen3-Reranker vía Jan local
                            ▼
                    índice propio de corpus curado          │  capa corpus
                    (Meilisearch/FTS5 + sqlite-vec)         │
                    alimentado por: feeds RSS · Zenodo API ·
                    yt-dlp · Common Crawl selectivo
                            ▼
                    UI en plataforma_educativa (biblioteca) │
                            ▼
                    pesos votables en el Parlamento Educativo
```

**Fases** (estimación orientativa, cada una con tests y commit como manda el
roadmap de la rama educativa):

| Fase | Qué | Piezas |
|---|---|---|
| **0 — Lente educativa** (días) | SearXNG auto-hospedado (es Python como el backend), JSON API activada, motores comerciales con ads fuera, motores independientes dentro (Marginalia, Mojeek, wiby, Wikipedia); motor custom de semillas maxocracia (YAML); endpoint proxy en `plataforma_educativa/` | SearXNG, docker/pip, ~200 líneas |
| **1 — Corpus propio** (1-2 semanas) | Ingestores: Zenodo API (autor de Max), RSS del canal + yt-dlp, semillas X manuales, feeds de blogs educativos independientes, ERIC/OER Commons; extracción `trafilatura`; verificación de enlaces HTTP (regla M15) antes de sembrar; índice Meilisearch o SQLite FTS5 + embeddings Qwen3-0.6B en sqlite-vec | Python, cron |
| **2 — Reranking + gobernanza** (1-2 semanas) | Fusión de capas, rerank local vía Jan, tabla `buscador_parameters` votable (patrón M9: cooldown 14 días, T13), panel "por qué veo esto" | Python, motor `maxocontracts` sin tocar (los pesos son parámetro, no ley) |
| **3 — Federación** (futuro) | Nodos OEV comparten semillas/índices (sincronización git de semillas — el tejido forkable — o P2P estilo YaCy) | Diseño aparte |

**Costes**: desarrollo local $0; producción en un VPS pequeño (SearXNG +
Meilisearch caben en 2-4 GB RAM, ~US$5-15/mes). Referencias reales del estado
del arte: Marginalia opera su índice completo con ~$200/mes; Kagi valida el
modelo de suscripción sin ads.

---

## 7. Riesgos y límites

1. **Términos de servicio**: usar siempre API oficial o RSS (YouTube, Zenodo);
   el scraping general (`yt-dlp`) limitarlo a metadatos públicos del canal
   propio y revisarlo antes de exponerlo públicamente. X: preferir la lista
   de semillas manual (coste cero) sobre la API de pago.
2. **Cuota YouTube**: con RSS + yt-dlp la cuota no se toca; la API oficial
   queda solo como respaldo.
3. **Mantenimiento del corpus**: feeds rotos, dominios muertos → el
   verificador de enlaces de la M15 es parte del pipeline, no un extra.
4. **AI slop**: el spam generado por IA invade también el web educativo → las
   heurísticas anti-comerciales + verificación humana de semillas son el
   filtro; evaluar con el set de oro.
5. **Multilingüe**: la plataforma ya vive es/EN con convivencia de lenguas
   (campo `idioma` de materials); embeddings multilingües (Qwen3) lo
   resuelven a nivel ranking, el corpus debe etiquetar idioma igual que la
   biblioteca.
6. **"Cero rankings" de personas**: el buscador ordena material, jamás
   personas; documentarlo como guardarraíl en el diseño (como M14/M15).
7. **Alucinación de IA**: si se añade síntesis con LLM, siempre con citas
   obligatorias a las fuentes mostradas (T13: nada viaja sin procedencia).
8. **Economía de la dependencia**: SearXNG depende de motores aguas arriba
   (que pueden bloquear instancias); mitigación: motor propio de semillas +
   índice propio de corpus como capa primaria, aguas arriba como extra.

---

## 8. Conclusión del estado del arte

- Existe todo lo necesario para un buscador educativo **sin anuncios, sin
  tracking, soberano y en español**, con coste de infraestructura de decenas
  de dólares al mes: metabuscador maduro (SearXNG), fuentes abiertas con API
  estable (Zenodo, OpenAlex, ERIC, Common Crawl, RSS), índice nicho
  independiente de inspiración (Marginalia, Kagi Small Web/Teclis), y
  reranking semántico multilingüe local (Qwen3).
- Lo que **no** existe en ningún proyecto vivo del estado del arte: un
  buscador cuyo ranking esté **gobernado por su comunidad** (parlamento con
  historial vinculante), con garantía editorial para el contenido verificado
  propio, y federable al tejido educativo. Esa es exactamente la combinación
  que la Maxocracia puede aportar — y que ningún actor comercial replicará
  porque su negocio es el ranking opaco.
- El primer paso recomendado es la **Fase 0** (lente educativa sobre
  SearXNG + semillas maxocracia): es de días, cero coste, y produce un
  artefacto usable para decidir el resto con evidencia.

---

## 9. Fuentes (consultadas 2026-09-03)

**Diagnóstico**
- Estudio SEO spam: "Is Google Getting Worse?" (ACM EC 2024) —
  <https://dl.acm.org/doi/abs/10.1007/978-3-031-56063-7_4> · cobertura:
  <https://www.404media.co/google-search-really-has-gotten-worse-researchers-find/>
- Retirada Bing Search APIs (11-08-2025) —
  <https://learn.microsoft.com/en-us/lifecycle/announcements/bing-search-api-retirement> ·
  costes de alternativas: <https://ppc.land/microsoft-ends-bing-search-apis-on-august-11-alternative-costs-40-483-more/>
- X API pricing (pay-per-use) — <https://docs.x.com/x-api/getting-started/pricing> ·
  cambio 20-04-2026: <https://devcommunity.x.com/t/x-api-pricing-update-owned-reads-now-0-001-other-changes-effective-april-20-2026/263025>
- YouTube Data API quota — <https://developers.google.com/youtube/v3/determine_quota_cost> ·
  RSS de canal: <https://chuck.is/yt-rss/>

**Motores y proyectos**
- SearXNG — <https://searxng.org/> · repo: <https://github.com/searxng/searxng/> ·
  motores custom: <https://docs.searxng.org/admin/settings/settings_engines.html>
- Marginalia — <https://www.marginalia.nu/log/88-futo-grant/> ·
  <https://www.marginalia.nu/log/a_116_grant_2.0/> ·
  <https://www.marginalia.nu/log/a_114_4_years/> · about:
  <https://about.marginalia-search.com/>
- Kagi Small Web — <https://kagi.com/smallweb> ·
  <https://blog.kagi.com/small-web-updates> · repo open source:
  <https://github.com/kagisearch/smallweb> · Teclis (discusión):
  <https://news.ycombinator.com/item?id=48266174> · TechCrunch (17-03-2026):
  <https://techcrunch.com/2026/03/17/kagi-small-web-human-authored-indie-internet-mobile-ios-android-devices/>
- Mwmbl — <https://mwmbl.org/> · Alexandria — <https://alexandria.org/> ·
  Stract (archivado) — <https://github.com/StractOrg/stract> ·
  YaCy — <https://yacy.net/>
- EUSP (Ecosia+Qwant, índice Staan) — <https://www.eu-searchperspective.com/> ·
  <https://blog.ecosia.org/launching-our-european-search-index/>
- Brave Search API — <https://brave.com/search/api/>

**Fuentes de corpus y APIs**
- Zenodo API — <https://developers.zenodo.org/> · guía de búsqueda:
  <https://help.zenodo.org/guides/search/>
- OpenAlex — <https://openalex.org/> · ERIC API — <https://eric.ed.gov/?api> ·
  OER Commons API — <http://docs.oercommons.org/api/> ·
  MERLOT — <https://info.merlot.org/merlothelp/MERLOT_Technologies.htm>
- Common Crawl — <https://commoncrawl.org/> · índice CDXJ:
  <https://commoncrawl.org/cdxj-index> · estadísticas:
  <https://commoncrawl.github.io/cc-crawl-statistics/>
- SepiaSearch (PeerTube) — <https://sepiasearch.org/>

**Reranking semántico local**
- Qwen3-Embedding / Qwen3-Reranker — <https://qwenlm.github.io/blog/qwen3-embedding/> ·
  <https://github.com/QwenLM/Qwen3-Embedding> · paper:
  <https://arxiv.org/html/2506.05176v1> · modelos:
  <https://huggingface.co/Qwen/Qwen3-Embedding-0.6B>

**Contexto interno del repo**
- `docs/architecture/BIBLIOTECA_CIUDAD_MATERIAL_EDUCATIVO.md` (M15)
- `docs/architecture/ROADMAP_RAMA_EDUCATIVA.md` (M1-M9)
- `docs/architecture/PROPUESTA_PARLAMENTO_UMBRAL_EDUCATIVO.md` (M9)
- `plataforma_educativa/README.md`
- `app/voting_oracle.py` (hub local Jan `localhost:1337` — base del reranking soberano)
