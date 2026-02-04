# Plan de Lanzamiento: GitHub Discussions

Este documento contiene el borrador y la estructura para el lanzamiento de la fase de feedback comunitario en GitHub Discussions.

## Estructura de Categorías Propuesta

1.  **📢 Anuncios**: Novedades oficiales y hitos del sprint.
2.  **💡 Ideas y Propuestas**: Espacio para sugerencias sobre el modelo Maxocrático o nuevas funcionalidades.
3.  **🐛 Reporte de Bugs**: Espacio técnico para fallos en el MVP de MaxoContracts o el Simulador.
4.  **⚖️ Debates Éticos**: Discusión sobre los Axiomas y los protocolos de retractación.
5.  **🤝 Cohorte Cero**: Coordinación para los participantes del primer experimento real.

---

## Borrador del Anuncio de Lanzamiento

**Título**: 🚀 ¡Lanzamiento de MaxoContracts MVP y Fase de Feedback (Sprint Día 14)!

Hola a todos,

Soy Max, y hoy cerramos la segunda semana de nuestro sprint intenso de 30 días. Hemos alcanzado un hito crítico: **MaxoContracts ya es una realidad funcional** (en su versión MVP Python).

### ¿Qué es MaxoContracts?
Es la Capa 4 de la Maxocracia. Son contratos inteligentes que no solo ejecutan transacciones, sino que validan **invariantes éticos** (Axiomas) en tiempo real. Si un acuerdo genera sufrimiento innecesario o viola el Bienestar Vital (Wellness Index), el contrato se bloquea o permite una retractación ética.

### ¿Cómo puedes ayudar?
Estamos buscando feedback en tres áreas:

1.  **El Código**: Revisa `maxocontracts/` en el repo. ¿Ves algún fallo en la lógica de los validadores?
2.  **La Simulación**: Prueba el **Nexus Simulator v2.2**. Hemos añadido un modelo no lineal de Bienestar. ¿Te parecen realistas los escenarios de la Cohorte Cero?
3.  **La Ética**: Lee el `Capítulo 18: MaxoContracts` en el libro. ¿Son suficientes los 15 axiomas temporales para proteger la dignidad vital?

### Próximos Pasos
Mañana empezamos la **Semana 3: Refinamiento**. Tu feedback aquí en Discussions alimentará directamente los ajustes finales antes del release v1.0.

¡Únete a la conversación y ayúdanos a construir una economía que respete el tiempo y la vida!

---
**Documentación Clave**:
- [Documentación de la API](https://github.com/maxnelsonlopez/maxocracia-cero/blob/main/docs/api/API.md)
- [Fundamentos de MaxoContracts](https://github.com/maxnelsonlopez/maxocracia-cero/blob/main/docs/architecture/maxocontracts/FUNDAMENTOS_CONCEPTUALES.md)

---

## Guía de Contribución Rápida (Developer Quickstart)

Si quieres probar el código localmente:

1. **Instalación**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Ejecutar Tests**:
   ```bash
   pytest tests/test_maxocontracts/
   ```
3. **Explorar el MVP**:
   Mira `maxocontracts/examples/simple_loan.py` para ver cómo se compone un contrato desde cero.

**¿Dónde buscar problemas?**
- Validadores en `maxocontracts/core/axioms.py`.
- Lógica de estados en `maxocontracts/core/contract.py`.
- Integración con el Oráculo Sintético en `maxocontracts/oracles/synthetic.py`.
