call "C:\Program Files (x86)\Microsoft Visual Studio 9.0\Common7\Tools\vsvars32.bat"

pip install https://github.com/cloudify-cosmo/cloudify-openstack-provider/archive/develop.zip --process-dependency-links
pip install pyinstaller

python -c "import pkg_resources;print pkg_resources.get_distribution('cloudify-cli').version" > version.txt
set /p CFYVERSION=<version.txt
del version.txt

git clone https://github.com/cloudify-cosmo/cloudify-cli-packager.git
cd cloudify-cli-packager\pyinstaller
pyinstaller cloudify-cli-packager\pyinstaller\cfy.spec -y
iscc ..\packaging\windows\inno\cfy_setup.iss
