# -*- coding: utf-8 -*-
"""Tests de Grupos de Solución (ECEs) y Células Madre (M4 — rama educativa).

Cubren: creación de ambos tipos (el ECE exige necesidad real), unirse,
la fractalidad (réplica registrada -> la madre gana el nodo facilitación),
permisos del coordinador y cierre.
"""


def _login_as(client, email):
    resp = client.post(
        "/auth/login", json={"email": email, "password": "ValidPass123!"}
    )
    return {"Authorization": f"Bearer {resp.get_json()['access_token']}"}


def test_requires_token(client):
    assert client.get("/groups").status_code == 401
    assert client.post("/groups", json={}).status_code == 401


def test_create_solution_group(auth_client):
    resp = auth_client.post(
        "/groups",
        json={
            "kind": "solution_group",
            "name": "Agua limpia para la vereda",
            "need_title": "No hay agua potable en la vereda",
            "description": "Grupo de solución para llevar agua limpia.",
        },
    )
    assert resp.status_code == 201
    data = resp.get_json()["group"]
    assert data["kind"] == "solution_group"
    assert data["need_title"] == "No hay agua potable en la vereda"
    assert data["member_count"] == 1
    assert data["creator"]["name"] == "Test User"
    assert data["status"] == "active"

    # Detalle: el creador es coordinador.
    detail = auth_client.get(f"/groups/{data['id']}")
    assert detail.status_code == 200
    assert detail.get_json()["group"]["members"][0]["role"] == "coordinator"


def test_solution_group_requires_need(auth_client):
    resp = auth_client.post(
        "/groups",
        json={"kind": "solution_group", "name": "Grupo sin necesidad"},
    )
    assert resp.status_code == 400
    assert "need_title" in resp.get_json()["error"]


def test_create_mother_cell(auth_client):
    resp = auth_client.post(
        "/groups",
        json={"kind": "mother_cell", "name": "Célula de facilitadores"},
    )
    assert resp.status_code == 201
    assert resp.get_json()["group"]["kind"] == "mother_cell"


def test_invalid_kind(auth_client):
    resp = auth_client.post(
        "/groups", json={"kind": "comite", "name": "x"}
    )
    assert resp.status_code == 400


def test_join_group(auth_client):
    created = auth_client.post(
        "/groups",
        json={"kind": "solution_group", "name": "Sembrar", "need_title": "Hambre"},
    )
    group_id = created.get_json()["group"]["id"]

    headers2 = _login_as(auth_client, "test2@example.com")
    resp = auth_client.post(f"/groups/{group_id}/join", headers=headers2)
    assert resp.status_code == 200

    # Miembro duplicado -> 409
    resp2 = auth_client.post(f"/groups/{group_id}/join", headers=headers2)
    assert resp2.status_code == 409

    detail = auth_client.get(f"/groups/{group_id}")
    members = detail.get_json()["group"]["members"]
    assert len(members) == 2
    assert {m["name"] for m in members} == {"Test User", "Test User 2"}


def test_join_closed_group(auth_client):
    created = auth_client.post(
        "/groups",
        json={"kind": "solution_group", "name": "Sembrar", "need_title": "Hambre"},
    )
    group_id = created.get_json()["group"]["id"]
    auth_client.post(f"/groups/{group_id}/close")

    headers2 = _login_as(auth_client, "test2@example.com")
    resp = auth_client.post(f"/groups/{group_id}/join", headers=headers2)
    assert resp.status_code == 400


def test_child_registers_fractality(auth_client):
    """Réplica registrada -> la célula madre gana el nodo facilitación."""
    mother = auth_client.post(
        "/groups", json={"kind": "mother_cell", "name": "Célula madre"}
    ).get_json()["group"]
    child = auth_client.post(
        "/groups",
        json={"kind": "solution_group", "name": "Hijos del agua", "need_title": "Agua"},
    ).get_json()["group"]

    resp = auth_client.post(
        f"/groups/{mother['id']}/child", json={"child_group_id": child["id"]}
    )
    assert resp.status_code == 200

    detail = auth_client.get(f"/groups/{mother['id']}")
    data = detail.get_json()["group"]
    assert data["children"] == [
        {"id": child["id"], "name": child["name"], "kind": "solution_group", "status": "active"}
    ]
    assert data["skill_nodes"][0]["skill_node"] == "facilitacion"
    assert "réplica" in data["skill_nodes"][0]["evidence"] or "replica" in data["skill_nodes"][0]["evidence"]


def test_child_requires_mother_cell(auth_client):
    sol = auth_client.post(
        "/groups",
        json={"kind": "solution_group", "name": "A", "need_title": "N"},
    ).get_json()["group"]
    other = auth_client.post(
        "/groups",
        json={"kind": "solution_group", "name": "B", "need_title": "N"},
    ).get_json()["group"]
    resp = auth_client.post(
        f"/groups/{sol['id']}/child", json={"child_group_id": other["id"]}
    )
    assert resp.status_code == 400


def test_child_requires_membership(auth_client):
    mother = auth_client.post(
        "/groups", json={"kind": "mother_cell", "name": "MM"}
    ).get_json()["group"]
    child = auth_client.post(
        "/groups",
        json={"kind": "solution_group", "name": "C", "need_title": "N"},
    ).get_json()["group"]
    headers2 = _login_as(auth_client, "test2@example.com")
    resp = auth_client.post(
        f"/groups/{mother['id']}/child",
        json={"child_group_id": child["id"]},
        headers=headers2,
    )
    assert resp.status_code == 403


def test_close_group_only_coordinator(auth_client):
    created = auth_client.post(
        "/groups",
        json={"kind": "solution_group", "name": "Sembrar", "need_title": "Hambre"},
    ).get_json()["group"]
    headers2 = _login_as(auth_client, "test2@example.com")
    auth_client.post(f"/groups/{created['id']}/join", headers=headers2)

    resp = auth_client.post(f"/groups/{created['id']}/close", headers=headers2)
    assert resp.status_code == 403

    resp = auth_client.post(f"/groups/{created['id']}/close")
    assert resp.status_code == 200
    assert resp.get_json()["group"]["status"] == "closed"


def test_list_groups_filter_kind(auth_client):
    auth_client.post(
        "/groups", json={"kind": "solution_group", "name": "S", "need_title": "N"}
    )
    auth_client.post("/groups", json={"kind": "mother_cell", "name": "M"})
    resp = auth_client.get("/groups?kind=solution_group")
    assert resp.get_json()["count"] == 1
    resp = auth_client.get("/groups?kind=mother_cell")
    assert resp.get_json()["count"] == 1
