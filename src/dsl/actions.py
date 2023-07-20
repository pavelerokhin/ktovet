class Action:
    def __init__(self, name, command, result_to=None, input_mapping=None):
        self.name = name
        self.command = command
        self.result_to = result_to
        self.input_mapping = input_mapping

    def do(self, context):
        return self.command(context=context,
                            result_to=self.result_to,
                            input_mapping=self.input_mapping)


# Actions is a list of Action, having the common context
class Actions:
    def __init__(self, actions, context):
        # actions should be a list of Action
        if not isinstance(actions, list):
            raise ValueError("Invalid actions type, should be a list of Action")

        self.actions = actions
        self.context = context

    def do(self):
        fails = []
        for action in self.actions:
            try:
                self.context = action.do(context=self.context)
            except Exception as e:
                fails.append(e)

        return self.context, fails

