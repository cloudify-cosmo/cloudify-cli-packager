

import unittest

import winrm

from novaclient.v1_1.client import Client


OS_AUTH_URL='http://192.168.9.161:5000/v2.0'
OS_TENANT_ID='3c4164a47e1e4a72ac996d5167efe58b'
OS_TENANT_NAME='idan'
OS_USERNAME='idan'
OS_PASSWORD='idan'


key_file_path = '/home/idanmo/.ssh/os-lab-idan-keypair.pem'


SERVER_NAME = 'windows-cli-package-test'

CLI_PACKAGE_URL = 'http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.2.0/m4-RELEASE/cloudify-windows-cli_3.2.0-m4-b173.exe'


userdata = """
winrm quickconfig -q
winrm set winrm/config/winrs '@{MaxMemoryPerShellMB="300"}'
winrm set winrm/config '@{MaxTimeoutms="1800000"}'
winrm set winrm/config/service '@{AllowUnencrypted="true"}'
winrm set winrm/config/service/auth '@{Basic="true"}'
 
netsh advfirewall firewall add rule name="WinRM 5985" protocol=TCP dir=in localport=5985 action=allow
netsh advfirewall firewall add rule name="WinRM 5986" protocol=TCP dir=in localport=5986 action=allow

net stop winrm
sc config winrm
net start winrm
 
#msiexec /i https://www.python.org/ftp/python/2.7.6/python-2.7.6.msi TARGETDIR=C:\Python27 ALLUSERS=1 /qn


#http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.2.0/m4-RELEASE/cloudify-windows-cli_3.2.0-m4-b173.exe
#cloudify-windows-cli.exe /SILENT /VERYSILENT /SUPPRESSMSGBOXES /DIR="C:\cloudify-cli"


"""

class TestWindowsBootstrap(unittest.TestCase):


	def test_bootstrap(self):
		nova = Client(OS_USERNAME, OS_PASSWORD, OS_TENANT_NAME, OS_AUTH_URL)

		# print([(x.name, x.id) for x in nova.flavors.list()])
		# print([(x.name, x.id) for x in nova.images.list()])

		s = [x for x in nova.servers.list() if x.name == SERVER_NAME]
		if len(s) > 0:
			print('server already exist!')
			server = nova.servers.get(s[0].id)
			print('server password: {0}'.format(server.get_password(key_file_path)))
		else:
			server = nova.servers.create(
				SERVER_NAME,
				image='1db1ddc5-5e5c-47f3-bca3-c97cfe77e736',
				flavor='8b5be402-98e6-461c-8425-56f708187c13',
				key_name='idan-keypair',
				userdata=userdata)

		print('server id: {0}'.format(server.id))

		ps_script = """C:\Python27\python.exe --version"""
		url = 'http://192.168.40.210:5985/wsman'
		print('winrm url: {0}'.format(url))
		s = winrm.Session(url, auth=('Admin', '9NXmx2yPy29hb9'))
		r = s.run_cmd(ps_script)
		print('status code: {0}'.format(r.status_code))
		print('stdout: {0}'.format(r.std_out))
		print('stderr: {0}'.format(r.std_err))








