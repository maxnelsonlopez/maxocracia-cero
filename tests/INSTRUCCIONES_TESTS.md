# Instrucciones para Ejecutar los Nuevos Tests

## Tests Creados

Se han creado los siguientes archivos de tests para aumentar la cobertura:

1. **`test_users.py`** - Tests completos para `app/users.py`
   - 12 tests cubriendo todos los endpoints
   - Casos: listar, obtener, crear usuarios
   - Edge cases: usuarios inexistentes, datos inválidos, duplicados

2. **`test_utils.py`** - Tests para `app/utils.py`
   - 8 tests cubriendo funciones de utilidad
   - Casos: conexión BD, cierre, inicialización
   - Edge cases: múltiples contextos, conexiones reutilizadas

3. **`test_forms_manager_comprehensive.py`** - Tests exhaustivos para `FormsManager`
   - 25+ tests cubriendo métodos no probados
   - Casos: dashboard stats, alerts, network flow, trends, categories, resolution
   - Edge cases: datos vacíos, JSON parsing, validaciones

## Ejecutar los Tests

### Ejecutar todos los tests nuevos

```bash
# Desde el directorio raíz del proyecto
pytest tests/test_users.py -v
pytest tests/test_utils.py -v
pytest tests/test_forms_manager_comprehensive.py -v
```

### Ejecutar todos los tests del proyecto

```bash
pytest tests/ -v
```

### Ejecutar con cobertura

```bash
# Instalar pytest-cov si no está instalado
pip install pytest-cov

# Ejecutar con reporte de cobertura
pytest tests/ --cov=app --cov-report=term-missing --cov-report=html

# Ver reporte HTML
open htmlcov/index.html  # macOS
# o
xdg-open htmlcov/index.html  # Linux
```

### Ejecutar tests específicos

```bash
# Solo tests de usuarios
pytest tests/test_users.py::TestListUsers -v

# Solo un test específico
pytest tests/test_users.py::TestListUsers::test_list_users_success -v
```

## Verificar Cobertura

### Ver qué archivos tienen poca cobertura

```bash
pytest tests/ --cov=app --cov-report=term-missing | grep -E "TOTAL|app/"
```

### Ver cobertura por archivo

```bash
pytest tests/ --cov=app --cov-report=term-missing --cov-report=html
# Luego revisar htmlcov/index.html
```

## Tests Esperados

### test_users.py
- ✅ 12 tests deberían pasar
- Cubre: `list_users()`, `get_user()`, `create_user()`

### test_utils.py
- ✅ 8 tests deberían pasar
- Cubre: `get_db()`, `close_db()`, `init_db()`

### test_forms_manager_comprehensive.py
- ✅ 25+ tests deberían pasar
- Cubre: métodos de FormsManager no probados anteriormente

## Próximos Pasos

Después de verificar que estos tests pasan, se pueden crear:

1. **`test_forms_bp_comprehensive.py`** - Tests exhaustivos para endpoints de forms
2. **`test_vhv_bp_comprehensive.py`** - Tests exhaustivos para endpoints VHV
3. **`test_maxo_comprehensive.py`** - Tests adicionales para edge cases de Maxo
4. **`test_tvi_bp_comprehensive.py`** - Tests adicionales para endpoints TVI
5. **`test_interchanges_comprehensive.py`** - Tests exhaustivos para intercambios
6. **`test_resources_comprehensive.py`** - Tests exhaustivos para recursos

## Notas

- Todos los tests usan bases de datos temporales que se limpian automáticamente
- Los fixtures están en `conftest.py` y se reutilizan cuando es posible
- Los tests siguen los patrones existentes en el proyecto
- Se incluyen tests de casos edge y manejo de errores

## Troubleshooting

### Error: "No module named 'app'"
```bash
# Asegúrate de estar en el directorio raíz del proyecto
cd /Users/Max/Otros\ documentos/maxocracia-cero
export PYTHONPATH=$PWD:$PYTHONPATH
pytest tests/test_users.py -v
```

### Error: "Database is locked"
- Los tests usan bases de datos temporales que deberían limpiarse automáticamente
- Si persiste, verifica que no hay procesos usando las bases de datos de prueba

### Error: "Schema not found"
- Asegúrate de que `app/schema.sql` existe
- Los tests lo leen para inicializar las bases de datos temporales
