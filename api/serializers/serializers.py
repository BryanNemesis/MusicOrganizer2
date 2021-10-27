from typing import List

from tekore.model import FullAlbum, SavedAlbumPaging, Image

def serialize_images(images: List[Image]):
    return [{"size": image.height, "url": image.url} for image in images]

def serialize_full_album(album: FullAlbum):
    album_data = {
        "artist": ", ".join([artist.name for artist in album.artists]),
        "title": album.name,
        "year": album.release_date.split("-")[0],
        "url": album.external_urls["spotify"],
        "images": serialize_images(album.images),
        }
    return album_data 

def serialize_saved_album_paging(paging: SavedAlbumPaging):
    albums = [item.album for item in paging.items]
    album_data = {
        album.id: serialize_full_album(album)
        for album in albums
    }
    return album_data
