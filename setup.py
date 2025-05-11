from setuptools import find_packages, setup
import os
from glob import glob
package_name = 'hitomi_display'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf')+ glob('urdf/*.xacro')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'meshes'), glob('meshes/*.dae')+ glob('meshes/*.stl')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.sdf')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*.rviz')),
        
    ],
    install_requires=[
        'setuptools',
    ],
    zip_safe=True,
    maintainer='badri',
    maintainer_email='badri@todo.todo',
    description='A robot',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'voice_controller = hitomi_display.speech_dev_controller.py:main',
            
        ],
    },
)
