from core.entropy.linguistic_entropy import LinguisticEntropyEngine


class EntropyEngine:
    """
    Decides how much entropy to apply.
    """

    def __init__(self):
        self.les = LinguisticEntropyEngine()

    def process(self, semantic_state):
        entropy = semantic_state.entropy_level
        semantic_state.semantic_payload = self.les.apply(
            semantic_state.semantic_payload,
            entropy
        )
        return semantic_state
