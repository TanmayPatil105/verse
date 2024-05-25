# secrets.py
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

gi.require_version("Secret", "1")
from gi.repository import Secret
import json

APP_ID = "io.github.TanmayPatil105.verse"

attrs = {"api_keys": Secret.SchemaAttributeType.STRING}

SECRET_SCHEMA = None
SECRET_KEY = "Verse-Login"

secrets_dict = {
    "client-id": None,
    "client-secret": None,
    "refresh-token": None,
    "genius-token": None,
}


def setup_secrets():
    global SECRET_SCHEMA
    global attrs
    if SECRET_SCHEMA is None:
        SECRET_SCHEMA = Secret.Schema.new(APP_ID, Secret.SchemaFlags.NONE, attrs)


def retrieve_secrets():
    global SECRET_SCHEMA
    password = Secret.password_lookup_sync(SECRET_SCHEMA, {}, None)

    try:
        if password:
            secrets = json.loads(password)
            return secrets

    except Exception as error:
        return None


def update_secrets(
    client_id=None, client_secret=None, refresh_token=None, genius_token=None
):
    global SECRET_SCHEMA
    secrets = retrieve_secrets()
    if secrets is None:
        secrets = secrets_dict

    if client_id is not None:
        secrets["client-id"] = client_id
    if client_secret is not None:
        secrets["client-secret"] = client_secret
    if refresh_token is not None:
        secrets["refresh-token"] = refresh_token
    if genius_token is not None:
        secrets["genius-token"] = genius_token

    json_data = json.dumps(secrets, indent=2)

    Secret.password_store_sync(
        SECRET_SCHEMA, {}, Secret.COLLECTION_DEFAULT, SECRET_KEY, json_data, None
    )

    print(secrets)
