from setuptools import setup

version = '1.0.0'

testing_extras = ['nose', 'coverage']

docs_extras = ['Sphinx']

setup(
    name='RethinkORM',
    version=version,
    description='Useful little ORM style wrapper for working with RethinkDB',
    long_description=open('README.rst').read(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 2.6",
    ],
    author='Joshua P Ashby',
    author_email='joshuaashby@joshashby.com',
    maintainer='Joshua P Ashby',
    url='https://github.com/JoshAshby/pyRethinkORM/',
    license='MIT',
    zip_safe=True,
    packages=['rethinkORM'],
    install_requires=[
        "rethinkdb >= 1.7.0"
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    extras_require = {
        'testing':testing_extras,
        'docs':docs_extras,
    }
)
