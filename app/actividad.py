# -*- coding: utf-8 -*-
"""Actividad de la plataforma en lenguaje natural (terminal).

Por defecto imprime una línea por acción relevante: quién (alias, nunca el
correo completo), qué hizo, cómo salió y cuánto tardó. Se silencia con
``LOG_HUMANO=0`` (o false/no/off). Nunca registra cuerpos, tokens ni
cabeceras: el password y los JWT no tienen forma de llegar a la salida.

Cada ``LOG_METRICAS_CADA`` peticiones (default 100; 0 lo apaga) imprime un
resumen de métricas: totales por clase de estado, acciones más frecuentes y
latencia media. Si ``LOG_JSON=1`` está activo, el logging JSON sigue siendo
el canal estructurado; este logger humano es independiente y sanitizado.
"""

from __future__ import annotations

import logging
import os
import sys
import threading
import time
from collections import Counter

from flask import Flask, request

from .logging_config import SanitizingFilter, redact_text

log = logging.getLogger("maxocracia.actividad")
_HANDLER_MARCA = "_maxocracia_actividad_handler"

# Rutas que no se narran (assets, health del borde).
_RUTAS_SILENCIOSAS = ("/static/", "/_next/", "/favicon.ico", "/cdn-cgi/")

# endpoint -> acción en lenguaje natural
_ACCIONES = {
    "auth.login": "inició sesión",
    "auth.register": "llegó como cuenta nueva",
    "auth.logout": "cerró sesión",
    "auth.me": "pidió su perfil",
    "auth.refresh": "renovó su sesión",
    "catch_all": "abrió una página",
    "users.list_users": "consultó el directorio",
    "users.get_user": "miró un perfil",
    "maxo.balance": "miró su saldo Maxo",
    "maxo.ledger": "revisó su libro de Maxo",
    "maxo.transfer": "transfirió Maxo",
    "interchanges.create_interchange": "registró un intercambio",
    "interchanges.list_interchanges": "revisó sus intercambios",
    "reputation.add_review": "dejó una reseña",
    "reputation.get_reputation": "miró una reputación",
    "resources.create_resource": "ofreció un recurso",
    "resources.claim_resource": "reclamó un recurso",
    "resources.list_resources": "miró los recursos disponibles",
    "forms.register_participant": "se registró en la Red de Apoyo",
    "forms.register_exchange": "registró un intercambio de la Red",
    "forms.register_followup": "reportó un seguimiento",
    "forms.oracle_chat": "habló con el oráculo",
    "forms.get_participants": "consultó la Red de Apoyo",
    "forms.get_cohort_pulse": "miró el pulso de la cohorte",
    "vhv.calculate": "calculó un VHV",
    "vhv.get_products": "exploró productos con VHV",
    "vhv.get_product": "miró un producto",
    "vhv.get_parameters": "consultó los parámetros del VHV",
    "vhv.update_parameters": "ajustó parámetros del VHV",
    "tvi.log_tvi": "registró su tiempo vital",
    "tvi.get_tvis": "revisó su tiempo vital",
    "tvi.get_community_stats": "miró el tiempo vital de la comunidad",
    "contracts.create_contract": "creó un contrato",
    "contracts.list_contracts": "revisó contratos",
    "contracts.get_contract": "abrió un contrato",
    "contracts.add_term": "añadió un término",
    "contracts.add_participant": "sumó una parte al contrato",
    "contracts.accept_term": "aceptó un término",
    "contracts.witness_contract": "atestiguó un contrato",
    "contracts.contract_checkin": "hizo check-in de un contrato",
    "contracts.report_fulfillment": "reportó cumplimiento",
    "contracts.appeal_fulfillment": "apeló un cumplimiento",
    "contracts.finalize_contract": "finalizó un contrato",
    "contracts.activate_contract": "activó un contrato",
    "contracts.request_retraction": "pidió retractarse",
    "contracts.negotiate_with_oracle": "negoció un contrato con el oráculo",
    "contracts.negotiate_oracle_feedback": "iteró la negociación",
    "contracts.record_nps": "dejó su evaluación (NPS)",
    "contracts.cohort_overview": "miró el panorama de la cohorte",
    "bridge_b.contract_from_need": "tejió un contrato desde una necesidad",
    "bridge_b.cycle_step": "avanzó el ciclo de un contrato",
    "parties.create_party": "inscribió una parte",
    "parties.list_all_parties": "miró el registro de partes",
    "parties.update_party": "actualizó una parte",
    "parties.governance_change": "cambió la gobernanza de una parte",
    "protection.my_profile": "miró su perfil de protección",
    "protection.update_my_profile": "actualizó su protección",
    "voting.create_proposal": "abrió una propuesta",
    "voting.cast_vote": "votó",
    "voting.close_proposal": "cerró una propuesta",
    "voting.analyze_proposal": "pidió análisis del oráculo",
    "voting.set_delegation": "delegó su voto",
    "voting.revoke_delegation": "recuperó su voto",
    "voting.propose_params": "propuso ajustar parámetros",
    "voting.propose_edu_umbral": "propuso el umbral educativo",
    "voting.voting_stats": "miró las votaciones",
    "voting.list_proposals": "leyó las propuestas",
    "voting.get_proposal": "leyó una propuesta",
    "guide.guide_chat": "consultó al guía",
    "guide.trust_assessment": "pidió evaluación de confianza",
    "guide.director_candidacy": "presentó candidatura a director",
    "micromax.create_household": "creó un hogar",
    "micromax.join_household": "se unió a un hogar",
    "micromax.get_household": "miró su hogar",
    "micromax.log_checkin": "registró un latido del hogar",
    "micromax.log_cdd": "registró un aporte de casa",
    "micromax.save_safety_survey": "respondió la encuesta de seguridad",
    "micromax.log_audit": "hizo una auditoría del hogar",
    "micromax.get_dashboard": "miró el bienestar de su hogar",
    "micromax.get_support_offers": "miró ofertas de la Red",
    "forum.create_post": "escribió en la plaza",
    "forum.add_reply": "respondió en la plaza",
    "forum.close_post": "cerró un hilo de la plaza",
    "forum.list_posts": "leyó la plaza",
    "forum.get_post": "abrió un hilo",
    "workshops.create_workshop": "abrió un taller",
    "workshops.enroll_workshop": "se inscribió en un taller",
    "workshops.add_output": "entregó un trabajo de taller",
    "workshops.grant_skill": "reconoció una habilidad",
    "workshops.close_workshop": "cerró un taller",
    "groups.create_group": "creó un grupo",
    "groups.join_group": "se unió a un grupo",
    "groups.register_child": "registró un hijo en el grupo",
    "groups.close_group": "cerró un grupo",
    "arrivals.invite": "abrió una invitación",
    "edu_bridge.status": "consultó el puente educativo",
    "edu_bridge.sync_mastery": "sincronizó una maestría",
    "verifier.verify_contract": "verificó un contrato en la plaza pública",
    "verifier.cohort_public": "miró la plaza pública",
    "verifier.oracle_ledger_public": "auditó el sustento del oráculo",
    "stripe.create_checkout_session": "empezó una contribución",
    "stripe.create_customer_portal": "abrió su portal de pagos",
    "stripe.stripe_webhook": "recibió un aviso de pago",
    "subscriptions.activate_manual": "activó una suscripción a mano",
    "subscriptions.register_crypto": "registró un pago cripto",
    "subscriptions.get_my_subscription": "miró su suscripción",
    "synthetic_sessions.create_session": "convocó una sesión sintética",
    "synthetic_sessions.run_session": "corrió una sesión sintética",
    "synthetic_sessions.review_session": "revisó una sesión sintética",
    "synthetic_sessions.revoke_session": "revocó una sesión sintética",
}

_metricas_lock = threading.Lock()
_metricas = {
    "total": 0,
    "ok": 0,
    "aviso": 0,
    "error": 0,
    "ms": 0.0,
    "ms_ventana": 0.0,
    "acciones_ventana": Counter(),
}


def _env_flag(nombre, default):
    valor = os.environ.get(nombre)
    if valor is None:
        return default
    return valor.strip().lower() not in ("0", "false", "no", "off", "")


def _default_activo(app) -> bool:
    """ON por defecto en la plataforma; OFF en tests salvo LOG_HUMANO=1."""
    if os.environ.get("PYTEST_CURRENT_TEST"):
        return False
    if os.environ.get("FLASK_ENV") == "testing":
        return False
    return not app.config.get("TESTING", False)


def _metricas_cada():
    try:
        return max(0, int(os.environ.get("LOG_METRICAS_CADA", "100")))
    except (TypeError, ValueError):
        return 100


class _StdoutActual(logging.StreamHandler):
    """Handler que re-apunta a sys.stdout en cada emisión (tests, reloader) y
    sobrevive a consolas cp1252: nunca revienta por un carácter."""

    def emit(self, record):
        self.stream = sys.stdout
        try:
            super().emit(record)
        except UnicodeEncodeError:
            msg = self.format(record)
            encoding = getattr(self.stream, "encoding", None) or "utf-8"
            safe = msg.encode(encoding, "replace").decode(encoding, "replace")
            self.stream.write(safe + self.terminator)


def _instalar_handler():
    if getattr(log, _HANDLER_MARCA, False):
        return
    handler = _StdoutActual()
    handler.setFormatter(
        logging.Formatter("[%(asctime)s] %(message)s", datefmt="%H:%M:%S")
    )
    handler.addFilter(SanitizingFilter())
    log.addHandler(handler)
    log.setLevel(logging.INFO)
    log.propagate = False
    setattr(log, _HANDLER_MARCA, True)


def correo_enmascarado(email):
    """a***@dominio: la identidad se ve, el correo completo no se registra."""
    local, _, dominio = str(email or "").partition("@")
    if not local:
        return "alguien"
    return f"{local[0]}***@{dominio or 'correo'}"


def actor():
    """Quién actuó: alias/nombre si el token lo trae; si no, correo enmascarado."""
    datos = getattr(request, "user", None)
    if not isinstance(datos, dict):
        datos = {}
    alias = datos.get("alias") or datos.get("name")
    if alias:
        return str(alias).strip()[:40]
    if datos.get("email"):
        return correo_enmascarado(datos["email"])
    uid = datos.get("user_id")
    if uid:
        return f"usuario #{uid}"
    return "un visitante"


def describir(endpoint, metodo, ruta):
    accion = _ACCIONES.get(endpoint or "")
    return accion or f"{metodo} {ruta}"


def _resultado(status):
    if status >= 500:
        return "algo falló"
    if status == 401:
        return "sin sesión válida"
    if status == 403:
        return "sin permiso"
    if status == 429:
        return "frenado por el límite"
    if status >= 400:
        return "no salió"
    return "salió bien"


def reiniciar_metricas():
    """Limpia contadores (tests y arranques limpios)."""
    with _metricas_lock:
        _metricas.update(
            {
                "total": 0,
                "ok": 0,
                "aviso": 0,
                "error": 0,
                "ms": 0.0,
                "ms_ventana": 0.0,
                "acciones_ventana": Counter(),
            }
        )


def resumen_metricas():
    """Emite (y devuelve) la línea de resumen de la ventana actual."""
    with _metricas_lock:
        total = _metricas["total"]
        if total == 0:
            return ""
        top = _metricas["acciones_ventana"].most_common(3)
        promedio = _metricas["ms"] / total
        linea = (
            f"[métricas] {total} acciones · {_metricas['ok']} bien · "
            f"{_metricas['aviso']} con aviso · {_metricas['error']} fallos · "
            f"{promedio:.0f} ms promedio"
        )
        if top:
            favoritas = ", ".join(f"{_ACCIONES.get(e, e)} ({n})" for e, n in top)
            linea += f" · más frecuentes: {favoritas}"
        _metricas["ms_ventana"] = 0.0
        _metricas["acciones_ventana"] = Counter()
    log.info(redact_text(linea))
    return linea


def _acumular(status, ms, endpoint):
    with _metricas_lock:
        _metricas["total"] += 1
        _metricas["ms"] += ms
        if status >= 500:
            _metricas["error"] += 1
        elif status >= 400:
            _metricas["aviso"] += 1
        else:
            _metricas["ok"] += 1
        _metricas["acciones_ventana"][endpoint or "?"] += 1
        total = _metricas["total"]
    cada = _metricas_cada()
    if cada and total % cada == 0:
        resumen_metricas()


def init_actividad(app: Flask) -> None:
    """Registra el narrador humano si LOG_HUMANO está activo (default: sí)."""
    activo = _env_flag("LOG_HUMANO", _default_activo(app))
    if not activo:
        return

    _instalar_handler()
    log.info(
        "[actividad] Narrando la plataforma en la terminal · "
        "silenciar con LOG_HUMANO=0"
    )

    @app.before_request
    def _marcar_inicio():
        request.environ["maxo_act_t0"] = time.perf_counter()

    @app.after_request
    def _narrar(response):
        ruta = request.path or "/"
        if any(ruta.startswith(prefijo) for prefijo in _RUTAS_SILENCIOSAS):
            return response

        t0 = request.environ.get("maxo_act_t0")
        ms = (time.perf_counter() - t0) * 1000.0 if t0 else 0.0
        endpoint = request.endpoint or ""
        frase = describir(endpoint, request.method, ruta)
        resultado = _resultado(response.status_code)
        sufijo = f" · {response.status_code}" if response.status_code >= 400 else ""
        linea = f"{actor()} · {frase} · {resultado}{sufijo} ({ms:.0f} ms)"
        log.info(redact_text(linea))
        _acumular(response.status_code, ms, endpoint)
        return response
