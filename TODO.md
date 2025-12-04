# Tareas Pendientes - Maxocracia-Cero

**Última actualización:** 2025-12-03

---

## 🔥 Prioridad Alta

### Cohorte Cero - Red de Apoyo

- [ ] **Implementar formularios en Google Forms**
  - Archivos de referencia: `formularios/*.md`
  - Crear 3 formularios:
    - Formulario CERO (Inscripción)
    - Formulario A (Registro de Intercambio)
    - Formulario B (Reporte de Seguimiento)
  - Compartir links con participantes actuales
  - Impacto: Operacional - crítico para Cohorte Cero

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

- [ ] **Aumentar cobertura de tests**
  - **Estado actual:** ✅ 77/77 tests pasando
  - Objetivo: 80%+ cobertura
  - Áreas prioritarias:
    - Tests de integración para formularios
    - Tests de edge cases en VHV Calculator
    - Tests de concurrencia en TVI

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

- [ ] **Refactorizar lógica de crédito de Maxo**
  - Archivos: `app/services/maxo_service.py`
  - Alinear con fórmulas del paper
  - Documentar reglas de negocio
  - Impacto: Mantenibilidad

---

## 🎨 Prioridad Baja

### UI/UX

- [x] **Añadir modo oscuro a Calculadora VHV**
  - Completado: 2025-12-04
  - Archivo: `app/static/css/vhv.css`
  - Implementado por Claude Opus

- [ ] **Mejorar diseño responsive de Calculadora VHV**
  - Archivo: `app/static/css/vhv.css`
  - Optimizar para móviles
  - Mejorar accesibilidad (ARIA labels)

- [ ] **Añadir animaciones a resultados VHV**
  - Transiciones suaves al mostrar resultados
  - Animación del gráfico Chart.js
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
  - Referencia: `docs/diseno-tecnico-comun-go.md`
  - Separar VHV, TVI, Auth en servicios independientes
  - Implementar en Go para performance
  - Timeframe: 24+ meses

---

## ✅ Completadas Recientemente

### Diciembre 2025

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

**Q4 2025:** Cohorte Cero - Validación experimental  
**Q1 2026:** Análisis de datos, refinamiento de fórmulas  
**Q2 2026:** Escalar a 50-100 participantes  
**Q3-Q4 2026:** Implementar Maxo beta  
**2027+:** Expansión a otras ciudades

---

*Para más detalles sobre la visión a largo plazo, ver [docs/TAREAS_PENDIENTES_IMPLEMENTACION.md](docs/TAREAS_PENDIENTES_IMPLEMENTACION.md)*
