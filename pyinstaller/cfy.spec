# -*- mode: python -*-
import pkg_resources
import os
from platform import system
from PyInstaller.hooks.hookutils import get_package_paths


def Entrypoint(dist, group, name,
               scripts=None, pathex=None, hiddenimports=None,
               hookspath=None, excludes=None, runtime_hooks=None):
    import pkg_resources
    scripts = scripts or []
    pathex = pathex or []
    # get the entry point
    ep = pkg_resources.get_entry_info(dist, group, name)
    # insert path of the egg at the verify front of the search path
    pathex = [ep.dist.location] + pathex
    # script name must not be a valid module name to avoid name clashes on import
    script_path = os.path.join(WORKPATH, name + '-script.py')
    print "creating script for entry point", dist, group, name
    with open(script_path, 'w') as fp:
        fp.write("import {}\n".format(ep.module_name))
        fp.write("{}.{}()\n".format(ep.module_name, '.'.join(ep.attrs)))

    return Analysis([script_path] + scripts, pathex, hiddenimports, hookspath, excludes, runtime_hooks)

if 'Windows' == system():
    binary_name = 'cfy.exe'
else:
    binary_name = 'cfy'

# add keystoneclient & novaclient egg-info directories to TOC for metadata
# support (pyinstaller doesn't support egg dirs yet)
keystoneclient = pkg_resources.get_distribution('python_keystoneclient')
keystoneclient_egg = keystoneclient.egg_name() + '.egg-info'
keystoneclient_tree = Tree(keystoneclient.location + '/' + keystoneclient_egg, keystoneclient_egg)

novaclient = pkg_resources.get_distribution('python_novaclient')
novaclient_egg = novaclient.egg_name() + '.egg-info'
novaclient_tree = Tree(novaclient.location + '/' +  novaclient_egg,  novaclient_egg)

# add provider modules to build
provider_packages = ['cloudify_openstack', 'cloudify_simple_provider']
provider_package_paths = [get_package_paths(pkg)[1] + '/' + pkg + '.py' for pkg in provider_packages]

# add VERSION file
cli_module_name = 'cloudify_cli'
version_path = pkg_resources.resource_filename(cli_module_name, 'VERSION')
version_file = [(os.path.join('cosmo_cli', 'VERSION'), version_path, 'DATA')]

a = Entrypoint('cloudify', 'console_scripts', 'cfy',
               scripts=provider_package_paths,
               hiddenimports=provider_packages,
               hookspath=['./hooks'])

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name=binary_name,
          debug=False,
          strip=None,
          upx=True,
          console=True)
coll = COLLECT(exe,
               keystoneclient_tree,
               novaclient_tree,
               version_file,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='cfy')

