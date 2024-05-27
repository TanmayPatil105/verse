# main.py
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

import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Gio, Adw
from .window import VerseWindow
from .views.verse_preferences import VersePreferences
from .lib.secrets import setup_secrets


class VerseApplication(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id="io.github.TanmayPatil105.verse",
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )
        self.create_action("quit", lambda *_: self.quit(), ["<primary>q"])
        self.create_action("about", self.on_about_action)
        self.create_action(
            "preferences", self.on_preferences_action, ["<primary>comma"]
        )

        setup_secrets()

    def do_activate(self):
        self.win = self.props.active_window
        if not self.win:
            self.win = VerseWindow(application=self)
        self.win.present()

    def on_about_action(self, widget, _):
        about = Adw.AboutWindow(
            transient_for=self.props.active_window,
            application_name="verse",
            application_icon="io.github.TanmayPatil105.verse",
            developer_name="Tanmay Patil",
            version="0.1.2",
            developers=["Tanmay Patil"],
            copyright="© 2024 Tanmay Patil",
        )
        about.present()

    def on_preferences_action(self, widget, _):
        self.preferences_window = VersePreferences()
        self.preferences_window.present()

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    app = VerseApplication()
    return app.run(sys.argv)
