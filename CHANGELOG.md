# Changelog

All notable changes to this project will be documented in this file.

Dates are ISO 8601 (YYYY-MM-DD). This changelog focuses on developer-facing changes: API, schema, DB seeds, and important operational notes.

## [Unreleased]

### Added - Dashboard Analytics Enhancements (2025-12-04)

**Temporal Trends Visualization:**
- Implemented `get_temporal_trends(period_days)` method in `FormsManager` for time-series analysis
- Added temporal trends section to dashboard with Chart.js line charts
- UTH mobilized over time visualization
- Exchanges per week trend chart
- Period selector buttons (7/30/90 days) for dynamic filtering

**Category Breakdown Analysis:**
- Implemented `get_category_breakdown()` method for analyzing offer/need distribution
- Tracks top offered and needed categories from participants
- Calculates match rate between available offers and existing needs
- Provides exchange types distribution

**Resolution Metrics:**
- Implemented `get_resolution_metrics()` method for effectiveness tracking
- Average resolution score calculation
- Resolution scores grouped by urgency level
- Average days to resolve (from exchange to follow-up)
- Success rate by category (resolution score >= 7)

**API Endpoints:**
- `GET /forms/dashboard/trends?period=30` - Temporal trends data
- `GET /forms/dashboard/categories` - Category breakdown analysis
- `GET /forms/dashboard/resolution` - Resolution effectiveness metrics

**Frontend Enhancements:**
- Added temporal trends section to `dashboard.html`
- Implemented Chart.js visualizations for UTH and exchanges trends
- Created period selector UI component with active state management
- Added responsive CSS styling in `dashboard.css`
- Updated `api.js` with new dashboard API methods
- Enhanced `dashboard.js` with chart rendering functions

**Testing:**
- Created comprehensive test suite (`test_dashboard_analytics.py`)
- 10 new tests covering authentication, data structure, and value ranges
- All tests passing (77/77 total project tests) ✅

### Fixed - Authentication and Schema Issues (2025-12-04)

**JWT Decorator Fix:**
- Fixed `token_required` decorator to properly pass `current_user` to decorated endpoints
- Resolved `TypeError` in forms endpoints that were missing the user parameter
- Updated all affected blueprints: `forms_bp.py`, `maxo_bp.py`, `tvi_bp.py`, `auth.py`

**Database Schema Updates:**
- Extended `interchange` table with coordination and follow-up fields:
  - `coordination_method` (TEXT): How the exchange was coordinated
  - `requires_followup` (BOOLEAN): Whether follow-up is needed
  - `followup_scheduled_date` (TIMESTAMP): When follow-up is scheduled
- Added migration script: `scripts/migrate_interchange_table.py`

**Security Test Refinements:**
- Updated security test assertions for better error message validation
- Improved password strength enforcement tests
- Enhanced sensitive information leakage detection

**Frontend Refactoring:**
- Implemented dark mode for VHV Calculator (Claude Opus)
- Centralized API calls and token management in `api.js` module
- Refactored `app.js`, `dashboard.js`, and `vhv-calculator.js` for consistency
- Improved code maintainability and reduced redundancy

**Code Quality:**
- Fixed all flake8 linting errors
- Standardized import ordering with isort
- Improved type hints and error handling

**Testing:**
- All 67 tests passing ✅
- CI/CD pipeline green 🟢

### Added - TVI (Tiempo Vital Indexado) Data Model (2025-12-02)

**Core Implementation:**
- Implemented TVI database schema (`tvi_entries` table) with strict uniqueness constraints
- Created `TVIManager` class for TVI logging and analysis (`app/tvi.py`)
- Enforced Axiom T0 (Uniqueness) with overlap detection algorithm
- Implemented 5 TVI categories: MAINTENANCE, INVESTMENT, WASTE, WORK, LEISURE

**API Endpoints:**
- `POST /tvi`: Log a time block with category and description
- `GET /tvi`: List user's time blocks with pagination
- `GET /tvi/stats`: Calculate Coeficiente de Coherencia Personal (CCP)

**CCP Calculation:**
- Formula: `CCP = (Investment + Leisure) / (Total Time - Maintenance)`
- Provides breakdown by category and discretionary time analysis

**Testing:**
- Added comprehensive test suite (`tests/test_tvi.py`)
- Tests for overlap detection (Axiom T0 enforcement)
- Tests for CCP calculation accuracy
- API integration tests with authentication

**Documentation:**
- Based on `docs/arquitectura_temporal_coherencia_vital.md`
- Implements mathematical formalization from the Temporal Architecture paper

### Added - VHV Calculator Frontend (2025-12-02)

**User Interface:**
- Complete web-based calculator at `/static/vhv-calculator.html`
- Nature-inspired design system with color-coded components (T=gradient, V=green, R=brown)
- Responsive layout for mobile, tablet, and desktop

**Features:**
- **Calculator Tab**: Interactive form with 15+ inputs for all VHV components
- **Comparison Tab**: Side-by-side product comparison, auto-sorted by Maxo price
- **Case Studies Tab**: Pre-loaded examples (Huevo Ético vs Industrial)
- **Parameters Tab**: Display of current α, β, γ, δ with axiom validation
- **Chart.js Integration**: Visual doughnut chart showing price breakdown
- **Educational Tooltips**: Contextual help throughout the interface
- **"Cargar Ejemplo" Button**: Quick-start with Huevo Ético case study
- **Save Product**: Persist calculations to database

**Technical Stack:**
- Vanilla JavaScript (no framework dependencies)
- Chart.js 4.4.0 for data visualization
- CSS Grid/Flexbox for responsive layout
- Full API integration with VHV backend

**Files:**
- `app/static/css/vhv.css` (470 lines) - Complete design system
- `app/static/vhv-calculator.html` (300+ lines) - Main interface
- `app/static/js/vhv-calculator.js` (500+ lines) - Logic and API integration
- `app/static/index.html` (modified) - Added navigation link

**For Cohorte Cero:**
- Ready for Mes 2: "Contabilidad Existencial"
- Enables experimentation with ethical product pricing
- Visual comparison of ethical vs conventional options
- Parameter calibration interface for "Calibración del Valor" ritual

### Added - Formularios Operativos para Red de Apoyo (2025-12-03)

**Sistema Completo de Gestión de Intercambios:**
- 3 formularios diseñados y documentados para Google Forms
- Especificaciones completas listas para implementación

**Formulario CERO: Inscripción** (`formularios/formulario_CERO_inscripcion.md`)
- 17 preguntas estructuradas
- Captura de ofertas y necesidades
- Valores personales y dimensiones humanas
- Información de contacto multi-canal

**Formulario A: Registro de Intercambio** (`formularios/formulario_A_registro_intercambio.md`)
- 16 preguntas + análisis automático
- Métricas Maxocráticas: UTH, URF, valor económico
- Sistema de urgencias (Alta/Media/Baja)
- Tracking de reciprocidad y resolución
- Dimensiones humanas atendidas

**Formulario B: Reporte de Seguimiento** (`formularios/formulario_B_reporte_seguimiento.md`)
- 18 preguntas + sistema de priorización
- Detección de nuevas necesidades y ofertas
- Evaluación de salud emocional
- Sistema de alertas (🔴 Alta, 🟡 Media, 🟢 Baja)
- Programación de seguimientos

**Métricas que Generan:**
- UTH total movilizado en la red
- Tasa de resolución de necesidades
- Flujo de red (nodos hub, clusters)
- Detección temprana de crisis
- Evolución de situaciones personales

**Diseño:**
- Campos obligatorios mínimos (no abrumadores)
- Métricas opcionales (recoger lo que se pueda)
- Lenguaje accesible con emojis
- Compatible con futuro sistema Maxo
- Escalable (de facilitador único a auto-reporte)

### Added - Documentación Teórica Compilada (2025-12-03)

**Brochure de Maxocracia** (`docs/maxocracia_brochure.md`)
- 376 líneas de introducción accesible al sistema
- Explica los 8 Axiomas de la Verdad
- Detalla el Maxo y las 3 unidades (UVC, UTH, URF)
- Teoría de juegos y equilibrio maxocrático
- Estado actual de la Red de Apoyo (11 personas, Bogotá)
- FAQ: ¿Es comunismo/socialismo/capitalismo?
- Cómo participar y contribuir

**Matemáticas de Maxocracia Compiladas** (`docs/matematicas_maxocracia_compiladas.md`)
- 982 líneas de formalización matemática completa
- Los 8 Axiomas de la Verdad (Código de Coherencia)
- Los 13 Axiomas Temporales (T0-T13)
- Axiomas Vitales (V0-V8)
- Principios de Recursos Finitos (R1-R3)
- Ecuaciones: TVI, TTVI, CCP, Trascendencia, VHV
- Casos de aplicación (accidente de puente, reunión inútil, protesta)
- Sistema de Coherencia Armónica (SCA)
- Mecanismos anti-acaparamiento

**Propósito:**
- Centralizar toda la base matemática del proyecto
- Facilitar onboarding de nuevos colaboradores
- Referencia rápida para implementadores
- Base para papers académicos futuros

---

## 2025-12-02 — Calculadora VHV para Cohorte Cero

### Añadido
- **Calculadora funcional del Vector de Huella Vital (VHV)** basada en `paper_formalizacion_matematica_maxo.txt`
- **Base de datos**:
  - Tabla `vhv_parameters`: Almacena parámetros α, β, γ, δ con restricciones axiomáticas mediante CHECK constraints
  - Tabla `vhv_products`: Catálogo de productos con desglose completo VHV = [T, V, R]
  - Tabla `vhv_calculations`: Historial de cálculos para auditoría y trazabilidad
  - INSERT inicial de parámetros DEFAULT basados en el paper (α=100, β=2000, γ=1.0, δ=100)
- **Módulo `app/vhv_calculator.py`**:
  - Clase `VHVCalculator` con implementación matemática completa
  - Cálculo de componente T (Tiempo Vital Indexado): directos + heredados + futuros
  - Cálculo de componente V (Unidades Vida Consumidas): con factores F_consciencia, F_sufrimiento, F_abundancia, F_rareza
  - Cálculo de componente R (Recursos Finitos): minerales, agua, petróleo, tierra ponderados por FRG × CS
  - Fórmula de valoración: `Precio_Maxos = α·T + β·V^γ + δ·R`
  - Validación de restricciones axiomáticas (α > 0, β > 0, γ ≥ 1, δ ≥ 0)
  - Casos de estudio precargados: Huevo Ético vs Huevo Industrial del paper
- **API Blueprint `app/vhv_bp.py`**:
  - `POST /vhv/calculate`: Calcular VHV de un producto con opción de guardar
  - `GET /vhv/products`: Listar productos con paginación y filtro por categoría
  - `GET /vhv/products/<id>`: Detalles completos de un producto
  - `GET /vhv/compare?ids=1,2`: Comparar múltiples productos
  - `GET /vhv/parameters`: Obtener parámetros actuales de valoración
  - `PUT /vhv/parameters`: Actualizar parámetros (requiere autenticación, valida axiomas)
  - `GET /vhv/case-studies`: Obtener casos de estudio del paper
- **Testing `tests/test_vhv_calculator.py`**:
  - 8 tests de lógica de cálculo (componentes T, V, R y precio Maxo)
  - 4 tests de validación de axiomas (restricciones α, β, γ, δ)
  - 3 tests de casos de estudio del paper (huevos ético vs industrial)
  - 8 tests de API endpoints
  - Test de autenticación requerida para actualización de parámetros
  - **Total: 19/19 tests pasando** ✅

### Verificado
- Suite completa de tests: **19/19 pasando** (100%)
- Casos de estudio validan mecanismo de penalización por sufrimiento:
  - Industrial (F_sufrimiento=25) genera contribución vida 10x mayor que ético (F_sufrimiento=1.1)
  - ✅ **Validación clave del MVP**: Factor de sufrimiento impacta el precio correctamente
- Servidor arranca correctamente con schema VHV inicializado
- Parámetros default cargados automáticamente
- Restricciones axiomáticas funcionan en DB (CHECK constraints) y en API (validación programática)
- Endpoint de actualización de parámetros requiere autenticación y valida axiomas

### Notas para Cohorte Cero
- Calculadora lista para Mes 2: "Contabilidad Existencial"
- Casos de estudio precargados facilitan experimentación
- Parámetros α, β, γ, δ son calibrables durante el ritual "Calibración del Valor"
- Historial completo de cálculos permite retrospectiva en Mes 3
- API `/vhv/case-studies` provee ejemplos inmediatos para aprendizaje

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/),
y este proyecto adhiere a [Versionado Semántico](https://semver.org/spec/v2.0.0.html).

## [No publicado]

### Añadido
- Configuración inicial de GitHub Actions para CI/CD
  - Ejecución automática de pruebas unitarias
  - Análisis estático de código con flake8, black, isort y mypy
  - Generación de documentación con Sphinx
  - Integración con Codecov para cobertura de código
  - Workflow para ejecución manual

### Cambiado
- Mejorada la estructura del proyecto con separación de dependencias principales y de desarrollo
- Actualizado el README.md con instrucciones de configuración del entorno de desarrollo
- Actualizado `IMPLEMENTACION_FLASK_PLAN.md` con estado actual del proyecto post-auditoría
- Actualizado `CONTRIBUTING.md` con instrucciones para herramientas de calidad de código

### Documentación
- **Nuevo**: Creado `DISENO_IMPLEMENTACION_FUTURA.md` (v2.0) - Roadmap completo de implementación
- **Nuevo**: Creado `TAREAS_PENDIENTES_IMPLEMENTACION.md` - Lista exhaustiva de tareas por fase
- **Nuevo**: Copiado `DOCUMENTATION_REVIEW.md` a carpeta docs/
- Revisión completa de documentación técnica y filosófica
- **Integración de 10 documentos fundamentales** en documentación del proyecto:
  - **Paper 1 (Fundacional)**: `Paper Maxocracia ChatGPT Scholar AI.txt` - 8 Axiomas de la Verdad y base teórica completa
  - **Paper 2 (Temporal)**: `arquitectura_temporal_coherencia_vital.md` (DOI: 10.5281/zenodo.17526611) - 13 Axiomas Temporales
  - **Paper 3 (Aplicado)**: `tercer_paper_ontometria_vital_huevo.md` - Ontometría Vital práctica
  - **Doc 4 (SDV-H)**: `SDV-H_Suelo_Dignidad_Vital_Humanos.txt` - 7 dimensiones de dignidad humana (123+ fuentes)
  - **Doc 5 (EVV)**: `EVV_estandar_final_v1.txt` - Estándar ISO-style para VHV con blockchain
  - **Doc 6 (Sintético)**: `oraculos_dinamicos_reino_sintetico_arquitectura.md` - IAs con validación axiomática 24/7
  - **Doc 7 (Humano)**: `oraculos_dinamicos_humanos_arquitectura.md` - Participación humana con anti-sesgo
  - **Doc 8 (Métricas)**: `metricas_detalle_kpis_oraculos_dinamicos.md` - 40+ KPIs para optimización
  - **Doc 9 (Matemática)**: `paper_formalizacion_matematica_maxo.txt` - Fórmula completa y casos de estudio cuantificados
  - **Doc 10 (Experimental)**: `playbook_cohorte_cero.txt` - Experimento Bogotá (11 personas, 90 días, $50 USD)
- Identificación de brecha entre teoría (TVI/VHV/SDV) e implementación actual
- Documentación de jerarquía conceptual completa: Axiomas → Especificaciones → Experimento
- Creado diagrama de flujo conceptual completo (Papers → Especificaciones → Cohorte Cero → Evidencia)
- **Prioridad establecida**: Cohorte Cero como Fase 0 (validación experimental)

### Corregido
- Corregidos problemas de importación en los tests
- Ajustes en la configuración de la base de datos para pruebas
- **Crítico**: Corregido error de sintaxis en `seeds/seed_demo.py` que impedía la inicialización de la base de datos
- Eliminadas importaciones no utilizadas en `app/auth.py`, `app/__init__.py` y tests
- Estandarizado el estilo de código con `black` e `isort`
- Añadida configuración faltante para linters (`pyproject.toml`, `.flake8`)
- Añadida dependencia crítica `pyjwt` a `requirements.txt`

## [0.1.0] - 2025-01-01
### Añadido
- Versión inicial del proyecto
- API básica con autenticación JWT
- Sistema de interacciones con seguimiento de VHV
- Documentación inicial del proyecto
