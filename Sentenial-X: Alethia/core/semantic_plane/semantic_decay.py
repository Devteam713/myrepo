"""
Alethia Semantic Decay Module

Implements time- and exposure-based semantic decay to reduce
the operational utility of data for unauthorized users.

Responsibilities:
- Apply progressive semantic degradation
- Integrate with trust and context signals
- Support exposure- or iteration-based decay strategies
- Maintain syntactic plausibility for degraded content

Author: Sentenial-X Alethia Core Team
"""

from typing import Dict, Any
from core.resolution.degradation import DegradationEngine
import math


class SemanticDecay:
    """
    Applies decay functions to semantic payloads.
    """

    def __init__(self, base_decay: float = 0.1, max_passes: int = 5):
        """
        Args:
            base_decay: Base fraction of degradation applied per exposure/iteration
            max_passes: Maximum degradation iterations allowed
        """
        self.base_decay = base_decay
        self.max_passes = max_passes
        self.degradation_engine = DegradationEngine(max_iterations=max_passes)

    def decay_payload(self, payload: str, context_vector: Dict[str, Any], exposure_count: int = 1) -> str:
        """
        Apply semantic decay based on exposure count and context.

        Args:
            payload: Original or partially degraded payload
            context_vector: Dictionary with context signals, e.g. auth_confidence
            exposure_count: Number of times payload has been exposed/accessed

        Returns:
            Decayed payload string
        """
        trust_score = context_vector.get("auth_confidence", 0.0)
        agent_trust = context_vector.get("agent_trust", 0.0)

        # Effective trust combines signals (lower trust → stronger decay)
        effective_trust = max(0.0, min(1.0, 0.5 * (trust_score + agent_trust)))

        # Compute decay intensity: lower trust and higher exposure → stronger decay
        decay_factor = self._compute_decay_factor(effective_trust, exposure_count)

        # Apply degradation using DegradationEngine
        return self.degradation_engine.degrade(payload, decay_factor)

    def _compute_decay_factor(self, trust_score: float, exposure_count: int) -> float:
        """
        Maps trust and exposure to degradation intensity in [0,1].

        Lower trust and higher exposure → higher degradation intensity.

        Args:
            trust_score: Float [0,1]
            exposure_count: Integer

        Returns:
            Decay intensity [0,1]
        """
        # Exponential decay formula: decay increases with exposure
        decay_intensity = min(1.0, (1 - trust_score) * (1 - math.exp(-self.base_decay * exposure_count)))
        return decay_intensity
