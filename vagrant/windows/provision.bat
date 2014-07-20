SET DSL_SHA=938cf6aece1504ef174f56efd1cb4c777ee3b7dd
SET REST_CLIENT_SHA=19af1a6055de5955f011963813f5c804ac9fbf5e
SET CLI_SHA=ed6a86fd2c1d611e4f68655c2397e8fc706d7e2b
SET OS_PROVIDER_SHA=d41a625a5621174d47dfaff1920fe4f82c86b331

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

python -c "import pkg_resources;print pkg_resources.get_distribution('cloudify-cli').version" > version.txt
set /p CFYVERSION=<version.txt
del version.txt

git clone https://github.com/cloudify-cosmo/cloudify-cli-packager.git
cd cloudify-cli-packager\pyinstaller
pyinstaller cfy.spec -y
iscc ..\packaging/windows\inno\cfy_setup.iss


