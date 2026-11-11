from setuptools import find_packages, setup

package_name = 'tf_broadcaster'

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
    maintainer='ssafy',
    maintainer_email='ssafy@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'tf_broadcaster = tf_broadcaster.tf_broadcaster:main',
            'turtlesim_avoid_obstacle = tf_broadcaster.turtlesim_avoid_obstacle:main',
            'turtle_obstacle_marker=tf_broadcaster.turtle_obstacle_marker:main',
        ],
    },
)
