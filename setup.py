from setuptools import setup

setup(
    name='openitnow',
    version='0.1',
    py_modules=['openitnow'],
    install_requires=[
        'click',
        'beautifulsoup4',
        'requests',
        'lxml',
    ],
    entry_points='''
        [console_scripts]
        openitnow=openitnow:cli
    ''',
)
