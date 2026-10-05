# Conectividad ecológica (dimensión transversal del SDV-E)
## La dimensión que sostiene la biodiversidad y que hoy no tiene piso —probabilidad de conectividad (PC), tamaño efectivo de malla, índice de fragmentación, anchura de corredor y distancia al vecino más cercano—: el único umbral con fuente que existe (CSI ≥ 95 %, Grill *et al.*, 2019), el desdoblamiento que el 0,000 del catálogo exige, y la explicación exacta de qué haría falta para cerrar el vacío

**Autoría:** Oráculo Sintético DeepSeek & Max Nelson López Restrepo
**Fecha:** octubre 2026
**Proyecto:** Maxocracia — El gobierno de la verdad, el tiempo y la vida
**Licencia:** Creative Commons BY-SA 4.0
**Estado:** Propuesta de estándar (rama SDV-E, Ola 4) — NO canon hasta ratificación
**Referencia canónica:** Cap. 10 §10.4 · Cap. 16.5 §16.5.14 · EVV-1.2 §4.3 · Cap. 9.5 (precedente SDV-S)
**Documento:** 21 de la biblioteca `docs/theory/SDV-E/`
**Revisión:** octubre 2026 — redactado contra el informe de fuentes verificado de esta rama (`scratch/sdv_e/fuentes/21_conectividad.md`) y contra la lectura directa de los documentos 01 a 20 de esta biblioteca. **Verificación propia de esta sesión de redacción, con estado HTTP real y cuerpo descargado:** 17 URLs comprobadas con `curl` (`-w "%{http_code}|%{size_download}"`), todas con respuesta **200** y cuerpo no vacío (§14.1). **Dos lecturas directas nuevas, hechas aquí y no heredadas del informe:** (a) las leyendas de la **Fig. 2** del artículo de *Nature* (2019), donde el umbral de **95 % de CSI** aparece escrito —sin acceso al texto completo de pago, la leyenda de figura sí es pública—, y (b) la **Tabla 6.2**, la **Caja 6.2**, la **Tabla 5.5** y la descomposición de **dPC/dIIC** del documento de directrices de NatureConnect (2024), extraídos del PDF con PyMuPDF en esta sesión. Los textos de la UICN (2020), la CMS (Res. 14.16) y la CBD se **consumen del informe de fuentes de la rama**, que los extrajo íntegros: aquí se verifica su URL y su tamaño, **no se re-extrae su texto**, y así se declara.

---

## 1. Qué es (y qué no es) este SDV

**Qué es.** Este documento fija **una sola dimensión** del SDV-E —la **conectividad ecológica**— y la
fija **como dimensión transversal**: el mismo objeto para un bosque, un humedal, un río, un arrecife, una
pradera o un agroecosistema. No es la dimensión de mayor peso (0,075 frente al 0,300 de la biodiversidad),
pero es **la más importante de esta biblioteca por lo que le falta**: es la única fila del catálogo que el
[documento 07](07_Formula_de_violacion_y_pesos.md) §5.3 deja con **peso en el tablero (0,075) y peso cero
en el piso (0,000)**, y la única, junto con el oxígeno disuelto, cuya ausencia de umbral está **declarada
como vacío** en el [documento 08](08_INV2-E_invariante.md) §4.2 y §5.2. El [documento 07](07_Formula_de_violacion_y_pesos.md)
§13 la registra como pregunta abierta 8; el [documento 02](02_Unidad_y_sujeto_del_SDV-E.md) §12 la deja
bloqueada como **U-11** (*«ancho funcional de corredor entre ocurrencias»*), con esta frase que es una
delegación explícita: *«La cifra pertenece al documento 21»*. Este documento responde a esa delegación,
y lo hace separando lo que **sí** tiene fuente de lo que **no** la tiene.

**El hallazgo, sin rodeos y por adelantado.** El 0,000 del catálogo **no es del todo cierto y no es del
todo falso: es la consecuencia de haber metido dos objetos distintos en una sola fila.** La conectividad
que el canon nombra para un ecosistema (Cap. 10 §10.4: *«Conectividad con otros ecosistemas»*) y la
conectividad que un río puede medir sobre sí mismo **no son la misma cosa** y **no tienen el mismo
destino**:

| | **Parámetro A — conectividad longitudinal / fluvial** | **Parámetro B — conectividad de paisaje** |
|---|---|---|
| Qué mide | si el continuo del río sigue siendo un continuo: función hidrológica observada | si los parches de hábitat están unidos en un grafo: **estructura** del paisaje |
| Instrumento con fuente | **CSI** (Conectividad de Estado, índice 0-100) con umbral explícito | PC, IIC, ECA, dPC, tamaño efectivo de malla, fragmentación, distancia al vecino más cercano |
| ¿Tiene umbral publicado? | **Sí: CSI ≥ 95 %** para que un tramo cuente como *de flujo libre* (Grill *et al.*, 2019) `[VERIFICADO en esta sesión: leyenda de la Fig. 2]` | **`[SIN FUENTE VERIFICADA — pendiente de consenso científico]`** |
| Régimen jurídico del umbral | umbral **de clasificación publicado por la fuente**, adoptarlo como piso es **decisión de política del proyecto** → `PROPUESTA NO RATIFICADA` | no hay umbral que adoptar |
| Aplica a | ríos, cuencas, humedales con conexión hidrológica, tramos con barreras | bosques, praderas, agroecosistemas, marino-costero, suelo vivo |

**La frase que este documento puede escribir y que ningún otro de la biblioteca podía escribir todavía:**
existe **un** umbral de conectividad con fuente institucional fuerte y es **fluvial**. No existe —y se
buscó, y las instituciones lo admiten por escrito— **ninguno** para la métrica de paisaje. El catálogo no
puede salir de 0,000 por la vía de la investigación; **sí puede salir por la vía de una decisión de
política declarada como tal**, y esa decisión tiene un coste aritmético que este documento publica con
números en §5.3 en lugar de esconderlo.

**Qué no es.**

- **No es el estándar por tipo de ecosistema.** Los umbrales estructurales y físicos de cada tipo
  —cobertura y borde del bosque, hidroperiodo del humedal, régimen de caudal del río, herbivoría de la
  pradera, matriz cultivada del agroecosistema— pertenecen a los documentos **10 a 18**. Aquí se fija **el
  instrumento común** y la **frontera** entre lo que este documento hereda y lo que no.
- **No es una métrica nueva.** Este documento **no inventa un índice de conectividad**: ordena los que
  existen, verifica cuáles pueden ser piso y cuáles no, y **publica los que no pueden**.
- **No es el «30×30» del Marco Kunming-Montreal.** El 30 % del GBF es **superficie** y la Meta 3 pide que
  esa superficie esté *«ecológicamente representativa, **bien conectada** y gobernada equitativamente»*:
  la conectividad es **condición**, no cifra `[VERIFICADO]`. Un sistema de redes «bien conectado» es una
  condición cualitativa y entra en la columna del **Óptimo (votable)**, nunca en la del piso.
- **No es el ISE.** El Índice de Salud Ecosistémica **no incluye conectividad en absoluto** —es una de las
  dos dimensiones que el canon nombra y el ISE omite, junto con el caudal ecológico— `[VERIFICADO en
  `docs/architecture/metricas_detalle_kpis_oraculos_dinamicos.md`, IN-01]`. El ISE es el **tablero**; esta
  dimensión aspira a ser una pieza del **juez**.
- **No es el Índice de Conectividad Dendrítica (DCI).** El [documento 12](12_Ecosistemas_Rios_y_cuencas.md)
  §Dimensión V pidió expresamente a este documento que verificara el DCI (Cote *et al.*, 2009). **No se
  verificó: ni su URL ni su escala**, y por tanto **este documento no lo adopta** (§13, pregunta 5). La
  petición queda registrada como incumplida, no como resuelta.
- **No está implementado.** 🔴 No existe `SDV_E` en `maxocontracts/core/types.py`, no existe
  `sdv_e_validator.py`, no existe INV2-E y **no hay un solo sensor, inventario ni ingestador de
  conectividad en el repositorio**. La búsqueda de `conectividad`, `connectivity`, `corredor` y `CSI` en
  `app/`, `maxocontracts/`, `tests/` y `scripts/` devuelve **cero coincidencias ecológicas** y dos
  **homónimos** que hay que nombrar para que nadie los lea como implementación (§12). La tabla honesta
  está en §12.

**Las cuatro marcas de evidencia, y por qué la cuarta es el resultado principal.** `[VERIFICADO]` =
comprobado con herramienta en esta sesión de redacción o leído directamente en el archivo citado.
`[REPORTADO]` = afirmado por la fuente citada sin haber podido abrir el documento primario. `[HIPÓTESIS]`
= inferencia razonada del proyecto, no observación. `[SIN FUENTE VERIFICADA — pendiente de consenso
científico]` = se buscó el número y **no existe fuente verificable**. En una dimensión cuyo hueco es el
tema, la cuarta marca no es una derrota: es **la respuesta**. Y hay una quinta etiqueta que esta dimensión
necesita y que las demás no: **`[ESTADO MEDIDO]`**, porque las cifras más citadas de la literatura de
conectividad —**37 %** de los ríos de más de 1 000 km permanecen de flujo libre en toda su longitud,
**23 %** fluyen sin interrupción hasta el océano— **miden el mundo; no fijan su ley**, y copiarlas como
piso equivaldría a declarar que el estado actual del planeta es el mínimo aceptable. El
[documento 12](12_Ecosistemas_Rios_y_cuencas.md) ya nombró ese error como *«el más tentador»*; aquí se
hereda la advertencia con su número.

**Una corrección de trazabilidad que este documento debe hacer, y no la hace por gusto.** El
[documento 02](02_Unidad_y_sujeto_del_SDV-E.md) §12.3 y §13 registraron que las directrices de
conectividad de la UICN (2020) *«existen y responden, pero su contenido no se pudo extraer (fallo de
parseo del PDF, tres intentos)»*. El informe de fuentes de esta rama identificó la **causa raíz**, y no
era el extractor: **el archivo guardado en el repositorio de trabajo con el nombre
`scratch/sdv_e/tmp/iucn_connectivity.pdf` no contenía las directrices de conectividad** —era un informe
sobre Soluciones basadas en la Naturaleza en las contribuciones determinadas nacionalmente—. **La
conclusión del documento 02 no cambia** (en la fuente no hay umbral numérico), pero **el motivo
registrado es incorrecto** y debe corregirse en la revisión de coherencia: no fue un fallo de
herramienta, fue **el documento equivocado** (§13, pregunta 6).

---

## 2. Preámbulo metodológico

El SDV-H lo tiene y el SDV-S lo omitió; el brief prohíbe repetir la omisión. En una dimensión
**transversal** el preámbulo tiene una función añadida y específica: una métrica de conectividad mal
formada no mide peor **que otra**, mide **otra cosa** —el paisaje en lugar de la unidad, la estructura en
lugar de la función, la ventana elegida por el analista en lugar del ecosistema—, y lo hace sin avisar,
porque el número sale igual de limpio. Estas son las nueve reglas con las que se escribió lo que sigue.

**Regla 1 — Conectividad estructural y conectividad funcional no son intercambiables.** La UICN (2020)
distingue subdefiniciones y da la definición operativa: *«la conectividad ecológica es el libre movimiento
de especies y el flujo de los procesos naturales que sostienen la vida en la Tierra»* `[VERIFICADO vía
informe de fuentes de la rama: texto de la UICN, 2020, glosario y resumen ejecutivo]`. Las métricas de
paisaje (**PC, IIC, malla efectiva, fragmentación**) miden **estructura**; el **CSI** mide **función
hidrológica observada**. El propio documento de directrices de NatureConnect (2024) lo separa en su
Tabla 5.5 —*«ejemplos de varias métricas de conectividad **estructural**»*— y trata la conectividad
fluvial en una sección aparte, con cuatro dimensiones de análisis propias `[VERIFICADO en esta sesión:
texto extraído del PDF]`. Consecuencia dura: **ninguna conclusión de este documento se obtiene mezclando
las dos familias**, y cuando una unidad solo tenga métrica estructural, su estado será estructural y se
dirá así.

**Regla 2 — Dos objetos en una fila es un error de catalogación, y la corrección es desdoblar.** El
`conectividad_indice` del catálogo del [documento 08](08_INV2-E_invariante.md) §4.1 no tiene unidad ni
operador declarados (`— | —`), precisamente porque en una sola fila no caben el CSI (porcentaje de un
río), la malla efectiva (un área), la distancia al vecino más cercano (una longitud) ni un índice de
grafo (adimensional). **Ningún umbral puede asignarse a una fila sin unidad.** Desdoblar no es añadir una
dimensión al estándar: es **restituir la unidad física** que la fila perdió.

**Regla 3 — El área de referencia es parte del umbral, no una nota al pie.** Un índice de paisaje se
calcula **dentro de una ventana** que elige quien mide. El propio documento de directrices declara que,
con el enfoque de ventana móvil, *«los rangos resultantes en los que operan algunas métricas de
conectividad cambiarán, porque ahora están confinadas a un tamaño predeterminado de ventana»*, y que eso
aplica justamente a las métricas cuyo rango es **[0, +∞)**: distancia al vecino más cercano, tamaño
efectivo de malla, hábitat dentro de un búfer, radio de giro, índice de proximidad `[VERIFICADO en esta
sesión: texto extraído, p. 80 del PDF]`. Por tanto: **un piso sobre un índice de paisaje sin declarar el
área de referencia es un piso sobre la ventana del analista**, y es la forma más barata de fabricar
cumplimiento. Este documento convierte la declaración del área de referencia en **campo obligatorio de
admisibilidad** (§6.2).

**Regla 4 — La conectividad puede mejorar en el índice mientras la unidad se pierde, y esa es la razón
técnica del 0,000.** `[HIPÓTESIS de este documento, y corrección de una hipótesis de la rama]` El informe
de fuentes de esta rama afirmó que la conectividad *«es la única dimensión del catálogo que sube cuando la
unidad desaparece y el vecino mejora»*. **Tomado literalmente, eso es falso para PC e IIC**: ambas son
sumas de términos no negativos y **retirar un parche solo puede bajar el índice**, nunca subirlo. Lo que
sí es cierto —y basta para invalidar un piso de unidad— es lo siguiente, y está en la fuente: la
contribución de un parche se descompone en **área propia** (`dPCintra`), **conexión con los vecinos**
(`dPCflux`) y **papel de trampolín** (`dPCconnector`), con `dPC = dPCintra + dPCflux + dPCconnector`
`[VERIFICADO en esta sesión: texto extraído, p. 70 del PDF, atribuido a Saura y Rubio, 2010]`. De ahí se
sigue, sin salir de la fuente: **la contribución de la unidad puede caer a cero mientras el índice
agregado se mantiene alto gracias a los vecinos**, y el índice **no detecta la pérdida de la unidad** si
el resto de la ventana está bien conectado. Un piso sobre ese índice no protege la unidad: protege el
promedio de la ventana. Se marca como `[HIPÓTESIS]` porque la deducción es del proyecto; la descomposición
de la que se deduce, no.

**Regla 5 — Mínimo Absoluto y Óptimo son dos columnas y dos regímenes jurídicos.** El piso es **LEY** y
**no se vota**; la plenitud aspiracional es **POLÍTICA** y **sí se vota** (precedente del Parlamento
Educativo, INV2-EDU: categoría `critical`, quórum 60 %, consenso 75 %, T13, anti-flip-flop 14 días,
`CHECK` en BD). En conectividad las dos columnas van separadas **incluso cuando el Óptimo está vacío**,
que es el caso de casi todas las filas de §4: *la ciencia publica pisos de riesgo, no plenitudes*
([documento 07](07_Formula_de_violacion_y_pesos.md) §4.3).

**Regla 6 — El piso y el peso son independientes, y esa independencia es la que permite que esta
dimensión deje de ser impotente.** Regla 1 de [documento 08](08_INV2-E_invariante.md) §5.2, citada
literalmente: *«Un parámetro **con umbral** produce `violacion` aunque su peso sea cero (P1, atomicidad);
el peso solo dimensiona `v` y `FE`»*, con el precedente ya operativo de `arrecife_dhw` —que tiene piso y
**no** tiene peso propio en el vector base—. Consecuencia para este documento: **puede proponerse un piso
de conectividad sin tocar ni un solo peso ratificado**, y el efecto inmediato no es aritmético sino
jurídico: la unidad puede **bloquear**. Eso sí: la propuesta exige revisar la tabla de §4.2 del documento
08, que hoy lista la conectividad entre los **seis dominios que no pueden activar INV2-E**. **Este
documento no la cambia por su cuenta** (§5.3 y §13, pregunta 2).

**Regla 7 — El tiempo del territorio manda.** La duración se acumula en **TA (Tiempo Absoluto)** y
*«el tiempo del territorio es TA y no se coloniza (el PIU traduce)»* (Cap. 16.5 §16.5.14). El único
traductor TA↔TVI es el **PIU** (Protocolo de Intercambio Universal, Cap. 5 §5.5). En esta dimensión la
regla tiene un filo propio: **una barrera hidráulica y un corredor fragmentado operan en ciclos
generacionales, no anuales** —el continuo fluvial y la maduración de un corredor de bosque son procesos de
escala multidecenal, no anual— **`[HIPÓTESIS]`: la rama no verificó ninguna fuente que publique un tiempo
de recuperación de continuidad fluvial ni de maduración de corredor, de modo que aquí se afirma la escala
cualitativamente y no con un número**, de modo
que **la unidad del ciclo TA (documento 07 §5.4b, sin decidir y sin fuente) importa aquí más que en
ninguna otra dimensión** y su elección no puede hacerse por comodidad de implementación (§13, pregunta 12).

**Alcance de ese `[HIPÓTESIS]`, para que no se lea como un dato cada vez que reaparece.** Toda afirmación
de **escala temporal** de este documento —«décadas», «siglos», «multidecenal», y el contraste entre la
duración de una barrera y la maduración de un corredor— **pertenece a esta misma hipótesis y no tiene
fuente verificada en la rama**. Se repite en §6.4, §8.4, §9 y §13 pregunta 12, y en **ninguna** de esas
apariciones debe leerse como una cifra publicada. **Si la revisión de coherencia encuentra una fuente de
tiempos de recuperación de continuidad fluvial o de maduración de corredor, la marca se retira en los
cinco lugares a la vez**; hasta entonces, el documento afirma la **desproporción** entre escalas —que es lo
que sostiene el argumento— y **no la magnitud**.

**Regla 8 — Ningún dato entra sin procedencia, y esta dimensión añade dos campos a los cuatro del
contrato.** Una medición entra en el cálculo **solo** si trae `valor` + `unidad`, `ta_periodo` en TA,
`fuente_dato` y `evidencia_ref` ([documento 08](08_INV2-E_invariante.md) §6.1). Aquí se añaden dos más,
porque sin ellos el número no es interpretable: **`area_de_referencia_declarada`** (Regla 3) y
**`grupo_taxonómico_declarado`** (§4.3; sin él, el piso de anchura de corredor es elegible por el
interesado, y una anchura de 41 m es cumplimiento si se declara «plantas» e incumplimiento si se declara
«mamíferos grandes»).

**Regla 9 — Sin dato no castiga, sin dato no aprueba, y sin monitoreo no hay crédito.** *«La duda sin
evidencia no castiga»* (INV2-EDU) se conserva con la corrección que el [documento 08](08_INV2-E_invariante.md)
§8.4 ya fijó: **«sin castigo» no es «aprobación»**. En esta dimensión eso tiene una consecuencia que se
puede escribir en una línea: **hoy, con cero sensores y cero inventarios, el estado por defecto de
cualquier unidad en conectividad es `indeterminado`** —no hay bloqueo por piso, **hay bandera de opacidad
ecológica**, obligación de instrumentar y **crédito regenerativo no acreditable** (§8.3).

---

## 3. Pilares epistemológicos

### 3.1 La definición canónica que hay que adoptar (y por qué se adopta esta y no otra)

> *«La conectividad ecológica es el libre movimiento de especies y el flujo de los procesos naturales que
> sostienen la vida en la Tierra. Esta definición está respaldada por la Convención sobre las Especies
> Migratorias de Animales Silvestres (CMS, 2020).»* — UICN (2020), glosario y resumen ejecutivo
> `[VERIFICADO: texto extraído en la sesión de fuentes de la rama; URL y tamaño comprobados en esta
> sesión]`

Y la misma definición en la letra de la resolución vinculante, que es la que da rango normativo al
concepto:

> *«Bearing in mind that ecological connectivity (hereafter "connectivity") is the unimpeded movement of
> species, connection of habitats without hinderance and the flow of natural processes that sustain life
> on Earth»* — UNEP/CMS, **Resolución 14.16**, adoptada en la COP14 (Samarcanda, febrero 2024)
> `[VERIFICADO]`

**Lo que esta definición obliga a medir y lo que prohíbe medir.** Obliga a medir **movimiento** y
**flujo**, no solo geometría: un paisaje con parches geométricamente unidos por una franja de hormigón no
es un paisaje conectado. Y prohíbe la lectura inversa: la definición **no incluye ninguna cifra**, y
ningún documento de los verificados en esta rama la convierte en cifra (§3.7). La definición es,
literalmente, **una condición sin umbral**: exactamente el hueco que el catálogo del
[documento 08](08_INV2-E_invariante.md) §4.1 registra con `[SIN FUENTE VERIFICADA]`.

### 3.2 La evidencia de que la conectividad sostiene la biodiversidad

La dimensión no se justifica por elegancia conceptual. Se justifica porque **la fragmentación es una de
las causas primarias del declive de la biodiversidad**, y eso está dicho por las instituciones que fijan
el marco, no por este proyecto:

| Afirmación | Formulación de la fuente | Fuente | Estado |
|---|---|---|---|
| La pérdida y fragmentación de hábitats está entre las causas principales del declive | *«La pérdida y fragmentación de hábitats son de las causas [principales del declive de la biodiversidad]»*; *«la fragmentación ocasionada por las actividades humanas sigue perturbando los hábitats, amenazando a la biodiversidad y obstaculizando la adaptación al cambio [climático]»* | UICN (2020), Lineamientos n.º 30, resumen ejecutivo | `[VERIFICADO vía informe de fuentes de la rama]` |
| La fragmentación amenaza específicamente a las especies migratorias | *«habitat destruction and fragmentation are among the primary threats to migratory species, and [...] the identification and conservation of habitats of appropriate quality, extent, distribution and connectivity are thus of paramount importance»*; *«Deeply concerned that habitats for migratory species are becoming increasingly fragmented across terrestrial and aquatic biomes»* | UNEP/CMS, Resolución 14.16 (COP14, 2024) | `[VERIFICADO]` |
| La conectividad es **condición** de la restauración, no su adorno | La Meta 2 del GBF exige que la restauración *«enhance biodiversity and ecosystem functions and services, ecological integrity and connectivity»* | CBD (2022), Decisión 15/4 | `[VERIFICADO]` |
| La integridad y la conectividad son objetivo de primer nivel del marco global | *«La integridad, la conectividad y la resiliencia de todos los ecosistemas se mantienen, mejoran o restauran»* (Meta A) | CBD, informe de progreso de indicadores, SBSTTA 28 | `[VERIFICADO]` |
| Los propios Estados reconocen la brecha | **41 %** de las Partes de la CBD declaran metas nacionales que ligan restauración y conectividad; **menos del 40 %** ligan restauración y biodiversidad | CBD, SBSTTA 28, informe de progreso (Tabla 6) | `[VERIFICADO]` |
| La falta de información global sobre corredores es un problema **reconocido por escrito** | *«The lack of global-level information on the extent and effectiveness of ecological corridors limits our understanding of the current state of biodiversity»* — motivo declarado de la creación del **World Database on Ecological Corridors (WDEC)**, prototipo de UNEP-WCMC con el grupo especialista de la UICN | UNEP-WCMC / Protected Planet (2026) | `[VERIFICADO]` |
| Hay una alianza internacional específica sobre esto | *«Global Partnership on Ecological Connectivity»* (CMS + CBD + UNCCD + Convención de Humedales + Banco Mundial + UNEP-WCMC), cuyo fin declarado es *«maintain, restore and enhance ecological connectivity across the globe by improving connectivity data and knowledge»*, con un **Atlas global de migración animal** | CBD, SBSTTA 28 | `[VERIFICADO]` |

**Lectura de esta tabla, sin adornos.** Cuatro cosas quedan probadas: (a) la conectividad **sostiene** la
biodiversidad y las instituciones lo dicen en sus instrumentos vinculantes; (b) es **condición** de las
metas globales de restauración y conservación; (c) **no tiene cifra** en ninguno de esos instrumentos; y
(d) **la ausencia de cifra y de inventario global está admitida por las propias instituciones** que
crearon una base de datos específica para empezar a cubrirla. El hueco de este documento no es un hueco
de este proyecto: es un hueco **documentado del régimen internacional de biodiversidad**, y decirlo con
la cita de la UNEP-WCMC es más fuerte que decir «no encontramos nada».

### 3.3 El instrumento existe, el umbral no (y esta distinción es el corazón del documento)

El hueco del catálogo **no es de instrumento**: el [documento 06](06_Medicion_y_verificacion_T13.md) ya
lo había clasificado como **«D5 Conectividad | 🟢 instrumento | 🔴 sin umbral»**. Lo que faltaba era
**norma**. La Tabla 5.5 del documento de directrices de NatureConnect (2024) enumera las métricas
estructurales con su definición y su referencia —**y ninguna columna de umbral**—. Estas son, leídas
directamente del PDF en esta sesión:

| Métrica | Qué mide, según la fuente (traducción literal) | Referencia que da la fuente | Rango declarado | Umbral |
|---|---|---|---|---|
| **Distancia al vecino más cercano** (*distance to nearest neighbour*) | *«Distancia de borde al parche vecino más cercano»* | Prugh, 2009 | **[0, +∞)** | `[SIN FUENTE VERIFICADA]` |
| **Tamaño efectivo de malla** (*effective mesh size*) | *«La probabilidad de que dos puntos colocados al azar en el paisaje estén conectados, convertida a área»* | Jaeger, 2000 | **[0, +∞)** | `[SIN FUENTE VERIFICADA]` |
| **Hábitat dentro de un búfer** | *«Medida de cuán aislados o agregados están los parches focales en el paisaje»* | Prugh, 2009 | **[0, +∞)** | `[SIN FUENTE VERIFICADA]` |
| **Índice de cohesión de parches** | *«Media estandarizada, ponderada por área, de la razón perímetro/área»* | Schumaker, 1996 | — | `[SIN FUENTE VERIFICADA]` |
| **Radio de giro medio** / **ponderado por área** | *«Medida de cuán lejos llega un parche a través del paisaje»* | McGarigal, 1995 | **[0, +∞)** | `[SIN FUENTE VERIFICADA]` |
| **Índice de proximidad** | — | — | **[0, +∞)** | `[SIN FUENTE VERIFICADA]` |

**Y las tres métricas de grafo que la fuente nombra como las más usadas** —textual: *«algunas de las
métricas más comunes usadas en modelación de conectividad son el **Índice Integral de Conectividad
[IIC]**, la **Probabilidad de Conectividad [PC]** y el **Área Conectada Equivalente [ECA]** (Pascual-Hortal
y Saura, 2006; Saura *et al.*, 2011; Saura y Pascual-Hortal, 2007)»* `[VERIFICADO en esta sesión: texto
extraído, p. 70]`— **tampoco tienen umbral en la fuente**, y sus artículos primarios están detrás de
muros que rechazan a los agentes automáticos (§14.6). El rango `[0, +∞)` de seis de las métricas no es un
detalle: **una métrica sin techo y sin piso no puede declarar violación por sí sola**, porque no hay
valor de referencia contra el cual estar por debajo.

**La pieza que sí sirve de la fuente, y hay que decirlo porque es útil:** la descomposición
`dPC = dPCintra + dPCflux + dPCconnector` (y su gemela `dIIC`) permite saber **por qué** una unidad
aporta o no aporta conectividad —área propia, conexión con vecinos, papel de trampolín—, y es la
herramienta con la que §7.4 construye el test de auditoría de esta dimensión. **Saber por qué no es
saber cuánto**: la fuente da la anatomía y no da la norma.

### 3.4 El único umbral de conectividad con fuente institucional fuerte: CSI ≥ 95 %

Es el hallazgo central de este documento, y se cita con la precisión que merece.

**Qué es el CSI.** El **Índice de Conectividad de Estado** (*Connectivity Status Index*) es la medida con
la que Grill, Lehner, Thieme, Geenen, Tickner, Antonelli *et al.* evaluaron la conectividad de **12
millones de kilómetros de ríos** en *«Mapping the world's free-flowing rivers»*, **Nature 569:215-221
(2019)**. El resumen del artículo —leído en esta sesión— declara el método y el mecanismo: *«Here we
assess the connectivity status of 12 million kilometres of rivers globally and identify those that remain
free-flowing in their entire length»*, y *«Dams and reservoirs and their up- and downstream propagation
of fragmentation and flow regulation are t[he main cause]»* `[VERIFICADO en esta sesión]`.

**El umbral, con su letra exacta.** El artículo completo es de pago, pero **las leyendas de sus figuras
son públicas** y en ellas el umbral está escrito dos veces, sin ambigüedad `[VERIFICADO en esta sesión,
leyendas de la Fig. 2 del artículo, leídas en la página del editor]`:

> *«Fig. 2: Dominant pressure indicator for global river reaches below the **CSI threshold of 95%**.»*

> *«CSI values for individual river reaches, as calculated with our model. If a value is **at or above the
> CSI threshold (95%)**, the river reach is declared to have **good connectivity status**; if it is below
> the threshold, it is declared to be **impacted**.»*

**Las tres cosas que hay que decir a la vez, porque decir solo una sería deshonesto.**

1. **El umbral existe, es explícito, es numérico y está publicado** por una fuente institucional fuerte
   (*Nature*, con datos y código abiertos según la propia fuente). **No es una invención de este
   proyecto.**
2. **La fuente mide estado; no fija un piso normativo.** El artículo **clasifica** tramos (de flujo libre
   / impactado); **no legisla** cuánta conectividad debe tener un río. **Adoptar 95 % como piso del SDV-E
   es una decisión de política del proyecto sobre un umbral publicado, y así se declara aquí:**
   `PROPUESTA NO RATIFICADA`.
3. **La fuente no da un umbral de red ni de paisaje.** Da un umbral de **tramo** (*river reach*), y el
   estado *free-flowing* de un río completo se decide con un árbol de decisión sobre los tramos. **No
   existe aquí ningún «X % de la red fluvial de la cuenca debe permanecer libre»**, y este documento **no
   lo inventa** (§13, pregunta 3).

**Y una precisión que corrige a la biblioteca sin contradecirla en el fondo.** El
[documento 12](12_Ecosistemas_Rios_y_cuencas.md) §Dimensión V escribió: *«Umbral numérico de conectividad
… `[SIN FUENTE VERIFICADA]` — **el estudio mide; no fija umbral**»*. Las dos mitades de esa frase no son
igual de exactas: **el estudio sí fija un umbral** (95 % de CSI, como línea de corte de su propia
clasificación, publicado en su Fig. 2) **y no fija un piso normativo**. La conclusión del documento 12
—que su piso debía ser estructural y no numérico— **sigue siendo defendible y este documento no la
revierte**; lo que este documento corrige es **la razón registrada**, porque de esa razón depende que el
95 % pueda o no adoptarse para unidades fluviales. Se registra como discrepancia localizada en §13,
pregunta 3, **sin editar el documento 12**.

### 3.5 La ley europea: la única norma que fija **dirección** (y una meta agregada, no un piso de unidad)

El **Reglamento (UE) 2024/1991** sobre restauración de la naturaleza, en vigor desde el 18 de agosto de
2024, es el instrumento verificado en esta rama que contiene obligaciones de conectividad **jurídicamente
exigibles** `[VERIFICADO]`. Trae dos cosas de naturaleza distinta y confundirlas sería el error clásico:

| Contenido | Naturaleza jurídica | ¿Puede ser piso del SDV-E? |
|---|---|---|
| **25 000 km** de ríos de la UE restaurados a flujo libre **antes de 2030**, mediante identificación y eliminación de barreras | **META AGREGADA** de un territorio político (la Unión), repartida entre Estados | **No como piso de unidad.** Es un compromiso de restauración; un tramo concreto no lo incumple |
| **Tendencia creciente** de la conectividad de los ecosistemas forestales, sin admitir tendencia decreciente | **NORMA DE DIRECCIÓN**: no fija un valor, prohíbe una evolución | **Sí, como piso de dirección** —binario y auditable: la tendencia no decrece— y **solo para unidades dentro del ámbito del Reglamento** |

**Lo que este documento propone, marcado como lo que es.** Adoptar la **norma de dirección** como piso
**binario** de la dimensión para unidades forestales europeas, y su **traslado por analogía** al resto de
unidades y regiones como `[HIPÓTESIS]` **no ratificada**: *«la tendencia de conectividad de la unidad no
puede ser decreciente»*. Es un piso débil —no dice cuánta conectividad hace falta, solo que no se puede
perder— y precisamente por eso es **honesto**: es lo único que la fuente permite afirmar. Y hay que
declarar su límite, que el [documento 12](12_Ecosistemas_Rios_y_cuencas.md) ya había descubierto en su
propio piso estructural: **un piso de no-regresión tolera un estado inicial malo**. Un bosque ya
fragmentado cumple «tendencia no decreciente» para siempre sin ganar un solo metro de corredor.

### 3.6 Lo que la UICN (2020) **sí** ofrece y lo que **no** (verificado por lectura, no por fallo)

La Serie de Directrices para Buenas Prácticas n.º 30 de la UICN es **el instrumento de referencia mundial
sobre conectividad** —grupo especialista de conservación de la conectividad (CCSG), establecido en 2016
dentro de la CMAP—, y es la fuente de la definición que §3.1 adopta. Ofrece, y es utilizable:

- el **marco de redes ecológicas**: *core areas*, **corredores**, *restoration areas* y *buffer zones*
  (la misma arquitectura que la Resolución CMS 14.16);
- **criterios de diseño y gobernanza**, y la taxonomía de la conectividad (terrestre, de agua dulce,
  marina, aérea).

Y **no ofrece**, según la extracción íntegra del texto realizada en la sesión de fuentes de esta rama
(146 páginas): **ninguna anchura mínima de corredor** —las únicas cifras de anchura del documento son
**descripciones de casos**, no recomendaciones normativas—, ningún valor de PC, IIC ni malla efectiva, y
**ningún umbral numérico de conectividad de ningún tipo**. Esta sesión **verifica la URL y el tamaño del
archivo** (200, 7 060 322 bytes descargados) y **no re-extrae el texto**: la conclusión es de la lectura
de la rama, y se cita como tal. **Corrección de trazabilidad:** el motivo por el que los documentos 02 y
09 registraron esta fuente como «no leída» fue **un archivo mal nombrado en el repositorio**, no un fallo
del extractor (§1 y §13, pregunta 6).

### 3.7 El hueco institucional, contado con la boca de las instituciones

Este es el pilar que cierra la sección y el que hace que el 0,000 del catálogo sea **un resultado y no
una vergüenza**:

| Organismo | Qué publica sobre conectividad | ¿Umbral numérico? |
|---|---|---|
| **CBD** (Marco Kunming-Montreal, Metas 2, 3, 12 y Meta A) | *«bien conectados»*, *«integridad, conectividad y resiliencia»*; y el **41 %** de Partes que declaran abordarla | **No.** Lo único numérico es el porcentaje de Partes que dicen abordarla: **mide la ambición declarada de los Estados, no el estado del ecosistema** |
| **UICN** (2020, directrices n.º 30) | definición, marco de red, criterios de diseño y gobernanza | **No** (verificado por lectura completa) |
| **CMS** (Resolución 14.16) | definición vinculante y mandato de conservar conectividad | **No** |
| **UNEP-WCMC** (WDEC, Protected Planet) | **inventario** de corredores y áreas protegidas en construcción | **No**: el WDEC registra *ubicación y características*, no un mínimo |
| **Comisión Europea** (Reglamento 2024/1991) | una meta agregada y una norma de dirección | **Meta sí, piso de unidad no** (25 000 km es de la Unión) |
| **AEMA** (Agencia Europea de Medio Ambiente) | — | **Rutas muertas**: cuatro rutas probadas del indicador de fragmentación del paisaje devuelven **404**. **Hoy la AEMA no publica un indicador accesible de fragmentación del paisaje en las rutas probadas** y este documento **no cita ninguna cifra suya** |
| **NatureConnect / Horizonte Europa** (2024) | revisión metodológica completa de métricas, anchuras y herramientas | **Umbrales solo de anchura de corredor** (§4.3); **ninguno** para las métricas de paisaje |

**Conclusión del pilar, en la forma más dura posible:** ningún organismo publica un valor mínimo
universal de conectividad de paisaje; **la ausencia está admitida por las instituciones** (que crearon
una base de datos global precisamente porque *«la falta de información a nivel global sobre la extensión
y la efectividad de los corredores ecológicos limita nuestra comprensión del estado actual de la
biodiversidad»*); y el único umbral publicado que existe es **fluvial** y **de clasificación**. Ese es el
suelo epistemológico sobre el que se apoya todo lo que sigue.

---

## 4. Dimensiones del SDV-E

### 4.0 El mapa: qué cubre esta dimensión, qué delega y qué no puede cubrir

La dimensión tiene **siete sub-parámetros** y **no todos son de la misma clase de objeto**. Esta tabla
es la que el [documento 08](08_INV2-E_invariante.md) §4.1 no podía escribir con una sola fila, y la que
sustituye a `conectividad_indice` (`— | —`):

| # | Sub-parámetro | Clase | Operador | Mínimo Absoluto (LEY, no votable) | Óptimo (POLÍTICA, votable) | Estado |
|---|---|---|---|---|---|---|
| **C1** | **Conectividad longitudinal fluvial (CSI)** | escalar 0-100 | `min` | **≥ 95 % de CSI** para declarar un tramo *de flujo libre* `PROPUESTA NO RATIFICADA` (Grill *et al.*, 2019) | **100 %** (río sin alteración de su conectividad longitudinal) | 🟡 umbral con fuente, adopción pendiente de ratificación |
| **C2** | **Barreras longitudinales nuevas** | binaria | `binary` | **0 barreras nuevas sin expediente de carga de la prueba (T14)**, en la unidad y aguas arriba/abajo | 0 barreras en toda la cuenca | 🟢 piso doctrinal (T14) + precedente del [documento 12](12_Ecosistemas_Rios_y_cuencas.md) |
| **C3** | **Anchura de corredor del grupo taxonómico declarado** | escalar (m) | `min` | **30 / 61 / 101 m** según grupo (Bentrup, 2008, vía NatureConnect, 2024) `[REPORTADO por vía secundaria verificada]` | extremo superior recomendado por grupo: **61 / 101 / 183 / 1 609 / 2 414 / > 4 828 m** | 🟡 umbral por grupo, fuente primaria 403 |
| **C3b** | **Anchura de corredor en contexto humano** | escalar (m) | `min` | **2 000 m** si conecta parches a 8-80 km (Beier, 2019) · **3 000 m** junto a zonas residenciales y **400 m** con senderos recreativos (Ford *et al.*, 2020) | **6 000 m** junto a residencial · **1 000 m** con senderos | 🟡 regla de dedo, no norma universal |
| **C4** | **Conectividad de paisaje**: PC, IIC, ECA, dPC/dIIC, tamaño efectivo de malla, fragmentación, distancia al vecino más cercano | índice / área | — | **`[SIN FUENTE VERIFICADA — pendiente de consenso científico]`** | *«red bien conectada»* — condición sin cifra (GBF, Meta 3) | 🔴 **sin piso**: instrumento sí, norma no |
| **C5** | **Tendencia de la conectividad** | binaria de dirección | `binary` | **La tendencia no puede ser decreciente** (Reglamento UE 2024/1991, para unidades forestales de su ámbito) `[VERIFICADO]`; por analogía, para toda unidad: `[HIPÓTESIS]` | Incremento sostenido, **sin cifra publicada** | 🟡 norma de dirección real, traslado no ratificado |
| **C6** | **Red ecológica declarada** (áreas núcleo, corredores, áreas de restauración, zonas de amortiguamiento) | binaria auditable **sin peso** | `binary` | **Presencia** de la red declarada y **declaración del área de referencia** | Amplitud y redundancia de la red | 🟡 marco con fuente (UICN, 2020), umbral no |
| **C7** | **Conectividad marina** · **conectividad hidrológica de humedales** | — | — | **`[SIN FUENTE VERIFICADA]`** | — | 🔴 **vacío declarado**: confirma los documentos 11 y 13 |

**Delegaciones explícitas, para que nadie lea este documento como si cubriera todo.** Los parámetros
**estructurales de cada tipo de ecosistema** —cobertura, borde, hidroperiodo, riberas, matriz cultivada—
pertenecen a los documentos 10 a 18 y **no se repiten aquí**. La **unidad de aplicación** —tipo,
bioma, cuenca, lugar o parte `eco-` instanciada— pertenece al [documento 02](02_Unidad_y_sujeto_del_SDV-E.md).
El **elenco de sensores** pertenece al [documento 06](06_Medicion_y_verificacion_T13.md). Lo que aquí se
fija es **el instrumento común, su régimen jurídico y su definición operativa de violación**.

---

### Dimensión C1: Conectividad longitudinal fluvial (*el único umbral que existe*)

**Qué protege.** Que el río sea un continuo y no una sucesión de embalses: que el sedimento, los
nutrientes, los peces migratorios y el agua lleguen abajo, y que el río complete su recorrido hasta su
punto terminal.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **Índice de Conectividad de Estado (CSI) del tramo** | **≥ 95 %** para que el tramo se declare *de flujo libre / buena conectividad*; por debajo, la fuente lo declara **impactado** `PROPUESTA NO RATIFICADA` (decisión de política del proyecto sobre un umbral publicado) | **100 %** — río sin ninguna alteración de su conectividad longitudinal | Grill, Lehner, Thieme, Geenen, Tickner, Antonelli *et al.*, **Nature 569:215-221 (2019)** `[VERIFICADO en esta sesión: leyenda de la Fig. 2]` |
| **Estado medido, no umbral — ríos > 1 000 km de flujo libre en toda su longitud** | **37 %** — **`[ESTADO MEDIDO]`**, no piso | — | Grill *et al.*, 2019 `[VERIFICADO: resumen del artículo]` |
| **Estado medido, no umbral — ríos que fluyen sin interrupción hasta el océano** | **23 %** — **`[ESTADO MEDIDO]`**, no piso | — | Grill *et al.*, 2019 `[VERIFICADO: resumen del artículo]` |
| **Mecanismo documentado de la pérdida** | *«Dams and reservoirs and their up- and downstream propagation of fragmentation and flow regulation»* | — | Grill *et al.*, 2019 `[VERIFICADO: resumen]` |
| **Umbral de red** («X % de la red fluvial de la cuenca debe permanecer libre») | **`[SIN FUENTE VERIFICADA — pendiente de consenso científico]`** | — | **No existe.** Este documento **no lo inventa** |

**Justificación.** El 95 % no es un número elegido por el proyecto: es **la línea de corte que la propia
fuente usa para clasificar** y está publicada con esta letra: *«If a value is at or above the CSI threshold
(95%), the river reach is declared to have good connectivity status; if it is below the threshold, it is
declared to be impacted»* `[VERIFICADO]`. La justificación de **adoptarlo como piso** es más modesta y hay
que decirla entera: **la fuente clasifica; el canon manda proteger** (Cap. 10 §10.4 nombra la conectividad
como parte del SDV de un ecosistema), y **entre clasificar y legislar hay un acto de política** que este
documento propone y **no puede ratificar por sí solo**. Tres razones sostienen la propuesta: (a) es el
**único** umbral de conectividad con fuente institucional fuerte que se pudo verificar en toda la rama;
(b) el dato que lo alimenta es **global y reproducible**, y **la fuente lo declara abierto**: sus valores
de CSI, factor de presión dominante y estado de flujo libre están publicados **bajo licencia CC-BY-4.0**
y *«el conjunto de datos puede usarse junto con el código fuente publicado (véase "Code availability")
para recalcular los resultados principales del estudio y ejecutar escenarios existentes y nuevos»*
`[VERIFICADO en esta sesión: declaración de disponibilidad de la fuente]` — **con una salvedad que la
propia fuente declara y que importa para la implementación: las bases de datos de represas necesarias
para calcular los indicadores de fragmentación y regulación no están en el repositorio de datos por
razones de licencia**, y se remiten a un portal externo que responde 200 (§14.1)—; y (c) su **área de
aplicación es el tramo**, que es una unidad física y no una ventana elegida por el analista —el defecto
que invalida los índices de paisaje como piso (Regla 3 y Regla 4)—.

**Protocolo.** **Inventario de barreras de la cuenca** —número, posición, tipo (presa, azud, derivación,
vertedero) y **año de construcción**— y cálculo del CSI por tramo, con la declaración obligatoria de la
**propagación aguas arriba y aguas abajo** de cada barrera, que es el mecanismo que la fuente documenta.
Frecuencia: **anual** para las barreras (es un hecho administrativo, no una medición de campo) y **cada
cinco años** para el estado del continuo, heredando la periodicidad que el
[documento 12](12_Ecosistemas_Rios_y_cuencas.md) §Dimensión V ya fijó. Quién reporta: **organismo de
cuenca + parte `eco-` + comunidad testigo**; el **guardián consiente y no mide** (Cap. 16.5 §16.5.14).

**Violación (hechos, no opiniones).** Constituye violación de esta dimensión:
(a) **el CSI del tramo es inferior a 95 %** por causa antrópica y la unidad **declara cumplimiento de
conectividad** —el hecho es el valor medido, no la intención—;
(b) se declara la conectividad **por tramo sin evaluar la propagación** aguas arriba y aguas abajo;
(c) el **inventario de barreras está incompleto** o una barrera **carece de año de construcción**, de modo
que su expediente no es auditable;
(d) se **renueva la concesión** de una barrera existente **sin expediente de carga de la prueba** —renovar
es proponer, y T14 carga la prueba sobre quien propone—;
(e) la unidad **cita el «bien conectados» del GBF como si fuera medición** sin haber medido nada.

---

### Dimensión C2: Barreras nuevas (*el piso estructural, ahora transversal*)

**Qué protege.** Que la conectividad **no se siga perdiendo mientras se discute cómo medirla**. Es el
único piso de esta dimensión que **no necesita ningún consenso científico pendiente**.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **Barreras nuevas** (presas, azudes, derivaciones, vertederos, infraestructura lineal que interrumpe el flujo) | **0 en la unidad y en cualquier punto que afecte su régimen, sin expediente de carga de la prueba** | 0 en toda la cuenca | **Piso doctrinal**: T14 (Cap. 5) — *«la carga de la prueba recae sobre quien propone acciones que afectan la temporalidad de no-participantes»*; **precedente de forma**: [documento 12](12_Ecosistemas_Rios_y_cuencas.md) §Dimensión V |
| **Barreras existentes cuya concesión se renueva** | **Expediente obligatorio** — la renovación es una propuesta nueva | Retirada y restauración del continuo | Ídem |
| **Superficie de corredor declarada** | **No reducción** de la superficie declarada | Ampliación y conexión con unidades vecinas | Construcción de este documento `[HIPÓTESIS]`, sobre el precedente del [documento 15](15_Ecosistemas_Praderas_y_sabanas.md) §Dimensión VIII |

**Justificación.** Este piso **ya existe en la biblioteca**, pero hasta ahora existía **solo para ríos**:
el [documento 12](12_Ecosistemas_Rios_y_cuencas.md) §Dimensión V lo dedujo de T14 y de la imposibilidad
de inventar un porcentaje. **El aporte de este documento es hacerlo transversal**: una carretera que
fragmenta una pradera, un parque eólico que rompe un corredor de aves de interior, un desarrollo
residencial en un cuello de botella o un canal que corta un humedal **son el mismo hecho ecológico** —una
barrera nueva sin expediente— y **no había ninguna dimensión transversal que los atrapara**. Su
legitimidad no es científica, es **doctrinal**, y por eso es **LEY y no se vota** mientras que su alcance
concreto por unidad es POLÍTICA.

**Protocolo.** Expediente de carga de la prueba **por barrera**, con: identificación, fecha, promotor,
costo de oportunidad asumido (T14 exige *documentar* el costo, no solo declararlo), medidas de
permeabilidad y **evidencia de que la conectividad no se redujo**. Registro público con T13. Frecuencia:
en el acto administrativo de autorización y **en cada renovación**.

**Violación.** (a) Existe una barrera nueva sin expediente; (b) se renovó una concesión sin expediente;
(c) el expediente no documenta el costo de oportunidad asumido; (d) se redujo la superficie de corredor
declarada sin expediente; (e) se declaró una barrera como «permeable» sin medición de permeabilidad.

---

### Dimensión C3: Anchura de corredor (*el piso que depende de un grupo que hay que declarar*)

**Qué protege.** Que un corredor sea **funcional para la fauna que efectivamente lo usa** y no una franja
simbólica. Un corredor de 30 m y uno de 101 m no son el mismo objeto ecológico, y la diferencia no es de
grado: es de **qué especies pueden atravesarlo**.

**La tabla completa, leída directamente del PDF en esta sesión** (Tabla 6.2 de NatureConnect, 2024,
atribuida a la revisión de **66 estudios** de **Bentrup, USDA Forest Service, 2008**):

| Grupo taxonómico | **Mínimo Absoluto (m)** | **Óptimo — extremo superior recomendado (m)** |
|---|---|---|
| **Plantas** | **30** | 101 |
| **Invertebrados** | **30** | 61 |
| **Especies acuáticas** | **30** | 61 |
| **Reptiles y anfibios** | **30** | 183 |
| **Aves de interior** | **61** | 1 609 |
| **Aves de borde** | **30** | 101 |
| **Mamíferos pequeños** | **101** | 101 |
| **Mamíferos grandes** | **101** | 2 414 |
| **Mamíferos predadores grandes** | **101** | **> 4 828** |

**Y las reglas de anchura para contextos concretos**, leídas en la Caja 6.2 del mismo documento:

| Regla | **Mínimo Absoluto** | **Óptimo** | Fuente |
|---|---|---|---|
| Corredores que conectan parches separados por **8-80 km** | **2 000 m** de ancho, salvo cuellos de botella inevitables (p. ej. cruces de autopista) | — | **Beier (2019)**, *A rule of thumb for widths of conservation corridors*, vía NatureConnect (2024) `[VERIFICADO en esta sesión]` |
| Justificación de esos 2 000 m | cubriría ámbitos de campeo de hasta **~8 km²**, suficiente para **345 especies** de mamíferos probables habitantes de corredor, seleccionadas de una lista de **429** mamíferos terrestres (Tucker *et al.*, 2014); con efectos de borde significativos hasta **300 m**, un corredor de 2 km deja **≥ 1 700 m** libres de borde | — | Beier (2019) vía NatureConnect (2024) `[VERIFICADO]` |
| Corredor junto a **zonas residenciales** | **3 000 m** | **6 000 m** | **Ford *et al.* (2020)**, vía NatureConnect (2024) `[VERIFICADO en esta sesión: «the effective corridor width should vary from 3000 to 6000 m close to residential areas»]` |
| Corredor en zonas con **senderos recreativos** | **400 m** | **1 000 m** | Ford *et al.* (2020), ídem `[VERIFICADO: «and 400 to 1000 m in areas containing recreational trails, depending on the species»]` |
| Principios generales de la fuente | los corredores **más largos deben ser más anchos** que los cortos, y los corredores **cortos conectan con más probabilidad** que los largos | — | NatureConnect (2024) `[VERIFICADO]` |

**Justificación, y sus tres límites declarados.**
1. **La fuente primaria no se pudo abrir.** Los valores están transcritos con atribución explícita en un
   documento de directrices verificado (HTTP 200, texto extraído), pero **el original de Bentrup (2008) en
   el USDA devuelve 403 a los agentes automáticos** y **este documento no lo ha leído**. Se marcan
   `[REPORTADO por vía secundaria verificada]`, y **leer el original es una tarea humana de una hora**
   (§13, pregunta 7).
2. **La propia fuente advierte que las cifras no son definitivas.** Textual de NatureConnect (2024):
   *«While the USDA acknowledged that many of the studies did not encompass a wide enough range of
   corridor widths to definitively determine optimal sizes, they did provide general recommendations»*
   `[VERIFICADO]`. Es decir: **ni la fuente secundaria presenta estas anchuras como normas cerradas**. Por
   eso el mínimo por grupo es un **piso candidato**, no un piso ratificado, y el Óptimo es todavía más
   frágil que el piso.
3. **El piso depende de un grupo que hay que declarar, y eso es un riesgo de fraude propio de esta
   dimensión.** Entre el piso de «plantas» (30 m) y el de «mamíferos predadores grandes» (101 m) hay un
   factor **3,4**. Un mismo corredor de 41 m es **cumplimiento** si la unidad declara «plantas» e
   **incumplimiento** si declara «mamíferos grandes». Ninguna otra dimensión del catálogo tiene un piso
   **elegible por el interesado**, y por eso §7.3 propone la regla anti-fraude correspondiente: **el grupo
   se fija por la composición faunística efectivamente presente y acreditada, no por conveniencia**, y la
   declaración es auditable.

**Protocolo.** Cartografía del corredor con **ancho medido en su punto más estrecho** (el cuello de
botella es el que decide si el corredor funciona); declaración del **grupo taxonómico objetivo** con su
evidencia (especies clave de la unidad, [documento 20](20_Transversal_Biodiversidad.md) §4.3); medición
del contexto (¿hay vivienda? ¿hay senderos recreativos?) porque **el contexto cambia el piso** de 400 m a
3 000 m según la fuente. Frecuencia: **anual** con la capa de cobertura; **en el acto de autorización**
cuando el corredor esté afectado por una obra.

**Violación.** (a) El ancho mínimo medido del corredor es **inferior al mínimo del grupo declarado**;
(b) el **grupo declarado no corresponde a la fauna acreditada** de la unidad —es fraude de declaración, no
error de medición—; (c) se mide el ancho en el punto más favorable (promedio o punto medio) en lugar del
**cuello de botella**; (d) se declara cumplimiento de anchura **sin declarar el grupo**, que es declarar
un número sin su unidad de sentido.

---

### Dimensión C4: Conectividad de paisaje (*el instrumento sin norma, y por qué el 0,000 es correcto*)

**Qué protege.** Nada, hoy, en el sentido jurídico del estándar: **se mide y no se juzga**. Esta
dimensión existe en el catálogo porque **el canon nombra la conectividad como parte del SDV de un
ecosistema** (Cap. 10 §10.4) y porque el proyecto debe poder **reportar** su estado en el tablero. **No
produce violación, y eso es una decisión, no un olvido.**

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **Probabilidad de conectividad (PC)**, **Índice Integral de Conectividad (IIC)**, **Área Conectada Equivalente (ECA)** | **`[SIN FUENTE VERIFICADA — pendiente de consenso científico]`** | *«red bien conectada»* (condición, sin cifra) | NatureConnect (2024), Tabla y texto: las tres métricas más usadas en modelación `[VERIFICADO]`; CBD, Meta 3 (2022) |
| **Contribución de un parche** `dPC = dPCintra + dPCflux + dPCconnector` (y `dIIC`) | **`[SIN FUENTE VERIFICADA]`** | — | NatureConnect (2024), atribuido a Saura y Rubio (2010) `[VERIFICADO]` |
| **Tamaño efectivo de malla** (*effective mesh size*) | **`[SIN FUENTE VERIFICADA]`** | — | Definición: Jaeger (2000), vía NatureConnect (2024) `[VERIFICADO]` |
| **Índice de fragmentación** / cohesión de parches | **`[SIN FUENTE VERIFICADA]`** — y **ninguna ruta accesible de la AEMA lo publica hoy** | — | Schumaker (1996), vía NatureConnect (2024) `[VERIFICADO]`; AEMA: **cuatro rutas probadas, 404** |
| **Distancia al vecino más cercano** | **`[SIN FUENTE VERIFICADA]`** — rango declarado **[0, +∞)** | — | Prugh (2009), vía NatureConnect (2024) `[VERIFICADO]` |
| **Distancia de dispersión máxima** del grafo | **NO ES UN UMBRAL**: es un **parámetro de entrada del modelo** | — | NatureConnect (2024): *«definir una distancia de dispersión máxima para limitar las conexiones entre nodos más allá de cierto umbral biológico»* `[VERIFICADO]` |

**Justificación de la ausencia de piso, en tres razones que no son la misma.** (a) **Ninguna institución
publica un valor**: se buscó en la CBD (Metas 2, 3, 12 y Meta A), en la UICN (146 páginas extraídas), en
la CMS (Resolución 14.16), en UNEP-WCMC/Protected Planet, en la AEMA (rutas muertas), en el ETC-DI (PDF
ilegible) y en la UNCCD (rutas 404): **ni un solo organismo publica un mínimo universal**. (b) **El
índice no es una propiedad de la unidad** (Regla 3 y Regla 4): depende de la ventana declarada y de los
vecinos, de modo que un piso sobre él sería un piso sobre el promedio del paisaje, no sobre la unidad
protegida. (c) **La distancia de dispersión, que sería el parámetro que convierte el grafo en algo
biológico, es una entrada del modelo**, y la fuente lo dice: no es una norma. **Asignarle un peso en el
piso sería el error que el [documento 07](07_Formula_de_violacion_y_pesos.md) §5.3 ya nombra: un peso sin
piso no mide, diluye.**

**Protocolo.** Cálculo de PC (o del índice declarado) sobre la capa de cobertura, con **declaración
obligatoria** de: (1) el **área de referencia** y su justificación; (2) la **distancia de dispersión**
usada y su fuente; (3) el **clasificador de cobertura** y su versión; (4) la **fecha en TA** de la capa.
Frecuencia: **anual** con la capa, y siempre en la misma ventana, porque **cambiar la ventana entre dos
mediciones invalida la serie** (T13: la contabilidad no se borra, y una serie con ventanas distintas está
borrada de hecho). Estos cuatro campos entran como `metodo_version` auditable.

**Violación.** **Ninguna por valor.** Esta dimensión **no produce violación numérica mientras no exista
umbral con fuente.** Sí produce, en cambio, dos hechos auditables: (a) **falta de declaración** del área
de referencia o de la distancia de dispersión → el parámetro se trata como **no medido** (`None`), con
bandera de opacidad y sin habilitar crédito; y (b) **incoherencia de serie** —dos mediciones con ventanas
distintas presentadas como comparables— que es una violación **de T13**, no de un umbral ecológico.

---

### Dimensión C5: Tendencia (*la única norma de dirección con fuente*)

**Qué protege.** Que la conectividad **no siga cayendo**, incluso cuando no se sabe cuánta hace falta. Es
el piso más débil de la dimensión y el único **jurídicamente exigible** en un territorio real.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **Tendencia de la conectividad de ecosistemas forestales** | **Tendencia creciente**: *no se admite tendencia decreciente* `[VERIFICADO]` | Incremento sostenido, **sin cifra publicada** | **Reglamento (UE) 2024/1991** (en vigor desde el 18-08-2024) |
| **Trend aplicado a cualquier unidad del SDV-E, dentro o fuera de la UE** | **Tendencia no decreciente** — `[HIPÓTESIS]` **no ratificada**: es un traslado por analogía de una norma territorial a una unidad ecológica | — | Traslado de este documento |
| **Meta agregada de la UE** | **25 000 km** de ríos restaurados a flujo libre antes de 2030 | Regeneración más allá de la meta | Reglamento (UE) 2024/1991 `[VERIFICADO]` — **meta de la Unión, no piso de unidad** |

**Justificación.** Es una norma **de dirección y no de nivel**, y esa es exactamente su fuerza: no exige un
consenso científico que no existe sobre *cuánta* conectividad hace falta, y sin embargo **prohíbe la
única cosa que no admite discusión: seguir perdiendo**. Su debilidad es simétrica y hay que escribirla:
**un piso de no-regresión tolera un estado inicial malo**, y el [documento 12](12_Ecosistemas_Rios_y_cuencas.md)
§Dimensión V ya lo había declarado para su propio piso estructural. Las mitigaciones son las mismas tres
que allí: el Óptimo votable, el expediente obligatorio **también en renovaciones**, y la declaración del
déficit acumulado como pasivo de la unidad con T13.

**Protocolo.** Comparación de la métrica declarada (C1 o C4) entre **dos ciclos TA consecutivos como
mínimo**, con la misma ventana y el mismo clasificador, y **declaración del signo**. Frecuencia: la del
ciclo TA, **cuya unidad sigue sin estar decidida** ([documento 07](07_Formula_de_violacion_y_pesos.md)
§5.4b). Quién reporta: parte `eco-` con comunidad testigo.

**Violación.** **La tendencia decreciente medida en dos ciclos TA comparables** constituye violación
**binaria y auditable** de esta dimensión, con independencia de que exista o no un umbral numérico —**salvo
que la caída sea atribuible a la fase documentada de un ciclo natural** (fuego, inundación, sequía) del
[documento 22](22_Transversal_Ciclos_naturales.md), en cuyo caso se registra como ciclo y no como
violación, con la carga de la atribución sobre quien la invoca (§5.5)—.

---

### Dimensión C6: Red ecológica declarada (*la dimensión binaria sin peso*)

**Qué protege.** Que exista **una red pensada** —no solo parches sueltos— y que la unidad **declare en qué
red está y contra qué ventana se mide**. Es la dimensión que hace posible que las demás sean auditables.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **Presencia de una red declarada** con sus elementos: áreas núcleo, **corredores**, áreas de restauración y zonas de amortiguamiento | **Presencia de la declaración** (binario auditable) | Red amplia, redundante y conectada con unidades vecinas | Marco de redes ecológicas de la **UICN (2020)**; misma arquitectura que la Resolución CMS 14.16 `[VERIFICADO vía informe de fuentes de la rama]` |
| **Declaración del área de referencia** de toda métrica de paisaje | **Presente y motivada** | — | Aporte de este documento `[HIPÓTESIS]`, exigido por NatureConnect (2024) p. 80 `[VERIFICADO]` |
| **Zona Libre del Reino Natural de esta dimensión** | **Presencia del registro de lo no medido** | — | Cap. 7 §7.9 · Cap. 16.5 §16.5.14 |

**Justificación.** Precedente canónico: las dimensiones VIII (Rehabilitación) y IX (Opacidad Vital) del
SDV-H *«se registran cualitativamente y mediante umbrales binarios (presencia/ausencia del derecho), no
mediante pesos en la fórmula»* (Cap. 8 §8.11). Aquí se usa el mismo instrumento para lo que en
conectividad **es procedural y no cuantificable**: la existencia de la red y de la declaración de
ventana. **Peso en la fórmula: 0**, y no por humildad, sino porque cuantificarlo permitiría que una red
excelente **compensara** una barrera nueva —exactamente lo que *«el suelo antes que el saldo»* prohíbe—.

**Protocolo.** Registro público (T13) de la red y de la ventana; verificación de que **los corredores
declarados existen en el terreno** y de que la ventana declarada **no es la que conviene al resultado**.
Frecuencia: cada 5 años, con la renovación del estándar de la unidad.

**Violación.** (a) **No existe declaración de red** para una unidad sujeta al SDV-E; (b) se declara una
métrica de paisaje **sin declarar su área de referencia**; (c) **los corredores declarados no existen** en
el terreno (el fraude más barato de esta dimensión, y el más fácil de detectar); (d) la ventana declarada
**cambia entre mediciones** sin registro del cambio.

---

### Dimensión C7: Lo que esta dimensión NO puede cubrir hoy (vacío declarado, no escondido)

**Qué protege.** Nada todavía. Se publica para que nadie lea el resto del documento como si la dimensión
estuviera cerrada.

| Vacío | Estado | Origen de la búsqueda fallida |
|---|---|---|
| **Conectividad marina** (larvaria, de arrecifes, de rutas oceánicas) | **`[SIN FUENTE VERIFICADA — pendiente de consenso científico]`** | Búsqueda confirmada y **no cerrada**; coincide con el [documento 13](13_Ecosistemas_Oceanos_y_costas.md) §13 |
| **Conectividad hidrológica de humedales** (el parámetro que el [documento 11](11_Ecosistemas_Humedales.md) §Dimensión VIII dejó abierto) | **`[SIN FUENTE VERIFICADA]`** | **No se encontró.** La Convención de Humedales devuelve **403 en todas las rutas probadas**: siendo una fuente real, **no se cita ninguna cifra suya** |
| **Umbral de fragmentación del paisaje de ámbito europeo** | **`[SIN FUENTE VERIFICADA]`** | Cuatro rutas de la **AEMA** devuelven **404**; el informe del ETC-DI (2024) se descargó **pero el PDF está truncado en 8 388 608 bytes exactos y es ilegible** para dos extractores distintos |
| **Ratio mínimo de conectividad de un río** («X % de la red libre») | **`[SIN FUENTE VERIFICADA]`** | **No existe en la fuente ni en ninguna otra verificada.** Las cifras de 37 % y 23 % son **`[ESTADO MEDIDO]`** del mundo, no normas |

---

### 4.8 Tabla de conjunto: qué es piso, qué es tablero y qué es política

| Sub-parámetro | ¿Piso (LEY, **no votable**)? | ¿Entra en `PESOS_PISO`? | ¿Tablero? | ¿Óptimo (POLÍTICA, **votable**)? |
|---|---|---|---|---|
| **C1 · CSI fluvial ≥ 95 %** | 🟡 **propuesto** (`PROPUESTA NO RATIFICADA`) | 0,000 hoy → **propuesta: no moverlo** (§5.3, opción A) | Sí, 0,075 | **100 %**, votable |
| **C2 · Cero barreras nuevas sin expediente** | 🟢 **sí** (doctrinal, T14) | Hereda la fila de conectividad | Sí | 0 barreras en la cuenca |
| **C3 · Anchura mínima por grupo declarado** | 🟡 **propuesto**, `[REPORTADO por vía secundaria]` | Hereda la fila de conectividad | Sí | Extremo superior del grupo, votable |
| **C4 · PC, IIC, ECA, malla, fragmentación, vecino más cercano** | 🔴 **no** | **0,000** (correcto y deliberado) | Sí, 0,075 | «bien conectada», sin cifra |
| **C5 · Tendencia no decreciente** | 🟢 **sí** para unidades del ámbito del Reglamento UE 2024/1991; `[HIPÓTESIS]` fuera de él | Hereda la fila de conectividad | Sí | Incremento sostenido |
| **C6 · Red declarada y área de referencia** | 🟢 **sí**, binaria **sin peso** | **0** (binaria) | Sí (registro) | Amplitud y redundancia |
| **C7 · Marina y humedal hidrológico** | 🔴 **no** | **0,000** | Declarado como vacío | — |

**Dos avisos de coherencia que esta tabla obliga a escribir, y que la revisión de la biblioteca debe
resolver.** (a) **El BII del 90 % que sirve de referencia a C3 no se usa aquí con su umbral**: el
[documento 07](07_Formula_de_violacion_y_pesos.md) §4.1 fija **90 % de integridad biótica** frente al
estado de referencia citando a Steffen *et al.*, 2015 vía Richardson *et al.*, 2023, pero **el informe de
fuentes de esta rama no verificó ese umbral**; este documento **lo cita como piso del vecino y no lo
adopta ni lo re-verifica**. (b) **La conectividad hidrológica de humedales no tiene el mismo tratamiento en
toda la biblioteca**: el [documento 11](11_Ecosistemas_Humedales.md) §4 le asigna **peso 0,10** como
Dimensión VIII —un peso que **paga la declaración procedural, no la métrica**, que allí también figura
`[SIN FUENTE VERIFICADA]`—, mientras que aquí C7 la declara **vacío con 0,000**. Las dos lecturas pueden
convivir (una pesa la declaración, la otra la métrica), pero **están escritas de forma que parecen
contradecirse** y se registran aquí en lugar de silenciarse.

**Una consecuencia que conviene leer dos veces: la conectividad es la única dimensión del catálogo cuyo
piso depende de la declaración del propio interesado.** El CSI depende de un inventario de barreras que
la unidad reporta; la anchura, del grupo que la unidad declara; la tendencia, de la métrica y la ventana
que la unidad elige. **Por eso §7.3 y §8.4 son la parte más importante de este documento**: un piso
declarativo sin auditoría es una autoevaluación, y una autoevaluación no es un juez.

---

## 5. Fórmula de violación, pesos y umbrales

### 5.1 El peso que este documento NO mueve

La fórmula pertenece al [documento 07](07_Formula_de_violacion_y_pesos.md) y la especificación del
invariante al [documento 08](08_INV2-E_invariante.md). **Este documento no las edita y no cambia ni un
peso.** Los valores vigentes, citados de sus fuentes:

| Vector | Conectividad | Suma del vector | Fuente |
|---|---|---|---|
| `PESOS_TABLERO` | **0,075** | **1,000** | [documento 07](07_Formula_de_violacion_y_pesos.md) §5.3 · [documento 08](08_INV2-E_invariante.md) §5.2 |
| `PESOS_PISO` | **0,000** | **1,000** — la suma de las dimensiones que **sí** tienen piso ([documento 08](08_INV2-E_invariante.md) §5.2); la cifra de cobertura es otra: **0,680** en el catálogo canónico del [documento 08](08_INV2-E_invariante.md) §5.2 · **0,905** en el catálogo propio del [documento 07](07_Formula_de_violacion_y_pesos.md) §5.3 | ídem |

**La disputa de la cifra de cobertura ya está declarada** ([documento 07](07_Formula_de_violacion_y_pesos.md)
§13, pregunta 2) y **este documento no la reabre**: publica su aritmética **contra las dos** y adopta
**0,680 como la cifra canónica**, tal como el [documento 07](07_Formula_de_violacion_y_pesos.md) §5.3
decidió al adoptar el criterio del [documento 08](08_INV2-E_invariante.md). El agujero que la
conectividad representa dentro de ese 0,320 no cubierto es **0,075: el 23,4 % del hueco entero**
(0,075 / 0,320). Es la porción más grande del hueco: el otro componente del 0,320 es el oxígeno disuelto
(0,020), que es menor. **Nota:** en el catálogo del [documento 07](07_Formula_de_violacion_y_pesos.md) §5.3
el hueco es **0,095** (oxígeno 0,020 + conectividad 0,075) sobre una cobertura de 0,905, porque allí el
suelo y el caudal **sí** cuentan como con piso; la proporción de la conectividad dentro de ese hueco es
entonces **0,075 / 0,095 = 78,9 %**. Las dos aritméticas se publican porque las dos están declaradas.

### 5.2 El operador, y por qué la fila tiene que desdoblarse

El [documento 07](07_Formula_de_violacion_y_pesos.md) §3.3 asigna a la conectividad el operador **`min`**
—más es mejor; el piso es un mínimo que se exige superar— con la forma saturada en cero:

```
D = max(0, (requerido − actual) / requerido)          (operador `min`, doc. 07 §3.3)
```

La saturación en cero es la que impide que un ecosistema «des-desafecte» su propio daño (Cap. 16.5
§16.5.14 y la asimetría de `v_ucv` en `app/micromax.py`). Y el operador es el correcto para **todos** los
sub-parámetros de §4.0 salvo C2, C5 y C6, que son binarios. **Dos precisiones sin las cuales la cita
induciría a error.** (a) La forma saturada en cero es un **añadido del [documento 07](07_Formula_de_violacion_y_pesos.md) §3.3**,
declarado ahí como corrección: el operador `min` del [documento 08](08_INV2-E_invariante.md) §5.1 se define
como `(req − actual) / req` **sin** `max(0, ·)`. Este documento adopta la forma del documento 07 y lo dice,
en vez de atribuirle al 08 una saturación que no escribe. (b) Los dos vecinos **invierten la etiqueta** del
operador: el [documento 08](08_INV2-E_invariante.md) §5.1 llama `min` a «menos es mejor» y `max` a «más es
mejor», mientras que el [documento 07](07_Formula_de_violacion_y_pesos.md) §3.3 usa `min` para «más es
mejor» y `max` para «menos es mejor». **Este documento usa la convención del documento 07** —la que hace
que `min` signifique «el piso es un mínimo que se exige superar»— y **registra la inversión como
discrepancia de nomenclatura entre los documentos 07 y 08**, no como una diferencia de fórmula: las dos
formas del cociente coinciden en el resultado y solo el nombre del operador cambia. **Lo que no es
correcto es el campo.** El
[documento 08](08_INV2-E_invariante.md) §4.1 define `conectividad_indice` con estas cuatro celdas:
operador `—`, unidad `—`, piso `[SIN FUENTE VERIFICADA]`, óptimo `[SIN FUENTE VERIFICADA]`. Un campo sin
unidad no puede tener umbral: **41 no es cumplimiento ni incumplimiento hasta saber si son metros,
porcentaje o hectáreas.** Propuesta `[HIPÓTESIS]`, no ratificada, de desdoblamiento del campo:

| Campo propuesto | Unidad | Operador | Piso | Fuente del piso |
|---|---|---|---|---|
| `conectividad_csi_pct` | % (índice 0-100) | `min` | **95** | Grill *et al.* (2019) — `PROPUESTA NO RATIFICADA` |
| `conectividad_ancho_corredor_m` | m | `min` | **por grupo declarado** (30/61/101) | Bentrup (2008) vía NatureConnect (2024) `[REPORTADO]` |
| `conectividad_grupo_declarado` | categoría | `ordinal` | **obligatorio** (sin él, el anterior no se evalúa) | Este documento |
| `conectividad_barreras_nuevas` | hecho binario | `binary` | **0 sin expediente** | T14 (Cap. 5) |
| `conectividad_tendencia` | signo | `binary` | **no decreciente** | Reglamento (UE) 2024/1991 · `[HIPÓTESIS]` fuera de su ámbito |
| `conectividad_paisaje_pc` | adimensional | `min` | **`[SIN FUENTE VERIFICADA]`** | — |
| `area_de_referencia_declarada` | geometría + motivación | `binary` | **obligatorio** | Este documento (Regla 3) |

### 5.3 La aritmética de las tres salidas posibles (y ninguna la decide este documento)

Adoptar el piso del CSI tiene una consecuencia contable y **hay que publicarla con números**. Las tres
salidas son legítimas y **solo la revisión de coherencia de la biblioteca puede elegir**:

| Opción | Qué hace | `PESOS_PISO` conectividad | Cobertura declarada (catálogo del **doc. 08**, canónico **0,680**) | Cobertura declarada (catálogo del **doc. 07**, **0,905**) | Efecto sobre el ejemplo canónico del doc. 07 §5.8 (`v = 0,3804`) |
|---|---|---|---|---|---|
| **A** — **piso sin mover el peso** | El CSI y la anchura entran como parámetros **con piso y sin coeficiente**, apoyados en la regla 1 del [documento 08](08_INV2-E_invariante.md) §5.2 (*«un parámetro con umbral produce `violacion` aunque su peso sea cero»*), con el precedente operativo de `arrecife_dhw` | **0,000** | **0,680** (no cambia) | **0,905** (no cambia) | **La unidad bloquea; `v` y `FE` no cambian** |
| **B** — **mover los 0,075 al piso** | La fila de conectividad pasa entera a `PESOS_PISO` | **0,075** | **0,755** | **0,980** | `v = 0,4250`; `FE ≈ 1,5296` |
| **C** — **desdoblar la fila en dos mitades simétricas** | El piso se queda con la mitad fluvial/estructural y el índice de paisaje conserva la otra mitad | **0,0375** | **0,7175** | **0,9425** | `v = 0,4027`; `FE ≈ 1,4959` |

**Por qué este documento propone la opción A y no las otras dos.** No por prudencia aritmética, sino
porque es **la única que no inventa un número**: la opción B mueve un peso que el
[documento 07](07_Formula_de_violacion_y_pesos.md) §5.3 y el [documento 08](08_INV2-E_invariante.md) §5.2
fijaron en 0,000 por una razón explícita —*una dimensión sin piso tiene déficit idénticamente cero, y
asignarle peso no la mide, la diluye*—, y esa razón **deja de aplicarse en cuanto hay piso**, pero el
**valor nuevo no lo publica ninguna fuente**: 0,075 es el reparto simétrico que el proyecto ya eligió
frente al caudal ecológico, y **moverlo ahora exigiría una nueva decisión de política, no una corrección
técnica**. La opción C es la más elegante y la más peligrosa: **0,0375 no tiene fuente, no tiene simetría
argumentada y no tiene precedente**; sería un número inventado con apariencia de precisión.

**Y la opción A tiene un coste que hay que decir en la misma frase: exige revisar el
[documento 08](08_INV2-E_invariante.md) §4.2**, que hoy lista la conectividad entre los **seis dominios
que no pueden activar INV2-E**. Con la opción A, la conectividad **saldría de esa lista por sus
sub-parámetros fluvial y estructural** y **seguiría dentro por el de paisaje**. Eso no es un detalle de
redacción: es un cambio en la tabla que dice qué puede bloquear un contrato. **Este documento no lo
ejecuta; lo propone y lo registra** (§13, pregunta 2).

**Propiedad formal que la opción A preserva, y que ninguna de las otras dos puede exhibir:** la
cobertura declarada **no se mueve** (`Σ PESOS_PISO = 0,680` en el catálogo canónico), el hueco sigue
publicado, y **lo que cambia no es la aritmética sino el poder de bloqueo**. Es la aplicación literal de
la Regla 6: **el piso y el peso son independientes, y esa independencia es exactamente lo que permite que
esta dimensión deje de ser impotente sin tocar ni un número ratificado.**

### 5.4 Ejemplo aplicado completo, con la aritmética verificable a mano

**La unidad.** La **cuenca del río del conjunto residencial** —unidad fluvial, con el argumento del
[documento 12](12_Ecosistemas_Rios_y_cuencas.md) §Dimensión V: *la conectividad de un río no se puede
evaluar tramo a tramo porque el efecto de una barrera se propaga en las dos direcciones y acumula*—. Se
evalúa **un ciclo TA completo**. Los valores son **ilustrativos** y están construidos para que la
aritmética sea comprobable a mano; **los pisos, en cambio, no son ilustrativos: son los de las fuentes
citadas**.

| Sub-parámetro | Piso (fuente) | Medición | Operador | Déficit `D_i` | Estado |
|---|---|---|---|---|---|
| **C1 · CSI** | ≥ 95 % (Grill *et al.*, 2019) | **72 %** | `min` | `(95 − 72)/95 = **0,2421**` | 🔴 violación |
| **C3 · Anchura de corredor** (grupo declarado: **mamíferos grandes**) | 101 m (Bentrup, 2008, vía NatureConnect, 2024) | **41 m** en el cuello de botella | `min` | `(101 − 41)/101 = **0,5941**` | 🔴 violación |
| **C2 · Barreras nuevas** | 0 sin expediente (T14) | **1 barrera nueva (2024) sin expediente** | `binary` | **no produce déficit: produce estado** | 🔴 violación binaria |
| **C5 · Tendencia** | no decreciente (Reglamento UE 2024/1991) | **decreciente** en 2 ciclos | `binary` | no produce déficit | 🔴 violación binaria |
| **C4 · PC de paisaje** | `[SIN FUENTE VERIFICADA]` | **0,42** | — | **declarada, no calculada** | 🟡 sin piso |
| **C6 · Área de referencia** | obligatoria | **declarada** (polígono de la cuenca + buffer de 5 km) | `binary` | cumple | 🟢 |

**El cálculo, paso a paso.**

```
Agregación intra-dimensión (doc. 07 §5.1, «peor caso medido»):
A_conectividad = max(0,2421 ; 0,5941) = 0,5941

Aporte al PESOS_PISO vigente (0,000):
v_conectividad = 0,5941 × 0,000 = 0,0000        ← NO aporta nada al compuesto

Aporte al PESOS_TABLERO (0,075):
tablero_conectividad = 0,5941 × 0,075 = 0,0446

Veredicto del piso (P1, atomicidad — doc. 08 §8.3):
is_valid = False   →   VIOLACIÓN DECLARADA Y BLOQUEO
```

**Las cuatro lecturas de este resultado, y la cuarta es la tesis del documento.**

1. **El compuesto no se mueve**: sobre el ejemplo canónico del [documento 07](07_Formula_de_violacion_y_pesos.md)
   §5.8 (`v = 0,3804`), la conectividad aporta **0,0000** y `FE` sigue siendo **≈ 1,4630**. *Una cuenca con
   una barrera nueva, un corredor de 41 m y el CSI al 72 % no recarga un solo punto porcentual más.*
2. **Y sin embargo bloquea.** `is_valid = False` por P1: el piso **decide**, el peso solo **dimensiona**.
   Es la Regla 6 funcionando, y es lo que hace que la opción A sea suficiente para dejar de ser impotente.
3. **Si se ratificara la opción B**, el mismo hecho pasaría a costar: `v = 0,3804 + 0,0446 = 0,4250` y
   `FE = e^0,4250 ≈ 1,5296` —es decir, la recarga pasaría de **+46,3 % a +53,0 %**—. Con la opción C
   (mitad simétrica): `v = 0,4027`, `FE ≈ 1,4959`. **La diferencia entre las tres opciones no es
   cosmética: es la diferencia entre bloquear gratis y bloquear cargando.**
4. **El crédito regenerativo no aparece en ninguna de las cuatro líneas del cálculo.** La cuenca puede
   haber restaurado riberas, plantado un bosque de galería y registrado el crédito como R negativo
   ([documento 07](07_Formula_de_violacion_y_pesos.md) §9, F8: `v(u, R) = v(u, R′)`): **la barrera sigue
   ahí y el veredicto es el mismo.** Eso es *«el suelo antes que el saldo»* traducido a la aritmética de
   esta dimensión.

### 5.5 La escala de lectura: la del [documento 07](07_Formula_de_violacion_y_pesos.md) §5.7, sin añadidos

Este documento **no propone bandas nuevas**. Se usa la escala de dos capas ya fijada: el compuesto en
bandas (0 · leve · moderada · severa · crítica · excedida) y, **mandando sobre ella**, la **Capa 2**: *si
existe al menos un parámetro medido bajo su piso, o una dimensión binaria violada, la unidad tiene
violación declarada con independencia de la banda*. El ejemplo de §5.4 es precisamente un caso donde la
banda del compuesto **no se mueve** y el veredicto **cambia**: la Capa 2 es la que decide, y por eso este
documento la cita antes que la banda.

**Y la advertencia simétrica, que este documento debe a su propio catálogo: C5 puede dar un falso positivo
por ciclo natural.** La prohibición 6 de §6.3 impide leer el estado medido como piso, pero no impide el
error inverso: **una caída de la métrica entre dos ciclos TA puede ser el ciclo natural y no una
degradación** —el fuego que abre un mosaico, la inundación que redistribuye el cauce, la sequía que
contrae la cobertura—. El régimen de esos ciclos pertenece al [documento 22](22_Transversal_Ciclos_naturales.md),
que los trata como **sujeto de derecho y no como daño**, y confundirlos con fragmentación sería el mismo
error que este documento prohíbe en el otro sentido. **Regla que se deriva:** una tendencia decreciente
**solo constituye violación de C5 si la caída no es atribuible a la fase documentada de un ciclo natural
declarado en el expediente de la unidad**; si lo es, se registra como **ciclo**, no como violación, y la
carga de acreditar esa atribución recae en quien la invoca —que es el interesado, no el auditor—. Sin esta
precisión, C5 sería el único piso del estándar que castiga un proceso que el canon manda respetar.

### 5.6 El Óptimo de esta dimensión: casi todo vacío, y una parte votable de verdad

De las siete filas de §4.0, **cuatro** tienen el Óptimo en `[SIN FUENTE VERIFICADA]` y **tres** lo tienen
por construcción del proyecto (el 100 % del CSI, la ausencia total de barreras, la amplitud de la red).
La razón es la de siempre ([documento 07](07_Formula_de_violacion_y_pesos.md) §4.3): **la ciencia publica
pisos de riesgo, no plenitudes**. Y aquí hay un dato que sí es del proyecto y conviene dejar escrito: el
Óptimo de conectividad **es la dimensión con el Óptimo más claramente votable de todo el catálogo**,
porque su contenido no es una cifra dudosa sino una **decisión de paisaje**: cuánto corredor se quiere,
con qué anchura, conectando qué. Eso se delibera —categoría `critical`, quórum 60 %, consenso 75 %, T13,
anti-flip-flop 14 días, `CHECK` en BD— y **no se investiga**.

---

## 6. Protocolo de medición (sensores, frecuencias, quién reporta)

El elenco de sensores del SDV-E es del [documento 06](06_Medicion_y_verificacion_T13.md). Aquí se fija **el
protocolo de esta dimensión**: con qué se mide cada sub-parámetro, cada cuánto, quién reporta, y qué es
inadmisible. La conectividad tiene una ventaja instrumental que ninguna otra dimensión del catálogo
tiene —**se mide con datos que ya existen**: cartografía de barreras administrativas, capas de cobertura
del suelo y un índice publicado con datos y código abiertos— y una desventaja que también es única:
**casi todo lo que la mide lo reporta el propio interesado**.

### 6.1 Tabla de protocolo por sub-parámetro

| Sub-parámetro | Instrumento | Frecuencia | Quién reporta | Estado del instrumento |
|---|---|---|---|---|
| **C1 · CSI fluvial** | Inventario administrativo de barreras (número, tipo, posición, **año de construcción**) + cálculo del índice por tramo, con propagación declarada aguas arriba y abajo | **Anual** (barreras) · **cada 5 años** (estado del continuo) | Organismo de cuenca + parte `eco-` + comunidad testigo | 🟡 **dato existe y es global**; el cálculo no está implementado en el proyecto |
| **C2 · Barreras nuevas** | Expediente de carga de la prueba por barrera, con costo de oportunidad documentado y medidas de permeabilidad | En el acto de autorización **y en cada renovación** | Autoridad que autoriza + parte `eco-` + comunidad testigo | 🟢 procedimiento especificado; 🔴 sin registro en el repositorio |
| **C3 · Anchura de corredor** | Cartografía del corredor con **ancho mínimo medido en el cuello de botella** + declaración del grupo taxonómico con su evidencia + contexto (vivienda / senderos) | **Anual** con la capa; en el acto de autorización si hay obra | Parte `eco-` + comunidad de custodia + verificación externa | 🟡 umbral con vía secundaria; 🔴 sin capa ni GIS en el proyecto |
| **C4 · Conectividad de paisaje** | Grafo sobre la capa de cobertura: PC/IIC/ECA, `dPC`, malla efectiva, fragmentación, distancia al vecino más cercano — con **área de referencia, distancia de dispersión, clasificador y fecha declarados** | **Anual**, siempre en la misma ventana | Parte `eco-` + analista declarado | 🟡 instrumento con fuente; 🔴 **sin umbral y sin código** |
| **C5 · Tendencia** | Comparación del índice declarado entre **dos ciclos TA consecutivos** como mínimo, misma ventana y mismo clasificador | La del ciclo TA (**unidad sin decidir**) | Parte `eco-` + comunidad testigo | 🟡 norma de dirección con fuente; 🔴 unidad de ciclo sin decidir |
| **C6 · Red y área de referencia** | Registro público (T13) de la red declarada y de la ventana; verificación de que los corredores **existen en el terreno** | Cada **5 años** | Parte `eco-` + comunidad de custodia + verificador externo | 🟡 marco con fuente (UICN, 2020); 🔴 sin registro |
| **C7 · Marina y humedal hidrológico** | — | — | — | 🔴 **sin instrumento y sin umbral** |

**Lo que esta tabla no da, y se dice:** **no existe un protocolo verificado de duración de violación**
(cuántos ciclos bajo el piso constituyen violación) —el [documento 07](07_Formula_de_violacion_y_pesos.md)
§6.3 ya declaró ese hueco y propuso la aproximación conservadora de contar el ciclo TA completo con
`duracion_aproximada = True`— y **no existe frecuencia con fuente** para ninguna de estas métricas: las
frecuencias de la tabla son **propuestas de este documento** (`[HIPÓTESIS]`), coherentes con las del
[documento 06](06_Medicion_y_verificacion_T13.md) para su dimensión D5, y **no normas**.

### 6.2 Los dos campos de admisibilidad que esta dimensión añade

A los cuatro campos del contrato del [documento 08](08_INV2-E_invariante.md) §6.1 —`valor` + `unidad`,
`ta_periodo` en TA, `fuente_dato`, `evidencia_ref`— esta dimensión añade **dos**, y sin ellos **el número
no se admite**:

| Campo añadido | Por qué es condición de admisibilidad y no un adorno |
|---|---|
| **`area_de_referencia_declarada`** | Porque el valor de PC, IIC, malla efectiva o fragmentación **cambia con la ventana** y la fuente lo declara: *«los rangos resultantes en los que operan algunas métricas de conectividad cambiarán, porque ahora están confinadas a un tamaño predeterminado de ventana»* `[VERIFICADO]`. Sin ventana declarada, el número **no es comparable consigo mismo en el tiempo**, y una serie no comparable está borrada (T13) |
| **`grupo_taxonómico_declarado`** | Porque el piso de anchura **depende del grupo** y entre el mínimo más bajo (30 m) y el más alto (101 m) hay un factor **3,4**. Sin grupo declarado, el piso es **elegible por el interesado**, y un piso elegible no es un piso |

**Regla dura derivada:** si falta cualquiera de los seis campos, el sub-parámetro se trata como **no
medido** (`D_i = None`), lo que produce **cobertura faltante y bandera de opacidad ecológica**, **no
violación** —y **tampoco aprobación** ([documento 08](08_INV2-E_invariante.md) §8.4)—. Los seis son
`valor` + `unidad`, `ta_periodo`, `fuente_dato`, `evidencia_ref` y estos dos, que son **añadido de esta
dimensión** y todavía **no forman parte del contrato del [documento 08](08_INV2-E_invariante.md) §6.1**:
adoptarlos exige editar ese documento, y hasta entonces son condición de admisibilidad **de este estándar**,
no del invariante ya especificado.

### 6.3 Lo que este protocolo prohíbe, y por qué cada prohibición tiene fuente

| # | Prohibición | Fundamento |
|---|---|---|
| 1 | **Citar el «bien conectados» del GBF como si fuera una medición** | La Meta 3 **exige la condición y no da cifra** `[VERIFICADO]`; el GBF exige además que las redes sean *«ecológicamente representativas, bien conectadas y gobernadas equitativamente»*, que es una condición entera, no un valor. El [documento 10](10_Ecosistemas_Bosques.md) §Dimensión V ya identificó esta forma de fraude |
| 2 | **Evaluar la conectividad solo dentro del área de referencia elegida por el interesado**, y declarar la unidad sana mientras su cuenca se fragmenta | La propagación aguas arriba y abajo es el **mecanismo documentado** de la pérdida `[VERIFICADO]`; el [documento 11](11_Ecosistemas_Humedales.md) §Dimensión VIII ya lo prohibió para el humedal |
| 3 | **Medir el ancho del corredor en su punto favorable** en lugar del cuello de botella | El diseño de corredores depende del **punto más estrecho**: es el que decide si la especie pasa |
| 4 | **Usar la distancia de dispersión como umbral normativo** | La fuente la define como **parámetro de entrada del modelo** (*«definir una distancia de dispersión máxima para limitar las conexiones entre nodos»*), **no como norma** `[VERIFICADO]` |
| 5 | **Mezclar la métrica estructural de paisaje con el CSI como si fueran intercambiables** | La fuente separa conectividad **estructural** (Tabla 5.5) de conectividad **funcional** (sección fluvial); no son la misma medida `[VERIFICADO]` |
| 6 | **Copiar el estado medido del mundo como piso** (37 %, 23 %) | Son **`[ESTADO MEDIDO]`**; declararlos piso equivaldría a certificar que el estado actual del planeta es el mínimo aceptable. El [documento 12](12_Ecosistemas_Rios_y_cuencas.md) §Dimensión V nombró este error como *«el más tentador»* y aquí se hereda la prohibición con su número |
| 7 | **Cambiar la ventana entre dos mediciones y presentarlas como serie** | T13: *la contabilidad nunca se borra*; una serie con ventanas distintas está borrada de hecho |

### 6.4 Frecuencia y ciclo TA: por qué aquí la unidad del ciclo no es un detalle de configuración

El [documento 07](07_Formula_de_violacion_y_pesos.md) §5.4b dejó `unidad_de_ciclo_ta` como
**configuración obligatoria y sin valor por defecto**, y con razón: *«elegir "año calendario" por
comodidad de implementación sería colonizar el tiempo del humedal con el calendario del municipio»*. En
conectividad esa decisión tiene una consecuencia material que conviene dejar escrita: **una barrera
hidráulica se mide en décadas y un corredor de bosque en siglos**. Si el ciclo TA se fija en un año
calendario, el contador de ciclos consecutivos del [documento 08](08_INV2-E_invariante.md) §8.6 —que
gobierna la **escalada**, no la magnitud— **escalaría a un ritmo desproporcionado respecto del fenómeno
que gobierna** —tantas veces más rápido cuanto difiera la unidad elegida de la escala real del proceso,
que es lo único que se puede afirmar sin fuente—, y un contrato podría llegar a la retractación por unos
pocos ciclos contados en años de una fragmentación cuya reparación pertenece a otra escala temporal.
**Este documento no elige la unidad** (no tiene fuente, y elegirla es
colonizar el TA): registra que **en esta dimensión la elección es determinante** y que debe hacerse
**por unidad ecológica y con la comunidad de custodia**, no globalmente por comodidad de código
(§13, pregunta 12).

### 6.5 Quién reporta, y la asimetría que no se puede arreglar con instrumentos

**El guardián oráculo consiente, no mide** (Cap. 16.5 §16.5.14; `app/contracts_bp.py`: *«Ecosistemas
(eco-*): consentimiento otorgado por el guardián oráculo»*). **Ninguna aprobación del guardián puede
entrar como valor de un sub-parámetro de esta dimensión.** Y hay una asimetría estructural que este
documento hereda del [documento 09](09_Comparativa_inter_reinos.md) §6 y no puede resolver: **el sujeto
del SDV-E no puede reportar su propio estado** (*«Nosotros registramos la interacción, no la vida interna
del ecosistema»*, Cap. 16.5 §16.5.14), de modo que **quien reporta la conectividad es, casi siempre, quien
se beneficia de haberla fragmentado**. La mitigación no es técnica, es institucional: **comunidad de
custodia, comunidad testigo, verificación externa y registro público con T13**. Sin eso, el protocolo de
esta dimensión sería **una autoevaluación con formato de estándar**.

---

## 7. Verificación y auditoría (T13, guardián, comunidad testigo)

### 7.1 Qué se puede auditar de esta dimensión

| Auditable | Cómo |
|---|---|
| Que el **inventario de barreras está completo** | contraste con el registro administrativo de concesiones y con la cartografía de infraestructura; una barrera es **visible** |
| Que **cada barrera tiene año de construcción** | sin fecha, su expediente no es auditable contra la fecha de declaración del piso |
| Que el **grupo taxonómico declarado corresponde a la fauna acreditada** | cruce con las especies clave de la unidad ([documento 20](20_Transversal_Biodiversidad.md) §4.3) y con las categorías de la Lista Roja |
| Que el **área de referencia está declarada y motivada** | y que **no cambió** entre mediciones de la misma serie |
| Que la **distancia de dispersión declarada tiene fuente** | es entrada de modelo, no norma: debe traer su referencia |
| Que la **tendencia se calculó con la misma ventana y el mismo clasificador** | comparación de `metodo_version` entre ciclos |
| Que el **CSI se reprodujo con datos abiertos** | el cálculo es reproducible por un tercero sin depender del proyecto |
| Que el **crédito regenerativo no alteró el resultado** | propiedad F8 del [documento 07](07_Formula_de_violacion_y_pesos.md) §7.2 |
| Que la **tabla de pesos no cambió sin registro** | hash de la tabla en cada validación ([documento 07](07_Formula_de_violacion_y_pesos.md) §5.3) |

### 7.2 El límite físico de la auditoría de esta dimensión: las fuentes que bloquean a los testigos

Esta dimensión depende de fuentes cuyo **original no es legible por un agente automático**, y eso debe
constar porque afecta a la auditabilidad del propio estándar:

| Fuente | Estado | Consecuencia |
|---|---|---|
| **Bentrup, 2008** (USDA Forest Service) — origen de la Tabla 6.2 de anchuras | **403** (rechaza agentes automáticos) | Las anchuras se citan **por vía secundaria verificada** y se marcan `[REPORTADO]`; **un humano debe abrir el original** (§13, pregunta 7) |
| **Beier, 2019** (*Conservation Biology*) y **Saura *et al.*** (ScienceDirect, Wiley) | **403** | Las reglas y las métricas se citan **por la transcripción con atribución** del documento de directrices |
| **Convención de Humedales (Ramsar)** | **403** en todas las rutas probadas | El vacío de conectividad hidrológica del humedal **no se cierra**, y **no se cita ninguna cifra suya** |
| **AEMA** — indicador de fragmentación del paisaje | **404 en cuatro rutas probadas** | **No existe hoy un indicador europeo accesible de fragmentación** que este estándar pueda adoptar |
| **ETC-DI (2024)** — especificación de cálculo de fragmentación del paisaje | **PDF truncado en 8 388 608 bytes exactos, ilegible** para dos extractores distintos *(estado registrado en la sesión de fuentes de la rama; no re-descargado aquí)* | **No se cita ninguna cifra suya.** Su lectura exigiría una descarga y un visor humanos |

**Lectura honesta de esta tabla:** la conectividad es la dimensión del SDV-E con **mejor dato disponible
en el mundo** (índices globales, capas abiertas, inventarios administrativos) y con **peor acceso
verificable desde el propio proyecto**. Eso no la invalida: la obliga a **declarar la vía** por la que
cita cada cifra, que es exactamente lo que hace este documento.

### 7.3 El fraude propio de esta dimensión, y su antídoto

Los riesgos de seguridad del repositorio (**R4** partes fantasma, **R6** T9 no validado en la creación,
**R13** guardián `eco-` con heurística laxa) afectan a esta dimensión como a todas. Pero la conectividad
tiene **tres fraudes propios** que ninguna otra dimensión del catálogo permite:

| # | Fraude propio | Antídoto propuesto |
|---|---|---|
| **F1** | **Elegir el grupo taxonómico que conviene**: declarar «plantas» (30 m) donde hay mamíferos grandes (101 m) | El grupo se fija por la **composición acreditada** de la unidad, con evidencia de especies clave; declarar un grupo que la unidad no contiene es **violación por declaración falsa**, registrada con T13 |
| **F2** | **Elegir la ventana que conviene**: medir PC sobre un polígono que excluye la matriz fragmentada | `area_de_referencia_declarada` obligatoria **y estable** entre mediciones; cambio de ventana = cambio de serie declarado |
| **F3** | **Declarar la red sin que exista**: corredores en el papel | Verificación en el terreno por **comunidad testigo**; es el fraude **más barato de cometer y el más barato de detectar** |

### 7.4 Dos tests de auditoría que solo esta dimensión necesita

`[HIPÓTESIS de este documento]` — son tests **deterministas, baratos y falsables**, y se proponen porque
la Regla 5 del [documento 07](07_Formula_de_violacion_y_pesos.md) §2 exige que toda propiedad formal tenga
un test nombrado. Se construirían sobre la descomposición `dPC = dPCintra + dPCflux + dPCconnector` que la
fuente sí publica `[VERIFICADO]`:

| Test | Enunciado | Qué demuestra si falla |
|---|---|---|
| **T-ventana** (`test_conectividad_ventana_estable`) | Calcular el índice declarado para la **misma** unidad con **dos** áreas de referencia razonables (el polígono de la unidad y un búfer fijo declarado). Si el **veredicto de cumplimiento cambia**, el índice **no puede ser el piso** de esa unidad | Que el «cumplimiento» era una propiedad de la ventana, no de la unidad (Regla 3) |
| **T-contribución** (`test_conectividad_contribucion_unidad`) | Calcular `dPC` (o `dIIC`) de la unidad. Si su contribución es **prácticamente nula** mientras el índice agregado se mantiene alto, el índice **no está protegiendo la unidad** | Que el índice agregado protege el promedio de la ventana y puede ignorar la pérdida de la unidad (Regla 4) |

**Ninguno de los dos tests existe en el repositorio** (§12), y **ninguno sustituye a un umbral**: son
instrumentos de auditoría **de la métrica**, no pisos. Su valor es que convierten en **comprobación
ejecutable** la razón por la que esta dimensión tiene hoy 0,000 en el piso.

---

## 8. Invariante INV2-E: de estándar a contrato ejecutable

La especificación del invariante es el [documento 08](08_INV2-E_invariante.md). Aquí se enumera
**exactamente lo que esta dimensión le entrega, lo que le exige y lo que le obliga a revisar.**

### 8.1 La interfaz: lo que esta dimensión entrega a INV2-E

| Pieza que INV2-E recibe | De dónde sale | Estado |
|---|---|---|
| `conectividad_csi_pct` con piso **95 %** y operador `min` | §4-C1, §5.2 | 🟡 **`PROPUESTA NO RATIFICADA`** — umbral con fuente, adopción pendiente |
| `conectividad_ancho_corredor_m` con piso **por grupo declarado** | §4-C3, §5.2 | 🟡 `[REPORTADO por vía secundaria]` |
| `conectividad_grupo_declarado` (obligatorio) | §6.2 | 🟡 propuesta de este documento |
| `conectividad_barreras_nuevas` (binaria, T14) | §4-C2 | 🟢 piso doctrinal con precedente en el [documento 12](12_Ecosistemas_Rios_y_cuencas.md) |
| `conectividad_tendencia` (binaria de dirección) | §4-C5 | 🟢 con fuente para el ámbito del Reglamento UE 2024/1991; `[HIPÓTESIS]` fuera |
| `conectividad_paisaje_pc` **sin piso** | §4-C4 | 🔴 `[SIN FUENTE VERIFICADA]` — declarado, no calculado |
| `area_de_referencia_declarada` (obligatorio) | §6.2 | 🟡 propuesta de este documento |
| Agregación intra-dimensión `A_k = max_i D_i` | §5.4, [documento 07](07_Formula_de_violacion_y_pesos.md) §5.1 | 🟡 especificada, sin implementar |
| Escala y prelación del piso | §5.5 | 🟡 la del [documento 07](07_Formula_de_violacion_y_pesos.md) §5.7, sin añadidos |

### 8.2 Lo que cambia en INV2-E con esta dimensión (y lo que este documento NO decide)

**Lo que cambia, si la revisión de coherencia ratifica la opción A de §5.3:** la conectividad **deja de
estar entre los seis dominios que no pueden activar INV2-E** ([documento 08](08_INV2-E_invariante.md)
§4.2) **por sus sub-parámetros fluvial, estructural y de tendencia**, y **sigue estando** por el de
paisaje. La formulación exacta de la fila revisada sería: *«Conectividad — **parcialmente ejecutable**:
`conectividad_csi_pct`, `conectividad_ancho_corredor_m` (con grupo declarado), `conectividad_barreras_nuevas`
y `conectividad_tendencia` **producen violación**; `conectividad_paisaje_pc` **se registra y no se
pondera**»*.

**Lo que este documento NO decide, y no puede decidir desde aquí:** (a) el valor de
`PESOS_PISO["conectividad"]`, que sigue en **0,000** y cuya modificación es POLÍTICA
([documento 07](07_Formula_de_violacion_y_pesos.md) §13, pregunta 1); (b) la cifra de
`cobertura_piso_declarada`, que sigue siendo **0,680** en el catálogo canónico; (c) la retirada de la
conectividad de la tabla del [documento 08](08_INV2-E_invariante.md) §4.2, que es una edición del
documento 08 y **no de este**. Las tres quedan registradas en §13, pregunta 2.

### 8.3 Los tres estados del invariante aplicados a la conectividad

| Estado | Condición en esta dimensión | Consecuencia |
|---|---|---|
| `cumple` | **Todos** los sub-parámetros aplicables están medidos, **ninguno** bajo su piso, y no hay violación binaria | `FE = 1,0`; el crédito regenerativo de esa unidad es **utilizable** |
| `violacion` | **Al menos un sub-parámetro medido bajo su piso** (p. ej. CSI al 72 %), **o** una dimensión binaria violada (barrera nueva sin expediente, tendencia decreciente) | `FE = e^v`; **bloqueo**; ciclos consecutivos avanzan; crédito **en cuarentena** |
| `indeterminado` | **No hay violación medida y falta al menos un sub-parámetro con piso** | **No hay bloqueo por piso**; **bandera de opacidad ecológica** y obligación de instrumentar; **no habilita crédito** |

**Y el estado real de hoy, sin adornos: `indeterminado` para todas las unidades del planeta.** No hay un
solo inventario de barreras, una sola capa de corredores ni un solo cálculo de PC conectado al sistema. El
[documento 08](08_INV2-E_invariante.md) §8.4 ya declaró que *«el estado por defecto del SDV-E hoy es
`indeterminado`, no `cumple`»*; en esta dimensión eso significa, además, que **hoy no se puede declarar
cumplimiento de conectividad ni por error ni por optimismo, y que ningún crédito regenerativo puede
acreditarse por conectividad restaurada** ([documento 08](08_INV2-E_invariante.md) §9.5).

### 8.4 El bloqueo precautorio: la vía que funciona incluso sin umbral

Es la pieza del [documento 08](08_INV2-E_invariante.md) §8.5 que **más valor tiene en esta dimensión**,
porque la conectividad es el caso donde la irreversibilidad es máxima: *«la carga de la prueba recae
sobre quien propone acciones que afectan la temporalidad de no-participantes»* (T14, Cap. 5), y **una
barrera hidráulica dura siglos**.

| Vía | Cuándo se activa en conectividad | Resultado |
|---|---|---|
| **Bloqueo por piso** | CSI medido bajo 95 %, o ancho bajo el mínimo del grupo declarado, o barrera nueva sin expediente | `should_block_action = True` |
| **Bloqueo precautorio** | **No hay medición de conectividad** para la unidad **y** la acción propuesta es **irreversible** (nueva barrera, nuevo desarrollo en un cuello de botella, nueva infraestructura lineal que corta un corredor) | `precautionary_block = True`, con `evidencia_ref` del **costo de oportunidad asumido** |

**Consecuencia doctrinal que este documento subraya:** en conectividad, **lo que no tiene cifra puede
seguir bloqueando una acción irreversible**. El 0,000 del piso priva a la dimensión de **cuantificar el
daño**; **no la priva de impedirlo**. Y como la irreversibilidad de una barrera es alta y verificable
—*hay o no hay barrera*—, **el bloqueo precautorio es hoy la única protección real y ejecutable de la
conectividad en el sistema**.

### 8.5 Contador, retractación y las dos rehabilitaciones

| Pieza | Aplicación a esta dimensión |
|---|---|
| **Contador de ciclos consecutivos** | Gobierna la **escalada**, no la magnitud ([documento 08](08_INV2-E_invariante.md) §8.6). `max_consecutive_cycles` **sin valor por defecto**: en conectividad el ciclo TA debe decidirse **por unidad** (Regla 7 y §6.4), y **no puede modificarse mientras exista una violación abierta** |
| **Objeto de la retractación** | `objeto_de_retractacion ∈ {"contrato", "actividad", "ninguno"}` — **nunca «unidad_ecologica»**. Un río no se retracta: se retracta **la actividad que lo fragmenta** |
| **Rehabilitación de la actividad** | Cesar o reducir de forma verificable la presión, con `evidencia_ref`: **la barrera se retira, la obra se detiene, la concesión no se renueva** |
| **Rehabilitación de la unidad** | **Recuperar el piso medido**: el CSI vuelve a ≥ 95 %, o el corredor recupera el ancho mínimo del grupo declarado, **medido en TA posterior**. **No depende de la voluntad del violador** |

**La separación de las dos rehabilitaciones es, en esta dimensión, la diferencia entre restaurar y
firmar.** Un contrato que declare «rehabilitada» la conectividad porque se firmó un acta de compromiso
**no ha rehabilitado nada**: el hecho que lo demuestra es **una medición posterior en TA**, y en
conectividad esa medición es de las más fáciles de hacer del estándar entero —una barrera es visible y una
capa de cobertura es pública—.

---

## 9. El suelo antes que el saldo (no compensación)

**La regla es canónica y este documento solo la traduce a su dimensión:** *«Un conjunto con crédito
regenerativo acumulado pero humedal bajo su SDV-E no está en coherencia: INV2-E será su juez»*
(Cap. 16.5 §16.5.14). El crédito regenerativo vive en el componente **R** del VHV, que **sí admite
negativos** (EVV-1.2 §4.3), implementado y probado con `r_units = -12.0` en `app/micromax.py` y
`tests/test_micromax.py` `[VERIFICADO]`, y **la fórmula del [documento 07](07_Formula_de_violacion_y_pesos.md)
§5 no tiene un término `R`**: la propiedad **F8** (`v(u, R) = v(u, R′)` para todo `R`, `R′`) no es un
acuerdo de caballeros, es la consecuencia de que **la variable no existe en la expresión**. El ejemplo de
§5.4 lo muestra con números: **una cuenca con una barrera nueva y el CSI al 72 % bloquea igual con −12 R
que con −12 000 R.**

**Y hay una asimetría específica de esta dimensión que conviene dejar escrita, porque es la única del
catálogo donde el crédito y el piso pueden apuntar en la misma dirección.** Restaurar la conectividad
—retirar un azud, revegetar un corredor, recuperar una llanura de inundación— **mejora la medición del
piso**: el CSI sube, el ancho crece, la tendencia se invierte. Ninguna otra dimensión tiene esa
propiedad con tanta claridad: un crédito de agua no arregla un suelo erosionado ni un crédito de suelo
arregla un pH. **La consecuencia práctica es la que hay que blindar, y es una regla:**

> **La mejora de conectividad cuenta cuando se MIDE en TA, nunca cuando se declara.** Un corredor
> plantado y no medido no acredita cumplimiento ni crédito; un corredor plantado **y medido** en el ciclo
> TA siguiente **sí mejora el piso**, y ese es el único camino legítimo por el que el crédito regenerativo
> puede tocar esta dimensión.

**El paralelo con `v_ucv`, y por qué importa en conectividad más que en ninguna otra parte.** El motor
impide que el componente V sea negativo —*«una vida afectada no se des-afecta en la misma cuenta»*
`[VERIFICADO en `app/micromax.py`]`—. Aplicado a la fragmentación, la asimetría es todavía más fuerte que
en el resto del catálogo, porque **la conectividad perdida no se recupera en el mismo TA**: el cierre de
dosel de un bosque y la recuperación de un continuo de sedimento en un río pertenecen a escalas
multidecenales, **sin cifra publicada en la rama** (`[HIPÓTESIS]` de orden de magnitud, §2 Regla 7). **El crédito
puede comprar la restauración; no puede comprar el tiempo.** Y el tiempo del territorio **es TA y no se
coloniza** (Cap. 16.5 §16.5.14): no hay tipo de cambio que convierta un año de presupuesto humano en un
año de maduración de un corredor.

---

## 10. Zona Libre: lo que NO se mide

*«Parte del valor del humedal es inefable (Cap. 7 §7.9). Los sensores miden salud (agua, cobertura,
biodiversidad indicadora); jamás "milagros". Medir todo sería la forma técnica de dejar de escucharlo»*
(Cap. 16.5 §16.5.14).

**Traducción formal para esta dimensión:** la Zona Libre del Reino Natural es una **dimensión binaria
auditable sin peso**. No tiene término en `v(u)`, no se cuantifica, no se canjea y **su ausencia no
resta**. En conectividad, el borde declarado tiene un contenido propio y hay que nombrarlo: **lo que la
métrica de conectividad no mide es el libre movimiento en sí**. La definición canónica habla de *«el libre
movimiento de especies y el flujo de los procesos naturales que sostienen la vida en la Tierra»* (§3.1), y
**una distancia de grafo no es un movimiento**: es su sombra geométrica. Entre el corredor declarado y el
paso efectivo de un animal hay una diferencia que **ningún índice de paisaje captura**, y esa diferencia
es exactamente la clase de cosa que el canon prohíbe convertir en número.

**Y el riesgo específico de esta dimensión, que es mayor que en ninguna otra: aquí la tentación de medir
todo es máxima.** La conectividad es la dimensión donde la tecnología ofrece más instrumentos que miden
**demasiado**: collares GPS, cámaras trampa, ADN ambiental, marcaje individual. Un estándar que exigiera
«probar el movimiento» para declarar conectividad estaría instrumentando **vigilancia de la fauna** con
el vocabulario de la conservación, y estaría convirtiendo el corredor en un tubo de observación. La línea
del canon es explícita —*medir todo sería la forma técnica de dejar de escucharlo*— y su aplicación aquí
se propone así `[HIPÓTESIS]`:

> **LEY (no votable).** Que exista Zona Libre en esta dimensión y que **no se pondere**: el canon la
> nombra (Cap. 16.5 §16.5.14, Cap. 7 §7.9) y ponderarla permitiría que un buen índice de paisaje
> **pagara** por la pérdida de lo que no se mide, que es lo que *«el suelo antes que el saldo»* prohíbe.
> **Queda fuera del cálculo**: el movimiento efectivo de las especies, el valor del corredor como lugar,
> y todo lo que exija seguir individuos para demostrar conectividad.
>
> **POLÍTICA (votable).** **Qué entra en el catálogo de lo no medido** en cada unidad ecológica concreta
> —y con ello qué deja de medirse— se vota con la categoría `critical` (quórum 60 %, consenso 75 %, T13,
> anti-flip-flop 14 días, `CHECK` en BD), igual que la plenitud aspiracional.

**La advertencia que cierra la sección, y que es la más importante de este documento sobre este tema:**
como la conectividad es hoy la dimensión **con menos piso**, es también la que más fácilmente puede
llenarse de **medición decorativa** —índices calculados, mapas vistosos, corredores dibujados— sin
proteger nada. El catálogo de lo inefable **no es la excusa para no medir lo medible**: es la frontera
que impide que la medición se convierta en el sustituto de la protección.

---

## 11. Comparativa inter-reinos (SDV-H · SDV-A · SDV-E · SDV-S)

La comparación completa es el [documento 09](09_Comparativa_inter_reinos.md). Lo pertinente aquí es **la
conectividad como objeto de protección en los cuatro reinos**, y lo que aparece en esa comparación es un
hallazgo que ninguna otra dimensión del catálogo produce.

| # | Eje | **SDV-H** — humanos | **SDV-A** — animales | **SDV-E** — ecosistemas | **SDV-S** — sintéticos |
|---|---|---|---|---|---|
| 1 | **¿Tiene una dimensión de vínculo?** | Sí, del sujeto: **conexión social** (Cap. 10 §10.4 y doctrina del SDV-H) | Sí, del sujeto: **espacio vital**, **movimiento** y **comportamiento natural** (Cap. 9 §9.4) | Sí, **y es la única cuyo objeto es el vínculo mismo entre unidades** (Cap. 10 §10.4) | 🔴 **No consta en esta biblioteca** y este documento **no la inventa**: no verificado en esta sesión |
| 2 | **¿De quién es el vínculo?** | De la persona: sus lazos | Del individuo: su ámbito y su desplazamiento | **Del espacio entre las unidades**: el corredor no pertenece a ningún parche | — |
| 3 | **¿Quién puede declarar su conectividad?** | **La persona** (y es auditable) | El tenedor o tutor, con responsabilidad jurídica | 🔴 **Nadie**: el sujeto no reporta (Cap. 16.5 §16.5.14) y quien reporta suele ser quien fragmentó | — |
| 4 | **Instrumento** | Instrumentos estandarizados por dimensión (Cap. 8 §8.6) | Observación etológica (Cap. 9 §9.9) | CSI fluvial + métricas de grafo + inventario de barreras y corredores | — |
| 5 | **¿Piso numérico?** | Sí, por necesidad | Sí, **por especie** | 🟡 **Parcial**: fluvial **sí** (CSI ≥ 95 %); paisaje **no** (`[SIN FUENTE VERIFICADA]`) | — |
| 6 | **Moneda temporal** | **TVI** (Cap. 5) | **TA**, traducido por el PIU | **TA**; *«el tiempo del territorio es TA y no se coloniza»* (Cap. 16.5 §16.5.14) | **TPI** |
| 7 | **Representación** | La persona misma | Tutor legal | Parte `eco-` + guardián oráculo; **quórum N-de-M sin N ni M** | La propia instancia, con auditoría cruzada AOS |
| 8 | **Quién audita** | Auditoría independiente | Certificación sin conflicto de interés | 🔴 **Sin par del propio reino**: ciencia, teledetección, comunidad testigo | AOS |
| 9 | **Remedio tras la violación** | Rehabilitación (Dim. VIII) y reintegración | Prohibición de mercado si es sistemática | 🔴 **Ninguno que devuelva lo perdido en el mismo TA** | Retractación + Capa de Ternura |
| 10 | **Origen del piso** | Dignidad y capacidades | **Diseño biológico** + etología | **Diseño biológico del ecosistema** (Cap. 16.5 §16.5.14) | Coherencia y precaución |

**Los tres hallazgos que solo se ven al comparar la conectividad entre reinos.**

**H1 — El SDV-E es el único estándar que protege una relación, y no un estado.** Los reinos H, A y S
protegen **entes** (una persona, un animal, una instancia) y sus dimensiones de vínculo —conexión social,
movimiento, espacio vital— son **propiedades del sujeto**: se pueden medir sobre él y, en el caso humano,
**él mismo las declara**. El SDV-E protege **el intervalo**: un corredor no es un atributo de ningún
parche, es la relación entre ellos. **Consecuencia métrica directa y es la clave de todo este documento:
un piso sobre una relación no puede medirse sobre un sujeto**, y por eso el intento de dar piso al índice
de paisaje de una unidad concreta estaba condenado desde el principio a medir la ventana en lugar de la
unidad.

**H2 — La asimetría de declaración es máxima precisamente en la dimensión más relacional.** El SDV-H
tiene un sujeto que puede declarar su conexión social y un auditor independiente; el SDV-A tiene un tutor
humano jurídicamente localizable; el SDV-S **registra su propio estado en bitácora**. **El SDV-E es el
único caso donde el objeto protegido —el vínculo— no tiene ni voz ni tutor con autoridad verificada**, y
donde el dato lo aporta, casi siempre, **una de las partes interesadas en romperlo** (R4 y R13). Esa
combinación —objeto relacional + sujeto mudo + reportante interesado— no se da en ninguna otra dimensión
del catálogo y es la razón de que §7.3 y §7.4 existan.

**H3 — El principio precautorio pesa más aquí que en ningún otro reino, porque la irreversibilidad es
mayor.** En el SDV-H hay rehabilitación; en el SDV-S hay retractación y Capa de Ternura; en el SDV-A hay
prohibición de mercado. En el SDV-E **el remedio no devuelve lo perdido en el mismo TA**
([documento 09](09_Comparativa_inter_reinos.md) §9). Y en conectividad eso es especialmente literal: **una
barrera retirada no devuelve el continuo perdido en el mismo ciclo**, y un corredor de bosque madura en
escala de siglo. T14 —menor irreversibilidad, carga de la prueba sobre quien propone— **deja de ser un
principio y pasa a ser el instrumento operativo principal de esta dimensión** (§8.4), porque es el único
que funciona **antes** de que exista el umbral.

---

## 12. Estado de implementación

Verificado por lectura directa del repositorio y por búsqueda de patrones en el código, en octubre de
2026. **La regla de honestidad del inventario de la rama se aplica sin excepciones: 🔴 para todo lo que no
tiene código y tests.**

### 12.1 La conectividad en el código

| Pieza | Estado | Evidencia verificada |
|---|---|---|
| `SDV_E` (tipo con dimensiones y pesos) | 🔴 **no existe** | `maxocontracts/core/types.py` define `SDV` y `SDV_S`; **no hay `SDV_E`** |
| `SDV_EValidatorBlock` | 🔴 **no existe** | `maxocontracts/blocks/` contiene `action.py`, `condition.py`, `gamma_protector.py`, `reciprocity.py`, `sdv_s_validator.py`, `sdv_validator.py`, `ternura.py`; **no existe `sdv_e_validator.py`** |
| Campo `conectividad_indice` | 🔴 **no existe en código** | Solo está especificado en el [documento 08](08_INV2-E_invariante.md) §4.1 y en su esqueleto propuesto, marcado como **no implementado** |
| INV2-E | 🔴 **no existe** | Es el agujero que esta biblioteca cierra (Cap. 16.5 §16.5.14) |
| Búsqueda de `conectividad`, `connectivity`, `corredor`, `CSI`, `malla` en `maxocontracts/` | 🔴 **cero coincidencias** | El motor de dominio puro **no conoce la conectividad** |
| La misma búsqueda en `tests/` y en `scripts/` | 🔴 **cero coincidencias** | **No hay un solo test ni script** que mencione conectividad ecológica |
| Cálculo del **CSI** (Grill *et al.*) | 🔴 **no existe** | Ningún ingestor, ningún cálculo. **Es la implementación más barata de toda la dimensión**: la fuente publica sus valores **bajo CC-BY-4.0** y declara que pueden recalcularse **con su código fuente** `[VERIFICADO]`; la única pieza con licencia restringida son las **bases de datos de represas**, que la fuente remite a un portal externo |
| **Inventario de barreras** | 🔴 **no existe** | Especificado en el [documento 12](12_Ecosistemas_Rios_y_cuencas.md) §Dimensión V; **sin tabla, sin seeds, sin data-model** |
| **Cartografía de corredores** y medición de anchura | 🔴 **no existe** | Sin capa, sin GIS, sin ingestores |
| **Métricas de paisaje** (PC, IIC, ECA, `dPC`, malla efectiva, fragmentación, vecino más cercano) | 🔴 **no existe nada** | Cero cálculo, cero dependencia, cero dato |
| **`area_de_referencia_declarada`** | 🔴 **no existe en ninguna parte** | Es una **propuesta de este documento** (§6.2) |
| **Tests T-ventana y T-contribución** | 🔴 **no existen** | Propuestos en §7.4 |
| Sensores, APIs, satélites o ingestores ecológicos en `app/` | 🔴 **cero** | Confirmado por el inventario de la rama y por búsqueda directa |
| **Índice de Salud Ecosistémica (ISE)** | 🟡 **documento, sin código** | `docs/architecture/metricas_detalle_kpis_oraculos_dinamicos.md`, IN-01 — y **no incluye conectividad** |
| Crédito regenerativo (`r_units` negativo) | 🟢 **implementado y probado** | `app/micromax.py`; `tests/test_micromax.py` con `-12.0` — **pero no pesa en ninguna cuenta y no tiene nada que ver con conectividad** |
| Auditar el **estándar** (no el ecosistema) | 🟢 **existe y es real** | `tests/test_sdv_e_biblioteca.py` audita la plantilla, las frases vetadas, las anclas de línea y el sustento documental de **todos los documentos** de esta biblioteca; `scripts/verificar_enlaces_sdv_e.py` comprueba el **estado HTTP real** de cada URL citada, con veredicto duro |

### 12.2 Dos homónimos que hay que nombrar para que nadie los lea como implementación

La búsqueda de términos de conectividad y fragmentación en el repositorio **sí devuelve coincidencias**,
y **ninguna es ecológica**. Es un hallazgo de la auditoría y se publica:

| Término encontrado | Dónde | Qué es **realmente** | Riesgo si no se nombra |
|---|---|---|---|
| `fragmentation_factor` | `app/micromax.py` (definición, validación y cálculo), `app/micromax_bp.py`, `app/schema.sql` | Un factor **doméstico y comunitario**: entra en `fic = attention_factor * fragmentation_factor * loneliness_factor` y se valida en el rango **[1,0 · 1,8]**. **No tiene ninguna relación con la fragmentación del paisaje** | Que una búsqueda de «fragmentación» en el repositorio **parezca** que la fragmentación ecológica está medida y tiene rango validado |
| «Guía de Conectividad» | `frontend/app/contracts/builder/page.tsx` (bloque «Guía de Conectividad Liminal», «Reglas de Integridad del Grafo») | La guía de **conectividad del grafo de un contrato** (nodos y aristas del constructor visual). **No es conectividad ecológica** | Que la palabra «conectividad» en la interfaz **parezca** una funcionalidad del SDV-E |

**Consecuencia honesta, en una frase:** el proyecto tiene hoy **crédito regenerativo sin juez**,
**estándar sin motor** y **conectividad sin una sola línea de código**; lo único que la conectividad
comparte con el repositorio actual es **el nombre de dos objetos que no son ella**.

### 12.3 Lo que sí existe, y no es poco: la biblioteca es auditable aunque la contabilidad no lo sea

Hay una pieza implementada que este documento debe reconocer porque **es la única que hoy protege algo**:
`tests/test_sdv_e_biblioteca.py` y `scripts/verificar_enlaces_sdv_e.py` convierten las reglas duras del
brief en **verificaciones deterministas** —plantilla canónica, separación de Mínimo Absoluto y Óptimo,
declaración de LEY y POLÍTICA, ausencia de las frases vetadas, cero anclas de línea, mínimo de sustento
externo y **estado HTTP real de cada URL citada**, con clasificación explícita de las fuentes bloqueadas y
las muertas—. Es decir: **el estándar del Reino Natural todavía no puede medir un ecosistema, pero ya
puede auditar sus propios documentos, y esta dimensión pasa esa auditoría sin excepciones.** La
conectividad ecológica no está implementada; **la honestidad sobre la conectividad ecológica, sí**.

---

## 13. Preguntas abiertas

Lo que **no** sé, y no finjo cerrar.

**1. El piso de la conectividad de paisaje no existe, y hay que decir con precisión qué haría falta para
cerrarlo.** Se buscó y **no se halló** en: CBD (Metas 2, 3, 12 y Meta A), UICN (Lineamientos n.º 30
completos, 146 pp.), CMS (Resolución 14.16 completa), UNEP-WCMC/Protected Planet, AEMA (rutas 404),
ETC-DI (PDF ilegible), UNCCD (rutas 404) y NatureConnect D6.1 (Tabla 5.5 **sin columna de umbral**).
**Ni un solo organismo publica un valor mínimo universal.** Los caminos para cerrarlo, en orden de coste:

| # | Camino | Qué se necesita | Viabilidad |
|---|---|---|---|
| 1 | **Adoptar el CSI ≥ 95 %** como piso **de unidades fluviales** | Nada más: la fuente está verificada en esta sesión, el umbral es explícito y el dato es global, reproducible y **publicado con su código fuente** (con la salvedad de licencia de las bases de represas) | **Inmediata** — es la única puerta abierta hoy |
| 2 | **Piso binario estructural** para el resto (cero barreras nuevas sin expediente, tendencia no decreciente) | Decisión de gobernanza del proyecto, **no de fuente**. Precedente: [documento 12](12_Ecosistemas_Rios_y_cuencas.md) | **Inmediata**, pero es LEY del proyecto, no norma científica |
| 3 | **Leer las fuentes primarias bloqueadas** (Bentrup 2008 USDA; Beier 2019; Saura; Jaeger 2000; ETC-DI 2024) | Una persona con navegador —no un bot— descargando cinco PDF; la Tabla 6.2 ya está transcrita en la vía secundaria | **Baja** (humano, ~1 hora) |
| 4 | **Construir el umbral por consenso científico** | Un panel tipo IPBES/CBD-AHTEG que fije un valor universal de PC, malla efectiva o fragmentación. **Hoy no existe y ningún organismo está en proceso de fijarlo** | **No disponible** — y hay que decirlo así |

**2. La decisión que este documento NO toma: qué hacer con los 0,075 del piso.** Las tres salidas de §5.3
—A (piso sin mover el peso), B (moverlo) y C (desdoblar la fila en mitades simétricas)— están calculadas
con sus consecuencias exactas, y **la elección no es de este documento**: exige, como mínimo, editar la
tabla de §4.2 del [documento 08](08_INV2-E_invariante.md) y ratificar o no un valor nuevo de
`PESOS_PISO`. **Propongo la opción A porque es la única que no inventa un número**, y lo dejo dicho como
propuesta, no como decisión.

**3. Discrepancia real con el [documento 12](12_Ecosistemas_Rios_y_cuencas.md) §Dimensión V.** Ese
documento registra para el umbral numérico de conectividad: *«`[SIN FUENTE VERIFICADA]` — el estudio mide;
no fija umbral»*, y más abajo: *«Y no fijaron un umbral, porque su artículo es una medición y no una
norma»*. **La segunda mitad es exacta; la primera es imprecisa:** el artículo **sí publica un umbral** (el
95 % de CSI, como línea de corte explícita de su clasificación, en su Fig. 2 `[VERIFICADO en esta
sesión]`) y **no fija un piso normativo**. La conclusión del documento 12 —piso estructural para el río—
**sigue siendo defendible y no la revierto**; lo que hace falta es corregir **la razón registrada**, que
es de la que depende que el 95 % pueda adoptarse. **No edito el documento 12**: lo registro aquí para la
revisión de coherencia.

**4. Refinamiento de la matriz del [documento 09](09_Comparativa_inter_reinos.md) §11.3.** Allí se
registra, para conectividad: *«ningún valor de índice de conectividad (PC, ECA) ni anchura mínima de
corredor en fuente oficial»*. **La primera mitad se confirma** (no hay valor de PC ni de ECA en fuente
oficial). **La segunda se refina**: **sí existen anchuras mínimas por grupo taxonómico** (30 / 61 / 101 m)
y reglas de contexto (2 000 m; 3 000-6 000 m; 400-1 000 m), verificadas en esta sesión **en la vía
secundaria**, mientras **la fuente primaria sigue bloqueada (403)**. La frase del documento 09 es
literalmente correcta si «fuente oficial» significa «leída en el original»; **es incompleta si se lee como
«no existen cifras»**. La distinción importa y por eso se publica.

**5. La petición del [documento 12](12_Ecosistemas_Rios_y_cuencas.md) sobre el DCI queda INCUMPLIDA.** Ese
documento pidió a este que verificara el **Índice de Conectividad Dendrítica** (Cote *et al.*, 2009),
citado solo en resultados de búsqueda. **No lo verifiqué: ni su URL ni su escala**, y por tanto **no lo
adopto**. Queda como petición abierta, no como tarea hecha.

**6. La causa registrada del fallo de la UICN en el [documento 02](02_Unidad_y_sujeto_del_SDV-E.md) §12.3
es incorrecta.** No fue un *«fallo de parseo del PDF, tres intentos»*: **el archivo guardado en el
repositorio de trabajo con el nombre de las directrices de conectividad contenía otro documento** (un
informe de Soluciones basadas en la Naturaleza en las NDC). La conclusión del documento 02 —no hay umbral
en la fuente— **no cambia y ahora está verificada por lectura completa**; lo que debe corregirse es **el
motivo**, porque un fallo de herramienta y un archivo equivocado tienen consecuencias distintas para
quien retome el trabajo.

**7. La fuente primaria de las anchuras de corredor no se pudo leer.** Las cifras provienen de la
**transcripción con atribución explícita** de un documento de directrices verificado (HTTP 200, texto
extraído en esta sesión), mientras **`fs.usda.gov` devuelve 403 a los agentes automáticos**. Es decir:
**este documento no ha leído a Bentrup (2008)** y lo marca `[REPORTADO]`. Un humano con navegador lo
cierra en una hora.

**8. El U-11 del [documento 02](02_Unidad_y_sujeto_del_SDV-E.md) se desbloquea a medias.** Aquel
documento dejó el *«ancho funcional de corredor entre ocurrencias»* como **marca bloqueada por falta de
umbral**, con la cifra delegada a este documento. Aquí llegan **cifras con fuente secundaria por grupo
taxonómico**, de modo que **el bloqueo puede levantarse en parte**; pero **la marca no puede pasar a
verde mientras (a) la fuente primaria no se lea y (b) la unidad no declare su grupo taxonómico**, porque
el piso depende de ese grupo y sin él no hay número.

**9. El grupo taxonómico declarado convierte el piso en elegible por el interesado, y no sé cómo
cerrarlo del todo.** Entre el mínimo de «plantas» (30 m) y el de «mamíferos predadores grandes» (101 m)
hay un factor **3,4**. §7.3 propone que el grupo se fije por la **composición faunística acreditada** y
que declarar un grupo ausente sea **violación por declaración falsa**. **No sé quién acredita esa
composición** ni con qué evidencia mínima: es una decisión de gobernanza, no de fuente.

**10. El área de referencia: quién la fija, y con qué límite.** Sin ella el índice no es interpretable
(Regla 3); con ella, **quien la elige elige el resultado**. Propongo que sea **obligatoria, motivada y
estable entre mediciones**, y **no sé cuál debe ser el criterio de suficiencia** de esa motivación. Es
POLÍTICA, y de la más difícil: es la decisión que determina si el piso de paisaje es algún día posible.

**11. La unidad de esta dimensión sigue sin estar decidida —y aquí no es una cuestión formal.** El
[documento 02](02_Unidad_y_sujeto_del_SDV-E.md) decide la unidad del SDV-E; el
[documento 12](12_Ecosistemas_Rios_y_cuencas.md) argumenta que **para un río la unidad tiene que ser la
cuenca** porque la conectividad se propaga. **Este documento hereda ese argumento y no lo extiende a los
demás tipos** (¿la unidad de un bosque fragmentado es el bosque, el paisaje o la red?), porque extenderlo
sería decidir la unidad del estándar desde una dimensión transversal.

**12. La unidad del ciclo TA es determinante en esta dimensión y sigue sin fuente.** Una barrera
hidráulica opera en **décadas** y un corredor de bosque en **siglos** (orden de magnitud declarado
`[HIPÓTESIS]`: **sin fuente**, §2 Regla 7); un contador de ciclos consecutivos
fijado en años calendario **escalaría a un ritmo desproporcionado respecto del fenómeno que gobierna**. Propongo
que la unidad se fije **por unidad ecológica y con la comunidad de custodia**; **no propongo cuál**,
porque no hay fuente y elegirla es colonizar el TA (§6.4).

**13. Conectividad marina y conectividad hidrológica de humedales: sin umbral, y confirmado.** El
[documento 13](13_Ecosistemas_Oceanos_y_costas.md) y el [documento 11](11_Ecosistemas_Humedales.md) ya lo
declararon; **esta sesión lo confirma y no lo cierra**. La Convención de Humedales devuelve **403 en todas
las rutas probadas** y **no se cita ninguna cifra suya**.

**14. El indicador europeo de fragmentación del paisaje no es accesible hoy.** Cuatro rutas de la **AEMA**
devuelven **404** y el informe del **ETC-DI (2024)** se descargó **truncado en 8 388 608 bytes exactos**,
ilegible para dos extractores. **No se cita ninguna cifra de ninguna de las dos fuentes.** Si ese
indicador existe en otra ruta, este documento no lo encontró.

**15. La ventana móvil puede invalidar comparaciones entre estudios y entre series.** La fuente declara
que con ese enfoque **los rangos de las métricas cambian** (Yang *et al.*, 2024, citado por NatureConnect,
2024) `[VERIFICADO]`. Consecuencia: **dos unidades medidas con ventanas distintas no son comparables**, y
este documento no puede resolverlo porque la elección de ventana es del analista. Es la misma familia de
problema que el §10 de la pregunta 10 y merece decisión conjunta.

**16. El peso 0,075 de la conectividad sigue sin respaldo empírico.** Es un **reparto simétrico del
proyecto** frente al caudal ecológico, sin fuente que justifique dar más a una que a otra
([documento 07](07_Formula_de_violacion_y_pesos.md) §5.3 y §13, pregunta 1). **No lo reabro**; lo heredo
como está, y lo menciono porque cualquier discusión sobre «cuánto debe pesar la conectividad» empieza por
reconocer que hoy **no pesa en el piso y pesa 0,075 solo en el tablero**.

**17. ¿Qué pasa si la unidad desaparece?** El [documento 02](02_Unidad_y_sujeto_del_SDV-E.md) dejó
abierta la pregunta *«¿qué pasa si el río se seca?»*, y en conectividad tiene una respuesta técnica
incómoda: **retirar los parches de una unidad baja el índice agregado, pero la contribución de la unidad
—`dPCintra`, `dPCflux`, `dPCconnector`— cae a cero y el resto de la ventana puede mantener el índice
alto**. Es decir: **el índice de paisaje puede seguir «bien» después de que la unidad haya dejado de
existir como sujeto**. El piso de una unidad inexistente no está definido, y este documento **no lo
define**.

**18. La cifra de cobertura del piso sigue en disputa entre los documentos 07 y 08 (0,905 frente a
0,680), y este documento no la reabre.** Publica su aritmética contra las dos (§5.3) y **adopta 0,680
como canónica**, siguiendo la decisión del [documento 07](07_Formula_de_violacion_y_pesos.md) §5.3 de
adoptar el criterio del [documento 08](08_INV2-E_invariante.md).

---

## 14. Referencias

**Regla aplicada sin excepciones:** solo se citan URLs cuyo **estado HTTP real y tamaño de cuerpo** se
comprobaron con `curl` en esta sesión de redacción, o cuya verificación está declarada como heredada del
informe de fuentes de la rama. **Ninguna cifra de este documento proviene de una fuente que no se haya
podido leer o cuya lectura se declare prestada.**

### 14.1 Fuentes citadas, verificadas en esta sesión de redacción (HTTP 200 y cuerpo descargado)

| Fuente | URL | Estado |
|---|---|---|
| Grill, G., Lehner, B., Thieme, M., Geenen, B., Tickner, D., Antonelli, A. *et al.* — *Mapping the world's free-flowing rivers*, **Nature 569:215-221 (2019)** | https://www.nature.com/articles/s41586-019-1111-9 | **200** (522 018 bytes; resumen, leyendas de figuras y declaración de disponibilidad de datos leídos en esta sesión). **Conjunto de datos de la fuente, bajo CC-BY-4.0:** DOI 10.6084/m9.figshare.7688801, transcrito en forma corta porque su resolución devolvió **202 con cuerpo vacío** al comprobarla en esta sesión |
| NatureConnect (2024) — *D6.1 Guidelines for connectivity conservation and planning in Europe with supporting web-based inventory and databases* (documento de directrices del proyecto homónimo de Horizonte Europa) | https://naturaconnect.eu/wp-content/uploads/2024/07/D6.1-Guidelines-for-connectivity-conservation-and-planning-in-Europe-with-supporting-webbased-inventory-and-databases.pdf | **200** (9 236 351 bytes; **texto extraído en esta sesión**: Tabla 5.5, Caja 6.2, Tabla 6.2 y descomposición de dPC) |
| UICN (2020) — Hilty, Worboys, Keeley, Woodley *et al.*, *Lineamientos para la conservación de la conectividad a través de redes y corredores ecológicos*, Serie Directrices para Buenas Prácticas en Áreas Protegidas **n.º 30** (edición en español) | https://portals.iucn.org/library/sites/library/files/documents/PAG-030-Es.pdf | **200** (7 060 322 bytes; texto extraído en la sesión de fuentes de la rama; **no re-extraído aquí**) |
| UICN — ficha de la publicación n.º 30 | https://portals.iucn.org/library/node/49137 | **200** (24 985 bytes) |
| UNEP/CMS — **Resolución 14.16 *Ecological Connectivity***, adoptada por la COP14 (Samarcanda, febrero 2024) | https://www.cms.int/sites/default/files/document/cms_cop14_res.14.16_ecological-connectivity_e.pdf | **200** (245 641 bytes; texto extraído en la sesión de fuentes de la rama) |
| CBD (2022) — Marco Kunming-Montreal, **Decisión 15/4** (texto del GBF) | https://www.cbd.int/doc/decisions/cop-15/cop-15-dec-04-en.pdf | **200** (329 142 bytes) |
| CBD (2022) — **Meta 3** del Marco Kunming-Montreal (página oficial) | https://www.cbd.int/gbf/targets/3/ | **200** (94 015 bytes) |
| CBD — informe de progreso de indicadores y metas nacionales, **SBSTTA 28** (Tabla 6: porcentaje de Partes) | https://www.cbd.int/doc/c/5611/c35f/aa96bdcd816f5952d586a777/sbstta-28-02-add1-rev1-en.pdf | **200** (23 965 035 bytes) |
| **Reglamento (UE) 2024/1991** sobre restauración de la naturaleza (texto consolidado) | https://eur-lex.europa.eu/eli/reg/2024/1991/oj | **200** (1 028 908 bytes) |
| UNEP-WCMC / Protected Planet — **Conectividad** y World Database on Ecological Corridors (WDEC) | https://www.protectedplanet.net/en/thematic-areas/connectivity-conservation | **200** (32 100 bytes) |
| **Global Dam Watch** — portal al que la fuente remite las bases de datos de represas (no incluidas en su repositorio de datos por licencia) | https://www.globaldamwatch.org | **200** (144 718 bytes) |
| Protected Planet — portal principal (WDPA, OECM, Lista Verde) | https://www.protectedplanet.net/en | **200** (45 318 bytes) |

### 14.2 Contexto verificado y no citado con cifra

Estas fuentes se comprobaron **200** en esta sesión y **este documento no extrae ninguna cifra de ellas**;
se listan porque acreditan el marco en el que la conectividad se declara problema global:
**Living Planet Index** — https://www.livingplanetindex.org/ (**200**, 7 312 bytes) ·
**IPBES** — https://www.ipbes.net/ (**200**, 125 391 bytes) ·
**Fronteras planetarias (Stockholm Resilience Centre)** — https://www.stockholmresilience.org/research/planetary-boundaries.html (**200**, 107 834 bytes) ·
**FAO, Evaluación de los Recursos Forestales Mundiales** — https://www.fao.org/forest-resources-assessment/en/ (**200**, 100 504 bytes) ·
**UNEP** — https://www.unep.org/ (**200**, 167 270 bytes).

### 14.3 Obras citadas **dentro** de las fuentes verificadas (no leídas en su original)

Estas obras **no se leyeron directamente**: aparecen en el cuerpo y la bibliografía del documento de
directrices de NatureConnect (2024), que las cita con atribución. Se listan con la forma exacta en que la
fuente las identifica, y **los DOI se transcriben en forma corta, sin prefijo, precisamente porque no se
resolvieron en esta sesión**.

- **Bentrup, G. (2008)** — *Conservation Buffers: Design Guidelines for Buffers, Corridors, and Greenways*, USDA Forest Service. DOI 10.2737/SRS-GTR-109. **Origen de la Tabla 6.2 de anchuras de corredor.** La ruta del USDA devuelve **403** a los agentes automáticos: **no leída**.
- **Beier, P. (2019)** — *A rule of thumb for widths of conservation corridors*, *Conservation Biology* **33**, 976-978. DOI 10.1111/cobi.13256. **Origen de la regla de los 2 000 m.** Ruta bloqueada (**403**).
- **Ford, A. T., Sunter, E. J., Fauvelle, C., Bradshaw, J. L., Ford, B., Hutchen, J., Phillipow, N., Teichman, K. J. (2020)** — *Effective corridor width: linking the spatial ecology of wildlife with land use policy*, *European Journal of Wildlife Research* **66**, 69. DOI 10.1007/s10344-020-01385-y. **Origen de las anchuras 3 000-6 000 m y 400-1 000 m.**
- **Métricas y su atribución tal como las da la fuente:** *distancia al vecino más cercano* y *hábitat dentro de un búfer* (Prugh, 2009) · *tamaño efectivo de malla* (Jaeger, 2000) · *índice de cohesión de parches* (Schumaker, 1996) · *radio de giro medio y ponderado por área* (McGarigal, 1995) · *IIC, PC y ECA* (Pascual-Hortal y Saura, 2006; Saura *et al.*, 2011; Saura y Pascual-Hortal, 2007) · *descomposición `dPC` y `dIIC`* (Saura y Rubio, 2010) · *centralidad de intermediación generalizada* (Bodin y Saura, 2010) · *efectos de borde hasta 300 m* (Kennedy *et al.*, 2003) · *345 de 429 mamíferos terrestres* (Tucker *et al.*, 2014) · *ventana móvil y cambio de rangos* (Yang *et al.*, 2024).

### 14.4 Fuentes descartadas (muertas, bloqueadas o ilegibles) — no citables

**Bloqueadas para agentes automáticos (403): son reales y un humano las abre, pero en este documento no
sostienen ninguna cifra leída directamente.** `fs.usda.gov` (Bentrup 2008) · `conbio.onlinelibrary.wiley.com` (Beier 2019) · `science.org` y `sciencedirect.com` (Saura *et al.*) · `sprep.org` · `ramsar.org` (Convención de Humedales: **todas** las rutas probadas; **no se cita ninguna cifra suya**, y por eso el vacío de conectividad hidrológica de humedales sigue abierto).

**Muertas (404): prohibido citarlas.** Cuatro rutas del indicador de fragmentación del paisaje de `eea.europa.eu` (**404 ×4**: la AEMA no publica hoy un indicador accesible en las rutas probadas) · la variante con guion bajo de la Resolución CMS 14.16 (**404**: solo la ruta con guion es válida) · rutas de `unccd.int` sobre degradación (**404**).

**Ilegibles o no verificables.** *(Los estados de este bloque provienen del informe de fuentes de la rama, verificado con `curl` en esa sesión; **no se re-descargaron aquí**, salvo los que se marcan como comprobados en esta sesión.)* `eionet.europa.eu` — especificación de cálculo de fragmentación del paisaje del ETC-DI (2024): descargado con **200**, pero **el PDF está truncado en 8 388 608 bytes exactos y es ilegible** para dos extractores distintos; **no se cita ninguna cifra suya** · `conservationcorridor.org` — un PDF devuelve **200 con cuerpo de 0 bytes**: **no verificable**.

**Archivo mal nombrado en el repositorio de trabajo (corrección de trazabilidad).** El PDF guardado como directrices de conectividad de la UICN en `scratch/sdv_e/tmp/` **no contenía esas directrices**: era un informe sobre Soluciones basadas en la Naturaleza en las contribuciones determinadas nacionalmente. **Ésa fue la causa real del «fallo de parseo» registrado en el [documento 02](02_Unidad_y_sujeto_del_SDV-E.md) §12.3**, y no un fallo del extractor.

**Dominios muertos declarados por el brief, no citados:** `iucnglobalecosystemtypology.org` · `eflows.net`.

### 14.5 Referencias internas al canon (por capítulo y sección, sin anclas de línea)

- **Cap. 10 §10.3** — Principio Precautorio de Consciencia: *«Donde hay duda de consciencia, se asume consciencia.»*
- **Cap. 10 §10.4** — SDV para Ecosistemas (*«Conectividad con otros ecosistemas»*, *«Ciclos naturales respetados»*) y SDV para Lugares (*«Caudal mínimo ecológico»*, *«Riberas protegidas»*, *«Fauna acuática viable»*).
- **Cap. 10 §10.5** — Principio de Proporcionalidad.
- **Cap. 10 §10.6** — Dignidad encadenada: *«Dignidad Humana ←→ Dignidad Ecosistémica ←→ Dignidad Material.»*
- **Cap. 10 §10.7** — *«La gobernanza debe ser operacionalmente finita.»*
- **Cap. 10 §10.8** — Criterios de Persona Sintética.
- **Cap. 16.5 §16.5.14** — SDV-E, *«INV2-E será su juez»*, TA y no colonización, Zona Libre del humedal, 7 campos de identidad de la representación natural, quórum delegado N-de-M, *«Nosotros registramos la interacción, no la vida interna del ecosistema»*, convivencia bidireccional.
- **Cap. 8 §8.11** — Dimensiones binarias sin peso del SDV-H (precedente de la Zona Libre y de la red declarada).
- **Cap. 9 §9.4** — Dimensiones del SDV-A (espacio vital, movimiento, comportamiento natural).
- **Cap. 9 §9.8** — Prohibición de mercado (el `∞` como consecuencia jurídica).
- **Cap. 9.5 §9.5.10** — Veto por Crimen de Coherencia (*«la interrupción total del sistema que la provoca»*).
- **Cap. 5** — **T14, Principio de Precaución Intergeneracional** (menor irreversibilidad; carga de la prueba sobre quien propone); **T9** (no-antropocentrismo); **T13** (la contabilidad nunca se borra).
- **Cap. 5 §5.5** — **PIU**, Protocolo de Intercambio Universal: único traductor TA↔TVI.
- **Cap. 7 §7.9** — Valor inefable.
- **Cap. 17** — INV2: *«Ninguna acción del contrato puede dejar a un participante bajo su SDV.»*
- **EVV-1.2 §4.3** — Componente **R** del VHV y crédito regenerativo (valores negativos admitidos).

### 14.6 Referencias internas a esta biblioteca y al repositorio

- [00 — Índice de la biblioteca SDV-E](00_README_indice.md) · [01 — Doctrina](01_Doctrina_SDV-E.md) · [02 — Unidad y sujeto](02_Unidad_y_sujeto_del_SDV-E.md) · [03 — No colonización del TA](03_No_colonizacion_del_TA.md) · [04 — Zona Libre](04_Zona_Libre_del_Reino_Natural.md) · [05 — Representación, guardián y mandato](05_Representacion_guardian_y_mandato.md) · [06 — Medición y verificación (T13)](06_Medicion_y_verificacion_T13.md) · [07 — Fórmula de violación y pesos](07_Formula_de_violacion_y_pesos.md) · [08 — INV2-E](08_INV2-E_invariante.md) · [09 — Comparativa inter-reinos](09_Comparativa_inter_reinos.md) · [10 — Bosques](10_Ecosistemas_Bosques.md) · [11 — Humedales](11_Ecosistemas_Humedales.md) · [12 — Ríos y cuencas](12_Ecosistemas_Rios_y_cuencas.md) · [13 — Océanos y costas](13_Ecosistemas_Oceanos_y_costas.md) · [14 — Suelos vivos](14_Ecosistemas_Suelos_vivos.md) · [15 — Praderas y sabanas](15_Ecosistemas_Praderas_y_sabanas.md) · [16 — Montañas y criosfera](16_Ecosistemas_Montanas_y_criosfera.md) · [17 — Zonas áridas](17_Ecosistemas_Zonas_aridas.md) · [18 — Agroecosistemas](18_Ecosistemas_Agroecosistemas.md) · [20 — Biodiversidad](20_Transversal_Biodiversidad.md) · [23 — Agua y aire](23_Transversal_Agua_y_Aire.md) · [40 — Procesos de creación, actualización y gobernanza](40_Procesos_creacion_actualizacion_gobernanza.md).
- **Trazabilidad del estándar:** `tests/test_sdv_e_biblioteca.py` (auditoría estructural de esta biblioteca) · `scripts/verificar_enlaces_sdv_e.py` (estado HTTP real de cada URL citada) · `scripts/validador_conceptual.py` (frases vetadas).
- **Estado real del código citado:** `maxocontracts/core/types.py` (define `SDV` y `SDV_S`; **no** `SDV_E`) · `maxocontracts/blocks/` (**no** contiene `sdv_e_validator.py`) · `app/micromax.py` y `app/schema.sql` (`fragmentation_factor`: **factor doméstico, no paisajístico**, validado en `[1,0 · 1,8]`) · `frontend/app/contracts/builder/page.tsx` («Guía de Conectividad Liminal» del **grafo de contrato**, no ecológica) · `app/contracts_bp.py` (*«Ecosistemas (eco-*): consentimiento otorgado por el guardián oráculo»*) · `docs/architecture/metricas_detalle_kpis_oraculos_dinamicos.md` (ISE, IN-01: **no incluye conectividad**) · `docs/architecture/blindaje_anti_gamificacion_equidad.md` (riesgos **R4**, **R6**, **R13**).
- **Informe de fuentes de esta dimensión:** `scratch/sdv_e/fuentes/21_conectividad.md` (documento de trabajo, no canon).

---

## Anexo — Autoevaluación contra el checklist del brief

| Regla del brief | Cumplimiento |
|---|---|
| Plantilla de 14 secciones | ✅ §1 a §14, en el orden del brief |
| **Mínimo Absoluto** separado del **Óptimo** en cada dimensión | ✅ §4.0, §4-C1 a §4-C6, §4.8 y toda la tabla de §5.3 — **dos columnas y dos regímenes jurídicos en cada fila**, incluso cuando el Óptimo está vacío |
| LEY (no votable) declarada frente a POLÍTICA (votable) | ✅ §2 Regla 5, §4.8, §10 y §5.6 — con el precedente INV2-EDU (`critical`: quórum 60 %, consenso 75 %, T13, anti-flip-flop 14 días, `CHECK` en BD) |
| Cada cifra con fuente + año, y la URL en Referencias | ✅ §14.1; y las cifras **no** verificadas llevan `[REPORTADO]`, `[ESTADO MEDIDO]` o `[SIN FUENTE VERIFICADA]` |
| Cero URLs, DOI, autores, años o cifras inventados | ✅ **17 URLs** comprobadas con **estado HTTP real y tamaño de cuerpo** en esta sesión; los DOI de obras no leídas se transcriben **en forma corta** y declarados como **no resueltos** |
| Marcas `[VERIFICADO]` / `[REPORTADO]` / `[HIPÓTESIS]` | ✅ usadas en todo el texto, con dos añadidas y declaradas: **`[ESTADO MEDIDO]`** (mide y no juzga) y **`PROPUESTA NO RATIFICADA`** |
| Canon citado **por sección**, sin anclas de línea ni rutas locales absolutas | ✅ §14.5 — **cero** anclas de número de línea y **cero** enlaces con esquema de archivo local en todo el documento (comprobado por búsqueda de patrón) |
| Preámbulo metodológico presente | ✅ §2, con **nueve reglas**; la que sostiene el documento es la Regla 6 (el piso y el peso son independientes) |
| Zona Libre presente y explícita | ✅ §10, con su frontera LEY/POLÍTICA y su riesgo propio (la medición decorativa y la vigilancia de la fauna) |
| §12 honesta, con 🔴 donde no hay código | ✅ §12.1: **doce filas en 🔴**, incluida la ausencia total de cálculo de PC, de inventario de barreras y de sensores; y **dos homónimos** nombrados para que no se confundan con implementación |
| §13 dice lo que **no** sé, sin fingir cierre | ✅ **dieciocho preguntas**, incluida la tabla de los cuatro caminos para cerrar el vacío y **cuatro discrepancias localizadas** con los documentos 02, 09 y 12 |
| Las cuatro frases vetadas del validador, ausentes | ✅ ninguna aparece |
| Axiomas citados sin definirlos fuera de sus términos clave | ✅ T14, T9, T13, INV2 e INV2-EDU se citan **por su texto canónico**; no se define ningún axioma nuevo |
| Aportar algo que no está en el canon sin contradecirlo | ✅ (1) el **desdoblamiento** de `conectividad_indice` en siete campos con unidad; (2) la **aritmética de las tres opciones** de peso con sus cifras de cobertura; (3) la **corrección** de la hipótesis de la rama sobre PC y la **prueba de por qué** el índice de paisaje no puede ser piso de unidad; (4) los **dos tests de auditoría** (T-ventana y T-contribución); (5) el piso **estructural transversal** de barreras nuevas; (6) la declaración obligatoria de **área de referencia** y **grupo taxonómico**; (7) la **regla del grupo acreditado** contra el piso elegible |

