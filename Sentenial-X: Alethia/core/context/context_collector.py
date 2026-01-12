"""
Context Collector Module

Responsible for gathering runtime context signals used by Alethia's
Semantic Plane to determine semantic rendering and entropy budgets.

Context signals include:
- Authentication confidence
- Agent trust
- Environment state
- Temporal or session-based metadata

These signals are collected, normalized, and aggregated for runtime
evaluation by AlethiaRuntime.

Author: Sentenial-X Alethia Core Team
"""

from dataclasses import dataclass, field
from typing import Dict
import random
import time

@dataclass
class ContextVector:
    """
    Represents a normalized set of runtime context signals.
    Values are between 0.0 (low trust) and 1.0 (high trust).
    """
    auth_confidence: float = 0.0
    agent_trust: float = 0.0
    environment_trust: float = 0.0
    timestamp: float = field(default_factory=time.time)

    def as_dict(self) -> Dict[str, float]:
        """Return context vector as dictionary."""
        return {
            "auth_confidence": self.auth_confidence,
            "agent_trust": self.agent_trust,
            "environment_trust": self.environment_trust,
            "timestamp": self.timestamp
        }


class ContextCollector:
    """
    Collects and normalizes context signals from local agents and
    runtime environment.

    Provides a unified interface for Alethia semantic decisions.
    """

    def __init__(self):
        self.context = ContextVector()

    def collect_from_agent(self, agent_signals: Dict[str, float]) -> None:
        """
        Updates context vector with signals from an agent.

        Args:
            agent_signals: Dictionary with keys:
                - 'auth_confidence'
                - 'agent_trust'
                - 'environment_trust'
        """
        self.context.auth_confidence = self._normalize(agent_signals.get("auth_confidence", 0.0))
        self.context.agent_trust = self._normalize(agent_signals.get("agent_trust", 0.0))
        self.context.environment_trust = self._normalize(agent_signals.get("environment_trust", 0.0))
        self.context.timestamp = time.time()

    def collect_randomized_demo(self) -> None:
        """
        Generates demo/randomized signals for testing or simulation.
        """
        self.context.auth_confidence = random.uniform(0.0, 1.0)
        self.context.agent_trust = random.uniform(0.0, 1.0)
        self.context.environment_trust = random.uniform(0.0, 1.0)
        self.context.timestamp = time.time()

    def get_context(self) -> ContextVector:
        """Returns the current context vector."""
        return self.context

    @staticmethod
    def _normalize(value: float) -> float:
        """Normalize a value to [0.0, 1.0]."""
        return max(0.0, min(1.0, value))
