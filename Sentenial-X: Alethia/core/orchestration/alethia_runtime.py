from core.semantic_plane.semantic_engine import SemanticEngine
from core.semantic_plane.semantic_policies import entropy_from_trust

class AlethiaRuntime:
    """
    Single integration entrypoint for Sentenial-X.
    """

    def __init__(self):
        self.engine = SemanticEngine()

    def render(self, ses, trust_score):
        ses.entropy_budget = entropy_from_trust(trust_score)
        return self.engine.execute(ses)
