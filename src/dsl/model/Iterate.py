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
        initial_keys = set(initial_context.keys())  # Track initial keys

        all_fails = []

        for element in elements:
            ctx = {**initial_context, self.iterator: element}
            ctx, fails = self.actions.do(ctx)
            ctx = {key: value for key, value in ctx.items() if key not in initial_keys}  # Update only modified keys
            all_fails.extend(fails)

            for key in ctx.keys():
                if self.context.get(key) is None:
                    self.context[key] = []
                self.context[key].append(ctx[key])

        return {**initial_context, **(self.context if self.context is not None else {})}, all_fails
