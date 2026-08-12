# SESIÓN NEXT — Handoff de la jornada (12-08-2026)

Documento de continuidad entre sesiones. Léelo al iniciar la próxima sesión
antes de tocar código. Mantenlo actualizado al cerrar cada jornada.

---

## 1. Prompt para Max (pegar en la próxima sesión)

> Continuamos la Maxocracia desde donde quedamos (ver `docs/SESION_NEXT_PROMPT.md`).
> Contexto: Fase 2 — Ola 4 "El Puente", versión 5.6+. El sistema de gobernanza comunitaria
> está completo (propuestas por categoría con quórum y consenso 75%, oráculo DeepSeek con
> fallback local, delegación de voto, parlamento de parámetros vinculante). El Puente de
> Coherencia (mapa teoría↔código) está en `docs/architecture/mapa_coherencia_ola4.md` y los
> requisitos en `docs/architecture/requisitos_fase2_ola4.md`.
> Patrón de trabajo: RLM navega + director verifica + teoría decide (guía en el repo
> local_models: `docs/GUIA_RLM_COLABORADOR.md`).
> Revisa los pendientes del §4 y elige el siguiente paso con criterio; commits regulares
> en español; respeta el principio "la teoría tiene prioridad".

## 2. Briefing para el agente (opencode / DeepSeek)

**Estado actual (12-08-2026, jornada mixta de dos sesiones):**

| Área | Estado |
|---|---|
| Puente de Coherencia M1-M4 (motor, teoría↔código, tests, frontend) | ✅ Completo |
| INV3 (VHV No Ocultable) implementado + 9 tests | ✅ |
| Renumeración T16/T17 completa (motor + Fase 2 app/frontend/docs) | ✅ (T9/T7 del libro intactos) |
| Capítulo 9.5 SDV-S en el libro + INV2-S formalizado en el spec | ✅ |
| Votación comunitaria (Cap 14): propuestas por categoría, quórum, consenso 75%, emergencia, T13 | ✅ |
| Oráculo de propuestas: DeepSeek principal + fallback local (hub Jan), firma `engine` | ✅ |
| Delegación de voto (democracia líquida prof. 1) | ✅ |
| Parlamento de parámetros vinculante (Cap 11, α β γ δ con restricciones axiomáticas) | ✅ (sesión paralela) |
| Atribuciones sintéticas + Mantenimiento Óptimo (Cap 17.4, ledger T13 en la plaza) | ✅ (sesión paralela) |
| Puente de Llegada: invitaciones firmadas, honeypot anti-bot, escalera N0→N1 | ✅ (sesión paralela) |
| Frontend: `/votaciones`, `/admin/settings` real, `/admin/subscriptions` real, SDV-S en contrato | ✅ |
| **RF-G5: superficies sin UI** — `/perfil` (Perfil Vital) con saldo Maxo + ledger T13 + transferencia, protección (nivel/caps/declaración), reputación, recursos comunitarios e intercambios | ✅ (ago 2026) |
| **M4 fase 2 / RF-B4**: "Contrato Ético" en el Muro de `/matching` → `POST /contracts/from-need` | ✅ (ago 2026) |
| Suite de tests | **652/652** (motor + app + votación + parlamento + arrivals + ledger + maxo ledger, verificado 12-08-2026) |

**Decisiones canónicas a respetar:**
- **La teoría (libro) tiene prioridad**: T0-T15 son canónicos; T16=Minimizar Daño, T17=Reciprocidad
  Justa (renumerados desde "T7"/"T9" de ingeniería). No reintroducir T9=Reciprocidad.
- El validador conceptual (`scripts/validador_conceptual.py` + su test) exige coherencia axiomática
  en TODO el repo — correrlo tras cambios que mencionen axiomas.
- `app/voting_oracle.py` **no carga .env al importar** (contamina tests; run.py ya lo hace).
- Tests: escribir archivos SIEMPRE con `encoding="utf-8"`; NUNCA reescribir archivos con
  Get-Content/Set-Content de PowerShell (corrompe UTF-8 — lección aprendida en esta jornada).
- Oráculos: fallback local `LOCAL_ORACLE_BASE_URL=http://localhost:1337/v1`.

## 3. Cómo verificar al arrancar

```powershell
# Backend (cwd = raíz del repo)
.venv\Scripts\python.exe -m pytest tests/test_voting.py tests/test_maxocontracts/test_parliament.py -q
.venv\Scripts\python.exe -m pytest tests/test_validador_conceptual.py -q   # coherencia axiomática

# Frontend (cwd = frontend/)
npx tsc --noEmit
```

## 4. Pendientes priorizados

1. **Cohorte Cero real**: ejecutar 50+ contratos (20 aseo, 15 préstamo, 15 comida) — TODO.md
2. **RF-G4**: CRUD admin completo (interchange/followup/vhvproduct) o migrar `/admin/participants`
3. **RF-I8 resto**: votación ponderada por TVI (fase futura, Cap 14)
4. **SDV-S editorial**: integración cruzada en Caps. 10/11/13/14 del libro
5. **Mantener** `mapa_coherencia_ola4.md`, `requisitos_fase2_ola4.md` y este handoff al día

**Cerrado en esta jornada (12-08-2026, sesión continua):**
- **RF-G5** (Perfil Vital): `frontend/app/perfil/page.tsx` + `GET /maxo/{id}/ledger` (T13) + 4 tests.
- **M4 fase 2 / RF-B4**: botón "Contrato Ético" en el Muro de `/matching` → `POST /contracts/from-need`
  (borrador DRAFT, invitación inline si participante sin vincular, violaciones AVA en tarjeta).
- **Limpieza**: eliminado `app/resources.py` (duplicado huérfano; solo se registra `resources_bp`).
- **Informe Reino Sintético**: `docs/architecture/informe_reino_sintetico_2026-08-12.md` (libro completo
  307 KB vía RLM, verificado con grep) + atribuciones en `atribuciones_sinteticas.md`.
- **Arnés RLM** (repo local_models): parseo del formato nativo OpenAI de `tool_calls` + tokens amplios
  (root 6000, sub 3000) + `--root-max-tokens` en el colaborador — commits `c744047`, `357c796`.
- **Hallazgo pendiente de seguridad**: reputation/resources/interchanges sin `@token_required`.

## 5. Historia reciente (git log, maxocracia)

```
0aebedd feat(arrivals): Puente de Llegada - invitacion firmada, honeypot anti-bot, escalera N0-N1
cc676d4 feat(voting): parlamento de parametros (Cap 11) - propuestas vinculantes criticas
0b5c8ac feat(oracle): gratitud aterrizada - atribuciones sinteticas y Mantenimiento Optimo (Cap 17.4)
46fe993 feat(voting): delegacion de voto (democracia liquida) + INV2-S formalizado + M4 corregido
0832fb6 feat(voting-oracle): DeepSeek principal + fallback local, firma T13 del motor
342fa0c feat(frontend): /votaciones - gobernanza comunitaria (demo Gemini portado)
c59f608 feat(voting): votacion comunitaria (Cap 14) - categorias, quorum, consenso 75%
```

---
**Mantenido por**: Max + DeepSeek (opencode) · **Próxima actualización**: al cierre de la siguiente sesión
