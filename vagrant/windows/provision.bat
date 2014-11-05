SET DSL_SHA=""
SET REST_CLIENT_SHA=""
SET COMMON_PLUGIN_SHA=""
SET CLI_SHA=""
SET OS_PROVIDER_SHA=""
SET OS_PLUGIN_SHA=""
SET FABRIC_PLUGIN_SHA=""


call "C:\Program Files (x86)\Microsoft Visual Studio 9.0\Common7\Tools\vsvars32.bat"

pip install pyinstaller

git clone https://github.com/cloudify-cosmo/cloudify-dsl-parser.git
pushd cloudify-dsl-parser
	if not (%DSL_SHA%)==() git reset --hard %DSL_SHA%
	pip install .
popd

git clone https://github.com/cloudify-cosmo/cloudify-rest-client.git
pushd cloudify-rest-client
	if not (%REST_CLIENT_SHA%)==() git reset --hard %REST_CLIENT_SHA%
	pip install .
popd

git clone https://github.com/cloudify-cosmo/cloudify-plugins-common.git
pushd cloudify-plugins-common
        if not (%COMMON_PLUGIN_SHA%)==() git reset --hard %COMMON_PLUGIN_SHA%
        pip install .
popd

git clone https://github.com/cloudify-cosmo/cloudify-cli.git
pushd cloudify-cli
	if not (%CLI_SHA%)==() git reset --hard %CLI_SHA%
	pip install .
popd

git clone https://github.com/cloudify-cosmo/cloudify-openstack-provider.git
pushd cloudify-openstack-provider
	if not (%OS_PROVIDER_SHA%)==() git reset --hard %OS_PROVIDER_SHA%
	pip install .
popd

git clone https://github.com/cloudify-cosmo/cloudify-openstack-plugin
pushd cloudify-openstack-plugin
    if not (%OS_PLUGIN_SHA%)==() git reset --hard %OS_PLUGIN_SHA%
	pip install .
popd

git clone https://github.com/cloudify-cosmo/cloudify-fabric-plugin
pushd cloudify-fabric-plugin
	if not (%FABRIC_PLUGIN_SHA%)==() git reset --hard %FABRIC_PLUGIN_SHA%
	pip install .
popd

python -c "import pkg_resources;print pkg_resources.get_distribution('cloudify').version" > version.txt
set /p CFYVERSION=<version.txt
del version.txt

git clone https://github.com/cloudify-cosmo/cloudify-cli-packager.git
cd cloudify-cli-packager\pyinstaller
pyinstaller cfy.spec -y
iscc ..\packaging/windows\inno\cfy_setup.iss
