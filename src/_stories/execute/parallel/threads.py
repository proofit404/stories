import types
from concurrent.futures.thread import ThreadPoolExecutor

from _stories.execute.parallel.base import ParallelStoryExecutor


class ThreadsStoryExecutor(ParallelStoryExecutor):
    def __init__(self, workers):
        super(ThreadsStoryExecutor, self).__init__(workers)

    def submit(self, calls, ctx):
        futures = []
        with ThreadPoolExecutor(max_workers=self._workers) as pool:
            for call in calls:
                if isinstance(call, types.MethodType):
                    futures.append(pool.submit(call, ctx))
                else:
                    # TODO: Figure out how to run substories correctly
                    futures.append(pool.submit(call.run))

        return tuple(future.result() for future in futures)
