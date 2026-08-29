# -*- coding: utf-8 -*-
"""Tests del Foro Abierto (M2 — rama educativa).

Cubren: publicación, validaciones, filtros, cierre por autor/admin,
prohibición de cierre por terceros, y la puerta de necesidades (/forum/needs).
"""


def test_requires_token(client):
    """Sin token, el foro niega el acceso."""
    resp = client.get("/forum/posts")
    assert resp.status_code == 401
    resp = client.post("/forum/posts", json={"kind": "topic", "title": "x", "body": "y"})
    assert resp.status_code == 401


def test_create_post_ok(auth_client):
    """Un miembro publica una pregunta en la plaza."""
    resp = auth_client.post(
        "/forum/posts",
        json={"kind": "question", "title": "¿Qué es un TVI?", "body": "No lo entiendo aún."},
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["success"] is True
    post = data["post"]
    assert post["id"] > 0
    assert post["kind"] == "question"
    assert post["status"] == "open"
    assert post["author"]["name"] == "Test User"
    assert post["tags"] == []


def test_create_post_with_tags(auth_client):
    resp = auth_client.post(
        "/forum/posts",
        json={
            "kind": "topic",
            "title": "Taller de huertas",
            "body": "Propongo aprender a cultivar con la comunidad.",
            "tags": ["naturaleza", "taller"],
        },
    )
    assert resp.status_code == 201
    assert resp.get_json()["post"]["tags"] == ["naturaleza", "taller"]
    assert resp.get_json()["post"]["kind_label"] == "Tema"


def test_create_post_invalid_kind(auth_client):
    resp = auth_client.post(
        "/forum/posts",
        json={"kind": "curriculum", "title": "x", "body": "y"},
    )
    assert resp.status_code == 400
    assert "allowed" in resp.get_json()


def test_create_post_missing_fields(auth_client):
    resp = auth_client.post("/forum/posts", json={"kind": "topic", "body": "y"})
    assert resp.status_code == 400
    resp = auth_client.post("/forum/posts", json={"kind": "topic", "title": "x"})
    assert resp.status_code == 400


def test_create_post_need_id_only_for_need(auth_client):
    resp = auth_client.post(
        "/forum/posts",
        json={"kind": "topic", "title": "x", "body": "y", "need_id": 1},
    )
    assert resp.status_code == 400


def test_list_posts_by_type(auth_client):
    auth_client.post(
        "/forum/posts", json={"kind": "question", "title": "Q1", "body": "b1"}
    )
    auth_client.post(
        "/forum/posts", json={"kind": "topic", "title": "T1", "body": "b2"}
    )
    resp = auth_client.get("/forum/posts?type=question")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["count"] == 1
    assert data["posts"][0]["title"] == "Q1"

    resp = auth_client.get("/forum/posts?type=topic")
    assert resp.get_json()["count"] == 1

    resp = auth_client.get("/forum/posts?type=not-a-kind")
    assert resp.status_code == 400


def test_list_posts_filter_tag_and_limit(auth_client):
    auth_client.post(
        "/forum/posts",
        json={"kind": "topic", "title": "A", "body": "b", "tags": ["vida"]},
    )
    auth_client.post(
        "/forum/posts",
        json={"kind": "topic", "title": "B", "body": "b", "tags": ["otro"]},
    )
    resp = auth_client.get("/forum/posts?tag=vida")
    assert resp.get_json()["count"] == 1

    resp = auth_client.get("/forum/posts?limit=1")
    assert resp.get_json()["count"] == 1

    resp = auth_client.get("/forum/posts?limit=abc")
    assert resp.status_code == 400


def test_close_post_by_author(auth_client):
    created = auth_client.post(
        "/forum/posts", json={"kind": "question", "title": "Q", "body": "b"}
    )
    post_id = created.get_json()["post"]["id"]
    resp = auth_client.post(f"/forum/posts/{post_id}/close", json={})
    assert resp.status_code == 200
    assert resp.get_json()["post"]["status"] == "closed"


def test_close_post_with_resolution(auth_client):
    created = auth_client.post(
        "/forum/posts", json={"kind": "topic", "title": "T", "body": "b"}
    )
    post_id = created.get_json()["post"]["id"]
    resp = auth_client.post(
        f"/forum/posts/{post_id}/close",
        json={"resolution": "Se formó un grupo de solución."},
    )
    assert resp.status_code == 200
    post = resp.get_json()["post"]
    assert post["status"] == "resolved"
    assert "grupo" in post["body"]


def test_close_post_forbidden_for_others(auth_client):
    created = auth_client.post(
        "/forum/posts", json={"kind": "topic", "title": "T", "body": "b"}
    )
    post_id = created.get_json()["post"]["id"]

    # Segundo usuario sin admin: login manual (test2 no es admin).
    login = auth_client.post(
        "/auth/login", json={"email": "test2@example.com", "password": "ValidPass123!"}
    )
    token = login.get_json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    resp = auth_client.post(f"/forum/posts/{post_id}/close", json={}, headers=headers)
    assert resp.status_code == 403


def test_close_post_not_found(auth_client):
    resp = auth_client.post("/forum/posts/9999/close", json={})
    assert resp.status_code == 404


def test_close_post_by_admin(auth_client):
    created = auth_client.post(
        "/forum/posts", json={"kind": "topic", "title": "T", "body": "b"}
    )
    post_id = created.get_json()["post"]["id"]
    # Admin cierra por moderación (nunca por opinión: es cierre, no borrado).
    login = auth_client.post(
        "/auth/login", json={"email": "admin@example.com", "password": "ValidPass123!"}
    )
    token = login.get_json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    resp = auth_client.post(
        f"/forum/posts/{post_id}/close",
        json={"resolution": "Moderación: contenido que vulnera la norma."},
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.get_json()["post"]["status"] == "resolved"


def test_forum_needs_gate(auth_client):
    """/forum/needs expone solo necesidades abiertas (puerta al matching)."""
    need_create = auth_client.post(
        "/forum/posts",
        json={"kind": "need", "title": "Necesitamos agua limpia", "body": "en la vereda"},
    )
    auth_client.post(
        "/forum/posts", json={"kind": "topic", "title": "Opinión", "body": "otro"}
    )
    resp = auth_client.get("/forum/needs")
    assert resp.status_code == 200
    assert resp.get_json()["count"] == 1

    # Al cerrar la necesidad, desaparece de la puerta.
    need_id = need_create.get_json()["post"]["id"]
    auth_client.post(
        f"/forum/posts/{need_id}/close",
        json={"resolution": "Resuelto por el grupo de solución."},
    )
    resp = auth_client.get("/forum/needs")
    assert resp.get_json()["count"] == 0


def test_get_post_detail(auth_client):
    created = auth_client.post(
        "/forum/posts", json={"kind": "workshop_offer", "title": "Ofrezco mates", "body": "b"}
    )
    post_id = created.get_json()["post"]["id"]
    resp = auth_client.get(f"/forum/posts/{post_id}")
    assert resp.status_code == 200
    assert resp.get_json()["post"]["id"] == post_id
    assert resp.get_json()["post"]["kind"] == "workshop_offer"


# ---------------------------------------------------------------------------
# Respuestas (la conversación de la plaza — siguiente etapa de la rama)
# ---------------------------------------------------------------------------


def _create_open_post(client):
    created = client.post(
        "/forum/posts", json={"kind": "question", "title": "Q", "body": "b"}
    )
    return created.get_json()["post"]["id"]


def test_add_reply_ok(auth_client):
    post_id = _create_open_post(auth_client)
    resp = auth_client.post(
        f"/forum/posts/{post_id}/replies", json={"body": "Yo tampoco lo tenía claro."}
    )
    assert resp.status_code == 201
    reply = resp.get_json()["reply"]
    assert reply["post_id"] == post_id
    assert reply["author"]["name"] == "Test User"

    # El listado muestra la respuesta en orden.
    listing = auth_client.get(f"/forum/posts/{post_id}/replies")
    assert listing.status_code == 200
    assert listing.get_json()["count"] == 1
    assert listing.get_json()["replies"][0]["author"]["name"] == "Test User"

    # El post ahora reporta reply_count.
    detail = auth_client.get(f"/forum/posts/{post_id}")
    assert detail.get_json()["post"]["reply_count"] == 1


def test_add_reply_requires_body(auth_client):
    post_id = _create_open_post(auth_client)
    resp = auth_client.post(f"/forum/posts/{post_id}/replies", json={"body": " "})
    assert resp.status_code == 400


def test_add_reply_requires_open_post(auth_client):
    post_id = _create_open_post(auth_client)
    auth_client.post(f"/forum/posts/{post_id}/close", json={})
    resp = auth_client.post(
        f"/forum/posts/{post_id}/replies", json={"body": "intento tardío"}
    )
    assert resp.status_code == 400


def test_add_reply_to_missing_post(auth_client):
    resp = auth_client.post("/forum/posts/9999/replies", json={"body": "hola"})
    assert resp.status_code == 404


def test_list_replies_of_missing_post(auth_client):
    resp = auth_client.get("/forum/posts/9999/replies")
    assert resp.status_code == 404


def test_replies_require_token(client):
    assert client.post("/forum/posts/1/replies", json={"body": "x"}).status_code == 401
    assert client.get("/forum/posts/1/replies").status_code == 401


def test_multiple_replies_ordered(auth_client):
    post_id = _create_open_post(auth_client)
    auth_client.post(f"/forum/posts/{post_id}/replies", json={"body": "primera"})

    # Segunda respuesta de otro usuario.
    login = auth_client.post(
        "/auth/login", json={"email": "test2@example.com", "password": "ValidPass123!"}
    )
    token = login.get_json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    auth_client.post(
        f"/forum/posts/{post_id}/replies", json={"body": "segunda"}, headers=headers
    )

    listing = auth_client.get(f"/forum/posts/{post_id}/replies")
    bodies = [r["body"] for r in listing.get_json()["replies"]]
    assert bodies == ["primera", "segunda"]


# ---------------------------------------------------------------------------
# Puente siamés (M8): la necesidad del foro sangra a la Plaza de Apoyo
# ---------------------------------------------------------------------------


def _register_participant(client, email="test@example.com"):
    return client.post(
        "/forms/participant",
        json={
            "name": "Test User",
            "email": email,
            "phone_call": "555",
            "phone_whatsapp": "555",
            "telegram_handle": "@test",
            "city": "Bogotá",
            "neighborhood": "Centro",
            "personal_values": "comunidad",
            "offer_description": "enseño lectura",
            "need_description": "aprender",
            "need_urgency": "Media",
            "consent_given": True,
        },
    )


def test_need_links_to_plaza_when_participant_exists(auth_client):
    """Con Form Cero: la necesidad del foro aparece en el matching (batido)."""
    _register_participant(auth_client)
    resp = auth_client.post(
        "/forum/posts",
        json={"kind": "need", "title": "Quiero aprender huertas", "body": "Necesito aprender huertas con la comunidad."},
    )
    assert resp.status_code == 201
    post = resp.get_json()["post"]
    assert post["in_plaza"] is True
    assert post["need_id"] is not None

    # La necesidad vive en participant_needs (la tabla del matching).
    participant = auth_client.get("/forms/participants?limit=10").get_json()[
        "participants"
    ][0]
    needs = auth_client.get(
        f"/forms/participants/{participant['id']}/needs"
    ).get_json()["needs"]
    assert any(n["id"] == post["need_id"] for n in needs)


def test_need_standalone_without_participant(auth_client):
    """Sin Form Cero: el post queda standalone con aviso (honesto)."""
    resp = auth_client.post(
        "/forum/posts",
        json={"kind": "need", "title": "Necesidad", "body": "Sin formulario aún."},
    )
    post = resp.get_json()["post"]
    assert resp.status_code == 201
    assert post["in_plaza"] is False
    assert post["need_id"] is None


def test_need_no_duplicates_in_plaza(auth_client):
    """Dos posts iguales referencian la misma necesidad (no se duplica)."""
    _register_participant(auth_client)
    body = "Necesito aprender a reparar bicicletas."
    first = auth_client.post(
        "/forum/posts", json={"kind": "need", "title": "Bici 1", "body": body}
    ).get_json()["post"]
    second = auth_client.post(
        "/forum/posts", json={"kind": "need", "title": "Bici 2", "body": body}
    ).get_json()["post"]
    assert first["need_id"] is not None
    assert second["need_id"] == first["need_id"]


class TestBusquedaTextual:
    """La plaza se busca con la propia lengua (Backlog UX, reflexión §3.1): el
    filtro por tipo/tag se queda corto al crecer; la búsqueda es literal y
    case-insensitive (título o cuerpo)."""

    def _posts(self, auth_client):
        auth_client.post(
            "/forum/posts",
            json={"kind": "question", "title": "¿Qué es un TVI?", "body": "Primer cuerpo."},
        )
        auth_client.post(
            "/forum/posts",
            json={"kind": "topic", "title": "Huertas urbanas", "body": "Cultivar en comunidad."},
        )

    def test_busqueda_por_titulo(self, auth_client):
        self._posts(auth_client)
        data = auth_client.get("/forum/posts?q=huertas").get_json()
        assert data["count"] == 1
        assert data["posts"][0]["title"] == "Huertas urbanas"

    def test_busqueda_case_insensitive(self, auth_client):
        self._posts(auth_client)
        upper = auth_client.get("/forum/posts?q=TVI").get_json()
        lower = auth_client.get("/forum/posts?q=tvi").get_json()
        assert upper["count"] == lower["count"] == 1

    def test_busqueda_por_cuerpo(self, auth_client):
        self._posts(auth_client)
        data = auth_client.get("/forum/posts?q=cultivar").get_json()
        assert data["count"] == 1
        assert data["posts"][0]["title"] == "Huertas urbanas"

    def test_busqueda_sin_resultados(self, auth_client):
        self._posts(auth_client)
        data = auth_client.get("/forum/posts?q=noexiste").get_json()
        assert data["count"] == 0

    def test_busqueda_comodines_literales(self, auth_client):
        """% y _ se escapan: el término se busca tal cual, no como patrón."""
        auth_client.post(
            "/forum/posts",
            json={"kind": "topic", "title": "Costos vitales", "body": "El costo es 10% de la vida."},
        )
        literal = auth_client.get("/forum/posts?q=10%25").get_json()
        assert literal["count"] == 1
        # '_' literal no matchea '10%' ni '10X' (sin subrayado en el texto).
        underscore = auth_client.get("/forum/posts?q=10_").get_json()
        assert underscore["count"] == 0

    def test_busqueda_combinada_con_tipo(self, auth_client):
        self._posts(auth_client)
        data = auth_client.get("/forum/posts?q=tvi&type=topic").get_json()
        assert data["count"] == 0
        data = auth_client.get("/forum/posts?q=tvi&type=question").get_json()
        assert data["count"] == 1
