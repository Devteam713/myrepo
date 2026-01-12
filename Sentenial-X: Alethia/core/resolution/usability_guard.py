"""
Alethia Usability Guard

Ensures authorized users maintain operational usability of Alethia-protected data
while enforcing degradation for unauthorized users.

Responsibilities:
- Measure semantic usability
- Apply corrective adjustments to avoid over-degradation
- Integrate with ResolutionEngine and PolicyEngine
- Support post-exfiltration semantic survivability

Author: Sentenial-X Alethia Core Team
"""

from typing import Dict, Any


class UsabilityGuard:
    """
    Monitors and enforces usability thresholds on semantic payloads.
    """

    def __init__(self, min_usability_threshold: float = 0.85):
        """
        Args:
            min_usability_threshold: Minimum usability value for authorized users [0,1]
        """
        self.min_usability_threshold = min_usability_threshold

    def assess_usability(self, payload: str, reference_payload: str) -> float:
        """
        Assess semantic usability by comparing transformed payload to reference payload.

        Args:
            payload: Current payload string (post-transformation)
            reference_payload: Original payload string

        Returns:
            Usability score in [0,1] (1 = fully usable)
        """
        if not payload or not reference_payload:
            return 0.0

        # Simple heuristic: fraction of shared words
        ref_tokens = set(reference_payload.lower().split())
        payload_tokens = set(payload.lower().split())
        overlap = ref_tokens.intersection(payload_tokens)
        score = len(overlap) / max(len(ref_tokens), 1)
        return min(max(score, 0.0), 1.0)

    def enforce_usability(self, payload: str, reference_payload: str, trust_score: float) -> str:
        """
        Ensure usability for authorized users.

        Args:
            payload: Current payload string
            reference_payload: Original payload string
            trust_score: Float [0,1]

        Returns:
            Payload adjusted to meet usability threshold if necessary
        """
        if trust_score >= 0.8:
            usability = self.assess_usability(payload, reference_payload)
            if usability < self.min_usability_threshold:
                # Reduce degradation proportionally
                restored_fraction = self.min_usability_threshold - usability
                payload = self._restore_semantics(payload, reference_payload, restored_fraction)
        return payload

    def _restore_semantics(self, degraded_payload: str, reference_payload: str, fraction: float) -> str:
        """
        Partially restores semantic content from reference payload.

        Args:
            degraded_payload: Current degraded payload
            reference_payload: Original content
            fraction: Fraction of words to restore (0-1)

        Returns:
            Restored payload string
        """
        degraded_tokens = degraded_payload.split()
        reference_tokens = reference_payload.split()
        restore_count = int(len(reference_tokens) * fraction)
        # Replace first `restore_count` tokens from reference
        restored_tokens = reference_tokens[:restore_count] + degraded_tokens[restore_count:]
        return " ".join(restored_tokens)
