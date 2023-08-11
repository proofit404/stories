from typing import Any


async def log(*args: object, **kwargs: Any) -> None:
    """Print."""
    __builtins__["print"](*args, **kwargs)
