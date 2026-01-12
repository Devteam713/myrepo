def evaluate_state(ses):
    """
    Computes semantic coherence and state based on trust and entropy.
    """
    trust_values = list(ses.trust_vector.values())
    avg_trust = sum(trust_values) / max(len(trust_values), 1)
    coherence = max(0.0, avg_trust - ses.entropy_budget)

    if coherence < 0.4:
        state = "collapsed"
    elif coherence < 0.7:
        state = "degraded"
    else:
        state = "resolved"

    return coherence, state
