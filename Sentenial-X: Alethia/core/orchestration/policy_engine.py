"""
Alethia Policy Engine

Defines and enforces semantic transformation policies for Alethia-protected data.

Responsibilities:
- Determine transformation profiles based on context and trust
- Apply adaptive linguistic entropy levels
- Select semantic noise strategies
- Support configurable, dynamic policy rules

Author: Sentenial-X Alethia Core Team
"""

from typing import Dict, Any, List

# Example transformation profiles
DEFAULT_PROFILES = {
    "low_trust": {
        "entropy_weight": 0.9,
        "apply_token_swap": True,
        "apply_sentence_shuffle": True,
        "apply_random_injection": True,
        "apply_case_noise": True
    },
    "medium_trust": {
        "entropy_weight": 0.5,
        "apply_token_swap": True,
        "apply_sentence_shuffle": False,
        "apply_random_injection": True,
        "apply_case_noise": False
    },
    "high_trust": {
        "entropy_weight": 0.1,
        "apply_token_swap": False,
        "apply_sentence_shuffle": False,
        "apply_random_injection": False,
        "apply_case_noise": False
    }
}


class PolicyEngine:
    """
    Evaluates context and trust to select a semantic transformation profile.
    """

    def __init__(self, profiles: Dict[str, Dict[str, Any]] = None):
        """
        Args:
            profiles: Optional custom policy profiles
        """
        self.profiles = profiles if profiles else DEFAULT_PROFILES

    def select_profile(self, trust_score: float) -> Dict[str, Any]:
        """
        Select a transformation profile based on trust score.

        Args:
            trust_score: Float in range [0,1]

        Returns:
            Dictionary containing profile parameters
        """
        if trust_score < 0.4:
            return self.profiles["low_trust"]
        elif trust_score < 0.8:
            return self.profiles["medium_trust"]
        else:
            return self.profiles["high_trust"]

    def apply_policy(self, data_object: Dict[str, Any], transformed_payload: str) -> str:
        """
        Apply selected semantic transformations to the payload.

        Args:
            data_object: Original data object with context and trust
            transformed_payload: Current payload string (may already have entropy applied)

        Returns:
            Payload string after policy-based transformations
        """
        from core.linguistics.semantic_noise import (
            token_swap,
            sentence_split_shuffle,
            random_token_injection,
            random_case_noise
        )

        trust_score = data_object.get("trust_score", 0.0)
        profile = self.select_profile(trust_score)

        payload = transformed_payload

        if profile.get("apply_token_swap", False):
            payload = token_swap(payload, probability=profile["entropy_weight"])

        if profile.get("apply_sentence_shuffle", False):
            payload = sentence_split_shuffle(payload, probability=profile["entropy_weight"])

        if profile.get("apply_random_injection", False):
            payload = random_token_injection(payload, probability=profile["entropy_weight"])

        if profile.get("apply_case_noise", False):
            payload = random_case_noise(payload, probability=profile["entropy_weight"])

        return payload
