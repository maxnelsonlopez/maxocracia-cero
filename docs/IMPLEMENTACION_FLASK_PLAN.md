# Plan de implementación (Flask + SQLite)

Este documento mapea las prioridades del proyecto a endpoints Flask, contratos de datos, pruebas y pasos de despliegue para la implementación local-first con SQLite.

## Objetivo

Proveer una API local, segura y testeable que soporte las operaciones núcleo de Maxocracia: intercambios, contabilidad Maxo (ledger), recursos y reputación. Mantener cero dependencias externas salvo Flask y herramientas de desarrollo.

## Resumen de prioridades (corto)

1. Endpoints core: `/interchanges`, `/maxo`, `/resources`, `/reputation`, `/users`.
2. Credito Maxo automático: reglas básicas implementadas en `app/maxo.py`.
3. Tests: pytest unit/integration por endpoint y flujo principal.
4. Auth: registrar/ingresar con contraseñas hasheadas; proteger endpoints críticos con JWT.
5. CI: GitHub Actions que corre los tests.

## Contratos (ejemplos)

- POST /interchanges

  - Input JSON: { interchange_id, giver_id, receiver_id, uth_hours, impact_resolution_score, description }
  - Output: { message, credit }

- GET /interchanges

  - Output: [ { interchange row } ]

- GET /maxo/{user_id}

  - Output: { user_id, balance }

- POST /maxo/transfer
  - Input: { from_user_id, to_user_id, amount, reason }
  - Output: { success }

## Esquema de base de datos (notas)

- Usar `app/schema.sql` como base.
- Agregar tabla `jwt_tokens` si se decide guardar revocaciones.

## Testing

- Tests unitarios para `app/maxo.py` (credit_user, get_balance).
- Integration tests para `/interchanges` que validan inserción y ledger.
- Tests para errores: usuario inexistente, cantidades negativas, payload inválido.

## Rollout y pasos para desarrollo

1. Mantener `comun.db` en `.gitignore`.
2. Crear rama feature/core-api e iterar con commits pequeños.
3. Usar `requirements-dev.txt` para herramientas de test.
4. Hacer PR y dejar CI correr; arreglar fallos que aparezcan.

## Tareas siguientes (mínimas viables)

- Implementar endpoints `/maxo/balance` y `/maxo/transfer` (esqueleto + tests).
- Sustituir semillas con contraseñas hasheadas.
- Añadir protección JWT y middleware de autorización.

---

Document generated and maintained by the development workflow on 2025-10-19.
