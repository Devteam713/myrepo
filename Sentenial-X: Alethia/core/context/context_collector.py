"""
Context Collector Module

Responsible for gathering and normalizing runtime context signals used by Alethia's
Semantic Plane to determine semantic rendering and entropy budgets.

Context signals include:
- Authentication confidence
- Agent trust
- Environment trust
- Temporal or session-based metadata

These signals are collected, optionally weighted, and aggregated for runtime
evaluation by AlethiaRuntime or orchestration layers.

Author: Sentenial-X Alethia Core Team
"""

from dataclasses import dataclass, field
from typing import Dict, Optional
import random
import time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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

    def weighted_score(self, weights: Optional[Dict[str, float]] = None) -> float:
        """
        Compute a weighted trust score from the context vector.

        Args:
            weights: Optional dictionary with keys matching context fields
                     e.g., {"auth_confidence": 0.5, "agent_trust": 0.3, "environment_trust": 0.2}

        Returns:
            Weighted score between 0.0 and 1.0
        """
        if weights is None:
            weights = {"auth_confidence": 0.4, "agent_trust": 0.4, "environment_trust": 0.2}

        total_weight = sum(weights.values())
        if total_weight == 0:
            logger.warning("Total weight is 0; defaulting to unweighted average.")
            total_weight = 1.0

        score = (
            self.auth_confidence * weights.get("auth_confidence", 0.0) +
            self.agent_trust * weights.get("agent_trust", 0.0) +
            self.environment_trust * weights.get("environment_trust", 0.0)
        ) / total_weight

        return max(0.0, min(1.0, score))


class ContextCollector:
    """
    Collects and normalizes context signals from local agents and runtime environment.

    Provides a unified interface for Alethia semantic decisions and entropy application.
    """

    def __init__(self):
        self.context = ContextVector()

    def collect_from_agent(self, agent_signals: Dict[str, float]) -> None:
        """
        Update context vector with signals from an agent.

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

        logger.debug("Context updated from agent: %s", self.context.as_dict())

    def collect_randomized_demo(self, seed: Optional[int] = None) -> None:
        """
        Generate demo/randomized signals for testing or simulation.

        Args:
            seed: Optional random seed for reproducibility
        """
        if seed is not None:
            random.seed(seed)

        self.context.auth_confidence = random.uniform(0.0, 1.0)
        self.context.agent_trust = random.uniform(0.0, 1.0)
        self.context.environment_trust = random.uniform(0.0, 1.0)
        self.context.timestamp = time.time()

        logger.info("Randomized demo context generated: %s", self.context.as_dict())

    def get_context(self) -> ContextVector:
        """Returns the current context vector."""
        return self.context

    @staticmethod
    def _normalize(value: float) -> float:
        """Normalize a value to the range [0.0, 1.0]."""
        return max(0.0, min(1.0, value))
