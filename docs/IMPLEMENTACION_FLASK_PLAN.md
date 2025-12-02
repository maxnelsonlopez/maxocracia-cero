# Plan de implementación (Flask + SQLite)

Este documento mapea las prioridades del proyecto a endpoints Flask, contratos de datos, pruebas y pasos de despliegue para la implementación local-first con SQLite.

**Estado actual:** Diciembre 2025 - MVP funcional completado y auditado.

## Objetivo

Proveer una API local, segura y testeable que soporte las operaciones núcleo de Maxocracia: intercambios, contabilidad Maxo (ledger), recursos y reputación. Mantener cero dependencias externas salvo Flask y herramientas de desarrollo.

## Estado de implementación

### ✅ Completado

1. **Endpoints core**: `/interchanges`, `/maxo`, `/resources`, `/reputation`, `/users` - Implementados y funcionando.
2. **Crédito Maxo automático**: Reglas básicas implementadas en `app/maxo.py`.
3. **Tests**: 45 pruebas unitarias e integración pasando exitosamente.
4. **Auth**: Sistema JWT completo con refresh tokens, rotación automática y revocación.
5. **CI/CD**: GitHub Actions configurado con tests, linting y documentación.
6. **Seguridad**: Rate limiting, validación de contraseñas, headers de seguridad.
7. **Calidad de código**: Configuración de linters (black, flake8, isort, mypy).

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

1. ✅ Mantener `comun.db` en `.gitignore`.
2. ✅ Crear rama feature/core-api e iterar con commits pequeños.
3. ✅ Usar `requirements-dev.txt` para herramientas de test.
4. ✅ Hacer PR y dejar CI correr; arreglar fallos que aparezcan.

## Próximos pasos (Post-MVP)

### Mejoras de corto plazo
- [ ] Añadir paginación a endpoints que retornan listas (`/interchanges`, `/resources`).
- [ ] Implementar búsqueda y filtrado avanzado en recursos.
- [ ] Añadir endpoints de estadísticas agregadas (`/stats/community`).
- [ ] Mejorar documentación de API con ejemplos de uso.

### Mejoras de mediano plazo
- [ ] Migrar a PostgreSQL para producción.
- [ ] Implementar sistema de notificaciones.
- [ ] Añadir soporte para imágenes en recursos.
- [ ] Dashboard web básico para visualización de datos.

### Consideraciones para escalabilidad
- [ ] Evaluar migración a arquitectura de microservicios (ver `docs/diseno-tecnico-comun-go.md`).
- [ ] Implementar caché con Redis.
- [ ] Añadir sistema de colas para procesamiento asíncrono.

---

**Última actualización:** Diciembre 2025  
**Mantenido por:** Equipo de desarrollo Maxocracia
