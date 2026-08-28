# -*- coding: utf-8 -*-
"""Tests del Form Cero con años de educación (M7 — rama educativa).

El Formulario CERO captura `educacion_anos` (0-60, opcional); el puente
`educacion_indice()` traduce años<->índice; el analizador SDV usa el dato
declarado como fuente para la dimensión educación (INV2-EDU conectado).
"""

from app.sdv_analyzer import SDVAnalyzer, educacion_indice


def _form_data(**overrides):
    data = {
        "name": "Ana Vital",
        "email": "test@example.com",  # dueño del auth_client (autorización PUT)
        "phone_call": "555",
        "phone_whatsapp": "555",
        "telegram_handle": "@ana",
        "city": "Bogotá",
        "neighborhood": "Centro",
        "personal_values": "comunidad",
        "offer_description": "enseño lectura",
        "need_description": "aprender a programar",
        "need_urgency": "Media",
        "consent_given": True,
    }
    data.update(overrides)
    return data


def test_register_with_education_years(auth_client):
    """El Form Cero guarda los años de educación declarados."""
    resp = auth_client.post("/forms/participant", json=_form_data(educacion_anos=8))
    assert resp.status_code == 201
    participant_id = resp.get_json()["participant_id"]

    detail = auth_client.get(f"/forms/participants/{participant_id}")
    assert detail.status_code == 200
    assert detail.get_json()["educacion_anos"] == 8


def test_register_without_education_years(auth_client):
    """Sin dato: la columna queda NULL (la duda no se castiga)."""
    resp = auth_client.post("/forms/participant", json=_form_data())
    assert resp.status_code == 201
    participant_id = resp.get_json()["participant_id"]
    detail = auth_client.get(f"/forms/participants/{participant_id}").get_json()
    assert detail["educacion_anos"] is None


def test_register_rejects_invalid_years(auth_client):
    resp = auth_client.post("/forms/participant", json=_form_data(educacion_anos=-1))
    assert resp.status_code == 400
    resp = auth_client.post("/forms/participant", json=_form_data(educacion_anos=70))
    assert resp.status_code == 400
    resp = auth_client.post("/forms/participant", json=_form_data(educacion_anos="años"))
    assert resp.status_code == 400


def test_update_education_years(auth_client):
    created = auth_client.post("/forms/participant", json=_form_data())
    participant_id = created.get_json()["participant_id"]
    resp = auth_client.put(
        f"/forms/participants/{participant_id}",
        json={"educacion_anos": 12},
    )
    assert resp.status_code == 200
    detail = auth_client.get(f"/forms/participants/{participant_id}").get_json()
    assert detail["educacion_anos"] == 12


def test_update_rejects_invalid_years(auth_client):
    created = auth_client.post("/forms/participant", json=_form_data())
    participant_id = created.get_json()["participant_id"]
    resp = auth_client.put(
        f"/forms/participants/{participant_id}",
        json={"educacion_anos": 61},
    )
    assert resp.status_code == 400


class TestAnalyzerConPuente:
    def test_estimacion_usa_anos_declarados(self, auth_client):
        created = auth_client.post(
            "/forms/participant", json=_form_data(educacion_anos=6)
        )
        participant_id = created.get_json()["participant_id"]

        with auth_client.application.app_context():
            from app.utils import get_db

            conn = get_db()
            analyzer = SDVAnalyzer(conn)
            score = analyzer.estimate_participant_sdv(participant_id)
            assert score.educacion == educacion_indice(6)  # 0.55

    def test_estimacion_piso_pleno_con_12_anos(self, auth_client):
        created = auth_client.post(
            "/forms/participant", json=_form_data(educacion_anos=14)
        )
        participant_id = created.get_json()["participant_id"]
        with auth_client.application.app_context():
            from app.utils import get_db

            conn = get_db()
            analyzer = SDVAnalyzer(conn)
            score = analyzer.estimate_participant_sdv(participant_id)
            assert score.educacion == 1.0

    def test_estimacion_sin_dato_mantiene_cualitativo(self, auth_client):
        """Sin años declarados, la estimación por necesidad conserva el valor."""
        created = auth_client.post(
            "/forms/participant",
            json=_form_data(
                need_urgency="Alta",
                need_human_dimensions=["crecimiento_aprendizaje"],
            ),
        )
        participant_id = created.get_json()["participant_id"]
        with auth_client.application.app_context():
            from app.utils import get_db

            conn = get_db()
            analyzer = SDVAnalyzer(conn)
            score = analyzer.estimate_participant_sdv(participant_id)
            assert score.educacion < 1.0  # penalizada por la necesidad
