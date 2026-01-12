# Alethia/core/orchestration/semantic_router.py

from typing import Dict, Any, Optional
from core.orchestration.policy_engine import PolicyEngine
from core.semantic_plane.semantic_engine import SemanticEngine
from core.entropy.entropy_engine import EntropyEngine


class SemanticRouter:
    """
    Routes data objects through Alethia's semantic control plane.
    Fully configurable, policy-driven, and testable.
    """

    def __init__(
        self,
        entropy_profile: Optional[Dict[str, float]] = None,
        policy_engine: Optional[PolicyEngine] = None,
        semantic_engine: Optional[SemanticEngine] = None,
        entropy_engine: Optional[EntropyEngine] = None
    ):
        # Allow engine injection for testing or custom behavior
        self.policy_engine = policy_engine or PolicyEngine()
        self.semantic_engine = semantic_engine or SemanticEngine()
        self.entropy_engine = entropy_engine or EntropyEngine(profile=entropy_profile)

    def route(self, data_object: Dict[str, Any]) -> Dict[str, Any]:
        """
        Routes the data object through semantic control plane.
        Applies entropy, policy transformations, and semantic resolution.
        """
        payload = data_object.get("semantic_payload", "")
        trust = data_object.get("trust_score", 0.0)
        context = data_object.get("context_vector", {})

        # 1. Calculate entropy level
        try:
            entropy_level = self.entropy_engine.calculate_level(trust, context)
            payload = self.entropy_engine.apply(payload, entropy_level)
        except Exception as e:
            print(f"[EntropyEngine Error] {e}")
            entropy_level = 1.0  # fallback to max entropy
            payload = ""

        # 2. Apply policy transformations
        try:
            payload = self.policy_engine.apply_policy(data_object, payload)
        except Exception as e:
            print(f"[PolicyEngine Error] {e}")

        # 3. Determine resolution state
        try:
            resolution_state = self.policy_engine.determine_resolution(trust)
        except Exception as e:
            print(f"[PolicyEngine Resolution Error] {e}")
            resolution_state = "degraded"

        # 4. Resolve semantics
        try:
            payload = self.semantic_engine.resolve(payload, context, trust)
        except Exception as e:
            print(f"[SemanticEngine Error] {e}")
            payload = ""

        # 5. Update data object
        data_object.update({
            "semantic_payload": payload,
            "entropy_level": entropy_level,
            "resolution_state": resolution_state
        })

        return data_object
