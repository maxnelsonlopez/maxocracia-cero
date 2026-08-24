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
  ahora lo decimos con la notación común. Un hogar en rojo no implementa el ledger: primero sana.

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
| ESI / Protocolo de Desintoxicación | INV1 + retractación ética + Ternura | Umbral γ<1; perdón protocolizado |
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
| Campos opcionales de vector (v/r) en `log_cdd` + `ceh_mode` en config | 🔴 pendiente |
| Check-ins de γ domésticos (endpoint + UI) | 🔴 pendiente |
| Renombrar pesos en salida del dashboard (con alias retrocompatible) | 🔴 pendiente |
| Plantillas de contratos domésticos en el builder | 🔴 pendiente (plantillas Cohorte ya existen) |

**Próxima acción**: implementar los campos opcionales y el `ceh_mode` (una jornada pequeña), dejando
los check-ins de γ domésticos para la Ola siguiente.

---

> **📖 Conexiones:** Cap. 7 §7.5 (hecho/valor) · Cap. 11 §11.6 (notación axiomática) · Cap. 13 §13.13
> (perdón y presencia) · Cap. 15 §15.6 (Zona Libre) · Cap. 17 §17.1/§17.7 (bloques y plantillas).
