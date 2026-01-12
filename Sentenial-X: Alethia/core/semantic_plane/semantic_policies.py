def entropy_from_trust(trust_score: float) -> float:
    """
    Map trust score (0.0-1.0) to an entropy budget.
    Lower trust → higher entropy.
    """
    return max(0.0, min(1.0, 1.0 - trust_score))
