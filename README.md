# Maxocracia-Cero: El Laboratorio Vivo

**Estado del Proyecto:** Fase Cero - Prototipo Funcional Activo (Bogotá, Colombia)

---

## ¿Qué es esto?

Este repositorio contiene los artefactos digitales y la hoja de ruta para la Fase Cero de la Maxocracia, un nuevo sistema operativo para la sociedad diseñado para maximizar el bienestar colectivo.

Aquí no encontrarás (aún) contratos inteligentes complejos, sino las herramientas prácticas y los datos que emergen de nuestra red de apoyo en el mundo real. Este es el lugar donde el "alma" de la Maxocracia (su filosofía y su gente) se encuentra con su "esqueleto" (su arquitectura de datos y sistemas).

maxlopeztutor@gmail.com

- **El Alma del Proyecto (El Porqué):** [Lee el Brochure de la Maxocracia aquí](docs/Paper Maxocracia ChatGPT Scholar AI.txt)
- **El Esqueleto del Proyecto (El Cómo):** Los archivos en este repositorio.

## Índice rápido

- [Manifiesto: MAXOCRACIA](docs/MAXOCRACIA_MANIFIESTO.md)
- [Documentación de la API](docs/API.md)
- [Guía de Estilo](docs/GUIA_DE_ESTILO.md)
- [Código de Conducta](CODE_OF_CONDUCT.md)
- [Guía de Contribución](CONTRIBUTING.md)
- [FAQ Extendido](docs/FAQ_EXTENDIDO.md)

## La Arquitectura en Práctica

Nuestra visión a largo plazo se basa en una arquitectura de tres capas (Verdad, Acción, Valor). En esta fase inicial, la implementamos de forma pragmática a través de formularios y esquemas que alimentan un modelo de datos en evolución.

- **El VerityLedger (Capa de Verdad):** Se implementa a través del `Formulario A`, donde cada intercambio se registra como un hecho verificable.
- **El Ciclo de Mejora Continua (Capa de Acción):** Se implementa a través del `Formulario B`, que da seguimiento a la evolución de los participantes y permite al sistema aprender y adaptarse.
- **El Módulo Económico (Capa de Valor):** Comenzamos a capturar las métricas (`UTH`, `URF`, `Impacto`) que formarán la base de la futura moneda, el Maxo.

## Cómo Contribuir

Actualmente, el proyecto se centra en apoyar y aprender de la red de apoyo de Bogotá. Si quieres contribuir, revisa las especificaciones en este repositorio y contacta a los facilitadores del proyecto.

---

## Interfaz web (API Playground)

Mientras la aplicación Flask esté corriendo (por defecto en `http://127.0.0.1:5001/` si usas `PORT=5001`), abre la raíz `/` en tu navegador para acceder a un pequeño "API Playground" estático en `app/static/index.html`.

### Características de seguridad implementadas:
- Autenticación basada en JWT (JSON Web Tokens)
- Tokens de actualización con rotación automática
- Validación robusta de entradas en todos los endpoints
- Rate limiting para prevenir abusos (3 peticiones por minuto en endpoints sensibles)
- Validación estricta de contraseñas (mínimo 8 caracteres, mayúsculas, minúsculas y números)
- **Calculadora VHV**: Implementación completa del Vector de Huella Vital (T, V, R) y precio Maxo.

### Pasos rápidos:

1. **Configuración inicial**:
   ```bash
   # Clona el repositorio
   git clone https://github.com/tu-usuario/maxocracia-cero.git
   cd maxocracia-cero
   
   # Crea y activa un entorno virtual (recomendado)
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   
   # Instala dependencias
   pip install -r requirements.txt
   ```

2. **Ejecuta el servidor**:
   ```bash
   # Configura las variables de entorno (opcional, usa valores seguros en producción)
   export FLASK_APP=app
   export FLASK_ENV=development
   export SECRET_KEY='tu-clave-secreta-segura'
   
   # Inicia la aplicación
   python run.py
   ```

3. **Accede al API Playground**:
   - Abre `http://127.0.0.1:5001/` en tu navegador.
   - Regístrate (Register) con un correo y contraseña segura.
   - Haz Login y copia el token JWT que aparece en la caja "Token".
   - Usa las secciones para crear interchanges, ver balances, transferir Maxo y crear/claim recursos.

> **Nota**: La interfaz de usuario está diseñada para pruebas locales y demostración; no es una interfaz de producción. Para entornos de producción, se recomienda implementar una interfaz de usuario completa y medidas de seguridad adicionales.

### Ejecutando las pruebas

Para ejecutar las pruebas unitarias y de integración:

```bash
# Instala dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecuta todas las pruebas
pytest -v

# Ejecuta pruebas específicas (ejemplo)
pytest tests/test_auth.py -v
```

## Contribuyendo

Las contribuciones son bienvenidas. Por favor, lee nuestras pautas de contribución antes de enviar pull requests.
