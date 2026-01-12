def evaluate_state(ses):
    trust = sum(ses.trust_vector.values()) / max(len(ses.trust_vector), 1)
    coherence = max(0.0, trust - ses.entropy_budget)

    if coherence < 0.4:
        state = "collapsed"
    elif coherence < 0.7:
        state = "degraded"
    else:
        state = "resolved"

    return coherence, state
