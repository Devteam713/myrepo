"""
Alethia Resolution Engine

Responsible for:
- Evaluating semantic payloads in context
- Determining authorized vs degraded resolution
- Applying adaptive linguistic entropy and shuffling
- Enforcing semantic policies

Author: Sentenial-X Alethia Core Team
"""

from typing import Dict, Any, List
from core.semantic_plane.semantic_policies import SemanticPolicySet
from core.semantics.reference_shuffler import ReferenceShuffler
from core.entropy.linguistic_entropy import LinguisticEntropy
from core.semantic_plane.semantic_execution_state import SemanticExecutionState


class ResolutionEngine:
    """
    Engine to resolve payloads according to context, trust, and semantic policies.
    """

    def __init__(self, policy_set: SemanticPolicySet = None):
        self.policy_set = policy_set if policy_set else SemanticPolicySet()
        self.shuffler = ReferenceShuffler()
        self.entropy_engine = LinguisticEntropy()

    def resolve_payload(
        self,
        exec_state: SemanticExecutionState,
        entities: List[str] = None
    ) -> str:
        """
        Resolve the semantic payload based on context and policies.

        Args:
            exec_state: SemanticExecutionState object for the payload
            entities: Optional list of known entities to target for shuffling

        Returns:
            Resolved payload string
        """
        # Determine decay factor based on policies
        decay_factor = self.policy_set.get_decay_factor(
            context_vector=exec_state.context_vector,
            exposure_count=exec_state.exposure_count
        )

        # Apply reference shuffling
        shuffled_payload = self.shuffler.shuffle_payload(
            exec_state.current_payload,
            entities=entities,
            entropy_level=decay_factor
        )

        # Apply additional linguistic entropy
        final_payload = self.entropy_engine.apply_entropy(
            shuffled_payload,
            entropy_level=decay_factor
        )

        # Update execution state
        exec_state.update_payload(final_payload, decay_factor=decay_factor)

        # Update resolution state based on trust
        if exec_state.trust_score >= 0.8:
            exec_state.set_resolution_state("authorized")
        else:
            exec_state.set_resolution_state("degraded")

        return final_payload

    def batch_resolve(
        self,
        exec_states: List[SemanticExecutionState],
        entities_map: Dict[str, List[str]] = None
    ) -> Dict[str, str]:
        """
        Batch process multiple payloads.

        Args:
            exec_states: List of SemanticExecutionState objects
            entities_map: Optional mapping of data_id -> entity list

        Returns:
            Dictionary of data_id -> resolved payload
        """
        resolved_payloads = {}
        for state in exec_states:
            entities = entities_map.get(state.data_id, []) if entities_map else None
            resolved_payloads[state.data_id] = self.resolve_payload(state, entities)
        return resolved_payloads
