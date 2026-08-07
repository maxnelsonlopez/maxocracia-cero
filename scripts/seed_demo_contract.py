"""
Seed del contrato demo de la Cohorte Cero
==========================================
Crea un MaxoContract REAL y completo para visualizar el flujo de principio a fin:

    "Max ofrece 10 horas de trabajo y la contraparte ofrece a cambio
     un objeto, 10 horas de trabajo o un servicio."

Incluye:
- 4 co-firmantes (Max + Ana + Luis + Caro) con sus cuentas reales.
- Cada bloque/término vinculado a la parte obligada (assigned_participant).
- Costos VHV (Tiempo) y protección SDV vía validación axiomática.

Uso:
    python scripts/seed_demo_contract.py

Los usuarios demo se crean si no existen (con contraseña 'Demo12345!').
"""

import base64
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("SECRET_KEY", "dev-fallback-key-12345")

from app import create_app


def _user_id_from_token(token):
    """Extrae el user_id del payload del JWT (sin verificar firma: el token
    acaba de ser emitido por el propio servidor)."""
    try:
        payload = token.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        return json.loads(base64.urlsafe_b64decode(payload))["user_id"]
    except Exception:
        return None

CONTRACT_ID = "demo-intercambio-10h"

DEMO_USERS = [
    {"email": "max@demo.maxocracia.org", "password": "Demo12345!", "name": "Max"},
    {"email": "ana@demo.maxocracia.org", "password": "Demo12345!", "name": "Ana"},
    {"email": "luis@demo.maxocracia.org", "password": "Demo12345!", "name": "Luis"},
    {"email": "caro@demo.maxocracia.org", "password": "Demo12345!", "name": "Caro"},
]

TERMS = [
    {
        "term_id": "trabajo-10h",
        "civil_text": "Max ofrece 10 horas de trabajo",
        "vhv": {"t": 10.0, "v": 0, "h": 0},
        "assigned_participant_id": None,  # se asigna tras conocer el id de Max
    },
    {
        "term_id": "reciprocidad",
        "civil_text": "Ana ofrece a cambio: un objeto, 10 horas de trabajo o un servicio, a convenir",
        "vhv": {"t": 2.0, "v": 0, "h": 0},
        "assigned_participant_id": None,  # se asigna tras conocer el id de Ana
    },
    {
        "term_id": "aval-luis",
        "civil_text": "Luis avala la simetría del intercambio (Axioma T9)",
        "vhv": {"t": 0.5, "v": 0, "h": 0},
        "assigned_participant_id": None,
    },
    {
        "term_id": "aval-caro",
        "civil_text": "Caro acompaña como testigo de coherencia vital",
        "vhv": {"t": 0.5, "v": 0, "h": 0},
        "assigned_participant_id": None,
    },
]


def main():
    app = create_app()
    # El seed hace varios logins consecutivos; en modo TESTING el rate
    # limiter sube a 100/min (en producción el login es 3/min).
    app.config["TESTING"] = True

    with app.test_client() as client:
        user_ids = {}

        for u in DEMO_USERS:
            res = client.post("/auth/register", json=u)
            if res.status_code == 201:
                data = res.get_json()
                user_ids[u["name"]] = _user_id_from_token(data["access_token"])
            else:
                # Ya existe: obtener token para leer su id
                login = client.post("/auth/login", json={"email": u["email"], "password": u["password"]})
                if login.status_code == 200:
                    token = login.get_json()["access_token"]
                    user_ids[u["name"]] = _user_id_from_token(token)
                if u["name"] not in user_ids or user_ids[u["name"]] is None:
                    print(f"  ! No se pudo resolver la cuenta de {u['name']}")

        if not all(user_ids.values()):
            print("ERROR: No se pudieron crear los usuarios demo.")
            sys.exit(1)

        # Eliminar contrato previo si existe
        with app.app_context():
            from app.utils import get_db
            db = get_db()
            db.execute("DELETE FROM maxo_contracts WHERE contract_id = ?", (CONTRACT_ID,))
            db.commit()

        # Token del creador (Max)
        login = client.post("/auth/login", json={"email": DEMO_USERS[0]["email"], "password": DEMO_USERS[0]["password"]})
        token = login.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Asignar las partes a los términos
        for t in TERMS:
            if t["term_id"] == "trabajo-10h":
                t["assigned_participant_id"] = f"user-{user_ids['Max']}"
            elif t["term_id"] == "reciprocidad":
                t["assigned_participant_id"] = f"user-{user_ids['Ana']}"
            elif t["term_id"] == "aval-luis":
                t["assigned_participant_id"] = f"user-{user_ids['Luis']}"
            elif t["term_id"] == "aval-caro":
                t["assigned_participant_id"] = f"user-{user_ids['Caro']}"

        res = client.post("/contracts/", headers=headers, json={
            "contract_id": CONTRACT_ID,
            "civil_description": (
                "Intercambio ético: Max ofrece 10 horas de trabajo; "
                "Ana ofrece a cambio un objeto, 10 horas de trabajo o un servicio."
            ),
            # Blindaje (Ola 3A): el demo es asimétrico (10h vs 3h) y declara
            # la asimetría explícitamente; sin reflexión forzada para demo.
            "min_reflection_hours": 0,
            "participants": [
                {"user_id": user_ids["Max"], "wellness": 1.0},
                {"user_id": user_ids["Ana"], "wellness": 1.0},
                {"user_id": user_ids["Luis"], "wellness": 1.0},
                {"user_id": user_ids["Caro"], "wellness": 1.0},
            ],
            "terms": TERMS,
        })

        if res.status_code != 201:
            print(f"ERROR al crear el contrato: {res.status_code} {res.get_json()}")
            sys.exit(1)

        # Reconocimiento explícito de la asimetría (Ola 3A.4, T9 ejecutable):
        # cada parte obligada (y el aval) firma la asimetría con su token.
        for u in DEMO_USERS:
            login = client.post("/auth/login", json={"email": u["email"], "password": u["password"]})
            uid = user_ids[u["name"]]
            ack = client.post(
                f"/contracts/{CONTRACT_ID}/acknowledge-asymmetry",
                headers={"Authorization": f"Bearer {login.get_json()['access_token']}"},
                json={"party_id": f"user-{uid}"},
            )
            if ack.status_code != 200:
                print(f"  ! {u['name']}: no pudo reconocer la asimetría ({ack.status_code})")

        print("=" * 60)
        print(f"OK: Contrato demo creado: {CONTRACT_ID}")
        print("=" * 60)
        print("Participantes (co-firmantes):")
        for name, uid in user_ids.items():
            print(f"   - {name} (user-{uid})")
        print("\nTérminos y partes obligadas:")
        for t in TERMS:
            print(f"   - {t['civil_text']}")
            print(f"     -> Obligada: {t['assigned_participant_id']} · T={t['vhv']['t']}h")
        print("\nAbre en el navegador:")
        print("   http://127.0.0.1:5001/contracts/demo-intercambio-10h")
        print("   (Panel Visual | Documento Legal — firma como cada co-firmante)")


if __name__ == "__main__":
    main()
