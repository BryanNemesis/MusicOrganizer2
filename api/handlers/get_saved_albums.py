import json

from clients.spotify import user_spotify_client as sp
from serializers.serializers import serialize_saved_album_paging


def handler(event, context):
    token = sp.get_user_token(event)
    if not token:
        return {
            "statusCode": 400,
            "body": json.dumps({"msg": "Could not get user token."})
        }

    saved_albums_paging = sp.get_saved_albums(token)
    album_data = serialize_saved_album_paging(saved_albums_paging)

    response = {"statusCode": 200, "body": json.dumps(album_data)}
    
    return response