# -*- coding: utf-8 -*-
"""Tests de Talleres de Aprendizaje (M3 — rama educativa).

Cubren: creación del taller (5-12), inscripción y cupos, obras de salida,
y la concesión de skill por la regla de oro (motor) + triada (mentor/par/
oráculo con veto); permisos del facilitador.
"""


def _login_as(client, email):
    resp = client.post(
        "/auth/login", json={"email": email, "password": "ValidPass123!"}
    )
    return {"Authorization": f"Bearer {resp.get_json()['access_token']}"}


def _create_workshop(client, headers=None, **overrides):
    payload = {
        "title": "Taller de huertas",
        "skill_node": "naturaleza/huertas",
        "description": "Aprender a cultivar con la comunidad.",
        "capacity": 8,
        **overrides,
    }
    return client.post("/workshops", json=payload, headers=headers or {})


def test_requires_token(client):
    assert client.get("/workshops").status_code == 401
    assert client.post("/workshops", json={}).status_code == 401


def test_create_workshop_ok(auth_client):
    resp = _create_workshop(auth_client)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["workshop"]["title"] == "Taller de huertas"
    assert data["workshop"]["capacity"] == 8
    assert data["workshop"]["status"] == "open"
    assert data["workshop"]["facilitator"]["name"] == "Test User"
    assert data["workshop"]["enrolled_count"] == 0


def test_create_workshop_capacity_bounds(auth_client):
    resp = _create_workshop(auth_client, capacity=4)
    assert resp.status_code == 400
    resp = _create_workshop(auth_client, capacity=13)
    assert resp.status_code == 400
    resp = _create_workshop(auth_client, capacity=5)
    assert resp.status_code == 201
    resp = _create_workshop(auth_client, capacity=12)
    assert resp.status_code == 201


def test_create_workshop_missing_fields(auth_client):
    resp = auth_client.post(
        "/workshops",
        json={"skill_node": "x", "capacity": 8},
    )
    assert resp.status_code == 400  # falta title
    resp = auth_client.post(
        "/workshops",
        json={"title": "x", "capacity": 8},
    )
    assert resp.status_code == 400  # falta skill_node


def test_create_workshop_validates_node_id(auth_client):
    """skill_node debe ser un nodo del árbol (rama o rama/nodo) — M6."""
    resp = _create_workshop(auth_client, skill_node="no vale / tres / partes")
    assert resp.status_code == 400
    resp = _create_workshop(auth_client, skill_node="")
    assert resp.status_code == 400
    # Nodo canónico válido (rama + slash es el formato del tejido).
    resp = _create_workshop(auth_client, skill_node="naturaleza/huertas")
    assert resp.status_code == 201
    # Fork con rama nueva también siembra el tejido (formato válido).
    resp = _create_workshop(auth_client, skill_node="gastronomia/fermentos")
    assert resp.status_code == 201


def test_enroll_workshop(auth_client):
    created = _create_workshop(auth_client)
    workshop_id = created.get_json()["workshop"]["id"]

    headers2 = _login_as(auth_client, "test2@example.com")
    resp = auth_client.post(f"/workshops/{workshop_id}/enroll", headers=headers2)
    assert resp.status_code == 200

    # Duplicado -> 409
    resp2 = auth_client.post(f"/workshops/{workshop_id}/enroll", headers=headers2)
    assert resp2.status_code == 409

    # El facilitador no puede inscribirse en su propio taller
    resp3 = auth_client.post(f"/workshops/{workshop_id}/enroll")
    assert resp3.status_code == 400


def test_enroll_full_workshop(auth_client):
    created = _create_workshop(auth_client, capacity=5)
    workshop_id = created.get_json()["workshop"]["id"]
    # Enrolar 4 usuarios distintos (test2, admin + 2 nuevos) hasta el cupo 5.
    from werkzeug.security import generate_password_hash

    with auth_client.application.app_context():
        from app.utils import get_db

        db = get_db()
        existing = db.execute(
            "SELECT id FROM users WHERE email != 'test@example.com' LIMIT 2"
        ).fetchall()
        for i in range(2):
            db.execute(
                "INSERT INTO users (email, name, is_admin, password_hash) VALUES (?, ?, 0, ?)",
                (f"fill{i}@example.com", f"Fill {i}", generate_password_hash("ValidPass123!")),
            )
        # Además de test2 y admin, 3 nuevos llenan el cupo 5.
        db.execute(
            "INSERT INTO users (email, name, is_admin, password_hash) VALUES (?, ?, 0, ?)",
            ("fill2@example.com", "Fill 2", generate_password_hash("ValidPass123!")),
        )
        # El intentante (fill3) existe pero queda afuera por cupo.
        db.execute(
            "INSERT INTO users (email, name, is_admin, password_hash) VALUES (?, ?, 0, ?)",
            ("fill3@example.com", "Fill 3", generate_password_hash("ValidPass123!")),
        )
        new_users = db.execute(
            "SELECT id FROM users WHERE email LIKE 'fill%@example.com' ORDER BY id"
        ).fetchall()
        targets = [u["id"] for u in existing] + [u["id"] for u in new_users[:3]]
        for uid in targets:
            db.execute(
                "INSERT INTO workshop_enrollments (workshop_id, user_id) VALUES (?, ?)",
                (workshop_id, uid),
            )
        db.commit()

    headers_full = _login_as(auth_client, "fill3@example.com")
    resp = auth_client.post(f"/workshops/{workshop_id}/enroll", headers=headers_full)
    assert resp.status_code == 409  # cupo lleno


def test_enroll_requires_open_status(auth_client):
    created = _create_workshop(auth_client)
    workshop_id = created.get_json()["workshop"]["id"]
    auth_client.post(f"/workshops/{workshop_id}/close")
    headers2 = _login_as(auth_client, "test2@example.com")
    resp = auth_client.post(f"/workshops/{workshop_id}/enroll", headers=headers2)
    assert resp.status_code == 400


def test_outputs_require_enrollment(auth_client):
    created = _create_workshop(auth_client)
    workshop_id = created.get_json()["workshop"]["id"]
    headers2 = _login_as(auth_client, "test2@example.com")
    resp = auth_client.post(
        f"/workshops/{workshop_id}/outputs",
        json={"kind": "material", "title": "Guía de compostaje"},
        headers=headers2,
    )
    assert resp.status_code == 403  # no inscrito

    resp2 = auth_client.post(
        f"/workshops/{workshop_id}/outputs",
        json={"kind": "material", "title": "Guía del facilitador"},
    )
    assert resp2.status_code == 201  # el facilitador sí puede


def test_grant_skill_full_flow(auth_client):
    """Regla de oro + triada: el aprendiz vacua al cumplir todo."""
    created = _create_workshop(auth_client)
    workshop_id = created.get_json()["workshop"]["id"]

    headers2 = _login_as(auth_client, "test2@example.com")
    auth_client.post(f"/workshops/{workshop_id}/enroll", headers=headers2)

    # El aprendiz publica obra y material.
    auth_client.post(
        f"/workshops/{workshop_id}/outputs",
        json={"kind": "obra", "title": "Huerta comunitaria sembrada"},
        headers=headers2,
    )
    auth_client.post(
        f"/workshops/{workshop_id}/outputs",
        json={"kind": "material", "title": "Cuaderno abierto de la huerta"},
        headers=headers2,
    )

    # Triada: facilitador (autor) firma mentor + par; sin veto de oráculo.
    with auth_client.application.app_context():
        from app.utils import get_db

        db = get_db()
        target = db.execute(
            "SELECT id FROM users WHERE email = 'test2@example.com'"
        ).fetchone()
        target_user_id = target["id"]

    resp = auth_client.post(
        f"/workshops/{workshop_id}/grant-skill",
        json={
            "user_id": target_user_id,
            "mentor_ok": True,
            "peer_ok": True,
            "oracle_veto": False,
            "mentoria_horas": 2.5,
        },
    )
    assert resp.status_code == 200
    award = resp.get_json()["award"]
    assert award["outcome"] == "awarded"
    assert award["skill_node"] == "naturaleza/huertas"
    assert award["vacua_faltantes"] == []
    assert award["triada_bloqueos"] == []


def test_grant_skill_violates_golden_rule(auth_client):
    """Sin obra ni material: la regla de oro rechaza (nada de títulos vacíos)."""
    created = _create_workshop(auth_client)
    workshop_id = created.get_json()["workshop"]["id"]
    headers2 = _login_as(auth_client, "test2@example.com")
    auth_client.post(f"/workshops/{workshop_id}/enroll", headers=headers2)

    with auth_client.application.app_context():
        from app.utils import get_db

        db = get_db()
        target_user_id = db.execute(
            "SELECT id FROM users WHERE email = 'test2@example.com'"
        ).fetchone()["id"]

    resp = auth_client.post(
        f"/workshops/{workshop_id}/grant-skill",
        json={
            "user_id": target_user_id,
            "mentor_ok": True,
            "peer_ok": True,
            "oracle_veto": False,
            "mentoria_horas": 0.0,
        },
    )
    assert resp.status_code == 200
    award = resp.get_json()["award"]
    assert award["outcome"] == "rejected"
    assert {"obra aplicada", "material de enseñanza publicado", "mentoría mínima (1 h de TVI)"} <= set(
        award["vacua_faltantes"]
    )


def test_grant_skill_awaiting_with_veto(auth_client):
    """El oráculo con veto deja la concesión en espera (no la anula solo)."""
    created = _create_workshop(auth_client)
    workshop_id = created.get_json()["workshop"]["id"]
    headers2 = _login_as(auth_client, "test2@example.com")
    auth_client.post(f"/workshops/{workshop_id}/enroll", headers=headers2)
    auth_client.post(
        f"/workshops/{workshop_id}/outputs",
        json={"kind": "obra", "title": "Obra X"},
        headers=headers2,
    )
    auth_client.post(
        f"/workshops/{workshop_id}/outputs",
        json={"kind": "material", "title": "Material X"},
        headers=headers2,
    )
    with auth_client.application.app_context():
        from app.utils import get_db

        db = get_db()
        target_user_id = db.execute(
            "SELECT id FROM users WHERE email = 'test2@example.com'"
        ).fetchone()["id"]

    resp = auth_client.post(
        f"/workshops/{workshop_id}/grant-skill",
        json={
            "user_id": target_user_id,
            "mentor_ok": True,
            "peer_ok": True,
            "oracle_veto": True,
            "mentoria_horas": 2.0,
        },
    )
    assert resp.status_code == 200
    assert resp.get_json()["award"]["outcome"] == "awaiting_triada"
    assert resp.get_json()["award"]["triada_bloqueos"] == [
        "el oráculo ejerció el veto (axiomas en riesgo)"
    ]


def test_grant_skill_only_facilitator(auth_client):
    created = _create_workshop(auth_client)
    workshop_id = created.get_json()["workshop"]["id"]
    headers2 = _login_as(auth_client, "test2@example.com")
    auth_client.post(f"/workshops/{workshop_id}/enroll", headers=headers2)

    # Test User 2 intenta conceder (no facilita) -> 403.
    resp = auth_client.post(
        f"/workshops/{workshop_id}/grant-skill",
        json={"user_id": 1, "mentor_ok": True, "peer_ok": True},
        headers=headers2,
    )
    assert resp.status_code == 403


def test_grant_skill_requires_enrolled_target(auth_client):
    created = _create_workshop(auth_client)
    workshop_id = created.get_json()["workshop"]["id"]
    with auth_client.application.app_context():
        from app.utils import get_db

        db = get_db()
        # Admin existe en la BD pero no está inscrito.
        target_user_id = db.execute(
            "SELECT id FROM users WHERE email = 'admin@example.com'"
        ).fetchone()["id"]
    resp = auth_client.post(
        f"/workshops/{workshop_id}/grant-skill",
        json={"user_id": target_user_id, "mentor_ok": True, "peer_ok": True},
    )
    assert resp.status_code == 400


def test_list_workshops(auth_client):
    _create_workshop(auth_client, title="Uno")
    _create_workshop(auth_client, title="Dos")
    resp = auth_client.get("/workshops")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["count"] == 2
    assert data["workshops"][0]["title"] == "Dos"


def test_close_workshop_by_facilitator(auth_client):
    created = _create_workshop(auth_client)
    workshop_id = created.get_json()["workshop"]["id"]
    headers2 = _login_as(auth_client, "test2@example.com")
    resp = auth_client.post(f"/workshops/{workshop_id}/close", headers=headers2)
    assert resp.status_code == 403
    resp = auth_client.post(f"/workshops/{workshop_id}/close")
    assert resp.status_code == 200
    assert resp.get_json()["workshop"]["status"] == "closed"
