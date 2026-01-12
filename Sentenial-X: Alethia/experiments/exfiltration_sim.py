from core.semantic_plane.semantic_execution_state import SemanticExecutionState
from core.orchestration.alethia_runtime import AlethiaRuntime

ses = SemanticExecutionState(
    semantic_payload="Authorize external wire transfer",
    trust_vector={"auth":0.2,"agent":0.1,"environment":0.1}
)

runtime = AlethiaRuntime()
out = runtime.render(ses, trust_score=0.15)

print(out.execution_state)
print(out.semantic_payload)
