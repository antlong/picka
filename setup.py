import os
from setuptools import setup

setup(
    name='picka',
    version="0.7.8",
    description="picka generates randomized, realistic data for use in any application.",
    author="Anthony Long",
    url='http://github.com/antlong/picka',
    packages=["picka"],
    package_data={
        'picka': ['*.sqlite', '*.txt', ], },
    include_package_data=True,
    install_requires=['setuptools'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python', ],
)
