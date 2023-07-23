class Action:
    def __init__(self, name, command, context: dict = None, input_mapping=None, result_to=None):
        self.name = name
        self.command = command
        self.context = context
        self.result_to = result_to
        self.input_mapping = input_mapping

    def do(self, context=None):  # context can be injected, updating the existing context
        if context is not None:
            if self.context is not None:
                self.context.update(context)
            else:
                self.context = context

        if self.context is None:
            raise ValueError("Action should have context")

        return self.command(context=self.context,
                            result_to=self.result_to,
                            input_mapping=self.input_mapping)
