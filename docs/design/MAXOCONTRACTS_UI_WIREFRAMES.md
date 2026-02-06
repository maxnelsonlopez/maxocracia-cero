# MaxoContracts UI Wireframes

**Fecha:** 2026-02-04
**Estado:** Draft
**Contexto:** Capítulo 17 - Drag-and-Drop Interface

---

## 1. Concepto General: "El Lienzo de la Verdad"

La interfaz no parece un formulario legal. Se asemeja a un editor de lógica visual (estilo Scratch o Unreal Blueprints) pero con estética "Glassmorphism" y feedback biomimético (colores suaves que indican bienestar γ).

### Paleta de Estados
- **Neutro (Draft):** Grises translúcidos, vidrio esmerilado.
- **Válido (γ > 1):** Verde menta suave, brillo sutil.
- **Inválido/Riesgo (γ < 1):** Ámbar o rojo difuso, bordes pulsantes.
- **Conectado:** Líneas de flujo doradas.

---

## 2. Wireframe: Contract Builder (Constructor)

**Vista Principal:** Lienzo infinito con sidebar de bloques.

```ascii
+---------------------------------------------------------------+
|  MAXOCRACIA | Contracts > Nuevo Contrato                      |
+-------------------+-------------------------------------------+
| [ BLOQUES ]       |  [ LIENZO DE CONSTRUCCIÓN ]      (γ: 1.0) |
|                   |                                           |
| > Condiciones     |        +--------------+                   |
|   [Fecha]         |        | INICIO       |                   |
|   [Pago Maxo]     |        +-------+------+                   |
|   [Entrega]       |                |                          |
|                   |        +-------v------+                   |
| > Acciones        |        | CONDICIÓN    |                   |
|   [Transferir]    |   +--->| Si: Fecha    +--+                |
|   [Desbloquear]   |   |    | = 2026-03-01 |  |                |
|                   |   |    +--------------+  |                |
| > Validadores     |   |                      |                |
|   [SDV Check]     |   |    +--------------+  |                |
|   [Reciprocidad]--+   |    | ACCIÓN       |< +                |
|                       |    | Transf: 10 M |                   |
| [ MIS PLANTILLAS ]    |    | A -> B       |                   |
| - Prestamo Simple     |    +-------+------+                   |
| - Aseo Cohorte        |            |                          |
|                       |    +-------v------+                   |
|                       |    | ORÁCULO SDV  |                   |
|                       |    | Valida γ     |                   |
|                       |    +--------------+                   |
|                       |                                       |
+-------------------+---+---------------------------------------+
| PROPIEDADES       |  SIMULACIÓN: [ ▶ Ejecutar ]               |
| Seleccionado:     |  "Este contrato es seguro. γ esp: 1.2"    |
| Acción Transfer   +-------------------------------------------+
```

### Componentes Clave

1.  **Sidebar de Bloques (Izquierda)**:
    *   Categorías colapsables: Condiciones, Acciones, Validadores, Lógica (Y/O).
    *   Drag-and-drop hacia el lienzo.

2.  **Lienzo (Centro)**:
    *   Nodos conectables.
    *   Visualización de flujo de izquierda a derecha o arriba a abajo.
    *   Indicadores en tiempo real de VHV acumulado en cada rama.

3.  **Panel de Simulación (Abajo)**:
    *   Barra de estado "Semáforo Ético": Muestra si el contrato actual viola algún axioma.
    *   Cálculo de complejidad en tiempo real (determina si la UX de firma será Simple o Rigurosa).

---

## 3. Wireframe: Proceso de Aceptación (UX Adaptativa)

### Escenario A: Contrato Simple (Peso < 10)

```ascii
+--------------------------------------------------+
|  FIRMA RÁPIDA                                [X] |
+--------------------------------------------------+
|  Resumen:                                        |
|  "Te comprometes a limpiar la cocina 1 vez."     |
|                                                  |
|  Impacto VHV: T: 1.5h | V: 0 | R: 0.1            |
|                                                  |
|  [ ACEPTAR (Deslizar) >>>>>>>>>>>>> ]            |
+--------------------------------------------------+
```

### Escenario B: Contrato Riguroso (Peso > 50)

```ascii
+--------------------------------------------------+
|  REVISIÓN PROFUNDA (Paso 1 de 4)                 |
+--------------------------------------------------+
|  Este contrato compromete 30% de tu TVI mensual. |
|  Por favor, revisa cada término.                 |
|                                                  |
|  TÉRMINO 1: Exclusividad laboral (60h/sem)       |
|  [ Video Explicativo IA (30s) ]                  |
|                                                  |
|  Pregunta de control:                            |
|  ¿Qué pasa si te enfermas?                       |
|  ( ) Pierdo el trabajo                           |
|  (x) Se activa cláusula de pausa SDV             |
|                                                  |
|  [ Confirmar Término ]  [ Rechazar/Negociar ]    |
+--------------------------------------------------+
```

---

## 4. Flujo de Retractación Ética

**Modal de Emergencia:**

```ascii
+--------------------------------------------------+
|  SOLICITUD DE RETRACTACIÓN                       |
+--------------------------------------------------+
|  Contrato: Préstamo #402                         |
|                                                  |
|  Motivo:                                         |
|  [ Seleccionar... ]                              |
|   - Crisis de Bienestar (γ < 1)                  |
|   - Violación de SDV                             |
|   - Fuerza Mayor                                 |
|                                                  |
|  Evidencia (Opcional pero recomendada):          |
|  [ Adjuntar logs médicos / TVI ]                 |
|                                                  |
|  [ SOLICITAR EVALUACIÓN DE ORÁCULO ]             |
+--------------------------------------------------+
```

---

## 5. Especificaciones Técnicas UI

*   **Framework**: React Flow (para el lienzo de nodos).
*   **Estilos**: Tailwind CSS + Glassmorphism (backdrop-filter: blur).
*   **Animaciones**: Framer Motion (transiciones suaves para cambios de estado γ).
*   **Iconografía**: Lucide React (minimalista).
*   **Accesibilidad**: Soporte completo de teclado para navegación de nodos (ARIA graphs).
