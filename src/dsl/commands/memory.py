
def store_to_memory(context=None):
    if context is None or "driver" not in context or "selector" not in context:
        raise Exception("Invalid context or missing driver or selector")


    return elements