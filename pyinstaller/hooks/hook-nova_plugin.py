from PyInstaller.hooks.hookutils import collect_submodules
hiddenimports = collect_submodules('nova_plugin')
