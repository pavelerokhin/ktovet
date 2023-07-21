# Actions is a list of Action, having the common context
class Actions:
    def __init__(self, actions: list, context: dict = None):
        # actions should be a list of Action
        if not isinstance(actions, list):
            raise ValueError("Invalid actions type, should be a list of Action")

        self.actions = actions
        self.context = context if context is not None else {}

    def do(self, context: dict = None):
        if context is not None:  # context can be injected
            self.context.update(context)

        fails = []
        for action in self.actions:
            try:
                if action.context is None:
                    self.context = action.do(self.context)
                else:
                    action.context.update(self.context)
                    self.context = action.do()
            except Exception as e:
                fails.append(e)

        return self.context, fails
