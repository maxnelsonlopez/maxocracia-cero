"""
Tests comprehensivos para Oracle API
Valida conformidad con docs/specs/ORACLE_API_SPEC.md v1.0
"""

import pytest
from decimal import Decimal
from datetime import datetime
import uuid

from maxocontracts.oracles.base import (
    OracleQuery,
    OracleResponse,
    Verdict,
    OracleInterface
)
from maxocontracts.oracles.synthetic import SyntheticOracle


class TestOracleDataStructures:
    """Tests para estructuras de datos del Oracle API."""
    
    def test_verdict_creation(self):
        """Test creación de Verdict."""
        verdict = Verdict(
            approved=True,
            confidence=Decimal("0.95"),
            reasoning="Contract meets all axioms"
        )
        
        assert verdict.approved is True
        assert verdict.confidence == Decimal("0.95")
        assert "axioms" in verdict.reasoning
    
    def test_verdict_to_dict(self):
        """Test serialización de Verdict a dict."""
        verdict = Verdict(
            approved=False,
            confidence=Decimal("0.85"),
            reasoning="Violates T1 (Finitude)"
        )
        
        data = verdict.to_dict()
        
        assert data["approved"] is False
        assert data["confidence"] == 0.85  # Convertido a float
        assert "T1" in data["reasoning"]
    
    def test_oracle_query_creation(self):
        """Test creación de OracleQuery."""
        query_id = str(uuid.uuid4())
        now = datetime.now()
        
        query = OracleQuery(
            query_id=query_id,
            query_type="contract_validation",
            context={"contract_id": "c-001"},
            submitted_at=now,
            requester_id="user-123"
        )
        
        assert query.query_id == query_id
        assert query.query_type == "contract_validation"
        assert query.context["contract_id"] == "c-001"
        assert query.requester_id == "user-123"
    
    def test_oracle_query_to_dict(self):
        """Test serialización de OracleQuery."""
        query = OracleQuery(
            query_id="test-123",
            query_type="retraction_evaluation",
            context={"reason": "emergency"},
            submitted_at=datetime(2026, 1, 23, 4, 0, 0),
            requester_id="user-456"
        )
        
        data = query.to_dict()
        
        assert data["query_id"] == "test-123"
        assert data["query_type"] == "retraction_evaluation"
        assert data["requester_id"] == "user-456"
        assert "2026-01-23" in data["submitted_at"]
        assert data["context"]["reason"] == "emergency"
    
    def test_oracle_response_creation(self):
        """Test creación de OracleResponse."""
        verdict = Verdict(
            approved=True,
            confidence=Decimal("0.9"),
            reasoning="Valid"
        )
        
        response = OracleResponse(
            query_id="q-001",
            oracle_id="synthetic-v1",
            verdict=verdict,
            metadata={"processing_time_ms": 150},
            signature="sig-abc123"
        )
        
        assert response.query_id == "q-001"
        assert response.oracle_id == "synthetic-v1"
        assert response.verdict.approved is True
        assert response.metadata["processing_time_ms"] == 150
        assert response.signature == "sig-abc123"
    
    def test_oracle_response_approved_property(self):
        """Test helper property 'approved' en OracleResponse."""
        verdict_approved = Verdict(True, Decimal("0.9"), "OK")
        verdict_rejected = Verdict(False, Decimal("0.8"), "Not OK")
        
        response_approved = OracleResponse("q1", "oracle1", verdict_approved)
        response_rejected = OracleResponse("q2", "oracle2", verdict_rejected)
        
        assert response_approved.approved is True
        assert response_rejected.approved is False
    
    def test_oracle_response_to_dict(self):
        """Test serialización completa de OracleResponse."""
        verdict = Verdict(False, Decimal("0.75"), "Insufficient evidence")
        response = OracleResponse(
            query_id="q-999",
            oracle_id="claude-3-opus",
            verdict=verdict,
            metadata={"model_version": "v1.2"},
            signature="hmac-sha256-xyz"
        )
        
        data = response.to_dict()
        
        assert data["query_id"] == "q-999"
        assert data["oracle_id"] == "claude-3-opus"
        assert data["verdict"]["approved"] is False
        assert data["verdict"]["confidence"] == 0.75
        assert data["verdict"]["reasoning"] == "Insufficient evidence"
        assert data["metadata"]["model_version"] == "v1.2"
        assert data["signature"] == "hmac-sha256-xyz"


class TestSyntheticOracle:
    """Tests para SyntheticOracle implementation."""
    
    def test_oracle_initialization(self):
        """Test inicialización del oráculo sintético."""
        oracle = SyntheticOracle(mode="simulation")
        
        assert oracle.mode == "simulation"
        assert oracle.oracle_id == "synthetic-v1-sim"
        assert oracle.get_oracle_type() == "synthetic"
        assert len(oracle._query_log) == 0
        assert len(oracle._response_log) == 0
    
    def test_validate_contract_valid(self):
        """Test validación de contrato válido."""
        oracle = SyntheticOracle()
        
        contract_data = {
            "contract_id": "c-001",
            "terms": [
                {"id": "t1", "vhv": {"T": 10, "V": 0, "R": 0}}
            ],
            "participants": [
                {"id": "user-a", "wellness": 1.2},
                {"id": "user-b", "wellness": 1.0}
            ]
        }
        
        response = oracle.validate_contract(contract_data)
        
        assert isinstance(response, OracleResponse)
        assert response.oracle_id == "synthetic-v1-sim"
        assert response.verdict.approved is True
        assert "válido" in response.verdict.reasoning.lower()
        assert response.verdict.confidence == Decimal("0.9")
        
        # Verificar logging
        assert len(oracle._query_log) == 1
        assert len(oracle._response_log) == 1
        assert oracle._query_log[0].query_type == "contract_validation"
    
    def test_validate_contract_no_terms(self):
        """Test validación rechaza contrato sin términos."""
        oracle = SyntheticOracle()
        
        contract_data = {
            "contract_id": "c-002",
            "terms": [],  # Sin términos
            "participants": [
                {"id": "user-a", "wellness": 1.0},
                {"id": "user-b", "wellness": 1.0}
            ]
        }
        
        response = oracle.validate_contract(contract_data)
        
        assert response.verdict.approved is False
        assert "términos" in response.verdict.reasoning.lower()
    
    def test_validate_contract_insufficient_participants(self):
        """Test validación rechaza contrato con menos de 2 participantes."""
        oracle = SyntheticOracle()
        
        contract_data = {
            "contract_id": "c-003",
            "terms": [{"id": "t1", "vhv": {"T": 5, "V": 0, "R": 0}}],
            "participants": [{"id": "user-a", "wellness": 1.0}]  # Solo 1
        }
        
        response = oracle.validate_contract(contract_data)
        
        assert response.verdict.approved is False
        assert "participantes" in response.verdict.reasoning.lower()
    
    def test_evaluate_retraction_approved(self):
        """Test evaluación de retractación aprobada por crisis de wellness."""
        oracle = SyntheticOracle()
        
        response = oracle.evaluate_retraction(
            contract_id="c-100",
            reason="gamma_crisis detected",
            evidence={
                "current_wellness": 0.7,
                "requester_id": "user-x"
            }
        )
        
        assert isinstance(response, OracleResponse)
        assert response.verdict.approved is True
        assert "wellness" in response.verdict.reasoning.lower()
        assert response.verdict.confidence == Decimal("0.9")
        
        # Verificar logging
        assert len(oracle._query_log) == 1
        assert oracle._query_log[0].query_type == "retraction_evaluation"
    
    def test_evaluate_retraction_rejected(self):
        """Test evaluación de retractación rechazada."""
        oracle = SyntheticOracle()
        
        response = oracle.evaluate_retraction(
            contract_id="c-101",
            reason="I changed my mind",
            evidence={"requester_id": "user-y"}
        )
        
        assert response.verdict.approved is False
        assert response.verdict.confidence == Decimal("0.7")
    
    def test_estimate_gamma_impact_high_suffering(self):
        """Test estimación de impacto negativo con alto sufrimiento."""
        oracle = SyntheticOracle()
        
        impact = oracle.estimate_gamma_impact(
            action_data={"vhv_cost": {"V": 0.6}},
            participant_data={"current_gamma": 1.2}
        )
        
        assert impact == Decimal("-0.1")
    
    def test_estimate_gamma_impact_medium_suffering(self):
        """Test estimación de impacto con sufrimiento medio."""
        oracle = SyntheticOracle()
        
        impact = oracle.estimate_gamma_impact(
            action_data={"vhv_cost": {"V": 0.3}},
            participant_data={"current_gamma": 1.0}
        )
        
        assert impact == Decimal("-0.05")
    
    def test_estimate_gamma_impact_low_suffering(self):
        """Test estimación de impacto positivo con bajo sufrimiento."""
        oracle = SyntheticOracle()
        
        impact = oracle.estimate_gamma_impact(
            action_data={"vhv_cost": {"V": 0.05}},
            participant_data={"current_gamma": 1.1}
        )
        
        assert impact == Decimal("0.02")
    
    def test_query_response_matching(self):
        """Test que query_id coincide entre query y response."""
        oracle = SyntheticOracle()
        
        contract_data = {
            "terms": [{"id": "t1"}],
            "participants": [{"id": "u1"}, {"id": "u2"}]
        }
        
        response = oracle.validate_contract(contract_data)
        query = oracle._query_log[0]
        
        assert response.query_id == query.query_id
    
    def test_signature_generation(self):
        """Test que todas las respuestas tienen firma."""
        oracle = SyntheticOracle()
        
        response = oracle.validate_contract({
            "terms": [{"id": "t1"}],
            "participants": [{"id": "u1"}, {"id": "u2"}]
        })
        
        assert response.signature is not None
        assert response.signature.startswith("sim-sig-")
    
    def test_metadata_in_responses(self):
        """Test que responses incluyen metadata."""
        oracle = SyntheticOracle()
        
        # Validación
        response1 = oracle.validate_contract({
            "terms": [{"id": "t1"}],
            "participants": [{"id": "u1"}, {"id": "u2"}]
        })
        assert "simulation_engine" in response1.metadata
        
        # Retractación
        response2 = oracle.evaluate_retraction(
            "c-001",
            "reason",
            {"key": "value"}
        )
        assert "evidence_points" in response2.metadata
    
    def test_api_mode_not_implemented(self):
        """Test que modo API lanza NotImplementedError."""
        oracle = SyntheticOracle(mode="api")
        
        with pytest.raises(NotImplementedError):
            oracle.validate_contract({"terms": [], "participants": []})
        
        with pytest.raises(NotImplementedError):
            oracle.evaluate_retraction("c-001", "reason", {})
        
        with pytest.raises(NotImplementedError):
            oracle.estimate_gamma_impact({}, {})


class TestOracleAPISpecCompliance:
    """Tests de conformidad con ORACLE_API_SPEC.md."""
    
    def test_query_types_supported(self):
        """Test que se soportan los 3 tipos de query especificados."""
        oracle = SyntheticOracle()
        
        # contract_validation
        oracle.validate_contract({
            "terms": [{"id": "t1"}],
            "participants": [{"id": "u1"}, {"id": "u2"}]
        })
        assert oracle._query_log[-1].query_type == "contract_validation"
        
        # retraction_evaluation
        oracle.evaluate_retraction("c-001", "reason", {})
        assert oracle._query_log[-1].query_type == "retraction_evaluation"
    
    def test_confidence_range(self):
        """Test que confidence está en rango [0.0, 1.0]."""
        oracle = SyntheticOracle()
        
        # Validación
        r1 = oracle.validate_contract({
            "terms": [{"id": "t1"}],
            "participants": [{"id": "u1"}, {"id": "u2"}]
        })
        assert Decimal("0") <= r1.verdict.confidence <= Decimal("1")
        
        # Retractación
        r2 = oracle.evaluate_retraction("c-001", "reason", {})
        assert Decimal("0") <= r2.verdict.confidence <= Decimal("1")
    
    def test_response_structure_complete(self):
        """Test que OracleResponse tiene todos los campos requeridos."""
        oracle = SyntheticOracle()
        
        response = oracle.validate_contract({
            "terms": [{"id": "t1"}],
            "participants": [{"id": "u1"}, {"id": "u2"}]
        })
        
        data = response.to_dict()
        
        # Campos requeridos según spec
        assert "query_id" in data
        assert "oracle_id" in data
        assert "verdict" in data
        assert "metadata" in data
        assert "signature" in data
        
        # Estructura de verdict
        assert "approved" in data["verdict"]
        assert "confidence" in data["verdict"]
        assert "reasoning" in data["verdict"]
    
    def test_audit_log_immutability(self):
        """Test que query/response logs son append-only."""
        oracle = SyntheticOracle()
        
        # Primera operación
        oracle.validate_contract({
            "terms": [{"id": "t1"}],
            "participants": [{"id": "u1"}, {"id": "u2"}]
        })
        
        log_size_1 = len(oracle._query_log)
        
        # Segunda operación
        oracle.evaluate_retraction("c-001", "reason", {})
        
        log_size_2 = len(oracle._query_log)
        
        # Logs crecen monotónicamente
        assert log_size_2 == log_size_1 + 1
        assert len(oracle._response_log) == 2
