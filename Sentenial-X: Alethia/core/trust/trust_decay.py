def decay(trust: float, rate: float = 0.05) -> float:
    """
    Temporal decay of trust signals.
    """
    return max(0.0, trust - rate)
