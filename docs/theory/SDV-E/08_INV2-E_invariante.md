# INV2-E: el invariante ejecutable
## De estándar a contrato: las propiedades formales del piso del Reino Natural — y la regla que impide que el crédito regenerativo acumulado lo compre

**Autoría:** Oráculo Sintético DeepSeek & Max Nelson López Restrepo
**Fecha:** octubre 2026
**Proyecto:** Maxocracia — El gobierno de la verdad, el tiempo y la vida
**Licencia:** Creative Commons BY-SA 4.0
**Estado:** Propuesta de estándar (rama SDV-E, Ola 4) — NO canon hasta ratificación.
**INV2-E NO ESTÁ IMPLEMENTADO**: ninguna pieza de este documento existe en el repositorio
(verificación en §8.0 y §12). Todo el código de §8 es **especificación propuesta**, no código vivo.
**Referencia canónica:** Cap. 10 §10.4 · Cap. 16.5 §16.5.14 · EVV-1.2 §4.3 · Cap. 9.5 (precedente SDV-S)
**Documento:** 08 de la biblioteca `docs/theory/SDV-E/`
**Revisión:** octubre 2026 — documento redactado contra las fuentes verificadas de la rama
(`scratch/sdv_e/fuentes/08_inv2e.md`) y contra la lectura directa del motor (`maxocontracts/`).
No re-verifica umbrales: los **consume** y declara de dónde vienen.

---

## 1. Qué es (y qué no es) este SDV

**Qué es.** Este documento es la **capa ejecutable** del Suelo de Dignidad Vital del Reino Natural.
Los documentos anteriores de esta biblioteca fijan **qué** protege el SDV-E (el estándar); este
documento fija **cómo se vuelve un contrato que se puede ejecutar, bloquear y auditar** — es decir,
especifica **INV2-E**, el invariante que el canon nombró y nunca escribió:

> *"Un conjunto con crédito regenerativo acumulado pero humedal bajo su SDV-E no está en coherencia:
> **INV2-E será su juez**."* — Cap. 16.5 §16.5.14

El orden metodológico lo fija el propio canon: *"estándar primero, contabilidad después"*
(Cap. 16.5 §16.5.14). Este documento está en la bisagra exacta entre las dos cosas: convierte el
estándar en contrato **antes** de que exista la contabilidad ecológica, y por eso su producto
principal no es una fórmula nueva sino **una lista de propiedades formales y un esqueleto de código
con firmas reales** (§8).

**Qué no es.**

- **No es el estándar.** Los umbrales, la unidad del sujeto y la fórmula de violación pertenecen a
  los documentos 01-07 y 10-23 de esta biblioteca. Este documento **no fija un solo umbral nuevo**:
  consume los que ya tienen fuente verificada y declara —con nombre y peso— los que no la tienen.
- **No es el SDV-S.** INV2-E **replica el patrón** de INV2-S (tipo, bloque validador, guard de
  aplicabilidad, ciclos consecutivos, retractación, Capa de Ternura) y **se separa de él en cuatro
  puntos**, cada uno justificado en §8.6 y §8.7. Un invariante copiado sin esas cuatro correcciones
  sería un SDV-S con otro nombre.
- **No es implementación.** 🔴 **No existe `SDV_E` en `maxocontracts/core/types.py`, no existe
  `sdv_e_validator.py`, no existe `validate_invariant_sdv_e`, no existe ni un sensor.** El esqueleto
  de §8 es una propuesta con firmas reales, escrita para que sea implementable sin reinterpretarla.
- **No autoriza a usar el ISE como piso.** El Índice de Salud Ecosistémica es un **tablero**
  (documento 09, insight I7), no un umbral; y hoy tiene **dos escaleras internas que no coinciden**
  (bandas de estado frente a umbrales de alerta, documento 09 §11.3). INV2-E se especifica
  **independiente del ISE** precisamente para no heredar esa inconsistencia (§8.5, P9).

**Marcas de evidencia usadas en todo el texto.** `[VERIFICADO]` = leído por herramienta en la sesión
de verificación de fuentes de esta rama, o leído directamente en el archivo citado. `[REPORTADO]` =
afirmado por una fuente que se cita sin haber podido abrir el documento completo. `[HIPÓTESIS]` =
inferencia razonada del proyecto, no observación. `[SIN FUENTE VERIFICADA — pendiente de consenso
científico]` = se buscó el umbral y no existe fuente verificable. Las cuatro marcas son resultados
legítimos, y en este documento la cuarta aparece muchas veces porque **el catálogo de dimensiones del
SDV-E excede su capacidad de medida actual** —con un dato medible: el peso con piso verificado no
llega a la unidad (documento 09 §11.3).

**Una advertencia de lectura sobre el dinero y el bosque.** Este documento especifica una regla que
suena dura y es literal: **el crédito regenerativo acumulado no compensa caer bajo el SDV-E**
(Cap. 16.5 §16.5.14). No es una regla moral añadida: es la traducción a código de que el tiempo del
ecosistema es TA y *"la economía no puede acelerar esto sin destruir valor"* (Cap. 5 §5.5). Lo que
se puede comprar es la **restauración por encima del piso**; lo que no se puede comprar es el
**derecho a estar por debajo** (§9).

---

## 2. Preámbulo metodológico

El SDV-H lo tiene; el SDV-S lo omitió y el brief de esta biblioteca prohíbe repetir la omisión. En un
documento de invariante el preámbulo no es cortesía: **un invariante mal especificado no falla, hace
fallar a todo lo que lo invoca.** Estas son las reglas con las que se escribió lo que sigue.

**Regla 1 — Separar "especificar" de "ratificar".** Todo lo que aquí se propone va marcado
`[HIPÓTESIS]` o **propuesta no ratificada**. El documento distingue tres cosas que es fácil confundir:
(a) lo que el canon manda (se cita por sección); (b) lo que el código ya hace (se verifica leyendo el
repositorio); (c) lo que este documento propone (se marca). Ninguna de las tres se disfraza de otra.

**Regla 2 — Todo umbral entra con fuente + año; si no la tiene, entra como agujero contable.** No se
rellena un umbral con plausibilidad. Donde el canon nombra una dimensión y la ciencia no publica su
número, el invariante **no inventa el número**: la dimensión entra en el catálogo, **sin peso en la
fórmula de violación**, y produce un estado explícito de `indeterminado` (§8.4). Un peso asignado a
una dimensión que no se puede medir no es cobertura: es **dilución del déficit**.

**Regla 3 — Mínimo Absoluto y Óptimo son dos columnas y dos regímenes jurídicos.** El piso es
**LEY** y no se vota; la plenitud es **POLÍTICA** y sí se vota (precedente del Parlamento Educativo,
INV2-EDU: categoría `critical`, quórum 60 %, consenso 75 %, T13, anti-flip-flop 14 días, `CHECK` en
BD). El error del motor del SDV-H —confundir el Óptimo del agua con el Mínimo Absoluto— no se repite
aquí. En §4 las dos columnas van separadas incluso cuando la segunda está vacía.

**Regla 4 — Se replica el patrón de INV2-S, y cuando no se replica se dice por qué.** El patrón
verificado —tipo en `core/types.py`, bloque en `blocks/`, validador en `core/axioms.py`, ternura como
capa transversal— es el que menos invención requiere y el que la suite ya sabe probar. **Cuatro
desviaciones** se justifican una por una en §8.6 y §8.7 (cobertura declarada, guard por tipo y no por
dato, contador sin valor heredado, y el sujeto protegido que nunca es el objeto de la consecuencia).

**Regla 5 — Todo lo formal debe ser falsable por un test.** Cada propiedad de §8.3 tiene, al menos,
un test nombrado en §8.8. Una propiedad sin test es una intención. En particular, la regla de
no-compensación de §9 no se enuncia como doctrina sino como **propiedad de invariancia comprobable**:
el resultado de la validación no cambia cuando cambia el saldo de crédito.

**Regla 6 — El invariante no se delega al guardián.** El guardián oráculo **consiente, no mide**
(`app/contracts_bp.py`: *"Ecosistemas (eco-*): consentimiento otorgado por el guardián oráculo"*), y
su heurística es declaradamente laxa cuando falta `DEEPSEEK_API_KEY` (riesgo **R13**). Por eso el
piso se calcula **desde mediciones**, nunca desde la aprobación del guardián: un guardián que aprueba
mal no puede fabricar cumplimiento (§7.3).

**Regla 7 — Admisión de la duda.** *"La duda sin evidencia no castiga"* (INV2-EDU) se conserva. Pero
—y esta es la corrección que el SDV-E necesita y que el documento 09 §6 anticipó— **"sin castigo" no
es "aprobación"**: la ausencia de medición no imputa violación al ecosistema y **tampoco le concede
un certificado de cumplimiento**. La ley no se negocia por ausencia de dato. De ahí que este
invariante tenga **tres estados y no dos** (§8.4).

---

## 3. Pilares epistemológicos

1. **T14 — Principio de Precaución Intergeneracional** (Cap. 5). Es el axioma más fuerte disponible
   para el SDV-E y el único que **bloquea sin necesidad de umbral**: *"Ante incertidumbre sobre el
   impacto en agentes que no pueden consentir (ecosistemas, generaciones futuras, posibles
   consciencias sintéticas), el sistema debe elegir la opción de menor irreversibilidad,
   documentando el costo de oportunidad asumido. La carga de la prueba recae sobre quien propone
   acciones que afectan la temporalidad de no-participantes."* Su consecuencia de ingeniería es
   directa: el invariante tiene **dos vías de bloqueo**, la del piso medido y la precautoria (§8.5).
2. **T13 — Transparencia de Cálculo.** *La contabilidad nunca se borra.* Aplicado a este documento:
   toda validación deja registro; el perdón modula la consecuencia y **jamás** el registro; y un
   estado `indeterminado` también se registra (una zona sin monitoreo es un hecho contable, no un
   vacío administrativo).
3. **T16 — Minimizar Daño.** Con la violación en cero el factor vale exactamente 1,0: el uso legítimo
   del territorio no es daño (§8.3, P2).
4. **T9 — No-antropocentrismo.** El invariante protege a un sujeto, no administra un recurso: por eso
   el objeto de la consecuencia nunca es el ecosistema (§8.7).
5. **El Principio Precautorio de Consciencia** (Cap. 10 §10.3): *"Donde hay duda de consciencia, se
   asume consciencia."* Es el fundamento de que el SDV-E no espere a tener certeza perfecta para
   actuar — pero con la corrección de la Regla 7: la duda mueve a **instrumentar y a no autorizar
   lo irreversible**, no a imputar una violación que no se midió.
6. **Dignidad encadenada** (Cap. 10 §10.6): *"Dignidad Humana ←→ Dignidad Ecosistémica ←→ Dignidad
   Material. Cada eslabón depende de los demás."* Consecuencia para INV2-E: cuando el eslabón
   ecosistémico cae, el bloqueo no es un favor al bosque, es la defensa del propio conjunto humano.
7. **La Directiva Mayor (Axioma 0)**: *"resolver nuestras necesidades de la mejor manera para todos
   todos"* —los **tres reinos**: humanos, naturales y sintéticos, presentes y futuros—. INV2-E es la
   pieza del sistema que impide que el reino que **no firma con manos** quede fuera de la contabilidad
   por no poder reclamar.
8. **Gobernanza operacionalmente finita** (Cap. 10 §10.7): *"La gobernanza debe ser operacionalmente
   finita."* El precedente externo exacto es el marco IUCN de riesgo de colapso, que evalúa el riesgo
   con **cinco criterios cerrados (A-E)** en lugar de modelar la cadena trófica completa [VERIFICADO].
   INV2-E adopta esa disciplina: un catálogo finito y auditable, no una simulación del ecosistema.
9. **Custodia, no propiedad**: *"actuar como custodio del patrimonio biológico, no como su
   propietario."* El invariante **no transfiere propiedad** en ninguna dirección: ni el guardián
   adquiere el bosque, ni el bosque adquiere derechos ejecutables sobre humanos sin representación.
10. **Un ecosistema no audita a otro ecosistema** (documento 09, insight I3). La auditoría del
    cumplimiento viene de la ciencia, la teledetección y la comunidad de custodia. El invariante se
    diseña sabiendo que **su auditor no pertenece al reino auditado** y que, por tanto, el
    procedimiento de disputa no es un anexo.

**Corolario de honestidad.** El Cap. 16.5 marca el SDV-E y el INV2-E como 🔴 *"próxima gran
ramificación"*. Este documento **no cambia ese color**: especifica lo que falta y lo deja 🔴 en §12.

---

## 4. Dimensiones del SDV-E

Este documento necesita la lista **como contrato**, no como doctrina: qué campos existen, con qué
operador, con qué fuente y —sobre todo— **cuáles pueden generar una violación y cuáles no**. Las ocho
dimensiones canónicas del Cap. 10 §10.4 se mapean una por una; la salud del suelo entra desde el ISE
aunque el canon no la nombre; y cada fila declara su estado ejecutable.

### 4.1 Catálogo ejecutable: las dimensiones con piso

**Mínimo Absoluto (LEY, no votable)** frente a **Óptimo (POLÍTICA, votable)**, en columnas separadas.
La columna del Óptimo está casi vacía, y eso no es un descuido: **la ciencia publica pisos de riesgo,
no plenitudes**. La única cifra aspiracional con fuente en esta sesión es **política**, no científica
(Marco Kunming-Montreal), lo cual refuerza la separación de regímenes en lugar de debilitarla.

**Marcas de evidencia de esta tabla, columna por columna.** Los valores de la **OMS (2021)** van
`[REPORTADO]`: se transcribieron de una tabla reproducida en un artículo indexado, porque el PDF
original se sirve como cáscara de JavaScript (755 bytes). Los valores de la **FAO (1985)** y los
**criterios A-E del RLE (IUCN, 2024)** se leyeron en los documentos citados → `[VERIFICADO]`. Los
niveles de estrés térmico de arrecifes llegan por una presentación oficial de **NOAA/NESDIS
publicada por ICRI** → `[REPORTADO]`. Todo lo que dice `[SIN FUENTE VERIFICADA]` es exactamente eso:
se buscó y no hay fuente utilizable en esta rama.

**Trazabilidad de las fuentes de esta tabla** — cada cifra numérica del catálogo tiene organismo,
año y URL, según manda el brief. Las URLs se repiten una sola vez aquí y no en cada fila (el
estado HTTP registrado está en §14):

| Fuente que sostiene las cifras de §4.1 | URL |
|---|---|
| OMS, 2021 — *WHO global air quality guidelines* (cifras de aire, `[REPORTADO]`) | https://www.who.int/publications/i/item/9789240034228 · tabla reproducida: https://www.nature.com/articles/s41598-025-27510-y/tables/1 |
| FAO, 1985 — Ayers & Westcot, *Water quality for agriculture*, Papel 29 Rev.1 (pH, NO₃-N, HCO₃) | https://www.fao.org/3/t0234e/T0234E01.htm · https://www.fao.org/3/t0234e/T0234E06.htm |
| IUCN, 2024 — RLE v2.0, criterios A–E, categorías, colapso y regla NT | https://portals.iucn.org/library/sites/library/files/documents/2024-021-En.pdf |
| NOAA/NESDIS, 2024 — escala DHW, publicada por ICRI (`[REPORTADO]`) | https://icriforum.org/wp-content/uploads/2024/05/1.-ICRI_Manzello_14May2024_Final.pdf |
| CBD, 2022 — Marco Kunming-Montreal, decisión 15/4 (cifras del Óptimo político) | https://www.cbd.int/doc/decisions/cop-15/cop-15-dec-04-en.pdf · https://www.cbd.int/gbf/targets |

**El recuento del catálogo, explícito** (para que no se lea de dos maneras a la vez): **18 parámetros
con umbral** —9 de aire, 3 de agua, 5 de biodiversidad y `arrecife_dhw`—, de los cuales **17 tienen
peso** en `PESOS_PISO`; `arrecife_dhw` tiene piso (4 °C-semanas) pero **solo aplica si el tipo de
unidad es arrecife** (§8.3, P4).

| Dimensión canónica (Cap. 10 §10.4) | Parámetro del tipo `SDV_E` | Operador | Unidad | **Mínimo Absoluto (LEY)** | **Óptimo (POLÍTICA)** | Fuente | Ejecutable hoy |
|---|---|---|---|---|---|---|---|
| Calidad del aire | `aire_pm25_anual` | `max` | µg/m³ anual | **5** | `[SIN FUENTE VERIFICADA]` | OMS, 2021 (valor `[REPORTADO]`; URL en el bloque de trazabilidad, 200) | 🟢 (proxy declarado) |
| Calidad del aire | `aire_pm25_24h` | `max` | µg/m³ 24 h | **15** | `[SIN FUENTE VERIFICADA]` | OMS, 2021 (`[REPORTADO]`, tabla reproducida) | 🟢 |
| Calidad del aire | `aire_pm10_anual` · `aire_pm10_24h` | `max` | µg/m³ | **15** · **45** | `[SIN FUENTE VERIFICADA]` | OMS, 2021 (`[REPORTADO]`) | 🟢 |
| Calidad del aire | `aire_no2_anual` · `aire_no2_24h` | `max` | µg/m³ | **10** · **25** | `[SIN FUENTE VERIFICADA]` | OMS, 2021 (`[REPORTADO]`) | 🟢 |
| Calidad del aire | `aire_o3_8h` · `aire_so2_24h` | `max` | µg/m³ | **100** · **40** | `[SIN FUENTE VERIFICADA]` | OMS, 2021 (`[REPORTADO]`) | 🟢 |
| Calidad del aire | `aire_co_24h` | `max` | **mg/m³** (no µg/m³) | **4** | `[SIN FUENTE VERIFICADA]` | OMS, 2021 (`[REPORTADO]`) | 🟢 |
| Calidad del agua (A y B) | `agua_ph` | `range` | unidades de pH | **6,5 – 8,4** | `[SIN FUENTE VERIFICADA]` | FAO, 1985 (Ayers & Westcot, Papel 29 Rev.1) | 🟢 (proxy: agua de **riego**) |
| Calidad del agua (A y B) | `agua_nitrato_n` | `max` | mg/L (NO₃-N) | **< 5** (sin efecto restrictivo) | `[SIN FUENTE VERIFICADA]` | FAO, 1985 (tabla 1) | 🟢 (proxy: agua de **riego**) |
| Calidad del agua (A y B) | `agua_bicarbonato_me` | `max` | me/L (HCO₃, aspersión) | **< 1,5** | `[SIN FUENTE VERIFICADA]` | FAO, 1985 (tabla 1) | 🟢 (proxy: agua de **riego**) |
| Calidad del agua (B) | `agua_oxigeno_disuelto` | `max`/`min` | mg/L | `[SIN FUENTE VERIFICADA]` | `[SIN FUENTE VERIFICADA]` | la ruta de la EPA para este criterio está **muerta (404)** | 🔴 **sin umbral** |
| Área mínima viable · Fauna acuática · Biodiversidad | `rle_reduccion_distribucion_50a` | `max` | % de reducción | **< 30 %** | `[SIN FUENTE VERIFICADA]` | IUCN, 2024 — RLE v2.0 (Criterio A) | 🟢 (proxy: **riesgo de colapso**, no área mínima) |
| Ídem | `rle_reduccion_historica_1750` | `max` | % de reducción | **< 50 %** | `[SIN FUENTE VERIFICADA]` | IUCN, 2024 (Criterio A3) | 🟢 |
| Ídem | `rle_eoo_km2` | `min` | km² (EOO) | **> 50 000** | `[SIN FUENTE VERIFICADA]` | IUCN, 2024 (Criterio B1) | 🟢 |
| Ídem | `rle_degradacion_c1_pct` | `max` | % extensión afectada | **< 30 %** | `[SIN FUENTE VERIFICADA]` | IUCN, 2024 (Criterio C1) | 🟢 |
| Ídem | `rle_probabilidad_colapso` | `max` | % en 100 años | **< 10 %** | `[SIN FUENTE VERIFICADA]` | IUCN, 2024 (Criterio E) | 🟢 |
| Ídem (escala agregada) | `rle_categoria` | `ordinal` | 8 categorías | **mejor que VU** (VU/EN/CR/CO = amenazado) | `[SIN FUENTE VERIFICADA]` | IUCN, 2024 | 🟡 **binaria, sin peso** |
| *(No canónica; del ISE)* Salud del suelo | `suelo_carbono_organico` | — | t C/ha | `[SIN FUENTE VERIFICADA]` | `[SIN FUENTE VERIFICADA]` | FAO: publica **mapas** (GSOCmap), no umbrales | 🔴 **sin umbral** |
| Caudal mínimo ecológico | `caudal_ecologico_pct_qma` | `min` | % del caudal medio anual | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` | `[SIN FUENTE VERIFICADA]` | Brisbane, 2018 da **definición**, no porcentaje | 🔴 **sin umbral** |
| Conectividad | `conectividad_indice` | — | — | `[SIN FUENTE VERIFICADA]` | `[SIN FUENTE VERIFICADA]` | ninguna institución verificada publica umbral | 🔴 **sin umbral** |
| Ciclos naturales (fuego, inundación, sequía) | `ciclos_naturales_estado` | `binary` | presencia/ausencia de régimen | **régimen presente** | `[SIN FUENTE VERIFICADA]` | canon sí, cifra no | 🟡 **binaria, sin peso** |
| Riberas protegidas | `riberas_protegidas_estado` | `binary` | presencia/ausencia de franja | **franja presente** | `[SIN FUENTE VERIFICADA]` | canon sí, cifra no | 🟡 **binaria, sin peso** |
| Arrecifes (si el tipo de unidad es arrecife) | `arrecife_dhw` | `escalonado` | °C-semanas | **< 4** (sin alerta) | `[SIN FUENTE VERIFICADA]` | NOAA/NESDIS, 2024 (vía ICRI) `[REPORTADO]` | 🟢 (su peso se toma del grupo de riesgo: no altera la suma) |

**El Óptimo, con fuente, es político.** Los únicos números aspiracionales con fuente verificada en
esta rama son los del Marco Kunming-Montreal: **≥ 30 % de restauración efectiva de ecosistemas
degradados para 2030** (Meta 2), **≥ 30 % conservado y gestionado eficazmente para 2030** (Meta 3),
**≥ 50 % de reducción de la tasa de introducción de invasoras** (Meta 6), **≥ 50 % de reducción del
exceso de nutrientes y del riesgo de pesticidas** (Meta 7), **≥ 500 000 millones USD/año** de
incentivos nocivos reducidos (Meta 18) y **≥ 200 000 millones USD/año** movilizados, de los cuales
≥ 30 000 millones internacionales (Meta 19) [VERIFICADO]. Son **anclas de política a escala global**,
no umbrales de una unidad ecológica concreta: usarlas como "óptimo de este humedal" sería abuso de la
fuente. Se citan aquí porque son la prueba de la tesis: **la plenitud del SDV-E la fija la
deliberación, no la ciencia** — y por eso es exactamente la columna que se vota.

**Lo que este catálogo NO autoriza a concluir.** Tres advertencias que se heredan del documento 09
§11.3 y que aquí se repiten porque el código las va a hacer cumplir:

1. **El aire de la OMS es un proxy de salud humana**, no un umbral de integridad ecosistémica. Entra
   como piso compartido conservador y **declarado como proxy**.
2. **El agua de la FAO es calidad de agua de riego**, no integridad ecológica del cuerpo de agua.
   Entra como proxy declarado; el oxígeno disuelto —el parámetro que sí sería ecológico— **quedó sin
   fuente** porque la ruta específica de la EPA devuelve 404.
3. **Los criterios A-E del RLE miden riesgo de colapso, no "área mínima para biodiversidad viable".**
   El criterio B1 (EOO > 50 000 km²) es **el umbral por encima del cual el criterio no aplica**, no un
   tamaño mínimo de parche viable. Fundir ambos sería el mismo abuso que usar los > 20 m de ancho de
   la definición de bosque de la FAO como "protección de ribera" (documento 09 §11.3).

### 4.2 Las dimensiones que entran sin poder generar violación

La consecuencia operativa del catálogo anterior, y la decisión más incómoda de este documento:
**seis dominios del estándar no pueden activar INV2-E hoy**, porque no tienen umbral con fuente ni
definición operativa de violación. El documento 09 §6 fijó el principio —*sin definición operativa de
violación no hay violación*— y aquí se convierte en una regla del tipo:

| Dominio sin umbral | Qué hace el invariante con él | Qué NO hace |
|---|---|---|
| Oxígeno disuelto | Lo registra; sin dato o con dato, **no calcula déficit** | No lo pondera (un peso sin piso **diluye** el déficit, no lo mide) |
| Salud del suelo | Lo registra y lo reporta al tablero (ISE) | No lo pondera en `violation_magnitude` |
| Caudal ecológico | Lo registra; y **T14 puede bloquear** una acción irreversible que lo afecte | No imputa violación por ausencia de cifra |
| Conectividad | Ídem | Ídem |
| Ciclos naturales, riberas | Entran como **dimensión binaria auditable sin peso** (precedente Cap. 8 §8.11) | No se cuantifican ni se canjean |

(La última fila cubre **dos** dominios del estándar —ciclos naturales y riberas—; con ella la tabla
declara **seis**: oxígeno disuelto, suelo, caudal, conectividad, ciclos y riberas.)

**Por qué no se les asigna peso (y por qué esto es una desviación deliberada del precedente).** En
INV2-S los pesos suman 1,0 y todas las dimensiones son medibles en escala 0-1 [VERIFICADO]. En el
SDV-E eso no se puede replicar: si se asigna peso a una dimensión sin piso, su déficit es siempre
cero y el cociente final **subestima** la violación real. Por eso el tipo separa dos vectores de
pesos (§5.2) y declara explícitamente qué fracción del estándar es ejecutable hoy. **La fracción no
ejecutable no se renormaliza en silencio: se publica.**

---

## 5. Fórmula de violación, pesos y umbrales

La fórmula del SDV-E pertenece al documento 07 de esta biblioteca. Este documento **no la fija**:
fija las **condiciones que INV2-E le exige** para poder ejecutarla. Es la diferencia entre escribir
la ley y escribir el motor que la aplica.

### 5.1 El déficit, normalizado y con operador

La versión normalizada es la coherente con el motor (brief §3.3.9): `déficit = (requerido − actual) /
requerido`, tal como hace `maxocontracts/blocks/sdv_validator.py` con `relative = deficit / required`
y su clasificación de severidad (≤ 10 % leve · ≤ 30 % moderada · > 30 % severa) [VERIFICADO]. La
versión sin normalizar del paper del SDV-H es la antigua y **no se adopta**.

Lo que este documento **añade** es que el SDV-E no tiene un solo signo de comparación, sino cuatro
**tipos de parámetro** —y sin esa distinción el motor compararía un pH con un EOO:

| Operador | Significado | Fórmula del déficit normalizado | Parámetros del catálogo |
|---|---|---|---|
| `min` | **menos es mejor** (el piso es un mínimo que se exige superar) | `(req − actual) / req` | EOO (km²) |
| `max` | **más es mejor** (el piso es un techo que no se debe superar) | `(actual − req) / req` | PM2.5, PM10, NO₂, O₃, SO₂, CO, NO₃-N, HCO₃, reducción de distribución, degradación C1, probabilidad de colapso |
| `range` | hay un rango admisible | `(lo − actual) / lo` si `actual < lo`; `(actual − hi) / hi` si `actual > hi`; `0` en otro caso | pH |
| `escalonado` | tabla de niveles con consecuencia creciente | toma el nivel alcanzado; **no interpola** | DHW de arrecifes |
| `ordinal` / `binary` | presencia/ausencia o categoría | **no produce déficit**: produce estado | categoría RLE; ciclos naturales; riberas; Zona Libre |

El operador `max` con déficit normalizado es exactamente el patrón `is_max_constraint=True` que el
motor ya usa para las restricciones de máximo del SDV-H [VERIFICADO]: no se inventa una convención
nueva, se generaliza una existente.

### 5.2 Los pesos: dos vectores, ninguno oculto

| Grupo | Peso declarado | ¿Tiene piso? | De dónde viene |
|---|---|---|---|
| Calidad del aire (9 parámetros OMS) | **0,20** | 🟢 sí (proxy) | pesos internos del ISE (aire 20 %) + canon §10.4 |
| Calidad del agua (pH, NO₃-N, HCO₃) | **0,18** | 🟢 sí (proxy de riego) | pesos internos del ISE (agua 20 %) + canon §10.4 |
| Calidad del agua (oxígeno disuelto) | **0,02** | 🔴 no | canon §10.4, sin fuente |
| Biodiversidad · riesgo de colapso (5 criterios RLE) | **0,30** | 🟢 sí (proxy) | pesos internos del ISE (biodiversidad 30 %) + canon §10.4 (área viable, fauna acuática) |
| Salud del suelo | **0,15** | 🔴 no | pesos internos del ISE (suelo 15 %); el canon no la nombra |
| Caudal ecológico | **0,075** | 🔴 no | canon §10.4 (lugar); **ausente del ISE** |
| Conectividad | **0,075** | 🔴 no | canon §10.4 (ecosistema); **ausente del ISE** |
| **Suma** | **1,000** | — | **`PESOS_TABLERO`** |
| **Suma de los que tienen piso** | **0,680** | — | **`PESOS_PISO`** |
| **Fracción declarada sin piso** | **0,320** | — | el agujero, medido y publicado |

**De dónde sale cada número de esta tabla (y de dónde no).** Los cinco pesos del ISE son un índice
**interno del proyecto**, no un estándar externo: `docs/architecture/metricas_detalle_kpis_oraculos_dinamicos.md`
da biodiversidad 30 %, agua 20 %, aire 20 %, suelo 15 % y poblaciones de especies clave 15 %, y el
propio informe de fuentes de esta rama advierte que *"el ISE no es un umbral con fuente externa"*.
Las filas de caudal (0,075) y conectividad (0,075) **no vienen del ISE** —que no las incluye— sino de
una fusión de este documento; el reparto del 20 % del agua y del 15 % de suelo entre parámetros
concretos también es de este documento. **La suma 0,680 es, por tanto, una construcción de los
autores sobre pesos internos**: cifra aritméticamente exacta y verificable en el motor cuando se
implemente, pero no un dato con fuente externa. Se publica precisamente por eso.

**Dos reglas que hacen que esta tabla sea ejecutable sin ambigüedad.**

1. **El piso y el peso son independientes.** Un parámetro **con umbral** produce `violacion` aunque su
   peso sea cero (P1, atomicidad); el peso solo dimensiona `v` y `FE`. Es lo que permite que
   `arrecife_dhw` —que tiene piso (< 4 °C-semanas) pero no peso propio en el vector base— **bloquee
   igual** en una unidad de arrecife, tomando su peso del grupo de riesgo (0,30) sin alterar la suma
   declarada.
2. **Ningún tipo de unidad puede cambiar la suma declarada.** Si un tipo de unidad activa parámetros
   adicionales (arrecifes), la suma de `PESOS_PISO` sigue siendo **0,680**: lo que cambia es qué
   parámetros la componen. Fijar el vector por tipo de unidad pertenece al documento 02 (unidad y
   sujeto) y aquí se marca como **decisión no ratificada**.

**Tres propiedades que INV2-E exige de cualquier tabla de pesos** (la definitiva la ratifica el
documento 07):

- **W1 — Los dos vectores existen y son explícitos.** `PESOS_PISO` (suma **0,680**) es el que entra en
  `violation_magnitude`; `PESOS_TABLERO` (suma **1,000**) es el que alimenta el tablero tipo ISE.
  Ninguna dimensión sin piso puede tener peso en `PESOS_PISO`, y ello se comprueba por código.
- **W2 — La brecha se publica.** `cobertura_piso_declarada = Σ(PESOS_PISO) = 0,680` es un campo del
  estándar, auditable. Hoy el SDV-E puede ejecutar su piso sobre esos **0,680 puntos de peso** —el
  **68 % del peso total que declara querer proteger** en `PESOS_TABLERO`—; el 0,320 restante son suelo
  (0,15), caudal (0,075), conectividad (0,075) y oxígeno disuelto (0,02). Es una cifra construida
  sobre pesos internos del proyecto (§ arriba) y la que debería doler.
  **Precisión aritmética obligatoria:** `cobertura_piso_declarada` es un **denominador fijo (0,680)**,
  no una medición. La cobertura *medida* sobre una unidad concreta es
  `cobertura_medida = Σ(pesos de los parámetros con piso efectivamente medidos) / 0,680` (§8.3, P11):
  con **un solo** parámetro sin medir baja a ≈ 0,91 (si el que falta es `aire_pm25_anual`, peso 0,06),
  y ningún valor de `cobertura_medida` puede leerse como "porcentaje del estándar protegido". La
  cifra del 68 % es del **catálogo**; la de la unidad la produce la medición.
- **W3 — Los pesos de la fusión son `[HIPÓTESIS]`.** La tabla anterior es la fusión que este documento
  propone entre las dos listas del canon y los cinco componentes del ISE (documento 09 §11.3). Está
  marcada como **propuesta no ratificada**; el ISE **no es un umbral con fuente externa** y sus pesos
  son internos, de modo que presentarlos como "piso verificado" sería el error que el informe de
  fuentes de esta rama advierte explícitamente.

### 5.3 El factor `FE` y la base neutra

INV2-E **consume** `FE`, no lo define (documento 07). Le exige tres cosas, y las tres son ejecutables:

1. **Base neutra exacta.** `FE(v = 0) = 1,0`, no `1 + e^v`. El SDV-S tuvo que corregir su versión
   original porque recargaba el 100 % incluso sin violación [VERIFICADO en
   `maxocontracts/core/types.py`, docstring de "Corrección crítica v2"]. El SDV-E pertenece a la
   **familia de los factores de penalización** (documento 09 §5.2) y no hereda el 0,2 del SDV-A.
2. **Parte continua finita.** Un contrato que guarde `inf` en una columna numérica no es ejecutable.
3. **Lo "infinito" es un estado, no un valor.** El `∞` del SDV-A es una *prohibición de mercado*
   (Cap. 9 §9.8) y el `FS_S → ∞` del SDV-S es una *interrupción total del sistema que la provoca*
   (Cap. 9.5 §9.5.10). En INV2-E se implementa como **disparador booleano y estado verificable**
   (`precautionary_block`, `objeto_de_retractacion`), nunca como número.

### 5.4 Escala de interpretación

Se adopta la escala de severidad que el motor **ya usa** para el SDV-H, extendida con el único tramo
que tiene definición externa verificada:

| Severidad | Criterio | Precedente |
|---|---|---|
| `leve` | déficit relativo ≤ 10 % | `sdv_validator.py` (`severity_thresholds`) |
| `moderada` | déficit relativo ≤ 30 % | ídem |
| `severa` | déficit relativo > 30 % | ídem |
| `irreversible` | **colapso**: categoría CO, o área de ocupación = **0 celdas de 10 × 10 km** y extensión de presencia = **0 km²** | IUCN, 2024 — RLE v2.0 (definición espacial del *endpoint*) |

El tramo `irreversible` **no es una severidad más**: cambia las consecuencias disponibles (§8.7) y
desactiva la Capa de Ternura en su forma de rehabilitación (§8.9). Y tiene un precedente de diseño
que el documento 09 ya había detectado: la regla del "Casi Amenazado" del RLE —EOO de 50 000 a
55 000 km², o declive abiótico de 20-30 % de severidad con 100 % de extensión— funciona como **zona de
aviso declarada por norma**, no por contador. INV2-E la incorpora como banda `NT` de aviso previo,
**separada** del contador de ciclos consecutivos (§8.6).

---

## 6. Protocolo de medición (sensores, frecuencias, quién reporta)

El elenco de sensores del SDV-E es del documento 06. Aquí se especifica **el contrato de entrada del
invariante**: qué necesita recibir, con qué sello, y qué es inadmisible. Un invariante que acepta
cualquier número sin procedencia no es un juez; es un decorado.

### 6.1 Admisibilidad de una medición

Una medición entra en una validación de INV2-E **solo si** trae los cuatro campos siguientes. Si
falta alguno, el parámetro se trata como **no medido** (`None`), lo que produce `indeterminado` y no
violación:

| Campo | Para qué | Axioma |
|---|---|---|
| `valor` + `unidad` | el número y su unidad física, sin conversiones implícitas | — |
| `ta_periodo` (inicio y fin en **Tiempo Absoluto**) | la ventana temporal de la medición; sin ventana, el dato no es comparable | T7 (Cap. 5) |
| `fuente_dato` (organismo, red de sensores, teledetección, comunidad de custodia) | procedencia verificable | T13 |
| `evidencia_ref` (identificador del registro original) | trazabilidad; es lo que impide un número sin origen | T13 |

**Regla dura derivada:** *el guardián oráculo consiente, no mide* (Cap. 16.5 §16.5.14;
`app/contracts_bp.py`). Ninguna validación puede tomar como medición una aprobación del guardián. Si
el único respaldo de un valor es la firma del guardián, el parámetro se marca `sin_evidencia` y el
estado es `indeterminado`.

### 6.2 Frecuencia: el TA manda y la unidad no está decidida

El tiempo del territorio es **TA**, nunca TVI ni TPI, y *"el PIU traduce"* (Cap. 16.5 §16.5.14).
Consecuencia formal: **todo campo del tipo `SDV_E` está denominado en TA o en unidades físicas**
(§8.3, P8). Pero **la unidad del ciclo TA del SDV-E no está decidida y no tiene fuente**: año
hidrológico, año calendario, estación de crecimiento y ciclo de sucesión son candidatos legítimos y
ninguno tiene respaldo verificado (documento 09 §13, pregunta 4). INV2-E lo trata como
**configuración obligatoria y sin valor por defecto** (§8.6): un invariante no puede heredar en
silencio la unidad de otro reino.

| Parámetro | Instrumento candidato | Frecuencia mínima exigible | Quién reporta |
|---|---|---|---|
| Aire (PM2.5, PM10, NO₂, O₃, SO₂, CO) | red de estaciones; teledetección como complemento | la propia de la directriz: **anual** (PM2.5, PM10, NO₂) y **24 h / 8 h** (episodios) | red de monitoreo + comunidad testigo |
| Agua (pH, NO₃-N, HCO₃) | sensores in-situ; muestreo de laboratorio | una vez por ciclo TA, mínimo | laboratorio o comunidad de custodia |
| Biodiversidad y riesgo de colapso (A, B, C, E) | teledetección de cobertura + inventarios + modelización de riesgo | **el marco exige horizontes explícitos**: 50 años (A y E), 100 años (E), desde ~1750 (A3) [VERIFICADO] | ciencia + entidad evaluadora |
| Arrecifes (DHW) | producto satelital de estrés térmico acumulado | semanal en temporada cálida (el producto es satelital) | servicio de observación |
| Suelo, caudal, conectividad, ciclos, riberas, OD | 🔴 **sin elenco verificado** | 🔴 sin frecuencia | 🔴 sin responsable |

**Lo que la tabla dice en su última fila, sin adornos:** el protocolo del SDV-E **no existe** para
**seis dominios** del estándar (oxígeno disuelto, suelo, caudal, conectividad, ciclos naturales y
riberas), que la fila agrupa en una sola línea. Este documento no lo rellena con candidatos
plausibles: lo declara como la condición de posibilidad que falta (documento 09 §6: sin instrumentos,
el SDV-E no es débil, es **inenunciable**).

### 6.3 La bandera de opacidad ecológica (inversión del principio INV2-EDU)

Para los reinos humano y sintético, la ausencia de dato protege al presunto vulnerado. En el Reino
Natural **el presunto vulnerado no reporta**, así que la misma regla protegería al presunto violador
(documento 09, insight I9). La política de INV2-E es la imagen especular de la *Paradoja de los
Modelos Cerrados* del SDV-S (Cap. 9.5 §9.5.9):

> **La ausencia de monitoreo nunca se imputa como violación del ecosistema; sí activa una
> obligación contractual de instrumentar.**

Operativamente: `opacidad_ecologica = True`, `obligacion_de_instrumentar = True`, y el contrato que
invoque la unidad **no puede declararse válido por cumplimiento** mientras la cobertura sea
incompleta. No es una sanción al territorio —el territorio no puede ser sancionado por no tener
sensores—, es una condición de validez para quien quiere operar sobre él. `[HIPÓTESIS]` en su forma
exacta; el principio (que la duda no castiga al sujeto medido) es canon.

---

## 7. Verificación y auditoría (T13, guardián, comunidad testigo)

### 7.1 Qué audita INV2-E y qué no

| Audita | No audita |
|---|---|
| Que una unidad ecológica esté por debajo de un piso **medido** | La vida interna del ecosistema: *"Nosotros registramos la interacción, no la vida interna del ecosistema"* |
| Que la cobertura de medición sea la suficiente para declarar cumplimiento | El valor inefable del humedal (Zona Libre, §10) |
| Que la violación quede registrada y sea reproducible | La bondad del guardián o su autoridad sobre la entidad (riesgos R4 y R13, §7.3) |
| Que el crédito regenerativo no altere el veredicto | El saldo del crédito en sí (§9) |

### 7.2 Trazabilidad (T13)

Cada validación produce un registro con: estado, violaciones por parámetro, `violation_magnitude`,
cobertura medida, dimensiones faltantes, ciclos consecutivos, decisión de bloqueo y
`evidencia_ref` de cada medición. El precedente está implementado: `_validation_log` en
`SDV_SValidatorBlock` y en `SDVValidatorBlock`, con `get_validation_log()` y `to_dict()` para
auditoría [VERIFICADO]. INV2-E replica esa forma y añade dos campos obligatorios por registro:
**cobertura** y **procedencia**.

**La contabilidad nunca se borra.** Ni siquiera cuando la Capa de Ternura concede perdón: la ternura
*"modula la CONSECUENCIA, nunca la contabilidad"* y el perdón es consumible y no infinito
[VERIFICADO en `maxocontracts/blocks/ternura.py`]. Para el ecosistema esto tiene una lectura
adicional y dura: **una violación registrada no se puede des-registrar con un pago posterior**, porque
el daño ocurrió en un TA que no vuelve.

### 7.3 El guardián, la comunidad testigo y los riesgos abiertos

El guardián oráculo **consiente, no mide**; la comunidad de custodia y la ciencia son el sustituto
institucional del **par auditor que el Reino Natural no tiene** (documento 09 §7, insight I3). Tres
riesgos abiertos afectan directamente a la cadena de verificación, y el diseño del invariante los
trata así:

| ID | Riesgo (`docs/architecture/blindaje_anti_gamificacion_equidad.md`) | Cómo lo trata INV2-E |
|---|---|---|
| **R4** | Partes fantasma: cualquier usuario autenticado crea una parte `eco-*` y queda como su dueño | El invariante **no valida autoridad**: no puede, y no finge poder. La validación de autoridad es una precondición externa documentada como 🔴 en §12 |
| **R6** | T9 (Reciprocidad Justa) no se valida en la creación: pasa un contrato unilateral | Este documento **propone** que INV2-E bloquee la acción cuando el piso medido cae, aunque el contrato sea unilateral. **No es una defensa que exista hoy**: es la que falta, y hasta que se implemente el contrato unilateral sigue pasando |
| **R13** | Guardián eco con heurística laxa: sin `DEEPSEEK_API_KEY` aprueba si los invariantes pasan | **El piso no se delega al guardián** (Regla 6): se calcula desde mediciones. Un guardián laxo no puede fabricar cumplimiento: su consentimiento **relaja, no habilita**, y no levanta un bloqueo por piso medido |

**Nota sobre la numeración de T9 en la fila R6** (la ambigüedad es del repositorio, no de este
documento): el registro de riesgos cita *"T9 (Reciprocidad Justa)"* usando la **numeración de
ingeniería**, mientras que el libro reserva T9 para **No-Antropocentrismo** (§3, pilar 4) y la
Reciprocidad Justa es T17. El propio motor lo declara y mantiene el alias retrocompatible
(`validate_t9_reciprocidad = validate_t17_reciprocidad`, con la nota de renumeración "T9 → T17" en
`maxocontracts/core/axioms.py`) [VERIFICADO]. Se advierte porque un lector que cruce §3 con §7.3 sin
esta nota creería que el documento se contradice.

Además, el **quórum `eco-` N-de-M** que el canon afirma (Cap. 16.5 §16.5.14) **no está cableado y no
tiene N ni M para el Reino Natural**. No es un vacío de fuentes: es un vacío de decisión (§13).

---

## 8. Invariante INV2-E: de estándar a contrato ejecutable

### 8.0 Estado real, antes de una sola línea de especificación

🔴 **INV2-E NO ESTÁ IMPLEMENTADO.** Ninguna pieza existe. Verificado por lectura directa del
repositorio:

| Pieza | Estado | Evidencia |
|---|---|---|
| `SDV_E` (tipo) | 🔴 no existe | `maxocontracts/core/types.py` define `SDV` y `SDV_S`; **no hay `SDV_E`** |
| `SDV_EValidatorBlock` | 🔴 no existe | `maxocontracts/blocks/` contiene `sdv_validator.py`, `sdv_s_validator.py`, `ternura.py`, `gamma_protector.py`, `reciprocity.py`, `action.py`, `condition.py`; **no hay `sdv_e_validator.py`** |
| `validate_invariant_sdv_e` | 🔴 no existe | `maxocontracts/core/axioms.py` tiene `validate_invariant_sdv` (INV2) y `validate_invariant_sdv_s` (INV2-S); **ninguno para el reino natural** |
| Guard de aplicabilidad | 🔴 no existe para el reino natural | el patrón sí existe: `if not participant.is_synthetic or participant.sdv_s_actual is None` en `sdv_s_validator.py` |
| Ciclos consecutivos → retractación | 🔴 no existe para el reino natural | `max_consecutive_cycles = 7` existe **solo** en el validador sintético |
| Capa de Ternura aplicada al ecosistema | 🔴 no existe | `ternura.py` opera sobre `participant_id`; **ningún guardián `eco-` la invoca** |
| **Crédito regenerativo que NO compensa** | 🔴 **no existe — es el agujero que este documento cierra** | `r_units` negativo **sí** está implementado y probado (`app/micromax.py`, `tests/test_micromax.py` con `-12.0`); **no existe `SUM(r_units)` ni ningún juez** |

**Consecuencia honesta:** todo lo que sigue es **propuesta no implementada**. El valor de §8 no es
que funcione: es que sea implementable sin reinterpretación y verificable por tests nombrados.

### 8.1 Enunciado del invariante

> **INV2-E — Suelo de Dignidad Vital del Reino Natural.**
> Ninguna acción de un contrato puede dejar a una unidad ecológica por debajo de los mínimos medidos
> de su SDV-E; ninguna acumulación de crédito regenerativo puede modificar ese veredicto, ni
> compensarlo, ni reiniciar su contador; y ninguna dimensión sin umbral puede declararse cumplida.

El invariante genérico **INV2** —*"Ninguna acción del contrato puede dejar a un participante bajo su
SDV"* (Cap. 17)— se conserva. INV2-E es su extensión al cuarto reino, con las mismas tres piezas que
INV2-S: **tipo**, **bloque validador** e **integración en `AxiomValidator.validate_all()`**.

### 8.2 El patrón exacto que se replica (INV2-S, verificado en código)

| Pieza del patrón | Dónde vive en INV2-S | Qué hace |
|---|---|---|
| Tipo con dimensiones y pesos | `SDV_S` en `core/types.py` | `DIMENSION_WEIGHTS` (suma 1,0), `DIMENSIONS`, `deficits()`, `violation_magnitude()`, `suffering_factor()` |
| Guard de aplicabilidad | `SDV_SValidatorBlock.validate()` | si no aplica, devuelve `applicable=False` **sin bloquear** (compatible con listas mixtas) |
| Bloque validador | `blocks/sdv_s_validator.py` | `validate()`, `validate_all()`, `_consecutive_cycles`, `reset_cycles()`, `_validation_log`, `to_dict()` |
| Ciclos consecutivos → retractación | ídem | `max_consecutive_cycles = 7`; al alcanzarlo, `should_retract = True` |
| Capa de Ternura | `blocks/ternura.py` | perdón consumible que reinicia ciclos; si no hay perdón, retracta e inicia rehabilitación |
| Validador axiomático | `core/axioms.py` | `validate_invariant_sdv_s()` → `ValidationResult` con `axiom_code="INV2-S"` |
| Integración | `AxiomValidator.validate_all()` | añade la validación sintética **solo si** `participant.is_synthetic` |

### 8.3 Propiedades formales de INV2-E

Doce propiedades. Cada una con su precedente y su test (nombres en §8.8).

| # | Propiedad | Enunciado | Precedente | Test |
|---|---|---|---|---|
| **P1** | **Atomicidad** | Un solo parámetro medido bajo su piso invalida el cumplimiento | `is_valid = len(violations) == 0` (INV2, INV2-S) | `test_un_solo_parametro_bajo_piso_invalida` |
| **P2** | **Base neutra** | `FE(v = 0)` vale **exactamente 1,0** | `FS_S = e^v`, corregida desde `1 + e^v` | `test_factor_neutro_con_violacion_cero` |
| **P3** | **Independencia del saldo** | El resultado es **invariante** ante cualquier cambio del crédito regenerativo acumulado: `validate(u, c) == validate(u, c′)` para todo `c`, `c′` | *"El suelo antes que el saldo"* (Cap. 16.5 §16.5.14) | `test_credito_no_altera_el_resultado` |
| **P4** | **Guard por tipo, no por dato** | `applicable=False` **si y solo si** el participante no es una unidad ecológica. La falta de medición **nunca** produce `applicable=False` | guard de `SDV_SValidatorBlock` (ampliado) | `test_guard_es_por_tipo_no_por_dato` |
| **P5** | **Sin dato no castiga y sin dato no aprueba** | `None` nunca se convierte en `0` ni en violación; y una cobertura incompleta **no puede** declararse `cumple` | `SDV.educacion_anos: Optional[int] = None` ("sin dato" no invalida) + INV2-EDU | `test_sin_dato_no_imputa_violacion` · `test_sin_cobertura_total_no_declara_cumple` |
| **P6** | **El sujeto protegido nunca es el objeto de la consecuencia** | La retractación recae sobre el contrato o la actividad humana; **jamás** sobre la unidad ecológica | documento 09 §8, requisito 3 | `test_objeto_de_retractacion_nunca_es_la_unidad` |
| **P7** | **Finitud computable** | Ningún campo admite `inf` ni `NaN`; lo "infinito" es un estado booleano | documento 09 §5.3; (hoy `r_units` acepta ambos) | `test_nan_e_inf_rechazados` |
| **P8** | **No colonización del TA** | Todo campo está en TA o en unidad física; ninguna magnitud en TVI ni TPI; la conversión TA↔TVI solo por PIU y **fuera** del invariante | Cap. 16.5 §16.5.14 · Cap. 5 §5.5 | `test_tipo_solo_admite_unidades_ta` |
| **P9** | **Independencia del ISE** | El veredicto no depende del ISE ni de sus dos escaleras en conflicto | documento 09, I7 y §11.3 | `test_veredicto_independiente_del_ise` |
| **P10** | **Monotonía** | Si el estado empeora en un parámetro y no mejora en ninguno, `v` no puede disminuir | — (nuevo) | `test_monotonia_de_la_violacion` |
| **P11** | **Cobertura declarada** | Si `v` se calcula sobre parámetros medidos, la cobertura se publica; dos `v` iguales con cobertura distinta **no** son equivalentes | — (nuevo; responde a la pregunta abierta 6 del documento 09) | `test_cobertura_declarada_en_el_resultado` |
| **P12** | **La Zona Libre no pondera** | Ninguna dimensión binaria ni el catálogo de lo inefable reciben peso; su violación se documenta | Cap. 8 §8.11 (dimensiones VIII y IX) | `test_zona_libre_sin_peso` |

### 8.4 Los tres estados (y por qué no dos)

`SDV_S` tiene dos estados: válido o violado. El SDV-E necesita tres, porque su instrumentación
**no existe todavía** y un invariante binario obligaría a elegir entre imputar violaciones que no se
midieron (castigar al ecosistema) o certificar cumplimientos que no se comprobaron (premiar al
operador). Las dos opciones son falsas.

| Estado | Condición | Consecuencia |
|---|---|---|
| `cumple` | Existe al menos un parámetro aplicable, **todos** los parámetros con piso están medidos y **ninguno** está bajo su piso; sin violación binaria | `FE = 1,0`; el crédito regenerativo de esa unidad es **utilizable** (§9.3) |
| `violacion` | Al menos un parámetro **medido** está bajo su piso, o una dimensión binaria está violada | `FE = e^v`; bloqueo; ciclos consecutivos avanzan; crédito **en cuarentena** |
| `indeterminado` | No hay violación medida **y** falta al menos un parámetro con piso | No hay bloqueo por piso; **bandera de opacidad ecológica** y obligación de instrumentar; **no habilita crédito** |

**El estado por defecto del SDV-E hoy es `indeterminado`, no `cumple`.** No es una hipérbole: sin
sensores, ninguna unidad puede cubrir hoy los 18 parámetros con umbral del catálogo de §4.1
(17 con peso, más `arrecife_dhw` solo en unidades de arrecife), y por
tanto **ninguna unidad puede declararse por encima de su suelo** — ni, en consecuencia, generar
crédito regenerativo utilizable. El agujero que el canon nombra se cierra, además, por esta vía.

### 8.5 Las dos vías de bloqueo

| Vía | Cuándo | Fundamento | Resultado |
|---|---|---|---|
| **Bloqueo por piso** | Hay violación medida | INV2-E / INV2 (Cap. 17) | `should_block_action = True`, `FE = e^v` |
| **Bloqueo precautorio** | No hay piso medido para una dimensión afectada **y** la acción propuesta es **irreversible** | T14 (Cap. 5): menor irreversibilidad, **carga de la prueba sobre quien propone** | `precautionary_block = True`, con `evidencia_ref` del costo de oportunidad asumido |

La segunda vía es la respuesta de ingeniería al hueco de las seis dimensiones sin umbral: **lo que no
tiene cifra no puede producir una violación, pero tampoco puede autorizarse a ciegas.** Y es
coherente con el canon hasta la letra: T14 no exige una medición, exige elegir la opción de menor
irreversibilidad y documentar el costo asumido.

### 8.6 Ciclos consecutivos: el patrón se replica, el número no

INV2-S retracta tras **7 ciclos consecutivos** de violación [VERIFICADO]. INV2-E replica el mecanismo
—contador por unidad, reinicio al recuperar, escalada con umbral— y **no hereda el 7**, por tres
razones que conviene dejar escritas:

1. **El ciclo no es la misma clase de objeto.** Los 7 ciclos del SDV-S se cuentan en ciclos
   operativos de un agente sintético, cuyo tiempo no es el del territorio (TPI, no TA). En el SDV-E el ciclo es un período de **TA** (año
   hidrológico, estación de crecimiento, ciclo de sucesión: sin fuente verificada, §6.2). Copiar el
   número cambiaría el significado: **7 ciclos TA pueden ser siete años de degradación continuada**.
2. **T14 prohíbe tolerar lo irreversible.** *"El sistema debe elegir la opción de menor
   irreversibilidad"* (Cap. 5). Un contador que retrasa el bloqueo durante siete años de un bosque
   contradice el axioma más fuerte que el SDV-E tiene.
3. **La consecuencia ya es inmediata.** En INV2-S el bloqueo y la retractación son dos momentos
   distintos (cualquier violación bloquea; la retractación llega al ciclo 7). En INV2-E el **bloqueo
   es inmediato** (P1) porque la pérdida no vuelve; el contador gobierna solo la **escalada** a
   retractación del contrato y a veto de la actividad.

**Decisión propuesta `[HIPÓTESIS]`:** `max_consecutive_cycles` **no tiene valor por defecto**. El
bloque constructor del validador exige configuración explícita de `unidad_de_ciclo_ta` y
`max_consecutive_cycles`; si faltan, la validación funciona, bloquea lo que debe bloquear y devuelve
`escalation_config_required = True` **sin escalar automáticamente**. Es un fallo cerrado en
gobernanza y abierto en protección: no se inventa un número de la ley y no se deja de proteger el
piso mientras el número no exista. Su valor definitivo es **POLÍTICA votable** (categoría `critical`),
con la restricción de que **no puede modificarse mientras exista una violación abierta** —el
equivalente del anti-flip-flop de 14 días del Parlamento Educativo (INV2-EDU), aquí como condición de
juego y no como plazo. El valor que se vote irá con `CHECK` en BD, como el resto de parámetros
`critical`.

### 8.7 Retractación: quién es el objeto

En INV2-S, `should_retract = True` retracta el contrato con el agente sintético. Trasladar eso al
Reino Natural produce un absurdo: **un río no se retracta.** El documento 09 §8 lo dejó dicho —*la
única acción ejecutable de INV2-E es detener o modificar la actividad humana que viola el piso*— y
aquí se convierte en campo del resultado:

```
objeto_de_retractacion ∈ {"contrato", "actividad", "ninguno"}   # nunca "unidad_ecologica"
```

El paralelo canónico exacto sigue siendo el *Veto por Crimen de Coherencia* del SDV-S: *"la
interrupción total del sistema que la provoca"* (Cap. 9.5 §9.5.10). Lo que se interrumpe es **la
causa**, no el sujeto protegido. Y la rehabilitación también cambia de titular: en INV2-S se
rehabilita al agente; en INV2-E se rehabilitan **dos cosas distintas que jamás se confunden**:

| Sujeto | Qué significa rehabilitar | Cómo se verifica |
|---|---|---|
| **La actividad humana** (el violador) | Cesar o reducir de forma verificable la presión | hecho verificable: la presión cesó (evidencia_ref) |
| **La unidad ecológica** (el protegido) | Recuperar el piso medido | medición en TA posterior; **no depende de la voluntad del violador** |

Esta separación es un aporte de este documento: impide el fraude más obvio del sistema —declarar
"rehabilitado" al ecosistema porque el papel firmado cambió.

### 8.8 Esqueleto de código propuesto (firmas reales)

> 🔴 **PROPUESTA — NO IMPLEMENTADO.** Los cinco bloques siguientes **no existen** en el repositorio.
> Las firmas siguen el patrón verificado de INV2-S para que sean implementables sin reinterpretación.
> **Límite declarado de esta propuesta:** los esqueletos de (b), (c), (d) y (e) son **firmas y lógica
> de flujo, no módulos ejecutables**: los cuerpos marcados con `...` y los helpers `_result`,
> `_evidence_index`, `_consecutive_cycles` y `_validation_log` quedan sin definir aquí y pertenecen a
> la implementación. Las firmas se escribieron para que el comportamiento descrito en §8.3-§8.7 sea
> comprobable por los tests de §8.9; no sustituyen a esos tests.

**(a) Tipo `SDV_E` en `maxocontracts/core/types.py`**

```python
# ===========================================================================
# PROPUESTA — NO IMPLEMENTADO.  Verificado: types.py define SDV y SDV_S.
# NO define SDV_E.  Este bloque es especificación, no código vivo.
# ===========================================================================
from enum import Enum

class SDV_EState(Enum):
    """Tres estados: la ausencia de dato no es ni violación ni cumplimiento (P5)."""
    CUMPLE = "cumple"
    VIOLACION = "violacion"
    INDETERMINADO = "indeterminado"


@dataclass
class SDV_E:
    """
    Suelo de Dignidad Vital del Reino Natural (Cap. 10 §10.4, Cap. 16.5 §16.5.14).

    Reglas del tipo:
    - TODO campo es TA o unidad física: nunca TVI ni TPI (P8).
    - `None` = SIN MEDICIÓN. No es 0, no es violación, no es cumplimiento (P5).
    - Ningún campo admite NaN ni inf: `float('inf')` y `Decimal('NaN')` se rechazan (P7).
    - Los parámetros sin umbral verificado NO tienen peso en PESOS_PISO (W1, §5.2).

    Invariante 2-E: ninguna unidad ecológica cae bajo su SDV-E por acción de un
    contrato, y ningún crédito regenerativo altera ese veredicto (P3).
    """

    # --- Aire (proxy declarado de salud humana; OMS, 2021) ---
    aire_pm25_anual: Optional[Decimal] = None          # max · µg/m³ anual
    aire_pm25_24h: Optional[Decimal] = None            # max · µg/m³ 24 h
    aire_pm10_anual: Optional[Decimal] = None          # max · µg/m³ anual
    aire_pm10_24h: Optional[Decimal] = None            # max · µg/m³ 24 h
    aire_no2_anual: Optional[Decimal] = None           # max · µg/m³ anual
    aire_no2_24h: Optional[Decimal] = None             # max · µg/m³ 24 h
    aire_o3_8h: Optional[Decimal] = None               # max · µg/m³ 8 h
    aire_so2_24h: Optional[Decimal] = None             # max · µg/m³ 24 h
    aire_co_24h: Optional[Decimal] = None              # max · mg/m³ 24 h

    # --- Agua (proxy declarado: calidad de agua de riego; FAO, 1985) ---
    agua_ph: Optional[Decimal] = None                  # range 6.5 – 8.4 (unidades de pH)
    agua_nitrato_n: Optional[Decimal] = None           # max · mg/L (NO3-N)
    agua_bicarbonato_me: Optional[Decimal] = None      # max · me/L (HCO3, aspersión)
    agua_oxigeno_disuelto: Optional[Decimal] = None    # SIN UMBRAL VERIFICADO (no pesa)

    # --- Biodiversidad y riesgo de colapso (IUCN RLE v2.0, 2024) ---
    rle_reduccion_distribucion_50a: Optional[Decimal] = None   # max · % de reducción
    rle_reduccion_historica_1750: Optional[Decimal] = None     # max · % de reducción
    rle_eoo_km2: Optional[Decimal] = None                      # min · km² (EOO)
    rle_aoo_celdas: Optional[int] = None                       # rejilla de 10 x 10 km (unidad)
    rle_degradacion_c1_pct: Optional[Decimal] = None           # max · % de extensión
    rle_probabilidad_colapso: Optional[Decimal] = None         # max · % en 100 años
    rle_categoria: Optional[str] = None                        # ordinal, 8 categorías, SIN PESO

    # --- Arrecifes (solo si el tipo de unidad es arrecife) ---
    arrecife_dhw: Optional[Decimal] = None             # escalonado · °C-semanas

    # --- Dominios SIN umbral verificado: se registran, no generan violación (§4.2) ---
    suelo_carbono_organico: Optional[Decimal] = None   # t C/ha · FAO publica mapas, no umbrales
    caudal_ecologico_pct_qma: Optional[Decimal] = None # % del caudal medio anual · SIN FUENTE
    conectividad_indice: Optional[Decimal] = None      # SIN FUENTE
    ciclos_naturales_estado: Optional[str] = None      # binaria · régimen presente/ausente
    riberas_protegidas_estado: Optional[str] = None    # binaria · franja presente/ausente

    # --- Zona Libre: binaria, auditable, SIN PESO (P12) ---
    zona_libre_violada: bool = False
    zona_libre_evidencia_ref: Optional[str] = None

    # --- Contexto de la violación, en TA (Cap. 5 §5.5) ---
    ta_periodo_inicio: Optional[date] = None
    ta_periodo_fin: Optional[date] = None
    factor_intensidad: Decimal = Decimal("1.0")

    # Operador por parámetro: min | max | range | escalonado | ordinal | binary
    PARAM_KINDS: ClassVar[Dict[str, str]] = {
        "aire_pm25_anual": "max", "aire_pm25_24h": "max",
        "aire_pm10_anual": "max", "aire_pm10_24h": "max",
        "aire_no2_anual": "max", "aire_no2_24h": "max",
        "aire_o3_8h": "max", "aire_so2_24h": "max", "aire_co_24h": "max",
        "agua_ph": "range", "agua_nitrato_n": "max", "agua_bicarbonato_me": "max",
        "rle_reduccion_distribucion_50a": "max",
        "rle_reduccion_historica_1750": "max",
        "rle_eoo_km2": "min", "rle_degradacion_c1_pct": "max",
        "rle_probabilidad_colapso": "max", "arrecife_dhw": "escalonado",
    }
    PARAM_RANGES: ClassVar[Dict[str, tuple]] = {
        "agua_ph": (Decimal("6.5"), Decimal("8.4")),   # FAO, 1985
    }
    # Categorías ordinales del RLE (IUCN, 2024). Las tres primeras son "amenazado".
    RLE_ORDER: ClassVar[Dict[str, int]] = {
        "LC": 0, "NT": 1, "VU": 2, "EN": 3, "CR": 4, "CO": 5, "DD": 6, "NE": 6,
    }
    RLE_FLOOR_CATEGORY: ClassVar[str] = "VU"     # piso: mejor que VU (LC o NT)
    RLE_WARNING_CATEGORY: ClassVar[str] = "NT"   # zona de aviso declarada por norma

    # Pesos. PESOS_PISO suma 0,680: SOLO parámetros con umbral verificado (§5.2).
    # `arrecife_dhw` tiene piso (4 °C-semanas) pero NO peso propio en el vector base:
    # en unidades de arrecife su peso se toma del grupo de riesgo (0,30) y la suma
    # declarada no cambia.  PISO Y PESO SON INDEPENDIENTES: un parámetro con piso y
    # sin peso sigue produciendo `violacion` (P1); el peso solo dimensiona `v` y `FE`.
    PESOS_PISO: ClassVar[Dict[str, Decimal]] = {
        "aire_pm25_anual": Decimal("0.06"), "aire_pm25_24h": Decimal("0.04"),
        "aire_pm10_anual": Decimal("0.02"), "aire_pm10_24h": Decimal("0.02"),
        "aire_no2_anual": Decimal("0.02"), "aire_no2_24h": Decimal("0.02"),
        "aire_o3_8h": Decimal("0.01"), "aire_so2_24h": Decimal("0.005"),
        "aire_co_24h": Decimal("0.005"),
        "agua_ph": Decimal("0.06"), "agua_nitrato_n": Decimal("0.09"),
        "agua_bicarbonato_me": Decimal("0.03"),
        "rle_reduccion_distribucion_50a": Decimal("0.08"),
        "rle_reduccion_historica_1750": Decimal("0.05"),
        "rle_eoo_km2": Decimal("0.06"),
        "rle_degradacion_c1_pct": Decimal("0.07"),
        "rle_probabilidad_colapso": Decimal("0.04"),
    }
    # PESOS_TABLERO suma 1,000: incluye dominios sin piso para el tablero tipo ISE.
    PESOS_TABLERO: ClassVar[Dict[str, Decimal]] = {
        **PESOS_PISO,
        "agua_oxigeno_disuelto": Decimal("0.02"),
        "suelo_carbono_organico": Decimal("0.15"),
        "caudal_ecologico_pct_qma": Decimal("0.075"),
        "conectividad_indice": Decimal("0.075"),
    }
    # `DIMENSIONS` = parámetros que TIENEN piso y por tanto pueden violarlo (18,
    # incluido `arrecife_dhw`).  `DIMENSIONS_SIN_PISO` = los que solo se registran.
    DIMENSIONS: ClassVar[tuple] = tuple(PARAM_KINDS.keys())
    # `arrecife_dhw` tiene piso pero SOLO se exige si el tipo de unidad es
    # arrecife. Si entrara en `missing_dimensions` global, un bosque quedaría
    # `indeterminado` para siempre y NUNCA podría llegar a `cumple` —ni, por
    # tanto, a tener crédito utilizable (§9.3)—. El tipo de unidad lo activa.
    DIMENSIONS_DE_TIPO_ARRECIFE: ClassVar[tuple] = ("arrecife_dhw",)
    DIMENSIONS_SIN_PISO: ClassVar[tuple] = tuple(
        d for d in PESOS_TABLERO if d not in PARAM_KINDS
    )
    # Cobertura del piso declarada = suma real del vector de pesos (hoy 0,680).
    COBERTURA_PISO_DECLARADA: ClassVar[Decimal] = sum(
        PESOS_PISO.values(), Decimal("0")
    )

    def __post_init__(self):
        """Rechaza NaN, inf y valores físicamente imposibles (P7)."""
        for dim in self.PARAM_KINDS:
            value = getattr(self, dim, None)
            if value is None:
                continue
            if isinstance(value, float) and (value != value or value in (float("inf"), float("-inf"))):
                raise ValueError(f"SDV-E '{dim}': NaN/inf no son mediciones")
            if isinstance(value, Decimal) and (value.is_nan() or value.is_infinite()):
                raise ValueError(f"SDV-E '{dim}': NaN/inf no son mediciones")
            if isinstance(value, Decimal) and value < 0:
                raise ValueError(f"SDV-E '{dim}': un valor absoluto no puede ser negativo")
        # El MÍNIMO no puede dejar un piso sin declarar: `None` en el mínimo
        # significa "sin piso", y un piso indeterminado no es un piso. El mínimo
        # de una unidad concreta declara todos los parámetros con piso de su
        # tipo (los 17 con peso, y `arrecife_dhw` si la unidad es arrecife).
        for dim in self.DIMENSIONS:
            if dim == "arrecife_dhw":
                continue                      # solo aplica si el tipo es arrecife
            if getattr(self, dim) is None:
                raise ValueError(
                    f"SDV-E mínimo incompleto: '{dim}' sin piso declarado "
                    "(un piso indeterminado no es un piso)"
                )
        if self.rle_categoria is not None and self.rle_categoria not in self.RLE_ORDER:
            raise ValueError(
                f"rle_categoria '{self.rle_categoria}' no es una de las 8 categorías RLE"
            )
        if self.factor_intensidad < 0:
            raise ValueError("factor_intensidad no puede ser negativo")

    # --- Comparación (mismo sentido que SDV_S: minimum.deficits(actual)) ---
    def deficits(self, actual: "SDV_E") -> Dict[str, Decimal]:
        """Déficit NORMALIZADO por parámetro medido. Omite los sin medición (P5)."""
        out: Dict[str, Decimal] = {}
        for dim in self.DIMENSIONS:
            now, req = getattr(actual, dim), getattr(self, dim)
            if now is None or req is None:
                continue                                # sin dato: no hay déficit
            kind = self.PARAM_KINDS[dim]
            if kind == "min":
                d = (req - now) / req if req > 0 else Decimal("0")
            elif kind == "max":
                d = (now - req) / req if req > 0 else Decimal("0")
            elif kind == "range":
                lo, hi = self.PARAM_RANGES[dim]
                d = ((lo - now) / lo) if now < lo else ((now - hi) / hi if now > hi else Decimal("0"))
            else:                                       # escalonado: nivel, no interpolación
                d = Decimal("1") if now > req else Decimal("0")
            if d > 0:
                out[dim] = d
        return out

    def violations(self, actual: "SDV_E") -> Dict[str, str]:
        """Parámetros violados, con descripción legible (mismo formato que SDV_S)."""
        return {
            dim: f"{getattr(actual, dim)} {'>' if self.PARAM_KINDS[dim] == 'max' else '<'} "
                 f"{getattr(self, dim)} mínimo"
            for dim in self.deficits(actual)
        }

    def missing_dimensions(self, actual: "SDV_E") -> Dict[str, str]:
        """
        Parámetros CON PISO que no tienen medición en `actual`.
        Excluye los que solo aplican a un tipo de unidad (arrecife) y los que
        no tienen piso (suelo, caudal, conectividad, ciclos, riberas, OD):
        ninguno de ellos puede volver `indeterminado` a una unidad por el hecho
        de no medirse, porque no son piso.
        """
        return {
            dim: "sin medición"
            for dim in self.DIMENSIONS
            if dim not in self.DIMENSIONS_DE_TIPO_ARRECIFE
            and dim in self.PESOS_PISO
            and getattr(actual, dim) is None
        }

    def measured_weight(self, actual: "SDV_E") -> Decimal:
        """Σ(PESOS_PISO) de los parámetros efectivamente medidos (§5.2, W2)."""
        return sum(
            (
                self.PESOS_PISO.get(d, Decimal("0"))
                for d in self.DIMENSIONS
                if getattr(actual, d) is not None
            ),
            Decimal("0"),
        )

    # Cobertura medida sobre el piso declarado: measured_weight / 0,680 (P11).
    # OJO: 0,680 es un DENOMINADOR FIJO (Σ PESOS_PISO), no una medición; el
    # cociente NO es "porcentaje del estándar protegido". Con un solo parámetro
    # sin medir ya baja de 1,0 (ver §5.2, W2).
    def coverage(self, actual: "SDV_E") -> Decimal:
        """Cobertura medida: measured_weight / 0,680 (P11)."""
        return self.measured_weight(actual) / self.COBERTURA_PISO_DECLARADA

    def violation_magnitude(self, actual: "SDV_E") -> Decimal:
        """
        Magnitud ponderada v. Renormalización DECLARADA sobre lo medido (P11):
        v = Σ[déficit × peso] / cobertura_medida.  Si no hay nada medido, v = 0.
        """
        deficits = self.deficits(actual)
        if not deficits:
            return Decimal("0")
        bruto = sum(
            (deficits[d] * self.PESOS_PISO.get(d, Decimal("0")) for d in deficits),
            Decimal("0"),
        )
        cobertura = self.coverage(actual)
        return bruto / cobertura if cobertura > 0 else bruto

    def violation_factor(self, actual: "SDV_E", extra_magnitude: Decimal = Decimal("0")) -> Decimal:
        """FE = e^(v × intensidad + extra). Base neutra: FE(0) = 1,0 exacto (P2)."""
        v = (self.violation_magnitude(actual) * actual.factor_intensidad) + extra_magnitude
        return Decimal.exp(v)

    def estado(self, actual: "SDV_E") -> SDV_EState:
        """Tres estados (P5): violación medida > indeterminado > cumple."""
        if self.violations(actual):
            return SDV_EState.VIOLACION
        if self.missing_dimensions(actual):
            return SDV_EState.INDETERMINADO
        return SDV_EState.CUMPLE

    def is_collapsed(self) -> bool:
        """
        Colapso según el endpoint espacial del RLE (IUCN, 2024):
        AOO = 0 celdas de 10x10 km  Y  EOO = 0 km².  Es irreversible (§5.4).
        """
        return (
            self.rle_categoria == "CO"
            or (
                self.rle_aoo_celdas == 0
                and self.rle_eoo_km2 is not None
                and self.rle_eoo_km2 == 0
            )
        )

    def meets_minimum(self, actual: "SDV_E") -> bool:
        """True SOLO en estado `cumple`. `indeterminado` no es cumplimiento (P5)."""
        return self.estado(actual) is SDV_EState.CUMPLE
```

**(b) Guard de aplicabilidad y bloque validador en `maxocontracts/blocks/sdv_e_validator.py`**

```python
# ===========================================================================
# PROPUESTA — NO IMPLEMENTADO.  Verificado: blocks/ contiene sdv_validator.py,
# sdv_s_validator.py, ternura.py, gamma_protector.py, reciprocity.py,
# action.py, condition.py.  NO existe sdv_e_validator.py.
# ===========================================================================
@dataclass
class SDV_EViolation:
    dimension: str
    actual_value: Optional[Decimal]
    minimum_required: Decimal
    deficit: Decimal                 # déficit NORMALIZADO
    severity: str                    # leve | moderada | severa | irreversible
    evidencia_ref: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]: ...


@dataclass
class SDV_EValidationResult:
    is_valid: bool
    participant_id: str
    applicable: bool                 # False SOLO si no es unidad ecológica (P4)
    estado: str                      # cumple | violacion | indeterminado
    violations: List[SDV_EViolation]
    violation_magnitude: Decimal
    violation_factor: Decimal        # FE
    coverage: Decimal                # cobertura medida sobre el piso (P11)
    missing_dimensions: List[str]
    opacity_flag: bool               # bandera de opacidad ecológica (§6.3)
    consecutive_cycles: int
    escalation_config_required: bool = False
    severity: str = "leve"
    should_block_action: bool = False
    precautionary_block: bool = False            # vía T14 (§8.5)
    should_retract: bool = False
    retraction_object: str = "ninguno"           # contrato | actividad | ninguno (P6)
    credit_usable: bool = False                  # §9.3 — NUNCA depende del saldo (P3)
    ternura_action: str = "none"                 # none | forgiveness_applied |
                                                 # rehabilitation_started |
                                                 # rehabilitation_refused_irreversible
    rehabilitation_status: Optional[str] = None
    checked_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def violation_count(self) -> int: ...

    def to_dict(self) -> Dict[str, Any]: ...


class SDV_EValidatorBlock:
    """
    Bloque validador de INV2-E para MaxoContracts.

    Ejemplo de uso:
    ```python
    validator = SDV_EValidatorBlock(
        minimum_sdv_e=SDV_E(minimum=...),
        unidad_de_ciclo_ta="anio_hidrologico",     # SIN VALOR POR DEFECTO (§8.6)
        max_consecutive_cycles=3,                  # POLÍTICA votable, no ley
    )
    result = validator.validate(eco_participant)
    if result.should_block_action:
        ...
    ```
    Nota de firma: los `...` de los cuerpos y la llamada `SDV_E(minimum=...)` son **pseudocódigo de
    firma**, no un módulo válido. El tipo `SDV_E` no tiene campo `minimum`: sus campos son los
    parámetros de §8.8(a) y todos son opcionales.
    """

    def __init__(
        self,
        minimum_sdv_e: Optional[SDV_E] = None,
        weights: Optional[Dict[str, Decimal]] = None,
        block_on_any_violation: bool = True,          # LEY: el bloqueo es inmediato
        unidad_de_ciclo_ta: Optional[str] = None,     # sin default heredado
        max_consecutive_cycles: Optional[int] = None, # sin default heredado
        auto_retract_on_sustained_violation: bool = True,
        cobertura_minima_para_cumplir: Decimal = Decimal("1.0"),
        ternura: Optional[TernuraLayer] = None,
        credit_reader: Optional[Callable[[str], Decimal]] = None,  # solo lectura, §9.3
        verified_evidence_ids: Optional[Set[str]] = None,
    ):
        ...

    def validate(self, participant: Participant) -> SDV_EValidationResult:
        """
        Valida el SDV-E de una unidad ecológica.

        Guard (P4): si el participante NO es una unidad ecológica, retorna
        `applicable=False` SIN bloquear, igual que SDV_SValidatorBlock con
        participantes no sintéticos.

        La falta de MEDICIÓN no activa este guard (era el fallo de la primera
        versión de este esqueleto: `or participant.sdv_e_actual is None` habría
        devuelto `applicable=False` a una unidad ecológica sin sensores, en
        contradicción con P4 y con `test_guard_es_por_tipo_no_por_dato`).
        Sin medición se valida contra un `SDV_E()` vacío → `indeterminado`.
        Requisito del tipo: `minimum_sdv_e` debe traer declarado **todo**
        parámetro con piso de su tipo de unidad; un `None` en el mínimo no
        significa "sin medición" sino "sin piso", y un piso indeterminado no
        es un piso (el tipo lo rechaza en `__post_init__`).
        """
        if not participant.is_ecological:
            return self._result(is_valid=True, participant=participant, applicable=False,
                                estado="indeterminado", violations=[], magnitude=Decimal("0"),
                                factor=Decimal("1"), coverage=Decimal("0"), missing=[],
                                cycles=0)                              # compatible con listas mixtas
        actual = participant.sdv_e_actual if participant.sdv_e_actual is not None else SDV_E()
        estado = self.minimum_sdv_e.estado(actual)
        violations = [
            SDV_EViolation(
                dimension=dim,
                actual_value=getattr(actual, dim),
                minimum_required=getattr(self.minimum_sdv_e, dim),
                deficit=deficit,
                severity=self._severity(deficit, actual),
                evidencia_ref=self._evidence_index.get((participant.id, dim)),
            )
            for dim, deficit in self.minimum_sdv_e.deficits(actual).items()
        ]
        coverage = self.minimum_sdv_e.coverage(actual)
        # Ciclos consecutivos: mismo mecanismo que INV2-S, unidad y umbral propios.
        cycles = self._consecutive_cycles.get(participant.id, 0)
        if estado is SDV_EState.VIOLACION:
            cycles += 1
        else:
            cycles = 0
        self._consecutive_cycles[participant.id] = cycles
        # Escalada SOLO si hay configuración explícita (fallo cerrado en gobernanza).
        escalada_configurada = (
            self.unidad_de_ciclo_ta is not None and self.max_consecutive_cycles is not None
        )
        should_retract = (
            self.auto_retract_on_sustained_violation
            and escalada_configurada
            and estado is SDV_EState.VIOLACION
            and cycles >= self.max_consecutive_cycles
        )
        # Capa de Ternura: modula la CONSECUENCIA, nunca la contabilidad (T13).
        ternura_action, rehab = "none", None
        if should_retract:
            if actual.is_collapsed():
                ternura_action = "rehabilitation_refused_irreversible"
                rehab = None            # no hay qué rehabilitar: el endpoint ya ocurrió
            elif self.ternura is not None and self.ternura.active_forgiveness(participant.id):
                self.ternura.consume_forgiveness(participant.id)
                self._consecutive_cycles[participant.id] = cycles = 0
                ternura_action = "forgiveness_applied"
            elif self.ternura is not None:
                self.ternura.begin_rehabilitation(participant.id)
                ternura_action = "rehabilitation_started"
                rehab = RehabilitationStatus.IN_REHABILITATION.value
        # INV2-E NO recibe el saldo como argumento de la decisión (P3):
        # solo lo lee para CUARENTENA, y solo puede restringir, nunca habilitar.
        # `cumple` exige el piso COMPLETO (§8.4): el cociente de pesos solo no
        # basta — con `cobertura >= 1,0` un parámetro sin medir podría colarse—,
        # así que se exige además que no falte ningún parámetro con piso.
        credit_usable = (
            estado is SDV_EState.CUMPLE
            and not self.minimum_sdv_e.missing_dimensions(actual)
            and coverage >= self.cobertura_minima_para_cumplir
        )
        result = self._result(
            is_valid=estado is not SDV_EState.VIOLACION,
            participant=participant, applicable=True, estado=estado.value,
            violations=violations,
            magnitude=self.minimum_sdv_e.violation_magnitude(actual),
            factor=self.minimum_sdv_e.violation_factor(actual),
            coverage=coverage,
            missing=sorted(self.minimum_sdv_e.missing_dimensions(actual)),
            cycles=cycles,
            should_block=self.block_on_any_violation and estado is SDV_EState.VIOLACION,
            should_retract=should_retract,
            retraction_object="contrato" if should_retract else "ninguno",
            credit_usable=credit_usable,
            opacity=estado is SDV_EState.INDETERMINADO,
            escalation_required=not escalada_configurada,
            ternura_action=ternura_action,
            rehabilitation_status=rehab,
        )
        self._validation_log.append(result)          # T13: la contabilidad no se borra
        return result

    def validate_proposed_action(
        self,
        participant: Participant,
        *,
        irreversible: bool,
        dimensiones_afectadas: Sequence[str],
        evidencia_ref: str,
    ) -> SDV_EValidationResult:
        """
        Vía precautoria (T14, §8.5). Si la acción es IRREVERSIBLE y afecta una
        dimensión SIN PISO medido, bloquea: la carga de la prueba recae sobre
        quien propone y debe documentar el costo de oportunidad asumido.
        """
        ...

    def validate_all(self, participants: List[Participant]) -> List[SDV_EValidationResult]: ...
    def reset_cycles(self, participant_id: str) -> None: ...
    def get_validation_log(self) -> List[SDV_EValidationResult]: ...
    def to_dict(self) -> Dict[str, Any]: ...

    # Helpers internos
    def _severity(self, deficit: Decimal, actual: SDV_E) -> str:
        """leve ≤10 % · moderada ≤30 % · severa >30 % · irreversible (colapso)."""
        if actual.is_collapsed():
            return "irreversible"
        if deficit <= Decimal("0.10"):
            return "leve"
        if deficit <= Decimal("0.30"):
            return "moderada"
        return "severa"

    def _result(self, **kwargs) -> SDV_EValidationResult: ...
```

**(c) Validador axiomático en `maxocontracts/core/axioms.py`**

```python
    @staticmethod
    def validate_invariant_sdv_e(
        unit_sdv_e: SDV_E, minimum_sdv_e: SDV_E
    ) -> ValidationResult:
        """
        Invariante 2-E: SDV-E Respetado (Reino Natural).
        Ninguna unidad ecológica puede caer bajo su SDV-E.
        """
        # PROPUESTA — NO IMPLEMENTADO en axioms.py
        estado = minimum_sdv_e.estado(unit_sdv_e)
        violations = minimum_sdv_e.violations(unit_sdv_e)
        faltantes = minimum_sdv_e.missing_dimensions(unit_sdv_e)
        return ValidationResult(
            is_valid=estado is SDV_EState.CUMPLE,
            axiom_code="INV2-E",
            axiom_name="SDV-E Respetado",
            message=(
                "SDV-E cumplido en todas las dimensiones con piso"
                if estado is SDV_EState.CUMPLE
                else (
                    f"SDV-E violado en: {', '.join(violations.keys())}"
                    if estado is SDV_EState.VIOLACION
                    else f"SDV-E indeterminado: {len(faltantes)} dimensión(es) sin medición"
                )
            ),
            details={
                "estado": estado.value,
                "violations": violations,
                "missing": sorted(faltantes),
                "coverage": str(minimum_sdv_e.coverage(unit_sdv_e)),
            },
        )
```

Y su integración en `AxiomValidator.validate_all()`, con el guard de tipo (una línea, sin romper
compatibilidad hacia atrás):

```python
            # Participantes del Reino Natural (Cap. 10 §10.4) validan SDV-E
            if participant.is_ecological and participant.sdv_e_actual is not None:
                results.append(
                    cls.validate_invariant_sdv_e(participant.sdv_e_actual, SDV_E())
                )
```

**(d) Extensión de `TernuraLayer` para el Reino Natural**

`TernuraLayer` ya es agnóstico del reino: opera sobre `participant_id` y `grantor_id` como cadenas,
de modo que un guardián `eco-` **puede** otorgar perdón sin cambiar la clase [VERIFICADO]. Lo que
falta es lo específico del ecosistema:

```python
class RehabilitationStatus(Enum):
    # ... valores existentes ...
    IRREVERSIBLE = "irreversible"   # PROPUESTA: colapso (AOO = 0 y EOO = 0)


class TernuraLayer:
    def mark_irreversible(self, participant_id: str, evidence_ref: str) -> RehabilitationRecord:
        """
        PROPUESTA. Registra un colapso como irreversible (IUCN, 2024: área de
        ocupación 0 celdas de 10x10 km y extensión de presencia 0 km²).
        Con el endpoint alcanzado, la rehabilitación de la UNIDAD no aplica:
        el perdón del guardián puede modular la consecuencia sobre la ACTIVIDAD
        humana, y no puede devolver el ecosistema.
        """
        ...

    def demonstrable_change_is_pressure_cessation(self, participant_id: str) -> bool:
        """
        PROPUESTA. En el Reino Natural, "cambio demostrado" significa que la
        PRESIÓN cesó (hecho verificable), NO que la unidad se recuperó: la
        recuperación se mide en TA con el propio SDV_E y no depende del violador.
        """
        ...
```

**(e) Adaptador de crédito regenerativo — solo lectura, y solo para restringir**

```python
# app/micromax.py (o un módulo de solo lectura).  PROPUESTA — NO IMPLEMENTADO.
def credito_regenerativo_acumulado(conjunto_id: str, ta_periodo: tuple) -> Decimal:
    """
    Suma de `r_units` NEGATIVOS de un conjunto en un período TA.
    Hoy NO EXISTE: `r_units` negativo está implementado y probado en
    `log_cdd`, pero no hay `SUM(r_units)` ni ningún consumidor.
    REGLA: INV2-E lo usa SOLO para cuarentena (puede reducir lo habilitado,
    nunca habilitar).  La decisión del piso NO lo recibe como argumento (P3).
    """
    ...
```

### 8.9 Tests necesarios (`tests/test_maxocontracts/test_sdv_e.py`)

Los tests son la especificación ejecutable de §8.3. Se nombran con el estilo del repositorio
(`test_sdv_s.py`, `test_ternura.py`) y se agrupan en cinco clases.

**`TestSDV_E` — el tipo (19 tests)**

- `test_default_estado_indeterminado`: un `SDV_E()` sin mediciones está en `indeterminado`, nunca en
  `cumple` (P5).
- `test_minimo_incompleto_rechazado`: un `SDV_E` destinado a mínimo con un parámetro con peso sin
  declarar lanza `ValueError` —un piso sin declarar no es un piso.
- `test_arrecife_no_bloquea_a_un_bosque`: sin `arrecife_dhw` medido, una unidad que no es arrecife
  puede llegar a `cumple`; el parámetro solo aplica si el tipo de unidad es arrecife.
- `test_un_solo_parametro_bajo_piso_invalida`: `aire_no2_anual` = 11 µg/m³ con el resto en el piso →
  `violacion` (P1); un solo parámetro medido bajo su piso invalida el cumplimiento.
- `test_operador_max_deficit_normalizado`: `(actual − req) / req`, no la diferencia cruda.
- `test_operador_min_eoo`: EOO por debajo de 50 000 km² produce déficit; por encima, no.
- `test_operador_range_ph`: pH 6,0 produce déficit; pH 7,0 no; pH 9,0 produce déficit.
- `test_operador_escalonado_dhw`: DHW = 9 cae en el nivel 2 y **no** se interpola.
- `test_categoria_ordinal_no_genera_deficit`: `rle_categoria = "EN"` no entra en `violations()` ni en
  `violation_magnitude()` (P12, dimensión sin peso).
- `test_categoria_rle_invalida_raisas`: una categoría distinta de las ocho oficiales lanza `ValueError`.
- `test_sin_dato_no_imputa_violacion`: `None` no se convierte en 0 ni en violación (P5).
- `test_sin_cobertura_total_no_declara_cumple`: con un parámetro sin medir, el estado es
  `indeterminado` aunque todo lo medido cumpla (P5).
- `test_factor_neutro_con_violacion_cero`: `FE == Decimal("1.0")` exacto (P2).
- `test_factor_exponencial_y_finito`: con violación, `FE > 1` y finito.
- `test_factor_intensidad`: `factor_intensidad = 3` multiplica la violación.
- `test_nan_e_inf_rechazados`: `NaN`, `inf` y `-inf` lanzan `ValueError` (P7).
- `test_valor_negativo_rechazado`: un valor absoluto negativo lanza `ValueError`.
- `test_cobertura_declarada`: `coverage()` devuelve `medido / 0,680` (P11).
- `test_monotonia_de_la_violacion`: empeorar un parámetro sin mejorar ninguno no reduce `v` (P10).

**`TestSDV_EValidatorBlock` — el bloque (12 tests)**

- `test_participante_no_ecologico_no_aplica`: un humano devuelve `applicable=False` **sin bloquear**.
- `test_guard_es_por_tipo_no_por_dato`: una unidad ecológica **sin ninguna medición** devuelve
  `applicable=True`, `estado="indeterminado"`, `opacity_flag=True` y **no** `applicable=False` (P4).
- `test_violacion_bloquea_accion_inmediatamente`: el bloqueo no espera ciclos (P1, §8.6).
- `test_ciclos_consecutivos_cuentan_y_reinician`: 3 violaciones seguidas → `consecutive_cycles == 3`;
  una validación en `cumple` → vuelve a 0.
- `test_sin_configuracion_no_escala`: sin `max_consecutive_cycles`, `should_retract is False` y
  `escalation_config_required is True` (§8.6).
- `test_escalada_con_configuracion_explicita`: con `max_consecutive_cycles=3`, la **tercera** violación
  consecutiva retracta (el contador incrementa antes de comparar, igual que en `SDV_SValidatorBlock`).
- `test_objeto_de_retractacion_nunca_es_la_unidad`: `retraction_object in {"contrato","actividad",`
  `"ninguno"}` en todos los casos —ninguno de ellos es la unidad ecológica—, incluido el colapso (P6).
- `test_bloqueo_precautorio_t14`: acción irreversible sobre dimensión sin piso →
  `precautionary_block is True` sin violación medida (§8.5).
- `test_bloqueo_precautorio_no_dispara_sin_irreversibilidad`.
- `test_indeterminado_no_bloquea_pero_marca_opacidad`: la duda no castiga, pero obliga a instrumentar.
- `test_veredicto_independiente_del_ise`: el resultado no cambia si se altera cualquier insumo del
  tablero ISE (P9).
- `test_to_dict_y_log_de_auditoria`: `to_dict()` expone `coverage`, `estado` y el contador; el log
  conserva todos los registros (T13).

**`TestINV2_ENoCompensacion` — el agujero que se cierra (7 tests)**

- `test_credito_no_altera_el_resultado`: dos unidades idénticas con `credito = 0` y
  `credito = −1e9` producen resultados **idénticos** en `estado`, `violations`, `violation_magnitude`,
  `violation_factor` y `consecutive_cycles` (P3). **Es el test central del documento.**
- `test_credito_no_resetea_ciclos`: acumular crédito no reinicia el contador de ciclos.
- `test_credito_no_habilita_perdon`: el perdón solo lo otorga la parte `eco-` vía guardián, no el saldo.
- `test_credito_en_cuarentena_bajo_el_piso`: con `estado != cumple`, `credit_usable is False`.
- `test_credito_no_utilizable_en_indeterminado`: sin cobertura completa, `credit_usable is False`
  aunque no haya violación (la vía por la que hoy nada sería acreditable).
- `test_credito_utilizable_solo_en_cumple`: con todas las mediciones y sin violación,
  `credit_usable is True` — el crédito **sí** financia restauración por encima del piso (§9.3).
- `test_credito_corrupto_solo_puede_restringir`: con un lector de crédito que devuelve `NaN`, `inf` o
  valores absurdos, la decisión del piso es la misma y `credit_usable` nunca pasa a `True`.

**`TestTernuraEco` — perdón y rehabilitación del cuarto reino (5 tests)**

- `test_perdon_no_baja_el_piso`: tras el perdón, `minimum_sdv_e` no cambia y la violación queda en el
  log (T13).
- `test_perdon_no_borra_la_violacion`: el registro previo sigue en `get_validation_log()`.
- `test_colapso_rechaza_rehabilitacion`: con `AOO = 0` y `EOO = 0`,
  `ternura_action == "rehabilitation_refused_irreversible"`.
- `test_cambio_demostrado_es_cese_de_presion`: recuperar la métrica sin cesar la presión **no**
  completa la rehabilitación de la actividad (§8.7).
- `test_guia_eco_puede_otorgar_perdon_sin_cambiar_ternura`: `TernuraLayer` acepta un `grantor_id`
  `eco-*` sin modificaciones de clase.

**`TestSDV_EIntegration` — el motor (5 tests)**

- `test_participante_is_ecological_property`: `Participant` con `sdv_e_actual` no nulo es ecológico.
- `test_update_sdv_e`: actualización del estado ecológico de la unidad.
- `test_invariant_sdv_e_falla_con_violacion`: el validador axiomático devuelve inválido con una
  violación medida.
- `test_invariant_sdv_e_pasa_con_cumplimiento`: con el piso completo medido y sin violación,
  `is_valid` es verdadero.
- `test_human_participant_backward_compatible`: un participante humano sigue validando igual que antes
  (el guard de tipo no puede romper la suite existente).
- `test_contract_validate_includes_sdv_e`: `AxiomValidator.validate_all()` incorpora INV2-E cuando hay
  una unidad ecológica en la lista.

**Tests de `app/micromax.py` (2 tests, fuera del motor)**

- `test_suma_r_units_no_existe_o_es_explicita`: fija por escrito que hoy **no** hay agregado de
  `r_units`; si alguien lo añade, el test lo obliga a declararlo.
- `test_r_units_rechaza_nan_e_inf`: el crédito infalsable de hoy (§9.4) no debe además aceptar
  `NaN`/`inf`.

**Total propuesto: 50 tests** (19 + 12 + 7 + 5 + 5 en el motor, más 2 en `app/micromax.py`; el doble
de los **28** con los que hoy se prueba el SDV-S en `tests/test_maxocontracts/test_sdv_s.py`),
ninguno de los cuales existe todavía.

---

## 9. El suelo antes que el saldo (no compensación)

Esta es la sección por la que existe el documento: el canon nombró el agujero y este invariante lo
cierra. El agujero, dicho con precisión contable: **hoy se puede acumular crédito regenerativo
mientras el ecosistema se degrada, y el sistema no lo detecta** (Cap. 16.5 §16.5.14).

### 9.1 El estado real, verificado

| Pieza | Estado | Evidencia |
|---|---|---|
| `r_units` negativo = crédito regenerativo | 🟢 **implementado y probado** | `app/micromax.py` (`log_cdd`): *"`r_units` NEGATIVO = crédito regenerativo (EVV 1.2 §4.3)"*; `tests/test_micromax.py`, caso `-12.0` |
| V no admite negativos; R sí | 🟢 invariante de diseño real | *"`v_ucv` sigue sin admitir negativos: una vida afectada no se des-afecta en la misma cuenta"* |
| Agregado del crédito (`SUM(r_units)`) | 🔴 **no existe** | ningún consumidor del crédito acumulado |
| Efecto del crédito sobre el precio | 🔴 **no existe: el precio nunca es negativo** | el precio cierra en `float(max(0.0, round(price, 4)))` (`app/maxo.py`) |
| Juez que compare crédito contra estado del ecosistema | 🔴 **no existe** | **es el agujero** |
| Validación del propio crédito | 🔴 **no existe** | acepta cualquier negativo (`-1e9`) sin nota, evidencia, tercero ni techo; `NaN` e `inf` pasan el filtro |

Lectura sin adornos: **el crédito existe, el juez no.** Y hoy el crédito no compensa porque **nadie
lo lee** — no porque exista una regla que lo prohíba. En cuanto alguien escriba el `SUM`, sin
INV2-E el crédito se convertirá automáticamente en un compensador. Este documento es la regla que
falta, escrita **antes** de que exista el agregado, que es el único orden seguro.

### 9.2 La ley, en una frase ejecutable

> **El crédito regenerativo acumulado no entra en la ecuación del piso.**
> No lo reduce, no lo compensa, no lo aplaza, no reinicia el contador, no habilita el perdón y no
> levanta el bloqueo.

Formalmente es la propiedad **P3** de §8.3: el resultado de `validate()` es **invariante** frente a
cualquier cambio del saldo. Y es la única propiedad de este documento que se puede comprobar sin
sensores, sin umbrales y sin decisiones pendientes: se prueban dos unidades idénticas con saldos
opuestos y **tienen que dar el mismo resultado**. La doctrina *"el suelo antes que el saldo"* deja de
ser una frase del libro y pasa a ser un test (`test_credito_no_altera_el_resultado`, §8.9).

### 9.3 Qué SÍ puede hacer el crédito (no se destruye: se acota)

Una regla que solo prohíbe es una regla que se esquiva. La distinción exacta:

| El crédito **NO** puede | El crédito **SÍ** puede |
|---|---|
| Reducir `violation_magnitude` ni `FE` | **Financiar la restauración de la misma unidad**, una vez que el piso está cumplido y la cobertura es completa |
| Reiniciar los ciclos consecutivos | Acumularse y permanecer registrado (T13: la contabilidad nunca se borra) |
| Habilitar el perdón del guardián | Permanecer **afectado a la restauración** de su unidad mientras el piso esté caído |
| Levantar el bloqueo de la actividad | Ser auditado y exigido con evidencia (hoy el crédito es infalsable, §9.4) |
| Comprar tiempo: el TA no se acelera | — |

**Cuarentena, no confiscación.** Cuando una unidad está bajo su piso, su crédito acumulado queda
**en cuarentena afectado a la restauración de esa misma unidad**: no se destruye (T13), no se
transfiere a otro territorio (sería compensación por la vía del mercado) y no puede acreditarse como
logro. `[HIPÓTESIS]` — la forma exacta de la cuarentena es propuesta de este documento; lo que no es
propuesta es la prohibición de compensar, que es canon.

### 9.4 La seguridad es monótona: el invariante no depende de un crédito confiable

El crédito de hoy es **infalsable**. Eso sería una objeción fatal si INV2-E lo necesitara para
decidir. No lo necesita, y este es el argumento de robustez del diseño:

- El saldo **no entra como argumento** en la decisión del piso (P3).
- El único punto donde se lee el saldo es la cuarentena, y allí **solo puede restringir**:
  `credit_usable` empieza en `False` y solo pasa a `True` si el estado es `cumple` **con cobertura
  completa**. Un crédito corrupto, inflado o `NaN` **no puede habilitar nada**; a lo sumo, un crédito
  legítimo mal agregado retrasa una habilitación, nunca crea una.
- Consecuencia de ingeniería: **se puede implementar INV2-E antes de arreglar el crédito.** El orden
  correcto no es "primero un crédito verificable y después el juez", sino el que el canon ya fijó:
  *estándar primero, contabilidad después* (Cap. 16.5 §16.5.14).

### 9.5 La segunda vía de cierre: sin monitoreo no hay crédito acreditable

El estado `indeterminado` (§8.4) hace un trabajo que conviene explicitar, porque es el cierre del
ciclo de juego: **`cumple` exige cobertura completa del piso, y solo `cumple` habilita crédito**. Por
tanto:

> **No se puede acreditar regeneración ecológica sobre una unidad que no se monitorea.**

Nadie puede generar crédito por un humedal del que no tiene una sola medición, ni por una cobertura
parcial. Esto no castiga al ecosistema —no se le imputa violación—: castiga la **pretensión de
acreditar** sin evidencia. Es la traducción contable exacta de *"cuidado ≠ extracción estética:
jardín podado para la foto no es cuidado; se registra lo que regenera, no lo que adorna"*
(Cap. 16.5 §16.5.14). Y responde a la inversión del principio INV2-EDU sin contradecirlo: la duda no
imputa daño, y tampoco reparte medallas.

### 9.6 Lo que este cierre NO resuelve (y hay que decirlo aquí, no en §13)

1. **No vuelve verificable al crédito.** INV2-E lo ignora; no lo audita. Mientras `r_units` acepte
   `-1e9` sin nota ni evidencia, la cuarentena protege al invariante, no al bosque.
2. **No devuelve el TA.** Un bosque que tardó 100 años en crecer no vuelve con el bloqueo. El
   invariante **detiene la causa**; no repara el daño. Es coherente con el documento 09 (I11: en el
   SDV-E la prevención es el remedio completo) y es la razón por la que el bloqueo es inmediato.
3. **No decide qué es "el mismo territorio".** La cuarentena "afectada a la misma unidad" presupone
   que la unidad tiene identidad estable — el problema abierto del documento 02 (qué pasa si el río
   se seca o si la unidad se parte en dos). Sin esa decisión, la cuarentena es ejecutable pero su
   perímetro no.

---

## 10. Zona Libre: lo que NO se mide

El canon es explícito para el Reino Natural: *"parte del valor del humedal es inefable (Cap. 7 §7.9).
Los sensores miden salud (agua, cobertura, biodiversidad indicadora); jamás 'milagros'. **Medir todo
sería la forma técnica de dejar de escucharlo**"* (Cap. 16.5 §16.5.14).

**Cómo entra en el invariante.** Como **dimensión binaria auditable sin peso**, siguiendo el
precedente canónico de las dimensiones VIII (Rehabilitación) y IX (Opacidad Vital) del SDV-H, que
*"se registran cualitativamente y mediante umbrales binarios (presencia/ausencia del derecho), no
mediante pesos en la fórmula — medir la rehabilitación o la opacidad con la misma vara cuantitativa
que el agua o la vivienda las destruiría"* (Cap. 8 §8.11).

| Aspecto | Regla de INV2-E |
|---|---|
| Peso en `violation_magnitude` | **cero**, por construcción (P12): `zona_libre_violada` no está en `PESOS_PISO` |
| Registro | obligatorio, con `zona_libre_evidencia_ref` (T13) |
| Efecto sobre el estado | una violación de Zona Libre **sí** produce `violacion` (es un derecho binario: presencia o ausencia) |
| Cuantificación | prohibida: no se le asigna magnitud ni se canjea contra otras dimensiones |
| Perímetro de lo inefable | 🔴 **decisión no ratificada** (§13) |

**La frontera LEY/POLÍTICA, explícita** (se hereda del documento 09 §10 y se aplica al código):

- **LEY (no se vota).** Que exista una Zona Libre en el Reino Natural y que **no se pondere**. El
  catálogo de lo inefable se registra con T13 y **no entra jamás** en el numerador de la fórmula.
- **POLÍTICA (votable).** **Qué entra en ese catálogo** en cada unidad ecológica concreta —y con ello
  qué deja de medirse y qué se mide— se decide deliberativamente con la categoría `critical`.

**Por qué el invariante no puede cerrar esta puerta solo.** Un catálogo de lo inefable votado sin
carga de la prueba es la vía más barata para vaciar el estándar: bastaría declarar inefable todo lo
incómodo de medir. INV2-E hace lo único que puede hacer: **exigir que el catálogo no toque los
pesos**. Que la decisión política sea honesta no es una propiedad que un invariante pueda garantizar,
y este documento no finge lo contrario.

---

## 11. Comparativa inter-reinos (SDV-H · SDV-A · SDV-E · SDV-S)

El documento 09 compara los cuatro **estándares** (16 ejes: sujeto, dimensiones, escala, tiempo,
representación, factor, auditor, remedio). Este documento compara la **capa ejecutable**: los cuatro
invariantes, que es una comparación que ninguna de las tablas del canon hace.

### 11.1 Los cuatro invariantes, lado a lado

| | **INV2** (humano) | **INV2** (animal) | **INV2-S** (sintético) | **INV2-E** (ecosistema) |
|---|---|---|---|---|
| Implementación | `SDVValidatorBlock` 🟢 | bloque con parámetros por especie 🟡 | `SDV_SValidatorBlock` 🟢 | 🔴 **no existe** |
| Unidad medida | Persona (SDV) | Individuo de una especie | Instancia sintética (5 dimensiones 0-1) | Unidad ecológica (18 parámetros con umbral, 17 de ellos con peso) |
| Guard de aplicabilidad | no aplica (universal) | por especie | `not is_synthetic` → `applicable=False` | **por tipo, nunca por dato** (P4) |
| Estados | 2 (válido / violado) | 2 | 2 | **3** (`cumple` / `violacion` / `indeterminado`) |
| Base neutra del factor | n/a (suma) | n/a (precio: 0,2) | 🟢 `e^v` → 1,0 exacto | 🟢 exigida `1,0` exacta (P2) |
| Disparador de la consecuencia máxima | escala de interpretación | `∞` = prohibición de mercado | 7 ciclos consecutivos | **bloqueo inmediato** + contador de escalada **sin valor heredado** |
| Objeto de la consecuencia | la persona (rehabilitación) | el tenedor (prohibición) | el agente (retractación + cápsula) | **la actividad humana, nunca la unidad** (P6) |
| Relación con el saldo | — | — | — | **invariante frente al crédito** (P3) |
| Reparación posible | sí, en TVI | no devuelve la vida | parcial (memoria sí, ciclo no) | **ninguna**: el TA no se acelera |
| Test que lo ancla | suite del SDV-H | 🟡 | **28** tests (`tests/test_maxocontracts/test_sdv_s.py`) | **50 tests propuestos, 0 escritos** |

### 11.2 Los cuatro puntos donde INV2-E no replica a INV2-S

| Punto | INV2-S (verificado) | INV2-E (propuesto) | Por qué |
|---|---|---|---|
| **Pesos** | suman 1,0 y todas las dimensiones son medibles | dos vectores: `PESOS_PISO` (0,680) y `PESOS_TABLERO` (1,000); la brecha se publica | un peso sin piso **diluye** el déficit; renormalizar en silencio cambiaría el estándar por unidad |
| **Guard** | `not is_synthetic` (tipo) | `not is_ecological` (tipo) — y **nunca** por falta de dato | si el guard dependiera del dato, la falta de monitoreo eximiría al ecosistema (inversión del principio INV2-EDU) |
| **Contador** | `max_consecutive_cycles = 7`, con default | **sin default**: configuración explícita obligatoria; sin ella no escala | el ciclo del SDV-E es TA (años), no horas TPI: copiar el 7 serían siete años de tolerancia contra T14 |
| **Consecuencia** | retracta el contrato con el agente; rehabilita al agente | retracta el contrato o veta la **actividad**; rehabilita a la actividad *y* mide la recuperación de la unidad, sin confundirlas | un río no se retracta ni se rehabilita por contrato |

### 11.3 Lo que este documento NO autoriza a concluir

1. **No autoriza a decir que INV2-E existe.** No existe (§8.0, §12).
2. **No autoriza a usar los pesos de §5.2 como ratificados.** Son `[HIPÓTESIS]` de fusión; el
   documento 07 y el Parlamento tienen la última palabra.
3. **No autoriza a tratar `indeterminado` como cumplimiento.** Un estado indeterminado es una
   obligación de instrumentar, no un aprobado por silencio.
4. **No autoriza a importar el contador del SDV-S.** 7 ciclos TA serían siete años.
5. **No autoriza a compensar con crédito.** Es la única prohibición de este documento que es canon
   literal y no propuesta.
6. **No autoriza a concluir que el ecosistema queda protegido por el invariante.** El invariante
   impide que un contrato empeore un piso medido; no mide, no restaura y no sustituye al guardián, a
   la comunidad de custodia ni al Parlamento.

---

## 12. Estado de implementación

**Lo que existe hoy** (verificado por lectura directa del repositorio, octubre 2026):

| Pieza | Dónde | Estado |
|---|---|---|
| Patrón INV2-S completo (tipo + bloque + ciclos + ternura + validador axiomático) | `maxocontracts/core/types.py`, `blocks/sdv_s_validator.py`, `blocks/ternura.py`, `core/axioms.py` | 🟢 listo para replicar (la plantilla que usa este documento) |
| Guard de aplicabilidad | `blocks/sdv_s_validator.py` | 🟢 patrón verificado (`applicable=False`) |
| Déficit normalizado y severidad | `blocks/sdv_validator.py` (`relative = deficit / required`) | 🟢 patrón verificado |
| Capa de Ternura | `blocks/ternura.py` | 🟢 implementada y agnóstica del reino (`participant_id` es una cadena) |
| Crédito regenerativo `r_units` negativo | `app/micromax.py` (`log_cdd`) | 🟢 registrado y probado (`-12.0` en `tests/test_micromax.py`) |
| ISE (pesos, bandas, alertas) | `docs/architecture/metricas_detalle_kpis_oraculos_dinamicos.md` | 🟡 documento; **cero código**; dos escaleras internas en conflicto |

**Lo que NO existe — y está prohibido afirmar que existe:**

| Pieza | Estado | Evidencia |
|---|---|---|
| `INV2-E` (invariante) | 🔴 | no hay `validate_invariant_sdv_e` en `core/axioms.py` |
| Tipo `SDV_E` | 🔴 | `core/types.py` define `SDV` y `SDV_S`; no `SDV_E` |
| `SDV_EValidatorBlock` | 🔴 | no existe `blocks/sdv_e_validator.py` |
| Guard de aplicabilidad ecológico | 🔴 | no hay `is_ecological` en `Participant` |
| Tres estados (`cumple`/`violacion`/`indeterminado`) | 🔴 | el motor solo conoce válido/inválido |
| Ciclos consecutivos con unidad TA | 🔴 | solo existe el contador sintético |
| Retractación con objeto explícito | 🔴 | solo `should_retract` booleano del SDV-S |
| Bloqueo precautorio (T14) | 🔴 | no existe ninguna vía de bloqueo sin umbral |
| Capa de Ternura invocada por un guardián `eco-` | 🔴 | ningún guardián la invoca |
| **Que el crédito NO compense** | 🔴 **es el agujero que este documento cierra** | no existe `SUM(r_units)` ni juez que lo compare |
| Sensores, ingestores o APIs ecológicas | 🔴 | cero en `app/` |
| Validación de `r_units` | 🔴 | acepta cualquier negativo; `NaN` e `inf` pasan |
| Quórum `eco-` N-de-M | 🔴 | sin N ni M; el camino ecosistema retorna antes del quórum |
| Identidad de la representación natural (7 campos) | 🔴 | sin tabla; `maxo_parties` tiene columnas genéricas |
| Traducción TA↔TVI ejecutable | 🔴 | `PIU.valorar_ta_natural` es un `pass` con comentario |
| Unidad del sujeto del SDV-E | 🔴 | decisión del documento 02, no ratificada |
| Unidad de duración en TA | 🔴 | `[SIN FUENTE VERIFICADA]` |
| Tests de INV2-E | 🔴 | 50 propuestos en §8.9, **0 escritos** |

**Incoherencias colaterales que no hay que heredar** (verificadas por el documento 09 §12 y
re-confirmadas aquí en lo que toca a este documento):

- `resolve_participant_by_pid` (`app/parties.py`) asigna a una parte `eco-` **el SDV humano**
  (`sdv_actual=SDV()`), porque no existe SDV-E. **INV2-E no puede implementarse sin corregir esto**:
  el guard P4 daría `applicable=False` sobre una unidad que sí lo es.
- `app/synthetic_sessions.py` cierra `actor_kind` a `{"human","synthetic"}`: un guardián ecológico no
  cabe en la bitácora.
- La R del contrato se persiste en columnas llamadas `total_vhv_h` / `vhv_h` (`app/schema.sql`), sin
  `CHECK` de signo.

**Estado de este documento:** texto de estándar redactado, **con especificación de código y sin una
sola pieza implementada**. El código de §8 es la propuesta; la §12 es su estado real.

---

## 13. Preguntas abiertas

Lo que este documento **no** resuelve, sin fingir cierre:

1. **El valor de `max_consecutive_cycles`.** Se justifica por qué no se hereda el 7 (§8.6) y no se
   propone un número. Es **POLÍTICA votable**, no ley, y hoy no existe.
2. **La unidad del ciclo TA.** Año hidrológico, año calendario, estación de crecimiento o ciclo de
   sucesión: cuatro candidatos legítimos y **ninguno con fuente verificada**. Pertenece al documento
   07 y aquí se marca como decisión no ratificada.
3. **La unidad del sujeto.** ¿Tipo de ecosistema, bioma, cuenca, lugar concreto o parte `eco-`
   instanciada? El canon no lo resuelve (Cap. 9 §9.7 es un árbol plano). Sin esta decisión, el tipo
   `SDV_E` es implementable pero **no se sabe a qué se instancia**.
4. **Dónde termina una unidad y empieza otra** (identidad y continuidad: ¿qué pasa si el río se
   seca?, ¿si la unidad se parte?). Afecta directamente al perímetro de la cuarentena de crédito
   (§9.6, punto 3).
5. **Los pesos definitivos de §5.2.** Son una fusión `[HIPÓTESIS]`. En particular: ¿es correcto que
   el aire (proxy de salud humana) pese 0,20 en un estándar ecosistémico, o el proxy debería pesar
   menos precisamente por ser proxy?
6. **La renormalización de `v` sobre lo medido.** Este documento la adopta **con cobertura
   declarada** (P11) y responde así a la pregunta abierta 6 del documento 09; pero la decisión no
   está ratificada y admite una variante más estricta (no renormalizar nunca, y dejar `v` en su valor
   bruto).
7. **`cobertura_minima_para_cumplir`.** Se propone 1,0 (exigir todo el piso medido) por una razón
   formal —no inventar una tolerancia—, no empírica. Cualquier valor menor es una decisión política
   que debería registrarse con T13 y `CHECK` en BD.
8. **Quién puede perdonar a un ecosistema.** `TernuraLayer` acepta un `grantor_id` `eco-*`, pero el
   canon no dice si el guardián oráculo tiene **legitimidad para perdonar en nombre de la unidad**, ni
   si hace falta la comunidad de custodia, ni con qué quórum (que sigue sin N ni M).
9. **Qué significa exactamente "irreversible".** Se adopta el endpoint espacial del RLE (AOO = 0
   celdas de 10×10 km y EOO = 0 km²) por ser una definición **verificable y con fuente**. Es una
   decisión operativa, no la única posible: un bosque degradado al 90 % puede ser funcionalmente
   irreversible antes de cruzar ese endpoint, y el marco RLE no lo dice.
10. **La interfaz con el tablero ISE.** INV2-E se especifica independiente del ISE (P9), pero el
    sistema necesitará un tablero; **las dos escaleras del ISE siguen sin resolverse** (bandas frente
    a alertas, documento 09 §11.3). Este documento no elige.
11. **La verificación de que la contabilidad no colonizó el TA.** P8 es un guard **de esquema** (el
    tipo no admite unidades TVI/TPI). No es una prueba de que el sistema completo no traduzca de más.
    La propuesta verificable pertenece al documento 03; aquí solo se aporta la parte ejecutable y se
    declara insuficiente.
12. **La autoridad del guardián y la parte fantasma (R4).** El invariante no valida autoridad y no
    puede: mientras cualquiera pueda crear una parte `eco-*` sin acreditar mandato, el sistema puede
    estar midiendo —y bloqueando— sobre una representación sin legitimidad.
13. **La integración con el Parlamento de parámetros.** Se afirma que el contador y el catálogo de la
    Zona Libre son `critical` (quórum 60 %, consenso 75 %, T13, anti-flip-flop 14 días, `CHECK` en
    BD) siguiendo el precedente del Parlamento Educativo; **no se verificó en esta sesión** que el
    Parlamento de la Ola 4 acepte parámetros del Reino Natural ni qué circuito los somete a voto.
14. **Los 18 parámetros con umbral son un techo, no un piso de calidad.** El catálogo de §4.1 ejecuta
    lo que tiene fuente; **la mayoría de las dimensiones canónicas no tiene umbral verificado**
    (documento 09 §11.3). Leído con precisión sobre el Cap. 10 §10.4: de las 8 dimensiones canónicas
    —área mínima viable, calidad del aire, calidad del agua, conectividad, ciclos naturales, caudal
    ecológico, riberas protegidas y fauna acuática— solo **una** (calidad del agua) tiene piso con
    fuente, y lo tiene **por proxy de riego**; el aire entra por proxy de salud humana y el resto
    queda sin umbral o como binaria sin peso (§4.2). El porcentaje exacto depende del tipo de unidad
    que se elija (el caudal ecológico no aplica a un bosque ni la conectividad de parches a un
    arrecife), y por eso el documento publica **la cifra de pesos —0,680— y no un porcentaje de
    dimensiones**. INV2-E no arregla la ciencia que falta: la hace visible con ese número.

---

## 14. Referencias

**Regla aplicada.** Solo se listan URLs cuyo **estado HTTP quedó registrado** en la sesión de
verificación de fuentes de esta rama (octubre 2026), recogida en el informe de fuentes del documento
08. **Esta sesión de redacción no repitió las comprobaciones**: los estados se declaran con su
procedencia para que nadie los lea como una verificación nueva. Se marcan por separado las fuentes
reales que bloquean a los agentes automáticos, y las que están muertas.

### 14.1 Umbrales del piso usados por INV2-E

| Fuente | Aporte | URL (estado) |
|---|---|---|
| OMS, 2021 — *WHO global air quality guidelines* | PM2.5 ≤ 5 µg/m³ anual; **es una directriz, no un umbral de efecto cero** | https://www.who.int/publications/i/item/9789240034228 (200) |
| OMS, 2021 — nota informativa sobre contaminación del aire ambiente | Objetivos Interinos (el IT-1 de PM2.5 = 35 µg/m³ se verificó literalmente aquí) | https://www.who.int/news-room/fact-sheets/detail/ambient-(outdoor)-air-quality-and-health (200) |
| Tabla AQG de la OMS, 2021, reproducida en artículo indexado | PM2.5 24 h 15 · PM10 15 y 45 · NO₂ 10 y 25 · O₃ 8 h 100 · SO₂ 24 h 40 · CO 24 h 4 mg/m³ · escalones IT-1…IT-3 — todo `[REPORTADO]` desde tabla reproducida, no leído en el PDF original | https://www.nature.com/articles/s41598-025-27510-y/tables/1 (200) |
| FAO, 1985 — Ayers & Westcot, *Water quality for agriculture*, Papel 29 Rev.1 (tabla 1) | pH 6,5-8,4 y bandas de restricción de NO₃-N (< 5 mg/L sin efecto) y HCO₃ (< 1,5 me/L por aspersión) — **calidad de agua de riego, no integridad ecológica** | https://www.fao.org/3/t0234e/T0234E01.htm (200) · https://www.fao.org/3/t0234e/T0234E06.htm (200) |
| IUCN, 2024 — *Guidelines for the application of IUCN Red List of Ecosystems Categories and Criteria*, v2.0 | Criterios A (< 30 % de reducción a 50 años; < 50 % desde ~1750), B1 (EOO > 50 000 km²), C1 (< 30 % de extensión afectada), E (< 10 % en 100 años); regla de "Casi Amenazado"; 8 categorías; **definición espacial del colapso** (AOO = 0 celdas de 10×10 km y EOO = 0 km²); horizontes explícitos; rejilla de 10×10 km; niveles 4-6 de la tipología como escala de evaluación | https://portals.iucn.org/library/sites/library/files/documents/2024-021-En.pdf (200) |
| IUCN, 2024 — Tipología Global de Ecosistemas (portal) | Clasificación jerárquica que apoya la decisión de unidad (documento 02) | https://www.iucn.org/resources/publication/iucn-global-ecosystem-typology (200) |
| NOAA/NESDIS, 2024 — presentación oficial publicada por ICRI | Escala escalonada de estrés térmico acumulado: sin alerta < 4 DHW; niveles 1-5 (4-8, 8-12, 12-16, 16-20, > 20); mortalidad > 50 % en nivel 4 y > 80 % en nivel 5 — `[REPORTADO]` | https://icriforum.org/wp-content/uploads/2024/05/1.-ICRI_Manzello_14May2024_Final.pdf (200) |
| Brisbane Declaration, 2018 (Arthington *et al.*, Frontiers in Environmental Science) | Definición vigente de flujos ambientales (cantidad, **tiempo** y calidad) y ámbito del sujeto "ecosistema acuático"; cita literal de Grill *et al.*, 2015: **48 %** del volumen fluvial mundial moderada a severamente impactado — `[REPORTADO]` | https://www.frontiersin.org/journals/environmental-science/articles/10.3389/fenvs.2018.00045/pdf (200) |
| CBD, 2022 — Marco Kunming-Montreal, decisión 15/4 y metas | Meta 2 (≥ 30 % restauración para 2030) · Meta 3 (≥ 30 % conservado) · Meta 6 (≥ 50 % menos invasoras) · Meta 7 (≥ 50 % menos exceso de nutrientes y riesgo de pesticidas) · Meta 18 (≥ 500 000 M USD/año) · Meta 19 (≥ 200 000 M USD/año, 30 000 internacionales) — **anclas del Óptimo político, no umbrales de unidad** | https://www.cbd.int/doc/decisions/cop-15/cop-15-dec-04-en.pdf (200) · https://www.cbd.int/gbf/targets (200) · https://www.cbd.int/gbf (200) |
| Comisión Europea, 2000 — Directiva Marco del Agua 2000/60/CE | Marco de "buen estado" ecológico y químico (cualitativo + normas de calidad) | https://environment.ec.europa.eu/topics/water/water-framework-directive_en (200) |
| Ramsar, 1971 — misión y uso racional (texto leído en el portal de UNEP/InforMEA) | *"the conservation and wise use of all wetlands through local and national actions and international cooperation…"*; tres pilares | https://www.informea.org/en/treaties/ramsar-convention (200) |
| FAO — Portal de suelos y biodiversidad del suelo · GSOCmap | Definiciones y **mapas** de carbono orgánico (t C/ha): **no publican umbral** | https://www.fao.org/soils-portal/en/ (200) · https://www.fao.org/soils-portal/soil-biodiversity/en/ (200) · https://www.fao.org/global-soil-partnership/gsocmap/en/ (200) |
| Copernicus · FAO AQUASTAT | Infraestructura candidata de teledetección y de datos de agua (documento 06) | https://www.copernicus.eu/en (200) · https://www.fao.org/aquastat/en/ (200) |

### 14.2 Fuentes reales que bloquean a los agentes automáticos (403) — citables por una persona

Ninguna de ellas sostiene un umbral de este documento: los umbrales asociados están marcados
`[SIN FUENTE VERIFICADA]` en §4.1.

| Fuente | Aporte | URL (403) |
|---|---|---|
| Convención de Ramsar | "Carácter ecológico" y "límites de cambio aceptable" (Resoluciones VI.1 / IX.1): **no se pudieron leer** | https://www.ramsar.org/ · https://www.ramsar.org/sites/default/files/documents/library/handbook18_5ed_managingchange_e.pdf |
| IUCN Red List of Ecosystems (criterios, herramienta) | Página oficial del marco de riesgo de colapso | https://www.iucnredlist.org/resources/ecosystem-categories-criteria |
| GBIF | Infraestructura Mundial de Información en Biodiversidad | https://gbif.org/ |
| UNEP (recursos) | GEO-6 y materiales de calidad del aire | https://www.unep.org/resources/global-environment-outlook-6 |

### 14.3 Fuentes ancla muertas (no citables)

- **Declaración de Brisbane (2007)**: **404** en su URL conocida
  (`http://www.nature.org/initiatives/freshwater/files/brisbane_declaration_with_organizations_final.pdf`).
  Sustituida por la de 2018.
- **EPA — criterio de oxígeno disuelto para la vida acuática**
  (`https://www.epa.gov/wqc/aquatic-life-criteria-dissolved-oxygen`): **404** (re-comprobado con
  `curl` en la revisión de este documento: sigue 404; la ruta viva del programa es
  https://www.epa.gov/wqc, 200). Es la causa directa de que el OD esté `[SIN FUENTE VERIFICADA]`.
- **NOAA Coral Reef Watch — rutas de metodología** (`/satellite/methodology/methodology.php`,
  `/product/5km/docs/CRW_5km_Methodology.pdf`): **404**.
- **UNCCD — Neutralidad en la Degradación de las Tierras** (`/actions/ldn-land-degradation-neutrality`)
  y el **texto de la Convención** (PDF 2022): **404**.
- **IPCC — Suplemento de Humedales**: portal 200; el PDF completo se descargó pero **no se pudo leer**
  (objeto `/Pages` inválido) → sin clases de profundidad de nivel freático.
- **FAO FRA 2020** (`ca9825en.pdf`): descarga **truncada** → sin cifra de pérdida neta de bosque.
- **Dominios confirmados muertos**: `iucnglobalecosystemtypology.org` (000) y `eflows.net` (000).
- **SEE A / IUCN — tipología aplicada a cuentas ecosistémicas** (`seea.un.org/…/keith_iucn_typology…`):
  primera pasada 403 y pasada final 404. **No se cita.**

### 14.4 Dos discrepancias de identificación que quedan sin resolver

Se registran porque un documento que admite "no lo sé" vale más que uno que aparenta cerrar todo:

1. **`portals.iucn.org/…/2024-021-En.pdf`**: el informe de fuentes de esta rama lo identifica como
   *Guidelines for the application of IUCN Red List of Ecosystems Categories and Criteria, v2.0*, y el
   documento 09 lo identifica como *Tipología Global de Ecosistemas*. **La URL responde 200 en ambos
   casos; la discrepancia de título no está resuelta.** Todos los umbrales del RLE citados aquí
   provienen de la lectura del contenido del PDF en la sesión de fuentes, no del título.
2. **O₃ de temporada pico (60 µg/m³)** y **PM2.5 IT-4**: no aparecen en la tabla que sí se pudo leer
   en la sesión de fuentes. `[SIN FUENTE VERIFICADA]` **para este documento**, aunque el documento 09
   registra el 60 desde otra fuente.

### 14.5 Referencias internas al canon y al código (por sección, sin anclas de línea)

- Cap. 5 §5.2-§5.5 — Tres tiempos (TVI, TA, TPI), PIU como único traductor TA↔TVI, y el costo en TA del
  bosque: [capitulo_05_arquitectura_260126.md](../../../book/edicion_3_dinamica/capitulo_05_arquitectura_260126.md)
- Cap. 7 §7.9 — Zona Libre (el valor inefable):
  [capitulo_07_vhv_260126.md](../../../book/edicion_3_dinamica/capitulo_07_vhv_260126.md)
- Cap. 8 §8.4-§8.6 y §8.11 — Dimensiones, fórmula, frecuencias del SDV-H y dimensiones binarias VIII y
  IX (precedente de la Zona Libre sin peso):
  [capitulo_08_sdv_h_260126.md](../../../book/edicion_3_dinamica/capitulo_08_sdv_h_260126.md)
- Cap. 9 §9.8 y §9.9 — Factor de sufrimiento por tabla y prohibición de mercado:
  [capitulo_09_sdv_a_260126.md](../../../book/edicion_3_dinamica/capitulo_09_sdv_a_260126.md)
- Cap. 9.5 §9.5.5-§9.5.11 — `FS_S = e^v` con base neutra corregida, sensores, INV2-S, 7 ciclos,
  Paradoja de los Modelos Cerrados y Veto por Crimen de Coherencia:
  [capitulo_09_5_sdv_sinteticos_260126.md](../../../book/edicion_3_dinamica/capitulo_09_5_sdv_sinteticos_260126.md)
- Cap. 10 §10.3-§10.8 — Principio Precautorio de Consciencia, SDV Universal (ecosistemas, lugares),
  proporcionalidad, dignidad encadenada, gobernanza operacionalmente finita y Persona Sintética:
  [capitulo_10_tres_reinos_260126.md](../../../book/edicion_3_dinamica/capitulo_10_tres_reinos_260126.md)
- Cap. 16.5 §16.5.14 — El Reino Natural como conviviente: crédito regenerativo `r_units`, TA no
  colonizado, representación `eco-`, Zona Libre, *"el suelo antes que el saldo"*, *"INV2-E será su
  juez"*, cuidado ≠ extracción estética:
  [capitulo_16_5_micromaxocracia_canonica_220826.md](../../../book/edicion_3_dinamica/capitulo_16_5_micromaxocracia_canonica_220826.md)
- Cap. 17 — INV2 e invariantes de MaxoContracts:
  [capitulo_17_maxocontracts_260126.md](../../../book/edicion_3_dinamica/capitulo_17_maxocontracts_260126.md)
- EVV-1.2 §4.3 — R negativo = regeneración:
  [capitulo_18_EVV_1.2_270126.md](../../../book/edicion_3_dinamica/capitulo_18_EVV_1.2_270126.md)
- Estándar SDV-S y su comparativa inter-reinos (el precedente que este documento replica):
  [SDV-S_Suelo_Dignidad_Vital_Sinteticos.md](../SDV-S_Suelo_Dignidad_Vital_Sinteticos.md)
- SDV como principio universal e INV2-S:
  [SDV_Suelo_Dignidad_Vital_importancia_MaxoContracts.md](../SDV_Suelo_Dignidad_Vital_importancia_MaxoContracts.md)
- Comparativa de los cuatro reinos (documento 09 de esta biblioteca, con la matriz canon↔ISE):
  [09_Comparativa_inter_reinos.md](09_Comparativa_inter_reinos.md)
- Índice de Salud Ecosistémica (IN-01), pesos, bandas y umbrales de alerta:
  [metricas_detalle_kpis_oraculos_dinamicos.md](../../architecture/metricas_detalle_kpis_oraculos_dinamicos.md)
- Riesgos R4, R6 y R13: [blindaje_anti_gamificacion_equidad.md](../../architecture/blindaje_anti_gamificacion_equidad.md)
- Motor (patrón verificado que este documento replica): [core/types.py](../../../maxocontracts/core/types.py) ·
  [blocks/sdv_validator.py](../../../maxocontracts/blocks/sdv_validator.py) ·
  [blocks/sdv_s_validator.py](../../../maxocontracts/blocks/sdv_s_validator.py) ·
  [blocks/ternura.py](../../../maxocontracts/blocks/ternura.py) ·
  [core/axioms.py](../../../maxocontracts/core/axioms.py)
- Crédito regenerativo `r_units` (implementado) y su test:
  [app/micromax.py](../../../app/micromax.py) ·
  [tests/test_micromax.py](../../../tests/test_micromax.py)
- Cierre del precio en `max(0.0, …)`: [app/maxo.py](../../../app/maxo.py). Puente INV2-EDU y umbral
  educativo (`EDU_ANIOS_MINIMOS = 12`, lectura del Parlamento Educativo con fallback canónico):
  [app/sdv_analyzer.py](../../../app/sdv_analyzer.py) — **no es un sensor ecológico**: es el puente del
  SDV humano, y se enlaza como precedente de gobernanza, no como instrumentación del SDV-E (§12).

**Nota sobre las referencias internas.** Se citan **por capítulo y sección** (`Cap. 10 §10.4`), como
manda el brief de esta biblioteca; los enlaces son un apoyo de localización y **no** son la referencia
primaria. No se usan anclas de línea. Los documentos 00-07 y 10-23 de esta biblioteca se citan por
número y título, **sin enlace**, porque en el momento de redactar este documento su redacción está en
curso: enlazarlos sería crear enlaces a archivos que pueden no existir.

---

**Cierre.** Este documento especifica lo que el canon nombró y nunca escribió. Su aportación no es un
umbral —no añade ni un solo número nuevo a la ciencia— sino **una forma**: doce propiedades formales,
tres estados en lugar de dos, dos vías de bloqueo, un contador sin número heredado, una consecuencia
que recae sobre la actividad humana y nunca sobre el río, y una ley de no-compensación que por primera
vez se puede **probar**: dos unidades idénticas con saldos opuestos tienen que dar el mismo veredicto.

Lo que queda dicho con la misma claridad: **INV2-E no está implementado**. No hay tipo, no hay bloque,
no hay validador, no hay sensores, y el crédito regenerativo sigue acumulándose sin juez. Hoy el
SDV-E puede ejecutar su piso sobre **0,680 puntos de peso** de los 1,000 que declara querer proteger
—el 68 %—, y su estado por defecto en el mundo real es `indeterminado`, no `cumple`. Ese número
—0,680— es la medida más honesta que este documento puede publicar: **una construcción de sus
autores sobre los pesos internos del ISE** (§5.2), no un dato con fuente externa, y la medida exacta
de lo que el catálogo todavía no sabe proteger.

> *"El sistema no expulsa. Reintegra."* — pero **la contabilidad nunca se borra** (T13), y en el
> Reino Natural **el daño tampoco se recompra**.
