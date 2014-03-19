cloudify-cli-pyinstaller
========================
This repository contains configuration files & scripts for [Pyinstaller](http://www.pyinstaller.org/) program for building stand alone [cfy](https://github.com/CloudifySource/cosmo-cli) command line utility for Linux, OS X and Windows including openstack provider.


Manual build instructions
=========================
Since we want to build cfy on Linux/OS X/Windows, we'll need to run the process on each OS separately:

Windows
-------
1. On a clean installation of Windows 8 install the following:
  * [Python2 x86](https://www.python.org/download/releases/)
  * [PyWin32 x86](http://sourceforge.net/projects/pywin32/)
  * [pip](http://www.pip-installer.org/en/latest/installing.html)
  * [Git](http://git-scm.com/download/win)
  * [Microsoft Visual Studio C++ 2008 Express](http://www.visualstudio.com/en-us/downloads/)

2. Follow cfy utility installation instructions (pip install cosmo-cli & openstack provider)
3. Install PyInstaller: `pip install pyinstaller`
4. Clone this repository to your working directory: `git clone https://github.com/CloudifySource/cloudify-cli-pyinstaller.git`
5. Run PyInstaller: `pyinstaller cfy.spec`
6. <TODO> Instructions for making self extracting zip?

OS X
----
<TODO>

Linux
-----
<TODO>

