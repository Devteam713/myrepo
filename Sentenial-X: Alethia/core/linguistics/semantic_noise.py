"""
Semantic Noise Module

Provides low-level token, sentence, and phrase-level transformations
to introduce controlled semantic noise into textual data.

Functions here are intended to be building blocks for higher-level
Alethia transformations (EntropyOps, linguistic_entropy, ambiguity_ops).

Author: Sentenial-X Alethia Core Team
"""

import random
from typing import Any, List

def token_swap(text: str, probability: float = 0.1) -> str:
    """
    Randomly swap adjacent tokens in the text to introduce local semantic noise.

    Args:
        text: Input string.
        probability: Chance to swap each pair of adjacent tokens.

    Returns:
        String with swapped tokens.
    """
    if not isinstance(text, str) or probability <= 0.0:
        return text

    tokens = text.split()
    for i in range(len(tokens) - 1):
        if random.random() < probability:
            tokens[i], tokens[i + 1] = tokens[i + 1], tokens[i]
    return " ".join(tokens)


def sentence_split_shuffle(text: str, probability: float = 0.2) -> str:
    """
    Split text into sentences and shuffle them with a given probability.

    Args:
        text: Input string containing sentences.
        probability: Chance to shuffle the sentence order.

    Returns:
        String with potentially shuffled sentences.
    """
    if not isinstance(text, str) or probability <= 0.0:
        return text

    sentences = [s.strip() for s in text.split('.') if s.strip()]
    if random.random() < probability:
        random.shuffle(sentences)
    return '. '.join(sentences) + ('.' if sentences else '')


def random_token_injection(text: str, candidates: List[str] = None, probability: float = 0.15) -> str:
    """
    Randomly inject tokens into the text to increase semantic uncertainty.

    Args:
        text: Input string.
        candidates: List of tokens to choose from. Defaults to generic ambiguous terms.
        probability: Chance to replace a token with a candidate.

    Returns:
        Transformed string with injected tokens.
    """
    if not isinstance(text, str) or probability <= 0.0:
        return text

    if candidates is None:
        candidates = ["ENTITY", "OBJECT", "ITEM", "TARGET", "SUBJECT"]

    tokens = text.split()
    transformed = [
        random.choice(candidates) if random.random() < probability else word
        for word in tokens
    ]
    return " ".join(transformed)


def random_case_noise(text: str, probability: float = 0.1) -> str:
    """
    Randomly changes case of letters in the text to introduce noise that can
    disrupt automated parsers or AI models without breaking readability.

    Args:
        text: Input string.
        probability: Chance each character changes case.

    Returns:
        String with randomized casing.
    """
    if not isinstance(text, str) or probability <= 0.0:
        return text

    return ''.join(
        c.upper() if random.random() < probability else c.lower()
        for c in text
    )
