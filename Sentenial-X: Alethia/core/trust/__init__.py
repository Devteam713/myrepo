"""
Alethia Trust Package

Manages trust scoring, decay, and vector evaluation for semantic payloads.

Components:
- TrustVector: Represents contextual trust metrics
- TrustDecay: Handles trust degradation over time or exposures
- TrustScoring: Calculates composite trust for authorization decisions

Author: Sentenial-X Alethia Core Team
"""

from .trust_vector import TrustVector
from .trust_decay import TrustDecay
from .trust_scoring import TrustScoring

# Explicitly define top-level exports
__all__ = [
    "TrustVector",
    "TrustDecay",
    "TrustScoring"
]
