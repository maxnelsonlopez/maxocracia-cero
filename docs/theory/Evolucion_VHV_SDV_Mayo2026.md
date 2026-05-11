# Evolución del Vector de Huella Vital (VHV): Integración del Suelo de Dignidad Vital (SDV)

**Fecha:** Mayo 2026  
**Estado:** Propuesta Avanzada de Implementación  
**Contexto:** Migración del Motor Económico a Next.js (Segmento 2)

## 1. Introducción: De lo Biológico a lo Dignatario

Originalmente, el componente **Vida (V)** del VHV se centraba en la cuantificación de las unidades de vida consumidas (especialmente de otras especies) y el sufrimiento asociado. La evolución de mayo de 2026 integra el concepto de **Suelo de Dignidad Vital (SDV)**, transformando la métrica en un indicador integral de la salud ética de un proceso productivo.

En este nuevo paradigma, el precio de un bien no solo refleja el tiempo invertido o los recursos naturales, sino la **calidad de vida de todos los seres sintientes involucrados** en su creación.

## 2. El Suelo de Dignidad Vital (SDV) como Parámetro Base

El SDV define los mínimos existenciales requeridos para una vida digna en 7 dimensiones críticas:
1.  **Subsistencia Física:** Agua, nutrición, vivienda.
2.  **Salud y Bienestar:** Atención sanitaria, aire limpio, descanso.
3.  **Seguridad:** Integridad física y jurídica.
4.  **Educación y Desarrollo:** Acceso al conocimiento y tecnología.
5.  **Conexión Social:** Vínculos de confianza y participación comunitaria.
6.  **Trabajo Significativo:** Jornadas justas y propósito.
7.  **Libertad:** Ejercicio de derechos fundamentales.

## 3. Integración en la Fórmula VHV

La nueva estructura del componente **V** integra la **Violación del SDV** como un factor de encarecimiento ético. 

$$V_{total} = V_{biológico} + \sum (V_{SDV})$$

Donde $V_{SDV}$ se calcula como el déficit acumulado de dignidad de los participantes en la cadena de valor:

$$V_{SDV} = \sum \left( (SDV_{requerido} - SDV_{actual}) \cdot \text{Intensidad} \right)$$

### Impacto en el Precio Maxo
Cualquier producto producido bajo condiciones que violen el Suelo de Dignidad Vital verá su precio en Maxos incrementado exponencialmente. Esto genera un desincentivo económico automático para las prácticas explotadoras o degradantes, haciendo que lo "inmoral" sea económicamente inviable dentro del sistema.

## 4. Propuestas de Mejora para la Experiencia de Usuario (Mayo 2026)

Para hacer tangible esta teoría avanzada, se proponen las siguientes implementaciones en el frontend:

### A. Narrativa Vital (Visual Storytelling)
En lugar de mostrar solo números abstractos, la interfaz traducirá los valores del SDV a narrativas humanas:
*   *Ejemplo:* "Este producto fue creado respetando el 100% de los parámetros de descanso y salud de sus productores."
*   *Alerta:* "Atención: Este producto tiene un recargo ético del 15% debido a una violación en la dimensión de Agua Potable en la zona de producción."

### B. Sandbox de Simulación Económica
Una herramienta que permita a los administradores y ciudadanos simular cómo un cambio en los umbrales del SDV (ej: aumentar el requerimiento de m² por vivienda) afectaría los precios de los productos en toda la red.

### C. Linaje de Precio (Auditoría Blockchain)
Cada cálculo de VHV guardado incluirá un "Snapshot de Dignidad", un registro inmutable de las condiciones de SDV vigentes en el momento del cálculo, permitiendo una trazabilidad ética total desde el consumidor hasta el origen.

## 5. Próximos Pasos en el Backend

1.  **Actualización de Esquemas:** Incluir los 7 campos de dimensiones de SDV en la tabla `vhv_products`.
2.  **Lógica de Penalización:** Implementar la función de peso para que los déficits de SDV actúen como multiplicadores en la función de valoración Maxo.
3.  **API de SDV:** Crear endpoints para que el Oráculo Dinámico (OD) actualice los mínimos de dignidad según el consenso comunitario.

---
*Este documento constituye la base teórica para la siguiente fase de desarrollo de la Inteligencia Económica de la Maxocracia.*
