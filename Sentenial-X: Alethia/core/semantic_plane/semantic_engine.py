from core.semantic_plane.semantic_decay import evaluate_state
from core.linguistics.entropy_ops import apply_entropy

class SemanticEngine:
    """
    Executes meaning as a function of trust and entropy.
    """

    def execute(self, ses):
        ses.semantic_coherence, ses.execution_state = evaluate_state(ses)

        if ses.execution_state != "resolved":
            ses.semantic_payload = apply_entropy(
                ses.semantic_payload,
                ses.entropy_budget
            )
        return ses


from core.linguistics.entropy_ops import apply_entropy


class SemanticEngine:
    """
    Executes meaning.
    """

    def execute(self, ses):
        ses.evaluate()

        if ses.state != "resolved":
            ses.payload = apply_entropy(
                ses.payload,
                ses.entropy_budget
            )

        return ses
