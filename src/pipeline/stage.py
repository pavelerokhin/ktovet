MAX_ATTEMPTS = 3
MAX_POOL = 10
STORE_PARTIAL = True


def stage(data=None, schema=None, context=None):
    if data is None:
        return None

    if schema is None:
        raise ValueError("schema is not defined")

    print(f"input: {len(data)} items to process")

    actions = schema["actions"]  # it always has actions by definition

    success, fails = actions.do(data=data, context=context)

    return success, fails
