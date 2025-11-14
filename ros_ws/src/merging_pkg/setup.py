from setuptools import setup, find_packages
import os
from glob import glob

package_name = 'merging_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='Custom map merging package with laser filtering',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'merger_node = merging_pkg.robust_map_merger:main',
            'robot_laser_filter = merging_pkg.robot_laser_filter:main',
        ],
    },
)