# Tutorial: Registrar tu TVI (Tiempo Vital Indexado)

**Tiempo de lectura:** 10 minutos  
**Requisitos:** Navegador web y servidor corriendo, o Google Sheets para registro manual

---

## ¿Qué es el TVI?

El **Tiempo Vital Indexado** es la unidad atómica de Maxocracia. Representa cada momento de tu vida como una coordenada única e irrepetible.

> **Axioma T0:** "Cada instante de la vida de un ser consciente es una coordenada espacio-temporal única e irrepetible."

Al registrar tu TVI, aprendes:
- **A dónde va tu tiempo** realmente
- **Cuánto tiempo inviertes** vs cuánto "fugado"
- **Tu CCP** (Coeficiente de Coherencia Personal)

---

## Categorías de Tiempo

Tu tiempo se clasifica en 5 categorías:

| Categoría | Código | Descripción | Ejemplos |
|-----------|--------|-------------|----------|
| **Mantenimiento** | MAINTENANCE | Lo básico para funcionar | Comer, dormir, higiene, transporte |
| **Inversión** | INVESTMENT | Construir capital vital | Trabajo, estudio, ejercicio, crianza |
| **Ocio** | LEISURE | Disfrute consciente | Hobbies, socializar, entretenimiento elegido |
| **Trabajo** | WORK | Obligaciones laborales | Empleo remunerado, proyectos |
| **Fuga** | WASTE | Tiempo no intencional | Scroll sin propósito, procrastinación |

---

## Método 1: Usando la API (Avanzado)

Si el servidor está corriendo:

### Registrar un bloque de tiempo

```bash
POST /tvi
Authorization: Bearer <tu_token>
Content-Type: application/json

{
  "start_time": "2025-12-09T09:00:00",
  "end_time": "2025-12-09T11:00:00",
  "category": "INVESTMENT",
  "description": "Trabajando en calculadora VHV"
}
```

### Ver tu tiempo registrado

```bash
GET /tvi?limit=50&offset=0
Authorization: Bearer <tu_token>
```

### Ver tu CCP (estadísticas)

```bash
GET /tvi/stats
Authorization: Bearer <tu_token>
```

---

## Método 2: Usando Google Sheets (Recomendado para Cohortes)

### Paso 1: Crear tu hoja TVI Log

Crea una hoja con estas columnas:

| Fecha | Hora Inicio | Hora Fin | Categoría | Descripción | Duración (h) |
|-------|-------------|----------|-----------|-------------|--------------|
| 2025-12-09 | 09:00 | 11:00 | INVESTMENT | Trabajo en proyecto | 2.0 |
| 2025-12-09 | 11:00 | 11:30 | MAINTENANCE | Almuerzo | 0.5 |
| 2025-12-09 | 11:30 | 12:30 | WASTE | Scroll Instagram | 1.0 |

### Paso 2: Registrar al final del día

Cada noche, llena tus ~16-18 horas de vigilia:

1. Abre tu hoja
2. Recuerda qué hiciste hoy (revisa calendario, fotos, etc.)
3. Clasifica honestamente cada bloque de tiempo
4. **Clave:** Sé brutal con el WASTE. No te juzgues, solo observa.

### Paso 3: Calcular tu CCP semanal

La fórmula del **Coeficiente de Coherencia Personal**:

```
CCP = (INVESTMENT + LEISURE) / (Total - MAINTENANCE)
```

**Ejemplo:**
| Categoría | Horas/semana |
|-----------|--------------|
| MAINTENANCE | 56 (8h/día × 7) |
| INVESTMENT | 35 |
| LEISURE | 14 |
| WORK | 40 |
| WASTE | 7 |
| **Total** | 112 (16h × 7) |

```
CCP = (35 + 14) / (112 - 56)
    = 49 / 56
    = 0.875 = 87.5%
```

**Interpretación:**
- **CCP > 80%:** Alta intencionalidad
- **CCP 50-80%:** Moderado, hay espacio para mejorar
- **CCP < 50%:** Mucha fuga de tiempo vital

---

## Detección de Superposiciones

El sistema detecta si intentas vivir dos momentos a la vez:

```
⚠️ Error: El TVI 09:00-11:00 se superpone con TVI existente 10:00-12:00
```

Esto te obliga a ser honesto: no puedes "trabajar" y "estar en reunión" al mismo tiempo.

---

## Tips para Registrar Mejor

### 1. Sé específico
❌ "Trabajé"  
✅ "Escribí documentación para API"

### 2. No infravalores el MAINTENANCE
Incluye todo: transporte, preparar comida, vestirse, ducharse.

### 3. Sé honesto con el WASTE
La mayoría subestimamos el tiempo perdido. Si scrolleaste "5 minutos" y fueron 30, registra 30.

### 4. Registra diario, no semanal
La memoria se distorsiona. Hazlo cada noche antes de dormir.

### 5. No te juzgues, observa
El objetivo no es tener CCP perfecto. Es **ver la realidad** de tu tiempo.

---

## Ritual Semanal: Análisis de Tu Tiempo

Cada domingo, dedica 15 minutos a:

1. **Calcular tu CCP semanal**
2. **Identificar patrones:**
   - ¿Cuándo fue tu mayor fuga?
   - ¿Qué días invertiste más?
3. **Una acción pequeña:**
   - ¿Qué cambio mínimo puedes hacer la próxima semana?

---

## Preguntas Frecuentes

### ¿El WORK cuenta como INVESTMENT?

Depende. Su tu trabajo es:
- ✅ Significativo y alineado con tus valores → INVESTMENT o WORK
- ❌ Solo para pagar cuentas, sin propósito → WORK (neutro)

Para el CCP, WORK no suma a intencionalidad. Solo INVESTMENT y LEISURE.

### ¿El ocio con pantallas es LEISURE o WASTE?

Si fue **elegido conscientemente** → LEISURE  
Si fue **scrolling automático** → WASTE

**Test:** ¿Lo elegiste antes de empezar o "te encontraste" haciéndolo?

### ¿Cuánto tiempo debo dedicar a registrar?

Máximo 5-10 minutos/día. Si toma más, simplifica las categorías.

---

## Próximos Pasos

1. Crea tu hoja TVI Log (o usa la API)
2. Registra tus primeros 7 días
3. Calcula tu primer CCP
4. Comparte el número con tu Cohorte (sin juzgar a nadie)

---

*Tutorial creado: Diciembre 2025*  
*Ver también: [arquitectura_temporal_coherencia_vital.md](../arquitectura_temporal_coherencia_vital.md)*
