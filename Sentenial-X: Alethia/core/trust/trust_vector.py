from dataclasses import dataclass

@dataclass
class TrustVector:
    auth: float
    agent: float
    environment: float
