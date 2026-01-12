"""
Alethia Core Utilities Package

Provides hashing, unique IDs, and other general-purpose utilities
used across the Alethia Protocol and Sentenial-X architecture.

Modules:
- hashing: Cryptographic hash functions for payloads and context vectors
- ids: Deterministic, random, and timestamped identifiers
"""

# Expose utility classes/functions at the package level
from .hashing import Hasher
from .ids import IDGenerator

__all__ = [
    "Hasher",
    "IDGenerator",
]
