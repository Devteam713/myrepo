"""
Alethia Semantic Decoder

Reconstructs semantic content for authorized contexts.
- Decodes payloads processed by Alethia
- Preserves authorized usability
- Prevents unauthorized semantic recovery
- Works with trust scores, exposure counts, and context vectors

Author: Sentenial-X Alethia Core Team
"""

from typing import Dict, Any, List
from core.semantics.reference_shuffler import ReferenceShuffler
from core.entropy.linguistic_entropy import LinguisticEntropy
from core.semantic_plane.semantic_execution_state import SemanticExecutionState


class SemanticDecoder:
    """
    Decodes Alethia-protected payloads for authorized contexts.
    """

    def __init__(self):
        self.shuffler = ReferenceShuffler()
        self.entropy_engine = LinguisticEntropy()

    def decode_payload(
        self,
        exec_state: SemanticExecutionState,
        entities: List[str] = None
    ) -> str:
        """
        Decode a payload based on context and trust.

        Args:
            exec_state: SemanticExecutionState object
            entities: Optional list of known entities to reconstruct

        Returns:
            Decoded payload string (authorized)
        """
        trust_score = exec_state.trust_score
        current_payload = exec_state.current_payload

        # Determine if authorized
        if trust_score < 0.75:
            # Low trust → do not fully decode
            return current_payload  # remains degraded

        # Step 1: Attempt entity restoration
        if entities:
            # Simple restoration by sorting tokens according to original entity list
            tokens = current_payload.split()
            for entity in entities:
                # If entity is in tokens, move it close to original position (naive demo)
                if entity in tokens:
                    tokens.remove(entity)
                    tokens.insert(0, entity)
            current_payload = " ".join(tokens)

        # Step 2: Apply entropy reduction for authorized users
        decoded_payload = self.entropy_engine.reduce_entropy(
            current_payload,
            reduction_factor=trust_score
        )

        # Step 3: Update execution state
        exec_state.update_payload(decoded_payload, decay_factor=0.0)
        exec_state.set_resolution_state("authorized")

        return decoded_payload

    def batch_decode(
        self,
        exec_states: List[SemanticExecutionState],
        entities_map: Dict[str, List[str]] = None
    ) -> Dict[str, str]:
        """
        Batch decode multiple payloads.

        Args:
            exec_states: List of SemanticExecutionState objects
            entities_map: Optional mapping of data_id -> entity list

        Returns:
            Dictionary of data_id -> decoded payload
        """
        decoded_payloads = {}
        for state in exec_states:
            entities = entities_map.get(state.data_id, []) if entities_map else None
            decoded_payloads[state.data_id] = self.decode_payload(state, entities)
        return decoded_payloads
