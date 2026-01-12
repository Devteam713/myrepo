"""
Signal Fusion Module

Aggregates runtime context signals into a unified context vector for Alethia's semantic plane.

Responsibilities:
- Combine agent signals (auth_confidence, agent_trust)
- Integrate environmental signals (network_risk, host_integrity, external_threat)
- Apply optional weighting
- Produce a normalized trust score for semantic entropy decisions

Author: Sentenial-X Alethia Core Team
"""

from dataclasses import dataclass, field
from typing import Dict, Optional
import time


@dataclass
class FusedContext:
    """
    Represents a unified context vector after signal fusion.

    Attributes:
        trust_score (float): Normalized overall trust score (0.0 = low, 1.0 = high)
        components (Dict[str, float]): Individual normalized signals
        timestamp (float): Time of fusion
    """
    trust_score: float = 0.0
    components: Dict[str, float] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

    def as_dict(self) -> Dict[str, float]:
        """Return the fused context as a dictionary including components and timestamp."""
        return {
            "trust_score": self.trust_score,
            **self.components,
            "timestamp": self.timestamp
        }


class SignalFusion:
    """
    Aggregates multiple signals into a single trust vector for semantic decisions.

    Works with:
        - ContextCollector output (auth_confidence, agent_trust)
        - EnvironmentModel output (network_risk, host_integrity, external_threat)
    """

    def __init__(self):
        self.fused = FusedContext()

    def fuse_signals(
        self,
        context_signals: Dict[str, float],
        environment_signals: Dict[str, float],
        weights: Optional[Dict[str, float]] = None
    ) -> FusedContext:
        """
        Fuse context and environment signals into a single trust score.

        Args:
            context_signals: Agent-provided signals (auth_confidence, agent_trust)
            environment_signals: Environment signals (host_integrity, network_risk, external_threat)
            weights: Optional weights for each signal (default: equal)

        Returns:
            FusedContext: Contains the trust score and normalized component signals
        """
        # Default: equal weight if not provided
        if weights is None:
            all_keys = list(context_signals.keys()) + list(environment_signals.keys())
            weight = 1.0 / max(len(all_keys), 1)
            weights = {k: weight for k in all_keys}

        fused_score = 0.0
        components = {}

        # Fuse context signals
        for key, value in context_signals.items():
            w = weights.get(key, 0.0)
            normalized = self._normalize(value)
            components[key] = normalized
            fused_score += normalized * w

        # Fuse environment signals
        for key, value in environment_signals.items():
            w = weights.get(key, 0.0)
            normalized = self._normalize(value)
            # Invert risk/threat signals to represent trust
            if "risk" in key.lower() or "threat" in key.lower():
                normalized = 1.0 - normalized
            components[key] = normalized
            fused_score += normalized * w

        # Clamp final trust score
        fused_score = max(0.0, min(1.0, fused_score))

        # Update fused context
        self.fused = FusedContext(trust_score=fused_score, components=components, timestamp=time.time())
        return self.fused

    def get_fused_context(self) -> FusedContext:
        """Return the latest fused context vector."""
        return self.fused

    @staticmethod
    def _normalize(value: float) -> float:
        """Clamp value to [0.0, 1.0]."""
        return max(0.0, min(1.0, value))
