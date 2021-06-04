async def _execute(steps, story, state):
    for step in steps:
        method = getattr(story, step)
        await method(state)
