import os

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

def redirect(location, event):
    return {
        "user_exists": False,
        "redirect": {
            "statusCode": 302,
            "headers": {
                "Location": location,
                "Set-Cookie": f"last_location={event['rawPath']}",
            },
        }
    }

def http_or_https():
    return f"http{'s' * ('IS_OFFLINE' not in os.environ)}://"