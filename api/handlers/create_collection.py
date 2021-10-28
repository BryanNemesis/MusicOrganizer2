import json

from models.collection import Collection
from utils.utils import get_cookie_value


def handler(event, context):
    try:
        name = json.loads(event["body"])["name"]
    except (KeyError, TypeError):
        return {
            "statusCode": 400,
            "body": json.dumps(
                {"msg": f"Collection name not found in request payload."}
            ),
        }

    collection = Collection(name)
    result = collection.save_to_db()
    current_user_id = get_cookie_value(event, "user_id")
    collection.add_for_user(current_user_id)

    if result["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return {
            "statusCode": 201,
            "body": json.dumps(
                {"msg": f"Collection {name} with id {collection.id} created."}
            ),
        }
    else:
        return {
            "statusCode": 500,
            "body": json.dumps(
                {"msg": f"Problem occured when trying to save collection {name}."}
            ),
        }
