"""
Environment Model Module

Responsible for representing and evaluating the runtime environment
for Alethia's semantic execution plane.

The environment context contributes to trust vectors and semantic
entropy decisions. Factors include:

- Network risk posture
- Host system security state
- Operational environment type (cloud, on-prem, hybrid)
- External threat signals

This module provides normalized, time-stamped state to feed into
AlethiaRuntime and entropy decisions.

Author: Sentenial-X Alethia Core Team
"""

from dataclasses import dataclass, field
from typing import Dict
import time
import random


@dataclass
class EnvironmentState:
    """
    Represents the operational environment state for Alethia.

    Attributes:
        network_risk (float): 0.0 (safe) → 1.0 (high risk)
        host_integrity (float): 0.0 (compromised) → 1.0 (secure)
        external_threat (float): 0.0 (low) → 1.0 (high)
        environment_type (str): "on-prem", "cloud", "hybrid", or "unknown"
        timestamp (float): last update time
    """
    network_risk: float = 0.0
    host_integrity: float = 1.0
    external_threat: float = 0.0
    environment_type: str = "unknown"
    timestamp: float = field(default_factory=time.time)

    def as_dict(self) -> Dict[str, float]:
        """Return environment metrics as a dictionary for runtime evaluation."""
        return {
            "network_risk": self.network_risk,
            "host_integrity": self.host_integrity,
            "external_threat": self.external_threat,
            "timestamp": self.timestamp
        }


class EnvironmentModel:
    """
    Evaluates environmental signals affecting Alethia semantic decisions.

    Provides methods to update, normalize, and retrieve a unified
    environment state, suitable for fusion with trust and context vectors.
    """

    def __init__(self, environment_type: str = "unknown"):
        """Initialize the environment model with optional environment type."""
        self.state = EnvironmentState(environment_type=environment_type)

    def collect_signals(self, network_risk: float, host_integrity: float, external_threat: float) -> None:
        """
        Updates environment state with normalized signals.

        Args:
            network_risk (float): Risk of network compromise (0.0–1.0)
            host_integrity (float): Host security level (0.0–1.0)
            external_threat (float): External threat level (0.0–1.0)
        """
        self.state.network_risk = self._normalize(network_risk)
        self.state.host_integrity = self._normalize(host_integrity)
        self.state.external_threat = self._normalize(external_threat)
        self.state.timestamp = time.time()

    def generate_random_demo(self) -> None:
        """
        Generates randomized signals for testing or simulation purposes.
        Useful for AI/entropy testing without live telemetry.
        """
        self.state.network_risk = random.uniform(0.0, 1.0)
        self.state.host_integrity = random.uniform(0.0, 1.0)
        self.state.external_threat = random.uniform(0.0, 1.0)
        self.state.timestamp = time.time()

    def get_state(self) -> EnvironmentState:
        """
        Returns the current environment state.

        Returns:
            EnvironmentState: Current operational environment snapshot
        """
        return self.state

    @staticmethod
    def _normalize(value: float) -> float:
        """
        Normalize a raw input value to [0.0, 1.0].

        Args:
            value (float): Raw signal value

        Returns:
            float: Normalized value in [0.0, 1.0]
        """
        return max(0.0, min(1.0, value))
