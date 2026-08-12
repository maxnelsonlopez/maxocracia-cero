# AGENTS.md — Maxocracia-Cero

Guía para agentes de IA (y humanos) que trabajen en este repositorio. Léela antes de tocar código.

## Qué es este proyecto

**Maxocracia-Cero**: "Sistema Operativo para una Civilización Coherente". Sistema ético-económico-político
alternativo: contabilidad de la vida en vez de dinero fiduciario. Fase 2 — Sostenibilidad Económica y
MicroMaxocracia Doméstica (versión 5.6, Ola 4). Backend Flask + frontend Next.js.

Conceptos clave: **VHV** (Vector de Huella Vital [T,V,R]), **TVI** (Tiempo Vital Indexado), **SDV**
(Suelo de Dignidad Vital), **Maxo** (moneda vital), **MaxoContracts** (contratos éticos con oráculo).

## Estructura

- `app/` — Backend Flask. Blueprints por dominio: `contracts_bp.py` (131 KB, el más grande), `matching.py`
  (necesidad x oferta → borrador), `vhv_bp.py`, `tvi_bp.py`, `micromax_bp.py`, `maxo_bp.py`, `forms_bp.py`,
  `parties_bp.py`, `protection_bp.py`, `reputation_bp.py`, `resources_bp.py`, `verifier_bp.py`, `auth.py`,
  **`voting_bp.py`** (gobernanza comunitaria: propuestas, votos, delegación, parlamento de parámetros),
  **`arrivals.py`** (invitaciones y escalera de confianza N0-N1). Modelos SQLAlchemy en `models.py`
  (User, Participant, Interchange, FollowUp, VHVProduct). `create_app()` en `app/__init__.py`.
- **`app/voting_oracle.py`** — oráculo de análisis de propuestas: DeepSeek (nube) con **fallback a modelos
  locales** (hub Jan `localhost:1337`, `LOCAL_ORACLE_*`); produce VHV + axiomas + 4 opiniones, firmado
  con `engine` (T13). **No carga .env al importar** (lo hace run.py) — NO reintroducir load_dotenv ahí
  (contamina los tests).
- `maxocontracts/` — **Motor de dominio puro** (sin Flask): `action.py`, `condition.py`, `gamma_protector.py`,
  `reciprocity.py`, `sdv_validator.py`, `sdv_s_validator.py`, `ternura.py`. Lógica de contratos validable por tests.
- `frontend/` — Next.js (App Router). Páginas: `contracts/` (builder, negotiate, [id]), `matching/`,
  `vhv/`, `tvi/`, `micromax/`, `verificador/`, `pulso/`, `participar/`, `forms/`, `admin/`, `dashboard/`...
- `docs/` — teoría (`theory/`), libro (`book/libro_completo_310126.md`, 300 KB), specs (`specs/`),
  arquitectura (`architecture/`), guides, API. **`architecture/mapa_coherencia_ola4.md`**: mapa vivo
  teoría↔implementación (motor `maxocontracts/`, invariantes, blueprints) — actualizarlo en cada Ola.
  **`architecture/requisitos_fase2_ola4.md`**: re-lista de RF/NFR de la fase con backlog de conexión
  (pilares A-L, incluye votación, parlamento, atribuciones sintéticas e invitaciones).
  **`architecture/mapa_frontend_ola4.md`**: páginas → blueprints + secciones desconectadas.
  **`SESION_NEXT_PROMPT.md`**: handoff entre sesiones (estado, pendientes, prompt de continuidad).
- `tests/` — ~40 archivos pytest con `conftest.py` y `INSTRUCCIONES_TESTS.md`.
- `scripts/` — migraciones, seeds, `list_routes.py`, `local_oracle.py`, `verify_setup.py`.
- `simulator/` — Nexus Simulator (VHV interactivo). `seeds/`, `migrations/`, `data-model/`, `dashboard-spec/`.

## Cómo ejecutar

```powershell
.venv\Scripts\python.exe run.py          # Flask en http://localhost:5001 (puerto 5001)
.venv\Scripts\python.exe -m pytest       # Suite de tests (pytest.ini define SECRET_KEY y FLASK_ENV de testing)
cd frontend; npm run dev                 # Next.js (dev) — el frontend se sirve también vía Flask en producción
.venv\Scripts\python.exe scripts\list_routes.py   # Inventario de rutas de la API
```

`run.py` fuerza `SECRET_KEY`/`FLASK_ENV` de desarrollo si faltan (fallback explícito de seguridad).
El oráculo en vivo usa DeepSeek (ver `scripts/local_oracle.py` y `app/contracts_bp.py`).

## Convenciones y reglas

- **Commits**: Conventional Commits en español con scope — `feat(contracts):`, `fix(verifier):`,
  `docs(roadmap):`, `test(...)`. Uno por cambio lógico. Mira `git log --oneline` para el estilo.
- **Windows**: escribir archivos SIEMPRE con `encoding="utf-8"` (consola cp1252 corrompe la visualización;
  los archivos quedan bien si se escribe con encoding explícito). `run.py` ya fuerza utf-8 en dotenv.
- **Tests**: cada cambio funcional debe acompañarse de tests (el repo tiene cultura de tests: ~40 archivos).
- **No commitear**: `.venv/`, `node_modules/`, `.next/`, `comun.db`, `scratch/` (salvo que el cambio lo exija).
- Hay archivos de notas sueltos en la raíz (p. ej. "Finalizing Maxocracia Frontend Migration",
  "Segment 2 SDV panel analyzer") — son outputs de sesiones previas; leerlos con cautela, no son código vivo.

## Colaborar con el agente RLM (desde local_models)

El repositorio hermano `local_models` (en `C:\Users\DARKM\Documents\local_models\local_models`) expone un
**colaborador DeepSeek** con dos modos:

```powershell
# Análisis de contextos largos (archivos enormes, docs, logs) — modo RLM:
& "C:\Users\DARKM\Documents\local_models\local_models\env\Scripts\python.exe" `
  "C:\Users\DARKM\Documents\local_models\local_models\core\collaborator.py" `
  "Resume qué hace este archivo y qué rutas expone" `
  --context "app\contracts_bp.py" --quiet

# Trabajo de archivos en una copia (NUNCA sobre el código vivo): modo agente
& "C:\Users\DARKM\Documents\local_models\local_models\env\Scripts\python.exe" `
  "C:\Users\DARKM\Documents\local_models\local_models\core\collaborator.py" `
  "Tarea..." --workspace "scratch\collab" --trace "scratch\collab\trace.jsonl" --output "scratch\collab\respuesta.txt"
```

Guía completa de trabajo con RLM: `docs/GUIA_RLM_COLABORADOR.md` en el repo local_models.
**Regla de oro**: el colaborador es para *investigar/resumir/generar*; las ediciones quirúrgicas al código
vivo las hace el agente de sesión con sus tools de edición (evita reescrituras que pierden texto).
