import json

from app import synthetic_sessions


def _create(admin_client, **overrides):
    payload = {
        "mandate": "Clasificar solicitudes y preparar seguimientos",
        "mode": "recommendation",
        "scope": {
            "read": ["read_intake_summary", "read_followup_alerts"],
            "write": ["draft_followup"],
        },
        "context": {"documents": ["forms-contract-v2"]},
        "budget": {"max_requests": 2, "max_cost_usd": 0.01},
    }
    payload.update(overrides)
    response = admin_client.post("/api/synthetic-sessions", json=payload)
    assert response.status_code == 201, response.get_json()
    return response.get_json()["session"]


def test_session_requires_admin(client, auth_client):
    response = auth_client.post(
        "/api/synthetic-sessions",
        json={"mandate": "leer", "mode": "recommendation"},
    )
    assert response.status_code == 403


def test_create_and_read_tool_are_minimised(admin_client):
    session = _create(admin_client)
    assert session["status"] == "active"
    assert session["scope"]["forbidden"]
    assert session["context"]["context_hash"].startswith("sha256:")

    response = admin_client.post(
        f"/api/synthetic-sessions/{session['session_id']}/tool",
        json={"tool": "read_intake_summary"},
    )
    assert response.status_code == 200
    result = response.get_json()["result"]
    assert result["mutated"] is False
    assert "privacy" in result
    assert "email" not in json.dumps(result).lower()


def test_forbidden_tool_is_rejected_and_audited(admin_client, app):
    session = _create(
        admin_client,
        scope={
            "read": ["read_intake_summary"],
            "write": ["draft_followup"],
        },
    )
    response = admin_client.post(
        f"/api/synthetic-sessions/{session['session_id']}/tool",
        json={"tool": "read_followup_alerts"},
    )
    assert response.status_code == 403

    with app.app_context():
        from app.utils import get_db

        row = get_db().execute(
            "SELECT COUNT(*) AS total FROM session_events WHERE session_id = ? AND event_type = 'tool_denied'",
            (session["session_id"],),
        ).fetchone()
        assert row["total"] == 1


def test_run_review_and_audit_do_not_mutate(monkeypatch, admin_client, app):
    session = _create(admin_client)
    calls = []

    def fake_oracle(messages):
        calls.append(messages)
        return (
            {
                "opinion": "Falta contexto; propongo revisar primero.",
                "evidence": [{"source": "resumen", "fact": "Hay entradas activas."}],
                "uncertainty": "No hay evidencia individual suficiente.",
                "proposal": "Preparar un borrador para revisión humana.",
                "refusal": None,
            },
            "deepseek",
            "deepseek-chat",
        )

    monkeypatch.setattr(synthetic_sessions, "_call_session_oracle", fake_oracle)
    response = admin_client.post(
        f"/api/synthetic-sessions/{session['session_id']}/run",
        json={
            "instruction": "Analiza el resumen y declara incertidumbres.",
            "tools": ["read_intake_summary", "read_followup_alerts"],
        },
    )
    assert response.status_code == 200, response.get_json()
    assert response.get_json()["mutated"] is False
    assert calls
    assert "api_key" not in json.dumps(calls).lower()

    response = admin_client.post(
        f"/api/synthetic-sessions/{session['session_id']}/review",
        json={"decision": "approve", "reason": "Revisé la propuesta y el alcance."},
    )
    assert response.status_code == 200
    assert response.get_json()["session"]["status"] == "approved"

    response = admin_client.get(
        f"/api/synthetic-sessions/{session['session_id']}/audit"
    )
    assert response.status_code == 200
    assert response.headers["Content-Disposition"].startswith("attachment;")
    audit = response.get_json()
    assert any(event["event_type"] == "assistant_message" for event in audit["events"])
    assert audit["reviews"][0]["decision"] == "approve"

    with app.app_context():
        from app.utils import get_db

        count = get_db().execute("SELECT COUNT(*) FROM follow_ups").fetchone()[0]
        assert count == 0


def test_budget_and_revocation_stop_future_runs(monkeypatch, admin_client):
    session = _create(admin_client, budget={"max_requests": 1, "max_cost_usd": 0.01})
    monkeypatch.setattr(
        synthetic_sessions,
        "_call_session_oracle",
        lambda messages: ({"opinion": "ok"}, "local", "test-model"),
    )
    endpoint = f"/api/synthetic-sessions/{session['session_id']}/run"
    first = admin_client.post(endpoint, json={"instruction": "Resume."})
    assert first.status_code == 200
    second = admin_client.post(endpoint, json={"instruction": "Resume otra vez."})
    assert second.status_code == 429

    session2 = _create(admin_client)
    response = admin_client.post(
        f"/api/synthetic-sessions/{session2['session_id']}/revoke",
        json={"reason": "Se cierra la prueba manual."},
    )
    assert response.status_code == 200
    response = admin_client.post(
        f"/api/synthetic-sessions/{session2['session_id']}/run",
        json={"instruction": "No debe ejecutarse."},
    )
    assert response.status_code == 409
