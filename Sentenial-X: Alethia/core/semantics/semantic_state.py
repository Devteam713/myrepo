from dataclasses import dataclass, field
from typing import Dict
import uuid
import time


@dataclass
class SemanticState:
    """
    Semantic State Object (SSO)

    Represents meaning as a function of trust, context, and entropy.
    This object is safe to exfiltrate.
    """
    data_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    semantic_payload: str = ""
    context_vector: Dict[str, float] = field(default_factory=dict)
    entropy_level: float = 0.0
    resolution_state: str = "unresolved"
    created_at: float = field(default_factory=time.time)

    def is_resolvable(self, threshold: float = 0.7) -> bool:
        """
        Determines whether meaning can be reconstructed.
        """
        trust = self.context_vector.get("agent_trust", 0.0)
        auth = self.context_vector.get("auth_confidence", 0.0)

        score = (trust + auth) / 2
        return score >= threshold and self.entropy_level < 0.5

    def degrade(self):
        """
        Force semantic degradation.
        """
        self.resolution_state = "degraded"
        self.semantic_payload = self._collapse_payload()

    def _collapse_payload(self) -> str:
        """
        Collapse meaning while preserving syntax.
        """
        tokens = self.semantic_payload.split()
        return " ".join(tokens[::-1])  # simple reversible-looking collapse

