class _Step:
    def __init__(self):
        self.steps = []

    def __getattr__(self, name):
        self.steps.append(name)
