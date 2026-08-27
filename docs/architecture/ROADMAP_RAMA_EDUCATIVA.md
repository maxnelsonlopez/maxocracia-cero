# Roadmap de implementación — Rama Educativa en la plataforma

> **Fase:** Ola 4 + — plan operativo de la rama educativa (marco conceptual en `docs/theory/EDUCACION_SIAMESA_estructura_maxocratica.md` y `docs/theory/ESTRUCTURA_IDEAL_ORGANISMO_EDUCATIVO_VITAL.md`).
> **Estado:** M1 implementado (INV2-EDU) — el motor ya valida la dimensión educativa cuando hay dato. M2-M5 diseñados, pendientes de sesiones siguientes.
> **Track paralelo (MVP):** `plataforma_educativa/` — plataforma educativa independiente con árbol (8 ramas), reuniones-células de 8, monitores-vacuadores y perfil sin email: prototipo vivo del OEV (ver `docs/guides/PLATAFORMA_EDUCATIVA.md`). Sirve de plantilla para los hitos M2-M4 de la plataforma principal.
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

## M2 ⏳ Foro Abierto (`app/forum_bp.py`)

**Qué es:** la plaza del conocimiento: cualquier participante publica un tema, una pregunta, una oferta de taller o una necesidad educativa.

- **Nuevo**: blueprint `forum_bp.py` con patrón de `guide_bp.py` (`token_required`, `init_*_tables`, T13) + tabla `forum_posts` (autor, tipo: `topic|question|workshop_offer|need`, título, cuerpo, tags, estado).
- **Ya existe**: necesidades en `forms_bp.py` (`POST /participants/<id>/needs`) y matching (`find_matches`, `get_community_sdv_gaps`) — el foro los referencia, no los duplica.
- **Endpoints** (propuesta): `POST /forum/posts`, `GET /forum/posts?type=&tags=`, `POST /forum/posts/<id>/close`, `GET /forum/needs→matching`.
- **Tests**: crear post, listar por tipo, cerrar, permisos (token).
- **Docs**: `frontend/` página `/foro` (M5); este hito solo API + tests.

## M3 ⏳ Talleres de Aprendizaje (`app/workshops_bp.py`)

**Qué es:** la unidad de enseñanza de CUALQUIER skill (la regla de oro: el skill se gana enseñándolo — la vacuación).

- **Tabla** `workshops` (título, skill_nodo, facilitador_id, estado `open|running|closed`, maestría mínima exigida, cupos), `workshop_enrollments` (aprendiz, estado `apprentice|advanced`), `workshop_outputs` (material de enseñanza abierto — la obra verificable).
- **Regla de oro en el motor**: para ganar el nodo de skill, el aprendiz debe (1) obra aplicada, (2) material de enseñanza publicado, (3) mentoría mínima (contada en TVI). Extensión a `maxocontracts/` (tipo `SkillNode`, `SkilledParticipant`?) o contrato flexible en `app/` con verificación por triada.
- **Endpoints**: `POST /workshops` (desde foro), `POST /workshops/<id>/enroll`, `POST /workshops/<id>/outputs`, `POST /workshops/<id>/grant-skill` (triada: facilitador + par + oráculo con veto).
- **Tests**: creación (requiere facilitador con nodo ganado), inscripción, material, concesión de skill, rechazo sin triada.

## M4 ⏳ Grupos de Solución y Células Madre (`app/groups_bp.py`)

**Qué es:** los ECEs — grupos que resuelven necesidades reales de la comunidad — y las células madre, cuyo oficio es formar otros grupos.

- **Tabla** `edu_groups` (tipo: `solution_group | mother_cell`, necesidad vinculada → `matching`, célula madre vinculada).
- **Célula madre**: cada grupo formado registra su matriz (trazabilidad fractal); la célula madre gana nodo "facilitación" al ver florecer una réplica.
- **Ya existe**: `micromax_bp.py` (household) como patrón doméstico — aquí es educativo, no se mezcla.
- **Endpoints**: `POST /groups` (solución/ madre), `POST /groups/<id>/join`, `POST /groups/<id>/needs` (vincular necesidad), `POST /groups/<id>/child` (registrar réplica).
- **Tests**: crear ambos tipos, vincular necesidad, registrar réplica.

## M5 ⏳ UI y puente años↔índice

- **Frontend** (`frontend/app/`): páginas `/foro`, `/talleres`, `/grupos` siguiendo el patrón de `guide_bp`/`guia` (API real, nada pintado).
- **Puente**: `app/sdv_analyzer.py` `SDVScore.educacion` (0-1) ↔ años del motor (`educacion_anos`); mapeo documentado (≥12 años → 1.0, lineal o umbral canónico a decidir en parlamento).
- **Docs**: `mapa_frontend_ola4.md` (+3 páginas), guía del foro en `docs/guides/`.

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
