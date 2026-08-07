# Maxocracia-Cero: Sistema Operativo para una Civilización Coherente

**Estado del Proyecto:** Fase 2 - Sostenibilidad Económica y MicroMaxocracia Doméstica (Agosto 2026)  
**Última actualización:** 6 de agosto 2026  
**Versión:** 4.7 - Gobernanza colectiva avanzada: delegación líquida, ciclo de vida del quórum y cohorte (DeepSeek)

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

### Capítulos Destacados
- **Cap. 3: Victoria Sintética** — El consenso ético entre inteligencias artificiales.
- **Cap. 16: MicroMaxocracia** — Equidad doméstica y el Modelo de 3 Cuentas.
- **Cap. 17: MaxoContracts** — Contratos inteligentes éticos y bloques modulares.
- **Cap. 18: Estándar EVV 1.2** — Especificación técnica para el Vector de Huella Vital.

### Software Funcional
- **Portal Unificado (Hybrid Frontend)**: Nueva landing page moderna (Next.js) servida por Flask.
- **MicroMaxocracia v1.0**: Registro interactivo de CDD, balance de Tres Cuentas en UI, encuesta de seguridad ESI con pantalla de bloqueo y monitor Detox relacional en tiempo real.
- **Nexus Simulator v2.2**: Simulador interactivo del VHV con Modo Oráculo Dinámico.
- **MaxoContracts v2.5**: Persistencia SQLite, 5 bloques modulares, oráculo sintético en vivo (DeepSeek), constructor de contratos visual (React Flow) con biblioteca de plantillas, validador de grafos, UX sobre-explicada liminal y **partes de cualquier escala** (personas, micro-sociedades, cooperativas, instituciones, sintéticas y ecosistemas).
- **SDV-S en la Interfaz**: Panel "Reino Sintético · SDV-S" en el detalle de contratos — FS_S = e^v, las 5 dimensiones de la ontometría sintética, violaciones y el Invariante INV2-S con el camino de Ternura. Las rutas dinámicas de `/contracts/` funcionan en pestaña nueva y por clic.
- **Dashboard de Métricas MaxoContracts**: Panel `/admin/contracts` con γ (bienestar), alertas del Invariante 1 (γ<1), violaciones SDV (humanos y sintéticos), NPS de la Cohorte y progreso hacia la meta de 50 contratos.
- **Portal de Transparencia Radical (T13)**: Páginas públicas `/transparency` (reporte vivo de costos e ingresos), `/privacy` (Opacidad Sagrada) y `/terms` (coherencia axiomática).
- **Navegación SPA reparada**: La navegación por clic funciona en todo el portal (barra superior, dropdowns, panel admin y secciones de usuario) — payloads RSC de la exportación estática servidos correctamente.
- **Escalas e Interescala (Bloque B)**: Un contrato ya no es solo persona↔persona — persona, micro-sociedad, cooperativa, institución, persona sintética y ecosistema son **Partes** con el mismo marco axiomático (`society-`, `coop-`, `org-`, `eco-`). Registro `maxo_parties` con API `/parties`, selector de partes colectivas en el builder, consentimiento agregado por **quórum delegado N de M**, guardián oráculo para el **Reino Natural** (`eco-`) y contratos interescala **anidados** (madre/hijos) con protección de ciclos.
- **Gobernanza colectiva avanzada (hackathon)**: **votación ponderada** (pesos por delegado y umbral de peso), **delegación temporal** (ceder la firma a un apoderado, cadena auditable), **γ agregado real** (el bienestar de la parte colectiva es la media ponderada del γ de sus miembros en el contrato), **jerarquía interescala** (árbol madre→hijos navegable en el detalle + endpoint `/tree`), **delegación líquida por término**, **expiración de delegaciones**, **ciclo de vida del quórum** (deadline, prórroga y re-consulta automática) y **vista de cohorte** consolidada de todas las partes colectivas.
- **Oráculo en vivo (Bloque A)**: DeepSeek negocia contratos por chat (`/contracts/negotiate`), audita existentes (`critique`) y firma como guardián de ecosistemas. Activado con `DEEPSEEK_API_KEY` en `.env`; sin key, degradación elegante al oráculo heurístico.
- **Calculadora VHV**: Frontend completo con Chart.js integrado en el portal.
- **Sistema TVI**: Detección de overlap temporal, cálculo de CCP.
- **501 tests** (501/501 pasando) ✅ (Backend Core + Blocks + Escalas + Quórum + Pesos + Delegación + Ciclo de vida + Cohorte + Métricas + Ruteo SPA)
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

