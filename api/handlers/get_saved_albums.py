import json

from clients.spotify import spotify_client
from serializers.serializers import serialize_saved_album_paging


def handler(event, context):
    auth_result = spotify_client.authorize(event)
    if not auth_result['user_exists']:
        return auth_result['redirect']

    saved_albums_paging = spotify_client.get_saved_albums(auth_result['token'])
    album_data = serialize_saved_album_paging(saved_albums_paging)

    response = {"statusCode": 200, "body": json.dumps(album_data)}
    
    return response