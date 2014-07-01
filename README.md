Cloudify CLI Packager
=====================
This repository contains configuration files for [PyInstaller](http://www.pyinstaller.org/), [fpm](https://github.com/jordansissel/fpm), [Vagrant](http://www.vagrantup.com/) and [Inno Setup](http://www.jrsoftware.org/isinfo.php) for creating stand-alone, self-contained, [Cloudify command line (cfy)](https://github.com/cloudify-cosmo/cloudify-cli) for multiple platforms (Windows, Linux, OS X).

At this point the package is pre-bundled with [cloudify-openstack-provider](https://github.com/cloudify-cosmo/cloudify-openstack-provider), to allow bootstraping Openstack based environments.

How to use this
===============
This project uses Vagrant as the executor to spin up virtual machine & run provision scripts remotely.
Current configured provider is AWS, so this means you'll need AWS plugin installed as well with your vagrant.

Provision scripts are located under `vagrant/<OS>` folder, so its possible to run these scripts without vagrant by executing them directly.

Quick start:

1. Set environment variables `AWS_ACCESS_KEY` and `AWS_ACCESS_KEY_ID`
1. Clone this repository
1. `vagrant up <windows/linux32/linux64> --provider aws`


Basic Flow
===========
1. Install Python and needed modules (PyInstaller, Virtualenv, Cloudify-CLI and dependencies)
1. Install packaging tools and its dependencies (Ruby & fpm in case of linux, Inno Setup in Windows)
1. Run PyInstaller to create binary
1. Create package from PyInstaller's output
1. *(Optional)* Run sanity tests on the package


Platform Specific Notes
======================
Windows:
-------
* Using x86 Python
* [Microsoft Visual Studio C++ 2008 Express](http://www.visualstudio.com/en-us/downloads/) is needed to compile part of the modules
* [PyWin32 x86](http://sourceforge.net/projects/pywin32/) is needed for PyInstaller as well
* Virtualenv is not installed in Windows since it doesn't come with built-in Python
* Ruby & fpm is replaced with Inno Setup to create executable installer
* Everything is being done with 32bit Python to try keep computability for maximum

Linux:
-----
* 32bit and 64bit are being built separately
* Ruby & fpm are installed for pain-free package creation
* Output is .deb package. But will be extended for .rpm as well
* Possbile issues on older distributions as explained in [PyInstaller FAQ](http://www.pyinstaller.org/wiki/FAQ) (Look under misc).

OS X:
----
* OS X is 64bit since Core 2 Duo days
* Currently NOT implemented


Vagrant
=======
To run this you need Vagrant v1.6.3 with [AWS plugin](https://github.com/mitchellh/vagrant-aws) v0.5.0.

Windows AMI is private custom built image that will hopefully made public.
The image comes with most of the software specified in __Platform Specific Notes__.
Additionally it comes with preinstalled Cygwin with SSH service, Curl and Git.

Cygwin is a must for now, until Vagrant plugins will become mature enough to support Windows provisioning via WinRM
support that was introduced in Vagrant 1.6.
