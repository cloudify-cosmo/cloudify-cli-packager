import os
import sys
import logging
import string
import random
from ast import literal_eval
from shutil import copy, rmtree
from ConfigParser import ConfigParser
from tempfile import mkdtemp
from unittest import TestCase, main, skip
from platform import system, linux_distribution, machine
from distutils.spawn import find_executable
from subprocess import call

logger = logging.getLogger()


def install_package(path):
    """
    Install package located in path (multiplatform)
    """
    logger.debug('Installing package for {}'.format(system()))
    if system() == 'Windows':
        return _install_win(path)
    elif system() == 'Linux':
        return _install_linux(path)
    elif system() == 'Darwin':
        return _install_osx(path)
    else:
        raise Exception('Unsupported OS')


def _install_win(path):
    """
    Install package from path in Windows and return exit code.
    Support .exe packages of Inno Setup
    """
    logger.debug('Installing package from: {}'.format(path))
    return_code = call(['cmd', '/c', 'start', '/WAIT', path, '/silent'])
    return return_code


# TODO: suppport rpm package as well
def _install_linux(path):
    """
    Install package from path in Linux and return exit code
    Supports .deb packages
    """
    logger.debug('Installing package for {}'.format(linux_distribution()))
    if 'Ubuntu' in linux_distribution():
        import apt.debfile
        file = apt.debfile.DebPackage(filename=path)
        return_code = file.install()
        return return_code
    else:
        return -1


# TODO: add OS X support
def _install_osx(path):
    return False


def uninstall_package(package):
    """
    Install package located in path (multiplatform)
    """
    logger.debug('Uninstalling package for {}'.format(system()))
    if system() == 'Windows':
        return _uninstall_win(package)
    elif system() == 'Linux':
        return _uninstall_linux(package)
    elif system() == 'Darwin':
        return _uninstall_osx(package)
    else:
        raise Exception('Unsupported OS')


# TODO: read uninstall string from registry
def _uninstall_win(appid):
    """
    Uninstall in Windows
    """
    import _winreg
    try:
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,
                              'SOFTWARE\\Wow6432Node\\Microsoft\\'
                              'Windows\\CurrentVersion\\Uninstall\\'
                              '{{{}}}_is1'.format(appid))
        uninstall_path = literal_eval(_winreg.QueryValueEx(
                                      key, 'UninstallString')[0])
    except WindowsError:
        return -1
    logger.debug('Uninstalling path: {}'.format(uninstall_path))
    return call([uninstall_path, '/silent'], shell=True)


# TODO: suppport rpm package as well
def _uninstall_linux(package):
    """
    Uninstall package Linux and return exit code
    Supports .deb packages
    """
    if 'Ubuntu' in linux_distribution():
        import apt
        cache = apt.Cache()
        try:
            cache[package].mark_delete()
        except KeyError:
            raise Exception('Failed uninstalling: package not installed?')
        # if True, return error code 0, else 1
        return(not int(cache.commit()))
    else:
        return -1


# TODO: add OS X support
def _uninstall_osx(pkg_id):
    """
    """
    pass


def is_installed(package):
    """
    Return True if package appears to be installed (multiplatform)
    """
    if system() == 'Windows':
        return _is_installed_win(package)
    elif system() == 'Linux':
        return _is_installed_linux(package)
    elif system() == 'Darwin':
        return _is_installed_osx(package)
    else:
        raise Exception('Unsupported OS')


# TODO: support 32bit and 64bit arch
def _is_installed_win(appid):
    """
    Return True if package appears to be installed in Windows
    """
    import _winreg
    try:
        _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,
                        'SOFTWARE\\Wow6432Node\\Microsoft\\'
                        'Windows\\CurrentVersion\\Uninstall\\'
                        '{{{}}}_is1'.format(appid))
    except WindowsError:
        return False
    return True


# TODO: Add rpm support (centos)
def _is_installed_linux(package):
    """
    Return True if package appears to be installed in Linux
    """
    logger.debug('checking if {} installed'.format(package))
    if 'Ubuntu' in linux_distribution():
        import apt
        cache = apt.Cache()
        return package in cache and cache[package].is_installed
    else:
        return False


# TODO: add OS X support
def _is_installed_osx(package):
    return False


# TODO: use registry to find install path
# On 32bit, application can only be installed as 32bit mode
# On 64bit, application can be installed both as 32bit and 64bit
# Python can run as both 32bit and 64bit as well.
# If running in 32bit mode, it will access only 32bit registry by default
# If running in 64bit mdoe, it will access only 64bit registry by default
# So if arch is 64bit, need to check both 32bit and 64bit registry
def _get_installed_path(appid):
    """
    In windows, find install dir of cfy from registry
    """
    return 'C:\\Program Files (x86)\\cfy'


def _call(cmd, stdout=open(os.devnull, 'w'), appid=None):
    """
    A proxy for subprocess.call to manipulate PATH env variable if
    called in windows, because in windows it's impossible to refresh shell
    environment
    """
    if system() == 'Windows':
        env = os.environ
        env['PATH'] += ';{}'.format(_get_installed_path(appid))
        return call(cmd, env=env, stdout=stdout)
    else:
        return call(cmd, stdout=stdout)


def _id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """
    Generate random ID
    """
    return ''.join(random.choice(chars) for _ in range(size))


def _copy_cloudify_config(source, dest):
    """
    Read source and write to dest while inserting appropriate values in
    template
    """
    logger.debug('copying cloudify config\nsource: {}\ndest: {}'.format(source,
                                                                        dest))
    with open(source, 'r') as file:
        template = file.read()
    instance_name = 'cloudify-management-clipkgtest-' + _id_generator()
    logger.debug('new instance name: {}'.format(instance_name))
    config = string.Template(template).substitute(instance_name=instance_name)
    with open(dest, 'w') as file:
        file.write(config)


def _get_abspath(path):
    """
    Return absolute path, relative to module
    """
    directory = os.path.dirname(os.path.realpath(__file__))
    return os.path.abspath(os.path.join(directory, path))


def _remove_files(files):
    for file in files:
        try:
            os.remove(file)
        except OSError as e:
            raise Exception('Failed deleting {}, reason: {}'
                            .format(file, e.strerror))


def _set_logging_stream_handler():
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.set_name('stdout')
    handlers = [hl for hl in logger.handlers if hl.get_name() == 'stdout']
    if not handlers:
        logger.addHandler(stream_handler)


# TODO: convert settings reading from ini to dynamic
def _set_class_vars(cls):
    """
    Set class variables for the whole test
    """
    config = ConfigParser()
    config.read(_get_abspath('settings.ini'))
    logger.level = eval('logging.' + config.get('global', 'logging'))
    cls.exec_name = config.get('global', 'exec')

    cls.opst_conf = _get_abspath(config.get('openstack', 'config_path'))
    cls.use_existing = literal_eval(config.get('global', 'use_existing'))
    cls.mgmt_ip = config.get('global', 'management_ip')
    cls.opst_blueprint_path = _get_abspath(config.get('openstack',
                                                      'blueprint_path'))

    if system() == 'Windows':
        cls.path = _get_abspath(config.get('exe', 'path'))
        cls.pkg_id = config.get('exe', 'pkg_id')
    elif system() == 'Linux' and 'Ubuntu' in linux_distribution():
        if 'i686' in machine():
            cls.pkg_id = config.get('deb32', 'pkg_id')
            cls.path = _get_abspath(config.get('deb32', 'path'))
        else:
            cls.pkg_id = config.get('deb64', 'pkg_id')
            cls.path = _get_abspath(config.get('deb64', 'path'))
    else:
        raise Exception('Unsupported OS')


class BaseTest(TestCase):
    def assertReturnCodeZero(self, cmd):
        """
        Assert return code is 0
        """
        returncode = _call(cmd.split(' '), appid=self.pkg_id)
        if returncode != 0:
            self.fail('{} != 0'.format(returncode))


class InstallCFY(BaseTest):
    @classmethod
    def setUpClass(cls):
        _set_logging_stream_handler()
        _set_class_vars(cls)

        errcode = install_package(cls.path)
        if errcode != 0:
            raise Exception('Installation failed, error: {}'.format(errcode))

    @classmethod
    def tearDownClass(cls):
        errcode = uninstall_package(cls.pkg_id)
        if errcode != 0:
            raise Exception('Uninstall failed, error: {}'.format(errcode))

    def test_installed(self):
        """
        is package installed
        """
        self.assertEqual(is_installed(self.pkg_id), True)

    def test_cfy_in_path(self):
        """
        is package executable is in PATH
        """
        envpath = None
        if system() == 'Windows':
            envpath = _get_installed_path(self.pkg_id)
        path = find_executable(self.exec_name, path=envpath)
        logger.debug('exec path: {}'.format(path))
        self.assertIsNotNone(path)

    def test_cfy_help(self):
        self.assertReturnCodeZero('cfy -h')

    def test_cfy_version(self):
        self.assertReturnCodeZero('cfy --version')

    def test_cfy_init_openstack(self):
        logger.debug('cwd: {}'.format(os.getcwd()))
        self.assertReturnCodeZero('cfy init openstack')
        _remove_files(['.cloudify', 'cloudify-config.yaml'])

    def test_cfy_init_simple_provider(self):
        logger.debug('cwd: {}'.format(os.getcwd()))
        self.assertReturnCodeZero('cfy init simple_provider')
        _remove_files(['.cloudify', 'cloudify-config.yaml'])


class BootstrapOpenstack(BaseTest):
    @classmethod
    def setUpClass(cls):
        _set_logging_stream_handler()
        _set_class_vars(cls)

        errcode = install_package(cls.path)
        if errcode != 0:
            raise Exception('Installation failed, error: {}'.format(errcode))

        cls.tempdir = mkdtemp()
        cls.origdir = os.getcwd()
        logger.debug('temp dir: {}'.format(cls.tempdir))
        os.chdir(cls.tempdir)

        _call(['cfy', 'init', 'openstack'], appid=cls.pkg_id)
        _copy_cloudify_config(cls.opst_conf,
                              os.path.join(cls.tempdir,
                                           'cloudify-config.yaml'))

        if cls.use_existing:
            _call(['cfy', 'use', cls.mgmt_ip], appid=cls.pkg_id)
        else:
            errcode = _call(['cfy', 'bootstrap', '-v'], appid=cls.pkg_id)
            if errcode != 0:
                os.chdir(cls.origdir)
                raise Exception('Bootstrap failed, error: {}'.format(errcode))

    @classmethod
    def tearDownClass(cls):
        if not cls.use_existing:
            errcode = _call(['cfy', 'teardown', '-f'], appid=cls.pkg_id)
            if errcode != 0:
                raise Exception('Teardown failed, error: {}'.format(errcode))

        os.chdir(cls.origdir)
        rmtree(cls.tempdir)
        errcode = uninstall_package(cls.pkg_id)
        if errcode != 0:
            raise Exception('Uninstall failed, error: {}'.format(errcode))

    def test_flow(self):
        bp = 'mock'
        dp = 'mock'
        path = self.opst_blueprint_path
        self.assertReturnCodeZero('cfy status')
        self.assertReturnCodeZero('cfy blueprints validate {}'.format(path))
        self.assertReturnCodeZero('cfy blueprints upload -b {} {}'.format(
                                  bp, path))
        self.assertReturnCodeZero('cfy blueprints list')
        self.assertReturnCodeZero('cfy deployments create -b {} -d {}'.format(
                                  bp, dp))
        self.assertReturnCodeZero('cfy deployments list')
        self.assertReturnCodeZero('cfy deployments execute -d {} install'
                                  .format(dp))
        self.assertReturnCodeZero('cfy executions list -d {}'.format(dp))
        self.assertReturnCodeZero('cfy deployments execute -d {} uninstall'
                                  .format(dp))
        self.assertReturnCodeZero('cfy deployments delete -d {} -f'.format(dp))

if __name__ == '__main__':
    main(verbosity=2)
