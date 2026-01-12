"""
Alethia Semantic Encoder

Transforms sensitive payloads into context-aware, semantically protected representations.
- Prepares payloads for post-exfiltration survivability
- Applies reference shuffling and entropy
- Updates execution state with initial degradation
- Integrates with ResolutionEngine and SemanticDecoder

Author: Sentenial-X Alethia Core Team
"""

from typing import List
from core.semantics.reference_shuffler import ReferenceShuffler
from core.entropy.linguistic_entropy import LinguisticEntropy
from core.semantic_plane.semantic_execution_state import SemanticExecutionState


class SemanticEncoder:
    """
    Encodes payloads with controlled semantic degradation.
    """

    def __init__(self):
        self.shuffler = ReferenceShuffler()
        self.entropy_engine = LinguisticEntropy()

    def encode_payload(
        self,
        exec_state: SemanticExecutionState,
        entities: List[str] = None,
        entropy_level: float = 0.5
    ) -> str:
        """
        Encode a payload into Alethia-protected form.

        Args:
            exec_state: SemanticExecutionState object
            entities: Optional list of known entities to shuffle
            entropy_level: Float [0,1] controlling initial semantic degradation

        Returns:
            Encoded payload string
        """
        original_payload = exec_state.initial_payload

        # Step 1: Shuffle entity references
        if entities:
            shuffled_payload = self.shuffler.shuffle_payload(
                original_payload, entities=entities, entropy_level=entropy_level
            )
        else:
            shuffled_payload = original_payload

        # Step 2: Apply entropy-based perturbations
        encoded_payload = self.entropy_engine.apply_entropy(
            shuffled_payload, entropy_level=entropy_level
        )

        # Step 3: Update execution state
        exec_state.current_payload = encoded_payload
        exec_state.decay_factor = entropy_level
        exec_state.resolution_state = "degraded"

        return encoded_payload

    def batch_encode(
        self,
        exec_states: List[SemanticExecutionState],
        entities_map: dict = None,
        entropy_level: float = 0.5
    ) -> dict:
        """
        Batch encode multiple payloads.

        Args:
            exec_states: List of SemanticExecutionState objects
            entities_map: Optional mapping of data_id -> entity list
            entropy_level: Float controlling initial degradation

        Returns:
            Dictionary of data_id -> encoded payload
        """
        encoded_payloads = {}
        for state in exec_states:
            entities = entities_map.get(state.data_id, []) if entities_map else None
            encoded_payloads[state.data_id] = self.encode_payload(
                state, entities=entities, entropy_level=entropy_level
            )
        return encoded_payloads
