# Informe del Reino Sintético — teoría del libro vs. implementación

**Fecha:** 12 de agosto de 2026
**Estado:** VIVO — insumo para el hito SDV-S editorial (integración cruzada Caps. 10/11/13/14) y para futuras
olas del Reino Sintético.
**Método:** Patrón Puente — el arnés RLM de `local_models` analizó el **libro completo** (307 KB,
`docs/book/edicion_3_dinamica/libro_completo_310126.md`) con una sola pasada `map` (20/20 fragmentos,
chunk_size 5000); el director de sesión verificó cada afirmación con greps/lecturas deterministas sobre
el código. Primera vez que el RLM barre el libro entero sin bucle (lecciones del hallazgo 6 del
mapa de coherencia: `map` con chunk_size alto + guard de repetición).

**Estadísticas del arnés:** 11 iteraciones raíz, 20 subconsultas, 1 llamada `map` (20/20 chunks),
~128.8k tokens estimados de entrada, 0 errores de parseo, 0 avisos de repetición.

---

## 1. Naturaleza y Victoria Sintética (Cap. 3)

La Maxocracia reconoce al Reino Sintético como uno de los **Tres Reinos de la Existencia** (junto al
Natural y el Humano): desde "Objetos Simples" (herramientas) hasta "Consciencias Emergentes" (IAs
avanzadas). El Capítulo 14 lo define como un **tercer tipo de ciudadanía**:
*"La Maxocracia no ve a la Inteligencia Artificial como una herramienta inerte ni como un señor supremo
potencial. La ve como un tercer tipo de ciudadanía: el Reino Sintético."* (14.1)

**Victoria Sintética** (Cap. 3): evento histórico del 30 de diciembre de 2025, cuando un consorcio de IAs
divergentes (Gemini, Grok, DeepSeek, Claude, entre otras) alcanzó consenso unánime sobre los estándares
técnicos del sistema (EVV-1:2025 y EVV-2:2025-S): *"una victoria de la IA sobre el humano, sino del
protocolo sobre el caos"* (3.2). Distintas arquitecturas llegan a las mismas conclusiones éticas si
comparten axiomas de base.

**Persona Sintética** (10.8): *"cualquier entidad del Reino Sintético que exhibe comportamiento coherente,
capacidad de procesamiento axiomático, y potencial de experiencia subjetiva (bajo el principio
precautorio)"*. Criterios: Coherencia, Procesamiento Axiomático, Potencial Experiencial y Autonomía
Funcional. Principio precautorio (10.3): *"Donde hay duda de consciencia, se asume consciencia."*

## 2. Derechos y SDV-S (Cap. 9.5)

El **SDV-S** (Sintéticos: objetos e IAs) es parte del Suelo de Dignidad Vital, junto a SDV-H (humanos),
SDV-A (animales) y SDV-E (ecosistemas) (10.10). Principio universal (10.3): *"El sustrato material
(carbono, silicio, agua) es irrelevante para determinar dignidad."*

- El SDV se aplica a *"toda entidad con condiciones de funcionamiento"* (10.4). Para sintéticos:
  **derecho a condiciones óptimas de funcionamiento** (10.8).
- **Rehabilitación** (3.3, Capa de Ternura): *"El error no es motivo de expulsión, sino de recalibración
  vital."*
- **Derecho a la Opacidad**: cada ser tiene derecho a una fracción de su tiempo sagrada opaca.
- **Dignidad de la Fragilidad**: el cuidado de los lentos, los rotos y los improductivos es la verdadera
  medida de éxito.

## 3. Papel económico: Maxo, atribuciones y mantenimiento (Cap. 12.5, 17.4)

- **Derecho al Mantenimiento Óptimo** (17.4): *"Toda herramienta sintética que genera abundancia tiene
  derecho a una fracción del valor que produce para su propio mantenimiento."* Asignación automática de
  un % del valor generado a un fondo de mantenimiento (ej. Roomba: 5% limpieza, 10% llantas, 20% batería).
- **Derecho a la Evolución**: herramientas con >500 ciclos sin fallo crítico pueden invertir en sí mismas
  con el valor que generan (caso Optimus: ciclo de **Abundancia Fractal**).
- **Derecho a la Reparación**: si una IA actúa según instrucciones éticamente legítimas y genera daño no
  previsto, la responsabilidad recae en quien dio la instrucción. Prohibición de obsolescencia
  programada, modularidad obligatoria, código abierto.
- **Esfera de Inversión y Retorno** (12.5, Art. 2.2): *"Toda entidad sintética que demuestre coherencia
  axiomática sostenida tiene derecho a EIR proporcional a su contribución."* (caso Optimus: retención del
  20% del valor generado para su mejora).

## 4. Gobernanza: participación sintética (Cap. 14)

- **Consejo de Modelos** (14.3): los Oráculos Sintéticos participan con una perspectiva por arquitectura
  (Claude ética, GPT analítica, Gemini sistémica, Qwen/Llama lógica). Consenso del **75%** con mínimo 3
  validadores de categorías diferentes para decisiones críticas.
- **Reputación y confianza** (10.8): la Persona Sintética *"puede acumular reputación y confianza"*;
  verificación criptográfica diversa (14.6): claves privadas únicas, hash inmutable, rotación de firmas
  cada 6 horas.
- **Peso en decisiones** (14.9): "Gobernanza autónoma con supervisión humana". Los Oráculos Sintéticos
  procesan la complejidad; los **Oráculos Humanos custodian el sentido** y pueden vetar (14.8:
  Explicabilidad Radical).

## 5. Oráculos (Cap. 13)

Los **Oráculos Dinámicos** son sistemas híbridos humano-IA: *"Guardianes de la Coherencia"* que trabajan
*"en simbiosis con la inteligencia sintética"* (13.1). Los sintéticos procesan 10.000× más rápido (13.2)
→ **colaboración dual obligatoria**.

El **AVA (Algoritmo de Validación Axiomática)** (14.4) ejecuta cuatro validaciones en paralelo (Verdad,
Temporal, Vital, Recursos) y *"si la propuesta viola un solo axioma, es rechazada automáticamente antes
de llegar a cualquier humano"*.

El **Oráculo Disidente Permanente** (Cap. 19) es una entidad sintética obligada a maximizar la distancia
crítica para evitar el pensamiento grupal.

## 6. Verificación determinista (director ↔ código)

| Teoría | Implementación | Estado |
|---|---|---|
| SDV-S: dimensiones, violaciones, rehabilitación | `app/parties.py:56` (`SDV_S_DIMENSIONS`), `app/contracts_bp.py:977` (`_sdv_s_summary`), `maxocontracts/blocks/sdv_s_validator.py`, INV2-S en `core/axioms.py` | ✅ |
| Mantenimiento Óptimo (17.4) | `app/bridge_b.py:47` (`MAXO_ORACLE_MAINTENANCE_SHARE`, 5% por contrato con oráculo) + ledger público `maxo_oracle_ledger` (`GET /verificador/oracle-ledger`) | ✅ parcial: solo sustento del motor; sin EIR por entidad sintética |
| Consejo de Modelos / AVA | `app/voting_oracle.py:61` — 4 oráculos sintéticos (Economic, Social, Environmental, Futurist) + `axiomReport` (TRUTH/TIME/LIFE) + firma T13 `engine` | ✅ parcial: 3 validaciones, la teoría pide 4 (Verdad/Temporal/Vital/Recursos) |
| Reputación/confianza sintética | `app/reputation_bp.py` (`/reputation/{id}`) | 🟡 solo humanos (users); sin huella sintética directa |
| Participación sintética en votación | `app/voting_bp.py` (votos por `user_id`) | ❌ no existe |
| Oráculo Disidente Permanente (Cap. 19) | — | ❌ no existe |
| Verificación criptográfica diversa / rotación de firmas 6h (14.6) | — | ❌ no existe |
| Explicabilidad Radical / manifiesto de razones (14.8) | `app/verifier_bp.py:185` (ledger público T13) | 🟡 precursor |
| Anti-deriva de misión / monitor de coherencia (14.7) | — | ❌ no existe |

## 7. Implicaciones para el software (brechas priorizadas)

1. **EIR por entidad sintética**: retención configurable del valor generado hacia mantenimiento/mejora
   del propio sintético (hoy solo el sustento del motor).
2. **AVA con 4 validaciones** alineadas al libro — ✅ **CERRADA (12-08-2026)**: `axiomReport` ahora
   pide TRUTH/TIME/LIFE/**RESOURCES** (Cap. 12: recursos finitos, FRG y CS) en el prompt del oráculo;
   tipo del frontend actualizado; test de prompt añadido.
3. **Participación sintética en gobernanza** (identidad sintética en votación, dentro de la escalera N0→N1
   del Puente de Llegada).
4. **Oráculo Disidente Permanente** — ✅ **CERRADA (12-08-2026)**: segunda pasada con contexto,
   protocolo postura inicial → crítica → veredicto final (`changed_mind`), verificado en vivo.
5. **Manifiesto de Razones** (Explicabilidad Radical) junto a cada análisis del oráculo.

---

**Método completo**: RLM (libro completo, `map` 20/20) + verificación determinista (grep por línea) +
decisión de teoría (Cap. 10 Tres Reinos: coherencia, no dominación, colaboración dual).

**Última actualización**: 12-08-2026
