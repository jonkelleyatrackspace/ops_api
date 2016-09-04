#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: pavement.py
# authors: jonathan kelley 2016

from paver.easy import *
import paver.doctools
from paver.setuputils import setup
import shutil
import os

def load_kv_from_spec(getkey):
    """
    nonregistered helper that loads the version from the .spec file
    which shall be our source of truth for versioning.

    i looked into using rpm, but the library is really really unwieldy
    not an external api, and looks like it's likely to change
    """
    spec = {}
    with open("opsapi.spec", "r") as f:
        for line in f.readlines():
            try:
                value = line.split(":")[1].lstrip()
                key = line.split(":")[0].lstrip().lower()
                print("X"+str(key))
                spec[key] = value
            except:
                pass
        print(spec)
        return spec[getkey]

__doc__ = """ Setuptools with paver """
install_requires = [
    'pyyaml==3.10',
    'tornado==3.0.1',
    'toro==0.5',
    'passlib==1.6'
]
setup(
    name="opsapi",
    version=load_kv_from_spec('version'),
    author="Jonathan Kelley",
    author_email="jonkelley@gmail.com",
    description="Lightweight API framework with simple extension SDK to allow rapid prototype of infrastructure-as-a-service concepts.",
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
    if os.path.isdir("/srv/extensions"):
        print("Deleting /srv/extensions")
        shutil.rmtree("/srv/extensions")
    print("Installing extensions to /srv/extensions")
    shutil.copytree("./srv/extensions", ("/srv/extensions"))
    chmod_dash_r("/srv/extensions", 0755)

@task
@needs('load_extensions')
def setup():
    """
    SETUP the application by loading the python package, extensions, 
    and pip requirements.
    """
    sudo_warning()
    for dependecy in install_requires:
        sh('pip install {package}'.format(package=dependecy))

@task
@needs('load_extensions')
def start():
    """
    START a local dev instance for testing
    """
    sudo_warning()
    sh('opsapi --dir=/srv/extensions')


@task
def prep_rpmbuild():
    print("TODO")

@task
def make_rpm():
    """
    Builds RPM from the local .spec file.
    """
    print("TODO")

@task
def install_rpms():
    print("TODO")

@task
def reinstall():
    print("TODO")

@task
def uninstall():
    print("TODO")

@task
def uninstall_rpms():
    print("TODO")

@task
def prep_debbuild():
    print("TODO")

@task
def make_deb():
    print("TODO")

@task
def uninstall_debs():
    print("TODO")

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
