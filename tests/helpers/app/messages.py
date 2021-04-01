def send_notification(user_id):
    keys = {1: False, 2: True}
    if keys[user_id]:
        raise Exception
