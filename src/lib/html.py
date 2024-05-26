# html.py
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


import random

def lyrics_to_html(lyrics, song):
    backgrounds = [
        "#00838F",
        "#F08080",
        "#FEE569",
        "#6A0Dad",
        "#A0C8A0",
        "#D3A7A4",
        "#87CEEB",
        "#40E0D0",
        "#FFFACD",
        "#E0B0FF",
        "#C8A2C8",
    ]

    background = random.choice(backgrounds)

    text_color = "#241F31"
    h2_color = "#FFFFFF"

    if background == "#FFFACD" or background == "#FEE569":
        h2_color = "#0047AB"
    elif background == "#40E0D0":
        h2_color = "#800020"

    styles = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
        body {
          font-family: 'Montserrat', sans-serif;
          background-color: %s;
          padding: 40px;
          text-align: center;
          color: %s;
        }

        h1 {
          font-size: 48px;
          font-weight: bold;
          margin-bottom: 10px;
        }

        h1.artist {
          font-size: 36px;
          font-weight: bold;
          margin-bottom: 20px;
        }

        h2 {
          font-size: 30px;
          color: %s;
          font-weight: bold;
          text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
          margin-bottom: 30px;
        }

        p {
          font-size: 24px;
          line-height: 1.5;
          margin: 15px 0;
          font-weight: 500;
          text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
        }
    </style>
    """ % (
        background,
        text_color,
        h2_color,
    )

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