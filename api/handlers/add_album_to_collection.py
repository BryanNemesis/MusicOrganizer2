import json

from clients.dynamodb import dynamodb_client


def handler(event, context):
    collection_id = event["pathParameters"]["collection_id"]
    try:
        album_id = json.loads(event["body"])["album_id"]
    except (KeyError, TypeError):
        return {
            "statusCode": 400,
            "body": json.dumps({"msg": f"Album id not found in request payload."}),
        }

    result = dynamodb_client.add_album_to_collection(collection_id, album_id)

    if result["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return {
            "statusCode": 201,
            "body": json.dumps({"msg": f"Album added to collection."}),
        }
    else:
        return {
            "statusCode": 500,
            "body": json.dumps(
                {"msg": f"Problem occured when trying to add album to collection."}
            ),
        }
