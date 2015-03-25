REM SET DSL_SHA=""
REM SET REST_CLIENT_SHA=""
REM SET COMMON_PLUGIN_SHA=""
REM SET CLI_SHA=""
REM SET OS_PROVIDER_SHA=""
REM SET OS_PLUGIN_SHA=""
REM SET FABRIC_PLUGIN_SHA=""
REM SET SCRIPTS_PLUGIN_SHA=""

SET core_tag_name="master"
SET plugins_tag_name="master"


call "C:\Program Files (x86)\Microsoft Visual Studio 9.0\Common7\Tools\vsvars32.bat"

pip install pyinstaller

pip install -e git://github.com/cloudify-cosmo/cloudify-dsl-parser.git@%core_tag_name%#egg=cloudify-dsl-parser==%core_tag_name%
pip install -e git://github.com/cloudify-cosmo/cloudify-rest-client.git@%core_tag_name%#egg=cloudify-rest-client==%core_tag_name%
pip install -e git://github.com/cloudify-cosmo/cloudify-plugins-common.git@%core_tag_name%#egg=cloudify-plugins-common==%core_tag_name%
pip install -e git://github.com/cloudify-cosmo/cloudify-script-plugin.git@%plugins_tag_name%#egg=cloudify-script-plugin==%plugins_tag_name%
pip install -e git://github.com/cloudify-cosmo/cloudify-cli.git@%core_tag_name%#egg=cloudify-cli==%core_tag_name%
pip install -e git://github.com/cloudify-cosmo/cloudify-openstack-provider.git@%plugins_tag_name%#egg=cloudify-openstack-provider==%plugins_tag_name%
pip install -e git://github.com/cloudify-cosmo/cloudify-openstack-plugin.git@%plugins_tag_name%#egg=cloudify-openstack-plugin==%plugins_tag_name%
pip install -e git://github.com/cloudify-cosmo/cloudify-fabric-plugin.git@%plugins_tag_name%#egg=cloudify-fabric-plugin==%plugins_tag_name%



python -c "import pkg_resources;print pkg_resources.get_distribution('cloudify').version" > version.txt
set /p CFYVERSION=<version.txt
del version.txt

git clone https://github.com/cloudify-cosmo/cloudify-cli-packager.git
cd cloudify-cli-packager\pyinstaller
pyinstaller cfy.spec -y
iscc ..\packaging/windows\inno\cfy_setup.iss
