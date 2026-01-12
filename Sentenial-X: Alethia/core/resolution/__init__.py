"""
Alethia Core Resolution Package

Responsible for post-exfiltration semantic control:
- Managing semantic degradation
- Enforcing authorized usability
- Resolving content contextually based on semantic and trust vectors

Modules:
- degradation: Handles semantic decay for unauthorized contexts
- resolution_engine: Core resolution logic for semantic content
- usability_guard: Ensures operational usability for authorized actors
"""

# Expose key classes/functions at the package level
from .degradation import SemanticDegradation
from .resolution_engine import ResolutionEngine
from .usability_guard import UsabilityGuard

__all__ = [
    "SemanticDegradation",
    "ResolutionEngine",
    "UsabilityGuard",
]
