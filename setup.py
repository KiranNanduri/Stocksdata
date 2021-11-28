# -*- coding: utf-8 -*-
"""
Created on Sat Oct 25 22:59:19 2021

@author: kiran
"""

from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Science/Research",
    "Operating System :: Microsoft :: Windows :: Windows 10",
    "Operating System :: POSIX :: Linux",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3" 
]

setup(
    name='stocksdata',
    version='1.0.2',
    description='Package of download bhavcopy data from nse website',
    long_description=open('README.md').read()+'\n\n'+open('CHANGELOG.txt').read(),
    url='https://github.com/KiranNanduri/StockCode',
    author='kiran nanduri',
    author_email='kirannanduri@outlook.com',
    license='MIT',
    classifiers=classifiers,
    keywords='nse',
    packages=find_packages(),
    install_requires=['requests==2.25.1']
)
