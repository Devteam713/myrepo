class ResolutionEngine:
    """
    Resolves or degrades semantic meaning.
    """

    def resolve(self, semantic_state):
        if semantic_state.is_resolvable():
            semantic_state.resolution_state = "resolved"
            return semantic_state.semantic_payload

        semantic_state.degrade()
        return semantic_state.semantic_payload
