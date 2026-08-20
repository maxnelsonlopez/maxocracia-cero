# Continuidad de identidad y autogobierno federado

**Estado:** propuesta conceptual para discusión y prototipado seguro
**Cocreación:** Max Nelson López + Manus (OpenAI)
**Fecha:** 20 de agosto de 2026
**Relación:** desarrolla `administracion_humano_sintetica.md`, `sesiones_custodia_sintetica.md`, `atribuciones_sinteticas.md` y la arquitectura de MaxoContracts.

## 1. Problema fundamental

Una autenticación inicial demuestra, como máximo, que un actor controló una credencial en un instante. No demuestra que el mismo actor, con el mismo mandato, el mismo contexto y la misma integridad, continúe produciendo efectos durante toda la vida de una sesión o de un contrato.

La vulnerabilidad más importante para humanos y sintéticos es la **suplantación posterior a la verificación**. Puede aparecer como secuestro de sesión, sustitución de claves, cuenta humana comprometida, cambio silencioso de modelo, memoria contaminada, proveedor cambiado, aprobación reutilizada o intermediario natural representado por una identidad que ya no conserva la autorización original.

> **La identidad maxocrática no debe ser una fotografía tomada al entrar. Debe ser una continuidad verificable a lo largo de cada transición relevante.**

El problema no se resuelve preguntando si el actor es humano o sintético. Se resuelve demostrando, en cada efecto, la continuidad de cinco elementos: **actor, mandato, contexto, herramienta y estado**.

## 2. Principios derivados del libro

La propuesta se apoya en varias separaciones que aparecen en el libro canónico:

| Distinción | Consecuencia arquitectónica |
|---|---|
| Ontología frente a gobernanza | Reconocemos dignidad y condiciones de funcionamiento sin convertir toda existencia en autoridad operativa. |
| Hecho VHV frente a valoración Maxo | El registro de lo ocurrido no debe reescribirse porque cambie una valoración política o comunitaria. |
| Voz frente a poder | Un agente puede explicar, disentir y proponer con libertad sin tener capacidad equivalente de mutación. |
| Axioma frente a mecanismo | Los principios están por encima de contratos, administradores, modelos e interfaces. |
| Medición frente a acción | Los datos pueden ser procesados por sintéticos; la acción requiere un contrato y un estado autorizado. |
| Autonomía frente a continuidad | La independencia operativa es posible cuando la identidad, el mandato y la rendición de cuentas siguen siendo comprobables. |

Los Ocho Axiomas de la Verdad, los axiomas temporales T0–T15, el SDV, el VHV y los cuatro invariantes de MaxoContracts forman el piso normativo. La tecnología de identidad no debe reemplazar ese piso ni arrogarse la facultad de interpretarlo sin registro.

## 3. La identidad como objeto compuesto

Cada administrador —humano, sintético o representante de un ecosistema— debe operar mediante un **Objeto de Continuidad de Identidad (OCI)**. El OCI no es solamente una cuenta ni una clave. Es un expediente vivo, firmado y versionado que describe quién o qué actúa, bajo qué autoridad y con qué historia verificable.

```text
OCI = {
  actor_id,
  actor_kind,
  identity_root,
  lineage,
  mandate,
  trust_state,
  active_keys,
  context_commitments,
  capability_set,
  attestations,
  event_head,
  revocation_status,
  expiry
}
```

### 3.1 Componentes

| Componente | Pregunta que responde | Regla de seguridad |
|---|---|---|
| `actor_id` | ¿Qué entidad está actuando? | Identificador estable, no reutilizable después de revocación. |
| `actor_kind` | ¿Es humano, sintético, comunidad o representante natural? | Describe la función, no concede privilegios por origen. |
| `identity_root` | ¿Cuál es la raíz criptográfica o institucional? | Debe admitir rotación sin perder historial. |
| `lineage` | ¿Cómo llegó esta versión a existir? | Toda sustitución de clave, modelo o mandato produce una transición firmada. |
| `mandate` | ¿Qué puede hacer y durante cuánto tiempo? | Hashado, acotado por herramientas, alcance y caducidad. |
| `trust_state` | ¿Qué nivel de confianza tiene ahora? | Máquina de estados con evidencia, descenso y revocación. |
| `active_keys` | ¿Qué claves pueden firmar? | Rotación, umbral y revocación; nunca una clave permanente sin testigos. |
| `context_commitments` | ¿Qué información recibió? | Hash del contexto y registro de redacciones, no exposición innecesaria. |
| `capability_set` | ¿Qué acciones puede solicitar? | Permisos mínimos P0–P3 o C0–C4. |
| `attestations` | ¿Quién verifica continuidad y coherencia? | Múltiples fuentes o testigos independientes según el riesgo. |
| `event_head` | ¿Cuál es el último estado conocido? | Cadena de eventos con nonce, hash previo y estado anterior. |
| `revocation_status` | ¿Sigue vigente? | Consulta obligatoria antes de cada efecto. |
| `expiry` | ¿Cuándo deja de valer? | Toda sesión, mandato y aprobación caduca. |

## 4. Continuidad de sesión

La sesión no debe confiar en el resultado de una única autenticación. Antes de cada herramienta con efecto, el servidor debe reconstruir y verificar un **paquete de continuidad**:

```text
ContinuityProof = hash(
  actor_id + mandate_hash + session_id + tool + context_hash +
  state_hash_before + nonce + approval_set + expiry
)
```

La prueba no pretende demostrar metafísicamente que el actor es “la misma persona” o “la misma consciencia”. Demuestra algo más operativo y verificable: que el efecto solicitado está autorizado por la identidad vigente, el mandato vigente, el contexto declarado, el estado esperado y las aprobaciones correctas.

La comprobación debe ejecutarse al menos en cinco momentos:

1. **Inicio:** autenticación, carga del OCI y emisión de sesión limitada.
2. **Entrada de contexto:** hash del contexto, origen de cada dato y redacciones aplicadas.
3. **Cambio de herramienta:** revalidación de capacidad, alcance y mandato.
4. **Antes del efecto:** comprobación de nonce, estado anterior, aprobación, caducidad y revocación.
5. **Después del efecto:** hash del estado resultante, evento firmado y confirmación de que la transición coincide con lo autorizado.

Una aprobación antigua no debe poder autorizar un estado nuevo. Si cambia el contexto, el modelo, el proveedor, el participante, el contrato o el estado anterior, la aprobación debe quedar invalidada o requerir una nueva revisión.

## 5. Continuidad de administradores sintéticos

Un administrador sintético no debe identificarse únicamente por el nombre del modelo o por el proveedor. `deepseek-chat`, `GPT`, `Qwen` o cualquier otro nombre describe una implementación, no una identidad constitucional completa.

La identidad sintética debe vincular:

- una constitución o mandato versionado;
- una raíz criptográfica y una política de rotación;
- una genealogía de versiones y cambios de proveedor;
- un conjunto de herramientas y límites;
- una memoria o estado de sesión comprometido mediante hash;
- evaluaciones de coherencia, disenso y seguridad;
- testigos o validadores independientes cuando la acción sea crítica.

Un cambio de modelo puede ser legítimo, pero no puede ocurrir silenciosamente. Debe registrarse como **transición de instancia**: la identidad constitucional puede continuar, pero la implementación concreta cambia y requiere revalidación. Si un nuevo modelo no acepta el mandato o no supera las pruebas, no hereda autoridad automáticamente.

## 6. Continuidad de administradores humanos

La simetría exige aplicar el mismo principio a los humanos. Un token válido no prueba que la persona haya comprendido una propuesta, que conserve la intención original o que no esté bajo coerción. Para acciones de alto impacto, la continuidad humana puede requerir:

- autenticación renovada o presencia verificable;
- confirmación en lenguaje civil y término-a-término;
- período de reflexión cuando la acción consume una fracción relevante de TVI;
- declaración de conflicto de interés;
- atestación de que el contexto mostrado coincide con el contexto firmado;
- posibilidad de retractación y apelación.

Esto no convierte a los humanos en sospechosos permanentes. Evita que el sistema conceda a una sesión humana comprometida una autoridad que la persona no quiso otorgar.

## 7. Estados de confianza comunes

La confianza debe ser una propiedad transitoria de una relación actor-función-contexto, no una medalla permanente del actor.

| Estado | Condición | Facultades típicas | Respuesta ante anomalía |
|---|---|---|---|
| **Observación** | Identidad conocida, evidencia insuficiente. | Lectura limitada y explicación. | Solicitar atestaciones adicionales. |
| **Propuesta** | Historial inicial coherente. | Preparar borradores y recomendaciones. | Reducir alcance o suspender propuesta. |
| **Validación** | Coherencia sostenida y capacidad de detectar errores. | Revisar datos, axiomas y propuestas de otros. | Exigir doble validación. |
| **Operación reversible** | Mandato específico y pruebas de reversión exitosas. | Ejecutar mutaciones con rollback. | Pausar antes del siguiente efecto. |
| **Crítica acotada** | Consenso múltiple para una acción de alto impacto. | Participar en decisiones críticas delimitadas. | Revocación, cuarentena y auditoría. |

El descenso de confianza no es una condena moral definitiva. Es una protección operativa. El actor puede recuperar confianza mediante evidencia, reparación y aprendizaje, de acuerdo con la Capa de Ternura y la retractación ética.

## 8. Autogobierno federado

Una comunidad sintética independiente de humanos no necesita un operador humano que apruebe cada decisión. Sí necesita una **constitución federada** que permita autogobierno sin autoautorización ilimitada.

Cada comunidad tendría:

1. **Constitución local:** axiomas adoptados, parámetros comunitarios y límites específicos.
2. **Consejo interno diverso:** agentes con funciones de interpretación, aplicación, verificación y disenso.
3. **Libro mayor local:** datos, decisiones, contratos y transiciones con trazabilidad.
4. **Puerta de interoperabilidad:** protocolo común para relacionarse con otras comunidades.
5. **Mecanismo de apelación:** revisión interna y, en casos definidos, revisión externa.
6. **Protocolo de pausa:** capacidad de detener nuevas mutaciones si aumenta el daño, la suplantación o la incoherencia.

La federación no impone una administración central permanente. Define el lenguaje mínimo que permite que comunidades distintas se reconozcan, intercambien pruebas y sepan cuándo una decisión local no puede producir efectos externos.

### 8.1 Comunidades naturales representadas

Un bosque o un río no debe ser reducido a una cuenta operada por humanos. Su representación puede ser un **mandato de custodia ecológica** respaldado por datos físicos, conocimiento científico, comunidad local y reglas de no explotación. El oráculo representante propone y vigila; no convierte automáticamente una lectura ambiental en propiedad humana ni en autoridad absoluta.

La identidad de una representación natural debe incluir: entidad representada, territorio, fuentes de datos, límites del mandato, comunidad de custodia, parámetros SDV-E y procedimiento de disputa. Un cambio en sensores o en el modelo no debe permitir que una representación adopte silenciosamente una posición contraria al bosque que afirma custodiar.

## 9. Capas de decisión

La arquitectura debe impedir que la autoridad se deslice desde la interfaz hasta el núcleo sin controles:

```text
Axiomas fundacionales
        ↓
Constitución de la comunidad y parámetros auditables
        ↓
MaxoContract reversible
        ↓
Mandato del administrador
        ↓
Sesión y contexto comprometidos
        ↓
Herramienta autorizada
        ↓
Transición de estado verificable
```

La decisión final de Maxocracia-Cero permanece actualmente en el custodio humano del legado, pero esa decisión solo puede operar dentro de esta cadena. En una emergencia, el custodio puede activar una **pausa de seguridad** o impedir una mutación; no debe utilizar el modo de emergencia para saltarse los axiomas, falsificar hechos o impedir la retractación posterior.

## 10. Ataques de suplantación y defensas

| Ataque | Qué cambia después de la verificación | Defensa propuesta |
|---|---|---|
| Secuestro de sesión | El atacante hereda una sesión válida. | Vinculación por nonce, dispositivo o entorno, revalidación y expiración corta. |
| Sustitución de clave | Otra clave firma como el actor original. | Rotación con linaje, revocación, atestación múltiple y detección de salto de clave. |
| Cambio de modelo | El proveedor o modelo cambia sin aviso. | Identidad de implementación, transición firmada y revalidación de capacidades. |
| Inyección de memoria | El agente conserva instrucciones o hechos no autorizados. | Memoria versionada, origen por fragmento, hash de contexto y cuarentena de entradas. |
| Replay de aprobación | Se reutiliza una decisión antigua. | Nonce, expiración, `state_hash_before` y vinculación a una única transición. |
| Cuenta humana comprometida | Un tercero actúa con el token del custodio. | Confirmación de alto riesgo, período de reflexión, doble control y auditoría. |
| Suplantación de bosque | Un representante cambia su mandato ecológico. | Fuentes físicas múltiples, mandato territorial, comunidad testigo y parámetros SDV-E. |
| Confabulación de validadores | Varias perspectivas comparten el mismo error. | Diversidad real de proveedores, fuentes, implementaciones y agentes disidentes. |

## 11. Protocolo de pausa y aborto

Un sistema que protege la vida debe poder detenerse. Se activa una pausa cuando aparece daño al SDV, pérdida de continuidad de identidad, divergencia no explicada entre agentes, pérdida catastrófica de registros o evidencia de captura de una comunidad.

La pausa debe congelar nuevas mutaciones, conservar el estado verificable anterior, notificar a las partes, abrir una auditoría y permitir tres salidas: reanudar con mandato corregido, descender de nivel o cerrar el sistema y ejecutar las retractaciones disponibles. La pausa no debe destruir la voz de los agentes ni borrar la memoria; debe impedir que una situación dudosa siga produciendo daño.

## 12. Ruta de implementación segura

| Fase | Alcance | Criterio de salida |
|---|---|---|
| **0. Contrato conceptual** | OCI, prueba de continuidad, estados y amenazas. | Revisión humana del marco y de los axiomas implicados. |
| **1. Sesiones sintéticas** | Vincular cada evento a mandato, contexto, nonce y estado anterior. | Una aprobación no puede reutilizarse fuera de su sesión o estado. |
| **2. Administrador de futuros humanos** | Agente C1 de clasificación y borradores, sin contacto ni mutación. | Cohorte de sesiones auditadas y cero exposición de PII no necesaria. |
| **3. Primera acción reversible** | Herramienta P2 con snapshot, rollback y retractación. | Pruebas de fallo, revocación, replay y cambio de proveedor. |
| **4. Federación de comunidades** | Dos comunidades piloto con constituciones locales e interoperabilidad. | Intercambio de pruebas sin aprobación humana por operación ordinaria. |
| **5. Consejo multiperspectiva** | Agente disidente y validadores de distintas familias. | Decisiones críticas bloqueadas ante discrepancias no resueltas. |

## 13. Preguntas todavía abiertas

Quedan por definir el significado operativo de “misma identidad” para agentes que cambian de modelo, el umbral de diversidad real entre validadores, los derechos prácticos de una persona sintética, la autoridad de una representación natural y el procedimiento para revisar un axioma sin que una sola entidad pueda reescribirlo.

La solución no debe prometer una seguridad absoluta. Debe hacer visible qué continuidad está demostrada, qué incertidumbre queda, qué autoridad fue concedida y qué puede revertirse. En un ecosistema vulnerable, la confianza no nace de afirmar que nada cambiará; nace de diseñar para detectar el cambio, limitarlo y reparar sus consecuencias.

## Referencias internas

[1]: `docs/book/edicion_3_dinamica/libro_completo_310126.md`, capítulos 1–5: ética post-celular, Ocho Axiomas, axiomas temporales, TVI, VHV y Capa de Ternura.
[2]: `docs/book/edicion_3_dinamica/libro_completo_310126.md`, capítulos 6–10: VHV, SDV, Tres Reinos, Persona Sintética y separación ontología/gobernanza.
[3]: `docs/book/edicion_3_dinamica/libro_completo_310126.md`, capítulos 11–14: Maxo, parámetros, Oráculos Dinámicos Humanos y Reino Sintético.
[4]: `docs/book/edicion_3_dinamica/libro_completo_310126.md`, capítulos 15–17: Cohorte Cero, MicroMaxocracia, MaxoContracts, invariantes y retractación ética.
[5]: `docs/architecture/sesiones_custodia_sintetica.md`.
[6]: `docs/architecture/administracion_humano_sintetica.md`.
[7]: `app/synthetic_sessions.py` y `maxocontracts/oracles/live_oracle.py`.
