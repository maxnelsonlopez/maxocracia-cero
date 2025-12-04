# Maxocracia-Cero: El Laboratorio Vivo

**Estado del Proyecto:** Fase Cero - Prototipo Funcional Activo (Bogotá, Colombia)  
**Última actualización:** Diciembre 2025

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/maxnelsonlopez/maxocracia-cero)
---

## 🌟 ¿Qué es esto?

Este repositorio contiene la implementación funcional de **Maxocracia**, un nuevo sistema operativo para la sociedad diseñado para maximizar el bienestar colectivo basándose en verdad verificable y métricas de impacto real.

**No es solo teoría.** Aquí encontrarás:
- ✅ **Backend Flask funcional** con API completa
- ✅ **Calculadora VHV** (Vector de Huella Vital) operativa
- ✅ **Sistema TVI** (Tiempo Vital Indexado) implementado
- ✅ **Red de Apoyo activa** en Bogotá con 11+ participantes
- ✅ **Formularios operativos** para gestión de intercambios
- ✅ **67 tests pasando** con CI/CD configurado

---

## 📚 Documentación Esencial

### Para Entender la Visión
- **[Brochure de Maxocracia](docs/maxocracia_brochure.md)** - Introducción accesible al sistema
- **[Manifiesto Maxocracia](docs/MAXOCRACIA_MANIFIESTO.md)** - Los 8 Axiomas de la Verdad
- **[FAQ Extendido](docs/FAQ_EXTENDIDO.md)** - Preguntas difíciles, respuestas honestas

### Para Entender las Matemáticas
- **[Matemáticas Compiladas](docs/matematicas_maxocracia_compiladas.md)** - Todas las fórmulas y axiomas
- **[Arquitectura Temporal](docs/arquitectura_temporal_coherencia_vital.md)** - TVI, TTVI, CCP
- **[Paper Fundacional](docs/Paper%20Maxocracia%20ChatGPT%20Scholar%20AI.txt)** - Base teórica completa

### Para Desarrolladores
- **[Documentación de la API](docs/API.md)** - Todos los endpoints con ejemplos
- **[Guía de Contribución](CONTRIBUTING.md)** - Cómo colaborar
- **[Modelo de Datos](docs/MODELO_DE_DATOS.md)** - Esquema de base de datos

---

## 🚀 Inicio Rápido

### 1. Instalación

```bash
# Clonar el repositorio
git clone https://github.com/maxnelsonlopez/maxocracia-cero.git
cd maxocracia-cero

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configuración

```bash
# Variables de entorno (opcional, valores por defecto seguros)
export SECRET_KEY='tu-clave-secreta-muy-segura'
export FLASK_ENV=development
```

### 3. Ejecutar

```bash
# Iniciar servidor
python run.py

# El servidor estará en http://127.0.0.1:5001/
```

### 4. Explorar

- **API Playground**: http://127.0.0.1:5001/
- **Calculadora VHV**: http://127.0.0.1:5001/static/vhv-calculator.html

---

## 🧮 Calculadora VHV

La **Calculadora del Vector de Huella Vital** es una implementación completa de la formalización matemática de Maxocracia.

### Características

**4 Pestañas Funcionales:**
1. **Calculadora** - Calcula VHV = [T, V, R] y precio en Maxos
2. **Comparación** - Compara productos lado a lado
3. **Casos de Estudio** - Huevo Ético vs Industrial (del paper)
4. **Parámetros** - Visualiza α, β, γ, δ con validación axiomática

**Componentes del VHV:**
- **T (Tiempo)**: Horas directas + heredadas + futuras
- **V (Vida)**: UVC × consciencia × sufrimiento × abundancia × rareza
- **R (Recursos)**: Minerales + agua + petróleo + tierra × FRG × CS

**Fórmula de Valoración:**
```
Precio_Maxos = α·T + β·V^γ + δ·R
```

**Restricciones Axiomáticas:**
- α > 0 (el tiempo siempre vale)
- β > 0 (la vida siempre importa)
- γ ≥ 1 (aversión al sufrimiento)
- δ ≥ 0 (recursos finitos cuentan)

---

## ⏰ Sistema TVI (Tiempo Vital Indexado)

Implementación del **Axioma T0: Unicidad Existencial**

### Características

- **Registro de tiempo** por categorías: MAINTENANCE, INVESTMENT, WASTE, WORK, LEISURE
- **Detección de superposiciones** (no puedes vivir dos momentos a la vez)
- **Cálculo de CCP** (Coeficiente de Coherencia Personal)

### API Endpoints

```bash
# Registrar bloque de tiempo
POST /tvi
{
  "start_time": "2025-12-03T10:00:00",
  "end_time": "2025-12-03T12:00:00",
  "category": "INVESTMENT",
  "description": "Programando calculadora VHV"
}

# Ver tu tiempo registrado
GET /tvi?limit=50&offset=0

# Calcular tu CCP
GET /tvi/stats
```

**Fórmula CCP:**
```
CCP = (Investment + Leisure) / (Total Time - Maintenance)
```

---

## 📋 Sistema de Formularios

Gestión completa de la **Red de Apoyo** con 3 formularios operativos:

### Formulario CERO: Inscripción
- **Ubicación**: `formularios/formulario_CERO_inscripcion.md`
- **Propósito**: Registro inicial de participantes
- **Captura**: Ofertas, necesidades, valores, contacto

### Formulario A: Registro de Intercambio
- **Ubicación**: `formularios/formulario_A_registro_intercambio.md`
- **Propósito**: Documentar intercambios completados
- **Captura**: QUÉ pasó, UTH, URF, impacto, reciprocidad

### Formulario B: Reporte de Seguimiento
- **Ubicación**: `formularios/formulario_B_reporte_seguimiento.md`
- **Propósito**: Evaluar CÓMO evoluciona cada persona
- **Captura**: Estado actual, nuevas necesidades, salud emocional

**Métricas que generan:**
- UTH (Unidades de Tiempo Humano) movilizado
- Tasa de resolución de necesidades
- Flujo de red (quién da, quién recibe)
- Detección temprana de crisis

---

## 🧪 Testing

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecutar todos los tests
pytest -v

# Ver cobertura
pytest --cov=app --cov-report=html

# Tests específicos
pytest tests/test_vhv_calculator.py -v  # 19 tests
pytest tests/test_tvi.py -v             # Tests de TVI
```

**Estado actual:** ✅ 67/67 tests pasando

---

## 🔐 Seguridad

- ✅ **Autenticación JWT** con tokens de acceso y refresh
- ✅ **Rate limiting** (3 req/min en endpoints sensibles)
- ✅ **Validación de contraseñas** (8+ caracteres, mayúsculas, números)
- ✅ **Hashing de contraseñas** con Werkzeug
- ✅ **HttpOnly cookies** para refresh tokens
- ✅ **Validación de entradas** en todos los endpoints

---

## 📊 Arquitectura

```
maxocracia-cero/
├── app/
│   ├── __init__.py           # Factory de Flask
│   ├── auth.py               # Autenticación JWT
│   ├── vhv_calculator.py     # Lógica VHV
│   ├── vhv_bp.py             # API VHV
│   ├── tvi.py                # Lógica TVI
│   ├── tvi_bp.py             # API TVI
│   ├── schema.sql            # Esquema de BD
│   └── static/
│       ├── vhv-calculator.html  # UI Calculadora
│       ├── css/vhv.css          # Design system
│       └── js/vhv-calculator.js # Lógica frontend
├── tests/                    # 67 tests
├── formularios/              # 3 formularios operativos
├── docs/                     # Documentación completa
└── scripts/                  # Utilidades
```

---

## 🌍 Red de Apoyo (Cohorte Cero)

**Estado actual (Diciembre 2025):**
- 📍 **Ubicación**: Bogotá, Colombia
- 👥 **Participantes**: 11+ personas activas
- 🔄 **Intercambios**: Alimentación, conocimiento, objetos, tiempo
- 📈 **Resultados**: Personas en crisis siendo apoyadas efectivamente

**Próximos pasos:**
- Mes 2: "Contabilidad Existencial" con Calculadora VHV
- Mes 3: Calibración de parámetros α, β, γ, δ
- Mes 6: Evaluación y decisión de escalar

---

## 🤝 Cómo Contribuir

1. **Lee la [Guía de Contribución](CONTRIBUTING.md)**
2. **Revisa [TODO.md](TODO.md)** para tareas pendientes
3. **Ejecuta los tests** antes de hacer PR
4. **Sigue la [Guía de Estilo](docs/GUIA_DE_ESTILO.md)**

### Áreas donde necesitamos ayuda:
- 🔧 **Backend**: Optimización de consultas, nuevos endpoints
- 🎨 **Frontend**: Mejorar UX de la calculadora
- 📊 **Data Science**: Análisis de patrones en intercambios
- 📝 **Documentación**: Tutoriales, traducciones
- 🧪 **Testing**: Aumentar cobertura, tests de integración

---

## 📞 Contacto

**Fundador:** Max Nelson López  
📧 maxlopeztutor@gmail.com  
📱 +57 311 574 6208  
📍 Bogotá, Colombia

**Repositorio:** https://github.com/maxnelsonlopez/maxocracia-cero  
**Licencia:** Ver [LICENSE](LICENSE)

---

## 🎯 Visión a Largo Plazo

**2025-2026:** Validar principios en comunidades pequeñas  
**2027-2030:** Implementar Maxo en versión beta, expandir a múltiples ciudades  
**2030+:** Sociedades organizadas bajo principios maxocráticos

**No es utopía. Es optimismo realista.**  
**No es perfecto. Pero es mejor.**  
**No está completo. Pero ya comenzó.**

---

*"La verdad es el camino más corto de sucesos e información. La honestidad radical es el camino más eficiente."*  
— Axioma 4, Código de Coherencia

---

**Versión:** 2.0  
**Última actualización:** 2025-12-03  
**Creado con:** ❤️ + 🤖 (Max Nelson López + Claude/Gemini/ChatGPT)
