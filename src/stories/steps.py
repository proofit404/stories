class Steps:
    def __init__(self):
        self.__steps__ = []

    def __getattr__(self, name):
        self.__steps__.append(name)
