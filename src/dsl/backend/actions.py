class Action:
    def __init__(self, name, command, context):
        self.name = name
        self.command = command
        self.context = context

    def do(self):
        return self.command(self.context)


class MemoryAction(Action):
    def __init__(self, name, command, context, memory):
        super().__init__(name, command, context)
        self.memory = memory

    def do(self):
        self.memory = self.command(self.context)
        return self.memory


class Actions:
    def __init__(self, actions, memory=None):
        self.actions = actions
        self.memory = memory if memory is not None else {}

    def do(self):
        success = None
        fails = []
        for action in self.actions:
            try:
                success = action.do()
                if type(action) == MemoryAction:
                    self.memory.update(action.memory)
            except Exception as e:
                fails.append(e)

        return success, fails
