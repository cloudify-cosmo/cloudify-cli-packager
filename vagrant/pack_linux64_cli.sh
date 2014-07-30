#!/bin/bash

#####################################################################
#install vagrant - https://www.vagrantup.com/downloads.html (1.6.2) #
#vagrant plugin install vagrant-aws (0.4.1)                         #
#vagrant plugin install unf                                         #
#####################################################################

source ../../credentials.sh

function  exit_on_error {
      status=$?
      echo "exit code="$status    
      if [ $status != 0 ] ; then
         	echo "Failed (exit code $status)" 
		vagrant destroy -f linux64            
		exit 1
      fi

}

sudo chown tgrid -R /cloudify
rm -f /cloudify/cloudify-linux64-cli*amd64.deb
rm -f /cloudify/cfy_*_amd64.deb


#destroy linux64 vm if exit
vagrant destroy -f linux64

vagrant up linux64 --provider=aws
exit_on_error

#get guest ip address
s=`vagrant ssh linux64 -- ec2metadata | grep public-hostname | cut -f1 -d"." | cut -d" " -f2` ; s=${s#ec2-} ; ip_address=${s//-/.}
echo "ip_address="$ip_address

#copy linux64 deb file
sudo chown tgrid -R /cloudify
scp -i ~/.ssh/aws/vagrant_build.pem ubuntu@$ip_address:~/cloudify-cli-packager/pyinstaller/*.deb /cloudify
exit_on_error

vagrant destroy -f linux64



