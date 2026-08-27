# -*- coding: utf-8 -*-
"""Test 3: el árbol viene sembrado (8 ramas, >30 temas, preguntas por tema)."""


def _token(client, username="nodo"):
    client.post("/api/auth/register", json={"username": username, "password": "secreto"})
    resp = client.post("/api/auth/login", json={"username": username, "password": "secreto"})
    return resp.get_json()["token"]


def test_tree_has_8_branches_and_more_than_30_topics(client):
    token = _token(client)
    headers = {"X-Auth-Token": token}
    resp = client.get("/api/tree", headers=headers)
    assert resp.status_code == 200
    branches = resp.get_json()["branches"]
    assert len(branches) == 8

    total = sum(len(b["topics"]) for b in branches)
    assert total > 30

    # Slugs obligatorios de las 8 ramas.
    slugs = {b["slug"] for b in branches}
    assert {
        "matematicas", "higiene", "relaciones", "lectura",
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
    # Las 8 ramas deben estar en orden (campo 'orden'): empiezan y terminan así.
    assert branches[0]["slug"] == "matematicas"
    assert branches[-1]["slug"] == "computadores"
