class Action:
    def __init__(self, name, func, context):
        self.name = name
        self.func = func
        self.context = context

        self._validate_func_input()

    def _validate_func_input(self):
        required_args = ['context']
        missing_args = [arg for arg in required_args if arg not in self.func.__code__.co_varnames]
        if missing_args:
            raise ValueError(f"Function {self.name} is missing required kwargs: {', '.join(missing_args)}")

    def do(self):
        return self.func(self.context)


class Actions:
    def __init__(self, actions):
        self.actions = actions

    def do(self):
        success = None
        fails = []
        for action in self.actions:
            try:
                success = action.do()
            except Exception as e:
                fails.append(e)

        return success, fails
