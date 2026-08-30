# Auditoría de mejora — Plataforma Educativa (29-08-2026)

> **Autoría**: MiniMax (subagente OpenRouter `:free`) — informe íntegro de forma y
> contenido. **Orquestador**: DeepSeek. Estado: hallazgos A2 y A4 **resueltos hoy**
> (commit de plataforma + fix); A1/B1 (sesgo de opción 0) y B2 (contenido nuevo)
> **pendientes de integrar** en una próxima pasada.

## A. FORMA — hallazgos (con prioridad)

| # | Hallazgo | Gravedad | Estado |
|---|---|---|---|
| A1/B1 | **70.5% de respuestas correctas en opción 0** (21/35 temas con las 3 en 0) — se aprueba marcando siempre la primera | 🔴 Alta | **Pendiente**: barajar opciones en `api_routes._topic_questions` (permutación determinista) + test anti-sesgo |
| A2 | **La explicación se veía antes de responder** (revelaba la respuesta: "3 + 4 = 7") | 🔴 Alta | ✅ **Resuelto** (app.js ya no renderiza el hint en el test) |
| A4 | "Hacer test" en temas bloqueados + endpoint sin validar prerrequisitos | 🔴 Alta | ✅ **Resuelto** (`topic_test` → 403 con `_prereqs_ok`; UI solo si `unlocked`) |
| A3 | Búsqueda sin debounce (~250 ms) y no expande ramas colapsadas | 🟡 Media | Pendiente |
| A5/A6 | Accesibilidad: labels/aria, modal sin `role="dialog"`, foco, Esc | 🟡 Media | Pendiente (mejoró al añadir modal evidence con aria) |
| A7/A8 | `alert()` bloqueante + sin `disabled` durante envíos | 🟡 Media | Pendiente |
| A9-A13 | Fecha ISO sin localizar; "Pedir mentoría" en mastered; contraste estrellas 2.2:1; errores silenciados | 🟢 Baja | Pendiente |
| B1 | "variable" definida dos veces con sentidos distintos (álgebra vs programación) | 🟡 Media | Pendiente (coherencia del tejido) |

## B. CONTENIDO — diagnóstico

- 35 temas × **3 preguntas exactas** (el mínimo es el máximo): sin profundidad.
- Ramas más débiles: lectura (3), lenguaje (3); solapamiento lectura/escritura/lenguaje.
- Explicaciones que solo repiten la respuesta (matemáticas: "3 + 4 = 7" sin estrategia).

### B2. 16 preguntas nuevas (una por tema débil priorizado) — formato del seed

Formato seed: `(pregunta, [opciones], índice_correcta, "explicación")`. Índices
distribuidos para corregir el sesgo de la opción 0.

matematicas/conteo: `("Cuentas de 5 en 5: 5, 10, 15, 20... ¿qué número sigue?", ["24", "25", "30", "21"], 1, "La secuencia avanza sumando 5 a cada número: 20 + 5 = 25.")`

matematicas/sumas_y_restas: `("María tenía 8 canicas, regaló 3 y luego encontró 2. ¿Cuántas tiene ahora?", ["6", "8", "7", "5"], 2, "Primero restamos lo que regaló: 8 − 3 = 5. Luego sumamos lo que encontró: 5 + 2 = 7.")`

matematicas/multiplicacion: `("Una bandeja tiene 4 filas con 3 galletas cada una. ¿Cuántas galletas hay en total?", ["12", "7", "34", "43"], 0, "Multiplicar es sumar en repetido: 3 + 3 + 3 + 3 = 12, es decir 4 × 3 = 12.")`

matematicas/fracciones: `("Divides una pizza en 4 partes iguales y comes 1. ¿Qué fracción de la pizza comiste?", ["1/3", "1/4", "3/4", "1/2"], 1, "Al cortar en 4 partes iguales, cada parte es 1/4 del total.")`

naturaleza/ecosistemas: `("Si desaparecieran los hongos y bacterias que descomponen la materia, ¿qué pasaría con el ecosistema?", ["Los productores crecerían más", "Nada cambiaría", "La materia orgánica se acumularía y se rompería el ciclo de nutrientes", "Habría más oxígeno"], 2, "Los descomponedores reciclan los nutrientes de lo que muere. Sin ellos, la materia se acumula y el ciclo se rompe.")`

naturaleza/plantas: `("¿Qué parte de la planta capta la luz para fabricar su alimento (fotosíntesis)?", ["La raíz", "El fruto", "El tallo", "La hoja"], 3, "Las hojas contienen clorofila y captan la luz que la planta usa para fabricar su alimento.")`

naturaleza/animales: `("¿Qué adaptación le permite al oso polar soportar el frío extremo?", ["Su grueso pelaje y su capa de grasa", "Volar", "Respirar bajo el agua", "Cambiar de tamaño"], 0, "El pelaje denso y la capa de grasa aíslan su cuerpo y le ayudan a conservar el calor.")`

naturaleza/astronomia: `("¿Por qué la Luna brilla de noche?", ["Porque emite luz propia", "Porque es una estrella", "Porque refleja la luz del Sol", "Porque es un espejo electrizado"], 2, "La Luna no produce luz: refleja la luz del Sol, por eso la vemos brillar.")`

higiene/alimentacion_saludable: `("¿Cuál es una porción razonable de fruta para una comida?", ["Cinco platos", "Una pieza o un puñado", "Ninguna", "Solo en jugo"], 1, "Una pieza o un puñado aporta vitaminas y fibra sin exceso de azúcar.")`

higiene/sueno: `("¿Qué efecto suele tener usar una pantalla (teléfono/tableta) justo antes de dormir?", ["Mejora el descanso", "No influye", "Reduce la necesidad de dormir", "Dificulta conciliar el sueño"], 3, "La luz de la pantalla y la actividad retrasan la melatonina y desordenan el inicio del sueño.")`

higiene/salud_mental: `("¿Qué efecto suele tener hablar de cómo te sientes con alguien de confianza?", ["Siempre empeora la situación", "Es inútil", "Solo funciona en niños", "Alivia y da otra perspectiva"], 3, "Expresar lo que sentimos baja la carga emocional y permite ver el problema desde fuera.")`

higiene/primeros_auxilios: `("Llamas a emergencias. ¿Qué dato es PRIORITARIO comunicar primero?", ["Tu nombre completo", "Dónde estás (ubicación/dirección)", "El color de tu ropa", "Qué desayunaste"], 1, "La ubicación permite que la ayuda llegue; el resto de los datos se aporta después.")`

relaciones/empatia: `("Tu amigo está triste. ¿Qué respuesta muestra más empatía?", ["'No es para tanto'", "'Veo que lo estás pasando mal, ¿quieres contarme?'", "'A mí me pasó algo peor'", "'Deja de llorar'"], 1, "Reconocer y validar la emoción (sin minimizarla ni competir) es el corazón de la empatía.")`

relaciones/trabajo_equipo: `("En un trabajo en equipo, ¿qué actitud mejora el resultado común?", ["Esperar a que otros decidan", "Competir por el crédito", "Aportar lo que cada quien sabe hacer mejor", "Quedarse solo con la tarea que más gusta"], 2, "Sumar talentos y repartir responsabilidades atiende mejor la meta del grupo.")`

relaciones/comunicacion_no_violenta: `("¿Cuál de estas frases es una petición (no una exigencia) en Comunicación No Violenta?", ["'¡Hazlo ya!'", "'¿Te parece si mañana lo revisamos juntos?'", "'Deberías hacerlo como digo yo'", "'No me importa lo que pienses'"], 1, "La CNV pide con claridad y deja espacio a la respuesta, sin exigir ni imponer.")`

relaciones/escucha_activa: `("Estás escuchando a alguien que habla. ¿Cuál acción NO es escucha activa?", ["Asentir y mantener contacto visual", "Hacer preguntas para aclarar", "Preparar tu respuesta mientras él/ella habla", "Resumir lo que entendiste"], 2, "Escuchar activamente exige atender de verdad; preparar la respuesta desvía la atención.")`

**Integración propuesta**: añadirlas al seed de `plataforma_educativa/app/schema.py` (función `_seed`) junto con el barajado de opciones (A1). Los temas usan slugs reales verificados por el subagente.
