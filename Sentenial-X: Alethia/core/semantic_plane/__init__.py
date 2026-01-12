"""
Alethia Semantic Plane Module

This module provides the core interfaces and orchestrations for semantic
transformations, post-exfiltration survivability, and context-aware
payload resolution.

It integrates:
- SemanticEngine
- ResolutionEngine
- DegradationEngine
- UsabilityGuard
- SemanticRouter

Author: Sentenial-X Alethia Core Team
"""

# Expose semantic plane components
from core.semantic_plane.semantic_engine import SemanticEngine
from core.resolution.resolution_engine import ResolutionEngine
from core.resolution.degradation import DegradationEngine
from core.resolution.usability_guard import UsabilityGuard
from core.orchestration.semantic_router import SemanticRouter

# Semantic plane version
__version__ = "1.0.0"

# Convenience constructor for full semantic pipeline
def create_semantic_pipeline(entropy_profile=None, max_degradation_passes: int = 3):
    """
    Initializes a full Alethia semantic plane pipeline with:
        - SemanticRouter
        - ResolutionEngine
        - DegradationEngine
        - UsabilityGuard

    Args:
        entropy_profile: Optional dictionary for entropy engine configuration
        max_degradation_passes: Maximum degradation iterations

    Returns:
        Dict with initialized components
    """
    router = SemanticRouter(entropy_profile=entropy_profile)
    resolution = ResolutionEngine(max_degradation_passes=max_degradation_passes)
    degradation = DegradationEngine(max_iterations=max_degradation_passes)
    usability = UsabilityGuard()

    return {
        "router": router,
        "resolution": resolution,
        "degradation": degradation,
        "usability": usability
    }
