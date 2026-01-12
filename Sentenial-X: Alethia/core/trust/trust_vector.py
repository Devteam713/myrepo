from dataclasses import dataclass

@dataclass
class TrustVector:
    """
    Trust signals collected from agents.
    Values normalized between 0.0 and 1.0.
    """
    auth_confidence: float
    agent_trust: float
    environment: float

    def as_dict(self):
        return {
            "auth": self.auth_confidence,
            "agent": self.agent_trust,
            "environment": self.environment
        }
