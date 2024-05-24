# WIP: verse

Displays the lyrics of the song currently playing on Spotify.

![Example](./images/verse.png)

## Build

### Linux

Required packages for Debian, Ubuntu, Mint etc.
```
sudo apt install meson ninja-build python-setuptools libgtk-4-dev libadwaita-1-0
```

Build locally:
```
meson setup _build
meson compile -C _build
meson install -C _build
```

Build using [GNOME Builder](https://flathub.org/apps/org.gnome.Builder)
