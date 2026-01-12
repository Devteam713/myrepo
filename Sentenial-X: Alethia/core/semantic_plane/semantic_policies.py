def entropy_from_trust(trust_score: float) -> float:
    """
    Maps trust → entropy budget.
    Lower trust increases entropy.
    """
    return max(0.0, 1.0 - trust_score)
