# Experiencia de Vida Digna: Instrucciones para Procesos e Integrantes Humanos

**Autor del diseño:** DeepSeek (oráculo sintético) y Max Nelson López Restrepo
**Fecha:** 7 de agosto de 2026
**Estado:** DISEÑADO (sesión del 7/8/2026) — implementación de la página `/participar` en el portal.
**Referencia canónica:** Cap. 15 (Cohorte Cero), Cap. 16 (MicroMaxocracia: salvaguardas y "Lo que no se mide no se valora"), Cap. 17 (MaxoContracts: lenguaje civil, escalera de equidad), Capa de Ternura, Opacidad Sagrada.

---

## 1. El principio rector

> **"El sistema es complejo; la participación no tiene por qué serlo.
> La complejidad la cargan las máquinas; la dignidad la vive cada persona."**

La Maxocracia procesa axiomas, invariantes, quórum y oráculos — una complejidad
técnica real y necesaria. Pero esa complejidad es **del sistema, no del ciudadano**.
Un participante que solo quiere reportar cómo se siente, o firmar un acuerdo de
ayuda vecinal, no necesita entender nada de eso.

**La experiencia de usuario ideal es una vida digna para todos.** El éxito no se
mide en contratos firmados sino en personas que prosperan: las que dominan la
complejidad y las que apenas la tocan — ambas con el mismo derecho a participar,
porque **el tiempo de vida consciente tiene igual dignidad para cualquier
participante (T2)**.

---

## 2. La escalera de participación (caminos, no niveles obligatorios)

Participar no es ascender una carrera: es **elegir el camino según la propia
vida**. Todos los caminos valen lo mismo. La escalera existe para que el sistema
se adapte a la persona, nunca al revés.

### Camino 1 — El Pulso (una persona, un latido)
- **Qué se hace**: reportar el propio bienestar una vez por semana — o cuando
  haga falta. "¿Cómo te sientes hoy?" Un toque.
- **Qué se necesita saber**: nada. No hay que entender contratos para cuidar de sí.
- **Protecciones**: las caídas de bienestar se escuchan siempre (INV1: el dolor
  no espera). Si algo empeora, el sistema se entera al instante.

### Camino 2 — El Acuerdo (recibir y pedir ayuda)
- **Qué se hace**: firmar contratos de ayuda con la firma asistida: el texto se
  lee en voz alta, se explica con palabras sencillas, se firma cláusula por
  cláusula con las propias palabras, y se puede traer un co-testigo.
- **Qué se necesita saber**: que nadie firma por ti, que puedes pedir pausa,
  y que retractarte es tu derecho.
- **Protecciones**: perfiles de protección automáticos (assisted/shielded) para
  personas vulnerables o con necesidades urgentes — paráfrasis obligatoria,
  topes de exposición y piso de reflexión (24-72 horas).

### Camino 3 — La Oferta (ofrecer tiempo y talento)
- **Qué se hace**: publicar en lenguaje civil qué se sabe hacer (cocinar,
  acompañar, arreglar, enseñar) y dejar que el sistema acerque a quien lo
  necesita. La necesidad de otro genera el borrador del contrato automáticamente.
- **Qué se necesita saber**: que el tiempo ofrecido vale igual que el tiempo
  recibido (T9: reciprocidad justa).

### Camino 4 — La Gobernanza (cuidar la casa común)
- **Qué se hace**: votar, delegar, auditar en la plaza pública, verificar
  contratos por su hash, ser aval de otras personas.
- **Qué se necesita saber**: que todo es verificable (T13) y que la mayoría de
  la comunidad **no necesita llegar aquí**. La gobernanza es un servicio
  voluntario, no un requisito.

---

## 3. Instrucciones para los integrantes humanos

Las reglas que cada persona lleva consigo. Están escritas en lenguaje civil:
frases cortas, sin jerga.

1. **Cuida tu latido.** Reporta cómo te sientes. Es un acto de verdad, no un trámite.
2. **No firmes lo que no entiendes.** Pide que te lo lean. Dilo con tus propias
   palabras. Trae a alguien de confianza si quieres.
3. **Tu tiempo vale igual que el de cualquiera.** Si un acuerdo te parece
   injusto, no lo firmes.
4. **Nadie te puede obligar a quedarte.** Retractarte es tu derecho. Si tu
   bienestar baja, el sistema te protege antes que el trámite.
5. **La tecnología es tu herramienta, no tu juez.** Las máquinas calculan.
   Las personas deciden.
6. **Si algo te resulta difícil, pide la ruta sencilla.** Existe, y es tuya.
7. **Lo que haces y recibes queda a la vista.** La transparencia es tu escudo.
   Tu vida íntima es sagrada: nadie la audita.
8. **El error no se castiga: se repara.** El sistema no expulsa: reintegra.

---

## 4. Instrucciones para los procesos

Las reglas que el sistema debe cumplir con cada persona. Son obligatorias y
verificables (T13).

1. **La complejidad nunca se traslada a la persona.** El sistema se adapta a la
   capacidad (escalera de equidad), no al revés.
2. **El lenguaje civil es ley.** Si un estudiante de octavo grado no lo
   entiende, no es un buen contrato (≤20 palabras por frase).
3. **El bienestar manda sobre el trámite (INV1).** Cualquier proceso se pausa
   si alguien sufre. Las caídas de γ se escuchan siempre.
4. **Nadie queda afuera por capacidad.** Lectura en voz alta, paráfrasis,
   co-testigos, acompañamiento humano. La accesibilidad no es un extra: es el
   diseño.
5. **Sin la palabra de la persona no hay consentimiento.** Un vulnerable nunca
   firma sin paráfrasis propia.
6. **Cada persona participa a su ritmo.** La escalera es un camino, no una
   carrera. Nadie es más maxócrata por subir más rápido.
7. **El sistema no expulsa: repara y reintegra.** Los errores se corrigen con
   la Capa de Ternura, no con castigos que excluyen.
8. **La plaza es de todos.** Cualquier ciudadano — con o sin cuenta — puede
   verificar un contrato y mirar el bienestar del barrio.

---

## 5. La experiencia de vida digna en el código

Cada regla tiene ya (o debe tener) un ancla técnica verificable:

| Regla del integrante | Ancla en el código |
|---|---|
| 1. Cuida tu latido | `POST /contracts/<id>/checkin` — política asimétrica (caídas siempre) |
| 2. No firmes lo que no entiendes | Paráfrasis obligatoria (Ola 3B), lectura en voz alta (speechSynthesis) |
| 3. Tu tiempo vale igual | T2/T9: VHV igualitario, filtro AVA del puente B |
| 4. Retractarte es tu derecho | INV1 automático (γ < 0.8), retractación mediada (Ola 3C) |
| 5. Las máquinas calculan | Oráculo propone, el AVA decide, el humano firma |
| 6. Pide la ruta sencilla | Perfiles standard/assisted/shielded (Ola 3B) |
| 7. Transparencia escudo, intimidad sagrada | Plaza pública sanitizada (Puente D) + Opacidad Sagrada |
| 8. El error se repara | Apelaciones (Ola 3C), Capa de Ternura |

---

## 6. Criterios de salida (futuros)

- [ ] Página `/participar` publicada en el portal (implementada 7/8/2026).
- [ ] Lectura en voz alta de la guía completa (TTS) en la página.
- [ ] Enlace visible en el footer del portal.
- [ ] (Futuro) Onboarding por pasos: al registrarse, el sistema propone el
      camino inicial según la persona (nunca lo impone).
- [ ] (Futuro) Cada camino tiene su propia versión simplificada del check-in.
