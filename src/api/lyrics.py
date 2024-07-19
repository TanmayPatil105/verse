# lyrics.py
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

import os
import lyricsgenius
from ..lib.secrets import retrieve_secrets
from ..lib.utils import sanitize_title


def get_lyrics(song):
    try:
        secrets = retrieve_secrets()
        genius_token = secrets["genius-token"]
        genius = lyricsgenius.Genius(genius_token, verbose=False)

        title = sanitize_title(song["title"])

        for artist in song["artists"]:
            artist_name = artist["name"]
            song = genius.search_song(title, artist_name)
            if song:
                break

        if not song:
            return {
                "error": "No Lyrics found",
                "description": f"Couldn't find the lyrics for {title}",
            }

        return {"lyrics": song.lyrics}
    except:
        return {
            "error": "Unable to fetch lyrics",
            "description": "Please ensure that the Genius token is valid in the Preferences.",
        }
