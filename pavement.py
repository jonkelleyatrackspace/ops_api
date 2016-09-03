#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: pavement.py
# authors: jonathan kelley 2016

from paver.easy import *
import paver.doctools
from paver.setuputils import setup
import shutil
import os

__doc__ = """ Setuptools with paver """
install_requires = [
    'pyyaml==3.10',
    'tornado==3.0.1',
    'toro==0.5',
    'passlib==1.6'
]
setup(
    name="opsapi",
    version="0.3",
    author="Jonathan Kelley",
    author_email="jonkelley@gmail.com",
    description="Extensible operations API and SDK blueprint examples",
    url="https://github.com/jonkelleyatrackspace/ops_api",
    packages=['opsapi'],
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'opsapi = opsapi.server:main'
        ]
    },
    zip_safe=False
)


def chmod_dash_r(path, mode):
    """
    Just a little non registered function to chmod a path with file mode.
    """
    for root, dirs, files in os.walk(path, topdown=False):
        for dir in [os.path.join(root, d) for d in dirs]:
            os.chmod(dir, mode)
    for file in [os.path.join(root, f) for f in files]:
        os.chmod(file, mode)

def sudo_warning():
    """
    A little non registered function to remind a user they might need to
    employ the use of sudo/su to properly run this paver command.
    """
    if os.getuid() > 0:
        print("-"*60)
        print("   WARNING: This unprivleged UID may need to use sudo/su.")
        print("-"*60)

@task
@needs('install')
def load_extensions(options):
    """
    LOAD the extensions
    """
    sudo_warning()
    if os.path.isdir("/srv/pyjojo"):
        shutil.rmtree("/srv/pyjojo")
    shutil.copytree("./srv/pyjojo", ("/srv/pyjojo"))
    chmod_dash_r("/srv/pyjojo", 0755)

@task
def install_deps():
    """
    INSTALL_DEPS for the package to run
    """
    sudo_warning()
    for dependecy in install_requires:
        sh('pip install {package}'.format(package=dependecy))

@task
@needs('load_extensions')
def start():
    """
    START a dev instance for test
    """
    sudo_warning()
    sh('opsapi --dir=/srv/pyjojo')


@task
def clean(options):
    """
    CLEAN after paver operations
    """
    for i in ['./dist', './build', './opsapi.egg-info']:
        print("Removing {file}".format(file=i))
        try:
            shutil.rmtree(i)
        except OSError:
            pass
