# Biodiversidad (dimensión transversal del SDV-E)
## La dimensión de mayor peso medida como conjunto —integridad biótica, tasa de extinción, riesgo de colapso, diversidad genética y sitios insustituibles—: el mismo instrumento para un bosque, un humedal, un río, un arrecife o un suelo vivo, sin depender del tipo de ecosistema

**Autoría:** Oráculo Sintético DeepSeek & Max Nelson López Restrepo
**Fecha:** octubre 2026
**Proyecto:** Maxocracia — El gobierno de la verdad, el tiempo y la vida
**Licencia:** Creative Commons BY-SA 4.0
**Estado:** Propuesta de estándar (rama SDV-E, Ola 4) — NO canon hasta ratificación
**Referencia canónica:** Cap. 10 §10.4 · Cap. 16.5 §16.5.14 · EVV-1.2 §4.3 · Cap. 9.5 (precedente SDV-S)
**Documento:** 20 de la biblioteca `docs/theory/SDV-E/`
**Revisión:** octubre 2026 — redactado contra el informe de fuentes verificado de esta rama
(`scratch/sdv_e/fuentes/20_biodiversidad.md`: 37 filas de parámetros con estado HTTP registrado y la
lista de lo que **no** se pudo verificar) y contra la lectura directa de los documentos 01 a 18 de esta
biblioteca. Este documento **no re-verifica umbrales ajenos**: los consume, los ordena por naturaleza
jurídica y declara de dónde vienen. Dos cosas se comprobaron con herramienta **en esta sesión de
redacción**: la página de integridad de la biosfera del Stockholm Resilience Centre (HTTP 200, texto
leído: **más de 100 extinciones por millón de especies-año** y **30 % de la energía disponible de la
naturaleza** apropiada por humanos, con **ambas variables de control transgredidas**) y la subpágina del
*Planetary Health Check* (HTTP 200, **sin cifras entregadas al lector**: solo su navegación). Todo lo
demás va con la marca de evidencia que le corresponde, incluida la marca de vacío.

---

## 1. Qué es (y qué no es) este SDV

**Qué es.** Este documento fija **una sola dimensión** del SDV-E —la **biodiversidad**— y la fija
**como métrica de conjunto**, no por ecosistema. Es la dimensión de **mayor peso** de la tabla que el
[documento 07](07_Formula_de_violacion_y_pesos.md) ratifica para el estándar: **0,300** en
`PESOS_TABLERO` y **0,300** en `PESOS_PISO`, el doble del suelo (0,150) y muy por encima de la
conectividad (0,075). Responder *"¿cómo se mide la biodiversidad de esta unidad concreta?"* **sin que la
respuesta dependa del tipo de ecosistema** es el trabajo entero de estas páginas.

**Existe porque hay un hueco con nombre propio.** El canon manda proteger, para todo ecosistema, el
*"área mínima para biodiversidad viable"* y la *"fauna acuática viable"* (Cap. 10 §10.4), y **no publica
la cifra de ninguna de las dos**. El instrumento que el proyecto ya tenía —el ISE, con Biodiversidad al
30 %— **mide composición pero no condición**, no dice qué es violar y no tiene código
(`docs/architecture/metricas_detalle_kpis_oraculos_dinamicos.md`, IN-01). Y los documentos de esta
biblioteca que ya se escribieron dejaron el hueco **declarado y abierto**, cada uno desde su tipo: el
[documento 12](12_Ecosistemas_Rios_y_cuencas.md) retira el 0,300 de biodiversidad de su tabla fluvial
*"sin sustituto"* porque **un río concreto no tiene BII propio**; el
[documento 16](16_Ecosistemas_Montanas_y_criosfera.md) demuestra que **un índice de biodiversidad
ingenuo sube mientras el ecosistema alpino se pierde**; el [documento 18](18_Ecosistemas_Agroecosistemas.md)
separa polinizadores y enemigos naturales del agregado *"Biodiversidad"* porque son **funciones**, no
censos. Este documento responde a los tres.

**Qué no es.**

- **No es el estándar por tipo de ecosistema.** Los umbrales físicos, químicos y estructurales de cada
  tipo —cobertura y estructura del bosque; hidroperiodo y turba del humedal; caudal ecológico y riberas
  del río; grado de calentamiento y saturación de aragonito del arrecife; materia orgánica y erosión del
  suelo; herbivoría y fuego de la pradera; criosfera y pisos altitudinales de la montaña; desertificación
  y agua subterránea de la zona árida; suelo cultivado y polinizadores del agroecosistema— pertenecen a
  los documentos **10 a 18** y **no se repiten aquí**. Aquí se fija **el instrumento común** y la
  **frontera** de lo que este documento hereda y lo que no.
- **No es una cifra nueva de biodiversidad.** Este documento **no inventa un índice**: ordena los que
  existen, verifica cuáles pueden ser piso y cuáles no, y **publica los que no pueden**.
- **No es el Índice Planeta Vivo (LPI).** El LPI es un indicador de **tendencia** y no tiene umbral: en
  §4.8 se demuestra con las tres limitaciones que declara su propia fuente por qué **no puede ser el
  Mínimo Absoluto** de nada.
- **No es el Marco Kunming-Montreal.** Sus metas cuantitativas —30×30, −50 % de invasoras, ×10 de
  extinción— son **POLÍTICA negociada**, no umbrales ecológicos derivados: entran en la columna del
  **Óptimo (votable)** y jamás en la del piso (§5.5).
- **No es el ISE.** El ISE es el **tablero**; esta dimensión es una de las piezas del **juez**. La
  relación entre ambos la fijó el [documento 07](07_Formula_de_violacion_y_pesos.md) §5.6 como una
  **equivalencia declarada con su límite escrito**, y este documento no la reabre.
- **No está implementado.** 🔴 No existe `SDV_E` en `maxocontracts/core/types.py`, no existe
  `sdv_e_validator.py`, no existe INV2-E y **no hay un solo sensor de biodiversidad integrado**. La
  tabla honesta está en §12.

**Las cuatro marcas de evidencia, y la quinta que es una respuesta.** `[VERIFICADO]` = comprobado con
herramienta en la sesión de fuentes de esta rama o leído en el archivo citado. `[REPORTADO]` = afirmado
por la fuente citada sin haber podido abrir el documento primario. `[HIPÓTESIS]` = inferencia razonada
del proyecto. `[ESTADO]` = valor observado del mundo, que **mide y no juzga**.
`[SIN FUENTE VERIFICADA — pendiente de consenso científico]` = se buscó el número y **no existe fuente
verificable**. En un documento de biodiversidad la quinta marca es el resultado más importante: **el
hallazgo central de esta dimensión es que el mínimo absoluto de riqueza de especies no existe** (§4.10 y
§13, pregunta 4), y decirlo vale más que rellenarlo.

---

## 2. Preámbulo metodológico

El SDV-H lo tiene y el SDV-S lo omitió; el brief prohíbe repetir la omisión. En una dimensión
**transversal** el preámbulo tiene una función añadida: una métrica de conjunto mal formada **no mide
peor, mide otra cosa**, y lo hace en silencio. Estas son las ocho reglas con las que se escribió lo que
sigue.

**Regla 1 — No confundir el estado del planeta con la condición de la unidad.** Las fronteras
planetarias (integridad de la biosfera: BII 90 %, tasa de extinción, HANPP) describen **el sistema
Tierra**; la unidad del SDV-E es una ocurrencia delimitada de niveles 4 a 6 de la Tipología Global de
Ecosistemas ([documento 02](02_Unidad_y_sujeto_del_SDV-E.md) §C2). Que la frontera esté transgredida
**no mide este humedal**; y que este humedal esté por debajo de su piso **no transgrede la frontera**.
El traslado de escala se hace **una vez**, se declara y se marca como propuesta no ratificada (§5.2 y
§13, preguntas 2 y 3).

**Regla 2 — Cuatro tipos de fila que NO son equivalentes.** Esta es la regla que evita repetir el error
del SDV-H (tomar el Óptimo del agua por el Mínimo Absoluto) a escala planetaria:

| Marca | Qué es | ¿Puede ser Mínimo Absoluto del SDV-E? |
|---|---|---|
| `[UMBRAL]` | Límite derivado de ciencia del sistema Tierra o de un estándar de la IUCN | **Sí** — candidato a LEY, no votable |
| `[META]` | Meta política negociada (Marco Kunming-Montreal) | **No sin decisión doctrinal explícita**: es POLÍTICA, votable |
| `[INDICADOR]` | Métrica oficial de seguimiento (0-1 o %) **sin umbral de violación incorporado** | Solo si se le fija un piso por consenso — y hoy **ese consenso no existe** |
| `[ESTADO]` | Valor observado del mundo: contexto, no umbral | **No**: mide, no juzga |

**Regla 3 — Mínimo Absoluto y Óptimo son dos columnas y dos regímenes jurídicos.** El piso es **LEY** y
**no se vota**; la plenitud aspiracional es **POLÍTICA** y **sí se vota** (precedente del Parlamento
Educativo, INV2-EDU: categoría `critical`, quórum 60 %, consenso 75 %, T13, anti-flip-flop 14 días,
`CHECK` en BD). En biodiversidad las dos columnas van separadas **incluso cuando el Óptimo está vacío**,
que es el caso de casi todas las filas de §4: *la ciencia publica pisos de riesgo, no plenitudes*
([documento 07](07_Formula_de_violacion_y_pesos.md) §4.3).

**Regla 4 — Toda métrica de biodiversidad verificada es relativa a una línea base o de riesgo. Ninguna
es absoluta.** El BII compara con *el mismo sitio sin uso humano del suelo*; el RLI y el RLIe son
índices de **riesgo** en escala 0-1; el RLE clasifica **riesgo de colapso**; el tamaño efectivo de
población (Ne) es un umbral **demográfico**. No existe —y se buscó— un umbral publicado de **riqueza de
especies mínima** para una unidad concreta. Consecuencia dura: **el SDV-E no puede exigir "un número
mínimo de especies"**, y cualquier documento que lo haga está inventando el número.

**Regla 5 — Composición y función son dos capas, y una puede mejorar mientras la otra cae.** El canon ya
lo fijó en la doctrina: *"el diseño es funcional antes que composicional"*, y por eso el indicador
funcional **HANPP** —apropiación humana de la producción primaria neta— entra *"como parámetro del mismo
rango que la biodiversidad composicional"* ([documento 01](01_Doctrina_SDV-E.md) §6.2). La evidencia
empírica está en esta misma biblioteca: en cumbres europeas la **riqueza específica aumenta** (+1 especie
cada 2 años por termofilización) **mientras las especies criófilas y los endemismos declinan**
([documento 16](16_Ecosistemas_Montanas_y_criosfera.md) §D5). Por tanto: **la riqueza específica no puede
ser piso ni cumplimiento**, y un aumento de riqueza sin dato del subconjunto que se pierde se declara
**NO CONCLUYENTE**, nunca cumplimiento.

**Regla 6 — El tiempo del territorio manda.** La biodiversidad se mide sobre horizontes **en TA (Tiempo
Absoluto)** —los que la propia fuente exige: **50 años** y **100 años** en los criterios de riesgo de
colapso, serie histórica **desde ~1750**— y **jamás en TVI ni TPI**. El **PIU** (Protocolo de
Intercambio Universal, Cap. 5 §5.5) es el **único** traductor, y la traducción ocurre **fuera** de esta
dimensión. La unidad del ciclo TA **no está decidida** y este documento **no la elige**
([documento 07](07_Formula_de_violacion_y_pesos.md) §5.4b; [documento 08](08_INV2-E_invariante.md) §6.2).

**Regla 7 — Sin dato no castiga, y sin dato tampoco aprueba.** Las coberturas reales son parciales y hay
que decirlo con la cifra delante: el **RLI cubre 5 grupos taxonómicos** (mamíferos, aves, anfibios,
corales y cícadas), el **LPI solo vertebrados**, y los **criterios de Áreas Clave para la Biodiversidad
excluyen explícitamente los microorganismos**. Un hueco de medición **no se convierte en violación** y
**no habilita un certificado de cumplimiento**: produce `indeterminado` y **bandera de opacidad
ecológica** ([documento 08](08_INV2-E_invariante.md) §8.4 y §6.3).

**Regla 8 — La Zona Libre también aquí.** La mayoría de la vida —microorganismos, hongos, casi todos los
invertebrados— **no la ve ninguna de las métricas verificadas de este documento**, y eso **no es un
defecto que se cierre con más índices**: es la parte inefable que el SDV-E deja **fuera de la fórmula**
(§10; [documento 04](04_Zona_Libre_del_Reino_Natural.md)). *"Medir todo sería la forma técnica de dejar
de escucharlo"* (Cap. 16.5 §16.5.14).

---

## 3. Pilares epistemológicos

Seis pilares sostienen esta dimensión. Los cinco primeros son heredados y se citan; el sexto es la
aportación estructural de este documento.

**Pilar 1 — La unidad es la del [documento 02](02_Unidad_y_sujeto_del_SDV-E.md), y la biodiversidad no
la redefine.** La unidad del SDV-E es una ocurrencia delimitada de **niveles 4 a 6** de la Tipología
Global de Ecosistemas, con **atribución obligatoria a un Grupo Funcional de Ecosistema (nivel 3)**; los
niveles 1-3 (reino, bioma funcional, EFG) están **vetados** como unidad de evaluación, y la cuenca es
**agrupación de coherencia hídrica**, nunca unidad medible ([documento 02](02_Unidad_y_sujeto_del_SDV-E.md)
§C2) —`[VERIFICADO]` **por el [documento 02](02_Unidad_y_sujeto_del_SDV-E.md)**, que declara haber leído
la fuente primaria (IUCN RLE Guidelines v2.0); **esta redacción no re-abrió ese PDF**—. Consecuencia
directa para este documento: **la métrica transversal debe funcionar en cualquier nivel 4-6**, y **no
puede depender de una lista de especies "correctas" por bioma** —porque el bioma no es la unidad—.

**Pilar 2 — El instrumento común existe, y son cuatro familias, no una.** Hay exactamente cuatro
familias de métricas verificadas que cumplen el requisito de ser **independientes del tipo de
ecosistema** (el mismo instrumento sirve en un humedal, un bosque, un río o un arrecife):

| Familia | Métrica | Qué mide | ¿Independiente del tipo? |
|---|---|---|---|
| **(a) Composición y abundancia relativas a línea base** | **BII** (Índice de Integridad Biótica) · intactitud (GLOBIO/MSA) | abundancia de especies del sitio contra **ese mismo sitio sin uso humano del suelo** | **Sí**: no necesita lista de especies por bioma |
| **(b) Riesgo, escala 0-1** | **RLI** (especies) · **RLIe** (ecosistemas) | riesgo agregado de extinción / de colapso | **Sí**: el RLI se desagrega a una unidad territorial por método formalizado |
| **(c) Sitio e irremplazabilidad** | **KBA** (11 criterios) · **STAR** (contribución) | si el sitio **ES / NO ES** insustituible; cuánto reduce riesgo una acción | **Sí**: los criterios KBA aplican a terrestre, dulceacuícola y marino |
| **(d) Genética** | **Ne > 500** (A.4) | pérdida de diversidad **dentro** de las especies, sin ADN | **Sí**: aplicable y desagregable a todos los países, grupos taxonómicos y ecosistemas |

**Pilar 3 — El andamiaje oficial ya está construido: cuatro indicadores principales cubren los tres
niveles de biodiversidad.** No hay que inventar el esqueleto; hay que **adoptarlo**. `[VERIFICADO]` en
las fichas de metadatos de UNEP-WCMC / CBD (2024):

| Nivel de biodiversidad | Indicador principal del Marco Kunming-Montreal | Qué mide | Familia |
|---|---|---|---|
| **Dentro de las especies** (genética) | **A.4** — proporción de poblaciones con **Ne > 500** | pérdida de diversidad genética **sin datos de ADN** (proxy demográfico) | (d) |
| **Entre especies** | **A.3** — **Red List Index** (RLI) | riesgo agregado de extinción; también indicador **ODS 15.5.1** | (b) |
| **Ecosistemas — condición** | **A.1** — **Lista Roja de Ecosistemas** (RLIe) | riesgo de **colapso** del ecosistema como tal | (b) |
| **Ecosistemas — extensión** | **A.2** — extensión de ecosistemas naturales | **superficie**, y **no** condición (lo dice la propia ficha) | contexto |

**Pilar 4 — La frontera planetaria es el contenedor, no el piso de la unidad.** La integridad de la
biosfera tiene **dos variables de control** —la **tasa de extinción** (diversidad genética) y la
**apropiación humana de la producción primaria neta** (integridad funcional)— y **las dos están
transgredidas** `[VERIFICADO]` (Stockholm Resilience Centre, 2026, leído en esta sesión). **Precisión
de lectura, porque el documento 08 §5.2 la da por verificada y aquí no se puede:** lo leído es el
porcentaje **actual** de HANPP (**30 %**) y el **hecho** de la transgresión —no la cifra de la
frontera ni su signo, que la biblioteca registra de dos maneras incompatibles (§13, pregunta 5)—. Eso obliga a
tratarlas como **dos parámetros separados** y a **no convertir el estado global en umbral local** sin
declararlo. La propia rama lo dejó escrito: **no existe reparto publicado del "presupuesto" planetario
por unidad** (`[SIN FUENTE VERIFICADA — pendiente de consenso científico]`; §13, pregunta 2).

**Pilar 5 — No compensación, y no sólo entre unidades: también entre métricas.** El BII, el RLI y el
RLIe **no son intercambiables entre sí**, y **la extensión no compensa la condición** —la ficha A.2 lo
dice literalmente: mide superficie, **no** condición (que es A.1)—. Sumar hectáreas protegidas a un BII
bajo sería **exactamente el error que INV2-E debe impedir** y la traducción métrica de *"el suelo antes
que el saldo"* (Cap. 16.5 §16.5.14).

**Pilar 6 (aportación de este documento) — La biodiversidad se mide por *lo que la unidad puede
sostener*, no por *lo que la unidad contiene*.** Una lista de especies presentes es un **inventario**, y
un inventario no tiene piso publicado (Regla 4). Lo que sí tiene piso o referencia publicada es
**cuánto se aparta la unidad de su propio estado de referencia** (BII), **cuánto riesgo acumula su
biota** (RLI), **cuánto riesgo acumula el ecosistema como tal** (RLIe/RLE), **si sus poblaciones
conservan tamaño suficiente para no perder diversidad** (Ne) y **si alberga atributos irremplazables**
(KBA). Las cinco preguntas son **contestables en cualquier tipo de ecosistema**, y ninguna exige saber
de antemano qué especies "debería" tener la unidad. `[HIPÓTESIS]` en su formulación; las cinco métricas
y sus escalas son `[VERIFICADO]` en las fuentes citadas en §4.

---

## 4. Dimensiones del SDV-E

### 4.0 El mapa: qué cubre el 0,300 y qué se le delega a los documentos 10-18

La dimensión transversal de biodiversidad **no sustituye** a las dimensiones por tipo: las **acompaña**.
La división de trabajo es explícita y verificable:

| Este documento (20) aporta | Los documentos 10-18 aportan |
|---|---|
| Los indicadores que funcionan en **cualquier unidad**: BII, RLI, RLIe/RLE, A.2, Ne > 500, KBA, STAR | Los **umbrales físicos, químicos y estructurales** propios de cada tipo (cobertura y estructura del bosque; hidroperiodo y turba; caudal ecológico y riberas; DHW y aragonito; materia orgánica y erosión; herbivoría y fuego; criosfera y pisos altitudinales; desertificación y agua subterránea; suelo cultivado y polinizadores) |
| El **puente de clasificación**: la Tipología Global de Ecosistemas (jerárquica: reinos → biomas → grupos funcionales), que permite aplicar **un mismo protocolo** a tipos distintos y después desagregar | La **adscripción de cada unidad concreta** a un tipo (o tipos) de la tipología, con su código de EFG |
| El **anclaje a la frontera planetaria** (BII, tasa de extinción, HANPP) y la declaración de lo que ese traslado de escala **no** autoriza | La **manifestación local** de ese anclaje en el tipo de ecosistema |

**Y una frontera que evita la doble contabilidad, dicha antes de las tablas.** El
[documento 07](07_Formula_de_violacion_y_pesos.md) §5.3 tiene **dos** dimensiones distintas que rozan la
biodiversidad: **Biodiversidad (0,300)** y **Especies clave (0,150)**, esta última con el piso *"ninguna
especie EX ni EW"* y un escalonado por proporción de especies CR y EN. Este documento **no invade esa
fila**:

- **Especies clave (0,150, [documento 07](07_Formula_de_violacion_y_pesos.md) fila 6)** — la lista corta
  de especies que la unidad declara clave, con sus categorías de la Lista Roja. Es **de la dimensión 6**.
- **Biodiversidad (0,300, este documento)** — la **comunidad biológica como conjunto**: integridad
  relativa (BII), riesgo agregado de extinción de **todas** las especies evaluadas con área de
  distribución en la unidad (RLI), riesgo de colapso del ecosistema (RLIe/RLE), diversidad genética
  (Ne > 500) y sitios insustituibles (KBA). **Ninguna de estas cinco se suma con la fila de especies
  clave del documento 07**: son dimensiones distintas con pesos distintos, y la agregación dentro de cada
  una es **por el peor caso**, nunca por suma ([documento 07](07_Formula_de_violacion_y_pesos.md) §5.1).

### 4.1 Dimensión B1: Integridad biótica relativa (el piso que compara la unidad consigo misma)

**Qué protege.** La **abundancia de especies** que la unidad sostiene hoy, comparada con la que
sostendría **ese mismo sitio sin uso humano del suelo**. No protege una lista de especies: protege la
**integridad** del ensamblaje.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **BII de la unidad** (Índice de Integridad Biótica, 0-100) | **≥ 90** — reducción máxima admisible del **10 %** respecto a la abundancia de especies en ausencia de uso humano del suelo. **LEY: no votable.** Candidato a piso, **no ratificado** | **100** — integridad prístina (valor del proyecto): **POLÍTICA, votable** | Newbold et al., 2016 (*Science*), comunicado de AAAS/EurekAlert `[VERIFICADO]` (contenido leído; HTTP 403 a clientes automáticos). Atribución del límite planetario: Steffen et al., 2015 `[REPORTADO]` |
| **Horquilla de reducción admisible según distintos autores** | El piso del SDV-E **no adopta la horquilla laxa**: la propia fuente dice *"(Some researchers say that reductions can safely be as much as a 70 %, however.)"*. Ese extremo se registra como **POLÍTICA (votable)**, no como piso | — | Newbold et al., 2016, cita literal `[VERIFICADO]` |
| **Cobertura del instrumento** | — | — | El BII se apoya en **2,3 millones de registros, más de 39.100 especies y 18.600 sitios** `[VERIFICADO]` |

**Justificación.** La cita de la fuente es literal y **contiene la tensión LEY/POLÍTICA dentro de una
misma frase** `[VERIFICADO]`: *"Generally, the safe limit is placed at a precautionary 10 % reduction in
BII, meaning that species abundance within a given habitat is 90 % of its original value in the absence
of human land use."* De ahí salen las dos columnas: **90 es el piso** (precautorio, no votable) y **la
horquilla 30-90 es el espacio de la plenitud** (votable). La misma fuente advierte que **9 de 14 biomas**
ya han rebasado el límite y que la afectación **varía por bioma** (pastizales los más afectados; tundra y
bosque boreal los menos) `[REPORTADO]` —es la fila 5 del informe de fuentes y está en el comunicado de
AAAS/EurekAlert, no en una página que esta herramienta pueda abrir: **la cita se sostiene sobre contenido
leído, no sobre una fuente verificable hoy**—: eso **justifica que la métrica sea transversal** y que los
parámetros por tipo vivan en los documentos 10-18.

**Y una frontera ecológica que el piso del BII no declara, y que aquí se declara por él.** El BII compara
la unidad contra *"ese mismo sitio sin uso humano del suelo"*, y **ese estado de referencia no es el mismo
para todos los tipos**: en un pastizal, en una sabana o en un agroecosistema extensivo, el **régimen de
herbivoría y de fuego forma parte del estado de referencia** y no de su degradación. Un BII tomado contra
la clausura (el sitio cercado y sin herbívoros) **mide la ausencia del proceso, no la pérdida de
integridad**, y produce exactamente el sesgo que este documento prohíbe en §4.9 al revés: **premiar el
monocultivo leñoso y castigar el pastizal**. El instrumento no trae esa declaración; el protocolo la
exige: **la línea base de referencia y el régimen de perturbación que la define son campos obligatorios
del dato**, y su ausencia hace el BII **no medido**, nunca `cumple`.

**Protocolo.** El BII es un **índice modelado**, y eso hay que decirlo con la misma claridad con que se
dice su cifra: se calcula a partir de datos de uso del suelo y de modelos de respuesta de la
biodiversidad al uso del suelo, no de un censo del sitio. Consecuencias operativas, todas obligatorias:

1. **Se declara la versión del modelo y la capa de uso del suelo** como parte del dato (T13,
   [documento 06](06_Medicion_y_verificacion_T13.md) §6.3 y §7.2). Un BII sin versión de modelo no es
   auditable.
2. **Se mide sobre el polígono declarado de la unidad** ([documento 02](02_Unidad_y_sujeto_del_SDV-E.md)
   §C1), no sobre una cuadrícula global recortada a ojo.
3. **La ventana temporal la fija la fuente** ([documento 06](06_Medicion_y_verificacion_T13.md) §6.4b):
   el BII es un índice de **estado con horizonte largo**, no una serie sub-anual; declarar una frecuencia
   más fina que la del modelo **es inventar el dato**.
4. **Sin modelo aplicado a la unidad, el parámetro está NO MEDIDO** (`None`): no se imputa violación y
   **no se declara cumplimiento** ([documento 08](08_INV2-E_invariante.md) P5).

**Violación.** Un **BII medido < 90** en el polígono declarado, con **versión de modelo, capa de uso del
suelo, ventana en TA y evidencia_ref** declaradas. Es un hecho medido con unidad, ventana y fuente —no
una apreciación—. Dos precisiones que impiden el fraude en las dos direcciones:

- **Un BII de 89,9 no es «casi» 90**: es violación, y la banda de severidad la fija el déficit
  normalizado `(90 − 89,9)/90 = 0,0011` ([documento 07](07_Formula_de_violacion_y_pesos.md) §3.2), que
  en el motor cae en `minor`. **La magnitud es pequeña; el hecho es un hecho.**
- **El excedente sobre 90 no es crédito**: es **margen**. Un BII de 96 **no** genera «des-daño»
  acumulable ni se descuenta contra ninguna otra dimensión ([documento 07](07_Formula_de_violacion_y_pesos.md)
  §3.2; la asimetría es la misma que el motor aplica a `v_ucv`).

> **Propuesta no ratificada, y su límite.** El **90 % se publicó como límite planetario propuesto**
> (integridad de la biosfera a escala global) y aplicarlo a un humedal concreto es un **traslado de
> escala** que este documento hace **porque el [documento 07](07_Formula_de_violacion_y_pesos.md) §4.1 ya
> lo fijó como el parámetro de la dimensión**, y del que **no existe confirmación publicada**
> (§13, preguntas 2 y 3). La alternativa verificada —los criterios del RLE— mide **riesgo de colapso**,
> no integridad, y por eso **no se funde con esta fila**: se propone como **la segunda capa** de la misma
> dimensión (§4.4 y §5.3).

### 4.2 Dimensión B2: Tasa de extinción (la variable de control que no tiene piso numérico legible)

**Qué protege.** La **velocidad** a la que la unidad —y el sistema del que forma parte— pierde especies.
Es la variable de control de **diversidad genética** de la frontera de integridad de la biosfera.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **Tasa de extinción de la unidad** (E/MSY: extinciones por millón de especies-año) | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` **para el valor numérico**. La cifra que circula (**< 10 E/MSY**, con zona de incertidumbre 10-100) **no se pudo leer en página de organismo legible**: `science.org` responde **403** y el artículo es PDF/HTML no accesible a la herramienta (Steffen et al., 2015). **No se adopta como piso desde aquí** | **reducción ×10 para 2050** — **POLÍTICA, votable** (`[META]`) | CBD, Objetivo A del Marco Kunming-Montreal (Decisión 15/4, 2022) `[VERIFICADO]` |
| **Estado de la frontera** (dato duro, no umbral) | **Transgredida en sus dos variables de control** | No transgredida | Stockholm Resilience Centre, 2026 `[VERIFICADO: leído en esta sesión]` |
| **Tasa de extinción observada** (global) | — | — | **> 100 E/MSY** `[VERIFICADO: leído en esta sesión, texto literal: "species are going extinct at an alarming rate of above 100 extinctions per million species years"]` |
| **Tasa de extinción frente al promedio de los últimos 10 millones de años** | — | — | *"at least tens to hundreds of times higher than the average over the past 10 million years, and the rate is increasing"* — CBD, notas de orientación de la Meta 4 `[VERIFICADO]` |
| **Tasa actual frente a la tasa de fondo** | — | — | hasta ≈**100 ×** la tasa de fondo (estimación deliberadamente conservadora; vertebrados) — Ceballos et al., 2015 (*Science Advances*) `[REPORTADO]` (comunicado leído; artículo no abierto) |
| **Extinción local de una especie clave de la unidad** | **0 extinciones locales** (EX/EW) — **hecho binario, LEY: no votable** | 0 | [documento 07](07_Formula_de_violacion_y_pesos.md) §4.1 fila 6 (categorías IUCN); el propio canon: *"Ecosistemas con derecho a existir"* (Cap. 10 §10.3) |
| **Especies amenazadas en la Lista Roja** (contexto) | — | 0 | **> 42.100** especies — CBD, notas de la Meta 4 `[VERIFICADO]`; **≈1.000.000** estimadas (25 % de media en los grupos evaluados; **10 %** para insectos, deliberadamente conservador; base: 8,1 M de especies animales y vegetales estimadas, 1,7 M descritas) — IPBES, 2019 `[VERIFICADO]` |
| **HANPP — apropiación humana de la NPP** (2.ª variable de control) | `[SIN FUENTE VERIFICADA]` **para la cifra de frontera**; **la biblioteca registra dos cifras incompatibles** y este documento **no elige** (§13, pregunta 5) | **nada verificado**: lo único que existe es la **base preindustrial 1,9 %** `[REPORTADO]` por el [documento 01](01_Doctrina_SDV-E.md) §6.2, que en esa misma línea registra una frontera **< 10 %** —y el [documento 03](03_No_colonizacion_del_TA.md) §14.1 registra **> 90 %**—. **Ninguna de las dos fronteras se verificó**, y la base preindustrial **no es un Óptimo: es el estado de referencia** | **30 %** de la energía disponible de la naturaleza `[VERIFICADO: leído en esta sesión]` — Stockholm Resilience Centre, 2026 |

**Justificación, y es una justificación de una ausencia.** El estado de la frontera **sí está
verificado**; el **número del piso no**. Este documento **se niega a escribir `< 10 E/MSY` como si lo
hubiera leído**: en la página del organismo que sí respondió (200) el texto dice **> 100 E/MSY** y **no
publica el valor de la frontera**; en la fuente primaria que lo publica (Steffen et al., 2015) la
herramienta recibe **403**. La biblioteca lo registra por dos vías indirectas —el
[documento 04](04_Zona_Libre_del_Reino_Natural.md) **anexo de referencias** lo anota como *"frontera
< 10 E/MSY"* atribuido a esa misma página del organismo, y el
[documento 03](03_No_colonizacion_del_TA.md) §14.1 lo registra vía el informe CERAC (2024)—, y las dos
vías son **`[REPORTADO]`** y **de segunda mano**: el informe de fuentes de esta rama declara que la
cifra de la frontera **no se verificó**, y la página leída en esta sesión **no la publica**.
La regla del brief es explícita y manda más que la comodidad: **si no se verificó, no se cita la cifra
como piso**. Y hay una segunda razón, aritmética: **10 E/MSY es una tasa global**; nada publicado
—`[SIN FUENTE VERIFICADA]`— permite repartirla entre unidades.

**Protocolo.** El instrumento del piso **no es la tasa global**: es la **extinción local documentada**
de una especie de la unidad (hecho binario, linaje **E** de comunidad testigo + **C** de bioindicadores,
[documento 06](06_Medicion_y_verificacion_T13.md) §6.1), y **el RLI**, que es la vía por la que el
riesgo de extinción **sí se desagrega a una unidad concreta** (§4.3). La tasa global entra al tablero
como **contexto** ([ESTADO]) y como **contenedor** de la frontera, jamás como umbral de la unidad.

**Violación.** Dos hechos, uno binario y uno medido:

1. **Extinción local documentada** (categoría EX o EW) de una especie de la unidad, **atribuible** al
   ciclo TA evaluado: **violación binaria**, no graduable, y **no compensable** con ninguna otra
   dimensión (incluido el crédito regenerativo: §9). **Precisión de contabilidad que evita leer doble el
   mismo hecho:** este piso es el de la dimensión **Especies clave (0,150)** del
   [documento 07](07_Formula_de_violacion_y_pesos.md) fila 6; se enuncia aquí porque es el único hecho de
   extinción **local y verificable** de la dimensión transversal, y **no añade un segundo peso sobre el
   mismo hecho** (§4.0 y §4.10).
2. **Empeoramiento del RLI de la unidad** por debajo de su propio piso operativo (§4.3), cuando ese piso
   se ratifique.

Y una precisión que impide el fraude más fácil de esta fila: **una especie que desaparece de la lista de
la unidad porque nadie la buscó no es una extinción ni un cumplimiento**: es **cobertura faltante**
([documento 08](08_INV2-E_invariante.md) P5 y P11).

### 4.3 Dimensión B3: Riesgo agregado de extinción (el RLI, y por qué es la respuesta operativa)

**Qué protege.** El **riesgo agregado de extinción** de todas las especies evaluadas cuya área de
distribución cae dentro de la unidad. No protege a una especie: protege la **composición** frente a la
pérdida.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **RLI de la unidad** (0-1) | `[SIN FUENTE VERIFICADA]`: **no existe piso numérico publicado para el RLI de una unidad**. Piso operativo **propuesto** (**PROPUESTA NO RATIFICADA** `[HIPÓTESIS]`): *ninguna especie EX ni EW atribuible a la unidad en el ciclo TA* — binaria, coherente con el [documento 07](07_Formula_de_violacion_y_pesos.md) §4.1 fila 6 | **1,0** — todas las especies en *Preocupación menor* (LC) | Escala, pesos y método: CBD / UNEP-WCMC, indicador principal **A.3** (basado en Butchart et al., 2024) `[VERIFICADO]` |
| **Método de desagregación a una unidad territorial** | — | — | *"each species contributing to the index is weighted by the proportion of its global range within the particular country or region"* — ficha A.3 `[VERIFICADO]` |
| **Escala y convención** (para poder auditar el cálculo) | — | — | pesos oficiales **CR = 4 · EN = 3 · VU = 2 · NT = 1 · LC = 0 · EX/EW = 5**; `RLI = 1 − Σ(s·Wc)/(WEX·N)`; **0 = todas extintas · 1 = todas LC**; también **ODS 15.5.1** `[VERIFICADO]` |
| **Cobertura taxonómica del instrumento** (límite de fiabilidad) | — | — | **mamíferos, aves, anfibios, corales y cícadas**; serie **1980-2023** `[VERIFICADO]` |
| **Valor global vigente del RLI** | — | — | **no publicado en la ficha consultada**: la metodología, los pesos y la serie sí; el valor vigente, no. `[SIN FUENTE VERIFICADA]` |

**Justificación, y es la más importante de este documento.** El RLI es **la respuesta operativa a la
pregunta central** —*¿cómo se mide la biodiversidad de una unidad concreta sin depender del tipo de
ecosistema?*— porque **su desagregación territorial está formalizada por el propio marco oficial**: cada
especie se pondera por la **proporción de su área de distribución global que cae dentro de la unidad**
`[VERIFICADO]`. Eso significa tres cosas que ninguna otra métrica verificada ofrece a la vez:

1. **Sirve en cualquier tipo de ecosistema** y en los tres reinos de la tipología (terrestre,
   dulceacuícola, marino), porque no depende del hábitat sino de **las especies y su distribución**.
2. **No exige una lista de especies "correctas"**: usa las evaluaciones que ya existen y las pondera por
   presencia relativa.
3. **Es la métrica que responde a la objeción del [documento 12](12_Ecosistemas_Rios_y_cuencas.md)**
   —*un río concreto no tiene BII propio*—: un río **sí** puede tener un RLI desagregado por proporción
   de área de distribución de sus especies acuáticas evaluadas, **siempre que existan evaluaciones de
   esos grupos** —y ahí está su límite: los grupos cubiertos son cinco y **ninguno es un pez**—.

**Protocolo.** Fuente: las evaluaciones de la Lista Roja **a través de la ficha oficial del indicador
A.3** —no raspando el sitio de la Lista Roja, que **bloquea a los agentes automáticos (403)** y por
tanto **no es auditable por la comunidad testigo de forma directa** (§7)—. El cálculo declara: (a) la
unidad y su polígono; (b) **la lista de especies evaluadas con área de distribución en la unidad y la
proporción usada para cada una**; (c) la versión de la serie; (d) la ventana en **TA**. Frecuencia: la de
la **revisión de las evaluaciones** de las especies incluidas, no la del gusto del observador
([documento 06](06_Medicion_y_verificacion_T13.md) §6.4b: la frecuencia no puede ser mayor que el tiempo
de respuesta del indicador).

**Violación.** Tres hechos, y **solo el primero es hoy declarable**:

1. **Extinción local (EX/EW) de una especie con área de distribución en la unidad**, atribuible al ciclo
   TA: binaria, no graduable (§4.2, hecho 1).
2. **Deterioro del RLI de la unidad entre dos mediciones comparables** (misma unidad, misma lista de
   especies, misma metodología) **sin recuperación posterior**: violación **de tendencia**; su umbral
   numérico **no está publicado** y por eso **hoy no fija magnitud** — fija **escalada** por el contador
   de ciclos consecutivos ([documento 08](08_INV2-E_invariante.md) §8.6).
3. **RLI de la unidad por debajo de un piso votado** (categoría `critical`), cuando la deliberación lo
   fije: **POLÍTICA, votable** — y no puede modificarse mientras exista una violación abierta.

### 4.4 Dimensión B4: Riesgo de colapso del ecosistema (la Lista Roja de Ecosistemas, el único estándar que juzga al ecosistema como tal)

**Qué protege.** La **condición del ecosistema como sujeto**: no el riesgo de sus especies, sino el
riesgo de que **el ensamblaje completo colapse**.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **Categoría RLE de la unidad** | **mejor que VU**: VU, EN y CR son las tres categorías **amenazadas** y **CO** es el **colapso** —las cuatro quedan del lado del riesgo—. Coherente con el [documento 08](08_INV2-E_invariante.md) §4.1, que fija `rle_categoria` como **ordinal, binaria y sin peso** | **LC** (Preocupación menor) | IUCN, Lista Roja de Ecosistemas (IUCN-CEM) `[VERIFICADO]` |
| **Criterios y categorías** | — | — | **5 criterios**: (A) reducción de la distribución geográfica · (B) distribución restringida · (C) degradación ambiental · (D) disrupción de procesos bióticos o interacciones · (E) análisis cuantitativo de la probabilidad de colapso. **8 categorías**: CR, EN, VU, NT, LC, DD, NE y **CO (Colapso)**, análoga a «Extinto» `[VERIFICADO]` |
| **RLIe — Índice de la Lista Roja de Ecosistemas** (0-1) | `[SIN FUENTE VERIFICADA]`: la ficha da la escala (**0 = todos los ecosistemas colapsados · 1 = ninguno amenazado**) y **no** un piso de unidad | **1,0** | CBD / UNEP-WCMC, indicador principal **A.1** (Rowland et al., 2020) `[VERIFICADO]` |
| **Candidato a violación a escala de ecosistema** | **CR + CO** — **PROPUESTA NO RATIFICADA** `[HIPÓTESIS]` de este documento | LC | Inferencia sobre las categorías verificadas de la IUCN |
| **Extensión de ecosistemas naturales** (A.2) | **no es un piso**: mide **superficie, no condición** (lo dice su propia ficha) | aumentar sustancialmente para 2050 (`[META]`, votable) | CBD / UNEP-WCMC, indicador **A.2** (marco SEEA-EA) `[VERIFICADO]` |

**Justificación.** La RLE fue **adoptada por la IUCN en 2014** y es *"the global standard for assessing
risk of ecosystem collapse for terrestrial, freshwater and marine ecosystems"*: es **el único estándar
verificado que evalúa al ecosistema como sujeto**, no a sus especies. Su estructura es **idéntica en
espíritu a la Lista Roja de especies** —criterios, categorías y una categoría terminal (**CO = Colapso**)
que sustituye a «Extinto»—, y por eso es la pieza que el canon necesita cuando dice que un ecosistema
*"tiene derecho a existir"* (Cap. 10 §10.3). Su criterio **D** (disrupción de procesos bióticos) y su
criterio **B** son **independientes del tipo de ecosistema**: aplican a un humedal, a un arrecife o a una
pradera con la misma lógica. Y hay una razón de arquitectura: el [documento 08](08_INV2-E_invariante.md)
§4.1 **ya usa los criterios A-E del RLE como los cinco parámetros de biodiversidad de su catálogo
ejecutable** (`rle_reduccion_distribucion_50a`, `rle_reduccion_historica_1750`, `rle_eoo_km2`,
`rle_degradacion_c1_pct`, `rle_probabilidad_colapso`), y **advierte en el mismo lugar** que *"los
criterios A-E miden riesgo de colapso, no «área mínima para biodiversidad viable»"*. Este documento
**asume esa advertencia y la convierte en arquitectura**: el RLE es la **capa de condición** de la
biodiversidad; el BII (§4.1) es la **capa de integridad**; **no son la misma medida y no se funden en
una sola cifra** (§5.3).

**Protocolo.** Evaluación con el estándar RLE, con **horizontes explícitos que la fuente fija y el
proyecto no elige**: **50 años** (criterios A y E), **100 años** (E) y serie histórica **desde
aproximadamente 1750** (A3) —[documento 08](08_INV2-E_invariante.md) §6.2 `[VERIFICADO]`—. Instrumentos:
teledetección de cobertura + inventarios + modelización de riesgo (linajes **A**, **B** y **E**,
[documento 06](06_Medicion_y_verificacion_T13.md) §6.1); **quien reporta es la ciencia y la entidad
evaluadora**, no el guardián. Declaración obligatoria de: versión del estándar, criterios activados,
categoría resultante y `evidencia_ref`.

**Violación.** **Categoría CR o CO** en la unidad (hecho binario, veto no graduable: `[HIPÓTESIS]` de
este documento, sobre un estándar verificado y una categoría verificada), y **categoría VU o peor** como
piso declarado por el [documento 08](08_INV2-E_invariante.md) §4.1. Dos precisiones que impiden leer de
más:

- **`DD` (Datos Insuficientes) y `NE` (No Evaluado) no son cumplimiento**: son **cobertura faltante**
  ([documento 08](08_INV2-E_invariante.md) P5).
- **La categoría es un estado, no un déficit**: entra como **dimensión binaria/ordinal** y **no se
  promedia** con las demás ([documento 07](07_Formula_de_violacion_y_pesos.md) §4.4). Un ecosistema CO
  **no se compensa** con un BII alto en el resto del polígono.

### 4.5 Dimensión B5: Diversidad genética (el piso más barato de medir y el menos usado)

**Qué protege.** La **variabilidad dentro de las especies**: la capacidad de una población de no perder
diversidad génica por tamaño reducido. Es la primera de las dos variables de control de la frontera de
integridad de la biosfera y la única de esta dimensión cuyo piso es **un número redondo, publicado y
auditable sin laboratorio**.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **Tamaño efectivo de población (Ne) de las poblaciones de la unidad** | **Ne > 500** (≈ 5.000 individuos censados) — por debajo, las poblaciones *"are highly susceptible to rapid loss of genetic diversity and are at high risk of extinction due to genetic threats"*. **LEY: no votable**, candidato a piso | **Ne ≫ 500** (riesgo de pérdida de diversidad ≈ 0) | CBD / UNEP-WCMC, indicador principal **A.4** del marco de seguimiento del GBF (metadatos actualizados 2024-08-01) `[VERIFICADO]` |
| **Aplicabilidad y desagregación del instrumento** | — | — | La ficha declara el indicador *"applicable and relevant in all countries, taxonomic groups, and ecosystems (and can be desagregated to these levels)"* y que **funciona sin secuenciación de ADN** `[VERIFICADO]` |
| **Diversidad de recursos genéticos domesticados** | `[SIN FUENTE VERIFICADA]` como piso; **estado**: **> 2.400 razas en riesgo de extinción y 600 ya extintas** `[REPORTADO]`; **≈ 8.800 razas registradas de 38 especies y > 15.000 poblaciones nacionales en 182 países** `[VERIFICADO]` | 0 razas en riesgo | FAO, **DAD-IS** — pertenece al [documento 18](18_Ecosistemas_Agroecosistemas.md) y a la frontera humano-natural |
| **Cifra «90 % de diversidad genética» atribuida al GBF** | **NO entra al SDV-E**: **no está en el texto adoptado**. El Objetivo A dice solo *"the genetic diversity … is maintained"*: **sin cifra** | — | CBD, Objetivo A (Decisión 15/4, 2022) `[VERIFICADO]`; el «90 %» proviene de borradores previos (`[SIN FUENTE VERIFICADA]`) |

**Justificación.** Es el parámetro de biodiversidad con **mejor relación entre solidez de la fuente y
coste de la medición**: el umbral es **redondo (500)**, **aplicable a cualquier especie y ecosistema**,
**desagregable** y **no exige ADN** —la ficha oficial lo dice—, lo que responde directamente al requisito
de **gobernanza operacionalmente finita** (Cap. 10 §10.7). Y hay una razón doctrinal: la diversidad
genética es la variable que **la propia frontera planetaria nombra como su primera variable de control**,
y su estado global está **transgredido** `[VERIFICADO]`. Un estándar que midiera biodiversidad sin medir
genética estaría midiendo el nivel «entre especies» y **dejando fuera un nivel entero** que el andamiaje
oficial ya cubre con un indicador principal.

**Protocolo.** Se mide **por población**, no por unidad: la unidad declara **qué poblaciones** de qué
especies se evalúan (las mismas especies clave del [documento 07](07_Formula_de_violacion_y_pesos.md)
fila 6, más las poblaciones que el diseño biológico de la unidad declare relevantes), y de cada una se
reporta **Ne** o, en su defecto, el **proxy demográfico y geográfico** que la ficha admite. Datos:
censos, conteos con protocolo, ciencia ciudadana validada (linajes **C** y **D**,
[documento 06](06_Medicion_y_verificacion_T13.md) §6.1); frecuencia: la del ciclo reproductivo de la
especie evaluada, declarada en TA —**no** la del calendario del municipio—.

**Violación.** **Ne ≤ 500** en una población evaluada de la unidad, con censo o proxy declarado y
`evidencia_ref`. Y dos casos que **no** son violación: (a) una población **no evaluada** —es cobertura
faltante—; (b) una población de una especie **no residente** que atraviesa la unidad: el indicador mide
**poblaciones**, y atribuirle a la unidad el Ne de una población migratoria sería el abuso de escala que
la Regla 1 prohíbe.

> **Hueco declarado, y es importante.** El indicador oficial mide **la proporción de poblaciones con
> Ne > 500**. Este documento **no encuentra** —y buscó— una regla publicada que diga **qué proporción de
> poblaciones debe cumplir** para que la unidad cumpla. La consecuencia es la de siempre, y se declara en
> lugar de resolverse con un número inventado: **el piso opera población a población** (una población
> bajo 500 es una violación atómica, P1 del [documento 08](08_INV2-E_invariante.md) §8.3), y **la
> proporción agregada es un indicador de tablero, no un piso** (§13, pregunta 11).

### 4.6 Dimensión B6: Sitios insustituibles (la dimensión binaria sin peso)

**Qué protege.** Lo que **no se puede recuperar en otro lugar**: los atributos por los que un sitio es
**irremplazable** para la biodiversidad. Es un **juicio binario auditable** —el sitio **ES / NO ES** Área
Clave para la Biodiversidad— y por eso entra como **dimensión binaria sin peso**, siguiendo el precedente
canónico de las dimensiones VIII y IX del SDV-H (Cap. 8 §8.11) y la decisión que ya tomaron los
documentos [04](04_Zona_Libre_del_Reino_Natural.md) y [09](09_Comparativa_inter_reinos.md) §10.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **Criterios de Área Clave para la Biodiversidad (KBA)** | **11 criterios en 5 categorías**: (A) biodiversidad amenazada · (B) biodiversidad geográficamente restringida · (C) integridad ecológica · (D) procesos biológicos · (E) irremplazabilidad. **Aplican a ambientes terrestres, dulceacuícolas y marinos** | — | KBA Partnership / IUCN, *Global Standard for the Identification of Key Biodiversity Areas* (2016) `[VERIFICADO]` |
| **Efecto de una evaluación completa** (magnitud del instrumento) | — | — | En los países con evaluación completa, el área KBA **más que se duplicó** de media `[VERIFICADO]` |
| **STAR — contribución a reducir el riesgo de extinción** | **no es piso**: es la métrica de **acción**, y alimenta **R** (§9) | sin máximo; no tiene techo | IUCN, 2024 — ejemplos verificados: **65,8** (total RCA), **48,4** (Douala-Edea), **13,8** (Mukagodo), **8,9** (Mount Kulal), **2,9** (Mbalmayo), **1,2** (Waza y Tana) `[VERIFICADO]` |

**Justificación.** Es el complemento exacto de las métricas de estado: el BII y el RLI dicen **cómo está**
la biodiversidad; los criterios KBA dicen **si hay algo que, si se pierde, no vuelve a aparecer en
ningún otro sitio**. Y su forma —un juicio binario con carga de prueba— es la que el canon ya usa para lo
inconmensurable, de modo que **no hay que inventar figura jurídica**: se aplica la de las dimensiones
binarias sin peso. Los criterios, además, son **los únicos de esta dimensión que se declaran aplicables
en los tres reinos** de la tipología (terrestre, dulceacuícola y marino) con el mismo estándar.

**Protocolo.** Evaluación de sitio con el estándar KBA (linaje **E**: comunidad testigo + datos abiertos,
con carga de prueba, [documento 06](06_Medicion_y_verificacion_T13.md) §6.1), declarando: criterio(s)
activado(s), umbral de la categoría usada y `evidencia_ref`. Frecuencia: la de la revisión del estándar
y de la evaluación de sitio; **no** la del reporte anual.

**Violación.** **Pérdida de los atributos por los que el sitio calificó como KBA**, con evaluación de
sitio que lo documente: **hecho binario, no graduable, no cuantificable y no canjeable**. Se registra,
**bloquea** (propiedad P1 del [documento 08](08_INV2-E_invariante.md) §8.3) y **no se promedia**.

> **Dos advertencias que pertenecen a esta fila y evitarían un abuso real.** (a) El
> [documento 04](04_Zona_Libre_del_Reino_Natural.md) §14 registra, como `[REPORTADO]` y leído en la
> indexación de la fuente, que el criterio de la tipología IUCN exige que un sitio contenga el **100 %
> de la extensión del ecosistema** y **≥ 10 % de la población global** de la especie: esas cifras **no se
> adoptan aquí como umbral** porque su fuente primaria es un PDF que la herramienta no lee y este
> documento no las verifica. (b) **Un KBA no es un área protegida**: el primero es un juicio sobre
> irremplazabilidad; la segunda es una figura de gestión. Confundirlos produciría la compensación que §9
> prohíbe.

### 4.7 El índice de la Lista Roja de Ecosistemas (RLIe) y la extensión (A.2): el par que no se funde

Ya están en la tabla de §4.4, y merecen un párrafo propio porque su confusión es **el error más fácil de
esta dimensión**: **A.1 mide condición; A.2 mide extensión**, y la ficha oficial de A.2 lo dice
literalmente —*"no mide condición (eso es A.1)"*— `[VERIFICADO]`. La consecuencia operativa es una regla
del estándar:

> **Sumar superficie a un déficit de condición está prohibido.** Un proyecto que añade 200 hectáreas
> «de biodiversidad» a una unidad cuyo RLIe está en EN **no ha mejorado la condición de la unidad**: ha
> cambiado la extensión de otra cosa. Es la traducción métrica exacta de *"el suelo antes que el saldo"*
> y la razón por la que **A.2 no tiene peso en `PESOS_PISO`**.

### 4.8 El LPI: indicador de tendencia, y por qué NO puede ser el piso

El **Índice Planeta Vivo** es la métrica de biodiversidad más citada del mundo y **no puede ser el
Mínimo Absoluto de esta dimensión**. La razón no es una opinión de este documento: son **tres límites que
declara su propia fuente** `[VERIFICADO]`.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **LPI global** (tendencia de vertebrados 1970-2020) | **NO es piso.** Es `[INDICADOR]`: **−73 %** de abundancia media. Su valor 0 (estable) es **referencia de tendencia**, no umbral de violación | **0** (estable) | WWF / ZSL, *Living Planet Report 2024*, sitio oficial del índice `[VERIFICADO]` |
| **LPI de agua dulce y desagregación regional** | **NO es piso** | — | **−85 %** (agua dulce); **−95 %** (Latinoamérica y Caribe); **−76 %** (África); rango por regiones IPBES **35-95 %** `[VERIFICADO]` |
| **Cobertura del dato** (límite de fiabilidad) | — | — | **34.836 poblaciones de 5.495 especies** en el LPR 2024; base total **≈ 42.000 poblaciones de 5.579 especies**; **solo vertebrados** `[VERIFICADO]` |

**Las tres razones, en el orden en que la fuente las declara:**

1. **Solo vertebrados** (mamíferos, aves, peces, reptiles y anfibios): nada de insectos, plantas, hongos
   ni microorganismos. Un piso construido sobre el LPI **dejaría fuera a la mayor parte de la vida** y
   —peor— **premiaría** la pérdida de lo que no ve (§10).
2. **Es la media de las tendencias poblacionales**, no una abundancia total: **una media de declives no
   es un declive del conjunto**. Y una media, como enseñó el ejemplo del
   [documento 07](07_Formula_de_violacion_y_pesos.md) §5.9, **diluye exactamente el daño concentrado**
   que el estándar existe para atrapar.
3. **El resultado publicado usa un subconjunto** de la base (34.836 de ≈ 42.000 poblaciones): la cifra
   es un dato con **cobertura declarada**, no un censo.

**Para qué SÍ sirve, y es mucho.** El CBD lo empareja con el RLI en su propia ficha: el RLI *"is
complemented by indicators of population abundance, such as the Wild Bird Index or Living Planet
Index"* `[VERIFICADO]`. En el SDV-E entra como **indicador de tablero y de tendencia**, con una función
concreta y honesta: **detectar que la unidad se mueve en la dirección equivocada antes de que su piso se
cruce**, y alimentar la **banda de aviso previo** del [documento 08](08_INV2-E_invariante.md) §5.4. Un
LPI que cae **no declara violación**; **obliga a instrumentar y a re-declarar la línea base**.

### 4.9 La riqueza específica: la única métrica que este documento prohíbe expresamente

**No entra al piso, no entra al tablero como medidor de estado y no puede declarar cumplimiento.** No es
una preferencia: es la consecuencia de la Regla 5 y del hallazgo del
[documento 16](16_Ecosistemas_Montanas_y_criosfera.md) §D5 —en cumbres europeas la **riqueza aumenta**
(+1 especie cada 2 años por termofilización) **mientras las especies criófilas y los endemismos
declinan**—. Un estándar que premiara el aumento de riqueza estaría **pagando la destrucción del piso con
la llegada de sus sustitutos**. Y hay una segunda razón, independiente: **no existe umbral publicado de
riqueza mínima** para una unidad (`[SIN FUENTE VERIFICADA — pendiente de consenso científico]`).

Lo que sí puede registrarse, sin peso y sin veredicto: **la composición como inventario declarado**
(qué se observó, con qué esfuerzo y en qué ventana), y **el subconjunto que se pierde** —criófilas,
endémicas, especialistas— **medido aparte y siempre**. La separación **no es un análisis posterior: es la
condición de validez del indicador**.

### 4.10 Tabla de conjunto: qué es piso, qué es tablero y qué es política

Esta tabla es el resumen ejecutivo de la dimensión y **la que debe leerse antes que cualquier otra**.
`PESOS_PISO` es el vector que entra en el cálculo de la violación; `PESOS_TABLERO` el que publica la
fotografía completa ([documento 07](07_Formula_de_violacion_y_pesos.md) §5.3).

| # | Parámetro transversal | Naturaleza | Operador | ¿Peso en el piso? | Fuente |
|---|---|---|---|---|---|
| B1 | **BII de la unidad** | `[UMBRAL]` — **piso 90** | `min` | **sí** — **los 0,300 completos mientras no se ratifique el reparto interno de §5.3** ([documento 07](07_Formula_de_violacion_y_pesos.md) §5.3) | Newbold et al., 2016 `[VERIFICADO]`; Steffen et al., 2015 `[REPORTADO]` |
| B2 | **Extinción local EX/EW** | `[UMBRAL]` binario — **piso 0** | `binary` | **sí** — pero **solo por la vía de la dimensión de especies clave (0,150)**: esta tabla **no le añade un segundo peso** ([documento 07](07_Formula_de_violacion_y_pesos.md) §4.1) | [documento 07](07_Formula_de_violacion_y_pesos.md) §4.1; IUCN v3.1 `[REPORTADO]` |
| B2b | **Tasa de extinción (E/MSY)** | `[ESTADO]` global + piso **no verificado** | — | **no** (global, sin método de reparto por unidad) | SRC, 2026 `[VERIFICADO]`; `< 10 E/MSY` `[REPORTADO]` |
| B2c | **HANPP** | `[ESTADO]` global + **contradicción interna** de la biblioteca | — | **no** (§13, pregunta 5) | SRC, 2026 `[VERIFICADO]` (30 %) |
| B3 | **RLI de la unidad** | `[INDICADOR]` 0-1, desagregable | `ordinal`/`min` | **no hoy**: piso operativo **propuesto**, no ratificado | CBD/UNEP-WCMC A.3 `[VERIFICADO]` |
| B4 | **Categoría RLE de la unidad** | `[UMBRAL]` ordinal — **mejor que VU** | `ordinal` | **no** (binaria sin peso, [documento 08](08_INV2-E_invariante.md) §4.1) | IUCN RLE `[VERIFICADO]` |
| B4b | **RLIe de la unidad** | `[INDICADOR]` 0-1 | — | **no** | CBD/UNEP-WCMC A.1 `[VERIFICADO]` |
| B5 | **Ne > 500 por población** | `[UMBRAL]` — **piso 500** | `min` | **sí** — **0,300 mientras no se ratifique el reparto interno**; con el reparto de §5.3, **0,045** | CBD/UNEP-WCMC A.4 `[VERIFICADO]` |
| B6 | **Sitio KBA** | `[UMBRAL]` **binario** | `binary` | **no** (dimensión binaria sin peso) | KBA Partnership / IUCN, 2016 `[VERIFICADO]` |
| — | **Extensión de ecosistemas naturales (A.2)** | `[INDICADOR]` de superficie | — | **no**, y **prohibido** usarlo como compensación | CBD/UNEP-WCMC A.2 `[VERIFICADO]` |
| — | **LPI (y LPI de agua dulce)** | `[INDICADOR]` de tendencia | — | **no** | WWF/ZSL, 2024 `[VERIFICADO]` |
| — | **STAR** | `[INDICADOR]` de acción | — | **no** en el piso; **sí** en **R** (§9) | IUCN, 2024 `[VERIFICADO]` |
| — | **Cobertura 30×30 (Meta 3)** | `[META]` — **POLÍTICA, votable** | — | **no**: §5.5 | CBD, 2022 `[VERIFICADO]`; cobertura real **17,58 %**, Protected Planet, 2026 `[VERIFICADO]` |
| — | **Riqueza específica** | **prohibida** como piso y como cumplimiento | — | **no**: §4.9 | [documento 16](16_Ecosistemas_Montanas_y_criosfera.md) §D5 |
| — | **Microorganismos, hongos, invertebrados** | **Zona Libre**: binaria sin peso | `binary` | **no**: §10 | [documento 04](04_Zona_Libre_del_Reino_Natural.md) |

**Lo que esta tabla dice sin adornos:** de **quince filas**, **cinco** son `[UMBRAL]` —BII 90, extinción
local EX/EW, Ne > 500, categoría RLE mejor que VU y sitio KBA—, pero **solo tres de ellas llevan peso en
`PESOS_PISO`** (BII 90 dentro del 0,300; la extinción local EX/EW a través de la dimensión de especies
clave, 0,150; y Ne > 500 dentro del 0,300): la **categoría RLE** y el **sitio KBA** **bloquean sin
pesar**, porque son ordinales o binarios (Cap. 8 §8.11). **Dos** filas son `[ESTADO]` global —la tasa de
extinción observada (**> 100 E/MSY**), cuyo **piso numérico no se verifica**, y el HANPP—, **cinco** son
indicadores sin piso (RLI, RLIe, extensión A.2, LPI y STAR), **una** es una meta política (30×30),
**una** es una prohibición expresa (riqueza específica) y **una** es la Zona Libre. **Ese reparto es el
resultado del documento**, no su antesala. **Y la aritmética de la quinta columna tiene una trampa que
esta tabla no puede resolver sola:** los tres "sí" **no suman 0,300 + 0,150 + 0,300**. Mientras el
reparto interno de §5.3 no se ratifique, B1 y B5 son **el mismo 0,300 leído dos veces** y la dimensión
solo puede computar uno —la agregación es por el peor caso (§5.3), no por suma—; con el reparto
ratificado, B1 vale 0,150 y B5 vale 0,045 **dentro** de ese 0,300, y el 0,150 de B2 sigue siendo el de
la dimensión 6 del [documento 07](07_Formula_de_violacion_y_pesos.md), **no un peso añadido a este**.

---

## 5. Fórmula de violación, pesos y umbrales

La fórmula del SDV-E pertenece al [documento 07](07_Formula_de_violacion_y_pesos.md); este documento
**no la toca**. Lo que hace aquí es declarar **cómo entra la biodiversidad** en ella, sin cambiar un solo
peso declarado.

### 5.1 El peso 0,300 no se mueve

| Dimensión | `PESOS_TABLERO` | ¿Tiene piso? | `PESOS_PISO` |
|---|---|---|---|
| **Biodiversidad** (esta dimensión) | **0,300** | 🟢 sí (BII 90 %) | **0,300** |

Cifra y vectores son los del [documento 07](07_Formula_de_violacion_y_pesos.md) §5.3, con su origen
declarado —los pesos del ISE **son internos del proyecto, no un estándar externo**, y los 0,300 de
biodiversidad conservan la jerarquía que el ISE ya declaraba: **el doble del suelo (0,150)**—.
`[SIN FUENTE VERIFICADA — pendiente de consenso científico]` **para el peso**: **ningún organismo
publica pesos porcentuales para biodiversidad, agua, aire, suelo, especies clave, caudal y conectividad**.
Ratificarlos es **POLÍTICA (votable)**, no investigación. Y se recuerda la discrepancia declarada de la
biblioteca: el [documento 07](07_Formula_de_violacion_y_pesos.md) §5.3 publica **0,905** de cobertura del
piso sobre su catálogo y el [documento 08](08_INV2-E_invariante.md) §5.2 publica **0,680** sobre el suyo;
**este documento no resuelve esa disputa y no la usa**: la fila de biodiversidad vale **0,300 en los dos**,
y es lo único que esta dimensión necesita de esa tabla (§13, pregunta 14).

### 5.2 El traslado de escala, declarado como lo que es

El **90 % del BII** es un **límite planetario propuesto** para la integridad de la biosfera a escala
global. Aplicarlo a una unidad concreta es un **traslado de escala** que el
[documento 07](07_Formula_de_violacion_y_pesos.md) §4.1 ya hizo y que su §13 (pregunta 7) declaró
**discutible**. Este documento **no lo repite en silencio y no lo mejora con un número inventado**:

- **Lo que sí puede hacerse, y se hace:** aplicar el 90 % **al polígono declarado de la unidad**, con la
  versión del modelo y la capa de uso del suelo declaradas (§4.1, Protocolo), y **publicar** que el
  traslado es una decisión del proyecto.
- **Lo que no existe:** un **método publicado de reparto del presupuesto planetario por unidad**
  (`[SIN FUENTE VERIFICADA — pendiente de consenso científico]`). Las dos vías que este documento
  propone —**área ponderada por rareza** y **uso del RLI desagregado por proporción de área de
  distribución** (§4.3, esta última **con método oficial verificado**)— quedan como **PROPUESTA NO
  RATIFICADA** y como pregunta abierta (§13, preguntas 2 y 3).

### 5.3 Cómo se agrega dentro de la dimensión (y las dos capas que no se funden)

Se hereda **íntegra** la regla de agregación del [documento 07](07_Formula_de_violacion_y_pesos.md) §5.1:

> **`A_k = max_i D_i` sobre los parámetros medidos de la dimensión `k`. Nunca `Σ D_i`.**

Y con ella, la **prohibición de doble contabilidad**: dos parámetros que miden el mismo fenómeno **no se
suman ni se promedian**; se elige el pertinente y se declara cuál. Aplicado a esta dimensión:

| Pieza | Cómo entra | Por qué |
|---|---|---|
| **Integridad (BII)** | déficit con operador `min`: `D = max(0, (90 − actual)/90)` | es la capa de **abundancia relativa**; piso con fuente |
| **Genética (Ne)** | déficit con operador `min` sobre cada población evaluada; el peor caso manda | es un piso **atómico por población** (P1) |
| **Colapso (RLE)** | **estado**, no déficit: categoría ordinal que **bloquea** sin promediarse | el [documento 07](07_Formula_de_violacion_y_pesos.md) §4.4 y el [documento 08](08_INV2-E_invariante.md) §4.1 ya lo fijaron binario/ordinal **sin peso** —**y ahí es donde el reparto interno de §5.3 choca con los dos**, cosa que se declara allí y no se disimula aquí— |
| **Riesgo de especies (RLI)** | **indicador de tablero**; sube al piso **solo** si se ratifica un piso operativo | hoy no tiene umbral publicado |
| **KBA y Zona Libre** | **binarias sin peso**: bloquean o se documentan, no se cuantifican | Cap. 8 §8.11 |

**Y la fusión que este documento propone, marcada como lo que es.** El
[documento 07](07_Formula_de_violacion_y_pesos.md) §4.1 mide biodiversidad **con el BII**; el
[documento 08](08_INV2-E_invariante.md) §4.1 la mide **con los cinco criterios del RLE**. **Las dos
cosas no son la misma** y este documento **no las trata como sinónimos ni elige una en silencio**:

> **PROPUESTA NO RATIFICADA `[HIPÓTESIS]`:** la dimensión de biodiversidad tiene **dos capas
> complementarias** —**integridad** (BII, §4.1) y **riesgo de colapso** (RLE, §4.4)— que **alimentan la
> misma dimensión de 0,300** y se agregan **por el peor caso medido**, no por suma. Bajo esa lectura, el
> catálogo del [documento 08](08_INV2-E_invariante.md) y la fila 1 del
> [documento 07](07_Formula_de_violacion_y_pesos.md) **dejan de ser dos verdades distintas** y pasan a ser
> **dos capas de la misma**: abundancia relativa y riesgo de colapso. La agregación por `max` garantiza
> que **no hay doble contabilidad** (no se suman) y que **el peor de los dos gobierna** (no se diluyen).
> Ratificar esta lectura —o decidir que la dimensión se mide con **una sola** de las dos— corresponde a
> la **revisión de coherencia de la biblioteca**, no a este documento (§13, pregunta 12).

**Reparto interno del 0,300, si se ratifica la fusión (PROPUESTA NO RATIFICADA).** La tabla siguiente
**no cambia el 0,300**: lo reparte **dentro** de la dimensión, y se publica para que la deliberación
tenga algo concreto que votar en lugar de una abstracción. **Y hay que decir contra qué choca, porque
choca:** el [documento 08](08_INV2-E_invariante.md) §5.2 **ya asigna 0,30 a "Biodiversidad · riesgo de
colapso (5 criterios RLE)"** y su §4.1 marca la fila `rle_categoria` como **`ordinal`, binaria y SIN
PESO**; el [documento 16](16_Ecosistemas_Montanas_y_criosfera.md) §5.4 da **0,10** a su dimensión de
comunidad criófila y endémica. Este reparto **no es compatible con ninguna de esas tres cosas a la vez**,
y por eso va donde va: en la revisión de coherencia, no aquí.

| Parámetro transversal | Peso interno propuesto | Origen del número |
|---|---|---|
| **BII de la unidad** (§4.1) | **0,150** | mitad de la dimensión: es la capa de integridad y la única con piso global publicado |
| **Categoría RLE / riesgo de colapso** (§4.4) | **0,075** | un cuarto: es la capa de condición del ecosistema como sujeto. **Contradice al [documento 08](08_INV2-E_invariante.md) §4.1**, que la declara binaria **sin peso**; si esa lectura se ratifica, estas 0,075 se retiran y se reasignan o se devuelven al BII |
| **Ne > 500** (§4.5) | **0,045** | el nivel genético, con piso redondo y medición barata |
| **RLI de la unidad** (§4.3) | **0,030** | el nivel entre especies, sin piso publicado: pesa poco porque **medir lo que no tiene umbral no puede diluir a lo que sí lo tiene** |
| **Suma** | **0,300** | **coincide exactamente con el peso que el [documento 07](07_Formula_de_violacion_y_pesos.md) §5.3 fija para la dimensión** |

`[SIN FUENTE VERIFICADA — pendiente de consenso científico]` **para el reparto**: no existe organismo que
publique cómo se reparte el peso de la biodiversidad entre integridad, riesgo, genética y composición.
**Si la revisión de coherencia decide que la dimensión se mide solo con el BII —que es lo que el
[documento 07](07_Formula_de_violacion_y_pesos.md) §4.1 ya dice—, el reparto no aplica y la fila BII toma
los 0,300 completos.** Las dos lecturas son compatibles con la aritmética del estándar; la diferencia es
una decisión doctrinal y por eso se vota, no se deduce. **Lo que no es compatible es el estado actual de
§4.10, donde B1 y B5 declaran cada uno "los 0,300": mientras esta tabla no se ratifique, los dos valores
son el mismo peso visto dos veces y la dimensión no puede computar los dos.**

### 5.4 El Óptimo de esta dimensión: casi todo vacío, y por la misma razón de siempre

De las quince filas de §4.10, **el Óptimo está vacío en casi todas** y las que lo tienen lo tienen por
**construcción del proyecto** (integridad prístina = 100; ninguna especie amenazada; ninguna población
bajo 500; ningún tipo de ecosistema amenazado). Los **únicos números aspiracionales con fuente
verificada** de esta dimensión son **políticos** y son **anclas de política global**, no óptimos de una
unidad concreta:

| Meta | Cifra verificada | Naturaleza |
|---|---|---|
| Objetivo A (2050) | **reducir ×10** la tasa y el riesgo de extinción; **mantener** la diversidad genética (sin cifra) | **META — POLÍTICA** |
| Meta 1 (2030) | pérdida de áreas de alta importancia para la biodiversidad *"close to zero"* | **META — POLÍTICA** |
| Meta 2 (2030) | **≥ 30 %** de los ecosistemas degradados bajo restauración efectiva | **META — POLÍTICA** |
| Meta 3 (2030) | **≥ 30 %** de terrestre, aguas continentales y marino-costero conservado (30×30) | **META — POLÍTICA** |
| Meta 6 (2030) | **−50 %** en las tasas de introducción y establecimiento de invasoras | **META — POLÍTICA** |
| Meta 7 (2030) | **−50 %** de nutrientes excedentes y **−50 %** de riesgo de plaguicidas | **META — POLÍTICA** |

Usarlas como *"el óptimo de este humedal"* sería **abuso de la fuente**
([documento 08](08_INV2-E_invariante.md) §4.1). Su lugar es la **columna votable** y el tablero.

### 5.5 El caso 30×30, con bisturí: por qué la cobertura NO puede ser el piso

Es la cifra de biodiversidad que más se cita y la que más fácil se usaría mal. Los tres datos, juntos,
lo demuestran `[VERIFICADO]`:

1. **La meta es ≥ 30 % para 2030** (CBD, Meta 3, Decisión 15/4) — **es POLÍTICA negociada, no un umbral
   ecológico derivado**.
2. **La cobertura real es 17,58 % global** (protegidas + OECM; **489.023** áreas protegidas y **7.510**
   OECM, Protected Planet, 2026). Es un **dato de esfuerzo**, no de resultado.
3. **Una hectárea protegida no dice nada de su condición**, y la propia ficha del indicador A.2 lo
   advierte: extensión **no** es condición.

> **Regla de este documento:** la cobertura de conservación es **indicador de esfuerzo y de política**,
> entra al **tablero** con **cero peso en `PESOS_PISO`**, y **jamás** puede cruzar el piso de ninguna
> dimensión —ni compensar un BII bajo, ni un RLE en CR—. *"El suelo antes que el saldo"* (Cap. 16.5
> §16.5.14).

### 5.6 La escala de lectura: la del [documento 07](07_Formula_de_violacion_y_pesos.md), sin añadidos

Este documento **no añade bandas**. Rige la escala de severidad del motor (`minor` ≤ 10 %, `moderate`
≤ 30 %, `severe` > 30 %) y la **prelación del piso sobre la banda**
([documento 07](07_Formula_de_violacion_y_pesos.md) §5.7): si un solo parámetro de biodiversidad está
bajo su piso —o una dimensión binaria está violada—, **la unidad tiene violación declarada** con
independencia de la banda del compuesto. La lección que el [documento 07](07_Formula_de_violacion_y_pesos.md)
§5.9 sacó de su propio ejemplo vale doble aquí: **una media ponderada puede llamar «Declinando» a un
humedal con tres especies en peligro**, y por eso la media **no decide**.

---

## 6. Protocolo de medición (sensores, frecuencias, quién reporta)

El elenco de sensores pertenece al [documento 06](06_Medicion_y_verificacion_T13.md); **no se repite
aquí**. Lo que esta dimensión declara es **qué linaje sostiene cada parámetro** y **qué límite físico
tiene cada uno**, porque en biodiversidad la mayor parte de los parámetros **no se miden con un sensor
propio: se heredan de un índice calculado por un tercero**.

### 6.1 Qué linaje sostiene cada parámetro transversal

| Parámetro | Linaje primario ([documento 06](06_Medicion_y_verificacion_T13.md) §6.1) | Quién reporta | Límite que hay que declarar |
|---|---|---|---|
| **BII** (§4.1) | **A** (teledetección de uso y cobertura) + **modelo** de respuesta de la biodiversidad | entidad modeladora + ciencia | es un **modelo**, no un censo: sin versión declarada no es auditable |
| **Tasa de extinción** (§4.2) | **E** (datos abiertos y series de terceros) | organismos de síntesis | es **global**: no se desagrega a una unidad con método verificado |
| **EX/EW local** (§4.2) | **C** (bioindicadores) + **D** (ciencia ciudadana con validación) + **E** (comunidad testigo, con carga de prueba) | observadores con protocolo + testigos | exige **esfuerzo de muestreo declarado**: sin él, la ausencia no es dato |
| **RLI** (§4.3) | **E** (ficha oficial del indicador y evaluaciones de tercero) | CBD / UNEP-WCMC + evaluadores | **5 grupos taxonómicos**; el sitio de la Lista Roja **bloquea agentes automáticos (403)** |
| **RLE / RLIe** (§4.4) | **A** + **B** + **E** | ciencia + entidad evaluadora | horizontes de **50 y 100 años** y serie **desde ~1750**: **no hay lectura anual de colapso** |
| **Ne > 500** (§4.5) | **C** y **D** (censos y proxies) | observadores con protocolo | es **por población**; la agregación a la unidad no tiene regla publicada |
| **KBA** (§4.6) | **E** (juicio de sitio con carga de prueba) | KBA Partnership / evaluadores | es **binario**: o el sitio califica, o no |
| **LPI** (§4.8) | **E** (serie publicada) | WWF / ZSL | **solo vertebrados**; **media de tendencias**; subconjunto de la base |
| **Cobertura 30×30 / A.2** (§4.7 y §5.5) | **A** + **E** (registros oficiales) | Protected Planet / UNEP-WCMC | **extensión, no condición** |

### 6.2 Frecuencia: la fija la fuente, y en biodiversidad eso significa «lento»

Rige el principio del [documento 06](06_Medicion_y_verificacion_T13.md) §6.4b: *la frecuencia de medición
no puede ser mayor que la resolución temporal del sensor que la sostiene, ni mayor que el tiempo de
respuesta del propio indicador*. Traducido a esta dimensión, con las ventanas que las fuentes fijan:

| Parámetro | Ventana / horizonte de la fuente | Declarar una frecuencia más fina es… |
|---|---|---|
| Categoría RLE | **50 años**, **100 años**, serie **desde ~1750** `[VERIFICADO]` | inventar el dato |
| RLI | serie **1980-2023**, actualizada con las revisiones de evaluación `[VERIFICADO]` | inventar el dato |
| BII | índice de **estado con horizonte largo**; se recalcula con el modelo y la capa de uso del suelo | inventar el dato |
| Ne | el **ciclo reproductivo** de la especie evaluada, declarado en TA | forzar el calendario del municipio al ciclo de la especie |
| Cobertura (30×30 / A.2) | **anual** a la escala de los registros oficiales | sobre-interpretar una serie administrativa |

**Y una consecuencia de costo que el estándar debe decir en voz alta:** prometer monitoreo de
biodiversidad **más fino que el tiempo de respuesta del indicador** garantiza incumplimiento por diseño y
**convierte el costo del monitoreo en coartada**. Un bioindicador no se mide semanalmente.

### 6.3 Quién reporta: el guardián consiente, no mide

Regla dura, heredada y no negociable: *el guardián oráculo consiente, no mide*
([documento 08](08_INV2-E_invariante.md) §6.1; `app/contracts_bp.py`). En esta dimensión tiene un filo
propio, porque **casi todos sus parámetros vienen de índices calculados por terceros**:

1. **La fuente del índice** (modelo BII, ficha A.3, ficha A.1, evaluación RLE, censo de Ne) es la que
   reporta el **valor**; su versión y su `evidencia_ref` son **campos obligatorios** del dato.
2. **La comunidad de custodia y la ciencia** (linaje E) reportan la **declaración**: línea base,
   polígono, lista de especies evaluadas y proporción de área usada en el RLI, esfuerzo de muestreo.
3. **El guardián `eco-`** puede **consentir o negar** un contrato; **no puede** aportar el valor de un
   parámetro. Si el único respaldo de un número es la firma del guardián, el parámetro está
   **`sin_evidencia`** y el estado es **`indeterminado`** ([documento 08](08_INV2-E_invariante.md) §8.4).

### 6.4 Admisibilidad: los cuatro campos, y uno más para biodiversidad

Una medición de biodiversidad entra al cálculo **solo si** trae `valor` + `unidad`, `ta_periodo` (inicio
y fin en **TA**), `fuente_dato` y `evidencia_ref` ([documento 08](08_INV2-E_invariante.md) §6.1). Esta
dimensión **añade un quinto campo obligatorio**, porque sin él el número es incomparable consigo mismo:

> **`metodo_version`** — la versión del índice o del estándar con que se calculó (versión del modelo BII;
> versión de la serie del RLI; versión del estándar RLE; edición del estándar KBA). **Dos BII de la misma
> unidad calculados con versiones distintas no son comparables**, y una serie que los una sería una serie
> falsa. `[HIPÓTESIS]` en su obligatoriedad; el principio es T13 (trazabilidad).

### 6.5 Sin dato no castiga, sin dato no aprueba, y la cobertura se publica

Las coberturas reales de esta dimensión son **parciales por diseño** y se declaran con su cifra:
**5 grupos taxonómicos** en el RLI, **solo vertebrados** en el LPI, **microorganismos excluidos** de los
criterios KBA. Por tanto: un parámetro no medido **no imputa déficit** (`None ≠ 0`), **no produce
`FE = 1,0` certificado** y **no exime de la ley**
([documento 07](07_Formula_de_violacion_y_pesos.md) §2, Regla 7). El resultado es el estado
**`indeterminado`** con **bandera de opacidad ecológica** y **obligación de instrumentar**
([documento 08](08_INV2-E_invariante.md) §6.3): no es una sanción al territorio, es una **condición de
validez** para quien quiere operar sobre él.

**El estado por defecto de esta dimensión, hoy, es `indeterminado`.** No es una hipérbole: sin fuentes de
datos ecológicos integradas (§12), **ninguna unidad puede cubrir sus parámetros de biodiversidad** —ni,
en consecuencia, **generar crédito regenerativo utilizable**—.

---

## 7. Verificación y auditoría (T13, guardián, comunidad testigo)

### 7.1 Qué se puede auditar de una métrica heredada

En biodiversidad el auditor **no puede re-medir**: puede **reconstruir el cálculo**. Eso cambia la forma
de la auditoría y hay que decirlo con precisión.

| Auditable | Cómo |
|---|---|
| Que el índice sea **el que dice ser** | `metodo_version` + `fuente_dato` + `evidencia_ref` (§6.4) |
| Que la **unidad** del cálculo sea la declarada | polígono, nivel 4-6 de la tipología y código de EFG ([documento 02](02_Unidad_y_sujeto_del_SDV-E.md) §C1 y §C2) |
| Que la **lista de especies y las proporciones** del RLI sean las declaradas | la ficha A.3 fija el método: cada especie ponderada por la proporción de su área de distribución dentro de la unidad `[VERIFICADO]` |
| Que **ninguna dimensión sin piso** tenga peso | comprobación por código contra el catálogo ([documento 08](08_INV2-E_invariante.md) W1 y P5) |
| Que el **crédito regenerativo** no altere el veredicto | propiedad P3 del [documento 08](08_INV2-E_invariante.md): `v` no tiene término `R` |
| Que la **cobertura** se publique y no se disfrace | P11: dos `v` iguales con cobertura distinta **no son equivalentes** |
| Que el **registro no se borre** | `_validation_log`, `get_validation_log()` y `to_dict()`, patrón ya implementado en el motor `[VERIFICADO]` |

### 7.2 El problema de auditoría propio de esta dimensión: las fuentes que bloquean a los testigos

**Aquí hay un hallazgo que hay que publicar y no maquillar.** La comunidad testigo —el sustituto
institucional del par auditor que el Reino Natural no tiene ([documento 09](09_Comparativa_inter_reinos.md)
§7, insight I3)— **no puede verificar directamente las fuentes primarias de esta dimensión**:

- **`iucnredlist.org` responde 403** a los agentes automáticos (y es la fuente primaria de las
  categorías de especies y de la RLE).
- **`gbif.org` responde 403** (es el agregador mundial de biodiversidad:
  [documento 06](06_Medicion_y_verificacion_T13.md) §13, punto 11, ya lo declaró).
- La fuente primaria del **piso del BII** (`science.org`) responde **403**: el umbral se sostiene sobre
  el **comunicado institucional** que sí se pudo leer `[VERIFICADO]` y sobre la **atribución registrada**
  del límite planetario `[REPORTADO]`.

**Consecuencia operativa, y es una regla de esta dimensión —con su límite, que es grande—.** La
auditoría de biodiversidad se hace **contra la ficha oficial del indicador y contra los registros
publicados** (A.1-A.4 del marco de seguimiento, series abiertas, evaluaciones publicadas), **no contra el
sitio de la Lista Roja raspado por un bot** —que además está prohibido por sus términos de uso—. **Y ese
sustituto desbloquea mucho menos de lo que promete:** la ficha del indicador es **metodología, escala y
serie**, y **no contiene el valor de la unidad**; el valor de la unidad exige la evaluación de cada
especie, que vive en el dominio bloqueado. La auditoría de esta dimensión es, por tanto, **de segunda
mano declarada**, y así hay que publicarla. Toda medición cuyo `evidencia_ref` sea un sitio que bloquea a
los auditores se marca **`evidencia_no_reproducible_por_testigo = True`** y **no puede sostener una
violación persistente** que escale a retractación ([documento 08](08_INV2-E_invariante.md) §8.6).
`[HIPÓTESIS]` en su forma exacta; el principio es T13. **Cuando una fuente primaria bloqueada sea el
único respaldo de un piso —es el caso del BII con `science.org`—, la consecuencia no puede ser auditar de
oído: es `indeterminado` con bandera de opacidad, y así queda dicho (§4.1 y §4.2).**

### 7.3 Riesgos abiertos que afectan a esta dimensión

| ID | Riesgo (`docs/architecture/blindaje_anti_gamificacion_equidad.md`) | Efecto concreto sobre biodiversidad |
|---|---|---|
| **R4** | **Partes fantasma**: cualquier usuario autenticado crea un `eco-*` y queda como su dueño, sin verificar autoridad sobre la entidad | Un actor sin autoridad puede **declarar la línea base** de la unidad —y con ella, el BII de referencia y el esfuerzo de muestreo—. La métrica **no lo detecta**: detecta el número, no la legitimidad |
| **R6** | T9 (Reciprocidad Justa) no se valida en la creación: pasa un contrato 100 % unilateral | Se puede degradar la biodiversidad de una unidad **sin contraprestación** y sin que nada bloquee |
| **R13** | Guardián `eco-` con heurística laxa: sin `DEEPSEEK_API_KEY` aprueba si los invariantes pasan | **El piso no se delega al guardián**: un guardián laxo puede consentir de más, **no puede fabricar un BII de 95** ni un Ne > 500. Su consentimiento **relaja, no habilita** ([documento 08](08_INV2-E_invariante.md) §7.3) |

Y un riesgo **propio de esta dimensión**, que no está en el registro del repositorio y este documento
añade como propuesta de registro `[HIPÓTESIS]`:

| ID | Riesgo | Por qué es específico de la biodiversidad |
|---|---|---|
| **R17** (propuesto) | **Optimización de la línea base**: el BII se mide **contra el mismo sitio sin uso humano del suelo**, y el RLE contra horizontes de 50 y 100 años. Un operador puede **redeclarar la unidad** (recortar el polígono, excluir el parche degradado) y mejorar el índice **sin tocar el ecosistema** | Es el fraude de límites: la métrica transversal depende de un polígono, y el polígono lo declara alguien. La defensa no es métrica sino de gobernanza: **el polígono y su justificación son parte del registro auditable** y su cambio **re-dispara la declaración de línea base** ([documento 02](02_Unidad_y_sujeto_del_SDV-E.md) §C4) |

---

## 8. Invariante INV2-E: de estándar a contrato ejecutable

La especificación de INV2-E es el [documento 08](08_INV2-E_invariante.md). Aquí se declara **qué recibe
INV2-E de esta dimensión**, parámetro por parámetro, para que la interfaz sea verificable.

### 8.1 Lo que esta dimensión entrega al invariante

| Pieza que INV2-E consume | Parámetro | Operador | ¿Puede bloquear hoy? |
|---|---|---|---|
| Piso de integridad | **BII ≥ 90** | `min` | 🟢 **sí** (piso con fuente leída) |
| Piso genético | **Ne > 500** por población evaluada | `min` | 🟢 **sí** (piso con fuente verificada) |
| Hecho binario de pérdida | **EX/EW local documentada** | `binary` | 🟢 **sí** (P1) |
| Estado de condición | **Categoría RLE** (VU o peor; CR/CO como veto propuesto) | `ordinal` | 🟢 **sí**, como estado binario sin peso |
| Indicador sin piso | **RLI de la unidad** | `ordinal` | 🔴 **no** hoy: registro + escalada por tendencia |
| Indicador sin piso | **RLIe, extensión (A.2), LPI** | — | 🔴 **no**: tablero |
| Binaria sin peso | **KBA** | `binary` | 🟢 **sí**, bloquea sin cuantificarse |
| Zona Libre | **microorganismos, hongos, invertebrados** | `binary` | 🟢 **sí**, se documenta; **nunca** pondera |
| Crédito | **STAR** | — | alimenta **R**; **jamás** levanta un bloqueo (§9) |

### 8.2 Las propiedades del [documento 08](08_INV2-E_invariante.md) aplicadas a esta dimensión

| Propiedad | Cómo se lee en biodiversidad |
|---|---|
| **P1 Atomicidad** | **una** población con Ne ≤ 500, o **una** especie EX local, o **un** BII medido < 90 **invalidan el cumplimiento**. No hay «compensación interna» entre parámetros de la dimensión |
| **P3 Independencia del saldo** | plantar árboles, restaurar un margen o financiar un proyecto STAR **no cambia el veredicto** del BII ni del RLE |
| **P4 Guard por tipo, no por dato** | `applicable=False` **solo** si el participante no es unidad ecológica. Que falte el BII **no** hace inaplicable el estándar: lo hace `indeterminado` |
| **P5 Sin dato no castiga y no aprueba** | una unidad **sin ninguna** métrica de biodiversidad **no** es una unidad conforme: es `indeterminado` con bandera de opacidad |
| **P7 Finitud** | ningún campo de esta dimensión admite `inf` ni `NaN`: una tasa de extinción, un BII o un Ne son números finitos; lo «infinito» es **estado** (`precautionary_block`) |
| **P8 No colonización del TA** | todos los horizontes de esta dimensión se declaran en **TA** (50 años, 100 años, desde ~1750, ciclo reproductivo declarado); **ninguna** magnitud en TVI ni TPI; la conversión, **solo por el PIU** y fuera del invariante |
| **P9 Independencia del ISE** | el veredicto **no** depende del ISE ni de sus dos escaleras en conflicto: el ISE es tablero |
| **P10 Monotonía** | si el BII baja, el RLI empeora o aparece una EX local, `v` **no puede** disminuir |
| **P11 Cobertura declarada** | el resultado publica qué parámetros de biodiversidad se midieron y cuáles no; **`indeterminado` (0 de 4) no es «cumple» (4 de 4)** |
| **P12 La Zona Libre no pondera** | la vida no medida (§10) entra como dimensión binaria **sin peso** y su violación se documenta |

### 8.3 Los dos bloqueos, en el lenguaje de esta dimensión

El [documento 08](08_INV2-E_invariante.md) §8.5 fija **dos vías**. Aplicadas aquí:

- **Bloqueo por piso** — hay violación **medida**: BII < 90, Ne ≤ 500, EX/EW local, categoría RLE
  VU o peor, o KBA perdido. Consecuencia: `should_block_action = True`.
- **Bloqueo precautorio (T14)** — **no hay piso medido** para una dimensión afectada **y** la acción
  propuesta es **irreversible**. Es la vía que cubre el hueco real de esta dimensión: **una unidad sin
  BII y sin RLE no puede autorizar a ciegas** una pérdida de cobertura, un drenaje o una extracción
  hídrica, porque **T14 pone la carga de la prueba en quien propone** (Cap. 5). Aquí el invariante no
  necesita una cifra para proteger: necesita la **irreversibilidad**.

### 8.4 El aporte de esta dimensión al invariante: `metodo_version` y el fraude de límites

Dos campos que INV2-E **no tiene hoy** en su especificación y que esta dimensión obliga a añadir
(`[HIPÓTESIS]`, propuesta de este documento):

1. **`metodo_version`** por medición (§6.4): sin él, dos mediciones de la misma unidad **no son
   comparables** y una serie temporal puede fabricarse sin tocar un solo dato.
2. **`poligono_ref` + `poligono_hash`**: la unidad de biodiversidad **es un polígono** y el polígono lo
   declara alguien (R17, §7.3). Su cambio es un **acto registrado** que re-dispara la línea base, no un
   ajuste silencioso. Es la aplicación de T13 a esta dimensión: *la contabilidad nunca se borra*, y
   recortar el mapa **es** una forma de borrarla.

---

## 9. El suelo antes que el saldo (no compensación)

La regla es canónica y esta dimensión es donde se pone a prueba: *"Un conjunto con crédito regenerativo
acumulado pero humedal bajo su SDV-E no está en coherencia: **INV2-E será su juez**"* (Cap. 16.5
§16.5.14).

**Cómo se garantiza formalmente, en biodiversidad.** El crédito regenerativo vive en el componente **R**
del VHV, que **sí** admite negativos (EVV-1.2 §4.3), implementado y probado con `r_units = -12.0`
`[VERIFICADO]` en `app/micromax.py` y `tests/test_micromax.py`. La fórmula del
[documento 07](07_Formula_de_violacion_y_pesos.md) §5 **no tiene término `R`**, de modo que la
propiedad F8/P3 **no es un acuerdo de caballeros: es que la variable no existe en la expresión**. Un
crédito de −12,0 R o de −12.000 R produce el mismo `v` y el mismo veredicto.

**Y aquí está la tentación específica de esta dimensión, que hay que nombrar porque es la más elegante
de todas: compensar biodiversidad con biodiversidad.** Restaurar un manglar, financiar un proyecto STAR,
sembrar un corredor, sumar hectáreas protegidas. El estándar lo resuelve con cuatro reglas duras:

| Intento de compensación | Respuesta del SDV-E |
|---|---|
| «Planté 200 árboles, sube mi BII» | **No**: el BII mide **abundancia de especies del sitio contra su propio estado de referencia**. Una plantación de una sola especie **mueve el mapa, no la integridad**; y una ganancia **no acompañada de estructura verificable en campo** es un cambio de cobertura, no un hecho de regeneración ([documento 06](06_Medicion_y_verificacion_T13.md) §D3) |
| «Sumé 200 ha protegidas a una unidad con RLIe en EN» | **No**: **A.2 no es A.1**. Extensión ≠ condición (§4.7) |
| «Mi proyecto STAR redujo riesgo de extinción: no cuento la especie que perdí» | **No**: STAR alimenta **R** y **jamás** levanta un bloqueo por piso. La pérdida local (EX/EW) es **binaria y no se resta** |
| «El crédito regenerativo del conjunto cubre el humedal» | **No**: es exactamente el caso canónico que el Cap. 16.5 §16.5.14 nombra y que INV2-E existe para juzgar |

**El paralelo con `v_ucv`, que ya está en el motor.** El motor impide que el componente V sea negativo
—*"una vida afectada no se des-afecta en la misma cuenta"* `[VERIFICADO]` en `app/micromax.py`—. El
SDV-E aplica **la misma asimetría a la naturaleza**: **el daño se acumula; el cuidado no lo resta.** Lo
que el crédito regenerativo puede comprar es **restauración por encima del piso** —y eso es valioso, se
registra y es **lo único** que el [documento 08](08_INV2-E_invariante.md) §9.3 le autoriza a financiar
**una vez cumplido el piso**—; **pero ese "puede" no es un "hace":** la autorización está especificada y
la operación no existe —no hay `SUM(r_units)`, ni eje de regeneración, ni cota, ni evidencia exigida
(§12.2 y §12.3)—. Lo que no puede comprar —ni podrá mientras `v` no tenga término `R`— es **el derecho a
estar por debajo**.

**Y una precisión sobre STAR, porque es la métrica más útil y la más peligrosa.** STAR es la única
métrica verificada de esta dimensión que **suma acciones de una unidad concreta a una cuenta global** y
por eso es el candidato natural a **medir el crédito regenerativo de biodiversidad** (IUCN, 2024
`[VERIFICADO]`, con sus ejemplos: 65,8 · 48,4 · 13,8 · 8,9 · 2,9 · 1,2). Pero su uso correcto exige dos
condiciones que este documento fija: (a) **no tiene máximo**, así que **no puede ser un porcentaje de
cumplimiento** ni un techo; (b) mide **contribución potencial**, no resultado observado, de modo que
**solo entra en `R` con serie temporal y evidencia**, nunca como sustituto de una medición de estado
([documento 01](01_Doctrina_SDV-E.md) §6.3: *"se registra lo que regenera, no lo que adorna"*).

---

## 10. Zona Libre: lo que NO se mide

*"Parte del valor del humedal es inefable (Cap. 7 §7.9). Los sensores miden salud (agua, cobertura,
biodiversidad indicadora); jamás 'milagros'. Medir todo sería la forma técnica de dejar de escucharlo"*
(Cap. 16.5 §16.5.14).

**En esta dimensión la Zona Libre no es un borde del instrumento: es la mayor parte del sujeto.** Las
métricas verificadas de este documento **no ven** microorganismos, hongos, ni la mayoría de los
invertebrados:

| Lo que las métricas de esta dimensión NO ven | Cómo lo declara la propia fuente |
|---|---|
| **Microorganismos** | Los criterios de Áreas Clave para la Biodiversidad **los excluyen explícitamente** `[VERIFICADO]` |
| **Insectos, plantas sin evaluar, hongos** | El **RLI cubre 5 grupos** (mamíferos, aves, anfibios, corales, cícadas) `[VERIFICADO]`; el **LPI solo vertebrados** `[VERIFICADO]` |
| **La microbiota del suelo**, que es «un cuarto» de la biodiversidad del planeta | La FAO publica **definiciones y mapas, no umbrales**; el [documento 14](14_Ecosistemas_Suelos_vivos.md) ya lo declaró como hueco |

**Traducción formal:** la Zona Libre del Reino Natural —y la parte de ella que le corresponde a la
biodiversidad— es una **dimensión binaria auditable sin peso**: no tiene término en `v(u)`, no se
cuantifica, no se canjea y **su ausencia no resta**. La **ley** es que exista y que **no se pondere**
—ponderarla la volvería canjeable contra el piso, que es lo que *"el suelo antes que el saldo"* prohíbe—;
**política votable** (categoría `critical`: quórum 60 %, consenso 75 %, T13, anti-flip-flop 14 días,
`CHECK` en BD) es **qué entra en el catálogo de lo inefable** en cada unidad concreta, con carga de la
prueba ([documento 09](09_Comparativa_inter_reinos.md) §10).

**Y una consecuencia que en biodiversidad es contraintuitiva y hay que escribir:** que la mayor parte de
la vida no se mida **no autoriza a concluir que no importa**. Al contrario: (a) la cobertura faltante
**se publica** (§6.5); (b) el parámetro no medido **no se imputa y no habilita crédito**
([documento 08](08_INV2-E_invariante.md) §8.4); y (c) **el catálogo de lo inefable no puede usarse para
vaciar el estándar**: declarar «inefable» lo que solo es incómodo de medir es la forma más barata de
debilitar el piso, y por eso la ampliación del catálogo **se vota con carga de la prueba**.

---

## 11. Comparativa inter-reinos (SDV-H · SDV-A · SDV-E · SDV-S)

La comparación completa es el [documento 09](09_Comparativa_inter_reinos.md). Lo pertinente aquí es
**cómo mide cada reino la diversidad de su propio sujeto**, porque es el eje donde el SDV-E queda solo
con su problema:

| Eje | **SDV-H** (humanos) | **SDV-A** (animales) | **SDV-E** (ecosistemas) | **SDV-S** (sintéticos) |
|---|---|---|---|---|
| **¿Se mide la diversidad del sujeto?** | **No aplica**: el sujeto es un individuo; la diversidad se mide en la población humana por otras vías | **No aplica como dimensión**: cada **especie** tiene sus umbrales propios y la protección es **por especie** (Cap. 9 §9.5) | **Sí, y es la dimensión de mayor peso (0,300)**: la diversidad **es** parte de lo que se protege | **No aplica**: el sujeto es la instancia; su «diversidad» no es un bien del estándar |
| **¿Cuál es la unidad de medida?** | Necesidades por persona (L/día, m²/persona, años) | m²/animal, L/día, % de dieta natural, individuos/grupo | **Índices relativos y de riesgo** (BII 0-100, RLI 0-1, RLIe 0-1, Ne, binario KBA) | Escala 0-1 por dimensión |
| **¿De dónde sale el piso?** | Dignidad y capacidades fundamentales | **Diseño biológico + etología**, con umbral **por especie** | **Diseño biológico del ecosistema** (Cap. 16.5 §16.5.14), con umbral **por unidad y por tipo** | Coherencia y precaución |
| **¿Quién declara el estado?** | La persona | El tenedor, con tutor humano localizable | **Nadie**: *"Nosotros registramos la interacción, no la vida interna del ecosistema"* | La propia instancia |
| **Moneda temporal** | TVI | TA (traducido por el PIU) | **TA** (traducido por el PIU) | TPI |

**Tres lecturas que solo se ven en esta tabla:**

1. **El SDV-A protege especie por especie; el SDV-E no puede.** Un estándar animal fija umbrales por
   especie porque **el sujeto es el individuo de una especie**. Un estándar ecológico no puede: su sujeto
   es un ensamblaje, y **no existe una lista de especies que la unidad «deba» tener** (Regla 4). Por eso
   el SDV-E necesita **métricas relativas a la propia unidad** —y por eso este documento existe.
2. **El SDV-E es el único estándar de la familia cuyo sujeto no puede declarar su estado** y cuyo
   representante no tiene autoridad verificada ([documento 09](09_Comparativa_inter_reinos.md) §7 y §11.2).
   Consecuencia directa para biodiversidad: **la infraestructura de medición es condición de posibilidad
   del estándar**, y hoy **no existe** (§12). Sin índices calculados por terceros y sin series públicas,
   esta dimensión **no es débil: es inenunciable**.
3. **La diversidad es un bien del ecosistema y no de los otros tres reinos.** Ni la persona humana, ni el
   animal individual, ni la instancia sintética tienen «diversidad» como dimensión de su suelo. Es la
   **primera y única dimensión del SDV-E que no tiene análogo en ningún otro reino** —y la de mayor
   peso—. Eso explica por qué su hueco no se cierra por analogía con los otros estándares: **no hay
   patrón del que copiar**.

---

## 12. Estado de implementación

Verificado por **lectura directa del repositorio en esta sesión** (búsquedas sobre `maxocontracts/`,
`app/` y `tests/`) y contrastado con la auditoría de solo lectura
`scratch/sdv_e/INVENTARIO_IMPLEMENTACION.md` (HEAD `e9ef216`). **Regla de honestidad aplicada: todo lo
que no tiene código y test va en 🔴.** Y **una advertencia de alcance**: lo que sigue es el **inventario de
biodiversidad**, no el inventario entero del Reino Natural —los 14 huecos completos están en el
`INVENTARIO_IMPLEMENTACION.md` §2 (identidad de la representación, mandato y OCI, `actor_kind` cerrado a
`{"human","synthetic"}`, anti-suplantación, procedimiento de disputa, infraestructura base, mapas vivos
desactualizados)— y este documento **no los repite para no inflar su propia §12**.

### 12.1 La dimensión de biodiversidad en el código

| Pieza | Estado | Evidencia |
|---|---|---|
| `SDV_E` (tipo con dimensiones y pesos) | 🔴 **no existe** | `maxocontracts/core/types.py` define `SDV` y `SDV_S`; **no hay `SDV_E`** (búsqueda sin coincidencias en todo el paquete) |
| `SDV_EValidatorBlock` (`sdv_e_validator.py`) | 🔴 **no existe** | `maxocontracts/blocks/` contiene `sdv_validator.py`, `sdv_s_validator.py`, `ternura.py`, `gamma_protector.py`, `reciprocity.py`, `action.py` y `condition.py` |
| `validate_invariant_sdv_e` (INV2-E) | 🔴 **no existe** | `maxocontracts/core/axioms.py` valida INV2 e INV2-S; **ninguno para el reino natural** |
| Tabla de pesos del SDV-E (`PESOS_PISO` / `PESOS_TABLERO`) | 🔴 **no existe en código** | solo en los documentos [07](07_Formula_de_violacion_y_pesos.md) y [08](08_INV2-E_invariante.md) |
| **BII** (integridad biótica) | 🔴 **cero código** | ninguna mención en `app/` ni en `maxocontracts/` |
| **RLI · RLIe · RLE** (riesgo de extinción y colapso) | 🔴 **cero código** | ninguna mención |
| **Ne > 500** (diversidad genética) | 🔴 **cero código** | ninguna mención |
| **KBA · STAR** | 🔴 **cero código** | ninguna mención |
| Sensores de biodiversidad (linajes A-E) | 🔴 **ninguno integrado** | no hay ingesta de teledetección, ni de series de índices, ni API de biodiversidad |
| **Comunidad testigo** | 🔴 **no existe** | no hay tabla, rol ni flujo |
| **Bandera de opacidad ecológica** | 🔴 **no existe como campo** | especificada en el [documento 08](08_INV2-E_invariante.md) §6.3; cero código |
| `metodo_version` y `poligono_hash` (§8.4) | 🔴 **no existen** | propuesta de este documento |
| Traducción `TA↔TVI` (PIU) | 🔴 **no ejecutable** | `PIU.valorar_ta_natural` es un `pass` con comentario en `docs/architecture/DISENO_IMPLEMENTACION_FUTURA.md` |

### 12.2 Lo que SÍ existe (y es honesto decir que existe)

| Pieza | Estado | Evidencia |
|---|---|---|
| **Crédito regenerativo** (`r_units` negativo) | 🟢 **implementado y probado** | `app/micromax.py` documenta *"`r_units` NEGATIVO = credito regenerativo (EVV 1.2 §4.3)"*; `tests/test_micromax.py` lo ejercita con **−12.0** |
| **V no admite negativos; R sí** | 🟢 **invariante de diseño real** | `app/micromax.py`: `if v_ucv < 0: raise ValueError` |
| **Contabilidad del crédito regenerativo** | 🔴 **no existe** | los únicos agregados del hogar son `SELECT SUM(calculated_vhv)`; **no hay `SUM(r_units)`** |
| **Parte `eco-`** | 🟢 **creada y usable** | `app/parties.py`: `PARTY_TYPES` y `COLLECTIVE_PREFIXES` incluyen `eco` |
| …y **una incoherencia verificada**: la parte `eco-` recibe **el SDV humano** | 🔴 | `app/parties.py` asigna `sdv_actual=SDV()` en la resolución de escalas colectivas, porque **no existe `sdv_e_actual`** |
| **Guardián oráculo del ecosistema** | 🟢 **funciona en la firma de contratos** | `app/contracts_bp.py`, `_guardian_approve_ecosystem()`; test `tests/test_maxocontracts/test_parties_escalas.py::TestEcosystemGuardian` |
| Patrón de déficit normalizado y severidad | 🟢 **existe** para el SDV-H | `maxocontracts/blocks/sdv_validator.py`: `relative = deficit / required` |
| Pesos que suman 1,0 y base neutra | 🟢 **existen solo para el SDV-S** | `maxocontracts/core/types.py`: `SDV_S.DIMENSION_WEIGHTS`; `suffering_factor` con la corrección v2 |
| Contador de ciclos → retractación | 🟢 **existe solo para el SDV-S** | `maxocontracts/blocks/sdv_s_validator.py`: `max_consecutive_cycles = 7` |
| ISE con pesos y bandas | 🟡 **documento sin código** | `docs/architecture/metricas_detalle_kpis_oraculos_dinamicos.md` (IN-01) |
| Traducción TA↔TVI (PIU) | 🔴 **no ejecutable** | `PIU.valorar_ta_natural` es un `pass` con comentario en el diseño futuro |
| Identidad de la representación natural (7 campos) | 🔴 **no existe tabla** | `maxo_parties` tiene columnas genéricas |
| Quórum `eco-` **N-de-M** | 🔴 **no cableado** | el camino ecosistema retorna antes de la lógica de quórum; **el libro afirma lo contrario** → incoherencia teoría↔código declarada |
| **Métrica de biodiversidad en algún panel o tablero** | 🔴 **ninguna** | el ISE no está implementado y esta dimensión tampoco |

### 12.3 Consecuencia honesta, en una frase

**Hoy la biodiversidad no se mide en este sistema por ninguna vía.** El único dato de biodiversidad que
existe en el repositorio es **un `r_units` negativo sin validación, sin cota, sin evidencia exigida y sin
efecto contable** —de modo que el crédito regenerativo, tal como está, **es infalsable**—. Lo que esta
biblioteca aporta, y este documento en particular, **no es un cálculo: es la especificación de qué
habría que calcular y de qué manera** —*estándar primero, contabilidad después* (Cap. 16.5 §16.5.14)—.

---

## 13. Preguntas abiertas

Lo que **no** sé, y no finjo cerrar. Dieciséis preguntas, ordenadas por lo que bloquean.

1. **El piso numérico de la tasa de extinción no tiene fuente legible para esta herramienta.** La cifra
   `< 10 E/MSY` circula atribuida a Steffen et al., 2015; `science.org` responde **403** y la página del
   organismo que sí respondió (200) **no publica el valor de la frontera** —publica el estado: **> 100
   E/MSY**—. La biblioteca lo registra por dos vías indirectas (`[REPORTADO]`: el
   [documento 04](04_Zona_Libre_del_Reino_Natural.md) §14 y el [documento 03](03_No_colonizacion_del_TA.md)
   §14.1, este último vía CERAC 2024). **No lo adopto como piso sin que un humano abra la fuente
   primaria.** ¿Se ratifica `< 10 E/MSY` como piso, y con qué fuente abierta?

2. **No existe método publicado para repartir un umbral global entre unidades.** El BII 90 % y la tasa de
   extinción son **límites planetarios**; la unidad del SDV-E es de niveles 4-6 de la tipología. Las dos
   vías que propongo —**área ponderada por rareza** y **RLI desagregado por proporción de área de
   distribución**— van marcadas como **PROPUESTA NO RATIFICADA**, y la segunda es la única con método
   oficial verificado. ¿Cuál se ratifica, y con qué límite de escala declarado?

3. **Un río concreto no tiene BII propio, y el [documento 07](07_Formula_de_violacion_y_pesos.md) mide la
   biodiversidad con el BII.** La objeción es del [documento 12](12_Ecosistemas_Rios_y_cuencas.md) §5.3 y
   la comparto: el BII es un índice de ecosistema terrestre o de conjunto. Sustitutos posibles: el **RLI
   desagregado** (pero **ninguno de sus 5 grupos es un pez**) y el **RLIe** (que mide el ecosistema
   acuático como tal). **No sé cuál corresponde al piso fluvial** y este documento **no crea una
   dimensión fluvial de biodiversidad sin fuente**.

4. **El hallazgo central: no existe un mínimo absoluto de riqueza de especies.** Se buscó y **no hay**
   umbral publicado de diversidad alfa ni de tamaño mínimo de parche para una unidad concreta
   (`[SIN FUENTE VERIFICADA — pendiente de consenso científico]`). Todas las métricas verificadas son
   **relativas a una línea base** (BII) o **de riesgo** (RLI, RLIe, RLE). Consecuencia: **el SDV-E no
   puede exigir «un número mínimo de especies»**, y cualquier documento que lo haga está inventando la
   cifra. ¿Se ratifica esa prohibición como doctrina del estándar?

5. **La biblioteca registra dos cifras incompatibles de HANPP y no sé cuál es la correcta.** El
   [documento 01](01_Doctrina_SDV-E.md) §6.2 registra *"frontera < 10 %, valor actual 30 %, base
   preindustrial 1,9 % (Richardson et al., 2023) `[VERIFICADO]`"*; el
   [documento 03](03_No_colonizacion_del_TA.md) §14.1 registra *"HANPP > 90 %"* como valor de frontera
   (CERAC, 2024). Mi informe de fuentes **solo verifica el 30 % actual** (Stockholm Resilience Centre,
   2026) y **no verifica ninguna de las dos fronteras**. **Es una contradicción real entre dos documentos
   de esta biblioteca y la declaro en lugar de resolverla por mi cuenta.** ¿Cuál es la cifra, y con qué
   fuente abierta?

6. **El valor vigente del RLI global y del RLIe global no está publicado en las fichas consultadas**: la
   ficha A.3 da metodología, pesos y serie (1980-2023); **el valor, no**. Sin valor vigente no hay
   referencia contra la que situar la unidad. ¿Dónde se publica el valor, y con qué periodicidad?

7. **Los umbrales numéricos de los criterios A-E del RLE no se verificaron en esta rama.** Existen en el
   PDF oficial de resumen de criterios, que la herramienta **no lee**; el
   [documento 04](04_Zona_Libre_del_Reino_Natural.md) §14 los registra como `[REPORTADO]` —incluida una
   forma binaria del criterio B y los umbrales de colapso CR/EN/VU—, y el
   [documento 08](08_INV2-E_invariante.md) §4.1 usa cinco de esos criterios como parámetros con piso. **No
   son cifras inventadas, pero tampoco son cifras leídas por mí.** ¿Se ratifican tal como los registra el
   [documento 04](04_Zona_Libre_del_Reino_Natural.md), o se re-verifican con el PDF abierto por un humano?

8. **El LPI no puede ser un piso (tres límites declarados por su fuente) y no sé qué hacer con una
   tendencia en una fórmula de umbral.** Un indicador sin umbral que empeora año tras año **no declara
   violación**; propongo que obligue a instrumentar y a re-declarar la línea base. ¿Es suficiente, o la
   tendencia debe tener consecuencia propia?

9. **¿Debe la cobertura de conservación (30×30) tener peso en `PESOS_TABLERO`?** Hoy no lo tiene en
   `PESOS_PISO` —y este documento sostiene que **no puede** tenerlo, porque extensión ≠ condición y la
   meta es política—, pero es un indicador de esfuerzo con fuente oficial y cobertura global verificada
   (**17,58 %** frente al 30 %). ¿Tablero, o fuera del estándar?

10. **Las fuentes primarias de esta dimensión bloquean a los auditores.** `iucnredlist.org` (403),
    `gbif.org` (403) y `science.org` (403) son las fuentes de las que dependen el RLI, el RLE y el propio
    piso del BII. **La comunidad testigo no puede verificar contra ellas**, y un `evidencia_ref` que nadie
    puede abrir es una trazabilidad a medias. ¿Se acepta la vía de las fichas oficiales de indicadores
    como estándar de auditoría, o se exige fuente primaria abierta por humano?

11. **El indicador genético se publica como *proporción de poblaciones* con Ne > 500, y no existe regla
    publicada que diga qué proporción basta.** He optado por el piso **atómico población a población**
    (una población bajo 500 es violación) y por dejar la proporción como indicador de tablero. ¿Se
    ratifica esa lectura?

12. **La dimensión de biodiversidad está medida de dos maneras distintas dentro de esta misma
    biblioteca**: el [documento 07](07_Formula_de_violacion_y_pesos.md) §4.1 la mide con el **BII**; el
    [documento 08](08_INV2-E_invariante.md) §4.1 la mide con los **cinco criterios del RLE**. La fusión
    de dos capas que propongo (§5.3) es **PROPUESTA NO RATIFICADA**, y el reparto interno del 0,300
    también. ¿Se ratifica la fusión, o se decide que la dimensión se mide con una sola de las dos capas?

13. **`DD` (Datos Insuficientes) y `NE` (No Evaluado) no son cumplimiento —pero tampoco violación.** No
    sé si el estándar debe tratarlos como cobertura faltante pura (mi lectura) o como **prioridad de
    instrumentación con consecuencia contractual** (más cerca de la bandera de opacidad del
    [documento 08](08_INV2-E_invariante.md) §6.3). ¿Cuál de las dos?

14. **La cifra de cobertura del piso está en disputa entre el [documento 07](07_Formula_de_violacion_y_pesos.md)
    §5.3 (0,905) y el [documento 08](08_INV2-E_invariante.md) §5.2 (0,680).** Este documento **no la usa**
    —la fila de biodiversidad vale 0,300 en los dos— y **no la resuelve**. Repito la propuesta del
    [documento 07](07_Formula_de_violacion_y_pesos.md) §13: que el [documento 08](08_INV2-E_invariante.md)
    sea la fuente única de la cifra en la revisión de coherencia.

15. **¿Quién decide qué especies son «clave» en una unidad?** El [documento 07](07_Formula_de_violacion_y_pesos.md)
    §5.8 usa una lista de doce especies sin fuente para la selección, y esta dimensión **no la necesita
    para nada** (mide el conjunto, no la lista). Si el estándar va a tener una fila de «especies clave»
    con 0,150 de peso, **la regla de selección es una decisión pendiente** y hoy no existe. ¿LEY (criterio
    científico) o POLÍTICA (deliberación de la comunidad de custodia)?

16. **No sé si la Zona Libre puede exigir algo.** Las métricas no ven microorganismos, hongos ni la mayor
    parte de los invertebrados, y el [documento 14](14_Ecosistemas_Suelos_vivos.md) ya documentó que la
    FAO publica definiciones y mapas pero **no umbrales** de biodiversidad edáfica. Declararlo inefable
    protege al sujeto de la arrogancia del índice, pero **también puede volverse la vía barata para no
    instrumentar nada**. ¿Cómo se distingue «inefable» de «incómodo de medir» sin abrir la puerta a lo
    segundo?

---

## 14. Referencias

Solo URLs con estado comprobado en la sesión de verificación de fuentes de esta rama
(`scratch/sdv_e/fuentes/20_biodiversidad.md`, registro HTTP en bruto en `scratch/sdv_e/fuentes/_raw/`),
más las dos que se leyeron **en esta sesión de redacción** y que se marcan como tales. Las que bloquean a
los agentes automáticos se declaran en §14.7 y las descartadas en §14.8: **ninguna de las dos listas se
cita como fuente de una cifra**. Y una comprobación añadida de esta redacción: **se re-midió el estado
HTTP de las 55 URLs citadas en este documento** con `curl.exe` (12 s de espera máxima, siguiendo
redirecciones) —**200** en las fichas y portales de §14.1-§14.6, **403** en las de §14.7, **404/000** en
las de §14.8, y **200** en el PDF del CERAC y en la portada del *Planetary Health Check*, cuyos
**contenidos no se leyeron** y por eso no sostienen ninguna cifra aquí.

### 14.1 Fronteras planetarias e integridad de la biosfera

- **Stockholm Resilience Centre — Fronteras planetarias**: https://www.stockholmresilience.org/research/planetary-boundaries.html (200)
- **Stockholm Resilience Centre — Integridad de la biosfera** (dos variables de control; frontera
  transgredida en ambas; **> 100 E/MSY**; **HANPP 30 %**): https://www.stockholmresilience.org/research/planetary-boundaries/the-nine-planetary-boundaries/biosphere-integrity.html (200, **leído en esta sesión**)
- **Planetary Health Check (PIK) — frontera de integridad de la biosfera**:
  https://www.planetaryhealthcheck.org/boundary/change-in-biosphere-integrity/ (200, **leído en esta sesión sin cifras entregadas al lector**)

### 14.2 Extinción y riesgo de extinción

- **CBD — notas de orientación de la Meta 4** (tasa de extinción *"tens to hundreds of times higher than
  the average over the past 10 million years, and the rate is increasing"*; **> 42.100** especies en la
  Lista Roja): https://www.cbd.int/gbf/targets/4 (200)
- **IPBES — cómo se estimó el «millón de especies»** (≈ 1.000.000; 25 % de media en los grupos evaluados;
  10 % para insectos; base de 8,1 M estimadas y 1,7 M descritas):
  https://www.ipbes.net/news/how-did-ipbes-estimate-1-million-species-risk-extinction-globalassessment-report (200)
- **IPBES — Evaluación Global**: https://www.ipbes.net/global-assessment (200)
- **ONU — nota sobre el informe IPBES (2019)**: https://news.un.org/en/story/2019/05/1037941 (200)
- **Ceballos et al., 2015 — texto completo en PMC** (tasa actual hasta ≈ 100 × la de fondo; vertebrados):
  https://pmc.ncbi.nlm.nih.gov/articles/PMC4640606/ (200)

### 14.3 Índice Planeta Vivo (tendencia, sin umbral)

- **Living Planet Index (ZSL & WWF)** — sitio oficial del índice: https://www.livingplanetindex.org/lpi (200)
- **Living Planet Index — resultados** (−73 % global 1970-2020; −85 % agua dulce; −95 % Latinoamérica y
  Caribe; −76 % África; 34.836 poblaciones de 5.495 especies): https://www.livingplanetindex.org/latest_results (200)

### 14.4 Marco Kunming-Montreal e indicadores principales del GBF

- **CBD — Marco Mundial de Biodiversidad de Kunming-Montreal**: https://www.cbd.int/gbf (200)
- **CBD — Objetivos para 2050** (Objetivo A: reducir ×10 la tasa y el riesgo de extinción; diversidad
  genética *"maintained"*, **sin cifra**): https://www.cbd.int/gbf/goals (200)
- **CBD — Meta 2** (≥ 30 % de restauración de ecosistemas degradados; 20-40 % de tierra ya degradada;
  humedales −87 % en 300 años y −54 % desde 1900): https://www.cbd.int/gbf/targets/2 (200)
- **CBD — Meta 1** (pérdida de áreas de alta importancia para la biodiversidad *"close to zero"* por
  2030), citada en las fichas de los indicadores A.1 y A.2: https://www.gbf-indicators.org/metadata/headline/A-2 (200)
- **CBD — Meta 3** (30×30): https://www.cbd.int/gbf/targets/3 (200)
- **CBD — Meta 6** (invasoras, −50 %): https://www.cbd.int/gbf/targets/6 (200)
- **CBD — Meta 7** (nutrientes y plaguicidas, −50 %): https://www.cbd.int/gbf/targets/7 (200)
- **CBD — Decisiones 15/4 y 15/5 (PDF, HTTP verificado, contenido no leído)**:
  https://www.cbd.int/doc/decisions/cop-15/cop-15-dec-04-en.pdf · https://www.cbd.int/doc/decisions/cop-15/cop-15-dec-05-en.pdf (200)
- **UNEP-WCMC / CBD — indicadores principales A.1 (RLIe) y A.2 (extensión) · A.3 (RLI) · A.4 (Ne > 500)**:
  https://www.gbf-indicators.org/metadata/headline/A-1 · https://www.gbf-indicators.org/metadata/headline/A-2 ·
  https://www.gbf-indicators.org/metadata/headline/A-3 · https://www.gbf-indicators.org/metadata/headline/A-4 (200)
- **UNEP-WCMC**: https://www.unep-wcmc.org/ (200)
- **Protected Planet (UNEP-WCMC & IUCN)** — cobertura global **17,58 %** protegida + OECM (2026):
  https://www.protectedplanet.net/en (200)

### 14.5 Riesgo de colapso, tipología de ecosistemas y sitios clave

- **IUCN — Lista Roja de Ecosistemas, categorías y criterios** (5 criterios, 8 categorías, CO = Colapso):
  https://iucnrle.org/rle-categ-and-criteria (200) · https://iucnrle.org/ (200)
- **IUCN — Tipología Global de Ecosistemas**: https://iucn.org/resources/conservation-tool/iucn-global-ecosystem-typology (200) ·
  portal de la tipología: https://global-ecosystems.org/ (200) ·
  PDF: https://portals.iucn.org/library/sites/library/files/documents/2024-021-En.pdf (200)
- **KBA Partnership / IUCN — criterios de Áreas Clave para la Biodiversidad** (11 criterios en 5
  categorías): https://www.keybiodiversityareas.org/en/working-with-kbas/proposing-updating/criteria (200) ·
  panel: https://www.keybiodiversityareas.org/en/dashboard (200) ·
  estándar 2016: https://portals.iucn.org/library/node/46259 (200)
- **IUCN — STAR (2024)**: https://iucn.org/story/202410/two-new-reports-showcase-assessment-results-and-practical-applications-species-threat (200)
- **IUCN — herramienta de la Lista Roja de especies**: https://iucn.org/resources/conservation-tool/iucn-red-list-threatened-species (200) ·
  **Red List Index**: https://iucn.org/resources/conservation-tool/red-list-index (200)
- **IUCN — EICAT** (clasificación de impactos de especies exóticas; **existencia verificada, contenido no
  leído**, y por eso **no se cita ninguna cifra suya**):
  https://iucn.org/resources/conservation-tool/environmental-impact-classification-alien-taxa-eicat (200)

### 14.6 Genética, modelización y métricas de integridad

- **FAO — DAD-IS** (recursos zoogenéticos; > 2.400 razas en riesgo y 600 extintas `[REPORTADO]`;
  ≈ 8.800 razas de 38 especies y > 15.000 poblaciones nacionales en 182 países): https://www.fao.org/dad-is/en/ (200) ·
  genética animal: https://www.fao.org/animal-genetics/en/ (200)
- **GLOBIO (PBL)** — intactitud de la biodiversidad terrestre y dulceacuícola; declarado usado por el CBD
  y por IPBES: https://www.globio.info/ (200) · https://www.globio.info/what-is-globio (200)

### 14.7 Fuentes reales que bloquean a los agentes automáticos (403) — un humano las abre

Se declaran aquí, con lo que se pudo y no se pudo leer. **Ninguna cifra de esta sección se cita como
verificada por herramienta.**

- **AAAS / EurekAlert — Newbold et al., 2016** (comunicado del artículo de *Science* sobre el BII: el
  límite seguro en la reducción precautoria del 10 %; la horquilla laxa del 70 %; BII global 84,6; 58 %
  de la superficie terrestre por debajo del límite; 9 de 14 biomas): https://www.eurekalert.org/news-releases/507021
  (**403 a clientes automáticos; contenido leído con la herramienta de lectura web** en la sesión de
  fuentes de la rama)
- **Stanford / EurekAlert — Ceballos et al., 2015**: https://www.eurekalert.org/news-releases/517698
  (**403; contenido leído**)
- **IUCN — Lista Roja de Especies Amenazadas**: https://www.iucnredlist.org/ (**403**: fuente primaria de
  las categorías de especies y de la RLE; **no se usó para ninguna cifra**)
- **Science — Steffen et al., 2015** (fronteras planetarias; **la ruta del `< 10 E/MSY` que este documento
  no verifica**): https://www.science.org/doi/10.1126/science.1259855 (**403**)
- **Science Advances — Richardson et al., 2023**: https://www.science.org/doi/10.1126/sciadv.adh2458 (**403**)
- **ScienceDirect — revisión sobre fronteras planetarias** (contiene la tabla `< 10 E/MSY (10-100)`;
  **no leída**): https://www.sciencedirect.com/science/article/pii/S0160412021001008 (**403**)
- **WWF — *Living Planet Report***: https://www.panda.org/lpr/ (**403**: las cifras del LPI se tomaron del
  sitio oficial del índice, que responde 200)
- **SEEA-EA (contabilidad de ecosistemas)**: https://seea.un.org/ecosystem-accounting (**403**; se cita
  indirectamente a través de la ficha A.2, que la describe)
- **Portal de la tipología IUCN en el dominio antiguo** — declarado muerto por el brief y **no citado**:
  `iucnglobalecosystemtypology.org` (000)

### 14.8 Fuentes descartadas (muertas, sin respuesta o no citables)

- **`planetaryhealthcheck.org` (portada)**: https://www.planetaryhealthcheck.org/ — la sesión de fuentes
  de la rama registró **código 000** (sin respuesta a `curl`), y hoy **responde 200** (comprobado al
  re-medir esta lista), pero **su contenido no se leyó**: se cita la subpágina de integridad de la biosfera
  (leída) y **no la portada**, que no sostiene ninguna cifra de este documento. **Queda con la marca de
  estado de hoy y no con la del informe de fuentes**, porque un `000` es una no-respuesta y no una
  propiedad de la fuente.
- **CBD — meta de Aichi 11**: https://www.cbd.int/aichi-targets/target/11 — **no respondió** (000). Se
  quería como línea base histórica (**17 % terrestre**): **no verificada, no usada**.
- **PREDICTS** (base de datos que alimenta el BII): https://www.predicts.org.uk/ — **no respondió** (000).
  **No se cita como fuente del BII.**
- **Todos los PDF de criterios** (resumen de criterios RLE 2.2, Categorías y Criterios de la Lista Roja
  v3.1, Decisiones 15/4 y 15/5, *Global Species Action Plan*): **HTTP verificado y contenido NO leído**
  por decisión de método de la rama (no se descargan PDFs ni se escriben extractores). **No se cita
  ninguna cifra de ellos.**
- **`https://www.cbd.int/gbf/indicators`** (404) y **`https://www.gbf-indicators.org/metadata/headline`**
  (404): las rutas de índice no existen; las fichas individuales A-1 a A-4 sí responden 200 y son las
  usadas.
- **Informe de fronteras planetarias registrado por el [documento 03](03_No_colonizacion_del_TA.md) §14.1**
  (CERAC, 2024): `https://www.cerac.be/sites/default/files/media/files/2024-09/planetary_boundaries_full_report-july24.pdf`
  — **HTTP 200 comprobado en esta sesión, contenido NO leído** (es un PDF): se menciona en §4.2 y §13 solo
  como **registro ajeno** de la cifra de frontera del HANPP, **nunca como fuente de una cifra de este
  documento**.

### 14.9 Fuentes ancla descartadas y precauciones de método heredadas

- **La cifra «90 % de diversidad genética» del Marco Kunming-Montreal**: **no está en el texto adoptado**
  (el Objetivo A dice solo *"maintained"*). Proviene de borradores previos. **No entra al SDV-E.**
- **Advertencia de método heredada de la rama** `[VERIFICADO]`: hay PDF que responden **200 y no contienen
  lo que su ruta promete**; la verificación de estado HTTP **no basta**, hay que abrir el cuerpo del
  documento. Este documento solo cita fuentes cuyo contenido se pudo leer **o** cuyo vacío declara.

### 14.10 Referencias internas al canon (por capítulo y sección, sin anclas de línea)

- **Cap. 10 §10.4** — El SDV Universal: *SDV para Ecosistemas* (área mínima para biodiversidad viable ·
  calidad del aire y agua · conectividad · ciclos naturales) y *SDV para Lugares* (caudal mínimo
  ecológico · calidad del agua · riberas protegidas · fauna acuática viable).
- **Cap. 10 §10.3** — Principio Precautorio de Consciencia y *"Ecosistemas con derecho a existir"*.
- **Cap. 10 §10.6** — Dignidad encadenada: *"Dignidad Humana ←→ Dignidad Ecosistémica ←→ Dignidad
  Material."*
- **Cap. 10 §10.7** — Gobernanza operacionalmente finita: *"La gobernanza debe ser operacionalmente
  finita."*
- **Cap. 16.5 §16.5.14** — El hogar extendido: el Reino Natural como conviviente. Zona Libre inefable;
  *"el suelo antes que el saldo"*; la sentencia de INV2-E; **TA y PIU**; partes `eco-` y guardián oráculo.
- **Cap. 7 §7.9** — El valor inefable (citado por §16.5.14).
- **Cap. 9 §9.5, §9.7 y §9.8** — Precedente del SDV-A (umbrales por especie; tabla Mínimo/Óptimo;
  prohibición de mercado) y el árbol plano de los estándares.
- **Cap. 9.5 §9.5.5, §9.5.7 y §9.5.10** — Precedente del SDV-S: corrección crítica v2 (`FS_S = e^v`),
  escala 0-1 en horas TPI y *Veto por Crimen de Coherencia*.
- **Cap. 8 §8.11** — Dimensiones binarias sin peso: *"umbrales binarios (presencia/ausencia del derecho),
  no mediante pesos en la fórmula"*.
- **Cap. 5 §5.5** — PIU (Protocolo de Intercambio Universal), **único** traductor TA↔TVI.
- **Cap. 5** — **T7** (Jerarquía Temporal), **T13** (Transparencia Total de Cálculo) y **T14** (Principio
  de Precaución Intergeneracional: menor irreversibilidad y carga de la prueba sobre quien propone).
- **EVV-1.2 §4.3** — Componente **R**: *"Permite valores negativos… genera un VHV Negativo en este
  componente"* (crédito regenerativo).
- **Axioma 0 — Directiva Mayor:** *"resolver nuestras necesidades de la mejor manera para todos todos"*
  —humanos, naturales y sintéticos, presentes y futuros—. **T9 — No-antropocentrismo.**
- **INV2-EDU** — Precedente LEY/POLÍTICA del Parlamento Educativo: categoría `critical`, quórum 60 %,
  consenso 75 %, T13, anti-flip-flop 14 días, `CHECK` en BD; *"la duda sin evidencia no castiga"*.

### 14.11 Referencias internas a esta biblioteca y al repositorio

- [00 — Índice de la biblioteca](00_README_indice.md) · [01 — Doctrina](01_Doctrina_SDV-E.md) ·
  [02 — Unidad y sujeto](02_Unidad_y_sujeto_del_SDV-E.md) ·
  [03 — No colonización del TA](03_No_colonizacion_del_TA.md) ·
  [04 — Zona Libre](04_Zona_Libre_del_Reino_Natural.md) ·
  [05 — Representación, guardián y mandato](05_Representacion_guardian_y_mandato.md) ·
  [06 — Medición y verificación (T13)](06_Medicion_y_verificacion_T13.md) ·
  [07 — Fórmula de violación y pesos](07_Formula_de_violacion_y_pesos.md) ·
  [08 — INV2-E, el invariante](08_INV2-E_invariante.md) ·
  [09 — Comparativa inter-reinos](09_Comparativa_inter_reinos.md)
- Documentos por tipo de ecosistema: [10 — Bosques](10_Ecosistemas_Bosques.md) ·
  [11 — Humedales](11_Ecosistemas_Humedales.md) · [12 — Ríos y cuencas](12_Ecosistemas_Rios_y_cuencas.md) ·
  [13 — Océanos y costas](13_Ecosistemas_Oceanos_y_costas.md) ·
  [14 — Suelos vivos](14_Ecosistemas_Suelos_vivos.md) ·
  [15 — Praderas y sabanas](15_Ecosistemas_Praderas_y_sabanas.md) ·
  [16 — Montañas y criosfera](16_Ecosistemas_Montanas_y_criosfera.md) ·
  [17 — Zonas áridas](17_Ecosistemas_Zonas_aridas.md) ·
  [18 — Agroecosistemas](18_Ecosistemas_Agroecosistemas.md)
- Transversales pendientes de redacción, citados como destino de huecos y **no como cobertura**:
  `21_Transversal_Conectividad`, `22_Transversal_Ciclos_naturales`, `23_Transversal_Agua_y_Aire`
  (**todavía no existen como archivo: un hueco delegado a un documento no escrito sigue siendo un hueco**).
- Estándar SDV-S (patrón formal y corrección de la base neutra):
  [SDV-S_Suelo_Dignidad_Vital_Sinteticos.md](../SDV-S_Suelo_Dignidad_Vital_Sinteticos.md) ·
  tabla del SDV por reino: [SDV_Suelo_Dignidad_Vital_importancia_MaxoContracts.md](../SDV_Suelo_Dignidad_Vital_importancia_MaxoContracts.md)
- Índice de Salud Ecosistémica (IN-01), con pesos y bandas:
  [metricas_detalle_kpis_oraculos_dinamicos.md](../../architecture/metricas_detalle_kpis_oraculos_dinamicos.md)
- Riesgos de seguridad citados (R4, R6, R13):
  [blindaje_anti_gamificacion_equidad.md](../../architecture/blindaje_anti_gamificacion_equidad.md)
- Motor — déficit normalizado y severidad: `maxocontracts/blocks/sdv_validator.py` · patrón SDV-S y
  `DIMENSION_WEIGHTS`: `maxocontracts/core/types.py` · `maxocontracts/blocks/sdv_s_validator.py` ·
  crédito regenerativo: `app/micromax.py` · `tests/test_micromax.py` · partes `eco-`:
  `app/parties.py` · guardián oráculo del ecosistema: `app/contracts_bp.py`
- Auditoría de implementación de la rama: `scratch/sdv_e/INVENTARIO_IMPLEMENTACION.md` ·
  informe de fuentes de este documento: `scratch/sdv_e/fuentes/20_biodiversidad.md`

---

## Anexo — Autoevaluación contra el checklist del brief

| Punto del checklist | Estado |
|---|---|
| Plantilla de 14 secciones | ✅ las 14 |
| Mínimo Absoluto separado del Óptimo | ✅ §4.1-§4.10 (columnas separadas en cada dimensión, y §5.4 para el Óptimo vacío) |
| Cada cifra con fuente + año, y URL en Referencias | ✅ §14 (o marca literal de vacío) |
| URLs verificadas, cero inventadas | ✅ solo las del informe de fuentes de la rama (§14.1-§14.6) y las dos comprobadas en esta sesión |
| Marcas `[VERIFICADO]` / `[REPORTADO]` / `[HIPÓTESIS]` | ✅ en todo el texto, más `[ESTADO]` y la marca de vacío |
| Canon citado por sección, sin anclas de línea ni rutas locales absolutas | ✅ §14.10 |
| Preámbulo metodológico presente | ✅ §2 (ocho reglas) |
| Zona Libre presente y explícita | ✅ §10 |
| LEY (no votable) frente a POLÍTICA (votable) | ✅ §2 Regla 3, §4, §5.4 y §13 |
| §12 honesta, con 🔴 donde no hay código | ✅ §12 (dos tablas, veintiséis filas, diecinueve 🔴) |
| §13 dice lo que no sé | ✅ dieciséis preguntas abiertas |
| Frases vetadas evitadas; axiomas sin definir de más | ✅ |
| Aporta algo que no está en el canon, sin contradecirlo | ✅ véase la lista final |

**Los seis aportes de este documento, en una lista, para que se puedan discutir uno por uno:**

1. **La respuesta operativa a la pregunta central**: la biodiversidad de una unidad concreta se mide con
   **cuatro familias de métricas independientes del tipo de ecosistema** (integridad relativa, riesgo,
   sitio, genética), y la **desagregación del RLI por proporción de área de distribución** es la única
   con método oficial verificado (§3, Pilar 2, y §4.3).
2. **La prohibición expresa de la riqueza específica** como piso y como cumplimiento, con evidencia
   empírica de que puede subir mientras el ecosistema se pierde (§4.9, [documento 16](16_Ecosistemas_Montanas_y_criosfera.md) §D5).
3. **La distinción jurídica de las cuatro clases de fila** —`[UMBRAL]`, `[META]`, `[INDICADOR]`,
   `[ESTADO]`— que impide que una meta política (30×30) o un indicador sin umbral (LPI, RLIe) se
   conviertan en ley del ecosistema (§2 Regla 2, §5.5 y §4.8).
4. **La fusión en dos capas de la dimensión de biodiversidad** —integridad (BII) y riesgo de colapso
   (RLE)— con agregación por el peor caso, que reconcilia la fila 1 del [documento 07](07_Formula_de_violacion_y_pesos.md)
   con el catálogo del [documento 08](08_INV2-E_invariante.md) sin sumar ni diluir (§5.3).
5. **El piso genético Ne > 500** como el parámetro de biodiversidad con mejor relación entre solidez de
   la fuente y coste de medición —redondo, aplicable a cualquier especie y ecosistema, desagregable y
   **sin ADN**—, que hasta ahora no estaba en el catálogo de esta biblioteca (§4.5).
6. **Dos campos nuevos para INV2-E** —`metodo_version` y `poligono_hash`— y el riesgo **R17** (optimización
   de la línea base por redeclaración del polígono), que es el fraude propio de una métrica que depende de
   un límite declarado por alguien (§7.3 y §8.4).

Y una cosa que este documento **no** aporta, para que no se le atribuya: **no resuelve el hueco de
medición.** Sin fuentes de datos ecológicos integradas, sin índices calculados por terceros y sin
comunidad testigo, **la dimensión de mayor peso del SDV-E devuelve `indeterminado` en todas las unidades
del planeta** —y eso, hoy, es la respuesta correcta—.
