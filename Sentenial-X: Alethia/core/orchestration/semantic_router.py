from core.entropy.entropy_engine import EntropyEngine
from core.resolution.resolution_engine import ResolutionEngine


class SemanticRouter:
    """
    Central semantic execution path.
    """

    def __init__(self):
        self.entropy_engine = EntropyEngine()
        self.resolution_engine = ResolutionEngine()

    def process(self, semantic_state):
        semantic_state = self.entropy_engine.process(semantic_state)
        return self.resolution_engine.resolve(semantic_state)
