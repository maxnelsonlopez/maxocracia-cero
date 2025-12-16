# Tutorial: Calculadora VHV (Vector de Huella Vital)

**Tiempo de lectura:** 10 minutos  
**Requisitos:** Navegador web, servidor de Maxocracia corriendo (o usa los ejemplos offline)

---

## ¿Qué es el VHV?

El **Vector de Huella Vital** responde a la pregunta: *"¿Cuál es el costo real de este producto para el mundo?"*

No es un precio en dinero. Es una medición tridimensional:

| Dimensión | Qué mide | Unidad |
|-----------|----------|--------|
| **T** (Tiempo) | Horas humanas invertidas | Horas |
| **V** (Vida) | Impacto en seres vivos | UVC (Unidades de Vida Consumidas) |
| **R** (Recursos) | Recursos finitos utilizados | Índice compuesto |

---

## Paso 1: Acceder a la Calculadora

### Opción A: Servidor local
1. Inicia el servidor: `python run.py`
2. Abre en tu navegador: `http://127.0.0.1:5001/static/vhv-calculator.html`

### Opción B: Solo leer este tutorial
Si no tienes el servidor, sigue los ejemplos de abajo para entender cómo funciona.

---

## Paso 2: La Interfaz

La calculadora tiene **4 pestañas**:

| Pestaña | Propósito |
|---------|-----------|
| 📊 **Calculadora** | Calcular VHV de un producto |
| ⚖️ **Comparación** | Comparar dos productos lado a lado |
| 📚 **Casos de Estudio** | Ejemplos pre-cargados (huevo ético vs industrial) |
| ⚙️ **Parámetros** | Ver/ajustar los pesos α, β, γ, δ |

---

## Paso 3: Calcular el VHV de un Producto

### 3.1 Ingresa los datos de Tiempo (T)

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| Horas directas | Tiempo de trabajo directo en el producto | 0.5 |
| Horas heredadas | Tiempo amortizado de herramientas/infraestructura | 0.1 |
| Horas futuras | Tiempo estimado de mantenimiento/disposición | 0.05 |

**Resultado:** T = 0.5 + 0.1 + 0.05 = **0.65 horas**

### 3.2 Ingresa los datos de Vida (V)

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| UVC base | Unidades de vida consumidas (1 animal = 1 UVC) | 1 |
| Factor consciencia | 0.1 (plantas) a 1.0 (mamíferos) | 0.7 |
| Factor sufrimiento | 1.0 (mínimo dolor) a 25+ (cruel) | 1.2 |
| Factor abundancia | Protección de especies (más raro = más costoso) | 0.001 |
| Factor rareza genética | 1.0 (común) a 10+ (única) | 1.0 |

**Resultado:** V = 1 × 0.7 × 1.2 × 0.001 × 1.0 = **0.00084 UVC ponderadas**

### 3.3 Ingresa los datos de Recursos (R)

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| Minerales (kg) | Peso de minerales extraídos | 0.01 |
| Agua (L) | Litros de agua dulce consumidos | 50 |
| Petróleo (L) | Litros de combustible fósil | 0.1 |
| Tierra (m²) | Área de tierra ocupada | 0.5 |

El sistema calcula automáticamente los factores FRG (Rareza Geológica) y CS (Criticidad Sistémica).

---

## Paso 4: Interpretar los Resultados

### El VHV como vector

```
VHV = [T: 0.65, V: 0.00084, R: 2.3]
```

Esto significa:
- **0.65 horas** de trabajo humano cristalizado
- **0.00084 UVC** de impacto en seres vivos
- **2.3 unidades** de recursos finitos consumidos

### El Precio en Maxos

La fórmula de conversión es:

```
Precio_Maxos = α·T + β·V^γ + δ·R
```

Con parámetros por defecto (α=1, β=10, γ=1.5, δ=0.5):

```
Precio_Maxos = 1×0.65 + 10×0.00084^1.5 + 0.5×2.3
             = 0.65 + 0.00024 + 1.15
             = 1.80 Maxos
```

---

## Paso 5: Ejemplo Completo — Huevo Ético vs Industrial

Este es el caso de estudio principal del proyecto.

### Huevo Ético (pastoreo regenerativo)

| Componente | Valor | Justificación |
|------------|-------|---------------|
| T (horas) | 0.083 | ~5 min de trabajo por huevo |
| V (UVC) | 0.001 | Gallina bien tratada, abundante |
| R (recursos) | 0.5 | Bajo impacto ambiental |
| **Precio Maxos** | **~0.35** | |

### Huevo Industrial (granja intensiva)

| Componente | Valor | Justificación |
|------------|-------|---------------|
| T (horas) | 0.017 | Más eficiente (automatizado) |
| V (UVC) | 0.0135 | **13.5× más** por sufrimiento animal |
| R (recursos) | 1.2 | Mayor huella ambiental |
| **Precio Maxos** | **~0.95** | |

### Conclusión

El huevo industrial parece "más barato" en dinero, pero en Maxos cuesta **2.7× más** porque el sistema visibiliza el sufrimiento animal.

---

## Preguntas Frecuentes

### ¿Los parámetros α, β, γ, δ son fijos?

No. Son ajustables por el **Oráculo Dinámico** (la comunidad). Lo que NO puede cambiar:
- α > 0 (el tiempo siempre vale)
- β > 0 (la vida siempre importa)
- γ ≥ 1 (aversión al sufrimiento)
- δ ≥ 0 (recursos finitos cuentan)

### ¿Cómo sé qué valores poner?

Empieza con estimaciones. El sistema mejora con datos reales. La calculadora incluye valores por defecto razonables para productos comunes.

### ¿Puedo guardar mis cálculos?

Sí. La pestaña "Calculadora" tiene opción de guardar productos a la base de datos si el servidor está corriendo.

---

## Próximos Pasos

- Calcula el VHV de tu almuerzo de hoy
- Compara dos productos que compres regularmente
- Comparte tus hallazgos con tu Cohorte

---

*Tutorial creado: Diciembre 2025*  
*Ver también: [matematicas_maxocracia_compiladas.md](../matematicas_maxocracia_compiladas.md)*
