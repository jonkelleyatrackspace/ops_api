#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: pavement.py
# authors: jonathan kelley 2016

from paver.easy import *
import paver.doctools
from paver.setuputils import setup
import shutil
import os
import platform

def value_from_specfile(getkey):
    """
    loads the version and other keys from the .spec file
    which shall be our source of truth for versioning.

    i looked into using rpm, but the library is really really unwieldy
    not an external api, and looks like it's likely to change
    """
    cwd = os.getcwd()
    for file in os.listdir(cwd):
        if file.endswith(".spec"):
            SPEC_FILE = file

    spec = {}
    with open(SPEC_FILE, "r") as f:
        for line in f.readlines():
            try:
                value = line.split(":")[1].lstrip().strip()
                key = line.split(":")[0].lstrip().lower().rstrip()

                spec[key] = value
            except:
                pass
        return spec[getkey]

__doc__ = """ Setuptools with paver """

install_requires = []
setup(
    name=value_from_specfile('name'),
    version=value_from_specfile('version'),
    author="Jonathan Kelley",
    author_email="jonkelley@gmail.com",
    description=value_from_specfile('summary'),
    url=value_from_specfile('url'),
    packages=[str(value_from_specfile('name'))],
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
             '{name} = {name}.server:main'.format(
                 name=value_from_specfile('name'))
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
        "Topic :: Utilities",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: System :: Operating System",
    ],
    zip_safe=False
)

@task
def clean(options):
    """
    CLEAN after paver build operations
    """
    for i in ['./dist', './build', './opsapi.egg-info']:
        print("Removing {file}".format(file=i))
        try:
            shutil.rmtree(i)
        except OSError:
            pass
