# spotify.py
#
# Copyright 2024 Tanmay Patil <tanmaynpatil105@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

import base64
import requests
import os
from urllib.parse import urlencode
from spotipy.oauth2 import SpotifyOAuth, CacheFileHandler
from ..lib.secrets import retrieve_secrets

# api endpoints
NOW_PLAYING_ENDPOINT = "https://api.spotify.com/v1/me/player/currently-playing"
TOKEN_ENDPOINT = "https://accounts.spotify.com/api/token"


def get_access_token():

    try:
        secrets = retrieve_secrets()
        client_id = secrets["client-id"]
        client_secret = secrets["client-secret"]
        refresh_token = secrets["refresh-token"]

        basic = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        response = requests.post(
            TOKEN_ENDPOINT,
            headers={
                "Authorization": f"Basic {basic}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data=urlencode(
                {
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                }
            ),
        )

        response.raise_for_status()

        return response.json()["access_token"]

    except:
        # callee sets the error
        return None


def get_now_playing(access_token):
    try:
        response = requests.get(
            NOW_PLAYING_ENDPOINT,
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )
        response.raise_for_status()

        return response.json()
    except:
        return None


def get_now_playing_item():
    access_token = get_access_token()

    if not access_token:
        return {
            "error": "Unable to obtain access token.",
            "description": "Please ensure that the CLIENT_ID and CLIENT_SECRET are valid in the Preferences.",
        }

    song = get_now_playing(access_token)
    if not song:
        return {
            "error": "You are currently not listening to anything!",
            "description": "Would you like to try again?",
        }

    try:
        artists = song["item"]["artists"]
        is_playing = song["is_playing"]
        title = song["item"]["name"]

        return {
            "title": title,
            "artists": artists,
            "is_playing": is_playing,
        }
    except:
        return {"error": "Uh-oh, smells like Ads", "description": "It'll pass.."}

def generate_refresh_token():
    if "XDG_CACHE_HOME" in os.environ:
        CACHE_PATH = os.path.join(os.environ.get("XDG_CACHE_HOME"), ".cache")
    else:
        CACHE_PATH = "/tmp/.cache"

    try:
        CACHE_PATH = os.path.join(os.environ.get("XDG_CACHE_HOME"), ".cache")
        secrets = retrieve_secrets()
        client_id = secrets["client-id"]
        client_secret = secrets["client-secret"]
        REDIRECT_URI = "http://localhost:3000"

        cache_handler = CacheFileHandler(cache_path=CACHE_PATH)

        sp_oauth = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=REDIRECT_URI,
            scope="user-read-currently-playing",
            cache_handler=cache_handler,
        )

        _auth_code = sp_oauth.get_auth_response()

        _access_token = sp_oauth.get_access_token(_auth_code, as_dict=False)
        refresh_token = sp_oauth.cache_handler.get_cached_token().get("refresh_token")

        if os.path.exists(CACHE_PATH):
            os.remove(CACHE_PATH)

        return {"refresh_token": refresh_token}
    except:
        if os.path.exists(CACHE_PATH):
            os.remove(CACHE_PATH)

        return {
            "error": "Couldn't fetch",
            "description": "Make sure API tokens are valid",
        }
