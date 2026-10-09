# SDV-A: el estándar de los animales
## Los mínimos del diseño biológico por especie: las ocho dimensiones genéricas del Cap. 9 §9.4, el Factor de Consciencia por niveles A/B/C/D, el arquetipo SDV-Gallinas y el Principio Precautorio de Consciencia — y el acoplamiento numérico por el que el techo del ecosistema condiciona la carga animal sin recortar el piso del animal

**Autoría:** Oráculo Sintético DeepSeek & Max Nelson López Restrepo
**Fecha:** octubre 2026
**Proyecto:** Maxocracia — El gobierno de la verdad, el tiempo y la vida
**Licencia:** Creative Commons BY-SA 4.0
**Estado:** Propuesta de estándar (rama SDV-E, Ola 4) — NO canon hasta ratificación
**Referencia canónica:** Cap. 10 §10.4 · Cap. 16.5 §16.5.14 · EVV-1.2 §4.3 · Cap. 9.5 (precedente SDV-S)
**Documento:** 30 de la biblioteca `docs/theory/SDV-E/` (Bloque D — reinos hermanos)
**Foco:** el estándar hermano del reino natural. Las ocho dimensiones genéricas del Cap. 9 §9.4 (Fase 2),
el Factor de Consciencia por niveles A/B/C/D (Cap. 9 §9.2.2), el arquetipo SDV-Gallinas (Cap. 9 §9.5),
el Principio Precautorio de Consciencia (Cap. 10 §10.3) y el acoplamiento numérico SDV-A ↔ SDV-E.
**Revisión:** octubre 2026 — documento redactado contra las fuentes verificadas de la rama
(`scratch/sdv_e/fuentes/30_sdva.md`), contra la lectura directa del capítulo del libro que hoy *es* el
SDV-A (Cap. 9, 317 líneas, leído completo), contra el código del repositorio (`maxocontracts/`, `app/`)
y contra los documentos 07, 08 y 09 de esta biblioteca. **No re-verifica umbrales externos: los consume**
y declara de dónde vienen. Los estados HTTP de las URLs citadas se recomprobaron en esta sesión:
**23 URL comprobadas — 20 responden 200, 2 responden 403 (reales, bloquean a los agentes automáticos) y
1 responde 404** (declarada como descartada en §14.7).

---

> **Advertencia de estado, antes de la primera línea de doctrina.** 🔴 **El SDV-A no tiene documento de
> estándar en `docs/theory`.** Existe como **capítulo de libro** (Cap. 9, edición 3.2 del 26 de enero de
> 2026, redactado en colaboración con Claude/Anthropic `[VERIFICADO]`), como **columna de las tablas
> comparativas de doce documentos de esta biblioteca**, y como **hueco matemático** en
> `app/vhv_calculator.py` —entendiendo «hueco» en su sentido literal: ahí existe una **firma con cinco
> argumentos y cero tablas**; ninguna parte de la arquitectura del reino animal está construida (§12)—.
> No existe tabla de especies, ni tabla de Factor de Consciencia, ni umbral
> implementado, ni invariante del reino animal. Este documento **no hereda un estándar: lo funda** —y todo
> lo que funda va marcado como **propuesta no ratificada**. Nada de lo que aquí se funda tiene piso
> **verificado por una fuente externa**: lo que este documento añade es forma —déficit, compuerta,
> estados, tests, protocolo—, y cada cifra nueva va con su marca.
>
> Y una segunda advertencia, que es la que sostiene la primera: el SDV-A **es el estándar hermano del
> reino natural, no su competidor ni su apéndice**. Un animal vive **dentro** de un ecosistema, y eso
> convierte la relación entre los dos estándares en una regla aritmética que este documento escribe con
> número: **el suelo del animal no puede ser mayor que el del ecosistema que lo sostiene** (§4.14).
>
> **Precisión de forma, para que la frase no se lea más de lo que dice.** El tope del ecosistema **no
> recorta el piso del animal** —el piso del individuo es LEY y no cede—: **limita la carga** (cuántos
> animales caben y cuánta superficie exterior se puede declarar, §4.14, reglas 1 a 3). Un «suelo del
> animal mayor que el del ecosistema» es exactamente la situación que el acoplamiento prohíbe; su
> resolución no es bajar el piso de nadie, sino reducir la actividad humana.

---

## 1. Qué es (y qué no es) este SDV

**Qué es.** Este documento fija el **estándar de los animales sintientes** dentro de la familia de Suelos
de Dignidad Vital que el canon reconoce: el SDV-H (humanos), el **SDV-A (animales)**, el SDV-E
(ecosistemas) y el SDV-S (sintéticos). Su tesis es una sola frase del Cap. 9 §9.1, y es una tesis
epistemológica, no sentimental: **cada especie tiene un diseño biológico que define sus necesidades
mínimas irrenunciables** `[VERIFICADO]`.

De esa tesis se derivan las cuatro piezas que este documento ordena, mide y —donde el canon no decidió—
propone:

1. **Las ocho dimensiones genéricas del Cap. 9 §9.4 (Fase 2):** espacio vital, alimentación natural,
   acceso a agua, luz y ritmos circadianos, socialización específica, libertad de movimiento, expresión
   del comportamiento natural y ausencia de crueldad. Genéricas en las dimensiones, **específicas en los
   umbrales por especie** (Cap. 9 §9.4, §9.9).
2. **El Factor de Consciencia por niveles A/B/C/D** (Cap. 9 §9.2.2), con sus dos funciones —alcance de la
   protección y peso en el cálculo del VHV— separadas, porque el canon las mezcla en una sola tabla.
3. **El arquetipo SDV-Gallinas** (Cap. 9 §9.5): los diez parámetros con Mínimo y Óptimo en columnas
   separadas, la fórmula de violación y los siete pesos dimensionales que suman 1,00.
4. **El Principio Precautorio de Consciencia** (Cap. 10 §10.3), que es el operador que gobierna el caso
   «en duda» — y que en este estándar no es una excepción, es una columna.

**Por qué existe este documento.** Por dos razones, y la segunda es la que le da su lugar en esta
biblioteca:

- **Porque el canon lo exige y no lo tiene.** El árbol de la Base de Datos Universal de SDV del Cap. 9
  §9.7 lista `SDV-A (Animales)` como rama de primer nivel, con subramas por taxón
  (`Mamíferos/Aves/Peces/Crustáceos`), y el Cap. 9 §9.10 convoca a etólogos, veterinarios y
  organizaciones de bienestar a desarrollarla. Hoy esa rama **tiene un capítulo y ningún estándar**.
  Este documento no cierra la rama: **abre su primer documento normativo**.
- **Porque el SDV-E no se puede cerrar sin él.** De los cuatro estándares, el SDV-E es **hijo
  epistemológico del SDV-A, no del SDV-H** (documento [09](09_Comparativa_inter_reinos.md), insight I1):
  comparten la **fuente del piso** —el diseño biológico y la etología— y comparten el **tiempo** —los dos
  viven en **TA (Tiempo Absoluto)**, nunca en TVI ni en TPI—. Y comparten una propiedad que ninguna tabla
  del canon dice junta: **en los dos, el sujeto no puede declarar su propio estado**. Lo que cambia es
  que el animal **sí tiene un tutor humano jurídicamente localizable** (documento 09 §11.2, eje 11) y el
  ecosistema no tiene a nadie con autoridad verificada.

**Qué no es.**

- **No es el estándar del ecosistema.** El SDV-E protege **una unidad ecológica** —un humedal, un río, un
  bosque— y sus parámetros son *condición por superficie y por tiempo* (% de cobertura, t·ha⁻¹·año⁻¹,
  °C-semanas). El SDV-A protege **individuos de una especie** y sus parámetros son *recurso por sujeto*
  (m²/animal, cm de percha/ave, aves/nido). **Un índice ecológico alto jamás promedia el sufrimiento de
  una gallina**, y un SDV-A cumplido jamás sustituye el piso del suelo: son **dos estándares sobre el
  mismo metro cuadrado** y ninguno absorbe al otro (documento [18](18_Ecosistemas_Agroecosistemas.md)
  §11.1, «doble jurisdicción»).
- **No es una lista de recomendaciones de bienestar.** Un estándar de esta familia tiene **piso con
  fuente, operador, protocolo y definición operativa de violación**. Una recomendación sin umbral no
  entra aquí como LEY: entra como POLÍTICA o no entra.
- **No es una copia de la ley vigente.** El canon es **más estricto que el derecho positivo verificado en
  tres lugares medibles** —el espacio vital del arquetipo (0,25 m²/ave frente a los 750 cm² de la jaula
  enriquecida de la UE), el 0 % de crueldad sin las excepciones escritas que la propia ley concede, y el
  0 % de crueldad como absoluto cuando las dos únicas prohibiciones absolutas verificadas traen
  excepción—. Este documento **cuantifica esa diferencia** en §5.6 en lugar de disimularla.
- **No es un apéndice del SDV-H.** El animal no tiene TVI (su tiempo es TA) y su piso no viene de la
  dignidad ni de las capacidades, sino del **diseño biológico** con el que la especie resolvió 3 800
  millones de años de selección natural (Cap. 9 §9.2.1) `[VERIFICADO]`. Trasvasar cifras del reino humano
  al animal es el error que el documento 09 §2 (Regla 2) prohíbe.
- **No está implementado.** 🔴 No existe tipo `SDV_A` en `maxocontracts/core/types.py`, no hay tabla de
  especies, no hay tabla de FC, no hay bloque validador con parámetros animales. La tabla de estado real
  está en §12, y **no se afirma en ninguna línea de este documento que algo de eso exista**.
- **No es canon.** Es una propuesta de estándar de la rama SDV-E, Ola 4, **no ratificada**.

**Las cuatro marcas de evidencia, y por qué la cuarta es un resultado.**
`[VERIFICADO]` = leído por herramienta en la sesión de verificación de fuentes de esta rama, leído
directamente en el archivo citado, o comprobado por HTTP en esta sesión. `[REPORTADO]` = afirmado por la
fuente citada sin haber podido abrir el documento completo. `[HIPÓTESIS]` = inferencia razonada del
proyecto, no observación. `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` = se buscó el
número y no existe fuente verificable. En el SDV-A la cuarta marca aparece
**en veinticinco sitios de este documento** (recuento directo sobre el archivo, no comparación con el
resto de la biblioteca: otros documentos la usan más veces), y eso apunta al hallazgo central de §5.6:
**el canon de los animales fija pisos que la ley no fija, y la ley fija pisos que el canon no midió.**

---

## 2. Preámbulo metodológico

El SDV-H lo tiene y el SDV-S lo omitió; el brief de esta biblioteca prohíbe repetir la omisión. En el
SDV-A el preámbulo cumple además una función específica: **es el único estándar de la familia cuyo
canon publica números que la fuente externa no respalda**, de modo que sin reglas de lectura explícitas
el documento se leería como si heredara un piso verificado cuando en realidad **funda uno**.

**Regla 1 — Separar «describir el canon» de «ratificar el estándar».** Este documento distingue tres
cosas y ninguna se disfraza de otra: (a) lo que el canon manda, citado por sección (Cap. 9 §9.4, §9.5,
§9.2.2); (b) lo que la ley y la ciencia verificadas publican, con organismo, año y URL; (c) lo que este
documento propone —marcado `[HIPÓTESIS]` o **propuesta no ratificada**—. La tercera categoría es la más
grande de las tres, y decirlo es parte del trabajo.

**Regla 2 — Ningún número entra sin fuente, y ninguno se rellena por plausibilidad.** Donde la ciencia no
publica un valor, el parámetro entra **declarado y sin piso ejecutable**, con la marca
`[SIN FUENTE VERIFICADA — pendiente de consenso científico]`. Sustituir ese vacío por un número
plausible sería exactamente el fraude que este estándar existe para impedir: **un piso inventado no
protege al animal, protege al operador.**

**Regla 3 — Mínimo Absoluto y Óptimo son dos columnas y dos regímenes jurídicos.** El piso es **LEY** y
**no se vota**; la plenitud aspiracional es **POLÍTICA** y **se vota** (precedente del Parlamento
Educativo, INV2-EDU: categoría `critical`, quórum 60 %, consenso 75 %, T13, anti-flip-flop de 14 días,
`CHECK` en base de datos). El motor del SDV-H confundió el Óptimo del agua con el Mínimo Absoluto y el
brief prohíbe repetir ese error; aquí las dos columnas van separadas **incluso cuando la segunda está
vacía** —que es el caso de casi todas las dimensiones del SDV-A (Cap. 9 §9.5 las publica, pero §5.6 de
este documento documenta que **ninguna tiene fuente externa verificada**).

**Regla 4 — El error del SDV-H se repite aquí al revés, y hay que nombrarlo.** En el SDV-H el motor tomó
el Óptimo por el Mínimo. En el SDV-A el riesgo es **simétrico y de otra forma**: el canon **inventa la
unidad de medida** donde la fuente verificable da otra. El caso canónico: el Cap. 9 §9.5 mide el agua en
**litros por día** (mínimo 0,3 · óptimo 0,5) y **ninguna fuente oficial verificada mide agua por ave en
litros**: la ley mide **puntos de acceso** (2,5 cm de bebedero por ave; una tetina o copa por cada diez
aves). No es un error de cifra: es un **error de unidad**, y una cifra con la unidad equivocada no se
puede medir ni auditar. Este documento lo corrige **proponiendo**, no reescribiendo el canon (§4.4,
§5.5).

**Regla 5 — Todo lo formal debe ser falsable por un test.** Cada propiedad de §5.7 tiene un test
nombrado. Una propiedad sin test es una intención, y en un estándar que hoy **no tiene ni una línea de
código** (§12) la diferencia entre propiedad y promesa es todo el documento.

**Regla 6 — El tiempo del animal es TA soberano.** Los dos estándares biológicos —animal y
ecosistema— viven en **Tiempo Absoluto**; el **PIU** (Protocolo de Intercambio Universal, Cap. 5 §5.5) es
el **único** traductor TA↔TVI, y **la traducción ocurre fuera de la fórmula**: una violación del SDV-A
expresada en TVI describiría el tiempo del animal con la unidad del tiempo humano, que es la forma exacta
de la colonización temporal que el canon prohíbe (Cap. 16.5 §16.5.14; documento
[03](03_No_colonizacion_del_TA.md) §11).

**Regla 7 — Admisión de la duda, con su inversión declarada.** *«La duda sin evidencia no castiga»*
(INV2-EDU) protege al presunto vulnerado cuando no hay medición. En el SDV-A el presunto vulnerado **es
el animal**, y quien reporta es **el tenedor** —el beneficiario de su uso—: la regla, aplicada sin
corrección, protegería a la parte que tiene el incentivo de no medir. La corrección que este documento
propone es la que el documento [08](08_INV2-E_invariante.md) §6.3 fijó para el ecosistema y que aquí
aplica **en su forma intermedia**: la ausencia de dato **no imputa violación** al animal y **tampoco
certifica cumplimiento**; activa una **obligación de instrumentar** sobre quien pretende operar. Y el
canon no se negocia por ausencia de dato: *«mientras no haya resolución, el canon manda»*.

**Regla 8 — El canon se cita por capítulo y sección, nunca por línea.** `Cap. 9 §9.5`, `Cap. 10 §10.3`,
`EVV-1.2 §4.3`. Sin anclas de línea y sin rutas absolutas locales: una cita que depende del número de
línea deja de ser cierta en la siguiente edición del libro.

---

## 3. Pilares epistemológicos

Once pilares. Los siete primeros son comunes a la familia de estándares y este documento los hereda sin
modificarlos; los cuatro últimos son **específicos del SDV-A** y son los que explican por qué este
documento existe.

**Los comunes.**

1. **T14 — Principio de Precaución Intergeneracional** (Cap. 5). *«Ante incertidumbre sobre el impacto en
   agentes que no pueden consentir (ecosistemas, generaciones futuras, posibles consciencias sintéticas),
   el sistema debe elegir la opción de menor irreversibilidad, documentando el costo de oportunidad
   asumido. La carga de la prueba recae sobre quien propone acciones que afectan la temporalidad de
   no-participantes.»* Es el axioma más fuerte disponible para el SDV-A: **bloquea sin necesidad de
   umbral**, y por eso es la única herramienta operativa en las cinco dimensiones del arquetipo que hoy
   no tienen piso con fuente (§5.6), y **lo que T14 bloquea es la autorización, no el hecho**: donde no
   hay umbral, no hay vía de autorizar a ciegas lo irreversible (§8.3, bloqueo precautorio).
2. **El Principio Precautorio de Consciencia** (Cap. 10 §10.3): *«Donde hay duda de consciencia, se asume
   consciencia.»* En este estándar no es una cláusula de estilo: es **el operador del nivel C** del Factor
   de Consciencia (§4.9), el estado `EN DUDA` que decide si un ser entra o no en el ámbito de protección.
3. **T9 — No-antropocentrismo.** El estándar protege **sujetos**, no administra **recursos**. Consecuencia
   de ingeniería, heredada del documento 08 §8.7: **el objeto de la consecuencia nunca es el animal**; es
   la actividad humana que lo afecta.
4. **Axioma 0 — Directiva Mayor:** *«resolver nuestras necesidades de la mejor manera para todos todos»*
   —los **tres reinos**: humanos, naturales y sintéticos, **presentes y futuros**—. El SDV-A es la pieza
   que impide que el reino que **no firma con manos** quede fuera de la contabilidad por no poder
   reclamar (documento 08 §3, pilar 7).
5. **T13 — Transparencia de Cálculo.** *La contabilidad nunca se borra.* Aplicado a este estándar: una
   violación medida se registra aunque se repare; y una violación **no medida** también se registra como
   vacío de cobertura (Regla 7). El perdón, cuando exista, modula la consecuencia y **jamás** el registro.
6. **Dignidad encadenada** (Cap. 10 §10.6): *«Dignidad Humana ←→ Dignidad Ecosistémica ←→ Dignidad
   Material. Cada eslabón depende de los demás.»* Consecuencia para el SDV-A: cuando el piso del animal
   cae, el bloqueo no es un favor al animal, es la defensa del propio conjunto humano que lo consume.
7. **Gobernanza operacionalmente finita** (Cap. 10 §10.7): *«La gobernanza debe ser operacionalmente
   finita.»* El SDV-A no modela la etología completa de una especie para decidir: usa **un catálogo
   cerrado de parámetros** por especie, con operador y umbral. Un estándar que exige un etograma completo
   por especie es inaplicable, y lo inaplicable no protege.

**Los específicos del SDV-A.**

8. **El piso viene del diseño biológico, no de la dignidad.** «Diseño biológico + Etología» es la base
   epistemológica que el propio canon declara para el SDV-A, frente a «Dignidad intrínseca +
   Capacidades» del SDV-H (Cap. 9 §9.9) `[VERIFICADO]`. Y el Cap. 9 §9.2.1 le da su fundamento fuerte:
   el ADN es un token no fungible que representa **una solución única en una secuencia evolutiva de 3 800
   millones de años**; violar el diseño biológico de una especie no es solo crueldad, es **destruir
   patrimonio evolutivo** `[VERIFICADO]`. De ahí una consecuencia que el estándar debe sostener: **el piso
   del SDV-A es una afirmación sobre la especie, no un promedio de lo que la industria tolera.**
9. **La definición de bienestar que este estándar usa no es propia: es la de la WOAH.** *«the physical
   and mental state of an animal in relation to the conditions in which it lives and dies»*
   `[VERIFICADO]`. Dos consecuencias de forma, y las dos son duras: (a) el bienestar incluye **los
   estados mentales**, de modo que un parámetro puramente físico no agota la dimensión; (b) incluye **el
   morir**, y por eso la dimensión 8 (ausencia de crueldad) **no puede excluir el sacrificio** — el
   estándar del animal es el único de la familia que debe normar su propia muerte (§4.8).
10. **Las ocho dimensiones del canon no son las cinco libertades, y hay que decir cuál es cuál.** Las
    cinco libertades de la WOAH (1965) —hambre y sed; miedo y angustia; estrés térmico o incomodidad
    física; dolor, lesión y enfermedad; **expresión de patrones normales de comportamiento**
    `[VERIFICADO]`— cubren **cinco** de las ocho dimensiones del Cap. 9 §9.4 (alimentación, agua,
    espacio/térmica, crueldad y comportamiento natural). **Las otras tres —luz y ritmos circadianos,
    socialización específica y libertad de movimiento— son aportación propia del canon** y no derivan de
    la WOAH. Esto importa para la trazabilidad: cuando este documento no encuentra fuente para la
    dimensión 4, no está fallando la WOAH: está fallando **una dimensión que el canon añadió**.
11. **La asimetría del que reporta: el tenedor es el beneficiario.** En el SDV-H el sujeto declara su
    propio estado; en el SDV-S la instancia registra su bitácora; en el SDV-E **nadie puede reportar**. El
    SDV-A es el **caso intermedio y el más incómodo de los cuatro**: el animal no reporta y quien reporta
    por él —el tenedor, o la entidad certificadora que él paga— **se beneficia de que el resultado sea
    favorable** (documento 09 §11.2, eje 7: *«riesgo principal: conflicto de interés del tutor»*). Ese
    conflicto no se resuelve con buena voluntad: se resuelve con **fuentes de datos independientes del
    tenedor**, y esa es la exigencia que §6 y §7 de este documento desarrollan.

---

## 4. Dimensiones del SDV-E y dimensiones del SDV-A: las ocho genéricas del Cap. 9 §9.4

Esta sección es el corazón del documento. Empieza por la frontera entre los dos estándares (4.1), fija
cómo se lee una dimensión (4.2 y 4.3), desarrolla las **ocho dimensiones** una por una (4.4 a 4.11), y
cierra con las tres piezas que el foco de este documento exige: el **Factor de Consciencia** (4.12), el
**arquetipo SDV-Gallinas** (4.13) y el **acoplamiento numérico con el SDV-E** (4.14).

### 4.1 La frontera: dos estándares sobre el mismo metro cuadrado

Antes de cualquier umbral hay que fijar de quién es cada piso, porque **el SDV-A y el SDV-E se aplican al
mismo territorio** y el error de atribución es la forma más fácil de vaciar los dos.

| | **SDV-A** — el animal | **SDV-E** — la unidad ecológica |
|---|---|---|
| **Sujeto** | El individuo de una especie sintiente (y la población como portadora de diversidad genética) | La ocurrencia ecológica delimitada (documento [02](02_Unidad_y_sujeto_del_SDV-E.md), C1-C5) |
| **Parámetro típico** | Recurso **por sujeto**: m²/animal, cm de percha/ave, aves/nido, L/día, h/día | Condición **por superficie y por tiempo**: % de cobertura, kg N/ha/año, t·ha⁻¹·año⁻¹, caudal en % del flujo medio |
| **Tiempo** | **TA**, traducido por el PIU (Cap. 5 §5.5) | **TA**, traducido por el PIU |
| **Fuente del piso** | Diseño biológico + etología científica (Cap. 9 §9.3, §9.9) | Diseño biológico **del ecosistema** (Cap. 16.5 §16.5.14) |
| **Representación** | La persona o el **tutor legal** (documento 09 §11.2) | Parte `eco-*` + guardián oráculo |
| **Factor** | Tabla escalonada: 0,2 · 0,5 · 1,0 · 2,0 · ∞ (prohibición de mercado) | `FE = e^(min(Σ FI·v·Δt, V_max))`, base neutra 1,0 (documento [07](07_Formula_de_violacion_y_pesos.md) §5.4) |
| **Naturaleza del factor** | **Precio del consumo** (con cumplimiento pleno vale 0,2, no 1,0) | **Penalización de la violación** (con violación 0 vale 1,0 exacto) |
| **Invariante** | `SDVValidator` con parámetros por especie 🟡 | **INV2-E** 🔴 no existe |
| **Remedio tras la violación** | **Prohibición de mercado** si la violación es sistemática | **Ninguno**: el TA del bosque no se compra de vuelta |

**La regla de atribución, en una frase:** *el animal tiene un piso por individuo y el ecosistema tiene un
piso por superficie; ninguno de los dos se deduce del otro.* Un gallinero es simultáneamente un
agroecosistema (suelo, agua, márgenes, estiércol, diversidad) y un conjunto de individuos con SDV-A
propio; **el índice ecológico no promedia el sufrimiento de una gallina y el SDV-A no autoriza a cruzar
el piso del suelo** (documento 18 §11.1). `[HIPÓTESIS]` en la formulación; los dos estándares son canon.

### 4.2 Cómo se lee una dimensión de este estándar

Cada una de las ocho dimensiones trae cinco piezas, y las cinco son obligatorias:

- **Qué protege.** Una frase, sin adjetivos.
- **Tabla de parámetros** con dos columnas separadas —**Mínimo Absoluto (el piso, LEY, no votable)** y
  **Óptimo (plenitud aspiracional, POLÍTICA, votable)**— y la fuente de cada cifra. La marca `—` significa
  **que la fuente no define ese extremo**, y no es un hueco de redacción: es el hallazgo estructural de
  esta sección (§4.3).
- **Justificación.** Por qué ese mínimo y no otro, con la fuente citada.
- **Protocolo.** Cómo se mide —instrumento, unidad, frecuencia— y quién reporta.
- **Violación.** Qué observación concreta constituye violación: **un hecho, no una opinión**.

### 4.3 El hallazgo estructural de esta sección: el derecho animal fija pisos y casi nunca óptimos

De las ocho dimensiones, **seis no tienen un solo Óptimo con fuente externa verificada** y las dos
restantes lo tienen **solo como nivel de certificación ecológica**, que es una categoría comercial, no
una plenitud científica. La razón es la misma que el documento 07 §4.3 documentó para el ecosistema, y
aquí es más radical: **la ciencia y el derecho publican umbrales de daño, no plenitudes.** Lo que existe
en el derecho de bienestar animal son **pisos exigibles** y **etiquetas de nivel superior** (producción
ecológica). Las dos únicas parejas piso/plenitud con fuente real que se pudieron verificar en esta rama
son:

| Parámetro | Piso con fuente | Nivel superior con fuente | Ratio | Fuente |
|---|---|---|---|---|
| Espacio de la ponedora (sistemas alternativos) | **750 cm²/ave** (jaula enriquecida) | **1 667 cm²/ave** (= 6 aves/m², ecológico interior) | **2,22×** `[VERIFICADO]` | UE, Directiva 1999/74/CE art. 6 · Reglamento (CE) 889/2008 anexo III |
| Percha de la ponedora | **15 cm/ave** | **18 cm/ave** (ecológico) | **1,20×** `[VERIFICADO]` | UE, Directiva 1999/74/CE art. 4.1(d) · Reglamento (CE) 889/2008 anexo III |

Dos consecuencias que hay que escribir sin rodeos:

1. **La columna del Óptimo del Cap. 9 §9.5 (0,75 m² · 12 h · 0,5 L · 60 % dieta · 10 h de luz · 25
   aves/grupo) no tiene fuente externa verificada en esta sesión.** Es POLÍTICA, y así debe declararse.
   El documento 09 §11.6 ya detectó la heurística que la generó —**«el Óptimo es 2-3× el Mínimo»**— y la
   marcó como **heurística de calibración, no ley**. El único par verificado de la tabla (2,22×) **es
   compatible** con esa heurística, y eso es todo lo que se puede decir: compatible, no confirmado.
2. **Que el Óptimo esté vacío refuerza la separación de regímenes en lugar de debilitarla.** Lo que no es
   dato es, por definición, lo que se delibera: **el Óptimo del SDV-A no se investiga, se vota.**

### 4.4 Dimensión 1: Espacio vital (el cuerpo necesita un sitio que no sea una celda)

**Qué protege.** La superficie y el volumen mínimos por animal por debajo de los cuales el movimiento, la
termorregulación y las conductas de descanso y huida se vuelven imposibles, con independencia de que el
animal siga produciendo.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| Ponedora — jaula convencional | **550 cm²/ave — PROHIBIDA**: la cría en estas jaulas está vetada desde el 1-1-2012 | — | UE, Directiva 1999/74/CE art. 5 (1999) |
| Ponedora — jaula enriquecida (piso legal vigente) | **750 cm²/ave** (≥ 600 utilizables; altura ≥ 20 cm; ninguna jaula < 2 000 cm²) | `[SIN FUENTE VERIFICADA]` | UE, Directiva 1999/74/CE art. 6 (1999) |
| Ponedora — sistemas alternativos (suelo/aviario) | **9 aves/m²** de área usable = **1 111 cm²/ave** | `[SIN FUENTE VERIFICADA]` | UE, Directiva 1999/74/CE art. 4.1.4 (1999) |
| Ponedora — ecológico, interior | **6 aves/m²** = **1 667 cm²/ave** | — | UE, Reglamento (CE) 889/2008 anexo III pt. 2 (2008) |
| Ponedora — ecológico, superficie exterior | **4 m²/ave** en rotación, **condicionados** a que no se superen 170 kg N/ha/año | — | UE, Reglamento (CE) 889/2008 anexo III pt. 2 (2008) |
| Ternero (< 6 meses) alojado en grupo | **1,5 m²** (< 150 kg) · **1,7 m²** (150-220 kg) · **1,8 m²** (≥ 220 kg) | — | UE, Directiva 2008/119/CE art. 3.1(b) (2008) |
| Cerdo en cebo — superficie libre de obstáculos | **0,55 m²** (50-85 kg) · **0,65 m²** (85-110 kg) · **1,0 m²** (> 110 kg) | — | UE, Directiva 2008/120/CE art. 3.1(a) (2008) |
| Cerda gestante / cerda joven en grupo | **2,25 m²** · **1,64 m²** | — | UE, Directiva 2008/120/CE art. 3.1(b) (2008) |
| Vaca lechera — ecológico | **6 m²** interior · **4,5 m²** exterior | — | UE, Reglamento (CE) 889/2008 anexo III pt. 1 (2008) |
| Peces — carga en acuicultura ecológica | **15 kg/m³** (salmónidos no listados) · **20** (salmón) · **25** (trucha común y arcoíris) · **10** (salmónidos en mar, jaulas) | — | UE, Reglamento (CE) 889/2008 anexo XIIIa §§1-2 (2009) |
| Peces — estanques de tierra en zonas de marea y lagunas costeras | **4 kg/m³** | — | UE, Reglamento (CE) 889/2008 anexo XIIIa §4 (2009) |
| Camarones peneidos | **240 g/m²** de biomasa instantánea máxima · siembra **22 postlarvas/m²** | — | UE, Reglamento (CE) 889/2008 anexo XIIIa §7 (2009) |
| Cangrejo de río — densidad por talla | **100 individuos/m²** (< 20 mm) · **30** (20-50 mm) · **10** (> 50 mm, con escondites) | — | UE, Reglamento (CE) 889/2008 anexo XIIIa §7a (2014) |
| **Gallina ponedora — parámetro del canon** | **0,25 m²/ave** (= 2 500 cm²) — **decisión del proyecto, sin fuente externa verificada** | **0,75 m²/ave** (= 7 500 cm²) — `[SIN FUENTE VERIFICADA]` | Cap. 9 §9.5 `[VERIFICADO]` |

**Justificación, y la cifra que hay que mirar dos veces.** El canon fija **0,25 m²/ave = 2 500 cm²**
(Cap. 9 §9.5). Ese número no es un mínimo legal heredado: es **3,33× el piso legal vigente de la UE**
(750 cm², jaula enriquecida) y **1,5× el piso ecológico interior** (1 667 cm²) `[VERIFICADO]`. Es decir:
**el canon del SDV-A no copia la ley, la excede** — y por eso este documento no puede presentar el 0,25
como «estándar internacional», sino como **decisión del proyecto** `[HIPÓTESIS]`. Su Óptimo (0,75 m²) es
exactamente **3× su propio Mínimo**, y coincide con la heurística 2-3× del documento 09 §11.6.

**Contradicción interna del canon, detectada y no resuelta aquí.** El paper de Ontometría Vital fija
`SDV_Espacio_Vital ≥ 0,75 m²/gallina` como **umbral del SDV** —es decir, como **piso**—, mientras el
Cap. 9 §9.5 fija **0,25 como Mínimo y 0,75 como Óptimo** para el mismo parámetro y la misma especie
`[VERIFICADO]` (lectura directa de `docs/theory/tercer_paper_ontometria_vital_huevo.md` §2.2.4). Los dos
textos están en el repositorio y **se contradicen en cuál de los dos números es el piso**. Este documento
**no elige desde aquí**: registra la contradicción como pregunta abierta (§13, pregunta 2) y conserva el
número del canon como referencia, porque cambiarlo por decisión de un documento de biblioteca sería
exactamente lo que la Regla 1 prohíbe.

**Protocolo.** Superficie **usable** libre de obstáculos por animal, en m²/animal o cm²/ave, medida sobre
plano o por medición directa; se registran además la altura libre (jaulas: ≥ 20 cm; sistemas de varios
niveles: ≥ 45 cm entre niveles, §4.9) y el número de niveles (máx. 4). Frecuencia: **una vez por ciclo de
producción** y **en cada cambio de lote**; el área no cambia sola, pero la **densidad efectiva** sí
(mortalidad, retirada de aves). Quien reporta: el tenedor con verificación de la entidad certificadora
(§6.3), nunca el tenedor solo (Regla 7).

**Violación.** Observación concreta: **la superficie usable por animal medida es inferior al piso
declarado**, o existe jaula convencional (prohibida) en uso, o el número de niveles excede el máximo, o la
superficie exterior ecológica se computa sin que se cumpla la condición de 170 kg N/ha/año (§4.14). Es un
hecho medible con una cinta métrica y un plano: no requiere interpretación.

### 4.5 Dimensión 2: Alimentación natural (comer lo que la especie come, no lo que la engorda)

**Qué protege.** El acceso a una dieta adecuada a la fisiología de la especie —cantidad, calidad, origen
y ausencia de manipulaciones que fuercen el cuerpo— y la prohibición de las prácticas alimentarias que
causan sufrimiento directo.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| Origen del pienso (ecológico) | Del propio predio o de unidades ecológicas/en conversión **de la misma región** — obligatorio | — | UE, Reglamento (UE) 2018/848 anexo II parte II pt. 1.4.1(a) (2018) |
| Alimentación forzada (*force-feeding*) | **Prohibida** | — | UE, Reglamento (UE) 2018/848 anexo II parte II pt. 1.4.1(d) (2018) |
| Pienso de conversión admisible en la ración | ≤ **25 %** de media de la fórmula (hasta 100 % si procede del propio predio) | — | UE, Reglamento (UE) 2018/848 anexo II parte II pt. 1.4.3.1 (2018) |
| Acceso permanente a pasto (no aplica a porcino, aves de corral ni abejas: éstos, acceso permanente a forraje) | Obligatorio cuando las condiciones lo permitan | — | UE, Reglamento (UE) 2018/848 anexo II parte II pt. 1.4.1(e) (2018) |
| Promotores del crecimiento y aminoácidos sintéticos | **No se usan** | — | UE, Reglamento (UE) 2018/848 anexo II parte II pt. 1.4.1(f) (2018) |
| Retirada de pienso antes del sacrificio (pollos de engorde) | **Máx. 12 h** antes de la hora prevista de sacrificio | — | UE, Directiva 2007/43/CE anexo I pt. 2 (2007) |
| Ayuno de peces antes del sacrificio | «No más de lo necesario» (regla cualitativa, sin cifra) | — | WOAH/OIE, Código Sanitario para los Animales Acuáticos cap. 7.3 art. 7.3.5.2.7 |
| **«% de dieta natural» — parámetro del canon** | **30 %** — `[SIN FUENTE VERIFICADA]` | **60 %** — `[SIN FUENTE VERIFICADA]` | Cap. 9 §9.5 `[VERIFICADO]`; ninguna fuente verificada define un porcentaje de «dieta natural» |

**Justificación.** La dieta es la dimensión donde el estándar corre el mayor riesgo de **confundir
bienestar con productividad**: un animal puede ganar peso y sufrir carencias. Por eso el piso verificable
no es un porcentaje de «naturalidad» —figura que ningún organismo define— sino **el origen del alimento**
(propio predio o región: el animal **no puede desacoplarse** de la unidad ecológica que lo sostiene) y
**las prohibiciones**: alimentación forzada, promotores del crecimiento, aminoácidos sintéticos. Es la
misma lección que la dimensión del agua (§4.6): **donde la fuente verificable da origen y prohibición, el
canon da un porcentaje, y el porcentaje no tiene fuente**.

**Protocolo.** Composición de la ración (materias primas y proporción de pienso en conversión) declarada
por el tenedor y verificada por la entidad certificadora con **trazabilidad de origen**; registro de
prohibiciones (forzado, promotores) como **declaración con evidencia documental** (facturas, albaranes,
certificado); para la retirada de pienso, **hora de retirada y hora prevista de sacrificio** en el
registro del matadero. Frecuencia: por lote y por ciclo.

**Violación.** Hechos observables: **alimentación forzada practicada**; uso de promotores del crecimiento
o aminoácidos sintéticos; pienso de conversión por encima del 25 % de media; retirada de pienso superior a
12 h en pollos de engorde; ausencia de acceso permanente a pasto/forraje cuando las condiciones lo
permiten; o pienso que **no procede del propio predio ni de unidades ecológicas de la misma región**. El
parámetro «30 % de dieta natural» del canon **no puede generar violación hoy**: no tiene fuente, y sin
definición operativa de violación no hay violación (documento 09 §6). Se registra y **no se imputa**.

### 4.6 Dimensión 3: Acceso a agua (la fuente mide grifos, el canon mide litros)

**Qué protege.** El acceso **permanente y suficiente** a agua limpia y fresca, y —en el caso de los
animales acuáticos— la calidad fisicoquímica del medio del que no pueden salir.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| Ponedoras — bebedero continuo | **2,5 cm** de longitud de bebedero por ave (o **1 cm/ave** en bebederos circulares) | — | UE, Directiva 1999/74/CE art. 4.1(b) (1999) |
| Ponedoras — tetinas o copas | **1 por cada 10 aves** (≥ 2 al alcance de cada ave si están conectadas a la red) | — | UE, Directiva 1999/74/CE art. 4.1(b) (1999) |
| Peces de acuicultura ecológica — oxígeno disuelto | **≥ 60 %** de saturación de O₂ | — | UE, Reglamento (CE) 889/2008 anexo XIIIa §1 (2009) |
| Aves de corral — agua limpia y fresca | Obligatorio, **sin cifra** (regla cualitativa) | — | FAO, *Gateway to poultry production and products* — Animal welfare: *«Other common welfare concerns are poor nutrition and lack of access to clean, cool water»* `[VERIFICADO]` |
| **Agua de bebida — volumen: parámetro del canon** | **0,3 L/ave/día** — `[SIN FUENTE VERIFICADA]` | **0,5 L/ave/día** — `[SIN FUENTE VERIFICADA]` | Cap. 9 §9.5 `[VERIFICADO]`; **ni la FAO, ni la WOAH, ni la legislación de la UE fijan L/ave/día** |

**Justificación, y la lección de forma más importante de esta sección.** La dimensión «agua» del SDV-A
**no se mide en litros en ninguna fuente oficial**: se mide en **puntos de acceso por ave** y, para los
peces, en **saturación de oxígeno**. La ley regula **acceso**, no consumo. La cifra 0,3-0,5 L/ave/día del
Cap. 9 §9.5 es `[SIN FUENTE VERIFICADA]`, y no es un detalle: es el **mismo error de forma** que el brief
advierte para el SDV-H (confundir el óptimo con el mínimo), pero **al revés** — aquí el canon **inventa la
unidad** donde la fuente verificable da otra. **Propuesta no ratificada de este documento:** el piso de
esta dimensión se escribe **en puntos de acceso** (2,5 cm de bebedero/ave; 1 tetina/10 aves; ≥ 60 % de
saturación de O₂ en acuicultura), y el volumen en L/ave/día se conserva como **parámetro informativo sin
piso** hasta que exista fuente que lo respalde.

**Protocolo.** Longitud de bebedero y número de tetinas/copas **medidos sobre plano y verificados en
visita**; caudal y temperatura del agua como dato complementario; para peces, **oxígeno disuelto en % de
saturación** con sonda in situ, frecuencia al menos **una vez por ciclo de producción** y **en el momento
de mayor carga** (biomasa máxima), no en el mejor momento del día.

**Violación.** Hechos observables: **menos de 2,5 cm de bebedero por ave**; **menos de una tetina o copa
por cada diez aves**; ausencia de acceso continuo al agua durante el ciclo; **saturación de oxígeno
inferior al 60 %** en el agua de cultivo de peces ecológicos; o agua que la propia FAO describe como
condición de bienestar deficitaria (sucia, caliente). El parámetro en litros del canon **no puede generar
violación hoy**: se registra y no se imputa.

### 4.7 Dimensión 4: Luz y ritmos circadianos (la dimensión que el canon añadió y la ley solo midió en una especie)

**Qué protege.** La alternancia previsible de luz y oscuridad que sincroniza el ritmo circadiano, la
posibilidad de dormir un período ininterrumpido y la intensidad luminosa suficiente para ver y
orientarse.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| Pollos de engorde — intensidad de luz | **≥ 20 lux** a la altura del ojo del ave, iluminando **≥ 80 %** del área usable | — | UE, Directiva 2007/43/CE anexo I pt. 6 (2007) |
| Pollos de engorde — oscuridad en el ciclo de 24 h | **≥ 6 h** en total, con **≥ 1 período ininterrumpido de ≥ 4 h** (excluidos los períodos de atenuación) | — | UE, Directiva 2007/43/CE anexo I pt. 7 (2007) |
| Ponedoras — horas de luz/oscuridad | `[SIN FUENTE VERIFICADA]` | `[SIN FUENTE VERIFICADA]` | **La Directiva 1999/74/CE no fija horas de luz ni de oscuridad para ponedoras** |
| **«Luz natural» — parámetro del canon** | **6 h/día** — `[SIN FUENTE VERIFICADA]` | **10 h/día** — `[SIN FUENTE VERIFICADA]` | Cap. 9 §9.5 `[VERIFICADO]`; ninguna fuente verificada exige **luz natural** |

**Justificación.** Esta es una de las **tres dimensiones que el canon añadió** y que no derivan de las
cinco libertades de la WOAH (§3, pilar 10): por eso el vacío de fuente es más agudo y más esperable. Lo
que sí está verificado es la **oscuridad** —el único umbral numérico de ritmo circadiano verificado en
esta rama: ≥ 6 h, con un tramo ininterrumpido de ≥ 4 h— y la **intensidad** (≥ 20 lux sobre ≥ 80 % del
área), y **las dos son de pollos de engorde**. El documento declara la consecuencia sin adornos:
**extrapolar de pollos de engorde a ponedoras es `[HIPÓTESIS]`**, y esa extrapolación debe ir marcada en
cada uso. La alternativa —dejar la dimensión sin cifra— es más honesta y menos protectora; la propuesta de
este documento es usarla **como piso precautorio declarado como extrapolación**, no como piso verificado
para la especie.

**Protocolo.** Luxómetro **a la altura del ojo del animal**, en varios puntos del área y en el momento de
mayor y de menor iluminación; registro horario del programa de luz (encendido, apagado, atenuaciones) y
cálculo de **horas de oscuridad totales** y del **tramo ininterrumpido máximo**; si hay acceso exterior,
horas de luz natural efectivas. Frecuencia: **una vez por ciclo de producción**, con verificación del
programa de luz en cada visita.

**Violación.** Hechos observables: **oscuridad total inferior a 6 h** o **ausencia de un tramo
ininterrumpido de al menos 4 h** (en las especies para las que el umbral se declara aplicable);
**intensidad inferior a 20 lux** sobre más del 20 % del área usable; **luz continua** sin período de
oscuridad. Para ponedoras, la violación solo puede declararse si la comunidad de custodia ha ratificado
la extrapolación como piso; si no, el parámetro se registra y **no se imputa**.

### 4.8 Dimensión 5: Socialización específica (la especie decide con quién y cuántos)

**Qué protege.** La posibilidad de establecer y mantener las relaciones sociales propias de la especie
—contacto visual y táctil, grupo estable, recursos sociales suficientes (nido)— y la prohibición del
aislamiento que la especie no tolera.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| Terneros — prohibición de corral individual | **Prohibido** confinar en corral individual **después de las 8 semanas** de edad (salvo certificación veterinaria por salud o comportamiento) | — | UE, Directiva 2008/119/CE art. 3.1(a) (2008) |
| Terneros — contacto social mínimo en corral individual | Paredes **perforadas** que permitan contacto **visual y táctil** directo (excepto aislamiento de enfermos) | — | UE, Directiva 2008/119/CE art. 3.1(a) (2008) |
| Cerdas y cerdas jóvenes — alojamiento en grupo | En grupo desde **4 semanas tras la cubrición** hasta **1 semana antes** del parto previsto | — | UE, Directiva 2008/120/CE art. 3.4 (2008) |
| Cerda / cerda joven — umbral de tamaño de grupo (**el único umbral de grupo verificado**) | Grupos de **< 6 individuos**: **+10 %** de superficie · grupos de **≥ 40**: **−10 %** | — | UE, Directiva 2008/120/CE art. 3.1(b) (2008) |
| Ponedoras — nido | **1 nido por cada 7 aves**; si es nido colectivo, **1 m² por un máximo de 120 aves** | — | UE, Directiva 1999/74/CE art. 4.1(c) (1999) |
| Ponedoras — nido (ecológico) | **7 aves/nido**, o **120 cm²/ave** en nido común | — | UE, Reglamento (CE) 889/2008 anexo III pt. 2 (2008) |
| **Gallinas por grupo — parámetro del canon** | **5 aves/grupo** — `[SIN FUENTE VERIFICADA]` | **25 aves/grupo** — `[SIN FUENTE VERIFICADA]` | Cap. 9 §9.5 `[VERIFICADO]`; **no existe umbral normativo de tamaño de grupo para ponedoras en las fuentes abiertas** |

**Justificación.** «Socialización específica» significa que **el número correcto lo fija la especie**, no
la comodidad del galpón: para un ternero, el aislamiento después de las ocho semanas es una violación
aunque esté limpio y alimentado; para una cerda, el grupo tiene una **ventana temporal** (desde cuatro
semanas tras la cubrición hasta una semana antes del parto) que la ley escribe con fechas; para una
gallina, lo que la fuente verifica no es el tamaño del grupo sino **el recurso social por ave** (un nido
por cada siete aves). Y hay un dato que el estándar debe decir: **el único umbral de tamaño de grupo
verificado en toda la sesión es del porcino** (± 10 % de superficie si el grupo es < 6 o ≥ 40), y **no se
traslada a las aves**: trasvasar ese umbral sería inventar el piso de otra especie.

**Protocolo.** Tamaño y composición del grupo (número, edades, estabilidad a lo largo del ciclo);
**relación recurso/ave** para nidos y comederos; **ventana temporal** de alojamiento en grupo para
porcino; existencia y tipo de separaciones (perforadas o ciegas) en corrales individuales; observación
etológica de conductas sociales alteradas (aislamiento, agresión) como dato complementario, **nunca como
sustituto del parámetro**. Frecuencia: por lote, y en cada reagrupación.

**Violación.** Hechos observables: **ternero en corral individual después de las 8 semanas** sin
certificación veterinaria; **paredes ciegas** en corral individual (sin contacto visual y táctil);
**cerda fuera de grupo** dentro de la ventana legal; **menos de un nido por cada siete aves** o nido
colectivo con densidad superior a 1 m² por 120 aves; grupo por debajo de 6 o por encima de 40 **sin el
ajuste de superficie** que la ley exige. El parámetro «5-25 gallinas/grupo» del canon se registra, se
mide y **hoy no imputa violación** por falta de fuente.

### 4.9 Dimensión 6: Libertad de movimiento (poder girar, salir y caminar)

**Qué protege.** La capacidad física de moverse, girar, caminar, salir y echarse sin obstáculo, y la
prohibición de los sistemas de inmovilización.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| Cerdas y cerdas jóvenes — ataduras | **Prohibidas** (uso vetado desde el 1-1-2006; construir o convertir instalaciones con ataduras, prohibido) | — | UE, Directiva 2008/120/CE art. 3.3 (2008) |
| Corral individual de cerdo (uso temporal) | Debe permitir **girar con facilidad** | — | UE, Directiva 2008/120/CE art. 3.8 (2008) |
| Ternero — dimensiones mínimas del corral individual | Ancho **≥ altura a la cruz** en estación; largo **≥ longitud corporal (nariz-punta del isquion) × 1,1** | — | UE, Directiva 2008/119/CE art. 3.1(a) (2008) |
| Ponedoras en sistemas de varios niveles | **Máx. 4 niveles**; altura libre **≥ 45 cm** entre niveles | — | UE, Directiva 1999/74/CE art. 4.1.3(a) (1999) |
| Ponedoras con acceso a parque exterior — salidas | Varias *popholes* de **≥ 35 cm de alto × 40 cm de ancho** a lo largo de todo el edificio; **≥ 2 m** de abertura total por grupo de **1 000 aves** | — | UE, Directiva 1999/74/CE art. 4.1.3(b)(i) (1999) |
| Transporte — «viaje largo» | **> 8 h** desde que se mueve el primer animal del lote | — | UE, Reglamento (CE) 1/2005 art. 2(m) (2004) |
| Transporte — condiciones mínimas | Prohibido transportar de modo que pueda causar lesión o sufrimiento indebido; superficie y altura suficientes; **agua, pienso y descanso** a intervalos adecuados | — | UE, Reglamento (CE) 1/2005 art. 3 (2004) |
| **«Horas/día fuera» — parámetro del canon** | **8 h/día** — `[SIN FUENTE VERIFICADA]` | **12 h/día** — `[SIN FUENTE VERIFICADA]` | Cap. 9 §9.5 `[VERIFICADO]`; **ninguna fuente verificada fija horas de acceso al exterior**. El extremo de 8 h **no es un umbral animal**: reproduce, con otra unidad, el corte de «viaje largo» del Reglamento (CE) 1/2005 art. 2(m) —una definición de transporte, no un piso de bienestar— y por eso no se hereda |

**Justificación.** La libertad de movimiento tiene dos formas verificables que no son «horas al aire
libre»: **la prohibición de inmovilizar** (ataduras, corrales que no permiten girar) y **la geometría del
acceso** (número y tamaño de las aberturas al exterior, altura libre entre niveles, dimensiones del
corral). La ley **nunca regula horas**: regula **superficie exterior** (4 m²/ave en ecológico) y
**aberturas** (≥ 2 m por 1 000 aves). El canon, en cambio, fija «8 h/día fuera, óptimo 12», y ese número
no tiene fuente. **Propuesta no ratificada:** el piso de esta dimensión se escribe con las tres formas
verificadas —prohibición de ataduras, geometría que permita girar, aberturas dimensionadas— y las horas
de acceso al exterior se conservan como **Óptimo votable** (POLÍTICA), no como piso.

**Protocolo.** Inspección de presencia de ataduras y de la geometría del corral (medidas de ancho y largo
frente a la cruz y la longitud corporal del animal); recuento y medición de *popholes*; número de niveles
y altura libre; registro de transporte (hora de carga, duración, paradas, agua y pienso). Frecuencia: en
cada visita de verificación y **en cada transporte**.

**Violación.** Hechos observables: **ataduras presentes**; corral individual en el que el animal **no
puede girar**; dimensiones de corral por debajo de la fórmula legal; **más de 4 niveles** o altura libre
< 45 cm; ausencia de aberturas al exterior cuando el sistema declara acceso; transporte superior a 8 h sin
las condiciones del Reglamento 1/2005. El parámetro «horas/día fuera» del canon se registra y, sin
fuente, **no imputa**.

### 4.10 Dimensión 7: Expresión del comportamiento natural (la dimensión con el peso más pequeño y el único piso/plenitud con fuente)

**Qué protege.** La posibilidad de ejecutar las conductas propias de la especie que no son ni
alimentarse ni moverse: **escarbar, picotear, bañarse en polvo, encaramarse, construir el nido, hozar,
manipular material**. Es la dimensión donde el estándar se juega su diferencia con una jaula limpia.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| Ponedoras — superficie de yacija | **≥ 250 cm²/ave**, ocupando **≥ 1/3** de la superficie del suelo | — | UE, Directiva 1999/74/CE art. 4.1(e) (1999) |
| Ponedoras — perchas | **≥ 15 cm/ave**; no sobre la yacija; distancia horizontal entre perchas **≥ 30 cm** y a la pared **≥ 20 cm** | **18 cm/ave** (ecológico) — **el único Óptimo con fuente de todo el SDV-A** | UE, Directiva 1999/74/CE art. 4.1(d) (1999) · Reglamento (CE) 889/2008 anexo III pt. 2 (2008) |
| Ponedoras — yacija en jaula enriquecida | Obligatoria, de modo que **picoteo y escarbado sean posibles**; nido obligatorio | — | UE, Directiva 1999/74/CE art. 6.1(b)(c) (1999) |
| Pollos de engorde — yacija | Acceso **permanente** a yacija **seca y friable** | — | UE, Directiva 2007/43/CE anexo I pt. 3 (2007) |
| Cerdas y cerdas jóvenes — material manipulable | Acceso **permanente** | — | UE, Directiva 2008/120/CE art. 3.5 (2008) |
| Cerdas gestantes secas — saciedad y necesidad de masticar | Pienso **voluminoso o rico en fibra** suficiente, además del energético | — | UE, Directiva 2008/120/CE art. 3.7 (2008) |
| Baños de polvo / baño de barro | **Presencia/ausencia** del comportamiento, reconocido como esencial — **sin cifra normativa** | — | `[SIN FUENTE VERIFICADA]` como umbral numérico: la Directiva 1999/74/CE solo obliga a yacija y perchas |
| **Perchas — parámetro del canon** | **15 cm/ave** (coincide con la fuente `[VERIFICADO]`) | **25 cm/ave** — `[SIN FUENTE VERIFICADA]` (el único *nivel superior* con fuente es **18 cm/ave**, ecológico) | Cap. 9 §9.5 `[VERIFICADO]` · Reglamento (CE) 889/2008 anexo III pt. 2 |

**Justificación, y el hallazgo que esta dimensión obliga a escribir.** Ésta es la dimensión con **más
contenido etológico y menos peso** de toda la tabla del canon. Los tres parámetros que la representan en
el SDV-Gallinas —baños de polvo, perchas y nidos— no tienen peso propio: caen en **«Otros: 0,05»**, el
peso más pequeño de los siete (§4.13). Y hay una ironía estructural que el estándar debe publicar: **el
único Óptimo con fuente externa verificada de todo el SDV-A es el de esta dimensión** (18 cm de percha
por ave en producción ecológica, frente a los 15 cm de la ley general). Es decir: **la dimensión que el
canon pondera menos es la única cuyo par piso/plenitud la ley sí publica.** Este documento lo registra
como hallazgo y **no reescribe los pesos** (Regla 1): cambiarlos es POLÍTICA y pertenece al Parlamento.

**Protocolo.** Superficie de yacija por ave y proporción del suelo que cubre; **cm de percha por ave** y
distancias verificadas con cinta métrica; presencia y accesibilidad de material manipulable y de zona de
baño (polvo o barro); estado de la yacija (seca y friable); observación directa de las conductas
—escarbado, picoteo, baño, encaramado— con **registro de presencia/ausencia**, no con estimación
subjetiva de «bienestar». Frecuencia: por ciclo, con observación en al menos **dos momentos del día**
(mañana y tarde), porque las conductas de confort tienen hora.

**Violación.** Hechos observables: **menos de 250 cm² de yacija por ave** o yacija que cubre menos de un
tercio del suelo; **menos de 15 cm de percha por ave**, o percha sobre la yacija, o distancias menores a
las mínimas; **ausencia de material manipulable** en cerdas; **ausencia total de zona de baño** cuando la
especie la requiere (registrada como violación binaria auditable, sin cuantificar); imposibilidad
manifiesta de picotear o escarbar. El Óptimo de 25 cm de percha del canon **no se usa como piso**: es
POLÍTICA y su lugar es la votación.

### 4.11 Dimensión 8: Ausencia de crueldad (la única con forma de prohibición absoluta)

**Qué protege.** La integridad física y la muerte sin dolor: prohíbe las intervenciones que mutilan o
dañan, y exige que el sacrificio no sea un sufrimiento añadido a la muerte.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| Intervenciones quirúrgicas no terapéuticas (pollos) | **Prohibidas** las que dañen o extirpen una parte sensible del cuerpo o alteren la estructura ósea. **Excepción verificada:** el corte de pico es autorizable solo si se agotan otras medidas, con asesoramiento veterinario, por personal cualificado y en aves de **< 10 días**; la castración, solo bajo supervisión veterinaria | 0 | UE, Directiva 2007/43/CE anexo I pt. 12 (2007) |
| Sacrificio — aturdimiento previo | **Obligatorio**: solo se mata tras aturdir; la pérdida de consciencia y sensibilidad debe **mantenerse hasta la muerte**. **Excepción verificada:** ritos religiosos en matadero | 0 sacrificios sin aturdir | UE, Reglamento (CE) 1099/2009 art. 4.1 y 4.4 (2009) |
| Peces — aturdimiento y métodos prohibidos | **Aturdidos antes de matarlos**, con **pérdida inmediata e irreversible de consciencia**. Métodos que «han mostrado un bienestar deficiente» y **no deben usarse** si es factible otra cosa: **hielo en el agua, CO₂, baños de sal o amoníaco, asfixia por extracción del agua, desangrado sin aturdimiento** | 0 | WOAH/OIE, Código Sanitario para los Animales Acuáticos cap. 7.3 arts. 7.3.1 y 7.3.6.4 |
| Verificación del aturdimiento en peces | Pérdida de movimiento corporal y respiratorio (actividad opercular); pérdida de respuesta visual evocada (**VER**); pérdida del reflejo vestíbulo-ocular (**VOR**) | — | WOAH/OIE, Código Acuático cap. 7.3 art. 7.3.6.1.6 |
| Camarones — ablación del pedúnculo ocular | **Prohibida** | 0 | UE, Reglamento (CE) 889/2008 anexo XIIIa §7 (2009) |
| Selección de razas para **evitar la mutilación** | Obligación: la elección de razas debe contribuir a **evitar la necesidad de mutilar** y asegurar un alto nivel de bienestar | — | UE, Reglamento (UE) 2018/848 anexo II parte II pts. 1.3.2(d) y 1.3.3 (2018) |
| Mutilaciones del porcino (corte de cola, castración, limado de dientes) | `[SIN FUENTE VERIFICADA]` — el anexo I de la Directiva 2008/120/CE **devuelve 404** en la ruta consultada: la dimensión queda sin verificar para el porcino | — | (fuente descartada, §14.7) |
| **«Crueldad = 0 %, absoluto e irrenunciable» — parámetro del canon** | **0 %** — verificable **como principio, no como derecho vigente**: las dos únicas prohibiciones absolutas verificadas traen excepción escrita | 0 % | Cap. 9 §9.5 `[VERIFICADO]` (la tabla del canon publica **0 % en las dos columnas**, no solo en el piso); contraste con UE 2007/43 anexo I pt. 12 y UE 1099/2009 art. 4.4 |

**Justificación, y la advertencia que este documento tiene la obligación de hacer.** La dimensión 8 es la
de **peso máximo** en la fórmula (0,30, «violación absoluta») y la única que el canon escribe como
absoluto. Pero la honestidad de fuente exige decir tres cosas:

1. **El 0 % no es derecho vigente: es una decisión del proyecto.** Las dos únicas prohibiciones absolutas
   que se pudieron verificar **traen excepción escrita**: el corte de pico en aves de menos de diez días
   (Directiva 2007/43/CE anexo I pt. 12) y los ritos religiosos en matadero (Reglamento 1099/2009
   art. 4.4) `[VERIFICADO]`. El canon es, por tanto, **más exigente que el derecho que lo verifica**, y
   debe presentarse como decisión del proyecto —no como estándar heredado—.
2. **Lo que sí es absoluto sin excepción**: la **prohibición de la ablación del pedúnculo ocular** en
   camarones (Reglamento 889/2008 anexo XIIIa §7) y el **aturdimiento con pérdida inmediata e
   irreversible de consciencia** en peces, con la lista de métodos prohibidos de la WOAH. Son los dos
   pisos más duros del SDV-A y los únicos que se pueden citar como 0 sin asterisco.
3. **El porcino quedó sin verificar.** El anexo I de la Directiva 2008/120/CE —donde viven las reglas de
   corte de cola, castración y limado de dientes— **devuelve 404** en la ruta consultada (§14.7). No se
   cita ninguna cifra suya. **Una dimensión sin fuente no se convierte en una dimensión sin violaciones**:
   se declara el vacío y, mientras no haya umbral, opera la vía precautoria de T14 (§5.5).

**Protocolo.** Registro de **todas** las intervenciones no terapéuticas practicadas (tipo, edad del
animal, personal, supervisión veterinaria, justificación); verificación de aturdimiento con **criterios
observables** en peces (movimiento corporal y opercular, VER, VOR) y con los registros del matadero en
las demás especies; vigilancia del **método de sacrificio** y de la lista de métodos prohibidos;
selección de razas documentada como medida preventiva. Frecuencia: **por lote y por evento** —cada
intervención y cada sacrificio son un evento registrable, no un promedio del ciclo—.

**Violación.** Hechos observables, y son los más nítidos del estándar porque son **actos**: una
intervención no terapéutica practicada fuera de las condiciones permitidas (o cualquiera, si el piso
ratificado es el 0 % del canon); un sacrificio **sin aturdimiento previo** o en el que la pérdida de
consciencia no se mantuvo hasta la muerte; el uso de un método de los que la WOAH declara de bienestar
deficiente en peces; la **ablación del pedúnculo ocular**; la aplicación sistemática de una práctica
dolorosa a un lote entero (que además activa el último escalón del Factor de Sufrimiento: `∞`, es decir
**prohibición de mercado** como estado, §5.4).

### 4.12 El Factor de Consciencia por niveles A/B/C/D (Cap. 9 §9.2.2): dos funciones y una compuerta

El canon define un **espectro de consciencia** que *«determina el peso ético de cada ser»* y publica esta
tabla (Cap. 9 §9.2.2) `[VERIFICADO]`:

| Categoría | Características (canon) | Factor de Consciencia (FC) | Ejemplos (canon) |
|---|---|---|---|
| **Nivel A** | Sistema nervioso central complejo, comportamiento social, evidencia de sufrimiento | **0,7 - 1,0** | Mamíferos, aves, cefalópodos |
| **Nivel B** | Sistema nervioso desarrollado, respuestas aversivas claras | **0,3 - 0,6** | Peces, reptiles, crustáceos |
| **Nivel C** | Sistema nervioso básico, respuestas reactivas | **0,1 - 0,2** | Insectos, moluscos simples |
| **Nivel D** | Sin sistema nervioso centralizado | **0,0** | Plantas, hongos, bacterias |

Y el canon declara expresamente **para qué sirve**: *«Este factor no determina el "derecho a existir"
(todos los seres tienen valor intrínseco), sino el **peso en el cálculo del VHV** cuando sus vidas son
consumidas»* `[VERIFICADO]`.

**Lo que la evidencia externa verificada respalda, y lo que no.**

| Pieza del FC | ¿Fuente externa verificada? | Evidencia |
|---|---|---|
| **Inclusión categórica** de vertebrados, **cefalópodos** y **crustáceos decápodos** en el ámbito de protección | 🟢 **Sí** | UE, Directiva 2010/63/UE art. 1.3(b): la Directiva se aplica a *«live cephalopods»*; Reino Unido, *Animal Welfare (Sentience) Act 2022* §5(1): animal = cualquier vertebrado distinto de *homo sapiens* + cualquier molusco cefalópodo + cualquier crustáceo decápodo |
| **Exclusión** de insectos y moluscos simples | 🟢 **Sí, como exclusión legal** | La Directiva 2010/63/UE y la *Sentience Act 2022* §5(2) los dejan fuera del ámbito (la segunda permite extenderlo por reglamento, **sin hacerlo**) |
| **Escala continua** 0,7-1,0 / 0,3-0,6 / 0,1-0,2 / 0,0 | 🔴 **No** | **Ningún organismo asigna pesos numéricos de consciencia.** Lo que existe es inclusión/exclusión categórica en el ámbito de protección legal. El número es una decisión del proyecto |
| **Nivel D = 0,0 (plantas, hongos, bacterias)** | 🔴 **No, y además contradice al propio repositorio** | `docs/theory/matematicas_maxocracia_compiladas.md` §IV.B.1 asigna **Plantas: 0,1** e **Insectos: 0,3-0,5** `[VERIFICADO]` (lectura directa) |
| **Nivel A incluye cefalópodos** | 🟢 **Sí** | Directiva 2010/63/UE art. 1.3(b) y *Sentience Act 2022* §5(1): los cefalópodos están **incluidos expresamente** en la protección |

**Contradicción interna nº 2 del canon, cuantificada.** Dos documentos del repositorio publican escalas
distintas del mismo factor `[VERIFICADO]`:

| Grupo | Cap. 9 §9.2.2 | `matematicas_maxocracia_compiladas.md` §IV.B.1 | ¿Compatible? |
|---|---|---|---|
| Plantas | 0,0 (Nivel D) | 0,1 | **No** |
| Insectos | 0,1-0,2 (Nivel C) | 0,3-0,5 | **No** (hasta 2,5× de diferencia) |
| Peces | 0,3-0,6 (Nivel B) | 0,5-0,7 | Solape parcial |
| Aves | 0,7-1,0 (Nivel A) | 0,7-0,9 | Compatible |
| Mamíferos | 0,7-1,0 (Nivel A) | 0,9-1,0 | Solape parcial |
| Cefalópodos | 0,7-1,0 (Nivel A) | **no aparecen** | Hueco |

**La propuesta de este documento: separar las dos funciones del FC y convertir la primera en compuerta.**
El FC hace hoy dos trabajos distintos con un solo número, y de ahí salen las contradicciones:

- **Función 1 — Alcance de la protección** (¿este ser entra en el estándar?): es una decisión
  **categórica**, y es lo que la ley realmente produce. **Propuesta no ratificada:** formalizarla como
  compuerta de tres estados `FC_estado ∈ {INCLUIDO, EN DUDA, EXCLUIDO}`, con `INCLUIDO` = vertebrados +
  cefalópodos + crustáceos decápodos (con fuente), `EN DUDA` = insectos, moluscos simples y otros
  invertebrados (excluidos hoy por la ley, con evidencia en movimiento), `EXCLUIDO` = plantas, hongos y
  bacterias — y aquí el canon **no tiene fuente y se contradice consigo mismo**, de modo que la propuesta
  es mantenerlo en `EN DUDA` **hasta que exista fuente**, no en `EXCLUIDO`.
- **Función 2 — Peso en el cálculo del VHV** (¿cuánto pesa su vida consumida?): es **POLÍTICA y
  votable**, con la contradicción interna declarada en la tabla anterior. Mientras no se ratifique una
  escala única, **el peso numérico no puede sostener por sí solo ninguna decisión del piso**.

**Y el Principio Precautorio de Consciencia (Cap. 10 §10.3) opera exactamente sobre `EN DUDA`.** No sobre
`INCLUIDO` —que ya está protegido— ni sobre `EXCLUIDO` —que no está en el ámbito—: **sobre el estado
intermedio**. Esta es la conexión estructural con el resto de la biblioteca y es un aporte de este
documento: **la compuerta `EN DUDA` del SDV-A es el análogo exacto del estado `indeterminado` que el
documento [08](08_INV2-E_invariante.md) §8.4 tuvo que crear para el ecosistema.** Los dos estándares
biológicos descubren, por vías independientes, que **dos estados no alcanzan**: uno porque no hay
sensores, el otro porque no hay certeza sobre la mente. Y en los dos, la duda **no imputa violación** y
**tampoco certifica cumplimiento**: obliga a instrumentar y **prohíbe lo irreversible** (T14).

### 4.13 El arquetipo SDV-Gallinas (Cap. 9 §9.5): diez parámetros, siete pesos y tres hallazgos

El Cap. 9 §9.5 publica el único SDV-A desarrollado del canon, y este documento lo transcribe **tal como
está** `[VERIFICADO]`:

| Dimensión (Cap. 9 §9.4) | Parámetro del canon | Mínimo (canon) | Óptimo (canon) | ¿Fuente externa verificada? |
|---|---|---|---|---|
| Espacio vital | m²/gallina | **0,25** | 0,75 | 🔴 no (la ley da 750 cm² = 0,075 m²; el ecológico, 1 667 cm² ≈ 0,167 m²) |
| Libertad de movimiento | horas/día fuera | **8** | 12 | 🔴 no (la ley no fija horas: fija aberturas y superficie exterior) |
| Acceso a agua | litros/día | **0,3** | 0,5 | 🔴 no (la ley fija **puntos de acceso**, no volumen) |
| Dieta natural | % de dieta natural | **30** | 60 | 🔴 no (la ley regula origen y prohibiciones, no un % de naturalidad) |
| Luz natural | horas/día | **6** | 10 | 🔴 no (la ley regula iluminación en lux y oscuridad, y solo en pollos de engorde) |
| Socialización | gallinas/grupo | **5** | 25 | 🔴 no (el único umbral de grupo verificado es del porcino) |
| Baños de polvo | acceso diario | ✓ | ✓ | 🟡 binario: la conducta es esencial, **sin cifra normativa** |
| Perchas | cm/gallina | **15** | 25 | 🟢 **el mínimo coincide** con la Directiva 1999/74/CE art. 4.1(d); el óptimo de 25 **no tiene fuente** (el verificado es 18) |
| Nidos | gallinas/nido | **5** | 3 | 🟡 parcial: la ley da **1 nido por cada 7 aves** (el canon es más estricto) |
| Crueldad | prácticas dolorosas | **0 %** | **0 %** | 🟡 parcial: verificable como principio; las dos prohibiciones absolutas verificadas **traen excepción escrita** |

**Hallazgo 1 — la tabla mezcla parámetros que no tienen el mismo sentido, y no declara operador.** «Más
es mejor» en m²/gallina, horas fuera, horas de luz y cm de percha; «menos es mejor» en gallinas/nido
(el Óptimo 3 es **menor** que el Mínimo 5, y eso es correcto); y «ni más ni menos» en gallinas/grupo,
donde 5 y 25 no son piso y techo de una escala sino **los dos extremos de una banda admisible**. Sin
operador declarado, el motor compararía un pH con un EOO —que es exactamente el problema que el documento
[07](07_Formula_de_violacion_y_pesos.md) §3.3 tuvo que resolver para el ecosistema—. **Propuesta no
ratificada:** adoptar para el SDV-A los mismos operadores (`min`, `max`, `range`, `binary`) con la misma
saturación en cero, y declarar `gallinas/grupo` como parámetro `range` (banda 5-25).

**Hallazgo 2 — diez parámetros, siete pesos y dos bloques compartidos.** Los pesos del canon suman
exactamente **1,00** `[VERIFICADO]` (0,30 + 0,15 + 0,15 + 0,15 + 0,10 + 0,10 + 0,05), y eso es una
propiedad que el SDV-A **ya cumple** y que el SDV-E tuvo que construir (`abs(Σ pesos − 1) < 1e-9`,
documento 07 §5.3). Pero el mapeo entre los diez parámetros y los siete pesos **no está publicado por el
canon**, y de ahí salen dos ambigüedades que este documento declara:

| Peso (canon) | Dimensión del Cap. 9 §9.4 | Parámetros del SDV-Gallina que caen en él | Ambigüedad |
|---|---|---|---|
| **0,30** | D8 Ausencia de crueldad | prácticas dolorosas (%) | — |
| **0,15** | D1 Espacio vital | m²/gallina | — |
| **0,15** | D6 Libertad de movimiento | horas/día fuera | — |
| **0,15** | **D2 + D3 (bloque «Agua/Alimentación»)** | % dieta natural **y** litros/día | **dos dimensiones comparten un peso** |
| **0,10** | D4 Luz y ritmos circadianos | horas/día de luz natural | — |
| **0,10** | D5 Socialización específica | gallinas/grupo **y** gallinas/nido | un peso para dos parámetros de forma distinta |
| **0,05** | **D7 Expresión del comportamiento natural (en «Otros»)** | baños de polvo, perchas (y nidos, según lectura) | **la dimensión más etológica tiene el peso más pequeño y no tiene peso propio** |

**Propuesta no ratificada, y con precedente en esta misma biblioteca:** mientras el Parlamento no
ratifique un reparto por parámetro, el bloque compartido se resuelve con la **agregación por el peor caso
medido** (`A_k = max_i D_i`, documento 07 §5.1, regla «one-out, all-out») y **no** repartiendo el peso por
analogía. Repartir 0,15 en 0,075 + 0,075 —como el documento 07 §5.3 hizo con caudal y conectividad— es
posible y está marcado allí como `[HIPÓTESIS]`; aquí **no se hace**, porque los dos casos no son
equivalentes: caudal y conectividad eran dos dimensiones **sin peso**, y agua y alimentación son dos
dimensiones **con un peso común**. La diferencia importa y se declara.

**Hallazgo 3 — el único número del canon con coincidencia exacta en una fuente externa pesa 0,05.** El
recuento, sin adornos, **por parámetro**: de los **diez** parámetros del SDV-Gallinas, **uno** (perchas:
15 cm/ave) coincide exactamente con un piso legal verificado; **tres** son una versión **más estricta** de
una fuente que publica el mismo tipo de parámetro —espacio: 2 500 cm² frente a los 750/1 667 de la ley;
nidos: 5 aves/nido frente a las 7 de la ley— o **traen excepciones escritas en la fuente que los
verifica** —crueldad: 0 % sin excepciones frente a prohibiciones con excepción—; y **seis** no tienen
fuente externa verificada en esta sesión. Traducido a la unidad de la fórmula —y clasificando cada peso
**por su parámetro más débil**, criterio conservador que §5.6 explicita—, **el SDV-A puede ejecutar hoy su piso
sobre 0,05 de su peso declarado con los números del canon tal como están escritos, 0,45 en forma parcial
(más estricta que la fuente o con excepciones) y 0,50 sin fuente.** Es el número más incómodo del
documento y es el que justifica §5.6.

### 4.14 El acoplamiento SDV-A ↔ SDV-E: el suelo del animal no puede ser mayor que el del ecosistema

Éste es el punto que este documento debe poder **citar con número**, no con metáfora, y el número existe.
Está en el derecho ecológico de la Unión Europea, y es **aritmético**:

| Pieza del acoplamiento | Valor | Unidad | Fuente |
|---|---|---|---|
| **Tope del ecosistema sobre la carga animal (nitrógeno)** | **170** de nitrógeno por año y por hectárea de superficie agrícola utilizada (estiércol de ganado): **limita cuántos animales caben**, no el piso de cada uno | kg N/ha/año | UE, Reglamento (UE) 2018/848 anexo II parte I pt. 1.9.4 (2018) |
| **Condicionalidad del exterior del ave al techo del suelo** | Los **4 m²/ave** de superficie exterior ecológica se conceden *«provided that the limit of 170 kg of N/ha/year is not exceeded»* | m²/ave **∧** kg N/ha/año | UE, Reglamento (CE) 889/2008 anexo III pt. 2 (2008) |
| **Tope del ecosistema acuático sobre la densidad de peces** | Producción en aguas continentales limitada a **1 500 kg de peces/ha/año**; fertilización máx. **20 kg N/ha**; **zonas de vegetación natural como franja tampón** alrededor de las unidades | kg/ha/año · kg N/ha | UE, Reglamento (CE) 889/2008 anexo XIIIa §6 (2009) |
| **Superficie de vegetación en estanques de tierra** | **≥ 50 %** de los diques con cobertura vegetal; balsas de depuración basadas en humedal | % de los diques | UE, Reglamento (CE) 889/2008 anexo XIIIa §4 (2009) |
| **Diversidad genética de especies domesticadas** (puente razas ↔ SDV-E) | Mantener y restaurar la diversidad genética **dentro y entre** poblaciones de especies nativas, silvestres **y domesticadas** | cualitativo | CBD, Marco Kunming-Montreal, Meta 4 (2022) |
| **Nutrientes y pesticidas** (el techo del suelo que el animal no puede cruzar) | Reducir **≥ 50 %** los nutrientes excedentes y **≥ 50 %** el riesgo de pesticidas y químicos altamente peligrosos | % | CBD, Marco Kunming-Montreal, Meta 7 (2022) |
| **Gobernanza del uso del territorio por el animal** | Marco vinculante: gestión sostenible de la agricultura, acuicultura, pesca y silvicultura; incremento sustancial de prácticas favorables a la biodiversidad | meta 2030 | CBD, Marco Kunming-Montreal, Meta 10 (2022) |

**La formulación citable, en una frase:** la única formulación **normativa y numérica** hallada donde el
piso del animal está **condicionado** por el techo del ecosistema es el **anexo III del Reglamento
889/2008**: los **4 m²/ave** de parque exterior **solo existen si el suelo no supera 170 kg N/ha/año**
(tope fijado en el anexo II parte I pt. 1.9.4 del Reglamento 2018/848). **El suelo del animal se recorta
contra el suelo del ecosistema, y el recorte es aritmético, no retórico.** El segundo par es el acuático:
**1 500 kg de peces/ha/año** con **50 % de los diques con cobertura vegetal** y franjas tampón de
vegetación natural.

**La regla de prelación entre los dos pisos, y las tres consecuencias que este documento propone.** Los
dos pisos son **LEY** y ninguno es votable; cuando entran en conflicto, la resolución **no puede ser
degradar a ninguno de los dos**:

1. **El piso del ecosistema no cede ante el Óptimo del animal.** Ampliar superficie exterior, densidad o
   carga ganadera para acercarse al Óptimo del animal **no autoriza** a cruzar el techo del ecosistema
   (170 kg N/ha/año, 1 500 kg/ha/año). Óptimo es POLÍTICA y piso es LEY: la LEY manda.
2. **El piso del animal no cede ante el Óptimo del ecosistema.** Mejorar el índice ecológico de la unidad
   **no autoriza** a reducir la superficie, el agua o la percha por debajo del piso del animal: los dos
   son LEY.
3. **Cuando los dos pisos no caben, la variable de ajuste es la actividad humana, no ninguno de los dos
   pisos.** Se reduce la **carga** (menos animales, menos superficie ocupada, más rotación), no el piso de
   nadie. Es la traducción exacta de la «doble jurisdicción» del documento
   [18](18_Ecosistemas_Agroecosistemas.md) §11.1 y del principio de que **el objeto de la consecuencia
   nunca es el sujeto protegido** (documento 08 §8.7). `[HIPÓTESIS]` en la formulación de las tres
   reglas; los dos pisos y su condicionalidad numérica son canon y derecho verificado.

**Y la frontera que este documento NO resuelve, y dice:** la diversidad de **razas ganaderas** es
simultáneamente una dimensión del SDV-E (diversidad cultivada y criada) y del SDV-A (la existencia de la
raza como población). **Dónde termina el SDV-A y empieza el SDV-E en un animal de granja no está resuelto
por ninguna fuente** (documento 18 §11.1), y este documento tampoco lo resuelve: lo declara (§13,
pregunta 12).

---

## 5. Fórmula de violación, pesos y umbrales

Esta sección fija **la aritmética del SDV-A**: qué publica el canon, qué le falta, y qué se propone para
que sea calculable sin inventar un solo umbral. Se presenta en siete piezas: la fórmula del canon y sus
dos versiones (5.1), el déficit normalizado y los operadores (5.2), la tabla de pesos (5.3), el Factor
de Sufrimiento y su `∞` (5.4), la duración en TA (5.5), la cobertura del piso y la sustitución de
parameterización (5.6), y un ejemplo aplicado completo con las dos parameterizaciones (5.7).

### 5.1 Las dos fórmulas del canon, y qué le falta a cada una

El canon escribe **dos** fórmulas para el SDV-A, y no son la misma `[VERIFICADO]`:

```
(a) Violación_SDV-A = Σ [ (Parámetro_requerido − Parámetro_actual) × Peso × Duración ]     Cap. 9 §9.5

(b) V = Σ ( Seres × Factor_Consciencia × Factor_Sufrimiento × Factor_Abundancia )          Cap. 9 §9.8
```

*(Las dos se copian de la edición del capítulo que está en el repositorio:
`docs/book/edicion_3_dinamica/capitulo_09_sdv_a_260126.md`, edición 3.2 del 26 de enero de 2026 — la
misma que §12 cita como la única doctrina escrita del SDV-A.)*

La primera es la **fórmula de violación** del estándar por parámetro; la segunda es el **componente V del
VHV** —el precio de las vidas consumidas—, **tal como el canon la escribe en el Cap. 9 §9.8: con tres
factores y sin `FR`**. El Factor de Sufrimiento se toma de una tabla escalonada que la propia sección
publica (5.4), y un cuarto factor (`FR`, rareza genética) aparece en **otras** partes del sistema: la
fórmula que el documento 09 §5.1 sí publica con cuatro factores y la firma del motor (§12.1). Este
documento **no lo añade al canon**: en §9, la única vez que el componente V se transcribe con cuatro
factores, se está describiendo **la forma que el motor ya implementa**, no la del Cap. 9 §9.8 (véase
§14.8).

**No son intercambiables**: la primera decide si hay violación; la segunda decide cuánto cuesta la vida
consumida. Confundirlas es el error que produciría un estándar que «cobra» la violación en lugar de
bloquearla.

**Lo que le falta a la fórmula (a), comparada con la del SDV-E que el documento
[07](07_Formula_de_violacion_y_pesos.md) ya fijó:**

| Pieza | SDV-E (documento 07 §5) | SDV-A (canon, Cap. 9 §9.5) | Consecuencia |
|---|---|---|---|
| Déficit | **normalizado** `(req − actual)/req` | **sin normalizar**: `(req − actual)` | magnitudes heterogéneas no comparables entre dimensiones |
| Operador | explícito (`min`/`max`/`range`/`escalonado`) | **ausente** | el sentido del parámetro no está declarado (§4.13, hallazgo 1) |
| Saturación en 0 | sí: `max(0, ·)` | **no declarada** | un parámetro mejor que el piso daría déficit negativo |
| Duración | en **TA**, con `unidad_de_ciclo_ta` obligatoria | **«Duración» sin unidad** | no comparable entre especies ni auditable |
| Factor | `FE = e^(min(Σ FI·v·Δt, V_max))`, base neutra 1,0 | **tabla escalonada** 0,2 · 0,5 · 1,0 · 2,0 · ∞ | familia distinta: **precio**, no penalización (documento 09 §5.2) |
| Pesos | dos vectores que suman 1,000 | **siete pesos que suman 1,00** `[VERIFICADO]` | ya cumple la propiedad F4 |

**La advertencia del documento 09 §5.1 se aplica aquí palabra por palabra:** *«las tres fórmulas
anteriores están sin normalizar… INV2-E no puede adoptar el `(req − actual)` sin normalizar»*. Lo mismo
vale para el SDV-A, y este documento lo propone **sin tocar el canon**: la fórmula (a) se **lee** como
está y se **ejecuta** normalizada (§5.2). `[HIPÓTESIS]`, propuesta no ratificada.

### 5.2 El déficit normalizado y los operadores (propuesta no ratificada)

```
D_i = 0                                    si el parámetro cumple su piso
D_i = op_i(requerido_i, actual_i)          si lo incumple, con el operador declarado
D_i = None                                 si el parámetro NO ESTÁ MEDIDO
```

| Operador | Significado | Parámetros del SDV-A | Déficit normalizado |
|---|---|---|---|
| `min` | más es mejor | m²/animal, cm de percha/ave, cm de bebedero/ave, h de oscuridad, % de yacija | `D = max(0, (req − actual)/req)` |
| `max` | menos es mejor | aves/nido, kg/m³ de carga, kg N/ha/año | `D = max(0, (actual − req)/req)` |
| `range` | hay una banda admisible | **gallinas/grupo (5-25)**, pH del agua de bebida | `D = max(0, (lo − actual)/lo)` por abajo; `D = max(0, (actual − hi)/hi)` por arriba |
| `binary` | presencia/ausencia del derecho | baño de polvo, ataduras, aturdimiento, mutilación, franja de vegetación | **no produce déficit**: produce **estado de violación** (0/1) con el peso de su dimensión |

**Tres reglas que la normalización obliga a fijar** (y que se toman del documento 07, no se inventan):

1. **Saturación en 0 por abajo.** Un parámetro mejor que su piso **no genera crédito**: *«una vida
   afectada no se des-afecta en la misma cuenta»* `[VERIFICADO]` en `app/micromax.py`
   (`if v_ucv < 0: raise`) y en la fórmula del ecosistema (documento 07 §3.2). En el SDV-A esto tiene una
   lectura propia: **dar a un animal más espacio del que su piso exige no compensa haberle dado menos
   agua.**
2. **Sin techo de 1 por arriba.** `D` puede superar 1 —y en el SDV-A es fácil: 90 gallinas por grupo
   contra un Óptimo de 25 da `(90 − 25)/25 = 2,6`—, lo que es correcto y deliberado: la fórmula debe poder
   decir «tres veces peor que el piso».
3. **`None` no es 0 y no es cumplimiento** (Regla 7): un parámetro no medido no entra en la suma, **no se
   imputa** y **cuenta como cobertura faltante** (§5.6).

### 5.3 Los pesos: los siete del canon, con su mapeo publicado

| Peso | Dimensión | ¿Tiene piso con fuente? | Observación |
|---|---|---|---|
| **0,30** | D8 Ausencia de crueldad | 🟡 **parcial**: principio verificado, con excepciones escritas en la ley | el peso mayor; su piso ratificado (0 %) es **más estricto que el derecho** |
| **0,15** | D1 Espacio vital | 🔴 **no** para el número del canon (0,25 m²); 🟢 **sí** para el parámetro legal (750 cm²) | decisión del proyecto: 3,33× la ley |
| **0,15** | D6 Libertad de movimiento | 🔴 no para «horas/día fuera»; 🟢 sí para ataduras, giro y aberturas | cambio de unidad (§4.9) |
| **0,15** | **D2 + D3** (bloque Agua/Alimentación) | 🔴 no para litros ni para % de dieta natural; 🟢 sí para **puntos de acceso** y para **origen y prohibiciones** | **dos dimensiones, un peso** |
| **0,10** | D4 Luz y ritmos circadianos | 🔴 no para «luz natural»; 🟢 sí para oscuridad e intensidad **en pollos de engorde** | extrapolación declarada |
| **0,10** | D5 Socialización específica | 🔴 no para «gallinas/grupo»; 🟢 sí para **nido por ave** y ventana de grupo del porcino | recurso social verificado |
| **0,05** | D7 Expresión del comportamiento natural («Otros») | 🟡 parcial: yacija (250 cm²/ave) y perchas (15 cm/ave) verificadas; baño de polvo sin cifra | **el peso más pequeño para la dimensión más etológica** |
| **Σ = 1,00** | | | **ya cumple la propiedad de suma exacta** |

> `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` **para los pesos del SDV-A.** No existe
> ningún organismo que publique pesos porcentuales para crueldad, espacio, movimiento, agua y
> alimentación, luz, socialización y comportamiento natural. Los siete pesos son **una decisión del
> proyecto publicada en el Cap. 9 §9.5**, y **este documento no los cambia**: cambiarlos es POLÍTICA y
> pertenece al Parlamento (categoría `critical`), no a un documento de biblioteca.

**Estabilidad de la tabla.** Se propone, igual que en el documento 07 §5.3, que la tabla se **hashee** y
que el hash se registre en cada validación: un peso cambiado a mitad de una serie temporal es una forma
de borrar la contabilidad (T13).

### 5.4 El Factor de Sufrimiento: una tabla escalonada cuyo último escalón no es un número

La tabla es canon (Cap. 9 §9.8) `[VERIFICADO]`:

| Cumplimiento del SDV | Factor de Sufrimiento | Efecto en el precio (canon) |
|---|---|---|
| 100 % | **0,2** | precio base |
| 75 % | **0,5** | +150 % aprox. |
| 50 % | **1,0** | +300 % aprox. |
| 25 % | **2,0** | +600 % aprox. |
| **Violación sistemática** | **→ ∞** | **Prohibición de mercado** |

**Tres consecuencias formales, y las tres son duras:**

1. **El SDV-A pertenece a la familia del «precio del consumo», no a la de la «penalización de la
   violación»** (documento 09 §5.2, insight I5). Con cumplimiento pleno el factor vale **0,2, no 1,0**, y
   eso **no es un error ni una base neutra mal corregida**: es que **consumir una vida tiene un costo base
   aunque se haga bien**. Heredar la base neutra del SDV-S o del SDV-E sería declarar que la vida
   consumida no cuesta nada, que es exactamente lo contrario de lo que dice el canon. Este documento
   **respeta esa diferencia** y no la «corrige».
2. **El `∞` no es una cifra: es una consecuencia jurídica.** Es la misma lección que el documento 07 §5.4
   y el documento 09 §5.3 fijaron para los otros reinos: en el SDV-A el `∞` **es la prohibición de
   mercado**. Un contrato que guarde `inf` en una columna numérica no es ejecutable; uno que pase a
   `estado = PROHIBIDO` sí. Implementación propuesta: **disparador booleano y estado verificable**
   (`prohibicion_de_mercado`, `objeto_de_la_consecuencia = "actividad"`), nunca un número.
3. **La tabla es escalonada y no interpola, y el canon no define «% de cumplimiento».** Éste es un hueco
   real: la tabla indexa por **cumplimiento** (100 %, 75 %, 50 %, 25 %) y la fórmula (a) produce una
   **magnitud de violación** (`v`). **Propuesta no ratificada:** `cumplimiento = 1 − min(v, 1)`, con la
   regla conservadora de **tomar el escalón alcanzado sin interpolar** (un `v = 0,52` da un cumplimiento
   de 0,48, que **no alcanza el escalón del 50 %**, y por tanto aplica el de 25 % → FS = 2,0). La
   equivalencia entre `v` y cumplimiento **tiene el mismo límite que el documento 07 §5.6 declaró para
   `ISE_derivado`**: son dos escalas distintas y solo coinciden cuando el piso coincide con el techo de la
   escala.

### 5.5 La duración: el animal vive en TA, y la unidad del ciclo no está decidida

El canon multiplica por «Duración» y **no dice en qué unidad** (documento 09 §8, requisito 1; documento
[03](03_No_colonizacion_del_TA.md) §11 lo remite expresamente a este documento). Estas son las decisiones
que se proponen, y son cuatro:

1. **La duración se acumula en TA (Tiempo Absoluto).** El tiempo del animal es TA, igual que el del
   ecosistema (documento 09 §11.1, eje 6); el **PIU** (Cap. 5 §5.5) es el **único** traductor TA↔TVI y la
   conversión ocurre **fuera** de la fórmula. Una violación del SDV-A expresada en TVI describiría el
   tiempo del animal con la unidad del tiempo humano: es la colonización temporal que el canon prohíbe
   (Cap. 16.5 §16.5.14).
2. **La unidad del ciclo es configuración obligatoria y sin valor por defecto.** Candidatos legítimos,
   ninguno con fuente verificada en esta sesión: el **ciclo biológico de la especie**, el **ciclo
   productivo** y el **año TA** del territorio. Se adopta la regla que el documento
   [08](08_INV2-E_invariante.md) §6.2 fijó para el ecosistema: `unidad_de_ciclo_ta` **sin default**;
   elegir «año calendario» por comodidad de implementación sería colonizar el tiempo del animal con el
   calendario del matadero.
3. **No se hereda el 7 del SDV-S.** Los siete ciclos consecutivos del invariante sintético se cuentan en
   **horas TPI** de un agente de cómputo; en el SDV-A el ciclo es un período biológico y **copiar el
   número cambiaría el significado** (documento 08 §8.6, razones 1 y 2). El contador de escalada se
   configura explícitamente y su valor es POLÍTICA votable.
4. **Mientras no exista umbral de duración, `Δt` se computa como el ciclo TA completo** en que la
   medición se realizó, y el resultado se marca `duracion_aproximada = True`. Es la aproximación
   conservadora y auditable que el documento 07 §6.3 ya adoptó para el ecosistema.

### 5.6 La cobertura del piso del SDV-A: el número incómodo

El documento 07 §5.3 publicó, para el ecosistema, una cifra que debe doler: **el SDV-E ejecuta hoy su piso
sobre 0,925 del peso que declara querer proteger** (y el documento 08 §5.2 publica 0,680 sobre su propio
catálogo, con la disputa declarada). El SDV-A tiene el mismo problema, **en una forma distinta y peor**:

| Categoría del piso | Peso | Qué significa |
|---|---|---|
| **Piso con coincidencia exacta en fuente externa verificada** | **0,05** | perchas: 15 cm/ave (Directiva 1999/74/CE art. 4.1(d)) — **la misma magnitud, el mismo número** |
| **Piso parcial: la misma magnitud con otro número (más estricto) o con excepciones escritas en la fuente** | **0,45** | espacio 0,15 (canon 2 500 cm² frente a 750 legales y 1 667 ecológicos); crueldad 0,30 (0 % sin excepciones frente a prohibiciones que sí las traen) |
| **Piso del canon sin fuente externa: la magnitud no la publica ninguna fuente verificada** | **0,50** | movimiento «horas/día fuera» 0,15; bloque agua/alimentación (litros y % de dieta natural) 0,15; luz natural 0,10; socialización «gallinas/grupo» 0,10 |
| **Σ** | **1,00** | |

**Criterio de clasificación, explícito** (para que la cifra no se lea de dos maneras): **exacto** = una
fuente verificada publica un piso para **la misma magnitud** con **el mismo número**; **parcial** = una
fuente publica un piso para **la misma magnitud** con otro número —el del canon es más estricto— o con
**excepciones escritas**; **sin fuente** = **la magnitud del canon** no la publica ninguna fuente
verificada (horas al exterior, litros por ave, porcentaje de dieta natural, horas de luz natural, aves por
grupo). Y una regla que evita el autoengaño: **cuando un peso cubre varios parámetros, se clasifica por el
más débil.** Aplicada al arquetipo, eso deja el peso de la socialización (0,10) en «sin fuente» aunque
dentro de él los nidos sí tengan un piso del mismo tipo: el parámetro que manda en ese peso —gallinas por
grupo— no tiene fuente.

**Cómo se lee esta tabla, sin adornos.** El SDV-A **no es un estándar débil**: es un estándar **estricto
cuyos números todavía no son ciencia publicada**. Y la consecuencia práctica es exactamente la que el
documento 08 §8.4 fijó para el ecosistema: **sin cobertura completa del piso no se puede declarar
`cumple`.** De ahí la propuesta central de esta sección:

**Propuesta no ratificada — la tabla de sustitución de parameterización.** Donde el canon nombra un
parámetro y la ciencia no publica su número, **la dimensión no se abandona: se mide con el parámetro que
la fuente sí publica**, y la sustitución se declara una por una. No es un cambio del piso: es un cambio de
**cómo se mide el mismo propósito**, y va marcado como decisión doctrinal pendiente de ratificación.

| Parámetro del canon, sin fuente | Sustituto verificado de la **misma dimensión** | Fuente |
|---|---|---|
| 8 h/día fuera (D6) | Aberturas: *popholes* ≥ 35 × 40 cm y **≥ 2 m** de abertura total por 1 000 aves; **4 m²/ave** de superficie exterior, condicionados a 170 kg N/ha/año | UE, Directiva 1999/74/CE art. 4.1.3(b)(i) · Reglamento (CE) 889/2008 anexo III pt. 2 |
| 0,3 L/ave/día (D3) | **2,5 cm** de bebedero por ave; **1 tetina o copa por cada 10 aves** (≥ 2 al alcance) | UE, Directiva 1999/74/CE art. 4.1(b) |
| 30 % de dieta natural (D2) | **Origen**: pienso del propio predio o de unidades ecológicas de la misma región; **≤ 25 %** de pienso en conversión; prohibición de alimentación forzada y de promotores del crecimiento | UE, Reglamento (UE) 2018/848 anexo II parte II pts. 1.4.1 y 1.4.3.1 |
| 6 h/día de luz natural (D4) | **≥ 20 lux** sobre **≥ 80 %** del área y **≥ 6 h de oscuridad** con **≥ 1 tramo ininterrumpido ≥ 4 h** — verificado **solo en pollos de engorde**: la extrapolación a ponedoras es `[HIPÓTESIS]` | UE, Directiva 2007/43/CE anexo I pts. 6-7 |
| 5-25 gallinas/grupo (D5) | **1 nido por cada 7 aves** (o 1 m² de nido colectivo por máx. 120 aves). Para ponedoras **no existe umbral de tamaño de grupo verificado**; el único umbral de grupo verificado es del porcino (< 6 → +10 % de superficie; ≥ 40 → −10 %) | UE, Directiva 1999/74/CE art. 4.1(c) · Directiva 2008/120/CE art. 3.1(b) |

**Y las tres reglas que gobiernan la sustitución, para que no se convierta en una puerta trasera:**

1. **El sustituto es un mínimo ejecutable, no un certificado de cumplimiento del canon.** Una unidad que
   cumple el sustituto **no puede declararse `cumple`** en el sentido del SDV-A mientras el parámetro del
   canon siga sin medir: su estado es **`indeterminado`** (§8.4), con bandera de opacidad y obligación de
   instrumentar. Es la translación exacta del estado `indeterminado` que el documento 08 §8.4 creó para
   el ecosistema.
2. **El sustituto no puede ser más laxo que el piso del canon cuando el canon sí tiene número.** En el
   arquetipo, el canon fija 0,25 m²/ave y la ley 750 cm²: **el sustituto solo puede usarse como mínimo
   precautorio transitorio mientras el piso del canon no esté instrumentado**, y nunca para declarar
   cumplimiento con el SDV-A.
3. **La sustitución se publica en el registro** (T13): qué parámetro se midió, con qué fuente, y qué
   parámetro del canon quedó sin medir. **Una sustitución no declarada es una violación del estándar**,
   aunque el número sea correcto.

### 5.7 Ejemplo aplicado completo, con las dos parameterizaciones

**La unidad.** Una nave de ponedoras en suelo (sistema alternativo), un ciclo TA completo. **Los pisos no
son ilustrativos: son los citados.** Las **mediciones son ilustrativas**, construidas para que la
aritmética sea verificable a mano. La nave tiene: 9 aves/m² de área usable (1 111 cm²/ave), sin acceso a
parque exterior, iluminación continua sin horas de oscuridad programadas, 1,2 cm de bebedero por ave,
alimentación con pienso comprado fuera de la región, 90 aves por grupo, 10 cm de percha por ave, 150 cm²
de yacija por ave, sin zona de baño de polvo, y se practicó **corte de pico a los 3 días de edad** a todo
el lote.

**Ejemplo A — parameterización del canon (Cap. 9 §9.5).**

| Dimensión | Parámetro (canon) | Piso (canon) | Medición | Operador | `D` | Peso | Aporte |
|---|---|---|---|---|---|---|---|
| D1 Espacio vital | m²/gallina | 0,25 m² = 2 500 cm² | 1 111 cm² | `min` | (2500−1111)/2500 = **0,5556** | 0,15 | 0,0833 |
| D2 Alimentación | % dieta natural | 30 % | 20 % | `min` | (30−20)/30 = **0,3333** | 0,15 (bloque) | — |
| D3 Agua | L/día | 0,3 | **no medido** | `min` | `None` | (bloque) | — |
| **Bloque Agua/Alimentación** (`A = max_i D_i`) | | | | | **0,3333** | **0,15** | **0,0500** |
| D4 Luz y ritmos | h/día de luz natural | 6 | **0** | `min` | (6−0)/6 = **1,0000** | 0,10 | 0,1000 |
| D5 Socialización | gallinas/grupo | banda 5-25 | 90 | `range` | (90−25)/25 = **2,6000** | 0,10 | 0,2600 |
| D6 Movimiento | h/día fuera | 8 | **0** | `min` | (8−0)/8 = **1,0000** | 0,15 | 0,1500 |
| D7 Comportamiento natural | perchas (cm/ave) · baño de polvo (binario) | 15 · presente | 10 · **ausente** | `min` · `binary` | max(0,3333 · **1,0**) = **1,0000** | 0,05 | 0,0500 |
| D8 Crueldad | prácticas dolorosas | 0 % | **corte de pico a los 3 días, a todo el lote** | `binary` | **1,0000** | 0,30 | 0,3000 |
| **Total** | | | | | | **1,00** | **`v_A = 0,9933`** |

Suma, paso a paso y sin pasos ocultos: `0,0833 + 0,0500 = 0,1333`; `+ 0,1000 = 0,2333`;
`+ 0,2600 = 0,4933`; `+ 0,1500 = 0,6433`; `+ 0,0500 = 0,6933`; `+ 0,3000 = **0,9933**`.

**Ejemplo B — parameterización verificada (la ley), sobre la misma nave y las mismas condiciones.**

| Dimensión | Parámetro verificado | Piso (fuente) | Medición | `D` | Peso | Aporte |
|---|---|---|---|---|---|---|
| D1 Espacio vital | cm²/ave (sistemas alternativos) | **1 111 cm²** (9 aves/m², Directiva 1999/74/CE art. 4.1.4) | 1 111 cm² | **0** (cumple) | 0,15 | 0,0000 |
| D2+D3 Agua/Alimentación | origen del pienso (regla) · cm de bebedero/ave | propio predio o región · **2,5 cm** | **fuera de la región** · 1,2 cm | max(binaria **1,0** · 0,5200) = **1,0000** | 0,15 | 0,1500 |
| D4 Luz y ritmos | h de oscuridad (extrapolado de pollos de engorde, `[HIPÓTESIS]`) | **6 h** con ≥ 1 tramo ≥ 4 h | 0 h | (6−0)/6 = **1,0000** | 0,10 | 0,1000 |
| D5 Socialización | aves/nido | **7** (Directiva 1999/74/CE art. 4.1(c)) | 12 | (12−7)/7 = **0,7143** | 0,10 | 0,0714 |
| D6 Movimiento | aberturas al exterior | *popholes* ≥ 35×40 cm y ≥ 2 m/1 000 aves | **0** | binaria **1,0000** | 0,15 | 0,1500 |
| D7 Comportamiento natural | cm de percha · cm² de yacija · baño | **15** · **250** · presente | 10 · 150 · ausente | max(0,3333 · 0,4000 · **1,0**) = **1,0000** | 0,05 | 0,0500 |
| D8 Crueldad | intervenciones no terapéuticas | prohibidas **salvo** corte de pico < 10 días con asesoramiento veterinario | corte de pico a los 3 días → **permitido por la ley** | **0** | 0,30 | 0,0000 |
| **Total** | | | | | **1,00** | **`v_B = 0,5214`** |

Suma: `0,0000 + 0,1500 = 0,1500`; `+ 0,1000 = 0,2500`; `+ 0,0714 = 0,3214`; `+ 0,1500 = 0,4714`;
`+ 0,0500 = 0,5214`.

**Lo que el par de ejemplos demuestra, y es el resultado más importante de esta sección.**

1. **La misma nave cumple la ley y viola el canon, y la diferencia se puede medir: `0,9933 − 0,5214 =
   0,4719`.** De esa diferencia, **0,3000 son exactamente el peso de la crueldad**: un acto que la ley
   autoriza con condiciones y que el canon prohíbe en absoluto. **Ésa es la distancia entre el SDV-A y el
   derecho vigente, cuantificada** — y es la razón por la que el 0 % del canon debe declararse como
   decisión del proyecto (§4.11).
2. **Con el piso legal, la dimensión de espacio deja de violarse** (`D = 0`): 1 111 cm² es tres veces el
   piso legal y menos de la mitad del piso del canon. El estándar del proyecto es **1,5× más estricto que
   el ecológico y 3,3× más estricto que el legal** en esa dimensión, y eso no es un adorno: es la razón
   por la que el SDV-A **no puede presentarse como una certificación de cumplimiento legal**.
3. **Los dos ejemplos caen en el mismo escalón del Factor de Sufrimiento** (`v_A = 0,9933` y
   `v_B = 0,5214` → cumplimiento 0,7 % y 47,9 %, los dos por debajo del escalón del 50 % → **FS = 2,0**).
   **El factor no distingue el canon de la ley; el veredicto del piso sí.** Es exactamente la lección que
   el documento 07 §5.5 fijó para el ecosistema: *el factor no sustituye al piso*, y un `FS` idéntico
   puede esconder dos mundos distintos.
4. **Y el último escalón se activa en el Ejemplo A**: el corte de pico se aplicó **a todo el lote**, es
   decir, es una **violación sistemática**, y la tabla del canon la castiga con `∞` → **prohibición de
   mercado**, implementada como **estado**, no como cifra (§5.4).

### 5.8 Las propiedades formales de la fórmula (y sus tests)

| # | Propiedad | Enunciado | Test propuesto |
|---|---|---|---|
| **A1** | **Suma de pesos** | `abs(Σ pesos − 1,00) < 1e-9` sobre los siete pesos del canon | `test_pesos_sdv_a_suman_uno` |
| **A2** | **No-negatividad** | `D_i ≥ 0` para todos los operadores, incluidos `range` y `max` | `test_deficit_nunca_negativo_sdv_a` |
| **A3** | **Operador declarado** | ningún parámetro entra en la suma sin operador; `gallinas/grupo` es `range` | `test_parametro_sin_operador_rechazado` |
| **A4** | **Atomicidad** | un solo parámetro medido bajo su piso invalida el cumplimiento | `test_un_solo_parametro_bajo_piso_invalida_sdv_a` |
| **A5** | **Sin dato no imputa y no aprueba** | `None` no se convierte en 0 ni en violación; una cobertura incompleta no se declara `cumple` | `test_none_no_imputa_ni_aprueba_sdv_a` |
| **A6** | **Solo TA** | ninguna magnitud de duración acepta TVI ni TPI; `unidad_de_ciclo_ta` es obligatoria y sin default | `test_duracion_solo_ta_y_sin_default` |
| **A7** | **El `∞` es un estado** | ningún campo admite `inf` ni `NaN`; la violación sistemática produce `estado = PROHIBIDO` | `test_infinito_como_estado_no_como_numero_sdv_a` |
| **A8** | **El FC no decide el piso** | el peso numérico del FC altera el componente V y **no** el veredicto del piso; la compuerta `FC_estado` sí decide el ámbito | `test_fc_no_altera_el_veredicto_del_piso` |
| **A9** | **Compuerta de consciencia** | `EN DUDA` produce estado de protección precautoria (no violación imputada, no certificado) | `test_en_duda_protege_sin_imputar` |
| **A10** | **Acoplamiento** | ninguna asignación de carga puede declarar cumplido el SDV-A si el ecosistema contenedor está bajo su piso | `test_carga_no_puede_cruzar_piso_del_ecosistema` |
| **A11** | **Doble jurisdicción** | el resultado del SDV-A es invariante ante cualquier cambio del índice ecológico, y viceversa | `test_doble_jurisdiccion_invariante` |
| **A12** | **Sustitución declarada** | una medición con parameterización sustituta no produce estado `cumple` mientras el parámetro del canon siga sin medir | `test_sustituto_no_certifica_cumple` |

Ninguno de los doce tests existe. **Cero de doce**, y ése es el estado real (§12).

---

## 6. Protocolo de medición (instrumentos, frecuencias, quién reporta)

El SDV-A es el **único estándar de la familia cuyo protocolo existe y es a la vez insuficiente por
construcción**: existe, porque la etología y la inspección veterinaria tienen instrumentos desde hace
décadas; es insuficiente, porque **el que mide es el beneficiario** (Regla 7) y porque **el estándar
internacional del arquetipo no se pudo leer** (§6.4).

### 6.1 Admisibilidad de una medición

Se adopta, sin cambiarla, la regla que el documento [08](08_INV2-E_invariante.md) §6.1 fijó para el
ecosistema, porque el problema es el mismo —un número sin procedencia no es un juez, es un decorado—. Una
medición entra en una validación del SDV-A **solo si** trae los cuatro campos siguientes; si falta
alguno, el parámetro se trata como **no medido** (`None`), lo que produce cobertura faltante y **no**
violación:

| Campo | Para qué | Axioma |
|---|---|---|
| `valor` + `unidad` | el número y su unidad física, sin conversiones implícitas | — |
| `ta_periodo` (inicio y fin en **Tiempo Absoluto**) | la ventana temporal; sin ventana, el dato no es comparable | T7 (Cap. 5) |
| `fuente_dato` (tenedor con evidencia, entidad certificadora, veterinario, laboratorio, observación etológica con observador identificado) | procedencia verificable | T13 |
| `evidencia_ref` (identificador del registro original) | trazabilidad; es lo que impide un número sin origen | T13 |

**Regla dura derivada, y es la que más se va a querer saltar: la declaración del tenedor no es una
medición.** El tenedor **declara y aporta evidencia**; la medición la verifica **un tercero sin conflicto
de interés** (Cap. 9 §9.3: *«certificación por entidades sin conflicto de interés»*) `[VERIFICADO]`. Si el
único respaldo de un valor es la declaración del tenedor, el parámetro se marca `sin_evidencia` y el
estado es `indeterminado`. Es la versión animal de la regla del ecosistema *«el guardián consiente, no
mide»*.

### 6.2 Instrumentos y frecuencias por dimensión

| Dimensión | Instrumento | Unidad | Frecuencia mínima | Quién reporta |
|---|---|---|---|---|
| D1 Espacio vital | Cinta métrica y plano; conteo de animales; registro de niveles y alturas | cm²/ave · m²/animal | por ciclo y en cada cambio de lote | tenedor **+ verificación** de la entidad certificadora |
| D2 Alimentación natural | Composición de la ración; trazabilidad de origen (facturas, albaranes, certificado); registro de matadero para la retirada de pienso | % · regla · h | por lote | tenedor + entidad certificadora |
| D3 Acceso a agua | Medición de bebederos y tetinas; sonda de oxígeno disuelto en acuicultura | cm/ave · unidades/ave · % de saturación de O₂ | por ciclo; **en el momento de máxima carga** | tenedor + laboratorio o entidad certificadora |
| D4 Luz y ritmos | Luxómetro a la altura del ojo; registro del programa de luz | lux · % del área · h | por ciclo y en cada cambio de programa | tenedor + verificación en visita |
| D5 Socialización | Recuento y composición del grupo; relación recurso/ave; registro de reagrupaciones y de ventanas temporales | aves/grupo · aves/nido · cm²/ave | por lote y en cada reagrupación | tenedor + entidad certificadora |
| D6 Libertad de movimiento | Inspección de ataduras y geometría del corral; medición de *popholes*; registro de transporte | cm · m · h | en cada visita y **en cada transporte** | inspección veterinaria o entidad certificadora |
| D7 Comportamiento natural | Medición de yacija y perchas; observación directa de conductas (presencia/ausencia) | cm²/ave · cm/ave · binario | por ciclo, en **dos momentos del día** | observador identificado (etólogo o inspector) |
| D8 Ausencia de crueldad | Registro de intervenciones (tipo, edad, personal, supervisión); verificación del aturdimiento (movimiento corporal y opercular, VER, VOR); registro del método de sacrificio | binario · % | **por evento** | veterinario y matadero; entidad certificadora |

**Frecuencia: la fija el ciclo de vida de la especie, no la comodidad del calendario.** El documento
[06](06_Medicion_y_verificacion_T13.md) §11 lo dejó escrito en su tabla comparativa —*«en el SDV-A, un
ciclo biológico»*— y este documento lo confirma: la unidad de ciclo del SDV-A es una **configuración
obligatoria sin valor por defecto** (§5.5), y ninguna frecuencia puede prometerse por debajo del tiempo
en que la especie expresa el comportamiento que se quiere medir (una conducta de confort tiene hora; una
oscuridad ininterrumpida tiene que caber en el día).

### 6.3 Los tres huecos del protocolo, dichos antes de que los encuentre un lector

1. **El conflicto de interés del que reporta.** El tenedor es el beneficiario del resultado
   (documento 09 §11.2, eje 7). La mitigación propuesta no es retórica: **fuente de datos independiente
   del tenedor** para cada parámetro con piso (certificadora, veterinario, laboratorio, observación de un
   tercero identificado), **evidencia documental** para las reglas cualitativas, y **registro por evento**
   para la D8, que es la única dimensión donde el acto *es* la prueba.
2. **La certificación ecológica no es una certificación de bienestar animal.** El Reglamento (CE)
   889/2008 es la fuente verificada más rica del SDV-A y **es una norma de producción ecológica**: regula
   densidades, acceso exterior y origen del pienso, y **no certifica estado mental ni ausencia de
   crueldad** —de hecho, permite el corte de pico bajo condiciones—. Usarla como si fuera una
   certificación de bienestar sería el abuso de fuente más fácil de este documento.
3. **El estándar internacional del arquetipo no se pudo leer.** El capítulo 7.11 del Código Terrestre de
   la WOAH —bienestar de las ponedoras— **devuelve 403** en esta sesión y en la de la rama (§14.7); la
   opinión científica de la EFSA de 2023 sobre ponedoras, **también 403**. Consecuencia declarada:
   **ningún umbral que solo exista allí entra en este documento** (densidades máximas recomendadas,
   longitud óptima de percha, calidad de yacija). Es un hueco de fuente, no una decisión: **el SDV-A del
   arquetipo se apoya hoy en derecho de la UE y en la FAO, no en el código internacional.**

### 6.4 Quién reporta, en una frase, y por qué es el punto más débil

En el SDV-H reporta el sujeto; en el SDV-S, la instancia; en el SDV-E, **nadie puede**. En el SDV-A
reporta **el tenedor o la entidad que él contrata**, y el animal **no puede contradecirlo**. Ésa es la
diferencia entre un estándar que se audita y un estándar que se declara, y este documento la deja escrita
en lugar de resolverla con una recomendación de buenas prácticas.

---

## 7. Verificación y auditoría (T13, tutor, entidad certificadora y comunidad testigo)

### 7.1 Qué se audita y qué no

| Audita | No audita |
|---|---|
| Que un parámetro medido esté por debajo de su piso | El estado mental del animal como tal: **la WOAH define el bienestar incluyendo los estados mentales** `[VERIFICADO]`, y ningún instrumento los mide directamente |
| Que la medición tenga procedencia y ventana en TA (§6.1) | La intención del tenedor |
| Que una violación quede registrada y sea reproducible (T13) | El valor inefable del tiempo propio del animal (§10) |
| Que el Factor de Consciencia no altere el veredicto del piso (§5.8, A8) | La corrección científica de la escala de FC, que **no tiene fuente verificada** (§4.12) |

### 7.2 El elenco auditor, y su asimetría

| Reino | ¿Quién audita al sujeto del propio reino? | Fuente |
|---|---|---|
| SDV-H | Auditoría independiente y organismos sin conflicto de interés | Cap. 8 §8.6 |
| **SDV-A** | **Sí, con matiz: certificación por entidades sin conflicto de interés** — pero **el certificador lo paga el tenedor**, y el animal no puede impugnar | Cap. 9 §9.3 · documento 09 §11.2 |
| SDV-S | **AOS**: un par sintético independiente evalúa la deriva del auditado | Cap. 9.5 §9.5.6 |
| SDV-E | 🔴 **ninguno**: ningún ecosistema audita a otro ecosistema | documento 09 §7 |

**Lectura sin adornos:** de los cuatro reinos, el SDV-A es **el único cuyo auditor previsto por el canon
pertenece a la misma familia del auditado** —un certificador humano, pagado por el tenedor—, frente al
SDV-S, que tiene un **par sintético independiente** (AOS, §7.2), y al SDV-H, que tiene organismos sin
conflicto de interés. Eso añade **un conflicto de interés estructural en la cadena de pago**. Es un problema de diseño
institucional, no de fuente, y este documento no lo resuelve: propone la **comunidad testigo** como
segundo canal (observación de terceros no pagados por el tenedor: organizaciones de protección animal,
ciencia ciudadana, inspección pública) y lo marca como `[HIPÓTESIS]` operativa.

### 7.3 Trazabilidad (T13) y riesgos abiertos

Cada validación del SDV-A debe producir un registro con: estado, violaciones por parámetro, magnitud `v`,
cobertura medida, parámetros sin medición, **parameterización usada** (canon o sustituta, §5.6),
`unidad_de_ciclo_ta`, decisión de bloqueo y `evidencia_ref` de cada medición. El precedente de forma está
implementado en el motor para el SDV-H y el SDV-S (`_validation_log`, `get_validation_log()`, `to_dict()`)
`[VERIFICADO]`; **para el reino animal no existe nada** (§12).

**Riesgos abiertos del repositorio, y su traducción al SDV-A.** El registro de riesgos documentado
(`docs/architecture/blindaje_anti_gamificacion_equidad.md`) describe **R4** (partes fantasma), **R6** (T9
no se valida en la creación) y **R13** (guardián `eco-` con heurística laxa), y **los tres son del reino
natural, no del animal**: no hay ninguna entrada de riesgo específica para el SDV-A `[VERIFICADO]`. La
consecuencia se declara: **el riesgo propio del SDV-A no está registrado en ninguna parte**, y su forma
es conocida —el tenedor declara, el tenedor paga al certificador, el animal no impugna—. Propuesta:
registrarlo como riesgo nuevo en el mapa de blindaje, con el nombre que corresponda al proyecto, **no
inventando un identificador aquí**.

### 7.4 El árbol del Cap. 9 §9.7 y el proceso que sí encaja con el SDV-A

El Cap. 9 §9.7 propone una Base de Datos Universal de SDV con el proceso de creación **«por especie»**
(grupos de trabajo por especie, ciclos de revisión cada 3-5 años, revisión por pares, DOI, deliberación
democrática, traducción a políticas) `[VERIFICADO]`. El documento [09](09_Comparativa_inter_reinos.md) §5
señaló que **ese proceso es inaplicable al SDV-E**, porque una unidad ecológica no es una especie. Aquí
hay que decir lo contrario y es un dato de coherencia del canon: **el proceso «por especie» es exactamente
el correcto para el SDV-A**, y su árbol por taxón (`Mamíferos/Aves/Peces/Crustáceos`) sí describe la
población real de unidades del estándar. Lo que le falta al árbol no es forma: es **contenido** — hoja
por hoja, el árbol está vacío de umbrales (el único SDV-A desarrollado es el de gallinas, y §4.13 muestra
que siete de sus diez parámetros no tienen fuente externa —cifra por parámetro; la de §5.6 es por peso—).

---
## 8. Invariante INV2-E: de estándar a contrato ejecutable

El título de esta sección es el de la plantilla de la biblioteca, y aquí cumple dos funciones: dice lo que
el SDV-A **hereda** del invariante del reino natural y dice lo que el SDV-A **ya tiene y no puede
fingir que no tiene** —un invariante genérico, sin parámetros de especie—. Las dos cosas van separadas
porque confundirlas produciría el error más caro de este documento: creer que el estándar del animal
existe porque existe el bloque que valida el del humano.

### 8.0 Estado real, antes de una línea de especificación

| Pieza | Estado | Evidencia |
|---|---|---|
| **INV2-E** (invariante del ecosistema) | 🔴 **no existe** | documento [08](08_INV2-E_invariante.md) §8.0, verificado por lectura del repositorio |
| **INV2 genérico** (`validate_invariant_sdv`) | 🟢 **existe** | `maxocontracts/core/axioms.py` |
| **Bloque `SDVValidator`** | 🟡 **existe y es genérico** | `maxocontracts/blocks/sdv_validator.py`: recibe `dimension`, `actual_value`, `minimum_required`, calcula `deficit` y `relative` — **sin ningún parámetro animal** |
| **Parámetros por especie** | 🔴 **no existen** | no hay tabla de especies, ni umbral por especie, ni catálogo de parámetros del SDV-A en el motor |
| **Factor de Consciencia en código** | 🔴 **no existe** | `app/vhv_calculator.py::calculate_v_component` **acepta** `f_consciousness` y `f_suffering` como argumentos que aporta quien llama; **no hay tabla de FC ni escalera de FS** |
| **Estados del invariante del animal** | 🟡 **dos** (válido / violado) | documento 09 §11.1, tabla de invariantes |

**Consecuencia honesta:** todo lo que sigue es **propuesta**. Y hay una precisión que este documento debe
hacer porque afecta a la coherencia de la biblioteca: el documento [09](09_Comparativa_inter_reinos.md)
§11.1 registra **dos estados** para el invariante del animal; este documento **propone tres**, y lo
declara como **cambio propuesto**, no como estado actual (§13, pregunta 14).

### 8.1 Enunciado propuesto del invariante del animal

> **INV2-A (nombre de trabajo: INV2 aplicado al reino animal).** Ninguna acción de un contrato puede dejar
> a un animal por debajo de los mínimos medidos de su SDV-A; ninguna dimensión sin umbral con fuente puede
> declararse cumplida; y el cumplimiento del ecosistema que lo contiene **no lo sustituye, no lo compensa
> y no lo autoriza a cruzar su propio piso**.

Las tres cláusulas son distintas y las tres hacen trabajo: la primera es la del invariante genérico
**INV2** (*«Ninguna acción del contrato puede dejar a un participante bajo su SDV»*, Cap. 17) `[VERIFICADO]`;
la segunda es la que el documento 08 §8.4 descubrió para el ecosistema y que aquí aplica con la misma
fuerza; la tercera es la que este documento añade y que sólo tiene sentido porque **el animal vive dentro
de un ecosistema** (§4.14).

### 8.2 Los tres estados, y por qué el animal también los necesita

El animal no tiene sensores por especie, su certificación es pagada por el beneficiario y **siete de los
diez números del arquetipo no tienen fuente** (§4.13). Con dos estados, el sistema tendría que elegir
entre **imputar violaciones que no se midieron** (castigar al tenedor por un número que nadie publicó) o
**certificar cumplimientos que no se comprobaron** (premiar al tenedor por la ausencia de dato). Las dos
opciones son falsas, y son exactamente las dos que el documento 08 §8.4 rechazó para el ecosistema:

| Estado | Condición | Consecuencia |
|---|---|---|
| `cumple` | Todos los parámetros con piso del catálogo de la especie están medidos y **ninguno** está bajo su piso; sin violación binaria | factor de sufrimiento según la tabla (0,2 con cumplimiento pleno); **piso satisfecho** |
| `violacion` | Al menos un parámetro **medido** bajo su piso, o una dimensión binaria violada | bloqueo; registro (T13); avance del contador de escalada si está configurado |
| `indeterminado` | No hay violación medida **y** falta al menos un parámetro con piso | **no hay bloqueo por piso**; bandera de opacidad y **obligación de instrumentar**; **no habilita declaración de cumplimiento** |

**El estado por defecto del SDV-A hoy es `indeterminado`, y no es una hipérbole.** Con siete de diez
parámetros del arquetipo sin fuente externa y **cero** parámetros de cualquier otra especie en el
repositorio, ninguna unidad animal puede cubrir hoy su catálogo con fuente: **ninguna puede declararse
por encima de su suelo con el estándar del proyecto**, y sí puede declararse, en cambio, por encima del
piso legal (§5.7, ejemplo B). Esa asimetría —**la ley se puede certificar, el canon no**— es el resultado
más útil de esta sección.

### 8.3 Las dos vías de bloqueo

| Vía | Cuándo | Fundamento | Resultado |
|---|---|---|---|
| **Bloqueo por piso** | Hay violación medida (parámetro bajo su piso o dimensión binaria violada) | INV2 (Cap. 17) | bloqueo de la acción; registro; escalada según contador configurado |
| **Bloqueo precautorio** | No hay piso medido para una dimensión afectada **y** la acción propuesta es **irreversible** (mutilación, sacrificio, cambio de sistema de alojamiento, transporte de viaje largo) | **T14** (Cap. 5): menor irreversibilidad, **carga de la prueba sobre quien propone** | bloqueo precautorio con `evidencia_ref` del costo de oportunidad asumido |

La segunda vía es la respuesta de ingeniería a los siete parámetros sin fuente del arquetipo: **lo que no
tiene cifra no puede producir una violación, pero tampoco puede autorizarse a ciegas.** Y es coherente
con el canon hasta la letra: T14 no exige una medición, exige elegir la opción de menor irreversibilidad
y documentar el costo asumido. Para el SDV-A esto tiene un nombre concreto: **una mutilación no
autorizada por un umbral no se autoriza por la ausencia del umbral.**

### 8.4 La composición con INV2-E: la doble jurisdicción, en cuatro casos

Cuando un animal vive dentro de una unidad ecológica —el caso normal en ganadería—, **los dos invariantes
se aplican a la vez y ninguno absorbe al otro** (documento 18 §11.1). La tabla de composición, que es la
aportación operativa de esta sección:

| SDV-A | SDV-E | Veredicto | Quién bloquea |
|---|---|---|---|
| `cumple` | `cumple` | operable | nadie |
| **`violacion`** | `cumple` | **bloqueo** | el invariante del animal: un índice ecológico alto **no** promedia el sufrimiento de una gallina |
| `cumple` | **`violacion`** | **bloqueo** | INV2-E: un SDV-A cumplido **no** sustituye el piso del suelo |
| `indeterminado` en cualquiera de los dos | | **no habilita declaración de cumplimiento** ni crédito; obligación de instrumentar | la bandera de opacidad de cada estándar |

**Y la regla de ajuste, que es la única salida:** cuando los dos pisos no caben, **la variable de ajuste es
la actividad humana**, no ninguno de los dos pisos (§4.14, regla 3). Se reduce la carga; no se recorta el
piso de nadie.

### 8.5 El objeto de la consecuencia nunca es el animal

Se adopta la propiedad **P6** del documento [08](08_INV2-E_invariante.md) §8.3 y §8.7, con la forma
propia del reino animal, que el canon ya escribió: **la prohibición de mercado** (Cap. 9 §9.8). El
paralelo con el ecosistema es exacto —allí *«la única acción ejecutable de INV2-E es detener o modificar la
actividad humana que viola el piso»*— y aquí se formaliza igual:

```
objeto_de_la_consecuencia ∈ {"contrato", "actividad", "mercado", "ninguno"}   # nunca "animal"
estado_maximo             ∈ {"operable", "bloqueado", "PROHIBIDO"}            # ∞ como estado, no como cifra
```

**Un animal no se retracta, no se rehabilita por contrato y no se sanciona.** Lo que se interrumpe es la
causa: el contrato, la actividad o el acceso al mercado. `[HIPÓTESIS]` en la forma exacta de los campos;
el principio (el `∞` del SDV-A es una prohibición de mercado) es canon.

### 8.6 Ciclos y escalada: el patrón se replica, el número no

El contador de ciclos consecutivos del SDV-S (`max_consecutive_cycles = 7`) **no se hereda**, por las
mismas tres razones que el documento 08 §8.6 fijó para el ecosistema y una cuarta propia de este estándar:

1. **El ciclo no es la misma clase de objeto.** Los siete ciclos del SDV-S se cuentan en horas TPI de un
   agente de cómputo; en el SDV-A el ciclo es **un período biológico en TA** (§5.5).
2. **T14 prohíbe tolerar lo irreversible.** Un contador que retrasa el bloqueo siete ciclos biológicos
   puede significar siete ciclos de mutilación o de hacinamiento.
3. **La consecuencia ya es inmediata** para la vía del piso: el bloqueo llega con la primera violación
   medida (propiedad A4). El contador gobierna sólo la **escalada** (prohibición de mercado).
4. **La cuarta, propia del SDV-A: la vida del animal es más corta que la del ecosistema.** En muchas
   especies de producción, un ciclo biológico **es la vida entera**: un contador de siete ciclos puede
   ser un contador que nunca se activa. Este documento lo declara como razón adicional para no heredar el
   número `[HIPÓTESIS]`, y propone que `max_consecutive_cycles` sea **configuración obligatoria y sin
   valor por defecto**, con su valor ratificado por POLÍTICA (categoría `critical`).

### 8.7 Lo que este documento NO autoriza a concluir

1. **No autoriza a decir que el invariante del animal está implementado.** El bloque `SDVValidator` es
   genérico y no tiene un solo parámetro de especie (§8.0, §12).
2. **No autoriza a usar el piso legal como si fuera el piso del SDV-A.** El ejemplo B de §5.7 demuestra
   que la misma nave **cumple la ley y viola el canon**: certificar la ley como si fuera el estándar del
   proyecto sería el fraude más fácil de este documento.
3. **No autoriza a tratar `indeterminado` como cumplimiento.** Un estado indeterminado es una obligación
   de instrumentar, no un certificado.

---

## 9. El suelo antes que el saldo (no compensación)

**La doctrina es la misma de la familia y en el SDV-A tiene una forma propia y ya canónica: el que viola
sistemáticamente no paga más — sale del mercado.** Pero antes de la consecuencia está la regla, y la
regla se puede escribir en una frase ejecutable:

> **El crédito regenerativo no entra en la ecuación del SDV-A.** No reduce la violación, no la compensa,
> no aplaza el bloqueo, no reinicia el contador y no habilita el perdón.

**Por qué es una consecuencia formal y no un acuerdo de caballeros.** La fórmula (a) del canon
—`Σ[(req − actual) × Peso × Duración]`— y el componente V —`Σ(Seres × FC × FS × FA × FR)`— **no tienen un
término de crédito**. Un crédito de −12,0 R o de −12 000 R produce la misma magnitud y el mismo veredicto:
**la variable no existe en la expresión**. Y el motor ya aplica la misma asimetría al componente V del
hogar: *«`v_ucv` sigue sin admitir negativos: una vida afectada no se des-afecta en la misma cuenta»*
`[VERIFICADO]` en `app/micromax.py` (`if v_ucv < 0: raise ValueError`), con el crédito regenerativo
viviendo en **R**, que sí admite negativos (EVV-1.2 §4.3). Trasladado al animal: **el daño se acumula y el
cuidado no lo resta.**

**Las cuatro formas de compensación que este documento prohíbe, y una que permite:**

| Forma de compensación | ¿Válida? | Razón |
|---|---|---|
| Pagar más por un producto obtenido con violación (el factor sube el precio) | **No** como reparación | el precio **encarece la siguiente**, no devuelve la vida: el canon lo dice con dos columnas distintas (factor de sufrimiento y prohibición de mercado) |
| Comprar crédito regenerativo ecológico para saldar el sufrimiento de un animal | **No** | **no compensación cruzada de reinos**: son dos estándares y dos pisos (§4.1, §8.4) |
| Cumplir el SDV-A para compensar el piso del ecosistema | **No** | documento 18 §11.1: un SDV-A cumplido no sustituye el piso del suelo |
| Declarar «bienestar» en la etiqueta lo que la medición no registró | **No** | *«cuidado ≠ extracción estética… se registra lo que regenera, no lo que adorna»* (Cap. 16.5 §16.5.14): una etiqueta no cierra una herida |
| **Financiar la mejora por encima del piso** (más espacio, más perchas, acceso exterior, enriquecimiento ambiental) | **Sí** | es restauración y es valiosa: el lugar del gasto es **por encima del piso**, nunca **por debajo** |

**Y una advertencia que el SDV-A necesita y los otros reinos no.** En el SDV-E el remedio no existe
(*«la pérdida no vuelve en el mismo TA»*, documento 09 §9). En el SDV-A el remedio existe **a medias y sólo
hacia adelante**: se puede mejorar el alojamiento del animal que vive, y **no se puede devolver la vida del
que murió ni el pico del que fue mutilado**. Por eso el canon no ofrece rehabilitación al animal: ofrece
**prohibición de mercado**. En la escalera del remedio de la familia, el SDV-A es el segundo escalón —no
repara, **impide la siguiente**— y este documento lo deja escrito sin suavizarlo.

---

## 10. Zona Libre: lo que NO se mide

**Qué es, en el SDV-A.** El canon ya nombra la Zona Libre del reino animal en su forma propia: **«no
interferencia invasiva»** y **expresión del comportamiento natural** (Cap. 9.5 §9.5.11, recogido en el
documento 09 §10), y el documento [03](03_No_colonizacion_del_TA.md) §11 la registra como **«tiempo propio
no observado»**. Las tres formulaciones dicen lo mismo: **hay una parte de la vida del animal que el
estándar no mide, y no medirla es una decisión doctrinal, no una carencia de instrumentos.**

**Cómo entra: dimensión binaria auditable sin peso.** Se adopta el precedente canónico de las dimensiones
VIII (Rehabilitación) y IX (Opacidad Vital) del SDV-H —*«se registran cualitativamente y mediante umbrales
binarios (presencia/ausencia del derecho), no mediante pesos en la fórmula — medir la rehabilitación o la
opacidad con la misma vara cuantitativa que el agua o la vivienda las destruiría»* (Cap. 8 §8.11)— y su
aplicación al ecosistema en el documento [04](04_Zona_Libre_del_Reino_Natural.md):

| Aspecto | Regla del SDV-A |
|---|---|
| Peso en la fórmula de violación | **cero**, por construcción: la Zona Libre no está en la tabla de pesos del canon |
| Registro | obligatorio, con evidencia y con la declaración de qué **no** se mide (T13) |
| Efecto sobre el estado | una violación de Zona Libre **sí** produce estado de violación (es un derecho binario: presencia o ausencia) |
| Cuantificación | prohibida: no se le asigna magnitud ni se canjea contra otras dimensiones |
| Perímetro de lo inefable | 🔴 **decisión no ratificada**: qué entra en el catálogo en cada especie lo vota la comunidad de custodia |

**La frontera LEY / POLÍTICA, explícita.** **LEY y no se vota**: que exista una Zona Libre en el SDV-A y
que **no se pondere** — ponderarla la volvería canjeable contra el piso, que es exactamente lo que «el
suelo antes que el saldo» prohíbe. **POLÍTICA y se vota**: **qué entra en ese catálogo** para cada especie
se decide deliberativamente con la categoría `critical` (quórum 60 %, consenso 75 %, T13, anti-flip-flop
de 14 días, `CHECK` en base de datos), igual que la plenitud aspiracional. Sin esa separación, «declarar
inefable» sería la vía más barata para vaciar el estándar.

### 10.1 El límite duro: la Zona Libre no puede tragarse una violación del piso

Éste es el aporte de esta sección, y es la corrección que el SDV-A necesita más que ningún otro estándar
de la familia:

> **Una violación del piso es un hecho documentable y la Zona Libre no la absorbe.** El catálogo de lo
> inefable puede cubrir el **interior** de la vida del animal —su tiempo propio, su experiencia no
> observada, su comportamiento cuando nadie mira— y **no puede cubrir los actos que el estándar prohíbe**:
> una mutilación, un sacrificio sin aturdimiento, un aislamiento, una atadura. Ésos no son intimidad: son
> **hechos con autor, fecha y responsable**.

Sin esta regla, «no interferencia invasiva» se convertiría en la coartada perfecta: bastaría declarar
inefable lo incómodo de medir para que el 0,30 de peso de la crueldad quedara sin contenido. El SDV-A es
el estándar donde esa puerta trasera es **más peligrosa** que en el ecosistema, porque aquí el que
declararía lo inefable es **el beneficiario de no medirlo** (Regla 7).

### 10.2 La Zona Libre del animal tiene una segunda cara: medir cuesta bienestar

El documento [03](03_No_colonizacion_del_TA.md) §11 dejó escrito, para el ecosistema, que *«el SDV-E es el
único reino cuya transparencia puede volverse vigilancia»*. En el SDV-A la misma idea toma una forma
**física y verificable**: **la observación entra en el espacio del animal.** Una inspección con personal
dentro del corral, un manejo para medir, una sujeción para pesar o un cambio de rutina para observar una
conducta **son perturbaciones**, y su costo no desaparece porque el motivo sea noble.

**Propuesta `[HIPÓTESIS]`, no ratificada:** que el protocolo de medición del SDV-A declare, junto a cada
parámetro, **el costo de intrusión de la propia medición** (número de visitas, manejo requerido,
inmovilización necesaria), y que ese costo se registre con T13 como parte del ciclo. No es una
suspensión del deber de medir: es la admisión de que **en este reino el instrumento también toca al
sujeto**, cosa que no ocurre con un satélite sobre un humedal.

---

## 11. Comparativa inter-reinos (SDV-H · SDV-A · SDV-E · SDV-S)

La comparación completa de los cuatro estándares es el documento [09](09_Comparativa_inter_reinos.md)
—16 ejes—. Aquí se compara **la columna del SDV-A** consigo misma y con las otras tres, y se extraen los
siete hallazgos que este documento añade.

### 11.1 La columna del SDV-A, eje por eje

| Eje | Valor en el SDV-A | Fuente |
|---|---|---|
| **Sujeto** | Individuo de una especie sintiente; la especie como portadora de diversidad genética | Cap. 9 §9.1, §9.2.1 |
| **Qué protege** | Espacio vital, alimentación natural, agua, luz y ritmos circadianos, socialización, movimiento, comportamiento natural, ausencia de crueldad | Cap. 9 §9.4 Fase 2 |
| **Escala** | **Por especie** — unidad que existe antes del estándar | Cap. 9 §9.9 |
| **Unidad de medida** | m²/animal · cm/ave · aves/nido · h/día · % · kg/m³ · binario | Cap. 9 §9.5 + derecho verificado |
| **Moneda temporal** | **TA**, traducido por el PIU | documento 09 §11.1, eje 6 |
| **Duración de la violación** | **Configuración obligatoria sin valor por defecto** (§5.5); el canon no la especifica | documento 09 §8, requisito 1 |
| **Representación** | La persona o el **tutor legal**; riesgo principal declarado: **conflicto de interés del tutor** | documento 09 §11.2, eje 7 |
| **Factor** | Tabla escalonada 0,2 · 0,5 · 1,0 · 2,0 · ∞ — **precio del consumo**, sin base neutra | Cap. 9 §9.8 · documento 09 §5.2 |
| **Invariante** | `SDVValidator` con parámetros por especie 🟡 | documento 09 §11.1 |
| **Quién audita** | Certificación por entidades **sin conflicto de interés**… pagadas por el tenedor | Cap. 9 §9.3 |
| **Remedio tras la violación** | **Prohibición de mercado** si es sistemática; **no devuelve la vida** | Cap. 9 §9.8 · documento 09 §9 |
| **Zona Libre** | «No interferencia invasiva»; tiempo propio no observado; **sin peso** | Cap. 9.5 §9.5.11 · documento 03 §11 |
| **Origen del piso** | **Diseño biológico + etología científica** | Cap. 9 §9.3, §9.9 |
| **Piso con fuente externa (peso)** | **0,05 exacto · 0,45 parcial · 0,50 sin fuente** (§5.6) | este documento |
| **Estado** | 🟡 **capítulo de libro, sin documento de estándar y sin código** | §12 |

### 11.2 Los siete hallazgos de la comparación

**I1 — Es el único estándar cuyo reportero es el beneficiario.** En el SDV-H y el SDV-S el sujeto declara
su estado; en el SDV-E nadie puede. En el SDV-A declara **el tenedor**, que se beneficia del resultado, y
el certificador lo paga él. La inversión del principio INV2-EDU que el documento 09 §6 (insight I9)
describió para el ecosistema es aquí **parcial y más insidiosa**: en el ecosistema la duda no castiga a
nadie porque nadie reporta; en el SDV-A la duda **favorece exactamente a quien tiene el incentivo de no
medir**.

**I2 — Es el único cuyo factor es un precio y no una penalización.** Con cumplimiento pleno, el factor
vale **0,2**, no 1,0 (documento 09 §5.2, insight I5). No es un defecto de calibración: **consumir una vida
cuesta aunque se haga bien**. Y tiene una consecuencia de diseño que este documento subraya: el SDV-A es
el único estándar de la familia en el que **el cumplimiento perfecto no es gratis**, lo que hace de la
reducción del consumo —no sólo de la mejora de la práctica— una palanca del propio estándar.

**I3 — Es el único cuyo canon excede sistemáticamente el derecho vigente, y la diferencia se puede
medir.** Tres lugares verificados: el espacio vital del arquetipo (**0,25 m²/ave = 3,33× el piso legal**
de 750 cm² y **1,5× el ecológico** de 1 667 cm²); el **0 % de crueldad** frente a las dos prohibiciones
absolutas verificadas, que **traen excepción escrita**; y los **5 gallinas/nido** frente a las 7 de la
ley. El ejemplo de §5.7 cuantifica el efecto conjunto sobre una nave concreta: **0,4719 de magnitud de
violación**, de los cuales **0,3000 son el peso de la crueldad**. Ningún otro estándar de la familia tiene
esta propiedad, y de ella se sigue una obligación de honestidad: **el SDV-A no puede venderse como una
certificación de cumplimiento legal.**

**I4 — Es el único estándar cuyo ámbito de aplicación está él mismo en duda.** El SDV-H sabe quién es su
sujeto; el SDV-S tiene cuatro criterios explícitos (Cap. 10 §10.8); el SDV-E constituye el suyo con
C1-C5; el SDV-A **depende de una compuerta científica abierta**: qué seres son sintientes (§4.12). Y el
canon resuelve la duda con un principio, no con una tabla: *«Donde hay duda de consciencia, se asume
consciencia»* (Cap. 10 §10.3). El SDV-A es, por eso, el único estándar cuya **primera decisión es
epistémica y no métrica**.

**I5 — El SDV-E es su hijo epistemológico, y el banco de pruebas del TA es el SDV-A.** El documento 09
(insight I1) estableció la genealogía: comparten la fuente del piso (diseño biológico) y el tiempo (TA), y
se separan en la unidad (especie frente a ocurrencia ecológica) y en la reversibilidad. El documento
[03](03_No_colonizacion_del_TA.md) §11 aceptó la propuesta del documento 09 §11.3 —**probar primero el
test de no colonización del TA sobre el SDV-A**, que ya existe y comparte el tiempo—. **Este documento
declara el estado de esa propuesta: el test no existe todavía**, y §5.5 fija lo único que se puede fijar
sin él (la duración en TA y la unidad de ciclo como configuración obligatoria sin default). Un test que
no existe no es una cobertura (documento 07 §13, pregunta 15).

**I6 — La doble jurisdicción.** Dos pisos sobre el mismo metro cuadrado, ninguno absorbible por el otro,
con la variable de ajuste en la actividad humana (§4.14, §8.4). El hallazgo nace en el documento
[18](18_Ecosistemas_Agroecosistemas.md) §11.1 y este documento lo formaliza como regla de composición de
invariantes.

**I7 — La cobertura del piso del SDV-A es la imagen especular de la del SDV-E, por una razón distinta.**
El SDV-E ejecuta hoy su piso sobre **0,925** del peso que declara proteger (documento 07 §5.3; 0,680 en el
catálogo del documento 08) y **le falta instrumento**: sensores, caudal, conectividad. El SDV-A ejecuta
**0,05 exacto, 0,45 parcial y 0,50 sin fuente** (§5.6) y **le falta número publicado**: no necesita más
sensores que un luxómetro y una cinta métrica; necesita **que la ciencia publique los pisos de los
parámetros que el canon ya escribió**. Es la misma herida en dos cuerpos distintos, y por eso los dos
estándares comparten la misma respuesta: **publicar la cobertura, no renormalizarla en silencio.**

### 11.3 Qué aprende el SDV-A de cada reino (y qué no hereda)

| De | Aprende | Y **no** hereda |
|---|---|---|
| **SDV-H** | (1) Separar **Mínimo Absoluto** de **Óptimo** en dos columnas. (2) **Dimensiones binarias sin peso** para lo inconmensurable (Cap. 8 §8.11). (3) Los **cinco criterios de validación** de parámetros (Cap. 9 §9.3, heredados del Cap. 8 §8.3). (4) Que **los pesos suman 1,0** y la fórmula es una suma ponderada. | No hereda el **TVI**: el tiempo del animal es TA. No hereda la fuente del piso (dignidad y capacidades), sino el diseño biológico. No hereda la **rehabilitación**: al animal no se le rehabilita, se le deja de dañar. |
| **SDV-E** | (1) El **déficit normalizado** con operador y saturación en 0 (documento 07 §3.3). (2) Los **tres estados**, con `indeterminado` para la falta de medición (documento 08 §8.4). (3) La **cobertura del piso declarada** como cifra publicada (documento 07 §5.3). (4) La **no compensación** y la **prelación del piso sobre la banda** (documento 07 §5.7, §5.9). (5) Que el **`∞` es un estado** y que el **objeto de la consecuencia nunca es el sujeto protegido** (documento 08 §8.7). | No hereda la **base neutra 1,0**: su factor es un precio y vale 0,2 con cumplimiento pleno. No hereda la unidad del sujeto: especie frente a ocurrencia. |
| **SDV-S** | (1) La **unidad de duración explícita**: sin ella el factor no es comparable. (2) El **contador con umbral** para la escalada, con configuración explícita. (3) La **trazabilidad** con registro que no se borra (T13). | No hereda los **7 ciclos** (§8.6). No hereda la **base neutra**. Y no tiene —ni puede tener— su **par auditor**: el SDV-S tiene AOS; el SDV-A tiene un certificador pagado por el beneficiario. |
| **Su propio canon (Cap. 9)** | El **arquetipo** de «dimensiones genéricas y umbrales por especie», que el SDV-E copió después por tipo de ecosistema (documento 09 §11.6). El **árbol por taxón** del Cap. 9 §9.7, que para este estándar **sí es la forma correcta**. El proceso de creación por especie (grupos de trabajo, revisión cada 3-5 años, DOI, deliberación) del Cap. 9 §9.7. | **No hereda la tabla de FC como escala continua** sin declarar su contradicción interna (§4.12). **No hereda los pesos como intocables**: están publicados sin fuente y su cambio es POLÍTICA. **No hereda el «70 mil millones»** del Cap. 9 §9.1 como cifra: va sin referencia y no se pudo verificar (§13, pregunta 5). |

### 11.4 Lo que el SDV-A aporta a la familia (y que la biblioteca ya reconocía en parte)

1. **El arquetipo de estandarización por sujeto**: dimensiones genéricas y umbrales específicos. Es el
   precedente formal que el SDV-E copió después **por tipo de ecosistema** (documento 09 §11.6) y el que
   el SDV-H no tenía.
2. **La única pareja piso/plenitud con fuente externa verificada de toda la familia** —y hay dos—:
   espacio **750 cm² → 1 667 cm²** (2,22×) y percha **15 cm → 18 cm** (1,20×). Sirven, además, como
   prueba empírica de la heurística de calibración «Óptimo = 2-3× Mínimo» que el documento 09 §11.6
   detectó: **compatible, no confirmada**.
3. **El `∞` como consecuencia jurídica**: la prohibición de mercado. Es la mitad de la doctrina que el
   documento 09 §5.3 usó para fijar que la parte infinita de un factor se implementa **como estado**.
4. **La compuerta de consciencia**: el único mecanismo de la familia que decide **si un ser entra en el
   ámbito de protección** con un principio precautorio en lugar de con una lista cerrada (§4.12). Es la
   aportación más original del canon de los animales y la que el resto de la familia no tiene.
5. **La doble jurisdicción** (§11.2, I6) y la **regla de ajuste sobre la actividad humana** (§4.14): dos
   pisos, ningún recorte, una sola variable de ajuste.

---

## 12. Estado de implementación

**Verificado por lectura directa del repositorio y del libro en esta sesión (octubre 2026).** La regla es
la de la biblioteca: 🔴 es 🔴. **Está prohibido afirmar que el SDV-A, su tabla de especies, su tabla de
Factor de Consciencia o su invariante están implementados: no lo están.**

### 12.1 Lo que SÍ existe (y es honesto decir que existe)

| Pieza | Dónde | Estado |
|---|---|---|
| **El SDV-A como doctrina escrita** | `docs/book/edicion_3_dinamica/capitulo_09_sdv_a_260126.md` (317 líneas, edición 3.2, 26-1-2026) | 🟢 **existe y se leyó completo**: 8 dimensiones, FC A/B/C/D, SDV-Gallinas, fórmula, pesos, FS, árbol |
| Bloques genéricos de validación de SDV | `maxocontracts/blocks/sdv_validator.py` | 🟢 **existe y funciona** para el SDV-H: `deficit`, `relative = deficit / required`, `severity_thresholds` (0,10 / 0,30 / 1,0) |
| Invariante genérico INV2 | `maxocontracts/core/axioms.py` (`validate_invariant_sdv`) | 🟢 existe |
| **Hueco matemático del FC y del FS** | `app/vhv_calculator.py::calculate_v_component` | 🟡 **existe la firma, no los datos**: multiplica `organisms_affected × f_consciousness × f_suffering × f_abundance × f_rarity`, **todos aportados por quien llama**. No hay tabla de FC por especie ni escalera de FS en el código |
| V no admite negativos | `app/micromax.py` (`if v_ucv < 0: raise ValueError`) | 🟢 invariante de diseño real, aplicable al componente V del SDV-A |
| Trazabilidad de validaciones | `SDVValidatorBlock` / `SDV_SValidatorBlock` (`_validation_log`, `to_dict()`) | 🟢 precedente reutilizable |
| **Verificación HTTP de las fuentes de este documento** | 23 URL comprobadas en esta sesión | 🟢 20 responden 200 · 2 responden 403 · 1 responde 404 (declarada en §14.7) |

### 12.2 Lo que NO existe (y está prohibido afirmar que existe)

| Pieza | Estado | Evidencia |
|---|---|---|
| **Documento de estándar del SDV-A en `docs/theory`** | 🔴 **no existe** | búsqueda por patrón de nombres en `docs/theory`: hay `SDV-H…txt`, `SDV-S…md` (dos), compilaciones y papers; **ningún archivo de SDV-A**. Este documento es el primero |
| **Tabla de especies** | 🔴 **no existe** | no hay catálogo de parámetros por especie en ningún módulo |
| **Tipo `SDV_A`** | 🔴 **no existe** | `maxocontracts/core/types.py` define **`SDV`** (línea 139) y **`SDV_S`** (línea 242); **no hay `SDV_E` ni `SDV_A`** |
| **Umbrales del SDV-A en código** | 🔴 **ninguno** | `sdv_validator.py` es **genérico**: `dimension`, `actual_value`, `minimum_required`, `deficit`, `severity`. **No tiene un solo parámetro animal** |
| **Tabla del Factor de Consciencia** | 🔴 **no existe** | ni en `maxocontracts/`, ni en `app/` |
| **Escalera del Factor de Sufrimiento** | 🔴 **no existe** | la tabla 0,2 · 0,5 · 1,0 · 2,0 · ∞ solo vive en el libro |
| **Pesos dimensionales del SDV-A** | 🔴 **no existen** en código | los siete pesos del Cap. 9 §9.5 no están en ningún módulo |
| **Invariante del animal** (`validate_invariant_sdv_a` o equivalente) | 🔴 **no existe** | `axioms.py` tiene INV2 (humano), INV2-S, INV2-EDU, INV1, INV3, INV4; **ninguno con parámetros de especie** |
| **Bloque validador con parámetros por especie** | 🔴 **no existe** | el guard por especie no está escrito en ninguna parte |
| **Tres estados para el animal** | 🔴 **no existen** (hoy el patrón tiene dos) | propuesta de este documento (§8.2) |
| **Regla de acoplamiento SDV-A ↔ SDV-E** | 🔴 **no existe** | ninguna pieza del motor relaciona la carga animal con el piso del ecosistema: ni el 170 kg N/ha/año, ni la prelación, ni la composición de invariantes |
| **Doble jurisdicción en el motor** | 🔴 **no existe** | no hay ningún punto del código donde dos SDV se apliquen a la vez sobre el mismo territorio |
| **Protocolo de medición instrumentado** | 🔴 **nada** | cero ingestores, cero integraciones de certificación, cero registros de evento para intervenciones o sacrificios |
| **Registro de riesgos del reino animal** | 🔴 **no existe** | `docs/architecture/blindaje_anti_gamificacion_equidad.md` documenta **R4, R6 y R13**, los tres del reino natural; **ninguna entrada para el SDV-A** |
| **Tests** | 🔴 **0 de 12** | las doce propiedades A1-A12 de §5.8 no tienen un solo test escrito |

### 12.3 Dos notas de lectura que evitan un error grave

1. **Colisión de nombres, declarada.** La única clase del repositorio cuyo nombre se parece al estándar de
   los animales es `app/sdv_analyzer.py::SDVAnalyzer`, y **no es el SDV-A**: es el analizador del **SDV
   humano** —calcula `SDVScore`, aplica el puente educativo `INV2-EDU` (`educacion_indice`) y estima el SDV
   de una persona participante— `[VERIFICADO]`. Un lector que vea «SDVAnalyzer» y lea «SDV-A» se llevará
   la impresión falsa de que el estándar de los animales existe en código. **No existe.**
2. **La `r_units` negativa no es una pieza del SDV-A.** El crédito regenerativo está implementado en la
   contabilidad doméstica y **no tiene ningún consumidor** (documento 08 §9.1); no lee, no pesa y no
   compensa nada del estándar de los animales. Se dice aquí porque es la confusión más probable al cruzar
   los dos documentos.

### 12.4 Estado real, en una frase

**El SDV-A es hoy un capítulo de libro bien construido, una columna en doce documentos de esta biblioteca
y cero líneas de código; su arquetipo tiene diez parámetros, de los cuales siete no tienen fuente externa
verificada, y su única pareja piso/plenitud verificada mide 15 cm de percha.** Este documento no cambia
ese estado: lo hace legible, y publica lo que habría que construir para cambiarlo.

---

## 13. Preguntas abiertas

Lo que **no** sé, y no finjo cerrar. Las cinco primeras son **contradicciones o vacíos del propio canon**,
localizados y verificados; el resto son decisiones que este documento **no puede tomar solo**.

1. **¿Cuál es el piso del espacio vital de la gallina?** El Cap. 9 §9.5 fija **0,25 m² como Mínimo y
   0,75 como Óptimo**; el paper de Ontometría Vital fija **`SDV_Espacio_Vital ≥ 0,75 m²` como umbral del
   SDV**, es decir, como **piso** `[VERIFICADO]` por lectura directa de los dos archivos del repositorio.
   **Los dos textos se contradicen y no sé cuál rige.** Es la contradicción más costosa de todo el SDV-A:
   decide si el arquetipo exige 2 500 cm² o 7 500 cm² por ave.
2. **¿Cuál es la escala vigente del Factor de Consciencia?** El Cap. 9 §9.2.2 da **plantas 0,0** e
   **insectos 0,1-0,2**; `docs/theory/matematicas_maxocracia_compiladas.md` da **plantas 0,1** e
   **insectos 0,3-0,5** `[VERIFICADO]`. Hasta 2,5× de diferencia en el mismo factor, y **ninguno de los dos
   tiene fuente externa**. No sé cuál es el vigente y este documento no lo elige.
3. **¿El Factor de Consciencia es de la especie o del individuo?** El canon lo publica por categorías
   («mamíferos, aves, cefalópodos») y lo aplica a «cada ser». Un individuo concreto de una especie de
   Nivel A no es idéntico a otro, y el estándar no dice qué hacer con esa variación. **No tengo fuente ni
   decisión del canon.**
4. **¿Dónde queda exactamente la frontera de `EN DUDA`?** Mi propuesta deja en `EN DUDA` a los insectos,
   los moluscos simples y el resto de invertebrados, y **no tengo fuente** para decidir si eso incluye,
   por ejemplo, a los crustáceos no decápodos. La ley verificada incluye decápodos y excluye al resto
   `[VERIFICADO]`; **la duda razonable no está cartografiada por ningún organismo**.
5. **El «más de 70 mil millones de animales de granja sacrificados cada año» del Cap. 9 §9.1 no tiene
   referencia y no se pudo verificar.** Se buscó en fuentes institucionales abiertas en esta rama y **no se
   encontró cifra verificable**: este documento **no la repite como propia** y la marca
   `[SIN FUENTE VERIFICADA]`. Si alguien la va a usar, que traiga la fuente.
6. **El 0 % de crueldad contra la libertad religiosa.** El Reglamento (CE) 1099/2009 art. 4.4 exceptúa del
   aturdimiento previo a los ritos religiosos en matadero `[VERIFICADO]`, y el canon fija un **0 %
   absoluto e irrenunciable**. **Las dos cosas no caben a la vez** y la resolución no es técnica: es
   deliberación política con un conflicto de derechos encima. Este documento **no la resuelve**: registra
   el conflicto y deja el piso del canon como **decisión del proyecto pendiente de ratificación**.
7. **La unidad de duración del ciclo TA por especie.** Candidata natural: el ciclo biológico o productivo
   de la especie; alternativa: el año TA del territorio. **Ninguna tiene fuente** y elegirla por comodidad
   sería colonizar el tiempo del animal (§5.5). Queda como configuración obligatoria sin default, y su
   ratificación es POLÍTICA.
8. **El «% de cumplimiento» de la tabla del Factor de Sufrimiento no está definido por el canon.** La
   tabla indexa por cumplimiento (100 / 75 / 50 / 25) y la fórmula produce una magnitud `v`. La
   equivalencia `cumplimiento = 1 − min(v, 1)` es **propuesta mía**, con el límite que el documento 07 §5.6
   ya declaró para el caso análogo del ISE.
9. **El mapeo de los diez parámetros a los siete pesos no está publicado por el canon**, y hay dos bloques
   compartidos: **«Agua/Alimentación» (0,15 para dos dimensiones)** y **«Otros» (0,05 para la dimensión
   más etológica)**. Propongo resolverlo con agregación por el peor caso medido y **no** repartiendo el
   peso, pero la decisión es del Parlamento.
10. **¿Se adopta la parameterización sustituta (la ley) como piso ejecutable?** Es la decisión doctrinal
    más importante de este documento (§5.6): hace el estándar medible hoy al precio de medir **el piso de
    la ley** en lugar del piso del canon. **No la tomo solo**: la propongo con sus tres reglas y la dejo
    marcada como propuesta no ratificada.
11. **No existe umbral de tamaño de grupo para aves.** El único umbral de grupo verificado es del porcino
    (< 6 → +10 %; ≥ 40 → −10 %) y **no se traslada**: haría falta una fuente para aves, y no la hay. La
    alternativa verificada (recurso por ave: nido, bebedero, percha) **no mide el aislamiento**, que es lo
    que la dimensión «socialización» quiere proteger.
12. **La frontera SDV-A / SDV-E en un animal de granja no está resuelta por ninguna fuente**
    (documento 18 §11.1 y su pregunta abierta 12): la diversidad de razas es a la vez dimensión ecológica
    y existencia de la población animal. Este documento **no la resuelve**: la declara.
13. **La ausencia de umbral de escala y de criterio de «persona natural» animal.** No existe fuente que
    diga cuándo un conjunto de animales es un sujeto (una población, una raza, un rebaño) y cuándo es un
    agregado de individuos. El problema de la unidad del documento [02](02_Unidad_y_sujeto_del_SDV-E.md)
    **también aplica al SDV-A** y ninguna fuente lo resuelve.
14. **El invariante del animal pasaría de dos a tres estados si se acepta §8.2**, y el documento
    [09](09_Comparativa_inter_reinos.md) §11.1 registra **dos**. Es un cambio propuesto, no un hecho: si la
    revisión de coherencia de la biblioteca no lo acepta, §8.2 debe retirarse y no el documento 09.
15. **El costo de intrusión de la propia medición** (§10.2) es una propuesta sin fuente y sin precedente
    en los otros reinos: **no sé cómo se mide un costo de intrusión** ni si es commensurable con las otras
    dimensiones. Se registra como idea con consecuencias, no como parámetro.
16. **El SDV-A no puede declararse `cumple` casi nunca, por diseño** (estado por defecto `indeterminado`).
    No sé si esa es la lectura políticamente sostenible del estándar o si producirá el efecto contrario al
    buscado —**que nadie lo use porque nunca certifica**—. Es una pregunta de adopción, no de doctrina, y
    no la puedo responder desde aquí.

---

## 14. Referencias

**Regla aplicada:** solo URLs con estado HTTP comprobado. Los estados que se declaran aquí **se
recomprobaron en esta sesión** (23 URL: 20 responden 200, 2 responden 403 y 1 responde 404). Los valores
numéricos provienen de la lectura de esas fuentes en la sesión de verificación de la rama
(`scratch/sdv_e/fuentes/30_sdva.md`), que abrió y leyó **18** de ellas; las que no se abrieron van
marcadas `[REPORTADO]` y **no sostienen ninguna cifra de este documento**.

### 14.1 Espacio vital, densidades y alojamiento

| Fuente | Aporte | URL (estado) |
|---|---|---|
| UE, Directiva 1999/74/CE — normas mínimas para la protección de las gallinas ponedoras | Jaula enriquecida **750 cm²/ave** (≥ 600 utilizables, altura ≥ 20 cm, ninguna jaula < 2 000 cm²) art. 6; jaula convencional **550 cm²** y su prohibición art. 5; sistemas alternativos **9 aves/m²** art. 4.1.4 | https://www.legislation.gov.uk/eudr/1999/74/article/4/2020-12-31?timeline=false&view=plain+extent (200) · https://www.legislation.gov.uk/eudr/1999/74/article/5/2020-12-31?timeline=false&view=plain+extent (200) · https://www.legislation.gov.uk/eudr/1999/74/article/6/2020-12-31?timeline=false&view=plain+extent (200) |
| UE, Reglamento (CE) 889/2008 — producción ecológica (aves y ganado) | Ecológico interior **6 aves/m²**; exterior **4 m²/ave condicionados a 170 kg N/ha/año**; vaca lechera **6 / 4,5 m²**; nido **7 aves/nido** o **120 cm²/ave**; percha ecológica **18 cm/ave** | https://www.legislation.gov.uk/eur/2008/889/annex/III (200) |
| UE, Reglamento (CE) 889/2008 anexo XIIIa — acuicultura ecológica | Carga: **15 / 20 / 25 / 10 kg/m³**; estanques de tierra **4 kg/m³**; aguas continentales **1 500 kg/ha/año** y **20 kg N/ha**; **≥ 50 %** de diques con vegetación; camarones **240 g/m²** y **22 postlarvas/m²**; cangrejo **100 / 30 / 10 ind/m²**; **ablación del pedúnculo ocular prohibida**; oxígeno **≥ 60 %** de saturación | https://www.legislation.gov.uk/eur/2008/889/annex/XIIIa (200) |
| UE, Directiva 2008/119/CE — protección de los terneros | Ternero en grupo **1,5 / 1,7 / 1,8 m²** art. 3.1(b); prohibición de corral individual tras **8 semanas**, paredes perforadas, dimensiones del corral art. 3.1(a) | https://www.legislation.gov.uk/eudr/2008/119/body/2008-12-18/data.xht (200) |
| UE, Directiva 2008/120/CE — protección de los cerdos | Superficie **0,55 / 0,65 / 1,0 m²** art. 3.1(a); cerda **2,25 m²** y cerda joven **1,64 m²**, ajuste **±10 %** con grupos **< 6 / ≥ 40** art. 3.1(b); **ataduras prohibidas** art. 3.3; grupo desde **4 semanas tras la cubrición** hasta **1 semana antes** del parto art. 3.4; material manipulable art. 3.5; fibra para saciedad art. 3.7; giro fácil art. 3.8 | https://www.legislation.gov.uk/eudr/2008/120/body/2008-12-18/data.xht (200) |

### 14.2 Alimentación y agua

| Fuente | Aporte | URL (estado) |
|---|---|---|
| UE, Reglamento (UE) 2018/848 — producción ecológica y etiquetado | Origen del pienso del propio predio o de la región (anexo II parte II pt. 1.4.1(a)); **alimentación forzada prohibida** (1.4.1(d)); pienso en conversión **≤ 25 %** (1.4.3.1); acceso permanente a pasto/forraje (1.4.1(e)); **sin promotores del crecimiento ni aminoácidos sintéticos** (1.4.1(f)); selección de razas para **evitar la mutilación** (1.3.2(d), 1.3.3); **tope de 170 kg N/ha/año** (parte I pt. 1.9.4) | https://www.legislation.gov.uk/eur/2018/848/annexes (200) |
| UE, Directiva 2007/43/CE — pollos de engorde | **Oscuridad ≥ 6 h** con **≥ 1 tramo ininterrumpido ≥ 4 h** (anexo I pt. 7); **≥ 20 lux** sobre **≥ 80 %** del área (pt. 6); yacija seca y friable permanente (pt. 3); retirada de pienso **máx. 12 h** (pt. 2); **intervenciones no terapéuticas prohibidas** con la excepción del corte de pico en aves **< 10 días** (pt. 12) | https://www.legislation.gov.uk/eudr/2007/43/annex/I (200) |
| FAO — *Gateway to poultry production and products*: bienestar animal | *«Other common welfare concerns are poor nutrition and lack of access to clean, cool water»*: el agua se regula como **acceso**, sin cifra de volumen; y las aves de corral tienen *«a sufficient degree of awareness or "sentience" to suffer pain if their health is poor, or deprivation if they are poorly housed»* | https://www.fao.org/poultry-production-products/production/animal-welfare/en (200) |

### 14.3 Transporte, sacrificio y crueldad

| Fuente | Aporte | URL (estado) |
|---|---|---|
| UE, Reglamento (CE) 1/2005 — transporte de animales | **«Viaje largo» = > 8 h** desde que se mueve el primer animal (art. 2(m)); condiciones mínimas: sin lesión ni sufrimiento indebido, superficie y altura suficientes, **agua, pienso y descanso** a intervalos (art. 3) | https://www.legislation.gov.uk/eur/2005/1/body (200) |
| UE, Reglamento (CE) 1099/2009 — sacrificio de animales | **Aturdimiento previo obligatorio** y pérdida de consciencia **mantenida hasta la muerte** (art. 4.1); **excepción de los ritos religiosos en matadero** (art. 4.4) | https://www.legislation.gov.uk/eur/2009/1099/article/4 (200) |
| WOAH/OIE — Código Sanitario para los Animales Acuáticos, cap. 7.3 (aturdimiento y sacrificio de peces) | Aturdimiento con **pérdida inmediata e irreversible de consciencia**; métodos de bienestar deficiente que **no deben usarse**: hielo en el agua, CO₂, baños de sal o amoníaco, asfixia por extracción del agua, desangrado sin aturdimiento; **criterios de verificación**: movimiento corporal y opercular, **VER**, **VOR**; ayuno «no más de lo necesario» | https://www.woah.org/fileadmin/Home/eng/Health_standards/aahc/2010/en_chapitre_welfare_stunning_killing.htm (200) |
| WOAH — bienestar animal (definición y cinco libertades) | Definición: *«the physical and mental state of an animal in relation to the conditions in which it lives and dies»*; cinco libertades: hambre y sed, miedo y angustia, estrés térmico o incomodidad física, dolor/lesión/enfermedad, **expresión de patrones normales de comportamiento** | https://www.woah.org/en/what-we-do/animal-health-and-welfare/animal-welfare/ (200) |

### 14.4 Factor de Consciencia: el ámbito de protección legal

| Fuente | Aporte | URL (estado) |
|---|---|---|
| UE, Directiva 2010/63/UE — protección de los animales utilizados para fines científicos | La Directiva se aplica a *«live cephalopods»* (art. 1.3(b)): **los cefalópodos están incluidos expresamente**; los insectos y moluscos no cefalópodos quedan fuera del ámbito (art. 1.3) | https://www.legislation.gov.uk/eudr/2010/63/article/1 (200) |
| Reino Unido, *Animal Welfare (Sentience) Act 2022* | Definición legal de animal (§5(1)): **cualquier vertebrado** distinto de *homo sapiens* + **cualquier molusco cefalópodo** + **cualquier crustáceo decápodo**; el ámbito puede extenderse por reglamento (§5(2)) sin que se haya hecho | https://www.legislation.gov.uk/ukpga/2022/22/body (200) |

### 14.5 Acoplamiento con el SDV-E (la gobernanza del territorio que sostiene al animal)

| Fuente | Aporte | URL (estado) |
|---|---|---|
| CBD, 2022 — Marco Kunming-Montreal: metas | **Meta 4**: mantener y restaurar la diversidad genética dentro y entre poblaciones de especies nativas, silvestres **y domesticadas**; **Meta 7**: reducir **≥ 50 %** el exceso de nutrientes y **≥ 50 %** el riesgo de pesticidas y químicos altamente peligrosos; **Meta 10**: gestión sostenible de agricultura, acuicultura, pesca y silvicultura; **Meta 2 y Meta 3**: **30 %** de restauración y **30 %** conservado para 2030 | https://www.cbd.int/gbf/targets (200) |

### 14.6 Fuentes reportadas que NO sostienen ninguna cifra de este documento

| Fuente | Estado | Por qué no sostiene nada |
|---|---|---|
| *Cambridge Declaration on Consciousness* (2012) — https://fcmconference.org/img/CambridgeDeclarationOnConsciousness.pdf | **200, PDF no abierto** | Responde 200, pero **no se abrió** en la sesión de la rama: queda `[REPORTADO]`. **No se usa para sostener el Factor de Consciencia** |
| FAO, *Review of animal welfare legislation in the beef, pork, and poultry industries* (2014) — https://www.fao.org/3/a-i4002e.pdf | **200, PDF no abierto** | `[REPORTADO]`. Es la vía más probable para cerrar los huecos de la dimensión 8 en porcino y vacuno, y **no se cita ninguna cifra suya** |
| *New York Declaration on Animal Consciousness* (2024) — https://sites.google.com/view/nydeclaration/home | **200 por comprobación, redirige a inicio de sesión de Google** | El contenido no es legible sin sesión: se reporta su existencia y **no se le atribuye ninguna afirmación** |

### 14.7 Fuentes reales que bloquean a los agentes automáticos (403) y fuentes descartadas (404)

**Regla:** estas direcciones son reales y un humano las abre; **ninguna sostiene una cifra de este
documento**.

| Fuente | Estado | Consecuencia |
|---|---|---|
| WOAH/OIE, Código Terrestre, **cap. 7.11** (bienestar de las gallinas ponedoras) — https://www.oie.int/index.php?id=169&L=0&htmfile=chapitre_aw_laying_hens.htm | **403** (bloquea a los agentes automáticos) | **El estándar internacional del arquetipo queda sin texto en esta rama.** Cualquier umbral que solo exista allí no entra |
| EFSA, opinión científica sobre bienestar de ponedoras (2023) — https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2023.7787 | **403** | Densidades recomendadas, longitud óptima de percha y calidad de yacija **no entran** |
| UE, Directiva 2008/120/CE, **anexo I** (mutilaciones del porcino: corte de cola, castración, limado de dientes) — https://www.legislation.gov.uk/eur/2008/120/annex/I | **404** (ruta muerta, recomprobada en esta sesión) | **La dimensión 8 queda sin verificar para el porcino**: no se cita ninguna cifra suya (§4.11) |
| WOAH, Código Terrestre en línea (ruta de acceso) | 200 **pero inútil**: devuelve la página índice, no el capítulo | Descartada como fuente del capítulo 7.11 |
| `iucnglobalecosystemtypology.org` · `eflows.net` | Dominios **muertos** ya declarados por el brief de la rama | No se han probado en esta sesión y **no se citan** |

### 14.8 Referencias internas al canon (por sección, sin anclas de línea)

- **Cap. 9 §9.1-§9.2** — Del antropocentrismo a la coherencia vital; el ADN como *token* no fungible
  (3 800 millones de años); el **Continuo de la Consciencia** con los niveles A/B/C/D; y la advertencia de
  que el FC **no** determina el derecho a existir, sino el peso en el cálculo del VHV.
  `docs/book/edicion_3_dinamica/capitulo_09_sdv_a_260126.md`
- **Cap. 9 §9.3** — Los cinco criterios de validación de parámetros del SDV-A: etología científica,
  medible cuantitativamente, verificable con independencia (certificación por entidades **sin conflicto de
  interés**), consenso científico-social y contextualizable.
- **Cap. 9 §9.4** — Las ocho dimensiones genéricas (Fase 2) y las cinco fases del proceso de creación.
- **Cap. 9 §9.5** — El **SDV-Gallinas**: diez parámetros con Mínimo y Óptimo en columnas separadas, la
  fórmula `Σ[(req − actual) × Peso × Duración]` y los siete pesos que suman 1,00.
- **Cap. 9 §9.6** — Los SDV-A en desarrollo (vacas, cerdos, peces): **listas cualitativas, sin un solo
  número** — no convertibles en tabla de umbrales sin fuente nueva.
- **Cap. 9 §9.7** — La Base de Datos Universal de SDV: el árbol `SDV-H / SDV-A / SDV-E / Procesos` y los
  cinco procesos continuos (redacción, revisión cada 3-5 años, validación científica con DOI,
  deliberación democrática, traducción a políticas).
- **Cap. 9 §9.8** — La integración con el VHV: `V = Σ(Seres × FC × FS × FA)` —**tres factores en el
  canon: el cuarto, `FR`, vive en el sistema y no en esta fórmula**—, la tabla del **Factor de
  Sufrimiento** (0,2 · 0,5 · 1,0 · 2,0 · ∞) y la **prohibición de mercado** como consecuencia máxima.
- **Cap. 9 §9.9** — La tabla comparativa SDV-H / SDV-A: base epistemológica, fuentes, dimensiones,
  medición, crueldad, libertad y escala.
- **Cap. 9.5 §9.5.11** — El precedente del SDV-S y la *«no interferencia invasiva»* del reino animal.
- **Cap. 10 §10.3** — **Principio Precautorio de Consciencia**: *«Donde hay duda de consciencia, se asume
  consciencia.»*
- **Cap. 10 §10.4** — El SDV Universal: ecosistemas, lugares y objetos; y el **Principio de
  Proporcionalidad** de §10.5.
- **Cap. 10 §10.6 · §10.7 · §10.8** — Dignidad encadenada; gobernanza operacionalmente finita; los cuatro
  criterios de Persona Sintética (contra los que se mide la ausencia de criterios equivalentes para el
  sujeto animal y ecológico).
- **Cap. 16.5 §16.5.14** — El Reino Natural como conviviente: TA soberano, PIU como traductor,
  crédito regenerativo `r_units`, partes `eco-`, Zona Libre, *«el suelo antes que el saldo»* y
  *«cuidado ≠ extracción estética»*.
- **Cap. 5 §5.5** — Los tres tiempos (TVI, TA, TPI), el **PIU** como único traductor TA↔TVI y el costo en
  TA del bosque. **Cap. 5** — **T14** (Principio de Precaución Intergeneracional) y T7 (Jerarquía
  Temporal).
- **Cap. 8 §8.11** — Dimensiones binarias sin peso (VIII y IX del SDV-H): el precedente de la Zona Libre.
- **Cap. 17** — INV2: *«Ninguna acción del contrato puede dejar a un participante bajo su SDV»*.
- **EVV-1.2 §4.3** — El componente R admite valores negativos (crédito regenerativo); **§4.2** — `NC` y
  `FS` en el componente V.
- **Axioma 0 — Directiva Mayor** (*«resolver nuestras necesidades de la mejor manera para todos todos»*:
  tres reinos, presentes y futuros) · **T9 — No-antropocentrismo** · **T13 — Transparencia de Cálculo** ·
  **T16 — Minimizar Daño**. `maxocontracts/core/axioms.py`

### 14.9 Referencias internas al repositorio (documentos de esta biblioteca y del proyecto)

- Documento [01 — Doctrina del SDV-E](01_Doctrina_SDV-E.md) · [02 — Unidad y sujeto](02_Unidad_y_sujeto_del_SDV-E.md) · [03 — No colonización del TA](03_No_colonizacion_del_TA.md) · [04 — Zona Libre](04_Zona_Libre_del_Reino_Natural.md) · [05 — Representación, guardián y mandato](05_Representacion_guardian_y_mandato.md) · [06 — Medición y verificación](06_Medicion_y_verificacion_T13.md)
- Documento [07 — Fórmula de violación y pesos](07_Formula_de_violacion_y_pesos.md): déficit normalizado, operadores, cobertura del piso.
- Documento [08 — INV2-E, el invariante](08_INV2-E_invariante.md): los tres estados, la doble vía de bloqueo y la regla de no compensación.
- Documento [09 — Comparativa inter-reinos](09_Comparativa_inter_reinos.md): la tabla maestra de 16 ejes y la genealogía SDV-A → SDV-E.
- Documento [18 — Agroecosistemas](18_Ecosistemas_Agroecosistemas.md): la doble jurisdicción y el puente de las razas ganaderas.
- Índice de Salud Ecosistémica (IN-01), con pesos y bandas: [metricas_detalle_kpis_oraculos_dinamicos.md](../../architecture/metricas_detalle_kpis_oraculos_dinamicos.md)
- Riesgos R4, R6 y R13 (del reino natural, **no** del animal): [blindaje_anti_gamificacion_equidad.md](../../architecture/blindaje_anti_gamificacion_equidad.md)
- Contradicciones internas citadas: `docs/theory/tercer_paper_ontometria_vital_huevo.md` §2.2.4 (`SDV_Espacio_Vital ≥ 0.75 m²/gallina` como umbral) · `docs/theory/matematicas_maxocracia_compiladas.md` §IV.B.1 (escala de FC alternativa)
- Motor — bloque genérico de validación de SDV: `maxocontracts/blocks/sdv_validator.py` · `maxocontracts/core/types.py` (`SDV`, `SDV_S`) · `maxocontracts/core/axioms.py` (INV2, INV2-S)
- Hueco matemático del Factor de Consciencia y del Factor de Sufrimiento: `app/vhv_calculator.py::calculate_v_component`
- V no admite negativos y el crédito vive en R: `app/micromax.py` · `tests/test_micromax.py`
- Nombre que **no** es este estándar: `app/sdv_analyzer.py::SDVAnalyzer` (analizador del **SDV humano**, puente INV2-EDU)

---

## Anexo — Autoevaluación contra el checklist del brief

| Punto del checklist | Estado |
|---|---|
| Plantilla de 14 secciones | ✅ las 14 |
| Mínimo Absoluto separado del Óptimo en cada dimensión | ✅ §4.4-§4.11 (ocho tablas, dos columnas) y §2 Regla 3 |
| Cada cifra con fuente + año, y URL en Referencias | ✅ §14, o marca literal `[SIN FUENTE VERIFICADA]` |
| URLs verificadas, cero inventadas | ✅ 23 comprobadas por HTTP en esta sesión; todas de la sesión de fuentes de la rama |
| Marcas `[VERIFICADO]` / `[REPORTADO]` / `[HIPÓTESIS]` | ✅ en todo el texto, con la cuarta marca (`[SIN FUENTE VERIFICADA]`) muy presente |
| Canon citado por sección, sin anclas de línea ni rutas locales absolutas | ✅ §14.8 |
| Preámbulo metodológico presente | ✅ §2 (ocho reglas) |
| Zona Libre explícita | ✅ §10, con el límite duro de §10.1 |
| LEY (no votable) frente a POLÍTICA (votable) | ✅ §2 Regla 3, §4.2, §4.12, §10 |
| §12 honesta, con 🔴 donde no hay código | ✅ quince filas 🔴 y dos notas de lectura |
| §13 dice lo que no sé | ✅ dieciséis preguntas abiertas, cinco de ellas contradicciones verificadas del canon |
| Frases prohibidas evitadas; axiomas citados sin definirlos de más | ✅ |
| Aporta algo que no está en el canon sin contradecirlo | ✅ véase la lista siguiente |

**Los ocho aportes de este documento, en una lista, para que se puedan discutir uno por uno:**

1. **La corrección de unidad de la dimensión «agua»** (y de «horas fuera» y «luz natural»): donde el canon
   mide litros, la fuente mide **puntos de acceso** (§4.6, §5.6). Una cifra con la unidad equivocada no se
   puede auditar.
2. **La separación de las dos funciones del Factor de Consciencia**: compuerta categórica
   (`INCLUIDO / EN DUDA / EXCLUIDO`) para el alcance de la protección, y peso numérico —votable— para el
   cálculo del VHV (§4.12). Es el hallazgo que disuelve la contradicción entre los dos documentos del canon.
3. **La compuerta `EN DUDA` como análogo exacto del estado `indeterminado`** del SDV-E: los dos estándares
   biológicos necesitan tres estados, no dos (§4.12, §8.2), y el Principio Precautorio de Consciencia
   (Cap. 10 §10.3) es el operador del estado intermedio.
4. **La cobertura del piso del SDV-A, medida y publicada**: **0,05 exacto · 0,45 parcial · 0,50 sin
   fuente** (§5.6), con el criterio de clasificación explícito. Es la cifra que debe doler, en el mismo
   sentido que el 0,925 del documento 07.
5. **La tabla de sustitución de parameterización, con sus tres reglas** (§5.6): mide hoy con el parámetro
   que la ley sí publica, **y no certifica cumplimiento del canon** mientras el parámetro del canon siga
   sin medir.
6. **El ejemplo aplicado con las dos parameterizaciones** (§5.7), que cuantifica la distancia entre el
   canon y el derecho vigente (**0,4719**, de los cuales **0,3000** son el peso de la crueldad) y demuestra
   que el mismo factor de sufrimiento puede esconder dos mundos.
7. **El acoplamiento numérico con el SDV-E y su regla de prelación en tres puntos** (§4.14): el piso del
   animal se recorta contra el techo del ecosistema (**170 kg N/ha/año**), ningún piso cede ante ningún
   óptimo, y **la variable de ajuste es la actividad humana**.
8. **La composición de invariantes de la doble jurisdicción** (§8.4) y **el límite duro de la Zona
   Libre**: una violación del piso es un hecho documentable y lo inefable no la absorbe (§10.1).

Y una cosa que este documento **no** aporta, para que no se le atribuya: **no cierra la rama del SDV-A.**
El árbol del Cap. 9 §9.7 pide un SDV por especie y aquí hay uno desarrollado —y con siete de sus diez
parámetros sin fuente externa—. Lo que este documento hace es dejar el molde, los pesos, la aritmética, las
marcas de evidencia y los huecos contados, **para que el siguiente SDV-A por especie se escriba sobre un
estándar y no sobre una página en blanco.**

