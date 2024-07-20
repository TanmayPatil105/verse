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

        # Genius API injects "You might also like" in lyrics
        lyrics = re.sub(r"You might also like", "", lyrics)

        # Remove "Embed" present at the last
        end_pos = lyrics.rfind("Embed")
        sanitized = lyrics[:end_pos].strip() + "\n"

        return sanitized
    except:
        return lyrics


#
# Genius.com returns incorrect lyrics if the title of the
# song is not passed properly. Here are some examples:
#
#    "See You Again (feat. Charlie Puth)",
# => "See You Again"
#
#    "lovely (with Khalid)",
# => "lovely"
#
#    "Save Your Tears (Remix)(with Ariana Grande)",
# => "Save Your Tears"
#
#    "Wrap me in Plastic - Marcus Layton Radio Edit",
# => "Wrap me in Plastic"
#
#    "Love me like you do - From \"Fifty shades of grey\"",
# => "Love me like you do"
#
#    "A Whole New World (End Title) - From \"Aladdin\"",
# => "A Whole New World End Title"
#
#    "Baby Blue - Remastered 2010",
# => "Baby Blue"
#
#    "Happy working song - From \"Enchanted\"/Soundtrack Version"
# => "Happy working song"
#

def sanitize_title(title):

    # Remove "(feat. #artist)"
    title = re.sub(r"\(feat. [^)]*\)", "", title)

    # Remove "(From movie)"
    title = re.sub(r"\(From [^)]*\)", "", title)

    # Remove "(with #artist)"
    title = re.sub(r"\(with [^)]*\)", "", title)

    # Remove " - From #movie"
    title = re.sub(r" - .*", "", title)

    # Update more keywords if necessary
    title = re.sub(r"remix", "", title, flags=re.IGNORECASE)

    # Remove all round brackets
    title = re.sub(r"\(|\)", "", title)

    return title.strip()

