"""
Alethia Linguistics Package

Provides linguistic operations for semantic transformations within
the Alethia Protocol.

Modules included:
- linguistic_entropy: Core semantic noise functions (synonym drift, polysemy injection, referential ambiguity)
- ambiguity_ops: Additional ambiguity-based transformations (if needed)
- semantic_noise: Low-level noise injection utilities (token scrambling, sentence reordering)

This __init__.py exposes the key functions for use by the EntropyEngine
and other semantic processing layers.
"""

from .linguistic_entropy import (
    apply_synonym_drift,
    apply_polysemy_injection,
    apply_referential_ambiguity
)

# Future extensions
# from .ambiguity_ops import ...
# from .semantic_noise import ...

__all__ = [
    "apply_synonym_drift",
    "apply_polysemy_injection",
    "apply_referential_ambiguity"
]
