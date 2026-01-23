# Oracle API Specification

## Overview
This document defines the interface for **Synthetic Oracles** (AI Agents) and **Human Oracles** to interact with the Maxocracia system. Oracles are responsible for validating contracts, mediating retractions, and estimating VHV impact.

## Protocol
- **Transport**: JSON over HTTPS (internal) or structured prompts (LLM integration).
- **Authentication**: Signed requests using JWT + HMAC.

## Data Structures

### 1. Oracle Query (Request)
Sent *to* the Oracle.

```json
{
  "query_id": "uuid-v4",
  "query_type": "contract_validation | retraction_evaluation | impact_estimation",
  "requester_id": "user-123",
  "submitted_at": "ISO8601",
  "context": {
    // Differs by query_type
  }
}
```

#### Context: Contract Validation
```json
{
  "contract_id": "c-001",
  "civil_text": "Alice pays 10 Maxos to Bob...",
  "terms": [
    { "id": "t1", "vhv": {"T": 10, "V": 0, "R": 0}, "text": "Transfer..." }
  ],
  "participants": [
    { "id": "user-a", "wellness": 1.2 },
    { "id": "user-b", "wellness": 1.0 }
  ]
}
```

#### Context: Retraction Evaluation
```json
{
  "contract_id": "c-001",
  "reason": "Medical emergency",
  "evidence": {
    "document_url": "...",
    "current_wellness": 0.8
  }
}
```

### 2. Oracle Response
Received *from* the Oracle.

```json
{
  "query_id": "uuid-v4-matching-request",
  "oracle_id": "claude-3-opus | human-jury-1",
  "verdict": {
    "approved": true,
    "confidence": 0.95, // 0.0 - 1.0
    "reasoning": "The contract violates Axiom T1 (Finitude)..."
  },
  "metadata": {
    "processing_time_ms": 1500,
    "model_version": "v1.2"
  },
  "signature": "hmac-sha256-signature"
}
```

## Interfaces

### Python Interface (`maxocontracts.oracles.base.OracleInterface`)
The existing Python abstraction must support async adapter implementations for these external calls.

```python
class OracleInterface(ABC):
    async def validate_contract(self, contract: Dict) -> OracleResponse: ...
    async def evaluate_retraction(self, query: Dict) -> OracleResponse: ...
```

## Security
1.  **Non-Repudiation**: Oracles must sign their verdicts (for human juries). Synthetic oracles provide a cryptographic proof of inference (if available) or a system signature.
2.  **Audit Log**: All queries and responses are immutable (recorded in `maxo_contract_events`).

## Integration Strategy (MVP)
For the MVP, we will implement `SyntheticOracle` using this schema but mocking the actual LLM call, preparing the system for the real API integration in Q2.
