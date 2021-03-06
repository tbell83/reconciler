from setuptools import setup

setup(
    name='reconciler',
    version='1.0',
    packages=['cheff', 'util'],
    include_package_data=True,
    install_requires=[
        'pychef',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        reconciler=cheff.__main__:main
    ''',
    )
