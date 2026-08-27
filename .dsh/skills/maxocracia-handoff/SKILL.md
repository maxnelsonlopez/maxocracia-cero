---
name: maxocracia-handoff
description: Usar al final de una sesión de trabajo en Maxocracia-Cero o al preparar una continuación — para actualizar SESION_NEXT_PROMPT.md, los mapas de coherencia si cambió teoría o implementación, y dejar el próximo prompt de continuidad listo sin duplicar notas sueltas en la raíz.
---

# Handoff de sesión (Maxocracia-Cero)

Las sesiones de este proyecto son largas y continuas. El handoff correcto decide si la próxima sesión arranca con contexto o vuelve a explorar desde cero.

## Qué actualizar SIEMPRE al terminar

1. **`SESION_NEXT_PROMPT.md`** (raíz) — el contrato de continuidad:
   - `Estado actual`: qué se cambió en la sesión (archivos, commits, tests) y qué quedó funcionando.
   - `Pendientes`: próximos pasos concretos, cada uno con su archivo de referencia.
   - `Prompt de continuidad`: 3-8 líneas que un agente nuevo pueda leer como arranque ("continúa desde…", "no tocar…", "primero leer…").
   - `Decisiones`: notas de diseño tomadas (con su porqué) para no re-discutirlas.
2. **Mapas de coherencia** si cambió teoría↔implementación: `docs/architecture/mapa_coherencia_ola4.md` (obligatorio por Ola), `requisitos_fase2_ola4.md`, `mapa_frontend_ola4.md`, `mapa_trazabilidad_canonica.md`.
3. **`TODO.md`** si hay trabajo pendiente no urgente que debe quedar visible.

## Higiene de notas sueltas

- Los archivos de notas en la raíz ("Finalizing Maxocracia Frontend Migration", "Segment 2 SDV panel analyzer", etc.) son outputs de sesiones previas: NO son código vivo y no deben editarse como si lo fueran.
- Si una nota de sesión tiene valor duradero: moverla a `docs/reports/` o `docs/design/` con nombre claro (fecha + tema) y actualizar el handoff; si no, no dejar más archivos sueltos en la raíz.
- Nunca duplicar: si el contenido es un subconjunto de un doc vivo, actualizar el doc vivo y descartar la nota.

## Plantilla de prompt de continuidad

```
[CONTINUACIÓN] Proyecto: Maxocracia-Cero (Ola 4). Esta sesión:
- Hizo: <resumen con rutas>
- Estado de tests: <verde/rojo — cuáles>
- Pendiente inmediato: <tarea con ruta>
- Regla especial: <p. ej. "NO reintroducir load_dotenv en voting_oracle.py">
Primero lee: AGENTS.md, docs/architecture/mapa_coherencia_ola4.md (sección X), <rutas de los archivos tocados>.
```

## Regla de oro

El handoff se escribe para el agente de la próxima sesión Y para Max: si una persona no puede retomar el hilo leyendo solo `SESION_NEXT_PROMPT.md`, el handoff está incompleto.
