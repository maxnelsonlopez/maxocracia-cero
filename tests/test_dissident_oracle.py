"""
Tests del Oráculo Disidente Permanente (Cap. 19) en app/voting_oracle.py.

Cubre:
- El protocolo del disidente: contexto del análisis, postura inicial,
  crítica racional, veredicto final y changed_mind.
- Integración: el análisis base gana una 5ª opinión "Dissident".
- Degradación elegante: si la segunda pasada falla, el análisis base se
  entrega intacto con dissident.available=False.
- El prompt del disidente exige racionalidad sobre el sesgo (no es un
  contreras): "lo que es MEJOR PARA LA COMUNIDAD".
"""

import os

os.environ["SECRET_KEY"] = "test-secret"
os.environ.pop("DEEPSEEK_API_KEY", None)

import pytest

from app import voting_oracle

BASE_ANALYSIS = {
    "vhv": {"vitalTime": 10, "affectedLives": 5, "finiteResources": 50,
            "timeFactor": 1.2, "confidence": 0.8},
    "axiomReport": [{"type": "TRUTH", "passed": True, "score": 80, "reasoning": "ok"}],
    "oracleOpinions": [
        {"role": "Economic", "verdict": "Approve", "analysis": "viable", "confidence": 0.7},
        {"role": "Social", "verdict": "Approve", "analysis": "justa", "confidence": 0.8},
        {"role": "Environmental", "verdict": "Approve", "analysis": "sostenible", "confidence": 0.6},
        {"role": "Futurist", "verdict": "Approve", "analysis": "precavido", "confidence": 0.7},
    ],
}

DISSIDENT_RESULT = {
    "initial_stance": "approve",
    "initial_reasoning": "El consenso de los cuatro oráculos parece sólido.",
    "critique": "Pero la coherencia exige mirar el punto ciego: el impacto en generaciones T+7 y el riesgo de acaparamiento no se han ponderado.",
    "final_verdict": "Modify",
    "changed_mind": True,
    "final_reasoning": "Aunque partí a favor, la crítica racional muestra que la propuesta necesita una cláusula de revisión. Lo mejor para la comunidad es Modify.",
    "confidence": 0.75,
}


def _fresh_base():
    """Copia fresca del análisis base (evita mutaciones entre tests)."""
    import copy
    return copy.deepcopy(BASE_ANALYSIS)


def test_disidente_recibe_contexto_y_cambia_de_opinion(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")
    monkeypatch.setenv("LOCAL_ORACLE_ENABLED", "false")
    calls = []

    def fake_llm(base_url, api_key, model, messages, temperature=0.2, json_mode=True, timeout=120):
        calls.append({"temperature": temperature, "user": messages[-1]["content"][:200]})
        if len(calls) == 1:
            return _fresh_base()
        return DISSIDENT_RESULT

    monkeypatch.setattr(voting_oracle, "_call_llm", fake_llm)
    result = voting_oracle.analyze_proposal("Propuesta X", "Descripción")

    # 5 oráculos: los 4 base + el Disidente
    opinions = result["oracleOpinions"]
    assert len(opinions) == 5
    assert opinions[-1]["role"] == "Dissident"
    assert opinions[-1]["verdict"] == "Modify"

    dissident = result["dissident"]
    assert dissident["initial_stance"] == "approve"
    assert dissident["changed_mind"] is True
    assert "comunidad" in dissident["final_reasoning"]
    assert len(calls) == 2
    # la segunda pasada ve el análisis base como contexto
    assert "ANÁLISIS INICIAL" in calls[1]["user"]


def test_disidente_puede_rectificar_contra_el_consenso(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")
    monkeypatch.setenv("LOCAL_ORACLE_ENABLED", "false")
    contra = dict(DISSIDENT_RESULT)
    contra["initial_stance"] = "reject"
    contra["changed_mind"] = False
    contra["final_verdict"] = "Reject"
    contra["final_reasoning"] = "El consenso apunta a aprobar, pero el examen racional muestra un riesgo fatal para la comunidad."
    calls = []

    def fake_llm(base_url, api_key, model, messages, temperature=0.2, json_mode=True, timeout=120):
        calls.append(True)
        if len(calls) == 1:
            return _fresh_base()
        return contra

    monkeypatch.setattr(voting_oracle, "_call_llm", fake_llm)
    result = voting_oracle.analyze_proposal("Propuesta Y", "Descripción")
    dissident = result["dissident"]
    assert dissident["initial_stance"] == "reject"
    assert dissident["final_verdict"] == "Reject"
    assert dissident["changed_mind"] is False


def test_disidente_falla_y_el_analisis_base_sigue_vivo(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")
    monkeypatch.setenv("LOCAL_ORACLE_ENABLED", "false")
    calls = []

    def fake_llm(base_url, api_key, model, messages, temperature=0.2, json_mode=True, timeout=120):
        calls.append(True)
        if messages[0]["content"] == voting_oracle.SYSTEM_PROMPT:
            return _fresh_base()
        raise RuntimeError("el disidente está caído")

    monkeypatch.setattr(voting_oracle, "_call_llm", fake_llm)
    result = voting_oracle.analyze_proposal("Propuesta Z", "Descripción")

    assert len(result["oracleOpinions"]) == 4
    assert result["dissident"] == {"available": False}
    assert result["engine"] == "deepseek"


def test_prompt_disidente_exige_racionalidad_no_contreras():
    assert "MEJOR PARA LA COMUNIDAD" in voting_oracle.DISSIDENT_SYSTEM_PROMPT
    assert "initial_stance" in voting_oracle.DISSIDENT_SYSTEM_PROMPT
    assert "changed_mind" in voting_oracle.DISSIDENT_SYSTEM_PROMPT
    assert "NO eres un contreras" in voting_oracle.DISSIDENT_SYSTEM_PROMPT


def test_ava_cuatro_validaciones():
    """El AVA (Cap. 14.4) exige Verdad, Temporal, Vital y Recursos."""
    assert "RESOURCES" in voting_oracle.SYSTEM_PROMPT
    assert "TRUTH" in voting_oracle.SYSTEM_PROMPT
    assert "TIME" in voting_oracle.SYSTEM_PROMPT
    assert "LIFE" in voting_oracle.SYSTEM_PROMPT
    assert "TRUTH|TIME|LIFE|RESOURCES" in voting_oracle.SYSTEM_PROMPT


def test_dissident_result_saneado():
    limpio = voting_oracle._clamp_dissident({
        "initial_stance": "otra cosa",
        "initial_reasoning": 42,
        "final_verdict": "RANDOM",
        "changed_mind": "sí",
        "final_reasoning": None,
        "confidence": 99.0,
    })
    assert limpio["initial_stance"] == "undecided"
    assert limpio["final_verdict"] == "Modify"
    assert limpio["changed_mind"] is False
    assert limpio["confidence"] == 1.0
