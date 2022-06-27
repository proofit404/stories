import importlib

import _stories.execute


_stories.execute.instrumented = False


origin_function = _stories.execute.function._execute
origin_coroutine = _stories.execute.coroutine._execute


def _instrumented_function(*args, **kwargs):
    if not _stories.execute.instrumented:
        raise Exception("Use 'r' fixture to run the story")  # pragma: no cover
    return origin_function(*args, **kwargs)


async def _instrumented_coroutine(*args, **kwargs):
    if not _stories.execute.instrumented:
        raise Exception("Use 'r' fixture to run the story")  # pragma: no cover
    return await origin_coroutine(*args, **kwargs)


_stories.execute.function._execute = _instrumented_function
_stories.execute.coroutine._execute = _instrumented_coroutine


class _Function:
    def run(self, story, *args, **kwargs):
        _stories.execute.instrumented = True
        try:
            return story(*args, **kwargs)
        finally:
            _stories.execute.instrumented = False

    def import_module(self, module_name):
        return importlib.import_module(module_name + ".functions")


class _Coroutine:
    def run(self, story, *args, **kwargs):
        _stories.execute.instrumented = True
        try:
            story(*args, **kwargs).send(None)
        except StopIteration as error:
            return error.value
        else:
            raise Exception("A coroutine does not return")  # pragma: no cover
        finally:
            _stories.execute.instrumented = False

    def import_module(self, module_name):
        return importlib.import_module(module_name + ".coroutines")


runners = {"function": _Function(), "coroutine": _Coroutine()}
