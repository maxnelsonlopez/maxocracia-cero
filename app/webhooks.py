import json
import threading
import requests
import hmac
import hashlib
from typing import Any, Dict, List, Optional


def webhook_matches_party(party_filter_raw, party_ids: Optional[List[str]]) -> bool:
    """
    Webhooks por parte (Ext. 4): True si el webhook (party_filter JSON, lista
    de party_id) debe recibir eventos de alguna de las party_ids.
    Sin filtro (null/vacío/JSON inválido) -> recibe todos los eventos.
    """
    if not party_filter_raw:
        return True
    try:
        parsed = json.loads(party_filter_raw)
    except (ValueError, TypeError):
        return True
    if not isinstance(parsed, list):
        return True
    if not party_ids:
        return False
    return any(pid in parsed for pid in party_ids)


def _send_webhook_async(url: str, secret: str, event_type: str, payload: Dict[Any, Any]):
    headers = {
        "Content-Type": "application/json",
        "X-Maxo-Event": event_type
    }
    
    body = json.dumps(payload)
    
    # Firmar el payload para que el cliente pueda verificar la autenticidad
    signature = hmac.new(
        secret.encode('utf-8'),
        body.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    headers["X-Maxo-Signature"] = f"sha256={signature}"
    
    try:
        # Timeout corto para no bloquear recursos (aunque está en un thread)
        requests.post(url, data=body, headers=headers, timeout=5)
    except Exception as e:
        # En un sistema en producción real, aquí se implementaría una cola de reintentos
        print(f"[Webhook Error] Fallo al entregar evento {event_type} a {url}: {e}")

def dispatch_event(event_type: str, payload: Dict[Any, Any],
                   party_ids: Optional[List[str]] = None):
    """
    Despacha un evento a todos los webhooks registrados que estén escuchando.
    Ejecuta el envío de forma asíncrona usando threads.

    party_ids: filtra webhooks con party_filter (notificaciones dirigidas,
    Ext. 4). Sin party_filter, el webhook recibe todos los eventos.
    """
    try:
        # get_db solo es seguro dentro del contexto de aplicación/request
        from .utils import get_db
        db = get_db()
        rows = db.execute(
            "SELECT url, secret, events, party_filter FROM maxo_webhooks WHERE is_active = 1"
        ).fetchall()
        
        for row in rows:
            try:
                if not webhook_matches_party(row["party_filter"], party_ids):
                    continue
                events = json.loads(row["events"])
                # Chequear si este webhook escucha este evento o todos ("*")
                if event_type in events or "*" in events:
                    t = threading.Thread(
                        target=_send_webhook_async,
                        args=(row["url"], row["secret"], event_type, payload)
                    )
                    t.daemon = True
                    t.start()
            except Exception as e:
                print(f"[Webhook Error] Fallo al parsear eventos: {e}")
    except Exception as e:
        print(f"[Webhook Error] Fallo al acceder a DB para dispatch: {e}")
