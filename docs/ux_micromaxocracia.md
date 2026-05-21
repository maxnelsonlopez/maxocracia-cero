# Diseño de Experiencia de Usuario (UX) e Interfaz (UI) - MicroMaxocracia

Este documento establece de forma permanente las directrices de Experiencia de Usuario (UX) y la descripción de la Interfaz de Usuario (UI) para el módulo de **MicroMaxocracia (Capítulo 16 - Equidad Doméstica y Salud Relacional)**.

---

## 1. Filosofía de Diseño y Experiencia de Usuario (UX)

La MicroMaxocracia tiene como fin visibilizar el trabajo reproductivo, de cuidado y del hogar (CDD), equilibrar la economía familiar con respecto a los ingresos financieros (CEH) y la energía vital disponible (TED), y salvaguardar la salud física y psicológica de los miembros del hogar mediante la Escala de Seguridad Relacional (ESI).

Por tanto, el diseño UX se rige por tres pilares fundamentales:
1. **Seguridad y Confidencialidad Primero**: Evitar la coerción mediante bloqueos de interfaz no eludibles si la encuesta de seguridad (ESI) detecta un puntaje de riesgo ($\ge 3$).
2. **Carga Cognitiva Reducida**: Facilitar la carga de tareas domésticas diarias a través de preconfiguraciones (presets) y selectores rápidos.
3. **Equidad Visual**: Representar gráficamente el balance relacional de forma equilibrada, sin penalizar visualmente a los miembros con menores ingresos monetarios, destacando en cambio su aporte energético y de tiempo vital.

---

## 2. Descripción de la Interfaz (UI)

La interfaz del módulo de MicroMaxocracia está desarrollada con **React, Next.js** y **Vanilla CSS** con diseño responsivo, utilizando técnicas de *glassmorphism* (fondos semi-transparentes difuminados), gradientes sutiles y micro-animaciones en hover para proveer una experiencia premium y viva.

### A. Vista de Configuración del Hogar
*   **Hogar Activo**: Si el usuario no pertenece a un hogar, se le presenta una pantalla limpia con dos opciones claras:
    *   *Crear Hogar*: Campo de texto con auto-foco y un botón de gradiente para generar el código de invitación único.
    *   *Unirse a un Hogar*: Caja de entrada de texto optimizada para códigos alfanuméricos y botón de validación instantánea.
*   **Parámetros Personales**: Formulario minimalista con deslizadores interactivos para definir los parámetros de base del miembro:
    *   Ingresos Mensuales monetarios (COP/USD).
    *   Horas semanales de trabajo formal.
    *   Horas semanales de transporte/desplazamiento.
    *   Horas semanales de sueño (por defecto 56).
    *   *Métrica de salida*: El sistema muestra en vivo las horas de **Energía Vital Disponible (TED)** semanales restantes.

### B. El Registro de Tareas (CDD Task Logger)
*   **Formulario de Carga Rápida**: Caja flotante con un selector de presets domésticos comunes (Cocinar, Limpieza, Cuidado Infantil, Reparaciones, Administración del Hogar).
*   **Cálculo en Vivo de VHV**: A medida que el usuario ajusta las horas y factores, una tarjeta animada muestra el valor acumulado del **Vector de Huella Vital Doméstico (VHV)** mediante la fórmula:
    $$\text{VHV} = \text{Duración} \cdot (\text{Esfuerzo} \cdot \text{Carga Mental} \cdot \text{Alcance}) \cdot \text{FIC}$$
*   **Multiplicador de Intensidad Contextual (FIC)**: Desplegables discretos para añadir factores agravantes:
    *   *Atención*: Si la tarea requiere foco total (+10%).
    *   *Fragmentación*: Si es interrumpida continuamente (+15%).
    *   *Soledad*: Si se ejecuta de forma aislada sin interacción constructiva (+5%).

### C. El Dashboard de Balances (Las Tres Cuentas)
*   **Visualización de Distribución**: Tres filas de gráficos de barras horizontales apiladas que muestran la proporción de cada miembro sobre el total del hogar:
    1.  *Barra CDD (Contribución Directa Doméstica)*: Compara el VHV total aportado por cada miembro.
    2.  *Barra CEH (Contribución Económica al Hogar)*: Compara el aporte de dinero formal.
    3.  *Barra TED (Tiempo y Energía Disponible)*: Compara el cansancio relativo (a mayor horas de trabajo externo/transporte, menor es el TED restante).
*   **Indicador de Equidad Global**: Un dial circular (o barra de progreso indexada) que calcula el porcentaje de equilibrio de cada miembro con base en la fórmula de ponderación ética:
    $$\text{Equilibrio} = 0.6 \cdot CDD\% + 0.3 \cdot CEH\% + 0.1 \cdot TED\%$$
    Si las diferencias individuales superan el $\pm 15\%$, la interfaz tiñe los bordes en un tono ámbar indicando "Desbalance Relacional Detectado".

### D. Protocolo ESI de Seguridad y Camuflaje Seguro (Safe Camouflage Mode)
*   **Frecuencia**: Se le solicita al usuario responder la encuesta ESI en el primer inicio de sesión o para reconfigurar el acceso al ledger del hogar.
*   **Flujo UX de Camuflaje (Stealth)**:
    *   Si la encuesta de seguridad relacional (ESI) detecta riesgo ($\ge 3$ respuestas afirmativas), el sistema **NO** muestra una pantalla de bloqueo roja o estática (lo cual podría despertar sospechas o furia en un agresor que vigile el dispositivo).
    *   En su lugar, activa el **Modo de Camuflaje Seguro**: la interfaz carga un dashboard idéntico al real pero alimentado con datos simulados y equilibrados ("Hogar Nelson-Lopez", contribuciones de ~50%, índices de salud excelentes).
    *   **Simulación Local Interceptada**: Toda acción de escritura (registrar tareas CDD, guardar auditorías) es interceptada por el frontend. Muestra un aviso de éxito local y actualiza los listados en memoria de manera dinámica, pero **nunca** realiza la llamada HTTP al backend (evitando que los errores de bloqueo del servidor delaten el estado de seguridad).
    *   **Atajo de Teclado y Botón de Pánico (Quick Escape)**: Un discreto botón flotante de "Salida Rápida (Esc)" y el atajo de la tecla `Esc` redirigen instantáneamente al usuario a un artículo genérico sobre Economía Doméstica en Wikipedia.
    *   **Puerta Trasera de Soporte**: En la parte inferior, un discreto enlace de "Soporte y Privacidad del Hogar" abre el modal confidencial donde se exponen las líneas de ayuda (Línea 155, 141) y se permite reiniciar la encuesta de seguridad (ESI) de forma segura.

### E. Monitor Relacional y Protocolo Detox
*   **Panel de Índices Relacionales**: Muestra tres tarjetas flotantes animadas con los niveles calculados a partir de las auditorías periódicas:
    1.  **ICE** (Índice de Conflicto Escalado): Proporción de altercados graves en el período (Umbral crítico: $\ge 3.0$).
    2.  **IDB** (Índice de Deterioro de Bienestar): Relación de fatiga, insomnio y desgaste relacional (Umbral crítico: $\ge 5.0$).
    3.  **IDP** (Índice de Desequilibrio Persistente): Desviación acumulada en el reparto del CDD (Umbral crítico: $\ge 0.50$ o $\ge 0.40$ en 8+ semanas).
*   **Banner de Detox Activo**: Si dos o más de estos índices superan el umbral tolerable, se activa el **Protocolo de Desintoxicación Doméstica**, bloqueando el registro de CDD durante 14 días para desactivar la competitividad métrica y promover la comunicación facilitada tradicional.

