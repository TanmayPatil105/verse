# window.py
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

import gi

gi.require_version("WebKit", "6.0")
from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import GObject, GLib
from gi.repository import WebKit

from .views.lyrics_view import LyricsView
from .api.spotify import get_now_playing_item
from .api.lyrics import get_lyrics
from .utils.utils import sanitize_lyrics

import time
from threading import Thread


@Gtk.Template(resource_path="/io/github/TanmayPatil105/verse/window.ui")
class VerseWindow(Adw.ApplicationWindow):
    __gtype_name__ = "VerseWindow"

    label = Gtk.Template.Child()
    search_button = Gtk.Template.Child()
    refresh_button = Gtk.Template.Child()
    lyrics_view = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.prev_song = None
        # song details
        self.song = None

        # set up widgets
        self.search_button.connect("clicked", self.on_search_cb)
        self.refresh_button.connect("clicked", self.on_refresh_cb)
        self.refresh_button.bind_property(
            "visible",
            self.search_button,
            "visible",
            GObject.BindingFlags.INVERT_BOOLEAN,
        )
        self.label.bind_property(
            "visible", self.lyrics_view, "visible", GObject.BindingFlags.INVERT_BOOLEAN
        )
        self.lyrics_view.bind_property(
            "visible", self.label, "visible", GObject.BindingFlags.INVERT_BOOLEAN
        )

    def on_search_cb(self, button):
        # call this on a separate thread
        self.fetch_details()
        self.refresh_button.set_visible(True)

    def on_refresh_cb(self, button):
        # call this on a separate thread
        self.fetch_details()

    # runs on a thread
    def fetch_song(self):
        song = get_now_playing_item()
        self.song = song

        if "error" not in song:
            if song["is_playing"]:
                artist = ", ".join([_artist["name"] for _artist in song["artists"]])
                GLib.idle_add(
                    self.label.set_label,
                    "Searching lyrics for {} by {}...".format(song["title"], artist),
                )
            else:
                GLib.idle_add(
                    self.label.set_label, "You have probably paused the song!"
                )
            # fetch lyrics
            # print (song)
            lyrics = get_lyrics(song)

            if "error" not in lyrics:
                self.lyrics = sanitize_lyrics(lyrics["lyrics"])
                GLib.idle_add(self.display_lyrics)
            else:
                GLib.idle_add(self.label.set_label, lyrics["error"])
        else:
            GLib.idle_add(self.label.set_label, song["error"])

    def display_lyrics(self):
        self.lyrics_view.set_visible(True)
        self.lyrics_view.append(self.lyrics, self.song)

    def fetch_details(self):
        self.label.set_label("Fetching song...")
        self.label.set_visible(True)

        # create separate thread
        thread = Thread(target=self.fetch_song)
        thread.start()
