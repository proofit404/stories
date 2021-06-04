from app.tools import log


def atomic(f):
    """Manage transactions."""

    def wrapper(*args, **kwargs):
        start_transaction()
        result = f(*args, **kwargs)
        end_transaction()
        return result

    return wrapper


def start_transaction():
    """Perform database query."""
    log("BEGIN TRANSACTION;")


def end_transaction():
    """Perform database query."""
    log("COMMIT TRANSACTION;")


def cancel_transaction():
    """Perform database query."""
    log("ROLLBACK TRANSACTION;")
