Testing flow:
=============
1. Copy packages to the correct folder in the `tests/files` directory
1. Update `tests/scripts/settings.ini` file with the correct filename for each package
1. Create instance with Vagrant
1. Run provision (Copies over tests and packages)
1. Run unit-tests via SSH

Settings.ini
============
settings.ini is a config file for the tests. It contains some important settings
and allows the tests to be configured easier by non programer.

__NOTE__: All paths are relative to `scripts` folder

## Sections:
### global
* exec: command line binary name - this is usually 'cfy'
* logging: logging level of python logging module (for debug)
* use_existing: If true, won't run bootstrap, but use existing environment (good for testing)
* management_ip: if `use_existing` is true, use this management server
* private_key: private key path used by cloudify-config.yaml

### deb32
* path: 32bit .deb package path
* name: package name (usually 'cfy')

### deb64
* path: 64bit .deb package path
* name: package name (usually 'cfy')

### exe
* path: exe package path
* appid: application id (unique id of application in windows, see Inno Setup config)

### openstack
* config_path: openstack's cloudify-config.yaml file path
* blueprint_path: mock blueprint file path


Running tests:
==============
From `tests/scripts` execute `sudo python -m unittest discover`

Sample output:

    $ sudo python -m unittest discover
    (Reading database ... 62243 files and directories currently installed.)
    Preparing to unpack .../cloudify-cli_3.0.0-m4-b4_amd64.deb ...
    Unpacking cfy (3.0) over (3.0) ...
    Setting up cfy (3.0) ...
    usage: cfy [-h]

               {status,use,init,bootstrap,teardown,blueprints,deployments,executions,workflows,events,dev,ssh}
               ...

    Manages Cloudify in different Cloud Environments

    positional arguments:
      {status,use,init,bootstrap,teardown,blueprints,deployments,executions,workflows,events,dev,ssh}
        status              Show a management server's status
        use                 Use/switch to the specified management server
        init                Initialize configuration files for a specific cloud
                            provider
        bootstrap           Bootstrap Cloudify on the currently active provider
        teardown            Teardown Cloudify
        blueprints          Manages Cloudify's Blueprints
        deployments         Manages and Executes Cloudify's Deployments
        executions          Manages Cloudify Executions
        workflows           Manages Deployment Workflows
        events              Displays Events for different executions
        ssh                 SSH to management server

    optional arguments:
      -h, --help            show this help message and exit
    ...
    ----------------------------------------------------------------------
    Ran 3 tests in 1.604s

    OK

Pre-Requirements:
=================
1. Python 2.7+
1. __(Windows)__ Cygwin + OpenSSH
