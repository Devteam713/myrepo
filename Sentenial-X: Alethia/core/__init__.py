"""
Core Alethia Package

This package contains all modules required for the Alethia Protocol,
including:

- Semantic Plane: Executes semantic transformations and coherence evaluation
- Trust Management: Tracks trust vectors and computes entropy budgets
- Linguistics: Implements entropy, ambiguity, and semantic noise operations
- Orchestration: Runtime engine integrating all components
- Utilities: Common helper functions (IDs, hashing, logging)

Alethia is designed to function as a post-exfiltration semantic control plane,
integrating into Sentenial-X for breach-resilient, AI-aware security.

Modules:
    core.semantic_plane
    core.trust
    core.linguistics
    core.orchestration
    core.utils

Usage:
    from core.semantic_plane.semantic_execution_state import SemanticExecutionState
    from core.orchestration.alethia_runtime import AlethiaRuntime

    ses = SemanticExecutionState(semantic_payload="Sensitive data")
    runtime = AlethiaRuntime()
    rendered_ses = runtime.render(ses, trust_score=0.5)
"""

# Expose common core classes at package level for convenience
from core.semantic_plane.semantic_execution_state import SemanticExecutionState
from core.orchestration.alethia_runtime import AlethiaRuntime

__all__ = [
    "SemanticExecutionState",
    "AlethiaRuntime"
]
