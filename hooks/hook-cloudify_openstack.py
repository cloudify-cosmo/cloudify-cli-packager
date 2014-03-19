from PyInstaller.hooks.hookutils import get_package_paths
from PyInstaller.hooks.hookutils import collect_data_files

package_name = 'cloudify_openstack'
package_path = get_package_paths(package_name)[1]

datas = [(package_path + '/*.py', package_name)] + collect_data_files(package_name)
