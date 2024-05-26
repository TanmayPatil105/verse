# utils.py
#
# Copyright 2024 Tanmay Patil <tanmaynpatil105@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0


import re

def sanitize_lyrics(lyrics):
    try:
        # Remove till "Lyrics" from fetched lyrics
        start_pos = lyrics.find("Lyrics") + len("Lyrics")
        lyrics = lyrics[start_pos:]

        # Remove "Embed" present at the last
        end_pos = lyrics.rfind("Embed")
        sanitized = lyrics[:end_pos].strip() + "\n"

        return sanitized
    except:
        return lyrics

def sanitize_title(title):
    sanitized = re.sub(r'\(feat\. [^\)]*\)', '', title)
    return sanitized.strip()

def lyrics_to_html(lyrics, song):
    styles = """
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #2ec27e;
            padding: 20px;
            text-align: center;
        }
        h1.artist {
            font-size: 28px;
        }
        h2 {
            font-size: 30px;
            color: #f6f5f4;
            font-weight: bold;
        }
        p {
            font-size: 23px;
            color: #241F31;;
            margin: 10px 0;
        }
    </style>
    """

    html = "<!DOCTYPE html>\n<html>\n<head>{}</head>\n<body>".format(styles)

    lines = lyrics.split("\n")
    html += "<h1>{}</h1>\n".format(song["title"])
    artist = ", ".join([_artist["name"] for _artist in song["artists"]])
    html += '<h1 class="artist">by {}</h1>'.format(artist)
    for line in lines:
        if line.startswith("["):
            html += "\t<h2>{}</h2>\n".format(line)
        else:
            html += "\t<p>{}</p>\n".format(line)

    html += "\t</body>\n</html>"

    return html
