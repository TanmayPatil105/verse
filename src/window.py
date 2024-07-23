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
from .lib.utils import sanitize_lyrics

import time
from threading import Thread


@Gtk.Template(resource_path="/io/github/TanmayPatil105/verse/window.ui")
class VerseWindow(Adw.ApplicationWindow):
    __gtype_name__ = "VerseWindow"

    box = Gtk.Template.Child()
    status = Gtk.Template.Child()
    search_button = Gtk.Template.Child()
    refresh_button = Gtk.Template.Child()
    lyrics_view = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # song details
        self.song = None

        # set up widgets
        self.refresh_button.bind_property(
            "visible",
            self.search_button,
            "visible",
            GObject.BindingFlags.INVERT_BOOLEAN,
        )
        self.status.bind_property(
            "visible", self.lyrics_view, "visible", GObject.BindingFlags.INVERT_BOOLEAN
        )
        self.lyrics_view.bind_property(
            "visible", self.status, "visible", GObject.BindingFlags.INVERT_BOOLEAN
        )

    @Gtk.Template.Callback()
    def on_search_cb(self, button):
        # call this on a separate thread
        self.fetch_details()

    def song_unchanged(self, song):
        if self.song and song:
            try:
                if (
                    self.song["title"] == song["title"]
                    and self.song["artists"] == song["artists"]
                ):
                    return True
            except:
                return False

        return False

    # runs on a thread
    def fetch_song(self):
        song = get_now_playing_item()

        if "error" not in song:
            # if song is unchanged, do not fetch
            if self.song_unchanged(song):
                # show lyrics
                self.box.set_valign(Gtk.Align.FILL)
                self.lyrics_view.set_visible(True)
                return

            if song["is_playing"]:

                artist = ", ".join([_artist["name"] for _artist in song["artists"]])
                GLib.idle_add(
                    self.status.set_title,
                    "Searching lyrics for {}..".format(song["title"], artist),
                )
                GLib.idle_add(
                    self.status.set_description,
                    "by {}".format(artist),
                )
            else:
                GLib.idle_add(self.status.set_title, "Song is Paused!")
                GLib.idle_add(self.status.set_description, "Here's the lyrics anyway..")

            # fetch lyrics
            lyrics = get_lyrics(song)

            if "error" not in lyrics:
                self.song = song
                self.lyrics = sanitize_lyrics(lyrics["lyrics"])
                GLib.idle_add(self.display_lyrics)
            else:
                GLib.idle_add(self.status.set_title, lyrics["error"])
                GLib.idle_add(self.status.set_description, lyrics["description"])
        else:
            GLib.idle_add(self.status.set_title, song["error"])
            GLib.idle_add(self.status.set_description, song["description"])

    def display_lyrics(self):
        self.box.set_valign(Gtk.Align.FILL)
        self.lyrics_view.append(self.lyrics, self.song)
        self.lyrics_view.set_visible(True)

    def fetch_details(self):
        if self.refresh_button.get_visible() == False:
            self.refresh_button.set_visible(True)

        self.box.set_valign(Gtk.Align.CENTER)
        self.status.set_title("Fetching song...")
        self.status.set_description(None)
        self.status.set_visible(True)

        # create separate thread
        thread = Thread(target=self.fetch_song)
        thread.start()
