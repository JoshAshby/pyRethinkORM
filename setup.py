from distutils.core import setup
import rethinkORM

setup(
    name='RethinkORM',
    version=rethinkORM.__version__,
    author='Joshua P Ashby',
    author_email='joshuaashby@joshashby.com',
    packages=['rethinkORM', 'rethinkORM.tests'],
    url='https://github.com/JoshAshby/pyRethinkORM',
    license='GPL v3 (See LICENSE.txt for more info)',
    description='Useful little ORM style wrapper for working with RethinkDB',
    long_description=open('README.rst').read(),
    install_requires=[
        "rethinkdb >= 1.7.0",
        "nose >= 1.3.0"
    ],
)
