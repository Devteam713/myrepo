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
