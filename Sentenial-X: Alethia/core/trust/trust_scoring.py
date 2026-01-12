"""
Trust Scoring Module for Alethia

Computes normalized trust scores based on context vectors, agent reliability,
and environmental factors. Designed to feed semantic resolution, entropy control,
and post-exfiltration survivability mechanisms.

Author: Sentenial-X Alethia Core Team
"""

from typing import Dict


class TrustScoring:
    """
    Computes composite trust scores for Alethia's context and semantic layers.
    """

    def __init__(self, weights: Dict[str, float] = None):
        """
        Initialize the TrustScoring module.

        Args:
            weights (dict): Optional weights for each context signal.
                            Default is equal weighting.
        """
        self.weights = weights or {}

    def compute_score(self, context_vector: Dict[str, float]) -> float:
        """
        Compute a composite trust score from a context vector.

        Args:
            context_vector (dict): Dictionary of context signals (0.0-1.0)

        Returns:
            float: Normalized trust score (0.0-1.0)
        """
        if not context_vector:
            return 0.0

        # Determine weights
        total_weight = sum(self.weights.values()) if self.weights else len(context_vector)
        if total_weight == 0:
            total_weight = 1.0  # Avoid division by zero

        score = 0.0
        for key, value in context_vector.items():
            weight = self.weights.get(key, 1.0)
            score += value * weight

        return min(1.0, max(0.0, score / total_weight))

    def update_weights(self, new_weights: Dict[str, float]):
        """
        Update the signal weights dynamically.

        Args:
            new_weights (dict): Key -> weight mapping
        """
        self.weights.update(new_weights)

    def evaluate_authorization_confidence(self, context_vector: Dict[str, float], threshold: float = 0.5) -> bool:
        """
        Determine if the context meets an authorization threshold.

        Args:
            context_vector (dict): Context signals
            threshold (float): Minimum trust score required

        Returns:
            bool: True if trust score >= threshold, False otherwise
        """
        score = self.compute_score(context_vector)
        return score >= threshold

    def weighted_signal_scores(self, context_vector: Dict[str, float]) -> Dict[str, float]:
        """
        Return each context signal multiplied by its weight.

        Args:
            context_vector (dict): Context signals

        Returns:
            dict: Key -> weighted score
        """
        weighted_scores = {}
        for key, value in context_vector.items():
            weight = self.weights.get(key, 1.0)
            weighted_scores[key] = value * weight
        return weighted_scores
