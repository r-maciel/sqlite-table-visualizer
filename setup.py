from setuptools import setup

setup(
    name='SQLite Table Visalizer',
    version='0.1',
    py_modules=['app'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        sqlite-viz=app:cli
    ''',
)
