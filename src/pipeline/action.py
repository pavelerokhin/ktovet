class Action:
    def __init__(self, name, func):
        self.name = name
        self.func = func

        self._validate_func_input()
        self._validate_func_return()

    def _validate_func_input(self):
        required_args = ['data', 'context']
        missing_args = [arg for arg in required_args if arg not in self.func.__code__.co_varnames]
        if missing_args:
            raise ValueError(f"Function {self.name} is missing required kwargs: {', '.join(missing_args)}")

    def _validate_func_return(self):
            result = self.func()
            if not isinstance(result, tuple) or len(result) != 2:
                raise ValueError(f"Function {self.name} should return a tuple of length 2")

    def do(self, *args, **kwargs):
        return self.func(*args, **kwargs)


class Actions:
    def __init__(self, actions):
        self.actions = actions

    def do(self, data, context):
        s = data
        f = []
        for action in self.actions:
            s, f_new = action.do(data=s, context=context)
            if f_new:
                f.extend(f_new)

        return s, f
