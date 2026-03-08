from setuptools import find_packages, setup

package_name = 'comuni_ABC'

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
            'node_A = comuni_ABC.node_A:main',
            'node_B = comuni_ABC.node_B:main',
            'node_C = comuni_ABC.node_C:main',
        ],
    },
)
