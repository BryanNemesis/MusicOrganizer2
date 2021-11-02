import json

from clients.dynamodb import dynamodb_client


def handler(event, context):
    try:
        collection_id = event["queryStringParameters"]["collection_id"]
    except (TypeError, KeyError):
        return {
            "statusCode": 400,
            "body": json.dumps(
                {"msg": "collection_id parameter not found in query string."}
            ),
        }

    result = dynamodb_client.delete_collection(collection_id)

    if result["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return {
            "statusCode": 200,
            "body": json.dumps(
                {"msg": "Collection deleted (or it wasn't there already)."}
            ),
        }

    else:
        return {
            "statusCode": 500,
            "body": json.dumps(
                {"msg": "Problem occured when trying to delete collection."}
            ),
        }
