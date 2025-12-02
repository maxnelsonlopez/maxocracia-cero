# Changelog

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
