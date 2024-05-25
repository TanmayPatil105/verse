pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'verse'
moduledir_api = pkgdatadir / 'verse' / 'api'
moduledir_utils = pkgdatadir / 'verse' / 'utils'
moduledir_views = pkgdatadir / 'verse' / 'views'
gnome = import('gnome')

gnome.compile_resources('verse',
  'verse.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'verse.in',
  output: 'verse',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr-xr-x'
)

verse_sources = [
  '__init__.py',
  'main.py',
  'window.py',
]

verse_sources_api = [
  'api/spotify.py',
  'api/lyrics.py',
]

verse_sources_utils = [
  'utils/utils.py',
]

verse_sources_views = [
  'views/lyrics_view.py',
]

install_data(verse_sources, install_dir: moduledir)
install_data(verse_sources_api, install_dir: moduledir_api)
install_data(verse_sources_utils, install_dir: moduledir_utils)
install_data(verse_sources_views, install_dir: moduledir_views)
