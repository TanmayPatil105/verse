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
from ..utils.secrets import retrieve_secrets


def get_lyrics(song):
    try:
        secrets = retrieve_secrets()
        genius_token = secrets["genius-token"]

        title = song["title"]
        artist = song["artists"][0]["name"]

        genius = lyricsgenius.Genius(genius_token)

        # FIXME: search for all artists
        song = genius.search_song(title, artist)

        if not song:
            return {"error": "Unable to fetch lyrics"}

        return {"lyrics": song.lyrics}
    except:
        return {"error": "Unable to fetch lyrics"}
