from setuptools import setup

setup(
    name='chef_prune',
    version='1.0',
    packages=['cheff', 'util'],
    include_package_data=True,
    install_requires=[
        'pychef',
        'boto3'
    ],
    entry_points={
        'console_scripts': [
            'chef_prune = cheff.__main__:main'
        ]
    }
)
