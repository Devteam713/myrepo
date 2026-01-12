"""
Alethia Semantic Policies

Defines semantic transformation rules and policies for:
- Exposure-based degradation
- Trust-aware routing
- Adaptive linguistic entropy
- Context-dependent usability enforcement

Author: Sentenial-X Alethia Core Team
"""

from typing import Dict, Any, List


class SemanticPolicy:
    """
    Represents a single semantic policy rule.
    """

    def __init__(self, name: str, min_trust: float = 0.0, max_decay: float = 1.0, description: str = ""):
        """
        Args:
            name: Policy name
            min_trust: Minimum trust score to avoid maximum decay
            max_decay: Maximum allowed semantic degradation
            description: Optional human-readable description
        """
        self.name = name
        self.min_trust = min_trust
        self.max_decay = max_decay
        self.description = description

    def evaluate(self, context_vector: Dict[str, Any], exposure_count: int) -> float:
        """
        Compute the decay intensity based on context and exposure.

        Args:
            context_vector: Dictionary containing 'auth_confidence' and 'agent_trust'
            exposure_count: Number of times the payload has been accessed

        Returns:
            Decay factor [0,1]
        """
        trust_score = context_vector.get("auth_confidence", 0.0)
        agent_trust = context_vector.get("agent_trust", 0.0)
        combined_trust = (trust_score + agent_trust) / 2.0

        # Decay intensity inversely proportional to trust, capped by max_decay
        decay_intensity = min(self.max_decay, (1.0 - combined_trust) * (exposure_count / (exposure_count + 1)))
        return decay_intensity


class SemanticPolicySet:
    """
    Collection of policies that define semantic behavior.
    """

    def __init__(self, policies: List[SemanticPolicy] = None):
        """
        Args:
            policies: Optional list of SemanticPolicy objects
        """
        self.policies = policies if policies else []

    def add_policy(self, policy: SemanticPolicy):
        """
        Add a new policy to the set.
        """
        self.policies.append(policy)

    def get_decay_factor(self, context_vector: Dict[str, Any], exposure_count: int) -> float:
        """
        Evaluate all policies and return the most conservative decay factor
        (i.e., highest decay applied among policies).
        """
        if not self.policies:
            return 0.0  # No policies → no decay

        decay_factors = [policy.evaluate(context_vector, exposure_count) for policy in self.policies]
        # Apply the maximum decay suggested by any policy
        return max(decay_factors)

    def describe_policies(self) -> List[str]:
        """
        Return human-readable descriptions of all policies
        """
        return [f"{p.name}: {p.description} (Min Trust: {p.min_trust}, Max Decay: {p.max_decay})"
                for p in self.policies]
