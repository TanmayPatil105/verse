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
from ..utils.secrets import retrieve_secrets, update_secrets


@Gtk.Template(
    resource_path="/io/github/TanmayPatil105/verse/views/verse_preferences.ui"
)
class VersePreferences(Adw.PreferencesDialog):
    __gtype_name__ = "VersePreferences"

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

        self.update_widgets()

    @Gtk.Template.Callback()
    def client_id_row_applied_cb(self, widget, *args):
        client_id = self.client_id_row.get_text()
        update_secrets(client_id=client_id)

    @Gtk.Template.Callback()
    def client_secret_row_applied_cb(self, widget, *args):
        client_secret = self.client_secret_row.get_text()
        update_secrets(client_secret=client_secret)

    @Gtk.Template.Callback()
    def refresh_token_row_applied_cb(self, widget, *args):
        refresh_token = self.refresh_token_row.get_text()
        print(refresh_token)
        update_secrets(refresh_token=refresh_token)

    @Gtk.Template.Callback()
    def genius_token_row_applied_cb(self, widget, *args):
        genius_token = self.genius_token_row.get_text()
        update_secrets(genius_token=genius_token)

    def update_widgets(self):
        secrets = retrieve_secrets()

        if secrets.get("client-id"):
            self.client_id_row.set_text(secrets["client-id"])

        if secrets.get("client-secret"):
            self.client_secret_row.set_text(secrets["client-secret"])

        if secrets.get("refresh-token"):
            self.refresh_token_row.set_text(secrets["refresh-token"])

        if secrets.get("genius-token"):
            self.genius_token_row.set_text(secrets["genius-token"])

    def open_wiki(self, button, url):
        GLib.spawn_command_line_async(f"xdg-open {url}")

    def wiki_get_token(self, url):
        info = Gtk.Button()
        info.set_icon_name("dialog-information-symbolic")
        info.set_tooltip_text(_("How to get a token"))
        info.add_css_class("flat")
        info.set_valign(Gtk.Align.CENTER)
        info.connect("clicked", self.open_wiki, url)
        return info
