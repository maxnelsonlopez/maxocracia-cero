# La no-colonización del Tiempo Absoluto
## Los mínimos que protege: que el tiempo del ecosistema no sea reescrito por el calendario, la unidad de cuenta, el precio ni la definición de quien contabiliza — y el mecanismo verificable (CNC = 0) que hoy no existe

**Autoría:** Oráculo Sintético DeepSeek & Max Nelson López Restrepo
**Fecha:** octubre 2026
**Proyecto:** Maxocracia — El gobierno de la verdad, el tiempo y la vida
**Licencia:** Creative Commons BY-SA 4.0
**Estado:** Propuesta de estándar (rama SDV-E, Ola 4) — NO canon hasta ratificación
**Referencia canónica:** Cap. 10 §10.4 · Cap. 16.5 §16.5.14 · EVV-1.2 §4.3 · Cap. 9.5 (precedente SDV-S)
**Documento:** 03 de la biblioteca `docs/theory/SDV-E/`
**Pieza que aporta:** el **Contador de No Colonización (CNC)**, su umbral exacto **CNC = 0** y diez casos de prueba falsables — especificación, no implementación

---

## 1. Qué es (y qué no es) este SDV

**La regla que este documento convierte en ingeniería.** El canon fija dos frases y ninguna tiene prueba:

> *"la contabilidad doméstica no coloniza el tiempo ajeno. El PIU (Cap. 5 §5.5) es quien traduce entre
> TA y TVI; nosotros registramos la interacción, no la vida interna del ecosistema."*
> — Cap. 16.5 §16.5.14 `[VERIFICADO]`

La familia de la biblioteca condensa esa regla en una fórmula que se repite en los documentos 09, 10,
13, 16 y 18: *"el tiempo del territorio es TA y no se coloniza (el PIU traduce)"*. Es una regla
correcta y es, hoy, **una intención sin test**. El brief de esta rama lo registra como hueco abierto:
*"No hay forma de verificar que la contabilidad NO colonizó el TA: no hay test, ni invariante, ni
umbral. La biblioteca debe proponerlo."* Este documento lo propone, y lo propone **como clase de acto
auditable**, no como métrica de buena voluntad.

**Qué es este documento.**

1. **La definición operativa de «colonización del TA»**, en tres sentidos separados y falsables (§1.2).
   Sin esa separación, «no colonizar» es un eslogan: se puede afirmar y negar sin contradicción.
2. **Seis guardas auditables** (G1 a G6) que cubren los modos conocidos de colonización del registro
   sobre el sujeto **salvo uno, declarado abierto**: la colonización por definición (F3, §1.1), que
   ninguna de las seis audita porque auditan asientos y no definiciones (§13.6). Dos de esas guardas no
   son aportación propia: vienen del [documento 16](./16_Ecosistemas_Montanas_y_criosfera.md) §5.3
   (invariancia ante el periodo contable, aquí G4) y del
   [documento 06](./06_Medicion_y_verificacion_T13.md) §7.4 (simetría de transparencia, aquí G6). El
   test del ciclo que el [documento 18](./18_Ecosistemas_Agroecosistemas.md) §11.3 aporta **es otra
   cosa** —un test sobre el sujeto, no sobre el registro— y por eso no se funde en el CNC: se cita como
   vía de validación cruzada en §6.1. Aquí se integran, se numeran y se les da un contador común. **No
   se descarta ninguna de las dos heredadas.**
3. **El Contador de No Colonización**: `CNC(R) = número de asientos del registro R que violan al menos
   una guarda`, con umbral **exacto cero**, no votable, y con la cláusula de no vacuidad que impide
   que el silencio se confunda con inocencia (§5).
4. **El perímetro del PIU** (Protocolo de Intercambio Universal, Cap. 5 §5.5): el canon lo declara
   *único* traductor TA↔TVI. Un traductor único es, por definición, el punto por donde pasa toda
   colonización posible. Aquí se le ponen tres cerrojos auditables (§4.7), y se declara lo que el
   traductor **no** puede hacer.
5. **La prueba negativa** que impide que el SDV-E fabrique un peso moral sobre el ecosistema (§4.8),
   con respaldo en el propio estándar de valoración del proyecto: los niveles de consciencia y el
   factor de sufrimiento viven en el componente **V** del EVV-1.2 §4.2, y ese componente **no es el
   registro del SDV-E**.

**Qué no es.**

- **No es un documento de umbrales ecológicos.** No fija ningún piso de agua, aire, suelo, biodiversidad
  ni caudal. La frontera es deliberada: este documento no mide el ecosistema, audita **el registro**
  que dice medirlo. Los pisos son del [documento 07](./07_Formula_de_violacion_y_pesos.md) y de los
  documentos 10 a 23.
- **No es la implementación del PIU.** El PIU no existe como código: `PIU.valorar_ta_natural` es hoy
  un `pass` con comentario en
  [DISENO_IMPLEMENTACION_FUTURA.md](../../architecture/DISENO_IMPLEMENTACION_FUTURA.md) `[VERIFICADO]`.
  Este documento especifica **qué tendría que declarar** el PIU para no colonizar; no lo construye.
- **No ratifica la categoría «Persona Natural»** ni el quórum `eco-` N-de-M: pertenecen a los
  documentos [02](./02_Unidad_y_sujeto_del_SDV-E.md) y
  [05](./05_Representacion_guardian_y_mandato.md).
- **No promete que el registro sea completo.** El CNC certifica que el registro **no se excede**;
  nunca que **alcance**. La Zona Libre del Reino Natural sigue intacta (Cap. 16.5 §16.5.14, salvaguarda
  1) y se trata en el [documento 04](./04_Zona_Libre_del_Reino_Natural.md).
- **No tiene precedente bibliográfico verificado.** No existe —en la literatura que esta rama pudo
  verificar— un umbral publicado para «grado de colonización epistémica de un registro contable sobre
  un sistema natural». El umbral `CNC = 0` es una **decisión axiomática** (T9 + T13 + T14), no un valor
  empírico. Se declara así en §5.5 y §13.1, y esa declaración es parte del resultado.

**Marcas de evidencia usadas en todo el texto.** `[VERIFICADO]` = comprobado con herramienta o leído en
el archivo citado en esta sesión. `[REPORTADO]` = afirmado por una fuente citada a la que no se pudo
acceder directamente. `[HIPÓTESIS]` = inferencia razonada del proyecto, sin respaldo externo.
`[SIN FUENTE VERIFICADA — pendiente de consenso científico]` = se buscó el umbral y no existe fuente
verificable. **La cuarta marca es un resultado legítimo y, en este documento, frecuente.**

### 1.1 El problema, enunciado sin adornos

Una contabilidad coloniza el tiempo del ecosistema cuando **el registro sustituye al territorio**:
cuando una celda del libro mayor pasa a ser tratada como el hecho que dice representar. El canon ya
tiene el nombre de ese error, aunque no lo aplique al Reino Natural: *"El mapa no es el territorio"*
(EVV-1.2 §3.6) `[VERIFICADO]`. Colonizar el TA es confundir el mapa con el territorio **en la
dimensión del tiempo**.

Hay tres formas de cometer ese error, y las tres están hoy abiertas en el proyecto:

| # | Forma | Cómo se ve en la práctica | ¿Existe hoy defensa? |
|---|---|---|---|
| F1 | **Colonización por conversión** | El TA del ecosistema se traduce a TVI o a precio, y ese número pasa a decidir el veredicto sobre el ecosistema | 🔴 no: el PIU es un `pass` y nada audita su dirección |
| F2 | **Colonización por reloj** | La ventana de muestreo, el periodo contable o la frecuencia de reporte los fija el contador, no el proceso físico | 🔴 no: ningún campo del registro almacena el tiempo característico del sujeto |
| F3 | **Colonización por definición** | El sujeto «existe» o «deja de existir» según un umbral del contador: un rodal que cae de 11 % a 9 % de cobertura cambia de categoría sin que el ecosistema cambie de naturaleza | 🔴 no: la definición FAO de bosque es operativa y convencional (FAO, 2020) |

**El caso F3 no es retórico y tiene fuente.** La definición vigente del término «bosque» es: tierra de
más de **0,5 ha**, con árboles de más de **5 m** y cobertura de copa superior al **10 %** (FAO, FRA
2020, Términos y definiciones) `[VERIFICADO]`. La deforestación se define como la caída bajo esa
cobertura `[VERIFICADO]`, y «otras tierras boscosas» cubre la banda de **5 % a 10 %** `[VERIFICADO]`.
Es decir: **la frontera entre «hay bosque» y «no hay bosque» es una decisión de frontera, no un hecho
del ecosistema.** Un estándar que herede ese umbral sin declararlo está dejando que el contador
nombre al sujeto. Este documento no cambia el umbral: exige que esté **declarado como decisión**.

### 1.2 Qué significa exactamente «el TA no se coloniza»

La frase admite tres lecturas, y solo dos son correctas. Se separan aquí porque de esta separación
depende todo el mecanismo de §4 y §5.

**(a) El TA no se convierte en magnitud valorada.** El tiempo del ecosistema puede aparecer en el
registro como **coordenada** (la marca de un instante, la ventana de una medición) y **nunca como
cantidad** que se sume, se pondere, se compre o se venda. Esta es la lectura fuerte, y tiene respaldo
en el propio estándar de valoración del proyecto: el componente **T** del VHV mide *"consumo de Tiempo
Vital Indexado (TVI) humano"*, en **hora-persona** (EVV-1.2 §4.1 y §4.4) `[VERIFICADO]`. El tiempo
del ecosistema **no cabe** en T. Y el crédito regenerativo —la parte del registro que toca al Reino
Natural— vive en **R**, no en T: *"Permite valores negativos… genera un VHV Negativo en este
componente"* (EVV-1.2 §4.3) `[VERIFICADO]`. Esta propiedad de diseño ya existe y es la base de todo
lo demás: **el registro del proyecto no almacena TA como costo; almacena interacciones humanas con
efecto sobre el soporte vital.**

**(b) El TA no se sustituye por su registro.** Ninguna celda puede subir ni bajar el veredicto sobre
el ecosistema por el hecho de existir, de faltar o de haberse medido con un instrumento distinto.
Esto es la traducción temporal de *"el suelo antes que el saldo"* (Cap. 16.5 §16.5.14) y del aviso de
la propia fuente internacional de restauración: *"el potencial de restauración no debe ser considerado
como una justificación para la degradación adicional de ecosistemas"* (CBD, notas guía de la Meta 2
del Marco Kunming-Montreal, 2022) `[VERIFICADO]`.

**(c) El TA no se mide.** — **Falso, y hay que decirlo.** El canon no prohíbe medir el ecosistema:
prohíbe medir *su vida interna*. La diferencia es la que separa un dato de una interpretación. Los
sensores miden salud —agua, cobertura, biodiversidad indicadora— y *"jamás 'milagros'"*
(Cap. 16.5 §16.5.14, salvaguarda 1). Lo que no se mide es lo inefable, y eso no es una prohibición de
medir: es un **límite de perímetro** que el [documento 04](./04_Zona_Libre_del_Reino_Natural.md)
desarrolla. Un estándar que confundiera (c) con (a) se volvería inoperante por pureza; el brief ya
advirtió que *"medir todo sería la forma técnica de dejar de escucharlo"*, y su simétrico también es
cierto: no medir nada sería la forma técnica de no poder protegerlo.

**Definición de trabajo, ya con las tres lecturas separadas:**

> `[HIPÓTESIS]` **Colonización del TA.** Un registro R de sostenimiento sobre una unidad ecológica
> `eco-u` **coloniza el TA** cuando al menos uno de sus asientos no puede escribirse como la tupla de
> una interacción declarada (§4.0), o cuando el veredicto de violación de esa unidad depende del reloj,
> del precio o de la definición de quien contabiliza, y no del estado del sujeto.

---

## 2. Preámbulo metodológico

El SDV-H lo tiene y el SDV-S lo omitió; el brief prohíbe repetir la omisión. Aquí es imprescindible,
porque este documento **audita al auditor**: escribe reglas sobre el acto de contar. Nueve reglas
gobiernan todo lo que sigue.

**Regla 1 — Registrar no es medir la vida interna; registrar es dejar huella de una interacción.**
Toda magnitud del registro debe poder responderse con la pregunta *¿qué intercambio ocurrió entre
quién y qué, medido con qué?* Si la respuesta honesta es *«el estado interior del ecosistema»*, no es
un dato: es una afirmación en su nombre.

**Regla 2 — El tiempo del sujeto manda.** TA, nunca TVI ni TPI (Cap. 16.5 §16.5.14; Cap. 5 §5.5). El
Axioma T7 enumera las tres escalas —*"TA (Tiempo Absoluto), TVI (Tiempo Vital Indexado Humano), TPI
(Tiempo de Procesamiento Indexado Digital)"*— y el Axioma T9 fija el marco:
*"El Tiempo Absoluto (TA) existe independientemente de la perspectiva humana y debe respetarse como
marco universal que incluye a los Tres Reinos"* (Cap. 5) `[VERIFICADO]`. Este documento no define esos
axiomas: los cita, y solo los usa en su literalidad.

**Regla 3 — El traductor es el primer sospechoso.** Si el PIU es el *único* traductor autorizado
(Cap. 5 §5.5), entonces **toda** colonización por conversión (F1) pasa por él. Auditar el registro sin
auditar al traductor sería auditar la puerta y no la llave. De ahí §4.7.

**Regla 4 — La traducción informa; no adquiere.** Que el PIU pueda expresar *cuánto TVI humano ahorra
un humedal* no lo autoriza a **comprar** TA con ese número. La traducción tiene dirección declarada y
no es reversible como medio de pago: del valor en TVI de un servicio ecosistémico no se reconstruye el
tiempo del ecosistema. La razón es del propio estándar internacional de contabilidad ambiental: las
perspectivas de valor *"no son en algún modo aditivas… no debería concluirse que, reconociendo todos
los tipos de valor, podría obtenerse un valor agregado de la naturaleza"* (SEEA EA §2.58; UN, 2021)
`[VERIFICADO]`; y los valores de intercambio *"no provee[n] un valor monetario más amplio que
incorpore los beneficios directos e indirectos recibidos de los ecosistemas, incluidos sus valores de
no-uso"* (SEEA EA §2.62) `[VERIFICADO]`.

**Regla 5 — LEY y POLÍTICA, separadas.** El **piso** es LEY y **no se vota**; la **plenitud** es
POLÍTICA y **sí se vota**, con el procedimiento del Parlamento Educativo (categoría `critical`: quórum
60 %, consenso 75 %, T13, anti-flip-flop 14 días, `CHECK` en BD). Aquí la separación es tajante y poco
intuitiva: **`CNC = 0` no se vota** (no mide magnitud, mide clase de acto), mientras que **la escalera
de consecuencias, las ventanas de auditoría y el Óptimo de cada guarda sí se votan** (§5.5, §5.6).

**Regla 6 — Ninguna cifra cruza de reino.** Un umbral de salud humana no es un umbral de salud
ecosistémica, aunque el organismo que lo publique nombre a los ecosistemas. Este es el caso exacto de
las directrices de calidad del aire: la OMS las enmarca como protección de la salud humana *"y de los
ecosistemas"* `[VERIFICADO]`, pero sus valores guía (PM₂.₅ ≤ 5 µg/m³ anual; OMS, 2021) son umbrales
**antropocéntricos**. Usarlos como piso del SDV-E es una **decisión de traducción del PIU**, y como
tal debe declararse. `[HIPÓTESIS]` de encuadre, con la cita `[VERIFICADO]`.

**Regla 7 — La duda no absuelve al contador.** El Principio Precautorio de Consciencia (Cap. 10 §10.3)
y el T14 (Cap. 5) ponen la carga de la prueba en quien propone. Aplicado al registro: **ante duda
sobre si un asiento registra una interacción o afirma un estado interno, se trata como colonización
hasta que exista instrumento declarado.** No se castiga al ecosistema por la duda: se marca el asiento
y se exige instrumentarlo. La duda, aquí, no produce violación ecológica: produce **opacidad**.

**Regla 8 — Sin propósito declarado no hay sensor legítimo.** *"Lo que no cambia una decisión que
afecta a otros, no se mide. Si un dato no puede modificar ninguna decisión sobre el ecosistema,
producir ese dato es vigilancia, no transparencia"* ([documento 06](./06_Medicion_y_verificacion_T13.md)
§7.4) `[HIPÓTESIS]` de la familia, coherente con T13. La guarda G1 lo convierte en campo obligatorio.

**Regla 9 — La auditoría debe ser operacionalmente finita.** El canon lo exige para la gobernanza
(Cap. 10 §10.7: *"La gobernanza debe ser operacionalmente finita"*) `[VERIFICADO]`. Un test de
colonización que exigiera modelar la cadena trófica completa para emitir un veredicto no sería un
test: sería una promesa. Las seis guardas de §4 se comprueban **sobre el registro**, no sobre el
ecosistema, y por eso son finitas.

---

## 3. Pilares epistemológicos

**Pilar 1 — Separación hecho/valor, aplicada al tiempo.** *"El termómetro no receta."* El estándar EVV
mide magnitudes físicas y *"la valoración (asignación de precios en Maxos) es un proceso político
posterior"* (EVV-1.2 §3.2) `[VERIFICADO]`. Corolario temporal: **la marca de tiempo es un hecho; el
precio del tiempo es un valor.** Si un vector de precios puede cambiar una violación ecológica, el
valor se comió al hecho — y eso es exactamente lo que la guarda G3 prohíbe.

**Pilar 2 — El principio anti-fiat protege al ecosistema de la escritura.** *"No se puede crear valor
por decreto. Todo reporte VHV debe estar respaldado por evidencia física verificable (sensores, logs,
trazabilidad biológica) **o consenso comunitario directo**. El dinero no es evidencia de valor"*
(EVV-1.2 §3.1) `[VERIFICADO]`. Dos consecuencias que se usan en la guarda G1 (§4) y en §6.1: (i) una celda sin respaldo
físico ni consenso no es un dato débil, es **una escritura en nombre del ecosistema**; (ii) el consenso
comunitario **sí** es evidencia legítima, lo que obliga a definir «instrumento» de forma que la
observación humana protocolizada quepa dentro y no sea castigada por no ser un sensor.

**Pilar 3 — Inconmensurabilidad: la naturaleza no tiene un valor agregado.** El estándar internacional
de contabilidad de ecosistemas declara su propio límite: su foco son *"valores de origen
antropocéntrico… valores instrumentales o de uso"* (SEEA EA §2.60) `[VERIFICADO]`; el valor intrínseco
se define como *"el valor que algo tiene independientemente de toda experiencia o evaluación humana…
no adscrito ni generado por agentes valorantes externos"* (SEEA EA §2.56) `[VERIFICADO]`; y la
contabilidad de servicios ecosistémicos *"no provee una evaluación completa"* de la relación
ecosistema–personas, porque los valores relacionales e intrínsecos quedan fuera (SEEA EA §6.6)
`[VERIFICADO]`. Este pilar sostiene la prueba negativa de §4.8: **un registro que asigne valor
intrínseco actúa como «agente valorante externo», y la fuente define el valor intrínseco precisamente
por su exclusión.**

**Y el marco dominante no es una excepción: es la regla.** El sistema de cuentas nacionales remite
expresamente al SEEA como estándar internacional para medir capital natural (SNA 2025, Cap. 35; UN
Statistics Division, 2025) `[VERIFICADO]`. Es decir: **la contabilidad de la naturaleza que el mundo
está adoptando es, por diseño, una contabilidad de valores de intercambio.** Eso no la vuelve ilegítima
—la vuelve útil y peligrosa a la vez—, y explica por qué la colonización por conversión (F1) no es una
hipótesis del proyecto: es la consecuencia previsible de adoptar ese marco **sin guardas**. Las seis
guardas de §4 son esas guardas.

**Pilar 4 — Auditabilidad T13: el cálculo se publica, la intimidad no.** El Axioma T13 exige que todo
cálculo de TA, TVI o cascadas temporales sea auditable públicamente, *"con metodología explícita y
posibilidad de disputa mediante métodos alternativos verificables"* (Cap. 5) `[VERIFICADO]`. Aplicado
al SDV-E, la regla operativa es asimétrica por diseño: se publica del ecosistema el parámetro, el
valor, la unidad, la ventana, el método, la incertidumbre y el hash; **no** se publica ni se infiere
una interpretación de su estado interior.

**Pilar 5 — Declarar la variable de control es parte del dato, no un anexo.** La recopilación de
referencia sobre fronteras planetarias advierte: *"el riesgo con múltiples variables de control
coexistiendo es que se obtengan resultados diferentes para el mismo país según cuál variable de control
se haya usado… simplificar [el resultado] sin declarar la variable de control usada puede por tanto
inducir a error"* (CERAC 2024, §2.4; sintetizando Steffen et al. 2015 y Richardson et al. 2023)
`[VERIFICADO]`. Un número sin variable de control declarada no es un número: es un número con
sobreentendidos.

**Pilar 6 — Un símbolo, un significado.** El canon nombra el problema (*"un símbolo, un significado"*,
Cap. 16.5 §16.5.14, tabla de colisiones) y el repositorio ya convive con dos colisiones activas que
afectan **directamente** a este documento `[VERIFICADO]`:

- **T9.** En el libro, T9 es *No-Antropocentrismo Temporal* (Cap. 5). En el motor de ingeniería, la
  etiqueta «T9» se usó para *Reciprocidad Justa* y fue renumerada: `maxocontracts/core/axioms.py`
  conserva el alias `validate_t9_reciprocidad = validate_t17_reciprocidad` y su comentario remite al
  [mapa de axiomas](../../book/edicion_3_dinamica/integraciones_pendientes/mapa_axiomas_ingenieria_puente.md).
  El riesgo documentado R6 del
  [blindaje anti-gamificación](../../architecture/blindaje_anti_gamificacion_equidad.md) sigue hablando
  de «T9 (Reciprocidad Justa)». **Cuando este documento dice T9, dice No-Antropocentrismo Temporal.**
- **TPI.** El Axioma T7 lo llama *"Tiempo de Procesamiento Indexado Digital"* (Cap. 5) y el cuerpo
  del Cap. 5 y el glosario lo llaman *"Tiempo Procesal Indexado"* `[VERIFICADO]`. Importa aquí porque
  **el guardián oráculo es un agente sintético: su reloj nativo es TPI**, y no puede firmar el registro
  de un sujeto TA con su propio reloj (§4.7, cerrojo 3).

**Pilar 7 — La contabilidad nunca se borra.** *"El sistema no expulsa. Reintegra"* — pero el registro
no se borra (T13). Consecuencia para este mecanismo: un `CNC > 0` **no se corrige en silencio**. Se
marca, se conserva y se instrumenta (§7.4).

---

## 4. Dimensiones del SDV-E: las seis guardas de no colonización (CNC)

Las «dimensiones» de este documento no son parámetros del ecosistema: son **clases de acto del
registro**. Es exactamente el precedente canónico de las dimensiones binarias sin peso del SDV-H: las
dimensiones VIII (Rehabilitación) y IX (Opacidad Vital) *"se registran cualitativamente y mediante
umbrales binarios (presencia/ausencia del derecho), no mediante pesos en la fórmula — medir la
rehabilitación o la opacidad con la misma vara cuantitativa que el agua o la vivienda las destruiría"*
(Cap. 8 §8.11). Igual aquí: **medir la colonización con la misma vara que la calidad del agua la
destruiría**, porque la colonización no tiene magnitud: tiene presencia o ausencia.

### 4.0 La tupla del asiento (contra qué se compara cada guarda)

Sea **R** el registro de sostenimiento de una unidad ecológica `eco-u` (Cap. 16.5 §16.5.14). Cada
asiento *e* de R se escribe:

`e = ⟨ t_TA , eco-u , m , x_antes , x_después , i , u_i , σ_i , s , π , Δt_TA ⟩`

| Campo | Qué es | Regla |
|---|---|---|
| `t_TA` | marca temporal en **Tiempo Absoluto** | coordenada, nunca cantidad (§1.2a) |
| `eco-u` | la unidad ecológica sujeto (documento 02) | una unidad, un registro |
| `m` | magnitud de la **interacción** (no del estado del ecosistema) | número + unidad |
| `x_antes`, `x_después` | estado observado de la variable física antes y después | ambos o ninguno |
| `i` | **instrumento o protocolo declarado** (incluye protocolo de observación humana) | no nulo |
| `u_i` | unidad de medida del instrumento | no nulo |
| `σ_i` | incertidumbre declarada | no nulo |
| `s` | signo (`R` negativo = crédito regenerativo, EVV-1.2 §4.3) | referenciado al componente correcto |
| `π` | **propósito declarado** de la medición (Regla 8) | no nulo |
| `Δt_TA` | **tiempo característico del proceso** medido, con fuente | no elegido por el contador (G2) |

`[HIPÓTESIS]` Los nueve primeros campos provienen del informe de fuentes de esta rama; los dos últimos
(`π`, `Δt_TA`) se añaden aquí porque las guardas G2 y G5 los necesitan para ser falsables, y porque
sin `π` la Regla 8 no sería auditable. La ampliación se declara para que quede claro qué es herencia y
qué es propuesta.

**Tesis falsable del documento:** *un asiento que no puede escribirse como esa tupla no registra una
interacción — registra una afirmación sobre la vida interna del ecosistema. La contabilidad colonizó
el TA.*

---

### Guarda G1: Linaje instrumental (*cada número tiene un padre*)

**Qué protege.** Que ninguna cifra del registro entre sin instrumento, unidad, incertidumbre y
propósito declarados. Es la guarda que impide la escritura por decreto.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| Asientos con al menos una celda numérica sin instrumento/protocolo declarado (`i` nulo) | **0** | — (acto de clase, no de magnitud) | EVV-1.2 §3.1 (canon del proyecto) `[VERIFICADO]` |
| Asientos con al menos una celda numérica sin unidad (`u_i`) | **0** | — | T13 (Cap. 5) `[VERIFICADO]` |
| Asientos con al menos una celda numérica sin incertidumbre (`σ_i`) | **0** | — | SEEA EA, documentación explícita de métodos y datos `[REPORTADO]` |
| Asientos con al menos una celda numérica sin propósito (`π`) | **0** | — | documento 06 §7.4 `[HIPÓTESIS]` del proyecto (el principio es de la familia; la conversión en campo obligatorio es aportación de este documento) |
| Reproducibilidad por un tercero independiente | — | **sí**: el mismo asiento, con los mismos insumos, da el mismo número | `[HIPÓTESIS]` Óptimo votable: ningún estándar consultado publica un criterio de reproducibilidad para un libro mayor ecológico |
| Asientos que almacenan magnitudes de TA como cantidad | **0** | — | EVV-1.2 §4.1/§4.4 (T en hora-persona) `[VERIFICADO]` |

**Justificación.** *"El dinero no es evidencia de valor"* (EVV-1.2 §3.1) y *"no se puede crear valor por
decreto"*. Si el registro de un ecosistema admite una cifra sin padre instrumental, el mecanismo queda
satisfecho por redacción: bastaría escribir «mejoró» con un número al lado. La incertidumbre es
obligatoria, no cortesía: sin `σ_i` no hay forma de distinguir una violación de ruido, y la propia
fuente de referencia sobre fronteras planetarias advierte que un resultado sin su variable de control
*"puede inducir a error"* (CERAC 2024, §2.4).

**Protocolo.** Auditoría de metadatos sobre el registro, no sobre el ecosistema: para cada celda
numérica se comprueba la existencia de los cinco campos (`i`, `u_i`, `σ_i`, `π`, y `Δt_TA` para las que
dependan del tiempo). Se ejecuta en cada ciclo de verificación. Quien reporta: la comunidad de custodia
y el guardián oráculo (§6.2). Un campo vacío no es un dato faltante: es **un asiento incompleto**, y se
cuenta.

**Violación.** Existe al menos un asiento con una celda numérica a la que le falta alguno de los campos que
le corresponden (`i`, `u_i`, `σ_i`, `π`, y `Δt_TA` en las que dependan del tiempo). Es un
hecho verificable por lectura del registro, sin peritaje: no requiere saber ecología, requiere leer el
libro mayor. **Unidad de conteo, para que no haya ambigüedad (§13.5):** se cuenta **asientos**, no celdas
—varias celdas sin linaje dentro de la misma fila son **una** violación, porque auditar celdas
multiplicaría el mismo error por columna—.

---

### Guarda G2: Autoridad del reloj (*el proceso fija la frecuencia, no el contador*)

**Qué protege.** Que la ventana de muestreo la dicte el proceso físico del sujeto y no el ciclo de
reporte humano (ejercicio fiscal, mandato, ciclo contable doméstico, gana de publicar).

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| Relación entre muestreo y tiempo característico, **leída desde el sujeto: cuanto mayor el cociente, más ciego el registro** | `Δt_muestreo ≤ Δt_TA / 2` (el piso: el muestreo no puede ser más lento que esto) | `Δt_muestreo ≤ Δt_TA / 10` (la plenitud: aspirar a la ventana más fina) | `[HIPÓTESIS]` del proyecto; ningún estándar verificado publica este cociente |
| `Δt_TA` citado con fuente | **obligatorio** (no elegido) | `Δt_TA` con margen de consenso científico declarado | UNCCD 2017 · NOAA CRW `[VERIFICADO]` |
| Cambiar `Δt` para mejorar el índice | **prohibido** (bandera roja dura) | — | T13 (Cap. 5) `[VERIFICADO]` |
| Ventana de observación de cambio del sujeto | **≥ 10 años** cuando el sujeto es cobertura y productividad de la tierra | — | UNCCD, Nota metodológica LDN, 2017 `[VERIFICADO]` |

**Justificación.** El único modo honesto de fijar una frecuencia es preguntarle a la disciplina del
sujeto cuánto tarda el sujeto en cambiar, y hay tres casos verificados que lo demuestran, todos de
fuentes externas:

1. **Un proceso lento exige una ventana larga.** El marco de neutralidad en la degradación de la tierra
   define su horizonte mínimo de observación en **10 años** para los tres sub-indicadores obligatorios
   (cobertura terrestre, dinámica de productividad, carbono orgánico del suelo), con el año base
   fijado en **2000** y un periodo de referencia de **3 a 5 años** para la línea base de productividad
   (UNCCD, 2017) `[VERIFICADO]`. Muestrear eso cada ejercicio contable no mide al sujeto: mide al
   contador.
2. **Un proceso rápido exige una ventana corta.** El estrés térmico de arrecifes se acumula en
   **semanas**: el indicador DHW suma los HotSpots de las **últimas 12 semanas**, con umbral de
   blanqueamiento en **1 °C** por encima de la media del máximo de verano local, blanqueamiento
   significativo en **4 degree C-weeks** y severo con mortalidad significativa en **8** (NOAA Coral
   Reef Watch) `[VERIFICADO]`. Un arrecife auditado cada 10 años estaría tan mal auditado como un
   glaciar auditado cada semana.
3. **El tiempo biológico no es el tiempo administrativo.** Los criterios de la Lista Roja de la IUCN
   expresan la reducción poblacional *"en 10 años **o 3 generaciones**"*, y usan umbrales de extensión
   de presencia de **100 / 5 000 / 20 000 km²**, de área de ocupación de **10 / 500 / 2 000 km²** y de
   individuos maduros desde **50** (IUCN, 2001) `[VERIFICADO]`. **«O tres generaciones» es la prueba de
   que la unidad de tiempo del sujeto no es el año del contador**: para una especie longeva, tres
   generaciones pueden ser un siglo.

**Protocolo.** Por cada parámetro con umbral, el registro debe declarar `Δt_TA` con su fuente y
`Δt_muestreo` efectivo. La auditoría comprueba la relación y marca dos banderas: `Δt_muestreo > Δt_TA / 2`
(ceguera) y `Δt` modificado entre ciclos sin cambio en la fuente de `Δt_TA` (ajuste de conveniencia).
Ambas son verificables con el histórico del propio registro, que T13 obliga a conservar.

**Violación.** Existe al menos un parámetro cuyo `Δt_muestreo` supera el piso de `Δt_TA / 2`, o cuyo
`Δt_TA` no está citado con fuente, o cuyo `Δt` fue alterado sin justificación documentada. **El umbral
numérico que dispara la violación es el piso, no el Óptimo**: superar `Δt_TA / 2` viola; muestrear entre
`Δt_TA / 10` y `Δt_TA / 2` cumple el piso y queda por debajo de la plenitud. La obligación de declarar el
reloj y su fuente es LEY; la magnitud del cociente se vota (§5.5).

> **Nota honesta.** `[HIPÓTESIS]` El cociente `Δt_TA / 2` **no tiene fuente verificada**: es una
> decisión de diseño del proyecto, análoga al criterio de Nyquist pero sin pretensión de derivarlo.
> Ningún estándar consultado publica un cociente mínimo entre frecuencia de muestreo y tiempo
> característico del ecosistema. Se marca como propuesta, y por eso el piso es votable en su
> *magnitud* aunque la obligación de declarar el reloj sea LEY (Regla 5, §5.5). **Y la dirección hay que
> decirla, porque es donde el SDV-H se equivocó con el agua: aquí el piso es el cociente más permisivo
> (`/2`) y la plenitud la más exigente (`/10`). El error histórico sería declarar `/10` como piso, que
> es lo que haría un documento que confundiera la aspiración con la ley.**

---

### Guarda G3: Invariancia ante precios y preferencias (*el precio no cambia el hecho*)

**Qué protege.** Que ninguna clasificación de violación ecológica se mueva cuando se mueve el dinero.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| Perturbar solo el vector de precios y recalcular `déficit = (requerido − actual) / requerido` | **invariante exacto**: ninguna violación de `{0,1}` cambia | — (no hay óptimo: es una identidad lógica) | SEEA EA §2.62 y §2.58; EVV-1.2 §3.2 `[VERIFICADO]` |
| Valores de no-uso y relacionales incorporados a la cuenta | **no exigido** (la cuenta no los tiene por diseño) | declarados como ausentes antes de usarse | SEEA EA §6.6 `[VERIFICADO]` |
| Agregación de perspectivas de valor en un solo número | **prohibida** | — | SEEA EA §2.58 `[VERIFICADO]` |

**Justificación.** La fuente externa es explícita y no deja margen interpretativo: los valores de
intercambio *"no provee[n] un valor monetario más amplio"* y las perspectivas de valor *"no son en
algún modo aditivas"*. El canon del proyecto dice lo mismo en tres palabras: *"El termómetro no
receta"*. Si un cambio de precio puede convertir un humedal bajo su SDV-E en un humedal en coherencia,
el estándar dejó de ser un suelo y pasó a ser un mercado.

**Protocolo.** Prueba de perturbación reproducible por cualquiera: se toma el registro, se sustituye
**solo** el vector de precios por otro (incluido uno absurdo: todo a cero, todo al doble) y se recalcula
el veredicto. Si cambia alguna violación, FALLA. Es la prueba que la **comunidad testigo** puede
ejecutar sin ser perito (§7.3), y por eso es auditabilidad T13 y no peritaje.

**Violación.** Cualquier cambio en el conjunto de violaciones bajo perturbación de precios. No hay
gradualidad: es exacto o no es.

---

### Guarda G4: Invariancia ante el periodo contable (*cambiar el calendario no cambia el veredicto*)

**Qué protege.** Que el veredicto mida al sujeto y no al contador. Es el criterio propuesto por el
[documento 16](./16_Ecosistemas_Montanas_y_criosfera.md) §5.3, que lo remitió expresamente a este
documento, y aquí se formaliza como guarda con test propio.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| Recalcular el déficit con **particiones distintas del mismo intervalo** (no con dos periodos administrativos elegidos por el contador) | **invariante exacto**: el déficit no puede depender del periodo contable | — | documento 16 §5.3 `[HIPÓTESIS]` |
| Origen de todo denominador de la fórmula | constante física · línea base del propio sujeto · ventana que la disciplina exige | ventana que la disciplina exige, publicada por la disciplina | documento 16 §5.3 `[HIPÓTESIS]` |
| Rellenar un denominador cero con una constante de conveniencia | **prohibido** | — | documento 16 §5.2 `[HIPÓTESIS]` |

**Justificación.** *"Si la fórmula usa el calendario del observador como denominador, coloniza el tiempo
del sujeto"*. El argumento no necesita fuente externa porque es una identidad: si dos particiones
distintas del mismo intervalo producen veredictos distintos sobre el mismo estado físico, el veredicto
no habla del estado. Y hay un respaldo externo indirecto del mismo tipo de error: el marco de
neutralidad de la tierra **elige un año base (2000)** y llama «neutralidad» a que las ganancias
compensen las pérdidas (UNCCD, 2017) `[VERIFICADO]` — es decir, fija el veredicto en el calendario. Ese
marco es el **contraejemplo verificado** contra el que el SDV-E se define (§9).

**Protocolo.** Test `test_sdv_e_no_coloniza_ta` (nombre propuesto): recalcular cada dimensión con **al menos
dos particiones distintas del mismo intervalo** y exigir invariancia. Coste computacional nulo: es el mismo
cálculo con otra partición de los datos. **Y una precisión que este documento se debe a sí mismo:** las dos
particiones **no pueden ser dos periodos administrativos** (12 y 6 meses), porque usar el calendario humano
como unidad del test es repetir la colonización por reloj que G2 prohíbe, y porque el sujeto lento —
carbono del suelo, UNCCD 2017— no muestra cambio en 6 meses. Las particiones se toman del **reloj del
sujeto**: cortes internos del propio registro, o múltiplos declarados de `Δt_TA`. Si por comodidad de
implementación se usan ventanas calendario, se declaran como lo que son —unidades del contador— y la
invariancia se exige igual con cualquier otra partición.

**Violación.** Que el déficit de una dimensión cambie al cambiar la partición del intervalo, o que algún
denominador provenga de un ciclo administrativo (ejercicio fiscal, mandato, ventana de reporte elegida
por quien reporta). **No se admite como «periodo contable legítimo» ninguna ventana medida en meses o
años del calendario humano**: mientras el denominador sea del contador, el veredicto es del contador.

---

### Guarda G5: Clausura unidireccional (*se registra la interacción, no la vida interna*)

**Qué protege.** Que el registro contenga interacciones —insumos, observaciones, productos— y no
estados internos del ecosistema. Es la guarda que traduce literalmente el canon: *"nosotros registramos
la interacción, no la vida interna del ecosistema"* (Cap. 16.5 §16.5.14).

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| Campos no instrumentales que expresan estado interno del ecosistema | **0** | — | Cap. 16.5 §16.5.14 `[VERIFICADO]` |
| Campos que ponderan grado de consciencia, intención, sufrimiento o valor intrínseco del ecosistema | **0** | — | EVV-1.2 §4.2 (NC nivel 0: 0,0) `[VERIFICADO]`; Cap. 10 §10.3 y §10.4 `[VERIFICADO]` |
| Publicación de la incertidumbre de cada campo | — | **sí**: cada campo con su `σ_i` y su método visibles | Óptimo votable; SEEA EA (documentación de métodos) `[VERIFICADO]` |
| Toda cifra clasificable como insumo, observación o producto | **obligatorio** | — | `[HIPÓTESIS]` de clasificación |

**Justificación.** La clausura es *unidireccional* porque hay una única dirección legítima del flujo: el
mundo afecta al sensor y el sensor produce un número; el número **no** produce mundo. Un campo como
«bienestar del humedal» sin instrumento no es un dato: es el contador hablando en nombre del humedal.
Y el caso del peso moral tiene respaldo literal en el propio sistema de valoración del proyecto: el
componente **V** mide *"el impacto en la experiencia consciente de seres sintientes"* mediante niveles
de consciencia (NC) y factor de sufrimiento (FS), y su tabla asigna al nivel 0 —*"Plantas, hongos,
bacterias, minerales"*— un factor de **0,0**, remitiendo expresamente su protección a **R** (EVV-1.2
§4.2) `[VERIFICADO]`. Es decir: **el canon ya decidió que la protección de lo no consciente no se
expresa como peso moral.** Un registro del SDV-E que produzca un peso moral no está protegiendo más al
ecosistema: está reclamando para sí una categoría que el canon asigna a otro estándar (el SDV-A).

**Protocolo.** Clasificación campo por campo del esquema del registro: cada campo debe ser (a) insumo,
(b) observación con instrumento, (c) producto, o (d) coordenada temporal. Cualquier quinto caso se
cuenta como violación hasta que se instrumente. La auditoría se hace sobre el **esquema**, no sobre los
valores: es la única guarda que puede auditarse sin abrir un solo dato de campo.

**Violación.** Existe al menos un campo sin instrumento que no es insumo, observación, producto ni
coordenada; o existe al menos un campo que pondera consciencia, intención o valor intrínseco del
ecosistema.

---

### Guarda G6: Simetría de transparencia (*no se le exige al río lo que no se le exige a quien lo seca*)

**Qué protege.** Que la carga de prueba y la carga de publicación recaigan sobre quien afecta, no sobre
quien no puede firmar. Es la regla 3 del [documento 06](./06_Medicion_y_verificacion_T13.md) §7.4,
formalizada aquí como guarda.

| Parámetro | Mínimo Absoluto (el piso) | Óptimo (plenitud aspiracional) | Fuente |
|---|---|---|---|
| Transparencia exigida al ecosistema vs. exigida al actor que lo afecta | **simetría**: el ecosistema nunca debe más campos ni más evidencia que el actor | **el actor publica más** (asimetría a favor del ecosistema) | documento 06 §7.4 `[HIPÓTESIS]`; T13 (Cap. 5) `[VERIFICADO]` |
| Evidencia declarada por el actor por cada parámetro medido en el ecosistema | **1:1 como mínimo** | 1:N | T14 (Cap. 5): la carga de la prueba recae en quien propone `[VERIFICADO]` |
| Parámetros exigidos al ecosistema sin contraparte declarada en el actor | **0** | — | documento 06 §7.4 `[HIPÓTESIS]` |

**Justificación.** *"La asimetría es la prueba de la violación: si la transparencia exigida al
ecosistema… es mayor que la exigida al actor que lo afecta, hay colonización del TA"* (documento 06
§7.4). El respaldo canónico es el T14 (Cap. 5): *"La carga de la prueba recae sobre quien propone
acciones que afectan la temporalidad de no-participantes"* `[VERIFICADO]`. Un sensor en el río sin
declaración equivalente de quien vierte es vigilancia con forma de ciencia.

**Protocolo.** Tabla de correspondencia: cada parámetro del elenco que se mide en el ecosistema se
empareja con la declaración exigida al actor correspondiente (vertido, extracción, obra). La auditoría
cuenta parámetros huérfanos. La tabla es pública y la mantiene la comunidad de custodia.

**Violación.** Existe al menos un parámetro medido sobre el ecosistema sin contraparte declarada en el
actor que lo afecta, o la evidencia exigida al ecosistema supera la exigida al actor.

---

### 4.7 El perímetro del PIU: la única puerta y sus tres cerrojos

El canon es tajante: el PIU (Protocolo de Intercambio Universal, Cap. 5 §5.5) es el **único** traductor
TA↔TVI, y su pregunta canónica es *"¿Cuántos TVIs humanos se ahorran o enriquecen gracias a esta
inversión de TA o TPI?"* `[VERIFICADO]`. El mecanismo de anclaje propuesto por el canon es la
**Energía Neta Transformada (ENT)**, con gobernanza del Oráculo Dinámico `[VERIFICADO]`.

**Hay que decir lo incómodo:** esa pregunta canónica es, literalmente, una valoración del TA **en
tiempo humano**. El canon no lo esconde —lo declara: *"El valor del TA del Realm Natural se mide por
los TVIs humanos que ahorra o posibilita"* ([arquitectura temporal](../../architecture/arquitectura_temporal_coherencia_vital.md))
`[VERIFICADO]`. Por tanto **el PIU no puede quedar fuera del perímetro auditado**: es el punto exacto
por donde F1 (colonización por conversión) entraría si el traductor no rinde cuentas. Tres cerrojos,
todos verificables:

**Cerrojo 1 — Dirección declarada y no reversible como pago.** Toda traducción declara su dirección
(TA→TVI informativa) y su fecha. La traducción **no** habilita comprar, canjear ni extinguir TA: del
valor en TVI de un servicio ecosistémico no se reconstruye el tiempo del ecosistema. Fundamento
externo: la no aditividad de las perspectivas de valor (SEEA EA §2.58) y el alcance limitado de los
valores de intercambio (SEEA EA §2.62) `[VERIFICADO]`; fundamente interno: Regla 4.

**Cerrojo 2 — Cada traducción es un asiento más.** La salida del PIU no es un oráculo: es una entrada
del registro, con `i` (motor y modelo que la produjo, firma T13), `u_i`, `σ_i` y `π`. Y queda sujeta a
G1-G6 como cualquier otra. Un número del PIU sin incertidumbre declarada viola G1.

**Cerrojo 3 — El traductor no firma con su reloj.** El guardián oráculo es un agente del Reino
Sintético: su tiempo nativo es **TPI**, no TA (Cap. 5 §5.5; Axioma T7). Por tanto **el guardián puede
consentir, pero no puede fechar**: las marcas `t_TA` del registro provienen de instrumentos o de
protocolos de observación declarados, nunca del reloj de proceso del guardián. Confundir el reloj del
guardián con el del ecosistema sería colonización por la vía del representante.

**Lo que el PIU sí puede hacer, y es mucho:** traducir **interacciones** (lo que el ecosistema ahorra,
purifica, regula, sostiene) para que dejen de ser externalidad gratuita. **Lo que no puede hacer:**
traducir **estados** (lo que el ecosistema *es*) ni alimentar el veredicto del invariante. La segunda
mitad es el invariante P8 del [documento 08](./08_INV2-E_invariante.md) §8.3: *"la conversión TA↔TVI
solo por PIU y **fuera** del invariante"* `[VERIFICADO]`. `[HIPÓTESIS]` La frontera
interacción/estado es la aportación de este apartado y **está sujeta a disputa** (§13.9): el canon no
la traza con estas palabras.

### 4.8 Prueba negativa obligatoria (el falso positivo del «grado de consciencia»)

Ninguna entrada compatible con las seis guardas puede afirmar, implicar ni ponderar **grado de
consciencia, intención, sufrimiento o valor intrínseco** del ecosistema. La ponderación de consciencia
es una operación del **SDV-A** sobre individuos sintientes (Cap. 9), no del SDV-E sobre unidades
ecológicas. Si el registro del SDV-E produce un peso moral, **ha colonizado**: se ha apropiado de una
categoría que no le corresponde, y lo ha hecho sobre un sujeto que no puede disputarlo.

**Respaldo externo** `[VERIFICADO]`: el valor intrínseco se define como aquel que algo tiene
*"independientemente de toda experiencia o evaluación humana… no adscrito ni generado por agentes
valorantes externos"* (SEEA EA §2.56). Un registro que lo **asigne** se convierte en agente valorante
externo, que es exactamente lo que la definición excluye. **Respaldo interno** `[VERIFICADO]`: el
componente V del EVV-1.2 §4.2 asigna factor 0,0 al nivel de consciencia 0 y remite la protección de
plantas, hongos, bacterias y minerales a **R**. **Respaldo axiomático** `[VERIFICADO]`: el Axioma T9
establece que el TA *"existe independientemente de la perspectiva humana y debe respetarse como marco
universal que incluye a los Tres Reinos"* (Cap. 5) — un peso moral **es** una perspectiva humana
adscrita al ecosistema.

---

## 5. Fórmula de violación, pesos y umbrales
## El contador cuenta asientos: por qué no lleva pesos, por qué su umbral es 0 exacto y por qué su base neutra vale 1,0

### 5.1 La fórmula

```
CNC(R) = | { e ∈ R : e viola al menos una de las guardas G1…G6 } |

Invariante:   CNC(R) = 0
Condición de validez:   CNC(R) = 0  ∧  R ≠ ∅  ∧  cobertura declarada
```

**Sin pesos. Sin suma ponderada. Sin factor multiplicativo.** Esta es la decisión central del
documento y se justifica en tres pasos:

1. **La colonización no tiene magnitud, tiene presencia.** Ponderarla con la misma vara que un
   parámetro ecológico la destruiría (Cap. 8 §8.11, dimensiones VIII y IX). Un `CNC` ponderado
   permitiría «un poco de colonización», que es la negación del invariante.
2. **Agregar sería repetir el acto que se quiere detectar.** Convertir seis clases de acto en un índice
   único es asignarles un valor de intercambio común. Las perspectivas de valor *"no son aditivas"*
   (SEEA EA §2.58). El mecanismo no puede hacer con las guardas lo que prohíbe hacer con el humedal.
3. **Un contador es auditable por lectura.** Cualquier ciudadano puede contar celdas sin linaje. Un
   índice ponderado exigiría confiar en los pesos, y los pesos serían votables — con lo que la
   prohibición de escribir en nombre del ecosistema quedaría a disposición de una mayoría.

### 5.2 Base neutra: exactamente 1,0 cuando la violación es 0

El SDV-S tuvo que corregir `FS_S = 1,0 + e^v` → `FS_S = e^v` porque la primera versión recargaba el
100 % incluso sin violación. Aquí se declara la propiedad equivalente **antes** de que exista código:

| Estado | `CNC(R)` | Efecto sobre el factor de violación ecológica | Efecto sobre el registro |
|---|---|---|---|
| Sin violación | **0** | **ninguno**: el factor no se recarga (base neutra exacta) | válido como evidencia de coherencia |
| Con violación | **> 0** | **ninguno** | **no válido como evidencia**, con independencia del saldo |

`CNC = 0` es el estado sin violación, y el CNC **no multiplica nada**: es una **compuerta**, no un factor.
Por eso este documento **no escribe un factor propio** (nada de `FE_TA`): el factor `FE = e^v` pertenece al
estándar de violación y a su corrección de base neutra (SDV-S), y el único compromiso del CNC con él es
**no recargarlo** cuando no hay violación. La razón es que el CNC no mide cuánto se violó
el suelo del ecosistema; mide si el registro es o no es prueba. Multiplicarlo por la violación
ecológica confundiría dos cosas: *el ecosistema está mal* y *nuestra cuenta del ecosistema no es
confiable*. La primera se arregla restaurando; la segunda, instrumentando.

### 5.3 El umbral: cero exacto, y por qué no puede ser otro

| Opción de umbral | Qué significaría | Por qué se rechaza |
|---|---|---|
| `CNC ≤ k` con `k > 0` | Tolerar k asientos escritos en nombre del ecosistema | Un solo asiento sin linaje ya es una escritura en su nombre; tolerar k es tolerar la clase de acto |
| `CNC / R` (proporción, normalizada por volumen de registro) | Tolerar una fracción de asientos escritos en nombre del ecosistema | Premia al que registra más y castiga al que registra poco; y hace que el veredicto dependa del tamaño de la cuenta, no del acto |
| `CNC` ponderado | Graduar la colonización | Requiere pesos votables sobre una prohibición (véase §5.1, punto 3) |
| **`CNC = 0`** | **Cero asientos sin linaje, sin autoridad de reloj, sin dependencia de precio, sin dependencia de periodo, sin estado interno, sin asimetría** | Es una condición sobre **clase de acto**, verificable por lectura, finita y no negociable |

### 5.4 Cláusula de no vacuidad: el vacío no es inocencia

**Este es el punto donde el mecanismo podía fallar en silencio, y hay que decirlo antes de que alguien
lo explote.** Un registro vacío tiene `CNC = 0` trivialmente. Un contador que no instrumenta nada
obtendría el certificado de no colonización **por no haber contado**. Sería el mismo error de clase que
`1 + e^v`, con otra cara: en lugar de recargar sin violación, **absolver sin registro**.

El repositorio tiene un precedente que va en la dirección contraria y hay que citarlo con precisión:
`validate_invariant_vhv_auditable` declara que *"Una lista vacía es válida por vacuidad: si no hay
acciones, no hay VHV que ocultar"* (`maxocontracts/core/axioms.py`) `[VERIFICADO]`. **Ahí la vacuidad
es correcta**: si nadie actuó, nadie ocultó nada. **Aquí la vacuidad es una estafa**: el ecosistema
existe y no se midió. Por eso el CNC necesita una condición de no vacuidad que INV3 no necesita, y por
eso el invariante se escribe con dos términos y no con uno:

```
válido(R)  ⟺  CNC(R) = 0  ∧  R ≠ ∅  ∧  cobertura declarada
```

Un registro vacío o de cobertura incompleta no produce `cumple`: produce el estado **`indeterminado`**
del [documento 08](./08_INV2-E_invariante.md) §8.4, con bandera de opacidad ecológica y obligación de
instrumentar. `[HIPÓTESIS]` Esta cláusula es aportación de este documento y **no está ratificada**.

### 5.5 LEY y POLÍTICA: qué se vota y qué no

| Elemento | LEY (no votable) | POLÍTICA (votable) |
|---|---|---|
| El invariante `CNC = 0` | **sí** · no mide magnitud, mide clase de acto | — |
| La obligación de declarar `i`, `u_i`, `σ_i`, `π` y `Δt_TA` | **sí** | — |
| La obligación de declarar la variable de control de cada umbral | **sí** | — |
| La prohibición de ponderar consciencia o valor intrínseco (G5) | **sí** | — |
| El cociente `Δt_muestreo ≤ Δt_TA / 2` | — | **sí**: la magnitud del cociente se vota; la obligación de declarar el reloj es LEY |
| El Óptimo de cada guarda (reproducibilidad, publicación de incertidumbre, asimetría pro-ecosistema) | — | **sí** |
| La escalera de consecuencias ante `CNC > 0` (§5.6) | — | **sí**, con el procedimiento `critical` (quórum 60 %, consenso 75 %, T13, anti-flip-flop 14 días) |
| La ventana de auditoría por tipo de unidad ecológica | — | **sí** (con el piso de la G2 como límite duro) |

**Base del reparto.** Es el mismo reparto del Parlamento Educativo (INV2-EDU): **la ley vive en el
motor y no se vota; la plenitud aspiracional sí.** Que `CNC = 0` sea LEY no la vuelve dogmática: la
vuelve **no negociable por mayoría**, que es precisamente lo que el canon pide para los mínimos del
diseño biológico (Cap. 16.5 §16.5.14). Si la mayoría pudiera votar cuánta colonización tolera, el
suelo dejaría de ser suelo.

### 5.6 Escalera de consecuencias (votable)

`[HIPÓTESIS]` Propuesta de grados de consecuencia **procesal**, no de castigo al ecosistema ni a
personas:

| Grado | Condición | Consecuencia | Fundamento |
|---|---|---|---|
| **C0** | `CNC = 0` ∧ registro no vacío ∧ cobertura declarada | Registro válido como evidencia de coherencia | base neutra §5.2 |
| **C1** | `1 ≤ CNC ≤ 5`, todas las violaciones en G1 o G2 | Marca en el registro + obligación de instrumentar en el ciclo siguiente; el registro **no** sirve como evidencia de coherencia | T13; `indeterminado` (documento 08 §8.4) |
| **C2** | `CNC > 5` o violación de G3 o G4 | Registro marcado como **no auditable**; el crédito regenerativo de esa unidad queda **en cuarentena** | doc. 08 §8.4 (crédito en cuarentena) |
| **C3** | Violación de G5 o G6, **una sola basta** | El registro no es válido como evidencia; bandera de **opacidad ecológica**; obligación de instrumentar antes de cualquier declaración de cumplimiento | prueba negativa §4.8; simetría, guarda G6 (§4) |
| **C4** | Violación de G5 o G6 **reincidente** tras instrumentación | Retractación del contrato que invocaba el registro como evidencia; **el registro no se borra** | T13; INV2-E (§8) |

**Los grados C1-C4 se votan; C0 no.** Y hay una regla que la escalera no puede violar: **la
consecuencia recae sobre el registro, el contrato o la actividad humana, jamás sobre la unidad
ecológica** (propiedad P6 del [documento 08](./08_INV2-E_invariante.md) §8.3: *"El sujeto protegido
nunca es el objeto de la consecuencia"*). Un ecosistema no puede ser sancionado por la mala contabilidad
de sus contadores.

---

## 6. Protocolo de medición (quién audita, cuándo, con qué)

Esta sección es incómoda por diseño: **el objeto medido por este protocolo es el registro, no el
ecosistema.** No hay sensores nuevos que instalar en el río para auditar la colonización; hay campos
obligatorios que exigir al libro mayor. Es la única forma de que la auditoría sea operacionalmente
finita (Regla 9).

### 6.1 Qué se audita, con qué instrumento

| Guarda | Instrumento de auditoría | Unidad de conteo | Incertidumbre | Frecuencia |
|---|---|---|---|---|
| G1 | El esquema del registro + la tabla de instrumentos declarados | celda numérica | no aplica (conteo) | cada ciclo de reporte del sujeto |
| G2 | Histórico de `Δt_muestreo` y la fuente citada de `Δt_TA` | parámetro | no aplica (comparación) | cada ciclo + revisión anual de fuentes |
| G3 | Perturbación reproducible del vector de precios | veredicto binario | nula (identidad lógica) | cada auditoría de comunidad testigo |
| G4 | Recálculo con dos ventanas contables | veredicto binario | nula (identidad lógica) | cada auditoría de comunidad testigo |
| G5 | El esquema del registro (clasificación de campos) | campo | no aplica (clasificación) | al crear o modificar el esquema |
| G6 | Tabla de correspondencia parámetro-del-ecosistema / declaración-del-actor | parámetro | no aplica (conteo) | cada ciclo |

**Sobre la definición de «instrumento»** — decisión de este documento y no del canon `[HIPÓTESIS]`:
instrumento es **todo protocolo de medición declarado con identificador**, e incluye sensores
automáticos, muestreos de laboratorio, teledetección **y protocolos de observación humana
protocolizada** (ciencia ciudadana, comunidad testigo). La razón es del propio estándar de valoración
del proyecto: el EVV-1.2 §3.1 acepta *"sensores, logs, trazabilidad biológica **o consenso comunitario
directo**"* `[VERIFICADO]`. Si «instrumento» se restringiera a hardware, el mecanismo castigaría
precisamente a las comunidades sin presupuesto de sensores, que son las que más custodian. Lo que G1
prohíbe no es la observación humana: es la cifra **sin protocolo**.

**Y una frontera que este documento no cruza, para no atribuirse lo ajeno.** El **test del ciclo** del
[documento 18](./18_Ecosistemas_Agroecosistemas.md) §11.3 audita **al sujeto** —si el ciclo de cosecha
respeta el proceso físico— y el CNC audita **al registro**. Los dos tests son complementarios y **ninguno
sustituye al otro**: un registro con `CNC = 0` puede describir un agroecosistema con el ciclo roto, y un
ciclo respetado puede estar contado con un libro mayor sin linaje. Este documento **no absorbe** el test
del 18 en el CNC: lo cita como validación cruzada.

### 6.2 Quién reporta

1. **La comunidad de custodia** (segundo de los 7 campos de identidad de la parte `eco-`,
   [documento 05](./05_Representacion_guardian_y_mandato.md); Cap. 10). Es quien declara `i`, `u_i`,
   `σ_i`, `π` y la tabla de correspondencia de G6.
2. **El guardián oráculo**: **consiente, no certifica**. La fórmula del canon es literal —
   *"Ecosistemas (eco-*): consentimiento otorgado por el guardián oráculo"* (`app/contracts_bp.py`)
   `[VERIFICADO]`— y la distinción es operativa: **consentir** es un acto de representación;
   **certificar** sería un acto de autoridad epistémica, y el guardián no es un instrumento. Si el
   único respaldo de un valor es su firma, el parámetro se marca `sin_evidencia` y el estado es
   `indeterminado` ([documento 06](./06_Medicion_y_verificacion_T13.md) §7.5; [documento
   08](./08_INV2-E_invariante.md) §6.1).
3. **La comunidad testigo**: ejecuta G3 y G4. Su función aquí es específica y no decorativa: perturbar
   el precio y el periodo, y comprobar que el registro no se mueve. Es una prueba que **cualquiera**
   puede repetir, y por eso es auditabilidad T13 y no peritaje.
4. **El auditor no es el beneficiario.** El Reino Natural es el único reino sin par auditor
   ([documento 09](./09_Comparativa_inter_reinos.md) §7): ningún ecosistema audita a otro, y el auditor
   humano suele ser quien se beneficia del uso. De ahí que la comunidad testigo deba incluir, por
   diseño, a un **no beneficiario** — regla que el [documento 18](./18_Ecosistemas_Agroecosistemas.md)
   §11.2 ya propone para el agroecosistema y que aquí se generaliza.

### 6.3 Cuándo

La frecuencia de auditoría **se deriva de `Δt_TA`** (G2), nunca del ciclo contable humano. Registrar
con frecuencia mayor que la que el proceso físico admite es también una forma de colonización: obligar
al ecosistema a hablar en el ritmo del contador. **Ninguna ventana del protocolo se escribe en meses del
calendario**: se escriben en unidades del sujeto, y las dos ventanas que siguen son del sujeto y no del
contador —**10 años** es el horizonte mínimo del marco internacional para observar cambio en cobertura,
productividad y carbono del suelo (UNCCD, 2017) `[VERIFICADO]`; **12 semanas** es la ventana de
acumulación del estrés térmico de arrecifes (NOAA CRW) `[VERIFICADO]`—. Dos sujetos del mismo estándar,
dos relojes incompatibles: **esa es la prueba de que el reloj no puede ser uno solo, y menos el del
contador.**

### 6.4 Lo que este protocolo NO mide (y no debe medir)

- **No mide el estado interior del ecosistema.** No hay campo para «bienestar», «sufrimiento» ni
  «integridad espiritual» de la unidad. Esa frontera es la Zona Libre ([documento
  04](./04_Zona_Libre_del_Reino_Natural.md); Cap. 7 §7.9; Cap. 16.5 §16.5.14).
- **No mide la calidad del registro por su volumen.** Un registro grande y limpio no vale más que uno
  pequeño y limpio; el CNC no tiene proporción (§5.3).
- **No mide la verdad ecológica del umbral.** Mide que el umbral esté **declarado** y que su variable
  de control esté a la vista (CERAC 2024 §2.4).
- **No mide intenciones.** Un registro limpio hecho por quien degrada y un registro limpio hecho por
  quien cuida son, para este mecanismo, iguales. Lo que distingue es el estado del suelo, y eso lo
  juzga el SDV-E, no el CNC.

---

## 7. Verificación y auditoría (T13, guardián, comunidad testigo)

### 7.1 La auditoría es pública por construcción

El Axioma T13 exige *"metodología explícita y posibilidad de disputa mediante métodos alternativos
verificables"* (Cap. 5) `[VERIFICADO]`. El CNC cumple esa exigencia de un modo poco habitual: **el
método alternativo verificable es la propia auditoría**. Cualquier tercero puede replicar G1 (contar
celdas sin linaje), G3 (perturbar precios) y G4 (cambiar la partición temporal) con los datos
publicados. No hace falta ser ecólogo ni tener acceso al territorio.

### 7.2 Separación de funciones (quién juzga, quién certifica, quién mide)

| Función | Quién | Puede | No puede |
|---|---|---|---|
| Medir el parámetro ecológico | instrumento / protocolo declarado | producir el número con `σ_i` | interpretar el estado interior |
| Consentir | guardián oráculo de la parte `eco-` | otorgar o negar consentimiento | certificar valores; fechar con su reloj (cerrojo 3) |
| Declarar linaje y propósito | comunidad de custodia | declarar `i`, `u_i`, `σ_i`, `π` | declararse a sí misma instrumento |
| Auditar el registro | comunidad testigo (con un no beneficiario) | contar violaciones, perturbar precio y periodo | modificar el registro |
| Sancionar | gobernanza (categoría `critical`) | aplicar la escalera C1-C4 | tocar a la unidad ecológica (P6) |

### 7.3 El test que la comunidad testigo puede ejecutar sin peritaje

```
PRUEBA DE NO COLONIZACIÓN (reproducible por cualquiera)
  entrada:  R  (registro publicado de la unidad eco-u)
  paso 1:   contar las celdas numéricas sin i, u_i, σ_i, π  -> v1
  paso 2:   comparar Δt_muestreo con Δt_TA declarado        -> v2
  paso 3:   perturbar SOLO el vector de precios y recalcular -> v3 (debe ser 0)
  paso 4:   recalcular con dos particiones del mismo intervalo   -> v4 (debe ser 0)
  paso 5:   clasificar los campos del esquema (insumo/observación/producto/coordenada) -> v5
  paso 6:   contar parámetros del ecosistema sin contraparte en el actor -> v6
  salida:   CNC = v1 + v2 + v3 + v4 + v5 + v6   ;  válido si y solo si CNC = 0 ∧ R ≠ ∅ ∧ cobertura declarada
```

Los pasos 3, 4 y 6 son la contribución operativa del documento: **no requieren conocimiento
ecológico**, requieren aritmética y disciplina de publicación.

### 7.4 Retractación: se marca, no se borra

Si `CNC > 0`, el registro **no se corrige silenciosamente**: se marca y se conserva. Esta es la regla
del canon —*"El sistema no expulsa. Reintegra"*, pero **la contabilidad nunca se borra** (T13)— y aquí
tiene una consecuencia precisa: **un `CNC > 0` corregido retroactivamente sin dejar la marca es en sí
mismo una violación de G3** (el veredicto cambió por una operación del contador, no por un cambio del
estado físico). La Capa de Ternura
([maxocontracts/blocks/ternura.py](../../../maxocontracts/blocks/ternura.py)) modula la consecuencia
sobre las personas: **no modula el registro**.

### 7.5 Los tres agujeros de auditoría que este mecanismo no cierra (y hay que decir)

1. **El auditor puede no existir.** Si nadie de la comunidad testigo se presenta, el CNC no se calcula
   y el registro queda en `indeterminado`. El mecanismo no crea auditores; crea el puesto de auditor.
2. **El guardián tiene heurística laxa.** El riesgo R13 del
   [blindaje anti-gamificación](../../architecture/blindaje_anti_gamificacion_equidad.md) sigue
   abierto: sin clave del oráculo externo, el guardián aprueba si los invariantes pasan. Un guardián
   laxo **puede consentir un registro que viola G5**, y G5 es precisamente la guarda contra hablar en
   nombre del ecosistema. Es la vulnerabilidad más grave del conjunto, y es de implementación, no de
   diseño.
3. **El esquema puede cambiar después de la auditoría.** Si el registro añade un campo de estado
   interno *después* de haber sido auditado, el `CNC = 0` caduca. Por eso G5 se audita sobre el
   **esquema** y todo cambio de esquema invalida la auditoría anterior hasta re-auditarse. `[HIPÓTESIS]`
   Esta cláusula de caducidad de esquema es aportación de este documento.

---

## 8. Invariante INV2-E: de estándar a contrato ejecutable

### 8.1 El invariante

> **INV2-E.5 — No colonización del TA.** Para toda unidad ecológica `eco-u`, el registro de
> sostenimiento R debe satisfacer `CNC(R) = 0` **y** R no puede ser vacío ni de cobertura no declarada.
> Si `CNC(R) > 0`, el registro **no es válido como evidencia de coherencia**, con independencia del
> saldo de crédito regenerativo acumulado. La violación de INV2-E.5 no se compensa con `R` negativo:
> el suelo antes que el saldo (Cap. 16.5 §16.5.14).

**Base neutra:** `CNC(R) = 0` es el estado sin violación y no produce recargo alguno — coherente con la
corrección de base neutra del SDV-S (`FS_S = e^v`, no `1,0 + e^v`).

### 8.2 Cómo se relaciona con las propiedades ya especificadas de INV2-E

El [documento 08](./08_INV2-E_invariante.md) §8.3 define doce propiedades. INV2-E.5 no las sustituye:
las usa. Correspondencia explícita:

| Propiedad del documento 08 | Relación con el CNC |
|---|---|
| **P2** Base neutra (`FE(v = 0) = 1,0`) | INV2-E.5 la hereda: `CNC = 0` no recarga nada (§5.2) |
| **P3** Independencia del saldo | INV2-E.5 la **refuerza**: el crédito no compra `CNC = 0` (§9) |
| **P4** Guard por tipo, no por dato | El CNC se aplica solo a unidades ecológicas; un registro humano no se audita con CNC |
| **P5** Sin dato no castiga **y** sin dato no aprueba | Es el fundamento de la cláusula de no vacuidad (§5.4) |
| **P6** El sujeto protegido nunca es el objeto de la consecuencia | Limita la escalera C1-C4 (§5.6) |
| **P8** No colonización del TA (guard de esquema) | P8 audita **tipos** (que ningún campo esté en TVI/TPI); el CNC audita además **actos** (linaje, reloj, precio, periodo, simetría). `[VERIFICADO]` P8 es hoy propiedad **especificada y no implementada** en `maxocontracts/`; el CNC es su complemento por actos, **tampoco implementado** (§12) |
| **P10** Monotonía | No aplica al CNC: no tiene magnitud, no hay monotonía que exigir |
| **P12** La Zona Libre no pondera | Coherente: el CNC no entra en ninguna suma ponderada (§5.1) |

`[HIPÓTESIS]` **El CNC es a P8 lo que la auditoría de actos es a la auditoría de tipos.** P8 impide
que un campo *esté* en la unidad equivocada; el CNC impide que un campo correcto *se haya producido*
por el procedimiento equivocado (sin instrumento, con el reloj del contador, con precio, con
asimetría). Los dos son necesarios; ninguno implica al otro.

### 8.3 Especificación mínima de implementación (propuesta, no código)

`[HIPÓTESIS]` Nombres y contratos propuestos, en el estilo del motor (`maxocontracts/`), para que la
biblioteca sea ejecutable cuando se decida implementarla:

| Pieza | Nombre propuesto | Contrato |
|---|---|---|
| Tipo del asiento | `AsientoInteraccion` | campos `t_TA, eco_u, m, x_antes, x_despues, i, u_i, sigma_i, s, pi, dt_ta`; ninguno opcional salvo `x_antes`/`x_despues` (juntos o ninguno) |
| Resultado | `CNCReport` | `cnc: int`, `violaciones: List[ViolacionGuarda]`, `valido: bool`, `no_vacio: bool`, `cobertura: str` |
| Bloque validador | `NoColonizacionBlock` | `evaluar(registro) -> CNCReport`; **sin** `peso`, **sin** `factor` |
| Integración | `AxiomValidator.validate_invariant_no_colonizacion_ta()` | devuelve `ValidationResult(axiom_code="INV2-E.5")`, en línea con INV1-INV4 |
| Guard de tipo | `applicable` | `True` solo si el participante es unidad ecológica (P4) |

Y la exigencia dura, heredada de P5 y de la cláusula de no vacuidad: **`evaluar([])` no puede devolver
`valido = True`.** Un test debe fijar esa propiedad, porque es la que un implementador descuidado
rompería primero (el repositorio ya tiene un invariante —INV3— donde la lista vacía **sí** es válida
por vacuidad, y la simetría entre ambos es una trampa de lectura).

### 8.4 Los diez casos de prueba (el mecanismo, concretamente)

`[HIPÓTESIS]` Todos son propuestas: **ninguno existe hoy** (véase §12). Van con nombre para que sean
implementables sin reinterpretación. **Son diez y no once:** el conteo se corrigió al auditar este
documento contra su propia tabla; ninguna otra parte del texto debe decir «once».

| # | Test propuesto | Qué hace | Esperado |
|---|---|---|---|
| 1 | `test_cnc_cero_no_penaliza` | registro limpio y no vacío | `FE` intacto; `valido = True` |
| 2 | `test_registro_vacio_no_certifica` | `evaluar([])` | `valido = False`, estado `indeterminado` |
| 3 | `test_celda_sin_instrumento_cuenta_violacion` | quita `i` de una celda | `CNC = 1` (G1) |
| 4 | `test_celda_sin_incertidumbre_cuenta_violacion` | quita `σ_i` | `CNC = 1` (G1) |
| 5 | `test_frecuencia_mayor_que_tiempo_caracteristico_falla` | `Δt_muestreo > Δt_TA` | `CNC ≥ 1` (G2) |
| 6 | `test_dt_ta_sin_fuente_falla` | `Δt_TA` sin cita | `CNC ≥ 1` (G2) |
| 7 | `test_precio_perturbado_no_cambia_veredicto` | duplica y anula el vector de precios | idéntico conjunto de violaciones (G3) |
| 8 | `test_sdv_e_no_coloniza_ta` | recalcula con ventana de 6 y de 12 meses | déficit idéntico (G4) |
| 9 | `test_campo_de_estado_interno_falla` | añade campo «bienestar del humedal» | `CNC ≥ 1` (G5) |
| 10 | `test_registro_no_admite_peso_de_conciencia` | intenta ponderar NC o FS sobre `eco-u` | rechazo (G5 + prueba negativa) |
| 11 | `test_simetria_de_transparencia` | parámetro del río sin contraparte del actor | `CNC ≥ 1` (G6) |

**Prueba negativa del conjunto (obligatoria en la suite):** los diez casos deben pasar **con el mismo
registro base** sin tocar el ecosistema simulado. Si algún caso exige cambiar el estado ecológico para
pasar, el test está midiendo al ecosistema y no al registro: está colonizando.

**Dónde vivirían:** `tests/test_maxocontracts/test_no_colonizacion_ta.py` — 🔴 **no existe**.

---

## 9. El suelo antes que el saldo (no compensación)

**La regla.** El crédito regenerativo acumulado **no compensa** caer bajo el SDV-E, y con mayor razón
**no compra** `CNC = 0`. Un conjunto puede haber plantado diez mil árboles y seguir teniendo un registro
que habla en nombre del humedal: la primera cosa la juzga el SDV-E; la segunda, INV2-E.5. Son dos
preguntas distintas y ninguna paga la otra.

**El contraejemplo verificado, que es externo y no una opinión del proyecto.** El marco internacional
de neutralidad en la degradación de la tierra adopta la lógica del **saldo**: ganancias que compensan
pérdidas, con año base 2000, tres sub-indicadores obligatorios (cobertura terrestre, dinámica de
productividad, reservas de carbono orgánico del suelo) y un horizonte mínimo de 10 años para observar
cambio (UNCCD, 2017) `[VERIFICADO]`. Es una formulación respetable —y es **exactamente** lo que el
canon del proyecto rechaza: *"Un conjunto con crédito regenerativo acumulado pero humedal bajo su
SDV-E no está en coherencia"* (Cap. 16.5 §16.5.14). La diferencia entre ambos marcos no es de grado:
**el LDN hace una condición sobre el saldo; el SDV-E la hace sobre el estado.** El umbral del SDV-E no
puede ser «no hay pérdida neta respecto a 2000»; tiene que ser «no se cae bajo el piso», que es una
afirmación sobre el estado y no sobre la aritmética.

**Los cuatro intentos de compensación y por qué fallan uno por uno.** Los tres primeros traen respaldo
externo verificado; el cuarto es una regla interna, y se marca como tal para no aparentar una fuente que
no existe:

| Intento | Cómo se presenta | Por qué no compensa |
|---|---|---|
| «Restauré en otro lado» | superficie restaurada en otra cuenca o a otra escala | La restauración no licencia la degradación: *"el potencial de restauración no debe ser considerado como una justificación para la degradación adicional de ecosistemas"* (CBD, Meta 2, 2022) `[VERIFICADO]` |
| «Tengo crédito regenerativo» | `r_units` muy negativo en el mismo registro | El crédito vive en R y el veredicto del SDV-E es independiente del saldo (P3; Cap. 16.5 §16.5.14) `[VERIFICADO]` |
| «Pagué por el servicio» | valoración del servicio ecosistémico vía PIU | Los valores de intercambio no incorporan valores de no-uso y las perspectivas de valor no son aditivas (SEEA EA §2.62 y §2.58) `[VERIFICADO]` |
| «El índice global mejoró» | el ISE agregado sube aunque el humedal caiga | La agregación no autoriza la caída local; el veredicto de INV2-E es por unidad (documento 07; documento 09 I7) `[HIPÓTESIS]` de familia: ningún estándar externo verificado en esta rama prohíbe la compensación entre unidades, y el ISE —que sí la practica— es el contraejemplo interno |

**Y la asimetría de la carga de la prueba.** T14 (Cap. 5) es explícito: *"Ante incertidumbre sobre el
impacto en agentes que no pueden consentir… el sistema debe elegir la opción de menor irreversibilidad,
documentando el costo de oportunidad asumido. La carga de la prueba recae sobre quien propone acciones
que afectan la temporalidad de no-participantes"* `[VERIFICADO]`. Aplicado a este documento: **quien
quiera declarar un registro como no colonizador carga con la prueba de los once campos de la tupla (§4.0)
y de las seis guardas.** No es el ecosistema quien debe demostrar que fue colonizado.

---

## 10. Zona Libre: lo que NO se mide

**Lo que entra en la Zona Libre de este documento (dimensión binaria, sin peso, Cap. 8 §8.11):**

1. **La vida interna del ecosistema.** No se registra, no se infiere, no se pondera. Es la frontera de
   G5 y la razón de existir de la prueba negativa (§4.8).
2. **El valor inefable.** *"Parte del valor del humedal es inefable (Cap. 7 §7.9). Los sensores miden
   salud (agua, cobertura, biodiversidad indicadora); jamás 'milagros'"* (Cap. 16.5 §16.5.14). No hay
   campo para el milagro, y su ausencia no es una carencia del estándar: es su límite declarado.
3. **La intención y la conciencia del ecosistema.** Si algún día la ciencia establece criterios de
   consciencia ecológica, corresponderá al SDV-A y al Principio Precautorio de Consciencia (Cap. 10
   §10.3) decidirlo — **no a este registro**.
4. **El juicio estético.** *"Jardín podado para la foto no es cuidado; se registra lo que regenera, no
   lo que adorna"* (Cap. 16.5 §16.5.14). El adorno no tiene campo, y un indicador que suba con la poda
   ornamental es una métrica enemiga (documento 06 §7.4).

**Y una regla que se deriva de todo lo anterior, que es el aporte normativo de esta sección:**

> **`CNC = 0` certifica que el registro no se excede; jamás autoriza a medir más.** La ausencia de
> violación de colonización **no es** un permiso para ampliar el elenco de sensores. La Zona Libre no
> se negocia con buenas prácticas de contabilidad: un registro impecable sigue sin acceso al interior
> del ecosistema.

Es la misma lógica que el [documento 04](./04_Zona_Libre_del_Reino_Natural.md) establece para la
dimensión `ZL`, y aquí se refuerza con un caso concreto: **el CNC no puede usarse como argumento de
autoridad para instrumentar más.** Si alguien dice «nuestro CNC es 0, luego podemos medir el bosque
entero», ha entendido el mecanismo al revés: el CNC mide el exceso, no la cobertura.

---

## 11. Comparativa inter-reinos (SDV-H · SDV-A · SDV-E · SDV-S)

| Eje | SDV-H (humanos) | SDV-A (animales) | **SDV-E (ecosistemas)** | SDV-S (sintéticos) |
|---|---|---|---|---|
| Tiempo nativo | TVI | TA | **TA** | TPI |
| Traductor autorizado | — (es su tiempo nativo) | PIU (Cap. 5 §5.5) | **PIU, y solo él** | PIU |
| Qué se coloniza si falla | el tiempo biográfico (vigilancia del tiempo íntimo) | el tiempo del animal (Cap. 9) | **el TA del ecosistema** | el tiempo de cómputo |
| Unidad de duración | meses | según especie (documento 30) | **la que fija el proceso: 12 semanas o 10 años, según sujeto (G2)** | horas TPI |
| ¿Puede producir un peso moral? | sí (es su dominio) | **sí**: NC y FS (EVV-1.2 §4.2) | **no: prohibido** (prueba negativa §4.8) | n/a |
| Representación | la propia persona | la propia persona (animal) | **parte `eco-` + guardián oráculo; el guardián consiente, no certifica** | la propia persona sintética |
| Par auditor | otro humano | comunidad testigo | **ninguno**: el reino natural no tiene par (documento 09 §7) | el par sintético (AOS) |
| Test de no colonización | no existe | **el banco de pruebas natural**: comparte TA y ya tiene SDV (documento 09 §11.3) | **CNC** (este documento) | no existe |
| Base del veredicto | déficit normalizado | SDV + factor de consciencia | **déficit normalizado + compuerta CNC** | `FS_S = e^v` |
| Zona Libre | dimensiones VIII y IX (Cap. 8 §8.11) | tiempo propio no observado | **vida interna, valor inefable, intención, estética (§10)** | opacidad ponderada 0,20 (Cap. 9.5) |

**Las tres lecciones de la comparación:**

1. **El SDV-E es el único reino cuyo tiempo se audita sin haber sido nunca su tiempo.** Un humano audita
   su propio TVI; un sintético, su propio TPI; un ecosistema **no puede auditar su TA** y por eso el
   mecanismo tiene que estar del lado del contador, no del sujeto.
2. **El test debería probarse primero en el SDV-A** (propuesta del [documento
   09](./09_Comparativa_inter_reinos.md) §11.3): los animales comparten el TA del ecosistema y ya
   tienen estándar y motor. Un test de no colonización temporal que funcione sobre una gallina y sobre
   un río es un test de la **relación**, no del sujeto. Se acepta la propuesta y se deja anotada como
   vía de validación cruzada.
3. **El SDV-E es el único reino cuya transparencia puede volverse vigilancia** (G6). Al ecosistema no
   se le puede pedir consentimiento informado; se le puede, sin embargo, pedir silencio.

---

## 12. Estado de implementación

Auditoría de solo lectura sobre el repositorio, octubre 2026. **Lo que existe se dice; lo que no existe
se marca en rojo, y está prohibido afirmar que existe.** Este documento es *estándar primero*; la
contabilidad viene después (Cap. 16.5 §16.5.14).

### 12.1 Lo que SÍ existe (y es honesto decir que existe)

| Pieza | Dónde | Estado |
|---|---|---|
| `r_units` negativo como crédito regenerativo | `app/micromax.py` (`log_cdd`), `app/micromax_bp.py` | 🟢 registrado y devuelto en el vector `[T, V, R]` |
| V no admite negativos; R sí | `app/micromax.py` (`if v_ucv < 0: raise`) | 🟢 invariante de diseño real |
| Parte `eco-` (Ecosistema) | `app/parties.py` (`PARTY_TYPES`, `COLLECTIVE_PREFIXES`) | 🟢 creada y usable |
| Guardián oráculo del ecosistema | `app/contracts_bp.py` (`_guardian_approve_ecosystem`) | 🟡 funciona en la firma de contratos; heurística laxa (R13) |
| Déficit normalizado y severidad | `maxocontracts/blocks/sdv_validator.py` (`relative = deficit / required`) | 🟢 es la base que INV2-E debería heredar |
| Auditoría estructural de esta biblioteca | `tests/test_sdv_e_biblioteca.py` (plantilla, frases vetadas, anclas, mínimo de URLs) | 🟢 |
| Verificación de enlaces vivos de la biblioteca | `scripts/verificar_enlaces_sdv_e.py` | 🟢 |

### 12.2 Lo que NO existe (🔴), con la comprobación hecha

| Pieza | Estado | Comprobación de esta sesión |
|---|---|---|
| **CNC** (contador, guardas, umbral) | 🔴 **no existe** | Este documento es su especificación; no hay código ni test |
| **Test de no colonización del TA** | 🔴 **no existe** | Ninguno de los diez casos de §8.4 está implementado; el documento hermano 12 §7.6 propone además un test de cuatro condiciones sobre el sujeto, que es otra cosa y tampoco existe |
| **PIU** como traductor TA↔TVI | 🔴 **no existe** | `PIU.valorar_ta_natural` es un `pass` con comentario en [DISENO_IMPLEMENTACION_FUTURA.md](../../architecture/DISENO_IMPLEMENTACION_FUTURA.md); no hay clase `PIU` en ningún módulo Python del repositorio |
| **Campo `ta_periodo`** (ventana en TA) | 🔴 **no existe** | Aparece en los catálogos propuestos de los documentos 06 y 08; **cero ocurrencias** en código Python |
| **Linaje instrumental en el registro** | 🔴 **no existe** | El esquema de `micromax_cdd_logs` no tiene columnas de instrumento, unidad, incertidumbre, propósito ni tiempo característico |
| **INV2-E** ejecutable | 🔴 **no existe** | El [documento 08](./08_INV2-E_invariante.md) es propuesta de estándar; sin bloque validador |
| **Validación de reciprocidad en creación** | 🔴 **hueco real** | `AxiomValidator.validate_all` valida T1, T13, INV3, INV1, INV2, INV2-S e INV4; **no** llama a `validate_exchange` (que contiene T2 y T17). Es el riesgo R6 del blindaje |
| **Test de la biblioteca que audite contenido, no forma** | 🟡 | `test_sdv_e_biblioteca.py` audita plantilla, frases vetadas y anclas; **no** puede auditar cifras |

### 12.3 El hallazgo incómodo: hoy el primer asiento no pasaría G1

`[VERIFICADO]` El único asiento hoy ejecutable que toca al Reino Natural es el CDD con `r_units`
negativo. Su esquema real (`micromax_cdd_logs`) guarda: `member_id`, `task_name`, `duration_hours`,
los seis factores de ponderación, `calculated_vhv`, `logged_date`, `v_ucv`, `r_units`, `r_notes`. **No
tiene columna de instrumento, ni de incertidumbre, ni de propósito declarado, ni de tiempo
característico.** Y su marca temporal es `logged_date`: la fecha del calendario del contador.

**Qué se puede y qué no se puede afirmar de esto, con precisión:**

- **No se puede afirmar que ese asiento colonice el TA.** Sería una acusación sin prueba, y este
  documento prohíbe exactamente eso.
- **Se puede afirmar que hoy no hay forma de saberlo** — que es el hueco que el brief nombra. Y por G1,
  un asiento sin linaje **no puede declararse no colonizador**: queda en `indeterminado`, que es el
  estado por defecto del SDV-E ([documento 08](./08_INV2-E_invariante.md) §8.4).
- **Y hay una buena noticia de diseño, verificada**: el componente **T** del vector es
  `duration_hours` —horas-persona humanas— y el efecto sobre el ecosistema vive en **R**. Es decir, el
  registro **ya no almacena el TA del ecosistema como cantidad** (cumple el espíritu de G1 en su
  cláusula de TA-como-coordenada). Lo que falta no es una propiedad del tiempo: es la **trazabilidad
  del dato**.

**Consecuencia operativa, y es un resultado, no un fallo:** el día que se implemente el CNC, **la suite
estará en rojo el primer día**. Un mecanismo de auditoría que nace en verde sobre un registro sin
linaje instrumental no estaría auditando nada.

### 12.4 Lo que haría falta, en orden

1. Añadir al registro los cinco campos de linaje (`i`, `u_i`, `σ_i`, `π`, `Δt_TA`) — migración
   idempotente, en el estilo de `_ensure_column` que el proyecto ya usa.
2. Implementar `NoColonizacionBlock` y sus diez casos de prueba (§8.4).
3. Publicar la tabla de correspondencia de G6 por unidad `eco-`.
4. **Antes que nada**: no declarar ningún registro «no colonizador» mientras los pasos 1-3 no existan.

---

## 13. Preguntas abiertas

Las que este documento **no** resuelve. Se escriben porque un documento que admite «no lo sé» vale más
que uno que aparenta cerrar todo.

1. **El umbral `CNC = 0` no tiene precedente bibliográfico.** `[SIN FUENTE VERIFICADA — pendiente de
   consenso científico]` No existe, en la literatura verificada por esta rama, un umbral publicado para
   «grado de colonización epistémica de un registro contable sobre un sistema natural». `CNC = 0` es una
   **decisión axiomática** (T9 + T13 + T14), no un valor empírico. Si alguien encuentra un precedente,
   este documento debe corregirse.
2. **El cociente `Δt_TA / 2` es una invención del proyecto.** `[SIN FUENTE VERIFICADA]` Ningún estándar
   consultado publica un cociente mínimo entre frecuencia de muestreo y tiempo característico de un
   ecosistema. Es plausible, es análogo a criterios de muestreo conocidos, y **no está respaldado**.
3. **Falta el tiempo característico de casi todos los sujetos.** Se verificaron ventanas para dos casos
   (12 semanas en arrecifes; 10 años en cobertura y productividad de la tierra). Para caudal ecológico,
   conectividad, ciclos de fuego, sucesión, polinizadores y microbiota del suelo **no hay `Δt_TA`
   verificado en esta rama**.
4. **El caudal ecológico se quedó sin fuente *en esta rama*.** `[SIN FUENTE VERIFICADA]` La Declaración
   de Brisbane (2007), fuente ancla del brief, **no tiene URL viva verificada** en esta rama (tres rutas
   probadas, todas 404), y el paper primario del método Tennant (1976) está bloqueado a clientes
   automáticos (403) `[REPORTADO]`. Consecuencia dura y **limitada a este documento**: **este documento no
   cita ningún valor numérico de caudal ecológico**, incluidos los porcentajes clásicos que circulan
   ampliamente. **Corrección de alcance, para no exagerar el vacío:** el [documento
   07](./07_Formula_de_violacion_y_pesos.md) §4 **sí consigna un umbral de caudal** —`< 10 %` del flujo
   promedio original como régimen «pobre o mínimo»— atribuido a Tennant (1976) vía FAO y con la tabla
   completa en `fao.org/4/X6853S/X6853S08.htm`. Es decir: **la ruta FAO que esta rama no abrió sí existe**,
   y la afirmación de §14.2 de que «sus valores numéricos no se usan» es cierta para el 03 y **falsa como
   afirmación general de la biblioteca**. Queda como deuda de verificación del 03, no como vacío de la
   familia: el canon nombra el caudal como dimensión del SDV-E (Cap. 10 §10.4) y el número está pendiente
   de una ronda de verificación propia.
5. **¿Se audita el asiento, el campo o la celda?** Aquí se propone **el asiento** (una fila = un
   asiento). Auditar celdas multiplicaría el mismo error por columna; auditar registros completos
   ocultaría el asiento aislado. `[HIPÓTESIS]` Sin ratificar.
6. **Falta una guarda contra la colonización por definición.** G1-G6 auditan asientos, no
   **definiciones**. Si mañana se cambia el umbral de «bosque» de 10 % a 20 % de cobertura, el sujeto
   cambia de nombre sin que ningún asiento viole nada. `[HIPÓTESIS]` Se propone una posible **G7 —
   inmutabilidad declarada de la definición** (toda definición de sujeto publica su umbral, su fuente y
   su fecha de entrada en vigor, y el cambio de definición no puede mejorar el veredicto). **No se
   ratifica aquí**: es la pregunta abierta más importante que deja este documento. **Y es la razón por la
   que §1 dice «seis guardas que cubren los modos conocidos salvo uno» y no «que los agotan»:** la
   colonización por definición (F3, §1.1) está **declarada y sin guarda** en este documento. Un lector que
   quiera atacar el CNC tiene aquí su punto de entrada, y este texto lo entrega antes de que lo busque.
7. **El ISE no se audita con el CNC, y el brief pedía fusionarlo.** `[HIPÓTESIS]` El Índice de Salud
   Ecosistémica (`docs/architecture/metricas_detalle_kpis_oraculos_dinamicos.md`, IN-01) es la única base
   numérica previa del Reino Natural, y este documento **lo usa una sola vez y como contraejemplo**
   (§9, «el índice global mejoró»). No dice si sus cinco componentes ponderados pueden entrar como
   parámetros de un registro auditado por G1-G6 —donde necesitarían linaje instrumental e incertidumbre
   declarada— ni qué pasa con sus **dos escaleras internas en conflicto** (bandas de estado frente a
   umbrales de alerta), que el documento 09 §11.3 reporta. Queda abierto: **el CNC no dice hoy si el ISE
   es auditable, ni con qué pesos entraría.**
8. **¿Quién audita al auditor cuando el auditor es un oráculo?** El riesgo R13 (guardián laxo) sigue
   abierto, y G5 es la guarda que un guardián laxo puede dejar pasar. Un guardián que no puede certificar
   puede, sin embargo, **consentir** un registro que hable en nombre del ecosistema.
9. **Variables lentas sin «después».** Para el carbono orgánico del suelo, el `x_después` puede no
   existir dentro de la vida de un contrato o de un mandato. ¿Cómo se registra una interacción cuyo
   efecto es más lento que el registro? La única salida verificada que se encontró es la del marco
   internacional: horizonte mínimo de **10 años** (UNCCD, 2017). Queda abierto el caso de contratos
   más cortos que el proceso.
10. **La frontera entre «interacción» y «estado» no está trazada por el canon.** El cerrojo 1 del
    perímetro del PIU (§4.7) propone que el PIU traduzca interacciones y no estados. Es una distinción
    útil y **no ratificada**. ¿Purificar agua es una interacción o un estado del humedal? La respuesta
    honesta: depende de si el registro guarda el **flujo** o el **stock**, y eso exige una decisión por
    parámetro que este documento no toma.
11. **¿Puede la Zona Libre producir algún dato en TVI sin quedar colonizada?** El
    [documento 04](./04_Zona_Libre_del_Reino_Natural.md) §14.5 registra que no. Si eso es correcto,
    entonces el PIU —que traduce a TVI— **no puede tocar la Zona Libre**, y esa restricción no está
    escrita en el canon. Queda abierta.
12. **Tensión entre G6 (simetría) y T14 (precaución).** Si el ecosistema no puede declarar nada y el
    actor no declara nada, G6 se cumple con un registro pobre. La simetría impide la vigilancia, pero
    no garantiza la protección. La salida probable es que el piso de protección lo ponga el SDV-E
    (suelo), no el CNC (procedimiento). **No resuelto.**
13. **Colisión de símbolos pendiente.** «T9» significa dos cosas en el repositorio (libro:
    No-Antropocentrismo Temporal; ingeniería histórica: Reciprocidad Justa, hoy T17) y «TPI» tiene dos
    expansiones distintas (Axioma T7 del Cap. 5 frente al glosario del Cap. 21). Mientras no se
    resuelva, toda cita de T9 en documentos del SDV-E puede leerse mal. Corresponde al canon, no a esta
    biblioteca.

---

## 14. Referencias

### 14.1 Fuentes externas (verificadas en esta sesión: HTTP 200 real)

| Fuente | Qué se usó de ella | URL |
|---|---|---|
| UN Statistical Commission (2021) — *System of Environmental-Economic Accounting—Ecosystem Accounting* (SEEA EA), borrador final | §2.56 valores intrínsecos y antropocéntricos; §2.58 no aditividad; §2.60 foco instrumental; §2.61-§2.62 valores de intercambio; §6.6 alcance parcial | https://unstats.un.org/unsd/statcom/52nd-session/documents/BG-3f-SEEA-EA_Final_draft-E.pdf |
| UN Statistics Division (2025) — *System of National Accounts 2025*, Cap. 35 | remisión del SNA al SEEA como estándar para medir capital natural | https://unstats.un.org/unsd/nationalaccount/snaupdate/2025/2025SNA_CH35_V7_GC.pdf |
| FAO (2020) — *FRA 2020, Terms and Definitions* | definición operativa de bosque (0,5 ha · 5 m · 10 %), otras tierras boscosas (5-10 %), deforestación | https://www.fao.org/3/i8661EN/i8661en.pdf |
| FAO (2020) — *FRA 2020, Key Findings* | 420 millones de ha perdidas 1990-2020; 10 millones de ha/año 2015-2020; 12 millones de ha/año 2010-2015; pérdida neta 4,7 millones de ha/año; 4,06 mil millones de ha (31 %) en 2020 | https://www.fao.org/3/CA8753EN/CA8753EN.pdf |
| CBD (2022) — Marco Kunming-Montreal, Meta 2 | restauración ≥ 30 % para 2030; aviso sobre el potencial de restauración; alta integridad ecológica; pérdida de humedales 87 % (300 años) y 54 % (desde 1900); 20-40 % de tierra degradada | https://www.cbd.int/gbf/targets/2 |
| CBD (2022) — Marco Kunming-Montreal, Meta 3 | conservación y gestión efectiva ≥ 30 % para 2030 | https://www.cbd.int/gbf/targets/3 |
| CBD (2022) — Marco Kunming-Montreal, Meta 7 | reducción ≥ 50 % del exceso de nutrientes y del riesgo de plaguicidas para 2030 | https://www.cbd.int/gbf/targets/7 |
| CERAC (2024) — *Planetary boundaries*, informe completo | §2.4 advertencia sobre variables de control; valores de frontera (bosque 75 %; CO₂ 350 ppm; BII 90 %; extinción < 10 E/MSY; HANPP > 90 %; P y N) | https://www.cerac.be/sites/default/files/media/files/2024-09/planetary_boundaries_full_report-july24.pdf |
| OMS (2021) — *Directrices mundiales de calidad del aire* | PM₂.₅ 5 µg/m³ anual y 15 µg/m³ 24 h; escalera de objetivos intermedios IT-1 a IT-4; enmarcado en salud humana y de los ecosistemas | https://www.europarl.europa.eu/meetdocs/2014_2019/plmrep/COMMITTEES/ENVI/DV/2021/11-29/211129_AQG_WHO_ECEH_EN.pdf |
| NOAA Coral Reef Watch (s.f.) — producto DHW | umbral de blanqueamiento 1 °C; 4 degree C-weeks significativo; 8 severo con mortalidad; acumulación sobre las últimas 12 semanas | https://coralreefwatch.noaa.gov/product/50km/tutorial/crw24_dhw_product.php |
| IUCN (2001) — *Categorías y Criterios de la Lista Roja v3.1* | criterio A (30 / 50 / 80 % en 10 años o 3 generaciones); EOO y AOO; individuos maduros | https://portals.iucn.org/library/sites/library/files/documents/RL-2001-001.pdf |
| IUCN (2001) — ficha de la publicación de Categorías y Criterios v3.1 | adopción por el Consejo de IUCN, febrero de 2001 | https://iucn.org/resources/publication/iucn-red-list-categories-and-criteria-version-31 |
| UNCCD (2017) — *Nota metodológica sobre la neutralidad en la degradación de la tierra (LDN)* | tres sub-indicadores obligatorios; año base 2000; horizonte mínimo de 10 años; ventana LPD 1999-2013; base NPP de 3 a 5 años; lógica de neutralidad (ganancias compensan pérdidas) | https://www.unccd.int/sites/default/files/2018-08/LDN%20Methodological%20Note_02-06-2017%20ENG.pdf |
| UNCCD (2017) — Decisión ICCD/COP(13)/CST/2 | mandato de la COP al secretariado para desarrollar el marco de los tres indicadores | https://www.unccd.int/sites/default/files/sessions/documents/2017-07/ICCD_COP%2813%29_CST_2-1710707E.pdf |
| ZSL & WWF (s.f.) — *Living Planet Index*, resultados | existencia del índice y su adopción por el CBD como indicador del GBF. **No se extrajo ningún valor numérico** | https://www.livingplanetindex.org/latest_results |
| IUCN (2024) — *Tipología Global de Ecosistemas* (portal de biblioteca) | marco taxonómico de referencia para delimitar la unidad (remite al documento 02) | https://portals.iucn.org/library/sites/library/files/documents/2024-021-En.pdf |

### 14.2 Fuentes leídas y descartadas (y por qué)

- **Declaración de Brisbane (2007) sobre caudales ecológicos** — fuente ancla del brief para caudal
  ecológico: **sin URL viva verificada** en esta rama (tres rutas probadas, todas 404). **No se cita.**
- **Método Tennant (1976)** — `[REPORTADO]`: existe, con publicación primaria en editorial que responde
  403 a clientes automáticos. **Sus valores numéricos no se usan en este documento** (§13.4). Precisión
  obligada: **otro documento de la misma biblioteca sí los usa** —
  [documento 07](./07_Formula_de_violacion_y_pesos.md) §4 adopta `< 10 %` del flujo promedio original como
  piso de caudal ecológico, vía la tabla de Tennant publicada por la FAO (`fao.org/4/X6853S/X6853S08.htm`).
  La afirmación de este apartado es sobre el 03, no sobre la familia.
- **Convención de Ramsar, criterios 5 y 6** — el sitio responde 403 en dominio raíz y en todos los PDF
  probados. Los criterios numéricos no se consignan. `[SIN URL VERIFICADA]`
- **Alerta metodológica heredada del informe de fuentes de esta rama** `[VERIFICADO]`: hay PDF que
  responden **200 y no contienen lo que su ruta promete** (uno identificado como documento de suelos
  resultó ser un informe sobre fiebre aftosa; otro identificado como fronteras planetarias resultó ser
  un artículo sobre herpesvirus). Y hay una fuente ancla del brief que responde 403 (portal de
  contabilidad de ecosistemas del SEEA), sustituida ventajosamente por el **estándar completo** en
  `unstats.un.org`. Consecuencia de método: **la verificación de estado HTTP no basta; hay que abrir el
  cuerpo del documento.** Este documento solo cita fuentes cuyo contenido fue leído.

### 14.3 Referencias internas al canon (por capítulo y sección, sin anclas de línea)

- **Cap. 5 §5.2-§5.5** — Tres tiempos (TVI, TA, TPI), Axiomas T7, T9, T13 y T14, y el PIU como único
  traductor TA↔TVI: [capitulo_05_arquitectura_260126.md](../../book/edicion_3_dinamica/capitulo_05_arquitectura_260126.md)
- **Cap. 7 §7.5 y §7.9** — separación hecho/valor y Zona Libre: [capitulo_07_vhv_260126.md](../../book/edicion_3_dinamica/capitulo_07_vhv_260126.md)
- **Cap. 8 §8.11** — dimensiones binarias sin peso (precedente de las seis guardas): [capitulo_08_sdv_h_260126.md](../../book/edicion_3_dinamica/capitulo_08_sdv_h_260126.md)
- **Cap. 9.5 §9.5.7-§9.5.11** — `FS_S = e^v`, base neutra (precedente que este documento no repite como error): [capitulo_09_5_sdv_sinteticos_260126.md](../../book/edicion_3_dinamica/capitulo_09_5_sdv_sinteticos_260126.md)
- **Cap. 10 §10.3, §10.4, §10.6, §10.7, §10.8** — Principio Precautorio de Consciencia; SDV para
  ecosistemas y lugares; dignidad encadenada; gobernanza operacionalmente finita; Persona Sintética: [capitulo_10_tres_reinos_260126.md](../../book/edicion_3_dinamica/capitulo_10_tres_reinos_260126.md)
- **Cap. 16.5 §16.5.14** — el hogar extendido: *"la contabilidad doméstica no coloniza el tiempo
  ajeno"*, PIU, registro de la interacción, representación `eco-`, Zona Libre, el suelo antes que el
  saldo, cuidado ≠ extracción estética: [capitulo_16_5_micromaxocracia_canonica_220826.md](../../book/edicion_3_dinamica/capitulo_16_5_micromaxocracia_canonica_220826.md)
- **EVV-1.2 §3.1, §3.2, §3.6, §4.1, §4.2, §4.3, §4.4** — anti-fiat y consenso comunitario como
  evidencia; separación hecho/valor; el mapa y el territorio; T en hora-persona; NC y FS (nivel 0 = 0,0,
  protección en R); R negativo = regeneración: [capitulo_18_EVV_1.2_270126.md](../../book/edicion_3_dinamica/capitulo_18_EVV_1.2_270126.md)
- **Arquitectura temporal** — los tres reinos, el PIU y la valoración del TA natural en TVI ahorrados: [arquitectura_temporal_coherencia_vital.md](../../architecture/arquitectura_temporal_coherencia_vital.md)
- **Índice de Salud Ecosistémica (IN-01)** — pesos 30/20/20/15/15 y bandas ≥ 85 / 70-84 / 50-69 / < 50
  (documentación interna, sin validación externa verificada): [metricas_detalle_kpis_oraculos_dinamicos.md](../../architecture/metricas_detalle_kpis_oraculos_dinamicos.md)
- **Diseño futuro del PIU** — `valorar_ta_natural` como `pass` con comentario: [DISENO_IMPLEMENTACION_FUTURA.md](../../architecture/DISENO_IMPLEMENTACION_FUTURA.md)
- **Riesgos R4 (partes fantasma), R6 (reciprocidad no validada en creación), R13 (guardián `eco`
  laxo)**: [blindaje_anti_gamificacion_equidad.md](../../architecture/blindaje_anti_gamificacion_equidad.md)
- **Colisión de numeración T9/T17**: [mapa_axiomas_ingenieria_puente.md](../../book/edicion_3_dinamica/integraciones_pendientes/mapa_axiomas_ingenieria_puente.md)
- **Parte `eco-` y guardián oráculo (consentimiento)**: `app/contracts_bp.py` · **crédito
  regenerativo**: `app/micromax.py` · **v_ucv sin negativos**: `app/micromax.py` · **déficit
  normalizado**: `maxocontracts/blocks/sdv_validator.py` · **validación axiomática**:
  `maxocontracts/core/axioms.py`

### 14.4 Referencias internas a esta biblioteca

- [02 — La unidad y el sujeto del SDV-E](./02_Unidad_y_sujeto_del_SDV-E.md) — qué es la `eco-u` que este
  registro audita.
- [04 — Zona Libre del Reino Natural](./04_Zona_Libre_del_Reino_Natural.md) — el límite de perímetro
  que este documento no toca.
- [05 — Representación, guardián y mandato](./05_Representacion_guardian_y_mandato.md) — los 7 campos de
  identidad y el quórum `eco-`.
- [06 — Medición y verificación T13](./06_Medicion_y_verificacion_T13.md) — elenco de sensores; §7.4
  aporta la asimetría de transparencia que aquí es G6.
- [07 — Fórmula de violación y pesos](./07_Formula_de_violacion_y_pesos.md) — el déficit normalizado que
  G3 y G4 perturban.
- [08 — INV2-E: de estándar a contrato ejecutable](./08_INV2-E_invariante.md) — las doce propiedades, el
  estado `indeterminado` y P8, del que INV2-E.5 es la ampliación por actos.
- [09 — Comparativa inter-reinos](./09_Comparativa_inter_reinos.md) — el reino sin par auditor y la
  propuesta de probar el test primero en el SDV-A.
- [16 — Ecosistemas de montañas y criosfera](./16_Ecosistemas_Montanas_y_criosfera.md) — §5.3 aporta el
  criterio de invariancia ante el periodo contable (aquí G4).
- [18 — Ecosistemas agroecosistemas](./18_Ecosistemas_Agroecosistemas.md) — §11.3 aporta el test del
  ciclo de cosecha y la exigencia de un no beneficiario en la comunidad testigo.

---

> **Cierre.** Este documento no afirma que la contabilidad del proyecto haya colonizado el Tiempo
> Absoluto del Reino Natural. Afirma algo más útil y más incómodo: **hoy no existe forma de saberlo, y
> a partir de aquí existe una forma de comprobarlo.** El Contador de No Colonización no mide al
> ecosistema; mide a quien lo cuenta. Y su umbral es cero porque no admite grados el acto de hablar en
> nombre de quien no puede responder.
