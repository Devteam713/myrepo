def score(trust_vector: dict) -> float:
    return sum(trust_vector.values()) / len(trust_vector)
