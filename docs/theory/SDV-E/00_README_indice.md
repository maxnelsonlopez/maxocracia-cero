# Biblioteca de Referencia del SDV-E — Suelo de Dignidad Vital del Reino Natural

**Estado:** 🟡 **Propuesta de estándar. NO es canon hasta su ratificación.**
**Rama:** SDV-E, Ola 4 — abierta en octubre de 2026.
**Autoría:** oráculos sintéticos de la rama & Max Nelson López Restrepo.
**Licencia:** Creative Commons BY-SA 4.0.
**Nada de lo que describe esta biblioteca está implementado en el motor todavía** (ver §7).

---

## 1. Por qué existe esta biblioteca

El canon convocó el SDV-E y dejó escrito el hueco exacto que había que cerrar:

> *"**El suelo antes que el saldo**: el SDV-E —los mínimos del diseño biológico del ecosistema
> (Cap. 10 §10.4)— es la ramificación pendiente que este capítulo convoca, siguiendo el precedente
> del SDV-S (Cap. 9.5): **estándar primero, contabilidad después**. Un conjunto con crédito
> regenerativo acumulado pero humedal bajo su SDV-E no está en coherencia: **INV2-E será su juez**."*
> — Cap. 16.5 §16.5.14

Hoy ese juez **no existe**, y la consecuencia está viva en el código:

- El **crédito regenerativo** (`r_units` negativo) está **implementado y probado**
  (`app/micromax.py`, `tests/test_micromax.py`) — pero **no pesa en ninguna cuenta**: los únicos
  agregados del hogar suman el escalar (`SUM(calculated_vhv)`), no el vector.
- **`INV2-E` no existe** en `maxocontracts/`. El motor tiene INV1, INV2, INV2-S, INV2-EDU, INV3 e
  INV4 — y ninguno de ecosistemas.
- Una parte `eco-` recibe hoy **el SDV humano** al resolverse como participante, porque no hay
  `sdv_e_actual`.
- El **R del sistema general** (`app/vhv_calculator.py`) solo cuenta extracción: no tiene eje de
  regeneración.

Es decir: **se puede acumular crédito regenerativo mientras el ecosistema se degrada, y el sistema
no lo detecta.** Esta biblioteca es el estándar que hace falta para que ese juicio sea posible.
La contabilidad viene después.

---

## 2. Qué contiene

### Bloque A — Doctrina y formalización

| Documento | Qué fija |
|---|---|
| [01 — Doctrina del SDV-E](01_Doctrina_SDV-E.md) | Qué es un SDV del reino natural y qué no es. Los tres pasos epistémicos (dato objetivo / umbral por consenso / violación como dato). LEY frente a POLÍTICA. |
| [02 — Unidad y sujeto](02_Unidad_y_sujeto_del_SDV-E.md) | La pregunta anterior a toda cifra: **¿de qué hablamos** cuando decimos que un ecosistema está bajo su suelo? Criterios de persona natural, escala mínima, continuidad de identidad, qué pasa si el río se seca. |
| [03 — No colonización del TA](03_No_colonizacion_del_TA.md) | El Tiempo Absoluto no se coloniza, y **cómo se comprueba** que no lo hicimos. Hoy el canon afirma la regla sin prueba; este documento la vuelve auditable. |
| [04 — Zona Libre del Reino Natural](04_Zona_Libre_del_Reino_Natural.md) | Lo que **no** se mide: el estado en que el interior de una unidad ecológica queda fuera de la contabilidad sin quedar fuera del Derecho. |
| [05 — Representación, guardián y mandato](05_Representacion_guardian_y_mandato.md) | El estándar de la voz: quién puede afirmar, en nombre de la unidad, que el mínimo se respetó. Los 7 campos de identidad, el quórum, la disputa y los riesgos abiertos. |
| [06 — Medición y verificación (T13)](06_Medicion_y_verificacion_T13.md) | El elenco de sensores que el documento 09 declaró inexistente: teledetección, sensores in situ, bioindicadores, ciencia ciudadana y comunidad testigo. |
| [07 — Fórmula de violación y pesos](07_Formula_de_violacion_y_pesos.md) | La aritmética: déficit normalizado, tabla de pesos, factor de intensidad, duración en TA y bandas de interpretación. |
| [08 — INV2-E, el invariante](08_INV2-E_invariante.md) | La capa ejecutable: cómo el estándar se vuelve un contrato que se puede bloquear y auditar. Cierra el agujero del crédito regenerativo. |
| [09 — Comparativa inter-reinos](09_Comparativa_inter_reinos.md) | Los cuatro SDV —humanos, animales, ecosistemas, sintéticos— eje por eje, y las decisiones que el SDV-E no puede tomar solo. |

### Bloque B — Un estándar por tipo de ecosistema

| Documento | Unidad |
|---|---|
| [10 — Bosques](10_Ecosistemas_Bosques.md) | Superficie, estructura, composición, carbono, continuidad, régimen de fuego, fauna dependiente. |
| [11 — Humedales](11_Ecosistemas_Humedales.md) | Hidroperiodo, nivel freático, turba, carbono del depósito orgánico, aves acuáticas, biota indicadora. **Es el caso canónico del humedal del conjunto residencial (Cap. 16.5 §16.5.14).** |
| [12 — Ríos y cuencas](12_Ecosistemas_Rios_y_cuencas.md) | Caudal ecológico, oxígeno, temperatura, ribera, conectividad, fauna, régimen de alteración. El "río con SDV" del Cap. 10 §10.4. |
| [13 — Océanos y costas](13_Ecosistemas_Oceanos_y_costas.md) | Arrecife, columna de agua, pesquería, red de áreas protegidas, manglar y pradera marina. |
| [14 — Suelos vivos](14_Ecosistemas_Suelos_vivos.md) | Materia orgánica y carbono del suelo, biodiversidad edáfica, balance erosión/formación, compactación, sellado, salinidad. |
| [15 — Praderas y sabanas](15_Ecosistemas_Praderas_y_sabanas.md) | Cobertura herbácea, carbono, herbivoría, régimen de fuego, aves de pastizal, movilidad del paisaje. |
| [16 — Montañas y criosfera](16_Ecosistemas_Montanas_y_criosfera.md) | Balance de masa glaciar, permafrost, pisos altitudinales, comunidad criófila, regulación hídrica de cabecera. |
| [17 — Zonas áridas](17_Ecosistemas_Zonas_aridas.md) | Neutralidad de la degradación contra línea base propia, agua subterránea, costras biológicas, umbrales de irreversibilidad. |
| [18 — Agroecosistemas](18_Ecosistemas_Agroecosistemas.md) | La frontera humano-natural: suelo cultivado, polinizadores, diversidad cultivada, márgenes y barbechos. |

### Bloque C — Dimensiones transversales, SDV-A y procesos

🔴 **Pendientes de redacción.** El canon los exige y esta biblioteca todavía no los tiene:
las dimensiones transversales (biodiversidad, conectividad, ciclos naturales, agua y aire como
métricas de conjunto), el estándar hermano **SDV-A** (animales), el hueco doctrinal de flora, hongos
y microorganismos, y el bloque **Procesos** que el árbol del Cap. 9 §9.7 pide
(`Metodología_Creación`, `Protocolo_Actualización`, `Gobernanza_Validación`).

---

## 3. La espina dorsal: ocho dimensiones

Los pesos **fusionan** el Índice de Salud Ecosistémica que el repo ya tenía definido y sin
implementar (biodiversidad 30 %, agua 20 %, aire 20 %, suelo 15 %, especies clave 15 %) con las dos
dimensiones que el canon nombra y **el ISE omitía** (caudal ecológico y conectividad). Fijados en el
[documento 07](07_Formula_de_violacion_y_pesos.md):

| Dimensión | Peso (catálogo) | Peso con piso declarado | ¿Tiene umbral verificado? |
|---|---|---|---|
| Biodiversidad | 0,300 | 0,300 | 🟢 sí |
| Calidad del aire | 0,200 | 0,200 | 🟢 sí (OMS, 2021) |
| Calidad del agua | 0,180 | 0,180 | 🟡 parcial (solo el pH) |
| Salud del suelo | 0,150 | 0,150 | 🟢 sí |
| Especies clave | 0,150 | 0,150 | 🟢 sí |
| **Caudal ecológico** | 0,075 | 0,075 | 🟢 sí |
| **Conectividad** | 0,075 | 0,000 | 🔴 **no** |
| Oxígeno disuelto | 0,020 | 0,000 | 🟡 en disputa |
| **Total** | **1,000** | **Σ PESOS_PISO = 0,905** | |

**Léase con honestidad:** el piso del SDV-E se ejecuta hoy sobre el **90,5 % del peso**, y una
dimensión que el canon nombra explícitamente —la conectividad— **todavía no tiene umbral
verificado**. Eso no es un defecto del documento: es el resultado de negarse a inventar cifras.
Una dimensión sin fuente no pesa; se declara.

---

## 4. Reglas que esta biblioteca se impuso

1. **Ninguna URL sin verificar.** Todo enlace fue comprobado por HTTP real durante la redacción.
2. **Ninguna cifra sin organismo, año y enlace.** Si no hay fuente, se escribe
   `[SIN FUENTE VERIFICADA]` — y eso vale más que un número inventado.
3. **Tres niveles de evidencia:** `[VERIFICADO]` / `[REPORTADO]` / `[HIPÓTESIS]`.
4. **Mínimo Absoluto separado del Óptimo.** El motor del SDV-H confundió el óptimo del agua
   (50-100 L/día) con su mínimo (20 L/día, OMS). Aquí el piso es LEY y la plenitud es POLÍTICA.
5. **El canon se cita por sección** (Cap. 10 §10.4), nunca por número de línea.
6. **Lo que no se sabe se declara.** Cada documento cierra con preguntas abiertas.

---

## 5. Cómo se verifica esta biblioteca

Dos puertas deterministas, no opiniones:

```powershell
# 1. Auditoria estructural: plantilla, minimo/optimo, LEY/POLITICA, anclas, frases vetadas
.venv\Scripts\python.exe -m pytest tests/test_sdv_e_biblioteca.py -q

# 2. Estado HTTP real de cada fuente citada (regla M15: jamas URLs alucinadas)
.venv\Scripts\python.exe scripts\verificar_enlaces_sdv_e.py
```

El verificador de enlaces distingue cuatro estados —`OK`, `BLOQUEADA` (real pero rechaza bots),
`SIN_RESPUESTA` (red o límite de peticiones: **no prueba muerte**) y `MUERTA`— y **no falla** si una
URL muerta está declarada como fuente descartada. El canon exige esa honestidad: distinguir lo
verificado de lo que falló.

---

## 6. Qué decide esta biblioteca y qué no

**Decide** (propuesta, pendiente de ratificación): la unidad del sujeto, los umbrales por tipo de
ecosistema, la fórmula y sus pesos, el elenco de sensores, el estándar de la voz y la especificación
de INV2-E.

**No decide**, y lo dice: quién tiene autoridad sobre un territorio concreto (los riesgos R4, R6 y
R13 siguen abiertos), qué umbral tiene la conectividad, cómo se compone el quórum de una parte
`eco-`, ni qué pasa con la flora, los hongos y los microorganismos.

**Discrepancias internas declaradas** (no ocultas): el documento 07 y el documento 08 no coinciden
en la cifra de cobertura del piso (0,905 frente a 0,680). Está marcado como **cifra en disputa** en
ambos.

---

## 7. Estado de implementación

| Pieza | Estado |
|---|---|
| Biblioteca del estándar (esta) | 🟢 escrita · 🟡 sin ratificar |
| `SDV_E` en el motor (`maxocontracts/core/types.py`) | 🔴 no existe |
| `Participant.sdv_e_actual` / `is_natural` | 🔴 no existe |
| `INV2-E` (`maxocontracts/core/axioms.py`) | 🔴 no existe |
| Bloque validador ecológico (`maxocontracts/blocks/`) | 🔴 no existe |
| Identidad de la representación natural (7 campos) | 🔴 no existe tabla |
| Contabilidad del crédito regenerativo | 🔴 no pesa (`r_units` se registra y se devuelve) |
| Eje de regeneración en el R general | 🔴 no existe |
| Traducción TA↔TVI (PIU) | 🔴 `pass` sin implementar |
| ISE en código | 🔴 documento sin implementación |
| Fuentes de datos ecológicos | 🔴 ninguna integrada |
| Quórum N-de-M de la parte `eco-` | 🔴 no cableado (el libro afirma que sí) |
| Validación de `r_units` | 🔴 sin cota, sin finitud, sin evidencia exigida |

---

## 8. Cómo entra al canon

El índice del canon (`scripts/canon_index.py`) recorre `docs/theory` de forma recursiva, así que
esta biblioteca **ya entra al corpus que el Concilio absorbe en F1**. Los oráculos podrán razonar
sobre el SDV-E en el próximo ciclo.

Pero entrar al corpus **no es ser canon**. El camino es el que el propio canon fija: propuesta,
deliberación, auditoría axiomática y validador conceptual. Mientras tanto, esta biblioteca se declara
por lo que es: **el estándar primero, para que la contabilidad pueda venir después.**

---

*"El sistema no expulsa. Reintegra."* — pero la contabilidad nunca se borra (T13).
