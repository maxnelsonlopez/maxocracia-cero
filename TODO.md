# Tareas Pendientes

## Prioridad Alta

### Seguridad
- [ ] **Actualizar seeds con contraseñas hasheadas**
  - Archivo: `scripts/seed_data.py`
  - Descripción: Reemplazar las contraseñas en texto plano por versiones hasheadas usando `generate_password_hash`
  - Impacto: Seguridad

### Pruebas
- [ ] **Implementar pruebas unitarias**
  - Archivos: `tests/`
  - Cobertura mínima objetivo: 80%
  - Tipos de pruebas a implementar:
    - Pruebas de autenticación
    - Pruebas de validación de entrada
    - Pruebas de lógica de negocio

- [ ] **Configurar integración continua (CI)**
  - Archivo: `.github/workflows/ci.yml`
  - Acciones a incluir:
    - Ejecución de pruebas
    - Análisis estático de código
    - Verificación de cobertura

## Prioridad Media

### Documentación
- [ ] **Documentar especificación formal de Maxo**
  - Archivo: `docs/maxo_specification.md`
  - Secciones a incluir:
    - Reglas de negocio
    - Cálculo de créditos
    - Políticas de canje

- [ ] **Actualizar documentación de la API**
  - Archivo: `docs/API.md`
  - Incluir ejemplos de solicitudes/respuestas
  - Documentar códigos de error

### Mejoras de Código
- [ ] **Refactorizar lógica de crédito de Maxo**
  - Archivos: `app/services/maxo_service.py`
  - Objetivos:
    - Mejorar mantenibilidad
    - Hacer el código más testeable
    - Documentar reglas de negocio

## Prioridad Baja

### Mejoras de UI/UX
- [ ] **Actualizar marcadores de posición en la documentación**
  - Archivo: `dashboard-spec/v0.1_widgets.md`
  - Reemplazar `INT-XXX` por identificadores reales

### Optimización
- [ ] **Revisar y optimizar consultas a la base de datos**
  - Archivos: `app/models/`
  - Objetivos:
    - Identificar consultas lentas
    - Añadir índices si es necesario
    - Optimizar relaciones

## En Progreso

- [ ] **Ninguna tarea en progreso actualmente**

## Completadas

- [x] **Corregir pruebas de validación de contraseñas**
  - Fecha de finalización: 2025-10-21
  - Archivos modificados:
    - `app/validators.py`
    - `tests/test_input_validation.py`

- [x] **Corregir pruebas de rate limiting**
  - Fecha de finalización: 2025-10-21
  - Archivos modificados:
    - `tests/test_rate_limiting.py`
    - `app/limiter.py`

## Cómo contribuir

1. Revisa la lista de tareas pendientes
2. Asigna una tarea a ti mismo comentando en el issue correspondiente
3. Crea una rama siguiendo el formato: `feature/descripcion-corta` o `fix/descripcion-corta`
4. Envía un Pull Request con una descripción clara de los cambios realizados

---

*Última actualización: 2025-10-21*
