from setuptools import find_packages, setup

package_name = 'pjt9'

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
            'rrbot_ik_node = pjt9.rrbot_ik:main',
            'rrbot_ik_ptp_move = pjt9.rrbot_ik_ptp_move:main',
            'rrbot_ik_circle_move = pjt9.rrbot_ik_circle_move:main',
            'rrbot_ik_eight_move = pjt9.rrbot_ik_eight_move:main',
            'rrbot_ik_eight_move_reference = pjt9.rrbot_ik_eight_move_reference:main',
        ],
    },
)
