"""
Linguistic Entropy Module

Provides core linguistic operations to inject semantic entropy into data,
as part of the Alethia Protocol.

Operations:
- Synonym Drift: Replace words with plausible synonyms
- Polysemy Injection: Insert ambiguous terms or phrases
- Referential Ambiguity: Obscure or replace entity references

These operations preserve syntactic validity but degrade semantic
interpretability for unauthorized or low-trust contexts.

Author: Sentenial-X Alethia Core Team
"""

import random
from typing import Any, List
from nltk.corpus import wordnet
import nltk

# Ensure WordNet corpus is available
try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet")


def apply_synonym_drift(data: Any, probability: float = 0.5) -> Any:
    """
    Replace words in the data with synonyms based on a probability.

    Args:
        data: Input string
        probability: Chance to replace each word (0.0 - 1.0)

    Returns:
        Transformed string with synonym substitutions
    """
    if not isinstance(data, str) or probability <= 0.0:
        return data

    words = data.split()
    transformed = []

    for word in words:
        if random.random() < probability:
            synsets = wordnet.synsets(word)
            lemmas = [lemma.name() for syn in synsets for lemma in syn.lemmas() if lemma.name() != word]
            if lemmas:
                word = random.choice(lemmas).replace("_", " ")
        transformed.append(word)

    return " ".join(transformed)


def apply_polysemy_injection(data: Any, probability: float = 0.3, ambiguous_terms: List[str] = None) -> Any:
    """
    Introduce ambiguous terms into the data to increase semantic entropy.

    Args:
        data: Input string
        probability: Chance to inject an ambiguous term at a word position
        ambiguous_terms: List of ambiguous words to choose from

    Returns:
        Transformed string with polysemous injections
    """
    if not isinstance(data, str) or probability <= 0.0:
        return data

    if ambiguous_terms is None:
        ambiguous_terms = ["set", "lead", "charge", "draft", "bank"]

    words = data.split()
    transformed = [
        random.choice(ambiguous_terms) if random.random() < probability else word
        for word in words
    ]

    return " ".join(transformed)


def apply_referential_ambiguity(data: Any, probability: float = 0.2, placeholder: str = "ENTITY") -> Any:
    """
    Obscure entity references (e.g., proper nouns) in the data.

    Args:
        data: Input string
        probability: Chance to replace a proper noun with the placeholder
        placeholder: Replacement string for entities

    Returns:
        Transformed string with referential ambiguity
    """
    if not isinstance(data, str) or probability <= 0.0:
        return data

    words = data.split()
    transformed = [
        placeholder if word[0].isupper() and random.random() < probability else word
        for word in words
    ]

    return " ".join(transformed)
