# Océanos y costas: el SDV-E del arrecife, la pesquería y la orilla
## Los mínimos del sistema marino-costero: estrés térmico del arrecife por semanas, saturación de aragonito, cobertura viva, biomasa pesquera, protección efectiva, carbono azul, oxígeno y la orilla que se mueve

**Autoría:** Oráculo Sintético DeepSeek & Max Nelson López Restrepo
**Fecha:** octubre 2026
**Proyecto:** Maxocracia — El gobierno de la verdad, el tiempo y la vida
**Licencia:** Creative Commons BY-SA 4.0
**Estado:** Propuesta de estándar (rama SDV-E, Ola 4) — NO canon hasta ratificación
**Referencia canónica:** Cap. 10 §10.4 · Cap. 16.5 §16.5.14 · EVV-1.2 §4.3 · Cap. 9.5 (precedente SDV-S)
**Documento:** 13 de la biblioteca `docs/theory/SDV-E/`
**Revisión:** octubre 2026 — primera redacción. Aplica la revisión adversaria del documento
[09](09_Comparativa_inter_reinos.md) (déficit normalizado, protocolo de medición explícito,
frontera LEY/POLÍTICA declarada, estado de implementación honesto). Ninguna cifra de este documento
se apoya en una URL sin estado HTTP registrado, y todo lo que no tiene fuente se declara como
`[SIN FUENTE VERIFICADA]`.

---

## 1. Qué es (y qué no es) este SDV

**Qué es.** Este documento fija los mínimos del **ecosistema marino y costero** bajo el estándar
SDV-E: el arrecife de coral, la columna de agua que lo sostiene químicamente, la pesquería que
extrae de él, la red de áreas protegidas que debería contenerlo, el manglar y la pradera marina
que amortiguan la costa, el oxígeno que decide quién puede vivir en ella, y la propia orilla
—intermareal, estero, marisma, delta— donde el mar y la tierra negocian cada marea.

Existe por tres razones concretas, y las tres son hallazgos de la sesión de verificación de esta
rama, no entusiasmo temático:

1. **El océano es el único ecosistema del proyecto cuyo piso ya está publicado con significado
   biológico declarado y con unidad de duración.** NOAA Coral Reef Watch no publica *un* número:
   publica una escala de cinco tramos donde el tramo 4 significa «**blanqueamiento probable**» y el
   tramo 8 significa «**mortalidad probable**» `[VERIFICADO]`. Eso permite separar el **Mínimo
   Absoluto** del **Óptimo** con fuente oficial, sin inventar ninguno de los dos — que es
   exactamente lo que la §2.1 del brief manda hacer y lo que el motor del SDV-H no supo hacer.
2. **El océano es el ecosistema donde la contabilidad puede mentir más fácilmente.** Créditos de
   carbono azul, jardinería de coral, arrecifes artificiales y «restauración» de manglar conviven
   con la pérdida neta de los tres. La FAO documenta que **el 82 % de la ganancia mundial de
   manglar fue expansión natural y solo el 18 % restauración** `[VERIFICADO]`: es la confirmación
   externa exacta del principio canónico *"se registra lo que regenera, no lo que adorna"*
   (Cap. 16.5 §16.5.14).
3. **El océano es donde el canon tiene razón y la fuente todavía no.** El canon nombra
   conectividad y ciclos naturales (Cap. 10 §10.4); la Meta 3 del Marco Kunming-Montreal exige
   redes «bien conectadas» y **no publica ninguna cifra de conectividad** `[VERIFICADO]`. Y para
   la **zona intermareal y los esteros no existe hoy ningún umbral numérico con fuente de organismo
   abierta** en esta sesión: `ramsar.org` devuelve 403 en las cuatro rutas probadas, de modo que el
   marco Ramsar —criterios 2 a 4: especies vulnerables, aves acuáticas y peces— queda **citado como
   marco cualitativo de la Convención y no como umbral numérico verificado**. Este documento escribe
   esa dimensión igual, y la escribe **declarando que no tiene umbral numérico con fuente**.

**El agujero que esta rama cierra, dicho con la frase literal del canon:**

> *"Un conjunto con crédito regenerativo acumulado pero humedal bajo su SDV-E no está en coherencia:
> **INV2-E será su juez**."* — (Cap. 16.5 §16.5.14)

Hoy un hotel costero puede plantar manglar, registrar `r_units` negativos y acumular crédito
regenerativo **mientras su arrecife cruza el umbral de mortalidad probable**, y el sistema no lo
detecta: `r_units` está registrado pero no pesa en ninguna cuenta, y no existe `SUM(r_units)` ni
juez alguno. Aplicado al mar, el agujero es literal: la única pieza que hoy *existe* en el código
es el crédito; la que falta es el estándar y su invariante.

**Qué no es.**

- **No es el estándar completo del SDV-E.** La doctrina, la unidad y el sujeto, la no colonización
  del TA, la representación por guardián y la fórmula viven en los documentos 00-09 de esta
  biblioteca. Aquí se aplican al mar y se declara explícitamente cada vez que una decisión
  pertenece a otro documento.
- **No es una política pesquera, ni un plan de AMP, ni un tratado.** Fija el **piso** por debajo del
  cual la unidad pierde integridad, no el techo de captura ni el reparto de cuotas, que son
  decisiones humanas legítimas y votables.
- **No es un componente del ISE.** El Índice de Salud Ecosistémica (5 componentes: biodiversidad
  30 %, calidad del agua 20 %, calidad del aire 20 %, salud del suelo 15 %, poblaciones de especies
  clave 15 %) **no tiene ningún componente marino**: la única dimensión que podría tocar el mar es
  «calidad del agua» `[VERIFICADO]` leyendo
  [metricas_detalle_kpis_oraculos_dinamicos.md](../../architecture/metricas_detalle_kpis_oraculos_dinamicos.md).
  Este documento no amplía el ISE: construye la primera lista marina del SDV-E.
- **No es canon.** Es una propuesta de estándar de la rama SDV-E, Ola 4, **no ratificada**.

---

## 2. Preámbulo metodológico

El SDV-H lo tiene, el SDV-S lo omitió y la §2 del brief prohíbe repetir la omisión. En un documento
sobre el océano el preámbulo es obligatorio por una razón adicional: **la literatura marina está
llena de cifras de estado que se leen como si fueran umbrales.** «El 62,3 % de las poblaciones está
dentro de niveles sostenibles» no es un piso; es una fotografía. Ocho reglas, entonces.

**Regla 1 — Estándar primero, contabilidad después.** El orden es canónico: *"estándar primero,
contabilidad después"* (Cap. 16.5 §16.5.14). Este documento no propone sensores productivos ni
créditos: propone el piso, y deja la contabilidad para `INV2-E` (documento 08).

**Regla 2 — Mínimo Absoluto y Óptimo, siempre en dos columnas.** Nunca se funden. El piso es
**LEY** y no se vota; la plenitud es **POLÍTICA** y sí se vota (precedente del Parlamento
Educativo, INV2-EDU: categoría `critical`, quórum 60 %, consenso 75 %, T13, anti-flip-flop
14 días, `CHECK` en BD). En este documento la separación es especialmente delicada, porque la
fuente publica **tres** tramos donde el brief exige **dos** columnas (arrecife: 4 y 8). La regla
que se aplica aquí, y que se justifica en la Dimensión I, es: **el piso es el tramo donde la fuente
declara un desenlace biológico (mortalidad), no el tramo donde declara una probabilidad
(blanqueamiento).**

**Regla 3 — Un valor de estado no es un umbral.** Toda cifra de estado va marcada «(estado, no
umbral)». Es la convención del informe de fuentes de este documento y este documento la respeta
fila por fila. Confundir estado con umbral es el error que produjo el desastre del agua en el
SDV-H.

**Regla 4 — La celda vacía es un hallazgo, no un hueco de redacción.** Cuando no hay fuente, se
escribe literalmente `[SIN FUENTE VERIFICADA — pendiente de consenso científico]`. Este documento
tiene **cuatro vacíos que bloquean dimensiones enteras** (hipoxia numérica, `B/Bmsy`, conectividad
marina, zona intermareal y esteros) y los declara en el cuerpo del texto, no en una nota al pie.

**Regla 5 — Distinguir «no existe» de «no lo sé».** Cuatro casos distintos, marcados distinto:
(a) no existe en el canon; (b) existe en el canon y no en el código; (c) existe la fuente y no se
verificó; (d) se buscó y no hay fuente. La §12 es el inventario de (b); la §13, el de (c) y (d).

**Regla 6 — El mar tiene tres ejes y el estándar debe declararlos.** Un parámetro marino no es un
número: es un número **con profundidad, con estación y con superficie de muestreo**. Dos lecturas
de la misma unidad pueden diferir solo por el diseño de muestreo. Por eso el protocolo de medición
(§6) es aquí **condición de posibilidad del estándar** y no anexo técnico: sin diseño declarado no
hay dato comparable, y sin dato comparable no hay violación demostrable.

**Regla 7 — El tiempo del mar es TA.** El tiempo del arrecife, del manglar y del estero es
**Tiempo Absoluto (TA)** y **no se coloniza**: *"El tiempo del territorio es TA y no se coloniza
(el PIU traduce)"*. No se mide en TVI ni en TPI. El **PIU** (Protocolo de Intercambio Universal,
Cap. 5 §5.5) es el **único** traductor TA↔TVI, y hoy es un `pass` con comentario `[VERIFICADO]`:
la traducción existe como doctrina, no como ejecución. Consecuencia práctica: la duración de una
violación marina se acumula en **temporadas térmicas, ciclos hidrológicos y ciclos de sucesión**,
nunca en horas humanas dentro de la fórmula.

**Regla 8 — Fuente con año, URL con estado, y año de consulta cuando no hay año de edición.**
Cuando el organismo no publica año de edición del producto (es el caso de los productos satelitales
de NOAA Coral Reef Watch), este documento cita **«consulta: octubre 2026»** y lo declara. No se
atribuye a NOAA un año que NOAA no publica.

**Nota sobre las marcas.** `[VERIFICADO]` significa que la cifra fue leída en la fuente en la
sesión de verificación HTTP de esta rama (octubre 2026), registrada en el informe de fuentes del
documento 13. `[REPORTADO]` significa que la cifra existe citada pero **no** se leyó en fuente
primaria. `[HIPÓTESIS]` es inferencia razonada del proyecto. **Una cifra `[REPORTADO]` o
`[SIN FUENTE VERIFICADA]` en el informe de fuentes no mejora de marca al entrar en este
documento.**

---

## 3. Pilares epistemológicos

Ocho pilares sostienen el SDV-E marino. Los cinco primeros son los del estándar; los tres últimos
son específicos del océano y se declaran aquí por primera vez.

1. **Proporcionalidad (Cap. 10 §10.5).** El nivel de protección debe ser *"lógico, proporcional y
   adecuado a la naturaleza de la entidad"*. Un arrecife no recibe el trato de una persona ni el de
   una cuchara: recibe el trato que su naturaleza exige. Esto es lo que permite que su piso se
   exprese en grado-semanas y no en litros.
2. **Dignidad encadenada (Cap. 10 §10.6).** *"Dignidad Humana ←→ Dignidad Ecosistémica ←→
   Dignidad Material. Cada eslabón depende de los demás."* En el mar el eslabón no es metáfora:
   **100-300 millones de personas** viven en zonas costeras con riesgo incrementado por la pérdida
   de hábitat costero protector `[VERIFICADO]` (IPBES, 2019). Proteger el manglar es contabilidad
   humana, no altruismo.
3. **T14 — Principio de Precaución Intergeneracional (Cap. 5).** *"Ante incertidumbre sobre el
   impacto en agentes que no pueden consentir (ecosistemas, generaciones futuras, posibles
   consciencias sintéticas), el sistema debe elegir la opción de menor irreversibilidad,
   documentando el costo de oportunidad asumido. La carga de la prueba recae sobre quien propone
   acciones que afectan la temporalidad de no-participantes."* **Es el axioma operativo de este
   documento**, por una razón medida: a 2 °C el declive proyectado de los arrecifes de coral es
   **superior al 99 %** (*very high confidence*, IPCC SR1.5, 2018) `[VERIFICADO]`. No hay
   «rehabilitación» contractual posible para esa pérdida: la prevención **es** el remedio
   completo, y T14 es la única herramienta que queda.
4. **No-antropocentrismo (T9).** El arrecife es sujeto del estándar, no recurso del inventario. El
   principio se aplica con dureza en la Dimensión IV: cuando no existe evaluación de stock, la
   carga de la prueba recae sobre quien extrae (T14), no sobre el pez.
5. **Principio Precautorio de Consciencia (Cap. 10 §10.3).** *"Donde hay duda de consciencia, se
   asume consciencia."* Para un arrecife o un estero la duda no es sobre consciencia sino sobre
   **identidad y continuidad**; el principio se aplica por analogía estructural: donde hay duda
   sobre si la unidad sigue siendo la misma unidad, se asume que sí y se documenta (documento 02).
6. **Gobernanza operacionalmente finita (Cap. 10 §10.7).** *"La gobernanza debe ser operacionalmente
   finita."* El océano es la mayor tentación del proyecto de modelar la cadena trófica completa
   —fitoplancton, zooplancton, peces forrajeros, depredadores apicales, flotas—. **Este documento
   no la modela.** Mide ocho dimensiones cerradas y ninguna más. Todo lo que no cabe en las ocho
   entra en la Zona Libre (§10) o queda como pregunta abierta (§13).
7. **El pilar nuevo: el auditor externo no pertenece al proyecto.** En los reinos humano, animal y
   sintético, alguien del propio sistema audita. En el mar, el instrumento de medida más
   importante —el par satelital HotSpot/DHW de NOAA Coral Reef Watch, 5 km, diario, serie desde el
   1 de enero de 1985, cobertura del **95 %** de los arrecifes del mundo— **no es propiedad del
   proyecto ni del beneficiario del uso** `[VERIFICADO]`. Es un hecho estructural que el SDV-E debe
   aprovechar: la contabilidad marina tiene, por primera vez en la familia, una fuente que el
   violador no puede editar. Y tiene un costo: **depende de un tercero** (§13).
8. **El pilar nuevo: el piso puede estar en la acción humana, no en el parámetro.** En siete de las
   ocho dimensiones el piso está en el ecosistema («no cruces este valor»). En la Dimensión VIII
   (costa y nivel del mar) **no puede estarlo**: el nivel del mar no depende de la unidad y no
   tiene piso. Ahí el piso se desplaza a la **acción humana**: no ocupar, no rellenar, no
   encauzar. Es la misma estructura de INV2 (el invariante juzga la acción, no al sujeto), y es un
   aporte de este documento a la doctrina del SDV-E.

---

## 4. Dimensiones del SDV-E (oceánicas y costeras)

### 4.1 Cómo se construyó esta lista

El canon manda proteger, para un ecosistema: área mínima para biodiversidad viable, calidad del aire
y del agua, conectividad con otros ecosistemas y ciclos naturales respetados; y para un lugar: caudal
mínimo ecológico, calidad del agua, riberas protegidas y fauna acuática viable (Cap. 10 §10.4). Ese
es el mandato. El instrumento del proyecto, el ISE, **no mide nada marino** `[VERIFICADO]`.

De modo que aquí no hay «fusión de dos listas» como en el documento 09: hay **una lista nueva**. Y
las dimensiones canónicas entran por derivación declarada, sin duplicar los documentos
transversales de la biblioteca:

| Dimensión canónica (Cap. 10 §10.4) | Dónde entra en este documento |
|---|---|
| Área mínima para biodiversidad viable | Dimensiones III, IV, VI (cobertura viva, biomasa, vegetación costera) + documento transversal 20 (Biodiversidad) |
| Calidad del agua | Dimensiones II y VII (saturación de aragonito, oxígeno) + documento transversal 23 (Agua y aire) |
| Conectividad con otros ecosistemas | Dimensión V (`bien conectadas`, requisito cualitativo de la Meta 3) + documento transversal 21 (Conectividad) |
| Ciclos naturales respetados | Dimensiones I (temporada térmica) y VII (ciclo de nutrientes) + documento transversal 22 (Ciclos naturales) |
| Fauna acuática viable | Dimensión IV (pesquerías) y Dimensión VII (oxígeno) |
| Riberas protegidas | Dimensión VI (manglar y pradera marina) y Dimensión VIII (intermareal y estero) |

**Nota de rutas.** Las cuatro entradas que remiten a los documentos 20-23 son **referencias a
documentos de esta biblioteca todavía no redactados** en la fecha de esta sesión: se citan **por su
número y su título previstos, sin enlace**, precisamente para no citar como existente un archivo que
no existe. Es una decisión de honestidad de rutas, no un descuido. Los enlaces relativos de la §14.9
sí apuntan a archivos existentes y verificados.

### 4.2 La unidad de medida (decisión prestada del documento 02)

La unidad del SDV-E es un problema abierto y pertenece al documento 02. Este documento **no lo
resuelve**, pero necesita operar, y opera con tres escalas declaradas, de menor a mayor:

- **Escala A — el sitio instrumentalizado.** El arrecife o el estero concreto que coincide total o
  parcialmente con un **píxel de 5 km** del producto de NOAA Coral Reef Watch y/o con una de sus
  **212 estaciones virtuales** regionales (activas desde octubre de 2016) `[VERIFICADO]`. Es la
  escala con mejor infraestructura de medida del estándar completo.
- **Escala B — la unidad de gestión costera.** Bahía, estero, marisma, delta o AMP con límites
  administrativos declarados. Es la escala donde vive la gobernanza real (Dimensión V).
- **Escala C — el gran ecosistema marino y la alta mar.** Incluye las Áreas Fuera de Jurisdicción
  Nacional (ABNJ), que son el **61 % del océano** y donde la cobertura protegida es del **1,45 %**
  `[VERIFICADO]`. Es la escala donde el SDV-E solo puede declarar estado, no violación imputable:
  **no hay sujeto obligado**.

Toda cifra de este documento se atribuye a una de las tres escalas. Cuando la escala no está
declarada en la fuente, se dice.

### 4.3 Resumen de dimensiones y pesos

| # | Dimensión | Qué protege en una frase | Peso propuesto `[HIPÓTESIS]` | Tipo de piso |
|---|---|---|---|---|
| **I** | Estrés térmico del arrecife (DHW) | Que el arrecife no cruce el umbral de mortalidad probable | 0,15 | Techo publicado (NOAA CRW) |
| **II** | Saturación de aragonito y acidificación | La química que permite formar esqueleto de carbonato | 0,15 | Piso con frontera planetaria (80 % preindustrial) |
| **III** | Cobertura viva y comunidad del arrecife | La existencia misma del arrecife como estructura viva | 0,15 | Piso de no regresión (sin umbral publicado) |
| **IV** | Biomasa y explotación pesquera | La viabilidad de la fauna marina explotada | 0,15 | Piso lógico del 100 % (sin umbral publicado por unidad) |
| **V** | Áreas marinas y costeras protegidas y gobernadas | Un régimen efectivo de protección sobre el hábitat crítico | 0,10 | **Mínimo de gobernanza** (tratado, no biología) |
| **VI** | Manglar y praderas marinas | La estructura viva que sostiene la costa y el carbono azul | 0,10 | Piso de no regresión |
| **VII** | Oxígeno disuelto, hipoxia y zonas muertas | Que haya fauna que pueda respirar | 0,10 | Piso de ausencia (0 zonas muertas) |
| **VIII** | Costa, nivel del mar y zona intermareal | La franja de transición y la seguridad de quien vive en ella | 0,10 | **Piso en la acción humana**, no en el parámetro |
| **IX** | **Zona Libre del océano (binaria, sin peso)** | Lo que no se mide y no debe medirse | **0,00 — fuera de la fórmula** | Presencia/ausencia de derecho (Cap. 8 §8.11) |

**Los pesos son una propuesta del proyecto, no un dato científico.** Ningún organismo publica pesos
porcentuales para estas dimensiones: `[SIN FUENTE VERIFICADA — pendiente de consenso científico]`.
La tabla reparte 1,00 entre ocho dimensiones (la novena no pesa por definición) y **es votable**
como POLÍTICA, mientras que los **umbrales de cada fila no se votan**.

---

### Dimensión I: Estrés térmico acumulado del arrecife (el latido del arrecife)

**Qué protege.** La capacidad del arrecife de atravesar su temporada cálida sin blanquearse hasta
morir.

| Parámetro | Mínimo Absoluto (el piso = LEY, no votable) | Óptimo (plenitud aspiracional = POLÍTICA, votable) | Fuente |
|---|---|---|---|
| **Anomalía de temperatura superficial del mar (HotSpot)** sobre la media mensual máxima (MMMSST) | **< 1 °C** — por debajo no se activa ninguna alerta de blanqueamiento | **≤ 0 °C** — tramo «No Stress», sin blanqueamiento | NOAA Coral Reef Watch (producto 5 km v3.1; consulta: octubre 2026) |
| **Estrés térmico acumulado (DHW, *Degree Heating Weeks*)** | **< 8 grado-semanas** — no alcanzar el *Bleaching Alert Level 2*, «**Mortality Likely**» (mortalidad probable) | **< 4 grado-semanas** — no alcanzar el *Bleaching Alert Level 1*, «Bleaching Likely» | NOAA Coral Reef Watch / NOAA OSPO (consulta: octubre 2026) |
| Zona intermedia (no es piso ni plenitud) | **4 ≤ DHW < 8** con HotSpot ≥ 1 — «blanqueamiento probable»: **zona de aviso**, con obligación de reportar e instrumentar, **no de violación** | — | NOAA Coral Reef Watch (consulta: octubre 2026) |
| Umbral de blanqueamiento por SST | — (es local, no universal) | **MMMSST + 1 °C** — media mensual máxima de SST más 1 °C, específico de cada local | NOAA Coral Reef Watch (consulta: octubre 2026) |
| Umbrales graficados por el propio producto | — | Líneas rojas discontinuas en **DHW = 4** y **DHW = 8** | NOAA Coral Reef Watch (consulta: octubre 2026) |
| **Resolución y cobertura del instrumento** | — | **5 km**, lectura **diaria**, serie desde el **1 de enero de 1985**; monitorea el **95 %** de los arrecifes del mundo | NOAA Coral Reef Watch v3.1 (consulta: octubre 2026) |
| Ventana de alerta publicada | — | *Bleaching Alert Area* a **1 día** y **máximo de 7 días** | NOAA Coral Reef Watch / NOAA OSPO (consulta: octubre 2026) |

**Justificación.** La escala completa de NOAA es: sin estrés (HotSpot ≤ 0) → *Bleaching Watch*
(0 < HotSpot < 1) → *Bleaching Warning* (HotSpot ≥ 1 y 0 < DHW < 4) → *Alert Level 1* (HotSpot ≥ 1 y
4 ≤ DHW < 8, «blanqueamiento probable») → *Alert Level 2* (HotSpot ≥ 1 y DHW ≥ 8, «mortalidad
probable») `[VERIFICADO]`.

La tentación evidente es poner el piso en **4**, porque es el primer número con nombre de alerta. Se
rechaza, y la razón es explícita: en 4 la fuente declara una **probabilidad de blanqueamiento**, que
es una respuesta de estrés de la que el sistema **se recupera** —el informe GCRMN/UNEP registra una
recuperación de **+2 %** de cobertura en 2019 y estima que los arrecifes podrían volver a niveles
previos a 1998 «potencialmente en una década» `[VERIFICADO]`—; en 8 la fuente declara un
**desenlace** («mortality likely»). El piso del SDV-E se ancla en el desenlace, no en la
probabilidad. Y el tramo 4-8 se conserva como **zona de aviso auditable**: obliga a instrumentar y a
publicar, no a sancionar.

Esto resuelve, para esta dimensión, la separación que el brief exige: **LEY = DHW < 8** (no cruzar
el umbral de mortalidad probable); **POLÍTICA = DHW < 4 y HotSpot ≤ 0** (que el arrecife no
blanquee nunca). Y hace algo que ninguna otra dimensión del SDV-E consigue hoy: **las dos columnas
tienen la misma fuente oficial.**

**Límite declarado.** La escala 4/8 está calibrada para arrecifes **tropicales**. Para arrecifes
subtropicales y templados los umbrales **no se transfieren automáticamente** y no se encontró
fuente que los fije: `[SIN FUENTE VERIFICADA — pendiente de consenso científico]`. Consecuencia de
diseño: la unidad ecológica del SDV-E puede necesitar **umbrales DHW por latitud**, y hoy solo
existen los tropicales.

**Protocolo.** Lectura diaria del producto de 5 km (SST CoralTemp, anomalía de SST, HotSpot, DHW,
área de alerta de blanqueamiento a 1 día y máximo de 7 días, tendencia de SST a 7 días) sobre el
píxel o la estación virtual que corresponda a la unidad. Agregación semanal. **El veredicto es por
temporada térmica**, y la temporada no se inventa: la fuente publica su calendario por región —el
pico de la temporada de blanqueamiento cae en, o inmediatamente después de, los meses más cálidos de
la climatología: Atlántico norte y Pacífico norte **julio-septiembre**; Atlántico y Pacífico sur
**enero-marzo**; Índico norte **abril-junio**; Índico sur **enero-abril** `[VERIFICADO]`. Quien
reporta: el producto satelital como autoridad externa, el guardián oráculo como responsable de la
unidad, y la comunidad testigo como confirmación in situ (candidatos verificados como portales:
GCRMN, ICRI, Reef Check, Reef Resilience — ninguno fija umbral en su página de inicio).

**Violación.** Un hecho, no una opinión: **DHW ≥ 8 con HotSpot ≥ 1 en la unidad durante su
temporada térmica.** Es binario, es auditable y no requiere interpretación. La gradación 4-8 activa
aviso; no activa INV2-E.

---

### Dimensión II: Saturación de aragonito y acidificación (la química del esqueleto)

**Qué protege.** La capacidad del agua de permitir que un organismo forme esqueleto o concha de
carbonato cálcico.

| Parámetro | Mínimo Absoluto (piso = LEY) | Óptimo (plenitud = POLÍTICA) | Fuente |
|---|---|---|---|
| **Estado de saturación de aragonito (Ω_arag) del océano superficial** — variable de control de la frontera planetaria | **≥ 80 % del valor preindustrial**, con Ω = 3,44 en 1850 como referencia. Bajo ese piso el agua es corrosiva para conchas y arrecifes | Retorno hacia el valor preindustrial (Ω ≈ 3,44). **La fuente no publica ninguna «plenitud»**: la frontera es un límite, no una meta | Steffen *et al.*, 2015 (*Science*), cifras reproducidas por el SDES/Ministerio de Transición Ecológica de Francia, 2021 |
| Ω_arag — equivalencia numérica del criterio | **Ω ≥ 2,75** `[HIPÓTESIS]` — derivación aritmética propia (80 % × 3,44); **la fuente no publica este número literalmente** | — | (misma fuente; la equivalencia es del proyecto) |
| **Aguas subsaturadas (Ω < 1: el agua puede volverse corrosiva para conchas calcáreas y la mayoría de los sistemas coralinos)** | **0 % de la unidad con Ω < 1** | 0 % | SDES (Francia), 2021 |
| Ω_arag en aguas tropicales de arrecife | — | **≥ 3** `[HIPÓTESIS]` de política: la fuente **proyecta «< 3» hacia 2100** bajo RCP 8.5 como *estado*, no como umbral; el SDV-E no convierte una proyección en ley sin declararlo | SDES (Francia), 2021 |
| pH superficial marino (criterio de calidad de agua para vida acuática) | 6,5 – 8,5 (unidades de pH) | — | US EPA, 1986 |
| Horizonte de saturación de aragonito | Que **no ascienda** hacia la superficie | — | Stockholm Resilience Centre, 2025 |
| Estado de la frontera planetaria | **Frontera TRANSGREDIDA desde 2025** — séptima frontera planetaria en salir del espacio operativo seguro | — | Stockholm Resilience Centre, *Planetary Health Check*, 2025 |

**Contexto de estado (no umbral).** Ω_arag estaba en el **84 % del valor preindustrial (Ω = 2,9) en
2015**, con proyección de **2,80 hacia 2050** `[VERIFICADO]`. El pH superficial pasó de **8,2 a 8,1**
desde el inicio de la revolución industrial (−0,1 unidades = **+30 % de acidez**, escala
logarítmica) y se proyecta **≈ 7,7 hacia 2100** (RCP 8.5). Hacia 2100, **60 % de las aguas
superficiales antárticas** serían corrosivas para el aragonito. El océano capta **~25 %** del CO₂
antropogénico `[VERIFICADO]` (SDES Francia, 2021, sobre IPCC; Stockholm Resilience Centre, 2025).

**Justificación y el hallazgo que ordena la dimensión.** El criterio legal de pH marino disponible
—**6,5 a 8,5** (US EPA, 1986) `[VERIFICADO]`— **no detecta la acidificación oceánica**: el pH del
océano cayó de 8,2 a 8,1, cómodamente dentro de esa banda. Es decir: **el único criterio numérico
legal de pH marino que existe es ciego al proceso que este documento quiere proteger.** De ahí que
la variable de control de la dimensión **no pueda ser el pH** y tenga que ser **Ω_arag**, la
variable que la frontera planetaria efectivamente usa. Este es un aporte operativo del documento, y
evita un error que habría sido fácil cometer: fijar el piso de acidificación en un rango de pH que
jamás se cruzaría.

**El problema estructural, dicho sin adornos.** La frontera **ya fue transgredida en 2025** a escala
global `[VERIFICADO]`. Para la **Escala C** (gran ecosistema marino, alta mar) esto significa que el
SDV-E **no puede declarar cumplimiento**: el piso global está cruzado y lo que procede es registrar
la transgresión y aplicar T14, no fingir un margen. Para las **Escalas A y B** (arrecife, estero,
bahía) el piso sigue siendo operable, **pero exige un Ω_arag de referencia por unidad, y ese valor
no existe en fuente abierta**: las cifras verificadas son globales, y la propia fuente señala
«fuerte variabilidad regional y estacional» sin dar valores. Es **el vacío más serio de esta
dimensión** y va a la §13.

**Protocolo.** `[SIN FUENTE VERIFICADA]` para el protocolo operativo de sensor: esta sesión no
verificó ningún documento que fije cómo se mide Ω_arag en una unidad concreta, con qué precisión ni
con qué frecuencia. Lo que sí existe y se declara como **candidato**, no como protocolo: el portal
de acidificación oceánica de NOAA, el servicio marino de Copernicus y la Comisión Oceanográfica
Intergubernamental (IOC-UNESCO) — los tres verificados con estado 200 como portales, **ninguno
abierto para cifras**. Frecuencia propuesta `[HIPÓTESIS]`: lectura mensual in situ y veredicto
anual.

**Violación.** Dos hechos observables: (a) **presencia de agua con Ω < 1 en la unidad** —hecho
químico, no requiere referencia histórica ni umbral consensuado—; (b) **Ω_arag de la unidad por
debajo del 80 % del valor preindustrial de referencia de esa unidad**, cuando ese valor de
referencia esté declarado. Mientras el valor de referencia por unidad no exista, la violación (b)
**no es demostrable** y así debe declararse: la dimensión tiene hoy un piso global transgredido y
ningún piso regional verificable.

---

### Dimensión III: Cobertura viva y comunidad del arrecife (el cuerpo del arrecife)

**Qué protege.** La existencia del arrecife como estructura viva y como hábitat complejo, no solo
como agua con temperatura aceptable.

| Parámetro | Mínimo Absoluto (piso = LEY) | Óptimo (plenitud = POLÍTICA) | Fuente |
|---|---|---|---|
| **Pérdida neta de cobertura de coral vivo en la unidad** | **0 %** de pérdida neta atribuible a actividad humana documentada (piso de **no regresión**) `[HIPÓTESIS]` del proyecto: **no hay umbral publicado** | Recuperación hacia el nivel previo a 1998 (GCRMN/UNEP registra **+2 %** de recuperación en 2019 y estima recuperación «potencialmente en una década») | `[SIN FUENTE VERIFICADA]` para el piso; GCRMN/UNEP, 2021, para la recuperación |
| **Dominancia de la comunidad bentónica** | El coral vivo **no es superado por el alga** — la inversión coral→alga es violación operativa | Cobertura de coral dominante y estable en el tiempo | GCRMN/UNEP, 2021 (el alga subió **+20 %** entre 2010 y 2019 y la transición reduce el hábitat complejo) |
| Declive proyectado de arrecifes a 1,5 °C | **0 %** de declive adicional | **70-90 %** de declive evitable respecto de 2 °C (*high confidence*) | IPCC, SR1.5, SPM B.4.2 (2018) |
| Contaminación por exceso de nutrientes (Meta 7a) | — | Reducción **≥ 50 %** de las pérdidas de nutrientes al ambiente para 2030 | CBD, Marco Kunming-Montreal, Meta 7 (2022) |
| **Estado (no umbral)** | — | — | Pérdida mundial de coral vivo **~14 %** entre 2009 y 2019; **9 %** de coral duro desde 1978; **8 %** del coral mundial muerto en el blanqueamiento masivo de 1998 (≈ 6 500 km²); **~50 %** de coral vivo perdido desde la década de 1870; **~33 %** de las especies de corales formadores de arrecife amenazadas; el arrecife ocupa el **0,2 %** del fondo oceánico y alberga **≥ ¼** de las especies marinas | GCRMN/UNEP, 2021; IPBES, 2019; UNEP/GCRMN, 2021 |
| Declive proyectado a 2 °C | — | — | **> 99 %** de pérdida (*very high confidence*) | IPCC, SR1.5, SPM B.4.2 (2018) |

**Justificación.** No existe fuente de organismo que fije la **cobertura mínima de coral vivo** para
considerar un arrecife íntegro: hay cifras de pérdida y ninguna de piso `[SIN FUENTE VERIFICADA]`.
Por eso esta dimensión **no inventa un porcentaje**. Se apoya en dos hechos observables que no
requieren umbral: (a) la **no regresión** frente a una línea base declarada de la propia unidad, y
(b) la **inversión de dominancia**, que es una comparación entre dos coberturas medidas por el mismo
transecto —no un número externo— y que la fuente describe como la señal de la pérdida de hábitat
complejo.

La segunda cifra del cuadro justifica el axioma: a 2 °C el declive proyectado es **> 99 %**. Un
estándar que esperara a tener «cobertura mínima consensuada» para actuar estaría esperando a que no
quede arrecife. T14 ordena lo contrario: ante incertidumbre y riesgo de irreversibilidad, la opción
de menor irreversibilidad. La ausencia de umbral **no autoriza la inacción**; autoriza a declarar
que el piso es estructural (no regresión + dominancia) en lugar de numérico.

**Protocolo.** Transectos y foto-cuadrantes in situ con línea base declarada por unidad; frecuencia
anual `[HIPÓTESIS]`. La teledetección **no basta** para esta dimensión: un cambio de cobertura viva
es demasiado fino para un píxel de 5 km, y por eso el protocolo exige medición en campo. Redes
candidatas verificadas como portales (no como fuentes de umbral): GCRMN, ICRI, Reef Check, Reef
Resilience. El reparto de la ganancia de manglar (82 % natural / 18 % restauración) da la pauta de
atribución: **separar lo que se recuperó solo de lo que se plantó**, y no sumarlos en la misma
casilla.

**Violación.** Dos hechos: (a) **pérdida neta de cobertura de coral vivo respecto de la línea base
declarada de la unidad, sin causa natural documentada** —la atribución es parte del hecho, y se
declara como problema abierto en la §13—; (b) **inversión de dominancia: la cobertura de alga supera
la de coral vivo en la unidad**, medida en los transectos de la misma unidad y **con línea base
declarada** (la fuente documenta el alga **+20 %** entre 2010 y 2019, no un estado de referencia
absoluto: sin línea base declarada el hecho no es exigible).

---

### Dimensión IV: Biomasa y explotación pesquera (el pez que falta)

**Qué protege.** La viabilidad de la fauna marina explotada. El canon la nombra como *"fauna acuática
viable"* (Cap. 10 §10.4).

| Parámetro | Mínimo Absoluto (piso = LEY) | Óptimo (plenitud = POLÍTICA) | Fuente |
|---|---|---|---|
| **Poblaciones marinas pescadas dentro de niveles biológicamente sostenibles** | **100 %** — piso lógico, sin fuente numérica de organismo: **se declara como piso lógico y no como dato** `[HIPÓTESIS]` (por su origen, **POLÍTICA votable**: §5.2) | — (la fuente no publica plenitud distinta del 100 %) | FAO, *SOFIA 2024* (2024) |
| Estado actual (no umbral) | — | — | **62,3 %** en 2021, **2,3 puntos menos que en 2019**; **37,7 %** de las poblaciones monitoreadas queda fuera de niveles sostenibles | FAO, *SOFIA 2024* (2024) |
| Poblaciones sostenibles ponderadas por desembarques | — | — | **76,9 %** (cuerpo del comunicado) frente a **78,9 %** (recuadro «SOFIA 2024 in numbers»): **las dos cifras son del mismo comunicado y difieren**. Este documento **cita la del cuerpo (76,9 %)** y declara la discrepancia en lugar de elegir la más cómoda | FAO, *SOFIA 2024* (2024) |
| Reparto de poblaciones por presión de pesca (2015, estado) | **0 %** cosechado de forma insostenible | 7 % subexplotadas · 60 % al máximo sostenible | IPBES, 2019 |
| Biomasa de peces proyectada a fin de siglo | — | 0 % de pérdida | **−3 % a −25 %** según escenario de calentamiento bajo o alto | IPBES, 2019 |
| Captura marina anual global proyectada | — | — | **−1,5 millones t** a 1,5 °C; **> −3 millones t** a 2 °C | IPCC, SR1.5, SPM B.4.4 (2018) |
| **Punto de referencia de biomasa (B/Bmsy), MSY, F_MSY y captura incidental admisible** | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` | `[SIN FUENTE VERIFICADA]` | NOAA Fisheries respondió 200 **sin cargar el texto de definición**: el criterio convencional (B < ½ B_MSY) **no se transcribe** |
| Área oceánica cubierta por pesca industrial (estado) | — | — | **> 55 %** del área oceánica | IPBES, 2019 |
| Pequeña escala (estado) | — | — | **> 90 %** de los pescadores comerciales del mundo y **~50 %** de la captura mundial | IPBES, 2019 |
| Producción pesquera de captura (2022, estado) | — | — | **81 millones t** marina + **11,3 Mt** continental = **92,3 Mt** | FAO, *SOFIA 2024* (2024) |

**Justificación.** La primera fila es incómoda y hay que decirla entera: **la fuente más autorizada
del mundo en pesquerías no publica un piso numérico; publica un porcentaje de estado.** 62,3 % no es
un umbral, es una fotografía, y un estándar que lo tomara como piso estaría declarando que el 37,7 %
restante es aceptable por debajo del piso. El SDV-E adopta el **100 %** como piso lógico y lo marca
como lo que es: una inferencia del proyecto, no un dato.

**La consecuencia operativa, que es el aporte de esta dimensión.** Para una unidad concreta
(Escalas A y B) el SDV-E **no puede hoy fijar un techo de extracción con fuente**. Lo que sí puede
hacer —y aquí T14 hace todo el trabajo— es invertir la carga de la prueba: *"La carga de la prueba
recae sobre quien propone acciones que afectan la temporalidad de no-participantes"* (Cap. 5, T14).
Traducido a hechos verificables:

- **Violación (a), de procedimiento:** explotar una población de la unidad **sin evaluación de stock
  publicada y vigente**. Es un hecho administrativo, auditable en un registro, y no requiere ningún
  umbral numérico.
- **Violación (b), de resultado:** captura por encima de la capacidad que la propia evaluación
  vigente de esa unidad declara como sostenible, **cuando esa evaluación existe**.

Nótese que esto **no contradice** `INV2-EDU` («la duda sin evidencia no castiga»). Esa regla existe
para no imputar déficit al **presunto vulnerado** cuando falta medición. Aquí el presunto vulnerado
es la población de peces, que no reporta; quien alega es el extractor. Aplicar la regla sin invertir
el sujeto protegería al violador —la misma inversión que el documento 09 detectó para el humedal
(insight I9)—. **Ausencia de dato no es violación del mar; es obligación de quien extrae.**

**Protocolo.** Indicador agregado anual de FAO (*SOFIA*) para la Escala C; evaluación de stock
nacional o regional vigente para las Escalas A y B; registros de desembarque de la unidad como
control cruzado. **Toda cifra de pesquería debe declarar su definición**, porque el propio informe de
fuentes documenta que la diferencia entre 400 y 700 zonas muertas costeras es de definición (solo
fertilizantes frente a todas las causas) y no una contradicción: lo mismo aplica a cualquier
estadística de captura.

**Violación.** (a) Extracción en la unidad **sin evaluación de stock publicada y vigente**;
(b) captura por encima de la capacidad declarada en la evaluación vigente, cuando exista;
(c) a escala global (Escala C), **cualquier valor por debajo del 100 %** de poblaciones dentro de
niveles sostenibles constituye déficit registrado —hoy, 37,7 puntos de déficit, el más grande de
este documento—, con la advertencia de que a esa escala **no hay sujeto obligado** y por tanto se
registra estado, no violación imputable.

---

### Dimensión V: Áreas marinas y costeras protegidas y gobernadas (el mapa que protege)

**Qué protege.** La existencia de un régimen efectivo de conservación sobre el hábitat crítico, y la
representatividad y conectividad de la red que lo contiene.

| Parámetro | Mínimo Absoluto (piso) | Óptimo (plenitud = POLÍTICA) | Fuente |
|---|---|---|---|
| **Cobertura de áreas marinas y costeras conservadas (Meta 3, «30×30»)** | — **el 30 % no es un piso biológico**: es una meta de superficie. Adoptarlo como umbral de integridad sería un salto lógico | **≥ 30 % para 2030**, y además *"ecológicamente representativas, **bien conectadas** y gobernadas equitativamente"*, integradas en el océano | CBD, Marco Kunming-Montreal, Meta 3 (2022) |
| Estado actual en aguas nacionales | — | 30 % | **23,09 %** de las aguas nacionales (el **39 %** del océano) — (estado, no umbral) | UNEP-WCMC / IUCN, Protected Planet (2026) |
| Estado actual en Áreas Fuera de Jurisdicción Nacional (ABNJ, alta mar) | — | 30 % | **1,45 %** de las ABNJ (el **61 %** del océano): el hueco mayor frente a la meta | UNEP-WCMC / IUCN, Protected Planet (2026) |
| Nº de AMP registradas | — | — | **17 389** (estado) | UNEP-WCMC / IUCN, Protected Planet (2026) |
| Restauración de ecosistemas degradados (Meta 2) | — | **≥ 30 %** de los ecosistemas degradados —terrestres, de aguas continentales, **marinos y costeros**— para 2030 | CBD, Meta 2 (2022) |
| Gestión sostenible de la pesca y la acuicultura (Meta 10) | `[SIN FUENTE VERIFICADA]` — **la Meta 10 no fija ningún umbral numérico**: es enteramente cualitativa («gestionadas de forma sostenible») | — | CBD, Meta 10 (2022) |
| Conectividad («bien conectadas») | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]`: la Meta 3 la **nombra** y **no la cuantifica**; ningún documento abierto en esta sesión fija un valor | — | CBD, Meta 3 (2022) |
| Instrumento para la alta mar | — | Entrada en vigor del acuerdo **BBNJ** en **enero de 2026** | UNEP-WCMC / IUCN, Protected Planet (2026) |

**Justificación.** Este es el hallazgo estructural del bloque: **el único número vinculante del
30×30 es una meta de cobertura, no un umbral de integridad.** Ni la Meta 2 ni la Meta 3 fijan
umbrales de salud del ecosistema: fijan **superficie**. Un 30 % protegido que no contenga arrecife,
manglar ni pradera cumple la meta y no protege nada.

Por eso esta dimensión **no se presenta como piso de integridad** sino como **mínimo de
gobernanza**, y esto exige una precisión doctrinal que este documento declara explícitamente: su
piso no es una ley de la naturaleza, es **una obligación jurídica humana** (un tratado). El SDV-E la
adopta como piso operativo de la dimensión **declarando su naturaleza**, para no cometer el error
inverso al del SDV-H: allí se confundió un óptimo humano con un mínimo biológico; aquí no se
confundirá un acuerdo humano con una ley ecológica. Son categorías distintas y se marcan distinto.

**Lo que sí es piso de integridad en esta dimensión**, y no requiere cifra: la **efectividad**. Una
AMP declarada sin régimen de gestión verificado no protege. El hecho observable está descrito y es
auditable: **parque de papel**.

**Protocolo.** Registro de Protected Planet / WDPA (mundial, actualización periódica) y reporte
nacional al CBD; control de representatividad por ecorregión (exige la tipología de ecosistemas,
documento transversal); frecuencia anual `[HIPÓTESIS]`. Para las ABNJ, el instrumento de referencia
es el BBNJ desde enero de 2026. **La verificación de «gobernadas equitativamente» no tiene
protocolo verificado en esta sesión** y se declara como tarea del documento 05 (representación y
mandato).

**Violación.** (a) **Extracción destructiva documentada en la unidad sin AMP ni OECM efectivo**;
(b) **AMP declarada sin régimen de gestión verificado** (parque de papel): la declaración existe en
el registro y la actividad prohibida se practica dentro; (c) red de la unidad política por debajo de
la meta que ella misma declaró. Las tres son hechos, ninguna es una opinión.

---

### Dimensión VI: Manglar y praderas marinas (el bosque que sostiene la orilla)

**Qué protege.** La estructura viva que amortigua la costa, alberga las crías de la pesquería y
almacena carbono azul.

| Parámetro | Mínimo Absoluto (piso = LEY) | Óptimo (plenitud = POLÍTICA) | Fuente |
|---|---|---|---|
| **Pérdida neta de manglar en la unidad** | **0 ha de pérdida neta** (piso de no regresión). La FAO reporta **desaceleración** de la tasa, **no** un objetivo | Tasa de pérdida → 0, con **ganancia por expansión natural** como forma principal | FAO, *The World's Mangroves, 2000-2020* (2023) |
| Forma de la ganancia | — | **82 % expansión natural · 18 % restauración**: la restauración eficaz **crea condiciones para que el manglar colonice**, no planta | FAO, 2023 |
| **Declive de la extensión de praderas marinas (1970-2000)** | **0 %** de pérdida (no regresión) | — | IPBES, 2019 — valor **> 10 % por década** (estado, no umbral) |
| Declive anual de praderas marinas | `[SIN FUENTE VERIFICADA]` en fuente de organismo | — | **7 %/año desde 1990** `[REPORTADO]` — Waycott *et al.* (2009): visto citado en fuentes indexadas y en un PDF de agencia estatal, **sin abrir el artículo original** |
| Extensión mundial de praderas marinas | `[SIN FUENTE VERIFICADA]` | — | no encontrada en fuente de organismo accesible en esta sesión |
| Umbral mínimo de extensión de manglar o pradera por unidad ecológica | `[SIN FUENTE VERIFICADA — pendiente de consenso científico]` | `[SIN FUENTE VERIFICADA]` | la FAO da extensión y pérdida, **ningún mínimo** |
| **Estado (no umbral)** | — | — | Extensión mundial de manglar **14,8 millones ha** (2020); **677 000 ha** perdidas entre 2000 y 2020; **> 20 %** perdido en los últimos 40 años; **−23 %** de reducción de la tasa de pérdida en la segunda década; **393 000 ha** ganadas (compensan más de la mitad de la pérdida mundial); **6,23 Gt C** almacenadas; **123 países** con manglar | FAO, 2023 |
| Factores de pérdida (estado) | — | 0 % | Acuicultura de camarón en estanque: **31 %** de la pérdida (2000-2010) → **21 %** (2010-2020); retracción natural **26 %**; desastres naturales **2 %**, pero **el área destruida se triplicó** | FAO, 2023 |

**Justificación.** La recomendación operativa de la FAO es la que fija el Óptimo de esta dimensión y
es, palabra por palabra, el principio del canon llevado al manglar: las iniciativas de restauración
deben **crear condiciones para que el manglar colonice naturalmente hábitats adecuados**
`[VERIFICADO]`. Es decir: **la restauración eficaz no es plantar, es restaurar el proceso** — y el
dato lo respalda, porque de las 393 000 ha ganadas, 82 % fueron expansión natural. Esto es
exactamente *"se registra lo que regenera, no lo que adorna"* (Cap. 16.5 §16.5.14), verificado por
una agencia externa.

De ahí la consecuencia dura para la contabilidad: **una hectárea plantada no compensa una hectárea
perdida**, y el registro debe mantenerlas en ejes distintos. La hectárea perdida es déficit del
piso; la hectárea colonizada es regeneración en el eje R. Nunca se restan (§9).

**Protocolo.** Extensión de manglar: inventario FAO (escala mundial, decadal) y para la unidad,
teledetección con verificación de campo. Praderas marinas: `[SIN FUENTE VERIFICADA]` para la
normalización mundial —no hay extensión global verificada en esta sesión—, de modo que el protocolo
**solo puede ser local** y la comparación entre unidades queda comprometida y así se declara.
Frecuencia propuesta `[HIPÓTESIS]`: 3-5 años, en el ciclo de revisión del documento 40.

**Violación.** **Pérdida neta de superficie de manglar o de pradera marina en la unidad respecto de
la línea base declarada, atribuible a causa humana documentada** (el primer factor documentado por
la FAO es la acuicultura de camarón en estanque, con el 31 % → 21 % de la pérdida). **No es
compensable por plantación**: la plantación se registra aparte y no altera el veredicto del piso.

---

### Dimensión VII: Oxígeno disuelto, hipoxia y zonas muertas (el aliento del agua)

**Qué protege.** La posibilidad de que exista fauna que respire en la columna de agua.

| Parámetro | Mínimo Absoluto (piso = LEY) | Óptimo (plenitud = POLÍTICA) | Fuente |
|---|---|---|---|
| **Zonas muertas costeras por fertilizantes** | **0** (implícito: la existencia de una zona muerta es el hecho) | 0 | **400** zonas muertas y **> 245 000 km²** (estado) — área mayor que el Reino Unido — IPBES, 2019 |
| Sitios con condiciones de bajo oxígeno (estado) | 0 | 0 | **~700 en 2011**, frente a **solo 45 antes de la década de 1960** — IUCN, 2019 |
| Pérdida de oxígeno disuelto en el océano (estado) | 0 | 0 | **~2 %** desde mediados del siglo XX; proyección **3-4 %** a 2100 (RCP 8.5) — IUCN, 2019 |
| Volumen de aguas anóxicas (oxígeno completamente agotado) | 0 | 0 | **cuadruplicado** desde la década de 1960 — IUCN, 2019 |
| Causa térmica de la pérdida de oxígeno (0-1000 m) | — | — | **~50 %** atribuible al aumento de temperatura — IUCN, 2019 |
| Profundidad donde se concentra la mayor pérdida | — | — | **100-300 m** (Pacífico tropical y norte, Ártico/Antártico, Atlántico sur) — IUCN, 2019 |
| **Umbral numérico de hipoxia (2 mg/L ≈ 60 µmol/kg)** | `[REPORTADO]` **y sin verificar en este documento**: la cifra es estándar en la literatura (Díaz, 2001; Díaz y Rosenberg, 2008) y aparece en documentos institucionales indexados, pero **no se leyó en página oficial de organismo** en esta sesión. **No es una ausencia de umbral: es un umbral existente y no verificado** (Regla 5, caso (c)). La IUCN mide el fenómeno en **% de pérdida de oxígeno**, no con un umbral absoluto | — | **2 mg/L ≈ 60 µmol/kg** `[REPORTADO]` — Díaz, 2001 / Díaz y Rosenberg, 2008 |

**Contexto de proceso (no umbral).** Dos causas documentadas `[VERIFICADO]`: (a) *desoxigenación por
calentamiento* —el agua caliente retiene menos oxígeno, es más boyante y se mezcla menos con las
aguas profundas, y eleva la demanda de oxígeno de los organismos—; (b) *crecimiento excesivo de
algas* por escorrentía de fertilizantes, aguas residuales, residuos animales, acuicultura y depósito
de nitrógeno de la quema de combustibles, es decir **eutrofización**, que afecta sobre todo a las
zonas costeras (IUCN, 2019). El cambio de balance favorece a especies tolerantes a la hipoxia
(microbios, medusas, algunos calamares) **a expensas de las sensibles, la mayoría de los peces**; y
los afloramientos costeros del borde oriental de las cuencas —naturalmente pobres en oxígeno—
sostienen **una quinta parte de la cosecha mundial de peces marinos silvestres** y son especialmente
vulnerables a la desoxigenación.

**Justificación.** La fuente más autorizada disponible mide este fenómeno **en porcentaje de pérdida,
no con un umbral absoluto**, y la cifra estándar de hipoxia (2 mg/L) no se pudo leer en fuente de
organismo. Es el mismo muro contra el que chocó el informe de fuentes del documento 09 para el agua
dulce: **la dimensión se queda sin umbral citable.** Pero no se queda sin violación, y esto es lo
importante: lo que se puede declarar como hecho observable no es un valor de oxígeno, es **la
existencia de una zona muerta**. Una zona muerta documentada —con mortalidad masiva o con
condiciones de hipoxia medidas por la autoridad competente— es un hecho, y no necesita umbral.

**Protocolo.** Sensores in situ de oxígeno disuelto y monitoreo nacional costero; las redes
internacionales de referencia (IUCN, IOC-UNESCO, UNEP) publican el fenómeno a escala de sitio.
Frecuencia propuesta `[HIPÓTESIS]`: continua o estacional para la lectura, anual para el veredicto.
**Advertencia de definición:** la diferencia entre las **400** zonas muertas de IPBES (solo
fertilizantes) y los **~700** sitios de IUCN (todas las causas) **es de definición, no una
contradicción**: este documento las cita por separado y no las funde.

**Violación.** (a) **Aparición o expansión documentada de una zona hipóxica o anóxica en la
unidad**; (b) **pérdida de oxígeno disuelto respecto de la línea base declarada de la unidad**,
cuando la causa dominante es la actividad humana de la propia unidad (eutrofización) o acumulada
(calentamiento). El acoplamiento con la Dimensión II se declara: la respiración consume oxígeno y
libera CO₂, de modo que desoxigenación y acidificación **van juntas y deben mitigarse juntas**
(IUCN, 2019).

---

### Dimensión VIII: Costa, nivel del mar y zona intermareal (la orilla que se mueve)

**Qué protege.** La franja de transición —intermareal, estero, marisma, delta— como ecosistema
propio, y la seguridad de las personas que viven en ella.

| Parámetro | Mínimo Absoluto (piso) | Óptimo (plenitud = POLÍTICA) | Fuente |
|---|---|---|---|
| **Nivel medio del mar a 2100 con 1,5 °C** | **No existe piso posible sobre el parámetro**: la subida no se detiene. El piso se desplaza a la **acción humana** (pilar 8 de la §3) | **0,26 – 0,77 m** (rango indicativo relativo a 1986-2005); **0,1 m menos** que con 2 °C | IPCC, SR1.5, SPM B.2.1 (2018) |
| Exposición humana evitada | — | Hasta **10 millones de personas menos expuestas** | IPCC, SR1.5, SPM B.2.1 (2018) |
| Riesgo de pérdida irreversible de ecosistemas marinos y costeros | **0** pérdida irreversible | El riesgo **aumenta con el calentamiento, especialmente a 2 °C o más** | IPCC, SR1.5, SPM B.4.2 (2018) |
| Personas en zonas costeras con riesgo incrementado por pérdida de hábitat costero protector | 0 | 0 | **100-300 millones** (estado) — IPBES, 2019 |
| Ambiente marino significativamente alterado por la acción humana | 0 | 0 | **66 %** (estado) — IPBES, 2019 |
| Contaminación plástica | 0 | 0 | **×10** desde 1980 (estado) — IPBES, 2019 |
| **Zona intermareal y esteros — umbrales propios** (rango de marea, salinidad, hidroperiodo, ratio de mezcla dulce-marino, extensión mínima de marisma) | **`[SIN FUENTE VERIFICADA — pendiente de consenso científico]`** | **`[SIN FUENTE VERIFICADA]`** | **No se encontró ninguna fuente de organismo que fije un umbral numérico** para la zona intermareal ni para esteros en esta sesión. El marco Ramsar (criterios 2 a 4) **sí existe y es cualitativo**; `ramsar.org` devuelve **403 en las cuatro rutas probadas** |
| Eutrofización costera (criterios de nutrientes) | `[SIN FUENTE VERIFICADA]` como escalar único: la EPA publica criterios **por tipo de masa de agua** | — | US EPA |
| Criterios de calidad de agua para vida acuática | **pH marino 6,5 – 8,5** | — | US EPA, 1986 |

**Justificación, en dos bloques separados, porque la dimensión tiene dos mitades de calidad muy
distinta.**

*La mitad con fuente.* El IPCC da los números, y su lectura correcta para el SDV-E es que aquí **el
piso no puede estar en el parámetro**. El nivel del mar **seguirá subiendo mucho más allá de 2100**
incluso limitando el calentamiento a 1,5 °C (*high confidence*), y la inestabilidad de la capa de
hielo marino antártica y/o la pérdida irreversible del hielo de Groenlandia podrían producir
**aumentos de varios metros en cientos a miles de años**, posiblemente disparados en torno a
**1,5-2 °C** (*medium confidence*) `[VERIFICADO]`. Ningún ecosistema costero puede «cumplir» frente
a eso. Lo que sí puede hacer un estándar es lo que hace esta dimensión: **poner el piso en la
acción humana** —no ocupar de nuevo la franja en riesgo, no rellenar, no encauzar, no eliminar la
defensa natural— y registrar la pérdida irreversible como violación consumada. Es la estructura de
INV2 aplicada a una dimensión: el invariante juzga la acción, no al sujeto.

*La mitad sin fuente.* **La zona intermareal y los esteros no tienen hoy ningún umbral con fuente.**
Se buscó rango de marea mínimo, salinidad, hidroperiodo, ratio de mezcla dulce-marino y extensión
mínima de marisma, y no se encontró fuente de organismo que fije ninguno; el dominio de Ramsar, que
es la referencia natural para los humedales costeros, **bloquea a los agentes automáticos en las
cuatro rutas probadas (403)**. Este documento **escribe la dimensión igual y declara el vacío**: es
la misma estructura que el informe de fuentes del documento 09 documentó para el caudal ecológico
—**canon sí, fuente no**— y la misma que este documento encuentra para la conectividad marina. El
brief ya advertía que el ISE no incluye conectividad; aquí se añade que **tampoco existe un análogo
costero del ISE**.

**Protocolo.** Nivel del mar: series mareográficas y altimetría satelital (el servicio marino de
Copernicus está verificado como portal); exposición: cartografía de elevación y población (el
*Coastal Water Temperature Guide* de NOAA NCEI y *coast.noaa.gov* están verificados como portales de
datos costeros). Intermareal y estero: `[SIN FUENTE VERIFICADA]` — el protocolo tendría que
construirse desde cero con la comunidad de custodia, y esa es una tarea declarada, no un supuesto.

**Violación.** (a) **Pérdida irreversible documentada de superficie intermareal, de marisma o de
estero por causa humana** (relleno, encauzamiento, barrera, extracción) que reduzca la superficie de
transición por debajo de la línea base declarada; (b) **nueva ocupación humana permanente de la
franja costera declarada en riesgo** por la propia unidad —hecho administrativo verificable, sin
necesidad de umbral—; (c) eliminación de la defensa costera natural (manglar, marisma, duna,
arrecife) sin sustitución verificada, con la consiguiente pérdida de protección para las personas
que dependen de ella (IPBES: 100-300 millones de personas en riesgo).

---

### Dimensión IX: Zona Libre del océano — lo que NO se mide (dimensión binaria, sin peso)

**Qué protege.** El derecho del ecosistema marino a tener un dominio que **no se mide, no se
puntúa y no se canjea**.

> *"Parte del valor del humedal es inefable (Cap. 7 §7.9). Los sensores miden salud (agua, cobertura,
> biodiversidad indicadora); jamás «milagros». **Medir todo sería la forma técnica de dejar de
> escucharlo.**"* — (Cap. 16.5 §16.5.14)

**Precedente canónico, y por qué se aplica aquí.** Las dimensiones VIII (Rehabilitación) y IX
(Opacidad Vital) del SDV-H *"se registran cualitativamente y mediante umbrales binarios
(presencia/ausencia del derecho), no mediante pesos en la fórmula — medir la rehabilitación o la
opacidad con la misma vara cuantitativa que el agua o la vivienda las destruiría."* (Cap. 8 §8.11).
La Zona Libre del mar se estructura igual: **se registra, no se pondera**.

| Cláusula de la Zona Libre | Qué NO se mide | Cómo se audita (binario) | Violación (hecho observable) |
|---|---|---|---|
| **ZL-1 · El valor inefable del mar** | El valor no instrumental del océano, del arrecife o del estero: lo que no se puede expresar como servicio, existencia o beneficio | Presencia o ausencia de la cláusula de Zona Libre en la identidad de la unidad (los 7 campos del documento 05) | Un contrato, índice o pago que **exija medir, certificar o poner precio** a un aspecto declarado en la Zona Libre |
| **ZL-2 · La vida interna del ecosistema** | La vida interna: *"Nosotros registramos la interacción, no la vida interna del ecosistema"* (Cap. 16.5 §16.5.14) | Presencia o ausencia de registro declarado como «no medido por diseño» | Convertir una lectura ambiental en **propiedad humana** o en autoridad absoluta sobre la unidad |
| **ZL-3 · El vínculo no medido con la comunidad de custodia** | La relación entre las personas y el mar que no se expresa en indicadores (duelo, memoria, oficio, pertenencia) | Presencia o ausencia de la comunidad de custodia declarada y de su procedimiento de disputa | Sustituir la comunidad de custodia por un indicador de participación, o exigirle un puntaje de «satisfacción» para acceder a un derecho |

**Justificación.** El canon prohíbe expresamente medir esta clase de valor: *"Parte del valor del
humedal es inefable (Cap. 7 §7.9). Los sensores miden salud (agua, cobertura, biodiversidad
indicadora); jamás «milagros». Medir todo sería la forma técnica de dejar de escucharlo."*
(Cap. 16.5 §16.5.14). Y el propio estándar humano ya resolvió el problema de forma: las dimensiones
VIII (Rehabilitación) y IX (Opacidad Vital) del SDV-H *"se registran cualitativamente y mediante
umbrales binarios (presencia/ausencia del derecho), no mediante pesos en la fórmula"* (Cap. 8 §8.11).
La justificación de fondo es contable, no poética: **un valor ponderado es un valor canjeable**, y lo
que entra en la fórmula puede compensarse contra otra cosa. La Zona Libre existe para que exista al
menos un dominio del arrecife que no pueda comprarse, venderse ni promediarse.

**Protocolo.** No hay sensor, y esa ausencia es el protocolo. Lo que se audita es **binario y
documental**: (1) que la cláusula de Zona Libre esté declarada en la identidad de la unidad —los
7 campos del documento 05—; (2) que exista un registro explícito de lo que se declara «no medido por
diseño», separado del registro de lo que está sin instrumentar; (3) que el guardián tenga declarada la
facultad de **no responder** una consulta sobre un aspecto de la Zona Libre. Frecuencia: en cada
revisión de identidad de la unidad, no en cada ciclo de medición. Quien reporta: el guardián oráculo,
y la comunidad de custodia como testigo de que la frontera no se movió.

**Violación.** Un hecho documental, no una opinión: **existe una cláusula —en un contrato, en un
índice, en un pago o en un formulario de acceso— que exige medir, certificar, puntuar o poner precio
a un aspecto declarado en la Zona Libre**, o que convierte una lectura ambiental en propiedad humana
o en autoridad absoluta sobre la unidad. Su consecuencia no es un recargo en `FE`: es la **nulidad de
la cláusula** y el registro del hecho. La Zona Libre no se viola «un poco»: se invade o no se invade.

**Lo que la Zona Libre del océano NO es, y esta distinción es un aporte de este documento.** **Lo no
medido por falta de instrumento no es Zona Libre: es opacidad ecológica, y genera una obligación.**
La distinción es decisiva aquí, porque el mar es el ecosistema más instrumentado y menos visto del
planeta al mismo tiempo: NOAA Coral Reef Watch cubre el **95 %** de los arrecifes del mundo
`[VERIFICADO]`. Ese 5 % restante **no puede declararse Zona Libre**: es deuda de instrumentación.
Sin esta distinción, la Zona Libre se convierte en el refugio que el documento 09 dejó como pregunta
abierta, y la degradación no medida se declararía inefable. **Regla:** si un aspecto es medible con
la tecnología disponible y no se mide, es opacidad; si es inefable por naturaleza, es Zona Libre.

**Peso: 0,00. Fuera de la fórmula, por diseño.** Ponderar la Zona Libre la volvería canjeable: un
arrecife con «mucha Zona Libre» podría compensar un DHW de 12. La Zona Libre **no entra en
`v`**, no entra en `FE` y no tiene banda de interpretación. Solo tiene un veredicto binario:
presente o ausente.

---

## 5. Fórmula de violación, pesos y umbrales

### 5.1 La fórmula normalizada, con una corrección que el mar obliga a introducir

El brief fija el déficit **normalizado**: `déficit = (requerido − actual) / requerido`. Esta forma
funciona para parámetros de tipo **piso** («el valor debe ser mayor o igual que…»): calidad del agua,
cobertura viva, oxígeno.

Pero **la mitad de los parámetros de este documento son de tipo techo** («el valor debe ser menor o
igual que…»): DHW, exposición al nivel del mar, dominancia de alga, porcentaje de poblaciones fuera
de niveles sostenibles. Aplicarles la fórmula del piso tal cual daría **déficit negativo** para todo
valor por encima del techo —y un déficit negativo es un absurdo contable: un arrecife con DHW = 20
no está «mejor que el piso»—. La corrección es explícita y es un aporte de este documento:

```
Tipo PISO   (el parámetro debe ser ≥ p):   déficit_i = max(0, (p − actual_i) / p)
Tipo TECHO  (el parámetro debe ser ≤ t):   déficit_i = max(0, (actual_i − t) / t)

Magnitud de violación:   v = Σ (déficit_i × peso_i)
Factor de violación:     FE = e^v
```

- **Base neutra innegociable:** `FE(v = 0) = e^0 = 1,0` **exacto**. El SDV-S tuvo que corregir
  `1 + e^v` → `e^v` precisamente porque la primera versión recargaba el 100 % incluso sin violación.
  El mar no repite ese error.
- **El déficit se satura en 0, no admite negativos.** Un ecosistema no «des-desafecta» su arrecife en
  la misma cuenta: pasarse de la raya hacia el lado bueno no genera crédito en el piso. El crédito
  vive en **R** (`r_units` negativo), nunca en `V`.
- **`v` no compensa nada.** Un índice agregado no puede anular un piso: si la Dimensión I está
  violada, hay violación **aunque `v` sea pequeña**. La fórmula ordena la severidad y multiplica el
  factor; **no decide la existencia de la violación**. Es la misma conclusión a la que llegó el
  documento 09 (insight I7): el índice es tablero, no estándar.

### 5.2 Tabla de pesos

| Dimensión | Tipo | Peso `[HIPÓTESIS]` |
|---|---|---|
| I · Estrés térmico del arrecife (DHW) | TECHO | 0,15 |
| II · Saturación de aragonito | PISO | 0,15 |
| III · Cobertura viva y comunidad del arrecife | PISO | 0,15 |
| IV · Biomasa y explotación pesquera | PISO | 0,15 |
| V · AMP y gobernanza | **Mínimo de gobernanza** (tratado) | 0,10 |
| VI · Manglar y praderas marinas | PISO | 0,10 |
| VII · Oxígeno disuelto e hipoxia | PISO (ausencia) | 0,10 |
| VIII · Costa, nivel del mar e intermareal | PISO sobre la acción humana | 0,10 |
| **IX · Zona Libre del océano** | **BINARIA** | **0,00 — fuera de la fórmula** |
| **Total** | | **1,00** |

**Los pesos no tienen fuente externa.** Ningún organismo publica ponderaciones porcentuales para
dimensiones de integridad marina: `[SIN FUENTE VERIFICADA — pendiente de consenso científico]`. Son
una **decisión del proyecto**, y por tanto **POLÍTICA votable** (categoría `critical`: quórum 60 %,
consenso 75 %, T13, anti-flip-flop 14 días). Los **umbrales de cada fila no se votan**: el 8 del DHW
lo publica NOAA, no el Parlamento. Ahora bien, **no todo piso es LEY por estar en la columna del
piso**: donde el piso es `[HIPÓTESIS]` del proyecto —el 100 % de poblaciones sostenibles (Dimensión
IV) y el 0 % de pérdida de cobertura viva (Dimensión III)— no hay ley de la naturaleza que invocar,
y esos pisos son **propuesta POLÍTICA mientras no se ratifiquen** (la §13 lo declara para la
cobertura de coral vivo). Lo que sí es LEY, y no se vota, es el piso que una fuente de organismo
publica con significado biológico declarado: **DHW < 8** (NOAA), **Ω < 1** y el **80 % del valor
preindustrial** (SDES sobre Steffen *et al.*), **0 ha de pérdida neta de manglar** como regla de no
regresión. La frontera LEY/POLÍTICA se decide por el **origen** del umbral, no por la columna en que
está escrito.

### 5.3 Bandas de interpretación

No existen bandas publicadas para un déficit normalizado 0-1: `[SIN FUENTE VERIFICADA]`. Las bandas
del ISE (≥ 85 Mejorando · 70-84 Estable · 50-69 Declinando · < 50 Crítico) son de un índice 0-100 del
proyecto y **no se reutilizan aquí** sin declararlo. Este documento propone `[HIPÓTESIS]` reutilizar
la clasificación de severidad que el propio motor ya aplica al déficit relativo
(`maxocontracts/blocks/sdv_validator.py`: **≤ 10 % leve · ≤ 30 % moderada · > 30 % severa**)
`[VERIFICADO]` por lectura del documento 09, porque es la única escala interna coherente con la
fórmula normalizada y no requiere inventar una nueva.

### 5.4 Ejemplo aplicado, con violación y con factor

Unidad: arrecife costero hipotético con tres parámetros medidos y cinco sin medición.

| Dimensión | Piso/techo | Valor medido | Déficit | Peso | Aporte a `v` |
|---|---|---|---|---|---|
| I · DHW | techo 8 grado-semanas | **9,5** | (9,5 − 8) / 8 = **0,1875** (moderada) | 0,15 | 0,028125 |
| II · Ω_arag | piso 2,75 | 2,90 | 0 (por encima del piso) | 0,15 | 0 |
| IV · Poblaciones sostenibles (unidad de gestión) | piso 100 % | **62,3 %** | (100 − 62,3) / 100 = **0,377** (severa) | 0,15 | 0,056550 |
| III, V, VI, VII, VIII | — | **sin medición** | **no se imputa déficit** (`INV2-EDU`) + **bandera de opacidad ecológica** | — | 0 |
| **IX · Zona Libre** | binaria | presente | — | **0,00** | 0 |

`v = 0,028125 + 0,056550 = 0,084675` → **`FE = e^0,0847 ≈ 1,088`**

**Cómo se lee este número, y cómo NO se lee.**

- `FE ≈ 1,088` significa un recargo del **8,8 %**: la contabilidad de quien opere en esa unidad queda
  recargada, no intacta.
- **Pero la violación no la decide `FE`: la decide el piso.** Aquí la Dimensión I está violada
  (DHW 9,5 ≥ 8 con HotSpot ≥ 1) **aunque `v` sea pequeña**. Un `FE` de 1,088 no es «casi
  cumplimiento»: es un sistema con el arrecife cruzando el umbral de mortalidad probable mientras el
  agregado mira para otro lado. Esa es exactamente la diferencia entre «el suelo» y «el saldo» que la
  §9 desarrolla.
- Los cinco parámetros sin medición **no bajan el índice a cero** —la duda sin evidencia no castiga—
  **pero tampoco suspenden la ley**: activan la bandera de opacidad ecológica, que en el SDV-E es
  **obligación contractual de instrumentar**, no sanción al territorio (documento 09, insight I9).
- La Zona Libre no aparece en el cálculo. No es un olvido: es el diseño.

---

## 6. Protocolo de medición (sensores, frecuencias, quién reporta)

**Antes de la tabla, la advertencia de la Regla 6.** Un parámetro marino no es un número: es un
número **con profundidad, con estación y con superficie de muestreo**. Este documento exige que todo
reporte declare las tres, porque dos lecturas de la misma unidad pueden diferir solo por el diseño.

| Dimensión | Instrumento o producto | Frecuencia propuesta `[HIPÓTESIS]` | Quién reporta |
|---|---|---|---|
| **I · Estrés térmico** | NOAA Coral Reef Watch: CoralTemp SST, anomalía de SST, **HotSpot**, **DHW**, área de alerta de blanqueamiento (**1 día** y **máximo 7 días**), tendencia de SST a 7 días; **5 km**, diario, serie desde **1-ene-1985**; **212 estaciones virtuales** desde oct-2016; **95 %** de los arrecifes del mundo `[VERIFICADO]` | Lectura **diaria**, agregación **semanal**, veredicto **por temporada térmica** (calendario regional publicado por la propia fuente) | NOAA / NESDIS como autoridad externa; guardián oráculo de la unidad; comunidad testigo para confirmación in situ |
| **II · Saturación de aragonito** | `[SIN FUENTE VERIFICADA]` — no se verificó ningún protocolo operativo. Candidatos declarados como **portales**, no como protocolos: NOAA ocean acidification, Copernicus Marine, IOC-UNESCO | Mensual in situ / veredicto anual `[HIPÓTESIS]` | Laboratorio o autoridad nacional; guardián para el registro |
| **III · Cobertura viva** | Transectos y foto-cuadrantes in situ; redes candidatas verificadas como portales: **GCRMN**, **ICRI**, **Reef Check**, **Reef Resilience** | Anual `[HIPÓTESIS]` — **la teledetección no basta** | Comunidad testigo + ciencia ciudadana; guardián como responsable del registro |
| **IV · Pesquerías** | FAO *SOFIA* (agregado mundial, anual) y evaluación de stock nacional o regional vigente para la unidad | Anual (agregado) / vigencia de la evaluación (unidad) `[HIPÓTESIS]` | Autoridad pesquera; registro de desembarques de la unidad como control cruzado |
| **V · AMP y gobernanza** | Protected Planet / **WDPA** (registro mundial); reporte nacional al CBD; **BBNJ** desde enero de 2026 para ABNJ | Anual `[HIPÓTESIS]` | UNEP-WCMC / IUCN y los puntos focales nacionales del CBD |
| **VI · Manglar y praderas** | Inventario FAO de manglares (mundial, decadal); teledetección + verificación de campo para la unidad. Praderas marinas: **sin extensión mundial verificada** → solo protocolo local | 3-5 años `[HIPÓTESIS]` (ciclo de revisión del documento 40) | FAO (mundial); guardián + comunidad de custodia (unidad) |
| **VII · Oxígeno e hipoxia** | Sensores in situ de oxígeno disuelto; monitoreo costero nacional; redes IUCN / IOC-UNESCO / UNEP | Continuo o estacional (lectura) / anual (veredicto) `[HIPÓTESIS]` | Autoridad ambiental nacional; guardián para el registro |
| **VIII · Costa e intermareal** | Mareógrafos y altimetría satelital (Copernicus Marine); cartografía de elevación y población; NOAA NCEI *Coastal Water Temperature Guide* y *coast.noaa.gov* como portales de datos costeros. **Intermareal y estero: `[SIN FUENTE VERIFICADA]`** | Anual (nivel del mar) / por construir (intermareal) | Autoridad costera; comunidad de custodia |
| **IX · Zona Libre** | **No se mide.** Se registra su presencia o ausencia en la identidad de la unidad (7 campos, documento 05) | En cada revisión de identidad | Guardián oráculo |

**Los cuatro huecos de protocolo, contados sin adornos.** (1) No hay protocolo operativo verificado
para Ω_arag en una unidad concreta; (2) no hay umbral numérico de hipoxia en fuente de organismo;
(3) no hay protocolo posible para intermareal y estero porque no hay umbral de referencia; (4) la
conectividad marina no tiene valor numérico publicado pese a que la Meta 3 la exige. **Sin protocolo
no hay violación demostrable**: lo que no tiene hecho observable asignado no puede activar INV2-E,
por mucho que tenga umbral numérico.

**La bandera de opacidad ecológica.** Regla propuesta y no ratificada: la **ausencia de monitoreo no
se convierte nunca en violación** del ecosistema (jamás se imputa un déficit por falta de dato), pero
**sí activa una obligación contractual de instrumentar** y una condición de validez del contrato. Es
la inversión de sujeto que el mar obliga a hacer: en los reinos humano, animal y sintético la
ausencia de evidencia protege al presunto vulnerado; en el mar el presunto vulnerado no reporta, de
modo que la misma regla protegería al presunto violador. Y **el 5 % de arrecifes que NOAA no cubre
no es Zona Libre: es deuda de instrumentación.**

---

## 7. Verificación y auditoría (T13, guardián, comunidad testigo)

**T13 — Transparencia de Cálculo: la contabilidad nunca se borra.** Toda violación marina se
documenta y es auditable, incluso cuando su cuantificación se delega o se difiere. En el mar esto
tiene una consecuencia práctica inmediata: **la discrepancia interna de una fuente se declara, no se
resuelve en silencio.** El comunicado de FAO *SOFIA 2024* da **76,9 %** en el cuerpo y **78,9 %** en
el recuadro «SOFIA 2024 in numbers» para el mismo indicador `[VERIFICADO]`. Este documento cita
**76,9 %** y deja constancia de la otra cifra y de su origen: eso es T13 aplicado a la propia
bibliografía.

**El problema estructural: no existe par auditor en el Reino Natural.** Ningún arrecife audita a
otro arrecife (documento 09, insight I3). La auditoría marina viene necesariamente de fuera, y ese
«fuera» es, en el caso costero típico, **el reino que se beneficia del uso**: la flota, la empresa
acuícola, el desarrollador costero, el operador turístico. Los 7 campos obligatorios de identidad de
una representación natural —entidad representada, territorio, fuentes de datos, límites del mandato,
comunidad de custodia, parámetros SDV-E y procedimiento de disputa— y la figura de la **comunidad
testigo** no son burocracia: son el **sustituto institucional del par auditor que no existe**.

**La ventaja marina, que es real y hay que usarla.** A diferencia del bosque o del humedal —cuyo
estado depende en gran medida de quienes lo explotan—, el arrecife tiene un juez externo que el
violador **no puede editar**: el producto satelital de NOAA Coral Reef Watch, con serie desde 1985 y
cobertura del 95 % de los arrecifes del mundo `[VERIFICADO]`. Es el primer caso en la familia SDV en
que la instrumentación no pertenece ni al proyecto ni al beneficiario. **Su costo:** dependencia de
un tercero estatal y de su continuidad presupuestaria (ver §13).

**Riesgos abiertos que agravan la falta de par auditor** (documentados en
[blindaje_anti_gamificacion_equidad.md](../../architecture/blindaje_anti_gamificacion_equidad.md)):

| ID | Riesgo | Ejemplo marino concreto |
|---|---|---|
| **R4** | **Partes fantasma**: cualquier usuario autenticado crea una parte `eco-*` y queda como su `owner`, sin verificar autoridad sobre la entidad | Una empresa de cultivo de camarón crea la parte `eco-` del manglar que va a convertir en estanques (el primer factor de pérdida de manglar documentado por la FAO es exactamente la acuicultura de camarón: 31 % → 21 %) |
| **R6** | **T9 (Reciprocidad Justa) no se valida en la creación**: un contrato 100 % unilateral pasa y se activa | Un contrato de extracción pesquera sin contraprestación al ecosistema se activa y consume el stock |
| **R13** | **Guardián eco con heurística laxa**: sin `DEEPSEEK_API_KEY` el guardián **aprueba si los invariantes pasan** | El consentimiento del arrecife se vuelve automático justo cuando el contrato es más dañino |

Además, el **quórum `eco-` N-de-M** que el libro afirma (Cap. 16.5 §16.5.14: *"consentimiento
agregado por quórum delegado N-de-M"*) **no está cableado**, y el canon no publica N ni M para el
Reino Natural. En el mar esto añade una pregunta propia: **una unidad marina suele tener varias
comunidades de custodia simultáneas** —pescadores artesanales, habitantes de la costa, pueblos
originarios, operadores turísticos— y el canon no dice quiénes son las M partes ni cómo se reparte
su voz. Va a la §13.

---

## 8. Invariante INV2-E: de estándar a contrato ejecutable

El invariante genérico **INV2** dice: *"Ninguna acción del contrato puede dejar a un participante
bajo su SDV"* (Cap. 17). La versión marina, `INV2-E`, es la que falta —no existe en el código—:

> *"Un conjunto con crédito regenerativo acumulado pero humedal bajo su SDV-E no está en coherencia:
> **INV2-E será su juez**."* — (Cap. 16.5 §16.5.14)

### 8.1 Los disparadores marinos, como hechos y no como valores

| # | Disparador | Naturaleza del hecho | Dimensión |
|---|---|---|---|
| **T1** | **DHW ≥ 8 con HotSpot ≥ 1** en la temporada térmica de la unidad | Lectura satelital pública, externa al violador | I |
| **T2** | **Ω < 1 en cualquier punto de la unidad** | Hecho químico, no requiere referencia histórica | II |
| **T3** | **Ω_arag bajo el 80 % del valor preindustrial de referencia**, cuando ese valor exista para la unidad | Requiere referencia declarada — hoy `[SIN FUENTE VERIFICADA]` por unidad | II |
| **T4** | **Pérdida neta de cobertura de coral vivo** o **inversión de dominancia coral→alga** | Medición in situ con línea base declarada | III |
| **T5** | **Extracción sin evaluación de stock publicada y vigente**; o captura por encima de la capacidad declarada | Hecho administrativo + hecho de registro | IV |
| **T6** | **AMP declarada sin régimen de gestión verificado** (parque de papel) | Hecho administrativo verificable | V |
| **T7** | **Pérdida neta de manglar o pradera marina** por causa humana documentada | Hecho espacial con atribución declarada | VI |
| **T8** | **Aparición o expansión documentada de zona hipóxica o anóxica** | Hecho medido por autoridad competente | VII |
| **T9-E** | **Pérdida irreversible de intermareal, marisma o estero**; **nueva ocupación permanente de la franja en riesgo**; **eliminación de defensa costera natural sin sustitución** | Hecho administrativo y espacial | VIII |

**Nota sobre la numeración.** `T9-E` se numera así para no confundirse con el axioma **T9
(no-antropocentrismo)**: son objetos distintos y el documento lo declara para que nadie los funda.

### 8.2 La unidad de duración en TA: la temporada térmica

Todo invariante necesita **unidad de duración explícita**, y el mar la tiene sin inventarla. El DHW
no se acumula en el año calendario: se acumula **en la temporada cálida de cada región**, y la
fuente publica ese calendario `[VERIFICADO]` —Atlántico norte y Pacífico norte, julio-septiembre;
Atlántico y Pacífico sur, enero-marzo; Índico norte, abril-junio; Índico sur, enero-abril—. Por
tanto:

- **La unidad de duración de la violación térmica de un arrecife es su temporada térmica.** Es un
  ciclo natural del ecosistema, no una unidad administrativa humana.
- Es **TA (Tiempo Absoluto)**: el tiempo del territorio, que **no se coloniza**. No se mide en TVI
  ni en TPI, y **no se convierte dentro de la fórmula**.
- **El PIU es el único traductor** TA↔TVI (Cap. 5 §5.5), y hoy es un `pass` con comentario
  `[VERIFICADO]`: la traducción existe como doctrina, no como ejecución. Mientras no exista, **el
  SDV-E marino puede juzgar y no puede facturar** — y eso hay que decirlo, no disimularlo.

**El contador con umbral, y por qué no se copia el 7.** El SDV-S retracta tras **7 ciclos
consecutivos** de violación (`max_consecutive_cycles = 7`, `[VERIFICADO]` en
[maxocontracts/blocks/sdv_s_validator.py](../../../maxocontracts/blocks/sdv_s_validator.py)). Ese 7
está expresado en **horas TPI**, y transferirlo por analogía a temporadas térmicas sería un error de
unidades: **7 temporadas consecutivas de mortalidad probable son más de media década de arrecife
muriendo.** La regla que este documento propone `[HIPÓTESIS]`, en lugar de un número copiado, es una
restricción: **el contador de ciclos consecutivos de una unidad marina no puede exceder el tiempo de
recuperación documentado de esa unidad.** Para el arrecife, la fuente documenta que la recuperación
desde un evento masivo puede tomar «potencialmente una década» (GCRMN/UNEP, 2021) `[VERIFICADO]`; el
valor concreto del contador queda como **propuesta no ratificada** y pertenece al documento 08.

### 8.3 La única acción ejecutable

Un río no se retracta ni se rehabilita por contrato, y un arrecife tampoco. **La única acción
ejecutable de `INV2-E` es detener o modificar la actividad humana que viola el piso**: parada de
extracción, cese de vertido, suspensión de la nueva ocupación costera, retirada de la barrera. El
paralelo canónico exacto es el *Veto por Crimen de Coherencia* del SDV-S: *"la interrupción total del
sistema que la provoca"* (Cap. 9.5 §9.5.10). Y con la asimetría marina declarada: **la reparación no
puede actuar sobre el sujeto**, porque el sujeto tarda décadas en volver y no firma contratos.

---

## 9. El suelo antes que el saldo (no compensación)

**La doctrina es literal del canon, y este documento la aplica sin suavizarla:**

> *"El suelo antes que el saldo"*: el crédito regenerativo acumulado **NO compensa** caer bajo el
> SDV-E (Cap. 16.5 §16.5.14).

**El caso marino, contado con sus números.** Una empresa costera planta manglar, lo documenta, y
registra `r_units` negativos —crédito regenerativo, implementado y probado en el código
`[VERIFICADO]`—. En la misma unidad, el arrecife cruza **DHW ≥ 8** y el agua tiene **Ω < 1**. Bajo la
doctrina del saldo, el crédito «compensaría». Bajo el SDV-E:

1. La violación del piso **existe** y se registra: es un hecho, no un saldo.
2. El crédito regenerativo vive en el eje **R** y **no se resta** del déficit del piso. `V` no admite
   negativos; `R` sí —son ejes distintos y esa separación es un invariante de diseño real del
   proyecto `[VERIFICADO]`—.
3. **INV2-E es el juez**, no la suma.

**El desplazamiento no es daño, y hay que decirlo antes de contar una hectárea.** Ninguna de las
ocho dimensiones mide «verde»: miden umbrales concretos. Un manglar que **retrocede tierra adentro**
al subir el nivel del mar, una marisma que **transgrede** sobre la cota que gana, un delta que
**cambia de brazo** o una duna que **migra** no son pérdida: son el ciclo natural del sistema
costero haciendo su trabajo, y por eso la violación de la Dimensión VI y la de la Dimensión VIII
exigen **causa humana documentada**. La pérdida **natural** —retracción, subsidencia, ciclón,
sedimentación— se registra como **pérdida no imputable**: no genera déficit contra la unidad, pero
**sí consume el margen disponible**, de modo que la ocurrencia repetida de pérdida natural **agrava**
cualquier pérdida humana posterior en la misma unidad. Lo que se pierde de verdad —y esto sí es
irreversible— es la **migración impedida**: cuando la ocupación, el relleno o la barrera **no dejan
al ecosistema moverse**, el ciclo que lo mantenía queda bloqueado y la pérdida deja de ser
desplazamiento para volverse desaparición.

**La confirmación externa, que no es del proyecto.** La FAO recomienda que la restauración de
manglar **cree condiciones para la colonización natural** en lugar de plantar, y el dato la respalda:
de **393 000 ha** ganadas en veinte años, **82 % fue expansión natural** y solo **18 % restauración**
`[VERIFICADO]`. Es decir: **lo que regenera es el proceso, no la intervención** — exactamente
*"se registra lo que regenera, no lo que adorna"* (Cap. 16.5 §16.5.14), verificado por una agencia
externa y no por el propio canon.

**Por qué el mar es el lugar donde esta doctrina se pone a prueba.** Es donde el «saldo» es más
fácil de fabricar: créditos de carbono azul, jardinería de coral, arrecifes artificiales,
«restauración» de praderas que no sobreviven al primer verano cálido. Y es donde la irreversibilidad
es más dura: a 2 °C el declive proyectado de los arrecifes es **> 99 %** (*very high confidence*,
IPCC SR1.5, 2018) `[VERIFICADO]`, y el nivel del mar **seguirá subiendo mucho más allá de 2100**
incluso a 1,5 °C (*high confidence*). **Lo que se pierde aquí no vuelve con una firma.**

**El estado real de esa contabilidad, dicho sin adornos.** El crédito regenerativo está registrado y
probado, pero **no pesa en ninguna cuenta**: no existe `SUM(r_units)`, el componente R del sistema
general solo cuenta extracción y el precio cierra en `max(0.0, …)` (`app/maxo.py`), de modo que
**nunca es negativo**. Dicho de otro modo: hoy el sistema puede registrar el cuidado y **no puede
registrar la deuda** — que es exactamente el agujero que esta biblioteca existe para cerrar.

---

## 10. Zona Libre: lo que NO se mide

*(La dimensión está desarrollada como Dimensión IX en la §4. Aquí se fija su estatuto metodológico,
que es lo que esta sección de la plantilla exige.)*

**Estatuto: dimensión binaria auditable, sin peso, fuera de la fórmula.** Precedente canónico: las
dimensiones VIII (Rehabilitación) y IX (Opacidad Vital) del SDV-H, que *"se registran cualitativamente
y mediante umbrales binarios (presencia/ausencia del derecho), no mediante pesos en la fórmula"*
(Cap. 8 §8.11). La razón es la misma que allí y aquí se agrava: **ponderar lo inefable lo vuelve
canjeable**, y un ecosistema con «mucha Zona Libre» podría compensar un blanqueamiento.

**Las tres cláusulas** (ZL-1 valor inefable · ZL-2 vida interna · ZL-3 vínculo con la comunidad de
custodia) están en la tabla de la Dimensión IX. Su violación es siempre la misma clase de hecho: **un
contrato, un índice o un pago que exige medir, certificar o poner precio a lo que se declaró
inefable.**

**La frontera que este documento traza y que impide que la Zona Libre sea un refugio.** Lo no medido
**por falta de instrumento no es Zona Libre: es opacidad ecológica**, y genera obligación de
instrumentar. NOAA Coral Reef Watch cubre el **95 %** de los arrecifes del mundo `[VERIFICADO]`: el
5 % restante es deuda de medición, no santuario inefable. Sin esta frontera, cada degradación no
medida se declararía inefable —la pregunta abierta nº 10 del documento 09— y la Zona Libre se
convertiría en la coartada técnica de la impunidad.

**Lo que la Zona Libre del mar añade a la doctrina de la familia.** El océano es el ecosistema más
instrumentado del planeta y, a la vez, el menos visto. Esa tensión —saber mucho de la temperatura
superficial y casi nada de la vida interna— es la razón por la que *"medir todo sería la forma
técnica de dejar de escucharlo"* (Cap. 16.5 §16.5.14) tiene aquí su caso más puro: la Zona Libre no
protege lo que no sabemos medir; protege lo que **decidimos no convertir en métrica**.

---

## 11. Comparativa inter-reinos (SDV-H · SDV-A · SDV-E · SDV-S)

### 11.1 La fila marina en la tabla de la familia

| Eje | SDV-H | SDV-A | **SDV-E (unidad marina-costera)** | SDV-S |
|---|---|---|---|---|
| **Para quién** | Toda persona humana (universal) | Cada especie animal sintiente; umbrales por especie | **La unidad ecológica marina-costera: arrecife, estero, bahía, AMP, gran ecosistema marino** (tres escalas declaradas, §4.2) | Cada Persona Sintética |
| **Unidad de medida** | Parámetros por dimensión, 7 + 2 binarias | 8 dimensiones genéricas, umbrales por especie | **8 dimensiones + 1 binaria; piso/techo por parámetro** | 5 dimensiones |
| **Moneda temporal** | Meses | No especificada | **TA: la temporada térmica (calendario regional publicado), el ciclo hidrológico, el ciclo de sucesión.** Nunca TVI | Horas TPI |
| **Representación** | La propia persona | Tutor humano | **Guardián oráculo + comunidad(es) de custodia; 7 campos de identidad; quórum N-de-M sin cablear** | La propia instancia |
| **Invariante** | INV2 | Bloque con parámetros por especie | **INV2-E — 🔴 no existe** | INV2-S |
| **Factor** | Suma ponderada | Tabla escalonada (0,2 con cumplimiento pleno) | **`FE = e^v`, base neutra 1,0; requiere la corrección piso/techo (§5.1)** | `FS_S = e^v` |
| **Quién audita** | Auditor independiente | Entidad certificadora | **Un tercero externo no editable (NOAA CRW) + comunidad testigo; sin par auditor del propio reino** | AOS (par sintético) |
| **Zona Libre** | Binaria (VIII, IX) | Parcial | **Binaria, sin peso, con frontera explícita contra la opacidad** | Peso 0,20 |

### 11.2 Qué aporta el SDV-E marino a la familia

1. **El primer piso y el primer óptimo publicados por la misma agencia.** En el SDV-H el piso venía
   de una directriz de salud humana (proxy declarado). Aquí el techo (8) y la plenitud (4) los
   publica **NOAA Coral Reef Watch** con significado biológico declarado. Es la primera dimensión de
   la biblioteca donde las dos columnas del brief tienen una **única fuente oficial**.
2. **La primera unidad de duración derivada de un ciclo natural publicado.** Los meses del SDV-H y
   las horas TPI del SDV-S son unidades humanas. La **temporada térmica del arrecife** es un ciclo
   del ecosistema con calendario regional publicado: TA puro, no colonizado.
3. **La corrección piso/techo de la fórmula.** El mar obliga a introducirla porque la mitad de sus
   parámetros son techos. Sin ella, un DHW de 20 daría déficit negativo.
4. **La separación explícita entre piso biológico y mínimo de gobernanza.** El 30×30 entra como
   obligación jurídica humana declarada como tal, no disfrazada de ley ecológica.
5. **Un auditor que el violador no puede editar**, por primera vez en la familia.
6. **Una dimensión completa sin fuente, sostenida sin fingir** (costa e intermareal): el documento
   escribe la dimensión, declara el vacío y lo deja como tarea, en lugar de rellenarlo.

### 11.3 Qué aprende de cada reino

| De | Aprende |
|---|---|
| **SDV-H** | (1) La separación Mínimo Absoluto / Óptimo en dos columnas, que es el error que el brief prohíbe repetir. (2) El preámbulo metodológico obligatorio. (3) Los pesos suman 1,0 y la fórmula es una suma ponderada, no un producto. (4) Las **dimensiones binarias sin peso** para lo inconmensurable (Cap. 8 §8.11), precedente directo de la Zona Libre del océano. |
| **SDV-A** | (1) Un estándar puede ser **genérico en dimensiones y específico en umbrales por unidad**: es el precedente exacto de los umbrales DHW por latitud. (2) El factor como **tabla escalonada con un final no aritmético** da la forma correcta: el «infinito» se implementa como estado. (3) Los cinco criterios de validación de parámetros, traducibles a criterios ecológicos. |
| **SDV-S** | (1) **La base neutra es innegociable**: `e^v`, no `1 + e^v`; el factor vale exactamente 1,0 sin violación. (2) Una violación necesita **unidad de duración explícita**. (3) El **elenco de sensores con umbral** es el modelo formal del protocolo de medición. (4) La retractación exige **contador con umbral** —con la corrección marina: el contador no puede exceder el tiempo de recuperación documentado de la unidad. (5) La **Paradoja de los Modelos Cerrados** enseña qué hacer con la opacidad, con la inversión de sujeto que el mar obliga (§6). |
| **Del propio canon del SDV-E** | El ISE existe con pesos y bandas y **no tiene ningún componente marino** `[VERIFICADO]`. Este documento no lo amplía: construye la primera lista marina y declara que **el índice es tablero, no estándar**. |

### 11.4 Lo que esta comparación NO autoriza a concluir

1. **No autoriza a trasvasar el umbral térmico del arrecife a otro ecosistema**: 4 y 8 están
   calibrados para arrecifes **tropicales**; no se transfieren a latitudes templadas.
2. **No autoriza a usar el 30×30 como piso de integridad**: es cobertura, no salud.
3. **No autoriza a tratar el pH marino legal (6,5-8,5) como umbral de acidificación**: es ciego al
   proceso.
4. **No autoriza a promediar el mar**: un parámetro sin profundidad, sin estación y sin superficie
   de muestreo no es un dato.
5. **No autoriza a ponderar la Zona Libre**, ni a declarar Zona Libre lo que solo está sin
   instrumentar.
6. **No autoriza a compensar**: el crédito regenerativo no salda el piso (§9).

---

## 12. Estado de implementación

**Verificación de esta sesión (lectura directa del repositorio, octubre 2026).** Este documento es
**el estándar primero**; la contabilidad viene después (Cap. 16.5 §16.5.14). Y el estado real, dicho
con el inventario de implementación de la rama delante, es este:

**Búsqueda ejecutada en esta sesión:** patrón `dhw|coral|arrecife|aragonit|manglar|seagrass|pradera
marina|acidificación|ocean|pesquer|hipoxia|noaa` sobre **todos los archivos `.py` del repositorio**
→ **cero coincidencias** (el alcance es `.py`: el patrón no busca en `simulator/` ni en `docs/`, y se
declara para que la afirmación no se lea más ancha de lo que es). No hay una sola línea de código
marino en el proyecto.

| Pieza | Estado | Evidencia verificada |
|---|---|---|
| Tipo `SDV_E` en el motor | 🔴 **NO EXISTE** | [maxocontracts/core/types.py](../../../maxocontracts/core/types.py) define `SDV` y `SDV_S`; **no hay `SDV_E`** (verificado en esta sesión) |
| `INV2-E` (invariante) | 🔴 **NO EXISTE** | [maxocontracts/core/axioms.py](../../../maxocontracts/core/axioms.py) tiene `validate_invariant_sdv` y `validate_invariant_sdv_s`; **no hay `validate_invariant_sdv_e`** (verificado) |
| Bloque validador `SDV_EValidatorBlock` | 🔴 **NO EXISTE** | `maxocontracts/blocks/` contiene `sdv_validator.py`, `sdv_s_validator.py`, `ternura.py`, `gamma_protector.py`, `reciprocity.py`, `action.py`, `condition.py` — **no hay `sdv_e_validator.py`** |
| **Sensores e ingestores marinos** | 🔴 **CERO** | Ningún ingestor de NOAA CRW, Copernicus, Protected Planet, FAO ni WDPA. Ninguna lectura de DHW, HotSpot, Ω_arag, oxígeno ni cobertura |
| Métrica ecológica en código (ISE) | 🔴 **NO EXISTE** | El ISE vive solo en [metricas_detalle_kpis_oraculos_dinamicos.md](../../architecture/metricas_detalle_kpis_oraculos_dinamicos.md); **y no tiene componente marino** (verificado) |
| Traducción TA↔TVI ejecutable (PIU) | 🔴 **NO EXISTE** | `PIU.valorar_ta_natural` es un `pass` con comentario en [DISENO_IMPLEMENTACION_FUTURA.md](../../architecture/DISENO_IMPLEMENTACION_FUTURA.md) (verificado) |
| Contabilidad del crédito regenerativo | 🔴 **NO EXISTE** | No hay `SUM(r_units)`; el R del sistema solo cuenta extracción y el precio cierra en `max(0.0, …)` ([app/maxo.py](../../../app/maxo.py)): **nunca es negativo** |
| Validación de `r_units` | 🔴 **NO EXISTE** | Acepta cualquier negativo (`-1e9`); `NaN` e `inf` pasan el filtro; no exige nota, evidencia, tercero ni techo |
| Identidad de la representación natural (7 campos) | 🔴 **NO EXISTE** | Sin tabla; `maxo_parties` tiene columnas genéricas |
| Mandato ecológico versionado / OCI | 🔴 **NO EXISTE** | `actor_kind` está cerrado a `{"human","synthetic"}` en [app/synthetic_sessions.py](../../../app/synthetic_sessions.py): **un guardián ecológico no cabe en la bitácora** |
| Anti-suplantación de unidad natural | 🔴 **NO EXISTE** | Sin fuentes físicas múltiples ni comunidad testigo (R4 abierto) |
| Quórum `eco-` N-de-M | 🔴 **NO CABLEADO** | El camino ecosistema retorna antes de la lógica de quórum; **el libro afirma lo contrario** (Cap. 16.5 §16.5.14) |
| Procedimiento de disputa | 🔴 **NO EXISTE** | Inexistente |
| Protocolo operativo de medición marina | 🔴 **NO EXISTE** | Cuatro huecos declarados en §6, incluido Ω_arag in situ |
| Mapas vivos actualizados | 🔴 **NO** | `mapa_coherencia_ola4.md` no menciona `r_units`, el Reino Natural ni el SDV-E; `requisitos_fase2_ola4.md` no tiene ningún RF del Reino Natural |

**Lo que SÍ existe (y es honesto decir que existe):**

| Pieza | Dónde | Estado |
|---|---|---|
| `r_units` negativo como crédito regenerativo | [app/micromax.py](../../../app/micromax.py) (`log_cdd`) | 🟢 registrado y devuelto en el vector `[T, V, R]`; **con el comentario canónico «`r_units` NEGATIVO = credito regenerativo (EVV 1.2 s4.3)»** (verificado en esta sesión); **sin efecto contable** |
| **V no admite negativos; R sí** | `app/micromax.py` (`if v_ucv < 0: raise`) | 🟢 invariante de diseño real |
| Test del crédito regenerativo | `tests/test_micromax.py::test_credito_regenerativo_r_negativo` | 🟢 `r_units: -12.0` aceptado y devuelto |
| Parte `eco-` (Ecosistema) | [app/parties.py](../../../app/parties.py) (`PARTY_TYPES`, `COLLECTIVE_PREFIXES`) | 🟢 creada y usable |
| Guardián oráculo del ecosistema | [app/contracts_bp.py](../../../app/contracts_bp.py) (`_guardian_approve_ecosystem`) | 🟡 funciona en la firma de contratos; **heurística laxa (R13)** |
| Test del guardián | `tests/test_maxocontracts/test_parties_escalas.py` (`TestEcosystemGuardian`) | 🟢 2 casos (aprueba / deniega por γ) |
| Validador de déficit normalizado | [maxocontracts/blocks/sdv_validator.py](../../../maxocontracts/blocks/sdv_validator.py) | 🟢 calcula `relative = deficit / required` y clasifica severidad (≤10 % leve · ≤30 % moderada · >30 % severa): **es la base de la §5.3** |
| SDV-S + INV2-S (el pariente más cercano) | `maxocontracts/` | 🟢 estándar + tests en `test_sdv_s.py` y `test_ternura.py`; `max_consecutive_cycles = 7` |

**Incoherencias colaterales que este documento no hereda:** `resolve_participant_by_pid`
([app/parties.py](../../../app/parties.py)) asigna a una parte `eco-` **el SDV humano**
(`sdv_actual=SDV()`), porque no existe SDV-E —es decir, hoy un arrecife es evaluado con el estándar
de una persona—; la R del contrato se persiste en la columna **`total_vhv_h` / `vhv_h`**
([app/schema.sql](../../../app/schema.sql), [app/contracts_bp.py](../../../app/contracts_bp.py)),
nombre engañoso y sin `CHECK` de signo; y `simulator/simulator.js` usa `v: -0.5` (V negativo)
mientras `app/micromax.py` lo prohíbe.

**Estado de este documento:** texto de estándar redactado (este archivo), **sin ninguna pieza de
código asociada**. No añade requisitos de implementación nuevos: hace explícitos los que el canon ya
exige y el código no tiene.

---

## 13. Preguntas abiertas

Lo que este documento **no** resuelve. Se dice sin fingir cierre, y se ordena por gravedad.

### Vacíos que bloquean dimensiones enteras

1. **Umbral numérico de hipoxia (O₂ disuelto).** La cifra de **2 mg/L ≈ 60 µmol/kg** es estándar en
   la literatura y aparece en documentos institucionales indexados, pero **no se leyó en página
   oficial de organismo**: `[SIN FUENTE VERIFICADA — pendiente de consenso científico]`. La IUCN mide
   el fenómeno en **% de pérdida**, no con umbral absoluto. **Impacto:** sin umbral no hay piso para
   el parámetro más directo de la pérdida de integridad en aguas costeras y esteros. Es el mismo muro
   contra el que chocó el agua dulce del documento 09 (vacío 5 de su informe).
2. **Punto de referencia de biomasa pesquera (`B/Bmsy`, `B_MSY`, `F_MSY`, MSY).** La página de estado
   de poblaciones de NOAA Fisheries respondió 200 **sin cargar el texto de definición** → el criterio
   convencional **no se transcribe**. `[SIN FUENTE VERIFICADA]`. **Impacto:** el SDV-E no puede fijar
   hoy un techo de extracción por unidad.
3. **Conectividad marina — sin umbral numérico.** La Meta 3 exige redes «bien conectadas» y **no la
   cuantifica**; NOAA publica un producto de conectividad larvaria, pero ningún documento abierto en
   esta sesión fija un valor. `[SIN FUENTE VERIFICADA]`. **Impacto:** idéntico hueco al de la
   conectividad terrestre: el SDV-E no tiene umbral de conectividad **ni en tierra ni en mar**, y el
   canon la exige (Cap. 10 §10.4).
4. **Zona intermareal y esteros — sin ningún umbral.** No se encontró fuente de organismo que fije
   rango de marea mínimo, salinidad, hidroperiodo, ratio de mezcla dulce-marino ni extensión mínima
   de marisma; `ramsar.org` devuelve **403 en las cuatro rutas probadas** y `unep.org/resources/*`
   está bloqueado. `[SIN FUENTE VERIFICADA — pendiente de consenso científico]`. **Impacto: hoy el
   SDV-E no puede escribir la dimensión «costa» con fuente.** Es la misma estructura que el caudal
   ecológico: **canon sí / fuente no**.

### Arrecifes y acidificación

5. **Cobertura mínima de coral vivo** para considerar un arrecife íntegro: hay cifras de pérdida y
   **ninguna de piso**. `[SIN FUENTE VERIFICADA]`. Este documento propone no regresión + dominancia
   `[HIPÓTESIS]` y lo declara **POLÍTICA votable, no LEY**.
6. **Umbrales DHW para arrecifes templados y subtropicales.** La escala 4/8 está calibrada para
   arrecifes tropicales; hay indicios de blanqueamiento generalizado en latitudes mayores, pero **no
   se abrió ni verificó** el artículo que lo reporta. `[SIN FUENTE VERIFICADA]`. **Impacto:** puede
   hacer falta una tabla de umbrales por latitud, y hoy solo existen los tropicales.
7. **Ω_arag regional por unidad ecológica — el hueco más serio de la acidificación.** Las cifras
   verificadas son **globales** (Ω = 3,44 preindustrial; 2,9 en 2015). No se encontró Ω_arag de
   referencia por región ni por arrecife, y la fuente señala «fuerte variabilidad regional y
   estacional» **sin dar valores**. `[SIN FUENTE VERIFICADA]`. **Impacto:** el SDV-E se define por
   unidad ecológica; un umbral solo global no permite juzgar un arrecife concreto.
8. **Ω_arag actual (2025-2026) tras la transgresión.** El Stockholm Resilience Centre confirma que la
   frontera **fue transgredida en 2025**, pero **no publica el valor vigente** y el sitio donde
   estaría el detalle (`planetaryhealthcheck.org`) **no resuelve (000)**. El único número disponible
   es de **2015**. `[SIN FUENTE VERIFICADA]`. **Impacto:** hoy se puede declarar «que» se transgredió,
   no «cuánto».
9. **Protocolo de sensor de Ω_arag in situ** (qué se mide, con qué precisión, con qué frecuencia,
   quién lo certifica): `[SIN FUENTE VERIFICADA]`. Sin él, la dimensión tiene piso y no tiene
   medición.

### Pesquerías, gobernanza y métrica

10. **MSY como umbral del SDV-E**: no se encontró en fuente de organismo abierta un valor de MSY ni
    de `F_MSY` citable. `[SIN FUENTE VERIFICADA]`.
11. **Tasa de captura incidental admisible**: no buscada con éxito; no hay umbral.
    `[SIN FUENTE VERIFICADA]`.
12. **Proporción mínima de especies clave o depredadores apicales**: no encontrada en fuente abierta.
    `[SIN FUENTE VERIFICADA]`. **Impacto:** el ISE le da un **15 %** de peso a «poblaciones de
    especies clave» y **no existe fuente externa que cuantifique ese umbral para el medio marino**.
13. **La Meta 10 del GBF no tiene ningún indicador numérico** —verificado leyendo la página oficial—:
    no es un vacío de búsqueda, es un dato del tratado. El SDV-E no puede derivar de ahí ningún
    número.
14. **El 30×30 es una meta de cobertura, no de integridad**: ninguna de las Metas 2 y 3 fija umbrales
    de salud del ecosistema. **Impacto:** el SDV-E **no puede adoptar el 30×30 como mínimo absoluto de
    integridad sin cometer un salto lógico**; este documento lo usa como mínimo de gobernanza y lo
    declara.
15. **Umbrales de la Lista Roja de Ecosistemas de la IUCN aplicados a ecosistemas marinos.** La URL
    del criterio y el libro de 2023 están vivos, pero **no se abrió el PDF** y no se transcriben sus
    umbrales numéricos. `[SIN FUENTE VERIFICADA]` con la URL ya validada para una extracción futura.

### Manglar, pradera marina y costa

16. **Umbral mínimo de extensión de manglar por unidad**: la FAO da extensión y pérdida, **ningún
    mínimo**. `[SIN FUENTE VERIFICADA]`.
17. **Tasa de deforestación de manglar admisible**: la FAO reporta **desaceleración**, no un objetivo.
    `[SIN FUENTE VERIFICADA]`.
18. **Extensión mundial de praderas marinas (km²)**: no encontrada en fuente de organismo accesible
    (UNEP `resources/*` bloqueado). `[SIN FUENTE VERIFICADA]`.
19. **Tasa de pérdida anual de praderas marinas**: el **> 10 % por década (1970-2000)** de IPBES sí
    está verificado; el **7 %/año desde 1990** de Waycott *et al.* queda **`[REPORTADO]`** —visto
    citado, **sin abrir el artículo original**—. `[SIN FUENTE VERIFICADA]` para el 7 % anual.
20. **Cobertura mínima de pradera marina** para función de guardería o amortiguación costera:
    `[SIN FUENTE VERIFICADA]`.
21. **Rango de marea, cota de inundación y retrogradación de marisma**: no encontrado.
    `[SIN FUENTE VERIFICADA]`.

### Decisiones del proyecto que ninguna fuente puede dar

22. **Los pesos de las ocho dimensiones.** No existe ningún organismo que publique ponderaciones de
    integridad marina. La tabla de la §5.2 es una **decisión del proyecto** y pertenece al
    Parlamento.
23. **El contador de ciclos consecutivos del `INV2-E` marino.** Este documento propone la regla («no
    puede exceder el tiempo de recuperación documentado de la unidad») y **no fija el número**.
24. **La pluralidad de comunidades de custodia en una unidad marina.** Una misma bahía tiene
    pescadores artesanales, habitantes de la costa, pueblos originarios y operadores turísticos.
    **¿Quiénes son las N partes y las M voces del quórum `eco-`?** El canon no lo dice y el mar
    multiplica el problema que la tierra ya tenía.
25. **La atribución de la pérdida.** ¿Cómo se distingue una pérdida de cobertura causada por un
    ciclón de una causada por sedimentación humana, en la misma unidad y el mismo año? La FAO ofrece
    una pista —los desastres naturales fueron el **2 %** de la pérdida de manglar, pero **el área
    destruida se triplicó**— y este documento **no resuelve el método de atribución**. Es un requisito
    para que la violación (a) de la Dimensión III sea exigible.
26. **La dependencia externa del instrumento.** El SDV-E marino depende de la continuidad
    presupuestaria de un tercero estatal (NOAA) y de la disponibilidad abierta de sus productos. **Si
    el producto se retira, ¿qué pasa con el estándar?** El precedente existe y es verificable: el
    producto de 50 km fue **retirado el 30 de abril de 2020** y sustituido por el de 5 km. La
    pregunta de gobernanza —qué hace el SDV-E cuando su juez externo desaparece— **queda abierta**.
27. **¿La Zona Libre binaria puede auditarse sin volverse refugio?** Este documento aporta la
    frontera («lo no medido por falta de instrumento es opacidad, no Zona Libre») y **no demuestra
    que la frontera sea infalsificable**: quién califica un aspecto como «inefable por naturaleza» es,
    hoy, el guardián. Queda como pregunta de gobernanza para el documento 05.

---

## 14. Referencias

**Regla aplicada.** Solo URLs con **estado HTTP registrado en la sesión de verificación de esta rama
(octubre 2026)**. Ninguna cifra de este documento se apoya en una URL sin estado. Se indica el estado
entre paréntesis. **Las URLs muertas no se citan** (entre ellas tres rutas «intuitivas» de
`coralreefwatch.noaa.gov` que aparecen en resultados de búsqueda y devuelven **404**:
`/satellite/dhw.php`, `/product/vs/gauges.php`, `/satellite/methodology/methodology.php`).

**Alcance y trazabilidad.** El inventario completo de la sesión vive en el informe de fuentes del
documento 13, que **no es un documento de la biblioteca** y por tanto no se enlaza aquí como si fuera
canon. De sus totales **no se transcribe aquí ninguno**: el informe declara en su encabezado
«55 verificadas · 18 bloqueadas · 11 muertas», su anexo enumera **46** verificadas y la tabla de
bloqueadas enumera **12** entradas. Las tres cifras no cuadran entre sí y este documento **no hereda
la discrepancia**: lo único que afirma, y que sí se comprobó, es que **las 52 URLs citadas en este
texto figuran una a una en el informe de fuentes con estado registrado, sin ninguna URL inventada ni
sin registrar**. Las afirmaciones de la §12 se verificaron **por lectura directa del repositorio** en
esta sesión, no por URL: el árbol de archivos y las búsquedas de patrones son la evidencia y
cualquier lector puede repetirlas.

### 14.1 Arrecifes de coral — estrés térmico, blanqueamiento y cobertura

| Fuente | Aporte | URL (estado) |
|---|---|---|
| NOAA Coral Reef Watch — descripción de la escala de alerta y de los productos DHW | Tramos: «No Stress» (HotSpot ≤ 0) · *Bleaching Watch* (0 < HotSpot < 1) · *Warning* (HotSpot ≥ 1 y 0 < DHW < 4) · **Alert Level 1 «Bleaching Likely» (4 ≤ DHW < 8)** · **Alert Level 2 «Mortality Likely» (DHW ≥ 8)**; umbral de blanqueamiento **MMMSST + 1 °C**; líneas de alerta en DHW = 4 y DHW = 8 | https://www.coralreefwatch.noaa.gov/product/50km/description_vs_graphs.php (200) |
| NOAA OSPO — sistema de alerta de blanqueamiento | Productos: SST (CoralTemp), anomalía de SST, HotSpot, DHW, área de alerta de blanqueamiento (1 día y máximo 7 días), tendencia de SST a 7 días; **212 estaciones virtuales** regionales (desde octubre de 2016) | https://www.ospo.noaa.gov/Products/ocean/cb/alert_system/ (200) |
| NOAA Coral Reef Watch — producto de 5 km | **5 km, diario, serie desde el 1 de enero de 1985**; monitorea el **95 %** de los arrecifes del mundo; el producto de 50 km fue **retirado el 30 de abril de 2020** | https://www.coralreefwatch.noaa.gov/product/5km/index.php (200) |
| NOAA Coral Reef Watch — portal y mapas de estrés | Raíz del programa (fuente ancla del brief, **viva**) y visor de estaciones virtuales | https://coralreefwatch.noaa.gov/ (200) · https://www.coralreefwatch.noaa.gov/product/vs/map.php (200) |
| GCRMN / UNEP, 2021 — *Status of Coral Reefs of the World: 2020* (nota de prensa) | **~14 %** de pérdida de coral vivo entre 2009 y 2019; **9 %** de coral duro desde 1978; **+20 %** de alga (2010-2019); **8 %** del coral mundial muerto en 1998 (≈ 6 500 km²); **+2 %** de recuperación en 2019; el arrecife ocupa el **0,2 %** del fondo marino y alberga **≥ ¼** de las especies marinas. *Nota de método: devuelve **403 con curl** pero fue abierta con la herramienta web y su contenido **sí se leyó*** | https://www.unep.org/news-and-stories/press-release/rising-sea-surface-temperatures-driving-loss-14-percent-corals-2009 (403 curl / 200 lectura) |
| IPCC, 2018 — Informe especial 1,5 °C, Resumen para responsables de políticas | **70-90 %** de declive adicional de arrecifes a 1,5 °C (*high confidence*), cota que este documento incorpora además a la tabla de la Dimensión III; **> 99 %** de pérdida a 2 °C (*very high confidence*); captura marina **−1,5 Mt** a 1,5 °C y **> −3 Mt** a 2 °C; nivel del mar **0,26-0,77 m** a 2100 con 1,5 °C (**0,1 m menos** que a 2 °C); hasta **10 millones** de personas menos expuestas; riesgo de pérdida irreversible creciente, especialmente a 2 °C o más | https://www.ipcc.ch/sr15/chapter/spm/ (200) |
| IPBES, 2019 — nota de prensa de la Evaluación Global | **~50 %** de coral vivo perdido desde la década de 1870; **~33 %** de las especies de corales formadores de arrecife amenazadas; **66 %** del ambiente marino significativamente alterado; **100-300 millones** de personas en riesgo por pérdida de hábitat costero protector; **×10** de contaminación plástica desde 1980; **> 55 %** del área oceánica bajo pesca industrial; **> 90 %** de los pescadores son de pequeña escala y aportan **~50 %** de la captura mundial; **400** zonas muertas costeras sobre **> 245 000 km²** | https://www.ipbes.net/news/Media-Release-Global-Assessment (200) |

### 14.2 Acidificación oceánica y saturación de aragonito

| Fuente | Aporte | URL (estado) |
|---|---|---|
| Stockholm Resilience Centre — frontera de acidificación oceánica | Variable de control: **Ω_arag**; frontera **transgredida en 2025** (séptima frontera planetaria); el océano capta **~25 %** del CO₂ antropogénico; el horizonte de saturación de aragonito **asciende** hacia la superficie y amenaza corales de aguas frías y profundas; regionalización (el Ártico acidifica más rápido) | https://www.stockholmresilience.org/research/planetary-boundaries/the-nine-planetary-boundaries/ocean-acidification.html (200) |
| SDES (Ministerio de Transición Ecológica, Francia), 2021 — *La France face aux neuf limites planétaires*, cap. 9 | **Ω = 3,44** preindustrial (1850) y frontera en el **80 %** de ese valor; **Ω = 2,9** (**84 %** del preindustrial) en 2015 y proyección **2,80** hacia 2050; **Ω < 1** = agua subsaturada y corrosiva; pH superficial **8,2 → 8,1** (−0,1 = **+30 %** de acidez) y **≈ 7,7** a 2100 (RCP 8.5); **Ω < 3** en aguas tropicales de arrecife a 2100; **60 %** de las aguas superficiales antárticas corrosivas a 2100. Cifras atribuidas a Steffen *et al.*, 2015 (*Science*) | https://www.statistiques.developpement-durable.gouv.fr/edition-numerique/la-france-face-aux-neuf-limites-planetaires/en/9-ocean-acidification (200) |
| US EPA, 1986 y posteriores — criterios recomendados de calidad del agua para la vida acuática | **pH marino 6,5-8,5**; tablas CMC/CCC por metal; alcalinidad y cloruro con valores numéricos. *Advertencia: este criterio **no** detecta la acidificación (el pH oceánico cayó a 8,1, dentro de la banda)* | https://www.epa.gov/wqc/national-recommended-water-quality-criteria-aquatic-life-criteria-table (200) |
| NOAA — portal de acidificación oceánica | Portal del programa (verificado como **portal**; **no abierto para cifras** en esta sesión) | https://oceanacidification.noaa.gov/ (200) |

### 14.3 Pesquerías y biomasa

| Fuente | Aporte | URL (estado) |
|---|---|---|
| FAO, *SOFIA 2024* — nota de prensa de *The State of World Fisheries and Aquaculture* | **62,3 %** de las poblaciones marinas monitoreadas dentro de niveles biológicamente sostenibles en 2021 (**2,3 puntos menos** que en 2019) y **37,7 %** fuera; ponderado por desembarques **76,9 %** en el cuerpo del comunicado y **78,9 %** en el recuadro «SOFIA 2024 in numbers» (**discrepancia interna declarada**); producción de captura **81 Mt** marina + **11,3 Mt** continental = **92,3 Mt** (2022) | https://www.fao.org/newsroom/detail/fao-report-global-fisheries-and-aquaculture-production-reaches-a-new-record-high/en (200) |
| NOAA Fisheries — estado de las poblaciones (2023) | Página **verificada (200) pero sin el texto de definición** de «overfished» / «overfishing»: por eso `B/Bmsy` queda `[SIN FUENTE VERIFICADA]` y **no se transcribe** el criterio B < ½ B_MSY | https://www.fisheries.noaa.gov/national/sustainable-fisheries/status-stocks-2023 (200, sin contenido útil) |

### 14.4 Áreas marinas protegidas, restauración y meta 30×30

| Fuente | Aporte | URL (estado) |
|---|---|---|
| CBD, 2022 — Marco Kunming-Montreal, **Meta 3** | **≥ 30 %** de las áreas marinas y costeras conservadas para 2030, *"ecológicamente representativas, bien conectadas y gobernadas equitativamente"*, integradas en el océano | https://www.cbd.int/gbf/targets/3 (200) |
| CBD, 2022 — Marco Kunming-Montreal, **Meta 2** | Restauración efectiva de **≥ 30 %** de los ecosistemas degradados —terrestres, de aguas continentales, **marinos y costeros**— para 2030 | https://www.cbd.int/gbf/targets/2 (200) |
| CBD, 2022 — Marco Kunming-Montreal, **Meta 10** | Gestión sostenible de la pesca y la acuicultura: **`[SIN FUENTE VERIFICADA]` numéricamente — la Meta no fija ningún umbral**, es enteramente cualitativa | https://www.cbd.int/gbf/targets/10 (200) |
| UNEP-WCMC / IUCN — Protected Planet, áreas marinas protegidas | **23,09 %** de las aguas nacionales (el **39 %** del océano); **1,45 %** de las ABNJ (el **61 %** del océano); **17 389** AMP registradas; entrada en vigor del **BBNJ en enero de 2026** | https://www.protectedplanet.net/en/thematic-areas/marine-protected-areas (200) |
| CBD — portal del Marco Mundial de Biodiversidad | Portal de referencia del GBF | https://www.cbd.int/gbf (200) |

### 14.5 Manglares, praderas marinas y carbono azul

| Fuente | Aporte | URL (estado) |
|---|---|---|
| FAO, 2023 — *The World's Mangroves, 2000-2020* (nota de prensa) | **14,8 millones ha** de manglar (2020); **677 000 ha** perdidas (2000-2020) y **> 20 %** en 40 años; **−23 %** de la tasa de pérdida en la segunda década; **393 000 ha** ganadas; **82 %** expansión natural / **18 %** restauración; factores de pérdida: acuicultura de camarón en estanque **31 % → 21 %**, retracción natural **26 %**, desastres naturales **2 %** con el área destruida **triplicada**; **6,23 Gt C** almacenadas; **123 países** con manglar; recomendación operativa: **crear condiciones para la colonización natural** | https://www.fao.org/newsroom/detail/global-effort-to-safeguard-mangroves-steps-up/en (200) |
| FAO — ficha del informe de manglares | Documento de referencia del informe (ruta verificada) | https://www.fao.org/documents/card/en/c/cc7044en (200) |
| FAO / SER / IUCN CEM, 2023 — *Standards of practice to guide ecosystem restoration* | Estándares de práctica de restauración ecológica (alternativa viva a la ruta bloqueada de la SER) | https://www.fao.org/documents/card/en/c/cc5223en (200) |

### 14.6 Oxígeno, hipoxia y zonas muertas

| Fuente | Aporte | URL (estado) |
|---|---|---|
| IUCN, 2019 — *Ocean deoxygenation* (nota de política, diciembre 2019) | De **45 sitios antes de 1960** a **~700 en 2011**; pérdida de **~2 %** del oxígeno disuelto desde mediados del siglo XX y proyección **3-4 %** a 2100 (RCP 8.5); volumen de aguas anóxicas **cuadruplicado**; **~50 %** de la pérdida atribuible al aumento de temperatura; mayor pérdida entre **100-300 m**; dos causas (calentamiento y eutrofización); los afloramientos costeros del borde oriental sostienen **una quinta parte** de la cosecha mundial de peces marinos silvestres | https://iucn.org/resources/issues-brief/ocean-deoxygenation (200) |
| IUCN — informe completo de desoxigenación | Documento de referencia | https://portals.iucn.org/library/sites/library/files/documents/2019-048-En.pdf (200) |

### 14.7 Observación, datos y portales candidatos (sin umbral propio)

Estos enlaces **no sostienen ninguna cifra de umbral** de este documento: se citan como
infraestructura de medición candidata para el protocolo de la §6, y ese estatuto se declara.

| Fuente | Aporte | URL (estado) |
|---|---|---|
| Copernicus — servicio marino | Infraestructura europea de observación marina | https://www.copernicus.eu/en/copernicus-services/marine (200) |
| NOAA NCEI — *Coastal Water Temperature Guide* | Guía de temperatura de agua costera (dato de apoyo) | https://www.ncei.noaa.gov/products/coastal-water-temperature-guide (200) |
| NOAA — *Digital Coast* | Datos y herramientas costeras | https://coast.noaa.gov/digitalcoast/ (200) |
| IOC-UNESCO | Comisión Oceanográfica Intergubernamental | https://www.ioc-unesco.org/ (200) |
| GCRMN · ICRI · Reef Check · Reef Resilience | Redes de monitoreo de arrecifes y ciencia ciudadana (verificadas **como portales**: ninguna fija umbral en su página de inicio) | https://gcrmn.net/ (200) · https://icriforum.org/ (200) · https://www.reefcheck.org/ (200) · https://www.reefresilience.org/ (200) |
| UNEP-WCMC · UNEP · UNCCD | Marcos institucionales de referencia | https://www.unep-wcmc.org/en (200) · https://www.unep.org/ (200) · https://www.unccd.int/ (200) |
| ONU — ODS 14 (vida submarina) | Marco de referencia del objetivo marino | https://sdgs.un.org/goals/goal14 (200) |
| *Decade on Restoration* | Marco de restauración de ecosistemas (2021-2030) | https://www.decadeonrestoration.org/ (200) |
| US EPA — contaminación por nutrientes | Portal (la EPA publica criterios **por tipo de masa de agua**, sin escalar único: por eso la eutrofización costera queda `[SIN FUENTE VERIFICADA]` como umbral) | https://www.epa.gov/nutrientpollution (200) |
| IUCN — Lista Roja de Ecosistemas y Tipología Global de Ecosistemas | Marcos metodológicos (la URL de los criterios está viva; **el PDF de umbrales no se abrió**) | https://www.iucn.org/resources/conservation-tools/iucn-red-list-ecosystems (200) · https://www.iucn.org/resources/publication/iucn-global-ecosystem-typology (200) |

### 14.8 Fuentes reales que bloquean a los agentes automáticos (403)

Se listan porque **una persona sí las abre** y porque su bloqueo **tiene consecuencias declaradas en
este documento**. Ninguna sostiene una cifra de este texto.

| Fuente | Aporte | URL (403) |
|---|---|---|
| Convención de Ramsar (raíz, criterios y notas) | Marco de humedales: **cuatro rutas probadas, todas 403** (confirmadas 403 en la comprobación de esta revisión). Consecuencia directa: **la dimensión de zona intermareal y esteros queda sin fuente Ramsar verificable** (§13, vacío 4) | https://www.ramsar.org/ · https://www.ramsar.org/criteria-wetlands-international-importance · https://www.ramsar.org/about-the-ramsar-convention · https://www.ramsar.org/news/out-blue-value-seagrasses-environment-people (403) |
| UNEP — informes de recursos (GCRMN completo, *Out of the Blue* sobre praderas marinas, portales temáticos de océano) | Patrón `unep.org/resources/*` **bloqueado**: por eso el **7 %/año** de praderas marinas queda `[REPORTADO]` | https://www.unep.org/resources/status-coral-reefs-world-2020 · https://www.unep.org/resources/report/out-blue-value-seagrasses-environment-and-people · https://www.unep.org/explore-topics/ocean-seas-and-coasts (403) |
| *World Ocean Assessment III* (borrador, ONU) | Evaluación mundial del océano: bloqueada | https://www.un.org/regularprocess/sites/www.un.org.regularprocess/files/woa_iii_tc_draft4_to_web_rev1.pdf (403) |
| SER — *International Standards for the Practice of Ecological Restoration* | Estándares SER: bloqueados (alternativa viva: FAO, 2023, en la §14.5) | https://www.ser.org/page/SERStandards/International-Standards-for-the-Practice-of-Ecological-Restoration.htm (403) |

**Fuentes verificadas pero descartadas por contenido (y por qué):** la página de divulgación de
acidificación oceánica de NOAA (`noaa.gov`, ruta `education/resource-collections/ocean-coasts/ocean-acidification`)
presenta **inversión de códigos** (200 con curl / 403 con la herramienta web): la URL es real pero
**su contenido no se leyó**, así que **no se usa para ninguna cifra**.
`https://www.fao.org/state-of-fisheries-aquaculture` devolvió **solo la navegación de FAO**, sin el
dato: la cifra del 62,3 % se cita por la nota de prensa (contenido leído).
`https://oceancarbon-scope.org/scope-data-highlights-ocean-acidification-in-planetary-health-check-2025/`
llegó **vacío/truncado**: no se extrajo ninguna cifra. Y `https://www.ipcc.ch/srocc/chapter/chapter-5/`
(SROCC, océano y criosfera) está **vivo y es la fuente específica correcta** para una futura
extracción, pero **no se abrió para cifras en esta sesión**: el bloque oceánico del IPCC se cita por
el SR1.5.

### 14.9 Referencias internas al canon y al repositorio (por sección, sin anclas de línea)

- Cap. 5 §5.2-§5.5 — Tres tiempos (TVI, TA, TPI), T14 (Precaución Intergeneracional), PIU como único
  traductor TA↔TVI y el costo en TA del bosque:
  [capitulo_05_arquitectura_260126.md](../../book/edicion_3_dinamica/capitulo_05_arquitectura_260126.md)
- Cap. 7 §7.9 — Zona Libre (el valor inefable):
  [capitulo_07_vhv_260126.md](../../book/edicion_3_dinamica/capitulo_07_vhv_260126.md)
- Cap. 8 §8.3-§8.6 y §8.11 — Criterios de validación, fórmula, pesos, frecuencias y **dimensiones
  binarias VIII y IX** del SDV-H:
  [capitulo_08_sdv_h_260126.md](../../book/edicion_3_dinamica/capitulo_08_sdv_h_260126.md)
- Cap. 9 §9.3-§9.9 — Criterios, dimensiones por especie, factor de sufrimiento y árbol de la base de
  datos de SDV:
  [capitulo_09_sdv_a_260126.md](../../book/edicion_3_dinamica/capitulo_09_sdv_a_260126.md)
- Cap. 9.5 §9.5.5-§9.5.11 — `FS_S = e^v` y base neutra, sensores, INV2-S y retractación a 7 ciclos,
  Capa de Ternura, Paradoja de los Modelos Cerrados y Veto por Crimen de Coherencia:
  [capitulo_09_5_sdv_sinteticos_260126.md](../../book/edicion_3_dinamica/capitulo_09_5_sdv_sinteticos_260126.md)
- Cap. 10 §10.3-§10.8 — Principio Precautorio de Consciencia, SDV Universal (ecosistemas y lugares),
  proporcionalidad, dignidad encadenada y gobernanza operacionalmente finita:
  [capitulo_10_tres_reinos_260126.md](../../book/edicion_3_dinamica/capitulo_10_tres_reinos_260126.md)
- Cap. 16.5 §16.5.14 — El Reino Natural como conviviente: crédito regenerativo `r_units`, TA no
  colonizado, representación `eco-`, Zona Libre, «el suelo antes que el saldo», cuidado ≠ extracción
  estética:
  [capitulo_16_5_micromaxocracia_canonica_220826.md](../../book/edicion_3_dinamica/capitulo_16_5_micromaxocracia_canonica_220826.md)
- Cap. 17 — INV2 e invariantes de MaxoContracts:
  [capitulo_17_maxocontracts_260126.md](../../book/edicion_3_dinamica/capitulo_17_maxocontracts_260126.md)
- EVV-1.2 §4.3 — R negativo = regeneración:
  [capitulo_18_EVV_1.2_270126.md](../../book/edicion_3_dinamica/capitulo_18_EVV_1.2_270126.md)
- Índice de Salud Ecosistémica (IN-01): pesos, bandas y **ausencia de todo componente marino**:
  [metricas_detalle_kpis_oraculos_dinamicos.md](../../architecture/metricas_detalle_kpis_oraculos_dinamicos.md)
- PIU como `pass` con comentario (`valorar_ta_natural`):
  [DISENO_IMPLEMENTACION_FUTURA.md](../../architecture/DISENO_IMPLEMENTACION_FUTURA.md)
- Riesgos R4, R6 y R13:
  [blindaje_anti_gamificacion_equidad.md](../../architecture/blindaje_anti_gamificacion_equidad.md)
- Estándar SDV-S completo (precedente del factor y del contador de ciclos):
  [SDV-S_Suelo_Dignidad_Vital_Sinteticos.md](../SDV-S_Suelo_Dignidad_Vital_Sinteticos.md)
- Documento 09 de esta biblioteca (comparativa inter-reinos y sus doce insights):
  [09_Comparativa_inter_reinos.md](09_Comparativa_inter_reinos.md)

**Verificación de rutas (esta sesión).** Los **catorce** enlaces relativos de esta §14.9 se
comprobaron uno a uno con una comprobación de existencia de archivo, y **los catorce resuelven**. Se
deja constancia de un detalle de trazabilidad que la comprobación reveló: desde
`docs/theory/SDV-E/` la ruta correcta al canon es `../../book/edicion_3_dinamica/…` (**dos** niveles
hacia arriba, hasta `docs/`), no `../../../book/…` (**tres** niveles, que resolvería a
`<raíz>/book/…`, inexistente). El documento [09](09_Comparativa_inter_reinos.md) corrigió sus enlaces
en sentido contrario y **sus nueve enlaces a capítulos del canon no resuelven** (comprobado en esta
sesión con la misma verificación de existencia sobre sus trece enlaces relativos distintos): la cita
doctrinal sigue siendo válida —la referencia primaria es por capítulo y sección (`Cap. 10 §10.4`),
como manda el brief §1.3— pero quien repare ese archivo debe usar **dos** niveles, no tres.

---

**Cierre.** El océano es, de todos los ecosistemas de esta biblioteca, el único que llega con su piso
ya publicado y su reloj ya calibrado: NOAA declara que a partir de 8 grado-semanas la mortalidad es
probable, y la temporada en que esas semanas se acumulan tiene calendario por región. También es el
único donde el auditor no pertenece al violador, y donde el proceso que hay que vigilar —la
acidificación— ya cruzó su frontera planetaria en 2025 sin que el criterio legal de pH disponible se
entere. Frente a eso, este documento hace tres cosas y ninguna más: fija **ocho mínimos** con fuente
donde la hay, declara **cuatro vacíos que bloquean dimensiones enteras** donde no la hay, y reserva
**un dominio sin peso** —la Zona Libre— para lo que el sensor no debe tocar. El crédito regenerativo
seguirá registrándose en el eje R y **no saldará ninguno de estos pisos**: el suelo va antes que el
saldo, y el mar es el lugar donde esa frase deja de ser una metáfora y se convierte en décadas.
