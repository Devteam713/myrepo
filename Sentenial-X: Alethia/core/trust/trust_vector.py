"""
Trust Vector Module for Alethia

Defines the data structure and operations for context-based trust vectors.
These vectors are the primary input to trust scoring, decay, and semantic
resolution in Alethia.

Author: Sentenial-X Alethia Core Team
"""

from typing import Dict


class TrustVector:
    """
    Represents a context-aware trust vector.
    Each key corresponds to a signal such as auth confidence, agent reliability,
    or environmental trust. Values are floats between 0.0 and 1.0.
    """

    def __init__(self, signals: Dict[str, float] = None):
        """
        Initialize the trust vector.

        Args:
            signals (dict): Optional initial signals
        """
        self.signals = signals or {}

        # Validate all signals
        for key, value in self.signals.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"Trust signal '{key}' must be between 0 and 1")

    def update_signal(self, key: str, value: float):
        """
        Update or add a signal to the trust vector.

        Args:
            key (str): Signal name
            value (float): Trust value (0.0 - 1.0)
        """
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"Trust signal '{key}' must be between 0 and 1")
        self.signals[key] = value

    def get_signal(self, key: str) -> float:
        """
        Retrieve a signal value.

        Args:
            key (str): Signal name

        Returns:
            float: Trust value (0.0 - 1.0), 0.0 if missing
        """
        return self.signals.get(key, 0.0)

    def normalize(self):
        """
        Normalize all signal values to be within [0,1].
        Useful after updates or transformations.
        """
        for key in self.signals:
            self.signals[key] = max(0.0, min(1.0, self.signals[key]))

    def as_dict(self) -> Dict[str, float]:
        """
        Return a dictionary representation of the trust vector.

        Returns:
            dict: Signal -> value
        """
        return self.signals.copy()

    def weighted_score(self, weights: Dict[str, float] = None) -> float:
        """
        Compute a weighted trust score for the vector.

        Args:
            weights (dict): Optional weights per signal. Defaults to equal weighting.

        Returns:
            float: Weighted normalized score between 0.0 and 1.0
        """
        if not self.signals:
            return 0.0

        total_weight = sum(weights.values()) if weights else len(self.signals)
        if total_weight == 0:
            total_weight = 1.0

        score = 0.0
        for key, value in self.signals.items():
            weight = weights.get(key, 1.0) if weights else 1.0
            score += value * weight

        return min(1.0, max(0.0, score / total_weight))

    def decay(self, decay_rate: float, min_trust: float = 0.0):
        """
        Apply uniform decay to all signals.

        Args:
            decay_rate (float): Fractional decay per step (0-1)
            min_trust (float): Minimum trust floor
        """
        for key, value in self.signals.items():
            decayed = value * (1.0 - decay_rate)
            self.signals[key] = max(min_trust, decayed)

    def __repr__(self):
        return f"TrustVector({self.signals})"

    def __getitem__(self, key):
        return self.get_signal(key)

    def __setitem__(self, key, value):
        self.update_signal(key, value)
