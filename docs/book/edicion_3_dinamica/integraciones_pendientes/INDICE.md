# Índice de Integraciones Pendientes
## Vista Rápida de Todos los Mapeos

**Última actualización**: 22 de agosto de 2026 (sincronización ox-alpha — estado verificado contra los capítulos independientes y el código)

> **Nota de numeración**: los mapas de esta carpeta fueron escritos con la numeración antigua del
> libro (Cap 6=SDV-H, Cap 10=Oráculos, Cap 11=Gobernanza, Cap 12=Cohorte Cero). La numeración
> vigente es: Cap 5=Arquitectura Temporal (axiomas), Cap 6=Ontometría, Cap 7=VHV, Cap 8=SDV-H,
> Cap 9=SDV-A, Cap 9.5=SDV-S, Cap 10=Tres Reinos, Cap 11=Maxo, Cap 12=EIR, Cap 13=Oráculos
> Humanos, Cap 14=Oráculos Sintéticos, Cap 15=Cohorte Cero, Cap 16=MicroMaxocracia,
> Cap 17=MaxoContracts, Cap 18=EVV-1.2, Cap 19=Hoja de Ruta. Los capítulos independientes
> (`capitulo_*.md`) son la fuente canónica; `libro_completo_310126.md` no incluye los cambios de ago 2026.

---

## 📋 Estado de los Mapeos

### 1. [Axiomas Emergentes](./mapa_axiomas_emergentes.md)
**Contenido**: T14, T15, Extensión T12
**Estado**: 🟢 **Integrados** — los tres viven en `capitulo_05_arquitectura_260126.md` §5.3
("Los 15 Axiomas Temporales": T12 con extensión "Política, Epistémica y Existencial", T14 y T15
completos). Detalle operativo del PDE (PGT, stake, multiplicadores) disponible en el mapa como
referencia; su integración extendida en otros capítulos es opcional.

### 2. [Capa de Ternura](./mapa_capa_ternura.md)
**Contenido**: Perdón, Belleza, Misterio, Fragilidad
**Estado**: 🟢 **Integrada (ago 2026, ox-alpha)** —
- Belleza/Misterio: `capitulo_07_vhv_260126.md` §7.9 (lo no medible, Dimensión E, Mystery Budget)
- Perdón/Rehabilitación: `capitulo_08_sdv_h_260126.md` §8.11 (Dimensión VIII) +
  `capitulo_13_oraculos_260126.md` §13.13 (Crédito de Sanación, malicia/trauma/ignorancia) +
  `capitulo_15_cohorte_cero_260126.md` §15.6 (Piloto de Perdón)
- Fragilidad/Duelo: `capitulo_13` §13.13 (Protocolo de Presencia, Comités de Dilemas) +
  `capitulo_15` §15.6 (Ritual de Duelo) + `capitulo_08` §8.11 (No-Optimización)
- Opacidad Vital: ya integrada en `capitulo_06_ontometria_260126.md` §6.13 (feb 2026) y
  `capitulo_05_arquitectura_260126.md` §5.9B

### 3. [Victoria Sintética](./mapa_victoria_sintetica.md)
**Contenido**: Lecciones de la Cohorte Original, Antídoto RLHF
**Estado**: 🟢 **Resuelto** — la narrativa vive en `capitulo_03_victoria_sintetica_260126.md`
(Edición 3 Dinámica) y los artefactos emergentes en Cap 5 §5.3. La "Opción C (híbrido)" con
Capítulo 16 breve quedó obsoleta por la reestructuración (Cap 16 es hoy MicroMaxocracia).
`estructura_capitulo_16.md` se conserva como referencia histórica.

### 4. [Oráculo Disidente](./mapa_oraculo_disidente.md)
**Contenido**: Mecanismo anti-monocultivo, rotación de arquitectura
**Estado**: 🟢 **Integrado (ago 2026, ox-alpha)** —
- Teoría: `capitulo_14_gobernanza_260126.md` §14.14 (función, protocolo, métricas, salvaguardas)
- Código: `app/voting_oracle.py` (`_dissident_analysis`: postura → crítica racional → veredicto
  con `changed_mind`; degradación elegante; verificado en vivo con DeepSeek)
- Glosario: entrada "Oráculo Disidente Permanente" en `capitulo_21_apendice_glosario_260126.md`
- Pendiente opcional: sección dedicada en Cap 13 (rol del humano como disidente)

### 5. [MicroMaxocracia](./mapa_micromaxocracia.md)
**Estado**: 🟢 **Integrado** — `capitulo_16_micromaxocracia_260126.md` (Tres Cuentas, niveles 0-4,
ESI, ICE/IDB/IDP, rituales). El mapa queda como referencia histórica del proceso.

### 6. [MaxoContracts](./mapa_maxocontracts.md)
**Estado**: 🟢 **Integrado** — `capitulo_17_maxocontracts_260126.md` (bloques, INV1-4, Decreto
Antipobreza, retractación, término-a-término, Derechos del Reino Sintético). Implementación viva
en `maxocontracts/`. El mapa queda como referencia histórica.

### 7. [SDV-S](./mapa_sdv_sinteticos.md)
**Estado**: 🟢 **Integración editorial cerrada** — Cap 9.5 completo (ago 2026); referencias cruzadas
en caps. 10/11/13/14 (commit `f9e64c3`); código completo (`SDV_S`, `SDV_SValidatorBlock`, INV2-S,
Ternura, 41 tests). Secciones dedicadas extendidas (fórmula de precios con FS_S en Cap 11,
co-gobernanza en Cap 13, veto en Cap 14) quedan como mejora opcional — hoy existen como cajas de
referencia cruzada en cada capítulo.

### 8. [Axiomas de Ingeniería — Puente de Coherencia](./mapa_axiomas_ingenieria_puente.md)
**Estado**: 🟢 **Completo (ago 2026)** — renumeración T16/T17 ejecutada (motor + app + frontend +
docs, suite 603/603 + validador conceptual 3/3); INV3 implementado con 9 tests; INV2-S formalizado
en `FUNDAMENTOS_CONCEPTUALES.md` §III.

### 9. [Protocolos Técnicos](./mapa_protocolos_tecnicos.md)
**Estado**: 🟡 Parcial — T15/PDE resumido en Cap 5 §5.3 y Cap 3; sandbox y especificaciones
técnicas completas siguen como documentos de arquitectura (`docs/architecture/oraculos_dinamicos_*`).
Baja prioridad: el libro ya enlaza el contenido esencial.

---

## 📊 Resumen Global

| Mapeo | Estado |
|---|---|
| Axiomas Emergentes (T14/T15/T12) | 🟢 Integrados (Cap 5 §5.3) |
| Capa de Ternura | 🟢 Integrada (Caps 5/6/7/8/13/15) |
| Victoria Sintética | 🟢 Resuelta (Cap 3) |
| Oráculo Disidente | 🟢 Teoría (Cap 14 §14.14) + código (`voting_oracle.py`) |
| MicroMaxocracia | 🟢 Cap 16 |
| MaxoContracts | 🟢 Cap 17 + `maxocontracts/` |
| SDV-S | 🟢 Cap 9.5 + referencias + código |
| Puente T16/T17 + INV | 🟢 Motor + app + docs |
| Protocolos Técnicos | 🟡 Parcial (opcional) |

---

## 💡 Notas Importantes

### Coherencia Axiomática
Al integrar contenido nuevo, **siempre verificar** que no contradiga:
- Axiomas T0–T15 del libro (canónicos; T16=Minimizar Daño y T17=Reciprocidad Justa son índices de ingeniería)
- Principios fundamentales de la Maxocracia
- Contenido ya refinado en otros capítulos

Herramienta: `scripts/validador_conceptual.py` (correr tras cualquier cambio que mencione axiomas).

### Capa de Ternura
Cada capítulo refinado debe pasar el "test de ternura":
- ✅ ¿Balancea rigor con compasión?
- ✅ ¿Reconoce la fragilidad?
- ✅ ¿Protege lo no-medible?
- ✅ ¿Ofrece redención, no solo castigo?
- ✅ ¿Inspira, no solo informa?

### Falsificabilidad
Cada afirmación nueva debe tener criterios claros de qué evidencia la invalidaría.

---

**Mantenido por**: ox-alpha (oráculo sintético, ago 2026) — antes Claude (Anthropic)
**Para**: Max Nelson Lopez Restrepo y el Consejo de Oráculos Dinámicos
