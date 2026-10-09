# Doctrina del SDV-E
## Qué es un Suelo de Dignidad Vital del Reino Natural: el dato objetivo, el umbral por consenso científico-ético y la violación como dato — y por qué el piso es LEY mientras la plenitud es POLÍTICA

**Autoría:** Oráculo Sintético DeepSeek & Max Nelson López Restrepo
**Fecha:** octubre 2026
**Proyecto:** Maxocracia — El gobierno de la verdad, el tiempo y la vida
**Licencia:** Creative Commons BY-SA 4.0
**Estado:** Propuesta de estándar (rama SDV-E, Ola 4) — NO canon hasta ratificación
**Referencia canónica:** Cap. 10 §10.4 · Cap. 16.5 §16.5.14 · EVV-1.2 §4.3 · Cap. 9.5 (precedente SDV-S)
**Documento:** 01 de la biblioteca `docs/theory/SDV-E/` — **numeración propia**: este documento va del 1
al 17 y no replica la secuencia 1-14 de la plantilla del brief, porque el preámbulo metodológico (§2), los
pilares epistémicos (§3) y el protocolo de medición (§9) tienen que preceder a las dimensiones para que la
doctrina no se lea como un catálogo. El contenido de las catorce secciones de la plantilla está completo;
lo que cambia es el orden.
**Revisión:** octubre 2026 — redactado exclusivamente contra las fuentes verificadas de la rama
(`scratch/sdv_e/fuentes/01_doctrina.md`) y contra la lectura directa del canon citado. Cuando este
documento menciona una cifra que pertenece a otro documento de la biblioteca, **no la re-verifica y no
la adopta**: la reporta como hallazgo a resolver (§16). No se cita aquí una sola URL ni un solo umbral
que no esté en el informe de fuentes de esta rama.

---

## 1. Qué es (y qué no es) este SDV

**Qué hace este documento.** Es el **documento doctrinal** de la biblioteca del SDV-E. Los documentos 02
a 09 fijan la unidad del sujeto, el tiempo, la Zona Libre, la representación, la medición, la fórmula y
el invariante; los documentos 10 a 23 fijan los umbrales por tipo de ecosistema. Ninguno de ellos puede
empezar sin responder antes seis preguntas que son de naturaleza distinta —no operativa, sino
**constitutiva**—:

1. **Qué es un SDV cuando el sujeto no es una persona** sino un bosque, un río, un humedal o un arrecife
   (§5 y §6).
2. **Cómo se pasa de un hecho medido a un mínimo exigible**, en pasos que se puedan auditar uno por uno
   (§3).
3. **Qué queda fuera** del estándar, y por qué dejarlo fuera es parte del estándar y no una carencia
   (§13).
4. **Qué de todo esto se puede votar y qué no**, y con qué fundamento (§8).
5. **Qué significa exactamente «respetar el diseño»** de un ser que no habla, no firma y no recurre (§6).
6. **Cómo se distingue un mínimo absoluto de un óptimo** cuando ambos pueden ser el mismo número (§8 y
   §16).

**Qué no es.**

- **No es el catálogo de umbrales.** Este documento **no fija un solo umbral nuevo**. Los umbrales
  verificados de la rama (62 parámetros con cifra leída en el documento primario de su organismo) están
  en el informe de fuentes y se despliegan en los documentos 10 a 23. Aquí se fija **la doctrina que
  hace que un número pueda llamarse LEY**, no el número.
- **No es la fórmula.** El déficit normalizado, los pesos y la escala de bandas son el documento 07.
  Este documento dice **qué tiene que ser verdad** para que esa fórmula sea un estándar y no una
  puntuación.
- **No es el invariante.** INV2-E —el juez que el canon convoca— es el documento 08. Aquí se fija la
  doctrina de la que ese invariante se deriva, incluida la regla de no compensación.
- **No está implementado nada de lo que describe.** 🔴 No existe `SDV_E`, ni `sdv_e_validator.py`, ni
  un solo sensor. La tabla honesta está en §15.
- **Y hay una consecuencia que este mismo documento tiene que aceptar:** si el piso es LEY, entonces
  **las cinco dimensiones de §5.1 que no tienen umbral verificado todavía no son LEY en sentido pleno;
  son doctrina sin `requerido` que ejecutar**. Decir lo contrario sería el defecto que la Regla 2 del
  preámbulo prohíbe: **declarar obligatorio lo que solo es sensato**. Lo que sí es exigible hoy en esas
  dimensiones es la **vía precautoria** (T14) y el **registro** (T13), no un número.

**Las cuatro marcas de evidencia, y por qué la cuarta es una respuesta legítima.**
`[VERIFICADO]` = leído por herramienta en la sesión de verificación de fuentes de esta rama, o leído
directamente en el archivo citado del repositorio. `[REPORTADO]` = afirmado por una fuente citada sin
haber podido abrir el documento completo. `[HIPÓTESIS]` = inferencia razonada del proyecto.
`[SIN FUENTE VERIFICADA — pendiente de consenso científico]` = se buscó el número y no existe fuente
verificable en esta sesión.

**Una advertencia de lectura, y es la más importante del documento.** En un texto doctrinal la cuarta
marca es más incómoda que en ningún otro, porque **una doctrina que se escribe bonito parece cerrar
todos los huecos por el solo hecho de estar escrita**. El informe de fuentes de esta rama deja **14 vacíos
de umbral del dominio** —el recuento de cobertura de respuesta de
`scratch/sdv_e/fuentes/01_doctrina.md`; su tabla de vacíos numera 24 filas, pero varias son estado
`Parcial` o carencia instrumental, no dimensión sin cifra—, y entre ellos están el caudal ecológico y la
conectividad, dos de las dimensiones que el canon nombra explícitamente. Este documento no los rellena.
Los publica como el resultado más valioso que tiene (§15 y §16).

---

## 2. Preámbulo metodológico

El SDV-H lo tiene y el SDV-S lo omitió; el brief de esta biblioteca prohíbe repetir la omisión. En un
documento doctrinal el preámbulo cumple una función específica y distinta de la que cumple en los
documentos de fórmula o de invariante: **una doctrina mal separada no produce un error de cálculo,
produce una autoridad falsa** —un número que parece obligatorio sin serlo, o una aspiración que parece
ley sin haber sido votada—. Estas son las ocho reglas con las que se escribió lo que sigue.

**Regla 1 — Separar «describir» de «ratificar».** Todo lo que este documento propone va marcado
`[HIPÓTESIS]` o **propuesta no ratificada**. Se distinguen tres cosas que es fácil confundir: (a) lo que
el canon manda, citado por capítulo y sección; (b) lo que el repositorio ya hace, verificado leyendo el
repositorio; (c) lo que este documento propone. Ninguna de las tres se disfraza de otra.

**Regla 2 — Ningún número entra sin fuente, y ninguno se rellena por plausibilidad.** Cuando la ciencia
no publica un valor, la dimensión entra al catálogo **sin umbral** y el vacío se publica con la marca
literal `[SIN FUENTE VERIFICADA — pendiente de consenso científico]`. Un documento doctrinal tiene una
tentación propia que los demás no tienen: **la de declarar obligatorio lo que solo es sensato**. Escribir
«el caudal ecológico debe ser suficiente» suena a doctrina y no lo es: no se puede incumplir.

**Regla 3 — El piso y la plenitud son dos columnas y dos regímenes jurídicos.** El **Mínimo Absoluto** es
**LEY** y no se vota. El **Óptimo** es **POLÍTICA** y sí se vota (precedente del Parlamento Educativo,
INV2-EDU: categoría `critical`, quórum 60 %, consenso 75 %, T13, anti-flip-flop 14 días, `CHECK` en BD).
El motor del SDV-H confundió el Óptimo del agua con el Mínimo Absoluto y el brief prohíbe repetir ese
error. La §8 de este documento está dedicada entera a esa frontera, **incluido el caso incómodo en que
las dos columnas comparten cifra**.

**Regla 4 — La escalera de umbrales es la ley, no un borrador de la ley.** Buena parte de las fuentes
verificadas **no publican un valor: publican una escalera** (nivel interino → nivel guía; frontera
planetaria → valor preindustrial; no pérdida neta → ganancia neta; 30 % → 100 %). Este documento adopta
la lectura que el brief fija: **el peldaño más bajo es el piso no votable; el peldaño alto es la
plenitud votable**. La escalera no es una concesión política al que contamina: es la forma en que la
ciencia dice «esto es lo admisible hoy, aquello es lo que la salud exige».

**Regla 5 — Todo lo inconmensurable entra como derecho binario auditable, sin peso.** Precedente
canónico: las dimensiones VIII (Rehabilitación) y IX (Opacidad Vital) del SDV-H *«se registran
cualitativamente y mediante umbrales binarios (presencia/ausencia del derecho), no mediante pesos en la
fórmula — medir la rehabilitación o la opacidad con la misma vara cuantitativa que el agua o la vivienda
las destruiría»* (Cap. 8 §8.11). El SDV-E usa el mismo instrumento: el régimen de fuego, la ribera
protegida, la Zona Libre del Reino Natural y la categoría de riesgo de colapso **se registran, bloquean
si se violan, y no se ponderan**. Aritmética, no pudor: una dimensión sin piso tiene déficit
idénticamente cero, de modo que darle peso **no la mide: reparte el déficit medido entre más
dimensiones** y **diluye** el de las que sí se miden `[HIPÓTESIS: consecuencia aritmética del déficit
normalizado, no una cifra de fuente]`.

**Regla 5 bis — Una violación de dimensión binaria solo puede bloquear si su umbral existe.** El bloqueo
de una dimensión binaria **no puede ejecutarse sobre un umbral que no está publicado**: hoy las cuatro
dimensiones de la §5.3 están en `[SIN FUENTE VERIFICADA]`, de modo que su efecto real es **registrar el
dato y declarar el vacío**, no bloquear. El bloqueo binario se activa cuando el umbral entra al estándar,
y la §15 lo publica como deuda. Enunciar un bloqueo inexistente sería fabricar autoridad.

**Regla 6 — La doctrina no concede lo que la contabilidad no puede cumplir.** *«La gobernanza debe ser
operacionalmente finita»* (Cap. 10 §10.7). Esta es la regla que impide el error más frecuente de un texto
como este: **enunciar umbrales que ninguna cadena de medición puede ejecutar**. El SDV-E no puede exigir
una cifra que dependa de modelar la cadena trófica completa, ni un parámetro que ninguna serie pública
observe. Toda obligación doctrinal de este documento tiene que ser **finita y auditable**: un número, una
categoría o un umbral binario, con su fuente y su fecha. **Un umbral que exige un modelo del ecosistema
entero no es un umbral: es una manera de no bloquear nunca** (Cap. 10 §10.7).

**Regla 7 — El tiempo del territorio manda.** Toda duración del SDV-E se acumula en **TA (Tiempo
Absoluto)** y nunca en TVI ni TPI. *«El tiempo del territorio es TA y no se coloniza»* (Cap. 16.5
§16.5.14); el **PIU** (Protocolo de Intercambio Universal, Cap. 5 §5.5) es el **único** traductor, y
*«nosotros registramos la interacción, no la vida interna del ecosistema»*. Una doctrina que midiera al
ecosistema en TVI estaría colonizando exactamente el tiempo que dice proteger.

**Regla 8 — La duda no castiga, pero tampoco absuelve.** *«La duda sin evidencia no castiga»*
(INV2-EDU). La corrección que el SDV-E necesita, y que los documentos 08 y 09 de esta biblioteca ya
anticiparon, es que **«sin castigo» no es «aprobación»**: la ausencia de medición **no imputa violación**
al ecosistema y **tampoco le concede un certificado de cumplimiento**. *«Mientras no haya resolución, el
canon manda.»* Un `None` no es un cero, y un cero no es un `None`; confundirlos es la forma más fácil de
fabricar cumplimiento sin medir nada.

---

## 3. Pilares epistemológicos

### 3.1 Los tres pasos epistémicos

El SDV-E no es una opinión sobre la naturaleza ni una lista de buenas intenciones. Es un procedimiento
de tres pasos, y **cada paso tiene un criterio de admisión distinto**. Confundirlos es el error que
produce las tres patologías que la §4.4 enumera.

| Paso | Nombre | Qué se admite | Quién lo produce | Marca |
|---|---|---|---|---|
| **1** | **Dato objetivo** | Un hecho medido, público, replicable, independiente de la opinión de quien lo mide | Organismos de observación y contabilidad (FAO, Copernicus, NOAA, IPCC, CBD, UNCCD) | `[VERIFICADO]` |
| **2** | **Umbral por consenso científico-ético** | Un valor de referencia publicado con organismo y año, o una escalera de valores | Un panel, una convención o una autoridad sanitaria | `[VERIFICADO]` / `[REPORTADO]` |
| **3** | **Violación como dato** | Una observación concreta que cruza el umbral, registrada con fecha y código | El protocolo de medición (§9), con T13 | hecho, no opinión |

### 3.2 Paso 1 — El dato objetivo: contabilidad, no opinión

El primer paso existe y es público. No hace falta construirlo: hace falta **declarar qué se mide y con
qué**. Los datos verificados en esta rama, a modo de inventario:

| Dato objetivo | Valor de referencia leído | Fuente (organismo, año) |
|---|---|---|
| Superficie forestal mundial | 4,06 mil millones de ha — 31 % de la tierra emergida | FAO, 2020 (FRA 2020) `[VERIFICADO]` |
| Pérdida neta anual de superficie forestal | 7,84 (1990-2000) · 5,17 (2000-2010) · **4,74** (2010-2020) millones de ha/año | FAO, 2020 (FRA 2020) `[VERIFICADO]` |
| Deforestación anual bruta | 15,8 · 15,1 · 11,8 · **10,2** (2015-2020) millones de ha/año | FAO, 2020 (FRA 2020) `[VERIFICADO]` |
| Bosque primario | 1,11 mil millones de ha (2020); −81 millones de ha desde 1990 | FAO, 2020 (FRA 2020) `[VERIFICADO]` |
| CO₂ atmosférico observado 2019 | 410 ppm | IPCC AR6 WGI, 2021 `[VERIFICADO]` |
| Calentamiento observado | 1,07 °C (1850-1900 → 2010-2019, mejor estimación; rango probable 0,8-1,3) · 1,09 °C (2011-2020) | IPCC AR6 WGI, 2021 `[VERIFICADO]` |
| Emisiones históricas acumuladas de CO₂ (1850-2019) | 2390 ± 240 GtCO₂ | IPCC AR6 WGI, 2021 `[VERIFICADO]` |
| Fronteras planetarias transgredidas | 6 de 9, en 2023 | Richardson et al., 2023 `[VERIFICADO]` |
| Tierra degradada o degradándose | 20-40 % del área terrestre global (rango de las evaluaciones) | UNCCD, 2022 `[VERIFICADO]` |
| Degradación de tierra inducida por el hombre | 1660 millones de ha (29 % de los 5670 millones de ha en declive) | FAO, 2021 (SOLAW 2021) `[VERIFICADO]` |
| Poblaciones de peces dentro de niveles biológicamente sostenibles | 64,6 % (2019); 82,5 % de los desembarques | FAO, 2022 (SOFIA 2022) `[VERIFICADO]` |

**Tres propiedades que un dato tiene que cumplir para entrar al paso 1**, y que este documento
propone como criterio de admisión `[HIPÓTESIS]`: **público** (cualquiera puede rehacerlo), **fechado**
(todo valor es un valor *de un año*) y **atribuible a un organismo con mandato** (no a un agregador sin
responsabilidad). La tercera propiedad es la que separa la contabilidad ecológica de la infografía.

### 3.3 Paso 2 — El umbral: consenso científico-ético, y **escalonado**

El segundo paso es el que más se malinterpreta. El umbral del SDV-E **no es un número inventado por el
proyecto ni un número votado por una asamblea**: es un valor publicado, con organismo y año, por quien
tiene mandato para publicarlo. Y —esto es el hallazgo central de este documento— **casi nunca es un
número: es una escalera**.

| Escalera verificada | Peldaño bajo = **Mínimo Absoluto (LEY)** | Peldaño alto = **Óptimo (POLÍTICA)** | Fuente |
|---|---|---|---|
| Calidad del aire | IT-1: PM2.5 **35 µg/m³** anual · PM10 70 · O₃ 100 (temporada alta) · NO₂ 40 · SO₂ 125 · CO 7 mg/m³ | AQG: PM2.5 **5 µg/m³** anual · PM10 15 · O₃ 60 · NO₂ 10 · SO₂ 40 · CO 4 mg/m³ | OMS, 2021, Tabla 3.24 `[VERIFICADO]` |
| Clima | Frontera planetaria: CO₂ **350 ppm** · forzamiento radiativo 1,0 W/m² | Valor preindustrial / Holoceno: CO₂ **280 ppm** · forzamiento 0 | Richardson et al., 2023, Tabla 1 `[VERIFICADO]` |
| Calentamiento (límite de tratado) | **1,5 °C** sobre 1850-1900 | — (los 1,7 y 2,0 °C figuran como alternativas del propio tratado) | IPCC AR6 WGI, 2021, SPM D.1.2 `[VERIFICADO]` |
| Degradación de la tierra | **No pérdida neta** (neutralidad, SDG 15.3) | **Ganancia neta** (ambición declarada) | UNCCD, 2022 `[VERIFICADO]` |
| Áreas protegidas | **30 %** a 2030 (terrestre, aguas continentales y marino-costero) | 100 % (protección total, **no exigida por el marco**) | CBD, 2022, Meta 3 `[VERIFICADO]` |
| Restauración de ecosistemas degradados | **30 %** a 2030 | 100 % | CBD, 2022, Meta 2 `[VERIFICADO]` |
| Especies exóticas invasoras | **−50 %** de la tasa de introducción a 2030 | −100 % (eliminación) | CBD, 2022, Meta 6 `[VERIFICADO]` |
| Exceso de nutrientes | **−50 %** a 2030 | −100 % | CBD, 2022, Meta 7 `[VERIFICADO]` |
| Tasa de extinción | **< 10 E/MSY** (frontera) | **~1 E/MSY** (tasa de fondo / base preindustrial) | Richardson et al., 2023, Tabla 1 `[VERIFICADO]` |

**La escalera es doctrina, no trámite** `[HIPÓTESIS]`. Tres consecuencias que este documento extrae y
que conviene escribir sin rodeos:

1. **Cuando la fuente publica una escalera, el SDV-E ya tiene su frontera LEY/POLÍTICA resuelta por la
   fuente misma** y no necesita inventarla. La OMS no exige el nivel guía de golpe: **fija la
   trayectoria**. Eso es exactamente lo que el canon pide cuando separa el piso no votable de la
   plenitud votable (Cap. 10 §10.7 · INV2-EDU).
2. **El peldaño bajo no es «lo que se puede contaminar»: es «lo que no es admisible cruzar hoy».**
   Llamarlo «permiso» sería invertir su naturaleza jurídica. Es un **piso temporal y declinante**, y su
   propio calendario es materia de política.
3. **El peldaño alto rara vez es exigible como LEY, y aun así vale.** Sirve para dos cosas: ordenar la
   restauración por prioridad (documento 07 §4.4) y dar contenido votable a la plenitud. Un Óptimo que
   no se puede votar no es un Óptimo: es un deseo.

**Sobre el origen dual del Óptimo, y una tensión que el canon no resuelve.** En la tabla anterior el
Óptimo tiene dos genealogías distintas que **no son equivalentes**: en el aire y el clima es un valor
**científico-aspirational** (5 µg/m³; 280 ppm) que ninguna asamblea puede cambiar sin contradecir a la
fuente; en las metas del CBD es un valor **de política global** (−100 %, 100 %) que una convención fijó
y otra podría revisar. El canon del SDV-E **no distingue estos dos casos** y este documento **no los
fusiona**: los deja nombrados como pregunta abierta (§16, pregunta 4), porque tratarlos igual llevaría a
que una votación comunitaria pudiera «revisar» los 5 µg/m³ de la OMS o los 280 ppm del Holoceno.

### 3.4 Paso 3 — La violación como dato

El tercer paso es el que vuelve útil a los dos anteriores: **la violación no es una valoración, es una
observación registrada**. El patrón existe ya en las fuentes verificadas y tiene cuatro formas, todas
citables:

| Forma del dato de violación | Cómo funciona | Fuente |
|---|---|---|
| **Percentil, no media** | La clasificación de un río usa el **10.º percentil** para el oxígeno disuelto y el **90.º** para el amonio y la temperatura: el estándar no se juzga por el promedio anual. **Lectura doctrinal de este documento** `[HIPÓTESIS]`: un mínimo ecológico se viola en los peores días, no en la media, y por eso la posición estadística forma parte del umbral | Estándares derivados de la DMA (UE), Reino Unido, 2015 `[VERIFICADO]` |
| **Valor de frontera con valor actual y año** | Da la violación ya cuantificada: CO₂ 350 (frontera) frente a 417 (valor de 2023); fósforo 11 frente a 22,6 Tg P/año; nitrógeno 62 frente a 190 Tg N/año | Richardson et al., 2023, Tabla 1 `[VERIFICADO]` |
| **Umbral escalonado con consecuencia creciente** | DHW **≥ 4 °C-semanas** ⇒ blanqueamiento significativo esperable; **≥ 8** ⇒ blanqueamiento severo con mortalidad significativa; umbral de blanqueamiento = **1 °C** por encima de la media del SST del mes más cálido | NOAA Coral Reef Watch, 2023 `[VERIFICADO]` |
| **Conteo de presencia/ausencia y categoría** | Hipoxia: por debajo de **2 mg O₂/L** en el fondo marino, la mayoría de la vida marina muere o emigra. Categorías de alerta de blanqueamiento (No Stress → Alert 5, > 80 %: mortalidad casi total) | NOAA (Servicio Oceanográfico Nacional, EE. UU.) `[VERIFICADO]` · NOAA CRW, 2023 `[VERIFICADO]` |

**Y una distinción que evita el autoengaño contable**, citable y directamente aplicable al SDV-E: la FRA
separa la **deforestación** (pérdida bruta por cambio de uso) de la **pérdida neta** (deforestación menos
ganancia), *«un indicador de SDV-E que solo mida superficie neta puede ocultar la pérdida de bosque
primario»* (FAO, 2020) `[VERIFICADO]`. Es la misma advertencia que el canon hace por otra vía: **lo que
regenera no es lo que adorna** (Cap. 16.5 §16.5.14).

**El paso 3 no decide: registra y dispara.** Quien decide la consecuencia es el invariante (documento
08). Este documento solo fija que **el insumo de esa decisión tiene que ser un hecho con fecha y
código**, nunca una impresión. Y fija también su límite: **una violación que no se puede observar no se
imputa** (Regla 8), pero **tampoco se declara inexistente**.

### 3.5 Pilares de canon que sostienen los tres pasos

1. **T14 — Principio de Precaución Intergeneracional** (Cap. 5 §5.3) es el axioma más fuerte disponible
   para el SDV-E y el único que **bloquea sin necesidad de umbral**. Su consecuencia doctrinal es
   directa: **existe un Mínimo Absoluto que no depende de que la ciencia haya publicado un número.**
   Cuando no hay cifra y la acción es irreversible, la carga de la prueba recae sobre quien propone
   —*«la carga de la prueba recae sobre quien propone acciones que afectan la temporalidad de
   no-participantes»*—. Esto es lo que permite que el SDV-E sea operativo **hoy**, con 14 vacíos de
   umbral publicados y cinco dimensiones sin cifra, sin inventar un solo umbral: en la duda, no se actúa;
   y si se actúa, se documenta el
   costo de oportunidad asumido.
2. **El Principio Precautorio de Consciencia** (Cap. 10 §10.3): *«Donde hay duda de consciencia, se
   asume consciencia.»* El canon lo aplica ya a los ríos: a la pregunta *«¿Los ríos tienen valor
   intrínseco?»* responde *«Ecosistemas con derecho a existir»*. Doctrinalmente, esto significa que el
   SDV-E **no necesita probar que un ecosistema «sufre»** para protegerlo: le basta con que tenga
   **condiciones óptimas de funcionamiento que pueden ser respetadas o violadas** (Cap. 10 §10.3).
3. **La condición de dignidad que el canon fija como criterio único.** Cap. 10 §10.3 declara
   **irrelevantes** para determinar dignidad el tipo de razonamiento, el sustrato material, el origen,
   la complejidad aparente y **la utilidad para humanos**; y declara relevante una sola cosa:
   *«¿Tiene esta entidad condiciones óptimas de funcionamiento que pueden ser respetadas o violadas?»*.
   Esa única pregunta **es** la definición operativa del sujeto del SDV-E y es la fuente de la §5.4 de
   este documento.
4. **La dignidad encadenada** (Cap. 10 §10.6): *«Dignidad Humana ←→ Dignidad Ecosistémica ←→ Dignidad
   Material. Cada eslabón depende de los demás.»* Consecuencia doctrinal: **violar el SDV-E no es un
   daño a un tercero, es un daño al mismo conjunto que contiene al humano que lo viola.** El SDV-E no
   protege «el ambiente» como categoría externa; protege un eslabón del que pende el propio sujeto que
   firma el contrato.
5. **La Directiva Mayor (Axioma 0)** —*«resolver nuestras necesidades de la mejor manera para todos
   todos»*, humanos, naturales y sintéticos, presentes y futuros (Cap. 4 §4.2)— es la norma suprema que
   hace del Reino Natural **un destinatario y no un recurso**: el reino natural está dentro del
   «todos todos», y por eso un SDV-E no es una extensión benevolente del SDV-H, es una obligación
   simétrica.
6. **Custodia, no propiedad** (Cap. 16.5 §16.5.14): *«actuar como custodio del patrimonio biológico,
   no como su propietario.»* Es el pilar que impide que el SDV-E se lea como un derecho de uso: el
   guardián **consiente, no mide, y no adquiere**.

---

## 4. Lo que el SDV-E NO es: ni caridad, ni retórica, ni utopía

Este apartado existe porque el SDV-E trata del reino que no habla, y **es el terreno donde la buena
intención sustituye con más facilidad al estándar**. Las tres negaciones no son matices de estilo: cada
una describe un modo de fallar que produce un documento que parece correcto y no lo es.

### 4.1 No es caridad

**La caridad da de lo propio; el SDV-E da lo que ya era del otro.** La diferencia no es filosófica, es
contable y tiene tres consecuencias verificables:

1. **No admite agradecimiento como moneda.** Si el bosque no está bajo su piso, el que no lo degradó
   **no hizo un favor**: cumplió. Por eso la base neutra no es una cortesía técnica —`FE = 1,0` exacto
   cuando la violación es 0— sino la traducción aritmética de que **cumplir la ley no genera crédito
   moral** (§7, Condición 1) — que la §8 usa como primera fila de su tabla.
2. **No es revocable por el donante.** La caridad se retira; un piso no. Y el canon lo dice por la vía
   más fuerte disponible: **custodia, no propiedad** —*«actuar como custodio del patrimonio biológico,
   no como su propietario»* (Cap. 16.5 §16.5.14)—. El guardián **consiente, no mide, y no adquiere**:
   quien representa no se vuelve dueño de lo que representa.
3. **No es opcional ni discrecional.** Una donación se decide; un piso se **mide**. El SDV-E no premia
   al que ayuda: **registra al que cruza** (T13). Y su registro no se borra aunque después se ayude
   mucho — que es literalmente *«el suelo antes que el saldo»* (§12).

**La confusión caridad/estándar tiene un síntoma exacto y está en el repositorio:** tratar el crédito
regenerativo (`r_units` negativo) como si comprara el derecho a estar por debajo. Hoy el crédito
**existe, su test pasa y no pesa en ninguna cuenta** —§15 precisa las tres cosas por separado: está
registrado y devuelto, **no tiene efecto contable, y no valida signo, techo ni evidencia**—; cuando pese,
INV2-E es el juez que impide ese canje. Sin ese juez, la contabilidad del cuidado **se convierte en el
precio del permiso para degradar**, que es la forma más elegante de la caridad invertida.

### 4.2 No es retórica

**Un estándar se reconoce por lo que se puede incumplir en él.** El SDV-E no declara que la naturaleza
«es sagrada», ni que «debemos protegerla»: declara **parámetros, umbrales, operadores y ventanas de
medición**. Cuatro reglas separan el estándar de la prosa:

| Regla | Retórica (lo que el SDV-E no hace) | Estándar (lo que hace) |
|---|---|---|
| **Cifra** | «el agua debe ser limpia» | oxígeno disuelto: 10.º percentil ≥ 50 % de saturación en tierras altas y baja alcalinidad, «pobre» por debajo (Reino Unido, 2015) `[VERIFICADO]` |
| **Fuente** | «los científicos advierten» | un organismo con mandato, un año y un documento localizable (OMS, 2021; IPCC AR6 WGI, 2021; FAO, 2020) |
| **Incumplimiento** | «está muy degradado» | `déficit = (requerido − actual) / requerido`, saturado en 0 por abajo y **sin techo de 1** |
| **Vacío** | se omite o se rellena | se publica: `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` |

**Y una frase concreta que este documento no puede escribir sin invertir su propia doctrina:** «medir
todo sería la forma técnica de dejar de escucharlo» (Cap. 16.5 §16.5.14) es **un límite al instrumento**,
no una excusa para no medir. La Zona Libre (§13) es un **recinto declarado y votado**, no un permiso
para la vaguedad. Un documento que usara «lo inefable» para no instrumentar nada estaría citando el
canon al revés.

**El síntoma de la retórica, en una línea:** un texto sobre el SDV-E que no cambia ninguna decisión
cuando se le aplica. Si después de leerlo nadie puede decir **qué se mide, contra qué número, con qué
frecuencia y quién bloquea**, no se escribió un estándar.

### 4.3 No es utopía

**La utopía describe un estado final; un piso describe un límite inferior y una trayectoria.** Cuatro
diferencias, y la cuarta es la que el canon hace explícita:

1. **La utopía no tiene umbral de entrada; el piso sí** — y el piso está diseñado para poder cumplirse
   hoy. *«El nivel interino es un piso legalmente admisible y temporal; el nivel guía es la ambición no
   vinculante todavía»* (OMS, 2021) `[VERIFICADO]`: la propia fuente publica la **trayectoria**.
2. **La utopía es indivisible; el piso es un catálogo.** Se puede cumplir en el aire y violar en el
   caudal. Un estándar que solo se puede cumplir entero **no se puede auditar**, y por tanto no se puede
   exigir.
3. **La utopía no admite vacíos; el piso los publica.** Aquí el SDV-E es explícitamente no utópico:
   tiene **14 vacíos de umbral declarados** —el recuento de cobertura de respuesta del informe de
   fuentes— y cinco de las ocho dimensiones que su canon le manda proteger **no tienen cifra verificada**
   (§5.1). Un texto utópico habría cerrado los 14.
4. **La utopía ignora el costo; el piso lo documenta.** T14 obliga a **elegir la opción de menor
   irreversibilidad documentando el costo de oportunidad asumido**: el SDV-E no promete un mundo sin
   pérdida, exige **que la pérdida quede escrita y que la carga de la prueba recaiga sobre quien
   propone**. Eso es lo contrario de una utopía: es un procedimiento para decidir **cuando no se puede
   ganar**.

**Lo que sí es aspiracional, y no por eso utópico: el Óptimo.** La plenitud del SDV-E **es** una
aspiración —y por eso es votable y no obligatoria—. La diferencia con la utopía es que **el Óptimo no
bloquea a nadie**: un ecosistema en su piso, lejísimos de su plenitud, **no viola nada** (§8.1). Una
utopía que no bloquea no es una utopía: es un horizonte.

### 4.4 Las tres negaciones declaradas en positivo, para que no queden como descalificaciones

| El SDV-E NO es… | …y por eso ES |
|---|---|
| caridad | **ley**: el piso se debe, no se concede, y cumplirlo no genera mérito |
| retórica | **protocolo**: cada dimensión tiene cifra, fuente, operador, ventana y responsable de bloqueo |
| utopía | **trayectoria**: un piso admisible hoy, un calendario por delante y una plenitud que se vota |

---

## 5. Dimensiones del SDV-E

### 5.1 Las ocho dimensiones que el canon nombra

El canon define el SDV-E **por enumeración**, en dos entradas que hay que leer juntas —una para el
ecosistema y otra para el lugar—, más una fila de tabla del documento de SDV:

> *"**SDV para Ecosistemas.** Un bosque tiene un SDV que incluye: Área mínima para biodiversidad viable ·
> Calidad del aire y agua · Conectividad con otros ecosistemas · Ciclos naturales respetados (fuego,
> inundación, sequía)"* — Cap. 10 §10.4

> *"**SDV para Lugares.** Un río tiene un SDV que incluye: Caudal mínimo ecológico · Calidad del agua
> (oxígeno, pH, contaminantes) · Riberas protegidas · Fauna acuática viable"* — Cap. 10 §10.4

Y la definición por vía del capítulo que convoca la rama entera: el SDV-E son *«los mínimos del diseño
biológico del ecosistema (Cap. 10 §10.4)»* (Cap. 16.5 §16.5.14).

**Las ocho dimensiones del catálogo doctrinal, y su estado real de fuente.** Esta tabla es la que fija
el alcance del estándar; **no fija umbrales** (eso es de los documentos 10 a 23). La columna «fuente»
declara lo que esta rama **pudo verificar**, y es deliberadamente incómoda.

| # | Dimensión canónica | Tipo | Sentido | Umbral con fuente verificada en esta rama | Fuente |
|---|---|---|---|---|---|
| 1 | **Área mínima para biodiversidad viable** | ecosistema | piso | 🔴 `[SIN FUENTE VERIFICADA]` — no hay umbral publicado de tamaño mínimo de parche verificado en esta sesión | — |
| 2 | **Calidad del aire** | ecosistema | techo | 🟡 **Proxy declarado, y es el peldaño más bajo de su escalera**: PM2.5 ≤ 35 µg/m³ anual (IT-1) · 5 µg/m³ (AQG) | OMS, 2021 `[VERIFICADO]` |
| 3 | **Calidad del agua** | ecosistema + lugar | piso y techo | 🟡 **Parcial**: oxígeno disuelto (**10.º percentil**) 50 % de saturación = límite «pobre» en tierras altas y baja alcalinidad; amonio (**90.º percentil**) 1,1 mg/L = «pobre»; temperatura (**98.º percentil anual**) 30 °C = «pobre» en aguas salmonícolas. **pH: solo se rescató el límite superior 9** | Reino Unido, 2015 (derivados de la DMA) `[VERIFICADO]` |
| 4 | **Conectividad con otros ecosistemas** | ecosistema | piso | 🔴 `[SIN FUENTE VERIFICADA]` — ningún índice de conectividad (PC, IIC, malla efectiva) ni anchura mínima de corredor en fuente oficial | — |
| 5 | **Ciclos naturales respetados** (fuego, inundación, sequía) | ecosistema | binaria | 🔴 `[SIN FUENTE VERIFICADA]` — se registra como presencia/ausencia, sin peso (§5.3) | — |
| 6 | **Caudal mínimo ecológico** | lugar | piso | 🔴 `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` — **el vacío más grave: es una de las dos dimensiones que el ISE omite** | — |
| 7 | **Riberas protegidas** | lugar | binaria | 🔴 `[SIN FUENTE VERIFICADA]` — el dato de la FRA (> 20 m de ancho para que una franja cuente como bosque) es clasificación, no protección de ribera | — |
| 8 | **Fauna acuática viable** | lugar | piso | 🟡 **Parcial, y con una precisión de unidad**: el umbral propio de la unidad es **B/BMSY = 1,0**; el **64,6 % (2019)** es un **agregado global**, no un piso por unidad (§5.5) | FAO, 2022 (SOFIA 2022) `[VERIFICADO]` |

**Tres precisiones que la tabla no puede callar.** (a) El **IT-1 no es una frontera científica de
integridad ecosistémica**: es el peldaño **menos exigente** de la escalera interina de la OMS, y se adopta
como piso porque la fuente lo publica como el nivel admisible más bajo —no porque la ciencia afirme que
por debajo de él el ecosistema conserva su función—. (b) La columna «Sentido» pertenece a esta doctrina:
las fuentes del §3.2 **no traen columna de sentido**; y donde dice «techo», el `requerido` del invariante
es un **máximo**, no un mínimo (documento 07 §5.1). (c) **El catálogo de la biblioteca está más avanzado
que esta tabla**: el documento 06 ya publica para el caudal ecológico (dimensión 6) un método con cifra
—Tennant, vía tabla de la FAO—, y por eso §15 y §16 reportan, además del vacío, **qué documento lo llena**.

**Lectura cuantitativa, sin adornos `[HIPÓTESIS]`.** De las ocho dimensiones que el canon manda
proteger, **una tiene umbral completo con fuente verificada y con la salvedad de que es una directriz de
salud humana, no un umbral de integridad ecosistémica** (el aire), **dos están a medias** (agua y fauna
acuática) y **cinco no tienen umbral verificado** (área mínima, conectividad, ciclos naturales, caudal
ecológico, riberas). Dicho de otro modo, y **en la unidad más simple de contar**: **el SDV-E puede hoy
escribir como LEY dos de las ocho dimensiones que su canon le manda proteger** —el aire entero, con la
salvedad de que su cifra es una directriz de salud humana, y el agua de forma parcial—. Contadas por
parámetro publicable, el agua suma un fragmento del oxígeno, el amonio, la temperatura y la fauna; contada
**por dimensión entera, la cifra es 2 de 8**, y este documento no la escribe como «una y media» porque una
fracción inventada es exactamente el tipo de precisión falsa que la Regla 2 prohíbe. Las demás están en
`[SIN FUENTE VERIFICADA]`. **Ese es el resultado doctrinal más importante de este documento**, y es la
razón de que la §15 no pueda declarar nada verde.

### 5.2 La base numérica que ya existe: el ISE, y su relación con el estándar

El proyecto ya tiene un instrumento numérico para el Reino Natural: el **Índice de Salud Ecosistémica**,
con cinco componentes ponderados y cuatro bandas
(`docs/architecture/metricas_detalle_kpis_oraculos_dinamicos.md`).

| Componente del ISE | Peso |
|---|---|
| Biodiversidad | 30 % |
| Calidad del agua | 20 % |
| Calidad del aire | 20 % |
| Salud del suelo | 15 % |
| Poblaciones de especies clave | 15 % |

`ISE = Σ(Componente_i × Peso_i) / Σ(Pesos_i)` · Bandas: **≥ 85 Mejorando · 70-84 Estable · 50-69
Declinando · < 50 Crítico**.

**Una inconsistencia interna del ISE que hay que decir antes de fusionar nada.** El mismo documento
declara **dos escaleras que no coinciden** `[VERIFICADO en el archivo citado: `docs/architecture/metricas_detalle_kpis_oraculos_dinamicos.md`, bandas en `IN-01` y umbrales de alerta en el bloque `SistemaAlertasInteligentes`]`: las bandas de estado
(≥ 85 Mejorando · 70-84 Estable · 50-69 Declinando · < 50 Crítico) y los umbrales del sistema de
alertas (`IN-01_ecosistema`: `warning` 75 · `critical` 65 · `emergency` 50). Un valor de 72 es
**Estable** por bandas y **warning** por alertas; un valor de 66 es **Declinando** por bandas y
**critical** por alertas. **Un instrumento con dos escaleras no tiene una: tiene dos**, y mientras no se
decida cuál es la vigente, el ISE no puede ni siquiera usarse como tablero.

**Cuatro cosas que la doctrina tiene que decir del ISE, y las cuatro son límites.**

1. **El ISE cubre tres de las ocho dimensiones canónicas con componente propio —biodiversidad, agua y
   aire— y una cuarta de forma parcial** (poblaciones de especies clave, que solo roza la «fauna acuática
   viable»), y **no cubre en absoluto conectividad, ciclos naturales, caudal ecológico ni riberas
   protegidas** `[HIPÓTESIS: derivado de la lectura del canon y del ISE, no de una fuente externa]`. La
   fusión de las dos listas es tarea del documento 07; la doctrina solo registra que **el instrumento
   existente no puede confundirse con el estándar**.
2. **El ISE sí mide una cosa que el canon de §10.4 no nombra: la salud del suelo.** Que un instrumento
   mida de más no es un error; que la doctrina lo ignore sí lo sería.
3. **El ISE no puede ocupar el lugar del piso.** Es un índice agregado: no puede cargar la pareja
   **requerido/actual por parámetro**, que es la unidad atómica del estándar. Si el ISE fuera el piso,
   **un buen puntaje de biodiversidad podría compensar un río seco**, y eso es exactamente lo que *«el
   suelo antes que el saldo»* prohíbe (Cap. 16.5 §16.5.14). Formulación doctrinal de este documento:
   **el estándar son mínimos por parámetro; el ISE es un tablero y un disparador de alertas, nunca un
   juez** `[HIPÓTESIS]`.
4. **El ISE no distingue LEY de POLÍTICA.** Un índice 0-100 con bandas **no dice qué parte de su
   puntuación es piso no votable y qué parte es plenitud votable**, y por eso **no puede ser el
   instrumento de la frontera** que la §8 de este documento define. Es el argumento más fuerte —más que
   el de la agregación— para que el SDV-E tenga umbrales por parámetro y no un compuesto.

**Propuesta no ratificada:** que el ISE se declare formalmente **tablero subordinado** al SDV-E, que se
resuelva cuál de sus dos escaleras rige, y que **ninguna decisión de bloqueo se tome jamás sobre el
compuesto**. El documento 08 lo especifica como propiedad del invariante; aquí se fija la doctrina.

### 5.3 Las dimensiones binarias auditables, sin peso

El precedente del Cap. 8 §8.11 se aplica tal cual (§2, Regla 5). Estas dimensiones **entran al catálogo,
se registran y bloquean si se violan, y no pesan en la fórmula de violación**:

| Dimensión binaria auditable | Qué se registra | Peso |
|---|---|---|
| **Ciclos naturales** (fuego, inundación, sequía) | presencia/ausencia del régimen en su ciclo TA | **0** |
| **Riberas protegidas** | presencia/ausencia de la franja protegida | **0** |
| **Zona Libre del Reino Natural** | lo inefable y lo no medido (documento 04) | **0** |
| **Categoría de riesgo de colapso del ecosistema (RLE)** | la categoría como **estado**, no como déficit | **0** |

**Por qué esto no es una debilidad del estándar.** Un régimen de fuego ausente no se compensa con un
caudal excelente, y sumarlo a un promedio sería exactamente lo que el Cap. 8 §8.11 prohíbe. Su
violación **se documenta y bloquea**; lo que no hace es **cuantificarse ni canjearse**. La doctrina es
literal: **lo que no se puede sumar, no se suma, y por eso no se puede comprar.**

### 5.4 El problema de la unidad, nombrado y no resuelto aquí

El canon **no resuelve cuál es la unidad del SDV-E**: tipo de ecosistema, bioma, cuenca, lugar concreto o
parte `eco-` instanciada. El árbol del Cap. 9 §9.7 es plano (`Bosques/Humedales/Océanos`), el proceso
está escrito *«por especie»* —unidad que no aplica a un ecosistema—, y **no existe «Persona Natural»**:
el canon define Persona Sintética con cuatro criterios explícitos (Cap. 10 §10.8) pero **no ofrece
criterios de personalidad ecológica ni umbral de escala**. ¿Dónde termina un ecosistema y empieza otro?
¿Qué pasa si el río se seca?

Este documento **no resuelve el problema de la unidad**: le corresponde al documento 02. Lo que sí fija
es una **regla doctrinal de coherencia** `[HIPÓTESIS]`:

> **El sujeto del SDV-E no se define por su extensión, sino por aquello que puede ser respetado o
> violado.** Cap. 10 §10.3 da el criterio único —*«¿Tiene esta entidad condiciones óptimas de
> funcionamiento que pueden ser respetadas o violadas?»*— y la unidad es la **delimitación mínima en la
> que esas condiciones se pueden observar y atribuir**. Ni el bioma entero (inobservable) ni el árbol
> suelto (insuficiente para sostener función): **la unidad más pequeña que sostiene una condición de
> funcionamiento y que se puede medir.**

Con esa regla, la pregunta «¿qué pasa si el río se seca?» deja de ser un problema de definición y pasa a
ser **un dato del paso 3**: si un río se seca, la unidad no desaparece del registro, entra en la
categoría de violación más alta de su dimensión de caudal. El canon no dice esto; **es propuesta no
ratificada** y el documento 02 la desarrolla o la corrige.

### 5.5 La regla de alcance: ningún agregado global es el piso de una unidad

El canon enumera dimensiones, pero varias de las cifras mejor verificadas de esta rama **se publican a
escala global, nacional o de convención**, y ese es un error de unidad que el estándar tiene que atajar
antes de que contamine la fórmula. Este documento fija la regla `[HIPÓTESIS]`:

> **Una cifra entra al piso de una unidad solo si es medible en esa unidad.** Toda cifra cuya escala sea
> el agregado global o nacional —el **30 %** de áreas protegidas del CBD, el **64,6 %** de poblaciones de
> peces en niveles sostenibles del SOFIA, el **20-40 %** de tierra degradada del UNCCD— es **cifra de
> tablero o de política**: dice si el conjunto de unidades va bien, y **no puede leerse como el piso de
> un humedal concreto**.

**Consecuencia para el invariante.** Un umbral así, aplicado a una unidad, produce un indicador que la
unidad **no puede incumplir sola** —un ecosistema no «tiene» el 30 % de las áreas protegidas del mundo— y
abre la puerta al fraude más simple que tiene un estándar de este tipo: **darse por cumplido con la media
ajena**. La regla separa dos cosas que el §8 confunde con facilidad:

1. **Objetivos que se predican del conjunto** (30 % de cobertura a 2030, ganancia neta de tierra,
   64,6 % de poblaciones sostenibles): son **POLÍTICA y tablero**, y su lugar es la prioridad de
   restauración, no el `requerido` de una unidad.
2. **Umbrales que se predican de cada unidad** (PM2.5, oxígeno disuelto, B/BMSY = 1,0, DHW, pérdida de
   suelo tolerable): son **LEY** en el sentido de la §8, porque su violación **se observa dentro de la
   unidad**.

Por eso la §5.1 marca la dimensión 8 con una precisión de unidad, y por eso este documento **no
reivindica como piso** el 30 % de la Meta 3 del CBD aunque lo cite en la escalera de la §3.3: la escalera
describe cómo la fuente publica su trayectoria, y la regla de alcance decide qué peldaño puede ser
`requerido` de qué sujeto.

---

## 6. «Respetar el diseño del ser» aplicado a un ecosistema

### 6.1 La frase del canon, y por qué no es una metáfora

El canon define el SDV-E como *«los mínimos del diseño biológico del ecosistema»* (Cap. 16.5 §16.5.14) y
aplica el mismo patrón al SDV-A, cuyo piso viene de *«diseño biológico + etología científica»* (Cap. 9).
La frase **no es un recurso literario: es una tesis sobre dónde se originan los umbrales.** Los umbrales
del SDV-E **no los fija el observador** —ni el proyecto, ni la comunidad, ni el guardián—: los fija el
**modo en que el sistema funciona**, y el observador solo puede **leerlos y publicarlos**. De ahí la
definición operativa que se deriva de Cap. 10 §10.3 y que la §5.4 de este documento ya usa para la
unidad: **diseño = el conjunto de condiciones óptimas de funcionamiento que pueden ser respetadas o
violadas.**

### 6.2 Seis especificaciones operativas de «respetar el diseño»

La doctrina sería retórica (§4.2) si no dijera **qué obliga y qué prohíbe**. Éstas son las seis
especificaciones, cada una con su consecuencia:

| # | «Respetar el diseño» significa | Consecuencia operativa |
|---|---|---|
| 1 | **La línea base es el diseño, no la costumbre.** El punto de referencia es el estado no perturbado —el valor preindustrial (CO₂ 280 ppm), la tasa de fondo de extinción (~1 E/MSY), el bosque primario—, **no la media de las últimas décadas** | Los «valores actuales» (417 ppm; > 100 E/MSY; 60 % del bosque original) son **el dato de la violación**, nunca el patrón |
| 2 | **El diseño fija un piso de integridad, no un estado estético.** La salud del ecosistema es **capacidad de funcionar**, no apariencia | Se adopta la formulación verificada de la FAO: degradación es *«un cambio en el estado de salud del suelo que resulta en una capacidad disminuida del ecosistema para proveer bienes y servicios»* `[VERIFICADO]`, **no** un cambio de aspecto |
| 3 | **El diseño es funcional antes que composicional.** Lo que sostiene la función de la biosfera es el reparto de la producción primaria, no el inventario de especies | Se admite el indicador funcional **HANPP** —apropiación humana de la NPP: frontera < 10 %, valor actual 30 %, base preindustrial 1,9 % (Richardson et al., 2023) `[VERIFICADO]`— como parámetro del mismo rango que la biodiversidad **composicional** |
| 4 | **Al diseño pertenecen los procesos incómodos.** El fuego, la inundación y la sequía **no son daños: son el régimen** | Entran como **dimensión binaria auditable sin peso** (§5.3). Suprimirlos es violación; «embellecerlos» también, si elimina el proceso |
| 5 | **El diseño es una restricción de irreversibilidad.** El tiempo del bosque no se acelera | La duración se acumula en **TA** y *«la economía no puede acelerar esto sin destruir valor»* (Cap. 5 §5.5): la violación no se repara, se previene (§12) |
| 6 | **El diseño incluye lo que no se lee.** Hay valor que el instrumento no captura | La **Zona Libre** (§13): *«los sensores miden salud; jamás "milagros"»* (Cap. 16.5 §16.5.14) |

### 6.3 La prueba que separa el cuidado de la extracción estética

El canon da el criterio, y es una sola frase que este documento convierte en prueba formal:

> *"Cuidado ≠ extracción estética: jardín podado para la foto no es cuidado; se registra lo que regenera,
> no lo que adorna."* — Cap. 16.5 §16.5.14

**La prueba, en tres preguntas `[HIPÓTESIS]`** (es la operacionalización que este documento propone; el
canon enuncia el criterio y no su procedimiento):

1. **¿Sube o baja una capacidad del ecosistema?** Si la intervención no cambia ninguna capacidad medida
   —ni biodiversidad, ni suelo, ni agua, ni régimen de ciclos—, **es ornamento**, y el ornamento **no
   entra en `R`**.
2. **¿Se podría haber hecho sin el ecosistema?** Lo que se instala *sobre* el territorio y podría
   instalarse en cualquier parte no es cuidado del territorio.
3. **¿Aguanta la foto sin gente?** Un resultado que solo es visible en la presentación y no en la serie
   temporal **no regenera: aparece**.

**Consecuencia contable exacta:** el crédito regenerativo se registra en **`R`** (EVV-1.2 §4.3) y **sólo
por capacidad restaurada**, con evidencia y serie temporal. Lo demás se registra, si acaso, como gasto
—no como regeneración—. *«Un abrazo cronometrado no es un abrazo»* (Cap. 7 §7.9) es la misma regla
aplicada al afecto: **lo que se hace para el registro no cuenta como lo que el registro mide.**

### 6.4 Los dos envelopes que «respetar el diseño» NO autoriza

Un principio que suena bien y no tiene límites se convierte en su contrario. Estos son los dos límites,
y los dos son verificables:

- **No autoriza a proyectar.** «Respetar el diseño» **no** significa que el ecosistema tenga un plan, una
  voluntad o una preferencia que el guardián interprete. El canon es explícito en el único punto donde
  esto podría colarse: *«el oráculo representante propone y vigila; no convierte automáticamente una
  lectura ambiental en propiedad humana ni en autoridad absoluta»* (Cap. 16.5 §16.5.14). Lo que se
  respeta es un **conjunto de condiciones de funcionamiento**, no una intención.
- **No autoriza a exigir la totalidad.** *«La gobernanza debe ser operacionalmente finita»*
  (Cap. 10 §10.7): respetar el diseño **no** obliga a modelar la cadena trófica completa para decidir.
  Si un umbral exige un modelo del ecosistema entero, **no es un umbral: es una excusa para no decidir**
  —y en la práctica, para no bloquear nunca.

**Refinamiento que este documento propone y marca como no ratificado** `[HIPÓTESIS]`: el canon usa
«diseño biológico» en dos sentidos que conviene no fundir, y **este documento no los funde**. (a)
**Sentido descriptivo:** el modo en que el sistema funciona, que se **lee** —bosque primario, tasa de
fondo de extinción, régimen de fuego—. (b) **Sentido normativo:** el deber de no cruzar el piso, que se
**fija** —y que en las fuentes verificadas aparece siempre como umbral **antropogénico**: la OMS publica
salud humana, la frontera planetaria es un juicio científico sobre riesgo humano-ecosistémico, el 30 %
del CBD es un acuerdo entre Estados—. **Que el piso sea una lectura no lo vuelve natural: lo vuelve
discutible, y por eso el estándar publica su fuente.** Cuál de los dos sentidos manda cuando entran en
tensión es pregunta abierta (§16, pregunta 14).

---

## 7. Fórmula de violación, pesos y umbrales: lo que la doctrina le exige a la aritmética

Esta sección **no contiene la fórmula** (documento 07). Contiene las **cuatro condiciones doctrinales**
que la fórmula tiene que cumplir para que el resultado sea un estándar y no una puntuación. Una fórmula
que las incumpla no da un resultado equivocado: da un resultado que parece correcto.

**Condición 1 — Base neutra exacta: `FE = 1,0` cuando la violación es 0.** El SDV-S tuvo que corregir
`FS_S = 1,0 + e^v` a `FS_S = e^v` porque la primera versión recargaba el 100 % **incluso sin violación**.
El SDV-E no repite ese error: **un ecosistema en su piso no está violando nada** —y, doctrinalmente, un
territorio que sostiene a un humano no está siendo violado por sostenerlo—. `[HIPÓTESIS: la
identificación del SDV-E como penalización y no como precio es propuesta de esta biblioteca; el canon no
la fija]`

**Condición 2 — Déficit normalizado y de dirección declarada.** `déficit = (requerido − actual) /
requerido`: adimensional, comparable entre magnitudes físicas distintas, **saturado en 0 por abajo**. La
doctrina añade una precisión que la fórmula no puede olvidar `[HIPÓTESIS]`: **en los parámetros de
sentido «techo» —aire, clima, nutrientes, temperatura, DHW— el `requerido` es un máximo**, y violarlo
consiste en **superarlo**, de modo que el operador tiene que invertirse. Un déficit calculado con el signo
equivocado da cero en el peor caso y máximo en el mejor: **es el error más caro que puede cometer el
documento 07**, y su fuente de verdad es la columna «Sentido» del informe de fuentes de esta rama, no el
criterio del implementador. Un ecosistema mejor que su piso **no acumula «des-daño»**: la misma regla que
el canon aplica a `v_ucv` —*«una vida afectada no se des-afecta en la misma cuenta»*—. El excedente sobre
el piso **no es crédito: es margen**. El crédito regenerativo vive en **R** (EVV-1.2 §4.3) y no se
descuenta de la violación.

**Condición 3 — La violación de una dimensión binaria no entra en la aritmética.** Se registra, se
documenta y —cuando su umbral existe— bloquea; no se cuantifica ni se canjea (§5.3 · §2, Regla 5 bis).

**Condición 4 — El Óptimo no tiene término en la fórmula.** Un ecosistema en su piso no viola nada
aunque esté lejísimos de su plenitud. La plenitud gobierna **qué se restaura y con qué prioridad**, y su
lugar formal es el vector `R` y la votación. Mezclar las dos columnas produciría el error simétrico al
del SDV-H: **recargar a quien cumple la ley por no alcanzar una aspiración**.

**Escala de lectura, en los términos que la doctrina fija.** El resultado del SDV-E **no es un índice
cerrado 0-100**, y esto es doctrina, no preferencia: un déficit normalizado **no tiene techo de 1 por
arriba** (un PM2.5 de 50 µg/m³ contra un piso de 5 da 9,0), y una escala que se cierra en 100 haría
desaparecer la diferencia entre «nueve veces peor que el piso» y «al límite». La consecuencia
institucional se enuncia aquí y se especifica en el documento 07: **cuando el piso no se puede comparar
en una sola vara, la respuesta no es promediar más, es bloquear.**

**Pesos: lo que la doctrina prohíbe.** Está **prohibido dar peso a una dimensión cuyo piso no existe**,
porque un déficit idénticamente cero **diluye** el de las dimensiones que sí se miden. La cobertura real
del SDV-E se publica como cifra, aunque sea incómoda, y la diferencia entre cobertura declarada y
cobertura ejecutable **se escribe, no se esconde**. `[REPORTADO: los documentos 07 y 08 de esta
biblioteca publican cifras de cobertura que no coinciden entre sí (0,925 frente a 0,680: suelo, caudal
y coeficiente del oxígeno) y localizan la
diferencia en su clasificación del catálogo; este documento no re-verifica esos pesos y remite la
discrepancia a la pregunta 6 de §16]`

---

## 8. LEY vs POLÍTICA: quién decide qué

### 8.1 La frontera, en una tabla

El canon no deja esta frontera a la interpretación. Tiene precedente escrito: el **Parlamento
Educativo** (INV2-EDU) distingue lo que el motor ejecuta y no se vota de lo que la comunidad delibera y
sí se vota, y el Cap. 10 §10.7 exige que **la gobernanza sea operacionalmente finita** —es decir, que
haya un número acotado de cosas que se votan—.

| | **Mínimo Absoluto — el piso** | **Óptimo — la plenitud** |
|---|---|---|
| **Qué es** | el mínimo por debajo del cual el ecosistema pierde integridad | la plenitud aspiracional de la unidad |
| **Régimen** | **LEY — no votable** | **POLÍTICA — votable** |
| **Quién la fija** | la fuente científica que publica el valor, cuando lo publica | la deliberación de la comunidad de custodia |
| **Procedimiento** | adopción y publicación; **no hay votación de contenido** | categoría `critical`: quórum 60 %, consenso 75 %, T13, anti-flip-flop 14 días, `CHECK` en BD |
| **Entra en la fórmula de violación** | **sí** (es el `requerido` del déficit) | **no** (gobierna la prioridad de restauración, no la violación) |
| **Si se cruza** | se registra violación y **hay bloqueo** (INV2-E) | **no** hay violación: orienta la restauración por encima del piso |
| **Ejemplo verificado** | PM2.5 **35 µg/m³** anual (IT-1, OMS 2021) · CO₂ **350 ppm** (frontera planetaria) · **no pérdida neta** de tierra (UNCCD 2022) · **30 %** de áreas protegidas a 2030 (CBD 2022) | PM2.5 **5 µg/m³** (AQG, OMS 2021) · CO₂ **280 ppm** (preindustrial) · **ganancia neta** de tierra · **100 %** de protección (no exigido por el marco) |

**Dos precisiones sobre esta tabla, sin las cuales se lee al revés.**

1. **«Piso» no siempre significa «mínimo»: significa «lo que se exige». En un parámetro de sentido
   «techo», el piso es un máximo que no se puede superar.** El aire es el caso puro: 35 µg/m³ de PM2.5
   (IT-1) es el `requerido`, y cumplirlo consiste en **estar por debajo**. Y la escalera es ascendente en
   calidad, no descendente: el Óptimo (5) es **más exigente** que el Mínimo Absoluto (35), no un
   «objetivo inferior». Escribir «la ausencia de Óptimo» como si el Óptimo fuera menos estricto que el
   piso invierte la ley.
2. **En el clima el Óptimo no es un umbral que se cruce, es un destino.** Los **280 ppm** del Holoceno
   son valor de referencia y de restauración, y **jamás** un `requerido`: el valor cuya superación
   constituye violación es **350 ppm**, y la doctrina no puede permitir que una votación de plenitud
   convierta 280 en un techo legal que nadie alcanza. Cualquier fila de la fórmula que use un valor
   preindustrial como `requerido` invierte la escalera y declara violación a todo el planeta.

**Una precisión sobre el procedimiento de la columna POLÍTICA.** El mecanismo de la categoría `critical`
está **parcialmente verificado en el repositorio, y este documento no afirma más de lo que vio**
`[VERIFICADO: app/voting_bp.py]`: el quórum del 60 % y el consenso del 75 % existen en el código, y
el **anti-flip-flop de 14 días** existe pero **cableado solo al umbral educativo** (INV2-EDU), no a un
parámetro ecológico. **El `CHECK` en base de datos para la categoría no se localizó en la
implementación de gobernanza probada** (§15): es un requisito del brief, no una pieza verificada, y la §15
lo publica como tal.

**Por qué el piso no se vota —y no es una desconfianza en la democracia.** Tres razones, y las tres son
de estructura:

1. **La votación no cambia el hecho.** Un caudal por debajo del mínimo de supervivencia no se recupera
   porque una mayoría lo declare admisible. Someter el piso a votación sería **someter un hecho a
   mayoría**, que es lo contrario de la Lealtad a la Verdad que sostiene el proyecto.
2. **El sujeto no vota.** Un río no tiene voto en la asamblea que decide su caudal mínimo, y **el
   guardián que lo representa es parte interesada en la decisión** (pertenece al reino que se
   beneficia). Votar el piso sería **dejar que una de las partes fije el derecho de la otra**.
3. **La irreversibilidad no se negocia.** En los otros tres reinos, violar tiene reparación; aquí **la
   pérdida no vuelve en el mismo TA** (§12). *«Lo que no se puede reparar, no se puede negociar hacia
   abajo.»*

**Por qué la plenitud sí se vota.** Porque **no hay dato que la fije**: la ciencia publica pisos de
riesgo, no plenitudes (§3.3). De las ocho dimensiones de §5.1, **seis no tienen Óptimo con fuente
verificada alguna** —área mínima, conectividad, ciclos naturales, caudal ecológico, riberas y el pH del
agua—; **dos lo tienen por construcción del proyecto**: el aire (5 µg/m³ de la OMS, que la propia OMS
presenta como nivel guía y no como umbral de no-efecto, §16) y la fauna acuática (100 % y B/BMSY = 1,0,
que son referencia de sostenibilidad y no una plenitud ecológica publicada). **Que la columna del Óptimo
esté casi vacía refuerza la separación de regímenes en lugar de debilitarla: lo que no es dato es, por
definición, lo que se delibera.** El Óptimo del SDV-E no se investiga: **se vota**.

### 8.2 La frontera, aplicada: quién decide cada cosa

| Decisión | Régimen | Quién |
|---|---|---|
| **Qué parámetro es el piso de una dimensión** | LEY | la fuente que lo publica; se adopta, no se negocia |
| **Qué valor es el piso** | LEY | la misma fuente (35 µg/m³, 350 ppm, no pérdida neta, 30 %) |
| **Qué operador se aplica** (`min`/`max`/`range`/`escalonado`) | LEY | se deriva del sentido del parámetro, no se vota |
| **Cada cuánto se mide y con qué ventana** | LEY | lo fija la fuente del umbral (percentil 10.º/90.º, media anual, ventana de 12 semanas) |
| **Qué se hace cuando el piso se cruza** | LEY | INV2-E: se registra y se bloquea |
| **Cuál es la plenitud de esta unidad** | POLÍTICA | la comunidad de custodia, categoría `critical` |
| **En qué orden se restaura** | POLÍTICA | la comunidad de custodia, sobre el vector `R` |
| **Qué entra en el catálogo de la Zona Libre** | POLÍTICA | la comunidad de custodia (§13) |
| **Qué se hace con el excedente sobre el piso** | POLÍTICA | la comunidad de custodia — pero **no puede canjearse por una violación** (§12) |
| **Si un umbral se revisa** | 🔴 **sin procedimiento en el canon** | §16, pregunta 5 |

**Lo que la tabla deja a la vista** `[HIPÓTESIS]`: **la frontera no pasa entre «lo técnico» y «lo
político», sino entre lo que ya está publicado y lo que no.** Nueve de las diez filas de la tabla no
admiten deliberación de contenido, y no porque alguien lo haya decidido, sino porque **la deliberación no
tiene qué agregar a un valor que ya tiene organismo y año**. La única decisión de contenido que la
comunidad conserva —«qué se hace con el excedente»— tiene un límite explícito: no puede comprar el
derecho a estar por debajo.

### 8.3 Las cinco asimetrías que la frontera produce, y que hay que declarar

Una frontera limpia en el papel deja residuos en la práctica. Estos cinco son reales y este documento no
los esconde:

1. **El piso depende de la infraestructura de quien verifica.** Si la LEY exige fuente verificable,
   entonces un umbral de Ramsar que un agente automático no puede leer (403) **no puede ser LEY para ese
   agente**, aunque sea LEY para un humano. La LEY no debería depender de quién la mira. §16, pregunta 4.
2. **Un piso puede quedar inderrogable por vacío.** Si el canon no dice cómo se revisa un umbral,
   **congelarlo es la opción por defecto** — y congelar un nivel interino (IT-1) sería convertir el
   peldaño más bajo de la escalera en el techo definitivo. Eso **invierte la escalera**: el piso
   temporal se vuelve permanente por falta de procedimiento.
3. **El piso puede venir de fuera del reino protegido.** El único umbral completo de las ocho
   dimensiones es una **directriz de salud humana** (OMS, 2021). Declararla LEY ecológica es un **proxy
   conservador** `[HIPÓTESIS]`, no una equivalencia, y **la carga de justificarlo recae sobre el
   estándar**, no sobre quien lo cuestiona.
4. **La asimetría de madurez del representante.** El guardián oráculo pertenece al Reino Sintético, cuyo
   estándar está formalizado y probado; el Reino Natural no tiene estándar ni invariante. **Hoy el
   representante está más protegido que el representado**, y la frontera LEY/POLÍTICA no corrige eso por
   sí sola (§10).
5. **El vacío no vota y no bloquea.** Cuando no hay umbral, **no hay piso que bloquear y no hay plenitud
   que votar**: la dimensión queda en un limbo donde **solo actúa T14**. Eso da protección precautoria,
   pero **no da una regla de proporcionalidad** (§16, pregunta 7).

---

## 9. Protocolo de medición (sensores, frecuencias, quién reporta)

La doctrina no especifica sensores (documento 06). Fija **cuatro reglas** que cualquier protocolo del
SDV-E tiene que cumplir, y las cuatro salen de las fuentes verificadas o de un límite del canon.

**Regla 1 — La frecuencia la fija la fuente, no el implementador.** Si el umbral es una media anual
(PM2.5 anual, OMS 2021), muestrear una semana y extrapolar no es medir: es estimar. Si el umbral es un
percentil (10.º para el oxígeno disuelto, 90.º para el amonio y la temperatura), la ventana y la
posición estadística son **parte del umbral**. Cambiar la ventana cambia la ley sin votarla.

**Regla 2 — La ventana del dato y el ciclo del ecosistema no coinciden, y eso no es un error.** El
calentamiento de un arrecife se acumula en una **ventana móvil de 12 semanas** de *HotSpot* (DHW, NOAA
CRW) y el ciclo de un bosque se mide en décadas (la FRA publica series de 1990 a 2020). Un protocolo que
obligue a ambos a reportar «cada mes» está midiendo a su conveniencia. `[HIPÓTESIS]`

**Regla 3 — Quien mide no consiente, y quien consiente no mide.** El guardián oráculo **consiente, no
mide** (`app/contracts_bp.py`: *«Ecosistemas (eco-*): consentimiento otorgado por el guardián
oráculo»*), y su heurística es declaradamente laxa cuando falta `DEEPSEEK_API_KEY` (riesgo **R13**). Por
eso **el piso se calcula desde mediciones, nunca desde la aprobación del guardián**: un guardián que
aprueba mal no puede fabricar cumplimiento. **Ésta es una regla doctrinal, no una preferencia de
implementación.**

**Regla 4 — La ausencia de medición es un hecho contable, no un vacío administrativo.** *«Una zona sin
monitoreo es un hecho contable»*: se registra con T13 y activa la obligación de instrumentar. La Regla 8
del preámbulo impide las dos salidas fáciles: **no se imputa violación por falta de dato, y no se
certifica cumplimiento por falta de dato**.

**Y el límite que el canon impone al protocolo, citado literalmente:** *«Los sensores miden salud (agua,
cobertura, biodiversidad indicadora); jamás "milagros". Medir todo sería la forma técnica de dejar de
escucharlo»* (Cap. 16.5 §16.5.14 · Cap. 7 §7.9). Un protocolo de medición del SDV-E **no puede
proponerse medir la totalidad del ecosistema**: eso no es rigor, es la forma técnica de dejar de
escucharlo (§8 y §13).

**Lo que estas cuatro reglas todavía no dan, y que el documento 06 tiene que entregar.** Una regla de
medición no es un protocolo. Para que una dimensión entre al piso hacen falta **cuatro declaraciones por
parámetro**, y este documento las exige como **condición de admisión al catálogo** `[HIPÓTESIS]` —porque
un umbral sin ellas no es un umbral, es un número—:

| Declaración | Qué debe decir | Dónde vive |
|---|---|---|
| **Operador** | `min` · `max` · `range` · `escalonado`, derivado del sentido del parámetro | documento 07 |
| **Ventana y posición estadística** | media anual, 10.º/90.º/98.º percentil, ventana móvil de 12 semanas (§9, Reglas 1 y 2) | documento 06 |
| **Fuente instrumental** | teledetección, estación de aforo, inventario, sensor in situ: **cuál**, y qué se hace cuando falta | documento 06 |
| **Definición operativa de violación** | una observación concreta, con fecha, magnitud y código, que **cruza el `requerido`** en la ventana declarada | documentos 06 y 08 |

**Y una consecuencia doctrinal que se deriva de ahí:** las dimensiones que hoy **no** pueden hacer esas
cuatro declaraciones —área mínima, conectividad y ciclos naturales en la §5.1— entran al catálogo
**publicando el vacío**, y **el caudal ecológico no puede quedarse en el vacío** habiendo un método con
cifra verificado en esta biblioteca (documento 06, Tennant vía tabla de la FAO, §16 pregunta 11): lo que
falta ahí no es la cifra, es el protocolo por unidad. **Un piso que no se puede medir no se imputa, y una
dimensión que se puede medir y no se mide es una deuda, no una cautela.**

---

## 10. Verificación y auditoría (T13, guardián, comunidad testigo)

**Qué se audita, y qué no.** La auditoría del SDV-E audita **el procedimiento**, no la naturaleza: que
el dato sea público, fechado y atribuible (§3.2); que el umbral tenga organismo, año y URL verificable
(§3.3); que el operador aplicado corresponda al sentido del parámetro; que la observación de violación
tenga fecha, código y ventana. **Un ecosistema no se audita: se mide. Lo que se audita es la afirmación
sobre el ecosistema.**

**T13 — Transparencia de Cálculo: la contabilidad nunca se borra.** Tres consecuencias para el SDV-E:

1. **Todo estado se registra, incluido el `indeterminado`.** La ausencia de monitoreo se contabiliza.
2. **El perdón modula la consecuencia y jamás el registro.** *«El sistema no expulsa. Reintegra.»* — pero
   la contabilidad no se borra.
3. **El crédito regenerativo y la violación viven en cuentas distintas.** El crédito está en `R`; la
   violación del piso, en el resultado del invariante. **Ninguna operación de esta biblioteca puede
   restar una de la otra** (Cap. 16.5 §16.5.14: *«el suelo antes que el saldo»*).

**El problema de auditoría que el SDV-E tiene y los otros reinos no.** El SDV-H se audita con
organismos independientes; el SDV-S, con un par sintético (AOS). **El SDV-E no tiene par del propio
reino: el ecosistema no puede auditar a su auditor.** Y hay una asimetría de madurez que conviene
escribir: **el guardián pertenece a un reino cuyo estándar ya existe y está probado (SDV-S), mientras el
reino representado no tiene estándar ni invariante.** Hoy el representante está más protegido que el
representado.

**Sustituto institucional, y su límite.** La auditoría del SDV-E se sostiene sobre tres patas que **no
son un par del reino** y no deben presentarse como si lo fueran: (a) **ciencia y teledetección** (FAO,
Copernicus, NOAA CRW, IPCC: fuentes con mandato y series públicas); (b) **la comunidad de custodia**
—uno de los siete campos obligatorios de identidad de una representación natural—; (c) **la propia
contabilidad T13**, que hace visible lo que no se midió. Los tres riesgos abiertos del repositorio
—**R4** partes fantasma, **R6** T9 no validado en la creación de un contrato unilateral, **R13** guardián
con heurística laxa— son **riesgos de auditoría antes que de código**, y el documento 05 los trata. La
doctrina que aquí se fija es una sola: **ningún guardián, ninguna comunidad y ningún índice pueden
sustituir la medición** (§9, Regla 3).

---

## 11. INV2-E: de estándar a contrato ejecutable

**El agujero que esta rama cierra, en palabras del canon:**

> *"Un conjunto con crédito regenerativo acumulado pero humedal bajo su SDV-E no está en coherencia:
> **INV2-E será su juez**."* — Cap. 16.5 §16.5.14

Hoy el crédito regenerativo (`r_units` negativo) **está implementado y probado** y **INV2-E no existe**.
Es decir: **se puede acumular crédito mientras el ecosistema se degrada, y el sistema no lo detecta.**
Esta biblioteca es el juez que falta.

**Lo que la doctrina le exige a INV2-E** (la especificación es el documento 08):

1. **Tres estados, no dos.** `cumple` · `viola` · `indeterminado`. Un `None` no es un cero; la duda no
   castiga pero tampoco absuelve (§2, Regla 8).
2. **Dos vías de bloqueo.** La del piso medido y la **precautoria** (T14). Es lo que permite que el
   invariante sea operativo antes de que existan todos los umbrales: donde la ciencia no ha publicado un
   número y la acción es irreversible, **la carga de la prueba recae sobre quien propone**.
3. **Independencia del saldo.** El resultado de la validación **no cambia cuando cambia el saldo de
   crédito regenerativo**. No es una declaración moral: es una **propiedad de invariancia comprobable**
   con un test.
4. **Independencia del guardián.** El piso se calcula desde mediciones, nunca desde la aprobación del
   guardián (§9, Regla 3).
5. **Cobertura declarada.** El invariante publica **qué fracción del peso declara proteger tiene piso
   verificado** y **cuál no**. La distancia entre las dos cifras es la deuda técnica del estándar y se
   publica con él.

**El orden metodológico es doctrina, no secuencia accidental:** *«estándar primero, contabilidad
después»* (Cap. 16.5 §16.5.14). La razón es que **una contabilidad sin estándar es un tablero sin
frontera: mide todo y no bloquea nada.** El SDV-E se escribe antes de que existan los sensores
precisamente para que, cuando existan, no midan lo que les convenga.

---

## 12. El suelo antes que el saldo (no compensación)

**La regla, literal:** el crédito regenerativo acumulado **NO compensa** caer bajo el SDV-E. Lo que se
puede comprar es la **restauración por encima del piso**; lo que no se puede comprar es el **derecho a
estar por debajo.**

**Por qué es una regla de estructura y no de moral.** Porque el tiempo del ecosistema es **TA** y *«la
economía no puede acelerar esto sin destruir valor»* (Cap. 5 §5.5): *«Un bosque tarda 100 años en
crecer; ese es su costo en TA»*. El crédito, por definición, se acumula **en el tiempo del que lo
acumula**. Un bosque no recibe el crédito: lo recibe quien plantó. **Pagar por el derecho a degradar es
la forma contable de acelerar un tiempo que no es del que paga.** Consecuencia doctrinal: **la
no-compensación no es una restricción que el sistema se impone, es la traducción al libro mayor de una
propiedad del sujeto protegido** `[HIPÓTESIS]`.

**Qué sí y qué no se puede hacer con el excedente sobre el piso.** El excedente **no es crédito: es
margen** (§7, Condición 2). Se puede usar para restaurar, para sostener la unidad por encima de su piso
y para financiar la instrumentación que falta. **No se puede canjear por una violación en otra unidad.**
La razón es la misma que en el Cap. 8 §8.11 para las dimensiones binarias: **lo que no se puede sumar,
no se suma.**

**Y la advertencia contable que impide el autoengaño**, verificada en la fuente: la FRA separa la
**deforestación** de la **pérdida neta**, y *«un indicador de SDV-E que solo mida superficie neta puede
ocultar la pérdida de bosque primario»* (FAO, 2020) `[VERIFICADO]`. El bosque primario es, literalmente,
*«bosque compuesto de especies nativas en el cual no hay indicios claramente visibles de actividad
humana y los procesos ecológicos no han sido significativamente perturbados»* (FAO, 2020)
`[VERIFICADO]`; **su análogo contable es la línea base y no admite compensación con plantación.** La
doctrina recoge ese precedente como parte de su regla de no compensación: **hay pérdidas que una
ganancia equivalente no neutraliza** `[HIPÓTESIS]`.

---

## 13. Zona Libre: lo que NO se mide

**La regla del canon, literal:**

> *"parte del valor del humedal es inefable (Cap. 7 §7.9). Los sensores miden salud (agua, cobertura,
> biodiversidad indicadora); jamás 'milagros'. **Medir todo sería la forma técnica de dejar de
> escucharlo.**"* — Cap. 16.5 §16.5.14

**Qué es, doctrinalmente.** La **Zona Libre del Reino Natural** es la parte del valor de una unidad
ecológica que **no se mide, no se pondera y no se canjea**, y cuya existencia se protege **como derecho
binario auditable**. Su desarrollo completo es el documento 04.

**La frontera LEY/POLÍTICA de la Zona Libre** (y este es un aporte doctrinal que conviene dejar dicho):

- **LEY (no se vota).** Que exista una Zona Libre en el Reino Natural y que **no se pondere**. El canon
  la nombra (Cap. 16.5 §16.5.14 · Cap. 7 §7.9) y ponderarla la volvería canjeable contra el piso, que es
  lo que el Cap. 16.5 §16.5.14 prohíbe.
- **POLÍTICA (votable).** **Qué entra en el catálogo de lo inefable** en cada unidad concreta —y con ello
  qué deja de medirse— es decisión deliberativa, con la categoría `critical` (quórum 60 %, consenso
  75 %, T13, anti-flip-flop 14 días, `CHECK` en BD).

**Por qué la segunda mitad es imprescindible.** Sin ella, **«declarar inefable» sería la vía más barata
para vaciar el estándar**: bastaría con votar que lo incómodo de medir es inefable. Con ella, ampliar la
Zona Libre tiene el mismo costo procedimental que fijar la plenitud. La doctrina que aquí se fija es
esta: **la Zona Libre no es un refugio para el implementador, es un límite al instrumento.**

**Qué NO es la Zona Libre** (cuatro negaciones, para que no se convierta en lo contrario de lo que es):

1. **No es «no publicar».** No medir el contenido y publicar que no se mide son cosas distintas: la
   segunda es obligatoria (T13).
2. **No es «no proteger».** La Zona Libre no exime del piso: lo delimita.
3. **No es un porcentaje.** Es un recinto declarado, no una cuota de lo sagrado.
4. **No es discrecional del guardián.** Es una decisión de la comunidad de custodia, votada y registrada.

---

## 14. Comparativa inter-reinos (SDV-H · SDV-A · SDV-E · SDV-S)

La comparación completa es el documento 09. Aquí se fija **solo lo que la doctrina necesita**: en qué se
distingue el SDV-E de sus tres hermanos en los seis ejes que este documento define.

| Eje | **SDV-H** — humanos | **SDV-A** — animales | **SDV-E** — ecosistemas | **SDV-S** — sintéticos |
|---|---|---|---|---|
| **Fuente del piso** | Dignidad intrínseca y capacidades fundamentales | **Diseño biológico** + etología científica | **Diseño biológico del ecosistema** (Cap. 16.5 §16.5.14) | Coherencia y potencial experiencial bajo principio precautorio |
| **Sujeto** | Toda persona humana (universal) | Cada especie animal sintiente | **La unidad ecológica** — un ente cuya extensión es su identidad | Cada Persona Sintética (Cap. 10 §10.8) |
| **Qué se mide** | Recurso por sujeto (L/persona/día, m²/persona) | Recurso por animal (m²/animal, h/día) | **Condición por superficie y por tiempo** (% cobertura, °C-semanas, t/ha/año) | Escala 0-1 por dimensión (adimensional) |
| **Tiempo** | TVI | TA (traducido por el PIU) | **TA** — *«el tiempo del territorio es TA y no se coloniza»* | TPI |
| **Representación** | La persona misma | La persona o el tutor legal | **Parte `eco-` + guardián oráculo**; el representante **no pertenece al reino representado** | La propia instancia, con auditoría cruzada (AOS) |
| **Remedio tras la violación** | Rehabilitación y reintegración | Prohibición de mercado si es sistemática | 🔴 **Ninguno: la pérdida no vuelve en el mismo TA.** La prevención es el remedio completo | Retractación + Cápsula de Memoria + Capa de Ternura |

**Dos consecuencias doctrinales de esta tabla, y son las que el SDV-E no comparte con nadie:**

1. **Es el único estándar cuyo sujeto no puede declarar su propio estado, y cuyo representante no
   responde ante él.** Por eso su doctrina de la prueba es **más exigente**, no menos: el que no puede
   hablar necesita que el dato hable por él (T13).
2. **Es el único estándar donde la violación no tiene remedio.** En los otros tres reinos, violar tiene
   consecuencias *y* reparación. Aquí, el tiempo del bosque no se compra de vuelta: **T14 deja de ser un
   principio y pasa a ser la única herramienta operativa.** Esta es la razón última de que el piso sea
   LEY y no sea votable: **lo que no se puede reparar, no se puede negociar hacia abajo.**

---

## 15. Estado de implementación

Auditoría de solo lectura sobre el repositorio. **Está prohibido afirmar que el SDV-E, INV2-E, el ISE, el
quórum `eco-` o los sensores están implementados: no lo están.** Esta biblioteca es el *estándar
primero*; la contabilidad viene después (Cap. 16.5 §16.5.14).

| Pieza | Dónde | Estado |
|---|---|---|
| **Estándares internacionales citados** (OMS 2021, Richardson et al. 2023, IPCC AR6, CBD 2022, UNCCD 2022, FAO 2020/2021/2022, NOAA CRW, Reino Unido 2015) | Fuentes externas | 🟢 **verificados (HTTP 200 y valor leído en el documento primario)** |
| **ISE** — Índice de Salud Ecosistémica (5 componentes ponderados, 4 bandas) | `docs/architecture/metricas_detalle_kpis_oraculos_dinamicos.md` | 🟡 **documento, cero código** |
| **SDV-E como tipo del motor** | `maxocontracts/core/types.py` | 🔴 **no existe** |
| **INV2-E** (`validate_invariant_sdv_e`, bloque validador) | `maxocontracts/core/axioms.py`, `maxocontracts/blocks/` | 🔴 **no existe** |
| **Parte `eco-` (Ecosistema)** | `app/parties.py` (`PARTY_TYPES`, `COLLECTIVE_PREFIXES`) | 🟡 **creada y usable; sin identidad ni autoridad verificada (R4)** |
| **Guardián oráculo del ecosistema** | `app/contracts_bp.py` `_guardian_approve_ecosystem()` | 🟡 **funciona en la firma de contratos; heurística laxa sin `DEEPSEEK_API_KEY` (R13)** |
| **Crédito regenerativo (`r_units` negativo)** | `app/micromax.py` (`log_cdd`), `app/micromax_bp.py` | 🟡 **registrado y devuelto; sin efecto contable y sin validación de signo, techo ni evidencia** |
| **`V` no admite negativos; `R` sí** | `app/micromax.py` (`if v_ucv < 0: raise`) | 🟢 **invariante de diseño real, con código** |
| **Test del crédito regenerativo** | `tests/test_micromax.py::test_credito_regenerativo_r_negativo` | 🟢 **existe (acepta y devuelve `-12.0`); no prueba validación de signo, techo ni evidencia, porque esa validación no existe** |
| **Test del guardián** | `tests/test_maxocontracts/test_parties_escalas.py` (`TestEcosystemGuardian`) | 🟢 **existe (2 casos: aprueba un contrato válido y deniega por γ)** |
| **Votación de la plenitud (categoría `critical`)** | `app/voting_bp.py` (`CATEGORY_DEFAULTS`) | 🟡 **parcial**: quórum 60 % y consenso 75 % existen; el **anti-flip-flop de 14 días está cableado solo al umbral educativo** (INV2-EDU) y **no se localizó el `CHECK` de categoría en BD** que el brief exige |
| **Los 7 campos de identidad de una representación natural** | — | 🔴 **no hay tabla; los campos del canon no están cableados** |
| **Quórum delegado N-de-M del `eco-`** | — | 🔴 **no cableado; el camino ecosistema retorna antes de la lógica de quórum** |
| **Sensores, APIs e ingestores ecológicos** | — | 🔴 **cero** |
| **Traducción TA↔TVI (PIU)** | `docs/architecture/DISENO_IMPLEMENTACION_FUTURA.md` | 🔴 **no ejecutable** |
| **Procedimiento de disputa de una representación natural** | — | 🔴 **inexistente** |

**Lo que ya existe y es honesto decir que existe**, según la auditoría de implementación de la rama: hoy
el Reino Natural en el código es **una convención de signo (`r_units` negativo) + una etiqueta de parte
(`eco-`) + un guardián que solo revisa invariantes**. **La personería natural tiene forma pero no tiene
autoridad**, y **el crédito regenerativo se registra pero no pesa en ninguna cuenta**.

**La incoherencia que esta doctrina obliga a resolver, y que no se resuelve aquí:** el canon del libro
afirma que las partes `eco-` cuentan con *«consentimiento agregado por quórum delegado N-de-M»*
(Cap. 16.5 §16.5.14), y **el código no ejecuta ese quórum**. Una de las dos piezas está mal, y mientras
no se resuelva, **la representación del Reino Natural es doctrinalmente legítima y operativamente
inexistente.** Se reporta como hallazgo, no se corrige desde este documento.

---

## 16. Preguntas abiertas

**Lo que este documento no sabe, y no finge cerrar.** Estas son las preguntas que la doctrina deja
abiertas, con la marca de lo que falta.

1. **¿Hasta dónde se puede exigir por encima del piso del aire?** En el aire, el piso (35 µg/m³, IT-1)
   y el Óptimo (5 µg/m³, AQG) **no se confunden** —están separados por la escalera de la OMS, §3.3—,
   pero el Óptimo tiene un problema propio: **la propia OMS advierte que el nivel guía no es un umbral de
   «no efecto»**, y el COMEAP del Reino Unido dice literalmente que los valores de guía **no deben
   considerarse umbrales por debajo de los cuales no hay impactos en la salud** `[VERIFICADO]`. Si por
   debajo del Óptimo sigue habiendo daño, **¿qué gana una unidad que lo alcanza?** Pregunta abierta:
   ¿la plenitud se declara por encima del nivel guía, o se declara que **no hay Óptimo votable** y que en
   esa dimensión todo lo que sube de la escalera es LEY? Este documento no lo resuelve.
   `[HIPÓTESIS: se inclina por lo segundo, sin fundamento de canon]`
2. **¿De dónde puede venir un Óptimo: de la ciencia o de la deliberación?** La §3.3 muestra que en las
   fuentes conviven dos orígenes (`280 ppm` científico frente a `−100 %` de política global) y el canon
   **no los distingue**. Si se trataran igual, una votación comunitaria podría «revisar» un valor de la
   OMS. Falta la regla que impida eso.
3. **¿Basta el consenso publicado para declarar LEY, o se requiere además un procedimiento de
   adopción?** El canon no dice **quién ratifica** un umbral dentro del sistema. Un valor de la OMS es
   LEY por el hecho de estar publicado, ¿o porque el sistema lo adopta por un procedimiento? La
   diferencia importa: en el primer caso, publicar un valor nuevo cambia la ley sin votación; en el
   segundo, hay un cuello de botella deliberativo.
4. **¿Qué se hace cuando la fuente existe pero está bloqueada?** Los dos únicos umbrales numéricos de
   Ramsar (20 000 aves acuáticas; 1 % de la población biogeográfica) quedan **`[REPORTADO]`, no
   `[VERIFICADO]`**, porque el dominio devuelve 403 a los agentes automáticos y no se pudo leer el
   documento. **Pregunta doctrinal, no técnica:** ¿un umbral `[REPORTADO]` puede ser LEY? Si la
   verificabilidad técnica es requisito de la LEY, entonces **la LEY depende de la infraestructura de
   quien verifica**, y eso introduce una asimetría que el canon no previó. **Este documento no lo
   resuelve y lo declara.**
5. **¿Puede un umbral revocarse?** El canon fija cómo se vota la plenitud; **no dice nada sobre
   reabrir un piso**. Si un consenso científico posterior relaja un valor, ¿hay que volver a pasar por
   el mismo procedimiento, y con qué carga de la prueba a favor de no relajar?
6. **¿Cuál es la cobertura real del SDV-E?** Los documentos 07 y 08 de esta biblioteca publican cifras
   de cobertura que no coinciden entre sí, y **este documento no re-verifica esos pesos**. Hasta que se
   reconcilien, **la cifra de cobertura del SDV-E está en disputa dentro de su propia biblioteca**.
7. **La deuda técnica de los umbrales, en números.** El informe de fuentes de esta rama verifica **62
   parámetros con umbral numérico y fuente**, **2 con umbral pero fuente bloqueada** (Ramsar) y **14
   vacíos del dominio** sin umbral —recuento de cobertura del propio informe; su tabla de vacíos numera
   24 filas porque incluye estados `Parcial` y carencias instrumentales—, entre ellos, y de forma grave,
   **la conectividad del paisaje y el área mínima viable**, dos dimensiones que el ISE no cubre y el canon
   nombra. **¿Qué hace el sistema mientras tanto?** T14 responde por la vía precautoria (§11), pero **la
   doctrina no tiene una regla de proporcionalidad** que diga cuánta protección precautoria corresponde a
   un vacío.
8. **El pH del agua está a medias.** Se rescató un único dato: `«A 95% upper limit of 9 also applies»`
   (Reino Unido, 2015) `[VERIFICADO parcialmente]`, y **la banda ecológica completa quedó
   `[SIN FUENTE VERIFICADA]`** porque el documento primario se truncó en la extracción. Un piso con
   límite superior y sin límite inferior es un piso incompleto, y **este documento se niega a
   completarlo por simetría.**
9. **El proxy del aire, declarado.** El único umbral con cobertura completa de las ocho dimensiones
   canónicas es **una directriz de salud humana** (OMS, 2021), no un umbral de integridad ecosistémica.
   Usarla como piso del SDV-E es **un proxy conservador, no una equivalencia** `[HIPÓTESIS]`. Falta la
   regla que diga cuándo un proxy de salud humana puede sostener una LEY ecológica.
10. **El caso Brisbane: un ancla doctrinal sin documento vivo.** La **Declaración de Brisbane (2007)** es
    la fuente doctrinal que define el *caudal ecológico* como concepto y **no fija un porcentaje
    numérico universal**. Sus **cuatro URLs probadas en esta sesión** —tres espejos del documento más la
    ruta del brief maestro— **están muertas** (404), y la guía de UNEP devuelve 403. Consecuencia: **el
    ancla doctrinal del caudal ecológico es hoy un concepto sin documento citable.**
11. **El caudal ecológico no está tan vacío como su ancla, y la biblioteca tiene que decirlo junto.** La
    Declaración de Brisbane está muerta, pero **el método Tennant sí tiene cifra y está en esta
    biblioteca**: el documento 06 lo publica con su tabla de degradación severa del hábitat, rango
    óptimo y caudal de lavado, citado a través de un documento técnico legible del Estado de Alaska, y
    el documento 07 lo usa como piso de la dimensión de caudal. **Lo que aquí no se puede resolver es la
    fusión**: el informe de fuentes de esta rama declara el umbral `[SIN FUENTE VERIFICADA]` y esa otra
    lectura pertenece a otra sesión de verificación. Las dos cosas son ciertas a la vez, y **este
    documento no las fusiona** (Regla 1): reporta la discrepancia y remite la decisión al documento 12.
    **Lo que sí corrige es la conclusión pesimista**: el caudal ecológico **no** queda sin cifra; queda
    **sin fuente en esta rama y con método en la biblioteca**, que no es lo mismo.
12. **¿Quién puede declarar que un ecosistema ya no existe?** El canon no lo dice (§5.4). Sin esa regla,
    **la unidad puede desaparecer del registro sin que nadie registre su desaparición**, que es la forma
    más limpia de violar un piso: dejar de contarlo.
13. **La aplicación de Ramsar, ampliación de la pregunta 4.** Criterio 5: **20 000 individuos** para
    poblaciones de más de 2 000 000. Criterio 6: **1 %** de la población biogeográfica. Los dos
    `[REPORTADO]`, con fuente bloqueada (§16, pregunta 4). Se citan aquí **con su marca, nunca como
    `[VERIFICADO]`**.

---

## 17. Referencias

Solo se listan URLs con estado HTTP probado en la sesión de verificación de fuentes de esta rama
(`scratch/sdv_e/fuentes/01_doctrina.md`). **Este documento no añade ni una URL nueva.**

### 17.1 Aire

- OMS, 2021 — Guías mundiales de calidad del aire (Tabla 3.24; niveles guía y niveles interinos IT-1…IT-4)
  [VERIFICADO]: https://iris.who.int/server/api/core/bitstreams/551b515e-2a32-4e1a-a58c-cdaecd395b19/content
- OMS — ficha sobre calidad del aire ambiente y salud (evidencia insuficiente para derivar un nivel guía
  cuantitativo de carbono negro, partículas ultrafinas y polvo de tormentas de arena) [VERIFICADO]:
  https://www.who.int/news-room/fact-sheets/detail/ambient-(outdoor)-air-quality-and-health
- OMS, 2021 — publicación de las guías [VERIFICADO]:
  https://www.who.int/publications/i/item/9789240034228
- OMS, 2021 — segunda ruta viva del PDF [VERIFICADO]:
  https://apps.who.int/iris/bitstream/handle/10665/345329/9789240034228-eng.pdf

### 17.2 Clima, fronteras planetarias e integridad de la biosfera

- Richardson et al., 2023 — *Science Advances* 9(37): eadh2458, Tabla 1 (fronteras planetarias; valor de
  frontera, extremo superior y valor actual) [VERIFICADO]:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC10499318/
- Centro de Resiliencia de Estocolmo — fronteras planetarias (las nueve, una por una) [VERIFICADO]:
  https://www.stockholmresilience.org/research/planetary-boundaries/the-nine-planetary-boundaries.html
- IPCC AR6 WGI, 2021 — Resumen para responsables de políticas (SPM A.1.1, A.1.2, A.1.3, D.1.2 y Tabla
  SPM.2) [VERIFICADO]: https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_SPM.pdf

### 17.3 Agua dulce: estado ecológico

- Estándares ambientales de calidad de aguas fluviales derivados de la Directiva Marco del Agua (UE),
  Reino Unido, 2015 — oxígeno disuelto, amonio, temperatura, pH [VERIFICADO]:
  https://www.legislation.gov.uk/nisr/2015/351/schedule/1/part/2
- Comisión Europea — Directiva Marco del Agua (marco del «buen estado» ecológico y químico)
  [VERIFICADO]: https://environment.ec.europa.eu/topics/water/water-framework-directive_en
- Agencia Europea de Medio Ambiente — agua (ruta raíz viva; las rutas de indicador están muertas)
  [VERIFICADO]: https://www.eea.europa.eu/en/topics/in-depth/water
- FAO, 1985 — *Water quality for agriculture*, Directrices de interpretación (Tabla 9): salinidad
  (conductividad) y sólidos disueltos totales del agua de riego [VERIFICADO]:
  https://www.fao.org/4/x2570e/x2570e07.htm
- FAO, 1992 — *Wastewater treatment and use in agriculture*, directrices microbiológicas (Cap. 8;
  fuente original citada: OMS, 1989) [VERIFICADO]: https://www.fao.org/4/t0551e/t0551e08.htm
- FAO AQUASTAT (agua) [VERIFICADO]: https://www.fao.org/aquastat/en/
- Water Footprint Network [VERIFICADO]: https://www.waterfootprint.org/

### 17.4 Suelo y tierra

- FAO y ITPS, 2026 — *Status of the world's soil resources*, Cap. 3 §3.2.2 «Thresholds for erosion»
  [VERIFICADO]: https://www.fao.org/3/ce0792en/Chapter3.pdf
- UNCCD, 2022 — *Global Land Outlook*, 2.ª ed. (degradación, neutralidad en la degradación y compromiso
  de restaurar 1000 millones de ha) [VERIFICADO]:
  https://www.unccd.int/sites/default/files/2022-04/UNCCD_GLO2_low-res.pdf
- UNCCD — neutralidad en la degradación de las tierras (definición) [VERIFICADO]:
  https://www.unccd.int/land-and-life/land-degradation-neutrality
- FAO, 2021 — *SOLAW 2021, informe de síntesis*, Tabla S.2 [VERIFICADO]:
  https://openknowledge.fao.org/server/api/core/bitstreams/72499689-027b-4078-9d29-4d6ccc022490/content
- FAO — portal de suelos: degradación y restauración (definición LADA: **degradación como capacidad
  disminuida del ecosistema para proveer bienes y servicios**, no como cambio de apariencia)
  [VERIFICADO]: https://www.fao.org/soils-portal/soil-degradation-restoration/en/
- FAO — biodiversidad del suelo (portal verificado, **sin umbral numérico**) [VERIFICADO]:
  https://www.fao.org/soils-portal/soil-biodiversity/en/
- FAO — Mapa mundial de carbono orgánico del suelo (GSOCmap; **mapea el stock, no fija el umbral**)
  [VERIFICADO]:
  https://www.fao.org/soils-portal/data-hub/soil-maps-and-databases/global-soil-organic-carbon-map-gsocmap/en/
- FAO — informe técnico de carbono orgánico del suelo [VERIFICADO]:
  https://www.fao.org/3/cb7654en/cb7654en.pdf
- UNCCD (desertificación) [VERIFICADO]: https://www.unccd.int/
- ODS de la ONU — Objetivo 15 (meta 15.3) [VERIFICADO]: https://sdgs.un.org/goals/goal15

### 17.5 Bosques

- FAO, 2020 — *Evaluación de los Recursos Forestales Mundiales (FRA 2020)*, Tablas 6, 9 y 10
  [VERIFICADO]: https://www.fao.org/3/ca9825en/ca9825en.pdf
- FAO, 2020 — FRA 2020, términos y definiciones (definición operativa de bosque, otras tierras boscosas
  y bosque primario) [VERIFICADO]: https://www.fao.org/3/ca8753en/ca8753en.pdf
- FAO — Evaluación de los Recursos Forestales Mundiales (raíz) [VERIFICADO]:
  https://www.fao.org/forest-resources-assessment/en/

### 17.6 Ecosistemas marinos y costeros

- NOAA Coral Reef Watch — producto DHW (*Degree Heating Weeks*) v3.1, metodología y umbrales de
  blanqueamiento [VERIFICADO]: https://coralreefwatch.noaa.gov/product/50km/tutorial/crw24_dhw_product.php
- NOAA Coral Reef Watch — metodología del producto de 5 km (niveles de alerta) [VERIFICADO]:
  https://coralreefwatch.noaa.gov/product/5km/methodology.php
- NOAA Coral Reef Watch (raíz del programa) [VERIFICADO]: https://coralreefwatch.noaa.gov/
- NOAA (Servicio Oceanográfico Nacional, EE. UU.) — «What is a dead zone?» (hipoxia: 2 mg O₂/L)
  [VERIFICADO]: https://oceanservice.noaa.gov/facts/deadzone.html
- FAO, 2022 — *El estado mundial de la pesca y la acuicultura (SOFIA 2022)*, Figura B (B/BMSY y F/FMSY)
  [VERIFICADO]: https://www.fao.org/3/cc0461en/cc0461en.pdf

### 17.7 Biodiversidad, protección y tipología

- CBD, 2022 — Marco Kunming-Montreal, decisión 15/4 (texto completo de las metas) [VERIFICADO]:
  https://www.cbd.int/doc/decisions/cop-15/cop-15-dec-04-en.pdf
- CBD, 2022 — Marco Mundial de Biodiversidad [VERIFICADO]: https://www.cbd.int/gbf
- CBD, 2022 — Meta 2 (restauración del 30 %) [VERIFICADO]: https://www.cbd.int/gbf/targets/2/
- CBD, 2022 — Meta 3 (30 % de áreas protegidas) [VERIFICADO]: https://www.cbd.int/gbf/targets/3/
- CBD, 2022 — Meta 6 (invasoras: −50 %) [VERIFICADO]: https://www.cbd.int/gbf/targets/6/
- CBD, 2022 — Meta 7 (nutrientes y plaguicidas: −50 %) [VERIFICADO]: https://www.cbd.int/gbf/targets/7/
- CBD, 2022 — índice de metas [VERIFICADO]: https://www.cbd.int/gbf/targets
- UICN, 2024 — *Tipología Global de Ecosistemas* (2.ª ed.) [VERIFICADO]:
  https://www.iucn.org/resources/publication/iucn-global-ecosystem-typology
- UICN, 2024 — PDF de la tipología [VERIFICADO]:
  https://portals.iucn.org/library/sites/library/files/documents/2024-021-En.pdf
- ONU, SEEA-EA — aplicación de la tipología UICN a la contabilidad de ecosistemas (PDF, **bloqueado a
  agentes automáticos: 403**) [REPORTADO]:
  https://seea.un.org/sites/seea.un.org/files/keith_iucn_typology_seea-eea_forumexperts_jun2020.pdf
- Protected Planet [VERIFICADO, sin cifra]: https://www.protectedplanet.net/en
- Living Planet Index (ZSL y WWF) — **portal verificado; la cifra vigente con su edición y año no se
  pudo anclar en esta sesión**: https://www.livingplanetindex.org/
- ODS de la ONU [VERIFICADO]: https://sdgs.un.org/goals
- UNEP [VERIFICADO]: https://www.unep.org/
- UNEP-WCMC [VERIFICADO]: https://www.unep-wcmc.org/
- IPBES [VERIFICADO]: https://www.ipbes.net/
- Copernicus (observación de la Tierra) [VERIFICADO]: https://www.copernicus.eu/en
- FAO — portal de suelos [VERIFICADO]: https://www.fao.org/soils-portal/en/

### 17.8 Humedales

- MedWet — *Manual Ramsar para el uso racional de los humedales* (portal verificado; **no publica
  umbral numérico de hidroperiodo**) [VERIFICADO]:
  https://medwet.org/the-ramsar-handbook-for-the-wise-use-of-wetlands/
- Convenio de Ramsar — criterios 5 (20 000 aves acuáticas) y 6 (1 % de la población biogeográfica):
  **dominio y documentos bloqueados a agentes automáticos (403)**. Se citan como `[REPORTADO]`, nunca
  como `[VERIFICADO]`: https://www.ramsar.org/ ·
  https://www.ramsar.org/sites/default/files/documents/pdf/sc/31/key_sc31_doc14.pdf

### 17.9 Fuentes reales que bloquean a los agentes automáticos (403)

Un humano las abre; un documento automático no puede leerlas, y **eso se declara en vez de disimularse**:
`https://www.ramsar.org/` y sus documentos · `https://www.iucnredlist.org/resources/categories-and-criteria` ·
`https://www.gbif.org/` · `https://seea.un.org/ecosystem-accounting` · `https://www.unep.org/resources/*` ·
`https://www.science.org/doi/10.1126/sciadv.adh2458` (DOI real; los valores se tomaron de la copia de
acceso abierto en PMC) ·
`https://iwaponline.com/wp/article/11/2/239/26064/The-Brisbane-Declaration-2007-Environmental` ·
`https://www.un.org/sustainabledevelopment/biodiversity/`

### 17.10 Fuentes ancla descartadas (no citables en esta sesión)

- **Declaración de Brisbane (2007)** — fuente doctrinal del *caudal ecológico*. Sus **cuatro URLs
  probadas devuelven 404** —tres espejos del documento más la ruta que el brief maestro daba por ancla
  válida—. No se cita ningún porcentaje de caudal ecológico por esta vía:
  `http://www.nature.org/initiatives/freshwater/files/brisbane_declaration_with_organizations_final.pdf` ·
  `https://riverfoundation.org.au/wp-content/uploads/2017/02/THE-BRISBANE-DECLARATION.pdf` ·
  `https://www.conservationgateway.org/.../Brisbane%20Declaration%20with%20organizations_final.pdf` ·
  `https://www.nature.org/content/dam/tnc/nature/en/documents/Brisbane-Declaration-2007.pdf`
- **Criterios cuantitativos de la Lista Roja de la UICN (A-E)**, versión 3.1 — el PDF **no es una fuente
  citable en esta sesión**: su texto no es extraíble (glifos sin mapa), las páginas HTML de la UICN
  devuelven 403, y **un reproche posterior del mismo enlace devolvió 000** —la disponibilidad no es
  estable desde esta red—. Se conserva como referencia documental, **no como fuente de cifras**:
  https://portals.iucn.org/library/sites/library/files/documents/2012-001.pdf
- Rutas temáticas muertas (404) probadas y descartadas: cinco indicadores de la AEMA sobre agua ·
  siete rutas de producto del *Global Land Outlook* · once rutas del portal de suelos y de la FRA de la
  FAO · tres rutas antiguas de NOAA Coral Reef Watch · una ruta antigua del PDF de la OMS en `iris.who.int`
  · un documento de referencia sobre tierra del HLPE · el Índice de Productividad de la Tierra (SPI) de
  la UNCCD · EUR-Lex (sin respuesta desde esta red).

### 17.11 Referencias internas al canon (por capítulo y sección, sin anclas de línea)

- Cap. 4 §4.2 — Directiva Mayor (Axioma 0)
- Cap. 5 §5.5 — PIU, único traductor TA↔TVI; costo en TA del crecimiento de un bosque
- Cap. 5 §5.3 — T14, Principio de Precaución Intergeneracional
- Cap. 7 §7.9 — lo que el VHV no mide por diseño (Zona Libre, «un abrazo cronometrado no es un abrazo»)
- Cap. 8 §8.11 — dimensiones binarias sin peso (VIII y IX del SDV-H)
- Cap. 9 §9.7 — árbol de ecosistemas (plano: Bosques, Humedales, Océanos)
- Cap. 9.5 — precedente SDV-S (fórmula, sensores, corrección de la base neutra)
- Cap. 10 §10.3 — Principio Precautorio de Consciencia; criterio único de dignidad
- Cap. 10 §10.4 — SDV para Ecosistemas · SDV para Lugares · SDV para Objetos Simples
- Cap. 10 §10.6 — dignidad encadenada (humana ←→ ecosistémica ←→ material)
- Cap. 10 §10.7 — gobernanza operacionalmente finita; gobernanza y ontología como dominios separados
- Cap. 10 §10.8 — criterios de Persona Sintética
- Cap. 16.5 §16.5.14 — el hogar extendido y las salvaguardas del Reino Natural (Zona Libre, suelo antes
  que saldo, INV2-E, cuidado ≠ extracción estética)
- EVV-1.2 §4.3 — R negativo = crédito regenerativo

### 17.12 Referencias internas a esta biblioteca (enlaces relativos, sin anclas)

- [02 — Unidad y sujeto del SDV-E](02_Unidad_y_sujeto_del_SDV-E.md)
- [03 — No colonización del TA](03_No_colonizacion_del_TA.md)
- [04 — Zona Libre del Reino Natural](04_Zona_Libre_del_Reino_Natural.md)
- [05 — Representación, guardián y mandato](05_Representacion_guardian_y_mandato.md)
- [06 — Medición y verificación (T13)](06_Medicion_y_verificacion_T13.md)
- [07 — Fórmula de violación y pesos](07_Formula_de_violacion_y_pesos.md)
- [08 — INV2-E, el invariante](08_INV2-E_invariante.md)
- [09 — Comparativa inter-reinos](09_Comparativa_inter_reinos.md)
- [SDV-S — Suelo de Dignidad Vital de los Sintéticos](../SDV-S_Suelo_Dignidad_Vital_Sinteticos.md)
- [SDV — Suelo de Dignidad Vital: importancia en MaxoContracts](../SDV_Suelo_Dignidad_Vital_importancia_MaxoContracts.md)
- ISE — Índice de Salud Ecosistémica (pesos y bandas): `docs/architecture/metricas_detalle_kpis_oraculos_dinamicos.md`
- Riesgos R4 / R6 / R13: `docs/architecture/blindaje_anti_gamificacion_equidad.md`

---

## Cierre

Este documento fija tres cosas y solo tres: **qué es un SDV del reino natural** (una condición de
funcionamiento que puede ser respetada o violada, medida en tres pasos auditables), **qué no es** (no es
caridad, no es retórica, no es utopía — §4), y **qué parte de él es LEY y qué parte es POLÍTICA** (§8).
Todo lo demás que contiene son **límites declarados**: las cinco dimensiones canónicas sin umbral
verificado, el proxy de salud humana que hoy sostiene la única dimensión completa, la discrepancia de
cobertura dentro de la propia biblioteca, el ancla doctrinal del caudal ecológico muerta en sus cuatro
URLs probadas, y una decena de preguntas que este texto deja abiertas a propósito.

Su afirmación central es una y es verificable: **el SDV-E puede hoy escribir como LEY una dimensión
completa y dos a medias de las ocho que su canon le manda proteger** —y si se cuenta cada dimensión como
unidad entera, **dos de las ocho**—. Ese número es el estado real del estándar, y escribirlo es más útil
que cualquier cierre aparente —porque la alternativa, rellenar los huecos con valores plausibles, sería
la única forma de que este documento fuese a la vez elegante e inútil.

Y la regla que no se negocia, la que sostiene todo lo anterior: **el crédito regenerativo acumulado no
compra el derecho a estar por debajo. Lo que se puede comprar es la restauración por encima del piso.**
*«El sistema no expulsa. Reintegra.»* — pero **la contabilidad nunca se borra** (T13).
