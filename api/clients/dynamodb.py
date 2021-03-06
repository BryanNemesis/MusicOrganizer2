import boto3


class DynamodbClient:
    def __init__(self):
        self.client = boto3.client("dynamodb")

    def get_user(self, user_id):
        return self.client.get_item(TableName="users", Key={"user_id": {"S": user_id}})

    def add_collection_to_user(self, user_id, collection_id):
        return self.client.update_item(
            TableName="users",
            Key={"user_id": {"S": str(user_id)}},
            UpdateExpression="ADD collections :c",
            ExpressionAttributeValues={":c": {'SS': [str(collection_id)]}}
        )

    def get_user_collection_ids(self, user_id):
        user = self.client.get_item(TableName="users", Key={"user_id": {"S": user_id}})
        try:
            return user['Item']['collections']['SS']
        except KeyError:
            return None

    def save_user(self, item):
        return self.client.put_item(TableName="users", Item=item)

    def get_collection(self, id):
        return self.client.get_item(TableName="collections", Key={"id": {"S": id}})

    def save_collection(self, item):
        return self.client.put_item(TableName="collections", Item=item)

    def delete_collection(self, id):
        return self.client.delete_item(TableName="collections", Key={"id": {"S": id}})

    def add_album_to_collection(self, collection_id, album_id):
        return self.client.update_item(
            TableName="collections",
            Key={"id": {"S": str(collection_id)}},
            UpdateExpression="ADD albums :a",
            ExpressionAttributeValues={":a": {'SS': [album_id]}}
        )

    def remove_album_from_collection(self, collection_id, album_id):
        return self.client.update_item(
            TableName="collections",
            Key={"id": {"S": str(collection_id)}},
            UpdateExpression="DELETE albums :a",
            ExpressionAttributeValues={":a": {'SS': [album_id]}}
        )

dynamodb_client = DynamodbClient()
