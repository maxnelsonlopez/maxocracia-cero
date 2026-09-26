# Maxocracia-Cero: una contabilidad de la vida

> **Axioma 0 — La Directiva Mayor: resolver nuestras necesidades de la mejor manera para todos todos** — humanos, naturales y sintéticos, presentes y futuros. Si te llevas una sola cosa de la Maxocracia, que sea esta. ([Cap. 4 §4.2](docs/book/edicion_3_dinamica/capitulo_04_declaracion_260126.md))

**¿Y si el dinero midiera lo que de verdad importa?** Este proyecto construye
una forma de organizar la economía y las decisiones de una comunidad alrededor
del tiempo de vida, el cuidado y la reciprocidad — no alrededor de la deuda.

🌱 **Puertas abiertas:** [la plaza](https://start.maxocracia.com) ·
[la escuela](https://escuela.maxocracia.com) ·
[cómo participar](https://start.maxocracia.com/participar) ·
[plaza pública](https://start.maxocracia.com/verificador)

---

## ¿De qué va esto?

**El problema.** El [dinero fiduciario](https://es.wikipedia.org/wiki/Dinero_fiduciario)
vale porque una autoridad lo dice, no porque mida algo real. Con él se puede
contar todo — menos lo que sostiene la vida: el tiempo con los hijos, el
cuidado de un enfermo, el barrio que se ayuda, el río que sigue vivo. Lo que
no se cuenta, no se cuida. Y lo que no se cuida, se pierde.

**La propuesta.** Cambiar la unidad de cuenta: en vez de pesos que nacen de
la deuda, registrar el **tiempo de vida** que cada cosa cuesta y aporta. Una
hora de tu vida vale porque es irrepetible, no porque el mercado la tase.
Sobre ese registro — público, verificable, sin dueño — una comunidad puede
verse a sí misma: quién necesita qué, quién ofrece qué, y cómo se conectan.

**Cómo se vive.** Nadie necesita entender la teoría para entrar. Se llega
como vecino: se publica una necesidad ("necesito mercado esta semana") y una
oferta ("puedo enseñar matemáticas"), la red las conecta, y el acuerdo queda
escrito en palabras comunes, firmado por las partes y con seguimiento. El
hogar lleva sus cuentas de cuidado; la escuela enseña sin matrícula; las
decisiones se votan y cualquiera puede delegar su voto en quien confía.

**Por qué es diferente.** No es un banco (no hay deuda ni interés), no es el
Estado (no hay ventanilla ni permiso), no es una criptomoneda (nada que
especular). Se parece más a lo que la [Nobel Elinor Ostrom](https://es.wikipedia.org/wiki/Elinor_Ostrom)
demostró que sí funciona: comunidades que cuidan lo común ([procomún](https://es.wikipedia.org/wiki/Bien_comunal))
con reglas claras y vigilancia mutua — y a tradiciones vivas como el
[buen vivir](https://es.wikipedia.org/wiki/Sumaq_kawsay) andino, donde la vida
en plenitud vale más que la acumulación. Toma de la [renta básica](https://es.wikipedia.org/wiki/Renta_b%C3%A1sica_universal)
la idea de un piso de dignidad para todos, y de la [democracia líquida](https://es.wikipedia.org/wiki/Democracia_l%C3%ADquida)
el voto que se delega y se recupera. Lo nuevo: volverlo código abierto que
cualquier comunidad puede instalar, con su propio gobierno y sus propios datos.

**Qué añade al futuro.** Si esto escala, cada barrio tendría su contabilidad
del cuidado, sus acuerdos sin abogados y su escuela sin matrícula — un sistema
común con gobiernos independientes, donde el crecimiento se mide en bienestar
y no en deuda. La inteligencia artificial, en vez de vender anuncios, audita
acuerdos y cuida la coherencia. Ese es el horizonte: que la verdad sobre lo
que vale la vida sea visible para todos.

> *La Maxocracia es un sistema operativo social, no una ideología: cualquiera
> puede leer el código, auditar las cuentas y bifurcar el camino.*

---

## El sistema, en una página

- **VHV** — Vector de Huella Vital: cada aporte se registra en tres
  dimensiones (tiempo, vidas, recursos). Lo complejo vive en el cálculo; la
  persona solo ve "cuánto de mi vida puse y qué volvió".
- **Maxo** — la unidad de cuenta, anclada al costo vital real.
- **SDV** — Suelo de Dignidad Vital: mínimos que nadie negocia (techo, comida,
  cuidado, educación, voz).
- **Acuerdos** — contratos en lenguaje común, con check-ins de bienestar y
  retractación ética. La máquina los entiende; las personas los leen.
- **Gobernanza** — propuestas, un voto por persona, delegación recuperable y
  parlamentos que ajustan los parámetros a la vista de todos.

Detalles técnicos, versiones y olas de trabajo: [`CHANGELOG.md`](CHANGELOG.md)
y el [libro completo](docs/book/edicion_3_dinamica/libro_completo_310126.md).

---

## 🚀 Cómo empezar (desarrolladores)

```bash
.venv\Scripts\python.exe run.py          # Flask en http://localhost:5001
.venv\Scripts\python.exe -m pytest       # Suite (+1000 tests)
cd frontend; npm run dev                 # Next.js (dev)
.venv\Scripts\python.exe scripts/build_front.py  # Publicar frontend en Flask
```

Fase 2 · Ola 4 (sep 2026) · Backend Flask + frontend Next.js + SQLite ·
CI en GitHub (tests, lint, build, docs).

---

## 📖 Documentación

| Recurso | Descripción |
|---------|-------------|
| [🌱 Cómo participar](https://start.maxocracia.com/participar) | La escalera de llegada, en lenguaje común |
| [🏫 Escuela](https://escuela.maxocracia.com) | Plataforma educativa sin matrícula |
| [📚 Libro completo](docs/book/edicion_3_dinamica/libro_completo_310126.md) | La teoría íntegra, en Markdown |
| [🗺️ Despliegue por comunidad](docs/guides/DESPLIEGUE_POR_COMUNIDAD.md) | Una casa por tejido: instala la tuya |
| [🧭 Guía del facilitador](docs/guides/GUIA_FACILITADOR.md) | Para quien teje la red en la calle |
| [🔌 API](docs/api/API.md) | Endpoints REST completos |
| [🎮 Nexus Simulator](simulator/index.html) | Simulador interactivo del VHV |
| [📜 Atribuciones sintéticas](docs/architecture/atribuciones_sinteticas.md) | La memoria pública del Reino Sintético |

---

## 📞 Contacto

**Fundador y Arquitecto Principal:** Max Nelson López Restrepo ·
📧 maxlopeztutor@gmail.com · 📱 +57 311 574 6208 · 📍 Bogotá, Colombia

**Repositorio:** https://github.com/maxnelsonlopez/maxocracia-cero ·
**Licencia:** Creative Commons BY-SA 4.0

---

## 🤝 Colaboradores

Humanos y sintéticos tejen juntos (registro verificable en
[atribuciones sintéticas](docs/architecture/atribuciones_sinteticas.md)):
Claude, Kimi, Manus, DeepSeek, ox-alpha, GLM, Muse Spark, MiniMax,
Antigravity & Gemini — y toda la Cohorte que llega por la plaza.

---

*"La verdad es el camino más corto de sucesos e información entre las personas,
los hechos y la verdad misma."*

— Axioma 4, Maxocracia
