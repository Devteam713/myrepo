"""
Linguistic Entropy Module

Provides linguistic operations to inject semantic entropy into data,
as part of the Alethia Protocol's semantic survivability layer.

Operations:
- Synonym Drift: Replace words with plausible synonyms
- Polysemy Injection: Insert ambiguous or context-ambiguous terms
- Referential Ambiguity: Obscure or replace entity references

These operations preserve syntactic validity but degrade semantic
interpretability for unauthorized or low-trust contexts.

Author: Sentenial-X Alethia Core Team
"""

import random
from typing import Any, List, Optional
import logging
import nltk
from nltk.corpus import wordnet

# Configure logger for the module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Ensure WordNet corpus is available
try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet")
    logger.info("WordNet corpus downloaded.")


class LinguisticEntropy:
    """
    Class to apply linguistic transformations to inject semantic entropy.
    """

    def __init__(self, 
                 synonym_prob: float = 0.5, 
                 polysemy_prob: float = 0.3, 
                 referential_prob: float = 0.2,
                 ambiguous_terms: Optional[List[str]] = None,
                 placeholder: str = "ENTITY") -> None:
        """
        Initialize the LinguisticEntropy engine.

        Args:
            synonym_prob: Probability of synonym replacement per word
            polysemy_prob: Probability of polysemy injection per word
            referential_prob: Probability of replacing proper nouns
            ambiguous_terms: Optional list of ambiguous words for injection
            placeholder: Placeholder for referential ambiguity
        """
        self.synonym_prob = synonym_prob
        self.polysemy_prob = polysemy_prob
        self.referential_prob = referential_prob
        self.ambiguous_terms = ambiguous_terms or ["set", "lead", "charge", "draft", "bank"]
        self.placeholder = placeholder

    def apply_synonym_drift(self, data: str) -> str:
        """
        Replace words with plausible synonyms.

        Args:
            data: Input text

        Returns:
            Transformed string with synonyms applied
        """
        if not isinstance(data, str) or self.synonym_prob <= 0.0:
            return data

        words = data.split()
        transformed = []

        for word in words:
            if random.random() < self.synonym_prob:
                synsets = wordnet.synsets(word)
                lemmas = [lemma.name() for syn in synsets for lemma in syn.lemmas() if lemma.name() != word]
                if lemmas:
                    word = random.choice(lemmas).replace("_", " ")
            transformed.append(word)

        return " ".join(transformed)

    def apply_polysemy_injection(self, data: str) -> str:
        """
        Insert ambiguous words to increase semantic entropy.

        Args:
            data: Input text

        Returns:
            Transformed string with polysemous injections
        """
        if not isinstance(data, str) or self.polysemy_prob <= 0.0:
            return data

        words = data.split()
        return " ".join(
            random.choice(self.ambiguous_terms) if random.random() < self.polysemy_prob else word
            for word in words
        )

    def apply_referential_ambiguity(self, data: str) -> str:
        """
        Obscure or replace proper nouns and entity references.

        Args:
            data: Input text

        Returns:
            Transformed string with referential ambiguity
        """
        if not isinstance(data, str) or self.referential_prob <= 0.0:
            return data

        words = data.split()
        return " ".join(
            self.placeholder if word[0].isupper() and random.random() < self.referential_prob else word
            for word in words
        )

    def apply_all(self, data: str) -> str:
        """
        Apply all linguistic entropy transformations in order.

        Args:
            data: Input text

        Returns:
            Fully transformed string
        """
        data = self.apply_synonym_drift(data)
        data = self.apply_polysemy_injection(data)
        data = self.apply_referential_ambiguity(data)
        return data
