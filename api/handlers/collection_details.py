import json

from models.collection import Collection
from serializers.serializers import serialize_collection


def handler(event, context):
    collection_id = event["pathParameters"]["collection_id"]
    collection = Collection.get_from_db(collection_id)
    if not collection:
        return {"statusCode": 404, "body": json.dumps({"msg": "Collection not found."})}

    return {"statusCode": 200, "body": json.dumps(serialize_collection(collection))}
