# Oracles subpackage for MaxoContracts
from .base import OracleInterface
from .synthetic import SyntheticOracle
from .live_oracle import (
    LiveOracle,
    OracleUnavailableError,
    OracleAPIError,
    NegotiationResult,
    CritiqueResult,
)

__all__ = [
    "OracleInterface",
    "SyntheticOracle",
    "LiveOracle",
    "OracleUnavailableError",
    "OracleAPIError",
    "NegotiationResult",
    "CritiqueResult",
]
