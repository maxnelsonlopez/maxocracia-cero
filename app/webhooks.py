import json
import threading
import requests
import hmac
import hashlib
from typing import Dict, Any

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

def dispatch_event(event_type: str, payload: Dict[Any, Any]):
    """
    Despacha un evento a todos los webhooks registrados que estén escuchando.
    Ejecuta el envío de forma asíncrona usando threads.
    """
    try:
        # get_db solo es seguro dentro del contexto de aplicación/request
        from .utils import get_db
        db = get_db()
        rows = db.execute("SELECT url, secret, events FROM maxo_webhooks WHERE is_active = 1").fetchall()
        
        for row in rows:
            try:
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
