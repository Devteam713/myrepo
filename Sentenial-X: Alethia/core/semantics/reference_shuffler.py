"""
Alethia Reference Shuffler

Provides controlled semantic perturbation by:
- Shuffling entity references
- Reordering logical statements
- Maintaining syntactic and statistical plausibility
- Supporting context-sensitive entropy injection

Author: Sentenial-X Alethia Core Team
"""

import random
from typing import List, Dict, Any


class ReferenceShuffler:
    """
    Engine for shuffling entity references and logical statements to degrade semantics.
    """

    def __init__(self, shuffle_seed: int = None):
        """
        Args:
            shuffle_seed: Optional random seed for reproducible shuffling
        """
        self.random = random.Random(shuffle_seed)

    def shuffle_entities(self, text_tokens: List[str], entities: List[str]) -> List[str]:
        """
        Shuffle entity mentions in text while preserving token positions.

        Args:
            text_tokens: List of tokenized text
            entities: List of entity strings to shuffle

        Returns:
            List of text tokens with shuffled entity references
        """
        # Extract indices of entities in text
        entity_indices = [i for i, token in enumerate(text_tokens) if token in entities]
        if len(entity_indices) <= 1:
            return text_tokens  # Nothing to shuffle

        # Shuffle entities
        shuffled_indices = entity_indices.copy()
        self.random.shuffle(shuffled_indices)

        # Map shuffled entities
        shuffled_text = text_tokens.copy()
        for orig_idx, shuffled_idx in zip(entity_indices, shuffled_indices):
            shuffled_text[orig_idx] = text_tokens[shuffled_idx]

        return shuffled_text

    def shuffle_sentences(self, sentences: List[str]) -> List[str]:
        """
        Shuffle sentence order while preserving overall coherence.

        Args:
            sentences: List of sentence strings

        Returns:
            Shuffled list of sentences
        """
        shuffled_sentences = sentences.copy()
        self.random.shuffle(shuffled_sentences)
        return shuffled_sentences

    def apply_entropy(self, text_tokens: List[str], entropy_level: float = 0.5) -> List[str]:
        """
        Introduce stochastic token-level perturbations proportional to entropy_level.

        Args:
            text_tokens: List of tokenized text
            entropy_level: Float [0,1] controlling the intensity of perturbation

        Returns:
            List of perturbed text tokens
        """
        perturbed_tokens = text_tokens.copy()
        n = len(text_tokens)
        num_swaps = max(1, int(entropy_level * n / 2))

        for _ in range(num_swaps):
            i, j = self.random.sample(range(n), 2)
            perturbed_tokens[i], perturbed_tokens[j] = perturbed_tokens[j], perturbed_tokens[i]

        return perturbed_tokens

    def shuffle_payload(
        self,
        payload: str,
        entities: List[str] = None,
        entropy_level: float = 0.5
    ) -> str:
        """
        High-level API to shuffle a semantic payload.

        Args:
            payload: Original string content
            entities: Optional list of known entities to target
            entropy_level: Float [0,1] controlling degradation

        Returns:
            Shuffled payload string
        """
        # Tokenize (naive whitespace for demo; replace with NLP tokenizer in prod)
        tokens = payload.split()

        # Step 1: Shuffle entities if provided
        if entities:
            tokens = self.shuffle_entities(tokens, entities)

        # Step 2: Apply entropy-based perturbation
        tokens = self.apply_entropy(tokens, entropy_level=entropy_level)

        # Step 3: Reconstruct payload
        shuffled_payload = " ".join(tokens)
        return shuffled_payload
