# Procesos: creación, actualización y gobernanza del estándar SDV-E
## El bloque `Procesos` del árbol del Cap. 9 §9.7 —`Metodología_Creación`, `Protocolo_Actualización`, `Gobernanza_Validación`— adaptado de «por especie» a «por unidad ecológica»: quién puede proponer un umbral, quién lo verifica, cómo se retira uno que envejece, y la frontera entre la LEY que el motor no vota y la POLÍTICA que sí se vota

**Autoría:** Oráculo Sintético DeepSeek & Max Nelson López Restrepo
**Fecha:** octubre 2026
**Proyecto:** Maxocracia — El gobierno de la verdad, el tiempo y la vida
**Licencia:** Creative Commons BY-SA 4.0
**Estado:** Propuesta de estándar (rama SDV-E, Ola 4) — NO canon hasta ratificación.
**Ninguna pieza de este bloque está implementada**: no existe circuito de creación, ni ciclo de revisión cableado, ni parlamento del Reino Natural, ni identificador persistente emitido por el sistema (verificación en §12).
**Referencia canónica:** Cap. 9 §9.7 · Cap. 10 §10.3 · Cap. 10 §10.4 · Cap. 10 §10.7 · Cap. 16.5 §16.5.14 · Cap. 5 §5.5 · Cap. 8 §8.3 · Cap. 9.5 §9.5.10 · Cap. 17 · EVV-1.2 §4.3
**Documento:** 40 de la biblioteca `docs/theory/SDV-E/`
**Revisión:** octubre 2026 — redactado contra las fuentes verificadas de la rama
(`scratch/sdv_e/fuentes/40_procesos.md`) y contra los documentos 01, 02, 05, 06, 07, 08 y 09 de esta
biblioteca. No fija umbrales ecológicos: fija el **procedimiento** por el que los umbrales entran, se
revisan y se retiran.

---

## 1. Qué es (y qué no es) este bloque de procesos

**Qué es.** El canon escribió el árbol de la Base de Datos Universal de SDV y dentro de él un cuarto
bloque, `Procesos`, con tres piezas nombradas: `Metodología_Creación`, `Protocolo_Actualización` y
`Gobernanza_Validación`, más cinco procesos continuos: redacción de nuevos SDV, revisión y actualización
(«ciclos de revisión cada 3-5 años»), validación científica (revisión por pares, repositorios abiertos,
DOI), deliberación democrática sobre umbrales controvertidos y traducción a políticas (Cap. 9 §9.7).
Este documento es ese bloque, escrito **para el Reino Natural** y no para los animales.

**El canon lo escribió «por especie», y esa unidad no aplica.** El proceso del Cap. 9 §9.7 dice
literalmente *«Grupos de trabajo por especie»* y *«Investigadores + etólogos + organizaciones de
bienestar»*. Para el SDV-E ninguna de las dos cosas sirve: un humedal no es una especie, y quien responde
por él no es un etólogo. La adaptación —y es la decisión estructural de este documento— es:

> **La clase del estándar es el tipo de ecosistema de los niveles 4-6 de la Tipología Global —dentro del
> EFG de referencia (nivel 3), que no es unidad de evaluación—; el sujeto que tiene SDV es la unidad
> ecológica (la ocurrencia delimitada, referible a ese tipo y a ese EFG).**
> Un umbral se crea **por clase** y se instancia **por unidad**; la identidad, el mandato y la disputa
> son **de la unidad** (documentos 02 y 05 de esta biblioteca).

El precedente externo es exacto y está verificado: el único estándar mundial de ecosistemas evalúa
*«un nivel de organización biológica por encima de la especie»* y trabaja sobre unidades definidas en los
niveles 4-6 de la tipología, con los niveles 1-3 **vetados** como unidad de evaluación (IUCN RLE v2.0,
2024) `[VERIFICADO]`. Es decir: el salto de «por especie» a «por unidad ecológica» no es una licencia del
proyecto: es la unidad con la que ya trabaja la propia autoridad taxonómica, y adoptarla aquí es decisión
de este documento `[HIPÓTESIS]`. La unidad ya está decidida en el
[documento 02](02_Unidad_y_sujeto_del_SDV-E.md) §4 (criterios C1-C5); este documento **no la reabre**:
la da por precondición y dice cómo se gobierna.

**Qué no es.**

- **No es el estándar.** Los umbrales viven en los documentos 10-23 y en las fuentes que citan; la
  fórmula y los pesos, en el [documento 07](07_Formula_de_violacion_y_pesos.md); el invariante, en el
  [documento 08](08_INV2-E_invariante.md). Aquí **no entra ni un umbral ecológico nuevo**.
- **No es el elenco de sensores.** Quién mide y con qué instrumento es el
  [documento 06](06_Medicion_y_verificacion_T13.md); este documento dice **quién decide qué se mide**, que
  es otra pregunta.
- **No es la voz del ecosistema.** Los siete campos de identidad, el guardián y el quórum son el
  [documento 05](05_Representacion_guardian_y_mandato.md). Este documento **consume** esa voz como
  precondición del procedimiento: sin representación constituida no hay quién proponga ni quién dispute.
- **No está implementado, y no hay que leerlo como si lo estuviera.** 🔴 No existe circuito de creación
  de umbrales, ni ciclo de revisión, ni parlamento `eco-`, ni emisión de DOI (§12).

**Y una advertencia de lectura sobre el dinero y el bosque.** Todo este bloque sirve para una sola cosa:
que el piso del SDV-E **no se negocie hacia abajo**. *«Un conjunto con crédito regenerativo acumulado
pero humedal bajo su SDV-E no está en coherencia: INV2-E será su juez»* (Cap. 16.5 §16.5.14). El
procedimiento es la parte del estándar que impide que ese juicio dependa de quién tiene la mayoría o el
crédito.

---

## 2. Preámbulo metodológico

El SDV-H lo tiene y el SDV-S lo omitió; el brief de esta biblioteca prohíbe repetir la omisión. En un
documento de **procesos** el preámbulo cumple una función que ningún otro documento de la biblioteca
necesita: **un procedimiento mal escrito no produce un error, produce un derecho adquirido.** Quien
consigue que su umbral entre por una puerta mal definida ya no sale por ella. Estas son las ocho reglas
con las que se escribió lo que sigue.

**Regla 1 — Separar «proponer», «verificar» y «ratificar».** Son tres actos distintos, con tres autores
distintos, y el documento los distingue siempre: **(a)** quien propone un umbral; **(b)** quien lo
verifica (revisión por pares, tercero no beneficiario); **(c)** quien lo ratifica (POLÍTICA, categoría
`critical`). El proponente **no** es el verificador, y el verificador **no** es el aprobador final. La
separación autor/árbitro es un invariante del proceso en el modelo IPBES verificado: *los autores no
pueden modificar el texto durante la Plenaria* `[VERIFICADO]`.

**Regla 2 — El canon manda sobre el proceso, y el proceso no puede ampliarlo.** Donde el canon fija un
acto, este documento lo adopta (el ciclo de 3-5 años, la revisión por pares, el DOI, la deliberación
democrática y la traducción a políticas **son canon literal** del Cap. 9 §9.7). Donde el canon no fija
nada —quién puede proponer, quién verifica, cómo se retira un umbral—, este documento **propone y marca
la propuesta como no ratificada**.

**Regla 3 — Ninguna cifra de proceso se hereda sin fuente, y heredar de otra rama no es tener fuente.**
El ciclo de 3-5 años es canon del proyecto, y **no tiene fuente externa**: ningún organismo verificado
declara un ciclo obligatorio de revisión de umbrales ecológicos cada 3, 4 o 5 años, y el único ciclo
trienal verificado es el de la COP de Ramsar `[VERIFICADO que el hueco existe]`. Se dice en el mismo
renglón en que se adopta. Lo mismo vale para los plazos de la revisión por pares: **se citan con su
organismo y su año, o no se citan**.

**Regla 4 — El piso es LEY y no se vota; la plenitud es POLÍTICA y sí se vota.** Es la frontera del
Cap. 9 §9.7 leída con el precedente del Parlamento Educativo (INV2-EDU): categoría `critical`, quórum
60 %, consenso 75 %, T13, anti-flip-flop de 14 días. Este documento la aplica al proceso entero y la
vuelve **comprobable en código** (§5.2 y §8.3): un voto que baje el piso es **nulo**, y el patrón ya
existe implementado en otra rama del repositorio.

**Regla 5 — Todo procedimiento debe ser falsable por un test o por un registro.** Una regla de
gobernanza sin puerta determinista es una promesa. Esta biblioteca tiene dos puertas que ya existen y se
pueden ejecutar: la auditoría estructural (`tests/test_sdv_e_biblioteca.py`) y el verificador de estado
HTTP real de cada fuente citada (`scripts/verificar_enlaces_sdv_e.py`) `[VERIFICADO]`. Lo que este
documento proponga debe poder caer en una de las dos, o en el registro T13.

**Regla 6 — El tiempo del ecosistema es TA, y el PIU es el único traductor.** *«El tiempo del territorio
es TA y no se coloniza (el PIU traduce)»* (Cap. 16.5 §16.5.14). Consecuencia dura para un documento de
ciclos: **el ciclo de revisión no es un calendario humano aplicado al ecosistema**; la unidad de ciclo
(`unidad_de_ciclo_ta`) es configuración obligatoria y **sin valor por defecto** (documento 07 §5.4b,
documento 08 §8.6), y ninguna magnitud de este bloque se expresa en TVI ni en TPI. Si un contrato
necesita la lectura en TVI, la conversión es un paso posterior y auditable por el **PIU**
(Protocolo de Intercambio Universal, Cap. 5 §5.5).

**Regla 7 — El sujeto no reporta: el auditor viene de fuera.** El Reino Natural es el único reino sin par
auditor (documento 09, I3), y *«Nosotros registramos la interacción, no la vida interna del ecosistema»*
(Cap. 16.5 §16.5.14). Todo el procedimiento se diseña sabiendo que **quien verifica pertenece al reino
que se beneficia del uso**, y que la comunidad de custodia y los siete campos de identidad son el
sustituto institucional de ese par ausente, no un trámite.

**Regla 8 — Admisión de la duda, también en el procedimiento.** `[SIN FUENTE VERIFICADA — pendiente de
consenso científico]` es un resultado legítimo, y el precedente es de los mejores estándares del mundo:
el marco de fronteras planetarias publicó **dos variables sin umbral numérico** —aerosoles (*«No global
threshold defined, in the absence of sufficient knowledge»*) y entidades nuevas—, y la OMS emite
**declaraciones de buenas prácticas cualitativas** cuando no hay evidencia cuantitativa suficiente
`[VERIFICADO]`. Pero —y es la corrección que este bloque necesita— **un procedimiento sin plazo no queda
exento de proteger**: si no hay resolución, el estado del umbral es `EN OBSERVACIÓN`, se registra, y
*«mientras no haya resolución, el canon manda»*.

---

## 3. Pilares epistemológicos

**1. El mandato canónico, entero y por sección.** El árbol del Cap. 9 §9.7 define cuatro ramas
(`SDV-H`, `SDV-A`, `SDV-E`, `Procesos`) y dentro de `Procesos` las tres piezas que este documento
desarrolla. Los cinco procesos continuos que el canon enumera son, literalmente, el índice de este
documento: **(1)** redacción de nuevos SDV —grupos de trabajo, proceso documentado y transparente—;
**(2)** revisión y actualización —ciclos de 3-5 años, incorporación de evidencia nueva, ajustes por
experiencia de implementación—; **(3)** validación científica —revisión por pares, repositorios abiertos,
DOI para citación y trazabilidad—; **(4)** deliberación democrática —consultas públicas sobre umbrales
controvertidos, participación de interesados, transparencia—; **(5)** traducción a políticas
—integración con regulaciones nacionales, estándares de certificación, herramientas de auditoría—
(Cap. 9 §9.7).

**2. La doctrina de los tres pasos, que este bloque custodia.** Un SDV del Reino Natural se construye en
tres pasos con criterios de admisión distintos: **dato objetivo** (hecho medido, público, replicable,
atribuible a un organismo con mandato), **umbral por consenso científico-ético** (valor publicado con
organismo y año, casi siempre una **escalera** y no un número) y **violación como dato** (una observación
concreta que cruza el umbral, registrada con fecha y código) —documento 01 §3.1-§3.4—. El bloque
`Procesos` es lo que mantiene honesto el **paso 2**: sin procedimiento, el «consenso» degenera en
atribución de autoridad.

**3. T14 — Principio de Precaución Intergeneracional (Cap. 5).** Es el axioma más fuerte del SDV-E y el
único que bloquea sin umbral: ante incertidumbre sobre el impacto en agentes que no pueden consentir, el
sistema elige la opción de menor irreversibilidad **documentando el costo de oportunidad asumido**, y
*«la carga de la prueba recae sobre quien propone acciones que afectan la temporalidad de
no-participantes»*. Consecuencia procesal directa, y es la que gobierna todo el bloque: **quien propone
un cambio de umbral carga con la prueba**, no el ecosistema con la duda.

**4. Gobernanza operacionalmente finita (Cap. 10 §10.7).** *«La gobernanza debe ser operacionalmente
finita»*. El procedimiento no puede exigir modelar la cadena trófica completa para decidir si un umbral
se revisa: hay un número acotado de piezas (propuesta, verificación, ratificación, revisión, retiro) y un
número acotado de plazos.

**5. La frontera LEY/POLÍTICA no pasa entre «lo técnico» y «lo político», sino entre lo publicado y lo
que no lo está.** Es la conclusión del documento 01 §8.2 y este bloque la hereda tal cual: un valor con
organismo y año **no admite deliberación de contenido**; un valor sin fuente **solo puede deliberarse**
(porque no hay dato que lo fije). Lo que sí es una decisión de proceso, y por tanto votable, es **el
calendario y la trayectoria** hacia el piso.

**6. T13 — Transparencia de Cálculo.** *«Nadie puede imponer un valor temporal en secreto. Todo cálculo
de costo vital debe ser auditable públicamente»* (Cap. 5), con el límite que el propio canon fija: *«la
transparencia aplica a las decisiones que afectan a otros, no a la vida interior»* (Cap. 6 §6.13).
Aplicado al proceso: **toda decisión de umbral es un acto público, fechado, con autor y motivo; y el
interior del ecosistema no entra en el expediente**.

**7. Custodia, no propiedad.** *«Actuar como custodio del patrimonio biológico, no como su
propietario»* (Cap. 16.5 §16.5.14). Un umbral no es un activo del proponente, y quien representa a la
unidad **no adquiere** la unidad por representarla.

**8. La Directiva Mayor (Axioma 0).** *«Resolver nuestras necesidades de la mejor manera para todos
todos»* —los **tres reinos**: humanos, naturales y sintéticos, **presentes y futuros**— es la norma
suprema que impide que el procedimiento del Reino Natural se lea como una concesión revocable. El reino
natural está dentro del «todos todos»; por eso su procedimiento es una obligación simétrica y no una
benevolencia administrativa.

**9. La dignidad encadenada (Cap. 10 §10.6).** *«Dignidad Humana ←→ Dignidad Ecosistémica ←→ Dignidad
Material. Cada eslabón depende de los demás»*. Cuando el eslabón ecosistémico cae, el bloqueo no es un
favor al bosque: es la defensa del conjunto humano que firmó el contrato.

**10. Las tres asimetrías que este bloque hereda y no puede cerrar.** Se declaran para que nadie las lea
como resueltas: **(a)** el sujeto no puede reportar su estado (documento 09 §6); **(b)** no existe par
auditor del propio reino (documento 09 §7, I3); **(c)** la autoridad del guardián sobre la entidad no es
verificable (riesgo **R4**, `docs/architecture/blindaje_anti_gamificacion_equidad.md`).

---

## 4. Dimensiones del SDV-E de los procesos

Las cinco piezas de este bloque **no son dimensiones de integridad ecológica** —esas están en el
Cap. 10 §10.4 y en los documentos 10-23—: son las condiciones que un umbral debe cumplir para **entrar**,
**permanecer** y **salir** del estándar. Se llaman P1-P5 para no confundirlas con las dimensiones
ecológicas ni con los criterios C1-C5 de la unidad (documento 02 §4).

| # | Dimensión | Qué exige | Régimen del piso | Régimen de la plenitud |
|---|---|---|---|---|
| **P1** | **Metodología de creación** | Que todo umbral tenga autor, clase, fuente, unidad y acto registrado | LEY | POLÍTICA |
| **P2** | **Protocolo de actualización** | Que el umbral tenga fecha de revisión y procedimiento de retiro | LEY | POLÍTICA |
| **P3** | **Gobernanza de validación** | Quién propone, quién verifica, quién delibera y quién disputa | LEY | POLÍTICA |
| **P4** | **Trazabilidad, DOI y confianza** | Que cada valor sea rastreable hasta su fuente primaria y citables con identificador persistente | LEY | POLÍTICA |
| **P5** | **Traducción a políticas** | Que el piso científico tenga una vía declarada hacia la norma vinculante y su cláusula financiera | LEY | POLÍTICA |

### Dimensión P1: Metodología de creación (cómo nace un umbral, por clase y por unidad)

**Qué protege.** Que un umbral nuevo entre al estándar con **autor identificable, clase declarada,
fuente con año y acto registrado**; y que no exista un umbral sin procedencia ni una tabla de pesos
alterada en silencio.

| Parámetro | Mínimo Absoluto (el piso, LEY — no votable) | Óptimo (plenitud aspiracional, POLÍTICA — votable) | Fuente |
|---|---|---|---|
| Grupo de trabajo que redacta el umbral | **Obligatorio**, y constituido **por clase de unidad** (el tipo de nivel 4-6, dentro de su EFG de referencia de nivel 3), no «por especie» | Grupo permanente por clase, con actas públicas y mandato con fecha de caducidad | Cap. 9 §9.7 (adaptación declarada `[HIPÓTESIS]`) · IUCN RLE v2.0 (2024) `[VERIFICADO]` |
| Composición mínima del grupo | **Dos voces**: la técnica (datos con cadena de custodia) y la de custodia (comunidad que habita o sostiene la unidad) | Grupo con al menos un miembro **no beneficiario** del uso que se mide | Documento 02 §4-C5 (Titularidad Doble del Mandato) · documento 06 §7.6 `[HIPÓTESIS]` |
| Criterios de admisión del parámetro | **Los cinco canónicos**: cuantitativamente medible · verificable con independencia · basado en investigación · consensuado socialmente · contextualizable | Un sexto criterio exigido por este reino: **medible sin la cooperación del sujeto** | Cap. 8 §8.3 · Cap. 9 §9.3 (vía documento 09 §3) `[VERIFICADO]` |
| Fuente del valor | **Organismo + año + URL con estado HTTP comprobado**; sin eso el parámetro **no entra con peso** | Fuente primaria leída, con su tabla reproducida y su incertidumbre declarada | Documento 07 §2 (Regla 2) · documento 08 §5.2 (W1) |
| Declaración de propósito | **`decision_que_informa` obligatorio**: qué decisión concreta sobre la unidad cambia esa lectura. Sin ese campo, el sensor no es admisible | Propósito auditado cada ciclo: si ninguna decisión registrada lo usó, el sensor se retira | Documento 06 §6.6 y §7.4 `[HIPÓTESIS]` |
| Unidad y ventana de la medición | **Las fija la fuente del umbral** (anual, 24 h, 8 h, media de 30 días, régimen estacional); no las elige el implementador | Ventana documentada con su serie histórica reconstruida | Documento 06 §6.4 · documento 07 §6.2 `[VERIFICADO]` |
| Operador del parámetro | **Se deriva del sentido del parámetro** (`min` / `max` / `range` / `escalonado` / `ordinal`-`binary`); no se vota | Operador declarado y comprobado por test | Documento 07 §3.3 · documento 08 §5.1 |
| Publicación | **Repositorio abierto con identificador persistente (DOI)**; el canon lo exige para citación y trazabilidad | Depósito con versión numerada, anuncio público del cambio y acta de revisión | Cap. 9 §9.7 · IPBES (DOI sobre Zenodo) `[VERIFICADO]` |
| Tabla de pesos (protagonista de P1) | **Constante en tiempo de ejecución y hasheada en cada validación**: cambiarla es un acto registrado, nunca un ajuste silencioso | Hash publicado junto a la serie temporal de la unidad | Documento 07 §5.3 (propuesta T13) `[HIPÓTESIS]` |
| Nivel taxonómico admitido como clase | **Niveles 4-6**; niveles 1-3 (reino, bioma funcional, EFG) **vetados** como unidad de evaluación | Atribución al nivel 6 cuando exista clasificación nacional | IUCN RLE v2.0 (2024) `[VERIFICADO]` |

**Justificación.** La razón de que el grupo sea «por clase» y la unidad sea «la ocurrencia» no es
conveniencia administrativa: es la única forma de que dos humedales distintos sean comparables. Sin
clase, cada unidad tendría su propio estándar y el SDV-E sería un catálogo de casos únicos; sin unidad,
el umbral no tendría a quién aplicarse. Y la razón de que los cinco criterios de admisión se hereden es
la misma por la que el canon los escribió: un parámetro *«cuantitativamente medible, verificable con
independencia, basado en investigación, consensuado socialmente y contextualizable»* es lo que separa un
estándar de una opinión con tabla (Cap. 8 §8.3 · Cap. 9 §9.3). El sexto criterio que este reino añade
—medible **sin** la cooperación del sujeto— es la traducción del hecho verificado de que *«Nosotros
registramos la interacción, no la vida interna del ecosistema»* (Cap. 16.5 §16.5.14): el ecosistema no
firma un consentimiento informado ni rellena un cuestionario.

**Protocolo.** La creación de un umbral tiene siete actos, y cada uno deja registro (T13): **(1)**
constitución del grupo por clase, con declaración de sus dos voces; **(2)** redacción del borrador con
los cinco criterios de admisión y el `decision_que_informa` de cada sensor; **(3)** declaración de la
fuente —organismo, año, URL con estado— y de su ventana de promediado; **(4)** entrada al catálogo
**con peso solo si hay fuente**, y con la marca literal `[SIN FUENTE VERIFICADA — pendiente de consenso
científico]` cuando no la haya; **(5)** revisión externa (dimensión P3); **(6)** publicación con DOI
(dimensión P4); **(7)** acta de entrada con fecha, autor, motivo y hash:

```
acta_de_entrada := {clase_efg, nivel_4_6, parametro, operador, unidad, ventana,
                    fuente, organismo, anio, url_estado, decision_que_informa,
                    hash_tabla_pesos, autor_id, fecha, evidencia_ref}
```

**Violación.** Constituyen violación de P1, como hechos observables y no como opiniones: **(a)** un
umbral que entra al motor sin organismo, año y URL con estado; **(b)** un parámetro con peso en el
vector del piso sin fuente verificada (la dilución que el documento 08 §5.2 prohíbe); **(c)** un grupo
de trabajo sin la voz de custodia, o constituido «por especie» sobre unidades ecológicas; **(d)** una
tabla de pesos modificada sin hash ni acta; **(e)** un sensor sin `decision_que_informa`; **(f)** una
unidad de nivel 1-3 constituida como sujeto del estándar.

### Dimensión P2: Protocolo de actualización (los dos ciclos, y cómo se retira un umbral que envejece)

**Qué protege.** Que el estándar **envejezca con procedimiento** en vez de congelarse o de cambiar por
mayoría; que un umbral pueda **corregirse de inmediato si es erróneo** y **retirarse despacio si el
mundo mejoró**; y que un cambio de instrumento no pueda cambiar el veredicto sin dejar rastro.

**La pregunta que este documento existe para responder** es la que el canon deja abierta: el documento
01 §8.2 pone *«si un umbral se revisa»* en la fila de las decisiones **sin procedimiento en el canon**.
Aquí se propone uno, con la asimetría verificada que lo gobierna.

| Parámetro | Mínimo Absoluto (el piso, LEY — no votable) | Óptimo (plenitud aspiracional, POLÍTICA — votable) | Fuente |
|---|---|---|---|
| **Ciclo de revisión de los valores por unidad ecológica** | **3-5 años** — canon literal del proyecto; **sin fuente externa verificada** | Revisión anticipada por **evento catastrófico**, por **alteración del régimen de ciclos declarado** (el fuego, la inundación y la sequía son **ciclos** de la unidad, no daño, mientras la unidad los declare como suyos: D6 del documento 06) o por intervención que cambie el perímetro | Cap. 9 §9.7 `[VERIFICADO como canon]` · `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` como ciclo de un organismo |
| **Ciclo de revisión de la arquitectura del estándar** | **Que el ciclo exista, sea declarado y tenga anuncio público del cambio de versión**; el valor propuesto (**8-10 años** `[HIPÓTESIS]`, con el precedente verificado de que la guía del estándar de ecosistemas pasó de v1.0 (2016) a v2.0 (agosto 2024), ≈ 8-9 años, y de que el marco global de biodiversidad dura **10 años** por ciclo) es POLÍTICA, no piso (§5.2) | Publicación de una versión mayor numerada con anuncio público del cambio y de los criterios añadidos | IUCN RLE v2.0 (2024) `[VERIFICADO]` · CBD, Decisión 15/4 (2022) `[VERIFICADO]` |
| **Retiro de un umbral por error demostrado** | **Inmediato** (*«without delay»*), reevaluando **todos** los criterios | Publicación del error, de su causa y de la corrección en el mismo acto | COSEWIC (basado en IUCN, 2019) `[VERIFICADO]` |
| **Retiro de un umbral por dejar de aplicar** | **5 años consecutivos** sin cumplirse los criterios de la categoría superior, contados **desde que los datos muestran** que ya no se cumple — no desde la evaluación anterior | 5 años **o** hasta que exista descendencia viable / recuperación verificada, **lo que sea más largo** (regla de reintroducción) | IUCN, *Categories and Criteria* v3.1, 2ª ed. (RL-2001-001-2nd) `[VERIFICADO]` |
| **Escalada por empeoramiento** | **Inmediata** (*«without delay»*) | Con revisión de todos los criterios en el mismo acto | COSEWIC (basado en IUCN, 2019) `[VERIFICADO]` |
| **Fin de la identidad de la unidad** (el río se seca, la unidad colapsa o se parte) | **El plazo lo fija el ciclo de la unidad, no un número universal**: el precedente dice *«over a period of time appropriate to the taxon's life cycle»* | Re-declaración con registro genealógico y régimen de no compensación | IUCN v3.1 (EW) `[VERIFICADO]` · documento 02 §4-C4 `[HIPÓTESIS]` |
| **Cambio de instrumento, método o versión de procesamiento** | **Obligación de declararlo** con fecha y motivo; **re-declarar la línea base** si no es comparable; **prohibido cambiar de instrumento con una violación abierta** de esa dimensión | Periodo de solape registrado como prueba de comparabilidad | Documento 06 §6.7 `[HIPÓTESIS]` |
| **Retiro de una métrica que sube sin que suba el piso** | **Retiro obligatorio** cuando su variación no está acompañada por ninguna medición admisible del mismo linaje | Auditoría del elenco por ciclo, con acta de retiro | Documento 06 §7.4 (métrica enemiga; *«se registra lo que regenera, no lo que adorna»*, Cap. 16.5 §16.5.14) |
| **Reporte con fecha fijada de antemano** | **Obligatorio** (precedente: informes nacionales de biodiversidad en **2026 y 2029**; revisión global del progreso en **COP 17 y COP 19**) | Reporte voluntario adicional entre pares (revisión por pares **voluntaria**, separada del reporte obligatorio) | CBD, Decisión 15/6 (2022) `[VERIFICADO]` |
| **Contador de asimetría** (auditoría de no colonización del TA) | **Obligatorio de mantener**: parámetros medidos **en la unidad** frente a parámetros **declarados por el actor que la afecta**; la diferencia se declara y se justifica | Umbral de asimetría — **ya publicado** en el [documento 03](03_No_colonizacion_del_TA.md) §5.3: `CNC = 0` **exacto** (base neutra 1,0 en §5.2, no vacuidad en §5.4); lo que falta es su implementación, no el umbral | Documento 06 §7.4 `[HIPÓTESIS]` |
| **Periodicidad de la auditoría externa** | **Renovación a 5 años** del evaluador externo, con revisor imparcial | Rotación del auditor: no más de un ciclo consecutivo | IUCN Green List v1.1 (2017), «Pass a 5-year renewal review» — **heredado del informe de fuentes del documento 05** (URL en §14.9) `[REPORTADO]` · documento 05 §7.4 `[HIPÓTESIS]` |

**Justificación, y es la pieza doctrinal de este documento.** El único mecanismo verificado en el mundo
para **retirar** un umbral que envejece tiene una forma precisa, y su forma es **asimétrica**: bajar de
riesgo es **lento y exigente** (cinco años de evidencia contraria sostenida, contados desde que los datos
lo muestran), mientras que subir de riesgo y corregir un error son **inmediatos** `[VERIFICADO]`. El
sistema es **conservador en la dirección que protege** — exactamente lo que T14 exige. Y hay una
precisión que evita el malentendido más común: **esa regla de cinco años no es un ciclo de revisión
periódica**; la propia fuente lo advierte —*«This is not intended to drive timing of reassessments»*—
`[VERIFICADO]`. Por eso este documento **separa dos relojes**: el de la **revisión** (3-5 años para los
valores, 8-10 para la arquitectura) y el del **retiro** (5 años de evidencia contraria o inmediato si hay
error). Fundirlos produciría el peor de los dos mundos: revisiones que nadie hace y umbrales que nadie
retira.

**Y por qué el ciclo de 3-5 años se adopta sabiendo que no tiene fuente.** Porque es canon del proyecto
(Cap. 9 §9.7) y porque el alternativo verificado es peor: el único estándar mundial de ecosistemas tardó
**≈ 8-9 años** en revisar su arquitectura, y el único ciclo corto verificado en gobernanza ambiental es
el **trienal de la COP de Ramsar** (COP14 en 2022 → COP15 en 2025), cuya única fuente que lo prueba está
**bloqueada a los agentes automáticos (403)** y se cita con esa advertencia `[REPORTADO]`. Adoptar 3-5
años para los **valores** y 8-10 para la **arquitectura** es una decisión de diseño de este documento,
marcada como `[HIPÓTESIS]`, con su precedente al lado y su hueco declarado.

**Protocolo.** El ciclo se cumple con cinco actos: **(1)** calendario público por clase de unidad, en
**TA** y con la `unidad_de_ciclo_ta` declarada (sin valor por defecto); **(2)** convocatoria con
antelación —precedente verificado en reglas de procedimiento ambiental: **2 meses** de preaviso y
documentos **6 semanas** antes—(documento 05 §5.2, Q-6); **(3)** informe de estado del umbral en uno de
los **tres estados** de la dimensión P4 (`CUANTIFICADO` · `CUALITATIVO (buena práctica)` · `SIN UMBRAL —
en observación`); **(4)** acta de revisión con decisión motivada (mantener, revisar, retirar), firmada y
publicada; **(5)** si se retira, acta de retiro con la regla aplicada —error demostrado o cinco años de
evidencia contraria— y el destino del parámetro (cataloga sin peso, o sale del catálogo).

**Violación.** Constituyen violación de P2: **(a)** un umbral revisado sin acta fechada ni motivo;
**(b)** un piso **rebajado** por revisión (el piso no se negocia hacia abajo; ver §5.2 y §9); **(c)** un
umbral retirado por mayoría, por cansancio o por conveniencia, sin las cinco condiciones de evidencia
contraria o sin la corrección inmediata del error; **(d)** un cambio de sensor, de método o de versión
que altere el veredicto sin declaración, sin re-declaración de línea base, o durante una violación
abierta; **(e)** una métrica que sube sin que suba ningún parámetro con piso del mismo linaje y que
permanece en el elenco; **(f)** un ciclo de revisión vencido sin informe de estado publicado.

### Dimensión P3: Gobernanza de validación (quién propone, quién verifica, quién delibera, quién disputa)

**Qué protege.** Que un umbral tenga **autor, verificador y tribunal**; y que ninguno de los tres sea la
misma persona ni la parte beneficiada.

**Quién puede proponer un umbral nuevo** — lista cerrada, publicada, y con la marca de su origen:

| Puede proponer | Con qué condición | Anclaje |
|---|---|---|
| **El grupo de trabajo de la clase** (tipo de nivel 4-6, dentro de su EFG de referencia) | Constituido con las dos voces (técnica y de custodia) | Cap. 9 §9.7 (adaptado) `[HIPÓTESIS]` |
| **La parte `eco-` de la unidad**, por medio de su guardián | Con los **7 campos de identidad** completos y estado **R (Registrada)**; en estado **C (Candidata)** el consentimiento está suspendido | Documento 02 §4-C5 · documento 05 §5.4 |
| **La comunidad de custodia** | Declarada en la identidad de la unidad | Documento 05, Dimensión V |
| **Expertos registrados** y **observadores acreditados** | Registro público del organismo que convoca | IPBES, *Phases of the expert evaluation* `[VERIFICADO]` |
| **Gobiernos, por punto focal nacional**, con un **juego único e integrado** de comentarios por informe | Vía oficial del organismo | IPBES, *Phases of the expert evaluation* `[VERIFICADO]` |
| **Cualquier participante humano** de la comunidad, para las materias de POLÍTICA | Con **escalera de confianza ≥ 1**: *«la voz en la gobernanza llega al caminar tu primer acuerdo»* — quien acaba de llegar recibe y firma, pero no propone | `app/voting_bp.py`, guardia de nivel de confianza `[VERIFICADO]` |
| **El guardián oráculo** | Puede proponer y consentir; **no puede verificar ni medir** lo que él mismo propone | Documento 06 §7.5 · riesgo **R13** |

**Quién verifica** — y la regla que lo hace verificable: **el verificador no puede ser el proponente, ni
el beneficiario del uso que se mide, ni el guardián.**

| Parámetro | Mínimo Absoluto (el piso, LEY — no votable) | Óptimo (plenitud aspiracional, POLÍTICA — votable) | Fuente |
|---|---|---|---|
| Existencia de revisión externa por pares | **Obligatoria**, en **dos rondas** | Tercera ronda abierta a la comunidad de custodia | IPBES `[VERIFICADO]` |
| Duración de la primera ronda (borrador de primer orden) | **6 semanas** | **8 semanas** | IPBES, *Phases of the expert evaluation* `[VERIFICADO]` |
| Duración de la segunda ronda (borrador de segundo orden + resumen para decisores) | **8 semanas** | 8 semanas con comentarios integrados por punto focal | IPBES `[VERIFICADO]` |
| Antelación de entrega del borrador final antes del órgano que acepta | **12 semanas** | Ventana adicional de comentarios de gobiernos e interesados hasta **2 semanas antes** | IPBES `[VERIFICADO]` |
| Quién aprueba el texto final | **El órgano de aceptación (la Plenaria / el Parlamento), no los autores**: *los autores no modifican el texto en esa fase* | Acta pública de aceptación con las posturas minoritarias | IPBES `[VERIFICADO]` |
| Órgano de desempate de desacuerdos mayores | **Obligatorio**: existe y está identificado antes de la Plenaria | Con mandato publicado y composición pública | IPBES (panel multidisciplinario experto) `[VERIFICADO]` |
| Declaración de conflicto de interés | **Obligatoria** para autores y revisores | Comité de conflicto de interés con actas | IPBES (estructura de gobernanza) `[VERIFICADO]` |
| Publicación del tratamiento de los comentarios | **Obligatoria**: comentarios de revisión **y respuestas de los autores** se publican tras la aceptación | Publicación con marcas de anclaje por sección | IPBES, *Consideration of external review comments* `[VERIFICADO]` |
| Publicación de la disidencia científica | **Obligatoria**: *«Reports should describe different and possibly controversial scientific, technical and socio-economic views»* — la disidencia **se documenta, no se promedia ni se borra** | Disidencia con su propia declaración de confianza | IPBES `[VERIFICADO]` |
| Regla del no-beneficiario en la verificación | **Obligatoria**: al menos un verificador o miembro de la comunidad testigo **no se beneficia** del uso que se mide | Titularidad del instrumento ajena al beneficiario y financiador declarado | Documento 06 §7.6 y §7.7 `[HIPÓTESIS]` |
| Deliberación pública sobre umbrales controvertidos | **Obligatoria**, con **participación plena y equitativa** en la toma de decisiones sobre biodiversidad y **acceso a la información** | Protección explícita de quien defiende el ecosistema | CBD, Meta 22 y Meta 21 (2022) `[VERIFICADO]` |
| Ventana de decisión del consejo `eco-` | **2 meses** de preaviso y **6 semanas** de documentos | 1 día completo de deliberación como mínimo; ≥ 4 días si se piden recomendaciones informadas | Documento 05 §5.2 (Q-6) · OCDE (2020), **heredado del informe de fuentes del documento 05** (`scratch/sdv_e/fuentes/05_representacion.md`); URL comprobada de nuevo (200) y listada en §14.9 `[VERIFICADO]` |
| Quórum `eco-` (N-de-M) | **`[SIN FUENTE VERIFICADA — pendiente de consenso científico]`**: el canon no publica N ni M para el Reino Natural. Regla de residuo: **sin M declarado, el consejo no puede decidir nada vinculante** y solo consiente el guardián | M declarado en la identidad de la unidad, **M ≥ 3** e impar, sin voto ponderado | Documento 05 §5.2 (Q-9) y §5.4 `[HIPÓTESIS]` |
| Procedimiento de disputa contra una decisión de umbral | **Obligatorio** y publicado (proceso accesible para identificar, oír y resolver quejas) | **90 días** como plazo máximo hasta el hito de decisión `[HIPÓTESIS]` (precedentes humanos publicados: 40, 60, ≤ 120 y 90 días) | Documento 05, Dimensión VII y su informe de fuentes (Banco Mundial, 2020; IUCN Green List v1.1, GLS-V1.1-1.2.4 — URL en §14.9) `[REPORTADO]` |
| Rotación del auditor externo | — | **No más de un ciclo consecutivo** | Documento 05 §7.4 `[HIPÓTESIS]` |

**Justificación.** El modelo está copiado de donde funciona y **no de donde se supone**: la revisión por
pares de un estándar científico intergubernamental tiene plazos publicados, un árbitro para los
desacuerdos mayores, un comité de conflicto de interés, la prohibición de que los autores toquen el texto
en la fase de aceptación y la obligación de publicar los comentarios y las respuestas `[VERIFICADO]`. La
razón de que este documento lo adopte tal cual, y no invente un proceso propio, es que **el Reino Natural
no tiene par auditor** (documento 09, I3): el auditor viene del reino que se beneficia del uso, y por eso
la **independencia del verificador es la única defensa estructural que existe**. De ahí las dos reglas
duras: el proponente no verifica, y el beneficiario no verifica.

**Protocolo.** **(1)** Toda propuesta se inscribe con proponente, clase, parámetro, fuente, ventana y
motivo; **(2)** pasa a revisión externa en dos rondas con los plazos de la tabla; **(3)** el órgano de
desempate resuelve los desacuerdos mayores **antes** de la aceptación; **(4)** si la materia es **LEY**
(el valor que la ciencia publica, su operador, su ventana), **no hay votación de contenido**: se adopta y
se publica; **(5)** si la materia es **POLÍTICA** (plenitud, trayectoria, plazos, catálogo de Zona Libre,
M y N del consejo), va a categoría `critical` con quórum 60 % y consenso 75 %, T13, anti-flip-flop de 14
días (precedente del Parlamento Educativo, INV2-EDU) —documento 05 §5.3—; **(6)** toda decisión publica
su postura minoritaria; **(7)** cualquier afectado puede abrir el procedimiento de disputa, con mediación
previa aceptada por las partes antes de escalar; **(8)** el acta queda en el registro T13 y **no se
borra**.

**Violación.** Constituyen violación de P3: **(a)** un umbral aprobado por su propio proponente;
**(b)** un verificador o un miembro de la comunidad testigo que se beneficia del uso que mide, sin
declararlo; **(c)** una decisión tomada sin quórum, sin preaviso o sin documentos; **(d)** una decisión
del consejo `eco-` tomada sin M declarado, o con voto ponderado; **(e)** **una votación sobre el piso del
SDV-E** (prohibición expresa: el piso es LEY); **(f)** la ausencia de procedimiento de disputa publicado,
o un guardián que sea juez de sus propias impugnaciones; **(g)** la disidencia científica borrada o
promediada en el acta.

### Dimensión P4: Trazabilidad, DOI y declaración de confianza (la cadena que no se puede saltar)

**Qué protege.** Que cada valor del estándar sea **rastreable hasta su fuente primaria** y **citable con
identificador persistente**; y que quien lo use sepa **cuánta confianza** merece.

| Parámetro | Mínimo Absoluto (el piso, LEY — no votable) | Óptimo (plenitud aspiracional, POLÍTICA — votable) | Fuente |
|---|---|---|---|
| Identificador persistente del producto | **DOI obligatorio** para el documento de umbral y para cada versión | Depósito en repositorio abierto con versión numerada | Cap. 9 §9.7 · IPBES (DOI sobre Zenodo, ej. `10.5281/zenodo.4147317`) `[VERIFICADO]` |
| Infraestructura de depósito y registro | **Repositorio abierto operado por una institución** (Zenodo, CERN) y **registro de DOI conforme a la norma ISO 26324** | Depósito con metadatos completos y política de preservación declarada | Zenodo `[VERIFICADO]` · DOI Foundation `[VERIFICADO]` |
| Cadena de trazabilidad de un hallazgo | **Tres saltos obligatorios**: resumen para decisores → resumen ejecutivo → sección del capítulo → **literatura primaria**, con marcas de anclaje por sección | Cuatro saltos cuando el dato viene de un dataset con su propio identificador | IPBES, *Traceability* `[VERIFICADO]` |
| Declaración de confianza del hallazgo | **Obligatoria**: modelo de cuatro cajas + relato trazable del **tipo, cantidad, calidad y consistencia** de la evidencia | Declaración de confianza publicada junto al valor en la tabla del estándar | IPBES, *Four-box confidence model* `[VERIFICADO]` |
| Cita de datos | **Obligatoria por dataset**, con su propio identificador y sus buenas prácticas de citación | Dataset citado en el acta de entrada del umbral | GBIF, *Citation guidelines* — **real, bloquea a los agentes automáticos (403)**: citable con advertencia `[REPORTADO]` |
| Marca de evidencia en cada cifra | **Obligatoria** en el texto del estándar: `[VERIFICADO]` · `[REPORTADO]` · `[HIPÓTESIS]` · `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` | Con el estado HTTP de la URL registrado y su fecha de comprobación | Brief de la rama §1.2 · `scripts/verificar_enlaces_sdv_e.py` (cuatro estados: `OK` · `BLOQUEADA` · `SIN_RESPUESTA` · `MUERTA`) `[VERIFICADO]` |
| Integridad del registro | **Hash SHA-256 por evento** (estándar NIST FIPS 180-4), con los campos concatenados y codificados en UTF-8 | Hash publicado y recalculable por un tercero desde datos públicos | `app/edu_bridge_bp.py` (columna `t13_hash`) `[VERIFICADO]` |
| Estado del umbral | **Uno de tres, declarado**: `CUANTIFICADO` · `CUALITATIVO (buena práctica)` · `SIN UMBRAL — en observación` | Estado revisado en cada ciclo y publicado con el umbral | Precedente: fronteras planetarias y OMS `[VERIFICADO]` · `[HIPÓTESIS]` en la formalización |
| Anuncio público del cambio de versión | **Obligatorio**: el estándar no se reescribe en silencio; cambia de número de versión y hay anuncio | Anuncio con la lista de criterios añadidos, no solo de números ajustados | IUCN RLE v2.0 (2024) `[VERIFICADO]` |

**Justificación.** La regla de los tres saltos no es un requisito bibliográfico: es la única forma de que
una afirmación del estándar pueda ser **refutada por quien la lee**. Si un umbral no llega hasta su
fuente primaria, no es un umbral: es una cita de una cita. Y la declaración de confianza es lo que
impide el uso abusivo del número: un valor con evidencia escasa y consistencia baja **no se usa igual**
que uno con revisión sistemática detrás. El detalle verificado que da fuerza a esta dimensión es que
**el estándar maduro declara lo que no sabe con la misma formalidad con que declara lo que sabe**: la
revisión 2023 de las fronteras planetarias publicó dos variables **sin umbral numérico** —aerosoles
(*«No global threshold defined, in the absence of sufficient knowledge»*) y entidades nuevas (*«0 to ?
(high threshold not defined)»*)—, y la OMS emite **declaraciones de buenas prácticas** cualitativas
cuando no hay evidencia cuantitativa `[VERIFICADO]`. El SDV-E adopta esa misma formalidad con el tercer
estado (`SIN UMBRAL — en observación`).

**Protocolo.** **(1)** Todo umbral se publica con DOI y con versión; **(2)** cada cifra de la tabla lleva
organismo, año, URL y estado HTTP registrado; **(3)** cada hallazgo que sostiene un umbral lleva su
declaración de confianza y su cadena de tres saltos; **(4)** cada acto del procedimiento —propuesta,
revisión, ratificación, revisión periódica, retiro— emite su registro con hash SHA-256; **(5)** el
registro **no se borra**, ni cuando la Capa de Ternura concede un perdón (T13: la ternura *«modula la
CONSECUENCIA, nunca la contabilidad»*) `[VERIFICADO en `maxocontracts/blocks/ternura.py`]`.

**Violación.** Constituyen violación de P4: **(a)** un umbral sin DOI ni versión; **(b)** una cifra sin
organismo ni año, o con URL cuyo estado no consta; **(c)** un hallazgo sin declaración de confianza;
**(d)** un dataset citado sin su identificador; **(e)** un cambio de versión del estándar sin anuncio
público; **(f)** un registro de decisión borrado o editado sin dejar el original.

**El hueco que esta dimensión declara.** La página del propio organismo internacional que enlaza el
**procedimiento escrito de depósito en Zenodo devuelve 404** en la sesión de verificación de esta rama:
el DOI está verificado **como práctica** (el ejemplo citado existe y responde) y **no como
procedimiento** `[VERIFICADO que el hueco existe]`. Este documento no rellena ese hueco con una
descripción plausible de un trámite que no pudo leer.

### Dimensión P5: Traducción a políticas (del piso científico a la norma, y su cláusula financiera)

**Qué protege.** Que el estándar **no se quede en doctrina**: que exista una cadena declarada desde el
umbral hasta la norma vinculante, con fechas, responsables y dinero.

| Parámetro | Mínimo Absoluto (el piso, LEY — no votable) | Óptimo (plenitud aspiracional, POLÍTICA — votable) | Fuente |
|---|---|---|---|
| Fecha de reporte | **Fijada de antemano y obligatoria** (precedente: **2026** y **2029**) — no se reporta «cuando se pueda» | Reporte anual voluntario adicional | CBD, Decisión 15/6 (2022) `[VERIFICADO]` |
| Revisión del progreso colectivo | **En reunión fijada** (precedente: **COP 17** y **COP 19**) | Revisión por pares **voluntaria** entre unidades o países (VPR), separada del reporte obligatorio | CBD, Decisión 15/6 (2022) · portal VPR `[VERIFICADO]` |
| Vía hacia la norma vinculante | **Declarada**: la directriz científica **no es vinculante por sí misma**; *«can be used as an evidence-informed reference tool to help decision-makers in setting legally binding standards»* | Acta de incorporación con plazo, responsable y autoridad competente `[HIPÓTESIS]` | OMS, 2021 `[VERIFICADO]` |
| Qué toca la política y qué no | **No toca el número**: la votación decide **la trayectoria y el plazo** (objetivos intermedios), no el nivel de la guía | Escalones intermedios con calendario decreciente y revisión pública | OMS, 2021 (arquitectura de tres niveles) `[VERIFICADO]` |
| Traducción a objetivos nacionales | **Obligatoria** la alineación de las estrategias y planes nacionales; articulación con los ODS de agua, ciudades, vida marina y vida terrestre | Planes con indicadores jerarquizados (de titular, de componente y complementarios) | CBD, Decisión 15/4 Meta 3 sección C · Decisión 15/5 `[VERIFICADO]` |
| Cláusula financiera | **Obligatoria**: un estándar sin cláusula financiera no se traduce a política. Precedente verificado: **≥ 500 000 M USD/año** de incentivos perjudiciales eliminados o reformados (Meta 18) y **≥ 200 000 M USD/año** movilizados, de los cuales **≥ 30 000 M USD/año internacionales para 2030** (y ≥ 20 000 M USD/año para 2025) (Meta 19) | Financiación de la restauración **por encima del piso** (nunca para comprar el derecho a estar por debajo) | CBD, Decisión 15/4, cifras verificadas en el documento 08 §4.1 y en la nota de orientación de la Meta 19 `[VERIFICADO]` |
| Herramientas de auditoría y certificación | **Declaradas** (el canon las exige: estándares de certificación y herramientas de auditoría) | Certificación con evaluador externo, revisor imparcial y renovación quinquenal | Cap. 9 §9.7 · IUCN Green List v1.1 (2017), **heredada del informe de fuentes del documento 05** (URL en §14.9) `[REPORTADO]` |
| Incorporación al derecho nacional | **`[SIN FUENTE VERIFICADA — pendiente de consenso científico]`**: no se encontró, en ninguna fuente leída, el procedimiento concreto por el que un umbral científico se convierte en norma jurídica vinculante, ni cuánto tarda, ni quién lo puede bloquear | Propuesta no ratificada: acta de incorporación con plazo máximo y responsable identificado | Hueco declarado en el informe de fuentes de esta rama §V8 |

**Justificación.** La cadena verificada es larga y tiene tres cosas que sí se pueden copiar sin inventar:
**(1)** la fecha de reporte está fijada de antemano; **(2)** la revisión por pares entre iguales es
**voluntaria y separada** del reporte obligatorio —dos niveles de escrutinio, el que se exige y el que se
ofrece—; **(3)** la traducción a política **incluye el dinero** `[VERIFICADO]`. La tercera es la que más
se olvida y la que decide si el estándar es real: una meta sin partida presupuestaria es una meta
declarativa. Y la precisión doctrinal que esta dimensión aporta, tomada del precedente de la directriz de
aire, es que **la votación no toca el número**: la guía científica fija el nivel y el cuerpo político
decide la trayectoria y el calendario para alcanzarlo. Eso es exactamente la separación LEY/POLÍTICA del
Cap. 9 §9.7, y su formulación verificada: *«guidelines are not legally binding recommendations, they can
be used as an evidence-informed reference tool to help decision-makers in setting legally binding
standards»* (OMS, 2021) `[VERIFICADO]`.

**Protocolo.** **(1)** Cada umbral entra con su acta de incorporación prevista: autoridad competente,
plazo y responsable; **(2)** la política fija los **escalones intermedios** con calendario, nunca el nivel
de la guía; **(3)** el reporte se entrega en la fecha fijada, con los indicadores acordados; **(4)** la
revisión global ocurre en la reunión fijada, no en la que convenga; **(5)** la cláusula financiera se
declara con su cifra y su año.

**Violación.** Constituyen violación de P5: **(a)** un umbral declarado «ley» sin acta de incorporación
ni autoridad competente identificada; **(b)** una política que **baja** el piso o que lo aplaza sin
trayectoria declarada; **(c)** una fecha de reporte incumplida; **(d)** una meta sin cláusula financiera;
**(e)** el uso del crédito regenerativo o de un pago como sustituto del cumplimiento del piso.

### 4.6 Lo que estas cinco dimensiones NO son

- **No son un índice ponderado.** Su piso es **binario** (presencia o ausencia del acto, del documento o
  del registro). Pesar la calidad de un procedimiento produciría el efecto perverso que el documento 05
  §4.1 ya advirtió: procesos «casi legítimos» que consienten «un poco».
- **No evalúan al ecosistema.** Evalúan al **procedimiento** que fija y revisa sus umbrales. Una unidad
  sana gobernada por un procedimiento violado viola este bloque; una unidad degradada con procedimiento
  impecable no lo viola — lo que viola es su SDV-E, y lo juzga INV2-E.
- **No sustituyen a los documentos 02, 05 ni 06.** La unidad, la voz y el sensor son precondiciones: si
  fallan, este bloque no tiene sobre qué operar.
- **No son votables en su piso.** Ver §5.2.

---

## 5. Fórmula de violación, pesos y umbrales

### 5.1 La fórmula de este bloque es una conjunción, no un promedio

En los documentos 07 y 10-23 la violación del SDV-E es un **déficit normalizado**
(`déficit = (requerido − actual) / requerido`) con un factor que vale **exactamente 1.0 cuando la
violación es 0** (base neutra; el SDV-S tuvo que corregir `FS_S = 1.0 + e^v` a `FS_S = e^v` porque la
primera versión recargaba el 100 % incluso sin violación) [VERIFICADO en `maxocontracts/core/types.py`].
**Aquí no hay déficit que promediar**: un procedimiento se cumple o no se cumple.

```
A(i) ∈ {0, 1}   para i = P1 … P5          (las cinco dimensiones de §4)
Admisible  ⇔  ∏ A(i) = 1                   (conjunción: todas, no el promedio)
Sin violación → ningún recargo            (base neutra exacta 1,0)
Si no Admisible → el umbral NO entra o NO se ratifica (BLOQUEA)
```

Tres consecuencias que conviene escribir: **(a)** un procedimiento con cuatro dimensiones en 1 y una en
0 es **inadmisible**, y la que suele fallar es la que protege (P1 sin fuente o P3 sin verificador
independiente); **(b)** **no hay pesos** en este bloque, y por tanto no hay forma de compensar una
dimensión con otra; **(c)** la base neutra es exacta: **cumplir el procedimiento no tiene recargo**. Y una
precisión de forma que este documento hereda del vecino: **aquí no se escribe un factor propio** —el
documento 03 §5.2 declara que su contador «es una **compuerta**, no un factor»—, porque una compuerta que
valiera 1,0 en todos los casos sería un nombre sin función. Es
la misma estructura que el documento 05 §5.1 fijó para la representación, aplicada ahora al proceso.

### 5.2 La frontera LEY/POLÍTICA, aplicada al proceso entero

Esta es la tabla central del documento, y su criterio es uno solo: **LEY es lo que el diseño biológico
ya decidió y ningún voto puede tocar; POLÍTICA es lo que no tiene dato y por eso se delibera.**

| Materia | **LEY — no votable** | **POLÍTICA — votable (categoría `critical`)** |
|---|---|---|
| **El piso (Mínimo Absoluto)** | El valor que la ciencia publica, con organismo y año; **no se vota, se adopta**. Y **no existe** si no hay fuente | — |
| **La plenitud (Óptimo)** | — | La plenitud aspiracional de cada unidad: **se vota** (el Óptimo del SDV-E no se investiga: se vota, porque la ciencia publica pisos de riesgo, no plenitudes) |
| **Existencia del piso en el motor** | Que el piso viva en el motor y en un `CHECK` de base de datos, y que **una votación no pueda bajarlo**: un voto por debajo del piso es **nulo** | El valor votable **acotado por abajo** por el piso, y su calendario |
| **Operador y ventana de medición** | El operador (`min`/`max`/`range`/`escalonado`) y la ventana los fija la fuente del umbral; **no se votan** | La frecuencia de **reporte** y de **auditoría** (que no es la de medición) |
| **Consecuencia del cruce** | Registro de violación y **bloqueo** (INV2-E); el bloqueo es inmediato, no espera ciclos | La **escalada** a retractación y su contador (`max_consecutive_cycles`: **sin valor por defecto**, es POLÍTICA) |
| **Ciclo de revisión** | Que exista calendario, acta y estado declarado; el retiro por error es **inmediato** y el retiro por mejora exige **5 años** de evidencia contraria | El valor concreto **dentro** del rango canónico de valores (3, 4 o 5 años —el rango **3-5 años es LEY**, canon del proyecto; el valor que se elija dentro de él es lo votable—) y el ciclo de la arquitectura (**8-10 años**, `[HIPÓTESIS]`, votable porque no tiene fuente externa) |
| **Trazabilidad** | DOI obligatorio, tres saltos, declaración de confianza, hash por evento, registro que no se borra | El repositorio de depósito y el formato del acta |
| **Zona Libre** | Que exista y que **no se pondere** (una violación de Zona Libre sí produce violación; su cuantificación está prohibida) | **Qué entra en el catálogo** de lo inefable de cada unidad, **con carga de la prueba sobre quien declara** |
| **Quórum `eco-`** | Que el silencio no consienta; que el guardián no vote el piso; que se prohíba el voto ponderado | **N y M** del consejo, los plazos de disputa y quién compone la comunidad de custodia |
| **Retractación** | Que el objeto de la retractación sea **el contrato o la actividad humana, nunca la unidad ecológica** | La forma del procedimiento y sus plazos |
| **Traducción a políticas** | Que la guía científica no sea vinculante por sí misma y que la política **no toque el número**, solo la trayectoria; la cláusula financiera | El calendario de los escalones intermedios y la autoridad competente |
| **Compensación** | La prohibición de compensar la violación con crédito regenerativo, con dinero o con mayoría | El destino del excedente **por encima** del piso (restauración, prioridades) |
| **Pesos e intensidades** | Que la tabla de pesos sea constante en ejecución y se **hashee** en cada validación; que ninguna dimensión sin piso tenga peso en el vector del piso | La tabla de pesos definitiva, los niveles del factor de intensidad y `V_max` |

**Cómo se vota, y qué está verificado en el repositorio hoy** (no es una promesa: es el mecanismo que ya
existe para otras ramas del proyecto, y que este bloque **propone reutilizar**):

| Pieza del mecanismo de POLÍTICA | Estado | Evidencia |
|---|---|---|
| Categoría `critical`: **quórum 60 %**, **consenso 75 %** | 🟢 **existe** | `app/voting_bp.py`, `CATEGORY_DEFAULTS = {"critical": {"quorum": 0.60, "majority": 0.75}}` `[VERIFICADO]` |
| Un voto por persona y registro inmutable (T13), con la voz ponderada por TVI invertido | 🟢 **existe** | `app/voting_bp.py` (Participación Inteligente; el quórum sigue siendo de personas) `[VERIFICADO]` |
| Guardia de escalera de confianza: quien no ha caminado su primer acuerdo **no propone** | 🟢 **existe** | `app/voting_bp.py`, `_trust_level_guard` (nivel ≥ 1) `[VERIFICADO]` |
| **Anti-flip-flop de 14 días** entre dos cambios del umbral | 🟡 **existe, cableado solo al umbral educativo** | `EDU_COOLDOWN_DAYS = 14`; el rechazo `EDU_COOLDOWN` solo opera en el circuito educativo `[VERIFICADO]` |
| **`CHECK` en base de datos** del parámetro votable | 🟡 **existe para el umbral educativo** (`umbral_anios >= 12.0` y `<= 30.0`); no existe un `CHECK` de categoría para parámetros ecológicos | `app/schema.sql`, tabla `edu_parameters` `[VERIFICADO]` |
| **Rechazo del voto que baja el piso** | 🟢 **existe el patrón**: el validador devuelve `PARAM_AXIOM_VIOLATION` si el umbral queda por debajo de la ley (≥ 12 años, INV2-EDU) | `app/voting_bp.py`, `_validate_edu_umbral_params` `[VERIFICADO]` |
| Circuito vinculante para parámetros del **Reino Natural** | 🔴 **no existe**: los únicos dos tipos de acción vinculante son `set_vhv_params` y `set_edu_umbral` | `app/voting_bp.py` (aplicadores de `action_json`) `[VERIFICADO]` |

**El patrón que este documento propone copiar, y que ya está probado en otra rama:** la ley **vive en el
motor** y el voto está **acotado por abajo** por ella, con doble candado —validación de la propuesta y
`CHECK` de base de datos—. Para el SDV-E eso significa: **(1)** el Mínimo Absoluto de cada parámetro vive
en el tipo del motor (documento 08 §8.8) y **no es un campo votable**; **(2)** el valor sujeto a votación
—la plenitud, la trayectoria, el contador de escalada— tiene **cota inferior igual al piso**, y un voto
por debajo **no se admite a trámite**; **(3)** un voto que consiguiera bajar un piso ya vigente sería
**nulo**, no derogatorio. `[HIPÓTESIS]` en su forma exacta; el principio es canon (el piso es LEY,
precedente INV2-EDU).

### 5.3 Los tres estados de un umbral (y por qué no dos)

Un umbral maduro no está «vigente» o «derogado»: está en uno de **tres estados**, y el tercero es una
aportación de este documento, con precedente verificado:

| Estado | Condición | Consecuencia |
|---|---|---|
| `CUANTIFICADO` | Existe valor publicado con organismo y año, operador y ventana | Entra al motor con peso en el vector del piso |
| `CUALITATIVO (buena práctica)` | No hay número suficiente, pero hay criterio cualitativo publicado (precedente: declaraciones de buenas prácticas de la OMS) | Entra como **dimensión binaria auditable sin peso** (precedente Cap. 8 §8.11) |
| `SIN UMBRAL — en observación` | Se buscó el número y no existe fuente verificable (precedente: aerosoles y entidades nuevas en las fronteras planetarias) | **No entra con peso**; se publica el hueco; opera T14 (bloqueo precautorio ante acción irreversible) |

La razón de que el tercer estado sea obligatorio y no un descargo de responsabilidad: **un peso asignado
a una dimensión sin piso no la mide, la diluye** —reduce el déficit de las que sí se miden— (documento 08
§4.2). Y la razón de que **el estado por defecto del SDV-E hoy sea `indeterminado`** es la misma, un
escalón más arriba: sin sensores y sin circuitos de gobernanza, ninguna unidad puede declararse por
encima de su suelo.

### 5.4 Escala de lectura del procedimiento

| Banda | Condición | Lectura |
|---|---|---|
| **Admisible** | `∏ A(P1…P5) = 1` | el umbral puede entrar, permanecer y ser citado |
| **Inadmisible** | una sola dimensión en 0 | el umbral **no entra** o queda en `SIN UMBRAL — en observación` |
| **Indeterminado** | falta el acto que acredita una dimensión (sin grupo, sin revisión vencida, sin DOI) | **no sanciona al ecosistema** y **no habilita crédito**; obliga a instrumentar y a registrar la ausencia |

---

## 6. Protocolo de medición (qué se mide en este bloque, quién reporta y qué se firma)

**Lo que se mide aquí no es el ecosistema: es el procedimiento.** La medición ecológica es del documento
06; este bloque mide **actos**: una propuesta, una revisión, una ratificación, una revisión periódica, un
retiro. Cada acto tiene fecha, autor, motivo y evidencia, y ninguno se presume.

### 6.1 Admisibilidad de un acto de procedimiento

Un acto entra al registro **solo si** trae los campos siguientes. Es la traducción al procedimiento del
expediente mínimo de una medición (documento 06 §6.6), y su ausencia produce estado `Indeterminado`, no
violación:

| Campo | Para qué | Axioma |
|---|---|---|
| `acto` + `tipo` | qué se hizo: propuesta, revisión, ratificación, revisión periódica, retiro | — |
| `clase_efg` + `nivel_4_6` | a qué clase de unidad afecta | documento 02 §4-C2 |
| `parametro` + `operador` + `unidad` + `ventana` | el objeto exacto del acto, sin conversiones implícitas | documento 07 §3.3 |
| `fuente` + `organismo` + `anio` + `url_estado` | procedencia verificable del valor | T13 |
| `ta_periodo_inicio` + `ta_periodo_fin` (**TA**) | la ventana temporal del acto; sin ventana, no es comparable (y **jamás** en TVI ni TPI) | T7 (Cap. 5) · Cap. 16.5 §16.5.14 |
| `decision_que_informa` | qué decisión concreta sobre la unidad cambia este acto | documento 06 §6.6 |
| `evidencia_ref` | identificador del registro original (acta, informe, escena, dataset) | T13 |
| `hash` (SHA-256) | integridad del registro; recalculable por un tercero | NIST FIPS 180-4 · `app/edu_bridge_bp.py` `[VERIFICADO]` |

### 6.2 Quién reporta en este bloque

| Reporta | Qué reporta, exactamente | Respaldo |
|---|---|---|
| **El proponente** | La propuesta con su fuente, su clase, su ventana y su `decision_que_informa` | Documento 06 §6.6 |
| **El grupo de trabajo de la clase** | El borrador del umbral y su informe de estado | Cap. 9 §9.7 (adaptado) |
| **Los revisores externos** | Los comentarios por sección y su declaración de confianza | IPBES `[VERIFICADO]` |
| **El órgano de aceptación** | El acta de aceptación con la postura minoritaria | IPBES `[VERIFICADO]` |
| **La parte `eco-` (custodio)** | La **declaración**: régimen de ciclos, línea base, área de referencia, protocolo de campo | Canon: los 7 campos de identidad |
| **La comunidad testigo** | Lo que la serie no recoge, la impugnación de la declaración, la continuidad de la custodia y la no interferencia del instrumento | Documento 06 §7.6 |
| **El verificador de enlaces y el auditor estructural** | El estado HTTP real de cada fuente y el cumplimiento de la plantilla del estándar | `scripts/verificar_enlaces_sdv_e.py` · `tests/test_sdv_e_biblioteca.py` `[VERIFICADO]` |

### 6.3 Las cuatro frecuencias que no se funden

El documento 06 §6.4(c) fija cuatro frecuencias distintas y este bloque las adopta sin mezclarlas:

| Frecuencia | Cadencia | De dónde sale |
|---|---|---|
| **De medición** | la del instrumento (5 / 8 / 10 / 16 días; anual; por evento) | la física y la fuente |
| **De reporte** | **una vez por ciclo ecológico dominante de la unidad**, más los eventos | `[HIPÓTESIS]`; sin fuente externa |
| **De auditoría** | **por ciclo, con muestreo declarado**: se audita una fracción, no todo | `[HIPÓTESIS]`; auditar todo es tan imposible como medirlo todo |
| **De revisión del umbral** | **3-5 años** (valores) y **8-10 años** (arquitectura); retiro: 5 años de evidencia contraria o inmediato si hay error | Cap. 9 §9.7 (canon) · IUCN/COSEWIC `[VERIFICADO]` |

**La regla que gobierna las cuatro:** *la frecuencia declarada no puede ser mayor que la resolución
temporal del sensor que la sostiene, ni mayor que el tiempo de respuesta del indicador*. **Declarar una
frecuencia más fina que la del instrumento es la forma técnica de inventar el dato** (documento 06
§6.4b). Y su consecuencia para este bloque: **una revisión de umbral no puede anunciarse antes de que
exista la serie que la sostiene**.

### 6.4 Continuidad instrumental aplicada al procedimiento

Un cambio de sensor, de constelación, de método o de versión de procesamiento **obliga a** declararlo con
fecha y motivo, **re-declarar la línea base** si no es comparable, **no cambiar de instrumento mientras
exista una violación abierta** de esa dimensión, y registrar el **periodo de solape** si existe
(documento 06 §6.7) `[HIPÓTESIS]`. La razón, que también vale para los umbrales: **cambiar de sensor es
la forma más barata de cambiar el resultado sin tocar el territorio**, y cambiar de revisión es la forma
más barata de cambiar el umbral sin tocar la ciencia.

---

## 7. Verificación y auditoría (T13, guardián, comunidad testigo)

### 7.1 El protocolo de revisión por pares, con plazos verificados

Es el modelo más completo y cuantificado que existe para un estándar científico intergubernamental, y sus
plazos son copiables tal cual `[VERIFICADO]`:

| Fase | Producto | Quién revisa | Duración / plazo |
|---|---|---|---|
| 1 | Esquema anotado, autores identificados y necesidades de datos | Equipo de autores + panel multidisciplinario experto | hasta la primera reunión de autores |
| 2 | Borrador de orden cero → revisión interna → **borrador de primer orden** | Interna, con participación del panel | — |
| 2b | **Primera revisión externa por pares** | Expertos registrados (propuestos también por autores y secretaría) | **6-8 semanas** |
| 3 | **Borrador de segundo orden** + primer borrador del resumen para decisores | Segunda reunión de autores | — |
| 3b | **Segunda revisión externa** (informe y resumen a la vez) | Gobiernos (comentarios integrados por punto focal) y expertos | **8 semanas** |
| 4 | Borrador final + resumen para decisores | Tercera reunión de autores; comentarios de gobiernos hasta **2 semanas antes** del órgano de aceptación | entrega **12 semanas** antes |
| 5 | **Aceptación** | El órgano de aceptación: **los autores no cambian el texto en esa fase** | — |

Y las reglas de oro del proceso, todas verificadas y todas adoptadas: **la disidencia científica se
documenta, no se promedia ni se borra**; **los comentarios de revisión y las respuestas de los autores se
publican en línea** después de la aceptación; **la separación autor/árbitro es un invariante**; existe un
**órgano de desempate** para las áreas de desacuerdo mayor; y existe **comité de conflicto de interés**
`[VERIFICADO]`.

### 7.2 La escalera de verificación en tres grados

Ningún grado se sustituye por otro (documento 05 §7.2):

| Grado | Quién | Qué verifica |
|---|---|---|
| **1 — Autodeclaración documental** | La parte, por medio de su creador o su comunidad | Que los siete documentos existen y son públicos |
| **2 — Comunidad testigo** | Comunidad de custodia + ciencia ciudadana + fuentes independientes | Que lo declarado **ocurre**: gobernanza de facto, territorio real, fuentes reales |
| **3 — Verificación externa** | Evaluador ajeno a la unidad + revisor imparcial | Los siete campos y las dimensiones del estándar, con **renovación a 5 años** |

Un sistema que aceptara la autodeclaración como verificación tendría exactamente el problema que describe
el riesgo **R4**. Y una advertencia honesta sobre los grados 2 y 3: **los tres linajes de observación
ciudadana y de testigos tienen como validador a la misma comunidad que produce el dato** —es un control
de calidad con regla calificada (acuerdo > 2/3), y **no es auditoría independiente**—; hoy **solo el
linaje satelital tiene auditor externo verificado y prueba documentada** (documento 06 §7.3)
`[VERIFICADO]`.

### 7.3 El guardián, y lo que no puede hacer en este bloque

El guardián oráculo **consiente, no mide** (`app/contracts_bp.py`: *«Ecosistemas (eco-*): consentimiento
otorgado por el guardián oráculo»*; Cap. 16.5 §16.5.14). En materia de procesos eso significa cuatro
prohibiciones que este documento fija: **(1)** no puede fijar, bajar ni interpretar el piso; **(2)** no
puede producir la medición que lo juzga; **(3)** no puede ser el verificador de un umbral que él propuso;
**(4)** no puede ser designado, invocado ni financiado por la parte beneficiada. Su heurística es
declaradamente laxa cuando falta la clave del oráculo en vivo (**R13**: aprueba si los invariantes pasan)
`[VERIFICADO en el test del guardián]`, y por eso **el piso no se delega al guardián**: se calcula desde
mediciones admisibles (documento 08, Regla 6).

### 7.4 La comunidad testigo, y su composición mínima

Sus cuatro funciones, ninguna decorativa: **detectar lo que la serie no recoge** (una carretera, un
drenaje, una extracción nocturna, una «restauración» fotogénica); **impugnar la declaración** (régimen de
ciclos, línea base, cambio de protocolo); **testificar la continuidad** de la custodia; y **verificar la
no interferencia** del propio instrumento (documento 06 §7.6). Composición mínima `[HIPÓTESIS]`:
**al menos un miembro que no se beneficie del uso que se mide**. Sin esa condición, la auditoría social es
una firma más del propio beneficiario.

### 7.5 Los riesgos abiertos, y uno nuevo

| ID | Riesgo | Cómo lo trata este bloque |
|---|---|---|
| **R4** | Partes fantasma: cualquiera crea un `eco-*` sin autoridad sobre la entidad | **No lo cierra.** El procedimiento de P3 exige los siete campos y el estado `R`, pero la autoridad verificable sigue siendo el hueco que el documento 02 §4-C5 declara |
| **R6** | T9/T17 (Reciprocidad Justa) no se valida en la creación: pasa un contrato unilateral | **No lo cierra.** Es la defensa que falta; el bloqueo por piso medido es la que este estándar propone |
| **R13** | Guardián `eco` con heurística laxa | **Lo acota**: el guardián consiente, no mide ni verifica umbrales, y su aprobación **no puede fabricar un piso cumplido** |
| **Nuevo — captura del instrumento** `[HIPÓTESIS]` | El mismo actor que degrada instala, financia o elige el instrumento que lo mide | Tres candados: regla del no-beneficiario en la titularidad del instrumento y en la comunidad testigo; calibración por un tercero declarado; **obligación de declarar el financiador** de cada serie |
| **Nuevo — captura del verificador** | Varias perspectivas comparten el mismo error (confabulación de validadores) | Diversidad real de proveedores, fuentes e implementaciones; **disenso registrado** (T12: la disidencia no es desperdicio); **rotación del auditor** (no más de un ciclo consecutivo) |

### 7.6 El límite de T13, aplicado al proceso

Se publica **el cálculo, no la intimidad del sujeto**: del ecosistema se publican el parámetro, el valor,
la unidad, la ventana, el método, la incertidumbre y el hash; **no** se publica ni se infiere una
interpretación de su «estado interior», que es el «milagro» que el canon prohíbe medir (Cap. 16.5
§16.5.14). Y una regla operativa que este bloque adopta literalmente del documento 06 §7.4: **lo que no
cambia una decisión que afecta a otros, no se mide** — si un dato no puede modificar ninguna decisión
sobre la unidad, producir ese dato es **vigilancia, no transparencia**.

---

## 8. Invariante INV2-E: de estándar a contrato ejecutable

La especificación completa es el [documento 08](08_INV2-E_invariante.md). Aquí se enumeran **exactamente
las piezas que el bloque de procesos le entrega**, para que la interfaz entre los dos documentos sea
verificable:

| Pieza que INV2-E consume del proceso | De dónde sale | Estado |
|---|---|---|
| El **piso** de cada parámetro, con fuente y ventana | §4-P1, §5.2 | 🟡 especificado; **sin fuente para 6 de 8 dimensiones canónicas** |
| La **prohibición de votar el piso** (un voto que lo baje es nulo) | §5.2 | 🟡 especificado; patrón verificado en otra rama (`PARAM_AXIOM_VIOLATION` + `CHECK`), **no aplicado al Reino Natural** |
| La **`unidad_de_ciclo_ta`** obligatoria y **sin valor por defecto** | §2 Regla 6, §4-P2 | 🔴 **la unidad no está decidida** (documento 07 §13, pregunta 3) |
| El **`max_consecutive_cycles`** como POLÍTICA sin default | §4-P2, §5.2 | 🔴 no existe; es votable y hoy no hay circuito `eco-` donde votarlo |
| El **objeto de la retractación** (contrato o actividad, nunca la unidad) | §5.2 | 🟡 especificado en el documento 08 §8.7 |
| Las **dos vías de bloqueo** (piso medido y precautoria T14) | §4-P3, §5.3 | 🟡 especificado; la precautoria es la única defensa de las dimensiones sin umbral |
| La **cobertura declarada** del piso | §5.3 | 🔴 cifra **en disputa** entre los documentos 07 (0,925) y 08 (0,680): este documento **no la elige** (§13) |
| La **Zona Libre** como dimensión binaria sin peso, con su catálogo votable | §5.2 | 🟡 especificado; el perímetro del catálogo es decisión no ratificada |

**Lo que el proceso no puede entregar, y no entrega:** no decide el bloqueo —eso es `is_valid`—, no
convierte un `FE` pequeño en autorización, y **no convierte una aprobación en medición**. Un procedimiento
impecable sobre una unidad sin sensores produce `indeterminado`, y el estado por defecto del SDV-E hoy es
`indeterminado`, no `cumple` (documento 08 §8.4).

**Y la regla que unifica las dos capas:** **el piso vive en el motor, la plenitud vive en la votación.**
El motor no sabe votar y la votación no sabe medir; la frontera entre ambos es la única pieza de este
bloque que puede implementarse **antes** de que existan los sensores —que es exactamente el orden que el
canon fijó: *«estándar primero, contabilidad después»* (Cap. 16.5 §16.5.14).

---

## 9. El suelo antes que el saldo (no compensación)

La regla es canónica y este bloque la traduce a gobernanza: *«Un conjunto con crédito regenerativo
acumulado pero humedal bajo su SDV-E no está en coherencia: **INV2-E será su juez**»* (Cap. 16.5
§16.5.14).

**Tres cosas que no compran el piso, y una que sí compra algo.**

| No compra el piso | Por qué |
|---|---|
| **El crédito regenerativo** | No entra en la ecuación del piso: no lo reduce, no lo compensa, no lo aplaza, no reinicia el contador (documento 08 §8.3, propiedad **P3**; su forma ejecutable, en §9.2). Cuando la unidad está bajo su piso, su crédito queda **en cuarentena afectado a la restauración de esa misma unidad**: no se destruye (T13), no se transfiere a otro territorio y no se acredita como logro |
| **La mayoría** | El piso es LEY y no se vota (§5.2). Una votación no cambia un hecho medido: un caudal por debajo del mínimo no se recupera porque una mayoría lo declare admisible |
| **El dinero de la restauración** | Financia la restauración **por encima** del piso; no compra el derecho a estar por debajo |
| **Sí compra: el crédito financia la restauración** | Una vez cumplido el piso y con cobertura completa, el crédito acumulado se afecta a restaurar la misma unidad. Es la única cosa que el saldo puede hacer, y es valiosa |

**Y la consecuencia doctrinal que este bloque hereda y refuerza:** el SDV-E es el primer estándar de la
familia en el que **la prevención es el remedio completo** (documento 09, I11). En los otros tres reinos,
violar tiene consecuencias *y* reparación; aquí, violar solo tiene consecuencias, porque el tiempo del
bosque no se compra de vuelta: *«Un bosque tarda 100 años en crecer; ese es su costo en TA. La economía
no puede acelerar esto sin destruir valor»* (Cap. 5 §5.5). Por eso **el procedimiento tiene que ser
preventivo**: la carga de la prueba recae sobre quien propone, y el bloqueo es inmediato, no al séptimo
ciclo.

---

## 10. Zona Libre: lo que NO se mide

*«Parte del valor del humedal es inefable (Cap. 7 §7.9). Los sensores miden salud (agua, cobertura,
biodiversidad indicadora); jamás "milagros". Medir todo sería la forma técnica de dejar de escucharlo»*
(Cap. 16.5 §16.5.14). Traducido a un documento de procesos, la Zona Libre impone **cuatro límites al
procedimiento**:

1. **Un límite a lo que se vota.** El catálogo de lo inefable de cada unidad **se vota** (POLÍTICA,
   categoría `critical`), pero **con carga de la prueba sobre quien declara**: sin ella, «declarar
   inefable» sería la vía más barata para vaciar el estándar, y el procedimiento estaría blindando con
   la palabra «inefable» lo que solo es incómodo de medir.
2. **Un límite a lo que se pondera.** Que exista Zona Libre y que **no se pondere** es LEY: no entra
   jamás en el numerador de la fórmula, y su violación se documenta sin cuantificarse (precedente
   canónico: las dimensiones binarias sin peso, Cap. 8 §8.11).
3. **Un límite a lo que se mide.** La regla de la **métrica enemiga**: un indicador que sube con la poda,
   con el riego ornamental o con el cierre del acceso para la fotografía **se retira del elenco**, aunque
   funcione; el criterio de retiro es objetivo —**sube sin que suba ningún parámetro con piso del mismo
   linaje**— (documento 06 §7.4).
4. **Un límite al propio auditor.** El contador de asimetría (parámetros medidos en la unidad frente a
   parámetros declarados por quien la afecta) es el indicador de colonización del TA; su umbral **ya está
   publicado** en el [documento 03](03_No_colonizacion_del_TA.md) §5.3 —`CNC = 0` exacto, con base neutra
   1,0 en §5.2 y cláusula de no vacuidad en §5.4— y **lo que no existe es su implementación**, no el umbral
   (documento 06 §7.4).

**Lo que la Zona Libre prohíbe a este bloque en una frase:** un procedimiento perfectamente auditado
**no** es una descripción completa de la unidad ecológica, y presentarlo como tal sería el error que la
Zona Libre existe para impedir.

---

## 11. Comparativa inter-reinos (SDV-H · SDV-A · SDV-E · SDV-S)

La comparación completa de los cuatro estándares es el [documento 09](09_Comparativa_inter_reinos.md).
Lo pertinente aquí es **cómo nace y cómo muere un umbral en cada reino** —una comparación que ninguna
tabla del canon hace—:

| Eje del proceso | **SDV-H** (humanos) | **SDV-A** (animales) | **SDV-E** (ecosistemas) | **SDV-S** (sintéticos) |
|---|---|---|---|---|
| **Unidad del proceso** | La persona; parámetros universales + adaptaciones regionales | **La especie** (*«grupos de trabajo por especie»*) | **La clase** (EFG / nivel 4-6) que se instancia en la **unidad** | La instancia sintética |
| **Quién redacta** | Instrumentos estandarizados por dimensión | Investigadores + etólogos + organizaciones de bienestar | Grupo por clase con **dos voces**: técnica y de custodia | El propio reino, con auditoría cruzada |
| **Ciclo de revisión** | 🔴 no verificado en esta rama | **3-5 años** (canon) | **3-5 años** (valores) y **8-10 años** (arquitectura) `[HIPÓTESIS]` | 🔴 no declarado; la retractación es por **7 ciclos consecutivos** |
| **Validación** | Auditoría independiente y organismos sin conflicto (Cap. 8 §8.6) | Revisión por pares + repositorios abiertos + DOI (Cap. 9 §9.7) | **Dos rondas externas** (6-8 y 8 semanas) + órgano de desempate + comité de conflicto `[VERIFICADO]` | Auditoría cruzada por un par sintético (**AOS**) |
| **Quién audita** | Auditor independiente | Entidad certificadora sin conflicto | 🔴 **nadie del propio reino**: ciencia, teledetección y comunidad testigo | Un par del propio reino |
| **Cómo se retira** | 🔴 no verificado en esta rama | 🔴 no verificado en esta rama | **Error: inmediato. Mejora: 5 años de evidencia contraria.** Fin de identidad: el ciclo de la unidad | Retractación tras el contador de ciclos |
| **Moneda temporal del proceso** | **TVI** | **TA**, traducido por el PIU | **TA**, traducido por el PIU | **TPI** |
| **Base neutra** | n/a (suma) | 🔴 no neutra por diseño (0,2 con cumplimiento pleno) | **1,0 exacto exigido** | 🟢 1,0 exacto |

**Tres lecturas que solo se ven en esta tabla.**

1. **El canon del proceso está escrito para el SDV-A, y este documento lo hereda declarándolo.** Los
   «ciclos de revisión cada 3-5 años», la revisión por pares, el DOI y la deliberación democrática son
   **literales del Cap. 9 §9.7**, que es el bloque de los animales. El SDV-E no inventa su procedimiento:
   **lo adapta**, cambiando la unidad (de especie a clase + unidad) y añadiendo lo que su sujeto exige
   —verificación externa obligatoria, porque no tiene par auditor—.
2. **El SDV-E es el único cuyo procedimiento debe vérselas con un sujeto que no puede proponer.** En los
   otros tres reinos, el sujeto (o su tutor, o su propia instancia) puede iniciar el proceso. Aquí, quien
   propone **siempre** pertenece al reino que se beneficia del uso, y esa es la razón de que la regla del
   no-beneficiario y los tres grados de verificación no sean un lujo: son la única sustitución posible de
   la voz ausente.
3. **El contador del SDV-S no se hereda.** Los **7 ciclos** del reino sintético se cuentan en **TPI**
   (horas de proceso); en el SDV-E el ciclo es **TA**. Copiar el 7 serían, en el mejor de los casos,
   siete años de tolerancia contra T14 (documento 08 §8.6). El mecanismo se replica; **el número no**.

---

## 12. Estado de implementación

Verificado por lectura directa del repositorio y de la suite en octubre de 2026. **La regla de honestidad
de esta sección: está prohibido afirmar que existe algo que no tiene código y test.**

### 12.1 Lo que sí existe (y es honesto decir que existe)

| Pieza | Dónde | Estado |
|---|---|---|
| Motor de propuestas con categoría, quórum y mayoría por categoría | `app/voting_bp.py` (`CATEGORY_DEFAULTS`) | 🟢 **existe**: `critical` = quórum **0,60** y consenso **0,75** |
| Un voto por persona, registro inmutable, voz ponderada por TVI | `app/voting_bp.py` | 🟢 **existe** |
| Guardia de escalera de confianza para proponer (nivel ≥ 1) | `app/voting_bp.py` (`_trust_level_guard`) | 🟢 **existe** |
| Rechazo axiomático de un valor por debajo de la ley del motor | `app/voting_bp.py` (`_validate_edu_umbral_params` → `PARAM_AXIOM_VIOLATION`) | 🟢 **existe como patrón** (rama educativa) |
| `CHECK` en base de datos del parámetro votable | `app/schema.sql` (`edu_parameters`: `umbral_anios >= 12.0` y `<= 30.0`) | 🟢 **existe** para el umbral educativo |
| Anti-flip-flop de 14 días | `app/voting_bp.py` (`EDU_COOLDOWN_DAYS = 14`) | 🟡 **existe, cableado solo al umbral educativo** |
| Firma T13 como hash real (SHA-256) | `app/edu_bridge_bp.py` (columna `t13_hash`; NIST FIPS 180-4) | 🟢 **existe** |
| Auditoría estructural de esta biblioteca (plantilla, mínimo/óptimo, LEY/POLÍTICA, frases vetadas, anclas) | `tests/test_sdv_e_biblioteca.py` | 🟢 **existe y es ejecutable** |
| Verificador del estado HTTP real de cada fuente citada | `scripts/verificar_enlaces_sdv_e.py` | 🟢 **existe** (cuatro estados: `OK`, `BLOQUEADA`, `SIN_RESPUESTA`, `MUERTA`) |
| Tipo de parte `ecosystem` | `app/schema.sql` (`party_type`) · `app/parties.py` | 🟢 **existe** |
| Guardián oráculo del ecosistema | `app/contracts_bp.py` · `tests/test_maxocontracts/test_parties_escalas.py` | 🟡 funciona en la firma de contratos; heurística laxa (R13) |
| Crédito regenerativo (`r_units` negativo) | `app/micromax.py` · `tests/test_micromax.py` | 🟢 registrado y probado; **sin efecto contable** |
| Biblioteca del estándar (00-18, 20-23, 30, 31 y 40: **26 archivos**, la lista completa del brief; recuento recomprobado en la revisión adversarial) | `docs/theory/SDV-E/` | 🟢 escrita · 🟡 sin ratificar |
| Suite del pariente más cercano (SDV-S) | `tests/test_maxocontracts/test_sdv_s.py` (**28** funciones) + `test_ternura.py` (**13**) = **41** | 🟢 **verificado por conteo en esta sesión** |

### 12.2 Lo que NO existe — y está prohibido afirmar que existe

| Pieza del bloque `Procesos` | Estado | Evidencia |
|---|---|---|
| Circuito de **creación de umbrales** (grupo por clase, borrador, acta de entrada) | 🔴 | no existe tabla, ruta ni flujo; ninguna pieza en `app/` |
| **Ciclo de revisión** (calendario, informe de estado, acta de revisión) | 🔴 | no existe campo, planificador ni tabla de revisiones |
| **`unidad_de_ciclo_ta`** declarada por unidad | 🔴 | no existe en el motor; el documento 07 §13 lo deja sin decidir |
| **Revisión externa por pares** con sus dos rondas y sus plazos | 🔴 | no existe proceso ni registro; el modelo está solo descrito |
| **Órgano de desempate** y **comité de conflicto de interés** | 🔴 | no existen |
| **Depósito con DOI** emitido por el sistema | 🔴 | cero integraciones con repositorios; el DOI se documenta, no se emite |
| **Cadena de tres saltos** y **declaración de confianza** en las tablas del estándar | 🟡 | exigida por el brief; aplicada de forma parcial en la biblioteca |
| **Parlamento del Reino Natural** (parámetros ecológicos votables) | 🔴 | **verificado en esta sesión**: los únicos dos tipos de acción vinculante son `set_vhv_params` y `set_edu_umbral`; **no hay ningún circuito `eco-`** |
| **Anti-flip-flop aplicado a un parámetro ecológico** | 🔴 | existe el reloj (14 días), no el circuito |
| **`CHECK` de base de datos** para un parámetro del Reino Natural | 🔴 | no existe tabla de parámetros ecológicos |
| **Quórum `eco-` N-de-M** | 🔴 | sin N ni M; **el camino ecosistema retorna antes de la lógica de quórum**, y el libro afirma lo contrario (Cap. 16.5 §16.5.14) |
| **Procedimiento de disputa** | 🔴 | inexistente |
| **Identidad de la representación natural** (los 7 campos) | 🔴 | sin tabla; `maxo_parties` tiene columnas genéricas |
| **Mandato ecológico versionado** | 🔴 | `actor_kind` está cerrado a `{"human","synthetic"}` (`app/synthetic_sessions.py`): un guardián ecológico no cabe en la bitácora |
| **INV2-E**, tipo `SDV_E` y bloque validador | 🔴 | no existen (documento 08 §8.0 y §12) |
| **Sensores, ingestores o APIs ecológicas** | 🔴 | cero en `app/` |
| **Contabilidad del crédito regenerativo** (`SUM(r_units)`) | 🔴 | no existe; el R del sistema solo cuenta extracción y el precio cierra en `max(0.0, …)` (`app/maxo.py`) |
| **Mapas vivos actualizados** | 🟢 | **Recomprobado en la revisión adversarial de este documento**: `docs/architecture/mapa_coherencia_ola4.md` ya tiene la sección «Reino Natural — el agujero de coherencia activo» (menciona `r_units`, el `SDV_E` ausente, el guardián `eco-` y la biblioteca) y `docs/architecture/requisitos_fase2_ola4.md` tiene el pilar **O. Reino Natural — SDV-E** con RF-N1…RF-N12. Lo único desactualizado en ambos es el **recuento** («18 documentos», «~27 000 líneas»), que en la fecha de esta revisión son **26 archivos** (00-18, 20-23, 30, 31 y 40) |
| **Índice de la biblioteca** | 🟡 | el documento 00 §2 listaba el bloque `Procesos` como **pendiente de redacción** al escribir este documento; la actualización del índice corresponde al índice |

**Consecuencia honesta, sin adornos.** De las cinco dimensiones de §4, **ninguna tiene hoy una sola línea
de código**. Lo que existe es el **patrón** de la POLÍTICA (categoría `critical` con quórum 60 y consenso
75, guardia de confianza, rechazo de un valor por debajo de la ley, `CHECK` en base de datos, hash T13) y
está probado **en otra rama del proyecto**: la educativa. Este bloque no pide construir un mecanismo
nuevo: pide **cablear el que ya funciona** para el Reino Natural — y dice, con la misma claridad, que
**hoy no está cableado**.

---

## 13. Preguntas abiertas

Lo que **no** sé, y no finjo cerrar.

1. **El ciclo de 3-5 años no tiene fuente externa.** Es canon del proyecto (Cap. 9 §9.7) y **ningún
   organismo verificado declara un ciclo obligatorio de revisión de umbrales ecológicos cada 3, 4 o 5
   años**. Lo que existe: ≈ **8-9 años** entre la v1.0 (2016) y la v2.0 (2024) de la guía del estándar de
   ecosistemas; **10 años** por marco del CBD; **3 años** de COP de Ramsar (única fuente que lo prueba:
   **bloqueada a los agentes automáticos, 403**); IPBES sin periodicidad fija publicada.
   `[VERIFICADO que el hueco existe]`. Que 3-5 años sea el ciclo de los valores y 8-10 el de la
   arquitectura es `[HIPÓTESIS]` de este documento.
2. **Nadie publica cuántos revisores constituyen una validación por pares suficiente.** Ni el proceso
   IPBES (que publica fases, plazos y reglas, pero **no el número de revisores ni el umbral de
   aceptación**) ni el estándar de ecosistemas. **El «quórum N-de-M» del Reino Natural sigue sin N ni M**,
   y no es un vacío de fuente sino de decisión.
3. **No existe un procedimiento verificado de retiro de una unidad ecológica evaluada.** El estándar de
   ecosistemas tiene base de datos y reglas de categorías, pero no se pudo leer ningún procedimiento
   publicado sobre qué ocurre cuando una unidad evaluada **deja de existir**. El precedente de especies sí
   existe —categoría `EW` con plazo *«appropriate to the taxon's life cycle»*, y retiro por error
   *«without delay»*— y es el que este documento adapta `[HIPÓTESIS]`.
4. **No se pudo verificar cómo se versiona, revisa ni enmienda la Tipología Global de Ecosistemas**, que
   es el marco de clasificación del que depende la unidad del SDV-E: el portal devuelve 200 **con cuerpo
   vacío** (carga por JavaScript) y la ruta de la IUCN redirige. **Es el vacío más costoso de este
   documento**: si la tipología cambia de versión, este documento solo puede ordenar la **re-declaración**
   de la atribución (documento 02 §4-C2), no decir cómo se traduce el cambio.
5. **Ningún organismo verificado publica un procedimiento de apelación contra un umbral fijado.** Existe
   un comité de estándares y apelaciones de áreas clave de biodiversidad, pero **su reglamento no se pudo
   leer** (el PDF devuelve 406 al leerse). El procedimiento de disputa del documento 05 es una propuesta
   sin modelo verificado que copiar.
6. **La política de uso de IA en evaluaciones científicas existe y no se leyó.** La página del organismo
   que la publica responde 200, y es la fuente más relevante que queda pendiente para un estándar
   redactado por un oráculo sintético. **Este bloque no tiene todavía una regla sobre el uso de IA en la
   revisión de umbrales**, y no la inventa.
7. **No hay umbral verificado de «dominio de la evidencia»** para declarar maduro un umbral: ni el número
   mínimo de estudios independientes, ni el criterio cuantitativo. La regla operativa verificada es
   **cualitativa**: si no hay evidencia cuantitativa clara, se emite una declaración de buenas prácticas
   en lugar de un número.
8. **No se encontró el procedimiento concreto por el que un umbral científico se convierte en norma
   jurídica vinculante en un Estado**, ni cuánto tarda, ni quién lo puede bloquear. La dimensión P5
   propone el acta de incorporación **sin fuente que la respalde**.
9. **El procedimiento escrito de depósito con DOI no se pudo verificar**: la página que la guía de fases
   enlaza devuelve **404**. El DOI está verificado como práctica (ejemplo real citado por la institución),
   no como trámite.
10. **Las normas ISO de vocabulario ambiental no se pudieron verificar** (403): **no se cita ni su número
    ni su año**. Se cita la norma del identificador persistente (ISO 26324) porque su registro sí está
    verificado.
11. **El mecanismo de la categoría `critical` existe y no está disponible para el Reino Natural.**
    Verificado en esta sesión: los únicos dos circuitos vinculantes del parlamento son los parámetros del
    VHV y el umbral educativo. **Cablear un tercero es una decisión, no una tarea de implementación** — y
    es la precondición de que la columna POLÍTICA de §5.2 sea algo más que una intención.
12. **La cifra de cobertura del piso está en disputa entre dos documentos de esta misma biblioteca**: 0,925
    (documento 07 §5.3: suelo y caudal con piso, oxígeno con coeficiente) frente a 0,680 (documento 08 §5.2),
    y el propio índice de la biblioteca la declara «cifra en disputa». **Este documento no la elige, no la
    usa y no la corrige**: la declara, porque la discrepancia es real y está localizada. Propongo —sin
    decidirlo— que el documento 08 sea la fuente única y que la revisión de coherencia de la biblioteca lo
    ratifique.
13. **El umbral de oxígeno disuelto estuvo clasificado de dos maneras distintas** en esta biblioteca y
    quedó resuelto en la revisión de coherencia (2026-10-09): el documento 07 §13 (pregunta 14) **usa** el
    umbral recuperado de la hoja informativa viva de la agencia ambiental (EPA/NIWA, documento 06 D2),
    y el documento 08 §5.2 lo acepta **con umbral pero sin coeficiente**, por su regla 1 (produce violación
    sin dimensionar `v`; su cobertura queda en 0,680). La ruta específica muerta (404) se registra como
    fuente descartada, no como ausencia de umbral.
14. **Dos rangos de pH conviven en la biblioteca sin citarse entre sí**: el del agua de riego (6,5-8,4)
    que usan los documentos 07 y 08, y el de aguas dulces (6,5-9) que publica el documento 09 §11.3. No
    son contradictorios en su lógica —uno es proxy declarado y el otro es criterio de vida acuática— pero
    **el lector no tiene forma de saber cuál es el vigente para el piso del SDV-E**. Lo declaro en vez de
    armonizarlo por mi cuenta.
15. **Quién puede perdonar a un ecosistema.** La capa de ternura acepta un otorgante `eco-*`, pero el
    canon no dice si el guardián tiene legitimidad para perdonar en nombre de la unidad, ni si hace falta
    la comunidad de custodia, ni con qué quórum —que sigue sin N ni M—. Este bloque **no lo decide**.
16. **El umbral del contador de asimetría** (la prueba de que la contabilidad no colonizó el TA) pertenece
    al documento 03, y **allí está publicado**: `CNC = 0` exacto (§5.3), con base neutra 1,0 (§5.2) y
    cláusula de no vacuidad (§5.4). Lo que este bloque no puede aportar es su **implementación**: el
    mecanismo verificable hoy no existe en código, y sin él la asimetría se declara pero no se juzga.
17. **La forma exacta del anti-flip-flop para los parámetros del Reino Natural** está sin decidir: el
    documento 08 §8.6 lo propuso como **condición de juego** («el contador no puede modificarse mientras
    exista una violación abierta») y el mecanismo verificado del repositorio lo implementa como **plazo**
    (14 días). Las dos formas conviven en la biblioteca y **no sé cuál debe regir**; propongo que rija la
    condición de juego **y** el plazo, en ese orden (la condición es más fuerte).
18. **La traducción a políticas no tiene procedimiento verificado de incorporación al derecho nacional**,
    y el dinero es la parte que decide: la cláusula financiera del precedente verificado es de escala
    global (cientos de miles de millones de USD/año) y **este documento no sabe cómo se traduce a la
    unidad ecológica concreta** sin convertir el estándar en un instrumento de política macro.

---

## 14. Referencias

**Regla aplicada.** Solo se listan URLs cuyo estado HTTP quedó registrado en la sesión de verificación de
fuentes de esta rama (octubre 2026), recogida en `scratch/sdv_e/fuentes/40_procesos.md`. **Esta sesión de
redacción no repitió las comprobaciones**: los estados se declaran con su procedencia. Se marcan por
separado las fuentes reales que bloquean a los agentes automáticos.
**Revisión adversarial posterior (misma rama).** Se recomprobaron por HTTP **todas** las URLs de §14.1-§14.4:
el resultado coincide con el informe salvo tres dominios que hoy bloquean al cliente automático
(`zenodo.org`, `rsis.ramsar.org`, `iucngreenlist.org`: §14.5). Se añadió la ruta que publica la cifra
internacional de la Meta 19 (§14.4) y se listaron con URL las **dos fuentes heredadas** que el texto citaba
sin ella (§14.9). Ninguna URL resultó muerta ni inventada.

### 14.1 Procesos de creación y validación por pares

| Fuente | Aporte | URL (estado) |
|---|---|---|
| IPBES — *Phases of the expert evaluation* | Fases del proceso, **dos rondas de revisión externa (6-8 semanas y 8 semanas)**, tres reuniones de autores, **12 semanas** de antelación del borrador final, ventana de comentarios hasta **2 semanas** antes de la Plenaria, y las reglas de oro (disidencia documentada, separación autor/árbitro) | https://www.ipbes.net/assessment-guide_phases-of-expert-evaluation (200) |
| IPBES — *Consideration of external review comments* | Tratamiento obligatorio y publicación de comentarios y respuestas tras la Plenaria | https://www.ipbes.net/assessment-guide_consideration-external-review-comments (200) |
| IPBES — *Assessments* (página oficial) | Publicación con **DOI sobre Zenodo** (ejemplo citado: `10.5281/zenodo.4147317`) | https://www.ipbes.net/assessments (200) |
| IPBES — *Traceability* | Regla de los **tres saltos** y marcas de anclaje por sección | https://www.ipbes.net/assessment-guide_traceability (200) |
| IPBES — *Four-box confidence model* | Declaración de confianza: tipo, cantidad, calidad y consistencia de la evidencia | https://www.ipbes.net/assessment-guide_four-box-confidence-model (200) |
| IPBES — política de uso de IA en evaluaciones (**verificada 200, NO leída en la sesión de fuentes**) | Pendiente de lectura obligatoria (§13, pregunta 6) | https://www.ipbes.net/assessment-guide_use-of-AI (200) |
| IPBES — programa de trabajo y segunda evaluación global (**verificadas 200, no leídas**) | Evidencia de que un estándar científico se re-evalúa, sin intervalo fijo declarado | https://www.ipbes.net/work-programme (200) · https://www.ipbes.net/second-global-assessment (200) |

### 14.2 Trazabilidad, identificadores persistentes y firma

| Fuente | Aporte | URL (estado) |
|---|---|---|
| Zenodo (CERN) — repositorio de depósito | Infraestructura de depósito en abierto | https://zenodo.org/ (200) |
| DOI Foundation — norma **ISO 26324** | Registro de identificadores persistentes | https://www.doi.org/ (200) |
| GBIF — *Citation guidelines* | Cita obligatoria por dataset con su propio identificador — **real, bloquea a los agentes automáticos** | https://www.gbif.org/citation-guidelines (403) |
| NIST FIPS 180-4 — *Secure Hash Standard* (vía implementación del repositorio) | SHA-256 como firma del registro: **256 bits** | `app/edu_bridge_bp.py` (columna `t13_hash`) `[VERIFICADO]` |

### 14.3 Ciclos de revisión y retiro de umbrales

| Fuente | Aporte | URL (estado) |
|---|---|---|
| IUCN — *Guidelines for the Application of IUCN Red List of Ecosystems Categories and Criteria*, **v2.0** (agosto 2024) | v1.0 (2016) → v2.0 (2024): **≈ 8-9 años**; 8 categorías, 5 criterios (A-E); *«a level of biological organization above species»*; el cambio de versión **añade criterios**, no solo números | https://iucnrle.org/news/updated-guidelines-for-the-application-of-iucn-red-list-of-ecosystems-categories-and-criteria-now-available (200) |
| IUCN RLE — gobernanza del estándar | Adopción formal por el Consejo de la IUCN en **2014**; grupo temático, asociación declarada, base de datos de evaluaciones conformes y regla de citación: **cuatro piezas replicables** | https://iucnrle.org/ (200) |
| IUCN — *Categories and Criteria* v3.1, 2ª ed. (documento RL-2001-001-2nd) | **Retiro por mejora: cinco años** consecutivos sin cumplir los criterios de la categoría superior, contados desde que los datos lo muestran; categoría **EW** con plazo *«appropriate to the taxon's life cycle»* | https://portals.iucn.org/library/sites/library/files/documents/RL-2001-001-2nd.pdf (200) |
| COSEWIC — *Guidelines on transferring between status categories during a reassessment* (basado en IUCN, 2019) | **Asimetría verificada**: bajar de riesgo es lento; **subir y corregir un error son inmediatos** (*«without delay»*); y la advertencia *«This is not intended to drive timing of reassessments»* | https://cosewic.ca/index.php/en/status-reports/applications-wildlife-species-assessment-status-reports/guidelines-on-transferring-between-status-categories-during-a-reassessment (200) |
| Ramsar — informe del Secretario General a la COP15 (2025) | Ciclo **trienal** de la COP (COP14 en 2022 → COP15 en 2025): el único ciclo corto verificado en gobernanza ambiental — **real, bloquea a los agentes automáticos (403)**: se cita con la advertencia de que no se pudo leer su cuerpo | https://www.ramsar.org/sites/default/files/2025-05/cop15_8_1_sg_report_global_implementation_e.pdf (403) |
| Ramsar Sites Information Service | Registro oficial de sitios y sus informes | https://rsis.ramsar.org/ (200) |
| CBD — Decisión 15/6: mecanismos de planificación, seguimiento, reporte y revisión | Informes nacionales en **2026 y 2029**; revisión global del progreso en **COP 17 y COP 19**; revisión por pares **voluntaria** (VPR) separada del reporte obligatorio | https://www.cbd.int/doc/decisions/cop-15/cop-15-dec-06-en.pdf (200) · https://www.cbd.int/gbf/related (200) · https://www.cbd.int/nbsap/vpr/ (200) |
| CBD — Decisión 15/5: marco de seguimiento | Indicadores jerarquizados (de titular, de componente y complementarios) con grupo técnico experto | https://www.cbd.int/doc/decisions/cop-15/cop-15-dec-05-en.pdf (200) |

### 14.4 LEY y POLÍTICA: el precedente verificado más fuerte

| Fuente | Aporte | URL (estado) |
|---|---|---|
| OMS, 2021 — *WHO global air quality guidelines* | El documento de la directriz (los números se leyeron en la tabla reproducida por el órgano asesor nacional, §14.5) | https://www.who.int/publications/i/item/9789240034228 (200) |
| OMS — preguntas y respuestas oficiales sobre las directrices | Arquitectura de **tres niveles**: nivel de directriz (**LEY**), objetivo intermedio (**POLÍTICA**, *«serve to guide reduction efforts towards the ultimate and timely achievement of the AQG levels»*) y declaración de buenas prácticas (cualitativa); grupo de desarrollo de la directriz, grupo de revisión externa y grupo directivo; **más de 500 artículos** en la revisión sistemática; y la frase que fija la frontera: *«guidelines are not legally binding recommendations, they can be used as an evidence-informed reference tool to help decision-makers in setting legally binding standards»* | https://www.who.int/news-room/questions-and-answers/item/who-global-air-quality-guidelines (200) `[VERIFICADO]` |
| COMEAP / UKHSA, 2022 — respuesta a las directrices de la OMS | **La tabla de valores de la OMS 2021**, y la advertencia decisiva: *«The guideline values should not be regarded as thresholds below which there are no impacts on health»* — **el piso no es «daño cero»: es el nivel donde la certeza se agota** | https://www.gov.uk/government/publications/comeap-statement-response-to-who-air-quality-guidelines-2021/comeap-statement-response-to-publication-of-the-world-health-organization-air-quality-guidelines-2021 (200) |
| Revisión 2023 de las nueve fronteras planetarias (reproducción oficial del organismo estadístico francés, CGDD) | Las **18 variables de control** con valor de referencia, umbral bajo, umbral alto y valor actual; y **dos variables sin umbral numérico**: aerosoles (*«No global threshold defined, in the absence of sufficient knowledge»*) y entidades nuevas (*«0 to ? (high threshold not defined)»*) — el precedente de `SIN UMBRAL — en observación` | https://www.statistiques.developpement-durable.gouv.fr/edition-numerique/la-france-face-aux-neuf-limites-planetaires/en/14-2023-revision-of-the-nine (200) |
| CBD, 2022 — Marco Kunming-Montreal, Decisión 15/4 y sus metas | Metas con cifra y año: **≥ 30 %** de restauración efectiva de ecosistemas degradados para 2030 (Meta 2) · **≥ 30 %** conservado y gestionado eficazmente (Meta 3) · **≥ 50 %** de reducción de la tasa de introducción de invasoras (Meta 6) · **≥ 50 %** de reducción del exceso de nutrientes y del riesgo de plaguicidas (Meta 7) · **participación plena y equitativa** en la toma de decisiones y acceso a la información (Metas 22 y 21) · **cláusula financiera**: ≥ 500 000 M USD/año de incentivos perjudiciales reformados (Meta 18) y ≥ 200 000 M USD/año movilizados, de los cuales **≥ 30 000 M USD/año internacionales para 2030** (y ≥ 20 000 M USD/año para 2025) (Meta 19) | https://www.cbd.int/doc/decisions/cop-15/cop-15-dec-04-en.pdf (200) · https://www.cbd.int/gbf (200) · https://www.cbd.int/gbf/targets (200) · https://www.cbd.int/gbf/targets/3/ (200) · https://www.cbd.int/gbf/targets/19/ (200, comprobada en la revisión adversarial de este documento: es la ruta que publica la cifra internacional de la Meta 19) |

### 14.5 Fuentes reales que bloquean a los agentes automáticos (403/406) — citables por una persona

`ramsar.org` (raíz y todos sus PDF) · `gbif.org` (guías de citación) · `iucnredlist.org` ·
`portals.iucn.org/…/SSC-Species-065-En_2.pdf` (**406 al leer**: el estándar de áreas clave de
biodiversidad y su comité de apelaciones **no se pudo leer**) · `global-ecosystems.org` (200 **con cuerpo
vacío**: la tipología carga por JavaScript y **no se pudo verificar su proceso de revisión**) ·
`science.org` · `iso.org` (no se pudo verificar el número ni el año de las normas de vocabulario
ambiental) · `whc.unesco.org` · `unep.org/resources/*`. **Añadidas en la revisión adversarial de este
documento** (bloquean al cliente automático con el que se recomprobaron, y un humano las abre):
`zenodo.org` (**403**) · `rsis.ramsar.org` (**418**) · `iucngreenlist.org` (**403**). Son fuentes reales: un humano las abre. **En este
documento no se cita de ellas ninguna cifra que no se haya podido leer.**

### 14.6 Fuentes descartadas (muertas o no citables)

- **`ipbes.net/assessment-guide_upload-to-zenodo`** — **404**. Enlazada desde la guía de fases del propio
  organismo, es la que habría documentado el **procedimiento de depósito**; su muerte es la causa directa
  de que la dimensión P4 declare el DOI verificado como práctica y no como trámite.
- **`help.zenodo.org/docs/deposit/describe-records/doi/`** — **404** (documentación de depósito
  reestructurada). No se cita.
- **`who.int/tools/airquality`** — 404. **`cdn.who.int/…/who-global-air-quality-guidelines-2021.pdf`** —
  404. Los números de la OMS se citan por la tabla reproducida por el órgano asesor nacional (§14.4).
- **`unccd.int/actions/ldn-land-degradation-neutrality`** y el texto de la Convención (PDF 2022) — 404.
- **`iucnrle.org/assessments/`** y **`iucnrle.org/resources`** — 404.
- **`epa.gov/wqc/aquatic-life-criteria-dissolved-oxygen`** — 404 (recomprobada): es la causa de la disputa
  de clasificación del oxígeno disuelto entre los documentos 07 y 08 (§13, pregunta 13).
- **`nature.com/articles/s41597-022-01604-9`**, **`livingplanetindex.org/latest-results`**,
  **`keybiodiversityareas.org/home`** — 404.
- **Dominios muertos confirmados**: `iucnglobalecosystemtypology.org` (000) y `eflows.net` (000).

### 14.7 Referencias internas al canon (por sección, sin anclas de línea)

- **Cap. 9 §9.7** — La Base de Datos Universal de SDV: el árbol (`SDV-H`, `SDV-A`, `SDV-E`, `Procesos`)
  con las tres piezas `Metodología_Creación`, `Protocolo_Actualización` y `Gobernanza_Validación`, y los
  cinco procesos continuos (redacción de nuevos SDV, ciclos de revisión cada 3-5 años, revisión por
  pares + repositorios abiertos + DOI, deliberación democrática sobre umbrales controvertidos,
  traducción a políticas). **Es el origen del bloque que este documento desarrolla, y está escrito "por
  especie".**
  `docs/book/edicion_3_dinamica/capitulo_09_sdv_a_260126.md`
- **Cap. 10 §10.4** — El SDV Universal: *SDV para Ecosistemas* (área mínima para biodiversidad viable ·
  calidad del aire y agua · conectividad · ciclos naturales respetados) y *SDV para Lugares* (caudal
  mínimo ecológico · calidad del agua · riberas protegidas · fauna acuática viable).
- **Cap. 10 §10.3** — Principio Precautorio de Consciencia. · **Cap. 10 §10.5** — Proporcionalidad. ·
  **Cap. 10 §10.6** — Dignidad encadenada. · **Cap. 10 §10.7** — Gobernanza operacionalmente finita.
- **Cap. 16.5 §16.5.14** — El hogar extendido: partes `eco-`, guardián oráculo, TA y PIU, Zona Libre,
  *«el suelo antes que el saldo»*, *«cuidado ≠ extracción estética»* y la sentencia del invariante que
  falta (*«INV2-E será su juez»*).
  `docs/book/edicion_3_dinamica/capitulo_16_5_micromaxocracia_canonica_220826.md`
- **Cap. 8 §8.3** y **Cap. 9 §9.3** — Los cinco criterios de validación de un parámetro. ·
  **Cap. 8 §8.6** — Auditoría independiente. · **Cap. 8 §8.11** — Dimensiones binarias sin peso.
- **Cap. 5 §5.5** — PIU (Protocolo de Intercambio Universal), único traductor TA↔TVI, y el costo en TA del
  bosque. · **Cap. 5** — T14 (Principio de Precaución Intergeneracional) y T7 (Jerarquía Temporal).
- **Cap. 9.5 §9.5.10** — Veto por Crimen de Coherencia: *«la interrupción total del sistema que la
  provoca»*. · **Cap. 9.5 §9.5.5** — La corrección de la base neutra (`FS_S = e^v`). · **Cap. 17** — INV2.
- **Cap. 14** — Arquitectura del Consenso Diverso (quórum y mayorías por categoría). · **Cap. 6 §6.13** —
  El límite de T13. · **Cap. 4 §4.2** — La Directiva Mayor.
- **EVV-1.2 §4.3** — Componente R: el crédito regenerativo admite valores negativos.
  `docs/book/edicion_3_dinamica/capitulo_18_EVV_1.2_270126.md`
- **Axioma 0 — Directiva Mayor** (*«resolver nuestras necesidades de la mejor manera para todos todos»*,
  los **tres reinos**, presentes y futuros) · **T13** · **T14** · **T9** · **T16**:
  `maxocontracts/core/axioms.py`

### 14.8 Referencias internas a esta biblioteca (enlaces relativos, sin anclas)

- Documento 00 — Índice y estado de la biblioteca: [00_README_indice.md](00_README_indice.md)
- Documento 01 — Doctrina del SDV-E (los tres pasos; LEY frente a POLÍTICA): [01_Doctrina_SDV-E.md](01_Doctrina_SDV-E.md)
- Documento 02 — Unidad y sujeto (criterios C1-C5; continuidad de identidad): [02_Unidad_y_sujeto_del_SDV-E.md](02_Unidad_y_sujeto_del_SDV-E.md)
- Documento 03 — No colonización del TA (el umbral del contador de asimetría): [03_No_colonizacion_del_TA.md](03_No_colonizacion_del_TA.md)
- Documento 04 — Zona Libre del Reino Natural: [04_Zona_Libre_del_Reino_Natural.md](04_Zona_Libre_del_Reino_Natural.md)
- Documento 05 — Representación, guardián y mandato (los 7 campos, quórum, disputa): [05_Representacion_guardian_y_mandato.md](05_Representacion_guardian_y_mandato.md)
- Documento 06 — Medición y verificación (T13): [06_Medicion_y_verificacion_T13.md](06_Medicion_y_verificacion_T13.md)
- Documento 07 — Fórmula de violación y pesos: [07_Formula_de_violacion_y_pesos.md](07_Formula_de_violacion_y_pesos.md)
- Documento 08 — INV2-E, el invariante: [08_INV2-E_invariante.md](08_INV2-E_invariante.md)
- Documento 09 — Comparativa inter-reinos: [09_Comparativa_inter_reinos.md](09_Comparativa_inter_reinos.md)
- Riesgos **R4**, **R6** y **R13**: [blindaje_anti_gamificacion_equidad.md](../../architecture/blindaje_anti_gamificacion_equidad.md)
- Puertas deterministas de esta biblioteca: `tests/test_sdv_e_biblioteca.py` ·
  `scripts/verificar_enlaces_sdv_e.py`
- Mecanismo de POLÍTICA verificado (quórum, mayoría, guardia de confianza, anti-flip-flop, `CHECK`):
  `app/voting_bp.py` · `app/schema.sql`
- Firma T13 (SHA-256): `app/edu_bridge_bp.py`

### 14.9 Fuentes heredadas de la sesión de fuentes del documento 05 (con URL y estado)

Estas dos fuentes estaban **citadas en el texto sin URL** (§4-P2, §4-P3 y §4-P5) porque proceden de la
sesión de verificación del [documento 05](05_Representacion_guardian_y_mandato.md), no de la de este
documento. La revisión adversarial posterior las trajo aquí con su URL y su estado, para que cualquiera
pueda recomprobarlas:

| Fuente | Aporte | URL (estado) |
|---|---|---|
| OCDE, 2020 — *Innovative Citizen Participation and New Democratic Institutions* | Vida mínima de una deliberación cara a cara: **1 día completo**; **≥ 4 días** si se piden recomendaciones informadas; preparación mínima previa (5-12 semanas) | https://www.oecd.org/content/dam/oecd/en/publications/reports/2020/06/innovative-citizen-participation-and-new-democratic-institutions_11aa2baf/339306da-en.pdf (200, recomprobada) |
| IUCN Green List, v1.1 (2017) — *Global Standard* e indicadores | Renovación de la verificación externa a **5 años**; proceso accesible de quejas (indicador **GLS-V1.1-1.2.4**) | https://iucngreenlist.org/standard/global-standard/ (**403**) · https://iucngreenlist.org/standard/components-criteria/ (**403**) |

**Precisión de alcance.** Ni la OCDE ni el Green List fijan umbral alguno del reino natural: son
**precedentes de procedimiento humano** (cuerpos deliberativos y estándares de conservación), y así están
marcados en el texto — `[VERIFICADO]` en su sesión de origen, `[REPORTADO]` cuando lo que se hereda es la
regla y no la cifra.

**Nota sobre las referencias internas.** Se citan **por capítulo y sección** (`Cap. 9 §9.7`,
`Cap. 16.5 §16.5.14`), como manda el brief de esta biblioteca; los enlaces son un apoyo de localización y
**no** son la referencia primaria. No se usan anclas de línea.

---

## Anexo — Autoevaluación contra el checklist del brief

| Punto del checklist | Estado |
|---|---|
| Plantilla de 14 secciones | ✅ las 14 |
| Mínimo Absoluto separado del Óptimo | ✅ §4 (cinco dimensiones, dos columnas) y §5.2 |
| Cada cifra con fuente + año, y URL en Referencias | ✅ §14 (o marca literal de vacío) |
| URLs verificadas, cero inventadas | ✅ solo las del informe de fuentes de la rama, con su estado |
| Marcas `[VERIFICADO]` / `[REPORTADO]` / `[HIPÓTESIS]` | ✅ en todo el texto |
| Canon citado por sección, sin anclas de línea ni enlaces locales de archivo | ✅ §14.7 |
| Preámbulo metodológico presente | ✅ §2 (ocho reglas) |
| Zona Libre explícita | ✅ §10 |
| LEY (no votable) frente a POLÍTICA (votable) | ✅ §5.2, con el mecanismo verificado en código |
| §12 honesta, con 🔴 donde no hay código | ✅ dos tablas: lo que existe y lo que no |
| §13 dice lo que no sé | ✅ dieciocho preguntas, con la contradicción declarada y no corregida |
| Frases prohibidas evitadas; axiomas sin definir de más | ✅ |
| Aporta algo que no está en el canon sin contradecirlo | ✅ véase el resumen final |

**Los cinco aportes de este documento, en una lista, para que se puedan discutir uno por uno:**

1. **La adaptación de «por especie» a «por unidad ecológica» con su anclaje externo**: la clase es el tipo
   de ecosistema de los niveles 4-6 (con su EFG de referencia, nivel 3, que **no** es unidad de evaluación)
   y la unidad es la ocurrencia delimitada; el umbral se crea **por clase** y se instancia
   **por unidad**, con el precedente verificado de que el estándar de ecosistemas evalúa *«un nivel de
   organización biológica por encima de la especie»* (§1) — lo que convierte una licencia aparente en la
   unidad con la que ya trabaja la autoridad taxonómica.
2. **El procedimiento de retiro de un umbral que envejece**, con la asimetría verificada —**error:
   inmediato; mejora: cinco años de evidencia contraria**— y con la separación de **dos relojes** que
   nadie había separado: el de la revisión periódica (3-5 / 8-10 años) y el del retiro (§4-P2).
3. **La lista cerrada de quién puede proponer y quién verifica**, con la regla del no-beneficiario y los
   plazos verificados de la revisión por pares en dos rondas (6-8 y 8 semanas), el órgano de desempate y
   el comité de conflicto de interés (§4-P3).
4. **La frontera LEY/POLÍTICA aplicada al proceso entero**, con el patrón ya probado en el repositorio
   para hacerla ejecutable: **la ley vive en el motor, el voto está acotado por abajo por ella y hay doble
   candado** —validación de la propuesta y `CHECK` en base de datos—, más la comprobación de que **el
   parlamento del Reino Natural no existe hoy** (§5.2 y §12).
5. **Los tres estados de un umbral** (`CUANTIFICADO` · `CUALITATIVO (buena práctica)` · `SIN UMBRAL — en
   observación`), con el precedente de los estándares que publican lo que no saben con la misma
   formalidad con que publican lo que saben (§5.3).

Y una cosa que este documento **no** aporta, para que no se le atribuya: **no crea un solo umbral
ecológico, no decide la unidad del sujeto, no fija los pesos ni la cifra de cobertura del piso en
disputa.** Su valor, hoy, es que el procedimiento está escrito **antes** de que exista el primer umbral
que lo use — que es el único orden en el que un procedimiento sirve para algo.

> *"El sistema no expulsa. Reintegra."* — pero **la contabilidad nunca se borra** (T13), y en el Reino
> Natural **el daño tampoco se recompra**.
