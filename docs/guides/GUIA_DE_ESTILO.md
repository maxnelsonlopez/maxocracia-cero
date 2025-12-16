# Guía de Estilo para Desarrollo en Maxocracia

Esta guía establece los estándares de codificación y estilo para el proyecto Maxocracia. Seguir estas pautas ayuda a mantener la consistencia y calidad del código en todo el proyecto.

## Tabla de Contenidos

- [Python](#python)
  - [Formato](#formato)
  - [Nombrado](#nombrado)
  - [Documentación](#documentación)
  - [Manejo de Errores](#manejo-de-errores)
- [JavaScript](#javascript)
- [Base de Datos](#base-de-datos)
- [Control de Versiones](#control-de-versiones)
- [Pruebas](#pruebas)
- [Seguridad](#seguridad)

## Python

### Formato

- **Tamaño de línea**: Máximo 88 caracteres (según Black)
- **Sangría**: 4 espacios (sin tabuladores)
- **Comillas**: Comillas dobles (`"`) para cadenas visibles al usuario, comillas simples (`'`) para el resto
- **Espaciado**:
  - 2 líneas en blanco entre funciones y clases
  - 1 línea en blanco entre métodos

### Nombrado

- **Clases**: `PascalCase`
- **Funciones y variables**: `snake_case`
- **Constantes**: `MAYUSCULAS_CON_GUION_BAJO`
- **Módulos**: `snake_case`
- **Clases privadas**: `_ClasePrivada`
- **Variables y métodos privados**: `_variable_privada`, `_metodo_privado()`

### Documentación

#### Docstrings

Usar el formato Google Style para docstrings:

```python
def calcular_credito(uth_horas, impacto, uvc=0.0, urf=0.0):
    """Calcula el crédito Maxo basado en los parámetros del intercambio.

    La fórmula utilizada es:
        crédito = (uth_horas * PESO_UTH) + 
                 (impacto * PESO_IMPACTO) + 
                 (uvc * PESO_UVC) + 
                 (urf * PESO_URF)

    Args:
        uth_horas (float): Horas de Unidad de Tiempo Humano.
        impacto (float): Puntuación de impacto (0-10).
        uvc (float, optional): Unidades de Vida Consumida. Defaults to 0.0.
        urf (float, optional): Unidades de Recursos Finitos. Defaults to 0.0.

    Returns:
        float: Crédito Maxo calculado.

    Raises:
        ValueError: Si uth_horas o impacto son negativos.
    """
    if uth_horas < 0 or impacto < 0:
        raise ValueError("Los valores no pueden ser negativos")
    
    return (uth_horas * PESO_UTH) + (impacto * PESO_IMPACTO) + \
           (uvc * PESO_UVC) + (urf * PESO_URF)
```

#### Comentarios

- Usar comentarios para explicar el "por qué", no el "qué".
- Evitar comentarios obvios o redundantes.
- Los comentarios deben mantenerse actualizados con el código.

### Manejo de Errores

- Usar excepciones específicas en lugar de genéricas.
- Proporcionar mensajes de error útiles.
- Registrar los errores inesperados.

```python
try:
    procesar_intercambio(datos)
except ValidationError as e:
    logger.error(f"Error de validación: {e}")
    raise

except DatabaseError as e:
    logger.critical(f"Error de base de datos: {e}")
    raise ServiceUnavailable("Error al procesar la solicitud")
```

## JavaScript

### Formato

- **Tamaño de línea**: Máximo 80 caracteres
- **Sangría**: 2 espacios
- **Punto y coma**: Siempre usar punto y coma
- **Llaves**: En la misma línea que la declaración

### Nombrado

- **Clases**: `PascalCase`
- **Funciones y variables**: `camelCase`
- **Constantes**: `MAYUSCULAS_CON_GUION_BAJO`
- **Archivos**: `kebab-case.js`
- **Componentes React**: `PascalCase.jsx`

### Estructura de Componentes React

```jsx
import React from 'react';
import PropTypes from 'prop-types';

/**
 * Componente de tarjeta de usuario
 * 
 * @param {Object} props - Las propiedades del componente
 * @param {string} props.nombre - Nombre del usuario
 * @param {string} props.email - Correo electrónico
 * @param {function} props.onClick - Manejador de clic
 */
const UserCard = ({ nombre, email, onClick }) => {
  return (
    <div className="user-card" onClick={onClick}>
      <h3>{nombre}</h3>
      <p>{email}</p>
    </div>
  );
};

UserCard.propTypes = {
  nombre: PropTypes.string.isRequired,
  email: PropTypes.string.isRequired,
  onClick: PropTypes.func
};

export default UserCard;
```

## Base de Datos

### Convenciones SQL

- **Nombres de tablas**: `snake_case` en plural (`users`, `interchanges`)
- **Nombres de columnas**: `snake_case`
- **Claves foráneas**: `nombre_tabla_en_singular_id` (ej: `user_id`)
- **Claves primarias**: `id` (entero autoincremental) o `uuid`

### Migraciones

- Usar migraciones para todos los cambios en el esquema
- Las migraciones deben ser atómicas y reversibles
- Incluir comentarios explicativos en las migraciones complejas

## Control de Versiones

### Mensajes de Commit

Usar Conventional Commits:

```
tipo(ámbito): mensaje descriptivo

Cuerpo opcional con más detalles

Pie de página opcional con referencias a issues
```

**Tipos de commit**:
- `feat`: Nueva característica
- `fix`: Corrección de errores
- `docs`: Cambios en la documentación
- `style`: Cambios de formato (puntos y comas, indentación, etc.)
- `refactor`: Cambios que no corrigen errores ni agregan características
- `test`: Agregar o corregir pruebas
- `chore`: Cambios en el proceso de construcción o herramientas auxiliares

**Ejemplo**:
```
feat(auth): agregar autenticación con Google

- Implementar flujo OAuth2
- Agregar configuración de Google Cloud
- Actualizar documentación

Cierra #123
```

### Ramas

- `main`: Rama de producción estable
- `develop`: Rama de desarrollo
- `feature/`: Para nuevas características
- `fix/`: Para correcciones de errores
- `release/`: Para preparar lanzamientos

## Pruebas

### Convenciones

- Nombrar los archivos de prueba como `test_*.py` o `*.test.js`
- Usar nombres descriptivos para los casos de prueba
- Agrupar pruebas relacionadas en clases o bloques describe
- Seguir el patrón Arrange-Act-Assert

### Ejemplo de prueba en Python

```python
def test_calcular_credito():
    # Arrange
    uth_horas = 2.5
    impacto = 8
    
    # Act
    resultado = calcular_credito(uth_horas, impacto)
    
    # Assert
    assert resultado == (uth_horas * PESO_UTH) + (impacto * PESO_IMPACTO)
```

### Cobertura

- Apuntar al menos al 80% de cobertura de código
- Verificar la cobertura antes de hacer push:
  ```bash
  pytest --cov=app tests/
  ```

## Seguridad

### Contraseñas

- Nunca registrar contraseñas en los logs
- Usar hashing seguro (bcrypt, Argon2)
- Validar la fortaleza de las contraseñas

### Datos Sensibles

- No incluir credenciales en el código
- Usar variables de entorno para configuraciones sensibles
- Validar y sanitizar todas las entradas del usuario

### API

- Validar todos los parámetros de entrada
- Implementar rate limiting
- Usar HTTPS en producción
- Implementar autenticación adecuada (JWT con expiración)

---

Esta guía está viva y puede evolucionar. Las contribuciones son bienvenidas.
