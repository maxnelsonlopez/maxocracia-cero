# Guía para Facilitadores: Cómo Iniciar una Cohorte Maxocracia

**Última actualización:** Diciembre 2025  
**Tiempo de lectura:** 15 minutos  
**Tiempo para iniciar una Cohorte:** 2-4 semanas de preparación

---

## ¿Qué es esto?

Esta guía te permite iniciar una **Red de Apoyo Maxocracia** en tu ciudad, sin conocer personalmente al fundador. Si puedes reunir 11 personas comprometidas y dedicar 2 horas semanales, puedes ser un facilitador.

> **Maxocracia** es un sistema de coordinación social donde las personas intercambian tiempo, conocimientos, objetos y apoyo basándose en necesidades reales y reciprocidad orgánica—no deudas.

---

## 📋 Requisitos Previos

### Mínimos para empezar:

| Requisito | Descripción |
|-----------|-------------|
| **11 personas** | Comprometidas a 90 días de experimento |
| **2h/semana** | Tiempo del facilitador (tú) |
| **Google Sheets** | Para tracking de intercambios |
| **Google Forms** | Para formularios de inscripción |
| **Grupo de chat** | WhatsApp, Telegram, o Discord |
| **$50 USD** | Opcional, para herramientas compartidas |

### Lecturas obligatorias antes de empezar:

1. **[maxocracia_brochure.md](maxocracia_brochure.md)** — Introducción de 10 min
2. **[MAXOCRACIA_MANIFIESTO.md](MAXOCRACIA_MANIFIESTO.md)** — Los 8 Axiomas de la Verdad
3. **[playbook_cohorte_cero.txt](playbook_cohorte_cero.txt)** — Protocolo de 90 días

---

## Paso 1: Preparación Personal (Semana 1)

### 1.1 Lee los documentos fundamentales

```
Orden recomendado:
1. maxocracia_brochure.md (visión general)
2. MAXOCRACIA_MANIFIESTO.md (principios)
3. matematicas_maxocracia_compiladas.md (opcional, si quieres profundidad)
4. playbook_cohorte_cero.txt (operacional)
5. FAQ_EXTENDIDO.md (para responder objeciones)
```

### 1.2 Comprende los 8 Axiomas de la Verdad

Estos son el núcleo del sistema. Memorízalos:

1. **Brújula Interna** — Lealtad a la verdad que descubres
2. **Compromiso Activo** — Coherencia por encima de comodidad
3. **Profundidad** — Rechazar explicaciones simplistas
4. **Eficiencia Espiritual** — La verdad es el camino más corto
5. **Ojo Claro** — Separar hechos de interpretación
6. **Verbo Justo** — Ni más ni menos que la verdad necesaria
7. **Optimismo Realista** — Máximo potencial dentro de límites reales
8. **Confianza Cósmica** — Todo lo que existe se estructura en la verdad

### 1.3 Prepara tu discurso de 2 minutos

Practica explicar Maxocracia en 2 minutos:

> "Es una red de apoyo donde intercambiamos tiempo, conocimientos y recursos basándonos en necesidades reales. No hay deudas—hay reciprocidad orgánica. Vamos a experimentar por 90 días para ver qué funciona y qué no. Todo se documenta, todo se aprende."

---

## Paso 2: Reclutamiento (Semanas 1-2)

### 2.1 Perfil ideal de participantes

Busca personas que:
- ✅ Tengan algo que ofrecer (tiempo, conocimiento, objetos, espacio)
- ✅ Tengan alguna necesidad real (no importa cuán pequeña)
- ✅ Estén dispuestas a comprometerse 90 días
- ✅ Valoren la honestidad y la reciprocidad

Evita personas que:
- ❌ Solo quieran recibir sin dar
- ❌ No puedan comprometerse al menos 1h/semana
- ❌ Tengan resistencia fuerte a documentar

### 2.2 Cómo encontrar a las 11 personas

**Canales efectivos:**
- Amigos cercanos que confías (núcleo inicial de 3-4)
- Grupos de vecinos o comunidad local
- Espacios de coworking, talleres, meetups
- Redes de voluntariado existentes

**Pitch para reclutamiento:**

> "Estoy iniciando un experimento de 90 días donde un grupo de 11 personas nos ayudamos mutuamente con lo que necesitamos y podemos ofrecer. No hay dinero de por medio, solo reciprocidad. ¿Te interesa?"

### 2.3 Formulario de inscripción

Usa el **[formulario_CERO_inscripcion.md](../formularios/formulario_CERO_inscripcion.md)** como base para crear tu Google Form.

Ver: **[INSTRUCCIONES_GOOGLE_FORMS.md](../formularios/INSTRUCCIONES_GOOGLE_FORMS.md)**

---

## Paso 3: Configurar Herramientas (Semana 2)

### 3.1 Formularios Web Integrados (RECOMENDADO)

El repositorio incluye formularios web listos para usar que se conectan directamente a la base de datos:

| Formulario | URL | Propósito |
|------------|-----|-----------|
| **Form CERO** | `/static/form-cero.html` | Inscripción de participantes |
| **Form A** | `/static/form-exchange.html` | Registro de intercambios |
| **Form B** | `/static/form-followup.html` | Seguimiento y evaluación |

**Ventajas sobre Google Forms:**
- ✅ Datos directos en la base de datos (no requiere exportar)
- ✅ Matching automático de ofertas/necesidades
- ✅ Dashboard de analytics integrado
- ✅ No dependes de servicios externos

**Para usarlos:**
1. Inicia el servidor: `python run.py`
2. Comparte el link: `http://tu-servidor:5001/static/form-cero.html`

### 3.2 Alternativa: Google Forms

Si prefieres Google Forms (p.ej. sin servidor propio), sigue las instrucciones en:
- **[INSTRUCCIONES_GOOGLE_FORMS.md](../formularios/INSTRUCCIONES_GOOGLE_FORMS.md)**

### 3.3 Google Sheets (Hoja de cálculo maestra)

Crea una hoja con las siguientes pestañas:

| Pestaña | Propósito |
|---------|-----------|
| `Participantes` | Lista de 11 personas, ofertas, necesidades |
| `Intercambios` | Registro de cada intercambio completado |
| `TVI Log` | Tiempo Vital Indexado de cada persona |
| `Métricas` | Cálculos automáticos (UTH, tasa resolución) |

### 3.3 Grupo de comunicación

Crea grupo en WhatsApp, Telegram, o Discord con reglas claras:

```
📋 Reglas del grupo:
1. Solo intercambios y coordinación
2. Honestidad radical
3. No spam, no ventas
4. Confidencialidad sobre situaciones personales
```

---

## Paso 4: Ceremonia de Inicio (Semana 3)

### 4.1 El Pacto de la Cohorte

Reunión presencial (o virtual) de 90 minutos:

**Agenda:**
1. **Bienvenida** (5 min) — El facilitador explica qué van a hacer
2. **Lectura de Axiomas** (20 min) — Cada persona lee un axioma en voz alta
3. **Compromiso verbal** (15 min) — Cada persona dice:
   - "Me comprometo a la honestidad radical sobre mi tiempo"
   - "Me comprometo a no juzgar los registros de los demás"
   - "Me comprometo a la confidencialidad"
4. **Presentación de ofertas/necesidades** (40 min) — Cada persona comparte brevemente
5. **Primeros matches** (10 min) — El facilitador sugiere 2-3 intercambios iniciales

### 4.2 Documentos para la ceremonia

Imprime o comparte en pantalla:
- Los 8 Axiomas de la Verdad
- El formulario de inscripción ya lleno por cada persona
- La hoja de cálculo maestra

---

## Paso 5: Operación Semanal (Meses 1-3)

### 5.1 Ritual semanal: "Puesta en Común" (60 min)

**Frecuencia:** Cada semana, mismo día/hora  
**Formato:** Presencial o videollamada

**Agenda:**
1. **Check-in rápido** (10 min) — ¿Cómo está cada persona?
2. **Intercambios de la semana** (20 min) — ¿Qué pasó? ¿Qué se aprendió?
3. **Nuevas necesidades** (15 min) — ¿Alguien tiene algo nuevo?
4. **Matching** (10 min) — El facilitador propone conexiones
5. **Cierre** (5 min) — ¿Algo para la próxima semana?

### 5.2 Tu rol como facilitador

**Semanal:**
- [ ] Revisar formularios de intercambio (Formulario A)
- [ ] Actualizar hoja de cálculo
- [ ] Facilitar la reunión semanal
- [ ] Proponer matches entre ofertas y necesidades

**Mensual:**
- [ ] Enviar Formulario B (seguimiento) a cada persona
- [ ] Analizar métricas básicas
- [ ] Ajustar protocolo si algo no funciona

### 5.3 Documentación obligatoria

Cada intercambio debe quedar registrado en Formulario A:
- Quién dio / quién recibió
- Tipo de intercambio
- UTH (horas humanas invertidas)
- ¿Se resolvió la necesidad? (1-5)

---

## Paso 6: Evolución por Mes

### Mes 1: Despertar Ontológico
- **Foco:** Aprender a ver el tiempo
- **Herramienta:** TVI Log (cada persona registra su tiempo diario)
- **Meta:** Calcular primer CCP (Coeficiente de Coherencia Personal)

### Mes 2: Contabilidad Existencial
- **Foco:** Introducir VHV y Maxo Beta
- **Herramienta:** Calculadora VHV simplificada
- **Meta:** Que cada persona calcule el VHV de una comida

### Mes 3: Gobernanza Coherente
- **Foco:** Decisiones colectivas
- **Herramienta:** Fondo Común (10% de Maxos Beta)
- **Meta:** Una propuesta votada y ejecutada por el grupo

---

## 📊 Métricas de Éxito

Tu Cohorte es exitosa si al final de 90 días:

| Métrica | Target |
|---------|--------|
| Participación sostenida | 80% (9/11 personas) |
| Intercambios documentados | 20+ |
| Insights reveladores | 5+ descubrimientos |
| Innovaciones propuestas | Al menos 1 mejora al protocolo |

---

## 🆘 Problemas Comunes y Soluciones

### "Nadie llena los formularios"

**Solución:** Simplifica. Reduce a 5 preguntas obligatorias. El facilitador puede llenar por ellos después de cada intercambio.

### "Siempre dan los mismos 3 personas"

**Solución:** Habla directamente con los que solo reciben. Pregunta: "¿Hay algo pequeño que puedas ofrecer?" A veces es un bloqueo psicológico, no falta de recursos.

### "La reunión semanal se alarga mucho"

**Solución:** Usa timer estricto. 60 minutos máximo. Lo que no se diga en la reunión se resuelve en chat.

### "Alguien está en crisis seria"

**Solución:** La red puede ayudar, pero tiene límites. Conecta con recursos profesionales (salud mental, servicios sociales) cuando sea necesario. Documenta y aprende.

---

## 📚 Recursos

### Documentos esenciales
- [maxocracia_brochure.md](maxocracia_brochure.md)
- [MAXOCRACIA_MANIFIESTO.md](MAXOCRACIA_MANIFIESTO.md)
- [playbook_cohorte_cero.txt](playbook_cohorte_cero.txt)
- [FAQ_EXTENDIDO.md](FAQ_EXTENDIDO.md)

### Formularios
- [formulario_CERO_inscripcion.md](../formularios/formulario_CERO_inscripcion.md)
- [formulario_A_registro_intercambio.md](../formularios/formulario_A_registro_intercambio.md)
- [formulario_B_reporte_seguimiento.md](../formularios/formulario_B_reporte_seguimiento.md)

### Tutoriales
- [Tutorial: Calculadora VHV](tutoriales/tutorial_calculadora_vhv.md)
- [Tutorial: Registrar tu TVI](tutoriales/tutorial_tvi.md)

### Aplicación web (opcional)
Si quieres usar la aplicación web:
- Ver [README.md principal](../README.md) para instrucciones de instalación
- La Calculadora VHV está en `http://localhost:5001/static/vhv-calculator.html`

---

## 🤝 Contacto y Comunidad

**Fundador:** Max Nelson López  
📧 maxlopeztutor@gmail.com  
📱 +57 311 574 6208  
📍 Bogotá, Colombia

**Para facilitadores:**
- Reporta tus aprendizajes al email del fundador
- Tus insights ayudarán a mejorar el protocolo para otras Cohortes
- Considera escribir tu propio "Informe de Hallazgos" al final de los 90 días

---

*"La verdad es el camino más corto. La honestidad radical es el camino más eficiente."*  
— Axioma 4, Código de Coherencia

---

**Versión:** 1.0  
**Creado:** Diciembre 2025  
**Licencia:** Dominio público - Comparte libremente
