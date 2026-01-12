"""
Ambiguity Operations Module

Provides advanced linguistic transformations to increase semantic
entropy and degrade unauthorized data interpretation within Alethia.

Functions include:
- sentence_shuffling: randomly reorder sentences
- token_scrambling: reorder or partially obfuscate words
- referential_substitution: swap entity references contextually

These transformations work in combination with linguistic_entropy
to enhance semantic degradation while preserving authorized usability.

Author: Sentenial-X Alethia Core Team
"""

import random
from typing import Any, List

def sentence_shuffling(text: str, probability: float = 0.3) -> str:
    """
    Randomly reorder sentences within the text with a given probability.

    Args:
        text: Input string containing sentences.
        probability: Chance of shuffling each sentence.

    Returns:
        String with sentences potentially shuffled.
    """
    if not isinstance(text, str) or probability <= 0.0:
        return text

    sentences = [s.strip() for s in text.split('.') if s.strip()]
    if random.random() < probability:
        random.shuffle(sentences)
    return '. '.join(sentences) + ('.' if sentences else '')

def token_scrambling(text: str, probability: float = 0.2) -> str:
    """
    Randomly swap adjacent words or shuffle tokens to introduce noise.

    Args:
        text: Input string.
        probability: Chance to scramble each token pair.

    Returns:
        Transformed string with token scrambling applied.
    """
    if not isinstance(text, str) or probability <= 0.0:
        return text

    tokens = text.split()
    for i in range(len(tokens) - 1):
        if random.random() < probability:
            tokens[i], tokens[i + 1] = tokens[i + 1], tokens[i]
    return ' '.join(tokens)

def referential_substitution(text: str, placeholders: List[str] = None, probability: float = 0.25) -> str:
    """
    Replace detected proper nouns or entity-like words with placeholder tokens.

    Args:
        text: Input string.
        placeholders: List of possible replacement strings.
        probability: Chance to replace each detected entity.

    Returns:
        Transformed string with substituted entities.
    """
    if not isinstance(text, str) or probability <= 0.0:
        return text

    if placeholders is None:
        placeholders = ["ENTITY", "OBJECT", "TARGET", "SUBJECT"]

    tokens = text.split()
    transformed = []
    for word in tokens:
        if word[0].isupper() and random.random() < probability:
            word = random.choice(placeholders)
        transformed.append(word)
    return ' '.join(transformed)
