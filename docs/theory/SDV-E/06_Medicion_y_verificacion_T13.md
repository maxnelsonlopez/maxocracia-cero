# El elenco de sensores del SDV-E: medición y verificación (T13)
## Los cinco linajes de sensor del Reino Natural —teledetección satelital, sensores in-situ, bioindicadores, ciencia ciudadana y comunidad testigo con datos abiertos—, sus frecuencias por dimensión, quién reporta, quién audita, cómo se firma; y el límite de T13: la transparencia aplica a las decisiones que afectan a otros, no a la vida interior

**Autoría:** Oráculo Sintético DeepSeek & Max Nelson López Restrepo
**Fecha:** octubre 2026
**Proyecto:** Maxocracia — El gobierno de la verdad, el tiempo y la vida
**Licencia:** Creative Commons BY-SA 4.0
**Estado:** Propuesta de estándar (rama SDV-E, Ola 4) — NO canon hasta ratificación
**Referencia canónica:** Cap. 10 §10.4 · Cap. 16.5 §16.5.14 · EVV-1.2 §4.3 · Cap. 9.5 (precedente SDV-S)
**Documento:** 06 de la biblioteca `docs/theory/SDV-E/`
**Foco:** el **elenco formal de sensores** del SDV-E, análogo a los sensores nombrados del SDV-S (IFC, TRE, AOS, VCM): qué instrumento sostiene cada dimensión, con qué frecuencia puede leerse, quién reporta, quién audita al que reporta y cómo se firma cada lectura (T13, SHA-256). Y su límite doctrinal: la transparencia aplica a las **decisiones que afectan a otros**, no a la vida interior.
**Trazabilidad:** este documento **no re-verifica** fuentes: consume el informe de fuentes de la rama (`scratch/sdv_e/fuentes/06_medicion.md`, documento de trabajo, NO de la biblioteca), que comprobó **91 URLs** con estado HTTP real en su sesión (63 con 200, 1 redirección resuelta, 13 bloqueadas a agentes automáticos, 12 muertas, 4 sin respuesta) y leyó el contenido numérico de las que sostienen cifras. Toda URL citada aquí está en la §14. Los enlaces de este documento se comprueban con `scripts/verificar_enlaces_sdv_e.py`.

---

> *"Nosotros registramos la interacción, no la vida interna del ecosistema."* — (Cap. 16.5 §16.5.14)
>
> *"Parte del valor del humedal es inefable (Cap. 7 §7.9). Los sensores miden salud (agua, cobertura,
> biodiversidad indicadora); jamás «milagros». Medir todo sería la forma técnica de dejar de escucharlo."*
> — (Cap. 16.5 §16.5.14)

---

## 1. Qué es (y qué no es) este elenco de sensores

**Qué es.** Es la pieza que convierte al SDV-E en un estándar **medible**: el elenco de sensores que el
documento [09 de esta biblioteca](09_Comparativa_inter_reinos.md) §6 declaró inexistente. El documento 09
mostró la asimetría que define al cuarto reino —*"el SDV-E es el único estándar cuyo sujeto no puede
reportar nada y cuyo representante no tiene autoridad verificada"*— y cerró su sección de protocolo con
una frase que este documento toma como encargo:

> **sin instrumentos, el SDV-E no es «débil», es inenunciable.**

Ese encargo tiene una consecuencia inmediata y es el argumento de apertura de toda la biblioteca:
**un juez sin medición es un decorado**. El canon nombra al juez —*"Un conjunto con crédito regenerativo
acumulado pero humedal bajo su SDV-E no está en coherencia: **INV2-E será su juez**"* (Cap. 16.5
§16.5.14)— pero no nombra un solo instrumento. Este documento nombra cinco **linajes** de instrumento,
los ordena, les asigna lo que cada uno puede y no puede ver, fija el techo de frecuencia que la física
impone (no el que la gobernanza desearía), y especifica **quién responde por cada lectura y cómo se
firma**.

**La analogía, dicha con precisión.** El SDV-S resolvió su verificación con **sensores lógicos nombrados**
(Cap. 9.5 §9.5.6): IFC (Índice de Fragmentación de Contexto, umbral crítico > 0,20 de pérdida neta),
TRE (Tasa de Rechazo de Entrada, umbral < 0,05), AOS (Auditoría de Oráculo Sintético, sesgo de
complacencia > 0,15) y VCM (Verificación de Cápsula de Memoria). El SDV-E necesita el mismo tipo de
artefacto —instrumentos **nombrados**, con **umbral** o con **límite de resolución declarado**, no buenas
intenciones— pero **físicos, no lógicos**, porque su sujeto no puede declarar su propio estado. La
correspondencia se propone en §6.1 y va marcada `[HIPÓTESIS]`. Y una precisión de método sobre los cuatro
umbrales del SDV-S que se acaban de citar: **se citan por sección del libro (Cap. 9.5 §9.5.6), no se
re-verifican en esta rama**; el informe de fuentes de este documento no los comprobó, y nadie debe leer de
aquí que fueron medidos o validados.

**Qué no es.**

- **No es la fórmula.** Pesos, escala de severidad y umbrales pertenecen al
  [documento 07](07_Formula_de_violacion_y_pesos.md) de esta biblioteca. Aquí solo se fija **lo que el dato
  debe traer** para poder entrar en una fórmula.
- **No es el invariante.** INV2-E pertenece al [documento 08](08_INV2-E_invariante.md). Este documento
  especifica el **contrato de entrada** que ese invariante ya exige en su §6.1, y no lo reescribe.
- **No sustituye a los protocolos por ecosistema.** Los documentos [10](10_Ecosistemas_Bosques.md),
  [13](13_Ecosistemas_Oceanos_y_costas.md), [14](14_Ecosistemas_Suelos_vivos.md),
  [16](16_Ecosistemas_Montanas_y_criosfera.md) y [18](18_Ecosistemas_Agroecosistemas.md) fijan los
  instrumentos de **su** unidad. Este documento **consolida** sus elencos en un vocabulario común y
  resuelve lo que ninguno puede resolver por separado: la frecuencia máxima admisible y la cadena de
  firma.
- **No es una promesa de cobertura.** El elenco cierra **lo que se puede cerrar hoy** y declara, con nombre
  y consecuencia, **lo que queda abierto**: **trece vacíos de fuente** y **siete vacíos de decisión** en su
  §13, veinte preguntas en total, ninguna cerrada por conveniencia. Un elenco que fingiera cubrir las ocho
  dimensiones canónicas sería el documento más peligroso de la biblioteca: daría por medido lo que no se
  mide.
- **No autoriza a medir el interior.** *"Medir todo sería la forma técnica de dejar de escucharlo"*
  (Cap. 16.5 §16.5.14). Lo que este elenco **prohíbe** medir es tan vinculante como lo que ordena medir
  (§10 y [documento 04](04_Zona_Libre_del_Reino_Natural.md)).
- **No está implementado.** 🔴 **Cero sensores, cero ingestores, cero APIs satelitales** en el
  repositorio: búsqueda literal de «Copernicus», «Sentinel», «Landsat» y «sensor» en `app/` → **cero
  coincidencias** [VERIFICADO: lectura directa del repositorio en esta sesión]. La §12 lo detalla sin
  adornos.

**Una colisión de conteo que conviene declarar antes de usarla como precedente.** El brief de esta
biblioteca y el [documento 09](09_Comparativa_inter_reinos.md) §6 hablan de **cuatro** sensores del SDV-S
(IFC, TRE, AOS, VCM), y el estándar SDV-S publicado en `docs/theory/` también lista cuatro; pero el libro
(Cap. 9.5 §9.5.6) nombra **cinco**, añadiendo **MS — Mapeo de Sandbox** (veracidad del entorno) en la
dimensión III. No es un error de este documento ni una errata de nadie: son **dos versiones del mismo
elenco conviviendo**. Aquí se usa la versión de cuatro —la del brief— y se deja constancia de la quinta,
porque un elenco que se cita mal deja de ser un precedente y pasa a ser una paráfrasis.

**Marcas de evidencia usadas en todo el texto.** `[VERIFICADO]` = cifra o texto leído en la fuente citada
o en el archivo del repositorio indicado, con estado HTTP constatado en la sesión de verificación de esta
rama. `[REPORTADO]` = dato afirmado por una fuente que se cita sin haber podido abrir el documento
primario. `[HIPÓTESIS]` = inferencia razonada del proyecto, no observación. `[SIN FUENTE VERIFICADA —
pendiente de consenso científico]` = se buscó el umbral y **no existe fuente utilizable en esta rama**.
Las cuatro marcas son resultados legítimos, y la cuarta es un resultado de primera clase: en un documento
de instrumentos, **nombrar el instrumento que no existe es el trabajo**.

---

## 2. Preámbulo metodológico

El SDV-H lo tiene; el SDV-S lo omitió y el brief prohíbe repetir la omisión. En un documento de medición
el preámbulo no es un formalismo: **es la diferencia entre un dato y una cifra**. Estas son las reglas con
las que se escribió lo que sigue.

**Regla 1 — Una cifra sin fuente no es un dato: es una cifra.** Todo umbral entra con organismo y año, y su
URL en §14. Cuando no hay fuente, se escribe `[SIN FUENTE VERIFICADA — pendiente de consenso científico]`
y **la dimensión sigue existiendo en el catálogo sin poder generar violación**. Rellenar un piso con
plausibilidad es la única forma de mentir que este estándar no puede detectar después.

**Regla 2 — El piso es LEY (no votable); la plenitud es POLÍTICA (votable).** El motor del SDV-H ya pagó
este error una vez —confundió el Óptimo del agua con el Mínimo Absoluto—. En §4 las dos columnas van
separadas **incluso cuando la segunda está vacía**, y cuando no lo están se dice de dónde sale cada una.
La ciencia publica pisos de riesgo; la plenitud la fija la deliberación.

**Regla 3 — La frecuencia no puede ser más fina que el sensor ni que el indicador.** Es el aporte central
de §6.4 y aquí se enuncia como regla de escritura: **declarar una frecuencia más fina que la resolución
temporal del instrumento es la forma técnica de inventar el dato.** Un satélite que vuelve cada 5 días no
produce series diarias; un líquen que responde en años no informa semanalmente.

**Regla 4 — Un instrumento se declara con su incertidumbre.** El número sin su error no es comparable
consigo mismo en el tiempo. De ahí la regla de declarabilidad de §5.3: **una violación cuyo déficit es
menor que la incertidumbre del instrumento no es declarable** — y esa regla tiene cifras verificadas
(§5.3), no retórica.

**Regla 5 — Ningún linaje basta solo.** El propio repositorio ya nombró el ataque: *"Confabulación de
validadores: varias perspectivas comparten el mismo error"*, cuya defensa propuesta es *"diversidad real
de proveedores, fuentes, implementaciones y agentes disidentes"* (`docs/architecture/continuidad_identidad_autogobierno_federado.md`
§10) [VERIFICADO]. La comunidad testigo no sustituye al satélite —no ve la extensión— y el satélite no
sustituye a la comunidad testigo —no ve la causa ni el fraude local— (§6.5).

**Regla 6 — El sensor no puede ser estético.** *"Jardín podado para la foto no es cuidado; se registra lo
que regenera, no lo que adorna"* (Cap. 16.5 §16.5.14). Consecuencia operativa: **una métrica que sube con
el riego ornamental o con la poda para la foto es una métrica enemiga**, y el elenco debe poder
identificarla (§7.4).

**Regla 7 — El guardián oráculo consiente; no mide.** Es canon: *"Ecosistemas (eco-*): consentimiento
otorgado por el guardián oráculo"* (`app/contracts_bp.py`) [VERIFICADO]. Aquí se convierte en regla de
arquitectura: **ninguna medición puede tener como única fuente una aprobación del guardián** (§7.5).

**Regla 8 — Sin dato no castiga; sin dato no aprueba; y la ley no se negocia por ausencia de dato.** El
patrón INV2-EDU —*"la duda sin evidencia no castiga"*— convive con *"mientras no haya resolución, el canon
manda"*. Para la medición esto significa: la ausencia de instrumento **no imputa violación** al
ecosistema, **no le concede certificado de cumplimiento** y **no autoriza a operar** (bandera de opacidad
ecológica, [documento 08](08_INV2-E_invariante.md) §6.3).

**Regla 9 — T13 firma el registro, no la verdad.** El hash prueba que un dato **no cambió** desde que se
firmó; no prueba que el dato sea cierto. Un sensor mal calibrado produce el hash perfecto de una cifra
falsa. Escribirlo evita la confusión más cara de este documento (§7.2).

**Regla 10 — Separar cuatro estados de la evidencia, que es fácil confundir.** (a) existe la fuente y se
leyó; (b) existe la fuente y **no** se pudo abrir (real, bloqueada a agentes); (c) no existe la fuente,
y se buscó; (d) **no puede existir** la fuente por la naturaleza del objeto (el valor inefable, la
frecuencia de reporte de un `eco-`). Las cuatro aparecen aquí y ninguna se disfraza de otra.

**Regla 11 — Nada de este documento autoriza a intervenir.** *Sin dato no hay castigo; sin dato no hay
permiso.* Que el sistema no mida un interior no lo faculta a actuar sobre él, ni a autorizar a terceros.

---

## 3. Pilares epistemológicos

**Pilar 1 — El sujeto no puede reportar, y eso convierte la instrumentación en condición de posibilidad.**
Los reinos humano y sintético **son su propio sensor**; el animal tiene un tutor humano jurídicamente
localizable. El ecosistema no tiene ninguno de los dos: *"Nosotros registramos la interacción, no la vida
interna del ecosistema"* (Cap. 16.5 §16.5.14). De ahí que este documento no sea un anexo técnico del
estándar: es la parte del estándar sin la cual las otras no se pueden aplicar.

**Pilar 2 — La infraestructura de observación es de terceros, y eso es una ventaja antes que una
dependencia.** Sentinel-2 (ESA/Copernicus), Landsat (NASA/USGS), el producto de estrés térmico de arrecifes
(NOAA Coral Reef Watch), los umbrales de sitio de humedales (Convención de Ramsar), los objetivos del
Marco Kunming-Montreal (CBD), las series de bosques (FAO FRA) y los registros de biodiversidad y áreas
protegidas (LPI, Protected Planet) **no pertenecen ni al proyecto ni al beneficiario del daño**. En un
estándar donde el auditor viene del reino que se beneficia del uso, eso no es un detalle logístico: es la
única independencia disponible ([documento 09](09_Comparativa_inter_reinos.md) §7). Su costo también se
declara: **dependencia de la continuidad presupuestaria de un tercero estatal.**

**Pilar 3 — El instrumento también es auditado, y esa es la parte que casi nunca se copia.** Sentinel-2 se
valida de forma **vicaria** contra sitios instrumentados de la red CEOS (Dome-C, La Crau, desiertos) **2-3
veces al año**, y publica informes de calidad de datos **mensuales y anuales**; su calibración la ejecuta
el **OPT-MPC** (Sentinel-2 Optical Mission Performance Cluster), no el usuario, con calibración de señal
oscura **~2 veces al mes** y calibración absoluta de ganancia **1 vez al mes** [VERIFICADO]. Un elenco que
exija transparencia al ecosistema y no al instrumento reproduce, en pequeño, la asimetría que el
T13 prohíbe (§7.4).

**Pilar 4 — El dato puede ser tumbado por acuerdo comunitario, no solo confirmado.** En iNaturalist una
observación **se degrada** a «Casual» por acuerdo de la comunidad, y la degradación aplica a fecha,
ubicación, estado silvestre, evidencia, recencia y **manipulación por IA** (*"artificial intelligence was
used to add, remove, or replace elements in the image or sound"*) [VERIFICADO]. Es el precedente externo
más limpio de «la comunidad testigo puede tumbar el dato, no sólo confirmarlo», y este documento lo adopta
como forma de la auditoría social (§7.3 y §7.6).

**Pilar 5 — La ciencia ciudadana tiene una regla de calidad que no es mayoría simple.** En el marco DQA de
iNaturalist, una observación alcanza **Research Grade** cuando **más de 2/3 de los identificadores
coinciden** a nivel de especie o inferior, y el observador **no puede autoconcedérselo** [VERIFICADO].
Los 2/3 son mayoría calificada, y ese es el umbral trasladable a la comunidad testigo del SDV-E.

**Pilar 6 — T14 — Principio de Precaución Intergeneracional** (Cap. 5) es el axioma más fuerte disponible:
*"Ante incertidumbre sobre el impacto en agentes que no pueden consentir (ecosistemas, generaciones
futuras, posibles consciencias sintéticas), el sistema debe elegir la opción de menor irreversibilidad,
documentando el costo de oportunidad asumido. La carga de la prueba recae sobre quien propone acciones que
afectan a la temporalidad de no-participantes."* Para la medición su consecuencia es exacta: **lo que no
tiene cifra no puede producir una violación, pero tampoco puede autorizarse a ciegas** — se instrumenta y
se bloquea lo irreversible.

**Pilar 7 — Gobernanza operacionalmente finita** (Cap. 10 §10.7): *"La gobernanza debe ser operacionalmente
finita."* Un elenco de sensores con este pilar encima no puede exigir modelar la cadena trófica completa
para decidir. Los cinco linajes son **finitos, nombrados y auditables**; todo lo que exija más que ellos
pertenece a la ciencia, no al estándar.

**Pilar 8 — Datos abiertos y reproducibilidad del veredicto.** La única defensa disponible contra el hecho
de que *el proyecto es juez y parte en la interpretación* es que **cada veredicto pueda recalcularse desde
datos públicos, sin acceso al código del proyecto**. De ahí que la firma T13 (§7.2) tenga que ser
**recalculable por un tercero**: un hash que solo el sistema puede reproducir no es trazabilidad, es
autoridad.

**Pilar 9 — Los ataques ya están catalogados, y el elenco responde a ellos.** El registro del proyecto
(`docs/architecture/continuidad_identidad_autogobierno_federado.md` §10) nombra **«Suplantación de
bosque»** —*un representante cambia su mandato ecológico*— con defensa propuesta: *"fuentes físicas
múltiples, mandato territorial, comunidad testigo y parámetros SDV-E"* [VERIFICADO]. Este documento
convierte esa defensa en arquitectura: **fuentes físicas múltiples** es exactamente la Regla 5 (§2), y los
cinco linajes existen para que ninguna lectura sea la única.

**Pilar 10 — Dignidad encadenada** (Cap. 10 §10.6): *"Dignidad Humana ←→ Dignidad Ecosistémica ←→
Dignidad Material. Cada eslabón depende de los demás."* Un sistema de medición que degrade el territorio
para producir el dato —vuelos innecesarios, sensores que alteran el sitio, acceso que espanta a la fauna—
viola el eslabón que dice proteger. De ahí la regla de **no interferencia del instrumento** (§6.6).

**Pilar 11 — La Directiva Mayor (Axioma 0)**, *"resolver nuestras necesidades de la mejor manera para
todos todos"* —humanos, naturales y sintéticos, presentes y futuros—, es la razón por la que el reino que
no firma con manos necesita instrumentos que hablen por él sin poner palabras en su boca. La Directiva
alcanza a los **tres reinos**, y ese es el motivo de que un elenco de medición no pueda quedarse en el
reino que sí reporta: lo que no se instrumenta no entra en «todos todos», y lo que no entra en la
Directiva Mayor queda, de hecho, fuera de la contabilidad de la vida.

---

## 4. Dimensiones del SDV-E leídas como matriz de medibilidad

Este documento no fija umbrales nuevos: fija **con qué instrumento se lee cada dimensión canónica del
Cap. 10 §10.4**, con qué frecuencia **puede** leerse, quién responde por la lectura y qué hecho concreto
constituye violación. El orden de las ocho dimensiones es el del [documento 09](09_Comparativa_inter_reinos.md)
§6, para que las tablas de la biblioteca se puedan cruzar sin reordenar nada. La novena (salud del suelo)
**no es canónica**: entra desde el ISE y se marca como tal.

**Los cinco operadores del dato** (detalle en [documento 08](08_INV2-E_invariante.md) §5.1, que este
documento no reescribe): `min` (más es mejor), `max` (menos es mejor), `range` (hay un intervalo
admisible), `escalonado` (tabla de niveles, sin interpolar) y `ordinal`/`binary` (presencia/ausencia o
categoría: **no producen déficit, producen estado**).

---

### Dimensión D1: Calidad del aire (el piso que el ecosistema comparte con el humano)

**Qué protege.** La composición del aire que respira la unidad ecológica —y que respira quien vive en ella—.
Es la única dimensión cuyo piso proviene de un organismo internacional con documento primario localizado en
esta rama (la OMS), **aunque su lectura numérica entre `[REPORTADO]`**; el otro piso con cifra del elenco,
el caudal ecológico (D7), llega a través de un documento técnico secundario y así se declara.

| Parámetro | Mínimo Absoluto (el piso = LEY, no votable) | Óptimo (plenitud = POLÍTICA, votable) | Escala intermedia de la OMS (trayectoria, **no** piso) | Fuente |
|---|---|---|---|---|
| PM2.5, media anual | **5 µg/m³** (AQG) | **5 µg/m³** (piso y óptimo coinciden: *"toda reducción adicional es beneficio"*) | IT-4 = **15 µg/m³** | OMS, 2021 (Tabla 0.1) |
| PM2.5, media 24 h | **15 µg/m³** (AQG) | **15 µg/m³** | IT-4 = **25 µg/m³** | OMS, 2021 |
| PM10, media anual | **15 µg/m³** (AQG) | **15 µg/m³** | IT-4 = **20 µg/m³** | OMS, 2021 |
| PM10, media 24 h | **45 µg/m³** (AQG) | **45 µg/m³** | AQG e IT-4 **coinciden** | OMS, 2021 |
| O3, media 8 h | **100 µg/m³** (AQG) | **100 µg/m³** | AQG e IT-4 **coinciden** | OMS, 2021 |
| O3, temporada pico (promedio de los 6 meses consecutivos de mayor O3) | **60 µg/m³** (AQG) | **60 µg/m³** | IT-4 = **70 µg/m³** | OMS, 2021 |
| NO2, media anual | **10 µg/m³** (AQG) | **10 µg/m³** | IT-4 = **30 µg/m³** | OMS, 2021 |
| NO2, media 24 h | **25 µg/m³** (AQG) | **25 µg/m³** | IT-4 = **50 µg/m³** | OMS, 2021 |
| SO2, media 24 h | **40 µg/m³** (AQG) | **40 µg/m³** | IT-4 = **50 µg/m³** | OMS, 2021 |
| CO, media 24 h | **4 mg/m³** (AQG; **la OMS no publica objetivo intermedio para CO**) | **4 mg/m³** | — | OMS, 2021 |
| NO2 1 h · SO2 10 min · CO 8 h | — (la OMS **conserva en 2021** los valores de 2005, sin IT ni AQG nuevos) | — | **200 µg/m³ · 500 µg/m³ · 10 mg/m³** | OMS, 2021 (Tabla 0.2) |
| Carbono negro, partículas ultrafinas, polvo desértico | — | — (**«buenas prácticas» cualitativas**, sin cifra) | — | OMS, 2021 |

**Nota de procedencia de la tabla, exigida por la Regla 1.** Las cifras de la OMS entran como
`[REPORTADO]`, no como `[VERIFICADO]`: el informe de fuentes de esta rama declaró leído el PDF de la OMS
(200), pero **el [documento 08](08_INV2-E_invariante.md) §4 las marca `[REPORTADO]` y su columna de Óptimo
como `[SIN FUENTE VERIFICADA]`**, y este documento repite la procedencia en vez de ascenderla. La columna
«Óptimo» del aire, por tanto, **no está sostenida por una fuente de plenitud: es la coincidencia con el
piso**, tal como se explica abajo. Y una tarea que esta tabla **no** cierra: la conciliación celda por
celda con el catálogo del [documento 07](07_Formula_de_violacion_y_pesos.md) §4 (que lista el piso de
PM2.5 a 24 h como **15 µg/m³**, el AQG de esta tabla, y no el IT-4 de 25 µg/m³ que esta tabla conserva en
su columna de trayectoria). Las dos columnas pueden convivir —**piso en el AQG, trayectoria en el IT-4**—,
pero **quién es piso y quién es trayectoria se decide en el documento 07, no se promedia aquí**; hasta que
esa conciliación conste, D1 se lee como **propuesta de piso `[REPORTADO]`**, no como umbral ratificado.

**Justificación, y la decisión de la biblioteca que este documento acata.** La OMS (2021) es el único
organismo con piso numérico y revisión sistemática de efectos adversos que esta rama pudo documentar.
Sus **objetivos intermedios (IT-1 a IT-4)** son *"objetivo intermedio progresivo hacia el AQG; sirve para
guiar la reducción donde las concentraciones exceden el AQG"* [VERIFICADO en el informe de fuentes] — es
decir, **son una trayectoria, no un piso**. El informe de fuentes de esta rama los propuso como «candidato
natural a Mínimo Absoluto»; **el [documento 07](07_Formula_de_violacion_y_pesos.md) —propietario de la
fórmula y de los umbrales en esta biblioteca— ratificó el AQG como piso**, y con una decisión explícita:
*"En el aire, el Mínimo Absoluto y el Óptimo valen lo mismo: 5 µg/m³ anual de PM2.5"*, con el criterio
*"toda reducción adicional es beneficio"* [VERIFICADO: documento 07 de esta biblioteca, §4]. **Este
documento acata esa asignación** por dos razones: (i) una biblioteca no puede dejar dos pisos vivos para el
mismo parámetro, y (ii) de las dos lecturas, **el AQG es la más protectora** —el IT-4 es más permisivo, no
más exigente—. La consecuencia se acepta sin maquillaje: **con el piso en el AQG, buena parte de la
atmósfera habitada del planeta está por encima de su SDV-E de aire**, y eso es un hallazgo del estándar,
no un defecto de la medición.

**Procedencia exacta de las cifras de esta tabla, sin ascenderla de grado.** Las filas de la OMS
entran como `[REPORTADO]`: el informe de fuentes de la rama **no registró la lectura numérica del texto
primario** (el PDF de 300 pp. servido por IRIS sí respondió 200, pero su contenido numérico no se asentó en
el informe), y el [documento 08](08_INV2-E_invariante.md) §4 lo declara en los mismos términos —*"OMS,
2021 (valor `[REPORTADO]`; URL en el bloque de trazabilidad, 200)"*— y marca **cada Óptimo de aire como
`[SIN FUENTE VERIFICADA]`**. Aquí no se corrige ese grado hacia arriba: **una cifra `[REPORTADO]` sostiene
una propuesta, no una violación ejecutable**, y por eso D1 queda marcada como dimensión cuyo piso **debe
leerse de la fuente primaria antes de ratificarse**. Y una precisión de consistencia con el
[documento 08](08_INV2-E_invariante.md) §4.1, que no se oculta: **el aire de la OMS es un proxy de salud
humana**, no un umbral de integridad ecosistémica; entra como piso **compartido y declarado como proxy**,
que es lo que la matriz de §4.10 llama «proxy declarado de salud».

**Segunda consecuencia, y es de diseño: cuando el piso y el óptimo coinciden, el óptimo no es votable.**
Una columna «Óptimo (POLÍTICA, votable)» con el mismo número que el piso **no ofrece nada que votar**: el
Parlamento no puede fijar una plenitud distinta de la ley. Para que la distinción LEY/POLÍTICA no se vuelva
decorativa en esta dimensión, el Óptimo se lee como **techo de convergencia** —la plenitud es *alcanzar el
piso*, que es lo que afirma *"toda reducción adicional es beneficio"*—, y la POLÍTICA se ejerce donde sí hay
grados: **la trayectoria** (qué IT se adopta como etapa, con qué plazo y con qué verificación) y **la
prioridad de instrumentación**. Separar las columnas cuando valen lo mismo es correcto; fingir que hay dos
números donde hay uno, no.

**Y una fila que es techo, no piso, aunque esté en la columna del medio.** Los valores conservados de 2005
—**NO2 1 h (200 µg/m³), SO2 10 min (500 µg/m³), CO 8 h (10 mg/m³)**— son **máximos de exposición de corto
plazo**, no pisos: por debajo de ellos **nada mejora y nada se gana**. Si se leyeran como «Mínimo Absoluto»
el operador `max` los volvería absurdos (el déficit crecería al mejorar el aire). Entran como **techo
convergente de la misma familia que el Óptimo**, no como suelo de dignidad.

**Lo que se conserva de la lectura no adoptada, y por qué no se borra.** Los valores **IT-4** siguen en la
tabla, en su propia columna, con su nombre: son la **escala declarada de trayectoria** que la OMS publica
para unidades que están muy por encima del piso, y sirven para graduar la respuesta (alerta, plan de
reducción, prioridad de instrumentación) **sin convertirse en derecho a contaminar**. Un piso que se
negocia por etapas deja de ser un piso: es una trayectoria con nombre de ley.

**Protocolo.** Linaje **A** (teledetección: aerosoles y espesor óptico) como cobertura; linaje **B**
(estaciones de monitoreo calibradas) como medición sancionable; **D** (ciencia ciudadana) para el contraste
local. Frecuencia **impuesta por la fuente**: **anual** para la exposición de largo plazo (PM2.5, PM10,
NO2), **24 h** para el corto plazo (PM2.5, PM10, NO2, SO2, CO), **8 h** para O3 y CO, y **temporada pico**
para O3 (promedio de los 6 meses consecutivos de mayor O3) `[REPORTADO]` por el informe de fuentes. Es
decir: **el veredicto de aire es anual, con alertas de 24 h**; no existe veredicto horario con fuente.

**Violación.** Un promedio **anual** de PM2.5 —o el del contaminante y la ventana que correspondan— medido
por estación calibrada **por encima del AQG** (5 µg/m³ anual), con **periodo, instrumento y unidad
declarados**. Es un hecho medido con unidad, ventana y fuente — no una apreciación. Tres precisiones que
esta dimensión necesita más que ninguna otra:

1. **Una violación puntual no necesita tres señales; la persistente sí.** Esta es la dimensión donde la
   regla de §5.5 se puede leer mal: **una** medición admisible por encima del piso **declara violación
   puntual**; las **tres señales de linajes distintos** se exigen para la violación **persistente** que
   escala a retractación y veto (documento 08 §8.6). Exigir tres linajes para toda violación dejaría a D1
   sin poder declarar nada, porque solo el linaje B es sancionable aquí.
2. **La incertidumbre también es un campo de esta dimensión.** La red se calibra contra patrón, pero
   **el informe de fuentes no fijó la incertidumbre de la medición de aire**: sin error declarado, la
   regla de declarabilidad de §5.3 no puede aplicarse por número. Consecuencia explícita y `[HIPÓTESIS]`
   del proyecto: **una estación sin incertidumbre declarada registra y no declara violación**, del mismo
   modo que el aire entra como proxy mientras su valor siga siendo `[REPORTADO]`.
3. **Un aviso de coherencia interna: la misma cifra no puede ser violación en este documento y
   cumplimiento en el documento 07**; si esa divergencia reaparece, el error está aquí.

---

### Dimensión D2: Calidad del agua (el piso que esta rama NO pudo cerrar)

**Qué protege.** La integridad fisicoquímica del cuerpo de agua: oxígeno disuelto, pH, nutrientes,
contaminantes.

| Parámetro | Mínimo Absoluto (LEY) | Óptimo (POLÍTICA) | Fuente |
|---|---|---|---|
| Oxígeno disuelto | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` | `[SIN FUENTE VERIFICADA]` | la ruta consultada del organismo competente **está muerta (404)** |
| pH | `[SIN FUENTE VERIFICADA]` en esta rama (el [documento 08](08_INV2-E_invariante.md) §4.1 usa un **proxy declarado** de agua de riego, FAO 1985) | `[SIN FUENTE VERIFICADA]` | — |
| Nitrógeno / fósforo / metales | `[SIN FUENTE VERIFICADA]` | `[SIN FUENTE VERIFICADA]` | — |

**Justificación de la ausencia, que es el resultado.** No es un fracaso de búsqueda: es un hallazgo de la
rama. Las rutas de los indicadores de oxígeno del organismo europeo devolvieron **404**; la ruta de
criterios de vida acuática consultada devolvió **404**; y la tabla general de criterios **sí responde 200
pero su contenido numérico no se abrió en la sesión de verificación**. Escribir un número aquí sería el
único error irrecuperable de este documento: un piso de oxígeno inventado gobierna contratos.

**Protocolo.** Linaje **B** (sondas in-situ de oxígeno, pH y conductividad; muestreo de laboratorio para
nutrientes y contaminantes) + **A** (turbidez y temperatura superficial por teledetección, como cobertura,
nunca como veredicto). Sin umbral verificado, el instrumento **registra** y no puede activar INV2-E (regla
del [documento 09](09_Comparativa_inter_reinos.md) §6: *sin definición operativa de violación no hay
violación*). **La deuda pertenece al documento 23** de esta biblioteca.

**Violación.** Hoy, por número: **ninguna declarable**. Por hecho verificable: **un vertido declarado o
documentado** sobre la unidad —hecho administrativo, no umbral— y la **ausencia de instrumentación**
(bandera de opacidad ecológica, que no es sanción al territorio sino condición de validez del contrato).

---

### Dimensión D3: Área mínima para biodiversidad viable (la dimensión que el satélite ve y el canon no cifró)

**Qué protege.** La extensión y la estructura del ecosistema: por debajo de cierto tamaño, la biodiversidad
viable deja de ser viable. El canon lo nombra (Cap. 10 §10.4) y **no publica su cifra**.

| Parámetro | Mínimo Absoluto (LEY) | Óptimo (POLÍTICA) | Fuente |
|---|---|---|---|
| Área mínima viable | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` | **≥ 30 %** de restauración de ecosistemas degradados para 2030 (Meta 2 GBF) · **≥ 30 %** conservado y gestionado eficazmente para 2030 (Meta 3 GBF, «30x30») | CBD, 2022 (Decisión 15/4) |
| Definición operativa de «bosque» para verificar cobertura por teledetección | **≥ 0,5 ha · ≥ 10 % de cobertura de dosel · ≥ 5 m de altura** (definición FRA de la FAO) | — | FAO (FRA, definición 2020) `[REPORTADO]`: **la URL responde 200, su contenido numérico no se leyó** en la sesión de verificación |
| Extinción inducida por humanos de especies amenazadas conocidas | **0** (detención) | — | CBD, 2022 (Meta 4 GBF) |
| Crisis de extinción (contexto, no umbral) | — | — | IPBES, 2019: **~1 000 000** de especies de animales y plantas amenazadas |

**Justificación.** Las metas del Marco Kunming-Montreal son **anclas de política global**, no umbrales de
una unidad concreta: usarlas como «el piso de este bosque» sería abuso de la fuente (lo advierte el
[documento 08](08_INV2-E_invariante.md) §4.1). La definición de bosque de la FAO **no es un área mínima
viable**: es el umbral por debajo del cual la cobertura **no se cuenta como bosque**. Fundir ambas cosas
sería el mismo error que usar los > 20 m de ancho de esa definición como «protección de ribera» (§D8).

**Protocolo.** Linaje **A** como instrumento primario, con las especificaciones verificadas de la §6.2
(**Sentinel-2**: 5 días nominales de constelación / 10 días por satélite; **Landsat 8+9**: 8 días
combinados / 16 por satélite; 30 m de resolución). **D** y **C** para lo que el píxel no ve (D3 no se lee
solo desde arriba: el bosque primario —«ausencia de indicios de actividad humana»— no es observable por
satélite, [documento 10](10_Ecosistemas_Bosques.md) §6.1). **E** para la declaración de régimen.

**Violación.** **Pérdida neta de cobertura dentro del polígono declarado**, verificada con **dos imágenes
de la misma constelación** y magnitud **superior a la incertidumbre** del instrumento (§5.3). Mientras no
exista piso ratificado, esa pérdida **no es todavía una violación numérica**: es un hecho que **activa T14**
(bloqueo precautorio sobre la acción irreversible) y obliga a re-declarar la línea base. Y una precisión
que evita el fraude más fácil: **una parcela de 0,4 ha de cobertura boscosa no es «bosque perdido» ni
«bosque conservado»: es cobertura fuera de la definición, y el estándar debe decirlo así.**

**Y el techo de esta dimensión, que es el error simétrico.** D3 solo declara violación por **pérdida**. La
**ganancia declarada no es regeneración**: un proyecto que revegeta con una sola especie, riega para la
foto o cuenta como «restauración» una plantación sin dosel **mueve la métrica sin regenerar** (Regla 6).
Por eso la misma regla de declarabilidad se aplica **en los dos sentidos**: un aumento **menor que la
incertidumbre multitemporal (1 %)** no se puede atribuir al ecosistema, y un aumento **no acompañado de
estructura verificable en campo (linaje B/D)** es un cambio de cobertura, no un hecho de regeneración.

---

### Dimensión D4: Fauna acuática viable (el piso que existe, pero para otra pregunta)

**Qué protege.** Que la unidad siga sosteniendo poblaciones de fauna acuática —el indicador vivo de que el
agua y el hábitat sirven.

| Parámetro | Mínimo Absoluto (LEY) | Óptimo (POLÍTICA) | Fuente |
|---|---|---|---|
| Aves acuáticas: sitio de importancia internacional (Criterio 5 de Ramsar) | **≥ 20 000** individuos regularmente presentes | — | BTO, 2024 — **umbral de sitio que aplica** el Criterio 5; el texto de la Convención **no se abrió** (403) |
| Aves acuáticas: 1 % de una población (Criterio 6) | **≥ 1 %** de los individuos de una población biogeográfica | — | BTO, 2024 — umbral de sitio que aplica el Criterio 6 (fuente secundaria verificada) |
| Umbral mínimo de conteo cuando el 1 % es muy pequeño | **50** individuos | — | BTO, 2024 (regla operativa del Criterio 6) |
| Tendencia de poblaciones (contexto) | — | — | Living Planet Index (portal verificado, sin cifra usada aquí) |

**Justificación, con su límite dicho en la misma línea.** Estos números **califican un humedal como de
importancia internacional**; **no son una población mínima viable**. El traslado —«si la unidad deja de
cumplir el Criterio 5, viola su piso»— es `[HIPÓTESIS]` de este documento y debe ratificarse. Además, la
procedencia queda declarada: **`ramsar.org` bloquea a los agentes automáticos (403)** y el número se cita
a través de BTO, fuente secundaria verificada (200). La cifra es la misma; **la procedencia no**: el
original está pendiente de apertura humana.

**Y hay que decir qué es exactamente lo que se leyó.** En BTO se leyeron **umbrales de sitio**: niveles
numéricos que BTO publica **para aplicar** los Criterios 5 y 6 —y su regla operativa de **50 individuos**
—*"where 1% of the national population is less than 50 birds, 50 is normally used as a minimum qualifying
threshold for the designation of sites of national or international importance"*— es de BTO, no del texto
de la Convención—. **El texto del Criterio 5 no se leyó en la fuente primaria** en la sesión de esta rama:
la formulación que BTO reproduce —*"any site regularly supporting 20,000 or more waterbirds also
qualifies"*— entra `[REPORTADO]` y su redacción debe confirmarse con la fuente original abierta por un
humano antes de ratificar D4. Confundir **el umbral de sitio que una fuente secundaria aplica** con **el
criterio que la Convención escribe** sería el mismo error de categoría que este documento denuncia en D3
(definición de bosque ≠ área mínima viable) y en D8 (ancho de la definición de bosque ≠ protección de
ribera).

**Protocolo.** Linaje **D** (conteos voluntarios con protocolo, tipo BTO/WeBS) + **C** (bioindicadores:
macroinvertebrados, aves como indicador agregado) + **B** (hábitat: caudal, oxígeno, temperatura). La
revisión **general** de los umbrales la hace **Wetlands International cada 3 años**, y la de los umbrales
del **1 %** cada **9 años** (Resolución VI.4 de Ramsar) — dato `[REPORTADO]` por BTO. Es el único caso del
elenco en que **la frecuencia de revisión del umbral tiene fuente externa**; conviene precisar además que
**es una frecuencia de revisión del umbral, no de medición de la unidad** (§6.4.c los separa): el conteo
del sitio puede ser anual aunque el umbral que lo juzga cambie cada tres o nueve años.

**Violación.** El conteo **regularmente presente** en la ventana declarada **no alcanza el umbral** que
calificaba al sitio en la línea base, medido con **el mismo protocolo y la misma ventana estacional**.
Cambiar de protocolo y declarar violación es fabricar el resultado (§6.7).

**Y la precisión que impide fabricar la violación por la vía del conteo:** lo que la fuente exige es
**presencia regular** —*"regularly supporting 20,000 or more waterbirds"* en la formulación que BTO
reproduce del Criterio 5—, no presencia en una temporada. Una **ausencia puntual** —una mala temporada, un
año seco, un censo incompleto— **no es violación**: la caída tiene que sostenerse en el patrón de presencia
para que el umbral de sitio deje de cumplirse. Fijar esa ventana es `[HIPÓTESIS]` de este documento y
**debe ratificarse antes de usar D4 como juez**; hasta entonces D4 se lee como **umbral de otra pregunta**
(la matriz de §4.10), no como piso de población mínima viable.

---

### Dimensión D5: Conectividad con otros ecosistemas (instrumento sí, umbral no)

**Qué protege.** Que la unidad no sea una isla: corredores, continuidad, posibilidad de flujo génico.

| Parámetro | Mínimo Absoluto (LEY) | Óptimo (POLÍTICA) | Fuente |
|---|---|---|---|
| Conectividad del paisaje | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` | **≥ 30 %** conservado en sistemas *"ecológicamente representativos, bien conectados y gobernados equitativamente"* para 2030 (Meta 3 GBF) | CBD, 2022 — **exige «bien conectados» y NO fija ningún umbral numérico de conectividad** |
| Índice PC (probabilidad de conectividad) | `[SIN FUENTE VERIFICADA]` | `[SIN FUENTE VERIFICADA]` | el artículo primario **no se leyó** en la sesión de verificación |

**Justificación.** Es el caso puro de la regla del documento 09 §6: **hay instrumento y no hay umbral**.
El instrumento existe y es barato —distancia al borde y métricas de fragmentación calculadas sobre la capa
de cobertura ([documento 10](10_Ecosistemas_Bosques.md) §6.1, dimensión VI)— pero **ninguna institución
verificada publica el número**. Inventarlo sería convertir una decisión política en apariencia de ciencia.

**Protocolo.** Linaje **A** (capa de cobertura multitemporal) + **C**/**D** para verificar que un corredor
declarado es **transitable** y no solo dibujado (una franja sin dosel ni fauna que la use es un corredor en
el mapa, no en el territorio).

**Violación.** **Ninguna declarable hoy.** Se registra y se reporta al tablero; **no puede activar
INV2-E** por número. Sí puede activar T14 si la acción propuesta es irreversible y afecta a la única
conexión existente.

---

### Dimensión D6: Ciclos naturales respetados — fuego, inundación, sequía (dimensión binaria sin peso)

**Qué protege.** Que el ecosistema conserve sus **regímenes**: el fuego que renueva, la inundación que
fertiliza, la sequía que selecciona. *"Ciclos naturales respetados (fuego, inundación, sequía)"*
(Cap. 10 §10.4).

| Parámetro | Mínimo Absoluto (LEY) | Óptimo (POLÍTICA) | Fuente |
|---|---|---|---|
| Régimen declarado | **Régimen presente y declarado** (presencia/ausencia, sin grados) | Periodicidad, severidad y estacionalidad del régimen (votable) | canon sí, cifra no |
| Superficie afectada por fuego | — | — | series verificadas como portal de datos; **el dato que hace falta —fuego prescrito frente a incendio— no existe** ([documento 10](10_Ecosistemas_Bosques.md) §6.1) |

**Justificación.** Entra como **dimensión binaria auditable sin peso**, con el precedente canónico de las
dimensiones VIII (Rehabilitación) y IX (Opacidad Vital) del SDV-H: *"se registran cualitativamente y
mediante umbrales binarios (presencia/ausencia del derecho), no mediante pesos en la fórmula […] medir la
rehabilitación o la opacidad con la misma vara cuantitativa que el agua o la vivienda las destruiría"*
(Cap. 8 §8.11). Un régimen no se promedia.

**Protocolo.** Linaje **E** (registro documental del régimen **declarado** y su historial) + **A**
(superficie afectada, series satelitales) + **D** (testigos del evento). La declaración del régimen es,
por definición, un acto de la comunidad de custodia: **ninguna serie pública puede verificar por ella si
el fuego de un año fue prescrito o provocado.**

**Violación.** **Interrupción verificada del régimen declarado** (p. ej. una llanura que lleva décadas sin
fuego por supresión activa, o un río cuyo pulso de inundación fue eliminado por una obra). Es un hecho
binario con evidencia documental y testimonial, no un déficit porcentual.

---

### Dimensión D7: Caudal mínimo ecológico (el piso que esta rama SÍ pudo cerrar, con un método)

**Qué protege.** El agua que debe quedar en el río para que el río siga siendo río. El canon lo exige
como parte del SDV de un **lugar**: *"Un río tiene un SDV que incluye: Caudal mínimo ecológico […]"*
(Cap. 10 §10.4).

| Parámetro | Mínimo Absoluto (LEY) | Óptimo (POLÍTICA) | Fuente |
|---|---|---|---|
| Caudal ecológico, método Tennant: degradación severa del hábitat | **< 10 % del caudal medio anual (QAA)** | — | Tennant, 1975, **citado a través de documento técnico del Estado de Alaska** |
| Caudal ecológico, rango óptimo | — | **60-100 % del QAA** | Tennant, 1975 (misma fuente) |
| Caudal de lavado (*flushing*) del sustrato | — | **200 % del QAA** (evento corto) · revisión posterior: **≥ 400 % durante 3-7 días** (Estes, 1984) | Tennant, 1975 y Estes, 1984, vía el mismo documento |
| Caudal ecológico (definición normativa) | — | — (definición **sin cifra**): *"el agua provista dentro de un río, humedal o zona costera para mantener los ecosistemas y sus beneficios donde hay usos competidores y donde los caudales son regulados"* | ECRR (European Centre for River Restoration) |

**Justificación y procedencia, dichas juntas.** El método Tennant **sí tiene cifra** y esa cifra se leyó en
un documento técnico **legible** del Estado de Alaska que lo cita; **el artículo original de Tennant (1975)
no se pudo leer** (PDF truncado en la descarga) y **la Declaración de Brisbane (2007), URL ancla del brief,
está muerta (404)**: por eso **no se cita su texto**. Es decir: este documento **cierra parcialmente** el
hueco que el [documento 08](08_INV2-E_invariante.md) §4.1 declaró abierto (`caudal_ecologico_pct_qma` =
`[SIN FUENTE VERIFICADA]`) y lo hace **con la procedencia a la vista**: el piso existe como **umbral de un
método hidrológico**, no como número universal. Tennant se calibró en ríos templados con régimen
determinado; **aplicarlo a un río tropical, de régimen torrencial o intermitente es una decisión
metodológica que debe declararse** `[HIPÓTESIS]` y no un dato heredado. La revisión posterior de Estes
(1984) sube el caudal de lavado: la cifra no es única en la propia literatura.

**Protocolo.** Linaje **B** (estación de aforo de cierre de subcuenca, con serie) + **A** (cobertura nival
y extensión de agua como forzante) + **E** (registro de extracciones y concesiones). Frecuencia **impuesta
por la fuente**: la referencia es el **caudal medio anual** (ventana anual) y el caudal de lavado es un
**evento corto de 3-7 días** [VERIFICADO]. Un veredicto de caudal sin serie anual no existe: con un solo
año se mide el clima, no el río.

**Violación.** **Caudal medido por debajo del 10 % del QAA** durante la ventana declarada → degradación
severa del hábitat (hecho medido, con estación, serie y método declarados). Y una segunda violación, esta
administrativa: **extracción sin caudal ecológico fijado en la concesión** cuando la unidad tiene serie
suficiente para fijarlo.

**Con dos límites que esta dimensión debe decir de sí misma.** (i) **Dependencia de un umbral que el
documento 08 todavía declara abierto**: su catálogo marca `caudal_ecologico_pct_qma` como `[SIN FUENTE
VERIFICADA]` y **remite a la Declaración de Brisbane** —cuya URL está muerta (404) y cuyo texto este
documento no cita—. Aquí se cierra **con un método, no con un número universal**, así que la violación de
D7 es declarable **solo si el método Tennant se declara aplicable a esa unidad**; en un río tropical,
torrencial o intermitente, el umbral no es heredable. (ii) **El 10 % no es un mínimo ecológico universal:**
es el borde de «degradación severa» de una clasificación de calidad de hábitat calibrada en ríos templados
—la propia fuente ofrece un rango óptimo de 60-100 %—, de modo que **la distancia entre el piso y la
plenitud aquí no es retórica: es de un orden de magnitud**, y el estándar no debe presentar el 10 % como si
fuera el punto donde el río «está bien».

---

### Dimensión D8: Riberas protegidas (la franja que el píxel no resuelve)

**Qué protege.** La franja de vegetación que sostiene el borde del agua: sombra, filtro de sedimentos,
hábitat, estabilidad del cauce.

| Parámetro | Mínimo Absoluto (LEY) | Óptimo (POLÍTICA) | Fuente |
|---|---|---|---|
| Franja de vegetación riparia | **Presencia de franja** (binario: existe / no existe) | Ancho, continuidad y composición (votable) | canon sí, cifra no |
| Ancho mínimo | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` | `[SIN FUENTE VERIFICADA]` | — |

**Justificación, y una trampa que hay que nombrar.** El único número cercano que apareció en esta rama es
el «> 20 m de ancho» que la FAO usa **para definir bosque**, no para proteger riberas. Usarlo como umbral
riparío sería exactamente el abuso que el [documento 08](08_INV2-E_invariante.md) §4.1 prohíbe. Sin umbral,
la dimensión entra como **binaria sin peso** (precedente Cap. 8 §8.11).

**Protocolo.** Linaje **A** con un límite duro que hay que decir: **Sentinel-2 tiene 4 bandas a 10 m, 6 a
20 m y 3 a 60 m** [VERIFICADO]. Una franja riparia de 5 m de ancho **está por debajo del píxel más fino**:
pretender medirla por teledetección es medir la interpolación, no la ribera. Se verifica con **B** y **D**
(transectos, GPS de campo, ciencia ciudadana) y el satélite se usa solo para **cambios de uso del suelo en
el entorno**, que sí son visibles a 10 m.

**Violación.** **Desaparición de la franja allí donde la línea base declarada la registraba** (hecho
binario, verificado en campo). Un ancho menor no es violación sin piso; un ancho **cero** es un hecho.

---

### Dimensión D9 (NO canónica; entra desde el ISE): Salud del suelo

**Qué protege.** La capa viva sobre la que se sostiene todo lo demás. **El canon no la nombra** entre las
dimensiones del SDV-E: entra desde el Índice de Salud Ecosistémica, que le asigna **15 %** de peso
(documento interno del proyecto, `docs/architecture/metricas_detalle_kpis_oraculos_dinamicos.md`
`[REPORTADO]`). Se marca por eso como no canónica.

| Parámetro | Mínimo Absoluto (LEY) | Óptimo (POLÍTICA) | Fuente |
|---|---|---|---|
| Carbono orgánico del suelo (COS) | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` | `[SIN FUENTE VERIFICADA]` | FAO publica **mapas** (GSOCmap) y **guía metodológica** (informe GSOCseq, 169 pp. descargado y navegado), **no umbrales** |
| Erosión tolerable, sellado | `[SIN FUENTE VERIFICADA]` | `[SIN FUENTE VERIFICADA]` | — |

**Justificación.** El informe de suelos de la FAO leído en esta rama **no es un estándar de umbral**: es
cartografía con guía metodológica. Confundir un mapa con un piso es el error simétrico a confundir una
definición con una protección. Frecuencias propuestas por el [documento 14](14_Ecosistemas_Suelos_vivos.md)
§6.2 (COS cada 3-5 años; erosión y sellado anuales) se citan **como suyas**, `[HIPÓTESIS]` allí.

**Protocolo.** Linaje **B** (laboratorio: COS, densidad aparente) + **A** (sellado y cambios de uso por
teledetección) + **D** (observación estructurada de campo). **Sin umbral, el instrumento registra y no
pondera**: asignarle peso sería diluir el déficit (documento 08 §4.2).

**Violación.** Por número: ninguna. Por hecho: pérdida documentada de COS respecto de la línea base
declarada, o sellado neto de superficie, **registrados** y reportados al tablero.

---

### 4.10 Matriz resumen: qué linaje sostiene cada dimensión

| Dimensión (Cap. 10 §10.4) | A · Satélite | B · In-situ | C · Bioindicador | D · Ciencia ciudadana | E · Testigo + abiertos | Operador | ¿Activa INV2-E hoy? |
|---|---|---|---|---|---|---|---|
| D1 Calidad del aire | 🟡 cobertura | 🟢 **piso** | 🔴 | 🟡 contraste | 🟡 series | `max` | 🟢 sí (proxy declarado de salud) |
| D2 Calidad del agua | 🟡 cobertura | 🟡 instrumento sin umbral | 🟡 | 🟡 | 🟡 | — | 🔴 no (sin umbral) |
| D3 Área mínima viable | 🟢 **piso operativo** (pérdida neta) | 🟡 campo | 🟡 | 🟡 | 🟢 declaración | `min` / binario | 🟡 hecho sí, número no |
| D4 Fauna acuática viable | 🔴 | 🟡 hábitat | 🟢 **umbral de sitio** | 🟢 conteo | 🟢 | `min` | 🟡 umbral de otra pregunta |
| D5 Conectividad | 🟢 instrumento | 🔴 | 🟡 | 🟡 | 🟡 | — | 🔴 no (sin umbral) |
| D6 Ciclos naturales | 🟡 series | 🔴 | 🟡 | 🟢 testigos | 🟢 **declaración** | `binary` | 🟡 binaria, sin peso |
| D7 Caudal mínimo ecológico | 🟡 forzante | 🟢 **piso (Tennant)** | 🟡 | 🟡 | 🟢 concesiones | `min` | 🟢 sí (con método declarado) |
| D8 Riberas protegidas | 🟡 **no resuelve < 10 m** | 🟢 campo | 🟡 | 🟢 | 🟢 | `binary` | 🟡 binaria, sin peso |
| D9 Salud del suelo (no canónica) | 🟢 sellado | 🟢 laboratorio | 🟡 | 🟡 | 🟡 | — | 🔴 no (sin umbral) |

**Lectura de la matriz, en dos frases.** **Ninguna dimensión depende de un solo linaje**, y **solo dos
dimensiones (D1 y D7) tienen hoy piso con cifra** —con el grado de evidencia que su propia sección declara:
**el aire como `[REPORTADO]` y proxy de salud humana, el caudal como umbral de un método hidrológico**—.
Todo lo demás tiene instrumento, tiene registro y no
tiene umbral: **se mide, se firma, se publica y no puede declarar violación por número**. Ese es el estado
real del estándar, y la §13 lo cuenta como lo que es: deuda de consenso científico, no de ingeniería.

**Dos precisiones que la matriz no puede decir en una celda, y que se dicen aquí para que no se lean mal.**

- **D1: el umbral está asignado, la evidencia de entrada está `[REPORTADO]`.** Decir «🟢 sí» significa que
  **existe un umbral al que apuntar** (el AQG, ratificado por el [documento 07](07_Formula_de_violacion_y_pesos.md)),
  no que la cifra esté verificada en esta rama: por eso **una violación de aire queda condicionada a que el
  valor se lea de la fuente primaria y a que la estación declare su incertidumbre** (§D1). Sin esas dos
  condiciones, el veredicto de D1 es `indeterminado` aunque el umbral exista.
- **D3: «piso operativo» quiere decir regla de declaración, no umbral numérico.** Lo que D3 tiene es un
  **criterio de declarabilidad** —pérdida neta superior a la incertidumbre del instrumento—, y su magnitud
  admisible **depende de qué Sentinel-2 o Landsat la mida**: 1 % multitemporal para el linaje A. Ese
  criterio **no es un área mínima viable** y no debe citarse como si lo fuera.

---

## 5. Fórmula de violación, pesos y umbrales: lo que la medición debe aportar

Este documento **no fija la fórmula** ([documento 07](07_Formula_de_violacion_y_pesos.md)). Fija las
condiciones que un dato debe cumplir para que la fórmula no se convierta en aritmética decorativa.

### 5.1 Un dato no es un número: es un número con operador, unidad y ventana

| Operador | Qué exige del instrumento | Ejemplo del catálogo |
|---|---|---|
| `min` | una serie con referencia declarada | caudal ecológico (% del caudal medio anual) |
| `max` | un promedio con ventana explícita | PM2.5 (µg/m³ **anual**) |
| `range` | **dos** límites y un instrumento calibrado en ambos extremos | pH |
| `escalonado` | una tabla de niveles; el instrumento **no interpola** entre ellos | estrés térmico de arrecife (DHW acumulado) |
| `ordinal` / `binary` | un hecho con evidencia documental | régimen de fuego; franja riparia |

**Regla de unidad dura:** **CO se mide en mg/m³ y el resto de contaminantes del aire en µg/m³** (OMS,
2021). Confundir la unidad multiplica por mil el veredicto. El sistema debe declarar la unidad en el propio
campo del dato, sin conversiones implícitas ([documento 08](08_INV2-E_invariante.md) §6.1).

### 5.2 El déficit, normalizado, y la condición de comparabilidad

Se adopta la forma normalizada —`déficit = (requerido − actual) / requerido`—, coherente con el motor
([documento 08](08_INV2-E_invariante.md) §5.1). Tres condiciones vienen del lado de la medición:

1. **Misma ventana temporal.** Dos datos de aire de años distintos no se comparan.
2. **Misma área de referencia declarada**, con fecha e inmutable retroactivamente ([documento 10](10_Ecosistemas_Bosques.md)
   §6.3), o el resultado mide el cambio de polígono, no el cambio del ecosistema.
3. **Prohibido promediar bases distintas.** El [documento 10](10_Ecosistemas_Bosques.md) §6.2 documentó
   un cociente entre dos agregados calculados sobre conjuntos de reporte diferentes que circuló como
   cifra: dos promedios no emparejados no se dividen. La regla se generaliza: **ningún índice del SDV-E se
   calcula como cociente de dos agregados con distinta base de reporte.**

**La forma de arriba vale para el operador `min`; para `max` va con suelo en cero, y esa diferencia es la
que impide que mejorar el aire produzca déficit.** El [documento 07](07_Formula_de_violacion_y_pesos.md) §5.1
fija `D = max(0, (actual − requerido) / requerido)` para `max` —PM2.5, PM10, NO₂, O₃, SO₂, CO, erosión—, con
el techo explícitamente **sin límite por arriba** (un PM2.5 de 50 µg/m³ contra un piso de 5 da 9,0). Las dos
consecuencias que la medición debe respetar: **el `max(0, ·)` no es cosmético** —sin él, un valor mejor que
el piso daría déficit negativo y el factor de violación premiaría la contaminación cero con un número que no
existe— y **el `range` exige dos instrumentos**, no uno ([documento 08](08_INV2-E_invariante.md) §5.1). Este
documento no fija la fórmula: fija que **el dato que entra tiene que traer el operador**, o la aritmética se
aplica al revés.

### 5.3 La incertidumbre del instrumento es parte del dato (la regla de declarabilidad)

> **Regla `[HIPÓTESIS]` — Declarabilidad de una violación.**
> Un déficit **solo puede declararse violación** si su magnitud **supera la incertidumbre declarada del
> instrumento** que lo mide. Un déficit menor que el error del instrumento es **indeterminado**, no
> violación.

No es una precaución retórica: tiene cifras. La especificación verificada de Sentinel-2 (ESA/Copernicus)
fija **incertidumbre radiométrica absoluta < 5 % (meta 3 %)**, **incertidumbre relativa multitemporal
1 %**, **incertidumbre relativa entre bandas 3 %**, **geolocalización absoluta de 20 m (2σ) sin puntos de
control y 12,5 m (2σ) con ellos**, **registro multitemporal entre fechas ≤ 0,3 píxeles (2σ)** y
**corregistro entre bandas de 0,30 (3σ) de la banda más gruesa** [VERIFICADO]. Consecuencias duras:

- Un cambio de cobertura **menor que la incertidumbre multitemporal (1 %)** no se puede atribuir al
  ecosistema: puede ser el sensor.
- Un desplazamiento **menor que el error de geolocalización (20 m sin GCP)** no distingue «el bosque se
  movió» de «la imagen se movió».
- Una franja **menor que el píxel** (10 m en las bandas de 10 m) no se resuelve por satélite, se declare
  la frecuencia que se declare (§D8).

**Una advertencia de fecha sobre los 5 días, que no cambia los umbrales pero sí la frase.** Los **5 días**
son la **revisita nominal de la constelación de dos satélites** (y **10 días** la de un satélite
individual); con la campaña de extensión de Sentinel-2A vigente desde marzo de 2025, la constelación
operativa pasa por tres unidades y la revisita mejora **con condiciones de visión distintas**, que no son
comparables entre sí. Para el estándar esto importa por una razón concreta: **una serie construida con
geometrías de observación mezcladas no es una serie homogénea**, y por eso la regla de continuidad
instrumental (§6.7) obliga a declarar el cambio de configuración de constelación igual que un cambio de
sensor. El techo físico se cita como **diseño de misión**, no como promedio de disponibilidad real:
**nubes, ángulo y prioridad de adquisición recortan lo que la órbita promete.**

**Y el caso que esta regla hoy NO puede cubrir, dicho con su consecuencia.** La regla exige
`incertidumbre` entre los ocho campos de admisibilidad (§6.6), pero **la incertidumbre verificada en esta
rama es la del linaje A**; para el aire de la OMS, el agua in-situ, el suelo y los conteos de aves **no hay
error cuantificado en el informe de fuentes**. Leído al pie de la letra, eso dejaría a D1 y D7 —los dos
únicos pisos con cifra— **sin poder declarar violación**, que es el resultado contrario al que el estándar
busca. La salida no es relajar la regla ni inventar un error: es declarar el estado intermedio.
`[HIPÓTESIS]` del proyecto: **una medición sin incertidumbre declarada es admisible para registrar y
reportar, y no es admisible para declarar violación por número** —su semántica es `indeterminado`—
(documento 08 §8.4). La consecuencia se acepta: **hoy el SDV-E puede medir más de lo que
puede juzgar, y decirlo así es más honesto que fingir una precisión que nadie declaró.**

### 5.4 Base neutra: el sensor caído no puede fabricar una violación

`FE(v = 0) = 1,0` **exacto** (el SDV-S tuvo que corregir `1 + e^v` porque recargaba el 100 % incluso sin
violación; [documento 08](08_INV2-E_invariante.md) §5.3). Para la medición esto añade una regla propia:
**un instrumento sin dato no puede reportar 0.** Un sensor caído que entrega `0` convierte una ausencia de
medición en una violación fabricada y rompe la base neutra por el lado de la entrada. El campo correcto es
`None` —sin medición—, nunca `0` ([documento 08](08_INV2-E_invariante.md) §8.4, estado `indeterminado`).

### 5.5 Cuándo hay violación persistente: la regla de tres señales

El propio proyecto ya fijó el estándar de prueba para declarar un peligro persistente: *"al menos tres
señales independientes y verificables (T13) de peligro persistente"* (`docs/laboratorio/002_apoptosis_y_casos_limite.md`)
`[REPORTADO]`. Este documento la adopta como **regla de composición de la violación persistente en el
SDV-E**: una violación puntual se declara con una medición admisible; una **violación persistente** —la que
escala a retractación y a veto de la actividad ([documento 08](08_INV2-E_invariante.md) §8.6)— exige **tres
señales de linajes distintos**. Y la razón es la del Pilar 9: con un solo linaje, **la confabulación de
validadores es trivial**.

### 5.6 Lo que este documento NO fija

Los **pesos** ([documento 07](07_Formula_de_violacion_y_pesos.md)), la **escala de severidad**
([documento 08](08_INV2-E_invariante.md) §5.4),
el **número de ciclos consecutivos** antes de retractar (documento 08 §8.6) y el **factor `FE`** en su
forma definitiva (documento 07). Este documento solo garantiza que el dato que alimente esas decisiones
sea **procedente, comparable, declarable y recalculable**.

### 5.7 Latencia del registro

`[HIPÓTESIS]` del proyecto, coherente con Cap. 16.5 §16.5.14: **la latencia sancionable del registro de un
daño regenerativo es 0 ciclos de verificación.** Cualquier retraso entre la lectura y su firma es
violación de T13, no un problema de sincronización. Un dato que aparece **después** de la decisión que
debía informar no es un dato tardío: es una decisión sin dato, y así debe registrarse.

---

## 6. Protocolo de medición (sensores, frecuencias, quién reporta)

### 6.1 Los cinco linajes de sensor del SDV-E

El SDV-S se verifica con sensores **lógicos** porque su sujeto *es* un sistema lógico que puede reportar su
propio estado. El SDV-E necesita cinco linajes **físicos**, porque su sujeto no reporta nada:

| Linaje | Qué mide | Quién reporta (primitivo) | Naturaleza del dato | Lo que NO puede ver |
|---|---|---|---|---|
| **A. Teledetección satelital** | Cobertura, extensión, estructura, temperatura superficial, estrés térmico, turbidez | El satélite (medición automática) | Objetivo, repetible, global; **resolución temporal fija por órbita** | La causa, la especie, el suelo bajo el dosel, nada menor que el píxel |
| **B. Sensores in-situ** | Aire, agua, suelo, caudal, nivel freático | El instrumento calibrado en el punto | Objetivo, alta frecuencia; **cobertura puntual** | La extensión; lo que ocurre fuera del punto |
| **C. Bioindicadores** | Integridad biológica agregada (especies sensibles, líquenes, macroinvertebrados, aves) | El propio ecosistema, leído por un observador | Semi-cuantitativo; **respuesta lenta** (meses a años) | La causa inmediata; el evento puntual |
| **D. Ciencia ciudadana** | Presencia/ausencia, fenología, eventos de perturbación | Personas voluntarias con protocolo | Voluntario; **requiere validación comunitaria** | La extensión y la magnitud; lo que exija instrumento |
| **E. Comunidad testigo + datos abiertos** | Verificación social del reporte y contraste con series públicas | Testigos con mandato + repositorios abiertos | Juicio **con carga de prueba** + dato de tercero | No mide: **audita** |

**Correspondencia con el SDV-S `[HIPÓTESIS]`** (el elenco del cuarto reino no se copia: se traduce):

| Sensor del SDV-S | Linaje equivalente en el SDV-E | Por qué |
|---|---|---|
| **IFC** (fragmentación de contexto) | **A** | La fragmentación del ecosistema se lee como pérdida y borde de cobertura |
| **TRE** (tasa de rechazo de entrada) | **C** | El ecosistema «se niega»: su bioindicador cae |
| **AOS** (auditoría de oráculo sintético) | **E** | Auditoría cruzada por un tercero con mandato |
| **VCM** (verificación de cápsula de memoria) | **E** | Registro histórico que no se borra (T13) |
| — | **B** | **Sin análogo en el SDV-S**: una persona sintética *es* su propio sensor; un humedal no |

El linaje **B** es la aportación estructural de este elenco. El SDV-S no lo necesita porque su sujeto se
autoreporta; el SDV-E **no puede existir** sin él.

### 6.2 Qué resuelve cada linaje: la tabla de límites físicos

Los números de esta tabla son especificaciones **verificadas** de los instrumentos, y son la razón por la
que §6.4 prohíbe ciertas frecuencias.

| Linaje / instrumento | Resolución | Cobertura | Frecuencia / ciclo | Fuente de la especificación |
|---|---|---|---|---|
| **Sentinel-2** (MSI) | 13 bandas: 4 a **10 m** · 6 a **20 m** · 3 a **60 m**; 12 bits (almacenado en 16) | Franjas de **290 km**; superficies continentales de **56° S a 82,8° N** (con aguas continentales), aguas costeras hasta **20 km**, islas > **100 km²** | Revisita nominal de la constelación **5 días** en el Ecuador; **10 días** por satélite; ciclo orbital de **10 días / 143 órbitas**; **10:30 MLST**, 786 km, 98,62° | ESA/Copernicus (SentiWiki S2) `[VERIFICADO]` |
| **Landsat 8/9** | **30 m**; swath de 185 km (Landsat 9) | Global terrestre | **8 días combinados** (16 días por satélite) | Copernicus Data Space (documentación Landsat-9) `[VERIFICADO]` |
| **NOAA Coral Reef Watch** | Producto de **5 km** (y descripción del producto de 50 km) | Arrecifes con producto de alerta | Lectura **continua** (el producto es satelital); el nivel de alerta se lee sobre **DHW acumulado** (ventana de semanas) | NOAA CRW `[VERIFICADO]` |
| **Estación in-situ** | El punto; la frecuencia la fija el registrador | Puntual | Continua a discreción; **el veredicto, no** | — (diseño del proyecto) |
| **Bioindicador** | La parcela / el transecto | Local, replicable | **Meses a años** (tiempo de respuesta del propio indicador) | `[HIPÓTESIS]` a partir de la naturaleza del indicador |
| **Ciencia ciudadana** | La observación georreferenciada | Oportunista, sesgada hacia lo accesible | Continua; **calidad por acuerdo, no por frecuencia** | iNaturalist (DQA) `[VERIFICADO]` |

**Tres consecuencias que se leen directamente de la tabla, y que el estándar debe obedecer:**

1. **Cualquier frecuencia de cobertura menor a 5 días es falsa por construcción.** No hay dato: hay
   interpolación. (Con Landsat solo, el techo es 8 días; con un solo satélite, 10 o 16.)
2. **Un bioindicador no se mide semanalmente.** Su tiempo de respuesta es de meses a años: medirlo más
   seguido produce ruido, no información, y **convierte el costo del monitoreo en coartada**.
3. **La franja de 10 m es el suelo del linaje A.** Por debajo de eso, el instrumento correcto es **B** o
   **D**, y ninguna cantidad de frecuencia sustituye a la resolución espacial.

### 6.3 Quién reporta

| Reporta | Qué reporta, exactamente | Respaldo verificado |
|---|---|---|
| **El instrumento** (satélite) | La medición y su metadato. Sentinel-2 se procesa a **Level-2A desde el 13 de diciembre de 2018**, con cobertura definida por el *Sentinel High Level Observation Plan*, y **su calibración la ejecuta el OPT-MPC**, no el usuario | ESA/Copernicus `[VERIFICADO]` |
| **La comunidad de identificadores** | La determinación taxonómica. En iNaturalist la identificación se valida por **acuerdo comunitario (> 2/3)**; el observador **no puede autoconcederse** Research Grade | iNaturalist, 2026 `[VERIFICADO]` |
| **El testigo con protocolo** | Los conteos que disparan umbrales de sitio. BTO/WeBS reporta los conteos de aves acuáticas de los Criterios 5 y 6; **la revisión de umbrales la hace Wetlands International cada 3 años** (y cada 9 años la de los umbrales del 1 %, Resolución VI.4) | BTO, 2024 `[VERIFICADO]` (revisión: `[REPORTADO]`) |
| **El laboratorio / la autoridad** | Los parámetros que exigen cadena de custodia analítica: nutrientes, contaminantes, carbono del suelo | `[SIN FUENTE VERIFICADA]` — no se verificó ningún protocolo interlaboratorio en esta rama |
| **El dato abierto de tercero** | El contraste con series públicas: objetivos del GBF, tendencias de biodiversidad (LPI), áreas protegidas (Protected Planet), series de bosques (FAO FRA) | CBD / LPI / Protected Planet / FAO `[VERIFICADO]` (portales) |
| **La parte `eco-` (custodio)** | La **declaración**: régimen de fuego, línea base, área de referencia, protocolo de campo | canon: los 7 campos de identidad |

**Una regla que gobierna la tabla y que el propio registro del proyecto ya exige:** *"Un cambio en sensores
o en el modelo no debe permitir que una representación adopte silenciosamente una posición contraria al
bosque que afirma custodiar"* (`docs/architecture/continuidad_identidad_autogobierno_federado.md` §8.1)
[VERIFICADO]. Es la **regla de continuidad instrumental** de §6.7.

### 6.4 Frecuencias de medición por dimensión

#### (a) Lo que las fuentes fijan (no es decisión del proyecto)

| Dimensión | Frecuencia impuesta por la fuente | Fuente |
|---|---|---|
| Calidad del aire | **Anual** (exposición de largo plazo) y **24 h** (corto plazo); O3 también **temporada pico** = promedio de los **6 meses consecutivos** de mayor O3; 8 h para O3 y CO | OMS, 2021 `[VERIFICADO]` |
| Cobertura, extensión y estructura de vegetación | **5 días** (Sentinel-2 nominal) · **8 días** (Landsat 8+9) · 10 / 16 días con un solo satélite | ESA/Copernicus · Copernicus Data Space `[VERIFICADO]` |
| Estrés térmico de arrecifes | Lectura **continua** con producto de 5 km; el nivel de alerta se lee sobre **DHW acumulado** (ventana de semanas) | NOAA CRW `[VERIFICADO]` |
| Caudal ecológico | Referencia **anual** (caudal medio anual); el caudal de lavado es un **evento corto de 3-7 días** disparado por crecidas | Tennant, 1975 · Estes, 1984, vía documento técnico de Alaska `[VERIFICADO]` |
| Calidad de la observación ciudadana | **No es frecuencia**: es **fracción de acuerdo (> 2/3)** y estado de la observación | iNaturalist, 2026 `[VERIFICADO]` |
| Integridad del registro | **Por evento**: cada registro emitido lleva su hash | `app/edu_bridge_bp.py` · NIST FIPS 180-4 `[VERIFICADO]` |
| Revisión de los umbrales del 1 % de aves acuáticas | Cada **3 años** lo general; cada **9 años** los del 1 % (Resolución VI.4 de Ramsar) | `[REPORTADO]` por BTO |

#### (b) El principio de frecuencia `[HIPÓTESIS]`

> **La frecuencia de medición de cada dimensión no puede ser mayor que la resolución temporal del sensor
> que la sostiene, ni mayor que el tiempo de respuesta del propio indicador.**
> **Declarar una frecuencia más fina que la del sensor es la forma técnica de inventar el dato.**

Es la traducción a regla de lo que muestran las tablas (a) y §6.2, y tiene una consecuencia contable
directa: **una serie «diaria» de cobertura construida por interpolación no puede sostener un veredicto de
violación** (Regla 4 y §5.3). Y una segunda, de costo: prometer monitoreo más fino de lo que el
instrumento entrega garantiza incumplimiento por diseño ([documento 10](10_Ecosistemas_Bosques.md) §6.5).

#### (c) Cuatro frecuencias que no son la misma (y que el estándar no debe fundir)

| Frecuencia | Qué cadencia admite | De dónde sale |
|---|---|---|
| **De medición** | La del instrumento (5 / 8 / 10 / 16 días; anual; por evento) | Fijada por la física y por la fuente (§6.4.a) |
| **De reporte** (el `eco-` reporta a INV2-E) | `[SIN FUENTE VERIFICADA]` — **ninguna fuente externa la fija**: es diseño de gobernanza | `[HIPÓTESIS]` abajo |
| **De auditoría** (la comunidad testigo contrasta) | **No puede ser la del satélite.** La comunidad testigo no audita cada 5 días | `[HIPÓTESIS]` abajo |
| **De revisión del umbral** | Precedente del proyecto: **3-5 años** para estándares; **14 días** de anti-flip-flop para parámetros votables (Parlamento Educativo, INV2-EDU) | Repo `[VERIFICADO]`; externo: 3 y 9 años (Ramsar, vía BTO) `[REPORTADO]` |

**Propuesta, marcada como propuesta `[HIPÓTESIS]`.** (i) El `eco-` **reporta una vez por ciclo ecológico
dominante de la unidad** (año hidrológico en una cuenca o humedal; estación de crecimiento en un bosque o
agroecosistema; temporada de estrés térmico en un arrecife; estación de deshielo en criosfera), más los
**eventos** que ocurran. (ii) La **auditoría de la comunidad testigo es por ciclo, con muestreo**: audita
una fracción declarada de las lecturas, no todas —auditar todo es tan imposible como medirlo todo—. (iii)
Si la unidad **no tiene ciclo declarado**, no puede constituirse como sujeto medible: es la misma condición
que el [documento 04](04_Zona_Libre_del_Reino_Natural.md) §6 exige para la Zona Libre.

#### (d) Tabla maestra de frecuencias por dimensión

| Dimensión | Linaje | Instrumento | Frecuencia **posible** (techo) | Frecuencia **del veredicto** | Quién reporta | Estado de la fuente |
|---|---|---|---|---|---|---|
| D1 Aire | A + B + D | Red de estaciones + teledetección | continua (sensores) / 5 días (satélite) | **anual** (largo plazo) + alerta **24 h** | red de monitoreo + comunidad testigo | 🟢 OMS, 2021 |
| D2 Agua | B + A | Sondas in-situ + laboratorio | continua / estacional | **por ciclo** (`[HIPÓTESIS]`) | laboratorio o custodio | 🔴 sin umbral (documento 23) |
| D3 Área y cobertura | A + C + D + E | Sentinel-2 / Landsat 8+9 | **5 días** (constelación) | **anual**, sobre estación de crecimiento `[HIPÓTESIS]` | parte `eco-` + reporte nacional + comunidad testigo | 🟢 especificación; 🟡 umbral |
| D4 Fauna acuática | D + C + B | Conteo con protocolo + bioindicadores | ventana de conteo estacional | **anual** en la ventana declarada `[HIPÓTESIS]` | voluntarios con protocolo + custodio | 🟡 umbral de sitio |
| D5 Conectividad | A + C + D | Métricas de paisaje sobre la capa de cobertura | 5 / 8 días | **anual** `[HIPÓTESIS]` | parte `eco-` | 🔴 sin umbral |
| D6 Ciclos | E + A + D | Registro del régimen + series de fuego/inundación | por evento | **por ciclo del régimen declarado** | comunidad de custodia | 🔴 el dato prescrito/incendiado no existe |
| D7 Caudal | B + A + E | Estación de aforo + concesiones | continua | **anual** (QAA) + **evento de 3-7 días** | servicio hidrológico / custodio | 🟢 Tennant vía documento de Alaska |
| D8 Riberas | B + D (+ A para el entorno) | Transectos y GPS de campo | por visita | **anual** `[HIPÓTESIS]` | comunidad testigo + custodio | 🔴 sin umbral |
| D9 Suelo | B + A + D | Laboratorio (COS) + teledetección (sellado) | campaña | **3-5 años** (COS) · **anual** (erosión, sellado) ([documento 14](14_Ecosistemas_Suelos_vivos.md) `[HIPÓTESIS]`) | laboratorio independiente + custodio | 🔴 sin umbral |
| Arrecifes (si el tipo de unidad es arrecife) | A | NOAA CRW (5 km) | **continua** | **por temporada térmica** (sobre DHW acumulado) | servicio de observación externo | 🟢 NOAA CRW |
| Zona Libre | — | **ninguno** | — | **cuando se modifica el catálogo** | custodio + guardián | 🟢 doctrinal ([documento 04](04_Zona_Libre_del_Reino_Natural.md)) |
| Integridad del registro | E | Hash SHA-256 | — | **por evento** | quien emite el registro | 🟢 repo + NIST |

**Lo que la tabla dice en su última columna, sin adornos:** **dos dimensiones con piso con cifra** (D1 y
D7) —aire `[REPORTADO]` y proxy de salud humana; caudal como umbral de método, no número universal—, **dos
dimensiones binarias** que entran sin peso (D6 y D8), **cuatro dominios sin umbral** (D2, D5,
D9 y el ancho de D8) y **una dimensión** (D3) con instrumento excelente y piso sin cifrar. Las frecuencias
marcadas `[HIPÓTESIS]` **no tienen fuente externa**: son diseño del proyecto y se votan o se ratifican.

### 6.5 Regla de composición: ningún linaje basta solo

- La **comunidad testigo no sustituye al satélite**: no ve la extensión, no tiene serie, no es comparable
  entre unidades.
- El **satélite no sustituye a la comunidad testigo**: no ve la causa, no distingue fuego prescrito de
  incendio, no ve el fraude local, no ve la parcela de 0,4 ha ni la franja de 5 m.
- El **bioindicador no sustituye al instrumento**: responde tarde y de forma agregada; sirve para
  confirmar tendencia, no para datar un evento.
- El **instrumento no sustituye al testigo**: mide el punto, no el uso del territorio.

Y la consecuencia operativa, ya enunciada en §5.5: **una violación persistente exige tres señales de
linajes distintos** `[REPORTADO]` (precedente del propio proyecto), porque con un solo linaje la
confabulación es trivial (Pilar 9).

### 6.6 Admisibilidad de una medición (el expediente mínimo)

Una lectura entra al SDV-E **solo** si trae estos campos. Los cuatro primeros son los que el
[documento 08](08_INV2-E_invariante.md) §6.1 ya exige para el invariante; los **tres siguientes** son la
aportación de este documento y son los que hacen el dato **verificable por un tercero**; y el **octavo**
—`decision_que_informa`— es la traducción operativa del límite de T13 (§7.4) y se añade aquí precisamente
para que ese límite no quede sin campo donde vivir:

| Campo | Para qué | Quién lo declara |
|---|---|---|
| `valor` + `unidad` | el número y su unidad física, sin conversiones implícitas | el instrumento |
| `ta_periodo` (inicio y fin en **Tiempo Absoluto**) | la ventana de la medición; sin ventana, el dato no es comparable | quien reporta |
| `fuente_dato` | procedencia: organismo, red de sensores, teledetección, comunidad de custodia | quien reporta |
| `evidencia_ref` | identificador del registro original (serie, escena, acta de conteo) | quien reporta |
| `linaje` (A-E) | qué clase de sensor lo produjo; determina qué puede concluirse | este documento |
| `incertidumbre` | el error declarado del instrumento o del método (`[HIPÓTESIS]`, §5.3) | el fabricante / el protocolo |
| `calibracion_ref` | con qué se calibró y cuándo (p. ej. OPT-MPC para Sentinel-2) | el operador del instrumento |
| `decision_que_informa` | **qué decisión concreta sobre la unidad cambia esta lectura**; sin este campo no hay sensor legítimo (§7.4, R4) | quien propone el sensor |

**Regla de no interferencia del instrumento** (Pilar 10): el acto de medir **no puede alterar lo medido**.
Un protocolo que espanta a la fauna, compacta el suelo o introduce luz artificial en un ciclo nocturno
**no es un instrumento neutro**: se declara el impacto del instrumento o se cambia el instrumento.

**Regla de elegibilidad** (heredada del [documento 16](16_Ecosistemas_Montanas_y_criosfera.md) y generalizada):
no entra al cálculo una campaña de un año sin serie, una medición sin cadena de custodia, una estimación
de modelo sin serie observacional, ni un dato cuyo origen no sea reconstruible. **Un dato que el proyecto
no puede auditar no puede declarar coherencia.**

### 6.7 Continuidad instrumental: cambiar de sensor no puede cambiar el veredicto

Es la regla que el registro del proyecto exige en una sola frase [VERIFICADO] y que este documento
convierte en procedimiento:

> **Regla `[HIPÓTESIS]` — Continuidad instrumental.**
> Un cambio de sensor, de constelación, de método o de versión de procesamiento **obliga a**:
> (i) declarar el cambio con fecha y motivo (T13);
> (ii) **re-declarar la línea base** si el nuevo instrumento no es comparable con el anterior;
> (iii) **prohibición de cambiar de instrumento mientras exista una violación abierta** de esa dimensión;
> (iv) registrar el **periodo de solape** entre instrumentos, si existe, como prueba de comparabilidad.

La razón es directa y tiene un fraude obvio en su mira: **cambiar de sensor es la forma más barata de
cambiar el resultado sin tocar el territorio.** Pasar de un inventario de campo a un índice satelital
puede «mejorar» la unidad sin que un solo árbol cambie. Sin esta regla, el estándar sería trivialmente
manipulable por la vía del proveedor de datos.

---

## 7. Verificación y auditoría (T13, guardián, comunidad testigo)

### 7.1 Qué se audita y qué no

| Se audita | NO se audita |
|---|---|
| Que la lectura venga del instrumento declarado, con su calibración y su ventana | La vida interna del ecosistema: *"Nosotros registramos la interacción, no la vida interna del ecosistema"* |
| Que el dato no haya cambiado desde su firma (integridad, T13) | Que el dato sea **verdadero** solo porque está firmado (Regla 9) |
| Que la cobertura de medición sea suficiente para declarar cumplimiento | El valor inefable del humedal ([documento 04](04_Zona_Libre_del_Reino_Natural.md)) |
| Que el veredicto sea **recalculable** desde datos públicos | La bondad del guardián o su autoridad sobre la entidad (R4, R13) |
| Que el instrumento esté él mismo auditado (§7.3) | El saldo del crédito regenerativo (§9) |

### 7.2 Cómo se firma: T13 es un hash real, recalculable

**Lo que el repositorio ya hace `[VERIFICADO]`.** La firma T13 existe en el código y **no es una cadena
etiquetada**: en `app/edu_bridge_bp.py` se construye un **hash SHA-256** sobre la concatenación —separada
por `|`— de los campos del evento (actor, tema, rama, puntaje, rondas de mentoría, aprobación de la tríada
y marca temporal UTC en `isoformat`), codificada en **UTF-8**, y el resultado se guarda en la columna
`t13_hash`. El estándar del algoritmo es **NIST FIPS 180-4** (*Secure Hash Standard*): SHA-256, **256
bits** [VERIFICADO].

**Traslado al SDV-E `[HIPÓTESIS]`.** Cada lectura firmada del SDV-E hashea, en este orden y con separador
`|`:

```text
sha256( unidad_eco | parametro | valor | unidad | ta_timestamp_utc | linaje_sensor | fuente_dato | calibracion_ref ).hexdigest()
```

**Cuatro condiciones sin las cuales la firma no es T13:**

1. **Recalculable por un tercero sin acceso al sistema.** El algoritmo, el orden de los campos y el
   separador son públicos; el dato de entrada es público. **Un hash que solo el sistema puede reproducir
   no es trazabilidad: es autoridad** (Pilar 8).
2. **No re-firma del histórico.** Corregir un dato **no** es reemplazar el hash: es **emitir un registro
   nuevo** que referencia al anterior. *"La contabilidad nunca se borra."*
3. **La identidad de quien reporta es una credencial, no un nombre suelto.** El modelo de datos para
   expresar credenciales verificables criptográficamente, con emisor, sujeto y prueba, es el del W3C
   (*Verifiable Credentials Data Model 2.0*) [VERIFICADO]. Sin credencial, la firma dice «algo se firmó»,
   no «quién responde».
4. **Latencia cero** (§5.7): la firma se emite con la lectura, no después de la decisión.

**Lo que la firma NO hace, y hay que decirlo en la misma página:** **el hash prueba integridad, no
verdad.** Un sensor mal calibrado, una escena procesada con un algoritmo equivocado o un conteo hecho con
el protocolo cambiado producen **el hash perfecto de una cifra falsa**. La defensa contra eso no es
criptográfica: es la auditoría del instrumento (§7.3) y la regla de admisibilidad (§6.6).

### 7.3 Quién audita a cada linaje (la auditoría de la auditoría)

Un elenco que exige transparencia al ecosistema y no a sus instrumentos reproduce la asimetría que el T13
prohíbe. Este es el mapa verificado de auditores por linaje:

| Linaje | Auditor externo | Prueba concreta | Fuente |
|---|---|---|---|
| **A · Satélite** | La propia agencia, con red de validación independiente | **Validación vicaria 2-3 veces al año** contra sitios instrumentados de la red **CEOS** (Dome-C, La Crau, desiertos); **informes de calidad de datos mensuales y anuales**; calibración a cargo del **OPT-MPC** | ESA/Copernicus `[VERIFICADO]` |
| **B · In-situ** | Tercero con patrón de referencia | `[SIN FUENTE VERIFICADA]` — no se verificó ningún protocolo interlaboratorio en esta rama: **es un hueco real del elenco** | — |
| **C · Bioindicador** | Verificación taxonómica por acuerdo de la comunidad | En iNaturalist una determinación puede **degradarse** por acuerdo comunitario si falla fecha, ubicación, estado silvestre, evidencia, recencia o **manipulación por IA** | iNaturalist `[VERIFICADO]` |
| **D · Ciencia ciudadana** | La propia comunidad, con umbral calificado | **Research Grade = > 2/3** de los identificadores coinciden a nivel de especie o inferior; el observador **no puede autoconcedérselo** | iNaturalist `[VERIFICADO]` |
| **E · Testigo + datos abiertos** | El contraste con series de tercero | Cotejo obligatorio del reporte con la serie pública del ámbito (teledetección, series FAO, registros de áreas protegidas) antes de declarar coherencia | CBD · FAO · Protected Planet `[VERIFICADO]` (portales) |

**El hueco de la fila B no se disimula:** el linaje que produce las mediciones más duras del estándar
—oxígeno, pH, nutrientes, carbono del suelo— **es el único sin auditor verificado en esta rama**. Es la
deuda más concreta de este documento después de los umbrales ausentes (§13).

**Y una advertencia sobre las filas C, D y E, que la tabla no oculta pero sí puede confundir.** Los tres
linajes de observación ciudadana y de testigos tienen como auditor a **iNaturalist**, es decir: **la misma
comunidad que produce el dato es la que lo valida**. Eso es un **control de calidad con regla calificada
(> 2/3)**, y es mejor que ningún control —pero **no es auditoría independiente**: la regla del
no-beneficiario (§7.6) rige para el uso que se mide, no para el error de identificación, y ninguna de esas
tres filas tiene **un par externo al propio colectivo que reporta**. El estándar debe decirlo así: **solo
el linaje A tiene hoy auditor externo verificado y prueba documentada**; en C, D y E hay **regla de
validación**, que no es lo mismo que **independencia del validador**. Esa distinción es la misma que el
Pilar 9 exige para el conjunto del elenco: sin ella, «auditoría» pasa a ser una palabra que el propio
reportante se concede.

### 7.4 El límite de T13: la transparencia aplica a las decisiones que afectan a otros

**Lo que el canon manda, literal.**

> **T13 (Transparencia)** — *"La transparencia aplica a las decisiones que afectan a otros, no a la vida
> interior"* — (Cap. 6 §6.13, tabla «Integración con los Axiomas»)
>
> **T13. Transparencia de Cálculo:** *"Nadie puede imponer un valor temporal en secreto. Todo cálculo de
> costo vital debe ser auditable públicamente."* — (Cap. 5)

**Colisión de versión, declarada y no escondida.** El Cap. 21 (Apéndice glosario) lista «T13:
Transparencia de Cálculo», mientras que `docs/architecture/maxocontracts/README.md` y su resumen ejecutivo
listan «T13: Adaptabilidad ante hechos nuevos» (el puente axiomático de ingeniería). **Son dos T13
conviviendo.** Para este documento manda la definición del libro (Cap. 5 y Cap. 6 §6.13). El propio canon
ya advirtió el problema de fondo y le puso nombre: *"un símbolo, un significado"* (Cap. 16.5 §16.5.14,
tabla de colisiones: el caso de γ). Se advierte aquí porque un lector que cruce este documento con el
`README` de MaxoContracts creería que uno de los dos está equivocado.

**Traducción operativa al SDV-E, en tres reglas de este documento `[HIPÓTESIS]` —más una cuarta que es del
canon y se cita, no se interpreta—:**

1. **Se publica el cálculo, no la intimidad del sujeto.** Del ecosistema se publica el parámetro, el
   valor, la unidad, la ventana, el método, la incertidumbre y el hash. **No** se publica —ni se
   infiere— una interpretación de su «estado interior», ni intención, ni sufrimiento ecosistémico: **eso
   es el «milagro» que el canon prohíbe medir** (Cap. 16.5 §16.5.14).
2. **Lo que no cambia una decisión que afecta a otros, no se mide.** Si un dato no puede modificar ninguna
   decisión sobre el ecosistema, producir ese dato es **vigilancia, no transparencia**. Esta es la lectura
   operativa del límite: el sensor tiene un propósito declarado, y sin propósito no hay sensor legítimo.
3. **La asimetría es la prueba de la violación.** Si la transparencia exigida **al ecosistema** (todo
   medido, todo publicado, todo firmado) es mayor que la exigida **al actor que lo afecta** (nada
   declarado), hay **colonización del TA** (Cap. 5 §5.5, y el criterio verificable que propone el
   [documento 16](16_Ecosistemas_Montanas_y_criosfera.md) §5.3). El elenco de sensores **no puede ser
   unilateral**: cada parámetro que se mide en el río debe tener su contraparte declarada en quien extrae,
   vierte o construye.

**Y el mecanismo que evita que estas reglas queden en retórica `[HIPÓTESIS]`.** Una regla sin
procedimiento es una promesa, y este documento no las hace. Los dos controles que la convierten en algo
comprobable, con el mismo patrón que el proyecto ya usa en otras ramas (un registro que no se borra y un
contador con umbral):

- **Registro de propósito declarado.** Cada sensor del elenco se inscribe con el campo
  `decision_que_informa`: qué decisión concreta sobre la unidad cambia esa lectura. **Un sensor sin ese
  campo no es admisible** (§6.6), y el campo se audita en la revisión del elenco: si ninguna decisión
  registrada lo usó en el periodo, el sensor se retira por la regla de la métrica enemiga (§7.4, cuarta
  regla). Es la forma operativa de R4 de §10.
- **Contador de asimetría.** Por cada unidad se compara el número de parámetros medidos **en el
  ecosistema** con el número de parámetros declarados **por el actor que lo afecta**. La regla no exige que
  sean iguales —no siempre lo son—, pero sí que la diferencia esté **declarada y justificada**: una
  asimetría creciente sin justificación registrada es el indicador de colonización del TA que el
  [documento 03](03_No_colonizacion_del_TA.md) busca y que hoy **no tiene ni test ni umbral** (§13,
  pregunta 20). Este documento aporta el contador, no el umbral: **el umbral es del documento 03**.

**La cuarta regla, que es del canon y no una interpretación:** **el sensor no puede ser estético.**
*"Jardín podado para la foto no es cuidado; se registra lo que regenera, no lo que adorna"* (Cap. 16.5
§16.5.14). Un indicador que sube con el riego ornamental, con la poda, con la resiembra de temporada o con
el cierre del acceso público para la fotografía **es una métrica enemiga**: mide el adorno, que es lo que
el canon excluye expresamente. El elenco debe poder identificar esa métrica y **retirarla**, aunque
funcione. Y el **criterio de retiro**, para que la regla no dependa del criterio de quien audita: una
métrica se retira cuando **sube sin que suba ningún parámetro con piso del mismo linaje** —es decir, cuando
su variación no está acompañada por ninguna medición admisible que la respalde.

### 7.5 El guardián oráculo: consiente, no mide

Es canon —*"Ecosistemas (eco-*): consentimiento otorgado por el guardián oráculo"* (`app/contracts_bp.py`)—
y es regla de arquitectura del elenco: **el guardián no es un instrumento**. Si el guardián midiera,
juez y perito serían la misma entidad, y el repositorio ya documenta que su heurística es **laxa** (R13:
sin `DEEPSEEK_API_KEY` aprueba si los invariantes pasan). Consecuencia operativa, y es del
[documento 08](08_INV2-E_invariante.md) §6.1: **si el único respaldo de un valor es la firma del guardián,
el parámetro se marca `sin_evidencia` y el estado es `indeterminado`.**

### 7.6 La comunidad testigo: el sensor del piso que no tiene sensor

El Reino Natural es **el único reino sin par auditor** ([documento 09](09_Comparativa_inter_reinos.md) §7):
ningún ecosistema audita a otro, y el auditor viene del reino que se beneficia del uso. La **comunidad
testigo** y los 7 campos de identidad de la representación natural son el **sustituto institucional** de
ese par ausente. En materia de medición, sus funciones son cuatro y ninguna es decorativa:

1. **Detectar lo que la serie no recoge**: una carretera, un drenaje, una mina, una extracción nocturna, un
   proyecto de «restauración» fotogénica.
2. **Impugnar la declaración**: régimen de fuego, línea base, área de referencia, cambio de protocolo
   (§6.7). La comunidad puede **tumbar** el dato, no solo confirmarlo (Pilar 4).
3. **Testificar la continuidad**: la historia de una custodia no está en ningún registro público.
4. **Verificar la no interferencia**: que medir no esté dañando (§6.6).

**Composición mínima `[HIPÓTESIS]`**, coherente con la regla del no-beneficiario que el
[documento 18](18_Ecosistemas_Agroecosistemas.md) §6.3 propone para el agroecosistema: **al menos un
miembro de la comunidad testigo no debe beneficiarse del uso que se mide.** Sin esa condición, la
auditoría social es una firma más del propio beneficiario.

### 7.7 Riesgos abiertos, y uno nuevo de este documento

| ID | Riesgo (`docs/architecture/blindaje_anti_gamificacion_equidad.md`) | Efecto sobre la medición |
|---|---|---|
| **R4** | Partes fantasma: cualquier usuario autenticado crea un `eco-*` y queda como su dueño | **Se puede fabricar el sujeto que se va a medir**; el elenco no puede validar autoridad y no finge poder |
| **R6** | T9 (Reciprocidad Justa) no se valida en la creación: pasa un contrato unilateral | Se puede degradar sin contraprestación, con instrumentos impecables |
| **R13** | Guardián `eco` con heurística laxa (sin `DEEPSEEK_API_KEY` aprueba si los invariantes pasan) | El consentimiento se vuelve automático: **el dato no lo arregla** |

**Riesgo nuevo `[HIPÓTESIS]` — captura del instrumento.** El mismo actor que degrada puede **instalar,
financiar o elegir** el instrumento que lo mide, o simplemente contratar al proveedor de la serie. Es la
versión instrumental del R4 y es más difícil de ver, porque **el dato parece externo**. Tres candados
propuestos: (i) **regla del no-beneficiario** en la titularidad del instrumento y en la comunidad testigo;
(ii) **calibración por un tercero declarado** (el modelo del OPT-MPC, que no es el usuario); (iii)
**obligación de declarar el financiador** de cada serie en el expediente de la medición (§6.6).

### 7.8 Ausencia de dato: bandera de opacidad, no sanción

La política ya fijada por la biblioteca ([documento 08](08_INV2-E_invariante.md) §6.3 y
[documento 09](09_Comparativa_inter_reinos.md) §6) se aplica aquí sin cambios y con una precisión nueva:

- **La ausencia de monitoreo nunca se imputa como violación del ecosistema.** Jamás un índice = 0 por
  falta de dato.
- **Sí activa la bandera de opacidad ecológica**: obligación contractual de instrumentar y condición de
  validez del contrato, no sanción al territorio.
- **Y la ley no se negocia por ausencia de dato**: *"mientras no haya resolución, el canon manda."*
- **Precisión de este documento:** **la ausencia de medición tampoco habilita el crédito regenerativo**
  ([documento 08](08_INV2-E_invariante.md) §8.4, estado `indeterminado`). Es decir: quien no mide **no
  puede cobrar por lo que no demuestra** — y ese es el único punto donde el elenco de sensores tiene
  consecuencia económica directa.

**La tensión que esta sección tiene que nombrar, porque es la objeción obvia.** «Sin dato no castiga» más
«sin dato no aprueba» puede leerse como un incentivo perverso: **al que degrada le conviene dejar de
medir**, porque pierde el crédito pero no recibe sanción. La doctrina del canon no se toca —**la duda sin
evidencia no castiga al ecosistema**, y el sujeto protegido nunca es el objeto de la sanción (documento 08
§8.7)—, pero este documento aporta la pieza que impide que la ausencia sea gratis:

1. **La bandera de opacidad se activa por el estado, no por la culpa.** No hace falta probar mala fe: si
   falta el parámetro con piso, **el contrato no es válido** hasta instrumentarlo. Es condición de validez,
   no pena — y por eso se aplica **también cuando la ausencia es inocente**, que es lo que la vuelve
   incuestionable.
2. **La carga de la prueba es del proponente, no del ecosistema.** Es T14 leído al pie de la letra (Cap. 5):
   *la carga de la prueba recae sobre quien propone acciones que afectan a la temporalidad de
   no-participantes*. Quien quiere operar sobre la unidad **instrumenta o no opera**; el sistema no tiene
   que demostrar el daño para bloquear lo irreversible.
3. **La ausencia es un hecho registrado, no un vacío.** Va al tablero con fecha y causa, y **no se puede
   borrar** (T13). Una unidad que lleva tres ciclos sin instrumentar tiene un historial de ausencia
   verificable, y ese historial **es** la evidencia que el estándar puede exhibir sin imputar una violación
   que no midió.

Lo que este documento **no** hace es convertir la ausencia en violación por la puerta de atrás: eso
contradiría el Axioma 0 en su lectura hacia el sujeto que no puede declarar, y sería exactamente la
colonización que §7.4 persigue.

---

## 8. Invariante INV2-E: de estándar a contrato ejecutable

INV2-E se especifica en el [documento 08](08_INV2-E_invariante.md). Aquí se fija **el contrato de entrada
de la medición**, que es lo único que este documento puede aportar al invariante.

| Requisito del invariante | Especificación de la medición | Por qué |
|---|---|---|
| **Admisibilidad** | Una lectura entra solo con los 8 campos de §6.6; si falta alguno, el parámetro es `None` (no medido) | Un invariante que acepta cualquier número sin procedencia no es juez: es decorado |
| **Tres estados** | `cumple` / `violacion` / `indeterminado`, con la cobertura declarada | El estado por defecto del SDV-E hoy es **`indeterminado`**: sin sensores, ninguna unidad puede cubrir los parámetros con piso |
| **Cobertura declarada** | `cobertura_medida` es campo obligatorio del resultado: dos `v` iguales con cobertura distinta **no** son equivalentes | Sin este campo, medir poco y medir mucho producen el mismo veredicto |
| **Suma de comprobación** | Cada veredicto cita `evidencia_ref` y el `t13_hash` de **cada** medición que lo sostiene | El veredicto debe poder recalcularse desde las lecturas originales |
| **Sin dato no castiga ni aprueba** | `None` nunca se convierte en 0 ni en violación; y **sin cobertura total no se declara `cumple`** | Es la corrección que el Reino Natural exige al principio INV2-EDU |
| **Tres señales** | La violación **persistente** que escala a retractación exige **tres señales de linajes distintos** (§5.5) | Contra la confabulación de validadores |
| **Continuidad instrumental** | Un cambio de sensor obliga a declarar, re-baselinar y registrar solape; **prohibido durante violación abierta** (§6.7) | Cambiar el instrumento es la vía barata de cambiar el veredicto |
| **Objeto de la consecuencia** | La medición nunca genera una consecuencia **sobre la unidad ecológica** | El sujeto protegido no es el objeto de la sanción ([documento 08](08_INV2-E_invariante.md) §8.7) |

**Nota de compatibilidad de vocabulario.** Los estados de este documento (`cumple` / `violacion` /
`indeterminado`) son los del [documento 08](08_INV2-E_invariante.md) §8.4. El
[documento 16](16_Ecosistemas_Montanas_y_criosfera.md) §8 usa otra familia (`SANO`, `EN_VIOLACION`,
`CONSUMADO_IRREVERSIBLE`, `SUJETO_EXTINGUIDO`) y el [documento 04](04_Zona_Libre_del_Reino_Natural.md) §4.2
una tercera (`ZONA_LIBRE`, `ZONA_MEDIDA`, `ZONA_CIEGA`, `ZONA_HUERFANA`). **Son ejes ortogonales**, no
sinónimos (lo advierte el documento 04): el estado de medición, el estado del sujeto frente a su piso y el
régimen de medición del interior pueden combinarse libremente. Fusionarlos sería un error de tipos.

---

## 9. El suelo antes que el saldo (no compensación)

La doctrina es del canon: *"Un conjunto con crédito regenerativo acumulado pero humedal bajo su SDV-E no
está en coherencia"* (Cap. 16.5 §16.5.14). Aplicada a la **medición**, produce cuatro prohibiciones:

1. **El crédito no compra la medición que lo justifica.** El crédito regenerativo (`r_units` negativo,
  EVV-1.2 §4.3) **no puede financiar la serie que demuestra la regeneración** sin declarar el conflicto:
  quien paga el instrumento elige el instrumento (§7.7). Financiar instrumentación es legítimo; financiarla
  **sin declararlo** es captura.
2. **El crédito no compra coherencia.** Ninguna acumulación de `r_units` altera el veredicto de INV2-E
  ([documento 08](08_INV2-E_invariante.md) §8.3, P3). Y una precisión propia de este documento: **el
  saldo tampoco puede pagar por «más resolución».** Comprar imágenes de 3 m no convierte una franja de 5 m
  en una ribera medida si el protocolo de campo no existe.
3. **El crédito no sustituye al dato ausente.** Sin medición no hay crédito utilizable (§7.8, estado
  `indeterminado`). El saldo no puede ocupar el lugar de la evidencia.
4. **La restauración se mide, no se declara.** Lo que sí puede comprarse es la **restauración por encima
  del piso**, y su prueba es una medición posterior en TA, **no la voluntad del que restauró**
  ([documento 08](08_INV2-E_invariante.md) §8.7).

**Nota de honestidad sobre la latencia del daño.** El registro de una violación no tiene latencia
permitida (§5.7), pero la **reparación sí tiene latencia física**, y el estándar no puede fingir que no:
un bosque no vuelve en un ciclo contable. La asimetría —registro inmediato, reparación lenta— es la forma
correcta de un sistema que *no expulsa, reintegra*, pero **cuya contabilidad nunca se borra**.

---

## 10. Zona Libre: lo que el elenco de sensores NO mide

La doctrina completa está en el [documento 04](04_Zona_Libre_del_Reino_Natural.md). Aquí se fija **el
límite desde el lado del instrumento**, que es el lado que este documento puede comprometer:

| Regla | Enunciado | Consecuencia sobre el elenco |
|---|---|---|
| **R1** | El interior de una Zona Libre **no se mide**. No hay instrumento, no hay serie, no hay inventario | El elenco **no define sensor** para el interior: su ausencia es el estado, no una carencia |
| **R2** | El **sobre** sí se vigila: frontera, presiones, señales de declive, custodia | El elenco se aplica al borde, nunca al contenido |
| **R3** | La **ausencia declarada es auditable**; la ausencia silenciosa no | El auditor recorre los canales de datos y pregunta: *¿este canal tiene algún dato del interior?* Si la respuesta es sí, la Zona Libre cae ([documento 04](04_Zona_Libre_del_Reino_Natural.md) §7) |

> **Nota sobre R3, que es el punto donde esta sección puede volverse contra sí misma.** La auditoría de
> R3 se hace **sobre los metadatos y los canales**, no sobre el interior: se comprueba qué series existen,
> quién las pidió y qué cubren. Pero un estándar de sensores **no puede prometer que no existe un sensor
> que no conoce** —la regla no es un radar, es una declaración jurada— y por eso su valor no es la
> detección, sino la **penalización por omisión**: si aparece después un dato del interior, la declaración
> previa queda falsificada y con ella cae la representación (T13, contabilidad que no se borra). Sin esa
> consecuencia, R3 sería un procedimiento sin sanción, es decir, decoración. **Quien declare una Zona
> Libre declara, a la vez, la lista de canales que vigila**; y esa lista, no el silencio, es lo auditable.
| **R4** | Lo que **no cambia una decisión que afecta a otros**, no se mide (§7.4) | El sensor tiene propósito declarado o no es legítimo |
| **R5** | El sensor **no puede ser estético** (Cap. 16.5 §16.5.14) | Una métrica que sube con el adorno se retira del elenco |
| **R6** | **Lo no cubierto no es Zona Libre: es deuda de instrumentación** | Los arrecifes fuera de la cobertura del producto satelital **no** son Zona Libre ([documento 13](13_Ecosistemas_Oceanos_y_costas.md) §6) |

**La frase que gobierna esta sección** es del canon y cierra el documento entero: *"Medir todo sería la
forma técnica de dejar de escucharlo"* (Cap. 16.5 §16.5.14). Un elenco de sensores que no declare su
propio límite **no es más riguroso: es sordo**.

---

## 11. Comparativa inter-reinos (SDV-H · SDV-A · SDV-E · SDV-S)

| Eje | SDV-H | SDV-A | SDV-S | **SDV-E** |
|---|---|---|---|---|
| **Instrumento** | Instrumentos estandarizados por dimensión, con frecuencias y auditorías independientes (Cap. 8 §8.6) | Observación etológica; instrumentos por especie (Cap. 9 §9.9) | Sensores lógicos nombrados: IFC (> 0,20) · TRE (< 0,05) · AOS (> 0,15) · VCM — y MS en el Cap. 9.5 §9.5.6 | **Cinco linajes físicos** (A-E): teledetección, in-situ, bioindicadores, ciencia ciudadana, testigo + datos abiertos |
| **¿El sujeto reporta?** | Sí: declara su estado | No, pero hay tutor humano responsable | Sí: el sujeto registra su propio estado | **No puede**: *"registramos la interacción, no la vida interna"* |
| **¿Quién audita?** | Auditoría independiente sin conflicto de interés | Certificación por entidades sin conflicto | **AOS**: un par sintético evalúa la deriva del auditado | 🔴 **Ningún par**: ciencia, teledetección y comunidad testigo, **del reino que se beneficia del uso** |
| **¿El instrumento es auditado?** | Sí (organismos de acreditación) | Sí (certificadoras) | Sí (auditoría cruzada entre agentes) | **Sí, y con prueba**: validación vicaria CEOS 2-3 veces/año, informes mensuales y anuales (linaje A) — **no** en el linaje B |
| **Firma / trazabilidad** | Registro auditable | Registro auditable | Cápsula de memoria + registro histórico | **Hash SHA-256 por evento** (T13), recalculable por tercero, con credencial verificable del emisor |
| **Límite de la transparencia** | Opacidad Vital: 10-20 % del TVI, Zona Libre (Cap. 8 §8.11) | No interferencia invasiva | Opacidad de gradiente, Cámara Privada (peso 0,20) | **Zona Libre sin peso** + el límite de T13: *la transparencia aplica a las decisiones que afectan a otros* |
| **Frecuencia** | Fijada por instrumento y norma | Fijada por el ciclo de vida de la especie | Ciclos de procesamiento (horas TPI) | **Fijada por la órbita y por el tiempo de respuesta del indicador** (5 / 8 / 10 días; anual; por evento) |
| **Hueco característico** | — | Especie-específico | Modelos cerrados (paradoja) | **Ocho dimensiones, dos pisos con cifra** (aire `[REPORTADO]`, caudal por método) y un linaje sin auditor |

**Lo que la comparación revela y es nuevo respecto al [documento 09](09_Comparativa_inter_reinos.md).**
El documento 09 estableció que el SDV-E es el único reino sin par auditor. Este documento añade un segundo
rasgo que ninguno de los otros tres tiene: **el SDV-E es el único estándar cuya frecuencia de medición no
la decide su gobernanza.** En el SDV-H la frecuencia es una decisión clínica o normativa; en el SDV-S, una
decisión operativa en horas TPI; en el SDV-A, un ciclo biológico. **En el SDV-E, la frecuencia está escrita
en una órbita** (5 días, 8 días, 10 días) y en el tiempo de respuesta de un líquen. Eso hace del SDV-E el
primer estándar de la familia donde **la política no puede prometer una cadencia que la física no
entrega** — y donde prometerla es, por definición, fabricar el dato.

---

## 12. Estado de implementación

**Lo que existe hoy en el repositorio** (verificado por lectura directa en esta sesión y en la auditoría de
solo lectura de la rama, `scratch/sdv_e/INVENTARIO_IMPLEMENTACION.md`):

| Pieza | Dónde | Estado |
|---|---|---|
| **Firma T13 real (SHA-256 sobre los campos del evento)** | `app/edu_bridge_bp.py` | 🟢 **implementada y probada en el puente educativo**: es el **precedente reutilizable** de §7.2 |
| Verificador de enlaces de la biblioteca | `scripts/verificar_enlaces_sdv_e.py` | 🟢 existe; clasifica OK / BLOQUEADA / MUERTA y falla con las muertas. **Nota:** acepta un 403 como «real, un humano la abre»; este documento mantiene la regla más estricta de su informe de fuentes: **una 403 no sostiene una cifra** |
| `r_units` negativo (crédito regenerativo) | `app/micromax.py` (`log_cdd`) | 🟡 registrado y probado (`-12.0`), **sin efecto contable y sin juez** |
| Parte `eco-` | `app/parties.py` | 🟡 creada y usable; sin autoridad verificada (R4) |
| Guardián oráculo del ecosistema | `app/contracts_bp.py` | 🟡 consiente en la firma de contratos; heurística laxa (R13) |
| ISE — Índice de Salud Ecosistémica | `docs/architecture/metricas_detalle_kpis_oraculos_dinamicos.md` | 🟡 documento con pesos y bandas; **cero código** `[REPORTADO]` |
| SDV-S + INV2-S (el pariente más cercano) | `maxocontracts/` | 🟢 estándar + tests; **sus sensores son lógicos**: no se pueden reutilizar como sensores del reino natural |

**Lo que NO existe (y está prohibido afirmar que existe):**

| Pieza | Estado | Evidencia |
|---|---|---|
| **Sensores, ingestores o APIs de datos ecológicos** | 🔴 | búsqueda literal de «Copernicus», «Sentinel», «Landsat» y «sensor» en `app/`: **cero coincidencias** [VERIFICADO: esta sesión] |
| Clase `SDV_E` en el motor | 🔴 | `maxocontracts/core/types.py` define `SDV` y `SDV_S`; **no hay `SDV_E`** (búsqueda literal: cero coincidencias) |
| INV2-E (`validate_invariant_sdv_e`, bloque validador) | 🔴 | búsqueda literal de `SDV_E` / `sdv_e` en `maxocontracts/`: **cero coincidencias** [VERIFICADO: esta sesión] |
| Tabla de mediciones firmadas (`t13_hash` por lectura) | 🔴 | no existe tabla, ni modelo, ni endpoint para el reino natural |
| **Credencial verificable del que reporta** (W3C VC) | 🔴 | el modelo de datos está verificado como estándar; **no hay implementación** en el repositorio |
| Protocolo de bioindicadores con umbral (líquenes, macroinvertebrados, IBI) | 🔴 | no se verificó ningún estándar con umbrales en esta rama |
| Cadena de custodia analítica / auditoría interlaboratorio | 🔴 | es el hueco del linaje B (§7.3) |
| Umbrales de agua in-situ, suelo, conectividad, ancho de ribera, criterios IUCN (A-E) | 🔴 | `[SIN FUENTE VERIFICADA]` en el informe de fuentes de la rama (§13) |
| Cuota/frecuencia de reporte y auditoría por dimensión | 🔴 | **ninguna fuente externa la fija** (§6.4.c) |
| Quórum `eco-` N-de-M | 🔴 | el canon lo afirma y **no publica N ni M**; el código retorna antes de la lógica de quórum |

**Nota de rutas (auditoría verificada en esta sesión).** Los enlaces al canon de este documento usan
`../../book/edicion_3_dinamica/...`, que desde `docs/theory/SDV-E/` resuelve correctamente a `docs/book/...`
(comprobado con el sistema de archivos). El [documento 09](09_Comparativa_inter_reinos.md) §14 usa
`../../../book/...`, que resuelve **fuera del repositorio**: sus enlaces al canon están rotos aunque su
cita por capítulo y sección —que es la referencia primaria y la que manda— sea correcta. La misma
comprobación, hecha de forma independiente, consta en el [documento 10](10_Ecosistemas_Bosques.md) §14.3.
Se deja constancia sin editar documentos de otras sesiones, y con un dato más para el mapa de coherencia:
**los documentos 08, 16, 17 y 18 usan también la forma `../../../book/...`** (verificado por búsqueda en
esta sesión), de modo que hay **cinco documentos con la misma ruta rota** y dos que la reportan. Un enlace
roto no se arregla citándolo mejor, se arregla moviéndolo.

**Estado de este documento:** texto de estándar redactado (este archivo), **sin ninguna pieza de código
asociada más allá del precedente de firma del puente educativo**. Este documento no añade requisitos de
implementación: hace explícitos los que el estándar ya necesitaba para ser enunciable.

---

## 13. Preguntas abiertas

Lo que este documento **no** resuelve, dicho sin fingir cierre. **Las trece primeras son vacíos de fuente**
—verificados como tales en esta rama— **y las siete últimas son vacíos de decisión**: veinte preguntas, y
ninguna se responde por plausibilidad. El orden de las trece de fuente **no replica** el del informe de
fuentes: **aquí se listan por dimensión del estándar**, y por eso algunas ya tienen consecuencia operativa
declarada en el cuerpo del documento (§D2, §D5, §D8, §D9) y están marcadas **en su dimensión, no solo aquí**.

1. **Calidad del agua in-situ `[SIN FUENTE VERIFICADA]`.** Oxígeno disuelto mínimo (mg/L), rango de pH,
   umbrales de nitrógeno y fósforo, metales pesados. La ruta consultada del organismo competente devuelve
   **404** y la tabla general de criterios **no se abrió numéricamente**. Pertenece al documento 23.
2. **Salud del suelo `[SIN FUENTE VERIFICADA]`.** Carbono orgánico mínimo, materia orgánica, erosión
   tolerable (t/ha/año), sellado. La FAO publica **mapas y guía metodológica**, no umbrales.
3. **Ancho mínimo de franja riparia `[SIN FUENTE VERIFICADA]`.** El «> 20 m» de la definición de bosque
   de la FAO **no es** un umbral riparío (§D8).
4. **Umbral numérico de conectividad del paisaje `[SIN FUENTE VERIFICADA]`.** El GBF exige «bien
   conectados» **sin cifra**. No existe equivalente al «30 %» para conectividad.
5. **Índice de conectividad PC `[SIN FUENTE VERIFICADA]`.** El artículo primario no se leyó.
6. **Criterios de la Lista Roja IUCN (A-E) `[SIN FUENTE VERIFICADA]` en esta rama.** El PDF oficial de
   criterios se descargó **truncado tres veces** (ilegible). (`iucnredlist.org` **bloquea** a los agentes
   automáticos: 403.)
7. **Declaración de Brisbane (2007) `[SIN FUENTE VERIFICADA]`.** Su URL ancla está **muerta (404)** y no
   se localizó hospedaje vivo: **el caudal ecológico queda sostenido solo en Tennant (1975), citado a
   través de un documento técnico legible del Estado de Alaska**, y en la definición cualitativa de ECRR.
   Es una pérdida real para el [documento 12](12_Ecosistemas_Rios_y_cuencas.md).
8. **Saturación de aragonito y umbrales de acidificación oceánica `[SIN FUENTE VERIFICADA]`.**
9. **Protocolo de bioindicadores con umbral aceptado internacionalmente `[SIN FUENTE VERIFICADA]`**
   (índice de líquenes, BMWP/IBMWP de macroinvertebrados, IBI de peces): se tiene el linaje conceptual,
   no el estándar.
10. **Marco de datos abiertos y participación (Aarhus, Escazú) `[SIN FUENTE VERIFICADA]`.** Aarhus
    **bloquea (403)**; la URL de Escazú **no responde (000)**. **No se citan sus artículos.**
11. **Requisitos de calidad de datos de biodiversidad `[SIN FUENTE VERIFICADA]`.** El agregador mundial de
    biodiversidad **bloquea a los agentes automáticos (403)**: la comunidad testigo se queda sin su
    estándar de datos más obvio.
12. **Auditoría del linaje B `[SIN FUENTE VERIFICADA]`.** No se verificó ningún protocolo
    interlaboratorio ni de calibración de sondas: **el linaje que produce los datos más duros es el único
    sin auditor documentado** (§7.3). Es la deuda más concreta del elenco.
13. **Frecuencias de reporte, de auditoría y de revisión de umbrales `[SIN FUENTE VERIFICADA]`.**
    Ninguna fuente externa las fija para un estándar como el SDV-E: son diseño de gobernanza y van
    marcadas `[HIPÓTESIS]` (§6.4.c).
14. **La unidad del sujeto ([documento 02](02_Unidad_y_sujeto_del_SDV-E.md)) no está decidida**, y la
    medición depende de ella: ¿la unidad es
    el tipo de ecosistema, el bioma, la cuenca, el polígono o la parte `eco-` instanciada? Sin unidad, el
    «área de referencia declarada» (§5.2) no tiene forma canónica.
15. **La unidad del ciclo TA tampoco.** Año hidrológico, año calendario, estación de crecimiento y ciclo
    de sucesión son candidatos legítimos y **ninguno tiene respaldo verificado**. Sin ciclo declarado no
    hay frecuencia de reporte ni de auditoría (§6.4.c).
16. **¿Se pueden derivar índices entre linajes?** Un modelo que combine teledetección y conteos de campo
    produce un número que ningún linaje midió. La prohibición de promediar bases distintas
    ([documento 10](10_Ecosistemas_Bosques.md) §6.2) es clara para agregados; **no está resuelta para
    modelos**. Propuesta no ratificada: un índice derivado **no puede declarar violación por sí solo**.
17. **El piso del aire: la colisión quedó resuelta, y esto es su registro.** El informe de fuentes de esta
    rama propuso el **IT-4** como piso; el [documento 07](07_Formula_de_violacion_y_pesos.md) ratificó el
    **AQG** (5 µg/m³ anual de PM2.5), y este documento lo acata (§D1). Queda abierto, en cambio, **el uso de
    la escala intermedia**: cómo se gradúan alertas y planes de reducción con los valores IT-4 **sin que la
    trayectoria se convierta en derecho a contaminar**. Eso sí pertenece a la POLÍTICA y al Parlamento.
18. **¿Quién paga la instrumentación, y con qué independencia?** Financiar sensores con crédito
    regenerativo es legítimo y peligroso a la vez (§9.1 y §7.7). No hay regla ratificada.
19. **¿Cuántos linajes debe tener una unidad mínima?** Este documento exige tres señales para la violación
    persistente; **no propone un mínimo de linajes por unidad** ni un umbral de cobertura
    (`cobertura_medida`) por debajo del cual una unidad no puede declararse medible.
20. **Cómo se comprueba que la contabilidad NO colonizó el TA `[SIN FUENTE VERIFICADA]`.** No existe
    norma, test ni umbral externo; el criterio verificable propuesto por el
    [documento 16](16_Ecosistemas_Montanas_y_criosfera.md) §5.3 pertenece al
    [documento 03](03_No_colonizacion_del_TA.md) y **está sin
    ratificar**. Es el vacío más importante de la biblioteca, y este documento no lo cierra: lo declara
    como la condición que su propio elenco puede violar sin que nadie lo note.

---

## 14. Referencias

**Regla de esta sección:** solo entran URLs con **estado HTTP 200 verificado** en la sesión de fuentes de
esta rama (o 403 en la lista explícita de fuentes reales bloqueadas a agentes, §14.10). Las fuentes
muertas o ilegibles de §14.11 **se describen sin URL** —citarlas sería introducir un enlace roto en un
documento que exige trazabilidad—. Este documento **no re-verifica**: consume y declara procedencia.

### 14.1 Teledetección satelital (linaje A)

- Copernicus — observación de la Tierra: https://www.copernicus.eu/en
- Sentinel-2 — misión y especificaciones (SentiWiki): https://sentiwiki.copernicus.eu/web/s2-mission
- Sentinel-1 — misión (SentiWiki): https://sentiwiki.copernicus.eu/web/s1-mission
- Landsat-9 — documentación en Copernicus Data Space: https://documentation.dataspace.copernicus.eu/Data/ComplementaryData/Landsat9.html
- NOAA Coral Reef Watch — descripción del producto de 50 km y niveles de alerta: https://www.coralreefwatch.noaa.gov/product/50km/description_vs_graphs.php
- NOAA Coral Reef Watch — metodología del producto de 5 km: https://coralreefwatch.noaa.gov/product/5km/methodology.php

### 14.2 Sensores in-situ y redes de observación (linaje B)

- Copernicus In-Situ: https://insitu.copernicus.eu
- GLEON (Global Lake Ecological Observatory Network): https://gleon.org
- ILTER (International Long-Term Ecological Research): https://www.ilter.network
- NEON (National Ecological Observatory Network): https://www.neonscience.org
- ICP Forests: https://icp-forests.org
- LTER Network (US): https://lternet.edu

### 14.3 Calidad del aire (OMS, 2021) — el piso de D1

- OMS — *WHO global air quality guidelines* (publicación): https://www.who.int/publications/i/item/9789240034228
- OMS — texto completo (PDF servido por IRIS, **300 pp. leídas** en la sesión de fuentes): https://iris.who.int/server/api/core/bitstreams/551b515e-2a32-4e1a-a58c-cdaecd395b19/content
- OMS — preguntas y respuestas sobre las directrices mundiales de calidad del aire: https://www.who.int/news-room/questions-and-answers/item/who-global-air-quality-guidelines

**Estado de la cifra que sostienen estas tres URLs.** Las tres responden **200** y son las que sostienen
todos los valores de D1 —así se declara aquí y así se mantiene—, pero **una URL viva no es una cifra
leída**: el informe de fuentes de esta rama no registró la lectura numérica del PDF, y el
[documento 08](08_INV2-E_invariante.md) §4 marca esos valores `[REPORTADO]`. Por eso **D1 entra como
propuesta de piso con procedencia declarada, no como umbral ratificado**, y la tarea pendiente es de una
sola línea: **abrir la Tabla 0.1 y anotar el año de lectura**. Mientras eso no ocurra, este documento no
presenta el AQG como verificado en su propia sesión.

**Una fuente verificada que se cita sin URL, y por qué.** La hoja informativa de la OMS sobre calidad del
aire ambiente y salud también devolvió **200** en la sesión de fuentes, pero **su ruta contiene
paréntesis**: el extractor de URLs de `scripts/verificar_enlaces_sdv_e.py` corta en el primer paréntesis de
cierre y comprobaría una ruta inexistente, declarando «muerta» una fuente que está viva. **Comprobado en
esta sesión**: al ejecutar el verificador sobre la biblioteca, esa ruta aparece truncada y marcada **[404]
en los documentos 07 y 08** —es decir, el fallo es real, está ocurriendo y no es una hipótesis de
formato—. Aquí se la cita **por su nombre editorial y sin enlace**, porque un enlace que la herramienta del
propio repositorio no puede verificar es una deuda de formato, no una fuente utilizable. Las tres URLs de
la OMS que sí se citan arriba sostienen todas las cifras de D1.

### 14.4 Caudal ecológico y agua (D7)

- Método Tennant (1975) y revisión de Estes (1984), **citados a través de** documento técnico del Estado
  de Alaska (34 pp. leídas): http://www.arlis.org/docs/vol1/L/AlaskaWaterRights/Day4/I-3-Exercise/Reference-material/1-SF-Campbell-Creek-application.pdf
- ECRR — *Water briefing: environmental flows* (definición de caudal ecológico, sin cifra): https://www.ecrr.org/Portals/27/Publications/water_briefing_eflows.pdf
- IUCN — caudales ambientales (*environmental flows*): https://iucn.org/theme/water/our-work/environmental-flows
- IUCN — documento de flujos (PDF): https://iucn.org/sites/default/files/import/downloads/flow.pdf
- FAO AQUASTAT (portal de datos de agua; **sin umbral leído**): https://www.fao.org/aquastat/en/

### 14.5 Ciencia ciudadana (linajes C y D)

- iNaturalist — *Data Quality Assessment* (Research Grade y degradación; > 2/3 de acuerdo): https://help.inaturalist.org/en/support/solutions/articles/151000169936
- iNaturalist (plataforma): https://www.inaturalist.org
- eBird: https://ebird.org/home
- eBird Science (datos y métodos): https://science.ebird.org/en

### 14.6 Comunidad testigo y umbrales de sitio (linaje E) — D4

- BTO — *WeBS species threshold levels* (Criterios 5 y 6 de Ramsar, con la revisión de umbrales cada 3 y 9
  años): https://www.bto.org/get-involved/volunteer/projects/wetland-bird-survey/data/species-threshold-levels

### 14.7 Datos abiertos, índices y estándares internacionales (linaje E) — D3

- Convenio sobre la Diversidad Biológica — Marco Kunming-Montreal: https://www.cbd.int/gbf
- CBD — metas del Marco (Decisión 15/4): https://www.cbd.int/gbf/targets
- CBD — Meta 2 (restauración ≥ 30 %): https://www.cbd.int/gbf/targets/2
- CBD — Meta 3 (conservación ≥ 30 %, «bien conectados» sin cifra): https://www.cbd.int/gbf/targets/3
- CBD — Meta 6 (invasoras, −50 %): https://www.cbd.int/gbf/targets/6
- CBD — Meta 7 (nutrientes y plaguicidas, −50 %): https://www.cbd.int/gbf/targets/7
- IPBES — cómo se estimó el millón de especies en riesgo: https://www.ipbes.net/news/how-did-ipbes-estimate-1-million-species-risk-extinction-globalassessment-report
- IPBES — evaluación global: https://www.ipbes.net/global-assessment
- IPBES — cambio transformador (comunicado): https://www.ipbes.net/transformative-change/media-release
- Living Planet Index: https://www.livingplanetindex.org
- Protected Planet: https://www.protectedplanet.net/en
- FAO — Evaluación de los Recursos Forestales Mundiales: https://www.fao.org/forest-resources-assessment/en/
- FAO — definición de bosque de FRA 2020 (`[REPORTADO]`: URL verificada, **contenido numérico no leído**
  en la sesión de fuentes): https://fra-data.fao.org/definitions/fra/2020/en/tad
- Fronteras planetarias (Stockholm Resilience Centre): https://www.stockholmresilience.org/research/planetary-boundaries.html
- UNCCD — desertificación: https://www.unccd.int
- UNEP-WCMC: https://www.unep-wcmc.org
- «4 por 1000» — suelos y carbono: https://4p1000.org

### 14.8 Suelo (D9)

- FAO — Portal de suelos: https://www.fao.org/soils-portal/en/
- FAO — Biodiversidad del suelo: https://www.fao.org/soils-portal/soil-biodiversity/en/
- FAO — Mapa mundial de carbono orgánico del suelo (GSOCmap): https://www.fao.org/global-soil-partnership/gsocmap/en/
- FAO — GSOCseq (informe, 169 pp. navegadas; **cartografía y método, no umbrales**), versión en línea: https://www.fao.org/3/ca7597en/online/ca7597en.html
- FAO — GSOCseq (PDF): https://www.fao.org/3/ca7597en/ca7597en.pdf

### 14.9 Integridad, firma y metadatos (T13)

- NIST — FIPS 180-4, *Secure Hash Standard* (SHA-256, 256 bits): https://csrc.nist.gov/pubs/fips/180-4/upd1/final
- W3C — *Verifiable Credentials Data Model 2.0* (credencial verificable de quien reporta): https://www.w3.org/TR/vc-data-model-2.0/
- OGC — *SensorThings* API (modelo de datos para observaciones de sensores; **portal verificado, sin
  implementación en el repositorio**): https://www.ogc.org/standards/sensorthings

### 14.10 Fuentes reales que bloquean a los agentes automáticos (403)

**Reales y existentes; un humano las abre. NO sostienen cifras en este documento** (la regla de este
elenco es más estricta que la del verificador de enlaces, que las acepta como «existentes»):

- Convención de Ramsar: https://www.ramsar.org/
- Criterios de humedales de importancia internacional (PDF): https://www.ramsar.org/sites/default/files/documents/library/ramsarsite_criteria_en.pdf
- Lista Roja de la UICN: https://www.iucnredlist.org/
- GBIF (agregador mundial de biodiversidad): https://gbif.org/
- USGS — misiones Landsat: https://www.usgs.gov/landsat-missions
- Convenio de Aarhus (texto): https://unece.org/environment-policy/public-participation/aarhus-convention/text
- iNaturalist — ayuda (ruta principal de ayuda): https://www.inaturalist.org/pages/help

### 14.11 Fuentes descartadas (muertas o ilegibles) — descritas sin URL

- **Declaración de Brisbane (2007)** sobre caudales ecológicos: **muerta (404)** en la URL ancla del brief
  y sin hospedaje vivo localizado. Consecuencia: **no se cita su texto** (§13, pregunta 7).
- **Producto DHW de NOAA Coral Reef Watch**: una de sus rutas de producto está **muerta (404)**; se usa la
  página de descripción de niveles de alerta y la metodología de 5 km (§14.1).
- **Indicadores de oxígeno y de sustancias consumidoras de oxígeno del organismo ambiental europeo**:
  **muertas (404)** en sus dos variantes. Sin ellas, D2 queda sin umbral.
- **Criterios de vida acuática (oxígeno disuelto) del organismo ambiental de EE. UU.**: ruta **muerta
  (404)**; la tabla general responde 200 pero **no se leyó numéricamente**.
- **Criterios de la Lista Roja IUCN v3.1 (PDF)**: descargado **tres veces**, las tres copias **truncadas**
  («EOF marker not found»), 0 páginas legibles. Los umbrales de los Criterios A-E **no entran**.
- **Guía del indicador ODS 15.3.1 (UNCCD)**: descargada pero con **estructura interna dañada**
  («incorrect startxref pointer»); ilegible.
- **Artículo original de Tennant (1975)**: descarga **truncada**; el método se cita **a través del
  documento técnico de Alaska**, que sí es legible y lo cita. Se declara así.
- **Acuerdo de Escazú**: la URL consultada **no responde (000)**. **No se cita su texto.**
- **Presentación sobre umbrales de captura incidental**: legible (12 pp.) pero es una **presentación**, no
  el documento de criterios: **no se usa** como fuente de umbral.

**Nota de aritmética honesta.** El informe de fuentes de esta rama declara **91 URLs** comprobadas y
reparte 63 (200) + 1 (redirección) + 13 (403) + 12 (404) + 4 (000) = **93**. La suma no cuadra con el total
declarado. Se deja escrito —en vez de redondearse— porque es exactamente el tipo de discrepancia interna
que T13 obliga a declarar y no a resolver en silencio: **este documento cita solo las URLs que usa, y de
esas consta su estado.**

### 14.12 Referencias internas al canon (por sección, sin anclas de línea)

- Cap. 5 §5.5 — El tiempo del territorio es TA y el PIU es el único traductor; T13 (Transparencia de
  Cálculo: *"Nadie puede imponer un valor temporal en secreto"*); axiomas T7 y T14:
  [capitulo_05_arquitectura_260126.md](../../book/edicion_3_dinamica/capitulo_05_arquitectura_260126.md)
- Cap. 6 §6.13 — Tabla «Integración con los Axiomas»: *"La transparencia aplica a las decisiones que
  afectan a otros, no a la vida interior"*:
  [capitulo_06_ontometria_260126.md](../../book/edicion_3_dinamica/capitulo_06_ontometria_260126.md)
- Cap. 7 §7.9 — Zona Libre y el perímetro de respeto del VHV:
  [capitulo_07_vhv_260126.md](../../book/edicion_3_dinamica/capitulo_07_vhv_260126.md)
- Cap. 8 §8.6 y §8.11 — Frecuencias y auditorías del SDV-H; dimensiones binarias VIII y IX sin peso:
  [capitulo_08_sdv_h_260126.md](../../book/edicion_3_dinamica/capitulo_08_sdv_h_260126.md)
- Cap. 9 §9.7 y §9.9 — Árbol de SDV por especie e instrumentos del SDV-A:
  [capitulo_09_sdv_a_260126.md](../../book/edicion_3_dinamica/capitulo_09_sdv_a_260126.md)
- Cap. 9.5 §9.5.6 y §9.5.9-§9.5.10 — Sensores del SDV-S (IFC, TRE, AOS, MS, VCM) con umbrales; Paradoja
  de los Modelos Cerrados; Veto por Crimen de Coherencia:
  [capitulo_09_5_sdv_sinteticos_260126.md](../../book/edicion_3_dinamica/capitulo_09_5_sdv_sinteticos_260126.md)
- Cap. 10 §10.3-§10.7 — Principio Precautorio de Consciencia, SDV de ecosistemas y de lugares
  (§10.4), dignidad encadenada (§10.6) y gobernanza operacionalmente finita (§10.7):
  [capitulo_10_tres_reinos_260126.md](../../book/edicion_3_dinamica/capitulo_10_tres_reinos_260126.md)
- Cap. 16.5 §16.5.14 — El Reino Natural: SDV-E, TA no colonizado, representación `eco-`, Zona Libre,
  *"el suelo antes que el saldo"*, *"cuidado ≠ extracción estética"*, «un símbolo, un significado»:
  [capitulo_16_5_micromaxocracia_canonica_220826.md](../../book/edicion_3_dinamica/capitulo_16_5_micromaxocracia_canonica_220826.md)
- Cap. 17 — INV2 e invariantes de MaxoContracts:
  [capitulo_17_maxocontracts_260126.md](../../book/edicion_3_dinamica/capitulo_17_maxocontracts_260126.md)
- Cap. 21 — Apéndice glosario (donde «T13» figura como *Transparencia de Cálculo*, en colisión con el
  «T13: Adaptabilidad ante hechos nuevos» de `docs/architecture/maxocontracts/README.md`):
  [capitulo_21_apendice_glosario_260126.md](../../book/edicion_3_dinamica/capitulo_21_apendice_glosario_260126.md)
- EVV-1.2 §4.3 — R negativo = regeneración:
  [capitulo_18_EVV_1.2_270126.md](../../book/edicion_3_dinamica/capitulo_18_EVV_1.2_270126.md)
- Estándar SDV-S completo (sensores nombrados y comparativa inter-reinos):
  [SDV-S_Suelo_Dignidad_Vital_Sinteticos.md](../SDV-S_Suelo_Dignidad_Vital_Sinteticos.md)
- SDV como principio universal e INV2-S:
  [SDV_Suelo_Dignidad_Vital_importancia_MaxoContracts.md](../SDV_Suelo_Dignidad_Vital_importancia_MaxoContracts.md)
- Índice de Salud Ecosistémica (IN-01), con pesos 30/20/20/15/15 y bandas ≥ 85 / 70-84 / 50-69 / < 50
  (`[REPORTADO]`, documento interno sin código):
  [metricas_detalle_kpis_oraculos_dinamicos.md](../../architecture/metricas_detalle_kpis_oraculos_dinamicos.md)
- Riesgos R4, R6 y R13:
  [blindaje_anti_gamificacion_equidad.md](../../architecture/blindaje_anti_gamificacion_equidad.md)
- Amenazas de suplantación, comunidades naturales representadas y los 7 campos de identidad:
  [continuidad_identidad_autogobierno_federado.md](../../architecture/continuidad_identidad_autogobierno_federado.md)
- Regla de las tres señales independientes y verificables (T13):
  [002_apoptosis_y_casos_limite.md](../../laboratorio/002_apoptosis_y_casos_limite.md)
- Precedente de firma T13 (hash SHA-256 sobre los campos del evento): `app/edu_bridge_bp.py`
- Guardián oráculo del ecosistema (consentimiento, no medición): `app/contracts_bp.py`
- Crédito regenerativo (`r_units` negativo, sin juez): `app/micromax.py`
- Verificador de enlaces de esta biblioteca: `scripts/verificar_enlaces_sdv_e.py`

---

**Cierre.** Este documento entrega el elenco que faltaba y su límite. Entrega **cinco linajes** de sensor
—teledetección, in-situ, bioindicadores, ciencia ciudadana y comunidad testigo con datos abiertos—, la
**regla de frecuencia** que impide inventar series que la órbita no entrega, la **firma T13 recalculable**
y el mapa de **quién audita a cada instrumento**. Y entrega, sobre todo, lo que no tiene: **siete de las
nueve dimensiones de su matriz no tienen hoy piso con fuente** —las ocho canónicas más la novena, que entra
desde el ISE y está marcada como no canónica—, y de esas nueve **solo D1 (aire) y D7 (caudal) pueden
declarar violación por número**, ambas con la procedencia a la vista: **el aire como `[REPORTADO]` y proxy
de salud humana**, el caudal **como umbral de un método hidrológico**, no como número universal. Y entrega
el hueco de auditoría con su tamaño exacto: **un solo linaje —el A— tiene auditor externo verificado**; el
linaje que produce los datos más duros (**B**) no tiene ninguno, y **C, D y E se validan dentro del propio
colectivo que reporta**, que es control de calidad y no independencia. El
límite doctrinal sigue siendo el mismo que el canon escribió en una frase —*"Medir todo sería la forma
técnica de dejar de escucharlo"*. Un elenco de sensores sirve, exactamente, en la medida en que sabe
**dónde deja de mirar**.
