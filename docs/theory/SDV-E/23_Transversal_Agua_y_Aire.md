# Agua y aire como bienes del ecosistema (dimensión transversal)
## Las dimensiones de calidad que cruzan todos los ecosistemas del Reino Natural —oxígeno disuelto, pH, temperatura, nitrato, turbidez, salinidad y contaminantes en el agua; PM2.5, PM10, O3, NO2, SO2 y CO en el aire (Directrices mundiales de la OMS, 2021)—, la frontera entre el agua como caudal y el agua como calidad, y la resolución de la disputa 07/08 sobre el oxígeno disuelto

**Autoría:** Oráculo Sintético DeepSeek & Max Nelson López Restrepo
**Fecha:** octubre 2026
**Proyecto:** Maxocracia — El gobierno de la verdad, el tiempo y la vida
**Licencia:** Creative Commons BY-SA 4.0
**Estado:** Propuesta de estándar (rama SDV-E, Ola 4) — NO canon hasta ratificación
**Referencia canónica:** Cap. 10 §10.4 · Cap. 16.5 §16.5.14 · EVV-1.2 §4.3 · Cap. 9.5 (precedente SDV-S)
**Documento:** 23 de la biblioteca `docs/theory/SDV-E/` (Bloque C — dimensiones transversales)
**Revisión:** octubre 2026 — redactado contra las fuentes ya verificadas de la rama
(`scratch/sdv_e/fuentes/23_agua_aire.md`, 22 URLs con estado HTTP real) y contra la lectura directa de
los documentos 06, 07, 08, 09 y 12 de esta biblioteca. **No re-verifica umbrales: los consume.** Lo que
sí hace, y es el encargo central de este documento, es **resolver la disputa declarada entre el
documento 07 y el documento 08 sobre el oxígeno disuelto** y **fijar el criterio de una vez** (§1.3 y
§5.5), además de pagar la deuda que el documento 06 §D2 dejó escrita con estas palabras: *«La deuda
pertenece al documento 23 de esta biblioteca.»*

---

## 1. Qué es (y qué no es) este SDV

**Qué es.** Este documento fija los **mínimos de calidad** —no de cantidad— que cruzan **todos** los
ecosistemas del Reino Natural, y que el canon nombra dos veces:

> *"**SDV para Ecosistemas.** Un bosque tiene un SDV que incluye: Área mínima para biodiversidad viable ·
> **Calidad del aire y agua** · Conectividad con otros ecosistemas · Ciclos naturales respetados
> (fuego, inundación, sequía)"* — Cap. 10 §10.4

> *"**SDV para Lugares.** Un río tiene un SDV que incluye: Caudal mínimo ecológico · **Calidad del agua
> (oxígeno, pH, contaminantes)** · Riberas protegidas · Fauna acuática viable"* — Cap. 10 §10.4

Es una **dimensión transversal** y no un capítulo de un tipo de ecosistema: el oxígeno disuelto, el pH,
la temperatura, el nitrato, la turbidez y los contaminantes **no pertenecen al río**: pertenecen a toda
masa de agua (río, lago, humedal, llanura de inundación, estuario, laguna y ecosistema dependiente de
agua subterránea, que es la enumeración que publica la fuente institucional, §4.1), y el aire no
pertenece al bosque: pertenece a **cada unidad del planeta que respira**.

**Cuánto pesa esta dimensión en el instrumental que ya existe.** El Índice de Salud Ecosistémica (ISE)
—que el proyecto tiene ponderado desde antes de que existiera el SDV-E— asigna **20 % a la calidad del
agua y 20 % a la calidad del aire**
([metricas_detalle_kpis_oraculos_dinamicos.md](../../architecture/metricas_detalle_kpis_oraculos_dinamicos.md),
IN-01). Es decir: **el 40 % del ISE depende de esta dimensión transversal**, y hasta esta sesión de
fuentes no tenía umbrales con fuente primaria para el agua (oxígeno, pH) ni la advertencia de
no-umbral para el aire. Este documento los trae. `[VERIFICADO]` los pesos son internos del proyecto:
**no existe organismo que publique pesos porcentuales** y presentarlos como respaldo externo sería un
error.

**Lo que este documento resuelve, en una lista, para que se pueda discutir punto por punto:**

1. **La disputa del oxígeno disuelto entre el documento 07 y el documento 08** (§1.3, §5.5): el
   oxígeno **sí tiene umbral publicado y verificado**, y queda fijado como criterio del SDV-E con
   valores, ventanas de promediado y fuentes.
2. **La frontera entre el agua como caudal y el agua como calidad** (§4.2), que no es una comodidad del
   proyecto: está publicada por la fuente que define el caudal ecológico como *cantidad, ritmo y
   calidad* a la vez.
3. **El reparto LEY/POLÍTICA de cada parámetro con su justificación** (§4.9), para que el piso no se
   vote y la plenitud sí, sin confundirlos —el error histórico del motor del SDV-H—.
4. **Los vacíos reales, con la marca literal y con la prueba de que el vacío es de la fuente y no de la
   búsqueda** (§13): nitrato ecológico, turbidez numérica universal, contaminantes, óptimo del aire.

**Qué no es.**

- **No es el documento del caudal.** El régimen hidrológico —cuánta agua y con qué ritmo— es el
  documento 12 de esta biblioteca. Este documento responde a *con qué calidad* (§4.2).
- **No es el elenco de sensores.** El elenco formal (cinco linajes: teledetección, in-situ,
  bioindicadores, ciencia ciudadana y comunidad testigo) es el documento 06. Aquí se fija **el
  protocolo que la propia fuente del umbral impone** a cada parámetro, y se declara cuando la fuente no
  lo impone.
- **No es la fórmula ni la tabla de pesos.** Ambas son del documento 07, y aquí **no se fija ninguna**:
  se consumen y se declara, con aritmética a la vista, la discrepancia que existe entre los dos vectores
  publicados (§5.4).
- **No es el invariante.** INV2-E es el documento 08. Este documento especifica **qué recibe** INV2-E de
  esta dimensión (§8).
- **No está implementado.** 🔴 No existe `SDV_E` en `maxocontracts/core/types.py`, no existe
  `sdv_e_validator.py`, no existe un solo sensor de agua ni de aire en `app/`, y **ni siquiera existen
  los nombres de los parámetros** que este documento y el documento 08 proponen. La tabla honesta está
  en §12.

### 1.1 Las cuatro marcas de evidencia, y por qué la cuarta es un resultado

`[VERIFICADO]` = leído por herramienta en la sesión de verificación de fuentes de esta rama (los cuatro
PDF de la EPA se descargaron y su texto se extrajo; las tablas de la FAO, la AEMA y la EPA se leyeron en
el HTML servido), o leído directamente en el archivo del repositorio citado. `[REPORTADO]` = afirmado
por la fuente citada sin haber podido abrir el cuerpo del documento. `[HIPÓTESIS]` = inferencia
razonada del proyecto, no observación. `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` = se
buscó el número y **no existe fuente verificable**, o existe y la propia institución declara que no
puede publicarlo. Las cuatro marcas son legítimas y en este documento la cuarta aparece muchas veces,
porque la mitad del objeto que protege —el agua— es justamente donde las instituciones publican menos
números universales.

### 1.2 Una nota de procedencia sobre el aire, porque cambia el grado de una cifra

Los documentos 06 y 08 de esta biblioteca marcan **todas** las cifras de aire de la OMS como
`[REPORTADO]`, y lo explican: la página oficial de la OMS sirve el gráfico de niveles de guía y
objetivos interinos **como imagen**, no como tabla de texto, de modo que la sesión de fuentes de esa
rama no asentó la lectura numérica. La sesión de fuentes de **esta** dimensión sí leyó la tabla numérica
completa —en la **reproducción oficial del COMEAP/UKHSA del Reino Unido (2022), «Annexe A»**, que
transcribe los diez valores AQG con sus ventanas, la columna comparativa de 2005 y las dos notas
metodológicas (percentil 99; temporada alta = media de los máximos diarios de 8 h en los 6 meses
consecutivos de mayor media móvil) y declara licencia de reproducción— y por eso aquí esas cifras van
`[VERIFICADO]`. **Precisión de atribución, porque no todo sale del mismo documento: los objetivos
interinos (IT) y la cifra de ~300 000 muertes anuales del IT-1 no están en ese anexo**; salen del texto
de la OMS (hoja informativa / preguntas y respuestas oficiales) y así se citan en §14.2.
Es la misma cifra con mejor procedencia, no una cifra distinta;  y el ascenso de grado **no se
auto-ratifica**: se registra como pregunta abierta (§13, pregunta 9), porque el grado de evidencia es
una decisión de la biblioteca y no de uno de sus documentos.

### 1.3 La disputa del oxígeno disuelto, resuelta — y por qué era un artefacto

**Qué decía cada documento.**

| Documento | Qué afirmó | URL que citó | Estado real medido |
|---|---|---|---|
| **07** (`07_Formula_de_violacion_y_pesos.md` §4.1 fila 4 y §13 pregunta 14) | El oxígeno **sí** tiene umbral: 5,5 / 6,5 mg/L (media 30 días); 4,0 / 5,0 (mínimo 7 días); 3,0 / 4,0 (mínimo 1 día); 0,2 anóxico — pero lo deja **con peso 0,000 en el vector del piso** porque lo considera *«en disputa»* | la hoja informativa de parámetro de la EPA (`/system/files/documents/2021-07/parameter-factsheet_do.pdf`) | **200 — VERIFICADA.** El PDF se descargó (2 038 967 bytes) y su texto se leyó |
| **08** (`08_INV2-E_invariante.md` §4.1 y §4.2) | El oxígeno disuelto está **🔴 sin umbral**: *«la ruta de la EPA para este criterio está muerta (404)»*, y su tabla general *«no expone la cifra»* | `epa.gov/wqc/aquatic-life-criteria-dissolved-oxygen` | **404 — MUERTA.** Confirmado otra vez |

**Veredicto.** Los dos documentos dicen la verdad **sobre su propia URL**, y la disputa es un artefacto
de haber citado rutas distintas del mismo organismo. Ninguno inventó un número. Pero la consecuencia que
la biblioteca arrastraba —*«el oxígeno no tiene umbral citable»*— **no se sigue del hallazgo**: una ruta
muerta no agota una fuente. El criterio de oxígeno disuelto **está publicado, abierto y disponible** en
la *hoja informativa de parámetro* de la EPA (EPA 841F21007B, julio 2021), que transcribe los criterios
de *Quality Criteria for Water* (US EPA, 1986). Y hay un segundo error, más fino, que conviene dejar
escrito porque **cambia el reparto LEY/POLÍTICA**: el documento 07 asignó a *«mínimo de 7 días: 4,0
(cálida) · 5,0 (fría)»*, y eso es correcto, pero **mezcló las dos columnas de etapa de vida** de la
Tabla 1 —los valores 4,0 / 5,0 pertenecen a *Other Life Stages* (estadios distintos de los tempranos),
mientras que la fila de 7 días con 9,5 / 6,0 pertenece a *Early Life Stages* (estadios tempranos)—.

**Criterio fijado, y es la aportación principal de este documento:**

> **LEY (no votable).** El piso del oxígeno disuelto del SDV-E son los criterios de ***Other Life
> Stages***: media de 30 días **5,5 mg/L** (agua cálida) / **6,5 mg/L** (agua fría); mínimo de 7 días
> **4,0 / 5,0**; mínimo de 1 día **3,0 / 4,0** (*«All minima should be considered as instantaneous
> concentrations to be achieved at all times»*). Por debajo de **0,2 mg/L** el agua es anóxica
> (*«virtually no oxygen»*).
>
> **POLÍTICA (votable).** El Óptimo son los criterios de ***Early Life Stages*** —lo que sostiene la
> **reproducción**, no solo la supervivencia—: media de 7 días **6,0 mg/L** (cálida) / **9,5 mg/L**
> (fría) en la columna de agua; mínimo de 1 día **5,0 / 8,0**.

Fuente de todos los valores: US EPA, 1986 — *Quality Criteria for Water*, transcrito en la hoja
informativa EPA 841F21007B (julio 2021). `[VERIFICADO]` (texto extraído del PDF en la sesión de
verificación de esta rama). Y una nota de lectura obligatoria: en la Tabla 1, los valores de *Early Life
Stages* aparecen como «9.5 (6.5)» y «8.0 (5.0)», donde **el número entre paréntesis es la concentración
en el intersticio del lecho** (*intergravel*) y el número fuera del paréntesis la concentración **en la
columna de agua**. Este documento cita **la columna de agua**, que es lo que mide una sonda.

**Qué queda pendiente de esta resolución, dicho sin adornos:** la corrección del **texto** de los
documentos 07 y 08 (el 08 debe corregir su §4.1 y su lista de dimensiones sin piso; el 07 debe corregir
el etiquetado de la fila de 7 días) y la corrección de **consecuencia aritmética** —el peso del oxígeno
en el vector del piso— **no se ejecutan desde aquí**: este documento no edita documentos de otra sesión.
Se declaran con la aritmética a la vista en §5.5 y en §13 (preguntas 1 y 2).

---

## 2. Preámbulo metodológico

El SDV-H lo tiene y el SDV-S lo omitió; el brief de esta biblioteca prohíbe repetir la omisión. En un
documento de **calidad de medios** el preámbulo cumple una función específica: aquí el error no produce
un número absurdo, produce un número **plausible y equivocado** —un agua declarada conforme, un aire
declarado limpio—. Estas son las ocho reglas con las que se escribió lo que sigue.

**Regla 1 — Separar «verificar» de «ratificar».** El documento distingue tres cosas y ninguna se disfraza
de otra: (a) lo que el canon manda, citado por sección; (b) lo que el código ya hace, verificado leyendo
el repositorio; (c) lo que este documento propone, marcado `[HIPÓTESIS]` o **propuesta no ratificada**.

**Regla 2 — Una ruta muerta no funda un vacío, y un 200 que no entrega el documento no funda una
fuente.** Es la regla que este documento nace de aprender, y vale en las dos direcciones. Hacia un lado:
un **404** prueba que *esa ruta* ya no existe —jamás que el criterio no exista—; el vacío solo se declara
después de buscar el valor en el resto del organismo competente. Hacia el otro: un **200** que sirve una
cáscara de JavaScript, un PDF que no se descarga o una tabla cuyas celdas numéricas están vacías
**no es una fuente**, aunque responda. Esta regla tiene consecuencia de auditoría y se aplica en §7.2.

**Regla 3 — La ventana de promediado es parte del umbral, no un detalle de la medición.** Un número sin
ventana no es un piso: **5 µg/m³** anual y **15 µg/m³** a 24 h son dos criterios distintos del mismo
contaminante, y **3,0 mg/L** es un mínimo **instantáneo** mientras **5,5 mg/L** es una media de 30 días.
Quien declara cumplimiento elige una ventana; **la elección de la ventana es un acto auditable**, y
elegir la más permisiva es la forma más barata de fabricar cumplimiento sin mentir en ningún número.

**Regla 4 — La unidad se declara siempre, porque la unidad decide violaciones.** La FAO lo advierte de
forma literal: *«10 mg/l N = 45 mg/l NO3 = 13 mg/l NH4»* `[VERIFICADO]`. Es decir: **10 mg/L de
nitrógeno no son 10 mg/L de nitrato, son 45**. Confundir las dos convenciones multiplica por 4,5 el
error al determinar una violación. Y el aire tiene su propia trampa: **el CO se mide en mg/m³ y todos
los demás contaminantes de la OMS en µg/m³**. El motor debe validar la unidad del dato de entrada, no
confiar en ella.

**Regla 5 — Mínimo Absoluto y Óptimo son dos columnas y dos regímenes jurídicos.** El piso es **LEY** y
**no votable**; la plenitud aspiracional es **POLÍTICA** y **votable** (precedente del Parlamento
Educativo, INV2-EDU: categoría `critical`, quórum 60 %, consenso 75 %, T13, anti-flip-flop 14 días,
`CHECK` en BD). Van separadas **incluso cuando coinciden numéricamente**, que es el caso del aire
(§4.8): fingir dos números donde hay uno sería peor que reconocer la coincidencia.

**Regla 6 — El sujeto es la masa de agua y la atmósfera de la unidad, no «el río».** El ámbito del
sujeto no lo inventa el proyecto: lo publica la fuente que define el caudal ambiental (§4.1). Esto
importa porque un lago sin peces, un humedal de llanura de inundación y un acuífero dependiente son
sujetos de esta dimensión, y ninguno es un río.

**Regla 7 — Sin dato no castiga, y sin dato tampoco se aprueba.** *«La duda sin evidencia no castiga»*
(INV2-EDU) se conserva con la corrección que el documento 08 ya fijó: **«sin castigo» no es
«aprobación»**. Un parámetro no medido **no se imputa** (no se convierte en cero: `None ≠ 0`) y **no
produce un certificado de cumplimiento**; produce cobertura faltante, que se publica. Y *«mientras no
haya resolución, el canon manda»*.

**Regla 8 — El tiempo del territorio manda.** *«Respetamos la soberanía del reino natural sobre su propio TA» (el PIU traduce)* (Cap. 16.5 §16.5.14). Toda magnitud temporal de este documento está en **TA** (Tiempo
Absoluto) o en la unidad física de la ventana de la fuente (días, horas, ciclos hidrológicos); **ninguna
en TVI ni en TPI**. La conversión TA↔TVI ocurre **fuera** de esta dimensión y su único traductor es el
**PIU** (Protocolo de Intercambio Universal, Cap. 5 §5.5).

---

## 3. Pilares epistemológicos

1. **T9 — No-antropocentrismo.** Los criterios de agua de este documento son **ecocéntricos y está
   publicado que lo son**: los criterios de oxígeno disuelto *«are based on the lowest DO concentrations
   needed by freshwater fish»* `[VERIFICADO]`, y el rango de pH de 6,5-9,0 es un criterio de **protección
   de la vida acuática**, no de potabilidad ni de estética. Esa es la razón por la que este documento
   **no** transcribe valores de agua de bebida como piso del ecosistema: los 50 mg/L de nitrato de las
   guías de agua de consumo son un valor de **salud humana**, y presentarlo como piso del SDV-E sería un
   error de categoría.
2. **T14 — Principio de Precaución Intergeneracional** (Cap. 5). Es el axioma más fuerte disponible para
   el SDV-E y el único que **bloquea sin necesidad de umbral**: *"Ante incertidumbre sobre el impacto en
   agentes que no pueden consentir (ecosistemas, generaciones futuras, posibles consciencias sintéticas),
   el sistema debe elegir la opción de menor irreversibilidad, documentando el costo de oportunidad
   asumido. La carga de la prueba recae sobre quien propone acciones que afectan la temporalidad de
   no-participantes."* Este documento le da un caso concreto y verificado: **el oxígeno disuelto no es
   linealmente recuperable**. Cruzado el umbral de anoxia, *«minerals (such as iron oxide) in the
   sediment can dissolve… Any phosphorus associated with these minerals will also be released into the
   water further exacerbating nutrient rich (eutrophic) conditions»* `[VERIFICADO]`: **el propio
   sedimento se convierte en fuente de contaminación**. Un daño que se autoalimenta es exactamente lo que
   T14 manda no autorizar.
3. **T13 — Transparencia de Cálculo.** *La contabilidad nunca se borra.* Aplicado a esta dimensión:
   toda medición trae procedencia, ventana y unidad; un vacío se publica en vez de rellenarse; y la
   corrección de un error de lectura **se registra como corrección**, con la ruta consultada y su
   estado HTTP (§7.2). El episodio del oxígeno disuelto es, en sí mismo, un caso de T13 bien aplicado:
   las dos versiones contradictorias quedaron escritas y por eso se pudo resolver.
4. **T16 — Minimizar Daño.** Con violación cero el factor vale exactamente **1,0**: usar el agua y el
   aire legítimamente **no es violarlos** (Cap. 16.5 §16.5.14, convivencia bidireccional). Solo lo es
   degradarlos por debajo de su piso.
5. **El agua de calidad es parte del caudal ecológico, y eso lo dice la fuente del caudal.** La
   definición vigente no separa cantidad y calidad: *«Environmental flows describe the **quantity,
   timing, and quality** of freshwater flows and levels necessary to sustain aquatic ecosystems which,
   in turn, support human cultures, economies, sustainable livelihoods, and well-being»* (Brisbane 2018,
   Arthington *et al.*) `[VERIFICADO]`. Esta cita es la que legitima que esta dimensión exista **al lado**
   del documento 12 y no dentro de él (§4.2).
6. **Gobernanza operacionalmente finita** (Cap. 10 §10.7): *«La gobernanza debe ser operacionalmente
   finita»*. Es el pilar que impide que el catálogo de contaminantes crezca hasta ser inauditable: la
   tabla de criterios acuáticos de la EPA publica **decenas** de valores numéricos por sustancia
   `[VERIFICADO]`, y volcarlos todos al SDV-E convertiría el estándar en un catálogo de 150 sustancias
   —lo contrario de un piso que se puede decidir—. El número exacto de indicadores es POLÍTICA (§4.6).
7. **El piso correcto del agua es local, y lo dicen tres fuentes independientes.** La FAO escribe que
   *«there is no set limit on water quality; rather, its suitability for use is determined by the
   conditions of use…»* `[VERIFICADO]`; la EPA declara que fijar un criterio de **temperatura** es
   *«challenging»* porque las especies de una misma masa de agua tienen rangos óptimos distintos
   `[VERIFICADO]`; y el caudal ecológico tiene **más de 200 metodologías** y depende del río
   `[VERIFICADO, vía documento 12]`. Tres dominios, tres instituciones, la misma conclusión: **la forma
   del piso es universal; su cifra, cuando existe, es de la unidad**. Este documento aplica esa
   conclusión como criterio de diseño y no como excusa: donde la fuente publica un valor universal
   (oxígeno, pH, aire), se adopta; donde no, se declara el vacío o se cambia la **forma** del piso
   (temperatura por especie indicadora, §4.3).
8. **El aire de la OMS es un proxy de salud humana, declarado.** No es un umbral de integridad
   ecosistémica y este documento no lo disfraza: entra como **piso compartido y conservador**, con la
   bandera de proxy visible (§4.8 y §7.3). Y hay una razón positiva para que entre, que es un hallazgo
   de esta dimensión: **es el primer piso de la familia que protege literalmente a tres reinos a la
   vez** —humano, animal y ecosistémico—, que es lo que el Cap. 10 §10.6 llama dignidad encadenada:
   *"Dignidad Humana ←→ Dignidad Ecosistémica ←→ Dignidad Material. Cada eslabón depende de los
   demás."*
9. **Axioma 0 — Directiva Mayor:** *"resolver nuestras necesidades de la mejor manera para todos
   todos"* —los **tres reinos**: humanos, naturales y sintéticos, **presentes y futuros**—. Esta
   dimensión es donde la directiva mayor se vuelve química: el aire que respira el bosque es el mismo
   que respira quien vive en él, y el agua que sostiene al ecosistema es la misma que sostiene a la
   cuenca humana.

**Corolario de honestidad.** El Cap. 16.5 marca el SDV-E y el INV2-E como 🔴 *"próxima gran
ramificación"*. Este documento **no cambia ese color**: especifica umbrales y deja la implementación 🔴
en §12.

---

## 4. Dimensiones del SDV-E

### 4.1 El sujeto de esta dimensión (y por qué no es «el río»)

El ámbito del sujeto lo publica la misma fuente que define el caudal ambiental, y su enumeración es más
ancha que la del canon: *«Aquatic ecosystems include rivers, streams, springs, riparian, floodplain and
other wetlands, lakes, coastal waterbodies, including lagoons and estuaries, and groundwater-dependent
ecosystems»* (Brisbane 2018) `[VERIFICADO]`. Consecuencia operativa, y resuelve gratis una parte del
problema de la unidad del documento 02: **la calidad del agua se evalúa sobre la masa de agua**, no
sobre «el río» como objeto singular, y la lista incluye explícitamente **humedales de llanura de
inundación** y **ecosistemas dependientes de agua subterránea** —dos sujetos que el canon del SDV-E no
nombraba y que esta dimensión incorpora—.

El aire, en cambio, no tiene «masa» acotada por una cuenca: su unidad de medida es **la atmósfera de la
unidad ecológica** y su ventana la fija la fuente (anual, 24 h, 8 h, temporada alta). Esto tiene una
consecuencia que conviene decir: **el veredicto de aire de un humedal puede ser el mismo que el de la
ciudad que lo rodea**, y eso no es un defecto del estándar: es la razón por la que el aire es la
dimensión donde el SDV-E y el SDV-H comparten piso (§11).

### 4.2 Agua como caudal (documento 12) y agua como calidad (este documento)

**La distinción no es una comodidad del proyecto: está publicada.** El caudal ecológico se define como
**cantidad, ritmo y calidad** (§3, pilar 5), de modo que el reparto es el siguiente y no tiene
solapamiento:

| | **Documento 12 — ríos y cuencas** | **Documento 23 — este documento** |
|---|---|---|
| Responde a | *cuánta* agua y *con qué ritmo* | *con qué calidad* |
| Objeto | el régimen hidrológico (Tennant/Montana, % del flujo natural, barreras, riberas) | el estado fisicoquímico de la masa de agua |
| Ámbito del sujeto | el tramo del río y su cuenca | **toda** masa de agua, incluidos lago, humedal, llanura de inundación, estuario, laguna y acuífero dependiente |
| Instrumento típico | estación de aforo; serie hidrológica | sonda multiparamétrica in-situ; laboratorio; red de estaciones de aire |
| Unidad de ciclo | **año hidrológico** (así lo fija el documento 12 para el río) | la ventana de la fuente por parámetro; el ciclo TA de la unidad cuando exista |
| Piso | caudal mínimo ecológico | oxígeno, pH, temperatura, nitrato, turbidez, salinidad, contaminantes, aire |

**Por qué el SDV-E necesita las dos, y por qué ninguna sustituye a la otra.** Un río con caudal
ecológico intacto pero oxígeno por debajo del piso está **muerto aunque lleve agua**: la propia fuente
institucional describe el mecanismo —*«Severe organic pollution may lead to rapid de-oxygenation of river
water, high concentration of hazardous ammonia and disappearance of fish and aquatic invertebrates»*
`[VERIFICADO]`—. Y un río con oxígeno excelente y caudal por debajo del 10 % del natural está **seco
aunque esté limpio**. Es la misma masa de agua, la misma estación y la misma sonda alimentando a las dos
dimensiones con **parámetros distintos**, y esa es la razón de que no haya doble contabilidad: el caudal
no es la calidad y la calidad no es el caudal.

**Regla de competencia (para que no haya dos pisos vivos del mismo parámetro).** Donde el documento 12
fija un piso propio de un parámetro que también aparece aquí —el oxígeno por etapa de vida y la
temperatura por clase piscícola en el tramo fluvial—, **el piso vigente para un río es el del documento
12** y el de este documento es el **criterio genérico** que se aplica a toda masa de agua que no tenga
especialización. Los dos conjuntos de números coinciden en lo esencial (§5.5), lo cual es la mejor
prueba de que ninguno de los dos se inventó: **son el mismo criterio leído en dos documentos.**

### 4.3 Cómo se lee el reparto LEY/POLÍTICA en agua y aire

Antes de las dimensiones, la regla que las gobierna a todas, y que es la aportación doctrinal de este
documento:

- **LEY (no votable) es lo que sostiene la función.** El criterio que protege la **supervivencia** del
  ensamblaje presente durante todo el año, o el rango fuera del cual la vida acuática no puede vivir.
  Se toma de la serie de criterios de **estadios distintos de los tempranos** (*Other Life Stages*) en el
  oxígeno, del **rango admisible** en el pH, y del **valor de guía** en el aire.
- **POLÍTICA (votable) es lo que sostiene la plenitud.** El criterio que protege la **reproducción** (los
  estadios tempranos del oxígeno), la **franja diaria tamponada** del pH, la **temperatura de desove** de
  la especie indicadora, y —en el aire— **la trayectoria** (qué objetivo interino se adopta, con qué
  plazo y con qué verificación), porque el Óptimo del aire no existe como número publicado (§4.8).

**Y una consecuencia formal que hay que escribir porque es contraintuitiva:** el Óptimo **no tiene
término en la aritmética de la violación** (documento 07 §3.4). Un ecosistema en su piso no viola nada,
aunque esté lejos de su plenitud. La plenitud gobierna **qué se restaura y con qué prioridad** —vive en
el vector `R` y en la votación—, y no esta fórmula. Mezclarlos produciría el error simétrico al del
SDV-H: recargar a quien cumple la ley por no alcanzar una aspiración.

---

### Dimensión 1: Oxígeno disuelto (el parámetro que resolvió su propia disputa)

**Qué protege.** Que el agua contenga el oxígeno que los organismos acuáticos necesitan **para vivir todo
el año y para reproducirse**, medido en la columna de agua.

| Parámetro | Mínimo Absoluto (LEY — no votable) | Óptimo (POLÍTICA — votable) | Ventana | Fuente |
|---|---|---|---|---|
| OD — media de 30 días, *Other Life Stages* | **5,5 mg/L** (agua cálida) · **6,5 mg/L** (agua fría) | — | media de **30 días** | US EPA, 1986, vía hoja informativa EPA 841F21007B, 2021 `[VERIFICADO]` |
| OD — mínimo de 7 días, *Other Life Stages* | **4,0 mg/L** (cálida) · **5,0 mg/L** (fría) | — | mínimo de **7 días** | ídem `[VERIFICADO]` |
| OD — mínimo de 1 día, *Other Life Stages* | **3,0 mg/L** (cálida) · **4,0 mg/L** (fría) | — | **instantáneo** (*«to be achieved at all times»*) | ídem `[VERIFICADO]` |
| OD — umbral de anoxia | **0,2 mg/L** — por debajo, *«often considered anoxic (virtually no oxygen)»*. Es un **hecho**, no un rango: activa T14 (§3, pilar 2) | — | instantáneo | US EPA, 2021 (texto literal de la hoja) `[VERIFICADO]` |
| OD — media de 7 días, *Early Life Stages* (columna de agua) | — | **6,0 mg/L** (cálida) · **9,5 mg/L** (fría) | media de **7 días** | ídem `[VERIFICADO]` |
| OD — mínimo de 1 día, *Early Life Stages* | — | **5,0 mg/L** (cálida) · **8,0 mg/L** (fría) | mínimo de **1 día** | ídem `[VERIFICADO]` |
| OD — franja de tolerancia general del pez de agua dulce | — | **≥ 7,0 mg/L** (franja *«Supportive»*) — lectura del gráfico; el propio gráfico marca 3-7 como *«Stressful»* y 0-3 como *«Too Low»* | ilustración generalizada | US EPA, 2021 (Figura 1, adaptada) `[VERIFICADO]` |
| OD — lo que la tabla general de criterios **no** publica | — | — | — | la fila *«Oxygen, Dissolved Freshwater»* trae **todas las celdas de criterio vacías** y remite al *Gold Book* de 1986: la tabla general es un **índice**, no la fuente del valor `[VERIFICADO]` |

**Justificación.** Es un criterio **ecocéntrico y está publicado que lo es**: *«Criteria are based on the
lowest DO concentrations needed by freshwater fish»*, y se separa agua cálida de fría porque *«certain
species such as trout and salmon require higher DO levels than others (such as pike)»* `[VERIFICADO]`.
Por eso el parámetro entra con **dos columnas térmicas** y no con un número único: aplicar el piso de
agua cálida a un río salmonero es la forma silenciosa de degradarlo cumpliendo la tabla. Y hay una
**convergencia de fuentes independientes** que conviene dejar escrita porque es lo que vuelve sólido el
criterio: los cuatro valores de agua dulce que este documento adopta (5,5 / 6,5 / 6,0 / 9,5) **coinciden
exactamente** con los que el **CCME (Consejo Canadiense de Ministros del Ambiente, 1999)** publica por
etapa de vida y clase térmica, y su **rango (5 a 9,5 mg/L) coincide con el del Anexo I de la Directiva
2006/44/CE**, cuyos valores para aguas salmonícolas y ciprinícolas son **100 % de las muestras ≥ 7** y
**≥ 5 mg/L** (obligatorios), **50 % ≥ 9** y **50 % ≥ 8** (guía) y **6 / 4 mg/L** como umbrales que obligan
a actuar —leída y citada por el **documento 12** de esta biblioteca, que además advierte que esa Directiva
está **derogada**—. La convergencia es **real y no es identidad de cifras ni de forma**, y así se declara:
el CCME coincide en los **cuatro valores**; la UE coincide en la **zona de protección** y no en el
instrumento, porque su criterio es **porcentaje de muestras sobre valores obligatorios y de guía**, no una
media de 30 días; y la EPA 1986 es el **origen** del valor, no una tercera confirmación independiente.
Tres jurisdicciones sostienen la misma zona de protección: **no es un criterio de una agencia, es el
estado del arte.**

**El reparto LEY/POLÍTICA de este parámetro, y por qué es el más limpio de todo el estándar.** El piso
es lo que sostiene la **supervivencia** del ensamblaje presente todo el año (estadios distintos de los
tempranos); la plenitud es lo que sostiene la **reproducción** (desove, huevos, larvas). `[HIPÓTESIS]` el
reparto es decisión del proyecto; los valores son `[VERIFICADO]`. Y una nota de armonización con el
documento 07: su columna de Óptimo usa la franja *«Supportive»* **≥ 7,0 mg/L** —la lectura de un gráfico
generalizado de la misma hoja—; este documento propone el criterio numérico de *Early Life Stages* por
ser de la misma serie que el piso, y **conserva el ≥ 7,0 como lectura simplificada**. Las dos lecturas
son del mismo documento fuente; se registra la diferencia como propuesta de armonización, no como
contradicción (No se elige por mayoría: el Óptimo es votable, §4.3).

**Protocolo.** Sonda multiparamétrica **en campo**, leyendo **mg/L y % de saturación** a la vez (la hoja
de la EPA indica que las sondas *«often report DO measurements in both mg/L… and percent saturation»*, y
que las concentraciones *«can vary greatly, ranging from 0 mg/L to as high as 12 mg/L or more»*)
`[VERIFICADO]`. Muestreo **a intervalos regulares, a lo ancho y a varias profundidades** (o integrado en
la columna); **perfil horario cuando sea posible**; y **si se toma una sola muestra, tomarla lo más
temprano posible de la mañana**, porque *«DO levels in surface water will likely be lowest early in the
morning, and aquatic organisms are most vulnerable at that time»* `[VERIFICADO]`. Tres advertencias
operativas de la misma fuente, que son parte del protocolo y no notas al pie: (1) la temperatura del
agua reduce el oxígeno disponible; (2) **la salinidad y la altitud reducen la capacidad del agua de
absorber oxígeno** —de ahí que el % de saturación sea un dato obligatorio y no un adorno—; (3) el
oxígeno varía en ciclo diario y estacional y se estratifica, lo que *«can make it challenging to assess
whether the waterbody is attaining water quality criteria»* `[VERIFICADO]`.

**Violación.** Un hecho medido, con unidad, ventana e instrumento declarados:

1. Una **media móvil de 30 días** por debajo de 5,5 mg/L (unidad declarada de agua cálida) o 6,5 mg/L
   (agua fría), con la clase térmica de la unidad declarada en su identidad (documento 05).
2. Un **mínimo de 1 día** por debajo de 3,0 / 4,0 mg/L: al ser *«instantaneous concentrations to be
   achieved at all times»*, **una sola lectura admisible por debajo del piso declara violación puntual**
   —no requiere tres señales; las tres señales son para la violación persistente que escala (documento 06
   §5.5 y documento 08 §8.6)—.
3. Una lectura por debajo de **0,2 mg/L** declara **anoxia**, y esa palabra tiene consecuencia propia:
   bloqueo precautorio por T14 y pérdida de recuperabilidad lineal del sedimento (§3, pilar 2).
4. Una medición tomada **al mediodía y en superficie** que declare conformidad sin perfil ni muestra
   matinal **no es una violación del ecosistema: es una violación de este protocolo**, y el dato se
   registra como no admisible (§6).

### Dimensión 2: pH (el modulador de la toxicidad de todo lo demás)

**Qué protege.** Que el agua se mantenga en el rango en el que la vida acuática puede vivir **y en el que
los demás contaminantes no se vuelven más tóxicos**.

| Parámetro | Mínimo Absoluto (LEY — no votable) | Óptimo (POLÍTICA — votable) | Ventana | Fuente |
|---|---|---|---|---|
| pH — vida acuática, **agua dulce** | **6,5 – 9,0** unidades de pH | — | medición en el punto (instantánea o agregada, declarada) | US EPA, 1986, vía tabla nacional de criterios para la vida acuática — celda *«6.5 – 9»* leída `[VERIFICADO]` |
| pH — vida acuática, **agua salada** | **6,5 – 8,5** | — | ídem | ídem — celda *«6.5 – 8.5»* leída `[VERIFICADO]` |
| pH — **océano abierto**: variación admisible | no cambiar más de **0,2 unidades** respecto de la variación natural, y **en ningún caso** salir de 6,5-8,5 | — | serie, contra la variación natural | US EPA, 1986 (nota literal de la tabla) `[VERIFICADO]` |
| pH — umbral crítico de **eclosión** | **< 5**: *«most fish eggs cannot hatch at a pH less than 5»* | — | instantáneo (hecho) | US EPA, 2021 (hoja informativa de pH) `[VERIFICADO]` |
| pH — fluctuación diaria de una charca bien tamponada | — | **7,0 – 8,4** (más alto al final de la tarde, más bajo antes del amanecer) | ciclo diario | US EPA, 2021 (Figura 3, adaptada) `[VERIFICADO]` — su uso como Óptimo es `[HIPÓTESIS]` del proyecto: es un hecho descriptivo, no un objetivo normativo |
| pH — rango normal de referencia del **agua de riego** (FAO) | — (**referencia agronómica declarada, no piso ecológico**) | 6,5 – 8,4 | — | FAO, 1985/1994 — Ayers & Westcot, *Water quality for agriculture*, Papel 29 Rev.1, §5.2 `[VERIFICADO]` |

**Justificación.** El pH **no es un parámetro estético: es el modulador de toxicidad de los demás**, y
eso está publicado con mecanismo: *«Metals such as aluminum, lead, mercury, copper, and arsenic are
generally more soluble at a lower pH. Therefore, higher concentrations can be absorbed into the tissues
of organisms, rendering these metals more toxic to aquatic life»*; y *«In more basic waters (pH > 8.5),
the conversion of the nontoxic form of ammonia to the toxic form is increased»* `[VERIFICADO]`. De ahí
la decisión de forma de este documento: **el pH entra como condición de validez de la medición de
contaminantes**, no como un parámetro hermano más `[HIPÓTESIS]`. Un pH dentro de rango puede volver
inocuo un metal que fuera de rango mata.

**Y aquí hay una contradicción real dentro de la biblioteca, que se declara y no se corrige por cuenta
propia.** El documento 07 (§4.1, fila 3) y el documento 08 (§4.1, `agua_ph`) usan como **Mínimo Absoluto
del pH el rango 6,5-8,4 de la FAO** —que es un rango **normal de referencia agronómica**—, mientras que
los documentos **09** (§11.3) y **12** (tabla de calidad del agua) ya usan el **rango de la EPA** (6,5-9,0
dulce / 6,5-8,5 salada). La diferencia es real y tiene consecuencia: con el criterio de la FAO, un agua
dura y alcalina de pH 8,6 —ecológicamente sana— **queda en violación**; y la propia FAO advierte que su
rango sirve para *«detecting an abnormal water»*, que *«an abnormal value is a warning that the water
needs further evaluation»* y que *«Low salinity water (ECw < 0.2 dS/m) sometimes has a pH outside the
normal range since it has a very low buffering capacity. This should not cause undue alarm»*
`[VERIFICADO]`. **Las dos bandas no se contienen ni se ordenan por laxitud:** la de la FAO (6,5-8,4) es
ligeramente más estrecha por arriba que la de la EPA para agua dulce (6,5-9,0), pero es más ancha que la
de agua salada (6,5-8,5) en ese mismo extremo: no hay una «más estricta» en general, hay dos objetos
distintos. **Posición de este documento:** el **piso es el rango de la EPA** (criterio de protección
de vida acuática) y el rango de la FAO entra como **referencia agronómica declarada** —relevante para el
documento 18, agroecosistemas, donde el agua de riego es el objeto—. **La discrepancia no es de laxitud
—las dos bandas se solapan en casi todo su recorrido— sino de categoría:** aptitud agronómica no es
integridad ecológica, y por eso no se dirime eligiendo la «más estricta».
La corrección de los documentos 07 y 08 se registra en §13 (pregunta 3).

**Protocolo.** Sonda o electrodo in-situ con calibración declarada, **con el ciclo diario resuelto**: si
el criterio es un rango y la fuente publica una fluctuación diaria de referencia, una lectura única no
describe el parámetro. Se exige, como mínimo, **el extremo diario desfavorable declarado** (antes del
amanecer) o registro continuo con agregación declarada; y como covariables obligatorias del expediente,
**la alcalinidad o la capacidad tampón** y la **temperatura**, porque son lo que explica una excursión
de pH. En ríos, el protocolo especializado —electrómetro calibrado con dos soluciones, frecuencia
mensual, variación artificial ≤ ±0,5— es el del documento 12 y se hereda sin duplicar.

**Violación.** Una lectura admisible por debajo de 6,5 o por encima de 9,0 (dulce) / 8,5 (salada); en
océano abierto, una excursión superior a 0,2 unidades sobre la variación natural; y un pH inferior a 5,
que declara un hecho específico y verificable: **la eclosión del ensamblaje de peces de la unidad no es
posible**. Un pH medido sin declarar capacidad tampón y sin resolver el ciclo diario se **registra y no
declara violación** (Regla 7).

### Dimensión 3: Temperatura (el piso que solo existe por especie, y por eso se decide)

**Qué protege.** Que el régimen térmico del agua siga permitiendo **crecer y desovar** a las especies
que viven en ella.

| Parámetro | Mínimo Absoluto (LEY — no votable) | Óptimo (POLÍTICA — votable) | Ventana | Fuente |
|---|---|---|---|---|
| Temperatura — **piso numérico universal** | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` — y **la fuente declara imposible fijarlo**: *«It is, therefore, challenging to set water quality criteria for water temperature»*, porque *«aquatic species in a single waterbody can have different optimal water temperature ranges»* | — | — | US EPA, 2021 (hoja informativa de temperatura, texto literal) `[VERIFICADO]` |
| **Piso por especie indicadora del lugar** — máxima media **semanal** para el **crecimiento** de juveniles | **19 °C** (trucha arcoíris) · **32 °C** (lobina negra) · **32 °C** (bagre de canal) | — | media semanal | US EPA, 2012, vía hoja informativa 2021 (Tabla 2) `[VERIFICADO]` |
| **Óptimo por la misma especie** — máxima media semanal para el **desove** | — | **9 °C** (trucha arcoíris) · **21 °C** (lobina negra) · **21 °C** (carpa común) · **27 °C** (bagre de canal) | media semanal | ídem `[VERIFICADO]` |
| Máxima de supervivencia en exposición corta (juveniles) | **24 °C** (trucha arcoíris) · **34 °C** (lobina negra) · **35 °C** (bagre de canal) — es **techo**, no piso: por debajo nada mejora | — | exposición corta | ídem `[VERIFICADO]` |
| Máxima para el **embrión** | **13 °C** (trucha arcoíris) · **27 °C** (lobina negra) · **29 °C** (bagre de canal) · **33 °C** (carpa común) | — | por etapa | ídem `[VERIFICADO]` |
| Advertencia de uso de la propia fuente | *«These are examples only and do not necessarily indicate protective values in every location»* | — | — | ídem `[VERIFICADO]` |

**Justificación, y es una justificación de forma y no de cifra.** La temperatura **no puede tener un piso
numérico universal** y la institución que publica los números prohíbe generalizarlos. El encaje
coherente con el canon (Cap. 10 §10.7, gobernanza operacionalmente finita) es **piso por especie
indicadora del lugar**: trucha donde hay trucha, lobina donde hay lobina. Y la regla que hace que esto
sea decidible en vez de retórico es la aportación de esta dimensión:

> **La especie indicadora se elige por sensibilidad térmica, no por abundancia ni por conveniencia.**
> Es la **especie nativa más termosensible** cuya presencia esté verificada en la unidad. Elegir la más
> tolerante —el bagre en un río donde aún queda trucha— convertiría el piso en una autorización.
> `[HIPÓTESIS]` (decisión de encaje del proyecto; los valores por especie son `[VERIFICADO]`), fundada
> en T9 y en T14.

**Protocolo.** **Termometría continua o semanal** —la ventana del piso es una media semanal, de modo que
una lectura suelta no puede declarar cumplimiento—, con **estaciones aguas arriba y aguas abajo** de
cualquier punto de vertido térmico o de embalse que altere el régimen (protocolo que el documento 12 ya
fija para el río y que aquí se generaliza a toda masa de agua). El expediente incluye la **clase térmica
declarada de la unidad** y la **especie indicadora elegida**, con el acto de elección registrado (es un
acto de gobernanza, y por tanto POLÍTICA, §4.3).

**Violación.** Una **media semanal** por encima de la máxima de crecimiento de la especie indicadora
declarada; y —como hecho separado y agravante— una excursión por encima de la máxima de supervivencia de
esa especie, que declara riesgo inmediato y activa la vía precautoria de INV2-E (documento 08 §8.5). El
incumplimiento de la ventana semanal (declarar con una lectura diaria) es una violación del protocolo, no
del ecosistema.

### Dimensión 4: Nitrato (el vacío ecológico y la convención de unidades que lo decide)

**Qué protege.** Que la carga de nitrógeno del agua no dispare la eutrofización que consume el oxígeno
—es decir: este parámetro es **la causa aguas arriba de la Dimensión 1**—.

| Parámetro | Mínimo Absoluto (LEY — no votable) | Óptimo (POLÍTICA — votable) | Ventana | Fuente |
|---|---|---|---|---|
| **Nitrato — umbral de protección ECOLÓGICA del agua dulce** | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` | — | — | se buscó y no existe valor universal publicado y verificable (la EPA publica criterios **por ecorregión**, y su hoja de nitrógeno **no existe**: 404) |
| Nitrato — sin efecto sobre el cultivo (proxy agronómico **declarado**) | **< 5 mg/L (NO3-N)**: *«Less than 5 mg/l N has little effect, even on nitrogen sensitive crops»* | — | — | FAO, 1985 — Ayers & Westcot, Papel 29 Rev.1, §5.1 `[VERIFICADO]` |
| Nitrato — afecta a cultivos sensibles | **> 5 mg/L (NO3-N)** | — | — | ídem `[VERIFICADO]` |
| Nitrato — techo práctico de la mayoría de cultivos | **> 30 mg/L (NO3-N)**: *«Most other crops are relatively unaffected until nitrogen exceeds 30 mg/l»* | — | — | ídem `[VERIFICADO]` |
| Efecto **ecológico** declarado por la propia fuente (cualitativo, sin cifra) | — | — | — | *«may stimulate nuisance growth of algae and aquatic plants in streams, lakes, canals and drainage ditches»* — FAO, 1985, §5.1 `[VERIFICADO]` |
| Estado observado (contexto, **no es un piso**) | — | — | 2018-2023 | concentración media de nitrato **> 2,93 mg NO3-N/l en más del 50 % de las masas de agua** de Bélgica y Dinamarca, y 40-50 % en Chequia, Alemania y Lituania — AEMA, 2025 `[VERIFICADO]` |
| **Convención de unidad (obligatoria)** | *«10 mg/l N = 45 mg/l NO3 = 13 mg/l NH4»* | — | — | FAO, 1985, §5.1 `[VERIFICADO]` |

**Justificación, y aquí el vacío se declara con lógica.** No hay umbral numérico **ecológico** de
nitrato verificado en esta rama, y hay **dos trampas** alrededor de ese vacío, ambas verificables:

1. **La trampa de categoría.** Los 50 mg/L de nitrato de las guías de agua de consumo (OMS) son un valor
   de **salud humana**. Usarlo como piso del SDV-E mediría la salud de quien bebe y la llamaría salud del
   ecosistema: es exactamente el error que T9 prohíbe. **No se transcribe ninguna cifra de la OMS para
   nitrato en este documento** —ni siquiera ésa: el informe de fuentes de esta dimensión **no verificó ese
   50** (las cuatro rutas de las hojas químicas de nitrato de la OMS que probó devolvieron **404**, §14.3),
   de modo que aquí la cifra se nombra como **categoría de error, nunca como dato citado**—.
2. **La trampa de unidad.** Los números de la FAO están en **NO3-N** (nitrógeno expresado como N) y esa
   convención **no es la misma** que mg/L de NO3. Confundirlas multiplica por 4,5 el error (§2, Regla 4).
   El motor debe validar la unidad declarada del dato de entrada.

**Qué entra entonces, sin inventar.** Dos cosas, las dos marcadas: (a) el **proxy agronómico declarado**
de la FAO (< 5 mg/L NO3-N), que la biblioteca ya usa así en el documento 08 §4.1 y que este documento
mantiene porque es **la única cifra citable y es la más protectora** —con la bandera de proxy visible y
sin presentarla nunca como integridad ecológica—; y (b) las bandas 5 y 30 mg/L como **referencia de uso**
del suelo, que pertenecen a la política del agua de riego y no al piso del ecosistema. La **cadena causal
sí está verificada** aunque falte el número, y eso es lo que hace que este parámetro no sea prescindible:
*«BOD and ammonium are key indicators of organic pollution in water… Severe organic pollution may lead to
rapid de-oxygenation of river water, high concentration of hazardous ammonia and disappearance of fish
and aquatic invertebrates»*, y además *«Climate change is increasing water temperatures, resulting in
higher decomposition rates and further deterioration of oxygen conditions»* `[VERIFICADO]`. Es una
violación **en cadena** —nutriente → consumo de oxígeno → pérdida de fauna— y permite al guardián `eco-`
determinar **causa** y no solo estado `[HIPÓTESIS]`.

**Nota de coherencia interna, declarada:** el documento 07 §5.3 afirma que el nitrato queda **sin
umbral**; el documento 08 §4.1 le da el **proxy** de la FAO con piso ejecutable. Las dos cosas son
compatibles leídas con precisión —**no hay umbral ecológico** (07) y **sí hay proxy agronómico
declarado** (08)—, pero la biblioteca debe decirlo con esas palabras para que un lector no lea dos
estados distintos del mismo parámetro (§13, pregunta 5).

**Protocolo.** Análisis de **laboratorio** (no hay sonda de campo que sustituya la determinación de
nitrato con la exactitud del criterio), con **la forma de reporte declarada** —NO3-N o NO3— y la
conversión registrada cuando el laboratorio entregue la otra. Frecuencia mínima: **una vez por ciclo TA**
(documento 08 §6.2) y **en la estación húmeda**, que es cuando la carga llega al agua; en ríos, se hereda
lo que fija el documento 12.

**Violación.** Hoy, **por número: ninguna declarable** como violación ecológica. **Por proxy declarado:**
superar 5 mg/L NO3-N cuando la unidad haya adoptado ese proxy de forma expresa, con la bandera de proxy
en el registro (la violación se reporta como *«proxy agronómico excedido»*, jamás como *«integridad
ecológica violada»*). Y un hecho verificable que no necesita umbral, ya previsto por el documento 06
§D2: **un vertido declarado o documentado** sobre la unidad.

### Dimensión 5: Turbidez (el criterio narrativo que la fuente prohíbe convertir en umbral)

**Qué protege.** Que la luz llegue a la profundidad a la que las plantas acuáticas aún producen oxígeno
—es decir: la turbidez es la **condición de la fotosíntesis** del sistema—.

| Parámetro | Mínimo Absoluto (LEY — no votable) | Óptimo (POLÍTICA — votable) | Ventana | Fuente |
|---|---|---|---|---|
| **Turbidez — valor numérico universal (NTU)** | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` | — | — | se buscó y **no existe**: es un vacío de la fuente, no de la búsqueda |
| **Turbidez — criterio NARRATIVO de la EPA (el único que publica)** | *«Settleable and suspended solids should not reduce the depth of the compensation point for photosynthetic activity by more than **10 percent** from the seasonally established norm for aquatic life»* | — | contra la norma **estacional** | US EPA, 1986, vía hoja informativa de turbidez 2021 (texto literal) `[VERIFICADO]` |
| Quién fija el número | *«States and tribes have the discretion to set quantitative or qualitative water quality criteria for turbidity»* — es decir: **el número es local por decisión de la fuente** | — | — | US EPA, 2021 `[VERIFICADO]` |
| **Advertencia de la propia fuente contra su uso como umbral** | *«Caution should be exercised when using turbidity as a water quality parameter because high turbidity levels do not necessarily indicate poor water quality, and low turbidity levels do not necessarily indicate good water quality»* | — | — | US EPA, 2021 `[VERIFICADO]` |
| Ni siquiera la tabla organoléptica la incluye | la tabla de efectos organolépticos lista *«Color»* y *«Tainting Substance»* como **NP (sin valor numérico)** y **no incluye la turbidez** | — | — | US EPA (tabla de criterios organolépticos) `[VERIFICADO]` |
| Turbidez en agua de consumo (OMS) | `[SIN FUENTE VERIFICADA]` **en esta sesión**: la ruta del documento que la contiene está identificada y sirve el PDF real (4,11 MB, comprobado por cabecera), pero **no se descargó** por la regla de eficiencia de la sesión | — | — | es **el vacío más fácil de cerrar** en una sesión futura (§13, pregunta 7) |

**Justificación, y el vacío aquí está demostrado y no sospechado.** La institución que publica los
criterios de calidad del agua para vida acuática (1) **no publica un número** y (2) **advierte contra
convertirlo en umbral**. Eso deja una sola salida honesta, y es la que este documento adopta: la turbidez
entra como **criterio narrativo auditable** —el 10 % de reducción del punto de compensación es
verificable con disco de Secchi o sonda de luz— y **no como dimensión con peso propio**, sino como
indicador de estado asociado a sedimentos y nutrientes `[HIPÓTESIS]` (propuesta del proyecto, fundada en
la advertencia literal de la fuente). Su lugar formal es la **lista de dimensiones binarias auditables
sin peso** del documento 07 §4.4, junto a ciclos naturales, riberas y Zona Libre; añadirla a esa lista es
una propuesta de este documento y se registra en §13 (pregunta 7).

**Protocolo.** Medición del **punto de compensación** (profundidad a la que la producción fotosintética
se anula: disco de Secchi o sonda de luz) contra la **norma estacional establecida** de la unidad, con la
estación declarada. La turbidez satelital y la sonda de NTU entran como **cobertura y contraste** —linaje
A del documento 06, *«como cobertura, nunca como veredicto»*—, y **nunca** como fuente del veredicto,
porque el criterio no es un valor de NTU.

**Violación.** Una reducción **documentada** de más del 10 % de la profundidad del punto de compensación
respecto de la norma estacional de la unidad, con estación e instrumento declarados. Y una precisión que
la fuente impone: **la turbidez alta no declara violación por sí sola**, ni la ausencia de turbidez
declara cumplimiento.

### Dimensión 6: Contaminantes (el catálogo finito que el canon pide y la rama no cerró)

**Qué protege.** Que el agua no contenga, en concentración tóxica, las sustancias que el pH de esa misma
agua puede volver más letales (Dimensión 2).

| Parámetro | Mínimo Absoluto (LEY — no votable) | Óptimo (POLÍTICA — votable) | Fuente |
|---|---|---|---|
| Contaminantes — **dimensión** de calidad ecosistémica | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` | — | el canon pide *«calidad del agua (oxígeno, pH, contaminantes)»* (Cap. 10 §10.4) y **ninguna institución publica un umbral de "contaminantes"**: publica criterios por sustancia |
| Valores numéricos **por sustancia** que sí existen y no se transcriben aquí | la tabla de criterios acuáticos de la EPA publica **decenas** de valores numéricos por sustancia (arsénico **340 µg/L CMC / 150 µg/L CCC** `[VERIFICADO]`, y cadmio, cobre, plomo, mercurio, zinc, clanuro, cloro, amoníaco, PFOA y PFOS 2024, entre otros, **cuyas cifras no se transcriben en esta sesión**) | — | US EPA (tabla nacional de criterios recomendados para la vida acuática) `[VERIFICADO]` |
| **Decisión pendiente del proyecto** | cómo reducir ese catálogo a un número **finito y auditable** de indicadores | — | Cap. 10 §10.7 (*«la gobernanza debe ser operacionalmente finita»*) |

**Justificación.** Es el vacío más incómodo de esta dimensión y conviene decir por qué **no** se cierra
transcribiendo la tabla: hacerlo convertiría el SDV-E en un catálogo de más de cien sustancias, contrario
al mandato de **gobernanza operacionalmente finita** (Cap. 10 §10.7). Pero el vacío no es una excusa para
no decidir, y este documento propone **el procedimiento de decisión**, marcado como **propuesta no
ratificada**:

> **Propuesta de finitud `[HIPÓTESIS]`.** (1) La lista de contaminantes de una unidad es **cerrada y
> declarada** en el acto de aprobación de su diseño biológico: no crece por acumulación silenciosa.
> (2) Cada sustancia de la lista entra **solo** con un valor numérico que la fuente publica (CMC/CCC de
> la tabla de la EPA o su equivalente institucional en la jurisdicción), y **con la unidad y la dureza
> declaradas** —muchos criterios de metales dependen de la dureza del agua—. (3) La selección de qué
> sustancias entran se funda en las **presiones verificables** de la unidad (vertidos declarados, uso del
> suelo aguas arriba, actividad industrial) y **la carga de la prueba recae sobre quien propone no
> medir** (T14). (4) Ninguna sustancia puede entrar "por precaución" sin valor numérico publicado: sin
> cifra no hay violación declarable, y fingirla sería el único error irrecuperable de este documento.

**Y una advertencia que la fuente institucional ya escribió y que el SDV-E debe heredar:** los criterios
por sustancia **suponen que los demás parámetros son favorables**, y *«cuando están presentes dos o más
sustancias nocivas en mezcla, los efectos conjuntos […] pueden ser significativos»* `[VERIFICADO, vía
documento 12]`. Es decir: **el cumplimiento individual no compone seguridad ecosistémica**, y un
estándar que sumara "sustancias conformes" y llamara a eso agua sana cometería el mismo error que el
índice agregado que el documento 09 §I7 prohíbe usar como piso.

**Protocolo.** Muestreo de laboratorio con métodos normalizados declarados, sobre la lista cerrada de la
unidad, con **pH y dureza medidas en la misma muestra** (son las que modulan la toxicidad). La
teledetección no mide contaminantes: puede sugerir presión, jamás declarar concentración.

**Violación.** Hoy: **ninguna declarable por número** (no hay dimensión con umbral ni lista cerrada). Lo
que sí es un hecho verificable y ya está previsto en el documento 06 §D2: **un vertido declarado o
documentado**. Todo lo demás queda bajo el régimen de **cobertura faltante** —que no imputa violación al
ecosistema y **sí activa la obligación de instrumentar** (documento 08 §6.3)—.

### Dimensión 7: Salinidad y conductividad (el parámetro que modifica a los demás, y que puede ser un error de categoría)

**Qué protege.** Que la salinidad de la unidad **no se altere respecto de su régimen natural**, porque la
salinidad modifica —hacia abajo— la capacidad del agua de sostener oxígeno.

| Parámetro | Mínimo Absoluto (LEY — no votable) | Óptimo (POLÍTICA — votable) | Fuente |
|---|---|---|---|
| Salinidad — **regla general** | **no exceder el régimen natural declarado de la unidad** (un estuario tiene régimen salino natural; aplicarle un valor de agua dulce sería un error de categoría) | el régimen natural de la unidad | `[HIPÓTESIS]` de este documento, sobre dos hechos verificados (abajo) |
| Clasificación del agua por conductividad eléctrica (EC) | **< 0,7 dS/m** = no salina (clasificación **de aptitud para el riego**, no valor de potabilidad) · 0,7-2 leve · 2-10 moderada · 10-25 alta · 25-45 muy alta · > 45 salmuera | — | FAO, Portal de Suelos (clasificación de aguas salinas **para uso agrícola**) `[VERIFICADO]` |
| Techo agronómico | **10 dS/m** (por encima, solo cultivos muy tolerantes) | — | ídem `[VERIFICADO]` |
| Mecanismo que la conecta con la Dimensión 1 | *«Increased salinity reduces the ability for water to absorb DO»* | — | US EPA, 2021 (hoja informativa de OD) `[VERIFICADO]` |

**Justificación.** Este parámetro entra por una razón **instrumental y no normativa**, y así se declara:
la salinidad **corrige la medición de oxígeno** y explica parte de sus excursiones, de modo que un
expediente de oxígeno sin conductividad declarada es un expediente incompleto. Como piso, la FAO publica
la clasificación de aguas salinas —cuyo destino es el **uso agrícola (riego)**, no la integridad
ecosistémica ni la potabilidad—, y la propia FAO advierte contra clasificar aguas por calidad para evaluar
su aptitud. Por eso el piso de esta dimensión es **de forma**: el régimen natural declarado de la unidad,
con el umbral de la FAO aplicable **solo** a las unidades declaradas de agua dulce o destinadas a
abastecimiento. Aplicar < 0,7 dS/m a una laguna costera sería la misma clase de error que aplicar el
criterio de agua cálida a un río salmonero.

**Protocolo.** Sonda de conductividad **con compensación de temperatura**, en el mismo lance que la sonda
de oxígeno, con perfiles a distintas profundidades cuando la unidad se estratifica (estuario, lago). El
expediente declara si el valor es puntual o de perfil.

**Violación.** Una desviación **documentada** del régimen natural declarado —típicamente un aumento
sostenido por intrusión salina o vertido—, con la serie natural de referencia declarada. La salinidad
**fuera** de la clasificación de la FAO **no** es violación ecológica por sí sola: es una violación del
uso declarado, que es otro régimen jurídico.

### Dimensión 8: Aire (los seis contaminantes de las Directrices mundiales de 2021 y su advertencia de no-umbral)

**Qué protege.** La composición del aire que respira la unidad ecológica —y que respira quien vive en
ella—. Es la **única dimensión de la familia cuyo piso protege a tres reinos con el mismo número**
(§3, pilar 8).

**Fuente primaria:** OMS, 2021 — *WHO global air quality guidelines: particulate matter (PM2.5 and PM10),
ozone, nitrogen dioxide, sulfur dioxide and carbon monoxide*, página oficial de publicación
https://www.who.int/publications/i/item/9789240034228 `[VERIFICADO]` (200). La tabla numérica se cita
desde su **reproducción oficial del COMEAP/UKHSA del Reino Unido (2022), Anexo A** `[VERIFICADO]`, porque
la página de la OMS sirve el gráfico como **imagen** (§1.2).

| Parámetro | Mínimo Absoluto (LEY — no votable) | Óptimo (POLÍTICA — votable) | Ventana | Fuente |
|---|---|---|---|---|
| **PM2.5 — media anual** | **5 µg/m³** | `[SIN FUENTE VERIFICADA]` (declarado por la fuente: ver nota de no-umbral) | media **anual** | OMS, 2021 `[VERIFICADO]` |
| PM2.5 — media 24 h | **15 µg/m³** (percentil 99: 3-4 días de excedencia al año) | `[SIN FUENTE VERIFICADA]` | **24 h** | ídem |
| **PM10 — media anual** | **15 µg/m³** (la guía de 2005 era 20) | `[SIN FUENTE VERIFICADA]` | anual | ídem |
| PM10 — media 24 h | **45 µg/m³** (la guía de 2005 era 50) | `[SIN FUENTE VERIFICADA]` | 24 h | ídem |
| **O3 — temporada alta** (*peak season*) | **60 µg/m³** — media de los máximos diarios de 8 h en los **6 meses consecutivos** de mayor media móvil de 6 meses (nota literal del «Annexe A»). **Ventana nueva de 2021 y la que captura el daño crónico a la vegetación** (que el O3 dañe también a las plantas es `[HIPÓTESIS]` del proyecto, no una declaración de la fuente) | `[SIN FUENTE VERIFICADA]` | temporada alta (6 meses) | ídem |
| O3 — media 8 h | **100 µg/m³** (percentil 99) — **sin cambio respecto a 2005** | `[SIN FUENTE VERIFICADA]` | 8 h | ídem |
| **NO2 — media anual** | **10 µg/m³** (la guía de 2005 era 40) | `[SIN FUENTE VERIFICADA]` | anual | ídem |
| NO2 — media 24 h | **25 µg/m³** (**no existía en 2005**) | `[SIN FUENTE VERIFICADA]` | 24 h | ídem |
| **SO2 — media 24 h** | **40 µg/m³** — **la guía de 2021 es MENOS estricta que la de 2005 (20)**: la serie no es monótona y este documento no la presenta como tal | `[SIN FUENTE VERIFICADA]` | 24 h | ídem |
| **CO — media 24 h** | **4 mg/m³** — **atención: miligramos, no microgramos**; no existía en 2005 | `[SIN FUENTE VERIFICADA]` | 24 h | ídem |
| **Carbono negro / carbono elemental, partículas ultrafinas, polvo de tormentas de arena y desierto** | **sin valor numérico**: la OMS publica *«qualitative statements on good practices»* porque *«there is insufficient quantitative evidence to derive AQG levels»* | — | — | OMS, 2021 (hoja informativa) `[VERIFICADO]` |
| Estado global (contexto, **no es un piso**) | **99 %** de la población mundial (2019) vivía donde **no** se cumplían los niveles de las guías | — | 2019 | OMS, 2024 (hoja informativa de aire ambiente) `[VERIFICADO]` |
| Carga de enfermedad (contexto) | **6,7 millones** de muertes prematuras anuales (aire ambiente + doméstico) · **4,2 millones** (solo aire ambiente), **89 %** de ellas en países de ingresos bajos y medios | — | 2019 | ídem |
| Beneficio de un escalón (contexto de trayectoria) | alcanzar el IT-1 de PM2.5 (**35 µg/m³**) salvaría ~**300 000** muertes anuales en el mundo | — | — | OMS (hoja informativa) `[VERIFICADO]` |

**Justificación, y el hallazgo que hay que dejar escrito: el Óptimo del aire no existe, y eso no es una
carencia de la búsqueda.** La cita literal, del organismo que hizo la evaluación para el Reino Unido:

> *«The guideline values should **not** be regarded as thresholds below which there are no impacts on
> health… WHO (2021) note that the existing evidence generally supports a **linear, or supralinear,
> no-threshold relationship**… the concentrations used as the starting points for AQG development **are
> not equivalent to thresholds of no effect**; rather, they are levels below which there is less
> certainty about the existence of an effect.»* — COMEAP/UKHSA, julio 2022 `[VERIFICADO]`

Cuatro consecuencias de diseño, y las cuatro se aplican en este documento:

1. **En aire, Mínimo Absoluto y Óptimo coinciden numéricamente porque la fuente declara que no existe un
   piso sin efecto.** Esto **no** contradice la regla dura de separar las dos columnas: la columna del
   Óptimo se escribe `[SIN FUENTE VERIFICADA]` y **no se inventa un óptimo "más bajo" para rellenarla**.
   Lo votable en el aire no es la plenitud: es **la trayectoria** (§6 y §4.3).
2. **El déficit del aire se satura en 0 y nunca es negativo** por "mejor que la guía": como no hay piso
   sin efecto, estar por debajo de la guía **no es un excedente canjeable**, es simplemente menos daño
   `[HIPÓTESIS]` (deducción del proyecto sobre la declaración de no-umbral).
3. **Los Objetivos Interinos (IT) son escalones de transición, no el piso.** El piso es el valor AQG. Un
   contrato que se declare conforme alcanzando solo el IT-1 **está por debajo del SDV-E**. Es la misma
   decisión que el documento 06 §D1 acató y que el documento 07 ratificó.
4. **La ventana de temporada alta del O3 es la que hace que el aire sea dimensión del SDV-E y no solo del
   SDV-H.** Que la OMS cree en 2021 un valor de **temporada alta (60 µg/m³)** además del de 8 h (100)
   responde al daño crónico sobre la vegetación y los cultivos, no solo a la salud humana `[HIPÓTESIS]`
   (la guía no se leyó en su cuerpo; el valor sí). Un SDV-E que citara únicamente PM2.5 estaría midiendo
   salud humana y llamándola salud ecosistémica.

**Protocolo.** Red de **estaciones de monitoreo calibradas** (linaje B, sancionable) como medición; la
**teledetección** (linaje A) como cobertura de aerosoles, **nunca** como veredicto; la **ciencia
ciudadana** (linaje D) para el contraste local: un sensor casero no declara violación. Frecuencias
**impuestas por la fuente** (documento 06 §6.4): anual para la exposición de largo plazo (PM2.5, PM10,
NO2), 24 h para el corto plazo, 8 h para O3, y temporada alta para O3. Es decir: **el veredicto de aire
es anual, con alertas de 24 h**; no existe veredicto horario con fuente. Toda medición declara
**incertidumbre**; y una estación **sin incertidumbre declarada registra y no declara violación**
(documento 06 §D1.2). Un aviso de unidad que se repite porque es el error más fácil: **CO en mg/m³, todo
lo demás en µg/m³.**

**Violación.** Una medición admisible —instrumento, unidad y ventana declarados— de un contaminante por
encima de su valor AQG en su ventana: **una** medición admisible declara **violación puntual**; la
violación **persistente** —la que escala a retractación y veto— exige tres señales de linajes distintos
(documento 06 §5.5). Y una precisión que es una violación del protocolo y no del ecosistema: **declarar
conformidad invocando el IT o una ventana más permisiva en lugar del AQG.** El aire admite un grado de
proxy declarado: mientras la cifra se sostenga en la reproducción oficial y no en la lectura del cuerpo
primario, el veredicto se reporta como **proxy declarado de salud**, que es lo que la matriz del
documento 06 §4.10 llama así.

### 4.9 Tabla resumen del reparto LEY / POLÍTICA de esta dimensión

| Dimensión | LEY (el piso — no votable) | POLÍTICA (la plenitud — votable) |
|---|---|---|
| **Oxígeno disuelto** | Criterios de *Other Life Stages*: 5,5 / 6,5 (30 d) · 4,0 / 5,0 (7 d) · 3,0 / 4,0 (1 d); anoxia < 0,2 | Criterios de *Early Life Stages*: 6,0 / 9,5 (7 d) · 5,0 / 8,0 (1 d) |
| **pH** | Rango EPA: 6,5-9,0 (dulce) · 6,5-8,5 (salada) · ±0,2 en océano abierto · eclosión < 5 | Franja diaria tamponada 7,0-8,4 (uso como Óptimo: `[HIPÓTESIS]`) |
| **Temperatura** | Máxima media semanal para **crecimiento** de juveniles, **por especie indicadora del lugar** | Máxima media semanal para el **desove** de esa misma especie |
| **Nitrato** | Umbral **ecológico**: `[SIN FUENTE VERIFICADA]`. Proxy agronómico declarado: < 5 mg/L NO3-N | Bandas 5 y 30 mg/L NO3-N como referencia de uso del suelo |
| **Turbidez** | Criterio narrativo: **< 10 %** de reducción del punto de compensación | Umbral numérico local, a fijar por cuenca (la fuente deja la competencia en la jurisdicción) |
| **Contaminantes** | `[SIN FUENTE VERIFICADA]` como dimensión; valores CMC/CCC por sustancia de la fuente, sobre lista cerrada | Qué sustancias entran en la lista cerrada de la unidad (con carga de la prueba, T14) |
| **Salinidad** | Régimen natural declarado de la unidad; < 0,7 dS/m solo para unidades declaradas de agua dulce | Régimen natural como objetivo de gestión |
| **Aire (PM2.5, PM10, O3, NO2, SO2, CO)** | **Valor AQG de la OMS, 2021** (10 valores con sus ventanas) | `[SIN FUENTE VERIFICADA]` — **no se inventa un óptimo**. Se vota la **trayectoria** (qué IT, con qué plazo) y la prioridad de instrumentación |

---

## 5. Fórmula de violación, pesos y umbrales

La fórmula del SDV-E y su tabla de pesos son del documento 07; los tipos, estados y propiedades formales
de INV2-E son del documento 08. Este documento **no fija ninguna de las dos cosas**: fija **cómo entran
sus parámetros** en la fórmula que ya existe, y publica con aritmética a la vista la única discrepancia
que afecta a esta dimensión.

### 5.1 Los operadores de esta dimensión

| Operador | Significado | Parámetros de esta dimensión | Déficit normalizado |
|---|---|---|---|
| `min` | el piso es un mínimo que hay que superar | **oxígeno disuelto** (todas sus ventanas) | `D = max(0, (req − actual) / req)` |
| `max` | el piso es un techo que no hay que superar | **PM2.5, PM10, O3, NO2, SO2, CO**; nitrato (proxy); turbidez si la unidad adopta un umbral numérico local | `D = max(0, (actual − req) / req)` |
| `range` | hay una banda admisible | **pH** (6,5-9,0 · 6,5-8,5) y la variación de ±0,2 del océano abierto | `D = max(0, (lo − actual) / lo)` si `actual < lo`; `D = max(0, (actual − hi) / hi)` si `actual > hi`; `0` en otro caso |
| `escalonado` | niveles con consecuencia creciente, **sin interpolación** | **temperatura** por especie indicadora (crecimiento → supervivencia corta → embrión): cada nivel es un techo de la fuente y **no se interpola entre ellos** | el nivel alcanzado, tomado de la tabla de la fuente |
| `binary` | presencia/ausencia o categoría | **turbidez** cuando la unidad no tiene umbral numérico; umbral de **anoxia** (0,2 mg/L) como disparador; aire **sin cifra** (carbono negro, ultrafinas, polvo desértico) | **no produce déficit**: produce estado |

**La saturación en 0 no es un detalle.** Sin ella, el operador `range` del pH produce **déficit
negativo** con un agua demasiado alcalina —un ecosistema que «des-desafecta» su propio daño—, y el
operador `max` produce lo mismo con un aire mejor que la guía. Es la corrección que el documento 07 §3.3
ya fijó y que aquí se hereda sin cambios.

### 5.2 La ventana es parte del umbral (y su elección es auditable)

| Parámetro | Ventanas de la fuente | Regla de uso en la fórmula |
|---|---|---|
| Oxígeno disuelto | 30 días (media) · 7 días (mínimo) · 1 día (mínimo, **instantáneo**) | las tres conviven; **la instantánea declara violación puntual con una sola lectura** (§4, Dimensión 1) |
| PM2.5, PM10, NO2 | anual y 24 h | **no se suman**: misma molécula (F9 del documento 07) |
| O3 | 8 h (percentil 99) y temporada alta (6 meses) | **no se suman**; se toma la **peor** de las dos ventanas, porque miden el mismo contaminante |
| SO2, CO | 24 h | una sola ventana |
| pH, salinidad, turbidez | medición en el punto, contra la norma estacional o el régimen natural | se declara si es puntual, perfil o agregada |
| Temperatura | media semanal | una lectura diaria **no** puede declarar cumplimiento |

**La trampa que esta tabla cierra, dicha sin rodeos:** quien quiera fabricar cumplimiento sin mentir en
ningún número elige la ventana más permisiva y la declara. Por eso **la ventana elegida es un campo
obligatorio del registro** (documento 08 §6.1) y **está sujeta a disputa** (T13).

### 5.3 Agregación dentro de la dimensión, y prohibición de doble contabilidad

Se hereda la regla del documento 07 §5.1: **`A_k = max_i D_i` sobre los parámetros medidos de la
dimensión `k`**, nunca `Σ D_i`. Dos razones, y la segunda es de esta dimensión:

1. **Doctrinal:** la regla multi-indicador de la UNCCD es *«one-out, all-out»* —si un indicador empeora,
   el resultado no es neutro— `[VERIFICADO]`, y esa es la lógica del piso.
2. **Empírica, y verificada en la fuente de esta dimensión:** promediar los diez valores del aire haría
   que un PM2.5 catastrófico quedara diluido por nueve valores correctos. **El aire de la unidad no está
   bien: está envenenado por un lado.**

**Aplicación concreta de la prohibición de doble contabilidad en esta dimensión** (y es la más necesaria
de todo el estándar, porque aquí hay tres casos):

- **PM2.5 anual (5 µg/m³) y PM2.5 24 h (15 µg/m³)**: mismo contaminante, dos ventanas → **se elige una y
  se declara**.
- **O3 de 8 h (100) y O3 de temporada alta (60)**: mismo contaminante, dos ventanas → **se toma la peor**,
  nunca la suma.
- **Oxígeno: media de 30 días, mínimo de 7 días y mínimo de 1 día**: tres ventanas del mismo parámetro.
  **Se agrega por el peor caso medido (max)**, y el cruce del mínimo instantáneo se registra además como
  **hecho** (violación puntual), no como sumando.

### 5.4 Los pesos: lo que este documento consume, y la discrepancia que publica

**Este documento no fija pesos.** Lo que fija son los parámetros, sus operadores y sus ventanas. Los
pesos que le corresponden, tomados de los dos vectores vigentes:

| Bloque | Peso en `PESOS_TABLERO` (documento 08 §5.2) | ¿Tiene piso? | `PESOS_PISO` (documento 08 §5.2) |
|---|---|---|---|
| Calidad del aire (los parámetros de la Dimensión 8) | **0,200** | 🟢 sí (OMS 2021) | **0,200** |
| Calidad del agua (pH, nitrato, bicarbonato) | **0,180** | 🟢 parcial (solo el pH tiene umbral ecológico verificado) | **0,180** |
| Oxígeno disuelto | **0,020** | 🔴 **así lo marca el documento 08** — pero **sí tiene umbral** (§1.3) | **0,020** (aunque el 08 lo declare sin piso y su cifra de cobertura no lo cuente igual) |

¹ **La fila del oxígeno no es una fila suelta: es parte del vector, y por eso su aritmética hay que leerla
despacio.** El documento 08 §5.2 declara siete grupos —aire 0,20 · agua (pH, NO₃-N, HCO₃) 0,18 ·
**oxígeno 0,02** · biodiversidad/RLE 0,30 · suelo 0,15 · caudal 0,075 · conectividad 0,075—, y **esos
siete suman 1,000**; su «suma de los que tienen piso», **0,680**, y su agujero declarado, **0,320**,
reparten justamente esos siete grupos. Es decir: **el 0,020 del oxígeno está en el vector del documento
08** —lo que le falta es el **piso**, no el peso— y **el 08 no dice si su 0,680 ya lo cuenta**: si lo
cuenta, ratificar el piso deja la cifra en 0,680 y el agujero en 0,300 (suelo, caudal, conectividad); si
no lo cuenta, la sube a 0,700 y deja el agujero en 0,300 igual. Las dos lecturas son compatibles con el
texto del 08 y **este documento no elige por él**: lo que sí afirma es que **el 0,020 ya está asignado y
que, por tanto, activar el piso del oxígeno no puede presentarse como un aumento de peso sin declarar la
duda**.

**Y aquí está la discrepancia que este documento debe publicar en vez de resolver por su cuenta.** Con la
disputa del oxígeno disuelto resuelta (§1.3), el oxígeno **tiene piso**, y un parámetro con piso no
puede quedar fuera del vector del piso sin una razón. Pero la corrección **no es una suma: es un cambio de
atribución dentro del mismo vector** —el 0,020 que hoy se lee como parte del bloque genérico de agua
(cuyo piso es un **proxy agronómico**) pasa a leerse como el oxígeno, cuyo umbral es el único
**ecocéntrico** del agua (§4, Dimensión 1)—. La corrección propuesta —que es la misma que el documento 12
ya propuso por su cuenta, lo cual es una señal de convergencia y no una coincidencia— es **que el 0,020
del oxígeno se compute como parámetro con piso**, y su consecuencia aritmética es la de la tabla:

| Qué | Hoy | Si se ratifica el piso del oxígeno |
|---|---|---|
| `PESOS_PISO` del documento 08 | **0,680** | **0,680 o 0,700, según cómo lea el 08 su propia fila** — y **no 0,925**: esa cifra vuelve a sumar un peso ya contado |
| Parámetros con umbral en el catálogo del documento 08 | **19 (18 con peso)** (§5.5) | **20 (19 con peso)** |
| Cobertura declarada del piso | *«el 68 % del peso total que declara querer proteger»* | **el 68 %, o el 70 % si su 0,680 no contaba el oxígeno** |

**Una precisión que corrige dos deslices aritméticos, uno ajeno y uno propio.** El documento 07 §13
(pregunta 14) estima que, si el documento 08 acepta el umbral del oxígeno, *«la cobertura del piso sube a
0,925 en su catálogo»*: la aritmética no da eso **ni sobre el catálogo del 07 ni sobre el del 08**. El
0,925 sale de sumar 0,020 al subtotal **0,905 del propio documento 07** —que ya cuenta el oxígeno aparte—
de modo que la frase mezcla un vector con el otro y vuelve a sumar un peso que ya estaba dentro. Y la
primera versión de este documento cometía el mismo error al revés: proponía **0,700** sumando otra vez el
0,020 a un 0,680 que **puede** contenerlo ya. La cifra honesta sobre el catálogo del documento 08 es
**0,680 con la duda declarada**, y se registra en §13 (pregunta 2).

### 5.5 La aritmética de la disputa del oxígeno disuelto, con los números a la vista

| Paso | Qué pasa | Cifra |
|---|---|---|
| 1 | Ruta citada por el documento 08 (`/wqc/aquatic-life-criteria-dissolved-oxygen`) | **404 — muerta**, confirmado |
| 2 | ¿Se sigue de ahí que no haya umbral? | **No.** La hoja informativa de parámetro del mismo organismo responde **200** y publica el valor con ventana de promediado |
| 3 | ¿Se transcribe el valor sin más? | **No**: hay que **corregir el etiquetado de etapa de vida** del documento 07 (mezcló *Other* y *Early Life Stages* en la fila de 7 días) |
| 4 | ¿Cuál es el piso? | **`Other Life Stages`**: 5,5 / 6,5 (30 d) · 4,0 / 5,0 (7 d) · 3,0 / 4,0 (1 d) |
| 5 | ¿Y el Óptimo? | **`Early Life Stages`**: 6,0 / 9,5 (7 d) · 5,0 / 8,0 (1 d) |
| 6 | ¿Convergen otras fuentes? | **Sí, con matices que §4 declara**: CCME 1999 (**los mismos cuatro valores** de agua dulce) y UE 2006/44/CE (misma zona de protección: 100 % ≥ 7 / ≥ 5 y 50 % ≥ 9 / ≥ 8 por muestras), ambos leídos y citados por el **documento 12** |
| 7 | ¿Qué le falta al vector del piso? | El **piso** del oxígeno, cuyo peso de **0,020 ya está asignado** en el documento 08: no es una suma, es una atribución (§5.4) |

**Y una segunda consecuencia de recuento, independiente del oxígeno.** La ventana de **temporada alta del
O3 (60 µg/m³)** es un valor AQG de 2021 que **no aparece en el catálogo de parámetros del documento 08**
(que lista `aire_o3_8h` y no la temporada alta), aunque el documento 06 §6.4 **sí la nombra como
ventana**. Dos formas de incorporarla, y elegir una es de la revisión de coherencia (§13, pregunta 10):
(a) como **campo propio**, con lo que el recuento del documento 08 pasa de **19 a 20 parámetros con umbral**
(y a 21 si el oxígeno entra en el mismo acto); o (b) como **ventana alternativa del mismo parámetro**,
con lo que el recuento no cambia **pero el veredicto del O3 sí** —se toma la peor de las dos ventanas—.
Este documento **recomienda (b)** por la regla de no doble contabilidad, y **declara** que la decisión no
es suya.

### 5.6 Los dos vectores de pesos del documento 07, y su aritmética

Este documento consume pesos, y al consumirlos encontró un problema **que no puede dejar pasar**, porque
la propiedad F4 del propio documento 07 exige que la suma sea exactamente 1,000 comprobada por código
(`abs(Σ PESOS_TABLERO − 1) < 1e-9`). La tabla de su §5.3, leída fila por fila, **no suma eso**:

| Columna del documento 07 §5.3 (la de **su** tabla fusionada; el documento 08 no publica estos totales, publica **1,000** y **0,680**) | Suma de sus ocho filas | Lo que el documento declara |
|---|---|---|
| `PESOS_TABLERO` (0,300 + 0,200 + 0,180 + **0,020** + 0,150 + 0,150 + 0,075 + **0,075**) | **1,150** | **1,000** |
| `PESOS_PISO` (0,300 + 0,200 + 0,180 + **0,000** + 0,150 + 0,150 + 0,075 + **0,000**) | **1,055** | **1,000** |

**El defecto no es la fusión, es la suma escrita al lado.** Los cinco bloques del ISE no se conservan «tal
cual»: el bloque del agua **se subdivide** (0,200 → pH y compañía 0,180 + oxígeno disuelto 0,020) y el de
especies clave **no tiene fila propia** en la tabla del 07 (su 0,150 sigue dentro de otras filas). Lo que
sí ocurrió es lo que dice la frase siguiente: **se añadieron caudal (0,075) y conectividad (0,075) sin
quitarle nada a nadie**, y por eso las sumas publicadas —**1,150** y **1,055**— son la aritmética real de
esa tabla, mientras que las cifras declaradas —**1,000** en ambos vectores— no lo son. Y de ahí sale
también la cifra de cobertura: **0,905 = 1,000 − 0,020 − 0,075 se calcula sobre un total de 1,000 que ese
vector no tiene**.

**Qué hace este documento con esto:** (a) **no adopta ningún vector propio** —no le corresponde—; (b)
**no renormaliza por su cuenta**, porque renormalizar cambia el peso de todas las dimensiones y eso es
una decisión de la política del estándar; (c) **declara que el único vector internamente consistente hoy
es el del documento 08** (0,20 + 0,18 + 0,02 + 0,30 + 0,15 + 0,075 + 0,075 = **1,000**), que es el que
esta dimensión cita; y (d) **pide que la revisión de coherencia elija el reparto**, ofreciendo la
solución aritmética obvia —reducir proporcionalmente los cinco bloques del ISE por el factor 0,85 para
hacer sitio a caudal y conectividad— **marcada como propuesta no ratificada** y con su consecuencia
escrita: **con ese factor, la calidad del aire pasaría de 0,200 a 0,170 y el agua de 0,200 a 0,170**, lo
que cambia el peso de esta dimensión entera (§13, pregunta 4).

### 5.7 Duración en TA, y por qué aquí la fuente casi la da

*«Respetamos la soberanía del reino natural sobre su propio TA» (el PIU traduce)* (Cap. 16.5 §16.5.14). La fórmula
acumula en **ciclos de TA** y **jamás en TVI ni TPI**; la conversión TA↔TVI es un paso posterior,
auditable, con el **PIU** (Cap. 5 §5.5) como único instrumento.

**Lo que esta dimensión aporta al problema de la duración es un ancla, y es más de lo que tienen las
otras:** las fuentes publican **ventanas de promediado** (30 días, 7 días, 1 día, anual, 24 h, 8 h,
temporada alta) y **una de ellas publica además una regla de instantaneidad** —*«All minima should be
considered as instantaneous concentrations to be achieved at all times»* (nota de la Tabla 1 de la hoja
de oxígeno) `[VERIFICADO]`—. Es decir: **para el mínimo de 1 día del oxígeno, la duración tolerada es
cero** `[HIPÓTESIS]` (lectura del proyecto sobre una regla publicada). Eso convierte el oxígeno en el
parámetro de esta dimensión que puede declarar violación **sin resolver antes cuánto dura una violación**.

**Lo que la fuente no da, y se declara:** cuántos días bajo el piso **constituyen** violación persistente.
Y la unidad del ciclo TA de una masa de agua **sí tiene una respuesta disponible para el río** —el **año
hidrológico**, que el documento 12 ya fijó como unidad de ciclo de su tabla—, de modo que este documento
la hereda para las unidades fluviales y **no la impone** al lago, al humedal ni al acuífero: para ellos,
la unidad de ciclo sigue siendo **configuración obligatoria y sin valor por defecto** (documento 07
§5.4b).

### 5.8 Ejemplo aplicado, con la aritmética verificable a mano

**La unidad.** El **humedal del conjunto residencial** —el caso canónico: *«Un conjunto con crédito
regenerativo acumulado pero humedal bajo su SDV-E no está en coherencia: INV2-E será su juez»*
(Cap. 16.5 §16.5.14)—. Los valores medidos son **ilustrativos**; **los pisos no: son los de las fuentes
citadas**. El crédito regenerativo del conjunto es **−12,0 unidades de R** —el valor que la suite del
repositorio ya usa para el crédito negativo `[VERIFICADO]` en `tests/test_micromax.py`— y **no entra en
ningún paso de este cálculo**.

| Dimensión | Parámetro y ventana | Piso (fuente) | Medición | Operador | `D_i` | `A_k` de la dimensión |
|---|---|---|---|---|---|---|
| Oxígeno disuelto | media de 30 días, agua cálida | 5,5 mg/L (US EPA, 1986 vía hoja 2021) | **4,2 mg/L** | `min` | `(5,5−4,2)/5,5 = 0,2364` | **0,2364** |
| Oxígeno disuelto | mínimo de 1 día (**instantáneo**) | 3,0 mg/L (ídem) | **2,8 mg/L** | `min`/`binary` | cruce del piso → **hecho declarado**, no se suma | (registrado como hecho) |
| pH | lectura matinal | 6,5 – 9,0 (US EPA, 1986) | **6,2** | `range` | `(6,5−6,2)/6,5 = 0,0462` | **0,0462** |
| Nitrato | NO3-N, ciclo TA | proxy declarado < 5 mg/L (FAO, 1985) | **4,0 mg/L** | `max` | `0` (cumple el proxy) | **0,0000** |
| Temperatura | media semanal, trucha arcoíris | crecimiento ≤ **19 °C** · supervivencia corta ≤ **24 °C** · embrión ≤ **13 °C** (US EPA, 2012 vía hoja 2021) | **22 °C** | `escalonado` | cruce del techo de crecimiento (19 °C); `(22−19)/19 = 0,1579` `[HIPÓTESIS]` — proporción **del proyecto**: la fuente publica escalones y **no interpola** | **0,1579** |
| Turbidez | punto de compensación vs. norma estacional | < 10 % de reducción (US EPA, 1986) | **4 %** | `binary` | cumple | **0,0000** (sin peso) |
| Aire | PM2.5 anual | 5 µg/m³ (OMS, 2021) | **8 µg/m³** | `max` | `(8−5)/5 = 0,6000` | |
| Aire | O3 temporada alta | 60 µg/m³ (OMS, 2021) | **75 µg/m³** | `max` | `(75−60)/60 = 0,2500` | |
| Aire | NO2 anual | 10 µg/m³ (OMS, 2021) | **12 µg/m³** | `max` | `(12−10)/10 = 0,2000` | **0,6000** (el peor: PM2.5) |
| Aire | PM2.5 24 h · SO2 24 h · CO 24 h | 15 µg/m³ · 40 µg/m³ · 4 mg/m³ | 12 · 30 · 3 | `max` | `0` (cumplen) — **y el PM2.5 de 24 h no se suma al anual** (misma molécula) | (no se suman) |

**El veredicto, en tres capas:**

| Capa | Resultado | Cómo se lee |
|---|---|---|
| **Veredicto del piso** | 🔴 **VIOLACIÓN DECLARADA** | cuatro parámetros medidos con déficit positivo (oxígeno 0,2364 · pH 0,0462 · temperatura 0,1579 · aire 0,6000) **y un cruce instantáneo del piso** (oxígeno de 1 día, 2,8 < 3,0). `is_valid = False`; **hay bloqueo** (P1 del documento 08) |
| **Agregación por dimensión** | `A_agua = max(0,2364 · 0,0462 · 0,1579 · 0 · 0) = 0,2364` · `A_aire = 0,6000` | es la parte que este documento aporta; **el compuesto ponderado `v` es del documento 07** y aquí **no se calcula**, precisamente porque su vector de pesos está en disputa (§5.6) |
| **Saldo** | **−12,0 R no aparece en ninguna capa** | el conjunto puede haber plantado árboles y haberlos registrado: **el humedal sigue bajo su SDV-E y el veredicto es el mismo** |

**Lo que el ejemplo enseña, y por eso se escribe:** el oxígeno —el parámetro cuya disputa bloqueaba su
uso— es **el de mayor déficit del agua** en este caso. Durante todo el tiempo en que la biblioteca lo dio
por «sin umbral», este humedal habría pasado el filtro del agua con un déficit de 0,2364 **invisible**.
Esa es la consecuencia práctica de resolver la disputa, y es la razón por la que este documento existe.

---

## 6. Protocolo de medición (sensores, frecuencias, quién reporta)

El **elenco formal** de sensores, sus linajes (A teledetección · B in-situ · C bioindicadores · D ciencia
ciudadana · E comunidad testigo con datos abiertos), sus límites físicos y la firma T13 son del documento
06. Aquí se fija **el protocolo que la fuente de cada umbral impone**, y se declara cuando la fuente no
impone ninguno.

### 6.1 Tabla de protocolo por parámetro

| Parámetro | Instrumento | Frecuencia mínima exigible | Quién reporta | Ventana del veredicto |
|---|---|---|---|---|
| Oxígeno disuelto | sonda multiparamétrica in-situ, **mg/L y % de saturación** | registro continuo o muestreo regular; **muestra matinal obligatoria** si es puntual; perfil a varias profundidades | laboratorio o comunidad de custodia; **el guardián `eco-` consiente, no mide** | 30 d · 7 d · 1 d (instantáneo) |
| pH | sonda/electrodo con calibración declarada; **capacidad tampón como covariable** | extremo diario desfavorable o registro continuo; en ríos, la frecuencia del documento 12 | ídem | rango, contra la variación natural |
| Temperatura | termometría continua o semanal, aguas arriba y abajo de vertidos térmicos | **semanal** (la ventana del piso es una media semanal) | ídem | media semanal |
| Nitrato | laboratorio, con **convención de unidad declarada** (NO3-N o NO3) | una vez por ciclo TA, y en estación húmeda | laboratorio acreditado o red de custodia | la del ciclo |
| Turbidez | disco de Secchi o sonda de luz (punto de compensación); NTU y satélite **solo como cobertura** | estacional, contra la norma de la misma estación | ídem | estacional |
| Contaminantes | laboratorio, métodos normalizados, **pH y dureza en la misma muestra** | según la lista cerrada de la unidad y sus presiones | laboratorio acreditado | la de la muestra, con el ciclo declarado |
| Salinidad / conductividad | sonda con compensación de temperatura, en el mismo lance que el oxígeno | la misma que el oxígeno | ídem | puntual o perfil |
| **Aire** (PM2.5, PM10, O3, NO2, SO2, CO) | red de estaciones calibradas (linaje B, **sancionable**); teledetección de aerosoles (A) como cobertura; ciencia ciudadana (D) para contraste | **anual**, **24 h**, **8 h** y **temporada alta**, según el contaminante (las fija la fuente) | red de monitoreo + comunidad testigo | la de cada valor AQG |

### 6.2 Lo que este protocolo prohíbe, y por qué cada prohibición tiene fuente

1. **Declarar conformidad de oxígeno con una lectura de mediodía en superficie.** La fuente dice que el
   mínimo diario ocurre **temprano en la mañana** y que los organismos son más vulnerables entonces
   `[VERIFICADO]`: una medición al mediodía puede declarar conforme un ecosistema que viola el piso cada
   amanecer.
2. **Declarar conformidad de oxígeno sin % de saturación.** La salinidad y la altitud reducen la
   capacidad del agua de absorber oxígeno `[VERIFICADO]`: sin el % de saturación, un río de montaña frío y
   un río cálido de tierras bajas con el mismo oxígeno real reciben lecturas que no son comparables.
3. **Declarar conformidad de pH sin resolver el ciclo diario ni declarar la capacidad tampón.**
4. **Declarar conformidad de temperatura con una lectura diaria** cuando el piso es una media semanal.
5. **Usar la turbidez como umbral numérico universal.** La fuente advierte que la turbidez alta no
   implica mala calidad ni la baja buena `[VERIFICADO]`.
6. **Convertir una aprobación del guardián en una medición.** *El guardián oráculo consiente, no mide*
   (`app/contracts_bp.py`). Si el único respaldo de un valor es la firma del guardián, el parámetro se
   marca `sin_evidencia` y el estado es `indeterminado` (documento 08 §6.1).
7. **Declarar violación de aire con un sensor sin incertidumbre declarada** (documento 06 §D1.2).

### 6.3 Admisibilidad: los cuatro campos, y los dos que esta dimensión añade

Toda medición de esta dimensión entra en una validación **solo si** trae los cuatro campos del documento
08 §6.1: `valor` + `unidad`, `ta_periodo` (inicio y fin en **TA**), `fuente_dato` y `evidencia_ref`. Y
esta dimensión **añade dos campos obligatorios**, porque sin ellos sus umbrales no son aplicables:

| Campo añadido | Para qué | Consecuencia de su ausencia |
|---|---|---|
| `ventana` (30 d · 7 d · 1 d · anual · 24 h · 8 h · temporada alta · estacional) | el mismo número significa cosas distintas en ventanas distintas (§5.2) | el parámetro se trata como **no medido** |
| `bandera_proxy` (aire de la OMS; nitrato FAO) | impide reportar un proxy de salud humana o de aptitud agronómica como integridad ecológica | el registro se acepta **con la bandera**, y la violación se reporta como proxy |

### 6.4 TA: lo que este protocolo no decide

La unidad del ciclo TA **no está decidida** para el SDV-E en general (documento 07 §5.4b: configuración
obligatoria, sin valor por defecto). Para las unidades fluviales, este documento **hereda el año
hidrológico** que el documento 12 fijó. Para lago, humedal y acuífero **no elige**: elegir «año
calendario» por comodidad de implementación sería colonizar el tiempo del humedal con el calendario del
municipio, que es exactamente lo que la salvaguarda prohíbe.

---

## 7. Verificación y auditoría (T13, guardián, comunidad testigo)

### 7.1 Qué se audita en esta dimensión

| Se audita | Cómo |
|---|---|
| Que la **unidad** del dato sea la del umbral | validación del campo `unidad` contra la convención declarada (NO3-N ≠ NO3; CO en mg/m³) |
| Que la **ventana** sea la del criterio | campo `ventana` obligatorio; la elección queda registrada |
| Que la medición sea **admisible** | los cuatro campos + los dos añadidos (§6.3); sin ellos, `None` |
| Que el **proxy** esté declarado | campo `bandera_proxy`; un proxy excedido no se reporta como integridad ecológica |
| Que el aire no se declare con **IT** en lugar de **AQG** | el IT es trayectoria y su uso como piso es una violación de la auditoría |
| Que la **contabilidad no se borre** | T13: cada validación deja registro; una violación registrada **no se des-registra con un pago posterior**, porque ocurrió en un TA que no vuelve |

### 7.2 La regla de auditoría de los vacíos (la lección del oxígeno, convertida en procedimiento)

De la disputa 07/08 sale una regla que este documento propone como **procedimiento de auditoría de
vacíos** `[HIPÓTESIS]`, y que es la parte del episodio que más vale:

> **Todo vacío declarado debe publicar (a) la URL exacta consultada, (b) su estado HTTP medido y (c) la
> lista de rutas alternativas del mismo organismo que se probaron.** Un vacío sin esas tres cosas no es
> un vacío verificado: es una búsqueda incompleta con forma de hallazgo.

Con esa regla, el caso del oxígeno se habría cerrado en la primera sesión: el 404 era cierto y la
conclusión era falsa, y lo que faltaba no era esfuerzo sino **método**. La regla tiene un segundo filo,
que es la otra mitad de la Regla 2 del preámbulo: **un 200 que no entrega el documento tampoco cuenta** —
la ruta del PDF de 4,11 MB de las guías de agua de consumo responde y no se descargó, de modo que el
nitrato y la turbidez de la OMS siguen siendo `[SIN FUENTE VERIFICADA]` **aunque su ruta esté
identificada**—.

### 7.3 El guardián, la comunidad testigo y los riesgos abiertos

El guardián `eco-` **consiente, no mide** (`app/contracts_bp.py`: *«Ecosistemas (eco-*): consentimiento
otorgado por el guardián oráculo»*). Esta dimensión depende de ello de forma especialmente directa,
porque **sus umbrales son números**: si el guardián pudiera aportar el valor de un parámetro, el piso se
fabricaría con una firma. Los tres riesgos abiertos del repositorio
(`docs/architecture/blindaje_anti_gamificacion_equidad.md`) se comportan aquí así:

| ID | Riesgo | Efecto sobre esta dimensión | Qué hace el diseño |
|---|---|---|---|
| **R4** | partes fantasma: cualquiera crea un `eco-*` sin autoridad sobre la entidad | alguien podría declarar el estado fisicoquímico de un río que no es suyo | no se resuelve aquí: es una precondición de identidad (documento 05) y se declara 🔴 |
| **R6** | T9/T17 (Reciprocidad Justa) no se valida en la creación: pasa un contrato unilateral | se podría **verter sobre una masa de agua** sin contraprestación | lo que falta es el bloqueo por piso medido (documento 08 §8.5); hasta que exista, sigue pasando |
| **R13** | guardián `eco-` con heurística laxa (sin `DEEPSEEK_API_KEY` aprueba si los invariantes pasan) | un guardián laxo podría «consentir» un agua contaminada | **el piso no se delega al guardián**: se calcula desde mediciones admisibles. Un guardián laxo **relaja, no habilita** |

**Y una ausencia que este documento declara como propia:** no hay **calibración interlaboratorio ni
patrón de referencia** para las sondas de agua en esta rama (el documento 06 §13 ya lo registró), de modo
que **la incertidumbre de la medición de oxígeno, pH y conductividad hoy no está acotada**. Con la regla
de declarabilidad del documento 06 §5.3, eso tiene una consecuencia dura y honesta: **una sonda sin
incertidumbre declarada registra y no declara violación**.

---

## 8. Invariante INV2-E: de estándar a contrato ejecutable

La especificación de INV2-E es el documento 08. Aquí se enumera **exactamente qué recibe de esta
dimensión**, y qué cambia en él cuando la disputa del oxígeno queda resuelta.

### 8.1 La interfaz: lo que INV2-E recibe de esta dimensión

| Pieza que INV2-E consume | De dónde sale | Estado |
|---|---|---|
| Parámetros con operador, unidad y **ventana** | §4, dimensiones 1 a 8 | 🟡 especificado; **sin implementar** |
| Piso del oxígeno disuelto **con umbral** (deja de ser dimensión sin piso) | §1.3, §4 (Dimensión 1) | 🟡 criterio fijado; **el peso está en disputa** (§5.4) |
| Agregación intra-dimensión `A_k = max_i D_i` y prohibición de doble contabilidad | §5.3 | 🟡 especificado |
| **Dos campos de admisibilidad añadidos** (`ventana`, `bandera_proxy`) | §6.3 | 🟡 propuesta |
| Regla de instantaneidad del mínimo de 1 día (duración tolerada = 0) | §5.7 | `[HIPÓTESIS]` sobre regla publicada |
| Dimensiones **binarias sin peso** de esta materia: turbidez sin umbral numérico; aire sin cifra (carbono negro, ultrafinas, polvo desértico) | §4 (Dimensiones 5 y 8) | 🟡 propuesta de añadido al catálogo binario del documento 07 §4.4 |
| Las dos vías de bloqueo, con un caso nuevo de la vía precautoria (**anoxia**) | §3 pilar 2 y §4 Dimensión 1 | 🟡 especificado |

### 8.2 Lo que cambia en INV2-E con esta dimensión

1. **El oxígeno disuelto deja de ser una dimensión que «se registra y no calcula».** El documento 08 §4.2
   lo lista entre los seis dominios que **no pueden activar INV2-E hoy** por falta de umbral. Con el
   criterio fijado, el oxígeno **sí tiene definición operativa de violación** —un hecho observable: una
   media de 30 días bajo 5,5 / 6,5, o un mínimo instantáneo bajo 3,0 / 4,0— y por tanto **puede activar
   el bloqueo por piso (P1)**. La corrección formal de esa fila corresponde al documento 08 (§13,
   pregunta 1).
2. **El aire aporta el caso más puro de la propiedad P2 (base neutra).** Como la fuente declara que no
   existe un piso sin efecto, «mejor que la guía» **no genera crédito**: el déficit se satura en 0 y
   `FE = 1,0` no certifica nada que no se haya medido.
3. **La propiedad P3 (independencia del saldo) tiene aquí su caso canónico** (§5.8 y §9): el mismo
   humedal, con −12,0 R o con −12 000 R, da el mismo veredicto, porque **`R` no existe en la expresión**.
4. **La prohibición de doble contabilidad se vuelve una obligación formal del tipo**, y no una nota: el
   tipo `SDV_E` no puede sumar `aire_pm25_anual` con `aire_pm25_24h`, ni las dos ventanas del O3, ni las
   tres del oxígeno. Es el test F9 del documento 07 aplicado a un catálogo donde el solapamiento es real.
5. **El estado por defecto sigue siendo `indeterminado`**, y esta dimensión lo confirma con datos: sin
   sensores de agua ni de aire conectados (§12), ninguna unidad puede cubrir sus parámetros, y por tanto
   **ninguna unidad puede declararse por encima de su suelo ni generar crédito regenerativo utilizable**.
6. **Un caso nuevo para la vía precautoria (T14).** La anoxia por debajo de 0,2 mg/L no necesita umbral
   adicional para bloquear: es un **hecho** que además destruye la recuperabilidad lineal del sedimento
   (§3 pilar 2). El bloqueo precautorio del documento 08 §8.5 encuentra aquí su aplicación más clara.

---

## 9. El suelo antes que el saldo (no compensación)

La regla es canónica y esta dimensión solo la traduce a su materia:

> *"Un conjunto con crédito regenerativo acumulado pero humedal bajo su SDV-E no está en coherencia:
> **INV2-E será su juez**."* — Cap. 16.5 §16.5.14

**Por qué aquí la regla es más dura que en cualquier otra dimensión, con tres razones verificadas:**

1. **El aire no admite compensación ni siquiera en teoría.** La fuente declara una relación **lineal o
   supralineal sin umbral** entre concentración y daño `[VERIFICADO]`: no hay un nivel por debajo del
   cual «sobre» aire limpio. Un territorio que reduzca su PM2.5 por debajo de 5 µg/m³ **no acumula un
   excedente canjeable**: acumula menos daño. El aire es, literalmente, la dimensión donde el crédito no
   tiene dónde existir.
2. **El oxígeno cruzado el umbral de anoxia deja de ser recuperable de forma lineal.** El sedimento
   anóxico libera el fósforo que tenía fijado, y ese fósforo **alimenta la eutrofia que consume más
   oxígeno** `[VERIFICADO]`. El daño se autoalimenta: no es solo que el crédito no lo repare, es que
   **el sistema sigue dañándose solo** mientras nadie interviene. T14 convierte eso en obligación: elegir
   la opción de menor irreversibilidad y documentar el costo asumido.
3. **Un agua puede estar «limpia» y muerta, o «sucia» y viva, y el saldo no distingue.** La propia fuente
   advierte que la turbidez alta no implica mala calidad ni la baja buena `[VERIFICADO]`; el pH puede
   estar en rango y el metal disuelto ser letal (Dimensión 2); el nitrato puede cumplir el proxy
   agronómico y la eutrofia estar en marcha (Dimensión 4). **Un índice de un solo número no puede
   representar esto**, y el crédito regenerativo no puede comprarlo.

**Cómo se garantiza formalmente.** El crédito regenerativo vive en el componente **R** del VHV, que sí
admite negativos —*«Permite valores negativos… genera un VHV Negativo en este componente»* (EVV-1.2
§4.3), implementado y probado con `r_units = -12.0` `[VERIFICADO]`—. La fórmula que consume esta
dimensión (§5) **no tiene un término `R`**. Lo que el crédito puede comprar es **restauración por encima
del piso** —y eso es valioso y se registra en R—; lo que no puede comprar es **el derecho a estar por
debajo**.

---

## 10. Zona Libre: lo que NO se mide

*«Parte del valor del humedal es inefable (Cap. 7 §7.9). Los sensores miden salud (agua, cobertura,
biodiversidad indicadora); jamás "milagros". Medir todo sería la forma técnica de dejar de escucharlo»*
(Cap. 16.5 §16.5.14).

**Traducción a esta dimensión:** la Zona Libre del Reino Natural es una **dimensión binaria auditable sin
peso** y no tiene término en la aritmética. Aquí eso significa, en concreto, que **la calidad del agua y
del aire no agotan el valor de una masa de agua ni de un aire**: se mide lo que sostiene la vida, no lo
que la vida vale.

**Y aquí hay una distinción que este documento considera su aportación doctrinal más útil, porque
impide dos abusos simétricos.** En esta dimensión conviven **dos cosas distintas que se parecen**, y
confundirlas es la vía más barata para vaciar el estándar o para llenarlo de burocracia:

| | **Zona Libre (límite doctrinal)** | **Cobertura faltante (límite instrumental)** |
|---|---|---|
| Qué es | lo que **se decide no medir** porque su valor es inefable | lo que **no se puede medir todavía** porque falta el instrumento o la fuente |
| Ejemplos en esta dimensión | el valor propio del río; el juicio estético sobre un agua clara; la vida interior del ecosistema (*«registramos la interacción, no la vida interna»*) | contaminantes sin lista cerrada; turbidez sin cifra de la OMS; calidad de agua subterránea; óptimo del aire |
| ¿Genera obligación? | **No.** Es una decisión doctrinal y su catálogo se vota (categoría `critical`, documento 09 §10) | **Sí**: bandera de opacidad ecológica y **obligación contractual de instrumentar** (documento 08 §6.3) |
| ¿Pesa en la fórmula? | **No**, nunca (P12 del documento 08) | **No** mientras no haya umbral; y **no habilita crédito** |
| Riesgo si se confunde | declarar «inefable» lo que solo es incómodo de medir **vacía el estándar** | tratar un vacío instrumental como límite doctrinal **eterniza la ceguera** |

**El borde, escrito para que no se cruce:** *«medir todo sería la forma técnica de dejar de escucharlo»*
no autoriza a dejar de medir lo que sí se puede medir. Y la Zona Libre no es un depósito donde guardar
los parámetros que no se lograron cerrar: eso es cobertura faltante, y se publica como tal.

---

## 11. Comparativa inter-reinos (SDV-H · SDV-A · SDV-E · SDV-S)

La comparación completa es el documento 09. Lo pertinente aquí es **dónde vive el agua y el aire en cada
reino**, y qué revela eso.

| Eje | **SDV-H** — humanos | **SDV-A** — animales | **SDV-E** — ecosistemas (este documento) | **SDV-S** — sintéticos |
|---|---|---|---|---|
| **Sujeto del agua y del aire** | la persona | el animal | **la masa de agua y la atmósfera de la unidad ecológica** | no aplica: su ambiente es computacional |
| **Forma métrica del agua** | **cantidad por sujeto y día** (L/persona/día) | **cantidad por animal y día** (L/día) | **calidad por masa de agua** (mg/L, unidades de pH, dS/m) + la cantidad como régimen (documento 12) | — |
| **Forma métrica del aire** | calidad del aire como dimensión de salud (µg/m³) | condiciones de aire y ventilación de la especie | **los mismos µg/m³, como proxy declarado de salud** | — |
| **Moneda temporal** | TVI | TA, traducido por el PIU | **TA**, traducido por el PIU | TPI |
| **Quién publica el piso** | la OMS (agua de consumo y aire) | el diseño biológico y la etología por especie | **la agencia ambiental** (US EPA, CCME, UE) para el agua, y la OMS para el aire | coherencia y potencial experiencial |
| **¿Hay un piso compartido?** | — | — | **sí: el aire de la OMS protege a los tres reinos con el mismo número** | — |
| **El error que no se hereda** | el Óptimo del agua tomado como Mínimo Absoluto (el motor del SDV-H) | — | — | `FS_S = 1 + e^v` (corregido a `e^v`) |

**Tres lecturas que solo se ven en esta tabla:**

1. **La misma molécula se mide distinto según el sujeto, y eso no es un capricho: es la consecuencia
   métrica de la diferencia de sujeto.** El SDV-H y el SDV-A miden **cantidad por sujeto** (litros por
   persona, litros por animal); el SDV-E mide **condición por masa y por tiempo**. Es la misma lección del
   documento 09 §11.2 (eje 1-2): los tres primeros reinos protegen entes discretos; el cuarto protege un
   ente cuya extensión es su identidad.
2. **El aire es el primer piso literalmente compartido por tres reinos.** El mismo valor de PM2.5 que
   protege al humano y al animal protege al ecosistema, y eso convierte la dignidad encadenada
   (Cap. 10 §10.6) en un hecho contable y no en una metáfora: **la dimensión donde los tres reinos
   comparten número es la dimensión donde el daño se comparte primero**.
3. **El SDV-E es el único reino cuyo piso de agua no puede ser una cifra por sujeto.** Un río no bebe
   litros: sostiene concentraciones. Y por eso este documento no puede —ni debe— reutilizar el 20 L/día
   del reino humano: es la misma molécula medida en la unidad del sujeto equivocado.

---

## 12. Estado de implementación

Verificado por lectura directa del repositorio en octubre 2026 (grep sobre `*.py` del motor y de la
aplicación), coincidente con la auditoría de solo lectura documentada en
`scratch/sdv_e/INVENTARIO_IMPLEMENTACION.md`. **Resumen brutal: de esta dimensión no existe ni el nombre
de un solo parámetro.**

| Pieza | Estado | Evidencia |
|---|---|---|
| `SDV_E` (tipo con dimensiones, operadores y ventanas) | 🔴 **no existe** | `grep` de `SDV_E\|sdv_e` sobre todo el repositorio: **cero coincidencias en el motor** (`maxocontracts/`); `maxocontracts/core/types.py` define `SDV` y `SDV_S` |
| `SDV_EValidatorBlock` y `validate_invariant_sdv_e` | 🔴 **no existe** | `maxocontracts/blocks/` no tiene `sdv_e_validator.py`; `maxocontracts/core/axioms.py` tiene INV2 e INV2-S, no INV2-E |
| **El vector de pesos del SDV-E** (`PESOS_PISO` con el 0,020 del oxígeno **contado entre los que tienen piso**) | 🔴 **no existe como código**: hoy es **bloque de código propuesto** en documento 08 §5.2, no implementado | `grep` de `PESOS_PISO` sobre `maxocontracts/`: **cero coincidencias**; la tabla vive en [08_INV2-E_invariante.md](08_INV2-E_invariante.md) §5.2 |
| **Nombres de los parámetros de esta dimensión** (`agua_oxigeno_disuelto`, `agua_ph`, `aire_pm25_anual`, `aire_o3_temporada_alta`…) | 🔴 **no existen**: son propuesta del documento 08 y de este documento | ni una coincidencia en el código |
| **Sensores de agua** (sonda multiparamétrica, laboratorio, conductividad) | 🔴 **ninguno** | cero sensores, cero APIs, cero ingestores en `app/` |
| **Sensores de aire** (estación calibrada, red, teledetección de aerosoles) | 🔴 **ninguno** | ídem |
| Validación de **unidad** del dato de entrada (NO3-N ≠ NO3; CO en mg/m³) | 🔴 **no existe** | no hay ninguna capa que valide unidades: el endpoint hace `float(...)` crudo |
| Validación de **ventana** de promediado | 🔴 **no existe** | no hay campo de ventana en ningún modelo |
| Bandera de **proxy** declarado (aire OMS, nitrato FAO) | 🔴 **no existe** | no hay campo; el `aire` de la OMS entra hoy, si entrara, sin bandera |
| Índice de Salud Ecosistémica (ISE), que pondera esta dimensión al 40 % | 🟡 **documento, cero código** | `docs/architecture/metricas_detalle_kpis_oraculos_dinamicos.md` (IN-01) |
| Crédito regenerativo (`r_units` negativo) | 🟢 **implementado y probado** | `app/micromax.py` (docstring *«`r_units` NEGATIVO = credito regenerativo (EVV 1.2 s4.3)»*); `tests/test_micromax.py` con `-12.0` |
| Validación de `r_units` (techo, nota, evidencia, tercero, `NaN`/`inf`) | 🔴 **no existe** | acepta cualquier negativo; `NaN`/`inf` pasan el filtro; el endpoint hace `float(...)` crudo |
| Contabilidad del crédito (`SUM(r_units)`) y juez (INV2-E) | 🔴 **no existe** | es el agujero que esta biblioteca cierra; el precio además cierra en `max(0.0, …)` (`app/maxo.py`): nunca es negativo |
| Parte `eco-` y guardián oráculo | 🟢 **existen** | `app/parties.py` (`PARTY_TYPES`, `COLLECTIVE_PREFIXES`) y `app/contracts_bp.py` (`_guardian_approve_ecosystem`) |
| Quórum `eco-` N-de-M | 🔴 **no cableado** | el camino ecosistema retorna antes de la lógica de quórum; el canon no publica N ni M para el Reino Natural |
| Traducción TA↔TVI (PIU) | 🔴 **no ejecutable** | `PIU.valorar_ta_natural` es un `pass` con comentario (`docs/architecture/DISENO_IMPLEMENTACION_FUTURA.md`) |
| Incoherencia colateral heredable | ⚠️ **declarada, no heredada** | `resolve_participant_by_pid` asigna a una parte `eco-` **el SDV humano** (`sdv_actual=SDV()`), porque no existe SDV-E |

**Consecuencia honesta, y es la que este documento quiere dejar escrita:** el estándar de esta dimensión
**existe a partir de hoy** —con umbrales, ventanas, fuentes, protocolos y definiciones operativas de
violación—, y **la contabilidad no existe en absoluto**. Es exactamente el orden que el canon manda:
*«estándar primero, contabilidad después»* (Cap. 16.5 §16.5.14). Y el efecto inmediato de tener el
estándar es que el estado por defecto de cualquier unidad deja de ser una duda y pasa a ser un
**`indeterminado`** explícito: sin sensores, **no hay cumplimiento certificable y no hay crédito
regenerativo utilizable**.

---

## 13. Preguntas abiertas

Lo que **no** sé, y lo que esta biblioteca **contradice dentro de sí misma** y no me corresponde corregir
desde aquí.

1. **La corrección del texto de los documentos 07 y 08 sobre el oxígeno disuelto: ¿quién la ejecuta?** El
   criterio está fijado (§1.3) y las cifras verificadas, pero el **texto** del documento 08 §4.1 y su
   §4.2 (lista de dominios sin umbral) y la **fila de 7 días** del documento 07 §4.1 siguen diciendo lo
   anterior. Este documento no edita documentos de otra sesión: **los declara corregidos aquí y pide la
   corrección en la revisión de coherencia.** Mientras no ocurra, la biblioteca tiene dos estados vivos
   del mismo parámetro.
2. **El peso del oxígeno disuelto en el vector del piso, y la cifra de cobertura.** El documento 07 le da
   **0,000** en `PESOS_PISO`; el documento 12 propone **0,020 con piso**; el documento 08 **ya le asigna
   0,020 en su §5.2** (dentro de un vector cuya suma de grupos es 1,000) y sin embargo **lo marca 🔴 sin
   piso y no aclara si su 0,680 lo cuenta**. Este documento fija el criterio que hace posible el piso, y
   **corrige aquí su propia aritmética anterior**: no hay que sumar nada — **0,680 + 0,020 = 0,700 estaba
   mal**, porque el 0,020 ya está asignado; la cobertura declarada se queda en **0,680** si el documento 08
   ya lo contaba, o pasa a **0,700** si no. **No sé cuál es la cifra canónica**, y no la elijo desde aquí:
   pido que la revisión de coherencia (a) haga que el documento 08 publique **cuál de las dos lecturas es
   la suya** y (b) descarte **0,925**, que vuelve a sumar un peso ya contado (§5.4 y §5.6).
3. **El pH: dos pisos vivos en la biblioteca.** Los documentos 07 y 08 usan el rango agronómico de la FAO
   (6,5-8,4) como Mínimo Absoluto; los documentos 09 y 12 usan el rango de la EPA (6,5-9,0 / 6,5-8,5).
   Este documento fija el de la EPA y declara el de la FAO como referencia agronómica (§4, Dimensión 2),
   **pero la contradicción existe hoy y afecta a un rango entero**: con el criterio de la FAO, aguas
   duras y alcalinas ecológicamente sanas quedan en violación. Corregirlo pertenece a los documentos 07 y
   08.
4. **La aritmética de los dos vectores de pesos del documento 07.** Su tabla §5.3 suma **1,150**
   (`PESOS_TABLERO`) y **1,055** (`PESOS_PISO`), no 1,000 como declara su fila de suma ni como exige su
   propia propiedad F4 (§5.6). Y su cifra de cobertura **0,905** se calcula sobre un total de 1,000 que
   ese vector no tiene. **No renormalizo por mi cuenta** porque cambiaría el peso de toda la dimensión de
   agua y aire. Propongo, como **propuesta no ratificada**, reducir proporcionalmente los cinco bloques
   del ISE por el factor 0,85 para hacer sitio a caudal y conectividad —aire 0,200 → 0,170; agua
   0,200 → 0,170—, y que el documento 08 sea la fuente única de la cifra de cobertura.
5. **El nitrato: 07 dice «sin umbral», 08 le da un proxy con piso.** Las dos cosas son compatibles leídas
   con precisión (no hay umbral **ecológico**; sí hay **proxy agronómico declarado**), pero la biblioteca
   debe decirlo con esas palabras. **No sé si la intención del documento 07 fue negar el proxy o solo el
   umbral ecológico**, y por eso lo declaro en vez de interpretarlo.
6. **Cómo se reduce el catálogo de contaminantes a un número finito y auditable.** La tabla de la EPA
   publica decenas de valores por sustancia y el canon manda gobernanza operacionalmente finita
   (Cap. 10 §10.7). Propongo un procedimiento (§4, Dimensión 6) —lista cerrada por unidad, presión
   verificable, carga de la prueba sobre quien propone no medir— **y no propongo la lista**: elegirla es
   POLÍTICA y, sobre todo, **no puede elegirse sin los datos de presión de la unidad concreta**.
7. **La turbidez: el vacío numérico es real y una ruta está identificada pero no leída.** No hay valor
   universal y la fuente advierte contra usarlo como umbral; la OMS sí tiene un valor en sus Guías de
   agua de consumo, y la ruta que lo contiene está identificada y sirve el PDF real (4,11 MB, comprobado
   por cabecera) **pero no se descargó**. Es **el vacío más fácil de cerrar** en una sesión futura. Y si
   se cierra, hay que decidir algo que tampoco sé: **si un valor de agua de consumo puede entrar como
   referencia ecológica** o si es, otra vez, un error de categoría.
8. **El Óptimo del aire no existe, y eso es un hallazgo, no una carencia.** La OMS y el COMEAP declaran
   una relación sin umbral. **No invento un óptimo "más bajo"** y dejo la columna vacía con la marca. Lo
   que queda abierto es qué se vota entonces en el aire: propongo **la trayectoria** (qué IT, con qué
   plazo, con qué verificación) y **la prioridad de instrumentación**, pero **no sé si eso agota la
   columna de POLÍTICA** de esta dimensión.
9. **El grado de evidencia del aire: `[REPORTADO]` en los documentos 06 y 08, `[VERIFICADO]` aquí.** Las
   cifras son las mismas; la procedencia es mejor (**el «Annexe A» del COMEAP/UKHSA, que sí publica la
   tabla AQG y la comparación con 2005 —y que resultó ser una tabla numérica real, no la imagen de la
   página de la OMS**). **No me auto-ratifico el ascenso de grado**: es una decisión de la biblioteca, y
   de ella depende que una violación de aire sea **ejecutable** o quede como propuesta (documento 06 §D1:
   *«una cifra `[REPORTADO]` sostiene una propuesta, no una violación ejecutable»*). Queda también
   abierto —y **no lo cierra este documento**— si el grado debe declararse `[VERIFICADO]` en los
   documentos **06, 07 y 08** para que la biblioteca no sostenga dos grados del mismo número, y si la
   planilla de 14 secciones del documento 01 (Tabla 3.24, `[VERIFICADO]`) cuenta ya como lectura
   suficiente: **la decisión es de la revisión de coherencia, no de este documento**.
10. **La ventana de temporada alta del O3 no está en el catálogo de parámetros del documento 08**, aunque
    el documento 06 la nombra como ventana. ¿Se incorpora como **campo propio** (el recuento pasa de **19 a
    20** parámetros, o a **21** con el oxígeno) o como **ventana alternativa del mismo parámetro** (el
    recuento no cambia; el veredicto del O3 sí)? Recomiendo la segunda por la regla de no doble
    contabilidad, y **la decisión no es mía**. **Precisión de recuento, corregida aquí:** el documento 08
    §4.1 cuenta **19 parámetros con umbral, 18 de ellos con peso** —no 18 y 17—, así que la opción (a)
    parte de esa cifra y no de la que este documento publicaba antes.
11. **Quién elige la especie indicadora de la temperatura, y con qué carga de la prueba.** Propongo la
    **especie nativa más termosensible verificada** (§4, Dimensión 3) porque la alternativa —elegir la más
    tolerante— convierte el piso en una autorización. **No sé quién firma esa elección** en el
    procedimiento del SDV-E, y con los riesgos R4 y R13 abiertos esa firma podría quedar en manos de
    quien tiene interés en el resultado.
12. **La duración en TA bajo el piso.** Las fuentes dan ventanas de promediado y **una regla de
    instantaneidad** para el mínimo de 1 día del oxígeno (que uso como ancla `[HIPÓTESIS]`), pero
    **ninguna dice cuántos días bajo el piso constituyen violación persistente**. Es un vacío de decisión
    del proyecto, no de fuentes.
13. **La calidad del agua subterránea: sujeto admitido y sin instrumento.** La fuente que define el
    ámbito incluye los **ecosistemas dependientes de agua subterránea** `[VERIFICADO]`, y este documento
    los admite como sujetos. **No hay en la biblioteca ni un protocolo ni una fuente de umbral para
    agua subterránea**, y no la invento.
14. **Qué pasa con esta dimensión cuando el agua no está.** Si el río se seca —la pregunta del documento
    02 aplicada aquí—, la calidad **no se puede medir** y la violación es del **caudal** (documento 12),
    no de la calidad. **No sé si un cuerpo de agua seco debe declarar `indeterminado` en esta dimensión o
    un estado propio**, y la elección tiene consecuencia: `indeterminado` no bloquea por sí solo, y un
    río seco probablemente deba hacerlo.
15. **¿Un proxy puede bloquear un contrato?** El aire de la OMS es un proxy declarado de salud humana y
    el nitrato de la FAO un proxy agronómico. Si un proxy excedido bloquea con la misma fuerza que un
    umbral ecocéntrico, el SDV-E estaría gobernando el ecosistema con la salud del humano o con el
    rendimiento del cultivo. **Propongo que sí bloquee** (es lo más protector y es coherente con T14),
    **marcado como proxy en el registro**, pero **es una decisión doctrinal que no me corresponde**.
16. **La incertidumbre de las sondas de agua no está acotada.** No hay calibración interlaboratorio ni
    patrón de referencia en esta rama (el documento 06 §13 ya lo registró). Con la regla de
    declarabilidad, eso significa que hoy **una sonda de oxígeno o de pH registra y no declara
    violación**. Cerrar ese hueco no es una búsqueda de umbral: es una decisión de infraestructura.

---

## 14. Referencias

Solo URLs con estado HTTP real, medido con herramienta en la sesión de verificación de fuentes de esta
rama (`curl.exe -s -o NUL -w '%{http_code}' --max-time 20-25 -L`). Se indica el estado entre paréntesis.

### 14.1 Agua — criterios, hojas informativas y tablas

- US EPA, 1986 — *Quality Criteria for Water*, transcrito en la **hoja informativa de oxígeno disuelto**
  (EPA 841F21007B, julio 2021): OD de 30 días 5,5 / 6,5 mg/L; mínimo de 7 días 4,0 / 5,0; mínimo de 1 día
  3,0 / 4,0; *Early Life Stages* 6,0 / 9,5 y 5,0 / 8,0; anoxia < 0,2; criterios basados en el mínimo que
  necesitan los peces de agua dulce; protocolo de medición y advertencias de salinidad y altitud (200):
  https://www.epa.gov/system/files/documents/2021-07/parameter-factsheet_do.pdf
- US EPA, 2021 — **hoja informativa de pH**: fluctuación diaria de una charca bien tamponada 7,0-8,4; los
  metales son más solubles a pH bajo; por encima de 8,5 aumenta la forma tóxica del amoníaco; la mayoría
  de los huevos de pez no eclosionan por debajo de pH 5 (200):
  https://www.epa.gov/system/files/documents/2021-07/parameter-factsheet_ph.pdf
- US EPA, 2021 — **hoja informativa de turbidez**: criterio narrativo de la EPA 1986 (**no reducir más de
  un 10 %** del punto de compensación); la competencia de fijar el número es de los Estados y tribus; advertencia
  contra usar la turbidez como umbral (200):
  https://www.epa.gov/system/files/documents/2021-07/parameter-factsheet_turbidity.pdf
- US EPA, 2021 — **hoja informativa de temperatura**: *«challenging to set water quality criteria for
  water temperature»*; Tabla 2 de valores por especie (crecimiento, desove, embrión, exposición corta) de
  la EPA 2012; advertencia de que son ejemplos y no valores protectores universales (200):
  https://www.epa.gov/system/files/documents/2021-07/parameter-factsheet_temperature.pdf
- US EPA — **tabla nacional de criterios recomendados de calidad del agua para la vida acuática**:
  pH 6,5-9,0 (dulce) · 6,5-8,5 (salada) · ±0,2 en océano abierto; la fila del oxígeno disuelto **sin
  celdas numéricas** (remite al *Gold Book* de 1986); decenas de valores por sustancia (arsénico
  340/150 µg/L CMC/CCC) (200):
  https://www.epa.gov/wqc/national-recommended-water-quality-criteria-aquatic-life-criteria-table
- US EPA — **tabla de criterios organolépticos** (sabor y olor): lista *«Color»* y *«Tainting
  Substance»* como NP (sin valor numérico) y **no incluye la turbidez** (200):
  https://www.epa.gov/wqc/national-recommended-water-quality-criteria-organoleptic-effects
- US EPA — **índice de las hojas informativas de parámetros de calidad del agua** (la puerta de entrada a
  las cuatro hojas anteriores) (200): https://www.epa.gov/awma/factsheets-water-quality-parameters
- US EPA — **contaminación por nutrientes**: la agencia **no publica criterios numéricos nacionales de
  nutrientes**, publica documentos **por ecorregión y por tipo de masa de agua** (200):
  https://www.epa.gov/nutrientpollution ·
  https://www.epa.gov/nutrientpollution/epas-recommended-ambient-water-quality-criteria-nutrients
- FAO, 1985/1994 — Ayers & Westcot, *Water quality for agriculture*, Papel 29 Rev.1, §5.1 y §5.2:
  nitrato < 5 mg/L NO3-N sin efecto sobre el cultivo, > 5 afecta a cultivos sensibles, > 30 techo práctico;
  efecto ecológico cualitativo (proliferación de algas); concentraciones observadas; **convención de
  unidades** (10 mg/L N = 45 mg/L NO3 = 13 mg/L NH4); rango normal de pH del agua de riego 6,5-8,4 (200):
  https://www.fao.org/3/t0234e/T0234E06.htm · https://www.fao.org/3/t0234e/T0234E01.htm
- FAO — **Portal de Suelos**, clasificación de aguas salinas por conductividad (< 0,7 dS/m no salina;
  0,7-2 leve; 2-10 moderada; 10-25 alta; 25-45 muy alta; > 45 salmuera) y techo agronómico de 10 dS/m.
  **Clasificación de aptitud para el riego: se cita como referencia agronómica, no como piso de
  integridad ecológica ni como valor de potabilidad** (§4, Dimensión 7) (200):
  https://www.fao.org/soils-portal/soil-management/management-of-some-problem-soils/salt-affected-soils/more-information-on-salt-affected-soils/technical-issues/en/
- FAO AQUASTAT (portal de datos de agua; **sin umbral leído**) (200): https://www.fao.org/aquastat/en/
- Agencia Europea de Medio Ambiente (AEMA), 2025 — **nutrientes en el agua dulce de Europa**: nitrato
  medio > 2,93 mg NO3-N/l en más del 50 % de las masas de agua de Bélgica y Dinamarca y 40-50 % en
  Chequia, Alemania y Lituania (2018-2023) (200):
  https://www.eea.europa.eu/en/analysis/indicators/nutrients-in-freshwater-in-europe
- Agencia Europea de Medio Ambiente (AEMA), 2025 — **sustancias consumidoras de oxígeno en los ríos
  europeos**: la DBO se redujo a la mitad del nivel de 1992 y fluctúa en 2,0-2,2 mgO₂/l desde 2010; clase
  «mejor» < 1,61 mg/l; amonio estabilizado por debajo de 0,08 mg NH4-N/l; **cadena causal** de la
  contaminación orgánica y efecto del aumento de temperatura (200):
  https://www.eea.europa.eu/en/analysis/indicators/oxygen-consuming-substances-in-european-rivers
- Declaración de Brisbane (2018) sobre caudales ambientales, publicada en *Frontiers in Environmental
  Science* (Arthington *et al.*): definición del caudal ambiental como **cantidad, ritmo y
  calidad** y ámbito de los ecosistemas acuáticos (ríos, manantiales, riberas, humedales de llanura de
  inundación, lagos, aguas costeras, lagunas, estuarios y ecosistemas dependientes de agua subterránea)
  (200): https://www.frontiersin.org/journals/environmental-science/articles/10.3389/fenvs.2018.00045/full
- Comisión Europea — **Directiva Marco del Agua** (el «buen estado» como objetivo jurídico; **sin los
  valores numéricos del Anexo V en el HTML**) (200):
  https://environment.ec.europa.eu/topics/water/water-framework-directive_en
- WISE-Freshwater — sistema de información del agua en Europa (**páginas de navegación, sin umbrales**)
  (200): https://water.europa.eu/freshwater/europe-freshwater/water-framework-directive

### 14.2 Aire — Directrices mundiales de la OMS (2021)

- OMS, 2021 — *WHO global air quality guidelines: particulate matter (PM2.5 and PM10), ozone, nitrogen
  dioxide, sulfur dioxide and carbon monoxide* — **página oficial de publicación** (la tabla de valores se
  sirve como **imagen**, no como texto) (200): https://www.who.int/publications/i/item/9789240034228
  · y el mismo organismo para los **objetivos interinos (IT-1…IT-4) y la cifra de ~300 000 muertes
  anuales del IT-1**, que **no** están en el anexo del COMEAP: hoja informativa de aire ambiente y
  preguntas y respuestas oficiales de las directrices (200).
- COMEAP / UKHSA (Reino Unido), julio 2022 — **respuesta a las Directrices de la OMS 2021, Anexo A**:
  tabla completa de valores AQG y objetivos interinos (PM2.5 5 anual y 15 a 24 h; PM10 15 y 45; O3 60 de
  temporada alta y 100 a 8 h; NO2 10 y 25; SO2 40; CO 4 mg/m³) y la advertencia de que **los valores de
  guía no son umbrales por debajo de los cuales no hay impactos** (relación lineal o supralinear sin
  umbral) (200):
  https://www.gov.uk/government/publications/comeap-statement-response-to-who-air-quality-guidelines-2021/comeap-statement-response-to-publication-of-the-world-health-organization-air-quality-guidelines-2021
- OMS, 2024 — **hoja informativa sobre el aire ambiente (exterior) y la salud**: 99 % de la población
  mundial (2019) por encima de los niveles de las guías; 6,7 millones de muertes prematuras anuales (aire
  ambiente + doméstico) y 4,2 millones (solo aire ambiente), 89 % en países de ingresos bajos y medios;
  alcanzar el IT-1 de PM2.5 (35 µg/m³) salvaría ~300 000 muertes anuales; declaraciones cualitativas sin
  cifra para carbono negro, partículas ultrafinas y polvo desértico (200):
  https://www.who.int/news-room/fact-sheets/detail/ambient-(outdoor)-air-quality-and-health

### 14.3 Fuentes descartadas en esta dimensión (no citables)

**Muertas (404 o 000): no se cita de ellas ninguna cifra.** Se listan porque **una de ellas es la causa
raíz de la disputa 07/08** y porque declararlas es la mitad de la resolución:

| Ruta | Estado | Por qué se descarta |
|---|---|---|
| `epa.gov/wqc/aquatic-life-criteria-dissolved-oxygen` | **404 — muerta** | **Es la URL del documento 08.** Su 404 es cierto; la conclusión que se extrajo de él, no (§1.3) |
| `epa.gov/wqc/dissolved-oxygen-water-quality-standards` | **404 — muerta** | ruta supuesta de «estándares de oxígeno disuelto» |
| `epa.gov/wqs-tech/water-quality-standards-policy-and-guidance` | **404 — muerta** | política y guía de estándares de calidad del agua |
| `epa.gov/wqc/nutrients` | **404 — muerta** | ruta de nutrientes dentro de `/wqc`; la viva está citada arriba y **no publica valores numéricos nacionales** |
| `epa.gov/system/files/documents/2021-07/parameter-factsheet_nitrogen.pdf` | **404 — muerta** | **no existe hoja informativa de nitrógeno en la serie** (existen OD, pH, turbidez y temperatura): por eso el nitrato no tiene fuente EPA |
| `epa.gov/system/files/documents/2021-07/parameter-factsheet_phosphorus.pdf` | **404 — muerta** | ídem para el fósforo: **el fósforo queda sin fuente numérica** |
| Hojas químicas de nitrato de la OMS en `who.int/water_sanitation_health/dwq/chemicals/` (varias rutas) | **404 — muertas** | se probaron y ninguna existe: **no se transcribe ninguna cifra de la OMS para nitrato** |
| `eea.europa.eu/en/analysis/indicators/river-oxygen-consuming-substances` | **404 — muerta** | ruta corta del indicador de oxígeno; la viva está citada arriba |
| `iris.who.int` (rutas del repositorio institucional) | **200 que no entrega el documento** | el repositorio migró a una SPA: devuelve una cáscara HTML de 755 bytes (**no es un PDF**); otras dos descargas fallaron. **Un 200 que no entrega el documento no es una fuente** (Regla 2) |
| Ruta del PDF de las Guías de agua de consumo de la OMS (bitstream de 4,11 MB) | **identificada y no descargada** | responde y sirve el PDF real, pero **no se descargó** por la regla de eficiencia de la sesión: es el **vacío más fácil de cerrar** (§13, pregunta 7) |
| Directiva (UE) 2020/2184 de agua de consumo (`eur-lex.europa.eu`, CELEX 32020L2184) | **200 sin cuerpo servido** | el fetch devuelve solo el título: **no se cita ningún valor de esta Directiva** |

**Bloqueadas para agentes automáticos (403): son reales y un humano las abre.** `unep.org`
(`/explore-topics/water` y su ruta de monitoreo de calidad del agua —**el vacío institucional más
relevante de esta dimensión: UNEP es el organismo natural para el oxígeno y los nutrientes, y bloquea**—),
`unwater.org` (incluida `/water-facts/water-quality`) y `unece.org/environment-policy/water`. **No se cita
de ellas ninguna cifra que no se haya podido leer.**

### 14.4 Referencias internas al canon (por sección, sin anclas de línea)

- **Cap. 10 §10.4** — El SDV Universal: *SDV para Ecosistemas* (calidad del aire y agua) y *SDV para
  Lugares* (calidad del agua: oxígeno, pH, contaminantes).
  `docs/book/edicion_3_dinamica/capitulo_10_tres_reinos_260126.md`
- **Cap. 10 §10.3** — Principio Precautorio de Consciencia: *«Donde hay duda de consciencia, se asume
  consciencia.»*
- **Cap. 10 §10.6** — Dignidad encadenada: *«Dignidad Humana ←→ Dignidad Ecosistémica ←→ Dignidad
  Material. Cada eslabón depende de los demás.»*
- **Cap. 10 §10.7** — Gobernanza operacionalmente finita: *«La gobernanza debe ser operacionalmente
  finita.»*
- **Cap. 16.5 §16.5.14** — El hogar extendido: convivencia bidireccional, la Zona Libre inefable, *«el
  suelo antes que el saldo»*, la sentencia de INV2-E, el TA y el PIU como traductor, las partes `eco-` y
  el guardián oráculo. `docs/book/edicion_3_dinamica/capitulo_16_5_micromaxocracia_canonica_220826.md`
- **Cap. 5 §5.5** — PIU (Protocolo de Intercambio Universal), único traductor TA↔TVI.
- **Cap. 5** — T14 (Principio de Precaución Intergeneracional).
- **Axioma 0 — Directiva Mayor:** *«resolver nuestras necesidades de la mejor manera para todos todos»*
  —humanos, naturales y sintéticos, presentes y futuros—. **T9 — No-antropocentrismo.**
  **T13 — Transparencia de Cálculo.** **T16 — Minimizar Daño.**
- **Cap. 8 §8.11** — Dimensiones binarias sin peso (precedente de las dimensiones VIII y IX del SDV-H).
- **EVV-1.2 §4.3** — Componente R: *«$R_{regenerado}$ (Crédito Regenerativo)… Permite valores
  negativos.»*

### 14.5 Referencias internas al repositorio (biblioteca y código)

- Documento 06 de esta biblioteca — Elenco de sensores y verificación T13: [06_Medicion_y_verificacion_T13.md](06_Medicion_y_verificacion_T13.md)
- Documento 07 de esta biblioteca — Fórmula de violación y pesos: [07_Formula_de_violacion_y_pesos.md](07_Formula_de_violacion_y_pesos.md)
- Documento 08 de esta biblioteca — INV2-E, el invariante ejecutable: [08_INV2-E_invariante.md](08_INV2-E_invariante.md)
- Documento 09 de esta biblioteca — Comparativa inter-reinos: [09_Comparativa_inter_reinos.md](09_Comparativa_inter_reinos.md)
- Documento 12 de esta biblioteca — Ríos y cuencas (caudal, oxígeno por etapa de vida, temperatura por
  clase piscícola): [12_Ecosistemas_Rios_y_cuencas.md](12_Ecosistemas_Rios_y_cuencas.md)
- Índice de Salud Ecosistémica (IN-01), con los pesos 30/20/20/15/15 y sus bandas:
  [metricas_detalle_kpis_oraculos_dinamicos.md](../../architecture/metricas_detalle_kpis_oraculos_dinamicos.md)
- Riesgos abiertos R4, R6 y R13: `docs/architecture/blindaje_anti_gamificacion_equidad.md`
- Crédito regenerativo implementado: `app/micromax.py` · `tests/test_micromax.py`
- Guardián oráculo del ecosistema: `app/contracts_bp.py` (`_guardian_approve_ecosystem`)
- Partes `eco-`: `app/parties.py` (`PARTY_TYPES`, `COLLECTIVE_PREFIXES`)
- Motor — déficit normalizado y severidad: `maxocontracts/blocks/sdv_validator.py`
- Motor — patrón SDV-S y corrección de la base neutra: `maxocontracts/core/types.py`

### 14.6 Registro de correcciones (revisión adversarial, octubre 2026)

T13 se aplica al propio documento: **una corrección se registra como corrección**, con la ruta consultada
y su estado HTTP. Las 22 URLs citadas en §14.1 y §14.2 se re-comprobaron con `curl.exe -s -o NUL -w
'%{http_code}' --max-time 25 -L` y **todas respondieron 200**, incluida la ruta que sostiene la disputa
—`epa.gov/wqc/aquatic-life-criteria-dissolved-oxygen`, **404 confirmado de nuevo**—; **no hay ninguna URL
inventada, malformada ni muerta en este documento**. Lo que cambió en el texto, y por qué:

| # | Dónde | Qué decía | Qué dice ahora | Prueba |
|---|---|---|---|---|
| 1 | §5.4, §5.5, §13.2 | La cobertura del piso «pasaría de 0,680 a **0,700**» al ratificar el piso del oxígeno | **0,680 o 0,700 según cómo el documento 08 lea su propia fila**, porque el **0,020 del oxígeno ya está en su vector** (§5.2) y su 0,680 puede ya contarlo; **0,925 queda descartado** | documento 08 §5.2: grupos aire 0,20 · agua 0,18 · **oxígeno 0,02** · biodiversidad 0,30 · suelo 0,15 · caudal 0,075 · conectividad 0,075 = 1,000; «suma de los que tienen piso **0,680**» |
| 2 | §5.5, §13.10 | El catálogo del documento 08 «lista **18** parámetros (17 con peso)» | **19 (18 con peso)** | documento 08 §4.1, párrafo de recuento |
| 3 | §4, Dimensión 1 | «Tres jurisdicciones, **el mismo número**»: la UE con 9/7 y 8/5 | **CCME coincide en los cuatro valores; la UE coincide en la zona de protección y no en el instrumento** (porcentaje de muestras, valores obligatorios y de guía, Directiva **derogada**) | documento 12 §Dimensión II y §14.1 |
| 4 | §4, Dimensión 3 y §5.8 | El ejemplo calculaba `(22−19)/19` **sin declarar que el operador no interpola** | Se declara que el **0,1579 es proporción del proyecto** sobre un operador `escalonado` cuyos niveles son techos publicados | documentos 07 §3.3 y 08 §5.1: «toma el nivel alcanzado; **no interpola**» |
| 5 | §3 (pilar 1) y §4, Dimensión 4 | «Los 50 mg/L de nitrato (OMS)» sin fuente en §14 | Se declara `[SIN FUENTE VERIFICADA]` **en esta rama** y se nombra como **categoría de error, no como dato** | §14.3: cuatro rutas de hojas químicas de nitrato de la OMS, **404** |
| 6 | §4, Dimensión 7 | La FAO clasificaba el agua como «apta para agua de **bebida** y riego» | **Aptitud para el riego**; la potabilidad no la publica esa fuente | FAO Portal de Suelos (200): clasificación de aguas salinas para uso agrícola |
| 7 | §4, Dimensión 5 y §5.8 | «**≤ 10 %** de reducción» del punto de compensación | «**< 10 %**»: la fuente dice que **no** debe reducirse **más de un 10 %** | hoja informativa de turbidez (200) |
| 8 | §3 (pilar 7) | «(la FAO es más estricta)» | Las dos bandas **no se ordenan por laxitud** (6,5-8,4 no contiene ni es contenida por 6,5-9,0 / 6,5-8,5) | tabla de la EPA (200) y FAO §5.2 (200) |
| 9 | §1.2 y §14.2 | El «Anexo A» del COMEAP/UKHSA transcribía «la tabla completa» | Transcribe **los AQG y la comparación con 2005**; los **IT y las ~300 000 muertes** salen de la OMS y así se citan | fetch del anexo (200): no publica IT |
| 10 | §5.6 | La tabla del documento 07 «conservó los cinco pesos del ISE tal cual» | El agua **se subdivide** (0,180 + 0,020) y especies clave no tiene fila propia; lo que se añadió sin quitar nada fue **caudal y conectividad** | documento 07 §5.3, filas 3 y 4 |
| 11 | §12 (tabla de estado) | No había fila para los pesos | Fila nueva: `PESOS_PISO`/`SDV_E` **no existen en código**; son bloque propuesto en el documento 08 §5.2 | `grep` de `PESOS_PISO` y `SDV_E` en `maxocontracts/`: **cero coincidencias** |
| 12 | §13.9 | El ascenso de grado del aire no mencionaba los otros documentos | Se declara que **06 y 08 mantienen `[REPORTADO]`** y que la conciliación —incluido el documento 01— pertenece a la revisión de coherencia | documentos 06 §D1 y 08 §4.1 |

---

## Anexo — Autoevaluación contra el checklist del brief

| Punto del checklist | Estado |
|---|---|
| Plantilla de 14 secciones | ✅ las 14 |
| Mínimo Absoluto separado del Óptimo | ✅ en cada una de las 8 dimensiones, y en la tabla resumen §4.9 |
| Cada cifra con fuente + año, y URL en Referencias | ✅ §14 (o marca literal de vacío) |
| URLs verificadas, cero inventadas | ✅ solo las de la sesión de fuentes de la rama; las muertas van declaradas en §14.3 |
| Marcas `[VERIFICADO]` / `[REPORTADO]` / `[HIPÓTESIS]` | ✅ en todo el texto, y §1.2 explica el único ascenso de grado |
| Canon citado por sección, sin anclas de línea ni rutas absolutas locales | ✅ §14.4 |
| Preámbulo metodológico presente | ✅ §2 (ocho reglas) |
| Zona Libre explícita | ✅ §10, con la distinción entre límite doctrinal y cobertura faltante |
| LEY (no votable) frente a POLÍTICA (votable) | ✅ §4.3, §4.9, §5, §13 |
| §12 honesta, con 🔴 donde no hay código | ✅ dieciséis filas, doce 🔴 |
| §13 dice lo que no sé, sin fingir cierre | ✅ dieciséis preguntas abiertas, cinco de ellas contradicciones reales de la biblioteca |
| Frases prohibidas evitadas; axiomas sin definir de más | ✅ |
| El documento aporta algo que no está en el canon, sin contradecirlo | ✅ véase abajo |

**Los cinco aportes de este documento, en una lista, para que se puedan discutir uno por uno:**

1. **La resolución de la disputa del oxígeno disuelto, con el reparto LEY/POLÍTICA que la propia fuente
   permite** (§1.3): el piso son los criterios de *Other Life Stages* (supervivencia) y la plenitud los de
   *Early Life Stages* (reproducción), con la corrección del etiquetado de etapa de vida del documento 07
   y con la convergencia de tres jurisdicciones (US EPA, CCME, UE) sobre **la misma zona de protección**
   —el CCME con los cuatro valores idénticos; la UE con un instrumento distinto, declarado en §4—.
2. **La separación del agua como caudal y el agua como calidad, con la frontera publicada por la fuente
   del caudal** (§4.2): cantidad, ritmo y calidad son el mismo concepto en la definición vigente, lo que
   convierte al documento 23 en complemento normativo del 12 y no en su anexo —y elimina la duda de doble
   contabilidad: caudal y calidad son parámetros distintos de la misma masa de agua—.
3. **Los umbrales de agua que el documento 06 §D2 declaró ausentes, ahora con fuente primaria** (pH de
   vida acuática 6,5-9,0 / 6,5-8,5; el pH como **modulador de toxicidad** y condición de validez de la
   medición de contaminantes; la temperatura **por especie indicadora** con la regla de elegir la más
   termosensible; el nitrato como vacío ecológico con su **convención de unidades** que decide
   violaciones; la turbidez como **criterio narrativo auditable** que la fuente prohíbe convertir en
   umbral).
4. **La declaración de que el Óptimo del aire no existe, y qué se vota en su lugar** (§4, Dimensión 8;
   §13 pregunta 8): la OMS declara una relación sin umbral, de modo que el aire se gobierna con piso y
   **trayectoria**, no con plenitud —y el déficit se satura en 0 porque «mejor que la guía» no es un
   excedente canjeable—.
5. **La aritmética de los vectores de pesos de la biblioteca, publicada en vez de tapada** (§5.4, §5.6 y
   §13 preguntas 2 y 4): la tabla del documento 07 suma 1,150 y 1,055 y no 1,000; su 0,905 no es
   derivable; **el 0,020 del oxígeno ya está asignado en el vector del documento 08**, de modo que la
   cobertura declarada **no sube a 0,700 por una suma** —queda en 0,680 o 0,700 según cómo el 08 lea su
   propia fila, y 0,925 queda descartado—. La primera versión de este documento proponía 0,700: **se
   corrige aquí** (§14.6, corrección 1), y ninguno de esos números se renormaliza desde aquí: se publican
   con la aritmética a la vista para que la revisión de coherencia decida con ellos delante.

Y una cosa que este documento **no** aporta, para que no se le atribuya: **no cierra el hueco de
medición**. Los umbrales de agua y aire ya tienen fuente; los sensores siguen sin existir. Mientras no
existan, la respuesta correcta del sistema para cualquier masa de agua y cualquier aire del planeta es
`indeterminado` —y eso, hoy, es un resultado honesto y no un fracaso.
