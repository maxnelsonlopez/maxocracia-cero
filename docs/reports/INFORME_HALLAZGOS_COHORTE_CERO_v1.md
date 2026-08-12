# Informe de Hallazgos v1.0 — Cohorte Cero

**Fecha:** 12 de agosto de 2026
**Versión:** 1.0 (primer corte de datos reales)
**Base de datos:** `comun.db` — 50 contratos de la Cohorte Cero (20 aseo, 15 préstamo, 15 comida) + 6 demo/oráculo
**Método:** análisis determinista (SQL sobre `comun.db`, verificado por el director) + marco teórico
(RLM sobre Caps. 17, 15 y 12 del libro). Patrón: RLM navega + director verifica + teoría decide.

---

## 1. Resumen ejecutivo

La Cohorte Cero sembró 50 contratos éticos activos con 294 check-ins y 40 registros NPS. El sistema
funciona de punta a punta: creación, firma, activación, check-ins y métricas de dashboard. Los
hallazgos clave:

| Métrica | Valor | Lectura |
|---|---|---|
| γ promedio (cohorte) | **1.1223** | Saludable (INV1 exige ≥1.0) |
| Violaciones INV1 (γ<1) | **3** | Contratos `-10` de cada categoría (γ 0.95) |
| Retractaciones | **0** | Cobertura del ciclo de vida incompleta |
| Check-ins | **294** (5.88/contrato, 98% cobertura) | Ritual de bienestar activo |
| NPS | **8.80/10** (23 promoters, 0 detractors) | Satisfacción alta (métrica complementaria) |
| VHV movilizado | **115.0 h** de tiempo vital | T solo; V y R en 0 (ver §6) |
| Sustento del oráculo (ledger) | **0 registros** | El oráculo nunca trabajó en la cohorte |
| Gobernanza | 4 propuestas abiertas, **0 votos** | La comunidad aún no vota |

## 2. Metodología

- **Fase de observación (Cap. 15)**: los contratos se crearon con plantilla determinista T17
  (reciprocidad igualitaria), ambas partes firman, y se activan tras el ciclo de firma.
- **Cuantificación**: γ por participante (check-ins), VHV por términos, NPS, cobertura de check-ins.
- **Determinismo**: todos los números salen de queries SQL directas sobre `comun.db`; ningún valor
  estimado. El marco de umbrales teóricos proviene de los Caps. 17.2/17.5/15 (INV1, retractación,
  TCN, resolución de conflictos).

## 3. Población y cobertura

- 50 contratos cohorte: **20 aseo, 15 préstamo, 15 comida** — todos `active`.
- 28 participantes humanos únicos involucrados (127 filas de participación).
- 6 contratos adicionales fuera de cohorte (demos de escalas, oráculo de prueba, SDV-S).
- 2 contract_ids huérfanos en `maxo_contract_participants` (`demo-sdv-s-001`, un `oracle-...`) que
  no existen en `maxo_contracts` — residuo de demos, pendiente de limpieza.

## 4. Bienestar (γ) y SDV

- **γ cohorte: avg 1.1223** (min 0.95, max 1.16); histograma: 83/100 registros >1.1, 14 en 1.05-1.1,
  3 bajo 1.0. El γ se mantiene sano pero con poca variación (semilla homogénea).
- **3 violaciones INV1** (γ<1.0): `cohorte-aseo-10`, `cohorte-comida-10`, `cohorte-prestamo-10` —
  un registro por contrato con γ 0.95. No activaron retractación ni alerta (ver §5).
- **SDV**: 2 participantes con `sdv_status != 'ok'` (ambos sintéticos de demos, SDV-S con estado JSON)
  — sin violaciones humanas SDV-H.

## 5. Ciclo de vida y retractaciones — el hallazgo más importante

**Retractaciones: 0.** Ningún contrato usó `state=retracted` ni el evento `retract`. La teoría
(Cap. 17.5) define la retractación como *"una salvaguarda axiomática, no un fracaso"*: causa válida
es γ < 1.0 sostenido >14 días, y γ < 0.8 activa protección de buena fe (primera retractación sin
costo; luego 0.5/2 Maxos y revisión comunitaria en la 4ª). **El ciclo de salida/retirada nunca se
ejercitó**: la Cohorte cubre nacer, vivir y medir, pero no el camino de salida. La próxima cohorte
(o un ejercicio de simulación) debe ejecutar al menos 2-3 retractaciones para verificar INV4 y el
registro público T13 en producción.

## 6. Cumplimiento y reciprocidad

- **Check-ins: 294** (5.88/contrato; 49/50 contratos, falta `cohorte-aseo-01`).
- **Intercambios (tabla `interchange`): 0** y **términos cumplidos: 0** — la semilla registró
  check-ins pero nunca completó el ciclo de cumplimiento (term_fulfillment → reciprocidad real).
  El eje VHV R (recursos) está en 0 en los términos de la cohorte; solo el tiempo (T=115 h) circula.
- Lectura: la reciprocidad está *declarada* en los términos, pero no *ejecutada* en el registro.
  La siguiente cohorte debe registrar cumplimientos e intercambios reales.

## 7. VHV movilizado

- Cohorte: **T = 115.0 h** (aseo 40 + préstamo 30 + comida 45), V = 0, R/H = 0.
- Todos los contratos: T = 147.6 h, V = 3.0, R/H = 2.2 (demos aportan los ejes no temporales).
- La contabilidad de la vida en la cohorte es, por ahora, contabilidad del tiempo. Los ejes V y R
  requieren contratos que toquen vidas (cuidado) y recursos (materiales) — naturales en la
  MicroMaxocracia doméstica.

## 8. Satisfacción (NPS — métrica complementaria)

40 registros: **promedio 8.80** (mín 7, máx 10), 23 promoters, 17 passives, 0 detractors. Uniforme
por categoría (aseo 8.75, préstamo 8.83, comida 8.83). La teoría no define NPS (el RLM lo confirmó);
se reporta como señal complementaria de salud, no como criterio canónico.

## 9. Gobernanza y oráculo

- **Oráculo: 0 registros en `maxo_oracle_ledger`** — ningún contrato de la cohorte usó el oráculo en
  vivo (los 2 contratos `oracle-*` son demos en draft). El Derecho al Mantenimiento Óptimo (Cap. 17.4)
  no recibió sustento: el motor trabajó gratis en esta cohorte.
- **Gobernanza incipiente**: 4 propuestas `open` (operational), 0 votos, 0 delegaciones. El Parlamento
  y la votación están construidos y migrados (la BD vieja no tenía las tablas; `create_app` las creó)
  pero la comunidad aún no delibera.
- **Guía**: 1 evaluación de confianza registrada (kind `trust`, motor `deepseek`) — el Guía ya
  acompañó a su primer miembro.

## 10. Calidad de datos

- 6 contratos sin meta de categoría (demos) — correcto, fuera de cohorte.
- 1 contrato cohorte sin check-ins (`cohorte-aseo-01`).
- 2 ids huérfanos en participantes (demos).
- 3 registros γ<1 sin alerta ni retractación (ver §5).

## 11. Lecciones y recomendaciones para la siguiente cohorte

1. **Ejercitar el ciclo completo**: retractaciones (INV4 + registro T13), cumplimientos de términos
   e intercambios — la Cohorte actual cubre nacer y medir, no salir ni devolver.
2. **Usar el oráculo en vivo** en los contratos: activa el sustento del motor (Cap. 17.4) y enriquece
   la redacción civil; la cohorte sembrada no lo usó.
3. **Diversificar el γ**: los check-ins son uniformes; conviene un patrón de caídas/recuperaciones
   para ejercitar el WellnessProtectorBlock y las alertas INV1 (γ<1.0 >14 días).
4. **Activar la gobernanza**: votar las 4 propuestas abiertas, ejercitar el parlamento y la delegación;
   el quórum se mide sobre usuarios totales (hoy 12 semilla + demos).
5. **Métricas teóricas pendientes**: TCN (>80% de necesidades críticas resueltas internamente,
   Cap. 15), velocidad de circulación del Maxo, e índice de resolución de conflictos (100%).
6. **Limpieza**: retirar los 2 ids huérfanos de demos y decidir el destino de los 6 contratos no-cohorte.

---

**Próximo hito**: análisis de la cohorte humana real (90 días) y generación del Informe v2.0 con
retractaciones, cumplimientos e intercambios reales. Kit open-source pendiente de publicación.

**Método completo**: análisis determinista (SQL) + RLM (Caps. 17/15/12) + verificación del director.
