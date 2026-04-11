from setuptools import find_packages, setup

package_name = 'mini_camera_system'

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
    maintainer='juanmi',
    maintainer_email='juan.miguel.onate.tevar@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'camara = mini_camera_system.camara_node:main',
            'sub_viewer = mini_camera_system.viewer_node:main',
            'processing_frame = mini_camera_system.processing_node:main'
        ],
    },
)
