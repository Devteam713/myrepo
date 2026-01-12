def score(trust_vector: dict) -> float:
    """
    Aggregate trust vector into a single score.
    """
    if not trust_vector:
        return 0.0
    return sum(trust_vector.values()) / len(trust_vector)
