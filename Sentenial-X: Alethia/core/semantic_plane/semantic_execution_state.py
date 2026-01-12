"""
Alethia Semantic Execution State

Tracks runtime metadata for semantic payloads processed through the Alethia pipeline.

Responsibilities:
- Maintain resolution state ('authorized', 'degraded', 'unknown')
- Track exposure count and decay progress
- Record trust and context metrics
- Support auditing and rollback for post-exfiltration analysis

Author: Sentenial-X Alethia Core Team
"""

from typing import Dict, Any
import datetime


class SemanticExecutionState:
    """
    Maintains execution state of a semantic payload in Alethia.
    """

    def __init__(self, data_id: str, initial_payload: str, context_vector: Dict[str, Any]):
        """
        Args:
            data_id: Unique identifier for the data object
            initial_payload: Original semantic content
            context_vector: Contextual signals and trust metrics
        """
        self.data_id = data_id
        self.original_payload = initial_payload
        self.current_payload = initial_payload
        self.context_vector = context_vector.copy()
        self.trust_score = context_vector.get("auth_confidence", 0.0)
        self.agent_trust = context_vector.get("agent_trust", 0.0)

        self.resolution_state = "unknown"
        self.exposure_count = 0
        self.decay_history = []
        self.last_updated = datetime.datetime.utcnow()

    def update_payload(self, new_payload: str, decay_factor: float = 0.0):
        """
        Update the current payload after transformation or decay.

        Args:
            new_payload: Transformed or degraded payload string
            decay_factor: Float indicating fraction of degradation applied [0,1]
        """
        self.current_payload = new_payload
        self.exposure_count += 1
        self.decay_history.append({"timestamp": datetime.datetime.utcnow(), "decay_factor": decay_factor})
        self.last_updated = datetime.datetime.utcnow()

    def set_resolution_state(self, state: str):
        """
        Set the current resolution state.

        Args:
            state: 'authorized', 'degraded', or 'unknown'
        """
        if state not in ["authorized", "degraded", "unknown"]:
            raise ValueError(f"Invalid resolution state: {state}")
        self.resolution_state = state
        self.last_updated = datetime.datetime.utcnow()

    def update_trust_score(self, new_trust_score: float, new_agent_trust: float = None):
        """
        Update trust metrics for dynamic context evaluation.

        Args:
            new_trust_score: Float [0,1] for auth_confidence
            new_agent_trust: Optional float [0,1] for agent_trust
        """
        self.trust_score = max(0.0, min(1.0, new_trust_score))
        if new_agent_trust is not None:
            self.agent_trust = max(0.0, min(1.0, new_agent_trust))
        self.context_vector["auth_confidence"] = self.trust_score
        self.context_vector["agent_trust"] = self.agent_trust
        self.last_updated = datetime.datetime.utcnow()

    def get_state_snapshot(self) -> Dict[str, Any]:
        """
        Returns a snapshot of the execution state for auditing or logging.

        Returns:
            Dictionary with payload metadata
        """
        return {
            "data_id": self.data_id,
            "current_payload": self.current_payload,
            "original_payload": self.original_payload,
            "resolution_state": self.resolution_state,
            "trust_score": self.trust_score,
            "agent_trust": self.agent_trust,
            "exposure_count": self.exposure_count,
            "decay_history": self.decay_history.copy(),
            "context_vector": self.context_vector.copy(),
            "last_updated": self.last_updated.isoformat()
        }

    def reset_state(self):
        """
        Reset payload to original state (useful for testing or rollback)
        """
        self.current_payload = self.original_payload
        self.resolution_state = "unknown"
        self.exposure_count = 0
        self.decay_history = []
        self.last_updated = datetime.datetime.utcnow()
