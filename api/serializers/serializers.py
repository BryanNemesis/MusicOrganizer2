from typing import List

from tekore.model import FullAlbum, SavedAlbumPaging, Image
from models.collection import Collection

def serialize_images(images: List[Image]):
    return [{"size": image.height, "url": image.url} for image in images]

def serialize_full_album(album: FullAlbum):
    return {
        "id": album.id,
        "artist": ", ".join(artist.name for artist in album.artists),
        "title": album.name,
        "year": album.release_date.split("-")[0],
        "url": album.external_urls["spotify"],
        "images": serialize_images(album.images),
    } 

def serialize_saved_album_paging(paging: SavedAlbumPaging):
    albums = [item.album for item in paging.items]
    return {
        album.id: serialize_full_album(album)
        for album in albums
    }

def serialize_collection_list(collections: List[Collection]):
    return [
        {
            "id": str(collection.id),
            "name": collection.name,
            "image_url": collection.image_url
            }
        for collection in collections
    ]

def serialize_collection(collection: Collection):
    return {
        "id": str(collection.id),
        "name": collection.name,
        "image_url": collection.image_url,
        "albums": [serialize_full_album(album) for album in collection.albums]
    }
