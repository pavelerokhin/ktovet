import inspect


def context_to_params(context, func, input_mapping=None):
    if input_mapping is None:
        input_mapping = {}

    context = dict(context)
    params = {}
    func_signature = inspect.signature(func)
    for param_name, _ in func_signature.parameters.items():
        mapping = input_mapping.get(param_name, param_name)
        if mapping not in context.keys():
            raise ValueError(f"Missing {param_name} in context (or missing input mapping)")
        params[param_name] = context[mapping]

    return params


def with_context(func):
    def wrapper(**kwargs):
        if "context" not in kwargs.keys():
            raise ValueError("Invalid arguments")

        context = kwargs.get("context")  # should always have context
        if context is None:
            raise ValueError("Missing context")

        input_mapping = kwargs.get("input_mapping")
        result_to = kwargs.get("result_to")

        params = context_to_params(context, func, input_mapping)

        result = func(**params)  # call the function and ignore the return value

        if result_to is not None:
            context[result_to] = result

        return context

    return wrapper
