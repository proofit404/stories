class ParallelStoryExecutor(object):
    def __init__(self, workers=None):
        self._workers = workers

    def submit(self, calls, ctx):
        raise NotImplementedError()
