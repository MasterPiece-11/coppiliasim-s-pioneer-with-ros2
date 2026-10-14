from setuptools import find_packages, setup

package_name = 'pioneer_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ahmed',
    maintainer_email='ahmed@todo.todo',
    description='Pioneer 3-DX Teleop and Sensor Visualization',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'teleop_node = pioneer_control.teleop_node:main',
            'sensor_viz_node = pioneer_control.sensor_viz_node:main'
        ],
    },
)
