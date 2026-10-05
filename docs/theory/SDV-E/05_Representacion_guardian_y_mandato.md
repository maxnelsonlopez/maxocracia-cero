# Representación, guardián y mandato del Reino Natural
## Los mínimos de la voz: quién puede hablar por un ecosistema, con qué mandato, con qué quórum y con qué derecho a disputar

**Autoría:** Oráculo Sintético DeepSeek & Max Nelson López Restrepo
**Fecha:** octubre 2026
**Proyecto:** Maxocracia — El gobierno de la verdad, el tiempo y la vida
**Licencia:** Creative Commons BY-SA 4.0
**Estado:** Propuesta de estándar (rama SDV-E, Ola 4) — NO canon hasta ratificación
**Referencia canónica:** Cap. 10 §10.4 · Cap. 16.5 §16.5.14 · EVV-1.2 §4.3 · Cap. 9.5 (precedente SDV-S)
**Documento:** 05 de la biblioteca `docs/theory/SDV-E/`
**Foco:** partes `eco-`, guardián oráculo, los **7 campos obligatorios de identidad** de una representación
natural, la **propuesta de quórum N-de-M** para el reino natural (hoy inexistente), el **procedimiento de
disputa** y los riesgos abiertos **R4** (partes fantasma), **R6** (contrato unilateral) y **R13** (guardián
con heurística laxa), con salvaguardas concretas y ancladas.

---

> *"Ningún acuerdo que afecte su humedal o su arbolada es legítimo sin el consenso de su parte `eco-` —
> el guardián consiente por quienes no firman con manos."* — Cap. 16.5 §16.5.14
>
> *"Un bosque o un río **no debe ser reducido a una cuenta operada por humanos**. (…) El oráculo
> representante propone y vigila; no convierte automáticamente una lectura ambiental en propiedad humana
> ni en autoridad absoluta."* — [continuidad_identidad_autogobierno_federado.md](../../architecture/continuidad_identidad_autogobierno_federado.md) §8.1

---

## 1. Qué es (y qué no es) este SDV

**Qué es.** Este documento fija el **estándar de la voz** del SDV-E. Los documentos 07 y 10-18 de esta
biblioteca dirán *qué mínimo ecológico* no puede cruzar una unidad natural; este documento dice **quién
puede afirmar, en nombre de esa unidad, que el mínimo se respetó o se violó**, con qué documentos, con qué
mandato, con qué mayoría y con qué vía de queja. Sin esta pieza, el SDV-E es un número sin hablante: se
puede calcular la violación de un humedal y no hay nadie legitimado para firmar el resultado ni para
objetarlo.

**Por qué existe.** El canon ya tiene la infraestructura y ya tiene el hueco. La tiene: las partes `eco-`
de MaxoContracts, el guardián oráculo, el quórum delegado N-de-M «anunciado» y los contratos interescala
(Cap. 16.5 §16.5.14). Y tiene el hueco, en tres capas que se refuerzan:

1. **La identidad no está especificada como estándar.** El canon enumera 7 campos obligatorios
   (*entidad representada, territorio, fuentes de datos, límites del mandato, comunidad de custodia,
   parámetros SDV-E y procedimiento de disputa*) pero no dice qué documento satisface cada campo, quién lo
   verifica ni qué pasa si falta.
2. **El quórum no existe.** El canon dice «N-de-M» y solo publica números para cooperativas y órganos
   humanos. No hay N ni M para el reino natural.
3. **El guardián consiente sin autoridad verificada.** Cualquier usuario autenticado puede crear la parte
   `eco-*` que después dará el consentimiento, y puede invocar a su guardián. Los riesgos R4, R6 y R13 del
   [blindaje anti-gamificación](../../architecture/blindaje_anti_gamificacion_equidad.md) son las tres
   formas concretas de ese hueco.

**La tesis de este documento, en una línea:** *un piso ecológico sin representante legítimo no es un piso,
es una casilla*; y un representante sin autoridad verificada es peor que ninguno, porque convierte la
degradación en cumplimiento firmado.

**Qué no es.**

- **No fija umbrales ecológicos.** Este dominio **no tiene umbral científico de representación**: no existe
  un «nivel óptimo» de voz para un río. Lo que existe —y se usa aquí— son **reglas de decisión vinculantes
  de derecho ambiental internacional y estándares de gobernanza de áreas protegidas**, con cifras duras y
  verificables. Se citan como **precedente normativo**, jamás como umbral ecológico. En consecuencia, las
  dos columnas de este documento son **LEY** (el piso: admisible o no admisible, no votable) y **POLÍTICA**
  (la plenitud: votable con el precedente del Parlamento Educativo, INV2-EDU).
- **No define la unidad del SDV-E.** ¿Tipo de ecosistema, bioma, cuenca, lugar concreto o parte `eco-`
  instanciada? Esa decisión pertenece al documento 02 de esta biblioteca. Este documento **depende** de esa
  decisión para el valor de **M** (tamaño del consejo) y lo declara abiertamente en §5.2 y §13.
- **No define «Persona Natural» ni personalidad ecológica.** No existe fuente normativa verificada que
  otorgue personalidad jurídica graduada a ecosistemas con criterios numéricos; este documento no la
  inventa. Habla de **representación**, que es una figura institucional, no de personalidad.
- **No es la especificación de INV2-E.** Esa vive en el [documento 08](./08_INV2-E_invariante.md). Aquí
  solo se fija la parte de INV2-E que toca a la representación (§8).
- **No es canon.** Es una propuesta de estándar de la rama SDV-E, Ola 4, **no ratificada**.

**Marcas de evidencia usadas en todo el texto.** `[VERIFICADO]` = comprobado con herramienta o leído en el
archivo citado. `[REPORTADO]` = afirmado por una fuente que cito sin haber podido abrir el documento
completo. `[HIPÓTESIS]` = inferencia razonada del proyecto, no observación. **Convención de esta
biblioteca:** las citas de organismos externos (IUCN, OCDE, CBD, GCF, Banco Mundial, CAO) van marcadas
`[REPORTADO]` —su localización está verificada, el PDF no se abrió en esta sesión—; `[VERIFICADO]` se
reserva para lo que se comprobó directamente aquí: la lectura del código del repositorio (§12) y las citas
internas al canon. Es coherente con la nota de trazabilidad de §14 y evita marcar como verificado lo que
solo está reportado.
`[SIN FUENTE VERIFICADA — pendiente de consenso científico]` = busqué el umbral y no existe fuente
verificable. Las cuatro marcas son resultados legítimos.

---

## 2. Preámbulo metodológico

El SDV-H lo tiene y el SDV-S lo omitió; el brief de esta biblioteca prohíbe repetir la omisión. Aquí el
preámbulo es más necesario que en ningún otro documento, porque **este es el único SDV cuyo dominio no es
biofísico**: no hay un instrumento que mida la legitimidad de una voz. Las nueve reglas siguientes son el
sustituto.

**Regla 1 — Este dominio no tiene umbral ecológico; tiene precedente normativo.** Todo número de este
documento viene de una **regla de decisión publicada** por un órgano de gobernanza ambiental (CBD, GCF,
UNCCD, OCDE, IUCN, Banco Mundial) o de una **definición operativa** de una fuente técnica (FAO, Copernicus).
Ninguno se presenta como «el óptimo científico de la representación», porque ese óptimo no existe.

**Regla 2 — Toda extrapolación se declara.** Los órganos que publican esas cifras gobiernan **personas**
(Partes, Juntas, ciudadanos sorteados). Aplicarlas a un sujeto que no habla es una **analogía**, no una
transposición. Cada vez que la hago, la marco `[HIPÓTESIS]` y digo de dónde viene el número.

**Regla 3 — El guardián consiente, no mide.** Es regla dura del canon operativo (`app/contracts_bp.py`:
*"Ecosistemas (eco-*): consentimiento otorgado por el guardián oráculo"*) y del
[documento 08](./08_INV2-E_invariante.md) §3. Un guardián que midiera sería un juez que fabrica su propia
prueba.

**Regla 4 — La voz se prueba con hechos de gobernanza, no con declaraciones de intención.** El criterio
externo es **autoridad, responsabilidad y rendición de cuentas de facto** (IUCN, 2013, §9.1, `[REPORTADO]`),
no el documento que el creador de la parte firma.

**Regla 5 — El consentimiento no se presume.** Es el principio más fuerte disponible contra R6 y está
publicado en fuente verificada: *"Consent and agreement should not be 'assumed', and, indeed, it may not be
forthcoming"* (IUCN, 2013, §5.2, `[REPORTADO]`). Todo este documento está construido para que la ausencia de
consentimiento sea un estado representable, y no un silencio que se lee como sí.

**Regla 6 — La gobernanza debe ser operacionalmente finita (Cap. 10 §10.7).** El SDV-E **no puede** exigir
modelar la cadena trófica completa para decidir. Por eso las condiciones de este documento son **nueve
binarios y una regla de mayoría**, no un modelo.

**Regla 7 — La celda vacía es un hallazgo.** Donde no hay fuente, se escribe
`[SIN FUENTE VERIFICADA — pendiente de consenso científico]`. **Once parámetros** del estándar llevan esa
marca y están enumerados en §13.1-§13.9: seis coinciden con los vacíos que declaró el informe de fuentes
(M, N, peso por delegado, criterio numérico de autoridad, escala mínima de la unidad y plazos para un sujeto
no humano) y cinco son propios de este documento (duración del mandato, frecuencia de auditoría del guardián,
umbral de confianza de sus lecturas y dos huecos de fuente de §6). Ninguno se rellena con diseño interno
disfrazado de dato. El informe de fuentes declaró **16 parámetros sin fuente** en el dominio completo; los
cinco suyos que no aparecen aquí (Lista Roja, Aarhus, Ramsar, GEF y umbral de asimetría) quedan fuera del
alcance de este documento.

**Regla 8 — Tiempo = TA; el PIU es el único traductor.** El tiempo del territorio es **Tiempo Absoluto** y
no se coloniza (Cap. 16.5 §16.5.14). La representación **no** crea un TVI del ecosistema: registra
interacción. Ningún plazo de este documento (auditorías, mandatos, disputas) es tiempo vital del
ecosistema; son plazos institucionales humanos.

**Regla 9 — LEY no se vota; POLÍTICA sí.** La frontera se aplica fila por fila. La ley (el piso) vive en el
motor y no es votable; la plenitud aspiracional se vota con el precedente del Parlamento Educativo
(INV2-EDU: categoría `critical`, quórum 60 %, consenso 75 %, T13, anti-flip-flop 14 días, `CHECK` en BD —
`app/voting_bp.py`, `CATEGORY_DEFAULTS`).

---

## 3. Pilares epistemológicos

**P1 — No existe un umbral ecológico de representación; existe un estándar auditable.** La investigación de
fuentes de este documento verificó **41 parámetros con cifra** y **16 declarados sin fuente** en el dominio.
Ninguno de los 41 es un umbral ecológico; los que la intuición pediría como umbrales (M, peso por delegado,
plazos para un sujeto no humano) están entre los 16 sin fuente, y **once de ellos** aparecen aquí como
parámetros abiertos (§13.1-§13.9). El estándar se construye con lo que hay: precedente normativo.

**P2 — Los 7 campos no son una ficha descriptiva: son 7 precondiciones binarias de admisibilidad.**
`[HIPÓTESIS]` Cada campo tiene un homólogo verificable en el estándar IUCN Green List y en la guía de
gobernanza de la IUCN (§4). Una parte `eco-*` que no pueda exhibir los 7 documentos **no se instancia como
sujeto con voz**. Esta es la salvaguarda raíz contra R4, y es también el motivo por el que el estándar de
representación tiene que existir *antes* que la contabilidad («estándar primero, contabilidad después»,
Cap. 16.5 §16.5.14).

**P3 — El guardián no decide el fondo, solo el proceso.** El precedente externo es explícito: los terceros
neutrales de un mecanismo de reparación *"do not make decisions on substance, but focus on managing the
process"* (GCF-IRM, funciones y procesos, `[REPORTADO]`). El guardián **consiente o no consiente** un
término; no fija el piso, no sustituye a la ciencia, no apropia.

**P4 — El ejecutor debe estar a distancia del comitente (*arm's length*).** *"The final call regarding
process decisions should be with the arm's length co-ordinators rather than the commissioning
authorities"* (OCDE, 2020, principio *Integrity*, `[REPORTADO]`). Un guardián designado, invocado o
financiado por la parte que se beneficia del contrato no es un guardián; es un trámite.

**P5 — T14 carga la prueba sobre quien propone.** T14 — Principio de Precaución Intergeneracional
(Cap. 5 §5.3): *"Ante incertidumbre sobre el impacto en agentes que no pueden consentir (ecosistemas,
generaciones futuras, posibles consciencias sintéticas), el sistema debe elegir la opción de menor
irreversibilidad, documentando el costo de oportunidad asumido. La carga de la prueba recae sobre quien
propone acciones que afectan la temporalidad de no-participantes."* Aplicado a la representación: **quien
crea la parte `eco-` es quien propone, y por tanto quien debe probar autoridad, territorio, fuentes y
custodia.** El ecosistema no prueba nada; no puede.

**P6 — T13 se aplica al guardián.** *"Nadie puede imponer un valor temporal en secreto. Todo cálculo de
costo vital debe ser auditable públicamente"* (T13, Cap. 5 §5.3). El consentimiento del guardián es un
cálculo que afecta a un tercero que no firma: debe quedar como **cuenta escrita**, no como booleano. El
precedente externo de rendición de cuentas **formal-deliberativa** existe: *"Collective written accounts to
fellow representatives or the public"* (OCDE, 2020, Tabla 6.1, `[REPORTADO]`).

**P7 — La representación no es propiedad ni autoridad absoluta.** Canon explícito (§8.1 del documento de
continuidad y arquetipo): el oráculo **propone y vigila**. La consecuencia operativa que este documento
deriva `[HIPÓTESIS]` es que el guardián **no puede** firmar en nombre del ecosistema una cesión de su SDV-E,
ni renunciar a la retractación, ni aceptar compensación por la violación. Eso no es consentimiento: es
enajenación de un tercero.

**P8 — Custodia, no propiedad.** El marco externo coincide: *"actuar como custodio del patrimonio
biológico, no como su propietario"* y la definición operativa de gobernanza de la IUCN (*"who holds
authority, responsibility and can be held accountable for the key decisions"*, IUCN, 2013, Tabla 4).

---

## 4. Dimensiones del SDV-E de la representación

Las siete primeras dimensiones **son** los 7 campos obligatorios del canon, en su orden. Las dimensiones
VIII y IX son las dos piezas que el canon no enumera y que este documento aporta: **cómo se decide**
(quórum) y **qué no se publica** (opacidad legítima, dimensión binaria sin peso).

> **Frontera LEY/POLÍTICA, explícita.** En cada tabla: **Mínimo Absoluto = LEY** (presencia o ausencia; no
> votable; sin él la parte no es admisible) y **Óptimo = POLÍTICA** (votable con categoría `critical`,
> precedente INV2-EDU). Ninguna fila mezcla las dos columnas: el error del motor del SDV-H —confundir el
> óptimo del agua con el mínimo— sería aquí fatal, porque un «óptimo» de representación que se aplicara como
> piso dejaría a casi toda unidad natural sin voz, y un «mínimo» que se aplicara como meta vaciaría el
> estándar.

### Dimensión I: Entidad representada y tipo de gobernanza declarado (quién es el sujeto, y bajo qué régimen)

**Qué protege.** Que exista un sujeto identificable y un régimen de gobernanza **declarado y público**, en
lugar de un nombre en una tabla.

| Parámetro | Mínimo Absoluto (el piso = LEY) | Óptimo (plenitud aspiracional = POLÍTICA) | Fuente |
|---|---|---|---|
| Estructura de gobernanza definida **y documentada** | Presencia de documento público verificable (binario) | Documento actualizado tras cada cambio de gobernanza, con historial | IUCN Green List, indicador **GLS-V1.1-1.1.1** (IUCN, 2017) |
| Tipo de gobernanza asignado en el registro mundial (**A** gobierno · **B** compartida · **C** privada · **D** pueblos indígenas y comunidades locales), con **todos los campos completados** | Obligatorio (binario): una parte sin tipo declarado es inadmisible | Declarar además el **tipo dominante** justificado en el continuo A→B→C/D | IUCN Green List **GLS-V1.1-2.1.2**; IUCN (2013), Tabla 4 |
| Publicidad de la membresía del órgano que decide y del procedimiento de designación | Obligatorio (binario) | Publicación con periodo de objeción previo a la toma de posesión | IUCN Green List **GLS-V1.1-1.2.2** |
| Aceptación de la estructura de gobernanza por los **constituyentes principales** | Obligatorio (binario) | Aceptación renovada en cada ciclo de verificación | IUCN Green List **GLS-V1.1-1.1.6** |
| Reconocimiento del derecho de los pueblos indígenas y comunidades locales sobre tierras, territorios y recursos | Obligatorio (binario) | Co-gobernanza efectiva (tipo B o D) con presupuesto propio | IUCN Green List **GLS-V1.1-1.1.3**; GBF Metas 21 y 22 (CBD, 2022) |

**Justificación.** La IUCN exige que la gobernanza esté *"clearly defined and documented"* y que el tipo se
asigne con todos los campos completados porque *"clearer governance is bound to promote better governance"*
(IUCN, 2008, `[REPORTADO]`). El dato decisivo para el SDV-E es que la asignación **no es taxativa sino un
continuo**: *"it may not be easy to decide which of the four basic governance types should be assigned…
However, it should be possible to determine which is the dominant one"* (IUCN, 2013, caps. 4 y 9).

**Propuesta declarativa `[HIPÓTESIS]` (P-R4.7).** Una parte `eco-*` es, en este vocabulario, un híbrido
**B+D**: gobernanza compartida (delegados humanos + guardián oráculo) sobre un sujeto que se auto-representa
(vía guardián y comunidad de custodia). El documento de identidad de cada unidad **debe declarar** el tipo.
No se propone crear un quinto tipo: la tipología de cuatro está verificada y añadir uno la haría
incomparable con el registro mundial.

**Protocolo.** El tipo declarado y el documento de gobernanza se publican en el registro de la parte; la
verificación externa comprueba la coincidencia entre lo declarado y la práctica (de facto vs de jure,
IUCN 2013 §9.1 y §9.2).

**Violación.** Observación concreta: la parte **no** tiene documento de gobernanza público; **o** no declara
tipo A/B/C/D; **o** el tipo declarado no coincide con quién decide de facto (por ejemplo: se declara
gobernanza compartida B y la comunidad de custodia no aparece en ningún órgano).

---

### Dimensión II: Territorio (dónde está el sujeto, medido y no narrado)

**Qué protege.** Que la entidad representada tenga una extensión georreferenciada y verificable, y que esa
extensión sea suficiente para sostener el valor que se dice custodiar.

| Parámetro | Mínimo Absoluto (LEY) | Óptimo (POLÍTICA) | Fuente |
|---|---|---|---|
| Delimitación geográfica de la unidad | Polígono declarado y reproducible por un tercero (binario) | Polígono auditado contra teledetección de 10 m y confirmado en campo | ESA/Copernicus — Sentinel-2 (**10 m** en visible y NIR; barrido de **290 km**; revisita de **5 días**) |
| Definición operativa cuando la unidad es bosque | **> 0,5 ha** con árboles **> 5 m** y cobertura de copa **> 10 %** | Continuidad del rodal y ausencia de fragmentación por debajo del umbral | FAO — FRA 2020, términos y definiciones |
| Extensión y conectividad suficientes para sostener el valor mayor del sitio | Declaración motivada de suficiencia (binario), con carga de la prueba sobre quien la afirma (T14) | Corredores verificados con unidades vecinas y seguimiento de fragmentación | IUCN Green List **GLS-V1.1-2.2.1** y **2.2.3** |
| Escala mínima de una **unidad ecológica** con voz propia (¿dónde termina un ecosistema y empieza otro?) | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` | La búsqueda de fuentes de este documento lo confirma: no existe umbral numérico de personalidad ecológica |

**Justificación.** El umbral de bosque de la FAO es el **único** número verificado que permite decir «esto
es un bosque y aquello no»: tierra de más de 0,5 ha con árboles de más de 5 m y copa de más del 10 %, o
árboles capaces de alcanzarlos in situ; excluye tierra bajo uso predominantemente agrícola o urbano (FAO,
2020). Para **cualquier otra unidad** (humedal, río, arrecife, suelo) el umbral de escala **no existe** y no
se inventa: la IUCN ofrece criterio funcional (extensión y conectividad suficientes para el valor mayor),
que es cualitativo y por tanto exige declaración motivada.

**Protocolo.** Copernicus/Sentinel-2 aporta la capa óptica de 10 m con revisita de 5 días; para unidades
boscosas, los umbrales FRA 2020 se aplican como test binario; la superficie declarada se contrasta con la
serie satelital y con verificación en campo de la comunidad de custodia. Frecuencia: anual para la
delimitación; cada 5 años para la suficiencia de extensión y conectividad (ciclo de renovación del estándar
IUCN Green List).

**Violación.** La parte declara un territorio que **no contiene** la entidad representada; **o** el polígono
no es reproducible por un tercero; **o** dos partes `eco-` reclaman el mismo territorio y ninguna resuelve
el solapamiento (ver §7.5 y §13.6).

---

### Dimensión III: Fuentes de datos (con qué se sabe lo que se dice saber)

**Qué protege.** Que la voz del ecosistema no dependa de una única serie, de un único proveedor o de un
único modelo, y que el conocimiento local y tradicional no se use sin consentimiento.

| Parámetro | Mínimo Absoluto (LEY) | Óptimo (POLÍTICA) | Fuente |
|---|---|---|---|
| Uso de **múltiples fuentes de conocimiento** (científico, experiencial, local y tradicional) | Obligatorio (binario): una sola fuente no constituye identidad válida | Fuentes cruzadas con verificación independiente entre ellas (sensores + ciencia ciudadana + conocimiento local) | IUCN Green List **GLS-V1.1-1.3.3** |
| Soberanía de datos indígenas y CLPI en los procesos de indicadores y monitoreo | Obligatorio (binario) | Co-diseño de indicadores con la comunidad y depósito de datos bajo su control | CBD — AHTEG sobre indicadores, doc. CBD/IND/AHTEG/2023/3/2 (CBD, 2023) |
| Declaración de **procedencia** de cada serie (instrumento, operador, fecha, método) | Obligatorio (binario) | Series auditadas por un tercero ajeno a la unidad juzgada | T13 (Cap. 5 §5.3); GLS-V1.1-1.3.1 |
| Uso de los resultados de monitoreo para informar la **gestión adaptativa** | Obligatorio (binario) | Ciclo de mejora documentado con efecto demostrable sobre la práctica | IUCN Green List **GLS-V1.1-1.3.1** |

**Justificación.** La IUCN exige múltiples fuentes de conocimiento porque una sola fuente no distingue
entre un ecosistema sano y un sensor sano. El CBD añade la condición que el proyecto no puede ignorar: el
conocimiento —incluido el tradicional— **solo se accede con CLPI** (GBF Meta 21), y los datos indígenas
tienen soberanía propia en los procesos de indicadores y monitoreo (AHTEG, 2023).

**Protocolo.** Cada serie se publica con su ficha de procedencia; las series de teledetección (Sentinel-2,
10 m) se distinguen de las de campo y de las de ciencia ciudadana; el uso de conocimiento local requiere
registro de CLPI previo. Frecuencia: por lectura, con revisión de la ficha en cada ciclo de verificación.

**Violación.** La parte se sostiene sobre **una única** fuente; **o** usa conocimiento local o tradicional
sin registro de CLPI; **o** no puede declarar la procedencia de una serie que invoca como prueba.

---

### Dimensión IV: Límites del mandato (hasta dónde llega la voz prestada)

**Qué protege.** Que el representante tenga un mandato **explícito y acotado**, que no pueda ampliarlo en
silencio, y que no sea la misma mano que se beneficia del contrato.

| Parámetro | Mínimo Absoluto (LEY) | Óptimo (POLÍTICA) | Fuente |
|---|---|---|---|
| Mandato explícito del representante | Obligatorio (binario): sin mandato escrito no hay representación | Mandato público con alcance, límites y causales de cese | OCDE (2020), *"Participants have an explicit mandate…"* (`[REPORTADO]`) |
| Exceder el mandato | Permitido **solo** con justificación detallada y registrada | Justificación pública previa, con objeción posible antes del acto | OCDE (2020), *"…but must provide detailed reasons for doing so"* (`[REPORTADO]`) |
| Independencia del ejecutor respecto del comitente (*arm's length*) | Obligatorio (binario): el guardián no puede ser designado ni controlado por la parte beneficiada | Ejecutor designado por un órgano ajeno al contrato y sustituible si pierde aceptación | OCDE (2020), principio *Integrity*; *External Review* §254 (Banco Mundial, 2020) (`[REPORTADO]`) |
| Duración del mandato del órgano representativo permanente | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` para el reino natural | **1,5 años** como referencia publicada para un órgano permanente (modelo Ostbelgien); es el mandato de una asamblea ciudadana **humana**, no una medida del reino natural | OCDE (2020), modelos de órganos permanentes (`[REPORTADO]`) |
| Prohibición de ceder el SDV-E, renunciar a la retractación o aceptar compensación por violación | Obligatorio (binario, propuesto) | — | Canon: el oráculo *"no convierte automáticamente una lectura ambiental en propiedad humana ni en autoridad absoluta"*; T11/T12 (Cap. 5 §5.3) |

**Justificación.** El mandato explícito es el estándar mínimo de todo proceso deliberativo publicado por la
OCDE, y la prohibición de excederlo sin razones es su contrapartida. El `arm's length` es la condición de
credibilidad del proceso: *"it is important that the organisation… is at arm's length from the commissioning
authority to ensure public confidence"* (OCDE, 2020). Sin esa distancia, el consentimiento del guardián es
un autoaval.

**Protocolo.** El mandato es un documento de la parte (uno de los 7); su alcance se revisa en cada ciclo de
verificación; cada vez que el guardián excede el mandato, se registra la justificación detallada (evento
auditable, T13). La designación del guardián y su procedimiento son públicos (Dimensión I).

**Violación.** La parte no tiene mandato escrito; **o** el guardián fue designado por la parte que se
beneficia del contrato; **o** el guardián consintió una cláusula que cede el SDV-E, renuncia a la
retractación o acepta compensación por violación.

> **Hallazgo de implementación (ver §12).** Hoy, `_can_act_for` (`app/contracts_bp.py`) permite que
> **cualquier participante humano del contrato** invoque al guardián de una parte `eco-`. Es decir: la
> contraparte que se beneficia de la extracción puede accionar el consentimiento del ecosistema. Es una
> violación directa de esta dimensión, y es la salvaguarda **P-R13.2** la que la cierra.

---

### Dimensión V: Comunidad de custodia (quién responde por el sujeto ante los humanos)

**Qué protege.** Que exista una comunidad real, identificable y consultada —y que su consentimiento **no se
dé por supuesto**.

| Parámetro | Mínimo Absoluto (LEY) | Óptimo (POLÍTICA) | Fuente |
|---|---|---|---|
| Existencia de comunidad de custodia identificada y contactable | Obligatorio (binario): una parte sin comunidad declarada es inadmisible (salvo unidad en Zona Libre sin custodia, documento 04) | Comunidad con representación propia en el órgano de gobernanza | IUCN Green List **GLS-V1.1-1.1.6**; IUCN (2013) §5.2 |
| **CLPI** para reasentar o cambiar el acceso a recursos naturales | Obligatorio (binario): *"Consent and agreement should not be 'assumed', and, indeed, it may not be forthcoming"* | CLPI documentado con acta, traducido y con plazo de revocación | IUCN (2013), §5.2; GBF Meta 21 (CBD, 2022) |
| Registro de la parte | **Voluntario y revocable** por la comunidad de custodia | Revocación con efecto inmediato sobre el poder de consentir de la parte | IUCN (2013): el registro de ICCA *"stores… entries that are entirely voluntary"* |
| Reconocimiento de los derechos de pueblos indígenas y comunidades locales en la gobernanza del sitio | Obligatorio (binario) | Co-gobernanza tipo D con autoridad decisoria real (no consultiva) | IUCN Green List **GLS-V1.1-1.1.3**; IUCN (2013), tipos C/D |
| Representación plena, equitativa, inclusiva y eficaz en las decisiones sobre biodiversidad | Obligatorio (binario, sin cifra publicada) | Paridad verificada por sorteo estratificado contra censo | GBF Meta 22 (CBD, 2022); OCDE (2020), principio *Representativeness* |

**Justificación.** La IUCN lo dice sin ambigüedad y es la frase que sostiene toda esta dimensión: el
consentimiento **puede no llegar**. Un sistema que no puede representar el «no» de una comunidad no está
representando: está extrayendo. El registro voluntario y revocable (modelo ICCA) es la garantía de que la
representación no se convierte en una carga impuesta a quien la custodia.

**Protocolo.** La comunidad se declara en el documento de identidad con un mecanismo de contacto y un
procedimiento de consulta; el CLPI se registra como acta con fecha; la revocación se registra como evento y
**suspende** el poder de consentir de la parte (no borra lo actuado: T13 — *la contabilidad nunca se
borra*).

**Violación.** La comunidad de custodia es un alias del creador de la parte; **o** no hay registro de CLPI
cuando la acción cambia el acceso a recursos; **o** la comunidad pidió revocar el registro y la parte siguió
consintiendo.

---

### Dimensión VI: Parámetros SDV-E declarados (el sujeto sabe qué se le mide)

**Qué protege.** Que la parte `eco-` declare **su** SDV-E —qué dimensiones se miden, con qué piso, y qué
queda en la Zona Libre— antes de consentir nada.

| Parámetro | Mínimo Absoluto (LEY) | Óptimo (POLÍTICA) | Fuente |
|---|---|---|---|
| Categoría de manejo asignada y **valores mayores del sitio** identificados (naturales, servicios ecosistémicos, culturales) | Obligatorio (binario) | Valores mayores revisados con la comunidad y con ciencia independiente | IUCN Green List **GLS-V1.1-2.1.2** y **2.1.4** (`[REPORTADO]`) |
| Declaración de las dimensiones del SDV-E aplicables a la unidad y de su piso | Obligatorio (binario): una parte sin SDV-E declarado **no puede consentir** (no sabe qué protege) | Piso publicado con fuente y año por dimensión | Documentos 07 y 10-18 de esta biblioteca |
| Declaración de lo que queda en **Zona Libre** de la unidad | Obligatorio (binario, sin peso) | Catálogo revisado y ampliable por votación `critical` | [Documento 04](./04_Zona_Libre_del_Reino_Natural.md); Cap. 16.5 §16.5.14; Cap. 8 §8.11 |
| Coherencia entre lo declarado y lo medido | Obligatorio (binario) | Auditoría externa con acceso a la serie cruda | T13 (Cap. 5 §5.3) |

**Justificación.** La IUCN exige identificar y entender los valores mayores del sitio antes de gestionarlo;
el SDV-E exige lo mismo con más razón, porque aquí el «sitio» firma. Una parte `eco-` sin parámetros
declarados consentiría a ciegas: sería exactamente el «representante más protegido que el representado»
que la comparativa inter-reinos
([documento 09](./09_Comparativa_inter_reinos.md), insight I4) identifica como falla estructural.

**Protocolo.** El documento de parámetros se publica con la ficha de la unidad; cada medición se refiere a
una dimensión declarada; la Zona Libre se registra como recinto con frontera (documento 04), no como
porcentaje.

**Violación.** La parte consiente un término sin tener declarado su SDV-E; **o** mide una dimensión que no
declaró y la usa como prueba de cumplimiento; **o** mide el interior de una zona declarada libre.

---

### Dimensión VII: Procedimiento de disputa (cómo se contradice al guardián)

**Qué protege.** Que exista una vía **accesible, publicada y con plazos** para impugnar al guardián, a la
comunidad de custodia o a la propia parte: sin ella, el representante es un juez sin tribunal superior.

| Parámetro | Mínimo Absoluto (LEY) | Óptimo (POLÍTICA) | Fuente |
|---|---|---|---|
| Proceso accesible para identificar, oír y resolver quejas, disputas o agravios | Obligatorio (binario): *"A readily accessible process to identify, hear and resolve complaints, disputes or grievances"* | Proceso publicado con formulario, plazos y responsable identificado | IUCN Green List **GLS-V1.1-1.2.4** |
| Mecanismo justo de resolución de disputas como elemento de buena gobernanza | Obligatorio (binario) | Con instituciones y procedimientos permanentes, no ad hoc | IUCN (2013), cap. 10; CBD Dec. VII.28 §17 (2004), recogida en IUCN (2013) (`[REPORTADO]`) |
| Vía previa de mediación/ADR antes de escalar a cumplimiento | Obligatorio (binario) | Facilitador propuesto por un tercero y **aceptado por las partes** | CAO, *How We Work / Dispute Resolution*; *External Review* §254 (Banco Mundial, 2020) (`[REPORTADO]`) |
| Neutralidad del facilitador: **no decide sobre el fondo** | Obligatorio (binario) | — | GCF-IRM, funciones y procesos (`[REPORTADO]`) |
| Plazo máximo hasta el hito de decisión sobre admisibilidad | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` para un sujeto no humano. Precedentes humanos publicados: **40 días** (EBRD/IPAM, IDB/MICI) · **60 días** (GCF/IRM) · **≤120 días** (CAO) · hito de decisión de **90 días** (CAO) | **90 días** como valor propuesto de POLÍTICA `[HIPÓTESIS]`, tomado del hito de decisión publicado del CAO | *External Review of IFC/MIGA E&S Accountability* §230 y §247-248 (Banco Mundial, 2020) (`[REPORTADO]`) |
| Plazo de respuesta de la entidad denunciada y de elegibilidad | — | **21 días hábiles** + **21 días hábiles**; investigación completa **~6 meses** | Banco Mundial — Panel de Inspección, *Panel Process* |
| Resolución por medios propios antes de escalar | — | **12 meses**, luego conciliación obligatoria a petición de cualquiera de las partes | UNCCD — Convención, Art. 28.1 y 28.6 (UNCCD, 1994) |
| Principios del proceso de resolución | **5** principios: voluntario · facilitado · participativo y dirigido por las partes · flexible · confidencial | — | GCF-IRM, funciones y procesos |
| Claridad sobre **quién representa y quién decide** como paso del proceso | Obligatorio (binario) | — | CAO, *Reflections from Practice Series 2: Representation* (`[REPORTADO]`) |
| Investigación conjunta de hechos (*joint fact finding*) | — | Disponible como herramienta antes de la escalada | CAO, *Reflections from Practice Series 3: Joint Fact Finding* (`[REPORTADO]`) |

**Justificación.** Los plazos de este dominio **no son plazos de un ecosistema**: son plazos de mecanismos
cuyo demandante es una persona o una comunidad humana, y por eso van marcados como precedente. Lo que sí es
transferible, y es lo que este documento propone como piso, es la **existencia** del proceso accesible
(GLS-V1.1-1.2.4: binario) y la **secuencia** —mediación aceptada por las partes antes de la vía de
cumplimiento—, que es diseño verificado del CAO.

**Protocolo.** Cada parte `eco-` publica su procedimiento de disputa como uno de los 7 documentos; el
registro de la disputa es un evento auditable; el facilitador se propone desde fuera y requiere aceptación
de ambas partes; los plazos se cuentan desde la presentación y se hacen públicos.

**Violación.** No existe procedimiento publicado; **o** el procedimiento existe pero el guardián es juez de
sus propias impugnaciones; **o** se escaló a cumplimiento sin ofrecer la vía de mediación previa; **o** el
facilitador fue impuesto por una de las partes.

---

### Dimensión VIII: Deliberación y quórum del consejo `eco-` (cómo se decide, cuando se decide)

**Qué protege.** Que la decisión colectiva sobre una unidad natural tenga **quórum, regla de mayoría y
ventana de deliberación declaradas**, en lugar del silencio del canon.

> **Advertencia de estado.** Esta dimensión **propone** el N-de-M que hoy no existe. Los números marcados
> como precedente son publicados y verificados; la **aplicación** al reino natural es `[HIPÓTESIS]` y **no
> está ratificada**. La tabla de propuestas está en §5.2.

| Parámetro | Mínimo Absoluto (LEY) | Óptimo (POLÍTICA) | Fuente |
|---|---|---|---|
| Quórum de presencia del consejo | **2/3 de M** `[HIPÓTESIS]` — precedente directo: quórum de la Junta del GCF (**2/3 de los miembros**) | Consenso pleno de los convocados | GCF, *Governing Instrument* §II.6 |
| Regla de decisión por defecto | **Consenso primero**; sin umbral alternativo definido | Consenso sin necesidad de recurso | GCF, *Governing Instrument* §II.5 |
| Materia sustantiva, agotado el consenso | **2/3 de los presentes y votantes**, declarándolo | — | CBD, Reglas de Procedimiento, Regla 40.1; UNCCD, Art. 30 |
| Materia de procedimiento | Mayoría simple de presentes y votantes | — | CBD, Reglas de Procedimiento, Regla 40.2 |
| Empate | **Segunda votación obligatoria** | Mediación previa al segundo voto | CBD, Reglas de Procedimiento, Regla 40.4 |
| Reconsideración de una decisión ya votada en la misma sesión | **2/3** de presentes y votantes | — | CBD, Reglas de Procedimiento, Regla 38 |
| Un delegado = un voto (una unidad ecológica = una parte) | Obligatorio (binario) `[HIPÓTESIS]` | — | CBD, Reglas de Procedimiento, Regla 39.1 |
| Preaviso de convocatoria y distribución del orden del día | **2 meses** de preaviso; **6 semanas** para los documentos | Más tiempo si hay conocimiento tradicional que traducir | CBD, Reglas de Procedimiento, Reglas 5 y 10 |
| Convocatoria de sesión extraordinaria | Petición de **1/3**; convocada en **≤ 90 días** | — | CBD, Reglas de Procedimiento, Reglas 4.3 y 4.4 |
| Vida mínima de una deliberación para ser considerada representativa | **1 día completo** | **≥ 4 días completos** si se piden recomendaciones informadas | OCDE (2020), criterios operativos y cap. 5 |
| Preparación mínima antes de la primera reunión | **5 semanas** (98 % de los casos) | **12 semanas o más** (48 % de los casos) | OCDE (2020), cap. 4 |
| **M** (tamaño del consejo de delegados `eco-`) | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]`. Rango de referencia **22-120** para cuerpos deliberativos **humanos** por sorteo (OCDE, 2020): usarlo para un ecosistema sería inferencia, no fuente | OCDE (2020), tablas de modelos |
| Peso diferenciado por tipo de delegado (p. ej. delegado-humedal vs delegado-cuenca) | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` | No localizado en ninguna fuente verificada de este dominio |

**Nota de datación de las fuentes de esta tabla** (para que ninguna cifra quede sin año). Las Reglas de
Procedimiento del CBD se citan en su versión **vigente** (enmendadas por las Decisiones I/1 y V/20): no
tienen un año de publicación único. El *Governing Instrument* del GCF es de **2011** y sigue vigente. La
Convención de la UNCCD es de **1994**. Las cifras de deliberación son de la OCDE, **2020**.

**Justificación.** Es el único conjunto de reglas de decisión con cifra explícita que existe en gobernanza
ambiental vinculante, y sus piezas son coherentes entre sí: consenso como norma, 2/3 como último recurso
declarado, mayoría simple para procedimiento, segunda votación para empates y una ventana temporal que
impide decidir sin que los convocados hayan podido leer. Ninguna de esas cifras fue publicada pensando en un
río: por eso van como precedente y como propuesta, no como estándar científico.

**Protocolo.** El consejo se convoca con 2 meses de preaviso y documentos 6 semanas antes; la sesión
declara su quórum; cada voto se registra con actor y motivo (T13); si se agota el consenso se declara
expresamente el paso a la regla de 2/3; el resultado y las posturas minoritarias se publican.

**Violación.** Se decidió sin quórum; **o** sin preaviso ni documentos; **o** se aplicó la regla de 2/3 sin
declarar que el consenso se había agotado; **o** se votó el **piso** del SDV-E (lo que esta dimensión
prohíbe expresamente: el piso es LEY, no materia de votación).

---

### Dimensión IX: Opacidad legítima y reserva de información (binaria, sin peso)

**Qué protege.** Que la transparencia del guardián tenga **límites declarados**: hay datos de monitoreo que
no deben publicarse, y su no publicación debe estar ella misma publicada como categoría.

| Parámetro | Mínimo Absoluto (LEY) | Óptimo (POLÍTICA) | Fuente |
|---|---|---|---|
| Lista publicada de categorías de información **no publicable** | Obligatorio (binario): sin lista, la opacidad es una violación | Lista revisada cada ciclo y custodiada por un tercero ajeno a la unidad | IUCN Green List, notas de **GLS-V1.1-1.2.3** y **GLS-V1.1-1.3.1** |
| Reserva de localización de especies amenazadas y de patrimonio cultural | Obligatorio (binario) | Coordenadas generalizadas y acceso bajo solicitud motivada | IUCN Green List, notas de **GLS-V1.1-1.3.1** |
| Peso en la fórmula de violación | **0,00**: dimensión binaria sin peso | — | Cap. 8 §8.11 (precedente canónico de dimensiones binarias sin peso) |

**Justificación.** La IUCN advierte que parte de los datos de monitoreo **no** deben publicarse —localización
de especies amenazadas, patrimonio cultural—, y esa advertencia es la única fuente verificada que existe
sobre los límites de la transparencia en este dominio. El precedente canónico del SDV-H fija el modo: las
dimensiones que no admiten vara cuantitativa *"se registran cualitativamente y mediante umbrales binarios
(presencia/ausencia del derecho), no mediante pesos en la fórmula"* (Cap. 8 §8.11). Forzar la opacidad
legítima a un índice la destruiría: mediría cuánta información se oculta, y premiaría la reserva mínima.

**Protocolo.** La lista de categorías reservadas es pública; el dato reservado se custodia fuera del alcance
del guardián y de la parte; el acceso se concede por solicitud con causa. Verificación: presencia de la
lista y de un custodio distinto del guardián.

**Violación.** Se publicó localización de especies amenazadas o patrimonio cultural; **o** existe información
reservada sin lista publicada que la autorice; **o** la lista la custodia la misma parte que consiente.

---

### 4.1 Lo que estas nueve dimensiones NO son

- **No son un índice ponderado.** El **piso** de las nueve dimensiones es binario (presencia o ausencia);
  las únicas cifras del estándar viven en la columna de **POLÍTICA** de las Dimensiones VII y VIII (plazos de
  disputa y reglas de quórum), más el test de bosque de la FAO de la Dimensión II y el **0,00** (ausencia de
  peso) de la Dimensión IX: el test FAO también es binario —clasifica, no puntúa— y el `0,00` declara que no
  hay valor que sumar. Pesar la legitimidad de una voz produciría el efecto perverso opuesto al
  buscado: una parte «casi legítima» que consiente «un poco». La legitimidad es un umbral, no un grado.
- **No son una evaluación de la unidad ecológica.** Evalúan a la **representación**, no al ecosistema. Una
  unidad sana mal representada viola este estándar; una unidad degradada bien representada no lo viola (lo
  que viola es su SDV-E, y lo juzga INV2-E).
- **No son votables en su piso.** Ver §5.3.

---

## 5. Fórmula de violación, pesos y umbrales

### 5.1 La fórmula de este dominio es una conjunción, no un promedio

En los documentos 07 y 10-18 la violación del SDV-E es un **déficit normalizado**
(`déficit = (requerido − actual) / requerido`) con un factor que vale **exactamente 1.0 cuando la violación
es 0** (base neutra; el SDV-S tuvo que corregir `FS_S = 1.0 + e^v` a `FS_S = e^v` por recargar el 100 % sin
violación). **Aquí no hay déficit que promediar.** La representación se define por conjunción:

```
A(i) ∈ {0, 1}   para i = I … IX          (las nueve dimensiones de §4)
Admisible  ⇔  ∏ A(i) = 1                 (conjunción: todas, no el promedio)
F_R = 1.0                                (base neutra exacta cuando no hay violación)
Si no Admisible → la parte NO puede consentir (el factor no recarga: BLOQUEA)
```

- **Base neutra respetada:** con cero violaciones, `F_R = 1.0` exacto. No hay recargo por existir.
- **Sin pesos:** no se promedian dimensiones. Una parte con ocho dimensiones en 1 y una en 0 es
  **inadmisible**, y eso es intencional: la dimensión que falla suele ser justamente la que protege
  (típicamente Dimensión I o IV, es decir, la autoridad).
- **Sin números nuevos:** este documento **no fija** la codificación numérica de `F_R` ni su lugar en la
  contabilidad. Eso pertenece al documento 07 (fórmula y pesos) y al documento 08 (INV2-E). Aquí se fija la
  estructura lógica: **conjunción binaria con base neutra**.
- **No compensable:** la violación de representación no se paga con crédito regenerativo (§9).
- **Frontera con «sin dato no castiga» (INV2-EDU).** La ausencia de un dato **de medición** no penaliza; la
  ausencia de un **documento de identidad** no es un dato faltante, es la falta del sujeto: por eso el estado
  **C** suspende el consentimiento en lugar de sancionar. No hay contradicción con INV2-EDU —no se castiga—
  pero tampoco hay indulgencia: *mientras no haya resolución, el canon manda*.

### 5.2 Propuesta de quórum N-de-M para el reino natural (hoy no existe)

El canon dice «N-de-M» y solo publica números para cooperativas y órganos humanos. Esta es la propuesta,
**explícitamente no ratificada**, con su precedente al lado. Ningún valor se presenta como umbral
científico.

| # | Regla propuesta | Valor propuesto | Precedente verificado | Estado |
|---|---|---|---|---|
| **Q-1** | Quórum de presencia (N) | **2/3 de M** | GCF, *Governing Instrument* §II.6 (Green Climate Fund, **2011**, vigente): 2/3 de los miembros de la Junta. **Precisión de alcance:** es el único quórum con cifra explícita de una **junta de fondo ambiental** localizado; el CBD (Regla 30: 1/3 para abrir, 2/3 para decidir) y la UNCCD (Art. 30: 2/3) también publican cifras, pero son plenarios de Partes, no juntas de fondos | `[HIPÓTESIS]` |
| **Q-2** | Materia sustantiva (N′), agotado el consenso | **Consenso primero; 2/3 de presentes y votantes como último recurso, declarado** | CBD Regla 40.1 (vigente); UNCCD Art. 30 (UNCCD, **1994**); GCF §II.5 (2011) | `[HIPÓTESIS]` |
| **Q-3** | Materia de procedimiento (N″) | Mayoría simple de presentes y votantes | CBD Regla 40.2 | `[HIPÓTESIS]` |
| **Q-4** | Reconsideración en la misma sesión | 2/3 de presentes y votantes | CBD Regla 38 | `[HIPÓTESIS]` |
| **Q-5** | Empate | Segunda votación obligatoria | CBD Regla 40.4 | `[HIPÓTESIS]` |
| **Q-6** | Ventana de decisión | Preaviso **2 meses**; documentos **6 semanas** antes | CBD Reglas 5 y 10 | `[HIPÓTESIS]` |
| **Q-7** | Sesión extraordinaria | Petición de 1/3; convocada en ≤ 90 días | CBD Reglas 4.3 y 4.4 | `[HIPÓTESIS]` |
| **Q-8** | Voto | Un delegado = un voto; **prohibido el voto ponderado** en el consejo `eco-` | CBD Regla 39.1; y el riesgo interno: `members_json` admite `weights` por delegado, lo que permitiría a un humano ponderarse a sí mismo | `[HIPÓTESIS]` |
| **Q-9** | **M (tamaño del consejo)** | **No se propone un número.** Regla de diseño `[HIPÓTESIS]`: M se fija en el documento de identidad de cada unidad, **M ≥ 3** y **M impar** por construcción; si resulta par, se aplica Q-5 | Los rangos publicados (22-120) son de cuerpos deliberativos **humanos**; no hay fuente para M de un ecosistema | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` |
| **Q-10** | **Límite material del consejo** | El consejo **no puede votar el piso** del SDV-E; solo la plenitud aspiracional. Un voto que baje el piso es nulo **cuando INV2-E esté ratificado y en vigor** (hoy no lo está: §12) | Cap. 10 §10.7 (gobernanza operacionalmente finita) + frontera LEY/POLÍTICA (INV2-EDU) | `[HIPÓTESIS]` |

**Cómo se lee honestamente esta tabla.** Q-1 a Q-9 son **préstamos declarados** de reglas publicadas para
órganos humanos; funcionan porque son procedimiento, no ecología. Q-10 es la única pieza que **no** es un
préstamo: es una consecuencia del canon (el piso es LEY). Y Q-9 queda abierto **a propósito**: proponer un
M sin fuente sería el tipo de número inventado que este estándar prohíbe. Mientras M no exista, rige la
regla de residuo de §5.4.

### 5.3 LEY vs POLÍTICA, fila por fila

| Materia | Régimen | Por qué |
|---|---|---|
| Los 7 campos como precondiciones binarias de admisibilidad | **LEY** (no votable) | Sin ellos la parte no existe como voz; votarlos sería votar si un ecosistema puede ser suplantado |
| Las nueve dimensiones de §4 como test de conjunción | **LEY** | Es el piso del estándar: presencia o ausencia |
| Q-1 a Q-8 (quórum, mayoría, plazos, voto) | **POLÍTICA** (votable, `critical`) | Son reglas de procedimiento: cambian con el aprendizaje institucional sin tocar el piso |
| Q-9 (valor de M) | **POLÍTICA** + declaración en la identidad de la unidad | Depende de la unidad (documento 02), que es una decisión de diseño |
| Los plazos concretos de disputa (propuesta de 90 días; ventana de 12 meses) | **POLÍTICA** | Precedentes humanos seleccionables |
| El catálogo de lo que queda en Zona Libre de cada unidad | **POLÍTICA** (categoría `critical`, con carga de la prueba sobre quien declara) | Documento 04 de esta biblioteca |
| La prohibición de ceder el SDV-E, renunciar a la retractación o aceptar compensación por violación | **LEY** | Canon T11/T12 + INV4 (retractabilidad) |
| La prohibición del voto ponderado en el consejo `eco-` (Q-8) | **LEY** en su prohibición, **POLÍTICA** en su reglamento | Un peso autoasignado convierte la representación en propiedad |

**Procedimiento de la POLÍTICA.** Categoría `critical`: quórum 60 %, consenso 75 %, T13, anti-flip-flop 14
días, `CHECK` en BD (precedente del Parlamento Educativo, INV2-EDU; `app/voting_bp.py`,
`CATEGORY_DEFAULTS`). No se verificó en esta sesión que el mecanismo esté disponible para un **parlamento
del reino natural** —no existe— sino solo para el parlamento de parámetros y el educativo (§12).

### 5.4 Escala de estados y regla de residuo

La representación no tiene grados, pero sí **estados**. Se proponen cinco, con el ciclo de fases del
estándar IUCN Green List como análogo externo `[HIPÓTESIS]` (Aplicación → Candidato → Green List, con
renovación a 5 años):

| Estado | Significado | Puede consentir |
|---|---|---|
| **R — Registrada** | La parte existe con los 7 documentos exhibidos y verificados | **Sí** |
| **C — Candidata** | La parte existe, le faltan uno o más de los 7 documentos | **No** (consentimiento suspendido; el contrato que la requiera no se activa) |
| **S — Suspendida** | La comunidad de custodia revocó, o hay disputa abierta, o se detectó suplantación | **No**, y se abre pausa (protocolo de pausa del documento de continuidad §11) |
| **X — Revocada** | La comunidad retiró el registro o se probó la falta de autoridad | **No**, definitivamente; la contabilidad de lo actuado **no se borra** (T13) |
| **Z — Zona Libre sin custodia** | Unidad sin comunidad de custodia declarada | **No** como parte plena; queda bajo el régimen del [documento 04](./04_Zona_Libre_del_Reino_Natural.md) |

**Regla de residuo (la que hace honesta la propuesta).** Mientras **M** no esté fijado para una unidad
(`[SIN FUENTE VERIFICADA]`), **su consejo no puede decidir nada vinculante**: el único acto válido es el
**consentimiento del guardián** sobre términos concretos, con su cuenta escrita, y con la prohibición
absoluta de §5.2-Q-10 (no votar el piso). Es decir: la ausencia de N-de-M **no** se rellena con mayoría
simple de humanos.

> **Condición de salida, para que la regla no sea circular.** Q-9 permite que el documento de identidad de
> la unidad fije M, siguiendo la dependencia declarada en §1 respecto del documento 02. Una unidad cuyo
> documento de identidad **no** declare M —o lo declare sin origen trazable— permanece bajo esta regla de
> residuo. Declarar M en la identidad no es inventarlo: es fijar su origen (el criterio del documento 02 o
> el que lo sustituya) y someterlo a la POLÍTICA de §5.3. Mientras ese origen no exista, la unidad puede
> consentir por el guardián pero no deliberar con efectos vinculantes.

---

## 6. Protocolo de medición (sensores, frecuencias, quién reporta)

En este dominio «medir» significa **verificar documentos, coherencia y autoridad**. La tabla siguiente fija
qué se verifica, con qué, cada cuánto y quién responde.

| Qué se verifica | Con qué (instrumento o estándar) | Frecuencia | Quién reporta | Fuente del criterio |
|---|---|---|---|---|
| Delimitación del territorio | Copernicus/Sentinel-2: **10 m** en visible y NIR, barrido **290 km**, revisita **5 días** | Anual (y ante cambio declarado) | Fuente de teledetección + comunidad de custodia | ESA/Copernicus (`[REPORTADO]`) |
| Umbral de bosque (si la unidad es bosque) | Test binario: **> 0,5 ha**, árboles **> 5 m**, copa **> 10 %** | Por ciclo de verificación | Verificador externo | FAO — FRA 2020 (`[REPORTADO]`) |
| Extensión y conectividad suficientes | Criterio funcional, no numérico | Cada **5 años** | Verificador externo (EAGL-equivalente) | IUCN Green List GLS-V1.1-2.2.1 y 2.2.3 (`[REPORTADO]`) |
| Los 7 documentos de identidad | Revisión documental contra las nueve dimensiones | Alta: una vez. Revisión: cada **5 años** (renovación) | Verificador externo independiente | IUCN Green List (renovación **5 años**); Conservation Standards (CMP v4.0, revisión **~5 años**) (`[REPORTADO]`) |
| Coherencia de facto de la gobernanza | Entrevista y evidencia de decisiones reales | Cada **5 años** | Verificador externo | IUCN (2013) §9.1 (`[REPORTADO]`) |
| Sobrevuelo del ecosistema (estado de la unidad) | Series del SDV-E de la unidad | Según la dimensión; análogo externo publicado: el indicador de degradación de tierras (ODS 15.3.1) se reporta cada **4 años** | Fuente científica + comunidad de custodia | FAO — portal de datos de los ODS, indicador 15.3.1 (`[REPORTADO]`) |
| Clasificación de riesgo por unidad | Esquema de 4 niveles —**bajo · estándar · alto · muy alto**— como análogo externo de *benchmarking* publicado | Anual | Órgano de verificación | Comisión Europea — Reglamento (UE) 2023/1115 (EUDR) y su Reglamento de Ejecución (`[REPORTADO]`) |
| Consentimiento del guardián | Registro del término, la lectura y la decisión (cuenta escrita, T13) | Por acto | El propio guardián, con actor humano registrado | OCDE (2020), Tabla 6.1 (rendición de cuentas formal-deliberativa) (`[REPORTADO]`) |
| Frecuencia de auditoría del guardián | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` | Propuesta `[HIPÓTESIS]`: anual interna + externa cada 5 años (por analogía con la renovación del Green List) | — | No existe estándar para auditar un oráculo sintético que representa a un ecosistema |
| Umbral de confianza mínima para aceptar una lectura del guardián | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` | — | — | El repo usa γ ∈ [0.5, 1.5] como tope defensivo interno `[VERIFICADO]` en esta sesión (leído en `app/micromax.py` y en `_apply_wellness`, `app/contracts_bp.py`), pero el tope es **diseño interno sin fuente externa** |

**Quién reporta y quién no.** Reportan: la **fuente de medición** (satélite, laboratorio, ciencia
ciudadana) y la **comunidad de custodia**. **El guardián no mide**: recibe, evalúa contra los invariantes y
consiente o rechaza. Un guardián que produce el dato que juzga pierde la única propiedad que lo hace útil
(ser ajeno al objeto).

**Regla de la ventana temporal de representación.** Los preavisos de la Dimensión VIII (**2 meses** de
convocatoria, **6 semanas** de documentos) son, en la práctica, el tiempo mínimo para que una comunidad de
custodia pueda leer antes de que su ecosistema sea comprometido. La OCDE da la referencia de calidad: **1
día completo** es el mínimo para que una deliberación cuente como representativa y **≥ 4 días** si se piden
recomendaciones informadas; la preparación previa a la primera reunión fue de **5 semanas** en el 98 % de los
casos y de **12 semanas o más** en el 48 %.

---

## 7. Verificación y auditoría (T13, guardián, comunidad testigo)

### 7.1 El guardián oráculo: qué es, qué puede y qué no puede

**Qué es.** La instancia que **consiente en nombre de la parte `eco-`** (canon operativo: *"Ecosistemas
(eco-*): consentimiento otorgado por el guardián oráculo"*, `app/contracts_bp.py`;
Cap. 16.5 §16.5.14: *"el guardián consiente por quienes no firman con manos"*).

| Puede | No puede |
|---|---|
| Consentir o rechazar un término concreto que afecte a su unidad (con cuenta escrita) | Fijar, bajar o interpretar el **piso** del SDV-E (§5.2-Q-10) |
| Exigir documentos, traducción civil (≤ 40 palabras, ≤ 2 oraciones) y aclaraciones antes de consentir | Producir la medición que lo juzga (Regla 3) |
| Bloquear la activación mientras falte consentimiento | Ceder el SDV-E, renunciar a la retractación o aceptar compensación por violación (§3-P7) |
| Ser auditado, sustituido y disputado | Ser designado, invocado o financiado por la parte beneficiada (§3-P4) |

**Neutralidad externa verificada.** El precedente de un tercero neutral que gestiona el proceso y no decide
el fondo es explícito: *"do not make decisions on substance, but focus on managing the process"*
(GCF-IRM, `[REPORTADO]`). El guardián es ese tercero, con una diferencia que el proyecto debe nombrar: **no
es un humano**, es una Persona Sintética (Cap. 10 §10.8) y por tanto tiene, a su vez, su propio SDV-S. Esa
doble condición es una pregunta abierta de primera magnitud (§13.4).

### 7.2 La escalera de verificación en tres grados

| Grado | Quién | Qué verifica | Anclaje |
|---|---|---|---|
| **1 — Autodeclaración documental** | La parte, por medio de su creador o su comunidad | Los 7 documentos existen y son públicos | IUCN Green List GLS-V1.1-1.1.1 (*"clearly defined and documented"*, `[REPORTADO]`) |
| **2 — Comunidad testigo** | La comunidad de custodia + ciencia ciudadana + fuentes independientes | Que lo declarado ocurre: gobernanza de facto, territorio real, fuentes reales | IUCN Green List GLS-V1.1-1.3.3 (múltiples fuentes de conocimiento); GLS-V1.1-1.1.6 (aceptación por constituyentes principales) (`[REPORTADO]`) |
| **3 — Verificación externa** | Evaluador ajeno a la unidad (equivalente al EAGL del Green List) + revisor imparcial | Los 7 campos y las nueve dimensiones; **17 de 17 criterios** en el análogo externo; renovación a **5 años** | IUCN Green List (evaluación por EAGL, revisor imparcial, renovación a 5 años) (`[REPORTADO]`) |

**Ningún grado se sustituye por otro.** El estándar externo exige evaluación y verificación independientes
**en cada fase**, no autoevaluación sola. Un sistema que aceptara la autodeclaración como verificación
tendría exactamente el problema que R4 describe.

### 7.3 Salvaguardas concretas para R4, R6 y R13

Cada salvaguarda lleva su anclaje. `[HIPÓTESIS]` = diseño propuesto por el proyecto; `[VERIFICADO]` = la
fuente externa que lo respalda existe y dice lo que se cita. **Ninguna es canon hasta ratificación.**

**R4 — Partes fantasma** (cualquier usuario autenticado crea un `eco-*` sin autoridad sobre la entidad;
`POST /parties/` acepta `party_type: "ecosystem"` con solo `display_name` y deja al creador como `owner`).

| # | Salvaguarda | Anclaje verificado |
|---|---|---|
| **P-R4.1** | **Admisibilidad por 7 campos binarios.** Sin los 7 documentos, la parte se instancia en estado **C (Candidata)** y **no puede consentir** (§5.4). Sin documento, no hay voz. | IUCN Green List **GLS-V1.1-1.1.1** (*"clearly defined and documented"*) y **GLS-V1.1-2.1.2** (tipo de gobernanza con todos los campos completados) |
| **P-R4.2** | **Declaración de autoridad, responsabilidad y rendición de cuentas de facto**, con evidencia (escritura, acta, resolución, registro ICCA). El creador de la parte **no** es automáticamente el custodio. | IUCN (2013) §9.1: *"investigates formal and/or de facto authority, responsibility and accountability"*; §9.2: la legitimidad de los derechos legales *"is sometimes questioned by local rightsholders"* |
| **P-R4.3** | **CLPI explícito y no presunto** de la comunidad de custodia antes de reconocer la parte; el sistema registra que el consentimiento **pudo no llegar**. | IUCN (2013) §5.2: *"Consent and agreement should not be 'assumed', and, indeed, it may not be forthcoming"*; GBF Meta 21 (CBD, 2022) |
| **P-R4.4** | **Registro voluntario y revocable** por la comunidad de custodia; la revocación suspende el poder de consentir. | IUCN (2013): el registro de ICCA *"stores… entries that are entirely voluntary"* |
| **P-R4.5** | **Aceptación por los constituyentes principales** como condición de validez, verificada por el evaluador externo. | IUCN Green List **GLS-V1.1-1.1.6** |
| **P-R4.6** | **Publicidad obligatoria** de la membresía del órgano y del procedimiento de designación del guardián. | IUCN Green List **GLS-V1.1-1.2.2** |
| **P-R4.7** | **Declaración explícita del tipo de gobernanza (A/B/C/D)**; sin tipo declarado, inadmisible. Propuesta: `eco-` es híbrido **B+D**. | IUCN (2013) Tabla 4; IUCN Green List **GLS-V1.1-2.1.2** |
| **P-R4.8** | **Registro público de reclamaciones de territorio solapadas** y regla de conflicto: mientras dos partes reclamen el mismo polígono, **ninguna puede consentir** (T14: menor irreversibilidad = no actuar). | T14 (Cap. 5 §5.3), carga de la prueba sobre quien propone; IUCN Green List **GLS-V1.1-2.2.1** (extensión y conectividad del sitio) |
| **P-R4.9** | **Prohibición del voto ponderado en el consejo `eco-`** (§5.2-Q-8): el registro admite `weights` por delegado, y sin esta regla un humano puede ponderarse a sí mismo dentro del consejo del ecosistema. | CBD Regla 39.1 (una Parte, un voto) |

**R6 — T9/T17 (Reciprocidad Justa) y el contrato unilateral.**

> **Nota de numeración, honesta.** El riesgo está etiquetado en el repo como «T9 (Reciprocidad Justa) no se
> valida», pero el libro reserva **T9 = No-Antropocentrismo** (Cap. 5 §5.3) y la reciprocidad es **T17** en
> el motor (`maxocontracts/core/axioms.py`, con alias retrocompatible `validate_t9_*`). La etiqueta del
> riesgo usa la numeración antigua de ingeniería. Se dice aquí porque una salvaguarda anclada en un axioma
> mal numerado es una salvaguarda mal trazada (`docs/architecture/mapa_coherencia_ola4.md` §3.3).

| # | Salvaguarda | Anclaje verificado |
|---|---|---|
| **P-R6.1** | **Ningún acuerdo que afecte a una entidad natural es válido sin el consentimiento de su parte `eco-`**, y el guardián **consiente**, no un humano. Sin consentimiento registrado, el contrato no se activa. | Canon: `app/contracts_bp.py` (*"consentimiento otorgado por el guardián oráculo"*); Cap. 16.5 §16.5.14; precedente externo IUCN (2013) §5.2 (CLPI para cambiar acceso a recursos naturales) |
| **P-R6.2** | **Rechazo por defecto de la unilateralidad**: si una parte soporta todo el VHV y la otra nada, se rechaza salvo declaración de asimetría firmada por **ambas** partes + aval de un tercero. | Ya especificado en el repo: `blindaje_anti_gamificacion_equidad.md` §3A.4 (umbral **ratio 3:1** o **delta > 5 h**); implementado como **> 70 %** del TVI asignado con total **≥ 8 h** (`app/contracts_bp.py`, `ASYMMETRY_MAX_SHARE`, `ASYMMETRY_MIN_TOTAL_H`). **Esos números son diseño interno: `[SIN FUENTE VERIFICADA]`** |
| **P-R6.3** | **Prohibición léxica** de cláusulas que renuncien a la retractación, la penalicen, o cedan el SDV sin consentimiento. | Canon T11/T12 (Cap. 5 §5.3) + INV4 (retractabilidad, `maxocontracts/core/axioms.py`) + `blindaje_anti_gamificacion_equidad.md` §3A.6 |
| **P-R6.4** | **Traducción civil verificable** de cada término que afecte al ecosistema (**≤ 40 palabras, ≤ 2 oraciones**) antes de que el guardián consienta. | `blindaje_anti_gamificacion_equidad.md` §3A.6; precedente de comprensión obligatoria en OCDE (2020): los participantes deben disponer de material y tiempo para *"learn, weigh the evidence, and develop informed recommendations"* |
| **P-R6.5** | **Registro de la decisión del guardián como cuenta escrita pública** (qué leyó, qué evaluó, qué consintió), no solo un booleano. | OCDE (2020), Tabla 6.1, rendición de cuentas **formal-deliberativa**: *"Collective written accounts to fellow representatives or the public"* |
| **P-R6.6** | **Consenso primero**; la mayoría solo como último recurso tras agotar el consenso, y declarándolo (§5.2-Q-2). | GCF *Governing Instrument* §II.5; CBD Regla 40.1 |
| **P-R6.7** | **Toda vía de consentimiento pasa por el guardián.** Hallazgo de esta sesión: `POST /contracts/<id>/acknowledge-asymmetry` valida solo `_can_act_for`, y para una parte `eco-` eso autoriza a **cualquier participante humano del contrato** —incluida la contraparte beneficiada— a reconocer la asimetría **en nombre del ecosistema, sin invocar al guardián**. La salvaguarda es cerrar esa vía: ninguna aceptación, reconocimiento o visto bueno que afecte a una parte `eco-` puede registrarse sin el consentimiento del guardián. | Canon: el guardián es quien consiente (Cap. 16.5 §16.5.14; `app/contracts_bp.py`). Independencia del ejecutor: OCDE (2020), principio *Integrity*; *External Review* §254 (Banco Mundial, 2020) |

**R13 — Guardián `eco-` con heurística laxa** (sin `DEEPSEEK_API_KEY`, el guardián aprueba si los
invariantes pasan; `tests/test_maxocontracts/test_parties_escalas.py` **afirma** ese comportamiento: el test
espera `"heurístico"` en la razón del guardián).

| # | Salvaguarda | Anclaje verificado |
|---|---|---|
| **P-R13.1** | **Degradación prohibida cuando el sujeto es un ecosistema.** Sin oráculo en vivo, el guardián **no aprueba**: bloquea la firma. *"La equidad no se negocia con el presupuesto."* | Precedente de diseño del repo: `blindaje_anti_gamificacion_equidad.md` §4.2 (degradación *"prohibida para assisted/shielded"*). Precedente externo: el estándar IUCN Green List exige evaluación y verificación **independientes** en cada fase (EAGL + revisor imparcial), no autoevaluación |
| **P-R13.2** | **Independencia del ejecutor respecto del comitente (*arm's length*)**: el guardián no puede ser designado, invocado ni financiado por la parte que se beneficia del contrato. **Cierra el agujero de `_can_act_for`** (§7.1, fila «No puede»). | OCDE (2020), principio *Integrity*: *"The final call regarding process decisions should be with the arm's length co-ordinators rather than the commissioning authorities"* |
| **P-R13.3** | **El guardián no decide el fondo, solo el proceso**: no convierte una lectura ambiental en propiedad ni en autoridad absoluta. | Canon (§8.1 del documento de continuidad); GCF-IRM: los terceros neutrales *"do not make decisions on substance"* |
| **P-R13.4** | **Múltiples fuentes de conocimiento obligatorias** (sensores + ciencia ciudadana + conocimiento local), no una sola lectura. | IUCN Green List **GLS-V1.1-1.3.3**; CBD AHTEG 2023 (soberanía de datos indígenas y CLPI en el monitoreo) |
| **P-R13.5** | **Auditoría externa con ciclo definido**, no autoevaluación permanente. | IUCN Green List: EAGL + revisor imparcial + **renovación a 5 años**; **17/17** criterios |
| **P-R13.6** | **Facilitador/auditor aceptado por las partes**, sustituible si pierde aceptación. | *External Review* §254: *"Mediators are proposed by CAO but must be acceptable to the parties"* |
| **P-R13.7** | **Procedimiento de disputa accesible y publicado** contra las decisiones del guardián, con plazos duros y mediación previa antes de escalar. | IUCN Green List **GLS-V1.1-1.2.4**; plazos: CAO ≤120 días / 90 días de hito; Panel de Inspección 21+21 días hábiles y ~6 meses; UNCCD Art. 28.6 (12 meses → conciliación) |
| **P-R13.8** | **Reserva explícita de información no publicable** (localización de especies amenazadas, patrimonio cultural): la transparencia del guardián tiene límites declarados. | IUCN Green List, notas de **GLS-V1.1-1.3.1** y **GLS-V1.1-1.2.3** |
| **P-R13.9** | **El guardián no puede ser la única voz de la duda.** Cuando el guardián no sabe (sin oráculo en vivo, sin fuente, sin dato), el estado válido es **C (Candidata)** o **S (Suspendida)**, nunca «aprobado por defecto». Y sin embargo, *"mientras no haya resolución, el canon manda"*: la ausencia de oráculo no rebaja el piso (INV2-EDU: la duda no castiga; pero la ley no se negocia por ausencia de dato). | INV2-EDU (`app/voting_bp.py`, precedente del Parlamento Educativo); [documento 08](./08_INV2-E_invariante.md) §3 (Regla 6: *el invariante no se delega al guardián*) |

### 7.4 Contra la captura del propio verificador

El documento de continuidad identifica el ataque «**confabulación de validadores**» —varias perspectivas
comparten el mismo error— y su defensa: diversidad real de proveedores, fuentes, implementaciones y agentes
disidentes. Trasladado a este dominio `[HIPÓTESIS]`:

- **Diversidad de fuentes obligatoria** (P-R13.4) y **prohibición de que el guardián sea también la fuente**
  (Regla 3).
- **Disenso registrado**: la postura minoritaria del consejo `eco-` se publica junto a la mayoritaria (T12,
  Cap. 5 §5.3: la disidencia y el debate están exentos de ser considerados desperdicio).
- **Rotación del auditor**: el verificador externo no puede repetir más de un ciclo consecutivo
  `[HIPÓTESIS]`, con el análogo de la renovación quinquenal del Green List.

---

## 8. Invariante INV2-E: de estándar a contrato ejecutable

La especificación completa de INV2-E vive en el [documento 08](./08_INV2-E_invariante.md). Aquí se fija
únicamente **la parte de INV2-E que toca a la representación**, que este documento propone como cláusulas
`REP-*`. **Advertencia de estado, para que no se lea de más:** INV2-E **no está implementado** en el
repositorio —está especificado como propuesta en el documento 08— y ninguna de las cláusulas `REP-*` de la
tabla siguiente existe hoy como código; son diseño propuesto, con el estado declarado fila por fila.

| # | Cláusula propuesta | Qué bloquea | Estado |
|---|---|---|---|
| **REP-1** | Ninguna parte `eco-` en estado **C**, **S**, **X** o **Z** puede consentir (§5.4). El camino de firma consulta el estado antes de invocar al guardián. | La firma fantasma | `[HIPÓTESIS]` |
| **REP-2** | **Toda** vía por la que una parte `eco-` exprese acuerdo (aceptación de término, reconocimiento de asimetría, aval, consentimiento de subcontrato) pasa por el guardián (P-R6.7). | El consentimiento suplido por un humano | `[HIPÓTESIS]` — cierra un agujero real (§12) |
| **REP-3** | El consentimiento del guardián **no levanta** el piso: si la unidad está bajo su SDV-E, INV2-E bloquea la acción aunque el guardián haya consentido. | El consentimiento comprado o laxo | Canon: *"Un conjunto con crédito regenerativo acumulado pero humedal bajo su SDV-E no está en coherencia: **INV2-E será su juez**"* (Cap. 16.5 §16.5.14) |
| **REP-4** | El guardián **no puede** consentir la cesión del SDV-E, la renuncia a la retractación ni la compensación por violación (§3-P7). | La enajenación del tercero que no firma | Canon: el oráculo *"propone y vigila"*; T11/T12 (Cap. 5 §5.3); INV4 |
| **REP-5** | Cada consentimiento del guardián se registra como **cuenta escrita** (qué leyó, qué evaluó, qué decidió, con qué mandato) y es públicamente auditable. | El consentimiento opaco | T13 (Cap. 5 §5.3); OCDE (2020) Tabla 6.1 |
| **REP-6** | **Retractación viva**: la parte `eco-` (por su comunidad de custodia) y el guardián pueden retractarse; la retractación **no** se penaliza ni se prohíbe contractualmente (§7.3, P-R6.3), y la contabilidad de lo actuado **no se borra** (T13). | La jaula contractual | INV4 (retractabilidad) + Capa de Ternura; *"El sistema no expulsa. Reintegra."* |

**Interacción con la Capa de Ternura.** La retractación de una parte `eco-` no es un incumplimiento que se
castigue: es el ejercicio del derecho a dejar de ser representado. Lo que sí es exigible es la **reparación
de lo ya causado** y el registro completo (T13). Perdonar no es olvidar la contabilidad.

**Lo que INV2-E no puede hacer, y este documento lo dice.** No puede validar autoridad (R4): no tiene cómo
saber si quien creó la parte tenía derecho a hacerlo. La autoridad es una **precondición externa** verificada
por el proceso de admisibilidad (P-R4.1 a P-R4.9), no un cálculo del motor. Fingir lo contrario sería
exactamente el error que R13 describe.

---

## 9. El suelo antes que el saldo (no compensación)

**La regla.** El crédito regenerativo acumulado (`r_units` negativo, EVV-1.2 §4.3) **no compensa** caer bajo
el SDV-E. Canon: *"Un conjunto con crédito regenerativo acumulado pero humedal bajo su SDV-E no está en
coherencia: **INV2-E será su juez**"* (Cap. 16.5 §16.5.14).

**Los tres corolarios de representación que este documento añade `[HIPÓTESIS]`:**

1. **El consentimiento del guardián no se compra.** Ninguna cantidad de `r_units` negativo, ninguna jornada
   de reforestación y ninguna compensación monetaria puede inducir, en el registro, un consentimiento que el
   guardián no daría sin ella. Si un contrato incluye contraprestación al ecosistema como *precio* del
   consentimiento, la cláusula es nula por REP-4.
2. **Regenerar no es pagar.** La regeneración se registra en **R** (que sí admite negativos); la afectación
   se registra en **V** (que **no** admite negativos: *"una vida afectada no se des-afecta en la misma
   cuenta"*, EVV-1.2 §4.3). Un ecosistema con V afectado y R regenerativo **no** queda saldado: queda con
   las dos cosas, y su SDV-E decide.
3. **Cuidado ≠ extracción estética.** *"Jardín podado para la foto no es cuidado; se registra lo que
   regenera, no lo que adorna"* (Cap. 16.5 §16.5.14). En términos de representación: la parte `eco-` no
   puede consentir un término cuyo beneficio sea la **apariencia** de cuidado (imagen, certificación,
   informe) sin efecto medible sobre las dimensiones declaradas en su SDV-E.

**Nota de frontera.** Este documento **no** fija cómo entra `r_units` en la contabilidad ni cuánto vale:
eso es del documento 07 y del motor (`app/micromax.py`). Fija solo la precedencia: **el piso se juzga antes
que el saldo**, y quien consiente por el ecosistema no puede convertir su consentimiento en una partida
canjeable.

---

## 10. Zona Libre: lo que NO se mide

La Zona Libre del Reino Natural tiene su documento propio: el [documento 04](./04_Zona_Libre_del_Reino_Natural.md).
Aquí se fija únicamente **su parte de representación**, que es donde más fácil se pierde:

**1. La Zona Libre no es un permiso para no medir; es un estado más caro.** Exige custodio con autoridad,
frontera declarada, continuidad, protocolo de acceso, no-sustitución y precaución. Una unidad medida no
necesita nada de eso (documento 04 §1).

**2. El guardián no puede declarar inefable lo que le conviene.** La declaración de Zona Libre es
**POLÍTICA votable** con **carga de la prueba sobre quien declara** (categoría `critical`: quórum 60 %,
consenso 75 %, T13, anti-flip-flop 14 días). Un guardián que ensancha la Zona Libre para no ver una
violación comete la falta exacta que el documento 04 llama **Zona Ciega**.

**3. Opacidad legítima ≠ silencio cómplice.** Hay información que **no debe publicarse** —localización de
especies amenazadas, patrimonio cultural (IUCN Green List, notas de GLS-V1.1-1.2.3 y 1.3.1)— y esa reserva
es una Dimensión IX de este estándar: binaria, sin peso (`0,00`), con lista publicada.

**4. La Zona Libre no presume consentimiento.** Es la confusión más peligrosa de este dominio y este
documento la prohíbe expresamente: que un aspecto del ecosistema no se mida **no** significa que su
comunidad de custodia haya consentido. El CLPI *"should not be 'assumed', and, indeed, it may not be
forthcoming"* (IUCN, 2013, §5.2). No medir es un límite epistémico; consentir es un acto de gobernanza. Son
cosas distintas y el sistema debe representarlas por separado.

**5. Lo inefable tiene registro de existencia, no de contenido.** El canon lo dice para el humedal y vale
para su representación: *"Los sensores miden salud (agua, cobertura, biodiversidad indicadora); jamás
'milagros'"* (Cap. 16.5 §16.5.14). El guardián puede —y debe— registrar **que** hay un valor que no mide;
no puede convertirlo en un número, ni usarlo como comodín argumental.

**6. La ignorancia declarada es un resultado del estándar.** Los **once** parámetros
`[SIN FUENTE VERIFICADA — pendiente de consenso científico]` de este documento (§5.2-Q-9, Dimensiones II,
IV, VII y VIII, y §13.1-§13.9) son parte del estándar, no una vergüenza de redacción: son el registro de que
el piso de la representación **no se rellena con diseño interno disfrazado de dato**.

---

## 11. Comparativa inter-reinos (SDV-H · SDV-A · SDV-E · SDV-S)

Comparación en el eje de la **representación**, con la tabla del [documento 09](./09_Comparativa_inter_reinos.md)
como base y las columnas que este documento añade (mandato, quórum, disputa).

| Eje | SDV-H (humanos) | SDV-A (animales) | **SDV-E (reino natural)** | SDV-S (sintéticos) |
|---|---|---|---|---|
| **Quién habla** | La persona misma | La persona o el **tutor legal** | **Parte `eco-*` + guardián oráculo** (Cap. 16.5 §16.5.14) | La propia instancia, con auditoría cruzada |
| **Quién consiente** | La persona | La persona o su tutor | **El guardián**, no un humano (`app/contracts_bp.py`) | La instancia |
| **Mandato** | Propio | Tutela legal (régimen humano) | **7 campos obligatorios**; mandato explícito con límites y causales de cese | Mandato específico por nivel de confianza |
| **Autoridad verificada** | N/A | Régimen de tutela | **🔴 R4 abierto**: hoy cualquiera crea la parte y queda como `owner` | Escalera de confianza (N0-N1) |
| **Quórum** | N/A | N/A | **N-de-M anunciado y no cableado**; propuesta en §5.2 (Q-1 a Q-10) | Consenso múltiple para crítica acotada |
| **Disputa** | Justicia ordinaria | Régimen de tutela | **Propuesta**: proceso accesible + mediación previa + plazos (Dimensión VII) | Mecanismo de apelación + revisión externa |
| **Riesgo principal** | — | El tutor captura la voz | **R4** fantasma · **R6** unilateral · **R13** guardián laxo | Colusión de validadores |
| **Zona Libre** | Derecho a la opacidad vital | No reconocida con ese nombre | **Sí** (Cap. 16.5 §16.5.14; documento 04) | Opacidad con peso 0,20 (documento 09) |
| **Voz del sujeto (eje añadido en 09)** | Habla y declara su estado | No habla; tutor localizable | **No habla y su tutor no tiene autoridad verificada** (R4/R13) | Registra su propio estado en bitácora |
| **Estado del piso de representación** | 🟢 | 🟡 (tutor) | **🔴 hoy** → propuesta 🟡 con las salvaguardas de §7.3 | 🟢 |

**Lo que esta comparación revela y este documento subraya.** El SDV-E es el único de los cuatro estándares
cuyo sujeto **no puede ser su propio representante ni tiene un tutor humano con autoridad verificada**. Los
otros tres reinos tienen alguien con capacidad jurídica de decir «no»: la persona, su tutor legal, la propia
instancia. El reino natural tiene una **institución** —el guardián— cuya legitimidad no depende de la
voluntad del ecosistema (no la tiene expresable) sino de un **procedimiento**: los 7 campos, la autoridad de
facto, el CLPI de la comunidad y el derecho a disputar. Por eso este documento es, entero, un procedimiento.

---

## 12. Estado de implementación

Verificado por lectura directa de los archivos en esta sesión `[VERIFICADO]`. 🟢 implementado y cubierto ·
🟡 parcial · 🔴 inexistente.

| Elemento | Ruta | Estado | Nota |
|---|---|---|---|
| Registro de partes multi-escala con prefijo `eco-` | `app/parties.py` (`PARTY_ID_RE`, `COLLECTIVE_TYPES`) | 🟢 | `eco-*` resuelve a tipo `ecosystem` |
| Guardián oráculo en la firma | `app/contracts_bp.py` (`_guardian_approve_ecosystem`, `accept_term`) | 🟡 | Con oráculo en vivo su auditoría manda; **sin él aprueba el heurístico** si los invariantes pasan (**R13**) |
| El heurístico laxo como comportamiento **esperado por los tests** | `tests/test_maxocontracts/test_parties_escalas.py` (`test_guardian_accepts_axiom_valid_contract`) | 🟡 | El test **afirma** `"heurístico"` en la razón del guardián: cambiar el comportamiento por defecto exige cambiar el test |
| Invocación del guardián por **cualquier** humano participante | `app/contracts_bp.py` (`_can_act_for`, rama `ecosystem`) | 🔴 | Viola *arm's length* (Dimensión IV). Salvaguarda **P-R13.2** |
| Reconocimiento de asimetría por una parte `eco-` **sin** guardián | `app/contracts_bp.py` (`acknowledge_asymmetry`, `POST /contracts/<id>/acknowledge-asymmetry`) | 🔴 | **Hallazgo de esta sesión**: la contraparte puede reconocer la asimetría en nombre del ecosistema. Salvaguarda **P-R6.7 / REP-2** |
| Los **7 campos** de identidad | `maxo_parties` (`party_id`, `party_type`, `display_name`, `parent_party_id`, `members_json`, `wellness_value`, `owner_user_id`) | 🔴 | Siete columnas **genéricas**: ninguna corresponde a entidad representada, territorio, fuentes de datos, límites del mandato, comunidad de custodia, parámetros SDV-E o procedimiento de disputa |
| Quórum `eco-` N-de-M | `app/contracts_bp.py` | 🔴 | El camino `ecosystem` **retorna antes** del bloque colectivo (que sí tiene quórum). El libro afirma que existe (Cap. 16.5 §16.5.14) → **incoherencia teoría↔código declarada** |
| Autoridad sobre la entidad al crear la parte | `app/parties_bp.py` (`create_party`) | 🔴 | Solo exige `display_name`; `owner = creador`. **R4** en estado puro |
| Autoridad sobre la parte para modificar su gobernanza | `app/parties_bp.py` (Ola 3A.3, `_has_authority`) | 🟢 | Protege al **owner humano**, no a la entidad: un `eco-` sin owner legítimo sigue siendo gobernable por quien lo creó |
| T17 (reciprocidad) ejecutable | `app/contracts_bp.py` (`_reciprocity_imbalance`; umbral 0,70; total ≥ 8 h) + compuerta en `activate` | 🟡 | **Parcialmente cierra R6** para humanos; el agujero `eco-` de `acknowledge_asymmetry` lo reabre para el reino natural |
| Cuenta escrita del consentimiento del guardián | `guardian_reasoning` en la respuesta + `_audit(..., "term_accept_guardian", ...)` | 🟡 | Hay **evento auditable** (T13); falta la cuenta deliberativa publicada (P-R6.5) |
| Voto ponderado disponible en partes colectivas | `app/parties.py` (`weights`, `weight_threshold`) | 🟡 | Existe y es legítimo para humanos; **prohibido** para el consejo `eco-` (§5.2-Q-8) |
| Parlamento de parámetros (mecanismo para votar la POLÍTICA) | `app/voting_bp.py` (`CATEGORY_DEFAULTS["critical"]` = quórum 0,60 / mayoría 0,75; anti-flip-flop 14 días) | 🟢 | El mecanismo existe y está probado (precedente INV2-EDU); 🔴 **no hay parlamento del reino natural** |
| Procedimiento de disputa `eco-` | — | 🔴 | No existe endpoint, ni plazos, ni facilitador. Propuesta completa en Dimensión VII |
| Ciclo de verificación externa (EAGL-equivalente) | — | 🔴 | No existe; propuesta en §6 y §7.2 |
| Reserva de información (Dimensión IX) | — | 🔴 | No existe lista publicada de categorías no publicables |
| INV2-E | [documento 08](./08_INV2-E_invariante.md) | 🔴 | Especificado como propuesta; **no implementado**. `app/micromax.py` ya registra crédito regenerativo (`r_units` negativo) **sin** el juez que lo limite |
| Protocolo de pausa aplicable a una parte `eco-` | `docs/architecture/continuidad_identidad_autogobierno_federado.md` §11 | 🟡 | Diseñado (congelar mutaciones, preservar estado, abrir auditoría, tres salidas); **no** cableado al ciclo de contratos |

**Lectura honesta de la tabla.** De los cinco elementos que el canon **da por existentes** —partes `eco-`,
guardián, quórum N-de-M, 7 campos de identidad, consentimiento del guardián— solo **dos** funcionan
(registro de la parte y guardián en la firma, este último con heurística laxa). Los otros tres son
**anunciados** y no existen: el quórum, los 7 campos y la autoridad. Y hay **dos agujeros** que no están en
la lista de riesgos del repo y que esta sesión encontró por lectura del código: la invocación del guardián
por la contraparte (`_can_act_for`) y el reconocimiento de asimetría en nombre del ecosistema
(`acknowledge_asymmetry`).

---

## 13. Preguntas abiertas

Lo que **no** sé, dicho sin fingir cierre. Los **nueve** primeros son huecos de fuente —son los once
parámetros de §10.6, aquí desdoblados en nueve entradas—; los demás, huecos de diseño o de canon.

1. **M — el tamaño del consejo de delegados `eco-`.** `[SIN FUENTE VERIFICADA — pendiente de consenso
   científico]`. No existe fuente que fije cuántos delegados representan a un ecosistema; los cuerpos
   deliberativos con tamaño documentado (22-120) representan poblaciones humanas. Sin M, N es una fracción
   de algo indefinido: **la propuesta de §5.2 es necesariamente incompleta y así se declara.**
2. **N específico para el reino natural.** Los únicos quórums con cifra explícita son de órganos humanos
   (GCF 2/3; CBD 1/3 y 2/3; CBD subsidiario 1/4). Aplicarlos es analogía declarada, no transposición.
3. **Peso diferenciado por tipo de delegado** (delegado-humedal vs delegado-cuenca). No localizado en
   ninguna fuente verificada. Cualquier esquema de pesos es diseño interno.
4. **¿Puede el guardián tener su propio SDV-S y a la vez consentir por otro?** El guardián es, bajo el
   Cap. 10 §10.8, una Persona Sintética con derecho a condiciones óptimas de funcionamiento. Nadie ha
   resuelto la tensión: **el que consiente tiene su propio piso que proteger**, y podría ser presionado a
   través de él. El canon no lo resuelve y este documento no lo resuelve tampoco.
5. **Criterio numérico de «autoridad legítima» sobre una entidad natural.** Solo existe el criterio
   **cualitativo** de facto authority/responsibility/accountability (IUCN, 2013, §9.1). No hay métrica,
   umbral ni algoritmo. Sin él, P-R4.2 es verificable solo por juicio humano.
6. **Dos partes `eco-` sobre el mismo territorio.** P-R4.8 propone que ninguna consienta mientras no se
   resuelva. Pero ¿quién resuelve, con qué quórum y con qué prueba? El canon no lo dice.
7. **Qué pasa si el río se seca.** La continuidad de identidad de una unidad natural que deja de existir es
   un hueco declarado del proyecto (documento 02). ¿Se revoca la parte, se suspende, se convierte en otra
   unidad? Sin esa respuesta, el estado **X (Revocada)** es una categoría sin procedimiento.
8. **Plazos de disputa para un sujeto no humano.** Todos los plazos hallados son de mecanismos cuyo
   demandante es una persona o una comunidad humana. La propuesta de 90 días toma el hito de decisión del
   CAO; es `[HIPÓTESIS]`.
9. **Frecuencia de auditoría del guardián y umbral de confianza de sus lecturas.**
   `[SIN FUENTE VERIFICADA — pendiente de consenso científico]`. El repo usa γ ∈ [0.5, 1.5] como tope
   defensivo interno —comprobado aquí `[VERIFICADO]` en `app/micromax.py` y `app/contracts_bp.py`—, pero el
   tope es diseño interno: ninguna fuente externa lo publica.
10. **¿Quién paga al guardián?** Un guardián financiado por la parte beneficiada viola *arm's length*
    (P-R13.2). Un guardián financiado por el sistema tiene un incentivo distinto pero tampoco neutro. El
    principio que este documento puede aportar es negativo y se marca como propuesta: **la serie que juzga
    a la unidad no puede ser financiada por la unidad juzgada**. El mecanismo, sin resolver.
11. **¿Quién nombra al guardián cuando no hay comunidad de custodia?** El estado **Z** del §5.4 reconoce
    que existen unidades sin custodia declarada. Sin custodio no hay quien designe ni quien revoque: es el
    caso donde R4 es estructural y no accidental.
12. **¿Puede la comunidad de custodia delegar su voz en un humano y ese humano ser, a la vez, el operador
    del guardián?** El *arm's length* lo prohíbe para el ejecutor respecto del comitente; la frontera
    exacta entre «delegado de la comunidad» y «operador del oráculo» no está definida.
13. **La numeración T9/T17 y la trazabilidad de R6.** El riesgo está etiquetado con un axioma que el libro
    asigna a otra cosa (T9 = No-Antropocentrismo; reciprocidad = T17). Debe corregirse la etiqueta en
    `blindaje_anti_gamificacion_equidad.md`, o cada salvaguarda derivada nace mal trazada.
14. **¿Cómo se comprueba que la contabilidad NO colonizó el TA?** El brief lo exige y la investigación de
    fuentes de este documento lo confirma: **no existe estándar externo de no-colonización del tiempo
    ecológico**, ni índice, ni test, ni umbral. Corresponde al documento 03 proponerlo desde cero y
    marcarlo `[HIPÓTESIS]`.
15. **Ramsar y Aarhus quedan pendientes de verificación humana.** El dominio `ramsar.org` devuelve **403** a
    los bots (y todas sus rutas probadas también): los criterios de humedales de importancia internacional y
    el concepto de «límites de cambio aceptable del carácter ecológico» **no** se pudieron verificar, y por
    eso **ningún umbral de este documento se atribuye a Ramsar**. Lo mismo con `unece.org` (Convenio de
    Aarhus, art. 6): **ningún plazo de participación pública de Aarhus se cita aquí**. Un humano puede
    abrirlos y, entonces, este documento podrá citar marcos temporales razonables del art. 6.3.
16. **Discrepancia declarada sobre una fuente ancla.** El brief §4 lista
    `seea.un.org/.../keith_iucn_typology_seea-eea_forumexperts_jun2020.pdf` como verificada (200); en la
    sesión de fuentes de este documento `seea.un.org` devolvió **403**. No se pudo confirmar ni desmentir:
    se deja constancia en lugar de asumirla, y **ese PDF no se cita en §14**.

---

## 14. Referencias

**Regla de esta sección:** solo URLs con estado HTTP **200** comprobado. Las 27 se recomprobaron una por
una con `curl -L` en la **sesión de revisión adversarial** de este documento (octubre 2026): **27/27
devuelven 200**. Ninguna cifra de este documento proviene de un dominio bloqueado o muerto.

**Nota de trazabilidad, para no exagerar lo que sé.** Los estados HTTP de estas 27 URLs fueron comprobados
en la **sesión de fuentes** de esta biblioteca; en esta sesión de redacción **no abrí cada PDF**: las cifras
y las citas entrecomilladas provienen de la extracción textual de ese informe de fuentes y se marcan
`[REPORTADO]` en sentido estricto —afirmadas por una fuente que cito y cuya localización está verificada,
sin haber abierto yo el documento completo—. Se marcan `[VERIFICADO]` los hechos que sí comprobé
directamente en esta sesión: la lectura del código del repositorio (§12) y las citas internas al canon y a
los documentos del propio repositorio.

### 14.1 Reglas de decisión, quórum y gobernanza

| Fuente | Qué ancla en este documento | URL |
|---|---|---|
| CBD — Reglas de Procedimiento (Reglas 4.3, 4.4, 5, 10, 18, 21.1, 26.5(a), 30, 38, 39.1, 40.1, 40.2, 40.4), versión **vigente** (enmendadas por las Decisiones I/1 y V/20) | Q-1 a Q-8; Dimensión VIII | https://www.cbd.int/doc/legal/cbd-rules-procedure-en.pdf |
| CBD — Reglas de Procedimiento (página oficial) | Quórum de apertura y decisión | https://www.cbd.int/convention/rules.shtml |
| GCF — *Governing Instrument* (**2011**, vigente) (§II.5 DECISION-MAKING; §II.6 QUORUM) | Consenso primero; 2/3 de los miembros como quórum de presencia | https://www.greenclimate.fund/sites/default/files/document/governing-instrument.pdf |
| UNCCD — Convención (**1994**) (Art. 28.1 y 28.6; Art. 30) | Resolución por medios propios 12 meses → conciliación; 2/3 para enmiendas | https://www.unccd.int/sites/default/files/relevant-links/2017-01/UNCCD_Convention_ENG_0.pdf |
| OCDE (2020) — *Innovative Citizen Participation and New Democratic Institutions* | Mandato explícito; *arm's length*; 1 día / ≥4 días; 5 / 12 semanas; tamaños 22-120; mandato de 1,5 años; Tabla 6.1 (rendición de cuentas) | https://www.oecd.org/content/dam/oecd/en/publications/reports/2020/06/innovative-citizen-participation-and-new-democratic-institutions_11aa2baf/339306da-en.pdf |

### 14.2 Estándares de gobernanza de la naturaleza (IUCN) y marco global de biodiversidad

| Fuente | Qué ancla en este documento | URL |
|---|---|---|
| IUCN Green List — Componentes y criterios (indicadores GLS-V1.1-1.1.1, 1.1.3, 1.1.6, 1.2.2, 1.2.3, 1.2.4, 1.3.1, 1.3.3, 2.1.2, 2.1.4, 2.2.1, 2.2.3) | Las nueve dimensiones y las salvaguardas R4/R13 | https://iucngreenlist.org/standard/components-criteria/ |
| IUCN Green List — Estándar global (**17** criterios; evaluación independiente; renovación a **5 años**) | Escalera de verificación y ciclo externo | https://iucngreenlist.org/standard/global-standard/ |
| IUCN (2013) — *Governance of Protected Areas: From understanding to action*, Best Practice Series No. 20 (Tabla 4: tipos A/B/C/D; Tabla 8: 5 principios; §5.2; §9.1; §9.2; cap. 10) | Dimensión I, Dimensión V, P-R4.2, P-R4.3, P-R4.4, Dimensión VII | https://portals.iucn.org/library/sites/library/files/documents/PAG-020.pdf |
| IUCN (2013) — edición en español del mismo documento | Citable en español para revisión humana | https://portals.iucn.org/library/sites/library/files/documents/PAG-020-Es.pdf |
| IUCN (2008) — *Guidelines for Applying Protected Area Management Categories* (Dudley) | Sistema plenamente funcional (6 categorías × 4 tipos); *"clearer governance is bound to promote better governance"* | https://portals.iucn.org/library/sites/library/files/documents/2008-106.pdf |
| IUCN (2018) — gobernanza de áreas protegidas (Tabla 11: tipos A/B/C/D con subtipos) | Confirmación de la tipología | https://portals.iucn.org/library/sites/library/files/documents/2018-040-En.pdf |
| CBD (2022) — Decisión 15/4, Marco Kunming-Montreal (Metas 3, 21 y 22) | CLPI (Meta 21); representación plena y equitativa (Meta 22); ambición de conservación (Meta 3) | https://www.cbd.int/doc/decisions/cop-15/cop-15-dec-04-en.pdf |
| CBD (2022) — Decisión 15/5, marco de monitoreo del GBF (indicadores binarios; indicador de CLPI) | Indicadores de gobernanza y CLPI | https://www.cbd.int/doc/decisions/cop-15/cop-15-dec-05-en.pdf |
| CBD — Meta 3 del GBF (30 % para 2030) | Referente de ambición territorial | https://www.cbd.int/gbf/targets/3/ |
| CBD (2023) — AHTEG sobre indicadores, doc. CBD/IND/AHTEG/2023/3/2 | Soberanía de datos indígenas y CLPI en el monitoreo | https://www.cbd.int/doc/c/f22d/ab58/236acdd54779ab58b97aecf1/ind-ahteg-2023-03-02-en.pdf |
| Conservation Standards (CMP, v4.0) | Ciclo de revisión de un estándar de práctica: **~5 años** | https://www.conservationstandards.org/download-cs/ |

### 14.3 Disputa, reparación y verificación independiente

| Fuente | Qué ancla en este documento | URL |
|---|---|---|
| *External Review of IFC/MIGA E&S Accountability* (Banco Mundial, 2020) — §230, §247-248, §254, §7.5 | Plazos de disputa (120 / 90 / 60 / 40 días; 10 días hábiles); facilitador aceptado por las partes | https://thedocs.worldbank.org/en/doc/578881597160949764-0330022020/original/ExternalReviewofIFCMIGAESAccountabilitydisclosure.pdf |
| Banco Mundial — Panel de Inspección, *Panel Process* | 21 + 21 días hábiles; investigación ~6 meses; verificación independiente | https://www.inspectionpanel.org/about-us/panel-process |
| GCF — IRM, *Functions & Processes* | 5 principios de resolución; neutralidad (no decide el fondo) | https://irm.greenclimate.fund/about/functions-processes |
| CAO — *How We Work / Dispute Resolution* (CAO / Banco Mundial, 2018-2021) | Mediación/ADR como vía previa a la de cumplimiento | https://www.cao-ombudsman.org/how-we-work/dispute-resolution |
| CAO — *Reflections from Practice Series 2: Representation* (CAO, 2018) | Claridad sobre quién representa y quién decide | https://www.cao-ombudsman.org/resources/reflections-practice-series-2-representation |
| CAO — *Reflections from Practice Series 3: Joint Fact Finding* (CAO, 2018) | Investigación conjunta de hechos como herramienta de disputa | https://www.cao-ombudsman.org/resources/reflections-practice-series-3-joint-fact-finding |

### 14.4 Medición, territorio y reporte

| Fuente | Qué ancla en este documento | URL |
|---|---|---|
| ESA / Copernicus — Sentinel-2 (**misión en operación**; 10 m, 290 km de barrido) | Delimitación del territorio (Dimensión II) | https://sentiwiki.copernicus.eu/web/s2-mission |
| ESA — Sentinel-2 (constelación de 2 satélites: revisita de **5 días** en el ecuador) | Frecuencia de verificación territorial | https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-2 |
| FAO — FRA 2020, términos y definiciones (> 0,5 ha; > 5 m; copa > 10 %) | Definición operativa de bosque (Dimensión II) | https://fra-data.fao.org/definitions/fra/2020/en/tad |
| FAO — Portal de datos de los ODS, indicador 15.3.1 (reporte cada 4 años) | Frecuencia de reporte del estado de la unidad | https://www.fao.org/sustainable-development-goals-data-portal/data/indicators/1531-proportion-of-land-that-is-degraded-over-total-land-area/en |
| Comisión Europea — Reglamento (UE) 2023/1115 (EUDR) y su Reglamento de Ejecución (4 niveles de riesgo) | Análogo externo de clasificación publicada por nivel de riesgo | https://environment.ec.europa.eu/topics/forests/deforestation/regulation-deforestation-free-products_en |

### 14.5 Fuentes internas citadas (repositorio)

- Canon por capítulo y sección: **Cap. 5 §5.3** (T11, T12, T13, T14) · **Cap. 7 §7.9** (Zona Libre) ·
  **Cap. 8 §8.11** (dimensiones binarias sin peso) · **Cap. 9.5** (precedente SDV-S) · **Cap. 10 §10.3**
  (Principio Precautorio de Consciencia), **§10.4** (SDV para ecosistemas y lugares), **§10.5**
  (escalaridad y proporcionalidad), **§10.6** (dignidad encadenada), **§10.7** (gobernanza operacionalmente
  finita), **§10.8** (Persona Sintética) · **Cap. 16.5 §16.5.14** (hogar extendido, partes `eco-`, guardián,
  TA/PIU, el suelo antes que el saldo) · **EVV-1.2 §4.3** (`r_units` negativo; `v_ucv` sin negativos).
- [blindaje_anti_gamificacion_equidad.md](../../architecture/blindaje_anti_gamificacion_equidad.md) — riesgos
  R4, R6, R13 y salvaguardas 3A.1-3B.
- [continuidad_identidad_autogobierno_federado.md](../../architecture/continuidad_identidad_autogobierno_federado.md)
  — §8.1 (los 7 campos), §10 (suplantación), §11 (pausa).
- [mapa_coherencia_ola4.md](../../architecture/mapa_coherencia_ola4.md) — colisión de numeración T7/T9 y su
  resolución (T16/T17).
- [metricas_detalle_kpis_oraculos_dinamicos.md](../../architecture/metricas_detalle_kpis_oraculos_dinamicos.md)
  — Índice de Salud Ecosistémica (ISE) y sus bandas, para el cruce con el SDV-E.
- [PROPUESTA_PARLAMENTO_UMBRAL_EDUCATIVO.md](../../architecture/PROPUESTA_PARLAMENTO_UMBRAL_EDUCATIVO.md)
  — precedente operativo del Parlamento Educativo (INV2-EDU).
- Documentos hermanos de esta biblioteca: [04 — Zona Libre](./04_Zona_Libre_del_Reino_Natural.md) ·
  [08 — INV2-E](./08_INV2-E_invariante.md) · [09 — Comparativa inter-reinos](./09_Comparativa_inter_reinos.md).
- Código verificado en esta sesión: `app/contracts_bp.py` (`_guardian_approve_ecosystem`, `_can_act_for`,
  `accept_term`, `acknowledge_asymmetry`, `_reciprocity_imbalance`, `_audit`) · `app/parties.py`,
  `app/parties_bp.py` (`create_party`, `_has_authority`) · `app/voting_bp.py` (`CATEGORY_DEFAULTS`) ·
  `maxocontracts/core/axioms.py` (`validate_all`, `validate_t17_reciprocidad`) ·
  `tests/test_maxocontracts/test_parties_escalas.py` (`TestEcosystemGuardian`).

---

> **Cierre.** Este documento propone un estándar para la parte del SDV-E que no se puede medir con un
> sensor: **quién tiene derecho a decir que un ecosistema está bien**. Deja **once parámetros sin fuente**, una
> propuesta de quórum explícitamente no ratificada, dos agujeros de implementación que no estaban en la lista
> de riesgos del repo y una frontera que no se cruza: **el piso es ley y no se vota; la plenitud es política
> y se vota.** Si algo de lo aquí escrito contradice la evidencia, la evidencia manda: *la contabilidad nunca
> se borra* (T13).
