"""
Alethia Core Context Package

Provides runtime context collection, modeling, and fusion utilities
for the Alethia Protocol semantic control plane within Sentenial-X.

Modules:
- context_collector: Collects and normalizes runtime context signals from agents and environments.
- environment_model: Models runtime environmental state for semantic evaluation.
- signal_fusion: Aggregates multiple context signals into a unified trust/confidence score.

Author: Sentenial-X Alethia Core Team
"""

# Explicit imports for package-level accessibility
from .context_collector import ContextCollector, ContextVector
from .environment_model import EnvironmentModel
from .signal_fusion import SignalFusion

__all__ = [
    "ContextCollector",
    "ContextVector",
    "EnvironmentModel",
    "SignalFusion",
]
