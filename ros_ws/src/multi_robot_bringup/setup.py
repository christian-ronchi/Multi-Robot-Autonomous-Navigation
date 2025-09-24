import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'multi_robot_bringup'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(where='.', include=['multi_robot_scripts', 'multi_robot_scripts.*'], exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        (os.path.join('share', package_name), ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*.launch.py'))),
        (os.path.join('share', package_name, 'params'), glob(os.path.join('params', '*.yaml'))),
        (os.path.join('share', package_name, 'rviz'), glob(os.path.join('rviz', '*.rviz'))),
        (os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*.yaml'))),
        (os.path.join('share', package_name, 'map'), glob(os.path.join('map', '*.yaml'))),
        (os.path.join('share', package_name, 'map'), glob(os.path.join('map', '*.pgm'))),
        (os.path.join('share', package_name, 'launch', 'nav2_custom'), glob(os.path.join('launch', 'nav2_custom', '*launch.py'))),
    ],
    install_requires=['setuptools', 'scikit-learn'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
)
