"""
Alethia Semantic Engine

Coordinates semantic transformations, post-exfiltration degradation,
context-aware routing, and usability enforcement.

Components integrated:
- SemanticRouter
- ResolutionEngine
- DegradationEngine
- SemanticDecay
- UsabilityGuard

Author: Sentenial-X Alethia Core Team
"""

from typing import Dict, Any, List
from core.orchestration.semantic_router import SemanticRouter
from core.resolution.resolution_engine import ResolutionEngine
from core.resolution.degradation import DegradationEngine
from core.resolution.usability_guard import UsabilityGuard
from core.semantic_plane.semantic_decay import SemanticDecay


class SemanticEngine:
    """
    Orchestrates the full Alethia semantic plane pipeline.
    """

    def __init__(
        self,
        entropy_profile: Dict[str, Any] = None,
        max_degradation_passes: int = 3,
        min_usability_threshold: float = 0.85,
        base_decay: float = 0.1,
        max_decay_passes: int = 5
    ):
        """
        Initialize all components of the semantic plane.

        Args:
            entropy_profile: Optional dict to configure entropy engine
            max_degradation_passes: Max iterations for resolution/degradation
            min_usability_threshold: Minimum usability threshold for authorized users
            base_decay: Base decay fraction per exposure for semantic decay
            max_decay_passes: Maximum passes for semantic decay
        """
        self.router = SemanticRouter(entropy_profile=entropy_profile)
        self.resolution = ResolutionEngine(max_degradation_passes=max_degradation_passes)
        self.degradation = DegradationEngine(max_iterations=max_degradation_passes)
        self.usability = UsabilityGuard(min_usability_threshold=min_usability_threshold)
        self.decay = SemanticDecay(base_decay=base_decay, max_passes=max_decay_passes)

    def process_payload(self, payload_obj: Dict[str, Any], exposure_count: int = 1) -> Dict[str, Any]:
        """
        Process a single data object through the full semantic pipeline.

        Args:
            payload_obj: Dict with keys:
                - 'semantic_payload': str
                - 'context_vector': dict
                - 'trust_score': float
            exposure_count: Number of exposures for semantic decay

        Returns:
            Updated payload object with:
                - 'semantic_payload': str (transformed/degraded)
                - 'resolution_state': 'authorized' or 'degraded'
        """
        # Step 1: Route payload based on context and entropy
        routed_obj = self.router.route(payload_obj)

        # Step 2: Apply semantic decay for repeated exposure
        decayed_payload = self.decay.decay_payload(
            routed_obj['semantic_payload'],
            routed_obj['context_vector'],
            exposure_count=exposure_count
        )

        # Step 3: Resolve payload based on trust and context
        resolved_payload = self.resolution.resolve(
            decayed_payload,
            routed_obj['context_vector'],
            routed_obj['trust_score']
        )

        # Step 4: Ensure usability for authorized users
        final_payload = self.usability.enforce_usability(
            resolved_payload,
            routed_obj['semantic_payload'],
            routed_obj['trust_score']
        )

        # Update object
        routed_obj['semantic_payload'] = final_payload
        routed_obj['resolution_state'] = self.resolution.evaluate_resolution_state(routed_obj['trust_score'])

        return routed_obj

    def batch_process(self, payload_objects: List[Dict[str, Any]], exposure_count: int = 1) -> List[Dict[str, Any]]:
        """
        Process multiple data objects in a batch.

        Args:
            payload_objects: List of data objects (see process_payload)
            exposure_count: Number of exposures for semantic decay

        Returns:
            List of updated payload objects
        """
        return [self.process_payload(obj, exposure_count=exposure_count) for obj in payload_objects]
