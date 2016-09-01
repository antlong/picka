#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='picka',
    version='1.0.1',
    install_requires=['attrdict', 'sqlalchemy', 'assertlib', "LatLon"],
    description='Picka generates randomized, realistic testing \
        data for use in any application.',
    keywords="data generation generate random randomization testing "
             "tests test qa",
    author='Anthony Long',
    author_email='antlong@gmail.com',
    license='Apache 2.0',
    packages=['picka'],
    url='http://github.com/antlong/picka',
    include_package_data=True,
    package_data={
        'picka': [
            '*.sqlite',
            '*.txt',
            'README.rst'
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Customer Service",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Legal Industry",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Other Audience",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Telecommunications Industry",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.3",
        "Programming Language :: Python :: 2.4",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: SQL",
        "Topic :: Software Development",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Debuggers",
        "Topic :: Software Development :: Localization",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX']
)
