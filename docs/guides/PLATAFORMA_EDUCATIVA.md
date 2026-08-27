# Plataforma Educativa Independiente (prototipo del OEV)

> **Qué es:** una plataforma **independiente pero compatible** con Maxocracia-Cero — el primer prototipo vivo del **Organismo Educativo Vital** (OEV; ver `docs/theory/ESTRUCTURA_IDEAL_ORGANISMO_EDUCATIVO_VITAL.md`), que vive en `plataforma_educativa/`.
> **Condición de diseño (Max, 2026):** simple; registro **sin email obligatorio** (usuario + contraseña bastan); perfil que guarda el progreso.
> **Estado:** MVP funcional con tests — la primera célula educativa de la Maxocracia que se puede tocar.

---

## 1. Qué materializa

| Componente OEV (concepto) | Implementación en la plataforma |
|---|---|
| **Árbol de habilidades** (especialización desbloqueada por maestría) | 8 ramas sembradas: Matemáticas, Higiene y salud, Relaciones sociales, Lectura, Escritura, Lenguaje e idiomas, Naturaleza, Computadores — con temas, prerrequisitos y dificultad |
| **Maestría verificada** (sin examen único) | Test virtual de capacidad por tema: ≥70% → `test_passed`; el nodo se gana además con mentoría (leader 1 reunión) — la *vacuación*: para avanzar/ser monitor hay que haber enseñado |
| **Células** (grupos de ~8, coordinados, con propósito) | **Reuniones semanales automáticas**: 8 estudiantes idealmente, máx 8, min 3; temas elegidos del árbol por **refuerzo necesario** (debilidades del grupo) |
| **Monitores que ganaron el skill enseñando** | Monitor = usuario con el tema `test_passed` + `mentor_rounds ≥ 1` (ya está pasando su etapa de mentoría) |
| **Reunión por cercanía de temas** | Si hay más población de la que cabe, la agrupación junta perfiles con **debilidades relativamente cercanas** — no todos tienen que haber visto todo |
| **Perfil y progreso** | `users` + `user_topics`: estado por tema, mejor score, rondas de mentoría — todo por perfil, sin email |
| **Disponibilidad** | Cada usuario declara su semana (días/horas) y el planificador conjuga disponibilidad + debilidades + monitores |

## 2. Independencia y compatibilidad

- **Independiente**: su propio servidor (puerto **5050**), su propio SQLite, su propio `requirements.txt` — no comparte nada con `app/` (Maxocracia, puerto 5001).
- **Compatible por diseño**: mismos conceptos (`Árbol`, `maestría`, `célula`, `mentoría`, `T13`: el progreso es auditable por perfil), y el roadmap de integración está abierto: conectar el árbol al matching de Maxocracia (necesidades→grupos de solución), el perfil a `guide_bp` (convalidación del saber de entrada) y las reuniones a la gobernanza (`voting_bp`: el árbol se co-diseña).
- **Primer usuario registrado = coordinador** (bootstrap documentado; en producción la coordinación es rotativa por parlamento).

## 3. Cómo usar (resumen)

1. Registrarse (solo usuario y contraseña) → perfil con progreso.
2. Explorar el árbol (8 ramas, ~35 temas), hacer los tests virtuales (≥70%).
3. Declarar disponibilidad semanal → el sistema genera reuniones automáticas por debilidades cercanas.
4. Quien aprobó un tema y ya lideró una reunión se convierte en **monitor** de ese tema (comienza su etapa de mentoría).
5. Ver/inscribirse en reuniones; el monitor marca asistencias.

Detalles técnicos, comandos y límites: `plataforma_educativa/README.md`.

## 4. Límites honestos (lo que el MVP no hace aún)

- La **triada de mentoría** (mentor + par + oráculo con veto) del OEV: hoy el `request-mentorship` es un flag de plantilla; el canal oráculo es trabajo futuro.
- Sin integración con `app/matching.py` (necesidades→grupos de solución) — puente M4.
- La gamificación cooperativa (chequeos sin rankings) y el foro abierto son hitos M2/M5 del [ROADMAP_RAMA_EDUCATIVA.md](../architecture/ROADMAP_RAMA_EDUCATIVA.md).
- El "sin permiso, con libertad": la plataforma corre en cualquier máquina; la ley y el marco defensivo aplican igual que al proyecto.

## 5. Ubicación

- Código: `plataforma_educativa/` (backend Flask + SQLite + frontend estático + tests).
- Este documento: la hoja de ruta conceptual del prototipo → OEV → plataforma Maxocracia.
