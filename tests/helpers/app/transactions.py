log = __builtins__["print"]


def atomic(f):
    def wrapper(*args, **kwargs):
        start_transaction()
        result = f(*args, **kwargs)
        end_transaction()
        return result

    return wrapper


def start_transaction():
    log("BEGIN TRANSACTION;")


def end_transaction():
    log("COMMIT TRANSACTION;")


def cancel_transaction():
    log("ROLLBACK TRANSACTION;")
