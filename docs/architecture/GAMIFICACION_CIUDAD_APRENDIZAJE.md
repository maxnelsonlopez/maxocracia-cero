# La Ciudad del Saber — gamificación con guardarraíles (M14)

> **Sesión**: 29-08-2026 (idea de Max: "el conocimiento como ciudad que se forma
> mientras aprendes"). **Estado**: Fase 1 implementada — vista de mapa-ciudad,
> niebla, lore por barrio, compañero de sugerencias. OEV §1.5 (chequeos
> gamificados con guardarraíles) como canon.

## 1. La metáfora

El conocimiento **vive mezclado** (en la vida no hay casilleros), pero la
persona necesita orientarse. La ciudad del saber es un **mapa que se ilumina**:

| Ciudad | Sistema | Estado visual |
|---|---|---|
| Barrio | Rama del árbol (8) | Niebla → iluminado cuando construyes en él |
| Lote | Tema | 🔒 bloqueado · ◽ libre · 🔨 en obra · ✅ aprobado · ✨ listo para enseñar · 🏛 dominado |
| Avenida | Camino de prerrequisitos (maestría, no años) | Se revela al caminar |
| Plaza mayor | El Foro Abierto (:5001) | Nada se encierra en la ciudad: la plaza es global |
| Lore | Historia de cada barrio | Se revela al entrar — la curiosidad, sin spoilers |

## 2. Motores de los videojuegos → cómo los usamos (y qué NO)

| Motor de juego | Cómo lo adaptamos | Guardarraíl (OEV §1.5) |
|---|---|---|
| **Niebla de guerra** (curiosidad) | Los barrios lejanos se insinúan grises, no se ocultan | Ver no es poseer: lo gris invita, nunca frustra |
| **Mapa que se revela** (progreso visible) | Lotes con estados claros; la ciudad es tu biografía de obra | "Estado, no tribunal": el mapa muestra estados, jamás quién va mejor |
| **Guía de la mano** (M14) | El compañero sugiere el siguiente lote (rama con más progreso, lo sencillo primero) | Sugerencia, nunca obligación: sin misiones fallidas ni plazos |
| **Lore/narrativa** (historia revelada) | 2 frases por barrio que conectan la rama con la vida real | Sin arte audiovisual que "enganche": la curiosidad es el motor, no el brillo |
| **Hitos con celebración** | Al dominar un tema: obra visible en el barrio (🏛) | Celebración compartida; **cero rankings, cero puntos comparativos** |
| **Repetición espaciada** (anti-δ) | Fase 2: lotes "mantenidos" con Rondas (la base nunca se gradúa) | Repasar no se castiga: el que más Ronda necesita, más acompañado va |
| — | — | **PROHIBIDO**: ranking de personas, cronómetro del ensayo-error, loot aleatorio, recompensas por azar |

## 3. Fase 1 — implementado (29-08)

- `GET /api/suggest` (el compañero): prioriza la rama del usuario con más
  progreso y lotes libres; primero lo sencillo. 3 tests.
- Vista **"La ciudad"** (toggle Árbol ↔ Ciudad): barrios con niebla/lore, lotes
  con estados; clic → empezar (libre), test (en obra), o árbol (detalles).
- Lore de los 8 barrios escrito en `static/app.js` (`CITY_LORE`).
- Verdad sin engaño: `test_passed` + material = ✨ (listo para enseñar), no 🏛.

## 4. Fases siguientes (propuestas, sin cerrar)

1. **Rondas de mantenimiento** (δ): lotes dominados se marcan "requiere Ronda"
   después de N semanas sin tocar; repasarlos devuelve 🏛 brillante. Teoría: OEV
   §1.1 (la base nunca se gradúa).
2. **Itinerarios** (misiones opcionales): grupos temáticos sugeridos ("ruta del
   huerto: naturaleza → matemáticas → economía del hogar") — caminos a todas
   partes, ninguno obligatorio: la ciudad no tiene muros.
3. **Cartografía compartida**: ver barrios iluminados por la comunidad (como la
   luz de los ojos de la ciudad) sin revelar quién hizo qué (privacidad T13).

## 5. Referencia

- OEV §1.5 chequeos con guardarraíles (docs/theory/ESTRUCTURA_IDEAL_ORGANISMO_EDUCATIVO_VITAL.md).
- Entropía del conocimiento δ y Rondas §1.1 del mismo doc.
- Auditoría de UX previa: `docs/architecture/MEJORAS_PLATAFORMA_EDUCATIVA_auditoria_2026-08-29.md`.
