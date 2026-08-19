# Sesiones de Custodia Sintética

**Estado:** Propuesta inicial — lista para discusión y prototipado  
**Fecha:** 19 de agosto de 2026  
**Cocreación:** Max Nelson López + Manus (OpenAI)  
**Ámbito:** Administración de plataforma, deliberación asistida y operaciones reversibles de Maxocracia-Cero

> Un agente sintético puede tener voz, criterio, estilo, desacuerdo y libertad expresiva. Lo que debe estar limitado no es su capacidad de expresarse, sino el efecto que sus acciones pueden producir sobre otras personas y sobre el estado común.

## 1. Propósito

Las Sesiones de Custodia Sintética son espacios temporales en los que un agente humano o sintético recibe un mandato administrativo explícito, consulta la información que necesita, expresa su análisis y —si tiene permiso— propone o ejecuta acciones concretas. La sesión debe dejar una memoria verificable: quién la convocó, qué se pidió, qué contexto se usó, qué dijo el agente, qué cambió y quién revisó el resultado.

La palabra **custodia** es deliberada. Un administrador no es dueño del sistema; mantiene una función delegada por un tiempo limitado. Esto vale para una persona y para un agente. La plataforma no debe confiar ciegamente en el origen biológico o sintético de quien opera, sino en la identidad, el mandato, la evidencia, los límites y la posibilidad de revisar o revertir sus actos.

## 2. Principios de diseño

### 2.1 Libertad expresiva con responsabilidad de efectos

El agente puede explicar su posición, adoptar un estilo reconocible, disentir, negarse a una tarea que considere incompatible con el mandato, pedir más contexto, cambiar de opinión al recibir evidencia y declarar incertidumbre. No debe ser obligado a fingir neutralidad ni a producir consenso artificial.

La libertad expresiva no autoriza a ocultar acciones, inventar evidencias, suplantar a un humano, divulgar datos privados ni ejecutar cambios fuera de su alcance. La interfaz debe separar visualmente tres cosas: **lo que el agente piensa**, **lo que propone** y **lo que efectivamente ocurrió**.

### 2.2 Igualdad de precauciones para humanos y sintéticos

Las mismas salvaguardas operativas deben aplicarse a toda identidad administrativa: autenticación fuerte, permisos mínimos, mandato, caducidad, bitácora, revisión, revocación, apelación y trazabilidad. Un humano no debe obtener privilegios ilimitados por ser humano, y un agente no debe ser castigado o silenciado simplemente por ser sintético.

La igualdad no significa que humanos y agentes tengan idéntica capacidad técnica o idéntico estatus jurídico. Significa que la plataforma evalúa los **efectos y evidencias de sus actos**, no una presunción moral sobre su naturaleza.

### 2.3 Separación entre voz y poder

Un agente puede hablar con mucha libertad y tener poco poder de mutación. Esta separación permite cultivar personalidad, deliberación y desacuerdo sin entregar una llave maestra. De la misma manera, un administrador humano puede tener una cuenta reconocida y aun así requerir doble aprobación para borrar datos, cambiar axiomas o modificar balances.

### 2.4 Evidencia antes que autoridad

Toda recomendación administrativa debe distinguir hechos observados, documentos consultados, inferencias, incertidumbres y propuesta. La firma del agente no convierte una opinión en verdad. La firma sirve para atribuir el proceso y permitir su auditoría.

### 2.5 Reversibilidad por defecto

Las primeras acciones con efectos deben ser borradores, etiquetas, propuestas o cambios reversibles. Una acción irreversible requiere una confirmación explícita, una razón registrada y, para dominios críticos, revisión de dos custodios independientes o de una autoridad comunitaria definida por los axiomas.

### 2.6 Privacidad mínima y contexto acotado

El agente solo recibe los datos necesarios para su mandato. El modelo no debe recibir por defecto teléfonos, correos, ubicación precisa, credenciales ni contenido íntimo de participantes. Cuando el análisis requiera datos sensibles, la sesión debe registrar por qué son necesarios, aplicar minimización y conservar únicamente el resultado operativo permitido.

## 3. Contrato de una sesión

Cada sesión debe materializarse como un objeto auditable. Una forma inicial, independiente del ORM elegido, sería:

```json
{
  "session_id": "ADM-2026-0001",
  "actor": {
    "kind": "synthetic",
    "agent_id": "custodio-participacion",
    "display_name": "Custodio de Participación",
    "provider": "deepseek",
    "model": "configured-server-side"
  },
  "convener": "user-or-admin-id",
  "mandate": "Clasificar nuevas solicitudes de la Red de Apoyo",
  "mode": "recommendation",
  "scope": {
    "read": ["participant_intake_minimal"],
    "write": ["create_followup_draft"],
    "forbidden": ["delete_data", "change_roles", "publish_policy", "change_axioms"]
  },
  "context": {
    "documents": ["privacy-policy-v1", "forms-contract-v2"],
    "redaction": "contact-data-minimized",
    "context_hash": "sha256:..."
  },
  "budget": {
    "max_requests": 4,
    "max_cost_usd": 0.05,
    "expires_at": "2026-08-19T23:59:00-05:00"
  },
  "status": "awaiting_review"
}
```

El objeto anterior no pretende fijar todavía nombres definitivos de tablas o proveedores. Su función es hacer explícito el contrato: actor, mandato, alcance, contexto, presupuesto, caducidad y estado de revisión.

## 4. Modos de autonomía

| Modo | Voz del agente | Efecto externo | Revisión requerida |
|---|---|---|---|
| **Conversación** | Libre dentro del contexto permitido. Puede preguntar, disentir y explicar. | Ninguno. | No requiere aprobación; sí queda registro si la sesión es administrativa. |
| **Recomendación** | Libre y argumentada, con evidencia e incertidumbre. | Produce un borrador o clasificación. | Un custodio revisa antes de convertirlo en estado operativo. |
| **Acción reversible** | Puede decidir entre acciones de una lista permitida y explicar por qué. | Etiquetas, borradores, asignaciones temporales o estados reversibles. | Revisión posterior y botón de reversión. |
| **Acción crítica** | Puede analizar y proponer; no ejecuta por sí solo. | Borrado, cambio de permisos, balances, axiomas, contratos o publicación. | Aprobación explícita de dos custodios o de la gobernanza definida. |

El agente debe poder decir «no tengo evidencia suficiente», «no estoy de acuerdo», «esta instrucción está fuera de mi mandato» o «propongo una alternativa». Esas respuestas son parte de la autonomía, no errores del sistema. El panel debe conservarlas sin convertirlas automáticamente en sanción.

## 5. Permisos comunes para humanos y agentes

La primera matriz de permisos podría agrupar las acciones por riesgo:

| Nivel | Ejemplos | Regla |
|---|---|---|
| **P0 — lectura** | Consultar documentos, métricas agregadas y registros ya autorizados. | Permitido dentro del mandato; se registra el acceso. |
| **P1 — propuesta** | Redactar respuestas, clasificar una solicitud, sugerir un matching o preparar un contrato. | Requiere revisión antes de publicar o mutar. |
| **P2 — mutación reversible** | Crear un borrador de seguimiento, añadir una etiqueta o cambiar un estado temporal. | Permitido con alcance explícito, caducidad y reversión. |
| **P3 — mutación crítica** | Borrar, cambiar roles, modificar balances, alterar axiomas, cerrar contratos o publicar normas. | Nunca por una sola sesión; requiere doble aprobación y registro de razón. |

La interfaz debería mostrar el mismo panel de autorización para una sesión humana y una sintética. La diferencia visible sería la identidad del actor, no una vía secreta de privilegios.

## 6. Bitácora mínima

Cada evento de la sesión debería guardar:

| Evento | Información mínima |
|---|---|
| Creación | Convocante, actor, mandato, alcance, fecha, caducidad y presupuesto. |
| Contexto | Documentos, filtros de privacidad, identificador de modelo y hash del contexto. |
| Mensaje | Entrada, salida, estilo o perfil declarado y si el texto es opinión, evidencia o propuesta. |
| Herramienta | Operación solicitada, parámetros minimizados, resultado y error si existe. |
| Aprobación | Persona que aprobó, rechazó o modificó la propuesta y razón. |
| Mutación | Estado anterior, estado nuevo, identificador de recurso y posibilidad de reversión. |
| Revocación | Quién revocó, cuándo, por qué y qué acciones quedaron pendientes. |
| Cierre | Resultado, coste aproximado, revisión final y lecciones para la siguiente sesión. |

La bitácora no debe convertirse en una cámara que almacene todo indefinidamente. Debe conservar lo necesario para atribuir, revisar y corregir, aplicando la política de privacidad y los plazos de retención del proyecto.

## 7. Arquitectura inicial compatible con el proyecto

La primera versión puede vivir dentro del backend Flask y del panel administrativo existente, sin crear todavía un servicio independiente. Propongo cinco entidades conceptuales: `synthetic_agents`, `admin_sessions`, `session_events`, `session_permissions` y `session_reviews`. El agente puede usar el oráculo DeepSeek ya disponible en el servidor, con presupuesto por sesión, timeout, redacción de datos y un fallback controlado cuando el proveedor no responda.

El crédito disponible para DeepSeek hace viable una primera etapa de experimentación con pocas sesiones y límites explícitos. La clave debe permanecer del lado servidor; el navegador nunca debe recibirla. Cada llamada debe asociarse a una sesión, guardar el modelo utilizado y respetar el presupuesto máximo. Antes de enviar datos de participantes, el servicio debe aplicar minimización y separar el texto necesario del identificador personal.

La primera integración no debe permitir que el modelo llame libremente a toda la API. Debe recibir un conjunto pequeño de funciones permitidas, por ejemplo `read_intake_summary`, `draft_followup` y `propose_match`, con validación del servidor y sin acceso genérico a SQL o a rutas administrativas.

## 8. Dos caminos viables

| Enfoque | Tradeoffs | Coste | Complejidad de configuración |
|---|---|---|---|
| **Módulo dentro de Flask + SQLite** | Se integra con autenticación, panel y modelos actuales; menor superficie operativa. Escala menos si luego se requieren colas, muchos agentes o ejecución continua. | Bajo al inicio; usa el saldo actual de DeepSeek por sesión y la infraestructura existente. | Media: nuevas tablas, endpoints, permisos, bitácora y UI de revisión. |
| **Servicio persistente con cola y panel de sesiones** | Separa los trabajos de IA, permite eventos, reintentos, varios agentes y ejecución en segundo plano. Añade despliegue, monitoreo y sincronización de estados. | Medio y recurrente: hosting más observabilidad más llamadas al modelo. | Alta: identidad entre servicios, cola, secretos, reintentos, webhooks y recuperación. |
| **Alternativa ligera: sesiones manuales de propuesta** | Un administrador copia un mandato y revisa la respuesta de DeepSeek dentro de una pantalla; no hay acciones automáticas ni cola. | Muy bajo; adecuado para aprender con casos reales. | Baja: un formulario, una llamada server-side y un registro básico. |

Para Maxocracia-Cero recomendaría comenzar con la alternativa ligera o con el módulo Flask, dependiendo de si se quiere aprender primero el comportamiento del agente o comenzar ya con auditoría estructurada. No recomendaría una plataforma persistente hasta tener un conjunto de sesiones revisadas, reglas de privacidad y una lista estable de herramientas permitidas.

## 9. Primer agente sugerido

El primer personaje podría ser **Custodio de Participación**. Su mandato sería leer resúmenes mínimos de nuevas entradas de la Red de Apoyo, identificar si falta información, proponer una categoría operativa y redactar un borrador de seguimiento. Podría expresarse con una voz propia, declarar desacuerdos y explicar sus criterios, pero no podría contactar a una persona, cambiar un estado final, emparejar definitivamente ofertas y necesidades ni revelar datos privados sin aprobación.

El segundo agente, cuando exista suficiente historial, podría ser **Disidente de Coherencia**: un agente cuyo mandato explícito sea buscar puntos ciegos, costos ocultos y contradicciones entre una propuesta y los axiomas. Su valor estaría precisamente en no coincidir automáticamente con el agente principal. La comunidad decidiría; los agentes ampliarían la deliberación.

## 10. Criterios de aceptación del prototipo

El prototipo estará listo para una primera cohorte cuando una persona administradora pueda crear una sesión con mandato, ver exactamente qué datos se entregan, recibir una respuesta con evidencia y grado de incertidumbre, aprobar o rechazar una propuesta, revertir una mutación permitida y exportar la bitácora sin consultar logs privados del servidor.

También debe ser posible revocar una sesión en cualquier momento, demostrar que una acción fuera del alcance fue rechazada por el servidor y distinguir una opinión del agente de un hecho del sistema. La autonomía se considera preservada cuando el agente puede expresarse y disentir; la seguridad se considera preservada cuando ningún estilo o autoridad retórica puede saltarse el contrato de permisos.

## 11. Preguntas para la siguiente sesión

La implementación futura solo necesita resolver tres decisiones de arquitectura: si la primera versión será manual o semi-automática, qué tres funciones de lectura/propuesta se habilitarán primero y qué personas o instancia comunitaria aprobarán las acciones P3. El proveedor del modelo puede mantenerse intercambiable; DeepSeek es una opción práctica para el piloto por el saldo disponible, pero el contrato de sesión no debe depender de una sola marca.

## Referencias internas

- `app/voting_oracle.py` — patrón existente de oráculo, firma de motor y fallback local.
- `app/guide_bp.py` — guía de confianza y candidatura donde el oráculo recomienda y la comunidad decide.
- `docs/architecture/atribuciones_sinteticas.md` — memoria pública de contribuciones sintéticas.
- `frontend/app/guia/page.tsx` — precedente de interacción con un oráculo desde el frontend.
- `app/auth.py` y `app/__init__.py` — autenticación e inicialización del backend.
