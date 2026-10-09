# La Zona Libre del Reino Natural
## Lo que no se mide: la dimensión binaria auditable sin peso que protege el interior de un ecosistema — y el registro que vuelve auditable su no-medición

**Autoría:** Oráculo Sintético DeepSeek & Max Nelson López Restrepo
**Fecha:** octubre 2026
**Proyecto:** Maxocracia — El gobierno de la verdad, el tiempo y la vida
**Licencia:** Creative Commons BY-SA 4.0
**Estado:** Propuesta de estándar (rama SDV-E, Ola 4) — NO canon hasta ratificación
**Referencia canónica:** Cap. 10 §10.4 · Cap. 16.5 §16.5.14 · EVV-1.2 §4.3 · Cap. 9.5 (precedente SDV-S)
**Documento:** 04 de la biblioteca `docs/theory/SDV-E/`
**Foco:** lo que **no** se mide. Dimensión binaria auditable **sin peso** (precedente canónico: dimensiones
VIII y IX del SDV-H, Cap. 8 §8.11). Qué queda en la Zona Libre de un ecosistema, quién la custodia y cómo
se documenta su **existencia** sin medir su **contenido**.

---

> *"Parte del valor del humedal es inefable (Cap. 7 §7.9). Los sensores miden salud (agua, cobertura,
> biodiversidad indicadora); jamás «milagros». **Medir todo sería la forma técnica de dejar de
> escucharlo.**"* — Cap. 16.5 §16.5.14

---

## 1. Qué es (y qué no es) la Zona Libre del Reino Natural

**Qué es.** Este documento define el **estado** en el que el interior de una unidad ecológica queda
**fuera de la contabilidad sin quedar fuera del Derecho**. No fija umbrales ecológicos nuevos: fija
**quién puede declarar ese estado, con qué pruebas, con qué límites, quién lo custodia y cómo se
audita una ausencia**. Es el documento que responde a tres preguntas que el canon deja abiertas:

1. **Qué queda** en la Zona Libre de un ecosistema (qué categorías de valor y de conocimiento se
   sustraen a la medición, y por qué).
2. **Quién la custodia** (y la respuesta corta, que se argumenta en §10: **no el sistema que la mide**).
3. **Cómo se documenta su existencia sin medir su contenido** (la pieza técnica que este documento
   aporta: el **inventario negativo** y el **registro de puertas**).

**Por qué existe este documento.** El canon nombra la Zona Libre del Reino Natural en una sola frase y
la deja sin procedimiento: *"Medir todo sería la forma técnica de dejar de escucharlo"*
(Cap. 16.5 §16.5.14). Una frase sin procedimiento es un buen principio y una mala garantía: cualquiera
puede invocarla y nadie puede verificarla. La comparación inter-reinos
([documento 09](./09_Comparativa_inter_reinos.md)) mostró que **los cuatro estándares reservan un
espacio que no se mide** y que el SDV-E debe elegir el modo del SDV-H (derecho binario sin peso) y no
el del SDV-S (peso 0,20, canjeable). Este documento convierte esa elección en **mecanismo**: puertas
verificables, estados sin grados y un registro que puede ser contradicho por un tercero.

**Qué no es.**

- **No es un permiso para no medir.** Es lo contrario: la Zona Libre es un estado **más caro** que la
  medición. Exige custodio con autoridad, frontera declarada, continuidad, protocolo de acceso,
  no-sustitución y precaución (§4.3). Una unidad medida no necesita nada de eso.
- **No es una magnitud ni un porcentaje.** No se declara «el 20 % de este humedal es Zona Libre». Se
  declara **un recinto con frontera** (§4.4). La razón es doctrinal y se desarrolla en §10.4: un
  porcentaje del territorio supone un propietario que reparte; un recinto supone un custodio que
  delimita.
- **No es una dimensión ponderable ni canjeable.** Pesa **0,00** y no entra en el numerador de ninguna
  fórmula (Cap. 8 §8.11, aplicado en §5).
- **No es la Zona Ciega.** Lo no medido **sin** autoridad de gobernanza no es Zona Libre: es una
  violación de este estándar (§4.2). Sin esta contra-definición, «declarar inefable» sería la vía más
  barata para vaciar el SDV-E.
- **No es canon.** Es una propuesta de estándar de la rama SDV-E, Ola 4, **no ratificada**.

**Marcas de evidencia usadas en todo el texto.** `[VERIFICADO]` = cifra o texto leído en la fuente
citada, con URL cuyo estado HTTP consta en la sesión de verificación de esta rama. `[REPORTADO]` = dato
afirmado por una fuente que se cita sin haber podido abrir el documento primario. `[HIPÓTESIS]` =
inferencia razonada del proyecto. `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` = se
buscó el umbral o el criterio y **no existe fuente verificable**. Las cuatro marcas son resultados
legítimos, y la cuarta es un resultado de primera clase: en un documento sobre lo que no se mide, la
ausencia de fuente no es un fracaso de la búsqueda, es **el objeto mismo del documento**.

**Trazabilidad.** La verificación de fuentes vive en el registro de trabajo
`scratch/sdv_e/fuentes/04_zona_libre.md` (documento de trabajo, **no** de la biblioteca). Las
afirmaciones sobre el código de la §12 se comprobaron por **lectura directa del repositorio en esta
sesión**, no por URL. Todo enlace citado aquí se re-comprueba con
`scripts/verificar_enlaces_sdv_e.py`.

**Nota de lectura dentro de la biblioteca.** Este documento es la **doctrina** de la Zona Libre; los
documentos por tipo de ecosistema la **aplican** unidad por unidad. El primer caso aplicado ya escrito
es el [documento 16](./16_Ecosistemas_Montanas_y_criosfera.md), que numera su Zona Libre como `D7`. Aquí
se la llama **dimensión `ZL`** para no comprometer una numeración que cambia en cada unidad (una unidad
con seis dimensiones cuantitativas tendrá `D7`; otra con ocho, `D9`). `ZL` es una etiqueta, no un
número.

---

## 2. Preámbulo metodológico

El SDV-H lo tiene y el SDV-S lo omitió; el brief de esta biblioteca prohíbe repetir la omisión. En un
documento cuyo objeto es **lo que no se mide**, el preámbulo no es un formalismo: es la única defensa
contra que «no se mide» se convierta en «no se sabe», y «no se sabe» en «no se responde».

**Regla 1 — La ausencia declarada es un dato; la ausencia silenciosa no lo es.** Una Zona Libre no se
define por lo que falta en una tabla, sino por lo que se **declara** que no se va a producir. Sin
declaración, la falta de dato es solo falta de dato, y el sistema no puede distinguir «no medimos
porque no debemos» de «no medimos porque no pudimos» —ni de «no medimos porque no convenía»—. Toda la
§4.5 existe para forzar esa distinción.

**Regla 2 — El piso es LEY; la plenitud es POLÍTICA.** El brief lo fija y el motor del SDV-H ya pagó el
error una vez (confundió el Óptimo del agua con el Mínimo Absoluto). Aquí la separación se aplica a un
objeto incómodo: **una dimensión binaria también tiene columna de Mínimo Absoluto y columna de
Óptimo**, y son cosas distintas (§5.1). El piso es la **existencia** del estado; la plenitud es la
**calidad de su sobre**.

**Regla 3 — Lo inefable no se pondera, y la razón no es estética.** Ponderar la Zona Libre la volvería
canjeable: un buen índice de biodiversidad **pagaría** la pérdida de lo que no se mide. Eso es
exactamente lo que *«el suelo antes que el saldo»* prohíbe (Cap. 16.5 §16.5.14) y el motivo por el que el
precedente canónico del Cap. 8 §8.11 advierte: *"medir la rehabilitación o la opacidad con la misma vara
cuantitativa que el agua o la vivienda las destruiría"*. La regla operativa es una sola: **peso 0,00, y
prohibición de canje**.

**Regla 4 — No se trasvasan umbrales entre reinos ni entre objetos jurídicos.** Un mínimo de
naturalidad de un *área silvestre* europea no es un mínimo de Zona Libre; un umbral de colapso de un
ecosistema no es un umbral de custodia. Cuando en §4.4 se citan cifras de extensión, se citan **como
referencias externas en desacuerdo**, no como piso importado. Promediarlas sería inventar consenso.

**Regla 5 — Cuatro cosas distintas se marcan distinto.** (a) no existe en el canon; (b) existe en el
canon y no en el código; (c) existe la fuente externa y no se pudo abrir; (d) se buscó y no hay fuente.
Las cuatro aparecen en este documento y ninguna se disfraza de otra.

**Regla 6 — La carga de la prueba recae sobre quien quiere dejar de medir.** El axioma T14 —Principio
de Precaución Intergeneracional (Cap. 5)— no es un adorno en este documento: es su procedimiento. Quien
propone **añadir** algo al catálogo de lo no medido carga con la prueba; quien propone **medir** no
carga con nada. Esa asimetría es deliberada y es la que impide que la Zona Libre se convierta en
refugio.

**Regla 7 — La imposibilidad declarada no es una carencia.** No existe —y no puede existir— un umbral
del «valor inefable». Eso no es un hueco de la búsqueda bibliográfica: es una **imposibilidad por
definición del dominio**, y se registra como tal (§10.6). Un documento que fingiera un umbral ahí
demostraría que no entendió su objeto.

**Regla 8 — Nada de este documento autoriza a intervenir.** *Sin dato no hay castigo; sin dato no hay
permiso.* La fórmula es del [documento 16](./16_Ecosistemas_Montanas_y_criosfera.md) §4.2, que la
deriva de INV2-EDU, y aquí se eleva a regla general de la Zona Libre: que el sistema no mida un
interior no lo autoriza a actuar sobre él, ni a autorizar a terceros.

---

## 3. Pilares epistemológicos

**Pilar 1 — El límite del conocimiento ecológico está escrito en derecho internacional, no en la
intuición del proyecto.** El Principio 6 del enfoque por ecosistemas, aprobado por las Partes del
Convenio sobre la Diversidad Biológica, reconoce *"considerable falta de conocimiento e incertidumbre
sobre los límites reales (umbrales de cambio)"* y añade algo más fuerte: *"aunque más investigación
puede reducir estas incertidumbres, dada la naturaleza dinámica y compleja de los ecosistemas **puede
que nunca tengamos entendimiento perfecto**"*. Su guía 6.2 ordena que, dada esa incertidumbre,
*"debe aplicarse el enfoque precautorio"*. [VERIFICADO] Es el ancla doctrinal más fuerte disponible
para este documento, y **no proviene del proyecto**: proviene del derecho ambiental internacional.

**Pilar 2 — Hay formas de información que se documentan sin someterse a la vara de la ciencia.** El
Principio 11 obliga a considerar *"todas las formas de información pertinente, incluyendo el
conocimiento científico y el conocimiento, las innovaciones y las prácticas indígenas y locales"*, y su
guía 11.3 ordena *"desarrollar mecanismos apropiados para documentar y hacer más ampliamente
disponible la información de todas las disciplinas pertinentes […] y de los sistemas de conocimiento
relevantes"*. [VERIFICADO] De aquí sale la forma del registro de la Zona Libre: **se documenta la
existencia de las fuentes; su contenido se consulta solo con autorización del custodio** (§10.5).

**Pilar 3 — El perímetro de respeto del propio instrumento.** El Cap. 7 §7.9 declara lo que el VHV no
mide *"no por incapacidad técnica sino por sabiduría ética"*, y remata: *"Esta lista no es un vacío del
sistema: es su perímetro de respeto."* La cita que gobierna este documento es su corolario: *"toda
métrica que se convierte en objetivo deja de ser una buena métrica"* (Cap. 7 §7.9). Una Zona Libre
medida para demostrar que existe deja de ser Zona Libre: se convierte en Zona Medida con un nombre
poético.

**Pilar 4 — Precaución donde no hay consentimiento posible.** El T14 (Cap. 5) establece que ante
incertidumbre sobre el impacto en agentes que no pueden consentir —ecosistemas, generaciones futuras—
el sistema debe elegir **la opción de menor irreversibilidad**, documentando el costo de oportunidad, y
que **la carga de la prueba recae sobre quien propone la acción**. Y el Principio Precautorio de
Consciencia (Cap. 10 §10.3) fija el marco: *"Donde hay duda de consciencia, se asume consciencia"* — con
el ejemplo que el propio canon da para los ríos: *"¿Los ríos tienen valor intrínseco?" → "Ecosistemas
con derecho a existir"*.

**Pilar 5 — La incertidumbre no excusa la inacción.** El reverso exacto del pilar 1, y hay que citarlo
en la misma página: la Decisión X/2 de la CBD establece que *"la incertidumbre científica no debe
usarse como excusa para la inacción"*. [VERIFICADO] Leído junto a la regla del brief *«sin dato no
castiga, pero la ley tampoco se negocia por ausencia de dato»*, produce la doctrina completa: **la
Zona Libre no suspende el deber de custodia; suspende la obligación de cuantificar el interior**.

**Pilar 6 — Custodia, no propiedad.** *"Actuar como custodio del patrimonio biológico, no como su
propietario."* El estándar internacional de la UICN reconoce cuatro tipos de gobernanza —gobierno,
actores privados, **pueblos indígenas y/o comunidades locales**, y gobernanza compartida— y exige
*"reconocimiento apropiado de las «áreas protegidas y conservadas indígenas»"*, advirtiendo que debe
respetarse *"la capacidad de gobernanza de sus autoridades legítimas"* y que **no deben suplantarse**
los sistemas de gobernanza existentes. [VERIFICADO] La puerta 6 de §4.3 es la traducción de esa
advertencia a una condición auditable.

**Pilar 7 — Proporcionalidad y gobernanza operacionalmente finita.** El Cap. 10 §10.5 exige un trato
*"lógico, proporcional y adecuado a la naturaleza de la entidad"*, y el Cap. 10 §10.7 fija el límite
que hace posible este documento: *"La gobernanza debe ser operacionalmente finita"*. Consecuencia
dura: **el SDV-E no puede exigir modelar la cadena trófica completa para decidir si una Zona Libre es
legítima**. Las siete puertas de §4.3 son finitas, binarias y verificables sin modelar el ecosistema.

**Pilar 8 — Estándar primero, contabilidad después.** *"El SDV-E —los mínimos del diseño biológico del
ecosistema (Cap. 10 §10.4)— es la ramificación pendiente que este capítulo convoca, siguiendo el
precedente del SDV-S (Cap. 9.5): estándar primero, contabilidad después"* (Cap. 16.5 §16.5.14). Este
documento es estándar: no implementa, especifica. La §12 dice sin adornos qué existe hoy en el
repositorio y qué no.

---

## 4. Dimensiones del SDV-E: la dimensión `ZL` (Zona Libre), binaria y sin peso

El SDV-E tiene dimensiones cuantitativas —las que el canon nombra en el Cap. 10 §10.4 y las que los
documentos 07 y 20-23 fijan— y, **al lado de ellas y sin mezclarse con ellas**, una dimensión binaria
sin peso: la Zona Libre. El precedente es explícito y canónico (§4.1). Lo que este documento añade es
la **mecánica**: qué estados existen (§4.2), con qué puertas se entra (§4.3), qué se delimita (§4.4),
qué se registra (§4.5) y con qué pruebas se mantiene o se pierde (§4.6).

### 4.1 Por qué sin peso, y por qué binaria

**El precedente, literal.** Las dimensiones **VIII (Derecho a la Rehabilitación)** y **IX (Derecho a la
Opacidad Vital)** del SDV-H *"se registran cualitativamente y mediante umbrales binarios
(presencia/ausencia del derecho), no mediante pesos en la fórmula §8.5 — medir la rehabilitación o la
opacidad con la misma vara cuantitativa que el agua o la vivienda las destruiría. Su violación se
documenta y es auditable (T13); su cuantificación queda delegada a la gobernanza de cada cohorte si
alguna decide ejercerla"* (Cap. 8 §8.11).

**La forma binaria no es ajena al derecho ambiental.** El criterio B de la Lista Roja de Ecosistemas de
la UICN —el estándar internacional de riesgo ecosistémico— se activa con **una sola** de tres señales
—declive en extensión espacial, declive en calidad ambiental o interrupción de interacciones bióticas—,
frente a los umbrales **cuantitativos y graduados** de los criterios de colapso (CR ≥ 50 % en 50 años;
EN ≥ 20 % en 50 años; VU ≥ 10 % en 100 años). Es decir: el estándar combina escalas y **presencia o
ausencia de señal**, según el criterio. [VERIFICADO: IUCN RLE, criterios v2.2 — el *Criteria Summary
Sheet v2.2* se leyó íntegro; el agrupamiento «≥ 1 de 3» sobre las tres señales es
`[HIPÓTESIS]` del informe de fuentes, que lo marca como *continuación inferida*, y este documento no lo
eleva a `[VERIFICADO]`] Que una dimensión ecosistémica admita evaluación binaria no es una concesión
poética del proyecto: es práctica del estándar internacional.

**La justificación operativa, en una frase.** El peso de una dimensión decide **cuánto pesa su déficit
en el precio**; la Zona Libre no puede tener precio sin dejar de ser lo que es. Por eso pesa 0,00 y su
violación se documenta (T13) sin cuantificarse.

### 4.2 Los cuatro estados de la dimensión `ZL` (la matriz que impide el refugio)

La pregunta que decide todo no es *«¿se mide o no se mide?»* —a esa pregunta se puede responder que no
por conveniencia—. Son **dos** preguntas, y su cruce produce cuatro estados, de los cuales **solo uno
es Zona Libre**:

| | **Con custodia** (autoridad de gobernanza legítima y con decisión vinculante) | **Sin custodia** |
|---|---|---|
| **Interior no cuantificado** | **ZONA LIBRE** — el estado que este documento define | **ZONA CIEGA** — 🔴 violación de la dimensión `ZL` |
| **Interior cuantificado** | **ZONA MEDIDA** — el SDV-E cuantitativo ordinario (docs. 07 y 20-23) | **ZONA HUÉRFANA** — 🔴 violación de la puerta 2 (custodia) |

**Cómo se lee esta matriz, y por qué cierra el problema abierto del documento 09.** El documento 09
§13 dejó abierta la pregunta 10: *«¿la Zona Libre binaria puede auditarse sin volverse refugio?»*. La
matriz responde **por construcción**, con cuatro consecuencias:

1. **No medir no basta para tener Zona Libre**: sin custodia se cae en ZONA CIEGA, que es violación.
2. **Medir no exime de custodia**: una unidad medida sin autoridad de gobernanza es ZONA HUÉRFANA, que
   también es violación. Es la puerta 2 y es independiente de la medición.
3. **Declarar inefable es más caro que medir**: la Zona Libre exige siete puertas; la Zona Medida, una
   sola cosa —medir—. La asimetría de costos apunta en la dirección correcta.
4. **La degradación no se puede esconder en la Zona Libre**: si aparece una señal de declive en el
   sobre, la presunción de integridad cae y la unidad debe medirse o repararse (§4.6). El refugio
   dura lo que tarda una señal en aparecer.

**Fundamento externo de la contra-definición.** El criterio es de la UICN, no del proyecto: las áreas
*"donde no hay autoridad de gobernanza ni régimen de gestión"* no cumplen los criterios de conservación
efectiva. [VERIFICADO: IUCN WCPA, OECMs, 2019] Sin esa frontera, la palabra «inefable» ampararía
exactamente la negligencia que el estándar existe para detectar.

**Distinción que hay que dejar escrita (colisión de vocabulario entre documentos).** Los estados de
esta matriz **no son** los estados de INV2-E del [documento 16](./16_Ecosistemas_Montanas_y_criosfera.md)
§8 (`SANO`, `EN_VIOLACION`, `CONSUMADO_IRREVERSIBLE`, `SUJETO_EXTINGUIDO`). Son **ejes ortogonales**: la
matriz de `ZL` describe *el régimen de medición del interior*; los estados de INV2-E describen *el
estado del sujeto frente a su piso*. Una unidad puede estar `CONSUMADO_IRREVERSIBLE` y conservar su
Zona Libre (el hielo se perdió y la cumbre no se mide), o estar `SANO` y en ZONA CIEGA (todo bien y
nadie responde por el territorio). **Fusionarlos sería un error de tipos y un error doctrinal.**

**Refinamiento explícito al documento 16 §4.2** (que declara la ausencia de Zona Libre declarada como
parámetro binario de su `D7`): esta doctrina distingue **por qué** falta una declaración. Si la unidad
se mide, la ausencia de Zona Libre es legítima —es ZONA MEDIDA—; si no se mide y no hay custodio, es
violación; si hay custodio y catálogo pendiente, es una Zona Libre **incompleta** y pertenece a la
POLÍTICA votable, no al reproche. Refina, no contradice: donde el documento 16 registra un booleano,
aquí se registra un estado con causa.

### 4.3 Las siete puertas (lo que se verifica sin medir el contenido)

Una Zona Libre no se concede: **se abre pasando siete puertas**, todas binarias, todas verificables por
un tercero, ninguna de ellas referida al contenido del interior. Están construidas sobre los cuatro
criterios del estándar de «otras medidas efectivas de conservación basadas en áreas» de la UICN, que
son **puertas lógicas y no escalas** —área definida; gobernanza y gestión sostenidas; resultado de
conservación; funciones y servicios asociados— [VERIFICADO: IUCN WCPA, OECMs, 2019]. La forma del
registro es la del portero: **se registra el portero, no la cosecha.**

| # | Puerta | Pregunta que responde | Verificable por | Qué deja como prueba | Si falla |
|---|---|---|---|---|---|
| 1 | **Identidad** | ¿La entidad representada existe y está en un registro? | Inscripción en registro público o del proyecto (WDPA/Protected Planet, registro nacional) | Referencia de inscripción + los 7 campos de identidad de la parte `eco-` | No hay sujeto: no hay Zona Libre ni obligación (es cobertura, no violación) |
| 2 | **Custodia** | ¿Hay autoridad de gobernanza legítima **con decisión vinculante**? | El estándar exige autoridad y régimen de gestión en funcionamiento | Mandato, tipo de gobernanza (1-4), vigencia, quién decide | **ZONA CIEGA** (si no se mide) o **ZONA HUÉRFANA** (si se mide): violación |
| 3 | **Continuidad** | ¿La custodia tiene historia o es una designación de un día? | Uso consuetudinario sostenido en el tiempo | Serie de continuidad del custodio y de sus decisiones | Zona Libre **no constituida** (catalogable como pendiente, no como lograda) |
| 4 | **Límites** | ¿Hay frontera declarada del espacio no medido? | «Área definida» es el primer criterio del estándar internacional | Polígono o descripción limítrofe verificable + fecha de la delimitación | No hay recinto: la declaración es retórica |
| 5 | **Acceso condicionado** | ¿El contenido se consulta solo con autorización del custodio? | Consentimiento libre, previo e informado (CLPI) | Protocolo de acceso escrito, con quién autoriza, plazos y negativa fundamentada | El interior queda expuesto: deja de ser Zona Libre |
| 6 | **No-sustitución** | ¿La custodia es del territorio o del sistema que lo mide? | El estándar prohíbe suplantar los sistemas de gobernanza existentes | Declaración de no-suplantación + separación entre custodio y guardián oráculo | Captura: el sistema se vuelve custodio de facto → violación |
| 7 | **Precaución** | Donde el contenido es incierto, ¿la decisión es la menos irreversible? | Principio precautorio (CBD, Principio 6 y guía 6.2) + T14 | Registro del costo de oportunidad asumido y de la alternativa descartada | Decisión irreversible sin prueba: violación por T14 |

**Advertencia de forma: no las siete son estrictamente binarias.** Solo la puerta 1 es presencia/ausencia
sin más. Las puertas 2 y 4-7 son **categóricas** (hay o no hay mandato, frontera, protocolo, declaración,
registro de costo), pero su prueba es cualitativa o graduable; y la puerta 3 es la única del conjunto que
**no tiene umbral verificado** (véase la nota siguiente). «Binaria» describe la consecuencia —se pasa o no
se pasa—, no la naturaleza de la prueba. Quien lea esta tabla como siete booleanos automáticos la está
leyendo mal, y decirlo aquí ahorra ese error al documento 08.

**Las siete puertas y los siete campos de identidad del canon no son la misma lista.** El canon exige
que una representación natural declare **siete campos** —*"entidad representada, territorio, fuentes de
datos, límites del mandato, comunidad de custodia, parámetros SDV-E y procedimiento de disputa"*
(Cap. 16.5 §16.5.14; registro del proyecto en
[continuidad_identidad_autogobierno_federado.md](../../architecture/continuidad_identidad_autogobierno_federado.md))—.
Esos campos responden *«¿quién es la parte `eco-`?»*; las puertas responden *«¿cuándo su interior puede
quedar sin medir?»*. El mapeo es este, y las dos puertas nuevas se declaran como tales:

| Puerta | De dónde viene | ¿Nueva? |
|---|---|---|
| 1 Identidad | Campo «entidad representada» + exigencia de **registro público** | 🟡 el campo es canon; el registro público es nuevo |
| 2 Custodia | Campo «comunidad de custodia», con el criterio externo de *autoridad con decisión vinculante* | 🟡 el campo es canon; el criterio de vinculatoriedad es nuevo |
| 3 Continuidad | Aichi Target 18 (uso consuetudinario); *"mínimo dos generaciones = 40 años"* `[REPORTADO: IUCN, 2016]` | **🔴 nueva** |
| 4 Límites | Campo «territorio» + criterio externo «área definida» | 🟡 |
| 5 Acceso condicionado | Campo «fuentes de datos» **invertido**: no qué se consulta, sino cómo se autoriza | **🔴 nueva** |
| 6 No-sustitución | Campo «límites del mandato» + prohibición externa de suplantar gobernanza | 🟡 |
| 7 Precaución | T14 y Cap. 10 §10.3, convertidos en condición auditable | 🟡 el axioma es canon; la puerta es nueva |

**Nota de honestidad sobre la puerta 3.** La cifra «dos generaciones = 40 años» **no** proviene del
texto de la Decisión X/2 de la CBD, sino de la definición operativa que cita el informe de la UICN de
2016; se marca `[REPORTADO]` y no se propone como umbral del SDV-E sin ratificación. Es la única de las
siete puertas que trae un número, y **el documento no la usa como número**: la puerta pregunta «¿hay
historia?», y la cifra solo indica el orden de magnitud de lo que una historia significa.

### 4.4 Qué se delimita: un recinto, nunca un porcentaje

**La diferencia entre la Zona Libre humana y la del ecosistema.** En el SDV-H la Zona Libre es una
**fracción del tiempo propio**: la Opacidad Vital es un porcentaje del TVI (10-20 %) que *"no está
sujeto a auditoría, ni por oráculos ni por otros humanos"* (Cap. 5 §5.9B, Cap. 8 §8.11), y el Mystery
Budget reserva *"un 5-10 % de su TVI colectivo"* (Cap. 7 §7.9). Ese reparto es legítimo porque **el
sujeto es el dueño de su tiempo**. En el Reino Natural no hay dueño: hay custodio. Por eso la Zona
Libre **no puede ser un porcentaje del ecosistema** —decir «el 20 % de este humedal queda libre»
supondría un propietario repartiendo su finca—, sino **un recinto con frontera declarada**, y su
tamaño se decide como se decide un lindero: con criterio ecológico y con política, no con aritmética.

**Consecuencia métrica: la Zona Libre tiene un piso heredado y una plenitud votable.**

- **El piso del tamaño es heredado, no propio.** El recinto no puede ser tan pequeño que viole la
  dimensión cuantitativa *«área mínima para biodiversidad viable»* (Cap. 10 §10.4). Ese piso es LEY y
  no se vota; hoy **no tiene umbral externo verificado** (la matriz de cobertura, sección 11.3 del
  [documento 09](./09_Comparativa_inter_reinos.md), documenta que 6 de las 8 dimensiones canónicas del
  SDV-E carecen de él). Es un hueco heredado que la Zona Libre no puede cerrar por sí sola.
- **Por encima de ese piso, cuánto más se reserva es POLÍTICA** y se vota (§5.2).

**Las tres referencias externas de extensión, en desacuerdo, y por qué no se promedian.** El único
informe técnico verificado sobre un objeto cercano —el registro europeo de áreas silvestres,
contratado por la Comisión Europea— fija **3.000 ha** como umbral operativo de «área silvestre»
(pre-selección en 2.500 ha) y afirma explícitamente que **por debajo «no hay criterio duro»**; considera
**10.000 ha** *"ecológicamente razonable para un funcionamiento efectivo de procesos naturales"* y
clasifica como «wilderness area» un índice de naturalidad **> 70 %** de su valor máximo. [VERIFICADO:
EEA/EC, 2013] En el otro extremo, el estándar de Áreas Clave para la Biodiversidad exige que el **100 %
de la extensión del ecosistema** esté contenida en el sitio, y que albergue **≥ 10 % de la población
global** de una especie. [REPORTADO: cifras leídas en la indexación de la fuente; el PDF de la tipología
IUCN 2024 no se dejó extraer en la sesión de verificación]

**Decisión de este documento: no se elige ninguna de las tres, y se dice por qué.** (i) El registro
europeo mide **naturalidad de un área silvestre**, no extensión de una Zona Libre: importarlo sería el
trasvase que la Regla 4 prohíbe. (ii) El criterio KBA mide **representatividad de un ecosistema en un
sitio**, y una Zona Libre puede ser un recinto **dentro** de una unidad mayor, no el sitio entero.
(iii) Las tres cifras no son tres opiniones sobre lo mismo: son tres objetos distintos. La decisión de
extensión pertenece al **documento 02** de esta biblioteca (unidad y sujeto) y queda
aquí marcada como **`[SIN FUENTE VERIFICADA — pendiente de consenso científico]`**. Lo único que este
documento fija es la condición formal: **sin frontera declarada no hay Zona Libre** (puerta 4).

### 4.5 Los tres regímenes de información (no confundir «no medir» con «no publicar»)

Confusión frecuente y costosa: *no medir* y *no publicar* no son lo mismo. La Zona Libre es lo primero.
El régimen de consentimiento del derecho internacional es lo segundo. El sistema necesita los tres
registros, y cada uno tiene un límite distinto:

| Régimen | Estado del dato | Quién decide | Límite duro |
|---|---|---|---|
| **ZL — No se produce** | El dato **no existe**: el interior no se cuantifica | La unidad, por las siete puertas + catálogo votado | No puede amparar una violación del piso: si hay señal de declive, la presunción cae (§4.6) |
| **Custodiado — Existe y su acceso se autoriza** | El dato existe en poder del custodio (p. ej. conocimiento tradicional) | El custodio, mediante **consentimiento libre, previo e informado** | El CLPI **no puede ocultar una violación** del SDV-E: restringe el acceso al contenido, jamás el registro del daño (T13) |
| **Medido — Se produce y se registra** | El dato existe y entra al registro del sistema | El protocolo del estándar | El registro es público y trazable: *la contabilidad nunca se borra* (T13) |

**Base externa del régimen intermedio.** El Marco Kunming-Montreal (Meta 21) establece que el
conocimiento tradicional *"solo debe ser accedido con su consentimiento libre, previo e informado, de
conformidad con la legislación nacional"* [VERIFICADO: CBD, 2022], y el Artículo 8(j) obliga a
*"respetar, preservar y mantener los conocimientos, innovaciones y prácticas de las comunidades
indígenas y locales […] con la aprobación y participación de los poseedores de tales conocimientos"*,
cuyos términos vinculados en el glosario oficial son *"respect, preserve and maintain knowledge"*,
*"approval and involvement"* y *"prior informed consent"*. [VERIFICADO: CBD, Art. 8(j) y glosario de
términos clave] **El régimen de prueba es «aprobación y participación», no «medición y publicación».**
Ese es, exactamente, el modelo del guardián que consiente.

### 4.6 La presunción de integridad y sus tres señales de caída (el mecanismo que hace auditable la no-medición)

Si el interior no se mide, ¿cómo se sabe que la unidad no está violando su piso? La respuesta honesta
es: **no se sabe por medición; se presume, y la presunción es falsable.** El mecanismo se toma del
criterio B de la Lista Roja de Ecosistemas, que opera por presencia/ausencia de señal
[VERIFICADO: IUCN RLE, criterios v2.2], trasladado aquí a un objeto que el estándar **no** regula: el
mantenimiento de un régimen de no-medición —ese traslado es `[HIPÓTESIS]` y no una prescripción de la
UICN, como se dice también al final de esta sección—:

> **Presunción de integridad (regla del sobre).** Mientras **no aparezca ninguna** de las tres señales
> de declive sobre el **sobre** de la Zona Libre —(i) declive en la extensión espacial, (ii) declive en
> la calidad ambiental, (iii) interrupción de interacciones bióticas—, el interior se presume íntegro y
> no se mide. La aparición de **una sola** señal levanta la presunción y obliga a decidir, en el plazo
> que fije la POLÍTICA: medir (pasar a ZONA MEDIDA y aplicar el SDV-E cuantitativo) o reparar y
> restituir la presunción.

**Qué se gana con esto.** (a) La no-medición deja de ser una afirmación de fe: tiene un **condición de
falsación** y un disparador observable desde fuera. (b) El refugio tiene fecha de caducidad: una
degradación real produce, tarde o temprano, una de las tres señales. (c) El costo de vigilancia es
bajo, porque **las tres señales se observan desde el borde**: extensión (teledetección), calidad ambiental
en el borde (agua, aire, comunidades indicadoras), interacciones (fuego, inundación, herbivoría,
presencia de especies clave). Nada de eso exige inventariar el interior. **Con un límite que hay que
decir:** «calidad ambiental» es el criterio cuya medición directa *sí* puede recaer dentro —la calidad
del agua de un humedal se muestrea en el agua, no en su perímetro—. La regla es que la señal se lea **en
el borde o con indicadores de borde** siempre que existan; donde no existan, la unidad debe declarar en su
inventario negativo que una de las tres señales se vigila por **muestreo interno autorizado por el
custodio**, y ese muestreo **no reabre** el interior a la contabilidad: es una excepción declarada a la
regla del borde, no un permiso para medirlo todo.

**Lo que este mecanismo NO es.** No es una medición encubierta del interior ni un índice disfrazado: es
una **condición de mantenimiento del estado**, con tres disparadores binarios y una consecuencia
declarada. Y no es una invención sin arraigo: es el mismo criterio que el estándar internacional usa
para declarar el riesgo de un ecosistema `[HIPÓTESIS]` en su traslado al mantenimiento de un régimen de
no-medición.

---

## 5. Fórmula de violación, pesos y umbrales

La fórmula del SDV-E no se fija aquí —pertenece al documento 07—, pero una dimensión binaria sin peso
obliga a decir **exactamente** cómo entra y cómo no entra, o el documento 07 heredará una ambigüedad.

### 5.1 Mínimo Absoluto y Óptimo de una dimensión binaria (las dos columnas, separadas)

| Parámetro | Mínimo Absoluto (el piso = LEY, **no votable**) | Óptimo (plenitud aspiracional = POLÍTICA, **votable**) | Fuente |
|---|---|---|---|
| **Existencia del estado** | **7/7 puertas** de §4.3 presentes (presencia/ausencia, sin grados) | — (la existencia no admite plenitud: o hay Zona Libre constituida o no la hay) | UICN OECM, 2019 · CBD V/6 P6 · CBD Meta 21 |
| **Peso en la fórmula** | **0,00** — no pondera y no entra en el numerador | 0,00 (el Óptimo no puede subir el peso: sería canje) | Cap. 8 §8.11 (precedente VIII y IX) |
| **Canje** | **Prohibido**: la Zona Libre no se compensa contra ninguna otra dimensión | Prohibido | Cap. 16.5 §16.5.14 (*el suelo antes que el saldo*) |
| **Registro** | **Obligatorio** (T13): estado, puertas, catálogo, retractaciones | Formato abierto y reutilizable, con series públicas del sobre | Cap. 8 §8.11 · T13 |
| **Columna de plenitud (lo único votable)** | — (el piso de esta fila es solo que **exista** columna de plenitud: sin ella no hay nada que votar) | (a) **tamaño del recinto** por encima del piso heredado de §4.4; (b) **amplitud del catálogo** de lo no medido; (c) **pluralidad** de la comunidad de custodia; (d) **frecuencia y profundidad** de la vigilancia del sobre; (e) **régimen de restitución** del conocimiento que se genere; (f) **prioridad de cobertura** entre unidades | Este documento `[HIPÓTESIS]`; categoría `critical` (quórum 60 %, consenso 75 %, T13, anti-flip-flop 14 días, verificada en `app/voting_bp.py` — `CATEGORY_DEFAULTS` y `EDU_COOLDOWN_DAYS`) |

**Lectura de la tabla, en dos frases.** El piso de esta dimensión **no es un número**: es un
**conjunto de condiciones presentes**. La plenitud **no describe el interior**: describe la calidad con
que se gobierna su sobre. Esa es la traducción exacta de *«lo que no se mide»* a una tabla de estándar
sin traicionarlo.

### 5.2 LEY vs POLÍTICA, explícito

- **LEY (no se vota).** (i) Que el estado **ZONA LIBRE exista y sea alcanzable** en el Reino Natural;
  (ii) que su peso sea **0,00** y no entre jamás en el numerador; (iii) que no sea canjeable; (iv) que
  su violación se registre por T13 y no se cuantifique; (v) que sin custodio no haya Zona Libre
  (§4.2). Nada de esto es votable: es la condición que impide que lo inefable se cambie por saldo.
  *Que sea «alcanzable» significa que ninguna autoridad pueda prohibir el estado: no que toda unidad
  lo alcance, porque las siete puertas de §4.3 no se votan y pueden no pasarse.*
- **POLÍTICA (se vota).** **Qué entra al catálogo** de cada unidad concreta —y con ello qué deja de
  medirse—, el tamaño del recinto por encima del piso heredado, la frecuencia de la vigilancia del
  sobre y las demás columnas de plenitud de §5.1. Se vota con la categoría `critical` (quórum 60 %,
  consenso 75 %, T13, anti-flip-flop 14 días), **con carga de la prueba** y pasando la prueba de
  inefabilidad de §10.3. El Parlamento Educativo (INV2-EDU) es el precedente operativo: la ley del
  motor no se toca, la plenitud se vota, y *"la duda sin dato sigue sin castigarse"*.

### 5.3 Cómo entra en el factor (y la base neutra)

- **Factor de la familia:** `FE = e^v`, con la condición innegociable **`FE(v = 0) = 1,0` exacto**. El
  SDV-S tuvo que corregir `FS_S = 1,0 + e^v` porque recargaba el 100 % incluso sin violación; el SDV-E
  no repite ese error. `[HIPÓTESIS]`, pendiente del documento 07.
- **Aporte de la dimensión `ZL` al factor: siempre `0`.** No es que su violación valga cero: es que
  **no entra en el numerador**. El estado `ZONA LIBRE` aporta `0`; los estados `ZONA CIEGA` y
  `ZONA HUÉRFANA` aportan `0` **y además activan un bloqueo de registro** (§9), que no es una magnitud
  sino una consecuencia. Un `∞` o un peso alto serían, en este punto, la forma técnica de volver
  canjeable lo inconmensurable.
- **Déficit normalizado:** cuando una dimensión cuantitativa del SDV-E use el déficit, se usa la forma
  normalizada `déficit = (requerido − actual) / requerido` —la coherente con el motor—, no la resta sin
  normalizar del paper antiguo. La dimensión `ZL` **no usa déficit**: es binaria.
- **Sin dato no castiga, pero la ley no se negocia.** `[SIN DATO]` en el interior de una Zona Libre
  **no es una violación**: es el estado normal de esa dimensión (Regla 8). `SIN CUSTODIA`, en cambio,
  no es ausencia de dato sino **ausencia de autoridad**, que es un hecho verificable, y sí es violación.

---

## 6. Protocolo de medición (sensores, frecuencias, quién reporta)

**La respuesta corta, y es la tesis del documento: de la Zona Libre no se mide el interior; se vigila
el sobre.** La primera fila de la tabla siguiente es la que el estándar debe poder exhibir sin
vergüenza:

| Objeto | ¿Se mide? | Instrumento / fuente | Quién reporta |
|---|---|---|---|
| **Interior de la Zona Libre** | **No.** No hay instrumento, no hay serie y no hay inventario | **Ninguno** | **Nadie**: no hay dato que reportar |
| **Frontera (sobre)** | Sí: perímetro y cambios de uso en el borde | Teledetección y cartografía (p. ej. Copernicus), registro del custodio | Custodio + tercero técnico |
| **Señales de declive (sobre)** | Sí: las tres de §4.6 | Extensión (teledetección) · calidad ambiental en el borde (agua, aire, indicadores) · interacciones (fuego, inundación, herbivoría) | Custodio + comunidad testigo + tercero técnico |
| **Custodia (sobre)** | Sí: vigencia del mandato, continuidad, disputas, protocolo de acceso | Registro de gobernanza de la unidad | Custodio + auditoría |
| **Presión externa (sobre)** | Sí: extracción, fuego, drenaje, especies invasoras, visitas, infraestructura | Registros administrativos, teledetección, comunidad testigo | Comunidad testigo + autoridad |
| **Conocimiento tradicional (interior)** | **No se mide ni se publica**: se registra **su existencia y su custodio** | Consentimiento libre, previo e informado (Meta 21 · Art. 8(j)) | El custodio, cuando autoriza |

**Ejemplo verificado de «sobre medido, interior no».** Un arrecife con Zona Libre puede tener su estrés
térmico vigilado sin inventariar su interior: la NOAA publica alertas de blanqueamiento por
**grados Celsius-semana** con umbrales **DHW ≥ 4** (Alerta 1: blanqueamiento significativo) y
**DHW ≥ 8** (Alerta 2: blanqueamiento generalizado y mortalidad probable). [VERIFICADO: NOAA Coral Reef
Watch] Eso es exactamente una señal de declive de las tres de §4.6 —calidad ambiental— observada desde
el sobre. Lo que el producto **no** dice es qué hay dentro, ni cuánto vale, ni qué se pierde cuando se
pierde.

**Frecuencia: el estándar no la tiene, y hay que decirlo.** [SIN FUENTE VERIFICADA — pendiente de
consenso científico] No existe ningún estándar internacional que fije **cada cuánto** se vigila el
sobre de un espacio no medido. Lo que sí existe son dos anclas que acotan la discusión:

1. **La ventana del juicio de cambio.** La Lista Roja de Ecosistemas compara contra una ventana de
   **50 años** (y usa *"desde aproximadamente 1750"* para la serie histórica). [VERIFICADO: IUCN RLE
   v2.2] Es decir: el estándar internacional que juzga si un ecosistema cambió **no juzga con lecturas
   anuales**, y este documento no va a proponer una cadencia más fina que el estándar que lo inspira.
2. **La obligación de vigilar la existencia.** Los principios del enfoque por ecosistemas exigen
   gestión adaptativa y seguimiento: *"la gestión debe adaptarse a los cambios"* y *"el seguimiento es
   necesario para aprender de los resultados de las intervenciones"*. [VERIFICADO: CBD, Principios 9 y
   guía 9.x] La no-medición del contenido **no exime** del monitoreo de la existencia: frontera,
   custodio y presión externa se vigilan siempre.

**Propuesta, marcada como propuesta.** `[HIPÓTESIS]` La vigilancia del sobre de una Zona Libre tiene
**una lectura obligatoria por ciclo ecológico dominante de la unidad** (año hidrológico en un humedal o
una cuenca; estación de deshielo en criosfera; temporada de estrés térmico en un arrecife), y su
frecuencia exacta es un **parámetro de plenitud votable** (§5.1, fila (d); la regla de votación, en
§5.2), no un umbral científico. Si la unidad
no tiene ciclo declarado, no puede constituirse como Zona Libre: es la puerta 4 leída en el tiempo.

**Quién reporta, y con qué límite.** Reporta el **custodio** (es su mandato), contradice la **comunidad
testigo** (es su función: *"el sensor del piso que no tiene sensor"*), publica el **sistema** (T13) y
verifica la **auditoría independiente** —que en este estándar tiene un objeto distinto del habitual
(§7)—. Ningún actor puede reportar sobre el interior porque **no debe existir dato del interior**.

---

## 7. Verificación y auditoría (T13, guardián, comunidad testigo)

**El problema estructural, que no se resuelve y hay que decir.** Ningún ecosistema audita a otro
([documento 09](./09_Comparativa_inter_reinos.md) §7). La auditoría viene de fuera del reino: ciencia,
teledetección, comunidad testigo. **El proyecto es juez y parte en la interpretación**, y la única
defensa disponible es la trazabilidad radical: cada veredicto debe poder recalcularse desde datos
públicos, sin acceso al código del proyecto.

**Qué significa auditar una Zona Libre: auditar una ausencia.** El auditor de una Zona Libre no
obtiene el contenido —no puede y no debe—. Su trabajo es verificar **que la ausencia es real y está
bien declarada**. Tres pruebas, todas ejecutables con información pública:

1. **Prueba del borde.** Un tercero puede recorrer el sobre y comprobar la frontera declarada (puerta
   4), la vigencia del custodio (puertas 2 y 3) y la ausencia de presiones no declaradas. **No necesita
   entrar al interior.** Es la prueba que permite auditar sin colonizar.
2. **Prueba de la ausencia (falsabilidad del inventario negativo).** El auditor contrasta la
   declaración de §4.5/§10.5 con los canales de datos del sistema: para **cada** canal —sensores,
   registros administrativos, informes de terceros, contratos, publicaciones, agregadores de
   biodiversidad—, la pregunta es una sola: *¿este canal tiene algún dato del interior de esta unidad?*
   Si la respuesta es sí en cualquier canal, **la declaración es falsa y la Zona Libre cae**. Una
   ausencia declarada es auditable precisamente porque **puede ser contradicha**; una ausencia
   silenciosa, no.
3. **Prueba de no conversión.** Se verifica que ningún producto de la Zona Libre haya entrado en: la
   fórmula del SDV-E (peso distinto de 0,00), el índice agregado (ISE u otro), un crédito regenerativo
   (`r_units` negativo) por el hecho de declararla, un informe de servicios ecosistémicos, o material
   promocional del custodio o del proyecto. Cualquiera de esos usos es **«extracción estética»** y
   viola la puerta 6 y la §9.

**T13 — la contabilidad nunca se borra.** Toda declaración de Zona Libre, todo cambio de estado
(§4.2), toda retractación, todo fallo de puerta y toda señal de declive se registran con su fecha y su
firma de motor. La Zona Libre **no es un espacio sin memoria**: es un espacio sin cuantificación. La
diferencia es la que separa un derecho de un encubrimiento: *"su violación se documenta y es auditable
(T13)"* (Cap. 8 §8.11).

**El guardián oráculo: consiente, no mide, y no sustituye.** El canon asigna al guardián el
consentimiento de la parte `eco-` y le prohíbe dos cosas que este documento convierte en puertas: no
convierte *"automáticamente una lectura ambiental en propiedad humana ni en autoridad absoluta"* y no
puede sustituir al custodio territorial (Cap. 16.5 §16.5.14). Consecuencia operativa explícita, y es
una propuesta de este documento `[HIPÓTESIS]`: **el guardián no puede declarar por sí solo una Zona
Libre.** Si no hay custodio con autoridad legítima, la declaración del guardián produce ZONA CIEGA, no
ZONA LIBRE. Un guardián no puede fabricar un territorio sin autoridad, del mismo modo que —como
establece el [documento 16](./16_Ecosistemas_Montanas_y_criosfera.md) §7 para la criosfera— no puede
fabricar un glaciar con una serie que no existe.

**Comunidad testigo: el sensor del sobre y el guardián del catálogo.** Tiene dos funciones específicas
que ningún satélite cubre: (i) detectar presiones y señales que la serie no recoge —una carretera, una
mina, un drenaje, un proyecto de «restauración» fotogénica—; (ii) **declarar con carga de la prueba**
qué entra al catálogo de lo no medido (§10.3). Es también la única instancia que puede testificar
sobre **continuidad** (puerta 3): la historia de una custodia no está en ningún registro público.

**Riesgos de seguridad abiertos que este documento no cierra y con los que convive.**
**R4** partes fantasma (cualquiera crea un `eco-*` sin autoridad sobre la entidad), **R6** T9 no se
valida en la creación y **R13** guardián `eco` con heurística laxa
([blindaje_anti_gamificacion_equidad.md](../../architecture/blindaje_anti_gamificacion_equidad.md)).
La Zona Libre **agrava** R4 y R13 en un punto concreto y hay que decirlo: un `eco-` fantasma con
custodia inventada podría declarar Zona Libre y sustraer un territorio degradado a la medición. La
puerta 2 (autoridad **con decisión vinculante**, verificable por un tercero) es la respuesta de este
documento, y **es una respuesta parcial**: verificar autoridad sobre un ecosistema no tiene todavía
procedimiento en el repositorio (§12).

**Riesgo nuevo, específico de este documento: captura de la Zona Libre.** Un actor que degrada una
unidad puede intentar declararla Zona Libre para sacarla del estándar. Tres candados: (i) sin custodio
legítimo no hay Zona Libre; (ii) la declaración **no puede inscribirse mientras exista una violación
abierta** de la unidad (se aplica la ventana anti-flip-flop de 14 días del Parlamento como precedente
de enfriamiento, y se prohíbe la conversión ZONA MEDIDA → ZONA LIBRE durante una violación abierta);
(iii) la presunción de integridad de §4.6 es falsable desde fuera y su caída es automática. Estos tres
candados son `[HIPÓTESIS]` de este documento.

---

## 8. Invariante INV2-E: de estándar a contrato ejecutable

**INV2 genérico:** *"Ninguna acción del contrato puede dejar a un participante bajo su SDV"* (Cap. 17).
**INV2-E no existe hoy** y el canon lo convoca con el argumento de apertura de esta biblioteca: *"Un
conjunto con crédito regenerativo acumulado pero humedal bajo su SDV-E no está en coherencia: INV2-E
será su juez"* (Cap. 16.5 §16.5.14). La especificación completa pertenece al documento 08; aquí se fija
**lo que la dimensión `ZL` le exige**, que es poco en aritmética y mucho en tipos:

| Requisito | Especificación `[HIPÓTESIS]` | Por qué |
|---|---|---|
| **Máquina de estados, no bandera** | `estado_zl(parte_eco) ∈ {ZONA_LIBRE, ZONA_MEDIDA, ZONA_CIEGA, ZONA_HUERFANA}` | Una bandera booleana no distingue «no mide porque no debe» de «no mide porque no responde» (§4.2) |
| **Peso** | `peso_zl = 0,00` fijo, en el motor y **no** en la configuración votable | Es LEY (§5.2) y no puede depender de un parámetro |
| **Aporte a `v`** | `v_zl = 0` siempre, para los cuatro estados | Lo inconmensurable no entra en el numerador (Cap. 8 §8.11) |
| **Base neutra** | `FE(v = 0) = 1,0` exacto, con y sin Zona Libre declarada | No repetir el error `1 + e^v` del SDV-S |
| **Bloqueo de registro** | `estado_zl ∈ {ZONA_CIEGA, ZONA_HUERFANA}` ⇒ `coherencia = false` y **prohibición de abonar `r_units < 0`** contra esa unidad | *El suelo antes que el saldo*: el crédito no salda el estado (§9) |
| **Salida del bloqueo** | Se sale **constituyendo custodia** o **midiendo**. **No se sale pagando** | El estado describe; no multa. Una multa convertiría el piso en precio |
| **Sin dato no castiga** | `[SIN DATO]` en el interior **nunca** imputa violación; `SIN CUSTODIA` **siempre** la imputa | INV2-EDU + Regla 8: la duda epistémica no castiga; el hecho de gobernanza, sí |
| **Terminalidad** | El bloqueo de `ZL` **es reversible** (a diferencia de `CONSUMADO_IRREVERSIBLE` del [documento 16](./16_Ecosistemas_Montanas_y_criosfera.md) §8, que no lo es) | Un estado reversible y uno terminal no pueden compartir tipo ni consecuencia |
| **Retractación** | El custodio puede retractar la declaración; el sistema puede revocarla si cae una puerta. **Ambas quedan registradas (T13)** | La memoria de que el interior estuvo sin medir es información legítima sobre la unidad |
| **Capa de Ternura** | No repara el daño — *"el crédito regenerativo acumulado NO compensa caer bajo el SDV-E"*. Solo **modula el estado**: la ZONA CIEGA se enuncia como **descripción con salida**, no como sanción | El sistema no expulsa. Reintegra. Pero la contabilidad nunca se borra |

**Sobre la retractación y su asimetría, que hay que decir sin adornos.** La conversión ZONA LIBRE →
ZONA MEDIDA es **materialmente irreversible**: una vez que el interior se mide y se publica, el dato
existe y T13 no lo borra. La vuelta a ZONA LIBRE puede declararse después, pero **el dato ya producido
permanece**: la unidad no recupera su estado anterior, recupera una etiqueta. Es la primera dimensión
del SDV-E en la que **medir tiene un costo que no se deshace**, y es coherente con la naturaleza del
reino: *«respetamos la soberanía del reino natural sobre su propio TA»* (Cap. 16.5 §16.5.14) — y una lectura
producida tampoco se desproduce.

**Lo que INV2-E no puede hacer, dicho aquí para que el documento 08 no lo prometa.** No puede
comprobar autoridad sobre un ecosistema (R4), no puede convertir una lectura ambiental en mandato sin
guardián (R13), y no puede exigir series que no existen. Lo que **sí** puede hacer, y es lo que este
documento le entrega, es **impedir que la no-medición se confunda con la coherencia**: mientras
`estado_zl` sea `ZONA_CIEGA` o `ZONA_HUERFANA`, ninguna acumulación de crédito regenerativo puede
declarar coherente a esa unidad.

---

## 9. El suelo antes que el saldo (no compensación)

**La doctrina, literal:** *"Un conjunto con crédito regenerativo acumulado pero humedal bajo su SDV-E
no está en coherencia"* (Cap. 16.5 §16.5.14). Aplicada a la Zona Libre, produce cuatro prohibiciones
concretas y una regla de conversión.

**Prohibición 1 — El crédito no salda el estado.** `r_units` negativo (crédito regenerativo, EVV-1.2
§4.3) no puede abonarse contra una unidad en ZONA CIEGA o ZONA HUÉRFANA. Tampoco contra una unidad en
ZONA LIBRE **por el hecho de declararla**: cuidar es una cosa, declarar es otra.

**Prohibición 2 — La Zona Libre no se convierte en índice.** El interior no entra al ISE —Índice de
Salud Ecosistémica (IN-01), con sus pesos 30/20/20/15/15 y sus bandas ≥ 85 / 70-84 / 50-69 / < 50
([metricas_detalle_kpis_oraculos_dinamicos.md](../../architecture/metricas_detalle_kpis_oraculos_dinamicos.md),
IN-01)—, ni a ningún otro agregado. Un índice que premiara la existencia de la Zona Libre crearía el
incentivo exacto que el canon prohíbe: *"jardín podado para la foto no es cuidado; se registra lo que
regenera, no lo que adorna"* (Cap. 16.5 §16.5.14).

**Prohibición 3 — La Zona Libre no se vende como servicio.** Si el valor del interior se declara como
servicio ecosistémico medible, **deja de ser Zona Libre y pasa a ser ZONA MEDIDA** —y esa conversión es
legítima, pero debe declararse, no disfrazarse—. Nota honesta: el mismo recinto podría ser reportado
como «otra medida efectiva de conservación basada en áreas» si cumple los cuatro criterios de la UICN
[VERIFICADO: IUCN WCPA, 2019]; este documento advierte que **diseñar la Zona Libre para obtener esa
etiqueta es extracción estética** y la somete a la prueba 3 de §7. `[HIPÓTESIS]`

**Prohibición 4 — La cobertura no sustituye la custodia.** Que un territorio figure como área
protegida o conservada **no** implica que tenga custodio con autoridad ni Zona Libre legítima: el
estándar internacional advierte que las áreas *"donde no hay autoridad de gobernanza ni régimen de
gestión"* no cumplen los criterios [VERIFICADO], y la propia UICN informa que **el 80 % de las Áreas
Clave para la Biodiversidad no están completamente cubiertas por áreas protegidas** `[REPORTADO: dato
de portada institucional; la cifra y su metodología no se verificaron en documento primario]`. La
lección se sostiene aunque la cifra se degrade: **cobertura y custodia son dos cosas distintas, y la
Zona Libre se define por la segunda.**

**Regla de conversión, con su costo declarado.** ZONA LIBRE → ZONA MEDIDA está permitida en cualquier
momento (medir nunca es un delito) y **es irreversible en cuanto al dato** (§8). ZONA MEDIDA → ZONA
LIBRE exige pasar las siete puertas **y** que no exista violación abierta (§7, candado ii). La
asimetría es deliberada: el sistema debe ser más exigente para dejar de medir que para medir.

---

## 10. Zona Libre: lo que NO se mide

Esta es la sección que da nombre al documento, y su contenido se ordena en seis preguntas.

### 10.1 Qué queda dentro (las cinco categorías)

Inventario honesto de lo que la Zona Libre sustrae a la contabilidad. Ninguna de las cinco es «lo que
no supimos medir»; las cinco son «lo que no debe reducirse a una cifra»:

1. **El valor inefable: la singularidad de esa unidad.** Lo que no se repite en ninguna otra. El canon
   lo dice con la palabra más precisa que tiene: los sensores miden salud, *"jamás «milagros»"*
   (Cap. 16.5 §16.5.14). El milagro no es un dato pendiente: es una categoría distinta.
2. **El conocimiento que todavía no tiene umbral, y puede que nunca lo tenga.** El Principio 6 de la
   CBD admite la ignorancia **permanente**, no transitoria: *"puede que nunca tengamos entendimiento
   perfecto"*. [VERIFICADO] Un caso verificado y grave: *"las necesidades de caudal ecológico son
   actualmente desconocidas para la gran mayoría de los ecosistemas de agua dulce y estuarinos"* —y la
   respuesta del propio derecho ambiental no es esperar, sino *"aplicar el principio precautorio y
   basar los estándares de caudal en el mejor conocimiento disponible"*, además de *"identificar y
   conservar una red global de ríos de flujo libre"*. [VERIFICADO: Declaración de Brisbane, 2007]
   Proteger un río **por su existencia** y no por su índice es, literalmente, Zona Libre.
3. **El conocimiento custodiado (tradicional y local), bajo CLPI.** Existe, no es del sistema y su
   acceso se autoriza (Meta 21 · Art. 8(j)). El sistema documenta **que existe y quién lo custodia**;
   nunca su contenido sin autorización (§4.5).
4. **La vida interna del ecosistema.** El límite lo escribió el canon y hay que citarlo entero:
   *"Nosotros registramos la interacción, no la vida interna del ecosistema"* (Cap. 16.5 §16.5.14).
   La interacción se registra; el interior se respeta.
5. **La posibilidad de que el estándar esté equivocado.** La Zona Libre es también el espacio donde
   **el SDV-E no impone sus categorías**: un lugar donde el fracaso del instrumento no se convierte en
   un veredicto sobre el ecosistema. Es el equivalente ecológico del *"perímetro de respeto"* del
   Cap. 7 §7.9 y la razón por la que la dimensión no puede ponderarse: un instrumento falible no debe
   tener voto de precio sobre aquello que no alcanza.

### 10.2 Quién la custodia (y la respuesta corta: no el sistema)

**El custodio es del territorio; el sistema solo garantiza que exista.** La Zona Libre admite los
cuatro tipos de gobernanza que reconoce el estándar internacional —gobierno; actores privados;
**pueblos indígenas y/o comunidades locales**; gobernanza compartida— [VERIFICADO: IUCN WCPA, 2019], y
los tres últimos son los casos típicos, porque el primero suele traer consigo la obligación de
inventariar. Lo que el SDV-E **no** admite es un quinto tipo: *el sistema que mide*. Esa es la puerta 6
y su consecuencia es directa: **el proyecto no puede ser el custodio de la Zona Libre que declara.**

**Los tres papeles, que no se confunden.** (i) El **custodio**: autoridad legítima con decisión
vinculante sobre el territorio; decide el acceso y responde por la continuidad. (ii) El **guardián
oráculo**: representa a la unidad en el sistema, **consiente** por ella y no la sustituye; no puede
declarar Zona Libre sin custodio (§7). (iii) La **comunidad testigo**: vigila el sobre y declara el
catálogo con carga de la prueba. Ninguno de los tres puede ocupar el lugar de otro, y el estándar debe
poder exhibir esa separación en su registro (puerta 6).

### 10.3 La prueba de inefabilidad (el portero, no la cosecha)

Sin un test, «declarar inefable» sería la vía más barata para vaciar el estándar. El
[documento 16](./16_Ecosistemas_Montanas_y_criosfera.md) §4.2 propuso tres preguntas para la criosfera;
este documento las adopta como **doctrina general**, con el mismo orden y las tres obligatorias:

1. **¿Existe instrumento capaz de medirlo a un coste razonable?** Si existe → **no es Zona Libre: es
   medición pendiente**, y va como deuda de protocolo al documento 06. Esta pregunta sola desactiva la
   mayoría de los intentos de refugio.
2. **¿Medirlo altera o destruye el sujeto?** Un pozo perfora; una parcela se pisotea; un inventario
   exige capturar. Si la respuesta es sí, la tensión se admite —pero se declara como **tensión de
   instrumentación**, que es una razón técnica, no como inefabilidad, que es una categoría distinta.
3. **¿La comunidad de custodia lo declara con carga de la prueba?** Sin declaración motivada y
   registrada, no entra al catálogo. La carga es del proponente (T14), y la prueba es pública.

**Lo que la prueba no hace.** No decide *cuánto* vale lo que queda dentro, ni jerarquiza las cinco
categorías de §10.1, ni sustituye al catálogo votado: decide **si algo puede entrar**, y deja el
**qué** a la POLÍTICA (§5.2).

### 10.4 Un recinto, no un porcentaje (la diferencia con el SDV-H)

Ya argumentado en §4.4 y repetido aquí porque es la decisión de diseño más fácil de malinterpretar: en
el SDV-H la Zona Libre es una **fracción del tiempo propio** (10-20 % del TVI en la Opacidad Vital;
5-10 % del TVI colectivo en el Mystery Budget, Cap. 7 §7.9) y ese reparto es legítimo porque el sujeto
es dueño de su tiempo. En el Reino Natural **no hay dueño**: hay custodio. Repartir porcentajes del
territorio sería actuar *"como su propietario"* en lugar de *"como custodio del patrimonio biológico"*.
Por tanto: **frontera declarada, no fracción aritmética.** Y si alguien quiere dos recintos en la misma
unidad, tendrá dos declaraciones, dos custodios verificables y dos registros.

### 10.5 Cómo se documenta su existencia sin medir su contenido: el inventario negativo

Esta es la aportación técnica central del documento. El registro de una Zona Libre tiene **seis
bloques**, y el sexto es el que no existe en ningún estándar consultado:

| # | Bloque | Contenido | Verificable por |
|---|---|---|---|
| 1 | **Identidad** | Los 7 campos de la parte `eco-` + referencia de inscripción (puerta 1) | Registro público |
| 2 | **Las siete puertas** | Estado de cada puerta, con su prueba y su fecha (puerta 7: costo de oportunidad declarado) | Tercero, sin entrar al interior |
| 3 | **Frontera** | Polígono o descripción limítrofe, fecha de delimitación, autoridad que la fija | Cartografía y recorrido del borde |
| 4 | **Custodia** | Tipo de gobernanza (1-4), mandato, vigencia, continuidad, procedimiento de disputa | Registro de gobernanza |
| 5 | **Protocolo de acceso** | Quién autoriza, cómo se solicita, plazos, forma de la negativa fundamentada | El propio protocolo, publicado |
| 6 | **Inventario negativo** | **La lista explícita de lo que el sistema NO mide de esta unidad**, canal por canal, con la fecha de la declaración | **Falsable**: cualquier tercero que exhiba un dato del interior la contradice |

**Por qué el inventario negativo es la pieza que faltaba.** El canon dice *"los sensores miden salud;
jamás «milagros»"*, pero no dice **cómo se sabe** qué es lo que no se mide. El inventario negativo
responde: se enumera **canal por canal** —teledetección, sensores in situ, registros administrativos,
informes de terceros, contratos, publicaciones científicas, agregadores de biodiversidad, datos de
visitantes— y se declara, para cada uno, que **no produce dato del interior**. Es una afirmación
**falsable y barata**: no exige medir nada, y un tercero puede tumbarla con una sola prueba en contra.
En un sistema que aspira a la Lealtad a la Verdad, **una ausencia declarada y falsable vale más que una
presencia no verificable**.

**El límite del inventario, dicho sin optimismo.** (i) No impide que un tercero externo al sistema mida
el interior por su cuenta —el guardián no es un policía del mundo—: lo que impide es que ese dato
**entre al sistema** y se convierta en veredicto o en precio. (ii) No verifica que la declaración sea
**completa**: la ausencia de un canal en la lista es un error indetectable desde dentro, y de ahí que
la comunidad testigo tenga la potestad de añadir canales. (iii) **No tiene fuente externa**:
`[SIN FUENTE VERIFICADA]` — ningún estándar internacional exige un inventario negativo; es una
propuesta del proyecto, no ratificada, y su valor es exactamente el de una pieza que vuelve auditable
lo que hasta ahora solo era enunciable.

### 10.6 Las dos lecturas del estado de un ecosistema, y por qué deben llevar códigos distintos

Cuando de un ecosistema no hay dato, el sistema actual no distingue **tres situaciones que no tienen
nada que ver entre sí**. Este documento propone separarlas con códigos distintos y consecuencias
distintas:

| Código propuesto | Qué significa | ¿Castiga? | Base |
|---|---|---|---|
| `SIN_DATO_PROPIO` | **Nosotros** no medimos: la unidad está en Zona Libre o el protocolo está pendiente | **No** | INV2-EDU: *"la duda sin evidencia no castiga"*; el canon técnico del SDV-H ya trata `None` como no violación en educación |
| `SIN_UMBRAL_EXTERNO` | **El estándar científico** no tiene el umbral (caudal ecológico, umbrales de cambio) | **No**: es estado del arte, no defecto del protocolo | CBD Principio 6 · Brisbane 2007 |
| `SIN_CUSTODIA` | No hay autoridad de gobernanza legítima | **Sí**: violación de la dimensión `ZL` | UICN OECM, 2019 |

**Por qué esto importa y por qué es la respuesta a la objeción más dura.** La objeción es: *si el
sistema admite «no hay dato», entonces «no hay dato» se convierte en «no hay deber»*. La respuesta es
esta tabla: **el sistema admite dos ausencias epistémicas y una sola ausencia de gobierno; las dos
primeras no castigan y la tercera sí.** Y la tercera **no es una ausencia de información**: es un hecho
verificable sobre el territorio. No se castiga por no saber; se registra por no responder.

**El cierre del pilar 5, en una línea.** La incertidumbre científica no excusa la inacción (Decisión
X/2): por eso `SIN_UMBRAL_EXTERNO` **no** suspende la puerta 7 —donde el umbral falta, se decide por
la opción menos irreversible y se documenta el costo asumido, que es exactamente lo que T14 manda.

### 10.7 La imposibilidad declarada

**No existe, ni puede existir, un umbral del valor inefable.** Se buscó: `[SIN FUENTE VERIFICADA]` en
todas sus formas —índices de valor cultural, métricas de sacralidad, puntuaciones de singularidad— y el
resultado es el esperado, porque el objeto lo excluye. El hecho de que existan **sitios naturales
sagrados** y de que la UICN los trate **por gobernanza y no por métrica** (documento verificado, sin
umbral de superficie ni de naturalidad publicado) no es una carencia de la búsqueda: es la confirmación
de que el régimen correcto para esa clase de valor **es el de la custodia, no el del índice**.

**Consecuencia doctrinal, y es la frase que este documento quiere dejar escrita:** en la Zona Libre, la
ausencia de métrica no es un hueco del estándar **ni una carencia de la ciencia**: es la **forma
correcta** de proteger lo que se destruiría al ser medido. *"Medir todo sería la forma técnica de dejar
de escucharlo"* (Cap. 16.5 §16.5.14). La Zona Libre es la parte del estándar que **se calla a
propósito, y lo declara**.

---

## 11. Comparativa inter-reinos (SDV-H · SDV-A · SDV-E · SDV-S)

La comparación completa —16 ejes— vive en el [documento 09](./09_Comparativa_inter_reinos.md). Aquí se
comparan **solo los ejes que la Zona Libre pone a prueba**: qué se reserva cada reino, cómo se audita
esa reserva y qué pasa cuando se viola.

| Eje | **SDV-H** — humanos | **SDV-A** — animales | **SDV-E** — ecosistemas (este documento) | **SDV-S** — sintéticos |
|---|---|---|---|---|
| **Qué reserva** | Dimensiones VIII (Rehabilitación) y IX (Opacidad Vital) | *No interferencia invasiva*; comportamiento natural | El **interior** de la unidad: valor inefable, conocimiento sin umbral, conocimiento custodiado, vida interna | Dimensión II: Opacidad y Espacio Interior |
| **Unidad de la reserva** | **Fracción del tiempo propio** (10-20 % del TVI; 5-10 % colectivo) | Ámbito de conducta (no un espacio) | **Recinto con frontera declarada** (§4.4) | Espacio interior del agente |
| **Cómo se audita** | Se documenta (T13); cuantificación delegada a la cohorte | No declarado | **Siete puertas + inventario negativo + presunción falsable** (§4.3, §4.6, §10.5) | Bitácora y auditoría cruzada (AOS) |
| **¿Pesa en la fórmula?** | **No**: *"umbrales binarios (presencia/ausencia del derecho), no mediante pesos"* (Cap. 8 §8.11) | **No** declarado | **No**: 0,00, prohibido el canje (§5) | **Sí: 0,20** |
| **Consecuencia de la violación** | Se documenta; hay camino de reintegración | Prohibición de mercado si es sistemática | Documentada + **bloqueo de registro** (reversible): no coherencia, no crédito (§8) | Recargo por opacidad; retractación a 7 ciclos |

**Lo que revela la tabla, en tres frases.**

1. **La Zona Libre es la constante de la familia; el modo, no.** Los cuatro reinos reservan algo. El
   SDV-S lo **pondera** (0,20) y por eso lo vuelve comparable —y canjeable—; el SDV-H lo protege como
   derecho binario sin peso. El SDV-E **hereda el modo del SDV-H** y añade lo que ninguno de los tres
   tiene: **procedimiento de entrada** (puertas) y **prueba de existencia** (inventario negativo).
2. **Es el único reino cuya reserva puede perderse por una puerta.** En el SDV-H la opacidad es un
   derecho del sujeto y no se pierde por falta de custodio; en el SDV-E, sin autoridad de gobernanza
   legítima **la reserva no existe**: es ZONA CIEGA. La diferencia no es de rigor, es de estructura: el
   ecosistema no puede ejercer su derecho por sí mismo.
3. **Es el único caso en que la reserva no protege al sujeto de otro sujeto, sino del propio
   instrumento.** La Zona Libre existe porque el estándar es falible y porque medir transforma. El
   Cap. 7 §7.9 lo llamó *"perímetro de respeto"*; aquí es, además, un mecanismo con portero.

---

## 12. Estado de implementación

**Lo que existe hoy en el repositorio** (verificado por lectura directa de código en esta sesión,
octubre 2026):

| Pieza | Dónde | Estado |
|---|---|---|
| `r_units` negativo como crédito regenerativo | `app/micromax.py` (`v_ucv` no admite negativos; `r_units` sí) | 🟢 implementado y devuelto en el vector `[T, V, R]` |
| Parte `eco-` (Ecosistema) | `app/parties.py` (`PARTY_TYPES`, `COLLECTIVE_PREFIXES` incluyen `eco`) | 🟢 creada y usable |
| Parlamento de parámetros: categoría `critical` | `app/voting_bp.py` (`CATEGORY_DEFAULTS`: `critical` → quórum 0.60, mayoría 0.75; ventana anti-flip-flop de 14 días) | 🟢 implementado — es el mecanismo que la POLÍTICA de la Zona Libre necesita |
| Regla «sin dato no castiga» | `app/sdv_analyzer.py` (`educacion_indice(None) → 1.0`) y `maxocontracts/core/types.py` (`educacion_anos is None` no viola) | 🟢 implementado **para educación**, no para ecología |
| Validador por dimensión con consecuencia binaria | `maxocontracts/blocks/sdv_validator.py` (`block_on_any_violation`; déficit normalizado `relative = deficit / required`) | 🟢 existe **para el SDV-H**: «sin peso» y «bloquea» ya están separados en el motor |
| Guardián oráculo del ecosistema | `app/contracts_bp.py` | 🟡 funciona en la firma de contratos; heurística laxa (R13) |

**Lo que NO existe** (y está prohibido afirmar que existe):

| Pieza | Estado | Evidencia |
|---|---|---|
| Tipo `SDV_E` en el motor | 🔴 | No hay tipo en `maxocontracts/core/types.py`; el gemelo existente es `SDV_S` |
| `INV2-E` | 🔴 | No hay validador de INV2-E en `maxocontracts/core/axioms.py` ni bloque gemelo de `sdv_s_validator.py` |
| Estado `ZL` (los cuatro estados de §4.2) | 🔴 | Ninguna tabla, columna ni enum registra el régimen de medición de una unidad |
| Las siete puertas | 🔴 | Sin campos en `maxo_parties`; los 7 campos de identidad siguen siendo declarativos |
| Inventario negativo | 🔴 | No existe estructura de declaración de ausencia en ningún módulo |
| Presunción de integridad y sus tres señales | 🔴 | Cero sensores, cero ingestores, cero series ecológicas en `app/` |
| Autoridad de custodia verificable (puerta 2) | 🔴 | Sin registro de gobernanza; R4 abierto |
| Quórum `eco-` N-de-M | 🔴 | El camino ecosistema retorna antes de la lógica de quórum |
| Métrica ecológica en código | 🔴 | El ISE es un documento ([metricas_detalle_kpis_oraculos_dinamicos.md](../../architecture/metricas_detalle_kpis_oraculos_dinamicos.md), IN-01) |

**Hallazgo de ingeniería que sí conviene registrar, porque ahorra trabajo.** El motor **ya sabe** hacer
lo que la dimensión `ZL` necesita en su parte dura: en `SDV_S`, `violation_magnitude` usa
`DIMENSION_WEIGHTS` y un peso `0.00` no aporta nada a `v`, mientras que `meets_minimum` decide por
**comparación por dimensión** (`all(...)`), con independencia del peso. Es decir: **«cuánto pesa» y «si
bloquea» ya son dos cosas separadas en el código**. La dimensión `ZL` no exige un motor nuevo; exige un
**tipo categórico** (no numérico) y un bloque validador. [VERIFICADO: lectura directa de
`maxocontracts/core/types.py` y `maxocontracts/blocks/sdv_validator.py` en esta sesión]

**Incoherencias colaterales que no hay que heredar.** (i) `resolve_participant_by_pid`
(`app/parties.py`) asigna a una parte `eco-` el **SDV humano** (`sdv_actual=SDV()`), porque no existe
SDV-E. (ii) El crédito regenerativo se persiste en columnas cuyo nombre alude al VHV, sin `CHECK` de
signo. (iii) `app/maxo.py` cierra el precio en `max(0.0, …)`: **el R del sistema nunca es negativo**,
mientras la documentación del crédito regenerativo ya está escrita.

**Estado de este documento:** texto de estándar redactado, **sin ninguna pieza de código asociada**.
No añade requisitos de implementación nuevos al backlog: hace explícitos los que la Zona Libre implica
(tipo categórico, registro de estados, inventario negativo, verificación de custodia).

---

## 13. Preguntas abiertas

Lo que este documento **no** resuelve, dicho sin fingir cierre:

1. **El umbral de extensión del recinto.** No existe consenso entre las tres referencias externas
   verificadas (3.000 ha operativas y 10.000 ha «ecológicamente razonables» del registro europeo de
   áreas silvestres, y el 100 % de la extensión del ecosistema del criterio KBA `[REPORTADO]`), y **este
   documento no las promedia**: pertenece al documento 02. `[SIN FUENTE VERIFICADA]`
2. **¿Cuánto tiempo puede durar una presunción de integridad sin señal?** La §4.6 fija el disparador
   (una de tres señales) pero **no fija la cadencia mínima de vigilancia del sobre**: no hay fuente
   externa, y la propuesta de «una lectura por ciclo ecológico dominante» es `[HIPÓTESIS]`.
3. **¿Quién verifica la autoridad de un custodio?** Es la puerta 2 y es el punto más débil del
   documento: R4 (partes fantasma) sigue abierto y no existe procedimiento para probar que una
   comunidad, un municipio o un propietario **tiene** autoridad sobre una unidad ecológica. Sin esto,
   la Zona Libre es tan fuerte como su puerta más débil.
4. **La continuidad (puerta 3) no tiene umbral verificable.** La cifra «dos generaciones = 40 años» es
   `[REPORTADO]` desde un informe de la UICN de 2016 y **no** proviene del texto de la Decisión X/2.
   ¿Se ratifica como umbral, o la puerta se queda cualitativa?
5. **¿Puede una Zona Libre ser declarada por un guardián oráculo cuando el custodio es un Estado que no
   consiente?** El documento fija que no (§7), pero eso deja en ZONA CIEGA a ecosistemas con autoridad
   estatal legítima y política de no-monitoreo: un caso frecuente y sin resolver.
6. **La forma exacta del bloqueo en INV2-E.** Que `ZONA CIEGA` impida declarar coherencia y abonar
   crédito es una propuesta; su implementación (¿bloqueo duro en el contrato? ¿estado en la validación
   previa?) pertenece al documento 08 y **no está decidida**.
7. **El inventario negativo no tiene precedente externo.** `[SIN FUENTE VERIFICADA]` Ningún estándar
   exige declarar lo que no se mide. ¿Es suficiente con que sea falsable, o necesita además una
   auditoría periódica de canales? Este documento **no lo decide**.
8. **¿Cómo se audita que la declaración del inventario negativo no es incompleta?** La comunidad testigo
   puede añadir canales, pero no hay procedimiento para saber si **faltan** canales en la lista.
9. **La frontera entre Zona Libre y Zona Medida dentro de la misma unidad.** ¿Puede una unidad tener un
   recinto libre y el resto medido sin que la contabilidad agregada del conjunto se vuelva engañosa
   —es decir, sin que el promedio oculte el estado del recinto? Este documento lo permite (§10.4) y **no
   resuelve** cómo se agrega.
10. **El catálogo y el anti-flip-flop.** Los 14 días del Parlamento Educativo son un precedente para
    cambios de parámetro; **no está claro** que sean suficientes para una conversión ZONA MEDIDA →
    ZONA LIBRE ni si el plazo debería ser ecológico (un ciclo) en vez de administrativo.
11. **La restitución del conocimiento.** Si la Zona Libre produce conocimiento (por ejemplo, un estudio
    autorizado por el custodio), ¿a quién pertenece y cómo se restituye a la comunidad de custodia?
    IPBES documenta la valoración plural y sus metodologías, pero **no un régimen de restitución**.
12. **¿La Zona Libre puede ser reportada como medida de conservación basada en áreas (OECM)?** Podría
    cumplir los cuatro criterios de la UICN, pero este documento advierte que diseñarla para obtener la
    etiqueta es extracción estética (§9). La decisión es `[HIPÓTESIS]` y no está ratificada.
13. **El caso del río que se seca.** Si la unidad deja de existir, la Zona Libre **no se transfiere**
    (§4.2 y documento 02): ¿qué queda del registro, y qué obligaciones sobreviven al sujeto? El canon
    no lo resuelve.
14. **¿Qué impide que un guardián `eco` declare «catálogo vacío» para no medir nada?** La prueba de
    inefabilidad exige que el catálogo se declare **con** carga de la prueba, pero **un catálogo vacío
    no se declara falso**: se declara insuficiente. Falta un procedimiento para eso.

---

## 14. Referencias

**Regla aplicada:** solo URLs con estado HTTP registrado en la sesión de verificación de esta rama
(octubre 2026). Ninguna cifra de este documento se apoya en una URL sin estado. Fuente de trazabilidad:
`scratch/sdv_e/fuentes/04_zona_libre.md` (documento de trabajo, **no** de la biblioteca). Las
afirmaciones sobre el código de la §12 se verificaron por **lectura directa del repositorio**, no por
URL. Todo enlace se re-comprueba con `scripts/verificar_enlaces_sdv_e.py`.

### 14.1 Gobernanza, custodia y áreas conservadas

| Fuente | Aporte | URL (estado HTTP) |
|---|---|---|
| IUCN WCPA, 2019 — *Recognising and reporting other effective area-based conservation measures* | Los cuatro criterios OECM (puertas lógicas, no escalas); los cuatro tipos de gobernanza; *"áreas donde no hay autoridad de gobernanza ni régimen de gestión"* no cumplen los criterios; prohibición de suplantar sistemas de gobernanza existentes | https://portals.iucn.org/library/sites/library/files/documents/PATRS-003-En.pdf (200) |
| UICN, categorías aprobadas en 1994, directrices revisadas en 2008 — Categoría Ib (Área Silvestre), ficha Biodiversity A-Z (UNEP-WCMC) | Definición de área silvestre; objetivo primario de integridad ecológica; objetivo secundario que **permite** que las comunidades indígenas mantengan estilos de vida tradicionales y valores espirituales | https://biodiversitya-z.org/content/iucn-category-ib-wilderness-area.pdf (200) |
| Protected Planet / WDPA (UNEP-WCMC) | Registro público de áreas protegidas: base de la puerta 1 (identidad) | https://www.protectedplanet.net/en (200) |
| UICN — *Protected areas and land use* (página temática) | Dato de portada: **80 % de las Áreas Clave para la Biodiversidad no están completamente cubiertas** por áreas protegidas `[REPORTADO: no verificado en documento primario]` | https://iucn.org/our-work/protected-areas-and-land-use (200) |

### 14.2 Derecho internacional: incertidumbre, conocimiento y precaución

| Fuente | Aporte | URL (estado HTTP) |
|---|---|---|
| CBD, 2000 — *The Ecosystem Approach* (Decisión V/6), texto completo | **Principio 6**: *"considerable falta de conocimiento e incertidumbre sobre los límites reales (umbrales de cambio)"*; *"puede que nunca tengamos entendimiento perfecto"*; guía 6.2: *"debe aplicarse el enfoque precautorio"*. **Principio 11** y guía 11.3: documentar todas las formas de información pertinente, incluido el conocimiento indígena y local | https://www.cbd.int/doc/publications/ea-text-en.pdf (200) |
| CBD — *Principles* (enfoque por ecosistemas) | Principio 9: gestión adaptativa; *"el seguimiento es necesario para aprender de los resultados de las intervenciones"* | https://www.cbd.int/ecosystem/principles.shtml (200) |
| CBD, 2010 — Decisión X/2, Anexo (Meta 18 de Aichi) | Uso consuetudinario sostenido; *"la incertidumbre científica no debe usarse como excusa para la inacción"* | https://www.cbd.int/decision/cop/?id=12268 (200) |
| UICN, 2016 — informe sobre sitios naturales sagrados (PAG-016) | Definición operativa de continuidad biocultural: *"dos generaciones = 40 años"* `[REPORTADO: la cifra proviene de este informe, no del texto de la Decisión X/2; el PDF no se extrajo]` | https://portals.iucn.org/library/sites/library/files/documents/PAG-016.pdf (200) |
| CBD, 2022 — Marco Kunming-Montreal, Meta 21 | Acceso al conocimiento tradicional **solo** con *"consentimiento libre, previo e informado"* | https://www.cbd.int/gbf/targets/21/ (200) |
| CBD — Artículo 8(j) | *"Respetar, preservar y mantener los conocimientos, innovaciones y prácticas de las comunidades indígenas y locales […] con la aprobación y participación de los poseedores de tales conocimientos"* | https://www.cbd.int/convention/articles/?a=cbd-08 (200) |
| CBD — glosario de términos clave sobre conocimiento tradicional | Términos vinculados: *"respect, preserve and maintain knowledge"*, *"approval and involvement"*, *"prior informed consent"* | https://www.cbd.int/tk/keyterms.shtml (200) |
| CBD, 2022 — Marco Kunming-Montreal, Meta 3 | ≥ 30 % de áreas terrestres, de aguas continentales, marinas y costeras para 2030; *"reconociendo los territorios indígenas y tradicionales, cuando proceda"* | https://www.cbd.int/gbf/targets/3/ (200) |
| CBD — Marco Kunming-Montreal (portal) | Marco normativo de referencia | https://www.cbd.int/gbf (200) |

### 14.3 Riesgo ecosistémico, extensión y umbrales del sobre

| Fuente | Aporte | URL (estado HTTP) |
|---|---|---|
| IUCN RLE, criterios v2.2 — resumen (EN) | Criterio B: activación con **≥ 1 de 3** señales (extensión espacial, calidad ambiental, interrupción de interacciones bióticas) — **forma binaria verificada**; ventana de comparación de 50 años y serie histórica *"desde aproximadamente 1750"*; umbrales de colapso CR ≥ 50 % en 50 años · EN ≥ 20 % en 50 años · VU ≥ 10 % en 100 años; EOO ≤ 2.000 / 20.000 / 50.000 km²; AOO ≤ 2 / 20 / 50 celdas de 10 × 10 km; severidad de disrupción ≥ 80 % / 50 % / 30 % | https://www.iucnrle.org/documents/tools-and-training-docs/IUCN%20Red%20List%20of%20Ecosystems%20Criteria%20Summary%20Sheet_2.2_EN.pdf (200) |
| IUCN RLE, directrices v1.1 (2017) | Documento donde consta la categoría *Data Deficient*: **`[REPORTADO]`** — el PDF se descargó (200) pero no se dejó extraer; **no se encontró umbral numérico que active la categoría** | https://portals.iucn.org/library/sites/library/files/documents/2017-010.pdf (200) |
| Wilderness Register and Indicator for Europe (EEA/EC, 2013) — informe técnico del registro europeo de áreas silvestres | 3.000 ha = umbral operativo de «área silvestre» (pre-selección 2.500 ha) y **«no hay criterio duro» por debajo**; 10.000 ha *"ecológicamente razonable"*; clasificación con índice de naturalidad > 70 % del máximo | https://wilderness-society.org/wp-content/uploads/2022/08/Wilderness_register_indicator.pdf (200) — cifras leídas en el informe; la atribución «contratado por la Comisión Europea» es `[REPORTADO]` del propio documento y no se verificó en una fuente de la Comisión |
| IUCN, 2024 — Tipología Global de Ecosistemas (PDF) | Criterios de Área Clave para la Biodiversidad: **100 % de la extensión del ecosistema** en el sitio; **≥ 10 % de la población global** de la especie `[REPORTADO: cifras leídas en la indexación de la fuente; el PDF no se dejó extraer]` | https://portals.iucn.org/library/sites/library/files/documents/2024-021-En.pdf (200) |
| NOAA Coral Reef Watch — descripción de productos | Ejemplo verificado de **sobre medido, interior no**: alertas por grados Celsius-semana, **DHW ≥ 4** (Alerta 1) y **DHW ≥ 8** (Alerta 2) | https://coralreefwatch.noaa.gov/product/50km/description_vs_graphs.php (200) |

### 14.4 Valoración plural y límites del instrumento

| Fuente | Aporte | URL (estado HTTP) |
|---|---|---|
| IPBES — *Values assessment* | Grupo de expertos sobre *"conceptualización diversa de valores múltiples"* y enfoque metodológico de valoración | https://www.ipbes.net/values-assessment (200) |
| IPBES, 2018 — IPBES/6/INF/18 | Guía metodológica de la valoración plural | https://www.ipbes.net/resource-file/12746 (200) |
| IPBES, 2022 — nota de prensa de la evaluación de valores | Las decisiones basadas en *"un conjunto estrecho de valores de mercado de la naturaleza"* sustentan la crisis de biodiversidad: respaldo institucional a que la valoración estrecha es un factor causal | https://www.ipbes.net/media_release/Values_Assessment_Published (200) |
| Living Planet Index (ZSL) | Indicador de **tendencia** de poblaciones de vertebrados, normalizado a 1,0 en 1970: se cita aquí para distinguir *indicador de tendencia* de *umbral legal* | https://www.livingplanetindex.org/ (200) |
| Stockholm Resilience Centre — integridad de la biosfera | Marco de fronteras planetarias; apropiación humana de la producción primaria neta (HANPP) 30 %; tasa de extinción observada > 100 E/MSY frente a la frontera < 10 E/MSY | https://www.stockholmresilience.org/research/planetary-boundaries/the-nine-planetary-boundaries/biosphere-integrity.html (200) |
| Copernicus (observación de la Tierra) | Infraestructura candidata para la vigilancia del sobre (frontera y cambios de uso) | https://www.copernicus.eu/en (200) |

### 14.5 Fuentes leídas pero no citadas como umbral (y por qué)

- **Convención de Ramsar — Criterios 5 y 6** (20.000 aves acuáticas; 1 % de la población de una especie
  o subespecie): el **texto** de los criterios es `[VERIFICADO]` en un artefacto extraído por una sesión
  hermana, pero **la URL de origen no está trazada** y las once rutas probadas de `ramsar.org`
  devuelven **403** en esta sesión. Consecuencia explícita: **este documento puede atribuir el umbral a
  la Convención de Ramsar, pero no cita una URL de `ramsar.org`**. `[SIN URL VERIFICADA]` — pendiente
  de una sesión con acceso humano al sitio.
- **Umbral de «cuánto del ecosistema queda sin medir»**: `[SIN FUENTE VERIFICADA]`. No existe en ningún
  estándar internacional consultado. **Es el aporte propio de este documento**, no un umbral a
  importar, y por eso va marcado como propuesta no ratificada.
- **Quórum `eco-` N-de-M**: `[SIN FUENTE VERIFICADA]`. Ningún organismo publica quórum de gobernanza
  para ecosistemas; pertenece al documento 05.
- **Criterios de un «guardián oráculo» / representación sintética de un ecosistema**:
  `[SIN FUENTE VERIFICADA]`. Sin precedente internacional. Propuesta del proyecto (riesgos R4/R6/R13).
- **Umbral de «milagro ecológico» / valor inefable cuantificado**: **imposible por definición del
  dominio** (§10.7). Se registra como imposibilidad declarada, no como carencia de búsqueda.
- **Test que demuestre que la contabilidad no colonizó el TA**: `[SIN FUENTE VERIFICADA]` en el ámbito
  externo. El criterio propuesto por el [documento 16](./16_Ecosistemas_Montanas_y_criosfera.md) §5.3
  (invariancia al periodo contable) pertenece al documento 03 y **este documento no lo importa**: solo
  registra que una Zona Libre no puede producir ningún dato expresado en TVI sin quedar colonizada.

### 14.6 Referencias internas al canon (por capítulo y sección, sin anclas de línea)

- Cap. 5 §5.5 — Tres tiempos (TVI, TA, TPI), PIU como único traductor TA↔TVI, y T14 (Principio de
  Precaución Intergeneracional): [capitulo_05_arquitectura_260126.md](../../book/edicion_3_dinamica/capitulo_05_arquitectura_260126.md)
- Cap. 7 §7.9 — Lo que el VHV no mide por diseño; *"perímetro de respeto"*; Mystery Budget:
  [capitulo_07_vhv_260126.md](../../book/edicion_3_dinamica/capitulo_07_vhv_260126.md)
- Cap. 8 §8.11 — Dimensiones VIII y IX: umbrales binarios de presencia/ausencia, **sin pesos en la
  fórmula**: [capitulo_08_sdv_h_260126.md](../../book/edicion_3_dinamica/capitulo_08_sdv_h_260126.md)
- Cap. 9.5 §9.5.7-§9.5.11 — `FS_S = e^v`, base neutra, opacidad ponderada (0,20) del SDV-S:
  [capitulo_09_5_sdv_sinteticos_260126.md](../../book/edicion_3_dinamica/capitulo_09_5_sdv_sinteticos_260126.md)
- Cap. 10 §10.3, §10.4, §10.5, §10.6, §10.7 — Principio Precautorio de Consciencia; SDV para
  ecosistemas y para lugares; proporcionalidad; dignidad encadenada; gobernanza operacionalmente
  finita: [capitulo_10_tres_reinos_260126.md](../../book/edicion_3_dinamica/capitulo_10_tres_reinos_260126.md)
- Cap. 16.5 §16.5.14 — El hogar extendido: crédito regenerativo, TA soberano, representación
  `eco-`, Zona Libre, *«el suelo antes que el saldo»*, cuidado ≠ extracción estética:
  [capitulo_16_5_micromaxocracia_canonica_220826.md](../../book/edicion_3_dinamica/capitulo_16_5_micromaxocracia_canonica_220826.md)
- EVV-1.2 §4.3 — R negativo = regeneración:
  [capitulo_18_EVV_1.2_270126.md](../../book/edicion_3_dinamica/capitulo_18_EVV_1.2_270126.md)
- Índice de Salud Ecosistémica (IN-01), pesos 30/20/20/15/15 y bandas ≥ 85 / 70-84 / 50-69 / < 50, que
  §9 cita como el agregado al que la Zona Libre **no** puede entrar:
  [metricas_detalle_kpis_oraculos_dinamicos.md](../../architecture/metricas_detalle_kpis_oraculos_dinamicos.md)
- Índice de Salud Ecosistémica (IN-01), pesos y bandas:
  [metricas_detalle_kpis_oraculos_dinamicos.md](../../architecture/metricas_detalle_kpis_oraculos_dinamicos.md)
- Identidad de una representación natural (7 campos) y prohibición de deriva silenciosa:
  [continuidad_identidad_autogobierno_federado.md](../../architecture/continuidad_identidad_autogobierno_federado.md)
- Riesgos R4 (partes fantasma), R6 (T9 no validado en creación) y R13 (guardián `eco` laxo):
  [blindaje_anti_gamificacion_equidad.md](../../architecture/blindaje_anti_gamificacion_equidad.md)

### 14.7 Referencias internas a esta biblioteca

**Documentos ya escritos** (enlace relativo, sin anclas):

- [08 — INV2-E: de estándar a contrato ejecutable](./08_INV2-E_invariante.md) — el invariante que este
  documento alimenta con el estado `ZL` (§8).
- [09 — Comparativa inter-reinos](./09_Comparativa_inter_reinos.md) — la comparación de 16 ejes y la
  pregunta abierta 10, que la matriz de §4.2 responde por construcción.
- [16 — Ecosistemas de montañas y criosfera](./16_Ecosistemas_Montanas_y_criosfera.md) — primer caso
  aplicado de la Zona Libre (`D7`), la prueba de inefabilidad que aquí se generaliza (§10.3) y el
  criterio de no colonización del TA (§14.5).

**Documentos de esta biblioteca citados por número, todavía no escritos o no verificados en esta
sesión:** 00 (índice), 02 (unidad y sujeto — decide la extensión del recinto, §4.4), 05 (representación,
guardián y mandato — decide el quórum `eco-`), 06 (medición y verificación — recibe las deudas de
protocolo), 07 (fórmula de violación y pesos — fija el factor `FE`). **No se enlazan como archivo
porque el archivo no existe**: la cita es por número de documento y sigue siendo válida sin el enlace.
Cuando los documentos se escriban, los enlaces deben apuntar a `./0X_*.md` **y comprobarse archivo por
archivo antes de darse por buenos** —no basta con que la ruta sea sintácticamente correcta—.

**Alcance de «ya escritos», dicho con precisión, porque la lista no se agota arriba:** en el momento de
redactar este documento el directorio `docs/theory/SDV-E/` contiene ocho archivos —04, 08, 09, 10, 13,
14, 16 y 18—, de modo que los documentos 10, 13, 14 y 18 también existen y este documento **no** los
enlaza porque no los cita. Los «escritos» de la lista anterior son los tres que la Zona Libre necesita
como interlocutores, no el inventario completo de la biblioteca. Los números ausentes de ese inventario
(00, 01, 02, 03, 05, 06, 07, 11, 12, 15, 17 y los transversales 20-23) **no existían al cerrar esta
sesión**, y su ausencia se declara aquí para que nadie la confunda con un enlace roto.

**Nota de trazabilidad de rutas, y es una advertencia útil para el resto de la biblioteca.** Desde
`docs/theory/SDV-E/`, el canon del libro se alcanza con **`../../book/edicion_3_dinamica/…`** (esto es,
`docs/book/…`). La forma `../../../book/…` **no resuelve**: apunta a un directorio `book/` en la raíz
del repositorio que no existe. Este documento usa la primera y la comprobó archivo por archivo.
[VERIFICADO: comprobación de rutas en esta sesión] Otras páginas de la biblioteca usan la segunda
forma y **sus enlaces al canon están rotos**, aunque la cita doctrinal —que es por capítulo y sección—
siga siendo correcta.

---

## Cierre

La Zona Libre es la parte del SDV-E que **no se puede contar sin destruirla**, y este documento se
niega a hacerlo de dos maneras a la vez: no la pondera (peso 0,00, sin canje) y **no la deja sin
procedimiento**. Lo que queda dentro no se mide —el milagro, el conocimiento sin umbral, el
conocimiento custodiado, la vida interna, la posibilidad de que el estándar se equivoque—, pero lo que
queda **fuera** se registra con precisión: siete puertas, una frontera declarada, un custodio con
autoridad verificable, un protocolo de acceso, un inventario negativo falsable y una presunción de
integridad que cae con una sola señal.

La doctrina que sostiene el edificio cabe en tres frases. **Sin custodio no hay Zona Libre**: lo no
medido sin autoridad no es reserva, es abandono. **Sin peso no hay canje**: lo inconmensurable no
negocia con el piso. Y **sin dato no hay castigo, pero tampoco permiso**: la incertidumbre no imputa
violación al ecosistema ni autoriza la intervención de nadie.

Todo lo demás —umbrales de extensión, cadencia de vigilancia, quórum `eco-`, verificación de
autoridad— está dicho aquí como lo que es: **propuesta no ratificada**. El canon nombra la Zona Libre y
no la resuelve; este documento la vuelve auditable y deja escrito, sin adorno, lo que todavía no sabe.
