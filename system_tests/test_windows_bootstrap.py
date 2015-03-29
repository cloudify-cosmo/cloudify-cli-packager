########
# Copyright (c) 2015 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.


import os
import socket
import time
import json
import uuid

import winrm

from cloudify_cli import constants as cli_constants
from cloudify.workflows import local
from cosmo_tester.framework.testenv import TestCase


WINRM_PORT = 5985
CLI_PACKAGE_EXE = 'windows-cli-package.exe'
HELLO_WORLD_URL = 'https://github.com/cloudify-cosmo/cloudify-hello-world-example/archive/{0}.zip'  # NOQA
TASK_RETRIES = 20


class TestWindowsBootstrap(TestCase):

    def setUp(self):
        super(TestWindowsBootstrap, self).setUp()
        if 'BRANCH_NAME_CORE' not in os.environ:
            raise ValueError('BRANCH_NAME_CORE environment variable not set')
        if 'WINDOWS_CLI_PACKAGE_URL' not in os.environ:
            raise ValueError(
                'WINDOWS_CLI_PACKAGE_URL environment variable not set')
        self.branch = os.environ['BRANCH_NAME_CORE']
        self.windows_cli_package_url = os.environ['WINDOWS_CLI_PACKAGE_URL']
        blueprint_filename = 'test-windows-bootstrap-blueprint.yaml'
        blueprint_path = os.path.join(os.path.dirname(__file__),
                                      'resources',
                                      blueprint_filename)
        self.logger.info('Creating local environment...')
        self._test_id = str(uuid.uuid4()).split('-')[0]
        inputs = {
            'test_id': self._test_id,
            'os_username': self.env.keystone_username,
            'os_password': self.env.keystone_password,
            'os_tenant_name': self.env.keystone_tenant_name,
            'os_region': self.env.region,
            'os_auth_url': self.env.keystone_url,
            'image_name': self.env.windows_image_name,
            'flavor': self.env.medium_flavor_id,
            'key_pair_path': '/tmp/{0}-keypair.pem'.format(self._test_id)
        }
        self.bootstrap_inputs = {
            'keystone_username': self.env.keystone_username,
            'keystone_password': self.env.keystone_password,
            'keystone_tenant_name': self.env.keystone_tenant_name,
            'keystone_url': self.env.keystone_url,
            'image_id': self.env.image_id,
            'flavor_id': self.env.medium_flavor_id,
            'external_network_name': 'public',
            'manager_public_key_name': '{0}-windows-manager-keypair'.format(
                self._test_id),
            'agent_public_key_name': '{0}-windows-agent-keypair'.format(
                self._test_id),
        }
        self.logger.info('Using branch/tag: {0}'.format(self.branch))
        self.local_env = local.init_env(
            blueprint_path,
            inputs=inputs,
            name=self._testMethodName,
            ignored_modules=cli_constants.IGNORED_LOCAL_WORKFLOW_MODULES)
        self.addCleanup(self.cleanup)

    def cleanup(self):
        self.local_env.execute('uninstall',
                               task_retries=40,
                               task_retry_interval=30)

    def test_windows_cli_package(self):
        self.local_env.execute('install',
                               task_retries=40,
                               task_retry_interval=30)
        ip_address = self.local_env.outputs()['windows_vm_ip_address']
        password = self.local_env.outputs()['windows_vm_password']
        self.logger.info('Outputs: {0}'.format(self.local_env.outputs()))

        self._wait_for_connection_availability(ip_address, WINRM_PORT, 300)

        url = 'http://{0}:{1}/wsman'.format(ip_address, WINRM_PORT)
        user = 'Admin'
        session = winrm.Session(url, auth=(user, password))

        self.install_cli(session)
        self.prepare_manager_blueprint(session)
        self.bootstrap_manager(session)
        blueprint_id = self.publish_hello_world_blueprint(session)
        deployment_id = self.create_deployment(blueprint_id, session)
        self.install_deployment(deployment_id, session)
        self.uninstall_deployment(deployment_id, session)
        self.teardown_manager(session)

    def _wait_for_connection_availability(self, ip_address, port, timeout=300):
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                socket.create_connection((ip_address, port), timeout=10)
                break
            except IOError, e:
                self.logger.info(
                    'Connection to {0}:{1} is not available: {2} - retrying...'
                    .format(ip_address, port, str(e)))
                time.sleep(5)

    def _execute_command(self, session, cmd, log_cmd=True):
        if log_cmd:
            self.logger.info('Executing command using winrm: {0}'.format(cmd))
        else:
            self.logger.info('Executing command using winrm: ***')
        r = session.run_ps(cmd)
        self.logger.info("""Command execution result:
Status code: {0}
STDOUT:
{1}
STDERR:
{2}""".format(r.status_code, r.std_out, r.std_err))
        if r.status_code != 0:
            raise Exception('Command: {0} exited with code: {1}'.format(
                cmd, r.status_code))

    def install_cli(self, session):
        wget_cmd = """
$client = New-Object System.Net.WebClient
$url = "{0}"
$file = "{1}"
$client.DownloadFile($url, $file)""".format(self.windows_cli_package_url,
                                            CLI_PACKAGE_EXE)
        self.logger.info(
            'Downloading Windows CLI package from: {0}'.format(
                self.windows_cli_package_url))
        self._execute_command(session, wget_cmd)
        self.logger.info('Installing CLI...')
        self._execute_command(session, '.\{0} /SILENT /VERYSILENT /SUPPRESSMSGBOXES /DIR="C:\cloudify-cli"'.format(CLI_PACKAGE_EXE))  # NOQA
        self.logger.info('Verifying CLI installation...')
        self._execute_command(session, """
cd /cloudify-cli
./cfy.exe --version""")

    def prepare_manager_blueprint(self, session):
        manager_blueprints_url = 'https://github.com/cloudify-cosmo/cloudify-manager-blueprints/archive/{0}.zip'.format(self.branch)  # NOQA
        wget_cmd = """
$client = New-Object System.Net.WebClient
$url = "{0}"
$file = "{1}"
$client.DownloadFile($url, $file)
7za x {1} -oC:\cloudify-cli -y""".format(
            manager_blueprints_url, 'cloudify-manager-blueprints.zip')
        self.logger.info(
            'Downloading and extracting cloudify-manager-blueprints from: {0}'
            .format(manager_blueprints_url))
        self._execute_command(session, wget_cmd)
        blueprint_path = 'C:\cloudify-cli\cloudify-manager-blueprints-{0}\openstack-docker\openstack-docker.yaml'.format(self.branch)  # NOQA
        self._execute_command(
            session, """
$path = "{0}"
$text = "{1}"
$replace = "{2}"
$content = get-content $path
$content = $content -replace $text, $replace
$content = $content -replace "task_retries: .*$", "task_retries: {3}"
$content > $path""".format(
                blueprint_path,
                'http://gigaspaces-repository-eu.s3.amazonaws.com/org',
                'http://tarzan/builds/GigaSpacesBuilds',
                TASK_RETRIES))
        self._execute_command(session, """$inputs = '{0}'
$inputs | Out-File C:\cloudify-cli\inputs.json""".format(
            json.dumps(self.bootstrap_inputs)), log_cmd=False)

    def bootstrap_manager(self, session):
        self.logger.info('Bootstrapping Cloudify manager...')
        self._execute_command(session, """cd \cloudify-cli
cfy init -r
cfy bootstrap -p .\cloudify-manager-blueprints-{0}\openstack-docker\openstack-docker.yaml -i .\inputs.json""".format(  # NOQA
            self.branch))

    def publish_hello_world_blueprint(self, session):
        hello_world_url = HELLO_WORLD_URL.format(self.branch)
        blueprint_id = 'blueprint-{0}'.format(uuid.uuid4())
        self.logger.info(
            'Publishing hello-world example from: {0} [{1}]'.format(
                hello_world_url, blueprint_id))
        self._execute_command(session, """cd \cloudify-cli
cfy blueprints publish-archive -l {0} -n blueprint.yaml -b {1}""".format(
            hello_world_url, blueprint_id))
        return blueprint_id

    def create_deployment(self, blueprint_id, session):
        deployment_id = 'deployment-{0}'.format(uuid.uuid4())
        deployment_inputs = {
            'agent_user': 'ubuntu',
            'image': self.env.ubuntu_image_id,
            'flavor': self.env.small_flavor_id
        }
        self._execute_command(session, """$inputs = '{0}'
$inputs | Out-File C:\cloudify-cli\deployment-inputs.json""".format(
            json.dumps(deployment_inputs)))
        self.logger.info('Creating deployment: {0}'.format(deployment_id))
        self._execute_command(session, """cd \cloudify-cli
cfy deployments create -d {0} -b {1}  -i deployment-inputs.json""".format(
            deployment_id, blueprint_id))
        return deployment_id

    def install_deployment(self, deployment_id, session):
        self.logger.info('Installing deployment...')
        self._execute_command(session, """cd \cloudify-cli
cfy executions start -w install -d {0}""".format(deployment_id))

    def uninstall_deployment(self, deployment_id, session):
        self.logger.info('Uninstalling deployment...')
        self._execute_command(session, """cd \cloudify-cli
cfy executions start -w uninstall -d {0}""".format(deployment_id))

    def teardown_manager(self, session):
        self.logger.info('Tearing down Cloudify manager...')
        self._execute_command(session, """cd \cloudify-cli
cfy teardown -f --ignore-deployments""")
