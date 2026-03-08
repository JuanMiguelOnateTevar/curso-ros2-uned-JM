from setuptools import find_packages, setup

package_name = 'practica_01_pubsub'

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
        'publisher_node = practica_01_pubsub.publisher_node:main',
        'subscriber_node = practica_01_pubsub.subscriber_node:main',
        ],
    },
)
