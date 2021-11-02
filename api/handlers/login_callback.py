import json

from clients.spotify import user_spotify_client as sp
from models.user import User


def handler(event, context):
    code = event["queryStringParameters"]["code"]
    token = sp.get_new_user_token(code)
    user_id = sp.get_current_user_id(token)
    user = User(user_id, token)
    result = user.save_to_db()

    return (
        {
            "statusCode": 200,
            "body": json.dumps({"msg": "Login successful"}),
            "headers": {
                "Set-Cookie": f"user_id={user_id}",
            },
        }
        if result["ResponseMetadata"]["HTTPStatusCode"] == 200
        else {
            "statusCode": 500,
            "body": json.dumps({"msg": "Error while trying to save user"}),
        }
    )
