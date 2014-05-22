cd "C:\Program Files (x86)\Microsoft Visual Studio 9.0\Common7\Tools\"
call vsvars32.bat
cd %HOME%
pip install https://github.com/cloudify-cosmo/cloudify-openstack-provider/archive/develop.zip --process-dependency-links
pip install pyinstaller
git clone https://github.com/cloudify-cosmo/cloudify-cli-packager.git
pyinstaller cloudify-cli-packager\cfy.spec
