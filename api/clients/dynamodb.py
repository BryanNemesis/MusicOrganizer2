import boto3


class DynamodbClient:
    def __init__(self):
        self.client = boto3.client("dynamodb")

    def get_user(self, user_id):
        return self.client.get_item(TableName="users", Key={"user_id": {"S": user_id}})

    def save_user(self, item):
        return self.client.put_item(TableName="users", Item=item)


dynamodb_client = DynamodbClient()
