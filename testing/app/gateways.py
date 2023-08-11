from app.entities import CustomerId


def send_notification(user_id: CustomerId) -> None:
    keys = {1: False, 2: True}
    if keys[user_id]:
        raise Exception
