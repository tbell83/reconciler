from setuptools import setup

setup(
    name='chef_prune',
    version='1.0',
    packages=['cheff', 'util'],
    include_package_data=True,
    install_requires=[
        'pychef',
        'boto3'
    ]
)
