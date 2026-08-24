# Capítulo 16.5
# MicroMaxocracia Canónica: la rama doméstica en unidades del sistema

> **Nota editorial:** Creada en agosto de 2026 en colaboración con ox-alpha, siguiendo el precedente
> del Cap. 9.5 (SDV-S): una ramificación que no reemplaza al Cap. 16 sino que lo **ancla al canon**,
> resolviendo las fricciones de unidades, notación y procesos detectadas al contrastarlo con la
> implementación (`app/micromax_bp.py`) y con los axiomas generales.

## 16.5.1 El problema de coherencia: tres fricciones verificables

La MicroMaxocracia (Cap. 16) fue diseñada como puerta de entrada: deliberadamente simple, operativa
con papel y lápiz. Pero contrastada con el sistema general emergen tres fricciones que un hogar
maxocrático maduro no debería heredar:

| # | Fricción | Evidencia | Axioma tensionado |
|---|---|---|---|
| 1 | **El hecho nace contado con la valoración**: el "VHV doméstico" es un escalar (`tiempo × esfuerzo × carga mental × alcance`), no el vector `[T, V, R]` | Fórmula Cap. 16 §16.2; campo único en `log_cdd` | Separación Hecho/Valor (Cap. 7 §7.5) y T13 |
| 2 | **CEH vive en dinero fiduciario**: la segunda cuenta mide "% de ingresos aportados" | Cap. 16 §16.3; `monthly_income` en la configuración del miembro | La premisa fundacional: reemplazar la contabilidad fiduciaria (Cap. 5 §5.1) |
| 3 | **Colisión de notación**: los pesos del equilibrio se llaman α=0.6, β=0.3, γ=0.1 — pero γ ya es el exponente axiomático de aversión al sufrimiento (γ≥1) y α/β/δ los pesos del precio | Glosario: dos definiciones de γ conviven hoy | T13 (transparencia: un símbolo, un significado) |

Hay una cuarta brecha, más silenciosa: el hogar no participa de los órganos vitales del sistema —
sin check-ins de γ, sin INV1 protector, sin opción de codificar sus acuerdos. Esta ramificación
cierra las cuatro.

## 16.5.2 Principio rector

> **El hogar no es un sistema paralelo con vocabulario prestado: es el fractal más pequeño del
> sistema completo.**

La regla es la misma que rige desde la célula (Cap. 1): cada nivel hereda y amplía la ética del
nivel inferior, nunca la sustituye. Por eso esta ramificación **no cambia cómo se vive el hogar**;
cambia en qué unidades se cuenta lo vivido, para que un hogar de Bogotá y una cohorte planetaria
puedan leerse en el mismo idioma contable.

## 16.5.3 Unidad única: el VHV vectorial doméstico

Se restituye la separación hecho/valor (Cap. 7 §7.5) dentro del hogar:

### Capa 1 — El hecho (vector objetivo)

Cada tarea doméstica se registra como vector:

$$VHV_{hogar} = [T, V, R]$$

- **T**: duración objetiva en horas (`duration_hours`), partida doble incluida (T_directo; el
  T_heredado de electrodomésticos e infraestructura es opcional en resolución baja, Cap. 7 §7.3).
- **V**: vidas afectadas cuando aplique (cuidado de niños, enfermos, animales — UCV ponderada,
  Caps. 9/9.5). En tareas sin terceros sintientes, V = 0.
- **R**: recursos del hogar consumidos (agua, energía, insumos). Estimación honesta a lápiz es válida.

### Capa 2 — La valoración (coeficientes consensuados)

Los multiplicadores del diseño original **no desaparecen: cambian de capa**. Esfuerzo, carga mental,
alcance y los factores FIC (atención, fragmentación, soledad) pasan a ser **coeficientes de
valoración social explícitos**, negociados por el hogar (exactamente como dictaba la Capa 2 original):

$$VHV^{ponderado}_{hogar} = T \times (w_e \cdot E) \times (w_m \cdot M) \times (w_a \cdot A)$$

La métrica ponderada existe **para el cálculo del equilibrio**, jamás para reemplazar al vector:
el dato queda limpio para siempre (INV3 aplicado al hogar: ningún VHV ocultable ni pre-mezclado).

## 16.5.4 La conversión del dinero: CEH canónico = TVI vendido

La segunda cuenta se libra del fiduciario con una traducción directa:

$$CEH_{TVI} = \frac{\text{ingresos aportados al fondo común}}{\text{tarifa horaria vital del miembro}}$$

Es decir: **las horas de vida que cada miembro vendió al mercado para sostener al hogar**.
Todas las cuentas quedan así en la misma unidad — horas de vida — y el equilibrio se vuelve
comparable entre miembros (T2: igualdad temporal fundamental hecha aritmética).

| Modo | CEH se calcula | Cuándo usarlo |
|---|---|---|
| **Puente** (transicional) | % de ingresos aportados (como Cap. 16) | Niveles 0–1; hogares que aún no conocen su tarifa horaria |
| **Canónico** (destino) | TVI vendido (fórmula arriba) | Nivel 2+ en adelante; requisito para acuerdos como MaxoContracts |

La tarifa horaria vital se declara por miembro y se revisa en la auditoría anual — es una declaración
honesta, no un dato fiscal: quien dona trabajo no remunerado al hogar declara tarifa 0 y su CEH_TVI
es cero por elección, no por pobreza.

## 16.5.5 Notación liberada: adiós a la colisión

Los pesos del equilibrio se renombran para dejar α, β, γ, δ exclusivamente a los axiomas del precio
(Cap. 11 §11.6):

| Antes (Cap. 16) | Ahora (rama canónica) | Significado |
|---|---|---|
| α = 0.6 | **p₁** | peso de contribución doméstica directa |
| β = 0.3 | **p₂** | peso de contribución económica (en TVI vendido) |
| γ = 0.1 | **p₃** | peso de tiempo de energía disponible |

Regla de estilo general que este capítulo instituye: **un símbolo griego, un solo significado en
todo el corpus** (T13). Los pesos domésticos usan consonantes latinas minúsculas con subíndice.

## 16.5.6 γ doméstico e INV1: el hogar que escucha la vida

El patrón del Puente A (γ que escucha la vida) llega al fractal doméstico:

- **Check-in de bienestar por miembro** (ritual semanal ya existente, ahora con registro): cada
  integrante reporta su γ con fuente. Las **caídas se escuchan siempre**; las mejoras siguen la
  ventana acordada (semántica idéntica a `MAXO_CHECKIN_WINDOW_DAYS`).
- **INV1-Hogar**: si el γ de cualquier miembro cae bajo 1.0 sostenido, se activa el **Protocolo de
  Desintoxicación** del Cap. 16 §16.5 — que queda así reconocido como la forma doméstica de la
  retractación ética: el sistema sirve a las personas, no al revés.
- **ESI rojo ≡ γ<1 estructural**: la Escala de Seguridad era intuitivamente el mismo umbral;
  ahora lo decimos con la notación común. Y bajo INV1-Hogar, el rojo no cierra nada: activa el
  **Modo Escudo Doméstico** — *el registro propio nunca se bloquea* (Derecho al Registro
  Protegido); lo que se oculta a los demás convivientes son las cifras de quien está protegida.
  La protección que silencia no es protección: es la violación con otra cara.

## 16.5.7 Acuerdos domésticos como MaxoContracts ligeros (opcional, Nivel 3+)

Cuando el hogar quiera blindar un acuerdo recurrente, no inventa nada: usa los Legos Éticos
(Cap. 17 §17.1) con plantillas ya probadas en la Cohorte (§17.7: aseo compartido, préstamo sin
usura, comida grupal):

- **ReciprocityBlock** (T17): balancea el VHV ponderado entre miembros — la asimetría >70% exige
  reconocimiento explícito antes de activar, igual que en cualquier contrato.
- **WellnessProtectorBlock** (T16): monitorea los check-ins de γ domésticos.
- **Retractación ética**: desintoxicación con Ternura — el perdón modula la consecuencia, nunca
  borra la contabilidad (Cap. 13 §13.13).

El contrato doméstico es **opcional y reversible**: muchos hogares vivirán felices en Nivel 2 toda
la vida. El código no debe ser una cárcel tampoco en la cocina (INV4).

## 16.5.8 Trazabilidad doméstica: transparencia hacia adentro, opacidad hacia afuera

Aquí la rama canónica precisa algo que el sistema general aún no había declarado:

> **El hogar es la unidad básica de la Opacidad Sagrada.**

- **Hacia adentro**: todo registro es auditable por los miembros (T13 intra-hogar) — ledgers,
  auditorías mensuales, historial de γ, procedencia de cada acuerdo.
- **Hacia afuera**: los datos del hogar son Tiempo Opaco colectivo (Cap. 5 §5.9B; Cap. 7 §7.9).
  Solo salen del hogar agregados, anonimizados y voluntarios (los datos que alimentan políticas
  públicas, Cap. 16 §16.7).

La transparencia radical no escala hacia el interior de la vida privada: escala hacia la verdad
compartida de quienes comparten el techo.

## 16.5.9 Correspondencia completa de procesos

| Proceso doméstico (Cap. 16) | Análogo en el sistema general | Cambio canónico |
|---|---|---|
| Ledger de tareas | VHV de intercambios (`forms/exchange`) | Vector [T,V,R] + coeficientes en Capa 2 |
| Check-in semanal | Check-ins de γ (`/contracts/<id>/checkin`, Puente A) | Registro con fuente; política asimétrica |
| Auditoría mensual | Auditoría de coherencia + stats | Acta con procedencia (T13) |
| ESI / Protocolo de Desintoxicación | INV1 + retractación ética + Ternura | Umbral γ<1; **Modo Escudo** (registro propio jamás bloqueado, cifras ocultas a los demás); perdón protocolizado |
| Niveles 0–4 | Resolución variable del VHV (Cap. 7 §7.3) | Sin cambios; modo puente→canónico en Nivel 2+ |
| Trabajo emocional no-indexable | Zona Libre de VHV (15 §15.6) + Dimensión E (7 §7.9) | Reforzado: la rama canónica no coloniza lo opaco |

## 16.5.10 Compatibilidad retroactiva

Ningún hogar existente queda invalidado:

1. El escalar histórico del CDD se reinterpreta como `VHV^ponderado` (siempre lo fue); el vector se
   registra de ahora en adelante junto a él.
2. El modo puente de CEH sigue siendo válido indefinidamente para quien lo prefiera — la canonicidad
   es destino, no requisito de entrada.
3. Los pesos p₁/p₂/p₃ conservan los valores típicos 0.6/0.3/0.1 del diseño original; solo cambia el
   símbolo, no el acuerdo.

## 16.5.11 Estado de implementación y próxima acción

| Componente | Estado |
|---|---|
| Hub doméstico (`app/micromax_bp.py`: household, cdd, safety-survey, audits, dashboard) | 🟢 vivo |
| Este capítulo (estándar teórico) | 🟢 creado (ago 2026) |
| **Modo Escudo Doméstico** — registro propio nunca bloqueado + cifras ocultas a los demás + vista discreta con datos reales privados | 🟢 implementado (ago 2026, hallazgo de campo de Max) |
| `wants_support` opt-in privado almacenado con la ESI (no altera puntaje, jamás visible al hogar) | 🟢 implementado (ago 2026) |
| **Vector [T,V,R] opcional en cada tarea** (`v_ucv`, `r_units`, `r_notes`) — hecho limpio comparable con el sistema general, escalar ponderado intacto | 🟢 implementado (ago 2026) |
| **CEH canónica por TVI vendido** (`ceh_mode` + `hourly_rate`; unidad homogénea solo cuando todo el hogar adopta, fallback fiat con `ceh_unit` explícito) | 🟢 implementado (ago 2026) |
| Pesos p₁/p₂/p₃ expuestos en la salida del dashboard | 🟢 implementado (ago 2026) |
| **Crédito regenerativo** — `r_units` negativo en CDD (EVV §4.3): cuidado del Reino Natural que devuelve más de lo toma | 🟢 implementado (ago 2026, §16.5.14) |
| **Check-ins de γ domésticos** — latido del hogar con INV1-Hogar; el angusto de un protegido jamás cruza la pantalla ajena | 🟢 implementado (ago 2026) |
| UI de los nuevos campos (vector, modo CEH, check-in γ en formularios) | 🔴 pendiente |
| Plantillas de contratos domésticos en el builder | 🔴 pendiente (plantillas Cohorte ya existen) |
| **Puente Red de Apoyo v1** (`/support/offers`): ofertas de cuidado afinadas por señal ESI, solo con opt-in; las respuestas jamás viajan | 🟢 implementado (ago 2026) |
| Puente Red de Apoyo v2 — publicación de ofertas de cuidado por la comunidad + circuito completo con facilitación humana | 🔴 próxima ola |
| **SDV-E** — Suelo de Dignidad Vital para Ecosistemas + INV2-E (convocado por §16.5.14) | 🔴 próxima gran ramificación |

**Próxima acción**: check-ins de γ domésticos y la primera escala vecinal real
(un piso compartido o conjunto residencial operando el §16.5.13).

## 16.5.12 La ESI como señal de necesidad: el puente hacia la Red de Apoyo

Las seis preguntas de la Escala de Seguridad no son solo un filtro de entrada: son un **mapa de
necesidades**. Cada "sí" describe algo concreto que la persona necesita y probablemente no puede
obtener dentro de su hogar:

| Señal ESI | Necesidad que describe | Apoyo que la comunidad puede ofrecer |
|---|---|---|
| Miedo a expresar desacuerdo | Voz protegida, acompañamiento | Acompañamiento emocional, escucha entrenada |
| Dinero controlado coercitivamente | Independencia económica | Asesoría financiera, rutas de empleo, recursos |
| Amenazas al cuestionar tareas | Seguridad jurídica | Asesoría legal, rutas de denuncia seguras |
| Represalias si documenta su carga | Confidencialidad y respaldo | Testigos comunitarios, registro protegido |
| Descalificación constante | Reconocimiento | Validación por pares, círculos de apoyo |
| Miedo a ser honesta sobre cómo se siente | Espacio seguro de palabra | Grupos de apoyo, terapia subsidiada |

### Principios del puente (no negociables)

1. **Consentimiento explícito y granular** (`wants_support`, opt-in voluntario y revocable): la señal
   viaja hacia afuera *solo si* la persona lo decide. Nunca automáticamente.
2. **Nunca hacia el hogar**: el opt-in es invisible al conviviente. El sistema jamás notifica,
   sugiere ni filtra nada que revele quién respondió qué dentro del hogar.
3. **Identidad protegida**: el match se realiza sin exponer el hogar ni la relación — la víctima
   reclama ofertas de cuidado desde su perfil de protección (`/protection`), no desde su domicilio.
4. **Ofertas antes que búsquedas**: la comunidad publica *ofertas de apoyo* (asesoría legal,
   acompañamiento, recursos) en el muro común; quien está protegida reclama sin declarar necesidad
   pública alguna. La necesidad sensible nunca se publica; la abundancia de la red sí.

### Estado

La bandera privada y el **puente v1** existen (ago 2026): con opt-in activo, `GET /support/offers`
devuelve las ofertas de cuidado de la comunidad ordenadas por afinidad con las señales ESI — sin
que las respuestas viajen jamás. Pendiente para la ola siguiente: que la comunidad publique sus
primeras ofertas de cuidado (asesoría legal, acompañamiento, terapia subsidiada) y probar el
circuito completo con facilitación humana. Protocolo de validación humana: la *Semana de la
Verdad* (`docs/guides/semana_de_la_verdad.md`).

## 16.5.13 Más allá del parentesco: roommates y conjuntos residenciales

Nada en la arquitectura exige que un "hogar" sea una familia. El esquema (`micromax_households`
con códigos de invitación) define **unidades de convivencia**: personas que comparten techo,
gastos y trabajo de sostenimiento. Eso abre dos escalas inmediatas que la contabilidad canónica
(§16.5.3–16.5.4) hace posibles por primera vez:

### Piso compartido (roommates)

El caso más simple: tres personas comparten apartamento. CDD = limpieza, cocina, compras,
gestión del arriendo. Las Tres Cuentas funcionan sin cambios — y con la CEH canónica resuelven
la pelea clásica: *"yo pago más arriendo"* vs *"yo hago más tareas"* deja de ser un duelo de
narrativas y se vuelve aritmética visible en horas de vida vendidas y horas de vida cuidada.
Los acuerdos recurrentes pueden subir a MaxoContracts ligeros (§16.5.7) con las plantillas de
la Cohorte (aseo compartido, comida grupal — Cap. 17 §17.7).

### Conjunto residencial (escala vecinal)

Un edificio o conjunto es una **unidad de convivencia colectiva**: zonas comunes, administración,
portería, jardines. La rama doméstica escala a él con un puente que ya existe en el sistema general:
las **partes de cualquier escala** (`maxo_parties`, Cap. 10) — un conjunto residencial es
literalmente una parte tipo `coop-` o `society-`.

- **Nivel vecinal**: el conjunto opera un "hogar" propio donde el CDD registra mantenimiento de
  zonas comunes, gestión administrativa y cuidado de áreas verdes — con el mismo vector `[T,V,R]`.
- **Contratos interescala**: servicios entre el conjunto y proveedores (jardinería, aseo) como
  MaxoContracts con partes colectivas y quórum delegado N-de-M (Cap. 17).
- **La condición de posibilidad**: que un roommate y un conjunto hablen el idioma del sistema
  requiere unidades compatibles — exactamente lo que este capítulo implementa. Sin vector ni
  TVI vendido, cada escala inventaría su propia moneda; con ellas, el trabajo invisible de un
  edificio y el de una cocina quedan legibles en el mismo libro mayor.

### Principio de escala

> La MicroMaxocracia Canónica aplica a toda unidad de convivencia que comparta sostenimiento:
> núcleo familiar, piso compartido, casa comunitaria o conjunto residencial. El parentesco no es
> criterio de entrada; la convivencia lo es.

## 16.5.14 El hogar extendido: el Reino Natural como conviviente

Toda unidad de convivencia humana habita *dentro* de un ecosistema: el conjunto residencial junto
al humedal, el piso bajo las arboladas, la casa comunitaria sobre la cuenca. Si la convivencia es
compartir sostenimiento (§16.5.13), esa relación es bidireccional — y los Tres Reinos (Cap. 10)
dejan de ser una ontología lejana para sentarse a la mesa del hogar:

### Convivencia bidireccional

- **El humano sostiene al territorio**: jornadas de reforestación, cuidado de zonas verdes,
  limpieza del humedal urbano. Se registra como CDD vecinal con vector `[T, V, R]` donde
  **R negativo = crédito regenerativo** (EVV-1.2 §4.3): devolver más de lo que se toma.
  Implementado (ago 2026).
- **El territorio sostiene al humano**: agua, sombra, aire, regulación climática. Su tiempo es
  **Tiempo Absoluto (TA)** — aquí manda el límite honesto: *la contabilidad doméstica no coloniza
  el tiempo ajeno*. El PIU (Cap. 5 §5.5) es quien traduce entre TA y TVI; nosotros registramos
  la interacción, no la vida interna del ecosistema.

### Representación: los representantes de ecosistemas ya tienen asiento

La infraestructura existe: las partes `eco-` de MaxoContracts cuentan con **guardián oráculo**
para el Reino Natural, consentimiento agregado por quórum delegado N-de-M y contratos interescala
(Cap. 10/17). En la escala vecinal esto significa algo concreto: ningún acuerdo del conjunto que
afecte su humedal o su arbolada es legítimo sin el consenso de su parte `eco-` — el guardián
consiente por quienes no firman con manos.

### Salvaguardas específicas del Reino Natural

1. **Zona Libre también para él**: parte del valor del humedal es inefable (Cap. 7 §7.9). Los
   sensores miden salud (agua, cobertura, biodiversidad indicadora); jamás "milagros". Medir todo
   sería la forma técnica de dejar de escucharlo.
2. **El suelo antes que el saldo**: el SDV-E —los mínimos del diseño biológico del ecosistema
   (Cap. 10 §10.4)— es la ramificación pendiente que este capítulo convoca, siguiendo el precedente
   del SDV-S (Cap. 9.5): estándar primero, contabilidad después. Un conjunto con crédito
   regenerativo acumulado pero humedal bajo su SDV-E no está en coherencia: INV2-E será su juez.
3. **Cuidado ≠ extracción estética**: jardín podado para la foto no es cuidado; se registra lo
   que regenera, no lo que adorna.

---

> **📖 Conexiones:** Cap. 5 §5.5 (PIU, traducción TA↔TVI) · Cap. 7 §7.5 (hecho/valor) · Cap. 7 §7.9
> (Zona Libre) · Cap. 8 §8.11 (Derecho al Registro Protegido) · Cap. 10 (Tres Reinos, eco-partes,
> SDV-E por desarrollar) · Cap. 13 §13.13 (perdón y presencia) · Cap. 15 §15.6 (Zona Libre de VHV) ·
> Cap. 17 §17.1/§17.7 (bloques, plantillas, partes de cualquier escala) · Cap. 18 §4.3
> (R negativo = regeneración).
