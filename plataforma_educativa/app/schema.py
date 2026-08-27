# -*- coding: utf-8 -*-
"""Máquina de datos de la Plataforma Educativa.

Define el esquema SQLite y la siembra obligatoria:

* 8 ramas del Árbol de Habilidades (``branches``).
* 35 temas (``topics``) con prerrequisitos y dificultad (1-5).
* Al menos 3 preguntas por tema (``questions``), con opciones JSON, índice de
  la respuesta correcta y una explicación breve.

El ``init_db`` es idempotente: crea las tablas si no existen y solo siembra
cuando el árbol está vacío (para no duplicar datos en cada arranque).
"""

import json
import sqlite3
from datetime import datetime, timezone

# --------------------------------------------------------------------------
# Definición de la base de datos (DDL)
# --------------------------------------------------------------------------

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    email TEXT,
    is_coordinator INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS branches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT NOT NULL UNIQUE,
    nombre TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    orden INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    branch_id INTEGER NOT NULL REFERENCES branches(id),
    slug TEXT NOT NULL UNIQUE,
    titulo TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    orden INTEGER NOT NULL,
    prereq_ids TEXT,
    dificultad INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id INTEGER NOT NULL REFERENCES topics(id),
    pregunta TEXT NOT NULL,
    opciones TEXT NOT NULL,
    correcta INTEGER NOT NULL,
    explicacion TEXT
);

CREATE TABLE IF NOT EXISTS user_topics (
    user_id INTEGER NOT NULL REFERENCES users(id),
    topic_id INTEGER NOT NULL REFERENCES topics(id),
    estado TEXT NOT NULL DEFAULT 'not_seen',
    score REAL,
    updated_at TEXT NOT NULL,
    mentor_rounds INTEGER NOT NULL DEFAULT 0,
    mentorship_approved INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (user_id, topic_id)
);

CREATE TABLE IF NOT EXISTS meetings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL,
    hora_inicio TEXT NOT NULL,
    duracion_min INTEGER NOT NULL DEFAULT 120,
    topic_id INTEGER NOT NULL REFERENCES topics(id),
    monitor_id INTEGER REFERENCES users(id),
    estado TEXT NOT NULL DEFAULT 'open',
    week TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS meeting_participants (
    meeting_id INTEGER NOT NULL REFERENCES meetings(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    asistio INTEGER,
    PRIMARY KEY (meeting_id, user_id)
);

CREATE TABLE IF NOT EXISTS availability (
    user_id INTEGER NOT NULL REFERENCES users(id),
    semana TEXT NOT NULL,
    slots TEXT NOT NULL,
    PRIMARY KEY (user_id, semana)
);
"""


def _now():
    """Timestamp UTC en formato ISO para las columnas created_at/updated_at."""
    return datetime.now(timezone.utc).isoformat()


# --------------------------------------------------------------------------
# Siembra (seed)
# --------------------------------------------------------------------------

# (slug, nombre, descripción, orden)
BRANCHES = [
    ("matematicas", "Matemáticas", "Razonamiento numérico y lógico-matemático.", 1),
    ("higiene", "Higiene y salud", "Cuidado del cuerpo, la mente y la salud pública.", 2),
    ("relaciones", "Relaciones sociales", "Cómo convivir, escuchar, cooperar y resolver conflictos.", 3),
    ("lectura", "Lectura", "Comprender, analizar y evaluar textos.", 4),
    ("escritura", "Escritura", "Expresar ideas por escrito con claridad y argumento.", 5),
    ("lenguaje", "Lenguaje e idiomas", "Comunicación en la lengua propia y en otras.", 6),
    ("naturaleza", "Naturaleza", "Comprender los ecosistemas, la vida y el planeta.", 7),
    ("computadores", "Computadores", "Uso seguro, programación e inteligencia artificial.", 8),
]

# (branch_slug, título, slug, descripción, dificultad, prereq_slugs, [preguntas])
# Cada pregunta: (pregunta, [opciones], índice_correcta, explicación)
TOPIC_SEEDS = [
    # --- Matemáticas ---
    ("matematicas", "Conteo", "conteo", "Contar objetos y entender secuencias numéricas.", 1, [], [
        ("¿Cuál es el número que sigue: 1, 2, 3, ...?", ["2", "3", "4", "5"], 2, "La secuencia avanza de uno en uno: sigue el 4."),
        ("¿Cuántos dedos tiene una mano?", ["3", "4", "5", "6"], 2, "Cada mano tiene 5 dedos."),
        ("¿Qué número es mayor, 7 u 8?", ["7", "8", "Iguales", "No se puede saber"], 1, "8 viene después de 7, por eso es mayor."),
    ]),
    ("matematicas", "Sumas y restas", "sumas_y_restas", "Operaciones básicas de suma y resta.", 2, ["conteo"], [
        ("¿Cuánto es 3 + 4?", ["6", "7", "8", "9"], 1, "3 + 4 = 7."),
        ("¿Cuánto es 10 - 4?", ["4", "5", "6", "7"], 2, "10 - 4 = 6."),
        ("Si tengo 2 manzanas y me dan 3, ¿cuántas tengo?", ["3", "4", "5", "6"], 2, "2 + 3 = 5 manzanas."),
    ]),
    ("matematicas", "Multiplicación", "multiplicacion", "Multiplicar como suma repetida.", 2, ["sumas_y_restas"], [
        ("¿Cuánto es 3 x 2?", ["5", "6", "7", "8"], 1, "3 x 2 = 6."),
        ("¿Cuánto es 4 x 5?", ["16", "18", "20", "25"], 2, "4 x 5 = 20."),
        ("¿Cuánto es 6 x 3?", ["12", "15", "18", "21"], 2, "6 x 3 = 18."),
    ]),
    ("matematicas", "Fracciones", "fracciones", "Partes de un todo y comparación de fracciones.", 3, ["multiplicacion"], [
        ("¿Qué fracción representa la mitad de algo?", ["1/2", "1/3", "1/4", "2/3"], 0, "La mitad es una de dos partes iguales: 1/2."),
        ("¿Cuánto es 1/2 + 1/2?", ["1", "1/2", "2", "3/4"], 0, "Dos mitades forman un entero: 1."),
        ("¿Qué es mayor: 1/2 o 1/4?", ["1/2", "1/4", "Iguales", "Ninguna"], 0, "Dividir en 2 partes da trozos más grandes que en 4."),
    ]),
    ("matematicas", "Álgebra básica", "algebra_basica", "Resolver incógnitas sencillas y variables.", 4, ["fracciones"], [
        ("Si x + 3 = 7, ¿cuánto vale x?", ["3", "4", "5", "7"], 1, "x = 7 - 3 = 4."),
        ("Si 2x = 10, ¿cuánto vale x?", ["2", "4", "5", "8"], 2, "x = 10 / 2 = 5."),
        ("¿Qué es una variable en álgebra?", ["Un número fijo", "Un símbolo que representa un valor", "Solo un número par", "Un error"], 1, "Una variable es un símbolo (como x) que toma un valor."),
    ]),
    ("matematicas", "Geometría", "geometria", "Figuras, lados y ángulos básicos.", 3, [], [
        ("¿Cuántos lados tiene un triángulo?", ["2", "3", "4", "5"], 1, "El triángulo tiene 3 lados."),
        ("¿Qué figura tiene 4 lados iguales?", ["Círculo", "Cuadrado", "Triángulo", "Óvalo"], 1, "El cuadrado tiene 4 lados iguales."),
        ("¿Cuántos grados suman los ángulos internos de un triángulo?", ["90", "180", "260", "360"], 1, "Los ángulos internos de un triángulo suman 180°."),
    ]),
    # --- Higiene y salud ---
    ("higiene", "Lavado de manos y agua", "lavado_manos_agua", "Higiene básica y acceso al agua.", 1, [], [
        ("¿Cuánto tiempo se recomienda lavarse las manos con jabón?", ["1 segundo", "15 segundos", "Al menos 20 segundos", "5 minutos"], 2, "Se recomienda unos 20 segundos, el tiempo de una canción corta."),
        ("¿Por qué es importante lavarse las manos?", ["Para oler mejor", "Para evitar la propagación de gérmenes", "Para gastar jabón", "No es importante"], 1, "Lavarse las manos reduce infecciones y enfermedades."),
        ("¿Cuándo conviene lavarse las manos?", ["Solo al despertar", "Antes de comer y después de ir al baño", "Solo si se ven sucias", "Una vez al día"], 1, "Sobre todo antes de comer y después del baño."),
    ]),
    ("higiene", "Alimentación saludable", "alimentacion_saludable", "Nutrición y hábitos de comida.", 2, [], [
        ("¿Qué grupo de alimentos aporta frutas y verduras?", ["Bebidas azucaradas", "Frutas y verduras", "Dulces", "Frituras"], 1, "Frutas y verduras aportan vitaminas y fibra."),
        ("¿Por qué es importante beber agua?", ["Para hidratar el cuerpo", "Para engordar", "No sirve para nada", "Solo en verano"], 0, "El agua es esencial para casi todas las funciones del cuerpo."),
        ("¿Cómo es una dieta equilibrada?", ["Con muchos dulces", "Con variedad y en porciones adecuadas", "Solo carne", "Solo pan"], 1, "La variedad y la proporción son claves."),
    ]),
    ("higiene", "Sueño", "sueno", "Higiene del sueño y descanso.", 2, [], [
        ("¿Cuántas horas de sueño se recomiendan por noche a un adulto?", ["2-3", "7-9", "15-18", "24"], 1, "La mayoría de adultos necesita entre 7 y 9 horas."),
        ("¿Qué ayuda a dormir mejor?", ["Usar el teléfono hasta tarde", "Tener un horario regular", "Tomar mucha cafeína", "Dormir todo el día"], 1, "Un horario regular sincroniza el reloj interno."),
        ("¿Por qué es importante dormir?", ["Porque descansa el cuerpo y la mente", "Porque es una pérdida de tiempo", "Para ver más tele", "No es importante"], 0, "El sueño restaura el cuerpo y consolida la memoria."),
    ]),
    ("higiene", "Salud mental", "salud_mental", "Bienestar emocional y psicológico.", 3, [], [
        ("¿Qué es la salud mental?", ["Ausencia total de problemas", "El bienestar emocional y psicológico", "Solo la memoria", "Un tema poco importante"], 1, "Es el bienestar emocional, psicológico y social."),
        ("¿Qué ayuda a cuidar la salud mental?", ["Hablar de lo que sientes", "Aislarte siempre", "Trabajar sin descanso", "Evitar a los demás"], 0, "Hablar de lo que se siente alivia y conecta."),
        ("¿Pedir ayuda profesional es...?", ["Una señal de debilidad", "Una señal de cuidado personal", "Solo para adultos", "Nunca necesario"], 1, "Pedir ayuda es cuidarse, no fallar."),
    ]),
    ("higiene", "Primeros auxilios", "primeros_auxilios", "Actuar ante emergencias básicas.", 3, [], [
        ("Ante una quemadura leve, ¿qué se recomienda primero?", ["Aplicar hielo directo", "Enfriar con abundante agua fría", "Poner pasta de dientes", "Pinchar la ampolla"], 1, "Agua fría reduce el calor y el daño; el hielo directo daña más."),
        ("Si alguien se atraganta y no puede respirar, ¿qué haces?", ["Llamar a un vecino", "Llamar al servicio de emergencias", "Ir a la tienda", "No hacer nada"], 1, "Llama a emergencias (o la manobra si sabes) de inmediato."),
        ("¿Qué haces ante una herida que sangra?", ["Presionar suavemente con un paño limpio", "Ponerle tierra", "Soplar la herida", "Ignorarla"], 0, "Presionar con un paño limpio ayuda a detener la hemorragia."),
    ]),
    # --- Relaciones sociales ---
    ("relaciones", "Escucha activa", "escucha_activa", "Atender y comprender al otro.", 2, [], [
        ("¿Qué es escuchar activamente?", ["Esperar tu turno para hablar", "Atender y comprender al otro", "Interrumpir con tu opinión", "Mirar el teléfono"], 1, "Escuchar activamente es dar atención y comprensión completa."),
        ("¿Qué señal muestra que estás escuchando?", ["Mirar a los ojos y asentir", "Hablar por encima", "Cambiar de tema", "No responder"], 0, "El contacto visual y el asentir invitan a hablar."),
        ("Para entender mejor a alguien conviene...", ["Hacer preguntas", "Suponer lo que dirá", "Juzgar rápido", "Ignorar detalles"], 0, "Preguntar aclara y muestra interés real."),
    ]),
    ("relaciones", "Resolución de conflictos", "resolucion_conflictos", "Resolver diferencias dialogando.", 2, [], [
        ("Ante un conflicto, lo más sano es...", ["Gritar más fuerte", "Buscar una solución dialogada", "Romper la relación", "Vengarse"], 1, "El diálogo permite resolver sin dañar la relación."),
        ("¿Qué significa 'ceder'?", ["Ganar siempre", "Renunciar a un extremo para acordar", "Perder todo", "Imponer"], 1, "Ceder es acercar posiciones, no rendirse por completo."),
        ("El primer paso para resolver un conflicto es...", ["Identificar el problema", "Hacer trampa", "Huir", "Acusar"], 0, "Hay que entender el problema antes de buscar soluciones."),
    ]),
    ("relaciones", "Empatía", "empatia", "Ponerse en el lugar del otro.", 2, [], [
        ("¿Qué es la empatía?", ["Ponerse en el lugar del otro", "Sentir lástima", "Ganar discusiones", "Tener razón"], 0, "Empatía es comprender lo que otra persona siente."),
        ("¿Cómo se muestra empatía?", ["Escuchando las emociones del otro", "Minimizando su dolor", "Cambiando de tema", "Riéndote"], 0, "Reconocer la emoción ajena es el corazón de la empatía."),
        ("La empatía ayuda a...", ["Construir confianza", "Manipular", "Ganar poder", "Evitar a la gente"], 0, "Comprender al otro genera vínculos y confianza."),
    ]),
    ("relaciones", "Comunicación no violenta", "comunicacion_no_violenta", "Expresar necesidades sin agredir.", 3, [], [
        ("¿Qué propone la comunicación no violenta?", ["Decir lo que siento sin dañar", "Soltar insultos", "Callarse", "Mandar"], 0, "CNV propone expresar sin juzgar ni agredir."),
        ("¿Cuál es un paso de la CNV?", ["Observar sin juzgar", "Etiquetar", "Acusar", "Amenazar"], 0, "Se observa el hecho sin ponerse en modo acusación."),
        ("En la CNV, las peticiones son...", ["Exigencias", "Peticiones claras y razonables", "Órdenes", "Sugerencias vagas"], 1, "Se pide con claridad, sin exigir ni manipular."),
    ]),
    ("relaciones", "Trabajo en equipo", "trabajo_equipo", "Colaborar hacia una meta común.", 2, [], [
        ("¿Qué es clave en un equipo?", ["Colaborar y comunicarse", "Competir entre todos", "Ignorar a los demás", "Hacerlo todo solo"], 0, "Colaboración y comunicación son la base del equipo."),
        ("Cuando hay una tarea en equipo conviene...", ["Repartirla", "Hacerla una sola persona", "No hacerla", "Esperar instrucciones"], 0, "Repartir aprovecha las fortalezas de cada quien."),
        ("Un buen equipo...", ["Suma las fortalezas de todos", "Depende del más listo", "Guarda los roles", "No conversa"], 0, "El buen equipo multiplica lo que cada uno aporta."),
    ]),
    # --- Lectura ---
    ("lectura", "Comprensión lectora", "comprension_lectora", "Captar ideas y detalles de un texto.", 2, [], [
        ("¿Qué es comprender un texto?", ["Captar su idea principal y sus detalles", "Leerlo rápido", "Saber cuántas palabras tiene", "Memorizarlo sin entender"], 0, "Comprender es darle sentido, no solo leer las palabras."),
        ("Para comprender un texto conviene...", ["Volver a releer las partes difíciles", "Saltarse palabras", "Leer sin atención", "Fijarte solo en el final"], 0, "Releer lo confuso afianza la comprensión."),
        ("La idea principal de un texto es...", ["Lo más importante que el autor quiere decir", "El título", "La primera palabra", "Un detalle cualquiera"], 0, "La idea principal resume el mensaje central."),
    ]),
    ("lectura", "Lectura crítica", "lectura_critica", "Cuestionar y evaluar lo que se lee.", 3, [], [
        ("¿Qué es leer de forma crítica?", ["Cuestionar y evaluar lo que lees", "Creerlo todo", "No leer", "Memorizar"], 0, "Leer críticamente es evaluar, no aceptar de entrada."),
        ("Ante una afirmación, la lectura crítica...", ["Busca evidencias y fuentes", "La acepta sin dudar", "La ignora", "La repite"], 0, "Se contrasta la afirmación con evidencias y fuentes."),
        ("Conocer al autor de un texto es...", ["Información útil para valorar su punto de vista", "Irrelevante", "Un dato falso", "Lo único a evaluar"], 0, "El contexto del autor ayuda a interpretar el texto."),
    ]),
    ("lectura", "Análisis de textos", "analisis_textos", "Descomponer un texto para entenderlo mejor.", 3, ["comprension_lectora"], [
        ("Analizar un texto implica...", ["Descomponerlo en partes para entenderlo mejor", "Leerlo una sola vez", "Copiarlo", "Contar sus letras"], 0, "Se separa en partes y relaciones."),
        ("¿Qué es el contexto de un texto?", ["Las circunstancias en que fue escrito", "El tamaño de la letra", "Solo el título", "El número de páginas"], 0, "El contexto es el marco que da sentido al texto."),
        ("Distinguir un hecho de una opinión es...", ["Parte del análisis", "Imposible", "Innecesario", "Solo para niños"], 0, "Saber qué es hecho y qué es opinión es base del análisis."),
    ]),
    # --- Escritura ---
    ("escritura", "Ortografía", "ortografia", "Escribir con reglas de escritura correctas.", 2, [], [
        ("¿Cuál palabra está escrita correctamente?", ["haver", "haber", "abér", "abeer"], 1, "La forma correcta es 'haber'."),
        ("Las palabras que terminan en -ción se escriben...", ["Con c", "Con s", "Con z", "Con x"], 0, "El sufijo -ción se escribe con c."),
        ("La tilde (acento) sirve para...", ["Indicar la sílaba tónica o distinguir significados", "Decorar", "Confundir", "No tiene función"], 0, "La tilde marca acento y, a veces, diferencia palabras."),
    ]),
    ("escritura", "Redacción", "redaccion", "Escribir de forma clara y ordenada.", 2, [], [
        ("Una buena redacción se caracteriza por...", ["Ser clara y ordenada", "Tener frases infinitas", "Usar muchas abreviaturas", "Ser confusa"], 0, "Claridad y orden permiten comunicar bien."),
        ("El inicio de un texto suele...", ["Presentar el tema", "Concluir", "No decir nada", "Repetir la conclusión"], 0, "La introducción presenta de qué se va a hablar."),
        ("¿Qué es un párrafo?", ["Un conjunto de oraciones con una idea", "Una palabra", "Una página entera", "Un dibujo"], 0, "El párrafo desarrolla una idea con varias oraciones."),
    ]),
    ("escritura", "Narrativa", "narrativa", "Contar historias con personajes y trama.", 3, [], [
        ("¿Qué elementos tiene una narración?", ["Personajes, lugar y trama", "Solo números", "Solo títulos", "Nada en particular"], 0, "Narrar implica personajes, espacio y una acción."),
        ("¿Qué es el narrador?", ["Quien cuenta la historia", "El lector", "El impresor", "El dibujante"], 0, "El narrador relata los hechos."),
        ("El conflicto en una narración es...", ["El problema central que se desarrolla", "El final", "El título", "Una página"], 0, "El conflicto es el motor de la historia."),
    ]),
    ("escritura", "Argumentación", "argumentacion", "Defender una idea con razones.", 3, ["redaccion"], [
        ("Argumentar es...", ["Dar razones para sostener una idea", "Insultar", "No opinar", "Cambiar de tema"], 0, "Argumentar es dar razones, no pelear."),
        ("Un buen argumento...", ["Se apoya en evidencias o razones válidas", "Es solo una opinión sin sustento", "Grita", "Repite el título"], 0, "Se sustenta en razones verificables o válidas."),
        ("El objetivo de una argumentación es...", ["Convencer con razones", "Imponer", "Humillar", "Callar a otros"], 0, "Se busca convencer, no silenciar ni imponer."),
    ]),
    # --- Lenguaje e idiomas ---
    ("lenguaje", "Español básico", "espanol_basico", "Fundamentos de gramática del español.", 1, [], [
        ("¿Cuál es una frase correcta en español?", ["Yo soy estudiante", "Yo es estudiante", "Yo ser estudiante", "Yo amigo"], 0, "El verbo 'soy' concuerda con 'yo'."),
        ("¿Qué es un sustantivo?", ["Una palabra que nombra personas, lugares o cosas", "Un verbo", "Un número", "Una pausa"], 0, "El sustantivo nombra seres, lugares u objetos."),
        ("¿Cuál es el verbo en 'el niño corre'?", ["corre", "niño", "el", "no hay verbo"], 0, "El verbo es la acción: 'corre'."),
    ]),
    ("lenguaje", "Inglés inicial", "ingles_inicial", "Vocabulario y frases básicas en inglés.", 2, [], [
        ("¿Cómo se dice 'hola' en inglés?", ["Hello", "Goodbye", "Please", "Thank you"], 0, "'Hello' es el saludo más común."),
        ("¿Qué significa 'cat'?", ["gato", "perro", "casa", "libro"], 0, "'Cat' significa gato."),
        ("¿Cuál es la traducción de 'water'?", ["agua", "fuego", "pan", "sol"], 0, "'Water' significa agua."),
    ]),
    ("lenguaje", "Oratoria", "oratoria", "Hablar en público con claridad y seguridad.", 3, [], [
        ("¿Qué es oratoria?", ["El arte de hablar en público con claridad", "El arte de callar", "Una técnica de baile", "Escribir cartas"], 0, "Oratoria es bien hablar en público."),
        ("Para hablar en público conviene...", ["Mirar al público y hablar con claridad", "Hablar muy rápido", "No preparar", "Mirar el suelo"], 0, "El contacto visual y la claridad conectan con la audiencia."),
        ("Antes de una exposición conviene...", ["Preparar y practicar", "Improvisar sin pensar", "Llegar tarde", "No saber el tema"], 0, "Practicar da seguridad y claridad."),
    ]),
    # --- Naturaleza ---
    ("naturaleza", "Ecosistemas", "ecosistemas", "Seres vivos y su entorno.", 2, [], [
        ("¿Qué es un ecosistema?", ["Un conjunto de seres vivos y su entorno", "Solo las plantas", "Solo los animales", "Un edificio"], 0, "El ecosistema integra organismos y su medio."),
        ("¿Qué hace un bosque por el planeta?", ["Produce oxígeno y alberga vida", "Calienta el planeta", "No hace nada", "Contamina"], 0, "Los bosques producen oxígeno y son hogar de muchas especies."),
        ("¿Qué es una cadena alimenticia?", ["El orden de quién se come a quién", "Un tipo de ecosistema", "Una herramienta", "Un animal"], 0, "La cadena alimenticia muestra el paso de energía entre seres."),
    ]),
    ("naturaleza", "Plantas", "plantas", "La vida vegetal y la fotosíntesis.", 2, [], [
        ("¿Qué necesitan las plantas para vivir?", ["Agua y luz", "Solo oscuridad", "Nada", "Solo piedras"], 0, "Las plantas necesitan agua, luz y nutrientes."),
        ("¿Qué es la fotosíntesis?", ["Proceso con el que la planta fabrica su alimento", "Una enfermedad", "Una herramienta", "El riego"], 0, "Con luz, las plantas fabrican su propio alimento."),
        ("¿Qué parte de la planta toma agua del suelo?", ["La raíz", "La flor", "La hoja", "El fruto"], 0, "La raíz absorbe agua y nutrientes del suelo."),
    ]),
    ("naturaleza", "Animales", "animales", "Clasificación y rol de los animales.", 2, [], [
        ("¿Qué es un mamífero?", ["Un animal que suele amamantar a sus crías", "Un pez", "Un insecto", "Un ave que vuela"], 0, "Los mamíferos alimentan a sus crías con leche."),
        ("¿A qué grupo pertenece la mariposa?", ["Insectos", "Mamíferos", "Peces", "Reptiles"], 0, "Las mariposas son insectos."),
        ("¿Por qué son importantes las abejas?", ["Polinizan plantas", "Son dañinas", "No hacen nada", "Comen todo"], 0, "Al polinizar, las abejas sostienen muchos ecosistemas."),
    ]),
    ("naturaleza", "Astronomía", "astronomia", "Estrellas, planetas y el sistema solar.", 3, [], [
        ("¿Qué es una estrella?", ["Un cuerpo que emite luz propia", "Un planeta", "Un satélite", "Una nube"], 0, "Las estrellas generan su propia luz."),
        ("¿Qué es el Sol?", ["La estrella más cercana a la Tierra", "Un planeta", "Un cometa", "Una luna"], 0, "El Sol es la estrella que da luz a la Tierra."),
        ("¿Cuántos planetas hay en el sistema solar?", ["8", "3", "12", "100"], 0, "El sistema solar tiene 8 planetas."),
    ]),
    ("naturaleza", "Cambio climático", "cambio_climatico", "Causas y efectos del cambio climático.", 3, [], [
        ("¿Qué causa el cambio climático en gran medida?", ["La acumulación de gases de efecto invernadero", "La rotación de la Tierra", "La Luna", "Las mareas"], 0, "Los gases de efecto invernadero atrapan calor."),
        ("¿Qué ayuda a reducir las emisiones?", ["Usar más energía renovable", "Quemar más combustible", "Talar bosques", "Desperdiciar energía"], 0, "Las renovables y el ahorro reducen emisiones."),
        ("¿Qué es un efecto del cambio climático?", ["El aumento de la temperatura global", "Nada", "Hacer siempre más frío", "Lluvia normal"], 0, "El aumento de temperatura es uno de sus efectos clave."),
    ]),
    # --- Computadores ---
    ("computadores", "Uso básico y archivos", "uso_basico_archivos", "Archivos, carpetas y guardado.", 1, [], [
        ("¿Qué es una carpeta?", ["Un lugar para organizar archivos", "Un programa de juego", "Una memoria", "Un cable"], 0, "Las carpetas agrupan y ordenan archivos."),
        ("¿Qué es un archivo?", ["Información guardada con un nombre", "Una ventana", "Una página web", "Un teclado"], 0, "Un archivo guarda información con nombre y formato."),
        ("¿Cómo guardas un documento?", ["Con la opción 'guardar'", "Apagar el equipo", "Quitar el archivo", "Cerrar sin guardar"], 0, "Guardar conserva los cambios en el disco."),
    ]),
    ("computadores", "Internet seguro", "internet_seguro", "Contraseñas, privacidad y phishing.", 2, [], [
        ("¿Qué es una contraseña segura?", ["Larga y difícil de adivinar", "Tu fecha de nacimiento", "'123456'", "'password'"], 0, "Una buena contraseña es larga y única."),
        ("¿A quién le compartes datos personales?", ["Solo a sitios confiables", "A cualquiera", "A desconocidos", "Nadie importa"], 0, "Los datos personales se comparten con cuentas confiables."),
        ("Un correo de un desconocido con un enlace...", ["Podría ser phishing", "Es siempre seguro", "Conviene abrirlo", "Es una broma"], 0, "Los enlaces de desconocidos suelen ser intentos de fraude."),
    ]),
    ("computadores", "Programación inicial", "programacion_inicial", "Algoritmos, variables y bucles.", 3, [], [
        ("¿Qué es un algoritmo?", ["Una secuencia de pasos para resolver un problema", "Un juego", "Un virus", "Una pantalla"], 0, "Un algoritmo es una receta de pasos finitos."),
        ("¿Qué es una variable?", ["Un espacio que guarda un valor", "Un error", "Un botón", "Un cable"], 0, "La variable almacena datos que pueden cambiar."),
        ("¿Qué hace un bucle (loop)?", ["Repite una acción", "Borra todo", "Nada", "Crea un archivo"], 0, "El bucle repite instrucciones varias veces."),
    ]),
    ("computadores", "IA como aliada", "ia_aliada", "Usar inteligencia artificial con criterio.", 3, [], [
        ("¿Qué es una IA?", ["Un sistema que procesa información para resolver tareas", "Un ser humano", "Un animal", "Un programa sin datos"], 0, "La IA procesa datos para ayudar a resolver tareas."),
        ("Una herramienta de IA puede...", ["Generar textos e ideas", "Pensar por ti sin revisar", "Decir siempre la verdad", "Reemplazar tu criterio"], 0, "La IA sugiere, pero conviene revisar y contrastar."),
        ("Al usar IA conviene...", ["Verificar la información", "Creer todo", "No preguntar", "Copiar sin revisar"], 0, "Comprobar lo que la IA propone es uso responsable."),
    ]),
]


def _seed(db_conn):
    """Siembra el árbol solo si la tabla de ramas está vacía (idempotente)."""
    count = db_conn.execute("SELECT COUNT(*) AS n FROM branches").fetchone()["n"]
    if count:
        return

    # Insertar ramas.
    for slug, nombre, descripcion, orden in BRANCHES:
        db_conn.execute(
            "INSERT INTO branches (slug, nombre, descripcion, orden) VALUES (?, ?, ?, ?)",
            (slug, nombre, descripcion, orden),
        )

    # Insertar temas pidiendo el id por slug (para poder resolver prerrequisitos).
    topic_ids = {}
    branch_ids = {
        row["slug"]: row["id"]
        for row in db_conn.execute("SELECT id, slug FROM branches").fetchall()
    }
    for branch_slug, titulo, slug, descripcion, dif, _prereqs, _questions in TOPIC_SEEDS:
        cur = db_conn.execute(
            "INSERT INTO topics (branch_id, slug, titulo, descripcion, orden, prereq_ids, dificultad) "
            "VALUES (?, ?, ?, ?, 0, '[]', ?)",
            (branch_ids[branch_slug], slug, titulo, descripcion, dif),
        )
        topic_ids[slug] = cur.lastrowid

    # Setear orden dentro de la rama (secuencial) y prerrequisitos por slug.
    # El orden es la posición del tema dentro de su rama en el seed (1..n).
    current_branch = None
    counter = 0
    for branch_slug, _t, slug, *_rest in TOPIC_SEEDS:
        if branch_slug != current_branch:
            current_branch = branch_slug
            counter = 0
        counter += 1
        prereq_list = [topic_ids[p] for p in _rest[2]]  # prereq_slugs
        db_conn.execute(
            "UPDATE topics SET orden = ?, prereq_ids = ? WHERE id = ?",
            (counter, json.dumps(prereq_list), topic_ids[slug]),
        )

    # Insertar preguntas (>=3 por tema).
    for _branch_slug, _t, slug, _d, _f, _prereqs, preguntas in TOPIC_SEEDS:
        topic_id = topic_ids[slug]
        for (pregunta, opciones, correcta, explicacion) in preguntas:
            db_conn.execute(
                "INSERT INTO questions (topic_id, pregunta, opciones, correcta, explicacion) "
                "VALUES (?, ?, ?, ?, ?)",
                (topic_id, pregunta, json.dumps(opciones, ensure_ascii=False), correcta, explicacion),
            )


def init_db(app):
    """Crea las tablas y siembra el árbol sobre la base configurada."""
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    _seed(conn)
    conn.commit()
    conn.close()
