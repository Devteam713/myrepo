from dataclasses import dataclass, field
from typing import Dict
import time
import uuid


@dataclass
class SemanticExecutionState:
    """
    The only artifact Alethia ever produces.
    Safe to exfiltrate by design.
    """
    ses_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    payload: str = ""
    trust_vector: Dict[str, float] = field(default_factory=dict)
    entropy_budget: float = 0.0
    semantic_stability: float = 1.0
    last_eval: float = field(default_factory=time.time)
    state: str = "latent"

    def evaluate(self):
        trust = sum(self.trust_vector.values()) / max(len(self.trust_vector), 1)

        # semantic stability collapses as trust decays
        self.semantic_stability = max(0.0, trust - self.entropy_budget)

        if self.semantic_stability < 0.4:
            self.state = "collapsed"
        elif self.semantic_stability < 0.7:
            self.state = "degraded"
        else:
            self.state = "resolved"

        return self.state
