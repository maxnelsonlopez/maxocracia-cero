# Tareas Pendientes - Maxocracia-Cero

**Última actualización:** 2026-05-06 (Sesión Antigravity Pro)

---

## 🔥 Prioridad Alta

### MaxoContracts MVP (Q1 2026) - NUEVO ✨

**Objetivo**: Validar contratos inteligentes éticos en Cohorte Cero (50+ contratos en 90 días)

- [x] **Semana 1-2: Especificación (Enero 22 - Febrero 5)** ✅ COMPLETADA
  - [x] **Implementar Persistencia en DB** (Completado 2026-01-23)
    - [x] Tablas en `schema.sql` para contratos y términos
    - [x] CRUD persistente en `app/contracts_bp.py`
    - [x] Refactorización Wellness (limpieza terminológica)
    - [x] Suite de tests de persistencia
  - [x] **Consolidar Libro Edición 3.3** (Completado 2026-02-04)
    - [x] Estructura plana de capítulos
    - [x] Libro completo en MD y DOCX
    - [x] Actualizar README.md a v3.3
  - [x] **Diseñar UI drag-and-drop (wireframes)** (Completado 2026-01-23)
    - [x] Especificaciones de UI en `docs/design/`
    - [x] Prototipo funcional en `app/static/contract-builder-mock.html`
    - [x] Estilos Glassmorphism en `app/static/css/contracts.css`
  - [x] **Definir API contracts para oráculos** (Completado 2026-01-23)
    - [x] Especificación API en `docs/specs/ORACLE_API_SPEC.md`
    - [x] Refactorización de `maxocontracts/oracles` (Verdict object)
    - [x] Actualización de `SyntheticOracle` y `app/contracts_bp.py`
  - **Entregables**: ✅ Persistencia SQL, ✅ Libro v3.3, ✅ Wireframes y API Oráculos listos

- [ ] **Semana 3-4: Prototipo (Febrero 6-19)**
  - [ ] Codificar 3 bloques básicos + tests
  - [ ] Desarrollar app MVP en React + Next.js
  - [ ] Deployar primeros contratos en Base Sepolia testnet
  - **Entregables**: 3 bloques funcionales, app MVP, 3 contratos de prueba

- [ ] **Semana 5-8: Validación (Febrero 20 - Marzo 19)**
  - [ ] Completar 5 bloques + auditoría
  - [ ] Ejecutar 50+ contratos en Cohorte Cero
    - [ ] 20 contratos de aseo compartido
    - [ ] 15 contratos de préstamos sin usura
    - [ ] 15 contratos de comidas colaborativas
  - [ ] Implementar dashboard de métricas (γ, SDV, NPS)
  - **Entregables**: 5 bloques completos, 50+ contratos ejecutados, dashboard

- [ ] **Semana 9-12: Análisis (Marzo 20 - Abril 16)**
  - [ ] Analizar 50+ casos (patrones, γ promedio, retractaciones)
  - [ ] Generar **Informe de Hallazgos v1.0**
  - [ ] Publicar kit open-source en GitHub
  - **Entregables**: Informe 30-50 páginas, repo público, 3 casos de estudio

**Stack**: React 18, Next.js 14, Solidity 0.8.20, Base L2, Claude API  
**Presupuesto**: $5,000-10,000 USD  
**Métricas de Éxito**: ≥50 contratos, γ>1.2, adopción ≥80%, NPS>70

### MicroMaxocracia Apps (Q2 2026) - NUEVO ✨

**Objetivo**: Crear herramientas digitales para 30 hogares piloto (90 días)

- [ ] **Mes 1: Diseño (Abril - Mayo)**
  - [ ] Diseñar 3 apps core
    - [ ] **Ledger App**: Registro VHV doméstico
    - [ ] **Auditoría App**: Rituales estructurados
    - [ ] **Desintoxicación App**: Monitoreo ICE/IDB/IDP
  - [ ] Prototipar Ledger App (MVP)
  - [ ] Testear con 3 hogares beta
  - **Entregables**: Diseños UI/UX, prototipo funcional, feedback beta

- [x] **Migración Frontend Unificado (Segmento 1: Formularios)** (Completado 2026-05-08) ✅
  - [x] Crear componentes base `FormWizard`, `FormStep`, `FormUI`
  - [x] Migrar Formulario CERO (Inscripción) a `/forms/cero`
  - [x] Migrar Formulario de Intercambio a `/forms/exchange`
  - [x] Migrar Formulario de Seguimiento a `/forms/follow-up`
  - [x] Actualizar navegación global

- [x] **Migración Frontend Unificado (Segmento 2: VHV & TVI)** (Completado 2026-05-08) ✅
  - [x] Migrar Calculadora VHV interactiva
  - [x] Implementar visualizaciones de TVI con Chart.js
  - [x] Integrar comparador de productos

- [x] **Migración Frontend Unificado (Segmento 3: Admin Dashboard & Red)** (Completado 2026-05-08) ✅
  - [x] Consolidar métricas de red en `/admin/dashboard`
  - [x] Implementar visualización de Grafos de Intercambio (React Flow)
  - [x] Panel de filtros avanzados de red
  - [x] Exportación de reportes de impacto (UI Base)

- [x] **Migración Frontend Unificado (Segmento 4: Unificación e Integración)** (Completado 2026-05-11) ✅
  - [x] Build final unificado y despliegue a `static/dist`
  - [x] Limpieza de archivos legados (.html, .js antiguos)
  - [x] Optimización de SPA routing en Flask

- [ ] **Mes 2-3: Desarrollo (Mayo - Julio)**
  - [ ] Desarrollar 3 apps completas (React Native)
  - [ ] Reclutar 30 hogares piloto
    - [ ] 10 parejas sin hijos
    - [ ] 10 familias con niños pequeños
    - [ ] 5 familias con niños mayores
    - [ ] 3 hogares multigeneracionales
    - [ ] 2 configuraciones no tradicionales
  - [ ] Ejecutar validación de 90 días (niveles 0→1→2→3)
  - **Entregables**: 3 apps desplegadas, 30 hogares activos, datos 90 días

- [ ] **Mes 4: Análisis (Julio - Agosto)**
  - [ ] Analizar datos de 30 hogares
    - [ ] Satisfacción relacional (+15 pts meta)
    - [ ] Reducción brecha VHV (30% meta)
    - [ ] Precisión estimaciones (±15% meta)
  - [ ] Generar **Informe MicroMaxocracia v1.0**
  - [ ] Preparar escalamiento a 100 hogares
  - **Entregables**: Informe, apps v2.0 optimizadas, plan escalamiento

**Stack**: React Native, Flask backend, PostgreSQL, Mixpanel  
**Presupuesto**: $8,000-12,000 USD  
**Métricas de Éxito**: ≥30 hogares, +15pts satisfacción, 30% reducción brecha

---

## 🔥 Prioridad Alta (Continuación)

### Cohorte Cero - Red de Apoyo

- [x] **Implementar formularios interactivos (Wizard) y Lookups**
  - Completado: 2026-01-16
  - Implementados como formularios multi-paso con validación:
    - Formulario CERO (Inscripción)
    - Formulario A (Registro de Intercambio)
    - Formulario B (Reporte de Seguimiento)
  - **Búsqueda Dinámica**: Reemplazados IDs estáticos por lookup en tiempo real de participantes e intercambios.
  - Integrados en el Dashboard web con estética glassmorphism.
  - Impacto: Operacional - mejora drástica en UX y precisión de datos para Cohorte Cero.

- [x] **Crear dashboard de análisis de intercambios**
  - Completado: 2025-12-04
  - Implementado como dashboard web con Chart.js
  - Métricas: UTH movilizado, tasa de resolución, flujo de red, tendencias temporales
  - Visualizaciones: Gráficos de línea, donas, barras, tablas de red
  - Nuevos endpoints: /trends, /categories, /resolution
  - Impacto: Seguimiento en tiempo real y análisis de tendencias

### Seguridad y Calidad

- [x] **Actualizar seeds con contraseñas hasheadas**
  - Completado: 2025-12-02
  - Archivo: `scripts/seed_data.py`

- [x] **Corregir bugs críticos en autenticación y esquema**
  - Completado: 2025-12-04
  - JWT decorator ahora pasa correctamente `current_user`
  - Tabla `interchange` extendida con campos de coordinación y seguimiento
  - Todos los tests pasando (67/67) ✅

- [x] **Aumentar cobertura de tests**
  - **Estado actual:** ✅ ~150+ tests pasando (aumentado de 120)
  - **Cobertura estimada:** ~80-85% (aumentado de ~70-75%)
  - **Completado:** 2025-12-16 (mejora comprehensiva por Auto/Cursor)
  - **Tests añadidos:**
    - `test_users.py` (12 tests) - Cobertura completa de `app/users.py`
    - `test_utils.py` (10 tests) - Cobertura completa de `app/utils.py`
    - `test_forms_manager_comprehensive.py` (29 tests) - Tests exhaustivos para `FormsManager`
    - `test_forms_bp_comprehensive.py` (13 tests) - Tests exhaustivos para endpoints de `forms_bp.py`
    - `test_vhv_bp_comprehensive.py` (15 tests) - Tests exhaustivos para endpoints de `vhv_bp.py`
    - `test_maxo_edgecases_comprehensive.py` (8 tests) - Tests adicionales para edge cases de `maxo.py`
  - **Documentación:**
    - `tests/ANALISIS_COBERTURA.md` - Análisis detallado de gaps y prioridades
    - `tests/INSTRUCCIONES_TESTS.md` - Guía de ejecución y verificación
  - **Cobertura mejorada:**
    - Endpoints de `forms_bp.py`: ~30% → ~85%
    - Endpoints de `vhv_bp.py`: ~50% → ~85%
    - Edge cases de `maxo.py`: ~60% → ~80%
  - **Próximos pasos:**
    - Tests de concurrencia en TVI
    - Tests de integración end-to-end
    - Tests de performance para consultas complejas

---

## 📊 Prioridad Media

### Documentación

- [x] **Actualizar README.md**
  - Completado: 2025-12-03
  - Refleja estado actual del proyecto

- [x] **Documentar VHV Calculator en API.md**
  - Completado: 2025-12-02
  - Incluye todos los endpoints y ejemplos

- [x] **Documentar TVI en API.md**
  - Completado: 2025-12-02
  - Incluye fórmulas y casos de uso

- [ ] **Crear tutoriales para usuarios**
  - Tutorial: Cómo usar la Calculadora VHV
  - Tutorial: Cómo registrar tu tiempo (TVI)
  - Tutorial: Cómo interpretar tu CCP
  - Ubicación sugerida: `docs/tutoriales/`

### Mejoras de Código

- [ ] **Optimizar consultas de base de datos**
  - Archivos: `app/vhv_bp.py`, `app/tvi.py`
  - Añadir índices para queries frecuentes
  - Implementar caching para parámetros VHV
  - Impacto: Performance

- [x] **Refactorizar lógica de crédito de Maxo**
  - Archivos: `app/maxo.py`
  - Alinear con fórmulas del paper
  - Documentar reglas de negocio
  - Impacto: Mantenibilidad

---

## 🎨 Prioridad Baja

### UI/UX

- [x] **Añadir modo oscuro y UI Shell unificado**
  - Completado: 2026-01-16
  - Implementado `ui-shell.js` con sidebar dinámico y toggle de tema
  - Aplicado glassmorphism moderno en todas las páginas
  - Implementado por Antigravity (Gemini)

- [ ] **Mejorar diseño responsive de Calculadora VHV**
  - Archivo: `app/static/css/vhv.css`
  - Optimizar para móviles
  - Mejorar accesibilidad (ARIA labels)

- [x] **Añadir animaciones y feedback visual**
  - Completado: 2026-01-16
  - Animaciones en resultados VHV y transiciones de wizard
  - Feedback visual al guardar productos

### Optimización

- [ ] **Implementar lazy loading en frontend**
  - Cargar case studies solo cuando se accede a la pestaña
  - Optimizar carga de Chart.js
  - Impacto: Performance inicial

- [ ] **Añadir service worker para PWA**
  - Permitir uso offline de la calculadora
  - Cache de parámetros VHV
  - Impacto: Experiencia de usuario

---

## 🚀 Futuro (Fase 2-3)

### Blockchain Integration

- [ ] **Diseñar smart contracts para TVIs**
  - Tecnología: Polygon (Ethereum L2)
  - TVIs como NFTs (ERC-721 modificado)
  - Registro inmutable de VHV
  - Timeframe: 12-18 meses

- [ ] **Implementar Oráculo Dinámico**
  - Chainlink para datos externos
  - Validación de parámetros α, β, γ, δ
  - Consenso híbrido (humano + IA)
  - Timeframe: 18-24 meses

### Escalabilidad

- [ ] **Migración a arquitectura de microservicios**
  - Referencia: `docs/legacy/diseno-tecnico-comun-go.md`
  - Separar VHV, TVI, Auth en servicios independientes
  - Implementar en Go para performance
  - Timeframe: 24+ meses

---

## ✅ Completadas Recientemente

### Mayo 2026

- [x] **Auditoría, Estabilización y Tipado Estricto del Frontend** (2026-05-19)
  - Corrección de bugs de sesión en local storage centralizando el uso de `mc_access_token`.
  - Desacoplamiento de hosts y estandarización de API en Next.js con el wrapper `apiFetch` y la constante `API_URL`.
  - Refactorización de componentes para React 19 eliminando efectos de renderizado en cascada y previniendo loops circulares.
  - Implementación de placeholders interactivos premium con glassmorphism para `/admin/subscriptions` y `/admin/settings`.
  - Reemplazo completo de tipos `any` con tipado estricto e interfaces sólidas en todas las vistas de administración (`dashboard`, `network`, `reports`, `sdv`, `comparison`, `parameters`).
  - Verificación exitosa mediante `npm run lint`, `npx tsc --noEmit` y compilación de producción con Next.js.
  - Responsable: Antigravity (Gemini).

- [x] **Reparación Integral de Frontend (Next.js 16 + Tailwind v4)** (2026-05-06)
  - Corrección de sintaxis de Tailwind v4 en `globals.css` (@import).
  - Ajuste de cabecera Content-Security-Policy (CSP) para permitir hidratación.
  - Relajación de Rate Limiter (5000/hr) para activos de Next.js en desarrollo.
  - Sincronización de bundle unificada mediante `scripts/build_front.py`.
  - **Implementación funcional de Contract Builder visual (React Flow)**.
  - Integración de validación axiomática en tiempo real con Flask API.
  - Responsable: Antigravity.

- [x] **Interactividad en Bloques Visuales de Contratos** (2026-05-06)
  - Implementación de `useReactFlow` en Nodos Personalizados para el Visual Builder.
  - Sincronización de inputs de nodos (costo VHV, Condiciones, Oráculos, Reciprocidad) con el backend.
  - Parsing dinámico de variables VHV en la ruta `validate_graph` de Flask.
  - Responsable: Antigravity.

### Diciembre 2025

- [x] **Refactorización Lógica Maxo (Fórmula VHV Polinómica)** (2025-12-10)
  - Implementación de fórmula rigurosa: `Precio = α·T + β·V^γ + δ·R·(FRG × CS)`
  - Lectura dinámica de parámetros desde BD
  - Nuevos tests de valoración exponencial
  - Actualización de `app/maxo.py` y `docs/API.md`

- [x] **Corrección de Formularios y CSP** (2025-12-10)
  - Solución a bloqueo de scripts inline por Content Security Policy
  - Extracción de lógica a archivos JS externos para `form-exchange` y `form-followup`
  - Verificación de flujo de envío de datos

- [x] **Refactorizar Frontend API** (2025-12-04)
  - Centralización de API calls en módulo `api.js`
  - Gestión consistente de tokens
  - Refactorización de `app.js`, `dashboard.js`, `vhv-calculator.js`
  - Implementación de dark mode

- [x] **Corregir bugs críticos** (2025-12-04)
  - JWT decorator fix para pasar `current_user`
  - Extensión de tabla `interchange` con campos de seguimiento
  - 67/67 tests pasando, CI/CD en verde

- [x] **Implementar VHV Calculator Frontend** (2025-12-02)
  - 4 pestañas funcionales
  - Chart.js integration
  - Design system completo
  - Archivos: `app/static/vhv-calculator.html`, `css/vhv.css`, `js/vhv-calculator.js`

- [x] **Implementar TVI Data Model** (2025-12-02)
  - Base de datos con overlap detection
  - API endpoints (/tvi, /tvi/stats)
  - Cálculo de CCP
  - Tests comprehensivos
  - Archivos: `app/tvi.py`, `app/tvi_bp.py`, `tests/test_tvi.py`

- [x] **Actualizar formularios operativos** (2025-12-03)
  - Formulario CERO: 17 preguntas estructuradas
  - Formulario A: 16 preguntas + métricas Maxocráticas
  - Formulario B: 18 preguntas + sistema de priorización
  - Archivos: `formularios/*.md`

- [x] **Crear documentación teórica compilada** (2025-12-03)
  - Brochure de Maxocracia (376 líneas)
  - Matemáticas compiladas (982 líneas)
  - Archivos: `docs/maxocracia_brochure.md`, `docs/matematicas_maxocracia_compiladas.md`

### Octubre-Noviembre 2025

- [x] **Implementar VHV Calculator Backend** (2025-12-02)
  - Clase VHVCalculator con todas las fórmulas
  - API Blueprint completo
  - 19 tests pasando
  - Casos de estudio del paper

- [x] **Configurar CI/CD** (2025-11-XX)
  - GitHub Actions con pytest, flake8, mypy, black, isort
  - 67 tests pasando
  - Archivo: `.github/workflows/ci.yml`

- [x] **Corregir pruebas de validación de contraseñas** (2025-10-21)
  - Archivos: `app/validators.py`, `tests/test_input_validation.py`

- [x] **Corregir pruebas de rate limiting** (2025-10-21)
  - Archivos: `tests/test_rate_limiting.py`, `app/limiter.py`

---

## 📝 Cómo Contribuir

1. **Revisa esta lista** y elige una tarea que te interese
2. **Comenta en el issue** correspondiente (o crea uno si no existe)
3. **Crea una rama**: `feature/descripcion-corta` o `fix/descripcion-corta`
4. **Ejecuta los tests** antes de hacer commit
5. **Envía un Pull Request** con descripción clara

### Convenciones

- **Commits**: Usa conventional commits (`feat:`, `fix:`, `docs:`, etc.)
- **Tests**: Añade tests para toda nueva funcionalidad
- **Docs**: Actualiza documentación relevante
- **Style**: Ejecuta `black .` y `isort .` antes de commit

---

## 🎯 Roadmap General

**Q1 2026:** MaxoContracts MVP + Cohorte Cero validación (50+ contratos)  
**Q2 2026:** MicroMaxocracia Apps + 30 hogares piloto (90 días)  
**Q3 2026:** Análisis de datos, refinamiento de fórmulas, escalamiento  
**Q4 2026:** Integración completa de 4 capas, preparación mainnet  
**2027+:** Expansión a 100 cohortes + 1,000 hogares + blockchain mainnet

---

*Para más detalles sobre la visión a largo plazo, ver [docs/project/TAREAS_PENDIENTES_IMPLEMENTACION.md](docs/project/TAREAS_PENDIENTES_IMPLEMENTACION.md)*
