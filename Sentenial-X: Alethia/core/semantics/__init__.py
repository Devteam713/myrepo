"""
Alethia Semantics Package

Provides tools for semantic post-exfiltration protection:
- Semantic encoding and decoding
- Context-aware resolution
- Reference shuffling
- Semantic state management

Author: Sentenial-X Alethia Core Team
"""

# Core semantic components
from .semantic_encoder import SemanticEncoder
from .semantic_decoder import SemanticDecoder
from .resolution_engine import ResolutionEngine
from .reference_shuffler import ReferenceShuffler
from .semantic_state import SemanticState

# Optional: define __all__ for cleaner imports
__all__ = [
    "SemanticEncoder",
    "SemanticDecoder",
    "ResolutionEngine",
    "ReferenceShuffler",
    "SemanticState"
]
