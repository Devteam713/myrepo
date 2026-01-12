"""
Linguistic Entropy Module

Provides core linguistic operations to inject semantic entropy
into data as part of the Alethia Protocol.

Operations include:
- Synonym drift: replace words with plausible synonyms
- Polysemy injection: introduce ambiguous terms or phrases
- Referential ambiguity: obscure entity references

These transformations preserve syntactic validity but degrade
semantic value for low-trust contexts.

Author: Sentenial-X Alethia Core Team
"""

import random
from typing import Any, List
from nltk.corpus import wordnet

# Ensure nltk wordnet is downloaded
import nltk
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')


def apply_synonym_drift(data: Any, probability: float = 0.5) -> Any:
    """
    Replace words in data with synonyms based on probability.

    Args:
        data: Input string
        probability: Chance to replace each word (0.0–1.0)

    Returns:
        Transformed string
    """
    if not isinstance(data, str) or probability <= 0.0:
        return data

    words = data.split()
    transformed = []

    for word in words:
        if random.random() < probability:
            synonyms = wordnet.synsets(word)
            if synonyms:
                lemmas = [lemma.name() for syn in synonyms for lemma in syn.lemmas() if lemma.name() != word]
                if lemmas:
                    word = random.choice(lemmas).replace("_", " ")
        transformed.append(word)

    return " ".join(transformed)


def apply_polysemy_injection(data: Any, probability: float = 0.3, ambiguous_terms: List[str] = None) -> Any:
    """
    Introduce ambiguous terms or phrases into data.

    Args:
        data: Input string
        probability: Chance to inject an ambiguous term at a position
        ambiguous_terms: List of ambiguous words to use

    Returns:
        Transformed string
    """
    if not isinstance(data, str) or probability <= 0.0:
        return data

    if ambiguous_terms is None:
        ambiguous_terms = ["set", "bank", "lead", "charge", "draft"]  # generic polysemous terms

    words = data.split()
    transformed = []

    for word in words:
        if random.random() < probability:
            word = random.choice(ambiguous_terms)
        transformed.append(word)

    return " ".join(transformed)


def apply_referential_ambiguity(data: Any, probability: float = 0.2, placeholder: str = "ENTITY") -> Any:
    """
    Obscure entity references in the data.

    Args:
        data: Input string
        probability: Chance to replace a word that looks like a proper noun
        placeholder: Replacement string

    Returns:
        Transformed string
    """
    if not isinstance(data, str) or probability <= 0.0:
        return data

    words = data.split()
    transformed = []

    for word in words:
        # Simple heuristic: words starting with uppercase assumed proper nouns
        if word[0].isupper() and random.random() < probability:
            word = placeholder
        transformed.append(word)

    return " ".join(transformed)

import random


class LinguisticEntropyEngine:
    """
    Applies controlled linguistic instability.
    """

    def apply(self, text: str, entropy_level: float) -> str:
        if entropy_level <= 0:
            return text

        words = text.split()
        swaps = int(len(words) * entropy_level)

        for _ in range(swaps):
            i, j = random.sample(range(len(words)), 2)
            words[i], words[j] = words[j], words[i]

        return " ".join(words)
