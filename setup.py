from setuptools import setup

setup(
    name='SQLite Table Visalizer',
    version='0.1',
    py_modules=['app', 'models'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        sqliteviz=app:cli
    ''',
)
