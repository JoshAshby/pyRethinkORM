from distutils.core import setup

setup(
    name='RethinkORM',
    version='0.1.0',
    author='Joshua P Ashby',
    author_email='joshuaashby@joshashby.com',
    packages=['rethinkORM', 'rethinkORM.test'],
    scripts=[],
    url='https://github.com/JoshAshby/pyRethinkORM',
    license='LICENSE.txt',
    description='Useful little ORM style wrapper for working with RethinkDB',
    long_description=open('README.rst').read(),
    install_requires=[
        "rethinkdb >= 1.7.0"
    ],
)
