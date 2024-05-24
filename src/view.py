# view.py
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

import gi
from gi.repository import Adw
from gi.repository import Gtk
gi.require_version('WebKit', '6.0')
from gi.repository import WebKit

from .utils.utils import lyrics_to_html

@Gtk.Template(resource_path='/io/github/TanmayPatil105/verse/lyrics-view.ui')
class LyricsView(Adw.Bin):
    __gtype_name__ = 'LyricsView'

    carousel = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.pages = []

        # temporary work around to append other pages
        view = WebKit.WebView()
        view.load_uri("https://www.gnome.org")
        view.set_vexpand(True)
        view.set_hexpand(True)
        view.set_visible(True)

        self.append_view(view)


    def append_view(self, view):
        self.pages.append(view)

        self.carousel.append(view)
        self.carousel.scroll_to(view, True)

    def append(self, lyrics, song):
        view = WebKit.WebView()
        html = lyrics_to_html(lyrics, song)
        view.load_html(html)
        view.set_visible(True)
        view.set_vexpand(True)
        view.set_hexpand(True)
        self.append_view(view)

