from typing import List

import uuid
from tekore.model import FullAlbum

from clients.dynamodb import dynamodb_client
from clients.spotify import app_spotify_client as sp


class Collection:
    def __init__(self, name: str, image_url: str = "", albums: List[FullAlbum] = []):
        self.id = uuid.uuid4()
        self.name = name
        self.image_url = image_url
        self.albums = albums

    def save_to_db(self):
        album_ids = [album.id for album in self.albums]
        item = {
            "id": {"S": str(self.id)},
            "name": {"S": self.name},
            "image_url": {"S": self.image_url},
            "albums": {"SS": album_ids if album_ids else [""]},
        }
        return dynamodb_client.save_collection(item)

    def add_for_user(self, user_id):
        return dynamodb_client.update_user_collections_list(user_id, self.id)

    @classmethod
    def get_from_db(cls, id, get_albums=True):
        try:
            data = dynamodb_client.get_collection(id)["Item"]
        except KeyError:
            return None
        if get_albums:
            albums = [sp.get_album(album_id) for album_id in data["albums"]["SS"]]
        else:
            albums = []
        return Collection(
            name=data["name"]["S"], image_url=data["image_url"]["S"], albums=albums
        )
