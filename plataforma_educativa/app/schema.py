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
    maxo_user_id INTEGER UNIQUE,
    share_progress INTEGER NOT NULL DEFAULT 0,
    idioma TEXT NOT NULL DEFAULT 'es',
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
    evidence TEXT,
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

CREATE TABLE IF NOT EXISTS mentorship_triadas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    topic_id INTEGER NOT NULL REFERENCES topics(id),
    mentor_ok INTEGER NOT NULL DEFAULT 0,
    peer_ok INTEGER NOT NULL DEFAULT 0,
    oracle_veto INTEGER NOT NULL DEFAULT 0,
    outcome TEXT NOT NULL CHECK(outcome IN ('pending', 'validated', 'vetoed')),
    created_at TEXT NOT NULL,
    UNIQUE(user_id, topic_id)
);

-- La Biblioteca de la Ciudad (M15): material educativo por tema.
-- 'guia' = contenido propio en markdown (carga local instantánea);
-- 'enlace' = URL verificada al mundo compartido (Wikipedia, Khan, YouTube).
-- 'idioma' (M16): la biblioteca se sirve en la lengua de la persona; los
-- idiomas conviven sin pisarse (material_key incluye el idioma).
CREATE TABLE IF NOT EXISTS materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id INTEGER NOT NULL REFERENCES topics(id),
    material_key TEXT NOT NULL UNIQUE,
    titulo TEXT NOT NULL,
    tipo TEXT NOT NULL DEFAULT 'guia' CHECK(tipo IN ('guia', 'enlace')),
    fuente TEXT NOT NULL DEFAULT 'oev',
    url TEXT,
    contenido TEXT,
    autor TEXT NOT NULL DEFAULT 'siembra',
    orden INTEGER NOT NULL DEFAULT 0,
    idioma TEXT NOT NULL DEFAULT 'es',
    created_at TEXT NOT NULL
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


# Enlaces del mundo (M15): un artículo de Wikipedia por tema, VERIFICADO
# (estado HTTP 200, 30-08-2026). El mundo compartido no se siembra a ciegas:
# cada URL pasó la comprobación. La siembra es idempotente por material_key.
# (topic_slug, título del material, fuente, url)
MATERIAL_LINKS = [
    ("conteo", "Conteo — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Conteo"),
    ("sumas_y_restas", "Suma — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Suma"),
    ("multiplicacion", "Multiplicación — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Multiplicaci%C3%B3n"),
    ("fracciones", "Fracción — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Fracci%C3%B3n"),
    ("algebra_basica", "Álgebra elemental — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/%C3%81lgebra_elemental"),
    ("geometria", "Geometría — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Geometr%C3%ADa"),
    ("lavado_manos_agua", "Higiene de manos — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Higiene_de_manos"),
    ("alimentacion_saludable", "Dieta saludable — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Dieta_saludable"),
    ("sueno", "Sueño — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Sue%C3%B1o"),
    ("salud_mental", "Salud mental — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Salud_mental"),
    ("primeros_auxilios", "Primeros auxilios — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Primeros_auxilios"),
    ("escucha_activa", "Escucha activa — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Escucha_activa"),
    ("resolucion_conflictos", "Resolución de conflictos — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Resoluci%C3%B3n_de_conflictos"),
    ("empatia", "Empatía — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Empat%C3%ADa"),
    ("comunicacion_no_violenta", "Comunicación no violenta — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Comunicaci%C3%B3n_no_violenta"),
    ("trabajo_equipo", "Trabajo en equipo — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Trabajo_en_equipo"),
    ("comprension_lectora", "Comprensión lectora — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Comprensi%C3%B3n_lectora"),
    ("lectura_critica", "Lectura crítica — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Lectura_cr%C3%ADtica"),
    ("analisis_textos", "Análisis del discurso — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/An%C3%A1lisis_del_discurso"),
    ("ortografia", "Ortografía — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Ortograf%C3%ADa"),
    ("redaccion", "Redacción — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Redacci%C3%B3n"),
    ("narrativa", "Narrativa — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Narrativa"),
    ("argumentacion", "Argumentación — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Argumentaci%C3%B3n"),
    ("espanol_basico", "Idioma español — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Idioma_espa%C3%B1ol"),
    ("ingles_inicial", "Idioma inglés — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Idioma_ingl%C3%A9s"),
    ("oratoria", "Oratoria — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Oratoria"),
    ("ecosistemas", "Ecosistema — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Ecosistema"),
    ("plantas", "Planta — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Planta"),
    ("animales", "Animal — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Animal"),
    ("astronomia", "Astronomía — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Astronom%C3%ADa"),
    ("cambio_climatico", "Cambio climático — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Cambio_clim%C3%A1tico"),
    ("uso_basico_archivos", "Archivo informático — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Archivo_inform%C3%A1tico"),
    ("internet_seguro", "Seguridad de la información — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Seguridad_de_la_informaci%C3%B3n"),
    ("programacion_inicial", "Programación — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Programaci%C3%B3n"),
    ("ia_aliada", "Inteligencia artificial — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Inteligencia_artificial"),
    # M16 — la Ética en lenguaje común (enlaces verificados 30-08-2026).
    ("etica_el_dinero_que_nos_manda", "Deuda — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Deuda"),
    ("etica_que_vale_la_pena", "Ética — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/%C3%89tica"),
    ("etica_la_vida_se_cuenta", "Economía del cuidado — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Econom%C3%ADa_del_cuidado"),
    ("etica_el_minimo_que_todos_merecen", "Mínimo vital — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/M%C3%ADnimo_vital"),
    ("etica_tu_tiempo_es_tuyo", "Gestión del tiempo — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Gesti%C3%B3n_del_tiempo"),
    ("etica_la_palabra_que_obliga", "Contrato — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Contrato"),
    ("etica_dar_y_recibir_con_medida", "Economía del don — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Econom%C3%ADa_del_don"),
    ("etica_todo_lo_que_se_hace_se_ve", "Registro público — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Registro_p%C3%BAblico"),
    ("etica_decidir_juntos", "Asamblea — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Asamblea"),
    ("etica_cuidar_sin_cronometro", "Trabajo de cuidados — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Trabajo_de_cuidados"),
    ("etica_la_casa_grande", "Cooperativa — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Cooperativa"),
    ("etica_el_idioma_de_la_ciudad", "Banco de tiempo — Wikipedia", "wikipedia", "https://es.wikipedia.org/wiki/Banco_de_tiempo"),
]


def _seed_etica(db_conn):
    """Siembra la categoría Ética (M16): la casa en lenguaje común.

    Idempotente por slug (rama por nombre, temas por slug): arranca sobre
    bases que ya tienen las 8 ramas sin tocarlas. Las preguntas se añaden
    solo si el tema aún no tiene ninguna (la revisión posterior no duplica).
    """
    branch = db_conn.execute(
        "SELECT id FROM branches WHERE slug = 'etica'"
    ).fetchone()
    if branch is None:
        cur = db_conn.execute(
            "INSERT INTO branches (slug, nombre, descripcion, orden) VALUES "
            "('etica', 'Ética', 'La casa en común: antes de medir y construir, se aprende para qué. "
            "Los fundamentos del sistema en lenguaje común; el idioma propio se nombra al final.', 0)"
        )
        branch_id = cur.lastrowid
    else:
        branch_id = branch["id"]

    topic_ids = {}
    # Primera pasada: temas sin prerrequisitos (se resuelven por slug).
    for pos, (slug, titulo, descripcion, dificultad, _prereqs) in enumerate(ETICA_TOPICS, start=1):
        row = db_conn.execute(
            "SELECT id FROM topics WHERE slug = ?", (slug,)
        ).fetchone()
        if row is not None:
            topic_ids[slug] = row["id"]
            continue
        cur = db_conn.execute(
            "INSERT INTO topics (branch_id, slug, titulo, descripcion, orden, prereq_ids, dificultad) "
            "VALUES (?, ?, ?, ?, ?, '[]', ?)",
            (branch_id, slug, titulo, descripcion, pos, dificultad),
        )
        topic_ids[slug] = cur.lastrowid

    # Segunda pasada: prerrequisitos (cadena 1→12) y preguntas del banco.
    for pos, (slug, _t, _d, _dif, prereqs) in enumerate(ETICA_TOPICS, start=1):
        prereq_ids = [topic_ids[p] for p in prereqs if p in topic_ids]
        db_conn.execute(
            "UPDATE topics SET prereq_ids = ?, orden = ? WHERE slug = ?",
            (json.dumps(prereq_ids), pos, slug),
        )
        row = db_conn.execute(
            "SELECT id FROM topics WHERE slug = ?", (slug,)
        ).fetchone()
        q_count = db_conn.execute(
            "SELECT COUNT(*) AS n FROM questions WHERE topic_id = ?", (row["id"],)
        ).fetchone()["n"]
        if q_count == 0:
            for (pregunta, opciones, correcta, explicacion) in ETICA_QUESTIONS.get(slug, []):
                db_conn.execute(
                    "INSERT INTO questions (topic_id, pregunta, opciones, correcta, explicacion) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (row["id"], pregunta, json.dumps(opciones, ensure_ascii=False), correcta, explicacion),
                )


# La categoría Ética (M16): (slug, título común, descripción, dificultad 1-3, prereqs por slug).
# Los temas siguen el orden de los capítulos del libro, SIN jerga propia
# (excepto el puente final). Ver docs/architecture/ETICA_LENGUAJE_COMUN_CATEGORIA.md.
ETICA_TOPICS = [
    ("etica_el_dinero_que_nos_manda", "El dinero que nos manda",
     "Cómo la deuda y el interés terminan mandando sobre la vida; cuándo una deuda es puente y cuándo cadena.", 1, []),
    ("etica_que_vale_la_pena", "¿Qué vale la pena?",
     "Cuatro prioridades antes de cualquier medida: la vida, la verdad, el tiempo y la medida justa.", 1, ["etica_el_dinero_que_nos_manda"]),
    ("etica_la_vida_se_cuenta", "La vida se cuenta y no se vende",
     "La huella de una actividad en tres números: cuánto tomó, qué tan real fue y hacia dónde llevó.", 2, ["etica_que_vale_la_pena"]),
    ("etica_el_minimo_que_todos_merecen", "El mínimo que todos merecen",
     "El piso común que nadie cruza hacia abajo, y por qué el techo sí es de cada quien.", 2, ["etica_la_vida_se_cuenta"]),
    ("etica_tu_tiempo_es_tuyo", "Tu tiempo es tuyo",
     "El presupuesto vital de la semana: sueño, trabajo, descanso y compartir. El descanso no se vende.", 2, ["etica_el_minimo_que_todos_merecen"]),
    ("etica_la_palabra_que_obliga", "La palabra que obliga",
     "Prometer y cumplir; la palabra por escrito con testigos; verificar no es desconfiar.", 2, ["etica_tu_tiempo_es_tuyo"]),
    ("etica_dar_y_recibir_con_medida", "Dar y recibir con medida",
     "Dar no empobrece cuando vuelve aprendizaje o cuidado; la medida que ambos lados pueden mirar.", 3, ["etica_la_palabra_que_obliga"]),
    ("etica_todo_lo_que_se_hace_se_ve", "Lo que se hace, se ve",
     "Lo que cuenta se registra y se ve; la vida íntima es sagrada y no se registra.", 3, ["etica_dar_y_recibir_con_medida"]),
    ("etica_decidir_juntos", "Decidir juntos y rectificar",
     "Las decisiones que afectan a todos se toman entre todos; la voz disidente tiene silla; cambiar de opinión es virtud.", 3, ["etica_todo_lo_que_se_hace_se_ve"]),
    ("etica_cuidar_sin_cronometro", "Cuidar sin cronómetro",
     "Lo que no se mide y vale: un cuidado, un duelo, un perdón. La otra mitad de la economía.", 3, ["etica_decidir_juntos"]),
    ("etica_la_casa_grande", "La casa grande: comunidad y oficios",
     "Nadie se sostiene solo: cuidar, construir, cultivar, enseñar, limpiar — todos los oficios hacen la casa.", 3, ["etica_cuidar_sin_cronometro"]),
    ("etica_el_idioma_de_la_ciudad", "El idioma de la ciudad",
     "El puente final: las frases comunes que ya viviste, ahora con sus nombres propios.", 3, ["etica_la_casa_grande"]),
]

# Banco de preguntas por slug (M16): (pregunta, [opciones], índice_correcta, explicación).
# Situaciones concretas en lenguaje común (nunca doctrina); revisadas por el director.
ETICA_QUESTIONS = {
    "etica_el_dinero_que_nos_manda": [
        ("María pide un préstamo para comprar semillas y, con la venta de la cosecha, pagarlo y que a su familia le quede para comer. ¿Qué tipo de deuda está usando?",
         ["Una deuda que crece sola y nunca termina", "Una deuda-puente, porque la lleva de hoy a un mejor momento", "Una deuda de lujo, por pedir sin necesidad", "Una deuda que no sirve, porque pudo esperar"], 1,
         "Es una deuda-puente: la saca de una necesidad y se puede cerrar con el fruto de su trabajo, sin hundirla."),
        ("Don Pedro pide cada mes un préstamo nuevo para pagar el anterior, y los intereses se comen lo que gana. ¿Qué está ocurriendo?",
         ["Está usando una deuda-puente de forma inteligente", "Está ahorrando sin darse cuenta", "Está cayendo en una deuda-cadena, que se encadena con otra y nunca acaba", "Está protegido porque siempre puede pedir más"], 2,
         "Es una deuda-cadena: cada préstamo alimenta el siguiente, los intereses la hacen crecer y no le dejan salida limpia."),
        ("Una familia prefiere no pedir dinero para un viaje de placer, porque no quiere endeudarse por algo que no le deja un bien. ¿Qué refleja esa decisión?",
         ["Que nunca deben pedir nada, ni siquiera para una emergencia", "Que el viaje era más importante que todo", "Que las deudas son siempre malas y no hay excepciones", "Que miden si la deuda es puente o cadena antes de aceptarla"], 3,
         "Saben distinguir una deuda que abre camino (puente) de una que solo encadena problemas, y por eso deciden con cuidado."),
    ],
    "etica_que_vale_la_pena": [
        ("La abuela está enferma; con la plata de la casa alcanza para su medicina o para arreglar el carro. Si eligen la medicina, ¿qué prioridad están cuidando?",
         ["La medida justa", "La verdad", "La vida y la salud", "El tiempo"], 2,
         "La salud de la abuela va primero: cuidar la vida vale más que arreglar el carro."),
        ("Un vendedor dice que la fruta está fresca, pero está muy verde. Si tú lo aclaras con respeto, ¿qué prioridad estás cuidando?",
         ["La vida", "La verdad", "El tiempo", "La medida justa"], 1,
         "Decir lo que realmente es, sin exagerar, es cuidar la verdad, aunque no sea cómodo."),
        ("Entre dos amigos, uno hace todo el trabajo de la casa y el otro nada. ¿Qué prioridad se está olvidando?",
         ["La medida justa, porque nadie debería cargar más de lo que le toca", "La verdad", "El tiempo", "La vida"], 0,
         "Repartir parejo lo que cuesta es respetar la medida justa, para que ninguno quede agotado por culpa del otro."),
    ],
    "etica_la_vida_se_cuenta": [
        ("Al terminar el día, tu tío cuenta su jornada: \"me tomó 8 horas\", \"fue trabajo de verdad\", \"sirvió para dar de comer a mi familia\". ¿Qué está haciendo?",
         ["Vendiendo su día por plata", "Contando su actividad en tres números: cuánto duró, qué tan real fue y hacia dónde llevó", "Presumiendo de su esfuerzo", "Quejándose de su trabajo"], 1,
         "Ese es el modo de contar la vida: el tiempo que tomó, la verdad de lo hecho y el rumbo que le dejó."),
        ("Para decidir si una actividad valió la pena, ¿qué preguntas te ayudan a contarla?",
         ["¿Cuánto dinero dejó, qué dirán los demás y qué me conviene?", "¿Quién la vio, cuánto duró y qué me apuraba hacer después?", "¿Qué tan difícil fue, quién la pidió y me alcanzó para descansar?", "¿Cuánto tiempo tomó, qué tan real fue y hacia dónde llevó?"], 3,
         "Esas tres preguntas son las que cuentan una actividad en serio: su tiempo, su verdad y su dirección."),
        ("Una vecina te dice: \"trabajé todo el día, pero no sé a dónde me llevó\". ¿Qué número de su actividad le falta mirar?",
         ["Cuánto tiempo tomó", "Qué tan real fue", "Hacia dónde llevó, es decir su dirección", "Cuánto le pagaron"], 2,
         "Sin saber hacia dónde lleva el esfuerzo, el tiempo y la verdad no bastan para decidir si valió la pena."),
    ],
    "etica_el_minimo_que_todos_merecen": [
        ("En tu barrio proponen que todas las familias tengan acceso a la misma comida, agua, salud y escuela para sus hijos. ¿Qué se está garantizando?",
         ["Un techo común, para que nadie pueda superar a otro", "Que nadie pueda tener más que el resto", "Un piso común, un mínimo igual para todos", "Que los que ahorran deben repartir lo suyo"], 2,
         "El piso común es el mínimo que todos merecen por igual: comida, agua, salud, techo, escuela y vínculos."),
        ("Una familia vive justa y con lo necesario; otra ahorra, crece y llega a tener más. ¿Cuál es lo correcto con el piso y el techo?",
         ["La segunda rompió la regla porque no debe superar a nadie", "El piso común es para todos, y cada quien puede subir tan alto como quiera", "La primera debería enojarse porque no tiene lo mismo", "Solo una puede tener lo necesario"], 1,
         "El piso común se garantiza a todos; el techo no: cada persona llega tan alto como se lo proponga."),
        ("Si el dinero no alcanza para darle a todos el mismo lujo, ¿qué debería asegurarse primero para todas las personas?",
         ["Que nadie tenga más que el resto", "Que todos gasten igual", "Que los que ganan más den todo lo que tienen", "El mínimo de comida, agua, salud, techo, escuela y vínculos para todos"], 3,
         "Primero se garantiza el piso para todos; el techo no es igual, porque cada quien sube hasta donde pueda."),
    ],
    "etica_tu_tiempo_es_tuyo": [
        ("Alguien trabaja, duerme, descansa y comparte con su familia. ¿Qué está haciendo?",
         ["Un presupuesto vital, donde el descanso y el compartir también cuentan", "Una excusa para trabajar menos", "Un desorden, porque debería trabajar más", "Poner el sueño por encima de todo"], 0,
         "El presupuesto vital reparte el día en sueño, trabajo, descanso y compartir, sin dejar ninguna parte por fuera."),
        ("A tu hermano le ofrecen un turno extra bien pagado, pero así no dormiría nada. ¿Qué principio le ayuda a decir que no?",
         ["Que dormir es perder plata", "Que el tiempo no se puede organizar", "Que el descanso no se vende, aunque le paguen por perderlo", "Que si paga bien, siempre conviene"], 2,
         "El descanso y el sueño son tuyos y no están en venta: el dinero no manda sobre tu salud y tu pausa."),
        ("En tu casa quieren organizar el día para dormir bien, cumplir el trabajo, descansar y compartir en familia. ¿Cómo se llama esta forma de repartir la jornada?",
         ["Un exceso de descanso", "Una pérdida de tiempo", "Una forma de trabajar sin parar", "Un presupuesto vital, que reparte sueño, trabajo, descanso y compartir"], 3,
         "Es el presupuesto vital: repartir el tiempo entre sueño, trabajo, descanso y compartir, con cada parte en su lugar."),
    ],
    "etica_la_palabra_que_obliga": [
        ("Un amigo te promete devolverte las herramientas el sábado, pero también pides un papel firmado con dos testigos. ¿Por qué hacerlo?",
         ["Porque no confías en nadie", "Porque un acuerdo con testigos obliga por igual a ambos y evita malentendidos", "Porque los papeles se pierden", "Porque estás buscando pelea"], 1,
         "Ponerlo por escrito con testigos no es desconfiar: es que la promesa quede clara y obligue por igual a quien promete y a quien recibe."),
        ("Para que una promesa importante obligue de verdad, ¿qué conviene asegurar?",
         ["Solo la palabra dicha de viva voz", "Nada, porque prometer es suficiente", "Que se cumpla lo acordado y, si es importante, dejarlo por escrito con testigos", "Que nadie más se entere"], 2,
         "Cumplir es lo esencial, y dejarlo por escrito con testigos hace que la promesa sea clara y verificable para los dos."),
        ("Cuando alguien promete algo, ¿qué significa verificar antes de confiar plenamente?",
         ["Desconfiar y tratarle como a un embaucador", "Vigilarle todo el tiempo", "Exigir que prometa más", "Confirmar los hechos para no confundir confianza con descuido, porque verificar no es desconfiar"], 3,
         "Verificar es confirmar lo que se dijo para acordar con seriedad; eso no es desconfiar, es cuidar el acuerdo."),
    ],
    "etica_dar_y_recibir_con_medida": [
        ("Un amigo te pasa sus apuntes cuando faltaste a clase y tú quieres corresponderle, pero tu semana está llena. ¿Qué es una medida justa?",
         ["No devolver nada porque \"ya te ayudó sin esperar nada\"", "Devolverle algo que te cuesta poco y a él le sirve de verdad, aunque no sea exactamente igual", "Pagarte lo que valen sus apuntes en dinero", "Prometerle que algún día lo compensarás, sin plazo ni forma concreta"], 1,
         "La medida justa se mira entre los dos: no tiene que ser igual en cantidad, sino que ambos la acepten sin que a nadie le duela."),
        ("En el mercado, una señora que siempre te vende fruta te regala de vez en cuando una mazorca extra \"para la casa\". Tú no quieres quedar en deuda. ¿Qué haces con medida?",
         ["Le das las gracias y aceptas, porque dar y recibir con medida también es dejarse querer", "Le pides que ya no te dé nada para no deberle", "Le pagas la mazorca cada vez aunque ella insista en regalarla", "Le llevas toda tu compra a otro puesto para que \"la cosa no se confunda\""], 0,
         "Dar no empobrece cuando vuelve en cuidado o en confianza; la medida justa es que ambos se sientan bien, no hacer cuentas exactas."),
        ("Organizas un bazar comunitario. Alguien aporta mucho tiempo y otra persona aporta solo una libra de café. ¿Es justo?",
         ["No, quien aporta más tiempo debe recibir más de lo recaudado", "No, quien aporta poco no debería participar en el bazar", "Sí, si ambos lo aceptan con gusto: cada uno dio lo que podía y lo que dejó vuelve como cuidado y aprendizaje", "Solo es justo si cada uno aporta exactamente lo mismo"], 2,
         "La medida justa no se mide en lo aportado sino en que los dos lados la miren y la acepten sin que a ninguno le duela."),
    ],
    "etica_todo_lo_que_se_hace_se_ve": [
        ("En tu grupo, hiciste el compromiso de enseñar lectura a los niños los sábados (se anotó en el tablero común), pero esta semana no puedes ir. ¿Qué hace visible tu situación?",
         ["Avisar por adelantado para que el tablero y el grupo lo vean y puedan cubrirte", "No decir nada, porque es algo personal", "Avisar solo a un amigo de confianza, sin tocar el tablero", "Quejarte en privado de que el tablero \"te vigila\""], 0,
         "Los acuerdos se registran para que todos los vean; avisar y hacer visible el cambio mantiene la confianza sin meterte en tu vida privada."),
        ("En tu huerta comunitaria, anotaste que le pusiste agua al cultivo de don Carlos una tarde (se registra con quién y cuándo). Después don Carlos dice que no le regaste. ¿Qué resuelve esto?",
         ["Que cada quien lleve cuenta propia y ya", "Que el registro visible muestre que sí lo hiciste, y ambos puedan mirarlo", "Que se lo pregunte solo a la familia, porque \"es asunto de casa\"", "Que don Carlos mienta y no se pueda saber nada"], 1,
         "Lo que cuenta se registra y se ve: no para vigilar, sino para que las cosas queden claras entre los dos."),
        ("Una compañera te cuenta algo muy personal que le pasa en su casa. En la ciudad hay un espacio para registrar lo que se hace. ¿Qué corresponde?",
         ["Registrar ese relato personal para que quede \"a la vista\", porque todo se ve", "Registrar solo los compromisos y acuerdos que se tomaron, y guardar lo íntimo en privado: lo íntimo es sagrado", "Registrar todo, incluso lo íntimo, para no perder nada", "No registrar nada de lo que hablaron, porque \"nada se ve\""], 1,
         "Lo que se hace y se acuerda se ve; lo íntimo no se registra: la ciudad no mira la vida privada."),
    ],
    "etica_decidir_juntos": [
        ("En la asamblea del barrio proponen pintar las fachadas de azul. Tú piensas que el verde combina mejor con las casas. ¿Qué es lo correcto?",
         ["Callarte para no armar problema, porque la mayoría ya votó", "Decir lo que ves, aunque te quedes solo: la voz disidente tiene silla y puede ver lo que otros no ven", "Irte de la asamblea para no pelearte", "Convencer a tu familia para que protesten afuera"], 1,
         "La voz que piensa distinto no es un estorbo: tiene silla, porque muchas veces ve el riesgo o el detalle que los demás no ven."),
        ("Mañana hay votación para decidir si el fondo común se usa para el arreglo de la cancha o para la sede de salud. Tú habías dicho \"cancha\", pero esta tarde leíste datos que te hicieron cambiar. ¿Qué se espera de ti?",
         ["Mantenerte en \"cancha\" para no quedar como que cambias de opinión", "No volver a hablar del tema, porque ya te pronunciaste", "Cambiar de opinión sin vergüenza y explicar por qué: a veces cambiar es virtud, no debilidad", "Dejar que decidan los demás para no comprometerte"], 2,
         "Cambiar de opinión cuando aparece nueva información no es un papelón: es rectificar, y eso es una virtud."),
        ("En la votación, tu grupo de amigos salió con tu candidato, pero gana el otro. En la asamblea siguiente todos deben decidir cómo usar el espacio. ¿Qué manda?",
         ["Tu candidato, porque fue tu opción", "La decisión que se tomó entre todos, aunque no sea la tuya; manda la decisión, no la persona", "Los amigos, porque son mayoría en tu mesa", "Quien más hable en la asamblea"], 1,
         "Cuando se decide en común, manda la decisión tomada, no la persona que la propuso y tampoco la que la perdió."),
    ],
    "etica_cuidar_sin_cronometro": [
        ("Tu abuela está triste tras una pérdida y te va a visitar. Unos te dicen \"quédate una hora y te vas, no más\". ¿Qué es lo correcto?",
         ["Medir exactamente la visita para no \"perder tiempo\"", "Quedarte el tiempo que tu abuela necesite: el duelo y el cariño cronometrados se mueren", "No ir, porque eso no se puede medir", "Ir solo si puedes registrar el tiempo como una tarea"], 1,
         "Cuidar y acompañar en el duelo no se mide con reloj: son de las cosas sin medida, y al cronometrarlas se pierden."),
        ("Tú y tu vecina cuidan por turnos a un señor enfermo del barrio. La vecina se pasó una tarde entera y tú solo pudiste una hora. ¿Cómo se valora eso?",
         ["La vecina aportó más, así que merece más reconocimiento", "Ni cuenta tiene, porque \"cuidar no vale nada\"", "No se cronometra como un turno de fábrica: también cuenta la atención y el cariño, que no se miden con hora", "Lo justo es que todos cuiden exactamente la misma cantidad de horas"], 2,
         "Hay economía que da vida: cuidar no se mide en minutos; cuenta la presencia y el afecto, que no caben en un cronómetro."),
        ("Después de una pelea familiar, alguien te dice \"perdónalo ya, hace una semana que no le hablas\". ¿Qué es lo correcto?",
         ["Perdonar porque ya pasó el tiempo justo", "Apurar el perdón para que \"quede dentro del plazo\"", "No perdonar nunca, porque el perdón se mide", "Perdonar cuando de verdad estés listo: el perdón no se apura con cronómetro, necesita su tiempo"], 3,
         "El perdón es de las cosas que no se cronometran; forzarlo con medida lo echa a perder."),
    ],
    "etica_la_casa_grande": [
        ("En tu barrio hay quien cuida a los niños, quien barre la plaza, quien cultiva la huerta y quien enseña a leer. ¿Todos son parte de la casa grande?",
         ["No, solo quien \"trabaja de verdad\", es decir, quien construye", "No, lo que cuenta es producir para fuera del barrio", "Sí, todos los oficios hacen la casa: cuidar, construir, cultivar, enseñar y limpiar son igual de necesarios", "Solo quienes reciben pago por su tarea"], 2,
         "Ningún oficio sobra: cada uno sostiene la casa grande, y todos tienen su lugar en la mesa."),
        ("Tú sabes arreglar cañerías, pero este año nadie te lo ha pedido y te sientes sin lugar. En la asamblea, ¿qué te devuelve tu lugar en la mesa?",
         ["Quejarte de que nadie te valora", "Dejar de ir a la asamblea porque \"no aportas\"", "Recordar tu oficio y ofrecerlo: quien deja de ver su oficio pierde su lugar en la mesa", "Pedir que te paguen por adelantado"], 2,
         "Ver tu oficio y ponerlo al servicio de la casa te mantiene en la mesa; no importa que no lo pidan todos los días."),
        ("Don José, que cuidó la huerta toda su vida, ahora está viejo y casi no puede trabajar. Un vecino dice \"ya no sirve para nada\". ¿Qué es lo correcto?",
         ["Tiene razón: si no puede trabajar, no aporta", "En la casa grande no se pierde a quien llevó su oficio: su saber, su historia y su ejemplo siguen siendo parte de la mesa", "Don José debería irse a vivir a otra parte", "Solo importa lo que hace hoy, no lo que hizo toda la vida"], 1,
         "En la casa grande, el oficio y el saber de toda una vida no se borran: quien dio su oficio nunca pierde del todo su lugar."),
    ],
    "etica_el_idioma_de_la_ciudad": [
        ("\"Una actividad que duró 3 horas, fue de verdad y me llevó adelante deja una VHV.\" ¿Qué describe esta frase?",
         ["El agradecimiento que se cuenta", "La huella en tiempo, verdad y rumbo, que en la ciudad se llama VHV", "El piso que nadie cruza hacia abajo", "La palabra que obliga con verificación"], 1,
         "El tiempo que usaste, con lo que fue de verdad y hacia dónde te llevó, deja una huella: esa huella es la VHV."),
        ("Si \"tu tiempo propio\" es la medida con que valoras lo que haces, y en la ciudad eso tiene nombre, ¿cómo se llama?",
         ["TVI — el tiempo propio como medida de valor", "Maxo — el agradecimiento que se cuenta", "SDV — el piso que nadie cruza hacia abajo", "OEV — la casa grande de aprendizaje"], 0,
         "Usar tu tiempo propio para medir cuánto vale algo es la TVI: cada hora vivida cuenta como medida de valor."),
        ("En la ciudad existe \"el piso que nadie cruza hacia abajo\": si algo te deja por debajo de ese piso, no se va a hacer, aunque digan que conviene. ¿Cómo se llama ese piso?",
         ["EIR — el dar y recibir con medida", "VHV — la huella en tiempo, verdad y rumbo", "SDV — el piso que nadie cruza hacia abajo", "MaxoContract — la palabra que obliga con verificación"], 2,
         "Ese piso de no-humillación que protege a todos por igual se llama SDV: nadie cae por debajo de él."),
    ],
}


def _seed_materials(db_conn):
    """Siembra los enlaces del mundo (M15), idempotente por material_key.

    Se ejecuta en cada arranque para migrar también las bases existentes;
    INSERT OR IGNORE evita duplicar lo sembrado.
    """
    topic_ids = {
        row["slug"]: row["id"]
        for row in db_conn.execute("SELECT id, slug FROM topics").fetchall()
    }
    for slug, titulo, fuente, url in MATERIAL_LINKS:
        topic_id = topic_ids.get(slug)
        if topic_id is None:
            continue
        db_conn.execute(
            "INSERT OR IGNORE INTO materials "
            "(topic_id, material_key, titulo, tipo, fuente, url, contenido, autor, orden, created_at) "
            "VALUES (?, ?, ?, 'enlace', ?, ?, NULL, 'siembra', 50, ?)",
            (topic_id, f"{slug}#w1", titulo, fuente, url, _now()),
        )


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


def _migrate_db(conn):
    """Aplica migraciones ligeras e idempotentes para bases de datos existentes."""
    cursor = conn.execute("PRAGMA table_info(users)")
    columns = [row["name"] for row in cursor.fetchall()]
    if "maxo_user_id" not in columns:
        try:
            conn.execute("ALTER TABLE users ADD COLUMN maxo_user_id INTEGER")
            conn.execute(
                "CREATE UNIQUE INDEX IF NOT EXISTS idx_users_maxo_user_id ON users(maxo_user_id)"
            )
        except sqlite3.OperationalError:
            pass

    # Evidencia didáctica del aprendiz (M13): material de enseñanza propio
    # (texto, audio, video, imagen) — la vacuación sin muros.
    cursor = conn.execute("PRAGMA table_info(user_topics)")
    topic_columns = [row["name"] for row in cursor.fetchall()]
    if "evidence" not in topic_columns:
        try:
            conn.execute("ALTER TABLE user_topics ADD COLUMN evidence TEXT")
        except sqlite3.OperationalError:
            pass

    # Compartir la luz (M15): opt-in voluntario y retractable; 0 = la ciudad
    # no ve mi progreso (default; compartir es una decisión, nunca un default).
    cursor = conn.execute("PRAGMA table_info(users)")
    user_columns = [row["name"] for row in cursor.fetchall()]
    if "share_progress" not in user_columns:
        try:
            conn.execute(
                "ALTER TABLE users ADD COLUMN share_progress INTEGER NOT NULL DEFAULT 0"
            )
        except sqlite3.OperationalError:
            pass

    # Idioma de la persona (M16): la biblioteca se sirve en su lengua.
    cursor = conn.execute("PRAGMA table_info(users)")
    user_columns = [row["name"] for row in cursor.fetchall()]
    if "idioma" not in user_columns:
        try:
            conn.execute(
                "ALTER TABLE users ADD COLUMN idioma TEXT NOT NULL DEFAULT 'es'"
            )
        except sqlite3.OperationalError:
            pass

    # Idioma del material (M16): los idiomas conviven por material_key.
    cursor = conn.execute("PRAGMA table_info(materials)")
    material_columns = [row["name"] for row in cursor.fetchall()]
    if "idioma" not in material_columns:
        try:
            conn.execute(
                "ALTER TABLE materials ADD COLUMN idioma TEXT NOT NULL DEFAULT 'es'"
            )
        except sqlite3.OperationalError:
            pass


def init_db(app):
    """Crea las tablas y siembra el árbol sobre la base configurada."""
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    _migrate_db(conn)
    _seed(conn)
    _seed_etica(conn)
    _seed_materials(conn)
    conn.commit()
    conn.close()

