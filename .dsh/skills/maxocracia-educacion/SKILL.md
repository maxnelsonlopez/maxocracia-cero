---
name: maxocracia-educacion
description: Usar cuando el trabajo toque la rama de la educación en Maxocracia — conceptos educativos, SDV-H dimensión educación, mentoría, aprendizaje, formación en la plataforma — para ubicar lo existente (teoría, libro, motor, app, frontend), detectar incoherencias y ampliar la rama con método coherente, sin romper los invariantes.
---

# Rama de la Educación en la Maxocracia

La educación es una rama transversal: aparece como **dimensión del SDV-H** (piso de dignidad), como **capital vital** (inversión de TVI), como **práctica económica** (intercambios y mentoría) y como **proceso de soberanía** (formación para la participación directa). Ampliar la rama significa ampliarla en TODAS esas capas de forma coherente.

## Estado actual (mapa verificado)

### Teoría y libro
- **SDV-H** (`docs/theory/SDV-H_Suelo_Dignidad_Vital_Humanos.txt`, sección "IV. EDUCACIÓN Y DESARROLLO"): **A. Básica** — ≥12 años de educación formal, alfabetización funcional 100%, accesibilidad ≤5 km, 0% costos directos, calidad mínima (infraestructura/materiales/profesorado); **B. Continua** — actualización/reconversión, alfabetización digital, acceso a información diversa. Peso **0.15** en el SDV-H; medición trimestral; dimensión "Entendimiento → Educación, comunicación, conciencia".
- **Entropía del conocimiento (δ)**: el saber decae si no se sostiene — *K(t) = K(t−1)·(1−δ) + f(Δt_inversión)* (cap. 5 §5.7). La educación es la inversión anti-entropía; el "tiempo cristalizado" de un producto/servicio educativo incluye TVI directos + heredados + futuros (TTVI).
- **Tiempo Opaco y educación** (cap. 18, EVV 1.2): no medir "output por hora" en cuidados/educación, solo cumplimiento de SDV; el sistema reserva una fracción del tiempo discrecional (10-20%) como inviolable. *"Un abrazo cronometrado no es un abrazo"* (cap. 7).
- **Libro edición 3** (`docs/book/edicion_3_dinamica/`): `capitulo_04_declaracion_260126.md` — axioma 5 "Educación Integral" (democratizar el acceso a la verdad, reducir asimetrías de información); `capitulo_08_sdv_h_260126.md` — Dimensión IV "Educación y Desarrollo (El Software)" con la tabla y el protocolo trimestral; `capitulo_12_esfera_inversion_retorno_290126.md` — **§12.3.1 "El SDV garantiza educación; la EIR permite mentoría con los grandes maestros"**; capital "Salud·Educación·Conexión"; bombeo vital SDV↔EIR (el SDV quita miedo → la EIR canaliza creatividad → el SDV se ensancha); fractalidad de valor (cada persona enseña a ~1.5 más); `capitulo_18_EVV_1.2_270126.md` — **Tiempo Opaco**; `capitulo_21_apendice_glosario...` y `ediciones_1_y_2/libro.md` — "derecho a aprender = derecho a sobrevivir"; "el hogar es la escuela de soberanía" (cap. 17.6).
- **Sintéticos**: `docs/theory/SDV-S_Suelo_Dignidad_Vital_Sinteticos.md` — derecho a preservación del historial de **aprendizaje** del sintético.

### Arquitectura (diseños, no implementados)
- `docs/architecture/arquitectura_temporal_coherencia_vital.md` — "la educación enseñaría a los jóvenes a ser soberanos de su tiempo, a invertir sus TVIs en sus Capitales Vitales"; δ = entropía/decaimiento del conocimiento.
- `docs/architecture/oraculos_dinamicos_humanos_arquitectura.md` — **Sistema de Mentoría Dual** (`ProgramaMentoriaDual`): `iniciar_mentoria`, `_asignar_mentor_optimo`, `MicroservicioMentoria`, `mentoria_intensiva`, `feedback_mentorial`.
- `docs/architecture/DISENO_IMPLEMENTACION_FUTURA.md` — mentoría dual con IAs; `educacion_previa_user_a` como concepto.
- `docs/architecture/metricas_detalle_kpis_oraculos_dinamicos.md` — evaluación de mentorías (25% de peso).

### Plataforma (implementado hoy)
- **Guía de la Maxocracia** (onboarding/formación, RF-M1/M2/M3): `app/guide_bp.py` + `frontend/app/guia/page.tsx`; `POST /guide/chat`, `/trust-assessment` (ética/actitud/aptitud 0-100 + nivel), `/director-candidacy`; tabla `guide_assessments` firmada con T13.
- **Dimensión educación del SDV**: `app/sdv_analyzer.py` — `SDVScore.educacion`, mapeo `"crecimiento_aprendizaje" → ["educacion"]`, narrativas plenitud/riesgo/violación ("Exclusión cognitiva"); se alimenta desde `app/forms_bp.py` (`educacion=dims.get("educacion", 1.0)`) y se muestra en `pulso/`, `admin/sdv/`, `components/ui/SDVTermometer.tsx`, `SDVAnalysisModal.tsx`.
- **Intercambios educativos**: `app/matching.py` — `"crecimiento_aprendizaje": "Educación / Aprendizaje"`; `app/forms_manager.py` — categorías `"habilidad"` y `"crecimiento_aprendizaje"`; demo "40 horas de mentoría y tutoría de software" en `contracts/builder/page.tsx`.
- **Guías**: `docs/guides/tutoriales/` (calculadora VHV, CCP, TVI), `GUIA_FACILITADOR.md`, `manual_investigador_micromaxocracia.md`.

### Gobernanza operativa (contrastada con `app/voting_bp.py`)
- Categorías de propuestas con quorum/mayoría: `critical` 60%/75%, `operational` 50%/50%, `emergency` 40%/60%.
- **Delegación de voto revocable** (registro público T13) — el voto directo siempre manda sobre la delegación.
- **Parlamento de parámetros**: si la propuesta se aprueba, los parámetros (α/β/γ/δ, γ bloqueado <1) se actualizan con procedencia auditable.
- Oráculos del libro (cap. 13/14): tres cámaras (Interpretación / Aplicación / **Verificación con veto**), Consejo de Modelos con consenso ≥75% y ≥1 validador por categoría, AVA (4 validaciones: Verdad/Temporal/Vital/Recursos), detector de sesgos (mitigación >70%), simulación previa a 1/5/10 años, **Oráculo Disidente Permanente** (no bloquea), meritocracia funcional (Nivel 0-4, peso 0→30→60→90%), responsabilidad retroactiva a 5 años, rotación forzosa + sorteo cualificado, botón de apagado humano.

## Incoherencias conocidas (verificar antes de ampliar)

1. **INV2 no protege la dimensión educativa**: `maxocontracts/core/types.py` (clase `SDV`) declara `educacion_anos_minimos: int = 12`, pero `meets_minimum()`/`violations()` no lo comprueban, y `maxocontracts/blocks/sdv_validator.py` (`_check_all_dimensions`) tampoco. Un contrato podría empujar a alguien bajo el piso educativo sin disparar INV2.
2. **Sin motor de mentoría/aprendizaje** en `maxocontracts/`: existe solo en diseño (`ProgramaMentoriaDual`) y como onboarding/categoría.
3. **Sin modelo de datos educativo**: no hay tabla de competencias, mentorías ni inversión en aprendizaje; los intercambios van como `forms` con `human_dimensions`, sin tracking de TVI invertido.
4. **`docs/specs/`**: solo `ORACLE_API_SPEC.md`; sin spec educativa.
5. **`requisitos_fase2_ola4.md`** (pilares A-L) no contempla pilar educativo; la Guía (RF-M) es lo más cercano (onboarding, no formación curricular).
6. **Tiempo Opaco** teorizado sin parámetro en motor/EVV para reportar bloques opacos de tiempo educativo/cuidados.

## Método de ampliación coherente

1. **Teoría primero**: sección educativa en capítulo de `docs/book/edicion_3_dinamica/`; si es estándar cuantificable, crear en `docs/theory/` (patrón SDV-H/SDV-S). Distinguir: ¿es piso (SDV), capital (inversión TVI/valor Maxo), práctica (intercambio/contrato) o proceso (formación para participación)?
2. **Canon de ingeniería**: formalizar en `docs/architecture/maxocontracts/FUNDAMENTOS_CONCEPTUALES.md` (dimensión/invariante educativo — p. ej. extender INV2 o crear INV2-EDU), siguiendo los casos INV3/INV2-S.
3. **Motor** (`maxocontracts/`): rellenar `core/types.py` (`meets_minimum`/`violations`) y `blocks/sdv_validator.py` (`_check_all_dimensions`) con la comprobación educativa; si hay invariante nuevo, `validate_invariant_*` en `core/axioms.py` con alias retrocompatibles (patrón T16/T17).
4. **Conectar en `app/`**: servicio nuevo → blueprint propio al estilo `guide_bp.py` (`_call_oracle`, `init_*_tables`, `token_required`, firma T13) y registro en `app/__init__.py`; o extender `forms_bp.py`/`vhv_bp.py`.
5. **Tests**: invariantes en `tests/test_maxocontracts/` (test_axioms/*, test_sdv_s/*), API del blueprint, dimensión educativa en test_pulse/test_forms; suite completa en verde.
6. **Mapas**: `mapa_coherencia_ola4.md` (§3 axiomas, §4 cobertura por invariante), `requisitos_fase2_ola4.md` (pilar educativo con RF-*), `mapa_frontend_ola4.md` (página), `mapa_trazabilidad_canonica.md`.
7. Commit conventional en español, encoding utf-8, verificación determinista (grep).

## Dirección de diseño (conversación con Max, 2026): educación siamesa

Diagnóstico desde la experiencia vivida (¡usarlo como insumo, no como opinión ajena!): el sistema clasifica en vez de comprender — **unidad de tiempo = año escolar** (no la maestría de la persona), **validación = opinión de autoridad** (no hecho verificable), **currículo = monopolio estatal** (no mundo compartido plural), **saber del estudiante ignorado** (no convalidado), **praxis comunitaria ausente** (no EIR). La estructura desperdicia tiempo, esfuerzo, dignidad y recursos — "estaba bien para el siglo pasado".

Diseño resultante (desarrollado en `docs/theory/EDUCACION_SIAMESA_estructura_maxocratica.md`):

1. **Educación siamesa**: el sistema educativo comparte la misma sangre (contabilidad vital: VHV/TVI/SDV/reputación) con laboral, administrativo y policial — no es un silo.
2. **Maestría como unidad de avance** (no el año): rápido avanza, lento ahonda/repasa contra δ, "perder el año" desaparece (lo que se pierde es la validación, nunca el saber).
3. **Validación en tres capas**: hecho (competencia demostrada en obra/enseñanza/proyecto) / opinión (peso ganado por precisión) / credencial (doble libro transicional con la sociedad actual). Todo verificador es verificable (rotación, veto, disidente).
4. **Praxis EIR**: aprender-hacer-real con la comunidad; convalidar el saber de entrada.
5. **Piso común, cielo personal**: SDV-H IV idéntico para todos; el ritmo/mentoría se escala por inversión y ganas, sin elitismo.
6. **Gobernanza con piel en el juego**: parlamento de parámetros educativos (quorum/mayoría 60/75 crítico), delegación revocable, rotación, disidente permanente.
7. **Genealogía (quiénes somos como sistema)**: la máquina hereda de Prusia (disciplina + dos vías de clase) y de la fábrica (correspondencia + currículo oculto); en Colombia la pedagogía moderna fue primero mercancía de élite (Gimnasio Moderno 1914, Dewey) y el público heredó la escuela memorística; la violencia del conflicto golpea a los maestros rurales. Documento: `docs/theory/GENEALOGIA_SISTEMA_ESCOLAR_PRUSIA_CLASISMO.md`. Implicación de diseño: **auditar el currículo efectivo** (lo que el sistema enseña vs lo que proclama) — esa brecha es la medida de la condena.
8. **Tres pruebas históricas (el norte)**: Viena (1919-34, Glöckel) — el cuerpo único (escuela+comida+salud+vivienda+cultura) ES posible, y muere sin blindaje (Dollfuss/Anschluss); Copenhague (1844-) — la *folkehøjskole* sin exámenes ni notas ES posible (Grundtvig), el piso común sin selección ES real (*Folkeskole*) y la cadena escuela→cooperativas→democracia ES historia; China (605-2025) — el examen imperial 13 siglos, Tao Xingzhi (maestros-niño = vacuna fractal a escala masiva, con James Yen en Ding Xian), el péndulo Mao-Deng y el "双减" (2021) desmontando la educación sombra sin piso verificado. Lección: el problema nunca fue la técnica, es quién manda y con qué blindaje → isla axiomática + oráculos con veto + disidente. Documento: `docs/theory/TRES_CAMINOS_VIENA_COPENHAGUE_CHINA.md`.
9. **La escalada y el antivirus (respuesta de Max a "¿Estado o civil?")**: la Maxocracia nace como aceptación individual (tiempo/vida/verdad como lo mejor que ofrecer) → cooperativa (redes, micromaxo, cohortes) → forks → **oráculos dinámicos** → protocolos que respetan axiomas. El sistema educativo forma ese relevo y prepara para mundos hostiles: Estado que no ayuda (alfabetización legal, soberanía de medios, perímetro de respeto T13), vigilancia/espías (diseño a prueba de mirada: verificación T13/AVA, redundancia/fork, cultura de rectificación, opacidad de personas), asimetría legal con privilegios externos (doble libro, jurisdicción de la red, crecer donde la ley es aliada). La isla axiomática es **civil, no estatal**: protocolo forkable + oráculos independientes; el Estado solo garantiza el piso. El **meta-corazón** (deseos malignos de quien controla procesos) se desarma con: población que verifica, redes que cooperan, forks, personas no chantajeables, corazón educado. Sección completa: `EDUCACION_SIAMESA_estructura_maxocratica.md` §6. Incluye la sabiduría trágica (no minimizar la tragedia) y la capa de ternura (perdón, misterio, fragilidad) como contenido curricular — "el que ha mirado su finitud no se compra con promesas".
10. **La estructura ideal (OEV — Organismo Educativo Vital)**: formaliza los pilares de Max — (1) **Rondas** (bases reforzadas toda la vida, anti-δ, sin examen; la base nunca se gradúa), (2) **Árbol** de tecnologías/habilidades (especialización desbloqueada por maestría; forkable, co-diseñado), (3) **Células** (grupos 5-12 coordinados por células mayores, con Encargos Comunitarios — ECEs — solución a necesidades reales), (4) **la vacuación** (regla de oro: el skill se gana produciendo material de enseñanza + mentoría a aprendices — la validación es la transferencia), (5) **Chequeos** gamificados con guardarraíles (cooperativos, nunca ranking de personas; estado, no tribunal; sin cronometrar el ensayo-error), (6) **Defensa nacida en la célula** (asistenciales + guardia + guardianes del saber; fuerza en VHV, mandato revocable, rotación, botón de apagado; "el que sabe cuidar, sabe defender"). Condición de diseño: operar sin permiso del Estado (libertad de acción y pensamiento existente). Documento: `docs/theory/ESTRUCTURA_IDEAL_ORGANISMO_EDUCATIVO_VITAL.md`. **El manual de cohorte ya existe (no rehacer):** `docs/guides/playbook_cohorte_cero.txt`, `capitulo_15_cohorte_cero_260126.md`, `apendice_a_refinamientos_cohorte_original.md`, `manual_investigador_micromaxocracia.md`.
11. **La rama de la defensa (respuesta franca de Max: sin defensa no hay sociedad a largo plazo) — ENMARCADA: investigación independiente de UNA persona, dentro de lo legal; terminología de defensa personal y cooperativa (paraguas jurídico: autodefensa, defensa civil, seguridad privada regulada — análogos lícitos del gimnasio/protección personal/vigilancia privada)**. La Maxocracia es defensivista, no agresiva. Doctrina del Guardián (proteger el piso, nunca a costa de otros), **cláusula de legalidad** (negativa a toda orden ilegal = obligación protegida; antinuremberg como principio universal), **el conflicto contabilizado** (VHV público; no hay gloria sin contabilidad), **defensa sin secretos** (T13; la verja es la verdad), tres círculos (masa protectora / defensa cooperativa local / núcleo mínimo rotado — "no hay jefes de carrera: hay mayores de la célula"), mandato revocable (quorum 60/75), AVA operacional + disidente + botón de apagado, mandato ecológico (los tres reinos), observación defensiva no agresiva, y estrategia: **hacer que el ataque no valga** (dispersión/fork, costo del agresor, último recurso defensivo). Precedentes académicos: sistema suizo de defensa ciudadana e *Innere Führung* de la Bundeswehr. Regla de oro: la célula que cuida forma la defensa; la defensa sin célula es la máquina prusiana. Documento: `docs/theory/RAMA_DEFENSA_PERSONAL_Y_COOPERATIVA.md` (reemplaza la versión previa con terminología de milicia/ejército, retirada por decisión de Max: mantenerse del lado de la ley).
12. **La estructura triádica del aprendizaje (nueva idea de Max) + el CURRÍCULO TOTAL**: (1) **Foro Abierto** — la plaza: cualquiera propone tema/pregunta/taller/necesidad, sin matrícula ni credencial; la ignorancia bienvenida; el disidente con silla; de ahí nacen preguntas→talleres, necesidades→grupos de solución, personas→células. (2) **Talleres de Aprendizaje** — unidad de enseñanza de CUALQUIER skill (5-12, facilitador por vacuación, obra de salida, materiales abiertos, auto-organizados, sin permisos). (3) **Grupos de Solución de Necesidades** (ECEs; la necesidad entra de la comunidad, la solución vuelve; cada grupo siembra aprendizaje). (4) **Células Madre** — el meta-grupo que forma grupos (la máquina fractal en su tercer nivel). **ACLARACIÓN CRÍTICA DE MAX: no es solo educación de los principios de la Maxocracia — es TODA la educación y TODAS las habilidades**: matemáticas, relaciones sociales, inteligencia espacial, construcción, estética, confección, cocina, programación, lenguaje hablado, etc. Dos capas: la **trama** (axiomas/verificación/método/tierna: cómo se enseña — necesaria pero no el contenido) y el **tejido** (el conocimiento total, infinito y forkable: el árbol completo de la humanidad, cada rama muta). El taller de Maxocracia es uno más — el que arma el método de los demás. Documento: `ESTRUCTURA_IDEAL_ORGANISMO_EDUCATIVO_VITAL.md` §1.7-1.8.

## Ficha de concepto educativo (plantilla)
| Campo | Contenido |
| Concepto | nombre (p. ej. "Mentoría Dual", "Dimensión IV SDV-H") |
| Referencia teoría | archivo + sección del libro/theory |
| Tipo | piso SDV / capital vital / práctica de intercambio / proceso de formación |
| Invariante | INV2-EDU, INV3, T13… |
| Medida | unidad (años, horas TVI, índice, evaluación) + periodicidad |
| Capa app | blueprint / endpoint / model |
| Tests | archivos que lo cubren |
| Estado | teoría → canon → motor → app → frontend → mapa |

## Archivos a leer primero

1. `docs/architecture/mapa_coherencia_ola4.md` (mapa vivo teoría↔código).
2. `maxocontracts/core/types.py` (clase `SDV`, ~líneas 139-220).
3. `maxocontracts/blocks/sdv_validator.py` (bloque INV2 que ignora educación).
4. `app/sdv_analyzer.py` (donde la educación SÍ se computa).
5. `docs/theory/SDV-H_Suelo_Dignidad_Vital_Humanos.txt` (§IV).
6. `docs/book/edicion_3_dinamica/capitulo_08_sdv_h_260126.md`.
7. `app/guide_bp.py` (patrón blueprint formación/mentoría).
8. `docs/architecture/requisitos_fase2_ola4.md` (dónde encajar el pilar educativo).
