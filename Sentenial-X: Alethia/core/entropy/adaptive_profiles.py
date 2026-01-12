"""
Adaptive Entropy Profiles Module

Defines semantic transformation and entropy profiles for the Alethia Protocol.

Profiles are applied based on the trust/confidence of the runtime context.
Lower trust or unauthorized context → higher semantic noise.
Higher trust or authorized context → minimal semantic distortion.

Author: Sentenial-X Alethia Core Team
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class EntropyProfile:
    """
    Represents a semantic entropy profile.

    Attributes:
        name (str): Name of the profile (e.g., 'high_noise', 'medium_noise', 'low_noise')
        noise_level (float): Amount of semantic noise applied (0.0–1.0)
        synonym_drift (float): Probability of synonym substitution (0.0–1.0)
        polysemy_injection (float): Probability of adding ambiguous terms (0.0–1.0)
        referential_ambiguity (float): Probability of disrupting entity references (0.0–1.0)
    """
    name: str
    noise_level: float
    synonym_drift: float
    polysemy_injection: float
    referential_ambiguity: float


class AdaptiveProfiles:
    """
    Provides adaptive semantic entropy profiles based on context/trust score.

    Usage:
        profile = AdaptiveProfiles.get_profile(trust_score=0.25)
    """

    # Predefined entropy profiles
    PROFILES = [
        EntropyProfile(
            name="high_noise",
            noise_level=0.9,
            synonym_drift=0.85,
            polysemy_injection=0.8,
            referential_ambiguity=0.9
        ),
        EntropyProfile(
            name="medium_noise",
            noise_level=0.5,
            synonym_drift=0.4,
            polysemy_injection=0.35,
            referential_ambiguity=0.45
        ),
        EntropyProfile(
            name="low_noise",
            noise_level=0.1,
            synonym_drift=0.05,
            polysemy_injection=0.05,
            referential_ambiguity=0.1
        )
    ]

    @staticmethod
    def get_profile(trust_score: float) -> EntropyProfile:
        """
        Selects an appropriate entropy profile based on trust/confidence.

        Args:
            trust_score: Value in [0.0, 1.0], where 1.0 = fully trusted context

        Returns:
            EntropyProfile object
        """
        trust_score = AdaptiveProfiles._normalize(trust_score)

        if trust_score >= 0.8:
            return AdaptiveProfiles._get_profile_by_name("low_noise")
        elif trust_score >= 0.4:
            return AdaptiveProfiles._get_profile_by_name("medium_noise")
        else:
            return AdaptiveProfiles._get_profile_by_name("high_noise")

    @staticmethod
    def _get_profile_by_name(name: str) -> EntropyProfile:
        """Helper to retrieve a profile by name."""
        for profile in AdaptiveProfiles.PROFILES:
            if profile.name == name:
                return profile
        raise ValueError(f"Entropy profile '{name}' not found.")

    @staticmethod
    def _normalize(value: float) -> float:
        """Ensure value is in range [0.0, 1.0]."""
        return max(0.0, min(1.0, value))
