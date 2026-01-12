"""
Signal Fusion Module

Responsible for aggregating multiple runtime context signals into
a unified context vector for Alethia's semantic plane.

Combines:
- Agent-provided signals (auth_confidence, agent_trust)
- Environmental signals (network risk, host integrity, external threat)
- Optional temporal or external telemetry

The fused signals determine semantic entropy and execution state.
"""

from dataclasses import dataclass, field
from typing import Dict
import time

@dataclass
class FusedContext:
    """
    Represents a unified context vector after signal fusion.

    Attributes:
        trust_score (float): 0.0 (low) → 1.0 (high)
        components (Dict[str, float]): Raw normalized signal contributions
        timestamp (float): Fusion time
    """
    trust_score: float = 0.0
    components: Dict[str, float] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

    def as_dict(self) -> Dict[str, float]:
        """Return fused context as dictionary."""
        return {
            "trust_score": self.trust_score,
            **self.components,
            "timestamp": self.timestamp
        }


class SignalFusion:
    """
    Aggregates context and environment signals into a single unified
    trust vector for semantic decisions.
    """

    def __init__(self):
        self.fused = FusedContext()

    def fuse_signals(self, context_signals: Dict[str, float], environment_signals: Dict[str, float], weights: Dict[str, float] = None) -> FusedContext:
        """
        Fuse multiple signals into a single trust score.

        Args:
            context_signals: Agent signals, e.g., auth_confidence, agent_trust
            environment_signals: Environment signals, e.g., host_integrity, network_risk
            weights: Optional dict specifying weight for each signal (default equal weight)

        Returns:
            FusedContext object with trust_score and individual components
        """
        if weights is None:
            # Default: equal weight across all signals
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
            # Invert risk signals to represent trust (higher risk → lower trust)
            if "risk" in key or "threat" in key:
                normalized = 1.0 - normalized
            components[key] = normalized
            fused_score += normalized * w

        fused_score = max(0.0, min(1.0, fused_score))
        self.fused = FusedContext(trust_score=fused_score, components=components, timestamp=time.time())
        return self.fused

    def get_fused_context(self) -> FusedContext:
        """Return the most recent fused context."""
        return self.fused

    @staticmethod
    def _normalize(value: float) -> float:
        """Ensure values are in range [0.0, 1.0]."""
        return max(0.0, min(1.0, value))
