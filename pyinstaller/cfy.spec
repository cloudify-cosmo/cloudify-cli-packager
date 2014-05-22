# -*- mode: python -*-
import pkg_resources
import cosmo_manager_rest_client
import os
from sys import platform
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
    fp = open(script_path, 'w')
    try:
        print >>fp, "import", ep.module_name
        print >>fp, "%s.%s()" % (ep.module_name, '.'.join(ep.attrs))
    finally:
        fp.close()

    return Analysis([script_path] + scripts, pathex, hiddenimports, hookspath, excludes, runtime_hooks)

if platform in ('win32', 'win64', 'cygwin'):
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

# add cosmo_manager_rest_client.swagger directory to TOC
swagger = os.path.dirname(cosmo_manager_rest_client.__file__)
swagger_tree = Tree(swagger + '/swagger', 'swagger')

# add cloudify_openstack package to build
provider_package = 'cloudify_openstack'
provider_package_path = get_package_paths(provider_package)[1] + '/' + provider_package + '.py'

a = Entrypoint('cloudify-cli', 'console_scripts', 'cfy',
               scripts=[provider_package_path],
               hiddenimports=[provider_package],
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
               swagger_tree,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='cfy')
