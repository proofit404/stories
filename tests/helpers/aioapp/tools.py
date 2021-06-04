async def log(*args, **kwargs):
    """Print."""
    __builtins__["print"](*args, **kwargs)
