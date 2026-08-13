# Oracles subpackage for MaxoContracts
from .base import OracleInterface
from .live_oracle import (
    CritiqueResult,
    LiveOracle,
    NegotiationResult,
    OracleAPIError,
    OracleUnavailableError,
)
from .synthetic import SyntheticOracle

__all__ = [
    "OracleInterface",
    "SyntheticOracle",
    "LiveOracle",
    "OracleUnavailableError",
    "OracleAPIError",
    "NegotiationResult",
    "CritiqueResult",
]
