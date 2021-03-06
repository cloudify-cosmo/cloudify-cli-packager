#!/bin/bash

DSL_SHA=""
REST_CLIENT_SHA=""
COMMON_PLUGIN_SHA=""
CLI_SHA=""
OS_PROVIDER_SHA=""
OS_PLUGIN_SHA=""
FABRIC_PLUGIN_SHA=""
SCRIPTS_PLUGIN_SHA=""

# update cache and install essentials
sudo apt-get update
sudo apt-get install -y git curl python-dev libyaml-dev make

# install pip
curl --silent --show-error --retry 5 https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py | sudo python

# install virtualenv
sudo pip install virtualenv

# install ruby
wget ftp://ftp.ruby-lang.org/pub/ruby/1.9/ruby-1.9.3-p547.tar.bz2
tar -xjf ruby-1.9.3-p547.tar.bz2
cd ruby-1.9.3-p547
./configure --disable-install-doc
make
sudo make install
cd ~

# install fpm
sudo gem install fpm --no-rdoc --no-ri

# create and activate virtualenv
virtualenv ve_pyinstaller
source ve_pyinstaller/bin/activate

# install pyinstaller inside virtualenv
pip install pyinstaller

# install cfy and it's dependencies
git clone https://github.com/cloudify-cosmo/cloudify-dsl-parser.git
pushd cloudify-dsl-parser
	if [ -n "$DSL_SHA" ]; then
		git reset --hard $DSL_SHA
	fi
	pip install .
popd

git clone https://github.com/cloudify-cosmo/cloudify-rest-client.git
pushd cloudify-rest-client
	if [ -n "$REST_CLIENT_SHA" ]; then
		git reset --hard $REST_CLIENT_SHA
	fi
	pip install .
popd

git clone https://github.com/cloudify-cosmo/cloudify-plugins-common.git
pushd cloudify-plugins-common
        if [ -n "$COMMON_PLUGIN_SHA" ]; then
                git reset --hard $COMMON_PLUGIN_SHA
        fi
        pip install .
popd

git clone https://github.com/cloudify-cosmo/cloudify-script-plugin.git
pushd cloudify-script-plugin
        if [ -n "$SCRIPTS_PLUGIN_SHA" ]; then
                git reset --hard $SCRIPTS_PLUGIN_SHA
        fi
        pip install .
popd

git clone https://github.com/cloudify-cosmo/cloudify-cli.git
pushd cloudify-cli
	if [ -n "$CLI_SHA" ]; then
		git reset --hard $CLI_SHA
	fi
	pip install .
popd


git clone https://github.com/cloudify-cosmo/cloudify-openstack-provider
pushd cloudify-openstack-provider
	if [ -n "$OS_PROVIDER_SHA" ]; then
		git reset --hard $OS_PROVIDER_SHA
	fi
	pip install .
popd


git clone https://github.com/cloudify-cosmo/cloudify-openstack-plugin
pushd cloudify-openstack-plugin
	if [ -n "$OS_PLUGIN_SHA" ]; then
		git reset --hard $OS_PLUGIN_SHA
	fi
	pip install .
popd

git clone https://github.com/cloudify-cosmo/cloudify-fabric-plugin
pushd cloudify-fabric-plugin
	if [ -n "$FABRIC_SHA" ]; then
		git reset --hard $FABRIC_SHA
	fi
	pip install .
popd


# run pyinstaller
git clone https://github.com/cloudify-cosmo/cloudify-cli-packager.git
cd cloudify-cli-packager/pyinstaller
pyinstaller cfy.spec -y

# create deb
fpm -s dir -t deb -n cfy --prefix /usr/local -C dist/ \
--version `python -c "import pkg_resources;print pkg_resources.get_distribution('cloudify').version"` \
--after-install ../packaging/linux/after-install.sh --before-remove ../packaging/linux/before-remove.sh \
--description "Command line interface for Cloudify" \
--url "https://github.com/cloudify-cosmo/cloudify-cli" --vendor "GigaSpaces" --license "Apache License 2.0" cfy/

#copy deb file to /vagrant folder
cp ~/cloudify-cli-packager/pyinstaller/*.deb /vagrant
