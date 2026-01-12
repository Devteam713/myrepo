from dataclasses import dataclass, field
from typing import Dict
import uuid
import time

@dataclass
class SemanticExecutionState:
    """
    The atomic semantic artifact. Safe to exfiltrate, unsafe to interpret
    without proper trust and runtime context.
    """
    ses_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    semantic_payload: str = ""
    trust_vector: Dict[str, float] = field(default_factory=dict)
    entropy_budget: float = 0.0
    semantic_coherence: float = 1.0
    execution_state: str = "latent"
    last_eval: float = field(default_factory=time.time)

    def update_timestamp(self):
        self.last_eval = time.time()    semantic_stability: float = 1.0
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
