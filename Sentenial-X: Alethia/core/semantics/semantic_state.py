"""
Alethia Semantic State

Central data model for Alethia semantic layer.

Tracks the lifecycle of sensitive content:
- Original and current payloads
- Semantic degradation and entropy levels
- Context vector and trust scoring
- Exposure counts and resolution state

Provides interfaces for:
- Encoding
- Decoding
- Dynamic resolution
- SDK integration

Author: Sentenial-X Alethia Core Team
"""

from typing import Dict, Any


class SemanticState:
    """
    Tracks all semantic properties for a single data object.
    """

    VALID_STATES = {"degraded", "authorized", "unknown"}

    def __init__(
        self,
        data_id: str,
        initial_payload: str,
        context_vector: Dict[str, float] = None,
        trust_score: float = 0.0,
        decay_factor: float = 0.0
    ):
        self.data_id = data_id
        self.initial_payload = initial_payload
        self.current_payload = initial_payload
        self.context_vector = context_vector if context_vector else {}
        self.trust_score = trust_score
        self.decay_factor = decay_factor  # 0.0 = no degradation, 1.0 = max degradation
        self.exposure_count = 0
        self.resolution_state = "unknown"

    def increment_exposure(self) -> None:
        """Increment the exposure count when the payload is processed."""
        self.exposure_count += 1

    def update_payload(self, new_payload: str, decay_factor: float = None) -> None:
        """
        Update the current payload and optionally the decay factor.

        Args:
            new_payload: The transformed payload
            decay_factor: Optional new semantic degradation level
        """
        self.current_payload = new_payload
        if decay_factor is not None:
            if not (0.0 <= decay_factor <= 1.0):
                raise ValueError("Decay factor must be between 0.0 and 1.0")
            self.decay_factor = decay_factor
        self.increment_exposure()

    def set_resolution_state(self, state: str) -> None:
        """
        Set the resolution state.

        Args:
            state: One of "degraded", "authorized", "unknown"
        """
        if state not in self.VALID_STATES:
            raise ValueError(f"Invalid resolution state: {state}")
        self.resolution_state = state

    def update_trust(self, trust_score: float) -> None:
        """
        Update the trust score of this payload.

        Args:
            trust_score: float between 0.0 and 1.0
        """
        if not (0.0 <= trust_score <= 1.0):
            raise ValueError("Trust score must be between 0.0 and 1.0")
        self.trust_score = trust_score

    def update_context(self, new_context: Dict[str, float]) -> None:
        """
        Merge new context signals into the existing context vector.

        Args:
            new_context: Dictionary of context key-value pairs
        """
        self.context_vector.update(new_context)

    def reset_state(self) -> None:
        """
        Reset the payload to its initial state.
        Useful for testing or re-encoding.
        """
        self.current_payload = self.initial_payload
        self.decay_factor = 0.0
        self.resolution_state = "unknown"
        self.exposure_count = 0

    def snapshot(self) -> Dict[str, Any]:
        """
        Return a full snapshot of the semantic state for logging, telemetry, or SDK consumption.
        """
        return {
            "data_id": self.data_id,
            "initial_payload": self.initial_payload,
            "current_payload": self.current_payload,
            "context_vector": self.context_vector,
            "trust_score": self.trust_score,
            "decay_factor": self.decay_factor,
            "exposure_count": self.exposure_count,
            "resolution_state": self.resolution_state
        }

    def is_authorized(self, threshold: float = 0.75) -> bool:
        """
        Check if the payload is in an authorized context.

        Args:
            threshold: Minimum trust_score to consider authorized

        Returns:
            True if authorized, False otherwise
        """
        return self.trust_score >= threshold
