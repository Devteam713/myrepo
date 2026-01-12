"""
Environment Model Module

Responsible for representing and evaluating the runtime environment
for Alethia's semantic execution.

The environment context contributes to trust vectors and semantic
entropy decisions. Includes factors like:

- Network risk posture
- Host system security state
- Operational environment (cloud, on-prem, hybrid)
- External threat signals

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
        environment_type (str): "on-prem", "cloud", "hybrid", etc.
        timestamp (float): last update time
    """
    network_risk: float = 0.0
    host_integrity: float = 1.0
    external_threat: float = 0.0
    environment_type: str = "unknown"
    timestamp: float = field(default_factory=time.time)

    def as_dict(self) -> Dict[str, float]:
        """Return environment metrics as a dictionary."""
        return {
            "network_risk": self.network_risk,
            "host_integrity": self.host_integrity,
            "external_threat": self.external_threat,
            "timestamp": self.timestamp
        }


class EnvironmentModel:
    """
    Collects and evaluates environmental signals that influence
    Alethia's semantic plane decisions.

    Provides normalized, runtime-accessible environment state.
    """

    def __init__(self, environment_type: str = "unknown"):
        self.state = EnvironmentState(environment_type=environment_type)

    def collect_signals(self, network_risk: float, host_integrity: float, external_threat: float) -> None:
        """
        Updates environment state with provided signals.

        Args:
            network_risk: Risk of network compromise (0.0–1.0)
            host_integrity: Host security (0.0–1.0)
            external_threat: External threat level (0.0–1.0)
        """
        self.state.network_risk = self._normalize(network_risk)
        self.state.host_integrity = self._normalize(host_integrity)
        self.state.external_threat = self._normalize(external_threat)
        self.state.timestamp = time.time()

    def generate_random_demo(self) -> None:
        """
        Generates randomized signals for simulation/testing.
        """
        self.state.network_risk = random.uniform(0.0, 1.0)
        self.state.host_integrity = random.uniform(0.0, 1.0)
        self.state.external_threat = random.uniform(0.0, 1.0)
        self.state.timestamp = time.time()

    def get_state(self) -> EnvironmentState:
        """Returns the current environment state."""
        return self.state

    @staticmethod
    def _normalize(value: float) -> float:
        """
        Ensures that any input value is within the valid range [0.0, 1.0].
        """
        return max(0.0, min(1.0, value))
