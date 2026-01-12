from core.semantic_plane.semantic_decay import evaluate_state
from core.linguistics.entropy_ops import apply_entropy

class SemanticEngine:
    """
    Executes semantic rendering of SES.
    Applies entropy when coherence < threshold.
    """
    def execute(self, ses):
        coherence, state = evaluate_state(ses)
        ses.semantic_coherence = coherence
        ses.execution_state = state

        if coherence < 0.7:
            ses.semantic_payload = apply_entropy(ses.semantic_payload, ses.entropy_budget)

        ses.update_timestamp()
        return ses        return ses
