'''Setup.py'''

from distutils.core import setup
from setuptools import find_packages

setup(
    name='models',
    version='0.0.0',
    author='Nicholas McKibben',
    author_email='nicholas.bgp@gmail.com',
    packages=find_packages(),
    scripts=[],
    url='https://github.com/backupinator/models',
    license='GPLv3',
    description=('Database models to be shared between all '
                 'applications.'),
    long_description=open('README.rst').read(),
    install_requires=[
        "peewee>=3.13.1",
        "requests>=2.22.0",
    ],
    python_requires='>=3.6',
)
