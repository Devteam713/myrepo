"""
Hashing Utilities for Alethia

Provides cryptographic hashing functions for semantic payloads,
context vectors, and general content integrity verification.

Author: Sentenial-X Alethia Core Team
"""

import hashlib
import json
from typing import Any


class Hasher:
    """
    A utility class for generating cryptographic hashes using
    secure algorithms.
    """

    @staticmethod
    def sha256(data: Any, encode_json: bool = True) -> str:
        """
        Compute SHA-256 hash of the given data.

        Args:
            data (Any): Data to hash (dict, list, str, bytes, int)
            encode_json (bool): If True and data is dict/list, convert to JSON string

        Returns:
            str: Hexadecimal SHA-256 hash
        """
        if isinstance(data, (dict, list)) and encode_json:
            data_bytes = json.dumps(data, sort_keys=True).encode("utf-8")
        elif isinstance(data, str):
            data_bytes = data.encode("utf-8")
        elif isinstance(data, bytes):
            data_bytes = data
        else:
            # fallback for numbers or other serializable types
            data_bytes = str(data).encode("utf-8")

        return hashlib.sha256(data_bytes).hexdigest()

    @staticmethod
    def sha512(data: Any, encode_json: bool = True) -> str:
        """
        Compute SHA-512 hash of the given data.

        Args:
            data (Any): Data to hash
            encode_json (bool): If True and data is dict/list, convert to JSON string

        Returns:
            str: Hexadecimal SHA-512 hash
        """
        if isinstance(data, (dict, list)) and encode_json:
            data_bytes = json.dumps(data, sort_keys=True).encode("utf-8")
        elif isinstance(data, str):
            data_bytes = data.encode("utf-8")
        elif isinstance(data, bytes):
            data_bytes = data
        else:
            data_bytes = str(data).encode("utf-8")

        return hashlib.sha512(data_bytes).hexdigest()

    @staticmethod
    def fingerprint_context(context_vector: dict) -> str:
        """
        Generate a consistent hash/fingerprint for a context vector.

        Args:
            context_vector (dict): Context signals

        Returns:
            str: SHA-256 fingerprint
        """
        return Hasher.sha256(context_vector)

    @staticmethod
    def fingerprint_payload(payload: str, salt: str = "") -> str:
        """
        Generate a hash for a semantic payload with optional salt.

        Args:
            payload (str): Semantic payload
            salt (str): Optional salt to prevent hash collisions

        Returns:
            str: SHA-256 hash
        """
        combined = f"{payload}|{salt}"
        return Hasher.sha256(combined)

    @staticmethod
    def verify_hash(data: Any, expected_hash: str, algorithm: str = "sha256") -> bool:
        """
        Verify that the hash of given data matches expected hash.

        Args:
            data (Any): Data to hash
            expected_hash (str): Reference hash
            algorithm (str): "sha256" or "sha512"

        Returns:
            bool: True if hash matches, False otherwise
        """
        if algorithm == "sha256":
            return Hasher.sha256(data) == expected_hash
        elif algorithm == "sha512":
            return Hasher.sha512(data) == expected_hash
        else:
            raise ValueError("Unsupported hashing algorithm. Use 'sha256' or 'sha512'.")
