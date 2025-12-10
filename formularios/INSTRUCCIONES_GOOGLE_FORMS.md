# Instrucciones: Crear Google Forms desde los Formularios Markdown

**Tiempo estimado:** 15-30 minutos por formulario  
**Requisitos:** Cuenta de Google

---

## Resumen

Este documento explica cómo convertir los formularios markdown del proyecto en Google Forms funcionales.

| Formulario | Archivo fuente | Propósito | Preguntas |
|------------|----------------|-----------|-----------|
| **CERO** | `formulario_CERO_inscripcion.md` | Inscripción inicial | 17 |
| **A** | `formulario_A_registro_intercambio.md` | Registro de intercambios | 16 |
| **B** | `formulario_B_reporte_seguimiento.md` | Seguimiento mensual | 18 |

---

## Paso 1: Crear un Nuevo Google Form

1. Ve a [forms.google.com](https://forms.google.com)
2. Click en **"+ Formulario en blanco"**
3. Dale el título correspondiente (ej: "Maxocracia: Únete a la Red de Apoyo")
4. Añade la descripción del archivo markdown

---

## Paso 2: Mapeo de Tipos de Pregunta

Usa esta tabla para convertir el markdown a Google Forms:

| En el Markdown | En Google Forms |
|----------------|-----------------|
| `Campo de texto` | Respuesta corta |
| `Campo de texto largo` | Párrafo |
| `Campo de email` | Respuesta corta (con validación de email) |
| `Campo de teléfono` | Respuesta corta |
| `Selecciona todos los que correspondan` | Casillas de verificación |
| `Selección (una sola opción)` | Opción múltiple |
| `Escala lineal (1 a 5)` | Escala lineal |
| `Fecha` | Fecha |
| `Casilla de verificación` | Casillas de verificación (1 opción) |

---

## Paso 3: Crear Formulario CERO (Inscripción)

### Configuración inicial
- **Título:** Maxocracia: Únete a la Red de Apoyo
- **Descripción:** (copiar del markdown)

### Secciones

Crea 4 secciones usando el botón "Añadir sección":

1. **¿Quién Eres?** (Preguntas 1-9)
2. **¿Cómo Podrías Ayudar?** (Preguntas 10-11)
3. **¿Qué Necesitas?** (Preguntas 13-16)
4. **Para Finalizar** (Pregunta 17)

### Preguntas clave

| # | Pregunta | Tipo | Obligatoria |
|---|----------|------|-------------|
| 1 | Tu nombre o Alias | Respuesta corta | ✅ |
| 2 | Tu correo electrónico | Respuesta corta + validación email | ✅ |
| 3 | ¿Quién te mostró este formulario? | Respuesta corta | ✅ |
| 10 | Describe brevemente lo que ofreces | Párrafo | ✅ |
| 15 | ¿Qué tan urgente es tu necesidad? | Opción múltiple (Alta/Media/Baja) | ✅ |
| 17 | Consentimiento | Casilla de verificación | ✅ |

---

## Paso 4: Crear Formulario A (Registro de Intercambio)

### Configuración inicial
- **Título:** Maxocracia - Registro de Intercambio Completado
- **Descripción:** "Este formulario registra intercambios ya realizados..."

### Secciones

1. **Identificación del Intercambio** (P1-P2)
2. **Participantes** (P3-P4)
3. **Detalles del Intercambio** (P5-P7)
4. **Métricas Maxocráticas** (P8-P10) - Opcionales
5. **Impacto y Seguimiento** (P11-P13)
6. **Notas del Facilitador** (P14-P16)

### Preguntas clave

| # | Pregunta | Tipo | Obligatoria |
|---|----------|------|-------------|
| 1 | Fecha del intercambio | Fecha | ✅ |
| 2 | Código de Intercambio | Respuesta corta | ✅ |
| 5 | Tipo de intercambio | Casillas de verificación (múltiple) | ✅ |
| 8 | Tiempo humano invertido (UTH) | Respuesta corta | ❌ |
| 11 | ¿Se resolvió la necesidad? | Escala lineal (1-5) | ✅ |
| 16 | ¿Requiere seguimiento? | Opción múltiple | ✅ |

---

## Paso 5: Crear Formulario B (Seguimiento)

Similar proceso. Consulta `formulario_B_reporte_seguimiento.md` para la estructura.

---

## Paso 6: Configuración Recomendada

En cada formulario, ve a **Configuración** (ícono de engranaje):

### Pestaña "Respuestas"
- ✅ **Recopilar direcciones de correo:** Desactivado (ya lo pedimos en el formulario)
- ✅ **Limitar a 1 respuesta:** Desactivado (pueden llenar múltiples veces)

### Pestaña "Presentación"
- ✅ **Mostrar barra de progreso:** Activado
- ✅ **Mensaje de confirmación:** "¡Gracias! Tu registro ha sido guardado."

---

## Paso 7: Conectar a Google Sheets

1. En el formulario, ve a **Respuestas**
2. Click en el ícono de Google Sheets (verde)
3. Selecciona **"Crear una hoja de cálculo nueva"**
4. Nombra la hoja (ej: "Respuestas Formulario CERO")

Ahora cada respuesta se guarda automáticamente en la hoja.

---

## Paso 8: Compartir los Formularios

1. Click en **Enviar** (botón azul arriba a la derecha)
2. Selecciona **Link** (ícono de cadena)
3. ✅ Marca **"Acortar URL"**
4. Copia y comparte

### Links sugeridos

Guarda los links en tu hoja maestra:

| Formulario | Link |
|------------|------|
| CERO (Inscripción) | forms.gle/xxx |
| A (Intercambio) | forms.gle/yyy |
| B (Seguimiento) | forms.gle/zzz |

---

## Verificación

Antes de usar con tu Cohorte:

- [ ] Llena cada formulario tú mismo como prueba
- [ ] Verifica que las respuestas llegan a Google Sheets
- [ ] Revisa que las preguntas obligatorias están marcadas
- [ ] Prueba en móvil (la mayoría llenará desde el celular)

---

## Tips Avanzados

### Lógica condicional
Google Forms permite mostrar secciones según respuestas anteriores. Útil para:
- Si urgencia = "Alta" → mostrar preguntas adicionales
- Si tipo = "Apoyo Económico" → pedir detalles extra

### Notificaciones
En Respuestas → menú ⋮ → **Recibir notificaciones por correo de nuevas respuestas**

### Copia entre Cohortes
Si otra Cohorte quiere usar tus formularios:
1. Abre el formulario
2. Menú ⋮ → **Hacer una copia**
3. Comparte la copia

---

## Recursos

- [Ayuda oficial de Google Forms](https://support.google.com/docs/answer/6281888)
- Formularios fuente: `/formularios/*.md`
- Guía del facilitador: [GUIA_FACILITADOR.md](../docs/GUIA_FACILITADOR.md)

---

*Última actualización: Diciembre 2025*
