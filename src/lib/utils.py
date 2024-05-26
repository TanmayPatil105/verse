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
    sanitized = re.sub(r"\([^\)]*\)", "", title)
    # sanitized = re.sub(r"\(with\. [^\)]*\)", "", sanitized)
    return sanitized.strip()

