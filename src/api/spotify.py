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

# api endpoints
NOW_PLAYING_ENDPOINT = "https://api.spotify.com/v1/me/player/currently-playing"
TOKEN_ENDPOINT = "https://accounts.spotify.com/api/token"


def get_access_token():

    try:
        client_id = os.environ.get("CLIENT_ID")
        client_secret = os.environ.get("CLIENT_SECRET")
        refresh_token = os.environ.get("REFRESH_TOKEN")

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

    except requests.exceptions.RequestException as e:
        print(f"Error obtaining access token: {e}")
        return None


def get_now_playing(access_token):
    if not access_token:
        return {"error": "Invalid access token"}

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
            "error": "Unable to obtain access token. Make sure CLIENT_ID and CLIENT_SECRET are correct."
        }

    song = get_now_playing(access_token)
    if not song:
        return {"error": "You are probably offline!"}

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
        return {"error": "Ads :/"}


if __name__ == "__main__":
    now_playing_item = get_now_playing_item()
    print(now_playing_item)
