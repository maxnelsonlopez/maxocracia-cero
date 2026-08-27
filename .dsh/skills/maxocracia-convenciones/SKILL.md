---
name: maxocracia-convenciones
description: Usar cuando vayas a trabajar en el repositorio Maxocracia-Cero — antes de tocar código, para entender su estructura (backend Flask app/, motor de dominio maxocontracts/, frontend Next.js, docs/), aplicar las reglas del proyecto (UTF-8, Conventional Commits en español, tests obligatorios, mapas de coherencia) y ejecutar la suite y los comandos habituales.
---

# Convenciones del proyecto Maxocracia-Cero

**Maxocracia-Cero** — "Sistema Operativo para una Civilización Coherente": sistema ético-económico-político alternativo, contabilidad de la vida en vez de dinero fiduciario. Fase 2 — Sostenibilidad Económica y MicroMaxocracia Doméstica (v5.6, Ola 4). Este repo es el legado de Max: trata cada edición con el máximo cuidado por la coherencia teoría↔código.

Consejos núcleo: **VHV** (Vector de Huella Vital [T,V,R]), **TVI** (Tiempo Vital Indexado), **SDV** (Suelo de Dignidad Vital), **Maxo** (moneda vital), **MaxoContracts** (contratos éticos con oráculo).

## Mapa del repositorio

| Capa | Ruta | Qué contiene |
|---|---|---|
| Backend Flask | `app/` | Blueprints por dominio: `contracts_bp.py` (el más grande), `matching.py` (necesidad×oferta→borrador), `vhv_bp.py`, `tvi_bp.py`, `micromax_bp.py`, `maxo_bp.py`, `forms_bp.py`, `parties_bp.py`, `protection_bp.py`, `reputation_bp.py`, `resources_bp.py`, `verifier_bp.py`, `voting_bp.py` (gobernanza), `arrivals.py` (invitaciones N0-N1), `guide_bp.py` (Guía/onboarding) |
| Modelos | `app/models.py`, `app/__init__.py` | SQLAlchemy + `create_app()` y registro de blueprints (`register_blueprint` + helpers `init_*_tables`) |
| Oráculo | `app/voting_oracle.py` | DeepSeek (nube) con fallback a modelos locales (Jan `localhost:1337`, `LOCAL_ORACLE_*`); produce VHV + axiomas + 4 opiniones firmadas con `engine` (T13). **No carga .env al importar** — NO reintroducir `load_dotenv` ahí (contamina los tests) |
| Motor de dominio | `maxocontracts/` | Lógica pura validable por tests: `action.py`, `condition.py`, `gamma_protector.py`, `reciprocity.py`, `sdv_validator.py`, `sdv_s_validator.py`, `ternura.py`, `core/axioms.py` (INV1-4, INV2-S, T9-T17), `core/types.py` |
| Frontend | `frontend/` | Next.js App Router: `contracts/`, `matching/`, `vhv/`, `tvi/`, `micromax/`, `verificador/`, `pulso/`, `participar/`, `forms/`, `admin/`, `dashboard/`, `guia/` |
| Docs | `docs/` | `theory/`, `book/edicion_3_dinamica/` (libro 312 KB), `specs/`, `architecture/`, `guides/`, `design/` |
| Tests | `tests/` | ~40 archivos pytest + `conftest.py` + `INSTRUCCIONES_TESTS.md`; motor en `tests/test_maxocontracts/` (286/286) |
| Simulator | `simulator/` | Nexus Simulator (VHV interactivo) |

## Comandos

```powershell
.venv\Scripts\python.exe run.py                      # Flask en http://localhost:5001
.venv\Scripts\python.exe -m pytest                   # Suite (pytest.ini define SECRET_KEY/FLASK_ENV testing)
cd frontend; npm run dev                             # Next.js dev
.venv\Scripts\python.exe scripts\list_routes.py      # Inventario de rutas API
.venv\Scripts\python.exe scripts\verify_setup.py     # Verificación de entorno
```

## Reglas duras

1. **UTF-8 siempre**: escribir archivos con `encoding="utf-8"` explícito (consola Windows cp1252 corrompe la visualización; los archivos quedan bien si se escribe explícito).
2. **Commits**: Conventional Commits en español con scope — `feat(contracts):`, `fix(verifier):`, `docs(roadmap):`, `test(...)`. Uno por cambio lógico. Mira `git log --oneline` para el estilo.
3. **Tests**: cada cambio funcional se acompaña de tests (cultura del repo: ~40 archivos).
4. **No commitear**: `.venv/`, `node_modules/`, `.next/`, `comun.db`, `scratch/`.
5. **Mapas vivos**: en cada Ola, actualiza `docs/architecture/mapa_coherencia_ola4.md` (teoría↔implementación, invariantes, blueprints). Complementos: `requisitos_fase2_ola4.md` (RF/NFR, pilares A-L), `mapa_frontend_ola4.md` (páginas→blueprints), `mapa_trazabilidad_canonica.md`.
6. **Handoff**: al terminar, actualiza `SESION_NEXT_PROMPT.md` (ver skill `maxocracia-handoff`).

## Colaborador RLM (investigar, no editar)

El repo hermano `local_models` expone un colaborador DeepSeek con dos modos: análisis de contextos largos (`--context archivo`) y trabajo en copias (`--workspace scratch\collab`). **Regla de oro**: el colaborador es para investigar/resumir/generar; las ediciones quirúrgicas al código vivo las hace el agente de sesión con sus tools de edición (evita reescrituras que pierden texto). Guía: `docs/GUIA_RLM_COLABORADOR.md`.

## Puntos de atención

- Archivos de notas sueltos en la raíz ("Finalizing Maxocracia Frontend Migration", "Segment 2 SDV panel analyzer", etc.) son outputs de sesiones previas: leer con cautela, no son código vivo.
- `run.py` fuerza `SECRET_KEY`/`FLASK_ENV` de desarrollo si faltan (fallback explícito de seguridad).
- Verificación determinista tras análisis RLM: grep/reconsulta manual.
- El oráculo en vivo usa DeepSeek; ver `scripts/local_oracle.py`.

## Checklist de sesión

1. Lee `AGENTS.md` y esta skill. 2. Ubica el dominio en `app/__init__.py` (blueprint) y su test. 3. Si toca conceptos: teoría primero (`docs/theory/` o `docs/book/`). 4. Implementa con tests. 5. `pytest` completo en verde. 6. Commit convencional en español. 7. Si cambió teoría↔implementación, actualiza los mapas. 8. Actualiza `SESION_NEXT_PROMPT.md`.
