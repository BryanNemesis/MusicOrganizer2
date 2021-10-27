import time
import os

import tekore as tk

from models.user import User
from utils.utils import get_cookie_value, redirect


class UserSpotifyClient:
    def __init__(self):
        if os.environ.get('IS_OFFLINE'):
            config = tk.config_from_environment()[:2] + (os.environ.get('SPOTIFY_REDIRECT_URI_LOCAL'),)
        else:
            config = tk.config_from_environment()
        self.creds = tk.Credentials(*config)
        self.auth = tk.UserAuth(self.creds, "user-library-read")
        self.client = tk.Spotify()

    def authorize(self, event):
        user_id = get_cookie_value(event, "user_id")
        if user_id:
            user = User.get_from_db(user_id)
            if not user:
                return redirect(self.auth.url, event)
            if time.time() >= int(user.token_expires_at):
                token = self.creds.refresh_user_token(user.refresh_token)
                user.update_token(token)
                user.save_to_db()
            return {"user_exists": True, "token": user.access_token}
        return redirect(self.auth.url, event)

    def get_user_token(self, code):
        return self.creds.request_user_token(code)

    def get_current_user_id(self, token):
        with self.client.token_as(token):
            return self.client.current_user().id

    def get_saved_albums(self, code):
        with self.client.token_as(code):
            return self.client.saved_albums()


class AppSpotifyClient:
    def __init__(self):
        config = tk.config_from_environment()
        token = tk.request_client_token(*config[:2])
        self.client = tk.Spotify(token)

    def get_album(self, id):
        # might wanna use "albums" if this is slow but i dont wanna fuck with paging now
        return self.client.album(id)


user_spotify_client = UserSpotifyClient()
app_spotify_client = AppSpotifyClient()
