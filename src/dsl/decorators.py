import inspect


def context_to_params(context, func):
    context = dict(context)
    params = {}
    func_signature = inspect.signature(func)
    for param_name, _ in func_signature.parameters.items():
        if param_name not in context.keys():
            raise ValueError(f"Missing {param_name} in context")
        params[param_name] = context[param_name]

    return params


def function(func):
    def wrapper(**kwargs):
        if "context" not in kwargs.keys():
            raise ValueError("Invalid arguments")

        context = kwargs.get("context")  # should always have context
        if context is None:
            raise ValueError("Missing context")

        params = context_to_params(context, func)

        func(**params)  # call the function and ignore the return value

        return context

    return wrapper


def function_with_result(func):
    def wrapper(**kwargs):
        if "context" not in kwargs.keys() and "result_to" not in kwargs.keys():
            raise ValueError("Invalid arguments")

        context = kwargs.get("context")  # should always have context
        if context is None:
            raise ValueError("Missing context")
        result_to = kwargs.get("result_to")  # should always have context
        if result_to is None:
            raise ValueError("Missing result_to")

        params = context_to_params(context, func)

        result = func(**params)
        context[result_to] = result

        return context

    return wrapper