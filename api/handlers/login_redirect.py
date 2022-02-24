import json

from clients.spotify import user_spotify_client as sp
from utils.utils import get_cookie_value
from models.user import User


def handler(event, _):
    if user_id := get_cookie_value(event, "user_id"):
        if User.get_from_db(user_id):
            return {"statusCode": 200, "body": json.dumps({"user_exists": True})}
    return {
        "statusCode": 200,
        "body": json.dumps({"user_exists": False, "login_url": sp.get_auth_url()}),
    }
