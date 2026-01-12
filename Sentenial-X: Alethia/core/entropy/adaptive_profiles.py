"""
Adaptive Entropy Profiles Module

Defines semantic transformation and entropy profiles for the Alethia Protocol.

Profiles are applied based on the trust/confidence of the runtime context.
Lower trust or unauthorized context → higher semantic noise.
Higher trust or authorized context → minimal semantic distortion.

Author: Sentenial-X Alethia Core Team
"""

import logging
from dataclasses import dataclass
from typing import List

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@dataclass
class EntropyProfile:
    """
    Represents a semantic entropy profile.

    Attributes:
        name: Profile name (e.g., 'high_noise', 'medium_noise', 'low_noise')
        noise_level: Overall semantic noise applied (0.0–1.0)
        synonym_drift: Probability of synonym substitution (0.0–1.0)
        polysemy_injection: Probability of adding ambiguous terms (0.0–1.0)
        referential_ambiguity: Probability of disrupting entity references (0.0–1.0)
    """
    name: str
    noise_level: float
    synonym_drift: float
    polysemy_injection: float
    referential_ambiguity: float


class AdaptiveProfiles:
    """
    Provides adaptive semantic entropy profiles based on context/trust score.

    Supports dynamic interpolation and runtime profile adjustments.
    """

    # Predefined entropy profiles (ordered low → high)
    PROFILES: List[EntropyProfile] = [
        EntropyProfile(
            name="low_noise",
            noise_level=0.1,
            synonym_drift=0.05,
            polysemy_injection=0.05,
            referential_ambiguity=0.1
        ),
        EntropyProfile(
            name="medium_noise",
            noise_level=0.5,
            synonym_drift=0.4,
            polysemy_injection=0.35,
            referential_ambiguity=0.45
        ),
        EntropyProfile(
            name="high_noise",
            noise_level=0.9,
            synonym_drift=0.85,
            polysemy_injection=0.8,
            referential_ambiguity=0.9
        )
    ]

    def __init__(self) -> None:
        """Initialize AdaptiveProfiles instance."""
        self.profiles = self.PROFILES

    def get_profile(self, trust_score: float) -> EntropyProfile:
        """
        Selects an entropy profile based on trust/confidence score.

        Args:
            trust_score: Value in [0.0, 1.0], where 1.0 = fully trusted

        Returns:
            EntropyProfile
        """
        trust_score = self._normalize(trust_score)

        # Interpolated selection (instead of hard thresholds)
        if trust_score >= 0.8:
            profile = self._get_profile_by_name("low_noise")
        elif trust_score >= 0.4:
            profile = self._get_profile_by_name("medium_noise")
        else:
            profile = self._get_profile_by_name("high_noise")

        logger.debug("Selected profile '%s' for trust_score %.2f", profile.name, trust_score)
        return profile

    def _get_profile_by_name(self, name: str) -> EntropyProfile:
        """Retrieve a profile by name."""
        for profile in self.profiles:
            if profile.name == name:
                return profile
        raise ValueError(f"Entropy profile '{name}' not found.")

    @staticmethod
    def _normalize(value: float) -> float:
        """Clamp value to [0.0, 1.0]."""
        return max(0.0, min(1.0, value))
