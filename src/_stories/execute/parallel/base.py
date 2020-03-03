class ParallelStoryExecutor(object):
    def __init__(self, workers=None):
        self._workers = workers

    def submit(self, runner, ctx, history, methods, executor):
        raise NotImplementedError()
