import json

from clients.dynamodb import dynamodb_client


def handler(event, context):
    collection_id = event["pathParameters"]["collection_id"]
    try:
        body = json.loads(event["body"])
        album_id = body["album_id"]
        operation = body["operation"]
    except (KeyError, TypeError):
        return {
            "statusCode": 400,
            "body": json.dumps({"msg": f"Incorrect request payload."}),
        }

    if operation == "add":
        result = dynamodb_client.add_album_to_collection(collection_id, album_id)
    elif operation == "remove":
        result = dynamodb_client.remove_album_from_collection(collection_id, album_id)
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"msg": f"Incorrect request payload."}),
        }

    if result["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return {
            "statusCode": 201,
            "body": json.dumps(
                {
                    "msg": f"Album {'added to' if operation == 'add' else 'removed from'} collection."
                }
            ),
        }
    else:
        return {
            "statusCode": 500,
            "body": json.dumps(
                {
                    "msg": f"Problem occured when trying to {operation} album {'to' if operation == 'add' else 'from'} collection."
                }
            ),
        }
