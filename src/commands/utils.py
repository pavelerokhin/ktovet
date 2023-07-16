import random


def shuffle(context=None):
    if context is None or "data" not in context:
        raise Exception("Invalid context or missing data")

    data = [*context["data"]]
    random.shuffle(data)

    return data
