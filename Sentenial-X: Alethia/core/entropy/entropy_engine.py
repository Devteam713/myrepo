"""
Entropy Engine Module

Responsible for applying semantic entropy transformations to data
according to Alethia Protocol adaptive profiles.

Transforms data to ensure:
- Semantic degradation for unauthorized or low-trust contexts
- Minimal distortion for authorized, high-trust contexts

Integrates with:
- AdaptiveProfiles for profile selection
- LinguisticEntropy for noise injection
- SemanticPlane for data execution and rendering

Author: Sentenial-X Alethia Core Team
"""

import logging
from typing import Any, Union

from core.entropy.adaptive_profiles import AdaptiveProfiles
from core.entropy.linguistic_entropy import LinguisticEntropy

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class EntropyEngine:
    """
    Engine for applying adaptive semantic entropy transformations
    based on trust/confidence scores.
    """

    def __init__(self):
        """Initialize the EntropyEngine."""
        # Stateless engine; profiles are loaded dynamically per transform
        self.profiles = AdaptiveProfiles()

    def transform(self, data: Union[str, Any], trust_score: float) -> Any:
        """
        Apply semantic entropy transformations based on the trust/confidence score.

        Args:
            data: Input content (string or structured text)
            trust_score: Normalized trust/confidence score [0.0, 1.0]

        Returns:
            Transformed data with semantic noise applied
        """
        if not isinstance(data, str):
            logger.warning("Non-string input detected; attempting to convert to string.")
            try:
                data = str(data)
            except Exception as e:
                logger.error("Failed to convert data to string: %s", e)
                return data  # Return as-is

        # Select adaptive profile based on trust score
        profile = self.profiles.get_profile(trust_score)

        # Initialize linguistic entropy engine with profile parameters
        entropy = LinguisticEntropy(
            synonym_prob=profile.synonym_drift,
            polysemy_prob=profile.polysemy_injection,
            referential_prob=profile.referential_ambiguity
        )

        # Apply all transformations in sequence
        transformed_data = entropy.apply_all(data)

        logger.debug(
            "EntropyEngine applied profile %s with trust_score %.2f",
            profile.name, trust_score
        )

        return transformed_data
