from setuptools import setup

setup(
    name='dfchef',
    version='1.0',
    packages=['cheff', 'util'],
    include_package_data=True,
    install_requires=[
        'pychef',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        dfchef=cheff.__main__:main
    ''',
    )
