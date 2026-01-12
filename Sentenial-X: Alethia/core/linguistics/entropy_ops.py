"""
Entropy Operations Module

Provides a unified interface to apply linguistic entropy transformations
from the Alethia Protocol. Combines core semantic noise with advanced
ambiguity operations.

Modules used:
- linguistic_entropy: synonym drift, polysemy injection, referential ambiguity
- ambiguity_ops: sentence shuffling, token scrambling, referential substitution

The combined transformations preserve syntactic validity while
degrading semantic interpretability for unauthorized contexts.

Author: Sentenial-X Alethia Core Team
"""

from typing import Any, Dict
from .linguistic_entropy import (
    apply_synonym_drift,
    apply_polysemy_injection,
    apply_referential_ambiguity
)
from .ambiguity_ops import (
    sentence_shuffling,
    token_scrambling,
    referential_substitution
)


class EntropyOps:
    """
    High-level orchestrator for applying semantic transformations
    to data based on provided entropy profile or custom parameters.
    """

    def __init__(self, profile: Dict[str, float] = None):
        """
        Args:
            profile: Dictionary of probabilities controlling transformation strength
                     Keys can include:
                        'synonym_drift'
                        'polysemy_injection'
                        'referential_ambiguity'
                        'sentence_shuffling'
                        'token_scrambling'
                        'referential_substitution'
        """
        default_profile = {
            'synonym_drift': 0.5,
            'polysemy_injection': 0.3,
            'referential_ambiguity': 0.2,
            'sentence_shuffling': 0.2,
            'token_scrambling': 0.1,
            'referential_substitution': 0.15
        }
        self.profile = profile or default_profile

    def transform(self, data: Any) -> Any:
        """
        Apply a full pipeline of semantic entropy transformations
        to the input data.

        Args:
            data: Input string or text content

        Returns:
            Transformed string with layered semantic entropy
        """
        if not isinstance(data, str):
            return data

        # Core linguistic transformations
        data = apply_synonym_drift(data, self.profile.get('synonym_drift', 0.5))
        data = apply_polysemy_injection(data, self.profile.get('polysemy_injection', 0.3))
        data = apply_referential_ambiguity(data, self.profile.get('referential_ambiguity', 0.2))

        # Advanced ambiguity transformations
        data = sentence_shuffling(data, self.profile.get('sentence_shuffling', 0.2))
        data = token_scrambling(data, self.profile.get('token_scrambling', 0.1))
        data = referential_substitution(data, probability=self.profile.get('referential_substitution', 0.15))

        return data
