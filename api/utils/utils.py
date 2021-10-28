def get_cookie_value(event, name):
    try:
        value = [
                cookie.split("=")[1]
                for cookie in event["cookies"]
                if cookie.startswith(name)
            ][0]
    except (IndexError, KeyError):
        return None
    return value
