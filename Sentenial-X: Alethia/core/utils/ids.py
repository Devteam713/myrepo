"""
IDs Utilities for Alethia

Provides cryptographically unique identifiers for data objects,
semantic payloads, context vectors, and runtime entities.

Author: Sentenial-X Alethia Core Team
"""

import uuid
import hashlib
import time
from typing import Optional
from .hashing import Hasher


class IDGenerator:
    """
    Generates deterministic and random IDs for Alethia objects.
    """

    @staticmethod
    def uuid4() -> str:
        """
        Generate a random UUID4 string.

        Returns:
            str: Random UUID4
        """
        return str(uuid.uuid4())

    @staticmethod
    def semantic_id(payload: str, salt: Optional[str] = None) -> str:
        """
        Generate a stable, content-based ID for a semantic payload.

        Args:
            payload (str): Semantic payload content
            salt (str): Optional salt to avoid collisions

        Returns:
            str: SHA-256 hash as unique semantic ID
        """
        return Hasher.fingerprint_payload(payload, salt or str(time.time()))

    @staticmethod
    def context_id(context_vector: dict, salt: Optional[str] = None) -> str:
        """
        Generate a unique ID for a trust/context vector.

        Args:
            context_vector (dict): Context signals
            salt (str): Optional salt to prevent collisions

        Returns:
            str: SHA-256 hash as context ID
        """
        combined = context_vector.copy()
        if salt:
            combined["_salt"] = salt
        return Hasher.fingerprint_context(combined)

    @staticmethod
    def short_id(length: int = 12) -> str:
        """
        Generate a short, URL-safe unique ID.

        Args:
            length (int): Desired length of ID

        Returns:
            str: Short unique ID
        """
        u = uuid.uuid4().hex
        return u[:length]

    @staticmethod
    def timestamped_id(prefix: str = "D") -> str:
        """
        Generate a timestamped ID for runtime objects.

        Args:
            prefix (str): Optional prefix (default: D)

        Returns:
            str: ID string like D_20260112_123456_abcd
        """
        ts = time.strftime("%Y%m%d_%H%M%S")
        random_suffix = IDGenerator.short_id(4)
        return f"{prefix}_{ts}_{random_suffix}"
