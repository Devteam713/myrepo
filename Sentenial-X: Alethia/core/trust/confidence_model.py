"""
Confidence Model for Alethia Trust Layer

Evaluates contextual and agent-based trust scores to guide semantic
resolution decisions.

Author: Sentenial-X Alethia Core Team
"""

from typing import Dict


class ConfidenceModel:
    """
    Models trust/confidence for a given payload or agent context.

    Combines multiple contextual signals into a composite confidence score.
    """

    def __init__(self, weights: Dict[str, float] = None):
        """
        Initialize the confidence model with optional weights.

        Args:
            weights: Optional dictionary mapping context keys to their weight in scoring.
                     Defaults to equal weighting.
        """
        self.weights = weights if weights else {}
        self.MIN_SCORE = 0.0
        self.MAX_SCORE = 1.0

    def compute_confidence(self, context_vector: Dict[str, float]) -> float:
        """
        Compute a normalized confidence score from a context vector.

        Args:
            context_vector: Dictionary of signals (e.g., auth_confidence, agent_trust, environment)

        Returns:
            A float between 0.0 and 1.0 representing the overall trust/confidence.
        """
        if not context_vector:
            return 0.0

        # If no weights defined, assume equal weighting
        if not self.weights:
            self.weights = {k: 1.0 for k in context_vector}

        total_weight = sum(self.weights.get(k, 0.0) for k in context_vector)
        if total_weight == 0:
            return 0.0

        score = sum(context_vector.get(k, 0.0) * self.weights.get(k, 0.0)
                    for k in context_vector) / total_weight

        # Clamp between 0.0 and 1.0
        return max(self.MIN_SCORE, min(self.MAX_SCORE, score))

    def update_weights(self, new_weights: Dict[str, float]):
        """
        Update the context weights dynamically.

        Args:
            new_weights: Dict of context keys and updated weights
        """
        self.weights.update(new_weights)

    def normalize_signal(self, value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
        """
        Normalize a single signal to [0,1] range.

        Args:
            value: Signal value
            min_val: Minimum possible value
            max_val: Maximum possible value

        Returns:
            Normalized value between 0.0 and 1.0
        """
        if max_val == min_val:
            return 0.0
        return max(0.0, min(1.0, (value - min_val) / (max_val - min_val)))
