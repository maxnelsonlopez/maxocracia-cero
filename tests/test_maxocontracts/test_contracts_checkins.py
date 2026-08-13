"""
Tests del Puente A de la Ola 4: γ que escucha la vida.

Cubre:
- POST /contracts/<id>/checkin: registro de γ real con fuente y actor.
- Límite semanal: un check-in por participante cada 7 días (429).
- Validaciones: rango de γ, participante ajeno al contrato.
- GET /contracts/<id>: serie temporal de check-ins en participants_details.
- GET /contracts/cohort: el γ agregado usa los check-ins reales.
"""

import os
import tempfile
from datetime import datetime, timedelta, timezone

os.environ["SECRET_KEY"] = "test-secret"

import pytest

from app import create_app
from app.utils import get_db


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app(db_path=db_path)
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        with app.app_context():
            db = get_db()
            with open("app/schema.sql", "r", encoding="utf-8") as f:
                db.executescript(f.read())

            db.execute(
                "INSERT INTO users (id, email, name, password_hash) VALUES (1, 'a@test.com', 'Alice', 'hash')"
            )
            db.execute(
                "INSERT INTO users (id, email, name, password_hash) VALUES (2, 'b@test.com', 'Bob', 'hash')"
            )
            db.execute(
                "INSERT INTO users (id, email, name, password_hash) VALUES (3, 'c@test.com', 'Carol', 'hash')"
            )
            db.commit()

        yield test_client

    os.close(db_fd)
    os.unlink(db_path)


def user_headers(client, uid):
    """Token del usuario real: la identidad SIEMPRE deriva del JWT (Ola 3A.1)."""
    from app.jwt_utils import create_token

    token = create_token({"user_id": uid})
    return {"Authorization": f"Bearer {token}"}


def _create_contract(client, auth_header, contract_id, description="Contrato"):
    return client.post(
        "/contracts/",
        headers=auth_header,
        json={
            "contract_id": contract_id,
            "civil_description": description,
        },
    )


def _add_participant(client, auth_header, contract_id, user_id, wellness=1.0):
    return client.post(
        f"/contracts/{contract_id}/participants",
        headers=auth_header,
        json={
            "user_id": user_id,
            "wellness": wellness,
        },
    )


def _force_old_checkin(client, contract_id, participant_id, wellness, days_ago):
    """Inserta un check-in con fecha antigua para saltar la ventana semanal."""
    with client.application.app_context():
        db = get_db()
        ts = (datetime.now(timezone.utc) - timedelta(days=days_ago)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        db.execute(
            """
            INSERT INTO maxo_contract_checkins (contract_id, participant_id, wellness, source, reported_by, created_at)
            VALUES (?, ?, ?, 'checkin', ?, ?)
            """,
            (contract_id, participant_id, wellness, "user-1", ts),
        )
        db.commit()


def _create_ready_contract(client):
    """Contrato Alice(1) + Bob(2) listo para check-ins."""
    h = user_headers(client, 1)
    assert _create_contract(client, h, "checkin-contract").status_code == 201
    assert (
        _add_participant(client, h, "checkin-contract", 1, wellness=1.0).status_code
        == 200
    )
    assert (
        _add_participant(client, h, "checkin-contract", 2, wellness=1.0).status_code
        == 200
    )
    return h


def test_checkin_basic(client):
    """Un participante reporta su γ real: queda con fuente y actor (T13)."""
    h = _create_ready_contract(client)

    res = client.post(
        "/contracts/checkin-contract/checkin",
        headers=h,
        json={
            "wellness": 0.92,
            "participant_id": "user-2",
            "source": "checkin",
        },
    )
    assert res.status_code == 201
    data = res.get_json()
    assert data["success"] is True
    assert data["participant_id"] == "user-2"
    assert abs(data["wellness"] - 0.92) < 1e-9
    assert data["source"] == "checkin"
    assert data["reported_by"] == "user-1"
    assert data["total_checkins"] == 1
    assert len(data["series"]) == 1

    # T13: el latido queda auditable y durable
    with client.application.app_context():
        db = get_db()
        event = db.execute(
            "SELECT event_type, metadata_json FROM maxo_contract_events WHERE contract_id = 'checkin-contract' ORDER BY id DESC LIMIT 1"
        ).fetchone()
        assert event is not None
        assert event["event_type"] == "checkin_reported"
        assert "0.92" in event["metadata_json"]
        row = db.execute(
            "SELECT wellness_value, reported_by FROM maxo_contract_participants WHERE contract_id = 'checkin-contract' AND participant_id = 'user-2'"
        ).fetchone()
        assert abs(row["wellness_value"] - 0.92) < 1e-9
        assert row["reported_by"] == "user-1"


def test_checkin_defaults_to_token_actor(client):
    """Sin participant_id, el actor del token reporta su propio γ."""
    h = user_headers(client, 2)
    assert (
        _create_contract(
            client, h, "checkin-self", description="Mi contrato"
        ).status_code
        == 201
    )
    assert (
        _add_participant(client, h, "checkin-self", 2, wellness=1.0).status_code == 200
    )

    res = client.post(
        "/contracts/checkin-self/checkin", headers=h, json={"wellness": 1.1}
    )
    assert res.status_code == 201
    data = res.get_json()
    assert data["participant_id"] == "user-2"
    assert data["reported_by"] == "user-2"


def test_checkin_updates_contract_gamma(client):
    """El contrato escucha: el γ del participante adopta el latido real."""
    h = _create_ready_contract(client)

    client.post(
        "/contracts/checkin-contract/checkin",
        headers=h,
        json={
            "wellness": 0.65,
            "participant_id": "user-2",
        },
    )
    assert (
        client.post(
            "/contracts/checkin-contract/checkin",
            headers=h,
            json={
                "wellness": 1.2,
                "participant_id": "user-2",
            },
        ).status_code
        == 429
    )

    detail = client.get("/contracts/checkin-contract", headers=h).get_json()
    bob = next(d for d in detail["participants_details"] if d["id"] == "user-2")
    assert abs(bob["wellness"] - 0.65) < 1e-9


def test_checkin_weekly_limit(client):
    """Mejora de γ dentro de la ventana: límite semanal (429)."""
    h = _create_ready_contract(client)

    assert (
        client.post(
            "/contracts/checkin-contract/checkin",
            headers=h,
            json={
                "wellness": 1.0,
                "participant_id": "user-2",
            },
        ).status_code
        == 201
    )

    res = client.post(
        "/contracts/checkin-contract/checkin",
        headers=h,
        json={
            "wellness": 1.1,
            "participant_id": "user-2",
        },
    )
    assert res.status_code == 429
    data = res.get_json()
    assert data["code"] == "CHECKIN_WEEKLY_LIMIT"
    assert data["window_days"] == 7


def test_checkin_decline_always_heard(client):
    """Política asimétrica: una CAÍDA de γ se escucha siempre, sin esperar
    la ventana (el WellnessProtectorBlock monitorea continuamente, INV1)."""
    h = _create_ready_contract(client)

    assert (
        client.post(
            "/contracts/checkin-contract/checkin",
            headers=h,
            json={
                "wellness": 1.0,
                "participant_id": "user-2",
            },
        ).status_code
        == 201
    )

    res = client.post(
        "/contracts/checkin-contract/checkin",
        headers=h,
        json={
            "wellness": 0.7,
            "participant_id": "user-2",
        },
    )
    assert res.status_code == 201
    data = res.get_json()
    assert data["policy"]["accepted"] == "decline_urgent"
    assert data["total_checkins"] == 2

    # El contrato adoptó el latido de la caída
    detail = client.get("/contracts/checkin-contract", headers=h).get_json()
    bob = next(d for d in detail["participants_details"] if d["id"] == "user-2")
    assert abs(bob["wellness"] - 0.7) < 1e-9

    # Otra caída al día siguiente también se escucha (crisis sostenida)
    res = client.post(
        "/contracts/checkin-contract/checkin",
        headers=h,
        json={
            "wellness": 0.6,
            "participant_id": "user-2",
        },
    )
    assert res.status_code == 201
    assert res.get_json()["total_checkins"] == 3


def test_checkin_equal_value_counts_as_noise(client):
    """Un γ idéntico no aporta información: aplica el ritmo semanal."""
    h = _create_ready_contract(client)

    assert (
        client.post(
            "/contracts/checkin-contract/checkin",
            headers=h,
            json={
                "wellness": 1.0,
                "participant_id": "user-2",
            },
        ).status_code
        == 201
    )
    res = client.post(
        "/contracts/checkin-contract/checkin",
        headers=h,
        json={
            "wellness": 1.0,
            "participant_id": "user-2",
        },
    )
    assert res.status_code == 429


def test_checkin_configurable_window(client):
    """La ventana es configurable por despliegue (migración masiva):
    MAXO_CHECKIN_WINDOW_DAYS define el ritmo de las mejoras."""
    os.environ["MAXO_CHECKIN_WINDOW_DAYS"] = "3"
    try:
        h = _create_ready_contract(client)
        _force_old_checkin(client, "checkin-contract", "user-2", 0.9, days_ago=2)

        # Mejora a los 2 días: dentro de la ventana de 3 -> 429
        res = client.post(
            "/contracts/checkin-contract/checkin",
            headers=h,
            json={
                "wellness": 1.1,
                "participant_id": "user-2",
            },
        )
        assert res.status_code == 429
        assert res.get_json()["window_days"] == 3
        assert res.get_json()["days_until_next"] == 1
    finally:
        del os.environ["MAXO_CHECKIN_WINDOW_DAYS"]

    # Fuera de la ventana (9 días > 7), la mejora fluye
    h = _create_ready_contract(client)
    _force_old_checkin(client, "checkin-contract", "user-2", 0.9, days_ago=9)
    res = client.post(
        "/contracts/checkin-contract/checkin",
        headers=h,
        json={
            "wellness": 1.1,
            "participant_id": "user-2",
        },
    )
    assert res.status_code == 201
    assert res.get_json()["policy"]["accepted"] == "window_open"


def test_checkin_weekly_limit_respects_per_participant(client):
    """El límite es por participante, no por contrato."""
    h = _create_ready_contract(client)

    assert (
        client.post(
            "/contracts/checkin-contract/checkin",
            headers=h,
            json={
                "wellness": 1.0,
                "participant_id": "user-1",
            },
        ).status_code
        == 201
    )
    # Bob aún puede reportar el suyo
    assert (
        client.post(
            "/contracts/checkin-contract/checkin",
            headers=h,
            json={
                "wellness": 1.1,
                "participant_id": "user-2",
            },
        ).status_code
        == 201
    )


def test_checkin_old_week_allows_new(client):
    """Tras la ventana de 7 días, el participante puede reportar de nuevo."""
    h = _create_ready_contract(client)
    _force_old_checkin(client, "checkin-contract", "user-2", 0.95, days_ago=9)

    res = client.post(
        "/contracts/checkin-contract/checkin",
        headers=h,
        json={
            "wellness": 1.2,
            "participant_id": "user-2",
        },
    )
    assert res.status_code == 201
    assert res.get_json()["total_checkins"] == 2


def test_checkin_invalid_wellness(client):
    """γ fuera de rango [0.5, 1.5] se rechaza (Ola 3A.5)."""
    h = _create_ready_contract(client)

    for bad in (0.1, 1.9, "alto"):
        res = client.post(
            "/contracts/checkin-contract/checkin",
            headers=h,
            json={
                "wellness": bad,
                "participant_id": "user-2",
            },
        )
        assert res.status_code == 400, f"wellness {bad} debió fallar"


def test_checkin_requires_wellness(client):
    h = _create_ready_contract(client)
    res = client.post(
        "/contracts/checkin-contract/checkin",
        headers=h,
        json={
            "participant_id": "user-2",
        },
    )
    assert res.status_code == 400


def test_checkin_foreign_participant_rejected(client):
    """Quien no es parte del contrato no puede reportar (autoridad de partes)."""
    h = _create_ready_contract(client)
    res = client.post(
        "/contracts/checkin-contract/checkin",
        headers=h,
        json={
            "wellness": 1.0,
            "participant_id": "user-3",
        },
    )
    assert res.status_code == 403
    assert res.get_json()["code"] == "CHECKIN_NOT_PARTICIPANT"


def test_checkin_unknown_contract(client):
    h = user_headers(client, 1)
    res = client.post(
        "/contracts/does-not-exist/checkin", headers=h, json={"wellness": 1.0}
    )
    assert res.status_code == 404


def test_detail_exposes_checkin_series(client):
    """Criterio de salida: 3 check-ins muestran la serie completa en el detalle."""
    h = _create_ready_contract(client)
    _force_old_checkin(client, "checkin-contract", "user-2", 1.3, days_ago=20)
    _force_old_checkin(client, "checkin-contract", "user-2", 0.85, days_ago=12)
    assert (
        client.post(
            "/contracts/checkin-contract/checkin",
            headers=h,
            json={
                "wellness": 1.05,
                "participant_id": "user-2",
            },
        ).status_code
        == 201
    )

    detail = client.get("/contracts/checkin-contract", headers=h).get_json()
    bob = next(d for d in detail["participants_details"] if d["id"] == "user-2")
    assert bob["checkins_count"] == 3
    assert [round(c["wellness"], 2) for c in bob["checkins"]] == [1.3, 0.85, 1.05]
    assert all(c["reported_by"] == "user-1" for c in bob["checkins"])

    alice = next(d for d in detail["participants_details"] if d["id"] == "user-1")
    assert alice["checkins_count"] == 0
    assert alice["checkins"] == []


def test_cohort_gamma_uses_real_checkins(client):
    """El γ agregado de la cohorte usa los check-ins reales (último latido)."""
    h = user_headers(client, 1)

    # Parte colectiva con dos contratos
    assert (
        _create_contract(client, h, "coop-a-1", description="Contrato coop").status_code
        == 201
    )
    res = client.post(
        "/contracts/coop-a-1/participants",
        headers=h,
        json={
            "party_id": "coop-7",
            "party_type": "cooperative",
            "display_name": "Cooperativa Semilla",
        },
    )
    assert res.status_code == 200

    assert (
        _create_contract(
            client, h, "coop-a-2", description="Segundo contrato coop"
        ).status_code
        == 201
    )
    res = client.post(
        "/contracts/coop-a-2/participants",
        headers=h,
        json={
            "party_id": "coop-7",
            "party_type": "cooperative",
            "display_name": "Cooperativa Semilla",
        },
    )
    assert res.status_code == 200

    # Latido antiguo en coop-a-1 (γ=0.9) y, semanas después, el latido real
    # en cada contrato: 1.2 en coop-a-1 y 1.0 en coop-a-2
    _force_old_checkin(client, "coop-a-1", "coop-7", 0.9, days_ago=15)
    assert (
        client.post(
            "/contracts/coop-a-1/checkin",
            headers=h,
            json={
                "wellness": 1.2,
                "participant_id": "coop-7",
            },
        ).status_code
        == 201
    )
    assert (
        client.post(
            "/contracts/coop-a-2/checkin",
            headers=h,
            json={
                "wellness": 1.0,
                "participant_id": "coop-7",
            },
        ).status_code
        == 201
    )

    cohort = client.get("/contracts/cohort", headers=h).get_json()
    coop = next(p for p in cohort["parties"] if p["party_id"] == "coop-7")
    # Último latido por contrato: (1.2 + 1.0) / 2 = 1.1
    assert abs(coop["wellness"] - 1.1) < 1e-9
    assert coop["wellness_source"] == "checkins"
    assert coop["checkins_total"] == 3
