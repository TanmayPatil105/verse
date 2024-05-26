#
# Source: https://github.com/arnvgh/get-spotify-refresh-token/blob/main/main.py
#

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import dotenv_values

config = dotenv_values(".env")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=config["SPOTIFY_CLIENT_ID"],
        client_secret=config["SPOTIFY_CLIENT_SECRET"],
        redirect_uri=config["SPOTIFY_REDIRECT_URI"],
        scope="user-read-currently-playing",
    )
)

current_user = sp.current_user()

assert current_user is not None

print("Token saved in '.cache' file.")
