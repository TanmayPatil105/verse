# verse_preferences.py
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

from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import GLib

@Gtk.Template(resource_path='/io/github/TanmayPatil105/verse/views/verse_preferences.ui')
class VersePreferences(Adw.PreferencesDialog):
    __gtype_name__ = 'VersePreferences'

    client_id_row = Gtk.Template.Child()
    client_secret_row = Gtk.Template.Child()
    refresh_token_row = Gtk.Template.Child()
    genius_token_row = Gtk.Template.Child()

    wiki_spotify_url = "https://github.com/TanmayPatil105/verse/tree/main/wiki#spotify"
    wiki_genius_url = "https://github.com/TanmayPatil105/verse/tree/main/wiki#genius"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.client_id_row.add_suffix(self.wiki_get_token(self.wiki_spotify_url))
        self.client_secret_row.add_suffix(self.wiki_get_token(self.wiki_spotify_url))
        self.refresh_token_row.add_suffix(self.wiki_get_token(self.wiki_spotify_url))
        self.genius_token_row.add_suffix(self.wiki_get_token(self.wiki_genius_url))

    def open_wiki(self, button, url):
        GLib.spawn_command_line_async(
            f"xdg-open {url}"
        )

    def wiki_get_token(self, url):
        info = Gtk.Button()
        info.set_icon_name("dialog-information-symbolic")
        info.set_tooltip_text(_("How to get a token"))
        info.add_css_class("flat")
        info.set_valign(Gtk.Align.CENTER)
        info.connect("clicked", self.open_wiki, url)
        return info

