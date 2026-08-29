# Roadmap de implementación — Rama Educativa en la plataforma

> **Fase:** Ola 4 + — plan operativo de la rama educativa (marco conceptual en `docs/theory/EDUCACION_SIAMESA_estructura_maxocratica.md` y `docs/theory/ESTRUCTURA_IDEAL_ORGANISMO_EDUCATIVO_VITAL.md`).
> **Estado:** M1-M8 implementados (28-08-2026) + **M9 Parlamento Educativo** (29-08-2026) — motor (INV2-EDU, regla de oro, triada, árbol de habilidades), Foro Abierto (+ respuestas), Talleres, Grupos/ECEs y Células Madre, UI y puente años↔índice **gobernable por votación**, guía del foro (MiniMax). Track paralelo (MVP): `plataforma_educativa/` con triada de mentoría completada.
> **Regla de coherencia:** cada hito = commit conventional en español + tests + entrada en `docs/architecture/atribuciones_sinteticas.md`.

---

## M1 ✅ INV2-EDU: el motor mide lo que declara

**Problema resuelto:** `SDV.educacion_anos_minimos = 12` estaba declarado pero NADIE lo validaba: ni `meets_minimum()`, ni `violations()`, ni `SDVValidatorBlock._check_all_dimensions()`. Un contrato podía empujar a alguien bajo el piso educativo sin disparar INV2.

**Implementación (retrocompatible):**

| Archivo | Cambio |
|---|---|
| `maxocontracts/core/types.py` | Nuevo campo de estado `educacion_anos: Optional[int] = None` (años completados; `None` = no reportado → la validación se activa cuando hay dato). `meets_minimum()` y `violations()` incluyen la dimensión educación |
| `maxocontracts/blocks/sdv_validator.py` | `_check_all_dimensions()` valida `educacion` con severidad; `to_dict()` la serializa (T13) |
| `tests/test_maxocontracts/test_types.py` | +4 tests (violación, frontera 12, por encima, sin dato) |
| `tests/test_maxocontracts/test_axioms.py` | +2 tests INV2 (educación violada / en piso) |
| `tests/test_maxocontracts/test_blocks.py` | +2 tests del bloque (violación / en piso) |

**Semántica:** el motor trabaja en **años** (canon SDV-H: ≥12 años formales). La capa app usa índice 0-1 (`SDVScore.educacion`) — el puente años→índice es el hito M5. Guardarraíl respetado: **nada de validación en `__post_init__`** (los 24 usos de `SDV()` en tests siguen intactos; verificado con suite completa en verde).

---

## M2 ✅ Foro Abierto (`app/forum_bp.py`)

**Qué es:** la plaza del conocimiento: cualquier participante publica un tema, una pregunta, una oferta de taller o una necesidad educativa.

- **Nuevo**: blueprint `forum_bp.py` con patrón de `guide_bp.py` (`token_required`, `init_*_tables`, T13) + tabla `forum_posts` (autor, tipo: `topic|question|workshop_offer|need`, título, cuerpo, tags, estado).
- **Ya existe**: necesidades en `forms_bp.py` (`POST /participants/<id>/needs`) y matching (`find_matches`, `get_community_sdv_gaps`) — el foro los referencia, no los duplica.
- **Endpoints**: `POST /forum/posts`, `GET /forum/posts?type=&tag=&status=`, `GET /forum/posts/<id>`, `POST /forum/posts/<id>/close`, `GET /forum/needs` (puerta al matching).
- **Tests**: 15 (`tests/test_forum.py`) — crear post, listar por tipo/tag, cerrar (autor/admin), permiso 403, puerta de necesidades.
- **Docs**: página `/foro` (M5); commit `128cfa6`.

## M3 ✅ Talleres de Aprendizaje (`app/workshops_bp.py`)

**Qué es:** la unidad de enseñanza de CUALQUIER skill (la regla de oro: el skill se gana enseñándolo — la vacuación).

- **Tabla** `workshops` (título, skill_nodo, facilitador_id, estado `open|running|closed`, cupos 5-12), `workshop_enrollments` (aprendiz, estado `apprentice|advanced`), `workshop_outputs` (material abierto | obra aplicada), `skill_awards` (T13 completo).
- **Regla de oro en el motor**: `maxocontracts/skills.py` — para ganar el skill: (1) obra aplicada, (2) material de enseñanza publicado, (3) mentoría mínima (≥1h TVI); veredicto puro (`evaluate_vacuacion`) + triada (`evaluate_triada`: mentor + par + oráculo con veto).
- **Endpoints**: `POST /workshops`, `GET /workshops`, `GET /workshops/<id>`, `POST /workshops/<id>/enroll`, `POST /workshops/<id>/outputs`, `POST /workshops/<id>/grant-skill`, `POST /workshops/<id>/close`.
- **Tests**: 30 (15 motor `tests/test_maxocontracts/test_skills.py` + 15 API `tests/test_workshops.py`); commit `c93a8a5`.

## M4 ✅ Grupos de Solución y Células Madre (`app/groups_bp.py`)

**Qué es:** los ECEs — grupos que resuelven necesidades reales de la comunidad — y las células madre, cuyo oficio es formar otros grupos.

- **Tabla** `edu_groups` (tipo: `solution_group | mother_cell`, need_title/need_id, estado), `edu_group_members` (rol member/coordinator), `edu_group_children` (fractalidad), `group_skill_nodes` (nodo ganado con evidencia).
- **Célula madre**: cada grupo formado registra su matriz (trazabilidad fractal); la madre gana nodo "facilitación" al ver florecer una réplica.
- **Endpoints**: `POST /groups`, `GET /groups`, `GET /groups/<id>`, `POST /groups/<id>/join`, `POST /groups/<id>/child`, `POST /groups/<id>/close`.
- **Tests**: 12 (`tests/test_groups.py`); commit `5d0b457`.

## M5 ✅ UI y puente años↔índice

- **Frontend** (`frontend/app/`): páginas `/foro`, `/talleres`, `/grupos` (API real, nada pintado) + sección de navegación "Aprendizaje" (desktop y móvil).
- **Puente**: `app/sdv_analyzer.py` `educacion_indice()` (años del motor ↔ índice 0-1 del SDVScore): ≥12 años → 1.0, lineal 0.1→1.0 0-12 años, None → 1.0 (sin dato no castiga); umbral canónico a decidir en parlamento.
- **Docs**: `mapa_frontend_ola4.md` (+4 filas: guia, foro, talleres, grupos); 7 tests del puente; commit `e992061`.

## M6 ✅ Árbol de habilidades en el motor (`maxocontracts/tree.py`)

**Qué es:** el tejido como dominio — nodos de skill con prerrequisitos (caminos de maestría, no años), forks del tejido, y el veredicto completo de apertura (prereq + regla de oro + triada, T13).

- `SkillNode` (id canónico `rama/nodo`, nombre, rama, prereqs, dificultad 1-5, descripción) y `SkillTree` inmutable **validado** (ids únicos, prérequisito ausente, auto-certificación, ciclos — guardarraíles).
- `prereqs_met`/`path_of` (camino de maestría), `with_node` (fork: el tejido se expande), `build_canonical_tree` (8 ramas canónicas = el mismo cosmos del prototipo) y `evaluate_unlock` (prerrequisitos + vacuación + triada en un veredicto serializable).
- API: `POST /workshops` valida `skill_node` como nodo del árbol (`rama` | `rama/nodo`); el cosmos completo por tema vive en `plataforma_educativa/`.
- **Tests**: 28 (20 motor `tests/test_maxocontracts/test_tree.py` + 8 validación API); commit `4071457`.

## M9 ✅ Parlamento Educativo — el umbral canónico se vota (29-08-2026)

**Problema resuelto:** M5 dejó `educacion_indice()` con el umbral congelado en 12 años y anotó "umbral canónico a decidir en parlamento" — pero no existía ningún mecanismo para votarlo: era una constante sagrada con la puerta cerrada.

**Implementación (la ley NO se vota; la plenitud sí):**

| Archivo | Cambio |
|---|---|
| `app/schema.sql` | Tablas `edu_parameters` (umbral vigente + procedencia T13; CHECK ≥ 12 — INV2-EDU — y ≤ 30) y `edu_parameter_resolutions` (historial vinculante, T13) |
| `app/voting_bp.py` | `POST/GET /voting/parliament/educativo` (categoría critical 60/75); acción vinculante `set_edu_umbral` despachada por `_apply_passed_action`; guardarraíles: `_validate_edu_umbral_params` (12-30, finito, no bool), anti-flip-flop 14 días (`EDU_COOLDOWN_DAYS`), escalera de confianza N1+ (guard añadido también al parlamento de α/β/γ/δ); finitud NaN/∞ y no-bool en ambos validadores |
| `app/sdv_analyzer.py` | `educacion_indice(anos, umbral_anios=EDU_ANIOS_MINIMOS)` parametrizada (retrocompatible) + `get_edu_umbral_anios(conn)` (última resolución o canon; tabla ausente → canon) |
| Tests | `tests/test_parlamento_educativo.py` (20: validación, creación, flujo aprobado/rechazado, cooldown, N0, NaN/∞, analizador con umbral comunitario) + `tests/test_sdv_educacion_puente.py` (+5 de umbral parametrizado) + `tests/test_maxocontracts/test_parliament.py` (+casos NaN/bool) |
| Docs | `docs/architecture/PROPUESTA_PARLAMENTO_UMBRAL_EDUCATIVO.md` — la propuesta lista para la comunidad (consecuencia honesta: umbral > 12 → quien tiene la ley obtiene índice < 1.0, narrativa "riesgo"; fundamento: Rondas §1.1 + δ §5.7) |

**Semántica:** la aspiración de plenitud es política votable (12-30); la ley ≥ 12 años es axioma del motor (`SDV.educacion_anos_minimos`) y no se toca. El parlamento ya sabe qué hacer: `_apply_passed_action` ejecuta y el analizador SDV recalibra los índices con el canónico vigente.

---

## Orden recomendado de sesiones

1. **M1** ✅ (hecho).
2. **M2** (foro API) — base de todo: el foro es la puerta de talleres y grupos.
3. **M3** (talleres + regla de oro) — el corazón conceptual; sin foro no hay talleres.
4. **M4** (grupos + células madre) — la capa fractal.
5. **M5** (UI + puente) — lo visible; se puede solapar con M3/M4.

## Riesgos y guardarraíles

- **Compatibilidad**: toda tabla nueva = schema idempotente (patrón `init_*_tables` de `create_app`).
- **La regla de oro sin burocracia**: la concesión de skill es por triada, no por examen; el verificador es verificable (rotación + veto).
- **Tiempo opaco**: los chequeos gamificados de la UI nunca exponen rankings por persona (cooperativos, de estado).
- **Marco legal**: la defensa/ protección se integra como en `RAMA_DEFENSA_PERSONAL_Y_COOPERATIVA.md` — asociaciones, defensa civil y seguridad regulada; nada fuera de la norma.
