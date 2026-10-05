# Suelos vivos
## Materia orgánica y carbono orgánico, biodiversidad edáfica y macrofauna, erosión tolerable, compactación, sellado urbano, salinidad y nutrientes: los mínimos por debajo de los cuales el suelo deja de ser un ecosistema y pasa a ser un sustrato

**Autoría:** Oráculo Sintético DeepSeek & Max Nelson López Restrepo
**Fecha:** octubre 2026
**Proyecto:** Maxocracia — El gobierno de la verdad, el tiempo y la vida
**Licencia:** Creative Commons BY-SA 4.0
**Estado:** Propuesta de estándar (rama SDV-E, Ola 4) — NO canon hasta ratificación
**Referencia canónica:** Cap. 10 §10.4 · Cap. 16.5 §16.5.14 · EVV-1.2 §4.3 · Cap. 9.5 (precedente SDV-S)
**Documento:** 14 de la biblioteca `docs/theory/SDV-E/`
**Bloque:** B — SDV-E por tipo de ecosistema (10-19)

---

## 1. Qué es (y qué no es) este SDV

**Qué es.** El estándar de mínimos para **suelos vivos** como unidad ecológica del Reino Natural:
la materia orgánica y el carbono orgánico del suelo (COS), la biodiversidad edáfica y su macrofauna,
el balance entre erosión y formación, la compactación, el sellado, la salinidad y los nutrientes.
Define qué observación convierte cada uno de esos procesos en **violación del piso**, y traduce esa
observación a la forma que el invariante **INV2-E** podrá ejecutar.

Existe porque el suelo es el ecosistema del Reino Natural donde el canon tiene un mandato explícito
y el proyecto **no tenía ni un umbral escrito** —no porque sea el único con mandato: los ríos tienen
el suyo con nombre propio en el Cap. 10 §10.4 y el documento 12 los desarrolla; lo que aquí se cierra
es el mandato sin números—. El **Índice de Salud Ecosistémica (ISE)** ya
dedica un **15 %** de su peso a «Salud del suelo»
(`docs/architecture/metricas_detalle_kpis_oraculos_dinamicos.md`, IN-01) [VERIFICADO] — y ese 15 %
no tenía, hasta este documento, ni un parámetro, ni una unidad, ni una fuente. Un peso sin parámetro
no es un indicador: es un hueco con nombre.

**Qué no es.**

- **No es un estándar de fertilidad agronómica.** Buena parte de la literatura operativa del suelo
  mide **productividad de cultivos**: el factor T del USDA-NRCS y el umbral del 2 % de COS están
  formulados así, con fuente verificada en §14 y **declarados en este documento como proxies
  agronómicos, no como pisos ecológicos** (§4, dimensiones 2 y 3). La frontera entre este documento
  y el 18 (agroecosistemas) es exactamente esa.
- **No es un catálogo de buenas prácticas agrícolas.** Define pisos del ecosistema; no prescribe
  labranza, rotación ni insumos. Donde una práctica aparece (labranza cero, riego), aparece **como
  referencia de umbral**, no como recomendación.
- **No es el estándar de la contaminación del suelo.** La FAO la enumera como la tercera degradación
  química mayor [VERIFICADO] y **no publica en su portal un valor de disparo**; este documento la
  trata como dimensión de umbral binario declarado (§4, dimensión 7) y no la resuelve.
- **No es canon.** Es una propuesta de la rama SDV-E, Ola 4.

**Advertencia de cifras, antes de la primera tabla.** Este documento cita **solo** cifras y URLs
verificadas en la sesión de fuentes de esta rama y registradas en §14 con su estado HTTP. Dos
consecuencias incómodas que el lector debe conocer desde aquí:

1. **Once de las fuentes verificadas son PDF que responden 200 y no se abrieron.** Sus cifras van
   marcadas `[REPORTADO]` y **no sostienen ningún piso de este documento**. Tres de ellas son la
   fuente primaria correcta del dominio del suelo (el manual de macrofauna de la FAO, el informe
   *State of knowledge on soil biodiversity* y el SWSR): **convertirlas en `[VERIFICADO]` es la
   tarea de mayor retorno pendiente de esta rama.**
2. **El dominio del suelo publica sus umbrales casi exclusivamente en PDF.** Eso explica el patrón
   de vacíos de §13 y no debe leerse como ausencia de fuente en el mundo: es una limitación del
   método de esta sesión, declarada.

**Marcas de evidencia usadas en todo el texto.** `[VERIFICADO]` = comprobado con herramienta o leído
en el archivo citado. `[REPORTADO]` = afirmado por una fuente que cito sin haber podido abrir el
documento completo. `[HIPÓTESIS]` = inferencia razonada del proyecto, no observación.
`[SIN FUENTE VERIFICADA — pendiente de consenso científico]` = busqué el umbral y no existe fuente
verificable. Las cuatro marcas son resultados legítimos.

---

## 2. Preámbulo metodológico

El SDV-H lo tiene, el SDV-S lo omitió y el brief de esta biblioteca prohíbe repetir la omisión. En
el suelo el preámbulo no es una formalidad: **el suelo es el ecosistema donde más fácil es escribir
un umbral plausible que no tiene fuente**, porque su literatura operativa nació agrónoma y sus
números sonarán razonables aunque midan otra cosa.

**Regla 1 — Un umbral agrónomico no es un piso ecológico, y se declara cuál es.** El factor T del
USDA-NRCS define la erosión tolerable como *«la cantidad máxima de erosión a la que la calidad de un
suelo **como medio para el crecimiento de las plantas** puede mantenerse»* [VERIFICADO, §14.2]. Es un
umbral de **rendimiento**, no de integridad. El 2 % de COS tiene el mismo vicio de origen: se formuló
para respuesta a fertilizante en suelos tropicales [VERIFICADO, §14.3]. Este documento **usa los dos
como referencia de comparación y no como piso**, y dice en cada tabla cuál de las dos cosas es.

**Regla 2 — El piso y el óptimo van en columnas separadas, siempre.** Es el error que el brief
prohíbe repetir (el motor del SDV-H confundió el Óptimo del agua con el Mínimo Absoluto). En el suelo
la confusión tiene una forma propia y muy concreta: **la «composición de un suelo típico sano» que
publica la FAO** —«varias especies de lombrices, 20-30 especies de ácaros, 50-100 especies de
insectos…» [VERIFICADO, §14.4]— es un **descriptor**, y un descriptor puede ser un Óptimo pero nunca
un piso. Ningún suelo se declara violado por no alcanzar la descripción de otro.

**Regla 3 — Distinguir «no existe» de «no lo sé».** Cuatro cosas distintas se marcan distinto:
(a) no existe en el canon; (b) existe en el canon y no en el código; (c) existe la fuente y no la
pude abrir; (d) busqué y no hay fuente. Las cuatro aparecen en este documento y ninguna se disfraza
de otra. La (c) es la más frecuente aquí y la más fácil de disfrazar: **una cifra vista en un
extracto indexado no es una cifra leída.**

**Regla 4 — Cero invención de constantes físicas.** Este documento necesita convertir milímetros de
suelo a toneladas por hectárea y **no tiene fuente verificada para la densidad aparente** (§13,
pregunta 3). Por eso la conversión se escribe **como fórmula con un parámetro α que la unidad
ecológica debe declarar**, no como una cifra disfrazada de dato. Una constante inventada contamina
todos los umbrales que dependen de ella.

**Regla 5 — LEY y POLÍTICA, explícitas en cada dimensión.** El piso (Mínimo Absoluto) es **LEY** y no
se vota. La plenitud (Óptimo) es **POLÍTICA** y se vota. Precedente del Parlamento Educativo
(INV2-EDU, categoría `critical`: quórum 60 %, consenso 75 %, T13, anti-flip-flop 14 días, `CHECK` en
BD). Cada dimensión de §4 lleva las dos columnas y su frontera declarada.

**Regla 6 — La escalera institucional del suelo no es una metáfora: es el disparador.** La FAO
publica la secuencia **Prevención → Mitigación → Rehabilitación** con su criterio de disparo y su
horizonte temporal [VERIFICADO, §14.2]. Este documento la adopta como **lógica de régimen de INV2-E
en el suelo** (§8), porque es la única escalera del dominio que tiene fuente oficial y coste
declarado.

**Regla 7 — Gobernanza operacionalmente finita (Cap. 10 §10.7).** El SDV-E no puede exigir modelar la
red trófica edáfica completa para decidir. Todo parámetro de este documento es **medible con
instrumento de campo o teledetección** por una comunidad de custodia; lo que no lo sea se declara
como tal y no entra en la fórmula.

---

## 3. Pilares epistemológicos

Cinco pilares sostienen este estándar. Los cuatro primeros son comunes a la familia SDV; el quinto es
el que el suelo aporta a la familia.

1. **Proporcionalidad (Cap. 10 §10.5).** El nivel de protección debe ser *"lógico, proporcional y
   adecuado a la naturaleza de la entidad"*. Un suelo no se protege como se protege una persona: se
   protege **por superficie, por perfil y por tiempo**.

2. **Dignidad encadenada (Cap. 10 §10.6).** *"Dignidad Humana ←→ Dignidad Ecosistémica ←→ Dignidad
   Material. Cada eslabón depende de los demás."* En el suelo esta cadena tiene una cifra: **el 95 %
   del alimento humano se produce en suelos** [VERIFICADO, §14.7] y **el 50-70 % del suelo está
   dedicado a agricultura** [VERIFICADO, §14.7]. El suelo es el eslabón donde la dignidad humana y la
   ecosistémica son literalmente el mismo objeto físico.

3. **Precaución ante quien no puede consentir.** El **Principio Precautorio de Consciencia**
   (Cap. 10 §10.3) y el **T14 — Principio de Precaución Intergeneracional** (Cap. 5): *"Ante
   incertidumbre sobre el impacto en agentes que no pueden consentir (ecosistemas, generaciones
   futuras, posibles consciencias sintéticas), el sistema debe elegir la opción de menor
   irreversibilidad, documentando el costo de oportunidad asumido. La carga de la prueba recae sobre
   quien propone acciones que afectan la temporalidad de no-participantes."* **Es el axioma más
   fuerte de este documento** y el suelo le da su caso más nítido: la FAO declara el suelo **recurso
   no renovable** y estima **más de 1000 años para formar 1 cm** [VERIFICADO, §14.1]. Ninguna
   actividad humana puede justificar bajo T14 la pérdida de un centímetro que no se repone en la
   escala de una civilización.

4. **No-antropocentrismo (T9).** El suelo no es un recurso con propietario: el canon fija *"actuar
   como custodio del patrimonio biológico, no como su propietario"* (Cap. 16.5 §16.5.14). Un
   estándar del suelo que solo mida rendimiento agrícola estaría midiendo al propietario, no al
   sujeto.

5. **El piso puede ser una razón de flujos, no un stock (aporte del suelo a la familia).** Los pisos
   de los otros estándares son concentraciones, cantidades o superficies: PM2.5 ≤ 5 µg/m³, 20 L por
   persona y día, 0,25 m² por gallina. El piso natural del suelo es **una razón entre dos flujos:
   erosión ≤ formación** [VERIFICADO, Montgomery, 2007, §14.1]. Es la formulación más limpia
   disponible de un «caudal ecológico del suelo» —el análogo exacto del caudal mínimo ecológico que
   el canon exige en el Cap. 10 §10.4 para los ríos— y tiene una propiedad que ningún otro piso de
   la familia tiene: **no se puede cumplir degradando despacio mientras se acelera la pérdida.** Por
   eso este documento lo propone como dimensión 1 y como la más resistente a la lógica del crédito
   regenerativo (§9).

**Corolario de honestidad.** El Cap. 16.5 marca el SDV-E y el INV2-E como 🔴 *"próxima gran
ramificación"*. Este documento no cambia ese color: lo detalla, y en §12 dice exactamente qué no
existe. Esta biblioteca es el *estándar primero*; la contabilidad viene después (Cap. 16.5 §16.5.14).

---

## 4. Dimensiones del SDV-E del suelo

> **Cómo se leen las tablas de §4.** «Mínimo Absoluto» es el piso (LEY, no votable); «Óptimo» es la
> plenitud aspiracional (POLÍTICA, votable). **«—» significa que la fuente no define ese extremo**, no
> que exista un cero. Un **valor de estado** —cuánto hay hoy en el mundo, no dónde está el límite—
> **no es un umbral**, y va marcado como tal donde aparece. Cuando un Óptimo numérico no existe con
> fuente, se escribe `[SIN FUENTE VERIFICADA]` en lugar de un número plausible: **es la corrección del
> error del SDV-H con el agua, aplicada dimensión por dimensión.**

### 4.0 De dónde sale esta lista, y por qué tiene este tamaño

No es una lista inventada. Se construye sobre dos listas oficiales que coinciden parcialmente y que
este documento fusiona de forma explícita [VERIFICADO en las dos, §14.2 y §14.6]:

- **La FAO organiza la salud física del suelo en tres componentes**: *ausencia de sellado y
  encostramiento* · *ausencia de erosión* (hídrica y eólica) · *ausencia de compactación*.
- **La Unión Europea enumera ocho amenazas al suelo**: erosión · inundaciones y deslizamientos ·
  pérdida de materia orgánica del suelo · salinización · contaminación · compactación · sellado ·
  pérdida de biodiversidad del suelo.
- **La FAO enumera además tres degradaciones químicas mayores**: minería de nutrientes ·
  salinización · contaminación.

**La fusión, y sus tres decisiones declaradas:**

| Decisión | Qué se hizo | Por qué |
|---|---|---|
| **Se ordena por el carbono** | El eje del estándar es el COS (dimensión 2), no un promedio de siete procesos | La FAO declara que el carbono del suelo *«trasciende las tres categorías de indicadores (química, física, biológica) y tiene la influencia más ampliamente reconocida sobre la calidad del suelo, pues está ligado a todas las funciones del suelo»* [VERIFICADO, §14.3] |
| **Se retiran las inundaciones y deslizamientos** | No son dimensión de este documento | Son procesos de **otros** ecosistemas (cuenca, montaña) que el canon ya manda proteger por sección propia (Cap. 10 §10.4, ciclos naturales). Contarlos aquí dos veces los contaría como compensables entre sí |
| **Se separan las dimensiones ponderadas de las binarias** | 7 dimensiones ponderadas + **2 binarias sin peso** (sellado y Zona Libre) | El sellado es irreversible y el piso y el óptimo coinciden en 0: ponderarlo lo haría canjeable contra el piso. Precedente: dimensiones VIII y IX del SDV-H (Cap. 8 §8.11) |

**Las nueve piezas del estándar, y su estado de fuente.** Cuatro tienen umbral numérico con fuente
verificada (las dimensiones 1 y 4, más el sellado y la Zona Libre, que son **políticas o doctrinales**,
no científicas); una tiene un proxy agronómico declarado como tal (el COS); y las **cuatro** restantes
no tienen ningún umbral publicado. El 🔴 de esta tabla **es el resultado del documento**, no un defecto
de redacción.

| # | Dimensión | Proceso FAO/UE que la origina | ¿Umbral con fuente verificada? |
|---|---|---|---|
| 1 | Balance erosión ≤ formación | Erosión (FAO física; UE amenaza 1) | 🟢 **Sí** — Montgomery, 2007 *(un balance, no un valor tolerable: la FAO no publica valor)* |
| 2 | Carbono orgánico del suelo | Pérdida de materia orgánica (UE amenaza 3) | 🟡 **Parcial** — 2 % COS, proxy agronómico |
| 3 | Biodiversidad edáfica y macrofauna | Pérdida de biodiversidad del suelo (UE amenaza 8) | 🔴 **No** — solo descriptores |
| 4 | Salinidad y sodicidad | Salinización (FAO química; UE amenaza 4) | 🟢 **Sí** — FAO GSASmap, 2021 |
| 5 | Compactación y degradación física | Compactación y encostramiento (FAO física; UE amenaza 6) | 🔴 **No** |
| 6 | Minería de nutrientes | Minería de nutrientes (FAO química) | 🔴 **No** |
| 7 | Contaminación del suelo | Contaminación (FAO química; UE amenaza 5) | 🔴 **No** |
| **B1** | **Sellado del suelo** *(binaria, sin peso)* | Sellado (FAO física; UE amenaza 7) | 🟢 **Sí, político** — sellado neto cero |
| **B2** | **Zona Libre del suelo** *(binaria, sin peso)* | — (Cap. 7 §7.9 · Cap. 16.5 §16.5.14) | 🟢 **Sí, doctrinal** |

---

### Dimensión 1: Balance erosión ≤ formación (el caudal ecológico del suelo)

**Qué protege.** Que el suelo no se pierda más rápido de lo que se forma: el balance entre la pérdida
de suelo y su producción.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **Razón erosión / formación (E/P)** | **E/P ≤ 1** — la erosión no supera la tasa de formación del suelo | **[SIN FUENTE VERIFICADA] como número.** La fuente solo dice que la labranza cero lleva la pérdida *«sorprendentemente cerca de estar equilibrada con la creación de suelo»*, es decir **E ≈ P**: un valor **igual al del piso**, no una décima parte de él | Montgomery, 2007 (PNAS 104(33), doi 10.1073/pnas.0611508104; cifra leída en la nota institucional de la Univ. de Washington, 2007) [VERIFICADO] |
| Tasa de formación de suelo, referencia mundial (P) | **< 0,1** mm/año — promedio mundial de la erosión a largo plazo, *«similar a la tasa a la que se produce el suelo»* por procesos mecánicos, químicos y biológicos | — *(valor de estado de referencia mundial, no un Óptimo aspiracional; el Óptimo de un balance es E/P → 0)* | Montgomery, 2007 [VERIFICADO] |
| Tasa de formación de perfil, referencia de largo plazo | **> 1000 años por cm** de suelo; el suelo es **recurso no renovable** | — *(referencia de estado del recurso, no un Óptimo)* | FAO, 2017 [VERIFICADO] |
| Razón E/P bajo agricultura convencional *(valor de estado, no umbral)* | — | **10 a 100 ×** | Montgomery, 2007 [VERIFICADO] |
| Tasa de erosión en terreno alpino escarpado *(referencia alta)* | — | **> 1** mm/año solo de forma consistente en terreno alpino escarpado | Montgomery, 2007 [VERIFICADO] |
| **Conversión mm ↔ t/ha (parámetro α, obligatorio)** | — | `1 mm de suelo sobre 1 ha = 10 · α t/ha`, con **α = densidad aparente en g/cm³** | **[HIPÓTESIS] aritmética de este documento** — α **no tiene fuente verificada** (§13, pregunta 3): la constante es del proyecto, **no un dato** `[SIN FUENTE VERIFICADA]` |
| **Factor T del USDA-NRCS** *(referencia de comparación, NO es el piso)* | **1** en suelos delgados o frágiles · **5** en suelos profundos | — | USDA-NRCS, *National Soil Survey Handbook* 430-VI [VERIFICADO] |
| Equivalencia métrica del factor T *(conversión propia)* | ≈ **2,24** a ≈ **11,2** t/ha/año (1 ton/acre = 2,2417 t/ha) | — | **[HIPÓTESIS] conversión aritmética de este documento**; la fuente **no** da el valor métrico |

**Justificación.** El piso es **E/P ≤ 1** y no el factor T, por tres razones que se sostienen juntas:

1. **T mide otra cosa.** Su definición oficial es la erosión máxima a la que se mantiene *«la calidad
   de un suelo **como medio para el crecimiento de las plantas**»* [VERIFICADO]. Adoptar T como piso
   sería repetir exactamente el error que el brief §2.1 prohíbe (confundir el Óptimo del agua con el
   Mínimo Absoluto): tomar un umbral de productividad y llamarlo integridad.
2. **T es un rango de 5×, no un piso.** 1 frente a 5 ton/acre/año —de 2,24 a 11,2 t/ha/año en
   conversión propia— es una horquilla de planificación de finca; un piso de ley no puede valer cinco
   veces más en el suelo de al lado.
3. **El balance sí tiene fuente y sí tiene la forma doctrinal correcta.** Montgomery (2007) da el
   criterio: la erosión **no debe superar la tasa de formación del suelo**, y documenta que las
   prácticas de largo plazo *«parecen incrementar la erosión del suelo hasta el punto de que **no es
   compensada por la creación de suelo**»* [VERIFICADO]. Es una razón entre dos flujos medibles, y
   **es estrictamente más exigente que T**: con P de referencia < 0,1 mm/año —que son ≈ 1,3 t/ha/año
   solo si se declara un α de ≈ 1,3 g/cm³, y esa conversión es de este documento—, un suelo que
   perdiera 2 t/ha/año podría estar dentro de T y por encima de su formación.

**Advertencia de honestidad sobre la unidad del piso.** El piso `E/P ≤ 1` **exige medir P en el
sitio**. No se puede evaluar contra una constante mundial, porque la formación varía con clima,
litología, relieve y biota, y este documento **no tiene fuente verificada para una tabla de P por
tipo de suelo**. Consecuencia declarada: mientras P no se mida localmente, el balance no es
auditable, y **la ausencia de dato no autoriza a declarar cumplimiento** (ver la inversión del
principio «sin dato no castiga» para el Reino Natural: documento 09 de esta biblioteca, insight I9).
La salida operativa `[HIPÓTESIS]`: si P no se mide, se usa P = 0,1 mm/año como **referencia
declarada** y el balance se reporta como **provisional**, no como cumplido.

**Protocolo.**

- **P (formación):** perfil de referencia y datación del horizonte superficial; a falta de datación,
  **P declarada con método y α explícitos** y marcada provisional. Frecuencia: cada ciclo de revisión
  del mandato ecológico (3-5 años, documento 40).
- **E (pérdida):** estacas de erosión (erosion pins), perfil de suelo comparado contra una parcela de
  referencia no perturbada, o teledetección de surcos y cárcavas. La FAO declara la erosión como
  **identificable por teledetección** únicamente en su componente de sellado [VERIFICADO]; para
  erosión laminar la teledetección **no basta** y hace falta suelo [HIPÓTESIS].
- **Conversión a masa:** obligatorio declarar α (densidad aparente del horizonte considerado). Sin α
  declarada, el balance se reporta **solo como razón adimensional** `E/P`, nunca en t/ha.
- **Quién reporta:** la comunidad de custodia del mandato ecológico, con la parte `eco-` como
  destinataria. El guardián oráculo **consiente, no mide**.
- **Frecuencia:** anual para E (es el proceso más rápido), con la revisión del piso cada 3-5 años.
- **Ciclos de disturbio:** si la unidad tiene **régimen de fuego o de inundación**, el registro debe
  declararlo **antes** de calcular `E/P` (§4.1): una avenida deposita, y contarla como erosión
  invertiría el signo del balance.

**Violación.** Constituye violación, como hecho observable y no como opinión:

- **V1.** `E/P > 1` medida en la unidad ecológica durante un ciclo de medición completo, con E y P
  declaradas y α declarada; o
- **V2.** pérdida de espesor del horizonte superficial **superior a la formación declarada** en el
  mismo periodo, aunque el valor absoluto parezca pequeño; o
- **V3.** **cárcavas o surcos con avance medido** dentro de la unidad, con o sin razón calculada: una
  cárcava es pérdida concentrada, no laminar, y `E/P ≤ 1` en promedio la ocultaría.

---

### Dimensión 2: Carbono orgánico del suelo (la memoria viva del perfil)

**Qué protege.** El carbono orgánico del suelo —el reservorio que regula la estructura, la retención
de agua, el ciclo de nutrientes y la vida edáfica.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **Umbral crítico de COS** *(proxy agronómico)* | **2 % COS** — *«ampliamente sugerido en torno a 2 %, por debajo del cual puede ocurrir deterioro»* | [SIN FUENTE VERIFICADA] | Musinguzi *et al.*, 2013 (*Journal of Sustainable Development*), registro FAO **AGRIS** [VERIFICADO] |
| **Rango crítico por tipo de suelo** | **0,5 % COS** (en algunos suelos, niveles tan bajos como 0,5 % dan respuesta a fertilizante) | [SIN FUENTE VERIFICADA] | Musinguzi *et al.*, 2013 (AGRIS) [VERIFICADO] |
| Umbral del 2 % COS, segunda fuente | **2 % COS** (*«el umbral inferior del 2 % de carbono orgánico del suelo ha sido usado ampliamente»*, citando Kemper y Koch, 1966, y Greenland *et al.*) | — | Informe del **JRC** (Comisión Europea) `[REPORTADO]` — cifra vista en extracto indexado, **PDF no abierto** |
| **Conclusión de la fuente sobre un umbral universal** | *«Sigue siendo difícil establecer un único valor umbral de COS mínimo o máximo que pueda ser aceptado universal o regionalmente»* | — | Musinguzi *et al.*, 2013 [VERIFICADO] — **la fuente misma niega el escalar universal** |
| **Instrumento de medida global** | — | Capas ráster en **t C/ha** (GSOCmap), licencia CC BY; mapa de potencial de secuestro (GSOCseq) | FAO, Global Soil Partnership [VERIFICADO] |
| Indicador de COS en la UE *(stock)* | — | *«Los stocks estimados de carbono orgánico del suelo se reportan en toneladas por hectárea»* — indicador C.41 de la PAC | JRC / EU Soil Observatory [VERIFICADO] |
| Factor de conversión MOS ↔ COS *(1,724)* | `[SIN FUENTE VERIFICADA]` | — | **no verificado en esta sesión**; este documento **no lo usa** |

**Justificación, y es una justificación de segundo orden.** Este documento **no puede** declarar el
2 % de COS como piso ecológico, y dice por qué:

1. **La fuente que da el 2 % niega su universalidad en el mismo documento.** No es una objeción
   externa: es la conclusión de Musinguzi *et al.* (2013) [VERIFICADO]. Un piso de ley construido
   sobre una cifra que su propio autor declara no universal sería un piso sin fuente, disfrazado.
2. **El 2 % es un umbral de fertilidad, no de integridad.** Está formulado para respuesta a
   fertilizante en agroecosistemas tropicales; un suelo forestal, un histosol de turba o un andosol
   volcánico no se describen con esa vara. Un piso único **destruiría** la dimensión, que es
   exactamente lo que el Cap. 8 §8.11 advierte sobre medir lo inconmensurable con la misma vara.
3. **Un suelo no se viola por tener poco carbono absoluto, sino por perder el suyo.** Un arenosol
   natural con 0,4 % de COS puede estar intacto; un chernozem con 3 % que perdió la mitad de su
   carbono está degradado y por encima del umbral.

**Por eso el piso operativo es un déficit normalizado contra línea base propia** `[HIPÓTESIS]` —
propuesta de este documento, no ratificada— y el 2 % entra **solo como disparador de revisión**:

```
déficit_COS = ( [COS]_línea_base − [COS]_actual ) / [COS]_línea_base
```

- **LEY:** la pérdida de COS respecto de la línea base de la propia unidad, y la obligación de
  declarar esa línea base antes de cualquier contrato que afecte al suelo.
- **POLÍTICA (votable, `critical`):** el valor de disparo del déficit y la definición de la línea
  base de cada unidad ecológica. El 2 % de COS y el 0,5 % operan aquí, **como referencias de
  revisión agronómica declaradas como tales**, no como piso.
- **Instrumento obligatorio:** el GSOCmap da la capa global de stock en t C/ha [VERIFICADO], y el
  JRC/EUSO publica el indicador de stock en t C/ha [VERIFICADO]. **Ninguno de los dos se abrió para
  leer una cifra de referencia por tipo de suelo**: por eso la línea base debe medirse en la unidad,
  no importarse (§13, pregunta 2).

**Protocolo.**

- **Muestra:** suelo del horizonte superficial (0-30 cm) y, cuando exista horizonte orgánico, su
  espesor completo. Muestreo compuesto por transecto, georreferenciado y repetible en el mismo punto.
- **Método:** análisis de carbono orgánico por combustión seca en laboratorio; **el método debe
  declararse** (no se fija aquí, y la conversión MOS↔COS no está verificada: no se usa).
- **α obligatoria:** para expresar el resultado en t C/ha hace falta densidad aparente, que **no
  tiene fuente verificada** (§13, pregunta 3). Sin α, el resultado se reporta **solo en % COS**.
- **Frecuencia:** cada 3-5 años (el COS cambia despacio; medirlo cada año gasta más de lo que
  informa) [HIPÓTESIS].
- **Quién reporta:** laboratorio independiente sobre muestreo de la comunidad de custodia. T13: la
  contabilidad nunca se borra; **la línea base no se re-negocia después de medir**.

**Violación.**

- **V1.** `déficit_COS` superior al disparo votado, medido contra una línea base **declarada antes**
  del contrato, con dos mediciones comparables (mismo método, misma α, mismo punto).
- **V2.** **Ausencia de línea base declarada** en una unidad ecológica sometida a un contrato que
  afecta al suelo. No es violación del suelo: es **condición de invalidez del contrato**
  (documento 09, insight I9: la opacidad no castiga al sujeto medido, obliga a quien mide).
- **V3.** Uso de una cifra de COS **sin método declarado** como prueba de cumplimiento.

---

### Dimensión 3: Biodiversidad edáfica y macrofauna (los ingenieros del perfil)

**Qué protege.** La comunidad viva del suelo —microorganismos, mesofauna y macrofauna— que produce
la estructura, la porosidad y el reciclaje de nutrientes de los que depende todo lo demás.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **Riqueza de invertebrados en suelo forestal** *(descriptor)* | — | **> 1000** especies por m² | FAO, Soils Portal — *Soil biodiversity: facts and figures* [VERIFICADO] |
| **Composición de un suelo típico sano** *(descriptor; la FAO escribe «a typical, healthy soil»)* | — | varias especies de lombrices · 20-30 especies de ácaros · 50-100 especies de insectos · decenas de nematodos · cientos de hongos · quizás miles de bacterias y actinomicetos | FAO, Soils Portal — *Facts and figures* [VERIFICADO] — **única definición de «suelo sano» con fuente oficial encontrada en esta sesión** |
| **Biomasa de lombrices en suelo agrícola** | — | **≈ 3000** kg/ha (equivalente a seis animales grandes) | FAO, C-RESAP, *Soil biology and agriculture*, Module 3 `[REPORTADO]` — **PDF no abierto** |
| Densidad de bacterias | — | millones de individuos y varios miles de especies por gramo | FAO, Soils Portal [VERIFICADO] |
| **El suelo como reservorio de biodiversidad planetaria** | — | **un cuarto (25 %)** de la biodiversidad del planeta | FAO, 2017 [VERIFICADO] |
| **Umbral numérico de lombrices (individuos/m²) o índice biótico** | **[SIN FUENTE VERIFICADA — pendiente de consenso científico]** | [SIN FUENTE VERIFICADA] | la FAO publica **composición y biomasa, ningún valor de disparo** |
| Protocolo de campo de macrofauna | — | transecto estándar **TSBF** (*Soil macrofauna field manual*) | FAO `[REPORTADO]` — PDF 200, **no abierto** |
| Estado del conocimiento | — | *State of knowledge on soil biodiversity: status, challenges and potentialities* (informe principal, FAO 2020) y su resumen para responsables de política | FAO `[REPORTADO]` — PDF no abierto |
| **Definición FAO de biodiversidad del suelo** | — | *«La variabilidad entre organismos vivos, incluida la miríada no visible a simple vista —microorganismos y mesofauna— así como la macrofauna más familiar (lombrices y termitas). Las raíces pueden considerarse organismos del suelo por sus relaciones simbióticas»* | FAO, Soils Portal — *Soil biodiversity* [VERIFICADO] |
| Función declarada de los organismos del suelo | — | *«Agentes impulsores primarios del ciclo de nutrientes, regulan la dinámica de la materia orgánica del suelo, el secuestro de carbono y la emisión de GEI, modifican la estructura física y los regímenes hídricos»* | FAO, Soils Portal [VERIFICADO] |

**Justificación.** Esta es la dimensión donde este documento **se niega a fabricar un umbral**, y la
negativa es el contenido:

1. **La FAO no publica un piso de biodiversidad del suelo.** Publica descriptores de un suelo sano.
   Un descriptor no es un umbral de disparo: **ningún suelo se declara violado por no alcanzar la
   descripción de otro suelo.** Convertir «> 1000 especies/m²» en piso sería legislar una cifra que
   nadie publicó como ley.
2. **La biomasa de 3000 kg/ha de lombrices es `[REPORTADO]`, y además es agrícola.** No sostiene un
   piso general del reino, y su PDF no se abrió. **No se usa como piso.**
3. **Modelar la red trófica edáfica completa violaría el Cap. 10 §10.7** (*«la gobernanza debe ser
   operacionalmente finita»*). El suelo contiene un cuarto de la biodiversidad del planeta
   [VERIFICADO]: ningún mandato ecológico puede auditar eso en un ciclo de contrato.
4. **Por eso el piso es binario y de orden de magnitud** `[HIPÓTESIS]`: **presencia de macrofauna
   observable (lombrices o termitas) en un transecto estándar**, más la obligación de repetir el
   mismo transecto en el tiempo. No un índice: un hecho.

**Y hay un segundo argumento, que es de mecanismo y no de prudencia.** La macrofauna **construye la
porosidad por la que entra el agua y crece la raíz**: la FAO documenta una galería de lombriz
*«llena de excrementos y una raíz siguiendo el camino abierto por la lombriz»* [VERIFICADO], y que la
labranza *«reduce el número de hifas fúngicas, porque los agregados del suelo, que se mantienen
unidos por estas hifas, se rompen»* [VERIFICADO]. Es decir: **la bioturbación es el mecanismo físico
que une esta dimensión con la 1 (infiltración ↔ erosión) y con la 5 (compactación)**. Medir la
macrofauna no es un adorno de biodiversidad: es medir el instrumento que produce las otras dos.

**Protocolo.**

- **Transecto de macrofauna** siguiendo el protocolo de campo estándar del dominio (**TSBF**, FAO,
  *Soil macrofauna field manual*) `[REPORTADO]` — **el documento no se abrió en esta sesión**: el
  protocolo se nombra, no se transcribe.
- **Unidad de reporte:** presencia/ausencia por transecto y **orden de magnitud** (presencia dispersa
  · presencia generalizada · ausencia total), con el número de monolitos o parcelas declarado.
- **Frecuencia:** anual o por estación de crecimiento, en el mismo transecto y la misma fecha
  relativa del año (la macrofauna es estacional) [HIPÓTESIS].
- **Quién reporta:** comunidad de custodia, con verificación por tercero (ciencia ciudadana
  admitida; T13 registro completo de fotografía y fecha).
- **Lo que NO se hace:** índice biótico agregado, abundancia por m², ni curva de especies. Todo eso
  **no tiene fuente verificada en esta sesión** y construir el instrumento antes de la fuente sería
  invertir el orden canónico (*"estándar primero, contabilidad después"*).

**Violación.**

- **V1. Ausencia total de macrofauna en el transecto estándar** de una unidad ecológica cuyo estado
  de referencia documentado la tenía — hecho observable, foto y fecha, con T13.
- **V2.** Ausencia **repetida** de macrofauna en el mismo transecto y la misma estación durante el
  número de ciclos que fije la política (candidato de diseño `[HIPÓTESIS]`: **tres ciclos
  consecutivos**, por analogía con el umbral de retractación a 7 ciclos del SDV-S, Cap. 9.5
  §9.5.10). No es un piso numérico: es un contador con umbral, como manda el documento 09 (§8).
- **Lo que NO es violación:** tener menos de 1000 especies/m², o menos biomasa de lombrices que
  3000 kg/ha. **Esos son Óptimos descriptivos, y tratarlos como piso sería el error del SDV-H.**

---

### Dimensión 4: Salinidad y sodicidad (la acumulación que no se degrada)

**Qué protege.** Que las sales no se acumulen hasta el punto en que el suelo deja de sostener vida
vegetal y se vuelve prácticamente irrecuperable.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **Salinidad del suelo** | **CEe > 2 dS/m** — el umbral por encima del cual el suelo deja de clasificarse como no salino *(es un criterio de clasificación del GSASmap, no un piso de manejo: ninguna CEe positiva es buena)* | [SIN FUENTE VERIFICADA] | FAO, **GSASmap V1.0.0** (Global Map of Salt-affected Soils), Global Soil Partnership, 2021 [VERIFICADO] |
| **Sodicidad del suelo** | **ESP > 15 %** (porcentaje de sodio intercambiable) | [SIN FUENTE VERIFICADA] | FAO, GSASmap V1.0.0, 2021 [VERIFICADO] |
| **pH del suelo** *(tercer criterio del GSASmap, **acompaña**, no dispara solo)* | **pH > 8,2** | [SIN FUENTE VERIFICADA] | FAO, GSASmap V1.0.0, 2021 [VERIFICADO] |
| **Origen dominante declarado** | — | *«La salinización ocurre generalmente por sistemas de riego mantenidos de forma inadecuada»* | FAO, Soils Portal — *Soil health: biological and chemical* [VERIFICADO] |
| **Discrepancia abierta con la literatura clásica** | `[SIN FUENTE VERIFICADA]` el umbral de **4 dS/m** del sistema Richards | — | **no verificado en esta sesión**: todas las rutas encontradas son PDF. **Este documento NO escribe 4 dS/m** |
| Superficie afectada por sales *(estado global)* | — | **> 424 millones ha** (0-30 cm) · **> 833 millones ha** (30-100 cm); **> 3 %** y **> 6 %** del suelo global | FAO, GSASmap V1.0.0, 2021 (118 países —85 % de la superficie terrestre global—, 257 419 puntos medidos) [VERIFICADO] |
| Composición de las tierras afectadas *(estado)* | — | 85 % salinas · 10 % sódicas · 5 % salino-sódicas (superficial); 62 % / 24 % / 14 % (subsuelo) | FAO, GSASmap [VERIFICADO] |
| Localización climática *(estado)* | — | 37 % en desiertos áridos · 27 % en estepa árida → **dos tercios en zonas áridas y semiáridas** | FAO, GSASmap [VERIFICADO] |

**Justificación.** Esta es la dimensión del suelo con **umbral oficial más limpio** —tres criterios
publicados, un mapa global, un umbral de clasificación inequívoco— y a la vez la que exige la
advertencia más fuerte de este documento:

1. **La discrepancia del 4 dS/m se declara, no se resuelve inventando.** El GSASmap usa **CEe > 2
   dS/m** [VERIFICADO]; la literatura clásica de suelos salinos usa 4 dS/m y **este documento no lo
   pudo verificar**. Se usa **2 dS/m** porque es el valor verificado de la FAO, y **se declara la
   discrepancia** en §13. Escribir 4 dS/m «porque es lo conocido» sería exactamente la invención que
   el brief prohíbe.
2. **Las sales no se degradan: se acumulan o se lavan.** No hay proceso biológico que las destruya.
   `[HIPÓTESIS]`: es el **candidato más fuerte a umbral duro** del SDV-E del suelo, por su
   irreversibilidad bajo T14 — y la FAO ya dio la definición operativa de irreversibilidad:
   desertificación es *«el cambio **irreversible** de la tierra a un estado en el que ya no puede
   recuperarse para su uso original»* [VERIFICADO].
3. **Acoplamiento con el documento 17 (zonas áridas):** dos tercios de la superficie afectada por
   sales está en zonas áridas y semiáridas [VERIFICADO]. La salinidad es la dimensión que **cruza**
   suelo y aridificación, y la única del suelo que este documento puede declarar con umbral duro sin
   discusión de fuente.
4. **Cuidado con el sujeto:** el umbral de clasificación es del **suelo**, y su consecuencia es sobre
   la vida vegetal y la biota. Este documento **no** propone un umbral de salinidad del agua de
   riego: eso pertenece al 23 (agua) y sería trasvasar un umbral entre sujetos, lo que el documento
   09 prohíbe expresamente.

**Protocolo.**

- **CEe** (conductividad eléctrica del extracto de pasta saturada) y **ESP**, en laboratorio de
  suelo, sobre muestras compuestas georreferenciadas, en **dos profundidades** (0-30 cm y 30-100 cm):
  el GSASmap distingue horizonte superficial y subsuelo y las dos superficies difieren en un factor
  de dos [VERIFICADO].
- **pH** en la misma muestra, como tercer criterio.
- **Frecuencia:** anual en unidades con riego o en zona árida (es la vía de entrada dominante
  declarada por la FAO); cada 3-5 años en el resto [HIPÓTESIS].
- **Escala válida:** la unidad ecológica y su cuenca de riego. La FAO advierte que los balances
  específicos son de utilidad **local y regional** [VERIFICADO] — un valor global de salinidad no
  describe ningún suelo concreto.
- **Quién reporta:** laboratorio independiente; datos de riego aportados por la parte que riega (con
  obligación de declararlos: es la actividad que la FAO señala como causa dominante).

**Violación.**

- **V1.** `CEe > 2 dS/m` **o** `ESP > 15 %` medidos en el mismo horizonte, con laboratorio y fecha
  declarados, en una unidad ecológica cuyo estado de referencia no era salino. El **pH > 8,2** se
  exige además como **criterio de clasificación acompañante** del GSASmap `[HIPÓTESIS]`: este
  documento **no lo usa como disparador único**, porque hay suelos naturalmente alcalinos o
  calcáreos —intactos y no salinos— con pH por encima de 8,2, y declararlos violados sería declarar
  violado un ecosistema que no lo está (documento 09, principio de la regla de ámbito).
- **V2.** **Tendencia sostenida de aumento de CEe** durante los ciclos que fije la política, aunque
  el valor absoluto siga por debajo de 2 dS/m: la salinidad es acumulativa y su tendencia es la señal
  temprana. `[HIPÓTESIS]` — la tendencia como hecho observable, con las series publicadas en T13.
- **V3.** **Aplicación de riego sin monitoreo de sales declarado** en unidad de zona árida o
  semiárida. No es violación del suelo: es **condición de invalidez del contrato de riego**
  [HIPÓTESIS], por el mismo principio que V2 de la dimensión 2.

---

### Dimensión 5: Compactación y degradación física (el suelo que deja de ser poroso)

**Qué protege.** Que el suelo conserve la porosidad por la que entran el aire, el agua y las raíces:
la ausencia de compactación y de encostramiento superficial.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **Densidad aparente crítica / densidad limitante para raíces** | **[SIN FUENTE VERIFICADA — pendiente de consenso científico]** | [SIN FUENTE VERIFICADA] | **segundo intento fallido**: ya lo era en `09_comparativa.md`. La FAO describe la compactación **cualitativamente** y no publica valor; el archivo histórico que contenía la tabla devolvió **HTTP 500** |
| Resistencia a la penetración / umbral numérico | **[SIN FUENTE VERIFICADA]** | [SIN FUENTE VERIFICADA] | no encontrada |
| **Definición de los tres componentes de la salud física del suelo** | — | (1) **ausencia de sellado y encostramiento** · (2) **ausencia de erosión** (hídrica y eólica) · (3) **ausencia de compactación** | FAO, Soils Portal — *Soil health: physical* [VERIFICADO] |
| **Efecto de la compactación** | — | *«A menudo resultan en la creación de **capas de suelo impermeables** cerca de la superficie y encharcamiento local»* | FAO, Soils Portal [VERIFICADO] |
| **Causas declaradas** | — | concentración fuerte de ganado (en climas secos, alrededor de puntos de agua) y uso de **maquinaria pesada y prácticas de labranza inapropiadas** | FAO, Soils Portal [VERIFICADO] |
| **Encostramiento superficial (*crusting*)** | — | *«Fenómeno local en la superficie del suelo que resulta en una **capa delgada impermeable** que dificulta la emergencia de plántulas, reduce la infiltración y favorece la escorrentía y la erosión»* | FAO, Soils Portal [VERIFICADO] |
| Deterioro de la estructura como indicador | — | *«Mejorar la estructura del suelo para aumentar la calidad del hábitat para la biota del suelo y los cultivos»* | JRC, EU Soil Observatory [VERIFICADO] |

**Justificación, y es la admisión central de este documento.** La FAO define la compactación como
**uno de los tres componentes de la salud física del suelo** y **no publica un valor de disparo**
[VERIFICADO]. Este documento **no fabrica uno**, por tres razones:

1. **No es un vacío de búsqueda: es un vacío verificado dos veces.** El umbral de densidad aparente
   ya faltaba en el documento 09 de esta biblioteca y vuelve a faltar aquí, con un intento directo
   fallido (el archivo histórico devolvió **500**). Declararlo es más honesto que rellenarlo.
2. **Una densidad aparente crítica no es una constante: depende del tipo de suelo y de la
   textura.** Un valor único para todos los suelos sería el mismo error que el 2 % universal de COS
   (dimensión 2), que su propia fuente niega.
3. **La compactación se puede detectar sin umbral numérico, como hecho.** La FAO describe el efecto
   observable —capas impermeables cerca de la superficie, encharcamiento local, costra superficial
   que impide la emergencia de plántulas y **favorece la escorrentía y la erosión** [VERIFICADO]— y
   ese efecto es un hecho observable con pala, agua y fotografía.

**Por eso esta dimensión entra a la fórmula con un indicador de estructura, no con un número**
`[HIPÓTESIS]`: presencia/ausencia declarada de (a) costra superficial, (b) capa compactada
identificada en perfil, (c) encharcamiento local persistente no explicado por el relieve ni por el
régimen de lluvia. Es un **indicador binario de tres componentes**, auditable con T13 (perfil
fotografiado, fecha, profundidad).

**Y una consecuencia de acoplamiento que este documento declara:** la costra superficial *«favorece
la escorrentía y la erosión»* [VERIFICADO] y la compactación destruye la porosidad que la macrofauna
(dimensión 3) construye. Es decir: **la dimensión 5 es a la vez causa y consecuencia de las
dimensiones 1 y 3**. Por eso este documento **no la pondera como si fuera independiente** (§5): en la
fórmula entra con el peso menor de las siete, y su función principal es **diagnóstica** —dice *por
qué* está fallando el balance de la dimensión 1, no cuánto.

**Protocolo.**

- **Perfil de suelo** en calicata o barreno, con fotografía escalada, a dos profundidades.
- **Prueba de infiltración** en campo (tiempo de entrada de un volumen conocido de agua), comparada
  contra la parcela de referencia de la misma unidad: la referencia interna evita necesitar el umbral
  que no existe.
- **α (densidad aparente)** medida en la misma campaña: es el parámetro que este documento necesita
  para la dimensión 1 y **no tiene fuente**; medirla aquí no resuelve el vacío doctrinal, pero cierra
  el dato de la unidad.
- **Frecuencia:** anual donde haya maquinaria pesada, ganadería concentrada o riego; cada 3-5 años en
  el resto [HIPÓTESIS].
- **Quién reporta:** comunidad de custodia; **la parte que opera la maquinaria pesada declara su
  paso** (la FAO nombra la maquinaria y la labranza como causas [VERIFICADO]).

**Violación.**

- **V1.** **Costra superficial presente** con infiltración medida sustancialmente menor que la
  parcela de referencia de la misma unidad, en la misma campaña.
- **V2.** **Capa compactada identificada en perfil** por debajo del horizonte arable, con fotografía
  y profundidad registradas (T13).
- **V3.** **Encharcamiento local persistente** tras lluvia o riego, no explicado por el relieve ni
  por el régimen hídrico, con registro de fechas.
- **Lo que NO es violación:** superar un valor de densidad aparente, **porque ese valor no existe con
  fuente**. Declarar violación contra un número no publicado sería ley sin fuente.

---

### Dimensión 6: Minería de nutrientes (solo donde la FAO dice que aplica)

**Qué protege.** Que el suelo no se vacíe de los nutrientes que exportan las cosechas sin
reposición — y **solo en el ámbito donde ese agotamiento existe**.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **Ámbito de aplicación (regla de la FAO)** | *«La minería de nutrientes **solo se considera en áreas agrícolas**. **No se espera agotamiento de nutrientes bajo otros usos del suelo** (silvicultura, pastos)»* | — | FAO, Soils Portal — *Soil health: biological and chemical* [VERIFICADO] — **crucial: el umbral de nutrientes NO aplica al suelo silvestre** |
| **Escala de aplicación válida** | *«Estudios específicos sobre balances de nutrientes son de particular utilidad **a escala local y regional**»* (no global) | — | FAO, Soils Portal [VERIFICADO] |
| **Umbral numérico de balance de nitrógeno (kg N/ha/año)** | **[SIN FUENTE VERIFICADA — pendiente de consenso científico]** | [SIN FUENTE VERIFICADA] | no encontrado. El indicador AE21/CAP y el informe del JRC dan **estado, no umbral**, y los PDF no se abrieron. El documento metodológico de balances de la FAO (*Assessment of soil nutrient balance*, Fertilizer and Plant Nutrition Bulletin #14) **está muerto en sus dos rutas (404)** |
| **Las tres degradaciones químicas mayores** | — | (1) minería de nutrientes · (2) salinización · (3) contaminación | FAO, Soils Portal [VERIFICADO] |
| **Frontera planetaria de flujos biogeoquímicos** | — | **Transgredida en ambas variables de control** (nitrógeno y fósforo) | Stockholm Resilience Centre, Planetary Health Check 2026 [VERIFICADO] |
| **Mecanismo de pérdida de fósforo** | — | *«El fósforo se acumula en los suelos y se libera a las aguas superficiales **vía erosión del suelo y escorrentía superficial**»* | Stockholm Resilience Centre, 2026 [VERIFICADO] — **enlaza nutrientes con erosión (dimensión 1)** |
| **Meta global de respuesta** | — | **≥ 50 %** de reducción del exceso de nutrientes al ambiente para 2030 | CBD, Marco Kunming-Montreal, **Meta 7** (2022) [VERIFICADO] |
| Efecto de la pérdida de bosque sobre el suelo | — | *«Sin esta protección natural, los suelos pueden lavarse, perder fertilidad y tardar décadas en recuperarse»* | Stockholm Resilience Centre, 2026 [VERIFICADO] |
| Causa directa del cambio de uso del suelo | — | agricultura y ganadería juntas: **casi el 90 %** de la pérdida forestal reciente | Stockholm Resilience Centre, 2026 [VERIFICADO] |

**Justificación.** Esta dimensión es la que **este documento restringe en lugar de expandir**, y esa
restricción es una decisión doctrinal:

1. **La FAO dice explícitamente que el agotamiento de nutrientes no se espera fuera de la
   agricultura** [VERIFICADO]. Aplicar un umbral de nutrientes a un suelo forestal o a un pastizal
   sería **inventar un umbral donde la FAO dice que no corresponde**, y con ello declarar violados
   ecosistemas intactos.
2. **La escala válida es local y regional** [VERIFICADO]. Un umbral global de balance de nitrógeno no
   existe por diseño, no por falta de búsqueda — y la ruta oficial del método de balances de la FAO
   está muerta (404) en sus dos direcciones.
3. **La dimensión entra al SDV-E del suelo con ámbito declarado y no como piso universal.**
   Pertenece primariamente al documento 18 (agroecosistemas), que es donde su sujeto vive. Aquí se
   registra porque **el mismo proceso exporta el nutriente que eutrofiza el agua** cuando el suelo se
   erosiona [VERIFICADO]: es el acoplamiento erosión → eutrofización, y es la razón por la que un
   SDV-E del suelo no puede ignorar el nitrógeno aunque no tenga su número.

**Protocolo.**

- **Balance de entradas y salidas** por parcela: extracción por cosecha, fijación, deposición,
  fertilización, lixiviación y pérdida por erosión. La FAO valida el método **a escala local y
  regional** [VERIFICADO].
- **Dos indicadores obligatorios que sí son verificables sin umbral numérico:** (a) **exportación
  neta sin reposición declarada** por ciclo de cultivo; (b) **concentración de nitrato en la descarga
  de la unidad** (la FAO declara que el uso excesivo de fertilizante nitrogenado *«a menudo lleva a
  la contaminación del agua subterránea»* [VERIFICADO]).
- **Frecuencia:** cada ciclo de cultivo en agroecosistemas; **no aplica** en suelo silvestre.
- **Quién reporta:** la parte que cultiva, con verificación por laboratorio independiente sobre
  muestra de suelo y de agua de descarga. La asimetría cuenta: **quien exporta el nutriente es quien
  lo declara**, y eso es una vulnerabilidad de auditoría declarada (§13, pregunta 7).

**Violación.**

- **V1.** Exportación neta de nutrientes **sin reposición declarada** durante el número de ciclos que
  fije la política, en **área agrícola** dentro de la unidad ecológica.
- **V2.** **Concentración creciente de nitrato en la descarga de la unidad** atribuible a
  fertilización, con series publicadas en T13.
- **V3.** **Aplicación de un umbral de nutrientes a suelo silvestre** (bosque, pastizal). Es
  violación **del estándar**, no del suelo: quien la aplica está declarando violado un ecosistema
  intacto. Este documento lo prohíbe expresamente por la regla de ámbito de la FAO.

---

### Dimensión 7: Contaminación del suelo (el umbral que el estándar no posee)

**Qué protege.** Que el suelo no acumule contaminantes hasta dejar de sostener la biota y exportarlos
al agua y a la cadena alimentaria.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **Umbral numérico de contaminantes (metales, plaguicidas, hidrocarburos)** | **[SIN FUENTE VERIFICADA — pendiente de consenso científico]** | [SIN FUENTE VERIFICADA] | no encontrado en fuente oficial en esta sesión |
| **Contaminación por cadmio asociada a fósforo** | — | *«Toxicidad por cadmio relacionada con aplicaciones altas de fósforo»* | FAO, Soils Portal [VERIFICADO] |
| **Contaminación de agua subterránea por nitrógeno** | — | *«El uso excesivo de fertilizante N a menudo lleva a la contaminación del agua subterránea»* | FAO, Soils Portal [VERIFICADO] |
| **Meta global de respuesta** | — | **≥ 50 %** de reducción del riesgo de pesticidas y químicos peligrosos para 2030 | CBD, Marco Kunming-Montreal, Meta 7 (2022) [VERIFICADO] |
| Contaminación como amenaza oficial | — | incluida en la lista de amenazas de la UE desde 2006 (Thematic Strategy for Soil Protection, COM(2006) 231) | Comisión Europea [VERIFICADO] como lista |

**Justificación.** Esta dimensión **entra al estándar sin umbral, y esa es la única forma honesta de
entrar**. La FAO enumera la contaminación como una de las tres degradaciones químicas mayores y
**describe dos mecanismos verificables** (cadmio asociado a fósforo; nitrógeno a agua subterránea)
[VERIFICADO], pero **no publica en su portal un valor de disparo**. Un SDV-E no puede dejar fuera un
proceso que la FAO llama «mayor»; tampoco puede ponerle un número que nadie publicó.

**Por eso entra como dimensión de umbral binario declarado** `[HIPÓTESIS]`: no «cuánto contaminante»,
sino **si existe evidencia de contaminación atribuible a una actividad identificable dentro de la
unidad**. La carga de la prueba recae sobre quien introduce el contaminante (T14: *"la carga de la
prueba recae sobre quien propone acciones que afectan la temporalidad de no-participantes"*), no
sobre el suelo.

**Protocolo.**

- **Muestreo dirigido** a los puntos donde la actividad declara entrada de contaminante: aplicación
  de fertilizantes fosfatados, plaguicidas, riego con agua de calidad desconocida, depósito de
  residuos, paso de maquinaria.
- **Analito obligatorio mínimo:** el que corresponde a la actividad declarada. Sin analito declarado
  no hay medición.
- **Agua de descarga:** nitrato y el contaminante declarado (la FAO da el mecanismo N → agua
  subterránea [VERIFICADO]).
- **Frecuencia:** cada ciclo de cultivo donde haya aplicación declarada; muestreo único de
  caracterización antes de cualquier contrato que introduzca un contaminante nuevo [HIPÓTESIS].
- **Quién reporta:** laboratorio independiente. **El sujeto no puede reportar** y el que introduce el
  contaminante no puede ser su propio auditor: es la asimetría estructural del SDV-E (documento 09,
  §7).

**Violación.**

- **V1.** **Concentración por encima del valor de referencia aplicable** que declare la autoridad
  competente del territorio donde esté la unidad. Este documento **no fija el número** porque no tiene
  fuente verificada: fija la **obligación de declarar cuál se aplica**.
- **V2.** **Contaminación atribuible a una actividad identificable** dentro de la unidad, con
  analito, laboratorio y fecha declarados, **incluso sin valor de referencia** aplicable.
- **V3.** **Introducción de un contaminante nuevo sin caracterización previa del suelo.** Es
  condición de invalidez del contrato, por T14 y por la carga de la prueba.
- **🔴 Nota de honestidad:** de las siete dimensiones ponderadas, **esta es la que tiene el umbral más
  débil de todo el documento**. Se declara, no se disimula (§13, pregunta 5).

---

### Dimensión B1 (binaria, SIN PESO): Sellado del suelo (la muerte por sustitución)

**Qué protege.** La existencia física del suelo: que no sea cubierto por infraestructura. Es la única
dimensión del SDV-E donde **el piso y el óptimo coinciden en cero**.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **Definición operativa** | — | *«**Soil sealing** es prevalente en suelos cubiertos por infraestructura. Estas áreas pueden identificarse fácilmente por teledetección»* | FAO, Soils Portal — *Soil health: physical* [VERIFICADO] |
| **Objetivo (umbral político, no científico)** | **sellado neto cero** | **sello neto cero**: *«Zero net soil sealing and increase the reuse of urban soils»* | JRC, EU Soil Observatory — indicador de la Misión Suelo [VERIFICADO] |
| **Compromiso de la UE con horizonte** | — | *«Lograr **ningún consumo neto de suelo** (*no net land take*)»* para **2050** | Comisión Europea, **EU Soil Strategy for 2030** [VERIFICADO] |
| **Consecuencias declaradas del sellado** | — | *«Impacta tierra agrícola fértil, **pone en peligro la biodiversidad, incrementa los riesgos de inundación y de escasez de agua**, y contribuye al calentamiento global»* | Comisión Europea [VERIFICADO] |
| Estado de los suelos de la UE *(contexto)* | — | **60-70 %** de los suelos de la UE **no sanos**; **75 %** sanos para 2030 y **todos** para 2050 | Comisión Europea, *Soil health*; JRC/EUSO [VERIFICADO] |
| Coste anual de la degradación del suelo en la UE | — | **50 000 millones €/año** | Comisión Europea, *Soil health* [VERIFICADO] |
| **Cifra de superficie sellada (ha/año o % del territorio)** | **[SIN FUENTE VERIFICADA]** | — | las guías de la Comisión para limitar el sellado están **bloqueadas a automatización (403, CIRCABC)**; el indicador de *land take* de la AEMA está **muerto (404)** |
| **Relación cuantitativa sellado → escorrentía** | **[SIN FUENTE VERIFICADA]** | — | la Comisión afirma el efecto **cualitativamente** [VERIFICADO], **sin número** |

**Justificación de la forma binaria y sin peso.** Esta dimensión **no se pondera**, y la razón es
doctrinal y física a la vez:

1. **El piso y el óptimo son el mismo valor: cero.** Cualquier sellado neto positivo es pérdida de un
   recurso que la FAO declara **no renovable**, con **más de 1000 años por centímetro** [VERIFICADO].
   Ponderar el sellado sería permitir que un buen índice de carbono **pagara** por un suelo
   enterrado — exactamente lo que *"el suelo antes que el saldo"* prohíbe (Cap. 16.5 §16.5.14).
2. **El precedente canónico aplica sin adaptación.** Las dimensiones VIII (Rehabilitación) y IX
   (Opacidad Vital) del SDV-H *"se registran cualitativamente y mediante umbrales binarios
   (presencia/ausencia del derecho), no mediante pesos en la fórmula — medir la rehabilitación o la
   opacidad con la misma vara cuantitativa que el agua o la vivienda las destruiría"* (Cap. 8 §8.11).
   Un suelo sellado no se «mejora parcialmente»: **está o no está**.
3. **Es la dimensión más barata de medir del estándar completo.** La FAO la declara identificable por
   teledetección [VERIFICADO]. No requiere sensores in situ ni laboratorio. Un SDV-E que no mida el
   sellado no tiene excusa de coste.
4. **Es el caso límite de la no-compensación (§9).** Un suelo sellado no se regenera ni con crédito
   ni con tiempo humano. Es el mejor ejemplo de por qué INV2-E es un juez y no un contador.

**Declaración explícita de lo que el umbral ES y NO ES.** El «sellado neto cero» es **política, no
ciencia del suelo**: la propia literatura institucional reconoce que, a diferencia de otros
indicadores del suelo, las líneas base y umbrales del sellado no se basan en la ciencia del suelo
sino en la política. `[REPORTADO]` — leído en un extracto indexado de Zenodo que **no se abrió**, por
lo que **no entra como cita** y aquí se registra solo como advertencia de lectura. Consecuencia
doctrinal: **el valor 0 es votable en su forma (¿neto? ¿bruto? ¿con qué horizonte?) y no votable en
su existencia** (que el suelo no se sustituya).

**Protocolo.**

- **Teledetección** de superficie cubierta por infraestructura, con la huella declarada y la fecha de
  la imagen (T13). Validación en campo por muestreo cuando la imagen sea ambigua.
- **Unidad de medida:** hectáreas selladas **netas** dentro del territorio del mandato ecológico, y
  **coeficiente de reutilización** de suelo urbano (el objetivo de la UE incluye *«increase the reuse
  of urban soils»* [VERIFICADO]).
- **Frecuencia:** anual (la teledetección lo permite y el sellado no espera).
- **Quién reporta:** el guardián oráculo **recibe** el dato; la medición la produce la fuente de
  teledetección declarada en los 7 campos de identidad. **Ningún actor con interés en la obra puede
  ser el único que mide.**

**Violación.**

- **V1.** **Sellado neto positivo** en el territorio del mandato durante el ciclo de medición,
  medido por teledetección con fecha e imagen registradas.
- **V2.** **Sellado de suelo agrícola fértil o de suelo con estado de referencia no degradado**
  (la Comisión declara que el sellado *«impacta tierra agrícola fértil»* [VERIFICADO]).
- **V3.** **Sellado sin reutilización declarada** de suelo ya construido en el mismo territorio,
  cuando exista suelo urbano disponible [HIPÓTESIS] — es la parte del objetivo que la UE nombra
  explícitamente y la única que da margen operativo a la política sin tocar el piso.

---

### Dimensión B2 (binaria, SIN PESO): Zona Libre del suelo (lo que no se mide)

**Qué protege.** Aquello del suelo que no se mide y que no debe ser medido. No es una licencia de
explotación: es el reconocimiento de que **el estándar no agota al sujeto**.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **Existencia de la Zona Libre** | **Que exista y que NO se pondere** — se registra con T13 y **no entra jamás en el numerador de la fórmula** | — | Cap. 7 §7.9 · Cap. 16.5 §16.5.14 (doctrina) |
| **Catálogo de lo inefable de una unidad concreta** | — | **POLÍTICA (votable, `critical`)**: quórum 60 %, consenso 75 %, T13, anti-flip-flop 14 días, `CHECK` en BD | precedente del Parlamento Educativo, INV2-EDU |
| **Registro de un hecho de valor no medido** | — | Registro cualitativo con fecha, observador y descripción; **sin índice, sin peso, sin conversión** | este documento `[HIPÓTESIS]` |
| **Umbral numérico de la Zona Libre** | **[SIN FUENTE VERIFICADA — por diseño: no debe existir]** | — | — |

**Justificación.** *«Parte del valor del humedal es inefable (Cap. 7 §7.9). Los sensores miden salud
(agua, cobertura, biodiversidad indicadora); jamás "milagros". **Medir todo sería la forma técnica de
dejar de escucharlo**»* (Cap. 16.5 §16.5.14). En el suelo esa frase tiene un caso propio y muy
concreto: **la turba, el horizonte orgánico y el perfil mismo son archivos de tiempo no humano.**

**El aporte propio de este documento sobre la Zona Libre del suelo** `[HIPÓTESIS]`: la Zona Libre de
un suelo **no es una lista de cosas bonitas, es un archivo de irreversibilidad**. Un perfil de suelo
es una secuencia de horizontes que **registra su propia historia** —carbón de un incendio, ceniza
volcánica, un horizonte enterrado por una avenida, la turba que guarda milenios de vegetación— y esa
secuencia **es un documento que ninguna medición puede reproducir ni reponer**. Medirla con un índice
la convertiría en comparable, y por tanto **canjeable**: se podría «compensar» la destrucción de un
archivo de 5000 años con una mejora de 0,3 puntos en una tabla. **Lo que se protege aquí no es un
valor estético: es la imposibilidad de volver a leer.**

**Frontera LEY/POLÍTICA, explícita** (precedente INV2-EDU):

- **LEY (no se vota).** Que exista una Zona Libre en el suelo y que **no se pondere**. Ponderarla la
  volvería canjeable contra el piso, lo que *"el suelo antes que el saldo"* prohíbe.
- **POLÍTICA (votable).** **Qué entra en el catálogo** de cada unidad ecológica concreta —y con ello
  qué deja de medirse y qué se mide— es decisión deliberativa con la categoría `critical`. Sin esa
  separación, «declarar inefable» sería la vía más barata para vaciar el estándar.

**Protocolo (y es deliberadamente pobre).**

- **Registro cualitativo**: descripción del hecho de valor no medido, con fecha, observador y
  localización, y **nada más**. Nada de índice, nada de peso, nada de puntuación.
- **Entrada obligatoria:** todo hecho registrado en la Zona Libre **debe acompañarse de un motivo
  escrito por el que no se mide**. Es la única defensa contra el uso del catálogo como refugio.
- **Frecuencia:** cuando ocurre. No hay campaña de medición de lo que no se mide.
- **Quién reporta:** la comunidad de custodia y cualquier parte del contrato. **El guardián oráculo
  no decide qué es inefable**: lo decide el catálogo votado.

**Violación.**

- **V1.** **Asignar peso, índice o puntuación** a un elemento del catálogo de la Zona Libre. Es
  violación de la doctrina, verificable por inspección del cálculo.
- **V2.** **Declarar inefable un elemento sin motivo escrito.**
- **V3.** **Ampliar el catálogo para retirar de la medición una dimensión con piso** (erosión, COS,
  salinidad, sellado). **Retirar una dimensión con piso del cálculo es la violación más grave que este
  documento puede describir**, y es la razón por la que el catálogo se vota y se audita.
- **Lo que NO es violación:** que un elemento del catálogo no tenga medición. **Esa es su definición.**

---

### 4.1 Lo que este estándar NO convierte en violación: el fuego y la inundación como ciclos
El canon define el SDV de un ecosistema incluyendo *«Ciclos naturales respetados (fuego, inundación,
sequía)»* (Cap. 10 §10.4), y el documento 22 de esta biblioteca es el que los especifica. Este
documento **no puede** ignorarlo al medir carbono, erosión y macrofauna, porque en el suelo los tres
procesos se tocan:

- **El fuego no es pérdida de carbono: es parte de su ciclo.** Un incendio de régimen consume parte
  del COS y deja **carbono pirogénico**, que es una fracción recalcitrante del propio reservorio.
  Medir el COS del año siguiente a un incendio de régimen y contarlo como déficit contra la línea
  base **es un error de medida, no una violación del suelo.** La línea base de la dimensión 2 debe
  declarar si la unidad tiene régimen de fuego y en qué fase del ciclo se tomó.
- **La inundación deposita tanto como arrastra.** Un horizonte enterrado por una avenida es
  sedimentación, no erosión (es el mismo hecho que §4 B2 protege como archivo). Una crecida que
  cubre la unidad no es `E/P > 1`: es un aporte.
- **Lo que sí es violación es la alteración del régimen, no el evento.** Cambiar la frecuencia, la
  intensidad o la estacionalidad del fuego o de la inundación —por drenaje, por diques, por
  supresión total de incendios— **sí** es materia del SDV-E, y su umbral pertenece al documento 22.

**Consecuencia de redacción, declarada:** ninguna violación de §4 se dispara por un evento de fuego o
de inundación. Si el evento es de régimen, **el registro debe declararlo antes de calcular el
déficit**; si no se declara, la medición queda **no evaluada**, no violada (§6.3). `[HIPÓTESIS]` de
este documento, pendiente del 22.

---

## 5. Fórmula de violación, pesos y umbrales

**Advertencia de alcance.** La fórmula del SDV-E pertenece al documento 07 de esta biblioteca. Este
documento **no la fija**: propone **la forma que el suelo le impone** y los pesos relativos de sus
siete dimensiones, marcados como **propuesta no ratificada**.

### 5.1 El esqueleto, con la corrección del SDV-S aplicada

```
déficit_i = (requerido_i − actual_i) / requerido_i        ← normalizado (SDV-S, no la versión antigua)

Violación_suelo = Σ_i ( déficit_i × Peso_i × Duración × Intensidad )

FE(violación = 0) = 1,0  exacto                            ← base neutra innegociable
```

- **Déficit normalizado** y no `(req − act)`: es la versión coherente con el motor
  (`maxocontracts/blocks/sdv_validator.py`, que calcula `relative = deficit / required` y clasifica la
  severidad en ≤ 10 % leve · ≤ 30 % moderada · > 30 % severa) [VERIFICADO].
- **Base neutra 1,0.** El SDV-S tuvo que corregir `FS_S = 1,0 + e^v` → `FS_S = e^v` porque la primera
  versión recargaba el 100 % **incluso sin violación** (Cap. 9.5 §9.5.5). **Este documento no repite
  ese error:** un suelo que cumple su piso no paga nada.
- **`FE` es penalización, no precio.** Se descarta explícitamente el piso 0,2 del SDV-A
  (`09_comparativa.md` §5.2): el territorio que sostiene al humano **no está siendo violado por
  sostenerlo**.
- **El «infinito» no es un número.** Igual que en el SDV-A y el SDV-S, la consecuencia máxima de este
  estándar se implementa como **estado**, nunca como valor en una columna numérica
  (`09_comparativa.md` §5.3). En el suelo ese estado tiene nombre y fuente oficial (ver §8).

### 5.2 Pesos propuestos (propuesta no ratificada)

| Dimensión | Peso propuesto | Por qué ese peso |
|---|---|---|
| **1. Balance erosión ≤ formación** | **0,25** | Es el proceso de **irreversibilidad más rápida** y el único con ecuación de balance publicada. Pérdida en TA no recuperable |
| **2. Carbono orgánico del suelo** | **0,20** | La FAO lo declara el indicador que **trasciende** las tres categorías (química, física, biológica) [VERIFICADO] |
| **3. Biodiversidad edáfica y macrofauna** | **0,15** | Es el **mecanismo** que produce las dimensiones 1 y 5 (bioturbación → porosidad → infiltración) [VERIFICADO] |
| **4. Salinidad y sodicidad** | **0,15** | Único **umbral duro oficial** del documento; acumulativo e irreversible en la práctica |
| **5. Compactación** | **0,10** | Causalmente acoplada a 1 y 3: su función principal es **diagnóstica**, no aditiva (§4, dim. 5) |
| **6. Minería de nutrientes** | **0,10** | Ámbito **restringido a agroecosistemas** por regla de la FAO: no puede pesar como una dimensión universal |
| **7. Contaminación** | **0,05** | **El umbral más débil del documento**, y el peso lo refleja en lugar de disimularlo |
| **Σ** | **1,00** | |
| **B1. Sellado** | **SIN PESO** | Binaria: presencia/ausencia. Precedente Cap. 8 §8.11 |
| **B2. Zona Libre del suelo** | **SIN PESO** | Binaria. Ponderarla la haría canjeable |

**Tres reglas de agregación que este documento impone a la fórmula del documento 07** `[HIPÓTESIS]`:

1. **La suma pondera déficits normalizados, nunca magnitudes físicas.** Sumar % de COS con dS/m y con
   t/ha/año es lo que hace el ISE y es lo que un estándar **no puede** hacer (`09_comparativa.md`,
   insight I7). Los pesos comparan **gravedad relativa de la violación**, no unidades.
2. **Ningún valor de una dimensión compensa el déficit de otra.** El peso ordena prioridad de
   lectura; **no autoriza trueque**. Es la traducción aritmética de *"el suelo antes que el saldo"*.
3. **El sellado y la Zona Libre no entran en la suma: la anulan.** Un sellado neto positivo **no
   suma puntos de violación: activa el estado** de §8. Es la única forma de que una dimensión binaria
   sea de verdad binaria.

### 5.3 Escala de interpretación (propuesta, con referencia en lugar de invención)

Este documento **no inventa bandas**: propone usar las bandas del tablero que ya existe —el ISE
(≥ 85 Mejorando · 70-84 Estable · 50-69 Declinando · < 50 Crítico) [VERIFICADO]— **solo como lenguaje
de reporte**, y **advirtiendo la inconsistencia conocida**: el mismo documento del ISE declara
**dos escaleras que no coinciden** (bandas de estado frente a umbrales de alerta
`{'warning': 75, 'critical': 65, 'emergency': 50}`), de modo que un valor de 72 es Estable por bandas
y `warning` por alertas (`09_comparativa.md` §11.3). **Mientras las dos escaleras no coincidan, el
SDV-E del suelo no puede usarlas como consecuencia jurídica.** La consecuencia jurídica del suelo es
binaria y tiene fuente oficial: la escalera de §8.

---

## 6. Protocolo de medición (instrumentos, frecuencias, quién reporta)

### 6.1 Elenco de instrumentos del suelo

Análogo a los sensores nombrados del SDV-S (IFC, TRE, AOS, MS, VCM, Cap. 9.5 §9.5.6): índices
nombrados **con umbral**, no buenas intenciones.

| Instrumento propuesto | Qué mide | Dimensión | Estado de la fuente |
|---|---|---|---|
| **BER** — Balance Erosión/Formación | `E/P` con α declarada | 1 | 🟢 método con fuente (Montgomery, 2007); α `[SIN FUENTE VERIFICADA]` |
| **COS-b** — Línea base de carbono orgánico | `% COS` y `déficit_COS` | 2 | 🟡 método estándar de laboratorio; umbral declarado proxy |
| **TMA** — Transecto de Macrofauna | presencia/ausencia y orden de magnitud | 3 | 🔴 protocolo **nombrado** (TSBF/FAO) y **no abierto** |
| **GSA** — Lectura GSASmap local | CEe · ESP · pH | 4 | 🟢 umbrales con fuente (FAO, 2021) |
| **EPF** — Estructura y Perfil Físico | costra · capa compactada · encharcamiento | 5 | 🔴 indicador propio; sin umbral externo |
| **BAL-N** — Balance de nutrientes | entradas/salidas · nitrato en descarga | 6 | 🔴 sin umbral; ámbito restringido |
| **CAR** — Caracterización de contaminantes | analito declarado | 7 | 🔴 sin umbral propio |
| **SAT-S** — Sellado por teledetección | ha selladas netas · reutilización | **B1** | 🟢 objetivo político con fuente (UE) |
| **REG-ZL** — Registro de Zona Libre | hecho no medido + motivo escrito | **B2** | 🟢 doctrinal |

**Dos reglas del elenco, heredadas del SDV-S y adaptadas al suelo:**

1. **Un instrumento sin umbral no es un instrumento: es una campaña de campo.** TMA, EPF, BAL-N y CAR
   se reportan hoy como **observación estructurada con registro T13**, y **no pueden activar INV2-E
   por sí solos** hasta que tengan umbral con fuente. Es la consecuencia directa de §9 del documento
   09: *sin definición operativa de violación no hay violación.*
2. **El instrumento más barato se mide primero.** SAT-S se resuelve con teledetección [VERIFICADO].
   Un mandato ecológico del suelo que no tenga ni eso no está midiendo: está declarando.

### 6.2 Frecuencias (propuesta)

| Dimensión | Frecuencia propuesta | Razón |
|---|---|---|
| 1. Erosión | **anual** | Es el proceso más rápido del estándar |
| 4. Salinidad | **anual** en zona árida o con riego; 3-5 años en el resto | Vía de entrada dominante declarada por la FAO: el riego |
| **B1. Sellado** | **anual** | La teledetección lo permite y el sellado no espera |
| 6 y 7 | por **ciclo de cultivo**, solo en agroecosistemas | El ámbito de la FAO es agrícola |
| 2. COS | **3-5 años** | El COS cambia despacio: medirlo cada año gasta más de lo que informa |
| 3. Macrofauna | **anual o por estación de crecimiento**, mismo transecto y misma fecha relativa | La macrofauna es estacional |
| 5. Estructura | **anual** donde haya maquinaria pesada, ganadería concentrada o riego | Causas nombradas por la FAO |
| **B2. Zona Libre** | **cuando ocurre** | No hay campaña de medición de lo que no se mide |

### 6.3 Quién reporta, y la asimetría que el suelo agrava

| Rol | Quién | Qué hace | Qué NO hace |
|---|---|---|---|
| **Mide** | Laboratorio independiente + fuente de teledetección declarada + comunidad de custodia | Produce el dato con T13 | No decide el piso |
| **Consiente** | **Guardián oráculo** de la parte `eco-` | Otorga o niega consentimiento | **No mide** y no decide qué es inefable |
| **Custodia** | Comunidad de custodia del mandato ecológico | Sostiene el registro, verifica en campo | No puede ser el único auditor de su propio beneficio |
| **Declara** | Quien opera: maquinaria, riego, fertilizante, obra | Declara su intervención | **No puede ser su propio verificador** |

**La asimetría, dicha sin adornos.** El sujeto del SDV-E **no puede reportar nada**: *"Nosotros
registramos la interacción, no la vida interna del ecosistema"* (Cap. 16.5 §16.5.14). Y en el suelo
esto es más grave que en cualquier otro ecosistema del reino, porque **la mayor parte de su
biodiversidad es invisible**: la FAO define la biodiversidad del suelo como *«la variabilidad entre
organismos vivos, incluida la miríada no visible a simple vista»* [VERIFICADO] y calcula que el suelo
alberga **un cuarto** de la biodiversidad del planeta [VERIFICADO], con **millones de individuos y
miles de especies de bacterias por gramo** [VERIFICADO]. Es decir: **el sujeto con más biodiversidad
del reino es el que menos puede declarar su estado.** Sin instrumentos, el SDV-E del suelo no es
«débil»: es **inenunciable**.

**Inversión del principio «sin dato no castiga»** (documento 09, insight I9). `INV2-EDU` dice
*"la duda sin evidencia no castiga"* y protege al presunto vulnerado cuando no hay medición. En el
suelo el presunto vulnerado **es el suelo y no reporta**: aplicar la regla sin más protegería al
presunto **violador**. Propuesta `[HIPÓTESIS]`, no ratificada, aplicada al suelo:

- **La ausencia de monitoreo NUNCA se imputa como violación del suelo** (jamás se declara un suelo
  violado por no haber sido medido).
- **Pero activa una bandera de opacidad edáfica** que opera como **obligación contractual de
  instrumentar** y como **condición de validez del contrato**, no como sanción al territorio.
- **Y la ley no se negocia por ausencia de dato:** *"mientras no haya resolución, el canon manda."*
  Un suelo sin medición **no está declarado conforme**: está **no evaluado**, y eso es un estado
  distinto que el registro debe distinguir.

---

## 7. Verificación y auditoría (T13, guardián, comunidad testigo)

**Lo que el suelo comparte con el resto del reino.** T13 (Transparencia de Cálculo): la contabilidad
nunca se borra. Toda violación del suelo se **documenta y es auditable**, incluso cuando su
cuantificación se delega (precedente de las dimensiones VIII y IX del SDV-H, Cap. 8 §8.11).

**Lo que el suelo no tiene: un par auditor.** Ningún suelo audita a otro suelo, y —a diferencia del
resto del reino natural, donde un río puede auditarse por su cuenca o un océano por sus satélites—
**tampoco hay un ecosistema vecino que sirva de referencia externa**: la cuenca que recibe el sedimento
**es la parte perjudicada**, no el auditor. La auditoría del suelo
viene necesariamente de fuera: **de la ciencia, de la teledetección y de la comunidad de custodia**,
es decir, del reino que se beneficia de su uso. Ese es el hallazgo estructural del documento 09
(insight I3) y en el suelo tiene su forma más incómoda: **el sedimento exportado por la unidad
erosionada degrada a la unidad de aguas abajo, que no tiene forma de auditar a la de arriba.**

**Consecuencia institucional (propuesta).** La **comunidad testigo** y los **7 campos obligatorios de
identidad** de una representación natural —entidad representada, territorio, fuentes de datos, límites
del mandato, comunidad de custodia, parámetros SDV-E y procedimiento de disputa— no son burocracia:
son el **sustituto institucional del par auditor que no existe**. En el suelo, tres de esos campos
tienen contenido técnico obligatorio:

| Campo de identidad | Contenido técnico obligatorio para una unidad de suelo |
|---|---|
| **Territorio** | Polígono con α (densidad aparente) declarada; **sin α no hay unidad comparable** |
| **Fuentes de datos** | Capa de teledetección + laboratorio + transecto, con fechas. **Dato sin fecha no es dato** |
| **Parámetros SDV-E** | Las 7 dimensiones ponderadas **más** las 2 binarias, con su frontera LEY/POLÍTICA declarada |

**Riesgos abiertos que esta falta de par agrava** (auditoría de solo lectura del repositorio,
`docs/architecture/blindaje_anti_gamificacion_equidad.md`):

| ID | Riesgo | Efecto concreto sobre el SDV-E del suelo |
|---|---|---|
| **R4** | Partes fantasma: cualquier usuario autenticado crea una parte `eco-*` y queda como su dueño, sin verificar autoridad sobre la entidad | Cualquiera puede **crear el suelo que va a declarar conforme** y quedar como su custodio |
| **R6** | T9 (Reciprocidad Justa) no se valida en la creación: un contrato 100 % unilateral pasa y se activa | Se puede **minar el carbono y exportar el nutriente** de una unidad sin contraprestación y sin bloqueo |
| **R13** | Guardián eco con heurística laxa: sin `DEEPSEEK_API_KEY` aprueba si los invariantes pasan | El consentimiento del suelo se vuelve **automático**, y con R6 incluye contratos unilaterales |

**Y una consecuencia específica del suelo, que no aparece en el documento 09.** El riesgo R4 es
**peor** en el suelo que en un bosque o un río, por una razón operativa: un río tiene cauce y un
bosque tiene dosel, **ambos visibles desde el satélite y difíciles de falsificar**. Un suelo es una
superficie que se puede declarar «en reposo» y **degradar sin cambio de cobertura apreciable** —
erosión laminar, minería de nutrientes y pérdida de carbono **no se ven desde arriba**. Es decir: **el
sujeto con el instrumento de medición más barato (el sellado) es también el que puede ser degradado
de forma más invisible (todo lo demás).** `[HIPÓTESIS]` — y es el argumento más fuerte de este
documento a favor del muestreo de suelo obligatorio, no opcional, en cualquier contrato que afecte a
una unidad con suelo.

---

## 8. Invariante INV2-E: de estándar a contrato ejecutable

**El invariante genérico.** **INV2** dice: *"Ninguna acción del contrato puede dejar a un
participante bajo su SDV"* (Cap. 17). Para el Reino Natural, **INV2-E no existe** —ni en el canon como
especificación, ni en el motor (`maxocontracts/core/axioms.py`, donde solo hay
`validate_invariant_sdv` e `validate_invariant_sdv_s`), ni como bloque validador
(`maxocontracts/blocks/sdv_s_validator.py` es el gemelo que falta)— y su especificación completa
pertenece al documento 08 de esta biblioteca.

**Lo que este documento aporta a INV2-E son los disparadores del suelo, y son la escalera oficial de
la FAO.** La FAO publica la secuencia **Prevención → Mitigación → Rehabilitación** con su criterio de
disparo y su horizonte temporal [VERIFICADO]:

| Régimen | Cuándo se aplica (criterio de la FAO) | Horizonte declarado | Traducción a INV2-E del suelo `[HIPÓTESIS]` |
|---|---|---|---|
| **1. Prevención** | *«Uso de medidas de conservación que mantienen los recursos naturales y sus funciones ambientales y productivas»* | — | **Estado normal.** No hay violación: el contrato exige **no cruzar el piso** y declarar línea base antes de intervenir |
| **2. Mitigación** | *«Cuando la degradación ya ha comenzado»* — *«detener la degradación ulterior y empezar a mejorar»* | **corto y medio plazo** | **Primera violación.** El contrato **no puede continuar la acción** que cruza el piso; debe **detenerla** y declarar plan de mejora. No hay reintegración automática |
| **3. Rehabilitación** | *«Cuando la tierra ya está degradada hasta tal punto que el uso original ya no es posible y la tierra se ha vuelto prácticamente improductiva»* | **largo plazo y a menudo inversiones más costosas** | **Estado agravado.** El coste en TA es declarado y **no se compra de vuelta**: T14 obliga a elegir la opción de **menor irreversibilidad** y a **documentar el coste de oportunidad asumido** |

**Tres requisitos que este documento impone a la especificación de INV2-E para el suelo:**

1. **El disparador es un hecho, no un índice agregado.** El sellado positivo (B1) y la Zona Libre mal
   usada (B2) **activan estado**, no suman puntos (§5.2, regla 3). Es la lección del SDV-A y del
   SDV-S: la consecuencia máxima se implementa como **estado verificable**, nunca como `inf` en una
   columna numérica (`09_comparativa.md` §5.3).
2. **La única acción ejecutable es detener o modificar la actividad humana que viola el piso.** Un
   suelo no se retracta, no se rehabilita por contrato y no cabe en una cápsula de memoria. El
   paralelo canónico exacto es el *Veto por Crimen de Coherencia* del SDV-S: *"la interrupción total
   del sistema que la provoca"* (Cap. 9.5 §9.5.10).
3. **Contador con umbral para los casos sin hecho agudo.** Donde la violación es progresiva
   (macrofauna ausente, costra persistente, dEe creciente) el invariante necesita **un contador de
   ciclos consecutivos**, como los 7 ciclos del SDV-S. **Este documento propone 3 ciclos para el
   suelo** `[HIPÓTESIS]` y **no lo ratifica**: la diferencia con el SDV-S (que cuenta ciclos de
   proceso en TPI) es que aquí el ciclo es un **año TA**, y elegir 3 frente a 7 es una decisión
   doctrinal del documento 07.

---

## 9. El suelo antes que el saldo (no compensación)

**La doctrina.** *"El suelo antes que el saldo"*: el crédito regenerativo acumulado **NO compensa**
caer bajo el SDV-E (Cap. 16.5 §16.5.14). El documento 09 de esta biblioteca ya estableció la doctrina
general para el reino; aquí se dice **por qué el suelo es su caso más puro**, con tres razones que solo
el suelo puede dar.

**Razón 1 — El suelo es el único ecosistema donde daño y reparación se miden en la misma unidad
física, y esa unidad ya tiene fuente.** La erosión se mide en t/ha/año y la formación también, **una
vez declarada α** (sin ella, el balance solo existe como razón adimensional, §4 dimensión 1). Eso
**no** significa que sean intercambiables: significa que la razón **se puede calcular**, y cuando la
razón supera 1, el saldo es **matemáticamente negativo** y ningún crédito lo cambia. `[HIPÓTESIS]`
del proyecto: **este balance es el «caudal ecológico» del suelo**, la formulación más limpia
disponible de un piso que no se puede cumplir degradando despacio (véase §3, pilar 5).

**Razón 2 — El sellado es el caso límite donde el crédito regenerativo es estructuralmente
inútil.** Un suelo sellado no se regenera **ni con crédito ni con tiempo humano**: la FAO declara el
suelo **recurso no renovable** y estima **más de 1000 años por centímetro** [VERIFICADO]. Es la
dimensión donde «compensar» no es caro: es **imposible**, y por eso es el mejor ejemplo de por qué
INV2-E es un juez y no un contador.

**Razón 3 — La irreversibilidad del suelo ya está definida por la FAO, y la definición es del
canon.** *«Desertificación: (a) degradación de la tierra en zonas secas y/o (b) el cambio
**irreversible** de la tierra a un estado en el que ya no puede recuperarse para su uso original»*
[VERIFICADO]. Esto tiene una consecuencia doctrinal precisa que este documento declara como aporte:
**T14 (menor irreversibilidad) no necesita definición propia en el SDV-E del suelo: la FAO ya la
dio.** El SDV-E del suelo es el único estándar de la familia cuyo criterio de irreversibilidad
**viene citado de una fuente oficial**, no construido por el proyecto.

**Razón 4 — El estado de la degradación justifica la carga de la prueba, no la compensación.**
**33 %** del suelo está **moderada a altamente degradado** por erosión, pérdida de materia orgánica,
agotamiento de nutrientes, acidificación, salinización, compactación y contaminación química (FAO,
2017) [VERIFICADO]; la productividad terrestre se ha reducido un **23 %** por degradación (IPBES,
2019) [VERIFICADO]; **60-70 %** de los suelos de la UE **no están sanos** y su degradación cuesta
**50 000 millones €/año** (Comisión Europea) [VERIFICADO]; y la frontera planetaria del **cambio del
sistema terrestre está transgredida** [VERIFICADO]. **Un piso no se relaja porque ya esté mayormente
incumplido.** Al contrario: es el argumento de T14 para que la carga de la prueba recaiga en quien
propone la intervención.

**Y el estado real del crédito regenerativo, hoy** (no es doctrina: es código, y es idéntico al que
el documento 09 documenta):

| Pieza | Estado | Evidencia |
|---|---|---|
| `r_units` negativo como crédito regenerativo | 🟢 existe y está probado | `app/micromax.py` (`log_cdd`) documenta *"`r_units` NEGATIVO = crédito regenerativo (EVV 1.2 §4.3)"*; `tests/test_micromax.py::test_credito_regenerativo_r_negativo` lo ejercita con `-12.0` |
| **Contabilidad del crédito** | 🔴 **no existe** | No hay `SUM(r_units)`. El componente R del sistema (`app/vhv_calculator.py::calculate_r_component`) **solo cuenta extracción**, y el precio cierra en `max(0.0, round(price, 4))` (`app/maxo.py`): **nunca es negativo** |
| **Validación de `r_units`** | 🔴 **ninguna** | Acepta cualquier negativo (`-1e9`); no exige nota, evidencia, tercero ni techo; `NaN` e `inf` pasan el filtro |

**Es exactamente el agujero que el canon nombra: el crédito existe, el juez no.** Y en el suelo tiene
una forma material que en ningún otro reino tiene: **hoy una unidad de suelo puede acumular crédito
regenerativo mientras pierde su horizonte superficial a 10-100 veces la tasa de formación, y ninguna
cuenta del sistema lo registra.** El balance de la dimensión 1 **no se consulta en ningún punto del
código**, porque el código no tiene SDV-E. Esta biblioteca es el juez que falta.

---

## 10. Zona Libre: lo que NO se mide

La Zona Libre del Reino Natural está enunciada en el canon y especificada para el suelo en la
**dimensión B2** de §4. Esta sección dice **qué es exactamente lo que no se mide en un suelo** y
**dónde está la frontera** entre no medir y no proteger.

**Lo que NO se mide en un suelo, y por qué (propuesta de este documento, `[HIPÓTESIS]`):**

| Lo que no se mide | Por qué no se mide |
|---|---|
| **El archivo del perfil** | La secuencia de horizontes (carbón de incendio, ceniza volcánica, horizonte enterrado, turba) **es un documento histórico**: ninguna medición lo reproduce ni lo repone. Medirlo con un índice lo volvería canjeable (§4, B2) |
| **El valor del suelo para quien lo habita sin declararlo** | No hay sujeto del suelo que pueda declarar su experiencia. *"Nosotros registramos la interacción, no la vida interna del ecosistema"* (Cap. 16.5 §16.5.14) |
| **El suelo como memoria de la comunidad de custodia** | El vínculo entre una comunidad y su suelo no es un parámetro ecológico y no debe convertirse en uno |
| **Lo que la FAO llama «milagros»** | Los sensores miden salud; jamás milagros (Cap. 16.5 §16.5.14). En el suelo, la fertilidad que aparece sin explicación documentada no se convierte en índice |

**Lo que sí se mide, aunque parezca inefable, y no puede refugiarse en la Zona Libre:** el carbono, la
macrofauna, la salinidad, la compactación, el sellado, el balance erosión/formación y el balance de
nutrientes (dimensión 6, con ámbito restringido a agroecosistemas). **Ninguno de esos siete es
inefable: son difíciles o caros.** La contaminación (dimensión 7) no entra en esta lista con la misma
fuerza —este documento no tiene su umbral— pero **tampoco entra en la Zona Libre**: su protocolo
existe (analito declarado, muestreo dirigido, laboratorio independiente) y lo que falta es el número,
no la medición. La Zona Libre no es un depósito de lo incómodo de medir, y este documento lo dice con
la regla de su protocolo (V2 y V3 de B2): **todo elemento del catálogo exige motivo escrito, y retirar
del cálculo una dimensión con piso es la violación más grave que este estándar describe.**

**Por qué no se pondera.** El precedente canónico es explícito: las dimensiones VIII (Rehabilitación)
y IX (Opacidad Vital) del SDV-H se registran con umbrales binarios y **no mediante pesos** porque
*"medir la rehabilitación o la opacidad con la misma vara cuantitativa que el agua o la vivienda las
destruiría"* (Cap. 8 §8.11). Y en el suelo hay un agravante que el SDV-H no tiene: **el suelo es el
sujeto del reino donde el instrumento existente (el ISE, 15 % de «Salud del suelo») premia medir.**
Un instrumento que premia medir tiene un incentivo estructural a medirlo todo — y *"medir todo sería
la forma técnica de dejar de escucharlo"* (Cap. 16.5 §16.5.14).

**La frontera LEY/POLÍTICA, resumida** (detalle en §4, B2):

- **LEY (no se vota):** que la Zona Libre exista en el suelo y que **no se pondere**.
- **POLÍTICA (votable, `critical`):** **qué entra en el catálogo** de cada unidad ecológica concreta.
- **Riesgo que la frontera no elimina, y este documento lo declara:** si el catálogo se vota sin
  carga de la prueba, «declarar inefable» se convierte en la vía más barata para vaciar el estándar.
  El único freno que este documento propone es procedimental —motivo escrito obligatorio y registro
  T13 del acto de votación— y **no está demostrado que sea suficiente** (§13, pregunta 9).

---

## 11. Comparativa inter-reinos (SDV-H · SDV-A · SDV-E · SDV-S)

**Solo los ejes donde el suelo dice algo distinto.** La tabla completa de 16 ejes está en el
documento 09 (`09_Comparativa_inter_reinos.md` §11.1); aquí se añaden los ejes que **aparecen al leer
el reino natural desde el suelo** y que ninguno de los cuatro estándares tenía nombrados.

### 11.1 Ejes nuevos que el suelo obliga a añadir

| # | Eje | SDV-H | SDV-A | **SDV-E (suelo)** | SDV-S |
|---|---|---|---|---|---|
| 17 | **Forma del piso** | Concentración y cantidad (µg/m³, L/día, m²) | Cantidad por individuo (m², L, h) | **Razón de flujos: `E/P ≤ 1`** + concentraciones (dS/m, % COS) | Escala 0-1 por dimensión |
| 18 | **¿El piso se puede cumplir degradando despacio?** | No aplica | No aplica | **No.** Si E y P caen juntos, la razón se mantiene; el piso obliga a medir **los dos** flujos, no el stock | No aplica |
| 19 | **Reversibilidad del daño en el propio tiempo del sujeto** | Sí: rehabilitación (Dim. VIII) | Prohibición, no reparación | **No. Nunca.** > 1000 años por cm; recurso no renovable (FAO, 2017) | Parcial: memoria sí, ciclo no |
| 20 | **¿Existe definición oficial de irreversibilidad?** | No | No | **Sí: la FAO la da** («cambio irreversible… ya no puede recuperarse para su uso original») | No |
| 21 | **Coste de la degradación declarado en dinero** | No | No | **Sí: 50 000 millones €/año** en la UE (Comisión Europea) | No |
| 22 | **El instrumento más barato de medir** | Encuesta o laboratorio | Observación etológica | **Teledetección del sellado** (FAO: «identificables fácilmente por teledetección») | Bitácora propia |
| 23 | **¿Puede degradarse sin cambio visible desde arriba?** | No aplica | No aplica | **Sí: erosión laminar, minería de nutrientes y pérdida de COS no se ven desde el satélite** → obliga a muestreo de suelo | No aplica |
| 24 | **Fracción de la biodiversidad planetaria del sujeto** | — | — | **Un cuarto (25 %)** del total, en su mayoría **no visible** (FAO) | — |
| 25 | **¿Hay dimensión con piso y óptimo idénticos?** | No | No | **Sí: el sellado (cero neto)** | No |

### 11.2 Inspección: qué revelan estos ejes

**Eje 17 y 18 — el suelo es el único estándar de la familia cuyo piso es una razón y no un nivel.**
Consecuencia de ingeniería inmediata: **un piso que es una razón no se puede evaluar con una sola
medición.** Los otros tres estándares se auditan con un valor por parámetro; el suelo exige **dos
flujos con el mismo α declarado**. Eso lo hace más caro de auditar y, a la vez, **inmune al truco más
obvio** —«mi suelo está bien porque su tasa de pérdida es pequeña»— porque la formación también hay
que medirla.

**Eje 19 y 20 — el suelo es el estándar donde la irreversibilidad no es una inferencia del proyecto
sino una cita.** El documento 09 estableció que en el SDV-E *"la prevención es el remedio completo"*;
el suelo permite decirlo **con fuente oficial**: la FAO declara el recurso no renovable, publica el
plazo (> 1000 años/cm) y da la definición de cambio irreversible. Ningún otro reino tiene las tres
cosas.

**Eje 21 — el suelo es el único sujeto del reino natural con coste monetario oficial de su
degradación.** 50 000 millones €/año en la UE [VERIFICADO]. Es un dato incómodo para la doctrina y
este documento lo declara sin usarlo como argumento: **usar el coste monetario como razón para
proteger el suelo sería contradecir el T9 (no-antropocentrismo)**. Se registra como **evidencia de
que el daño es real y medido**, no como su valoración.

**Eje 22 y 23 — la asimetría del suelo: medición baratísima para lo irreversible y carísima para lo
invisible.** El sellado (la pérdida más absoluta) se mide desde el satélite; la erosión laminar, la
minería de nutrientes y la pérdida de carbono (las pérdidas más extendidas) **exigen pala,
laboratorio y años de serie**. Un estándar que solo use teledetección medirá **la única dimensión que
no puede compensarse** y **ninguna de las que se están perdiendo ahora**. `[HIPÓTESIS]` — y es la
razón por la que §6.3 declara el muestreo de suelo obligatorio y no opcional.

**Eje 24 — el sujeto con más biodiversidad es el que menos puede declarar.** Un cuarto de la
biodiversidad planetaria [VERIFICADO], en su mayoría no visible a simple vista [VERIFICADO], con miles
de especies de bacterias por gramo [VERIFICADO]. Contrastado con el eje «voz del sujeto» del documento
09: **el suelo es el extremo absoluto de esa asimetría.**

**Eje 25 — el sellado es el único caso de la familia donde piso y óptimo coinciden.** Ni el agua (20
frente a 50-100 L), ni el espacio de una gallina (0,25 frente a 0,75 m²), ni la opacidad sintética
tienen esa propiedad. Es lo que lo vuelve **necesariamente binario** y no una decisión de prudencia.

### 11.3 Lo que este documento NO autoriza a concluir

1. **No autoriza a trasvasar el factor T del USDA como piso del SDV-E.** T es un umbral
   agronómico-económico de planificación de finca; el piso es el balance de Montgomery (2007). T entra
   solo como comparación (§4, dimensión 1).
2. **No autoriza a usar el 2 % de COS como piso ecológico.** Es un proxy agronómico, su fuente niega
   su universalidad, y este documento lo usa solo como disparador de revisión (§4, dimensión 2).
3. **No autoriza a aplicar el umbral de nutrientes al suelo silvestre.** La FAO dice explícitamente
   que el agotamiento **no se espera** fuera de la agricultura (§4, dimensión 6).
4. **No autoriza a ponderar el sellado ni la Zona Libre**, ni a usarlos como puntos que compensen
   otro déficit (§5.2, regla 3).
5. **No autoriza a escribir 4 dS/m.** El umbral verificado de la FAO es **CEe > 2 dS/m**; la
   discrepancia con el sistema Richards queda declarada y abierta (§13, pregunta 4).
6. **No autoriza a leer los descriptores de la FAO como umbrales.** «> 1000 especies/m²» y «3000 kg/ha
   de lombrices» son Óptimos descriptivos —y el segundo, `[REPORTADO]`— nunca pisos (§4, dimensión 3).
7. **No autoriza a usar las bandas del ISE como consecuencia jurídica** mientras sus dos escaleras
   internas no coincidan (§5.3).

---

## 12. Estado de implementación

**Regla de honestidad aplicada:** se marca 🔴 **todo** lo que no tiene código y tests. Está prohibido
afirmar que el SDV-E, el INV2-E, el ISE, los sensores o el quórum `eco-` están implementados: **no lo
están.** Esta biblioteca es el *estándar primero*; la contabilidad viene después (Cap. 16.5 §16.5.14).

### 12.1 Lo que SÍ existe (y es honesto decir que existe)

| Pieza | Dónde | Estado |
|---|---|---|
| `r_units` negativo como crédito regenerativo | `app/micromax.py` (`log_cdd`), `app/micromax_bp.py` | 🟢 registrado y devuelto; **sin efecto contable** |
| **V no admite negativos; R sí** | `app/micromax.py` (`if v_ucv < 0: raise`) | 🟢 invariante de diseño real |
| Test del crédito regenerativo | `tests/test_micromax.py::test_credito_regenerativo_r_negativo` | 🟢 `-12.0` aceptado y devuelto |
| Parte `eco-` (Ecosistema) | `app/parties.py` (`PARTY_TYPES`, `COLLECTIVE_PREFIXES`) | 🟢 creada y usable |
| Guardián oráculo del ecosistema | `app/contracts_bp.py` (`_guardian_approve_ecosystem()`) | 🟡 funciona en la **firma de contratos**; heurística laxa (R13) |
| Test del guardián | `tests/test_maxocontracts/test_parties_escalas.py` (`TestEcosystemGuardian`) | 🟢 2 casos (aprueba / deniega por γ) |
| Validación de déficit normalizado | `maxocontracts/blocks/sdv_validator.py` (`relative = deficit / required`) | 🟢 el suelo **debe** usar esta forma (§5.1) |
| Vector `[T, V, R]` en CDD doméstico | `app/micromax.py`, `frontend/app/micromax/page.tsx` | 🟢 implementado |
| SDV-S + INV2-S (el pariente más cercano) | `maxocontracts/` | 🟢 estándar + 41 tests (`test_sdv_s.py`, `test_ternura.py`) |

### 12.2 Lo que NO existe (y está prohibido afirmar que existe)

| Pieza | Estado | Evidencia |
|---|---|---|
| **Clase `SDV_E` en el motor** | 🔴 | no hay tipo en `maxocontracts/core/types.py` (el gemelo sería `SDV_S`); no hay `Participant.sdv_e_actual` ni `is_natural` |
| **`INV2-E`** | 🔴 | no hay `validate_invariant_sdv_e` en `maxocontracts/core/axioms.py` ni bloque validador gemelo de `sdv_s_validator.py` |
| **Cualquier dimensión del suelo en código** | 🔴 | **cero** implementación de erosión, COS, macrofauna, salinidad, compactación, nutrientes, contaminación o sellado |
| **Ingesta de datos de suelo** | 🔴 | **cero** sensores, APIs, satélites o ingestores en `app/`. Ni GSOCmap, ni GSASmap, ni teledetección |
| **Línea base de COS por unidad** | 🔴 | no existe tabla, ni campo, ni migración para una línea base edáfica |
| **Densidad aparente (α) en el modelo** | 🔴 | no existe el parámetro; sin él **ninguna** conversión mm ↔ t/ha es posible (§4, dimensión 1) |
| **Identidad de la representación natural (7 campos)** | 🔴 | los 7 campos del canon (entidad representada, territorio, fuentes de datos, límites del mandato, comunidad de custodia, parámetros SDV-E, procedimiento de disputa) **no tienen tabla**; `maxo_parties` tiene 7 columnas genéricas |
| **Mandato ecológico versionado / OCI** | 🔴 | teoría pura (0 coincidencias en código). **`actor_kind` está cerrado a `{"human","synthetic"}`** (`app/synthetic_sessions.py`): un guardián ecológico **no cabe en la bitácora** |
| **Anti-suplantación de unidad de suelo** | 🔴 | sin fuentes físicas múltiples ni comunidad testigo; **R4 abierto**, y agravado en el suelo porque la degradación sin cambio de cobertura es invisible (§7) |
| **Traducción TA↔TVI ejecutable** | 🔴 | `PIU.valorar_ta_natural` es un `pass` con comentario (`docs/architecture/DISENO_IMPLEMENTACION_FUTURA.md`) |
| **Contabilidad del crédito regenerativo** | 🔴 | no existe `SUM(r_units)`; el R del sistema solo cuenta extracción; el precio cierra en `max(0.0, …)` (`app/maxo.py`): **nunca es negativo** |
| **Validación de `r_units`** | 🔴 | acepta cualquier negativo (`-1e9`); no exige `r_notes`, evidencia, tercero ni techo; `NaN` e `inf` pasan el filtro (para V, `nan < 0` es falso) |
| **Métrica ecológica en código** | 🔴 | el ISE es **un documento**: `docs/architecture/metricas_detalle_kpis_oraculos_dinamicos.md` |
| **Quórum `eco-` N-de-M** | 🔴 | el camino ecosistema retorna antes de la lógica de quórum; **el libro afirma lo contrario** (Cap. 16.5 §16.5.14: *"consentimiento agregado por quórum delegado N-de-M"*) → **incoherencia teoría↔código declarada** |
| **Procedimiento de disputa** | 🔴 | inexistente |
| **Protocolo TMA (macrofauna) ejecutable** | 🔴 | el protocolo está **nombrado** (FAO, *Soil macrofauna field manual*, `[REPORTADO]`) y **no abierto** |
| **Eje de ciclos naturales del suelo (fuego, inundación, sequía)** | 🔴 | **no existe como dimensión ni como parámetro**: §4.1 solo declara que los eventos de régimen **no** son violación. Falta el umbral de **alteración del régimen** (frecuencia, intensidad, estacionalidad), que pertenece al documento 22 (§13, pregunta 16) |
| **Umbral numérico de compactación** | 🔴 | `[SIN FUENTE VERIFICADA]` — segundo intento fallido (§13, pregunta 3) |
| **Mapas vivos actualizados** | 🔴 | `docs/architecture/mapa_coherencia_ola4.md` no menciona `r_units`, el Reino Natural ni el SDV-E; `docs/architecture/requisitos_fase2_ola4.md` **no tiene ningún RF del Reino Natural** |
| **Infraestructura base** | 🔴 | sin seeds ni data-model para una entidad natural; `simulator/` no tiene las carpetas que anuncia `AGENTS.md` |

### 12.3 Incoherencias colaterales que este documento NO hereda

- `resolve_participant_by_pid` (`app/parties.py`) asigna a una parte `eco-` **el SDV humano**
  (`sdv_actual=SDV()`), porque no existe SDV-E. **Un suelo con SDV humano es una incoherencia de
  sujeto, no un hueco de implementación.** [VERIFICADO]
- La R del contrato se persiste en la columna **`total_vhv_h` / `vhv_h`** (`app/schema.sql`,
  `app/contracts_bp.py`): nombre engañoso, sin `CHECK` de signo. En el suelo, **un crédito
  regenerativo guardado en una columna llamada «vhv_h» no es auditable por nombre.**
- `simulator/simulator.js` usa `v: -0.5` (V negativo) mientras `app/micromax.py` lo prohíbe.
- `docs/architecture/DISENO_IMPLEMENTACION_FUTURA.md` y
  `docs/architecture/oraculos_dinamicos_humanos_arquitectura.md` /
  `oraculos_dinamicos_reino_sintetico_arquitectura.md` describen sensores y fuentes **como si fueran
  arquitectura**, sin marcar que no están implementados. Este documento **no repite ese patrón**: el
  elenco de §6.1 lleva estado de fuente en cada fila.

**Riesgos de seguridad abiertos que afectan directamente a una unidad `eco-` con suelo:**
**R4** partes fantasma (severidad alta — cualquiera puede fabricar el suelo que va a declarar
conforme) · **R6** T9 no validado en la creación (alta — permite extraer sin contraprestación) ·
**R13** guardián eco con heurística laxa (media). Fuente:
`docs/architecture/blindaje_anti_gamificacion_equidad.md`.

### 12.4 Estado de este documento

**Texto de estándar redactado, con cero piezas de código asociadas.** Este documento **no añade
requisitos de implementación**: hace explícitos los que el suelo ya exigía y no tenía escritos. Las
nueve piezas de §4 son propuesta; las que tienen fuente verificada (balance erosión/formación y
salinidad, más el sellado y la Zona Libre, que son **políticas o doctrinales**, no científicas) están
listas para especificación; **las cuatro sin umbral no deben programarse antes de tener fuente**,
porque *"estándar primero, contabilidad después"* (Cap. 16.5 §16.5.14) y programar un umbral sin
fuente es hacer contabilidad de una ley que no existe.

---

## 13. Preguntas abiertas

Lo que este documento **no** sabe, dicho sin fingir cierre.

1. **¿Existe la densidad aparente crítica?** `[SIN FUENTE VERIFICADA]` — **segundo intento fallido**
   (ya lo era en `09_comparativa.md`). La FAO describe la compactación cualitativamente y no publica
   valor; el archivo histórico que contenía la tabla devolvió **HTTP 500**. *Impacto:* la dimensión 5
   entra a la fórmula sin número, y la dimensión 1 **no puede convertir mm a t/ha sin α**. **Es el
   vacío que más daño hace en cascada a todo el documento.**

2. **¿Cuál es la cifra de COS de referencia por tipo de suelo o bioma?** El **GSOCmap** está
   verificado como producto (200, CC BY) y el **JRC/EUSO** publica el indicador de stock en t C/ha
   [VERIFICADO], pero **no abrí sus capas ni su informe técnico**. Sin cifra de referencia, el SDV-E
   **no puede decir «este suelo está bajo su mínimo de carbono»** y depende de una línea base medida
   localmente. `[SIN FUENTE VERIFICADA]` como número.

3. **¿Cuál es la reserva mundial de carbono en el suelo (Pg C)?** El SWSR de la FAO (2015) la contiene
   y la página está verificada (200), pero **la cifra está en PDF no abierto**. `[SIN FUENTE
   VERIFICADA]`.

4. **¿Es 2 dS/m o 4 dS/m el umbral de salinidad?** El **GSASmap usa CEe > 2 dS/m** [VERIFICADO]; la
   literatura clásica (sistema Richards) usa **4 dS/m** y **no lo pude verificar**. **Este documento
   no resuelve la discrepancia y no escribe 4 dS/m.** Queda abierta, declarada, y como tarea para una
   sesión con extracción de PDF.

5. **¿Cuál es el umbral de contaminación del suelo?** `[SIN FUENTE VERIFICADA]`. La FAO da los
   mecanismos (cadmio por fósforo, nitrógeno a acuíferos) y **ningún valor de disparo**. La dimensión
   7 tiene hoy el umbral más débil del estándar y **este documento no lo disimula**.

6. **¿Existe un umbral de biodiversidad edáfica, o la FAO tiene razón al no publicarlo?** La FAO
   publica **valores característicos de un suelo sano** («más de 1000 especies de invertebrados/m²»,
   «varias especies de lombrices»), que son **descriptores, no umbrales de disparo**. `[SIN FUENTE
   VERIFICADA]` como mínimo aceptable. *Impacto:* el **15 % del ISE («salud del suelo») sigue sin
   número**, y este documento propone sustituir el número por un transecto binario — **propuesta no
   ratificada**.

7. **¿Quién audita a quien exporta el nutriente?** En la dimensión 6, **quien exporta es quien
   declara**. La FAO valida los balances a escala local y regional [VERIFICADO] pero no dice quién los
   verifica. La asimetría estructural del SDV-E (documento 09, §7) **no tiene solución propuesta
   aquí**.

8. **¿Cuántos ciclos consecutivos agravan la violación del suelo?** Este documento propone **3 ciclos
   anuales** `[HIPÓTESIS]` por analogía con los **7 ciclos** del SDV-S (Cap. 9.5 §9.5.10), y **no lo
   ratifica**: la analogía es formal y los dos ciclos miden cosas distintas (años TA frente a ciclos
   TPI). Pertenece al documento 07.

9. **¿El catálogo de la Zona Libre puede auditarse sin volverse refugio?** Si su violación «se
   documenta y no se cuantifica», ¿qué impide que toda degradación no medida se declare inefable? El
   freno propuesto es procedimental (motivo escrito obligatorio + T13 del acto de votación) y **no
   está demostrado que sea suficiente** (§10).

10. **¿El sellado debe medirse neto o bruto, y con qué horizonte?** El objetivo de la UE es **neto**
    (*«no net land take»*), con reutilización de suelo urbano [VERIFICADO]. Un objetivo **neto**
    permite sellar suelo nuevo si se renaturaliza otro **—y ese trueque es exactamente lo que la
    no-compensación prohíbe—**. Este documento **usa el objetivo oficial y declara la tensión sin
    resolverla.**

11. **¿Cuánto suelo está sellado hoy?** `[SIN FUENTE VERIFICADA]`: las guías de la Comisión Europea
    sobre sellado están **bloqueadas (403, CIRCABC)** y el indicador de *land take* de la AEMA está
    **muerto (404)**. **El SDV-E tiene el objetivo (cero) y no la magnitud actual.**

12. **¿Cómo se relaciona cuantitativamente el sellado con la escorrentía y la inundación?** La
    Comisión afirma el efecto cualitativamente [VERIFICADO] y **sin número**. `[SIN FUENTE
    VERIFICADA]`.

13. **¿Cuál es el tiempo de restauración de un suelo degradado, comparable a su tiempo de
    formación?** Tengo la formación (**> 1000 años/cm**, FAO 2017) y tengo «décadas en recuperarse»
    para el suelo tras pérdida de bosque (Stockholm Resilience Centre, 2026) [VERIFICADO] — **pero las
    dos afirmaciones no son la misma magnitud** (formación de perfil frente a recuperación funcional).
    **El SDV-E no debe fundirlas en un solo número.** `[SIN FUENTE VERIFICADA]` como tasa de
    restauración comparable.

14. **¿Existe un umbral de balance de nutrientes que no sea de ámbito agrícola?** `[SIN FUENTE
    VERIFICADA]`, y **la FAO sugiere que no existe por diseño** (utilidad local y regional; el
    documento metodológico de balances está muerto en sus dos rutas, 404). Puede que la pregunta
    correcta no sea «cuál es el umbral» sino **«debe existir uno»**.

15. **¿El factor de violación del suelo y su base neutra?** Este documento propone `FE(0) = 1,0`
    exacto y la forma normalizada (§5.1), y **no lo ratifica**: pertenece al documento 07. Candidato
    argumentado: el balance erosión/formación y la escalera Prevención → Mitigación → Rehabilitación
    con sus horizontes declarados.

16. **¿Qué umbral tiene el suelo para el fuego y la inundación como ciclos?** El canon los manda
    respetar (Cap. 10 §10.4) y este documento declara que **no los convierte en violación** (§4.1),
    pero **no tiene fuente verificada para un régimen de disturbio** (frecuencia, intensidad,
    estacionalidad) ni para el carbono pirogénico como fracción del COS. `[SIN FUENTE VERIFICADA]`.
    *Impacto:* la línea base de la dimensión 2 puede quedar mal fechada si la unidad tiene régimen de
    fuego, y ninguna medición de este documento lo corrige. Pertenece al documento 22.

17. **Las once fuentes PDF que responden 200 y no se abrieron.** Entre ellas están las **fuentes
    primarias correctas** del dominio: el *Soil macrofauna field manual* (protocolo TMA), el informe
    *State of knowledge on soil biodiversity* (FAO, 2020) y el SWSR (FAO & ITPS, 2015). **Una sesión
    con extracción de PDF convierte buena parte de §13 en §4 en minutos.** Es, con diferencia, **la
    tarea de mayor retorno pendiente de esta rama.**

---

## 14. Referencias

**Regla aplicada:** solo URLs con estado HTTP registrado en la sesión de verificación de esta rama
(octubre 2026). Se indica el estado entre paréntesis. **Ninguna cifra de este documento se apoya en
una URL sin estado.** El registro completo de la sesión —62 URLs probadas: 47 verificadas (200),
5 bloqueadas (403), 4 muertas (404), 3 inaccesibles (000), 1 archivo caído (500)— vive en
`scratch/sdv_e/fuentes/14_suelos.md`, que **no es un documento de la biblioteca** y por tanto no se
enlaza aquí como si fuera canon. **Nota de trazabilidad, para que la regla sea verificable:** el
informe de fuentes **no registra el código HTTP** de las cinco URLs ancla de §14.7 (se tomaron del
brief de la rama) ni de las rutas descartadas de §14.9; en este documento esas filas van marcadas
«estado no registrado en el informe de fuentes» o con el código entre paréntesis cuando consta, y
**ninguna sostiene una cifra**.

**Advertencia de alcance, antes de la primera tabla.** De las 47 URLs verificadas, **11 son documentos
PDF que responden 200 pero cuya cifra no se pudo leer** (`web_fetch` no procesa `application/pdf`).
Todas sus cifras van marcadas `[REPORTADO]` y **ninguna sostiene un piso de este documento**. Se
listan porque son citables por una persona y porque **convertirlas a `[VERIFICADO]` es la tarea de
mayor retorno pendiente** (§13, pregunta 17).

### 14.1 El tiempo del suelo (formación, erosión y el balance) — el piso de la dimensión 1

| Fuente | Aporte | URL (estado) |
|---|---|---|
| FAO, 2017 — *Cherishing the ground we walk on* | **> 1000 años para formar 1 cm** de suelo; el suelo como recurso **no renovable**; **33 %** del suelo moderada a altamente degradado (7 procesos enumerados); el suelo alberga **un cuarto** de la biodiversidad planetaria; **95 %** del alimento se produce en suelos | https://www.fao.org/newsroom/story/Cherishing-the-ground-we-walk-on/en (200) |
| Univ. de Washington, 2007 — nota institucional sobre Montgomery, 2007 | **< 0,1 mm/año** de formación; **10 a 100 ×** de erosión bajo agricultura convencional; **E ≈ P** bajo labranza cero; **> 1 mm/año** solo en terreno alpino escarpado; la erosión no compensada por la creación de suelo. **Es la fuente de la cifra** `[VERIFICADO]` | https://www.washington.edu/news/2007/08/08/conventional-plowing-is-skinning-our-agricultural-fields/ (200) |
| Montgomery, D. R., 2007 — *Soil erosion and agricultural sustainability*, **PNAS** 104(33): 13268-13272, doi **10.1073/pnas.0611508104** | **Artículo primario** del que proceden las cifras anteriores. **Bloqueado a automatización (403, Cloudflare)**: se cita para la atribución, **no para la cifra** | https://www.pnas.org/doi/10.1073/pnas.0611508104 (**403**) |

### 14.2 Erosión tolerable, sellado, compactación y degradación física

| Fuente | Aporte | URL (estado) |
|---|---|---|
| USDA-NRCS, *National Soil Survey Handbook* 430-VI (reproducido por California Soil Resource Lab, UC Davis) | **Factor T: 1-5** ton/acre/año; definición operativa de T (*«la calidad de un suelo **como medio para el crecimiento de las plantas**»*) — **umbral agronómico, NO ecológico**: se usa como referencia, no como piso | https://casoilresource.lawr.ucdavis.edu/gmap/help/defn-t-factor.html (200) |
| FAO — Portal de suelos, *Soil health: physical* | Los **tres componentes de la salud física** (ausencia de sellado y encostramiento · ausencia de erosión · ausencia de compactación); **definición de sellado** («identificables fácilmente por teledetección»); efecto y causas de la compactación; definición de encostramiento (*crusting*) | https://www.fao.org/soils-portal/soil-degradation-restoration/global-soil-health-indicators-and-assessment/soil-heath-physical/en/ (200) |
| FAO — Portal de suelos, degradación y restauración | **Definición operativa de degradación** (LADA); definición de **erosión** (*«solo pérdidas absolutas de suelo»*, no cubre toda la degradación); **definición de desertificación** con el **cambio irreversible** (base de T14 en el suelo); escalera **Prevención → Mitigación → Rehabilitación** con horizontes; **la FAO no publica valor numérico de erosión tolerable** | https://www.fao.org/soils-portal/soil-degradation-restoration/en/ (200) |
| Comisión Europea — *Soil health* (DG Environment) | **60-70 %** de los suelos de la UE **no sanos**; coste **50 000 millones €/año**; **95 %** del alimento de la UE viene del suelo; guías de mejores prácticas sobre sellado (en revisión) | https://environment.ec.europa.eu/topics/soil-health_en (200) |
| Comisión Europea — **EU Soil Strategy for 2030** (adoptada 17/11/2021) | **Ningún consumo neto de suelo** (*no net land take*) para 2050; **todos** los ecosistemas de suelo de la UE sanos y resilientes para 2050; lista de las **8 amenazas** al suelo | https://environment.ec.europa.eu/topics/soil-health/soil-strategy-2030_en (200) |
| Comisión Europea — **Soil Monitoring Law** | Primera legislación de la UE sobre suelos; **en vigor 16/12/2025**; transposición nacional 16/12/2028; primer informe de los Estados miembros 16/12/2031 | https://environment.ec.europa.eu/topics/soil-health/soil-monitoring-law_en (200) |
| JRC — EU Soil Observatory (EUSO), indicadores del tablero | Objetivo **suelos sanos 2030: 75 %**; **sellado neto cero** y reutilización de suelos urbanos; indicador de **COS en t C/ha** (C.41 de la PAC); estructura del suelo como indicador | https://joint-research-centre.ec.europa.eu/eu-soil-observatory-euso/eu-soil-observatory-dashboard-indicators_en (200) |
| JRC — EU Soil Observatory (portal) | Misión «Caring for soil is caring for life»; marco general | https://joint-research-centre.ec.europa.eu/eu-soil-observatory-euso_en (200) |
| FAO — Portal de suelos, conservación y agricultura | **50-70 %** del suelo dedicado a agricultura; efecto de la labranza sobre las **hifas fúngicas** y los agregados; respuesta de la biota al disturbio agrícola | https://www.fao.org/soils-portal/soil-biodiversity/soil-conservation-and-agriculture/en/ (200) |

### 14.3 Carbono orgánico del suelo (COS) — dimensión 2

| Fuente | Aporte | URL (estado) |
|---|---|---|
| Musinguzi *et al.*, 2013 — *Journal of Sustainable Development* (registro FAO **AGRIS**) | **Umbral crítico de COS ≈ 2 %**; rango **0,5-2,0 %** por tipo de suelo; y la conclusión de que *«sigue siendo difícil establecer un único valor umbral de COS mínimo o máximo que pueda ser aceptado universal o regionalmente»* → **proxy agronómico, no piso ecológico** | https://agris.fao.org/search/en/records/6903526fb901ffe5ca658954 (200) |
| FAO — Global Soil Partnership, **GSOCmap** | Mapa Mundial de Carbono Orgánico del Suelo: primer mapa global de COS por proceso participativo de países; capas ráster en **t C/ha**, licencia CC BY. **Es un mapa, no un umbral** | https://www.fao.org/global-soil-partnership/gsocmap/en/ (200) |
| FAO — Portal de suelos, GSOCmap (Data Hub) | Ruta de acceso al producto y a sus capas | https://www.fao.org/soils-portal/data-hub/soil-maps-and-databases/global-soil-organic-carbon-map-gsocmap/en/ (200) |
| FAO — **GSOCseq** (potencial de secuestro de COS) | Mapa de potencial de secuestro de carbono orgánico del suelo | https://www.fao.org/soils-portal/data-hub/soil-maps-and-databases/global-soil-organic-carbon-sequestration-potential-map-gsocseq/en/ (200) |
| FAO — Informe técnico del GSOCmap V1.2.0 | Documentación metodológica del mapa | https://www.fao.org/documents/card/en/c/I8891EN (200) |
| FAO — Portal de suelos, indicadores globales de salud del suelo | **El carbono del suelo «trasciende las tres categorías de indicadores (química, física, biológica)»** y está ligado a todas las funciones del suelo: **el argumento oficial para que el COS sea el eje del estándar** | https://www.fao.org/soils-portal/soil-degradation-restoration/global-soil-health-indicators-and-assessment/soil-heath-biological-and-chemical/en/ (200) |
| FAO — Global Soil Partnership, GSOCmap (portal) | Puerta del programa | https://www.fao.org/global-soil-partnership/gsocmap/en/ (200) |
| Informe del **JRC** (Comisión Europea) | *«El umbral inferior del 2 % de carbono orgánico del suelo ha sido usado ampliamente (Kemper y Koch, 1966; Greenland et al.)»* — `[REPORTADO]`: **HTTP 200 pero PDF no abierto** | https://publications.jrc.ec.europa.eu/repository/bitstream/JRC47184/env_vol-i_final2_web.pdf (200, **no abierto**) |

### 14.4 Biodiversidad del suelo y macrofauna — dimensión 3

| Fuente | Aporte | URL (estado) |
|---|---|---|
| FAO — Portal de suelos, *Soil biodiversity* | **Definición FAO de biodiversidad del suelo** (incluida la miríada no visible); función de los organismos del suelo (*«agentes impulsores primarios del ciclo de nutrientes»*); respuesta de la biota al disturbio agrícola | https://www.fao.org/soils-portal/soil-biodiversity/en/ (200) |
| FAO — Portal de suelos, *Soil biodiversity: facts and figures* | **> 1000 especies** de invertebrados por m² en suelos forestales; **composición de un suelo típico sano** («varias especies de lombrices, 20-30 de ácaros, 50-100 de insectos, decenas de nematodos, cientos de hongos, quizás miles de bacterias y actinomicetos»); millones de individuos de bacterias por gramo. **Son descriptores, no umbrales** | https://www.fao.org/soils-portal/soil-biodiversity/facts-and-figures/en/ (200) |
| FAO, 2020 — *State of knowledge on soil biodiversity: status, challenges and potentialities* | Informe principal sobre el estado del conocimiento de la biodiversidad edáfica — `[REPORTADO]` (PDF 200, no abierto) | https://www.fao.org/documents/card/en/c/CB1928EN (200) |
| FAO, 2020 — Resumen para responsables de política del informe anterior | Síntesis de política — `[REPORTADO]` | https://www.fao.org/documents/card/en/c/cb1929en (200) |
| FAO — *Soil macrofauna field manual* (protocolo estándar **TSBF**) | Metodología de campo de macrofauna: **el protocolo que este documento nombra y no transcribe** — `[REPORTADO]` (PDF 200, no abierto) | https://www.fao.org/tempref/docrep/fao/011/i0211e/i0211e.pdf (200, **no abierto**) |
| FAO, C-RESAP — *Soil biology and agriculture* (Module 3) | **≈ 3000 kg/ha** de biomasa viva de lombrices en suelo agrícola (equivalente a seis animales grandes) — `[REPORTADO]` (PDF 200, **no abierto**) | https://www.fao.org/fileadmin/templates/cpesap/C-RESAP_Info_package/Links/Module_3/soil_bio_and_ag.pdf (200, **no abierto**) |
| Comisión Europea / JRC — **ESDAC**, Atlas Global de Biodiversidad del Suelo | Atlas de referencia de biodiversidad edáfica | https://esdac.jrc.ec.europa.eu/content/global-soil-biodiversity-atlas (200) |

### 14.5 Salinidad y sodicidad — dimensión 4

| Fuente | Aporte | URL (estado) |
|---|---|---|
| FAO, 2021 — **GSASmap V1.0.0** (Global Map of Salt-affected Soils), Global Soil Partnership | **Umbrales de clasificación, aplicados conjuntamente: CEe > 2 dS/m · ESP > 15 % · pH > 8,2** (este documento solo usa los dos primeros como disparador: §4 dimensión 4); **> 424 millones ha** afectadas (0-30 cm) y **> 833 millones ha** (30-100 cm); **> 3 %** y **> 6 %** del suelo global; composición 85/10/5 % y 62/24/14 %; 37 % en desiertos áridos y 27 % en estepa árida; 118 países (85 % de la superficie terrestre) y 257 419 puntos medidos | https://www.fao.org/soils-portal/data-hub/soil-maps-and-databases/global-map-of-salt-affected-soils/en/ (200) |
| FAO — Portal de suelos, *Soil health: biological and chemical* | **Minería de nutrientes: solo en áreas agrícolas** (*«no se espera agotamiento bajo otros usos del suelo»*); las **tres degradaciones químicas mayores**; balances útiles a **escala local y regional**; origen de la salinización (*«sistemas de riego mantenidos de forma inadecuada»*); cadmio por fósforo; nitrógeno a agua subterránea | https://www.fao.org/soils-portal/soil-degradation-restoration/global-soil-health-indicators-and-assessment/soil-heath-biological-and-chemical/en/ (200) |

### 14.6 Nutrientes, fronteras planetarias y estado global del suelo

| Fuente | Aporte | URL (estado) |
|---|---|---|
| Stockholm Resilience Centre — **flujos biogeoquímicos** | Frontera **transgredida en ambas variables de control** (nitrógeno y fósforo); el fósforo se libera a las aguas **vía erosión del suelo y escorrentía** (acoplamiento erosión ↔ eutrofización) | https://www.stockholmresilience.org/research/planetary-boundaries/the-nine-planetary-boundaries/biogeochemical-flows.html (200) |
| Stockholm Resilience Centre — **cambio del sistema terrestre** | Frontera **transgredida**; *«los suelos pueden lavarse, perder fertilidad y tardar décadas en recuperarse»*; agricultura y ganadería = **casi el 90 %** de la pérdida forestal reciente | https://www.stockholmresilience.org/research/planetary-boundaries/the-nine-planetary-boundaries/land-system-change.html (200) |
| CBD, 2022 — Marco Kunming-Montreal, **Meta 7** | Reducción **≥ 50 %** del exceso de nutrientes al ambiente y del riesgo de pesticidas y químicos peligrosos para 2030 | https://www.cbd.int/gbf/targets/7 (200) |
| CBD, 2022 — Marco Kunming-Montreal, **Meta 2** | Restauración efectiva de **≥ 30 %** de los ecosistemas degradados para 2030 (**incluye suelos**) | https://www.cbd.int/gbf/targets/2 (200) |
| CBD, 2022 — **Marco Kunming-Montreal** (portal) | Marco global de biodiversidad del que proceden las metas anteriores. Fuente ancla de esta biblioteca | https://www.cbd.int/gbf *(estado no registrado en el informe de fuentes: URL ancla del brief)* |
| IPBES, 2019 — nota de prensa de la Evaluación Global | **23 %** de la productividad terrestre reducida por degradación; **75 %** del ambiente terrestre significativamente alterado (valores de **estado**, no umbrales) | https://www.ipbes.net/news/Media-Release-Global-Assessment (200) |
| UNCCD — **Neutralidad en la degradación de las tierras (LDN)** | *«Sin pérdida neta»* de tierra productiva (ODS 15.3) — ancla doctrinal de la no-compensación del suelo | https://www.unccd.int/land-and-life/land-degradation-neutrality/overview (200) |
| FAO & ITPS, 2015 — *Status of the World's Soil Resources* (SWSR) | *«La mayoría de los recursos de suelo del mundo están en condición solo regular, pobre o muy pobre»*; reserva mundial de carbono en el suelo (**cifra no leída**, PDF) | https://www.fao.org/documents/card/en/c/c6814873-efc3-41db-b7d3-2081a10ede50/ (200) |
| FAO — Portal de suelos, *Cost of Soil Erosion* | Portal temático del coste de la erosión del suelo (**datos no leídos**) | https://www.fao.org/soils-portal/soil-degradation-restoration/cost-of-soil-erosion/en/ (200) |

### 14.7 Contexto: uso del suelo, alimentación y observación de la Tierra

| Fuente | Aporte | URL (estado) |
|---|---|---|
| FAO — Portal de suelos | Puerta del dominio del suelo (fuente ancla de esta biblioteca) | https://www.fao.org/soils-portal/en/ *(estado no registrado en el informe de fuentes: URL ancla del brief)* |
| Copernicus — infraestructura de observación de la Tierra | Infraestructura europea de observación de la Tierra: **fuente candidata de la teledetección del sellado (B1)**. Fuente ancla de esta biblioteca | https://www.copernicus.eu/en *(estado no registrado en el informe de fuentes: URL ancla del brief)* |
| ONU — ODS | Marco de referencia (ODS 15.3, tierra; ODS 2, alimento). Fuente ancla de esta biblioteca | https://sdgs.un.org/goals *(estado no registrado en el informe de fuentes: URL ancla del brief)* |
| UNEP · IPBES · UNCCD (portales) | Marcos institucionales de referencia. El IPBES y la UNCCD tienen además URL específicas citadas arriba (§14.6); estos son sus portales | https://www.unep.org/ *(estado no registrado en el informe de fuentes: URL ancla del brief)* |

**Nota de trazabilidad de la §14.7.** Las cinco filas de esta sección son **fuentes ancla de la
biblioteca**: el brief maestro de la rama las registra como verificadas (HTTP 200) y en la sesión de
fuentes del documento 14 **no se probaron una por una, así que el informe de fuentes no les asigna
código**; su uso aquí es **de puerta de acceso, no de cifra**. Por eso se marcan «estado no registrado
en el informe de fuentes» y **no sostienen ningún piso de este documento**. La única cifra de contexto
que sí procede de una fuente probada en esta sesión es el **95 % del alimento** (FAO, 2017 y Comisión
Europea, §14.2), y su URL está en §14.2.

### 14.8 Fuentes reales que bloquean a los agentes automáticos (403) — citables por una persona

Se listan porque son abribles por un humano y **ninguna sostiene un piso de este documento**: las
cifras asociadas van marcadas `[REPORTADO]` o `[SIN FUENTE VERIFICADA]`.

| Fuente | Aporte | URL (403) |
|---|---|---|
| Montgomery, D. R., 2007 — PNAS 104(33): 13268-13272 | Artículo primario del piso de la dimensión 1. La **cifra** se tomó de la nota institucional de la Univ. de Washington (200); la **atribución** es este DOI | https://www.pnas.org/doi/10.1073/pnas.0611508104 (403) |
| Comisión Europea — **guías de mejores prácticas para limitar, mitigar o compensar el sellado del suelo** | **La fuente que daría el umbral operativo de sellado y el dato de superficie sellada. NO se pudo abrir (CIRCABC)** → es la causa directa de dos de los vacíos de §13 (preguntas 10 y 11) | https://circabc.europa.eu/ui/group/54d2e010-4fc4-4962-9113-1e7d574f4a46/library/c201a601-293f-48b9-abe3-3fea3fdc1a82/details?download=true (403) |
| UNCCD, 2022 — *Debt for Land Restoration* | Daría la cifra de **≈ 20 %** de tierra global degradada — `[REPORTADO]`, **no abierta**. La UNCCD se cita por `https://www.unccd.int/land-and-life/land-degradation-neutrality/overview` (200) | https://www.unccd.int/sites/default/files/2022-05/220509_UNCCD_Debt_for_Land_Restroration_Report.pdf (403) |

### 14.9 Rutas descartadas (no citables en este documento)

**Muertas (404):**

- `https://www.fao.org/iran/news/detail-events/zh/c/357388` — ruta antigua de FAO News con el 33 % de
  degradación. **Sustituida con ventaja** por la nota de 2017 (200), que da el mismo dato con fecha.
- `https://www.fao.org/global-soil-partnership/gsocseq/en/` — ruta corta del GSOCseq (**viva** en
  `/soils-portal/data-hub/…`, §14.3).
- `https://www.fao.org/3/y5066e/y5066e00.htm` **y** `https://www.fao.org/docrep/006/y5066e/y5066e00.htm`
  — *Assessment of soil nutrient balance* (FAO Fertilizer and Plant Nutrition Bulletin #14), **muerta
  en sus dos rutas**. Consecuencia: **el umbral de nutrientes queda `[SIN FUENTE VERIFICADA]`** por
  inaccesibilidad del documento metodológico (§13, pregunta 14).
- `https://www.eea.europa.eu/en/analysis/indicators/land-take` — indicador de *land take* de la AEMA:
  **muerta**. Consecuencia: sin magnitud actual del sellado (§13, pregunta 11).

**Inaccesibles (000, sin respuesta HTTP):**

- `https://eur-lex.europa.eu/eli/dir/2025/2360/oj` y
  `https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A52021DC0699` — **EUR-Lex no responde
  desde automatización**. La Soil Monitoring Law y la Soil Strategy se citan por las páginas de la
  Comisión (200).
- `https://www.stockholmresilience.org/research/planetary-boundaries.html` — la **página índice** no
  respondió en el lote de esta sesión, aunque las **páginas hijas sí (200)**. Se citan siempre las
  URL específicas.

**Archivo caído (500):**

- `https://web.archive.org/web/20230507054358/http://soilquality.org/indicators/bulk_density.html` —
  **el intento directo de cerrar el vacío de densidad aparente, y falló.** El dominio original
  `soilquality.org` está dado de baja. Es la causa del vacío más grave del documento (§13, pregunta 1).

**No citables por falta de lectura o de pertinencia:**

- `https://www.fao.org/3/i5126e/I5126E.pdf` (SWSR, resumen técnico) · `…/cb1928en/cb1928en.pdf` ·
  `…/cb1929en/cb1929en.pdf` · `…/i0211e/i0211e.pdf` (manual de macrofauna) ·
  `…/ca9215en/ca9215en.pdf` (mapeo de suelos afectados por sales) · `…/a-bl813e.pdf` (Directrices
  voluntarias para la gestión sostenible del suelo) — **todas 200 por HTTP y todas PDF no abiertas**:
  reserva documental, **no fuente de cifra**.
- `https://esdac.jrc.ec.europa.eu/themes/soil-biodiversity` — página de portal, sin umbral numérico.
- `https://www.nrcs.usda.gov/state-offices/illinois/soil-tech-note-16a-compacted-zone-in-soil` — el
  contenido útil está en un PDF enlazado no abierto.
- Rutas de sellado y umbrales halladas en búsqueda y **no comprobadas**
  (`jcerni.rs`, `laukutikls.lv`, `zenodo.org/records/14013998`, `zenodo.org/records/10391033`,
  `sns.uba.de/chronik/…`): no aportan cifra propia y **no entran**.
- **El «4 dS/m» del sistema Richards**: `[SIN FUENTE VERIFICADA]` — todas las rutas son PDF.
  **Este documento usa 2 dS/m (FAO, 2021) y declara la discrepancia** (§13, pregunta 4).
- Cualquier valor de **«lombrices por m²»** de manuales nacionales o guías de campo: aparecieron en
  búsqueda, **son literatura secundaria y no se abrieron**. **No entran** y **no se usan como piso**.

### 14.10 Referencias internas al canon (por sección, sin anclas de línea)

- Cap. 5 §5.2-§5.5 — Tres tiempos (TVI, TA, TPI), axioma T7 (Jerarquía Temporal), PIU como **único**
  traductor TA↔TVI, y el costo en TA del bosque: [capitulo_05_arquitectura_260126.md](../../book/edicion_3_dinamica/capitulo_05_arquitectura_260126.md)
- Cap. 7 §7.9 — Zona Libre (el valor inefable): [capitulo_07_vhv_260126.md](../../book/edicion_3_dinamica/capitulo_07_vhv_260126.md)
- Cap. 8 §8.3-§8.6 y §8.11 — Criterios de validación, dimensiones, fórmula, pesos, frecuencias y **las
  dimensiones binarias VIII y IX** (precedente directo de B1 y B2 de este documento):
  [capitulo_08_sdv_h_260126.md](../../book/edicion_3_dinamica/capitulo_08_sdv_h_260126.md)
- Cap. 9 §9.3-§9.9 — Criterios, dimensiones por especie, factor de sufrimiento y árbol de la base de
  datos de SDV: [capitulo_09_sdv_a_260126.md](../../book/edicion_3_dinamica/capitulo_09_sdv_a_260126.md)
- Cap. 9.5 §9.5.5-§9.5.11 — `FS_S = e^v` y **base neutra 1,0**, sensores nombrados, INV2-S y
  retractación a **7 ciclos**, Veto por Crimen de Coherencia:
  [capitulo_09_5_sdv_sinteticos_260126.md](../../book/edicion_3_dinamica/capitulo_09_5_sdv_sinteticos_260126.md)
- Cap. 10 §10.3-§10.8 — Principio Precautorio de Consciencia, **SDV Universal (ecosistemas, lugares,
  objetos) §10.4**, proporcionalidad, **dignidad encadenada**, **gobernanza operacionalmente finita
  §10.7** y Persona Sintética: [capitulo_10_tres_reinos_260126.md](../../book/edicion_3_dinamica/capitulo_10_tres_reinos_260126.md)
- Cap. 16.5 §16.5.14 — El Reino Natural como conviviente: crédito regenerativo `r_units`, **TA no
  colonizado**, representación `eco-` con guardián oráculo, Zona Libre, **«el suelo antes que el
  saldo»**, cuidado ≠ extracción estética: [capitulo_16_5_micromaxocracia_canonica_220826.md](../../book/edicion_3_dinamica/capitulo_16_5_micromaxocracia_canonica_220826.md)
- Cap. 17 — INV2 e invariantes de MaxoContracts: [capitulo_17_maxocontracts_260126.md](../../book/edicion_3_dinamica/capitulo_17_maxocontracts_260126.md)
- **EVV-1.2 §4.3** — R negativo = regeneración: [capitulo_18_EVV_1.2_270126.md](../../book/edicion_3_dinamica/capitulo_18_EVV_1.2_270126.md)
- Índice de Salud Ecosistémica (IN-01), con **«Salud del suelo» = 15 %**, bandas y umbrales de alerta:
  [metricas_detalle_kpis_oraculos_dinamicos.md](../../architecture/metricas_detalle_kpis_oraculos_dinamicos.md)
- Estándar SDV-S y su comparativa inter-reinos: [SDV-S_Suelo_Dignidad_Vital_Sinteticos.md](../SDV-S_Suelo_Dignidad_Vital_Sinteticos.md)
- SDV como principio universal e INV2-S: [SDV_Suelo_Dignidad_Vital_importancia_MaxoContracts.md](../SDV_Suelo_Dignidad_Vital_importancia_MaxoContracts.md)
- Comparativa inter-reinos de esta biblioteca (los 16 ejes y los insights I1-I12, citados en §11):
  [09_Comparativa_inter_reinos.md](09_Comparativa_inter_reinos.md)
- Riesgos **R4, R6 y R13**: [blindaje_anti_gamificacion_equidad.md](../../architecture/blindaje_anti_gamificacion_equidad.md)

---

**Cierre.** El suelo es el ecosistema del Reino Natural donde el canon tenía un mandato, un peso del
15 % en el ISE y **ni un solo umbral escrito**. Este documento pone nueve piezas sobre la mesa y dice
de cada una si tiene fuente: **tres la tienen de verdad** —el balance erosión ≤ formación (Montgomery,
2007), los umbrales de salinidad del GSASmap (FAO, 2021) y el umbral del COS, que es un **proxy
agronómico** y se declara como tal—, **una es doctrinal y política** (la Zona Libre y el sellado neto
cero, que no son ciencia del suelo) y **cuatro no la tienen** (biodiversidad edáfica, compactación,
nutrientes y contaminación). No cierra esas cuatro: las declara. De las ocho amenazas que la UE
reconoce al suelo, **solo la salinización tiene hoy un umbral numérico con fuente publicada**: la
erosión tiene un balance pero no un valor tolerable, la materia orgánica solo un proxy agronómico, y
las cinco restantes (inundaciones y deslizamientos, contaminación, compactación, sellado y pérdida de
biodiversidad) ningún valor de disparo. Ese es el resultado honesto de la investigación, no un defecto
de redacción.

Lo que este documento aporta a la familia SDV no es una cifra nueva: es **un piso que es una razón de
flujos** —erosión ≤ formación, la única forma de un piso que no se cumple degradando despacio—, **una
dimensión binaria donde el piso y el óptimo son el mismo cero**, y **una irreversibilidad que no hay
que construir porque la FAO ya la definió**. Todo lo demás queda dicho como lo que es: **propuesta no
ratificada**, pendiente del documento 07 (fórmula y pesos), del 08 (INV2-E), del 06 (elenco de
sensores) y, en último término, del Parlamento.
