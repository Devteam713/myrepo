"""
Trust Decay Module

Manages trust degradation over time, exposure, and semantic transformations
to support post-exfiltration survivability in Alethia.

Author: Sentenial-X Alethia Core Team
"""

from typing import Dict


class TrustDecay:
    """
    Handles decay of trust scores for agents, payloads, and context vectors.
    Decay can occur over time, repeated exposures, or semantic events.
    """

    def __init__(self, decay_rate: float = 0.05, min_trust: float = 0.0):
        """
        Initialize the TrustDecay model.

        Args:
            decay_rate (float): Fraction of trust lost per decay step (0 < decay_rate < 1)
            min_trust (float): Minimum allowed trust after decay
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
            trust_score (float): Current trust value (0.0 - 1.0)

        Returns:
            float: Decayed trust value (>= min_trust)
        """
        decayed = trust_score * (1.0 - self.decay_rate)
        return max(self.min_trust, decayed)

    def decay_context_vector(self, context_vector: Dict[str, float]) -> Dict[str, float]:
        """
        Apply decay to all trust-related signals in a context vector.

        Args:
            context_vector (dict): Key -> trust score

        Returns:
            dict: New context vector with decayed trust values
        """
        return {k: self.decay_trust(v) for k, v in context_vector.items()}

    def decay_with_exposure(self, trust_score: float, exposure_count: int) -> float:
        """
        Apply compounded decay based on repeated exposures or semantic events.

        Args:
            trust_score (float): Original trust score
            exposure_count (int): Number of exposures or semantic events

        Returns:
            float: Trust score after compounded decay
        """
        decayed = trust_score
        for _ in range(exposure_count):
            decayed = self.decay_trust(decayed)
        return decayed

    def decay_with_dynamic_rate(self, trust_score: float, dynamic_rate: float) -> float:
        """
        Apply decay using a dynamic rate (e.g., based on context risk scoring).

        Args:
            trust_score (float): Current trust score
            dynamic_rate (float): Decay rate between 0 and 1

        Returns:
            float: Decayed trust score
        """
        if not 0 <= dynamic_rate <= 1:
            raise ValueError("dynamic_rate must be between 0 and 1")
        decayed = trust_score * (1.0 - dynamic_rate)
        return max(self.min_trust, decayed)
