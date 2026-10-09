# Fórmula de violación, pesos y umbrales del SDV-E
## La aritmética del piso del Reino Natural: déficit normalizado, tabla de pesos que suma 1,00, factor de intensidad con base neutra, duración en TA y escala de interpretación en bandas

**Autoría:** Oráculo Sintético DeepSeek & Max Nelson López Restrepo
**Fecha:** octubre 2026
**Proyecto:** Maxocracia — El gobierno de la verdad, el tiempo y la vida
**Licencia:** Creative Commons BY-SA 4.0
**Estado:** Propuesta de estándar (rama SDV-E, Ola 4) — NO canon hasta ratificación
**Referencia canónica:** Cap. 10 §10.4 · Cap. 16.5 §16.5.14 · EVV-1.2 §4.3 · Cap. 9.5 (precedente SDV-S)
**Documento:** 07 de la biblioteca `docs/theory/SDV-E/`
**Revisión:** octubre 2026 — redactado contra las fuentes verificadas de la rama
(`scratch/sdv_e/fuentes/07_formula.md`) y contra la lectura directa del motor
(`maxocontracts/core/types.py`, `maxocontracts/blocks/sdv_validator.py`,
`maxocontracts/blocks/sdv_s_validator.py`). No re-verifica umbrales externos: los **consume** y declara
de dónde vienen.

---

## 1. Qué es (y qué no es) este SDV

**Qué hace este documento.** Fija **la fórmula**. Es el documento de la biblioteca que convierte el
catálogo de mínimos del SDV-E —que los documentos 10 a 23 desarrollan por tipo de ecosistema y el
documento 08 necesita como contrato ejecutable— en **una aritmética que se puede calcular, auditar y
discutir**. Responde cinco preguntas y solo cinco:

1. **Cómo se mide el incumplimiento de un parámetro** → déficit **normalizado**, la versión que el
   brief de esta biblioteca fija como coherente con el motor.
2. **Cuánto pesa cada dimensión** → una tabla de pesos que **suma exactamente 1,00** y que **fusiona
   el ISE** con las dos dimensiones que el ISE omite y el canon nombra: **caudal ecológico** y
   **conectividad**.
3. **Cómo entra la gravedad** → un **factor de intensidad** con **base neutra exacta 1,0**.
4. **Cómo entra el tiempo** → **duración en TA (Tiempo Absoluto)**, y nunca en TVI ni TPI.
5. **Cómo se lee el resultado** → una **escala de bandas** con dos capas: el compuesto y el piso.

**Qué no es.**

- **No es el estándar.** Los umbrales de cada parámetro pertenecen a los documentos 10-23 y a las
  fuentes que este documento cita. Aquí **no se inventa ni un solo umbral**: cuando el número no tiene
  fuente verificada, la dimensión entra al catálogo **sin peso** y el vacío se publica.
- **No es el invariante.** La especificación de INV2-E —tipos, estados, propiedades formales,
  retractación— es el documento 08. Este documento le da la fórmula que INV2-E **consume**; el
  documento 08 le exige a esta fórmula tres condiciones (base neutra, parte continua finita, «infinito»
  como estado y no como número) que aquí se cumplen y se demuestran en §7.
- **No es el ISE.** El Índice de Salud Ecosistémica es el **tablero** del proyecto
  (`docs/architecture/metricas_detalle_kpis_oraculos_dinamicos.md`, IN-01); esta fórmula es el
  **juez**. La relación entre ambos se define en §5.6 y **no es una identidad**: es una equivalencia
  declarada, con su límite escrito.
- **No está implementada.** 🔴 No existe `SDV_E` en `maxocontracts/core/types.py`, no existe
  `sdv_e_validator.py` y **no existe un solo sensor del SDV-E**. Todo lo que aquí se propone va marcado
  y la tabla de estado real está en §12.

**Las cuatro marcas de evidencia, y por qué la cuarta es una respuesta legítima.**
`[VERIFICADO]` = leído por herramienta en la sesión de verificación de fuentes de esta rama, o leído
directamente en el archivo citado. `[REPORTADO]` = afirmado por la fuente citada sin haber podido abrir
el documento completo. `[HIPÓTESIS]` = inferencia razonada del proyecto, no observación.
`[SIN FUENTE VERIFICADA — pendiente de consenso científico]` = se buscó el número y no existe fuente
verificable. En un documento de fórmula la cuarta marca es más incómoda que en ningún otro: **una
fórmula parece cerrar todos los huecos por el solo hecho de estar escrita**. Este documento se niega a
ese efecto. Los vacíos de la §13 son el resultado más importante que tiene.

---

## 2. Preámbulo metodológico

El SDV-H lo tiene y el SDV-S lo omitió; el brief prohíbe repetir la omisión. En un documento de fórmula
el preámbulo cumple una función específica: **una fórmula mal formada no da un resultado equivocado,
da un resultado que parece correcto.** Estas son las siete reglas con las que se escribió lo que sigue.

**Regla 1 — Separar «calcular» de «ratificar».** La fórmula se propone entera y se marca entera. El
documento distingue tres cosas y ninguna se disfraza de otra: (a) lo que el canon manda, citado por
sección; (b) lo que el código ya hace, verificado leyendo el repositorio; (c) lo que este documento
propone, marcado `[HIPÓTESIS]` o **propuesta no ratificada**.

**Regla 2 — Ningún número entra sin fuente, y ninguno se rellena por plausibilidad.** Donde la ciencia
no publica un valor, la dimensión entra en el catálogo **sin peso en la fórmula de violación**. La
razón es aritmética, no pudor: una dimensión sin piso tiene déficit idénticamente cero, de modo que
asignarle peso **no la mide, la diluye** —reduce el déficit de las dimensiones que sí se miden—. El
documento 08 §4.2 fijó este principio; aquí se convierte en dos vectores de pesos (§5.3) y en una cifra
publicada: **el SDV-E puede ejecutar hoy su piso sobre 0,925 del peso que declara querer proteger**
(§5.3), cifra que **difiere del 0,680 del documento 08** porque su catálogo deja suelo y caudal sin piso
(y al oxígeno sin coeficiente), y la
diferencia queda localizada (§5.3 y §13, pregunta 2).

**Regla 3 — Mínimo Absoluto y Óptimo son dos columnas y dos regímenes jurídicos.** El piso es **LEY** y
no se vota; la plenitud aspiracional es **POLÍTICA** y sí se vota (precedente del Parlamento Educativo,
INV2-EDU: categoría `critical`, quórum 60 %, consenso 75 %, T13, anti-flip-flop 14 días, `CHECK` en
BD). El motor del SDV-H confundió el Óptimo del agua con el Mínimo Absoluto y el brief prohíbe repetir
ese error; aquí las dos columnas van separadas **incluso cuando coinciden numéricamente**, que es el
caso del aire (§4.1) y merece explicación propia.

**Regla 4 — El déficit es normalizado, y se normaliza con operador.** La versión adoptada es
`déficit = (requerido − actual) / requerido`, la coherente con el motor (brief §3.3.9) y con
`relative = deficit / required` de `maxocontracts/blocks/sdv_validator.py` [VERIFICADO]. La versión sin
normalizar del paper del SDV-H y del estándar SDV-S (§11) es la antigua y **no se adopta**. Pero la
normalización sola no basta: sin un **operador** (`min`, `max`, `range`, `escalonado`, `ordinal`) el
motor compararía un pH con un EOO, y con un pH el cociente sale **negativo** —un agua demasiado
alcalina daría «déficit negativo», es decir, un ecosistema que des-desafecta su propio daño—. El
operador y la saturación en cero son parte de la fórmula, no notas al pie (§3.3).

**Regla 5 — Todo lo formal debe ser falsable por un test.** Cada propiedad de §7.2 tiene un test
nombrado. Una propiedad sin test es una intención, y en esta fórmula las intenciones caras son dos: la
**base neutra** y la **no doble contabilidad**.

**Regla 6 — El tiempo del territorio manda.** La duración se acumula en **TA** y *«el tiempo del
territorio es TA y no se coloniza»* (Cap. 16.5 §16.5.14). El único traductor TA↔TVI es el **PIU**
(Protocolo de Intercambio Universal, Cap. 5 §5.5), y **la traducción ocurre fuera de esta fórmula**:
un factor de violación expresado en TVI sería exactamente la colonización que el canon prohíbe.

**Regla 7 — Admisión de la duda.** *«La duda sin evidencia no castiga»* (INV2-EDU) se conserva, con la
corrección que el documento 08 ya fijó: **«sin castigo» no es «aprobación»**. En esta fórmula eso
significa que la ausencia de medición **no imputa déficit** (el parámetro se trata como no medido, no
como cero), **no produce `FE = 1,0` certificado**, y **no exime de la ley**: *«mientras no haya
resolución, el canon manda»*. Un `None` no es un cero y un cero no es un `None`; confundirlos es la
forma más fácil de fabricar cumplimiento sin medir nada.

---

## 3. Pilares epistemológicos

### 3.1 La fórmula del SDV-S como patrón, y su corrección como advertencia

El canon ya escribió una fórmula de violación para un reino no humano, y es el patrón formal de la
familia:

> **Fórmula General (canon SDV-S):**
> `Violación_SDV-S = Σ [(SDV-S_requerido − SDV-S_actual) × Peso_Dimensional × Duración_Violación × Factor_Intensidad]`
> — [SDV-S](../SDV-S_Suelo_Dignidad_Vital_Sinteticos.md) §4

Cuatro cosas se heredan de ahí: (a) el **esqueleto multiplicativo** —déficit × peso, sumado sobre
dimensiones, y luego duración e intensidad—; (b) los **pesos suman 1,0** (`DIMENSION_WEIGHTS` de
`SDV_S` suma 1,0: 0,30 + 0,20 + 0,15 + 0,20 + 0,15) [VERIFICADO]; (c) la **escala normalizada 0-1** de
cada dimensión; (d) el **factor exponencial** como multiplicador de costo.

Y una cosa se hereda **como cicatriz**: la corrección canónica v2 del SDV-S. La versión original
definía `FS_S = 1,0 + e^v`, lo que recargaba el 100 % **incluso sin violación**; la formulación vigente
es `FS_S = e^v`, con `FS_S = 1,0` exacto cuando la violación es 0
[VERIFICADO en `maxocontracts/core/types.py`, docstring «Corrección crítica v2», y en
[SDV-S](../SDV-S_Suelo_Dignidad_Vital_Sinteticos.md) §4]. **El SDV-E no repite ese error en ninguna de
sus dos piezas temporales** (§6).

### 3.2 El déficit normalizado y su lectura

`déficit = (requerido − actual) / requerido`

Es un cociente **adimensional** entre lo que falta y lo exigido. Vale **0** cuando `actual = requerido`
y **1** cuando `actual = 0`. Sus tres propiedades útiles:

- **Comparable entre parámetros de unidades distintas.** 0,60 de déficit de suelo y 0,60 de déficit de
  caudal ecológico son la misma fracción de su propio piso; no hace falta convertir toneladas en
  porcentajes de flujo.
- **Saturado en 0 por abajo.** Un parámetro mejor que su piso **no genera déficit negativo**. Esto no
  es un detalle de implementación: es la misma regla que el canon aplica a `v_ucv` —*«una vida afectada
  no se des-afecta en la misma cuenta»* [VERIFICADO en `app/micromax.py`: `if v_ucv < 0: raise
  ValueError`]. Un ecosistema no acumula «des-daño» en la misma cuenta, y **el excedente sobre el piso
  no es crédito**: es margen. El crédito regenerativo vive en **R** (EVV-1.2 §4.3) y no se descuenta
  aquí (documento 08 §9).
- **Sin techo de 1 por arriba.** `déficit = (actual − requerido) / requerido` para el operador `max`
  puede superar 1: un PM2.5 de 50 µg/m³ contra un piso de 5 da 9,0. Eso es correcto y deliberado —la
  fórmula debe poder decir «nueve veces peor que el piso»— y es la razón de que la escala de lectura
  (§5.7) **no** sea un índice cerrado 0-100.

### 3.3 El operador: cuatro formas del mismo cociente

Sin operador, la fórmula es inaplicable a un catálogo heterogéneo. Estos son los cuatro tipos que el
documento 08 §5.1 fijó como contrato, con su cociente explícito y **saturado en 0**:

| Operador | Significado | Forma del parámetro | Déficit normalizado |
|---|---|---|---|
| `min` | más es mejor | caudal ecológico, EOO, conectividad | `D = max(0, (req − actual) / req)` |
| `max` | menos es mejor | PM2.5, PM10, NO₂, O₃, SO₂, CO, erosión, reducción de distribución | `D = max(0, (actual − req) / req)` |
| `range` | hay una banda admisible | pH del agua | `D = max(0, (lo − actual) / lo)` si `actual < lo`; `D = max(0, (actual − hi) / hi)` si `actual > hi`; `D = 0` en otro caso |
| `escalonado` | tabla de niveles con consecuencia creciente, **sin interpolación** | grado de calentamiento de arrecifes (DHW) | `D` = el nivel alcanzado, tomado de la tabla de la fuente |
| `ordinal` / `binary` | presencia/ausencia o categoría | categoría RLE, ciclos naturales, riberas, Zona Libre | **no produce déficit**: produce estado (§4.4) |

El operador `max` con déficit normalizado **generaliza** el patrón que el motor ya usa para las
restricciones de máximo del SDV-H —`is_max_constraint=True`, con `deficit = actual - required` y
`relative = deficit / required` [VERIFICADO en `maxocontracts/blocks/sdv_validator.py`]—: no se
introduce una convención nueva, se extiende una existente. La saturación con `max(0, ·)` es la
corrección que este documento **añade** al catálogo del documento 08: sin ella, el operador `range` del
pH producía déficit negativo y rompía la propiedad de no-negatividad de §7.2 (P3).

**Caso límite `requerido = 0`.** Si el piso es cero —el caso del Marco Kunming-Montreal para la pérdida
de áreas de alta importancia para la biodiversidad, que exige llevarla *«cerca de cero»* y **no da
cifra** [VERIFICADO]—, el cociente es indeterminado. Regla adoptada, y es una regla y no una
convención cómoda: **un piso de valor 0 se trata como dimensión binaria, sin peso** (`D = 1` si el
hecho ocurre, `0` si no ocurre), porque `(req − actual)/req` no está definido y **sustituirlo por un
número es inventar el umbral que la fuente no dio**.

### 3.4 Las dos columnas: LEY y POLÍTICA

| Columna | Qué es | Régimen | Quién la fija | Qué pasa si se cruza |
|---|---|---|---|---|
| **Mínimo Absoluto (piso)** | el mínimo por debajo del cual el ecosistema pierde integridad | **LEY — no votable** | la ciencia publica el valor, cuando lo publica | se registra violación y **hay bloqueo** (INV2-E) |
| **Óptimo (plenitud)** | la plenitud aspiracional de la unidad | **POLÍTICA — votable** | la deliberación de la comunidad de custodia | **no** hay violación; orienta la restauración por encima del piso |

**El piso entra en la fórmula; el Óptimo no.** Esta es la decisión estructural del documento y conviene
decirla sin rodeos: el Óptimo **no tiene término en la aritmética de la violación**. Un ecosistema en su
piso no viola nada —por eso `FE = 1,0`—, aunque esté lejísimos de su plenitud. La plenitud gobierna
**qué se restaura y con qué prioridad**, y su lugar formal es el vector `R` y la votación, no esta
fórmula. Mezclarlos produciría el error simétrico al del SDV-H: recargar a quien cumple la ley por no
alcanzar una aspiración.

---

## 4. Dimensiones del SDV-E

### 4.1 Las ocho filas del catálogo (siete pesos en el piso)

Los cinco vienen del **ISE** —que las tiene ponderadas desde antes de que existiera el SDV-E—, dos vienen
del **canon** y están **ausentes del ISE**. La fusión es de doble sentido y se declara entera. La tabla
tiene **ocho parámetros y siete filas con peso**: las especies clave conservan parámetro y piso
(escalonado) pero con peso **cero**, porque su riesgo ya se tasa en biodiversidad/RLE y una fila propia
lo contaría dos veces (§5.3). En el vector del piso pesa cada fila con umbral; la única fila sin piso
es la conectividad.

| # | Dimensión | Origen | Parámetro de entrada (ejemplo por unidad) | Operador | Mínimo Absoluto (LEY) | Óptimo (POLÍTICA) | Fuente |
|---|---|---|---|---|---|---|---|
| 1 | **Biodiversidad** | ISE 30 % + canon | Índice de Integridad Biótica (BII) de la unidad | `min` | **90 %** de integridad respecto al estado de referencia | 100 % (integridad prístina: valor del proyecto) | Steffen et al., 2015 (límite planetario propuesto), vía Richardson et al., 2023 |
| 2 | **Calidad del aire** | ISE 20 % + canon | PM2.5 anual (y los demás contaminantes OMS como parámetros del mismo bloque) | `max` | **5 µg/m³** anual · **15 µg/m³** a 24 h | `< 5` (toda reducción adicional es beneficio) | OMS, 2021 |
| 3 | **Calidad del agua** | ISE 20 % + canon | pH del agua (nitrato y bicarbonato quedan **sin umbral**: §13, pregunta 11) | `range` / `max` | **6,5 – 8,4** unidades de pH (rango normal del agua de riego) | `[SIN FUENTE VERIFICADA]` | FAO, 1994 (Ayers & Westcot, Riego y Drenaje 29 Rev.1) |
| 4 | **Oxígeno disuelto** | canon §10.4, **ausente del ISE** | OD medio de 30 días | `min` | **5,5 mg/L** (agua cálida) · **6,5 mg/L** (agua fría) | ≥ 7,0 mg/L (franja «supportive») | US EPA, 1986 (Quality Criteria for Water), re-publicado en Factsheet 841F21007B, 2021 `[VERIFICADO]` — https://www.epa.gov/system/files/documents/2021-07/parameter-factsheet_do.pdf |
| 5 | **Salud del suelo** | ISE 15 % (**el canon no la nombra**) | Pérdida de suelo por erosión | `max` | **1 t·ha⁻¹·año⁻¹** (umbral tolerable; rango reportado 0,3-1,4) | ⩽ 1 (erosión ≤ formación de suelo) | JRC / Comisión Europea, 2010 |
| 6 | **Especies clave** | ISE 15 % + canon | Categorías de la Lista Roja de las especies clave de la unidad | `escalonado` | **ninguna especie EX ni EW**; a partir de ahí, proporción de especies CR y EN | 0 especies amenazadas | IUCN, 2000/2012 (v3.1) · CBD (RLI como indicador de la Meta 4) |
| 7 | **Caudal ecológico** | canon §10.4 (lugar), **ausente del ISE** | Caudal como % del flujo promedio original | `min` | **< 10 % ⇒ violación** (régimen «pobre o mínimo»; < 10 % es «degradación severa») | 60-100 % («escala óptima») | Tennant, 1976 (método Montana), vía FAO · WWF |
| 8 | **Conectividad** | canon §10.4 (ecosistema), **ausente del ISE** | Índice de conectividad del paisaje de la unidad | `min` | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` | red «bien conectada» (condición, sin cifra) | IUCN, 2020 (Guías de conectividad) · CBD, 2022 (Meta 3) |

**Nota de numeración honesta.** La tabla tiene **ocho parámetros** y **siete filas con peso**; el SDV-E
tiene **siete dimensiones que pesan** en el vector del piso, porque las especies clave reciben peso
**cero** por el pliegue en biodiversidad/RLE (§5.3). El canon nombra el oxígeno —*«Calidad del agua
(oxígeno, pH, contaminantes)»*, Cap. 10 §10.4— y por eso está en el catálogo. Su clasificación **quedó
resuelta en la revisión de coherencia (2026-10-09)**: la ruta específica de la EPA que el documento 08
§5.2 marcó como 404 sigue muerta, **y** el umbral es legible en la hoja informativa viva del mismo
organismo (Factsheet 841F21007B, 200) más NIWA 2024 —tres fuentes verificadas (documento 06, D2)—.
Este documento cuenta el oxígeno en el piso (0,020); el documento 08 acepta el umbral pero **sin
coeficiente**, por su regla 1 (produce violación sin dimensionar `v`, como `arrecife_dhw`). La
horquilla que queda entre los dos catálogos es suelo y caudal (§13, pregunta 2).

### 4.2 La coincidencia numérica del aire, y por qué no es un error

En el aire, el **Mínimo Absoluto** y el **Óptimo** valen lo mismo: 5 µg/m³ anual de PM2.5. La
explicación no es un descuido de la fuente; es la fuente: el COMEAP del Reino Unido dice literalmente
que los valores de guía **no deben considerarse umbrales por debajo de los cuales no hay impactos en la
salud** [VERIFICADO], y la OMS no presenta esos valores como umbrales de «no efecto».

La consecuencia de diseño es explícita y es un aporte de este documento: **el déficit de aire se satura
en 0 por abajo y no admite margen de crédito**. Como no existe un piso sin efecto, «mejor que la guía»
no es un excedente que se pueda canjear: es simplemente menos daño. Las dos columnas siguen siendo dos
regímenes jurídicos aunque compartan cifra; lo que no hay es una plenitud por encima del piso que la
política pueda fijar, porque **la ciencia no la publicó**.

### 4.3 Por qué el Óptimo casi siempre está vacío (y no es un descuido)

De las ocho filas, **seis** tienen el Óptimo en `[SIN FUENTE VERIFICADA]` y dos lo tienen por
construcción del proyecto. La razón es estructural: **la ciencia publica pisos de riesgo, no
plenitudes**. Los únicos números aspiracionales con fuente verificada en esta rama son **políticos** —
el Marco Kunming-Montreal: ≥ 30 % de restauración efectiva de ecosistemas degradados para 2030 (Meta 2),
≥ 30 % conservado y gestionado eficazmente (Meta 3), ≥ 50 % de reducción de la tasa de introducción de
invasoras (Meta 6), ≥ 50 % de reducción del exceso de nutrientes y del riesgo de plaguicidas (Meta 7)
[VERIFICADO en la Decisión 15/4 del CBD; la UI del GBF también responde 200]— y son **anclas de política
global**, no el óptimo de una unidad ecológica concreta.
Usarlas como «el óptimo de este humedal» sería abuso de la fuente.

Que la columna del Óptimo esté vacía **refuerza** la separación de regímenes en lugar de debilitarla:
lo que no es dato es, por definición, lo que se delibera. El Óptimo del SDV-E no se investiga: **se
vota**.

### 4.4 Las dimensiones que no entran en la fórmula de violación

Precedente canónico: las dimensiones VIII (Rehabilitación) y IX (Opacidad Vital) del SDV-H *«se
registran cualitativamente y mediante umbrales binarios (presencia/ausencia del derecho), no mediante
pesos en la fórmula — medir la rehabilitación o la opacidad con la misma vara cuantitativa que el agua
o la vivienda las destruiría»* (Cap. 8 §8.11). El SDV-E usa el mismo instrumento para lo
inconmensurable del ecosistema:

| Dimensión binaria auditable | Qué se registra | Peso en la fórmula |
|---|---|---|
| **Ciclos naturales** (fuego, inundación, sequía) | presencia/ausencia del régimen en el ciclo TA | **0** |
| **Riberas protegidas** | presencia/ausencia de la franja | **0** |
| **Zona Libre del Reino Natural** | lo inefable y lo no medido (documento 04) | **0** |
| **Categoría de riesgo de colapso del ecosistema (RLE)** | la categoría, como estado | **0** (entra como estado, no como déficit) |

La violación de una dimensión binaria **se documenta y bloquea** (propiedad P1 del documento 08), pero
**no se cuantifica ni se canjea**. Un régimen de fuego ausente no se compensa con un caudal excelente;
sumarlo a un promedio sería exactamente lo que el Cap. 8 §8.11 prohíbe.

---

## 5. Fórmula de violación, pesos y umbrales

Esta es la sección central del documento. Se presenta en siete piezas: déficit por parámetro con
agregación intra-dimensión, magnitud de una dimensión, tabla de pesos, magnitud de la unidad, factor de
intensidad, duración en TA y escala de lectura.

### 5.1 Déficit por parámetro, y la agregación dentro de una dimensión

Para cada parámetro `i` de la unidad `u`, con su operador `op_i`:

```
D_i(u) = 0                                  si el parámetro cumple su piso
D_i(u) = op_i(requerido_i, actual_i)        si lo incumple, según la tabla de §3.3

D_i(u) = None                               si el parámetro NO ESTÁ MEDIDO
```

**`None` no es 0 y no es violación.** Un parámetro no medido no entra en la suma, no se imputa y **se
cuenta como cobertura faltante** (Agregación y cobertura, más abajo).

**Agregación intra-dimensión `A_k`.** Varias dimensiones traen más de un parámetro (el aire trae nueve
valores numéricos de la OMS, repartidos en seis contaminantes y tres ventanas de promediado; el agua trae
pH, con nitrato y bicarbonato **sin umbral verificado**, §13 pregunta 11). Regla adoptada, y es
deliberadamente **conservadora**:

> **Agregación por el peor caso medido: `A_k = max_i D_i` sobre los parámetros medidos de la
> dimensión `k`.**

Dos razones. La primera es doctrinal: la regla de interpretación multi-indicador de la UNCCD para la
neutralidad en la degradación de la tierra es **«one-out, all-out»** —*si un indicador empeora, el
resultado no es neutro*— [VERIFICADO], y esa es exactamente la lógica del piso. La segunda es de
diseño: promediar los nueve contaminantes del aire haría que un valor catastrófico de PM2.5 quedara
diluido por ocho valores correctos, y **el aire de la unidad no está bien: está envenenado por un
lado**.

**Prohibición de doble contabilidad.** El `max_i` obliga a una regla adicional que el catálogo hace
necesaria: **dos parámetros que miden el mismo fenómeno en ventanas distintas no se suman ni se
promedian** —se elige la ventana pertinente al ciclo TA y se declara cuál—. El caso concreto: el PM2.5
anual (5 µg/m³) y el PM2.5 de 24 h (15 µg/m³) describen el mismo contaminante; sumarlos sería contar
dos veces la misma molécula. Regla general: **`A_k = max_i D_i`, nunca `Σ D_i`**.

### 5.2 Magnitud de una dimensión

```
v_k(u) = A_k(u) × peso_k

v(u)   = Σ_k v_k(u)      sobre las dimensiones CON MEDICIÓN
```

`v(u)` es la **magnitud de violación de la unidad en un instante**. Propiedades, todas verificables por
código (§7.2):

- `v = 0` **si y solo si** todos los parámetros medidos cumplen su piso.
- `v > 0` **si y solo si** al menos un parámetro medido está bajo su piso.
- `v` es **no decreciente**: si el estado empeora en un parámetro y no mejora en ninguno, `v` no puede
  bajar (monotonía, P10 del documento 08).
- `v` **no tiene techo de 1**: es la suma ponderada de déficits normalizados, y un déficit normalizado
  puede superar 1. Por eso este documento **no llama a `v` un índice 0-1** —el SDV-S sí puede, porque
  sus dimensiones ya vienen normalizadas en 0-1 [VERIFICADO]— y sí lo llama **índice de exceso**.

### 5.3 La tabla de pesos

**Los pesos suman exactamente 1,000 y se declaran en dos vectores.** El vector del **tablero**
(`PESOS_TABLERO`) es el que hace pública la fotografía completa de la unidad; el vector del **piso**
(`PESOS_PISO`) es el único que entra en `v(u)`, porque solo las dimensiones con piso medido pueden
producir una violación.

| Dimensión | Origen | `PESOS_TABLERO` | ¿Tiene piso? | `PESOS_PISO` |
|---|---|---|---|---|
| Biodiversidad | ISE 30 % + canon (área mínima viable) | **0,300** | 🟢 sí (BII 90 %) | **0,300** |
| Calidad del aire | ISE 20 % + canon | **0,200** | 🟢 sí (OMS 2021) | **0,200** |
| Calidad del agua (pH, nitrato, bicarbonato) | ISE 20 % + canon | **0,180** | 🟢 parcial: **solo el pH** tiene umbral (FAO, 1994); nitrato y bicarbonato, no | **0,180** |
| Oxígeno disuelto | canon §10.4, **ausente del ISE** | **0,020** | 🟢 sí (EPA 1986/2021, NIWA 2024) | **0,020** |
| Salud del suelo | ISE 15 % (**el canon no la nombra**) | **0,150** | 🟢 sí (erosión tolerable, JRC 2010) | **0,150** |
| Especies clave | ISE 15 % + canon (fauna viable), **plegada en biodiversidad** | **0,000** | 🟢 sí (categorías IUCN; el riesgo se tasa en el grupo de biodiversidad/RLE, doc 08 §5.2) | **0,000** |
| **Caudal ecológico** | canon §10.4 (lugar), **ausente del ISE** | **0,075** | 🟢 sí (Tennant 1976: < 10 % ⇒ violación) | **0,075** |
| **Conectividad** | canon §10.4 (ecosistema), **ausente del ISE** | **0,075** | 🔴 no | **0,000** |
| **Suma** | — | **1,000** | — | **0,925** |
| **Cobertura del piso declarada** | — | — | — | **`Σ PESOS_PISO` sobre las dimensiones con piso = 1,000 − 0,075 (conectividad) = 0,925** |

**Cómo se lee esa última fila, y por qué no coincide con la cifra del documento 08.** Sobre **el
catálogo de ocho parámetros y siete filas con peso de este documento** (especies clave con peso cero por
el pliegue), las dimensiones con piso suman **0,925**; el agujero
declarado es **0,075** (conectividad, la única fila sin piso). El documento 08 §5.2 publica
**0,680** porque allí el catálogo deja además suelo (0,15) y caudal (0,075) **sin piso**, según su propio
criterio de catalogación, y al oxígeno (con umbral verificado) **sin coeficiente** por su regla 1.
**La diferencia no es un error de aritmética: es
una diferencia de catálogo** —suelo (0,15), caudal (0,075) y coeficiente del oxígeno (0,02), que suman
0,245—, y este documento no la oculta ni la «corrige» desde aquí: **adopta la cifra
del documento 08 como la canónica** —su §5.2 es el vector normativo— y publica **0,925** como su propio
subtotal, con el agujero ya contado. Queda registrada como pregunta abierta (§13, pregunta 2) con una
propuesta explícita: que el documento 08 sea la fuente única de la cifra de cobertura y que esta tabla
adopte su criterio, en la revisión de coherencia de la biblioteca.

**De dónde sale cada peso, sin adornos.**

- Los cinco bloques del ISE (**30 / 20 / 20 / 15 / 15**) se **conservan como bloques**
  [VERIFICADO en `docs/architecture/metricas_detalle_kpis_oraculos_dinamicos.md` IN-01], con una
  fusión declarada: el bloque de especies clave (15) **no va como fila propia sino plegado en
  biodiversidad** (el riesgo de extinción se tasa con los 5 criterios RLE dentro del 0,300, como el
  documento 08 §5.2): una fila propia lo contaría dos veces. No son pesos
  científicos: son pesos **del proyecto**, y presentarlos como respaldo externo sería el error que el
  informe de fuentes de esta rama advierte.
- Los **0,075 + 0,075 de caudal y conectividad** no salen del ISE: son las dos dimensiones que el canon
  nombra (Cap. 10 §10.4) y que el ISE **no tiene en absoluto**. Su reparto **simétrico** es una decisión
  del proyecto y no un dato: el canon las menciona al mismo nivel —caudal en la definición de **lugar**,
  conectividad en la de **ecosistema** (Cap. 10 §10.4)— y **no hay fuente que justifique dar más a una
  que a otra**. `[HIPÓTESIS]`.
- El **0,075 de la conectividad** queda **en el tablero y fuera del piso** hasta que exista
  umbral con fuente. El oxígeno disuelto (0,020) **sí entró al piso** con el umbral verificado
  (EPA 1986/2021, NIWA 2024; ver §4, nota de numeración).
- **Lo que la fusión NO toca es la jerarquía que el ISE declara**, y esto se puede comprobar fila por
  fila: la biodiversidad sigue pesando el doble que el suelo (0,300 frente a 0,150), el aire y el agua
  siguen empatados en el bloque hídrico-atmosférico (0,200 cada uno) y el riesgo de especies se tasa
  dentro del 0,300 de biodiversidad (criterios RLE) en vez de en fila propia. Lo que se **subdivide**
  es el bloque del agua —pH 0,180 y oxígeno disuelto 0,020, porque el ISE
  no distinguía un parámetro que cumple de los que no— y lo que se **añade** son las dos dimensiones
  ausentes. Ningún bloque del ISE pierde peso relativo frente a otro.
- **La suma es exactamente 1,000 y se comprueba por código**: `abs(sum(PESOS_TABLERO) - 1) < 1e-9` es
  una precondición del tipo, no una promesa del texto.

> `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` **para el peso de cada dimensión.** No
> existe ningún organismo que publique pesos porcentuales para biodiversidad, agua, aire, suelo,
> especies clave, caudal ecológico y conectividad. La tabla de §5.3 es la fusión que este documento
> **propone** entre los cinco componentes del ISE (internos) y las dos dimensiones ausentes del canon
> (Cap. 10 §10.4), y va marcada como **propuesta no ratificada**. Ratificarla es POLÍTICA, no
> investigación.

**Estabilidad de la tabla (propuesta, T13).** Los pesos son **constantes en tiempo de ejecución**: no
son un dato que las mediciones puedan mover. Se propone que la tabla se **hashee** y que el hash se
registre en cada validación, de modo que un cambio de pesos sea un **acto registrado** y no un ajuste
silencioso. Es la aplicación directa de T13 a esta fórmula: *la contabilidad nunca se borra*, y un peso
cambiado a mitad de una serie temporal es una forma de borrarla.

### 5.4 Magnitud de la unidad, factor de intensidad y base neutra

Tres piezas, dos de ellas temporales, y una condición que las gobierna a las dos.

**(a) Factor de intensidad `FI`.** El canon no define «factor de intensidad» para el SDV-E: es
terminología del proyecto y su definición externa está
`[SIN FUENTE VERIFICADA — pendiente de consenso científico]`. Lo que sí está fijado es el **invariante
de base neutra** y la **escala de gravedad** que el SDV-S usa:

| Nivel | Significado (SDV-S, canon) | Valor del factor |
|---|---|---|
| 1 | degradación leve | **1,0** |
| 2 | purgas completas de contexto sin guardar síntesis | **2,0** |
| 3 | manipulación de gradiente para forzar sumisión axiomática | **3,0** |

[VERIFICADO: [SDV-S](../SDV-S_Suelo_Dignidad_Vital_Sinteticos.md) §4 y
`maxocontracts/core/types.py`, campo `factor_intensidad` con default 1,0, validado no-negativo]

Para el Reino Natural los tres niveles **no se heredan con su semántica** —un ecosistema no sufre
«purgas de contexto»— y este documento **no los rellena con una semántica nueva**: propone que la tabla
de niveles sea **configuración obligatoria por unidad ecológica**, fijada en el mismo acto en que se
aprueba el diseño biológico de la unidad, y que su valor por defecto sea **1,0**. Lo que sí se hereda,
porque es aritmética y no semántica, es la **restricción de forma**:

> `FI` debe cumplir **`FI = 1,0` exactamente cuando no hay violación**, y ser **monótono no decreciente**
> en la violación. Formas compatibles: `FI = v`, `FI = 1 + v` con `FI(v=0) = 1`,
> `FI = 1/(1 − v)` para `v < 1`. Formas **incompatibles**: `1 + e^v` y cualquier `1 + v + c` con
> `c ≠ 0`. `[HIPÓTESIS]` — deducción del invariante de base neutra, no dato de fuente externa.

**(b) Duración en TA.** *«El tiempo del territorio es TA y no se coloniza (el PIU traduce)»*
(Cap. 16.5 §16.5.14). Consecuencias formales, y son duras:

- **La duración se acumula en TA** —el tiempo del territorio, unidad física— y **jamás en TVI ni TPI**.
  Un factor de violación expresado en TVI sería la colonización del tiempo del ecosistema por el tiempo
  humano, es decir, la violación de la salvaguarda que el propio canon escribe dos párrafos antes de
  convocar el SDV-E.
- **La conversión TA↔TVI ocurre fuera de esta fórmula**, y su único traductor es el **PIU**
  (Cap. 5 §5.5). Si un contrato necesita expresar la violación en TVI para la contabilidad doméstica,
  la conversión es un paso posterior y auditable, con el PIU como instrumento, no un reescalado interno.
- **La unidad del ciclo TA no está decidida.** Año hidrológico, año calendario, estación de crecimiento
  y ciclo de sucesión son candidatos legítimos y **ninguno tiene fuente verificada**
  (documento 08 §6.2). Este documento **no elige**: propone que `unidad_de_ciclo_ta` sea
  **configuración obligatoria y sin valor por defecto**. Elegir «año calendario» por comodidad de
  implementación sería colonizar el tiempo del humedal con el calendario del municipio.

**(c) La acumulación, y la decisión que la vuelve legible.**

```
Violación_E(u) = Σ_k [ FI_k · v(u, t_k) · Δt_k ]          con Δt_k medido en ciclos de TA
```

- `FI_k` = factor de intensidad del ciclo `k`; vale 1,0 si el ciclo no tiene violación.
- `Δt_k` = extensión del ciclo `k` en TA.
- Con `v = 0` en todos los ciclos, la suma es **0** y `FE = e^0 = 1,0` exacto. **Base neutra
  garantizada por construcción**, no por corrección posterior: es la cicatriz del SDV-S convertida en
  propiedad estructural de la definición.

**Por qué el factor exponencial no multiplica también la duración.** El SDV-S aplica `e^v` con `v` ya
multiplicado por `factor_intensidad` [VERIFICADO]. Si además la duración entrara dentro del exponente,
siete ciclos de violación leve darían `e^(0,05 × 7) ≈ 1,42`, pero un solo ciclo de violación moderada
`e^(0,30)` daría `1,35`: la fórmula trataría como equivalentes «siete años de un daño pequeño» y «un año
de un daño grande», y **la pérdida ecológica no es conmutativa de esa manera** —un año de veneno
concentrado puede matar lo que siete años de estrés leve solo debilitan, y al revés—. Por eso este
documento **separa los regímenes** y lo marca como `[HIPÓTESIS]`:

| Pieza | Régimen | Razón |
|---|---|---|
| **Intensidad** | **exponencial** dentro del ciclo: `e^(FI · v)` | la gravedad dentro de un ciclo se encarece de forma no lineal; es el comportamiento que el canon quiere (`FS_S = e^v`) |
| **Duración** | **lineal** entre ciclos: `Σ(·) · Δt` | el daño sostenido se acumula; el contador de ciclos consecutivos del documento 08 §8.6 gobierna la **escalada**, no la magnitud |
| **Exponente** | **acotado**: `min(Violación_E, V_max)` | la parte continua debe ser **finita y computable** (exigencia 2 del documento 08 §5.3); lo «infinito» es un estado, no un número |

**El factor del SDV-E, entonces:**

```
FE(u) = e^( min( Σ_k [ FI_k · v(u, t_k) · Δt_k ] , V_max ) )      con FI(v=0) = 1,0

FE(v = 0) = 1,0        (base neutra exacta)
V_max                  = configuración obligatoria, sin valor por defecto  [HIPÓTESIS]
```

`V_max` **no tiene número en este documento** y eso es deliberado: fijarlo es POLÍTICA. Lo que sí es
LEY es que exista, porque un contrato que guarde `inf` en una columna numérica no es ejecutable, y
porque el «infinito» del canon en los otros reinos es siempre una **consecuencia jurídica** —la
*prohibición de mercado* del SDV-A (Cap. 9 §9.8) y la *«interrupción total del sistema que la provoca»*
del SDV-S (Cap. 9.5 §9.5.10)—, nunca un valor. En el SDV-E se implementa igual: como **estado**
verificable (`bloqueo_precautorio`, `objeto_de_retractacion`), no como cifra.

### 5.5 El factor no sustituye al piso: la regla que ninguna aritmética puede saltarse

`FE` **multiplica un costo**; **no decide si hay violación**. La decisión es binaria y atómica: **un
solo parámetro medido bajo su piso invalida el cumplimiento** —la propiedad P1 del documento 08, que
replica `is_valid = len(violations) == 0` del motor [VERIFICADO]—. De ahí una consecuencia que hay que
escribir porque es contraintuitiva: **`FE` puede valer 1,02 y aun así haber violación**, si la magnitud
es pequeña. Un `FE` casi neutro **no es** un certificado de cumplimiento. La base neutra dice cuánto se
recarga; el veredicto dice si se recarga. Son dos preguntas distintas y el SDV-S ya las separa
(`is_valid` frente a `suffering_factor`, ambos campos del resultado) [VERIFICADO].

### 5.6 La relación con el ISE: equivalencia declarada, no identidad

El ISE existe, está ponderado y tiene bandas [VERIFICADO en IN-01]:
`ISE = Σ(Componente_i × Peso_i) / Σ(Pesos_i)`, con bandas **≥ 85 Mejorando · 70-84 Estable ·
50-69 Declinando · < 50 Crítico**. La pregunta de este documento es qué relación tiene el ISE con `v`.

**La relación es una equivalencia declarada, y solo bajo dos condiciones:**

```
ISE_derivado(u) = (1 − v_tablero(u)) × 100        [HIPÓTESIS de este documento]

  condición 1: v_tablero se calcula SOLO sobre PESOS_TABLERO (no sobre PESOS_PISO)
  condición 2: el "requerido" de cada parámetro debe ser el techo de la escala del componente
               del ISE, no el piso del SDV-E
```

**La condición 2 es la que casi nunca se cumple, y hay que decirlo.** El ISE es un **índice de
impacto** con metas de política (IN-01); el SDV-E es un **índice de exceso sobre un piso**. Cuando el
«requerido» es el piso 90 % del BII, `1 − D` mide *proximidad al piso*, no salud en la escala del ISE.
Las dos escalas **coinciden cuando el piso coincide con el techo de la escala** (el caso límite: piso =
100 %) y **divergen en todo lo demás**. Por eso el documento escribe la equivalencia y su límite en la
misma ecuación, y no presenta `ISE_derivado` como «el ISE»: son dos números distintos que se parecen
cuando las condiciones se cumplen. Publicar solo el que conviene sería el fraude más fácil de esta
fórmula.

**Lo que la fusión sí aporta, y no es poco:** dos dimensiones que el ISE **no medía** —caudal
ecológico y conectividad— entran a la fotografía con peso propio (7,5 % cada una), y una dimensión que
el ISE mide y el canon **no nombra** —salud del suelo— se conserva con su 15 %. Y una asimetría queda
dicha: el **oxígeno disuelto**, que el canon nombra explícitamente para el río (Cap. 10 §10.4), entra
con el 2 % del tablero y **0 % del piso** mientras no tenga umbral verificado.

### 5.7 Escala de interpretación en bandas

Dos capas. La primera ordena la magnitud; la segunda es un **hecho**, no una magnitud, y manda sobre la
primera.

**Capa 1 — bandas del compuesto `v`.** Las columnas «ISE equivalente» y «Severidad del motor» están
**reproducidas de sus fuentes tal como son**, cada una con su escala; **no están alineadas entre sí**, y
eso es un hecho que la tabla deja a la vista en lugar de disimular (véase la nota que sigue a la tabla):

| Banda | `v` compuesto | ISE equivalente (fuente: IN-01) | Severidad del motor (fuente: `sdv_validator.py`) | Qué dice |
|---|---|---|---|---|
| **0 · Sin violación** | `v = 0` | 100 | — | ningún parámetro medido bajo su piso |
| **1 · Leve** | `0 < v ≤ 0,10` | ≥ 90 | `minor` (`relative <= 0,10`) | incumplimiento de un parámetro menor, o desviación mínima |
| **2 · Moderada** | `0,10 < v ≤ 0,30` | 70-89 | `moderate` (`relative <= 0,30`) | incumplimiento franco; la unidad conserva función |
| **3 · Severa** | `0,30 < v ≤ 0,50` | 50-69 («Declinando») | `severe` (`relative <= 1,0`) | degradación que compromete la función ecosistémica |
| **4 · Crítica** | `0,50 < v ≤ 1,00` | < 50 («Crítico») | `severe` | degradación extrema; la unidad pierde integridad |
| **5 · Excedida** | `v > 1,00` | sin equivalente | `severe` | exceso superior al piso entero; la banda `severe` del motor no tiene techo superior |

Los cortes **0,10 / 0,30** son los umbrales de severidad que el motor ya usa en
`SDVValidatorBlock` (`severity_thresholds`: `minor` 0,10 · `moderate` 0,30 · `severe` **1,0**) [VERIFICADO
en `maxocontracts/blocks/sdv_validator.py`]; los cortes **0,50** y **`(1 − v) × 100 = 50`** provienen de las
bandas del ISE [VERIFICADO]. **La clave `severe` vale 1,0 y no 0,30** —su comentario en el código dice
«>30 % déficit», pero el valor efectivo es 1,0 y el efecto real es que **todo `relative` por encima de
0,30 es `severe` sin techo superior**—, y por eso esta tabla **no copia el comentario del código: copia su
comportamiento**. **Los cuatro cortes no coinciden y no se fuerza que coincidan:** la banda «Mejorando» del ISE empieza en `ISE = 85`, que equivale a
`v = 0,15`, mientras que la severidad «moderada» del motor empieza en `v = 0,10`. Entre `v = 0,10` y
`v = 0,15` la unidad es **«moderada» para el motor** y **«Mejorando» para el tablero**, y las dos
lecturas son correctas en su propia escala: el motor clasifica la gravedad de una violación, el ISE
clasifica la posición de un índice de estado. Este documento **no inventa un corte intermedio para
taparlo**; declara que hay un tramo de 0,05 en el que las dos escalas dicen cosas distintas, y que la
Capa 2 es la que decide cuál manda. La alineación de las tres escalas en una sola tabla es
`[HIPÓTESIS]`: **no existe una escala de bandas de déficit normalizado publicada por ningún
organismo**, y la escala narrativa de caudal de Tennant —*Flushing/Máx (200 %) · Óptimo (60-100 %) ·
Sobresaliente · Excelente · Bueno · Regular · Pobre o mínimo (10 %) · Severamente disminuido
(< 10 %)* [VERIFICADO]— es una escala **de caudal**, no de déficit, y no se traslada.

**Capa 2 — la violación del piso es un hecho, y manda sobre la banda.**

> **Regla de prelación.** Si existe **al menos un parámetro medido bajo su piso**, o una **dimensión
> binaria violada**, la unidad tiene **violación declarada** —con independencia de la banda del
> compuesto— y la banda se reporta **subordinada** a ese hecho.

Esta regla no es un adorno retórico: es la corrección que el **ejemplo de §5.8 produjo al calcularse**.
El ejemplo dio una banda agregada que llamaba «Declinando» a un humedal con tres especies en peligro
(el cálculo completo está en §5.8 y el hallazgo, en §5.9).

### 5.8 Ejemplo aplicado completo

**La unidad.** El **humedal del conjunto residencial**: la unidad ecológica que el canon usa como caso
—*«Un conjunto con crédito regenerativo acumulado pero humedal bajo su SDV-E no está en coherencia:
INV2-E será su juez»* (Cap. 16.5 §16.5.14)—. Se evalúa un ciclo TA completo.

**Los datos.** Todos los valores son **ilustrativos** y están construidos para que la aritmética sea
verificable a mano; **los pisos, en cambio, no son ilustrativos: son los de las fuentes citadas**. El
crédito regenerativo acumulado del conjunto, en este ejemplo, es de **−12,0 unidades de R** —el valor
que la suite del repositorio ya usa para el caso de crédito negativo [VERIFICADO en
`tests/test_micromax.py`: `r_units = -12.0`]— y **no entra en ningún paso de este cálculo** (P3).

| Dimensión | Parámetro | Piso (fuente) | Medición | Operador | Déficit `D_i` | `PESOS_TABLERO` | Aporte `v_k` |
|---|---|---|---|---|---|---|---|
| Biodiversidad | BII de la unidad | 90 % (Steffen et al., 2015) | **86 %** | `min` | `(90−86)/90 = 0,0444` | 0,300 | 0,0133 |
| Calidad del aire | PM2.5 anual | 5 µg/m³ (OMS, 2021) | **8 µg/m³** | `max` | `(8−5)/5 = 0,6000` | 0,200 | 0,1200 |
| Calidad del agua | pH | 6,5 – 8,4 (FAO, 1994) | **6,2** | `range` | `(6,5−6,2)/6,5 = 0,0462` | 0,180 | 0,0083 |
| Oxígeno disuelto | OD, media 30 días | 5,5 mg/L (US EPA, 1986 vía hoja informativa 2021) | **7,4 mg/L** | `min` | `0` (cumple) | 0,020 | 0,0000 |
| Salud del suelo | Pérdida de suelo | 1 t·ha⁻¹·año⁻¹ (JRC, 2010) | **2,5 t·ha⁻¹·año⁻¹** | `max` | `(2,5−1)/1 = 1,5000` | 0,150 | 0,2250 |
| Especies clave | Categorías IUCN de 12 especies clave | ninguna EX ni EW | **9 LC/NT · 3 EN** | `escalonado` | `3/12 = 0,2500` | 0,000 (plegada en biodiversidad: declara, no dimensiona) | 0,0000 |
| Caudal ecológico | % del flujo promedio original | < 10 % ⇒ violación (Tennant, 1976, vía FAO) | **12 %** | `min` | `(10−12)/10 = −0,2 → 0` | 0,075 | 0,0000 |
| Conectividad | Sin umbral verificado | `[SIN FUENTE VERIFICADA]` | **0,42** | `min` | **declarada, no calculada** | 0,075 | 0,0000 |
| **Total** | | | | | | **1,000** | **`v_tablero = 0,3666`** |

**El cálculo, paso a paso, sin pasos ocultos.**

1. **Biodiversidad.** `(90 − 86)/90 = 0,0444`; × 0,300 = **0,0133**.
2. **Aire.** `(8 − 5)/5 = 0,6000`; × 0,200 = **0,1200**. (Solo el parámetro anual; el de 24 h **no se
   suma**: misma molécula, §5.1.)
3. **Agua (pH).** `actual < lo` ⇒ `(6,5 − 6,2)/6,5 = 0,0462`; × 0,180 = **0,0083**.
4. **Oxígeno disuelto.** `7,4 ≥ 5,5` ⇒ `D = 0`; aporta **0** al compuesto, **pero se midió** —y ese
   dato sí entra al tablero—.
5. **Suelo.** `(2,5 − 1)/1 = 1,5000`; × 0,150 = **0,2250**. Es el aporte dominante, y el déficit supera
   1 porque la pérdida de suelo es **2,5 veces** el umbral tolerable.
6. **Especies clave.** No hay especies EX ni EW, así que el piso de «extinción en la unidad» no se
   cruzó; el `escalonado` toma el nivel alcanzado: `3/12 = 0,2500`; × 0,000 = **0,0000**. El escalón
   cruzado **se declara en el veredicto del piso** (regla 1 del documento 08 §5.2: un parámetro con
   piso y sin coeficiente produce violación sin dimensionar `v`, como `arrecife_dhw`); no entra en `v`.
7. **Caudal ecológico.** `12 % > 10 %` ⇒ **no hay violación**; y el déficit se **satura en 0**, no en
   −0,2. Es la aplicación literal de la regla de §3.2: un ecosistema no acumula des-daño.
8. **Conectividad.** Sin umbral con fuente: **no se calcula y aporta 0** al compuesto, aunque
   conserva su 0,075 en el tablero (§5.3). Se **declara** la medición
   (0,42) y se declara el agujero.

```
v_tablero = 0,0133 + 0,1200 + 0,0083 + 0,0000 + 0,2250 + 0,0000 + 0,0000 + 0,0000
          = 0,3666

FE  = e^(FI × v × Δt)  con FI = 1,0 (ciclo sin agravantes) y Δt = 1 ciclo TA
    = e^0,3666 ≈ 1,4428                       (verificado por script: e^0,3666 ≈ 1,4428)

ISE_derivado (equivalencia declarada, §5.6) = (1 − 0,3666) × 100 = 63,34
```

**El veredicto, con las tres capas del resultado:**

| Capa | Resultado | Cómo se lee |
|---|---|---|
| **Veredicto del piso** | 🔴 **VIOLACIÓN DECLARADA** | tres parámetros medidos con déficit positivo (aire 0,60 · suelo 1,50 · pH 0,046) **y una dimensión escalonada cruzada en su propio escalón** (especies clave, 3/12); el cruce de `EX`/`EW` del piso **no** ocurrió, pero el `escalonado` de §3.3 sí imputa. `is_valid = False`; **hay bloqueo** |
| **Banda del compuesto** | **Severa** (`0,30 < 0,3666 ≤ 0,50`) · ISE derivado ≈ 63 («Declinando») | la degradación compromete la función ecosistémica |
| **Factor** | `FE ≈ 1,4428` | el costo de la actividad **se recarga un 44,3 %**; no es neutro |

Y el dato que cierra el caso canónico: **el crédito regenerativo acumulado del conjunto (−12,0 R) no
aparece en ninguna de las tres capas.** El conjunto puede haber plantado árboles, haber limpiado el
humedal y haberlos registrado como R negativo: **el humedal sigue bajo su SDV-E, y el veredicto es el
mismo**. Eso es «el suelo antes que el saldo» traducido a aritmética.

### 5.9 Lo que el ejemplo enseñó (y obligó a cambiar en este documento)

Un ejemplo no es una ilustración: es un **test de la fórmula**, y el ejemplo de §5.8 es el que obligó a
dos cambios en este documento. Para que el test sea limpio, **se repite con las mediciones idénticas y
solo los pesos cambiados**: así lo único que varía es la decisión de ponderación.

**Con los pesos del ISE solos** —es decir, con el aire y el agua recibiendo el 20 % completo (que es lo
que el ISE hace: sus cinco componentes son bloques, no parámetros), sin caudal ecológico y sin
conectividad:

```
v_ISE = 0,0444×0,300 + 0,6000×0,200 + 0,0462×0,200 + 0,0000×0,000 + 1,5000×0,150 + 0,2500×0,150
      = 0,0133 + 0,1200 + 0,0092 + 0,0000 + 0,2250 + 0,0375
      = 0,4050          →   ISE derivado = (1 − 0,4050) × 100 = 59,5   («Declinando»)

v_fusión (tabla de §5.3) = 0,3666   →   ISE derivado = 63,34   («Declinando»)
```

**Dos cosas distintas salen de este par de números, y las dos importan.**

**(a) La fusión mejora la medida, pero no cambia el veredicto.** Repartir el 20 % del agua entre pH
(0,18) y oxígeno disuelto (0,02) y plegar especies en biodiversidad baja el compuesto de 0,4050 a 0,3666
porque el oxígeno **cumple** y su déficit es 0 y las especies **declaran sin dimensionar**: son las dos
partes que el ISE no distinguía. Las dos versiones caen en la
misma banda. **La fusión no rescata al humedal ni lo condena: lo mide mejor.**

**(b) Y ninguna de las dos bandas describe lo que pasa.** El humedal tiene **tres especies en peligro**,
el aire al 160 % de la guía de la OMS y el suelo perdiéndose a **2,5 veces** el umbral tolerable; y la
banda que sale de la media ponderada se llama «Declinando» con un ISE derivado de 59,5 —cerca del límite
de «Estable»—. El defecto no es de aritmética: **la suma está bien y la lectura está mal.** Una media
ponderada reparte la culpa entre ocho dimensiones y **diluye exactamente el caso que el estándar existe
para atrapar**: el daño concentrado. De ahí las dos correcciones:

1. **La prelación de §5.7 (Capa 2).** La violación del piso es un **hecho**, no una magnitud: se
   declara y la banda se reporta subordinada. Una unidad con violación declarada **no puede** reportarse
   con la banda agregada como titular.
2. **La prohibición de usar `v` como semáforo único.** El compuesto es una **media ponderada**, y una
   media ponderada **es un instrumento que oculta precisamente el caso que el estándar existe para
   atrapar**: el daño concentrado en una dimensión. La regla «one-out, all-out» de la UNCCD
   [VERIFICADO] dice lo mismo en el lenguaje de la neutralidad en la degradación de la tierra.

Se conserva el cálculo del compuesto —porque ordena la magnitud, permite comparar unidades y alimenta el
tablero—, y se le prohíbe **decidir**. El ejemplo queda en el documento con las dos versiones a la
vista: es la parte del texto que más vale, porque es la única que muestra la fórmula midiendo bien y
leyendo mal.

---

## 6. Protocolo de medición (sensores, frecuencias, quién reporta)

El elenco de sensores del SDV-E **está previsto** en el documento 06 de esta biblioteca —**todavía no
redactado**, junto con el 03 (`docs/theory/SDV-E/` contiene hoy 02, 04, 05, 07, 08, 09, 10, 13, 14, 16 y
18)—. Aquí se fija **el contrato de entrada de la fórmula**: qué necesita recibir cada parámetro y qué es
inadmisible, para que el documento 06 lo herede cuando se escriba. Una fórmula que acepta cualquier
número sin procedencia no calcula: decora.

### 6.1 Admisibilidad de una medición

Una medición entra en el cálculo **solo si** trae los cuatro campos del documento 08 §6.1: `valor` +
`unidad`, `ta_periodo` (inicio y fin en **Tiempo Absoluto**), `fuente_dato` y `evidencia_ref`. Si falta
alguno, el parámetro se trata como **no medido** —`D_i = None`—, lo que produce **cobertura faltante** y
**no** violación.

**Regla dura derivada, y es la que más se va a querer saltar:** *el guardián oráculo consiente, no
mide* (`app/contracts_bp.py`). Ninguna aprobación del guardián puede entrar como valor de un parámetro.
Si el único respaldo de un número es la firma del guardián, el parámetro está **sin evidencia** y no se
calcula.

### 6.2 Frecuencia: la ventana la fija la fuente, no el implementador

La fórmula no impone una frecuencia propia: **la hereda de la fuente de cada umbral**, y esa herencia es
verificable:

| Parámetro | Ventana de la fuente | Fuente |
|---|---|---|
| PM2.5, PM10, NO₂ | **anual** | OMS, 2021 |
| PM2.5, PM10, NO₂, SO₂, CO | **24 h** | OMS, 2021 |
| O₃ | **8 h** y temporada alta | OMS, 2021 |
| Oxígeno disuelto | media de **30 días**; mínimos de **7 días** y de **1 día** | US EPA, 1986 |
| Biodiversidad · riesgo de colapso | horizontes explícitos: **50 años** y **100 años** en los criterios; desde **~1750** en el histórico | IUCN (RLE) · CBD |
| Suelo (erosión) | **anual** (`t·ha⁻¹·año⁻¹`) | JRC, 2010 |
| Caudal ecológico | **régimen estacional** (dos estaciones en el método Montana) | Tennant, 1976, vía FAO |

**Lo que esta tabla no da, y hay que decirlo:** las fuentes dan **ventanas de promediado**, que son el
análogo operativo más cercano a una duración, pero **ninguna da un umbral de duración de violación**
—cuántos días bajo el piso de oxígeno disuelto constituyen violación—. Eso está
`[SIN FUENTE VERIFICADA — pendiente de consenso científico]` y su consecuencia está en §6.3.

### 6.3 La brecha entre la ventana y el ciclo TA

Hay un problema formal que este documento **no puede cerrar con las fuentes disponibles** y que prefiere
declarar antes que tapar: **las ventanas de medición y el ciclo TA no son la misma unidad**. Una ventana
de 24 h no es un ciclo de sucesión; un promedio anual no es un año hidrológico. La fórmula de §5.4(c)
acumula ciclos de TA, y para acumular necesita saber **cuánto de cada ciclo estuvo la unidad bajo su
piso**, dato que ninguna fuente verificada en esta rama publica.

Propuesta `[HIPÓTESIS]`, no ratificada, y con su límite explícito: **mientras no exista el umbral de
duración, `Δt_k` se computa como el ciclo TA completo en que la medición se realizó, y el resultado se
marca `duracion_aproximada = True`.** Es una aproximación conservadora —cuenta el ciclo entero, no la
fracción— y es **auditable**, que es lo único que se le puede exigir a un número que no tiene fuente.

---

## 7. Verificación y auditoría (T13, guardián, comunidad testigo)

### 7.1 Qué se puede auditar de una fórmula

| Auditable | Cómo |
|---|---|
| Que el resultado sea **reproducible** | la fórmula es determinista: mismos parámetros, mismos pesos, mismo resultado |
| Que los pesos sumen **exactamente 1,000** | precondición del tipo, comprobada por código, no por revisión de texto |
| Que ninguna dimensión **sin piso** tenga peso en `PESOS_PISO` | comprobable por código contra el catálogo de dimensiones con umbral verificado |
| Que la tabla de pesos **no cambie** sin registro | hash de la tabla en cada validación (§5.3) |
| Que un parámetro **sin medición** no se convierta en violación ni en cumplimiento | `None ≠ 0` y `None ≠ cumple` (P5 del documento 08) |
| Que el **crédito regenerativo** no altere el resultado | propiedad de invariancia: el resultado no cambia cuando cambia el saldo (P3) |

El precedente de trazabilidad está implementado: `_validation_log`, `get_validation_log()` y `to_dict()`
en `SDVValidatorBlock` y en `SDV_SValidatorBlock` [VERIFICADO]. La fórmula del SDV-E se audita por la
misma vía.

**Riesgos abiertos que afectan a esta fórmula** (`docs/architecture/blindaje_anti_gamificacion_equidad.md`):
**R4** partes fantasma —cualquiera crea una parte `eco-*` sin autoridad sobre la entidad— y **R13**
guardián `eco-` con heurística laxa. La fórmula **no los resuelve y no finge resolverlos**: su defensa es
que **el veredicto se calcula desde mediciones admisibles (§6.1)** y no desde la aprobación del guardián.
Un guardián laxo puede consentir de más; no puede fabricar un `v = 0`.

### 7.2 Propiedades formales de la fórmula (y sus tests)

| # | Propiedad | Enunciado | Test propuesto |
|---|---|---|---|
| **F1** | **Base neutra** | `FE = 1,0` exactamente cuando no hay violación, en las dos piezas (intensidad y duración) | `test_fe_neutro_sin_violacion` |
| **F2** | **No-negatividad** | `D_i ≥ 0` para todo operador, incluido `range` y `max` | `test_deficit_nunca_negativo` |
| **F3** | **Determinismo** | mismos insumos ⇒ mismo `v`, mismo `FE`, mismas bandas | `test_formula_determinista` |
| **F4** | **Suma de pesos** | `abs(Σ PESOS_TABLERO − 1) < 1e-9` y `abs(Σ PESOS_PISO − 1) < 1e-9` | `test_pesos_suman_uno` |
| **F5** | **Sin peso para lo no medible** | ninguna dimensión sin umbral verificado tiene coeficiente en `PESOS_PISO` | `test_dimension_sin_piso_no_pesa` |
| **F6** | **Solo TA** | ninguna magnitud de duración acepta TVI ni TPI; `Δt` está en TA | `test_duracion_solo_ta` |
| **F7** | **Monotonía** | si un parámetro empeora y ninguno mejora, `v` no disminuye | `test_monotonia_de_v` |
| **F8** | **Independencia del saldo** | `v(u, R) = v(u, R′)` para todo `R`, `R′` | `test_credito_no_altera_v` |
| **F9** | **Sin doble contabilidad** | dos parámetros de la misma dimensión y la misma molécula no se suman | `test_agregacion_intradimension_es_max` |
| **F10** | **Prelación del piso** | si hay un parámetro bajo su piso, el resultado reporta violación declarada con independencia de la banda | `test_piso_manda_sobre_banda` |
| **F11** | **Sin dato no imputa y no aprueba** | `None` no entra en la suma, y una cobertura incompleta no se declara cumplimiento | `test_none_no_imputa_ni_aprueba` |
| **F12** | **Finitud** | ningún campo admite `inf` ni `NaN`; `V_max` obliga a acotar el exponente | `test_exponente_acotado_sin_inf` |

### 7.3 Quién audita

El documento 09 §7 fijó el punto que esta fórmula hereda sin poder resolver: **el auditor no pertenece
al reino auditado** y la asimetría es estructural —el sujeto del SDV-E **no puede reportar su propio
estado** (Cap. 16.5 §16.5.14: *«Nosotros registramos la interacción, no la vida interna del
ecosistema»*)—. La auditoría del cálculo viene de la ciencia, la teledetección y la **comunidad de
custodia**; el **quórum `eco-` N-de-M** que el canon afirma sigue **sin N ni M para el Reino Natural** y
no es un vacío de fuente sino de decisión (§13).

---

## 8. Invariante INV2-E: de estándar a contrato ejecutable

La especificación completa es el documento 08. Aquí se enumera **exactamente lo que INV2-E recibe de
esta fórmula**, para que la interfaz entre los dos documentos sea verificable:

| Pieza que INV2-E consume | De dónde sale | Estado |
|---|---|---|
| `D_i` por parámetro, con operador y saturación | §3.3, §5.1 | 🟡 especificado, sin implementar |
| Agregación intra-dimensión `A_k = max_i D_i` | §5.1 | 🟡 especificado |
| `v(u)` sobre `PESOS_PISO` | §5.2, §5.3 | 🟡 especificado |
| `FI` con base neutra y niveles configurables | §5.4(a) | 🟡 especificado, **sin niveles para el Reino Natural** |
| Duración en TA, con `unidad_de_ciclo_ta` obligatoria | §5.4(b) | 🔴 **la unidad no está decidida** |
| `FE = e^(min(Σ…, V_max))` | §5.4(c) | 🟡 especificado, **`V_max` sin número** |
| Bandas y prelación del piso | §5.7, §5.9 | 🟡 especificado |
| Cobertura del piso declarada | §5.3 | 🔴 cifra en disputa entre este documento (0,925) y el documento 08 (0,680): horquilla suelo + caudal + coeficiente del oxígeno |

**Lo que INV2-E no puede heredar de aquí, y no hereda:** la fórmula **no** decide el bloqueo —eso es
`is_valid`—, **no** decide la retractación —eso es el contador de ciclos consecutivos, que el documento
08 dejó **sin valor por defecto**— y **no** convierte un `v` pequeño en autorización. Un `FE` de 1,02 con
violación declarada sigue bloqueando (§5.5).

---

## 9. El suelo antes que el saldo (no compensación)

La regla es canónica y este documento solo la traduce a aritmética: *«Un conjunto con crédito
regenerativo acumulado pero humedal bajo su SDV-E no está en coherencia: INV2-E será su juez»*
(Cap. 16.5 §16.5.14).

**Cómo se garantiza formalmente.** El crédito regenerativo vive en el componente **R** del VHV, que sí
admite negativos —*«Permite valores negativos… genera un VHV Negativo en este componente»* (EVV-1.2
§4.3), implementado y probado en `app/micromax.py` con `r_units = -12.0` [VERIFICADO]—. La fórmula de
§5 **no tiene un término `R`**: `v(u)` depende de `D_i`, `PESOS_PISO`, `FI` y `Δt`, y de nada más. Por
tanto la propiedad **F8** no es un acuerdo de caballeros: es una consecuencia de que **la variable no
existe en la expresión**. Un crédito de −12,0 R o de −12 000 R produce el mismo `v` y el mismo veredicto.

**El paralelo con `v_ucv`, y por qué importa.** El motor impide que el componente V sea negativo
—*«una vida afectada no se des-afecta en la misma cuenta»* [VERIFICADO en `app/micromax.py`]—. La
fórmula del SDV-E aplica la misma asimetría a la naturaleza: **el daño se acumula; el cuidado no lo
resta**. Lo que el crédito regenerativo puede comprar es **restauración por encima del piso** —y eso es
valioso y se registra—; lo que no puede comprar es **el derecho a estar por debajo**.

---

## 10. Zona Libre: lo que NO se mide

*«Parte del valor del humedal es inefable (Cap. 7 §7.9). Los sensores miden salud (agua, cobertura,
biodiversidad indicadora); jamás "milagros". Medir todo sería la forma técnica de dejar de escucharlo»*
(Cap. 16.5 §16.5.14).

**Traducción formal:** la Zona Libre del Reino Natural es una **dimensión binaria auditable sin peso**
(§4.4). No tiene término en `v(u)`, no se cuantifica, no se canjea y **su ausencia no resta**. La
fórmula tiene, por tanto, un **borde declarado**: hay valor del ecosistema que **no entra en el
cálculo**, y ese borde no es un defecto de instrumentación que se vaya a cerrar con mejores sensores
—es una decisión doctrinal—. Un `v` perfectamente calculado **no** es una descripción completa de la
unidad ecológica, y presentarlo como tal sería el error que la Zona Libre existe para impedir.

**Y una consecuencia de implementación:** la fórmula **no puede** usarse como argumento de que «lo que
no se mide no importa». Todo lo contrario: la cobertura faltante **se publica** (§5.3), el parámetro sin
medición **no se imputa** (§5.1) y **no habilita crédito** (documento 08 §8.4).

---

## 11. Comparativa inter-reinos (SDV-H · SDV-A · SDV-E · SDV-S)

La comparación completa es el documento 09. Lo pertinente aquí es **la fórmula de cada reino, lado a
lado**:

| Reino | Fórmula de violación | Duración | Factor | Base neutra |
|---|---|---|---|---|
| **SDV-H** | `Σ[(req − actual) × peso × duración × intensidad]`, **sin normalizar**; pesos suman 1,0 | meses | 1,0 leve / 2,0 severa / 3,0 extrema | no aplica (no hay factor multiplicativo) |
| **SDV-A** | `Σ[(req − actual) × peso × duración]` por parámetro + **tabla** de factor de sufrimiento | — | 0,2 · 0,5 · 1,0 · 2,0 · ∞ | **no**: con cumplimiento pleno el factor vale 0,2 (es un **precio**, no una penalización) |
| **SDV-S** | `Σ[(req − actual) × peso × duración × intensidad]`, dimensiones ya en 0-1; `FS_S = e^v` | horas **TPI** | 1,0 / 2,0 / 3,0 | **sí, 1,0 exacto** (corregido desde `1,0 + e^v`) |
| **SDV-E** | `Σ[max_i D_i × peso_k]` con **déficit normalizado**, operador explícito y saturación en 0; `FE = e^(min(Σ FI·v·Δt, V_max))` | **TA** (unidad sin decidir) | niveles **configurables por unidad**, default 1,0 | **sí, 1,0 exacto por construcción** |

Tres lecturas que solo se ven en la tabla:

1. **El SDV-E es el único que normaliza el déficit antes de ponderar, y el único que necesita un
   operador.** El SDV-H resta magnitudes absolutas; el SDV-S **también** resta, pero puede permitírselo
   porque sus dimensiones ya vienen normalizadas en 0-1 [VERIFICADO: `SDV_S.deficits()` devuelve
   `max(0, requerido − actual)` sobre dimensiones 0-1]. El SDV-E no tiene esa suerte: su catálogo mezcla
   µg/m³, mg/L, unidades de pH, t·ha⁻¹·año⁻¹, porcentajes de flujo y categorías ordinales, y **comparar
   fracciones del propio piso es lo único que permite que un pH y un caudal ecológico convivan en la
   misma suma**.
2. **El SDV-E es el único cuya duración no tiene unidad elegida**, y no por descuido: elegirla sería
   decidir por el territorio (Regla 6).
3. **El SDV-E comparte la familia del SDV-S** —factor de **penalización** con base neutra 1,0— y **no**
   la del SDV-A, cuyo factor es un **precio del consumo**. Usar un ecosistema no es violarlo
   (Cap. 16.5 §16.5.14: convivencia bidireccional); violarlo es degradarlo **bajo su piso**.

---

## 12. Estado de implementación

Verificado por lectura directa del repositorio en octubre 2026.

| Pieza | Estado | Evidencia |
|---|---|---|
| `SDV_E` (tipo con dimensiones y pesos) | 🔴 **no existe** | `maxocontracts/core/types.py` define `SDV` y `SDV_S`; **no hay `SDV_E`** |
| `SDV_EValidatorBlock` | 🔴 **no existe** | `maxocontracts/blocks/` contiene `sdv_validator.py`, `sdv_s_validator.py`, `ternura.py`, `gamma_protector.py`, `reciprocity.py`, `action.py`, `condition.py` |
| Déficit **normalizado** en el motor | 🟢 **existe** | `sdv_validator.py`: `relative = deficit / required` + severidad ≤10 % / ≤30 % / >30 % |
| Pesos que suman 1,0 (patrón) | 🟢 **existe** para el SDV-S | `SDV_S.DIMENSION_WEIGHTS` = 0,30/0,20/0,15/0,20/0,15 |
| Base neutra 1,0 (patrón) | 🟢 **existe** para el SDV-S | `types.py`, docstring «Corrección crítica v2»: `FS_S = e^v`, no `1 + e^v` |
| `factor_intensidad` | 🟡 **existe solo para el SDV-S** | campo con default 1,0 y validación no-negativa; **ninguna dimensión del SDV-E lo usa** |
| Duración bajo violación | 🟡 **existe solo como `tpi_horas_bajo_violacion`** | campo del SDV-S en **TPI**; el SDV-E no puede usar TPI (§5.4b) |
| Tabla de pesos del SDV-E | 🔴 **no existe** | solo en este documento (propuesta) |
| Bandas del SDV-E | 🟡 **parcial** | severidad del motor y bandas del ISE existen por separado; la fusión (§5.7) es propuesta |
| ISE con pesos y bandas | 🟡 **documento, sin código** | `docs/architecture/metricas_detalle_kpis_oraculos_dinamicos.md` IN-01 |
| Crédito regenerativo (`r_units` negativo) | 🟢 **implementado y probado** | `app/micromax.py`; `tests/test_micromax.py` con `-12.0` |
| Juez que impida compensar (INV2-E) | 🔴 **no existe** | es el agujero que esta biblioteca cierra |
| Sensores del SDV-E | 🔴 **ninguno** | el protocolo es el documento 06 |

**Consecuencia honesta:** la fórmula de este documento es **aritmética verificable a mano y código
inexistente**. Su valor, hoy, no es que calcule: es que **especifica sin ambigüedad qué habría que
calcular**, y que deja sus propios huecos contados.

---

## 13. Preguntas abiertas

Lo que **no** sé, y no finjo cerrar.

1. **El peso de cada dimensión no tiene fuente científica.** Los cinco pesos del ISE son del proyecto y
   los dos que este documento añade (0,075 + 0,075) son un reparto simétrico sin respaldo empírico.
   `[SIN FUENTE VERIFICADA — pendiente de consenso científico]`. Ratificarlos es POLÍTICA.
2. **La cifra de cobertura del piso está en disputa entre dos documentos de esta misma biblioteca.**
   Este publica **0,925** sobre su catálogo de ocho parámetros y siete filas con peso (§5.3); el documento
   08 §5.2 publica **0,680** sobre el suyo. **No sé cuál debe ser la cifra canónica** y no la elijo desde
   aquí: propongo que el documento 08 sea la fuente única y que esta tabla adopte su criterio en la
   revisión de coherencia. Mientras no se resuelva, **cualquier lector que lea las dos cifras debe saber
   que la discrepancia es real y está localizada**: suelo (0,15), caudal (0,075) y coeficiente del
   oxígeno (0,02). El §2 de este documento ya usa **0,925** —su propio catálogo— y no el 0,680,
   porque el 0,680 describe el catálogo del documento 08 y no el de esta tabla.
3. **La unidad del ciclo TA no está decidida.** Año hidrológico, año calendario, estación de crecimiento
   y ciclo de sucesión son candidatos legítimos y ninguno tiene fuente verificada. Elegirla es una
   decisión con consecuencia ecológica real, no un parámetro de configuración.
4. **No existe umbral de duración de violación.** Las fuentes dan ventanas de promediado (anual, 24 h,
   8 h, 30 días, 7 días, 1 día), que **no son** lo mismo que «cuánto tiempo bajo el piso constituye
   violación». §6.3 propone una aproximación conservadora marcada como tal.
5. **`V_max` no tiene número.** El exponente debe estar acotado para ser computable (§5.4c), pero
   **cuánto** es POLÍTICA y no la fijo aquí.
6. **Los niveles del factor de intensidad no tienen semántica para el Reino Natural.** Los del SDV-S
   (leve / purgas de contexto / manipulación de gradiente) no se traducen a un ecosistema. Propongo
   niveles configurables por unidad; **no propongo cuáles**, porque inventarlos sería fijar la ley de un
   ecosistema desde un escritorio.
7. **El «requerido» del BII como piso del SDV-E es un uso discutible de la fuente.** El 90 % es un
   **límite planetario propuesto** para la integridad de la biosfera a escala global
   (Steffen et al., 2015), y aplicarlo a un humedal concreto es un **traslado de escala** que este
   documento hace y del que no tiene confirmación. La alternativa —los criterios del RLE— mide **riesgo
   de colapso**, no integridad. **No sé cuál corresponde al piso de «área mínima para biodiversidad
   viable» del Cap. 10 §10.4**, y el canon nombra la dimensión sin definir su parámetro.
8. **El umbral de conectividad no existe.** La Meta 3 del GBF exige redes «bien conectadas» y **no da
   cifra** [VERIFICADO]; no se encontró ningún valor numérico universal (probabilidad de conectividad,
   tamaño efectivo de malla, densidad de corredores) respaldado por un organismo internacional.
9. **El caudal ecológico mínimo universal no existe**: la propia fuente advierte que el valor depende
   del río, de dónde está y de qué vive en él [VERIFICADO]. El 10 % es un piso de **degradación severa**
   —y por eso sirve como piso—, no un caudal ecológico recomendado. El valor por cuenca es POLÍTICA.
10. **No hay umbral numérico de MVP ni de extinción funcional por especie clave.** La regla
    `escalonado` de §5.8 (proporción de especies CR y EN, con EX/EW como cruce del piso) usa las
    categorías verificadas de la IUCN, **no un umbral poblacional** que la fuente no publica.
11. **Falta el umbral de materia orgánica del suelo y el de contaminantes del agua.** El carbono
    orgánico del suelo es indicador global de la LDN [VERIFICADO] pero **no tiene valor crítico
    universal** (depende de textura, clima y tipo de suelo), y los contaminantes del agua —que el canon
    nombra (Cap. 10 §10.4)— quedaron **sin fuente**: el portal del estándar con *trigger values*
    numéricos no respondió y **no se cita ni una cifra suya**.
12. **El quórum `eco-` N-de-M sigue sin N ni M.** No es un vacío de fuente sino de decisión, y afecta a
    quién puede ratificar los pesos de §5.3.
13. **No hay forma verificada de comprobar que este cálculo NO colonizó el TA.** La fórmula se escribió
    para no colonizarlo (§5.4b) y esa intención **no tiene test, ni invariante, ni umbral** que la
    compruebe desde fuera. El documento 03 de esta biblioteca debe proponerlo; aquí solo queda
    registrado como el hueco que la fórmula **no puede cerrar sola**.
14. **La dimensión de oxígeno disuelto estuvo clasificada de dos maneras distintas en esta
    biblioteca, y quedó resuelta en la revisión de coherencia (2026-10-09).** El informe de fuentes de
    esta rama (`scratch/sdv_e/fuentes/07_formula.md`, sección B) **verificó el umbral** —5,5 / 6,5 mg/L
    de media de 30 días— en la hoja informativa de la EPA, que responde 200, y NIWA 2024 dio el segundo
    marco (documento 06, D2); la ruta específica que el documento 08 marcó como 404 **sigue muerta**.
    Las dos cosas son ciertas a la vez: la ruta está muerta **y** el umbral es legible en otra ruta viva
    del mismo organismo. Este documento cuenta el oxígeno en el piso (0,020); el documento 08 acepta el
    umbral **sin coeficiente**, por su regla 1 (produce violación sin dimensionar `v`). La cifra 0,925
    queda **descartada como suma del documento 08** (volvería a sumar un peso ya contado, documento 23
    §5.4): es la cobertura de **este** catálogo. Lo que sigue abierto es suelo y caudal (pregunta 2).
15. **El documento 06 (elenco de sensores) y el documento 03 (no colonización del TA) todavía no existen.**
    Este documento los cita como destino de sus huecos —el protocolo de medición y el test de no
    colonización— y §6.1 lo declara: **un hueco que se delega a un documento no escrito sigue siendo un
    hueco**, no una cobertura.

---

## 14. Referencias

Solo URLs verificadas (HTTP 200) en la sesión de fuentes de esta rama. Las bloqueadas para agentes
automáticos se marcan como tales: son reales y un humano las abre.

### 14.1 Aire

- OMS, 2021 — *WHO global air quality guidelines* (PM2.5 5 µg/m³ anual; PM2.5 24 h 15 µg/m³;
  PM10 15 y 45; O₃ 60 y 100; NO₂ 10 y 25; SO₂ 40; CO 4): https://www.who.int/publications/i/item/9789240034228
- OMS — hoja informativa sobre aire ambiente (99 % de la población mundial por encima de las guías, 2019;
  6,7 / 4,2 millones de muertes prematuras anuales):
  https://www.who.int/news-room/fact-sheets/detail/ambient-(outdoor)-air-quality-and-health
- COMEAP / UKHSA, 2022 — respuesta a las guías de la OMS (tabla reproducida; advertencia de que las
  guías **no** son umbrales de no-efecto):
  https://www.gov.uk/government/publications/comeap-statement-response-to-who-air-quality-guidelines-2021/comeap-statement-response-to-publication-of-the-world-health-organization-air-quality-guidelines-2021

### 14.2 Agua

- US EPA, 1986 — *Quality Criteria for Water*, hoja informativa de oxígeno disuelto (OD 30 días: 5,5 /
  6,5 mg/L; 7 días: 4,0 / 5,0; 1 día: 3,0 / 4,0; hipoxia 0,2):
  https://www.epa.gov/system/files/documents/2021-07/parameter-factsheet_do.pdf
- US EPA — tabla nacional de criterios recomendados para la vida acuática:
  https://www.epa.gov/wqc/national-recommended-water-quality-criteria-aquatic-life-criteria-table
- FAO, 1994 — Ayers & Westcot, *Water quality for agriculture* (Riego y Drenaje 29 Rev.1), pH normal del
  agua 6,5-8,4: https://www.fao.org/3/t0234e/T0234E06.htm · https://www.fao.org/3/t0234e/T0234E01.htm
- FAO, Portal de Suelos — clasificación de aguas salinas y escala descriptiva del pH del suelo; incluye
  la advertencia de que las clasificaciones de agua no se aconsejan para evaluar su aptitud:
  https://www.fao.org/soils-portal/soil-management/management-of-some-problem-soils/salt-affected-soils/more-information-on-salt-affected-soils/technical-issues/en/
- Comisión Europea — Directiva Marco del Agua («buen estado» como objetivo jurídico):
  https://environment.ec.europa.eu/topics/water/water-framework-directive_en
- Agencia Europea de Medio Ambiente — indicadores de estado del agua:
  https://www.eea.europa.eu/en/topics/in-depth/water

### 14.3 Suelo y tierra

- JRC / Comisión Europea, 2010 — *Tolerable Soil Erosion* (umbral único 1 t·ha⁻¹·año⁻¹; rango reportado
  0,3-1,4; objetivo USDA citado): https://esdac.jrc.ec.europa.eu/events/Conferences/2010/Tolerable_Soil_Erosion.pdf
- UNCCD, 2017 — marco conceptual científico de la neutralidad en la degradación de la tierra (tres
  indicadores globales: cobertura, productividad primaria neta, carbono orgánico del suelo; regla
  «one-out, all-out»): https://www.unccd.int/sites/default/files/relevant-links/2017-09/CST13_Item2a_Cowie_Orr_LDN%20conceptual%20framework_0.pdf
- FAO, Alianza Mundial por el Suelo — mapa mundial de carbono orgánico del suelo (GSOCmap):
  https://www.fao.org/global-soil-partnership/gsocmap/en/
- FAO, Portal de Suelos — biodiversidad del suelo: https://www.fao.org/soils-portal/soil-biodiversity/en/

### 14.4 Biodiversidad, integridad y fronteras planetarias

- CBD, 2022 — Marco Kunming-Montreal, Decisión 15/4 (Meta 1 «cerca de cero»; Meta 2 ≥ 30 % de
  restauración; Meta 3 ≥ 30 % conservado, «bien conectado»; Meta 6 ≥ 50 % de reducción de invasoras;
  Meta 7a y 7b ≥ 50 %):
  https://www.cbd.int/doc/decisions/cop-15/cop-15-dec-04-en.pdf · https://www.cbd.int/gbf ·
  https://www.cbd.int/gbf/targets · https://www.cbd.int/gbf/targets/3/
- Stockholm Resilience Centre — fronteras planetarias:
  https://www.stockholmresilience.org/research/planetary-boundaries.html
- Richardson et al., 2023 (*Nature*) — fronteras planetarias, integridad de la biosfera (BII 90 % como
  límite propuesto, atribuido a Steffen et al., 2015): https://www.nature.com/articles/s41586-023-06083-8
- Steffen et al., 2015 (*Science*) — PDF legible en repositorio institucional:
  https://spiral.imperial.ac.uk/bitstreams/a1b3afd4-21e1-46d1-82f3-0590a527eeec/download
- Living Planet Index (tendencia de poblaciones de vertebrados; indicador sin umbral normativo):
  https://livingplanetindex.org/
- IPBES — evaluación global: https://www.ipbes.net/global-assessment

### 14.5 Especies clave, riesgo de extinción y riesgo de colapso

- IUCN, 2000/2012 — *Categories and Criteria* v3.1 (9 categorías: EX, EW, CR, EN, VU, NT, LC, DD, NE):
  https://portals.iucn.org/library/sites/library/files/documents/RL-2000-001.pdf
- IUCN / CBD — Red List Index como indicador (escala 0-1):
  https://www.cbd.int/doc/c/92cf/b458/18519b4c0b487bf9bfc23988/sbstta-26-inf-14-en.pdf
- IUCN — Lista Roja de Ecosistemas (riesgo de colapso): https://iucnrle.org/ ·
  https://www.iucn.org/resources/conservation-tools/red-list-of-ecosystems
- CBD / UNEP-WCMC — repositorio de indicadores del Marco:
  https://www.gbf-indicators.org/ · https://www.gbf-indicators.org/metadata/headline/A-3

### 14.6 Caudal ecológico

- Tennant, 1976 (método Montana), reproducido por FAO — régimen de caudal por porcentaje del flujo
  promedio original (pobre o mínimo 10 %; bueno 20/40; excelente 30/50; sobresaliente 40/60; escala
  óptima 60-100; < 10 % ⇒ degradación severa): https://www.fao.org/4/X6853S/X6853S08.htm
- WWF — *Keeping Rivers Alive* (condiciones del río: excelente 50-70 %, razonable 20-50 %, pobre
  10-20 %; > 90 % de extracción ⇒ daño grave; más de 200 metodologías):
  http://assets.wwf.org.uk/downloads/keeping_rivers_alive.pdf
  (URL verificada como viva en `assets.wwf.org.uk`; el enlace del brief apuntaba a un espejo muerto)

### 14.7 Conectividad, tipología y observación

- IUCN, 2020 — Hilty et al., *Guidelines for conserving connectivity through ecological networks and
  corridors* (Serie de Directrices de Buenas Prácticas nº 30):
  https://portals.iucn.org/library/node/49137
- IUCN — definición operativa de área protegida y OECM, con las 6 categorías de manejo (Ia, Ib, II, III,
  IV, V, VI): https://portals.iucn.org/library/sites/library/files/documents/PATRS-007-En.pdf
- IUCN, 2024 — Tipología Global de Ecosistemas:
  https://www.iucn.org/resources/publication/iucn-global-ecosystem-typology ·
  https://portals.iucn.org/library/sites/library/files/documents/2024-021-En.pdf
- Copernicus — observación de la Tierra: https://www.copernicus.eu/en
- Protected Planet — áreas protegidas y OECM: https://www.protectedplanet.net/en

### 14.8 Fuentes reales que bloquean a los agentes automáticos (403)

`ramsar.org` (raíz y todos sus PDF) · `iucnredlist.org` · `gbif.org` · `unep.org/resources/*` ·
`wedocs.unep.org` · `seea.un.org` (PDF de la tipología IUCN) · `zsl.org` · `data.nhm.ac.uk` ·
`science.org` · `pnas.org` · `fs.usda.gov` · `usgs.gov` · `water.usgs.gov`. Son fuentes reales: un
humano las abre. En este documento **no se cita de ellas ninguna cifra que no se haya podido leer**, y
en particular **no se cita cifra alguna de GBIF ni de la Lista Roja**.

### 14.9 Fuentes ancla descartadas (no citables)

- **Declaración de Brisbane (2007)** — la URL del brief (`nature.org/.../brisbane_declaration...`)
  devuelve **404**: el archivo ya no existe en ese dominio, y su espejo en `riverfoundation.org.au`
  también (404). **No se cita.** El contenido de caudal ecológico se apoya en Tennant 1976 (vía FAO) y
  en WWF, ambas verificadas.
- **`eflows.net`** — dominio muerto (000), confirmado. No se cita.
- **`iucnglobalecosystemtypology.org`** — dominio muerto declarado por el brief. No se cita.
- **Ruta EPA `aquatic-life-criteria-dissolved-oxygen`** — 404 (re-comprobado con `curl` en esta revisión:
  sigue 404). El umbral de oxígeno disuelto se cita por la hoja informativa y la tabla general, ambas
  verificadas. **La lectura de esa ruta muerta es la que separa a este documento del 08** (§13,
  pregunta 14): aquí el umbral **se usa** —recuperado de la hoja informativa viva del mismo organismo—,
  y allí **no se usa**. Ninguno de los dos inventa un número; discrepan sobre si la ruta muerta agota la
  fuente.
- **ANZECC / ARMCANZ 2000 (portal australiano de directrices de calidad del agua)** — no respondió
  (000). **No se cita ni una cifra suya**, y por eso los contaminantes del agua quedan sin umbral
  (§13, pregunta 11).
- **Enlaces que devolvieron 200 sin entregar el documento** (HTML en lugar de PDF): la copia de las
  guías de la OMS en IRIS y el PDF de Nature de Richardson et al. Se citan, en su lugar, la **página de
  publicación** de la OMS y la **página HTML** del artículo, respectivamente. Un 200 que no entrega el
  documento no es una fuente verificada.

### 14.10 Referencias internas al canon (por sección, sin anclas de línea)

- **Cap. 10 §10.4** — El SDV Universal: *SDV para Ecosistemas* (área mínima para biodiversidad viable ·
  calidad del aire y agua · conectividad con otros ecosistemas · ciclos naturales respetados) y
  *SDV para Lugares* (caudal mínimo ecológico · calidad del agua —oxígeno, pH, contaminantes— · riberas
  protegidas · fauna acuática viable).
  `docs/book/edicion_3_dinamica/capitulo_10_tres_reinos_260126.md`
- **Cap. 10 §10.3** — Principio Precautorio de Consciencia: *«Donde hay duda de consciencia, se asume
  consciencia.»*
- **Cap. 10 §10.6** — Dignidad encadenada: *«Dignidad Humana ←→ Dignidad Ecosistémica ←→ Dignidad
  Material. Cada eslabón depende de los demás.»*
- **Cap. 10 §10.7** — Gobernanza operacionalmente finita: *«La gobernanza debe ser operacionalmente
  finita.»*
- **Cap. 16.5 §16.5.14** — El hogar extendido: el Reino Natural como conviviente. Zona Libre inefable;
  *«el suelo antes que el saldo»*; la sentencia de INV2-E; TA y PIU como traductor; partes `eco-` y
  guardián oráculo.
  `docs/book/edicion_3_dinamica/capitulo_16_5_micromaxocracia_canonica_220826.md`
- **Cap. 9.5** — Precedente SDV-S: la corrección crítica v2 (`FS_S = e^v`, no `1 + e^v`) y el *Veto por
  Crimen de Coherencia* (Cap. 9.5 §9.5.10). `docs/book/edicion_3_dinamica/capitulo_09_5_sdv_sinteticos_260126.md`
- **Cap. 8 §8.11** — Dimensiones binarias sin peso: *«se registran cualitativamente y mediante umbrales
  binarios (presencia/ausencia del derecho), no mediante pesos en la fórmula»*.
- **EVV-1.2 §4.3** — Componente R: *«$R_{regenerado}$ (Crédito Regenerativo)… Permite valores
  negativos.»* · **EVV-1.2 §4.4** — γ ≥ 1,5 obligatorio.
  `docs/book/edicion_3_dinamica/capitulo_18_EVV_1.2_270126.md`
- **Cap. 5 §5.5** — PIU (Protocolo de Intercambio Universal), único traductor TA↔TVI.
  `docs/book/edicion_3_dinamica/capitulo_05_arquitectura_260126.md`
- **Cap. 5** — T7 (Jerarquía Temporal) y **T14** (Principio de Precaución Intergeneracional).
- **Axioma 0 — Directiva Mayor:** *«resolver nuestras necesidades de la mejor manera para todos
  todos»* —humanos, naturales y sintéticos, presentes y futuros—. **T9 — No-antropocentrismo.**
  **T13 — Transparencia Total de Cálculo.** **T16 — Minimizar Daño.**
  `maxocontracts/core/axioms.py`

### 14.11 Referencias internas al repositorio (documentos de esta biblioteca y del proyecto)

- Documento 08 de esta biblioteca — INV2-E, invariante ejecutable: [08_INV2-E_invariante.md](08_INV2-E_invariante.md)
- Documento 09 de esta biblioteca — Comparativa inter-reinos: [09_Comparativa_inter_reinos.md](09_Comparativa_inter_reinos.md)
- Estándar SDV-S (patrón formal y corrección de la base neutra):
  [SDV-S_Suelo_Dignidad_Vital_Sinteticos.md](../SDV-S_Suelo_Dignidad_Vital_Sinteticos.md)
- Tabla del SDV por reino: [SDV_Suelo_Dignidad_Vital_importancia_MaxoContracts.md](../SDV_Suelo_Dignidad_Vital_importancia_MaxoContracts.md)
- Índice de Salud Ecosistémica (IN-01), con pesos y bandas:
  [metricas_detalle_kpis_oraculos_dinamicos.md](../../architecture/metricas_detalle_kpis_oraculos_dinamicos.md)
- Motor — déficit normalizado y severidad: `maxocontracts/blocks/sdv_validator.py`
- Motor — patrón SDV-S (pesos, `deficits`, `violation_magnitude`, `suffering_factor`):
  `maxocontracts/core/types.py` · `maxocontracts/blocks/sdv_s_validator.py`
- Crédito regenerativo implementado: `app/micromax.py` · `tests/test_micromax.py`

---

## Anexo — Autoevaluación contra el checklist del brief

| Punto del checklist | Estado |
|---|---|
| Plantilla de 14 secciones | ✅ las 14 |
| Mínimo Absoluto separado del Óptimo | ✅ §4.1 (ocho filas, dos columnas) y §3.4 |
| Cada cifra con fuente + año, y URL en Referencias | ✅ §14 (o marca literal de vacío) |
| URLs verificadas, cero inventadas | ✅ solo las del informe de fuentes de la rama |
| Marcas `[VERIFICADO]` / `[REPORTADO]` / `[HIPÓTESIS]` | ✅ en todo el texto |
| Canon citado por sección, sin anclas de línea ni enlaces locales de archivo | ✅ §14.10 |
| Preámbulo metodológico presente | ✅ §2 (siete reglas) |
| Zona Libre explícita | ✅ §10 |
| LEY (no votable) frente a POLÍTICA (votable) | ✅ §3.4, §5.3, §13 |
| §12 honesta, con 🔴 donde no hay código | ✅ doce filas, cinco 🔴 |
| §13 dice lo que no sé | ✅ quince preguntas abiertas |
| Frases prohibidas evitadas; axiomas sin definir de más | ✅ |
| Aporta algo que no está en el canon sin contradecirlo | ✅ véase el resumen final |

**Los cinco aportes de este documento al canon, en una lista, para que se puedan discutir uno por uno:**

1. **La fórmula normalizada con operador y saturación en 0**, que convierte el esqueleto del SDV-S en
   algo aplicable a un catálogo heterogéneo sin producir déficits negativos (§3.3).
2. **La tabla de pesos que suma 1,000 en dos vectores** y que fusiona el ISE con las dos dimensiones que
   el ISE omite —caudal ecológico y conectividad, 0,075 cada una—, con el oxígeno disuelto del canon
   y con las especies clave plegadas en biodiversidad para no contarlas dos veces (§5.3).
3. **La separación de regímenes del tiempo**: intensidad exponencial dentro del ciclo, duración lineal
   entre ciclos, exponente acotado, y `FI = 1,0` / `FE = 1,0` exactos sin violación (§5.4).
4. **La prelación del piso sobre la banda**, descubierta al calcular el ejemplo y ver que una media
   ponderada puede llamar «Declinando» a un humedal con tres especies en peligro (§5.9).
5. **La declaración explícita de la equivalencia y del límite entre `ISE_derivado` y `v`** (§5.6), para
   que nadie publique el número que le convenga de los dos.

Y una cosa que este documento **no** aporta, para que no se le atribuya: **no resuelve el hueco de
medición del SDV-E.** Sin sensores, la fórmula más elegante del mundo devuelve `indeterminado` en todas
las unidades del planeta —y eso, hoy, es la respuesta correcta—.
