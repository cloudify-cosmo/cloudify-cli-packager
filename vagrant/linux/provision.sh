#!/bin/bash

DSL_SHA=938cf6aece1504ef174f56efd1cb4c777ee3b7dd
REST_CLIENT_SHA=19af1a6055de5955f011963813f5c804ac9fbf5e
CLI_SHA=ed6a86fd2c1d611e4f68655c2397e8fc706d7e2b
OS_PROVIDER_SHA=d41a625a5621174d47dfaff1920fe4f82c86b331

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
#pip install --process-dependency-links https://github.com/cloudify-cosmo/cloudify-openstack-provider/archive/develop.zip
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

git clone https://github.com/cloudify-cosmo/cloudify-cli.git
pushd cloudify-cli
	if [ -n "$CLI_SHA" ]; then
		git reset --hard $CLI_SHA
	fi
	pip install .
popd

git clone https://github.com/cloudify-cosmo/cloudify-openstack-provider.git
pushd cloudify-openstack-provider
	if [ -n "$OS_PROVIDER_SHA" ]; then
		git reset --hard $OS_PROVIDER_SHA
	fi
	pip install .
popd


# run pyinstaller
# rm -rf cloudify-cli-packager
git clone https://github.com/cloudify-cosmo/cloudify-cli-packager.git
cd cloudify-cli-packager/pyinstaller
pyinstaller cfy.spec -y

# create deb
fpm -s dir -t deb -n cfy --prefix /usr/local -C dist/ \
--version `python -c "import pkg_resources;print pkg_resources.get_distribution('cloudify-cli').version"` \
--after-install ../packaging/linux/after-install.sh --before-remove ../packaging/linux/before-remove.sh \
--description "Command line interface for Cloudify" \
--url "https://github.com/cloudify-cosmo/cloudify-cli" --vendor "GigaSpaces" --license "Apache License 2.0" cfy/

#copy deb file to /vagrant folder
cp ~/cloudify-cli-packager/pyinstaller/*.deb /vagrant
