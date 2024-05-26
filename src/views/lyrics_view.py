# lyrics_view.py
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

gi.require_version("WebKit", "6.0")
from gi.repository import WebKit

from ..lib.html import lyrics_to_html


@Gtk.Template(resource_path="/io/github/TanmayPatil105/verse/views/lyrics_view.ui")
class LyricsView(Adw.Bin):
    __gtype_name__ = "LyricsView"

    carousel = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.pending_view = None

    def append_view(self, view):
        self.carousel.append(view)
        if self.pending_view is None:
            view.connect("load-changed", self.on_view_load_changed)
            self.pending_view = view

    def on_view_load_changed(self, web_view, load_event):
        if load_event == WebKit.LoadEvent.FINISHED:
            web_view.disconnect_by_func(self.on_view_load_changed)
            # instantly scroll
            self.carousel.scroll_to(web_view, False)
            self.pending_view = None

    def append(self, lyrics, song):
        view = WebKit.WebView()
        html = lyrics_to_html(lyrics, song)
        view.load_html(html)
        view.set_vexpand(True)
        view.set_hexpand(True)
        self.append_view(view)

