"""
Seed del demo interescala de la Cohorte Cero (ROADMAP Bloque B + extensiones)
================================================================================
Crea un MaxoContract REAL entre una COOPERATIVA y una INSTITUCIÓN:

    "La Coop Semilla del Valle ofrece cuidado comunitario (12h/semana);
     la Escuela Aurora ofrece a cambio el salón de usos múltiples
     y la huerta escolar para la comunidad."

Incluye:
- Cooperativa con 3 delegados (Max, Ana, Luis), votación ponderada
  (Max pesa 2) y quórum de 0.5 del peso total.
- Institución (Escuela Aurora) con 2 delegados y quórum de unanimidad.
- Contrato coop <-> org con términos vinculados a cada parte obligada.

Uso:
    python scripts/seed_demo_scales.py

Los usuarios demo se crean si no existen (con contraseña 'Demo12345!').
Idempotente: recrea las partes y el contrato si ya existen.
"""

import base64
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("SECRET_KEY", "dev-fallback-key-12345")

from app import create_app

CONTRACT_ID = "demo-escalas-coop-org"
COOP_ID = "coop-semilla"
ORG_ID = "org-aurora"

DEMO_USERS = [
    {"email": "max@demo.maxocracia.org", "password": "Demo12345!", "name": "Max"},
    {"email": "ana@demo.maxocracia.org", "password": "Demo12345!", "name": "Ana"},
    {"email": "luis@demo.maxocracia.org", "password": "Demo12345!", "name": "Luis"},
    {"email": "caro@demo.maxocracia.org", "password": "Demo12345!", "name": "Caro"},
]


def _user_id_from_token(token):
    """Extrae el user_id del payload del JWT (sin verificar firma: el token
    acaba de ser emitido por el propio servidor)."""
    try:
        payload = token.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        return json.loads(base64.urlsafe_b64decode(payload))["user_id"]
    except Exception:
        return None


def main():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        user_ids = {}

        for u in DEMO_USERS:
            res = client.post("/auth/register", json=u)
            if res.status_code == 201:
                data = res.get_json()
                user_ids[u["name"]] = _user_id_from_token(data["access_token"])
            else:
                login = client.post("/auth/login", json={"email": u["email"], "password": u["password"]})
                if login.status_code == 200:
                    token = login.get_json()["access_token"]
                    user_ids[u["name"]] = _user_id_from_token(token)
                if u["name"] not in user_ids or user_ids[u["name"]] is None:
                    print(f"  ! No se pudo resolver la cuenta de {u['name']}")

        if not all(user_ids.values()):
            print("ERROR: No se pudieron crear los usuarios demo.")
            sys.exit(1)

        # Limpiar estado previo (idempotente)
        with app.app_context():
            from app.utils import get_db
            db = get_db()
            db.execute("DELETE FROM maxo_contracts WHERE contract_id = ?", (CONTRACT_ID,))
            db.execute("DELETE FROM maxo_parties WHERE party_id IN (?, ?)", (COOP_ID, ORG_ID))
            db.commit()

        # Token del creador (Max)
        login = client.post("/auth/login", json={"email": DEMO_USERS[0]["email"], "password": DEMO_USERS[0]["password"]})
        token = login.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        max_pid = f"user-{user_ids['Max']}"
        ana_pid = f"user-{user_ids['Ana']}"
        luis_pid = f"user-{user_ids['Luis']}"
        caro_pid = f"user-{user_ids['Caro']}"

        # 1. Cooperativa con votación ponderada y quórum por peso
        res = client.post("/parties/", headers=headers, json={
            "party_id": COOP_ID,
            "party_type": "cooperative",
            "display_name": "Coop Semilla del Valle",
            "members": {
                "delegates": [max_pid, ana_pid, luis_pid],
                "weights": {max_pid: 2, ana_pid: 1, luis_pid: 1},
                "quorum": 0.5,  # mitad del peso total (2 de 4)
                "delegations": {},  # opcional: {ana_pid: max_pid} para delegar
            },
        })
        if res.status_code != 201:
            print(f"ERROR al crear la cooperativa: {res.status_code} {res.get_json()}")
            sys.exit(1)

        # 2. Institución (delegados: Luis y Caro, unanimidad)
        res = client.post("/parties/", headers=headers, json={
            "party_id": ORG_ID,
            "party_type": "institution",
            "display_name": "Escuela Aurora",
            "members": {
                "delegates": [luis_pid, caro_pid],
                "quorum": 1.0,
            },
        })
        if res.status_code != 201:
            print(f"ERROR al crear la institución: {res.status_code} {res.get_json()}")
            sys.exit(1)

        # 3. Contrato interescala coop <-> org
        res = client.post("/contracts/", headers=headers, json={
            "contract_id": CONTRACT_ID,
            "civil_description": (
                "La Coop Semilla del Valle ofrece cuidado comunitario (12 horas/semana); "
                "la Escuela Aurora ofrece a cambio el salón de usos múltiples y la huerta escolar."
            ),
            "participants": [
                {"user_id": user_ids["Max"], "wellness": 1.0},
                {"party_id": COOP_ID},
                {"party_id": ORG_ID},
            ],
            "terms": [
                {
                    "term_id": "cuidado-comunitario",
                    "civil_text": "La cooperativa ofrece 12 horas semanales de cuidado comunitario a las familias de la escuela",
                    "vhv": {"t": 12.0, "v": 0, "h": 0},
                    "assigned_participant_id": COOP_ID,
                },
                {
                    "term_id": "salon-uso-multiple",
                    "civil_text": "La escuela ofrece el salón de usos múltiples los sábados para talleres de la cooperativa",
                    "vhv": {"t": 4.0, "v": 0, "h": 0},
                    "assigned_participant_id": ORG_ID,
                },
                {
                    "term_id": "huerta-escolar",
                    "civil_text": "La escuela cede la huerta escolar para el cultivo comunitario con acompañamiento de la cooperativa",
                    "vhv": {"t": 2.0, "v": 0, "h": 0},
                    "assigned_participant_id": ORG_ID,
                },
            ],
        })
        if res.status_code != 201:
            print(f"ERROR al crear el contrato: {res.status_code} {res.get_json()}")
            sys.exit(1)

        print("=" * 62)
        print("OK: Contrato interescala creado:", CONTRACT_ID)
        print("=" * 62)
        print("Partes:")
        print(f"   - Coop Semilla del Valle ({COOP_ID})")
        print(f"     Delegados: {max_pid} (peso 2), {ana_pid} (1), {luis_pid} (1)")
        print("     Quórum: 0.5 del peso total -> se sella con peso 2 de 4")
        print(f"   - Escuela Aurora ({ORG_ID})")
        print(f"     Delegados: {luis_pid}, {caro_pid} (unanimidad)")
        print("\nPara sellar el contrato en el navegador:")
        print("   1. Abre http://127.0.0.1:5001/contracts/demo-escalas-coop-org")
        print("   2. Firmante 'Coop Semilla': entra como delegado Max y firma (peso 2/4)")
        print("      -> con Ana (o Luis) alcanzas peso 3/4: quórum sellado")
        print("   3. Firmante 'Escuela Aurora': firma como Luis y como Caro (2/2)")
        print("   4. Firmante 'Max' (persona): firma el contrato y actívalo")
        print("   La jerarquía del árbol interescala se ve en la cabecera del detalle.")


if __name__ == "__main__":
    main()
