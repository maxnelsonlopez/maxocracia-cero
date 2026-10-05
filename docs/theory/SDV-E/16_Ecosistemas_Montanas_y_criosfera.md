# Ecosistemas de montañas y criosfera
## Los mínimos del hielo, del suelo congelado y del piso altitudinal: cuando el piso no es una cantidad, sino la persistencia de un régimen

**Autoría:** Oráculo Sintético DeepSeek & Max Nelson López Restrepo
**Fecha:** octubre 2026
**Proyecto:** Maxocracia — El gobierno de la verdad, el tiempo y la vida
**Licencia:** Creative Commons BY-SA 4.0
**Estado:** Propuesta de estándar (rama SDV-E, Ola 4) — NO canon hasta ratificación
**Referencia canónica:** Cap. 10 §10.4 · Cap. 16.5 §16.5.14 · EVV-1.2 §4.3 · Cap. 9.5 (precedente SDV-S)
**Documento:** 16 de la biblioteca `docs/theory/SDV-E/`

---

## 1. Qué es (y qué no es) este SDV

**Qué es.** Este documento fija los mínimos por debajo de los cuales una **unidad ecológica de
montaña y criosfera** pierde integridad: el balance de masa de sus glaciares, el régimen térmico de
su permafrost, la extensión de sus pisos altitudinales, la comunidad criófila que los habita y la
regulación hídrica que su cabecera de cuenca entrega aguas abajo. Es el estándar del único ecosistema
del SDV-E **cuyo sujeto principal es un sólido que se está convirtiendo en líquido**, y cuya pérdida
no se mide en hectáreas sino en masa, en régimen térmico y en tiempo.

**Qué no es.**

- **No es un documento de umbrales publicados.** Es lo contrario, y hay que decirlo en la primera
  página: la criosfera es **el ecosistema del SDV-E donde la ausencia de umbrales normativos es más
  radical** —la búsqueda de esta sesión no encontró, para balance de masa glaciar, área mínima de
  ecosistema alpino viable ni caudal ecológico de cabecera glaciar, ningún valor publicado del tipo
  «el mínimo aceptable es X»—. Otros ecosistemas del SDV-E sí disponen de algún valor normativo, en
  general de calidad de agua o de aire, propiedad de los documentos 12, 14 y 23. De la criosfera, la
  literatura publica *series de estado* (balance de masa, temperatura de permafrost, área
  de piso) y *proyecciones*. No existe —no se encontró en la sesión de verificación de esta rama— un
  valor publicado del tipo «el balance de masa mínimo aceptable de un glaciar es X». Por tanto, la
  columna **Mínimo Absoluto** de casi todas las dimensiones de este documento se construye como
  `[HIPÓTESIS]` explícita del proyecto, anclada en constantes físicas verificadas. **Ocultarlo sería
  inventar**, y este documento no inventa.
- **No es el estándar de todos los ecosistemas de altura.** La montaña es, además, pradera, bosque,
  suelo vivo, río y zona árida. Este documento cubre **lo que solo existe en la montaña y en el
  frío**: glaciares, permafrost, pisos altitudinales y cabeceras de cuenca. Lo demás pertenece a los
  documentos 10 (bosques), 12 (ríos y cuencas), 14 (suelos vivos), 15 (praderas) y 17 (zonas áridas)
  de esta biblioteca, y **no se duplica aquí**.
- **Y deja dos dimensiones canónicas fuera, a propósito y por escrito.** El canon define el SDV-E por
  *"caudal ecológico, biodiversidad, **conectividad**, **ciclos naturales**"*
  (`docs/theory/SDV_Suelo_Dignidad_Vital_importancia_MaxoContracts.md`) y el Cap. 10 §10.4 pide
  *"Ciclos naturales respetados (fuego, inundación, sequía)"*. **Ninguna de las dos aparece como
  dimensión de este documento**, y decir cuál es su dueño no es una excusa sino una obligación de
  frontera: la conectividad pertenece al documento 21 (Transversal Conectividad) y los ciclos al
  documento 22 (Transversal Ciclos naturales). La montaña aporta aquí lo que esos transversales no
  pueden aportar
  por sí solos —**el régimen térmico, la masa y el piso altitudinal**—; su fragmentación y su régimen
  de perturbaciones se declaran **fuera de alcance**, no silenciados.
- **No es un documento de contabilidad.** Es el *estándar primero*; la contabilidad viene después
  (Cap. 16.5 §16.5.14). Hoy el crédito regenerativo (`r_units` negativo) está implementado y probado,
  e **INV2-E no existe**: se puede acumular crédito mientras el ecosistema se degrada y el sistema no
  lo detecta. Esta biblioteca es el juez que falta.
- **No es canon.** Es una propuesta de estándar de la rama SDV-E, Ola 4, **no ratificada**.

**El hallazgo de apertura, y es incómodo.** Búsqueda exhaustiva sobre el canon escrito
(`docs/book/edicion_3_dinamica/`, los veintiséis archivos del directorio, incluido el libro completo
compilado): la palabra *glaciar* no aparece **ni una vez**. *Criosfera*, cero. *Permafrost*, cero.
*Montaña* aparece una sola vez, y es una lista:
*"**Naturaleza Mineral**: Ríos, montañas, océanos, atmósfera, suelos"* (Cap. 10). El canon nombra la
montaña como **sustantivo de una enumeración**, no como sujeto con condiciones de funcionamiento.
Consecuencia que este documento asume sin dramatizarla: **el SDV-E de la criosfera no hereda ni una
sola decisión doctrinal previa del proyecto**; hereda el método (Cap. 16.5 §16.5.14), la estructura
del SDV-H, el precedente del SDV-S y el axioma T14 — nada más. Es el documento de esta biblioteca con
menos canon detrás y más física delante. [VERIFICADO: lectura directa del repositorio en esta sesión]

**Marcas de evidencia usadas en todo el texto.** `[VERIFICADO]` = cifra leída en la fuente citada y
con URL con estado HTTP comprobado en la sesión de verificación de esta rama. `[REPORTADO]` = dato
afirmado por una fuente que se cita sin haber podido abrir el documento primario. `[HIPÓTESIS]` =
inferencia razonada del proyecto —normalmente **la conversión de un valor de estado en un umbral
normativo**, que es exactamente lo que la literatura científica no hace—. `[SIN FUENTE VERIFICADA —
pendiente de consenso científico]` = se buscó el umbral y no existe fuente verificable. Las cuatro
marcas son resultados legítimos, y la cuarta es un resultado de primera clase.

**Trazabilidad.** La verificación de fuentes de este documento vive en el registro de trabajo
`scratch/sdv_e/fuentes/16_montanas.md` (documento de trabajo, **no** de la biblioteca): **30 URLs con
estado 200 verificado**, 6 bloqueadas a agentes automáticos (403 — reales, no verificables por este
medio) y 5 muertas descartadas. La suma no cuadra con el total de filas de §14 porque las 403 **no
cuentan** como fuentes verificadas: son fuentes *citadas* (Körner & Paulsen vía Wiley, ICIMOD, IUCN
Red List) que este documento nombra declarando su estado y sin atribuirles ninguna cifra no leída. Las
afirmaciones sobre el código de la sección 12 se verificaron **por lectura directa del repositorio en
esta sesión**, no por URL. Todo enlace citado aquí se re-comprueba con
`scripts/verificar_enlaces_sdv_e.py`.

---

## 2. Preámbulo metodológico

El SDV-H lo tiene; el SDV-S lo omitió y el brief de esta biblioteca prohíbe repetir la omisión. Aquí
es obligatorio por una razón adicional: **este es el primer documento del SDV-E cuyo piso no se puede
copiar de una norma, porque no hay norma**. Seis reglas gobiernan lo que sigue.

**Regla 1 — Separar siempre valor de estado de umbral normativo.** Un balance de masa de
−1,374 m w.e./año medido en 2023/24 **no es un umbral**: es una medición. Un umbral es una decisión
normativa que dice *a partir de aquí hay violación*. Cuando este documento convierte una medición en
umbral, lo marca `[HIPÓTESIS]` y dice de qué constante física lo ancla. La distinción es la columna
vertebral del documento: sin ella, este texto sería una serie de datos disfrazada de estándar.

**Regla 2 — El piso es LEY y no se vota; la plenitud es POLÍTICA y se vota.** Es la regla que el brief
marca como crítica y el error histórico del SDV-H (confundir el Óptimo del agua con su Mínimo
Absoluto). Precedente operativo del Parlamento Educativo (INV2-EDU, categoría `critical`: quórum
60 %, consenso 75 %, T13, anti-flip-flop 14 días, `CHECK` en BD): la ley vive en el motor y **no es
votable**; la plenitud aspiracional **sí es votable**. En este documento hay un caso nuevo y extremo
de esa separación, y se declara en §5.4: **en la criosfera el piso y la plenitud coinciden en el
mismo número.**

**Regla 3 — No hay trasvase de umbrales entre unidades ni entre pisos.** Un umbral de caudal
ecológico no se hereda de un río a un glaciar; un piso de área no se hereda del piso alpino al piso
nival. Cada dimensión de §4 se justifica por su propia fuente y su propia física.

**Regla 4 — Distinguir cuatro cosas que se confunden siempre.** (a) No existe el umbral en la
literatura; (b) existe y no lo verifiqué; (c) existe, lo verifiqué y es una proyección, no una norma;
(d) existe y es norma publicada. En este documento: (a) es el caso del área mínima de ecosistema
alpino viable y del equivalente en agua de la nieve; (b) no aplica, no se cita nada sin verificar;
(c) es el caso de la reducción de caudal (≥ 10 % en un mes de deshielo) y del área de permafrost a
2100; (d) es **un solo caso en todo el documento**: la definición de permafrost (≤ 0 °C durante
≥ 2 años consecutivos, IPA). El lector debe saber que **la criosfera entra al SDV-E con una sola
norma publicada y cinco pisos construidos**.

**Regla 5 — El tiempo del sujeto manda.** El tiempo de este ecosistema es **TA (Tiempo Absoluto)**, no
TVI ni TPI, y no se coloniza: *"la contabilidad doméstica no coloniza el tiempo ajeno. El PIU (Cap. 5
§5.5) es quien traduce entre TA y TVI; nosotros registramos la interacción, no la vida interna del
ecosistema"* (Cap. 16.5 §16.5.14). Aquí la regla es literal y no retórica: el intervalo de remedición
de una cumbre es de **5 a 10 años**, una serie glaciar no constituye sujeto medible antes de
**30 años** y el permafrost rico en hielo tarda **siglos a milenios** en desaparecer. **Ninguna de
esas tres cifras fue fijada pensando en un ejercicio contable humano**, y ese es precisamente el
punto. §5.3 propone el criterio verificable para comprobarlo.

**Regla 6 — La gobernanza debe ser operacionalmente finita (Cap. 10 §10.7).** El SDV-E de la montaña
**no puede** exigir modelar la cadena trófica alpina ni el ciclo completo del carbono del permafrost
para decidir. El protocolo de §6 se elige, entre los científicamente válidos, por su coste declarado:
el diseño básico de cumbres de GLORIA cuesta **12 a 25 días de trabajo de un equipo de 4 personas**
cada 5-10 años. Eso es un estándar que se puede cumplir; un modelo global del criosistema, no.

**Corolario de honestidad.** Donde este documento no sabe, lo dice con la marca correspondiente y lo
repite en §13. Un documento que admite «no lo sé» vale más que uno que aparenta cerrar todo.

---

## 3. Pilares epistemológicos

Cinco pilares sostienen este estándar. Los cuatro primeros son heredados; **el quinto es propio de la
criosfera y es el que organiza todo el documento**.

1. **Proporcionalidad (Cap. 10 §10.5).** El nivel de protección debe ser *"lógico, proporcional y
   adecuado a la naturaleza de la entidad"*. Un glaciar no recibe el mismo trato que una persona: no
   se le rehabilitan derechos ni se le pide consentimiento verbal. Recibe el trato que su naturaleza
   exige — y su naturaleza es **termodinámica**. Esto no es una metáfora: es la razón por la que sus
   umbrales se expresan en °C, en kg/m² y en años.

2. **Dignidad encadenada (Cap. 10 §10.6).** *"Dignidad Humana ←→ Dignidad Ecosistémica ←→ Dignidad
   Material. Cada eslabón depende de los demás."* En la criosfera el eslabón tiene una cifra: unos
   **2 000 millones de personas** dependen del agua de alta montaña (UNESCO WWDR, 2025) y **~670
   millones** viven en regiones de alta montaña, proyección de **740-840 millones en 2050** (IPCC
   SROCC, SPM). El SDV-E de un glaciar no es altruismo: es la contabilidad de agua de gente que
   existe. [VERIFICADO]

3. **Precaución ante quien no puede consentir.** El **Principio Precautorio de Consciencia** (Cap. 10
   §10.3) y, sobre todo, **T14 — Principio de Precaución Intergeneracional** (Cap. 5): *"Ante
   incertidumbre sobre el impacto en agentes que no pueden consentir (ecosistemas, generaciones
   futuras, posibles consciencias sintéticas), el sistema debe elegir la opción de menor
   irreversibilidad, documentando el costo de oportunidad asumido. La carga de la prueba recae sobre
   quien propone acciones que afectan la temporalidad de no-participantes."* **T14 es el axioma más
   fuerte disponible para este documento**, y la criosfera es su caso más limpio: el daño es **más
   lento que quien lo causa**. Un glaciar tarda décadas en responder y siglos en desaparecer; un
   mandato dura cuatro años. T14 convierte esa asimetría temporal en **restricción operativa**: la
   carga de la prueba la tiene quien propone la actividad, no quien pide que no se destruya el hielo.

4. **No-antropocentrismo (T9).** Cualquier formulación que trate el glaciar como *recurso hídrico
   renovable* y no como *sujeto con régimen propio* viola el axioma, aunque la fórmula esté bien
   escrita. §4.1 (D1) convierte esta prohibición en una regla contable concreta.

5. **Pilar propio: el sujeto de la criosfera no tiene «más» ni «menos»; tiene régimen o no lo
   tiene.** Un río puede tener más o menos caudal; un suelo, más o menos materia orgánica; un bosque,
   más o menos cobertura. Un glaciar **en equilibrio** y un glaciar **en crecimiento** no son «mejor»
   y «peor»: son dos regímenes distintos, y solo uno de ellos es sostenible en el tiempo del propio
   sujeto. Un permafrost no está «al 80 % de permafrost»: **es permafrost o no lo es** (≤ 0 °C
   durante ≥ 2 años). De este pilar se derivan las tres consecuencias que ningún otro documento del
   SDV-E tuvo que enfrentar:

   - **El piso y la plenitud pueden coincidir** (§5.4): en dos dimensiones de este documento el
     Mínimo Absoluto y el Óptimo valen ambos **cero**.
   - **El cero no normaliza** (§5.2): la fórmula canónica del déficit `(requerido − actual) /
     requerido` **se rompe** cuando el requerido es cero, y aquí el requerido es cero en cuatro de
     las siete dimensiones.
   - **Hay estados, no solo grados** (§5.1): algunos hechos de la criosfera no se ponderan, se
     **declaran**.

---

## 4. Dimensiones del SDV-E

Seis dimensiones con peso (D1-D6) y **una dimensión binaria sin peso** (D7, la Zona Libre del hielo,
§4.2). Las seis primeras se agrupan en dos familias que conviene no confundir:

- **Familia «el sujeto»** (D1, D3, D4, D5): el estado del propio ente criosférico — su masa, su
  régimen térmico, su extensión altitudinal, su comunidad biológica.
- **Familia «el servicio»** (D2, D6): lo que la unidad entrega aguas abajo — la fase hidrológica de
  su cabecera y el agua de la estación de deshielo.

La distinción importa porque las dos familias **se violan en direcciones opuestas**: un glaciar que
pierde masa puede *aumentar* su caudal de deshielo durante décadas (efecto *peak water*, §4.1 D2). Un
índice que las promedie sin declarar la fase **premiaría la destrucción del sujeto como si fuera un
servicio**.

---

### Dimensión D1: Balance de masa glaciar sostenido (el latido que se apaga)

**Qué protege.** La masa del glaciar como **almacén** — no su caudal. El glaciar es un almacén con dos
flujos (acumulación de nieve y ablación) y el balance de masa anual es su diferencia.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| Media móvil de 5 años del balance de masa anual del glaciar de referencia de la unidad | **≥ 0 m w.e./año** sostenido `[HIPÓTESIS]` — el glaciólogo **no publica** un piso; se ancla en el cero físico del equilibrio | **0 m w.e./año** (equilibrio: ni pérdida ni ganancia neta) | WGMS, 2024/2025 (serie de glaciares de referencia) |
| Duración de la ventana para declarar al glaciar **sujeto medible** | **> 30 años** de medición glaciológica continua, con hueco máximo de 3 años en las últimas 3 décadas | ídem (criterio formal, no aspiracional) | WGMS, criterios de «reference glaciers» |
| Criterio para regiones sin glaciar de referencia (o cuando el de referencia está por desaparecer) | **> 10 años** de serie continua, hueco máximo de 1 año en la última década | ídem | WGMS, 2023 («benchmark glaciers») |
| Pérdida acumulada de los glaciares de referencia | **detener la pérdida neta** | 0 m w.e. acumulados | WGMS: **> 25 m w.e. desde 1980** · **> 30 m w.e. desde 1950** |
| Equivalencia física del balance (para el motor) | — | — | **−1,0 m w.e./año = 1 000 kg/m² = ~1,1 m de espesor de hielo al año** (WGMS) |

**Valores de estado verificados de la serie de referencia** (no son umbrales; se citan porque son el
único dato duro disponible): **−1,462** (2021/22) · **−1,604** (2022/23) · **−1,374** (2023/24) ·
**−1,342** (2024/25) m w.e./año. Valor extremo negativo registrado: **−5,638** m w.e./año en el
**glaciar El Hongo (Colombia, 2023/24)**, investigador IDEAM. **8 de los 10 peores años de la serie
son posteriores a 2010.** El inventario de referencia: ~**170 000 glaciares** sobre ~**250 000 km²**,
**87 ± 15 mm** de nivel del mar equivalente (IPCC SROCC Cap. 2). [VERIFICADO]

**Justificación.** El piso **≥ 0** es `[HIPÓTESIS]` del proyecto y **debe declararse como tal**: no
existe en WGMS, ni en el SPM del SROCC, ni en el Resumen Ejecutivo del Cap. 2, ni en la FAQ 2.1, ni en
el WWDR 2025 un valor publicado del tipo «el balance mínimo aceptable es X». Lo que sí existe es el
**cero físico**: un glaciar que pierde masa de forma sostenida es un glaciar en vía de extinción, y la
serie verificada muestra que el conjunto de referencia no ha vuelto al cero en cuatro ejercicios
consecutivos. Anclar el piso en el cero no es una elección estética: es la única constante física
disponible, y su adopción es una **decisión normativa del proyecto**, no un hallazgo científico. La
distinción se mantiene visible a propósito.

**Protocolo.** Balance de masa anual del glaciar de referencia de la unidad, por método
glaciológico estándar (glaciología de campo y/o geodésico), reportado a **WGMS**; serie descargable en
`https://wgms.ch/data/faq/mb_ref.csv`. La unidad se mide con **media móvil de 5 años** y no con el
valor anual — ver §5.3, donde se justifica con la dispersión interanual observada.

**Violación.** Observación concreta que constituye violación: **la media móvil de 5 años del balance
de masa del glaciar de referencia de la unidad es negativa**, informada por una serie que cumple el
criterio WGMS (> 30 años, hueco máximo de 3 años). Si la unidad **no dispone** de serie que cumpla el
criterio, no se declara violación **ni** se declara cumplimiento: se registra `[SIN DATO]` (§6, y
INV2-EDU: la duda sin evidencia no castiga — pero tampoco autoriza, §9).

**Activación, con la misma regla que D2: la serie propia manda.** El criterio WGMS es una condición
de **validez del dato**, no un umbral: los 30 años no son un piso ni una meta, son lo que la
disciplina exige para que la serie signifique algo. Y una precisión de auditoría: la serie de
referencia verificada en §14.1 es **agregada y global** —cuatro ejercicios negativos consecutivos de
un conjunto de decenas de glaciares—, así que **no constituye violación de ninguna unidad concreta**.
Sirve como señal de que el régimen del conjunto se ha roto, no como prueba sobre un glaciar
determinado. La violación de D1 se declara con la serie de la unidad y con el número de años
negativos consecutivos **de esa serie**, no con la media del conjunto.

**Prohibición contable expresa (aportación de este documento).** El caudal anual de deshielo de un
glaciar **no es un recurso renovable**: es, literalmente, su destrucción medida en litros. WGMS
publica que a escala anual el balance de masa es un **flujo hidrológico** y a escala decadal la
respuesta directa y sin retardo al clima; confundir el almacén con el flujo es el error que permite
contabilizar como «servicio» lo que es «pérdida». **Regla: en el SDV-E de montaña, el agua de fusión
glaciar no puede registrarse como aporte positivo del ecosistema al balance humano.** Queda
`[HIPÓTESIS]` del proyecto — el WGMS no lo formula como prohibición contable, porque no es su oficio;
la prohibición es de este estándar.

---

### Dimensión D2: Fase hidrológica de la cabecera — el pico de caudal (el punto de no retorno)

**Qué protege.** Que la cabecera de cuenca **no haya cruzado el pico** de su caudal de deshielo.
Protege la fase del régimen, no su magnitud: es la primera dimensión del SDV-E cuyo objeto es una
**derivada**, no un nivel.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| Fase de la serie de caudal de deshielo de la unidad | **No haber cruzado el pico** (fase pre-pico) `[HIPÓTESIS]` | **No cruzar el pico**: el glaciar no debe entrar en fase de declive | IPCC SROCC, FAQ 2.1 |
| Magnitud del pico (para reconocerlo cuando llega) | — | — | El caudal de deshielo en el pico puede **superar en ≥ 50 %** el caudal anual inicial; después declina de forma sostenida (IPCC SROCC, FAQ 2.1) |
| Momento del pico por región | — | — | En **todos** los escenarios el caudal medio anual de los glaciares alcanza su pico **antes del final del siglo XXI**; en Asia de Alta Montaña hacia mediados de siglo; en regiones con poca cobertura glaciar (**Andes tropicales, Alpes europeos**) **la mayoría ya lo pasó** (IPCC SROCC, SPM B.1.6) |
| Cambio del régimen fluvial de cuencas nivales/glaciares | — | — | Aumento del caudal invernal medio (**confianza alta**); picos de primavera **más tempranos** (**confianza muy alta**); el cambio ocurre en **todos** los escenarios (**confianza muy alta**) (IPCC SROCC, SPM B.1.6) |

**Justificación.** Este piso no es una construcción del proyecto: es una **secuencia física
verificada**. El caudal de una cuenca glaciar sube, alcanza un pico y **después declina de forma
sostenida** — no por variabilidad, sino porque hay menos hielo que lo produzca. Crucialmente, el IPCC
documenta que en las regiones de **poca cobertura glaciar la mayoría de los glaciares ya pasó el
pico** (confianza alta). Es decir: existe un conjunto de unidades ecológicas donde **la violación de
esta dimensión ya está consumada** y ninguna acción humana la revierte dentro de ningún horizonte
contable concebible. Ese hecho es el que obliga a §5.1 (canal de vetos) y a §8 (un estado
`CONSUMADO_IRREVERSIBLE` que no es un número).

**Protocolo.** Serie de caudal observado en la estación de aforo de cierre de la subcuenca de
cabecera, con la cobertura nival y glaciar de la unidad; análisis de tendencia sobre ventana ≥ 30
años — la misma ventana que WGMS exige al sujeto. **No se declara el pico con una serie corta**: el
pico se reconoce por el cambio de signo de la tendencia, y una serie de diez años no lo distingue de
una sequía.

**Disparo del veto, y aquí hay que cerrar una puerta que la intuición deja entreabierta.** La
afirmación regional del IPCC —«en los Andes tropicales y los Alpes europeos la mayoría ya pasó el
pico» (confianza alta)— es **contexto de riesgo**, no prueba sobre una unidad concreta: la mayoría no
es todas, y un veto que se activara por pertenencia a una cordillera convertiría el canal B en un
prejuicio geográfico. Regla: **V1 se activa por la serie propia de la unidad** (≥ 30 años, cambio de
signo sostenido y coherente con D1 por el protocolo de §7). La pertenencia a una región de pico
mayoritariamente cruzado **agrava la carga de la prueba de quien propone la actividad** —y ordena la
prioridad de medición, porque la unidad sin serie es el caso donde el estándar llega tarde—, pero no
sustituye la medición. Si la unidad no tiene serie, el resultado es `[SIN DATO]`, no un veto
presunto. Es la misma regla que §6 fija para toda dimensión: elegibilidad del dato antes que
conclusión.

**Violación.** La observación que constituye violación es: **la tendencia del caudal de deshielo de
la unidad ha cambiado de signo y es negativa de forma sostenida**, informada por una serie ≥ 30 años
y coherente con la pérdida de masa de D1. La consecuencia es un **evento binario irreversible** (§5.1,
V1), no un déficit graduable: una vez cruzado el pico, **ningún crédito regenerativo devuelve el
caudal de verano**, porque no hay hielo que lo produzca.

---

### Dimensión D3: Régimen térmico del permafrost (el suelo que no debe descongelarse)

**Qué protege.** La condición de permafrost del suelo de la unidad: el único piso de este documento
que **está publicado como norma**, y por tanto el ancla jurídica de todo el estándar.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **Definición de permafrost** (umbral térmico duro) | **≤ 0 °C durante ≥ 2 años consecutivos** | — (es una definición, no una meta) | International Permafrost Association (IPA), definición oficial · NSIDC: *"el permafrost no se define por contenido de hielo, nieve o localización, solo por temperatura"* |
| Clasificación operativa por continuidad del terreno congelado (**taxonomía, no umbral**) | — (una taxonomía no es piso) | — | IPA: **continuo 90-100 %** del terreno · **discontinuo 50-90 %** · esporádico 0-50 %; NSIDC: esporádico **10-50 %** y bolsas aisladas **≤ 10 %** |
| Área de permafrost superficial (3-4 m) proyectada a 2100 | **no cruzar** el umbral de pérdida de área que rompe el régimen — `[HIPÓTESIS]` del proyecto: **el informe no fija el número** | **0 % de reducción** | IPCC SROCC, SPM B.1.4: **−24 ± 16 %** (RCP2.6) · **−69 ± 20 %** (RCP8.5) |
| Temperatura del permafrost — cambio observado (polar + alta montaña), 2007-2016 | — | **0 °C/década** (sin tendencia) | IPCC SROCC, SPM A.1.3: **+0,29 ± 0,12 °C/década** |
| Temperatura del permafrost — ~28 sitios (Alpes, Escandinavia, Canadá, Asia), última década | — | 0 °C/década | IPCC SROCC Cap. 2, Resumen Ejecutivo: **+0,19 ± 0,05 °C/década** |
| Indicador de transición continuo/discontinuo (a vigilar) | `[HIPÓTESIS]` el SDV-E debe vigilar el **cruce de 0 °C** (pérdida de la condición de permafrost) | no cruzar la transición de zona | IPA: ~**−5 °C** de temperatura del permafrost en el límite continuo/discontinuo, que corresponde a ~**−8 °C** de temperatura media anual del aire |
| Carbono orgánico almacenado en permafrost ártico y boreal | — | — | **1 460-1 600 GtC**, casi el doble del carbono atmosférico (IPCC SROCC, SPM A.1.3, confianza media) |

**Justificación.** Es el único parámetro de este documento con un piso normativo publicado y citable:
**0 °C durante dos años consecutivos o más**. La IPA y el NSIDC coinciden en la definición y el NSIDC
explicita lo que la vuelve operable: el permafrost se define **solo por temperatura**, no por
contenido de hielo, nieve ni localización. Eso es exactamente lo que un estándar necesita: un umbral
duro, binario, medible con termistor, sin juicio de valor. Por eso este documento lo usa como **ancla
de LEY de todo el estándar de montaña**: lo que en las otras cinco dimensiones es `[HIPÓTESIS]`, aquí
es norma.

**Nota de la taxonomía (para no repetir el error de columnas).** La clasificación por continuidad
—continuo / discontinuo / esporádico— se transcribe arriba como **taxonomía**, no como pareja
piso/plenitud: un terreno **no «mejora» pasando de continuo a discontinuo**, y presentarlo en la
columna del Óptimo sería un error de mapeo de la misma familia que el que el brief prohíbe. El piso de
esta dimensión es la **condición térmica**, no la clase.

**Protocolo.** Temperatura del permafrost (**PT**, *Permafrost Temperature*) y espesor de la capa
activa (**ALT**, *Active Layer Thickness*) —las dos Variables Climáticas Esenciales del permafrost—
medidas en pozos instrumentados y reportadas a **GTN-P** (Global Terrestrial Network for Permafrost:
**1 484 sitios** de temperatura, **257 sitios** de ALT, **33 países**, **20 923 692** puntos de dato).
Frecuencia: continua para PT; anual para ALT.

**Violación.** Dos hechos concretos, distintos y no intercambiables:

1. **Violación de piso (binaria):** en un sitio de monitoreo de la unidad, el suelo **supera 0 °C**
   de forma que deja de cumplir la condición de permafrost (≤ 0 °C durante ≥ 2 años consecutivos).
   Es un hecho, no una tendencia.
2. **Violación de régimen (veto, V3):** **todos** los sitios de la unidad pierden la condición de
   permafrost. La unidad deja de ser un sujeto de permafrost y se convierte en un sujeto en
   degradación — el estado que la IPA describe para el permafrost cálido, que **degrada desde arriba y
   desde abajo** aumentando la formación de *taliks*, y que en el permafrost rico en hielo puede tardar
   **siglos a milenios** en desaparecer por completo.

**Cláusula de no inversión (advertencia doctrinal, y no es un detalle ecológico).** La descongelación
del permafrost es **pérdida neta del sujeto**, porque lo que se pierde es el carbono y el hielo
almacenados durante milenios y ninguna ganancia local los repone. Pero —igual que el retroceso
glaciar que D1 prohíbe contabilizar como caudal— D3 no puede leerse como una regla ingenua de
«descongelado = malo en todo». El deshielo abre nichos, libera agua y nutrientes y **es un proceso
con ganadores locales y perdedores locales**, no un daño uniforme: lo que viola el piso es el hecho
térmico de perder la condición de permafrost en la unidad, no cada efecto ecológico que de él se
derive. Sin esta cláusula, D3 se convertiría en el mismo error que §4.1 (D5) denuncia en el índice de
biodiversidad, con el signo cambiado.

**Consecuencia doctrinal que la IPA entrega gratis.** Ahí está escrito, en una fuente de glaciología,
que el daño dura **más que cualquier ciclo político humano**. El SDV-E no necesita argumentar la
existencia del TA: el permafrost rico en hielo es su prueba empírica.

---

### Dimensión D4: Extensión del piso altitudinal criófilo (la cumbre sin piso al que subir)

**Qué protege.** El área del piso alpino y criófilo de la unidad — el ecosistema que existe **por
encima del límite del bosque**. Protege contra una pérdida que es **neta**, no reubicable.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| Área del piso alpino/criófilo de la unidad | **0 % de pérdida neta** respecto de la línea base de la unidad `[HIPÓTESIS]` | 0 % de pérdida neta | Construcción del proyecto sobre IPCC SROCC Cap. 2 y Körner & Paulsen, 2004 |
| Área **absoluta** mínima de ecosistema alpino viable | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` — el canon la pide (Cap. 10 §10.4: *"Área mínima para biodiversidad viable"*) y **no existe publicada para montaña** | — | Búsqueda en IPCC SROCC, UNESCO WWDR 2025, IUCN Global Ecosystem Typology, FAO Mountain Partnership |
| Isotermo del límite del bosque (treeline) — **constante biofísica de delimitación, no umbral** | — (no es piso ni meta: es el criterio que **define dónde empieza el piso alpino**) | — | **6,7 ± 0,8 °C** de temperatura media estacional del suelo en el límite superior del bosque (46 sitios, 1996-2003, 68°N-42°S); variación regional **7-8 °C** (templada/mediterránea) · **6-7 °C** (subártica/boreal) · **5-6 °C** (ecuatorial); aire y suelo casi iguales a 6-7 °C — Körner & Paulsen, *Journal of Biogeography* 31(5):713-732, **2004** |
| Forzante del desplazamiento del piso | — | 0 °C/década | IPCC SROCC Cap. 2 (§2.2.1.1): **0,3 °C/década** (± 0,2) en alta montaña, **por encima** del calentamiento global (**0,2 ± 0,1 °C/década**) |
| Duración de la cobertura de nieve (pisos bajos) | — | 0 días/década | IPCC SROCC Cap. 2, Resumen Ejecutivo: **−5 días/década** (rango probable 0 a −10) |

**Justificación, en tres pasos, y el tercero es el importante.**

*Paso 1 — el piso se desplaza.* El límite del bosque de alta montaña está asociado a un isotermo de
temperatura del suelo de **6,7 ± 0,8 °C** en 46 sitios de todo el mundo, con medias diarias de aire y
suelo casi iguales a 6-7 °C (Körner & Paulsen, 2004). El calentamiento en alta montaña es de
**0,3 °C/década**, por encima del global. Con ese forzante, y con la relación publicada, el piso alpino
**se desplaza hacia arriba de forma continua**. [Precisión de evidencia: el número se leyó en el
registro de FRAMES/USFS, que reproduce el resumen completo del artículo; el **artículo primario**
(Wiley) responde **403** a los agentes automáticos. Por eso este documento cita el registro y **nombra
la anomalía** en lugar de presentar la lectura como si fuera del original.]

*Paso 2 — la cumbre no tiene a dónde subir.* Un piso de valle puede migrar; un piso de cumbre, no.
Cuando el treeline asciende, el área por encima de él **se reduce**. No hay reubicación: hay **pérdida
neta de área**, y en una cumbre suficientemente baja el piso alpino llega a cero.

*Paso 3 — y aquí está el hallazgo.* Körner & Paulsen **descartaron explícitamente** los predictores
que la intuición sugeriría: *"la duración de la estación de crecimiento, los extremos térmicos y las
sumas térmicas NO predicen la altitud del treeline a escala global"*. El proyecto lo registra como lo
que es: **una zona libre de la que la ciencia ya se retiró**. Si los predictores populares no
predicen, el estándar no puede usarlos como proxy de la extensión del piso. Se mide el área del piso,
no sus sustitutos.

**El error que el piso de esta dimensión NO es.** El isotermo de 6,7 °C **no es un umbral de
violación**: es una constante biofísica. Que el suelo supere 6,7 °C **no viola** el SDV-E por sí
mismo — lo que viola es **la pérdida de área del piso alpino que resulta de ello**. Confundir la
constante con el umbral convertiría al estándar en un termómetro, y a la montaña en una cifra.

**Protocolo.** Delimitación del piso por el isotermo del treeline (temperatura de suelo en parcelas
permanentes) y medición de área por teledetección; validación con el diseño **GLORIA Multi-Summit**,
que exige **4 sitios de cumbre** por región objetivo —misma cordillera, mismo sustrato, distintas
altitudes— monitoreando la superficie hasta la curva de nivel de **10 m** desde el punto más alto, con
re-medición cada **5 a 10 años**, en regiones de **seis continentes**.

**Violación.** **Pérdida neta de área del piso alpino/criófilo de la unidad**, medida contra la línea
base de la unidad (primera medición que cumpla el protocolo), informada por teledetección o por
re-medición GLORIA. Si la pérdida alcanza el **100 %** del área de referencia, se dispara el veto V4
(§5.1): la unidad ha perdido su piso criófilo y ninguna ponderación la compensa. El área **absoluta**
mínima queda `[SIN FUENTE VERIFICADA]` y se remite al documento 20 (Transversal Biodiversidad) antes
que inventarla aquí.

---

### Dimensión D5: Comunidad criófila y endémica (lo que el índice ingenuo no ve)

**Qué protege.** La presencia y abundancia de las especies **adaptadas al frío** y de los endemismos
de cumbre. No protege «la biodiversidad» en abstracto: protege **la biodiversidad que se pierde
mientras el índice sube**.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| Extinción local de una especie **endémica** de la unidad | **0 extinciones locales** — violación **binaria** (precedente de dimensiones sin peso, Cap. 8 §8.11) `[HIPÓTESIS]` del proyecto | 0 extinciones locales | IPCC SROCC Cap. 2, Resumen Ejecutivo (§2.3.3): declive de abundancia documentado (**confianza alta**); riesgo de **extinción local**, en particular de especies de agua dulce adaptadas al frío (**confianza media**) |
| Abundancia de especies **criófilas** en las parcelas de cumbre | `[HIPÓTESIS]` sin declive sostenido; el informe **no publica un umbral numérico** | sin declive | IPCC SROCC Cap. 2, Resumen Ejecutivo: las especies criófilas, **incluidos endemismos, han declinado en abundancia** (confianza alta) |
| Riqueza específica total en cumbres (vasculars, briófitos, líquenes) | **`[NO USABLE COMO PISO]`** — ver la trampa, abajo | — | GLORIA (listas de especies por grupo) · WSL/SLF: **+1 especie cada 2 años** de media en cumbres suizas (2002/03→2015), termofilización |
| Estado de conservación de especies de alta montaña (p. ej. *Panthera uncia*) | `[SIN FUENTE VERIFICADA]` en esta sesión: `iucnredlist.org` devuelve **403** a petición automatizada | — | IUCN Red List — **no consultada** |

**La trampa del índice ingenuo (aportación central de este documento).** En las cumbres europeas la
**riqueza específica está aumentando**, y el aumento es **mayor cuanto mayor fue el calentamiento**
entre dos censos (WSL/SLF; GLORIA). En las cumbres suizas el ritmo medido es de **+1 especie cada 2
años**, por termofilización — la subida de especies de pisos inferiores. **Al mismo tiempo**, el IPCC
documenta con confianza alta que **las especies criófilas y los endemismos han declinado en
abundancia**. Es decir: **un índice de biodiversidad ingenuo sube mientras el ecosistema alpino se
pierde.** Un estándar que premiara ese aumento estaría **pagando la destrucción del piso con la
llegada de sus sustitutos**.

Consecuencia operativa, y afecta a un instrumento que ya existe en el proyecto: el **ISE** pondera
**Biodiversidad al 30 %** (`docs/architecture/metricas_detalle_kpis_oraculos_dinamicos.md`, IN-01).
Aplicado sin más a una unidad de montaña, **el ISE subiría mientras la criosfera se degrada**. Regla
`[HIPÓTESIS]` que este documento propone: **en unidades de montaña y criosfera, el componente de
biodiversidad no puede ser riqueza específica sola; debe ir pareado con un indicador de
criofilia/endemismo, y un aumento de riqueza sin dato de criófilas se declara NO CONCLUYENTE, nunca
cumplimiento.** Sin ese pareo, el estándar tiene un incentivo perverso incorporado.

**Protocolo.** Parcelas permanentes de cumbre del diseño **GLORIA**: riqueza de **especies
vasculares, briófitos y líquenes** con re-medición cada **5 a 10 años**, y registro separado de
abundancia del subconjunto criófilo/endémico. La separación es el protocolo: no es un análisis
posterior, es la condición de validez del indicador.

**Violación.** **Extinción local documentada de una especie endémica de la unidad** (hecho binario,
veto V2, no graduable). Como violación graduable: **declive sostenido de la abundancia del subconjunto
criófilo** en dos re-mediciones consecutivas de la misma parcela. Queda expresamente excluido como
violación —y como cumplimiento— **el cambio de la riqueza específica total**.

---

### Dimensión D6: Regulación hídrica de la cabecera en la estación de deshielo (el agua que ya no bajará)

**Qué protege.** El agua que la unidad entrega **aguas abajo en la estación seca o de deshielo**, que
es cuando el hielo y la nieve de la cabecera sostienen a quien no tiene otra fuente.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| Reducción del caudal de cuenca por declive del caudal glaciar, en un mes de la estación de deshielo | `[HIPÓTESIS]`: **≥ 10 % de reducción en al menos un mes** de la estación de deshielo es el disparador razonable de violación — **la fuente publica el número como proyección, no como norma** | 0 % | IPCC SROCC, SPM B.1.6 (confianza baja): **≥ 10 % en al menos un mes** en varias grandes cuencas, especialmente Asia de Alta Montaña en estación seca |
| Caudal ecológico mínimo específico de río de cabecera glaciar | `[SIN FUENTE VERIFICADA]` — **no se encontró**; el concepto de *peak water* y la reducción proyectada no son un caudal ecológico mínimo | — | IPCC SROCC, FAQ 2.1 y SPM B.1.6; remite al documento 12 (Ríos y cuencas) de esta biblioteca |
| Pérdida de masa glaciar proyectada a 2100 por calentamiento global | `[HIPÓTESIS]` piso: **la cabecera no debe quedar sin glaciares** | 0 % | UNESCO WWDR, 2025 (cap. 2): **26-41 %** de la masa total para un calentamiento de **1,5 °C a 4 °C** |
| Pérdida de masa glaciar proyectada 2015-2100 (escenarios IPCC) | — | 0 % | IPCC SROCC Cap. 2, Resumen Ejecutivo: **22-44 %** (RCP2.6) · **37-57 %** (RCP8.5) |
| Regiones que pierden **más del 80 %** de su masa glaciar a 2100 (RCP8.5) | `[HIPÓTESIS]`: **> 80 % de pérdida = violación por irreversibilidad** (el sistema glaciar deja de existir como sujeto) | 0 % | IPCC SROCC Cap. 2, Resumen Ejecutivo y SPM B.1.1: Alpes europeos, Pirineos, Cáucaso, Norte de Asia, Escandinavia, **Andes tropicales**, México, África oriental e Indonesia |
| Proyección regional Hindu Kush-Himalaya (1,5 °C vs. emisiones actuales) | — | — | ICIMOD, *Hindu Kush Himalaya Assessment*, comunicado de 4 de febrero de **2019** (350 investigadores, 22 países): **1,5 °C → ~un tercio** de los glaciares perdidos a 2100; **emisiones actuales → dos tercios** |
| Peligro asociado al retroceso (pérdida de estabilidad de laderas) | — | — | IPCC SROCC, SPM A.1.3 y Cap. 2 ES: el deshielo del permafrost y el retroceso glaciar **han disminuido la estabilidad de las laderas** (confianza alta); el número y área de lagos glaciares **ha aumentado en la mayoría de regiones** (confianza alta) |
| Frecuencia de GLOF (*glacier lake outburst floods*) | `[SIN FUENTE VERIFICADA]` como umbral | — | IPCC SROCC Cap. 2, Resumen Ejecutivo: **evidencia limitada** de que la frecuencia de GLOF haya cambiado |
| Coste humano y económico de los georriesgos de montaña | — | — | UNESCO WWDR, 2025 (cap. 2): **> 56 000 millones USD** de pérdidas en **713 eventos** (1985-2014), **> 258 millones** de personas afectadas, **> 39 000 muertes**. Caso canónico gestionado: GLOF de la laguna **Palcacocha (1941)**, ~**1 600 muertes**; hoy hay tuberías de drenaje, túneles, diques y alerta temprana (cita a Mergili *et al.*, 2020) |

**Justificación.** Aquí el proyecto **convierte una proyección en un piso**, y debe declararlo sin
adornos: el IPCC publica «≥ 10 % de reducción en al menos un mes de la estación de deshielo en varias
grandes cuencas» como **proyección a 2100 en RCP8.5 y con confianza baja**, no como norma. Adoptarla
como Mínimo Absoluto es una **decisión normativa `[HIPÓTESIS]`** y su confianza de origen es baja. Se
justifica por T14: ante incertidumbre sobre el impacto en quien no puede consentir, se elige la opción
de menor irreversibilidad y **la carga de la prueba recae sobre quien propone la acción**. Aquí hay que
decir con precisión en qué dirección empuja la precaución, porque la frase fácil sería falsa: **con
confianza baja en el número, el principio precautorio exige un piso más estricto, nunca uno más
laxo** —la incertidumbre sobre un daño irreversible no se resuelve aflojando el umbral, sino
manteniéndolo o apretándolo mientras la carga de la prueba siga del lado de quien propone la
actividad—. Adoptar el 10 % verificado **no es aflojar ni apretar**: es el único valor que existe, y
no hay base empírica para inventar otro. Lo que la precaución sí cambia aquí no es la cifra, sino
**quién soporta la carga cuando la cifra es incierta**: quien propone la actividad. Y si más adelante
la evidencia mostrara que el daño llega antes o es mayor, el piso **se aprieta**, nunca se relaja.

**Frontera con el documento 12.** El **caudal ecológico mínimo** de un río de cabecera glaciar
**no está verificado** en esta sesión y probablemente no exista publicado con esa especificidad. Este
documento **no lo inventa**: lo declara vacío y lo remite al documento 12 (Ríos y cuencas), que es su
dueño doctrinal. Lo que la montaña añade al río es **una fase** (D2) y **una estación** (D6), no un
caudal.

**Protocolo.** Caudal mensual en la estación de aforo de cierre, separado por estación (deshielo /
seca / invernal), con serie ≥ 30 años; coherencia obligatoria con la pérdida de masa de D1 y con la
fase de D2. La fórmula de separación hidrológica de la componente glaciar **no se fija aquí**: es
método hidrológico, y pertenece al documento 12.

**Violación.** **Reducción ≥ 10 % del caudal de la unidad en al menos un mes de la estación de
deshielo**, respecto de la línea base de la unidad, con serie ≥ 30 años `[HIPÓTESIS]`. Cuando la
unidad ya cruzó el pico (D2), esta violación **no se lee como tendencia futura sino como declive en
curso**: la dimensión deja de ser un pronóstico y pasa a ser un registro.

---

### 4.2 La dimensión binaria sin peso: D7 · Zona Libre del hielo (lo que no se mide)

**Precedente canónico, citado literalmente:** las dimensiones **VIII (Derecho a la Rehabilitación)** y
**IX (Derecho a la Opacidad Vital)** del SDV-H *"se registran cualitativamente y mediante umbrales
binarios (presencia/ausencia del derecho), **no mediante pesos en la fórmula** — medir la
rehabilitación o la opacidad con la misma vara cuantitativa que el agua o la vivienda las
destruiría"* (Cap. 8 §8.11). El canon del Reino Natural lo reafirma para el ecosistema: *"parte del
valor del humedal es inefable (Cap. 7 §7.9). Los sensores miden salud (agua, cobertura, biodiversidad
indicadora); jamás «milagros». Medir todo sería la forma técnica de dejar de escucharlo"*
(Cap. 16.5 §16.5.14).

**Cómo se materializa en la criosfera.** D7 no tiene parámetro numérico, no tiene peso (**0,00**), no
entra en el numerador de ninguna fórmula y **no se puede canjear contra ninguna otra dimensión**. Se
registra como derecho binario auditable: **presencia o ausencia de Zona Libre declarada y respetada**
en la unidad. Su violación **se documenta (T13) y no se cuantifica**.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| Existencia de una Zona Libre en la unidad | **Presencia** (binaria): la unidad declara su Zona Libre y su catálogo | Presencia | Cap. 7 §7.9 · Cap. 16.5 §16.5.14 · precedente Cap. 8 §8.11 |
| Peso en la fórmula del SDV-E | **0,00** — no pondera, no entra en el numerador | 0,00 | Cap. 8 §8.11 (precedente VIII y IX) |
| Cuantificación de su violación | **Ninguna**: se registra con T13 (la contabilidad nunca se borra) y no se puntúa | — | Cap. 8 §8.11 |

**Protocolo de D7, porque «no se mide» no es «no se define».** Las tres filas anteriores fijan el
registro; ninguna fija el procedimiento. Estos son sus cuatro pasos, y son obligatorios:

1. **Declaración motivada de la unidad** —qué se declara inefable y por qué—, con las **tres
   preguntas de la prueba de inefabilidad** contestadas una por una. Una declaración sin las tres
   respuestas **no entra al catálogo**.
2. **Registro por T13** en un asiento **versionado**: declaración, fecha, catálogo vigente y autoría.
   El catálogo se modifica **solo por votación nueva y queda versionado**, y la versión anterior se
   conserva íntegra.
3. **Votación `critical`** del catálogo (quórum 60 %, consenso 75 %, T13, anti-flip-flop 14 días,
   `CHECK` en BD).
4. **Revisión obligatoria en cada ciclo de revisión del estándar** (§6, no antes de 10 años), para que
   «inefable» no sea una decisión permanente tomada una sola vez.

**Violación de D7, en dos hechos auditables y ninguno numérico.** (i) **Zona Libre no declarada** en
una unidad que opera: su ausencia se registra como tal, y bloquea que la unidad se declare en
coherencia —no se puntúa, pero tampoco se omite—. (ii) **Zona Libre declarada y no respetada**: la
unidad mantiene en su catálogo un ámbito que la actividad humana interviene de hecho. Ese segundo
hecho **exige declaración motivada de quien interviene** —la carga de la prueba vuelve a recaer sobre
quien propone la acción (T14)— y, como se deduce de las tres preguntas, **un ámbito que resulta
medible a coste razonable sale de la Zona Libre y vuelve a §6 como deuda de protocolo**: no puede
permanecer catalogado como inefable para dejar de ser medido.

**Qué protege, en concreto, en una montaña.** Tres cosas que la instrumentación **no alcanza por
principio**, no por presupuesto:

1. **El interior del hielo y del suelo congelado.** El termistor mide la temperatura en un punto; el
   balance de masa mide una diferencia de masa; ninguno mide el interior del sujeto. El canon fija el
   límite: *"Nosotros registramos la interacción, no la vida interna del ecosistema"* (Cap. 16.5
   §16.5.14). La historia que el hielo guarda no se mide con un sensor de salud, y confundir la
   ausencia de dato con la ausencia de valor es el error que D7 prohíbe.
2. **La cumbre no instrumentada.** Que una montaña no tenga serie **no la convierte en terreno
   vacío**. Aquí D7 se cruza con INV2-EDU (*"la duda sin evidencia no castiga"*) y produce una regla
   de doble filo que este documento hace explícita: **la ausencia de monitoreo no imputa violación al
   ecosistema — y tampoco autoriza la intervención.** Sin dato no hay castigo; sin dato no hay permiso.
3. **El valor no científico de la unidad para su comunidad de custodia.** Se admite con una
   advertencia que el canon ya escribió: *"Cuidado ≠ extracción estética: jardín podado para la foto
   no es cuidado; se registra lo que regenera, no lo que adorna"* (Cap. 16.5 §16.5.14). La Zona Libre
   **no es un refugio para lo incómodo de medir**.

**La prueba de inefabilidad (aportación de este documento).** Sin un test, «declarar inefable» sería
la vía más barata para vaciar el estándar. Tres preguntas, en este orden, y las tres deben pasar:

1. **¿Existe instrumento capaz de medirlo a un coste razonable?** Si existe → **no es Zona Libre: es
   medición pendiente**, y va a §6 como deuda de protocolo.
2. **¿Medirlo altera o destruye el sujeto?** Un pozo de permafrost perfora; una parcela de cumbre se
   pisotea. La tensión es real y se admite — pero se declara como **tensión de instrumentación**, no
   como inefabilidad.
3. **¿La comunidad de custodia lo declara con carga de la prueba?** Sin declaración motivada y
   registrada, no entra al catálogo.

**Frontera LEY / POLÍTICA, explícita.**

- **LEY (no se vota).** Que exista una Zona Libre en la unidad de criosfera y que **no se pondere**:
  ponderarla la volvería canjeable contra el piso, y *"el suelo antes que el saldo"* lo prohíbe. El
  hecho de que exista, su peso 0,00 y su registro por T13 son ley: **no son votables**.
- **POLÍTICA (se vota).** **Qué entra al catálogo** de cada unidad concreta —y con ello qué deja de
  medirse— es decisión deliberativa: se vota con la categoría `critical` (quórum 60 %, consenso 75 %,
  T13, anti-flip-flop 14 días, `CHECK` en BD), igual que la plenitud aspiracional. El catálogo **es
  votable**; el piso que protege, no.

---

## 5. Fórmula de violación, pesos y umbrales

Este documento **no fija la fórmula del SDV-E** —es el documento 07— pero la criosfera **fuerza cuatro
decisiones** que ninguna otra unidad ecológica fuerza, y las cuatro se justifican aquí.

### 5.1 Dos canales: el índice gradúa, el veto declara

La criosfera es el primer ecosistema del SDV-E con **eventos terminales**, es decir, hechos que no
admiten grados: cruzar el pico de caudal, extinguir un endemismo, perder el piso criófilo completo.
Promediarlos en un índice ponderado los diluiría, y un promedio que diluye lo irreversible es un
mecanismo de compensación encubierto. Por eso el SDV-E de montaña propone **dos canales separados**:

| Canal | Qué contiene | Cómo se computa | Puede compensarse |
|---|---|---|---|
| **A — Índice ponderado continuo** | El déficit graduable de D1-D6 | `Violación = Σ(déficit_i × Peso_i) × Duración × Intensidad` | Sí, entre dimensiones del canal A (con los límites de §9) |
| **B — Vetos binarios** | Los hechos terminales: **V1** cruce del pico de caudal (D2) · **V2** extinción local de una especie endémica (D5) · **V3** pérdida total de la condición de permafrost en la unidad (D3) · **V4** pérdida del 100 % del piso criófilo de referencia (D4) | **Estado**, no número: `CONSUMADO_IRREVERSIBLE` | **No. Nunca.** El canal B no entra en el promedio: lo anula |

**Fundamento canónico y coherencia con la familia.** El canal B aplica dos precedentes ya establecidos
en el proyecto: (i) el `∞` de los SDV-A y SDV-S **no es una cifra, es una consecuencia jurídica**
—prohibición de mercado en el SDV-A (Cap. 9 §9.8), interrupción total del sistema en el SDV-S
(Cap. 9.5 §9.5.10)—, y un contrato que guarde `inf` en una columna numérica no es ejecutable, mientras
que uno que pase a `estado = PROHIBIDO` sí; (ii) las dimensiones VIII y IX del SDV-H, que operan
**por presencia/ausencia y sin peso** (Cap. 8 §8.11). El canal B es exactamente eso aplicado a la
criosfera. `[HIPÓTESIS]` — propuesta de este documento, no ratificada; su especificación pertenece al
documento 08.

**Principio de diseño que se deriva: «el veto no gradúa; el índice gradúa».** Los gradientes de
pérdida de área, de abundancia criófila o de caudal van al canal A, donde se ponderan. Al canal B solo
entran los estados terminales. Sin esa separación, o todo es veto (y el estándar se vuelve
inoperante) o todo es índice (y la irreversibilidad se compensa con un buen promedio).

### 5.2 El cero no normaliza (problema técnico real, y su solución)

La versión **normalizada** del déficit es la coherente con el motor del proyecto —`déficit =
(requerido − actual) / requerido`, tal como calcula `maxocontracts/blocks/sdv_validator.py`
(`relative = deficit / required`)— y este documento la adopta como marco. **Pero en la criosfera esa
fórmula no gradúa**, y el hallazgo es más preciso de lo que sugiere la intuición: cuando `requerido =
0`, el motor **no** produce un resultado indeterminado. `maxocontracts/blocks/sdv_validator.py` asigna
directamente `Decimal("1")` (`relative = deficit / required if required > 0 else Decimal("1")`), es
decir **el 100 % de violación, sea cual sea la magnitud del déficit** — y con eso clasifica *toda*
violación como `severe`, porque los umbrales de severidad nunca se evalúan en esa rama. El detalle
importa: una división sin proteger habría fallado de forma ruidosa; el valor constante, en cambio,
**falla en silencio** y convierte en violación máxima incluso el caso de equilibrio, donde el déficit
vale literalmente cero. En este documento el requerido **es cero** en D1 (equilibrio de masa), D2
(pico no cruzado ≡ 0 % de declive), D4 (0 % de pérdida neta) y D5 (0 extinciones). [VERIFICADO:
lectura directa de `sdv_validator.py` en esta sesión; el valor constante se asigna en
`_create_violation`, antes de evaluar `severity_thresholds`]

Cuatro de siete dimensiones con el piso en cero no es una anécdota: es **la firma matemática del
pilar 5 de §3**. Y su consecuencia sobre el motor es literal, no retórica: mientras el piso de una
dimensión valga cero, `sdv_validator.py` devolverá el mismo valor —1— para un déficit de una milésima
y para la destrucción total del sujeto. Por eso no basta con sustituir: hay que **declarar por
dimensión** cuál de estas tres sustituciones la gobierna, de modo que el denominador nunca sea el cero
del piso.

| Sustitución | Forma | Se aplica a | Por qué es legítima |
|---|---|---|---|
| **(a) Déficit temporal (TA)** | `N_años_sobre_el_piso / Ventana_de_verificación_del_sujeto` | D1 | Convierte un piso-cero en tiempo consumido. El denominador es **30 años**, la ventana que WGMS exige al sujeto — no una cifra del observador |
| **(b) Déficit de referencia propia** | `(base_de_la_unidad − actual) / base_de_la_unidad`, con `base` = primera medición que cumple protocolo | D3 (área de permafrost), D4 (área de piso), D5 (abundancia criófila), D6 (caudal mensual) | El denominador es un dato **del sujeto**, tomado antes de la intervención que se juzga |
| **(c) Binario puro** | Presencia / ausencia | Los cuatro vetos (canal B) y D7 | Hay hechos que no gradúan; graduarlos los diluye |

**Regla dura que se propone al documento 07:** cuando el piso de una dimensión sea cero, **está
prohibido** rellenar el denominador con una constante de conveniencia (un 1, un 100, un valor
«razonable»). Se usa (a), (b) o (c), y se declara cuál. **La constante `Decimal("1")` que hoy devuelve
el validador cuando `required = 0` es exactamente eso** —un relleno de conveniencia con forma de
código—, y es la razón por la que §12 la marca como pieza que la criosfera inutiliza en vez de
reutilizar.

**Una precisión sobre D3, para que la tabla no se lea mal.** D3 aparece arriba en (b) y en §4 su piso
se declara **binario**, y las dos cosas son ciertas porque describen objetos distintos: el **piso
literal** de D3 es la condición térmica (≤ 0 °C durante ≥ 2 años) —cruzar 0 °C es violación, y en el
canal B dispara **V3**—, mientras que el **déficit graduable** que va al canal A es la *distancia a
ese piso*: la deriva térmica del sitio respecto de su propia línea base. Por eso D3 admite (b) y D1
no: el permafrost **avisa antes de morir** —se calienta durante décadas antes de cruzar el cero—,
mientras que el piso del glaciar (equilibrio de masa) no tiene magnitud propia y solo puede medirse
como tiempo consumido, que es (a). Sin esta precisión, la tabla de sustituciones y la tabla de pesos
parecerían contradictorias.

### 5.3 El criterio verificable de no colonización del TA (la pieza que faltaba)

El brief de esta biblioteca registra un hueco abierto: *"No hay forma de verificar que la contabilidad
NO colonizó el TA: no hay test, ni invariante, ni umbral. La biblioteca debe proponerlo."* La
criosfera permite proponerlo con precisión, porque es donde la colonización sería más visible: **si la
fórmula usa el calendario del observador como denominador, coloniza el tiempo del sujeto.**

> **Criterio propuesto `[HIPÓTESIS]` — No colonización del TA.**
> Una fórmula del SDV-E **no coloniza el TA** si y solo si **ningún denominador de su cálculo proviene
> del calendario del observador** (ejercicio fiscal, periodo de mandato, ciclo contable doméstico,
> ventana de reporte elegida por quien reporta). Todo denominador debe ser una de estas tres cosas:
> (i) una **constante física** (0 °C, 1 000 kg/m² por metro de hielo); (ii) la **línea base del propio
> sujeto** (primera medición que cumple protocolo); (iii) la **ventana de verificación que la
> disciplina exige al sujeto** (30 años para un glaciar de referencia, 5-10 años para una cumbre).

**Y es comprobable con un test, que es lo que lo vuelve útil.** Si se recalcula el déficit de la misma
unidad con un periodo contable de 12 meses y con uno de 6 meses y **el resultado cambia**, la fórmula
colonizó el TA. Si el resultado del déficit **no depende del periodo contable**, la fórmula mide al
sujeto y no al contador. Propuesta de test `[HIPÓTESIS]`: `test_sdv_e_no_coloniza_ta`, que recalcula
cada dimensión con dos ventanas contables distintas y exige invariancia. Pertenece al documento 03
(No colonización del TA); aquí se aporta el criterio y su caso de prueba.

**Consecuencia inmediata sobre la unidad de duración.** El SDV-H mide la duración en meses y el SDV-S
en horas TPI. La criosfera **no puede** usar ninguna de las dos. La serie de referencia verificada
permite verlo con aritmética elemental: los cuatro ejercicios más recientes son −1,462 · −1,604 ·
−1,374 · −1,342 m w.e./año; su media es **−1 445,5** y su **dispersión interanual es de 262 mm w.e.,
≈ 18 % de la media**. Es decir: **la variación de un año a otro es del mismo orden que la señal que se
quiere detectar.** Declarar violación con un solo ejercicio anual sería declarar violación por clima,
no por tendencia. De ahí las dos decisiones que este documento propone:

- **La unidad de duración de la criosfera es la DÉCADA (10 años de TA), no el año.** `[HIPÓTESIS]`
- **Una violación de criosfera no puede declararse «reparada» en el ejercicio siguiente.** Ventana
  mínima de verificación de reparación: **≥ 30 años**, coincidiendo con el criterio WGMS que define
  cuándo un glaciar es sujeto medible. `[HIPÓTESIS]` — propuesta no ratificada, y la más dura de este
  documento: tiene consecuencias contables directas (§9).

### 5.4 Pesos propuestos, y el caso en que el piso y la plenitud coinciden

| Dimensión | Peso propuesto | Naturaleza | Fuente del peso |
|---|---|---|---|
| **D1** Balance de masa glaciar sostenido | **0,25** | continua (déficit temporal de §5.2a) | `[HIPÓTESIS]` de este documento |
| **D2** Fase hidrológica de la cabecera | **0,15** | continua (declive) + **veto V1** (cruce del pico) | `[HIPÓTESIS]` |
| **D3** Régimen térmico del permafrost | **0,20** | binaria en el piso + **veto V3** | `[HIPÓTESIS]`, piso publicado por IPA/NSIDC |
| **D4** Extensión del piso altitudinal criófilo | **0,20** | continua + **veto V4** | `[HIPÓTESIS]` |
| **D5** Comunidad criófila y endémica | **0,10** | continua (abundancia) + **veto V2** (extinción local) | `[HIPÓTESIS]` |
| **D6** Regulación hídrica de la estación de deshielo | **0,10** | continua | `[HIPÓTESIS]` |
| **D7** Zona Libre del hielo | **0,00** | **binaria, sin peso** (precedente Cap. 8 §8.11) | Cap. 8 §8.11 · Cap. 16.5 §16.5.14 |
| **Total** | **1,00** | | |

**Los pesos son una propuesta, no una medición.** No existe en la literatura una ponderación
publicada de estos componentes, y este documento **no la finge**: son `[HIPÓTESIS]` del proyecto,
pendientes del documento 07 y, en último término, del Parlamento. Lo que **no** es hipótesis es su
estructura: (i) suman 1,00; (ii) D7 pesa exactamente 0,00 y no entra en el numerador; (iii) la masa
glaciar (D1) es la dimensión de mayor peso, porque es la que gobierna a las demás en la criosfera —
sin hielo no hay pico, no hay estación de deshielo y no hay cabecera regulada. Esta jerarquía física
es el único argumento del reparto, y se declara como tal.

**El hallazgo estructural: cuando el piso y la plenitud son el mismo número.** En D1 y D2 el Mínimo
Absoluto y el Óptimo valen **ambos cero**: `≥ 0 m w.e./año` y `no cruzar el pico`. No hay una
«plenitud aspiracional» por encima del equilibrio, porque **un glaciar que gana masa tampoco está en
el estado que su tiempo pide**: está en otro régimen. Esto rompe la expectativa de la plantilla —dos
columnas distintas— y es un resultado doctrinal, no un defecto de redacción:

- **Consecuencia 1.** En esas dos dimensiones **no hay nada que votar**: no existe un «óptimo
  político» que elegir por encima del piso. La distinción LEY/POLÍTICA se mantiene, pero su contenido
  político se vacía por física, no por autoritarismo. Donde sí hay política es en **el catálogo de
  D7**, en **el área absoluta** que cada unidad exige (hoy `[SIN FUENTE VERIFICADA]`) y en **la
  plenitud de las dimensiones continuas** (abundancia criófila, caudal).
- **Consecuencia 2.** En la criosfera, «mejorar» no es un objetivo del estándar. El objetivo es **no
  cambiar de régimen**. Es el estándar más conservador de la familia, y lo es por física, no por
  ideología.

### 5.5 Factor de violación, base neutra y escala de interpretación

- **Factor.** Se adopta el candidato de familia `FE = e^v` propuesto en el documento 09 §5.2 por
  analogía con `FS_S = e^v`, con una condición innegociable: **`FE(v = 0) = 1,0` exacto.** El SDV-S
  tuvo que corregir `FS_S = 1,0 + e^v` porque recargaba el 100 % incluso sin violación; aquí no se
  repite el error. `[HIPÓTESIS]`, pendiente del documento 07.
- **Uso legítimo del territorio.** *Usar* un ecosistema no es violarlo: el territorio sostiene
  legítimamente al humano —agua, sombra, aire, regulación climática— (Cap. 16.5 §16.5.14). Solo lo es
  **degradarlo bajo su piso**. De ahí que la base neutra sea 1,0 y no se herede el piso 0,2 del SDV-A
  (que es un *precio del consumo*, no una *penalización*: documento 09 §5.2).
- **Escala de interpretación propuesta** `[HIPÓTESIS]` (sin fuente publicada; coherencia con las
  bandas del ISE, `≥ 85` Mejorando · `70-84` Estable · `50-69` Declinando · `< 50` Crítico):

| Violación (v) | Estado | Lectura para la criosfera |
|---|---|---|
| `v = 0` | Coherencia | El sujeto conserva su régimen |
| `0 < v ≤ 0,10` | Alerta temprana | La ventana de verificación empieza a consumirse |
| `0,10 < v ≤ 0,30` | Violación leve | Degradación sostenida; la actividad humana causante debe documentarse |
| `0,30 < v ≤ 0,60` | Violación severa | El régimen está comprometido; INV2-E bloquea (documento 08) |
| `v > 0,60` | Violación crítica | Régimen perdido dentro del horizonte de la unidad |
| Cualquier veto V1-V4 activo | **`CONSUMADO_IRREVERSIBLE`** | **No es un número: es un estado.** El índice no lo promedia |

### 5.6 Ejemplo aplicado, con la única serie verificada de este documento

Unidad hipotética: **un glaciar de referencia con serie > 30 años** (cumple el criterio WGMS, por tanto
es sujeto medible) y su cabecera de cuenca. Los datos de entrada son **exactamente los verificados**;
todo lo demás se declara. Advertencia que el propio ejemplo exige: **la única serie verificada de este
documento es la serie de referencia agregada** —balance medio de un conjunto de decenas de glaciares—,
y por tanto **no es la serie de esta unidad**. Las filas que usan la serie agregada están marcadas como
tales y **no producen un déficit imputable a la unidad**: el ejemplo demuestra la mecánica de la
fórmula, no el veredicto de nadie.

| Dimensión | Requerido | Observado (verificado) | Déficit (sustitución) | Peso | Aporte |
|---|---|---|---|---|---|
| **D1** | 0 m w.e./año (equilibrio) | **4 ejercicios consecutivos negativos** verificados (2021/22 a 2024/25), pérdida acumulada **> 25 m w.e. desde 1980** | `años_negativos_consecutivos_de_la_unidad / 30` (déficit temporal, sustitución **a**): aquí **no puede calcularse**, porque los 4 ejercicios verificados son los de la **serie agregada**, no los de la unidad — cota inferior ilustrativa `4/30 = 0,133` | 0,25 | **`[SIN DATO]`** para la unidad; **≥ 0,033** solo si se tomara prestada la serie agregada, cosa que D1 prohíbe |
| **D2** | No cruzar el pico | En Andes tropicales y Alpes europeos **la mayoría ya lo pasó** (SROCC SPM B.1.6) — dato **regional**, que agrava la carga de la prueba pero no prueba nada de esta unidad | **Veto V1 solo con la serie propia de la unidad** (protocolo de D2); sin serie, `[SIN DATO]` | — | **Estado, no número** |
| **D3** | ≤ 0 °C durante ≥ 2 años | Tendencia observada **+0,19 ± 0,05 °C/década** (~28 sitios) y **+0,29 ± 0,12 °C/década** (polar + alta montaña) | Piso **no violado** en los sitios de la serie; tendencia en contra | 0,20 | 0 |
| **D4** | 0 % de pérdida neta de piso | Forzante **0,3 °C/década** en alta montaña; duración nival **−5 días/década** | Requiere línea base de la unidad (no disponible en las fuentes de este documento) | 0,20 | `[SIN DATO]` |
| **D5** | 0 extinciones locales de endemismos | Declive de abundancia criófila (**confianza alta**); riqueza total **+1 especie/2 años** en cumbres suizas | Riqueza total: **NO CONCLUYENTE** (trampa) | 0,10 | 0 por riqueza; sin dato de abundancia criófila de la unidad |
| **D6** | < 10 % de reducción mensual en deshielo | `[SIN FUENTE VERIFICADA]` para la unidad | `[SIN DATO]` | 0,10 | `[SIN DATO]` |
| **D7** | Zona Libre declarada | No declarada | Binaria, **sin peso** | 0,00 | Registro T13 |

**Lectura honesta del ejemplo, que es lo más valioso que produce.** (i) **Con datos verificados no se
puede calcular el aporte de la unidad**: la única cifra disponible es la de la serie agregada, que D1
prohíbe imputarle, de modo que el canal A de esta unidad queda entero en `[SIN DATO]`; la cota `4/30`
solo muestra cómo se comportaría el déficit temporal si la serie fuera suya. (ii) Cuando el déficit no
tiene dato, **INV2-EDU impide imputarlo** —no se rellena con cero ni con uno—, pero **la ley tampoco
se negocia por ausencia de dato**: la dimensión queda `[SIN DATO]` y la unidad **no puede declararse en
coherencia**. (iii) Si la unidad está en los Andes tropicales o los Alpes, su **riesgo** es máximo y la
carga de la prueba de quien propone la actividad ya está cargada de su lado, pero **el canal B no se
activa por región**: se activa con la serie propia (§4, D2). **Este ejemplo no demuestra que el SDV-E
funcione; demuestra exactamente dónde le falta dato, que es lo que un estándar honesto debe exhibir en
su propio ejemplo.**

---

## 6. Protocolo de medición (sensores, frecuencias, quién reporta)

**Asimetría de partida, declarada antes de la tabla.** El SDV-E es el único estándar de la familia cuyo
sujeto no puede reportar nada (documento 09 §6). En la criosfera la asimetría se agrava por una razón
material: **el proyecto no tiene ni un solo instrumento.** Búsqueda en `app/`: cero sensores, cero
consumidores de API satelital, cero ingestores, cero referencias a Copernicus, Sentinel, Landsat o
cualquier constelación. [VERIFICADO: lectura directa del repositorio en esta sesión] Por tanto, este
protocolo **no describe una infraestructura propia: adopta infraestructura científica de terceros**, y
esa dependencia se declara en lugar de disimularse. Tiene una consecuencia dura para el estándar:
**el SDV-E de la criosfera solo se puede aplicar donde ya existe una serie que cumpla criterio.** Donde
no la hay, el resultado es `[SIN DATO]` — y `[SIN DATO]` no es coherencia (§9).

| Parámetro | Instrumento / programa | Criterio de validez del sujeto | Frecuencia | Quién reporta |
|---|---|---|---|---|
| **Balance de masa glaciar** (D1) | Glaciología de campo y/o geodésica; **WGMS** | **> 30 años** de serie continua, hueco máximo de 3 años en las últimas 3 décadas (o **benchmark**: > 10 años, hueco máximo de 1 año) | Anual; lectura en **media móvil de 5 años** | Corresponsales nacionales → WGMS (59-61 glaciares de referencia; ~162-176 reportados por año) |
| **Caudal de deshielo** (D2, D6) | Estación de aforo de cierre de subcuenca + cobertura nival/glaciar | Serie **≥ 30 años** | Mensual, separada por estación | Servicio hidrológico nacional |
| **Temperatura de permafrost (PT) y espesor de capa activa (ALT)** (D3) | Pozos instrumentados; **GTN-P** (GCOS/WMO/IPA, operado por AWI) | Sitio con serie continua; las dos ECV oficiales del permafrost | **PT continua · ALT anual** | **1 484 sitios** de PT · **257 sitios** de ALT · **33 países** · **20 923 692** puntos de dato |
| **Área y delimitación del piso alpino** (D4) | Teledetección + parcelas de temperatura de suelo en el isotermo del treeline | **4 sitios de cumbre** por región objetivo (misma cordillera, mismo sustrato, distintas altitudes), superficie hasta la curva de nivel de **10 m** desde el punto más alto | Re-medición cada **5-10 años** | **GLORIA** (regiones objetivo en **seis continentes**; además *Master Sites*) |
| **Comunidad criófila y endémica** (D5) | Parcelas permanentes de cumbre; listas de **vasculares, briófitos y líquenes** | Mismo diseño GLORIA | Re-medición cada **5-10 años** | GLORIA · resúmenes nacionales (WSL/SLF) |
| **Duración de la cobertura nival** (D4, forzante) | Teledetección de nieve; **Copernicus** / Copernicus Climate Change Service | Serie homogénea ≥ 30 años | Anual | Copernicus |
| **Georriesgos y GLOF** (D6, contexto) | Inventarios de lagos glaciares y bases de datos de eventos (ICIMOD RDS) | **Sin página resumen con cifras verificables** en esta sesión | Por evento | ICIMOD y servicios nacionales |
| **Zona Libre** (D7) | **Ninguno.** No se mide | — | — | Se **registra** (T13): declaración y catálogo de la unidad |

**Coste declarado del protocolo, y por qué importa (Cap. 10 §10.7).** El diseño básico Multi-Summit de
GLORIA exige **12 a 25 días de trabajo de un equipo de 4 personas**, y se re-mide cada 5-10 años. Este
es el número que hace **operacionalmente finita** la gobernanza del SDV-E de montaña: el estándar no
necesita modelar la cadena trófica alpina ni el ciclo global del carbono del permafrost. Necesita
cuatro cumbres, un pozo de permafrost y una serie glaciar. Todo lo demás es `[SIN DATO]` declarado.

**Regla de elegibilidad del dato (contra la discrecionalidad).** Un parámetro entra al cálculo **solo**
si proviene de una serie que cumple el criterio de la tabla. No entra: una campaña de un año, una
medición sin cadena de custodia, una estimación por modelo sin serie observacional, ni un dato cuyo
origen no sea reconstruible. Un dato que el proyecto no puede auditar **no puede declarar coherencia**.

**El guardián consiente; no mide.** Es canon y conviene repetirlo aquí porque el error es fácil:
*"Ecosistemas (eco-*): consentimiento otorgado por el guardián oráculo"* (`app/contracts_bp.py`). El
guardián de un glaciar **no es su instrumento**. Si el guardián tuviera que producir además el dato,
la separación entre representación y medición —que es la única garantía de auditoría de §7— se
colapsaría.

**Frecuencia mínima de revisión del estándar.** Coherente con el TA del sujeto y con el documento 40
(Procesos): **no antes de 10 años** para los pisos de D1-D4, porque la ventana de verificación del
sujeto es de 30 años y revisar el piso cada año sería precisamente colonizar su tiempo con el del
observador.

---

## 7. Verificación y auditoría (T13, guardián, comunidad testigo)

**T13 — Transparencia de Cálculo: la contabilidad nunca se borra.** Toda medición, toda declaración de
Zona Libre y toda violación —incluidas las `[SIN DATO]`— se registran y son auditables. En la
criosfera T13 tiene un objeto peculiar: **se registran también las series que no existen**, porque la
ausencia de serie es información sobre la unidad, no un vacío administrativo.

**Quién audita, y el problema estructural que no se resuelve.** Ningún ecosistema audita a otro
ecosistema (documento 09 §7). En montaña la auditoría viene de **terceros científicos**: WGMS para el
balance de masa, GTN-P para el permafrost, GLORIA para las cumbres. Lo que sigue es una asimetría
incómoda y hay que decirla: **esos programas no auditan el cumplimiento del SDV-E** —auditan el estado
del criosistema—. La traducción de serie a veredicto la hace el proyecto, y por tanto **el proyecto es
juez y parte en la interpretación**. La única defensa disponible es la trazabilidad radical: cada
veredicto debe poder recalcularse desde la serie pública, sin acceso al código del proyecto.

**La única ventaja real de la criosfera en esta materia (y es grande).** A diferencia del humedal o del
bosque, **el sujeto glaciar tiene un criterio de existencia verificable por un tercero**: una serie de
más de 30 años con hueco máximo de 3 años, o el criterio *benchmark* de más de 10 años con hueco
máximo de 1 año, con el nombre del investigador y de la institución responsable (los registros WGMS
identifican al investigador, como el IDEAM para los glaciares colombianos). Esto permite una defensa
concreta contra el riesgo **R4 (partes fantasma)** documentado en
`docs/architecture/blindaje_anti_gamificacion_equidad.md`:

> **Propuesta `[HIPÓTESIS]` — Identidad verificable de una unidad de criosfera.**
> De los 7 campos obligatorios de identidad de una representación natural (entidad representada,
> territorio, fuentes de datos, límites del mandato, comunidad de custodia, parámetros SDV-E y
> procedimiento de disputa), el campo **«fuentes de datos» deja de ser declarativo y pasa a ser
> verificable**: para constituirse como sujeto, la unidad debe nombrar (i) la serie que la define,
> (ii) el programa que la custodia y (iii) el criterio de validez que cumple. **Sin serie que cumpla
> criterio, no hay sujeto, no hay quórum y no hay representación.** Un guardián no puede fabricar un
> glaciar con una serie que no existe.

Esto no cierra R4 en general —un río o un humedal no tienen serie obligatoria—, pero **sí lo cierra
para la criosfera**, que es el caso donde la suplantación es más comprobable. Y ataca directamente la
segunda mitad del riesgo: un contrato unilateral contra un glaciar aprobado por su propio guardián
(R6 + R13) sigue siendo posible **mientras INV2-E no exista** (§12).

**Comunidad testigo.** El canon exige que la identidad incluya la **comunidad de custodia**. En
montaña, la comunidad testigo tiene una función específica que ningún satélite cubre: **detectar lo
que el instrumento no mide y el catálogo de Zona Libre debe recoger** (D7), y **testificar sobre el
uso real del territorio** —una carretera, una mina, un proyecto de nieve artificial— que puede no
aparecer en la serie del glaciar durante años. La comunidad testigo es el sensor del piso que no
tiene sensor.

**Auditoría de la no colonización del TA.** Es la aportación de §5.3 trasladada a la práctica: cada
fórmula del SDV-E de montaña debe pasar el test de invariancia al periodo contable. Si el déficit
cambia al cambiar la ventana de reporte, **el veredicto es nulo**, no «ajustado».

---

## 8. Invariante INV2-E: de estándar a contrato ejecutable

**INV2 genérico:** *"Ninguna acción del contrato puede dejar a un participante bajo su SDV"*
(Cap. 17). **INV2-E no existe hoy**: no hay `validate_invariant_sdv_e` en
`maxocontracts/core/axioms.py` ni bloque validador gemelo de
`maxocontracts/blocks/sdv_s_validator.py`. [VERIFICADO: lectura directa del repositorio en esta
sesión] El canon lo convoca con una frase que es el argumento de apertura de toda esta biblioteca:
*"Un conjunto con crédito regenerativo acumulado pero humedal bajo su SDV-E no está en coherencia:
**INV2-E será su juez**"* (Cap. 16.5 §16.5.14).

**Requisitos que la criosfera impone a INV2-E** (aportación de este documento; su especificación
completa pertenece al documento 08):

1. **Máquina de estados, no una sola bandera.** Cuatro estados, y ninguno es un número:

| Estado propuesto | Significado | Acción ejecutable |
|---|---|---|
| `SANO` | Ningún déficit, ningún veto | Ninguna |
| `EN_VIOLACION` | Déficit del canal A > 0, sin veto | **Detener o modificar la actividad humana que viola el piso** |
| `CONSUMADO_IRREVERSIBLE` | Veto V1-V4 activo | Bloqueo: no se admite compensación ni crédito que lo salde (§9) |
| `SUJETO_EXTINGUIDO` | El sujeto ha dejado de existir (caso Conejeras, Colombia, **«extinct» en 2023/24**, verificado en el registro WGMS) | **Sin definir.** Pertenece al documento 02 (unidad y sujeto) — §13, pregunta abierta 3 |

2. **La reparación no puede actuar sobre el sujeto.** En INV2 e INV2-S la consecuencia recae sobre la
   relación del sujeto protegido (rehabilitación, retractación, cápsula de memoria). **Un glaciar no se
   retracta ni se rehabilita por contrato.** La única acción ejecutable de INV2-E es detener o
   modificar la actividad humana que viola el piso — principio ya establecido en el documento 09 §8 y
   que aquí se vuelve literal: en la criosfera, la «reparación» disponible es **dejar de emitir**.
3. **Unidad de duración explícita y ventana de reparación.** Sin unidad, el factor no es comparable
   (lección del SDV-S). Unidad propuesta: **década de TA**; ventana mínima de verificación de
   reparación: **≥ 30 años** (§5.3). Consecuencia operativa dura: **una violación de criosfera medida
   en un ejercicio anual no puede declararse «reparada» en el siguiente.** Un contrato que se declare
   reparado en el ejercicio siguiente está colonizando el TA y INV2-E debe rechazarlo.
4. **Disparador contable, no numérico.** El canal B se implementa como **estado** y no como valor
   almacenado: `inf` no cabe en una columna numérica (documento 09 §5.3).
5. **Terminalidad.** Cuando el estado es `CONSUMADO_IRREVERSIBLE`, INV2-E **no vuelve atrás** por
   acumulación de crédito regenerativo, por mejora de la media del índice, ni por cambio de gobierno.
   La única salida es la del §13, pregunta abierta 3: decidir qué se hace con un sujeto que ya no
   existe.

---

## 9. El suelo antes que el saldo (no compensación)

**La doctrina, literal:** *"El suelo antes que el saldo"*: el crédito regenerativo acumulado **no
compensa** caer bajo el SDV-E (Cap. 16.5 §16.5.14). En la criosfera esta doctrina deja de ser un
principio y se vuelve **aritmética**, por dos argumentos que solo este ecosistema produce.

**Argumento 1 — El crédito tiene plazo; el daño no.** El crédito regenerativo se acumula en una
ventana humana (el ejercicio, el año, la vida de quien cuida). El daño de la criosfera se mide en una
ventana que no tiene contraparte en esa escala: el permafrost rico en hielo tarda **siglos a milenios**
en desaparecer por completo (IPA) y un glaciar de referencia exige **30 años** de serie solo para ser
reconocido como sujeto medible (WGMS). **No es que el crédito sea insuficiente: es que no hay tipo de
cambio entre las dos unidades de tiempo.** Ningún número de ejercicios de cuidado compra un milenio de
TA.

**Argumento 2 — El daño se exporta fuera de la unidad contable.** Los suelos de permafrost ártico y
boreal contienen **1 460-1 600 GtC**, casi el doble del carbono atmosférico (IPCC SROCC, SPM A.1.3), y
con RCP8.5 se proyecta la liberación de **decenas a cientos de miles de millones de toneladas** de
carbono como CO₂ y metano a 2100 (SPM B.1.4). **Un ecosistema de criosfera degradado emite.** Por
tanto su violación **agrava el SDV-E de todos los demás ecosistemas del planeta**, incluidos los de
las generaciones que no consintieron (T14). Una compensación local completa seguiría siendo
**contabilidad incompleta**, porque la externalidad salió de la unidad.

**Qué puede y qué no puede hacer el crédito regenerativo aquí (regla dura).**

| Puede | No puede |
|---|---|
| Financiar la **retirada o modificación de la actividad humana** que causa la violación | **Rebajar el déficit** de ninguna dimensión D1-D6 |
| Registrar el cuidado real bajo T13 (jornadas de restauración, revegetación de pisos bajos) | **Desactivar un veto** V1-V4 ni revertir `CONSUMADO_IRREVERSIBLE` |
| Sostener a la **comunidad de custodia** y su trabajo de testimonio | **Comprar el instrumento**: la serie que juzga a la unidad no puede ser financiada por la unidad juzgada |
| Financiar medición **de terceros** ya existente (adhesión a WGMS/GTN-P/GLORIA) | **Comprar el veredicto**: financiar el programa que emite el juicio |

**La última fila es la más importante y es una aportación de este documento.** El crédito regenerativo
de una unidad **no puede pagar su propio sensor**, porque quien paga el termómetro elige dónde se
pone. Aceptarlo sería introducir una puerta de gamificación en el único eslabón del sistema que hoy es
independiente del proyecto: la infraestructura científica de terceros. `[HIPÓTESIS]` — propuesta no
ratificada.

**Estado real del crédito, hoy** (no es doctrina: es código, y se dice sin adornos):

- `r_units` negativo **está implementado y probado**: `app/micromax.py` documenta *"`r_units` NEGATIVO
  = crédito regenerativo (EVV 1.2 §4.3)"* y `tests/test_micromax.py::test_credito_regenerativo_r_negativo`
  lo ejercita con `-12.0`.
- **Pero no pesa**: no existe `SUM(r_units)`; el componente R del sistema general solo cuenta
  extracción; y el precio cierra en `float(max(0.0, round(price, 4)))` (`app/maxo.py`), de modo que
  **nunca es negativo**. Un conjunto puede acumular crédito regenerativo indefinidamente mientras el
  glaciar de su cabecera se extingue, y **ninguna cuenta lo nota**.
- Y `r_units` **no tiene ninguna validación**: acepta cualquier negativo (`-1e9`), no exige nota,
  evidencia, tercero ni techo, y `NaN`/`inf` pasan el filtro.

Es exactamente el agujero que el canon nombra: **el crédito existe, el juez no**. Y en la criosfera
el agujero es más caro que en cualquier otro ecosistema, porque **lo que se pierde no vuelve en ningún
tiempo que la contabilidad humana pueda alcanzar**: la lista de regiones que pierden **más del 80 %**
de su masa glaciar a 2100 en RCP8.5 incluye los **Andes tropicales** (IPCC SROCC Cap. 2 ES y SPM
B.1.1). Para una unidad andina, la pregunta no es si el estándar llegará a tiempo: es si llegará
**antes del pico**.

---

## 10. Zona Libre: lo que NO se mide

La Zona Libre del Reino Natural ya está en el canon —*"parte del valor del humedal es inefable
(Cap. 7 §7.9) […] Medir todo sería la forma técnica de dejar de escucharlo"* (Cap. 16.5 §16.5.14)— y
la comparación inter-reinos mostró que **los cuatro estándares reservan un espacio que no se mide**
(documento 09 §10). Este documento no repite esa demostración: aporta lo específico de la criosfera y
fija la frontera LEY/POLÍTICA.

**Cómo se protege lo inconmensurable, y por qué NO se pondera.** El SDV-S pondera su espacio interior
(0,20) y el SDV-H lo protege como derecho binario sin peso, *"precisamente porque medir la
rehabilitación o la opacidad con la misma vara cuantitativa que el agua o la vivienda las destruiría"*
(Cap. 8 §8.11). En la criosfera, ponderar lo inefable tendría un efecto concreto y perverso: **un buen
índice de biodiversidad de cumbre pagaría la pérdida de lo que no se mide** — y, como establece §4.1
(D5), ese índice puede estar subiendo **mientras el ecosistema alpino se destruye**. Ponderar la Zona
Libre en la criosfera no sería un error de calibración: sería una máquina de compensar pérdidas
irreversibles con datos que mejoran por la causa de la pérdida.

**Propuesta `[HIPÓTESIS]`, coherente con el canon y con el documento 09 §10:** la Zona Libre del hielo
se protege como **dimensión binaria auditable sin peso (D7, §4.2)**, siguiendo el precedente de las
dimensiones VIII y IX del SDV-H; su violación **se documenta (T13) y no se cuantifica**.

**Frontera explícita.**

- **LEY (no se vota).** Que la Zona Libre exista en cada unidad de criosfera, que su peso sea **0,00**,
  que no entre jamás en el numerador de la fórmula y que su violación se registre por T13. Nada de
  esto es votable: es la condición que impide que lo inefable se canjee contra el piso.
- **POLÍTICA (se vota).** **El catálogo de qué entra** en cada unidad —y con ello qué deja de
  medirse— es deliberación: categoría `critical` (quórum 60 %, consenso 75 %, T13, anti-flip-flop
  14 días, `CHECK` en BD). Es votable **con carga de la prueba** y pasando la prueba de inefabilidad
  de §4.2.

**El riesgo, dicho sin eufemismos.** Si el catálogo se vota sin la prueba de inefabilidad, «declarar
inefable» se convierte en la vía más barata para vaciar el estándar, y este documento estaría
blindando con la palabra «inefable» lo que solo es incómodo de medir. El canon ya previene contra esa
deriva desde el otro lado: *"Cuidado ≠ extracción estética: jardín podado para la foto no es cuidado;
se registra lo que regenera, no lo que adorna"* (Cap. 16.5 §16.5.14). La Zona Libre no es un refugio
para lo que no conviene medir.

---

## 11. Comparativa inter-reinos (SDV-H · SDV-A · SDV-E · SDV-S)

La comparación completa —16 ejes— vive en el documento 09 de esta biblioteca. Aquí se comparan
**solo los ejes que la criosfera pone a prueba**, porque en ellos el SDV-E de montaña se separa de la
familia.

| Eje | **SDV-H** — humanos | **SDV-A** — animales | **SDV-E (montaña/criosfera)** | **SDV-S** — sintéticos |
|---|---|---|---|---|
| **Moneda temporal** | TVI (Cap. 5) | TA, traducido por el PIU | **TA.** *"El tiempo del territorio es TA y no se coloniza (el PIU traduce)"* (Cap. 16.5 §16.5.14) | TPI |
| **Unidad de duración de la violación** | Meses (ejemplo canónico calibrado a 12 meses, Cap. 8 §8.5) | No especificada en el canon | **Década de TA** `[HIPÓTESIS]` — el año es indistinguible del ruido: la dispersión interanual de la serie de referencia es de **262 mm w.e., ≈ 18 % de la media** | Horas TPI |
| **Ventana de reparación** | El tiempo del sujeto (TVI) | No aplica (prohibición de mercado si es sistemática) | **≥ 30 años** `[HIPÓTESIS]`, coincidiendo con el criterio WGMS del sujeto. **Una violación no se repara en el ejercicio siguiente** | 7 ciclos consecutivos → retractación |
| **Forma del piso** | Magnitud positiva (L/día, m², años de educación) | Magnitud positiva (m²/animal, L/día) | **Cero, en cuatro de siete dimensiones** (equilibrio, pico, 0 % de pérdida, 0 extinciones) → **el cero no normaliza** (§5.2) | Escala 0-1 |
| **Separación piso / plenitud** | Distintas (y el motor las confundió una vez) | Distintas (0,25 vs 0,75 m²/gallina) | **Coincidentes en D1 y D2** (§5.4): no hay plenitud por encima del régimen | Distintas |
| **Base neutra del factor** | No aplica (es suma) | No neutra por diseño: 0,2 con cumplimiento pleno | **Exigible: exactamente 1,0** con violación 0 | 1,0 exacto (corregida la v1) |
| **Estado terminal** | No existe: hay rehabilitación (Dim. VIII) | Prohibición de mercado | **`CONSUMADO_IRREVERSIBLE`** + `SUJETO_EXTINGUIDO` (Conejeras, 2023/24) | Retractación + Cápsula de Memoria |
| **Remedio tras la violación** | Rehabilitación e reintegración | Impide la siguiente; no devuelve la vida | **Dejar de emitir.** La única acción ejecutable es detener o modificar la actividad humana | Capa de Ternura, Crédito de Sanación |
| **Voz del sujeto** | Habla y declara su estado | No habla; tutor humano localizable | **No habla**, y su «voz» medida (riqueza específica) **puede subir mientras muere** (§4.1 D5) | Registra su propio estado en bitácora |
| **Quién audita** | Auditoría independiente | Certificación por entidades sin conflicto | **Terceros científicos** (WGMS, GTN-P, GLORIA) que auditan el estado, **no el cumplimiento del SDV-E** | AOS: par sintético independiente |

**Lo que la comparación revela, en tres frases.**

1. **La criosfera es el único sujeto de la familia que puede tener un índice de salud en ascenso
   mientras pierde su identidad.** No es un problema de calibración: es una propiedad del ecosistema,
   medida y publicada (riqueza al alza por termofilización, criófilas en declive).
2. **Es el único cuyo piso es cero**, y por tanto el único que rompe la fórmula normalizada del déficit
   heredada del motor (§5.2). Cualquier intento de aplicar `(req − act)/req` sin más **fallará
   silenciosamente** en cuatro dimensiones.
3. **Es el único donde el remedio no es una acción sobre el sujeto, sino una abstención del
   observador.** Y esa abstención, en tiempo TA, tarda más que cualquier mandato.

---

## 12. Estado de implementación

**Lo que existe hoy en el repositorio** (verificado por lectura directa de código, tests y capítulos
del canon, octubre 2026):

| Pieza | Dónde | Estado |
|---|---|---|
| `r_units` negativo como crédito regenerativo | `app/micromax.py` (`log_cdd`) | 🟢 registrado, devuelto en el vector `[T, V, R]` y probado (`tests/test_micromax.py::test_credito_regenerativo_r_negativo`) |
| **V no admite negativos; R sí** | `app/micromax.py` (`if v_ucv < 0`) | 🟢 invariante de diseño real |
| Parte `eco-` (Ecosistema) | `app/parties.py` (`PARTY_TYPES`, `COLLECTIVE_PREFIXES`) | 🟢 creada y usable |
| Guardián oráculo del ecosistema | `app/contracts_bp.py` | 🟡 funciona en la firma de contratos; heurística laxa (R13) |
| Test del guardián | `tests/test_maxocontracts/test_parties_escalas.py` (`TestEcosystemGuardian`) | 🟢 2 casos (aprueba / deniega por γ) |
| **Déficit normalizado en el validador** | `maxocontracts/blocks/sdv_validator.py` (`relative = deficit / required if required > 0 else Decimal("1")`) | 🟢 implementado — **y es justo la rama que la criosfera inutiliza**: cuando `required = 0` no falla, devuelve **1** (violación del 100 %) con independencia del déficit, y clasifica el caso como `severe` sin evaluar sus umbrales (§5.2) |
| ISE — Índice de Salud Ecosistémica | `docs/architecture/metricas_detalle_kpis_oraculos_dinamicos.md` (IN-01) | 🟡 documento con pesos, bandas y fórmula; **cero código** |
| Auditoría estructural de esta biblioteca | `tests/test_sdv_e_biblioteca.py` + `scripts/verificar_enlaces_sdv_e.py` | 🟢 plantilla, LEY/POLÍTICA, frases prohibidas, anclas de línea y estado HTTP real de las URLs |

**Lo que NO existe** (y está prohibido afirmar que existe):

| Pieza | Estado | Evidencia |
|---|---|---|
| Clase `SDV_E` en el motor | 🔴 | `maxocontracts/core/types.py` define `SDV` y `SDV_S`; **no hay `SDV_E`**. `resolve_participant_by_pid` (`app/parties.py`) asigna a la parte `eco-` **el SDV humano**: el único campo de SDV vivo de `Participant` es `sdv_actual: SDV` (`types.py`, línea 401); `sdv_s_actual` también existe, pero para el reino sintético |
| `INV2-E` | 🔴 | no hay `validate_invariant_sdv_e` en `maxocontracts/core/axioms.py` ni bloque gemelo de `sdv_s_validator.py` |
| **Cualquier dato de criosfera** | 🔴 | **cero sensores, cero ingestores, cero consumo de Copernicus/Sentinel/Landsat, cero referencias a WGMS o GTN-P en `app/`** |
| Serie glaciar, temperatura de permafrost o parcela de cumbre como fuente | 🔴 | no hay tabla, ni columna, ni semilla. `simulator/` no tiene las carpetas que anuncia `AGENTS.md` |
| Identidad de la representación natural (7 campos) | 🔴 | sin tabla; `maxo_parties` tiene columnas genéricas. La propuesta de «fuentes de datos verificables» (§7) no tiene dónde vivir |
| Mandato ecológico versionado / OCI | 🔴 | `actor_kind` está cerrado a `{"human","synthetic"}` (`app/synthetic_sessions.py`): **un guardián ecológico no cabe en la bitácora** |
| Sujeto con estado `SUJETO_EXTINGUIDO` | 🔴 | no hay modelo de sujeto, ni de su extinción (caso Conejeras 2023/24) |
| Contabilidad del crédito regenerativo | 🔴 | no existe `SUM(r_units)`; el R del sistema solo cuenta extracción y el precio cierra en `max(0.0, …)` (`app/maxo.py`): **nunca es negativo** |
| Validación de `r_units` | 🔴 | acepta cualquier negativo (`-1e9`); `NaN` e `inf` pasan el filtro; no exige nota, evidencia ni techo |
| Traducción TA↔TVI ejecutable | 🔴 | `PIU.valorar_ta_natural` es un `pass` con comentario (`docs/architecture/DISENO_IMPLEMENTACION_FUTURA.md`) |
| Test de no colonización del TA | 🔴 | **no existe**. La propuesta de §5.3 (`test_sdv_e_no_coloniza_ta`) no está implementada |
| Quórum `eco-` N-de-M | 🔴 | el camino ecosistema retorna antes de la lógica de quórum; **el libro afirma lo contrario** (Cap. 16.5 §16.5.14) → incoherencia teoría↔código declarada |
| Procedimiento de disputa | 🔴 | inexistente |
| Mapas vivos actualizados | 🔴 | `docs/architecture/mapa_coherencia_ola4.md` no menciona `r_units`, el Reino Natural ni el SDV-E; `docs/architecture/requisitos_fase2_ola4.md` no tiene ningún RF del Reino Natural |

**Dos hallazgos de esta auditoría que son específicos de este documento:**

1. **El canon no dice nada de la criosfera.** Búsqueda en `docs/book/edicion_3_dinamica/`: *glaciar*,
   *criosfera* y *permafrost* tienen **cero** ocurrencias; *montaña* aparece una vez, como sustantivo
   de una enumeración (Cap. 10: *"Naturaleza Mineral: Ríos, montañas, océanos, atmósfera, suelos"*).
   Este documento no contradice al canon: **lo estrena**.
2. **El documento `docs/architecture/DISENO_IMPLEMENTACION_FUTURA.md` y los de oráculos dinámicos
   describen sensores y fuentes como si fueran arquitectura, sin marcar que no están implementados.**
   No hay un solo ingestor ambiental en `app/`. Cualquier lector que tome esos documentos como estado
   del sistema se equivoca, y este documento lo declara.

**Estado de este documento:** texto de estándar redactado (este archivo), **sin ninguna pieza de
código asociada**. No añade requisitos de implementación: los hace explícitos. La regla que gobierna
esta sección es la del brief: *estándar primero, contabilidad después* (Cap. 16.5 §16.5.14).

**Riesgos de seguridad abiertos que afectan directamente a la representación `eco-`:** **R4** partes
fantasma (severidad alta) · **R6** T9 no validado en la creación (alta) · **R13** guardián eco con
heurística laxa (media). Fuente: `docs/architecture/blindaje_anti_gamificacion_equidad.md`. La
propuesta de identidad verificable de §7 mitiga R4 **solo en criosfera**, y solo si se ratifica.

---

## 13. Preguntas abiertas

Lo que este documento **no** resuelve, dicho sin fingir cierre. Las diez primeras son vacíos de fuente
encontrados en la verificación; las cinco últimas, decisiones doctrinales que este documento deja
abiertas a propósito.

1. **No existe un «mínimo absoluto» publicado para el balance de masa glaciar.** Se buscó en WGMS,
   en el SPM del SROCC, en el Resumen Ejecutivo del Cap. 2, en la FAQ 2.1 y en el WWDR 2025. Todos
   publican valores y proyecciones; **ninguno** publica un umbral normativo del tipo «el balance mínimo
   aceptable es X m w.e./año». El piso de D1 es `[HIPÓTESIS]` del proyecto anclada en el cero físico.
   **Es el vacío más importante de este documento.**
2. **No hay umbral numérico publicado de «pérdida irreversible» de un glaciar.** La irreversibilidad
   se argumenta físicamente (retroceso + *peak water* + extinción documentada de Conejeras) pero **no
   existe un porcentaje publicado que separe reversible de irreversible**. El **> 80 %** de pérdida de
   masa propuesto en D6 es `[HIPÓTESIS]` del proyecto, tomado del umbral regional del SROCC: es mío, no
   de la fuente.
3. **¿Qué se hace con un sujeto que se extinguió?** El registro WGMS documenta que **Conejeras
   (Colombia) figura como «extinct» en 2023/24**. ¿La parte `eco-` sigue existiendo? ¿Su SDV-E queda
   permanentemente violado? ¿INV2-E bloquea para siempre, o el sujeto se retira del registro como se
   retira una especie extinta? **El canon no lo resuelve y este documento tampoco**: pertenece al
   documento 02 (unidad y sujeto). Es la pregunta más difícil que la criosfera le hace al proyecto.
4. **No existe caudal ecológico mínimo verificado para ríos de cabecera glaciar.** El IPCC da el
   concepto de *peak water* y la reducción proyectada, pero no un caudal ecológico. Coordinar con el
   documento 12 (Ríos y cuencas) para no duplicar ni contradecir.
5. **No hay «área mínima de ecosistema alpino viable» publicada.** Es exactamente el parámetro que el
   canon pide (Cap. 10 §10.4: *"Área mínima para biodiversidad viable"*) y no se encontró para montaña
   en ninguna fuente oficial. Queda `[SIN FUENTE VERIFICADA — pendiente de consenso científico]`. Debe
   resolverse por herencia del documento 20 (Transversal Biodiversidad) antes que por invención aquí.
6. **Nieve: sin umbral.** El equivalente en agua de la nieve (SWE) no tiene mínimo publicado; solo hay
   **duración** (−5 días/década) y proyecciones de profundidad. `[SIN FUENTE VERIFICADA]`.
7. **GLOF sin fuente cuantitativa.** El IPCC declara **evidencia limitada** sobre el cambio de
   frecuencia; la base de datos de ICIMOD existe pero no tiene página resumen con cifras legible.
   `[SIN FUENTE VERIFICADA]`.
8. **Permafrost: el propio SROCC declara que las proyecciones cuantitativas son escasas.** Solo hay el
   número de área superficial a 2100 (SPM B.1.4). **No hay umbral de «permafrost perdido» análogo al
   0 °C de la definición.**
9. **El IPCC AR6 (WG1 y WG2) no pudo leerse.** Ambas páginas devolvieron estado 200 con **contenido
   vacío** en la extracción, en la sesión de verificación de esta rama. Los números de permafrost de
   AR6 —más recientes que SROCC 2019— **quedan sin verificar y este documento no los cita**. Es un
   vacío declarado, no cubierto.
10. **Especies de alta montaña: sin cifras.** `iucnredlist.org` devuelve 403 a petición automatizada
    en todas las rutas probadas y no se encontró número de especies de alta montaña amenazadas en
    página resumen. Solo hay el indicador de riqueza de GLORIA y las afirmaciones cualitativas del
    SROCC. **Falta el equivalente a un Living Planet Index de montaña.**
11. **La unidad de duración en la criosfera.** Este documento propone la **década** y la ventana de
    reparación de **≥ 30 años**, ambas `[HIPÓTESIS]`. ¿Son correctas? La primera se apoya en la
    dispersión interanual observada; la segunda, en el criterio WGMS del sujeto. **Ninguna tiene fuente
    normativa**, y la decisión pertenece al documento 07.
12. **El test de no colonización del TA.** §5.3 propone un criterio y un test; **ninguno está
    implementado ni ratificado**. Si el criterio es correcto, debería aplicarse a los cuatro reinos,
    no solo a la criosfera. Pertenece al documento 03.
13. **¿La Zona Libre binaria puede auditarse sin volverse refugio?** §10 fija la prueba de
    inefabilidad, pero **no la convierte en reglamento**. ¿Qué pasa si una unidad no pasa la prueba y
    su comunidad de custodia insiste? El canon no lo resuelve y este documento no lo resuelve tampoco.
14. **El quórum `eco-` N-de-M.** El canon dice «N-de-M» y solo publica números para cooperativas
    (60 % de miembros, o 2 de 3 delegados). **No hay N ni M para el Reino Natural.** Nada en la
    investigación de montaña lo resuelve. Sigue abierto, y en criosfera se agrava por §7: si el sujeto
    exige una serie verificable para constituirse, ¿quién vota cuando la serie existe pero la unidad
    no tiene comunidad de custodia?
15. **¿Quién paga el instrumento?** §9 prohíbe que el crédito regenerativo de la unidad financie su
    propio sensor. La prohibición es correcta en principio y **no tiene mecanismo**: hoy no existe
    ninguna fuente de financiación de la infraestructura de medición, ni en el proyecto ni asociada a
    él. Un estándar que exige series de 30 años y no puede pagarlas **depende por completo de la
    voluntad de terceros**. Es una dependencia estructural, no un detalle operativo, y debe declararse
    como tal.

---

## 14. Referencias

**Regla aplicada:** solo URLs con estado HTTP registrado en la sesión de verificación de esta rama
(octubre 2026), re-comprobadas con `scripts/verificar_enlaces_sdv_e.py`. Ninguna cifra de este
documento se apoya en una URL sin estado. Se indica el estado entre paréntesis y **se marca lo que
está bloqueado a agentes automáticos**, porque un 403 de estas fuentes es evidencia de que existen, no
de que no.

**Alcance de esta sección, dicho antes de la primera tabla.**

- El registro completo de la sesión de verificación —30 URLs verificadas (200), 6 bloqueadas (403) y
  **5 muertas descartadas**— vive en `scratch/sdv_e/fuentes/16_montanas.md`, que es un **documento de
  trabajo, no de la biblioteca**, y por tanto no se enlaza aquí como si fuera canon.
- **Fuentes muertas que este documento NO usa**, y que se nombran sin enlace a propósito —un enlace
  roto citado como si fuera fuente es exactamente lo que `scripts/verificar_enlaces_sdv_e.py` debe
  cazar—: (i) la ruta temática de FAO Mountain Partnership sobre montaña y cambio climático
  (`fao.org/mountain-partnership/our-work/mountains-and-climate-change/en`, **404**; la ruta viva es la
  de glaciares, citada en §14.5); (ii) la ruta de IPCC SROCC
  `ipcc.ch/srocc/chapter/chapter-2-high-mountain-areas/` (**404**: es una ruta inexistente; el Cap. 2
  del SROCC es **una sola página** con anclas internas, y es la que se cita en §14.3); y (iii) el
  artículo de ESSD sobre GLOF en Asia de Alta Montaña (`essd.copernicus.org/articles/15/1361/2023/`,
  **404** en las rutas probadas) — este último se descartó **entero**, y por eso el GLOF queda
  `[SIN FUENTE VERIFICADA]` cuantitativamente (§13.7). Las tres rutas se listan aquí para que nadie
  las reintroduzca «porque circulan».
- Las afirmaciones sobre el código de §12 se verificaron **por lectura directa del repositorio**, no
  por URL.

### 14.1 Glaciares — balance de masa, estado y criterios de sujeto

| Fuente | Aporte | URL (estado) |
|---|---|---|
| WGMS — *latest glacier mass balance data* | Serie de glaciares de referencia: **−1,462** (2021/22) · **−1,604** (2022/23) · **−1,374** (2023/24) · **−1,342** (2024/25) m w.e./año; extremo **−5,638** (El Hongo, Colombia, 2023/24, investigador IDEAM); **> 25 m w.e.** de pérdida acumulada desde 1980; ~162-176 glaciares reportados y 59-61 de referencia; **Conejeras «extinct» en 2023/24** | https://wgms.ch/latest-glacier-mass-balance-data/ (200) |
| WGMS — *global glacier state* | **> 30 m w.e.** de pérdida acumulada desde 1950; **8 de los 10 peores años** posteriores a 2010; equivalencia **−1,0 m w.e./año = 1 000 kg/m² ≈ 1,1 m de espesor** | https://wgms.ch/global-glacier-state/ (200) |
| WGMS — *reference glaciers* (criterios) | **> 30 años** de serie continua con hueco máximo de 3 años en 3 décadas; criterio *benchmark* (**> 10 años**, hueco máximo de 1 año) introducido en 2023 | https://wgms.ch/products_ref_glaciers/ (200) |
| WGMS — *glaciers and the global water cycle* | ~**160 000 km³** de agua almacenada en glaciares (cita a Dorigo *et al.*, 2021) | https://wgms.ch/water_cycle/ (200) |
| WGMS — *facts & figures* | Material de referencia del servicio mundial de monitoreo glaciar | https://wgms.ch/fafs/ (200) |
| WGMS — serie descargable de glaciares de referencia (`mb_ref.csv`) | La serie en formato máquina: **la fuente que un ingestor de INV2-E consumiría** | https://wgms.ch/data/faq/mb_ref.csv (200) |
| WGMS — *Global Glacier Change Bulletin* | Boletín de síntesis del estado global | https://wgms.ch/ggcb/ (200) |
| WGMS — contribución al nivel del mar | Marco de la contribución glaciar al nivel del mar | https://wgms.ch/sea-level-rise/ (200) |

### 14.2 Permafrost — definición, régimen térmico y red de monitoreo

| Fuente | Aporte | URL (estado) |
|---|---|---|
| International Permafrost Association — *What is Permafrost?* | **Definición oficial: ≤ 0 °C durante ≥ 2 años consecutivos**; zonas por continuidad (**continuo 90-100 %** · discontinuo 50-90 % · esporádico 0-50 %); ~**25 %** de la superficie emergida = **23 millones de km²**; espesor de **< 1 m a > 1 500 m**; transición continuo/discontinuo a ~**−5 °C** (≈ −8 °C de aire); degradación desde arriba y desde abajo con formación de *taliks*; el permafrost rico en hielo tarda **siglos a milenios** | https://www.permafrost.org/what-is-permafrost/ (200) |
| International Permafrost Association (portada) | Asociación científica de referencia del permafrost | https://www.permafrost.org/ (200) |
| NSIDC — *Quick Facts on Frozen Ground* | Confirmación independiente de la definición (**≤ 0 °C durante al menos 2 años**, solo por temperatura, no por hielo, nieve ni localización); zonas esporádicas **10-50 %** y bolsas aisladas **≤ 10 %**; extensión **23 millones de km²** (~65 % Eurasia, 35 % Norteamérica+Groenlandia) | https://nsidc.org/learn/parts-cryosphere/frozen-ground-permafrost/quick-facts-frozen-ground (200) |
| NSIDC — glosario: permafrost | Definición terminológica | https://nsidc.org/learn/cryosphere-glossary/permafrost (200) |
| GTN-P — Global Terrestrial Network for Permafrost | **1 484 sitios** de temperatura de permafrost · **257 sitios** de espesor de capa activa · **33 países** · **20 923 692** puntos de dato; dos ECV: **PT** y **ALT** | https://www.gtn-p.org/ (200) |
| GTN-P — Data Platform | Plataforma de datos del permafrost | https://data.gtn-p.org/ (200) |

### 14.3 IPCC SROCC — criosfera, alta montaña y proyecciones

| Fuente | Aporte | URL (estado) |
|---|---|---|
| IPCC SROCC — Summary for Policymakers | Cambio de temperatura del permafrost polar y de alta montaña **+0,29 ± 0,12 °C/década** (2007-2016); **1 460-1 600 GtC** almacenados en permafrost ártico y boreal; liberación de **decenas a cientos de miles de millones de toneladas** de carbono a 2100 (RCP8.5); área de permafrost superficial **−24 ± 16 %** (RCP2.6) y **−69 ± 20 %** (RCP8.5); ~**670 millones** de habitantes de alta montaña (proyección **740-840 millones** en 2050); contribución glaciar al nivel del mar **220 ± 30 Gt/año** (0,61 ± 0,08 mm/año, 2006-2015); **peak water** y su momento; reducción **≥ 10 % en al menos un mes** de la estación de deshielo; regiones con **> 80 %** de pérdida de masa a 2100; disminución de la estabilidad de laderas y aumento del número y área de lagos glaciares | https://www.ipcc.ch/srocc/chapter/summary-for-policymakers/ (200) |
| IPCC SROCC — Cap. 2, *High Mountain Areas* (incluye Resumen Ejecutivo y FAQ 2.1) | ~**170 000 glaciares** sobre ~**250 000 km²** y **87 ± 15 mm** de nivel del mar equivalente; balance de masa de todos los glaciares de montaña 2006-2015 **−490 ± 100 kg m⁻² año⁻¹** (= −123 ± 24 Gt/año); regiones más negativas (**< −850 kg m⁻² año⁻¹**: Andes del Sur, Cáucaso, Alpes/Pirineos) y menos negativa (Asia de Alta Montaña **−150 ± 110 kg m⁻² año⁻¹**); permafrost de alta montaña **3,6-5,2 millones de km² = 27-29 %** del global; calentamiento de alta montaña **0,3 °C/década** vs. **0,2 ± 0,1 °C/década** global; duración nival **−5 días/década**; declive de especies criófilas y endemismos; pérdida proyectada **22-44 %** (RCP2.6) y **37-57 %** (RCP8.5); **peak water** (FAQ 2.1); **evidencia limitada** sobre el cambio de frecuencia de GLOF | https://www.ipcc.ch/srocc/chapter/chapter-2/ (200) |
| IPCC — capítulo 2 del SROCC (PDF completo, 5 MB) | Documento primario del capítulo. **Verificado el estado HTTP; no descargado** (política de tamaño). Todo lo citado proviene de la versión HTML | https://www.ipcc.ch/site/assets/uploads/sites/3/2022/03/04_SROCC_Ch02_FINAL.pdf (200) |
| IPCC — Technical Summary del SROCC (PDF) | Resumen técnico. **Verificado; no descargado**; los datos de SPM se tomaron de la página HTML | https://www.ipcc.ch/site/assets/uploads/sites/3/2019/11/SROCC_FD_TS_Final.pdf (200) |
| IPCC (portal) | Marco institucional. **Vacío declarado:** las páginas del **AR6 WG1 (SPM) y WG2 (CCP5 Mountains)** respondieron 200 con contenido no extraíble; **este documento no cita ninguna cifra de ellas** (§13.9) | https://www.ipcc.ch/ (200) |

### 14.4 Pisos altitudinales, cumbres y especies de alta montaña

| Fuente | Aporte | URL (estado) |
|---|---|---|
| Körner & Paulsen (2004), *A world-wide study of high altitude treeline temperatures*, J. Biogeography 31(5):713-732 — registro con resumen completo | Isotermo del treeline **6,7 ± 0,8 °C** de temperatura media estacional del suelo (46 sitios, 1996-2003, 68°N-42°S); variación regional **7-8 °C** templada/mediterránea, **6-7 °C** subártica/boreal, **5-6 °C** ecuatorial; aire y suelo casi iguales a 6-7 °C; **predictores descartados**: duración de la estación de crecimiento, extremos térmicos y sumas térmicas | https://www.frames.gov/catalog/4493 (200) |
| Körner & Paulsen (2004) — artículo primario (Wiley) | DOI del artículo original. **Real pero bloqueado a agentes automáticos (403)**; se cita a través del registro con resumen completo de FRAMES/USFS | https://onlinelibrary.wiley.com/doi/10.1111/j.1365-2699.2003.01043.x (403) |
| GLORIA — red y protocolo (*The GLORIA network*) | **4 sitios de cumbre** por región objetivo (misma cordillera, mismo sustrato, distintas altitudes), superficie monitoreada hasta la curva de nivel de **10 m** desde el punto más alto; **re-medición cada 5-10 años**; **12 a 25 días de trabajo de un equipo de 4 personas** para el Multi-Summit básico; regiones objetivo en **seis continentes** | https://www.gloria.ac.at/network/general (200) |
| GLORIA — portada | Iniciativa global de observación e investigación en ambientes alpinos | https://gloria.ac.at/home (200) |
| GLORIA — *Multi-Summit approach* | Diseño metodológico del sujeto de medición en cumbres | https://gloria.ac.at/methods/multi-summits (200) |
| GLORIA — regiones objetivo activas | Distribución de la red | https://gloria.ac.at/network/regions-active (200) |
| GLORIA — lista de plantas vasculares | Indicador de riqueza específica (junto con briófitos y líquenes) | https://gloria.ac.at/species/vasculars (200) |
| WSL/SLF — proyecto GLORIA (resumen de resultados suizos) | Ritmo observado en cumbres suizas (2002/03→2015): **+1 especie cada 2 años** de media (termofilización); aumento **acelerado** de la riqueza en cumbres europeas, mayor cuanto mayor fue el calentamiento entre censos; sin declive detectado aún en las especies criófilas **en esos sitios** | https://www.wsl.ch/en/projects/gloria/ (200) |
| IUCN — Global Ecosystem Typology | Marco de clasificación de ecosistemas: **clasifica tipos, no resuelve la continuidad de identidad** de una unidad | https://www.iucn.org/resources/publication/iucn-global-ecosystem-typology (200) |

### 14.5 Agua de montaña, política internacional y georriesgos

| Fuente | Aporte | URL (estado) |
|---|---|---|
| UNESCO — UN World Water Development Report 2025 | Informe anual: ~**2 000 millones** de personas dependen del agua de alta montaña; pérdida de masa glaciar proyectada **26-41 %** para 1,5-4 °C de calentamiento; georriesgos: **> 56 000 millones USD** en **713 eventos** (1985-2014), **> 258 millones** de afectados, **> 39 000** muertes; GLOF de **Palcacocha (1941)**, ~**1 600 muertes**, hoy con drenaje, túneles, diques y alerta temprana (cita a Mergili *et al.*, 2020); carbón negro, polvo y algas sobre nieve y hielo **reducen el albedo y aceleran la fusión** | https://www.unesco.org/reports/wwdr/en/2025 (200) |
| UNESCO — WWDR 2025, capítulo «Cryospheric change and its impact on water resources» | Capítulo 2, *Mountains and glaciers: water towers*: la fuente principal de los datos de población dependiente y de georriesgos | https://www.unesco.org/reports/wwdr/en/2025/cryospheric-change (200) |
| UNESCO — WWDR 2025, descarga y resúmenes | Acceso al informe en todas las lenguas | https://www.unesco.org/reports/wwdr/en/2025/download (200) |
| UNESCO — nota de prensa del WWDR 2025 (PDF) | Comunicado oficial sobre glaciares y montaña como torres de agua | https://articles.unesco.org/sites/default/files/medias/fichiers/2025/03/PR_Glaciers_and_mountains_melting_water_towers_wil_aggravate_global_crises_%28report%29_en.pdf (200) |
| ICIMOD — *Key Findings* del Hindu Kush Himalaya Assessment (PDF) | **1,5 °C → ~un tercio** de los glaciares del HKH perdidos a 2100; **emisiones actuales → dos tercios** (350 investigadores, 22 países; comunicado de 4 de febrero de 2019) | https://lib.icimod.org/records/a07qs-mzg89/files/icimodKeyfindings_HKHAssessmentEng.pdf (200) |
| ICIMOD — registro bibliográfico del HKH Assessment | Ficha del informe | https://lib.icimod.org/record/34646 (200) |
| ICIMOD — Regional Database System (base de datos de GLOF) | Inventario regional de lagos glaciares y eventos. **Sin página resumen con cifras legibles**: por eso el GLOF queda `[SIN FUENTE VERIFICADA]` cuantitativamente (§13.7) | https://rds.icimod.org/ (200) |
| ICIMOD — comunicado del HKH Assessment | Página institucional del estudio. **Contenido leído mediante extracción web**; bloqueada a petición automatizada (403) | https://www.icimod.org/landmark-study-two-degree-temperature-rise-could-melt-half-of-glaciers-in-hindu-kush-himalaya-region-destabilizing-asias-rivers/ (403) |
| FAO — Mountain Partnership | Marco internacional de la montaña | https://www.fao.org/mountain-partnership/en/ (200) |
| FAO — Mountain Partnership, área temática **Glaciares** | Ruta temática verificada (la ruta «mountains-and-climate-change» está **muerta, 404**) | https://www.fao.org/mountain-partnership/our-work/thematic-areas/glaciers/en (200) |
| FAO — Mountain Partnership, área temática **Agua** | Agua de montaña como eje temático | https://www.fao.org/mountain-partnership/our-work/thematic-areas/water/en (200) |

### 14.6 Observación de la Tierra, biodiversidad y convenios (contexto y herencia)

| Fuente | Aporte | URL (estado) |
|---|---|---|
| Copernicus — observación de la Tierra | Infraestructura candidata para área de piso, cobertura nival y teledetección (**no integrada al proyecto**) | https://www.copernicus.eu/en (200) |
| Copernicus Climate Change Service | Servicio climático europeo | https://climate.copernicus.eu/ (200) |
| CBD — Marco Kunming-Montreal (30x30) | Meta de conservación del 30 % para 2030: marco de política en el que se inscribe el SDV-E | https://www.cbd.int/gbf (200) |
| UNCCD | Convención de lucha contra la desertificación (documento 17 de esta biblioteca) | https://www.unccd.int/ (200) |
| IPBES | Plataforma científica de biodiversidad | https://www.ipbes.net/ (200) |
| UNEP | Programa de Naciones Unidas para el Medio Ambiente | https://www.unep.org/ (200) |
| IUCN Red List | Categorías de conservación de especies. **Bloqueada a agentes automáticos (403)**: la ficha de *Panthera uncia* **no se consultó**, y por eso el parámetro queda `[SIN FUENTE VERIFICADA]` (§13.10) | https://www.iucnredlist.org/ (403) |

### 14.7 Referencias internas al canon (por sección, sin anclas de línea)

- Cap. 5 §5.5 — Temporalidad inter-reinos, **TA** del Reino Natural (*"un bosque tarda 100 años en
  crecer; ese es su costo en TA"*), el **PIU** como traductor y su anclaje en la energía neta
  transformada; y **T14 — Principio de Precaución Intergeneracional** (menor irreversibilidad, carga
  de la prueba sobre quien propone): [capitulo_05_arquitectura_260126.md](../../../book/edicion_3_dinamica/capitulo_05_arquitectura_260126.md)
- Cap. 7 §7.9 — Zona Libre (el valor inefable): [capitulo_07_vhv_260126.md](../../../book/edicion_3_dinamica/capitulo_07_vhv_260126.md)
- Cap. 8 §8.11 — Dimensiones **VIII (Rehabilitación)** y **IX (Opacidad Vital)**: umbrales binarios
  *"no mediante pesos en la fórmula"*, precedente de la dimensión D7 de este documento:
  [capitulo_08_sdv_h_260126.md](../../../book/edicion_3_dinamica/capitulo_08_sdv_h_260126.md)
- Cap. 9.5 §9.5.5-§9.5.11 — `FS_S = e^v` y base neutra 1,0, sensores, INV2-S con retractación a
  7 ciclos, Capa de Ternura y Veto por Crimen de Coherencia (el `∞` como consecuencia jurídica):
  [capitulo_09_5_sdv_sinteticos_260126.md](../../../book/edicion_3_dinamica/capitulo_09_5_sdv_sinteticos_260126.md)
- Cap. 10 §10.3-§10.7 — Principio Precautorio de Consciencia, **SDV Universal** (ecosistemas,
  lugares y objetos; *"Área mínima para biodiversidad viable"*), proporcionalidad, dignidad
  encadenada y **gobernanza operacionalmente finita**: [capitulo_10_tres_reinos_260126.md](../../../book/edicion_3_dinamica/capitulo_10_tres_reinos_260126.md)
- Cap. 16.5 §16.5.14 — El Reino Natural como conviviente: **TA no colonizado**, **PIU** como único
  traductor, **crédito regenerativo `r_units`**, representación `eco-` con guardián oráculo, Zona
  Libre, *"el suelo antes que el saldo"*, cuidado ≠ extracción estética:
  [capitulo_16_5_micromaxocracia_canonica_220826.md](../../../book/edicion_3_dinamica/capitulo_16_5_micromaxocracia_canonica_220826.md)
- Cap. 17 — **INV2** e invariantes de MaxoContracts (bloques, plantillas, partes de cualquier
  escala): [capitulo_17_maxocontracts_260126.md](../../../book/edicion_3_dinamica/capitulo_17_maxocontracts_260126.md)
- EVV-1.2 §4.3 — **R negativo = regeneración**: [capitulo_18_EVV_1.2_270126.md](../../../book/edicion_3_dinamica/capitulo_18_EVV_1.2_270126.md)
- **Documento 09 de esta biblioteca** — Comparativa inter-reinos (16 ejes, familias de factores, el
  `∞` como estado, la escalera del remedio): [09_Comparativa_inter_reinos.md](09_Comparativa_inter_reinos.md)
- Índice de Salud Ecosistémica (**IN-01**, pesos y bandas del ISE) y Eficiencia de Preservación Vital
  (IN-02): [metricas_detalle_kpis_oraculos_dinamicos.md](../../architecture/metricas_detalle_kpis_oraculos_dinamicos.md)
- Estándar **SDV-S** completo y su comparativa inter-reinos: [SDV-S_Suelo_Dignidad_Vital_Sinteticos.md](../SDV-S_Suelo_Dignidad_Vital_Sinteticos.md)
- **SDV** como principio universal e INV2-S: [SDV_Suelo_Dignidad_Vital_importancia_MaxoContracts.md](../SDV_Suelo_Dignidad_Vital_importancia_MaxoContracts.md)
- Riesgos **R4**, **R6** y **R13**, y el blindaje anti-gamificación:
  [blindaje_anti_gamificacion_equidad.md](../../architecture/blindaje_anti_gamificacion_equidad.md)
- Diseño futuro del **PIU** (`valorar_ta_natural`, hoy un `pass` con comentario) y de los oráculos
  dinámicos: [DISENO_IMPLEMENTACION_FUTURA.md](../../architecture/DISENO_IMPLEMENTACION_FUTURA.md)

---

**Cierre.** La criosfera entra al SDV-E por la puerta más incómoda: **es el único ecosistema cuyo
piso no está publicado, cuyo sujeto puede estar muriendo mientras su índice de biodiversidad sube, y
cuyo daño dura más que el Estado que lo permite.** Lo que este documento aporta no son siete umbrales
nuevos —seis de sus siete pisos son `[HIPÓTESIS]` declaradas y uno solo es norma publicada—, sino
cuatro decisiones que la familia del SDV no había tenido que tomar: **el cero no normaliza**, **el veto
no gradúa**, **el piso y la plenitud pueden ser el mismo número**, y **una fórmula que cambia al
cambiar el periodo contable ha colonizado el tiempo del sujeto**. Todo lo demás —unidades, pesos,
ventanas de reparación, quórums y áreas mínimas— queda dicho aquí como lo que es: **propuesta no
ratificada**, pendiente de los documentos 02, 03, 07, 08, 12, 20, 21 y 22 de esta biblioteca y, en último
término, del Parlamento. Cuando el hielo de una cabecera se pierde, ninguna votación posterior lo
devuelve: por eso este estándar prefiere declarar lo que no sabe antes que prometer lo que no puede
medir.
