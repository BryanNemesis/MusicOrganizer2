import json
import os

from clients.spotify import spotify_client
from utils.utils import get_cookie_value, http_or_https
from models.user import User


def handler(event, context):
    code = event["queryStringParameters"]["code"]
    token = spotify_client.get_user_token(code)
    user_id = spotify_client.get_current_user_id(token)
    user = User(user_id, token)
    result = user.save_to_db()

    if result["ResponseMetadata"]["HTTPStatusCode"] == 200:
        response = {
            "statusCode": 302,
            "headers": {
                "Location": f"{http_or_https()}{event['headers'].get('host') or event['headers'].get('Host')}{get_cookie_value(event, 'last_location')}",
                "Set-Cookie": f"user_id={user_id}",
            },
        }
    else:
        response = {
            "statusCode": 400,
            "body": json.dumps({"msg": f"Error while trying to add user"}),
        }

    return response
