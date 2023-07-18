class Stage:
    def __init__(self, schema):
        if schema is None or "actions" not in schema:
            raise Exception("Invalid context or missing actions")

        self.actions = schema["actions"]
        self.memory = schema.get("memory", {})  # inherit memory or create new context

    def do(self):
        success, fails = self.actions.do()

        return success, fails
