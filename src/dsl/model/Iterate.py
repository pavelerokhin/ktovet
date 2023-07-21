from src.dsl.model.Actions import Actions


class Iterate:
    def __init__(self, actions: Actions, iterator: str, context: dict):
        self.actions = actions
        self.iterator = iterator
        self.context = context

    def do(self, context: dict = None):
        if context is not None:
            self.context = context

        elements = self.context.get(self.iterator)
        if elements is None:
            raise ValueError("Nothing to iterate")

        initial_context = self.context
        all_fails = []
        for element in elements:
            ctx = initial_context
            ctx[self.iterator] = element
            ctx, fails = self.actions.do(ctx)
            self.context.update(ctx)
            all_fails.extend(fails)

        return self.context, all_fails
