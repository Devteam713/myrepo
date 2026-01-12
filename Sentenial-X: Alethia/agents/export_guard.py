def allow_export(ses):
    return ses.execution_state != "resolved"
