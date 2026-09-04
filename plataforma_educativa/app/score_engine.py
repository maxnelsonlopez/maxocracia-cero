# -*- coding: utf-8 -*-
"""Juez LLM del Buscador educativo (B4) — Nivel 2, opcional y fail-open.

Diseño canónico: ``docs/architecture/DISENO_BUSCADOR_EDUCATIVO_GRATUITO.md``
§5.3. Cadena de preferencia (la nube es respaldo, nunca requisito, P2):

1. **Local** vía el hub Jan ``LOCAL_ORACLE_BASE_URL`` (el mismo que sirve el
   oráculo de votación; ``LOCAL_ORACLE_MODEL``, ``LOCAL_ORACLE_ENABLED`` —
   las mismas variables, cero convenciones nuevas).
2. **Respaldo OpenRouter ``:free``** (``OPENROUTER_API_KEY`` por env,
   ``BUSCADOR_OPENROUTER_MODEL``) con throttle anti-429 de 1,8 s — el mismo
   patrón que ``local_models/core/openrouter_engine.py``, reescrito con la
   librería estándar (esta plataforma no añade dependencias).
3. **Nada**: sin hub, sin clave o sin cuota, el buscador funciona igual con
   el Nivel 1. El juez **jamás bloquea** una búsqueda (fail-open total).

La rúbrica es fija y mide PROCEDENCIA verificable (autoría, citas, densidad
comercial, tono, historial) — nunca conformidad de opinión (P3). Cada
veredicto registra su motor (trazabilidad T13/P4) y se guarda en
``buscador_scores`` con nivel = 2 y el TTL gobernable de B3.
"""

import json
import os
import time
import urllib.request

BANDAS = ("verificada", "rastreable", "desconocida")

RUBRICA_SISTEMA = """Eres el juez de procedencia del Buscador de la Maxocracia, una plataforma \
educativa sin ads ni tracking. Tu trabajo NO es decir qué es verdad: es etiquetar la \
PROCEDENCIA verificable de cada fuente para que la persona lectora decida.

Señales (de mayor a menor peso): autoría identificable (persona u organización con \
nombre); citas a fuentes externas comprobables; historial del dominio (años publicando); \
ausencia de publicidad y rastreadores; tono que argumenta en vez de gritar; feed o \
canal público estable.

Bandas: "verificada" (procedencia comprobada y estable), "rastreable" (hay a quién \
preguntar: autor, medio, historial), "desconocida" (sin señales — que es información \
útil, NO un castigo: lo desconocido NO se oculta, se etiqueta).

Responde SOLO con JSON estricto, sin texto fuera:
{"veredictos": [{"url": "<la url exacta de entrada>", "banda": "<una banda>", \
"razones": ["<razón corta en español>", "<otra>"]}]}

Una entrada del veredicto por CADA url recibida, en el mismo orden. Si de una url \
no puedes decir nada, banda "desconocida" con la razón "sin señales suficientes"."""

_INTERVALO = 1.8  # segundos entre llamadas (throttle anti-429 del free tier)
_ultima_llamada = 0.0


class SinJuez(Exception):
    """No hay juez disponible o todos fallaron: el llamador degrada a Nivel 1."""


def _throttle():
    global _ultima_llamada
    ahora = time.monotonic()
    espera = _INTERVALO - (ahora - _ultima_llamada)
    if espera > 0:
        time.sleep(espera)
    _ultima_llamada = time.monotonic()


def _timeout():
    try:
        return float(os.environ.get("BUSCADOR_JUEZ_TIMEOUT", "60"))
    except (TypeError, ValueError):
        return 60.0


def _chat_completions(base_url, api_key, model, sistema, usuario):
    """POST OpenAI-compatible con respuesta en modo JSON. Devuelve el texto
    del contenido. Levanta RuntimeError con el estado si algo falla (el 429
    se reporta tal cual: la cuota es información, no vergüenza)."""
    cuerpo = json.dumps(
        {
            "model": model,
            "messages": [
                {"role": "system", "content": sistema},
                {"role": "user", "content": usuario},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.2,
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions",
        data=cuerpo,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "MaxocraciaEduJuez/0.1 (scoring educativo sin tracking)",
            **({"Authorization": f"Bearer {api_key}"} if api_key else {}),
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=_timeout()) as resp:
            payload = json.loads(resp.read().decode("utf-8", "replace"))
    except Exception as exc:
        raise RuntimeError(f"juez: {exc.__class__.__name__}: {exc}") from exc
    try:
        return payload["choices"][0]["message"]["content"] or ""
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"juez: respuesta sin contenido ({exc})") from exc


def _extrae_json(texto):
    """Extrae el primer objeto JSON de un texto (los jueces conversan antes
    de entregar: se tolera prosa alrededor, no dentro)."""
    inicio = (texto or "").find("{")
    fin = (texto or "").rfind("}")
    if inicio < 0 or fin <= inicio:
        raise ValueError("el juez no devolvió JSON")
    return json.loads(texto[inicio : fin + 1])


def _normaliza_veredictos(items, datos):
    """Cruza lo juzgado con lo pedido: cada url de entrada tiene EXACTAMENTE
    un veredicto (lo que el juez calló se etiqueta desconocida, P3)."""
    juzgados = {}
    crudo = datos.get("veredictos") if isinstance(datos, dict) else None
    for v in crudo if isinstance(crudo, list) else []:
        if isinstance(v, dict) and v.get("url"):
            juzgados[str(v["url"]).strip()] = v
    veredictos = []
    for it in items:
        u = it["url"]
        v = juzgados.get(u) or {}
        banda = str(v.get("banda") or "").strip().lower()
        if banda not in BANDAS:
            banda = "desconocida"
        razones = [str(z) for z in (v.get("razones") or []) if str(z).strip()][:4]
        if not razones:
            razones = ["el juez no se pronunció: desconocida no significa excluida (P3)"]
        veredictos.append({"url": u, "banda": banda, "razones": razones})
    return veredictos


def juzgar_con(nombre, base_url, api_key, model, items):
    """Juzga UN lote con UN motor concreto. Devuelve
    ``(veredictos, motor_id)`` con ``motor_id`` trazable (T13)."""
    lineas = [
        f"{n + 1}. {it['url']} — {it.get('titulo', '')} [{it.get('fuente', '')}] "
        f"{(it.get('resumen') or '')[:200]}".strip()
        for n, it in enumerate(items)
    ]
    usuario = (
        f"Juzga estas {len(items)} fuentes (una entrada de veredicto por cada una):\n"
        + "\n".join(lineas)
    )
    _throttle()
    texto = _chat_completions(base_url, api_key, model, RUBRICA_SISTEMA, usuario)
    return _normaliza_veredictos(items, _extrae_json(texto)), f"{nombre}:{model}"


def _candidatos():
    """Motores en orden de preferencia (P2: local primero)."""
    motores = []
    if os.environ.get("LOCAL_ORACLE_ENABLED", "true").lower() != "false":
        motores.append(
            (
                "jan",
                os.environ.get("LOCAL_ORACLE_BASE_URL", "http://localhost:1337/v1"),
                None,
                os.environ.get("LOCAL_ORACLE_MODEL", "Qwen3-8B-Q4_K_M"),
            )
        )
    clave = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if clave:
        motores.append(
            (
                "openrouter",
                "https://openrouter.ai/api/v1",
                clave,
                os.environ.get("BUSCADOR_OPENROUTER_MODEL", "deepseek/deepseek-r1:free"),
            )
        )
    return motores


def juzgar_lote(items):
    """Juzga un lote (~10 urls) con el primer motor que responda. Devuelve
    ``(veredictos, motor_id)``. Levanta ``SinJuez`` si no hay motores o todos
    fallan — el buscador sigue con Nivel 1 (fail-open total)."""
    items = list(items or [])
    if not items:
        return [], "ninguno"
    motores = _candidatos()
    if not motores:
        raise SinJuez("sin juez configurado (ni hub local ni OPENROUTER_API_KEY)")
    fallos = []
    for nombre, base, clave, modelo in motores:
        try:
            return juzgar_con(nombre, base, clave, modelo, items)
        except Exception as exc:  # el siguiente motor lo intenta
            fallos.append(f"{nombre}: {exc}")
    raise SinJuez("jueces agotados: " + " | ".join(fallos))
