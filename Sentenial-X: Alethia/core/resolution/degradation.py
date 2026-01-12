"""
Alethia Semantic Degradation Module

Implements controlled semantic degradation for post-exfiltration protection.

Responsibilities:
- Introduce controlled semantic ambiguity
- Reduce operational value for unauthorized users
- Apply context-aware degradation strategies
- Maintain syntactic validity for plausibility

Author: Sentenial-X Alethia Core Team
"""

import random
from typing import Dict, Any
from core.linguistics.ambiguity_ops import synonym_drift, polysemy_injection, referential_ambiguity
from core.linguistics.semantic_noise import token_swap, sentence_split_shuffle


class DegradationEngine:
    """
    Applies semantic degradation to payloads based on trust and context.
    """

    def __init__(self, max_iterations: int = 3):
        """
        Args:
            max_iterations: Maximum degradation passes to apply
        """
        self.max_iterations = max_iterations

    def degrade(self, payload: str, trust_score: float) -> str:
        """
        Degrade a payload based on trust score.

        Args:
            payload: Original payload string
            trust_score: Float [0,1] representing authorization confidence
                         Lower trust → stronger degradation

        Returns:
            Degraded payload string
        """
        # Compute degradation intensity
        intensity = (1 - trust_score)
        iterations = max(1, int(self.max_iterations * intensity))

        degraded_payload = payload

        for _ in range(iterations):
            # Randomly select degradation methods
            methods = [
                lambda text: synonym_drift(text, intensity),
                lambda text: polysemy_injection(text, intensity),
                lambda text: referential_ambiguity(text, intensity),
                lambda text: token_swap(text, probability=intensity),
                lambda text: sentence_split_shuffle(text, probability=intensity)
            ]
            # Apply 2-3 random methods per iteration
            for func in random.sample(methods, k=min(3, len(methods))):
                degraded_payload = func(degraded_payload)

        return degraded_payload

    def degrade_with_context(self, payload: str, context_vector: Dict[str, Any]) -> str:
        """
        Degrade payload using context signals from the context vector.

        Args:
            payload: Original payload string
            context_vector: Dictionary of contextual signals including:
                - auth_confidence
                - environment
                - agent_trust

        Returns:
            Degraded payload string
        """
        trust_score = context_vector.get("auth_confidence", 0.0)
        agent_trust = context_vector.get("agent_trust", 0.0)
        # Combine trust signals for degradation weighting
        combined_trust = max(0.0, min(1.0, 0.5 * (trust_score + agent_trust)))
        return self.degrade(payload, combined_trust)
