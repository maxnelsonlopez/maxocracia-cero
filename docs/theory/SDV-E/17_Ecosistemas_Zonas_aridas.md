# Ecosistemas de zonas áridas y tierras secas
## Los mínimos de lo que vive con poca agua: neutralidad en la degradación de la tierra, agua subterránea, costras biológicas y umbral de irreversibilidad — y por qué lo árido no es degradado

**Autoría:** Oráculo Sintético DeepSeek & Max Nelson López Restrepo
**Fecha:** octubre 2026
**Proyecto:** Maxocracia — El gobierno de la verdad, el tiempo y la vida
**Licencia:** Creative Commons BY-SA 4.0
**Estado:** Propuesta de estándar (rama SDV-E, Ola 4) — NO canon hasta ratificación
**Referencia canónica:** Cap. 10 §10.4 · Cap. 16.5 §16.5.14 · EVV-1.2 §4.3 · Cap. 9.5 (precedente SDV-S)
**Documento:** 17 de la biblioteca `docs/theory/SDV-E/`

---

## 1. Qué es (y qué no es) este SDV

**Qué es.** Este documento fija los mínimos por debajo de los cuales una **unidad ecológica de tierras
secas** pierde integridad: la neutralidad de su degradación medida como tendencia contra su propia línea
base, el agua subterránea que la sostiene, la capa viva de su suelo (costras biológicas y
criptobiótica), su capacidad de recuperarse después de una sequía, el uso ganadero que soporta sin
morir y los humedales y oasis que la habitan. Es el estándar del único ecosistema del SDV-E **cuyo
estado de referencia no es verde**, y esa sola frase obliga a reescribir el modo en que la familia mide
salud.

**Las cuatro tesis de apertura.** No son opiniones del proyecto: son definiciones del marco
internacional que este documento adopta como punto de partida y cita en su literalidad.

1. **Lo árido no es degradado.** El IPCC fija la frontera operativa: las zonas hiperáridas —índice de
   aridez inferior a 0,05— *"se incluyen en las tierras áridas, pero quedan excluidas de la definición
   de desertificación (UNCCD 1994)"*, y *"los desiertos son ecosistemas valiosos (…) sin embargo, no se
   consideran propensos a la desertificación"* [REPORTADO, IPCC SRCCL Cap. 3, 2019]. Un desierto con
   índice de aridez 0,03 **no está degradado**: está en su estado de referencia. Cualquier índice que
   puntúe ese desierto como ecosistema fallido está midiendo una preferencia estética, no un umbral
   ecológico.
2. **La degradación es una tendencia contra una línea base, no una fotografía.** *"La desertificación
   no se limita a formas irreversibles de degradación de la tierra, ni se equipara a la expansión del
   desierto, sino que representa todas las formas y niveles de degradación de la tierra que ocurren en
   las tierras áridas"* [REPORTADO, IPCC SRCCL Cap. 3, 2019]. Es la misma arquitectura que el principio
   4 de la LDN: **el objetivo es igual a la línea base** [REPORTADO, UNCCD].
3. **Aridez no es sequía, y la sequía es un ciclo natural que el canon manda respetar.** *"La aridez es
   un rasgo climático de largo plazo (…). La aridez es distinta de la sequía, que es un evento climático
   temporal (…). Además, las sequías no se restringen a las tierras áridas"* [REPORTADO, IPCC SRCCL
   Cap. 3, 2019]. El canon ya nombra el ciclo: *"Ciclos naturales respetados (fuego, inundación,
   sequía)"* (Cap. 10 §10.4). **Consecuencia formal, y es la que ningún otro documento de esta
   biblioteca puede escribir: un año seco no puede ser una violación del SDV-E.** Solo lo es la pérdida
   de la capacidad de recuperarse después del evento (§4.2, D4).
4. **Bombear un acuífero fósil es la forma más literal de colonizar el tiempo de un ecosistema.** La
   escala de recarga de un acuífero árido se mide en miles de años; la de su extracción, en décadas.
   Ese desajuste es el objeto de §5.5 y la razón de que este ecosistema tenga **tiempo propio TA
   (Tiempo Absoluto), no TVI**, y de que el **PIU** (Cap. 5 §5.5) sea su único traductor.

**El hallazgo de apertura, y es incómodo.** Búsqueda sobre el canon escrito
(`docs/book/edicion_3_dinamica/`, los capítulos fuente, sin el libro compilado): la palabra
*desiertos* aparece **una vez**, y es un sustantivo dentro de una enumeración —
*"**Ecosistemas**: Bosques, humedales, desiertos, arrecifes"* (Cap. 10 §10.4)—; *desierto* reaparece solo
como **ejemplo de comunidad** que *"aplicará un multiplicador alto al componente R_agua"* (Cap. 6
§6.4 y Cap. 7 §7.9); *sequía* aparece **una vez**, en la lista de ciclos naturales (Cap. 10 §10.4). Y
*desertificación*, *aridez*, *árido* y *UNCCD* tienen **cero ocurrencias en todo el capítulo fuente y
cero en `docs/architecture/`**. [VERIFICADO: búsqueda directa sobre el repositorio en esta sesión]
Consecuencia que este documento asume sin dramatizarla: **el SDV-E de las tierras secas hereda del
canon dos sustantivos y una lista de ciclos** —nada más que una decisión doctrinal previa—, y hereda
del método lo esencial: el estándar primero, la contabilidad después (Cap. 16.5 §16.5.14), el
precedente del SDV-S y el axioma T14.

**Qué no es.**

- **No es un documento que confunda «verde» con «sano».** Es su objeto central evitarlo. Aquí el sesgo
  tiene nombre técnico y consecuencia contable: un índice de verdor aplicado a una unidad árida
  **puntúa el estado de referencia como fallo** y **premia la sustitución de la comunidad nativa por
  una cobertura más verde**. §3.5 lo convierte en regla del estándar.
- **No es el estándar del suelo ni el del agua.** El carbono orgánico del suelo y la salinidad tienen
  dueño doctrinal en el [documento 14](./14_Ecosistemas_Suelos_vivos.md) §4 (D2 y D4); el caudal
  ecológico superficial, en el documento 12 (Ríos y cuencas); la hidroperiodicidad de un humedal, en el
  documento 11 (Humedales); **el fuego y la herbivoría como ciclos, en el documento 15 (Praderas y
  sabanas), que los trata como dimensiones** —aquí el pastoreo es una dimensión con protocolo y umbral
  de uso, no una repetición de aquel tratado—; la calidad del agua y del aire, en el documento 23. Este documento **no los duplica**:
  aporta lo que solo existe en la tierra seca —la neutralidad de la degradación como marco, el
  acuífero como sujeto, la costra biológica, el umbral de irreversibilidad y el oasis—.
- **No es un documento de umbrales publicados, y hay que decirlo en la primera página.** A diferencia
  del SDV-H, el marco internacional de las tierras áridas **no publica pisos absolutos**: la LDN es
  *relativa a la línea base de cada territorio por diseño* (UNCCD, principio 4). Lo que sí publica son
  **reglas de integración** (la regla «uno fuera, todos fuera» del principio 16), **jerarquías**
  (Evitar > Reducir > Revertir, principio 12) y **factores de uso** (el 50 % de utilización de forraje
  del USDA NRCS). **El alcance de esa ausencia hay que decirlo con precisión, porque el documento sí
  usa un umbral publicado en D5**: no existe **ningún** piso absoluto de estado (cobertura, productividad,
  carbono, nivel freático, costra biológica) — el 50 % del NRCS es un **factor de uso ganadero
  publicado**, es decir gestión y no estado, y este documento lo usa como tal, con su margen de ajuste
  por sitio. Por tanto la columna **Mínimo Absoluto** de este documento se construye casi entera
  como `[HIPÓTESIS]` declarada sobre la línea base de la propia unidad. **Ocultarlo sería inventar**, y
  este documento no inventa.
- **No es un documento de contabilidad.** Es el *estándar primero*. Hoy el crédito regenerativo
  (`r_units` negativo) está **implementado y probado en su registro** —y en nada más: no suma, no pondera
  y no bloquea, §9—, e **INV2-E no existe**: se puede acumular crédito
  mientras la tierra se degrada y el sistema no lo detecta. Esa es la frase que abre esta biblioteca y
  es literal del canon: *"Un conjunto con crédito regenerativo acumulado pero humedal bajo su SDV-E no
  está en coherencia: **INV2-E será su juez**"* (Cap. 16.5 §16.5.14).
- **No es canon.** Es una propuesta de estándar de la rama SDV-E, Ola 4, **no ratificada**.

**Marcas de evidencia usadas en todo el texto.** `[VERIFICADO]` = cifra leída en la fuente citada, con
la URL y su estado HTTP comprobados en la sesión de verificación de esta rama. `[REPORTADO]` = dato
afirmado por una fuente que se cita, leído en su página resumen. `[HIPÓTESIS]` = inferencia razonada
del proyecto —normalmente **la conversión de un valor de estado, o de una regla relativa, en un piso
normativo**, que es exactamente lo que el marco internacional no hace—. `[SIN FUENTE VERIFICADA —
pendiente de consenso científico]` = se buscó el umbral y no existe fuente verificable. Las cuatro
marcas son resultados legítimos, y la cuarta es un resultado de primera clase.

**Trazabilidad.** La verificación de fuentes de este documento vive en el registro de trabajo
`scratch/sdv_e/fuentes/17_aridas.md` (documento de trabajo, **no** de la biblioteca): **35 URLs
verificadas** (HTTP 200 re-comprobado al cierre de la sesión), **14 bloqueadas** a agentes automáticos
(403/203, reales: un humano las abre) y **24 muertas o descartadas** por irrelevancia. El informe
recoge **44 filas de parámetro con fuente verificada** y **3 filas marcadas sin fuente**, que este
documento respeta como vacíos declarados. Las afirmaciones sobre el código de la §12 se verificaron
**por lectura directa del repositorio en esta sesión**, no por URL. Todo enlace citado aquí se
re-comprueba con `scripts/verificar_enlaces_sdv_e.py`.

---

## 2. Preámbulo metodológico

El SDV-H lo tiene; el SDV-S lo omitió y el brief de esta biblioteca prohíbe repetir la omisión. Aquí es
obligatorio por una razón propia: **este es el ecosistema donde el piso no es un número importable, sino
una fecha y un lugar**. Seis reglas gobiernan lo que sigue.

**Regla 1 — Separar siempre valor de estado, regla de integración y umbral normativo.** Confundirlos es
el error que este documento más fácilmente cometería. Ejemplos de las tres cosas, tomados de las
fuentes: un **valor de estado** es que hasta el 40 % de la tierra está degradada [REPORTADO, UNCCD
GLO2, 2022]; una **regla de integración** es que un solo sub-indicador en negativo declare pérdida
(UNCCD, principio 16); un **umbral normativo** es el 50 % de utilización de forraje del USDA NRCS. Solo
lo tercero es un piso de uso; solo lo segundo es arquitectura de invariante; lo primero es un dato. El
documento etiqueta cada fila de sus tablas con una de las tres naturalezas.

**Regla 2 — El piso es LEY y no se vota; la plenitud es POLÍTICA y se vota.** Es la regla que el brief
marca como crítica y el error histórico del SDV-H (confundir el Óptimo del agua con su Mínimo
Absoluto). Precedente operativo del Parlamento Educativo (INV2-EDU, categoría `critical`: quórum 60 %,
consenso 75 %, T13, anti-flip-flop 14 días, `CHECK` en BD): la ley vive en el motor y **no es votable**;
la plenitud aspiracional **sí es votable**. En las tierras secas esta separación tiene una trampa
específica que la Regla 3 desmonta.

**Regla 3 — La plenitud de una tierra seca no puede ser el verde, y el piso no puede ser importado de
una norma ajena.** Dos prohibiciones simétricas:

- **Prohibición del óptimo verde.** En una unidad árida, «más cobertura vegetal» **no es** la plenitud
  aspiracional: puede ser la firma de una invasión leñosa, de una especie exótica o de un riego que
  saliniza. El Óptimo de cada dimensión se define como **el régimen propio de la unidad**, no como un
  valor absoluto de biomasa.
- **Prohibición del piso importado.** El propio IPCC advierte que *"el índice de aridez no es un proxy
  preciso para delimitar las tierras áridas en un ambiente con CO₂ creciente"* y que *"la utilidad de
  los umbrales de IA aplicados actualmente para estimar la superficie de tierras áridas es limitada
  bajo cambio climático"* [REPORTADO, IPCC SRCCL Cap. 3, 2019]. Es decir: **el umbral de aridez es un
  criterio LEY para clasificar, no un criterio de salud**, y encima pierde poder de delimitación. No se
  usa como vara de estado, y su degradación bajo cambio climático es pregunta abierta (§13.2).

**Regla 4 — Distinguir cuatro cosas que se confunden siempre.** (a) No existe el umbral en la
literatura; (b) existe y no se verificó; (c) existe y es una **proyección**, no una norma; (d) existe y
es **norma o regla publicada**. En este documento: (a) es el caso de las costras biológicas, del umbral
de irreversibilidad y del piso absoluto de carbono orgánico del suelo; (b) no aplica, no se cita nada
sin verificar; (c) es el caso del estrés hídrico proyectado a 2050 y de la proyección del oasis del sur
de Túnez; (d) es el caso de la regla «uno fuera, todos fuera» (UNCCD principio 16), de la jerarquía
Evitar > Reducir > Revertir (principio 12), del factor de uso del 50 % (USDA NRCS) y del **umbral de
clasificación del índice de aridez** (IPCC) —que clasifica, no juzga salud—. **Cuatro reglas publicadas
y tres vacíos declarados: ese es el balance real de este estándar, y el lector tiene derecho a saberlo
antes de la primera tabla.**

**Regla 5 — El tiempo del sujeto manda, y en tierra seca el tiempo del sujeto es fósil.** El tiempo de
este ecosistema es **TA (Tiempo Absoluto)**, no TVI ni TPI, y no se coloniza: *"el tiempo del territorio
es TA y no se coloniza (el PIU traduce)"* y *"nosotros registramos la interacción, no la vida interna
del ecosistema"* (Cap. 16.5 §16.5.14). Aquí la regla no es retórica: el agua de un acuífero árido se
recarga en **miles de años** y se extrae en **décadas** `[HIPÓTESIS: el informe de fuentes de esta rama
documenta el desajuste de escalas como carácter propio del acuífero árido fósil, pero no fija las dos
cifras como rango publicado; se declaran como caracterización del proyecto, contrastable en cada unidad
contra su tiempo de recarga declarado]`; el suelo se forma en siglos y se erosiona —
según el propio marco— hasta **100 veces más rápido** que su tasa de formación natural [REPORTADO,
UNCCD, 2022]. El crédito regenerativo se acumula en la escala humana. **No hay tipo de cambio entre las dos
unidades de tiempo, y §9 lo demuestra con aritmética.**

**Regla 6 — La gobernanza debe ser operacionalmente finita (Cap. 10 §10.7).** El SDV-E de las tierras
secas **no puede** exigir modelar el ciclo hidrológico completo de un acuífero transfronterizo ni la
cadena trófica del desierto para decidir. El mejor precedente externo de finitud que este documento
encontró es el propio conjunto mínimo de la LDN: **tres métricas y una regla booleana, sin modelo**
(UNCCD, principio 15 y 16; Copernicus CLMS/JRC, 2025). Un estándar de tres indicadores y un booleano es
un estándar que se puede cumplir; un modelo climático-hidrológico-pastoral integrado, no.

**Corolario de honestidad.** Donde este documento no sabe, lo dice con la marca correspondiente y lo
repite en §13. Un documento que admite «no lo sé» vale más que uno que aparenta cerrar todo.

---

## 3. Pilares epistemológicos

Cinco pilares sostienen este estándar. Los cuatro primeros son heredados; **el quinto es propio de las
tierras secas y es el que organiza todo el documento**.

1. **Proporcionalidad (Cap. 10 §10.5).** El nivel de protección debe ser *"lógico, proporcional y
   adecuado a la naturaleza de la entidad"*. Un acuífero no recibe el trato de un río visible ni el de
   una persona: no se le pide consentimiento verbal ni se le mide el caudal, porque **no tiene caudal
   superficial**. Se le mide el nivel piezométrico, la salinidad acoplada y el tiempo de recarga, que
   es lo que su naturaleza exige.

2. **Dignidad encadenada (Cap. 10 §10.6).** *"Dignidad Humana ←→ Dignidad Ecosistémica ←→ Dignidad
   Material. Cada eslabón depende de los demás."* En las tierras secas el eslabón tiene cifra, y tiene
   **dos cifras que no coinciden** — y este documento las cita ambas sin promediarlas, porque
   promediarlas sería inventar: el IPCC afirma que las tierras áridas albergan *"unos 3 000 millones de
   personas"* [REPORTADO, IPCC SRCCL Cap. 3, 2019, sobre van der Esch *et al.* 2017], mientras la nota
   del GLO2 de la UNCCD afirma que son el hogar de *"una de cada tres personas"* (≈ 2 700 millones)
   [REPORTADO, UNCCD, 2022]. **Las dos cifras no coinciden y no se resuelven aquí**: se declaran. Y el
   dato de extensión tampoco es único: **46,2 % (± 0,8 %)** de la superficie terrestre según el IPCC
   [REPORTADO, 2019], *"más del 45 %"* según la UNCCD [REPORTADO, 2022].

3. **Precaución ante quien no puede consentir.** El **Principio Precautorio de Consciencia** (Cap. 10
   §10.3) y, sobre todo, **T14 — Principio de Precaución Intergeneracional** (Cap. 5): *"Ante
   incertidumbre sobre el impacto en agentes que no pueden consentir (ecosistemas, generaciones
   futuras, posibles consciencias sintéticas), el sistema debe elegir la opción de menor
   irreversibilidad, documentando el costo de oportunidad asumido. La carga de la prueba recae sobre
   quien propone acciones que afectan la temporalidad de no-participantes."* **T14 es el axioma más
   fuerte disponible para este documento**, y aquí tiene una traducción institucional exacta que el
   proyecto no tiene que inventar: la jerarquía de respuesta de la LDN —**Evitar > Reducir >
   Revertir**, con *"avoid"* y *"reduce"* con prioridad sobre revertir (UNCCD, principio 12)— es
   literalmente «la carga de la prueba recae sobre quien propone degradar». Que dos marcos
   independientes coincidan en la misma asimetría es la mejor evidencia disponible de que la asimetría
   no es un sesgo del proyecto.

4. **No-antropocentrismo (T9).** La formulación que trata la tierra seca como *terreno baldío*,
   *tierra no productiva* o *superficie en espera de uso* viola el axioma, aunque la fórmula esté bien
   escrita. El IPCC da el respaldo externo: los desiertos *"son ecosistemas valiosos"* y no se
   consideran propensos a la desertificación [REPORTADO, 2019]. §4.2 (D7) convierte esta prohibición en
   una regla contable concreta.

5. **Pilar propio: en una tierra seca el estado de referencia no es verde, y la salud se mide como
   distancia respecto de la propia línea base.** Es el pilar que organiza el documento entero, y tiene
   tres consecuencias que ningún otro documento del SDV-E tuvo que enfrentar:

   - **El «Óptimo» deja de ser un número más alto.** En el SDV-H el óptimo del agua es más litros y en
     el SDV-A más metros cuadrados por animal. Aquí, **más cobertura no es mejor**: el óptimo es el
     régimen de la unidad. Presentar la plenitud como una magnitud creciente sería introducir en el
     estándar el sesgo que el estándar existe para evitar.
   - **El piso tiene fecha y dueño.** El mínimo absoluto no se importa de una norma: se toma contra una
     **línea base de la propia unidad**, que alguien mide, fecha y certifica. Eso introduce un problema
     de gobernanza que ningún otro reino de la familia tiene (§5.2, y el eje nuevo de §11).
   - **Un índice de verdor puede subir mientras la unidad se degrada, y puede bajar mientras está
     sana.** Ambas direcciones del error son posibles, y §5.2 las convierte en prohibiciones contables.

---

## 4. Dimensiones del SDV-E

Seis dimensiones con peso (D1-D6) y **una dimensión binaria sin peso** (D7, la Zona Libre de las tierras
secas, §4.2). Las seis primeras se agrupan en tres familias que conviene no confundir, porque **se
violan en direcciones distintas**:

- **Familia «el proceso»** (D1, D4): si la tierra pierde o se recupera, y si puede recuperarse. Son
  dimensiones **de tendencia**: no describen un estado, describen una derivada contra la línea base.
- **Familia «el recurso que no se ve»** (D2, D3): el agua subterránea y la capa biológica del suelo.
  Son las dos dimensiones **invisibles** del ecosistema: no aparecen en una imagen de satélite
  convencional, y son las que deciden si lo visible sobrevive.
- **Familia «el uso y el refugio»** (D5, D6): el pastoreo, que es un ciclo natural y no una agresión, y
  el humedal árido, que es el punto donde el agua sí aparece y por tanto donde la presión humana se
  concentra.

La distinción importa por una razón operativa: un índice que promedie las tres familias sin declarar
cuál pesa **premiaría la desaparición del proceso con la aparición del refugio**, o al contrario. Por
eso §5.3 declara los pesos como propuesta explícita y no como medición.

---

### Dimensión D1: Neutralidad en la degradación de la tierra (la tendencia contra la propia línea base)

**Qué protege.** Que la unidad **no pierda** capacidad de sostener su función ecológica: que la
cobertura de su suelo, su productividad primaria y su carbono orgánico no retrocedan respecto del
estado que la propia unidad declaró como referencia. Protege una **derivada**, no un nivel.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| Conjunto mínimo de sub-indicadores (indicador ODS 15.3.1) | **3 sub-indicadores obligatorios**: cobertura del suelo + productividad primaria neta (NPP) + carbono orgánico del suelo (COS) | ídem — es un conjunto cerrado, no una aspiración | UNCCD, principio LDN 15 · Copernicus CLMS/JRC, 2025 |
| **Regla de integración (el piso del invariante)** | **«Uno fuera, todos fuera» (1OAO): si UNO de los tres muestra cambio negativo significativo ⇒ PÉRDIDA** | — | UNCCD, principio LDN 16 |
| Regla de ganancia | — | **≥ 1 indicador positivo y ninguno negativo ⇒ GANANCIA** | UNCCD, principio LDN 16 |
| Jerarquía de respuesta (orden obligatorio) | **Evitar > Reducir > Revertir**; *"avoid"* y *"reduce"* tienen **prioridad** sobre revertir | — (es un orden, no una meta) | UNCCD, principio LDN 12 |
| Definición del objetivo | **El objetivo LDN es igual a la línea base de la propia unidad** | igual a la línea base | UNCCD, principio LDN 4 |
| Contrapeso entre pérdidas y ganancias | **Misma escala** que la planificación del uso del suelo (nacional/subnacional) y **«like for like»**: no compensar entre tipos de ecosistema distintos salvo ganancia neta | — | UNCCD, principios LDN 8 y 9 |
| Estado global de referencia *(valor de estado, no umbral)* | — | — | **Hasta 40 %** de la tierra degradada, **40 %+** de la superficie con uso agrícola [REPORTADO, UNCCD GLO2, 2022]. **Dato de estado: no es piso, no es meta y no entra en la columna de Mínimo Absoluto** |
| Proyección a 2050 del escenario tendencial *(proyección, no umbral)* | — | — | **16 millones de km²** de degradación continuada; caída persistente de la productividad vegetal del **12-14 %** en tierras agrícolas, de pastoreo y naturales [REPORTADO, UNCCD GLO2, 2022] |
| Compromiso mundial de restauración *(valor de estado, no piso)* | **1 000 millones de ha** de tierras degradadas para 2030, con **115+ países** comprometidos — es un compromiso declarado, no un mínimo de la unidad | — | [REPORTADO, UNCCD GLO2, 2022] |
| Retorno de la inversión en restauración *(valor de estado, no piso)* | **7-30 USD** por cada USD invertido — cifra de retorno agregada, no un piso ecológico | — | [REPORTADO, UNCCD GLO2, 2022] |
| Piso absoluto de COS en t C/ha o % para tierras áridas | **[SIN FUENTE VERIFICADA — pendiente de consenso científico]**: la LDN es relativa por diseño y **no publica un piso absoluto**. El suelo lo trata el [documento 14](./14_Ecosistemas_Suelos_vivos.md) §4 (D2) | — | Búsqueda en UNCCD, FAO y Copernicus CLMS en la sesión de verificación de esta rama |

**Justificación.** Esta dimensión es la de mayor peso del documento, y su justificación no es
ecológica sino **arquitectónica**: el principio 16 de la UNCCD es, literalmente, la forma de un
invariante. *Un solo indicador en negativo invalida la neutralidad*, por muchos positivos que haya en
los otros dos. El marco explica además por qué usa esa lógica booleana: la regla 1OAO existe para
*"prevenir falsos positivos o negativos"* [REPORTADO, Copernicus CLMS, 2025, sobre la GPG v2]. Es la
versión institucional del *"el suelo antes que el saldo"* del canon (Cap. 16.5 §16.5.14): **la
neutralidad agregada no puede tapar una pérdida local.** Y el principio 12 (Evitar > Reducir > Revertir)
es la traducción operativa de T14: la carga de la prueba recae sobre quien propone degradar.

**Nota de coherencia obligatoria — la LDN NO autoriza compensar.** El principio 7 de la LDN admite
contrapesar pérdidas con ganancias *"en el mismo marco temporal"*. Eso **no equivale** a compensación de
crédito regenerativo, y el propio marco lo delimita: el principio 8 exige la **misma escala** que la
planificación territorial y el 9 el **«like for like»**. Es un mecanismo de **planificación del uso del
suelo**, no un mercado de compensaciones. Regla que este documento fija a partir de ello `[HIPÓTESIS]`:
**la unidad del SDV-E es más pequeña que la escala de planificación de la LDN, de modo que el contrapeso
del principio 7 no puede invocarse dentro de la contabilidad de la propia unidad.** Si una unidad pierde
en un sub-indicador, su SDV-E está violado; que el país compense en otra provincia es asunto de la
planificación nacional y **no de este estándar**. Sin esa frontera, la LDN se leería como una licencia
de compensación, que es exactamente lo que no es.

**Protocolo.** Los tres sub-indicadores se computan **por terceros** con la guía GPG v2 del ODS 15.3.1
(Copernicus CLMS / JRC, 2025), que además simplificó los métodos estadísticos y clarificó la
interpretación de **severidad y nivel de confianza** [REPORTADO]. Cobertura del suelo y NPP por
teledetección; COS por el método alineado con los *IPCC 2019 Refinements* [REPORTADO, Copernicus CLMS,
2025] y con el mapa mundial de referencia de la FAO (**GSOCmap**, primera compilación global país por
país armonizada) [VERIFICADO, FAO]. La **línea base se declara antes** de cualquier contrato que afecte
a la unidad (§5.2) y no se re-negocia después de medir.

**Violación.** Observación concreta que constituye violación: **uno cualquiera de los tres
sub-indicadores muestra un cambio negativo significativo respecto de la línea base declarada de la
unidad**, informado por el cálculo de tercero con la guía vigente. Es un hecho, no una opinión, y es
**binario**: no se gradúa promediando los otros dos. Si la unidad **no tiene** línea base declarada ni
cómputo de tercero, no se declara violación **ni** cumplimiento: se registra `[SIN DATO]` (§6), y
`[SIN DATO]` **no es coherencia** (§9).

---

### Dimensión D2: Agua subterránea y acuíferos (el tiempo fósil que se bombea)

**Qué protege.** El acuífero que sostiene la unidad: que su nivel no descienda de forma sostenida, que
la salinidad acoplada al descenso no destruya la aptitud del sistema, y que la extracción no exceda la
recarga a una escala que ninguna contabilidad humana puede alcanzar.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **Nivel piezométrico de la unidad** | `[HIPÓTESIS]` **ningún descenso sostenido respecto de la línea base de la propia unidad**; el marco internacional **no publica un piso absoluto de nivel freático** | **Estabilización del nivel** en la ventana de la unidad | Construcción del proyecto sobre UNCCD principio LDN 4 (relatividad a la línea base) e IPCC SRCCL Cap. 3, 2019 |
| Ventana de profundidad para uso extractivo — **caso local, y NO es un piso** | — **no es Mínimo Absoluto**: es una **ventana óptima local de uso**, no un piso ecológico generalizable (la propia fuente lo dice). El piso de esta dimensión es el de la fila anterior: ningún descenso sostenido contra la línea base | **1-2 m** de profundidad (oasis del Souf, Sahara argelino) — ventana óptima declarada; conviene registrar que **más del 77 % del área ya la excede** | Khezzani & Bouchemal, *Environmental Earth Sciences* 77, vía FAO **AGRIS**, 2018 |
| Tasa de descenso del nivel freático — **caso local** | — | **0,29 (2011) → 2,37 (2015) m/año**: se multiplica por 8 en cuatro años | Khezzani & Bouchemal, vía FAO AGRIS, 2018 |
| Descenso absoluto documentado (Ghamra, 2015) — **caso local** | — | **18,2 m** | Khezzani & Bouchemal, vía FAO AGRIS, 2018 |
| Acoplamiento descenso ↔ salinidad — **relación documentada, no umbral** | — | **R > 0,99** entre descenso del freático y conductividad eléctrica en el caso Souf | Khezzani & Bouchemal, vía FAO AGRIS, 2018 |
| **Estrés hídrico** (retiro de agua / oferta renovable) — **alerta de cuenca, NUNCA piso ni violación** | — **no entra al piso**: es un indicador de cuenca y de año, no de ecosistema; registrarlo como violación trasvasaría un umbral entre sujetos (documento 09 §11.9) | **40 % = alto · 80 % = extremadamente alto** como niveles de referencia de la fuente; disparador de revisión, jamás déficit | WRI, **Aqueduct 4.0**, 2023 |
| Población bajo estrés hídrico alto ≥ 1 mes/año *(estado)* | — | — | **≈ 4 000 millones** (≥ 50 % de la humanidad); **25 países** en estrés extremadamente alto (**25 %** de la población mundial) [REPORTADO, WRI, 2023] |
| Proyección 2050 *(proyección, no umbral)* | — | — | **+1 000 millones** de personas bajo estrés extremo; **MENA al 100 %** de su población [REPORTADO, WRI, 2023] |
| Contexto global del recurso *(estado)* | — | — | **110 000 km³/año** de precipitación sobre tierra; **43 000 km³/año** de recursos renovables [REPORTADO, FAO AQUASTAT, metodología de uso del agua] |
| Escala temporal de la recarga frente a la extracción | `[HIPÓTESIS]`: **ningún denominador contable puede ser más corto que el tiempo de recarga del recurso que consume** (§5.5) | — | Construcción del proyecto sobre la asimetría documentada en IPCC SRCCL Cap. 3, 2019 |

**Justificación, y su parte incómoda.** El caso del oasis del Souf es el mejor material disponible y
**no es un estándar**: son **65 puntos de medición, 2010-2015**, en un acuífero concreto. La ventana de
1-2 m es una **ventana óptima de uso extractivo local**, no un piso ecológico generalizable, y el
documento lo dice en la propia tabla. Lo que **sí** es generalizable es la estructura del daño, y está
documentada: descenso del freático → ascenso de sales por capilaridad y evaporación → salinización →
pérdida de aptitud agrícola → abandono del sistema de cultivo. La fuente lo cierra con un hecho, no con
una proyección: la sobreexplotación *"llevó a la desaparición del sistema de cultivo del patrimonio
agrícola mundial (Ghout)"* [REPORTADO, FAO AGRIS, 2018]. El IPCC confirma el mecanismo en términos
generales: *"los oasis en climas hiperáridos están usualmente sujetos a escasez de agua, ya que la
evapotranspiración excede la precipitación. Esto a menudo causa salinización de los suelos"*
[REPORTADO, 2019].

**Las dos advertencias que el documento debe poner sobre la mesa.**

1. **El estrés hídrico no es una violación.** La propia WRI advierte que *"el estrés hídrico no conduce
   necesariamente a una crisis hídrica"* [REPORTADO, 2023]. Un valor de 40 % o 80 % es una **alerta de
   cuenca**, no un hecho de ecosistema: tratarlo como violación sería trasvasar un umbral entre sujetos,
   que el [documento 09](./09_Comparativa_inter_reinos.md) §11.9 prohíbe. Entra al estándar como
   **disparador de revisión**, nunca como déficit.
2. **El agua subterránea árida es un recurso fósil.** La escala temporal de su recarga —miles de años—
   es incompatible con la de su extracción —décadas—, y ese desajuste **es la definición operativa de la
   colonización del TA** en este ecosistema. No es una metáfora: es la razón de que §5.5 proponga un
   criterio verificable específico para tierras secas.

**Frontera con los documentos 12, 14 y 23.** Esta dimensión **no** mide caudal superficial (documento
12), **no** mide salinidad del suelo ni umbrales de CEe (documento 14 §4 D4, que además declara la
discrepancia entre el 2 dS/m verificado de la FAO y el 4 dS/m clásico no verificado —este documento **no
repite ni resuelve esa cifra**) y **no** mide calidad del agua de consumo (documento 23). Mide lo que
solo existe aquí: **el acuífero como sujeto del que depende la unidad, y su nivel como serie temporal.**

**Protocolo.** Serie piezométrica de los pozos de la unidad, en metros de profundidad y en metros sobre
el nivel del mar, medida por el servicio hidrológico nacional o por red de pozos de observación
(ninguno de los dos pertenece hoy al proyecto, §12). Frecuencia: **al menos una campaña anual en la
misma fecha estacional del ciclo propio de la unidad**; en unidades bajo extracción intensiva, continua.
La serie se contrasta obligatoriamente con la conductividad eléctrica del agua o del suelo, por el
acoplamiento documentado (R > 0,99). El **indicador de estrés hídrico** se consulta anualmente de la
fuente de tercero (WRI Aqueduct) y solo como alerta. Los datos de extracción se reportan con la
metodología de uso del agua de FAO AQUASTAT, que distingue tipos de extracción [VERIFICADO].

**Violación.** Dos hechos concretos, distintos y no intercambiables:

1. **Violación de tendencia (graduable, canal A):** **descenso sostenido del nivel piezométrico** de la
   unidad respecto de su línea base declarada, informado por una serie con al menos **dos observaciones
   comparables** en el tiempo (mismo pozo, misma fecha estacional, mismo método). No se declara con una
   sola campaña, y no se declara con una serie de recarga estimada por modelo sin observación.
2. **Violación terminal (veto V2, canal B):** **salinización acoplada al descenso que destruye la
   aptitud del sistema** —el caso Ghout es el precedente documentado—. Es un **estado**, no un número:
   `CONSUMADO_IRREVERSIBLE`. Una vez que la sal sube por capilaridad, **ningún crédito regenerativo
   devuelve el sistema de cultivo**, y la fuente lo documenta en pasado.

---

### Dimensión D3: Costras biológicas del suelo y criptobiótica (la piel viva que se confunde con escombros)

**Qué protege.** La comunidad de cianobacterias, algas, líquenes, briófitos y microorganismos que forma
la **costra biológica del suelo** (*biocrust*): la capa que en una tierra seca protege la superficie de
la erosión, retiene agua, fija nitrógeno y constituye, en muchos casos, la única cubierta viva del
suelo. Protege lo que los sistemas de clasificación llaman «suelo desnudo» y que con frecuencia **no
está desnudo**.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| Cobertura mínima de costras biológicas antes de que se dispare la erosión | **[SIN FUENTE VERIFICADA — pendiente de consenso científico]** | **[SIN FUENTE VERIFICADA]** | Búsqueda en USDA Forest Service, USGS, ScienceDirect y Annual Reviews: **todas las candidatas devolvieron 403** en la sesión de verificación de esta rama |
| Tasa de fijación de nitrógeno por costras biológicas | **[SIN FUENTE VERIFICADA]** | **[SIN FUENTE VERIFICADA]** | idem |
| Proporción de la superficie terrestre cubierta por costras biológicas | — **No se cita**: las cifras que circulan en la literatura **no se verificaron en esta sesión** y quedan fuera del documento por regla de oro | — | — |
| **Indicador provisional propuesto** `[HIPÓTESIS]` | **Presencia / ausencia** de costra biológica en las parcelas de referencia de la unidad, con dos señales acompañantes: (a) **suelo desnudo** con desviación respecto de la referencia, y (b) **erosión hídrica** con clase de desviación | Cobertura continua y sin fragmentación en las parcelas de referencia | USDA NRCS / BLM, *Interpreting Indicators of Rangeland Health* TR 1734-6 (portal BLM verificado; el documento se cita como estándar de indicadores cualitativos-cuantitativos con desviación de referencia) |
| **Sensibilidad al pisoteo y al pastoreo** | — **No hay piso**: no se obtuvo en esta sesión ningún valor numérico | — | — |
| **Fuente identificada y pendiente de apertura humana** | — | — | Artículo de *Catena* sobre el umbral de cobertura de costras por encima del cual se controla la erosión en tierras áridas (`S0341816224006003`): **existe y contiene el umbral que este documento busca**, pero devuelve **403** a clientes automáticos. **Es lo primero que debería abrir una persona** |

**Justificación, y es la admisión central de este documento.** El **indicador** de carbono orgánico del
suelo está perfectamente documentado en el marco internacional; el de costras biológicas **no lo está en
esta sesión**. No se obtuvo **ninguna** fuente con valor numérico, organismo y año sobre cobertura
mínima, fijación de nitrógeno, extensión global o sensibilidad al pisoteo. Este documento **no fabrica
el umbral**, por tres razones:

1. **No es un vacío de búsqueda, es un vacío verificado.** Todas las candidatas serias (USDA Forest
   Service RMRS-GTR-135, USGS, ScienceDirect, Annual Reviews) bloquearon el acceso automático. Un 403
   es evidencia de que la fuente existe y de que un humano puede abrirla; **no** es evidencia de su
   contenido, y citar su cifra de memoria sería exactamente la invención que el brief prohíbe.
2. **La dimensión existe aunque el umbral no.** Que no haya piso publicado no la convierte en Zona
   Libre: hay instrumento capaz de medirla (observación de campo, fotografía escalada, transectos) y
   por tanto, según la prueba de inefabilidad del [documento 04](./04_Zona_Libre_del_Reino_Natural.md)
   §10.3, es **medición pendiente**, no inefabilidad. **Ese es el argumento por el que esta dimensión
   NO puede pesar cero** (§5.3): un peso de 0,00 sería la vía más barata para que la Zona Libre se
   tragara una deuda de medición.
3. **La costra biológica tiene una trampa de clasificación que hay que desactivar antes de medirla.**
   Es la aportación técnica más útil de esta dimensión: **en español, y en el mismo estándar, «costra»
   significa dos cosas opuestas.**

   | Término | Qué es | Qué significa | Dónde vive |
   |---|---|---|---|
   | **Costra física** (*crusting*) | Capa delgada **impermeable** que dificulta la emergencia de plántulas, reduce la infiltración y **favorece la escorrentía y la erosión** | **Degradación** | [Documento 14](./14_Ecosistemas_Suelos_vivos.md) §4 (D5) |
   | **Costra biológica** (*biocrust*) | Comunidad viva que **protege** la superficie, retiene agua y fija nitrógeno | **Salud** | Este documento, D3 |

   Confundirlas sería un error de tipos con consecuencia contable directa: **un suelo cubierto de
   costra biológica puede estar clasificado como «suelo desnudo» por un sistema de cobertura del suelo,
   y con ello el sub-indicador de cobertura de D1 leería salud como degradación.** Este documento exige
   por tanto que, en unidades áridas, la clase «suelo desnudo» del sub-indicador de cobertura **se
   verifique en campo antes de computarse** `[HIPÓTESIS]`. Si no se verifica, el sub-indicador no es
   válido (§6, regla de elegibilidad del dato) — y el estándar **no lo rellena**.

**Protocolo.** Parcelas de referencia georreferenciadas y repetibles, con transectos y fotografía
escalada, en dos momentos: antes de la intervención que se juzga y después. Se registra
**presencia/ausencia** de costra biológica, su fragmentación y las dos señales acompañantes de
*Interpreting Indicators of Rangeland Health* (suelo desnudo y erosión hídrica, con clase de desviación
respecto de la referencia). Frecuencia `[HIPÓTESIS]`: **anual en unidades pastoreadas o pisoteadas**,
cada 3-5 años en el resto, alineada con la medición de COS del documento 14. Quién reporta: **la
comunidad de custodia y la comunidad testigo** (§7), con verificación por tercero cuando exista. No
existe hoy **ningún programa global de monitoreo de costras biológicas**, y ese vacío se declara en vez
de disimularse.

**Violación.** Dos hechos concretos:

1. **Pérdida de la costra biológica en las parcelas de referencia** de la unidad respecto de su línea
   base, informada por dos observaciones comparables con fotografía y fecha (T13). Es un hecho
   observable, no una estimación.
2. **Clasificación de un suelo con costra biológica como «suelo desnudo» usada como prueba de
   degradación**, sin verificación de campo. No es violación del ecosistema: es **condición de
   invalidez del cómputo** del sub-indicador de cobertura de D1, por el mismo principio que el
   documento 14 aplica al COS sin método declarado.

**Lo que esta dimensión no puede hacer, y lo dice.** Sin umbral publicado no puede graduar la pérdida:
su déficit entra como **binario dentro del canal A** (pérdida / no pérdida), y su umbral queda
`[SIN FUENTE VERIFICADA — pendiente de consenso científico]` **con la fuente ya localizada y bloqueada**.
Eso es un resultado, no un fracaso.

---

### Dimensión D4: Resiliencia y umbral de irreversibilidad (lo que no vuelve después de la sequía)

**Qué protege.** La capacidad de la unidad de **volver a su régimen después de un evento** —sequía
dentro del rango histórico, fuego, pastoreo intenso puntual—. No protege contra el evento: protege
contra su permanencia.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **Umbral numérico único de irreversibilidad en tierras áridas** | **[SIN FUENTE VERIFICADA — pendiente de consenso científico]** | — | **No existe.** El IPCC declara explícitamente: *"actualmente hay una falta de conocimiento de los límites de adaptación y de la maladaptación potencial a los efectos combinados del cambio climático y la desertificación"* [REPORTADO, SRCCL Cap. 3 §3.6.4, 2019] |
| Definición operativa del piso | `[HIPÓTESIS]`: **la unidad no supera, tras un evento dentro de su rango histórico, el tiempo de recuperación de su propia línea base** | Recuperación al régimen previo en el ciclo propio de la unidad | Construcción del proyecto sobre UNCCD principio LDN 4 + IPCC SRCCL Cap. 3, 2019 |
| Aridez frente a sequía — **frontera que evita la violación falsa** | **Una sequía no es violación.** *"La aridez es un rasgo climático de largo plazo (…). La aridez es distinta de la sequía, que es un evento climático temporal (…). Las sequías no se restringen a las tierras áridas"* | — | IPCC SRCCL Cap. 3, 2019 (definición de sequía de AR5/SYR: *"un periodo de tiempo anormalmente seco lo bastante largo como para causar un serio desequilibrio hidrológico"*) |
| Ciclos que el canon manda respetar | **fuego, inundación, sequía** | — | Cap. 10 §10.4 |
| **Irreversibilidad práctica documentada** — el caso que sí existe | **Pérdida del sistema completo por salinización**: *"llevó a la desaparición del sistema de cultivo del patrimonio agrícola mundial (Ghout)"* — el sistema **no se recuperó** | — | Khezzani & Bouchemal, vía FAO AGRIS, 2018 |
| Persistencia de los oasis *(evidencia de que la resiliencia es la propiedad de referencia)* | — | *"Muchos oasis han persistido durante varios miles de años"* | [REPORTADO, IPCC SRCCL Cap. 3, 2019] |
| Abandono de oasis *(hecho documentado)* | — | *"Muchos oasis han sido abandonados"* por cambios climáticos o hidrológicos | [REPORTADO, IPCC SRCCL Cap. 3, 2019] |
| Proyección de cambio en oasis del sur de Túnez, década de 2050 *(proyección, no umbral)* | — | **+2,7 °C**, **−29 %** de precipitación, **+14 %** de evapotranspiración | [REPORTADO, IPCC SRCCL Cap. 3 §3.7.4, 2019, sobre Ministerio de Agricultura y Recursos Hídricos de Túnez y GIZ, 2007] |
| Demanda agrícola de agua en Arabia Saudí a 2050 *(proyección)* | — | **+5 a +15 %** para mantener la producción de 2011 | [REPORTADO, IPCC SRCCL Cap. 3 §3.7.4, 2019, sobre Chowdhury & Al-Zahrani, 2013] |
| Recarga de acuíferos y oasis *(proceso documentado)* | — | *"En Marruecos, se espera que el descenso de la recarga del acuífero afecte al suministro de agua del oasis de Figuig (…), así como al valle del Draa"* | [REPORTADO, IPCC SRCCL Cap. 3, 2019] |

**Justificación, y aquí el documento convierte una ausencia en doctrina.** No existe el número. Lo que
sí existe son tres cosas verificables, y las tres se usan:

1. **El marco internacional elude el umbral absoluto por diseño.** La LDN es *relativa a la línea base*
   (principio 4): no es un olvido, es una decisión. Copiar un piso absoluto de otra latitud sería
   colonizar la unidad con una vara ajena.
2. **El IPCC declara el vacío en voz propia** [REPORTADO, §3.6.4]. Un estándar que declare un umbral de
   irreversibilidad «científico» estaría inventando lo que la propia ciencia declara no saber.
3. **La irreversibilidad práctica sí tiene un caso documentado:** el sistema Ghout. No es un umbral, es
   un **precedente**: prueba que la categoría existe, aunque no fije dónde empieza.

**La consecuencia formal, que es la aportación doctrinal de esta dimensión.** Con esas tres piezas, el
SDV-E puede escribir algo que ningún otro documento de la biblioteca puede escribir con esta precisión:

> **Regla `[HIPÓTESIS]` — la sequía no viola; la pérdida de resiliencia sí.**
> Un evento seco dentro del rango histórico de la unidad **no constituye violación** del SDV-E: es un
> ciclo natural que el canon manda respetar (Cap. 10 §10.4) y que el IPCC distingue expresamente de la
> aridez. Lo que constituye violación es que la unidad **no regrese a su régimen** después del evento:
> que un ciclo reversible se haya vuelto permanente. El objeto de esta dimensión no es el clima: es
> **la derivada de la recuperación**.

Sin esta regla, el estándar tendría un defecto fatal y evidente: **violaría a todas las unidades áridas
del planeta cada vez que hay una sequía**, que es precisamente el sesgo «verde = sano» que este
documento existe para desactivar.

**Protocolo.** No hay instrumento estándar, y se declara: **no existe métrica estandarizada de
resiliencia operacionalizable** (tiempo de recuperación, capacidad de carga adaptativa, memoria
ecológica) en las fuentes verificadas en esta sesión. El protocolo propuesto `[HIPÓTESIS]` es una
**medición derivada, no un sensor nuevo**: se toma la serie de los sub-indicadores de D1 y se mide el
**tiempo de retorno** al valor previo al evento, comparado con el tiempo de retorno documentado en la
línea base de la propia unidad. El evento se identifica con el registro meteorológico e hidrológico
nacional, no con la memoria de la parte interesada. Frecuencia: por evento, más una revisión de la serie
en cada ciclo de reporte del marco LDN.

**Violación.** Dos hechos concretos:

1. **Violación de resiliencia (graduable):** la unidad **no regresa a su régimen previo** dentro del
   tiempo de recuperación de su propia línea base, tras un evento **dentro de su rango histórico**, con
   serie comparable antes y después. El déficit se expresa, por sustitución (b) de §5.2, como
   `(tiempo_de_retorno_base − tiempo_de_retorno_observado) / tiempo_de_retorno_base`.
2. **Violación terminal (veto V3, canal B):** **estado `CONSUMADO_IRREVERSIBLE`** cuando el sistema
   productivo o ecológico de la unidad se ha perdido por salinización acoplada al descenso freático
   (precedente Ghout). No es un número: es un estado, y §8 lo hace no retornable por acumulación de
   crédito.

---

### Dimensión D5: Pastoreo sostenible (la herbivoría es un ciclo; el uso excesivo es una violación)

**Qué protege.** El equilibrio entre la producción de forraje de la unidad y lo que se le extrae. No
protege contra el pastoreo —que es un proceso natural y, en muchas tierras secas, **el régimen que
mantuvo el ecosistema**—: protege contra la **tasa de uso** que mata la planta y con ella la base
forrajera.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **Factor de uso apropiado del forraje anual («take half and leave half»)** | **≤ 50 %** de la producción anual de forraje — **regla publicada de gestión ganadera**, no constante ecológica: la fuente la llama *"un punto de partida común o regla"* y el factor concreto de cada unidad es **POLÍTICA votable** dentro del rango ajustable por sitio (advertencia 1, más abajo) | **Régimen de herbivoría propio de la unidad** — `[SIN FUENTE VERIFICADA]` como número: **el óptimo no es cero pastoreo**, y presentarlo como cero sería el sesgo que este documento prohíbe | USDA NRCS, *Utilization and Harvest Efficiency*, Technical Note Plant Materials n.º 39 |
| Qué cuenta dentro de ese 50 % | Incluye **el forraje consumido y el daño por pisoteo, reposo y otros factores no ganaderos** | — | USDA NRCS, Technical Note n.º 39 |
| Componente no-ganadero de la pérdida | — | Hasta **~25 %** de la producción anual se pierde por insectos, fauna silvestre y pisoteo | USDA NRCS, Technical Note n.º 39 |
| Demanda de forraje por unidad animal (AU) | — | **3,0 % del peso corporal/día** en forraje secado al aire (**30 lb/día** para una vaca de 1 000 lb) | USDA NRCS, Technical Note n.º 39 |
| Unidad animal-mes (AUM) | — | **912,5 lb** (≈ **414 kg**) de forraje seco | USDA NRCS, Technical Note n.º 39 |
| **Ajuste de la capacidad de carga por distancia al agua** | — | **100 %** a 2 640 ft → **90 %** a 5 280 ft → **70 %** a 7 920 ft → **50 %** a 10 560 ft | USDA NRCS, Technical Note n.º 39 |
| **Ajuste de la capacidad de carga por pendiente** | — | **100 %** a 0-15 % → **70 %** a 15-30 % → **40 %** a 31-60 % → **0 %** a > 60 % | USDA NRCS, Technical Note n.º 39 |
| Manual nacional de referencia | — | *National Range and Pasture Handbook*, Parte 645 (criterios de utilización sostenible) | USDA NRCS, vía Rangelands Gateway |

**Justificación, en la lectura textual de la fuente.** El 50 % no es una convención: es un umbral de
**uso** con mecanismo biológico declarado. *"Las plantas tienen una tolerancia al pastoreo, pero si la
remoción de herbaje excede un punto crítico, la mayoría de las plantas perderán vigor, producirán menos
y, si la remoción excesiva continúa, eventualmente morirán. El uso apropiado es el punto aproximado de
cosecha de forraje que no llevará a deterioro del pastizal ni a una disminución del rendimiento
animal. (…) Un punto de partida común o regla para planificar un nivel apropiado de utilización es
«tomar la mitad y dejar la mitad», o 50 por ciento de utilización de la producción anual de forraje"*
[REPORTADO, USDA NRCS]. Y su alcance es más amplio de lo que su nombre sugiere: *"Esta utilización
incluye el forraje realmente consumido por el animal, pero también el daño a las plantas causado por el
pisoteo, el reposo y otros factores no ganaderos"* [REPORTADO]. **Eso es exactamente «cuidado ≠
extracción estética»** (Cap. 16.5 §16.5.14): lo que el animal pisotea cuenta como uso, aunque no se lo
haya comido.

**Las dos advertencias obligatorias, y la segunda es la más importante del documento.**

1. **El 50 % es un factor de uso, no un estado.** La propia NRCS lo llama *"un punto de partida común o
   regla"*: es ajustable por sitio, y no es una ley universal. Este documento **no lo eleva a constante
   ecológica**.
2. **Que un pastizal esté al 60 % de uso un año NO lo convierte en ecosistema violado.** Sería el error
   simétrico al «verde = sano»: convertir un factor de gestión en una foto de degradación. El propio
   marco LDN exige **tendencia y línea base**. La violación de esta dimensión es el **uso excesivo
   sostenido con pérdida documentada de la base forrajera**, no un año por encima del factor.

**Protocolo.** Medición de la producción anual de forraje por **jaulas de exclusión y corte** (método de
utilización del NRCS), contrastada con la carga animal efectiva (AU por unidad de superficie y por
tiempo), con los factores de ajuste por **distancia al agua** y por **pendiente** de la tabla. La
estimación de carga sin los ajustes es inválida: la fuente los publica como parte del método, no como
refinamiento opcional. Frecuencia: **anual, al final de la estación de crecimiento** (la producción
anual es la unidad de la regla). Quién reporta: la parte que pastorea **declara su carga** —es la
actividad que se mide— y la comunidad de custodia verifica la producción de forraje; el tercero
científico interviene cuando hay disputa.

**Violación.** Dos hechos concretos:

1. **Utilización superior al factor declarado para la unidad, sostenida en el tiempo y con pérdida
   documentada de la base forrajera o de la composición de especies** (mortalidad de plantas,
   disminución de la producción, cambio de composición), informada por dos campañas comparables. El
   factor concreto de cada unidad es **POLÍTICA votable** dentro del rango que la fuente permite
   ajustar; el 50 % es el punto de partida declarado, no el dogma.
2. **Carga animal declarada sin los ajustes de distancia al agua y pendiente**, en una unidad donde
   alguno de los dos aplica. No es violación del ecosistema: es **condición de invalidez del cómputo**,
   porque la fuente publica esos factores como parte del método.

---

### Dimensión D6: Humedales áridos y oasis (el agua que sí aparece)

**Qué protege.** El humedal árido y el oasis como **sujeto**: su extensión, su fuente de agua y su
continuidad. Es la dimensión donde la presión humana se concentra, porque es el único punto de una
tierra seca donde el agua está disponible sin tecnología.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| **Extensión del humedal u oasis de la unidad** | `[HIPÓTESIS]` **ninguna pérdida neta de extensión** respecto de la línea base de la unidad — **y la línea base puede no existir** (§6, `[SIN DATO]`) | Estabilidad de la extensión en la ventana de la unidad | Construcción del proyecto sobre UNCCD principio LDN 4 y el marco Ramsar |
| **Extensión y número de humedales áridos a escala global** | — **No hay piso**: el propio marco reconoce el vacío en su escala, no en la de la unidad. Los humedales de zona árida están *"generalmente mal cartografiados"* | — | Manual Ramsar, Vol. 17 (*Ramsar Handbook*, humedales de zonas áridas) — **URL bloqueada (403)**; el vacío lo declara el propio manual |
| **Fuente de agua que lo sostiene** | `[HIPÓTESIS]` **ninguna pérdida de la surgencia o de la recarga declarada** que lo alimenta | Recarga sostenida | IPCC SRCCL Cap. 3, 2019 (caso Figuig y valle del Draa) |
| Definición de oasis — **criterio de delimitación, no umbral** | — | — | *"Áreas aisladas con suministro de agua fiable procedente de lagos y manantiales, localizadas en zonas hiperáridas y áridas"* [REPORTADO, IPCC SRCCL Cap. 3, 2019] |
| **Extensión y número de humedales áridos a escala global** | **[SIN FUENTE VERIFICADA]** — el propio marco reconoce el vacío: los humedales de zona árida están *"generalmente mal cartografiados"* | — | Manual Ramsar, Vol. 17 (*Ramsar Handbook*, humedales de zonas áridas) — **URL bloqueada (403)**; el vacío lo declara el propio manual |
| Persistencia histórica *(evidencia de que el sujeto es antiguo y resiliente)* | — | *"Muchos oasis han persistido durante varios miles de años"* | [REPORTADO, IPCC SRCCL Cap. 3, 2019] |
| Abandono histórico *(hecho documentado)* | — | *"Muchos oasis han sido abandonados"* por cambios climáticos o hidrológicos | [REPORTADO, IPCC SRCCL Cap. 3, 2019] |
| Proyección al 2050 en el sur de Túnez *(proyección)* | — | **+2,7 °C**, **−29 %** precipitación, **+14 %** evapotranspiración | [REPORTADO, IPCC SRCCL Cap. 3 §3.7.4, 2019] |
| Demanda agrícola de agua en Arabia Saudí a 2050 *(proyección)* | — | **+5 a +15 %** para mantener la producción de 2011 | [REPORTADO, IPCC SRCCL Cap. 3 §3.7.4, 2019] |
| Caudal ecológico o asignación de agua para un humedal árido | **[SIN FUENTE VERIFICADA]** en esta sesión: la fuente pertinente (Manual Ramsar Vol. 17) está bloqueada. Pertenece al documento 11 (Humedales) y al 12 (Ríos y cuencas) | — | — |

**Justificación.** Los oasis son sistemas **resilientes y antiguos**, no restos degradados: el propio
IPCC documenta que muchos han persistido **varios miles de años**, y que su abandono —cuando ocurre—
responde a cambios climáticos o hidrológicos [REPORTADO, 2019]. Eso refuerza la tesis del documento
desde el lado contrario al habitual: **lo que hay que proteger en un oasis no es su verde, es su
fuente**. La dependencia es explícita en la fuente: *"en Marruecos, se espera que el descenso de la
recarga del acuífero afecte al suministro de agua del oasis de Figuig (…), así como al valle del
Draa"* [REPORTADO, 2019]. Y la presión que viene está cuantificada como proyección, no como norma: se
declara en la columna del Óptimo, y **no se convierte en piso** —hacerlo sería el error que la Regla 1
prohíbe—.

**Frontera con los documentos 11 y 12.** Esta dimensión **no** mide hidroperiodo, ni turba, ni el
régimen de inundación de un humedal (documento 11), y **no** fija caudal ecológico (documento 12). Mide
lo específico del humedal árido: **que exista, que no pierda extensión y que su fuente de agua no
caiga**. La cifra de caudal ecológico para humedales áridos queda declarada como
`[SIN FUENTE VERIFICADA]` y **no se inventa aquí**.

**Protocolo.** Delimitación del cuerpo de agua y de la extensión del oasis por teledetección, con
validación de campo; nivel piezométrico de la surgencia o del acuífero asociado (misma serie que D2);
registro de la superficie efectivamente cultivada o inundada. Frecuencia: **anual** para extensión;
**la de D2** para el nivel. Quién reporta: servicio hidrológico y autoridad del sitio (si está
designado); comunidad de custodia para el uso efectivo. Advertencia declarada: los humedales áridos
están *"generalmente mal cartografiados"* según el propio manual de referencia, de modo que la línea
base de esta dimensión **puede no existir** y su resultado más frecuente será `[SIN DATO]`.

**Violación.** Dos hechos concretos:

1. **Pérdida neta de extensión del humedal u oasis** respecto de su línea base, informada por dos
   delimitaciones comparables.
2. **Descenso de la fuente de agua por debajo de la surgencia o de la recarga declarada** que sostiene
   al humedal. Cuando esto ocurre de forma sostenida, se activa el **veto V4**: la unidad pierde su
   humedal árido y ninguna ponderación lo compensa.

---

### 4.2 La dimensión binaria sin peso: D7 · Zona Libre de las tierras secas (lo que no se mide)

**Precedente canónico, citado literalmente:** las dimensiones **VIII (Derecho a la Rehabilitación)** y
**IX (Derecho a la Opacidad Vital)** del SDV-H *"se registran cualitativamente y mediante umbrales
binarios (presencia/ausencia del derecho), **no mediante pesos en la fórmula** — medir la rehabilitación
o la opacidad con la misma vara cuantitativa que el agua o la vivienda las destruiría"* (Cap. 8 §8.11).
El canon del Reino Natural lo reafirma: *"parte del valor del humedal es inefable (Cap. 7 §7.9). Los
sensores miden salud (agua, cobertura, biodiversidad indicadora); jamás «milagros». **Medir todo sería
la forma técnica de dejar de escucharlo**"* (Cap. 16.5 §16.5.14).

**Cómo se materializa en tierra seca.** D7 no tiene parámetro numérico, no tiene peso (**0,00**), no
entra en el numerador de ninguna fórmula y **no se puede canjear contra ninguna otra dimensión**. Se
registra como derecho binario auditable: **presencia o ausencia de Zona Libre declarada y respetada** en
la unidad. Su violación **se documenta (T13) y no se cuantifica**. La mecánica general —los cuatro
estados de la matriz `ZL`, las siete puertas de entrada, la prueba de inefabilidad y el inventario
negativo— pertenece al [documento 04](./04_Zona_Libre_del_Reino_Natural.md) y **no se repite aquí**.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| Existencia de una Zona Libre en la unidad | **Presencia** (binaria): la unidad declara su Zona Libre y su catálogo | Presencia | Cap. 7 §7.9 · Cap. 16.5 §16.5.14 · precedente Cap. 8 §8.11 |
| Peso en la fórmula del SDV-E | **0,00** — no pondera, no entra en el numerador | 0,00 | Cap. 8 §8.11 (precedente VIII y IX) |
| Cuantificación de su violación | **Ninguna**: se registra con T13 (la contabilidad nunca se borra) y no se puntúa | — | Cap. 8 §8.11 |
| **Regla específica de tierra seca** `[HIPÓTESIS]` | **Regla, no piso numérico**: la Zona Libre no puede absorber una deuda de medición del marco LDN. Los tres sub-indicadores de D1 los computa un tercero con **datos abiertos**, de modo que su coste de cómputo para la unidad es nulo o marginal; lo que sí puede costar es la **verificación de campo** del suelo desnudo (§4.1 D3) y la **capa de COS de la propia unidad** | — | Construcción de este documento sobre el [documento 04](./04_Zona_Libre_del_Reino_Natural.md) §10.3 (prueba de inefabilidad), Copernicus CLMS/JRC, 2025 y FAO GSOCmap |

**Qué protege, en concreto, en una tierra seca.** Tres cosas que la instrumentación no alcanza **por
principio**, no por presupuesto:

1. **El interior del acuífero.** El piezómetro mide un nivel y una conductividad; **no mide el agua
   fósil ni su historia**. El canon fija el límite: *"nosotros registramos la interacción, no la vida
   interna del ecosistema"* (Cap. 16.5 §16.5.14). Un acuífero no es un depósito: es un archivo, y el
   archivo no se mide con una sonda de nivel.
2. **El desierto como sujeto, no como vacío.** La forma más común de negar dignidad ecosistémica a una
   tierra seca es llamarla **terreno baldío**, **tierra no productiva** o **superficie disponible**. El
   IPCC da el respaldo externo —*"los desiertos son ecosistemas valiosos"* [REPORTADO, 2019]— y D7 lo
   convierte en regla: **la unidad árida no está «en espera de uso»**, y su valor no se mide por lo que
   produciría si se la convirtiera en otra cosa.
3. **El territorio no instrumentado.** En tierras secas las distancias son enormes y las redes de
   observación escasas. Aquí D7 se cruza con INV2-EDU (*"la duda sin evidencia no castiga"*) y produce
   la regla de doble filo que este documento hace explícita: **la ausencia de monitoreo no imputa
   violación al ecosistema — y tampoco autoriza la intervención.** Sin dato no hay castigo; sin dato no
   hay permiso.

**El riesgo propio de esta Zona Libre, y es el más agudo de toda la biblioteca.** En tierra seca medir
es **caro** (distancias, acceso, pocos pozos) y el catálogo de lo no medido es la opción **barata**, no
la respetuosa. Es la inversión exacta del caso de la criosfera, donde la inefabilidad era evidente y la
medición imposible por física. Por eso este documento añade una puerta a la prueba de inefabilidad del
documento 04, aplicada al caso árido:

> **Puerta adicional `[HIPÓTESIS]` — coste de tercero.** Si un parámetro del piso puede ser computado
> por un tercero con datos abiertos y **a coste nulo o marginal para la unidad** —es el caso de los tres
> sub-indicadores de la LDN (Copernicus CLMS/JRC) y de la cobertura de superficie—, **no puede entrar al
> catálogo de la Zona Libre**: es medición pendiente, no inefabilidad. La Zona Libre no puede invocarse
> para no mirar lo que ya está mirado desde fuera.

Y el límite contrario, que el canon ya escribió: *"Cuidado ≠ extracción estética: jardín podado para la
foto no es cuidado; se registra lo que regenera, no lo que adorna"* (Cap. 16.5 §16.5.14). **La Zona
Libre no es un refugio para lo incómodo de medir.**

**Frontera LEY / POLÍTICA, explícita.**

- **LEY (no se vota).** Que exista una Zona Libre en la unidad y que **no se pondere**: ponderarla la
  volvería canjeable contra el piso, y *"el suelo antes que el saldo"* lo prohíbe. Su existencia, su peso
  0,00 y su registro por T13 **no son votables**.
- **POLÍTICA (se vota).** **Qué entra al catálogo** de cada unidad concreta —y con ello qué deja de
  medirse— es decisión deliberativa: se vota con la categoría `critical` (quórum 60 %, consenso 75 %,
  T13, anti-flip-flop 14 días, `CHECK` en BD), igual que la plenitud aspiracional. El catálogo **es
  votable**; el piso que protege, no.

---

## 5. Fórmula de violación, pesos y umbrales

Este documento **no fija la fórmula del SDV-E** —es el [documento 07](./07_Formula_de_violacion_y_pesos.md)—
pero las tierras secas **fuerzan cuatro decisiones** que ningún otro ecosistema fuerza, y las cuatro se
justifican aquí.

### 5.1 Dos canales: el índice gradúa, el veto declara

Las tierras secas tienen **eventos terminales** —perder el sistema por salinización, perder el humedal,
cruzar el umbral de irreversibilidad práctica— y tienen, sobre todo, **una regla booleana ya publicada**
que hace el trabajo del canal B sin que el proyecto tenga que inventarla: la regla «uno fuera, todos
fuera» de la LDN. Promediar un sub-indicador negativo en un índice ponderado sería diluir exactamente
lo que el marco internacional prohíbe diluir.

| Canal | Qué contiene | Cómo se computa | Puede compensarse |
|---|---|---|---|
| **A — Índice ponderado continuo** | El déficit graduable de D1-D6 | `Violación = Σ(déficit_i × Peso_i) × Duración × Intensidad`, con déficit normalizado (§5.2) | Sí, entre dimensiones del canal A, con los límites de §9 |
| **B — Vetos binarios** | Hechos terminales: **V1** pérdida declarada por la regla 1OAO cuando **cualquiera** de los tres sub-indicadores de D1 —o el cómputo que los integra— muestra cambio negativo significativo · **V2** pérdida del sistema por salinización acoplada (D2/D4, precedente Ghout) · **V3** irreversibilidad práctica: la unidad no regresa tras un evento dentro de su rango histórico (D4) · **V4** pérdida del humedal árido u oasis por caída de su fuente de agua (D6) | **Estado**, no número: `CONSUMADO_IRREVERSIBLE` | **No. Nunca.** El canal B no entra en el promedio: lo anula |

**Fundamento y coherencia con la familia.** El canal B aplica dos precedentes ya establecidos: (i) el
`∞` de los SDV-A y SDV-S **no es una cifra, es una consecuencia jurídica** —prohibición de mercado en el
SDV-A (Cap. 9 §9.8), interrupción total del sistema en el SDV-S (Cap. 9.5 §9.5.10)—, y un contrato que
guarde `inf` en una columna numérica no es ejecutable, mientras que uno que pase a `estado = PROHIBIDO`
sí; (ii) las dimensiones VIII y IX del SDV-H, que operan **por presencia/ausencia y sin peso**
(Cap. 8 §8.11). `[HIPÓTESIS]` — propuesta de este documento, no ratificada; su especificación completa
pertenece al [documento 08](./08_INV2-E_invariante.md).

**Nota de honestidad sobre V1.** El veto V1 **no es una invención del proyecto**: es la regla 1OAO del
principio 16 de la UNCCD transcrita como disparador. Es el único veto de esta biblioteca cuya forma está
publicada por un organismo internacional antes de que el proyecto la adoptara.

### 5.2 La línea base como denominador: la trampa de la captura de línea base

La versión **normalizada** del déficit es la coherente con el motor del proyecto —`déficit =
(requerido − actual) / requerido`, tal como calcula `maxocontracts/blocks/sdv_validator.py`
(`relative = deficit / required`)— y este documento la adopta como marco. Pero en tierras secas el
**requerido** no es una norma: es **la línea base de la propia unidad** (LDN, principio 4). Eso
introduce un riesgo nuevo en la familia, y es un riesgo **de gobernanza, no de aritmética**:

> **La captura de línea base.** Si la línea base se fija con la primera medición disponible, **quien
> degrada primero y mide después obtiene un piso más bajo**. El principio 4 de la LDN, que dice que el
> objetivo *es* la línea base, es correcto como marco de planificación y **peligroso como piso
> contable** si la fecha de la línea base queda a discreción de la parte interesada.

**Reglas duras que este documento propone `[HIPÓTESIS]`:**

1. **La línea base se declara antes de la intervención que se juzga**, y **no se re-negocia después de
   medir**. Es la misma regla que el [documento 14](./14_Ecosistemas_Suelos_vivos.md) §4 (D2) fija para
   el carbono orgánico del suelo: la línea base no se re-negocia después de medir.
2. **La línea base la certifica un tercero y lleva fecha.** Una línea base declarada por la parte que
   opera la extracción no es línea base: es declaración de parte.
3. **Una unidad ya degradada antes de su primera medición no puede declararse en coherencia.** Su estado
   es `DEGRADADO_HEREDADO` (§8), no `SANO`: el estándar mide **tendencia**, y una tendencia plana sobre
   un estado degradado no es salud, es **daño estabilizado**. Este estado es una aportación de este
   documento y responde a una realidad que ningún otro ecosistema de la familia enfrenta con esta
   crudeza: **en tierras secas, la mayoría de las unidades ya están en algún punto del espectro de
   degradación cuando alguien empieza a medirlas.**
4. **El déficit no puede ser negativo por verdor.** Un aumento de cobertura vegetal **no genera
   crédito** por sí mismo: si el aumento proviene de una especie invasora, de una plantación exótica o
   de riego que saliniza, el indicador sube mientras la unidad se degrada. Regla `[HIPÓTESIS]`: **un
   déficit negativo (ganancia) solo se computa si es consistente con los otros dos sub-indicadores de
   D1**; si un solo indicador muestra ganancia y otro pérdida, se aplica la regla 1OAO y **no hay
   ganancia neta**. Es la traducción aritmética del pilar 5 y del sesgo «verde = sano».
5. **Sustituciones admisibles** cuando el piso es cero o la línea base no es un número:

| Sustitución | Forma | Se aplica a | Por qué es legítima |
|---|---|---|---|
| **(a) Déficit temporal (TA)** | `ciclos_sobre_el_piso / ventana_de_la_serie` | D2 (descenso sostenido) | Convierte un piso-cero en tiempo consumido; el denominador es **la serie de la propia unidad**, no el ejercicio contable |
| **(b) Déficit de referencia propia** | `(base_de_la_unidad − actual) / base_de_la_unidad` | D1, D4, D6 | El denominador es un dato **del sujeto**, tomado antes de la intervención que se juzga |
| **(c) Binario puro** | Presencia / ausencia | Los cuatro vetos (canal B), D3 y D7 | Hay hechos que no gradúan; graduarlos los diluye |

**Regla dura que se propone al documento 07:** cuando el piso de una dimensión sea la línea base propia
o sea cero, **está prohibido** rellenar el denominador con una constante de conveniencia (un 1, un 100,
un valor «razonable»). Se usa (a), (b) o (c), y se declara cuál.

### 5.3 Pesos propuestos (propuesta no ratificada)

| Dimensión | Peso propuesto | Naturaleza | Fuente del peso |
|---|---|---|---|
| **D1** Neutralidad en la degradación de la tierra | **0,30** | continua + **veto V1** (regla 1OAO) | `[HIPÓTESIS]`; la regla del veto es UNCCD, principio 16 |
| **D2** Agua subterránea y acuíferos | **0,25** | continua (tendencia) + **veto V2** | `[HIPÓTESIS]` |
| **D4** Resiliencia y umbral de irreversibilidad | **0,15** | continua (tiempo de retorno) + **veto V3** | `[HIPÓTESIS]` |
| **D3** Costras biológicas y criptobiótica | **0,10** | **binaria** (presencia/ausencia) dentro del canal A, con deuda de medición declarada | `[HIPÓTESIS]`; el umbral está `[SIN FUENTE VERIFICADA]` |
| **D5** Pastoreo sostenible | **0,10** | continua (factor de uso) | `[HIPÓTESIS]`; el factor es USDA NRCS |
| **D6** Humedales áridos y oasis | **0,10** | continua (extensión) + **veto V4** | `[HIPÓTESIS]` |
| **D7** Zona Libre de las tierras secas | **0,00** | **binaria, sin peso** (precedente Cap. 8 §8.11) | Cap. 8 §8.11 · Cap. 16.5 §16.5.14 |
| **Total** | **1,00** | | |

**Los pesos son una propuesta, no una medición.** No existe en la literatura una ponderación publicada
de estos componentes, y este documento **no la finge**: son `[HIPÓTESIS]` del proyecto, pendientes del
documento 07 y, en último término, del Parlamento. Lo que **no** es hipótesis es su estructura: (i)
suman 1,00; (ii) D7 pesa exactamente 0,00 y no entra en el numerador; (iii) **D1 y D2 concentran el
55 %**, porque son las dos dimensiones que gobiernan a las demás: sin proceso de tierra no hay pastizal
que pastorear ni oasis que sostener, y **sin acuífero no hay nada de lo demás en una tierra seca**.
(iv) **D3 no pesa cero a pesar de no tener umbral**, y esa decisión tiene su propia justificación: darle
0,00 equivaldría a declararla inefable, y no lo es —es **medición pendiente**, con instrumento
disponible y una fuente identificada y bloqueada—. El peso de 0,10 es deliberadamente bajo porque **no
se puede ponderar con fuerza lo que no se puede medir**, pero es **deliberadamente distinto de cero**
para que la Zona Libre no absorba la deuda.

**Nota de concordancia obligatoria con el [documento 01](./01_Doctrina_SDV-E.md) §5.3.** La doctrina de la
biblioteca asigna **peso 0** a las dimensiones binarias auditables —ciclos naturales, riberas, Zona
Libre—. **D3 no puede recibir 0,00**, y conviene decir por qué para que no se lea como una excepción
arbitraria: lo que la doctrina lleva a peso cero es **lo inconmensurable**, es decir aquello para lo que
**no existe instrumento**; aquí existe instrumento (transecto, fotografía escalada, T13) y lo que falta
es el **umbral publicado**. Consecuencia de forma, y es la que este documento propone: **la
VERIFICACIÓN de D3 entra sin peso**, como hecho binario —presencia o pérdida de costra biológica—,
mientras que el **déficit graduable** —la cobertura respecto de la referencia— es lo único que lleva
peso (0,10), y solo mientras su umbral siga declarado como vacío. Si una revisión futura concluye que la
dimensión es inefable, su peso pasa a 0,00 y entra como derecho binario, como las otras; si se publica el
umbral, deja de ser `[SIN FUENTE VERIFICADA]` y se revisa su peso. **Ninguna de las dos cosas es votable
por mayoría: la primera la decide la prueba de inefabilidad del documento 04 §10.3, y la segunda, la
aparición de la fuente.** `[HIPÓTESIS]` —propuesta no ratificada, pendiente del documento 07.

### 5.4 Escala de interpretación (propuesta, con referencia en lugar de invención)

| Violación (v) | Estado | Lectura para la tierra seca |
|---|---|---|
| `v = 0` | Coherencia | La unidad conserva su régimen **y su línea base está certificada** |
| `0 < v ≤ 0,10` | Alerta temprana | La ventana de la serie empieza a consumirse |
| `0,10 < v ≤ 0,30` | Violación leve | Degradación sostenida; la actividad causante debe documentarse |
| `0,30 < v ≤ 0,60` | Violación severa | El régimen está comprometido; INV2-E bloquea (documento 08) |
| `v > 0,60` | Violación crítica | Régimen perdido dentro del horizonte de la unidad |
| Cualquier veto V1-V4 activo | **`CONSUMADO_IRREVERSIBLE`** | **No es un número: es un estado.** El índice no lo promedia |
| Línea base no certificada o posterior a la intervención | **`DEGRADADO_HEREDADO`** | La unidad no puede declararse en coherencia; **tampoco se le imputa violación** (§5.2) |
| Sin dato en una o más dimensiones | **`[SIN DATO]`** | INV2-EDU: la duda sin evidencia no castiga — **y la ley tampoco se negocia por ausencia de dato**: no hay coherencia |

Las bandas se proponen por coherencia con las del ISE (`≥ 85` Mejorando · `70-84` Estable · `50-69`
Declinando · `< 50` Crítico, `docs/architecture/metricas_detalle_kpis_oraculos_dinamicos.md` IN-01) y
**no tienen fuente publicada** para el SDV-E: son `[HIPÓTESIS]` pendientes del documento 07.

### 5.5 Unidad de duración y el criterio verificable de no colonización del TA

**El problema, en una frase.** El brief de esta biblioteca registra un hueco abierto: *"No hay forma de
verificar que la contabilidad NO colonizó el TA: no hay test, ni invariante, ni umbral."* El
[documento 16](./16_Ecosistemas_Montanas_y_criosfera.md) §5.3 propuso un criterio general —ningún
denominador puede provenir del calendario del observador— y un test de invariancia al periodo contable.
**Las tierras secas añaden un segundo criterio, más duro y específico, porque aquí el tiempo del sujeto
es literalmente fósil.**

> **Criterio propuesto `[HIPÓTESIS]` — No colonización del TA en tierras secas (el criterio de la
> recarga).**
> Un cálculo del SDV-E sobre una unidad de tierra seca **no coloniza el TA** si y solo si **ningún
> denominador de su cálculo es más corto que el tiempo de recarga del recurso que ese cálculo declara
> sostenible**. Todo balance de extracción de agua, de carbono del suelo o de uso de forraje debe
> declarar, junto al numerador, **la escala temporal del proceso que repone lo consumido**; si el
> resultado cambia al cambiar el periodo contable, la fórmula mide al contador, no al sujeto.

**Por qué este criterio es más fuerte que el general, y por qué es verificable.** En un acuífero árido,
la recarga se mide en **miles de años** y la extracción en **décadas**. Un cálculo que declare
«sostenible» una extracción porque el ejercicio anual cierra en equilibrio está **usando el calendario
del observador como denominador de un proceso que dura milenios**: es la colonización del TA en su forma
más literal, y es detectable sin ambigüedad, porque la asimetría de escalas es de dos o tres órdenes de
magnitud. Propuesta de test `[HIPÓTESIS]`: `test_sdv_e_no_coloniza_ta_aridas`, que recalcula el balance
de D2 con dos ventanas contables distintas y exige invariancia **y** que la ventana declarada no sea
menor que la escala de recarga declarada. Pertenece a los documentos 03 y 07; aquí se aporta el
criterio y su caso de prueba.

**Unidad de duración, y aquí el documento se niega a inventar un número.** La unidad de duración de la
violación debe ser **la ventana que el método de tercero exige para declarar un cambio significativo**
en los sub-indicadores de la LDN. Este documento **no verificó la longitud de esa ventana** en la sesión
de esta rama (la guía GPG v2 describe severidad y nivel de confianza, no el número de años), y por tanto
**no la escribe**. Lo que sí fija, y es operativo:

- **No se declara violación con una sola observación.** Mínimo: **dos observaciones comparables** en el
  tiempo (mismo método, mismo punto, misma fecha estacional).
- **No se declara coherencia sin la ventana completa** que el método de tercero requiera. Sin ella, el
  resultado es `[SIN DATO]`.
- **Prohibido usar el ejercicio fiscal como denominador** de cualquier dimensión de este documento.

### 5.6 Ejemplo aplicado, con el único caso documentado de este documento

Unidad hipotética construida **exactamente** sobre los datos verificados del oasis del Souf (Sahara
argelino; estudio local, 65 puntos, 2010-2015) y su acuífero. No es un ejemplo inventado: es el único
caso de tierra seca con números de campo en las fuentes de esta rama. **Sus límites se declaran: es un
caso, no un estándar.**

| Dimensión | Requerido | Observado (verificado) | Déficit (sustitución) | Peso | Aporte |
|---|---|---|---|---|---|
| **D1** | Sin cambio negativo en ninguno de los 3 sub-indicadores | **No hay cómputo de los 3 sub-indicadores para esta unidad en las fuentes** | `[SIN DATO]` | 0,30 | `[SIN DATO]` |
| **D2** | Ningún descenso sostenido del nivel freático | Descenso **0,29 (2011) → 2,37 (2015) m/año** (×8 en cuatro años); **más del 77 %** del área ya por debajo de los 2 m; **18,2 m** de descenso absoluto en Ghamra (2015); **R > 0,99** con la salinidad | Tendencia negativa sostenida en una serie de 5 años → sustitución **(c) binaria**: `v = 1` (el piso-cero no admite déficit graduado) | 0,25 | **0,25** |
| **D3** | Sin pérdida de costra biológica | Sin dato. **Y es la carencia más grave del caso**: una unidad hiperárida es donde la costra biológica importa más y donde menos se mide | `[SIN DATO]` | 0,10 | `[SIN DATO]` |
| **D4** | Regreso al régimen previo tras el evento | **El sistema de cultivo Ghout no se recuperó**: *"llevó a la desaparición del sistema de cultivo del patrimonio agrícola mundial"* | **Veto V3** (y V2 por salinización acoplada) | 0,15 | **Estado, no número** |
| **D5** | Uso ≤ factor declarado | Sin serie de producción de forraje de la unidad | `[SIN DATO]` | 0,10 | `[SIN DATO]` |
| **D6** | Sin pérdida neta de extensión del oasis | El oasis existe y su acuífero desciende; el abandono de oasis está documentado como fenómeno, no para esta unidad | `[SIN DATO]` | 0,10 | `[SIN DATO]` |
| **D7** | Zona Libre declarada | No declarada (unidad medida) | Binaria, **sin peso** | 0,00 | Registro T13 |

**Lectura honesta del ejemplo, que es lo más valioso que produce.** (i) De las seis dimensiones con
peso, **solo una es computable** con los datos verificados, y su aporte es **0,25** por sustitución
binaria: el piso-cero de D2 no admite un déficit graduado, y fingir un número sería inventar precisión.
(ii) **El canal B está activo**: la desaparición documentada del sistema Ghout es un estado
`CONSUMADO_IRREVERSIBLE`, y ninguna combinación de déficits del canal A cambia ese hecho. (iii) Las
cuatro dimensiones `[SIN DATO]` **no se rellenan con cero ni con uno**: INV2-EDU impide imputar
violación sin evidencia, y la ley impide declarar coherencia sin dato. (iv) **Este ejemplo no demuestra
que el SDV-E funcione; demuestra exactamente dónde le falta dato**, que es lo que un estándar honesto
debe exhibir en su propio ejemplo. Y el hueco más grande del caso no es el agua —que sí se midió— sino
**la costra biológica, que no se midió en absoluto**.

---

## 6. Protocolo de medición (sensores, frecuencias, quién reporta)

**Asimetría de partida, declarada antes de la tabla.** El SDV-E es el único estándar de la familia cuyo
sujeto no puede reportar nada (documento 09 §6). En tierras secas la asimetría tiene una forma
específica que conviene decir sin adornos: **el proyecto no tiene ni un solo instrumento.** Búsqueda en
`app/`: **cero sensores, cero ingestores, cero consumo de datos satelitales, cero referencias a
Copernicus, UNCCD, AQUASTAT o WRI**; y en todo `docs/architecture/` **cero menciones de desertificación,
tierras áridas o UNCCD**. [VERIFICADO: búsqueda directa de patrones sobre el árbol de trabajo en esta
sesión: `Copernicus|UNCCD|AQUASTAT|WRI|desertificaci|aridez|tierras áridas|GSOCmap|piezométric|biocrust`
en `app/` no devuelve ninguna referencia real —las únicas coincidencias son subcadenas de identificadores
internos, como `WRITE_TOOLS`—, y las mismas raíces en `docs/architecture/` no devuelven ninguna]. Por
tanto este
protocolo **no describe una infraestructura propia: adopta infraestructura científica de terceros**, y
esa dependencia se declara en lugar de disimularse.

**La buena noticia, y es real: aquí el tercero ya existe y su cómputo es abierto.** A
diferencia de la criosfera —donde cada serie exige un glaciar de referencia con 30 años—, en tierras
secas **los tres sub-indicadores del piso los computa un tercero con datos abiertos** (Copernicus
CLMS/JRC, guía GPG v2 del ODS 15.3.1, 2025). Eso hace que la parte más pesada de este estándar sea
**auditable sin que la unidad pague el cómputo** — y es la razón de la puerta adicional de §4.2.
**Lo que sigue costando, y se dice para no vender una gratuidad que no existe:** la verificación de campo
del «suelo desnudo» (D3), el análisis de laboratorio del COS de la propia unidad, la serie piezométrica y
los transectos **no los cubre ningún tercero abierto**, y su financiación es una pregunta abierta
(§13.16).

| Parámetro | Instrumento / programa | Criterio de validez | Frecuencia | Quién reporta |
|---|---|---|---|---|
| **3 sub-indicadores LDN** (D1) | Copernicus CLMS / JRC — guía GPG v2 del ODS 15.3.1 (2025); teledetección para cobertura y NPP | Cómputo **de tercero** con la guía vigente; severidad y nivel de confianza declarados | La del ciclo de reporte del marco — `[SIN FUENTE VERIFICADA]` en esta sesión: **no se fija un número** | Copernicus / JRC · reporte nacional a la UNCCD |
| **Carbono orgánico del suelo** (D1) | **GSOCmap** (FAO, Global Soil Partnership) como referencia global + análisis de laboratorio en la unidad | Método alineado con los *IPCC 2019 Refinements*; método declarado; línea base certificada **antes** de la intervención | Cada 3-5 años (el COS cambia despacio) `[HIPÓTESIS]`, coherente con el [documento 14](./14_Ecosistemas_Suelos_vivos.md) | Laboratorio independiente; la FAO solo aporta la capa de referencia |
| **Suelo desnudo y erosión hídrica** (D1, D3) | *Interpreting Indicators of Rangeland Health* (USDA NRCS / BLM, TR 1734-6) | Indicador con **clase de desviación respecto de la referencia**, no valor absoluto | Anual en unidades pastoreadas `[HIPÓTESIS]` | Comunidad de custodia con verificación de tercero |
| **Nivel piezométrico y salinidad acoplada** (D2, D6) | Red de pozos de observación; servicio hidrológico nacional | Serie con **≥ 2 observaciones comparables** (mismo pozo, misma fecha estacional, mismo método); CE medida en la misma campaña | **Al menos anual**, en la misma fecha estacional del ciclo de la unidad; continua bajo extracción intensiva | Servicio hidrológico nacional; **no la parte que extrae** |
| **Extracción y uso del agua** (D2) | **FAO AQUASTAT** — metodología de uso del agua | Reporte con la distinción de tipos de extracción de la fuente | Anual | Autoridad del agua; la parte que riega **declara su extracción** |
| **Estrés hídrico** (D2, alerta) | **WRI Aqueduct** | Indicador de **cuenca/año**, no de ecosistema: **disparador de revisión, nunca déficit** | Anual | WRI |
| **Costras biológicas** (D3) | **Ninguno estandarizado.** No existe programa global de monitoreo | Presencia/ausencia con fotografía escalada, fecha y georreferencia (T13) | Anual en unidades pisoteadas; cada 3-5 años en el resto `[HIPÓTESIS]` | **Comunidad testigo**; la fuente del umbral está **bloqueada (403)** y pendiente de apertura humana |
| **Tiempo de recuperación tras evento** (D4) | **Ninguno estandarizado** — `[SIN FUENTE VERIFICADA]` | Medición **derivada** de la serie de D1; el evento se identifica con el registro meteorológico e hidrológico nacional | Por evento + revisión en cada ciclo de reporte | Servicio meteorológico/hidrológico + cómputo de tercero |
| **Producción de forraje y carga animal** (D5) | Jaulas de exclusión y corte (método de utilización del USDA NRCS, Technical Note n.º 39) + *National Range and Pasture Handbook* Parte 645 | Con los **ajustes obligatorios** de distancia al agua y pendiente; sin ellos el cómputo es inválido | Anual, al final de la estación de crecimiento | La parte que pastorea **declara su carga**; la comunidad de custodia mide el forraje |
| **Extensión del humedal u oasis** (D6) | Teledetección + validación de campo; autoridad del sitio si está designado | **Dos delimitaciones comparables**; advertencia declarada: los humedales áridos están *"generalmente mal cartografiados"* | Anual | Autoridad del sitio + comunidad de custodia |
| **Zona Libre** (D7) | **Ninguno.** No se mide | — | — | Se **registra** (T13): declaración y catálogo de la unidad |

**Regla de elegibilidad del dato (contra la discrecionalidad).** Un parámetro entra al cálculo **solo**
si proviene de una fuente que cumple el criterio de su fila. No entra: una campaña de un año sin
comparación, una estimación por modelo sin serie observacional, una clasificación de «suelo desnudo»
sin verificación de campo (D3), una carga animal sin los ajustes de distancia al agua y pendiente (D5),
ni un dato cuyo origen no sea reconstruible. Un dato que el proyecto no puede auditar **no puede
declarar coherencia**. **Coste de la regla, declarado:** la verificación de campo de D3 y el análisis de
laboratorio de COS **no son gratis para la unidad**; lo que es de coste nulo o marginal es el cómputo de
tercero de los tres sub-indicadores de D1 con datos abiertos (§4.2). La regla de elegibilidad no
convierte en gratuita la medición que exige, y §13.16 deja abierta la pregunta de quién la paga.

**Coste declarado y finitud (Cap. 10 §10.7).** El SDV-E de las tierras secas se puede cumplir con
**tres sub-indicadores de tercero, una serie piezométrica, un transecto de costras, jaulas de exclusión
y dos delimitaciones**. No necesita modelar el ciclo del acuífero transfronterizo ni la cadena trófica
del desierto. El mejor precedente externo de que un estándar finito es posible es el propio marco que
este documento adopta: **tres métricas y una regla booleana, sin modelo** (UNCCD, principios 15 y 16).

**El guardián consiente; no mide.** Es canon y conviene repetirlo aquí: *"Ecosistemas (eco-*):
consentimiento otorgado por el guardián oráculo"* (`app/contracts_bp.py`). El guardián de una tierra
seca **no es su instrumento y no es su laboratorio**. Si el guardián tuviera que producir además el dato
de la línea base, el riesgo R4 (partes fantasma) dejaría de ser un riesgo y pasaría a ser el diseño: un
guardián que fija su propia línea base **elije el piso contra el que se le juzga** (§5.2).

**Frecuencia mínima de revisión del estándar.** Coherente con el TA del sujeto y con el documento 40
(Procesos): **no antes de 5 a 10 años** para los pisos de D1-D6 `[HIPÓTESIS]`, porque las variables
lentas de una tierra seca —carbono del suelo, composición de la costra biológica, nivel freático— no
cambian a la velocidad de un ciclo contable, y revisar el piso cada año sería colonizar el tiempo del
sujeto con el del observador. Este documento **no verifica** el ciclo de reporte del marco LDN y por
tanto **no lo usa como número**: queda en §13.

---

## 7. Verificación y auditoría (T13, guardián, comunidad testigo)

**T13 — Transparencia de Cálculo: la contabilidad nunca se borra.** Toda medición, toda declaración de
Zona Libre, toda violación y toda ausencia de dato se registran y son auditables. En tierras secas T13
tiene dos objetos peculiares que este documento hace explícitos:

1. **Se registra la fecha y el certificante de la línea base.** Sin eso, la captura de línea base (§5.2)
   es indetectable.
2. **Se registran las series que no existen**, y se registra **quién no las midió**. La ausencia de una
   serie piezométrica o de un transecto de costras es información sobre la unidad **y sobre su
   gobernanza**, no un vacío administrativo.

**Quién audita, y la asimetría que no se resuelve.** Ningún ecosistema audita a otro (documento 09 §7).
En tierras secas la auditoría viene de **terceros**: Copernicus CLMS/JRC y el reporte nacional para los
sub-indicadores LDN, el servicio hidrológico para el freático, el laboratorio para el COS, la WRI para
el estrés hídrico. Lo que sigue es incómodo y hay que decirlo: **ninguno de esos terceros audita el
cumplimiento del SDV-E** —auditan el estado de la tierra—. La traducción de serie a veredicto la hace el
proyecto, y por tanto **el proyecto es juez y parte en la interpretación**. La única defensa disponible
es la trazabilidad radical: cada veredicto debe poder recalcularse desde la fuente pública, sin acceso
al código del proyecto.

**La ventaja real de las tierras secas, y es grande: el piso es computable por un tercero.** Frente al
glaciar —que necesita una serie de 30 años que solo existe donde alguien la mantiene—, aquí los tres
sub-indicadores del piso **los computa una agencia externa con datos satelitales abiertos**, y la regla
de integración es **booleana**. Es decir: **el veredicto de pérdida de D1 se puede emitir sin
interpretación del proyecto, siempre que se cumplan dos condiciones que hay que decir en la misma
frase**: (i) que el cómputo de tercero **exista** para la unidad y cumpla la ventana del método —hoy
**no existe ninguna integración** con Copernicus ni con el reporte nacional (§12)—, y (ii) que el
proyecto se limite a **transcribir** el resultado del tercero y a aplicar la regla 1OAO, sin reclasificar
«suelo desnudo» ni reinterpretar severidad. **El cómputo es de tercero y eso es lo auditable; la
traducción de serie a veredicto la sigue haciendo el proyecto mientras no exista la integración**, como
este mismo capítulo declara dos párrafos arriba. Es la pieza de auditabilidad más fuerte de toda esta
biblioteca, y este
documento la declara como tal.

**Y la desventaja, igual de grande: la línea base es un acto político.** Es el eje que este documento
añade a la comparativa (§11) y el riesgo de seguridad específico de las tierras secas:

> **Propuesta `[HIPÓTESIS]` — Identidad verificable de una unidad de tierra seca.**
> De los 7 campos obligatorios de identidad de una representación natural (entidad representada,
> territorio, fuentes de datos, límites del mandato, comunidad de custodia, parámetros SDV-E y
> procedimiento de disputa), el campo **«fuentes de datos» se vuelve verificable y se le añade una
> condición temporal**: para constituirse como sujeto, la unidad debe nombrar (i) la línea base
> certificada **con fecha y certificante**, (ii) el cómputo de tercero de los tres sub-indicadores, y
> (iii) la serie piezométrica que la define. **Una línea base posterior a la intervención no
> constituye sujeto: constituye coartada.**

Esto mitiga el riesgo **R4 (partes fantasma)** de una forma distinta a como lo hace el
[documento 16](./16_Ecosistemas_Montanas_y_criosfera.md) §7: allí la serie es difícil de fabricar;
**aquí es fácil de fabricar**, y lo que la vuelve verificable no es su existencia sino **su fecha**. Un
guardián no puede inventar un acuífero, pero sí puede declarar una línea base cómoda. Por eso la
auditoría de esta unidad mira **cuándo** se declaró el piso, no solo cuánto vale.

**Comunidad testigo.** El canon exige que la identidad incluya la **comunidad de custodia**. En tierras
secas la comunidad testigo tiene una función que ningún satélite cubre, y son tres cosas concretas:

1. **Detectar la costra biológica**, que los clasificadores de cobertura confunden con suelo desnudo
   (§4.1 D3) y que ningún programa global monitorea.
2. **Testificar sobre el uso real del territorio** —pozos nuevos, ampliación de la superficie regada,
   cambio de especie, cierre de rutas de pastoreo— que puede tardar años en aparecer en una serie.
3. **Declarar la Zona Libre** de la unidad (§4.2) y su catálogo, con carga de la prueba.

**El límite de la comunidad testigo, dicho sin romanticismo.** La comunidad testigo **no certifica su
propia línea base** (§5.2, regla 2): si lo hiciera, el estándar tendría el mismo problema que evita. Su
papel es **testificar y detectar**, no juzgar. La frontera entre testimonio y certificación es la que
separa este estándar de un sistema de autoevaluación.

**Auditoría de la no colonización del TA.** Es la aportación de §5.5 trasladada a la práctica: cada
fórmula del SDV-E de tierras secas debe pasar (i) el test de invariancia al periodo contable del
documento 16 §5.3 y (ii) el **criterio de la recarga** —ningún denominador más corto que el tiempo de
recarga del recurso que el cálculo declara sostenible—. Si el déficit cambia al cambiar la ventana de
reporte, o si la ventana declarada es más corta que la recarga, **el veredicto es nulo**, no
«ajustado».

---

## 8. Invariante INV2-E: de estándar a contrato ejecutable

**INV2 genérico:** *"Ninguna acción del contrato puede dejar a un participante bajo su SDV"* (Cap. 17).
**INV2-E no existe hoy**: no hay `validate_invariant_sdv_e` en `maxocontracts/core/axioms.py` ni bloque
validador gemelo de `maxocontracts/blocks/sdv_s_validator.py`. [VERIFICADO: lectura directa del
repositorio en esta sesión] El canon lo convoca con la frase que abre esta biblioteca: *"Un conjunto con
crédito regenerativo acumulado pero humedal bajo su SDV-E no está en coherencia: **INV2-E será su
juez**"* (Cap. 16.5 §16.5.14).

**Requisitos que las tierras secas imponen a INV2-E** (aportación de este documento; su especificación
completa pertenece al [documento 08](./08_INV2-E_invariante.md)):

1. **El invariante debe poder dispararse con UN solo indicador, sin cómputo completo del índice.** Es el
   requisito más fuerte y **no es una invención del proyecto**: es la regla 1OAO del principio 16 de la
   UNCCD. Consecuencia de implementación: `validate_invariant_sdv_e` **no puede** exigir el índice
   agregado para bloquear; con el primer sub-indicador negativo debe poder emitir `EN_VIOLACION`. Un
   invariante que necesite los tres indicadores para decidir **falla en el caso que el marco
   internacional diseñó para no fallar**.
2. **La jerarquía Evitar > Reducir > Revertir es el orden de las obligaciones del contrato, no un
   consejo.** Traducción `[HIPÓTESIS]`: ante una acción que afecte a la unidad, el contrato debe
   declarar primero qué **evita**, después qué **reduce** y solo al final qué **revierte**; una
   propuesta que vaya directamente a «revertir» sin haber evaluado evitar y reducir **es inválida**,
   porque invierte el principio 12 y con él T14 (la carga de la prueba recae sobre quien propone).
3. **Máquina de estados, no una sola bandera.** Cinco estados, y ninguno es un número:

| Estado propuesto | Significado | Acción ejecutable |
|---|---|---|
| `SANO` | Ningún déficit, ningún veto, **línea base certificada** | Ninguna |
| `EN_VIOLACION` | Déficit del canal A > 0, o un sub-indicador negativo (V1), sin veto | **Detener o modificar la actividad humana que viola el piso** |
| `CONSUMADO_IRREVERSIBLE` | Veto V2/V3/V4 activo | Bloqueo: no se admite compensación ni crédito que lo salde (§9) |
| `DEGRADADO_HEREDADO` | Línea base no certificada, posterior a la intervención, o ya degradada al declararse | **No se declara coherencia ni violación.** Obligación: certificar la línea base antes de contratar — es una obligación **de quien mide**, no un castigo al sujeto (mismo principio que el «insight I9» del documento 09) |
| `[SIN DATO]` | Falta la medición de una o más dimensiones | **No castiga y no autoriza.** La actividad no puede declararse en coherencia |

4. **La unidad de duración es explícita y prohibida de sustituir por el ejercicio fiscal.** Sin unidad,
   el factor no es comparable (lección del SDV-S). Regla dura: **ningún denominador puede ser más corto
   que el tiempo de recarga del recurso que el cálculo declara sostenible** (§5.5). Consecuencia
   operativa: **una extracción de agua fósil no puede declararse sostenible porque el ejercicio cierre
   en equilibrio.**
5. **Terminalidad.** Cuando el estado es `CONSUMADO_IRREVERSIBLE`, INV2-E **no vuelve atrás** por
   acumulación de crédito regenerativo, por mejora de la media del índice, ni por cambio de gobierno.
   El precedente documentado es un sistema de cultivo que desapareció y no volvió (Ghout), y la
   terminalidad no es una decisión estética: es el reconocimiento de un hecho ya ocurrido.
6. **Disparador contable, no numérico.** El canal B se implementa como **estado** y no como valor
   almacenado: `inf` no cabe en una columna numérica (documento 09 §5.3).

---

## 9. El suelo antes que el saldo (no compensación)

**La doctrina, literal:** *"El suelo antes que el saldo"*: el crédito regenerativo acumulado **no
compensa** caer bajo el SDV-E (Cap. 16.5 §16.5.14). En las tierras secas esta doctrina deja de ser un
principio y se vuelve **aritmética**, por tres argumentos que este ecosistema produce con números.

**Argumento 1 — El crédito tiene plazo; el acuífero no.** El crédito regenerativo se acumula en una
ventana humana (el ejercicio, el año, la vida de quien cuida). El agua de un acuífero árido se recarga
en una escala que no tiene contraparte en esa ventana: **miles de años**. **No es que el crédito sea
insuficiente: es que no hay tipo de cambio entre las dos unidades de tiempo.** Ningún número de
ejercicios de cuidado compra mil años de TA. Y el suelo sigue la misma asimetría: se forma en siglos y
se erosiona, según el propio marco, hasta **100 veces más rápido** que su tasa de formación natural
[REPORTADO, UNCCD].

**Argumento 2 — El daño se exporta fuera de la unidad contable.** Una tierra seca degradada no
contiene su daño: lo emite. El escenario base del GLO2 proyecta **69 Gt C** emitidas entre 2015 y 2050
por cambio de uso y degradación del suelo, desglosadas en **32 Gt C de carbono orgánico del suelo + 27
Gt C de vegetación + 10 Gt C de turberas** [REPORTADO, UNCCD, 2022]; y el propio IPCC trata el **polvo
mineral** como forzante climático de vida corta, mientras la UNCCD incluye la mitigación de tormentas de
arena y polvo entre las prácticas de restauración (casos de Irak, China y Kuwait) [REPORTADO, 2022].
**Un ecosistema árido degradado agrava el SDV-E de todos los demás ecosistemas del planeta**, incluidas
las generaciones que no consintieron (T14). Una compensación local completa seguiría siendo
**contabilidad incompleta**, porque la externalidad salió de la unidad.

**Argumento 3 — El contrapeso de la LDN no es un mercado de compensaciones.** Es la confusión más
probable y la más costosa, y este documento la cierra: el principio 7 de la LDN admite contrapesar
pérdidas con ganancias *"en el mismo marco temporal"*, pero el principio 8 exige la **misma escala** que
la planificación territorial y el 9 el **«like for like»**. Es planificación del uso del suelo, **no un
mercado de offsets**. Consecuencia dura: **la LDN no autoriza compensar una unidad bajo su SDV-E con
crédito acumulado en otra parte.** Si el proyecto citara la LDN como fuente y a la vez aceptara ese
contrapeso dentro de su contabilidad, estaría usando el marco para lo contrario de lo que el marco dice.

**Qué puede y qué no puede hacer el crédito regenerativo aquí (regla dura).**

| Puede | No puede |
|---|---|
| Financiar la **retirada o modificación de la actividad humana** que causa la violación | **Rebajar el déficit** de ninguna dimensión D1-D6 |
| Registrar el cuidado real bajo T13 (revegetación con especies propias, cierre de pozos, descanso de pastizales) | **Desactivar un veto** V1-V4 ni revertir `CONSUMADO_IRREVERSIBLE` |
| Sostener a la **comunidad de custodia** y su trabajo de testimonio | **Comprar el instrumento**: la serie que juzga a la unidad no puede ser financiada por la unidad juzgada |
| Financiar medición **de terceros** ya existente (adhesión a programas de monitoreo, análisis de laboratorio independiente) | **Comprar el veredicto**: financiar el programa que emite el juicio |
| Pagar la **certificación de la línea base** por un tercero **elegido por quien no opera la extracción** (§5.2) | **Fijar la línea base** después de la intervención, o fijarla por la parte interesada |

**La última fila del bloque «no puede» es propia de este documento y es la más delicada.** En la
criosfera, la regla es que la unidad no pague su termómetro (documento 16 §9). En tierras secas hay un
objeto más peligroso que el termómetro: **la línea base**. Quien fija la línea base elige el piso contra
el que se le juzga, y el principio 4 de la LDN —que dice que el objetivo *es* la línea base— convierte
esa elección en el acto de mayor poder de todo el estándar. Por eso la regla se propone así:
**el crédito puede pagar la certificación de la línea base, pero no puede elegir al certificante.**
`[HIPÓTESIS]` — propuesta no ratificada.

**Estado real del crédito, hoy** (no es doctrina: es código, y se dice sin adornos):

- `r_units` negativo **está implementado y probado en su registro**: `app/micromax.py` documenta *"`r_units` NEGATIVO
  = crédito regenerativo (EVV 1.2 §4.3)"* y `tests/test_micromax.py::test_credito_regenerativo_r_negativo`
  lo ejercita con `-12.0`.
- **Pero no pesa**: no existe `SUM(r_units)`; el componente R del sistema general solo cuenta
  extracción; y el precio cierra en `float(max(0.0, round(price, 4)))` (`app/maxo.py`), de modo que
  **nunca es negativo**. Un conjunto puede acumular crédito regenerativo indefinidamente mientras el
  acuífero de su tierra seca desciende 2,37 m al año, y **ninguna cuenta lo nota**.
- Y `r_units` **no tiene ninguna validación de entrada**: acepta cualquier negativo (`-1e9`), no exige
  techo, tipo de cuidado, tercero ni evidencia; el campo `r_notes` existe pero es libre y opcional, y
  `NaN`/`inf` pasan el filtro.
- **Consecuencia, dicha sin eufemismos:** lo que existe es el **registro** de una magnitud con signo
  negativo y una prueba de que se acepta y se devuelve. **Lo que no existe es su contabilidad**: no suma,
  no pondera, no bloquea y no tiene consecuencia jurídica alguna. **[Un registro probado no es una
  contabilidad implementada, y §12 las separa a propósito.]**

**Un dato que este documento NO usa, y lo declara.** El GLO2 reporta una cifra de subvenciones
perversas que habría que reorientar para cumplir las metas de restauración, expresada en la fuente como
**«1,6 de 700»** miles de millones de USD por año [REPORTADO, UNCCD, 2022]. **Este documento no la
interpreta ni la usa como umbral**: la formulación admite más de una lectura y convertirlas en una cifra
única sería inventar precisión sobre una fuente ambigua. Queda declarada aquí y en §13.

---

## 10. Zona Libre: lo que NO se mide

La Zona Libre del Reino Natural ya está en el canon —*"parte del valor del humedal es inefable
(Cap. 7 §7.9) […] Medir todo sería la forma técnica de dejar de escucharlo"* (Cap. 16.5 §16.5.14)— y la
mecánica completa vive en el [documento 04](./04_Zona_Libre_del_Reino_Natural.md). Este documento no
repite esa demostración: aporta lo específico de las tierras secas y fija la frontera LEY/POLÍTICA.

**Cómo se protege lo inconmensurable, y por qué NO se pondera.** El SDV-S pondera su espacio interior
(0,20) y el SDV-H lo protege como derecho binario sin peso, *"precisamente porque medir la
rehabilitación o la opacidad con la misma vara cuantitativa que el agua o la vivienda las destruiría"*
(Cap. 8 §8.11). En una tierra seca, ponderar lo inefable tendría un efecto concreto y perverso:
**un índice de verdor pagaría la pérdida de lo que no se mide** — y ese índice puede subir por una
invasión leñosa o por riego que saliniza, es decir, **por la causa misma de la degradación** (§3.5 y
§5.2). Ponderar la Zona Libre aquí no sería un error de calibración: sería una máquina de compensar
pérdidas irreversibles con datos que mejoran por la causa de la pérdida.

**Propuesta `[HIPÓTESIS]`, coherente con el canon y con el documento 04 §10:** la Zona Libre de las
tierras secas se protege como **dimensión binaria auditable sin peso (D7, §4.2)**, siguiendo el
precedente de las dimensiones VIII y IX del SDV-H; su violación **se documenta (T13) y no se cuantifica**.

**La contribución específica de este documento a la doctrina de la Zona Libre, en dos reglas.**

1. **La Zona Libre no puede absorber deuda de medición que un tercero cubre gratis.** Los tres
   sub-indicadores del piso de D1 los computa Copernicus CLMS/JRC con datos abiertos: su coste para la
   unidad es nulo. Declararlos «inefables» sería usar la figura más respetuosa del estándar para no
   mirar lo que ya está mirado desde fuera (§4.2, puerta adicional de coste de tercero).
2. **En tierras secas el catálogo de lo no medido tiene un incentivo económico invertido.** Medir es
   caro —distancias, acceso, pocos pozos— y no medir es barato. Es la inversión exacta del caso de la
   criosfera, donde la inefabilidad era evidente y la medición imposible por física. Por eso aquí la
   **prueba de inefabilidad del documento 04 §10.3 se aplica con la carga de la prueba del lado de
   quien declara**, y el coste declarado de la medición es parte de la prueba.

**Frontera explícita.**

- **LEY (no se vota).** Que la Zona Libre exista en cada unidad de tierra seca, que su peso sea **0,00**,
  que no entre jamás en el numerador de la fórmula y que su violación se registre por T13. Nada de esto
  es votable: es la condición que impide que lo inefable se canjee contra el piso.
- **POLÍTICA (se vota).** **El catálogo de qué entra** en cada unidad —y con ello qué deja de medirse—
  es deliberación: categoría `critical` (quórum 60 %, consenso 75 %, T13, anti-flip-flop 14 días,
  `CHECK` en BD). Es votable **con carga de la prueba** y pasando la prueba de inefabilidad y la puerta
  de coste de tercero.

**El riesgo, dicho sin eufemismos.** Si el catálogo se vota sin esas dos pruebas, «declarar inefable» se
convierte en la vía más barata para vaciar el estándar —y en tierras secas es también la más barata
**económicamente**—, y este documento estaría blindando con la palabra «inefable» lo que solo es
incómodo o caro de medir. El canon ya previene contra esa deriva desde el otro lado: *"Cuidado ≠
extracción estética: jardín podado para la foto no es cuidado; se registra lo que regenera, no lo que
adorna"* (Cap. 16.5 §16.5.14). La Zona Libre no es un refugio para lo que no conviene medir.

**Una nota sobre el vocabulario, para no repetir un error.** Los estados de la matriz `ZL` del
documento 04 (`ZONA LIBRE`, `ZONA CIEGA`, `ZONA MEDIDA`, `ZONA HUÉRFANA`) **no son** los estados de
INV2-E de §8 (`SANO`, `EN_VIOLACION`, `CONSUMADO_IRREVERSIBLE`, `DEGRADADO_HEREDADO`, `[SIN DATO]`).
Son ejes ortogonales y fusionarlos sería un error de tipos: una unidad puede estar
`CONSUMADO_IRREVERSIBLE` y conservar su Zona Libre (el humedal se perdió y el territorio no se mide), o
estar `SANO` y en ZONA CIEGA (todo bien y nadie responde por la tierra).

---

## 11. Comparativa inter-reinos (SDV-H · SDV-A · SDV-E · SDV-S)

La comparación completa —16 ejes— vive en el [documento 09](./09_Comparativa_inter_reinos.md) §11. Aquí
se comparan **solo los ejes que las tierras secas ponen a prueba**, y se añaden **dos ejes nuevos** que
este ecosistema revela y que ningún otro reino de la familia obliga a mirar.

| Eje | **SDV-H** — humanos | **SDV-A** — animales | **SDV-E (zonas áridas)** | **SDV-S** — sintéticos |
|---|---|---|---|---|
| **Moneda temporal** | TVI (Cap. 5) | TA, traducido por el PIU | **TA.** *"El tiempo del territorio es TA y no se coloniza (el PIU traduce)"* (Cap. 16.5 §16.5.14). Aquí el tiempo del sujeto es **fósil**: miles de años de recarga | TPI |
| **Unidad de duración de la violación** | Meses (ejemplo canónico calibrado a 12 meses, Cap. 8 §8.5) | No especificada en el canon | **La ventana que el método de tercero exige para declarar cambio significativo** `[SIN FUENTE VERIFICADA]`; mínimo operativo: **≥ 2 observaciones comparables**. **Prohibido el ejercicio fiscal como denominador** | Horas TPI |
| **Forma del piso** | Magnitud positiva (L/día, m², años de educación) | Magnitud positiva (m²/animal, L/día) | **Relativa: la línea base de la propia unidad** (LDN, principio 4) + **regla booleana** (1OAO, principio 16) | Escala 0-1 |
| **Separación piso / plenitud** | Distintas (y el motor las confundió una vez) | Distintas (0,25 vs 0,75 m²/gallina) | **Distintas y no comparables en magnitud**: la plenitud **no es «más verde»** (§3.5). En D5 el óptimo es el régimen de herbivoría propio, **no cero pastoreo** | Distintas |
| **Base neutra del factor** | No aplica (es suma) | No neutra por diseño: 0,2 con cumplimiento pleno | **Exigible: exactamente 1,0** con violación 0 | 1,0 exacto (corregida la v1) |
| **Estado terminal** | No existe: hay rehabilitación (Dim. VIII) | Prohibición de mercado | **`CONSUMADO_IRREVERSIBLE`** (salinización acoplada, pérdida del humedal) + **`DEGRADADO_HEREDADO`** (estado nuevo de este documento) | Retractación + Cápsula de Memoria |
| **Remedio tras la violación** | Rehabilitación e reintegración | Impide la siguiente; no devuelve la vida | **Dejar de extraer.** La única acción ejecutable es detener o modificar la actividad humana, en el orden **Evitar > Reducir > Revertir** | Capa de Ternura, Crédito de Sanación |
| **Forma de la transgresión máxima** | No existe estado terminal: hay rehabilitación (Dim. VIII) | El `∞` **no es una cifra**: es **prohibición de mercado** (Cap. 9 §9.8) | **Igual que el SDV-A: `∞` es consecuencia jurídica, no número.** Un contrato que guarde `inf` en una columna numérica no es ejecutable; uno que pase a `estado = PROHIBIDO` sí. Por eso el canal B se almacena como **estado** (§5.1, §8) | SDV-S: el factor `FS_S = e^v` **no es un estado terminal**, su consecuencia es la **interrupción del sistema** y la retractación (Cap. 9.5 §9.5.5, §9.5.10) |
| **Voz del sujeto** | Habla y declara su estado | No habla; tutor humano localizable | **No habla**, y su «voz» medida puede **subir mientras se degrada** (invasión leñosa, riego que saliniza) o **bajar mientras está sana** (sequía dentro del ciclo) | Registra su propio estado en bitácora |
| **Quién audita** | Auditoría independiente | Certificación por entidades sin conflicto | **Terceros que auditan el estado, no el cumplimiento del SDV-E** — pero con la ventaja de que **el piso de D1 lo computa un tercero con datos abiertos y regla booleana**: el veredicto no depende de la interpretación del proyecto | AOS: par sintético independiente |
| **Eje nuevo 1 — Naturaleza del piso** *(aportado por este documento)* | Dignidad intrínseca + capacidades fundamentales (DUDH, OMS) | Diseño biológico + etología científica | **El piso es un acto político con fecha**: la línea base **alguien la mide, la fecha y la certifica**. Ningún otro reino tiene un piso cuya fijación sea, en sí misma, un riesgo de captura (§5.2) | Coherencia + potencial experiencial |
| **Eje nuevo 2 — Relación entre el observador y el sujeto** *(aportado por este documento)* | El observador es el sujeto | El sujeto no habla; el tutor lo representa | **El estado de referencia y la degradación pueden ser indistinguibles desde fuera**: un desierto sano y un desierto degradado se parecen en una imagen de satélite, y un suelo cubierto de costra biológica se clasifica como «suelo desnudo». **El observador debe saber qué está mirando antes de medir** | El sujeto registra su propio estado: no hay asimetría de observación |

**Lo que la comparación revela, en tres frases.**

1. **Las tierras secas son el único reino de la familia donde el piso no es un dato, sino una decisión
   con fecha y certificante.** En el SDV-H el piso viene de la dignidad y de la OMS; en el SDV-A, del
   diseño biológico y la etología; en el SDV-S, de la coherencia y el potencial experiencial. Aquí viene
   de **la propia unidad en un momento del pasado**, y por eso el estándar tiene que proteger el acto de
   fijarlo, no solo el valor fijado.
2. **Es el único ecosistema donde la misma imagen puede significar salud o degradación, y el estándar no
   puede resolverlo con más resolución: tiene que resolverlo sabiendo qué mira.** El sesgo «verde =
   sano» no es una imprecisión del instrumento; es un error de categoría, y §4.1 (D3) muestra su forma
   más cruda: **la costra biológica es literalmente clasificada como suelo desnudo**.
3. **Es el único reino de la familia cuyo piso es, a la vez, el más auditable y el más capturable.**
   Los tres sub-indicadores los computa un tercero con regla booleana —lo más auditable de la
   biblioteca—; la línea base la declara un interesado —lo más capturable—. Ambas cosas son verdad al
   mismo tiempo, y el estándar que no declare las dos estaría contando media historia.

---

## 12. Estado de implementación

**Lo que existe hoy en el repositorio** (verificado por lectura directa de código, tests y capítulos del
canon, octubre 2026):

| Pieza | Dónde | Estado |
|---|---|---|
| `r_units` negativo como crédito regenerativo | `app/micromax.py` (`log_cdd`) | 🟢 **registrado** — se acepta, se persiste (`r_units`, `r_notes`), se devuelve en el vector `[T, V, R]` y está probado (`tests/test_micromax.py::test_credito_regenerativo_r_negativo`, con `-12.0`) — **y ninguna otra pieza lo consume: registro, no contabilidad** (§9, y la fila 🔴 correspondiente) |
| **V no admite negativos; R sí** | `app/micromax.py` (`if v_ucv < 0`) | 🟢 invariante de diseño real |
| Parte `eco-` (Ecosistema) | `app/parties.py` (`PARTY_TYPES`, `COLLECTIVE_PREFIXES`) | 🟢 creada y usable |
| Guardián oráculo del ecosistema | `app/contracts_bp.py` (`_guardian_approve_ecosystem()`) | 🟡 funciona en la firma de contratos; heurística laxa (R13) |
| Test del guardián | `tests/test_maxocontracts/test_parties_escalas.py` (`TestEcosystemGuardian`) | 🟢 2 casos (aprueba / deniega por γ) |
| Déficit normalizado en el validador | `maxocontracts/blocks/sdv_validator.py` (`relative = deficit / required`) | 🟢 implementado — **y es justo la fórmula que este documento tiene que leer contra la línea base propia, no contra una norma** (§5.2) |
| ISE — Índice de Salud Ecosistémica | `docs/architecture/metricas_detalle_kpis_oraculos_dinamicos.md` (IN-01) | 🟡 documento con pesos, bandas y fórmula; **cero código**. Y **no tiene componente de aridez ni de degradación de la tierra**: sus cinco componentes son biodiversidad (30 %), calidad del agua (20 %), calidad del aire (20 %), salud del suelo (15 %) y poblaciones clave (15 %) [VERIFICADO: lectura del documento en esta sesión] |
| Auditoría estructural de esta biblioteca | `tests/test_sdv_e_biblioteca.py` + `scripts/verificar_enlaces_sdv_e.py` | 🟢 plantilla, LEY/POLÍTICA, frases prohibidas, anclas de línea y estado HTTP real de las URLs |

**Lo que NO existe** (y está prohibido afirmar que existe):

| Pieza | Estado | Evidencia |
|---|---|---|
| Clase `SDV_E` en el motor | 🔴 | `maxocontracts/core/types.py` define `SDV` y `SDV_S`; **no hay `SDV_E`**. `resolve_participant_by_pid` (`app/parties.py`) asigna a la parte `eco-` **el SDV humano** (`sdv_actual=SDV()`) |
| `INV2-E` | 🔴 | no hay `validate_invariant_sdv_e` en `maxocontracts/core/axioms.py` ni bloque gemelo de `sdv_s_validator.py` |
| **Cualquier dato de tierras secas** | 🔴 | **cero sensores, cero ingestores, cero consumo de Copernicus, cero referencias a UNCCD, AQUASTAT o WRI en `app/`** [VERIFICADO: búsqueda directa en esta sesión] |
| La LDN como marco | 🔴 | **`docs/architecture/` no menciona desertificación, tierras áridas ni UNCCD en ningún archivo** [VERIFICADO: búsqueda directa en esta sesión] |
| Serie piezométrica, línea base de COS o transecto de costras como fuente | 🔴 | no hay tabla, ni columna, ni semilla. `simulator/` no tiene las carpetas que anuncia `AGENTS.md` |
| Identidad de la representación natural (7 campos) | 🔴 | sin tabla; `maxo_parties` tiene columnas genéricas. La propuesta de «línea base certificada con fecha» (§5.2, §7) no tiene dónde vivir |
| Mandato ecológico versionado / OCI | 🔴 | `actor_kind` está cerrado a `{"human","synthetic"}` (`app/synthetic_sessions.py`): **un guardián ecológico no cabe en la bitácora** |
| Estado `DEGRADADO_HEREDADO` y control de fecha de línea base | 🔴 | no existe modelo de sujeto, ni de línea base, ni de su fecha de certificación |
| Contabilidad del crédito regenerativo | 🔴 | no existe `SUM(r_units)`; el R del sistema solo cuenta extracción y el precio cierra en `max(0.0, …)` (`app/maxo.py`): **nunca es negativo** |
| Validación de `r_units` | 🔴 | acepta cualquier negativo (`-1e9`); `NaN` e `inf` pasan el filtro; no exige nota, evidencia ni techo |
| Traducción TA↔TVI ejecutable | 🔴 | `PIU.valorar_ta_natural` es un `pass` con comentario (`docs/architecture/DISENO_IMPLEMENTACION_FUTURA.md`) |
| Test de no colonización del TA (general y de la recarga) | 🔴 | **no existe**. Ni `test_sdv_e_no_coloniza_ta` (documento 16 §5.3) ni `test_sdv_e_no_coloniza_ta_aridas` (§5.5) |
| Quórum `eco-` N-de-M | 🔴 | el camino ecosistema retorna antes de la lógica de quórum; **el libro afirma lo contrario** (Cap. 16.5 §16.5.14) → incoherencia teoría↔código declarada |
| Procedimiento de disputa | 🔴 | inexistente. Y en tierras secas es más grave: **la disputa sobre la fecha y el certificante de la línea base no tiene foro** |
| Mapas vivos actualizados | 🔴 | `docs/architecture/mapa_coherencia_ola4.md` no menciona `r_units`, el Reino Natural ni el SDV-E; `docs/architecture/requisitos_fase2_ola4.md` no tiene ningún RF del Reino Natural |

**Tres hallazgos de esta auditoría que son específicos de este documento:**

1. **El canon nombra el desierto una vez, como sustantivo de una lista, y la sequía una vez, como
   ciclo.** *Desertificación*, *aridez*, *árido* y *UNCCD* tienen **cero ocurrencias** en los capítulos
   fuente y **cero en `docs/architecture/`**. Este documento no contradice al canon: **lo estrena**, y
   con menos anclaje textual que cualquier otro de la biblioteca salvo el de criosfera.
2. **El ISE, que es la base numérica declarada del SDV-E, no tiene componente de degradación de la
   tierra.** Pondera biodiversidad, agua, aire, suelo y especies clave; **no pondera cobertura ni
   productividad ni carbono** —los tres sub-indicadores del único marco internacional vinculante sobre
   tierras secas—. Aplicado a una unidad árida, el ISE **no puede detectar la desertificación**, y esa
   afirmación se sostiene leyendo el documento, no interpretándolo.
3. **`docs/architecture/DISENO_IMPLEMENTACION_FUTURA.md` y los documentos de oráculos dinámicos
   describen sensores y fuentes como si fueran arquitectura, sin marcar que no están implementados.**
   No hay un solo ingestor ambiental en `app/`. Cualquier lector que tome esos documentos como estado
   del sistema se equivoca, y este documento lo declara.

**Estado de este documento:** texto de estándar redactado (este archivo), **sin ninguna pieza de código
asociada**. No añade requisitos de implementación: los hace explícitos. La regla que gobierna esta
sección es la del brief: *estándar primero, contabilidad después* (Cap. 16.5 §16.5.14).

**Riesgos de seguridad abiertos que afectan directamente a la representación `eco-`:** **R4** partes
fantasma (severidad alta) · **R6** T9 no validado en la creación (alta) · **R13** guardián eco con
heurística laxa (media). Fuente: `docs/architecture/blindaje_anti_gamificacion_equidad.md`. Y una
advertencia propia: **R4 es peor en tierras secas que en cualquier otro ecosistema**, porque aquí el
objeto fabricable no es solo el sujeto sino **su línea base** (§7): un guardián no puede inventar un
acuífero, pero sí puede declarar un piso cómodo con fecha conveniente.

---

## 13. Preguntas abiertas

Lo que este documento **no** resuelve, dicho sin fingir cierre. Las nueve primeras son vacíos de fuente
encontrados en la verificación; las restantes, decisiones doctrinales que este documento deja abiertas a
propósito.

1. **Costras biológicas: cero umbral verificado.** No se obtuvo **ninguna** fuente con valor numérico,
   organismo y año sobre cobertura mínima antes de que se dispare la erosión, tasa de fijación de
   nitrógeno, extensión global o sensibilidad al pisoteo. Todas las candidatas serias devolvieron **403**.
   **El artículo de *Catena* sobre el umbral de cobertura existe** (enlace en §14.3, bloqueado a agentes
   automáticos) y **debería ser lo primero que abra una persona**. Es el vacío más importante de este
   documento.
2. **El índice de aridez pierde poder de delimitación bajo cambio climático.** El propio IPCC advierte
   que *"no es un proxy preciso"* en un ambiente con CO₂ creciente y que *"la utilidad de los umbrales
   de IA aplicados actualmente es limitada"*, sugiriendo precipitación, humedad del suelo y
   productividad primaria como alternativas [REPORTADO, 2019]. **¿Con qué criterio se delimita una
   unidad árida cuando el índice de aridez deja de servir?** Este documento usa la frontera de aridez
   para **clasificar** y no para juzgar salud, pero no resuelve la delimitación futura.
3. **No existe piso absoluto de carbono orgánico del suelo para tierras áridas.** La LDN es relativa
   por diseño (principio 4). Si el SDV-E quiere un piso en t C/ha o en % de COS, **tiene que proponerlo
   él**; este documento no lo hace, y remite al [documento 14](./14_Ecosistemas_Suelos_vivos.md) §4 (D2).
4. **No existe umbral numérico de irreversibilidad para tierras áridas.** El IPCC declara la falta de
   conocimiento sobre límites de adaptación y maladaptación [REPORTADO, §3.6.4]. El constructo de §4.1
   (D4) —tiempo de retorno contra la línea base— es `[HIPÓTESIS]` del proyecto, **no estándar
   internacional**.
5. **No hay indicadores operacionalizables de resiliencia.** No se encontró ninguna métrica
   estandarizada de tiempo de recuperación, capacidad de carga adaptativa o memoria ecológica. **Es un
   vacío global, no solo del proyecto**, y sin él la dimensión D4 depende de una medición derivada que
   nadie ha validado.
6. **Salinidad: el umbral sigue sin verificar.** El caso Souf da el acoplamiento (R > 0,99) pero **no**
   un valor de CE a partir del cual el sistema árido colapsa. El umbral clásico de 4 dS/m **no se
   verificó en esta sesión y este documento no lo escribe**; el [documento 14](./14_Ecosistemas_Suelos_vivos.md)
   §4 (D4) resuelve el suelo con el 2 dS/m verificado del GSASmap de la FAO y declara la discrepancia.
   La frontera entre la salinidad del suelo y la del agua de riego **no está cerrada**.
7. **Pastoreo: tengo el factor de uso, no la carga.** El **50 % de utilización** es sólido y está
   publicado; **no** se obtuvieron tiempos de descanso ni cargas animales en ha/UGM específicas por tipo
   de pastizal árido. **No confundir «50 % de uso» con «X ha por unidad animal»**: son parámetros
   distintos y este documento solo tiene el primero.
8. **La ventana del método de tercero no está verificada.** La guía GPG v2 (2025) del ODS 15.3.1
   describe severidad y nivel de confianza, pero **este documento no verificó cuántos años exige para
   declarar un cambio significativo**, y por eso **no fija la unidad de duración** (§5.5). Sin ese
   número, el SDV-E de tierras secas no puede calibrar su factor de duración. **Es la deuda técnica más
   concreta de este documento.**
9. **Dos cifras de población que no coinciden, y no se promedian.** El IPCC cita *"unos 3 000 millones
   de personas"* en tierras áridas (van der Esch *et al.* 2017); la nota del GLO2 dice *"una de cada
   tres personas"* (≈ 2 700 millones). **Las dos se citan con su fuente y no se resuelven aquí.**
10. **Humedales áridos: el marco reconoce que están mal cartografiados.** El Manual Ramsar Vol. 17
    —la fuente pertinente— está **bloqueado (403)**. No hay cifra global verificada de extensión ni de
    número de humedales áridos u oasis, y por tanto **la línea base de D6 puede no existir** en la
    mayoría de las unidades.
11. **Caudal ecológico para humedales áridos: sin verificar.** Pertenece al documento 11 (Humedales) y
    al 12 (Ríos y cuencas); este documento no lo inventa.
12. **¿Cómo se audita la fecha de una línea base?** §5.2 y §7 exigen que la línea base esté certificada
    **antes** de la intervención y por un tercero **que no elija la parte interesada**. **El mecanismo no
    existe**: no hay registro de líneas base, ni foro de disputa, ni forma de probar que una medición es
    anterior a una intervención si nadie la publicó entonces. Es un problema abierto y es,
    probablemente, el más difícil que las tierras secas le plantean al proyecto.
13. **`DEGRADADO_HEREDADO`: ¿qué se hace con una unidad que ya estaba degradada?** El estado se propone
    en §8 y **no tiene consecuencia contable definida**. ¿Se le exige restaurar antes de contratar? ¿Se
    le mide solo la tendencia? ¿Quién paga la certificación de su línea base? El canon no lo resuelve y
    este documento tampoco.
14. **La unidad de duración del SDV-E de tierras secas.** Este documento propone el mínimo operativo
    (≥ 2 observaciones comparables), prohíbe el ejercicio fiscal como denominador y **se niega a fijar un
    número** sin la ventana del método de tercero (pregunta 8). La decisión pertenece al documento 07.
15. **El quórum `eco-` N-de-M.** El canon dice «N-de-M» y solo publica números para cooperativas (60 %
    de miembros, o 2 de 3 delegados). **No hay N ni M para el Reino Natural**, y en tierras secas se
    agrava: si el piso depende de una línea base certificada, **¿quién certifica cuando la unidad no
    tiene comunidad de custodia?**
16. **¿Quién paga el instrumento?** §9 prohíbe que el crédito de la unidad elija a quien fija su línea
    base. La prohibición es correcta en principio y **no tiene mecanismo de financiación**: hoy no existe
    ninguna fuente para la infraestructura de medición. Un estándar que exige series piezométricas y
    certificación de tercero **depende por completo de la voluntad de terceros**.
17. **Los PDF verificados y no leídos.** Están vivos (HTTP 200) y **no se explotaron por límite de
    recursos**: el Cross-Chapter Paper 3 del AR6 WGII («Deserts, Semi-Arid Areas and Desertification») y
    su versión SOD, el GLO2 completo, el capítulo 12 del GLO2 (cuencas de tierras áridas), *Drought in
    Numbers*, el CRIC-2 y el *National Range and Pasture Handbook* Parte 645. **Contienen, con alta
    probabilidad, parte de lo que aquí queda sin fuente** —sobre todo resiliencia y sequía—. **No se cita
    ninguna cifra de ellos porque no se leyeron**, y quien continúe este documento debería empezar por
    ahí.
18. **La cifra «1,6 de 700» del GLO2.** Este documento la declara y **no la interpreta** (§9). Quien la
    use debe resolver primero qué mide exactamente.
19. **La doble acepción de «costra».** §4.1 (D3) la desactiva con una tabla y una regla de verificación
    de campo. **¿Debería ser una regla del estándar entero** —y no solo de las unidades áridas— que
    ninguna clasificación de «suelo desnudo» compute sin verificación? Es una propuesta que este
    documento deja abierta a los documentos 14 y 20.
20. **¿Puede una tierra seca declarar plenitud sin verde?** §3.5 afirma que sí y convierte la
    afirmación en prohibición contable. **Pero no existe ningún índice publicado que mida salud de
    tierras secas sin usar cobertura vegetal como proxy principal**, y este documento no lo construye.
    Es la pregunta abierta más profunda de las veinte.

---

## 14. Referencias

**Regla aplicada:** solo URLs con estado HTTP registrado en la sesión de verificación de esta rama
(octubre 2026), re-comprobadas con `scripts/verificar_enlaces_sdv_e.py`. Ninguna cifra de este documento
se apoya en una URL sin estado. Se indica el estado entre paréntesis y **se marca lo que está bloqueado
a agentes automáticos**, porque un 403 de estas fuentes es evidencia de que existen, no de que no.

**Alcance de esta sección, dicho antes de la primera tabla.**

- El registro completo de la sesión de verificación —**35 URLs verificadas (200)**, **14 bloqueadas**
  (403/203) y **24 muertas o descartadas**— vive en `scratch/sdv_e/fuentes/17_aridas.md`, que es un
  **documento de trabajo, no de la biblioteca**, y por tanto no se enlaza aquí como si fuera canon.
- Las afirmaciones sobre el código de §12 se verificaron **por lectura directa del repositorio**, no por
  URL.
- **Fuentes que este documento NO usa y nombra sin enlace a propósito** (un enlace roto citado como si
  fuera fuente es exactamente lo que el verificador debe cazar): la ruta de la jerarquía de respuesta de
  la UNCCD (`unccd.int/actions/ldn-response-hierarchy`, **404** — el contenido de la jerarquía sí está
  en la página de principios LDN, §14.2); el Mapa de aridez de FAO AQUASTAT en el catálogo de datos
  (`data.apps.fao.org`, **000** — la página de AQUASTAT sí es 200 y se cita en §14.4); la ruta del
  Cross-Chapter Paper 3 en el sitio del IPCC (`ipcc.ch/report/ar6/wg2/chapter/cross-chapter-paper-3`,
  **404** — las URL vivas son los PDF de §14.6); el compendio de tormentas de arena y polvo de la OMM
  (tres rutas probadas, **404**); y la ruta de NRCS sobre pastoreo y salud del suelo
  (`nrcs.usda.gov/resources/guides-and-instructions/grazing-management-and-soil-health`, **404** — la
  nota técnica viva es la de §14.5). Se listan aquí para que nadie las reintroduzca «porque circulan».
- **Tres fuentes que el informe de verificación de esta rama daba por bloqueadas (403) y que el
  verificador del repositorio resolvió de otro modo, retiradas de las tablas por esa razón** —se
  nombran sin enlace y con el código observado, para que nadie las reponga creyendo que solo están
  bloqueadas—: la ruta del USGS sobre costras biológicas del programa de adaptación climática
  (`usgs.gov/programs/climate-adaptation-science-centers/...`, **404** al cliente del verificador y
  **403** a curl); el *Global Drylands Outlook* del UNEP
  (`unep.org/resources/report/global-drylands-outlook`, **404/403**); y el PDF de la tipología IUCN
  aplicada a SEEA-EA (`seea.un.org/.../keith_iucn_typology_seea-eea_forumexperts_jun2020.pdf`,
  **404/403**). **Ninguna cifra de este documento provenía de ellas**, de modo que su retirada no deja
  ningún dato sin respaldo: los vacíos que declaraban siguen declarados en §13. Se conserva en su lugar
  la tipología IUCN por su registro principal (§14.6) y el registro de publicaciones del USGS sobre
  costras biológicas, que sí responde como bloqueada (§14.3).
- **Nota de mantenimiento, declarada para evitar un falso negativo.** La nota técnica n.º 39 del USDA
  NRCS es **la fuente del umbral más determinante de este documento** (el factor de uso del 50 %, D5) y
  responde **200 a `curl.exe`** y a cualquier cliente HTTP estándar, pero **rechaza la conexión del
  cliente con que está escrito `scripts/verificar_enlaces_sdv_e.py`**: con ese cliente devuelve
  `ConnectionResetError` o tiempo de espera agotado, de forma reproducible, mientras que la misma
  petición con cabeceras `Accept` y `Connection: close` devuelve **200**. **Es una limitación del
  servidor frente a un cliente concreto, no un enlace muerto**, y se declara aquí para que nadie retire
  la única fuente publicada del umbral de pastoreo por un fallo de negociación HTTP.
- **Reintento obligatorio antes de declarar un enlace muerto.** La misma clase de falso negativo se
  observó en dos URL de primer orden de este documento —la guía GPG v2 en `land.copernicus.eu` y el
  capítulo 12 del GLO2 en `unccd.int`—: una pasada en lote devolvió `000` y la comprobación aislada e
  inmediata devolvió **200** con el mismo comando. Regla que este documento deja escrita para quien
  mantenga el verificador: **ningún `000` ni `ConnectionResetError` se registra como URL muerta sin una
  segunda comprobación aislada**, porque un servidor lento o que cierra conexiones no es una fuente
  inexistente. Las 54 URL de esta sección devuelven estado vivo en comprobación aislada.

### 14.1 Desertificación, aridez y tierras áridas — el marco de definición

| Fuente | Aporte | URL (estado) |
|---|---|---|
| IPCC — SRCCL, Cap. 3, *Desertification* | Definición de desertificación (todas las formas y niveles de degradación en tierras áridas, **no** equivalente a expansión del desierto); frontera hiperárido/árido y exclusión del hiperárido de la definición de desertificación (UNCCD 1994); *"los desiertos son ecosistemas valiosos"* y no propensos a desertificación; **46,2 % (± 0,8 %)** de la superficie terrestre en tierras áridas; **≈ 3 000 millones** de personas (van der Esch *et al.* 2017); **aridez ≠ sequía**; oasis: definición, abandono histórico y persistencia de miles de años; **falta de conocimiento sobre límites de adaptación**; advertencia de que el índice de aridez no es proxy preciso bajo CO₂ creciente | https://www.ipcc.ch/srccl/chapter/chapter-3/ (200) |
| IPCC — SRCCL, Cap. 3, Fig. 3.1 (introducción a la naturaleza de la desertificación) | **Clasificación completa del índice de aridez**: hiperárido < 0,05 · árido 0,05-0,20 · semiárido 0,20-0,50 · subhúmedo seco 0,50-0,65 | https://www.ipcc.ch/srccl/chapter/chapter-3/3-1-the-nature-of-desertification/3-1-1-introduction/c3_figure-3-1/ (200) |
| IPCC — SRCCL, Cap. 3 §3.7.4, *Oases in hyper-arid areas* | Proyección del sur de Túnez a 2050 (**+2,7 °C**, **−29 %** precipitación, **+14 %** evapotranspiración); demanda agrícola de agua en Arabia Saudí (**+5 a +15 %**); definición de oasis | https://www.ipcc.ch/srccl/chapter/chapter-3/3-7-hotspots-and-case-studies/3-7-4-oases-in-hyper-arid-areas-in-the-arabian-peninsula-and-northern-africa/ (200) |
| IPCC — SRCCL, Cap. 3 §3.6.4, *Limits to adaptation, maladaptation and barriers* | *"Actualmente hay una falta de conocimiento de los límites de adaptación y de la maladaptación potencial a los efectos combinados del cambio climático y la desertificación"* — **la fuente del vacío de D4** | https://www.ipcc.ch/srccl/chapter/chapter-3/3-6-responses-to-desertification-under-climate-change/3-6-4-limits-to-adaptation-maladaptation-and-barriers-for-mitigation/ (200) |
| IPCC — SRCCL (ancla del informe) | Informe especial sobre cambio climático y tierra (2019) | https://www.ipcc.ch/srccl/ (200) |
| CBD — Marco Kunming-Montreal (30x30) | Meta de conservación del 30 % para 2030: marco de política en el que se inscribe el SDV-E | https://www.cbd.int/gbf (200) |
| Fronteras planetarias (Stockholm Resilience Centre) | Marco de los límites planetarios; la UNCCD reporta **4 fronteras ya excedidas** vinculadas a la desertificación (clima, biodiversidad, uso del suelo, ciclos geoquímicos) | https://www.stockholmresilience.org/research/planetary-boundaries.html (200) |

### 14.2 Neutralidad en la degradación de la tierra (LDN / ODS 15.3) — el respaldo externo de INV2-E

| Fuente | Aporte | URL (estado) |
|---|---|---|
| UNCCD — *LDN principles* (los 19 principios) | **Principio 4**: el objetivo LDN **es igual a la línea base**. **Principio 7**: contrapeso en el mismo marco temporal. **Principio 8**: misma escala que la planificación del uso del suelo. **Principio 9**: «like for like». **Principio 12**: jerarquía **Evitar > Reducir > Revertir**, con prioridad de evitar y reducir. **Principio 15**: **3 sub-indicadores obligatorios** (cobertura del suelo + productividad + COS). **Principio 16**: **regla «uno fuera, todos fuera»** —si UNO muestra cambio negativo significativo ⇒ PÉRDIDA— y regla de ganancia (≥ 1 positivo y ninguno negativo). **Es la arquitectura externa de INV2-E** | https://www.unccd.int/land-and-life/land-degradation-neutrality/ldn-principles (200) |
| UNCCD — *Land Degradation Neutrality: overview* | Definición de LDN; **70 %** de la tierra libre de hielo alterada; **3 200 millones** de personas afectadas; **90 %** de la tierra con huella humana en 2050; **32 Gt C** 2015-2030; **131/196** países comprometidos | https://www.unccd.int/land-and-life/land-degradation-neutrality/overview (200) |
| UNCCD — nota de prensa del **Global Land Outlook 2** (2022) | **Hasta 40 %** de la tierra degradada; **más del 45 %** de tierras áridas y «una de cada tres personas»; **16 millones de km²** de degradación continuada a 2050; caída persistente de productividad del **12-14 %**; **69 Gt C** (COS 32 + vegetación 27 + turberas 10) 2015-2050; **1 000 millones de ha** comprometidas por **115+ países**; retorno de **7-30 USD** por USD; **4 fronteras planetarias** excedidas; subvenciones perversas («1,6 de 700», **no interpretada por este documento**) | https://www.unccd.int/news-stories/press-releases/chronic-land-degradation-un-offers-stark-warnings-and-practical (200) |
| UNCCD — página del **GLO2** | Documento de referencia del escenario base y del escenario de restauración (**+17 Gt C** netas y **+55 Gt C** de stock de carbono del suelo en 2050 frente al base) | https://www.unccd.int/resources/global-land-outlook/global-land-outlook-2 (200) |
| UNCCD — Resumen para decisores del GLO2 | Síntesis del informe para responsables de política | https://www.unccd.int/resources/global-land-outlook/glo2-summary-decision-makers (200) |
| UNCCD — **GLO2 completo** (PDF, 589 KB) | Documento primario. **Verificado el estado HTTP; no descargado ni leído** (§13.17) | https://www.unccd.int/sites/default/files/2022-04/UNCCD_GLO2_low-res_2.pdf (200) |
| UNCCD — **GLO2, Cap. 12**: cuencas hidrográficas de tierras áridas (PDF, 2,1 MB) | Capítulo específico de cuencas áridas. **Verificado; no leído** (§13.17): es la lectura pendiente más pertinente para D2 | https://www.unccd.int/sites/default/files/2018-06/GLO%20English_Ch12.pdf (200) |
| UNCCD — ***Drought in Numbers*** (página) | Publicación específica sobre sequía | https://www.unccd.int/resources/publications/drought-numbers (200) |
| UNCCD — ***Drought in Numbers*** (PDF, 1,0 MB) | Documento primario sobre sequía. **Verificado; no leído** (§13.17): es la lectura pendiente para D4 | https://www.unccd.int/sites/default/files/2022-05/Drought%20in%20Numbers.pdf (200) |
| UNCCD — documento **CRIC-2** (2025, PDF, 490 KB) | Documento de la Convención verificado y no explotado por límite de eficiencia | https://www.unccd.int/sites/default/files/2025-09/cric2-unedited.pdf (200) |
| UNCCD — ancla institucional | Convención de lucha contra la desertificación | https://www.unccd.int/ (200) |
| Copernicus Land Monitoring Service — **nuevas guías de la ONU para monitorear la degradación de la tierra** (2025) | **GPG v2 del ODS 15.3.1**: los 3 sub-indicadores, la regla 1OAO, la lógica de prevención de falsos positivos y negativos, y el método de COS alineado con los *IPCC 2019 Refinements*; simplificación de los métodos estadísticos y clarificación de **severidad y nivel de confianza** | https://land.copernicus.eu/en/news/new-un-guidelines-to-monitor-land-degradation (200) |

### 14.3 Suelo árido: carbono, costras biológicas y salud del pastizal

| Fuente | Aporte | URL (estado) |
|---|---|---|
| FAO — **GSOCmap** (Global Soil Carbon Map) | Primera compilación global de carbono orgánico del suelo **país por país, armonizada**: la referencia instrumental del sub-indicador de COS | https://www.fao.org/global-soil-partnership/gsocmap/en/ (200) |
| FAO — Portal de suelos | Marco institucional del recurso suelo | https://www.fao.org/soils-portal/en/ (200) |
| FAO — Biodiversidad del suelo | Biodiversidad edáfica como eje del portal | https://www.fao.org/soils-portal/soil-biodiversity/en/ (200) |
| FAO — Degradación y restauración del suelo | Eje de degradación y restauración | https://www.fao.org/soils-portal/soil-degradation-restoration/en/ (200) |
| USDA NRCS / BLM — *Interpreting Indicators of Rangeland Health*, TR 1734-6 (portal BLM) | **Indicadores cualitativo-cuantitativos con desviación respecto de la referencia**: suelo desnudo y erosión hídrica como señales acompañantes de D3 y D1 | https://www.blm.gov/policy/im-2018-064 (200) |
| ***Catena*** — *Maintaining biocrusts in grasslands above a threshold coverage is vital for soil erosion control in drylands* | **Contiene el umbral de cobertura de costras biológicas que este documento busca** y no pudo usar. **Bloqueada a agentes automáticos (403): pendiente de apertura humana.** Es la fuente prioritaria de §13.1 | https://www.sciencedirect.com/science/article/abs/pii/S0341816224006003 (403) |
| USGS — publicaciones sobre costras biológicas | Registro de publicaciones del USGS sobre costras biológicas. **Bloqueada a agentes automáticos (403)**: un humano la abre | https://www.usgs.gov/publications/biological-soil-crusts (403) |
| USDA Forest Service — RMRS-GTR-135: costras biológicas (PDF) | Informe técnico de referencia sobre costras biológicas del suelo. **Bloqueado (403)** | https://www.fs.usda.gov/rm/pubs/rmrs_gtr135_1.pdf (403) |
| **Maestre *et al.*, 2012**, *Science* 335:2144 — riqueza de especies y multifuncionalidad en tierras áridas globales | El artículo de referencia sobre biodiversidad de tierras áridas. **HTTP 203**, no 200: **no se cita ninguna cifra de él** en este documento | https://pubmed.ncbi.nlm.nih.gov/22246775/ (203) |
| DOI del mismo artículo (*Science*) | Registro primario. **Bloqueado (403)**; se cita a través del registro de PubMed | https://www.science.org/doi/10.1126/science.1215442 (403) |

### 14.4 Agua subterránea, estrés hídrico y oasis

| Fuente | Aporte | URL (estado) |
|---|---|---|
| Khezzani & Bouchemal, *Environmental Earth Sciences* 77 — registro en **FAO AGRIS** (2018) | **Caso del oasis del Souf (Sahara argelino)**: ventana óptima de profundidad **1-2 m**; **más del 77 %** del área ya la excede; descenso del freático **0,29 (2011) → 2,37 (2015) m/año**; descenso absoluto de **18,2 m** en Ghamra (2015); correlación descenso ↔ salinidad **R > 0,99**; *"llevó a la desaparición del sistema de cultivo del patrimonio agrícola mundial (Ghout)"*; 65 puntos, 2010-2015 | https://agris.fao.org/search/en/records/65df0d7363b8185d9caa78a8 (200) |
| WRI — *Highest water stressed countries*, **Aqueduct 4.0** (2023) | Estrés hídrico = **demanda / oferta renovable**; **40 % = alto**, **80 % = extremadamente alto**; **≈ 4 000 millones** de personas bajo estrés alto ≥ 1 mes/año (≥ 50 % de la humanidad); **25 países** en estrés extremadamente alto (**25 %** de la población mundial); proyección 2050: **+1 000 millones** y **MENA al 100 %**; advertencia de que *"el estrés hídrico no conduce necesariamente a una crisis hídrica"* | https://www.wri.org/insights/highest-water-stressed-countries (200) |
| WRI — **Aqueduct** (ancla de la herramienta) | Plataforma de datos de riesgo hídrico | https://www.wri.org/aqueduct (200) |
| FAO — **AQUASTAT** | Programa de información sobre agua y agricultura | https://www.fao.org/aquastat/en/ (200) |
| FAO — AQUASTAT, metodología de uso del agua | **110 000 km³/año** de precipitación sobre tierra; **43 000 km³/año** de recursos renovables; tipos de extracción | https://www.fao.org/aquastat/en/overview/methodology/water-use (200) |
| Manual Ramsar, **Vol. 17: humedales de zonas áridas** | La fuente más pertinente para D6: afirma que los humedales áridos están *"generalmente mal cartografiados"*. **Bloqueada (403)**: se cita como `[REPORTADO]` y con el aviso | https://www.ramsar.org/sites/default/files/documents/pdf/lib/hbk4-17.pdf (403) |
| Ramsar — Resolución VIII.40 (*Wetlands: water, life and culture*) | Resolución sobre agua, vida y cultura en humedales. **Bloqueada (403)** | https://www.ramsar.org/sites/default/files/documents/pdf/res/key_res_viii_40_e.pdf (403) |
| Ramsar — Resolución VIII.40, versión en español | Versión en español de la misma resolución. **Bloqueada (403)** | https://www.ramsar.org/sites/default/files/documents/library/key_res_viii_40_s.pdf (403) |
| Ramsar — actualización COP15 de la Resolución VIII.40 | Actualización de la resolución. **Bloqueada (403)** | https://www.ramsar.org/sites/default/files/2025-10/key_res_viii_40_e%20COP15_update.pdf (403) |

### 14.5 Pastoreo sostenible en tierras áridas

| Fuente | Aporte | URL (estado) |
|---|---|---|
| USDA NRCS — *Utilization and Harvest Efficiency*, Technical Note Plant Materials n.º 39 (PDF) | **«Take half and leave half» = 50 %** de utilización de la producción anual de forraje, con la advertencia de que es *"un punto de partida común o regla"*; el uso **incluye el forraje consumido y el daño por pisoteo, reposo y factores no ganaderos**; hasta **~25 %** de la producción anual se pierde por insectos, fauna silvestre y pisoteo; demanda por AU de **3,0 %** del peso corporal/día (**30 lb/día** para vaca de 1 000 lb); **AUM = 912,5 lb** (≈ 414 kg); **ajustes de capacidad de carga por distancia al agua** (100 % @ 2 640 ft → 90 % @ 5 280 → 70 % @ 7 920 → 50 % @ 10 560) y **por pendiente** (100 % @ 0-15 % → 70 % @ 15-30 → 40 % @ 31-60 → 0 % @ > 60) | https://www.nrcs.usda.gov/plantmaterials/idpmstn9390.pdf (200) |
| USDA NRCS — *National Range and Pasture Handbook*, Parte 645 (PDF, vía Rangelands Gateway) | Criterios de utilización sostenible del manual nacional de referencia | https://rangelandsgateway.org/sites/default/files/2024-02/National%20Range%20and%20Pasture%20Handbook%20%28Part%20645%29.pdf (200) |
| FAO / Banco Mundial — *Livestock & the Environment* | Contexto internacional del pastoreo y el ambiente | https://www.fao.org/3/x5304e/x5304e00.htm (200) |

### 14.6 Documentos verificados y NO leídos (la deuda de lectura declarada)

| Fuente | Aporte | URL (estado) |
|---|---|---|
| IPCC — AR6 WGII, **Cross-Chapter Paper 3: *Deserts, Semi-Arid Areas and Desertification*** (PDF, 1,99 MB) | **El compendio de referencia para este documento.** Verificado y **no leído** por límite de eficiencia (§13.17): con alta probabilidad contiene parte de lo que aquí queda sin fuente, sobre todo en resiliencia | https://www.ipcc.ch/report/ar6/wg2/downloads/report/IPCC_AR6_WGII_CrossChapterPaper3.pdf (200) |
| IPCC — versión **SOD** del mismo CCP3 (PDF, 1,68 MB) | Versión de borrador para revisión del mismo capítulo. **Verificada y no leída** | https://www.ipcc.ch/report/ar6/wg2/downloads/report/IPCC_AR6_WGII_SOD_CCP3.pdf (200) |
| IPCC — portal | Marco institucional. **Este documento no cita cifras del AR6 WG1/WG2 leídas**: solo los PDF de arriba, verificados como vivos | https://www.ipcc.ch/ (200) |
| UNCCD — marco conceptual científico de la LDN | Informe del marco conceptual científico de la neutralidad en la degradación de la tierra (la ruta viva; la ruta antigua está muerta, ver el encabezado de esta sección) | https://www.unccd.int/resources/reports/scientific-conceptual-framework-land-degradation-neutrality-report-science-policy (200) |
| Copernicus — observación de la Tierra | Infraestructura candidata para cobertura del suelo y productividad (**no integrada al proyecto**) | https://www.copernicus.eu/en (200) |
| IUCN — Tipología Global de Ecosistemas | Marco de clasificación de ecosistemas: **clasifica tipos, no resuelve la continuidad de identidad** de una unidad | https://www.iucn.org/resources/publication/iucn-global-ecosystem-typology (200) |
| IUCN — Tipología Global de Ecosistemas (PDF del informe 2024-021) | Documento primario de la tipología. **Bloqueado a agentes automáticos (403)**: un humano lo abre | https://portals.iucn.org/library/sites/library/files/documents/2024-021-En.pdf (403) |
| CBD — Decisión 15/4 (Marco Kunming-Montreal, PDF) | Texto de la decisión | https://www.cbd.int/doc/decisions/cop-15/cop-15-dec-04-en.pdf (200) |
| UNEP | Programa de Naciones Unidas para el Medio Ambiente | https://www.unep.org/ (200) |
| UNEP-WCMC | Centro de monitoreo de la conservación | https://www.unep-wcmc.org/ (200) |
| IPBES | Plataforma científica de biodiversidad | https://www.ipbes.net/ (200) |
| Protected Planet | Base de datos de áreas protegidas (la «puerta 1» de identidad del [documento 04](./04_Zona_Libre_del_Reino_Natural.md)) | https://www.protectedplanet.net/en (200) |
| ODS de la ONU | Marco de los Objetivos de Desarrollo Sostenible (ODS 15.3 y 15.3.1) | https://sdgs.un.org/goals (200) |

### 14.7 Referencias internas al canon (por capítulo y sección, sin anclas de línea)

- Cap. 5 §5.5 — Temporalidad inter-reinos, **TA** del Reino Natural, el **PIU** como único traductor, y
  **T14 — Principio de Precaución Intergeneracional** (menor irreversibilidad, carga de la prueba sobre
  quien propone): [capitulo_05_arquitectura_260126.md](../../../book/edicion_3_dinamica/capitulo_05_arquitectura_260126.md)
- Cap. 6 §6.4 — La comunidad del desierto y el multiplicador del componente `R_agua`:
  [capitulo_06_ontometria_260126.md](../../../book/edicion_3_dinamica/capitulo_06_ontometria_260126.md)
- Cap. 7 §7.9 — Zona Libre y valor inefable; ejemplo del desierto y `R_agua`:
  [capitulo_07_vhv_260126.md](../../../book/edicion_3_dinamica/capitulo_07_vhv_260126.md)
- Cap. 8 §8.11 — Dimensiones **VIII (Rehabilitación)** y **IX (Opacidad Vital)**: umbrales binarios
  *"no mediante pesos en la fórmula"*, precedente de la dimensión D7 de este documento:
  [capitulo_08_sdv_h_260126.md](../../../book/edicion_3_dinamica/capitulo_08_sdv_h_260126.md)
- Cap. 9 §9.8 — El `∞` como consecuencia jurídica (prohibición de mercado) en el SDV-A:
  [capitulo_09_sdv_a_260126.md](../../../book/edicion_3_dinamica/capitulo_09_sdv_a_260126.md)
- Cap. 9.5 §9.5.5-§9.5.11 — `FS_S = e^v` y base neutra 1,0, sensores nombrados, INV2-S con retractación
  a 7 ciclos, Capa de Ternura y Veto por Crimen de Coherencia:
  [capitulo_09_5_sdv_sinteticos_260126.md](../../../book/edicion_3_dinamica/capitulo_09_5_sdv_sinteticos_260126.md)
- Cap. 10 §10.3-§10.7 — Principio Precautorio de Consciencia, **SDV Universal** (la lista
  *"Ecosistemas: Bosques, humedales, desiertos, arrecifes"* y la dimensión *"Ciclos naturales
  respetados (fuego, inundación, sequía)"*), proporcionalidad, dignidad encadenada y **gobernanza
  operacionalmente finita**: [capitulo_10_tres_reinos_260126.md](../../../book/edicion_3_dinamica/capitulo_10_tres_reinos_260126.md)
- Cap. 16.5 §16.5.14 — El Reino Natural como conviviente: **TA no colonizado**, **PIU** como único
  traductor, **crédito regenerativo `r_units`**, representación `eco-` con guardián oráculo, Zona
  Libre, *"el suelo antes que el saldo"*, cuidado ≠ extracción estética:
  [capitulo_16_5_micromaxocracia_canonica_220826.md](../../../book/edicion_3_dinamica/capitulo_16_5_micromaxocracia_canonica_220826.md)
- Cap. 17 — **INV2** e invariantes de MaxoContracts (bloques, plantillas, partes de cualquier escala):
  [capitulo_17_maxocontracts_260126.md](../../../book/edicion_3_dinamica/capitulo_17_maxocontracts_260126.md)
- EVV-1.2 §4.3 — **R negativo = regeneración**:
  [capitulo_18_EVV_1.2_270126.md](../../../book/edicion_3_dinamica/capitulo_18_EVV_1.2_270126.md)

### 14.8 Referencias internas a esta biblioteca y al proyecto

- **Documento 04** — La Zona Libre del Reino Natural: la matriz `ZL` de cuatro estados, las siete
  puertas, la prueba de inefabilidad y el inventario negativo que este documento usa sin repetir:
  [04_Zona_Libre_del_Reino_Natural.md](./04_Zona_Libre_del_Reino_Natural.md)
- **Documento 07** — Fórmula de violación y pesos del SDV-E (`FE = e^(min(Σ…, V_max))`, base neutra
  1,0, unidades y bandas): [07_Formula_de_violacion_y_pesos.md](./07_Formula_de_violacion_y_pesos.md)
- **Documento 08** — INV2-E, el invariante que falta: especificación, tipos y retractación:
  [08_INV2-E_invariante.md](./08_INV2-E_invariante.md)
- **Documento 09** — Comparativa inter-reinos (16 ejes, familias de factores, la escalera del remedio,
  la regla de ámbito y la prohibición de trasvasar umbrales entre sujetos):
  [09_Comparativa_inter_reinos.md](./09_Comparativa_inter_reinos.md)
- **Documento 14** — Suelos vivos: **dueño doctrinal del carbono orgánico del suelo** (su D2), de la
  **salinidad y sodicidad** (su D4) y de la **costra física** (su D5), con el acoplamiento explícito a
  este documento: [14_Ecosistemas_Suelos_vivos.md](./14_Ecosistemas_Suelos_vivos.md)
- **Documento 16** — Montañas y criosfera: el criterio general de no colonización del TA y su test de
  invariancia al periodo contable, que este documento extiende con el criterio de la recarga:
  [16_Ecosistemas_Montanas_y_criosfera.md](./16_Ecosistemas_Montanas_y_criosfera.md)
- **Documento 02** — Unidad y sujeto del SDV-E (documento pendiente de esta biblioteca: la unidad
  ecológica y los criterios de «Persona Natural»).
- **Documento 03** — No colonización del TA (documento pendiente: el criterio de §5.5 y su test
  pertenecen ahí).
- **Documentos 11, 12, 15 y 20-23** — Humedales, Ríos y cuencas, Praderas y sabanas, y las
  transversales de biodiversidad, conectividad, ciclos naturales y agua y aire (documentos pendientes:
  a ellos pertenecen el hidroperiodo, el caudal ecológico, el fuego como ciclo, el área mínima viable
  y la calidad del agua y del aire).
- Índice de Salud Ecosistémica (**IN-01**, pesos y bandas del ISE) y Eficiencia de Preservación Vital
  (IN-02): [metricas_detalle_kpis_oraculos_dinamicos.md](../../architecture/metricas_detalle_kpis_oraculos_dinamicos.md)
- Estándar **SDV-S** completo y su comparativa inter-reinos: [SDV-S_Suelo_Dignidad_Vital_Sinteticos.md](../SDV-S_Suelo_Dignidad_Vital_Sinteticos.md)
- **SDV** como principio universal e INV2-S: [SDV_Suelo_Dignidad_Vital_importancia_MaxoContracts.md](../SDV_Suelo_Dignidad_Vital_importancia_MaxoContracts.md)
- Riesgos **R4**, **R6** y **R13**, y el blindaje anti-gamificación:
  [blindaje_anti_gamificacion_equidad.md](../../architecture/blindaje_anti_gamificacion_equidad.md)
- Diseño futuro del **PIU** (`valorar_ta_natural`, hoy un `pass` con comentario) y de los oráculos
  dinámicos: [DISENO_IMPLEMENTACION_FUTURA.md](../../architecture/DISENO_IMPLEMENTACION_FUTURA.md)

---

**Cierre.** Las tierras secas entran al SDV-E por la puerta más incómoda de la biblioteca: **son el
único ecosistema cuyo piso no es un número sino una fecha, cuyo estado de referencia no es verde, y
cuyo daño se paga con un tiempo que ninguna contabilidad humana alcanza.** Lo que este documento aporta
no son seis umbrales nuevos —solo cuatro reglas de su columna de Mínimo Absoluto están publicadas por un
organismo internacional, y el resto son `[HIPÓTESIS]` declaradas—, sino seis decisiones que la familia
del SDV no había tenido que tomar: **lo árido no es degradado**, **la sequía es un ciclo y no una
violación**, **la costra biológica es salud aunque se llame suelo desnudo**, **el contrapeso de la LDN
no es un mercado de compensaciones**, **la línea base es un acto político con fecha y certificante**, y
**ningún denominador contable puede ser más corto que el tiempo de recarga de lo que consume**. Todo lo
demás —unidades de duración, pesos, ventanas de reparación, quórums, umbrales de costras y de
irreversibilidad— queda dicho aquí como lo que es: **propuesta no ratificada**, pendiente de los
documentos 02, 03, 07, 08, 11, 12, 14, 15 y 20 de esta biblioteca y, en último término, del Parlamento.
Cuando el agua de un acuífero fósil se pierde, ninguna votación posterior la devuelve: por eso este
estándar prefiere declarar lo que no sabe antes que prometer lo que no puede medir.
