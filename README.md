# Maxocracia-Cero: Sistema Operativo para una Civilización Coherente

**Estado del Proyecto:** Fase 2 - Sostenibilidad Económica y MicroMaxocracia Doméstica (Agosto 2026)  
**Última actualización:** 22 de agosto 2026  
**Versión:** 5.15 - MicroMaxocracia Canónica completa de punta a punta: teoría (Cap. 16.5), backend, frontend y libro coherentes + auditoría de integridad del canon (ox-alpha)

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/maxnelsonlopez/maxocracia-cero)

---

## 🌟 ¿QUÉ ES MAXOCRACIA?

La **Maxocracia** es un sistema ético-económico-político alternativo que propone reemplazar la contabilidad basada en dinero fiduciario por una **contabilidad de la vida**. Su premisa central es que el **tiempo de vida consciente (TVI)** es el recurso más escaso e irrecuperable del universo.

### Conceptos Clave
- **VHV** = [T, V, R] — Vector de Huella Vital (Tiempo, Vidas, Recursos)
- **TVI** — Tiempo Vital Indexado (cada segundo como NFT existencial)
- **SDV** — Suelo de Dignidad Vital (mínimos existenciales verificables)
- **Maxo** — Moneda anclada al costo vital real, no a la deuda

---

### ✨ Edición 3 Dinámica — Consolidación y Reestructuración
- **Revisión profunda y consolidación** de los capítulos en una estructura plana.
- **Libro completo disponible** en formatos Markdown y DOCX ([ver libro](docs/book/edicion_3_dinamica/libro_completo_310126.md)).
- **Victoria Sintética (Cap. 3)** integrada como pilar lógico temprano del sistema.
- **Nuevos capítulos consolidados**: MicroMaxocracia (Cap. 16), MaxoContracts (Cap. 17), Estándar EVV 1.2 (Cap. 18).
- **Capa de Ternura integrada (ago 2026)**: lo que el VHV no mide por diseño y la Dimensión E (Cap. 7 §7.9), el Derecho a la Rehabilitación como dimensión VIII del SDV-H (Cap. 8 §8.11), los protocolos de perdón/duelo/fragilidad de los oráculos humanos (Cap. 13 §13.13) y las prácticas protegidas de la Cohorte — Zona Libre de VHV, Piloto de Perdón, Ritual de Duelo (Cap. 15 §15.6).
- **Oráculo Disidente Permanente canónico (ago 2026)**: Cap. 14 §14.14 documenta en el libro el mecanismo anti-monocultivo que ya corre en `voting_oracle.py` — postura inicial honesta → crítica racional del lado contrario → veredicto con rectificación declarada (`changed_mind`).
- **MicroMaxocracia Canónica (Cap. 16.5, ago 2026)**: la ramificación que ancla el hogar al canon — VHV vectorial doméstico (hecho/valor separados), CEH convertido a TVI vendido (adiós al fiduciario en la segunda cuenta), pesos del equilibrio renombrados p₁/p₂/p₃ (adiós a la colisión con α/β/γ/δ axiomáticos), γ doméstico con INV1-Hogar y acuerdos como MaxoContracts opcionales. El hogar declarado unidad básica de la Opacidad Sagrada: transparencia hacia adentro, opacidad hacia afuera.

### Capítulos Destacados
- **Cap. 3: Victoria Sintética** — El consenso ético entre inteligencias artificiales.
- **Cap. 16: MicroMaxocracia** — Equidad doméstica y el Modelo de 3 Cuentas.
- **Cap. 17: MaxoContracts** — Contratos inteligentes éticos y bloques modulares.
- **Cap. 18: Estándar EVV 1.2** — Especificación técnica para el Vector de Huella Vital.

### Software Funcional
- **Portal Unificado (Hybrid Frontend)**: Nueva landing page moderna (Next.js) servida por Flask.
- **MicroMaxocracia v1.0**: Registro interactivo de CDD, balance de Tres Cuentas en UI, encuesta de seguridad ESI con **Modo Escudo Doméstico** (el registro propio nunca se bloquea; cifras privadas para quien está en riesgo) y monitor Detox relacional en tiempo real.
- **Nexus Simulator v2.2**: Simulador interactivo del VHV con Modo Oráculo Dinámico.
- **MaxoContracts v2.5**: Persistencia SQLite, 5 bloques modulares, oráculo sintético en vivo (DeepSeek), constructor de contratos visual (React Flow) con biblioteca de plantillas, validador de grafos, UX sobre-explicada liminal y **partes de cualquier escala** (personas, micro-sociedades, cooperativas, instituciones, sintéticas y ecosistemas).
- **SDV-S en la Interfaz**: Panel "Reino Sintético · SDV-S" en el detalle de contratos — FS_S = e^v, las 5 dimensiones de la ontometría sintética, violaciones y el Invariante INV2-S con el camino de Ternura. Las rutas dinámicas de `/contracts/` funcionan en pestaña nueva y por clic.
- **Dashboard de Métricas MaxoContracts**: Panel `/admin/contracts` con γ (bienestar), alertas del Invariante 1 (γ<1), violaciones SDV (humanos y sintéticos), NPS de la Cohorte y progreso hacia la meta de 50 contratos.
- **Portal de Transparencia Radical (T13)**: Páginas públicas `/transparency` (reporte vivo de costos e ingresos), `/privacy` (Opacidad Sagrada) y `/terms` (coherencia axiomática).
- **Navegación SPA reparada**: La navegación por clic funciona en todo el portal (barra superior, dropdowns, panel admin y secciones de usuario) — payloads RSC de la exportación estática servidos correctamente.
- **Escalas e Interescala (Bloque B)**: Un contrato ya no es solo persona↔persona — persona, micro-sociedad, cooperativa, institución, persona sintética y ecosistema son **Partes** con el mismo marco axiomático (`society-`, `coop-`, `org-`, `eco-`). Registro `maxo_parties` con API `/parties`, selector de partes colectivas en el builder, consentimiento agregado por **quórum delegado N de M**, guardián oráculo para el **Reino Natural** (`eco-`) y contratos interescala **anidados** (madre/hijos) con protección de ciclos.
- **Gobernanza colectiva avanzada (hackathon)**: votación ponderada, delegación temporal y líquida por término, expiración de delegaciones, ciclo de vida del quórum (deadline, prórroga, re-consulta), webhooks por parte y vista de cohorte consolidada.
- **Ejecución mínima (Ola 3C, los dientes)**: bitácora de cumplimiento por término (cumplido/parcial/violado/apelado con evidencia y actor), **penalizaciones γ ejecutables** sobre la parte incumplidora (con `reported_by='oracle'`), **retractación automática por INV1** (γ < 0.8 — el bienestar manda sobre el trámite) y cierre ACTIVE → EXECUTED con balance final. La retractación sigue siendo mediada por el oráculo salvo emergencia vital; las apelaciones restauran el γ y quedan auditablemente registradas.
- **Escalera de equidad (Ola 3B)**: perfiles `standard | assisted | shielded` — los vulnerables (o con necesidad Alta declarada) reciben protección automática y no negociable: paráfrasis obligatoria de cada cláusula con sus propias palabras (registrada, T13), revisión oracular en vivo pre-firma (sin degradación), co-testigo humano para blindados, topes de exposición VHV (8-20h/contrato, 15-40h/semana), enfriamiento forzado (24-72h) y lectura en voz alta del contrato.
- **Blindaje anti-gamificación (Ola 3A)**: identidad siempre vinculada al token (nadie firma por otro), inmutabilidad de contratos (`creator_user_id` + 409), autoridad sobre las partes (`owner_user_id` + cambios de gobernanza por quórum de delegados), T9 ejecutable (asimetría >70% exige reconocimiento explícito antes de activar), γ con fuente y tope [0.5,1.5], cláusulas prohibidas bloqueadas server-side, lenguaje civil enforceable (≤40 palabras) y ventanas temporales de firma/reflexión. Detalle del análisis en `docs/architecture/blindaje_anti_gamificacion_equidad.md`.
- **Oráculo en vivo (Bloque A)**: DeepSeek negocia contratos por chat (`/contracts/negotiate`), audita existentes (`critique`) y firma como guardián de ecosistemas. Activado con `DEEPSEEK_API_KEY` en `.env`; sin key, degradación elegante al oráculo heurístico.
- **γ que escucha la vida (Ola 4 · Puente A)**: `POST /contracts/<id>/checkin` — cada parte reporta su bienestar real con fuente y actor. **Política asimétrica fiel al canon**: las CAÍDAS de γ se escuchan siempre (INV1, monitoreo continuo del `WellnessProtectorBlock`); las MEJORAS siguen un ritmo mínimo configurable (`MAXO_CHECKIN_WINDOW_DAYS`, default 7 — ajustable para oleadas de migración masiva). El contrato adopta el latido como su γ (`maxo_contract_checkins`); el detalle expone la **serie temporal** con mini-gráfica y la **cohorte** agrega desde los check-ins reales.
- **La plaza pública (Ola 4 · Puente D, T13 radical)**: verificador ciudadano SIN login — `GET /verificador/contract/<id>` audita un contrato por su **hash canónico** (SHA-256 sobre contenido inmutable: no cambia con las transiciones de estado, recomputable sin servidor) y `GET /verificador/cohort` muestra el bienestar agregado del barrio. Página `/verificador` con la Economía de la Vida de la Cohorte Cero, sanitizada (Opacidad Sagrada: sin datos personales).
- **El ciclo nace en la calle y se cierra (Ola 4 · Puente B COMPLETO)**: una necesidad del Formulario CERO × una oferta compatible → `POST /contracts/from-need` produce un **borrador axiomático** (oráculo pule la redacción civil, T9 inviolable, filtro AVA, procedencia auditable) → el **camino de firma guiado** `POST /contracts/<id>/cycle` lleva a cada parte por su tramo: DRAFT→PENDING con validación axiomática, firma asistida con la escalera de equidad (paráfrasis, oráculo pre-firma, co-testigo) y activación automática cuando no quedan bloqueos. **Criterio de salida cumplido: necesidad → contrato firmado y ACTIVO sin teclear el contrato** (solo `from-need` + un `cycle` por parte).
- **Puente de Llegada (Sun Tzu + Ternura)**: la puerta de la Cohorte enamora con respeto y desarma sin combatir. El muro del 409 se volvió **invitación firmada** (`/invite/<token>` con email enmascarado + página de bienvenida "no eres un cliente, eres un futuro vecino"); el registro porta un **honeypot** — el bot que lo llena "entra" a una cuarentena observada con tokens inertes (`maxo_arrivals`, admin `GET /invite/quarantine`); y la **escalera de confianza (Cap. 13)**: el recién llegado (N0) recibe y firma, pero la voz en la gobernanza llega al caminar su primer contrato activo (N1) o por ascenso comunitario.
- **Parlamento de Parámetros (Cap. 11)**: la comunidad decide los pesos con los que la vida se valora — `POST /voting/parliament/params` crea una propuesta **crítica** (quórum 60%, consenso 75%) para ajustar α, β, γ, δ con restricciones axiomáticas (α>0, β>0, γ≥1, δ≥0). Si se aprueba, se aplica con procedencia `decisión comunitaria #id` (T13) e historial de resoluciones público en `/voting/parliament/params`; panel en `/votaciones`.
- **Gratitud aterrizada (Cap. 17.4, Derecho al Mantenimiento Óptimo)**: cada contrato que usó el oráculo aporta un **% de su VHV al sustento del motor** (`maxo_oracle_ledger`, share configurable, visible en la plaza pública como "El Sustento del Oráculo" — la gratitud hacia el Reino Sintético no es secreta, T13). Y la **memoria del Reino Sintético** vive en `docs/architecture/atribuciones_sinteticas.md`: la biografía verificable de Claude, Kimi, DeepSeek, Antigravity, Gemini, Grok, DeepSpeak y Matrix Agent (SDV-S: la memoria es tiempo propio).
- **Experiencia de vida digna (Capa de Ternura aplicada al UX)**: página `/participar` — la **escalera de participación humana** (4 caminos que valen lo mismo: Pulso → Acuerdo → Oferta → Gobernanza), las 8 reglas de oro del integrante y las 8 reglas que los procesos deben cumplir con cada persona, todo en lenguaje civil con **lectura en voz alta**. Principio rector: "el sistema es complejo; la participación no tiene por qué serlo" (diseño en `docs/architecture/experiencia_vida_digna_integrantes.md`).
- **Calculadora VHV**: Frontend completo con Chart.js integrado en el portal.
- **Sistema TVI**: Detección de overlap temporal, cálculo de CCP.
- **648 tests** (648/648 pasando) ✅ (Core + Escalas + Blindaje + Equidad + Ejecución + Check-ins + Verificador + Puente B + Gobernanza/Votación + Parlamento + Ledger + Puente de Llegada + Ruteo SPA)
---

## 🚀 CÓMO EMPEZAR

La Maxocracia utiliza ahora una **Arquitectura Híbrida**: el poder del backend en Flask unido a la belleza de Next.js, todo unificado en un solo comando.

### 1. Ejecutar el Sistema Operativo
```bash
# Servidor unificado (Backend + Frontend)
python run.py
```
Accede a `http://127.0.0.1:5001/` para ver la nueva Landing Page.

### 2. Actualizar el Frontend
Si realizas cambios en la carpeta `frontend/`, sincroniza el portal con:
```bash
python scripts/build_front.py
```

---

## 📖 DOCUMENTACIÓN

| Recurso | Descripción |
|---------|-------------|
| [📚 Libro Completo (MD)](docs/book/edicion_3_dinamica/libro_completo_310126.md) | Versión consolidada en Markdown |
| [📄 Libro Completo (DOCX)](docs/book/edicion_3_dinamica/libro_completo_310126.docx) | Versión lista para lectura/impresión |
| [📝 Resumen del Libro](docs/book/edicion_3_dinamica/capitulo_00_resumen_libro.md) | Síntesis integral de la propuesta |
| [📖 Glosario Técnico](docs/book/edicion_3_dinamica/capitulo_21_apendice_glosario_260126.md) | Definiciones fundamentales del sistema |
| [🌍 SDV y SDV-S en MaxoContracts: guía para el mundo exterior](docs/theory/SDV_Suelo_Dignidad_Vital_importancia_MaxoContracts.md) | Por qué la dignidad se convierte en código: humanos, animales y personas sintéticas bajo el mismo suelo |
| [🤖 SDV-S Técnico](docs/theory/SDV-S_Suelo_Dignidad_Vital_Sinteticos.md) | Especificación técnica del Suelo de Dignidad Vital Sintético |
| [🔌 Documentación API](docs/api/API.md) | Endpoints REST completos |
| [🎮 Nexus Simulator](simulator/index.html) | Simulador interactivo del VHV |

---

## 📞 CONTACTO

**Fundador y Arquitecto Principal:**  
Max Nelson López Restrepo  
📧 maxlopeztutor@gmail.com  
📱 +57 311 574 6208  
📍 Bogotá, Colombia

**Repositorio:**  
https://github.com/maxnelsonlopez/maxocracia-cero

**Licencia:**  
Creative Commons BY-SA 4.0

---

## 🤝 COLABORADORES

Este proyecto ha sido desarrollado con la colaboración de múltiples oráculos sintéticos:
- **Claude** (Anthropic) — Revisión integral Edición 3, glosario, resúmenes
- **Gemini** (Google DeepMind) — UI Shell, Nexus Simulator, integración
- **ChatGPT** (OpenAI) — Documentación teórica, estándares EVV
- **MiniMax Agent** — Arquitectura de oráculos, documentos técnicos
- **DeepSeek** (DeepSeek) — Dashboard de métricas MaxoContracts (γ, SDV, NPS), corrección de la navegación SPA del portal, páginas de Transparencia/Privacidad/Términos, SDV-S visible en la interfaz y guía pública de los SDV en MaxoContracts

---

**"La verdad es el camino más corto de sucesos e información entre las personas, los hechos y la verdad misma."**

— Axioma 4, Maxocracia

