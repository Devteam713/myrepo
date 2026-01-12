"""
Trust Decay Module for Alethia

Manages the degradation of trust scores and context confidence over time,
exposures, or semantic transformations.

Author: Sentenial-X Alethia Core Team
"""

from typing import Dict


class TrustDecay:
    """
    Handles trust decay for a given agent, payload, or context vector.
    """

    def __init__(self, decay_rate: float = 0.05, min_trust: float = 0.0):
        """
        Initialize the TrustDecay model.

        Args:
            decay_rate: Fraction of trust lost per decay step (0 < decay_rate < 1)
            min_trust: Minimum trust allowed after decay
        """
        if not 0 <= decay_rate <= 1:
            raise ValueError("decay_rate must be between 0 and 1")
        if not 0 <= min_trust <= 1:
            raise ValueError("min_trust must be between 0 and 1")

        self.decay_rate = decay_rate
        self.min_trust = min_trust

    def decay_trust(self, trust_score: float) -> float:
        """
        Apply decay to a single trust score.

        Args:
            trust_score: Current trust score (0.0 to 1.0)

        Returns:
            Decayed trust score (>= min_trust)
        """
        decayed = trust_score * (1.0 - self.decay_rate)
        return max(self.min_trust, decayed)

    def decay_context_vector(self, context_vector: Dict[str, float]) -> Dict[str, float]:
        """
        Apply decay to all trust-related signals in a context vector.

        Args:
            context_vector: Dictionary of signal_name -> trust_score

        Returns:
            New dictionary with decayed trust scores
        """
        decayed_vector = {}
        for key, value in context_vector.items():
            decayed_vector[key] = self.decay_trust(value)
        return decayed_vector

    def decay_with_exposure(self, trust_score: float, exposure_count: int) -> float:
        """
        Apply compounded decay based on number of exposures.

        Args:
            trust_score: Original trust score
            exposure_count: Number of times the payload/context has been exposed

        Returns:
            Trust score after compounded decay
        """
        decayed = trust_score
        for _ in range(exposure_count):
            decayed = self.decay_trust(decayed)
        return decayed
