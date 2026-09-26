# -*- coding: utf-8 -*-
"""Test 3: el árbol viene sembrado (9 ramas, >40 temas, preguntas por tema)."""


def _token(client, username="nodo"):
    client.post("/api/auth/register", json={"username": username, "password": "secreto"})
    resp = client.post("/api/auth/login", json={"username": username, "password": "secreto"})
    return resp.get_json()["token"]


def test_tree_has_9_branches_and_more_than_40_topics(client):
    token = _token(client)
    headers = {"X-Auth-Token": token}
    resp = client.get("/api/tree", headers=headers)
    assert resp.status_code == 200
    branches = resp.get_json()["branches"]
    assert len(branches) == 9

    total = sum(len(b["topics"]) for b in branches)
    assert total > 40

    # Slugs obligatorios de las 9 ramas (la Ética desde M16).
    slugs = {b["slug"] for b in branches}
    assert {
        "etica", "matematicas", "higiene", "relaciones", "lectura",
        "escritura", "lenguaje", "naturaleza", "computadores",
    } <= slugs


def test_every_topic_has_at_least_3_questions(client):
    token = _token(client)
    headers = {"X-Auth-Token": token}
    branches = client.get("/api/tree", headers=headers).get_json()["branches"]
    for branch in branches:
        for topic in branch["topics"]:
            assert topic["questions"] >= 3, f"El tema {topic['slug']} tiene menos de 3 preguntas"

    total_questions = sum(t["questions"] for b in branches for t in b["topics"])
    assert total_questions >= 3 * 30


def test_branches_are_ordered(client):
    token = _token(client)
    headers = {"X-Auth-Token": token}
    branches = client.get("/api/tree", headers=headers).get_json()["branches"]
    # Las 9 ramas deben estar en orden (campo 'orden'): la Ética primero
    # (M16: los valores antes que la técnica), computadores al final.
    assert branches[0]["slug"] == "etica"
    assert branches[-1]["slug"] == "computadores"


def test_public_tree_needs_no_login_and_leaks_no_progress(client):
    # El árbol privado exige token...
    assert client.get("/api/tree").status_code == 401
    # ...pero el público se mira sin papeles, sin estado personal.
    resp = client.get("/api/tree/public")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["publico"] is True
    assert len(body["branches"]) == 9
    for branch in body["branches"]:
        for topic in branch["topics"]:
            assert topic["estado"] == "not_seen"
            assert topic["score"] is None
            assert topic["triada"] is None
            assert topic["publico"] is True
