def decay(trust: float, rate: float = 0.05) -> float:
    return max(0.0, trust - rate)
