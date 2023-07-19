class Action:
    def __init__(self, name, command):
        self.name = name
        self.command = command
        self.context = {}

    def do(self, context):
        c = self.command(context)
        self.context = c


# Actions is a list of Action, having the common context
class Actions:
    def __init__(self, actions, context, to_store=None):
        self.actions = actions
        self.context = context

        # check if to_store is a list
        if to_store is not None and not isinstance(to_store, list):
            raise Exception("Invalid to_store type, should be a list of stings")

        self.to_store = to_store if to_store is not None else []

    def do(self):
        fails = []
        for action in self.actions:
            try:
                action.do(self.context)
                if action.context and not action.context.keys().isdisjoint(self.to_store):
                    # select only to_store keys from the context
                    context = {k: v for k, v in action.context.items() if k in self.to_store}
                    self.context.update(context)

            except Exception as e:
                fails.append(e)

        return self.context, fails


class MemoryAction(Action):
    def __init__(self, name, command, context, memory):
        super().__init__(name, command, context)
        self.memory = memory

    def do(self):
        self.memory = self.command(self.context)
        return self.memory
