from dataclasses import make_dataclass


def initiate(cls):
    """Create story with all steps required in constructor argument."""
    return make_dataclass(
        cls.__name__, cls.__call__.steps, namespace={"__call__": cls.__call__}
    )
