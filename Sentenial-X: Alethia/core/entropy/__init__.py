"""
Alethia Core Entropy Package

Responsible for controlling adaptive semantic entropy:
- Modulates content intelligibility based on context and trust
- Provides dynamic, content-aware degradation mechanisms
- Implements linguistic and probabilistic transformations to prevent unauthorized reconstruction

Modules:
- adaptive_profiles: Predefined and dynamic entropy profiles for different contexts
- entropy_engine: Core engine controlling entropy levels and transformations
- linguistic_entropy: Functions for synonym drift, polysemy injection, and semantic noise
"""

# Expose key classes/functions at the package level
from .adaptive_profiles import AdaptiveProfileManager
from .entropy_engine import EntropyEngine
from .linguistic_entropy import LinguisticEntropy

__all__ = [
    "AdaptiveProfileManager",
    "EntropyEngine",
    "LinguisticEntropy",
]
