SET core_tag_name="master"
SET plugins_tag_name="master"


call "C:\Program Files (x86)\Microsoft Visual Studio 9.0\Common7\Tools\vsvars32.bat"

pip install pyinstaller

pip install -e git://github.com/cloudify-cosmo/cloudify-dsl-parser.git@%core_tag_name%
pip install -e git://github.com/cloudify-cosmo/cloudify-rest-client.git@%core_tag_name%
pip install -e git://github.com/cloudify-cosmo/cloudify-plugins-common.git@%core_tag_name%
pip install -e git://github.com/cloudify-cosmo/cloudify-script-plugin.git@%plugins_tag_name%
pip install -e git://github.com/cloudify-cosmo/cloudify-cli.git@%core_tag_name%
pip install -e git://github.com/cloudify-cosmo/cloudify-openstack-provider.git@%plugins_tag_name%
pip install -e git://github.com/cloudify-cosmo/cloudify-openstack-plugin.git@%plugins_tag_name%
pip install -e git://github.com/cloudify-cosmo/cloudify-fabric-plugin.git@%plugins_tag_name%



python -c "import pkg_resources;print pkg_resources.get_distribution('cloudify').version" > version.txt
set /p CFYVERSION=<version.txt
del version.txt

git clone https://github.com/cloudify-cosmo/cloudify-cli-packager.git
cd cloudify-cli-packager\pyinstaller
  git checkout -b tmp_branch %core_tag_name%
	git log -1
  pyinstaller cfy.spec -y
  iscc ..\packaging/windows\inno\cfy_setup.iss
