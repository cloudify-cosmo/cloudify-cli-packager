#!/bin/bash

# update cache and install essentials
sudo apt-get update
sudo apt-get install -y git curl python-dev ruby-dev make

# install pip
curl --silent --show-error --retry 5 https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py | sudo python

# install virtualenv
sudo pip install virtualenv

# install fpm
sudo gem install fpm --no-rdoc --no-ri

# create and activate virtualenv
virtualenv ve_pyinstaller
source ve_pyinstaller/bin/activate

# install pyinstaller inside virtualenv
pip install pyinstaller

# install cfy
pip install --process-dependency-links https://github.com/cloudify-cosmo/cloudify-cli/archive/develop.zip
pip install https://github.com/cloudify-cosmo/cloudify-openstack-provider/archive/develop.zip

# add github fingerprint to known host and clone (must user agent-forwarding)
ssh-keyscan -H github.com >> ~/.ssh/known_hosts
git clone git@github.com:CloudifySource/cloudify-cli-pyinstaller.git
cd cloudify-cli-pyinstaller
git checkout develop

# run pyinstaller
pyinstaller cfy.spec

# create deb
fpm -s dir -t deb -n cfy --prefix /usr/local -C dist/ \
--version `python -c "import pkg_resources;print pkg_resources.get_distribution('cloudify-cli').version"` \
--after-install after-install.sh --before-remove before-remove.sh \
--description "Command line interface for Cloudify" \
--url "https://github.com/cloudify-cosmo/cloudify-cli" --vendor "GigaSpaces" --license "Apache License 2.0" cfy/

mv cfy_*.deb ~/output