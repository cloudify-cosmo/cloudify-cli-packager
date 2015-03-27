SET CORE_TAG_NAME="master"
SET PLUGINS_TAG_NAME="master"

call "C:\Program Files (x86)\Microsoft Visual Studio 9.0\Common7\Tools\vsvars32.bat"

pip install pyinstaller

pip install git+https://github.com/cloudify-cosmo/cloudify-dsl-parser.git@%CORE_TAG_NAME%
pip install git+https://github.com/cloudify-cosmo/cloudify-rest-client.git@%CORE_TAG_NAME%
pip install git+https://github.com/cloudify-cosmo/cloudify-plugins-common.git@%CORE_TAG_NAME%
pip install git+https://github.com/cloudify-cosmo/cloudify-script-plugin.git@%PLUGINS_TAG_NAME%
pip install git+https://github.com/cloudify-cosmo/cloudify-cli.git@%CORE_TAG_NAME%
pip install git+https://github.com/cloudify-cosmo/cloudify-openstack-provider.git@%PLUGINS_TAG_NAME%
pip install git+https://github.com/cloudify-cosmo/cloudify-openstack-plugin.git@%PLUGINS_TAG_NAME%
pip install git+https://github.com/cloudify-cosmo/cloudify-fabric-plugin.git@%PLUGINS_TAG_NAME%



python -c "import pkg_resources;print pkg_resources.get_distribution('cloudify').version" > version.txt
set /p CFYVERSION=<version.txt
del version.txt

git clone https://github.com/cloudify-cosmo/cloudify-cli-packager.git
cd cloudify-cli-packager\pyinstaller
  git checkout -b tmp_branch %CORE_TAG_NAME%
  git log -1
  pyinstaller cfy.spec -y
  iscc ..\packaging/windows\inno\cfy_setup.iss
