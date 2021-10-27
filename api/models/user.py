import time

from tekore import Token

from clients.dynamodb import dynamodb_client


class User:
    def __init__(self, id: int, token: Token):
        self.id = id
        self.refresh_token = token.refresh_token
        self.access_token = token.access_token
        self.token_expires_at = token.expires_at

    def save_to_db(self):
        item = {
            "user_id": {"S": self.id},
            "access_token": {"S": self.access_token},
            "refresh_token": {"S": self.refresh_token},
            "token_expires_at": {"N": str(self.token_expires_at)},
        }
        return dynamodb_client.save_user(item)

    def update_token(self, token: Token):
        self.refresh_token = token.refresh_token
        self.access_token = token.access_token
        self.token_expires_at = token.expires_at

    @classmethod
    def get_from_db(cls, id):
        try:
            data = dynamodb_client.get_user(id)["Item"]
        except KeyError:
            return None
        token = Token(
            token_info={
                "access_token": data["access_token"]["S"],
                "refresh_token": data["refresh_token"]["S"],
                "expires_in": int(data["token_expires_at"]["N"]) - int(time.time()),
                "token_type": "Bearer",
            },
            uses_pkce=False,
        )
        return User(
            id=id,
            token=token,
        )
