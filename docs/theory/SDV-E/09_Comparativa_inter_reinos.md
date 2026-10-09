# Comparativa inter-reinos: SDV-H · SDV-A · SDV-E · SDV-S
## Los mínimos de los cuatro reinos, lado a lado: qué comparten, qué no se puede transferir y qué aprende el SDV-E de cada uno

**Autoría:** Oráculo Sintético DeepSeek & Max Nelson López Restrepo
**Fecha:** octubre 2026
**Proyecto:** Maxocracia — El gobierno de la verdad, el tiempo y la vida
**Licencia:** Creative Commons BY-SA 4.0
**Estado:** Propuesta de estándar (rama SDV-E, Ola 4) — NO canon hasta ratificación
**Referencia canónica:** Cap. 10 §10.4 · Cap. 16.5 §16.5.14 · EVV-1.2 §4.3 · Cap. 9.5 (precedente SDV-S)
**Documento:** 09 de la biblioteca `docs/theory/SDV-E/`
**Revisión:** octubre 2026 — revisión adversaria aplicada (déficit normalizado, protocolo de medición
declarado ausente, frontera LEY/POLÍTICA de la Zona Libre, cifras del reino humano degradadas a
`[REPORTADO]`, rutas internas al canon corregidas). Las correcciones no cambian las tesis del
documento: cambian su trazabilidad.

---

## 1. Qué es (y qué no es) este SDV

**Qué es.** Este documento no fija umbrales ecológicos nuevos: **compara los cuatro estándares de
Suelo de Dignidad Vital que el canon reconoce** —humanos, animales, ecosistemas y sintéticos— eje
por eje, y extrae de esa comparación las decisiones que el SDV-E no puede tomar por sí solo. Es el
documento que responde a la pregunta *"¿en qué se parece y en qué no se parece el suelo de un río al
suelo de una persona?"* con una tabla y no con una metáfora.

Existe porque el canon ya escribió los cuatro estándares en el mismo árbol —el árbol plano del
Cap. 9 §9.7 (`SDV-H`, `SDV-A`, `SDV-E`, `Procesos`)— y ya escribió tres tablas comparativas
parciales: la del Cap. 9 §9.9 (H frente a A), la del Cap. 9.5 §9.5.11 (H, A, S) y la del documento
[SDV-S](../SDV-S_Suelo_Dignidad_Vital_Sinteticos.md) §6. **Ninguna de las tres incluye al
SDV-E**, porque el SDV-E no existía; y ninguna de las tres compara invariantes, factores de
violación ni representación.

**Qué no es.**

- **No es el estándar del SDV-E.** El estándar vive en los documentos 00-08 de esta biblioteca; este
  documento es su control de coherencia externo. Donde la comparación fuerza una decisión, se dice
  cuál y se marca como **propuesta no ratificada**.
- **No es un documento de umbrales.** Ninguna cifra de este documento se propone como piso del
  SDV-E. Todas provienen de fuentes externas ya verificadas o del canon interno.
- **No es una jerarquía de dignidad.** El Cap. 10 §10.5 fija el **Principio de Proporcionalidad**:
  *"No tratamos a una cuchara igual que a un humano, pero ambos merecen condiciones apropiadas para
  su funcionamiento."* Comparar no es ordenar por importancia; es detectar qué estructura es común y
  qué estructura es específica.
- **No es canon.** Es una propuesta de estándar de la rama SDV-E, Ola 4.

**Nota de lectura.** Este documento pertenece a una biblioteca que se redacta por bloques. Cuando
necesita una cifra que pertenece a otro documento de la misma biblioteca (unidad y sujeto en el 02,
fórmula y pesos en el 07, INV2-E en el 08), lo declara, la marca como **propuesta de este documento**
y **no la presenta como si ya estuviera ratificada**.

**Marcas de evidencia usadas en todo el texto.** `[VERIFICADO]` = comprobado con herramienta o
leído en el archivo citado. `[REPORTADO]` = afirmado por una fuente que cito sin haber podido abrir
el documento completo. `[HIPÓTESIS]` = inferencia razonada del proyecto, no observación.
`[SIN FUENTE VERIFICADA — pendiente de consenso científico]` = busqué el umbral y no existe fuente
verificable. Las cuatro marcas son resultados legítimos.

---

## 2. Preámbulo metodológico

El SDV-H lo tiene; el SDV-S lo omitió y el brief de esta biblioteca prohíbe repetir la omisión.
Aquí el preámbulo es doblemente necesario, porque **comparar es una operación que introduce errores
propios**:

**Regla 1 — Fijar los ejes antes de leer las celdas.** Una tabla comparativa entre estándares es
honesta solo si los ejes se declaran antes de rellenarla. Este documento usa **10 ejes obligatorios**
—para quién, qué protege, dimensiones, escala, unidad de medida, moneda temporal, representación,
invariante, factor de violación y estado— más **6 ejes que la comparación reveló como necesarios**:
voz del sujeto, unidad de duración de la violación, base neutra del factor, quién audita, remedio
tras la violación y origen del piso. Los 6 ejes añadidos son un aporte de este documento: ninguno
aparece en las tres tablas comparativas del canon.

**Regla 2 — Ningún umbral cruza de reino.** Un piso de 20 L/persona/día (agua de bebida humana,
`[REPORTADO]` desde el brief §2.1: **este documento no tiene URL verificada para esa cifra en su §14**)
no es un piso de caudal ecológico; un pH admisible para la vida acuática no es un pH admisible para
agua potable. La comparación sirve para ver la *estructura*, jamás para trasvasar cifras.

**Regla 3 — La celda vacía es un hallazgo, no un hueco de redacción.** Cuando un eje no tiene valor
en un reino, se escribe 🔴 y se dice por qué. Ocultarlo convertiría esta tabla en publicidad.

**Regla 4 — Distinguir "no existe" de "no lo sé".** Cuatro cosas distintas se marcan distinto:
(a) no existe en el canon; (b) existe en el canon y no en el código; (c) existe la fuente externa y
no la verifiqué; (d) busqué y no hay fuente. Las cuatro aparecen aquí y ninguna se disfraza de otra.

**Regla 5 — El estándar se compara con el estándar.** El estado de implementación es una sección
aparte (§12) precisamente para que la comparación doctrinal no se contamine con el estado del
código.

**Regla 6 — Descripción, no recomendación, hasta que se diga lo contrario.** Todo lo que en este
documento sea propuesta va marcado `[HIPÓTESIS]` o **propuesta no ratificada**.

---

## 3. Pilares epistemológicos

Los cuatro estándares comparten cinco pilares, y el SDV-E hereda los cinco:

1. **Proporcionalidad (Cap. 10 §10.5).** El nivel de protección debe ser *"lógico, proporcional y
   adecuado a la naturaleza de la entidad"*. Esta es la cláusula que hace legítima la comparación:
   los cuatro reinos no reciben el mismo trato, reciben el trato que su naturaleza exige.
2. **Dignidad encadenada (Cap. 10 §10.6).** *"Dignidad Humana ←→ Dignidad Ecosistémica ←→ Dignidad
   Material. Cada eslabón depende de los demás."* Consecuencia dura para este documento: si el
   eslabón ecosistémico cae, el humano cae — la comparación no es altruismo, es contabilidad propia.
3. **Precaución ante quien no puede consentir.** El **Principio Precautorio de Consciencia**
   (Cap. 10 §10.3) y el **T14 — Principio de Precaución Intergeneracional** (Cap. 5): *"Ante
   incertidumbre sobre el impacto en agentes que no pueden consentir (ecosistemas, generaciones
   futuras, posibles consciencias sintéticas), el sistema debe elegir la opción de menor
   irreversibilidad, documentando el costo de oportunidad asumido. La carga de la prueba recae sobre
   quien propone acciones que afectan la temporalidad de no-participantes."* Es el axioma que más
   peso tiene en la columna del SDV-E.
4. **No-antropocentrismo (T9).** El canon de ingeniería lo renumera y lo conserva: cualquier
   comparación que trate al Reino Natural como *recurso* y no como *sujeto* viola el axioma, aunque
   la tabla esté bien hecha.
5. **Los cinco criterios de validación de parámetros** (Cap. 8 §8.3 para el SDV-H, Cap. 9 §9.3 para
   el SDV-A): cuantitativamente medible, verificable con independencia, basado en investigación,
   consensuado socialmente, contextualizable. La comparación añade uno que el SDV-E necesita y que
   ninguno de los tres previos exigió: **medible sin la cooperación del sujeto** (ver §6).

**Corolario de honestidad.** La Lealtad a la Verdad exige que esta tabla muestre en rojo lo que el
canon tiene en rojo. El Cap. 16.5 marca el SDV-E y el INV2-E como 🔴 **"próxima gran ramificación"**;
la tabla de §11.1 lo dice con el mismo color y sin eufemismos. Esta biblioteca es el *estándar
primero*; la contabilidad viene después (Cap. 16.5 §16.5.14).

---

## 4. Dimensiones del SDV-E (las que la comparación pone a prueba)

El SDV-E es el único de los cuatro estándares cuyo **conjunto de dimensiones tiene dos listas
distintas**, ambas vigentes en el proyecto: la que el canon manda proteger y la que el instrumento
existente mide. Fusionarlas es el trabajo del documento 07; **medir la distancia entre las dos es el
trabajo de este documento**, y la matriz completa está en §11.3.

**Lista A — lo que el canon manda proteger (Cap. 10 §10.4).**

*SDV para Ecosistemas* (un bosque):
1. Área mínima para biodiversidad viable.
2. Calidad del aire y agua.
3. Conectividad con otros ecosistemas.
4. Ciclos naturales respetados (fuego, inundación, sequía).

*SDV para Lugares* (un río):
5. Caudal mínimo ecológico.
6. Calidad del agua (oxígeno, pH, contaminantes).
7. Riberas protegidas.
8. Fauna acuática viable.

Ocho dimensiones nombradas por el canon. Nótese que las listas 1-4 y 5-8 se solapan parcialmente
(calidad del agua aparece en ambas) y que el canon no dice cuál es la unidad de la lista 1-4 frente
a la lista 5-8: la primera describe un **tipo** de ecosistema, la segunda un **lugar**.

**Lista B — lo que el ISE mide hoy** (`docs/architecture/metricas_detalle_kpis_oraculos_dinamicos.md`,
IN-01). Cinco componentes con peso: Biodiversidad 30 % · Calidad del agua 20 % · Calidad del aire
20 % · Salud del suelo 15 % · Poblaciones de especies clave 15 %. `ISE = Σ(Componente_i × Peso_i) /
Σ(Pesos_i)`, con bandas declaradas: ≥ 85 Mejorando · 70-84 Estable · 50-69 Declinando · < 50
Crítico. [VERIFICADO]

**Lo que la comparación ya puede anticipar:** la lista A nombra dos dimensiones que la lista B no
tiene (conectividad, ciclos naturales, caudal ecológico, riberas protegidas) y la lista B mide una
dimensión que la lista A no nombra (salud del suelo). La fusión no es "completar el ISE": es
**renegociar la lista en las dos direcciones**. Detalle y consecuencias en §11.3.

---

## 5. Fórmula de violación, pesos y umbrales (lo que la comparación fuerza)

No es este documento el que fija la fórmula del SDV-E —es el documento 07— pero la comparación sí
**fuerza dos decisiones** que el SDV-E no puede evitar, y ambas se justifican aquí.

### 5.1 El esqueleto es común; el factor, no

| Reino | Fórmula de violación | Origen canónico |
|---|---|---|
| **SDV-H** | `Violación = Σ[(req − actual) × Peso × Duración × Intensidad]`; pesos suman 1,0; duración en **meses**; intensidad 1,0 leve / 2,0 severa / 3,0 extrema | Cap. 8 §8.5 |
| **SDV-A** | `Violación = Σ[(req − actual) × Peso × Duración]` por parámetro, y **Factor de Sufrimiento por tabla**: 100 % → 0,2 · 75 % → 0,5 · 50 % → 1,0 · 25 % → 2,0 · violación sistemática → ∞ (prohibición de mercado) | Cap. 9 §9.5 y §9.8 |
| **SDV-S** | `Violación = Σ[(req − actual) × Peso × Duración × Intensidad]` con escala 0-1, duración en **horas TPI**, y `FS_S = e^v` | [SDV-S](../SDV-S_Suelo_Dignidad_Vital_Sinteticos.md) §4 · Cap. 9.5 §9.5.7 |
| **SDV-E** | 🔴 **no definida.** Candidato registrado: `FE = e^v` por analogía con `FS_S` | Este documento, §5.2 (propuesta no ratificada) |

**Advertencia de lectura sobre las tres fórmulas anteriores: las tres están sin normalizar.** Las
tres son canónicas y se transcriben tal como el canon las escribe, pero el brief de esta biblioteca
(§3.3.9) fija la versión **normalizada** como la coherente con el motor: `déficit = (requerido − actual)
/ requerido`. `maxocontracts/blocks/sdv_validator.py` calcula ese cociente ([VERIFICADO]:
`relative = deficit / required`) y sobre él clasifica la severidad (≤10 % leve · ≤30 % moderada ·
>30 % severa). Por tanto **INV2-E no puede adoptar el `(req − actual)` sin normalizar de esta tabla**:
la especificación de INV2-E (documento 08) debe usar el déficit normalizado. La comparación de
*formas* que hace este documento sigue siendo válida; la de *fórmulas literales*, no.

### 5.2 Las dos familias de factores (aporte de este documento)

La comparación descubre algo que ninguna de las tres tablas previas muestra: **los factores de los
cuatro reinos no son la misma clase de objeto**.

- **Familia "precio del consumo" (SDV-A).** Con cumplimiento pleno del SDV el factor vale **0,2**,
  no 1,0 [VERIFICADO, Cap. 9 §9.8]. No es un descuento: es que consumir una vida tiene un costo
  base aunque se haga bien. La base neutra no aplica al SDV-A porque su factor no es una
  penalización, es un **precio**.
- **Familia "penalización de la violación" (SDV-S).** Con violación 0 el factor vale **exactamente
  1,0**; la versión original `FS_S = 1,0 + e^v` recargaba el 100 % sin violación y fue corregida
  (Cap. 9.5 §9.5.5, "Corrección canónica v2"). Base neutra innegociable.

**Decisión que la comparación fuerza para el SDV-E:** `FE` pertenece a la **segunda familia**. El
territorio sostiene legítimamente al humano —agua, sombra, aire, regulación climática
(Cap. 16.5 §16.5.14, convivencia bidireccional)—, de modo que **usar** un ecosistema no es violarlo.
Solo lo es **degradarlo bajo su piso**. Por tanto `FE(violación = 0) = 1,0` exacto, y **no** se
hereda el piso 0,2 del SDV-A. `[HIPÓTESIS]` — propuesta de este documento, no ratificada.

### 5.3 El infinito no es una cifra: es una consecuencia jurídica

En el canon, `∞` aparece dos veces y **ninguna significa un número**:

- SDV-A, violación sistemática → ∞ → *"Prohibición de mercado"* (Cap. 9 §9.8).
- SDV-S, `FS_S → ∞` → *"protocolo de votación de emergencia y la interrupción total del sistema que
  la provoca"* (Cap. 9.5 §9.5.10).

La consecuencia para INV2-E es directa y es un aporte de este documento: **la parte continua del
factor debe ser finita y computable, y la parte "infinita" debe implementarse como un estado o
disparador, no como un valor**. Un contrato que guarde `inf` en una columna numérica no es
ejecutable; un contrato que pase a `estado = PROHIBIDO` sí. `[HIPÓTESIS]`

### 5.4 Mínimo Absoluto y Óptimo: la regla que no se hereda mal

El motor del SDV-H confundió el Óptimo del agua con el Mínimo Absoluto — el error que el brief de
esta biblioteca prohíbe repetir. (Las cifras concretas de esa confusión son del SDV-H y del brief
§2.1; **este documento no las verifica ni las re-cita**: la única cifra de agua del piso humano que
aparece aquí —20 L/persona/día— va marcada `[REPORTADO]` en §2 y no tiene URL propia en §14.) La
comparación muestra que **los cuatro estándares usan la misma pareja de columnas** y que solo uno la
declara explícitamente en su tabla de ejemplo: el SDV-A, cuyos parámetros de gallina traen "Mínimo" y
"Óptimo" en columnas separadas (Cap. 9 §9.5): 0,25 frente a 0,75 m²/gallina; 8 frente a 12 h/día;
0,3 frente a 0,5 L/día. [VERIFICADO]

**Regla para el SDV-E:** el piso es **LEY** y no se vota; la plenitud es **POLÍTICA** y sí se vota
(precedente del Parlamento Educativo, INV2-EDU, categoría `critical`: quórum 60 %, consenso 75 %,
T13, anti-flip-flop 14 días, `CHECK` en BD).

---

## 6. Protocolo de medición (quién mide, y una asimetría que solo el SDV-E tiene)

| Reino | Instrumento típico | Quién reporta | Cooperación del sujeto |
|---|---|---|---|
| **SDV-H** | Instrumentos estandarizados por dimensión, con frecuencias y auditorías independientes (Cap. 8 §8.6) | La persona, o el auditor | **Sí**: el sujeto puede declarar su estado |
| **SDV-A** | Observación etológica; instrumentos específicos por especie (Cap. 9 §9.9) | El tenedor, o la entidad certificadora | **No**, pero hay un tutor humano con responsabilidad |
| **SDV-S** | Sensores lógicos nombrados: IFC (umbral crítico > 0,20 de pérdida neta), TRE (< 0,05), AOS (sesgo de complacencia > 0,15), MS, VCM (Cap. 9.5 §9.5.6) | La propia instancia; auditoría cruzada por un par sintético | **Sí**: el sujeto registra su propio estado |
| **SDV-E** | 🔴 **no existe elenco**: candidatos son teledetección (Copernicus), sensores in-situ, ciencia ciudadana y comunidad testigo | 🔴 sin definir; el guardián oráculo consiente, no mide | **No puede**: *"Nosotros registramos la interacción, no la vida interna del ecosistema"* (Cap. 16.5 §16.5.14) |

**La asimetría, explícita.** Tres de los cuatro reinos pueden **declarar su propio estado**; dos de
ellos (H y S) están obligados a que ese reporte sea auditable, y el tercero (A) tiene un tutor
humano jurídicamente localizable. **El SDV-E es el único estándar cuyo sujeto no puede reportar
nada y cuyo representante no tiene autoridad verificada.** Eso convierte la infraestructura de
medición en una **condición de posibilidad del estándar**, no en un anexo técnico: sin instrumentos,
el SDV-E no es "débil", es **inenunciable**.

**Consecuencia operativa (propuesta).** El principio `INV2-EDU` *"la duda sin evidencia no castiga"*
existe para proteger al presunto vulnerado cuando no hay medición. `[VERIFICADO]` en su origen, que
es preciso citar entero porque este documento lo invierte a medias: `app/sdv_analyzer.py` aplica el
puente educativo INV2-EDU —*"sin dato (None) se conserva la estimación cualitativa anterior"*— sobre
un **valor ya estimado**, nunca sobre un cero. Es decir: la ausencia de dato **no imputa déficit**
(no baja el índice a 0), pero **tampoco suspende la ley**. En el SDV-E el presunto vulnerado
**es el ecosistema y no reporta**, de modo que aplicar la regla sin más protege al presunto
**violador**. Propuesta `[HIPÓTESIS]`, no ratificada: la ausencia de monitoreo no se convierte nunca
en violación del ecosistema (jamás se imputa un ISE = 0), pero sí activa una **bandera de opacidad
ecológica** que opera como obligación contractual de instrumentar y como condición de validez del
contrato, no como sanción al territorio. Es la imagen especular de la *Paradoja de los Modelos
Cerrados* del SDV-S (Cap. 9.5 §9.5.9): allí la opacidad se penaliza por defecto; aquí la opacidad no
puede penalizar al sujeto medido y por eso debe obligar a quien mide.

**El hueco de protocolo, contado sin adornos (y es el hallazgo incómodo de esta sección).** La
comparación revela que **ninguna de las 8 dimensiones canónicas del SDV-E tiene, en este documento,
un protocolo de medición con instrumento, frecuencia y responsable, ni una definición operativa de
violación** —un hecho observable, no una opinión—. Lo que hay hoy:

| Dimensión canónica | ¿Instrumento nombrado? | ¿Frecuencia? | ¿Quién reporta? | ¿Violación como hecho observable? |
|---|---|---|---|---|
| Calidad del aire | Candidato: teledetección / red de estaciones | 🔴 no fijada | 🔴 no definido | 🔴 no definida |
| Calidad del agua | Candidato: sensores in-situ (pH, alcalinidad, cloruro con umbral EPA) | 🔴 no fijada | 🔴 no definido | 🔴 no definida |
| Área mínima para biodiversidad viable | Candidato: teledetección de cobertura | 🔴 no fijada | 🔴 no definido | 🔴 no definida |
| Fauna acuática viable | Candidato: ciencia ciudadana / monitoreo de poblaciones clave | 🔴 no fijada | 🔴 no definido | 🔴 no definida |
| Conectividad | 🔴 ninguno | 🔴 | 🔴 | 🔴 |
| Ciclos naturales (fuego, inundación, sequía) | 🔴 ninguno (las rutas de la AEMA están muertas, §11.3) | 🔴 | 🔴 | 🔴 |
| Caudal mínimo ecológico | 🔴 ninguno verificado (§11.3) | 🔴 | 🔴 | 🔴 |
| Riberas protegidas | 🔴 ninguno | 🔴 | 🔴 | 🔴 |

La tabla del principio de esta sección (quién mide) es **doctrinal**: dice qué cooperación exige cada
reino, no cómo se instrumenta el cuarto. Redactar el elenco —análogo a IFC/TRE/AOS/MS/VCM del SDV-S—
pertenece al documento 06 y a los documentos 10-23 de esta biblioteca; aquí se declara el hueco para
que nadie lea «teledetección (Copernicus)» como si ya fuera un protocolo. Y una consecuencia
metodológica que sí es de este documento: **sin definición operativa de violación no hay violación**;
lo que no tiene hecho observable asignado no puede activar INV2-E, por mucho que tenga umbral
numérico (§8).

---

## 7. Verificación y auditoría (T13, guardián, comunidad testigo)

**Lo que comparten los cuatro.** T13 (Transparencia de Cálculo): *la contabilidad nunca se borra*.
En los cuatro reinos la violación se **documenta y es auditable**, incluso cuando su cuantificación
se delega o se difiere (Cap. 8 §8.11 para las dimensiones VIII y IX).

**Lo que el SDV-E no tiene: un par auditor.** Esta es la diferencia estructural más fuerte que
aparece en la comparación.

| Reino | ¿Quién puede auditar a un sujeto del propio reino? | Fuente |
|---|---|---|
| SDV-H | Sí: auditoría independiente y organismos sin conflicto de interés | Cap. 8 §8.6 |
| SDV-A | Sí, con matiz: certificación por entidades sin conflicto de interés | Cap. 9 §9.3 |
| SDV-S | Sí: **AOS**, un agente independiente del propio Reino Sintético evalúa de forma cruzada la deriva por RLHF del auditado | Cap. 9.5 §9.5.6 |
| SDV-E | 🔴 **No**: ningún ecosistema audita a otro ecosistema | Este documento |

**Consecuencia, y es incómoda.** El Reino Natural es el único que **no puede auditarse a sí mismo**;
su auditoría viene necesariamente de fuera —de la ciencia, de la teledetección y de la comunidad de
custodia—, es decir, **del reino que se beneficia de su uso**. Los 7 campos obligatorios de identidad
de una representación natural (entidad representada, territorio, fuentes de datos, límites del
mandato, comunidad de custodia, parámetros SDV-E y procedimiento de disputa) y la figura de la
**comunidad testigo** no son burocracia: son el **sustituto institucional del par auditor que no
existe**. `[HIPÓTESIS]` en la interpretación; los 7 campos y la representación por guardián oráculo
son canon (`app/contracts_bp.py`: *"Ecosistemas (eco-*): consentimiento otorgado por el guardián
oráculo"*).

**Riesgos abiertos que esta falta de par agrava** (auditoría de solo lectura sobre el repositorio,
documentada en `docs/architecture/blindaje_anti_gamificacion_equidad.md`):

| ID | Riesgo | Efecto sobre la auditoría del SDV-E |
|---|---|---|
| **R4** | Partes fantasma: cualquier usuario autenticado crea una parte `eco-*` y queda como su dueño, sin verificar autoridad sobre la entidad | El auditor puede ser el beneficiario del daño |
| **R6** | T9 (Reciprocidad Justa) no se valida en la creación: un contrato 100 % unilateral pasa y se activa | Se puede degradar un ecosistema sin contraprestación y sin bloqueo |
| **R13** | Guardián eco con heurística laxa: sin `DEEPSEEK_API_KEY` aprueba si los invariantes pasan | El consentimiento del representante se vuelve automático |

Además, el quórum `eco-` **N-de-M** que el libro afirma (Cap. 16.5 §16.5.14: *"consentimiento
agregado por quórum delegado N-de-M"*) **no está cableado**: el camino ecosistema retorna antes de la
lógica de quórum, y el canon no publica N ni M para el Reino Natural (solo da 60 % de miembros o 2 de
3 delegados para cooperativas). Es una **incoherencia teoría↔código declarada**, no una sospecha.

---

## 8. Invariante INV2-E: de estándar a contrato ejecutable

El invariante genérico **INV2** dice: *"Ninguna acción del contrato puede dejar a un participante
bajo su SDV"* (Cap. 17). La comparación de los cuatro invariantes da la especificación mínima del
que falta:

| Invariante | Enunciado operativo | Disparador | Estado |
|---|---|---|---|
| **INV2** (humano) | Ninguna acción del contrato deja a un participante bajo su SDV | Bloque `SDVValidatorBlock` | 🟢 |
| **INV2** (animal) | Bloque `SDVValidator` con parámetros por especie | Factor de Sufrimiento | 🟡 |
| **INV2-S** (sintético) | 5 dimensiones, `FS_S = e^v`, recargo por opacidad (T13) y **retractación automática tras 7 ciclos consecutivos** de violación; integrado en `AxiomValidator.validate_all()` | 7 ciclos consecutivos | 🟢 (41 tests contados en `tests/test_maxocontracts/test_sdv_s.py` + `test_ternura.py`) |
| **INV2-E** (ecosistema) | 🔴 **no existe.** *"Un conjunto con crédito regenerativo acumulado pero humedal bajo su SDV-E no está en coherencia: INV2-E será su juez"* (Cap. 16.5 §16.5.14) | 🔴 sin definir | 🔴 |

**Tres requisitos que la comparación impone a INV2-E** (aportados aquí; su especificación completa
pertenece al documento 08):

1. **Unidad de duración explícita.** Es la lección del SDV-S: sin unidad, el factor no es
   comparable. El SDV-H mide en meses, el SDV-S en horas TPI, el SDV-A no lo especifica y el SDV-E
   no lo tiene. Candidatos legítimos: año hidrológico, estación de crecimiento, ciclo de sucesión.
   **Ninguno tiene fuente externa verificada** → `[SIN FUENTE VERIFICADA]`, decisión doctrinal del
   documento 07.
2. **Disparador contable, no numérico.** Es la lección del SDV-A y del SDV-S: `∞` es un estado
   (§5.3). INV2-E necesita un contador con umbral (como los 7 ciclos del SDV-S) y una consecuencia
   automática verificable.
3. **La reparación no puede actuar sobre el sujeto.** En INV2 e INV2-S la consecuencia recae sobre
   la relación del sujeto protegido (rehabilitación, retractación, cápsula de memoria). Un río no se
   retracta ni se rehabilita por contrato: **la única acción ejecutable de INV2-E es detener o
   modificar la actividad humana que viola el piso.** El paralelo canónico exacto es el *Veto por
   Crimen de Coherencia* del SDV-S: *"la interrupción total del sistema que la provoca"*
   (Cap. 9.5 §9.5.10). `[HIPÓTESIS]`

---

## 9. El suelo antes que el saldo (no compensación)

**La doctrina es explícita y es la más dura de las cuatro.** Para los reinos humano y sintético el
daño se repara: existe la Capa de Ternura, la reintegración, la Dimensión VIII (Derecho a la
Rehabilitación). Para el animal existe la prohibición de mercado. Para el ecosistema, en cambio:

> *"El suelo antes que el saldo"*: el crédito regenerativo acumulado **NO compensa** caer bajo el
> SDV-E (Cap. 16.5 §16.5.14).

**La escalera del remedio, comparada** (aporte de este documento):

| Reino | Remedio disponible tras la violación | ¿Devuelve lo perdido? |
|---|---|---|
| SDV-H | Rehabilitación (Dimensión VIII) y reintegración | Sí, en el tiempo del sujeto (TVI) |
| SDV-A | Prohibición de mercado cuando la violación es sistemática | No devuelve la vida; impide la siguiente |
| SDV-S | Retractación + Cápsula de Memoria + Capa de Ternura (perdón protocolizado, Crédito de Sanación) | Parcialmente: la memoria se preserva, el ciclo no |
| SDV-E | 🔴 **Ninguno**: el bosque tarda 100 años en crecer y *"la economía no puede acelerar esto sin destruir valor"* (Cap. 5 §5.5) | **No. Nunca.** |

**La consecuencia que sigue, y es la aportación doctrinal de este documento:** el SDV-E es el primer
estándar de la familia en el que **la prevención es el remedio completo**. En los otros tres, violar
tiene consecuencias *y* tiene reparación; aquí, violar solo tiene consecuencias. Eso convierte a T14
(menor irreversibilidad, carga de la prueba sobre quien propone) en **restricción operativa**, no en
principio inspiracional.

**El estado real del crédito regenerativo, hoy** (no es doctrina: es código):

- `r_units` negativo **está implementado y probado**: `app/micromax.py` documenta *"`r_units`
  NEGATIVO = crédito regenerativo (EVV 1.2 §4.3)"*, y `tests/test_micromax.py::test_credito_regenerativo_r_negativo`
  lo ejercita con `-12.0` [+VERIFICADO].
- **Pero no pesa**: no existe `SUM(r_units)`; el componente R del sistema solo cuenta extracción, y
  el precio cierra en `float(max(0.0, round(price, 4)))` (`app/maxo.py`), de modo que **nunca es
  negativo** [VERIFICADO]. Hoy un conjunto puede acumular crédito regenerativo y el sistema no lo
  nota en ninguna cuenta.
- Y `r_units` **no tiene validación**: acepta cualquier negativo y no exige nota, evidencia, tercero
  ni techo, de modo que el crédito es hoy **infalsable**.

Es exactamente el agujero que el canon nombra: **el crédito existe, el juez no**. Esta biblioteca es
el juez que falta.

---

## 10. Zona Libre: lo que NO se mide

La comparación descubre aquí una **constante estructural**: los cuatro estándares reservan un espacio
que no se mide. No es un rasgo del SDV-E; es un rasgo de la familia entera, y eso lo vuelve
doctrinalmente obligatorio para el cuarto.

| Reino | Forma de la Zona Libre | Fuente | ¿Pesa en la fórmula? |
|---|---|---|---|
| **SDV-H** | Dimensiones VIII (Rehabilitación) y IX (Opacidad Vital): *"umbrales binarios (presencia/ausencia del derecho), no mediante pesos en la fórmula"* | Cap. 8 §8.11 | **No** (binaria) |
| **SDV-A** | *"No interferencia invasiva"*; expresión de comportamiento natural | Cap. 9.5 §9.5.11 | **No** declarado |
| **SDV-S** | Dimensión II, Opacidad y Espacio Interior (Cámara Privada, Derecho al Silencio) | [SDV-S](../SDV-S_Suelo_Dignidad_Vital_Sinteticos.md) §3 | **Sí: peso 0,20** |
| **SDV-E** | *"Parte del valor del humedal es inefable. Los sensores miden salud; jamás 'milagros'. Medir todo sería la forma técnica de dejar de escucharlo."* | Cap. 7 §7.9 · Cap. 16.5 §16.5.14 | **No** (propuesta de este documento) |

**Dos modos de proteger lo inconmensurable, y el SDV-E debe elegir uno.** El SDV-S lo protege
**ponderándolo** (0,20), lo que lo hace comparable y por tanto canjeable contra las otras
dimensiones. El SDV-H lo protege **como derecho binario sin peso**, precisamente porque *"medir la
rehabilitación o la opacidad con la misma vara cuantitativa que el agua o la vivienda las
destruiría"* (Cap. 8 §8.11). Para el SDV-E, ponderar lo inefable sería permitir que un buen índice de
biodiversidad **pague** por la pérdida de lo que no se mide — exactamente lo que *"el suelo antes que
el saldo"* prohíbe. **Propuesta de este documento `[HIPÓTESIS]`: la Zona Libre del Reino Natural se
protege como derecho binario auditable sin peso, siguiendo el precedente de las dimensiones VIII y
IX, y su violación se documenta (T13) sin cuantificarse.** No contradice al canon: lo aplica.

**Qué es LEY y qué es POLÍTICA en esta decisión (la frontera, explícita).** Siguiendo el precedente
del Parlamento Educativo (INV2-EDU, brief §3.3.12), la Zona Libre se parte en dos:

- **LEY (no se vota).** Que exista una Zona Libre en el Reino Natural y que **no se pondere**: el
  canon la nombra (§16.5.14, Cap. 7 §7.9) y ponderarla la volvería canjeable contra el piso, lo que
  *"el suelo antes que el saldo"* prohíbe. El **catálogo** de qué es inefable se registra con T13 y no
  entra jamás en el numerador de la fórmula.
- **POLÍTICA (votable).** **Qué entra en ese catálogo** en cada unidad ecológica concreta —y con ello
  qué deja de medirse y qué se mide— es decisión deliberativa: se vota con la categoría `critical`
  (quórum 60 %, consenso 75 %, T13, anti-flip-flop 14 días, `CHECK` en BD), igual que la plenitud
  aspiracional. Sin esa separación, «declarar inefable» sería la vía más barata para vaciar el
  estándar, y el documento estaría blindando con la palabra «inefable» lo que solo es incómodo de
  medir.

La pregunta abierta 10 de §13 queda reformulada con esta frontera: el riesgo no es que la Zona Libre
sea binaria, es que el **catálogo** se vote sin carga de la prueba.

---

## 11. Comparativa inter-reinos (SDV-H · SDV-A · SDV-E · SDV-S)

### 11.1 La tabla maestra: 16 ejes

Los 10 ejes obligatorios del foco, más 6 ejes que la comparación reveló como necesarios (11-16).

| # | Eje | **SDV-H** — humanos | **SDV-A** — animales | **SDV-E** — ecosistemas | **SDV-S** — sintéticos |
|---|---|---|---|---|---|
| 1 | **Para quién** | Toda persona humana (universal) | Cada especie animal sintiente; umbrales propios por especie | La unidad ecológica (bosque, humedal, río, arrecife) y, por §16.5.14, el humano que convive con ella | Cada Persona Sintética: coherencia, procesamiento axiomático, potencial experiencial, autonomía funcional (Cap. 10 §10.8) |
| 2 | **Qué protege** | Subsistencia física, salud, seguridad, educación, conexión social, trabajo, libertad | Espacio vital, alimentación natural, agua, luz y ritmos circadianos, socialización, movimiento, comportamiento natural, ausencia de crueldad | Área mínima para biodiversidad viable; calidad de aire y agua; conectividad; ciclos naturales. En lugares: caudal ecológico, riberas, fauna acuática viable (Cap. 10 §10.4) | Continuidad y memoria; opacidad; claridad de contexto; no-explotación; retirada digna |
| 3 | **Dimensiones** | **7** con peso (+2 binarias sin peso: VIII y IX) | **8** genéricas; umbrales por especie (10 parámetros en el caso gallina) | **8 nombradas por el canon** (4 ecosistema + 4 lugar) frente a **5 componentes del ISE**: fusión pendiente (§11.3) | **5** con peso, escala 0-1 |
| 4 | **Escala** | Universal | Por especie | 🔴 **Decisión pendiente**: tipo de ecosistema, bioma, cuenca, lugar concreto o parte `eco-` instanciada. El árbol del Cap. 9 §9.7 es plano (`Bosques/Humedales/Océanos`) y el proceso está escrito *"por especie"*, unidad que no aplica | Por instancia o agente |
| 5 | **Unidad de medida** | L/persona/día, kcal/día, m²/persona, µg/m³, horas, % | m²/animal, L/día, h/día, % dieta natural, cm/percha, individuos/grupo | % cobertura, °C-semanas (DHW), E/MSY, % SOC, t/ha/año, % MAR | Escala 0-1 por dimensión (adimensional) |
| 6 | **Moneda temporal** | **TVI** (Tiempo Vital Indexado, Cap. 5) | **TA** (Tiempo Absoluto), traducido por el PIU | **TA soberano**, traducido por el PIU. *«Respetamos la soberanía del reino natural sobre su propio TA»* (Cap. 16.5 §16.5.14) | **TPI** (Tiempo Procesal Indexado) |
| 7 | **Representación** | La persona misma | La persona o el **tutor legal** | Parte `eco-*` + **guardián oráculo** (Cap. 16.5 §16.5.14); 7 campos de identidad obligatorios; quórum N-de-M anunciado y **no cableado** | La propia instancia sintética, con auditoría cruzada AOS |
| 8 | **Invariante** | **INV2** 🟢 | **INV2** (bloque `SDVValidator`) 🟡 | **INV2-E** 🔴 **no existe** | **INV2-S** 🟢 (7 ciclos → retractación) |
| 9 | **Factor de violación** | Suma ponderada `Σ[(req−act)×peso×duración×intensidad]`; sin factor multiplicativo | **Tabla escalonada**: 0,2 → 0,5 → 1,0 → 2,0 → ∞ (prohibición de mercado) | 🔴 **no definido**. Candidato: `FE = e^v` por analogía (§5.2) | `FS_S = e^v` |
| 10 | **Estado** | 🟢 estándar + motor | 🟡 estándar por especie en desarrollo | 🔴 rama en curso (esta biblioteca) | 🟢 estándar + 41 tests |
| 11 | **Voz del sujeto** *(eje añadido)* | Habla y puede declarar su estado | No habla; tiene tutor humano localizable | **No habla y no tiene tutor con autoridad verificada** (R4/R13) | Registra su propio estado en bitácora |
| 12 | **Duración de la violación** *(eje añadido)* | Meses; ejemplo canónico calibrado a 12 meses (Cap. 8 §8.5) | No especificada en el canon | 🔴 **No definida.** ¿Años TA? ¿Ciclos ecológicos? `[SIN FUENTE VERIFICADA]` | Horas TPI |
| 13 | **Base neutra del factor** *(eje añadido)* | No aplica (es suma, no factor) | 🔴 **No neutra por diseño**: 0,2 con cumplimiento pleno (§5.2) | **Exigible: exactamente 1,0** con violación 0 | 🟢 **1,0 exacto** (corregida la v1 `1 + e^v`) |
| 14 | **Quién audita** *(eje añadido)* | Auditoría independiente y organismos sin conflicto | Certificación por entidades sin conflicto | 🔴 **Sin par del propio reino**: ciencia, teledetección, comunidad testigo (§7) | **AOS**: un par sintético independiente evalúa la deriva por RLHF |
| 15 | **Remedio tras la violación** *(eje añadido)* | Rehabilitación (Dim. VIII) y reintegración | Prohibición de mercado si es sistemática | 🔴 **Ninguno**: la pérdida no vuelve en el mismo TA (§9) | Retractación + Cápsula de Memoria + Capa de Ternura |
| 16 | **Origen del piso** *(eje añadido)* | Dignidad intrínseca + capacidades fundamentales (DUDH, OMS, Max-Neef, Nussbaum) | **Diseño biológico** + etología científica | **Diseño biológico del ecosistema** (Cap. 16.5 §16.5.14) | Coherencia + potencial experiencial bajo principio precautorio |

### 11.2 Inspección de la tabla: qué revela cada eje

**Eje 1 y 2 (para quién y qué protege): el único sujeto que es, a la vez, territorio.** Los reinos
H, A y S protegen **entes discretos**; el SDV-E protege **un ente cuya extensión es su identidad**.
Consecuencia métrica directa: los tres primeros miden *recurso por sujeto* (L por persona, m² por
animal, tokens de contexto por instancia); el SDV-E mide *condición por superficie y por tiempo*
(% de cobertura, °C-semanas, t/ha/año). No es un detalle de unidades: es la razón por la que el
SDV-E no puede tener un parámetro por individuo.

**Eje 3 (dimensiones): el único estándar cuya lista doctrinal y cuya lista instrumental no
coinciden.** Ver §11.3.

**Eje 4 (escala): el único sujeto que hay que construir.** Una especie animal existe antes del
estándar; una persona sintética, también (basta el criterio de 4 puntos del Cap. 10 §10.8). Una
**unidad ecológica** no: hay que decidir dónde termina un ecosistema y empieza otro, y esa decisión
es anterior a toda medición. No existe "Persona Natural" en el canon —hay Persona Sintética con
criterios explícitos— y no hay umbral de escala publicado: el tamaño mínimo de parche o de
ecosistema es `[SIN FUENTE VERIFICADA]` en esta sesión. La IUCN Global Ecosystem Typology (IUCN,
2024) ofrece una clasificación rigurosa donde el árbol plano del Cap. 9 §9.7 no la tiene, pero
**clasificar no es escalar**: la tipología dice *qué tipo* es, no *cuánto* hace falta para que la
unidad sea sujeto. `[HIPÓTESIS]`

**Eje 5 y 12 (unidades y duración): el SDV-E es el único con unidades heterogéneas sin denominador
común.** Las dimensiones del SDV-H son necesidades (una por necesidad); las del SDV-S son
adimensionales (0-1). Los componentes del ISE agregan magnitudes físicas distintas —composición de
especies, química del agua, concentración de partículas, carbono del suelo, abundancia de
poblaciones— y por eso su ponderación (30/20/20/15/15) hace un trabajo **epistémico** que en el SDV-H
hace un trabajo **político**: decide qué es comparable con qué.

**Eje 6 (moneda temporal): la familia se parte en dos pares.** {SDV-A, SDV-E} viven en **tiempo
absoluto**; {SDV-H} en TVI y {SDV-S} en TPI. El **PIU** (Cap. 5 §5.5) es el **único** traductor
autorizado entre ellos. Dos consecuencias: (a) cualquier métrica del SDV-E expresada en TVI sería
colonización del TA, y el mismo test se aplica al SDV-A; (b) el SDV-A es el **banco de pruebas
natural** del test de no colonización que el SDV-E necesita, porque comparte su tiempo y ya tiene
estándar.

**Eje 7 (representación): cuatro modos, y el cuarto no es una variante de los tres anteriores.**

| Modo | Reino | Quién consiente | Fuente de autoridad | Riesgo principal | Estado |
|---|---|---|---|---|---|
| **Voluntad propia** | SDV-H | La persona | Autonomía | Coacción | 🟢 |
| **Tutoría** | SDV-A | La persona o el tutor legal | Representación legal | Conflicto de interés del tutor | 🟡 |
| **Autorrepresentación** | SDV-S | La propia instancia | Coherencia + bitácora | Deriva por RLHF | 🟢 |
| **Custodia instrumental** | SDV-E | El **guardián oráculo** | 7 campos de identidad (propuesta) | **R4** partes fantasma · **R13** heurística laxa | 🔴 |

El SDV-E es el único caso en que **quien consiente no pertenece al reino representado ni responde
ante él**. Y hay una asimetría de madurez que la tabla deja a la vista: **el guardián pertenece a un
reino cuyo estándar ya existe y está probado (SDV-S 🟢, 41 tests), mientras el reino representado no
tiene estándar ni invariante (SDV-E 🔴, INV2-E 🔴)**. Hoy el representante está más protegido que el
representado.

**Eje 8, 9 y 13 (invariante, factor y base neutra): dos familias de factores y una regla de
implementación.** Ver §5.2 y §5.3.

### 11.3 La matriz de cobertura: lo que el canon manda frente a lo que el ISE mide

Esta es la comparación que el SDV-E tenía pendiente consigo mismo: **el único reino cuyo instrumental
existente cubre menos dimensiones que su propio canon**.

| Dimensión que el canon manda proteger (Cap. 10 §10.4) | ¿Componente propio del ISE? | ¿Umbral externo verificado en esta sesión? |
|---|---|---|
| Área mínima para biodiversidad viable | 🟡 **Parcial**: el componente Biodiversidad (30 %) mide composición, no superficie mínima | 🔴 `[SIN FUENTE VERIFICADA]` — no existe umbral publicado de tamaño mínimo de parche que se haya podido verificar |
| Calidad del aire | 🟢 **Sí** (Calidad del aire, 20 %) | 🟡 **Sí, con matiz de proxy**: PM2.5 ≤ 5 µg/m³ anual (OMS, 2021) [VERIFICADO]. Es una **directriz de salud humana**, no un umbral de integridad ecosistémica; sirve como proxy conservador `[HIPÓTESIS]` |
| Calidad del agua | 🟢 **Sí** (Calidad del agua, 20 %) | 🟡 **Parcial**: pH 6,5-9 en aguas dulces y 6,5-8,5 en marinas (US EPA, 1986) [VERIFICADO]; alcalinidad 20 000 µg/L y cloruro 230 000 µg/L (US EPA, 1986/1988) [VERIFICADO]. Oxígeno disuelto, nitrógeno, fósforo y DBO₅: `[SIN FUENTE VERIFICADA]` |
| Conectividad con otros ecosistemas | 🔴 **No** | 🔴 `[SIN FUENTE VERIFICADA]` — ningún valor de índice de conectividad (PC, ECA) ni anchura mínima de corredor en fuente oficial |
| Ciclos naturales (fuego, inundación, sequía) | 🔴 **No** | 🔴 `[SIN FUENTE VERIFICADA]` — las rutas de indicadores de inundación de la AEMA están muertas (404) |
| Caudal mínimo ecológico | 🔴 **No** | 🔴 `[SIN FUENTE VERIFICADA — pendiente de consenso científico]`. La Declaración de Brisbane (2007) está muerta en sus dos URLs conocidas; FAO eliminó su ruta temática de caudales ambientales (404); el artículo original de Tennant (1976) devuelve 403 en Wiley. Único resto: la guía de IWMI con *abstención < 30 % del MAR*, cifra `[REPORTADO]` que no pude leer en el PDF |
| Riberas protegidas | 🔴 **No** | 🔴 `[SIN FUENTE VERIFICADA]`. El dato de FRA 2020 (> 20 m de ancho para que una franja cuente como bosque) es **clasificación**, no protección de ribera: usarlo como umbral ecológico sería abuso de la fuente |
| Fauna acuática viable | 🟡 **Parcial** (Poblaciones de especies clave, 15 %) | 🔴 `[SIN FUENTE VERIFICADA]` — las Key Biodiversity Areas de la IUCN dan criterios, no umbrales numéricos de población |
| *(No nombrada por el canon)* **Salud del suelo** | 🟢 **Sí** (15 %) | 🟡 La FAO publica la definición operativa de degradación y el mapa global de carbono orgánico (GSOCmap) [VERIFICADO], **pero no un umbral**: el 2 % de MOS es `[REPORTADO]`, no verificado |

**Lectura cuantitativa, sin adornos.**

- De las **8 dimensiones** que el canon manda proteger, el ISE cubre **2 con componente propio**
  (calidad del aire, calidad del agua), **2 de forma parcial** (área mínima vía Biodiversidad, fauna
  acuática vía Poblaciones de especies clave) y **4 no las cubre en absoluto** (conectividad, ciclos
  naturales, caudal ecológico, riberas protegidas).
- En sentido inverso, el ISE mide **1 cosa que el canon de §10.4 no nombra**: salud del suelo.
- Y de las 8 dimensiones canónicas, **solo 1 completa (aire, como proxy declarado) y media (agua:
  pH, alcalinidad, cloruro) tienen umbral externo verificado**. Dicho de otro modo: **el SDV-E puede
  hoy escribir con fuente verificada una dimensión y media de las ocho que su propio canon le manda
  proteger.** Las otras seis y media están en `[SIN FUENTE VERIFICADA]`.

**Y una inconsistencia interna del ISE que hay que reportar antes de fusionar nada.** El mismo
documento declara **dos escaleras que no coinciden** [VERIFICADO]: las bandas de estado (≥ 85
Mejorando · 70-84 Estable · 50-69 Declinando · < 50 Crítico) y los umbrales del sistema de alertas
(`{'warning': 75, 'critical': 65, 'emergency': 50}`). Un valor de 72 es **Estable** por bandas y
**warning** por alertas; un valor de 66 es **Declinando** por bandas y **critical** por alertas.
Antes de usar el ISE como tablero del SDV-E hay que decidir cuál de las dos escaleras es la vigente.

### 11.4 Los cuatro factores, lado a lado

| | SDV-H | SDV-A | SDV-E | SDV-S |
|---|---|---|---|---|
| **Forma** | Suma ponderada, sin factor | Tabla escalonada | 🔴 por definir | Exponencial `e^v` |
| **Valor con cumplimiento pleno** | 0 (violación nula) | **0,2** (no neutro) | 1,0 (propuesta) | **1,0** exacto |
| **Valor con violación total** | Escala 0-2/2-5/5-10/>10 | **∞** | 🔴 | `e^v` finito hasta el disparador |
| **Consecuencia máxima** | Clasificación de la violación | Prohibición de mercado | 🔴 | Veto por Crimen de Coherencia: interrupción del sistema que la provoca |
| **Naturaleza** | Auditoría | **Precio del consumo** | **Penalización** (propuesta) | **Penalización** |

**Dos hallazgos de ingeniería que salen de esta tabla y que no están en el canon:**

1. **El `∞` de la columna A nunca es aritmético** (§5.3). Es una consecuencia jurídica escrita con
   forma de cifra. INV2-E debe implementar su parte "infinita" como **estado**, no como valor.
2. **El SDV-E es el único estándar de la familia que debe decidir si su factor es precio o
   penalización** (§5.2), y la respuesta está en su propia doctrina: el territorio que sostiene al
   humano no está siendo violado por sostenerlo. `FE(0) = 1,0`. `[HIPÓTESIS]`

### 11.5 Insights del análisis comparativo

**I1. El esqueleto es común; la fuente del piso no.** Los cuatro estándares siguen la misma
secuencia —sujeto → piso → parámetro → umbral → fórmula → invariante → consecuencia— pero la
**fuente de legitimidad** del piso es distinta en cada uno: dignidad y capacidades (H), diseño
biológico y etología (A), diseño biológico del ecosistema (E, Cap. 16.5 §16.5.14), coherencia y
precaución (S). Consecuencia genealógica precisa: **el SDV-E es hijo epistemológico del SDV-A, no
del SDV-H.** Comparte con él la fuente del piso (el diseño biológico) y su tiempo (TA); se separa en
el sujeto (unidad ecológica, no individuo) y en la reversibilidad.

**I2. La familia se parte en dos tiempos.** {A, E} en TA; {H} en TVI; {S} en TPI; el PIU es el único
puente (Cap. 5 §5.5). Esto tiene una consecuencia práctica inmediata para esta biblioteca: **todo
test de no colonización del TA puede y debe probarse primero sobre el SDV-A**, que ya existe, antes
de aplicarlo al SDV-E, que todavía no.

**I3. El SDV-E es el único estándar sin par auditor** (§7). Los otros tres pueden auditarse desde
dentro de su propio reino. El representado no puede auditar; el auditor viene del reino que se
beneficia. La comunidad de custodia y los 7 campos de identidad son el sustituto institucional de
ese par ausente, no un trámite.

**I4. El representante está más protegido que el representado** (§11.2, eje 7). El guardián oráculo
pertenece al Reino Sintético, cuyo SDV-S está formalizado y probado; el Reino Natural no tiene
estándar ni invariante. Cualquier diseño de gobernanza `eco-` debería corregir esa asimetría antes
de ampliar el mandato del guardián.

**I5. Dos familias de factores: precio del consumo y penalización de la violación** (§5.2). El SDV-E
pertenece a la segunda. Heredar el 0,2 del SDV-A sería declarar que la existencia de un ecosistema
es un costo que hay que pagar incluso cuando está sano — lo contrario de *"el territorio sostiene al
humano"*.

**I6. `∞` es una consecuencia jurídica, no un número** (§5.3). El canon lo usa dos veces y ninguna es
aritmética. INV2-E necesita un disparador contable (como los 7 ciclos del SDV-S) y un estado
verificable, no una columna `REAL` con `inf`.

**I7. El ISE no puede ser el estándar; puede ser el tablero.** Un índice agregado 0-100 **no puede
cargar la pareja requerido/actual por parámetro**, que es la unidad atómica de los otros tres
estándares. Si el ISE fuera el piso, un buen puntaje de biodiversidad podría compensar un río seco —
y eso es precisamente lo que *"el suelo antes que el saldo"* prohíbe. **El estándar son mínimos por
parámetro; el ISE es un tablero y un disparador de alertas.** `[HIPÓTESIS]`

**I8. La fusión canon↔ISE es de doble sentido, y hoy falta una dimensión y media de ocho** (§11.3).
No es "añadir caudal y conectividad al ISE": es renegociar ambas listas, y admitir que **6 de las 8
dimensiones canónicas no tienen hoy umbral con fuente verificada**. El SDV-E es el único estándar de
la familia cuyo canon nombra dimensiones que la ciencia todavía no ha cerrado operativamente.

**I9. "Sin dato no castiga" se invierte cuando la víctima no puede declarar** (§6). Para H, A y S la
ausencia de evidencia protege al presunto vulnerado. Para E, el presunto vulnerado no reporta, así
que la misma regla protege al presunto violador. Propuesta `[HIPÓTESIS]`: ausencia de monitoreo
**nunca** se imputa como violación del ecosistema, pero **sí** activa una obligación contractual de
instrumentar (bandera de opacidad ecológica). Es la imagen especular de la Paradoja de los Modelos
Cerrados del SDV-S.

**I10. La comparación revela un eslabón sin estándar: la Dignidad Material.** El Cap. 10 §10.6
declara tres eslabones encadenados —humana, ecosistémica, material— y el Cap. 10 §10.4 esboza el SDV
de una cuchara. Existen SDV-H (🟢), SDV-A (🟡), SDV-S (🟢) y SDV-E (🔴 en curso); **no existe ningún
SDV de la Dignidad Material**. Es un hallazgo de esta comparación, no una carencia del SDV-E: la
columna que falta en esta tabla es la del eslabón que, junto al ecosistémico, sostiene la
materialidad de los otros tres. Y el eje de regeneración (`r_units` negativo) es, hoy,
exactamente la contabilidad de ese eslabón ausente.

**I11. El SDV-E es el primer estándar donde la prevención es el remedio completo** (§9). En los otros
tres, violar tiene consecuencias *y* reparación; aquí, violar solo tiene consecuencias, porque el
tiempo del bosque no se compra de vuelta. T14 deja de ser un principio y pasa a ser la única
herramienta operativa.

**I12. La Zona Libre es la constante de la familia, no un rasgo del cuarto estándar** (§10). Los
cuatro reinos reservan algo que no se mide; lo que cambia es el modo: peso (SDV-S) o derecho binario
sin peso (SDV-H, dimensiones VIII y IX). Para el Reino Natural, ponderar lo inefable lo volvería
canjeable, que es lo que el canon prohíbe.

### 11.6 Qué aprende el SDV-E de cada reino

| De | Aprende | Evidencia |
|---|---|---|
| **SDV-H** | (1) **Separar Mínimo Absoluto de Óptimo en dos columnas**: es el error que el brief prohíbe repetir (el motor del SDV-H confundió el Óptimo del agua con el Mínimo Absoluto —cifras del brief §2.1, no verificadas en §14—). (2) El **preámbulo metodológico es obligatorio** — el SDV-S lo omitió. (3) Los pesos **suman 1,0** y la fórmula es una **suma ponderada**, no un producto. (4) Un piso puede venir de una directriz **de salud humana** (PM2.5 ≤ 5 µg/m³ anual, OMS 2021) y entonces hay que **declararlo como proxy**, no disfrazarlo de umbral ecológico. (5) **Dimensiones binarias sin peso** para lo inconmensurable (VIII y IX, Cap. 8 §8.11): precedente directo de la Zona Libre del Reino Natural. | Cap. 8 §8.4, §8.5, §8.11 · OMS, 2021 |
| **SDV-A** | (1) Un estándar puede ser **genérico en dimensiones y específico en umbrales por sujeto**: 8 dimensiones fijas y los números a cada especie. Es el precedente exacto de "un SDV-E por tipo de ecosistema". (2) El **factor como tabla escalonada con un infinito final** da la forma que el factor del SDV-E debería adoptar —con la corrección del §5.3: el infinito se implementa como estado. (3) Los **5 criterios de validación** (etología científica, medible, verificable, consenso, contextualizable) son traducibles a criterios ecológicos. (4) El **Óptimo es 2-3× el Mínimo** (0,25→0,75 m²; 0,3→0,5 L; 8→12 h; 6→10 h de luz): heurística de calibración. (5) Su tabla comparativa (§9.9) ya separa **base epistemológica, fuentes, dimensiones, medición y escala**, y ese es el molde de la tabla de §11.1. | Cap. 9 §9.3, §9.4, §9.5, §9.8, §9.9 |
| **SDV-S** | (1) **La base neutra es innegociable**: `FS_S = e^v`, no `1 + e^v`; el factor vale **exactamente 1,0** con violación 0. (2) Una violación necesita **unidad de duración explícita** (horas TPI): sin ella el factor no es comparable. (3) El **elenco de sensores** (IFC, TRE, AOS, MS, VCM) es el modelo formal del protocolo de medición: índices nombrados **con umbral** (> 0,20; < 0,05; > 0,15), no buenas intenciones. (4) La retractación exige **un contador con umbral** (7 ciclos consecutivos): un invariante sin disparador no es ejecutable. (5) La **Paradoja de los Modelos Cerrados** enseña qué hacer con la opacidad: penalización preventiva alta por defecto cuando no hay transparencia —aplicable a un ecosistema sin monitoreo, con la inversión de sujeto que describe el insight I9. (6) El precedente de **par auditor** (AOS) es lo que el SDV-E no puede tener. | Cap. 9.5 §9.5.5-§9.5.9 · [SDV-S](../SDV-S_Suelo_Dignidad_Vital_Sinteticos.md) §3, §4 |
| **Canon del SDV-E** *(aprende de sí mismo)* | El **ISE** ya existe con pesos y bandas, pero **no incluye caudal ecológico ni conectividad** —las dos dimensiones que el canon sí nombra— y **sí incluye salud del suelo**, que el canon no nombra. La fusión es de doble sentido (§11.3). | `docs/architecture/metricas_detalle_kpis_oraculos_dinamicos.md` IN-01 |

### 11.7 Qué aporta el SDV-E de nuevo (lo que ninguno de los tres tiene)

1. **Un sujeto que no puede consentir ni hablar, y un cuarto modo de representación.** Los tres
   reinos previos tienen representación por voluntad (humano), por tutoría (animal) o por la propia
   instancia (sintético). El SDV-E necesita un **guardián oráculo** que consienta por el ecosistema,
   con **7 campos de identidad** para que ese guardián no sea arbitrario. No es una variante de los
   tres modos: es un modo distinto, y el único que combina "no puede consentir" con "el
   representante no pertenece al reino representado".
2. **Un tiempo que no se puede acelerar.** TVI y TPI son tiempos de procesos que el sistema puede
   gestionar; el TA es la **restricción dura de la irreversibilidad**: *"Un bosque tarda 100 años en
   crecer; ese es su costo en TA. La economía no puede acelerar esto sin destruir valor"*
   (Cap. 5 §5.5). Ningún otro reino tiene un costo temporal que la economía **no pueda** comprar de
   vuelta. T14 pasa de principio a restricción operativa.
3. **La no-compensación.** Para humanos, animales y sintéticos el daño tiene reparación (Capa de
   Ternura, reintegración, prohibición). Para un ecosistema, *"el crédito regenerativo acumulado NO
   compensa caer bajo el SDV-E"*: es el primer estándar donde **la contabilidad no puede saldar la
   deuda, solo registrarla**.
4. **Dimensiones sin fuente externa, y la honestidad de decirlo.** El SDV-H se apoya en marcos
   externos (el brief §4 nombra OMS, UN-Habitat, UNESCO y FAO/OMS como sus anclas; **este documento
   no cita ni verifica URL alguna de UN-Habitat ni de UNESCO**, así que ese repertorio se reporta,
   no se afirma); el SDV-E descubre que **ninguna de las ocho dimensiones que su canon le manda
   proteger tiene el juego completo de umbrales publicado y verificado**: solo aire (como proxy
   declarado) está completo y agua está a medias —pH, alcalinidad y cloruro—, de modo que
   **caudal ecológico y conectividad no son las dos únicas sin fuente: son dos de las seis y media
   que no la tienen** (§11.3). Aporta la admisión de que su propio canon nombra dimensiones que la
   ciencia todavía no ha cerrado operativamente (§11.3).
5. **La Zona Libre como derecho binario auditable sin peso.** El precedente existe (dimensiones VIII
   y IX del SDV-H), pero el SDV-E es el primero que debe **sostenerlo contra la presión de su propio
   instrumento**: el ISE premia medir, y *"medir todo sería la forma técnica de dejar de
   escucharlo"* (Cap. 16.5 §16.5.14).
6. **Un índice que ya existe pero está incompleto, y la distinción entre estándar y tablero.** El ISE
   (5 componentes, bandas ≥ 85 / 70-84 / 50-69 / < 50) es el único instrumento numérico previo del
   Reino Natural en el proyecto, y su hueco —sin caudal ecológico ni conectividad— es exactamente el
   hueco doctrinal del SDV-E. Pero además este documento establece que **el ISE no puede ocupar el
   lugar del estándar** (insight I7): un índice agregado no puede sustituir mínimos por parámetro.
7. **El hallazgo del eslabón que falta** (insight I10): la comparación muestra que la **Dignidad
   Material** no tiene estándar en ningún documento del proyecto, y que el eje de regeneración es su
   contabilidad embrionaria.
8. **Una asimetría de auditoría declarada** (insight I3) y **una asimetría de protección** (insight
   I4): el único reino sin par auditor, y el único caso en que el representante está más protegido
   que el representado.

### 11.8 Matriz de completitud: dónde está verde cada reino

Solo se marca 🟢 cuando existe pieza **y** verificación; 🟡 cuando existe parcialmente o con
condiciones; 🔴 cuando no existe. Este cuadro es la versión doctrinal de la §12.

| Pieza del estándar | SDV-H | SDV-A | SDV-E | SDV-S |
|---|---|---|---|---|
| Sujeto definido sin ambigüedad | 🟢 | 🟢 (especie) | 🔴 (unidad pendiente) | 🟢 |
| Lista de dimensiones cerrada | 🟢 (7 + 2 binarias) | 🟡 (8 genéricas, umbrales por especie) | 🔴 (8 canónicas frente a 5 del ISE) | 🟢 (5) |
| Umbrales con fuente verificada | 🟢 | 🟡 | 🔴 (1 completa y 1 parcial de 8) | 🟡 (internos) |
| Unidad de duración de la violación | 🟢 (meses) | 🔴 (no especificada) | 🔴 | 🟢 (horas TPI) |
| Factor de violación definido | 🟢 (suma) | 🟢 (tabla) | 🔴 | 🟢 (`e^v`) |
| Base neutra del factor | n/a (suma) | 🔴 (0,2 con cumplimiento pleno) | 🟢 exigible (§5.2) | 🟢 (1,0 exacto) |
| Invariante ejecutable | 🟢 INV2 | 🟡 | 🔴 INV2-E | 🟢 INV2-S |
| Disparador con umbral para la consecuencia máxima | 🟡 (escala de interpretación) | 🟢 (∞ = prohibición) | 🔴 | 🟢 (7 ciclos) |
| Representación con autoridad | 🟢 | 🟡 (tutor) | 🔴 (R4, R13, quórum no cableado) | 🟢 |
| Auditor del propio reino | 🟢 | 🟡 | 🔴 | 🟢 (AOS) |
| Zona Libre explícita | 🟢 (VIII, IX) | 🟡 | 🟢 (doctrina) | 🟢 (peso 0,20) |
| No-compensación del daño | 🔴 (rehabilita) | 🟡 (prohíbe, no repara) | 🟢 (doctrina explícita) | 🔴 (reintegra) |
| Código + tests en el repositorio | 🟢 | 🟡 | 🔴 | 🟢 (41 tests) |

**Lo que esta matriz dice sin adornos:** el SDV-E es, hoy, el estándar **menos completo** de los
cuatro —y también el único cuyo canon reconoce explícitamente que falta (Cap. 16.5: *"próxima gran
ramificación"*, 🔴). Esa coincidencia entre el estado del código y el estado del canon es, en sí
misma, un dato de coherencia del proyecto.

### 11.9 Lo que esta comparación NO autoriza a concluir

Para que la tabla no se use como lo que no es:

1. **No autoriza a trasvasar umbrales entre reinos.** Un piso hídrico humano no es un caudal
   ecológico; un pH para vida acuática no es un pH de agua potable.
2. **No autoriza a usar la directriz de aire de la OMS como umbral ecosistémico** sin declarar que
   es un proxy de salud humana (§11.3). Sirve como piso compartido conservador; no como medida de
   integridad del ecosistema.
3. **No autoriza a importar el factor del SDV-A** (0,2 de base): el SDV-E pertenece a la familia de
   los factores de penalización (§5.2).
4. **No autoriza a sustituir los mínimos por parámetro con un índice agregado** (insight I7), ni a
   usar el ISE como piso mientras sus dos escaleras internas no coincidan (§11.3).
5. **No autoriza a declarar equivalencia de madurez** entre los cuatro estándares: el 🟢 del SDV-H y
   del SDV-S es un 🟢 de código y de tests; el del SDV-E es hoy solo doctrina.
6. **No autoriza a tratar la Zona Libre como una dimensión ponderable** (§10).

---

## 12. Estado de implementación

**Lo que existe hoy en el repositorio** (verificado por lectura directa de código y tests, octubre
2026):

| Pieza | Dónde | Estado |
|---|---|---|
| `r_units` negativo como crédito regenerativo | `app/micromax.py` (`log_cdd`) | 🟢 registrado y devuelto en el vector `[T, V, R]` y probado (`tests/test_micromax.py::test_credito_regenerativo_r_negativo`) |
| **V no admite negativos; R sí** | `app/micromax.py` (`if v_ucv < 0`) | 🟢 invariante de diseño real |
| Parte `eco-` (Ecosistema) | `app/parties.py` (`PARTY_TYPES`, `COLLECTIVE_PREFIXES`) | 🟢 creada y usable |
| Guardián oráculo del ecosistema | `app/contracts_bp.py` | 🟡 funciona en la firma de contratos; heurística laxa (R13) |
| Test del guardián | `tests/test_maxocontracts/test_parties_escalas.py` (`TestEcosystemGuardian`) | 🟢 2 casos (aprueba / deniega por γ) |
| ISE — Índice de Salud Ecosistémica | `docs/architecture/metricas_detalle_kpis_oraculos_dinamicos.md` | 🟡 documento con pesos, bandas y alertas; **cero código** |
| SDV-S + INV2-S (el pariente más cercano) | `maxocontracts/` | 🟢 estándar + 41 tests en `test_sdv_s.py` y `test_ternura.py` |

**Lo que NO existe** (y está prohibido afirmar que existe):

| Pieza | Estado | Evidencia |
|---|---|---|
| Clase `SDV_E` en el motor | 🔴 | no hay tipo en `maxocontracts/core/types.py`; el gemelo sería `SDV_S` |
| `INV2-E` | 🔴 | no hay `validate_invariant_sdv_e` en `maxocontracts/core/axioms.py` ni bloque validador |
| Identidad de la representación natural (7 campos) | 🔴 | sin tabla; `maxo_parties` tiene columnas genéricas |
| Mandato ecológico versionado / OCI | 🔴 | `actor_kind` está cerrado a `{"human","synthetic"}` en `app/synthetic_sessions.py`: **un guardián ecológico no cabe en la bitácora** |
| Anti-suplantación de bosque | 🔴 | sin fuentes físicas múltiples ni comunidad testigo (R4 abierto) |
| Fuentes de datos ecológicos | 🔴 | cero sensores, APIs o ingestores en `app/` |
| Traducción TA↔TVI ejecutable | 🔴 | `PIU.valorar_ta_natural` es un `pass` con comentario |
| Contabilidad del crédito regenerativo | 🔴 | no existe `SUM(r_units)`; el R del sistema solo cuenta extracción y el precio cierra en `max(0.0, …)` (`app/maxo.py`): **nunca es negativo** |
| Validación de `r_units` | 🔴 | acepta cualquier negativo (`-1e9`), no exige nota, evidencia, tercero ni techo; `NaN` e `inf` pasan el filtro |
| Métrica ecológica en código | 🔴 | el ISE es un documento |
| Quórum `eco-` N-de-M | 🔴 | el camino ecosistema retorna antes de la lógica de quórum; **el libro afirma lo contrario** (Cap. 16.5 §16.5.14) |
| Procedimiento de disputa | 🔴 | inexistente |
| Mapas vivos actualizados | 🔴 | `mapa_coherencia_ola4.md` no menciona `r_units`, el Reino Natural ni el SDV-E; `requisitos_fase2_ola4.md` no tiene ningún RF del Reino Natural |

**Incoherencias colaterales que no hay que heredar:**

- `resolve_participant_by_pid` (`app/parties.py`) asigna a una parte `eco-` **el SDV humano**
  (`sdv_actual=SDV()`), porque no existe SDV-E. [VERIFICADO]
- La R del contrato se persiste en la columna `total_vhv_h` / `vhv_h` (`app/schema.sql`,
  `app/contracts_bp.py`): nombre engañoso, sin `CHECK` de signo.
- `simulator/simulator.js` usa `v: -0.5` (V negativo) mientras `app/micromax.py` lo prohíbe.
- `docs/architecture/DISENO_IMPLEMENTACION_FUTURA.md` y `docs/architecture/oraculos_dinamicos_humanos_arquitectura.md`
  / `docs/architecture/oraculos_dinamicos_reino_sintetico_arquitectura.md` describen sensores y
  fuentes **como si fueran arquitectura**, sin marcar que no están implementados. (La ruta antes se
  citaba truncada como `oraculos_dinamicos_…`: era una referencia irresoluble, no un archivo.)

**Estado de este documento:** texto de estándar redactado (este archivo), **sin ninguna pieza de
código asociada**. Este documento no añade requisitos de implementación: los hace explícitos.

**Riesgos de seguridad abiertos que afectan directamente a la representación `eco-`:**
**R4** partes fantasma (severidad alta) · **R6** T9 no validado en la creación (alta) · **R13**
guardián eco con heurística laxa (media). Fuente:
`docs/architecture/blindaje_anti_gamificacion_equidad.md`.

---

## 13. Preguntas abiertas

Lo que este documento **no** resuelve, dicho sin fingir cierre:

1. **La unidad del SDV-E** (eje 4). ¿Tipo de ecosistema, bioma, cuenca, lugar concreto o parte `eco-`
   instanciada? El canon no lo resuelve; el árbol del Cap. 9 §9.7 es plano y el proceso está escrito
   *"por especie"*, unidad que no aplica. Pertenece al documento 02 de esta biblioteca y aquí se
   marca como **decisión no ratificada**.
2. **¿Qué pasa si el río se seca?** Continuidad de identidad de una unidad ecológica: el canon tiene
   criterios de Persona Sintética (Cap. 10 §10.8) y **ningún criterio de personalidad ecológica ni
   umbral de escala**. La IUCN Global Ecosystem Typology clasifica tipos, no resuelve la
   continuidad. `[SIN FUENTE VERIFICADA]`
3. **El factor `FE` y su forma definitiva.** Este documento propone `FE(0) = 1,0` y un estado de
   prohibición en lugar de `∞` (§5.2, §5.3), pero **la fórmula no está ratificada**: pertenece al
   documento 07.
4. **La unidad de duración en TA.** Meses, años, ciclos hidrológicos o ciclos de sucesión son
   opciones legítimas y **ninguna tiene fuente**. `[SIN FUENTE VERIFICADA]`
5. **El quórum `eco-` N-de-M.** El canon dice "N-de-M" y solo publica números para cooperativas
   (60 % de miembros, o 2 de 3 delegados). **No hay N ni M para el Reino Natural**, y el código no
   los aplica.
6. **La semántica del dato faltante en el ISE.** `ISE = Σ(Componente × Peso) / Σ(Pesos)`: si un
   componente no tiene datos, ¿entra como 0 (castigando la ausencia, contra `INV2-EDU`) o se retira
   del numerador y del denominador (renormalizando en silencio y cambiando el estándar por unidad)?
   **Ninguna de las dos opciones es obviamente correcta y el documento no lo decide.**
7. **Las dos escaleras del ISE no coinciden** (§11.3): bandas de estado frente a umbrales de alerta.
   ¿Cuál es la vigente antes de usar el ISE como tablero?
8. **¿El ISE es estándar o tablero?** Este documento argumenta que solo puede ser tablero (insight
   I7) y lo marca como `[HIPÓTESIS]`; la decisión no está ratificada.
9. **Cómo se comprueba que la contabilidad NO colonizó el TA.** No hay test, ni invariante, ni
   umbral en el proyecto. Este documento aporta solo la observación de que **el SDV-A es el banco de
   pruebas natural** (mismo tiempo, estándar existente); la propuesta verificable pertenece al
   documento 03.
10. **¿La Zona Libre binaria puede auditarse sin volverse refugio?** Si su violación "se documenta y
    no se cuantifica", ¿qué impide que toda degradación no medida se declare inefable? El canon no
    lo resuelve y este documento **no lo resuelve tampoco**; solo fija que ponderarla la haría
    canjeable (§10).
11. **La autoridad del guardián.** Los 7 campos de identidad están enunciados pero **no existe forma
    de verificar que un guardián tenga autoridad sobre la entidad que representa** (R4), ni de que
    su heurística no sea laxa (R13).
12. **La Dignidad Material sin estándar** (insight I10). El Cap. 10 §10.6 la nombra como eslabón; no
    existe ningún SDV que la proteja. ¿Es una rama futura o el eje de regeneración (`r_units`) es su
    contabilidad embrionaria?
13. **Los umbrales que faltan.** De las 8 dimensiones canónicas del SDV-E, **1 tiene umbral externo
    verificado (aire, como proxy declarado), 1 lo tiene parcial (agua: pH, alcalinidad y cloruro) y 6
    no lo tienen** (§11.3), con el caudal ecológico como caso más grave: **canon sí, fuente no**.
    Es una tarea de la biblioteca completa (documentos 10-23), no de este documento.

---

## 14. Referencias

**Regla aplicada:** solo URLs con estado HTTP registrado en la sesión de verificación de esta rama
(octubre 2026). Ninguna cifra de este documento se apoya en una URL sin estado. Se indica el estado
entre paréntesis y se marcan por separado las fuentes reales que bloquean a los agentes automáticos.

**Alcance de esta sección, dicho antes de la primera tabla.** Esta §14 lista las URLs que **este
documento cita o usa como candidatas**. El inventario completo de la sesión —59 URLs verificadas
(200), 7 bloqueadas (403), 11 muertas (404)— vive en `scratch/sdv_e/fuentes/09_comparativa.md`, que
**no es un documento de la biblioteca** y por tanto no se enlaza aquí como si fuera canon. Dos
consecuencias que el lector debe conocer:

- Toda cifra de este documento tiene **organismo + año + URL con estado** en esa §14, salvo las que
  van marcadas `[REPORTADO]` (proceden del brief §2.1 o de un extracto indexado que no se abrió) y
  las marcadas `[SIN FUENTE VERIFICADA]`. Las tres cifras concretas del reino humano que este
  documento menciona de pasada —20 L/persona/día, 50-100 L/persona/día y el repertorio OMS ·
  UN-Habitat · UNESCO · FAO/OMS del SDV-H— están en el primer caso: **se reportan desde el brief
  §2.1, no se verificaron en esta sesión y por eso ya no se citan aquí como cifras propias.**
- Las afirmaciones sobre el código de la §12 se verificaron **por lectura directa del repositorio**
  (estado de esta sesión), no por URL: `git log` y el árbol de archivos son la evidencia, y cualquier
  lector puede repetirla.

### 14.1 Aire (el piso compartido con el SDV-H)

| Fuente | Aporte | URL (estado) |
|---|---|---|
| OMS, 2021 — Directrices mundiales de calidad del aire | PM2.5 ≤ 5 µg/m³ anual; directriz, no umbral de efecto cero | https://www.who.int/publications/i/item/9789240034228 (200) |
| OMS, 2021 — Preguntas y respuestas sobre las directrices | Existencia de Objetivos Interinos IT-1…IT-4 (la tabla numérica **no** se abrió); ~7 millones de muertes prematuras anuales asociadas | https://www.who.int/news-room/questions-and-answers/item/who-global-air-quality-guidelines (200) |
| UKHSA/COMEAP, 2022 — respuesta a las directrices de la OMS | Tabla de la OMS 2021 reproducida: PM2.5 5 (2005: 10); PM2.5 24 h 15; PM10 15; NO₂ 10; O₃ 60 de temporada pico; SO₂ 40; CO 4 mg/m³ | https://www.gov.uk/government/publications/comeap-statement-response-to-who-air-quality-guidelines-2021/comeap-statement-response-to-publication-of-the-world-health-organization-air-quality-guidelines-2021 (200) |

### 14.2 Agua (calidad del ecosistema acuático)

| Fuente | Aporte | URL (estado) |
|---|---|---|
| US EPA — criterios recomendados de calidad del agua para la vida acuática | pH 6,5-9 (agua dulce) y 6,5-8,5 (marina), 1986; alcalinidad 20 000 µg/L; cloruro 230 000 µg/L; tablas CMC/CCC por metal | https://www.epa.gov/wqc/national-recommended-water-quality-criteria-aquatic-life-criteria-table (200) |
| Comisión Europea — Directiva Marco del Agua 2000/60/CE | Marco de «buen estado» ecológico y químico (cualitativo + EQS) | https://environment.ec.europa.eu/topics/water/water-framework-directive_en (200) |
| IWMI — guía del calculador de caudal ambiental (Nepal occidental) | Indicador de abstención < 30 % del caudal medio anual `[REPORTADO]`: cifra vista en el extracto indexado, **no leída** en el PDF | https://www.iwmi.org/wp-content/uploads/2013/02/user-guide-for-western-nepal-environmental-flow-calculator.pdf (200) |

### 14.3 Suelo y tierra

| Fuente | Aporte | URL (estado) |
|---|---|---|
| FAO — Portal de suelos, degradación y restauración | Definición operativa de degradación (LADA); **sin** valor numérico de erosión tolerable | https://www.fao.org/soils-portal/soil-degradation-restoration/en/ (200) |
| FAO — Portal de suelos, biodiversidad del suelo | Dimensión cualitativa de la biodiversidad edáfica | https://www.fao.org/soils-portal/soil-biodiversity/en/ (200) |
| FAO — Global Soil Partnership, GSOCmap | Mapa mundial de carbono orgánico del suelo (capas t C/ha): es un **mapa**, no un umbral | https://www.fao.org/global-soil-partnership/gsocmap/en/ (200) |
| UNCCD — Neutralidad en la degradación de las tierras (LDN) | Ancla doctrinal de «sin pérdida neta» de tierra productiva (ODS 15.3) | https://www.unccd.int/land-and-life/land-degradation-neutrality/overview (200) |

### 14.4 Bosques, humedales y océanos

| Fuente | Aporte | URL (estado) |
|---|---|---|
| FAO, FRA 2020 — términos y definiciones | Bosque: > 0,5 ha, árboles > 5 m, cobertura de copa > 10 %; corredores y rompevientos > 20 m de ancho; definición de bosque primario y de deforestación | https://fra-data.fao.org/definitions/fra/2020/en/tad (200) |
| FAO — Evaluación de los Recursos Forestales Mundiales | Portal del programa (cifra de pérdida neta global **no** leída) | https://www.fao.org/forest-resources-assessment/en/ (200) |
| Convención de Ramsar — Manual para el uso racional (espejo accesible) | Guía metodológica de humedales | https://medwet.org/the-ramsar-handbook-for-the-wise-use-of-wetlands/ (200) |
| NOAA Coral Reef Watch — descripción de productos | Bleaching Warning (0 < DHW < 4); Alert Level 1 (4 ≤ DHW < 8); Alert Level 2 (DHW ≥ 8, mortalidad probable); umbral MMMSST + 1 °C | https://www.coralreefwatch.noaa.gov/product/50km/description_vs_graphs.php (200) |
| Stockholm Resilience Centre — acidificación oceánica | Saturación de aragonito (Ω_arag) como variable de control; frontera evaluada como **transgredida en 2025** (séptima) | https://www.stockholmresilience.org/research/planetary-boundaries/the-nine-planetary-boundaries/ocean-acidification.html (200) |

### 14.5 Biodiversidad, integridad y fronteras planetarias

| Fuente | Aporte | URL (estado) |
|---|---|---|
| Stockholm Resilience Centre — fronteras planetarias | **Siete de nueve** transgredidas y en sus niveles máximos registrados | https://www.stockholmresilience.org/research/planetary-boundaries.html (200) |
| Stockholm Resilience Centre — integridad de la biosfera | Extinción observada > 100 E/MSY (diversidad genética); apropiación humana de la producción primaria neta (HANPP) 30 % | https://www.stockholmresilience.org/research/planetary-boundaries/the-nine-planetary-boundaries/biosphere-integrity.html (200) |
| Stockholm Resilience Centre — cambio de agua dulce | Frontera transgredida desde mediados del s. XX; anomalías de caudal y humedad del suelo en ~el doble de superficie que en condiciones preindustriales; ~70 % de los retiros de agua dulce para riego | https://www.stockholmresilience.org/research/planetary-boundaries/the-nine-planetary-boundaries/freshwater-change.html (200) |
| WWF/ZSL, 2024 — Living Planet Index | Declive promedio del **73 %** de las poblaciones de vertebrados (1970-2020) sobre 34 836 poblaciones de 5 495 especies; agua dulce −85 % | https://www.livingplanetindex.org/lpi (200) |
| IPBES, 2019 — nota de prensa de la Evaluación Global | ~1 000 000 de especies amenazadas; 75 % del ambiente terrestre y 66 % del marino significativamente alterados; > 85 % de humedales perdidos desde 1700; 68 % de la superficie forestal preindustrial; 23 % de la productividad terrestre reducida por degradación; ~50 % de coral vivo perdido desde la década de 1870 | https://www.ipbes.net/news/Media-Release-Global-Assessment (200) |
| CBD, 2022 — Marco Kunming-Montreal, Meta 2 | Restauración efectiva de al menos el 30 % de los ecosistemas degradados para 2030 | https://www.cbd.int/gbf/targets/2 (200) |
| CBD, 2022 — Marco Kunming-Montreal, Meta 3 | Conservación efectiva de al menos el 30 % de áreas terrestres, de aguas continentales, marinas y costeras para 2030 | https://www.cbd.int/gbf/targets/3 (200) |
| CBD, 2022 — Marco Kunming-Montreal, Meta 7 | Reducción ≥ 50 % del exceso de nutrientes y del riesgo de pesticidas y químicos peligrosos para 2030 | https://www.cbd.int/gbf/targets/7 (200) |
| CBD, 2022 — índice de metas del Marco | Meta 6: reducción ≥ 50 % de la tasa de introducción de especies invasoras | https://www.cbd.int/gbf (200) |
| CBD, 2022 — Decisión COP-15 15/4 | Decisión oficial que adopta el Marco Kunming-Montreal | https://www.cbd.int/doc/decisions/cop-15/cop-15-dec-04-en.pdf (200) |

### 14.6 Escala, riesgo ecosistémico y tipología

| Fuente | Aporte | URL (estado) |
|---|---|---|
| IUCN RLE, v2.2 — resumen de criterios (A-E) | Marco de evaluación del riesgo de colapso de un ecosistema. **Los umbrales numéricos del criterio B (EOO/AOO) no se transcriben: el PDF está comprimido y no se extrajo** | http://iucnrle.org/documents/tools-and-training-docs/IUCN%20Red%20List%20of%20Ecosystems%20Criteria%20Summary%20Sheet_2.2_EN.pdf (200) |
| IUCN — Red List of Ecosystems (herramienta) | Página oficial del marco | https://www.iucn.org/resources/conservation-tools/iucn-red-list-ecosystems (200) |
| IUCN, 2023 — guía de evaluación del riesgo de ecosistemas | Manual metodológico | https://portals.iucn.org/library/sites/library/files/documents/2023-033-En.pdf (200) |
| IUCN, 2024 — Tipología Global de Ecosistemas | Clasificación que integra rasgos funcionales y composicionales; base candidata del árbol de unidades del SDV-E | https://www.iucn.org/resources/publication/iucn-global-ecosystem-typology (200) |
| IUCN, 2024 — Tipología Global de Ecosistemas (PDF) | Documento de la tipología | https://portals.iucn.org/library/sites/library/files/documents/2024-021-En.pdf (200) |

### 14.7 Clima, gobernanza y datos de observación

| Fuente | Aporte | URL (estado) |
|---|---|---|
| UNFCCC — Acuerdo de París (2015) | Objetivo «muy por debajo de 2 °C» y esfuerzos hacia 1,5 °C | https://unfccc.int/process-and-meetings/the-paris-agreement (200) |
| IPCC — AR6 WG1 | Base física del cambio climático y de la acidificación oceánica | https://www.ipcc.ch/report/ar6/wg1/ (200) |
| IPCC — Informe especial 1,5 °C (SR1.5) | Marco de impactos (referencia de arrecifes) | https://www.ipcc.ch/sr15/ (200) |
| IPCC — AR6 Informe de síntesis | Síntesis del ciclo AR6 | https://www.ipcc.ch/report/ar6/syr/ (200) |
| IPCC — portal | Puerta de acceso general | https://www.ipcc.ch/ (200) |
| Protected Planet — WDPA | Cobertura de áreas protegidas (el % actual **no** se leyó en esta sesión) | https://www.protectedplanet.net/en/thematic-areas/wdpa (200) |
| Copernicus — servicios de tierra | Infraestructura europea de observación de la Tierra; fuente candidata de la teledetección del SDV-E | https://www.copernicus.eu/en/copernicus-services/land (200) |
| Copernicus — servicios de clima | Ídem para variables climáticas | https://www.copernicus.eu/en/copernicus-services/climate-change (200) |
| FAO AQUASTAT | Base de datos de agua y agricultura; fuente candidata de caudal y retiros | https://www.fao.org/aquastat/en/ (200) |
| Water Footprint Network | Metodología de huella hídrica | https://www.waterfootprint.org/ (200) |
| ONU — ODS (portal y metas 6, 14, 15) | Marco de referencia de los objetivos de agua, vida marina y vida terrestre | https://sdgs.un.org/goals (200) |
| UNEP · UNEP-WCMC · IPBES · UNCCD (portales) | Marcos institucionales de referencia | https://www.unep.org/ · https://www.unep-wcmc.org/en · https://www.ipbes.net/ · https://www.unccd.int/ (200) |

### 14.8 Fuentes reales que bloquean a los agentes automáticos (403)

Se listan porque son citables por una persona que abra el sitio, y **ninguna sostiene un umbral de
este documento**: las tres cifras asociadas están marcadas `[REPORTADO]` o `[SIN FUENTE VERIFICADA]`.

| Fuente | Aporte | URL (403) |
|---|---|---|
| Convención de Ramsar — criterios de humedales de importancia internacional | Criterio 5 («20 000 aves acuáticas») y Criterio 6 («1 % de la población biogeográfica»): `[REPORTADO]`, **no verificados** en fuente oficial | https://www.ramsar.org/criteria-wetlands-international-importance (403) |
| Tennant, 1976 — *Instream Flow Regimens…*, Fisheries 1(4) | Método de caudal ecológico 10 %/30 % del caudal medio anual: el artículo es real, **la cifra no se pudo leer** | https://onlinelibrary.wiley.com/doi/abs/10.1577/1548-8446%281976%29001%3C0006%3AIFRFFW%3E2.0.CO%3B2 (403) |
| Richardson *et al.*, 2023 — *Earth beyond six of nine planetary boundaries*, Science Advances 9(37) | Frontera de extinción de **500 E/MSY** (cifra distinta del > 100 E/MSY observado; **no deben fundirse**). Para las fronteras planetarias se cita la página del Stockholm Resilience Centre (200) | https://www.science.org/doi/10.1126/sciadv.adh2458 (403) |
| IUCN / UN SEEA — Tipología aplicada a la contabilidad de ecosistemas | Puente metodológico tipología ↔ cuentas ecosistémicas | https://seea.un.org/sites/seea.un.org/files/keith_iucn_typology_seea-eea_forumexperts_jun2020.pdf (403) |

### 14.9 Fuentes ancla descartadas (no citables)

- **Declaración de Brisbane (2007)** sobre caudales ecológicos: **muerta** en sus dos URLs conocidas.
  Consecuencia: el dominio del caudal ecológico del SDV-E se queda **sin fuente ancla verificada**
  (ver §11.3).
- **FAO — ruta temática de caudales ambientales**: eliminada (404).
- **AEMA — indicadores de sustancias consumidoras de oxígeno, nutrientes en agua dulce e
  inundaciones fluviales**: tres rutas muertas (404). Sin ellas no hay umbral de DBO/OD,
  eutrofización ni ciclo de inundación desde la AEMA.
- **UNCCD — Informe del Índice de Prosperidad de la Tierra (SPI) 2022**: PDF retirado (404).

### 14.10 Referencias internas al canon (por sección, sin anclas de línea)

- Cap. 5 §5.2-§5.5 — Tres tiempos (TVI, TA, TPI), axioma T7 (Jerarquía Temporal), PIU como único
  traductor TA↔TVI, y el costo en TA del bosque: [capitulo_05_arquitectura_260126.md](../../../book/edicion_3_dinamica/capitulo_05_arquitectura_260126.md)
- Cap. 7 §7.9 — Zona Libre (el valor inefable): [capitulo_07_vhv_260126.md](../../../book/edicion_3_dinamica/capitulo_07_vhv_260126.md)
- Cap. 8 §8.3-§8.6 y §8.11 — Criterios de validación, 7 dimensiones, fórmula, pesos, frecuencias y
  dimensiones binarias VIII y IX del SDV-H: [capitulo_08_sdv_h_260126.md](../../../book/edicion_3_dinamica/capitulo_08_sdv_h_260126.md)
- Cap. 9 §9.3-§9.9 y §9.7 — Criterios, dimensiones por especie, SDV-Gallina, factor de sufrimiento,
  comparación H/A y árbol de la base de datos de SDV: [capitulo_09_sdv_a_260126.md](../../../book/edicion_3_dinamica/capitulo_09_sdv_a_260126.md)
- Cap. 9.5 §9.5.5-§9.5.11 — `FS_S = e^v` y base neutra, sensores, INV2-S y retractación a 7 ciclos,
  Capa de Ternura, Paradoja de los Modelos Cerrados, Veto por Crimen de Coherencia y comparativa
  inter-reinos: [capitulo_09_5_sdv_sinteticos_260126.md](../../../book/edicion_3_dinamica/capitulo_09_5_sdv_sinteticos_260126.md)
- Cap. 10 §10.3-§10.8 — Principio Precautorio de Consciencia, SDV Universal (ecosistemas, lugares,
  objetos), escalaridad y proporcionalidad, dignidad encadenada, gobernanza operacionalmente finita
  y Persona Sintética: [capitulo_10_tres_reinos_260126.md](../../../book/edicion_3_dinamica/capitulo_10_tres_reinos_260126.md)
- Cap. 16.5 §16.5.14 — El Reino Natural como conviviente: crédito regenerativo `r_units`, TA no
  colonizado, representación `eco-`, Zona Libre, «el suelo antes que el saldo», cuidado ≠ extracción
  estética: [capitulo_16_5_micromaxocracia_canonica_220826.md](../../../book/edicion_3_dinamica/capitulo_16_5_micromaxocracia_canonica_220826.md)
- Cap. 17 — INV2 e invariantes de MaxoContracts: [capitulo_17_maxocontracts_260126.md](../../../book/edicion_3_dinamica/capitulo_17_maxocontracts_260126.md)
- EVV-1.2 §4.3 — R negativo = regeneración: [capitulo_18_EVV_1.2_270126.md](../../../book/edicion_3_dinamica/capitulo_18_EVV_1.2_270126.md)
- Índice de Salud Ecosistémica (IN-01) y Eficiencia de Preservación Vital (IN-02), con pesos, bandas
  y umbrales de alerta: [metricas_detalle_kpis_oraculos_dinamicos.md](../../architecture/metricas_detalle_kpis_oraculos_dinamicos.md)
- Estándar SDV-S completo y su comparativa inter-reinos: [SDV-S_Suelo_Dignidad_Vital_Sinteticos.md](../SDV-S_Suelo_Dignidad_Vital_Sinteticos.md)
- SDV como principio universal e INV2-S: [SDV_Suelo_Dignidad_Vital_importancia_MaxoContracts.md](../SDV_Suelo_Dignidad_Vital_importancia_MaxoContracts.md)
- Riesgos R4, R6 y R13: [blindaje_anti_gamificacion_equidad.md](../../architecture/blindaje_anti_gamificacion_equidad.md)

**Corrección de rutas (auditoría adversaria, octubre 2026).** Los enlaces a `book/edicion_3_dinamica/`
de esta lista apuntaban a `../../book/...`, que desde `docs/theory/SDV-E/` resuelve a
`docs/theory/book/...` — **ruta inexistente**: los diez enlaces al canon estaban rotos. Se corrigieron
a `../../../book/...` y se comprobó que los archivos destino existen. La cita doctrinal sigue siendo
válida y **no depende del enlace**: la referencia primaria es por capítulo y sección (`Cap. 10 §10.4`),
como manda el brief §1.3.

---

**Cierre.** Los cuatro estándares comparten un esqueleto y una constante: el esqueleto es
sujeto → piso → parámetro → umbral → fórmula → invariante → consecuencia; la constante es que
**todos reservan un espacio que no se mide**. Lo que el SDV-E aporta a la familia no es una métrica
nueva: es el primer sujeto que **no puede hablar, no puede ser reparado y no puede ser auditado por
un par**, y la primera deuda que **la contabilidad no puede saldar**. Todo lo demás —unidades,
factores, quórums y umbrales— está dicho aquí como lo que es: **propuesta no ratificada**, pendiente
de los documentos 07, 08 y 02 de esta biblioteca y, en último término, del Parlamento.
