def stage(schema=None):
    if schema is None or "actions" not in schema:
        raise Exception("Invalid context or missing actions")

    actions = schema["actions"]
    success, fails = actions.do()

    return success, fails
