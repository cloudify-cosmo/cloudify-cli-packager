#!/bin/bash

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

# install cfy
pip install --process-dependency-links https://github.com/cloudify-cosmo/cloudify-openstack-provider/archive/develop.zip

# rm -rf cloudify-cli-packager
git clone https://github.com/cloudify-cosmo/cloudify-cli-packager.git

# run pyinstaller
cd cloudify-cli-packager/pyinstaller
pyinstaller cfy.spec -y

# create deb
fpm -s dir -t deb -n cfy --prefix /usr/local -C dist/ \
--version `python -c "import pkg_resources;print pkg_resources.get_distribution('cloudify-cli').version"` \
--after-install cloudify-cli-packager/packaging/linux/after-install.sh --before-remove cloudify-cli-packager/packaging/linux/before-remove.sh \
--description "Command line interface for Cloudify" \
--url "https://github.com/cloudify-cosmo/cloudify-cli" --vendor "GigaSpaces" --license "Apache License 2.0" cfy/
