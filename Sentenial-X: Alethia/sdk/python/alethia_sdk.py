from core.orchestration.alethia_runtime import AlethiaRuntime

runtime = AlethiaRuntime()

def protect(ses, trust_score):
    return runtime.render(ses, trust_score)
