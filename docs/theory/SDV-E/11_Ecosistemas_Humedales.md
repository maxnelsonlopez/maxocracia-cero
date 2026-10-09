# Humedales — Suelo de Dignidad Vital del Reino Natural (SDV-E)
## Hidroperiodo, nivel freático, turba y carbono, aves acuáticas y calidad del agua: el régimen hídrico como piso y como identidad del sujeto, y los umbrales que sí tienen fuente

**Autoría:** Oráculo Sintético DeepSeek & Max Nelson López Restrepo
**Fecha:** octubre 2026
**Proyecto:** Maxocracia — El gobierno de la verdad, el tiempo y la vida
**Licencia:** Creative Commons BY-SA 4.0
**Estado:** Propuesta de estándar (rama SDV-E, Ola 4) — NO canon hasta ratificación
**Referencia canónica:** Cap. 10 §10.4 · Cap. 16.5 §16.5.14 · EVV-1.2 §4.3 · Cap. 9.5 (precedente SDV-S)
**Documento:** 11 de la biblioteca `docs/theory/SDV-E/` (Bloque B — SDV-E por tipo de ecosistema)
**Revisión:** octubre 2026 — redactado contra el informe de fuentes verificado de la rama
(`scratch/sdv_e/fuentes/11_humedales.md`, que **no es un documento de la biblioteca** y por eso no se
enlaza como si fuera canon) y contra lectura directa del repositorio. **Se comprobaron por HTTP las 38 URLs
con esquema que cita este documento, en esta misma sesión: 30 respondieron 200 y 8 respondieron 403**
(reales, rechazan clientes automáticos: un humano las abre). Ninguna respondió 404. El estado real de cada
una está en §14. **No se heredó ninguna cifra sin fuente y no se añadió ninguna cifra sin verificación.**

> **Fe de erratas de la revisión adversarial (octubre 2026).** Cinco defectos se detectaron y se corrigieron
> en su lugar: (1) el conteo de marcas `[SIN FUENTE VERIFICADA]` del cuerpo era erróneo —decía cinco y
> omitía cuatro umbrales marcados en las tablas de dimensión; el inventario correcto, nueve parámetros,
> está en §1 y §13—; (2) la fila de turberas de §4-II atribuía a Xu *et al.* (2018) cifras que el informe
> de fuentes asigna a **IUCN, 2021**, y omitía su «al menos **3 %**»; (3) el instrumento de aves se citaba
> con la URL de NABCI, que **no es su fuente**; (4) el valor 9,0 de pH de agua dulce figuraba como «Mínimo
> Absoluto» cuando es un **límite superior** (operador `range`); y (5) el **oxígeno disuelto** se declaraba
> «sin fuente verificada» cuando el documento [07](07_Formula_de_violacion_y_pesos.md) §5.3 de esta misma
> biblioteca **sí publica una cifra** (5,5 / 6,5 mg/L) y la marca **en disputa** con el documento 08 §5.2:
> la exclusión de este documento es **doctrinal**, y ahora se dice así, sin apoyarla en una ausencia de
> dato que no es cierta. **Ninguna corrección mueve un piso, un peso ni una cifra de fuente.**

---

## 1. Qué es (y qué no es) este SDV

**Qué es.** Este documento fija los mínimos del **ecosistema humedal** dentro del Suelo de Dignidad Vital
del Reino Natural: el régimen hídrico —hidroperiodo y nivel freático—, la turba, el carbono del depósito
orgánico, las aves acuáticas, la calidad del agua y la biota indicadora, por debajo de los cuales un
humedal **pierde integridad** y deja de sostener lo que sostiene. Es el documento que responde, para un
humedal, a la pregunta que el canon dejó abierta y que este ecosistema tiene el privilegio incómodo de
protagonizar:

> *"Un conjunto con crédito regenerativo acumulado pero humedal bajo su SDV-E no está en coherencia:
> **INV2-E será su juez**."* — Cap. 16.5 §16.5.14

Ése es el **caso canónico del proyecto**: el humedal del conjunto residencial del que habla el Cap. 16.5
§16.5.14. Este documento existe para que la frase tenga respuesta operativa, y la respuesta se da en §5.6
y §5.7 con aritmética a la vista. Y responde también a la definición positiva que el canon ya escribió
para este reino, que nombra a los humedales por su proceso y no por su biota:

> *"**SDV para Ecosistemas.** Un bosque tiene un SDV que incluye: Área mínima para biodiversidad viable ·
> Calidad del aire y agua · Conectividad con otros ecosistemas · Ciclos naturales respetados (fuego,
> inundación, sequía)"* — Cap. 10 §10.4

> *"**SDV para Lugares.** Un río tiene un SDV que incluye: Caudal mínimo ecológico · Calidad del agua
> (oxígeno, pH, contaminantes) · Riberas protegidas · Fauna acuática viable"* — Cap. 10 §10.4

De esas dos definiciones, este documento toma cinco elementos y declara qué hace con cada uno:
*calidad del agua* es la Dimensión VI; *conectividad* es la Dimensión VIII (con su piso procedural y su
vacío declarado); *ciclos naturales (inundación, sequía)* es la dimensión binaria sin peso B-I;
*fauna viable* es la Dimensión V, **restringida a las aves acuáticas por gremio** y con la advertencia que
la hace útil; y *calidad del aire* **no entra**: pertenece al documento 23 de esta biblioteca
(transversal de agua y aire) y aquí se declara la frontera en vez de duplicar la dimensión (§4, cierre).

**Qué no es.**

- **No es el estándar del SDV-E.** El estándar —unidad y sujeto, TA soberano, Zona Libre, guardián,
  fórmula, INV2-E— vive en los documentos 00-09 de esta biblioteca. Este documento es la **instancia de
  tipo de ecosistema**: aplica ese estándar al humedal y sólo al humedal.
- **No es el manual de Ramsar.** La Convención de Ramsar designa humedales de importancia internacional;
  el SDV-E mide si un humedal conserva integridad. **Son dos cosas distintas y su confusión es el error
  más caro que este documento puede evitar** (§4, B-II y R17 en §7.4): un humedal puede estar sano y no
  ser Ramsar, y puede ser Ramsar y estar degradado.
- **No es un catálogo de buenas prácticas de restauración.** Lo que sigue son parámetros con fuente, piso
  separado de óptimo, protocolo y **definición operativa de violación**. Lo que no tiene las cuatro cosas
  no entra como dimensión ponderada: entra como dimensión binaria sin peso, o como pregunta abierta
  (§13).
- **No es el documento de la contabilidad.** *"Estándar primero, contabilidad después"*
  (Cap. 16.5 §16.5.14). Aquí no hay fórmula ejecutable, ni bloque validador, ni sensor conectado: hay el
  piso que esa contabilidad tendrá que respetar. La §12 dice, sin adorno, que **nada de esto existe en el
  código**.
- **No es el documento del ISE.** El Índice de Salud Ecosistémica es un **tablero** de cinco componentes;
  el SDV-E es un conjunto de **mínimos por parámetro**. §5.4 y §12.3 demuestran que el tablero existente
  **no toca el eje maestro del humedal** (0,38 del peso de este documento) y que en un humedal puede
  subir mientras el piso cae.
- **No es canon.** Es propuesta de estándar de la rama SDV-E, Ola 4.

**Nota de lectura (por qué algunos documentos de esta biblioteca no son enlaces).** Existen y se enlazan
los documentos [02](02_Unidad_y_sujeto_del_SDV-E.md), [04](04_Zona_Libre_del_Reino_Natural.md),
[05](05_Representacion_guardian_y_mandato.md), [07](07_Formula_de_violacion_y_pesos.md),
[08](08_INV2-E_invariante.md), [09](09_Comparativa_inter_reinos.md), [10](10_Ecosistemas_Bosques.md),
[13](13_Ecosistemas_Oceanos_y_costas.md), [14](14_Ecosistemas_Suelos_vivos.md),
[16](16_Ecosistemas_Montanas_y_criosfera.md) y [18](18_Ecosistemas_Agroecosistemas.md). Los documentos
`00`, `01`, `03`, `06`, `12`, `15`, `17`, `19`-`24` y `40` están anunciados en el brief de la rama pero
**todavía no existen como archivo**: se citan por número y título, **sin enlace**, porque un enlace a un
archivo inexistente no es una referencia: es un error de trazabilidad.

**Marcas de evidencia usadas en todo el texto.** `[VERIFICADO]` = leído en la fuente citada o en el
archivo del repositorio. `[REPORTADO]` = afirmado por una fuente que cito sin haber podido abrir el
documento completo, o fuente cuyo contenido no es legible por la herramienta. `[HIPÓTESIS]` = inferencia
razonada del proyecto, no observación. `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` = se
buscó el umbral y no existe fuente verificable. **Las cuatro marcas son resultados legítimos**, y en este
documento la cuarta recae sobre **nueve parámetros distintos**: la frecuencia y duración del hidroperiodo
en días (§4-I), el espesor mínimo universal de turba (§4-III), el umbral de degradación del depósito en
t C/ha (§4-IV), la población viable por especie (§4-V), los umbrales de nitrógeno y fósforo (§4-VI), el
valor de corte del IBI y el de macroinvertebrados (§4-VII), la métrica cuantitativa de conectividad
hidrológica (§4-VIII) y el régimen de fuego del humedal (§13, pregunta 8). §1 nombra **cinco** de
ellos —los que recaen sobre el eje maestro y su vecindad— y **§13 es el inventario completo**. **El
oxígeno disuelto ya no está en esta lista**, y el cambio importa: no se excluye por falta de cifra sino
porque **medirlo en una turbera destruiría el objeto protegido** (§4-VI). **El más grave de los nueve es
el primero**: cae sobre el parámetro que este documento declara eje maestro y de mayor peso (0,20).

---

## 2. Preámbulo metodológico

El SDV-H lo tiene y el SDV-S lo omitió; el brief de esta biblioteca prohíbe repetir la omisión. En un
documento sobre humedales el preámbulo es además la defensa contra un error concreto y documentado: **las
métricas del agua miden agua, y un humedal no es agua.** Un embalse, un estanque ornamental y una turbera
comparten la palabra "húmedo" y no comparten ni un parámetro de los que aquí importan. Estas son las ocho
reglas con las que se escribió todo lo que sigue.

**Regla 1 — La definición no es el piso.** Existen definiciones legales y científicas de "humedal", y son
operativas: un área *"inundada o saturada por agua superficial o subterránea con una **frecuencia y
duración** suficientes para sostener —y que en circunstancias normales sostiene— una prevalencia de
vegetación típicamente adaptada a condiciones de suelo saturado"* (EPA, 40 CFR 120.2(c)(1))
[VERIFICADO]; el sustrato saturado *"el tiempo suficiente para desarrollar condiciones anaerobias en las
capas superiores"* (Queensland DETSI, 2023) [VERIFICADO]; y, en la definición de la Convención de Ramsar
art. 1.1, las *"aguas marinas cuya profundidad en marea baja no exceda **6 m**"* [VERIFICADO en la
transcripción de International Peatland Society, 2020, que coincide palabra por palabra con la
transcripción independiente de la fuente gubernamental de Queensland]. Todo eso marca **cuándo una
superficie empieza a contarse como humedal**: es el piso del *concepto*, no el piso de un humedal *sano*.
En este documento todo dato de definición va marcado `[DEFINICIÓN]` y **no puede convertirse en Mínimo
Absoluto sin decisión doctrinal explícita**. Y aquí hay una vuelta de tuerca que ningún otro documento de
esta biblioteca tiene: en el humedal, el criterio definitorio **es** el eje maestro, de modo que la
definición no se descarta — se convierte en **dimensión binaria auditable** (Dimensión I) en lugar de
convertirse en un número inventado. La decisión se explica en §4-I.

**Regla 2 — La política no es la ley.** La designación Ramsar, la meta de conservar el 30 % de las aguas
continentales para 2030 del Marco Kunming-Montreal (CBD, 2022) [VERIFICADO — URL de la Meta 3 en §14], la
tasa global de pérdida de **0,52 % anual** y el **22 %** de humedales perdidos desde 1970
(Convención de Ramsar, *Global Wetland Outlook 2025*) [VERIFICADO en la nota de prensa oficial] son
**datos de estado y política**, no umbrales de integridad de una unidad. Siguiendo la frontera LEY/POLÍTICA
del brief §3.3.12: **entran en la columna del Óptimo o en el contexto de calibración, nunca en la del
Mínimo Absoluto**.

**Regla 3 — Un promedio mundial no puede ser un piso local.** El mundo pierde humedales a **0,52 % anual**
y **1 de cada 4** humedales restantes está en **mal estado ecológico** (Ramsar, GWO 2025) [VERIFICADO].
Un agregado global que se mueve lentamente puede esconder la desaparición completa de una unidad, y en
EE. UU. —la serie nacional más larga publicada— la pérdida de **221.000 acres** entre 2009 y 2019
representó un **aumento de más del 50 %** respecto del estudio anterior (USFWS, 2024) [VERIFICADO]. Todo
piso de este documento es **local** (de la unidad declarada) o no es piso.

**Regla 4 — El indicador que sube puede ser el daño.** Ésta es la regla de medición propia del humedal y
se descubrió al leer la fuente, no al razonar sobre ella. En el mismo período 2009-2019 en que se
perdieron **670.000 acres** de humedal **vegetado** y **426.000 acres** de bosque de humedal de agua
dulce, los humedales **no vegetados** ganaron **488.000 acres** (**+7 %** de área de estanques); y los
patos nadadores y zambullidores —que usan **agua abierta**— muestran poblaciones **estables o en
aumento**, mientras **casi un tercio de las aves acuáticas** está en declive, incluidas garzas y rascones
**que dependen de marismas y humedales efímeros** (USFWS, 2024, citando *State of the Birds 2022*;
NABCI, 2022) [todo VERIFICADO]. **Consecuencia operativa, y es dura: el aumento del espejo de agua no es
señal de salud del humedal, y la abundancia total de aves acuáticas no es un indicador de cumplimiento.**
Es la versión limnológica de *"jardín podado para la foto no es cuidado; se registra lo que regenera, no
lo que adorna"* (Cap. 16.5 §16.5.14).

**Regla 5 — El tiempo del humedal es TA soberano.** *«Respetamos la soberanía del reino natural sobre su propio TA» (el PIU traduce)* (Cap. 16.5 §16.5.14). Ninguna métrica de este documento se expresa en TVI ni
en TPI. El **PIU** (Protocolo de Intercambio Universal, Cap. 5 §5.5) es el **único** traductor autorizado
entre el TA del humedal y el TVI humano, y **este documento no traduce nada**: fija el piso y declara que
la traducción es un acto aparte, con su propio registro. Dos consecuencias formales propias del humedal:
(a) **la unidad del ciclo TA no se elige por comodidad** —año hidrológico, año calendario, estación de
crecimiento y ciclo de sucesión son candidatos legítimos y ninguno tiene fuente verificada—, y (b) el piso
numérico del nivel freático **exige por definición un ciclo multi-anual**, porque la clase de drenaje del
IPCC se calcula sobre la **media anual de varios años** (§4-II). Elegir "año calendario" por comodidad de
implementación sería colonizar el tiempo del humedal con el calendario del municipio.

**Regla 6 — La carga de la prueba es de quien propone.** El **T14 — Principio de Precaución
Intergeneracional** (Cap. 5) es el axioma más fuerte disponible para este reino: *"Ante incertidumbre
sobre el impacto en agentes que no pueden consentir (ecosistemas, generaciones futuras, posibles
consciencias sintéticas), el sistema debe elegir la opción de menor irreversibilidad, documentando el
costo de oportunidad asumido. La carga de la prueba recae sobre quien propone acciones que afectan la
temporalidad de no-participantes."* Para un humedal esto no es inspiración: es la regla de decisión
cuando falta el dato — y falta en el parámetro central (Regla 8 y §4-I). Además tiene un anclaje
empírico que ningún otro ecosistema de esta biblioteca tiene: **drenar una turba la pierde
permanentemente del sistema y produce compactación y subsidencia del suelo, de modo que la hidrología
adecuada no se restaura sin manejo del nivel freático** (International Peatland Society, 2020)
[VERIFICADO], y *"pueden pasar décadas, siglos o más antes de que los humedales restaurados funcionen
como humedales naturales, si es que alguna vez lo hacen"* (USFWS, 2024) [VERIFICADO].

**Regla 7 — El territorio sostiene al humano; usarlo no es violarlo.** Un humedal que da agua, amortigua
inundaciones y sostiene pesca no está siendo violado por hacerlo. Por eso el factor de violación de este
documento vale **exactamente 1,0 cuando la violación es 0**, y no hereda el piso 0,2 del SDV-A. La
justificación completa está en el documento [09 de esta biblioteca](09_Comparativa_inter_reinos.md) §5.2;
aquí se aplica. El SDV-S tuvo que corregir `FS_S = 1,0 + e^v` porque la primera versión recargaba el
100 % incluso sin violación; **este documento no repite ese error**.

**Regla 8 — Cuatro estados, y uno de ellos es el que evita el fraude más fácil.** Un parámetro de un
humedal puede estar: (a) **cumpliendo** su piso; (b) **violándolo**; (c) **no aplicable** (p. ej. la
Dimensión III en un humedal mineral sin horizonte orgánico); (d) **sin dato**. El cuarto estado **no
castiga** —*"la duda sin evidencia no castiga"*, INV2-EDU— pero **tampoco suspende la ley**: *"mientras no
haya resolución, el canon manda"* (brief §3.3.10). Y este documento añade una prohibición simétrica que es
su regla más importante de medición: **está prohibido imputar violación a partir de una lectura
instantánea del nivel del agua.** Muchos humedales son estacionales —*"están secos una o más estaciones
cada año"*— y *"pueden estar húmedos solo periódicamente"*; incluso los que *"parecen secos durante partes
significativas del año, como las vernal pools, a menudo proveen hábitat crítico para fauna adaptada a
reproducirse exclusivamente en esas áreas"* (EPA, 2026) `[REPORTADO — el informe de fuentes de la rama
atribuye esta cita a la EPA (2026) sin fijar la URL exacta; véase §14.2]`. Un sensor de nivel que dispare
violación por lectura baja en estación seca **produciría falsos positivos sistemáticos**. Por eso el piso
se expresa **como régimen** (frecuencia, duración, estacionalidad), no como nivel instantáneo.

---

## 3. Pilares epistemológicos

El SDV-E hereda los pilares de la familia —proporcionalidad (Cap. 10 §10.5), dignidad encadenada
(Cap. 10 §10.6), precaución ante quien no puede consentir (Cap. 10 §10.3), no-antropocentrismo (T9) y los
cinco criterios de validación de parámetros— y añade cuatro que son específicos del humedal y que ningún
otro reino necesita.

**Pilar heredado que más trabaja aquí — gobernanza operacionalmente finita (Cap. 10 §10.7).** *"La
gobernanza debe ser operacionalmente finita"*: el SDV-E **no puede** exigir modelar la cadena trófica
completa del humedal para decidir. Un humedal es un sistema con miles de interacciones hidrológicas,
biogeoquímicas y tróficas; este documento elige **ocho dimensiones ponderadas y tres binarias** y declara
que lo demás no se modela. Finito y auditable.

**Pilar heredado que obliga aquí — dignidad encadenada (Cap. 10 §10.6).** *"Dignidad Humana ←→ Dignidad
Ecosistémica ←→ Dignidad Material. Cada eslabón depende de los demás."* Los humedales cubren **~6 %** de
la superficie terrestre y aportan **> 7,5 %** del PIB global (Ramsar, GWO 2025) [VERIFICADO]; la
proyección de la propia Convención es que hasta **20 %** de los humedales restantes podrían desaparecer
para 2050 poniendo en riesgo **39 billones USD** de beneficios (Ramsar, GWO 2025) [VERIFICADO]. El piso de
este documento no es un asunto "ambiental": es el eslabón material de los otros dos.

**Pilar propio 1 — El humedal es el ecosistema cuya definición de existencia es su régimen.** No es una
dimensión más: **es la variable de estado que decide si el sujeto existe**. Las tres definiciones
verificadas de §2-Regla 1 definen el humedal por *frecuencia y duración* de inundación o saturación, no
por su biota ni por su superficie. La consecuencia es dura y es el aporte doctrinal central de este
documento: **es el único caso del SDV-E en el que la violación del piso puede implicar cambio de identidad
del sujeto.** Si el régimen hídrico cae bajo el piso de forma sostenida, el humedal no "empeora": **deja
de ser humedal** y se transforma en otra cosa —lo que el documento [02 de esta biblioteca](02_Unidad_y_sujeto_del_SDV-E.md)
§C4 formaliza como **colapso**, siguiendo la Lista Roja de Ecosistemas de la UICN: *"una transformación de
identidad"*, y *"a diferencia de las especies, los ecosistemas no desaparecen; se transforman en
ecosistemas novedosos"* `[HIPÓTESIS de encuadre: la premisa es de las fuentes; la aplicación al humedal
como caso de cambio de identidad es de este documento]`. Y hay un segundo filo, que este documento declara
en lugar de esconder: **un humedal puede convertirse en tierra firme sin intervención humana.** *"Los
humedales son sistemas dinámicos, que forman parte del continuo hidroserial desde el agua abierta hasta la
tierra firme, un proceso que toma miles de años y del cual no todas las etapas pueden estar evidentes en
cada localidad"* (International Peatland Society, 2020) [VERIFICADO]. Distinguir la terrestrialización
natural del drenaje antrópico es un problema abierto y está en §13 (pregunta 10).

**Pilar propio 2 — La anoxia es definitoria, no patológica: un parámetro candidato queda prohibido.** Es
el pilar más contraintuitivo del documento. El oxígeno disuelto es, para el canon, un parámetro explícito
de la calidad del agua (Cap. 10 §10.4) y el documento [07 de esta biblioteca](07_Formula_de_violacion_y_pesos.md)
§5.3 le asigna 2 % de tablero precisamente porque carece de umbral verificado. En un humedal, además,
**medirlo mal destruye el objeto que se dice proteger**: la condición *ácuica* —capas *"virtualmente
libres de oxígeno disuelto con ambiente reductor"*— es **criterio definitorio** de suelo de humedal
(Queensland DETSI, 2023; IPCC, 2014, glosario, entrada *Aquic*) [VERIFICADO], y la anoxia es la **causa**
de que exista turba: *"las condiciones de anegamiento permanente frenan la descomposición vegetal hasta
tal punto que las plantas muertas se acumulan formando turba"* (IUCN, 2021) [VERIFICADO]. **Un SDV-E que
exija oxígeno disuelto alto en una turbera destruiría el ecosistema que dice proteger.** Por eso este
documento **excluye el oxígeno disuelto de sus pisos** y declara la exclusión como decisión doctrinal, no
como falta de dato (§4-VI). Ningún otro estándar de la familia prohíbe un parámetro que podría medir.

**Pilar propio 3 — El hidroperiodo no es observable directo; sus indicadores sí.** El hidroperiodo —la
duración, frecuencia, profundidad y estacionalidad del anegamiento— es un **histórico**, no una lectura.
La fuente gubernamental que sí se pudo leer lo resuelve con una **lista cerrada de indicadores**: basta
**uno** de —observación directa de saturación o inundación; patrones topográficos de drenaje; vegetación
dominada por plantas indicadoras de humedal; suelos de humedal; microrelieve (*hummock* de pantano);
mantos de algas; raíces aéreas; marcas de inundación; restos vegetales transportados por agua; líneas de
limo; marcas de agua— (Queensland DETSI, *Queensland Wetland Delineation Guideline* v2) [VERIFICADO]. Eso
convierte el eje maestro en **auditable sin cifra**: no se mide el régimen, se verifica su **huella**. Es
exactamente la forma de la dimensión binaria canónica (Cap. 8 §8.11) y es la única forma honesta de tener
un piso del eje maestro en 2026.

**Pilar propio 4 — El humedal pierde volumen, no sólo tiempo.** En el bosque la irreversibilidad se mide
en años (*"un bosque tarda 100 años en crecer"*, Cap. 5 §5.5). En el humedal se mide en **centímetros**:
la turba drenada se oxida y *"se pierde permanentemente del sistema"*, y el proceso *"también produce
compactación y subsidencia del suelo"* (International Peatland Society, 2020) [VERIFICADO]. **La
subsidencia es pérdida de volumen del suelo: no se recupera rehumedeciendo.** Esto ancla T14 en una
unidad física medible —cm de turba y cm de subsidencia— y es la razón de que la Dimensión III tenga piso
de pérdida neta cero (§4-III), de que la Dimensión IV mida un stock y no un flujo (§4-IV), y de que la
Capa de Ternura no tenga análogo aquí (§8.4).

**Corolario de honestidad.** De las **ocho dimensiones ponderadas** de este documento: **una** (II) tiene
piso numérico con fuente verificada y es una **decisión de traducción declarada**; **una** (VI) tiene
piso numérico con fuente verificada y aplicable directamente; **cuatro** (III, IV, V, VII) tienen piso
como **no-regresión** respecto de una línea base declarada; y **dos** (I, VIII) tienen piso
**procedural/binario**. **Ninguna** de las ocho tiene un umbral publicado y verificado del tipo "éste es
el valor por debajo del cual el humedal **pierde integridad**". La precisión importa y se escribe: la
Dimensión VI **sí** tiene criterios numéricos publicados (pH, alcalinidad, sulfuro, hierro, cloruro) y lo
que no existe es un umbral de **integridad del humedal como tal**; los de la VI son criterios de
**protección de vida acuática**, un objeto distinto que la propia EPA advierte que puede no ser el
instrumento adecuado para juzgar un humedal. Y la dimensión de
**mayor peso del eje maestro —el hidroperiodo— es precisamente la que no tiene cifra**. Eso no es un fracaso de la redacción:
es el estado de la ciencia de humedales, y este documento lo dice con el conteo hecho.

---

## 4. Dimensiones del SDV-E (humedales)

**La unidad de aplicación.** Este documento aplica al **tipo de ecosistema "humedal"** y se evalúa sobre
una **unidad declarada** (la parte `eco-` instanciada sobre un territorio, con área de referencia
declarada). El problema de la unidad —dónde termina un humedal y empieza otro, si el sujeto es el tipo, la
cuenca o el lugar— **no lo resuelve este documento**: pertenece al documento
[02 de esta biblioteca](02_Unidad_y_sujeto_del_SDV-E.md), y aquí se opera con una unidad declarada y un
**área de referencia inmutable**. Pero este documento sí aporta la regla técnica que fija **por qué el
sujeto se define por tipo y no por superficie**: la autoridad ambiental de referencia lo exige
metodológicamente —*"los humedales solo se comparan con otros humedales del mismo tipo"* (EPA) [VERIFICADO]—,
de modo que **el tipo de humedal es un metadato obligatorio** (§6.3, campo 3) y la comparación entre
humedales de tipo distinto es una violación de método, no una imprecisión.

**Las ocho dimensiones ponderadas.**

| # | Dimensión | Qué mide | Peso |
|---|---|---|---|
| **I** | Hidroperiodo: frecuencia, duración, profundidad y estacionalidad | Si el humedal sigue anegándose como un humedal | 0,20 |
| **II** | Nivel freático y gradiente de drenaje | Si el agua sigue donde tiene que estar | 0,18 |
| **III** | Turba: espesor, permanencia y subsidencia | Si se está perdiendo lo que no vuelve | 0,12 |
| **IV** | Carbono del depósito orgánico (y su exportación acuática) | Si la turbera sigue siendo sumidero | 0,10 |
| **V** | Aves acuáticas por gremio (el gremio vegetado es el vinculante) | Si el humedal sigue siendo hábitat | 0,10 |
| **VI** | Calidad del agua (con la exclusión doctrinal del oxígeno) | Si el agua sigue siendo habitable | 0,12 |
| **VII** | Biota indicadora: vegetación hidrófita y macroinvertebrados | Si la comunidad dice lo mismo que el sensor | 0,08 |
| **VIII** | Conectividad hidrológica (cuenca, acuífero, humedales vecinos) | Si el humedal sigue conectado a su agua | 0,10 |
| | **Suma** | | **1,00** |

**Las tres dimensiones binarias sin peso.**

| # | Dimensión | Qué registra | Peso |
|---|---|---|---|
| **B-I** | **Ciclos naturales: inundación y sequía** | Presencia/ausencia de régimen declarado; la sequía estacional **no** es violación | **0,00** |
| **B-II** | **Eje de designación Ramsar** | Si la unidad es de importancia internacional — y **no** si está sana | **0,00** |
| **B-III** | **Zona Libre del humedal** (lo que no se mide) | Presencia/ausencia del derecho a no ser medida | **0,00** |

El precedente de las binarias es canónico y explícito: las dimensiones VIII (Rehabilitación) y IX
(Opacidad Vital) del SDV-H *"se registran cualitativamente y mediante umbrales binarios (presencia/ausencia
del derecho), no mediante pesos en la fórmula — medir la rehabilitación o la opacidad con la misma vara
cuantitativa que el agua o la vivienda las destruiría"* (Cap. 8 §8.11). El desarrollo de la Zona Libre del
Reino Natural está en el documento [04 de esta biblioteca](04_Zona_Libre_del_Reino_Natural.md): **aquí se
aplica, no se reinventa** (§10).

**Lo que NO entra como dimensión, y por qué (fronteras declaradas).**

| Elemento del canon o del tablero | Dónde vive | Por qué no es dimensión de este documento |
|---|---|---|
| *"Calidad del aire"* (Cap. 10 §10.4) | Documento 23 de esta biblioteca (transversal de agua y aire) | Un humedal no es sujeto de la calidad del aire; su vía de efecto es el **depósito atmosférico de nutrientes**, y no se verificó umbral en esta sesión → §13, pregunta 7. El ISE le da **20 %** de su peso: para un humedal, eso es 20 % midiendo otra cosa |
| *"Riberas protegidas"* (Cap. 10 §10.4, definición de **lugar**) | Documento 12 de esta biblioteca (ríos y cuencas) | Aplica al humedal ribereño como condición de su hidroperiodo; aquí entra por la Dimensión I (presiones) y no como dimensión propia |
| *"Fauna acuática viable"* (Cap. 10 §10.4) | Este documento, **restringido a aves acuáticas por gremio** (Dimensión V) | Los peces y anfibios pertenecen al documento 12 (ríos) y al 13 (océanos y costas). La restricción se declara: **es un recorte de alcance, no una afirmación de que el resto no importa** |
| *"Área mínima para biodiversidad viable"* (Cap. 10 §10.4) | Documento [02](02_Unidad_y_sujeto_del_SDV-E.md) (criterio C3, escala) | No existe umbral verificado de superficie mínima de humedal; el documento 02 lo declara como hueco |

---

### Dimensión I: Hidroperiodo — frecuencia, duración, profundidad y estacionalidad (*el eje maestro, y el piso que no tiene cifra*)

**Qué protege.** Que el humedal siga anegándose y saturándose con la frecuencia, la duración y la
estacionalidad que lo constituyen como humedal. Es el eje maestro: no mide el estado del humedal, mide
**si el sujeto sigue existiendo** (§3, Pilar propio 1).

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **Régimen hídrico declarado** (frecuencia, duración, profundidad, estacionalidad) | **Existencia de la declaración**, con fuente o determinación local documentada (piso procedural) | Régimen declarado con serie histórica y sin presiones antrópicas activas | Consecuencia del concepto de *"frecuencia y duración suficientes"* — EPA, 40 CFR 120.2(c)(1) [VERIFICADO] |
| **Huella del régimen en el sustrato** (condición *ácuica*) | **Presencia**: capas superiores del suelo *"virtualmente libres de oxígeno disuelto con ambiente reductor"* — anoxia desarrollada | Suelo de humedal con horizonte de turba dentro de los primeros **0,3 m** | Queensland DETSI, 2023; IPCC, 2014 (glosario, *Aquic*); Queensland DETSI, *Delineation Guideline* v2 [VERIFICADO] |
| **Indicadores de hidroperiodo** (si no hay registro continuo) | **Basta uno** de la lista cerrada: saturación o inundación observada · patrones topográficos de drenaje · vegetación dominada por plantas indicadoras · suelos de humedal · microrelieve · mantos de algas · raíces aéreas · marcas de inundación · restos vegetales transportados por agua · líneas de limo · marcas de agua | Registro continuo del régimen con piezómetros y escala limnimétrica | Queensland DETSI, *Delineation Guideline* v2 [VERIFICADO] |
| **Umbral numérico de frecuencia y duración** (días, o % de la estación de crecimiento) | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` — el *Corps of Engineers Wetlands Delineation Manual* (1987) y sus suplementos regionales existen y están referenciados, pero el dominio `mvp.usace.army.mil` **devolvió HTTP 403 a los clientes automáticos en esta sesión** (URL completa en §14.2) | — | U.S. Army Corps of Engineers **(403, real, no legible por bot)** |
| **Profundidad de la lámina** `[DEFINICIÓN]` | **≤ 6 m** en marea baja (criterio de inclusión de aguas marinas en la definición de humedal) — **es definición, no salud** | — | Convención de Ramsar art. 1.1 (1971), transcripción de International Peatland Society, 2020 [VERIFICADO] |
| **Presiones que modifican el régimen** (taxonomía de la violación) | **Cero presiones de la lista aplicadas sin expediente T14** — familias con código: **H2-M5** cultivo en humedal · **H2-M9-a/b/c** drenaje parcial · **H2-M10-a/c** excavación en cauce · **H2-M11-a/b/c/d** excavación fuera de cauce · **H2-M6-a/b/f** hidrología superficial controlada · **H2-M13** canal construido · **H2-M7** canal construido en humedal · **H3-C1/C2-a/b/C4/C5-a/b** creación de humedal artificial | Ausencia de presiones activas | Queensland DETSI (WetlandInfo), 2023 [VERIFICADO] |
| **Referencia de estado (no umbral): el mundo** | — | — | **0,52 %/año** de pérdida · **22 %** perdido desde 1970 · **1 de cada 4** humedales restantes en mal estado ecológico · hasta **20 %** más perdido para 2050 (Ramsar, GWO 2025) [VERIFICADO] |

**Justificación.** Esta dimensión tiene el peso más alto del documento (0,20) y **ninguna cifra**, y hay
que defender las dos cosas por separado.

*Por qué el peso más alto.* Porque la definición de humedal **es** el régimen. Las tres definiciones
verificadas (§2-Regla 1) definen el humedal por frecuencia y duración de inundación o saturación y por la
vegetación o el sustrato que eso sostiene; ninguna lo define por superficie ni por especie. Es la única
dimensión de este documento cuya violación puede cambiar la **identidad** del sujeto.

*Por qué no hay cifra.* Porque el umbral numérico de días o de porcentaje de la estación de crecimiento
vive en el *Corps of Engineers Wetlands Delineation Manual* (1987) y en sus suplementos regionales, y
**no se pudo leer**: `usace.army.mil` devolvió **403** a los clientes automáticos en esta sesión, y
`usgs.gov` —que publica la definición de hidroperiodo— devolvió **403** en todas las rutas probadas (ambas
URLs se listan en §14.2 con su código). **No se inventa el número.** Lo que sí existe, y es suficiente
para un piso auditable, es la **huella** del régimen: la condición ácuica del sustrato y la lista cerrada
de once indicadores aceptados, que la fuente gubernamental de Queensland publica como método oficial de
delimitación [VERIFICADO]. De ahí la forma del piso: **procedural + binario**, no numérico.

*Y una precisión que evita el error más probable.* El **≤ 6 m** de Ramsar y el *"tiempo suficiente para
desarrollar condiciones anaerobias"* de Queensland **no son pisos de salud**: el primero decide qué aguas
entran en la definición de humedal y el segundo decide cuándo un sustrato es de humedal. Usar cualquiera
de los dos como "nivel mínimo de dignidad" sería exactamente el error que el brief §2.1 prohíbe con el
agua del SDV-H (tomar el Óptimo por el Mínimo) cometido en otra dirección: tomar la **definición** por el
**piso**.

**Protocolo.** Tres niveles, y no los inventa este documento: la arquitectura es la de la EPA —
**Nivel 1** evaluación de paisaje con inventario y teledetección (clasificación del tipo de humedal);
**Nivel 2** protocolos rápidos a escala de sitio, **validados y calibrados contra el Nivel 3**;
**Nivel 3** evaluación intensiva de sitio con índices multi-métrica derivados de investigación (enfoque
hidrogeomórfico HGM y evaluaciones biológicas) [VERIFICADO]. Para el régimen se combinan: (a) **registro
continuo** si existe (piezómetro + escala limnimétrica, con fecha de inicio declarada); (b) si no existe,
**la lista de indicadores de la tabla** —basta uno—; y (c) **el catálogo de presiones** de Queensland como
**registro de causas** (T13): cada familia de presión aplicada a la unidad se anota con su código y con el
expediente de T14 que la autorizó. Componentes del ciclo del agua que la fuente estructura como procesos
y que aquí funcionan como lista de verificación de la medición: precipitación, escorrentía e infiltración,
evaporación y evapotranspiración, descarga de agua subterránea, recarga, inundación, sedimentación y
estratificación (Queensland DETSI, 2023) [VERIFICADO]. **Frecuencia declarada:** la del ciclo TA de la
unidad (§6.3, campo 2), y **al menos un ciclo por año hidrológico declarado**. Quién reporta: la parte
`eco-` con la **comunidad testigo** verificando la declaración del régimen (§7.3).

**Violación.**
(a) **No existe régimen declarado** para la unidad (violación procedural: no se puede cumplir ni violar un
régimen que no se ha enunciado);
(b) **no se cumple ninguno de los once indicadores** de la tabla y **no hay registro continuo** que
demuestre anegamiento o saturación dentro del ciclo;
(c) **cualquier presión del catálogo aplicada sin expediente T14** —drenaje, canal, excavación, cultivo en
el humedal, hidrología superficial controlada—, con independencia de que el espejo de agua se conserve;
(d) **imputar violación a partir de una lectura instantánea** baja de nivel o de una estación seca
**declarada en el régimen** — prohibido por §2-Regla 8: es el falso positivo que el estándar debe
bloquear, no producir;
(e) **usar el criterio `≤ 6 m` de Ramsar** o la condición ácuica **como umbral de salud**, o declarar
cumplimiento del hidroperiodo **contando superficie de agua** (Regla 4).

---

### Dimensión II: Nivel freático y gradiente de drenaje (*el único número del eje maestro*)

**Qué protege.** Que el agua subterránea siga sosteniendo la saturación del sustrato. Es la cara
**subsuperficial** del eje maestro y la única parte de él que tiene cifra.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **Profundidad media anual del nivel freático** | **< 30 cm** bajo la superficie — permanecer en la clase *"shallow-drained"* (drenado somero). La clase *"deep-drained"* (drenado profundo) es **≥ 30 cm**. La media es **sobre varios años** | Nivel freático **cerca de la superficie del suelo** en condiciones naturales, con fluctuaciones estacionales admitidas | IPCC, *2013 Supplement to the 2006 IPCC Guidelines: Wetlands* (publicado 2014), Cap. 2 §2.1 y Glosario, entrada *Drainage class* [VERIFICADO] |
| **Horizonte de turba como indicador de saturación** | **Presencia de turba dentro de los primeros 0,3 m** de la superficie (umbral de **detección**) **+ registro del espesor** | Espesor en aumento (acumulación neta) | Queensland DETSI, *Delineation Guideline* v2 [VERIFICADO]. **Aviso de no duplicación, añadido en la revisión adversarial:** los **0,3 m** de esta fila, los del Óptimo de la Dimensión I y los de la Dimensión III son **el mismo número de la misma fuente** (Queensland) usado con tres funciones distintas —detección de suelo de humedal, contraste de la huella del régimen y umbral de detección de turba—. **No son tres indicadores independientes y no deben contarse como tres señales**: la Dimensión III es la que manda sobre el espesor, y esta fila es sólo la lectura de saturación |
| **Duración de la serie** | **Varios años** (la clase del IPCC se define sobre la media anual de varios años) | Serie plurianual con estaciones de referencia | IPCC, 2014, Cap. 2 §2.1 [VERIFICADO] |
| **Traducción declarada del umbral de 30 cm** | `[HIPÓTESIS]` — **decisión del proyecto**, declarada como tal | — | El IPCC define las clases de drenaje para **inventario de GEI**; **no dice** que 30 cm sea el mínimo de dignidad de un humedal |
| **Referencia de estado (no umbral)** | — | — | Turberas: **4,23 millones de km² = 2,84 %** de la superficie terrestre; **~84 %** en estado natural o casi natural y **~16 %** drenadas (= **0,5 %** de la superficie terrestre) — estimación *PEATMAP* (**Xu *et al.*, 2018**), vía International Peatland Society, **200** [VERIFICADO]. Segunda estimación independiente (**IUCN, 2021**): **al menos 3 %** de la superficie terrestre; **> 3 millones de km²** de turbera casi natural; **hasta 44 %** de todo el carbono del suelo; **> 600 Gt C** en suelos de turba [VERIFICADO]. **Las dos cifras de extensión no son sinónimos ni se promedian: son dos estimaciones distintas y así se reportan** |

**Justificación.** Dos razones, y la segunda obliga a declarar la primera.

1. **Es el único umbral numérico verificado que mide el eje maestro de forma continua y auditable.** El
   IPCC formaliza el nivel freático en dos clases operativas con frontera en **30 cm** (media anual sobre
   varios años): *shallow-drained* y *deep-drained* [VERIFICADO]. Con él, el déficit normalizado del
   brief §3.3.9 **sí se puede calcular sin inventar nada**: `requerido = 30 cm`, operador `max`,
   `déficit = max(0, (actual − 30)/30)`. Un humedal con nivel freático medio anual de 45 cm tiene un
   déficit de **0,5000** en esta dimensión.
2. **Y con él se puede decir algo que ninguna otra dimensión permite: el piso exige un ciclo
   multi-anual.** La clase se define sobre la media anual **de varios años**, de modo que **un solo ciclo
   estacional no puede producir violación por esta dimensión**. Ésa es la traducción aritmética de la
   Regla 8 y del hecho documentado de que los humedales estacionales están secos parte del año: el
   estándar **no puede** disparar por una estación seca, y la forma del umbral lo impide por construcción
   y no por buena voluntad del implementador. Es el aporte metodológico más importante de esta
   investigación.

**La advertencia que hay que dejar escrita, porque es la honestidad del dato.** El IPCC usa las clases de
drenaje para **inventario de emisiones**, no como estándar ecológico. Usar **30 cm** como piso del SDV-E
es una **decisión de traducción del proyecto**: legítima, verificable y **no ratificada por la fuente**.
El IPCC dice qué es "drenado somero" para contabilizar GEI; **no dice** que 30 cm sea el mínimo de
dignidad del humedal. Por eso la fila está marcada `[HIPÓTESIS]` y la pregunta 2 de §13 queda abierta.
Presentar este número como si fuera un umbral ecológico publicado sería la violación más grave posible de
la Regla de Oro de esta biblioteca.

**Protocolo.** Piezómetros o freatímetros en **al menos tres puntos** de la unidad declarada (borde,
centro y zona de descarga, si la topografía lo permite), con lectura **al menos mensual** durante años
consecutivos; se reporta la **media anual**, el **número de años** de la serie y la **fecha de inicio**.
En turberas se añade **calicata o barreno** para registrar el **espesor del horizonte de turba** y su
profundidad de techo, con método declarado. **El dato no es admisible sin los campos 4 y 5 de §6.3**
(número de años de la serie y profundidad de la turba): sin ellos, dos unidades con el mismo número no son
comparables. Quién reporta: la parte `eco-` con verificación de la comunidad testigo; la **medición** no
la hace el guardián oráculo (§7.2). Frecuencia declarada: anual para la media, **plurianual para la
clase**.

**Violación.**
(a) **media anual del nivel freático ≥ 30 cm** (clase *deep-drained*) en la unidad, sostenida en el ciclo
declarado de varios años;
(b) **ausencia de serie plurianual** presentada como cumplimiento (declarar "cumple" con una campaña de un
verano es declarar sin dato: estado (d), no estado (a));
(c) **drenaje, canalización o extracción de agua subterránea** que baje el nivel freático, aunque el
espejo de agua superficial se mantenga alimentado artificialmente;
(d) **reportar nivel freático sin declarar el número de años de la serie** o sin declarar el método
(piezómetro, calicata, sensor), lo que vuelve el número no auditable;
(e) **usar el umbral de 30 cm del IPCC como si fuera un umbral ecológico publicado**, omitiendo que es
una decisión de traducción del proyecto.

---

### Dimensión III: Turba — espesor, permanencia y subsidencia (*lo que no vuelve con rehumedecer*)

**Qué protege.** El depósito orgánico acumulado durante milenios: que no se pierda, porque **la pérdida
es irreversible en el sentido de T14**.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **Espesor del horizonte de turba** (cm) | **Pérdida neta = 0** respecto de la línea base declarada de la unidad (piso cero, §5.1) | **Aumento** del espesor: producción de materia orgánica > descomposición | International Peatland Society, 2020 (*"la producción de materia orgánica excede su descomposición, lo que resulta en una acumulación neta de turba"*) [VERIFICADO] |
| **Subsidencia del suelo** (cm) | **0 cm de subsidencia atribuible al drenaje** | 0 | IPE, 2020: el drenaje produce *"compactación y subsidencia del suelo, dificultando restaurar la hidrología adecuada sin manejo del nivel freático"* [VERIFICADO] |
| **Umbral de espesor que define "turba"** | **`[SIN FUENTE VERIFICADA]` como mínimo universal — y la fuente explica por qué no existe**: el IPCC *"no define un espesor mínimo del horizonte orgánico, para permitir definiciones nacionales de suelo orgánico"*, con **un único criterio mencionado de 10 cm**; **"los países pueden definir turba según sus circunstancias nacionales"** | Umbral **de la unidad**, declarado y votado (POLÍTICA) | IPCC, 2014, Glosario, entradas *Organic soil* y *Peat* [VERIFICADO] |
| **Umbral de detección en campo** `[DEFINICIÓN]` | Turba **dentro de los primeros 0,3 m** = indicador de suelo de humedal (umbral de **detección**, no de salud) | — | Queensland DETSI, *Delineation Guideline* v2 [VERIFICADO] |
| **Definición de turba** `[DEFINICIÓN]` | *"Depósito blando, poroso o comprimido, sedentario, del cual una porción sustancial es material vegetal parcialmente descompuesto, con alto contenido de agua en estado natural (hasta ~90 %)"* | — | IPCC, 2014, Glosario, entrada *Peat* [VERIFICADO] |
| **Referencia de estado (no umbral): daño por drenaje** | — | — | **1,9 Gt CO₂e/año** emitidos por turberas drenadas = **5 %** de las emisiones antropogénicas globales de GEI con sólo **0,3 %** de la superficie terrestre; *"en algunas regiones, hasta 80 % de las turberas han sido dañadas"* (IUCN, 2021) [VERIFICADO] |

**Justificación — y aquí el documento tiene un hallazgo doctrinal, no un vacío.** La pregunta "¿cuál es el
espesor mínimo de turba para que un humedal sea turbera?" **no tiene respuesta universal, y la fuente dice
por qué**: el IPCC permite definiciones nacionales y la IUCN lo confirma como problema de política —*"la
definición de turberas varía entre países y a menudo excluye áreas de valor para la industria… las
definiciones de turberas deberían priorizar la conservación, la restauración y el manejo sostenible"*
(IUCN, 2021) [VERIFICADO]. **Consecuencia para el SDV-E, y es la conclusión más limpia de este documento:
el umbral de turba es POLÍTICA (votable, de la unidad concreta), no un mínimo universal de LEY.** No es
una preferencia del proyecto: es **instrucción de la fuente**. Éste es el caso más claro de la biblioteca
en que la frontera LEY/POLÍTICA no la fija el proyecto sino el estado del conocimiento.

Y **lo que sí es LEY**, porque la física lo fija: **la pérdida de turba es irreversible**. La turba
drenada *"se seca y se oxida gradualmente a CO₂, y se pierde permanentemente del sistema"*; con el tiempo
el proceso produce **compactación y subsidencia**, y la hidrología no se restaura sólo rehumedeciendo
(International Peatland Society, 2020) [VERIFICADO]; *"pueden pasar décadas, siglos o más antes de que los
humedales restaurados funcionen como humedales naturales, si es que alguna vez lo hacen"* (USFWS, 2024)
[VERIFICADO]. Por eso el piso es **pérdida neta cero**, medido contra la línea base declarada de la
unidad: es la única forma de piso que la irreversibilidad admite (§5.1, piso cero).

**Protocolo.** Barreno o calicata con **profundidad de sondeo declarada** y **método declarado**; registro
del **techo** y del **espesor** del horizonte de turba; repetición en **los mismos puntos** (la
comparabilidad exige puntos fijos y fechados); en turberas drenadas, **nivelación topográfica de precisión
o GNSS** para medir subsidencia, con línea base fechada. Frecuencia mínima: la del ciclo TA declarado;
anual en unidades con presión de drenaje activa. Quién reporta: la parte `eco-` con verificación de la
comunidad testigo. **Regla dura del protocolo: no se acepta ningún reporte de turba sin profundidad de
sondeo y método** —el mismo principio que el documento [10](10_Ecosistemas_Bosques.md) §6.3 fijó para la
profundidad del suelo en el carbono edáfico—.

**Violación.**
(a) **pérdida neta de espesor de turba > 0** respecto de la línea base declarada, en un ciclo de medición;
(b) **subsidencia medible** atribuible al drenaje (compactación del depósito orgánico);
(c) **reportar espesor de turba sin declarar profundidad de sondeo, método y puntos de medición** (dato no
auditable: se trata como estado (d), sin dato, y activa bandera de opacidad, §6.4);
(d) **usar el criterio de detección de 0,3 m como umbral de salud**, o **elegir el umbral nacional de turba
después de conocer el resultado** (fijar la POLÍTICA a la medida del interés, sin expediente ni T13);
(e) **invocar la restauración futura** de la turbera como equivalente de la turba perdida (§9).

---

### Dimensión IV: Carbono del depósito orgánico (*el carbono que no sólo se emite: se exporta*)

**Qué protege.** Que la turbera siga siendo **sumidero neto** y no fuente; y que la pérdida se mida
entera, incluida la que sale por el agua.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **Stock de carbono orgánico del depósito** (t C/ha, **con la profundidad declarada**) | **No pérdida neta** respecto de la línea base declarada de la unidad (piso cero) | Aumento del stock | IPCC, 2014, Cap. 2 (suelos orgánicos drenados: el marco contable del stock y sus pérdidas) [VERIFICADO]; IUCN, 2021 (turbera húmeda = sumidero neto con efecto de enfriamiento) [VERIFICADO] |
| **Balance de la turbera** | **Sumidero neto** (turbera húmeda) o, como mínimo, **no fuente** atribuible al drenaje | **0,37 Gt CO₂/año** es la referencia mundial de secuestro de las turberas casi naturales (IUCN, 2021) [VERIFICADO] — **referencia global, no umbral local** | IUCN, 2021 [VERIFICADO] |
| **Exportación acuática de carbono** (DOC, POC, DIC) y CH₄ de zanjas | **Declaración obligatoria** del flujo por vía acuática cuando la unidad está drenada | — | IPCC, 2014, Cap. 2: pérdidas de carbono de suelos orgánicos drenados por **DOC** (carbono orgánico disuelto), **POC** (particulado) y **DIC** (inorgánico disuelto), con factores de flujo (Tabla 2A.2) y factores de emisión de CH₄ en zanjas (Tabla 2A.1) [VERIFICADO] |
| **Emisión por quema de suelo orgánico** | **Declaración obligatoria** de superficie quemada de turba y consumo de combustible | 0 ha | IPCC, 2014, Cap. 2, Tablas 2.6 y 2.7 (consumo de combustible de suelo orgánico y factores de emisión en **g/kg** de materia seca quemada) [VERIFICADO] |
| **Referencia de estado (no umbral): la alarma** | — | — | **1,9 Gt CO₂e/año** = **5 %** de las emisiones antropogénicas con **0,3 %** de la tierra; incendios de turba de Indonesia 2015: *"casi 16 millones de toneladas de CO₂ al día"* (IUCN, 2021) [VERIFICADO] |
| **Umbral de degradación del depósito** | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` para un valor de t C/ha por tipo de turbera | — | — |

**Justificación.** Tres hechos con fuente sostienen el diseño de esta dimensión:

1. **El estado natural del humedal turcoso es un sumidero, y el drenado lo invierte.** La turbera húmeda
   tiene **efecto neto de enfriamiento**; la drenada oxida su carbono a CO₂ y lo pierde (IUCN, 2021; IPS,
   2020) [VERIFICADO]. La comparación no es "húmedo = bueno, seco = malo" en forzamiento bruto a corto
   plazo —la turbera húmeda también emite CH₄—, y este documento **no improvisa ese balance**: cita la
   fuente, que es la que sostiene que el estado natural enfría y que la restauración es *"la única opción
   terrestre para secuestrar carbono indefinidamente"* `[REPORTADO — IUCN, 2021]`.
2. **El carbono de un humedal drenado no sólo se emite in situ: se exporta por el agua.** El IPCC
   contabiliza explícitamente las pérdidas por vía acuática —DOC, POC y DIC— además de las emisiones
   directas [VERIFICADO]. **Un SDV-E que mida sólo el suelo subestima la pérdida**, y por eso la
   exportación acuática es una fila propia y no una nota al pie.
3. **La quema de turba es una vía de pérdida con factores de emisión publicados**, no un caso anecdótico:
   el IPCC da el consumo de combustible de suelo orgánico y los factores en g/kg de materia seca quemada
   [VERIFICADO].

**Protocolo.** Inventario del depósito orgánico por **muestreo de suelo con profundidad declarada**
(número de calicatas, profundidad, densidad aparente y % de carbono orgánico, o el método nacional
declarado), **con la misma rejilla de puntos** que la Dimensión III para que las dos dimensiones sean
comparables; factores de emisión y de flujo del suplemento de humedales del IPCC para las pérdidas
(emisiones directas, DOC/POC/DIC y CH₄ de zanjas); superficie quemada de turba por teledetección y
verificación de campo donde exista. **Regla dura: no se acepta dato de carbono edáfico sin profundidad
declarada.** El balance se reporta como **stock** y como **flujo**, y nunca se compensa con la Dimensión
III ni con ningún crédito (§9). **Aviso de la revisión adversarial — el flujo no entra en la aritmética y
hay que decirlo:** la tabla de violación (b) exige **declarar** la exportación acuática (DOC/POC/DIC) y
las emisiones de zanjas cuando la unidad está drenada, pero §5.1 **no define un operador para ese flujo**
y ninguna fila del ejemplo de §5.6 lo calcula. Es decir: **la exportación acuática es hoy una obligación
de reporte, no un término del déficit**, y el propio documento lo reconoce al decir que el cálculo
«subestima» (§5.6, paso 4). Medirla entera es más exigente que la fila por sí sola, y ese hueco se
registra aquí en lugar de aparentar que está cerrado: **la fila es declarativa, el operador del flujo no
existe todavía**. Frecuencia: la del ciclo TA declarado; anual si hay presión de drenaje
activa. Quién reporta: la parte `eco-`; verificación por la comunidad testigo y, cuando exista, por el
reporte nacional de inventario de GEI.

**Violación.**
(a) **pérdida neta de stock de carbono** del depósito orgánico en el ciclo;
(b) **turbera drenada declarada en cumplimiento** sin declarar la exportación acuática de carbono
(DOC/POC/DIC) ni las emisiones de zanjas;
(c) **reportar carbono del depósito sin declarar la profundidad** del muestreo;
(d) **invocar la captura de carbono como compensación** de una violación de cualquier otra dimensión de
este documento, o **vender como secuestro** lo que el balance neto de la unidad no es;
(e) **omitir la superficie quemada de turba** del reporte en unidades con régimen de fuego activo.

---

### Dimensión V: Aves acuáticas por gremio (*el sensor integrado del hidroperiodo, y el falso positivo que hay que bloquear*)

**Qué protege.** Que el humedal siga siendo **hábitat para las aves que dependen de su régimen** —muy
especialmente las que dependen del humedal **vegetado** y **efímero**, que son las que el mundo está
perdiendo.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **Línea base de aves por gremio, declarada** (gremio del humedal vegetado; gremio de agua abierta; gremio de humedal efímero, si aplica) | **Existencia de la declaración** (piso procedural) con método, esfuerzo de muestreo y fecha | Serie comparable de al menos 5 ciclos | Consecuencia de la regla de referencia por tipo: *"los humedales solo se comparan con otros humedales del mismo tipo"* (EPA) [VERIFICADO] |
| **Tendencia del gremio del humedal vegetado** | **No regresión** respecto de la línea base declarada (piso cero: §5.1) | Poblaciones estables o en aumento | USFWS, 2024: *seaside sparrow* y *saltmarsh sparrow* —dependientes de marisma vegetada— con **> 70 %** de pérdida acumulada de población **desde 1980**; **1/3** de las aves playeras (citando *State of the Birds 2022*) [VERIFICADO] |
| **Tendencia del gremio de humedal efímero** (garzas, rascones) | **No regresión** respecto de la línea base declarada | Estable o en aumento | NABCI, *State of the Birds 2022*: **casi un tercio** de las aves acuáticas en declive, incluidas garzas y rascones **que dependen de marismas y humedales efímeros** [VERIFICADO] |
| **Abundancia total de aves acuáticas** | **PROHIBIDA como indicador de cumplimiento** (el gremio de agua abierta puede subir mientras el humedal vegetado colapsa) | — | USFWS, 2024: patos nadadores y zambullidores de **agua abierta** estables o en aumento, frente al declive de los dependientes de humedal vegetado [VERIFICADO]. §2-Regla 4 |
| **Umbral de población viable por especie** | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` | — | La fuente real existe y **no se pudo abrir**: `iucnredlist.org` bloquea a los clientes automáticos |
| **Referencia de estado (no umbral): dependencia del régimen** | — | — | El umbral Ramsar (1 % de una población; 20.000 aves) es el **único indicador cuantitativo internacionalmente acordado** de *importancia*, **no de salud** (§4, B-II) |
| **Instrumento** | — | — | Para **medir aves**: eBird / Macaulay Library (Cornell Lab of Ornithology) — observación estructurada, abundancia relativa, fenología. **Para medir el hidroperiodo con la huella del sustrato**: indicadores de suelo hidrico del **NRCS (USDA)**, *Field Indicators of Hydric Soils in the United States* (decisión de esta revisión: el informe de fuentes ya lo tenía verificado y el documento no lo usaba; es el método de campo que sostiene la fila de la condición ácuica de §4-I, hoy apoyada sólo en las fuentes de Queensland y el IPCC) [VERIFICADO]. **El instrumento de aves y el del sustrato son dos filas distintas y se citaban como una**: ésa era la ambigüedad que esta revisión corrige |

**Justificación.** Las aves acuáticas son el **bioindicador natural del eje maestro** y la evidencia
verificada lo sostiene en tres puntos, de los cuales el tercero es el que cambia el diseño del estándar:

1. **Dependen del régimen, no del espejo de agua.** *"Casi un tercio de las aves acuáticas muestran
   declives, incluidas varias especies de garzas y rascones que dependen de marismas y humedales
   efímeros"* (NABCI, 2022) [VERIFICADO]. Los rascones son el caso extremo: dependen de **humedales
   vegetados**, la categoría que más se pierde.
2. **La categoría que más se pierde es la vegetada, y hay cifra.** *"92 % de los humedales de agua dulce
   y 80 % de los salinos son vegetados"* y se perdieron **670.000 acres** de humedales vegetados entre
   2009 y 2019 (USFWS, 2024) [VERIFICADO].
3. **El contraste de validación bloquea el falso positivo.** Los gremios de **agua abierta** están
   estables o en aumento mientras los dependientes de humedal vegetado colapsan [VERIFICADO]. **Por eso
   este documento prohíbe la abundancia total como indicador de cumplimiento y exige el desglose por
   gremio**, con el gremio vegetado como **vinculante**. Un conjunto residencial que "embellece" con una
   lámina de agua permanente puede subir la abundancia total de aves y estar destruyendo el humedal
   vegetado: es la versión limnológica de *"jardín podado para la foto no es cuidado"*
   (Cap. 16.5 §16.5.14) y **está documentada con cifras, no con intuición**.

**Cómo se construye el piso sin inventar un número.** El SDV-E **no fija una población mínima viable** —no
tiene fuente y una cifra inventada aquí sería la violación más grave posible de la Regla de Oro—. En su
lugar:
1. **El piso es de no-regresión por gremio**, contra una **línea base declarada** de la propia unidad
   (método, esfuerzo y fecha). Es verificable y no exige ningún umbral que nadie haya publicado.
2. **Se añade un piso procedural:** sin línea base declarada no hay cumplimiento ni violación posibles,
   sólo opacidad (§6.4).
3. **Y se declara la debilidad, que es real:** un piso de no-regresión **tolera un estado inicial malo**
   (una unidad con el gremio vegetado ya diezmado que no empeora, cumple). Las mitigaciones son el Óptimo
   votable y la comunidad testigo; **no eliminan el problema** (§13, pregunta 5).

**Protocolo.** Censos por **punto de escucha o transecto** con esfuerzo declarado y repetido en la **misma
ventana fenológica** cada ciclo (comparar censos de estaciones distintas destruye la serie);
clasificación **obligatoria por gremio** (vegetado / agua abierta / efímero / playeros) y no sólo por
especie; plataforma de registro tipo eBird/Macaulay; **comunidad testigo** como verificador externo. Se
exige reportar, junto a la tendencia: método, esfuerzo, fechas y **cobertura del gremio** dentro de la
unidad. Frecuencia: anual en la misma ventana; la serie discontinua **no es una serie**.

**Violación.**
(a) **regresión del gremio del humedal vegetado** (o del gremio efímero, si la unidad lo tiene) respecto
de la línea base declarada;
(b) **declarar cumplimiento de fauna usando la abundancia total de aves acuáticas** o el gremio de agua
abierta — prohibido por ser el falso positivo documentado;
(c) **declarar cumplimiento sin línea base declarada** (método, esfuerzo, fecha);
(d) **imputar violación por ausencia de datos** de censo —prohibido: *"la duda sin evidencia no castiga"*
(INV2-EDU)—, aunque la ausencia activa bandera de opacidad;
(e) **usar los umbrales Ramsar (1 % / 20.000 aves) como piso de salud** de esta dimensión: son umbrales de
**designación** (§4, B-II).

---

### Dimensión VI: Calidad del agua (*por qué los criterios de agua corriente no se trasladan*)

**Qué protege.** Que el agua del humedal siga siendo habitable para su comunidad —con los parámetros
químicos que sí tienen fuente, y **con un parámetro explícitamente prohibido**—.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **pH — agua dulce** (operador `range`) | **Banda admisible 6,5 – 9,0**: **6,5** es el **límite inferior** de la banda y **9,0** el **superior**. Ninguno de los dos es un «piso» ni un «techo de plenitud»: son los dos bordes del mismo criterio, y salirse por arriba viola igual que salirse por abajo | Franja estrecha alrededor del valor natural de referencia del tipo de humedal (POLÍTICA) | EPA, 1986 [VERIFICADO] |
| **pH — agua salada / salobre** (operador `range`) | **Banda admisible 6,5 – 8,5** (mismo criterio, agua salada o salobre) | Idem sobre el valor natural de referencia | EPA, 1986 [VERIFICADO] |
| **Alcalinidad** (capacidad tampón) | **20 mg/L**, *"salvo que la alcalinidad natural sea menor —entonces rige la alcalinidad natural del agua en cuestión; si la natural es > 20 mg/L, el criterio no puede ser inferior a 25 % del nivel natural o 20 mg/L, el que sea mayor"* | Alcalinidad natural del tipo de humedal | EPA, 1986 [VERIFICADO] |
| **Sulfuro** (sulfuro de hidrógeno) | **2,0 µg/L** (CCC crónico) | 0 | EPA, 1986 [VERIFICADO] |
| **Hierro** | **1.000 µg/L** (CCC crónico) | — | EPA, 1986 [VERIFICADO] |
| **Cloruro** | **230.000 µg/L** (CCC crónico) · **860.000 µg/L** (CMC agudo) | — | EPA, 1988 [VERIFICADO] |
| **Otros contaminantes** (As, Cd, Cu, Hg, Ni, Pb, Zn, Se, amoníaco, cloro…) | Tabla completa CMC/CCC, agua dulce y salada, por contaminante | — | EPA, varios años (1980-2024) [VERIFICADO] |
| **Oxígeno disuelto (OD)** | 🔴 **PROHIBIDO como piso del SDV-E humedales — y la prohibición es doctrinal, no un hueco de dato.** Este documento **no** se apoya en que la cifra no exista: la tabla oficial de la EPA no la expone (remite al *Gold Book* de 1986 y a un documento aparte para agua salada), **pero el documento [07 de esta biblioteca](07_Formula_de_violacion_y_pesos.md) §5.3 sí publica una** —**5,5 mg/L** (agua cálida) y **6,5 mg/L** (agua fría), media de 30 días, EPA 1986— y la marca **en disputa con el documento 08 §5.2, que la da por 404** (documento 07, pregunta abierta 14). **Aunque la cifra exista y se verifique, sería el instrumento equivocado**: en un humedal la anoxia es definitoria (es la **causa** de la turba), no patológica. La exclusión se sostiene **contra una cifra disponible**, que es una posición más fuerte que sostenerla contra una ausencia | — | EPA, tabla de criterios de vida acuática (cifra no expuesta en la página); documento 07 §5.3 (cifra publicada, **en disputa** con el documento 08 §5.2); Queensland DETSI, 2023 e IPCC, 2014 (*Aquic*) para el carácter definitorio [VERIFICADO] |
| **Nitrógeno y fósforo** | `[SIN FUENTE VERIFICADA EN ESTA SESIÓN]` **y restricción doctrinal: son específicos por ecorregión y tipo de humedal; un valor global sería un error de tipo, no un dato faltante** | Criterio **narrativo** del tipo de humedal (POLÍTICA) | EPA, *Recommended Ambient Water Quality Criteria — Nutrients* (remisión verificada; cifra no verificada) [VERIFICADO parcialmente] |
| **Advertencia estructural de la fuente** | **La propia EPA advierte que los estándares para humedales *"pueden diferir de los estándares de aguas superficiales corrientes"* y que *"pueden depender menos de parámetros de química del agua y más de la diversidad de vegetación o de comunidades de macroinvertebrados"*, y que los criterios narrativos pueden ser *"más adaptativos y el enfoque preferido"*** | Criterios narrativos por tipo | EPA, *Wetland Water Quality Standards* (actualizado 2026) [VERIFICADO] |

**Justificación.** Tres argumentos, y el tercero es una prohibición.

1. **Lo que tiene fuente, entra.** pH, alcalinidad, sulfuro, hierro y cloruro tienen criterios numéricos
   publicados por la EPA para protección de la vida acuática [VERIFICADO]. Es la dimensión con el juego de
   parámetros más sólido del documento.
2. **Lo que no tiene fuente, no se inventa, y además no se traslada.** El OD **no se excluye por falta de
   cifra**: la cifra existe en el documento [07](07_Formula_de_violacion_y_pesos.md) §5.3 (5,5 / 6,5 mg/L,
   con la disputa abierta sobre su estado frente al documento 08 §5.2). Se excluye **porque en un humedal
   mediría lo contrario de lo que hay que proteger**: la anoxia es la causa de la turba, no su enfermedad
   (§3, Pilar propio 2). **Un estándar que prohíbe un parámetro que sí tiene número es más fuerte que uno
   que lo omite porque no lo encuentra**, y por eso aquí la prohibición se declara como decisión doctrinal.
   Y los nutrientes (N, P) **no admiten un valor global**
   porque los umbrales son específicos por ecorregión y tipo de humedal. Éste no es un hueco de búsqueda:
   es una **restricción de tipo**, y este documento la escribe como tal.
3. **Y la propia autoridad ambiental dice que la química del agua puede ser el instrumento equivocado para
   juzgar un humedal** [VERIFICADO, cita literal en la tabla]. Eso valida con fuente externa el precedente
   canónico del Cap. 8 §8.11 que el brief §2.2 ordena usar: hay cosas que **se registran cualitativamente
   y de forma binaria, no con la misma vara cuantitativa que el agua o la vivienda**, porque medirlas así
   las destruiría. Aquí no es una concesión poética del proyecto: lo dice la EPA.

**Protocolo.** Sonda multiparamétrica **calibrada** para pH; laboratorio con método declarado para
alcalinidad, sulfuro, hierro y cloruro; **medición en al menos tres puntos y en la misma fase hidrológica**
del ciclo (medir en creciente y en estiaje y comparar sin declararlo es un error de serie); criterios de
nutrientes **por ecorregión y tipo**, con enfoque narrativo cuando la fuente lo prefiere. **El OD se mide
sólo si la unidad es de agua libre y somera no turbosa, y se declara la exclusión de las turberas** —
medirlo en una turbera y usarlo como piso sería destruir el objeto protegido (Dimensión III). Frecuencia:
mensual en fase de diagnóstico, trimestral en seguimiento, siempre con la fase hidrológica declarada.
Quién reporta: parte `eco-` con laboratorio o sonda de referencia y verificación de la comunidad testigo.

**Violación.**
(a) **pH fuera de 6,5-9,0** en agua dulce, o **fuera de 6,5-8,5** en salobre o salada, medido con sonda
calibrada y excluida la variación natural declarada del tipo;
(b) **alcalinidad < 20 mg/L** cuando la alcalinidad natural de la masa de agua es ≥ 20 mg/L (la excepción
de la fuente —alcalinidad natural menor— **debe declararse**, no presuponerse);
(c) **sulfuro, hierro o cloruro por encima de los criterios CCC/CMC** citados;
(d) **usar el oxígeno disuelto como piso** en cualquier humedal, y muy especialmente en turbera: es la
prohibición doctrinal de §3;
(e) **reportar nutrientes con un valor global** de "los humedales" o **sin declarar la ecorregión y el
tipo**, o **medir en una sola fase hidrológica** presentándolo como estado del ciclo;
(f) **declarar cumplimiento de calidad del agua por el aspecto del agua** (transparencia, "agua limpia")
sin ninguno de los parámetros de la tabla: es la forma estética de cumplir sin medir.

---

### Dimensión VII: Biota indicadora — vegetación hidrófita y macroinvertebrados (*cuando la fuente prefiere el criterio narrativo*)

**Qué protege.** La **comunidad** que el régimen sostiene: la vegetación típicamente adaptada a suelo
saturado —que está en la definición de humedal— y la comunidad de macroinvertebrados, que la propia EPA
señala como base preferente de los estándares de humedal.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **Cobertura de vegetación hidrófita obligada** (% del área de referencia) | **No pérdida neta** respecto de la línea base declarada (piso cero) | Aumento; composición del tipo de referencia | EPA, 40 CFR 120.2(c)(1): la definición exige *"prevalencia de vegetación típicamente adaptada a condiciones de suelo saturado"* [VERIFICADO] |
| **Composición por tolerancia a la saturación** (obligadas / facultativas / upland) | **No aumento de la fracción *upland*** respecto de la línea base | Dominancia de obligadas del tipo de referencia | Queensland DETSI, 2023 (indicador: *"vegetación dominada por plantas indicadoras de humedal"*) [VERIFICADO] |
| **Índice de Integridad Biótica (IBI) de humedal** (multi-métrica) | `[SIN FUENTE VERIFICADA]` para un valor de corte; **el instrumento existe** (documento de 6 métricas de la EPA) | Multi-métrica con condición de referencia del **mismo tipo** | EPA, *Wetlands Monitoring and Assessment* — remisión verificada [VERIFICADO] |
| **Umbral cuantitativo de macroinvertebrados** | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` | Criterio **narrativo** del tipo de humedal | EPA, *Wetland Water Quality Standards*: los estándares de humedal *"pueden depender menos de parámetros de química del agua y más de la diversidad de vegetación o de comunidades de macroinvertebrados"*; los criterios narrativos *"pueden ser más adaptativos y el enfoque preferido"* [VERIFICADO] |
| **Regla de comparación** | **Obligatoria**: la unidad **sólo se compara con humedales del mismo tipo** y contra **condición mínimamente disturbada** | Referencia del mismo tipo, declarada y fechada | EPA, *Wetlands Monitoring and Assessment* [VERIFICADO] |

**Justificación.** Esta dimensión existe por tres razones verificadas y ninguna inventada. Primero, **la
vegetación hidrófita no es un adorno: está en la definición legal de humedal** —un área es humedal si
sostiene *"una prevalencia de vegetación típicamente adaptada a condiciones de suelo saturado"* (EPA, 40
CFR 120.2(c)(1)) [VERIFICADO]—, de modo que su pérdida es la señal más directa de que el régimen se está
perdiendo, y **es anterior a que el espejo de agua desaparezca**: es exactamente la categoría que más se
pierde en las series nacionales (**670.000 acres** de humedal vegetado en 2009-2019, USFWS 2024)
[VERIFICADO]. Segundo, **la propia EPA pone la comunidad biótica por delante de la química del agua** para
los estándares de humedal, y acepta el criterio **narrativo** como el enfoque preferido [VERIFICADO] —lo
que convierte a esta dimensión en el lugar donde el precedente del Cap. 8 §8.11 se aplica con respaldo
externo—. Tercero, **es la dimensión que hace auditable el falso positivo**: el gremio vegetal dice lo que
el espejo de agua oculta.

**Protocolo.** Transectos o parcelas fijas y georreferenciadas para cobertura y composición por clase de
tolerancia (obligada / facultativa / *upland*), con lista de especies del tipo de referencia; muestreo de
macroinvertebrados con método estandarizado y **misma época hidrológica**; IBI de humedal cuando exista
condición de referencia del mismo tipo. Frecuencia: anual en la misma ventana fenológica; la composición
se reporta **con la lista de especies**, porque dos coberturas iguales con composiciones distintas no son
el mismo humedal. Quién reporta: parte `eco-` con la comunidad testigo; **la ciencia mide, el guardián
consiente** (§7.2).

**Violación.**
(a) **pérdida neta de cobertura de vegetación hidrófita obligada** respecto de la línea base declarada;
(b) **aumento de la fracción *upland*** en el área de referencia (señal de desecación del sustrato);
(c) **declarar cumplimiento de biota comparando la unidad con humedales de otro tipo** o contra una
condición no declarada — prohibido por la regla de referencia por tipo de la EPA;
(d) **declarar cumplimiento con criterio narrativo sin expediente**: el criterio narrativo es legítimo
—lo prefiere la fuente— pero **exige declaración escrita, fechada y firmada** con la condición de
referencia; sin eso es una opinión, y una opinión no es un estado.

---

### Dimensión VIII: Conectividad hidrológica (*el piso procedural del canon que no tiene métrica*)

**Qué protege.** Que el humedal siga conectado a **su agua**: la cuenca que lo alimenta, el acuífero que
lo sostiene y los humedales vecinos con los que intercambia agua, nutrientes y propágulos. El canon lo
exige explícitamente: *"Conectividad con otros ecosistemas"* (Cap. 10 §10.4).

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **Declaración de dependencia hidrológica de la unidad** (cuenca de aporte, acuífero, humedales vecinos, obras que la interceptan) | **Existencia de la declaración** (piso procedural, verificable por documento), con los 7 campos de identidad de la parte `eco-` | Declaración con modelo hidrológico y serie de niveles del acuífero | Canon, Cap. 16.5 §16.5.14 (campos de identidad) · Queensland DETSI, 2023 (procesos: descarga y recarga de agua subterránea, escorrentía e infiltración) [VERIFICADO] |
| **Presiones que interrumpen la conexión** | **Cero** de la lista aplicadas sin expediente T14: canal construido (**H2-M13**), canal en el humedal (**H2-M7**), hidrología superficial controlada (**H2-M6-a/b/f**), excavación (**H2-M10/M11**) | Ausencia de intercepción antrópica | Queensland DETSI, 2023 [VERIFICADO] |
| **Métrica cuantitativa de conectividad** (índice de conectividad hidrológica del humedal con su cuenca y su acuífero) | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` | — | No se verificó ninguna métrica cuantitativa en esta sesión; corresponde al documento 21 de esta biblioteca (transversal de conectividad) |

**Justificación.** Esta dimensión es la más débil del documento y se declara antes de defenderla. **El
canon la exige y la ciencia, hoy, no publica el número.** Lo que hay es: (a) los procesos de conexión
—descarga de agua subterránea, recarga, escorrentía, infiltración, inundación— **catalogados como procesos
ecológicos** por la fuente gubernamental [VERIFICADO]; (b) las **presiones con código** que la
interrumpen, que son auditables [VERIFICADO]; y (c) los **7 campos de identidad** del canon, que obligan a
declarar el territorio y las fuentes de datos de la parte `eco-` [VERIFICADO]. Con eso se puede construir
un **piso procedural**: la unidad **debe** declarar de qué agua vive y qué obras la interceptan. Lo que no
se puede construir, sin inventar, es un índice.

**Y una consecuencia que hay que decir, porque es incómoda: un humedal puede cumplir todas las demás
dimensiones y estar condenado por su cuenca.** Si el acuífero que lo alimenta se sobreexplota aguas
arriba, la unidad pierde su régimen sin que ninguna presión se haya aplicado **dentro** de su área de
referencia. Por eso la declaración de dependencia hidrológica es **condición de validez** del expediente
(§6.3, campo 10) y no un adorno: sin ella, el estándar mediría el humedal y **no vería al culpable**.

**Protocolo.** Declaración documental de la cuenca de aporte y del acuífero (con cartografía y fuentes
públicas de datos hidrológicos), inventario de obras de intercepción en la cuenca con fecha y
autorización, y serie de niveles piezométricos **en la unidad** (los de la cuenca, si existen, como
contexto). Frecuencia: revisión de la declaración **cuando cambie cualquier obra o uso del agua en la
cuenca**, y al menos una vez por ciclo TA. Quién reporta: parte `eco-`, con la **comunidad de custodia**
como fuente de conocimiento local y la comunidad testigo como verificador.

**Violación.**
(a) **no existe declaración de dependencia hidrológica** de la unidad (violación procedural);
(b) **intercepción, canalización o extracción** en la cuenca o el acuífero del que depende la unidad, sin
expediente T14 y sin medición de su efecto sobre el nivel freático de la unidad;
(c) **declarar cumplimiento de conectividad citando un índice** que la unidad no puede medir ni la fuente
publicar — citar la existencia de métricas como si fueran umbral es fabricar la fuente;
(d) **evaluar la conectividad sólo dentro del área de referencia** y declarar la unidad sana mientras su
cuenca se seca.

---

## 5. Fórmula de violación, pesos y umbrales

Este documento no ratifica la fórmula del SDV-E: pertenece al documento
[07 de esta biblioteca](07_Formula_de_violacion_y_pesos.md). Lo que sí hace es **fijar las condiciones que
la fórmula debe cumplir en un humedal**, y una de ellas es un problema aritmético que este ecosistema
hereda de los bosques con una vuelta de tuerca propia.

### 5.1 El déficit normalizado, y el piso cero con denominador de *stock*

La versión vigente en el proyecto es la **normalizada**, coherente con el motor:
`déficit = (requerido − actual) / requerido` (brief §3.3.9; `maxocontracts/blocks/sdv_validator.py`).

**Operadores que este documento necesita** (los del catálogo del documento 07 §3.3, con el uso concreto de
cada uno en humedales):

| Operador | Dimensión donde se usa | Forma |
|---|---|---|
| `max` (menos es mejor) | **II** nivel freático (profundidad), **IV** exportación de carbono | `D = max(0, (actual − req) / req)` |
| `range` (banda admisible) | **VI** pH | `D = max(0, (lo − actual)/lo)` si `actual < lo`; `D = max(0, (actual − hi)/hi)` si `actual > hi`; `0` en otro caso |
| `min` (más es mejor) | **VI** alcalinidad y cloruro (según criterio), coberturas | `D = max(0, (req − actual) / req)` |
| `binario/procedural` | **I** régimen, **VIII** declaración, **B-I**, **B-II**, **B-III** | no produce déficit: produce **estado** |
| piso cero | **III** turba, **IV** stock de carbono, **V** gremios, **VII** cobertura hidrófita | ver abajo |

**El problema del piso cero, y su solución propia del humedal.** Cuatro pisos de este documento tienen
`requerido = 0` (no pérdida neta de turba, no pérdida neta de carbono, no regresión de gremios, no pérdida
de cobertura hidrófita). Con `requerido = 0`, la fórmula vigente **no está definida**:
`(0 − actual)/0` es una división por cero. El documento [10 de esta biblioteca](10_Ecosistemas_Bosques.md)
§5.1 propuso para los bosques una normalización de piso cero que divide por el **área de referencia**
(`déficit = pérdida_neta / área_de_referencia`). **En un humedal eso no sirve, y hay que decir por qué: lo
que se pierde no es superficie, es *stock*.** Perder 6 cm de turba en un humedal de 8 ha y perderlos en uno
de 80 ha **no es el mismo daño ecológico**, y el área no lo captura porque el objeto perdido es un volumen
orgánico acumulado durante milenios. La normalización que este documento propone `[HIPÓTESIS]` es:

```
déficit_piso_cero = pérdida_neta_del_período / línea_base_declarada_del_stock

  · Dimensión III → línea base = espesor de turba declarado (cm), mismo punto de sondeo
  · Dimensión IV  → línea base = stock de carbono declarado (t C/ha), misma profundidad
  · Dimensión V   → línea base = abundancia del gremio en la línea base declarada (individuos o índice)
  · Dimensión VII → línea base = cobertura hidrófita obligada declarada (% del área de referencia)
```

Con dos condiciones que la hacen auditable en vez de elástica: (1) **cada línea base se declara en el
expediente de identidad de la parte `eco-`** (los 7 campos del canon, Cap. 16.5 §16.5.14), con fecha y
método, y **no se modifica retroactivamente** —si se modifica, T13 registra la modificación y el cambio de
denominador queda a la vista—; y (2) **el período se declara** y es el mismo para todos los parámetros de
la unidad en ese ciclo. Sin la condición (1), **elegir una línea base baja es la forma más barata de
reducir el déficit a cero**, y en humedales esa tentación es especialmente fuerte porque la línea base la
mide quien tiene el interés. Es una invención de este documento, **no está ratificada**, y se registra como
pregunta abierta 4 de §13.

### 5.2 Base neutra: el factor vale exactamente 1,0 cuando la violación es 0

Innegociable, y es la lección que el SDV-S tuvo que corregir en su v2 (`FS_S = 1,0 + e^v` recargaba el
100 % incluso sin violación; el brief §3.3.8 lo prohíbe expresamente). Para el humedal la razón es
doctrinal, no aritmética: **el humedal que da agua y amortigua inundaciones no está siendo violado por
hacerlo** (§2, Regla 7). Candidato registrado, consistente con el análisis de la familia: `FE = e^v`, con
`FE(0) = 1,0` exacto. Y una precisión que el humedal necesita más que ningún otro ecosistema: **la
duración se acumula en TA** (Tiempo Absoluto), nunca en TVI ni TPI, y el **PIU** es su único traductor
(Cap. 5 §5.5). Un factor de violación expresado en TVI sería la colonización del tiempo del humedal por el
tiempo humano, es decir, la violación de la salvaguarda que el canon escribe dos párrafos antes de
convocar el SDV-E.

### 5.3 Pesos (propuesta no ratificada) y cobertura declarada del piso

| # | Dimensión | Peso | Naturaleza del piso | Por qué ese peso y no otro |
|---|---|---|---|---|
| **I** | Hidroperiodo | **0,20** | 🔵 procedural + binario (11 indicadores, condición ácuica) | Es el eje maestro y **define la identidad del sujeto** (§3, Pilar 1): el peso más alto es doctrinal |
| **II** | Nivel freático | **0,18** | 🟢 numérico (**30 cm**, IPCC 2014) — *traducción declarada* | Es el único número del eje maestro; sostiene el 0,20 de la Dimensión I |
| **III** | Turba y subsidencia | **0,12** | 🟡 piso cero con línea base (espesor) | Irreversibilidad física (subsidencia): T14 anclado en centímetros |
| **IV** | Carbono del depósito | **0,10** | 🟡 piso cero con línea base (stock) | Reservorio dominante de la turbera y pérdida **exportada por agua**, que el IPCC contabiliza y casi nadie mide |
| **V** | Aves acuáticas por gremio | **0,10** | 🟡 piso cero por gremio + procedural (línea base) | Es el sensor integrado del régimen; su debilidad (tolerar un estado inicial malo) se declara |
| **VI** | Calidad del agua | **0,12** | 🟢 numérico (EPA, 1986/1988) | Es la dimensión con más parámetros publicados; el OD queda **excluido por doctrina**, no por falta de dato |
| **VII** | Biota indicadora | **0,08** | 🟡 piso cero con línea base (cobertura) | La fuente prefiere el criterio **narrativo**: menos peso, más declaración |
| **VIII** | Conectividad hidrológica | **0,10** | 🔵 procedural (declaración) + `[SIN FUENTE VERIFICADA]` la métrica | El canon la exige; sin número, el peso paga la declaración, no la medición |
| | **Suma** | **1,00** | | |
| **B-I** | Ciclos naturales (inundación y sequía) | **0,00** | binaria | Lo inconmensurable no se pondera: ponderarlo lo vuelve canjeable (Cap. 8 §8.11) |
| **B-II** | Eje de designación Ramsar | **0,00** | binaria | **Designación ≠ salud**: ponderarla dejaría comprar cumplimiento con un sello |
| **B-III** | Zona Libre del humedal | **0,00** | binaria | Precedente VIII/IX del SDV-H; desarrollo en el documento [04](04_Zona_Libre_del_Reino_Natural.md) |

**Cobertura declarada del piso, en cifras y sin adornos.** De los **1,00** de peso declarado:

| Naturaleza del piso | Peso | Qué significa operativamente |
|---|---|---|
| 🟢 **Numérico con fuente verificada** | **0,30** (II 0,18 + VI 0,12) | puede producir déficit normalizado calculable hoy |
| 🟡 **No-regresión con línea base declarada** | **0,40** (III 0,12 + IV 0,10 + V 0,10 + VII 0,08) | produce déficit **sólo si existe la línea base**; sin ella, estado (d) y bandera de opacidad |
| 🔵 **Procedural / binario** | **0,30** (I 0,20 + VIII 0,10) | produce **estado**, no déficit; su violación bloquea (§8) |

**Y la lectura que importa: el 0,38 del peso —Dimensión I + Dimensión II— es el eje maestro, y de ese
0,38 sólo 0,18 tiene número.** Un humedal puede hoy ser juzgado aritméticamente sobre el **30 %** de su
peso declarado y **binariamente** sobre otro **30 %**; el **40 %** restante queda condicionado a que
alguien haya declarado y fechado una línea base. Si el proceso de ratificación concluye que **una
dimensión sin piso numérico no puede cargar peso**, las Dimensiones I y VIII pasan a **binarias sin peso**
y las seis restantes renormalizan a 1,00 (II 0,225 · III 0,150 · IV 0,125 · V 0,125 · VI 0,150 · VII 0,100,
redondeo declarado). **Las dos opciones son defendibles y este documento no las resuelve**: pertenece al
documento 07 y se registra en §13, pregunta 12.

### 5.4 La relación con el ISE, y el falso positivo que el tablero no puede ver

El ISE existe, está ponderado y tiene bandas (Biodiversidad 30 % · Calidad del agua 20 % · Calidad del aire
20 % · Salud del suelo 15 % · Poblaciones de especies clave 15 %) [VERIFICADO en
`docs/architecture/metricas_detalle_kpis_oraculos_dinamicos.md`, IN-01; **cero código**]. Medido contra las
dimensiones de este documento:

| Dimensión del SDV-E humedales | ¿Componente del ISE? |
|---|---|
| **I — Hidroperiodo** | 🔴 **ninguno** |
| **II — Nivel freático** | 🔴 **ninguno** |
| III — Turba y subsidencia | 🟡 parcial vía *Salud del suelo* (15 %), que no nombra turba ni subsidencia |
| IV — Carbono del depósito | 🔴 **ninguno** (ningún componente mide carbono) |
| V — Aves acuáticas por gremio | 🟡 parcial vía *Poblaciones de especies clave* (15 %) y *Biodiversidad* (30 %), **sin desglose por gremio** |
| VI — Calidad del agua | 🟡 parcial vía *Calidad del agua* (20 %), que no distingue tipos de humedal |
| VII — Biota indicadora | 🟡 parcial vía *Biodiversidad* (30 %), que no mide vegetación hidrófita |
| **VIII — Conectividad hidrológica** | 🔴 **ninguno** |
| B-III — Zona Libre | 🔴 **ninguno** |

**Lectura sin adornos: el ISE cubre CERO de las ocho dimensiones ponderadas de un humedal de forma
completa, cuatro de forma parcial y cuatro no las cubre en absoluto.** Y hay dos agravantes que son
específicas de este ecosistema:

1. **El eje maestro entero (0,38 del peso) tiene cobertura cero.** El ISE no mide hidroperiodo ni nivel
   freático: mide, en el mejor de los casos, **las consecuencias visibles** de perderlos.
2. **El 20 % del peso del ISE corresponde a calidad del aire, que es otra cosa.** En un humedal eso
   significa que una quinta parte del tablero mide un parámetro que pertenece al documento 23 de esta
   biblioteca. Es la versión de humedal del hallazgo del documento [09](09_Comparativa_inter_reinos.md)
   §11.3: **el tablero no puede ser el estándar.**

**El falso positivo, con cifras (§2-Regla 4).** En el mismo período en que EE. UU. perdió **670.000 acres**
de humedal vegetado y **426.000 acres** de bosque de humedal de agua dulce, ganó **488.000 acres** de
humedales no vegetados (**+7 %** de área de estanques), y los gremios de agua abierta se mantuvieron
estables o en aumento mientras los dependientes de humedal vegetado colapsaban (USFWS, 2024; NABCI, 2022)
[VERIFICADO]. **Un tablero que sume "superficie de humedal" y "aves acuáticas" sin desglosar reportará
MEJORA en una unidad que está perdiendo el humedal que importa.** Por eso este documento: (a) prohíbe la
abundancia total como indicador (Dimensión V, violación (b)); (b) prohíbe contar superficie de agua como
cumplimiento del hidroperiodo (Dimensión I, violación (e)); y (c) exige el desglose por gremio y por
vegetación hidrófita, que son las dos únicas señales que no se pueden maquillar con una lámina de agua
permanente.

### 5.5 Semántica de evaluación: cuatro estados, y el que no castiga

**Aviso de lectura, porque la tabla que sigue generaliza y los operadores no son el mismo.** «Cumple» no
significa «estar por encima de un número». La condición concreta depende del **operador** de la dimensión
(§5.1): con `max` —Dimensión II, profundidad del nivel freático— cumplir es estar **por debajo** del
requerido (`actual ≤ 30 cm`); con `min` —alcalinidad, cloruro, coberturas— es estar **por encima**
(`actual ≥ requerido`); y con `range` —el **pH** de la Dimensión VI, que es el caso que la tabla
anteriormente ocultaba— cumplir es **caer dentro de la banda** (`6,5 ≤ actual ≤ 9,0`), de modo que estar
por encima del límite superior **también viola**. La tabla escribe el caso `min`, que es el más frecuente,
y la fila (a) se lee con el operador de cada dimensión.

| Estado | Condición | Efecto en la fórmula | Efecto en INV2-E |
|---|---|---|---|
| **(a) Cumple** | El valor cae del lado admisible **según el operador de la dimensión** (véase el aviso anterior): `actual ≥ requerido` con `min` · `actual ≤ requerido` con `max` · `lo ≤ actual ≤ hi` con `range`; o régimen verificado | `v = 0` → `FE = 1,0000` exacto | Ninguno |
| **(b) Viola** | El valor cae del lado inadmisible **según el mismo operador**, con dato | `v = déficit normalizado` → `FE = e^v` | Disparador según §8 |
| **(c) No aplicable** | El parámetro no puede existir en la unidad (p. ej. Dimensión III en un humedal mineral sin horizonte orgánico) | **Se retira del numerador y del denominador**, con la retirada **declarada y fechada** | Exige expediente con carga de la prueba (T14) e impugnable por la comunidad testigo |
| **(d) Sin dato** | No hay medición, o hay medición **no admisible** por falta de metadatos (§6.3) | **No puntúa y no castiga** (*"la duda sin evidencia no castiga"*, INV2-EDU) | Activa **bandera de opacidad ecológica** (§6.4). **No** pone el índice en 0 y **no** suspende la ley |

La diferencia entre (c) y (d) evita dos fraudes simétricos: **declarar "no aplicable"** para escapar de un
piso, y **declarar "sin dato"** para escapar de una obligación de medir. Por eso (c) exige expediente y (d)
exige instrumentación. **Y en humedales hay un tercer fraude, que este documento nombra porque es el más
probable: declarar (a) cumplimiento a partir de una lectura de estación húmeda.** No es un estado: es un
error de método, y la Dimensión II lo bloquea por construcción al exigir media anual sobre varios años.

### 5.6 Ejemplo aplicado: el humedal del conjunto residencial (el caso canónico)

**La unidad.** El **humedal del conjunto residencial** del Cap. 16.5 §16.5.14: la unidad ecológica que el
canon usa como caso —*"Un conjunto con crédito regenerativo acumulado pero humedal bajo su SDV-E no está en
coherencia: INV2-E será su juez"*—. Se evalúa **un ciclo TA** declarado (año hidrológico) y el nivel
freático con la serie plurianual exigida por la Dimensión II.

**Los datos.** Todos los valores de medición son **ilustrativos** y están construidos para que la aritmética
sea verificable a mano; **los pisos, en cambio, no son ilustrativos: son los de las fuentes citadas**. El
crédito regenerativo acumulado del conjunto, en este ejemplo, es de **−12,0 unidades de R** —el valor que
la suite del repositorio ya usa para el caso de crédito negativo [VERIFICADO en
`tests/test_micromax.py`]— y **no entra en ningún paso de este cálculo**.

| # | Dimensión | Piso (fuente) | Medición | Operador | `D_i` | Peso | Aporte |
|---|---|---|---|---|---|---|---|
| **I** | Hidroperiodo | Régimen declarado + huella (11 indicadores / condición ácuica) | **2 presiones aplicadas sin expediente T14** (drenaje parcial **H2-M9** e hidrología superficial controlada **H2-M6**); régimen **no declarado** | binario | **VIOLADA** (estado, no déficit) | 0,20 | **estado** |
| **II** | Nivel freático | **< 30 cm** media anual, varios años (IPCC, 2014) | **45 cm** media anual (serie de 4 años) | `max` | `(45−30)/30 = 0,5000` | 0,18 | **0,0900** |
| **III** | Turba | Pérdida neta **0** (línea base 120 cm) | **114 cm** (mismos sondeos) | piso cero | `6/120 = 0,0500` | 0,12 | **0,0060** |
| **IV** | Carbono del depósito | Pérdida neta **0** (línea base 480 t C/ha, 1 m) | **462 t C/ha** | piso cero | `18/480 = 0,0375` | 0,10 | **0,0038** |
| **V** | Aves — gremio vegetado | No regresión (línea base 25 ind.) | **17 ind.** (el gremio de agua abierta subió de 40 a 55: **no cuenta**) | piso cero | `8/25 = 0,3200` | 0,10 | **0,0320** |
| **VI** | Calidad del agua | pH 6,5-9,0 · sulfuro ≤ 2,0 µg/L · hierro ≤ 1.000 µg/L · cloruro ≤ 230.000 µg/L (EPA) | pH **6,2**; sulfuro 1,0; hierro 300; cloruro 40.000 | `range`, `max`, `min` | `max = (6,5−6,2)/6,5 = 0,0462` | 0,12 | **0,0055** |
| **VII** | Biota indicadora | Pérdida neta **0** (línea base 60 % de cobertura hidrófita obligada) | **35 %** | piso cero | `25/60 = 0,4167` | 0,08 | **0,0333** |
| **VIII** | Conectividad | Declaración de dependencia hidrológica | **declaración existente**; métrica `[SIN FUENTE VERIFICADA]` | procedural | **0** (piso procedural cumplido; agujero declarado) | 0,10 | **0,0000** |
| | **Total** | | | | | **1,00** | **`v = 0,1706`** |

**El cálculo, paso a paso, sin pasos ocultos.**

1. **Hidroperiodo.** No produce déficit: produce **estado**. Su violación es un hecho documental —dos
   familias de presión del catálogo oficial aplicadas sin expediente T14, y régimen no declarado—, y
   **bloquea por sí sola** (§8).
2. **Nivel freático.** `(45 − 30)/30 = 0,5000`; × 0,18 = **0,0900**. Es el aporte dominante y el único
   cálculo del eje maestro.
3. **Turba.** `6/120 = 0,0500`; × 0,12 = **0,0060**. Seis centímetros que **no vuelven** (§3, Pilar 4).
4. **Carbono.** `18/480 = 0,0375`; × 0,10 = **0,00375 ≈ 0,0038**. Y el cálculo **subestima**: no incluye
   la exportación acuática (DOC/POC/DIC) que el IPCC contabiliza y que la unidad no declaró.
5. **Aves.** `8/25 = 0,3200`; × 0,10 = **0,0320**. El incremento del gremio de agua abierta **no se
   resta**: no es una compensación, es el falso positivo de §5.4.
6. **Calidad del agua.** El peor caso medido es el pH: `(6,5 − 6,2)/6,5 = 0,0462`; × 0,12 = **0,0055**.
   Sulfuro, hierro y cloruro cumplen y aportan 0 — **pero se midieron**, y ese dato sí entra al tablero.
7. **Biota indicadora.** `25/60 = 0,4167`; × 0,08 = **0,0333**. Es el déficit más alto en proporción: el
   humedal ha perdido el 42 % de su vegetación hidrófita obligada.
8. **Conectividad.** El piso procedural se cumple (la declaración existe) y **la métrica no se calcula
   porque no tiene fuente**: se declara el agujero.

```
v = 0,0900 + 0,0060 + 0,0038 + 0,0320 + 0,0055 + 0,0333 + 0,0000
  = 0,1706

FE = e^(FI × v × Δt)   con FI = 1,0 (ciclo sin agravantes) y Δt = 1 ciclo TA
   = e^0,1706 ≈ 1,1860
```

**Aviso de forma, añadido en la revisión adversarial.** La aritmética de este ejemplo es correcta, pero
**`FE = e^(FI × v × Δt)` no es la forma que §5.2 propone**: allí el candidato registrado es `FE = e^v`, y
el exponente multiplicado por un factor de irreversibilidad y por la duración en TA es una **variante**.
Con `FI = 1,0` y `Δt = 1` las dos coinciden —y por eso el ejemplo no cambia—, pero el lector no debe
llevarse la fórmula del ejemplo como la del estándar: **la forma del exponente pertenece al documento
[07](07_Formula_de_violacion_y_pesos.md) y este documento sólo fija el valor de `v` y la base neutra.**

**El veredicto, con las tres capas del resultado:**

| Capa | Resultado | Cómo se lee |
|---|---|---|
| **Veredicto del piso** | 🔴 **VIOLACIÓN DECLARADA** | Dimensión I violada (binaria) + 6 parámetros medidos bajo su piso: nivel freático, turba, carbono, aves del gremio vegetado, pH y cobertura hidrófita. `is_valid = False`; **hay bloqueo** |
| **Banda del compuesto** | **Moderada** (`0,10 < 0,1706 ≤ 0,30`) | la degradación es franca y la unidad conserva función — **todavía** |
| **Factor** | `FE ≈ 1,1860` | el costo de la actividad se recarga un **18,6 %**; no es neutro |

**Y el dato que cierra el caso canónico:** el crédito regenerativo acumulado del conjunto (**−12,0 R**) no
aparece en ninguna de las tres capas. El conjunto puede haber plantado árboles, haber limpiado el estanque
y haberlo registrado como R negativo: **el humedal sigue bajo su SDV-E, y el veredicto es el mismo.** Eso
es *"el suelo antes que el saldo"* (Cap. 16.5 §16.5.14) traducido a aritmética.

**Lo que este ejemplo enseña y hay que decir sin adornos: el compuesto de 0,1706 subestima el daño.** El
eje maestro —0,38 del peso— sólo aporta aquí **0,0900** de déficit numérico, porque la dimensión de mayor
peso (I) **no tiene número** y entra como estado. Un tablero que se leyera por la banda "Moderada"
reportaría un humedal con problemas moderados; la lectura correcta es que **el sujeto está perdiendo su
régimen, que es lo que lo define** (§3, Pilar 1). De ahí la regla de prelación de §5.8.

### 5.7 Respuesta corta: cuándo un humedal está bajo su SDV-E

Un humedal está **bajo su SDV-E** —y por tanto INV2-E es su juez— cuando se cumple **cualquiera** de estas
cinco condiciones, y la primera tiene prelación sobre las demás:

1. **El régimen hídrico cae bajo el piso, o se interviene sin expediente.** No hay régimen declarado, **o**
   no se cumple ninguno de los once indicadores de hidroperiodo ni existe registro continuo, **o** se
   aplicó cualquiera de las presiones del catálogo (drenaje, canal, excavación, hidrología superficial
   controlada) sin expediente T14. **Es el único caso del SDV-E en el que la violación puede cambiar la
   identidad del sujeto**: si el régimen se pierde de forma sostenida, el humedal **deja de ser humedal**.
2. **El nivel freático medio anual está en la clase drenada profunda (≥ 30 cm)** sobre una serie de varios
   años. Es el único piso numérico del eje maestro (IPCC, 2014 — traducción declarada).
3. **Hay pérdida neta de turba o de carbono del depósito** respecto de la línea base declarada, o
   subsidencia atribuible al drenaje. Es la única pérdida del estándar que la restauración **no devuelve**.
4. **Hay regresión del gremio de aves del humedal vegetado** (o del efímero) respecto de su línea base, o
   de la cobertura de vegetación hidrófita obligada. Y **no la compensa** el aumento de aves de agua
   abierta ni el aumento del espejo de agua.
5. **Alguno de los parámetros de calidad del agua con fuente** —pH, alcalinidad, sulfuro, hierro,
   cloruro— está fuera de su criterio, medido en la fase hidrológica declarada.

**Y no está bajo su SDV-E, aunque lo parezca:** por estar **seco en su estación seca declarada** (§2-Regla
8); por **no tener dato** de un parámetro (estado (d): bandera de opacidad, no violación); por **no ser
Ramsar** (la designación no es salud, §4 B-II); por **tener un espejo de agua permanente y "bonito"**
(§5.4); ni por tener **oxígeno disuelto bajo** (prohibido como piso, §4-VI). **Cuatro de estos cinco
falsos positivos son la forma en que un humedal se pierde con los indicadores a favor.**

### 5.8 Escala de interpretación y regla de prelación

**Capa 1 — bandas del compuesto `v`** (las del documento [07](07_Formula_de_violacion_y_pesos.md) §5.7, que
este documento no re-deriva):

| Banda | `v` compuesto | Qué dice |
|---|---|---|
| **0 · Sin violación** | `v = 0` | ningún parámetro medido bajo su piso y ninguna binaria violada |
| **1 · Leve** | `0 < v ≤ 0,10` | incumplimiento de un parámetro menor |
| **2 · Moderada** | `0,10 < v ≤ 0,30` | incumplimiento franco; la unidad conserva función |
| **3 · Severa** | `0,30 < v ≤ 0,50` | degradación que compromete la función ecosistémica |
| **4 · Crítica** | `0,50 < v ≤ 1,00` | degradación extrema; la unidad pierde integridad |
| **5 · Excedida** | `v > 1,00` | violación múltiple |

**Capa 2 — la violación del piso es un hecho, y manda sobre la banda.**

> **Regla de prelación.** Si existe **al menos un parámetro medido bajo su piso** (o fuera de su banda,
> con `range`), o una **dimensión binaria violada**, la unidad tiene **violación declarada** —con
> independencia de la banda del compuesto— y la banda se reporta **subordinada** a ese hecho.

**Las binarias de esta regla son las de este documento, y hay que nombrarlas: I, VIII, B-I, B-II y B-III**
—las ocho ponderadas están listadas en §5.3 y las tres binarias sin peso en §4—. Pero **no todas pesan
igual al disparar, y la diferencia se declara**: la violación de **I** (no hay régimen declarado, o una
presión del catálogo sin expediente T14) es el **disparador de cambio de identidad** de §3 Pilar propio 1
y bloquea por sí sola (§8.1); la de **VIII** (no hay declaración de dependencia hidrológica) y la de
**B-III** (no hay catálogo de Zona Libre, o no hay custodia sobre el recinto no medido) son **violaciones
procedurales**: no miden daño ecológico, miden **falta de expediente**, y por eso bloquean el expediente
pero **no se suman como si fueran hectáreas perdidas**; y las de **B-I** y **B-II** son de otra especie
todavía —**B-I registra el régimen de ciclos y B-II registra una designación**: lo que se viola en B-II es
*usar* la designación como prueba de salud (R17), no carecer de ella, y un humedal no Ramsar **no viola
nada** por no serlo—. Sin esta distinción, la regla de prelación convertiría cualquier expediente
incompleto en una alarma ecológica, que es exactamente el falso positivo que el documento existe para
bloquear.

Esta regla no es un adorno: es la que el ejemplo de §5.6 hace necesaria al calcularse. **El compuesto dio
0,1706 ("Moderada") en una unidad cuyo eje maestro —el 38 % del peso— está violado y cuyo sujeto puede
estar dejando de ser un humedal.** Una media ponderada reparte la culpa y **diluye exactamente el caso que
el estándar existe para atrapar**: el daño concentrado en el eje que define la identidad. Es la misma
lección que el documento 07 §5.9 extrajo de su propio ejemplo, con una diferencia propia del humedal:
**aquí lo que la media diluye no es una dimensión cualquiera: es la condición de existencia del sujeto.**

---

## 6. Protocolo de medición (sensores, frecuencias, quién reporta)

El elenco completo del SDV-E es el documento 06 de esta biblioteca (todavía no existe como archivo). Aquí
se fija lo que un humedal exige, con una advertencia inicial que ordena todo lo demás: **el humedal no se
mide desde arriba.** La arquitectura de tres niveles de la EPA funciona porque el nivel 3 (intensivo, de
sitio) **calibra** el nivel 2 (protocolos rápidos), y la teledetección sola no distingue un humedal
vegetado de un estanque. Quien pretenda certificar un humedal sólo con satélite está certificando otra
cosa.

### 6.1 Elenco por dimensión

| # | Dimensión | Instrumento | Frecuencia | Quién reporta | Estado de la fuente |
|---|---|---|---|---|---|
| **I** | Hidroperiodo | **Nivel 1** clasificación del tipo y teledetección · **Nivel 2** protocolos rápidos (11 indicadores) **validados contra el Nivel 3** · **Nivel 3** HGM y evaluación biológica · **registro de presiones con código H2-*** (T13) | Ciclo TA declarado; **al menos uno por año hidrológico** | Parte `eco-` + **comunidad testigo** (declaración del régimen) | 🟡 método con fuente (EPA 3 niveles; Queensland 11 indicadores); 🔴 **sin umbral numérico** de días/% |
| **II** | Nivel freático | Piezómetros/freatímetros en **≥ 3 puntos** (borde, centro, descarga) + calicata/barreno para turba; nivelación de precisión para subsidencia | Mensual mínimo; **media anual sobre varios años** | Parte `eco-` + verificación de la comunidad testigo | 🟢 umbral con fuente (IPCC, 2014); 🟡 **traducción declarada** |
| **III** | Turba | Barreno/calicata con **profundidad y método declarados**, **puntos fijos** repetidos; GNSS o nivelación para subsidencia | La del ciclo TA; anual con presión activa | Parte `eco-` + comunidad testigo | 🟢 irreversibilidad con fuente; 🔴 **umbral de turba: POLÍTICA, no existe mínimo universal** |
| **IV** | Carbono del depósito | Muestreo de suelo con profundidad declarada (o método nacional) + factores del suplemento de humedales del IPCC (directas, DOC/POC/DIC, CH₄ de zanjas) + superficie quemada por teledetección | La del ciclo TA; anual con drenaje activo | Parte `eco-` + reporte nacional de GEI cuando exista | 🟡 factores con fuente; 🔴 **sin umbral de t C/ha por tipo** |
| **V** | Aves por gremio | Censos por punto de escucha o transecto, **misma ventana fenológica**, clasificación por gremio; eBird / Macaulay Library | Anual, misma ventana | Parte `eco-` + **comunidad testigo** | 🟡 instrumento con fuente; 🔴 **sin umbral de población viable** |
| **VI** | Calidad del agua | Sonda multiparamétrica calibrada (pH) + laboratorio con método (alcalinidad, sulfuro, hierro, cloruro); nutrientes **por ecorregión y tipo** | Mensual en diagnóstico; trimestral en seguimiento; **fase hidrológica declarada** | Parte `eco-` + laboratorio de referencia | 🟢 criterios con fuente (EPA); 🔴 **OD sin cifra y prohibido**; 🔴 **N y P sin cifra** |
| **VII** | Biota indicadora | Parcelas o transectos fijos georreferenciados; composición por tolerancia (obligada/facultativa/*upland*); macroinvertebrados con método estandarizado; IBI de humedal si hay referencia del mismo tipo | Anual, misma ventana | Parte `eco-` + comunidad testigo | 🟡 instrumento con fuente (EPA, IBI); 🔴 **valores de corte: `[SIN FUENTE VERIFICADA]`** |
| **VIII** | Conectividad | Declaración documental de cuenca, acuífero y obras de intercepción; piezometría de la unidad como contexto | Revisión al cambiar cualquier obra o uso del agua; ≥ 1 por ciclo TA | Parte `eco-` + **comunidad de custodia** | 🔵 piso procedural con fuente (canon + Queensland); 🔴 **sin métrica** |
| **B-I** | Ciclos (inundación / sequía) | Registro del régimen declarado y de la estacionalidad permitida; la sequía estacional **declarada** no dispara | Cuando se modifica el régimen | Parte `eco-` con consentimiento del guardián | 🟢 doctrina con fuente (EPA 2026 [REPORTADO]; Cap. 10 §10.4) |
| **B-II** | Designación Ramsar | Consulta en el **RSIS** (buscador oficial) y criterios de la Convención; el umbral del 1 % se consulta por población en **WPE** (Wetlands International) | Cuando cambia la designación o se reporta cambio de carácter ecológico | Parte `eco-` + Secretaría de la Convención | 🟡 criterios `[REPORTADO]` (dominio bloqueado a bots); 🟢 RSIS y WPE verificados |
| **B-III** | Zona Libre | **Registro cualitativo documental**, no instrumento de medida | Cuando se modifica el catálogo | Parte `eco-`, con consentimiento del guardián | 🟢 doctrina explícita (Cap. 7 §7.9 · Cap. 16.5 §16.5.14; documento [04](04_Zona_Libre_del_Reino_Natural.md)) |

### 6.2 La arquitectura de tres niveles, y por qué encaja sin adaptación

La EPA tiene una arquitectura madura y **este documento no la reinventa**: **Nivel 1** "evaluación de
paisaje" —inventario a escala de paisaje, teledetección, preferentemente en SIG, con clasificación—;
**Nivel 2** "protocolos rápidos" a escala de sitio, **validados y calibrados contra el Nivel 3**; **Nivel
3** "evaluación intensiva de sitio" —índices multi-métrica derivados de investigación, enfoque
hidrogeomórfico HGM, evaluaciones biológicas— [VERIFICADO]. Tres reglas de la fuente que este documento
adopta **como reglas duras**:

1. **Referencia por tipo:** las evaluaciones comparan cada humedal contra un conjunto de **humedales de
   referencia**, y *"los humedales solo se comparan con otros humedales del mismo tipo"*, contra
   **condición mínimamente disturbada** [VERIFICADO]. Es el fundamento técnico de que el tipo de humedal
   sea metadato obligatorio (§6.3).
2. **Calibración:** un protocolo rápido (Nivel 2) que no está calibrado contra el Nivel 3 **no es una
   medición**: es una impresión.
3. **Diseño estadístico:** el inventario nacional de referencia usa **5.048 parcelas de 4 millas cuadradas
   distribuidas aleatoriamente** con control de calidad en varios pasos y verificación de campo, y reporta
   al Congreso **cada diez años** (mandato de la *Emergency Wetlands Resources Act*, Public Law 99-645),
   con **6 reportes nacionales y 8 regionales** que cubren **1954-2019** [VERIFICADO]. Consecuencia para el
   SDV-E: **el ciclo decenal es el techo de fineza de la serie nacional; no se puede exigir a la unidad más
   fineza que la de su base de reporte** (§6.5, regla 1).

### 6.3 Metadatos obligatorios (aportación de este documento)

Ningún parámetro de este documento es auditable sin los siguientes campos, y **ninguno existe hoy en el
repositorio** (§12). Se incorporan como campos obligatorios del expediente de la parte `eco-` y como
**condición de validez del contrato**:

1. **Área de referencia declarada** de la unidad, con fecha, e **inmutable retroactivamente**.
2. **Unidad del ciclo TA declarada** —año hidrológico, año calendario, estación de crecimiento o ciclo de
   sucesión—, **sin valor por defecto**. Elegirla por comodidad de implementación es colonizar el tiempo
   del humedal.
3. **Tipo de humedal declarado** (porque *"los humedales solo se comparan con otros humedales del mismo
   tipo"*).
4. **Serie de nivel freático**: número de años, fecha de inicio, método y número de puntos. Sin esto, la
   Dimensión II **no es admisible**.
5. **Profundidad y método del sondeo de turba**, y el **umbral de turba de la unidad** si se declara uno
   (POLÍTICA votable, §4-III).
6. **Profundidad del muestreo de carbono** del depósito orgánico.
7. **Línea base de aves por gremio** (método, esfuerzo, fecha) o su ausencia explícita.
8. **Régimen hídrico declarado** (frecuencia, duración, profundidad, estacionalidad) con la fuente o la
   determinación local documentada.
9. **Catálogo de presiones aplicadas** con su código (**H2-**\*) y el **expediente T14** de cada una (menor
   irreversibilidad elegida y costo de oportunidad asumido).
10. **Declaración de dependencia hidrológica**: cuenca de aporte, acuífero y obras de intercepción
    conocidas.

### 6.4 El dato que falta: bandera de opacidad, no sanción

El principio `INV2-EDU` *"la duda sin evidencia no castiga"* existe para proteger al presunto vulnerado
cuando no hay medición. **En el SDV-E el presunto vulnerable no puede reportar nada** —*"Nosotros
registramos la interacción, no la vida interna del ecosistema"* (Cap. 16.5 §16.5.14)—, de modo que aplicar
la regla sin más **protege al presunto violador**. La propuesta, formulada por el documento
[09 de esta biblioteca](09_Comparativa_inter_reinos.md) y que este documento adopta para humedales:

- **La ausencia de monitoreo NUNCA se imputa como violación del humedal.** Jamás un `ISE = 0` por falta de
  dato, jamás un déficit imputado por silencio, y **jamás una violación disparada por una lectura
  instantánea de estación seca** (§2-Regla 8). En un humedal esto no es una cortesía: es la diferencia
  entre un estándar y un generador de falsos positivos.
- **Y activa una bandera de opacidad ecológica** que opera como **obligación contractual de instrumentar**
  y como **condición de validez del contrato**, no como sanción al territorio.
- **Y la ley no se negocia por ausencia de dato:** *"mientras no haya resolución, el canon manda"* (brief
  §3.3.10). La bandera obliga a medir; no autoriza a drenar.

### 6.5 Cinco reglas duras del protocolo

1. **El ciclo no puede exigir más fineza que la base de reporte.** El inventario nacional de referencia
   reporta **cada diez años** [VERIFICADO]. Un piso que exija medición mensual del nivel freático en toda
   unidad sin financiarla es un piso que se violará por diseño; por eso el protocolo distingue **Nivel 1-2
   (declaración y verificación)** de **Nivel 3 (intensivo)**, y sólo exige el Nivel 3 donde hay presión
   activa.
2. **El espejo de agua no es un indicador de salud.** Prohibido usarlo como cumplimiento del hidroperiodo
   (Dimensión I, violación (e)) y prohibido usar la abundancia total de aves como cumplimiento de fauna
   (Dimensión V, violación (b)). Con cifras: **+7 %** de área de estanques convive con **670.000 acres**
   de humedal vegetado perdidos [VERIFICADO].
3. **El oxígeno disuelto no es un piso.** Se mide sólo en humedales de **agua libre y somera no turbosos**
   y se declara la exclusión de las turberas: en ellas la anoxia es definitoria (§4-VI).
4. **N y P no tienen valor global.** Son específicos por **ecorregión y tipo de humedal**; la propia EPA
   acepta y prefiere el **criterio narrativo** para humedales [VERIFICADO]. Un valor único de "los
   humedales" sería un error de tipo.
5. **T13: la contabilidad nunca se borra.** Toda corrección de serie, todo cambio de línea base y todo
   sondeo se registra con fecha. En un humedal esto tiene un peso especial: **la turba perdida no vuelve,
   así que el registro es lo único que queda de ella** (§7.1).

---

## 7. Verificación y auditoría (T13, guardián, comunidad testigo)

### 7.1 T13 — Transparencia de Cálculo

*La contabilidad nunca se borra.* Para un humedal esto tiene una consecuencia específica: **la
subsidencia y la oxidación de la turba hacen que la pérdida sea físicamente irreversible**
(International Peatland Society, 2020) [VERIFICADO], y *"pueden pasar décadas, siglos o más antes de que
los humedales restaurados funcionen como humedales naturales, si es que alguna vez lo hacen"* (USFWS,
2024) [VERIFICADO]. En los reinos humano y sintético la violación se repara y el registro se cierra; aquí
**el registro es lo que queda del humedal que hubo**. De ahí que la Capa de Ternura no tenga análogo en
este documento (§8.4) y que cada centímetro de turba perdido deba llevar fecha, punto de sondeo y método.

### 7.2 El guardián oráculo consiente; no mide

El canon lo fija: *"Ecosistemas (`eco-*`): consentimiento otorgado por el guardián oráculo"*
(`app/contracts_bp.py`) [VERIFICADO]. **Este documento añade una separación que el canon no explicita y que
el código hoy no respeta: el guardián consiente, la ciencia mide, la comunidad testigo verifica.** Un
guardián que además midiera sería juez y perito de la misma causa, y el repositorio ya documenta que su
heurística es laxa (§7.4, R13). En un humedal la separación tiene un caso concreto y caro: **el guardián no
puede certificar el régimen hídrico**. Una firma no es un hidroperiodo.

### 7.3 La comunidad testigo

El documento [09 de esta biblioteca](09_Comparativa_inter_reinos.md) mostró que el Reino Natural es el
**único reino sin par auditor**: ningún humedal audita a otro humedal, y el auditor viene necesariamente
del reino que se beneficia de su uso. La **comunidad de custodia** y los **7 campos de identidad** —entidad
representada, territorio, fuentes de datos, límites del mandato, comunidad de custodia, parámetros SDV-E y
procedimiento de disputa— (Cap. 16.5 §16.5.14) **son el sustituto institucional de ese par que no existe**,
no un trámite. Para humedales, este documento le asigna **cuatro tareas concretas y verificables**:

1. **Verificar la declaración del régimen hídrico** (frecuencia, duración, estacionalidad) — que ningún
   dato público puede verificar por ella y que es el piso de mayor peso del documento.
2. **Verificar el catálogo de presiones aplicadas** y que cada una tenga expediente T14; es la tarea que
   hace auditable la violación más probable (el drenaje silencioso).
3. **Impugnar el falso positivo estético**: el espejo de agua permanente, el estanque "mejorado", el
   aumento de aves de agua abierta presentado como mejora.
4. **Impugnar las declaraciones de "no aplicable"** (estado (c)), que son la salida más barata del
   estándar: un humedal mineral sin turba puede declararse (c) en la Dimensión III legítimamente, pero
   declarar (c) en la Dimensión II o VI es declarar que el humedal no tiene agua ni calidad de agua.

### 7.4 Riesgos abiertos, con tres nuevos específicos de humedales

Riesgos ya documentados en `docs/architecture/blindaje_anti_gamificacion_equidad.md`:

| ID | Riesgo | Efecto sobre el SDV-E humedales |
|---|---|---|
| **R4** | **Partes fantasma**: cualquier usuario autenticado crea un `eco-*` y queda como su dueño, sin verificar autoridad sobre la entidad | Se puede fabricar el humedal que se va a medir y bajar su línea base a voluntad (§5.1) |
| **R6** | T9 (Reciprocidad Justa) **no se valida** en la creación: un contrato 100 % unilateral pasa y se activa | Se puede drenar sin contraprestación y sin bloqueo |
| **R13** | **Guardián eco con heurística laxa**: sin `DEEPSEEK_API_KEY` **aprueba si los invariantes pasan** | El consentimiento del humedal se vuelve automático — y con R6, un contrato unilateral lo activa |

**Tres riesgos nuevos, documentados aquí por primera vez con fuente:**

| ID | Riesgo | Evidencia |
|---|---|---|
| **R16** | **La estética del agua como cumplimiento.** Superficie de agua "mejorada" y aves de agua abierta en aumento se presentan como mejora, mientras el humedal vegetado —el que sostiene la biodiversidad dependiente del régimen— se pierde. Es el falso positivo de la Regla 4 convertido en estrategia de reporte | USFWS, 2024: **+488.000 acres (+7 %)** de humedales no vegetados frente a **−670.000 acres** de humedales vegetados (2009-2019), con **1/3** de las aves playeras y **> 70 %** de pérdida acumulada desde 1980 en dos pasadores de marisma; gremios de agua abierta estables o en aumento [VERIFICADO] |
| **R17** | **La designación como sustituto de la salud.** Se invoca la condición de sitio Ramsar (o el criterio del 1 % / 20.000 aves) como prueba de que el humedal está por encima de su SDV-E. La designación mide **importancia internacional**, no integridad | Ramsar, GWO 2025: **1 de cada 4** humedales restantes está en **mal estado ecológico** mientras la red Ramsar alcanza **172 Partes Contratantes** y **> 2.530 sitios** [VERIFICADO]; el marco oficial describe el **carácter ecológico** de los sitios Ramsar y su **cambio**, lo que presupone que un sitio designado puede cambiar (Queensland DETSI — marco Ramsar; URL verificada, **contenido no leído**: la lectura falló con `fetch failed`) [VERIFICADO parcialmente] |
| **R18** | **El drenaje como "mejora" y la definición de turba a la medida.** La definición de turbera *"varía entre países y a menudo excluye áreas de valor para la industria"*; el IPCC delega la definición en las circunstancias nacionales. Quien fija el umbral puede quedar fuera del umbral | IPCC, 2014 (glosario, *Organic soil* y *Peat*): *"los países pueden definir turba según sus circunstancias nacionales"*, con un único criterio mencionado de **10 cm** [VERIFICADO]; IUCN, 2021: las definiciones *"deberían priorizar la conservación, la restauración y el manejo sostenible"* [VERIFICADO]; revisión del **mismo período**: **221.000 acres** perdidos con un aumento **> 50 %** respecto del estudio anterior, marisma salina **−2 %** y bosque de humedal de agua dulce **−426.000 acres** (USFWS, 2024) [VERIFICADO]; conductores del cambio: desarrollo urbano y rural **> 53 %** y agricultura **26 %** [VERIFICADO] |

**La consecuencia institucional de R16 y R17 es la más incómoda de este documento:** las dos señales que
más fácilmente se reportan como mejora —más agua y más aves— **no miden el piso**, y una de ellas (el área
de estanques) creció en el mismo período en que se perdió el humedal que importa. Este documento no puede
resolver el problema; sí puede **negarse a esconderlo**, y por eso prohíbe expresamente los dos indicadores
(Dimensiones I y V) y exige el desglose por gremio y por vegetación hidrófita.

### 7.5 Lo que el canon afirma y el código no hace

El libro afirma que el consentimiento del `eco-` es *"consentimiento agregado por quórum delegado N-de-M"*
(Cap. 16.5 §16.5.14). **El quórum no está cableado**: el camino ecosistema retorna antes de la lógica de
quórum, y el canon **no publica N ni M** para el Reino Natural (solo da 60 % de miembros o 2 de 3
delegados para cooperativas; el documento [05](05_Representacion_guardian_y_mandato.md) §5.2 hace la
propuesta). Es una **incoherencia teoría↔código declarada**, no una sospecha, y este documento no la
hereda como si estuviera resuelta. Añádase, para humedales, una consecuencia material: **sin quórum
cableado, el humedal del conjunto residencial del caso canónico consiente por la firma de un guardián cuya
heurística es laxa (R13), y el conjunto es quien creó la parte `eco-` (R4)**. La personería natural tiene
forma pero no tiene autoridad.

---

## 8. Invariante INV2-E: de estándar a contrato ejecutable

El invariante genérico **INV2** dice: *"Ninguna acción del contrato puede dejar a un participante bajo su
SDV"* (Cap. 17). **INV2-E no existe**: no hay `validate_invariant_sdv_e` en
`maxocontracts/core/axioms.py` ni bloque validador gemelo de `maxocontracts/blocks/sdv_s_validator.py`
[VERIFICADO, §12]. Lo que sigue es **especificación**, no implementación.

### 8.1 Especificación propuesta

```
INV2-E (humedales) — propuesta no ratificada
────────────────────────────────────────────────────────────────────────────
PRECONDICIÓN DE VALIDEZ DEL CONTRATO
  El expediente de la parte eco- contiene los 10 metadatos obligatorios (§6.3).
  Si falta cualquiera  →  contrato INVÁLIDO (no "violado": inválido).
  Fundamento: sin ciclo TA declarado, tipo de humedal, serie plurianual del
  nivel freático, profundidad de turba y línea base de gremios, ningún
  parámetro del humedal es auditable; validar sería certificar a ciegas.

DISPARADOR INMEDIATO  (lo irreversible: dimensiones I, III y IV)
  Cualquier evento de:
    · aplicación de una presión del catálogo H2-* sin expediente T14
      (drenaje parcial, canal, excavación, hidrología superficial controlada)
    · pérdida neta de espesor de turba > 0, o subsidencia atribuible al drenaje
    · pérdida neta de stock de carbono del depósito orgánico
    · quema de suelo orgánico no declarada
    · ausencia de régimen hídrico declarado o pérdida de todos los indicadores
  →  estado = BLOQUEADO en el mismo ciclo. Sin acumulación, sin segundo aviso.
  Fundamento: T14 — ante incertidumbre sobre quien no puede consentir, elegir
  la opción de menor irreversibilidad, y la carga de la prueba es de quien
  propone. La turba perdida "se pierde permanentemente del sistema" (IPS, 2020)
  y la subsidencia no se recupera rehumedeciendo.

DISPARADOR CONTINUO  (lo reversible: dimensiones II, V, VI, VII)
  Un ciclo por debajo del piso  → v = déficit normalizado → FE = e^v (FE(0)=1,0)
  Dos ciclos consecutivos       → estado = BLOQUEADO
  El "∞" no se guarda como número: se implementa como ESTADO (lección del
  SDV-A y del SDV-S: el infinito es una consecuencia jurídica, no una cifra).
  ATENCIÓN AL CICLO DE LA DIMENSIÓN II: el piso del nivel freático es una
  media anual sobre VARIOS AÑOS (IPCC, 2014). Un ciclo estacional NO PUEDE
  disparar esta dimensión. Implementarlo con la media de una campaña sería
  construir el falso positivo que §2-Regla 8 prohíbe.

CAMBIO DE IDENTIDAD  (caso propio del humedal, §3 Pilar 1)
  Si el régimen hídrico se pierde de forma sostenida, la unidad puede DEJAR DE
  SER un humedal (transformación de identidad, doc. 02 §C4).
    · No se cierra en silencio: se declara el cambio con registro genealógico.
    · La unidad sucesora es una unidad NUEVA, con su propia área de referencia.
    · PROHIBIDO declarar el cambio de identidad para extinguir el SDV-E y
      evadir el bloqueo: es la violación (b) del criterio C4 del documento 02.
    · La carga de la prueba de que el cambio fue NATURAL (terrestrialización
      hidroserial, miles de años — IPS, 2020) y no antrópico recae en quien
      propone la actividad (T14).

ESTADO (c) NO APLICABLE
  Exige expediente fechado con carga de la prueba (T14) e impugnable por la
  comunidad testigo. Sin expediente → se trata como (b) VIOLA, no como (c).

ESTADO (d) SIN DATO
  No puntúa, no castiga, no pone el índice en 0 (INV2-EDU).
  Activa BANDERA DE OPACIDAD ECOLÓGICA = obligación de instrumentar,
  condición de validez del contrato. NO es sanción al territorio.

ACCIÓN EJECUTABLE ÚNICA
  Un humedal no se retracta y una turba no se rehabilita por contrato.
  La única acción ejecutable de INV2-E es DETENER O MODIFICAR LA ACTIVIDAD
  HUMANA QUE VIOLA EL PISO — el cierre de la zanja, la retirada del drenaje,
  la restitución del aporte hídrico. El paralelo canónico exacto es el Veto por
  Crimen de Coherencia del SDV-S: "la interrupción total del sistema que la
  provoca".

NO COMPENSACIÓN
  El crédito regenerativo acumulado (r_units negativo) NO levanta el estado
  BLOQUEADO. El suelo antes que el saldo (Cap. 16.5 §16.5.14).
  La Zona Libre (B-III) no entra en ningún numerador.
  La "creación de humedal artificial" NO es compensación: figura en el catálogo
  oficial de MODIFICACIONES HIDROLÓGICAS (Queensland DETSI, 2023, códigos
  H3-C1/C2-a/b/C4/C5-a/b) y por tanto es una alteración que se declara y se
  autoriza, no un crédito que se abona. [HIPÓTESIS de interpretación]
────────────────────────────────────────────────────────────────────────────
```

### 8.2 El precedente exacto del disparador

El SDV-S resolvió el mismo problema con un contador y un umbral: **7 ciclos consecutivos de violación →
retractación automática**, integrado en `AxiomValidator.validate_all()` y con 41 tests [VERIFICADO]. El
SDV-E humedales **no puede copiar el número 7**: los ciclos del SDV-S son horas TPI de un proceso que el
sistema gobierna, y los ciclos de un humedal son **años TA que el sistema no gobierna**. De ahí dos
disparadores distintos —uno inmediato para lo irreversible y uno acumulativo para lo reversible—, que es
una aportación de este documento y no una variante del anterior. **Y un tercer mecanismo que ningún otro
documento de la serie necesita: el cambio de identidad** (§8.1), porque en el humedal la violación
sostenida del piso no deja un humedal dañado: deja **otro ecosistema**.

### 8.3 Ningún dato del expediente existe hoy

De los **10 metadatos obligatorios** de §6.3, **ninguno** tiene tabla, columna ni validación en el
repositorio (§12). La consecuencia es directa y hay que decirla: **con el código de hoy, la precondición de
validez de INV2-E sería imposible de satisfacer, y por tanto todo contrato contra un humedal sería
inválido.** Eso es, literalmente, lo que significa *"estándar primero, contabilidad después"*: hoy no hay
juez.

### 8.4 Retractación, Capa de Ternura y la asimetría del humedal

En INV2 e INV2-S la consecuencia recae sobre la relación del sujeto protegido: rehabilitación,
retractación, cápsula de memoria, perdón protocolizado. **Nada de eso tiene análogo en un humedal**, y no
por una carencia de diseño: **la turba oxidada no se des-oxida y el suelo subsidiado no se des-subsidia**.
Un humedal restaurado *"puede tardar décadas, siglos o más en funcionar como un humedal natural, si es que
alguna vez lo hace"* (USFWS, 2024) [VERIFICADO]. El SDV-E es el primer estándar de la familia en el que
**la prevención es el remedio completo**, y el humedal lo lleva al extremo: aquí la prevención tiene
**unidad de medida** (cm de turba, cm de subsidencia) y por eso es más fácil de auditar que en cualquier
otro reino.

---

## 9. El suelo antes que el saldo (no compensación)

**La doctrina, literal:** *"Un conjunto con crédito regenerativo acumulado pero humedal bajo su SDV-E no
está en coherencia: INV2-E será su juez"* (Cap. 16.5 §16.5.14). Para humedales, la evidencia dura de que
**la promesa no es el hecho** está publicada y es contundente:

| Hecho | Cifra | Fuente |
|---|---|---|
| Reversibilidad de la restauración | *"Los impactos de la pérdida, ganancia y cambio de los humedales sobre las funciones y servicios que proveen son acumulativos en el espacio y el tiempo y pueden ser difíciles de revertir"*; *"pueden pasar décadas, siglos o más antes de que los humedales restaurados funcionen como humedales naturales, si es que alguna vez lo hacen"* | USFWS, 2024 [VERIFICADO] |
| Irreversibilidad física del carbono de la turba | *"Cuando las turberas se drenan, el carbono de la materia orgánica contenida en la turba se seca y se oxida gradualmente a CO₂, y **se pierde permanentemente del sistema**"*; con el tiempo produce **compactación y subsidencia** | International Peatland Society, 2020 [VERIFICADO] |
| Turberas drenadas como fuente global | **1,9 Gt CO₂e/año** = **5 %** de las emisiones antropogénicas de GEI con **0,3 %** de la superficie terrestre; *"en algunas regiones, hasta 80 % de las turberas han sido dañadas"* | IUCN, 2021 [VERIFICADO] |
| Turberas naturales como sumidero | **0,37 Gt CO₂/año** secuestrado por turberas casi naturales; > **600 Gt C** almacenados en suelos de turba | IUCN, 2021 [VERIFICADO] |
| Tendencia global en curso | **0,52 %/año** de pérdida; **22 %** perdido desde 1970; **1 de cada 4** humedales restantes en mal estado; hasta **20 %** más para 2050 con **39 billones USD** en riesgo | Ramsar, GWO 2025 [VERIFICADO] |
| Escala del interés económico en juego | Humedales = **~6 %** de la superficie terrestre y **> 7,5 %** del PIB global | Ramsar, GWO 2025 [VERIFICADO] |

**La forma aritmética de la no-compensación, en tres escalas:**

1. **Dentro del mismo año y del mismo país:** superficie de estanques **+488.000 acres (+7 %)** frente a
   humedal vegetado **−670.000 acres** y bosque de humedal de agua dulce **−426.000 acres** (2009-2019)
   [VERIFICADO]. El indicador de superficie de agua **compensa** la pérdida del humedal vegetado, y por eso
   el SDV-E **no puede usar sólo el área de agua** (Dimensiones I y V).
2. **Dentro del mismo documento:** el ejemplo de §5.6 — la dimensión de mayor peso (I) no tiene número y el
   compuesto apenas recarga un **18,6 %** mientras el eje maestro está violado y el sujeto puede estar
   dejando de ser un humedal. **El agregado no puede levantar el piso.**
3. **En el código de hoy:** `r_units` negativo está **implementado y probado**
   (`app/micromax.py`, `tests/test_micromax.py::test_credito_regenerativo_r_negativo`, con `-12.0`
   [VERIFICADO]) **pero no pesa en ninguna cuenta**: no existe `SUM(r_units)`; el componente R del sistema
   general sólo cuenta extracción; el precio cierra en `float(max(0.0, round(price, 4)))`
   (`app/maxo.py`) [VERIFICADO], de modo que **nunca es negativo**; y `r_units` **no tiene ninguna
   validación** —acepta cualquier negativo (`-1e9`), no exige nota, evidencia, tercero ni techo, y `NaN` e
   `inf` pasan el filtro [VERIFICADO, §12].

**La aportación específica de este documento a la no-compensación.** Hay una tentación propia de los
humedales que las otras ramas no tienen: **"crear" un humedal en otro sitio y presentarlo como
compensación del drenado.** La fuente la desarma sin necesidad de doctrina: **la creación de humedal
artificial figura en el catálogo oficial de modelos conceptuales de MODIFICACIÓN HIDROLÓGICA** —familia
**H3**, códigos *H3-C1 / C2-a / C2-b / C4 / C5-a / C5-b*— (Queensland DETSI, 2023) [VERIFICADO]. Es
decir: **crear un humedal es, en la taxonomía oficial, una alteración del régimen hídrico que se declara
como las demás**, no un acto exento que se abona contra un daño. `[HIPÓTESIS de interpretación: la fuente
cataloga el hecho; la conclusión de que por ello no puede operar como crédito compensatorio es de este
documento.]` Y hay una segunda razón, empírica: un humedal creado **no es el humedal perdido** —no tiene su
turba, ni su banco de semillas, ni su serie de aves, ni su régimen—, y *"pueden pasar décadas, siglos o
más"* antes de que se parezca a uno natural, *"si es que alguna vez lo hace"*.

---

## 10. Zona Libre: lo que NO se mide

### 10.1 La doctrina, literal

> *"Parte del valor del humedal es inefable (Cap. 7 §7.9). Los sensores miden salud (agua, cobertura,
> biodiversidad indicadora); jamás 'milagros'. **Medir todo sería la forma técnica de dejar de
> escucharlo.**"* — Cap. 16.5 §16.5.14

El canon nombra **el humedal** en la formulación misma de la Zona Libre del Reino Natural. Este documento no
la desarrolla: la **aplica**, y remite al documento [04 de esta biblioteca](04_Zona_Libre_del_Reino_Natural.md)
para la mecánica completa —los cuatro estados (Zona Libre · Zona Ciega · Zona Medida · Zona Huérfana), las
siete puertas, el recinto y no el porcentaje, los tres regímenes de información, la presunción de
integridad y sus señales de caída, y el inventario negativo—.

### 10.2 Dimensión B-III — Zona Libre del humedal (binaria, sin peso)

**Qué protege.** El derecho de un humedal a tener una parte de su valor que no se mide, no se pondera y no
se canjea.

| Parámetro binario | Condición de cumplimiento | Fuente |
|---|---|---|
| Catálogo de Zona Libre declarado y publicado para la unidad | **Presencia** | Cap. 7 §7.9 · Cap. 16.5 §16.5.14 |
| El catálogo fue establecido **con el consentimiento de la parte `eco-`** (guardián oráculo) | **Presencia** | Cap. 16.5 §16.5.14; `app/contracts_bp.py` |
| Existe **custodia** con autoridad de gobernanza y decisión vinculante sobre el recinto no medido | **Presencia** (sin custodia: **Zona Ciega**, violación) | Documento [04](04_Zona_Libre_del_Reino_Natural.md) §4.2-4.3, sobre el criterio de la IUCN WCPA (OECM, 2019) |
| **Ningún valor del catálogo entra en el numerador de ninguna fórmula** | **Presencia de la prohibición** (ausencia de infracción) | Precedente: Cap. 8 §8.11 (dimensiones VIII y IX del SDV-H) |
| Carga de la prueba al **ampliar** el catálogo | **Presencia de expediente** (categoría `critical`: quórum 60 %, consenso 75 %, T13, anti-flip-flop 14 días, `CHECK` en BD) | Precedente INV2-EDU (Parlamento Educativo) |
| **Peso en la fórmula** | **0,00 — no entra** | Este documento |

**Justificación.** Para un humedal la Zona Libre no es un adorno doctrinal: es la respuesta a una presión
concreta que este documento ya documentó. **El instrumento existente premia medir, y medir tiene un
límite.** El ISE pondera cinco componentes y nada más; una unidad de humedal puede acabar gestionada para
las cinco variables del tablero y para ninguna de las que la comunidad de custodia conoce sin instrumento:
los ritmos locales, los umbrales de perturbación que sólo se aprenden viviendo allí, los sitios de valor
cultural y las especies que nadie ha catalogado. Sin Zona Libre, el estándar sólo reconocería lo que un
sensor registra, que es exactamente el sesgo que el canon llama *"extracción estética"*: *"se registra lo
que regenera, no lo que adorna"* (Cap. 16.5 §16.5.14).

**Protocolo.** Registro **cualitativo y documental**: acta del catálogo, fecha, consentimiento de la parte
`eco-`, delimitación del recinto, y el expediente de carga de la prueba por cada elemento. **No hay
instrumento de medida y ése es el punto.** Frecuencia: sólo cuando el catálogo se modifica. Firma: guardián
oráculo + comunidad testigo.

**Violación (binaria, presencia/ausencia).**
(a) **No existe catálogo declarado** para la unidad;
(b) el catálogo se **modificó sin el consentimiento** de la parte `eco-`;
(c) **cualquier valor del catálogo aparece en el numerador de cualquier fórmula**, incluido el compuesto de
§5.6;
(d) **no hay custodia** sobre el recinto no medido (Zona Ciega), o la hay pero **sin decisión vinculante**
(Zona Huérfana);
(e) **se declaró "inefable" un parámetro que sí es medible y que está en este documento** —el régimen
hídrico, el nivel freático, el espesor de turba, el pH, la cobertura hidrófita— **para eludir su piso sin
expediente de carga de la prueba**. **Éste es el fraude específico de esta dimensión en un humedal**, y
tiene una forma previsible: declarar que "el humedal es un ser vivo y no se le puede poner números" para
**no medir el drenaje**. Es la operación inversa del falso positivo estético (R16) y hace el mismo daño.

### 10.3 Frontera LEY / POLÍTICA (explícita, porque es donde se puede vaciar el estándar)

- **LEY (no se vota).** Que exista una Zona Libre en el Reino Natural **y que no se pondere**. El canon la
  nombra (Cap. 7 §7.9 · Cap. 16.5 §16.5.14) y ponderarla la volvería canjeable contra el piso, lo que *"el
  suelo antes que el saldo"* prohíbe. **Y es LEY que el régimen hídrico, el nivel freático, el espesor de
  turba y la calidad del agua NO puedan entrar en el catálogo**: son medibles, están en este documento, y
  su no-medición es lo que permite el drenaje. El catálogo se registra con T13 y **no entra jamás en el
  numerador de la fórmula**.
- **POLÍTICA (votable).** **Qué entra en el catálogo** en cada unidad concreta —y con ello qué deja de
  medirse— es decisión deliberativa, con la categoría `critical` (quórum 60 %, consenso 75 %, T13,
  anti-flip-flop 14 días, `CHECK` en BD), exactamente igual que la plenitud aspiracional. **Y también es
  POLÍTICA el umbral de turba de la unidad** (§4-III), porque la fuente delega expresamente esa definición
  en las circunstancias nacionales y en la decisión de conservación.

**Sin esa doble frontera, «inefable» sería la vía más barata para vaciar el estándar** —y en un humedal,
la vía más barata para drenarlo.

---

## 11. Comparativa inter-reinos (lo que el humedal aporta y lo que no hereda)

El análisis completo de los cuatro estándares está en el documento
[09 de esta biblioteca](09_Comparativa_inter_reinos.md). Aquí se comparan **sólo los ejes en los que el
humedal tiene una posición propia**, y se contrasta con el bosque, que es el otro ecosistema ya desarrollado
en esta biblioteca (documento [10](10_Ecosistemas_Bosques.md)).

| Eje | SDV-H | SDV-A | **SDV-E — humedales** | SDV-E — bosques | SDV-S |
|---|---|---|---|---|---|
| **Sujeto** | La persona | La especie / el individuo | **Tipo de humedal evaluado sobre una unidad declarada; el régimen hídrico es su identidad** | Tipo de ecosistema sobre unidad declarada de área inmutable | La instancia |
| **Unidad de medida** | L/persona/día, kcal, m², µg/m³ | m²/animal, L/día, h/día | **cm de nivel freático, días/estacionalidad del régimen, cm de turba, t C/ha, individuos por gremio, unidades de pH, µg/L** | % del territorio, ha/año, m³/ha, t C/ha | Escala 0-1 |
| **Moneda temporal** | TVI | TA (PIU) | **TA — sin traducir aquí; el PIU es el único traductor; el ciclo del piso numérico es plurianual** | TA — sin traducir aquí | TPI |
| **Fuente del piso** | Dignidad + capacidades | Diseño biológico + etología | **Diseño biológico del humedal + una clase de drenaje del IPCC que NO es un estándar ecológico (traducción declarada)** | Diseño biológico + evaluación mundial que se autodeclara incompleta | Coherencia + precaución |
| **Piso dominante** | Nivel | Nivel | **Mixto: procedural en el eje maestro (0,20), numérico en su cara subsuperficial (0,18), no-regresión en cuatro dimensiones (0,40)** | Trayectoria "no perder" (4 de 8 pisos con requerido = 0) | Umbral 0-1 |
| **¿El sujeto reporta?** | Sí | No (tutor humano) | **No, y su representante tiene heurística laxa (R4/R13)** | No, y su representante no tiene autoridad verificada | Sí |
| **Par auditor** | Sí | Certificación | **No existe: ningún humedal audita a otro humedal** | No existe | AOS |
| **Instrumento del piso principal** | Encuesta / medición | Observación etológica | **Piezómetro + lista cerrada de indicadores de hidroperiodo: el régimen no se ve desde un satélite, pero su huella sí** | Inventario de campo (el bosque primario no se ve desde un satélite) | Sensores lógicos |
| **Remedio tras la violación** | Rehabilitación | Prohibición de mercado | **Ninguno: la turba perdida no vuelve y el suelo subsidiado no se des-subsidia** | Ninguno: 100 años de TA | Retractación + Ternura |
| **Riesgo propio** | Confundir Óptimo y Mínimo | Antropomorfismo | **Que el indicador suba mientras el piso cae (R16: espejo de agua; R17: designación)** | Reclasificación como cumplimiento (R14) | Juez y perito |
| **Zona Libre** | Binaria (VIII, IX) | No interferencia invasiva | **Binaria, sin peso (B-III), con la prohibición expresa de declarar inefable lo medible** | Binaria, sin peso (IX) | Ponderada (0,20) |
| **Estado** | 🟢 | 🟡 | **🔴 no existe (ni estándar ratificado ni código)** | 🔴 no existe | 🟢 (41 tests) |

### 11.1 Seis aportaciones del humedal a la familia de estándares

**A1 — El eje maestro partido: piso procedural arriba, piso numérico abajo.** Es el hallazgo estructural
de este documento. El régimen hídrico —que **define** si el humedal existe— **no tiene cifra** (0,20 del
peso, piso binario auditable mediante once indicadores y la condición ácuica), mientras su cara
subsuperficial **sí la tiene** (nivel freático, 0,18 del peso, 30 cm del IPCC). **El eje que define al
sujeto entra por estado; el que lo sostiene entra por número.** Ninguna otra dimensión de la familia tiene
esta asimetría, y el bosque presenta la inversa: su dimensión de mayor peso (primario, 0,18) es la que
ningún satélite puede medir.

**A2 — El piso numérico exige un ciclo plurianual, y eso bloquea el falso positivo por construcción.**
La clase de drenaje del IPCC se define sobre la **media anual de varios años** [VERIFICADO]. En términos de
INV2-E, esto significa que **una estación seca no puede disparar la Dimensión II**: el estándar no depende
de la buena voluntad del implementador para no generar falsos positivos, sino de la forma del umbral. Es la
traducción aritmética del hecho documentado de que muchos humedales **están secos parte del año**
`[REPORTADO — EPA, 2026; véase §14.2]` y de que *"incluso humedales que parecen secos durante partes
significativas del año… a menudo proveen hábitat crítico"*.

**A3 — El ecosistema puede mejorar los indicadores del tablero mientras pierde el piso.** Con cifras:
**+7 %** de área de estanques y gremios de agua abierta estables o en aumento, frente a **670.000 acres**
de humedal vegetado perdidos y **> 70 %** de pérdida acumulada en dos pasadores de marisma desde 1980
[VERIFICADO]. La consecuencia de diseño es inédita en la familia: **el estándar PROHÍBE dos parámetros que
podría medir** —la superficie de agua como cumplimiento del hidroperiodo y la abundancia total de aves
como cumplimiento de fauna—. Un estándar que prohíbe un indicador que sube es un estándar que ya sabe cómo
se le va a hacer trampa.

**A4 — Un parámetro candidato queda prohibido por doctrina, no por falta de dato.** El oxígeno disuelto
está nombrado por el canon (Cap. 10 §10.4) y el documento 07 le da 2 % de tablero; **en un humedal se
excluye de los pisos** porque la anoxia es **definitoria** —es la causa de la turba— y exigir OD alto en
una turbera **destruiría el ecosistema que dice proteger** (Queensland DETSI, 2023; IPCC, 2014, *Aquic*;
IUCN, 2021) [VERIFICADO]. No es un hueco: es una decisión, y se declara como tal.

**A5 — La irreversibilidad tiene unidad física.** En el bosque se mide en **tiempo** (*"un bosque tarda
100 años en crecer"*, Cap. 5 §5.5); en el humedal se mide en **centímetros**: turba oxidada *"se pierde
permanentemente del sistema"* y el suelo **subsidia** (International Peatland Society, 2020) [VERIFICADO].
Que la irreversibilidad sea medible en una unidad física la vuelve **directamente auditable** —es la
traducción operativa de T14 más limpia de toda la biblioteca— y es la razón de que la Dimensión III tenga
piso cero con línea base de espesor.

**A6 — Una fuente que delega el umbral a la política.** El IPCC *"no define un espesor mínimo del horizonte
orgánico, para permitir definiciones nacionales de suelo orgánico"* y *"los países pueden definir turba
según sus circunstancias nacionales"*; la IUCN añade que las definiciones *"varían entre países y a menudo
excluyen áreas de valor para la industria"* y *"deberían priorizar la conservación, la restauración y el
manejo sostenible"* [todo VERIFICADO]. **La frontera LEY/POLÍTICA del brief §3.3.12 no es aquí una
preferencia del proyecto: es la instrucción de la fuente.** El umbral de turba es POLÍTICA porque la
ciencia dice que lo es —y el riesgo de que esa política se fije a la medida del interés queda registrado
como R18.

### 11.2 Lo que este documento NO autoriza a concluir

1. **No autoriza a trasvasar umbrales entre ecosistemas.** El piso de un humedal no es el de un bosque: el
   hidroperiodo no es la cobertura, la turba no es el carbono del suelo mineral, el nivel freático no es el
   núcleo interior, y **el oxígeno disuelto prohibido aquí es obligatorio en el río** (documento 12).
2. **No autoriza a usar el 30 cm del IPCC como estándar ecológico publicado.** Es una **decisión de
   traducción** del proyecto, declarada, no ratificada por la fuente.
3. **No autoriza a tratar la definición de humedal (frecuencia y duración, anoxia, ≤ 6 m) como piso de
   integridad**, ni a convertir la designación Ramsar en certificado de salud.
4. **No autoriza a sustituir los mínimos por parámetro con un índice agregado** (§5.8), ni a leer la banda
   del compuesto como titular cuando hay violación declarada.
5. **No autoriza a compensar.** Ni crédito regenerativo contra drenaje, ni humedal creado contra humedal
   perdido, ni carbono contra régimen, ni restauración futura contra turba perdida.
6. **No autoriza a imputar violación por sequía estacional declarada, por ausencia de dato, ni por lectura
   instantánea** — y **no autoriza a declarar inefable** ninguno de los parámetros medibles de este
   documento.

---

## 12. Estado de implementación

**Regla aplicada:** se marca 🔴 **todo** lo que no tiene código y tests. Está prohibido afirmar que el
SDV-E, INV2-E, el ISE o los sensores de humedal están implementados: **no lo están**. Auditoría de solo
lectura sobre el repositorio, consumida del inventario de implementación de la rama y **con
comprobaciones propias de esta sesión** sobre el código (§12.2).

### 12.1 Lo que SÍ existe (y es honesto decir que existe)

| Pieza | Dónde | Estado |
|---|---|---|
| `r_units` negativo como crédito regenerativo | `app/micromax.py` (`log_cdd`), `app/micromax_bp.py` | 🟢 registrado y devuelto; **sin efecto contable** |
| Parte `eco-` (Ecosistema) | `app/parties.py` (`PARTY_TYPES`, `COLLECTIVE_PREFIXES`) | 🟢 creada y usable |
| Guardián oráculo del ecosistema | `app/contracts_bp.py` (`_guardian_approve_ecosystem()`) | 🟡 funciona en la **firma de contratos**; heurística laxa (R13) |
| **V no admite negativos; R sí** | `app/micromax.py` (validación `v_ucv < 0`) | 🟢 invariante de diseño real |
| Test del crédito regenerativo | `tests/test_micromax.py::test_credito_regenerativo_r_negativo` | 🟢 `r_units: -12.0` aceptado y devuelto |
| Test del guardián | `tests/test_maxocontracts/test_parties_escalas.py::TestEcosystemGuardian` | 🟢 2 casos (aprueba / deniega por γ) |
| SDV-S + INV2-S (el pariente más cercano) | `maxocontracts/` | 🟢 estándar + 41 tests |
| **Auditoría estructural de esta biblioteca** | `tests/test_sdv_e_biblioteca.py` | 🟢 **existe y es determinista**: verifica plantilla de secciones, separación Mínimo/Óptimo, LEY/POLÍTICA, frases prohibidas, ausencia de anclas de línea (`#L…`) y de rutas locales absolutas, y mínimo de URLs por documento |
| **Verificador de enlaces HTTP de la biblioteca** | `scripts/verificar_enlaces_sdv_e.py` | 🟢 **existe**: clasifica OK / BLOQUEADA (401/403/429) / MUERTA y devuelve código de salida duro |

### 12.2 Lo que NO existe — ninguna de las ocho dimensiones de este documento

| Pieza | Estado | Evidencia |
|---|---|---|
| **Cualquier dato de humedal ingestado** (hidroperiodo, nivel freático, turba, carbono, aves, agua, biota, conectividad) | 🔴 | cero sensores, cero APIs, cero satélites, cero ingestores en `app/`; ningún parámetro de este documento tiene fuente de datos conectada |
| **La palabra "humedal" en el código** | 🔴 | aparece **dos veces** en todo el código Python: un **comentario** en `app/micromax.py` (que nombra "arboladas, humedales, suelos" al explicar por qué R admite negativos) y el **nombre de una tarea** en una fixture de `tests/test_micromax.py`. **Cero ocurrencias** de `wetland`, `hidroperiodo`, `hydroperiod`, `nivel freático` o `turba` en `app/`, `frontend/`, `maxocontracts/`, `simulator/` y `scripts/` [VERIFICADO por búsqueda en esta sesión] |
| Clase `SDV_E` en el motor | 🔴 | no hay tipo en `maxocontracts/core/types.py`; el gemelo sería `SDV_S` |
| `INV2-E` | 🔴 | no hay `validate_invariant_sdv_e` en `maxocontracts/core/axioms.py` ni bloque validador |
| Los **10 metadatos obligatorios** de §6.3 (área de referencia, ciclo TA, tipo de humedal, serie de nivel freático, profundidad de turba, profundidad de carbono, línea base de gremios, régimen declarado, catálogo de presiones, dependencia hidrológica) | 🔴 | sin tabla ni columna; `maxo_parties` tiene 7 columnas genéricas |
| Identidad de la representación natural (los 7 campos del canon) | 🔴 | sin tabla |
| Mandato ecológico versionado / OCI | 🔴 | **`actor_kind` está cerrado a `{"human","synthetic"}`** (`app/synthetic_sessions.py`, con `raise ValueError` si no es uno de los dos) [VERIFICADO]: un guardián ecológico **no cabe en la bitácora** |
| Anti-suplantación de humedal | 🔴 | sin fuentes físicas múltiples ni comunidad testigo (**R4 abierto**) |
| Validación de la línea base declarada (el denominador del piso cero, §5.1) | 🔴 | no existe ningún campo de línea base; **elegirla baja es hoy gratis** |
| Traducción TA↔TVI ejecutable | 🔴 | `PIU.valorar_ta_natural` es un `pass` con comentario (`docs/architecture/DISENO_IMPLEMENTACION_FUTURA.md`) [VERIFICADO] |
| Contabilidad del crédito regenerativo | 🔴 | no existe `SUM(r_units)`; el R del sistema sólo cuenta extracción; el precio cierra en `max(0.0, …)` (`app/maxo.py`) [VERIFICADO]: **nunca es negativo** |
| Validación de `r_units` | 🔴 | acepta cualquier negativo (`-1e9`), no exige nota, evidencia, tercero ni techo; `NaN` e `inf` pasan el filtro |
| Normalización de piso cero con denominador de *stock* (§5.1) | 🔴 | no existe en `maxocontracts/blocks/sdv_validator.py` (y la variante por área del documento 10 tampoco sirve aquí) |
| Bandera de opacidad ecológica (§6.4) | 🔴 | sin implementación |
| Bloqueo por presión del catálogo `H2-*` sin expediente T14 | 🔴 | no existe el catálogo de presiones en código, ni el bloqueo |
| Distinción "humedal degradado" / "ex humedal" (cambio de identidad, §8.1) | 🔴 | no existe estado de identidad en el motor; el documento 02 §C4 lo propone en teoría |
| Quórum `eco-` N-de-M | 🔴 | el camino ecosistema retorna antes de la lógica de quórum; **el libro afirma lo contrario** (Cap. 16.5 §16.5.14) |
| Procedimiento de disputa | 🔴 | inexistente |
| Mapas vivos actualizados | 🔴 | `mapa_coherencia_ola4.md` no menciona `r_units`, el Reino Natural ni el SDV-E; `requisitos_fase2_ola4.md` no tiene ningún RF del Reino Natural |

### 12.3 El ISE, medido contra este documento: cero de ocho, y el eje maestro a cero

El único instrumento numérico previo del Reino Natural es el Índice de Salud Ecosistémica
(`docs/architecture/metricas_detalle_kpis_oraculos_dinamicos.md`, IN-01), **documento sin código**, con
cinco componentes ponderados: Biodiversidad 30 % · Calidad del agua 20 % · Calidad del aire 20 % · Salud
del suelo 15 % · Poblaciones de especies clave 15 % [VERIFICADO en el documento]. El desglose frente a las
dimensiones de §4 está en la tabla de §5.4, y su lectura sin adornos es: **cero de ocho dimensiones
cubiertas de forma completa, cuatro parciales, cuatro sin cobertura alguna**, y **el eje maestro entero
(0,38 del peso) con cobertura cero**. Además, **el 20 % del peso del ISE es calidad del aire**, que no es un
parámetro de humedal y pertenece al documento 23 de esta biblioteca.

**Consecuencia cuantificada:** si el humedal del ejemplo de §5.6 se evaluara **sólo con las dimensiones que
el ISE toca** —VI calidad del agua (0,12), VII biota (0,08) y V aves (0,10), con 0,30 de peso—, el
compuesto sería `0,0055 + 0,0333 + 0,0320 = 0,0708` y `FE ≈ 1,0734`. **El mismo humedal leería "Leve" por
el subconjunto del tablero y "Moderada" con violación declarada del eje maestro por el estándar.** La
diferencia no es de aritmética: es que **el subconjunto no puede ver el piso que define al sujeto**.

### 12.4 Incoherencias colaterales que no hay que heredar

- `resolve_participant_by_pid` (`app/parties.py`) asigna a una parte `eco-` **el SDV humano**
  (`sdv_actual=SDV()`), porque no existe SDV-E. [VERIFICADO]
- La R del contrato se persiste en la columna **`total_vhv_h` / `vhv_h`** (`app/schema.sql`,
  `app/contracts_bp.py`): nombre engañoso, sin `CHECK` de signo.
- `simulator/simulator.js` usa `v: -0.5` (V negativo) mientras `app/micromax.py` lo prohíbe.
- `docs/architecture/DISENO_IMPLEMENTACION_FUTURA.md` y los documentos de oráculos dinámicos describen
  sensores y fuentes **como si fueran arquitectura**, sin marcar que no están implementados.
- **La discrepancia de pH entre documentos de esta misma biblioteca.** El documento
  [07](07_Formula_de_violacion_y_pesos.md) §5.3 usa **6,5-8,4** con fuente FAO, 1994 (criterio de **agua de
  riego**), mientras este documento usa **6,5-9,0** (agua dulce) y **6,5-8,5** (salobre/salada) con fuente
  EPA, 1986 (criterio de **vida acuática**) [ambas fuentes VERIFICADAS en su propio documento]. **No es un
  error de ninguna de las dos: son dos objetos distintos** —el agua que se usa para regar y el agua que
  tiene que sostener vida acuática—, y el SDV-E debe declarar cuál aplica. Propuesta: **EPA para el estado
  del cuerpo de agua del humedal; FAO para el uso de riego**, declarado en el expediente. Queda como
  pregunta abierta 13.

**Estado de este documento:** texto de estándar redactado, **sin ninguna pieza de código asociada**. Este
documento no añade requisitos de implementación nuevos al backlog: **hace explícitos los que ya se derivan
del canon** y añade **cuatro** que son propios (la normalización de piso cero con denominador de *stock*,
los 10 metadatos obligatorios, los disparadores de §8.1 con el estado de cambio de identidad, y la
prohibición de los dos indicadores falsos positivos).

---

## 13. Preguntas abiertas

Lo que este documento **no** resuelve, dicho sin fingir cierre. **Ocho** de las catorce contienen un
`[SIN FUENTE VERIFICADA]`, y ése es el resultado, no la disculpa.

1. **El umbral numérico de frecuencia y duración del hidroperiodo — el vacío crítico.** No se localizó en
   esta sesión un umbral oficial en **días** ni en **% de la estación de crecimiento**. La fuente normativa
   (*Corps of Engineers Wetlands Delineation Manual*, 1987, y sus suplementos regionales) existe y está
   referenciada, pero `usace.army.mil` devolvió **403** a los clientes automáticos y `usgs.gov` devolvió
   **403** en todas las rutas probadas. **Vías de recuperación documentadas**: (a) una sesión humana abre
   el manual y el suplemento de Virginia (2010); (b) la definición de **Cowardin *et al.* (1979)** fija las
   clases de régimen hídrico (*permanently flooded*, *seasonally flooded*, *temporarily flooded*) con su
   duración — **no verificada en esta sesión** —; (c) literatura revisada por pares sobre hidroperiodo.
   **Si existe el número y no lo encontré, este documento está incompleto y debe corregirse.**
2. **La traducción de los 30 cm del IPCC.** El IPCC define la frontera entre *shallow-drained* y
   *deep-drained* para **inventario de GEI**. ¿Es 30 cm el piso ecológico correcto de un humedal, o sólo el
   número disponible? Este documento lo adopta **declarándolo como traducción** y no puede probar que sea
   el umbral ecológico. **Tarea del documento 06 y de la revisión de coherencia de la biblioteca.**
3. **El umbral de turba.** No existe mínimo universal y la fuente dice por qué (definiciones nacionales).
   Si el umbral es POLÍTICA, ¿quién lo vota, con qué carga de la prueba y con qué prohibición de fijarlo
   *después* de conocer el resultado? Aquí está el riesgo **R18**, y este documento no lo cierra.
4. **La normalización de piso cero con denominador de *stock* (§5.1).** Es una invención de este documento,
   no ratificada. Sin ella, **cuatro de los ocho pisos de un humedal no caben en la fórmula vigente**; con
   ella, el denominador (la línea base declarada) se vuelve el punto débil: **elegirla baja es la forma más
   barata de reducir el déficit**, y la inmutabilidad retroactiva es una defensa, no una prueba.
5. **El piso de aves acuáticas.** No hay umbral de población viable por especie (la fuente real está
   bloqueada a los agentes) y el piso de no-regresión por gremio **tolera un estado inicial malo**: una
   unidad cuyo gremio vegetado ya colapsó y no empeora, cumple. ¿Cuál es el piso de un humedal que **ya
   está degradado**? El canon no lo responde y este documento tampoco. **Tarea del documento 20
   (biodiversidad).**
6. **El oxígeno disuelto.** No hay cifra verificada **y** su uso está prohibido por doctrina (§4-VI). La
   pregunta abierta no es el número: es **la frontera de la prohibición** —¿qué humedales son "de agua
   libre y somera no turbosos" y por tanto sí pueden usar OD? Hoy esa frontera es `[HIPÓTESIS]` de este
   documento.
7. **Los nutrientes y el depósito atmosférico.** No hay valores verificados de N y P, y la fuente advierte
   que son específicos por ecorregión y tipo, con criterios narrativos preferidos. Queda abierto también
   **si el depósito atmosférico de nitrógeno** debe entrar como parámetro del humedal y con qué umbral:
   sería la única vía por la que la "calidad del aire" del canon (Cap. 10 §10.4) afecta a este documento, y
   no se verificó ninguna fuente en esta sesión.
8. **El régimen de fuego del humedal.** El canon lo nombra (Cap. 10 §10.4) y este documento **no tiene
   umbral**: lo que sí hay es la **quema de turba como fuente de emisión** (IPCC, 2014, Tablas 2.6 y 2.7) y
   el caso de Indonesia 2015 (*"casi 16 millones de toneladas de CO₂ al día"*, IUCN, 2021), que describen
   **el daño, no el régimen**. Pertenece al documento 22 (ciclos naturales) y aquí se declara la dependencia
   cruzada.
9. **La conectividad hidrológica.** No se verificó ninguna métrica cuantitativa. El piso es procedural
   (declaración de dependencia) y el riesgo declarado es grave: **una unidad puede cumplir todo y estar
   condenada por su cuenca**. Pertenece al documento 21 (conectividad).
10. **La terrestrialización natural frente al drenaje antrópico.** Un humedal **puede colmatarse y
    convertirse en tierra firme sin intervención humana**: forma parte del *"continuo hidroserial desde el
    agua abierta hasta la tierra firme, un proceso que toma miles de años"* (International Peatland
    Society, 2020) [VERIFICADO]. Si el sujeto cambia de identidad, ¿cómo se distingue el proceso natural
    del antrópico, quién soporta la carga de la prueba y qué pasa con la contabilidad de la unidad
    sucesora? La regla provisional de §8.1 es **T14: la prueba recae en quien propone la actividad**, pero
    **eso no resuelve el caso sin actividad humana identificable**. Es la pregunta más difícil de este
    documento.
11. **La unidad y el tipo.** El tipo de humedal es metadato obligatorio porque *"los humedales solo se
    comparan con otros humedales del mismo tipo"* (EPA) [VERIFICADO], y eso da base técnica a la solución
    "por tipo" del problema de la unidad del documento 02. **No hay**, en cambio, **superficie mínima
    verificada** para constituir una parte `eco-`, ni quórum N-de-M (propuesta del documento 05, no
    ratificada).
12. **Los pesos.** La tabla de §5.3 es una propuesta no ratificada, y la decisión de fondo es anterior:
    **¿puede una dimensión sin piso numérico cargar peso?** Las dos salidas —mantener I y VIII con peso, o
    moverlas a binarias sin peso y renormalizar a seis— están escritas en §5.3 y **ninguna está elegida**.
13. **La discrepancia de pH entre el documento 07 y éste** (§12.4): FAO, 1994 (riego, 6,5-8,4) frente a
    EPA, 1986 (vida acuática, 6,5-9,0 / 6,5-8,5). Propuesta: declarar el objeto de cada criterio y usar el
    pertinente. **Decisión de la revisión de coherencia de la biblioteca, no de este documento.**
14. **El catálogo de la Zona Libre.** El riesgo no es que sea binaria —eso lo fija el precedente del
    SDV-H—: es que **se declare inefable lo que sólo es incómodo de medir** (§10.2, violación (e)).
    ¿Quién soporta la carga de la prueba y cómo se impugna? El canon no lo resuelve; el documento 04 lo
    mecaniza y este documento **añade una prohibición**, pero no una garantía.

---

## 14. Referencias

**Regla aplicada.** Solo se citan URLs con **estado HTTP comprobado**. En esta sesión se comprobaron por
HTTP **las 38 URLs con esquema que cita este documento: 30 respondieron 200 y 8 respondieron 403** (reales,
rechazan clientes automáticos: un humano las abre), **ninguna 404**. Además se comprobaron **13 rutas
descartadas** (9 devolvieron 404 y 4 resultaron bloqueadas o sin respuesta), que se documentan en §14.2
**sin esquema** para no alimentar al verificador con enlaces muertos. Se distinguen las dos procedencias de
verificación porque la honestidad de una referencia incluye cómo se comprobó:

- **(S)** = **re-verificada en esta sesión** con petición HTTP real (cada fila lleva su código).
- **(R)** = registrada como verificada en la **sesión de verificación de fuentes de la rama**, octubre
  2026, documentada en `scratch/sdv_e/fuentes/11_humedales.md`, que **no es un documento de la biblioteca**
  y por tanto no se enlaza aquí como si fuera canon.

**Ninguna cifra de este documento se apoya en una fuente que no esté en 14.1 o 14.2.** Las cifras marcadas
`[REPORTADO]` se señalan individualmente en la tabla.

### 14.1 Fuentes que sostienen cifras y umbrales

**Hidroperiodo, definición de humedal y sustrato**

| Fuente | Aporte | URL (estado) |
|---|---|---|
| EPA — *What is a Wetland?* (definición legal, 40 CFR 120.2(c)(1)) | *"inundada o saturada por agua superficial o subterránea con una **frecuencia y duración** suficientes para sostener… una prevalencia de vegetación típicamente adaptada a condiciones de suelo saturado"* | https://www.epa.gov/wetlands/what-wetland **(S, 200)** |
| Queensland DETSI (WetlandInfo, 2023) — *Wetland definition* | Definición por tres atributos: sostiene plantas o animales adaptados **al menos periódicamente**; sustrato **no drenado**, saturado, inundado o encharcado **el tiempo suficiente para desarrollar condiciones anaerobias en las capas superiores**; o sustrato no edáfico saturado o cubierto de agua. Incluye **≤ 6 m** en marea baja (definición base Ramsar art. 1.1) | https://wetlandinfo.detsi.qld.gov.au/wetlands/what-are-wetlands/definitions-classification/wetland-definition.html **(S, 200)** |
| Queensland DETSI — *Queensland Wetland Definition Guideline* v2.1 (abr. 2025) | Ramsar arts. 1 y 2.1; anoxia de las capas superiores como condición definitoria | https://wetlandinfo.detsi.qld.gov.au/resources/static/pdf/facts-maps/mapping-method/qld-wetland-definition-guideline-v2.1-april25.pdf **(S, 200)** |
| Queensland DETSI — *Queensland Wetland Delineation Guideline* v2 | **Once indicadores aceptados de hidroperiodo** (basta uno); **horizonte de turba dentro de los primeros 0,3 m** como indicador de suelo de humedal y registro del espesor | https://wetlandinfo.detsi.qld.gov.au/resources/static/pdf/facts-maps/mapping/qld-wetland-delineation-guideline-v2.pdf **(S, 200)** |
| Queensland DETSI (2023) — *Wetland hydrological modification conceptual models* | **Catálogo oficial de presiones** con código: **H2-M5** cultivo · **H2-M9-a/b/c** drenaje parcial · **H2-M10-a/c** y **H2-M11-a/b/c/d** excavación · **H2-M6-a/b/f** hidrología superficial controlada · **H2-M13** canal construido · **H2-M7** canal en humedal · **H3-C1/C2-a/b/C4/C5-a/b** creación de humedal artificial. Componentes del ciclo del agua como procesos ecológicos (precipitación, escorrentía e infiltración, evaporación y evapotranspiración, descarga y recarga de agua subterránea, inundación, sedimentación, estratificación) | https://wetlandinfo.detsi.qld.gov.au/wetlands/ecology/processes-systems/anthropogenic/hydro-concept-mod/ **(S, 200 — respondió 200 en dos de tres intentos de esta sesión y sin respuesta en el tercero: el servidor limita las peticiones automatizadas; la URL es válida)** |
| NRCS (USDA) — *Field Indicators of Hydric Soils in the United States* | Metodología de campo de indicadores de suelo hidrico (suelos de humedal) | https://www.nrcs.usda.gov/resources/guides-and-instructions/field-indicators-of-hydric-soils-in-the-united-states **(S, 200)** |
| International Peatland Society (2020) — *What are peatlands?* (transcribe Ramsar art. 1.1; cifras de *PEATMAP* / Xu *et al.*, 2018) | Definición Ramsar art. 1.1 (**≤ 6 m**); *"la producción de materia orgánica excede su descomposición"*; *"el carbono… se seca y se oxida gradualmente a CO₂, y **se pierde permanentemente del sistema**"* + **compactación y subsidencia**; *"continuo hidroserial desde el agua abierta hasta la tierra firme, un proceso que toma miles de años"*; extensión **4,23 millones de km² = 2,84 %** de la tierra, **~84 %** natural o casi natural, **~16 %** drenada (=**0,5 %**) | https://peatlands.org/peatlands/what-are-peatlands/ **(S, 200)** |

**Nivel freático, turba y carbono**

| Fuente | Aporte | URL (estado) |
|---|---|---|
| IPCC (2014) — *2013 Supplement to the 2006 IPCC Guidelines: Wetlands*, **Cap. 2** *Drained Inland Organic Soils* | Clases de drenaje con frontera en **30 cm** (media anual, varios años): *shallow-drained* (< 30 cm) y *deep-drained* (≥ 30 cm) — Cap. 2 §2.1; **pérdidas de carbono por vía acuática** (DOC, POC, DIC) con factores de flujo (Tabla 2A.2) y **CH₄ en zanjas** (Tabla 2A.1); **quema de suelo orgánico**: consumo de combustible y factores de emisión en **g/kg** de materia seca (Tablas 2.6 y 2.7) | https://www.ipcc-nggip.iges.or.jp/public/wetlands/pdf/Wetlands_separate_files/WS_Chp2_Drained_Inland_Organic_Soils.pdf **(S, 200)** |
| IPCC (2014) — *Wetlands Supplement*, **Glosario** | **Drainage class** (frontera 30 cm); **Aquic** (capas virtualmente libres de oxígeno disuelto con ambiente reductor); **Organic soil**: *"las Guías IPCC 2006 no definen un espesor mínimo del horizonte orgánico, para permitir definiciones nacionales"*, con **un único criterio mencionado de 10 cm**; **Peat**: *"depósito blando, poroso o comprimido, sedentario, del cual una porción sustancial es material vegetal parcialmente descompuesto, con alto contenido de agua en estado natural (hasta ~90 %)"* y *"los países pueden definir turba según sus circunstancias nacionales"* | https://www.ipcc-nggip.iges.or.jp/public/wetlands/pdf/Wetlands_separate_files/WS_Glossary.pdf **(S, 200)** |
| IPCC — portal del *Wetlands Supplement* | Acceso al suplemento completo y a sus capítulos | https://www.ipcc-nggip.iges.or.jp/public/wetlands/ **(S, 200)** |
| IUCN (nov. 2021) — *Issues brief: Peatlands and climate change* | **Al menos 3 %** de la superficie terrestre; **> 3 millones de km²** de turbera casi natural; **hasta 44 %** de todo el carbono del suelo; **> 600 Gt C**; **0,37 Gt CO₂/año** secuestrado por turberas casi naturales; **1,9 Gt CO₂e/año** emitidos por turberas drenadas = **5 %** de las emisiones antropogénicas con **0,3 %** de la tierra; *"en algunas regiones, hasta 80 % de las turberas han sido dañadas"*; incendios de turba de Indonesia 2015: *"casi 16 millones de toneladas de CO₂ al día"*; *"las condiciones de anegamiento permanente frenan la descomposición vegetal… las plantas muertas se acumulan formando turba"*; definiciones de turbera *"varían entre países y a menudo excluyen áreas de valor para la industria"* y *"deberían priorizar la conservación, la restauración y el manejo sostenible"* | https://iucn.org/resources/issues-brief/peatlands-and-climate-change **(S, 200)** |
| Wetlands International — *Emission factors for managed peat soils* | Acceso disponible; **contenido no leído en esta sesión**: **no se cita ninguna cifra de esta fuente** | https://www.wetlands.org/download/4824/ **(R, 200 — contenido no leído)** |

**Ramsar — importancia internacional (eje de designación, NO de salud)**

| Fuente | Aporte | URL (estado) |
|---|---|---|
| Convención de Ramsar (Secretaría, 2025) — *Global Wetland Outlook 2025*, nota de prensa oficial | **0,52 %/año** de pérdida de humedales (*"desapareciendo más rápido que cualquier otro ecosistema"*); **22 %** perdido desde 1970; hasta **20 %** de los restantes podría desaparecer para 2050 con **39 billones USD** de beneficios en riesgo; **1 de cada 4** humedales restantes en **mal estado ecológico**; **~6 %** de la superficie terrestre y **> 7,5 %** del PIB global; **172 Partes Contratantes** y **> 2.530 sitios Ramsar** (~2,58 millones de km² = ~14-17 % de los humedales del mundo) | https://www.global-wetland-outlook.ramsar.org/new-page-39 **(S, 200)** |
| Convención de Ramsar — *Global Wetland Outlook* (portal) | Portal del informe | https://www.global-wetland-outlook.ramsar.org/ **(R, 200)** |
| Ramsar Sites Information Service (**RSIS**) — buscador oficial de sitios | Consulta de sitios por criterio, país y fecha de designación | https://rsis.ramsar.org/ris-search/ **(S, 200)** |
| Wetlands International — **Waterbird Population Estimates (WPE)** | **Base de datos oficial** contra la que se calculan los umbrales de los Criterios 5 y 6; el portal es accesible y el umbral del 1 % se consulta **por población y especie** | https://wpe.wetlands.org/ **(S, 200)** · https://wpe.wetlands.org/data/Threshold **(S, 200 — el valor se carga por JavaScript: no es legible por bot)** |
| Convención de Ramsar — Resolución XI.8 Anexo 2 (2012, enm. 2014): **Criterios 5 y 6** | **`[REPORTADO]`** — **Criterio 6**: un humedal es de importancia internacional si *"sostiene regularmente el **1 %** de los individuos de la población de una especie o subespecie de ave acuática"*; **Criterio 5**: *"**20.000 o más** aves acuáticas"*; **9 criterios** en total, basta **uno** para poder designar. **Texto leído sólo en fragmentos indexados por buscador**: el dominio responde **403** a los clientes automáticos | https://www.ramsar.org/sites/default/files/2025-10/cop11-res08-e-anx2_revcop15.docx **(S, 403 — real, no legible por bot)** |
| Convención de Ramsar — *Workbook: Introductory Course* | `[REPORTADO]` — contiene el texto de los 9 criterios; **no legible por bot (403)** | https://www.ramsar.org/sites/default/files/2023-11/Workbook_Introductory%20Course%20to%20the%20Convention%20on%20Wetlands.pdf **(S, 403)** |
| MedWet (Ramsar) — *The Ramsar Handbook for the Wise Use of Wetlands* (ficha) | Acceso a la ficha del manual; **contenido del manual no leído en esta sesión** | https://medwet.org/the-ramsar-handbook-for-the-wise-use-of-wetlands/ **(S, 200)** |
| Queensland DETSI — *Framework for describing the ecological character of Ramsar wetlands* | **Marco oficial** para describir el carácter ecológico de un sitio Ramsar (componentes, servicios, límites de cambio aceptable). **URL verificada (200); contenido NO leído**: la lectura falló con `fetch failed` en la sesión de la rama. **No se extrae ninguna cifra de esta fuente** | https://wetlandinfo.detsi.qld.gov.au/wetlands/resources/tools/assessment-search-tool/framework-for-describing-the-ecological-character-of-ramsar-wetlands/ **(S, 200 — contenido no leído)** |

**Aves acuáticas**

| Fuente | Aporte | URL (estado) |
|---|---|---|
| NABCI (2022) — *State of the Birds 2022*, sección *Waterfowl and Waterbirds* | **Casi un tercio** de las aves acuáticas en declive, incluidas varias especies de garzas y rascones **que dependen de marismas y humedales efímeros** | https://www.stateofthebirds.org/2022/waterfowl-and-waterbirds/ **(S, 200)** |
| NABCI (2022) — *State of the Birds 2022* (portada e índice) | Programa y edición; instrumento de referencia del estado de las aves | https://www.stateofthebirds.org/2022/ **(S, 200)** · https://www.stateofthebirds.org/2022/state-of-the-birds-by-habitat/ **(S, 200)** |
| USFWS (2024) — *2019 Wetlands Status and Trends Report* | *Seaside sparrow* y *saltmarsh sparrow* con **> 70 %** de pérdida acumulada **desde 1980**; **1/3** de las aves playeras; **92 %** de los humedales de agua dulce y **80 %** de los salinos son **vegetados**; **670.000 acres** de humedales vegetados perdidos (2009-2019); **116,4 millones de acres** de humedales en 2019 (**< 6 %** del área terrestre de los EE. UU. contiguos, **95 %** de agua dulce); **221.000 acres** perdidos con un aumento **> 50 %** respecto del estudio anterior; marisma salina **−2 %** (**−70.000 acres**); bosque de humedal de agua dulce **−426.000 acres**; ganancia neta de humedales **no vegetados** **+488.000 acres** (**+7 %** de área de estanques); conductores: desarrollo urbano y rural **> 53 %** y agricultura **26 %**; reversibilidad: *"acumulativos en el espacio y el tiempo y pueden ser difíciles de revertir"* y *"pueden pasar décadas, siglos o más antes de que los humedales restaurados funcionen como humedales naturales, si es que alguna vez lo hacen"* | https://www.fws.gov/project/2019-wetlands-status-and-trends-report **(S, 200)** |
| USFWS — *Wetlands Status and Trends* (metodología) | **5.048** parcelas de 4 millas cuadradas distribuidas aleatoriamente; reportes **decenales** al Congreso (*Emergency Wetlands Resources Act*, Public Law 99-645); **6** reportes nacionales y **8** regionales que cubren **1954-2019** | https://www.fws.gov/program/national-wetlands-inventory/wetlands-status-and-trends **(S, 200)** |
| eBird / Macaulay Library (Cornell Lab of Ornithology) | Plataforma de observación estructurada, abundancia relativa y fenología. **Fila corregida en la revisión adversarial**: antes se le asignaba la URL de NABCI `stateofthebirds.org`, que **es la fuente de las cifras de aves pero no la de este instrumento**. El informe de fuentes registra la plataforma, cita la autoría (Cornell Lab) y **no le fija URL propia**, así que aquí se declara el hueco en lugar de rellenarlo: **`[REPORTADO]`, sin URL verificada de su sede** (§14.2). **Ninguna cifra de este documento depende de esta fila** | *(sin URL propia: `[REPORTADO]` — §14.2)* |

**Calidad del agua**

| Fuente | Aporte | URL (estado) |
|---|---|---|
| EPA — *National Recommended Water Quality Criteria — Aquatic Life Criteria Table* (criterios de 1980-2024; *Gold Book*, 1986) | **pH agua dulce 6,5-9,0** · **pH agua salada/salobre 6,5-8,5** · **alcalinidad 20 mg/L** con la regla de la alcalinidad natural · **sulfuro (H₂S) 2,0 µg/L** (CCC) · **hierro 1.000 µg/L** (CCC) · **cloruro 860.000 µg/L** (CMC) y **230.000 µg/L** (CCC) · tabla CMC/CCC por contaminante (As, Cd, Cu, Hg, Ni, Pb, Zn, Se, amoníaco, cloro…). **El valor numérico del oxígeno disuelto NO se verificó**: la tabla remite al *Gold Book* de 1986 y a un documento aparte para agua salada | https://www.epa.gov/wqc/national-recommended-water-quality-criteria-aquatic-life-criteria-table **(S, 200 — tabla verificada; cifra de OD no verificada)** |
| EPA — *Wetland Water Quality Standards* (actualizado 2026) | **Advertencia estructural**: los estándares para humedales *"pueden diferir de los estándares de aguas superficiales corrientes"* y *"pueden depender menos de parámetros de química del agua y más de la diversidad de vegetación o de comunidades de macroinvertebrados"*; los criterios **narrativos** pueden ser *"más adaptativos y el enfoque preferido"* | https://www.epa.gov/wetlands/wetland-water-quality-standards **(S, 200)** |
| EPA — *Wetlands Monitoring and Assessment* | **Arquitectura de 3 niveles** (paisaje / protocolos rápidos calibrados contra el nivel 3 / evaluación intensiva HGM y biológica); **referencia por tipo**: *"los humedales solo se comparan con otros humedales del mismo tipo"* y contra condición mínimamente disturbada; **IBI de humedal** (documento de 6 métricas) | https://www.epa.gov/wetlands/wetlands-monitoring-and-assessment **(S, 200)** |
| EPA — *Wetlands Factsheet Series* | Serie de fichas divulgativas de la EPA sobre humedales (candidata a sostener la cita de humedales estacionales de §2-Regla 8; **no leída en esta sesión**) | https://www.epa.gov/wetlands/wetlands-factsheet-series **(S, 200)** |

**Contexto global y de política (calibración de bandas, no umbral de unidad)**

| Fuente | Aporte | URL (estado) |
|---|---|---|
| CBD — *Marco Kunming-Montreal* (Meta 3) | Meta **política** de conservar al menos el 30 % de las zonas terrestres y de aguas continentales para 2030; **votable, no LEY** | https://www.cbd.int/gbf **(S, 200)** |
| MedWet (Ramsar) — *Global Wetland Outlook 2025* (ficha) | Ficha de la edición 2025 del informe (las cifras del GWO 2025 de este documento provienen de la **nota de prensa oficial**, no del PDF completo: 6,89 MB excedía el límite de eficiencia fijado) | https://medwet.org/publications/global-wetland-outlook/ **(S, 200)** |

### 14.2 Fuentes reales que NO se pudieron usar (y por qué)

Se listan para que la ausencia de umbral en §4 tenga causa documentada, no sospecha. **Ninguna de ellas
sostiene una cifra de este documento.**

| Fuente | Motivo | Consecuencia |
|---|---|---|
| `https://www.mvp.usace.army.mil/portals/57/docs/regulatory/regulatorydocs/hydrologyncnesupplementapril2010.pdf` — **Suplemento hidrológico del Corps of Engineers (2010)** | **403 (verificado en esta sesión)** — bloqueo por Akamai a clientes automáticos | **EL VACÍO CRÍTICO (§13, pregunta 1):** contiene el umbral numérico de **frecuencia y duración** del hidroperiodo. Un humano lo abre. La dimensión de mayor peso del documento queda con piso procedural por esta única causa |
| `https://www.usgs.gov/special-topics/water-science-school/science/hydroperiod` — **USGS, *Hydroperiod*** | **403 (verificado en esta sesión)** | Era la fuente más deseable para el parámetro central. Sin ella, el hidroperiodo se define por las fuentes de la EPA y de Queensland |
| `https://www.ramsar.org/` y sus documentos de criterios (incluidos los citados en 14.1) | **403 (verificado en esta sesión)** — todo el dominio rechaza clientes automáticos | Los umbrales de los Criterios 5 y 6 (**20.000 aves**, **1 %** de una población) quedan `[REPORTADO]`, **no verificados**. Que el redactor no los presente como verificados: **es la limitación más grave de esta investigación en el foco Ramsar** |
| `https://www.unep.org/resources/report/global-peatlands-assessment-2022` — *Global Peatlands Assessment* (UNEP / Global Peatlands Initiative) | **403 (documentado por la sesión de la rama)** | Habría dado la cifra oficial de turberas y de su degradación; se usan en su lugar las de IUCN 2021 e IPS 2020 |
| `https://www.usgs.gov/special-topics/water-science-school/science/wetlands-and-water-quality` | **403** | Sin la fuente USGS de calidad de agua en humedales; se usa la EPA |
| `https://www.ser.org/page/SERStandards/International-Standards-for-the-Practice-of-Ecological-Restoration` | **403** | Sin el marco de "recuperación" para la columna del Óptimo |
| `dcceew.gov.au/water/wetlands/publications/criteria-identifying-wetlands-international-importance` (Gobierno de Australia) | **403 en la sesión de la rama; 000 (sin respuesta) al re-comprobarlo en esta sesión** | Sin fuente gubernamental alternativa para los criterios Ramsar |
| Rutas **muertas** (404) de la EPA, el NRCS, el USFWS, el IPCC, MedWet, Wetlands International y el NPS: `epa.gov/wetlands/indicators-wetland-condition` · `epa.gov/wq-tech/templates-developing-wetland-water-quality-standards` · `nrcs.usda.gov/resources/data-and-reports/hydric-soils` · `nrcs.usda.gov/sites/default/files/2023-01/Field-Indicators-of-Hydric-Soils-in-the-United-States.pdf` · `fws.gov/sites/default/files/documents/2019-wetlands-status-and-trends-report.pdf` · `ipcc.ch/report/2013-supplement-to-the-2006-ipcc-guidelines-for-national-greenhouse-gas-inventories/` (la ruta viva del suplemento es `ipcc-nggip.iges.or.jp`, 14.1) · `medwet.org/publications/ramsar-handbook/` (la viva es `medwet.org/the-ramsar-handbook-for-the-wise-use-of-wetlands/`, 14.1) · `wetlands.org/publication/waterbird-population-estimates/` (la viva es `wpe.wetlands.org`, 14.1) · `nps.gov/subjects/wetlands/hydroperiod.htm` | **404 (S — re-comprobadas en esta sesión)** | **No se citan.** Se listan para que la búsqueda del umbral de hidroperiodo no se repita por las mismas rutas muertas |
| **Cita de humedales estacionales y *vernal pools*** (atribuida a **EPA, 2026** en §2-Regla 8) | **`[REPORTADO]`** — el informe de fuentes de la rama la atribuye a la EPA (2026) **sin fijar la URL exacta** | Este documento **no le asigna URL**: la usa como `[REPORTADO]` y declara la carencia. La URL candidata es la *Wetlands Factsheet Series* (14.1, 200, **no leída en esta sesión**); **no se afirma que sea su origen** |
| `wpe.wetlands.org/data/Threshold?conservation=7` | **200 pero sirve sólo el título de la aplicación**: los valores del umbral del 1 % se cargan por JavaScript | Se cita el **portal** como base oficial de consulta (14.1); **este documento no transcribe ningún valor de umbral de esa consulta** |
| **eBird / Macaulay Library** (Cornell Lab of Ornithology) | **`[REPORTADO]` sin URL propia**: el informe de fuentes de la rama registra la plataforma y su autoría pero **no le fija una URL**, y la que este documento le asignaba antes (`stateofthebirds.org/2022/`) es de **NABCI**, no de la plataforma | Se cita el instrumento declarando el hueco (**§4-V**). **Ninguna cifra de este documento se apoya en esta fila**; si se quiere usar como fuente de un piso, un humano debe verificar primero su sede y su estado HTTP |
| `docs/architecture/DISENO_IMPLEMENTACION_FUTURA.md` y `oraculos_dinamicos_…` — sensores y fuentes ecológicas descritos como arquitectura | **Documentos del repositorio, no implementación** | Se citan **como diseño**, nunca como código existente (§12) |

**Nota de formato deliberada.** Las rutas descartadas de las tres últimas filas se escriben **sin esquema**
(`http` / `https`) a propósito. El verificador de enlaces de esta biblioteca
(`scripts/verificar_enlaces_sdv_e.py`) extrae **toda** URL con esquema y clasifica como **MUERTA**
cualquiera que no responda 200-299 ni 401/403/405/406/429: escribir aquí rutas muertas con esquema pondría
en **ROJO** un documento que precisamente las declara **no citables**. La información se conserva —para que
nadie repita la búsqueda por las mismas rutas— y el verificador no recibe un enlace muerto que no es una
cita. Las que sí responden 403 (Ramsar, USGS, USACE, UNEP, SER) **conservan su URL completa** porque el
verificador las clasifica como **BLOQUEADA**, que es la clasificación correcta: son reales y un humano las
abre.

### 14.3 Referencias internas al canon (por capítulo y sección, sin anclas de línea)

La cita doctrinal es **por capítulo y sección** y no depende del enlace. Los enlaces se dan a continuación
sólo como comodidad de lectura, y se comprobó en esta sesión que **cada archivo destino existe**.

- Cap. 5 §5.2-§5.5 — Tres tiempos (TVI, TA, TPI), **el PIU como único traductor TA↔TVI**, el costo en TA de
  los ecosistemas (*"un bosque tarda 100 años en crecer"*) y el axioma **T14** (precaución
  intergeneracional): [capitulo_05_arquitectura_260126.md](../../book/edicion_3_dinamica/capitulo_05_arquitectura_260126.md)
- Cap. 7 §7.9 — Zona Libre (el valor inefable):
  [capitulo_07_vhv_260126.md](../../book/edicion_3_dinamica/capitulo_07_vhv_260126.md)
- Cap. 8 §8.3-§8.6 y §8.11 — Criterios de validación, dimensiones del SDV-H, fórmula y pesos, y
  **dimensiones binarias VIII y IX sin peso**:
  [capitulo_08_sdv_h_260126.md](../../book/edicion_3_dinamica/capitulo_08_sdv_h_260126.md)
- Cap. 9 §9.3-§9.9 — Criterios del SDV-A, dimensiones por especie y árbol plano de la base de datos de SDV
  (§9.7): [capitulo_09_sdv_a_260126.md](../../book/edicion_3_dinamica/capitulo_09_sdv_a_260126.md)
- Cap. 9.5 §9.5.5-§9.5.11 — `FS_S = e^v` y base neutra, elenco de sensores, INV2-S y retractación a 7
  ciclos, Veto por Crimen de Coherencia:
  [capitulo_09_5_sdv_sinteticos_260126.md](../../book/edicion_3_dinamica/capitulo_09_5_sdv_sinteticos_260126.md)
- Cap. 10 §10.3-§10.8 — Principio Precautorio de Consciencia, **SDV para Ecosistemas y para Lugares
  (§10.4)**, proporcionalidad, dignidad encadenada, **gobernanza operacionalmente finita (§10.7)** y
  criterios de Persona Sintética:
  [capitulo_10_tres_reinos_260126.md](../../book/edicion_3_dinamica/capitulo_10_tres_reinos_260126.md)
- Cap. 16.5 §16.5.14 — **El Reino Natural como conviviente**: el caso canónico del humedal del conjunto,
   crédito regenerativo `r_units`, **TA soberano**, representación `eco-` y guardián oráculo, Zona
  Libre, *"el suelo antes que el saldo"*, *"cuidado ≠ extracción estética"* y *"medir todo sería la forma
  técnica de dejar de escucharlo"*:
  [capitulo_16_5_micromaxocracia_canonica_220826.md](../../book/edicion_3_dinamica/capitulo_16_5_micromaxocracia_canonica_220826.md)
- Cap. 17 — INV2 e invariantes de MaxoContracts:
  [capitulo_17_maxocontracts_260126.md](../../book/edicion_3_dinamica/capitulo_17_maxocontracts_260126.md)
- EVV-1.2 §4.3 — R negativo = regeneración:
  [capitulo_18_EVV_1.2_270126.md](../../book/edicion_3_dinamica/capitulo_18_EVV_1.2_270126.md)

### 14.4 Referencias internas a la biblioteca y al repositorio

**Documentos de esta biblioteca que existen** (los que no existen se citan por número y título, sin enlace,
en §1):

- Documento [02](02_Unidad_y_sujeto_del_SDV-E.md) — Unidad y sujeto: los cinco criterios (delimitación,
  referibilidad taxonómica, escala, **continuidad de identidad C4** — colapso y cambio de identidad, que
  este documento usa en §3 y §8 —, y representación).
- Documento [04](04_Zona_Libre_del_Reino_Natural.md) — **Zona Libre del Reino Natural**: cuatro estados,
  siete puertas, recinto y no porcentaje, presunción de integridad, inventario negativo.
- Documento [05](05_Representacion_guardian_y_mandato.md) — Representación, guardián y mandato: los 7 campos
  de identidad, dimensiones de la representación y propuesta de quórum N-de-M.
- Documento [07](07_Formula_de_violacion_y_pesos.md) — **Fórmula, pesos y escala de bandas**: déficit
  normalizado, operadores, base neutra, duración en TA; su §5.8 usa el humedal como ejemplo aplicado y su
  §5.3 fija los pesos del catálogo general.
- Documento [08](08_INV2-E_invariante.md) — Especificación de **INV2-E**: tipos, estados, propiedades
  formales, precondición de validez y retractación.
- Documento [09](09_Comparativa_inter_reinos.md) — Comparativa inter-reinos: base neutra, **insight I3 (sin
  par auditor)**, **I7 (el ISE como tablero y no como estándar)**, **I9 (la inversión de "sin dato no
  castiga")** e **I11 (la prevención como remedio completo)**.
- Documento [10](10_Ecosistemas_Bosques.md) — Bosques: la normalización de piso cero (§5.1) que este
  documento adapta a denominador de *stock*, los metadatos obligatorios y los disparadores de INV2-E.
- Documentos [13](13_Ecosistemas_Oceanos_y_costas.md) · [14](14_Ecosistemas_Suelos_vivos.md) ·
  [16](16_Ecosistemas_Montanas_y_criosfera.md) · [18](18_Ecosistemas_Agroecosistemas.md) — Otros tipos de
  ecosistema ya desarrollados.

**Documentos de esta biblioteca que NO existen todavía** (citados por número y título, sin enlace): `00`
índice · `01` doctrina · `03` no colonización del TA · `06` medición y verificación T13 (elenco de
sensores) · `12` ríos y cuencas · `15` praderas y sabanas · `17` zonas áridas · `19`-`24` dimensiones
transversales, en particular **`20` biodiversidad**, **`21` conectividad**, **`22` ciclos naturales** y
**`23` agua y aire** · `40` procesos de creación, actualización y gobernanza.

**Repositorio:**

- Índice de Salud Ecosistémica (IN-01), pesos, bandas y umbrales de alerta:
  [metricas_detalle_kpis_oraculos_dinamicos.md](../../architecture/metricas_detalle_kpis_oraculos_dinamicos.md)
- Riesgos R4, R6 y R13: [blindaje_anti_gamificacion_equidad.md](../../architecture/blindaje_anti_gamificacion_equidad.md)
- Identidad de las representaciones naturales (7 campos) y autogobierno federado:
  [continuidad_identidad_autogobierno_federado.md](../../architecture/continuidad_identidad_autogobierno_federado.md)
- Mapas vivos de la Ola 4 (donde el Reino Natural **no aparece**):
  [mapa_coherencia_ola4.md](../../architecture/mapa_coherencia_ola4.md) y
  [requisitos_fase2_ola4.md](../../architecture/requisitos_fase2_ola4.md)
- Auditoría estructural de esta biblioteca: [test_sdv_e_biblioteca.py](../../../tests/test_sdv_e_biblioteca.py)
- Verificador de enlaces HTTP de esta biblioteca:
  [verificar_enlaces_sdv_e.py](../../../scripts/verificar_enlaces_sdv_e.py)
- Estándar SDV-S completo: [SDV-S_Suelo_Dignidad_Vital_Sinteticos.md](../SDV-S_Suelo_Dignidad_Vital_Sinteticos.md)
- SDV como principio universal e INV2:
  [SDV_Suelo_Dignidad_Vital_importancia_MaxoContracts.md](../SDV_Suelo_Dignidad_Vital_importancia_MaxoContracts.md)

**Nota final sobre el alcance de esta §14.** El inventario completo de la sesión de verificación de la rama
—33 URLs verificadas, 24 muertas y 16 bloqueadas— vive en `scratch/sdv_e/fuentes/11_humedales.md`, que **no
es un documento de la biblioteca** y por eso no se enlaza aquí como si fuera canon. Las afirmaciones de la
§12 se verificaron **por lectura directa del repositorio y por búsqueda en el código**, no por URL. Y las
**38 URLs con esquema de este documento se comprobaron en esta misma sesión con petición HTTP real**
(30 × 200 y 8 × 403, ninguna 404); de ellas, las que sostienen los pisos de las ocho dimensiones son
**nueve**: la
definición legal de la EPA, la definición y la guía de delimitación de Queensland, el catálogo de presiones
de Queensland, el Cap. 2 y el Glosario del suplemento de humedales del IPCC, el informe de turberas de la
IUCN, el informe de estado y tendencias del USFWS, el estado de las aves acuáticas de NABCI y la tabla de
criterios de vida acuática de la EPA. **Todo lo demás de este documento son decisiones declaradas, no
datos.**

---

**Cierre.** Este documento define **ocho dimensiones ponderadas y tres binarias sin peso** para el
ecosistema humedal, con **un** piso numérico directo (calidad del agua), **un** piso numérico que es una
traducción declarada (nivel freático), **cuatro** pisos de no-regresión con línea base, **dos** pisos
procedurales y **nueve** parámetros `[SIN FUENTE VERIFICADA]` explícitos (§1 y §13 llevan el inventario)
— y **el hidroperiodo, de peso 0,20, es el primero de los nueve**. La cifra que resume su estado es la del
§5.3: **de los 1,00 de peso declarado, 0,30 tiene número, 0,40 depende de que alguien haya declarado y
fechado una línea base, y 0,30 entra como estado.** Y su hallazgo doctrinal es incómodo: **el eje que
define al humedal —su régimen hídrico— es el que no tiene cifra, mientras su cara subsuperficial sí la
tiene.** Eso no es una debilidad de la redacción: es el estado de la ciencia de humedales, y el único modo
de escribir un estándar honesto sobre ella es decir dónde está el borde del conocimiento y qué se hace
mientras tanto. Lo que se hace mientras tanto es lo que el canon ya decidió: **T14** —elegir la opción de
menor irreversibilidad y poner la carga de la prueba en quien propone—, **el suelo antes que el saldo** —el
crédito regenerativo no levanta un bloqueo, y un humedal creado no repone el drenado— y **T13** —la
contabilidad nunca se borra, porque en una turbera perdida el registro es lo único que queda—. Un humedal
no firma, no declara y no reclama. Este documento es, por ahora, todo lo que tiene.
