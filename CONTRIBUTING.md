# Guía de Contribución a Maxocracia

¡Gracias por tu interés en contribuir a Maxocracia! Esta guía te ayudará a entender cómo puedes contribuir al proyecto de manera efectiva.

## Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [¿Cómo puedo contribuir?](#cómo-puedo-contribuir)
  - [Reportar errores](#reportar-errores)
  - [Sugerir mejoras](#sugerir-mejoras)
  - [Contribuir con código](#contribuir-con-código)
  - [Mejorar la documentación](#mejorar-la-documentación)
- [Proceso de Desarrollo](#proceso-de-desarrollo)
  - [Configuración del Entorno](#configuración-del-entorno)
  - [Estructura del Proyecto](#estructura-del-proyecto)
  - [Convenciones de Código](#convenciones-de-código)
  - [Pruebas](#pruebas)
- [Preguntas Frecuentes](#preguntas-frecuentes)
- [Recursos Adicionales](#recursos-adicionales)

## Código de Conducta

Al participar en este proyecto, aceptas cumplir con nuestro [Código de Conducta](CODE_OF_CONDUCT.md). Por favor, repórtalo a [maxlopeztutor@gmail.com] si presencias algún comportamiento inaceptable.

## ¿Cómo puedo contribuir?

### Leer la documentación

Hay bastante escrito, y algunos documentos son cada uno una tesis con bastante información.
Bastantes de los posibles caminos para desarrollar el proyecto se han explorado en los documentos.
Con cada progreso se abren preguntas y misiones de ampliación del sistema. 
Si quieres contribuir tus propios textos envíamelos a maxlopeztutor@gmail.com



### Mejorar la documentación

La documentación es clave para el proyecto. Puedes ayudar a mejorarla de varias formas:

1. Corregir errores ortográficos o gramaticales
2. Mejorar la claridad de la documentación existente
3. Agregar ejemplos de código
4. Crear guías paso a paso
5. Traducir la documentación a otros idiomas

### Reportar errores

1. **Verifica si ya existe un issue** que describa el mismo problema.
2. Si no existe, crea un nuevo issue con la plantilla de "Reporte de Error".
3. Incluye toda la información solicitada:
   - Descripción clara del problema
   - Pasos para reproducir el error
   - Comportamiento esperado vs. comportamiento actual
   - Capturas de pantalla si es relevante
   - Versión del software y entorno

### Sugerir mejoras

1. **Verifica si ya existe un issue** relacionado con tu sugerencia.
2. Si no existe, crea un nuevo issue con la plantilla de "Sugerencia de Mejora".
3. Describe claramente:
   - La característica o mejora que te gustaría ver
   - Por qué crees que sería útil
   - Posibles implementaciones o consideraciones

### Contribuir con código

1. **Haz un fork** del repositorio.
2. Crea una rama descriptiva para tu característica o corrección:
   ```bash
   git checkout -b feature/nombre-de-la-caracteristica
   ```
3. Haz commits atómicos con mensajes descriptivos:
   ```bash
   git commit -m "tipo(ámbito): mensaje descriptivo"
   ```
4. Empuja tus cambios a tu fork:
   ```bash
   git push origin feature/nombre-de-la-caracteristica
   ```
5. Abre un Pull Request (PR) a la rama `develop`.


## Proceso de Desarrollo

### Configuración del Entorno

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/maxocracia-cero.git
   cd maxocracia-cero
   ```

2. Crea un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. Configura las variables de entorno:
   ```bash
   cp .env.example .env
   # Edita .env con tus configuraciones
   ```

5. Inicializa la base de datos:
   ```bash
   python scripts/init_db.py
   ```

### Estructura del Proyecto

```
maxocracia-cero/
├── app/                  # Código fuente de la aplicación
│   ├── __init__.py
│   ├── auth.py          # Autenticación y autorización
│   ├── models.py        # Modelos de datos
│   ├── routes/          # Rutas de la API
│   └── utils/           # Utilidades y helpers
├── tests/               # Pruebas automatizadas
├── docs/                # Documentación
├── migrations/          # Migraciones de base de datos
├── scripts/             # Scripts de utilidad
└── config/              # Archivos de configuración
```

### Convenciones de Código

- **Estilo de código**: Seguimos PEP 8 para Python
- **Docstrings**: Usamos el formato Google Style
- **Mensajes de commit**: Usamos Conventional Commits
  - `feat`: Nueva característica
  - `fix`: Corrección de errores
  - `docs`: Cambios en la documentación
  - `style`: Cambios de formato (espacios, puntos y comas, etc.)
  - `refactor`: Cambios que no corrigen errores ni agregan características
  - `test`: Agregar o corregir pruebas
  - `chore`: Cambios en el proceso de construcción o herramientas auxiliares

### Pruebas

1. Ejecuta todas las pruebas:
   ```bash
   pytest
   ```

2. Para cobertura de código:
   ```bash
   pytest --cov=app tests/
   ```

3. Para pruebas específicas:
   ```bash
   pytest tests/test_auth.py -v
   ```

### Calidad de Código

Para asegurar la calidad del código, utilizamos varias herramientas de análisis estático. Por favor, ejecútalas antes de enviar tu PR:

1. **Formato de código** (black e isort):
   ```bash
   black .
   isort .
   ```

2. **Linting** (flake8):
   ```bash
   flake8 .
   ```

3. **Tipado estático** (mypy):
   ```bash
   mypy .
   ```

## Preguntas Frecuentes

### ¿Cómo empiezo a contribuir?

1. Revisa los issues etiquetados como `good first issue` o `help wanted`.
2. Pregunta en el issue si necesitas aclaraciones.
3. Sigue el proceso de contribución descrito arriba.

### ¿Cómo propongo una nueva característica?

1. Abre un issue con la etiqueta `enhancement`.
2. Describe la característica en detalle.
3. Espera la retroalimentación del equipo.
4. Una vez aprobada, sigue el proceso de contribución.

## Recursos Adicionales

- [Documentación de la API](docs/API.md)
- [Guía de Estilo de Código](docs/CODING_STANDARDS.md)
- [Hoja de Ruta del Proyecto](docs/ROADMAP.md)

---

Gracias por tu interés en hacer de Maxocracia un proyecto mejor. ¡Tu contribución es muy valiosa!
