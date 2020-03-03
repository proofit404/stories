from concurrent.futures.thread import ThreadPoolExecutor

from _stories.execute.parallel.base import ParallelStoryExecutor


class ThreadsStoryExecutor(ParallelStoryExecutor):
    def __init__(self, workers):
        super(ThreadsStoryExecutor, self).__init__(workers)

    def submit(self, runner, ctx, history, methods, executor):
        futures = []
        with ThreadPoolExecutor(max_workers=self._workers) as pool:
            for method in methods:
                if hasattr(method[0], 'run'):
                    story = method[0]
                    futures.append(pool.submit(executor, runner, ctx, history, story.methods))
                else:
                    futures.append(pool.submit(executor, runner, ctx, history, [method]))

        return tuple(future.result() for future in futures)
