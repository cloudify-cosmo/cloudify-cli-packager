import os

from PyInstaller.hooks.hookutils import collect_submodules
from PyInstaller.hooks.hookutils import get_package_paths

hiddenimports = collect_submodules('cloudify')

_relative_ctx_client_path = 'cloudify/proxy'
_pkg_base, _pkg_dir = get_package_paths('cloudify')
_full_ctx_client_path = os.path.join(_pkg_base, _relative_ctx_client_path, 'client.py')

datas = [(_full_ctx_client_path, _relative_ctx_client_path)]
