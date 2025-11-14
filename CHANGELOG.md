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

### Corregido
- Corregidos problemas de importación en los tests
- Ajustes en la configuración de la base de datos para pruebas

## [0.1.0] - 2025-01-01
### Añadido
- Versión inicial del proyecto
- API básica con autenticación JWT
- Sistema de interacciones con seguimiento de VHV
- Documentación inicial del proyecto
