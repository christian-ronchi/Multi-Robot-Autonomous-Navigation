from setuptools import find_packages
from setuptools import setup

setup(
    name='dynamic_obstacle_detector_interfaces',
    version='0.0.0',
    packages=find_packages(
        include=('dynamic_obstacle_detector_interfaces', 'dynamic_obstacle_detector_interfaces.*')),
)
