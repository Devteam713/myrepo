"""
Trust Engine for Alethia

Coordinates trust computation using context vectors, confidence models,
and trust decay mechanisms to guide semantic resolution and adaptive
linguistic entropy.

Author: Sentenial-X Alethia Core Team
"""

from typing import Dict
from .confidence_model import ConfidenceModel
from .trust_decay import TrustDecay


class TrustEngine:
    """
    Main orchestrator for evaluating, updating, and maintaining trust scores
    for payloads, agents, or contexts within Alethia.
    """

    def __init__(self,
                 weights: Dict[str, float] = None,
                 decay_rate: float = 0.05,
                 min_trust: float = 0.0):
        """
        Initialize the TrustEngine.

        Args:
            weights (dict): Context key weights for confidence scoring
            decay_rate (float): Default per-step trust decay
            min_trust (float): Minimum trust value allowed
        """
        self.confidence_model = ConfidenceModel(weights)
        self.trust_decay = TrustDecay(decay_rate=decay_rate, min_trust=min_trust)

    def evaluate_trust(self, context_vector: Dict[str, float]) -> float:
        """
        Compute a composite trust score for a given context vector.

        Args:
            context_vector (dict): Signals such as auth_confidence, agent_trust, environment

        Returns:
            float: Normalized trust score (0.0 - 1.0)
        """
        # Step 1: Compute initial confidence
        confidence = self.confidence_model.compute_confidence(context_vector)

        # Step 2: Apply standard decay
        trust_score = self.trust_decay.decay_trust(confidence)

        return trust_score

    def update_context_trust(self, context_vector: Dict[str, float]) -> Dict[str, float]:
        """
        Apply decay to an entire context vector to reflect trust changes over time.

        Args:
            context_vector (dict): Original context vector

        Returns:
            dict: Decayed context vector
        """
        return self.trust_decay.decay_context_vector(context_vector)

    def evaluate_trust_with_exposure(self, context_vector: Dict[str, float], exposure_count: int) -> float:
        """
        Compute a trust score considering repeated exposures or semantic events.

        Args:
            context_vector (dict): Original context vector
            exposure_count (int): Number of exposures

        Returns:
            float: Trust score after compounded decay
        """
        initial_confidence = self.confidence_model.compute_confidence(context_vector)
        return self.trust_decay.decay_with_exposure(initial_confidence, exposure_count)

    def dynamic_trust_update(self, context_vector: Dict[str, float], dynamic_rate: float) -> Dict[str, float]:
        """
        Apply decay with a dynamic rate to all elements in a context vector.

        Args:
            context_vector (dict): Original context vector
            dynamic_rate (float): Decay rate (0-1), e.g., from risk scoring

        Returns:
            dict: Updated context vector
        """
        return {k: self.trust_decay.decay_with_dynamic_rate(v, dynamic_rate)
                for k, v in context_vector.items()}

    def set_weights(self, new_weights: Dict[str, float]):
        """
        Update confidence model weights dynamically.

        Args:
            new_weights (dict): Mapping context keys to new weights
        """
        self.confidence_model.update_weights(new_weights)
