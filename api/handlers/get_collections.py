import json

from clients.dynamodb import dynamodb_client
from models.collection import Collection
from serializers.serializers import serialize_collection_list


def handler(event, context):
    try:
        user_id = event["queryStringParameters"]["user_id"]
    except (TypeError, KeyError):
        return {
            "statusCode": 400,
            "body": json.dumps({"msg": "user_id parameter not found in query string."}),
        }

    collection_ids = dynamodb_client.get_user_collection_ids(user_id)
    if not collection_ids:
        return {"statusCode": 404, "body": json.dumps({"msg": "User not found."})}

    collections = [
        Collection.get_from_db(id, get_albums=False) for id in collection_ids
    ]
    return {
        "statusCode": 200,
        "body": json.dumps(serialize_collection_list(collections)),
    }
